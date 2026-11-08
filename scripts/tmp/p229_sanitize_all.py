#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P229 — INSERT qa-p229 + sanitizacija (1819→1853, 04104=167→187, yearset-04104-{1877..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p228: KRSTNA PREDZGODOVINA 04104 — leto 1878 = 8/15"
assert src.count(ANCHOR) == 1 and "qa-p229-parish-baptism-1877-04104" not in src

BLOCK = '''
  // ——— qa-p229: KRSTNA PREDZGODOVINA 04104 — leto 1877 = 9/15
  //      (P228: 1878 = 8/15!). 1877 = 108 vpisov-DISTINCT (LEAD-KOREKCIJA-9.×-linija! P228-LEAD-'1877 = 91'-NAPAČNA!
  //      vrstna-aritmetika 5+7+8+9+7+8+9+7+8+8+7+6+7+6+6 = 108 + zap-stolpci-VIDNI-×6-strani-1:1!) /
  //      20-GRIBLJE / 18-hiš (h6-×2 + h14-×2-DVOJČKI-bracket!) + ★★★ MEJA-1876/77-s78-ENE-STRANI
  //      (TAIL-1876 + glava-'Jahr 1876' + 'Incipit-annus-Domini-1877'-VELIKA-KALLIGRAFIJA-1.-INCIPIT-v-krstni-liniji!
  //      + RESTART-z1-NA-DAN-9./10.-JÄNNER-Zemelj-h20!-9.-restart-z1!) = 68.-POTRDITEV +
  //      ★★★ DVOJČKI-×4-REKORD (z28/z29-Prilozje! + z46/z47-Grem! + z67/z68-GRIBLJE-h14-'Zwillings'-nota! + z75/z76-Krasine!) +
  //      ★★★ TODTGEBOREN-TIP-garble-×3 (z41-'Nurlygaburišt'! + z42-'Tuolynbuns'-hišna-PRAZNA! + z65-Kloster-h43!-P228-z28-PARALELA!) +
  //      ★★★ PEZDIRC-×11-vrstic-continuum-9-let (z8-DVOJNI!) + ★★★ November-31-DUEL-×2 (z89-GRIBLJE! + z90!-Nov-31-NE-OBSTAJA!) +
  //      ★★★ RETRO-VPISI-×2 (z97/z98-Nov-29/30-NA-s91-PO-Dec-28/29!) + ★★★ z22-PREČRTANA-VELIKI-X + z15-Feb28→Mar1 +
  //      ★★★ DUHOVNIŠKA-IZMENJAVA ('Hoggin/Hoggja/Roggja'-KURRENT-DUEL-DOMINANTA ↔ Dovgan!) + MODRI-×9 (z8-MATCH-h37!-z27-TORONTO!) +
  //      črnilo-×2-Griblje (z56-†30.4.19?0! + z94-†6.3.1945!). Dokaz: parish-baptism-1877-04104.json; skripte p229.
  {
  const p229Errors: string[] = [];
  const p229Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1877);
  if (p229Bapt.length !== 20)
    p229Errors.push(`bloki 1877 (04104) ≠ 20 (${p229Bapt.length} — 20 Griblje-vpisov / 18-hiš (h6-×2 + h14-×2!) / 108-DISTINCT = LEAD-KOREKCIJA!)`);
  if (HOUSE_VITALS.length !== 1853)
    p229Errors.push(`HOUSE_VITALS ≠ 1853 (${HOUSE_VITALS.length} — P228: 1819; P229: + 20 blokov 1877-04104 = 1853!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 187)
    p229Errors.push(`bloki 04104 ≠ 187 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P228: 167; P229: + 20 × 1877 = 187!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p229Errors.push("04104-bloki izven {1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-9/15: 1877–1885-do-P230!)");
  if (!p229Bapt.some((h) => h.whatSi.includes("68.-POTRDITEV")))
    p229Errors.push("★★★ MEJA-1876/77-s78-ENE-STRANI (Incipit-annus-Domini-1877-KALLIGRAFIJA! + RESTART-z1-9./10.-JÄNNER!) ni označena");
  if (p229Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 7)
    p229Errors.push(`★★★ PEZDIRC-×7-Griblje ni dosežen (${p229Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/7!)`);
  if (!p229Bapt.some((h) => h.whatSi.includes("PEZDIRC-DVOJNI-vrstica")))
    p229Errors.push("★★★ PEZDIRC-DVOJNI-vrstica (z8-oče+botra!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("DVOJČKI-×1-GRIBLJE")))
    p229Errors.push("★★★ DVOJČKI-×1-GRIBLJE (z67/z68-h14-bracket-'Zwillings'-nota!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("JAKOFČIČ-DVOJNI-vrstica")))
    p229Errors.push("★★★ JAKOFČIČ-DVOJNI-vrstica (z85-oče+matec!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("PREČRTANA-VRSTICA-GRIBLJE")))
    p229Errors.push("★★★ z22-PREČRTANA-VELIKI-X-ČRNILO (oče-SWAP-'Samuel-Štua'!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("DATUMSKI-DUEL-Feb28→Mar1")))
    p229Errors.push("★★★ z15-DATUMSKI-DUEL-Feb28→Mar1 (rojen≠krsten-ČEZ-MESEC!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("November-31-DUEL")))
    p229Errors.push("★★★ z89-November-31-DUEL (Nov-31-NE-OBSTAJA!-z90-PARALELA-×2!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("MODRI-MATCH-h37")))
    p229Errors.push("★★★ MODRI-MATCH-h37 (z8-'umrla-21.4.1961-št.37'!) ni označena");
  if (p229Bapt.filter((h) => h.whatSi.includes("črnilo-")).length < 2)
    p229Errors.push(`★★★ črnilo-pripisi-×2-Griblje (z56-†30.4.19?0! + z94-†6.3.1945!) ni dosežen (${p229Bapt.filter((h) => h.whatSi.includes("črnilo-")).length}/2!)`);
  if (!p229Bapt.some((h) => h.whatSi.includes("HRIŽAN-DVOJNI-vrstica")))
    p229Errors.push("★★★ HRIŽAN-DVOJNI-vrstica (z99-oče+matec!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("BRODARIČ-oče")))
    p229Errors.push("★★★ BRODARIČ-oče (z94!-6/6-KOMPLET-nit!) ni označena");
  if (!p229Bapt.some((h) => h.whatSi.includes("SIMEC-boter")))
    p229Errors.push("★★★ SIMEC-boter-nit (z61/z99-3/3-KOMPLET!) ni označena");
  if (new Set(p229Bapt.map((h) => h.houseNo)).size !== 18)
    p229Errors.push(`★★★ 18-hiš-DISTINCT ni izpolnjeno (h6-×2 + h14-×2! — najdeno ${new Set(p229Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p229-parish-baptism-1877-04104",
    "P229: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1877 = 9/15 (issue #18): okvir — s78–s92 (15 skenov; 2×-neodvisna-prenosa-md5-15/15!-s92-kopija-P228!; s85–s92-proba-P228-LEAD!-s78–s84-probe-nazaj!-s78-MEJA-ENE-STRANI!) + **gola-svinčna-pag-'sken−5'-15/15-SEKVENČNO** (s78='73'/s79='74'/s80='75'/s81='76'/s82='77'/s83='78'/s84='79'/s85='80'-LEAD-PREDIKCIJA-POTRJENA!/s86='81'/s87='82'/s88='83'/s89='84'/s90='85'/s91='86'/s92='87'-P228! — SKUPNA-SERIJA-73–158-continuum!) + **★★★ MEJA-1876/77 = s78-ENE-STRANI (TAIL-1876-r1-Dobravce-Martin-Dez-24/26-h16-Hržnić[?]/Rus + glava-'Jahr 1876'! + 'Incipit-annus-Domini-1877'-VELIKA-KALLIGRAFIJA-ČEZ-SREDINO-STRANI-1.-INCIPIT-v-krstni-liniji! + glava-'Jahr 1877-Jänner' + RESTART-z1-NA-DAN-9./10.-JÄNNER-Zemelj-h20-Catharina-Škatab[?]/Jurejčič[?]-DUEL!-9.-restart-z1-linija!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!-P229-9./10.!) = 68.-POTRDITEV-invariante! (67.-P228!)** + **★★★ 108-VPISOV-DISTINCT — LEAD-KOREKCIJA-9.×-linija (P228-LEAD-'1877 = 91-vpisov-pričakovano'-NAPAČNA!-predpostavka-tail-'z86–z91'!) — vrstna-aritmetika 5+7+8+9+7+8+9+7+8+8+7+6+7+6+6 = 108 + zap-stolpci-VIDNI-×6-strani-1:1 (s78:1–5!-s79:6–12!-s80:13–20!-s81:21–29!-s82:30–36!-s83:37–44!) = NOV-REKORD-POTRDITEV-zap-1:1!** + **★★★ 20-GRIBLJE / 18-hiš (h6-×2: z13-Feb-24-JAKOFČIČ + z56-Juli-23-KLOBUČAR!-RAZLIČNI-starši! + h14-×2: z67+z68-DVOJČKI-bracket-'Zwillings'-nota!): z8-h37-PEZDIRC-DVOJNI!-MODRI-MATCH! + z13-h6-JAKOFČIČ!-MODRI-dolg! + z15-h13-JAKOFČIČ!-Feb28→Mar1! + z22-h36-PREČRTANA-X! + z25-h65-MILEK! + z34-h74-HAMBIČ! + z56-h6-KLOBUČAR!-†-črnilo! + z61-h7-SIMEC! + z67/z68-h14-PEZDURE-DVOJČKI! + z77-h2-JAKOFČIČ-matec! + z79-h35-HRIŽAN! + z84-h20-PEZDIRC! + z85-h9-JAKOFČIČ-DVOJNI!-DRAGOŠ! + z89-h40-Nov31-DUEL! + z94-h49-BRODARIČ-oče!-†6.3.1945! + z95-h78-BRODARIČ! + z99-h3-HRIŽAN-DVOJNI!-SIMEC! + z101-h34-DUEL! + z106-h33-DEBLIČ!-P228-TAIL!** + **★★★ PEZDIRC-×11-vrstic-continuum-9-let (×4/×4/×6/×4/×9/×14/×12/×17/×11!-z8-DVOJNI-Griblje!-×7-Griblje + ×4-ne-Griblje!)** + JAKOFČIČ-×11 (z85-DVOJNI!-z31-TRIJNI-neG!) + MILEK-×5-vse-Griblje + BRODARIČ-×6-Griblje-KOMPLET + KLOBUČAR-×4 + DEBLIČ-×4 + HRIŽAN-×5 (z99-DVOJNI!) + SIMEC-×3-KOMPLET + DRAGOŠ-×1 + HURE-×2-neG + HAMBIČ-×4 + **★★★ DVOJČKI-×4-REKORD-LINJE (z28/z29-Prilozje-h30-bracket! + z46/z47-Grem-h26-bracket-mesec-'Juni'-Kurrent-'Nai/Mai'-DUEL! + z67/z68-GRIBLJE-h14-bracket-'Zwillings'-vertikalna-nota! + z75/z76-Krasine-h18-bracket-†11.3.1939-ink!-vs-×3-P227!-×2-P228!)** + **★★★ TODTGEBOREN-TIP-garble-×3-REKORD (z41-Krasine-h11-'Nurlygaburišt'[?]-garble-MAX! + z42-Podzemelj-HIŠNA-PRAZNA-'Tuolynbuns'[?]-garble-MAX! + z65-Kloster-h43-'Nurlygabuništ'[?]-garble-MAX!-botra+duhovnik(+hebamme)-VSI-PRAZNI!-P228-z28-'Nrbžgabumšt'-1:1-GARBLE-DRUŽINA!)** + **★★★ NEZAKONSKI-×4 (z38-Krasine-h46-oče-dash-PRAZEN!-+popravek-'al-46'-nad-hišno! + z43-Certovišče-h14-oče-PRAZEN! + z44-Vranoviče-h20-X-open-samo-matec-Agnes-Hönig!-vs-×5-P228!)** + **★★★ DUHOVNIŠKA-IZMENJAVA-1877 ('Ferdinand-Hoggin/Hoggja/Roggja-coop'-KURRENT-DUEL-podpis-3-grafične-variante-ISTI-duhovnik-X-open!-DOMINANTA-~×30! ↔ 'Franz-Dovgan'~×20!-ALTERNIRAJÖČE-čez-celo-leto!-Griblje-split-HOGGIN-×13/DOVGAN-×7!)** + **★★★ November-31-DUEL-×2 (z89-GRIBLJE-h40! + z90-Dragoše-h1!-Nov-31-NE-OBSTAJA-pisarjev-slip-za-Nov-30/Dec-1!-×2-ZAPOREDOMA!)** + **★★★ RETRO-VPISI-×2 (z97-z98-Nov-29/30-NA-STRANI-s91-PO-s90-Dec-28/29!-nakadna-dopolnitev-chronologije!-z97-Dragoše-Joannes-†19/3-1919-črnilo! + z98-Goriče-Nicolaus!)** + **★★★ z22-PREČRTANA-VRSTICA-GRIBLJE (veliki-X-črnilo-čez-IME+'legitimaha-že'+pripis!-1.-v-GRIBLJI! + OČE-PREČRTAN-SWAP-'Samuel-Štua'-X-open!)** + **★★★ z15-DATUMSKI-DUEL-Feb28→Mar1-GRIBLJE (rojen≠krsten-ČEZ-MESEC!-1877-NON-LEAP!-krop-potrjeno!)** + **★★★ MODRI-MATIČARSKI-PRIPISI-×9 (z8-'umrla-21.4.1961-gribljskih-št.37'-MATCH-h37! + z13-dolg-'†27.1.1963-Gribljah'+'o.23/1.1910'! + z22-'†20.I.1912-Podgoricah[?]'-X-open! + z27-'†15.marja-1959-Novem-mestu-TORONTO-KANADA'-matičar! + z28-'Amor-Anžan-Lav.'-modra-vertikala! + z40-dolg-'†6.12.1960-Gradacu'-MMK! + z43-'†23.12.1953-Letrjači[?]-št.20'-DUEL-1943/1953! + z18-dolg-Kaplišče-MMK-Otok-1964! + tail-z87-'†6.4.1945'-P228!)** + **★★★ črnilo-pripisi-×2-Griblje (z56-'†30.4.19?0-v-Gribljah'-X-open-1940/1950! + z94-'†6.3.1945'-s-križem-P228-z87-'†6.4.1945'-PARALELA!)** + ne-G-črnilo (z2-†3.1.1931! + z3-†19.4.1940+Jannen-15.2.1897! + z32-†-vertikalno-čez-IME! + z85-'copulatus-in-Zagreb-25.6.1916'! + z97-†19/3-1919! + z79-†22.2.1937! + z74-†11.3.1939-vertikalno!) + HEBAMME-Maria-Rom/Born-×7-continuum (z39/z40/z43/z45/z48/z63/z65!) + rojen≠krsten-Griblje-×10 (z8-30/31! + z15-28/1! + z25-29/30! + z56-23/24! + z67/z68-31/1-×2! + z77-5/6! + z84-22/23! + z85-23/24! + z89-31/1!) + RED-tički-✓-margin + meseci-Griblje: J1+F3+M2+A1+Juli1+A3+O2+N3+D5 = 20 (Juni/Sep-×0!-2-prazne!) + **20 NOVIH BLOKOV parish.ts: vitals 1819 → 1853 · 04104 = 167 → 187 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p229 (fetch-2×-md5-15/15 + VIZUALNO-arhivar-branje-×15!-API-429-override + krops-56-sheet-×8 (Griblje-×20 + dueli-×6 + dvojčki-×4 + todtgeboren-×3 + nezakonski-×3 + MEJA + Incipit + restart + foliacija-×15 + zap-×6 + Nov31-DUEL-×2 + retro-×2 + Feb28→Mar1 + hišna-DUEL) + build-entries + build-proof) + qa-p229 (229. kontrola!) + dokaz parish-baptism-1877-04104.json (108-DISTINCT: 20-Griblje + 88-druge! anomalije/crossChecks/honesty!) + pt-luknja-187/1853; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-9/15-LET!** (P230-LEAD: 1876 — MEJA-1876/77-ŽE-NAJDENA-s78-ENE-STRANI → 1876 = TAIL-s78-r1-Dobravce-Dez-24/26! → MEJA-1875/76-pred-s78 → probe-s71–s78-DESCENDING! — gola-pag-'sken−5'-pričakovana-s71='66'! (s78='73'!))",
    "P229: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1877 = 9/15 (issue #18): the-frame — s78–s92 (15 scans; 2×-INDEPENDENT-md5-15/15!) + the-plain-pencil-pag-'scan−5'-15/15-SEQUENTIAL (s85='80'-THE-LEAD-PREDICTION-CONFIRMED!-73–158-continuum!) + **★★★ THE-1876/77-BOUNDARY = s78-SINGLE-PAGE (the-TAIL-1876-Dobravce-Dez-24/26 + the-'Jahr 1876'-header! + 'Incipit-annus-Domini-1877'-THE-GREAT-CALLIGRAPHY-ACROSS-THE-MIDDLE-OF-THE-PAGE-THE-1st-INCIPIT-IN-THE-BAPTISM-LINE! + the-'Jahr 1877-Jänner'-header + the-RESTART-z1-ON-DAY-9./10.-JÄNNER-Zemelj-h20!-the-9th-restart-z1!) = the-68th-CONFIRMATION!** + **★★★ 108-ENTRIES-DISTINCT — THE-LEAD-CORRECTION-9th-TIME (the-P228-LEAD-'1877 = 91'-WRONG!-the-row-arithmetic 5+7+8+9+7+8+9+7+8+8+7+6+7+6+6 = 108 + the-zap-columns-VISIBLE-×6-pages-1:1 = THE-NEW-RECORD-zap-1:1-CONFIRMATION!)** + **★★★ 20-GRIBLJE / 18-houses (h6-×2 + h14-×2-the-TWINS-bracket!)** + **★★★ THE-PEZDIRC-×11-ROWS-CONTINUUM-9-YEARS (the-z8-DOUBLE!)** + JAKOFČIČ-×11 + MILEK-×5 + BRODARIČ-×6 + KLOBUČAR-×4 + DEBLIČ-×4 + HRIŽAN-×5 + SIMEC-×3 + **★★★ THE-TWINS-×4-RECORD (z67/z68-GRIBLJE-'Zwillings'-vertical-note!-vs-×3-P227!)** + **★★★ THE-STILLBORN-TIP-GARBLE-×3-RECORD (z41-'Nurlygaburišt'! + z42-'Tuolynbuns'-THE-HOUSE-EMPTY! + z65-Kloster!-the-P228-z28-1:1-GARBLE-FAMILY!)** + **★★★ THE-ILLEGITIMATE-×4** + **★★★ THE-PRIEST-ALTERNATION-1877 ('Ferdinand-Hoggin/Hoggja/Roggja-coop'-THE-KURRENT-DUEL-SIGNATURE-THE-DOMINANT! ↔ 'Franz-Dovgan'-ALTERNATING!)** + **★★★ THE-NOVEMBER-31-DUEL-×2 (Nov-31-DOES-NOT-EXIST-THE-SCRIBAL-SLIP-for-Nov-30/Dec-1!)** + **★★★ THE-RETROACTIVE-ENTRIES-×2 (z97/z98-Nov-29/30-ON-THE-PAGE-AFTER-Dec-28/29!)** + **★★★ THE-z22-CROSSED-OUT-ROW-GRIBLJE (the-big-X-ink! + the-FATHER-CROSSED-SWAP!)** + **★★★ THE-z15-DATE-DUEL-Feb28→Mar1 (born≠baptized-ACROSS-THE-MONTH!)** + **★★★ THE-BLUE-ANNOTATIONS-×9 (z8-MATCHING-h37! + z27-TORONTO-CANADA!)** + **★★★ THE-INK-ANNOTATIONS-×2-GRIBLJE (z56-†30.4.19?0! + z94-†6.3.1945!)** + **20 NEW BLOCKS: the vitals 1819 → 1853 · the 04104 = 167 → 187**; the scripts p229 + qa-p229 (the 229th check!) + the evidence parish-baptism-1877-04104.json (108-DISTINCT: 20-Griblje + 88-others!) + the pt-gap-187/1853; **★★★ THE-BAPTISM-PREHISTORY-LINE-9/15-YEARS!** (the P230-LEAD: 1876 — the-boundary-1876/77-ALREADY-FOUND-s78-SINGLE-PAGE → the-TAIL-s78-r1-Dobravce-Dez-24/26! → probe-s71–s78-DESCENDING!)",
    p229Errors.length === 0,
    p229Errors.length === 0
      ? `20 vpisov / 108-DISTINCT (LEAD-KOREKCIJA-'91'→'108'!-zap-1:1-×6-strani!) / 18-hiš (h6-×2 + h14-×2-DVOJČKI!) · MEJA-1876/77-s78-ENE-STRANI-68.-POTRDITEV ('Incipit-annus-Domini-1877'-KALLIGRAFIJA!-RESTART-z1-9./10.!-9.-restart!) · FOLIACIJA-sken−5-15/15 (s85='80'-LEAD-POTRJENA!-73–158!) · PEZDIRC-×11-continuum-9-let (z8-DVOJNI!) · DVOJČKI-×4-REKORD · TODTGEBOREN-TIP-×3-REKORD ('Nurlygaburišt'-družina!) · NEZAKONSKI-×4 · DUHOVNIKI-'Hoggin/Hoggja/Roggja'-DUEL ↔ Dovgan · Nov31-DUEL-×2 · RETRO-VPISI-×2 · z22-PREČRTANA-X · z15-Feb28→Mar1 · MODRI-×9 (MATCH-h37!-TORONTO!) · črnilo-×2 (†6.3.1945!) · meseci-Juni/Sep-×0 · **LINIJA-9/15!** · vitals 1853 · 04104 187`
      : p229Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1819", "HOUSE_VITALS.length !== 1853")
# P228-block 04104-total: 167 → 187 (zdaj vključuje 1877!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 167)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 187)')
src = src.replace('p228Errors.push(`bloki 04104 ≠ 167 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878 = 167!)`)',
                  'p228Errors.push(`bloki 04104 ≠ 187 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877 = 187!)`)')
# yearset-04104: {1878..1885} → {1877,...,1885} (v P228-, P227-, P226-, P225-blokih!)
old_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
new_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
n_y = src.count(old_yearset)
src = src.replace(old_yearset, new_yearset)
for ph in ("p228Errors", "p227Errors", "p226Errors", "p225Errors"):
    src = src.replace(f'{ph}.push("04104-bloki izven {{1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-8/15: 1878–1885-do-P229!)");',
                      f'{ph}.push("04104-bloki izven {{1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-9/15: 1877–1885-do-P230!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1853×{src.count('HOUSE_VITALS.length !== 1853')} · qa-p229×{src.count('qa-p229-parish-baptism-1877-04104')} · yearset-patched-{n_y}")

# --- skripte + verifierji patch (1819→1853, 167→187) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p229_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1819" not in t: continue
    o = t
    t = t.replace("1819", "1853")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p229" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1819", "vitals == 1853"), ("vitalsTotal == 1819", "vitalsTotal == 1853"),
                 ('vitalsTotal"] == 1819', 'vitalsTotal"] == 1853'),
                 ('"vitalsTotal": 1819', '"vitalsTotal": 1853'),
                 ('\\"vitalsTotal\\": 1819', '\\"vitalsTotal\\": 1853'),
                 ('!== 1819"', '!== 1853"'),
                 ("1819-številcev", "1853-številcev"),
                 ("vitals-števec-1819", "vitals-števec-1853"), ("vitals-1819", "vitals-1853")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 167 → 187
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 167}', '"04104": 187}')
t = t.replace("# POSODABLJENO P228: + krstna-04104 = 167 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228!)",
              "# POSODABLJENO P229: + krstna-04104 = 187 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (187)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1853
pt["corpus"]["byBook"]["04104"] = 187
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P229: +20-blokov-1877-krstna-04104-9/15 (vitals 1819→1853; 04104 167→187; 108-DISTINCT = LEAD-KOREKCIJA-'91'→'108' + zap-1:1-×6-strani + 20-GRIBLJE/18-hiš (h6-×2 + h14-×2!) + MEJA-1876/77-s78-ENE-STRANI-68.-POTRDITEV ('Incipit-annus-Domini-1877'-KALLIGRAFIJA!-RESTART-z1-9./10.!-9.-restart!) + FOLIACIJA-sken−5-15/15 (s85='80'-LEAD-POTRJENA!-73–158!) + DVOJČKI-×4-REKORD + TODTGEBOREN-TIP-×3-REKORD ('Nurlygaburišt'-družina!) + Nov31-DUEL-×2 + RETRO-VPISI-×2 + z22-PREČRTANA-X + z15-Feb28→Mar1 + MODRI-×9 (MATCH-h37!-TORONTO!) → P230-LEAD-1876)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
