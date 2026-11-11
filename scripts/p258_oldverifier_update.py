#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — kaskadna posodobitev starih preverjevalnikov (po vzoru P257: 2032→2043 → zdaj 2043→2059).
1) qa-parish.ts: HOUSE_VITALS.length → 2059 (vse žive kontrole) + byBook-01738-živo 31→47 (p253/p255/p256/p257)
   + SIX-lista 23→31 (×2) + tiers 23→31 + bothEra-poročna 26→34 (×2) + p94-izjemi h22-1832 + h49-1833.
2) pt-luknja-18-final.json: 2043→2059, 01738 31→47, housesNote + P258."""
import json
import re

QA = "src/lib/qa-parish.ts"
PT = "research/issue17/pt-luknja-18-final.json"

s = open(QA, encoding="utf-8").read()
n0 = len(s)

# ——— 1) HOUSE_VITALS.length !== N → 2059 (vse žive; P253-snapshot konstante v modulu se NE dotikajo) ———
def sub_len(m):
    n = int(m.group(1))
    if n == 2059:
        return m.group(0)
    return "HOUSE_VITALS.length !== 2059"
s, c1 = re.subn(r"HOUSE_VITALS\.length !== (\d{3,4})", sub_len, s)

# ——— 2) sporočila z živimi števci 2043 → 2059 ———
for a, b in [
    ("vsota-blokov ≠ 2043 (modul-vsota ${p254Sum} / TOTALS ${HOUSE_STORY_TOTALS.blocks} / HOUSE_VITALS ${HOUSE_VITALS.length})",
     "vsota-blokov ≠ 2059 (modul-vsota ${p254Sum} / TOTALS ${HOUSE_STORY_TOTALS.blocks} / HOUSE_VITALS ${HOUSE_VITALS.length})"),
    ("p254Sum !== 2043 || HOUSE_STORY_TOTALS.blocks !== 2043 || HOUSE_VITALS.length !== 2043",
     "p254Sum !== 2059 || HOUSE_STORY_TOTALS.blocks !== 2059 || HOUSE_VITALS.length !== 2059"),
    ("P253-snapshot-2023/živo-2043 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257!)",
     "P253-snapshot-2023/živo-2059 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257 + 16-P258!)"),
]:
    s = s.replace(a, b)

# ——— 3) SIX-lista ×2 (23 → 31: +h2/h8/h35/h36/h42/h46/h47/h48) ———
OLD23 = '["1", "3", "5", "6", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "56", "61", "62", "63", "65", "73"]'
NEW31 = '["1", "2", "3", "5", "6", "8", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "56", "61", "62", "63", "65", "73"]'
c_six = s.count(OLD23)
s = s.replace(OLD23, NEW31)
s = s.replace("šest-knjižne-živo ≠ [1,3,5,6,10,11,12,16,18,19,20,22,26,27,28,32,33,56,61,62,63,65,73]",
              "šest-knjižne-živo ≠ [1,2,3,5,6,8,10,11,12,16,18,19,20,22,26,27,28,32,33,35,36,42,46,47,48,56,61,62,63,65,73] (P258: +8!)")
s = s.replace("HOUSE_STORY_SIX ≠ [1,3,5,6,10,11,12,16,18,19,20,22,26,27,28,32,33,56,61,62,63,65,73]",
              "HOUSE_STORY_SIX ≠ [1,2,3,5,6,8,10,11,12,16,18,19,20,22,26,27,28,32,33,35,36,42,46,47,48,56,61,62,63,65,73] (P258: +8!)")

# ——— 4) tiers 23→31 (p254 živa tier-kontrola) ———
s = s.replace("if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== 23 || HOUSE_STORY_TIERS[0]?.books !== 6)",
              "if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== 31 || HOUSE_STORY_TIERS[0]?.books !== 6)")

# ——— 5) bothEra-poročna 26 → 34 (p254 + p256) ———
s = s.replace("if (HOUSE_STORY_TOTALS.bothEraKrstna !== 69 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== 26)",
              "if (HOUSE_STORY_TOTALS.bothEraKrstna !== 69 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== 34)")
s = s.replace('p254Errors.push("obe-eri-pokritje ≠ 69/75/26 (krstna/mrliška/poročna!)");',
              'p254Errors.push("obe-eri-pokritje ≠ 69/75/34 (krstna/mrliška/poročna!-P258: +8!)");')
s = s.replace('if (HOUSE_STORY_TOTALS.bothEraPorocna !== 26) p256Errors.push("bothEra-poročna ≠ 26 (P257!)");',
              'if (HOUSE_STORY_TOTALS.bothEraPorocna !== 34) p256Errors.push("bothEra-poročna ≠ 34 (P258: +8 — h47/h46/h8/h48/h2/h35/h36/h42!)");')

# ——— 6) byBook-01738-živo 31 → 47 (p253/p255/p256/p257) ———
s = s.replace("if (by01738.length !== 31 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)",
              "if (by01738.length !== 47 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)")
s = s.replace("byBook-01738 ≠ 31-živo/11-P253-snapshot (${by01738.length} — P257: +11-blokov-1830/31!)",
              "byBook-01738 ≠ 47-živo/11-P253-snapshot (${by01738.length} — P257: +11 + P258: +16-blokov-1831k/32/33!)")
s = s.replace("if (p255ByBook01738 !== 31) p255Errors.push(`bloki-01738 ≠ 31 (${p255ByBook01738} — P257: +11-1830/31!)`);",
              "if (p255ByBook01738 !== 47) p255Errors.push(`bloki-01738 ≠ 47 (${p255ByBook01738} — P257: +11 + P258: +16-1831k/32/33!)`);")
s = s.replace("if (p256ByBook01738 !== 31) p256Errors.push(`bloki-01738 ≠ 31 (${p256ByBook01738})`);",
              "if (p256ByBook01738 !== 47) p256Errors.push(`bloki-01738 ≠ 47 (${p256ByBook01738} — P258: +16!)`);")
s = s.replace("if (p257ByBook01738 !== 31) p257Errors.push(`bloki-01738 ≠ 31 (${p257ByBook01738})`);",
              "if (p257ByBook01738 !== 47) p257Errors.push(`bloki-01738 ≠ 47 (${p257ByBook01738} — P258: +16!)`);")

# ——— 7) p94-izjemi: h22-1832 + h49-1833 (P258-notranjost!) ———
old94 = '&& !(v.bookSignature === "01738" && v.year === 1830 && hn === "22"))) // P257: + poročna 01738-1830 h22 (m4-Anna-MILEK-nevesta — 3.-ZAPOREDNO-LETO-1828+1829+1830!)'
new94 = ('&& !(v.bookSignature === "01738" && v.year === 1830 && hn === "22") '
         '&& !(v.bookSignature === "01738" && v.year === 1832 && hn === "22") '
         '&& !(v.bookSignature === "01738" && v.year === 1833 && hn === "49")'
         ')) // P258: + poročna 01738-1832 h22 (m8-ŽENIN-Johann-MILEK-oče-Johann!-MILEK-DOMNEVA-POTRJENA-4.-blok-v-5-letih!) + 01738-1833 h49 (m6-NEVESTA-Maria-[~Himiz]-×-Johann-PESDIRZ-h50!-h49-BREZ-04455-poročna-vrzela!) // P257: + poročna 01738-1830 h22 (m4-Anna-MILEK-nevesta — 3.-ZAPOREDNO-LETO-1828+1829+1830!)')
c94 = s.count(old94)
s = s.replace(old94, new94)

open(QA, "w", encoding="utf-8").write(s)
print(f"qa-parish.ts: {c1} HOUSE_VITALS-kontrol → 2059; SIX-{c_six}×; tiers-31; bothEra-34; byBook-47×4; p94-izjemi-{c94}×; delta={len(s)-n0} znakov")

# ——— 8) pt-luknja-18-final.json ———
d = json.load(open(PT, encoding="utf-8"))
d["corpus"]["vitalsTotal"] = 2059
d["corpus"]["byBook"]["01738"] = 47
if "vitalsTotal" in d:
    d["vitalsTotal"] = 2059
hn = d["corpus"].get("housesNote", "")
if "P258" not in hn:
    d["corpus"]["housesNote"] = hn + " | P258: +16-blokov-1831-konec/1832/1833-01738 (5×1831: h47/h46/h8/h48/h2 + 2×1832-s9: h22/h35 + 7×1832-s10: h2/h42/h36/h35/h66/h56/h61 + 2×1833: h50/h49!) — vitals 2043→2059, 01738 31→47, šest-knjižne 23→31, bothEra 26→34!"
json.dump(d, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pt-luknja-18-final.json: 2059/47 + housesNote-P258")
