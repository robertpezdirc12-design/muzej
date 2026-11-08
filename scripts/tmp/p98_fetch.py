#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P98 delovna faza — prenos skenov krstne knjige 04105 (leto 1903: skeni 141–170).
Ni del repozitorija: delovni imenik /tmp/p98 (po vzoru P85 /tmp/p85, P96 /tmp/p96, P97 /tmp/p97)."""
import base64, re, sys, urllib.request, urllib.error, os

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p98"
SCANS = range(141, 171)  # skeni 141–170 (1902 konec + celo leto 1903 + uvod 1904)


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
    print(f"inventar: {len(urls)} slik (pričakovano 326)")
    if len(urls) != 326:
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    for i in SCANS:
        out = f"{OUT}/scan-{i:02d}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"sken {i}: že obstaja, preskočim"); continue
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG"); sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        print(f"sken {i}: {len(data)} B JPEG OK")


if __name__ == "__main__":
    main()
