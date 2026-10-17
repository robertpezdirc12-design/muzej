#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P96 delovna faza — prenos skenov krstne knjige 04105 (leto 1901: skeni 125–140).
Delovni imenik /tmp/p96 (po vzoru P90–P95). Okvir: 1901 se začne na str. 122 =
sken 125 = glava (row 1 = Griblje 12 Peter, Januarius 3/4). NOVELA P96: sken 128
je PODVOJENA fotografija str. 124 (nalepki prepognjeni — r32/r33 vidna), zato od
skena 129 stran == sken − 4 (129→125, 130→126, …) — velja do naslednjega
podvojenega skena. Leto 1901: rows 1–35 na str. 122–124 (skeni 125–128);
dolžina neznana (~75–94 vrstic po vzoru 1890–1900) — prenesemo skeni 129–140
(str. 125–136), dovolj za celo leto + prelom 1902. Skeni 125–128 kopije iz /tmp/p95."""
import base64, re, sys, urllib.request, urllib.error, os, shutil

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p96"
COPY_FROM = {125: "/tmp/p95/scan-125.jpg", 126: "/tmp/p95/scan-126.jpg",
             127: "/tmp/p95/scan-127.jpg", 128: "/tmp/p95/scan-128.jpg"}
SCANS = range(125, 141)  # skeni 125–140 (str. 122–124 + 125–136)


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
            print(f"scan-{s}: kopija iz /tmp/p95")
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
