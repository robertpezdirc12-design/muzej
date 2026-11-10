#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p241_qa_insert — vstavi qa-p241 blok v src/lib/qa-parish.ts pred qa-p234 komentar."""
import sys

PATH = '/home/z/my-project/src/lib/qa-parish.ts'
with open(PATH, encoding='utf-8') as f:
    text = f.read()

anchor = None
for line in text.split('\n'):
    if 'qa-p234' in line and '1872' in line and line.strip().startswith('//'):
        anchor = line
        break
if anchor is None:
    print('ABORT: anchor ni najden'); sys.exit(1)
if text.count(anchor) != 1:
    print('ABORT: anchor ni unikaten'); sys.exit(1)

BLOCK = '''  // ——— qa-p241: POROČNA PREDZGOVINA 04455 — leto 1882 = 4/13 (P241) ———
  {
    const p241Errors: string[] = [];
    if (HOUSE_VITALS.length !== 1958) p241Errors.push(`HOUSE_VITALS ≠ 1958 (${HOUSE_VITALS.length})`);
    if (MARRIAGE_1882_GRIBLJE !== 7) p241Errors.push(`Griblje-poroke-1882 ≠ 7 (${MARRIAGE_1882_GRIBLJE})`);
    const p241Pri = ["35", "38", "56", "13", "8", "1", "36"];
    if (JSON.stringify(MARRIAGE_1882_HOUSES) !== JSON.stringify(p241Pri)) p241Errors.push(`hiše-1882 ≠ [35,38,56,13,8,1,36] (${MARRIAGE_1882_HOUSES.join(",")})`);
    if (MARRIAGE_1882_TOTAL !== 26) p241Errors.push("vpisi-1882 ≠ 26 (BREZ-preskokov — 4.-leto-zapored!-kontrast-1885-vpis-3!)");
    if (MARRIAGE_1882_XOPEN.length !== 2) p241Errors.push(`X-OPEN-dueli-1882 ≠ 2 (${MARRIAGE_1882_XOPEN.length} — v14-3-vasni-+ v17-Mličar/Mlinar!)`);
    if (MARRIAGE_1882_VILLAGE_DUELS.length !== 4) p241Errors.push(`vas-dueli-1882 ≠ 4 (${MARRIAGE_1882_VILLAGE_DUELS.length})`);
    if (!MARRIAGE_1882_BLOCKS.some((h) => h.whatSi.includes("h1 = NAJNIŽJA-HIŠA-S-POROČNIM-BLOKOM-KADARKOLI"))) p241Errors.push("h1-REKORD-ni-označen (vpis-23-LESIRO!)");
    if (!MARRIAGE_1882_BLOCKS.some((h) => h.whatSi.includes("RESTART-1882 = s45"))) p241Errors.push("restart-s45-glava-PRED-vrstico-1-ni-označena (NOVA-4.-mejna-varianta!)");
    if (!MARRIAGE_1882_BLOCKS.some((h) => h.whatSi.includes("h36-PREDISTOPNA-NIT-P240-IZPOLNJENA"))) p241Errors.push("v26-h36-P240-napoved-IZPOLNJENA-ni-označena (TAIL-1882!)");
    if (!MARRIAGE_1882_BLOCKS.some((h) => h.whatSi.includes("POLNI-GRIBLJE-BLOK ×2"))) p241Errors.push("POLNI-GRIBLJE-BLOK-×2-ni-označen (h38×h12 · h13×h52 · h1×h10!)");
    if (!MARRIAGE_1882_BLOCKS.some((h) => h.whatSi.includes("BRINC/BRINEC-MREŽA"))) p241Errors.push("v13-BRINC-vdova-h56-mreža-ni-označena (priči-Peter-×-Georg-BRINEC!)");
    // neodvisni PEZDIRC-križ 1882: korpus-bloki z PEZDIRC-v-whatSi = 2 (v15-Maria-h52 + v16-Michael!-v9/v18/v21-so-izven-Griblje-blokov!)
    const p241Pez = MARRIAGE_1882_BLOCKS.filter((h) => /PEZDIRC/i.test(h.whatSi));
    if (p241Pez.length !== 2) p241Errors.push(`PEZDIRC-bloki-1882 ≠ 2 (${p241Pez.map((h) => h.houseNo).join(",")} — v15-Maria-h52-+ v16-Michael!-v9/v18/v21-so-izven-Griblje!)`);
    // neodvisni križ 1882: PRAZEN (iskreno!) — noben MILEK/MILIČ-vpis-v-1882 (križ-×237-ostaja!-v17-'Mličar'-NI-MILIČ!)
    const p241Križ = MARRIAGE_1882_BLOCKS.filter((h) => MILIC_FAMILY_RE.test(h.whatSi));
    if (p241Križ.length !== 0)
      p241Errors.push(`križ-bloki-1882 ≠ [] (${p241Križ.map((h) => h.houseNo).join(",")} — nobenega-MILEK/MILIČ-v-1882-iskreno!-v17-'Mličar'-NI-MILIČ!)`);
    if (MILIC_FAMILY_TOTAL !== 237) p241Errors.push(`MILIČ-family-total ≠ 237 (${MILIC_FAMILY_TOTAL} — 1882-brez-novih-križev!)`);
    if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 215)
      p241Errors.push(`bloki-04455 ≠ 215 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — 208 + 7-leta-1882!)`);
    push(
      "qa-p241-parish-marriage-early-04455-1882",
      "P241: ŽUPNIJA PODZEMELJ — POROČNA PREDZGOVINA 04455, LETO 1882 = 4/13 (issue #18): s45–s50 (6 razprti-listov; 26-vpisov-leta-1882-ŠTEVJE-IZ-ZAP-STOLPCA-1.–26.-BREZ-preskokov-4.-leto-zapored!-kontrast-1885-vpis-3!) · RESTART-1882 = s45 (VELIKA-GLAVA-'1882'-PRED-VRSTICO-1-NE-V-GLAVI-STRANI!-NOVA-4.-MEJNA-VARIANTA!-cf.-1883-'1-8-8-3.'-razporejeno + 1884/1885-vrhnja!) · MEJA-1881/82 = s44→s45-glava (tail-1881-NI-na-s45-top!) · MEJA-1882/83 = s50-MID (P240-1:1!) · številčenje s45=1–4 · s46=5–8 · s47=9–12 · s48=13–17 · s49=18–23 (nodat-trakovi-×5!) · s50-tail=24–26 — 7-GRIBLJE-blokov [35,38,56,13,8,1,36] (3-POLNA ×2!) · ★★★★★ h1 = NAJNIŽJA-HIŠA-S-POROČNIM-BLOKOM-KADARKOLI (preglasi-h2-P240!) · PEZDIRC-×5-vpisov (v9-OBA!) · BRINC/BRINEC-mreža-v13-vdova-48-let! · DRAGOŠ-nit-v8 · Jakopič-križ-v15×v16 · foliacija-s45-'93/94'-[~X-OPEN!]. Dokaz: parish-marriage-1882-04455.json; skripte p241.",
      "P241: THE PARISH OF PODZEMELJ — THE MARRIAGE-REGISTER-PREHISTORY 04455, THE YEAR 1882 = 4/13 (issue #18): s45–s50 (6 spreads; 26 entries of 1882 counted from the number-column-1.–26.-NO-skips-the-4th-year-in-a-row!-in-contrast-to-the-1885-entry-3!) · THE-1882-RESTART = s45 (the-BIG-'1882'-HEADING-BEFORE-row-1-NOT-in-the-page-head!-a-NEW-4th-BOUNDARY-VARIANT!) · the-1881/82-boundary = s44→s45-heading · the-1882/83-boundary = s50-MID (P240-1:1!) · numbering s45=1–4 · s46=5–8 · s47=9–12 · s48=13–17 · s49=18–23 (the-nodat-strips-×5!) · s50-tail=24–26 — 7-GRIBLJE-blocks [35,38,56,13,8,1,36] (3-FULL ×2!) · ★★★★★ h1 = THE-LOWEST-HOUSE-WITH-A-MARRIAGE-BLOCK-EVER (it-supersedes-the-h2-P240!) · PEZDIRC-×5-entries (v9-BOTH!) · the-BRINC/BRINEC-network-v13-widow-48-y! · the-DRAGOŠ-thread-v8 · the-Jakopič-cross-v15×v16 · the-foliation-s45-'93/94'-[~X-OPEN!]. Evidence: parish-marriage-1882-04455.json; scripts p241.",
      p241Errors.length === 0,
      p241Errors.length === 0
        ? `poročna-1882: 26-vpisov/BREZ-preskokov-4.-leto! · 7-Griblje-blokov-[35,38,56,13,8,1,36]-3-POLNA-×2! · ★★★★★ h1 = najnižja-hiša-s-poročnim-blokom-KADARKOLI (preglasi-h2-P240!) · restart-s45-glava-PRED-vrstico-1-NOVA-4.-mejna-varianta! · PEZDIRC-×5 (v9-OBA-Georg-×-Margaretha!) · BRINC/BRINEC-v13-vdova! · Jakopič-križ-v15×v16! · h36-P240-napoved-IZPOLNJENA! · foliacija-'93/94'-[~X-OPEN] · MILIČ-križ-×237-nespremenjen (nobenega-v-1882!)`
        : p241Errors.join("; "),
    );
  }

'''

text = text.replace(anchor, BLOCK + anchor, 1)
with open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(text)
print('OK: qa-p241 blok vstavljen')
