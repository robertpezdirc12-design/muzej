#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P169 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1903).
P168-okvir: meja 1902/03 = s90-sredina ('1903.' VELIKA + DVOJNI podčrtaj
na PRAZNI vrsti + Januarj-INLINE + restart zap 61→1 = 5. STIL 10. POTRDITEV
— P167-lead-'[~ s90+?]' POTRJEN!).
P169-lead za 1903: s90-dno-restart zap1–7 ŽE prebrani [Griblje-kandidati
ŽE-VIDNI: zap1-h45?-Alojzij-Štravs-5-mes-Jan + zap3-h43/45?-Nikolaj-
Štravs-2-let-Feb + zap4-h30?-Jožef-Zagriva?-10-mes-Feb = Štravs-×2 ŽE!]
+ s91 (zap8–19?) + s92+; meja 1903/04 [~ s94+?].
P169 potrebuje skene 90–95 (s90-dno reuse — ampak /tmp izbrisan med
sejami → re-fetch s90 tudi za dno-crops forenziko!).
Ni del repozitorija: delovni imenik /tmp/p169 (po vzoru P153–P168)."""
import json, os, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p169"
SCANS = range(90, 96)  # skeni 90–95 (s90-dno = 1903-restart zap1–7; meja ~s94+?)
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
    os.makedirs(OUT, exist_ok=True)
    inv_path = os.path.join(OUT, "inventory.json")
    if os.path.exists(inv_path):
        urls = json.load(open(inv_path))
        print(f"inventar iz /tmp/p169/inventory.json: {len(urls)} slik")
    else:
        st, body = http_get(BOOK_URL)
        if st != 200:
            print(f"knjiga HTTP {st}")
            sys.exit(1)
        urls = decode_inventory(body.decode("utf-8", "replace"))
        print(f"inventar: {len(urls)} slik (pričakovano {EXPECTED})")
        if len(urls) != EXPECTED:
            sys.exit(1)
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
