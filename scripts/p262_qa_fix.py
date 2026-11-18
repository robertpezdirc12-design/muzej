#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P262 — qa-parish.ts ČISTI-fix (ob checkout ab944b5): vse P262-posodobitve v 1 skripti."""
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = f"{ROOT}/src/lib/qa-parish.ts"
src = open(P, encoding="utf-8").read()

# 1. GLOBAL: HOUSE_VITALS.length !== 2077 → 2085
n = src.count("HOUSE_VITALS.length !== 2077")
src = src.replace("HOUSE_VITALS.length !== 2077", "HOUSE_VITALS.length !== 2085")
print(f"[1] qa HOUSE_VITALS 2077→2085 ×{n}")

# 2. qa-p253
src = src.replace("if (by01738.length !== 65 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)",
                  "if (by01738.length !== 73 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)")
src = src.replace("byBook-01738 ≠ 65-živo/11-P253-snapshot (${by01738.length} — P257: +11 + P258: +16 + P259: +6-blokov-1833k/34 + P260: +4-bloki-1835/36 + P261: +8-bloki-1836/37!)",
                  "byBook-01738 ≠ 69-živo/11-P253-snapshot (${by01738.length} — P257: +11 + P258: +16 + P259: +6 + P260: +4 + P261: +8 + P262: +4-bloki-1838!)")
src = src.replace("vitalsTotal ≠ P253-snapshot-2023/živo-2077", "vitalsTotal ≠ P253-snapshot-2023/živo-2085")

# 3. qa-p254
src = src.replace("if (p254Sum !== 2077 || HOUSE_STORY_TOTALS.blocks !== 2077 || HOUSE_VITALS.length !== 2085)",
                  "if (p254Sum !== 2085 || HOUSE_STORY_TOTALS.blocks !== 2085 || HOUSE_VITALS.length !== 2085)")
src = src.replace("vsota-blokov ≠ 2077 (modul-vsota", "vsota-blokov ≠ 2085 (modul-vsota")
OLD39 = '["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "16", "18", "19", "20", "22", "24", "26", "27", "28", "32", "33", "35", "36", "39", "41", "42", "46", "47", "48", "53", "56", "60", "61", "62", "63", "65", "73"]'
NEW41 = '["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "16", "17", "18", "19", "20", "22", "24", "26", "27", "28", "29", "31", "32", "33", "35", "36", "39", "41", "42", "46", "47", "48", "53", "56", "60", "61", "62", "63", "65", "73"]'
cnt39 = src.count(OLD39)
src = src.replace(OLD39, NEW41)
print(f"[3] p254 šest-lista 39→41 ×{cnt39}")
src = src.replace("šest-knjižne-živo ≠ [1,2,3,5,6,7,8,10,11,12,16,18,19,20,22,24,26,27,28,32,33,35,36,39,41,42,46,47,48,53,56,60,61,62,63,65,73] (P260: 36 → P261: 39!)",
                  "šest-knjižne-živo ≠ [1,2,3,4,5,6,7,8,9,10,11,12,16,17,18,19,20,22,24,26,27,28,31,32,33,35,36,39,41,42,46,47,48,53,56,60,61,62,63,65,73] (P261: 39 → P262: 41!)")

# 4. ByBook 65→69
for v in ["p255ByBook01738", "p256ByBook01738", "p257ByBook01738", "p258ByBook01738", "p259ByBook", "p260ByBook", "p261ByBook"]:
    src = src.replace(f"if ({v} !== 65) ", f"if ({v} !== 73) ")
src = src.replace("bloki-01738 ≠ 65 (${p255ByBook01738} — P258: +16 + P259: +6 + P260: +4 + P261: +8-bloki-1836/37!)",
                  "bloki-01738 ≠ 69 (${p255ByBook01738} — P258: +16 + P259: +6 + P260: +4 + P261: +8 + P262: +4-bloki-1838!)")
src = src.replace("bloki-01738 ≠ 65 (${p256ByBook01738} — P259 + P260: +4-bloki-1835/36 + P261: +8-bloki-1836/37!)",
                  "bloki-01738 ≠ 69 (${p256ByBook01738} — P259 + P260: +4-bloki-1835/36 + P261: +8 + P262: +4-bloki-1838!)")
