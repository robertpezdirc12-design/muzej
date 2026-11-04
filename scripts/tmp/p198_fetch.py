#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P198 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1879).
SANACIJA-RE-RUN: /tmp wiped → ponovni-prenos s157–s164 (inventar 04106-208).
Preslikava: inventory-idx = sken − 1 (P197-md5-validirano + TA-seja-2.×);
VALIDACIJA: vizualna (s158-'Incipit-annus' + s164-tail-z62/z63-KROP-žegnano!)
+ ordinalna-kontinuiteta. Recept: P153/P126/P197."""
import base64, hashlib, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p198"
SCANS = range(157, 165)  # probe s157–s164


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


def md5b(data):
    return hashlib.md5(data).hexdigest()


def main():
    st, body = http_get(BOOK_URL)
    if st != 200:
        print(f"knjiga HTTP {st}")
        sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "replace"))
    print(f"inventar 04106: {len(urls)} slik")
    if len(urls) < 164:
        print("inventar premajhen za s164!")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))

    for i in SCANS:
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"sken {i}: že obstaja, preskočim")
            continue
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        print(f"sken {i}: {len(data)} B JPEG OK md5={md5b(data)[:12]}")

    print("→ preslikava: inventory-idx = sken − 1 (P197-md5-2×-validirano; vizualna-validacija-sledi!)")


if __name__ == "__main__":
    main()
