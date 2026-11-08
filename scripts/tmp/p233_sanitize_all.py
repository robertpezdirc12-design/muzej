#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P233 — INSERT qa-p233 + sanitizacija (1889→1906, 04104=237→254, yearset-04104-{1873..1885}, pt-luknja)
+ FIX p232-verifier-I9b stale-1887→1889 (aritmetična-napaka-P232-popolna-sanitizacija!)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p232: KRSTNA PREDZGODOVINA 04104 — leto 1874 = 12/15"
assert src.count(ANCHOR) == 1 and "qa-p233-parish-baptism-1873-04104" not in src

BLOCK = '''
  // ——— qa-p233: KRSTNA PREDZGODOVINA 04104 — leto 1873 = 13/15
  //      (P232: 1874 = 12/15!). 1873 = 98 vpisov (z1–z98!-X-ARITMETIČNI-MODEL-9-ANKER: s28=11–21-+10-KURRENT-'1'-'2'-MISREAD!
  //      → s29=22–32 → s30=33–40 → s31=41–51 → s32=52–60 → s33=61–68 → s34=69–78 → s35=79–87 → s36=88–97 = z11–z97-okno!
  //      + z1–z10-pred-s28 + z98-tail-s37!-P232-X-open-'zap-28[~98]'-REŠEN-'98'!) /
  //      17-GRIBLJE / 16-hiš (h37-×2-DUEL-X-open-z19-vs-z81!) + ★★★ MEJA-1872/73-PRED-s28 (glave-9/9-'Jahr 1873'!
  //      + foliacija-'sken−3'-25–33-SEKVENČNO-BREZ-duplikatov!-LEAD-s35='32'-s30='27'-1:1-POTRJENI!)
  //      = 13.-restart-z1 (X-open-ARITMETIČNO-dokazan!) + ★★★ PEZDIRC-×8-GARBLE-REKORD (vs-×7-P232!)
  //      + ★★★ JAKOFČIČ-×5 + ★★★ BRODARIČ-×6-KOMPLET + ★★★ 4-PRAZNI-MESECI + ★★★ PENT-duhovnikov-X-open.
  //      Dokaz: parish-baptism-1873-04104.json; skripte p233.
  {
  const p233Errors: string[] = [];
  const p233Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1873);
  if (p233Bapt.length !== 17)
    p233Errors.push(`bloki 1873 (04104) ≠ 17 (${p233Bapt.length} — 17 Griblje-vpisov / 16-hiš-h37-DUEL! / 98-vpisov!)`);
  if (HOUSE_VITALS.length !== 1906)
    p233Errors.push(`HOUSE_VITALS ≠ 1906 (${HOUSE_VITALS.length} — P232: 1889; P233: + 17 blokov 1873-04104 = 1906!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 254)
    p233Errors.push(`bloki 04104 ≠ 254 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P232: 237; P233: + 17 × 1873 = 254!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p233Errors.push("04104-bloki izven {1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-13/15: 1873–1885-do-P234!)");
  if (!p233Bapt.some((h) => h.whatSi.includes("MEJA-1872/73-PRED-s28")))
    p233Errors.push("★★★ MEJA-1872/73-PRED-s28 (glave-9/9-'Jahr 1873'!-restart-z1-X-open-ARITMETIČNO!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("X-ARITMETIKA")))
    p233Errors.push("★★★ X-ARITMETIČNI-MODEL (9-ANKER!-+10-KURRENT-'1'-'2'-MISREAD!-zap-98-REŠEN!) ni označen");
  if (p233Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 8)
    p233Errors.push(`★★★ PEZDIRC-×8-GARBLE-REKORD ni dosežen (${p233Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/8!)`);
  if (!p233Bapt.some((h) => h.whatSi.includes("PEZDIRC-×3-DVOJNI")))
    p233Errors.push("★★★ PEZDIRC-×3-DVOJNI-garble-nit (z73-h53-oče+boter+matec-hipoteza!-X-'Pezdirc'-EKSPPLICITNO!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("PEZDIRC-×2-DVOJNI")))
    p233Errors.push("★★★ PEZDIRC-×2-DVOJNI-garble-nit (z39-h49-matec+boter!) ni označena");
  if (p233Bapt.filter((h) => h.whatSi.includes("JAKOFČIČ")).length < 5)
    p233Errors.push(`★★★ JAKOFČIČ-×5-REKORD ni dosežen (${p233Bapt.filter((h) => h.whatSi.includes("JAKOFČIČ")).length}/5!)`);
  if (!p233Bapt.some((h) => h.whatSi.includes("JAKOFČIČ-boter-DVOJNI-zakonca")))
    p233Errors.push("★★★ JAKOFČIČ-boter-DVOJNI-zakonca-nit (z47-PARALELA-P232-z2-1:1!) ni označena");
  if (p233Bapt.filter((h) => h.whatSi.includes("BRODARIČ")).length < 6)
    p233Errors.push(`★★★ BRODARIČ-×6-REKORD ni dosežen (${p233Bapt.filter((h) => h.whatSi.includes("BRODARIČ")).length}/6!)`);
  if (!p233Bapt.some((h) => h.whatSi.includes("ŠILAR")))
    p233Errors.push("★★★ ŠILAR-×3-KOMPLET-NOVA-NIT (z14/z18-oče!-z23-matec!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("DRAGOŠ-botra-nit (3/3-KOMPLET")))
    p233Errors.push("★★★ DRAGOŠ-botra-3/3-KOMPLET (z73!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("h40-DUEL-continuum")))
    p233Errors.push("★★★ h40-DUEL-continuum (z51-P232-h40-×2-križ!) ni označen");
  if (!p233Bapt.some((h) => h.whatSi.includes("POZICIJSKA-PARALELA-P232-z73")))
    p233Errors.push("★★★ z73-POZICIJSKA-PARALELA-P232 (obe-z73-1:1!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("zap-51-X-POTRJEN-1:1")))
    p233Errors.push("★★★ X-ANKA-zap-51-1:1 ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("LEAD-'JAKOŠA[?]'-REŠEN")))
    p233Errors.push("★★★ LEAD-P232-'JAKOŠA[?]'-REŠEN-X-'JAKOFČIČ' (z92!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("LEAD-'MILEK-botra'-DUEL-X-open")))
    p233Errors.push("★★★ LEAD-P232-'MILEK-botra'-DUEL-X-open (z93!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("LEAD-'h11-Kaspar-KUMIĆ'-DUEL-REŠEN")))
    p233Errors.push("★★★ LEAD-P232-'h11-Kaspar-KUMIĆ'-DUEL-REŠEN-×3 (z94!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("h37/57-DUEL-X-★★★-REŠEN-'37'")))
    p233Errors.push("★★★ hisna-37/57-DUEL-X-REŠEN-'37' (z81!-full-MERGE-RAZREŠEN!) ni označena");
  if (!p233Bapt.some((h) => h.whatSi.includes("matec-PRAZNO/prečrtano")))
    p233Errors.push("★★★ NEZAKONSKI?-X-open (z68-matec-PRAZNO/prečrtano!) ni označena");
  if (p233Bapt.filter((h) => h.whatSi.includes("MODRI")).length < 2)
    p233Errors.push(`★★★ MODRI-×2-Griblje ni dosežen (${p233Bapt.filter((h) => h.whatSi.includes("MODRI")).length}/2!)`);
  if (new Set(p233Bapt.map((h) => h.houseNo)).size !== 16)
    p233Errors.push(`★★★ 16-hiš-DISTINCT (h37-×2-DUEL!) ni izpolnjeno (najdeno ${new Set(p233Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p233-parish-baptism-1873-04104",
    "P233: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1873 = 13/15 (issue #18): okvir — s28–s36 (9 skenov; MEJA-1872/73-PRED-s28!-glave-9/9-'Jahr 1873'!-s28–s35-1873-teče!-s36-TAIL-zap-88–97-P232-predizkop!-DESCENDING-probe-P232-LEAD-s28–s36!-2×-neodvisna-md5-9/9!) + **★★★ FOLIACIJA-'sken−3'-SEKVENČNO-s28–s36 (25–33!-9/9-visoko!-s28='25'-s30='27'-s35='32'-s36='33'!-P232-LEAD-s35='32'-1:1-POTRJENA!-s30='27'-1:1-POTRJENA!-formula-CONTINUES!-BREZ-duplikatov-v-oknu!-2-DUPLIKATA-še-vedno-pred-s28-neznana-lokacija-s1–s27!)** + **★★★ X-ARITMETIČNI-MODEL-zap (9-ANKER-X-POTRJENIH: z51-s31-r11!-z55/z56-s32!-z65/z68-s33!-z88/z92/z93/z94-s36!): s28=11–21 (brano-20–30-★★★ +10-SISTEMATIČNI-KURRENT-'1'-'2'-MISREAD-11-vrstic!) + s29=22–32 (brano-32–42-+10!) + s30=33–40 + s31=41–51 + s32=52–60 + s33=61–68 + s34=69–78 + s35=79–87-P232! + s36=88–97-P232-križ! = 87-vrstic-okna (z11–z97!) + z1–z10-PRED-s28 (Jänner–März-na-s26/s27!-X-open!) + z98-TAIL-s37-r1! = ★★★ 98-VPISOV-1873 (z1–z98!-vs-LEAD-'~95'-NADGRADJENO!) — ★★★ P232-X-open-'TAIL-zap-28[~98/lokalni-restart]'-REŠEN-1:1-'zap-98' (KURRENT-'9'-'2'-misread!-z97+1-ARITMETIKA!)** + **★★★ MEJA-1872/73 = PRED-s28 (IZVEN-okna!-X-open): glave-s28–s36-VSE-'Jahr 1873' (9/9-Q1!) + s28-r1 = z11-März-3 (1873-teče!) → restart-z1-Jänner-1873-NA-s26/s27 ('finis-Anni-1872'/'Initium-1873'-kalligrafija-NI-v-oknu-Q4-9/9-negativno!) = 13.-restart-z1-linije (X-open-ARITMETIČNO-dokazan: z11-s28-r1!) | TAIL-1873 = s36-r1–r10-zap-88–97-vsi-November-P232-1:1! + s37-r1-Dez-28/29-Kloster-zap-98!; MEJA-1873/74-s37-SREDI-PAGI-'Initium-anni-Domini-1874'-P232!** + **★★★ 17-GRIBLJE / 16-hiš (h37-×2-DUEL-X-open-z19-'37[~27]'-Hrič!-vs-z81-'37'-X-REŠEN-Logar!-RAZLIČNI-družini!-vs-P232-h40-×2-VZOREC!): z14-h16-ŠILAR-oče-1.-v-oknu!-zap-[~14-X-ARITMETIKA!] + z18-h34-ŠILAR-oče-DEBLIČ-matec! + z19-h37/27-DUEL-Maria-HRIČ-garble-3-way!-URH-botra!-DEBLIČ-botra! + z23-h13-JAKOFČIČ-oče-ŠILAR-matec-KOMPLET!-MODRI-†28.12.1941!-retro-nota-'von-20-April-1873'-X-open! + z28-h31/33-DUEL-Johann-PEZDIRC-oče-garble-X-★★★!-mesec-MAI-X-open (full-'September'-kronološko-IZKLJUČEN!) + z39-h49-BRODARIČ-oče-PEZDIRC-×2-matec+boter-garble-★★★! + z47-h1-JAKOFČIČ-botra-DVOJNI-zakonca-PARALELA-P232-z2-1:1! + z51-h40-PEZDIRC-oče-garble-hipoteza-'Ležir'!-MODRI-†12.3.1938-Q4-križ!-h40-DUEL-continuum-P232-×2-križ!-★zap-51-X-POTRJEN! + z55-h69-vas-DUEL-×2/×1-GRIBLJE-zmaga-majoriteta-PARALELA-P232-z51-1:1!-PEZDIRC-botra-'Pedice'!-★zap-55-X! + z56-h74/64-DUEL-BRODARIČ-matec+botra-DVOJNI!-oče-garble-3-way!-★zap-56-X! + z65-h8-BRODARIČ-matec-3/3!-DRAGOŠ-botra!-oče-garble-JAKOPIČ/GLASPIĆ!-★zap-65-X! + z68-h22/42-DUEL-MILEK-vs-NOVAC-DUEL-X-★★★!-matec-PRAZNO/prečrtano-NEZ?-X-open!-BRODARIČ-boter-3/3!-★zap-68-X! + z73-h53-PEZDIRC-×3-DVOJNI-oče+boter+matec-hipoteza-X-'Pezdirc'-EKSPPLICITNO-branje!-DRAGOŠ-botra-3/3!-datum-DUEL-Oct-3/31!-★★★ POZICIJSKA-PARALELA-P232-z73 (obe-z73-1:1!) + z81-h37-X-★★★-REŠEN-'37'-LOGAR-oče-garble!-KLOBUČAR-botra!-full-r2/r3-MERGE-RAZREŠEN (Carolina-Sušnik-IZLOŽENA!) + z92-h6-JAKOFČIČ-oče-X-★★★-LEAD-'JAKOŠA'-REŠEN!-DRAGOŠ-botra!-★zap-92-X-P232-KRIŽ! + z93-h62-HRIŽAN-matec-garble!-MILEK-botra-DUEL-X-open-LEAD-'MILEK-botra'-DUEL! + z94-h41/11-DUEL-Kaspar-LEAD-'h11-KUMIĆ'-DUEL-REŠEN-×3-X-open!-DRAGOŠ-matec!-SIMEC-boter!-JAKOFČIČ-botra-5/5!-★zap-94-X-P232-KRIŽ!** + **★★★ PEZDIRC-×8-GARBLE-REKORD-PORAST (vs-×7-P232!-X-★★★-×3-eksplicitni-branji!-grafija-continuum: Pezdirc/Perdisek/Ležir/Pedice/Pegdire/Bezdirč!)** + JAKOFČIČ-×5-REKORD (PARALELA-P232-z2-zakonca-1:1!) + BRODARIČ-×6-REKORD-KOMPLET (oče+matec+botra!) + ŠILAR-×3-KOMPLET-NOVA-NIT + DRAGOŠ-×3-KOMPLET + DEBLIČ-×3-continuum + MILEK-×1-DUEL-X-open + HRIŽAN-×1-garble + KLOBUČAR-×1 + URH-×1-garble + LEGDIRE-×2-garble + SIMEC-×1 + LOGAR-×1-garble + **★★★ NEZAKONSKI-×1-X-open (z68-matec-PRAZNO/prečrtano!-vs-×0-P232!-row-alignment-pozor!)** + **★★★ MODRI-×2-Griblje (†28.12.1941-z23!-†12.3.1938-z51-Q4-križ-1:1!-razpon-1938–1941!-+ne-G-MODRI-s36-kontrole: r1-1960!-r3-1935!-r10-1877-OTROK!-r9-prečrtano-ime!)** + **★★★ 4-PRAZNI-MESECI-REKORD-IZENAČEN (Jänner/Juni/September/Dezember!-M1+A3+Mai1-DUEL+Juli3+Aug4+O2+N3 = 17!-vs-P232-BREZ-PRAZNIH!-vs-P231-2!-vs-P229-2!)** + **★★★ PENT-DUHOVNIKOV-1873-X-open-GARBLE-IZMENJAVA (vs-P232-TRI!-vs-P231-2!-REKORD-linije!): 'Franz-Dovgan'-continuum (s36-X-'Franz-Novgan'-KURRENT!) ↔ 'Joseph-Pihlár[?]' (P232-s36-r3/r4/r5!) ↔ 'Joseph-Roblek-Kaplan' (s30-X!) ↔ 'Jožef-Bobleh-Kaplan' (s32-X!-ROBLEK/BOBLEH-KURRENT-B/R-DUEL-X-open!) ↔ 'Franc-Dolenc[?]' (s31/s33-X-'Dolenc[~Dolžan?]'!-DOVGAH/DOLENC-DUEL-X-open!)** + s36-r9-PREČRTANO-ime + rdeči-tički-continuum + **17 NOVIH BLOKOV parish.ts: vitals 1889 → 1906 · 04104 = 237 → 254 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p233 (fetch-2×-md5-9/9 + celostanska-branja-×9 (s28–s36!) + probe-glave/foliacije/prve-vrstice/dna-Q1–Q4 (9/9-'Jahr 1873'!-25–33!-Q4-9/9-negativno!) + vrstični-krops-×9-sheetov + ločilni-krops-X1–X3 (×39!)) + qa-p233 (233. kontrola!) + dokaz parish-baptism-1873-04104.json (98-vpisov: 17-Griblje + 81-druge! anomalije/crossChecks/honesty!) + pt-luknja-254/1906; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-13/15-LET!** (P234-LEAD: 1872 — MEJA-1872/73-PRED-s28 → probe-s19–s28-DESCENDING!-'sken−3'-pričakovana-s27='24'! (s28='25'-P233-potrjena!)-POZOR: 2-DUPLIKATA-še-vedno-neznana-lokacija-s1–s27!-1872-vpisov-pričakovano-~85/95 (z1-restart-s26/s27!-'finis-Anni-1872'-/'Initium-1873'-kalligrafija-LAHKO!-P223-vzorec-'4.1-krst'-restart!)-restart-NA-s26/s27-GLAVE-'Jahr 1872'-pričakovane-s19–s27!)",
    "P233: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1873 = 13/15 (issue #18): the-frame — s28–s36 (9 scans; 2×-INDEPENDENT-md5-9/9!) + **★★★ THE-FOLIATION-'scan−3'-SEQUENTIAL-s28–s36 (25–33!-9/9!-the-P232-LEAD-CONFIRMED-2×!-NO-DUPLICATES-in-window!-2-DUPLICATES-still-before-s28-unknown-s1–s27!)** + **★★★ THE-X-ARITHMETIC-MODEL-zap (9-X-CONFIRMED-ANCHORS!): s28=11–21 (read-20–30-★★★ +10-SYSTEMATIC-KURRENT-'1'-'2'-MISREAD!) + ... + s36=88–97 = 87-window-rows (z11–z97!) + z1–z10-BEFORE-s28 + z98-TAIL! = ★★★ 98-ENTRIES-1873 (z1–z98!-the-LEAD-'~95'-UPGRADED!) — ★★★ THE-P232-X-open-'TAIL-zap-28[~98]'-SOLVED-1:1-'zap-98' (the-KURRENT-'9'-'2'-misread!-the-z97+1-ARITHMETIC!)** + **★★★ THE-1872/73-BOUNDARY-BEFORE-s28 (OUTSIDE-window!-X-open): the-headers-9/9-'Jahr 1873'!-the-restart-z1-Jänner-1873-ON-s26/s27 (X-open-ARITHMETICALLY-documented!) = the-13th-restart! | the-TAIL-1873 = s36-zap-88–97-November! + s37-r1-Dez-28/29-zap-98!** + **★★★ 17-GRIBLJE / 16-houses (h37-×2-DUEL-X-open!)** + **★★★ THE-PEZDIRC-×8-GARBLE-RECORD-GROWTH (vs-×7-P232!-X-★★★-×3-EXPLICIT!-the-grapheme-continuum-Pezdirc/Perdisek/Ležir/Pedice/Pegdire/Bezdirč!)** + JAKOFČIČ-×5-RECORD + BRODARIČ-×6-RECORD-COMPLETE + ŠILAR-×3-COMPLETE-NEW-THREAD + DRAGOŠ-×3-COMPLETE + **★★★ THE-ILLEGITIMATE-×1-X-open (vs-×0-P232!)** + **★★★ THE-BLUE-ANNOTATIONS-×2-GRIBLJE-† (1938–1941!)** + **★★★ 4-EMPTY-MONTHS-THE-RECORD-TIE (Jänner/Juni/September/Dezember!)** + **★★★ THE-FIVE-PRIESTS-1873-X-open-GARBLE-THE-ALTERNATION (vs-P232-THREE!-THE-LINE-RECORD!)** + **17 NEW BLOCKS: the vitals 1889 → 1906 · the 04104 = 237 → 254**; the scripts p233 + qa-p233 (the 233rd check!) + the evidence parish-baptism-1873-04104.json (98-entries: 17-Griblje + 81-others!) + the pt-gap-254/1906; **★★★ THE-BAPTISM-PREHISTORY-LINE-13/15-YEARS!** (the P234-LEAD: 1872 — the-boundary-ALREADY-FOUND-BEFORE-s28! → probe-s19–s28-DESCENDING!-the-'sken−3'-expected-s27='24'!)",
    p233Errors.length === 0,
    p233Errors.length === 0
      ? `17 vpisov / 98-vpisov (z1–z98!-X-ARITMETIČNI-MODEL-9-ANKER!-+10-KURRENT-misread!-zap-98-REŠEN!) / 16-hiš-h37-DUEL · MEJA-1872/73-PRED-s28 (glave-9/9!-13.-restart-X-open!) · 'sken−3'-25–33-SEKVENČNO · PEZDIRC-×8-GARBLE-REKORD · JAKOFČIČ-×5 · BRODARIČ-×6-KOMPLET · ŠILAR-×3-NOVA · DRAGOŠ-×3 · NEZ-×1-X-open · MODRI-×2 · 4-PRAZNI-MESECI · PENT-duhovnikov-X-open · **LINIJA-13/15!** · vitals 1906 · 04104 254`
      : p233Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1889", "HOUSE_VITALS.length !== 1906")
# P232-block 04104-total: 237 → 254 (zdaj vključuje 1873!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 237)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 254)')
src = src.replace('p232Errors.push(`bloki 04104 ≠ 237 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875; P232: + 19 × 1874 = 237!)`)',
                  'p232Errors.push(`bloki 04104 ≠ 254 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875; P232: + 19 × 1874; P233: + 17 × 1873 = 254!)`)')
# yearset-04104: {1874..1885} → {1873,...,1885} (v P232-, P231-, P230-, P229-, P228-, P227-, P226-, P225-blokih!)
old_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
new_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
n_y = src.count(old_yearset)
src = src.replace(old_yearset, new_yearset)
for ph in ("p232Errors", "p231Errors", "p230Errors", "p229Errors", "p228Errors", "p227Errors", "p226Errors", "p225Errors"):
    src = src.replace(f'{ph}.push("04104-bloki izven {{1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-12/15: 1874–1885-do-P233!)");',
                      f'{ph}.push("04104-bloki izven {{1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-13/15: 1873–1885-do-P234!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1906×{src.count('HOUSE_VITALS.length !== 1906')} · qa-p233×{src.count('qa-p233-parish-baptism-1873-04104')} · yearset-patched-{n_y}")

# --- FIX p232-verifier I9b stale-1887→1889 (P232-aritmetična-sanitizacija-lepa!) ---
v232 = ROOT / "scripts/p232_parish_baptism_1874_04104.py"
t = v232.read_text(encoding="utf-8"); o = t
t = t.replace('check("I9b pt-luknja-237/1887 + byBook-04104", \'"vitalsTotal": 1887\' in pt and \'"04104": 237\' in pt)',
              'check("I9b pt-luknja-237/1889 + byBook-04104", \'"vitalsTotal": 1889\' in pt and \'"04104": 237\' in pt)')
t = t.replace('f"1887-številcev={st}"', 'f"1889-številcev={st}"')
t = t.replace('check("I5 qa-p232 + števec-1887"', 'check("I5 qa-p232 + števec-1889"')
if t != o:
    v232.write_text(t, encoding="utf-8"); print("p232-verifier-I9b-FIX: 1887→1889 (stale!)")

# --- skripte + verifierji patch (1889→1906, 237→254) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p233_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1889" not in t: continue
    o = t
    t = t.replace("1889", "1906")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p233" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1889", "vitals == 1906"), ("vitalsTotal == 1889", "vitalsTotal == 1906"),
                 ('vitalsTotal"] == 1889', 'vitalsTotal"] == 1906'),
                 ('"vitalsTotal": 1889', '"vitalsTotal": 1906'),
                 ('\\"vitalsTotal\\": 1889', '\\"vitalsTotal\\": 1906'),
                 ('!== 1889"', '!== 1906"'),
                 ("1889-številcev", "1906-številcev"),
                 ("vitals-števec-1889", "vitals-števec-1906"), ("vitals-1889", "vitals-1906")]:
        t = t.replace(a, b)
    # 04104-total 237 → 254 v verifierjih p221–p232
    t = t.replace("== 237", "== 254")
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 237 → 254
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 237}', '"04104": 254}')
t = t.replace("# POSODABLJENO P232: + krstna-04104 = 237 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230 + 17×1875-P231 + 19×1874-P232!)",
              "# POSODABLJENO P233: + krstna-04104 = 254 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230 + 17×1875-P231 + 19×1874-P232 + 17×1873-P233!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (254)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1906
pt["corpus"]["byBook"]["04104"] = 254
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P233: +17-blokov-1873-krstna-04104-13/15 (vitals 1889→1906; 04104 237→254; 98-vpisov z1–z98-X-ARITMETIČNI-MODEL-9-ANKER-s28=11–21-+10-KURRENT-'1'-'2'-MISREAD-P232-'zap-28'-REŠEN-'98' + MEJA-1872/73-PRED-s28-glave-9/9-13.-restart-X-open + foliacija-25–33-SEKVENČNO-BREZ-duplikatov + 17-GRIBLJE/16-hiš-h37-DUEL + PEZDIRC-×8-GARBLE-REKORD + JAKOFČIČ-×5 + BRODARIČ-×6-KOMPLET + ŠILAR-×3-NOVA + NEZ-×1-X-open + MODRI-×2 + 4-PRAZNI-MESECI + PENT-duhovnikov-X-open → P234-LEAD-1872)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
