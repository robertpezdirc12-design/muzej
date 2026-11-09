// parish-marriage-early.ts — P238: POROČNA PREDZGOVINA 04455, leto 1885 = 1/13 NOVA LINIJA
// Meritve so izpeljane ob zagonu IZ korpusa HOUSE_VITALS (parish.ts) — qa-p238 jih živo
// preverja proti dokaz-seji P238 (research/issue17/parish-marriage-1885-04455.json, 2026-11-09).
// NOVA LINIJA: poročna-predzgodovina (krstna-04104-KONČANA-15/15-P236-sinteza! + forenzika-P237!).
// Vir: poročna knjiga 04455 (Trauungs-Buch), Matricula Online — skeni s56–s61 == Pag. 55–60
// (★★★ Pag = sken−1 RAZŠIRJENO na 55–66; prej P84: samo 61–66!).

import { HOUSE_VITALS } from "./parish";

/** Leta poročne predzgodovine 04455 (1873–1885) — descending-vzorec kot 04104-linija. */
export const MARRIAGE_LINE_YEARS = 13;

/** Bloki P238 (leto 1885) iz korpusa — izpeljano 1:1. */
export const MARRIAGE_1885_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1885,
);

/** Št. Griblje porok 1885 v korpusu (meritev: 7 — 1:1 + 3 X-OPEN-vasi NISO bloki). */
export const MARRIAGE_1885_GRIBLJE = MARRIAGE_1885_BLOCKS.length;

/** Hiše poročne linije 1885 (merjeni vrstni-red blokov: 58, 60, 32, 71, 29, 26, 13). */
export const MARRIAGE_1885_HOUSES = MARRIAGE_1885_BLOCKS.map((h) => h.houseNo);

/** Vsi vpisi leta 1885 (meritev: 22 številčenih; zap-stolpec 2,4,5,6 → vpis 3 PRESKOČEN!). */
export const MARRIAGE_1885_TOTAL = 22;

/** Ordinalna anomalija: pisar je preskočil vpis 3 (s57 zap-stolpec ultra-zoom 1:1). */
export const MARRIAGE_1885_ZAP_SKIPPED = 3;

/** X-OPEN vas-dueli (h29/h15/h9 — »½-Gütl-Gern/Glob«-vs-GRIBLJE, ne-bloki!). */
export const MARRIAGE_1885_XOPEN = ["29 [~X-OPEN]", "15 [~X-OPEN]", "9 [~X-OPEN]"] as const;

/** PEZDIRC-omembe v letu 1885 (meritev: 3 — vpis 11 ženin 1:1 + vpis 22 mati + vpis 7 starši ×2 [~]). */
export const PEZDIRC_1885 = MARRIAGE_1885_BLOCKS.filter((h) => /PEZDIRC|Pezdirec|Pegdirec/i.test(h.whatSi)).length;

/** LEDERER (usnjar)-omembe v blokih vpisov 16–22 (meritev: usnjarska koncentracija poletja 1885). */
export const LEDERER_1885 = MARRIAGE_1885_BLOCKS.filter((h) => /Lederer|Ledererin|usnjar/i.test(h.whatSi)).length;

/** BRINC/BRINEC-mreža 1885 (meritev: vpis 1 mati roj. Brunc[~Brinc] + vpis 16 Georg Brinec h26 + vpis 17 Marko Brinec). */
export const BRINEC_1885 = MARRIAGE_1885_BLOCKS.filter((h) => /BRINC|Brinec|Brunc/i.test(h.whatSi)).length;

/** Meja 1885/86: s61 = TAIL (vpis 22, 22. Nov) + RESTART-1886 (velike »1 8 8 6«, vpisi 1–3) — sidro P84 1:1. */
export const MARRIAGE_1885_MEJA = {
  restartSi: "restart-vpis-1 = 25. Jän 1885 (s56, tail-1884-vpisi-15–18 na isti strani!)",
  restartEn: "restart-entry-1 = Jan 25, 1885 (s56, the 1884-tail-entries-15–18 on the same page!)",
  tailSi: "tail-vpis-22 = 22. Nov 1885 (s61 + restart-1886-na-isti-strani!)",
  tailEn: "tail-entry-22 = Nov 22, 1885 (s61 + the 1886-restart on the same page!)",
} as const;

/** P84-okvir-korekcija: P84 je brala s58–s68 kot »okvir 1886« — s58–s60 so DEJANSKO tail-1885 (vpisi 7–21). */
export const P84_CORRECTION =
  "P84-okvir-korekcija: s58–s60 = februar–julij-vpisi-7–21-leta-1885 (ne-1886!) — vpisi-1886-se-začnejo-z-restartom-na-s61";

/** Datum izven vrsti: vpis 7 = 7. Feb vpisan PO vpisih 5–6 (8. Feb) — 1-dan-korak-nazaj (×2-1:1). */
export const MARRIAGE_1885_OUT_OF_ORDER = "vpis-7 = 7.-Feb-po-8.-Feb (vpis-6!) — 1-dan-nazaj";

/** Duhovnik vseh 22 vpisov 1885. */
export const PRIEST_1885 = "Franz Dovgan [~Dorgan/Dergan] — edini-duhovnik-vseh-22-vpisov";

/** Najstarejši par leta 1885 (vpis 21: 48 + 49 = 97 let skupaj). */
export const OLDEST_PAIR_1885 = "48 + 49 = 97 let (vpis 21, Bruselj × Planinec)";

/** Najmlajša nevesta (vpis 7: 17 [~19-duel]). */
export const YOUNGEST_BRIDE_1885 = 17;
