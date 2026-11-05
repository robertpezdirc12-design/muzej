#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P217 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1860 = 26/29!).
Okvir-proba: s023–s029 (7 skenov; pag 18–24 = sken−5).
ZNANO iz P216: s23-ŽE-VLM (z40–z52: 13-vrstic-1860!) + s24 (z53–z66: 14!) + s25-tail (WRITTEN-53–59: 7!) — 34-vrstic-1860-znanih; z1–z39 → PROBA s017–s022!
s023 PRENESEN iz /tmp/p216 (md5-križ proti /tmp/p215/md5s.json — veriga-P216 14.×!).
NOVI skeni s023–s028: 2×-NEODVISNA-PRENOSA vsak (md5-samoskladnost; P211–P215 recept)."""
import hashlib, json, os, shutil, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p217"
OLD = "/tmp/p216"
CARRIES = [23]         # s023: prenos iz /tmp/p216 + md5-križ
NEW = range(17, 23)      # s017-s022: proba za MEJO-1859/60 (z1–z39!)


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


import base64, re


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

    old_md5s = json.load(open(f"{OLD}/md5s.json"))
    md5s = {}
    ok = True

    # 1) CARRIES s029/s030 iz /tmp/p215 + md5-križ
    for c in CARRIES:
        src = f"{OLD}/s{c}.jpg"
        dst = f"{OUT}/s{c}.jpg"
        old_md5 = old_md5s.get(f"s{c}")
        if os.path.exists(src):
            d = open(src, "rb").read()
            m = md5b(d)
            match = (old_md5 is None) or (m == old_md5)
            ok = ok and match
            shutil.copyfile(src, dst)
            md5s[f"s{c}"] = m
            print(f"sken {c} (CARRY iz P216): {len(d)} B md5={m[:12]} križ-vs-P216-md5={'1:1 ✓' if match else '✗ RAZLIKA!'}")
        else:
            print(f"sken {c}: /tmp/p216 NI VEČ — fresh 2×-prenos")
            st2, d1 = http_get(urls[c - 1]); st3, d2 = http_get(urls[c - 1])
            m1, m2 = md5b(d1), md5b(d2)
            same = (m1 == m2) and d1[:2] == b"\xff\xd8"
            ok = ok and same
            with open(dst, "wb") as f: f.write(d1 if same else d2)
            md5s[f"s{c}"] = m1 if same else m2
            print(f"sken {c} (fresh): md5={md5s[f's{c}'][:12]} 2×={'1:1 ✓' if same else '✗'}")

    # 2) NOVI skeni s023–s028: 2×-neodvisna prenosa
    for i in NEW:
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out):
            print(f"sken {i}: ŽE na disku"); continue
        st2, d1 = http_get(urls[i - 1])
        if st2 != 200 or d1[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG"); sys.exit(1)
        st3, d2 = http_get(urls[i - 1])
        m1, m2 = md5b(d1), md5b(d2)
        same = (m1 == m2) and d2[:2] == b"\xff\xd8"
        ok = ok and same
        with open(out, "wb") as f: f.write(d1 if same else d2)
        md5s[f"s{i}"] = m1 if same else m2
        print(f"sken {i}: {len(d1)} B JPEG OK md5={m1[:12]} 2×-križ={'1:1 ✓' if same else '✗ NESTABILNO!'}")

    json.dump(md5s, open(f"{OUT}/md5s.json", "w"), indent=1)
    print("→ veriga-P215 2×-samoskladnost-" + ("13.×-OK" if ok else "POZOR: odmak!"))


if __name__ == "__main__":
    main()
