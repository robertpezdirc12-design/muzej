#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P253 — posodobitev STARIH VERIFIKATORJEV na žive številke po P253 (+11 blokov 01738).
Korpus: 2012 → 2023; pt-luknja vitalsTotal 2012 → 2023; 04455-byBook ostaja 269 (01738 = NOVA knjiga!)."""
import re, sys

ROOT = "/home/z/my-project"
changed = {}

def patch(path, pairs, count_only=None):
    src = open(path, encoding="utf-8").read()
    orig = src
    for old, new in pairs:
        src = src.replace(old, new)
    if src != orig:
        open(path, "w", encoding="utf-8").write(src)
        changed[path] = sum(orig.count(o) for o, _ in pairs if o != new)
        print(f"  {path.split('/')[-1]}: posodobljen")

# Vsi stari verifikatorji z '2012' → '2023' (vitals/pt-luknja). 04455-269 ostaja (01738 = nova knjiga!).
VERIFIERS = [
    "p236_parish_synthesis_04104.py", "p237_parish_forensics.py",
    "p238_parish_marriage_1885_04455.py", "p239_parish_marriage_1884_04455.py",
    "p240_parish_marriage_1883_04455.py", "p241_parish_marriage_1882_04455.py",
    "p242_parish_marriage_1881_04455.py", "p243_parish_marriage_1880_04455.py",
    "p244_parish_marriage_1879_04455.py", "p246_parish_marriage_1878_04455.py",
    "p247_parish_marriage_1877_04455.py", "p248_parish_marriage_1876_04455.py",
    "p249_parish_marriage_1875_04455.py", "p250_parish_marriage_1874_04455.py",
    "p251_parish_marriage_1873_04455.py", "p252_parish_synthesis_04455.py",
]
for v in VERIFIERS:
    p = f"{ROOT}/scripts/{v}"
    patch(p, [
        ('"vitalsTotal": 2012', '"vitalsTotal": 2023'),
        ("HOUSE_VITALS.length !== 2012", "HOUSE_VITALS.length !== 2023"),
        ('"vitalsTotal": 1940', '"vitalsTotal": 2023'),
        ("HOUSE_VITALS.length !== 1940", "HOUSE_VITALS.length !== 2023"),
        ("vitals-2012", "vitals-2023"),
        ("2012-vpisov", "2023-vpisov"),
        ("korpus 2012", "korpus 2023"),
        ("pt-luknja-2012", "pt-luknja-2023"),
        ("1940-vpisov", "2023-vpisov"),
    ])

# p251_docs.py / p251_bump.py (dokumentacijske skripte — uskladi števila)
for d in ["p251_docs.py", "p251_bump.py"]:
    p = f"{ROOT}/scripts/{d}"
    if __import__("os").path.exists(p):
        patch(p, [('"vitalsTotal": 2012', '"vitalsTotal": 2023'), ("korpus 2012", "korpus 2023")])

print(f"\nSTARI-VERIFIKATORJI: {len(changed)} datotek posodobljenih")
print("KONTROLNA vsota: pričakovano ≥ 16")
sys.exit(0)
