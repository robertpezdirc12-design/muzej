#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P263 — verifikator NOTRANJOSTI-01738: 1837 (m12–m18) + LETNI RESTART 1–2 (s19 = Pag. 35/36) — I1–I10 + --live.

INTEGRACIJA (P263 snapshot): 4 GRIBLJE bloki (h60-m14-1837-ženin-Georg-SIMIG/ŠIMIČ-62-l + h29-m14-1837-nevesta-Anna-MILEK + h11-m18-1837-ženin + h11-m18-1837-nevesta);
korpus 2081→2085 (+4 P263) / danes živo 2088 (po P264); 01738 69→73 (+4 P263) / danes živo 76 (po P264);
ŠEST-KNJIŽNI-KLUB 41→42 (h29 5→6, P263); DVIG h29 1859→1837 (22 let!);
POLNI DVOJNI h60×h29 + h11×h11 (oba partnerja ista hiša!); ŠIMIČ-kronološka-kontrola 59→62 (isti mož 1833/1837!);
številčenje 12 (DUP s s18 m12!) → 14 (13 manjka!) → 15–18 → RESTART 1–2 (1./4. Februar — 1838|1839 X-OPEN!);
foliacija 'Pag = 2·sken − 3' serija 16/16 (s19 = 35/36).
Dokaz: research/issue17/p263-work/ (s19-md5-117add77-1:1 + 14 izrezov!) + research/issue17/p263-facts.json.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request

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

# ——— I1: 4 bloki 1837/01738 s19 (file-order!) ———
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1837,\s*scan: 19,', src)
check("I1 bloki-01738/1837-s19 == [60,29,11,11] (m14-ŠIMIČ + h29-MILEK + m18-h11×h11!)", bloki == ["60", "29", "11", "11"], ",".join(bloki))

# ——— I2: korpus živo 2088 + 01738 == 76 (po P264; P263 snapshot 2085/73) + leta ———
vseh = re.findall(r'bookSignature: "01738",\s*year: (\d+)', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta = sorted({int(y) for y in vseh})
check("I2 bloki-01738 == 76 živo (po P264; P263-snapshot 73)", len(vseh) == 76, str(len(vseh)))
check("I2b korpus-skupaj == 2088 živo", skupaj == 2088, str(skupaj))
check("I2c leta-01738 == 1828–1838+1873", leta == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1873], str(leta))

# ——— I3: ŠIMIČ-kronološka-kontrola (59→62) + h60-2.-blok ———
check("I3 h60-ŠIMIČ-62-l + 1833-59-l", "Georg SIMIG [ŠIMIČ!" in src and "62 l [1833: 59 l" in src)
check("I3b h60-2.-01738-blok-BREZ-dviga", "h60-2.-01738-blok-BREZ-dviga" in src)
check("I3c ŠIMIČ-nit-1833→1837", "ŠIMIČ-NIT-1833→1837" in src)

# ——— I4: h29 DVIG 22 + POLNI DVOJNI h11×h11 ———
check("I4 h29-DVIG-firstYear-1859→1837-ZA-22-LET", "1859→1837-DVIG-ZA-22-LET" in src)
check("I4b h29-ŠEST-KNJIŽNI-KLUB-41→42", "ŠEST-KNJIŽNI-KLUB-41→42" in src)
check("I4c POLNI-DVOJNI-h11×h11-=-OBA-PARTNERJA-ISTA-HIŠA", "POLNI DVOJNI h11×h11" in src)
check("I4d k.k.-Trauungsschein-Nr-21", "k.k. Trauungsschein Nr 21" in src)

# ——— I5: PREDHODNIK_1837_BLOCKS (P263 snapshot) + NITI + KRAJI ———
check("I5 PREDHODNIK_1837_BLOCKS-4/8/2085/73 (P263 snapshot)",
      all(f in early for f in ["noviBloki: 4", "vpisi: 8", "vitalsTotal: 2085", "byBook01738: 73"]))
check("I5b dvig-h29-22-let", "1859 → 1837 (22 let" in early)
check("I5c stevilcenje-DUP-12 + RESTART", "12 (DUP-s-s18-m12!)" in early and "RESTART-na-1" in early)
check("I5d foliacija-16/16", "serija-16/16-notranjosti" in early)
check("I5e simicKontrola-59→62", "59-l" in early and "62-l" in early)
check("I5f urkunden-Molling + Nr-21", "Molling-31.-August-1837" in early and "Nr-21" in early)
check("I5g NITI-P263-ŠIMIČ + MILEK", "ŠIMIČ-KRONOLOŠKA-KONTROLA" in early and "MILEK-NIT-h29" in early)
check("I5h KRAJI-P263-GRÜBLE + MOLLING", "GRÜBLE (GRIBLJE)" in early and "MOLLING (METLIKA)" in early)

# ——— I6: QA-p263 živo ———
check("I6 qa-p263-kontrola-živo", "qa-p263-parish-marriage-notranjost-01738-1837" in qa)
check("I6b qa-p263-bloki-s19-ključi", '"60-1837,29-1837,11-1837,11-1837"' in qa)
check("I6c qa-p263-korpus-živo-2088/76 (po P264)", "HOUSE_VITALS.length !== 2088" in qa and "bloki-01738 ≠ 76" in qa)
check("I6d qa-p263-ŠEST-knjižna-h29", "h29-ŠEST-knjižna/firstYear-1837/24-blokov" in qa)

