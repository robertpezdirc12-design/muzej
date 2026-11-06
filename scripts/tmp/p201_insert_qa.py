#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P201 — INSERT qa-p201 blok v qa-parish.ts (pred qa-p200-anchor)."""
from pathlib import Path

QA = Path("/home/z/my-project/src/lib/qa-parish.ts")
src = QA.read_text(encoding="utf-8")

ANCHOR = "  // ——— qa-p200: MRLIŠKA PREDZGODOVINA 04106 — leto 1877 = 9. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1, f"anchor-qa={src.count(ANCHOR)}"
assert "qa-p201-parish-death-1876-04106" not in src, "qa-p201-že-obstaja?!"

BLOCK = '''
  // ——— qa-p201: MRLIŠKA PREDZGODOVINA 04106 — leto 1876 = 10. leto PREDZGODOVINSKE
  //      LINIJE (issue #18; knjiga 1857–1885!).
  //      1876 = 89 vpisov (z1–z89, ŠTEVJE-IZ-VRSTIC — ordinali-NEVIDNI-×9!) /
  //      20 Griblje / 19 hiš (h46-×2!) + ★★★ MEJA-1875/76-s134 (TAIL-4-Dez-1875 +
  //      VELIKA-'1876 Jänner'-glava + 'Jahr'-beseda + restart-Jänner-2.!) + ★★★
  //      DECEMBER-1876 = 0-VPIISOV (31-dnevna-vrzel!) + ★★★ NOVEMBER-FALSIFIKA-
  //      CIJA (s142-VLM-'Dezember'-KROP-FALSIFICIRAN — 'N-o-v-e-m-b-e-r.'!) +
  //      ★★★ 40.-in-41.-POTRDITEV-invariante (s136-'1876.'-v-z1-celici + s142-
  //      '1876.'-v-z1-celici!) + ★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-V-1876 (Hogeja/
  //      Hoggin/Hogyi-Coop-×9-Feb→Nov!) + ★★★ PEZDINC-#8 + DRAGOŠ-h12-NIT +
  //      ŠIMEC-h18-3.-LETO + KRONOLOŠKA-NAPAKA-PISARJA.
  //      Dokaz: parish-death-1876-04106.json; skripte p201 (fetch-md5 + read +
  //      crop + build-entries + build-proof).
  {
  const p201Errors: string[] = [];
  const p201Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1876);
  if (p201Death.length !== 20)
    p201Errors.push(`bloki 1876 (04106) ≠ 20 (${p201Death.length} — 20 Griblje-vpisov / 89 vpisov vrstno-štetje!)`);
  const p201Houses = p201Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p201Houses.join(",") !== "7,8,12,16,18,20,23,26,34,41,44,46,46,49,52,53,55,64,70,75")
    p201Errors.push(`hiše 1876 neujemane — najdeno: ${p201Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1375)
    p201Errors.push(`HOUSE_VITALS ≠ 1375 (${HOUSE_VITALS.length} — P200: 1355; P201: + 20 blokov 1876-04106 = 1375!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 156)
    p201Errors.push(`bloki 04106 ≠ 156 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 156!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p201Errors.push("04106-bloki izven {1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1875 še nebrani!)");
  if (!p201Death.some((h) => h.houseNo === "53" && h.whatSi.includes("PEZDINC-GRAFIA-NIT-#8")))
    p201Errors.push("★★★ PEZDINC-GRAFIA-#8 (z22-'Perdire'-h53 — h53-NIT-babica+dojenček!) ni označena");
  if (!p201Death.some((h) => h.houseNo === "12" && h.whatSi.includes("DRAGOŠ-h12-NIT")))
    p201Errors.push("★★★ DRAGOŠ-h12-NIT (z36-Anton-¼J-sin-Joanesa → 1877-z56-Katharina!) ni označena");
  if (!p201Death.some((h) => h.houseNo === "18" && h.whatSi.includes("ŠIMEC-NIT-3.-LETO")))
    p201Errors.push("★★★ ŠIMEC-h18-NIT-3.-LETO (z78-'Simec' — 4-imena-4-leti!) ni označena");
  if (!p201Death.some((h) => h.houseNo === "44" && h.whatSi.includes("KRONOLOŠKA-NAPAKA-PISARJA")))
    p201Errors.push("★★★ KRONOLOŠKA-NAPAKA-PISARJA (z83-Nov-24-zapisan-pred-Nov-12!) ni označena");
  if (!p201Death.some((h) => h.houseNo === "44" && h.whatSi.includes("PRIMEK-NESOGLASJE-×3")))
    p201Errors.push("★ h44-PRIMEK-NESOGLASJE-×3 (Kavčič[?]/Arnuetz[?]/Struselj[?]!) ni označena");
  if (!p201Death.some((h) => h.houseNo === "46" && h.whatSi.includes("h46-×2-v-2-MESECIH")))
    p201Errors.push("★★★ h46-×2-v-2-MESECIH (z24-April + z35-Mai!) ni označena");
  push(
    "qa-p201-parish-death-1876-04106",
    "P201: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1876 = 10. LETO PREDZGODOVINSKE LINIJE (issue #18; knjiga 1857–1885!): okvir — s134–s142 == Pag. 128–136 (stran == sken − 6! md5-križna-validacija-verige-P197→P198→P199→P200→P201: s142-svež == P200-disk-1:1 — 5.×!) + **MEJA 1875/76 = s134 (TAIL-4-DEZ-1875-nad + VELIKA-'1876 Jänner'-GLAVA-V-SREDINI-STRANI + 'Jahr'-beseda + RESTART-Jänner-2.-pod — ordinali-NEVIDNI!)** + MEJA 1876/77 = s143-'18 77.'-ODREZANA (P200-reuse + TA-SEJA-RE-VERIFIKACIJA: z1-smrt-'1.'/pokop-'8.' + 'todt geboren zu Podžemelj' + restart-1 + Jänner@z2 → P200-60-NETAKNJENA!) + **★★★ DECEMBER-1876 = 0-VPIISOV** (Nov-30-pokop-'31.'[=Dez-1!] → Jänner-1-1877 = 31-dnevna-brez-smrti-vrzel — redka-zerost!) + **★★★ NOVEMBER-FALSIFIKACIJA** (s142-VLM-'Dezember'-×2-KROP-FALSIFICIRAN — 'N-o-v-e-m-b-e-r.'-črka-za-črko-pod-'1876.'-glavo! P200-lead-'Dez-tail'-POPREVEK — Griblje-×3-OSTAJAJO-kot-November!) + **★★★ 40.-in-41.-POTRDITEV-invariante** ('1876.'-glava-V-Z1-DATUMSKI-CELICI: s136-März + s142-NOVEMBER!) + **★★★ 89-VPIISOV — ŠTEVJE-IZ-VRSTIC** (ordinali-NEVIDNI-×9! vrstna-aritmetika 6+12+12+10+10+9+10+10+10 + meseci J6+F9+M6+A6+M10+J7+J5+A10+S16+O4+N10 + DEZEMBER-0!) + **★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-V-1876** (Hogeja/Hoggin/Hogyi-'Coop.'-×9-Feb→Nov + eksplicitni-'Jožef-Kogej-coop.'-z78! + Franz-Dorgan-[DOVGAN]-×3 + fortd.-Jos.-HOZJAN-Capp.-×2 + Justiniant-Roggia-×1!) + **★★★ PEZDINC-GRAFIA-#8** (z22-Maria-'Perdire'-h53 — KROP-'P-e-r-d-i-r-e'! h53-NIT-×2: babica-62J-März-1876 + dojenček-1J-Okt-1877!) + **★★★ DRAGOŠ-h12-NIT** (z36-Anton-¼J — KROP-'sin-Joanesa-Dragoša' + VLM-'2½J'-ZAVRJEN! → 1877-z56-Katharina — Joanes-otoka-×2!) + **★★★ ŠIMEC-h18-NIT-3.-LETO** (z78-Maria-'Simec'-Mädchen-72¾J → 1877-Siniec + 1878-Innec? + 1881-TIMEC = 4-IMENA-4-LETI!) + ★ h46-×2-v-2-mesecih (z24-Anna-Klobučar-April + z35-Mathias-Mai!) + ★ h8-JAKOFČIČ-nit (z79-Anna-27½J-Hirnhautentzündung → 1877-z39!) + ★ FRISEN-×2-v-6-dneh (z41-h20 + z43-h64-Kerbica!) + ★ MASERN-z32 (h70-Katharina-6½J-Masernfriesel!) + ★ KLOBUČAR-z24 (→ P199-h48!) + ★ 24-URE-z83 (h44-Barbara-[?]nesoglasje-×3: Kavčič[?]/Arnuetz[?]/Struselj[?]!) + ★★★ KRONOLOŠKA-NAPAKA-PISARJA (z83-Nov-24-zapisan-PRED-z85-Nov-12 — KROP-×2-potrjeno — 1.-pojav-v-korpusu!) + ★ '31.'-pokop-NE-obstaja-v-Nov (z88/z89: Nov-29/30-smrt-pokop-Dez-1! ULEDBA-#10-vzorec!) + ★ s139-tabela-konča-prek (9-vrstic + prazen-prostor!) + **★★★ GRIBLJE-OTROŠKA-UMRLJIVOST-55%-1876 (11/20!)**; **1876 = 89 vpisov (z1–z89) / 20 Griblje-vpisov / 19 hiš**; **20 NOVIH BLOKOV parish.ts: vitals 1355 → 1375 · 04106 = 136 → 156 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p201 (fetch-md5 + read + crop + build-entries + build-proof) + qa-p201 (201. kontrola!) + dokaz parish-death-1876-04106.json (89 entries: 20-Griblje + 69-druge! 16-anomalij + 10-crossChecks + honesty-16 + tail_1875-×4 + leadP202-1875!) + pt-luknja-REGENERACIJA (156/1375!) + krstni-izjeme-RAZŠIRJENE-×3 (h53-PEZDIRE + h12-DRAGOŠ + h18-ŠIMEC-1876!); **★★★ PREDZGODOVINA-LINIJA-10/29-LET!** (P202-LEAD: 1875 — s134-TAIL-×4-ŽE-PREBRAN (Griblje-×1: z4-h11-Catharina-KUNIĆ[~Kuniz?]-geb.-Jakoš-65J-Dez-24/26!) + s133-Nov–Dez-1875-×11-ŽE-PREBRAN ('1875'-glava-violetna!) → probe-s126–s134!)",
    "P201: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1876 = THE 10th YEAR OF THE PREHISTORY LINE (issue #18): the frame — s134–s142 == pages 128–136 (page == scan − 6! the-md5-cross-validation-of-the-chain-P197→P198→P199→P200→P201: s142-fresh == P200-disk-1:1 — the-5th-time!) + **THE 1875/76 BOUNDARY = s134 (the-TAIL-4-DEZ-1875-above + the-BIG-'1876 Jänner'-HEAD-IN-THE-MIDDLE-OF-THE-PAGE + the-'Jahr'-word + the-RESTART-Jänner-2.-below — the-ordinals-INVISIBLE!)** + the 1876/77 boundary = s143 (the-P200-reuse + THIS-SESSION-RE-VERIFICATION: z1-death-'1.'/burial-'8.' + 'todt geboren zu Podžemelj' + restart-1 + Jänner@z2 → the-P200-60-INTACT!) + **★★★ DECEMBER-1876 = 0-ENTRIES** (Nov-30-burial-'31.'[=Dec-1!] → Jänner-1-1877 = the-31-day-no-death-gap — a-rare-zero!) + **★★★ the-NOVEMBER-FALSIFICATION** (the-s142-VLM-'Dezember'-×2-FALSIFIED-BY-THE-KROP — 'N-o-v-e-m-b-e-r.'-letter-by-letter-under-the-'1876.'-head! the-P200-lead-'Dec-tail'-CORRECTED — the-Griblje-×3-REMAIN-as-November-entries!) + **★★★ the-40th-and-41st-INVARIANT-CONFIRMATIONS** (the-'1876.'-head-WRITTEN-INSIDE-THE-Z1-DATE-CELL: s136-März + s142-NOVEMBER!) + **★★★ THE-89-ENTRIES — THE-COUNT-FROM-ROWS** (the-ordinals-INVISIBLE-×9! the-row-arithmetic 6+12+12+10+10+9+10+10+10 + the-months + DECEMBER-0!) + **★★★ the-KOGEJ-PERIOD-EXTENDED-INTO-1876** (Hogeja/Hoggin/Hogyi-'Coop.'-×9-Feb→Nov + the-explicit-'Jožef-Kogej-coop.'-z78! + Franz-Dorgan-[DOVGAN]-×3 + Jos.-HOZJAN-Capp.-×2 + Roggia-×1!) + **★★★ the-PEZDINC-GRAFIA-#8** (the-h53-NIT-×2: the-62J-grandmother-März-1876 + the-1J-infant-Okt-1877!) + **★★★ the-DRAGOŠ-h12-THREAD** (z36-Anton-¼J — → 1877-z56-Katharina! ×2-children-of-Joannes!) + **★★★ the-ŠIMEC-h18-THREAD-3rd-YEAR** (4-NAMES-4-YEARS-ON-h18!) + ★ the-h46-×2-in-2-months + ★ the-h8-JAKOFČIČ-thread + ★ FRISEN-×2-in-6-days (the-Kerbica-family!) + ★ the-MASERN-z32 + ★ the-KLOBUČAR-z24 + ★ the-24-HOURS-z83 (the-h44-surname-×3-disagreement!) + ★★★ the-CHRONOLOGICAL-SCRIBE-ERROR (Nov-24-written-BEFORE-Nov-12 — the-1st-in-the-corpus!) + ★ the-'31.'-burial-does-NOT-exist-in-Nov + ★ the-s139-table-ends-early + **★★★ the-GRIBLJE-CHILD-MORTALITY-55%-1876 (11/20!)**; **1876 = 89 entries / 20 Griblje / 19 houses**; **20 NEW BLOCKS: the vitals 1355 → 1375 · the 04106 = 136 → 156 · the 04894 = 520-UNCHANGED**; the scripts p201 + the qa-p201 (the 201st check!) + the evidence parish-death-1876-04106.json (89 entries!) + the pt-gap-REGENERATION (156/1375!) + the-baptism-exceptions-EXTENDED-×3; **★★★ THE-PREHISTORY-LINE-10/29-YEARS!** (the P202-LEAD: 1875 — the-s134-TAIL-×4-ALREADY-READ (Griblje-×1: h11-Catharina-KUNIĆ[~]-65J-Dec-24/26!) + the-s133-Nov–Dez-1875-×11-ALREADY-READ → the-probe-s126–s134!)",
    p201Errors.length === 0,
    p201Errors.length === 0
      ? `20 vpisov / 89 vrstic (števje-iz-vrstic!) / 19 hiš · MEJA-s134-VELIKA-'1876 Jänner'-glava + 40.-41.-POTRDITVI-s136/s142-celici · DECEMBER-0 (31-dnevna-vrzel!) · NOVEMBER-FALSIFIKACIJA (KROP!) · KOGEJ-v-1876 (×9!) · PEZDINC-#8-h53-nit · DRAGOŠ-h12-nit · ŠIMEC-h18-3.-leto · h46-×2 · KRONOLOŠKA-NAPAKA-pisarja · otroška-umrljivost-55% · **PREDZGODOVINA-10/29!** · vitals 1375 · 04106 156 · 04894 520`
      : p201Errors.join("; "),
  );
  }
'''

src = src.replace(ANCHOR, BLOCK + "\n" + ANCHOR, 1)
QA.write_text(src, encoding="utf-8")
print(f"qa-p201-blok: INSERTED (+{len(BLOCK)} B)")
