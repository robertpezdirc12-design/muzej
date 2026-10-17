#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P95 fix — zastarele skripte p85–p94: vitals 254, kumulativ 260, hiše 79,
filtri vesolja + 1900 (poznejši bloki ne smejo spreminjati zgodovinske
klasifikacije novih hiš)."""
import re

FIXES = {
    "scripts/p85_parish_baptism_1890.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 91 + 21 (p80 I7 pin); P86: + 9 (1891); P87: + 12 (1892); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 91 + 21 (p80 I7 pin); P86: + 9 (1891); P87: + 12 (1892); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899)',
         'v["year"] in (1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900)'),
        ("n_entries_total + ev_only_total == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + ev_only_total == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p86_parish_baptism_1891.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 121 + 12 (p80 I7 pin); P87: + 12 (1892); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 121 + 12 (p80 I7 pin); P87: + 12 (1892); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899)',
         'v["year"] in (1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900)'),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p87_parish_baptism_1892.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 121 + 12 (p80 I7 pin); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 121 + 12 (p80 I7 pin); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1893, 1894, 1895, 1896, 1897, 1898, 1899)',
         'v["year"] in (1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900)'),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p88_parish_baptism_1893.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 133 + 17 (p80 I7 pin); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 133 + 17 (p80 I7 pin); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1894, 1895, 1896, 1897, 1898, 1899)',
         'v["year"] in (1894, 1895, 1896, 1897, 1898, 1899, 1900)'),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p89_parish_baptism_1894.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 179 + 14 (p80 I7 pin); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 179 + 14 (p80 I7 pin); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1895, 1896, 1897, 1898, 1899)',
         'v["year"] in (1895, 1896, 1897, 1898, 1899, 1900)'),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p90_parish_baptism_1895.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 179 + 15 (p80 I7 pin); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 179 + 15 (p80 I7 pin); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1896, 1897, 1898, 1899)',
         'v["year"] in (1896, 1897, 1898, 1899, 1900)'),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p91_parish_baptism_1896.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 179 + 14 (p80 I7 pin); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 179 + 14 (p80 I7 pin); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1897, 1898, 1899)',
         'v["year"] in (1897, 1898, 1899, 1900)'),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p92_parish_baptism_1897.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 211 + 12 (P93: krstna 1898); h61 sidro = P79-era placeholder ZDRUŽEN, ne dupliran; P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 211 + 12 (P93: krstna 1898); h61 sidro = P79-era placeholder ZDRUŽEN, ne dupliran; P94: + 15 (1899); P95: + 16 (1900)"),
        ('v["year"] in (1898, 1899)',
         'v["year"] in (1898, 1899, 1900)'),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p93_parish_baptism_1898.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 211 + 12 (P93: krstna 1898); P94: + 15 (1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 211 + 12 (P93: krstna 1898); P94: + 15 (1899); P95: + 16 (1900)"),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
    ],
    "scripts/p94_parish_baptism_1899.py": [
        ("EXPECTED_VITALS_TOTAL = 238     # HOUSE_VITALS 223 + 15 (P94: krstna 1899)",
         "EXPECTED_VITALS_TOTAL = 254     # HOUSE_VITALS 223 + 15 (P94: krstna 1899); P95: + 16 (1900)"),
        ("n_entries_total + EV_ONLY_TOTAL == 244  # kumulativno po P94 (238 + 6)",
         "n_entries_total + EV_ONLY_TOTAL == 260  # kumulativno po P95 (254 + 6)"),
        ("n_houses_total == 78  # P93: 76; P94: + 2 (22, 49)",
         "n_houses_total == 79  # P94: 78; P95: + 1 (67)"),
        ("# (22/49); kumulativ 238 + 6 EV-only == 244; hiše vitals 78; duhovniki",
         "# (22/49); kumulativ 254 + 6 EV-only == 260; hiše vitals 79; duhovniki"),
        ("# stran == sken − 3; vitals skupaj 238",
         "# stran == sken − 3; vitals skupaj 254"),
    ],
}

for path, pairs in FIXES.items():
    src = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in src:
            print(f"MISS {path}: {old[:70]}...")
        else:
            src = src.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(src)
    print(f"OK  {path}")
