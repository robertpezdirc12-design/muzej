#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P233 delovna faza — prenos skenov KRSTNE knjige 04104 (PREDZGODOVINA 13/15, leto 1873!).
LEAD-P232: MEJA-1873/74 = s37-SREDI-PAGI-'Initium-anni-Domini-1874' (ŽE-POTRJENA!).
  TAIL-1873 = s36-r1–r10 (zap-88–97!-vsi-November!) + s37-r1 (zap-28[~98]-Dez-28/29!).
  → MEJA-1872/73-PRED-s36 → probe-s28–s36 (DESCENDING — po potrebi nazaj!).
Pričakovana gola-pag-'sken−3': s36='33' (P232-potrjena!) ... s35='32'!-s30='27'!-s28='25'!.
★★★ POZOR: 2-DUPLIKATA-še-vedno-neznana-lokacija-s1–s35! Zaporedje-LAHKO-skoči!
  TROJNI-DUPLIKAT-s60=s61=s62-P231-dokazano-izven-okna ('sken−3'-formula-do-s60!).
1873-vpisov-pričakovano-~97/98 (zap-97-s36-r10-Nov-28!-+Dez-28-tail-zap-28[~98]!-X-open!).
'Initium-anni-Domini-1873'-kalligrafija-LAHKO-se-ponovi (če-leto-1873-ne-konča-sredinsko!-ali-'finis-Anni-1872'!).
2×-NEODVISNA-PRENOSA vsak (md5-samoskladnost; P211/P219–P232-recept!)."""
import hashlib, json, os, sys, time, urllib.request, urllib.error, base64, re

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p233"  # P233-lastni-dir (fresh!)
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


def fetch_one(urls, i, out):
    st2, d1 = http_get(urls[i - 1])
    if st2 != 200 or d1[:2] != b"\xff\xd8":
        print(f"sken {i}: HTTP {st2} — NI JPEG"); return None
    st3, d2 = http_get(urls[i - 1])
    m1, m2 = md5b(d1), md5b(d2)
    same = (m1 == m2) and d2[:2] == b"\xff\xd8"
    with open(out, "wb") as f: f.write(d1 if same else d2)
    print(f"sken {i}: {len(d1)} B JPEG OK md5={m1[:12]} 2×-križ={'1:1 ✓' if same else '✗ NESTABILNO!'}")
    return m1


def main():
    inv = f"{OUT}/inventory.json"
    if os.path.exists(inv):
        urls = json.load(open(inv))
        print(f"inventar 04104: {len(urls)} slik (že na disku)")
    else:
        st, body = http_get(BOOK_URL)
        if st != 200: print(f"knjiga HTTP {st}"); sys.exit(1)
        urls = decode_inventory(body.decode("utf-8", "replace"))
        print(f"inventar 04104: {len(urls)} slik")
        os.makedirs(OUT, exist_ok=True)
        json.dump(urls, open(inv, "w"))

    if PROBE:
        for i in PROBE:
            out = f"{OUT}/s{i}.jpg"
            if os.path.exists(out):
                print(f"sken {i}: ŽE na disku"); continue
            fetch_one(urls, i, out)
        return

    lo, hi = (int(x) for x in os.environ.get("P233_WINDOW", "28-36").split("-"))
    md5s = {}
    for i in range(lo, hi + 1):
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out):
            print(f"sken {i}: ŽE na disku"); continue
        m = fetch_one(urls, i, out)
        if m is None: sys.exit(1)
        md5s[i] = m
    json.dump({str(k): v for k, v in md5s.items()}, open(f"{OUT}/md5_p233.json", "w"))
    print(f"prenos okno {lo}-{hi}: končano")


if __name__ == "__main__":
    main()
