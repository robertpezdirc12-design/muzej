#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — KASKADA starih verifierjev (p200–p261): živi števci 2077→2081, 01738 65→69,
leta-01738 +1838, sixBook 39→41/fiveBook 29→27, qa.count HOUSE_VITALS-length 2081."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (stari, novi) splošni vzorci — uporabljeni v VSEH verifierjih
GENERIC = [
    ('qa.count("HOUSE_VITALS.length !== 2077")', 'qa.count("HOUSE_VITALS.length !== 2081")'),
    ('"HOUSE_VITALS.length !== 2077" not in src', '"HOUSE_VITALS.length !== 2081" not in src'),
    ('"HOUSE_VITALS.length !== 2077" in qa', '"HOUSE_VITALS.length !== 2081" in qa'),
    ('"HOUSE_VITALS.length !== 2077" not in qa', '"HOUSE_VITALS.length !== 2081" not in qa'),
    ('pt.get("vitalsTotal") == 2077', 'pt.get("vitalsTotal") == 2081'),
    ('pt_corpus.get("vitalsTotal") == 2077', 'pt_corpus.get("vitalsTotal") == 2081'),
    ("pt2.get(\"vitalsTotal\") == 2077", "pt2.get(\"vitalsTotal\") == 2081"),
    ('\'"vitalsTotal": 2077\' in pt', '\'"vitalsTotal": 2081\' in pt'),
    ('== 2077 blokov (križ z HOUSE_VITALS) — P261-živo!', '== 2081 blokov (križ z HOUSE_VITALS) — P262-živo!'),
    ('{04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:65}', '{04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:69}'),
    ('(04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:65', '(04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:69'),
    ('len(vseh) == 65 and skupaj == 2077', 'len(vseh) == 69 and skupaj == 2081'),
    ('and skupaj == 2077 and min(leta) == 1828', 'and skupaj == 2081 and min(leta) == 1828'),
    ('"blocks: 2077," in stories', '"blocks: 2081," in stories'),
    ('"blocks: 2077" in stories', '"blocks: 2081" in stories'),
    ('"sixBook: 39" in stories', '"sixBook: 41" in stories'),
    ('"fiveBook: 29" in stories', '"fiveBook: 27" in stories'),
    ('["sixBookHouses"]["stories"]) == 39', '["sixBookHouses"]["stories"]) == 41'),
    ('expected_books = {"01738": 65,', 'expected_books = {"01738": 69,'),
    ('.get("01738") == 65', '.get("01738") == 69'),
    ("'\"01738\": 65' in pt", "'\"01738\": 69' in pt"),
    ('leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1873]', 'leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1873]'),
    ('vitals == 2077 + 01738 == 65', 'vitals == 2081 + 01738 == 69'),
    ('vitals-2077 + 04455==269', 'vitals-2081 + 04455==269'),
    ('vsota blokov HOUSE_STORIES == 2077 (P259: +6 + P260: +4 + P261: +8-bloki-1836/37!)', 'vsota blokov HOUSE_STORIES == 2081 (P259: +6 + P260: +4 + P261: +8-bloki-1836/37 + P262: +4-bloki-1838!)'),
]

CHANGED = 0
for path in sorted(glob.glob(f"{ROOT}/scripts/p2[0-6]*.py")):
    name = path.split("/")[-1]
    if "oldverifier" in name or "tmp" in name or "p262" in name:
        continue
    src = open(path, encoding="utf-8").read()
    orig = src
    for a, b in GENERIC:
        if a in src:
            src = src.replace(a, b)
    # kozmetika: številcev-oznake v I5 sporočilih (2077-živi → 2081)
    src = re.sub(r'f"(\d{4})-številcev=\{st(\d*)\}"', r'f"2081-številcev={st\2}"', src)
    if src != orig:
        open(path, "w", encoding="utf-8").write(src)
        CHANGED += 1
        print(f"[UPDATED] {name}")
print("skupaj spremenjenih:", CHANGED)
