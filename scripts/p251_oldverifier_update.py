#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P251 — sanacija STARIH verifikatorjev na žive številke: 2008→2012 · 265→269 ·
sidra-message 258→262 (1873:4-P251! na vrh!) · dobe 232→236 (66-pred-linijskih!) ·
MILIČ 243→247 (56→60!) · p237-2012/269 · p238-števec · oznake."""
import re

ROOT = "/home/z/my-project"
delo = 0

FILES = [
    f"{ROOT}/scripts/p250_parish_marriage_1874_04455.py",
    f"{ROOT}/scripts/p249_parish_marriage_1875_04455.py",
    f"{ROOT}/scripts/p248_parish_marriage_1876_04455.py",
    f"{ROOT}/scripts/p247_parish_marriage_1877_04455.py",
    f"{ROOT}/scripts/p246_parish_marriage_1878_04455.py",
    f"{ROOT}/scripts/p244_parish_marriage_1879_04455.py",
    f"{ROOT}/scripts/p243_parish_marriage_1880_04455.py",
    f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py",
    f"{ROOT}/scripts/p241_parish_marriage_1882_04455.py",
    f"{ROOT}/scripts/p240_parish_marriage_1883_04455.py",
    f"{ROOT}/scripts/p239_parish_marriage_1884_04455.py",
    f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py",
    f"{ROOT}/scripts/p237_parish_forensics.py",
]

REPS = [
    # ——— vitals 2008→2012 / negativni-gardi ———
    ('qa.count("HOUSE_VITALS.length !== 2023")', 'qa.count("HOUSE_VITALS.length !== 2012")'),
    ('"HOUSE_VITALS.length !== 2023" not in src', '"HOUSE_VITALS.length !== 2011" not in src'),
    ("HOUSE_VITALS.length !== 2007", "HOUSE_VITALS.length !== 2011"),
    # ——— 04455 265→269 ———
    ("vitals-2008 + 04455==265", "vitals-2012 + 04455==269"),
    ("skupaj == 265", "skupaj == 269"),
    ('\'"vitalsTotal": 2023\' in pt', '\'"vitalsTotal": 2012\' in pt'),
    ('\'"04455": 265\' in pt', '\'"04455": 269\' in pt'),
    ('pt.get("vitalsTotal") == 2023', 'pt.get("vitalsTotal") == 2023'),
    ('.get("04455") == 265', '.get("04455") == 269'),
    # ——— sidra 258→262 + 1873:4-P251! na vrh sporočila ———
    ("poročna sidra ≠ 258 (1874:11-P250!", "poročna sidra ≠ 262 (1873:4-P251! · 1874:11-P250!"),
    # ——— dobe 232→236 + 66-pred-linijskih (1873-P251×4! na vrh) ———
    ("dobe-bloki ≠ 232/7/26", "dobe-bloki ≠ 236/7/26"),
    ("62 pred-linijskih 1874-P250×11!", "66 pred-linijskih 1873-P251×4!+1874-P250×11!"),
    # ——— MILIČ 243→247 (56→60) ———
    ("MILIC_FAMILY_TOTAL !== 243", "MILIC_FAMILY_TOTAL !== 247"),
    ("53,78,20,36,56", "53,78,20,36,60"),
    # ——— p237-specific ———
    ("len(bloki) == 2023", "len(bloki) == 2012"),
    ("== 2023 blokov", "== 2012 blokov"),
    ("04455:242}", "04455:269}"),
    ("04455:242)", "04455:269)"),
]

OZNAKE = [
    # kozmetika oznak (samo labelo popravi, ne preverjanj)
    (r"števec-\d{4}", "števec-2012"),
    (r"\d{4}-številcev=\{st\}", "2012-številcev={st}"),
    (r"sidra-\d{3} \+", "sidra-262 +"),
    (r"I5b sidra-\d{3}", "I5b sidra-262"),
    (r"skupaj 243", "skupaj 247"),
    (r"243/53-78-20-36-56", "247/53-78-20-36-60"),
    (r"preverja 243/", "preverja 247/"),
    (r"MILIČ-241 \+", "MILIČ-247 +"),
    (r"MILIČ-243", "MILIČ-247"),
    (r"vitals-1966 \+ 04455==223", "vitals-2012 + 04455==269"),
    (r"živi preverja 243/53-78-20-36-56", "živi preverja 247/53-78-20-36-60"),
]

for f in FILES:
    src = open(f, encoding="utf-8").read()
    pred = delo
    for a, b in REPS:
        n = src.count(a)
        if n:
            src = src.replace(a, b)
            delo += n
    for pat, b in OZNAKE:
        src, n = re.subn(pat, b, src)
        delo += n
    if delo > pred:
        open(f, "w", encoding="utf-8").write(src)
        print(f"  {f.split('/')[-1]}: {delo - pred} sprememb")
    else:
        print(f"  {f.split('/')[-1]}: brez sprememb (že živo?)")

print(f"\nSKUPAJ: {delo} sprememb")
