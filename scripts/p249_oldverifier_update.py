#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P249 — sanacija STARIH verifikatorjev na žive številke: 1996→1997 · 253→254 ·
sidra-message 246→247 (1875:1!) · dobe 220→221 (51-pred-linijskih!) ·
pt-luknja-1996→1997 · + sken-range-8–10-garda-omejitev (1876-garda-ostaja!)."""
ROOT = "/home/z/my-project"
delo = 0

FILES = [
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
    ("HOUSE_VITALS.length !== 1996", "HOUSE_VITALS.length !== 1997"),
    ("skupaj == 253", "skupaj == 254"),
    ('qa.count("HOUSE_VITALS.length !== 1996")', 'qa.count("HOUSE_VITALS.length !== 1997")'),
    ("poročna sidra ≠ 246 (1876:6-P248!", "poročna sidra ≠ 247 (1875:1-P249! · 1876:6-P248!"),
    ('"poročna sidra ≠ 246 (1876:6-P248!', '"poročna sidra ≠ 247 (1875:1-P249! · 1876:6-P248!'),
    ("dobe-bloki ≠ 220/7/26", "dobe-bloki ≠ 221/7/26"),
    ("50 pred-linijskih 1876-P248×6!", "51 pred-linijskih 1875-P249×1!+1876-P248×6!"),
    ('pt.get("vitalsTotal") == 1996', 'pt.get("vitalsTotal") == 1997'),
    ('.get("04455") == 253', '.get("04455") == 254'),
    ('"vitalsTotal": 1996', '"vitalsTotal": 1997'),
    ('"04455": 253', '"04455": 254'),
    ("vitals-1996 + 04455==253", "vitals-1997 + 04455==254"),
    ("pt-luknja-1996 + byBook-04455=253", "pt-luknja-1997 + byBook-04455=254"),
    ("len(bloki) == 1996", "len(bloki) == 1997"),
    ("== 1996 blokov", "== 1997 blokov"),
    ("korpus razčlenjen == 1996", "korpus razčlenjen == 1997"),
    ('"1996" in open(f"{ROOT}/scripts/p238', '"1997" in open(f"{ROOT}/scripts/p238'),
    ('"1996" in open(f"{ROOT}/scripts/p237', '"1997" in open(f"{ROOT}/scripts/p237'),
    ("1996-številcev", "1997-številcev"),
    ("pte-luknja-1996", "pte-luknja-1997"),
    ("1996 · 04455", "1997 · 04455"),
    ("1996/253", "1997/254"),
    ("1990→1996", "1996→1997"),
    ("st >= 150", "st >= 150"),
]

for f in FILES:
    try:
        src = open(f, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"  [!] manjka: {f}")
        continue
    orig = src
    fdelo = 0
    for a, b in REPS:
        n = src.count(a)
        if n and a != b:
            src = src.replace(a, b)
            fdelo += n
            delo += n
    if src != orig:
        open(f, "w", encoding="utf-8").write(src)
        print(f"  {f.split('/')[-1]}: {fdelo} sprememb")
    else:
        print(f"  {f.split('/')[-1]}: 0")
print(f"P249 oldverifier-update: {delo} sprememb")
