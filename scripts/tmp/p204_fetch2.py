#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P204 faza-2 — išče-nazaj: prenos skenov s100–s109 (s110 je ŠE sredina-1873: zaporedne 87–99,
brez restarta, kolera-August!). Meja-1872/73 (restart + 'Incipit annus Domini 1873') je pred s110.
KRIŽNA-VALIDACIJA: sveži-s110/s111-md5 == /tmp/p204-disk (1:1 → kontinuiteta verige!).
Preslikava: inventory-idx = sken − 1; pag = sken − 5 (LEKCIJA-#21, preverjati natisnjene-št.!)."""
import base64, hashlib, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p204"
NEW = range(100, 110)   # s100–s109 (sveže!)
REFS = [("s110", "/tmp/p204/s110.jpg"), ("s111", "/tmp/p204/s111.jpg")]


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
    if len(urls) < 111:
        print("inventar premajhen za P204-s111!")
        sys.exit(1)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))
    md5s = json.load(open(f"{OUT}/md5s.json")) if os.path.exists(f"{OUT}/md5s.json") else {}

    # ——— sveži s100–s109 ———
    for i in NEW:
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out):
            print(f"sken {i}: ŽE-na-disku")
            md5s.setdefault(f"s{i}", md5b(open(out, "rb").read()))
            continue
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        md5s[f"s{i}"] = md5b(data)
        print(f"sken {i}: {len(data)} B JPEG OK md5={md5s[f's{i}'][:12]}")

    # ——— KRIŽNA-validacija s110/s111 (že na P204-disku) ———
    ok = True
    for name, ref in REFS:
        i = int(name[1:])
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"{name}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        fresh = md5b(data)
        disk = md5b(open(ref, "rb").read())
        same = fresh == disk
        print(f"KRIŽNI-MD5 {name}: svež={fresh[:12]} disk={disk[:12]} → {'1:1 ✓' if same else '✗ ODMAK!'}")
        ok = ok and same
        md5s[name] = fresh if same else disk
    if not ok:
        print("⚠ md5-križna-validacija: vsaj-1-ODMAK!")

    json.dump(md5s, open(f"{OUT}/md5s.json", "w"), indent=1)
    print("→ veriga P197→…→P203→P204-8.× (2. krog: s100–s109 + s110/s111-potrditev)")


if __name__ == "__main__":
    main()
