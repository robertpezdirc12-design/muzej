#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P94 delovna faza — prenos skenov krstne knjige 04105 (leto 1899: skeni 110–120).
Delovni imenik /tmp/p93 (po vzoru P86–P92). Okvir: 1898 se začne na strani 98 =
sken 101 row 86 po 1897 row 85 (P92: prelom potrjen, oznake se ponastavijo na 1;
1899 row 1 = Griblje 12 Marija — novo leto se začne z Griblji!). NOVELA P92: od skena 98
stran == sken − 3 (101→98, 102→99, …) — velja do naslednjega podvojenega skena.
Leto 1898 dolžina neznana (~75–94 vrstic po vzoru 1890–1897) — prenesemo skeni
102–113 (strani 99–110), dovolj za celo leto + prelom 1899. Sken 101 kopija iz
/tmp/p93 (že na disku, str. 98 = prelomna stran)."""
import base64, re, sys, urllib.request, urllib.error, os, shutil

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p94"
COPY_FROM = {110: "/tmp/p93/scan-110.jpg", 111: "/tmp/p93/scan-111.jpg", 112: "/tmp/p93/scan-112.jpg", 113: "/tmp/p93/scan-113.jpg"}
SCANS = range(110, 121)  # skeni 110–120 (str. 107–117)


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
        if s in COPY_FROM and os.path.exists(COPY_FROM[s]):
            shutil.copy(COPY_FROM[s], out)
            print(f"scan-{s}: kopija iz /tmp/p93")
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
