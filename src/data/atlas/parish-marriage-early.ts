// parish-marriage-early.ts — P238: POROČNA PREDZGOVINA 04455, leto 1885 = 1/13 NOVA LINIJA
// P239: leto 1884 = 2/13 (s52–s56, 18 vpisov, RESTART = s53, 3 Griblje bloka, MILEK-križ +2!).
// P240: leto 1883 = 3/13 (s50–s52, 12 vpisov, RESTART = s50-dno, 2 Griblje bloka h13+h2, h2 = 1.-poročni-04455-blok!).
// Meritve so izpeljane ob zagonu IZ korpusa HOUSE_VITALS (parish.ts) — qa-p238/qa-p239/qa-p240 jih živo
// preverja proti dokaz-seji P238 (research/issue17/parish-marriage-1885-04455.json, 2026-11-09),
// dokaz-seji P239 (parish-marriage-1884-04455.json) in dokaz-seji P240 (parish-marriage-1883-04455.json).
// NOVA LINIJA: poročna-predzgodovina (krstna-04104-KONČANA-15/15-P236-sinteza! + forenzika-P237!).
// Vir: poročna knjiga 04455 (Trauungs-Buch), Matricula Online — skeni s56–s61 == Pag. 55–60
// (★★★ Pag = sken−1 RAZŠIRJENO na 55–66; prej P84: samo 61–66!). P239: s52–s56. P240: s50–s52.

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

// ——— P239: leto 1884 = 2/13 — s52–s56, 18 vpisov, RESTART = s53 ———

/** Bloki P239 (leto 1884) iz korpusa — izpeljano 1:1 (h54 × h44 · h47 × h34 · h36-nevesta). */
export const MARRIAGE_1884_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1884,
);

/** Št. Griblje porok 1884 v korpusu (meritev: 3 — 2 polna Griblje×2 + 1 Griblje-nevesta; 2 X-open NISTA bloka). */
export const MARRIAGE_1884_GRIBLJE = MARRIAGE_1884_BLOCKS.length;

/** Hiše poročne linije 1884 (merjeni vrstni-red blokov: 54, 47, 36). */
export const MARRIAGE_1884_HOUSES = MARRIAGE_1884_BLOCKS.map((h) => h.houseNo);

/** Vsi vpisi leta 1884 (meritev: 18 številčenih — zap 1.–18., BREZ preskokov!). */
export const MARRIAGE_1884_TOTAL = 18;

/** X-open kandidati 1884 (v7 nevesta Hrizan? — Griblje-2?-duel-Vrtok-5 + v10 nevesta-dekla brez hišne) — NE-bloki! */
export const MARRIAGE_1884_XOPEN = [
  "v7 [~X-OPEN]",
  "v10 [~X-OPEN]",
] as const;

/** Meje leta 1884: restart = s53 (vpis 1 = 6. Februar, Martin PEZDIRC!) · meja-1883/84 = s52→s53 · meja-1884/85 = s56-tail (P238-1:1!). */
export const MARRIAGE_1884_MEJA = {
  restartSi: "restart-vpis-1 = 6. Februar 1884 (s53, velika-glava-»1884«, ženin Martin PEZDIRC!)",
  restartEn: "restart-entry-1 = Feb 6, 1884 (s53, the big-»1884«-heading, groom Martin PEZDIRC!)",
  tailSi: "tail-vpis-18 = 23. Novembris 1884 (s56, RESTART-1885-na-isti-strani!)",
  tailEn: "tail-entry-18 = Nov 23, 1884 (s56, the 1885-restart on the same page!)",
  boundarySi: "meja-1883/84 = s52→s53 (s52 = tail-1883-vpisi-8–12-vsi-»1883«!)",
  boundaryEn: "the 1883/84 boundary = s52→s53 (s52 = the 1883-tail-entries-8–12-all-»1883«!)",
} as const;

/** Številčenje strani 1884 (s53=1–5 · s54=6–10 · s55=11–14 · s56=15–18) — ultra-zoom-RAZREŠITEV: s55-prva = '11.' (dve-navpični-črti, NE-'12.' — 3:1!). */
export const MARRIAGE_1884_NUMBERING =
  "s53 = vpisi 1–5 · s54 = 6–10 · s55 = 11–14 ('11.'-ultra-zoom-3:1!) · s56 = tail-15–18 — 18-VPISOV-BREZ-PRESKOKA (kontrast-1885-vpis-3-PRESKOČEN!)";

/** PEZDIRC-nit 1884: ×4 GROOMI (vpis-1-Martin + vpis-2-Mathias-[isti-vas-duel-Oslob/Podkraj/Plok-1!] + vpis-14-Janez-Črnomelj-152/352 + vpis-15-Matthias-Otok-1-tail!) — PEZDIRC-CONTINUUM-04104-×131→04455! */
export const PEZDIRC_1884_NIT =
  "×4-ženini (vpis-1-Martin-30 + vpis-2-Mathias-27-isti-hiša-1! + vpis-14-Janez-Črnomelj + vpis-15-Matthias-Otok-1) + priče/starši-[~Pezdivec/Peddirec-×2]";

