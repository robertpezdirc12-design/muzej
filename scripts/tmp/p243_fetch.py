#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — prenos skenov poročne knjige 04455 (leto 1880 predzgodovina, 6/13).
Delovni imenik /tmp/p243 (po vzoru P241/P242). Skeni s31–s39 (razprti listi):
- s39-top: letnica '1881' ŽE 1:1 (P242!) — reconciliacija
- s38: tail-1880 pričakovan (P242-material!)
- restart-1880 = neznana lokacija (s31–s38 razpon)
Metoda P242: viewer-HTML → 192-base64-URL dekodiranih (hosted-images,
trailing-slash-fix) → direct-JPG + 2× neodvisna prenesa md5."""
import base64, hashlib, os, re, sys, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p243"
SCANS = list(range(31, 40))  # s31–s39


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
    if len(urls) != 192:
        print("WARNING: expected 192 URLs, got", len(urls))
    if len(urls) < 40:
        sys.exit(2)
    for s in SCANS:
        idx = s - 1  # sken N = N-ti URL (1-based)
        if idx >= len(urls):
            print(f"s{s}: izven inventarja!")
            continue
        u = urls[idx]
        # trailing-slash-fix (P242 NOV RAZRED): hosted-images URL ima včasih /
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
    print("DONE")


if __name__ == "__main__":
    main()
