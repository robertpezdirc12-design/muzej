#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P231 — INSERT qa-p231 + sanitizacija (1853→1870, 04104=201→218, yearset-04104-{1875..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p230: KRSTNA PREDZGODOVINA 04104 — leto 1876 = 10/15"
assert src.count(ANCHOR) == 1 and "qa-p231-parish-baptism-1875-04104" not in src

BLOCK = '''
  // ——— qa-p231: KRSTNA PREDZGODOVINA 04104 — leto 1875 = 11/15
  //      (P230: 1876 = 10/15!). 1875 = 119 vpisov (z1–z115-Jan–Nov + TAIL-z1–z4-LOKALNI-RESTART-Dez-NOVA-VARIANTA!-
  //      aritmetika 3+9+8+9+9+9+9+7+7+7+7+8+8+7+8+4 = 119 + zap-stolpec-NEZAPISAN-s47–s63-starša-forma!-z100-MILESTONE-s59-r8-TODGEBORENE[?]-garble!) /
  //      17-GRIBLJE / 16-hiš (h48-×2-DUEL-z4-'48[~18]'-NEZ!-vs-z93-KLOBUČAR!) + ★★★ MEJA-1874/75-s47-SREDI-PAGI-NOVA-VARIANTA-3.-mejna-varianta-zaporedoma
  //      (TAIL-1874-Dez-26–31-×5-vrstic!-GRIBLJE-h22+μh65-MILEK-×2-Dovgan! + 'Jänner'-VELIKA-PRELIM + veliki-cifri-'1'+'8'-VSOTNA-razpeto[?]-X-open! +
  //      RESTART-z1-9./9.-JÄNNER-Dobravce-h20!-11.-restart!) = 70.-POTRDITEV + ★★★ BREZ-'finis-Anni-1874'-kalligrafije (leto-končano-SREDI-PAGI!) +
  //      ★★★ TROJNI-DUPLIKAT-SKENOV-folio-57 (s60=s61=s62!-NOVO-ODKRITJE!-sken−3-42–57!-+sken−5-s63/s64!) + ★★★ TAIL-1874-zap-72–87-VIDEN-×2-strani +
  //      ★★★ PEZDIRC-×5-NAJNIŽJA-linije-continuum-11-let (×3-Griblje!) + ★★★ NEZAKONSKI-×2-GRIBLJE + ★★★ MODRI-×4-Griblje-† (†1933/1940/1946/1948!) +
  //      ★★★ VIOLET-RETRO-VPIS-z6-datiran-'vom-11.-October-1875'-NOVI-TIP! + ★★★ FEBER-1-PRELIM-BREZ-DATUMA-s48-r9! + ★★★ DUHOVNIKI-DOVGAN-×10/HOGGIA-×7.
  //      Dokaz: parish-baptism-1875-04104.json; skripte p231.
  {
  const p231Errors: string[] = [];
  const p231Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1875);
  if (p231Bapt.length !== 17)
    p231Errors.push(`bloki 1875 (04104) ≠ 17 (${p231Bapt.length} — 17 Griblje-vpisov / 16-hiš-h48-DUEL! / 119-vpisov!)`);
  if (HOUSE_VITALS.length !== 1870)
    p231Errors.push(`HOUSE_VITALS ≠ 1870 (${HOUSE_VITALS.length} — P230: 1853; P231: + 17 blokov 1875-04104 = 1870!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 218)
    p231Errors.push(`bloki 04104 ≠ 218 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P230: 201; P231: + 17 × 1875 = 218!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p231Errors.push("04104-bloki izven {1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-11/15: 1875–1885-do-P232!)");
  if (!p231Bapt.some((h) => h.whatSi.includes("70.-POTRDITEV")))
    p231Errors.push("★★★ MEJA-1874/75-s47-SREDI-PAGI-NOVA-VARIANTA (TAIL-1874! + 'Jänner'-PRELIM + veliki-cifri-'1'+'8'! + RESTART-z1-9./9.!-11.-restart!) ni označena");
  if (p231Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 3)
    p231Errors.push(`★★★ PEZDIRC-×3-Griblje ni dosežen (${p231Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/3!)`);
  if (!p231Bapt.some((h) => h.whatSi.includes("PEZDIRC-boter-nit")))
    p231Errors.push("★★★ PEZDIRC-boter-nit (z29-h33!) ni označena");
  if (p231Bapt.filter((h) => h.whatSi.includes("NEZAKONSKI")).length < 2)
    p231Errors.push(`★★★ NEZAKONSKI-×2-GRIBLJE ni dosežen (${p231Bapt.filter((h) => h.whatSi.includes("NEZAKONSKI")).length}/2!)`);
  if (!p231Bapt.some((h) => h.whatSi.includes("'ledig.'")))
    p231Errors.push("★★★ 'ledig.'-materina-NOTA (z4-h48!) ni označena");
  if (p231Bapt.filter((h) => h.whatSi.includes("MODRI")).length < 4)
    p231Errors.push(`★★★ MODRI-×4-Griblje ni dosežen (${p231Bapt.filter((h) => h.whatSi.includes("MODRI")).length}/4!)`);
  if (!p231Bapt.some((h) => h.whatSi.includes("HRIŽAN-boter-DVOJNI")))
    p231Errors.push("★★★ HRIŽAN-boter-DVOJNI (z2-h30-Nicolaus+Rosa!) ni označen");
  if (!p231Bapt.some((h) => h.whatSi.includes("SIMEC-oče-nit")))
    p231Errors.push("★★★ SIMEC-oče-nit (z57-h38-X2-potrjen!) ni označen");
  if (!p231Bapt.some((h) => h.whatSi.includes("KLOBUČAR-oče-nit")))
    p231Errors.push("★★★ KLOBUČAR-oče-nit (z93-h48!) ni označen");
  if (!p231Bapt.some((h) => h.whatSi.includes("URH-oče-nit")))
    p231Errors.push("★★★ URH-oče-nit (z98-h68-KOMPLET!) ni označen");
  if (!p231Bapt.some((h) => h.whatSi.includes("GOZEK-DVOJNI-nit")))
    p231Errors.push("★★★ GOZEK-DVOJNI-nit (z98-h68-matec+botra!) ni označena");
  if (!p231Bapt.some((h) => h.whatSi.includes("TAIL-RESTART-z1–z4-LOKALNI")))
    p231Errors.push("★★★ TAIL-RESTART-z1–z4-LOKALNI-NOVA-VARIANTA (z3t-h11!) ni označena");
  if (new Set(p231Bapt.map((h) => h.houseNo)).size !== 16)
    p231Errors.push(`★★★ 16-hiš-DISTINCT (h48-×2-DUEL!) ni izpolnjeno (najdeno ${new Set(p231Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p231-parish-baptism-1875-04104",
    "P231: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1875 = 11/15 (issue #18): okvir — s45–s64 (20 skenov; s45–s47-TAIL-1874 + s47-SREDI-PAGI-MEJA! + s48–s64-1875!-DESCENDING-probe-P230-LEAD-s57–s64-RAZŠIRJEN-na-s45–s56!-2×-neodvisna-md5-20/20!) + **★★★ TROJNI-DUPLIKAT-SKENOV-folio-57-NOVO-ODKRITJE (s60=s61=s62-VIZUALNO-1:1-isti-razpon-November-3–20!-3-različnih-md5!-prilepljeni-listi-na-3-položajih!) + FOLIACIJA-s45–s60-'sken−3'-SEKVENČNO (42–57!-15/15-visoko-zanesljivost!) + s63='58'/s64='59'-'sken−5'-P230!-2-DUPLIKATA-PRED-s45-neznana-lokacija-s1–s44!** + **★★★ MEJA-1874/75 = s47-SREDI-PAGI-NOVA-VARIANTA-3.-mejna-varianta-zaporedoma (vs-P230-DVO-STRANSKA!-vs-P229-ENO-STRANSKA!): s47-r1–r5 = TAIL-1874 (Dez-26/26-Dobravce-h13! + Dez-26/27-Krasine-h10! + Dez-28/28-GRIBLJE-h22-Maria-MILEK+PEZDIRE-Dovgan! + Dez-28/29-GRIBLJE-h65-Maria-MILEK+Harasinič! + Dez-31/31-Certoviše-h11-'izvršena-4.3.1953-dekret-št.9'-MODRI!) + 'Jänner'-VELIKA-PRELIM + veliki-cifri-'1'+'8'-VSOTNA-'1[8][7][5]'-razpeto[?]-X-open! + RESTART-z1-9./9.-JÄNNER-Dobravce-h20-Nicolaus-Rus-MODRI-umrl-2.1.1953! = 70.-POTRDITEV-invariante (69.-P230!-11.-restart-z1-linije!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!-P229-9./10.!-P230-5./5.!-P231-9./9.!-najpoznejši-TIE-P229!) + ★★★ BREZ-'finis-Anni-1874'-KALLIGRAFIJE (P230-LEAD-'lahko-se-ponovi'-PREVERJENO-NI!-leto-končano-SREDI-PAGI-kalligrafija-ni-mogoča!) + GLAVE-'Jahr 1874'-×3/'Jahr 1875'-×14-glava-NI-meja! | s64-TAIL-1875 + TAIL-RESTART-z1–z4-LOKALNI-NOVA-VARIANTA + 'finis-Anni-1875'-KALLIGRAFIJA-P230!** + **★★★ 119-VPISOV (z1–z115-Jan–Nov + TAIL-z1–z4-Dez!-aritmetika 3+9+8+9+9+9+9+7+7+7+7+8+8+7+8+4 = 119!-z100-MILESTONE-s59-r8-Nov-3-Krasinec-h22-TODGEBORENE[?]-garble-P229-DRUŽINA-PARALELA!) + zap-stolpec-NEZAPISAN-s47–s63-starša-forma (vs-P230-×6-strani-VIDNI!) + TAIL-1874-zap-72–87-VIDEN-×2-strani (s45-z72–z79!-s46-z80–z87!-1874-sklenjen-z~92!)** + **★★★ 17-GRIBLJE / 16-hiš (h48-×2-DUEL-z4-'48[~18-DUEL]'-NEZ-Straus!-vs-z93-KLOBUČAR!-RAZLIČNI-družini!): z2-h30-NEZ-HRIŽAN-boter-DVOJNI-Nicolaus+Rosa!-matec-'eg.-paroch.-Lipnik'-nota!-DOVGAN! + z4-h48-NEZ-'ledig.'-NOTA!-h48[~18]-DUEL!-Urih-boter! + z7-h5-STRUZEL-DVOJNI-oče+botra!-MODRI-umrla-24.5.1948-dolg!-Roggja-Coop! + z8-h28-MILEK-boter!-Jožek-DVOJNI! + z14-h34-DEBLIČ-matec-garble-DUEL!-Hoggjač-Coop! + z15-h37-HUSIČ-oče!-HAMBIČ-matec! + z16-h94-HAMBIČ-oče!-MILEK-boter-X1!-MODRI-†6.3.1946-+poroka-1925!-h94-NOVA! + z29-h33-PEZDIRC-boter!-DEBLIČ-oče!-BRODARIČ-botra!-X4-extended! + z36-h29-MILEK-oče!-HRIŽAN-matec! + z44-h64-PEZDIRC-matec!-WERBÖSER-garble! + z51-h72-DRAGOŠ-matec!-ŠKRANC-oče+boter-DVOJNI!-h72/42-DUEL! + z57-h38-SIMEC-oče-X2!-HRIŽAN-matec!-DRAGOŠ-boter!-MODRI-nota-5.9.1922!-mesec-DUEL-REŠEN-JULI! + z59-h57-LOGAR-oče!-HARASINIČ-matec!-BRODARIČ-botra!-row-DUP-halucinacija-ZAVRNJENA! + z93-h48-KLOBUČAR-oče!-BRODARIČ-boter!-STRUZEL-botra!-MODRI-†28.XI.1940!-PEZDIRC?-matec-DUEL! + z98-h68-URH-oče!-GOZEK-DVOJNI-matec+botra!-LOGAR/LOZAR-ime-DUEL! + z111-h1-JAKOFČIČ-DVOJNI-matec+boter!-MODRI-†17.9.1933!-h1-NOVA! + z3t-h11-TAIL-DRAGOŠ-matec!-JAKOFČIČ-botra!-ŠIMEC-boter!-Hoggia-Coop!** + **★★★ PEZDIRC-×5-NAJNIŽJA-vrednost-linije-continuum-11-let (×4/×4/×6/×4/×9/×14/×12/×17/×11/×17/×5!-×3-Griblje-z29-boter!-z44-matec!-z93-matec[~DUEL]!-+×2-ne-G-z38-Boršt!-z46-Primostek-NEZ!-+TAIL-1874-×5!)** + MILEK-×4 + HRIŽAN-×6 + BRODARIČ-×5 + DRAGOŠ-×3-KOMPLET-continuum + JAKOFČIČ-×4 + DEBLIČ-×2 + HAMBIČ-×2-SOSEDNJI-VRSTICI + STRUZEL-×3 + URH-×2-KOMPLET + GOZEK-×2-DVOJNI + LOGAR/LOZAR-×2-ime-DUEL + ŠKRANC-×2-DVOJNI + ŠIMEC-×2 + KLOBUČAR-×1 + HUSIČ-×1 + **★★★ NEZAKONSKI-×2-GRIBLJE (z2! + z4!-oče-PRAZNO-×2!-+'ledig.'-nota!-vs-×6-P230-REKORD!)** + **★★★ MODRI-×4-Griblje-† (z7-umrla-24.5.1948-dolg! + z16-†6.3.1946-+poroka-1925! + z93-†28.XI.1940! + z111-†17.9.1933!-1933–1948!-+ne-G-×10!-+TAIL-1874-×3-incl.-CHICAGO-13.7.1949-military-service-record!-TAIL-CHICAGO-P230-CHICAGO-1970-PARALELA!)** + **★★★ VIOLET-RETRO-VPIS-z6-NOVI-TIP (s48-r3-Vranoviče-h19-Maria-Jän-24/25-vijolični-črnilo-+'vom-11.-October-[18]75-geschriben'-DATIRANI-retro-nota!-P230-RETRO-PARALELA!)** + **★★★ FEBER-1-PRELIM-BREZ-DATUMA (s48-r9-Gradac-h13-Anton-veliki-'Feber-1'-prelom-datumi-celici-PRAZNI!-Marenki/Nowall!-Dovgan!)** + ★★★ 11.-restart-z1-9./9.-JÄNNER + z100-MILESTONE-TODGEBORENE[?] + HEBAMME-Maria-Born[~Rom]-×2-continuum (s59-r7/r8!) + botra-PRAZNO-anomalija (s49-r1!) + rdeči-tički-continuum + **★★★ DUHOVNIŠKA-IZMENJAVA-1875 ('Hoggia/Roggja/Hoggin-Coop'-KURRENT-DUEL-continuum ↔ 'Franz-Dovgan'-ALTERNIRAJÖČE!-Griblje-split-DOVGAN-×10/HOGGIA-×7-vs-P230-7/7-IZENAČEN!-vs-P229-13/7!-TAIL-1874-'Rogej-Coop'-×3-varianta!)** + meseci-Griblje: J4+F3+M1+A1+Mai1+Juni1+Juli2+O2+N1+D1 = 17 (August+September-×0!-2-prazne!-vs-P230-3-prazne!) + **17 NOVIH BLOKOV parish.ts: vitals 1853 → 1870 · 04104 = 201 → 218 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p231 (fetch-2×-md5-20/20 + celostanska-branja-×15! + probe-glave/foliacije/dna-×2-sets + vrstični-krops-×18-sheetov + ločilni-krops-X1–X4! + build-entries + build-proof) + qa-p231 (231. kontrola!) + dokaz parish-baptism-1875-04104.json (119-vpisov: 17-Griblje + 102-druge! anomalije/crossChecks/honesty!) + pt-luknja-218/1870; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-11/15-LET!** (P232-LEAD: 1874 — MEJA-1874/75-ŽE-NAJDENA-s47-SREDI-PAGI!-TAIL-1874-ŽE-VLM-×5-vrstic-s47 + s45–s46-zap-72–87! → MEJA-1873/74-pred-s47 → probe-s38–s47-DESCENDING!-'sken−3'-pričakovana-s44='41'! (s47='44'!)-POZOR: TROJNI-DUPLIKATI-LAHKO-se-ponovijo!-1874-vpisov-pričakovano-~92 (zap-87-DO-Dez-22!))",
    "P231: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1875 = 11/15 (issue #18): the-frame — s45–s64 (20 scans; 2×-INDEPENDENT-md5-20/20!) + **★★★ THE-TRIPLE-DUPLICATE-SCANS-OF-FOLIO-57-THE-NEW-DISCOVERY (s60=s61=s62-VISUALLY-1:1-THE-SAME-SPREAD!-3-DIFFERENT-md5!) + THE-FOLIATION-s45–s60-'scan−3'-SEQUENTIAL (42–57!) + s63='58'/s64='59'-'scan−5'!** + **★★★ THE-1874/75-BOUNDARY = s47-MID-PAGE-THE-NEW-VARIANT-THE-3RD-BOUNDARY-VARIANT-IN-A-ROW (the-TAIL-1874-Dez-26–31-×5-rows!-incl.-GRIBLJE-×2! + the-'Jänner'-GREAT-BREAK + the-big-digits-'1'+'8'-the-VSOTNA-spread[?]-X-open! + the-RESTART-z1-9./9.-JÄNNER = the-70th-CONFIRMATION!-the-11th-restart!-WITHOUT-the-'finis-Anni-1874'-CALLIGRAPHY-the-year-ends-MID-PAGE!)** + **★★★ 119-ENTRIES (z1–z115 + the-TAIL-z1–z4-LOCAL-RESTART-THE-NEW-VARIANT!-the-z100-MILESTONE-TODGEBORENE[?]-garble!)** + **★★★ 17-GRIBLJE / 16-houses (h48-×2-DUEL!)** + **★★★ THE-PEZDIRC-×5-THE-LOWEST-VALUE-OF-THE-LINE-THE-CONTINUUM-11-YEARS** + MILEK-×4 + HRIŽAN-×6 + DRAGOŠ-×3 + **★★★ THE-ILLEGITIMATE-×2-GRIBLJE (the-'ledig.'-note!)** + **★★★ THE-BLUE-ANNOTATIONS-×4-GRIBLJE-† (1933/1940/1946/1948!-+the-CHICAGO-1949-TAIL!)** + **★★★ THE-VIOLET-RETRO-ENTRY-z6-THE-NEW-TYPE (the-DATED-retro-note-'vom-11.-October-1875'!)** + **★★★ THE-FEBER-1-BREAK-WITHOUT-DATE (s48-r9-the-date-cells-EMPTY!)** + **★★★ THE-PRIEST-ALTERNATION-1875 (DOVGAN-×10/HOGGIA-×7!)** + **17 NEW BLOCKS: the vitals 1853 → 1870 · the 04104 = 201 → 218**; the scripts p231 + qa-p231 (the 231st check!) + the evidence parish-baptism-1875-04104.json (119-entries: 17-Griblje + 102-others!) + the pt-gap-218/1870; **★★★ THE-BAPTISM-PREHISTORY-LINE-11/15-YEARS!** (the P232-LEAD: 1874 — the-boundary-ALREADY-FOUND-s47-MID-PAGE! → the-TAIL-1874-×5-rows! → probe-s38–s47-DESCENDING!)",
    p231Errors.length === 0,
    p231Errors.length === 0
      ? `17 vpisov / 119-vpisov (z1–z115 + TAIL-z1–z4-LOKALNI-RESTART!-z100-TODGEBORENE[?]-garble!) / 16-hiš-h48-DUEL · MEJA-1874/75-s47-SREDI-PAGI-NOVA-VARIANTA-70.-POTRDITEV (TAIL-1874-×5!-'Jänner'-PRELIM-+-'1'+'8'-VSOTNA[?]!-RESTART-z1-9./9.!-11.-restart!-BREZ-finis-kalligrafije!) · TROJNI-DUPLIKAT-folio-57-NOVO-ODKRITJE (sken−3-42–57! + sken−5-s63/s64!) · PEZDIRC-×5-NAJNIŽJA-continuum-11-let (×3-Griblje!) · NEZAKONSKI-×2-GRIBLJE ('ledig.'-NOTA!) · MODRI-×4 (†1933–1948!-CHICAGO-TAIL!) · VIOLET-RETRO-z6-DATIRANI-NOVI-TIP · FEBER-1-BREZ-DATUMA · DUHOVNIKI-DOVGAN-×10/HOGGIA-×7 · meseci-August+September-×0 · **LINIJA-11/15!** · vitals 1870 · 04104 218`
      : p231Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1853", "HOUSE_VITALS.length !== 1870")
# P230-block 04104-total: 201 → 218 (zdaj vključuje 1875!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 201)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 218)')
src = src.replace('p230Errors.push(`bloki 04104 ≠ 201 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876 = 201!)`)',
                  'p230Errors.push(`bloki 04104 ≠ 218 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875 = 218!)`)')
# yearset-04104: {1876..1885} → {1875,...,1885} (v P230-, P229-, P228-, P227-, P226-, P225-blokih!)
old_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
new_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
n_y = src.count(old_yearset)
src = src.replace(old_yearset, new_yearset)
for ph in ("p230Errors", "p229Errors", "p228Errors", "p227Errors", "p226Errors", "p225Errors"):
    src = src.replace(f'{ph}.push("04104-bloki izven {{1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-10/15: 1876–1885-do-P231!)");',
                      f'{ph}.push("04104-bloki izven {{1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-11/15: 1875–1885-do-P232!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1870×{src.count('HOUSE_VITALS.length !== 1870')} · qa-p231×{src.count('qa-p231-parish-baptism-1875-04104')} · yearset-patched-{n_y}")

# --- skripte + verifierji patch (1853→1870, 201→218) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p231_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1853" not in t: continue
    o = t
    t = t.replace("1853", "1870")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p231" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1853", "vitals == 1870"), ("vitalsTotal == 1853", "vitalsTotal == 1870"),
                 ('vitalsTotal"] == 1853', 'vitalsTotal"] == 1870'),
                 ('"vitalsTotal": 1853', '"vitalsTotal": 1870'),
                 ('\\"vitalsTotal\\": 1853', '\\"vitalsTotal\\": 1870'),
                 ('!== 1853"', '!== 1870"'),
                 ("1853-številcev", "1870-številcev"),
                 ("vitals-števec-1853", "vitals-števec-1870"), ("vitals-1853", "vitals-1870")]:
        t = t.replace(a, b)
    # 04104-total 201 → 218 v verifierjih p221–p230
    t = t.replace("== 201", "== 218")
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 201 → 218
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 201}', '"04104": 218}')
t = t.replace("# POSODABLJENO P230: + krstna-04104 = 201 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230!)",
              "# POSODABLJENO P231: + krstna-04104 = 218 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230 + 17×1875-P231!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (218)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1870
pt["corpus"]["byBook"]["04104"] = 218
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P231: +17-blokov-1875-krstna-04104-11/15 (vitals 1853→1870; 04104 201→218; 119-vpisov z1–z115+TAIL-z1–z4-LOKALNI-RESTART-NOVA-VARIANTA + MEJA-1874/75-s47-SREDI-PAGI-3.-varianta-70.-POTRDITEV (TAIL-1874-×5 + 'Jänner'-PRELIM + veliki-cifri-'1'+'8' + RESTART-z1-9./9.!-11.-restart!-BREZ-finis-kalligrafije!) + TROJNI-DUPLIKAT-SKENOV-folio-57-NOVO-ODKRITJE (sken−3-42–57!) + 17-GRIBLJE/16-hiš-h48-DUEL + PEZDIRC-×5-NAJNIŽJA-continuum-11-let + NEZAKONSKI-×2 + MODRI-×4-† + VIOLET-RETRO-z6-DATIRANI-NOVI-TIP + FEBER-1-BREZ-DATUMA + DUHOVNIKI-DOVGAN-×10/HOGGIA-×7 → P232-LEAD-1874)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
