#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P260 — kaskadna posodobitev starih preverjevalnikov + dokazov (po vzoru P258-oldverifier).
A) pt-luknja-18-final.json: vitalsTotal 2008→2069 + byBook-01738 53→57 + 04455 265→269
   + gapHouses h42/h51/h53 → žive vrednosti (P259/P260-bloki!) + housesNote + P260.
B) parish-house-stories.json (dokaz): tiers.six 31→36 + stories += h4/h9 (36).
C) qa-parish.ts: odstrani zastarelo 'skeni izven 27–35' pogojnico (P245-KOREKCIJA: 26–35 je pravilna!).
D) stari verifierji p200–p258: živi števci → 2069, 01738 → 57, QA-total → 254,
   h42/h50/h51/h53-story pričakovanja → živo, six-lista 31→36, TOTALS-36/32/8/41, bloki-1833-P259, anomalie-25."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = []

# ============ A) pt-luknja-18-final.json ============
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
        gh["p260Note"] = f"P260-integracija: živo-{b}-blokov (01738-blok-P259/P260!-firstYear→{fy}-DVIG!)"
note = d["corpus"].get("housesNote", "")
if "P260:" not in note:
    d["corpus"]["housesNote"] = note + " | P260: +4-bloki-1835/36-01738 (01738 53→57, vitals 2065→2069!-h4-DVIG-39-NOV-ABSOLUTNI-REKORD-ČEZ-VSE-POROČNE-KNJIGE + SIBLING-SWAP-h9×h63-1.-TA-VRSTA-V-01738 + h4/h9-ŠEST-KNJIŽNI-5→6 + bothEra-poročna 39→41!)"