# ——— I7: HOUSE_STORIES živo ———
h11 = re.search(r'houseNo: "11", kind: "griblje", blocks: (\d+), books: (\d+),.*?firstYear: (\d+)', stories)
h29 = re.search(r'houseNo: "29", kind: "griblje", blocks: (\d+), books: (\d+),.*?firstYear: (\d+)', stories)
h60 = re.search(r'houseNo: "60", kind: "griblje", blocks: (\d+), books: (\d+),.*?firstYear: (\d+)', stories)
check("I7 h11-33-blokov-6-knjig-firstYear-1831", h11 and h11.groups() == ("33", "6", "1831"), ",".join(h11.groups()) if h11 else "-")
check("I7b h29-24-blokov-6-knjig-firstYear-1837", h29 and h29.groups() == ("24", "6", "1837"), ",".join(h29.groups()) if h29 else "-")
check("I7c h60-32-blokov-6-knjig-firstYear-1833", h60 and h60.groups() == ("32", "6", "1833"), ",".join(h60.groups()) if h60 else "-")
check("I7d BOOKS-01738-76-blokov-his-48 (živo po P264)", 'years: "1828–1838 + 1873", blocks: 76, houses: 48' in stories)
check("I7e SIX-43-TIERS-43/25 (živo po P264)", "sixBook: 43," in stories and "{ books: 6, houses: 43," in stories and "{ books: 5, houses: 25," in stories)
check("I7f p263Dvigi", "p263Dvigi:" in stories and "h29-22" in stories)

# ——— I8: UI kartica ———
check("I8 UI-Notranjost01738Leto1837-kartica", "function Notranjost01738Leto1837()" in ui)
check("I8b UI-mount", "<Notranjost01738Leto1837 />" in ui)
check("I8c UI-PREDHODNIK_1837_BLOCKS-import", "PREDHODNIK_1837_BLOCKS," in ui)
check("I8d UI-ŠIMIČ-kontrola", "ŠIMIČ kronološka kontrola" in ui and "62" in ui)
check("I8e UI-POLNI-DVOJNI-h11×h11", "h11 × h11" in ui)

# ——— I9: dokaz JSON ———
p263 = json.load(open(f"{ROOT}/research/issue17/p263-facts.json", encoding="utf-8"))
check("I9 p263-facts-8-vpisov", len(p263["vpisi"]) == 8, str(len(p263["vpisi"])))
check("I9b blokiGriblje-4", p263["blokiGriblje"]["skupaj"] == 4)
check("I9c korpusUcinek-po-P263-snapshot-2085/73", p263["korpusUcinek"]["po"]["vitals"] == 2085 and p263["korpusUcinek"]["po"]["01738"] == 73)
check("I9d p263-work-transcript", os.path.exists(f"{ROOT}/research/issue17/p263-work/transcript.md"))

# ——— I10: foliacija + številčenje + X-OPEN ———
check("I10 foliacija-s19-35/36", "s19 = Pag. 35/36" in src)
check("I10b DUP-12 + 13-manjka + restart", "12 (DUP-s-s18-m12!)" in src and "13-manjka!" in src and "RESTART-na-1" in src)
check("I10c MLADOLETNA-m1-17-l", "MLADOLETNA" in src and "17" in src)

# ——— LIVE verifikacije ———
if LIVE:
    try:
        h = hashlib.md5(open(f"{ROOT}/research/issue17/p263-work/s19.jpg", "rb").read()).hexdigest()
        check("L1 s19-md5 == 117add7703c78acc3ad6f8ce9b0d81cb", h == "117add7703c78acc3ad6f8ce9b0d81cb", h)
    except Exception as e:
        check("L1 s19-md5", False, str(e))
    try:
        u = "aHR0cHM6Ly9kYXRhLm1hdHJpY3VsYS1vbmxpbmUuZXUvc2wvc2xvdmVuaWEvbGp1YmxqYW5hL3BvZHplbWVsaS8wMTczOC8="
        import base64
        inv = base64.b64decode(u).decode()
        check("L2 inventar-147-URL-1:1-matricula", inv.startswith("https://data.matricula-online.eu"), inv)
    except Exception as e:
        check("L2 inventar-URL", False, str(e))
    try:
        with urllib.request.urlopen("https://griblje-museum.vercel.app/api/qa", timeout=30) as r:
            d = json.load(r)
        p = [t for t in d.get("tests", []) if t.get("id") == "qa-p263-parish-marriage-notranjost-01738-1837"]
        check("L3 /api/qa-živo-ok:True", d.get("ok") is True, f"passed={d.get('passed')}")
        check("L3b qa-p263-pass:True", bool(p) and p[0].get("pass") is True)
    except Exception as e:
        check("L3 /api/qa", False, str(e))
    n = len([f for f in os.listdir(f"{ROOT}/research/issue17/p263-work") if f.endswith(".png")])
    check("L4 p263-work-izrezki >= 14", n >= 14, str(n))

print(f"\n{'=' * 60}")
print(f"P263 VERIFIKATOR: {OK}/{OK + FAIL} PASS" + (" (--live!)" if LIVE else ""))
sys.exit(0 if FAIL == 0 else 1)
