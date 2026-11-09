#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — INSERT qa-p235 + sanitizacija (1923→1940, 04104=271→288, yearset-04104-{1871..1885}, pt-luknja)
+ verifier-patchi (stale-1923→1940, 271→288)."""
from pathlib import Path
import glob, json

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p234: KRSTNA PREDZGODOVINA 04104 — leto 1872 = 14/15"
assert src.count(ANCHOR) == 1 and "qa-p235-parish-baptism-1871-04104" not in src

BLOCK = '''
  // ——— qa-p235: KRSTNA PREDZGODOVINA 04104 — leto 1871 = 15/15 — LINIJA KOMPLETNA!
  //      (P234: 1872 = 14/15!). 1871 = 108 vpisov (z1–z108!-116-vrstic − 8-DUPLIKAT-s4!-SEKVENČNO-1:1-10/10-strani!
  //      108-ARITMETIČNI-MODEL: s3=1–8 (z1-RESTART-13.!-ODPRTJE!) + [s4=DUPLIKAT-fol-1!] → s5=9–19 → s6=20–30 → s7=31–41
  //      (z37/z38-PREČRTANI!) → s8=42–52 → s9=53–64 → s10=65–74 (z72/z73-DVOJČKI-ZWILLINGE!) → s11=75–86 → s12=87–96
  //      (z91-KRSTEN-PRAZNO!) → s13=97–108-TAIL (TAIL-VERIGA-3/3!-z108-Dez-31-Otok!)!) /
  //      17-GRIBLJE / 16-hiš (h28-×2-DUEL-z81-vs-z83!-3.-LETO-VZOREC!) +
  //      ★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s1-vezava!-s2-naslovna!-nalepek-'PODZEMELJ-R-1871-1885'-KNJIGA = 15-LET-LINIJA!)
  //      + ★★★ MEJA-1871/72 = s13/s14 (P234-1:1!-re-use!) + ★★★ DUPLIKAT-s3=s4-RESITEV (fol-1-2×!-2-DUPLIKATA-KNJIGE-KOMPLET!)
  //      + ★★★ DUHOVNIKI-EKSTRAHIRANI (Weisel/Dotto/Feršlan/Wessely!-WEISEL/WENZEL/WESSELY-garble!) + ★★★ PEZDIRC-×8-'Peter'-×3
  //      + ★★★ MILIČ-×5 + JAKOFČIČ-×11-ish (SAKOFČIČ-garble!) + HRIŽAN-×9 + DVOJČKI + PREČRTANI + TOTGEBOREN.
  //      Dokaz: parish-baptism-1871-04104.json; skripte p235.
  {
  const p235Errors: string[] = [];
  const p235Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1871);
  if (p235Bapt.length !== 17)
    p235Errors.push(`bloki 1871 (04104) ≠ 17 (${p235Bapt.length} — 17 Griblje-vpisov / 16-hiš-h28-DUEL! / 108-vpisov!)`);
  if (HOUSE_VITALS.length !== 1940)
    p235Errors.push(`HOUSE_VITALS ≠ 1940 (${HOUSE_VITALS.length} — P234: 1923; P235: + 17 blokov 1871-04104 = 1940!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 288)
    p235Errors.push(`bloki 04104 ≠ 288 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P234: 271; P235: + 17 × 1871 = 288!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p235Errors.push("04104-bloki izven {1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-15/15-KOMPLETNA: 1871–1885!)");
  if (!p235Bapt.some((h) => h.whatSi.includes("MEJA-1870/71")))
    p235Errors.push("★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s1-vezava!-s2-naslovna!-nalepek-'PODZEMELJ-R-1871-1885'!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("TAIL-1871 = z108")))
    p235Errors.push("★★★ TAIL-1871 = z108-Dez-31-Otok (TAIL-VERIGA-3/3!-108-VPISOV!) ni označen");
  if (!p235Bapt.some((h) => h.whatSi.includes("MEJA-1871/72 = s13/s14-PAGE-BOUNDARY")))
    p235Errors.push("★★★ MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (P234-1:1!-re-use!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("DUPLIKAT-s3 = s4-RESITEV")) && !p235Bapt.some((h) => h.whatSi.includes("DUPLIKAT-s3")))
    p235Errors.push("★★★ DUPLIKAT-s3=s4-RESITEV (fol-1-2×!-P234-UGE-REŠENA!) ni označena");
  if (p235Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 5)
    p235Errors.push(`★★★ PEZDIRC-×8 ni dosežen (${p235Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/5!)`);
  if (!p235Bapt.some((h) => h.whatSi.includes("PEZDIRC-oče-EKSPPLICITEN-'Peter-Pezdirc'")))
    p235Errors.push("★★★ PEZDIRC-oče-'Peter-Pezdirc'-EKSPPLICITEN-X-ZOOM-1:1 (z81-h28!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("MILIČ-oče-nit-KOMPLET")))
    p235Errors.push("★★★ MILIČ-×5-oseb-REKORD (z16/z81/z83/z91/z96!-MILEK?-X-open!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("h28-×2-DELO-DUEL")))
    p235Errors.push("★★★ h28-×2-DELO-DUEL (z81-Pezdirc!-vs-z83-Požek!-3.-LETO-VZOREC!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("KLOBUČAR-oče-nit-EKSPPLICITEN")))
    p235Errors.push("★★★ KLOBUČAR-oče-'Joanes-Klobučar'-X-POTRJEN (z80-h48!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("DRAGOŠ-DVOJNI-oče+matec-nit")))
    p235Errors.push("★★★ DRAGOŠ-DVOJNI-oče+matec-nit (z46-h12!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("JAKOFČIČ-DVOJNI-boter+botra-nit")))
    p235Errors.push("★★★ JAKOFČIČ-DVOJNI-boter+botra-nit (z46!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("SAKOFČIČ-×3-TROJNI-block")))
    p235Errors.push("★★★ SAKOFČIČ-×3-TROJNI-block (z69!-'S'-for-'J'-garble!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("h69-CONTINUUM")))
    p235Errors.push("★★★ h69-CONTINUUM-×3-v-3-letih (z44-1871!-z97-1872!-z55-1873!) ni označen");
  if (!p235Bapt.some((h) => h.whatSi.includes("TAIL-VERIGA-z98")))
    p235Errors.push("★★★ TAIL-VERIGA-z98-X-'98'-1:1-POTRJEN (s13-r2-GRIBLJE!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("KRSTEN-PRAZNO-'—'")))
    p235Errors.push("★★★ z91-KRSTEN-PRAZNO-'—'-BREZ-BOTER-BREZ-PODPISA (X-open!) ni označena");
  if (!p235Bapt.some((h) => h.whatSi.includes("vrstica-ZELO-BLEDA")))
    p235Errors.push("★★★ z25-vrstica-ZELO-BLEDA (DOTTO.-podpis!) ni označena");
  if (p235Bapt.filter((h) => h.whatSi.includes("POŽEK")).length < 1)
    p235Errors.push("★★★ POŽEK-oče-nit (z83!-'Pez-Jure'-continuum!) ni označena");
  if (p235Bapt.filter((h) => h.whatSi.includes("DUEL")).length < 4)
    p235Errors.push(`★★★ DUEL-oznake ni dovolj (${p235Bapt.filter((h) => h.whatSi.includes("DUEL")).length}/4!)`);
  if (new Set(p235Bapt.map((h) => h.houseNo)).size !== 16)
    p235Errors.push(`★★★ 16-hiš-DISTINCT (h28-×2-DUEL!) ni izpolnjeno (najdeno ${new Set(p235Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p235-parish-baptism-1871-04104",
    "P235: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1871 = 15/15 — LINIJA KOMPLETNA (issue #18): okvir — s3–s13 (11 skenov-ODPRTJE-KNJIGE!-s1-vezava-0!-s2-naslovna-'Tauf-Buch.'-0!-arhivski-nalepek-'PODZEMELJ-R-1871-1885'-★★★ KNJIGA = 15-LET-LINIJA-1:1!-s3–s13-'Jahr 1871'-11/11-glave!-DESCENDING-probe-P234-LEAD-s9–s13-NADGRAJENO-s3–s13!-2×-neodvisna-md5-14/14!) + **★★★ FOLIACIJA-'sken−3'-KOMPLETNA-FORMULA-KNJIGE-s3–s14 (s3='1'!-s4='1'-★★★ DUPLIKAT!-s5='2'-s6='3'-s7='4'-s8='5'-s9='6'-s10='7'-s11='8'-s12='9'-s13='10'!-s14='11'-P234!-12/12!-SKOK-NA-DUPLIKATU-'1'→'2'-PARALELA-'25'→'27'-P234-1:1-2×!-★★★ 2-DUPLIKATA-KNJIGE: s3=s4-fol-1 + s28=s29-fol-25!)** + **★★★ 108-VPISOV-ARITMETIČNI-MODEL (z1–z108!-SEKVENČNO-1:1-10/10-strani-celost-branja-POPOLNO-BREZ-NAPAK!): s3=1–8 (z1-RESTART-13.-restart!-ODPRTJE-ZVEZKA!-Jänner-3-KRASINEC!) + [s4=DUPLIKAT-fol-1!] + s5=9–19 (z9-POST-DUPLIKAT-X!) + s6=20–30 + s7=31–41 (z37/z38-PREČRTANI!) + s8=42–52 + s9=53–64 + s10=65–74 (z72/z73-DVOJČKI-ZWILLINGE!) + s11=75–86 (z80/z81/z83-X!) + s12=87–96 (z91-KRSTEN-PRAZNO!) + s13=97–108 (TAIL-VERIGA-3/3!-z108-TAIL-Dez-31-Otok!) = ★★★ 116-vrstic-−-8-DUPLIKAT-s4 = 108-DISTINCT-VPISOV — vs-LEAD-'~90–110'-POTRJENO-1:1 (108!)** + **★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s2/s3!-EDINSTVENO-LINIJE!): s1 = vezava + s2 = tiskana-naslovna + ARHIVSKI-NALEPEK-'PODZEMELJ-R-1871-1885' (★★★ 1:1-KNJIGA = 15-LET = CELOTNA-PREDZGODOVINSKA-LINIJA!-P235 = ZADNJA-FAZA!) + s3-r1 = z1-RESTART-Jänner-3-KRASINEC-h27-Joanes-Zupanič (13.-restart!-1.-vpis-leta = KRASINEC-NOT-GRIBLJE!-★★★ VZOREC-'1.-vpis = GRIBLJE'-PREKINJEN!) | MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (P234-1:1!-re-use!): s13-TAIL-z108-Dez-31-Otok (TAIL-VERIGA-3/3-X!-BREZ-'finis-Anni-1871'-kalligrafije-Q4-5/5!-plain-PARALELA-1872!) + s14-r1 = z1-GRIBLJE (12.-restart-P234-SUPER!)** + **★★★ DUPLIKAT-s3 = s4-RESITEV (P234-'1-DUPLIKAT-s1–s13'-UGE-REŠENA-1:1!-fol-1-2×-SKENIRAN!-s3-r1 = s4-r1-'Jänner-3'-1:1!-X-K1/K2!-s4-vlepljeni-list!-★★★ 2-DUPLIKATA-KNJIGE-KOMPLETNA-REŠITEV!-108-TOTAL-INTAKTEN!)** + **★★★ 17-GRIBLJE / 16-hiš (h28-×2-DUEL-z81-Pezdirc!-vs-z83-Požek!-RAZLIČNI!-3.-LETO-VZOREC-h30-h37-h28!-+ X-hisna-z81-28/20!): z13-h24-1.-GRIBLJE-1871! + z16-h23-BRINE-KOMPLET! + z18-h60-HRIŽAN! + z25-h5-ZELO-BLEDA! + z34-h46-PEZDIRC-boter! + z35-h4-TOMC-†-pripis! + z44-h69-CONTINUUM! + z46-h12-DRAGOŠ-DVOJNI!-JAKOFČIČ-DVOJNI! + z69-h1-SAKOFČIČ-×3-TROJNI! + z80-h48-KLOBUČAR-X! + z81-h28-★★★-'Peter-Pezdirc'-EKSPPLICITNO-X-ZOOM-1:1! + z83-h28-★★★-DUEL-POŽEK! + z91-h65-KRSTEN-PRAZNO! + z92-h72-WENZEL?-skupni-podpis! + z96-h26[?]-MILIČ-KOMPLET! + z98-h6-TAIL-VERIGA-X! + z103-h10-pred-tail!** + **★★★ PEZDIRC-×8-'Peter'-×3-LINIJE (z81-oče-X-ZOOM-POTRJEN!-z34-z40-boter!-z32-matec+botra!-z84-matec+boter!-z88-garble!-z80-'Pez-Jure'-hipoteza!-vs-×5-1872!-×8-1873!)** + **★★★ MILIČ-×5-oseb-REKORD (z16-'Mihelik'-matec-hipoteza!-z81-z83-boter-2×-ISTI-h28-pair!-z91-z96-oče!-MILEK?-X-open-continuum!)** + ★★★ JAKOFČIČ-×11-ish-REKORD-LINIJE (×7-eksplicitni!-SAKOFČIČ-×4-garble-'S'-for-'J'!-z69-TROJNI!) + ★★★ HRIŽAN-×9-oseb-REKORD (Križan/Križanič/Krlžan/Kricžan-continuum!) + ★★★ KLOBUČAR-×5 ('Klobučan'-garble!-z80-oče-X!) + ★★★ BRODARIČ-×5 + ★★★ DRAGOŠ-×6-oseb (z46-DVOJNI-oče+matec!-z92-'Dragaš'-matec+botra!) + POŽEK-nit (z83-oče!-z80-matec-'PozJure'-continuum-1:1!) + ŠKALA-KUKE-TOMC-BRINE-STRUČELJ-niti + **★★★ DUHOVNIKI-1871-EKSTRAHIRANI-1:1 (1872-X-open-LEKCIJA-UPOŠTEVANA!): Wilhelm-Weisel-'D.H.-Cap.'-z1–z13 + Jakob?-z14–z19 (MEJA-z13/z14!) + Dotto.-z20–z41 (z25-ekspliciten!) + D.-Feršlan-'Pfr.'-z42–z52 (z46-ekspliciten!) + Daniel?-z53–z64-X-open + neberljivi-paraf-s11 + Wilhelm-Wenzel?-Coop.-z92/93 (skupni-podpis!) + Daniel-Wessely-'cop.'-z98 (ekspliciten!-TAIL!) + 'Po-ista-roka'-z103 — ≥4-eksplicitnih-im + ★★★ WEISEL/WENZEL/WESSELY-garble-continuum-ista-oseba?-X-open!** + **★★★ z72/z73-DVOJČKI-'Zwillinge'-pripis-X-POTRJEN (Boršt-h20!-Georg+Catharina!-1.-DVOJČKI-linije!)** + ★★★ z37/z38-PREČRTANI-DVOJNI (Krasinec-h12-Harasinič!-vijugasta-črta!-mrtvorojeni?-X-open!) + z30-TOTGEBOREN-Dragoše + z91-KRSTEN-PRAZNO-BREZ-botra-BREZ-podpisa (Griblje-h65-MILIČ!) + ★★★ NEZAKONSKI-×1 (z29-oče-PRAZNO!-PARALELA-1873!) + ★★★ MODRI-×3 ('umrl-20.12.1957'-★★★ 1957-NAJNOVEJŠI-LINIJE!-'1940'-'1953'!-razpon-1940–1957!) + **★★★ JÄNNER-×0-+ JUNI-×0-GRIBLJE (2-prazna-meseca!-vs-1872-Sep!-vs-1873-4!)** + h69-×3-CONTINUUM + h12-CONTINUUM-DRAGOŠ→PEZDIRC + h24/h1/h60/h6-×2-continuumi + rdeči-tički-'Lamim'-noty-'E-125.2.1933'-z42 + **17 NOVIH BLOKOV parish.ts: vitals 1923 → 1940 · 04104 = 271 → 288 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p235 (fetch-2×-md5-14/14 + celostanska-branja-×13 (s1–s13!-SEKVENČNO-1–108-BREZ-NAPAK!) + probe-Q1–Q4-A/B (8-sheetov!-glave-11/11!-foliacija-12/12-KOMPLETNA!) + X-DECISIVE-×10 (z1/z9/z71/z72/z73/z80/z81/z97/z98/z108!-TAIL-VERIGA-3/3!-DVOJČKI!-PREČRTANI!-PEZDIRC-EKSPPLICITEN!)) + qa-p235 (235. kontrola!) + dokaz parish-baptism-1871-04104.json (108-vpisov: 17-Griblje + 91-druge! anomalije/crossChecks/honesty!) + pt-luknja-288/1940; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-15/15-LET-KOMPLETNA! — KNJIGA-04104-DOKUMENTIRANA-OD-ZAČETKA!** (nalepek-'PODZEMELJ-R-1871-1885'-1:1!-korpus: 1940/235+288(04104)+433(04106)+502(04105)+520(04894)+197(04455)!-nadaljevanje: sinteza-linije-P236+!)",
    "P235: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1871 = 15/15 — THE LINE COMPLETE (issue #18): the-frame — s3–s13 (11 scans-the-BOOK-OPENING!-s1-binding!-s2-title-page!-THE-ARCHIVE-LABEL-'PODZEMELJ-R-1871-1885'-★★★ THE-BOOK = THE-15-YEAR-LINE-1:1!-2×-INDEPENDENT-md5-14/14!) + **★★★ THE-FOLIATION-'scan−3'-COMPLETE-FORMULA-OF-THE-BOOK-s3–s14 (s3='1'!-s4='1'-THE-DUPLICATE!-s5='2'-...-s13='10'!-s14='11'-P234!-12/12!-THE-SKIP-AT-THE-DUPLICATE-'1'→'2'-PARALLEL-'25'→'27'-P234-1:1-2×!-★★★ THE-2-DUPLICATES-OF-THE-BOOK: s3=s4-fol-1 + s28=s29-fol-25!)** + **★★★ THE-108-ENTRIES-ARITHMETIC-MODEL (z1–z108!-SEQUENTIAL-1:1-10/10-pages-THE-FULL-PAGE-READS-FLAWLESS!): s3=1–8 (z1-RESTART-the-13th!-THE-BOOK-OPENING!-Jan-3-KRASINEC!) + [s4=DUPLICATE!] + s5=9–19 + ... + s13=97–108 (THE-TAIL-CHAIN-3/3!-z108-TAIL-Dec-31!) = ★★★ 116-rows-−-8-DUPLICATE-s4 = 108-DISTINCT-ENTRIES — the-LEAD-'~90–110'-CONFIRMED-1:1 (108!)** + **★★★ THE-1870/71-BOUNDARY = THE-BOOK-START (s2/s3!-UNIQUE-IN-THE-LINE!): s1 = binding + s2 = printed-title-page + THE-ARCHIVE-LABEL-'PODZEMELJ-R-1871-1885' (★★★ 1:1-THE-BOOK = 15-YEARS = THE-WHOLE-PREHISTORY-LINE!) + s3-r1 = z1-RESTART-Jan-3-KRASINEC-h27 (the-13th-restart!-the-1st-entry = KRASINEC-NOT-GRIBLJE!-★★★ THE-'1st-entry = GRIBLJE'-PATTERN-BROKEN!) | THE-1871/72-BOUNDARY = s13/s14-PAGE-BOUNDARY (P234-1:1!-re-use!): s13-TAIL-z108 + s14-r1 = z1-GRIBLJE (the-12th-restart-P234-SUPER!-NO-'finis-Anni-1871'-calligraphy-Q4-5/5!-plain-PARALLEL-1872!)** + **★★★ THE-DUPLICATE-s3 = s4-RESOLUTION (the-P234-'1-DUPLICATE-s1–s13'-PUZZLE-SOLVED-1:1!-fol-1-SCANNED-TWICE!-s3-r1 = s4-r1-'Jan-3'-1:1!-★★★ THE-2-DUPLICATES-OF-THE-BOOK-COMPLETE-RESOLUTION!-108-TOTAL-INTACT!)** + **★★★ 17-GRIBLJE / 16-houses (h28-×2-DUEL!-THE-3rd-YEAR-PATTERN!)** + **★★★ THE-PEZDIRC-×8-'Peter'-×3-LINES (z81-father-'Peter-Pezdirc'-EXPLICIT-X-ZOOM-CONFIRMED-1:1!)** + **★★★ THE-MILIČ-×5-persons-RECORD (MILEK?-hypothesis-X-open-continuum!)** + ★★★ JAKOFČIČ-×11-ish-RECORD (SAKOFČIČ-garble-'S'-for-'J'!) + ★★★ HRIŽAN-×9-RECORD + ★★★ KLOBUČAR-×5 + ★★★ BRODARIČ-×5 + ★★★ DRAGOŠ-×6 (z46-DOUBLE-father+mother!) + **★★★ THE-PRIESTS-1871-EXTRACTED-1:1 (the-1872-X-open-LESSON-APPLIED!): Wilhelm-Weisel-'D.H.-Cap.' + Jakob? + Dotto. + D.-Feršlan-'Pfr.' + Daniel-Wessely-'cop.' — ≥4-EXPLICIT-NAMES + ★★★ WEISEL/WENZEL/WESSELY-garble-continuum-SAME-person?-X-open!** + **★★★ THE-TWINS-z72/z73-'Zwillinge'-note-X-CONFIRMED (Boršt-h20!-Georg+Catharina!-THE-1st-TWINS-of-the-line!)** + ★★★ z37/z38-CROSSED-OUT-DOUBLE + z30-STILLBORN + z91-NO-BAPTISM-DATE + ★★★ ILLEGITIMATE-×1 (z29!-PARALLEL-1873!) + ★★★ BLUE-ANNOTATIONS-×3 ('died-20.12.1957'-★★★ 1957-THE-LATEST-DATE-OF-THE-LINE!-'1940'-'1953'!) + **★★★ JANUARY-×0-+ JUNE-×0-GRIBLJE (the-2-EMPTY-MONTHS-of-1871!)** + h69-×3-CONTINUUM + h12-CONTINUUM + **17 NEW BLOCKS: the vitals 1923 → 1940 · the 04104 = 271 → 288**; the scripts p235 + qa-p235 (the 235th check!) + the evidence parish-baptism-1871-04104.json (108-entries: 17-Griblje + 91-others!) + the pt-gap-288/1940; **★★★ THE-BAPTISM-PREHISTORY-LINE-15/15-YEARS-COMPLETE! — THE-BOOK-04104-DOCUMENTED-FROM-ITS-BEGINNING!** (the-label-'PODZEMELJ-R-1871-1885'-1:1!-the-corpus: 1940/235+288(04104)+433(04106)+502(04105)+520(04894)+197(04455)!-next: the-line-synthesis-P236+!)",
    p235Errors.length === 0,
    p235Errors.length === 0
      ? `17 vpisov / 108-vpisov (z1–z108!-116-vrstic-−-8-DUPLIKAT!-SEKVENČNO-1:1-10/10!-TAIL-VERIGA-3/3!-z108-TAIL!) / 16-hiš-h28-DUEL-3.-LETO! · MEJA-1870/71 = ZAČETEK-KNJIGE (nalepek-'PODZEMELJ-R-1871-1885'!-KNJIGA = 15-LET-LINIJA!) · MEJA-1871/72 = s13/s14 (P234-1:1!) · DUPLIKAT-s3=s4-RESITEV (2-DUPLIKATA-KNJIGE-KOMPLET!) · DUHOVNIKI-EKSTRAHIRANI (Weisel/Dotto/Feršlan/Wessely!) · PEZDIRC-×8-'Peter'-×3-X! · MILIČ-×5 · JAKOFČIČ-×11-ish · HRIŽAN-×9 · KLOBUČAR-×5 · BRODARIČ-×5 · DRAGOŠ-×6 · DVOJČKI-z72/z73-X! · PREČRTANI-z37/z38 · NEZ-×1 · MODRI-×3-1957! · 2-PRAZNA-MESECA · **LINIJA-15/15-KOMPLETNA!** · vitals 1940 · 04104 288`
      : p235Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1923", "HOUSE_VITALS.length !== 1940")
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 271)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 288)')
src = src.replace('`bloki 04104 ≠ 271 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875; P232: + 19 × 1874; P233: + 17 × 1873; P234: + 17 × 1872 = 271!)`',
                  '`bloki 04104 ≠ 288 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875; P232: + 19 × 1874; P233: + 17 × 1873; P234: + 17 × 1872; P235: + 17 × 1871 = 288!)`')
# yearset-04104: add 1871 to all yearsets (p233..p235 blocks)
old_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874'
new_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874'
n_y = src.count(old_yearset)
src = src.replace(old_yearset, new_yearset)
src = src.replace("(predzgodovina-14/15: 1872–1885-do-P235!)", "(predzgodovina-15/15-KOMPLETNA: 1871–1885!)")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1940×{src.count('HOUSE_VITALS.length !== 1940')} · qa-p235×{src.count('qa-p235-parish-baptism-1871-04104')} · yearset-patched-{n_y}")

# --- skripte patch (1923→1940, 271→288) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p235_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1923" not in t and "271" not in t: continue
    o = t
    t = t.replace("1923", "1940")
    t = t.replace("== 271", "== 288")
    t = t.replace("271/1923", "288/1940")
    t = t.replace('"04104": 271', '"04104": 288')
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

# p191 EXPECTED_CORPUS: 04104 271 → 288
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 271}', '"04104": 288}')
t = t.replace("271", "288") if '"04104": 288}' not in t and "271" in t else t
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (288)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1940
pt["corpus"]["byBook"]["04104"] = 288
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P235: +17-blokov-1871-krstna-04104-15/15-LINIJA-KOMPLETNA (vitals 1923→1940; 04104 271→288; 108-vpisov z1–z108-116-−-8-DUPLIKAT-s3=s4-fol-1-2× + MEJA-1870/71-ZAČETEK-KNJIGE-nalepek-'PODZEMELJ-R-1871-1885'-KNJIGA = 15-LET-LINIJA-1:1 + MEJA-1871/72-s13/s14-P234-1:1-re-use + 13.-RESTART-z1-s3-r1-KRASINEC-VZOREC-PREKINJEN + TAIL-VERIGA-3/3-z108-Dez-31 + DVOJČKI-z72/z73-ZWILLINGE-X + PREČRTANI-z37/z38 + DUHOVNIKI-EKSTRAHIRANI-Weisel/Dotto/Feršlan/Wessely + PEZDIRC-×8-'Peter'-×3-z81-X-POTRJEN + MILIČ-×5-REKORD + JAKOFČIČ-×11-ish-REKORD + HRIŽAN-×9-REKORD + KLOBUČAR-×5 + BRODARIČ-×5 + DRAGOŠ-×6-DVOJNI-z46 + h28-×2-DUEL-3.-LETO + MODRI-×3-1957-NAJNOVEJŠI + NEZ-×1 + 2-PRAZNA-MESECA → LINIJA-15/15-KOMPLETNA-sinteza-P236+!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
