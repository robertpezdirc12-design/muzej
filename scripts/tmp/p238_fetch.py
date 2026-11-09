#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P238 delovna faza — prenos skenov POROČNE knjige 04455 (PREDZGOVINA 1873–1885 — 1/13, leto 1885!).
NOVA-LINIJA: poročna-predzgodovina (krstna-04104-KONČANA-15/15-P235+P236-sinteza! + forenzika-P237!).
Knjiga 04455 = 1873–1922; GLAVNA-linija (P84+) je brala s58–s68 za 1886 → PREDZGOVINA = s1–s57!
Descending-vzorec: start-1885 = ZADNJE leto predzgodovine → okno-proba: s54–s60 (meja!).
2×-NEODVISNA-PRENOSA vsak (md5-samoskladnost; P221/P237-recept!)."""
import hashlib, json, os, sys, time, urllib.request, urllib.error, base64, re

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p238"
PROBE = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[1] == "-probe" else None


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

    if PROBE:
        for i in PROBE:
            out = f"{OUT}/s{i}.jpg"
            if os.path.exists(out):
                print(f"sken {i}: ŽE na disku"); continue
            st2, d1 = http_get(urls[i - 1])
            if st2 != 200 or d1[:2] != b"\xff\xd8":
                print(f"sken {i}: HTTP {st2} / ni JPEG"); continue
            st3, d2 = http_get(urls[i - 1])
            m1, m2 = md5b(d1), md5b(d2)
            if m1 != m2:
                print(f"sken {i}: MD5-NEUJEMANJE ({m1} vs {m2})"); continue
            open(out, "wb").write(d1)
            print(f"sken {i}: OK {len(d1)}B md5={m1[:10]}")
        return

    # polni prenos iz args: -range A,B
    if len(sys.argv) > 2 and sys.argv[1] == "-range":
        a, b = [int(x) for x in sys.argv[2].split(",")]
        for i in range(a, b + 1):
            out = f"{OUT}/s{i}.jpg"
            if os.path.exists(out):
                print(f"sken {i}: ŽE"); continue
            st2, d1 = http_get(urls[i - 1])
            if st2 != 200 or d1[:2] != b"\xff\xd8":
                print(f"sken {i}: HTTP {st2}"); continue
            st3, d2 = http_get(urls[i - 1])
            if md5b(d1) != md5b(d2):
                print(f"sken {i}: MD5-NEUJEMANJE"); continue
            open(out, "wb").write(d1)
            print(f"sken {i}: OK {len(d1)}B")
            time.sleep(1.2)
        return
    print("uporaba: -probe 54,55,56,57,58,59,60 | -range A,B")


if __name__ == "__main__":
    main()
