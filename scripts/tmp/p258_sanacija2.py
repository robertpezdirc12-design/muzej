#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258-SANACIJA — ponovna izvedba VSEH mojih qa-parish.ts sprememb po checkout (nesreča-bump-skript!).
Koraki: uvoz + 157×2059 + SIX×2 + tiers + bothEra + byBook + p94 + MILIČ + p237-križ + p88 + p254 + p257 + h22 + qa-p258 + part5 + h8/h35 + pt-luknja-04455-269."""
import json
import re

QA = "src/lib/qa-parish.ts"
PT = "research/issue17/pt-luknja-18-final.json"

s = open(QA, encoding="utf-8").read()
n0 = len(s)
steps = []

# ——— 1) uvozi P258 ———
old_imp = """  PREDHODNIK_1831_NITI,
  PREDHODNIK_1831_KRAJI,
  PREDHODNIK_257_KORPUS,
} from "@/data/atlas/parish-marriage-early";"""
new_imp = """  PREDHODNIK_1831_NITI,
  PREDHODNIK_1831_KRAJI,
  PREDHODNIK_257_KORPUS,
  PREDHODNIK_1831K_BLOCKS,
  PREDHODNIK_1831K_HOUSES,
  PREDHODNIK_1831K_TOTAL,
  PREDHODNIK_1831K_BLOCKI,
  PREDHODNIK_1831K_STRUNA,
  PREDHODNIK_1832_BLOCKS,
  PREDHODNIK_1832_HOUSES,
  PREDHODNIK_1832_TOTAL,
  PREDHODNIK_1832_BLOCKI,
  PREDHODNIK_1832_STRUNA,
  PREDHODNIK_1833_BLOCKS,
  PREDHODNIK_1833_HOUSES,
  PREDHODNIK_1833_TOTAL,
  PREDHODNIK_1833_BLOCKI,
  PREDHODNIK_1833_RESTART,
  PREDHODNIK_258_NITI,
  PREDHODNIK_258_KRAJI,
  PREDHODNIK_258_KORPUS,
} from "@/data/atlas/parish-marriage-early";"""
assert old_imp in s; s = s.replace(old_imp, new_imp); steps.append("1-uvoz")

# ——— 2) HOUSE_VITALS.length → 2059 (vse žive) ———
def sub_len(m):
    n = int(m.group(1))
    return m.group(0) if n == 2059 else "HOUSE_VITALS.length !== 2059"
s, c1 = re.subn(r"HOUSE_VITALS\.length !== (\d{3,4})", sub_len, s)
steps.append(f"2-2059×{c1}")

# ——— 3) p254Sum vrstica ———
s = s.replace("if (p254Sum !== 2043 || HOUSE_STORY_TOTALS.blocks !== 2043 || HOUSE_VITALS.length !== 2043)",
              "if (p254Sum !== 2059 || HOUSE_STORY_TOTALS.blocks !== 2059 || HOUSE_VITALS.length !== 2059)")
s = s.replace("vsota-blokov ≠ 2043 (modul-vsota ${p254Sum} / TOTALS ${HOUSE_STORY_TOTALS.blocks} / HOUSE_VITALS ${HOUSE_VITALS.length})",
              "vsota-blokov ≠ 2059 (modul-vsota ${p254Sum} / TOTALS ${HOUSE_STORY_TOTALS.blocks} / HOUSE_VITALS ${HOUSE_VITALS.length})")
s = s.replace("P253-snapshot-2023/živo-2043 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257!)",
              "P253-snapshot-2023/živo-2059 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257 + 16-P258!)")
steps.append("3-p254Sum")

# ——— 4) SIX-lista ×2 ———
OLD23 = '["1", "3", "5", "6", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "56", "61", "62", "63", "65", "73"]'
NEW31 = '["1", "2", "3", "5", "6", "8", "10", "11", "12", "16", "18", "19", "20", "22", "26", "27", "28", "32", "33", "35", "36", "42", "46", "47", "48", "56", "61", "62", "63", "65", "73"]'
c_six = s.count(OLD23); s = s.replace(OLD23, NEW31)
s = s.replace("šest-knjižne-živo ≠ [1,3,5,6,10,11,12,16,18,19,20,22,26,27,28,32,33,56,61,62,63,65,73]",
              "šest-knjižne-živo ≠ [1,2,3,5,6,8,10,11,12,16,18,19,20,22,26,27,28,32,33,35,36,42,46,47,48,56,61,62,63,65,73] (P258: +8!)")
s = s.replace("HOUSE_STORY_SIX ≠ [1,3,5,6,10,11,12,16,18,19,20,22,26,27,28,32,33,56,61,62,63,65,73]",
              "HOUSE_STORY_SIX ≠ [1,2,3,5,6,8,10,11,12,16,18,19,20,22,26,27,28,32,33,35,36,42,46,47,48,56,61,62,63,65,73] (P258: +8!)")
steps.append(f"4-SIX×{c_six}")

# ——— 5) tiers + bothEra ———
s = s.replace("if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== 23 || HOUSE_STORY_TIERS[0]?.books !== 6)",
              "if (p254TierSum !== 100 || HOUSE_STORY_TIERS[0]?.houses !== 31 || HOUSE_STORY_TIERS[0]?.books !== 6)")
s = s.replace("if (HOUSE_STORY_TOTALS.bothEraKrstna !== 69 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== 26)",
              "if (HOUSE_STORY_TOTALS.bothEraKrstna !== 69 || HOUSE_STORY_TOTALS.bothEraMrliska !== 75 || HOUSE_STORY_TOTALS.bothEraPorocna !== 34)")
s = s.replace('p254Errors.push("obe-eri-pokritje ≠ 69/75/26 (krstna/mrliška/poročna!)");',
              'p254Errors.push("obe-eri-pokritje ≠ 69/75/34 (krstna/mrliška/poročna!-P258: +8!)");')
s = s.replace('if (HOUSE_STORY_TOTALS.bothEraPorocna !== 26) p256Errors.push("bothEra-poročna ≠ 26 (P257!)");',
              'if (HOUSE_STORY_TOTALS.bothEraPorocna !== 34) p256Errors.push("bothEra-poročna ≠ 34 (P258: +8 — h47/h46/h8/h48/h2/h35/h36/h42!)");')
steps.append("5-tiers-bothEra")

# ——— 6) byBook 31→47 (×4) ———
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
steps.append("6-byBook")

# ——— 7) p94-izjemi (h22-1832 + h49-1833) ———
old94 = '&& !(v.bookSignature === "01738" && v.year === 1830 && hn === "22"))) // P257: + poročna 01738-1830 h22 (m4-Anna-MILEK-nevesta — 3.-ZAPOREDNO-LETO-1828+1829+1830!)'
new94 = ('&& !(v.bookSignature === "01738" && v.year === 1830 && hn === "22") '
         '&& !(v.bookSignature === "01738" && v.year === 1832 && hn === "22") '
         '&& !(v.bookSignature === "01738" && v.year === 1833 && hn === "49")'
         ')) // P258: + poročna 01738-1832 h22 (m8-ŽENIN-Johann-MILEK-oče-Johann!-MILEK-DOMNEVA-POTRJENA-4.-blok-v-5-letih!) + 01738-1833 h49 (m6-NEVESTA-Maria-[~Himiz]-×-Johann-PESDIRZ-h50!-h49-BREZ-04455-poročna-vrzela!) // P257: + poročna 01738-1830 h22 (m4-Anna-MILEK-nevesta — 3.-ZAPOREDNO-LETO-1828+1829+1830!)')
assert old94 in s; s = s.replace(old94, new94); steps.append("7-p94")

# ——— 8) MILIČ 250→252 ———
s = s.replace("MILIC_FAMILY_TOTAL !== 250", "MILIC_FAMILY_TOTAL !== 252")
s = s.replace("MILIČ-family-total ≠ 250", "MILIČ-family-total ≠ 252")
s = s.replace('"53,78,20,36,60,3"', '"53,78,20,36,60,5"')
s = s.replace("MILIČ-po-knjigah ≠ [53,78,20,36,60,3]", "MILIČ-po-knjigah ≠ [53,78,20,36,60,5]")
s = s.replace("53+78+20+36+60+3 čez 6 knjig (P257: +2 — h22-1830-Anna-Milek + h65-1831-Nicol-Milek!)",
              "53+78+20+36+60+5 čez 6 knjig (P257: +2 — h22-1830-Anna-Milek + h65-1831-Nicol-Milek! + P258: +2 — h22-1832-ŽENIN-Johann-Milek + h35-1832-nevesta-stran-Milek!)")
steps.append("8-MILIČ")

# ——— 9) p237-križ ———
old237 = "p237Errors.push(`neodvisni-križ-proti-korpusu ≠ 250 (${p237Križ} — P248: +1-v9-'Mihelič'-garble-kandidat!-P246: +2-v7/v11!-P250: +2-1874-m5-h65-+-m16-h29!-P251: +4-1873!-P253: +1-01738-predhodnik-m2!-P257: +2-1830/31 (h22-Anna-Milek + h65-Nicol-Milek!)!)`);"
new237 = "p237Errors.push(`neodvisni-križ-proti-korpusu ≠ 252 (${p237Križ} — P248: +1-v9!-P246: +2!-P250: +2-1874!-P251: +4-1873!-P253: +1!-P257: +2-1830/31!-P258: +2-1832 (h22-ŽENIN-Johann-Milek + h35-nevesta-stran!)!)`);"
assert old237 in s; s = s.replace(old237, new237)
m = re.search(r'p237Križ !== (\d+)', s)
assert m and m.group(1) == "250"
s = s.replace("p237Križ !== 250", "p237Križ !== 252")
steps.append("9-p237-križ")

# ——— 10) p88-h46 izjema ———
old88 = "&& !(v.bookSignature === \"04106\" && v.year === 1865 && hn === \"23\") && !(v.bookSignature === \"04106\" && v.year === 1865 && hn === \"70\")))"
new88 = ("&& !(v.bookSignature === \"04106\" && v.year === 1865 && hn === \"23\") && !(v.bookSignature === \"04106\" && v.year === 1865 && hn === \"70\")"
         " && !(v.bookSignature === \"01738\" && v.year === 1831 && hn === \"46\")))"
         " // P258: + poročna 01738-1831 h46 (m19-ŽENIN-Matthias-KLOBUČAR-h46×h8 — POLNI-DVOJNI-24.-Avg!)")
assert old88 in s; s = s.replace(old88, new88); steps.append("10-p88-h46")

# ——— 11) p254: h2-93 + h50-13 + 66-skupina ———
s = s.replace('''    // 66-letni razponi (h50 izstopila — P257: h50-span-93!)
    for (const hh of ["2", "13", "60", "64"]) {
      const st = houseStoryByNo(hh);
      if (!st || st.span !== 66) p254Errors.push(`h${hh}-razpon ≠ 66 let (${st?.span})`);
    }''',
'''    // 66-letni razponi (h50 izstopila — P257: h50-span-93!; h2 izstopila — P258: h2-firstYear-1831-span-93!)
    for (const hh of ["13", "60", "64"]) {
      const st = houseStoryByNo(hh);
      if (!st || st.span !== 66) p254Errors.push(`h${hh}-razpon ≠ 66 let (${st?.span})`);
    }
    const h2st66 = houseStoryByNo("2");
    if (!h2st66 || h2st66.span !== 93 || h2st66.firstYear !== 1831 || h2st66.books !== 6)
      p254Errors.push(`h2-P258 ≠ span-93/firstYear-1831/6-knjig (${h2st66?.span}/${h2st66?.firstYear}/${h2st66?.books})`);''')
s = s.replace('''    const h50st = houseStoryByNo("50");
    if (!h50st || h50st.span !== 93 || h50st.firstYear !== 1831 || h50st.blocks !== 12)
      p254Errors.push(`h50-PEZDIRC-nit ≠ span-93/firstYear-1831/12-blokov (${h50st?.span}/${h50st?.firstYear}/${h50st?.blocks})`);''',
'''    const h50st = houseStoryByNo("50");
    if (!h50st || h50st.span !== 93 || h50st.firstYear !== 1831 || h50st.blocks !== 13)
      p254Errors.push(`h50-PEZDIRC-nit ≠ span-93/firstYear-1831/13-blokov (${h50st?.span}/${h50st?.firstYear}/${h50st?.blocks})`);''')
steps.append("11-p254-h2/h50")

# ——— 12) p257: scan-7 filter + h22-36 ———
s = s.replace('const p257Live = HOUSE_VITALS.filter((v) => v.bookSignature === "01738" && v.year === 1831);',
              'const p257Live = HOUSE_VITALS.filter((v) => v.bookSignature === "01738" && v.year === 1831 && v.scan === 7); // P258: +scan-7 (s8-bloki = qa-p258!)')
s = s.replace("""    const h22st = houseStoryByNo("22");
    if (!h22st || h22st.firstYear !== 1828 || h22st.span !== 93 || h22st.blocks !== 35 || h22st.perBook[0]?.n !== 3)
      p257Errors.push(`h22 ≠ firstYear-1828/span-93/35-blokov/01738×3 (${h22st?.firstYear}/${h22st?.span}/${h22st?.blocks}/${h22st.perBook[0]?.n})`);""",
"""    const h22st = houseStoryByNo("22");
    if (!h22st || h22st.firstYear !== 1828 || h22st.span !== 93 || h22st.blocks !== 36 || h22st.perBook[0]?.n !== 4)
      p257Errors.push(`h22 ≠ firstYear-1828/span-93/36-blokov/01738×4-P258 (${h22st?.firstYear}/${h22st?.span}/${h22st?.blocks}/${h22st?.perBook[0]?.n})`);""")
steps.append("12-p257-scan7-h22")

open(QA, "w", encoding="utf-8").write(s)
print("KORAK-A:", " | ".join(steps), f"| delta={len(s)-n0}")

# ——— 13) pt-luknja: 04455 265→269 (kirurško) ———
d = json.load(open(PT, encoding="utf-8"))
assert d["corpus"]["vitalsTotal"] == 2059 and d["corpus"]["byBook"]["01738"] == 47
d["corpus"]["byBook"]["04455"] = 269
json.dump(d, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("KORAK-B: pt-luknja 04455→269 (vitals 2059/01738 47 že OK)")
