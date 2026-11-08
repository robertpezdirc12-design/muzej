#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P230 — INSERT qa-p230 + sanitizacija (1839→1870, 04104=187→201, yearset-04104-{1876..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p229: KRSTNA PREDZGODOVINA 04104 — leto 1877 = 9/15"
assert src.count(ANCHOR) == 1 and "qa-p230-parish-baptism-1876-04104" not in src

BLOCK = '''
  // ——— qa-p230: KRSTNA PREDZGODOVINA 04104 — leto 1876 = 10/15
  //      (P229: 1877 = 9/15!). 1876 = 100 vpisov-DISTINCT (z1–z100! vrstna-aritmetika 7+7+7+8+9+8+8+7+8+8+7+7+8+1 = 100 +
  //      zap-stolpci-VIDNI-×6-strani-1:1 s65:1–7-s66:8–14-s67:15–21-s68:22–29-s69:30–38-s70:39–46 + s77-zap-'94'-MODRA!) /
  //      14-GRIBLJE / 14-hiš-BREZ-DUPLIKATOV + ★★★ MEJA-1875/76-s64/s65-DVO-STRANSKA-NOVA-VARIANTA
  //      (TAIL-1875-incl.-GRIBLJE-h11! + 'finis-Anni-1875'-VELIJA-KALLIGRAFIJA-PARALELA-Incipit! | glava-'Jahr 1876'-BREZ-INCIPIT +
  //      RESTART-z1-5./5.-JÄNNER!-10.-restart!) = 69.-POTRDITEV + FOLIACIJA-'sken−5'-15/15 (59–73!-3×-NARISE!) +
  //      ★★★ PEZDIRC-×18-vrstic-NOV-REKORD-LINJE-continuum-10-let (×2-DVOJNI-GRIBLJE-h53/h55!) + ★★★ DVOJČKI-×4-dogodki-NOVI-VARIANTI
  //      (2-BRACE-'Zwillinge' + 2-SHARED-ROW!) + ★★★ NEZAKONSKI-×6-REKORD + ★★★ WOLFGR-ANOMALIJA-DRUŽINA-×3-NOVA (botra+duhovnik-PRAZNI!)
  //      + ★★★ MODRI-×11-linij-REKORD (×4-Griblje-†! + CHICAGO-1970! + MMK-×2!) + ★★★ 'als-Amtsvormund'-botra-NOTA-NOVI-TIP +
  //      ★★★ zap-'94'-MODRA + RETRO-VPISI-×2 + HEBAMME-Maria-Rom-×9 + DUHOVNIKI-Griblje-split-7/7-IZENAČEN. Dokaz: parish-baptism-1876-04104.json; skripte p230.
  {
  const p230Errors: string[] = [];
  const p230Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1876);
  if (p230Bapt.length !== 14)
    p230Errors.push(`bloki 1876 (04104) ≠ 14 (${p230Bapt.length} — 14 Griblje-vpisov / 14-hiš-BREZ-DUPLIKATOV / 100-DISTINCT!)`);
  if (HOUSE_VITALS.length !== 1870)
    p230Errors.push(`HOUSE_VITALS ≠ 1870 (${HOUSE_VITALS.length} — P229: 1839; P230: + 14 blokov 1876-04104 = 1870!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 201)
    p230Errors.push(`bloki 04104 ≠ 201 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P229: 187; P230: + 14 × 1876 = 201!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p230Errors.push("04104-bloki izven {1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-10/15: 1876–1885-do-P231!)");
  if (!p230Bapt.some((h) => h.whatSi.includes("69.-POTRDITEV")))
    p230Errors.push("★★★ MEJA-1875/76-s64/s65-DVO-STRANSKA (finis-Anni-1875-KALLIGRAFIJA! + RESTART-z1-5./5.-JÄNNER!-10.-restart!) ni označena");
  if (p230Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 7)
    p230Errors.push(`★★★ PEZDIRC-×7-Griblje ni dosežen (${p230Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/7!)`);
  if (!p230Bapt.some((h) => h.whatSi.includes("PEZDIRC-DVOJNI-vrstica")))
    p230Errors.push("★★★ PEZDIRC-DVOJNI-vrstici (h53-oče+boter! + h55-matec+botra!) nista označeni");
  if (!p230Bapt.some((h) => h.whatSi.includes("MILEK-oče")))
    p230Errors.push("★★★ MILEK-oče (z53-h22!) ni označen");
  if (!p230Bapt.some((h) => h.whatSi.includes("HURE-boter")))
    p230Errors.push("★★★ HURE-boter (z43-h7-P228-×1-PARALELA!) ni označen");
  if (!p230Bapt.some((h) => h.whatSi.includes("als-Amtsvormund")))
    p230Errors.push("★★★ 'als-Amtsvormund'-botra-NOTA-NOVI-TIP (z43!) ni označena");
  if (!p230Bapt.some((h) => h.whatSi.includes("MESEC-DUEL-X-open")))
    p230Errors.push("★★★ z53-MESEC-DUEL-X-open ('August[?]-4/4'-vs-'Juli-27/27'!) ni označen");
  if (!p230Bapt.some((h) => h.whatSi.includes("zap-'94'-MODRA")))
    p230Errors.push("★★★ z94-zap-'94'-MODRA ni označen");
  if (p230Bapt.filter((h) => h.whatSi.includes("MODRI")).length < 4)
    p230Errors.push(`★★★ MODRI-×4-Griblje ni dosežen (${p230Bapt.filter((h) => h.whatSi.includes("MODRI")).length}/4!)`);
  if (!p230Bapt.some((h) => h.whatSi.includes("SIMEC-oče")))
    p230Errors.push("★★★ SIMEC-oče-×2 (z26-h39! + z96-h55!-KOMPLET!) ni označen");
  if (!p230Bapt.some((h) => h.whatSi.includes("KLOBUČAR-DVOJNI-vrstica")))
    p230Errors.push("★★★ KLOBUČAR-DVOJNI-vrstica (z98-h44-matec+botra!) ni označena");
  if (!p230Bapt.some((h) => h.whatSi.includes("DRAGOŠ-boter")))
    p230Errors.push("★★★ DRAGOŠ-boter-×2-KOMPLET (z85-h53! + z92-h8!) ni označen");
  if (!p230Bapt.some((h) => h.whatSi.includes("BRINC-oče")))
    p230Errors.push("★★★ BRINC-oče (z88-h25-P229-z67/z68-PARALELA!) ni označen");
  if (!p230Bapt.some((h) => h.whatSi.includes("MUC-oče")))
    p230Errors.push("★★★ MUC-oče (z46-h15-P229-z1-PARALELA!) ni označen");
  if (new Set(p230Bapt.map((h) => h.houseNo)).size !== 14)
    p230Errors.push(`★★★ 14-hiš-DISTINCT-BREZ-DUPLIKATOV ni izpolnjeno (najdeno ${new Set(p230Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p230-parish-baptism-1876-04104",
    "P230: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1876 = 10/15 (issue #18): okvir — s64–s78 (15 skenov; 2×-neodvisna-prenosa-md5-15/15!-s71–s78-proba-P229-LEAD-DESCENDING! + s60–s70-probe-globlje!-s64/s65-MEJA-DVO-STRANSKA!-s78-tail-r1-P229!) + **gola-svinčna-pag-'sken−5'-15/15-SEKVENČNO** (s64='59'-NARISE!/s65='60'-NARISE!/s71='66'-NARISE!-3×-VIZUALNO!/s78='73'-P229! — SKUPNA-SERIJA-59–158-continuum!) + **★★★ MEJA-1875/76 = s64/s65-DVO-STRANSKA-NOVA-VARIANTA (s64 = TAIL-1875-×4-vrstic (r1-Dez-1/1-Krasine-h15! + r2-Dez-3/3-Zemelj-h17-MUC! + r3-Dez-26/26-GRIBLJE-h11-Anna! + r4-Dez-18/19-RETRO-DUEL-Gradac-h55!) + glava-'Jahr 1875' + 'finis-Anni-1875'-VELIKA-KALLIGRAFIJA-'finis'-LEVO-'An-ni-1-8-75'-DESNO-PARALELA-'Incipit-annus-Domini-1877'-P229! | s65 = glava-'Jahr 1876'-BREZ-INCIPIT-P229-LEAD-PREDPOSTAVKA-NAPAČNA! + RESTART-z1-NA-DAN-5./5.-JÄNNER-Aloshor[?]-h24-Agnes-Hampauhar[?]/Schweiger!-10.-restart-z1-linija!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!-P229-9./10.!-P230-5./5.!) = 69.-POTRDITEV-invariante! (68.-P229!)** + **★★★ 100-VPISOV-DISTINCT (z1–z100!) — vrstna-aritmetika 7+7+7+8+9+8+8+7+8+8+7+7+8+1 = 100 + zap-stolpci-VIDNI-×6-strani-1:1 (s65:1–7!-s66:8–14!-s67:15–21!-s68:22–29!-s69:30–38!-s70:39–46!-P229-×6-PARALELA!) + s77-zap-'94'-MODRA (z94-GRIBLJE-h31!) + s78-r1-zap-'100'-X-open + TWINS-SHARED-ZAP-VARIANTI (s69-r9-Anna+Katharina-zap-38-ISTI!)** + **★★★ 14-GRIBLJE / 14-hiš-BREZ-DUPLIKATOV (h7-h8-h15-h16-h20-h22-h25-h31-h39-h40-h44-h53-h55-h62!-vs-P229-18-hiš-h6/h14-×2!): z22-h40-Maria-PEZDIRC-oče-garble!-Hoggia! + z26-h39-Georg-SIMEC-oče! + z28-h20-Mathias-PEZDIRC-oče-P229-z84-PARALELA! + z32-h16-Joannes-HRIŽAN-boter! + z43-h7-Anna-HRIŽAN-matec!-HURE-boter!-'als-Amtsvormund'-NOTA! + z46-h15-Nicolaus-MUC-oče! + z53-h22-Katharina-MILEK-oče!-PEZDIRC-matec!-MESEC-DUEL!-MODRI-†7.10.1931! + z85-h53-Maria-PEZDIRC-DVOJNI!-DRAGOŠ-boter! + z86-h62-Nicolaus-MODRI-umrl-23.12.1953!-MILEK+BRODARIČ-botra! + z88-h25-Mathias-BRINC-oče!-MODRI-†9.12.1935! + z92-h8-Catharina-JAKOFČIČ-oče!-BRODARIČ-matec!-DRAGOŠ-boter! + z96-h55-Maria-SIMEC-oče!-PEZDIRC-DVOJNI! + z98-h44-Barbara-KLOBUČAR-DVOJNI! + z94-h31-Nicolaus-PEZDIRC-matec!-ŽUPANIČ-DVOJNI!-zap-'94'-MODRA!-MODRI-umrl-18.9.1961!** + **★★★ PEZDIRC-×18-vrstic-NOV-REKORD-LINJE-continuum-10-let (×4/×4/×6/×4/×9/×14/×12/×17/×11/×18!-×2-DVOJNI-GRIBLJE-h53-oče+boter!-h55-matec+botra!-×7-Griblje + ×11-ne-Griblje!)** + JAKOFČIČ-×8 + MILEK-×5 + BRODARIČ-×7 + KLOBUČAR-×5 (z98-DVOJNI!) + HRIŽAN-×6 + SIMEC-×3 (2×-Nicolaus!) + DEBLIČ-×3 + DRAGOŠ-×2-KOMPLET + MUC-×4 + ŽUPANIČ-×2-DVOJNI + HURE-×1 + **★★★ DVOJČKI-×4-dogodki-REKORD-NOVI-VARIANTI (2-BRACE-'Zwillinge'-vertikalna-nota: s71-r4/r5-Peter+Michael-Krasine-h25-Aug-19/20! + s73-r3/r4-Petrus+Maria-Certoviše-h26-Sep-15/15! + 2-SHARED-ROW-NOVI: s71-r6-Nicolaus+Martin-'Gri-moršk[?]'-h15-Juli-25/25! + s69-r9-Anna+Katharina-Goriče-h25-Juni-4/5-zap-38-ISTI!-vs-×4-P229-ALL-BRACE!)** + **★★★ NEZAKONSKI-×6-REKORD (s66-r6-Krasine-h34-Maria-Kralj-dolga-nota! + s72-r3-Zemelj-h22-oče-dash! + s72-r7-Certoviše-h13! + s77-r7-Grem-h33-Šelah-matec! + s74-r2-Boginja-vas-h42-dolga-matec-nota! + s72-r6-'Griže'-h55-WOLFGR!-vs-×5-P228!)** + **★★★ WOLFGR-ANOMALIJA-DRUŽINA-×3-NOVA ('Wolfgrabiff[?]'-s69-r1-Gradac! + 'Wolfgr-Annišl[?]'-s70-r1-Gradac! + 'Wolfgr-Daisl[?]'-s72-r6-'Griže'-RETRO!-VSI-3-botra+duhovnik-PRAZNI!-samo-hebamme-Maria-Rom-×2!-P229-TODTGEBOREN-GARBLE-DRUŽINA-PARALELA!)** + **★★★ MODRI-×11-linij-REKORD (Griblje-×4-†: h22-†7.10.1931-črnilo-floret! + h62-umrl-23.12.1953-MODRA! + h25-†9.12.1935-črnilo! + h31-umrl-18.9.1961-MODRA-dolg-por-1914! + ne-G-×7: CHICAGO-1970! + MMK-Metlika-1962-dolg! + MMK-Novo-mesto-1963! + umrl-18.8.1946-poročen-1911! + umrl-5.1.1950! + umrla-9.10.1956! + umrla-20.3.1957!-1931–1970-razpon!)** + **★★★ 'als-Amtsvormund'-botra-NOTA-NOVI-TIP (z43-h7-Maria-Jetter-als-Amtsvormund-der-Ehegatten-Tochter-uradni-skrbnik!)** + ★★★ RETRO-VPISI-×2 (s72-r6-'Griže'-25/25-PO-28/29! + s64-TAIL-r4-Gradac-18/19-PO-26/26!-P229-z97/z98-PARALELA!) + ★★★ zap-'94'-MODRA + HEBAMME-Maria-Rom-×9-continuum (botra-×2 + hebamme-×7-Gradac!) + RED-tički-✓-margin-continuum + rojen≠krsten-Griblje-×4 + vas-garble-DUELI ('Gritže'-Griče-s66-r4! + 'Grilže'-s72-r6! + 'Gri-moršk'-s71-r6! + 'Aloshor[?]'-s65-r1!) + hišne-DUELI (h6/67! + h55-sof/ad! + h20-pmix-16! + h7-'až7'!) + **★★★ DUHOVNIŠKA-IZMENJAVA-1876 ('Hoggia/Roggja/Hoggin-Coop'-KURRENT-DUEL-4-varianti ↔ 'Franz-Dovgan'-ALTERNIRAJÖČE!-Griblje-split-7/7-POPOLNOM-IZENAČEN-vs-P229-13/7!)** + meseci-Griblje: M1+A2+Mai1+Juli2+A[?]1+S3+O1+N2+D1 = 14 (Jänner/Feber/Juni-×0!-3-prazne!) + **14 NOVIH BLOKOV parish.ts: vitals 1839 → 1870 · 04104 = 187 → 201 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p230 (fetch-2×-md5-15/15 + VIZUALNO-arhivar-branje-×15! + krops-8-sheet-×69 + mikro-krop-K + build-entries + build-proof) + qa-p230 (230. kontrola!) + dokaz parish-baptism-1876-04104.json (100-DISTINCT: 14-Griblje + 86-druge! anomalije/crossChecks/honesty!) + pt-luknja-201/1870; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-10/15-LET!** (P231-LEAD: 1875 — MEJA-1875/76-ŽE-NAJDENA-s64/s65-DVO-STRANSKA → 1875 = TAIL-s64-×4-vrstic-ŽE-VLM! → MEJA-1874/75-pred-s64 → probe-s57–s64-DESCENDING! — gola-pag-'sken−5'-pričakovana-s57='52'! (s64='59'!) — POZOR: 'finis-Anni'-kalligrafija-LAHKO-se-ponovi!-1875-vpisov-NEZNANO-št.)",
    "P230: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1876 = 10/15 (issue #18): the-frame — s64–s78 (15 scans; 2×-INDEPENDENT-md5-15/15!) + the-plain-pencil-pag-'scan−5'-15/15-SEQUENTIAL (s64='59'/s65='60'/s71='66'-3×-VISUALLY-SEEN!/s78='73'!-59–158-continuum!) + **★★★ THE-1875/76-BOUNDARY = s64/s65-TWO-PAGE-NEW-VARIANT (s64 = the-TAIL-1875-×4-rows-incl.-GRIBLJE-h11-Anna-Dez-26/26! + the-'Jahr 1875'-header + 'finis-Anni-1875'-THE-GREAT-CALLIGRAPHY-'finis'-LEFT-'An-ni-1-8-75'-RIGHT-THE-PARALLEL-OF-'Incipit-annus-Domini-1877'! | s65 = the-'Jahr 1876'-header-WITHOUT-INCIPIT-the-P229-LEAD-ASSUMPTION-WRONG! + the-RESTART-z1-ON-DAY-5./5.-JÄNNER-Aloshor[?]-h24-Agnes!-the-10th-restart!) = the-69th-CONFIRMATION!** + **★★★ 100-ENTRIES-DISTINCT (z1–z100!) — the-row-arithmetic 7+7+7+8+9+8+8+7+8+8+7+7+8+1 = 100 + the-zap-columns-VISIBLE-×6-pages-1:1 + s77-zap-'94'-BLUE + the-TWINS-SHARED-ZAP-VARIANTS!** + **★★★ 14-GRIBLJE / 14-houses-WITHOUT-DUPLICATES** + **★★★ THE-PEZDIRC-×18-ROWS-THE-NEW-RECORD-THE-CONTINUUM-10-YEARS (×2-DOUBLE-GRIBLJE!)** + JAKOFČIČ-×8 + MILEK-×5 + BRODARIČ-×7 + KLOBUČAR-×5 + HRIŽAN-×6 + SIMEC-×3 + DRAGOŠ-×2 + MUC-×4 + **★★★ THE-TWINS-×4-EVENTS-RECORD-THE-NEW-VARIANTS (2-BRACE + 2-SHARED-ROW-the-zap-38-IDENTICAL!)** + **★★★ THE-ILLEGITIMATE-×6-RECORD** + **★★★ THE-WOLFGR-ANOMALY-FAMILY-×3-NEW (the-godparents+priest-ALL-EMPTY-the-midwife-only-PARALLEL-OF-THE-STILLBORN-GARBLE-FAMILY!)** + **★★★ THE-BLUE-ANNOTATIONS-×11-RECORD (×4-GRIBLJE-†! + CHICAGO-1970! + MMK-×2!-the-1931–1970-span!)** + **★★★ THE-'als-Amtsvormund'-godparent-NOTE-THE-NEW-TYPE** + the-RETROACTIVE-ENTRIES-×2 + the-zap-'94'-BLUE + HEBAMME-Maria-Rom-×9 + the-RED-ticks + **★★★ THE-PRIEST-ALTERNATION-1876 (Griblje-split-7/7-EXACTLY-EQUAL-vs-P229-13/7!)** + **14 NEW BLOCKS: the vitals 1839 → 1870 · the 04104 = 187 → 201**; the scripts p230 + qa-p230 (the 230th check!) + the evidence parish-baptism-1876-04104.json (100-DISTINCT: 14-Griblje + 86-others!) + the pt-gap-201/1870; **★★★ THE-BAPTISM-PREHISTORY-LINE-10/15-YEARS!** (the P231-LEAD: 1875 — the-boundary-ALREADY-FOUND-s64/s65 → the-TAIL-s64-×4-rows! → probe-s57–s64-DESCENDING!)",
    p230Errors.length === 0,
    p230Errors.length === 0
      ? `14 vpisov / 100-DISTINCT (z1–z100!-zap-1:1-×6-strani + zap-'94'-MODRA!) / 14-hiš-BREZ-DUPLIKATOV · MEJA-1875/76-s64/s65-DVO-STRANSKA-69.-POTRDITEV (finis-Anni-1875-KALLIGRAFIJA!-RESTART-z1-5./5.!-10.-restart!-BREZ-INCIPIT!) · FOLIACIJA-sken−5-15/15 (59–73!-3×-NARISE!) · PEZDIRC-×18-NOV-REKORD-continuum-10-let (×2-DVOJNI!) · DVOJČKI-×4-NOVI-VARIANTI (2-BRACE + 2-SHARED-ROW!) · NEZAKONSKI-×6-REKORD · WOLFGR-DRUŽINA-×3-NOVA · MODRI-×11-REKORD (CHICAGO-1970!-MMK-×2!) · 'als-Amtsvormund'-NOTA · zap-'94'-MODRA · DUHOVNIKI-7/7-IZENAČEN · meseci-Jänner/Feber/Juni-×0 · **LINIJA-10/15!** · vitals 1870 · 04104 201`
      : p230Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1839", "HOUSE_VITALS.length !== 1870")
# P229-block 04104-total: 187 → 201 (zdaj vključuje 1876!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 187)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 201)')
src = src.replace('p229Errors.push(`bloki 04104 ≠ 187 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877 = 187!)`)',
                  'p229Errors.push(`bloki 04104 ≠ 201 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876 = 201!)`)')
# yearset-04104: {1877..1885} → {1876,...,1885} (v P229-, P228-, P227-, P226-, P225-blokih!)
old_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
new_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
n_y = src.count(old_yearset)
src = src.replace(old_yearset, new_yearset)
for ph in ("p229Errors", "p228Errors", "p227Errors", "p226Errors", "p225Errors"):
    src = src.replace(f'{ph}.push("04104-bloki izven {{1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-9/15: 1877–1885-do-P230!)");',
                      f'{ph}.push("04104-bloki izven {{1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-10/15: 1876–1885-do-P231!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1870×{src.count('HOUSE_VITALS.length !== 1870')} · qa-p230×{src.count('qa-p230-parish-baptism-1876-04104')} · yearset-patched-{n_y}")

# --- skripte + verifierji patch (1839→1870, 187→201) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p230_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1839" not in t: continue
    o = t
    t = t.replace("1839", "1870")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p230" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1839", "vitals == 1870"), ("vitalsTotal == 1839", "vitalsTotal == 1870"),
                 ('vitalsTotal"] == 1839', 'vitalsTotal"] == 1870'),
                 ('"vitalsTotal": 1839', '"vitalsTotal": 1870'),
                 ('\\"vitalsTotal\\": 1839', '\\"vitalsTotal\\": 1870'),
                 ('!== 1839"', '!== 1870"'),
                 ("1839-številcev", "1870-številcev"),
                 ("vitals-števec-1839", "vitals-števec-1870"), ("vitals-1839", "vitals-1870")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 187 → 201
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 187}', '"04104": 201}')
t = t.replace("# POSODABLJENO P229: + krstna-04104 = 187 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229!)",
              "# POSODABLJENO P230: + krstna-04104 = 201 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (201)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1870
pt["corpus"]["byBook"]["04104"] = 201
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P230: +14-blokov-1876-krstna-04104-10/15 (vitals 1839→1870; 04104 187→201; 100-DISTINCT z1–z100 + zap-1:1-×6-strani + s77-zap-'94'-MODRA + 14-GRIBLJE/14-hiš-BREZ-DUPLIKATOV + MEJA-1875/76-s64/s65-DVO-STRANSKA-69.-POTRDITEV ('finis-Anni-1875'-KALLIGRAFIJA!-RESTART-z1-5./5.!-10.-restart!-BREZ-INCIPIT!) + FOLIACIJA-sken−5-15/15 (59–73!-3×-NARISE!) + PEZDIRC-×18-NOV-REKORD-continuum-10-let + DVOJČKI-×4-NOVI-VARIANTI (2-BRACE + 2-SHARED-ROW!) + NEZAKONSKI-×6-REKORD + WOLFGR-DRUŽINA-×3-NOVA + MODRI-×11-REKORD (CHICAGO-1970!-MMK-×2!) + DUHOVNIKI-7/7-IZENAČEN → P231-LEAD-1875)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