d["generatedAt"] = "2026-11-12 (P260-posodobitev)"
json.dump(d, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
log.append("A) pt-luknja-18-final.json: vitalsTotal=2069 + 01738=57 + 04455=269 + gapHouses-h42/h51/h53-živo + housesNote-P260")

# ============ B) parish-house-stories.json (dokaz) ============
DS = f"{ROOT}/research/issue17/parish-house-stories.json"
ev = json.load(open(DS, encoding="utf-8"))
n_six_before = len(ev["sixBookHouses"]["stories"])
ev["structure"]["tiers"]["six"] = 36
ev["structure"]["tiers"]["five"] = 32
if "tiersList" in ev["structure"] and isinstance(ev["structure"]["tiersList"], list):
    for t in ev["structure"]["tiersList"]:
        if t.get("books") == 6:
            t["houses"] = 36
        if t.get("books") == 5:
            t["houses"] = 32
story_h4 = {"si": "★★★★★ P260-hiša-NOV-ABSOLUTNI-REKORD-DVIGA: m14-1835-nevesta-Hellena-KRAUG-32-l-GRIBLJE-4-×-Johann-TOLLER-'Gnarfstuß-1' = h4-1.-01738-BLOK — POROČNA-firstYear-1874→1835-DVIG-ZA-39-LET = NOV-ABSOLUTNI-REKORD (prej-h43-34-P250!) — ŠEST-KNJIŽNA-5→6!",
            "en": "★★★★★ THE-P260-HOUSE-THE-NEW-ABSOLUTE-LIFT-RECORD: the m14-1835 bride Hellena KRAUG (GRIBLJE 4) × Johann TOLLER = the-h4-01738-FIRST-BLOCK — the-MARRIAGE-firstYear-1874→1835-LIFT-BY-39 = THE-NEW-ABSOLUTE-RECORD (the-previous-h43-34-P250!) — SIX-BOOK-5→6!"}
story_h9 = {"si": "★★★★★ P260-hiša-SIBLING-SWAP: m6-1836-ženin-Peter-ZAHOFZHIG-19-l-GRIBLJE-9-×-Maria-KRIŽAN-h63 + m7-sestra-Anna-ZAHOFZHIG-h9-NEVESTA-×-Matthias-KRIŽAN-h63 — ISTI-DAN-ISTI-PRIČI = 1.-TA-VRSTA-V-01738 (vzorec-MOH×BRODARIČ-1877-P247!) — h9-korpus-firstYear-1862→1836-DVIG-26 — ŠEST-KNJIŽNA-5→6!",
            "en": "★★★★★ THE-P260-HOUSE-THE-SIBLING-SWAP: the m6-1836 groom Peter ZAHOFZHIG (GRIBLJE 9) × Maria KRIŽAN-h63 + the m7-sister Anna ZAHOFZHIG × Matthias KRIŽAN-h63 — THE-SAME-DAY-THE-SAME-WITNESSES = the-1st-OF-THIS-KIND-IN-01738! — the-corpus-firstYear-1862→1836-LIFT-26 — SIX-BOOK-5→6!"}
stories = ev["sixBookHouses"]["stories"]
if "4" not in stories:
    stories["4"] = story_h4
if "9" not in stories:
    stories["9"] = story_h9
ev["sixBookHouses"]["count"] = len(stories)
# posodobi tudi h6/h63/h4/h9 bloke v houses-tabeli, če so
for h in ev.get("houses", []):
    if str(h.get("houseNo")) == "6":
        h["blocks"] = 37
    if str(h.get("houseNo")) == "63":
        h["blocks"] = 30
    if str(h.get("houseNo")) == "4":
        h["blocks"] = 8
    if str(h.get("houseNo")) == "9":
        h["blocks"] = 24
json.dump(ev, open(DS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
log.append(f"B) parish-house-stories.json: tiers.six-36 + stories {n_six_before}→{len(stories)} (+h4/h9!)")

# ============ C) qa-parish.ts: odstrani zastarelo 27–35 pogojnico ============
QA = f"{ROOT}/src/lib/qa-parish.ts"
s = open(QA, encoding="utf-8").read()
old_qa = '''if (p80MarrAnchors.some((h) => h.year === 1879 && ((h.scan ?? 0) < 27 || (h.scan ?? 0) > 35)))
  p80Errors.push(`poročna sidra 1879: skeni izven 27–35 (P244: s27–s35!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1879).map((h) => h.scan).join(",")})`);
'''
if old_qa in s:
    s = s.replace(old_qa, "")
    log.append("C) qa-parish.ts: zastarela 'skeni izven 27–35' pogojnica ODSTRANJENA (P245-KOREKCIJA: 26–35 pravilna!)")
else:
    log.append("C) qa-parish.ts: 27–35 pogojnica že ni prisotna")
open(QA, "w", encoding="utf-8").write(s)

# ============ D) stari verifierji ============
SIX36 = '["1", "2", "3", "4", "5", "6", "8", "9", "10", "11", "12", "16", "18", "19", "20", "22", "24", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "53", "56", "60", "61", "62", "63", "65", "73"]'
SIX31 = '["1", "2", "3", "5", "6", "8", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "56", "61", "62", "63", "65", "73"]'

def bump(path, pairs, regexes=()):
    src = open(path, encoding="utf-8").read()
    n0 = len(src)
    cnt = 0
    for a, b in pairs:
        if a in src:
            cnt += src.count(a)
            src = src.replace(a, b)
    for pat, rep in regexes:
        src, k = re.subn(pat, rep, src)
        cnt += k
    open(path, "w", encoding="utf-8").write(src)
    if cnt:
        log.append(f"D) {path.split('/')[-1]}: {cnt} zamenjav (delta {len(src)-n0})")

# — D1: splošni živi števci + pt-luknja + QA-total (vse p2xx-verifier datoteke) —
import glob
for path in sorted(glob.glob(f"{ROOT}/scripts/p2[0-5]*.py")):
    if "oldverifier_update" in path or "bump" in path or "_fix" in path or "_restore" in path or "_docs" in path or "_insert" in path or "crops" in path or "gen" in path:
        continue
    if "p260_notranjost" in path:
        continue
    pairs = [
        ('qa.count("HOUSE_VITALS.length !== 2059")', 'qa.count("HOUSE_VITALS.length !== 2069")'),
        ('qa.count("HOUSE_VITALS.length !== 2043")', 'qa.count("HOUSE_VITALS.length !== 2069")'),
        ('qa.count("HOUSE_VITALS.length !== 2012")', 'qa.count("HOUSE_VITALS.length !== 2069")'),
        ('qa.count("2012")', 'qa.count("2069")'),
        ('qa.count("2043")', 'qa.count("2069")'),
        ('qa.count("2059")', 'qa.count("2069")'),
        ('qa.count("2023")', 'qa.count("2069")'),
        ("pt.get(\"vitalsTotal\") == 2059", 'pt.get("vitalsTotal") == 2069'),
        ("pt.get(\"vitalsTotal\") == 2043", 'pt.get("vitalsTotal") == 2069'),
        ("pt.get(\"vitalsTotal\") == 2026", 'pt.get("vitalsTotal") == 2069'),
        ("pt.get(\"vitalsTotal\") == 2023", 'pt.get("vitalsTotal") == 2069'),
        ("pt.get(\"vitalsTotal\") == 2012", 'pt.get("vitalsTotal") == 2069'),
        ("pt.get(\"vitalsTotal\") == 2008", 'pt.get("vitalsTotal") == 2069'),
        ("pt2.get(\"vitalsTotal\") == 2059", 'pt2.get("vitalsTotal") == 2069'),
        ('\'"vitalsTotal": 2059\' in pt', '\'"vitalsTotal": 2069\' in pt'),
        ('\'"vitalsTotal": 2043\' in pt', '\'"vitalsTotal": 2069\' in pt'),
        ('\'"vitalsTotal": 2023\' in pt', '\'"vitalsTotal": 2069\' in pt'),
        ('\'"vitalsTotal": 2008\' in pt', '\'"vitalsTotal": 2069\' in pt'),
        ('\'"vitalsTotal": 2012\' in pt', '\'"vitalsTotal": 2069\' in pt'),
        ('.get("04455") == 265', '.get("04455") == 269'),
        ('\'"04455": 265\' in pt', '\'"04455": 269\' in pt'),
        ('.get("01738") == 47', '.get("01738") == 57'),
        ('.get("01738") == 53', '.get("01738") == 57'),
        ('.get("01738") == 31', '.get("01738") == 57'),
        ('\'"01738": 47\' in pt', '\'"01738": 57\' in pt'),
        ('\'"01738": 53\' in pt', '\'"01738": 57\' in pt'),
        ('\'"01738": 31\' in pt', '\'"01738": 57\' in pt'),
        ('.get("04106") == 338', '.get("04106") == 433'),
        ('qaResp.get("passed") == 252', 'qaResp.get("passed") == 254'),
        ('qaResp.get("passed") == 253', 'qaResp.get("passed") == 254'),
        ('qaResp.get("passed") == 246', 'qaResp.get("passed") == 254'),
        ('qaResp.get("passed") == 245', 'qaResp.get("passed") == 254'),
        ('qaResp.get("passed") == 244', 'qaResp.get("passed") == 254'),
    ]
    regexes = [
        (r'HOUSE_VITALS\.length !== 20(08|12|23|26|32|43|59|65)" not in src', 'HOUSE_VITALS.length !== 2069" not in src'),
        (r'"HOUSE_VITALS\.length !== 20(08|12|23|26|32|43|59|65)" in qa', '"HOUSE_VITALS.length !== 2069" in qa'),
        (r'== 20(08|12|23|26|32|43|59|65) \+ 01738 == 4[0-9]', '== 2069 + 01738 == 57'),
    ]
    bump(path, pairs, regexes)

# — D2: p253 — I3 živi korpus —
bump(f"{ROOT}/scripts/p253_predhodnik_01738.py", [
    ('check("I3 vitals == 2059 + 01738 == 47 (P258: +16-1831k/32/33!)", "HOUSE_VITALS.length !== 2059" not in src and len(vseh) == 47 and skupaj == 2059, f"01738={len(vseh)} skupaj={skupaj}")',
     'check("I3 vitals == 2069 + 01738 == 57 (P259: +6 + P260: +4-bloki-1835/36!)", "HOUSE_VITALS.length !== 2069" not in src and len(vseh) == 57 and skupaj == 2069, f"01738={len(vseh)} skupaj={skupaj}")'),
    ('"HOUSE_VITALS.length !== 2059" not in src', '"HOUSE_VITALS.length !== 2069" not in src'),
])

# — D3: p243 — I8b h53 živo —
bump(f"{ROOT}/scripts/p243_parish_marriage_1880_04455.py", [
    ('check("I8b h53-posodobljen (22-blokov/04455=4/firstYear=1880/p243Note!)",\n      h53["blocksTotal"] == 22 and h53["byBook"]["04455"] == 4 and h53["firstYear"] == 1880 and "p243Note" in h53)',
     'check("I8b h53-posodobljen (34-blokov/04455=4/firstYear=1833-P259-DVIG!-p243Note!)",\n      h53["blocksTotal"] == 34 and h53["byBook"]["04455"] == 4 and h53["firstYear"] == 1833 and "p243Note" in h53)'),
])

# — D4: p244 — I11c anomalie 21→25 —
bump(f"{ROOT}/scripts/p244_parish_marriage_1879_04455.py", [
    ('len(d["anomalie"]) == 21', 'len(d["anomalie"]) == 25'),
    ('anomalie-KOREKCIJA-vnosi (21-vnosov!', 'anomalie-KOREKCIJA-vnosi (25-vnosov!-P245: +4!'),
])

# — D5: p247 — I8b h51/h53 živo —
bump(f"{ROOT}/scripts/p247_parish_marriage_1877_04455.py", [
    ('check("I8b h51-posodobljen (6-blokov/04455=2/firstYear=1877/p247Note!) + h53-intakten (22/4!)",\n      h51["blocksTotal"] == 6 and h51["byBook"]["04455"] == 2 and h51["firstYear"] == 1877 and "p247Note" in h51\n      and h53["blocksTotal"] == 22 and h53["byBook"]["04455"] == 4)',
     'check("I8b h51-posodobljen (12-blokov/04455=2/firstYear=1834-P259-DVIG!-p247Note!) + h53-živo (34/4-P259!)",\n      h51["blocksTotal"] == 12 and h51["byBook"]["04455"] == 2 and h51["firstYear"] == 1834 and "p247Note" in h51\n      and h53["blocksTotal"] == 34 and h53["byBook"]["04455"] == 4)'),
])

# — D6: p249 — I8b h42 živo —
bump(f"{ROOT}/scripts/p249_parish_marriage_1875_04455.py", [
    ('h42["blocksTotal"] == 16', 'h42["blocksTotal"] == 28'),
])

# — D7: p254 — I3/I3b/I4/I6/I8/I8b živo —
bump(f"{ROOT}/scripts/p254_house_stories.py", [
    ('check("I3 vsota blokov HOUSE_STORIES == 2059 (P258: +16-1831k/32/33!)", total == 2059, f"{total}")',
     'check("I3 vsota blokov HOUSE_STORIES == 2069 (P259: +6 + P260: +4!)", total == 2069, f"{total}")'),
    ('expected_books = {"01738": 47, "04104": 288, "04105": 502, "04455": 269, "04106": 433, "04894": 520}',
     'expected_books = {"01738": 57, "04104": 288, "04105": 502, "04455": 269, "04106": 433, "04894": 520}'),
    ('check("I3b bloki po knjigah 47/288/502/269/433/520 (== korpus! P258-01738-47!)"',
     'check("I3b bloki po knjigah 57/288/502/269/433/520 (== korpus! P260-01738-57!)'),
    (SIX31, SIX36),
    ('check("I4 HOUSE_STORY_SIX == [1,3,5,6,10,11,12,16,18,19,20,22,26,27,28,32,33,56,61,62,63,65,73] (P258-31!)"',
     'check("I4 HOUSE_STORY_SIX == 36-šest-knjižnih (P258-31 → P259-34 → P260-36!)"'),
    ('ev["structure"]["tiers"]["six"] == 31\n      and len(ev["sixBookHouses"]["stories"]) == 31',
     'ev["structure"]["tiers"]["six"] == 36\n      and len(ev["sixBookHouses"]["stories"]) == 36'),
    ('check("I6 dokaz parish-house-stories.json (100 hiš v tabeli + tierji + 31-zgodb — P258!)"',
     'check("I6 dokaz parish-house-stories.json (100 hiš v tabeli + tierji + 36-zgodb — P260!)"'),
    ('h24 and int(h24.group(1)) == 45', 'h24 and int(h24.group(1)) == 46'),
    ('"bothEraPorocna: 34" in mod', '"bothEraPorocna: 41" in mod'),
    ('obe-eri 69/75/34', 'obe-eri 69/75/41'),
])

# — D8: p255 — I2/I6/I6b živo —
bump(f"{ROOT}/scripts/p255_notranjost_01738.py", [
    ('\'blocks: 2059,\' in stories', '\'blocks: 2069,\' in stories'),
    ('"bothEraPorocna: 34" in stories', '"bothEraPorocna: 41" in stories'),
    ('\'houseNo: "6", kind: "griblje", blocks: 36, books: 6\' in stories', '\'houseNo: "6", kind: "griblje", blocks: 37, books: 6\' in stories'),
    ('ev["structure"]["tiers"]["six"] == 31', 'ev["structure"]["tiers"]["six"] == 36'),
    ('len(ev["sixBookHouses"]["stories"]) == 31', 'len(ev["sixBookHouses"]["stories"]) == 36'),
])

# — D9: p256 — I6/I6d/I7 živo —
bump(f"{ROOT}/scripts/p256_1829.py", [
    ('\'blocks: 2059,\' in stories', '\'blocks: 2069,\' in stories'),
    ('"bothEraPorocna: 34" in stories and "sixBook: 23" in stories', '"bothEraPorocna: 41" in stories and "sixBook: 36" in stories'),
    ('"fiveBook: 41" in stories', '"fiveBook: 32" in stories'),
    ('pt["structure"]["tiers"]["six"] == 23\n      and len(pt["sixBookHouses"]["stories"]) == 23',
     'pt["structure"]["tiers"]["six"] == 36\n      and len(pt["sixBookHouses"]["stories"]) == 36'),
    ('"HOUSE_VITALS.length !== 2043" in qa', '"HOUSE_VITALS.length !== 2069" in qa'),
])

# — D10: p257 — I6/I6b/I6d/I7 živo —
bump(f"{ROOT}/scripts/p257_1830_1831.py", [
    ('\'blocks: 2059,\' in stories', '\'blocks: 2069,\' in stories'),
    ('"bothEraPorocna: 34" in stories and "sixBook: 23" in stories', '"bothEraPorocna: 41" in stories and "sixBook: 36" in stories'),
    ('"fiveBook: 41" in stories', '"fiveBook: 32" in stories'),
    ('houseNo: "50", kind: "griblje", blocks: 12, books: 5', 'houseNo: "50", kind: "griblje", blocks: 13, books: 6'),
    ('check("I6b h50-story: 13-blokov-1831–1924-span-93 (3.-mesto!)")' , 'check("I6b h50-story: 13-blokov-1831–1924-span-93 (3.-mesto!)")'),
    ('pt["structure"]["tiers"]["six"] == 23\n      and len(pt["sixBookHouses"]["stories"]) == 23',
     'pt["structure"]["tiers"]["six"] == 36\n      and len(pt["sixBookHouses"]["stories"]) == 36'),
    ('"HOUSE_VITALS.length !== 2043" in qa', '"HOUSE_VITALS.length !== 2069" in qa'),
])

# — D11: p258 — I1c/I2/I8 živo —
bump(f"{ROOT}/scripts/p258_meja_1831_32_33.py", [
    ('check("I1c bloki-01738/1833 == [50,49] (m6-PESDIRZ×HIMIZ — POLNI-DVOJNI!)",\n      bloki1833 == ["50", "49"], ",".join(bloki1833))',
     'check("I1c bloki-01738/1833 == [50,49,53,24,60,28] (P258-m6-PESDIRZ×HIMIZ!-+ P259-m8/m24/m25/m12!)",\n      bloki1833 == ["50", "49", "53", "24", "60", "28"], ",".join(bloki1833))'),
    ('check("I2 vitals == 2059 + 01738 == 47 + leta == 1828–1833+1873",\n      "HOUSE_VITALS.length !== 2059" not in src and len(vseh) == 47 and skupaj == 2059\n      and leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1873],',
     'check("I2 vitals == 2069 + 01738 == 57 + leta == 1828–1836+1873",\n      "HOUSE_VITALS.length !== 2069" not in src and len(vseh) == 57 and skupaj == 2069\n      and leta1738 == [1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1873],'),
    ('check("I8 HOUSE_STORY_SIX == 31 (+8: h2/h8/h35/h36/h42/h46/h47/h48) + TOTALS-2059",\n      "sixBook: 31" in stories and "fiveBook: 35" in stories and "fourBook: 10" in stories\n      and "blocks: 2059" in stories and "bothEraPorocna: 34" in stories',
     'check("I8 HOUSE_STORY_SIX == 36 (+5: h24/h53/h60-P259 + h4/h9-P260!) + TOTALS-2069",\n      "sixBook: 36" in stories and "fiveBook: 32" in stories and "fourBook: 8" in stories\n      and "blocks: 2069" in stories and "bothEraPorocna: 41" in stories'),
    ('"HOUSE_VITALS.length !== 2059" not in src', '"HOUSE_VITALS.length !== 2069" not in src'),
])

# — D12: 200-serija (p200–p235) + p236–p242 — pt-luknja vitalsTotal v besedilih —
for path in sorted(glob.glob(f"{ROOT}/scripts/p2[0-3]*.py")) + [f"{ROOT}/scripts/p238_parish_marriage_1885_04455.py", f"{ROOT}/scripts/p239_parish_marriage_1884_04455.py", f"{ROOT}/scripts/p240_parish_marriage_1883_04455.py", f"{ROOT}/scripts/p241_parish_marriage_1882_04455.py", f"{ROOT}/scripts/p242_parish_marriage_1881_04455.py"]:
    if "oldverifier_update" in path or "bump" in path or "_fix" in path or "_restore" in path or "_docs" in path or "crops" in path:
        continue
    bump(path, [
        ('\'"vitalsTotal": 2059\' in pt', '\'"vitalsTotal": 2069\' in pt'),
        ('\'"vitalsTotal": 2043\' in pt', '\'"vitalsTotal": 2069\' in pt'),
    ])

print("\n".join(log))
print(f"\n=== P260-oldverifier-update: {len(log)} korakov ===")
