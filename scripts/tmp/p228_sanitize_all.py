#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P228 — INSERT qa-p228 + sanitizacija (1803→1870, 04104=151→167, yearset-04104-{1878..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p227: KRSTNA PREDZGODOVINA 04104 — leto 1879 = 7/15"
assert src.count(ANCHOR) == 1 and "qa-p228-parish-baptism-1878-04104" not in src

BLOCK = '''
  // ——— qa-p228: KRSTNA PREDZGODOVINA 04104 — leto 1878 = 8/15
  //      (P227: 1879 = 7/15!). 1878 = 94 vpisov-DISTINCT (vrstna-aritmetika
  //      7+6+7+7+6+8+8+7+8+8+7+10+5 = 94 = P227-LEAD-'1878 = 94-vpisov-pričakovano'-1:1-INVARIANTA! —
  //      zap-stolpci-15/15-ČISTO!) / 16-GRIBLJE / 14-hiš (h11-×2 + h64-×2-identični-glifyi-64/69-DUEL!) +
  //      ★★★ MEJA-1877/78-s92/s93 (TAIL-1877 + glava-'Jahr 1877'-BREZ-VSOTNE/velikih-cifer-P225-TIP! +
  //      RESTART-z1-NA-DAN-[8↔9]-JÄNNER-DUEL-Boginja-vas-h14-Margareth!-mesec-PREČRTAN!-8.-restart-z1!) = 67.-POTRDITEV +
  //      ★★★ FOLIACIJA-'sken−5'-13/14 (87–99!-LUKNJA-'94'-NA-s99-TEMNA-'34'-ANOMALIA!) + s105-DUPLIKAT-SKEN
  //      (≡s104!-LEPLJENEC-1908-Danijel-Barle-PEČAT!) → 'sken−6'-od-s106 = ARTEFAKT-DUPLIKATA-RAZLAGA! +
  //      ★★★ PEZDIRC-×17-vrstic-REKORD (2-DVOJNI!-continuum-8-let!) + ★★★ DUHOVNIŠKA-TROJNA-IZMENJAVA
  //      (Kroggj-coop ↔ Dovgan ↔ Janičar-coop-3-PODPISA!) + ★★★ z28-TODTGEBOREN-GRIBLJE + ★★★ z65-NEZAKONSKI-GRIBLJE
  //      (×5-linije!) + ★★★ DVOJČKI-×2 (z17/z18-bracket + z87/z88-squiggle!) + ★★★ MODRI-×12 (×2-MATCH-hišam!) +
  //      ★★★ POPRAVKI-×5 (z87-VAS-✗✗→'Primostek'! + z46-DATUMSKA! + z1-MESEC! + z4-OČE!) + meseci
  //      A6+Mai1+Aug1+Juli2+S3+O2+D1 (Jänner/Feber/März-×0!). Dokaz: parish-baptism-1878-04104.json; skripte p228.
  {
  const p228Errors: string[] = [];
  const p228Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1878);
  if (p228Bapt.length !== 16)
    p228Errors.push(`bloki 1878 (04104) ≠ 16 (${p228Bapt.length} — 16 Griblje-vpisov / 14-hiš (h11-×2 + h64-×2!) / 94-DISTINCT = P227-LEAD-1:1!)`);
  if (HOUSE_VITALS.length !== 1870)
    p228Errors.push(`HOUSE_VITALS ≠ 1870 (${HOUSE_VITALS.length} — P227: 1803; P228: + 16 blokov 1878-04104 = 1870!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 167)
    p228Errors.push(`bloki 04104 ≠ 167 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P227: 151; P228: + 16 × 1878 = 167!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p228Errors.push("04104-bloki izven {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-8/15: 1878–1885-do-P229!)");
  if (!p228Bapt.some((h) => h.whatSi.includes("67.-POTRDITEV")))
    p228Errors.push("★★★ MEJA-1877/78-s92/s93 (RESTART-z1-[8↔9]-JÄNNER-DUEL-Boginja-vas!-BREZ-VSOTNE!) ni označena");
  if (p228Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 6)
    p228Errors.push(`★★★ PEZDIRC-×6-Griblje ni dosežen (${p228Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/6!)`);
  if (!p228Bapt.some((h) => h.whatSi.includes("PEZDIRC-DVOJNI-vrstica")))
    p228Errors.push("★★★ PEZDIRC-DVOJNI-vrstica (z46-oče+boter! + z81-matec+boter!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("TODTGEBOREN-GRIBLJE")))
    p228Errors.push("★★★ z28-TODTGEBOREN-GRIBLJE (garble-'Nrbžgabumšt'!-botra+duhovnik-PRAZNI!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("NEZAKONSKI-GRIBLJE")))
    p228Errors.push("★★★ z65-NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!-×5-linije!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("TRETJI-DUHOVNIK")))
    p228Errors.push("★★★ z24-TRETJI-DUHOVNIK-'…binant-Kroggj[?]-coop' (trojna-izmenjava!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("JANIČAR-coop")))
    p228Errors.push("★★★ JANIČAR-coop-podpisi (z45/z52/z81-×3-Griblje!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("DATUMSKA-KOREKCIJA")))
    p228Errors.push("★★★ z46-DATUMSKA-KOREKCIJA ('Juni 30'-prečrtan→'Juli 1'!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("h64-×2-DUEL")))
    p228Errors.push("★★★ h64-×2-DUEL (z46+z81-identični-glifyi-64/69-X-open!) ni označen");
  if (!p228Bapt.some((h) => h.whatSi.includes("h11-×2")))
    p228Errors.push("★★★ h11-×2 (z28+z29!) ni označen");
  if (!p228Bapt.some((h) => h.whatSi.includes("HURE-boter-nit")))
    p228Errors.push("★★★ z64-HURE-boter-nit (P227-PARALELA!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("MODRI-MATIČARSKI-PRIPIS")))
    p228Errors.push("★★★ MODRI-pripisi (z31-h43-MATCH! + z52-h18-MATCH!) ni označena");
  if (!p228Bapt.some((h) => h.whatSi.includes("MATCH-h43")) || !p228Bapt.some((h) => h.whatSi.includes("MATCH-h18")))
    p228Errors.push("★★★ MODRI-MATCH-hišam (z31-'št 43'! + z52-'št 18'!) ni označena");
  if (p228Bapt.filter((h) => h.whatSi.includes("črnilo-pripis")).length < 4)
    p228Errors.push(`★★★ ČRNILO-pripisi-×4-Griblje ni dosežen (${p228Bapt.filter((h) => h.whatSi.includes("črnilo-pripis")).length}/4!)`);
  if (new Set(p228Bapt.map((h) => h.houseNo)).size !== 14)
    p228Errors.push(`★★★ 14-hiš-DISTINCT ni izpolnjeno (h11-×2 + h64-×2! — najdeno ${new Set(p228Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p228-parish-baptism-1878-04104",
    "P228: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1878 = 8/15 (issue #18): okvir — s92–s106 (15 skenov; 2×-neodvisna-prenosa-md5-15/15!; s99–s106-proba-P227-LEAD!-s92–s98-probe-nazaj!-s105-DUPLIKAT!) + **gola-svinčna-pag-'sken−5'-13/14-SEKVENČNO** (s92='87'/s93='88'/s94='89'/s95='90'/s96='91'/s97='92'/s98='93'-LEAD-'93'-NA-s98-NE-s99!-KOREKCIJA!/s99-TEMNA-'34'-ANOMALIA-LUKNJA-'94'!/s100='95'/s101='96'/s102='97'/s103='98'/s104='99' + s105='99'-DUPLIKAT-SKEN (≡s104-1:1!-LEPLJENEC-1908!)-→ s106='100'-'sken−6'-P227/P226-konvencija = **ARTEFAKT-DUPLIKATA-s105-RAZLAGA-NAJDENA!** — SKUPNA-SERIJA-87–158!) + **★★★ MEJA-1877/78 = s92/s93 (TAIL-1877-Dezember + glava-'Jahr 1877'-BREZ-VSOTNE/velikih-cifer-P225-TIP! + RESTART-z1-NA-DAN-[8↔9]-JÄNNER-DUEL-Geburt-'9'/Taufe-'8'-OBRNJENO-X-open!-Boginja-vas-h14-Margareth-MODRI-dolg-'†6.12.1959'-MMK-1959!-mesec-'Jänner'-PREČRTAN!-8.-restart-z1-NAJPONEJŠI-SE-ZLOMIL!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!) = 67.-POTRDITEV-invariante! (66.-P227!)** + **★★★ 94-VPIISOV-DISTINCT — ŠTEVJE-IZ-VRSTIC-8.×-ZA-KRSTNO-LINIJO (z1–z94; vrstna-aritmetika 7+6+7+7+6+8+8+7+8+8+7+10+5 = 94 = P227-LEAD-'1878 = 94-vpisov-pričakovano'-1:1-INVARIANTA! — zap-stolpci-15/15-ČISTO-brez-duplikatov!)** + **★★★ 16-GRIBLJE / 14-hiš (h11-×2: z28+z29-1:1-VIZUALNO! + h64-×2: z46+z81-identični-glifyi-64/69-DUEL-X-open! — z23-h73!-z31-h43!-z45-h55!-z56-h53!-KURRENT-DUELI-RAZREŠENI-7/4-5/3!): z23-h73-PEZDIRC!-por-†-črnilo! + z24-h19-TRETJI-DUHOVNIK! + z27-h29-MILEK! + z28-h11-TODTGEBOREN! + z29-h11-DRAGOŠ!-SIMEC! + z30-h1-JAKOFČIČ-×2! + z31-h43-MODRI-MATCH! + z45-h55-SIMEC!-PEZDIRC! + z46-h64-PEZDIRC-DVOJNI!-DATUMSKA-KOREKCIJA! + z52-h18-MODRI-MATCH!-DRAGOŠ!-KLOBUČAR! + z53-h48-PEZDIRC!-BRODARIČ! + z56-h53-PEZDIRC-×2!-BRODARIČ!-DRAGOŠ! + z64-h77-HURE!-poročen-črnilo! + z65-h6-NEZAKONSKI!-um-črnilo! + z69-h38-SIMEC!-DRAGOŠ!-†-črnilo! + z81-h64-PEZDIRC-DVOJNI!-JAKOFČIČ!** + **★★★ PEZDIRC-×17-vrstic-NOV-REKORD-LINJE-continuum-8-let (×4/×4/×6/×4/×9/×14/×12/×17!-z2/z3/z4-matec-×3-ZAPOREDOMA-RESTART-stran!-z46/z81-DVOJNI-Griblje!-×11-ne-Griblje!)** + SIMEC-×3-KOMPLET + DRAGOŠ-×4 (3/3-KOMPLET!) + JAKOFČIČ-×5 (z30-DVOJNI-botra!) + BRODARIČ-×2 + MILEK-×2 + HURE-×1 (P227-PARALELA!) + **★★★ DUHOVNIŠKA-TROJNA-IZMENJAVA-1878 ('…binant-Kroggj[?]-coop'-garble ↔ 'Franz-Dovgan' ↔ 'Franz-Janičar-coop'-3-PODPISA-REKORD-LINJE!-vs-×2-1879/1880!-Kroggj-z1–z26-alternacija-z-Dovganom!-Janičar-vstopi-okoli-z35!-Griblje-split-DOVGAN-×10/JANIČAR-×3/KROGGJ-×1/PRAZNA-×1!)** + **★★★ z28-TODTGEBOREN-GRIBLJE (garble-'Nrbžgabumšt'≈'nichtlebendgeburt'/'Notgeburt'-X-open-MAX-krop!-botra+duhovnik-VSI-PRAZNI!-1.-v-GRIBLJI!-P227-todtgeboren-×3-PARALELA!)** + **★★★ NEZAKONSKI-×5-REKORD-LINJE (očetov-stolpec-PRAZEN!-z9 + z13? + z36? + z63? + z65-GRIBLJE!-P227-z23-PARALELA!)** + **★★★ DVOJČKI-×2 (z17/z18-Krasinec-h43-Febrar-28/März-1-zavit-oklepaj-bracket-P223-PARALELA! + z87/z88-Bajukh-h12-December-17/17-squiggle-mark-+Agnes-Bajukh-PREČRTANA-v-botrah!-vs-×3-P227-REKORD)** + **★★★ MODRI-MATIČARSKI-PRIPISI-×12+-REKORD (1948–1978!-×2-MATCH-hišam: z31-'†18.6.1955-št 43'-MATCH-h43! + z52-'†18.3.1959-v-Gribljah-št 18'-MATCH-h18!-+z1-dolg!-z2-dolg!-z11/z20/z22/z37/z38/z39/z42/z83!)** + **★★★ ČRNILO-pripisi-×4-Griblje (z23-'por. 18/11 1920-† 12.5.1939'! + z64-'poročen 27/9 974[?]'-dolg! + z65-'um 16 Novr 880[?]'! + z69-'† 31.10.1931-Anwaru[?]-Reading[?]'!-+ne-G-×7!)** + **★★★ POPRAVKI-×5 (z87-VAS-POPRAVEK-'Nicolaus'-✗✗-DOVEMA-KRIŽEMA→'Primostek'-pisarjev-slip-otrokovo-ime-v-vas-stolpcu! + z88-vas-'Gerag[?]'-X-open-✗-v-sredini! + z46-DATUMSKA-KOREKCIJA-'Juni 30'-prečrtan→'Juli 1'-Z49-PARALELA! + z1-MESEC-'Jänner'-PREČRTAN-ponovljen! + z4-OČE-POPRAVEK-'Georg-gm[?]fič'-PREČRTAN→'Nicolaus-Uhr'!)** + z1-RESTART-DATUMSKI-DUEL (Geburt-'9'/Taufe-'8'-OBRNJENI-glifyi-X-open-P227-8./9.-PARALELA!) + **s105-LEPLJENEC-1908 (Danijel-Barle-rojen-19/1-1879-v-Podzemlju-+Marijo-Župan-15/5-1908-poročen-Župni-urad-v-Svinčah[?]-25/5-1908-OVALNI-PEČAT-+podpis-'Ant.-Peterlin[?]'-lepljen-ČEZ-z82–z85!)** + HEBAMME-Maria-Rom/Born-×8-continuum (z10/z19/z34/z35/z37/z40/z68/z72!) + rojen≠krsten-Griblje-×5 (z24-4/5! + z30-28/29! + z46-30/1! + z56-19/20! + z64-28/29!) + ✠-veliki-križ-margina (z60!) + zap-r1-'34-42'-STRAY-s99 + meseci-Griblje: A6+Mai1+Aug1+Juli2+S3+O2+D1 = 16 (Jänner/Feber/März-×0!-3-prazne!) + **16 NOVIH BLOKOV parish.ts: vitals 1803 → 1870 · 04104 = 151 → 167 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p228 (fetch-2×-md5-15/15 + VIZUALNO-arhivar-branje-×15!-API-429-override + krop-70 (Griblje-×16 + dueli-×8 + dvojčki-×2 + todtgeboren + nezakonski-×4 + MEJA + restart + foliacija-×14 + zap-×4 + podpisi-×16 + lepljenec + vsotna!) + build-entries + build-proof) + qa-p228 (228. kontrola!) + dokaz parish-baptism-1878-04104.json (94-DISTINCT: 16-Griblje + 78-druge! 15-anomalij/11-crossChecks/honesty-13!) + pt-luknja-167/1870; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-8/15-LET!** (P229-LEAD: 1877 — MEJA-1877/78-ŽE-NAJDENA-s92/s93 → 1877 = z1–z91?-vpisov (TAIL-z86–z91-Dezember-ŽE-VLM-s92!) → MEJA-1876/77-pred-s92 → probe-s85–s92!-DESCENDING! — gola-pag-'sken−5'-pričakovana-s85='80'!)",
    "P228: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1878 = 8/15 (issue #18): the-frame — s92–s106 (15 scans; 2×-INDEPENDENT-md5-15/15!-s105-DUPLICATE!) + the-plain-pencil-pag-'scan−5'-13/14-SEQUENTIAL (87–99!-THE-'94'-GAP-ON-s99-THE-DARK-'34'-ANOMALY!) + s105-DUPLICATE-SCAN (≡s104!-THE-1908-PASTED-SLIP!) → 'scan−6'-from-s106 = **THE-ARTEFACT-OF-THE-DUPLICATE-EXPLANATION-FOUND!** + **★★★ THE-1877/78-BOUNDARY = s92/s93 (the-TAIL-1877 + the-'Jahr 1877'-header-WITHOUT-THE-SUM/BIG-DIGITS-the-P225-TYPE! + the-RESTART-z1-ON-DAY-[8↔9]-JÄNNER-DUEL-Boginja-vas-h14-Margareth!-the-month-CROSSED!-the-8th-restart-z1!) = the-67th-CONFIRMATION!** + **★★★ 94-ENTRIES-DISTINCT (the-ROW-ARITHMETIC = 94 = the-P227-LEAD-1:1-INVARIANT!-the-zap-columns-15/15-CLEAN!)** + **★★★ 16-GRIBLJE / 14-houses (h11-×2 + h64-×2-identical-glyphs-64/69-DUEL!-the-7/4-5/3-KURRENT-DUELS-RESOLVED!)** + **★★★ THE-PEZDIRC-×17-ROWS-NEW-RECORD-CONTINUUM-8-YEARS (2-DOUBLE!-×3-CONSECUTIVE-mother-ON-THE-RESTART-PAGE!)** + SIMEC-×3 + DRAGOŠ-×4 + JAKOFČIČ-×5 + **★★★ THE-PRIEST-TRIPLE-ALTERNATION-1878 (Kroggj-coop ↔ Dovgan ↔ Janičar-coop-3-SIGNATURES-RECORD!-vs-×2-1879/1880!)** + **★★★ THE-z28-STILLBORN-GRIBLJE (garble-'Nrbžgabumšt'≈'nichtlebendgeburt'-ALL-COLUMNS-EMPTY!-the-1st-IN-GRIBLJE!)** + **★★★ THE-ILLEGITIMATE-×5-RECORD (incl.-z65-GRIBLJE!)** + **★★★ THE-TWINS-×2 (z17/z18-bracket! + z87/z88-squiggle-+Agnes-CROSSED-OUT!)** + **★★★ THE-BLUE-ANNOTATIONS-×12 (×2-MATCHING-THE-HOUSES: z31-'št 43'! + z52-'št 18'!)** + **★★★ THE-INK-ANNOTATIONS-×4-GRIBLJE** + **★★★ THE-CORRECTIONS-×5 (z87-VILLAGE-'Nicolaus'-✗✗→'Primostek'-THE-SCRIBE'S-SLIP! + z46-DATE-'Juni 30'→'Juli 1'! + z1-MONTH-CROSSED! + z4-FATHER-CROSSED!)** + **THE-s105-PASTED-SLIP-1908 (Danijel-Barle-THE-OVAL-SEAL!)** + **16 NEW BLOCKS: the vitals 1803 → 1870 · the 04104 = 151 → 167**; the scripts p228 + qa-p228 (the 228th check!) + the evidence parish-baptism-1878-04104.json (94-DISTINCT: 16-Griblje + 78-others!) + the pt-gap-167/1870; **★★★ THE-BAPTISM-PREHISTORY-LINE-8/15-YEARS!** (the P229-LEAD: 1877 — the-boundary-1877/78-ALREADY-FOUND-s92/s93 → the-TAIL-z86–z91-ALREADY-VLM'd-s92! → probe-s85–s92-DESCENDING!)",
    p228Errors.length === 0,
    p228Errors.length === 0
      ? `16 vpisov / 94-DISTINCT (vrstna-aritmetika = P227-LEAD-1:1!) / 14-hiš (h11-×2 + h64-×2-identični-glifyi!) · MEJA-1877/78-s92/s93-67.-POTRDITEV (RESTART-z1-[8↔9]-DUEL!-BREZ-VSOTNE!-mesec-PREČRTAN!) · FOLIACIJA-sken−5-13/14 (87–99!-LUKNJA-'94'-temna-'34'!) + s105-DUPLIKAT-SKEN → 'sken−6'-ARTEFAKT-RAZLAGA! · PEZDIRC-×17-REKORD (2-DVOJNI!-continuum-8-let!) · TROJNA-IZMENJAVA (3-PODPISA!) · TODTGEBOREN-GRIBLJE-z28! · NEZAKONSKI-×5! · DVOJČKI-×2 · MODRI-×12 (×2-MATCH!) · POPRAVKI-×5 (z87-VAS-✗✗!) · LEPLJENEC-1908! · meseci-J/Fe/M-×0 · **LINIJA-8/15!** · vitals 1870 · 04104 167`
      : p228Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1803", "HOUSE_VITALS.length !== 1870")
# P227-block 04104-total: 151 → 167 (zdaj vključuje 1878!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 151)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 167)')
src = src.replace('p227Errors.push(`bloki 04104 ≠ 151 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879 = 151!)`)',
                  'p227Errors.push(`bloki 04104 ≠ 167 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878 = 167!)`)')
# yearset-04104: {1879..1885} → {1878,...,1885} (v P227-, P226-, P225-blokih!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)')
src = src.replace('p227Errors.push("04104-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-7/15: 1879–1885-do-P228!)");',
                  'p227Errors.push("04104-bloki izven {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-8/15: 1878–1885-do-P229!)");')
src = src.replace('p226Errors.push("04104-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-7/15: 1879–1885-do-P228!)");',
                  'p226Errors.push("04104-bloki izven {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-8/15: 1878–1885-do-P229!)");')
src = src.replace('p225Errors.push("04104-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-7/15: 1879–1885-do-P228!)");',
                  'p225Errors.push("04104-bloki izven {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-8/15: 1878–1885-do-P229!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1870×{src.count('HOUSE_VITALS.length !== 1870')} · qa-p228×{src.count('qa-p228-parish-baptism-1878-04104')} · yearset-{src.count('(h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879')}")

# --- skripte + verifierji patch (1803→1870, 151→167) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p228_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1803" not in t: continue
    o = t
    t = t.replace("1803", "1870")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p228" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1803", "vitals == 1870"), ("vitalsTotal == 1803", "vitalsTotal == 1870"),
                 ('vitalsTotal"] == 1803', 'vitalsTotal"] == 1870'),
                 ('"vitalsTotal": 1803', '"vitalsTotal": 1870'),
                 ('\\"vitalsTotal\\": 1803', '\\"vitalsTotal\\": 1870'),
                 ('!== 1803"', '!== 1870"'),
                 ("1803-številcev", "1870-številcev"),
                 ("vitals-števec-1803", "vitals-števec-1870"), ("vitals-1803", "vitals-1870")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 151 → 167
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 151}', '"04104": 167}')
t = t.replace("# POSODABLJENO P227: + krstna-04104 = 151 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227!)",
              "# POSODABLJENO P228: + krstna-04104 = 167 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (167)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1870
pt["corpus"]["byBook"]["04104"] = 167
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P228: +16-blokov-1878-krstna-04104-8/15 (vitals 1803→1870; 04104 151→167; 94-DISTINCT = P227-LEAD-'1878 = 94'-1:1 + 16-GRIBLJE/14-hiš (h11-×2 + h64-×2!) + MEJA-1877/78-s92/s93-67.-POTRDITEV (RESTART-z1-[8↔9]-DUEL!-BREZ-VSOTNE!-mesec-PREČRTAN!) + FOLIACIJA-sken−5-13/14 (87–99!-LUKNJA-'94'-temna-'34'!) + s105-DUPLIKAT-SKEN → 'sken−6'-ARTEFAKT-RAZLAGA! + PEZDIRC-×17-REKORD (2-DVOJNI!-continuum-8-let!) + TROJNA-IZMENJAVA (3-PODPISA!) + TODTGEBOREN-GRIBLJE-z28 + NEZAKONSKI-×5 + DVOJČKI-×2 + MODRI-×12 (×2-MATCH!) + POPRAVKI-×5 + LEPLJENEC-1908 → P229-LEAD-1877)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
