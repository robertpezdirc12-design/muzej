#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P195 delovna faza — prenos skenov MRLIŠKE PREDZGODOVINE 04106 (leto 1882 = 4/29).
P194-LEAD: 1882 = s180–s186 (Pag. 174–180 = sken − 6!); 1882 = z1–z59 —
s186-z59-Dragoše ŽE viden (P194-tail!), z1–z58 na s180–s185;
meja-1881/82 = s180/s181-probe. Ni del repozitorija: /tmp/p195 (po vzoru P192–P194)."""
import base64, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p195"
SCANS = range(180, 187)  # skeni 180–186 (celo leto 1882 + tail-s186-že-viden!)
EXPECTED = 208  # inventar 04106 (P192-T0)


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
    os.makedirs(OUT, exist_ok=True)
    inv = f"{OUT}/inventory.json"
    if os.path.exists(inv):
        urls = json.load(open(inv))
    else:
        st, body = http_get(BOOK_URL)
        if st != 200:
            print(f"knjiga HTTP {st}")
            sys.exit(1)
        urls = decode_inventory(body.decode("utf-8", "replace"))
        json.dump(urls, open(inv, "w"))
    print(f"inventar: {len(urls)} slik (pričakovano {EXPECTED})")
    if len(urls) != EXPECTED:
        sys.exit(1)
    for i in SCANS:
        out = f"{OUT}/s{i:02d}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"sken {i}: že obstaja, preskočim")
            continue
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        print(f"sken {i}: {len(data)} B JPEG OK")


if __name__ == "__main__":
    main()
