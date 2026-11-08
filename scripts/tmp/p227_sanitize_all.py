#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P227 — INSERT qa-p227 + sanitizacija (1781→1870, 04104=129→151, yearset-04104-{1879..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p226: KRSTNA PREDZGODOVINA 04104 — leto 1880 = 6/15"
assert src.count(ANCHOR) == 1 and "qa-p227-parish-baptism-1879-04104" not in src

BLOCK = '''
  // ——— qa-p227: KRSTNA PREDZGODOVINA 04104 — leto 1879 = 7/15
  //      (P226: 1880 = 6/15!). 1879 = 96 vpisov-DISTINCT (vrstna-aritmetika
  //      2+8+7+7+6+6+7+8+8+9+8+7+8+5 = 96 = P226-LEAD-'1879 = 96-vpisov-BONUS'-1:1-INVARIANTA! —
  //      zap-stolpci-14/14-ČISTO!) / 22-GRIBLJE / 19-hiš (h31-×2 + h22-×2 + h17-×2-DUELI-REŠENI-MAX-krop!) +
  //      ★★★ MEJA-1878/79-s105/s106 (TAIL-1878-z90–z94 + VSOTNA-RAZPETA-'1 8'+'79'-čez-obe-strani! +
  //      glava-'Jahr 1878'-s-popravo! + RESTART-z1-NA-DAN-8./9.-JÄNNER-Kloster-h37-†19.7.1942!-7.-restart-z1-
  //      NAJPONEJŠI!) = 66.-POTRDITEV + ★★★ FOLIACIJA-'sken−6'-14/14-SEKVENČNO (100–113!-s112='106'-
  //      LEAD-PREDICTION-POTRJENA!) + ★★★ PEZDIRC-×12-vrstic (z51-DVOJNI! z67-DVOJNI!-continuum-7-let!) +
  //      MILEK-×6 (z22-DVOJNI!) + JAKOFČIČ-×5+×3 (z28/z44-DVOJNI!) + KRIŽAN-×4 (z13-DVOJNI!) + SIMEC-×3-
  //      KOMPLET + BRODARIČ-×3-KOMPLET + ★★★ DVOJČKI-ZWILLINGE-×3-REKORD (z47/48 + z55/56 + z65/66!-
  //      vse-z-'Zwillinge'-anotacijo!) + ★★★ TODTGEBOREN-×3 (z15/z57/z66!-vsi-stolpci-PRAZNI!) + ★★★
  //      z23-NEZAKONSKI-GRIBLJE + ★★★ MODRI-×12-REKORD (×7-Griblje!) + ★★★ DUHOVNIŠKA-IZMENJAVA
  //      (Janičar-coep↔Dovgan-alternirajoče!-11/22!) + z60-POGOJNI-KRST ('sub conditione'-B.Dog!) +
  //      z32-IMENSKI-POPRAVEK + z76-DATUMSKI-PRIPIS + meseci J1+F2+A5+Juni2+Juli2+A2+S3+O1+N2+D2
  //      (März/Mai-×0!). Dokaz: parish-baptism-1879-04104.json; skripte p227.
  {
  const p227Errors: string[] = [];
  const p227Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1879);
  if (p227Bapt.length !== 22)
    p227Errors.push(`bloki 1879 (04104) ≠ 22 (${p227Bapt.length} — 22 Griblje-vpisov / 19-hiš (h31-×2 + h22-×2 + h17-×2!) / 96-DISTINCT = P226-LEAD-1:1!)`);
  if (HOUSE_VITALS.length !== 1870)
    p227Errors.push(`HOUSE_VITALS ≠ 1870 (${HOUSE_VITALS.length} — P226: 1781; P227: + 22 blokov 1879-04104 = 1870!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 151)
    p227Errors.push(`bloki 04104 ≠ 151 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P226: 129; P227: + 22 × 1879 = 151!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p227Errors.push("04104-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-7/15: 1879–1885-do-P228!)");
  if (!p227Bapt.some((h) => h.whatSi.includes("RESTART-stran") || h.whatSi.includes("66.-POTRDITEV")))
    p227Errors.push("★★★ MEJA-1878/79-s105/s106 (VSOTNA-RAZPETA-'1 8'+'79' + RESTART-z1-8./9.-JÄNNER-Kloster-h37!) ni označena");
  if (p227Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 3)
    p227Errors.push(`★★★ PEZDIRC-×3+-in-Griblje ni dosežen (${p227Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/3!)`);
  if (!p227Bapt.some((h) => h.whatSi.includes("PEZDIRC-matec-nit") || h.whatSi.includes("PEZDIRC-oče-nit")))
    p227Errors.push("★★★ PEZDIRC-nit (z22/z91-matec + z95-oče!) ni označena");
  if (!p227Bapt.some((h) => h.whatSi.includes("MILEK-DVOJNI-nit")))
    p227Errors.push("★★★ z22-MILEK-DVOJNI-nit (oče+boter!) ni označena");
  if (!p227Bapt.some((h) => h.whatSi.includes("JAKOFČIČ-DVOJNI-nit")))
    p227Errors.push("★★★ z28/z44-JAKOFČIČ-DVOJNI-nit (matec+botra / botra-×2!) ni označena");
  if (!p227Bapt.some((h) => h.whatSi.includes("KRIŽAN-DVOJNI-botra-nit")))
    p227Errors.push("★★★ z13-KRIŽAN-DVOJNI-botra-nit ni označena");
  if (!p227Bapt.some((h) => h.whatSi.includes("NEZAKONSKI-GRIBLJE")))
    p227Errors.push("★★★ z23-NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!) ni označena");
  if (p227Bapt.filter((h) => h.whatSi.includes("MODRI-MATIČARSKI-PRIPIS")).length < 7)
    p227Errors.push(`★★★ MODRI-×7-Griblje ni dosežen (${p227Bapt.filter((h) => h.whatSi.includes("MODRI-MATIČARSKI-PRIPIS")).length}/7!)`);
  if (!p227Bapt.some((h) => h.whatSi.includes("h49-DUEL-REŠEN-MAX-krop")))
    p227Errors.push("★★★ z33-h49-DUEL-REŠEN-MAX-krop ni označen");
  if (!p227Bapt.some((h) => h.whatSi.includes("h22-×2-REŠEN-MAX-krop")))
    p227Errors.push("★★★ z61-h22-×2-REŠEN-MAX-krop (z22!) ni označen");
  if (!p227Bapt.some((h) => h.whatSi.includes("h17-×2-REŠEN-MAX-krop")))
    p227Errors.push("★★★ z69-h17-×2-REŠEN-MAX-krop (z28!) ni označen");
  if (!p227Bapt.some((h) => h.whatSi.includes("h31-×2")))
    p227Errors.push("★★★ h31-×2 (z2+z91!) ni označen");
  if (!p227Bapt.some((h) => h.whatSi.includes("†-15.6.1941")))
    p227Errors.push("★★★ z95-pripis-'†-15.6.1941'-PEZDIRC-oče ni označena");
  if (!p227Bapt.some((h) => h.whatSi.includes("podpis-Franz-DOVGAN")))
    p227Errors.push("★★★ z95-podpis-Franz-DOVGAN (izmenjava!) ni označena");
  if (!p227Bapt.some((h) => h.whatSi.includes("TAIL-1879-ZAČETEK")))
    p227Errors.push("★★★ z92-TAIL-1879-ZAČETEK ('Jahr 1879'-BREZ-VSOTNE!) ni označena");
  if (!p227Bapt.some((h) => h.whatSi.includes("HURE-oče-nit")))
    p227Errors.push("★★★ z63-HURE-oče-nit (P226-PARALELA!) ni označena");
  if (new Set(p227Bapt.map((h) => h.houseNo)).size !== 19)
    p227Errors.push(`★★★ 19-hiš-DISTINCT ni izpolnjeno (h31-×2 + h22-×2 + h17-×2! — najdeno ${new Set(p227Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p227-parish-baptism-1879-04104",
    "P227: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1879 = 7/15 (issue #18): okvir — s106–s119 (14 skenov; 2×-neodvisna-prenosa-md5-15/15-s105–s119!; s112-proba + s105–s111-probe-nazaj!) + **gola-svinčna-pag-'sken−6'-14/14-SEKVENČNO** (s106='100'/s107='101'/s108='102'/s109='103'/s110='104'/s111='105'/s112='106'-LEAD-PREDICTION-POTRJENA!/s113='107'/s114='108'/s115='109'/s116='110'/s117='111'/s118='112'/s119='113'-P226! — brez-luknje-v-1879-oknu — SKUPNA-SERIJA-100–158-z-1880/1881/1882/1883-okni!-LUKNJA-'158'-ostaja-samo-1882!) + **★★★ MEJA-1878/79 = s105/s106 (TAIL-1878-z90–z94-Dez-23–30-×5 + VSOTNA-RAZPETA-'1 8'+'79'-RAZPETA-ČEZ-OBE-STRANI! + glava-'Jahr 1878'-s-popravo-cifre! + RESTART-z1-NA-DAN-8./9.-JÄNNER-Kloster-h37-Maria-†19.7.1942-MODRI-PRIPIS! — 7.-restart-z1-NAJPONEJŠI-LINIJE!-P221-1.1-h21!-P222-1.1-h34!-P223-4.1-Gradac!-P224-2.1-Dobravce-h27!-P225-1.1-h55!-P226-3.1-Dobravce-h11!) = 66.-POTRDITEV-invariante! (65.-P226!)** + **★★★ 96-VPIISOV-DISTINCT — ŠTEVJE-IZ-VRSTIC-7.×-ZA-KRSTNO-LINIJO (z1–z96; vrstna-aritmetika 2+8+7+7+6+6+7+8+8+9+8+7+8+5 = 96 = P226-LEAD-'1879 = 96-vpisov-BONUS'-1:1-INVARIANTA! — zap-stolpci-14/14-ČISTO-brez-duplikatov!)** + **★★★ 22-GRIBLJE / 19-hiš (h31-×2: z2+z91! + h22-×2: z22+z61! + h17-×2: z28+z69! — DUELI-REŠENI-MAX-krop!-PARALELA-22-P226!): z2-h31-RESTART-stran! + z11-h68 (P223-PARALELA!) + z13-h16-KRIŽAN-DVOJNI!-†1949! + z20-h18-SIMEC! + z21-h6-JAKOFČIČ!-†1953! + z22-h22-MILEK-DVOJNI!-PEZDIRC! + z23-h24-NEZAKONSKI! + z28-h17-JAKOFČIČ-DVOJNI! + z30-h23-MILEK!-†1960! + z33-h49-DUEL-REŠEN!-SIMEC! + z39-h44-KLOBUČAR!-†1962-dolg! + z44-h7-JAKOFČIČ-DVOJNI! + z49-h46-KLOBUČAR! + z61-h22-REŠEN!-DRAGOŠ! + z63-h62-HURE!-KRIŽAN!-†1945! + z69-h17-REŠEN! + z74-h37-BRODARIČ!-KLOBUČAR!-†1939! + z78-h63-MILEK!-PEZDIRC-X-open! + z85-h11-DRAGOŠ! + z91-h31-PEZDIRC!-†1965! + z92-h28-MILEK-KOMPLET! + z95-h40-PEZDIRC!-†15.6.1941!** + **★★★ PEZDIRC-×12-vrstic-continuum-7-let (×4/×4/×6/×4/×9/×14/×12!-z51-matec+botra-DVOJNI! + z67-matec+boter-DVOJNI!-ne-Griblje! + z22-matec-Perdiče! + z91-matec-Pedirc! + z95-oče-Pezdirc!-in-Griblje! + z23/z78-boter-X-open!)** + MILEK-×6 (z22-DVOJNI-oče+boter!-6/6-KOMPLET-nit!) + JAKOFČIČ-×5+×3-neG (z28-matec+botra! + z44-botra-×2!-DVOJNI!) + KRIŽAN-×4 (z13-botra-×2!-DVOJNI!) + SIMEC-×3-KOMPLET + BRODARIČ-×3-KOMPLET + KLOBUČAR-×5-X-open + HURE-×2 + DRAGOŠ-×2 + **★★★ DVOJČKI-ZWILLINGE-×3-REKORD-LINJE (z47/48-Dorothea+Margaretha-Krasinec-h43! + z55/56-Katharina+Barbara-Krasinec-h32! + z65/66-Martin+todtgeboren-Zemelj-h24! — VSE-TRI-z-pisarjevo-'Zwillinge'-vertikalno-anotacijo + zavitim-oklepajem!-dvema-zap-številkama-v-eni-vrstici!-vs-×1-P223-GRIBLJE-h68 + ×1-P226-Boršt-h20!)** + **★★★ TODTGEBOREN-garble-×3 (z15-Vranoviče-h21-März-9/—! + z57-Prilozye-h35-16/—! + z66-Zemelj-h24-23/—! — garble-'…blyaborn'-≈-'todtgeboren'-krsten+botra+duhovnik-VSI-PRAZNI!-Mißgeburt-P226-z76/z77-PARALELA!-1.-DVOJČEK-todtgeboren!)** + **★★★ z23-NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!-April-19/20!-P226-z114-PARALELA!-+z86-Certoviše = ×2-linije!)** + **★★★ MODRI-MATIČARSKI-PRIPISI-×12-REKORD-LINJE (×7-Griblje: z13-'†-25.4.1949'! + z21-'†-30.12.1953'! + z30-'†-19.9.1960'! + z39-'†-10.5.1962'-DOLG-'v-Gribljah-št.65'! + z63-'†-7.5.1945'! + z74-'†-20.1.1939'! + z91-'†-15.11.1965'! + ×5-ne-G: z35-'†-22.6.1961'-DOLG-'Gradec-22.12.1975'-uradnik! + z41 + z55 + z64 + z79-dolg! — vs-×9-P226!)** + **★★★ DUHOVNIŠKA-IZMENJAVA-1879 ('Franz/Franc-Janičar-coep' ↔ 'Franz-Dovgan'-ALTERNIRAJOČE-čez-celo-leto!-X-open-po-VIZUALNO-branju!-Griblje-split-11/22!-vs-1880-ČISTA-menjava-okoli-z106!-z60-pripis-'B.Dog'-iniciale!-z95-DOVGAN-v-TAIL!)** + **Z60-POGOJNI-KRST ('Richtiglubem[?]-…-sub-conditione-…-die-27.-Augusti-1879-B.Dog'-pripis-čez-gender-stolpce!-1.-pogojni-krst-linije!)** + **Z32-IMENSKI-POPRAVEK ('Anna'-→-prečrtano-'Johann'-→-'Anna'-ponovno!-+✗-pred-hišo-9!-P226-z100-Alois-PARALELA!)** + **Z76-DATUMSKI-PRIPIS ('…-gebären-am-[21~26].-Decemb-1879'-pod-September-vpiso-Anna!-X-open!-Z49-'zuzschreiben'-PARALELA!)** + Z42-HEBAMME ('Die-beistehende-Hebamme'-Maria-Rom!-rojen≠krsten-10/13!-+z25/z46/z52!) + glave-s-popravami-cifer ('Jahr 1878'-s106 + 'Jahr 1879'-s119-9čez7-X-open!) + rojen≠krsten-×5-Griblje (z2-8/9! + z21-13/14 + z23-19/20 + z28-10/13 + z39-vpis!) + meseci-Griblje: J1+F2+A5+Juni2+Juli2+A2+S3+O1+N2+D2 = 22 (März/Mai-×0!-2-prazne!) + foliacija-s112-'106'-LEAD-PREDICTION-POTRJENA + **22 NOVIH BLOKOV parish.ts: vitals 1781 → 1870 · 04104 = 129 → 151 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p227 (fetch-2×-md5-15/15 + VIZUALNO-arhivar-branje-×14!-API-429-override + krop-70 (DUELI-MAX-×4 + DVOJČKI-×3 + todtgeboren-×3 + MEJA + glava + z60/z32/z76 + zap + meseci + podpisi-×9!) + build-entries + build-proof) + qa-p227 (227. kontrola!) + dokaz parish-baptism-1879-04104.json (96-DISTINCT: 22-Griblje + 74-druge! 14-anomalij/11-crossChecks/honesty-24!) + pt-luknja-151/1870; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-7/15-LET!** (P228-LEAD: 1878 — TAIL-ŽE-VLM (s106: z90–z94-Dez-23–30 + VSOTNA-'1/8/7/8'?-ali-'1/8/7/9'-DUEL! + glava-'Jahr 1878'-s-popravo!) → 1878 = z1–z94-94-vpisov-pričakovano → MEJA-1877/78-pred-s106 → probe-s99–s106! — gola-pag-'sken−6'-pričakovana-s99='93'!)",
    "P227: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1879 = 7/15 (issue #18): the-frame — s106–s119 (14 scans; 2×-INDEPENDENT-md5-15/15!) + the-plain-pencil-pag-'scan−6'-14/14-SEQUENTIAL (100–113-no-gap!-s112='106'-LEAD-PREDICTION-CONFIRMED!) + **★★★ THE-1878/79-BOUNDARY = s105/s106 (the-TAIL-1878-z90–z94 + the-SPREAD-SUM-'1 8'+'79'-ACROSS-BOTH-PAGES! + the-'Jahr 1878'-header-WITH-A-DIGIT-CORRECTION! + the-RESTART-z1-ON-DAY-8/9-JÄNNER-Kloster-h37-Maria-†19.7.1942-BLUE! — the-7th-restart-z1-THE-LATEST!) = the-66th-CONFIRMATION!** + **★★★ 96-ENTRIES-DISTINCT (the-ROW-ARITHMETIC = 96 = the-P226-LEAD-1:1-INVARIANT!-the-zap-columns-14/14-CLEAN!)** + **★★★ 22-GRIBLJE / 19-houses (h31-×2 + h22-×2 + h17-×2 — DUELS-RESOLVED-BY-MAX-krops!)** + **★★★ THE-PEZDIRC-×12-ROWS-CONTINUUM-7-YEARS (2-DOUBLE-non-Griblje!-×5-in-Griblje!)** + MILEK-×6 + JAKOFČIČ-×5 + KRIŽAN-×4 + SIMEC-×3 + BRODARIČ-×3 + KLOBUČAR-×5 + HURE-×2 + DRAGOŠ-×2 + **★★★ THE-TWINS-ZWILLINGE-×3-RECORD (ALL-THREE-with-the-scribe's-vertical-'Zwillinge'-annotation!-2-zap-numbers-in-one-row!)** + **★★★ THE-TODTGEBOREN-garble-×3 (z15/z57/z66!-ALL-COLUMNS-EMPTY!-the-1st-TWIN-stillborn!)** + **★★★ THE-z23-ILLEGITIMATE-GRIBLJE (the-EMPTY-FATHER-COLUMN!)** + **★★★ THE-BLUE-MATRICULAR-ANNOTATIONS-×12-RECORD (×7-Griblje!)** + **★★★ THE-PRIEST-ALTERNATION-1879 (Janičar-coep ↔ Dovgan-THROUGH-THE-YEAR!-the-11/22-Griblje-split!-vs-the-1880-CLEAN-change!)** + THE-Z60-CONDITIONAL-BAPTISM ('sub conditione'-B.Dog!) + THE-Z32-NAME-CORRECTION (Anna→Johann-crossed→Anna!) + THE-Z76-DATE-ANNOTATION ('gebären-am-Decemb-1879'!) + **22 NEW BLOCKS: the vitals 1781 → 1870 · the 04104 = 129 → 151**; the scripts p227 + qa-p227 (the 227th check!) + the evidence parish-baptism-1879-04104.json (96-DISTINCT: 22-Griblje + 74-others!) + the pt-gap-151/1870; **★★★ THE-BAPTISM-PREHISTORY-LINE-7/15-YEARS!** (the P228-LEAD: 1878 — the-TAIL-ALREADY-VLM'd (s106: z90–z94!) → the-boundary-1877/78-before-s106 → probe-s99–s106!)",
    p227Errors.length === 0,
    p227Errors.length === 0
      ? `22 vpisov / 96-DISTINCT (vrstna-aritmetika = P226-LEAD-1:1!) / 19-hiš (h31-×2 + h22-×2 + h17-×2-REŠENE-MAX-krop!) · MEJA-1878/79-s105/s106-66.-POTRDITEV (VSOTNA-RAZPETA!-RESTART-z1-8./9.-JÄNNER-NAJPONEJŠI!-'Jahr 1878'-s-popravo!) · FOLIACIJA-sken−6-14/14-SEKVENČNO (100–113!-s112-'106'-PREDICTION!) · PEZDIRC-×12 (2-DVOJNI!-continuum-7-let!) · DVOJČKI-ZWILLINGE-×3-REKORD ('Zwillinge'-anotacije!) · TODTGEBOREN-×3 + NEZAKONSKI-z23! · MODRI-×12-REKORD + DUHOVNIŠKA-IZMENJAVA (alternacija!) · meseci-März/Mai-×0 · **LINIJA-7/15!** · vitals 1870 · 04104 151`
      : p227Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1781", "HOUSE_VITALS.length !== 1870")
# P226-block 04104-total: 129 → 151 (zdaj vključuje 1879!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 129)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 151)')
src = src.replace('p226Errors.push(`bloki 04104 ≠ 129 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880 = 129!)`)',
                  'p226Errors.push(`bloki 04104 ≠ 151 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879 = 151!)`)')
# yearset-04104: {1880..1885} → {1879,...,1885} (v P226-bloku!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p226Errors.push("04104-bloki izven {1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-6/15: 1880–1885-do-P227!)");',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p226Errors.push("04104-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-7/15: 1879–1885-do-P228!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1870×{src.count('HOUSE_VITALS.length !== 1870')} · qa-p227×{src.count('qa-p227-parish-baptism-1879-04104')} · yearset-{src.count('(h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880')}")

# --- skripte + verifierji patch (1781→1870, 129→151) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p227_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1781" not in t: continue
    o = t
    t = t.replace("1781", "1870")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p227" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1781", "vitals == 1870"), ("vitalsTotal == 1781", "vitalsTotal == 1870"),
                 ('vitalsTotal"] == 1781', 'vitalsTotal"] == 1870'),
                 ('"vitalsTotal": 1781', '"vitalsTotal": 1870'),
                 ('\\"vitalsTotal\\": 1781', '\\"vitalsTotal\\": 1870'),
                 ('!== 1781"', '!== 1870"'),
                 ("1781-številcev", "1870-številcev"),
                 ("vitals-števec-1781", "vitals-števec-1870"), ("vitals-1781", "vitals-1870")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 129 → 151
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 129}', '"04104": 151}')
t = t.replace("# POSODABLJENO P226: + krstna-04104 = 129 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226!)",
              "# POSODABLJENO P227: + krstna-04104 = 151 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (151)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1870
pt["corpus"]["byBook"]["04104"] = 151
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P227: +22-blokov-1879-krstna-04104-7/15 (vitals 1781→1870; 04104 129→151; 96-DISTINCT = P226-LEAD-'1879 = 96'-1:1 + 22-GRIBLJE/19-hiš (h31-×2 + h22-×2 + h17-×2!) + MEJA-1878/79-s105/s106-66.-POTRDITEV (VSOTNA-RAZPETA-'1 8'+'79'!-RESTART-z1-8./9.-JÄNNER-NAJPONEJŠI!-'Jahr 1878'-s-popravo!) + FOLIACIJA-sken−6-14/14-SEKVENČNO (100–113!-s112-'106'-PREDICTION!) + PEZDIRC-×12 (2-DVOJNI!-continuum-7-let!) + DVOJČKI-ZWILLINGE-×3-REKORD ('Zwillinge'-anotacije!) + TODTGEBOREN-×3 + NEZAKONSKI-z23 + MODRI-×12-REKORD + DUHOVNIŠKA-IZMENJAVA + 1878 = 94-BONUS → P228-LEAD)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
