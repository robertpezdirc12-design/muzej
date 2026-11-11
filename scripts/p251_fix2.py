#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P251 — popravki 2. kroga: MILIČ-križ 243→247 (04455 56→60!) + p94-h22-izjema-1873."""
ROOT = "/home/z/my-project"
QA = f"{ROOT}/src/lib/qa-parish.ts"
delo = 0
src = open(QA, encoding="utf-8").read()

def rep(a, b, label=""):
    global src, delo
    n = src.count(a)
    src = src.replace(a, b); delo += n
    print(f"  [{n}] {a[:60]} → {b[:48]} {label}")

# 1. p94: h22-izjema-04455-1873
rep('&& !(v.bookSignature === "04455" && hn === "22" && (v.year === 1898 || v.year === 1904 || v.year === 1919))',
    '&& !(v.bookSignature === "04455" && hn === "22" && (v.year === 1873 || v.year === 1898 || v.year === 1904 || v.year === 1919))',
    "(p94-h22-1873!)")

# 2. MILIČ-total ×5: 243→247 + narrativi
rep("if (MILIC_FAMILY_TOTAL !== 243)", "if (MILIC_FAMILY_TOTAL !== 247)")
rep("MILIČ-family-total ≠ 243 (", "MILIČ-family-total ≠ 247 (")
rep("MILIČ↔MILEK-križ = ×243 blokov", "MILIČ↔MILEK-križ = ×247 blokov")
rep("neodvisni-križ-proti-korpusu ≠ 243 (247", "neodvisni-križ-proti-korpusu ≠ 247 (247")
rep("53+78+20+36+56 čez 5 knjig", "53+78+20+36+60 čez 5 knjig")
rep("04455 ×56-P250-+2!", "04455 ×60-P251-+4!-+ P250-+2!")
rep("P250-×2-1874 (m5-h65-+ m16-h29!)", "P250-×2-1874 (m5-h65-+ m16-h29!)-+ P251-×4-1873 (m18-mati-Maria-Milek-h13/h62!-+ m20-ženin-Johann-Milek-h22/h50!)")
rep("MILIČ-po-knjigah ≠ [53,78,20,36,56]", "MILIČ-po-knjigah ≠ [53,78,20,36,60]")
rep('p237PoKnjigah.join(",") !== "53,78,20,36,56"', 'p237PoKnjigah.join(",") !== "53,78,20,36,60"')
rep("+ 2-nov-1874-P250 (m5-Mathias-Milek-h65-+ m16-Johann-Milek-h29!)!)", "+ 2-nov-1874-P250 (m5-Mathias-Milek-h65-+ m16-Johann-Milek-h29!)-+ 4-nov-1873-P251 (m18-mati-Maria-Milek-×2-h13/h62!-+ m20-ženin-Johann-Milek-×2-h22/h50!)!)")

open(QA, "w", encoding="utf-8").write(src)
print(f"P251-fix2: {delo} sprememb")
