#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P255 — notranjost poročne knjige 01738 (1828–1872): ZAČETEK.
Delovni imenik /tmp/p255 (po vzoru P243/P253). Skeni s1–s12 (razprti listi):
- s1: verjetno naslovnica/prvi list (cf. s147 = 'Podzemelj III' naslovnica na KONCU!)
- s2–s12: pričakovani prvi vpisi 1828
Metoda P242/P253: viewer-HTML → 147-base64-URL dekodiranih (hosted-images,
trailing-slash-fix) → direct-JPG + 2× neodvisna prenesa md5."""
import base64, hashlib, os, re, sys, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p255"
SCANS = list(range(1, 13))  # s1–s12


def http_get(url, headers=UA, tries=4):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:
            last = e
    raise last


def decode_inventory(html):
    urls = []
    for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
        s = m.group(1)[7:-1]
        try:
            d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
            if d.startswith("http"):
                urls.append(d)
        except Exception:
            pass
    return sorted(set(urls))


def main():
    os.makedirs(OUT, exist_ok=True)
    st, body = http_get(BOOK_URL)
    print("book page:", st, "bytes:", len(body))
    if st != 200:
        sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "ignore"))
    print("decoded URLs:", len(urls))
    if len(urls) != 147:
        print("WARNING: P253-claim 147 URLs, got", len(urls))
    if len(urls) < 40:
        sys.exit(2)
    for s in SCANS:
        idx = s - 1  # sken N = N-ti URL (1-based)
        if idx >= len(urls):
            print(f"s{s}: izven inventarja!")
            continue
        u = urls[idx]
        if u.endswith("/"):
            u = u[:-1]
        out = f"{OUT}/s{s}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            print(f"s{s}: že obstaja ({os.path.getsize(out)} B)")
        else:
            st2, data = http_get(u)
            if st2 != 200 or len(data) < 50000:
                print(f"s{s}: FAIL status={st2} len={len(data)}")
                sys.exit(3)
            with open(out, "wb") as f:
                f.write(data)
        md5 = hashlib.md5(open(out, "rb").read()).hexdigest()
        print(f"s{s}: {os.path.getsize(out)} B md5={md5}")
    # 2. neodvisna prenesa = md5 dvojno preverjanje (P242/P253 metoda!)
    print("--- md5 double-check (2. neodvisni prenos) ---")
    bad = 0
    for s in SCANS:
        idx = s - 1
        if idx >= len(urls):
            continue
        u = urls[idx]
        if u.endswith("/"):
            u = u[:-1]
        st2, data2 = http_get(u)
        md5a = hashlib.md5(open(f"{OUT}/s{s}.jpg", "rb").read()).hexdigest()
        md5b = hashlib.md5(data2).hexdigest()
        ok = "1:1" if (st2 == 200 and md5a == md5b) else "RAZLIKA!"
        if ok != "1:1":
            bad += 1
        print(f"s{s}: 2.prenes status={st2} md5={md5b} {ok}")
    print("DONE", "NAPAKE:", bad)


if __name__ == "__main__":
    main()
