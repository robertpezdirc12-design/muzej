#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P220 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1857 = 29/29 — ZADNJE leto!).
Okvir-proba: s001–s007 (7 skenov). ZNANO iz P219-lead: s004–s006-ŽE-VLM-v-P219-seji
(s004: z33–z45-13-vrstic-Juni–August + s005: z46–z58-13 + s006: z59–z72-14!) +
tail-1857-ŽE-KROP'd (s7-z73–z74: Gradac + GRIBLJE-h36!) → s001–s003-NAZAJ-PROBA
(knjiga-04106-SE-ZAČNE-1857 — morda-naslovni-listi-s001–s003!).
SANDBOX-REZET: brez-carryja (veriga-md5-RESTART — vsebinska-križ-bo-v-build_entries!).
NOVI skeni s001–s007: 2×-NEODVISNA-PRENOSA vsak (md5-samoskladnost; P211/P219-recept!)."""
import hashlib, json, os, sys, time, urllib.request, urllib.error, base64, re

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p220"
NEW = range(1, 8)  # s001-s007: naslovni-listi + celo leto 1857 (z1–z32?) + s7-tail-križ


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
    print("→ veriga-P220 2×-samoskladnost-" + ("SANDI-REZET-RESTART-OK" if ok else "POZOR: odmik!"))


if __name__ == "__main__":
    main()
