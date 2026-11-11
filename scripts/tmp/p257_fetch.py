#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — notranjost poročne knjige 01738 (1828–1873): LETO 1830/1831.
Delovni imenik /tmp/p257 (po vzoru P256/P255/P253). Skeni s6–s7 (razprti listi):
- s6: Pag. 9 — vrstice 1829 m18–m20 (P256) + RESTART-1830 na r4 (12. Jänner 1830)
      + 8 vpisov 1830 (12. Jän + 17. Febr ×4 + 18. + 21. + 30. Juni) do r11
- s7: Pag. 11 — leto 1831 (26. Jän 1831 + 1./9. Febr + dt°-vrstice; Griblje 3/50/56/65/1/(20?)!)
Metoda P256/P255/P253: viewer-HTML → 147-base64-URL dekodiranih → direct-JPG
+ 2× neodvisna prenesa md5 (skupaj 4. neodvisni prenos — P256 je že 2× prenesla!)."""
import base64, hashlib, os, re, sys, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p257"
SCANS = [6, 7]


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
        print("WARNING: P255/P253-claim 147 URLs, got", len(urls))
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
    # 2. neodvisna prenesa = md5 dvojno preverjanje (P242/P253/P255/P256 metoda!)
    print("--- md5 double-check (2. neodvisni prenos; skupaj 4. s P256!) ---")
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
