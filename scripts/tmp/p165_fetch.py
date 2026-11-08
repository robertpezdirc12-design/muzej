#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P165 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1899).
P164-okvir: meja 1898/99 = s70-top ('1899.'-INLINE v smrti-celici zap1 +
Januarj-INLINE + restart zap 58→1 = 4. INLINE-potrditev — cf. P161-s51!;
P163-lead-'s71+?' OVRJEN — s70 = ŽE 1899! s69-dno = PRAZNE vrste!).
P164-lead za 1899: s70-glava-'Leto 1899' + '1899.'-INLINE-zap1
[Januarj 1./5.-Otok-11-Nikolaj-Jurcavič-68!] + s70 zap 1–11
[Griblje ×1: h20-Marija-Pezdirec — PEZDIREC-era-8.!] + s71 (12–23 [×5!])
+ s72 (24–35 [×2] — VLM-s72-meseci-KAOS ANOMALIJA! + NOVI-DUHOVNIK-
#9-kandidat Franc-Števan-coop!); meja 1899/1900 [~ s75+?].
P165 potrebuje skene 70–77 (s70 = 1899 začetek + celo leto + meja
1899/1900 + 1 varnostni sken). s70–s72 že preneseni/prebrani (P164).
Ni del repozitorija: delovni imenik /tmp/p165 (po vzoru P153–P164)."""
import json, os, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p165"
SCANS = range(70, 78)  # skeni 70–77 (s70 = 1899 + celo leto + meja 1899/1900 +1)
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
        print(f"inventar iz /tmp/p165/inventory.json: {len(urls)} slik")
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
