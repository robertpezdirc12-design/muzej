#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P247 — sanacija STARIH verifikatorjev na žive številke: 1985→1990 · 242→247 ·
sidra-message 235→240 (1877:5!) · dobe 209→214 · pt-luknja-1985→1990."""
import re

ROOT = "/home/z/my-project"
delo = 0

FILES = [
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
    ("HOUSE_VITALS.length !== 1985", "HOUSE_VITALS.length !== 1990"),
    ("skupaj == 242", "skupaj == 247"),
    ('qa.count("HOUSE_VITALS.length !== 1985")', 'qa.count("HOUSE_VITALS.length !== 1990")'),
    ("poročna sidra ≠ 235 (1878:7-P246! · 1879:9-P244! · 1880:3-P243!", "poročna sidra ≠ 240 (1877:5-P247! · 1878:7-P246! · 1879:9-P244! · 1880:3-P243!"),
    ('"poročna sidra ≠ 235 (1878:7-P246!', '"poročna sidra ≠ 240 (1877:5-P247! · 1878:7-P246!'),
    ("dobe-bloki ≠ 209/7/26", "dobe-bloki ≠ 214/7/26"),
    ("39 pred-linijskih 1878-P246×7!", "44 pred-linijskih 1877-P247×5!"),
    ('pt.get("vitalsTotal") == 1985', 'pt.get("vitalsTotal") == 1990'),
    ('.get("04455") == 242', '.get("04455") == 247'),
    ('"vitalsTotal": 1985', '"vitalsTotal": 1990'),
    ('"04455": 242', '"04455": 247'),
    ("vitals-1985 + 04455==242", "vitals-1990 + 04455==247"),
    ("vitals-1985 + 04455==242 (P246-živo!)", "vitals-1990 + 04455==247 (P247-živo!)"),
    ("pt-luknja-1985 + byBook-04455=242", "pt-luknja-1990 + byBook-04455=247"),
    ("len(bloki) == 1985", "len(bloki) == 1990"),
    ("== 1985 blokov", "== 1990 blokov"),
    ("korpus razčlenjen == 1985", "korpus razčlenjen == 1990"),
    ('"1985" in open(f"{ROOT}/scripts/p238', '"1990" in open(f"{ROOT}/scripts/p238'),
    ('"1985" in open(f"{ROOT}/scripts/p237', '"1990" in open(f"{ROOT}/scripts/p237'),
    ("1985-številcev", "1990-številcev"),
    ("pte-luknja-1985", "pte-luknja-1990"),
    ("1985 · 04455", "1990 · 04455"),
    ("1985/242", "1990/247"),
    ("1978→1985", "1985→1990"),
]

for f in FILES:
    src = open(f, encoding="utf-8").read()
    n0 = 0
    for a, b in REPS:
        n = src.count(a)
        if n:
            src = src.replace(a, b)
            n0 += n
            delo += n
    open(f, "w", encoding="utf-8").write(src)
    print(f"{f.split('/')[-1]}: {n0} sprememb")

print(f"P247 stari-verifikatorji: {delo} sprememb")
