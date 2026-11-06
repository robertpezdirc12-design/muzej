#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 — INSERT qa-p202 blok v qa-parish.ts (pred qa-p201-anchor)."""
from pathlib import Path

QA = Path("/home/z/my-project/src/lib/qa-parish.ts")
src = QA.read_text(encoding="utf-8")

ANCHOR = "  // ——— qa-p201: MRLIŠKA PREDZGODOVINA 04106 — leto 1876 = 10. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1, f"anchor-qa={src.count(ANCHOR)}"
assert "qa-p202-parish-death-1875-04106" not in src, "qa-p202-že-obstaja?!"

BLOCK = '''
  // ——— qa-p202: MRLIŠKA PREDZGODOVINA 04106 — leto 1875 = 11. leto PREDZGODOVINSKE
  //      LINIJE (issue #18; knjiga 1857–1885!).
  //      1875 = 71 vpisov (z1–z71, ŠTEVJE-IZ-VRSTIC — ordinali-NEVIDNI-×8!) /
  //      10 Griblje / 10 hiš (★★★ 5-NOVIH: h11/h35/h45/h59/h72!) + ★★★
  //      MEJA-1874/75-s127 (TAIL-10-NOV/DEZ-1874 + 'Jänner 1875'-glava-v-z11-
  //      celici = 42.-POTRDITEV + z1-ULEDBA-31-Dez→2-Jän!) + ★★★ GLAVE-V-
  //      CELICAH-×6-REKORD (42.+43.+44.-POTRDITVI + Juli/November/Dezember!)
  //      + ★★★ KOGEJ-OBDOBJE-3.-RAZŠIRITEV ('provinciat'-RANK-1875!) +
  //      ★★★ DOVGAN-DOMINANTA-×23 + 5-NOVIH-HIŠ-REKORD + PEZDIR-DUEL-#1 +
  //      KROP-FALSIFIKACIJA-#9 + GEORG-HUSIČ-DUEL + BRAUŠ-NIT-×2.
  //      Dokaz: parish-death-1875-04106.json; skripte p202 (fetch-md5 + read +
  //      crop + build-entries + build-proof).
  {
  const p202Errors: string[] = [];
  const p202Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1875);
  if (p202Death.length !== 10)
    p202Errors.push(`bloki 1875 (04106) ≠ 10 (${p202Death.length} — 10 Griblje-vpisov / 71 vpisov vrstno-štetje!)`);
  const p202Houses = p202Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p202Houses.join(",") !== "5,11,17,22,31,35,45,59,69,72")
    p202Errors.push(`hiše 1875 neujemane — najdeno: ${p202Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1385)
    p202Errors.push(`HOUSE_VITALS ≠ 1385 (${HOUSE_VITALS.length} — P201: 1375; P202: + 10 blokov 1875-04106 = 1385!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 166)
    p202Errors.push(`bloki 04106 ≠ 166 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 166!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p202Errors.push("04106-bloki izven {1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1874 še nebrani!)");
  if (!p202Death.some((h) => h.houseNo === "59" && h.whatSi.includes("PEZDIR-GRAFIA-DUEL-#1")))
    p202Errors.push("★★★ PEZDIR-GRAFIA-DUEL-#1 (z9-'Peglinc[?Bezdira?]'-h59 — PEZDINC-nit-kontekst!) ni označena");
  if (!p202Death.some((h) => h.houseNo === "35" && h.whatSi.includes("KROP-FALSIFIKACIJA-VLM-#9")))
    p202Errors.push("★★★ KROP-FALSIFIKACIJA-VLM-#9 (z27-'Miha-Nemanič'-moško-NE-'Matthea-Klemencic'!) ni označena");
  if (!p202Death.some((h) => h.houseNo === "72" && h.whatSi.includes("KURRENT-DUEL-RAZREŠEN")))
    p202Errors.push("★★★ h72-KURRENT-DUEL-RAZREŠEN (z40-'Griblje 72.'-NE-h73! BRAUŠ-nit!) ni označena");
  if (!p202Death.some((h) => h.houseNo === "11" && h.whatSi.includes("P201-lead-NAPVED-1:1-POTRJENA")))
    p202Errors.push("★★★ h11-P201-lead-1:1 (z71-KUNIĆ-geb.-JAKOŠ-65J-Dez-24/26!) ni označena");
  if (!p202Death.some((h) => h.houseNo === "69" && h.whatSi.includes("GEORG-HUSIČ-DUEL-s133")))
    p202Errors.push("★★★ GEORG-HUSIČ-DUEL-s133 (z58-Gradac-37J + z59-Griblje-27J — isti-dnevi-26/28!) ni označena");
  if (!p202Death.some((h) => h.houseNo === "31" && h.whatSi.includes("provinciat Hogeyu Coop.")))
    p202Errors.push("★★★ KOGEJ-'provinciat'-RANK (z17-Hogeyu + z18-'Kooci'-eksplicitno!) ni označena");
  push(
    "qa-p202-parish-death-1875-04106",
    "P202: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1875 = 11. LETO PREDZGODOVINSKE LINIJE (issue #18; knjiga 1857–1885!): okvir — s127-z11–s134-z4 == Pag. 121–128 (stran == sken − 6! md5-križna-validacija-verige-P197→P198→P199→P200→P201→P202: s134-svež == P201-disk-1:1 — 6.×!) + **MEJA 1874/75 = s127 (TAIL-10-NOV/DEZ-1874-nad — NAJVEČJI-tail-v-korpusu! 2-GRIBLJE: r1-Krič[?] + r4-Miler[?]! + 'Jänner 1875'-GLAVA-V-Z11-CELICI = 42.-POTRDITEV-invariante + z1-ULEDBA: smrt-31-Dez-1874 → pokop-2-Jän-1875 — pokop-v-novem-letu!)** + MEJA 1875/76 = s134 (P201-REUSE-1:1-MD5: TAIL-4-DEZ-1875 + VELIKA-'1876 Jänner'-glava — POPOLNA-SOGLASJA-Z-P201!) + **★★★ GLAVE-V-DATUMSKI-CELICAH-×6-korpus-REKORD: 42.-'Jänner 1875'-s127-z11 (z-letom!) + 43.-'März'-s128-z6 + 44.-'1875'-s133-z1 (KROP-eksplicitno — VIOLETNA-TINTA!) + mesečne-podpore Juli-s131-z6/November-s133-z2/Dezember-s133-z10!** + **★★★ 71-VPIISOV — ŠTEVJE-IZ-VRSTIC** (ordinali-NEVIDNI-×8! recept-4.×! vrstna-aritmetika 1+11+10+13+12+10+10+4 + meseci J3+F3('Feber'-grafa!)+M15-MAX+A7+M6+J6+J1-MIN+A6+S6+O4+N8+D5 = 71!) + **★★★ KOGEJ-OBDOBJE-3.-RAZŠIRITEV-NAZAJ — 'provinciat'-RANK-1875** (provinciat-Hogeyu-z17 + provinciat-Kooci-z18-eksplicitno + Feldkurat-Bogija-Corp.-×5 — 1875→1876→1877-NEPREKINJENO!) + **★★★ DOVGAN-DOMINANTA-×23** (Dovgan-7 + Dorgai-6 + Dorgam-3 + franzy-Dorgan-3 + Lovšar-[Dovgan?]-4 — NAJVEČJA-letnica!) + **★★★ 5-NOVIH-HIŠ-REKORD-1870s** (h11 + h35 + h45 + h59 + h72!) + niti-RAZŠIRJENE-NAZAJ: h5-10-letna (1875→1880/85!) + h69-9-letna (→1882/84!) + h17/h22/h31! + **★★★ PEZDIR-GRAFIA-DUEL-#1** (z9-'Peglinc[?Bezdira?]'-h59 — PEZDINC-h53-1876/77-kontekst!) + **★★★ KROP-FALSIFIKACIJA-VLM-#9** (z27-VLM-'Matthea-Klemencic'-ŽENSKO → KROP-'Miha-Nemanič'-MOŠKO-potrjeno!) + **★★★ GEORG-HUSIČ-DUEL-s133** (z58-Gradac-37J-Okt-26/28 + z59-Griblje-27J-Nov-26/28 — ista-imena + isti-dnevi-RAZLIČEN-mesec — 2-vpisa-KROP + [~]-dvojnost!) + **★★★ BRAUŠ-NIT-×2-1875** (z11-h45-sohn-der-Anna-Braußsche + z40-h72-sohn-des-Marcus-Brauše!) + ★ h72-KURRENT-DUEL-RAZREŠEN (KROP-'Griblje 72.'-2/3-NE-h73!) + ★ '24'-ENOTA-ZMEDA-×2 (z17-'24 7/8' + z18-'24' — leta/tednov-NEJASNA — isti-datumi-März-21/23!) + ★ ZIMSKI-KLASTER-GRIBLJE-MÄRZ-×4 (4-od-10!) + ★ FRISEN-NIT-×2 (z40-h72 + z59-h69!) + ★ 'Feber'-GRAFA-×3 (s128!) + ★ Juli-1-MIN (skoraj-mrtvi-mesec!) + ★ z18-'¾ J.'-glif-v-napačnem-stolpcu + ★★★ OTROŠKA-UMRLJIVOST-30%-3/10-jasna (2-Mes + 4½-Mon + 5-Tednov; +2-[?]-mejna — če-tednov → 50%!); **1875 = 71 vpisov (z1–z71) / 10 Griblje-vpisov / 10 hiš**; **10 NOVIH BLOKOV parish.ts: vitals 1375 → 1385 · 04106 = 156 → 166 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p202 (fetch-md5 + read + crop + build-entries + build-proof) + qa-p202 (202. kontrola!) + dokaz parish-death-1875-04106.json (71 entries: 10-Griblje + 61-druge! 14-anomalij + 10-crossChecks + honesty-16 + tail_1874-×10 + leadP203-1874!) + pt-luknja-REGENERACIJA (166/1385!); **★★★ PREDZGODOVINA-LINIJA-11/29-LET!** (P203-LEAD: 1874 — s127-TAIL-×10-ŽE-PREBRAN (2-Griblje: Krič[?] + Miler[?]!) + s126-ŽE-FETCHAN → probe-s118–s127!)",
    "P202: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1875 = THE 11th YEAR OF THE PREHISTORY LINE (issue #18): the frame — s127-z11–s134-z4 == pages 121–128 (page == scan − 6! the-md5-cross-validation-of-the-chain-P197→…→P202: s134-fresh == P201-disk-1:1 — the-6th-time!) + **THE 1874/75 BOUNDARY = s127 (the-TAIL-10-NOV/DEZ-1874-above — the-BIGGEST-tail-in-the-corpus! 2-GRIBLJE! + the-'Jänner 1875'-HEAD-IN-THE-Z11-CELL = the-42nd-INVARIANT-CONFIRMATION + the-z1-ULEDBA: death-31-Dec-1874 → burial-2-Jän-1875 — the-burial-in-the-new-year!)** + the 1875/76 boundary = s134 (the-P201-REUSE-1:1-MD5: the-TAIL-4-DEZ-1875 + the-BIG-'1876 Jänner'-head — the-FULL-AGREEMENTS-WITH-P201!) + **★★★ THE-HEADS-IN-THE-DATE-CELLS-×6-the-corpus-RECORD: the-42nd-'Jänner 1875'-s127-z11 (with-the-year!) + the-43rd-'März'-s128-z6 + the-44th-'1875'-s133-z1 (KROP-explicit — VIOLET-INK!) + the-monthly-supports-Juli/November/Dezember!** + **★★★ THE-71-ENTRIES — THE-COUNT-FROM-ROWS** (the-ordinals-INVISIBLE-×8! the-recipe-4th-time! the-row-arithmetic 1+11+10+13+12+10+10+4 + the-months + 'Feber'-the-graphia + März-15-MAX + Juli-1-MIN!) + **★★★ the-KOGEJ-PERIOD-THE-3rd-EXTENSION-BACK — the-'provinciat'-RANK-1875** (provinciat-Hogeyu-z17 + provinciat-Kooci-z18-explicit + Feldkurat-Bogija-Corp.-×5 — 1875→1876→1877-UNINTERRUPTED!) + **★★★ the-DOVGAN-DOMINANCE-×23** (the-BIGGEST-year!) + **★★★ 5-NEW-HOUSES-RECORD-1870s** (h11 + h35 + h45 + h59 + h72!) + the-threads-EXTENDED-BACK: h5-the-10-YEAR-thread + h69-the-9-YEAR-thread + h17/h22/h31! + **★★★ the-PEZDIR-GRAFIA-DUEL-#1** (z9-'Peglinc[?Bezdira?]'-h59!) + **★★★ the-KROP-FALSIFICATION-VLM-#9** (z27-the-VLM-'Matthea-Klemencic'-FEMALE → KROP-'Miha-Nemanič'-MALE-confirmed!) + **★★★ the-GEORG-HUSIČ-DUEL-s133** (z58-Gradac-37J-Oct-26/28 + z59-Griblje-27J-Nov-26/28 — the-same-names + the-same-days-different-month!) + **★★★ the-BRAUŠ-THREAD-×2-1875** (z11-the-mother + z40-the-father!) + ★ the-h72-KURRENT-DUEL-RESOLVED (h72-NOT-h73!) + ★ the-'24'-UNIT-CONFUSION-×2 (years/weeks-[?]!) + ★ the-WINTER-CLUSTER-GRIBLJE-MÄRZ-×4 + ★ the-FRISEN-THREAD-×2 + ★ the-'Feber'-GRAFIA-×3 + ★ Juli-1-MIN + ★★★ the-CHILD-MORTALITY-30%-3/10-clear (+2-[?]-borderline!); **1875 = 71 entries / 10 Griblje / 10 houses**; **10 NEW BLOCKS: the vitals 1375 → 1385 · the 04106 = 156 → 166 · the 04894 = 520-UNCHANGED**; the scripts p202 + the qa-p202 (the 202nd check!) + the evidence parish-death-1875-04106.json (71 entries!) + the pt-gap-REGENERATION (166/1385!); **★★★ THE-PREHISTORY-LINE-11/29-YEARS!** (the P203-LEAD: 1874 — the-s127-TAIL-×10-ALREADY-READ (2-Griblje!) + the-s126-ALREADY-FETCHED → the-probe-s118–s127!)",
    p202Errors.length === 0,
    p202Errors.length === 0
      ? `10 vpisov / 71 vrstic (števje-iz-vrstic-4.×!) / 10 hiš (5-NOVIH-rekord!) · MEJA-s127-TAIL-10 + 42.-43.-44.-POTRDITVI-celici (×6-rekord!) · KOGEJ-'provinciat'-1875 (3.-razširitev!) · DOVGAN-×23 · PEZDIR-DUEL-#1 · KROP-FALSIFIKACIJA-#9 · GEORG-HUSIČ-DUEL · BRAUŠ-×2 · h72-KURRENT-RAZREŠEN · otroška-umrljivost-30% (+2-[?]!) · **PREDZGODOVINA-11/29!** · vitals 1385 · 04106 166 · 04894 520`
      : p202Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
QA.write_text(src, encoding="utf-8")
print(f"OK — qa-p202 vstavljen ({len(BLOCK)} znakov)")
print("qa-p202-blokov:", src.count("qa-p202-parish-death-1875-04106"))