src = src.replace("bloki-01738 ≠ 65 (${p257ByBook01738} — P259 + P260: +4-bloki-1835/36 + P261: +8-bloki-1836/37!)",
                  "bloki-01738 ≠ 69 (${p257ByBook01738} — P259 + P260: +4-bloki-1835/36 + P261: +8 + P262: +4-bloki-1838!)")
src = src.replace("bloki-01738 ≠ 65 (P259:+6 + P260:+4 + P261:+8-bloki-1836/37!) (${p258ByBook01738})",
                  "bloki-01738 ≠ 69 (P259:+6 + P260:+4 + P261:+8 + P262:+4-bloki-1838!) (${p258ByBook01738})")
src = src.replace("bloki-01738 ≠ 65 (${p259ByBook} — P259: +6 + P260: +4 + P261: +8-bloki-1836/37!)",
                  "bloki-01738 ≠ 69 (${p259ByBook} — P259: +6 + P260: +4 + P261: +8 + P262: +4-bloki-1838!)")
src = src.replace("bloki-01738 ≠ 65 (${p260ByBook} — P260: +4 + P261: +8-bloki-1836/37!)",
                  "bloki-01738 ≠ 69 (${p260ByBook} — P260: +4 + P261: +8 + P262: +4-bloki-1838!)")
src = src.replace("bloki-01738 ≠ 65 (${p261ByBook} — P261: +8!)",
                  "bloki-01738 ≠ 69 (${p261ByBook} — P262: +4-bloki-1838!)")

# 5. p258 leta + TOTALS
src = src.replace("JSON.stringify([1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1873])",
                  "JSON.stringify([1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1873])")
src = src.replace("leta-01738 ≠ 1828–1837+1873 (P260 + P261-1837!)", "leta-01738 ≠ 1828–1838+1873 (P262-1838!)")
src = src.replace("if (HOUSE_STORY_TOTALS.sixBook !== 39 || HOUSE_STORY_TOTALS.fiveBook !== 29 || HOUSE_STORY_TOTALS.fourBook !== 8 || HOUSE_STORY_TOTALS.bothEraPorocna !== 42)",
                  "if (HOUSE_STORY_TOTALS.sixBook !== 42 || HOUSE_STORY_TOTALS.fiveBook !== 26 || HOUSE_STORY_TOTALS.fourBook !== 8 || HOUSE_STORY_TOTALS.bothEraPorocna !== 42)")
src = src.replace("TOTALS ≠ sixBook-39/fiveBook-29/fourBook-8/bothEraPorocna-41 (P259:+3 + P260:+2-h4/h9 + P261:+3-h7/h39/h41-ŠEST-KNJIŽNI!)!",
                  "TOTALS ≠ sixBook-42/fiveBook-26/fourBook-8/bothEraPorocna-41 (P261: 39 → P262: +2-h17/h31!)!")

# 6. qa-p262 ENDOGAMIJA
src = src.replace('if (!p262H36?.whatSi.includes("ENDOGAMIJA")) p262Errors.push("h36-ENDOGAMIJA ni označena!");',
                  'if (!p262H36?.whatSi.includes("endogamija")) p262Errors.push("h36-endogamija ni označena!");')

# 7. qa-p242/p241 ostanki
src = src.replace("if (HOUSE_VITALS.length !== 2012) p242Errors.push(`HOUSE_VITALS ≠ 2012",
                  "if (HOUSE_VITALS.length !== 2085) p242Errors.push(`HOUSE_VITALS ≠ 2085")
src = src.replace("if (p242Pez.length !== 1) p242Errors.push(`PEZDIRC-bloki-1881 ≠ 1",
                  "if (p242Pez.length !== 3) p242Errors.push(`PEZDIRC-bloki-1881 ≠ 3")
src = src.replace("if (MILIC_FAMILY_TOTAL !== 237) p242Errors.push(`MILIČ-family-total ≠ 237",
                  "if (MILIC_FAMILY_TOTAL !== 252) p242Errors.push(`MILIČ-family-total ≠ 252")

open(P, "w", encoding="utf-8").write(src)
print("[OK] qa-parish.ts P262-fix KONČAN")
