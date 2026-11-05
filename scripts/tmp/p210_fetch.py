#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P210 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1867 = 19/29!).
Okno-proba: s057–s063 sveže; s64–s68 (1867-kontekst-zap-36–102 + tail-103-ULEDBA-'valovita-črta'!)
že na P209-disku → md5-KRIŽNA-validacija vs /tmp/p207 (1:1 → veriga P197→…→P207→P210-12.×!)."""
import base64, hashlib, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p210"
NEW = range(57, 64)   # s057–s063 (sveže!)
REFS = [("s78", "/tmp/p207/s78.jpg"), ("s79", "/tmp/p207/s79.jpg"), ("s80", "/tmp/p207/s80.jpg")]


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
    print(f"inventar 04106: {len(urls)} slik")
    os.makedirs(OUT, exist_ok=True)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))
    md5s = {}
    for i in NEW:
        out = f"{OUT}/s{i}.jpg"
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG"); sys.exit(1)
        with open(out, "wb") as f: f.write(data)
        md5s[f"s{i}"] = md5b(data)
        print(f"sken {i}: {len(data)} B JPEG OK md5={md5s[f's{i}'][:12]}")
    ok = True
    for name, ref in REFS:
        i = int(name[1:])
        st2, data = http_get(urls[i - 1])
        fresh = md5b(data); disk = md5b(open(ref, "rb").read())
        same = fresh == disk
        print(f"KRIŽNI-MD5 {name}: svež={fresh[:12]} P209-disk={disk[:12]} → {'1:1 ✓' if same else '✗ ODMAK!'}")
        ok = ok and same
        if same:
            with open(f"{OUT}/{name}.jpg", "wb") as f: f.write(data)
        else:
            import shutil; shutil.copyfile(ref, f"{OUT}/{name}.jpg")
        md5s[name] = fresh if same else disk
    json.dump(md5s, open(f"{OUT}/md5s.json", "w"), indent=1)
    print("→ veriga P197→…→P207→P210-12.×" + ("" if ok else " (POZOR: odmak!)"))


if __name__ == "__main__":
    main()
