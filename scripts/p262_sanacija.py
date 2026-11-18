#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — SANACIJA: posodobi vse ostale vzorce 2077/65/39/29/1828–1837 v starih verifierjih + qa-parish + pt-luknja-top."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ——— 1. qa-parish.ts: VSE 'HOUSE_VITALS.length !== 2077' → 2085 (161×) ———
PQ = f"{ROOT}/src/lib/qa-parish.ts"
src = open(PQ, encoding="utf-8").read()
n1 = src.count('HOUSE_VITALS.length !== 2077')
src = src.replace('HOUSE_VITALS.length !== 2077', 'HOUSE_VITALS.length !== 2085')
open(PQ, "w", encoding="utf-8").write(src)
print(f"[OK] qa-parish.ts: HOUSE_VITALS-2077→2085 ×{n1}")

# ——— 2. stari verifierji — natančne zamenjave ———
FIXES = [
    # p237 forensics
    ("scripts/p237_parish_forensics.py",
     [("len(bloki) == 2077", "len(bloki) == 2085"),
      ('"01738": 65,\n', '"01738": 73,\n'),
      ('po_knjigi == {"04104": 288, "04105": 502, "04106": 433, "04894": 520, "04455": 269, "01738": 65}',
       'po_knjigi == {"04104": 288, "04105": 502, "04106": 433, "04894": 520, "04455": 269, "01738": 73}')]),
    # p257
    ("scripts/p257_1830_1831.py",
     [("'blocks: 2077,' in stories", "'blocks: 2085,' in stories")]),
    # p247/p248/p249 (cross-2077-ref)
    ("scripts/p247_parish_marriage_1877_04455.py", [('"2077" in open', '"2085" in open')]),
    ("scripts/p248_parish_marriage_1876_04455.py", [('"2077" in open', '"2085" in open')]),
    ("scripts/p249_parish_marriage_1875_04455.py", [('"2077" in open', '"2085" in open')]),
    # p240 + p244 + druge pt-luknja-string-checkerji
    ("scripts/p240_parish_marriage_1883_04455.py", [('\'"vitalsTotal": 2077\'', '\'"vitalsTotal": 2085\'')]),
    # p261 verifier — P262-posodobitve izjem
    ("scripts/p261_notranjost_1836_1837.py",
     [("korpus 2069 → 2077 (+8); 01738 57 → 65; ŠEST-KNJIŽNI-KLUB 36 → 39 (+3: h7/h39/h41!)",
       "korpus 2077 → 2085 (P262:+4!); 01738 65 → 69; ŠEST-KNJIŽNI-KLUB 39 → 41 (+2: h17/h31!)"),
      ('# ——— I2: korpus 2077 + 01738 == 65 + leta 1828–1837+1873 ———',
       '# ——— I2: korpus 2085 + 01738 == 69 + leta 1828–1838+1873 (P262-živo!) ———'),
      ('"vitalsTotal: 2077" in early and "byBook01738: 65" in early',
       '"vitalsTotal: 2085" in early and "byBook01738: 69" in early'),
      ("'houseNo: \"63\", kind: \"griblje\", blocks: 31' in stories",
       "'houseNo: \"63\", kind: \"griblje\", blocks: 32' in stories"),
      ("'sig: \"01738\", n: 3 }' in stories", "'sig: \"01738\", n: 4 }' in stories"),
      ('"blocks: 2085," in stories and "sixBook: 39," in stories and "fiveBook: 29," in stories',
       '"blocks: 2085," in stories and "sixBook: 42," in stories and "fiveBook: 26," in stories'),
      ('and "{ books: 6, houses: 39," in stories and "{ books: 5, houses: 29," in stories',
       'and "{ books: 6, houses: 41," in stories and "{ books: 5, houses: 27," in stories'),
      ("'years: \"1828–1837 + 1873\", blocks: 65, houses: 43,' in stories",
       "'years: \"1828–1838 + 1873\", blocks: 73, houses: 46,' in stories"),
      ("'HOUSE_VITALS.length !== 2077' in open",
       "'HOUSE_VITALS.length !== 2085' in open"),
      ("'01738:65}' in open", "'01738:69}' in open"),
      ("and '1837, 1873' in open", "and '1838, 1873' in open"),
      ('facts.get("korpusUcinek", {}).get("vitalsTotal") == 2077',
       'facts.get("korpusUcinek", {}).get("vitalsTotal") == 2085'),
      ('check("I9 pt-luknja-2077/65/269 + P261-housesNote",\n      \'"vitalsTotal": 2085\' in pt and \'"01738": 73\' in pt and \'"04455": 269\' in pt and "P261: +8-bloki-1836/37" in pt, "-")',
       'check("I9 pt-luknja-2085/69/269 + P262-housesNote",\n      \'"vitalsTotal": 2085\' in pt and \'"01738": 73\' in pt and \'"04455": 269\' in pt and "P262: +4-bloki-1838-s18" in pt, "-")'),
      ('leta == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1873]',
       'leta == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1873]'),
      ('len(vseh) == 65', 'len(vseh) == 73'),
      ('skupaj = len(re.findall(r\'bookSignature: "\', src))', 'skupaj = len(re.findall(r\'bookSignature: "\', src))')]),
    # p260 verifier — I5d six/tiers/totals
    ("scripts/p260_notranjost_1835_1836.py",
     [('"sixBook: 39," in stories', '"sixBook: 42," in stories'),
      ('"fiveBook: 29," in stories', '"fiveBook: 26," in stories'),
      ('"{ books: 6, houses: 39,"', '"{ books: 6, houses: 41,"'),
      ('"{ books: 5, houses: 29,"', '"{ books: 5, houses: 27,"'),
      ('"blocks: 2077," in stories', '"blocks: 2085," in stories')]),
]

for path, pairs in FIXES:
    try:
        src = open(f"{ROOT}/{path}", encoding="utf-8").read()
        orig = src
        for a, b in pairs:
            src = src.replace(a, b)
        if src != orig:
            open(f"{ROOT}/{path}", "w", encoding="utf-8").write(src)
            print(f"[OK] {path}")
        else:
            print(f"[SKIP] {path} (brez ujemanj)")
    except FileNotFoundError:
        print(f"[MISS] {path}")

# ——— 3. pt-luknja top vitalsTotal ———
import json
P2 = f"{ROOT}/research/issue17/pt-luknja-18-final.json"
pt2 = json.load(open(P2, encoding="utf-8"))
if pt2.get("vitalsTotal") == 2077:
    pt2["vitalsTotal"] = 2085
    json.dump(pt2, open(P2, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[OK] pt-luknja top vitalsTotal 2077→2085")
else:
    print(f"[SKIP] pt-luknja top vitalsTotal == {pt2.get('vitalsTotal')}")
