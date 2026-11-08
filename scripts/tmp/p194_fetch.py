#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P153 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1887).
P80-okvir: 1884 = s192–s198 (P193!) — 1883 = s187–s192 (Pag. 181–186 = sken − 6!);
1883-tail z69–z75 ŽE na s192 (P193-prebrani!); meja-1882/83 = s187/s188-probe. Ni del
repozitorija: delovni imenik /tmp/p194 (po vzoru P192/P193). P194 potrebuje skene
187–192 (celo leto 1883 + tail-s192). Prej: (izpuščeno — prepisani opis)
/tmp/p194 (po vzoru P102/P103)."""
import base64, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p194"
SCANS = range(187, 193)  # skeni 187–192 (celo leto 1883 + meja-1884-že-na-s192!)
EXPECTED = 208  # inventar 04106 (P192-T0)


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
