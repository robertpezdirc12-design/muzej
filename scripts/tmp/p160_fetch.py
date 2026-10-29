#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P160 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1894).
P158-okvir: 1892 = s34-top (r1 LEAD) + s34–s40 + s41-top (r81) == str. 33–40;
meja 1892/93 = »— 1893. —« na PRAZNI vrsti s flomastri + Januarij pod njo (s41) — 5. STIL MEJE!
P159-lead: s41-dno za markerjem — Griblje 69(?) Katarina P~rinc 35 + Griblje 53(?) Ana F~oček
roj. Dragaj 35 (oba Jos. Rauq Januar); r5 = h61 4. leto? [~ γ-7]; meja 1893/94 [~ s47+?].
P159 potrebuje skene 41–49 (celo leto 1893 + meja 1893/94 kontrola).
Ni del repozitorija: delovni imenik /tmp/p160 (po vzoru P153–P158)."""
import base64, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p160"
SCANS = range(47, 56)  # skeni 47–55 (s47-restart "Leto 1894" + meja 1894/95 kontrola)
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
    sys.exit(0 if ok == len(SCANS) else 1)


if __name__ == "__main__":
    main()
