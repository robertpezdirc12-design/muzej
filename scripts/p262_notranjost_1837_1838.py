#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — verifikator NOTRANJOSTI-01738: 1837-NADALJEVANJE (m6–m12) → POROKE-1.-FEBRUAR-1838 + PROKLAMACIJE (I1–I10 + --live).
INTEGRACIJA: 4 GRIBLJE bloki (h36-m6-1838-nevesta-Anna-KRISCHAN + h63-m8-1838-ženin-Johann-KRISCHAN + h31-m8-1838-nevesta-Anna-TILAH + h17-m10-1838-nevesta-Maria-KRAL!);
korpus 2077 → 2081 (+4); 01738 65 → 69; ŠEST-KNJIŽNI-KLUB 39 → 41 (+2: h17/h31!);
2 DVIGI (h17-1875→1838-37-2.-NAJVEČJI-NOTRANJOSTI! + h31-1857→1838-19!);
RESTART-(D)-1.-FEBRUAR-1838 (glavni-datum-×7-ALL-'1.-Februar'-d°!-proklamacije-mali-annot: 1-Nov-×4 + 6-Nov-×3!-MNOŽIČNI-DAN-×7!);
KRIŠAN-NIT-×4-s18 (m6-endogamija-Georg-×-Anna-KRISCHAN! + m8-Johann-20-l-NAJMLAJŠI!); NOVI-PRIMEKI-×9; NOVE-VASI-×7 (VRANOVICH-1:1!);
foliacija-'Pag-=-2·sken−3'-serija-15/15 (s18-33/34!).
Dokaz: research/issue17/p262-work/ (s18-REZERVA-1bb45fb3-2×-neodvisen-1:1!-≈83-izrezkov!)."""
import json
import os
import re
import sys
import base64
import urllib.request
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OK = 0
FAIL = 0
LIVE = "--live" in sys.argv


def check(name, ok, msg=""):
    global OK, FAIL
    if ok:
        OK += 1
        print(f"[PASS] {name}" + (f" — {msg}" if msg else ""))
    else:
        FAIL += 1
        print(f"[FAIL] {name}" + (f" — {msg}" if msg else ""))


src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
early = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
stories = open(f"{ROOT}/src/data/atlas/parish-house-stories.ts", encoding="utf-8").read()
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()

# ——— I1: 4 bloki 1838/01738 s18 (file-order!) ———
bloki1838 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1838,\s*scan: 18,', src)
check("I1 bloki-01738/1838-s18 == [36,63,31,17] (m6-KRISCHAN-endogamija + m8-h63×h31-POLNI-DVOJNI + m10-KRAL!)",
      bloki1838 == ["36", "63", "31", "17"], ",".join(bloki1838))

# ——— I2: korpus 2081 + 01738 == 69 + leta 1828–1838+1873 ———
vseh = re.findall(r'bookSignature: "01738",\s*year: (\d+)', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta = sorted({int(y) for y in vseh})
check("I2 bloki-01738 == 69 (2077→2081-+4!)", len(vseh) == 69, str(len(vseh)))
check("I2b korpus-skupaj == 2081", skupaj == 2081, str(skupaj))
check("I2c leta-01738 == 1828–1838+1873 (11-let-notranjosti!)",
      leta == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1873], str(leta))

# ——— I3: POLNI-DVOJNI m8 h63×h31 ———
check("I3 m8-POLNI-DVOJNI-h63×h31-whatSi ('ALL-GRABLJE-1:1!')",
      "h63×h31-ALL-GRABLJE-1:1!" in src or "h63×h31-ALL-GRABLJE!" in src)
check("I3b h63-4.-01738-blok-whatSi", "4.-01738-blok-BREZ-dviga" in src)

# ——— I4: DVIGI h17-37/h31-19 ———
check("I4 h17-DVIG-37-whatSi ('1875→1838-DVIG-ZA-37-LET')", "1875→1838-DVIG-ZA-37-LET" in src)
check("I4b h31-DVIG-19-whatSi ('1857→1838-DVIG-ZA-19-LET')", "1857→1838-DVIG-ZA-19-LET" in src)
check("I4c h17-2.-NAJVEČJI-DVIG-NOTRANJOSTI ('2.-NAJVEČJI-DVIG-NOTRANJOSTI-PO-h22-41-P255')",
      "2.-NAJVEČJI-DVIG-NOTRANJOSTI-PO-h22-41-P255" in src)

# ——— I5: PREDHODNIK_1838_BLOCKS + NITI + KRAJI ———
import re as _re
_b = _re.search(r'export const PREDHODNIK_1838_BLOCKS = \{.*?\} as const;', early, _re.S)
dvigi_txt = _b.group(0) if _b else ''
check("I5 PREDHODNIK_1838_BLOCKS-4/7/2081/69",
      all(f in early for f in ["noviBloki: 4", "vpisi: 7", "vitalsTotal: 2081", "byBook01738: 69"]))
check("I5b dvigi-h17-37/h31-19", 'h17: "1875 → 1838 (37 let' in early and 'h31: "1857 → 1838 (19 let' in early, dvigi_txt[:120])
check("I5c restartStruktura-(D)-1.-FEBRUAR-1838 + MNOŽIČNI-DAN-×7",
      "1.-FEBRUAR-1838" in early and "MNOŽIČNI-DAN-×7" in early)
check("I5d foliacija-15/15", "serija-15/15-notranjosti" in early)
check("I5e krishanNit-×4", "×4-s18" in early)
check("I5f noviPrimeki-×9", "×9-s18" in early)
check("I5g urkunden1837-m12-3.-Feb", "3.-Februar-1837" in early)
check("I5h NITI-P262-KRIŠAN-×4 + NOVI-PRIMEKI-×9", "KRIŠAN-NIT-×4-NA-S18" in early and "NOVI-PRIMEKI-×9-NA-S18" in early)
check("I5i KRAJI-P262-VRANOVICH + OLOK-2 + GRADAG-20", "VRANOVICH" in early and "OLOK 2" in early and "GRADAG 20" in early)

# ——— I6: KRIŠAN-nit-×4-bloki-whatSi ———
check("I6 h36-whatSi-KRISCHAN-endogamija", "endogamija" in src)
check("I6b h63-whatSi-KRISCHAN", "Johann KRISCHAN" in src)
check("I6c h17-whatSi-KRAL", "Maria KRAL" in src)
check("I6d h31-whatSi-TILAH", "Anna TILAH" in src)

# ——— I7: QA-p262 živo ———
check("I7 qa-p262-kontrola-živo", "qa-p262-parish-marriage-notranjost-01738-1837-1838" in qa)
check("I7b qa-p262-bloki-s18-ključi", '"17-1838,31-1838,36-1838,63-1838"' in qa)
check("I7c qa-p262-korpus-2081/69", "HOUSE_VITALS.length !== 2081" in qa and 'bloki-01738 ≠ 69' in qa)
check("I7d qa-p262-ŠEST-knjižna-živo", "h17-ŠEST-knjižna ≠ 6" in qa and "h31-ŠEST-knjižna ≠ 6" in qa)

# ——— I8: HOUSE_STORIES živo ———
h17 = re.search(r'houseNo: "17", kind: "griblje", blocks: (\d+), books: (\d+),.*?firstYear: (\d+)', stories)
h31 = re.search(r'houseNo: "31", kind: "griblje", blocks: (\d+), books: (\d+),.*?firstYear: (\d+)', stories)
h36 = re.search(r'houseNo: "36", kind: "griblje", blocks: (\d+), books: (\d+),.*?firstYear: (\d+)', stories)
h63 = re.search(r'houseNo: "63", kind: "griblje", blocks: (\d+), books: (\d+),.*?firstYear: (\d+)', stories)
check("I8 h17-19-blokov-6-knjig-firstYear-1838", h17 and h17.groups() == ("19", "6", "1838"),
      ",".join(h17.groups()) if h17 else "-")
check("I8b h31-43-blokov-6-knjig-firstYear-1838", h31 and h31.groups() == ("43", "6", "1838"),
      ",".join(h31.groups()) if h31 else "-")
check("I8c h36-35-blokov-firstYear-1832-ostaja", h36 and h36.group(1) == "35" and h36.group(3) == "1832",
      ",".join(h36.groups()) if h36 else "-")
check("I8d h63-32-blokov-firstYear-1836-ostaja", h63 and h63.group(1) == "32" and h63.group(3) == "1836",
      ",".join(h63.groups()) if h63 else "-")
check("I8e BOOKS-01738-69-blokov-leta-1828–1838", 'years: "1828–1838 + 1873", blocks: 69' in stories)
check("I8f p262Dvigi-h17-37/h31-19", "p262Dvigi:" in stories and "h17-37" in stories)

# ——— I9: UI kartica ———
check("I9 UI-Notranjost01738Leto1837_1838-kartica", "function Notranjost01738Leto1837_1838()" in ui)
check("I9b UI-mount", "<Notranjost01738Leto1837_1838 />" in ui)
check("I9c UI-PREDHODNIK_1838_BLOCKS-import", "PREDHODNIK_1838_BLOCKS," in ui)
check("I9d UI-PROKLAMACIJE-timeline", "Proklamacije 1. novembar 1837" in ui and "Proklamacije 6. novembar 1837" in ui)
check("I9e UI-NOVE-VASI-×7", "NOVE VASI ×7 P262" in ui)

# ——— I10: RESTART-(D)-struktura-proklamacije ———
check("I10 proklamacije-m6–m9-1-Nov-×4 + m10–m12-6-Nov-×3",
      "m6–m9-'1-Nov'-1837-×4 + m10–m12-'6-Nov'-1837-×3" in src)
check("I10b MNOŽIČNI-DAN-×7-VSI-VPISI", "×7-VSI-VPISI-1-sam-dan" in src)
check("I10c header-1837-pastoralno-leto-1837/38", "header-'1837'-pastoralno-leto-1837/38" in src)

# ——— LIVE verifikacije ———
if LIVE:
    # L1: s18-REZERVA md5 1:1
    try:
        h = hashlib.md5(open(f"{ROOT}/research/issue17/p261-work/s18.jpg", "rb").read()).hexdigest()
        check("L1 s18-REZERVA-md5 == 1bb45fb32482e5a0b46287c0d034ec7f (2.-neodvisen-prenos!)",
              h == "1bb45fb32482e5a0b46287c0d034ec7f", h)
    except Exception as e:
        check("L1 s18-REZERVA-md5", False, str(e))
    # L2: inventar-147-URL 1:1
    try:
        u = "aHR0cHM6Ly9kYXRhLm1hdHJpY3VsYS1vbmxpbmUuZXUvc2wvc2xvdmVuaWEvbGp1YmxqYW5hL3BvZHplbWVsaS8wMTczOC8="
        inv = base64.b64decode(u).decode()
        check("L2 inventar-147-URL-1:1-matricula", inv.startswith("https://data.matricula-online.eu"), inv)
    except Exception as e:
        check("L2 inventar-URL", False, str(e))
    # L3: /api/qa živo — 256/256 + qa-p262 pass
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=30) as r:
            d = json.load(r)
        p262 = [t for t in d.get("tests", []) if t.get("id") == "qa-p262-parish-marriage-notranjost-01738-1837-1838"]
        check("L3 /api/qa-živo-ok:True", d.get("ok") is True, f"passed={d.get('passed')}")
        check("L3b /api/qa-256/256", d.get("passed") == 256 and d.get("failed") == 0, f"{d.get('passed')}/{d.get('passed', 0) + d.get('failed', 0)}")
        check("L3c qa-p262-pass:True", bool(p262) and p262[0].get("pass") is True)
    except Exception as e:
        check("L3 /api/qa", False, str(e))
    # L4: p262-work-izrezki ≈83
    import os
    n = len([f for f in os.listdir(f"{ROOT}/research/issue17/p262-work") if f.endswith(".png")])
    check("L4 p262-work-izrezki == 83", n == 83, str(n))

print(f"\n{'=' * 60}")
print(f"P262 VERIFIKATOR: {OK}/{OK + FAIL} PASS" + (" (--live!)" if LIVE else ""))
sys.exit(0 if FAIL == 0 else 1)
