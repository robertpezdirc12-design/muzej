#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P241 delovna faza — prenos skenov POROČNE knjige 04455 (PREDZGOVINA, leto 1882 = 4/13).
Descending-vzorec: tail-1882-vpisi-24–26 = s50-TOP (P240-1:1!) → leto 1882 teče nazaj
čez s49/s48/s47/s46 (restart-1882 + tail-1881 nekje tam). Recept: P238 (2×-md5)."""
import hashlib, json, os, sys, time, urllib.request, urllib.error, base64, re

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p241"
SCANS = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [45, 46, 47, 48, 49, 50]


def http_get(url, headers=UA, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(3 * (i + 1)); last = e; continue
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise last


def decode_inventory(html):
    urls = []
    for m in re.finditer(r'"(/image/[A-Za-z0-9+/=%]+/)"', html):
        s = m.group(1)[7:-1]
        try:
            d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
            if d.startswith("http"): urls.append(d)
        except Exception: pass
    return sorted(set(urls))


def md5b(data): return hashlib.md5(data).hexdigest()


def main():
    st, body = http_get(BOOK_URL)
    if st != 200: print(f"knjiga HTTP {st}"); sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "replace"))
    print(f"inventar 04455: {len(urls)} slik")
    os.makedirs(OUT, exist_ok=True)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))
    for i in SCANS:
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"sken {i}: ŽE na disku"); continue
        st2, d1 = http_get(urls[i - 1])
        if st2 != 200 or d1[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} / ni JPEG"); continue
        st3, d2 = http_get(urls[i - 1])
        if md5b(d1) != md5b(d2):
            print(f"sken {i}: MD5-NEUJEMANJE ({md5b(d1)[:10]} vs {md5b(d2)[:10]})"); continue
        open(out, "wb").write(d1)
        print(f"sken {i}: OK {len(d1)}B md5={md5b(d1)[:10]}")
        time.sleep(1.2)


if __name__ == "__main__":
    main()
