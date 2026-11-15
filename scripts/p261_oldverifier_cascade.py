#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P261 — KASKADA starih verifierjev (p200–p260): živi števci 2069→2077, 01738 57→65,
leta-01738 +1837, sixBook 36→39/fiveBook 32→29, qa.countHOUSE_VITALS-length 2077."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (stari, novi) splošni vzorci — uporabljeni v VSEH verifierjih
GENERIC = [
    ('qa.count("HOUSE_VITALS.length !== 2069")', 'qa.count("HOUSE_VITALS.length !== 2077")'),
    ('"HOUSE_VITALS.length !== 2069" not in src', '"HOUSE_VITALS.length !== 2077" not in src'),
    ('"HOUSE_VITALS.length !== 2069" in qa', '"HOUSE_VITALS.length !== 2077" in qa'),
    ('"HOUSE_VITALS.length !== 2069" not in qa', '"HOUSE_VITALS.length !== 2077" not in qa'),
    ('pt.get("vitalsTotal") == 2069', 'pt.get("vitalsTotal") == 2077'),
    ('pt_corpus.get("vitalsTotal") == 2069', 'pt_corpus.get("vitalsTotal") == 2077'),
    ("pt2.get(\"vitalsTotal\") == 2069", "pt2.get(\"vitalsTotal\") == 2077"),
    ('\'"vitalsTotal": 2069\' in pt', '\'"vitalsTotal": 2077\' in pt'),
    ('== 2069 blokov (križ z HOUSE_VITALS) — P260-živo!', '== 2077 blokov (križ z HOUSE_VITALS) — P261-živo!'),
    ('{04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:57}', '{04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:65}'),
    ('(04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:65', '(04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:65'),
    ('len(vseh) == 57 and skupaj == 2069', 'len(vseh) == 65 and skupaj == 2077'),
    ('and skupaj == 2069 and min(leta) == 1828', 'and skupaj == 2077 and min(leta) == 1828'),
    ('"blocks: 2069," in stories', '"blocks: 2077," in stories'),
    ('"blocks: 2069" in stories', '"blocks: 2077" in stories'),
    ('"sixBook: 36" in stories', '"sixBook: 39" in stories'),
    ('"fiveBook: 32" in stories', '"fiveBook: 29" in stories'),
    ('["sixBookHouses"]["stories"]) == 36', '["sixBookHouses"]["stories"]) == 39'),
    ('expected_books = {"01738": 57,', 'expected_books = {"01738": 65,'),
    ('.get("01738") == 57', '.get("01738") == 65'),
    ("'\"01738\": 57' in pt", "'\"01738\": 65' in pt"),
    ('leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1873]', 'leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1873]'),
    ('vitals == 2069 + 01738 == 57', 'vitals == 2077 + 01738 == 65'),
    ('vitals-2026 + 04455==269', 'vitals-2077 + 04455==269'),
    ('vsota blokov HOUSE_STORIES == 2069 (P259: +6 + P260: +4!)', 'vsota blokov HOUSE_STORIES == 2077 (P259: +6 + P260: +4 + P261: +8-bloki-1836/37!)'),
]

CHANGED = 0
for path in sorted(glob.glob(f"{ROOT}/scripts/p2[0-6]*.py")):
    name = path.split("/")[-1]
    if "oldverifier" in name or "tmp" in name:
        continue
    src = open(path, encoding="utf-8").read()
    orig = src
    for a, b in GENERIC:
        if a in src:
            src = src.replace(a, b)
    # kozmetika: številcev-oznake v I5 sporočilih (1940/2012/2059/2043 → 2077-živi)
    src = re.sub(r'f"(?:1940|2012|2059|2043)-številcev=\{st\}"', 'f"2077-številcev={st}"', src)
    src = re.sub(r'f"(\d{4})-številcev=\{st(\d*)\}"', r'f"2077-številcev={st\2}"', src)
    if src != orig:
        open(path, "w", encoding="utf-8").write(src)
        CHANGED += 1
        print(f"[UPDATED] {name}")
print("skupaj spremenjenih:", CHANGED)
