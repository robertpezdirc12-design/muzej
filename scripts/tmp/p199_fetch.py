#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P199 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1878).
Okno: s150–s158 (meja-1878/79 = s158 po P198!; meja-1877/78 = išče-nazaj v
s150/s151). Preslikava: inventory-idx = sken − 1 (P197/P198-md5-validirano).
KRIŽNA-VALIDACIJA: sveži-s157/s158-md5 == /tmp/p198-seja (stabilnost-matricule
+ kontinuiteta-verige P197→P198→P199). Recept: P198/P197."""
import base64, hashlib, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p199"
SCANS = range(150, 159)  # s150–s158
REFS = [("s157", "/tmp/p198/s157.jpg"), ("s158", "/tmp/p198/s158.jpg")]


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
    if len(urls) < 158:
        print("inventar premajhen za s158!")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))
    md5s = {}

    for i in SCANS:
        out = f"{OUT}/s{i}.jpg"
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        md5s[f"s{i}"] = md5b(data)
        print(f"sken {i}: {len(data)} B JPEG OK md5={md5s[f's{i}'][:12]}")

    # ——— križna-validacija vs P198-seja ———
    ok = True
    for name, ref in REFS:
        disk = md5b(open(ref, "rb").read())
        same = disk == md5s.get(name)
        print(f"KRIŽNI-MD5 {name}: svež={md5s.get(name, '')[:12]} disk={disk[:12]} → {'1:1 ✓' if same else '✗ ODMAK!'}")
        ok = ok and same
    if not ok:
        print("md5-križna-validacija NEUSPEŠNA!")
        sys.exit(2)
    json.dump(md5s, open(f"{OUT}/md5s.json", "w"), indent=1)
    print("→ preslikava: inventory-idx = sken − 1 (P197/P198-md5-veriga + TA-seja-3.×)")


if __name__ == "__main__":
    main()