/** MILEK-križ-nit 1884: +2 NOVA-bloka (v6-priča-Jovan-MIHELČ-[~Milech!] + v18-mati-ženina-Anna-roj.-MILEK-[~!]) — križ-235→237 (04455-48→50!). */
export const MILEK_1884_NIT =
  "v6-priča-MIHELČ-[~Milech!] + v18-mati-ženina-MILEK-[~!] = križ-235→237 (04455-×48→×50!)";

/** Duhovnik vseh 18 vpisov 1884 (1:1-kot-1885-PRIEST_1885!). */
export const PRIEST_1884 = "Franz Dovgan [~Dorgen/Doregan] — edini-duhovnik-vseh-18-vpisov (1:1-kot-1885!)";

/** Najstarejši par leta 1884 (vpis 12: 56 + 41 = 97 let [~duel-starost!]). */
export const OLDEST_PAIR_1884 = "56 + 41 = 97 let [~duel] (vpis 12, Jakobčič? × vdova)";

/** Vase-dueli 1884 (v1/v2-'Oslob/Podkraj/Plok'-1 + v7-'Voranci/Brasine'-13 + v9-'Boginja/Podgora/Borinja'-vas-12 + v10-'Ceroviči/Cerovica'-17 + v14-'Črnomelj-152/352'). */
export const MARRIAGE_1884_VILLAGE_DUELS = [
  "v1/v2 »Oslob/Podkraj/Plok« 1 [~X-OPEN]",
  "v7 »Voranci/Brasine« 13",
  "v9 »Boginja/Podgora/Borinja« vas 12",
  "v10 »Ceroviči/Cerovica« 17",
  "v14 »Črnomelj 152/352«",
] as const;

// ——— P240: leto 1883 = 3/13 — s50–s52, 12 vpisov, RESTART = s50-dno ———

/** Bloki P240 (leto 1883) iz korpusa — izpeljano 1:1 (h13-ženin-RADOVIČ · h2-ženin-HLEBEC). */
export const MARRIAGE_1883_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1883,
);

/** Št. Griblje porok 1883 v korpusu (meritev: 2 — oba-GRIBLJE-ženina; 1 X-OPEN-kandidat-v3-NI-blok). */
export const MARRIAGE_1883_GRIBLJE = MARRIAGE_1883_BLOCKS.length;

/** Hiše poročne linije 1883 (merjeni vrstni-red blokov: 13, 2). */
export const MARRIAGE_1883_HOUSES = MARRIAGE_1883_BLOCKS.map((h) => h.houseNo);

/** Vsi vpisi leta 1883 (meritev: 12 številčenih — zap 1.–12., BREZ preskokov!). */
export const MARRIAGE_1883_TOTAL = 12;

/** X-open kandidat 1883 (v3 ženin 'Granc 25'-duel-'Nemški-Rif' — ni-GRIBLJE) — NE-blok! */
export const MARRIAGE_1883_XOPEN = ["v3 [~X-OPEN]"] as const;

/** Meje leta 1883: restart = s50-DNO (vpis 1 = 21. Januar, Jovan CRNIČ!) · meja-1882/83 = s50-MID (tail-1882-vpisi-24–26!) · meja-1883/84 = s52→s53 (P239-1:1!). */
export const MARRIAGE_1883_MEJA = {
  restartSi: "restart-vpis-1 = 21. Januar 1883 (s50-DNO, števke-»1 8 8 3.«-razporejene-črez-stolpce!, ženin Jovan CRNIČ von-Bedenj-H.20-Adlešiči-[~])",
  restartEn: "restart-entry-1 = Jan 21, 1883 (the s50-BOTTOM, the-»1 8 8 3.«-digits-spread-across-the-columns!, groom Jovan CRNIČ from-Bedenj-no.20-Adlešiči-[~])",
  tailSi: "tail-vpis-12 = 28. Oktober 1883 (s52 — 1884-se-začne-na-naslednjem-listu!)",
  tailEn: "tail-entry-12 = Oct 28, 1883 (s52 — 1884-starts-on-the-next-spread!)",
  boundarySi: "meja-1882/83 = s50-MID (tail-1882-vpisi-24–26-novembra!-#26-Mathias-HRIZAN-GRIBLJE-36-tail!) · meja-1883/84 = s52→s53 (P239-1:1!)",
  boundaryEn: "the 1882/83 boundary = s50-MID (the 1882-tail-entries-24–26-of-November!-#26-Mathias-HRIZAN-GRIBLJE-36-tail!) · the 1883/84 boundary = s52→s53 (P239-1:1!)",
} as const;

