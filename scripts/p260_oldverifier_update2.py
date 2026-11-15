#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — update2: preostali precision-popravki starih preverjevalnikov + ponovna pt-luknja json sanacija.
(bump-veriga iz enkratnega pomota je json povrnila na 2008/265 — part A ponovno nanesam.)"""
import json

ROOT = "/home/z/my-project"
log = []

# ============ A) pt-luknja-18-final.json (ponovno — bump-veriga je revertirala!) ============
PT = f"{ROOT}/research/issue17/pt-luknja-18-final.json"
d = json.load(open(PT, encoding="utf-8"))
d["vitalsTotal"] = 2069
d["corpus"]["vitalsTotal"] = 2069
d["corpus"]["byBook"]["01738"] = 57
d["corpus"]["byBook"]["04455"] = 269
live = {
    "42": (28, {"01738": 1, "04104": 3, "04105": 5, "04455": 5, "04106": 6, "04894": 8}, 1832),
    "51": (12, {"01738": 1, "04104": 2, "04455": 2, "04106": 3, "04894": 4}, 1834),
    "53": (34, {"01738": 1, "04104": 5, "04105": 7, "04455": 4, "04106": 6, "04894": 11}, 1833),
}
for gh in d["gapHouses"]:
    hn = str(gh.get("houseNo"))
    if hn in live:
        b, bb, fy = live[hn]
        gh["blocksTotal"] = b
        gh["byBook"] = bb
        gh["firstYear"] = fy
        if "p260Note" not in gh:
            gh["p260Note"] = f"P260-integracija: živo-{b}-blokov (01738-blok-P259/P260!-firstYear→{fy}-DVIG!)"
note = d["corpus"].get("housesNote", "")
if "P260:" not in note:
    d["corpus"]["housesNote"] = note + " | P260: +4-bloki-1835/36-01738 (01738 53→57, vitals 2065→2069!-h4-DVIG-39-NOV-ABSOLUTNI-REKORD + SIBLING-SWAP-h9×h63 + h4/h9-ŠEST-KNJIŽNI!)"
d["generatedAt"] = "2026-11-12 (P260-posodobitev)"
json.dump(d, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
log.append("A) pt-luknja json ponovno: 2069/57/269 + h42/h51/h53-živo")


def bump(path, pairs):
    src = open(path, encoding="utf-8").read()
    n0 = len(src)
    cnt = 0
    for a, b in pairs:
        c = src.count(a)
        if c:
            src = src.replace(a, b)
            cnt += c
    open(path, "w", encoding="utf-8").write(src)
    if cnt:
        log.append(f"{path.split('/')[-1]}: {cnt} zamenjav")
    return cnt


# ============ B) I2-pogoji: len(vseh) == 47 and skupaj == 2059 → 57/2069 ============
for f in ["p253_predhodnik_01738.py", "p255_notranjost_01738.py", "p256_1829.py", "p257_1830_1831.py"]:
    bump(f"{ROOT}/scripts/{f}", [
        ("len(vseh) == 47 and skupaj == 2059 and min(leta) == 1828",
         "len(vseh) == 57 and skupaj == 2069 and min(leta) == 1828"),
        ("len(vseh) == 47 and skupaj == 2059,",
         "len(vseh) == 57 and skupaj == 2069,"),
    ])
bump(f"{ROOT}/scripts/p258_meja_1831_32_33.py", [
    ("len(vseh) == 47 and skupaj == 2059\n", "len(vseh) == 57 and skupaj == 2069\n"),
])

# ============ C) '"vitalsTotal": 2059' in open(...pt json...) → 2069 ============
for f in ["p239_parish_marriage_1884_04455.py", "p240_parish_marriage_1883_04455.py",
          "p241_parish_marriage_1882_04455.py", "p242_parish_marriage_1881_04455.py",
          "p200_parish_death_1877_04106.py", "p201_parish_death_1876_04106.py",
          "p202_parish_death_1875_04106.py", "p203_parish_death_1874_04106.py",
          "p204_parish_death_1873_04106.py"]:
    bump(f"{ROOT}/scripts/{f}", [
        ('\'"vitalsTotal": 2059\' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json"',
         '\'"vitalsTotal": 2069\' in open(f"{ROOT}/research/issue17/pt-luknja-18-final.json"'),
    ])

# ============ D) I9c-verižne kontrole (v232/v233/v234) 2059 → 2069 ============
for f, v in [("p233_parish_baptism_1873_04104.py", "v232"), ("p234_parish_baptism_1872_04104.py", "v233"),
             ("p235_parish_baptism_1871_04104.py", "v234")]:
    bump(f"{ROOT}/scripts/{f}", [
        (f'\'"vitalsTotal": 2059\' in {v}', f'\'"vitalsTotal": 2069\' in {v}'),
    ])

# ============ E) I9c stari-verifikatorji: "2059" in p238 → "2069" ============
for f in ["p241_parish_marriage_1882_04455.py", "p242_parish_marriage_1881_04455.py",
          "p243_parish_marriage_1880_04455.py", "p244_parish_marriage_1879_04455.py",
          "p246_parish_marriage_1878_04455.py", "p247_parish_marriage_1877_04455.py",
          "p248_parish_marriage_1876_04455.py", "p249_parish_marriage_1875_04455.py"]:
    bump(f"{ROOT}/scripts/{f}", [
        ('"2059" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py"',
         '"2069" in open(f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py"'),
    ])

# ============ F) p237 forensics: 2059 → 2069 + 01738 47 → 57 ============
bump(f"{ROOT}/scripts/p237_parish_forensics.py", [
    ("check(\"I1 korpus razčlenjen == 2059 blokov (križ z HOUSE_VITALS) — P257-živo!\",\n      len(bloki) == 2059",
     "check(\"I1 korpus razčlenjen == 2069 blokov (križ z HOUSE_VITALS) — P260-živo!\",\n      len(bloki) == 2069"),
    ('check("I1b bloki-po-knjigah == {04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:47} (P258-živo!)",\n      po_knjigi == {"04104": 288, "04105": 502, "04106": 433, "04894": 520, "04455": 269, "01738": 47},',
     'check("I1b bloki-po-knjigah == {04104:288, 04105:502, 04106:433, 04894:520, 04455:269, 01738:57} (P260-živo!)",\n      po_knjigi == {"04104": 288, "04105": 502, "04106": 433, "04894": 520, "04455": 269, "01738": 57},'),
])

# ============ G) p248 I8b: h51 živo 12 ============
bump(f"{ROOT}/scripts/p248_parish_marriage_1876_04455.py", [
    ('check("I8b h44-posodobljen (24-blokov/04455=6/firstYear=1876/p248Note!) + h51-intakten (6/2!)",\n      h44["blocksTotal"] == 24 and h44["byBook"]["04455"] == 6 and h44["firstYear"] == 1876 and "p248Note" in h44\n      and h51["blocksTotal"] == 6 and h51["byBook"]["04455"] == 2)',
     'check("I8b h44-posodobljen (24-blokov/04455=6/firstYear=1876/p248Note!) + h51-živo-P259/P260 (12/2!)",\n      h44["blocksTotal"] == 24 and h44["byBook"]["04455"] == 6 and h44["firstYear"] == 1876 and "p248Note" in h44\n      and h51["blocksTotal"] == 12 and h51["byBook"]["04455"] == 2)'),
])

# ============ H) p254 I9: pt_corpus 2059 → 2069 ============
bump(f"{ROOT}/scripts/p254_house_stories.py", [
    ('pt_corpus.get("vitalsTotal") == 2059', 'pt_corpus.get("vitalsTotal") == 2069'),
])

# ============ I) p255 I6b: pt-tiers 31/31 → 36/36 ============
bump(f"{ROOT}/scripts/p255_notranjost_01738.py", [
    ('pt["structure"]["tiers"]["six"] == 31\n      and len(pt["sixBookHouses"]["stories"]) == 31',
     'pt["structure"]["tiers"]["six"] == 36\n      and len(pt["sixBookHouses"]["stories"]) == 36'),
])

# ============ J) p257 I6: firstYear-1831-števec 10 → 15 + h50m books-5 ============
bump(f"{ROOT}/scripts/p257_1830_1831.py", [
    ("len(re.findall(r'firstYear: 1831, lastYear', stories)) == 10",
     "len(re.findall(r'firstYear: 1831, lastYear', stories)) == 15"),
    ('houseNo: "50", kind: "griblje", blocks: 13, books: 6',
     'houseNo: "50", kind: "griblje", blocks: 13, books: 5'),
])

print("\n".join(log))
print(f"\n=== P260-update2: {len(log)} korakov ===")
