#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P167 delovna faza — prenos skenov MRLIŠKE knjige 04894 (leto 1901).
P166-okvir: meja 1900/01 = s80-sredina ('1901' VELIKA + podčrtaj na
PRAZNI vrsti + Januarj-INLINE + restart zap 61→1 = 5. STIL 8. POTRDITEV
— P165-lead-'s79+?' OVRJEN!).
P166-lead za 1901: s80-dno-restart zap 1–6 ŽE prebrani [Griblje ×3
ŽE-VIDNI: zap1-h36-Ana-Križan-76-vdova-kolarica + zap4-h48-Matija-
HLOBUČAR-65-samski-½-zemlj.-sin = HLOBUČAR-×2-v-2-MESECIH! + Krasinec-
18-2-mes] + s81 (zap 7–18?) + s82+; meja 1901/02 [~ s85+?].
P167 potrebuje skene 81–85 (+ s80-reuse = dno s80: zap 1–6).
Ni del repozitorija: delovni imenik /tmp/p167 (po vzoru P153–P166)."""
import json, os, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p167"
SCANS = range(81, 86)  # skeni 81–85 (s80-dno reuse iz /tmp/p166; meja ~s85?)
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
        print(f"inventar iz /tmp/p167/inventory.json: {len(urls)} slik")
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
    # s80 kopija iz /tmp/p166 (dno = restart zap 1–6; P166 je prebral)
    if not os.path.exists(f"{OUT}/s80.jpg") and os.path.exists("/tmp/p166/s80.jpg"):
        open(f"{OUT}/s80.jpg", "wb").write(open("/tmp/p166/s80.jpg", "rb").read())
        print("s80: kopija iz /tmp/p166 ✓")
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
