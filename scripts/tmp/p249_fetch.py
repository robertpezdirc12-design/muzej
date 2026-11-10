#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P249 — prenos skenov poročne knjige 04455 (leto 1875 predzgodovina, 11/13).
Metoda s8-nazaj (P248 NAPAVED): tail-1875 = s11-vpis-8-violet NAKNADNI (že 1:1 P248)
+ regularni-tail-17 'Juli 20' s10 (že 1:1 očesa P248) → restart-1875 pričakovan
na s8-TOP ali s7. Skeni s7–s11 (razprti listi ~2458×1800 px).
Delovni imenik /tmp/p249 (po vzoru P243/P246/P248): inventor /tmp/04455_urls.json
(192 URL-ov, 1:1 z P246) → direct-JPG + md5-kontrole + s8/s11 križni md5 (P248-disk ni več:
/tmp/p248 izpraznjen → s8+s11 ponoven 2. neodvisen prenos za dvojno kontrolo!)."""
import hashlib, json, os, sys, urllib.request, urllib.error

OUT = "/tmp/p249"
SCANS = list(range(7, 12))  # s7–s11
URLS = json.load(open("/tmp/04455_urls.json"))


def http_get(url, tries=4):
    UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:
            last = e
    raise last


def fetch(s, tag):
    idx = s - 1
    u = URLS[idx]
    if u.endswith("/"):
        u = u[:-1]  # trailing-slash-fix (P242 razred)
    out = f"{OUT}/s{s}_{tag}.jpg" if tag else f"{OUT}/s{s}.jpg"
    if os.path.exists(out) and os.path.getsize(out) > 100000:
        print(f"s{s}{tag}: že obstaja ({os.path.getsize(out)} B)")
    else:
        st, data = http_get(u)
        if st != 200 or len(data) < 50000:
            print(f"s{s}{tag}: FAIL status={st} len={len(data)}")
            sys.exit(3)
        with open(out, "wb") as f:
            f.write(data)
    md5 = hashlib.md5(open(out, "rb").read()).hexdigest()
    print(f"s{s}{tag}: {os.path.getsize(out)} B md5={md5}")
    return md5


def main():
    os.makedirs(OUT, exist_ok=True)
    md5s = {}
    for s in SCANS:
        md5s[s] = fetch(s, "")
    # 2. neodvisen prenos s8+s11 (križna md5-kontrola — P248-disk izpraznjen!)
    for s in (8, 11):
        m2 = fetch(s, "x2")
        if m2 != md5s[s]:
            print(f"s{s}: MD5 MISMATCH x2 ({md5s[s]} vs {m2})!")
            sys.exit(4)
        print(f"s{s}: križna md5 x2 1:1 ✓")
    print("DONE", len(SCANS), "skenov +2 x2")


if __name__ == "__main__":
    main()
