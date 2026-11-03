#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P197 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1880).
P196-sidro: s171 = MEJA-1880/81 (tail-1880: z72 Valčič 92J Wassersucht!);
1880 se konča na s171-top → leto teče nazaj vsaj do s165 (P197-lead).
Probe: s163–s171 (9 skenov) — branje od s165; če z1-restart ni viden,
razširimo nazaj. Preslikava se VALIDIRA z md5-primerjavo s171
proti P196-znanemu dobremu jpgu (kandidata: idx=sken−1 ALI idx=pag−1,
kjer pag = sken − 6 po P196-preslikavi!). Recept: P153/P126
(inventar-/image/<b64>/ → hosted-images.matricula-online.eu + UA)."""
import base64, hashlib, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p197"
SCANS = range(163, 172)  # probe s163–s171
REF = "/tmp/p196/s171.jpg"  # znan-dober s171 iz P196


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


def md5b(data):
    return hashlib.md5(data).hexdigest()


def main():
    st, body = http_get(BOOK_URL)
    if st != 200:
        print(f"knjiga HTTP {st}")
        sys.exit(1)
    urls = decode_inventory(body.decode("utf-8", "replace"))
    print(f"inventar 04106: {len(urls)} slik")
    if len(urls) < 172:
        print("inventar premajhen za s171!")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))

    off = 0
    if os.path.exists(REF):
        ref_md5 = md5b(open(REF, "rb").read())
        for label, idx in [("sken−1", 171 - 1), ("pag−1 (sken−6)", 171 - 6 - 1)]:
            st2, data = http_get(urls[idx])
            ok = st2 == 200 and md5b(data) == ref_md5
            print(f"validacija-{label}: idx={idx} → {'MATCH ✓' if ok else 'ne'} ({len(data)}B)")
            if ok:
                off = idx - (171 - 1)
                break
        else:
            print("❌ preslikava neznana — ročna forenzika (inventar ≠ pričakovan vrstni red?)")
            sys.exit(1)
        print(f"→ preslikava: inventory-idx = sken − 1 {'+ 0' if off == 0 else f'{off:+d} (pag-režim)'}")

    for i in SCANS:
        out = f"{OUT}/s{i}.jpg"
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"sken {i}: že obstaja, preskočim")
            continue
        st2, data = http_get(urls[i - 1 + off])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        print(f"sken {i}: {len(data)} B JPEG OK")


if __name__ == "__main__":
    main()
