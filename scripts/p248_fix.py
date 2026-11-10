#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P248-fix: p85-izjemi (h30/h41-04455-1876) + MILIČ-garde 240→241 (v9-'Mihelič'-garble-kandidat!)."""
ROOT = "/home/z/my-project"
QA = f"{ROOT}/src/lib/qa-parish.ts"
delo = 0

src = open(QA, encoding="utf-8").read()

def rep(a, b, n_expect=1):
    global src, delo
    n = src.count(a)
    src = src.replace(a, b)
    delo += n
    print(f"  [{n}] {a[:60]} → {b[:60]}")

# ——— 1. p85-izjemi h30/h41-04455-1876 ———
a = '&& !(v.bookSignature === "04455" && v.year === 1881 && hn === "41")'
b = a + ' && !(v.bookSignature === "04455" && v.year === 1876 && (hn === "30" || hn === "41"))'
rep(a, b)

# opomba-komentar za izjeme
a = "// P242: + izjeme-04455-1881-h41/h28"
b = "// P248: + izjeme-04455-1876-h30/h41 (v14-Anna-PEGDIRE-h30-'Leinmannstochter'!-+ v13-Maria-PEGDIRE-h41-'Leinmannstochter'!-14-/15-let-pred-prvencema-1890!-poročna-predzgodovina-PEZDIRC-veja!)\n// P242: + izjeme-04455-1881-h41/h28"
rep(a, b)

# ——— 2. MILIČ-garde 240→241 ———
rep("if (MILIC_FAMILY_TOTAL !== 240)\n    p237Errors.push(`MILIČ-family-total ≠ 240 (${MILIC_FAMILY_TOTAL} — 53+78+20+36+53 čez 5 knjig — P246-v7-Milek-h65!-+ v11-cf.-MILIČ-P235!-P244-v25-Mihelec-prej!`);",
    "if (MILIC_FAMILY_TOTAL !== 241)\n    p237Errors.push(`MILIČ-family-total ≠ 241 (${MILIC_FAMILY_TOTAL} — 53+78+20+37+53 čez 5 knjig — P248-v9-'Mihelič'[~Milek]-garble-kandidat!-+ P246-v7-Milek-h65!-+ v11-cf.-MILIČ-P235!-P244-v25-Mihelec-prej!`);")
rep('p237PoKnjigah.join(",") !== "53,78,20,36,53"', 'p237PoKnjigah.join(",") !== "53,78,20,37,53"')
rep("MILIČ-po-knjigah ≠ [53,78,20,36,53]", "MILIČ-po-knjigah ≠ [53,78,20,37,53]")
rep("neodvisni-križ-proti-korpusu ≠ 240 (${p237Križ} — P246: +2-v7/v11!)",
    "neodvisni-križ-proti-korpusu ≠ 241 (${p237Križ} — P248: +1-v9-'Mihelič'-garble-kandidat!-P246: +2-v7/v11!)")
rep("if (MILIC_FAMILY_TOTAL !== 240) p239Errors.push(`MILIČ-family-total ≠ 240 (${MILIC_FAMILY_TOTAL} — 237 + 1-nov-1879-v25-Mihelec! + 2-nov-1878-P246!)`);",
    "if (MILIC_FAMILY_TOTAL !== 241) p239Errors.push(`MILIČ-family-total ≠ 241 (${MILIC_FAMILY_TOTAL} — 237 + 1-nov-1876-P248-v9-'Mihelič'-garble!-+ 1-nov-1879-v25!-+ 2-nov-1878-P246!)`);")
rep("if (MILIC_FAMILY_TOTAL !== 240) p240Errors.push(`MILIČ-family-total ≠ 240 (${MILIC_FAMILY_TOTAL} — 237 + 1-nov-1879! + 2-nov-1878-P246!)`);",
    "if (MILIC_FAMILY_TOTAL !== 241) p240Errors.push(`MILIČ-family-total ≠ 241 (${MILIC_FAMILY_TOTAL} — 237 + 1-nov-1876-P248-v9!-+ 1-nov-1879!-+ 2-nov-1878-P246!)`);")
rep("if (MILIC_FAMILY_TOTAL !== 240) p242Errors.push(`MILIČ-family-total ≠ 240 (${MILIC_FAMILY_TOTAL} — 1881-brez-novih-križev!-+2-P246-1878!)`);",
    "if (MILIC_FAMILY_TOTAL !== 241) p242Errors.push(`MILIČ-family-total ≠ 241 (${MILIC_FAMILY_TOTAL} — 1881-brez-novih-križev!-+1-P248-1876!-+2-P246-1878!)`);")
rep("if (MILIC_FAMILY_TOTAL !== 240) p241Errors.push(`MILIČ-family-total ≠ 240 (${MILIC_FAMILY_TOTAL} — 1882-brez-novih-križev!-+2-P246-1878!)`);",
    "if (MILIC_FAMILY_TOTAL !== 241) p241Errors.push(`MILIČ-family-total ≠ 241 (${MILIC_FAMILY_TOTAL} — 1882-brez-novih-križev!-+1-P248-1876!-+2-P246-1878!)`);")

open(QA, "w", encoding="utf-8").write(src)
print(f"P248-fix: {delo} sprememb")
