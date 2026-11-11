#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250-OBNOVA: stražarski popravki v qa-parish.ts (p85/p92-izjeme, p115-izjema,
MILIČ-241→243, p237-pod-previrke, forensics-komentar) + sken-range in letni gardi
sta del p250_bump.py — ta skripta pokrije PREOSTANE ročne popravke."""
import re

# ——— 1. qa-parish.ts stražarji ———
P1 = 'src/lib/qa-parish.ts'
src = open(P1, encoding='utf-8').read()
n0 = len(src)

a = '&& !(v.bookSignature === "04455" && v.year === 1876 && (hn === "30" || hn === "41")) && !(v.bookSignature === "04455" && v.year === 1881 && hn === "28")'
b = '&& !(v.bookSignature === "04455" && v.year === 1876 && (hn === "30" || hn === "41")) && !(v.bookSignature === "04455" && v.year === 1874 && (hn === "7" || hn === "30")) && !(v.bookSignature === "04455" && v.year === 1881 && hn === "28")'
if a in src:
    src = src.replace(a, b, 1)
    src = src.replace('// P248: + izjeme-04455-1876-h30/h41',
                      '// P250: + izjeme-04455-1874-h7/h30 (m6-Johann-Totlhar-GRIBLJE 7!-+ m16-Johann-Milek-GRIBLJE 30!-poročna-predzgodovina!)\n// P248: + izjeme-04455-1876-h30/h41', 1)
    print('p85-izjeme-vređene')

a = '&& !(v.bookSignature === "04455" && v.year === 1877 && hn === "10") && !(v.bookSignature === "04455" && v.year === 1889 && hn === "40")'
b = '&& !(v.bookSignature === "04455" && v.year === 1877 && hn === "10") && !(v.bookSignature === "04455" && v.year === 1874 && (hn === "10" || hn === "43")) && !(v.bookSignature === "04455" && v.year === 1889 && hn === "40")'
if a in src:
    src = src.replace(a, b, 1)
    src = src.replace('// P247: + poročni blok 04455-1877 h10 (v1-nevesta-Cäcilie-Grubanič',
                      '// P250: + izjeme-04455-1874-h10/h43 (m17-Mathias-Kraue-GRIBLJE 10!-+ m25-Marina-BRULA-GRIBLJE 43!-poročna-predzgodovina!)\n// P247: + poročni blok 04455-1877 h10 (v1-nevesta-Cäcilie-Grubanič', 1)
    print('p92-izjeme-vređene')

a = '!(old === "GRIBLJE 29" && (h.year === 1897 || h.year === 1909))'
b = '!(old === "GRIBLJE 29" && (h.year === 1897 || h.year === 1909 || h.year === 1874))'
if a in src:
    src = src.replace(a, b, 1)
    src = src.replace('// P126: »GRIBLJE 29« LEGITIMNO v poročnih blokih 1897',
                      '// P250: + 1874 (m16-Johann-MILEK-GRIBLJE 29-mikro-1:1!-pass1-\'Verček\'-garble-ZAVRŽEN!-legitimno!)\n// P126: »GRIBLJE 29« LEGITIMNO v poročnih blokih 1897', 1)
    print('p115-izjema-vređena')

src = src.replace('MILIC_FAMILY_TOTAL !== 241', 'MILIC_FAMILY_TOTAL !== 243')
src = src.replace('MILIČ-family-total ≠ 241', 'MILIČ-family-total ≠ 243')
src = src.replace('MILIČ-po-knjigah ≠ [53,78,20,36,54]', 'MILIČ-po-knjigah ≠ [53,78,20,36,56]')
src = src.replace('53+78+20+36+54 čez 5 knjig', '53+78+20+36+56 čez 5 knjig')
src = src.replace('[53,78,20,36,54] (53,78,20,36,', '[53,78,20,36,56] (53,78,20,36,')
src = src.replace('237 + 1-nov-1876-P248-v9-\'Mihelič\'-garble!-+ 1-nov-1879-v25!-+ 2-nov-1878-P246!)',
                  '237 + 1-nov-1876-P248-v9-\'Mihelič\'-garble!-+ 1-nov-1879-v25!-+ 2-nov-1878-P246!-+ 2-nov-1874-P250 (m5-Mathias-Milek-h65-+ m16-Johann-Milek-h29!)!)')
src = src.replace('P248-v9-\'Mihelič\'[~Milek]-garble-kandidat!-+ P246-v7-Milek-h65!-+ v11-cf.-MILIČ-P235!-P244-v25-Mihelec-prej!`',
                  'P248-v9-\'Mihelič\'[~Milek]-garble-kandidat!-+ P246-v7-Milek-h65!-+ v11-cf.-MILIČ-P235!-P244-v25-Mihelec-prej!-+ P250-×2-1874 (m5-h65-+ m16-h29!)`')
src = src.replace('MILIČ-family-total ≠ 243 (${MILIC_FAMILY_TOTAL} — 1881-brez-novih-križev!-+1-P248-1876!-+2-P246-1878!)',
                  'MILIČ-family-total ≠ 243 (${MILIC_FAMILY_TOTAL} — 1881-brez-novih-križev!-+1-P248-1876!-+2-P246-1878!-+2-P250-1874!)')
src = src.replace('MILIČ-family-total ≠ 243 (${MILIC_FAMILY_TOTAL} — 1882-brez-novih-križev!-+1-P248-1876!-+2-P246-1878!)',
                  'MILIČ-family-total ≠ 243 (${MILIC_FAMILY_TOTAL} — 1882-brez-novih-križev!-+1-P248-1876!-+2-P246-1878!-+2-P250-1874!)')

# p237-pod-previrke
src = src.replace('p237PoKnjigah.join(",") !== "53,78,20,36,54"', 'p237PoKnjigah.join(",") !== "53,78,20,36,56"')
src = src.replace('if (p237Križ !== 241)\n    p237Errors.push(`neodvisni-križ-proti-korpusu ≠ 241 (${p237Križ} — P248: +1-v9-\'Mihelič\'-garble-kandidat!-P246: +2-v7/v11!)`);',
                  'if (p237Križ !== 243)\n    p237Errors.push(`neodvisni-križ-proti-korpusu ≠ 243 (${p237Križ} — P248: +1-v9-\'Mihelič\'-garble-kandidat!-P246: +2-v7/v11!-P250: +2-1874-m5-h65-+-m16-h29!)`);')
src = src.replace('if (MATHIAS_H65_TOTAL !== 22)', 'if (MATHIAS_H65_TOTAL !== 23)')
src = src.replace('p237Errors.push(`Mathias/Matija-h65-veriga ≠ 22 (${MATHIAS_H65_TOTAL})`);',
                  'p237Errors.push(`Mathias/Matija-h65-veriga ≠ 23 (${MATHIAS_H65_TOTAL} — P250-m5-Mathias-MILEK-h65-1874!)`);')
src = src.replace('if (H65_STATS.total !== 42 || H65_STATS.family !== 36 || H65_STATS.others !== 6)\n    p237Errors.push(`h65 ≠ {42, 36, 6} (${H65_STATS.total}/${H65_STATS.family}/${H65_STATS.others} — 04894-1907: \'h65 = MILEK-hiša!\')`);',
                  'if (H65_STATS.total !== 43 || H65_STATS.family !== 37 || H65_STATS.others !== 6)\n    p237Errors.push(`h65 ≠ {43, 37, 6} (${H65_STATS.total}/${H65_STATS.family}/${H65_STATS.others} — 04894-1907: \'h65 = MILEK-hiša!\'-P250-m5-blok!)`);')
src = src.replace('**★★★ MILIČ↔MILEK-križ = ×237 blokov** (04104 ×53 · 04105 ×78 · 04106 ×20 · 04894 ×36 · 04455 ×47',
                  '**★★★ MILIČ↔MILEK-križ = ×243 blokov** (04104 ×53 · 04105 ×78 · 04106 ×20 · 04894 ×36 · 04455 ×56-P250-+2!— P250-m5-Mathias-MILEK-h65-+-m16-Johann-MILEK-h29!')
src = src.replace('**★★★ Mathias/Matija-h65-veriga ×22 blokov 1871–1914 = 43 let**',
                  '**★★★ Mathias/Matija-h65-veriga ×23 blokov 1871–1914 = 43 let** (P250-m5-1874-Mathias-MILEK-h65!)')
src = src.replace('**h65 = {42 blokov · 36 družinskih · 6 ostalih (Brinc/Brune-doba 1863–1873!)}**',
                  '**h65 = {43 blokov · 37 družinskih · 6 ostalih (Brinc/Brune-doba 1863–1873!-P250-m5!)}**')
open(P1, 'w', encoding='utf-8').write(src)
print('qa-parish.ts stražarji:', n0, '→', len(src))

# ——— 2. parish-forensics.ts komentar ———
P2 = 'src/data/atlas/parish-forensics.ts'
f = open(P2, encoding='utf-8').read()
f2 = f.replace('total: 241', 'total: 243')
if f2 != f:
    open(P2, 'w', encoding='utf-8').write(f2)
    print('forensics total-243')
else:
    print('forensics-ni-sprememb')
