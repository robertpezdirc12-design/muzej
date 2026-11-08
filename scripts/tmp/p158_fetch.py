#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P158 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1892).
P157-okvir: 1891 = skeni 28-dno (r1–3) + 29–33 (str. 27–32, 65 vrstic / 15 Griblje-vpisov);
meja 1891/92 = glava »Leto 1892.« + podčrtan »1892« na s34 (4. STIL MEJE — hibrid marker+glava!)
— s34-r1 = P158-lead (Griblje 57 Rudolf P~ezdinec 2½ let Merlica 6./8.1.).
P158 potrebuje skene 34–42 (celo leto 1892 + meja 1892/93 kontrola — kjer se konča,
še ni znano: 1891 = 65 vrstic / ~6 skenov, pričakujemo ~60–70 vrstic).
Ni del repozitorija: delovni imenik /tmp/p158 (po vzoru P153–P157)."""
import base64, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p158"
SCANS = range(34, 43)  # skeni 34–42 (s34-top = 1892-leto + meja 1892/93 kontrola)
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
        json.dump(urls, f, indent=1)
    ok = 0
    for s in SCANS:
        dst = f"{OUT}/s{s:02d}.jpg"
        if os.path.exists(dst) and os.path.getsize(dst) > 50000:
            ok += 1
            print(f"s{s:02d}: že nazaj ✓")
            continue
        st, data = http_get(urls[s - 1])
        if st == 200 and len(data) > 50000:
            open(dst, "wb").write(data)
            ok += 1
            print(f"s{s:02d}: {len(data)//1024} KB ✓")
        else:
            print(f"s{s:02d}: HTTP {st} ✗")
        time.sleep(1.5)
    print(f"prenos: {ok}/{len(SCANS)}")
    sys.exit(0 if ok == len(SCANS) else 1)


if __name__ == "__main__":
    main()
