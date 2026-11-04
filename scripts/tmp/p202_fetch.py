#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 delovna faza — prenos skenov MRLIŠKE knjige 04106 (leto 1875 = 11/29!).
Okno: s126–s133 (s134 = meja-1875/76 ŽE-VLM-PREBRANA-v-P201-seji [TAIL-4-DEZ-1875-nad
+ VELIKA-'1876 Jänner'-glava-V-SREDINI + leadP202-tail_1875 ×4 — Griblje-×1: h11-KUNIĆ/
Jakoš!]; meja-1874/75 = išče-nazaj v s126–s133). Preslikava: pag = sken − 6;
inventory-idx = sken − 1. KRIŽNA-VALIDACIJA: sveži-s134-md5 == /tmp/p201-disk
(P201-seja-1:1 → kontinuiteta-verige P197→P198→P199→P200→P201→P202!). Recept: P201."""
import base64, hashlib, json, os, re, sys, time, urllib.request, urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
OUT = "/tmp/p202"
NEW = range(126, 134)   # s126–s133 (sveže!)
REFS = [("s134", "/tmp/p201/s134.jpg")]


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
    if len(urls) < 134:
        print("inventar premajhen za s134!")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    json.dump(urls, open(f"{OUT}/inventory.json", "w"))
    md5s = {}

    # ——— sveži s126–s133 ———
    for i in NEW:
        out = f"{OUT}/s{i}.jpg"
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"sken {i}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        with open(out, "wb") as f:
            f.write(data)
        md5s[f"s{i}"] = md5b(data)
        print(f"sken {i}: {len(data)} B JPEG OK md5={md5s[f's{i}'][:12]}")

    # ——— s134: sveže-prenesi + KRIŽNA-validacija vs P201-disk (kopiraj-1:1!) ———
    ok = True
    for name, ref in REFS:
        i = int(name[1:])
        st2, data = http_get(urls[i - 1])
        if st2 != 200 or data[:2] != b"\xff\xd8":
            print(f"{name}: HTTP {st2} — NI JPEG")
            sys.exit(1)
        fresh = md5b(data)
        disk = md5b(open(ref, "rb").read())
        same = fresh == disk
        print(f"KRIŽNI-MD5 {name}: svež={fresh[:12]} P201-disk={disk[:12]} → {'1:1 ✓' if same else '✗ ODMAK!'}")
        ok = ok and same
        if same:
            with open(f"{OUT}/{name}.jpg", "wb") as f:
                f.write(data)
            md5s[name] = fresh
        else:
            # fallback: kopiraj P201-disk (avtoriteta — VLM-branja so nanj vezana!)
            import shutil
            shutil.copyfile(ref, f"{OUT}/{name}.jpg")
            md5s[name] = disk
            print(f"  → KOPIJA {name} iz P201-diska (avtoriteta-verige!)")
    if not ok:
        print("⚠ md5-križna-validacija: vsaj-1-ODMAK — nadaljujem-z-P201-kopijo (VLM-vezava!)")

    json.dump(md5s, open(f"{OUT}/md5s.json", "w"), indent=1)
    print("→ preslikava: inventory-idx = sken − 1 (P197→P198→P199→P200→P201-veriga + TA-seja-6.×); pag = sken − 6")


if __name__ == "__main__":
    main()
