#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P97 delovna faza — prenos skenov krstne knjige 04105 (leto 1902: skeni 135–152).
Delovni imenik /tmp/p97 (po vzoru P90–P96). Okvir: glava »1902« (podčrtana) na
DNNU str. 129 = sken 135 (P96 dokazano); row 1 1902 = str. 130 = sken 136.
NOVELA P96 še velja: stran == sken − 6 (135 → 129, 136 → 130 …) do naslednjega
podvojenega skena. Dolžina leta 1902 neznana (~77–90 vrstic po vzoru 1900/1901)
— prenesemo skeni 141–152 (str. 135–146), dovolj za celo leto + prelom 1903.
Skeni 135–140 kopije iz /tmp/p96."""
import base64, re, sys, urllib.request, urllib.error, os, shutil

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p97"
COPY_FROM = {n: f"/tmp/p96/scan-{n}.jpg" for n in range(135, 141)}  # 135–140
SCANS = range(135, 153)  # skeni 135–152 (str. 129 okvir + 130–146)


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
            print(f"scan-{s}: kopija iz /tmp/p96")
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
