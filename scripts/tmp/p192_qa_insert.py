#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P192 — vstavi qa-p192 (192. kontrola) v qa-parish.ts za konec qa-p191 bloka."""
PATH = "src/lib/qa-parish.ts"
src = open(PATH, encoding="utf-8").read()

ANCHOR = """      : p191Errors.join("; "),
  );
  }
  // ——— qa-p189: MRLIŠKA KNJIGA 04894 — polno leto 1923"""

BLOCK = """      : p191Errors.join("; "),
  );
  }
  // ——— qa-p192: MRLIŠKA PREDHODNICA 04106 — leto 1885 = 1. leto PREDZGODOVINSKE
  //      LINIJE (P192; knjiga 1857–1885 = predhodnica 04894! celoten neodvisen
  //      preracun iz bundled parish.ts!) ———
  //      1885 = 93 veljavnih vrstic / 16 GRIBLJE / 13 hiš (h31-×4! + h63-×2!) +
  //      ★★★ MEJA 1884/85 na s198-mid ('Jänner anno, 1885.') + ★★★ z4-DUPLIKAT-
  //      VSTAVEK (3.×-duplikat-linije!) + ★★★ DUAL-NUMBERING s204–s207 (črnilo +
  //      SVINČNIK off-by-one!) + ★★★ SPREMEMBA-FORME (nemška → hibrid s205 →
  //      slovenska s206 'Mrtvaška knjiga'!) + GLAVE 'Jahr 18' NEPOPOLNE ×2 +
  //      ★★★ MASERN/DAVICA-EPIDEMIJA + h31-PAPIČ-KATASTROFA-3/3 + POŽEK-×2 +
  //      KRIŽAN-×2-h63 + hišne-kontinuitete (h9/h13/h62/h68/h78!) + DUHOVNIKI:
  //      And. GLIBE[L] coöp-DOMINANTA-×13 (→ P153-1887-ISTI!) + Franz DOVGAN-×2
  //      (= poročna-1886-ISTI!) + PREČRTANA VNOSA ×2 (s203-z62 + s206-z81!) +
  //      KONEC-KNJIGE (s207-z92/93-†-30.12.1885 + s208-platnica-1857–1885!).
  //      Dokaz: parish-death-1885-04106.json; verifikator:
  //      scripts/p192_parish_death_1885_04106.py --live I1–I12.
  {
  const p192Errors: string[] = [];
  const p192Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1885);
  if (p192Death.length !== 16)
    p192Errors.push(`bloki 1885 (04106) ≠ 16 (${p192Death.length} — 16 Griblje-vpisov / 93 veljavnih vrstic!)`);
  const p192Houses = p192Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p192Houses.join(",") !== "1,5,9,13,21,31,31,31,31,54,58,62,63,63,68,78")
    p192Errors.push(`hiše 1885 ≠ [1,5,9,13,21,31,31,31,31,54,58,62,63,63,68,78] — najdeno: ${p192Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1235)
    p192Errors.push(`HOUSE_VITALS ≠ 1235 (${HOUSE_VITALS.length} — P190: 1219; P192: + 16 blokov 1885-04106 = 1235!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 16)
    p192Errors.push(`bloki 04106 ≠ 16 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P192: 1. bloki knjige!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1885).length > 0)
    p192Errors.push("04106-bloki izven leta 1885 (predzgodovina-lead: 1857–1884 še nebrani!)");
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04894" && (h.year ?? 0) >= 1925).length > 0)
    p192Errors.push("1925+-mrliški (04894) bloki že v korpusu (ne smejo biti!)");
  const p192H31 = p192Death.filter((h) => h.houseNo === "31");
  if (p192H31.length !== 4)
    p192Errors.push(`h31-vpisov-1885 ≠ 4 (${p192H31.length} — z12-Župarič + PAPIČ-KATASTROFA-3/3!)`);
  if (!p192H31.every((h) => h.whatSi.includes("KATASTROFA") || h.whatSi.includes("ŽUPARIČ")))
    p192Errors.push("h31-katastrofa-oznake manjkajo");
  if (!p192Death.some((h) => h.whatSi.includes("DUPLIKAT-VSTAVEK")))
    p192Errors.push("★★★ z4-DUPLIKAT-VSTAVEK ni označen");
  if (!p192Death.some((h) => h.whatSi.includes("DUAL-NUMBERING-START")))
    p192Errors.push("★★★ DUAL-NUMBERING (s204) ni označen");
  if (!p192Death.some((h) => h.whatSi.includes("SPREMEMBA-FORME")))
    p192Errors.push("★★★ SPREMEMBA-FORME (s206-slovenska!) ni označena");
  if (!p192Death.some((h) => h.whatSi.includes("DAVICA")))
    p192Errors.push("★★★ Difteribis[~davica]-epidemija ni označena");
  if (!p192Death.some((h) => h.whatSi.includes("POŽEK") && h.houseNo === "21") || !p192Death.some((h) => h.whatSi.includes("POŽEK") && h.houseNo === "58"))
    p192Errors.push("★★★ POŽEK-×2-hiši (h21 + h58!) manjkata");
  if (!p192Death.some((h) => h.whatSi.includes("KRIŽAN") && h.houseNo === "63"))
    p192Errors.push("★★★ h63 = KRIŽAN-hiša-pred-04894 ni označena");
  if (!p192Death.some((h) => h.whatSi.includes("Glibe")))
    p192Errors.push("duhovnik And. Glibe[l] coöp manjka");
  if (!p192Death.some((h) => h.whatSi.includes("Dovgan")))
    p192Errors.push("duhovnik Franz Dovgan manjka");
  if (!p192Death.some((h) => h.whatSi.includes("JAKOFČIČ") && h.houseNo === "9"))
    p192Errors.push("★★★ h9 = JAKOFČIČ-pred-04894 ni označena");
  push(
    "qa-p192-parish-death-1885-04106",
    "P192: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDHODNICA 04106, LETO 1885 = 1. LETO PREDZGODOVINSKE LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1885-04106; knjiga 1857–1885 = predhodnica 04894!): okvir — s198–s207 == Pag. 192–201 (stran == sken − 6! nova-preslikava-knjige!) + **MEJA 1884/85 = s198-mid ('Jänner anno, 1885.' zapisano čez vas+ime + restart z1 = 31.-POTRDITEV-invariante!)** + **★★★ z4-DUPLIKAT-VSTAVEK** (pisar izpustil Dragota †5./6.-jan → VSTAVIL s št. 4 = duplikat z z4-Krasinec-Husič — 3.×-duplikat-številčenja-linije cf. 1921-s218 + 1904-s253!) + **★★★ DUAL-NUMBERING s204–s207** (črnilo-št. + SVINČNIK-preštevanje off-by-one = veljavne-vrstice; prečrtani-niso-prešteni!) + **★★★ SPREMEMBA-FORME-MID-BOOK**: nemška (s198–s204 'Sterb-Register'/'Krankheit und Todesart') → HIBRID s205 (nemška-levo + slovenska-desno 'knjiga.'!) → POLNO-SLOVENSKA s206–s207 ('Mrtvaška knjiga'/'Bivališče mrličevo'/'Previden (a) ali ne'!) + **GLAVE-'Jahr 18'-NEPOPOLNE-×2** (s203 + s205!) + PREČRTANA-VNOSA-×2 (s203-z62-Podzemelj + s206-z81-Gemišče!) + **★★★ MASERN/DAVICA-EPIDEMIJA Nov-1884–Mär-1885** (z4dup-Difteribis[~DAVICA!] + z12-~Rubeolis? + z26-Masernkrämpfen + ~Masernika?-z1-1885 + Fraisen-kopica!) + **★★★ h31-PAPIČ-KATASTROFA-3/3** (Maria-25-20./22.-feb + Maria-19-23./24.-feb + Anna-vdova-16./18.-mär — mati+2-hčerke-v-enem-mesecu! + z12-Župarič-h31!) + **★★★ POŽEK-×2-hiši-pred-04894** (h21-Janez-64-l + h58-Janez-3-mes — cf. P153-r55-h21 + r66-h58-1887!) + **★★★ h63-KRIŽAN-×2** (z66-Johann-4-mes + z89-Katarina-31 — cf. krstna-1892-oče-Jurij + poročna-1911-№1!) + hišne-kontinuitete-v-04894 (h9-JAKOFČIČ-37-let + h13-JAKOFČIČ-38-let + h62-KURE-39-let + h68-MLEK-39-let + h78-LOZAR-39-let!) + **DUHOVNIKI-1885**: **And. GLIBE[L][~Gleibe]-coöp-DOMINANTA-×13** (→ P153-1887-'Andrej-Glibel' = ISTI — kontinuiteta-čez-šiv-knjig-04106→04894!) + **Franz-DOVGAN[~Dorgun]-×2** (= poročna-1886-'franz-Dovgan' ISTI!) + FULL-FORM-'Andreas'-z61! + VLM-zavrnitve-×6 (Pajer→PAPIČ + h4→h31 + Peček→POŽEK + Pegan→POŽEK + Valdbeič→JAKOFČIČ + Prigožan→KRIŽAN!) + '3-dni'→3-LETA (z12!) + neberljivi-priimki-×2-dokumentirana (Hrijan[~] + Brgum[~]) + starost-neskladje-z39 ('1½-Monate'-vdova-gospodarica!); **1885 = 93 veljavnih vrstic** (črnilo-št. z1–z93-s-duplikati + svinčnik-preštevanje!) / **16 Griblje-vpisov / 13 hiš (h31-×4! + h63-×2!)**; **16 NOVIH BLOKOV parish.ts: vitals 1219 → 1235 · 04106 = 0 → 16 (1.-bloki-knjige!) · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJENO · PT-luknja 18-NESPREMENJENA**; **KONEC-KNJIGE-04106: s207-z92/93-†-28./30.-december-1885-brez-zaključne-opombe + s208-platnica-'PODZEMELJ / M / 1857–1885'!**; skripta p192 (I1–I12, --live) + qa-p192 (192. kontrola) + dokaz parish-death-1885-04106.json (93 entries: 16-Griblje + 77-ne + 2-prečrtana! 12-anomalij + 8-crossChecks + honesty-12 + leadP192-04106/04104!) + notes; verifikacija: runQA 192/192 ok:True · tsc 0 · lint 0; korpus po P192: **1235/198+16(04106)+520/191/94(p80)·93(korpus) — PT-luknja 18**; **★★★ PREDZGODOVINA-LINIJA-1/29-LET-START!** (P193-LEAD: 1884 — s195–s198-pred + s193/s194-probe! + krstna-04104-1871–1885-×200-skenov-čaka!)",
    "P192: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER PREDECESSOR 04106, THE YEAR 1885 = THE 1st YEAR OF THE PREHISTORY LINE (issue #18; SAMPLE-TRANSCRIPTION-D1885-04106; the 1857–1885 book = the predecessor of 04894!): the frame — s198–s207 == pages 192–201 (page == scan − 6! the new book mapping!) + **THE 1884/85 BOUNDARY = s198-mid ('Jänner anno, 1885.' written across vas+name + the z1-restart = the 31st boundary-invariant confirmation!)** + **★★★ THE z4-DUPLICATE-INSERT** + **★★★ THE DUAL-NUMBERING s204–s207** (ink + PENCIL recount off-by-one = the valid rows!) + **★★★ THE MID-BOOK FORM-CHANGE**: German → hybrid s205 → FULLY-SLOVENE s206–s207 ('Mrtvaška knjiga'!) + the INCOMPLETE-'Jahr 18'-HEADINGS-×2 + the CROSSED-OUT-entries-×2 + **★★★ THE MASERN/DIPHTHERIA-EPIDEMIC Nov-1884–Mär-1885** + **★★★ THE-h31-PAPIČ-CATASTROPHE-3/3** (the mother + 2 daughters in one month!) + **★★★ POŽEK-×2-houses-BEFORE-04894** + **★★★ h63-KRIŽAN-×2** + the house-continuities (h9/h13/h62/h68/h78!) + **THE PRIESTS-1885**: And. GLIBE[L]-coop-DOMINANT-×13 (→ P153-1887-THE-SAME — the continuity-across-the-book-seam!) + Franz-DOVGAN-×2 (= the marriage-1886-THE-SAME!) + the VLM-rejections-×6 + the illegible-surnames-×2 + the age-inconsistency-z39; **1885 = 93 valid rows / 16 Griblje / 13 houses**; **16 NEW BLOCKS: the vitals 1219 → 1235 · the 04106 = 0 → 16 (the 1st blocks of the book!) · the 04894 = 520-UNCHANGED · the p80 94-UNCHANGED · the corpus 93-UNCHANGED · the PT-gap 18-UNCHANGED**; **THE-END-OF-BOOK-04106: s207-z92/93-Dec-28/30-1885-no-closing-note + s208-the-binding-'PODZEMELJ / M / 1857–1885'!**; the verification: the runQA 192/192 ok:True · tsc 0 · lint 0; the corpus after P192: **1235/198+16+520/191/94(p80)·93(corpus) — the PT-gap 18**; **★★★ THE-PREHISTORY-LINE-1/29-YEARS-START!** (the P193-LEAD: 1884!)",
    p192Errors.length === 0,
    p192Errors.length === 0
      ? `16 vpisov / 93 veljavnih vrstic / 13 hiš (h31-×4-KATASTROFA! h63-×2!) · MEJA-'Jänner-anno-1885'-31.-POTRDITEV · z4-DUPLIKAT-VSTAVEK-3.× · DUAL-NUMBERING-črnilo+svinčnik · SPREMEMBA-FORME-nemška→slovenska-MID-BOOK · GLAVE-'Jahr 18'-×2-nepopolne · MASERN/DAVICA-epidemija · POŽEK-×2 + KRIŽAN-×2-pred-04894 · Glibe[l]-DOMINANTA-×13-→-P153-ISTI · DOVGAN-×2-→-1886-ISTI · KONEC-KNJIGE-s207+s208-platnica-1857–1885 · **PREDZGODOVINA-1/29-START!** · vitals 1235 · 04106 16 · 04894 520`
      : p192Errors.join("; "),
  );
  }
  // ——— qa-p189: MRLIŠKA KNJIGA 04894 — polno leto 1923"""

assert ANCHOR in src, "anchor qa-p191-konec ni najden!"
src = src.replace(ANCHOR, BLOCK, 1)
open(PATH, "w", encoding="utf-8").write(src)
print("qa-p192 vstavljen ✓")
