#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250 — sanacija STARIH verifikatorjev na žive številke: 1997→2008 · 254→265 ·
sidra-message 247→258 (1874:11!) · dobe 221→232 (62-pred-linijskih!) ·
MILIČ 241→243 (54→56!) · h65 {42,36,6}→{43,37,6} · Mathias-h65 22→23 ·
pt-luknja-1997→2008 · + sken-range-2–7-garda (1875-garda-ostaja!)."""
ROOT = "/home/z/my-project"
delo = 0

FILES = [
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
    # vitals
    ("HOUSE_VITALS.length !== 1997", "HOUSE_VITALS.length !== 2008"),
    ("HOUSE_VITALS ≠ 1997", "HOUSE_VITALS ≠ 2008"),
    ('qa.count("HOUSE_VITALS.length !== 1997")', 'qa.count("HOUSE_VITALS.length !== 2008")'),
    ("1997-številcev", "2008-številcev"),
    ("vitals-1997 + 04455==254", "vitals-2008 + 04455==265"),
    ("pt-luknja-1997 + byBook-04455=254", "pt-luknja-2008 + byBook-04455=265"),
    ('pt.get("vitalsTotal") == 1997', 'pt.get("vitalsTotal") == 2008'),
    ('.get("04455") == 254', '.get("04455") == 265'),
    ('"vitalsTotal": 1997', '"vitalsTotal": 2008'),
    ('"04455": 254', '"04455": 265'),
    ("skupaj == 254", "skupaj == 265"),
    ("skupaj-04455 == 254", "skupaj-04455 == 265"),
    ("== 1997", "== 2008"),
    ("vitals 1997", "vitals 2008"),
    ("vitalsTotal 1997", "vitalsTotal 2008"),
    ("1997 vitals", "2008 vitals"),
    ("1997 vitalov", "2008 vitalov"),
    # bloki-04455
    ("04455==254", "04455==265"),
    ("254 (04455", "265 (04455"),
    ("bloki 04455 == 254", "bloki 04455 == 265"),
    ("byBook-04455=254", "byBook-04455=265"),
    ("byBook 04455 = 254", "byBook 04455 = 265"),
    ("04455 = 254", "04455 = 265"),
    ("04455-254", "04455-265"),
    ("254/04455", "265/04455"),
    # sidra
    ("poročna sidra ≠ 247 (1875:1-P249! · 1876:6-P248!", "poročna sidra ≠ 258 (1874:11-P250! · 1875:1-P249! · 1876:6-P248!"),
    ('"poročna sidra ≠ 247 (1875:1-P249!', '"poročna sidra ≠ 258 (1874:11-P250! · 1875:1-P249!'),
    ("poročna sidra ≠ 247 (${p80MarrAnchors.length} — 246-P248 + 1-h8-1875-P249!)",
     "poročna sidra ≠ 258 (${p80MarrAnchors.length} — 247-P249 + 11-blokov-1874-P250!)"),
    ("p80MarrAnchors.length !== 247", "p80MarrAnchors.length !== 258"),
    ("sidra-247", "sidra-258"),
    ("sidra 247", "sidra 258"),
    ("≠ 247 (", "≠ 258 ("),
    # dobe
    ("dobe-bloki ≠ 221/7/26", "dobe-bloki ≠ 232/7/26"),
    ("p152Pre !== 221", "p152Pre !== 232"),
    ("dobe 221", "dobe 232"),
    ("221/7/26", "232/7/26"),
    ("51 pred-linijskih 1875-P249×1!", "62 pred-linijskih 1874-P250×11!+1875-P249×1!"),
    ("62-pred-linijskih", "62-pred-linijskih"),
    # MILIČ + p237-forenzika
    ("MILIC_FAMILY_TOTAL !== 241", "MILIC_FAMILY_TOTAL !== 243"),
    ("MILIČ-family-total ≠ 241", "MILIČ-family-total ≠ 243"),
    ("neodvisni-križ-proti-korpusu ≠ 241", "neodvisni-križ-proti-korpusu ≠ 243"),
    ("p237Križ !== 241", "p237Križ !== 243"),
    ('join(",") !== "53,78,20,36,54"', 'join(",") !== "53,78,20,36,56"'),
    ("MILIČ-po-knjigah ≠ [53,78,20,36,54]", "MILIČ-po-knjigah ≠ [53,78,20,36,56]"),
    ("Mathias/Matija-h65-veriga ≠ 22", "Mathias/Matija-h65-veriga ≠ 23"),
    ("MATHIAS_H65_TOTAL !== 22", "MATHIAS_H65_TOTAL !== 23"),
    ("h65 ≠ {42, 36, 6}", "h65 ≠ {43, 37, 6}"),
    ("H65_STATS.total !== 42 || H65_STATS.family !== 36", "H65_STATS.total !== 43 || H65_STATS.family !== 37"),
    # sken-range-garda-omejitev (1874-garda-ne-sme-lomiti-starih-letalskih-gard!)
    ("skeni izven 7–10", "skeni izven 7–10"),
]

for f in FILES:
    try:
        src = open(f, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"  MANJKA: {f}")
        continue
    orig = len(src)
    n = 0
    for a, b in REPS:
        if a != b and a in src:
            k = src.count(a)
            src = src.replace(a, b)
            n += k
            delo += k
    if n:
        open(f, "w", encoding="utf-8").write(src)
    print(f"  {f.split('/')[-1]}: {n} sprememb ({orig}→{len(src)})")

print(f"P250 oldverifier update: {delo} sprememb")
