#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — kaskadna posodobitev starih preverjevalnikov (po vzoru P258: 2043→2059 → zdaj 2059→N).
CONFIG-DRIVEN: bere scripts/tmp/p259-config.json (zapiše ga integracijski korak!):
  {"total": N, "byBook01738": M, "sixList": ["1","2",...], "bothEraPorocna": B,
   "p94exceptions": [{"year": 1833, "house": "24", "note": "..."}], "housesNote": "..."}
1) qa-parish.ts: HOUSE_VITALS.length → N + sporočila 2059→N + SIX-lista 31→S (×2) + tiers 31→S
   + bothEra-poročna 34→B (×2) + byBook-01738-živo 47→M (×4) + p94-izjemi-P259.
2) pt-luknja-18-final.json: 2059→N, 01738 47→M, housesNote + P259."""
import json
import re
import sys
import os

QA = "src/lib/qa-parish.ts"
PT = "research/issue17/pt-luknja-18-final.json"
CFG = "scripts/tmp/p259-config.json"

if not os.path.exists(CFG):
    print(f"MANJKA {CFG}! Zapiši ga po integraciji (total/byBook01738/sixList/bothEraPorocna/p94exceptions/housesNote) in ponovno zaženi.")
    sys.exit(2)
cfg = json.load(open(CFG, encoding="utf-8"))
N = cfg["total"]; M = cfg["byBook01738"]; B = cfg["bothEraPorocna"]
SIX = cfg["sixList"]; P94 = cfg.get("p94exceptions", [])
assert isinstance(SIX, list) and all(isinstance(x, str) for x in SIX), "sixList = niz-bloklist!"

s = open(QA, encoding="utf-8").read()
n0 = len(s)

# ——— 1) HOUSE_VITALS.length !== N (vse žive kontrole) ———
def sub_len(m):
    return f"HOUSE_VITALS.length !== {N}"
s, c1 = re.subn(r"HOUSE_VITALS\.length !== \d{3,4}", sub_len, s)

# ——— 2) sporočila z živimi števci 2059 → N ———
for a, b in [
    (f"vsota-blokov ≠ 2059 (modul-vsota ${{p254Sum}} / TOTALS ${{HOUSE_STORY_TOTALS.blocks}} / HOUSE_VITALS ${{HOUSE_VITALS.length}})",
     f"vsota-blokov ≠ {N} (modul-vsota ${{p254Sum}} / TOTALS ${{HOUSE_STORY_TOTALS.blocks}} / HOUSE_VITALS ${{HOUSE_VITALS.length}})"),
    ("p254Sum !== 2059 || HOUSE_STORY_TOTALS.blocks !== 2059 || HOUSE_VITALS.length !== 2059",
     f"p254Sum !== {N} || HOUSE_STORY_TOTALS.blocks !== {N} || HOUSE_VITALS.length !== {N}"),
    ("P253-snapshot-2023/živo-2059 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257 + 16-P258!)",
     f"P253-snapshot-2023/živo-{N} (${{PREDHODNIK_1873_KORPUS.vitalsTotal}}/${{HOUSE_VITALS.length}} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257 + 16-P258 + {N-2059}-P259!)"),
]:
    s = s.replace(a, b)

# ——— 3) SIX-lista ×2 (31 → S) ———
OLD31 = '["1", "2", "3", "5", "6", "8", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "56", "61", "62", "63", "65", "73"]'
NEW_S = json.dumps(SIX)  # ["1", "2", ...] format 1:1
c_six = s.count(OLD31)
s = s.replace(OLD31, NEW_S)
OLD_MSG = "šest-knjižne-živo ≠ [1,2,3,5,6,8,10,11,12,16,18,19,20,22,26,27,28,32,33,35,36,42,46,47,48,56,61,62,63,65,73] (P258: +8!)"
NEW_MSG = f"šest-knjižne-živo ≠ [{','.join(SIX)}] (P259: {len(SIX)}!)"
s = s.replace(OLD_MSG, NEW_MSG)
OLD_HS = "HOUSE_STORY_SIX ≠ [1,2,3,5,6,8,10,11,12,16,18,19,20,22,26,27,28,32,33,35,36,42,46,47,48,56,61,62,63,65,73] (P258: +8!)"
NEW_HS = f"HOUSE_STORY_SIX ≠ [{','.join(SIX)}] (P259: {len(SIX)}!)"
s = s.replace(OLD_HS, NEW_HS)

# ——— 4) tiers 31→S ———
s = s.replace("if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== 31 || HOUSE_STORY_TIERS[0]?.books !== 6)",
              f"if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== {len(SIX)} || HOUSE_STORY_TIERS[0]?.books !== 6)")

# ——— 5) bothEra-poročna 34 → B ———
s = s.replace("if (HOUSE_STORY_TOTALS.bothEraKrstna !== 69 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== 34)",
              f"if (HOUSE_STORY_TOTALS.bothEraKrstna !== 69 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== {B})")
s = s.replace('p254Errors.push("obe-eri-pokritje ≠ 69/75/34 (krstna/mrliška/poročna!-P258: +8!)");',
              f'p254Errors.push("obe-eri-pokritje ≠ 69/75/{B} (krstna/mrliška/poročna!-P259!)");')
s = s.replace('if (HOUSE_STORY_TOTALS.bothEraPorocna !== 34) p256Errors.push("bothEra-poročna ≠ 34 (P258: +8 — h47/h46/h8/h48/h2/h35/h36/h42!)");',
              f'if (HOUSE_STORY_TOTALS.bothEraPorocna !== {B}) p256Errors.push("bothEra-poročna ≠ {B} (P259!)");')

# ——— 6) byBook-01738-živo 47 → M (×4) ———
s = s.replace("if (by01738.length !== 47 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)",
              f"if (by01738.length !== {M} || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)")
s = s.replace("byBook-01738 ≠ 47-živo/11-P253-snapshot (${by01738.length} — P257: +11 + P258: +16-blokov-1831k/32/33!)",
              f"byBook-01738 ≠ {M}-živo/11-P253-snapshot (${{by01738.length}} — P257: +11 + P258: +16 + P259: +{M-47}-blokov-1833k/34!)")
s = s.replace("if (p255ByBook01738 !== 47) p255Errors.push(`bloki-01738 ≠ 47 (${p255ByBook01738} — P257: +11 + P258: +16-1831k/32/33!)`);",
              f"if (p255ByBook01738 !== {M}) p255Errors.push(`bloki-01738 ≠ {M} (${{p255ByBook01738}} — P258: +16 + P259: +{M-47}!)`);")
s = s.replace("if (p256ByBook01738 !== 47) p256Errors.push(`bloki-01738 ≠ 47 (${p256ByBook01738} — P258: +16!)`);",
              f"if (p256ByBook01738 !== {M}) p256Errors.push(`bloki-01738 ≠ {M} (${{p256ByBook01738}} — P259!)`);")
s = s.replace("if (p257ByBook01738 !== 47) p257Errors.push(`bloki-01738 ≠ 47 (${p257ByBook01738} — P258: +16!)`);",
              f"if (p257ByBook01738 !== {M}) p257Errors.push(`bloki-01738 ≠ {M} (${{p257ByBook01738}} — P259!)`);")

# ——— 7) p94-izjemi: + P259-bloki (vsak nov 01738-blok s STARIM letom!) ———
# zadnja P258-izjema = h49-1833; nova P259-izjeme se dodajo ZA njo (pred zaklepom ')) //')
OLD_TAIL = '''&& !(v.bookSignature === "01738" && v.year === 1833 && hn === "49")
)) // P258:'''
if P94:
    add = "\n".join(
        f'''         && !(v.bookSignature === "01738" && v.year === {e["year"]} && hn === "{e["house"]}")''' for e in P94)
    notes = " + ".join(f'01738-{e["year"]}-h{e["house"]} ({e["note"]})' for e in P94)
    NEW_TAIL = f'''&& !(v.bookSignature === "01738" && v.year === 1833 && hn === "49")\n{add}
)) // P259: + {notes}! // P258:'''
    c94 = s.count(OLD_TAIL)
    s = s.replace(OLD_TAIL, NEW_TAIL)
else:
    c94 = 0

open(QA, "w", encoding="utf-8").write(s)
print(f"qa-parish.ts: {c1} HOUSE_VITALS-kontrol → {N}; SIX-{c_six}× → {len(SIX)}; tiers-{len(SIX)}; bothEra-{B}; byBook-{M}×4; p94-izjemi-{c94}× (+{len(P94)}); delta={len(s)-n0} znakov")

# ——— 8) pt-luknja-18-final.json ———
d = json.load(open(PT, encoding="utf-8"))
d["corpus"]["vitalsTotal"] = N
d["corpus"]["byBook"]["01738"] = M
if "vitalsTotal" in d:
    d["vitalsTotal"] = N
hn = d["corpus"].get("housesNote", "")
if "P259" not in hn:
    d["corpus"]["housesNote"] = hn + " | P259: " + cfg.get("housesNote", f"+{M-47}-blokov-1833-nadaljevanje/1834-01738 — vitals 2059→{N}, 01738 47→{M}, šest-knjižne 31→{len(SIX)}, bothEra 34→{B}!")
json.dump(d, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"pt-luknja-18-final.json: {N}/{M} + housesNote-P259")
