#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 delovna faza — prenos skenov MRLIŠKE PREDHODNICE 04106 (1857–1885).
Strategija: braanje OD ZADAJ — zadnja leta knjige (1885 = šiv z 04894-1886!).
Ni del repozitorija: delovni imenik /tmp/p192."""
import base64, re, sys, urllib.request, urllib.error, os

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p192"

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
    print(f"inventar 04106: {len(urls)} slik")
    with open("/tmp/p192/inventory.txt", "w") as f:
        for u in urls:
            f.write(u + "\n")
    # download requested scans
    args = [int(a) for a in sys.argv[1:]]
    os.makedirs(OUT, exist_ok=True)
    for i in args:
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 10000:
            print(f"s{i}: ŽE"); continue
        st2, data = http_get(urls[i-1])
        if st2 == 200 and len(data) > 10000:
            with open(out, "wb") as f:
                f.write(data)
            print(f"s{i}: OK {len(data)}")
        else:
            print(f"s{i}: FAIL HTTP {st2} len {len(data)}")

if __name__ == "__main__":
    main()
