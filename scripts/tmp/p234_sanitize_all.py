#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P234 — INSERT qa-p234 + sanitizacija (1906→1940, 04104=254→271, yearset-04104-{1872..1885}, pt-luknja)
+ verifier-patchi (stale-1906→1940, 254→271)."""
from pathlib import Path
import glob, json

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p233: KRSTNA PREDZGODOVINA 04104 — leto 1873 = 13/15"
assert src.count(ANCHOR) == 1 and "qa-p234-parish-baptism-1872-04104" not in src

BLOCK = '''
  // ——— qa-p234: KRSTNA PREDZGODOVINA 04104 — leto 1872 = 14/15
  //      (P233: 1873 = 13/15!). 1872 = 115 vpisov (z1–z115!-116-vrstic − 1-PREČRTANA-kopija-r7-s24!-X-★★★!
  //      115-ARITMETIČNI-MODEL: s14=1–11 → s15=12–21 → s16=22–30 → s17=31–40 → s18=41–50 (X-50!)
  //      → s19=51–59 (JUNI!) → s20=60–68 → s21=69–79 → s22=80–89 → s23=90–99 → s24=100–109 (+1-prečrtana!)
  //      → s25=110–115-TAIL (TAIL-VERIGA-6/6!-z115-Dez-29-GRIBLJE!)!) /
  //      17-GRIBLJE / 16-hiš (h30-×2-DUEL-z14-vs-z103!-+ r7-PREČRTANA-KOPIJA!-ISENAČEN-1873!) +
  //      ★★★ 12.-RESTART-z1-NA-s14-r1 (1.-VPIS-leta = GRIBLJE!-PARALELA-P223!) + MEJA-1871/72-PAGE-BOUNDARY!
  //      + ★★★ MEJA-1872/73 = s25/s26-PAGE-BOUNDARY (P233-NAPoved-1:1!-restart-z1-s26-SUPER-POTRJEN!)
  //      + ★★★ DUPLIKAT-s28=s29-RESITEV (fol-25-2×!-98-TOTAL-1873-INTAKTEN!) + ★★★ PEZDIRC-×5-GARBLE.
  //      Dokaz: parish-baptism-1872-04104.json; skripte p234.
  {
  const p234Errors: string[] = [];
  const p234Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1872);
  if (p234Bapt.length !== 17)
    p234Errors.push(`bloki 1872 (04104) ≠ 17 (${p234Bapt.length} — 17 Griblje-vpisov / 16-hiš-h30-DUEL! / 115-vpisov!)`);
  if (HOUSE_VITALS.length !== 1940)
    p234Errors.push(`HOUSE_VITALS ≠ 1940 (${HOUSE_VITALS.length} — P233: 1906; P234: + 17 blokov 1872-04104 = 1940!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 288)
    p234Errors.push(`bloki 04104 ≠ 271 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P233: 254; P234: + 17 × 1872 = 271!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p234Errors.push("04104-bloki izven {1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-14/15: 1872–1885-do-P235!)");
  if (!p234Bapt.some((h) => h.whatSi.includes("MEJA-1871/72")))
    p234Errors.push("★★★ MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (restart-z1-s14-r1!-12.-restart!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("TAIL-1872 = z115")))
    p234Errors.push("★★★ TAIL-1872 = z115-Dez-29-GRIBLJE (TAIL-VERIGA-6/6!-115-VPISOV!) ni označen");
  if (!p234Bapt.some((h) => h.whatSi.includes("MEJA-1872/73 = s25/s26-PAGE-BOUNDARY")))
    p234Errors.push("★★★ MEJA-1872/73 = s25/s26-PAGE-BOUNDARY (P233-NAPoved-1:1!-restart-s26-SUPER!) ni označena");
  if (p234Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 5)
    p234Errors.push(`★★★ PEZDIRC-×5-GARBLE ni dosežen (${p234Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/5!)`);
  if (!p234Bapt.some((h) => h.whatSi.includes("PEZDIRC-×2-DVOJNI")))
    p234Errors.push("★★★ PEZDIRC-×2-DVOJNI-matec+boter-nit (z63-h6/61-EKSPPLICITNO-'Pezdirc'-2×!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("h40-CONTINUUM")))
    p234Errors.push("★★★ h40-CONTINUUM-×4-v-3-letih (z74-1872!-z51-1873!-z51/z82-1874!) ni označen");
  if (!p234Bapt.some((h) => h.whatSi.includes("DRAGOŠ-matec-nit")))
    p234Errors.push("★★★ DRAGOŠ-matec-nit (z1-h11-1.-vpis-leta!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("DRAGOŠ-botra-nit (3/3-KOMPLET")))
    p234Errors.push("★★★ DRAGOŠ-3/3-KOMPLET (z38!-1:1-PARALELA-P233!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("HRIŽAN-DVOJNI-oče+matec-nit")))
    p234Errors.push("★★★ HRIŽAN-DVOJNI-nit (z27!-×5-oseb-KOMPLET!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("HLOBUČAR-DVOJNI-matec+botra-nit")))
    p234Errors.push("★★★ HLOBUČAR-DVOJNI-nit (z34!-×3-KOMPLET-z103!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("ŠIMEC-oče-nit")))
    p234Errors.push("★★★ ŠIMEC-oče-nit (z38!-×3-KOMPLET!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("JAKOFČIČ-matec-nit (2/2-KOMPLET")))
    p234Errors.push("★★★ JAKOFČIČ-matec-2/2-KOMPLET (z103!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("MILEK-botra-garble-X-open-'Milhoeluc'")))
    p234Errors.push("★★★ MILEK-botra-'Milhoeluc'-PARALELA-P233-z93 (z92!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("DEBLIČ-oče-garble-nit-'Deblin'")))
    p234Errors.push("★★★ DEBLIČ-'Deblin'-X-★★★ (z61!-3-way-DUEL!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("PRIMING-HALUCINACIJA-RAZREŠENA")))
    p234Errors.push("★★★ 'Jänner'-PRIMING-HALUCINACIJA-RAZREŠENA (z59-JUNI-kronologija!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("mesec-GARBAGE-ROW")))
    p234Errors.push("★★★ mesec-GARBAGE-ROW (z27-celost-'November'-KRONOLOŠKO-IZKLJUČEN!) ni označena");
  if (!p234Bapt.some((h) => h.whatSi.includes("r7-PREČRTANA-KOPIJA-TE-VRSTICE-X")))
    p234Errors.push("★★★ h30-×2-DELO-DUEL + r7-PREČRTANA-KOPIJA-X (z103!) ni označena");
  if (p234Bapt.filter((h) => h.whatSi.includes("MODRI")).length < 4)
    p234Errors.push(`★★★ MODRI-×4-Griblje ni dosežen (${p234Bapt.filter((h) => h.whatSi.includes("MODRI")).length}/4!)`);
  if (!p234Bapt.some((h) => h.whatSi.includes("1.-VPIS-leta-1872 = GRIBLJE")))
    p234Errors.push("★★★ 1.-VPIS-leta-1872 = GRIBLJE-h11 (z1-RESTART-12.-restart-PARALELA-P223!) ni označen");
  if (new Set(p234Bapt.map((h) => h.houseNo)).size !== 16)
    p234Errors.push(`★★★ 16-hiš-DISTINCT (h30-×2-DUEL!) ni izpolnjeno (najdeno ${new Set(p234Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p234-parish-baptism-1872-04104",
    "P234: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1872 = 14/15 (issue #18): okvir — s14–s25 (12 skenov; MEJA-1871/72 = s13/s14-PAGE-BOUNDARY!-glave-12/12-'Jahr 1872'!-s14–s25-1872-teče!-s26-ŽE-1873-z1!-DESCENDING-probe-P233-LEAD-s19–s28-NADGRAJENO!-2×-neodvisna-md5-16/16!) + **★★★ FOLIACIJA-'sken−3'-SEKVENČNO-s14–s25 (11–22!-12/12-visoko!-s14='11'-s19='16'-s25='22'!-formula-CONTINUES-iz-P233!-BREZ-duplikatov-v-oknu!-★★★ DUPLIKAT-s28=s29-ILE-okna (fol-25-2×-skeniran!))** + **★★★ 115-VPISOV-ARITMETIČNI-MODEL (z1–z115!-TAIL-VERIGA-6/6!): s14=1–11 (11!-z1-X-RESTART-12.-restart!) + s15=12–21 + s16=22–30 (meseci-GARBAGE-ROW!) + s17=31–40 + s18=41–50 (X-50-KONTROLA!-z47/48-DUEL!) + s19=51–59 (JUNI-kronologija!-vs-'Jänner'-★★★ PRIMING-HALUCINACIJA-RAZREŠENA!) + s20=60–68 + s21=69–79 + s22=80–89 (BREZ-Griblje!) + s23=90–99 + s24=100–109 (10-distinct-+1-PREČRTANA-KOPIJA-r7-X-★★★!) + s25=110–115 (TAIL-VERIGA!-z115-TAIL-Dez-29-GRIBLJE!) = ★★★ 116-vrstic − 1-prečrtana = 115-DISTINCT-VPISOV (z1–z115!) — vs-LEAD-'~85–95'-NADGRADJENO** + **★★★ MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (1.-PAGE-BOUNDARY-linije!): restart-z1-NA-s14-r1 = Jänner-5-GRIBLJE-h11 (X-SUPER-'1'-POTRJEN!-12.-restart-PARALELA-P223-'krst-4.1'!-1.-vpis-leta = GRIBLJE!) | MEJA-1872/73 = s25/s26-PAGE-BOUNDARY (P233-ARITMETIČNA-NAPoved-1:1!): s25-TAIL-z115 + s26-r1 = z1-Jänner-3 (restart-13.-restart-S26R1-SUPER-'1'-VISOKO!-P233-X-open-RESOLVED!-BREZ-'finis-Anni-1872'-kalligrafije-Q4-10/10-negativno!)** + **★★★ DUPLIKAT-s28 = s29-RESITEV (fol-25-2×-skeniran!-P233-'z11–z21'-fantom-NIKOLI-ne-obstajal!-z1–z21-VSE-na-s26/s27!-★★★ 98-TOTAL-1873-INTAKTEN-1:1!-'2-DUPLIKATA'-P233-UGE-DELOVNO-RAZREŠENA!-vs-P231-TROJNI-s60–s62!)** + **★★★ 17-GRIBLJE / 16-hiš (h30-×2-DUEL-z14-Petek!-vs-z103-Simic!-RAZLIČNI-družini!-+ r7-PREČRTANA-KOPIJA-z103!-ISENAČEN-z-1873-×17!-PARALELA-h37-×2!): z1-h11-1.-VPIS-leta = GRIBLJE!-DRAGOŠ-matec! + z14-h30-Petek! + z27-h3-HRIŽAN-DVOJNI!-mesec-GARBAGE-ROW! + z34-h44-KRAUP-HLOBUČAR-DVOJNI! + z36-h9-DRAGOŠ-boter! + z38-h38-ŠIMEC-oče-DRAGOŠ-botra-KOMPLET!-MODRI-'poročena-18.II.1919-†16.3.'! + z47-h24-PRINC!-zap-47/48-DUEL! + z59-h12-PEZDIRC-'Pegdic'!-'Jänner'-PRIMING-halucinacija-RAZREŠENA-JUNI! + z61-h33-DEBLIČ-'Deblin'-X-★★★! + z63-h6/61-DUEL-PEZDIRC-×2-DVOJNI-EKSPPLICITNO! + z74-h40-★★★-CONTINUUM-×4-v-3-letih!-PEZDIRC-'Lezdirc/Ležir'-PARALELA-P233-z51! + z92-h68-MILEK-'Milhoeluc'-PARALELA-P233! + z97-h69-continuum! + z99-h7-PEZDIRC-'Peghirc'-5/5! + z103-h30/39-DUEL-JAKOFČIČ-KOMPLET!-HLOBUČAR-KOMPLET! + z112-h66-HRIŽAN-'Kribžan'!-MODRI-'smrtka-8.I'! + z115-h29-★★★-TAIL-1872!** + **★★★ PEZDIRC-×5-GARBLE-continuum (z59-'Pegdic'!-z63-Anna+Michael-'Pezdirc'-×2-EKSPPLICITNO-DVOJNI!-z74-'Lezdirc'-'Ležir'-hipoteza!-z99-'Peghirc'!-vs-×8-1873!)** + DEBLIČ-×1-'Deblin'-X-★★★ (3-way-DUEL!) + JAKOFČIČ-×2-KOMPLET + ★★★ DRAGOŠ-×3-KOMPLET-1:1-PARALELA-P233 (matec+boter+botra!) + ★★★ HRIŽAN-×5-oseb-KOMPLET (z27-DVOJNI!-Kribžan/Križan-garble!) + ★★★ HLOBUČAR-×3-KOMPLET (z34-DVOJNI!) + ★★★ ŠIMEC-×3-KOMPLET + KLOBUČAR-×2 + BRODARIČ-×2-garble + LOŽEK-×2 + MILEK-×1-'Milhoeluc'-PARALELA + MIHELIČ-×2-MILEK?-X-open + **★★★ NEZAKONSKI-×0-GRIBLJE (vs-×1-1873!)** + **★★★ MODRI-×4-Griblje-1872 ('poročena-18.II.1919-†16.3.'!-2-neberljivih!-'smrtka-dne-8.I'!-razpon-1919!)** + **★★★ SEPTEMBER-×0-GRIBLJE (1.-prazen-mesec-1872!-vs-1873-4-prazni!-vs-1874-BREZ-praznih!)** + s24-r7-PREČRTANA-KOPIJA-X-★★★ + 'Morija'-črtan-nota-z112 + 'November'-prelom-nota-z97 + rdeči-tički-continuum + **17 NOVIH BLOKOV parish.ts: vitals 1906 → 1940 · 04104 = 254 → 271 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p234 (fetch-2×-md5-16/16 + celostanska-branja-×16 (s13–s28!) + probe-glave/foliacije/prve-vrstice/dna-Q1–Q4 (s19–s28!-glave-10/10!-16–25-SEKVENČNO!) + X-DECISIVE-zap-veriga (s19–s31-17-kropov!) + VERIGA-26-27 (21!) + VERIGA-29-31 (30!-X-ANKA-z51-POTRJENA!-S28R1-SUPER-'22'!-S26R1-SUPER-'1'!) + TAIL-VERIGA (21!-s25-'110–115'-6/6!) + ločilni-X1/X2 (38-kropov!-17-GRIBLJE-vrstic!)) + qa-p234 (234. kontrola!) + dokaz parish-baptism-1872-04104.json (115-vpisov: 17-Griblje + 98-druge! anomalije/crossChecks/honesty!) + pt-luknja-271/1940; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-14/15-LET!** (P235-LEAD: 1871 — MEJA-1871/72-PAGE-BOUNDARY-s13/s14 → probe-s9–s13-DESCENDING!-'sken−3'-pričakovana-s13='10'-s12='9'! (s14='11'-P234-potrjena!)-POZOR: 1-DUPLIKAT-še-vedno-neznana-lokacija-s1–s13!-1871-vpisov-pričakovano-~90–110 (s13-12-vrstic-tail!)-GLAVE-'Jahr 1871'-pričakovane-s9–s13!-DUHOVNIKI-1871-X-open-ločilni-R-zoom!)",
    "P234: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1872 = 14/15 (issue #18): the-frame — s14–s25 (12 scans; 2×-INDEPENDENT-md5-16/16!) + **★★★ THE-FOLIATION-'scan−3'-SEQUENTIAL-s14–s25 (11–22!-12/12!-the-P233-LEAD-CONFIRMED!-NO-DUPLICATES-in-window!-★★★ THE-DUPLICATE-s28=s29-RESOLVED (folio-25-scanned-TWICE!))** + **★★★ THE-115-ENTRIES-ARITHMETIC-MODEL (z1–z115!-the-TAIL-CHAIN-6/6!): s14=1–11 (z1-X-RESTART-12th!) + ... + s24=100–109 (10-distinct-+1-CROSSED-OUT-copy-r7-X-★★★!) + s25=110–115 (the-TAIL!-z115-Dec-29-GRIBLJE!) = ★★★ 116-rows − 1-crossed-out = 115-DISTINCT-ENTRIES — the-LEAD-'~85–95'-UPGRADED** + **★★★ THE-1871/72-BOUNDARY = s13/s14-PAGE-BOUNDARY (the-1st-PAGE-BOUNDARY-of-the-line!): the-restart-z1-ON-s14-r1 = Jan-5-GRIBLJE-h11 (X-SUPER-'1'-CONFIRMED!-the-12th-restart!-the-1st-entry-of-the-year = GRIBLJE!) | THE-1872/73-BOUNDARY = s25/s26-PAGE-BOUNDARY (the-P233-ARITHMETIC-PREDICTION-1:1!): the-s25-TAIL-z115 + s26-r1 = z1-Jan-3 (the-13th-restart-SUPER-CONFIRMED!-the-P233-X-open-RESOLVED!-NO-'finis-Anni-1872'-calligraphy!)** + **★★★ THE-DUPLICATE-s28 = s29-RESOLUTION (folio-25-scanned-TWICE!-the-P233-'z11–z21'-phantom-NEVER-EXISTED!-z1–z21-ALL-on-s26/s27!-★★★ THE-98-TOTAL-1873-INTACT!-the-'2-DUPLICATES'-P233-PARTLY-RESOLVED!)** + **★★★ 17-GRIBLJE / 16-houses (h30-×2-DUEL!-the-r7-CROSSED-OUT-copy!-EQUAL-to-1873's-×17!)** + **★★★ THE-PEZDIRC-×5-GARBLE-continuum ('Pegdic'!-'Pezdirc'-×2-EXPLICIT-DOUBLE!-'Lezdirc/Ležir'!-'Peghirc'!-vs-×8-1873!)** + DEBLIČ-×1-'Deblin'-X-★★★ (3-way!) + JAKOFČIČ-×2-COMPLETE + ★★★ DRAGOŠ-×3-COMPLETE-1:1-PARALLEL (matec+boter+botra!) + ★★★ HRIŽAN-×5-persons-COMPLETE + ★★★ HLOBUČAR-×3-COMPLETE + ★★★ ŠIMEC-×3-COMPLETE + **★★★ THE-ILLEGITIMATE-×0-GRIBLJE (vs-×1-1873!)** + **★★★ THE-BLUE-ANNOTATIONS-×4-GRIBLJE ('married-18.II.1919-†16.3.'!-2-illegible!-'death-8.I'!)** + **★★★ SEPTEMBER-×0-GRIBLJE (the-1st-EMPTY-MONTH-of-1872!)** + **17 NEW BLOCKS: the vitals 1906 → 1940 · the 04104 = 254 → 271**; the scripts p234 + qa-p234 (the 234th check!) + the evidence parish-baptism-1872-04104.json (115-entries: 17-Griblje + 98-others!) + the pt-gap-271/1940; **★★★ THE-BAPTISM-PREHISTORY-LINE-14/15-YEARS!** (the P235-LEAD: 1871 — the-boundary-ALREADY-FOUND-s13/s14! → probe-s9–s13-DESCENDING!-the-'sken−3'-expected-s13='10'!-1-DUPLICATE-still-unknown-s1–s13!)",
    p234Errors.length === 0,
    p234Errors.length === 0
      ? `17 vpisov / 115-vpisov (z1–z115!-116-vrstic-−-1-prečrtana!-TAIL-VERIGA-6/6!-X-RESTART-z1!) / 16-hiš-h30-DUEL · 12.-RESTART-z1-s14-r1 (1.-vpis-leta = GRIBLJE!) · MEJA-1871/72 + MEJA-1872/73-PAGE-BOUNDARY (P233-NAPoved-1:1!) · DUPLIKAT-s28=s29-RESITEV (98-INTAKTEN!) · 'sken−3'-11–22-SEKVENČNO · PEZDIRC-×5-GARBLE · DRAGOŠ-×3-KOMPLET · HRIŽAN-×5 · HLOBUČAR-×3 · ŠIMEC-×3 · MODRI-×4 · NEZ-×0 · SEPTEMBER-×0 · **LINIJA-14/15!** · vitals 1940 · 04104 271`
      : p234Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1906", "HOUSE_VITALS.length !== 1940")
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 254)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 288)')
src = src.replace('`bloki 04104 ≠ 254 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875; P232: + 19 × 1874; P233: + 17 × 1873 = 254!)`',
                  '`bloki 04104 ≠ 271 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875; P232: + 19 × 1874; P233: + 17 × 1873; P234: + 17 × 1872 = 271!)`')
# yearset-04104: add 1872 to all yearsets (p232..p225 blocks + p233)
old_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874'
new_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874'
n_y = src.count(old_yearset)
src = src.replace(old_yearset, new_yearset)
src = src.replace("(predzgodovina-13/15: 1873–1885-do-P234!)", "(predzgodovina-14/15: 1872–1885-do-P235!)")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1940×{src.count('HOUSE_VITALS.length !== 1940')} · qa-p234×{src.count('qa-p234-parish-baptism-1872-04104')} · yearset-patched-{n_y}")

# --- skripte + verifierji patch (1906→1940, 254→271) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p234_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1906" not in t: continue
    o = t
    t = t.replace("1906", "1940")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-3][0-9]_parish*.py")):
    if "p234" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1906", "vitals == 1940"), ("vitalsTotal == 1906", "vitalsTotal == 1940"),
                 ('vitalsTotal"] == 1906', 'vitalsTotal"] == 1940'),
                 ('"vitalsTotal": 1906', '"vitalsTotal": 1940'),
                 ('\\"vitalsTotal\\": 1906', '\\"vitalsTotal\\": 1940'),
                 ('!== 1906"', '!== 1940"'),
                 ("1906-številcev", "1940-številcev"),
                 ("vitals-števec-1906", "vitals-števec-1940"), ("vitals-1906", "vitals-1940")]:
        t = t.replace(a, b)
    t = t.replace("== 254", "== 288")
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 254 → 271
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 254}', '"04104": 288}')
t = t.replace("# POSODABLJENO P233: + krstna-04104 = 254 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230 + 17×1875-P231 + 19×1874-P232 + 17×1873-P233!)",
              "# POSODABLJENO P234: + krstna-04104 = 271 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230 + 17×1875-P231 + 19×1874-P232 + 17×1873-P233 + 17×1872-P234!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (271)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1940
pt["corpus"]["byBook"]["04104"] = 271
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P234: +17-blokov-1872-krstna-04104-14/15 (vitals 1906→1940; 04104 254→271; 115-vpisov z1–z115-116-vrstic-−-1-prečrtana-TAIL-VERIGA-6/6 + 12.-RESTART-z1-s14-r1-1.-vpis-leta-GRIBLJE-PARALELA-P223 + MEJA-1871/72-s13/s14-PAGE-BOUNDARY + MEJA-1872/73-s25/s26-PAGE-BOUNDARY-P233-NAPoved-1:1-restart-s26-SUPER-POTRJEN + DUPLIKAT-s28=s29-RESITEV-fol-25-2×-98-TOTAL-1873-INTAKTEN + 17-GRIBLJE/16-hiš-h30-×2-DUEL-ISENAČEN-1873 + PEZDIRC-×5-GARBLE-continuum + DRAGOŠ-×3-KOMPLET-PARALELA + HRIŽAN-×5 + HLOBUČAR-×3 + ŠIMEC-×3 + MODRI-×4 + NEZ-×0 + SEPTEMBER-×0 + PREČRTANA-KOPIJA-r7-s24-X + PRIMING-halucinacija-'Jänner'-RAZREŠENA-JUNI → P235-LEAD-1871)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
