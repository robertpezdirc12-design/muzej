#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P177 — vstavi qa-p177 blok v qa-parish.ts (pred qa-p168, po vzoru p176)."""

QA = "src/lib/qa-parish.ts"
ANCHOR = "  // ——— qa-p168: MRLIŠKA KNJIGA 04894 — polno leto 1902 (P168; 17. polno leto"

BLOCK = '''  // ——— qa-p177: MRLIŠKA KNJIGA 04894 — polno leto 1911 (P177; 26. polno leto
  //      mrliške linije; celoten neodvisen preracun iz bundled parish.ts!) ———
  //      1911 = 58 vrstic / 13 Griblje-vpisov / 12 hiš (h14-×2-BRINEC!) +
  //      z31-'96'→26-LET-KROP (roj. 1884!) + z30-'95'→35-KROP (roj. 1876!)
  //      + z47-'Nepomuk'→KUPANIČ + z48-'Birčec'→BRINEC + z54-'Fošelj'→POŽEK
  //      + z51-'Perdih'→PEZDIREC (×4-1911!) + z42-h14→h19 + z24/z30/z36-VAS-×3
  //      + z55-'Vlobučar'→HLOBUČAR + z46-HLADNI-KAŠELJ + meja 1911/12 =
  //      s135-INSIDE (2.-POTRDITEV-STILA-8!). Dokaz:
  //      research/issue17/parish-death-1911.json; verifikator:
  //      scripts/p177_parish_death_1911.py --live I1–I13.
  {
  const p177Errors: string[] = [];
  const p177Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04894" && h.year === 1911);
  if (p177Death.length !== 13)
    p177Errors.push(`bloki 1911 (04894) ≠ 13 (${p177Death.length} — 13 Griblje-vpisov / 58 vrstic!)`);
  const p177Houses = p177Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p177Houses.join(",") !== "14,14,19,20,24,31,34,41,42,43,46,48,57")
    p177Errors.push(`hiše 1911 ≠ [14,14,19,20,24,31,34,41,42,43,46,48,57] — najdeno: ${p177Houses.join(",")} (12 RAZLIČNIH — h14-×2-BRINEC!)`);
  if (p177Death.some((h) => !h.scan || h.page !== h.scan - 1 || h.scan < 131 || h.scan > 135))
    p177Errors.push("stran == sken − 1 krščeno (s131–s135; 106.–111. potrditev — novi skeni s133–s136!)");
  // 178. kontrola — ključne forezike-1911
  if (!p177Death.some((h) => h.whatSi.includes("roj. 19. 4. 1884")))
    p177Errors.push("★★★ z31-'96'→26-LET-KROP-forenzika (roj. 1884-marginalija — 26-SKLADNO!) manjka");
  if (!p177Death.some((h) => h.whatSi.includes("KUPANIČ")))
    p177Errors.push("★★★ z47-'Nikolaj Nepomuk'→KUPANIČ-KROP (@×3.0 — NI-sv.-Nepomuk!) manjka");
  if (!p177Death.some((h) => h.whatSi.includes("BRINEC-×2-1911")))
    p177Errors.push("★★ h14-×2-BRINEC-1911 (z13-Ana-8 + z48-Matija-4!) manjka");
  if (!p177Death.some((h) => h.whatSi.includes("PEZDIREC-×4-1911")))
    p177Errors.push("★★★ PEZDIREC-×4-1911 (z24 + z26 + z27 + z51 = 1.-LETO-×4!) manjka");
  if (!p177Death.some((h) => h.whatSi.includes("Opeklina")))
    p177Errors.push("★★ z48-OPEKLINA = 1.-TA-BOLEZEN-LINIJE + 3.-TRAUMA-SMRT manjka");
  if (!p177Death.some((h) => h.whatSi.includes("Hladni kašelj")))
    p177Errors.push("★★ z46-HLADNI-KAŠELJ = 1.-TA-BOLEZEN (2.-nova-1911!) manjka");
  if (!p177Death.some((h) => h.whatSi.includes("HLOBUČAR")))
    p177Errors.push("★★ z55-'Vlobučar'→HLOBUČAR (H-prečka + P166-vez-×3!) manjka");
  if (!p177Death.some((h) => h.whatSi.includes("POŽEK")))
    p177Errors.push("★★ z54-'Fošelj'→POŽEK (ž-CARON-KROP!) manjka");
  const p177Future = HOUSE_VITALS.filter((h) => h.bookSignature === "04894" && (h.year ?? 0) >= 1913);
  if (p177Future.length > 0)
    p177Errors.push(`1912+-mrliški bloki že v korpusu (${p177Future.length} — P178-lead: ne smejo biti!; P177 = 1911 sedaj v korpusu!)`);
  if (HOUSE_VITALS.length !== 1045)
    p177Errors.push(`HOUSE_VITALS ≠ 1045 (${HOUSE_VITALS.length} — P176: 1032; P177: + 13 blokov 1911!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04894").length !== 346)
    p177Errors.push(`bloki 04894 ≠ 346 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04894").length} — P176: 333; P177: + 13 = 346!)`);
  push(
    "qa-p177-parish-death-1911",
    "P177: ŽUPNIJA PODZEMELJ — MRLIŠKA KNJIGA 04894, LETO 1911 = 26. POLNO LETO MRLIŠKE LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1911; mrliška linija: … → P174 = 1908 → P175 = 1909 → P176 = 1910 → **P177 = 1911 = 58 vrstic / 13 Griblje-vpisov / 12 hiš (h14-×2-BRINEC!) — rast 12→13**): okvir — s130-dno (z1–5; meja-'~1911~'-band!) + s131 (z6–17) + s132 (z18–29) + s133 (z30–41) + s134 (z42–53) + s135 (z54–58) == str. 129–134 (stran == sken − 1 — 106.–111. potrditev — VLM-glave-s133/134/136-'Stran 132/133/135'!) + **meja 1911/12 = s135-INSIDE ('1912'-VELIKA-v-praznem-bandu-k5 + restart-z58→z1 + Bitnar-podpis-v-meja-bandu = 2.-POTRDITEV-STILA-8 — P176-lead-'[?]' REŠEN!)**; **★★★ z31-Marija-MAVREŠIČ-h57-'96 let' → 26 LET (KROP-×3.0 + roj. 19. 4. 1884-marginalija → 26-SKLADNO!) + roj. PEZDIREC (KROP!)** + **★★★ z30-TAPRIČ-'95'→35-LET (roj. 4. 8. 1876! — ne-Griblje-GRIŠIČE?)** + **★★★ z47-'Nikolaj-Nepomuk' → Nikolaj-KUPANIČ (KROP-@×3.0 — '[K]upanič'-jasno — NI-sv.-Nepomuk! NOV-PRIIMEK? [~])** + **★★★ z51-'Peter-Perdih' → Peter-PEZDIREC (KROP-širok — z-DESCENDER-leksikon!) → PEZDIREC-×4-1911 (z24-Podzemelj + z26-h42 + z27-h48 + z51-h20 = 1.-LETO-×4-PRIIMKA!)** + **★★ z48-'Matija-Birčec'→Matija-BRINEC (KROP — 'Brinec'-jasno; panel-'Sofija'-ZAVRJENA-sin-stan!) → h14-×2-1911 = BRAT+SESTRA?-PAR (z13-Ana-8 + z48-Matija-4!)** + **★★ z54-'Janez-Fošelj'→Janez-POŽEK (KROP — ž-CARON! POŽEK-veriga-P85!)** + **★★ z42-h14→h19 (KROP — 4/9-KURRENT!)** + **★★★ VAS-KOREKCIJE-×3: z24-'Lodnemej'→PODZEMELJ + z30/z36-'Griblje'→GRIŠIČE? (KROP-×3 — P131-'Grišiče?35'-precedent!) → GRIBLJE-13-ne-16 (P176-lead-'5-GRIBLJE'-= 2-realnih + 3-zavrnjenih!)** + **★★ z55-'Vlobučar'→Katarina-HLOBUČAR (H-prečka-@×3.0 + P166-vez-×3! H/V-lekcija-2.-potrditev)** + **★★ z46-'Hladno-klatran'→HLADNI-KAŠELJ = 1.-TA-BOLEZEN-LINIJE** + **★★ z48-OPEKLINA = 1.-TA-BOLEZEN = 3.-TRAUMA-SMRT (1908-vrca + 1910-mrtvo-najden!) — 2-NOVI-BOLEZNI-V-1-LETU!** + ★★ z14-Katarina-HRUŠIČ-h34-88 = NAJSTAREJŠA-1911 (ŠILAK-vrnitev-hipoteza [~]!) + ★★ z31-'Pithar'→Bitnar + z30-'Rauq'→Pumf + z42-'Pihnar'→Bitnar (PODW-KROPI-×3 — VLM-podpis-zmeda-RAZREŠENA!) + ★ meja-'1912'-band + z58-pokop-'2-jan-1912'-EKSPPLICITNO; DUHOVNIKI: Bitnar-#16-DOMINANTA-×12-3.-LETO + Jos.-Pumf-×1 (z14!) — 0-NOVIH; bolezni: Jetika ×3 + Naduha ×3 + Slabost ×2 + Božjast ×2 + Hladni-kašelj + Opeklina + Vodenica + Pljučnica + razpon-3-meseci→88-let + otroška-smrt-×3 (23%!); **13 NOVIH BLOKOV parish.ts: vitals 1032 → 1045 · mrliški 04894 333 → 346 · p80 92-NESPREMENJENO · korpus 93-NESPREMENJEN · PT 29 (0-novih-kandidatov — vse-hiše-3.–8.-vpis!)**; skripta p177 (I1–I13, --live) + qa-p177 (178. kontrola) + dokaz parish-death-1911.json (58 entries: 13-Griblje + 45-ne! 3-excluded + 12-anomalij + 5-crossChecks + honesty-7 + P178-lead) + notes; KASKADA: qa 91× 1032→1045 + 25× 333→346 + guardi-1912 (24×!) + p80Death-sporočilo + skripte-p153–p176-×24 (VITALS_TOTAL-1045 + BLOKI-346); verifikacija: p177 35/35 · runQA 178/178 ok:True · tsc 0 · lint 0; korpus po P177: 1045/198+346/191/92(p80)·93(korpus) — PT 29; **P178 LEAD: mrliška 1912** (s135-dno-z1–6 + s136-z7–18 ŽE-prebrani: 2-GRIBLJE — 1912-z1-jožef-PEČNIK?-h87 [K-C-'Pechnik'-vs-diag-'Pačdivec'!] + 1912-z10-barbara-ŠTRAVS-h11! + 1912-z3-MRTVOROJENEC-×2-v-2-mesecih-Dobravice-h7!; meja-1912/13 [~ s140+?])",
    "P177: THE PARISH OF PODZEMELJ — THE DEATH REGISTER 04894, THE YEAR 1911 = THE 26th FULL YEAR OF THE DEATH LINE (issue #18; SAMPLE-TRANSCRIPTION-D1911; the death line: … → P175 = 1909 → P176 = 1910 → **P177 = 1911 = 58 rows / 13 Griblje entries / 12 houses (h14-×2-BRINEC!) — the growth 12→13**): the frame — the s130-bottom (z1–5; the-'~1911~'-boundary-band!) + s131 (z6–17) + s132 (z18–29) + s133 (z30–41) + s134 (z42–53) + s135 (z54–58) == pages 129–134 (page == scan − 1 — the 106th–111th confirmations — the VLM-headers-s133/134/136-'Stran 132/133/135'!) + **the 1911/12 boundary = s135-INSIDE (the-'1912'-LARGE-in-the-empty-band-k5 + the-z58→z1-restart + the-Bitnar-signature-in-the-boundary-band = the 2nd-CONFIRMATION-OF-STYLE-8 — the P176-lead-'[?]' RESOLVED!)**; **★★★ the z31-Marija-MAVREŠIČ-h57-'96-years' → 26 YEARS (the crop-×3.0 + born-Apr-19-1884-margin → 26-CONSISTENT!) + born-PEZDIREC (the crop!)** + **★★★ the z30-TAPRIČ-'95'→35-YEARS (born-Aug-4-1876! — a non-Griblje-GRIŠIČE?)** + **★★★ the z47-'Nikolaj-Nepomuk' → Nikolaj-KUPANIČ (the crop-@×3.0 — '[K]upanič'-clear — NOT-st.-Nepomuk! a NEW-SURNAME? [~])** + **★★★ the z51-'Peter-Perdih' → Peter-PEZDIREC (the wide-crop — the z-DESCENDER-lexicon!) → PEZDIREC-×4-1911 (z24-Podzemelj + z26-h42 + z27-h48 + z51-h20 = the 1st-YEAR-×4-SURNAME!)** + **★★ the z48-'Matija-Birčec'→Matija-BRINEC (the crop — 'Brinec'-clear; the panel-'Sofija'-REJECTED-son-status!) → h14-×2-1911 = a BROTHER+SISTER?-PAIR (z13-Ana-8 + z48-Matija-4!)** + **★★ the z54-'Janez-Fošelj'→Janez-POŽEK (the crop — the ž-CARON! the POŽEK-chain-P85!)** + **★★ the z42-h14→h19 (the crop — the 4/9-KURRENT!)** + **★★★ the VILLAGE-CORRECTIONS-×3: z24-'Lodnemej'→PODZEMELJ + z30/z36-'Griblje'→GRIŠIČE? (the crops-×3 — the P131-'Grišiče?35'-precedent!) → GRIBLJE-13-not-16 (the P176-lead-'5-GRIBLJE'-= 2-real + 3-rejected!)** + **★★ the z55-'Vlobučar'→Katarina-HLOBUČAR (the H-crossbar-@×3.0 + the P166-link-×3! the H/V-lesson-2nd-confirmation)** + **★★ the z46-'Hladno-klatran'→COLD-COUGH = the 1st SUCH-ILLNESS-of-the-line** + **★★ the z48-BURN = the 1st SUCH-ILLNESS = the 3rd-TRAUMA-DEATH (1908-cart + 1910-found-dead!) — 2-NEW-ILLNESSES-IN-1-YEAR!** + ★★ the z14-Katarina-HRUŠIČ-h34-88 = the OLDEST-1911 (the ŠILAK-return-hypothesis [~]!) + ★★ the z31-'Pithar'→Bitnar + the z30-'Rauq'→Pumf + the z42-'Pihnar'→Bitnar (the WIDE-SIGNATURE-CROPS-×3 — the VLM-signature-confusion-RESOLVED!) + ★ the boundary-'1912'-band + the z58-burial-'2-Jan-1912'-EXPLICIT; THE PRIESTS: Bitnar-#16-THE-DOMINANT-×12-THE-3rd-YEAR + Jos.-Pumf-×1 (z14!) — 0-NEW; the illnesses: Jetika ×3 + Naduha ×3 + Slabost ×2 + Božjast ×2 + the cold-cough + the burn + the dropsy + the pneumonia + the range-3-months→88-years + the child-deaths-×3 (23%!); **13 NEW BLOCKS parish.ts: the vitals 1032 → 1045 · the 04894 333 → 346 · the p80 92-UNCHANGED · the corpus 93-UNCHANGED · the PT 29 (0-new-candidates — all-houses-3rd–8th-entry!)**; the script p177 (I1–I13, --live) + the qa-p177 (the 178th check) + the evidence parish-death-1911.json (58 entries: 13-Griblje + 45-non! 3-excluded + 12-anomalies + 5-cross-checks + honesty-7 + the P178-lead) + notes; the CASCADE: the qa 91× 1032→1045 + the 25× 333→346 + the guards-1912 (24×!) + the p80Death-message + the scripts-p153–p176-×24 (the VITALS_TOTAL-1045 + the BLOKI-346); the verification: the p177 35/35 · the runQA 178/178 ok:True · tsc 0 · lint 0; the corpus after P177: 1045/198+346/191/92(p80)·93(corpus) — the PT 29; **the P178 LEAD: the 1912** (the s135-bottom-z1–6 + the s136-z7–18 ALREADY-read: 2-GRIBLJE — the 1912-z1-jožef-PEČNIK?-h87 [the K-C-'Pechnik'-vs-the-diag-'Pačdivec'!] + the 1912-z10-barbara-ŠTRAVS-h11! + the 1912-z3-STILLBORN-×2-in-2-months-Dobravice-h7!; the 1912/13 boundary [~ s140+?])",
    p177Errors.length === 0,
    p177Errors.length === 0
      ? `13 vpisov / 58 vrstic-zap1–58 (ČISTA-SEKVENCA — 7.-čisto-leto!) / 12 hiš (h14-×2-BRINEC!) · stran == sken − 1 (106.–111. potrditev) · meja 1911/12 = s135-INSIDE (2.-POTRDITEV-STILA-8!) · **★★★ 26-LET-KROP-'96' + KUPANIČ-'Nepomuk' + PEZDIREC-×4-1911 + BRINEC-×2-h14 + POŽEK-'Fošelj' + VAS-×3 + HLOBUČAR-'Vlobučar' + HLADNI-KAŠELJ + OPEKLINA!** · kumulativ po P177: 1045/346/92/93 (PT 29) · P178-LEAD: 1912 (s135-dno + s136: 2-GRIBLJE-ŽE-vidnih!)`
      : p177Errors.join("; "),
  );
  }

'''

src = open(QA, encoding="utf-8").read()
assert "qa-p177-parish-death-1911" not in src, "qa-p177 že obstaja!"
assert ANCHOR in src, "sidro-ni-najdeno!"
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
open(QA, "w", encoding="utf-8").write(src)
print("qa-p177 blok vstavljen ✓")
