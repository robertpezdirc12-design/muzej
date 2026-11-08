#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P89 delovna faza — prenos skenov krstne knjige 04105 (leto 1894: skeni 70–81).
Delovni imenik /tmp/p89 (po vzoru P86/P87/P88). Okvir: 1894 se začne NA
STRANI 69 = sken 70 row 1 po 1893 row 83 (P88: velike cifre »1894« na str. 69).
Skeni 70–73 že v /tmp/p88 (kopirani). Leto 1894 dolžina neznana (~75–86
vrstic po vzoru 1890–1893) — prenesemo skeni 70–81 (strani 69–80), dovolj za
celo leto + prelom 1895."""
import base64, re, sys, urllib.request, urllib.error, os

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p89"
SCANS = range(70, 82)  # skeni 70–81 (str. 69–80)


def http_get(url, headers=UA, tries=4):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
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
    print("book page:", st)
    if st != 200:
        sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "replace"))
    print("inventory:", len(urls))
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    for s in SCANS:
        if only and s not in only:
            continue
        out = f"{OUT}/scan-{s}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            print(f"scan-{s}: obstoji, preskočim")
            continue
        st, b = http_get(urls[s - 1])
        if st == 200 and b[:2] == b"\xff\xd8":
            open(out, "wb").write(b)
            print(f"scan-{s}: {len(b)} bajtov")
        else:
            print(f"scan-{s}: NAPAKA http={st}")
            sys.exit(1)


if __name__ == "__main__":
    main()
