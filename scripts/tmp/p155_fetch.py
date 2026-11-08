#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P155 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1889).
P154-okvir: 1888 = s13-dno–s21 (102 vrstic); meja 1889 = veliki cifri »1 8 8 9«
čez prazno vrsto na s21 + ozek stolpec restarta 1–6; 1889 r4 (Griblje h53 Ana
Perdihec, 25.1.) = P155-lead že forenzično izrezan. P155 potrebuje s21–s3x
(celo leto 1889 + meja 1890). Ni del repozitorija: delovni imenik /tmp/p155."""
import base64, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p155"
SCANS = range(21, 33)  # s21–s32 (celo leto 1889 + meja 1890; s21/s22 kopirani)
EXPECTED = 256  # inventar 04894 (P80)


def http_get(url, headers=UA, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(3 * (i + 1))
                last = e
                continue
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    raise last


def decode_inventory(html):
    urls = []
    for m in re.finditer(r'"(/image/[A-Za-z0-9+/=%]+/)"', html):
        s = m.group(1)[7:-1]
        try:
            d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
            if d.startswith("http"):
                urls.append(d)
        except Exception:
            pass
    return sorted(set(urls))


def main():
    st, body = http_get(BOOK_URL)
    if st != 200:
        print(f"knjiga HTTP {st}")
        sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "replace"))
    print(f"inventar: {len(urls)} slik (pričakovano {EXPECTED})")
    if len(urls) != EXPECTED:
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/inventory.json", "w") as f:
        json.dump(urls, f)
    # s21/s22 že v /tmp/p154 — kopiraj
    for src in (21, 22):
        dst = f"{OUT}/s{src:02d}.jpg"
        if not os.path.exists(dst):
            srcp = f"/tmp/p154/s{src:02d}.jpg"
            if os.path.exists(srcp):
                import shutil
                shutil.copy(srcp, dst)
                print(f"sken {src}: kopiran iz /tmp/p154")
    for i in SCANS:
        out = f"{OUT}/s{i:02d}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"sken {i}: že obstaja, preskočim")
            continue
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        print(f"sken {i}: {len(data)} B JPEG OK")


if __name__ == "__main__":
    main()
