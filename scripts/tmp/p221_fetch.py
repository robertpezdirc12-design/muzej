#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P221 delovna faza — prenos skenov KRSTNE knjige 04104 (PREDZGODOVINA 1871–1885 — 1/15, leto 1885!).
NOVA-LINIJA: krstna-predzgodovina (mrliška-04106-KONČANA-29/29-P220!).
Knjiga 04104 = STAREJŠI-zvezek-krstne (04105 = 1886–1919-korpus!) — 200 slik.
 descending-vzorec: start-1885 = ZADNJE leto knjige → okno-proba: zadnjih-skenov.
2×-NEODVISNA-PRENOSA vsak (md5-samoskladnost; P211/P219/P220-recept!)."""
import hashlib, json, os, sys, time, urllib.request, urllib.error, base64, re

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p221"
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
    print(f"inventar 04104: {len(urls)} slik")
    os.makedirs(OUT, exist_ok=True)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))

    if PROBE:
        for i in PROBE:
            out = f"{OUT}/s{i}.jpg"
            if os.path.exists(out):
                print(f"sken {i}: ŽE na disku"); continue
            st2, d1 = http_get(urls[i - 1])
            if st2 != 200 or d1[:2] != b"\xff\xd8":
                print(f"sken {i}: HTTP {st2} — NI JPEG"); continue
            st3, d2 = http_get(urls[i - 1])
            m1, m2 = md5b(d1), md5b(d2)
            same = (m1 == m2) and d2[:2] == b"\xff\xd8"
            with open(out, "wb") as f: f.write(d1 if same else d2)
            print(f"PROBE sken {i}: {len(d1)} B JPEG OK md5={m1[:12]} 2×-križ={'1:1 ✓' if same else '✗ NESTABILNO!'}")
        return

    # polno okno: privzeto iz okolja P221_WINDOW (npr. "190-200")
    lo, hi = (int(x) for x in os.environ.get("P221_WINDOW", "190-200").split("-"))
    md5s = {}
    ok = True
    for i in range(lo, hi + 1):
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
    print("→ veriga-P221 2×-samoskladnost-" + ("OK" if ok else "POZOR: odmik!"))


if __name__ == "__main__":
    main()
