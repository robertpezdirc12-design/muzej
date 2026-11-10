#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P248 — sanacija STARIH verifikatorjev na žive številke: 1990→1996 · 247→253 ·
sidra-message 240→246 (1876:6!) · dobe 214→220 (50-pred-linijskih!) ·
MILIČ 240→241 + [53,78,20,36,54] · pt-luknja-1990→1996."""
ROOT = "/home/z/my-project"
delo = 0

FILES = [
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
    ("HOUSE_VITALS.length !== 1990", "HOUSE_VITALS.length !== 1996"),
    ("skupaj == 247", "skupaj == 253"),
    ('qa.count("HOUSE_VITALS.length !== 1990")', 'qa.count("HOUSE_VITALS.length !== 1996")'),
    ("poročna sidra ≠ 240 (1877:5-P247!", "poročna sidra ≠ 246 (1876:6-P248! · 1877:5-P247!"),
    ('"poročna sidra ≠ 240 (1877:5-P247!', '"poročna sidra ≠ 246 (1876:6-P248! · 1877:5-P247!'),
    ("dobe-bloki ≠ 214/7/26", "dobe-bloki ≠ 220/7/26"),
    ("44 pred-linijskih 1877-P247×5!", "50 pred-linijskih 1876-P248×6!+1877-P247×5!"),
    ('pt.get("vitalsTotal") == 1990', 'pt.get("vitalsTotal") == 1996'),
    ('.get("04455") == 247', '.get("04455") == 253'),
    ('"vitalsTotal": 1990', '"vitalsTotal": 1996'),
    ('"04455": 247', '"04455": 253'),
    ("vitals-1990 + 04455==247", "vitals-1996 + 04455==253"),
    ("pt-luknja-1990 + byBook-04455=247", "pt-luknja-1996 + byBook-04455=253"),
    ("len(bloki) == 1990", "len(bloki) == 1996"),
    ("== 1990 blokov", "== 1996 blokov"),
    ("korpus razčlenjen == 1990", "korpus razčlenjen == 1996"),
    ('"1990" in open(f"{ROOT}/scripts/p238', '"1996" in open(f"{ROOT}/scripts/p238'),
    ('"1990" in open(f"{ROOT}/scripts/p237', '"1996" in open(f"{ROOT}/scripts/p237'),
    ("1990-številcev", "1996-številcev"),
    ("pte-luknja-1990", "pte-luknja-1996"),
    ("1990 · 04455", "1996 · 04455"),
    ("1990/247", "1996/253"),
    ("1985→1990", "1990→1996"),
    # MILIČ-garde 240→241
    ("MILIC_FAMILY_TOTAL !== 240", "MILIC_FAMILY_TOTAL !== 241"),
    ("MILIČ-family-total ≠ 240", "MILIČ-family-total ≠ 241"),
    ('p237PoKnjigah.join(",") !== "53,78,20,36,53"', 'p237PoKnjigah.join(",") !== "53,78,20,36,54"'),
    ("MILIČ-po-knjigah ≠ [53,78,20,36,53]", "MILIČ-po-knjigah ≠ [53,78,20,36,54]"),
    ("53+78+20+36+53 čez 5 knjig", "53+78+20+36+54 čez 5 knjig"),
    ("if (p237Križ !== 240)", "if (p237Križ !== 241)"),
    ("neodvisni-križ-proti-korpusu ≠ 240", "neodvisni-križ-proti-korpusu ≠ 241"),
    ("MILIČ-240", "MILIČ-241"),
    # p85-izjeme-1876-h30/h41 v starih verifikatorjih (če jih preverjajo)
    ('v.year === 1881 && hn === "41"))', 'v.year === 1881 && hn === "41")) && !(v.bookSignature === "04455" && v.year === 1876 && (hn === "30" || hn === "41"))'),
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
print(f"P248 oldverifier-update: {delo} sprememb")
