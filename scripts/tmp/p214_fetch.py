#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P214 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1863 = 23/29!).
Okvir-proba: s033–s039 (7 skenov; pag 28–34 = sken−5).
ZNANO iz P213-lead/meja: s39-vrstice-1–10 = 1863-tail z55–z64 (ŽE-VLM v /tmp/p213/vlm-page/s39.json!)
+ vsotna '1-8-6-4' + restart-z1–z2 (1864). 1863-z1–z54 → PROBA s033–s038!
s39.jpg PRENESEN iz /tmp/p213 (md5-križ proti /tmp/p213/md5s.json — veriga-P213 11.×!).
NOVI skeni s033–s038: 2×-NEODVISNA-PRENOSA vsak (md5-samoskladnost; P211–P213 recept)."""
import hashlib, json, os, shutil, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p214"
OLD = "/tmp/p213"
NEW = range(33, 39)   # s033-s038: proba za MEJO-1862/63 (s39-tail z55–z64 že znan!)
CARRY = 39            # s39: prenos iz /tmp/p213 + md5-križ


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


import base64, re


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

    # 1) CARRY s39 iz /tmp/p213 + md5-križ
    src = f"{OLD}/s{CARRY}.jpg"
    dst = f"{OUT}/s{CARRY}.jpg"
    old_md5 = json.load(open(f"{OLD}/md5s.json")).get(f"s{CARRY}")
    if os.path.exists(src):
        d = open(src, "rb").read()
        m = md5b(d)
        match = (old_md5 is None) or (m == old_md5)
        ok = ok and match
        shutil.copyfile(src, dst)
        md5s[f"s{CARRY}"] = m
        print(f"sken {CARRY} (CARRY iz P213): {len(d)} B md5={m[:12]} križ-vs-P213-md5={'1:1 ✓' if match else '✗ RAZLIKA!'}")
    else:
        print(f"sken {CARRY}: /tmp/p213 NI VEČ — fresh 2×-prenos")
        st2, d1 = http_get(urls[CARRY - 1]); st3, d2 = http_get(urls[CARRY - 1])
        m1, m2 = md5b(d1), md5b(d2)
        same = (m1 == m2) and d1[:2] == b"\xff\xd8"
        ok = ok and same
        with open(dst, "wb") as f: f.write(d1 if same else d2)
        md5s[f"s{CARRY}"] = m1 if same else m2
        print(f"sken {CARRY} (fresh): md5={md5s[f's{CARRY}'][:12]} 2×={'1:1 ✓' if same else '✗'}")

    # 2) NOVI skeni s033–s038: 2×-neodvisna prenosa
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
    print("→ veriga-P213 2×-samoskladnost-" + ("11.×-OK" if ok else "POZOR: odmak!"))


if __name__ == "__main__":
    main()
