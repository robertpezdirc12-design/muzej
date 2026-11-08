#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P226 — INSERT qa-p226 + sanitizacija (1759→1870, 04104=107→129, yearset-04104-{1880..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p225: KRSTNA PREDZGODOVINA 04104 — leto 1881 = 5/15"
assert src.count(ANCHOR) == 1 and "qa-p226-parish-baptism-1880-04104" not in src

BLOCK = '''
  // ——— qa-p226: KRSTNA PREDZGODOVINA 04104 — leto 1880 = 6/15
  //      (P225: 1881 = 5/15!). 1880 = 122 vpisov-DISTINCT (vrstna-aritmetika
  //      8+9+9+8+7+9+7+6+7+8+7+8+8+7+7+7 = 122 = P225-LEAD-'1880 = 122'-1:1-INVARIANTA! —
  //      zap-stolpci-16/16-ČISTO!) / 22-GRIBLJE / 20-hiš (h27-×2 + h24-×2-DUELI-REŠENI!) +
  //      ★★★ MEJA-1879/80-s119/s120 (TAIL-1879-z92–z96 + Schnörkel + 'Jahr 1879'-BREZ-VSOTNE! +
  //      velike-cifre-'1/8/8/0'-P214-TIP + 'Jahr 1880'-glava + RESTART-z1-NA-DAN-3.-1.-JÄNNER-
  //      Dobravce-h11!-5.-restart-z1!) = 65.-POTRDITEV + ★★★ FOLIACIJA-'sken−6'-17/17-SEKVENČNO
  //      (113–129!-s129-9↔3 + s133-4↔7-VLM-misreada-REŠENA!) + ★★★ PEZDIRC-×14-NOV-REKORD-LINJE
  //      (z35-DVOJNI! z99-DVOJNI! + ×10-ne-Griblje!-continuum-6-let!) + KRIŽAN-×9 (2-DVOJNI!) +
  //      JAKOFČIČ-×10 + ★★★ DVOJČKI-Boršt-h20 (z5/z6-ne-Griblje!-P223-PARALELA!) + ★★★
  //      Mißgeburt-'Mößgelauffer'-×2 (z76/z77!) + ★★★ z110-KRSTEN-PRAZEN + BOTRA-PRAZNA +
  //      ★★★ NEZAKONSKI-×7-REKORD (očetov-stolpec-PRAZEN!-incl.-z114-GRIBLJE!) + ★★★
  //      MODRI-MATIČARSKI-PRIPISI-×9 (1963–1990!) + pripisi-MMK-†-×7 + Z49-datumski-popravek +
  //      Z100-imenski-popravek (P221-PARALELA!) + z79-JULI-REŠEN + z15-FEB-20-SANDWICH +
  //      DUHOVNIŠKA-MENJAVA (Janičar→Dovgan!) + meseci-Griblje F3+M4+Mai3+J2+Juli2+S2+O3+N1+D1
  //      (Jänner/April/August-×0!). Dokaz: parish-baptism-1880-04104.json; skripte p226.
  {
  const p226Errors: string[] = [];
  const p226Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1880);
  if (p226Bapt.length !== 22)
    p226Errors.push(`bloki 1880 (04104) ≠ 22 (${p226Bapt.length} — 22 Griblje-vpisov / 20-hiš (h27-×2 + h24-×2!) / 122-DISTINCT = P225-LEAD-1:1!)`);
  if (HOUSE_VITALS.length !== 1870)
    p226Errors.push(`HOUSE_VITALS ≠ 1870 (${HOUSE_VITALS.length} — P225: 1759; P226: + 22 blokov 1880-04104 = 1870!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 129)
    p226Errors.push(`bloki 04104 ≠ 129 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P225: 107; P226: + 22 × 1880 = 129!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p226Errors.push("04104-bloki izven {1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-6/15: 1880–1885-do-P227!)");
  if (!p226Bapt.some((h) => h.whatSi.includes("RESTART-z1-NA-DAN-3.-1.-JÄNNER-Dobravce-h11") || h.whatSi.includes("65.-POTRDITEV")))
    p226Errors.push("★★★ MEJA-1879/80-s119/s120 (velike-cifre-'1/8/8/0' + RESTART-z1-Dobravce-h11!) ni označena");
  if (p226Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 4)
    p226Errors.push(`★★★ PEZDIRC-×4-in-Griblje (2-DVOJNI!) ni dosežen (${p226Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/4!)`);
  if (!p226Bapt.some((h) => h.whatSi.includes("PEZDIRC-DVOJNI-nit")))
    p226Errors.push("★★★ PEZDIRC-DVOJNI-nit (z35-oče+matec + z99-botra+boter!) ni označena");
  if (p226Bapt.filter((h) => h.whatSi.includes("KRIŽAN")).length < 9)
    p226Errors.push(`★★★ KRIŽAN-×9-rekord ni dosežen (${p226Bapt.filter((h) => h.whatSi.includes("KRIŽAN")).length}/9!)`);
  if (!p226Bapt.some((h) => h.whatSi.includes("KRIŽAN-DVOJNI-nit")))
    p226Errors.push("★★★ KRIŽAN-DVOJNI-nit (z31-matec+boter + z69-matec+botra!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("NEZAKONSKI-vzorec")))
    p226Errors.push("★★★ z114-NEZAKONSKI-vzorec (očetov-stolpec-PRAZEN!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("MODRI-MATIČARSKI-PRIPIS")))
    p226Errors.push("★★★ MODRI-MATIČARSKI-PRIPISI (z26-1969! + z46-1957!) niso označeni");
  if (!p226Bapt.some((h) => h.whatSi.includes("JAKOFČIČ-DVOJNI-nit")))
    p226Errors.push("★★★ z11-JAKOFČIČ-DVOJNI-nit (oče+matec-isti-priimek!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("h27-×2-REŠEN")))
    p226Errors.push("★★★ h27-×2-REŠEN (z46+z54!) ni označen");
  if (!p226Bapt.some((h) => h.whatSi.includes("h24-×2-REŠEN")))
    p226Errors.push("★★★ h24-×2-REŠEN (z65+z72!) ni označen");
  if (!p226Bapt.some((h) => h.whatSi.includes("†-21.8.1935")))
    p226Errors.push("★★★ z11-pripis-MMK-'†-21.8.1935' ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("†-13.9.1940")))
    p226Errors.push("★★★ z89-pripis-MMK-'†-13.9.1940' ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("TOTER-garble-oče")))
    p226Errors.push("★★★ z58-TOTER-garble-oče (P225-z30-PARALELA!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("SIMEC-boter-nit (3/3-KOMPLET")))
    p226Errors.push("★★★ z58-SIMEC-boter-nit (3/3-KOMPLET!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("KLOBUČAR-boter-nit-X-open")))
    p226Errors.push("★★★ z10-KLOBUČAR-boter-nit-X-open (Klebučar!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("LASIE~LAZAR-grafija-X-open")))
    p226Errors.push("★★★ z89-LASIE~LAZAR-grafija-X-open ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("POŽEK-oče-grafija-X-open")))
    p226Errors.push("★★★ z104-POŽEK-oče-grafija-X-open (Pozelj/Pozek!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("'October'-labela-VIZUALNO")))
    p226Errors.push("★★★ z95-'October'-labela-VIZUALNO (VLM-'December'-REŠEN!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("pag-'123'-VIZUALNO")))
    p226Errors.push("★★★ z72-pag-'123'-VIZUALNO (s129-VLM-misread-9↔3-REŠEN!) ni označena");
  if (!p226Bapt.some((h) => h.whatSi.includes("44 [~]")))
    p226Errors.push("★★★ z104-hiša-'44 [~]' (VLM-'(77?)-DUEL'-REŠEN!) ni označena");
  if (new Set(p226Bapt.map((h) => h.houseNo)).size !== 20)
    p226Errors.push(`★★★ 20-hiš-DISTINCT ni izpolnjeno (h27-×2 + h24-×2! — najdeno ${new Set(p226Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p226-parish-baptism-1880-04104",
    "P226: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1880 = 6/15 (issue #18): okvir — s119–s135 (17 skenov; 2×-neodvisna-prenosa-md5-17/17!; s129–s135-proba + s119–s128-probe-nazaj!) + **gola-svinčna-pag-'sken−6'-17/17-SEKVENČNO** (s119='113'/s120='114'/s121='115'/s122='116'/s123='117'/s124='118'/s125='119'/s126='120'/s127='121'/s128='122'/s129='123'-VLM-'129'-misread-9↔3-REŠEN!/s130='124'/s131='125'/s132='126'-VLM-VIZUALNO!/s133='127'-VLM-'124'-misread-4↔7-REŠEN!/s134='128'/s135='129'! — brez-luknje-v-1880-oknu — SKUPNA-SERIJA-113–158-z-1881/1882/1883-okni!) + **★★★ MEJA-1879/80 = s119/s120 (TAIL-1879-z92–z96-Dez-17–30-×5 + 'Schnörkel'-zaključna-vijuga + 'Jahr 1879'-glava-BREZ-VSOTNE + s120-VELIKE-CIFRE-'1/8/8/0'-čez-glavne-celice-P214-TIP (2.-instance!-P222-'1/8/8/4'-PARALELA!) + 'Jahr 1880'-glava + RESTART-z1-NA-DAN-3.-1.-JÄNNER-Dobravce-h11-Martin — 5.-restart-z1 (PARALELA-P221-z1-1.1.-h21!-P222-z1-1.1.-h34!-P223-z1-4.1.!-P224-z1-2.1.-Dobravce!-P225-z1-1.1.-h55!) = 65.-POTRDITEV-invariante! (64.-P225!)** + **★★★ 122-VPIISOV-DISTINCT — ŠTEVJE-IZ-VRSTIC-6.×-ZA-KRSTNO-LINIJO (z1–z122; vrstna-aritmetika 8+9+9+8+7+9+7+6+7+8+7+8+8+7+7+7 = 122 = P225-LEAD-'1880 = 122-vpisov-BONUS'-1:1-INVARIANTA! — zap-stolpci-16/16-ČISTO-brez-duplikatov!)** + **★★★ 22-GRIBLJE / 20-hiš (h27-×2: z46+z54! + h24-×2: z65+z72! — DUELI-REŠENI-1:1-VIZUALNO!-vs-25-TIE-rekord-P221/P224 + 21-P222 + 19-P223 + 17-P225!): z10-h2-KLOBUČAR-X-open! + z11-h9-JAKOFČIČ-DVOJNI-†1935! + z14-h39-SIMEC-oče! + z26-h13-MODRI-1969! + z31-h60-ŽELKO+KRIŽAN-DVOJNI-×2! + z35-h53-PEZDIRC-DVOJNI! + z36-h35-KRIŽAN-oče! + z46-h27-MODRI-1957-MILEK! + z51-h19-SIMEC! + z54-h27-JAKOFČIČ! + z58-h7-TOTER-SIMEC! + z61-h21-BRODARIČ! + z65-h24-JAKOFČIČ! + z69-h42-KRIŽAN-DVOJNI-PEZDIRC! + z72-h24-MILEK-HRIŽAN! + z88-h10-HURE! + z89-h43-LASIE-†1940! + z95-h18-PENT-garble! + z99-h33-PEZDIRC-DVOJNI! + z101-h29-MILEK-KRIŽAN! + z104-h44-POŽEK-KRIŽAN! + z114-h5-NEZAKONSKI-HRIŽAN!** + **★★★ PEZDIRC-×14-NOV-REKORD-LINJE (z35-oče-Joannes+matec-Perdiče-DVOJNI! + z99-boter-Johann+botra-Barbara-DVOJNI! + ×10-ne-Griblje: z3/z7-botra-Pozdire!-z15-boter!-z20-oče!-z29-matec+boter-DVOJNI!-z39-matec!-z57-oče!-z121-oče-Gradac! — grafija-continuum-6-let: P221-×4/P222-×4/P223-×6/P224-×4/P225-×9/P226-×14!)** + KRIŽAN-×9-in-Griblje (z26!-z31-DVOJNI!-z36!-z69-DVOJNI!-z72!-z101!-z104! — 8/9-vidnih!) + JAKOFČIČ-×10-skupaj (z10-matec!-z11-oče+matec-DVOJNI!-z26-oče!-z54-botra!-z65-matec! + ne-G-z13/z53-×2/z63!) + MILEK-×4 (z46-boter!-z72-botra!-z101-oče! + ne-G-z4/z29!) + SIMEC-×3 (z14-oče!-z51!-z58!) + BRODARIČ-×4 (z14!-z35!-z46!-z61!-KOMPLET-nit!) + ŽELKO-×4 (z11!-z31-DVOJNI!) + DRAGOŠ-×2 (z11!-z35!) + HRIŽAN-×2 (z72!-z114!) + TOTER-garble (z58-oče!-P225-z30-PARALELA!) + LASIE~LAZAR-X-open (z89-oče!-P220/P222-nit!) + POŽEK-X-open (z104-oče!-Pozelj/Pozek-DUEL!) + KLOBUČAR-X-open (z10-boter!-Klebučar!) + HURE (z88-oče!-P221-nit!) + **★★★ DVOJČKI-Boršt-h20-z5/z6 (ne-Griblje!-oba-21.-Juli!-isti-starši-Mathias-Rovačič + Kathharina-Jurjefičič!-pisarjev-oklepaj-vertikalna-črta!-2.-DVOJČKI-linije-P223-GRIBLJE-h68-z105/z106-PARALELA!)** + **★★★ Mißgeburt-'Mößgelauffer'-×2 (z76-Certoviše-h11-Anton + z77-Goričice-h5-Martin!-'Mößgelauffer'-garble-~'Mißgeburt'-Stillgeburt-designacija-X-open!-rojen=krsten-26.-Juli-×2!-BOTRA-'—'-PRAZNA!-duhovnik-NI-podpisan!-1.-TIP-v-liniji!)** + **★★★ Z110-KRSTEN-DAN-PRAZEN + BOTRA-PRAZNA (Dobravce-h8-'Ludblendus-garble'-rojen-21.-Nov + krsten-'—' + botra-'—'!-2.-BOTRA-PRAZNA-linije-P225-z48!-1.-KRSTEN-PRAZEN!)** + **★★★ NEZAKONSKI-×7-REKORD-LINJE (očetov-stolpec-PRAZEN!-z30-Dobravce + z56-Kaplišče-✗✗ + z59-Krasinec-'mortua'-opomba + z79-Krasinec + z85-Gradec-'von-Vrhnika' + z100-Podzemelj + ★★★ z114-GRIBLJE-h5!-edini-Griblje!) = 5.7%-vs-×1-P225-z66-'ynb.'-linija!** + **★★★ MODRI-MATIČARSKI-PRIPISI-×9-REKORD (modri-tintnik-1963–1990!-z21-MMK-Ljubljana-1957!-z26-1969!-z46-1957!-z55-1957!-z56-1965!-z68-1955!-z70-1990-MMK-Gradec!-z83-1964-MMK-Primskovo!-z91-1963-MMK-Kranj!)** + pripisi-MMK-†-ink-×7 (z11-'†-21.8.1935'-Griblje! + z42-'†-18[?].1888'-garble! + z45-'umrl-24.3.1949'-'Copul-1879-1903'! + z25-'umrl-17.II.1949'! + z89-'†-13.9.1940'-Griblje! + z105-dolg-garble! + z112-'†-24/5.1919'!) + Z49-DATUMSKI-POPRAVEK ('den-17.-Juli-1880-zuzschreiben'-Boršt-h17!-1.-datumski-popravek-linije!) + Z100-IMENSKI-POPRAVEK ('Alois'-prečrtano→'Alojs-Alojzija' + 'att.-Jos.-Kersy'-garble!-P221-z102-Katharina→Marija-PARALELA!) + ★★★ z79-JULI-MISREAD-REŠEN (VLM-'Juni'→krop-'Juli'-labela-VIZUALNO!-kronologija-z78-Juli-28→z79-Juli-29→z80-Aug-7!-'…ember/Juni'-failure-continuum-P223/P224/P225!) + ★★★ z15-FEB-20-SANDWICH (VLM-'29'-misread-9↔0-ZAVRNJEN-po-kronologiji-z16–z19-Feb-24–26!-prestupno-leto-1880-brez-Feb-29-vpisa!) + z59-vas-DUEL (prečrtano-'Boršt'→'Krasinec'!-'die-4-Wochbř-880-mortua'-opomba!) + z60-vas-DUEL (prečrtano!-P223-z34-PARALELA!) + ★★★ DUHOVNIŠKA-MENJAVA-MID-1880 ('Franz/Franc-Janičar-coep'-z1–z105! → 'Franc-Dovgan'-z106–z122!-menjava-okoli-Nov-z106-X-open!-z101-tretji-podpis-'Jb.-Oberuiter-R.D.Frišt'-garble!) + meseci-Griblje: F3+M4+Mai3+J2+Juli2+S2+O3+N1+D1 = 22 (Jänner/April/August-×0!-3-prazne-rekord!-Feb-prestupno-brez-29!) + 1879 = 96-vpisov-BONUS (s119-tail-z92–z96!-incl.-2-Griblje!→P227-LEAD!) + **22 NOVIH BLOKOV parish.ts: vitals 1759 → 1870 · 04104 = 107 → 129 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p226 (fetch-2×-md5-17/17 + read-×5-VLM + VIZUALNO-arhivar-×12 + krop-86 + build-entries + build-proof) + qa-p226 (226. kontrola!) + dokaz parish-baptism-1880-04104.json (122-DISTINCT: 22-Griblje + 100-druge! 13-anomalij/12-crossChecks/honesty-26!) + pt-luknja-129/1870; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-6/15-LET!** (P227-LEAD: 1879 — 96-vpisov-BONUS-ŽE-ŠTEVJE (s119-tail-z92–z96 + zap-linija!) → MEJA-1878/79-pred-s119 → probe-s112–s119! — gola-pag-'sken−6'-pričakovana-s112='106'!)",
    "P226: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1880 = 6/15 (issue #18): the-frame — s119–s135 (17 scans; 2×-INDEPENDENT-md5-17/17!) + the-plain-pencil-pag-'scan−6'-17/17-SEQUENTIAL (113–129-no-gap!-2-VLM-misreads-RESOLVED-by-krops!) + **★★★ THE-1879/80-BOUNDARY = s119/s120 (the-TAIL-1879-z92–z96 + the-'Schnörkel'-closing-squiggle + the-'Jahr 1879'-header-WITHOUT-THE-SUM-ROW + the-LARGE-DIGITS-'1/8/8/0'-across-the-header-cells-P214-TYPE (the-2nd-instance!-P222-'1/8/8/4'-PARALLEL!) + the-'Jahr 1880'-header + the-RESTART-z1-ON-DAY-3-1-JÄNNER-Dobravce-h11-Martin — the-5th-restart-z1!) = the-65th-CONFIRMATION!** + **★★★ 122-ENTRIES-DISTINCT — the-ROW-COUNTING-6th-×-FOR-THE-BAPTISM-LINE (the-ROW-ARITHMETIC = 122 = the-P225-LEAD-1:1-INVARIANT!-the-zap-columns-16/16-CLEAN!)** + **★★★ 22-GRIBLJE / 20-houses (h27-×2 + h24-×2 — DUELS-RESOLVED-1:1!)** + **★★★ THE-PEZDIRC-×14-NEW-RECORD-OF-THE-LINE (2-DOUBLE-in-Griblje!-×10-non-Griblje!-the-graph-continuum-6-years!)** + KRIŽAN-×9 + JAKOFČIČ-×10 + MILEK-×4 + SIMEC-×3 + BRODARIČ-×4 + ŽELKO-×4 + DRAGOŠ-×2 + HRIŽAN-×2 + TOTER-garble + LASIE~LAZAR-X-open + POŽEK-X-open + KLOBUČAR-X-open + HURE + **★★★ THE-TWINS-Boršt-h20-z5/z6 (non-Griblje!-same-parents!-the-scribe's-bracket!-the-2nd-TWINS-of-the-line-P223-PARALLEL!)** + **★★★ THE-MİSSGEBURT-'Mößgelauffer'-×2 (z76/z77!-the-Stillbirth-designation-1st-TYPE-in-the-line!)** + **★★★ THE-Z110-EMPTY-BAPTISM-DAY + EMPTY-GODPARENT (the-2nd-empty-godparent-P225-z48!-the-1st-empty-baptism-day!)** + **★★★ THE-ILLEGITIMATE-×7-RECORD (the-empty-father-column!-incl.-z114-GRIBLJE!)** + **★★★ THE-BLUE-MATRICULAR-ANNOTATIONS-×9-RECORD (the-blue-ink-1963–1990!)** + the-MMK-†-annotations-×7 + the-Z49-DATE-CORRECTION ('den-17.-Juli-1880-zuzschreiben'!-the-1st-date-correction!) + the-Z100-NAME-CORRECTION (Alois→Alojzija!-P221-PARALLEL!) + the-z79-JULI-MISREAD-RESOLVED (krop>page!-the-'…ember/Juni'-failure-continuum!) + the-z15-FEB-20-SANDWICH (the-VLM-'29'-9↔0-REJECTED-by-chronology!-the-leap-year-without-Feb-29!) + the-vas-DUELS (z59/z60-crossed!) + **★★★ THE-PRIEST-CHANGE-MID-1880 (Janičar-coep→Dovgan-around-z106!-the-3rd-signature-z101!)** + **22 NEW BLOCKS: the vitals 1759 → 1870 · the 04104 = 107 → 129**; the scripts p226 + qa-p226 (the 226th check!) + the evidence parish-baptism-1880-04104.json (122-DISTINCT: 22-Griblje + 100-others!) + the pt-gap-129/1870; **★★★ THE-BAPTISM-PREHISTORY-LINE-6/15-YEARS!** (the P227-LEAD: 1879 — the-96-entries-BONUS-COUNT-ALREADY-KNOWN (s119-tail-z92–z96!) → the-boundary-1878/79-before-s119 → probe-s112–s119!)",
    p226Errors.length === 0,
    p226Errors.length === 0
      ? `22 vpisov / 122-DISTINCT (vrstna-aritmetika = P225-LEAD-1:1!) / 20-hiš (h27-×2 + h24-×2-REŠENA!) · MEJA-1879/80-s119/s120-65.-POTRDITEV (velike-cifre-P214-TIP!-RESTART-z1-Dobravce-h11!-'Jahr 1879'-BREZ-VSOTNE!) · FOLIACIJA-sken−6-17/17-SEKVENČNO (113–129!-2-VLM-misreada-REŠENA!) · PEZDIRC-×14-REKORD-LINJE (2-DVOJNI!-continuum-6-let!) · KRIŽAN-×9 + JAKOFČIČ-×10! · DVOJČKI-Boršt-h20 + Mißgeburt-×2 + z110-KRSTEN-PRAZEN! · NEZAKONSKI-×7-REKORD + MODRI-PRIPISI-×9-REKORD! · DUHOVNIŠKA-MENJAVA (Janičar→Dovgan!) · meseci-J/A/Apr-×0 · **LINIJA-6/15!** · vitals 1870 · 04104 129`
      : p226Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1759", "HOUSE_VITALS.length !== 1870")
# P225-block 04104-total: 107 → 129 (zdaj vključuje 1880!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 107)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 129)')
src = src.replace('p225Errors.push(`bloki 04104 ≠ 107 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881 = 107!)`)',
                  'p225Errors.push(`bloki 04104 ≠ 129 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880 = 129!)`)')
# yearset-04104: {1881..1885} → {1880,...,1885} (v P225-bloku!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p225Errors.push("04104-bloki izven {1881, 1882, 1883, 1884, 1885} (predzgodovina-5/15: 1881–1885-do-P226!)");',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)\n    p225Errors.push("04104-bloki izven {1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-6/15: 1880–1885-do-P227!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1870×{src.count('HOUSE_VITALS.length !== 1870')} · qa-p226×{src.count('qa-p226-parish-baptism-1880-04104')} · yearset-{src.count('(h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885')}")

# --- skripte + verifierji patch (1759→1870) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p226_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1759" not in t: continue
    o = t
    t = t.replace("1759", "1870")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p226" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1759", "vitals == 1870"), ("vitalsTotal == 1759", "vitalsTotal == 1870"),
                 ('vitalsTotal"] == 1759', 'vitalsTotal"] == 1870'),
                 ('"vitalsTotal": 1759', '"vitalsTotal": 1870'),
                 ('\\"vitalsTotal\\": 1759', '\\"vitalsTotal\\": 1870'),
                 ('!== 1759"', '!== 1870"'),
                 ("1759-številcev", "1870-številcev"),
                 ("vitals-števec-1759", "vitals-števec-1870"), ("vitals-1759", "vitals-1870")]:
        t = t.replace(a, b)
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 107 → 129
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 107}', '"04104": 129}')
t = t.replace("# POSODABLJENO P225: + krstna-04104 = 107 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225!)",
              "# POSODABLJENO P226: + krstna-04104 = 129 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (129)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1870
pt["corpus"]["byBook"]["04104"] = 129
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P226: +22-blokov-1880-krstna-04104-6/15 (vitals 1759→1870; 04104 107→129; 122-DISTINCT = P225-LEAD-'1880 = 122'-1:1 + 22-GRIBLJE/20-hiš (h27-×2 + h24-×2!) + MEJA-1879/80-s119/s120-65.-POTRDITEV (velike-cifre-'1/8/8/0'-P214-TIP!-RESTART-z1-Dobravce-h11!-'Jahr 1879'-BREZ-VSOTNE!) + FOLIACIJA-sken−6-17/17-SEKVENČNO (113–129!-2-VLM-misreada-REŠENA!) + PEZDIRC-×14-REKORD-LINJE (2-DVOJNI!-continuum-6-let!) + DVOJČKI-Boršt-h20 + Mißgeburt-×2 + z110-KRSTEN-PRAZEN + NEZAKONSKI-×7-REKORD + MODRI-PRIPISI-×9-REKORD + DUHOVNIŠKA-MENJAVA (Janičar→Dovgan!) + 1879 = 96-BONUS → P227-LEAD)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
