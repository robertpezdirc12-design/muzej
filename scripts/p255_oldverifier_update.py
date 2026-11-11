#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P255 — posodobitev STARIH VERIFIKATORJEV na žive številke po P255 (+3 bloki 1828/01738).
Korpus: 2023 → 2026; pt-luknja vitalsTotal 2023 → 2026; 01738-byBook 11 → 14 (p253-I9);
p253-I3 01738-števec 11 → 14; QA-živo-števec 248 → 249 (p243/p244/p246/p247/p248/p252/p254)."""
import os

ROOT = "/home/z/my-project"
changed = {}


def patch(path, pairs):
    if not os.path.exists(path):
        return
    src = open(path, encoding="utf-8").read()
    orig = src
    for old, new in pairs:
        src = src.replace(old, new)
    if src != orig:
        open(path, "w", encoding="utf-8").write(src)
        changed[path] = True
        print(f"  {os.path.basename(path)}: posodobljen")


# Vsi stari verifikatorji z '2023' → '2026' (vitals/pt-luknja).
VERIFIERS = [
    "p235_parish_baptism_1871_04104.py", "p236_parish_synthesis_04104.py",
    "p237_parish_forensics.py", "p238_parish_marriage_1885_04455.py",
    "p239_parish_marriage_1884_04455.py", "p240_parish_marriage_1883_04455.py",
    "p241_parish_marriage_1882_04455.py", "p242_parish_marriage_1881_04455.py",
    "p243_parish_marriage_1880_04455.py", "p244_parish_marriage_1879_04455.py",
    "p246_parish_marriage_1878_04455.py", "p247_parish_marriage_1877_04455.py",
    "p248_parish_marriage_1876_04455.py", "p249_parish_marriage_1875_04455.py",
    "p250_parish_marriage_1874_04455.py", "p251_parish_marriage_1873_04455.py",
    "p252_parish_synthesis_04455.py", "p253_predhodnik_01738.py",
    "p254_house_stories.py",
]
for v in VERIFIERS:
    patch(f"{ROOT}/scripts/{v}", [
        ('"vitalsTotal": 2023', '"vitalsTotal": 2026'),
        ("HOUSE_VITALS.length !== 2023", "HOUSE_VITALS.length !== 2026"),
        ("vitals-2023", "vitals-2026"),
        ("2023-vpisov", "2026-vpisov"),
        ("korpus 2023", "korpus 2026"),
        ("pt-luknja-2023", "pt-luknja-2026"),
        ("== 2023", "== 2026"),
        ("=== 2023", "=== 2026"),
        ("2023/269/11", "2026/269/14"),
        ('"01738": 11', '"01738": 14'),
    ])

# p253 I9/I3: pt-luknja 2026/14 + 01738-števec 14 + PREDHODNIK-2026 (živo) — posebno!
patch(f"{ROOT}/scripts/p253_predhodnik_01738.py", [
    ('check("I9 pt-luknja-2023/01738:11 + byBook", \'"vitalsTotal": 2023\' in pt and \'"01738": 11\' in pt, "-")',
     'check("I9 pt-luknja-2026/01738:14 + byBook (P255!)", \'"vitalsTotal": 2026\' in pt and \'"01738": 14\' in pt, "-")'),
    ('check("I3 vitals == 2023 + 01738 == 11", "HOUSE_VITALS.length !== 2023" not in src and len(vseh) == 11 and skupaj == 2023, f"01738={len(vseh)} skupaj={skupaj}")',
     'check("I3 vitals == 2026 + 01738 == 14 (P255: +3-1828!)", "HOUSE_VITALS.length !== 2026" not in src and len(vseh) == 14 and skupaj == 2026, f"01738={len(vseh)} skupaj={skupaj}")'),
    ('check("I5 qa-p253 + števec-2023", "qa-p253-parish-marriage-predhodnik-01738-1873" in qa and st >= 152, f"2023-številcev={st}")',
     'check("I5 qa-p253 + števec-2026", "qa-p253-parish-marriage-predhodnik-01738-1873" in qa and st >= 152, f"2026-številcev={st}")'),
])

# I10-QA-živo 248 → 249 (kontrole, ki gledajo /api/qa passed-števec)
for v in ["p243_parish_marriage_1880_04455.py", "p244_parish_marriage_1879_04455.py",
          "p246_parish_marriage_1878_04455.py", "p247_parish_marriage_1877_04455.py",
          "p248_parish_marriage_1876_04455.py", "p252_parish_synthesis_04455.py",
          "p254_house_stories.py"]:
    patch(f"{ROOT}/scripts/{v}", [
        ("passed\") == 248", "passed\") == 249"),
        ("passed') == 248", "passed') == 249"),
        ('get("passed") == 248', 'get("passed") == 249'),
        ("248/248", "249/249"),
    ])

print(f"\nSTARI-VERIFIKATORJI: {len(changed)} datotek posodobljenih")
print("KONTROLNA vsota: pričakovano ≥ 18")
