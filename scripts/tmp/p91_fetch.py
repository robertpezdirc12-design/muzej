#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P90 delovna faza — prenos skenov krstne knjige 04105 (leto 1896: skeni 85–94).
Delovni imenik /tmp/p91 (po vzoru P86–P89). Okvir: 1895 se začne NA STRANI 76 =
sken 78 row 1 po 1894 row 90 (P89: velike cifre »1895~« na str. 76). Skeni 78–81
že v /tmp/p89 (kopirani). NOVELA P89: stran == sken − 2 od skena 74 naprej
(sken 78 = str. 76 … sken 88 = str. 86). Leto 1895 dolžina neznana (~75–90
vrstic po vzoru 1890–1894) — prenesemo skeni 78–88 (strani 76–86), dovolj za
celo leto + prelom 1896."""
import base64, re, sys, urllib.request, urllib.error, os

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p91"
SCANS = range(85, 95)  # skeni 78–88 (str. 76–86)


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
