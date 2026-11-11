#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — kaskadna posodobitev starih preverjevalnikov (po vzoru P256: 2026→2032 → zdaj 2032→2043).
1) qa-parish.ts: HOUSE_VITALS.length → 2043 (vse žive kontrole) + MILIČ 248→250/{43,37,6}→{44,38,6}/[..,1]→[..,3]
   + p253-byBook 20→31 + p94-izjema h22-1830.
2) pt-luknja-18-final.json: 2032→2043, 01738 20→31, housesNote + P257."""
import json
import re

QA = "src/lib/qa-parish.ts"
PT = "research/issue17/pt-luknja-18-final.json"

s = open(QA, encoding="utf-8").read()
n0 = s

# ——— 1) HOUSE_VITALS.length !== N → 2043 (vse žive; P253-snapshot konstante v modulu se NE dotikajo) ———
def sub_len(m):
    n = int(m.group(1))
    if n == 2043:
        return m.group(0)
    return "HOUSE_VITALS.length !== 2043"
s, c1 = re.subn(r"HOUSE_VITALS\.length !== (\d{3,4})", sub_len, s)

# ——— 2) MILIČ: 248→250 (p237/p239/p240/p242 — 4 kraji + sporočila) ———
s = s.replace("MILIC_FAMILY_TOTAL !== 248", "MILIC_FAMILY_TOTAL !== 250")
s = s.replace("MILIČ-family-total ≠ 248", "MILIČ-family-total ≠ 250")
s = s.replace("MILIČ-family-total ≠ 247", "MILIČ-family-total ≠ 250")
s = s.replace("53+78+20+36+60+1 čez 6 knjig", "53+78+20+36+60+3 čez 6 knjig (P257: +2 — h22-1830-Anna-Milek + h65-1831-Nicol-Milek!)")
s = s.replace('"53,78,20,36,60,1"', '"53,78,20,36,60,3"')
s = s.replace("MILIČ-po-knjigah ≠ [53,78,20,36,60,1]", "MILIČ-po-knjigah ≠ [53,78,20,36,60,3]")
s = s.replace("— P253: + 01738-predhodnik-×1!`);", "— P253: + 01738-predhodnik-×1 + P257: + 01738-1830/31-×2 (h22+h65!)`);")
# h65 {43,37,6} → {44,38,6}
s = s.replace("H65_STATS.total !== 43 || H65_STATS.family !== 37 || H65_STATS.others !== 6",
              "H65_STATS.total !== 44 || H65_STATS.family !== 38 || H65_STATS.others !== 6")
s = s.replace("h65 ≠ {43, 37, 6}", "h65 ≠ {44, 38, 6}")
s = s.replace("(H65_STATS.total}/${H65_STATS.family}/${H65_STATS.others} — 04894-1907:",
              "(H65_STATS.total}/${H65_STATS.family}/${H65_STATS.others} — P257: +1831-Nicol-Milek! — 04894-1907:")

# ——— 3) p253: byBook-živo 20→31 ———
s = s.replace("if (by01738.length !== 20 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)",
              "if (by01738.length !== 31 || PREDHODNIK_1873_KORPUS.byBook01738 !== 11)")
s = s.replace("byBook-01738 ≠ 20-živo/11-P253-snapshot (${by01738.length} — P256: +6-blokov-1829!)",
              "byBook-01738 ≠ 31-živo/11-P253-snapshot (${by01738.length} — P257: +11-blokov-1830/31!)")
s = s.replace("P253-snapshot-2023/živo-2026 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255!)",
              "P253-snapshot-2023/živo-2043 (${PREDHODNIK_1873_KORPUS.vitalsTotal}/${HOUSE_VITALS.length} — 2012+11-P253 + 3-P255 + 6-P256 + 11-P257!)")

# ——— 4) p94-izjema: h22-1830 (za 1828/1829 dodajamo 1830!) ———
old94 = '&& !(v.bookSignature === "01738" && v.year === 1829 && hn === "22")))'
new94 = ('&& !(v.bookSignature === "01738" && v.year === 1829 && hn === "22") '
         '&& !(v.bookSignature === "01738" && v.year === 1830 && hn === "22"))'
         ') // P257: + poročna 01738-1830 h22 (m4-Anna-MILEK-nevesta — 3.-ZAPOREDNO-LETO-1828+1829+1830!)')
assert old94 in s, "p94-izjema: niza ni!"
s = s.replace(old94, new94, 1)

open(QA, "w", encoding="utf-8").write(s)
print(f"qa-parish.ts: {c1} HOUSE_VITALS-kontrol → 2043; MILIČ 248→250; h65 {{44,38,6}}; p253 20→31; p94+h22-1830; delta={len(s)-len(n0)} znakov")

# ——— 5) pt-luknja-18-final.json ———
d = json.load(open(PT, encoding="utf-8"))
d["corpus"]["vitalsTotal"] = 2043
d["corpus"]["byBook"]["01738"] = 31
d["vitalsTotal"] = 2043 if "vitalsTotal" in d else d.get("vitalsTotal")
hn = d["corpus"].get("housesNote", "")
if "P257" not in hn:
    d["corpus"]["housesNote"] = hn + " | P257: +11-blokov-1830/31-01738 (1×h22-1830 + 10×1831: h3/h33/h50/h54/h56/h26/h27/h65/h1/h11!) — vitals 2032→2043, 01738 20→31, šest-knjižne 16→23, bothEra 17→26!"
json.dump(d, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pt-luknja-18-final.json: 2043/31 + housesNote-P257")
