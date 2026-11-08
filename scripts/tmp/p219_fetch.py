#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P219 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1858 = 28/29!).
Okvir-proba: s004–s011 (8 skenov). ZNANO iz P218: s11-tail-ŽE-VLM (tail-54–57-1858:
4-vrstice + VSOTNA-'1 8 [5 9]'-marker + '1858'-glava-KROP — 0-GRIBLJE-tail!) →
MEJA-1857/58 = išči-nazaj → PROBA s004–s011! (1858 ≈ 57+ vpisov → start ≈ s006/s007.)
SANDBOX-REZET: brez-carryja (veriga-md5-RESTART — vsebinska-križ-bo-v-build_entries!).
NOVI skeni s004–s011: 2×-NEODVISNA-PRENOSA vsak (md5-samoskladnost; P211-recept!)."""
import hashlib, json, os, sys, time, urllib.request, urllib.error, base64, re

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p219"
NEW = range(4, 12)  # s004-s011: proba za MEJO-1857/58 + celo leto 1858


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
    ok = True
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
    print("→ veriga-P219 2×-samoskladnost-" + ("SANDI-REZET-RESTART-OK" if ok else "POZOR: odmak!"))


if __name__ == "__main__":
    main()
