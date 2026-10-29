#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P161 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1895).
P160-okvir: 1894 = s47-restart + s48–s50 + s51-top (zap 49–50) == str. 46–50;
meja 1894/95 = »— 1895. —« velik razporejeni marker na PRAZNI vrsti + Januarij
+ restart zap 1 na s51 = 5. STIL MEJE 2. POTRDITEV!
P160-lead za 1895: s51-dno-restart zap1 = Krasinec-50?/30? Katarina JAKOBČIČ
vdova bajtarca roj. PEZDIREC 70 Nadruha Jelen! + s52 zap 10–21 Feb–Maj
×6 Gribljev [JOŽEK-1-DAN-h38 + PAVČIČ-14-h33 + HRIŠAN-16-mes-h35 +
BRODANIČ?-×2-h46 + PEZDIREC-28-h87!] + s53 ×2 [GRINEC?-36-h26 + HLEVIČ?-60-h37]
+ s54 ×1 [ŠEPINA?-6-mes-h30 — VLM-'Češarek'-podpis = A-napaka!] + s55 ×2
[KRIŽAN-1½-h36 + JAKLOVIČ?-53-h8] = VLM-total 12 — največ odkar 1892-17!
Meja 1895/96 ŽE VIDENTA: s55-'1896.'-velika-letnica + Januar + restart-zap1
= 7. STIL-kandidat!
P161 potrebuje skene 51–56 (s51-dno = 1895 začetek + celo leto + meja 1895/96).
Ni del repozitorija: delovni imenik /tmp/p161 (po vzoru P153–P160)."""
import base64, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p161"
SCANS = range(51, 57)  # skeni 51–56 (s51-dno-restart = 1895 z + meja 1895/96 kontrola)
EXPECTED = 256  # inventar 04894 (P80)


def http_get(url, headers=UA, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(3 * (i + 1))
                last = e
                continue
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    raise last


def decode_inventory(html):
    urls = []
    for m in re.finditer(r'"(/image/[A-Za-z0-9+/=%]+/)"', html):
        s = m.group(1)[7:-1]
        try:
            d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
            if d.startswith("http"):
                urls.append(d)
        except Exception:
            pass
    return sorted(set(urls))


def main():
    st, body = http_get(BOOK_URL)
    if st != 200:
        print(f"knjiga HTTP {st}")
        sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "replace"))
    print(f"inventar: {len(urls)} slik (pričakovano {EXPECTED})")
    if len(urls) != EXPECTED:
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/inventory.json", "w") as f:
        json.dump(urls, f, indent=1)
    ok = 0
    for s in SCANS:
        dst = f"{OUT}/s{s:02d}.jpg"
        if os.path.exists(dst) and os.path.getsize(dst) > 50000:
            ok += 1
            print(f"s{s:02d}: že nazaj ✓")
            continue
        st, data = http_get(urls[s - 1])
        if st == 200 and len(data) > 50000:
            open(dst, "wb").write(data)
            ok += 1
            print(f"s{s:02d}: {len(data)//1024} KB ✓")
        else:
            print(f"s{s:02d}: HTTP {st} ✗")
        time.sleep(1.5)
    print(f"prenos: {ok}/{len(SCANS)}")


if __name__ == "__main__":
    main()
