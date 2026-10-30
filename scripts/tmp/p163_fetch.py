#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P163 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1897).
P162-okvir: 1896 = s55-dno + s56–s59 + s60 (zap 53–60) == str. 54–59
(stran == sken − 1 — 20.–25. potrditev!);
meja 1896/97 = '1897.' TROJNI podčrtaj na PRAZNI vrsti s60 + Januarj +
restart zap 1–2 = 5. STIL MEJE 4. POTRDITEV (s61 = že 1897 — glava
'Leto 1897' + zap 3–14!).
P162-lead za 1897: s60-dno-restart zap1–2 + s61 zap 3–14 [Griblje ×3:
h51-Ana-Urh-roj.-Novosel-61-vdova-bajtarca-2.2. = URH-TRILOGIJA #3 +
h42-Jurij/Jožef-Pezdirc?-52-Jetika-6.3. = h42-PEZDIREC-nadaljevanje +
h2-Ana-Vrobeč?-33/53?-Jetika-19.5. — γ-3-dvom!] + s62+; meja 1897/98
[~ s67+?].
P163 potrebuje skene 60–68 (s60-dno-restart = 1897 začetek + celo leto
+ meja 1897/98 + 1 varnostni sken). Ni del repozitorija: delovni imenik
/tmp/p163 (po vzoru P153–P162)."""
import json, os, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p163"
SCANS = range(60, 69)  # skeni 60–68 (s60-dno-restart = 1897 + celo leto + meja 1897/98 +1)
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
    import base64, re
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
    inv_path = os.path.join(OUT, "inventory.json")
    if os.path.exists(inv_path):
        urls = json.load(open(inv_path))
        print(f"inventar iz /tmp/p163/inventory.json: {len(urls)} slik")
    else:
        st, body = http_get(BOOK_URL)
        if st != 200:
            print(f"knjiga HTTP {st}")
            sys.exit(1)
        urls = decode_inventory(body.decode("utf-8", "replace"))
        print(f"inventar: {len(urls)} slik (pričakovano {EXPECTED})")
        if len(urls) != EXPECTED:
            sys.exit(1)
        os.makedirs(OUT, exist_ok=True)
        with open(inv_path, "w") as f:
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


if __name__ == "__main__":
    main()
