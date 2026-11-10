#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P246 — sanacija STARIH verifikatorjev na žive številke: 1978→1985 · 235→242 ·
sidra-message 228→235 (1878:7!) · dobe 202/7/26→209/7/26 · pt-luknja-1978→1985."""
import re

ROOT = "/home/z/my-project"
delo = 0

FILES = [
    f"{ROOT}/scripts/p243_parish_marriage_1880_04455.py",
    f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py",
    f"{ROOT}/scripts/p241_parish_marriage_1882_04455.py",
    f"{ROOT}/scripts/p240_parish_marriage_1883_04455.py",
    f"{ROOT}/scripts/p239_parish_marriage_1884_04455.py",
    f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py",
    f"{ROOT}/scripts/p237_parish_forensics.py",
]

REPS = [
    ("HOUSE_VITALS.length !== 1978", "HOUSE_VITALS.length !== 1985"),
    ("skupaj == 235", "skupaj == 242"),
    ('qa.count("HOUSE_VITALS.length !== 1978")', 'qa.count("HOUSE_VITALS.length !== 1985")'),
    ("poročna sidra ≠ 228 (1879:9-P244! · 1880:3-P243!", "poročna sidra ≠ 235 (1878:7-P246! · 1879:9-P244! · 1880:3-P243!"),
    ('"poročna sidra ≠ 228 (1879:9-P244!', '"poročna sidra ≠ 235 (1878:7-P246! · 1879:9-P244!'),
    ("dobe-bloki ≠ 202/7/26", "dobe-bloki ≠ 209/7/26"),
    ("32 pred-linijskih 1879-P244×9!", "39 pred-linijskih 1878-P246×7!"),
    ('pt.get("vitalsTotal") == 1978', 'pt.get("vitalsTotal") == 1985'),
    ('.get("04455") == 235', '.get("04455") == 242'),
    ('"vitalsTotal": 1978', '"vitalsTotal": 1985'),
    ('"04455": 235', '"04455": 242'),
    ("vitals-1978 + 04455==235", "vitals-1985 + 04455==242"),
    ("vitals-1966 + 04455==223 (P241-živo!)", "vitals-1985 + 04455==242 (P246-živo!)"),
    ("pt-luknja-1978 + byBook-04455=235", "pt-luknja-1985 + byBook-04455=242"),
    ("len(bloki) == 1978", "len(bloki) == 1985"),
    ("== 1978 blokov", "== 1985 blokov"),
    ("korpus razčlenjen == 1978", "korpus razčlenjen == 1985"),
    ('"1978" in open(f"{ROOT}/scripts/p238', '"1985" in open(f"{ROOT}/scripts/p238'),
    ('"1978" in open(f"{ROOT}/scripts/p237', '"1985" in open(f"{ROOT}/scripts/p237'),
    ("1978-številcev", "1985-številcev"),
    ("pte-luknja-1978", "pte-luknja-1985"),
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

print(f"P246 stari-verifikatorji: {delo} sprememb")
