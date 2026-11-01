#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P172 delovna faza — prenos skenov mrliške knjige 04894 (leto 1906: skeni 105–110).
Ni del repozitorija: delovni imenik /tmp/p172 (po vzoru P171 /tmp/p171)."""
import base64, re, sys, urllib.request, urllib.error, os

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p172"
SCANS = range(105, 111)  # skeni 105–110 (celo leto 1906 + uvod 1907 — meja 1906/07 [~ s107+?])


def http_get(url, headers=UA, tries=4):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:
            last = e
    raise last


def decode_inventory(html):
    urls = []
    for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
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
        print(f"knjiga HTTP {st}"); sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "replace"))
    print(f"inventar: {len(urls)} slik")
    if len(urls) < 111:
        print(f"OPOZORILO: pričakovano >= 111 skenov, najdeno {len(urls)}")
    os.makedirs(OUT, exist_ok=True)
    for i in SCANS:
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"sken s{i}: že obstaja, preskočim"); continue
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken s{i}: HTTP {st2} — NI JPEG"); sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        print(f"sken s{i}: {len(data)} B JPEG OK")


if __name__ == "__main__":
    main()
