#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P162 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1896).
P161-okvir: 1895 = s51-dno + s52–s54 + s55-top (zap 46–52) == str. 50–54;
meja 1895/96 = '1896.' velika PODČRTANA letnica na PRAZNI vrsti s55 +
Januarij + restart zap 1 = 5. STIL MEJE 3. POTRDITEV.
P161-lead za 1896: s55-dno-restart zap1–4 [GRIBLJE-58-Ana-roj.-Primca-vdova-
kolarica-40!] + s56 Stran-55 zap5–16 ×4 Gribljev [14-mrtvorojeno? +
h45-Barbara-Straus-vdova-Zavrtovič-40 + h51 ×2-DVORNA — Peter-URH-vdovec-42-
Nadluha = URH-h32-vez!] + s57+; meja 1896/97 [~ s60+?].
P162 potrebuje skene 55–61 (s55-dno-restart = 1896 začetek + celo leto
+ meja 1896/97). Ni del repozitorija: delovni imenik /tmp/p162 (po vzoru
P153–P161)."""
import base64, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p162"
SCANS = range(55, 62)  # skeni 55–61 (s55-dno-restart = 1896 + celo leto + meja 1896/97)
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