/** Številčenje strani 1883 (s50 = restart-1 · s51 = 2–7 · s52 = 8–12) — nodat-ULTRA-ZOOM: s51-prva = '2.' (navpični-lok-Kurent, NE-'1.')-1:1! Pass-1-'statistika-1,8,8,3'-MISREAD = glava-1883-števke-razporejene-črez-stolpce (razrešeno-2:1!). */
export const MARRIAGE_1883_NUMBERING =
  "s50 = restart-1 · s51 = vpisi 2–7 (nodat-ultra-zoom-'prva-je-2.-ne-1.'!) · s52 = 8–12 (P239-1:1!) — 12-VPISOV-BREZ-PRESKOKOV · glava-'1 8 8 3.'-števke-črez-stolpce (pass-1-'statistika'-MISREAD-razrešen!)";

/** PEZDIRC-nit 1883: vpis-4-ženin-Miha-PEZDIRC-Podzemelj-3-'NI-Pegdirc'-ULTRA-ZOOM-črka-za-črko! + v5-priča-[~Pezdirc/Jakobrič-DUEL!] + v7-mati-neveste-roj.-Pezdič-[~pass-2] — PEZDIRC-CONTINUUM-04104-×131→04455! */
export const PEZDIRC_1883_NIT =
  "vpis-4-ženin-Miha-PEZDIRC-Podzemelj-3 (ultra-zoom-'NI-Pegdirc'-črka-za-črko!) + v5-priča-[~Pezdirc/Jakobrič-DUEL!] + v7-mati-roj.-Pezdič-[~1-read] = continuum-04104-×131→04455-se-širi-v-3.-letu-predzgodovine!";

/** MILEK-križ-kandidat 1883 (IZVEN-KORPUSA!): v10-nevesta-Margareth-'Milleh-(Milek/Milech)'-[~X-OPEN-3-branja-1:1] × Johann-Horvat-Metlika-45 — križ-×237-NESPREMENJEN (blok- ni-v-korpusu-iskreno!). */
export const MILEK_1883_KANDIDAT =
  "v10-nevesta-Margareth-Milleh-[~Milek/Milech]-×-Johann-Horvat-Metlika-45 = križ-KANDIDAT-IZVEN-KORPUSA (×237-ostaja-iskreno!)";

/** Duhovnik 1883: Franz Dovgan-[~garble-×5] + v12-'Michael-Fandorf-[?]'-1-read = NOVI-DUHOVNIK-KANDIDAT-[~X-OPEN!]. */
export const PRIEST_1883 =
  "Franz Dovgan [~Dorgan/Dergan/Lovgan-garble-×5] — dominanta (v1-v9!) + v12-'Michael-[?]'-Fandorf-[?]-pp. = NOVI-DUHOVNIK-KANDIDAT-[~1-read-X-OPEN!]";

/** HROVALJ-brat+sestra-isti-dan: v8-ženin-Mathias-HROVALJ-Kaplitz-8-[~Podmelc-DUEL] + v9-nevesta-Anna-HROVALJ-Kaplische-(ISTA-hiša!)-13.-Mai = brat+sestra-poroka-ISTI-DAN (cf.-h34-SILAH-sestrski-2-leta!). */
export const HROVALJ_1883_SIBLINGS =
  "v8-ženin-Mathias-HROVALJ-Kaplitz-8-[~Podmelc-DUEL] × Anna-Klepec/Hlepec-Boršt-16 + v9-nevesta-Anna-HROVALJ-'Kaplische'-(ISTA-hiša-[~]!) × Janez-Gašlevič/Jaklevič-PriLozja — brat+sestra-IZ-ISTE-HIŠE-poroka-ISTI-DAN-13.-Mai (1.×-v-predzgodovini!-cf.-h34-SILAH-sestrski-1884+1885!)";

/** Najstarejši par leta 1883 (v10: 28 + 28 = 56 — prvo-branje; starosti-dueli-[~]). */
export const OLDEST_PAIR_1883 = "28 + 28 = 56 let (vpis 10, Horvat × Milleh-[~] — starosti-dueli-[~!])";

/** Vas-dueli 1883 (v2-'Gradec-47/17-vs-Graduc'-fil.-cerkev! + v3-'Granc-25-vs-Nemški-Rif'-X-OPEN! + v8-'Kaplitz-vs-Podmelc'! + v12-'Gertsitsch-3-vs-5'!). */
export const MARRIAGE_1883_VILLAGE_DUELS = [
  "v2 »Gradec 47/17 vs Graduc« fil.-cerkev [~]",
  "v3 »Granc 25 vs Nemški Rif« [~X-OPEN]",
  "v8 »Kaplitz 8 vs Podmelc« [~]",
  "v12 »Gertsitsch 3 vs 5« [~]",
] as const;
