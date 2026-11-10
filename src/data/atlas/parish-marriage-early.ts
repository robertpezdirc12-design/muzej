// parish-marriage-early.ts — P238: POROČNA PREDZGOVINA 04455, leto 1885 = 1/13 NOVA LINIJA
// P239: leto 1884 = 2/13 (s52–s56, 18 vpisov, RESTART = s53, 3 Griblje bloka, MILEK-križ +2!).
// P240: leto 1883 = 3/13 (s50–s52, 12 vpisov, RESTART = s50-dno, 2 Griblje bloka h13+h2, h2 = 1.-poročni-04455-blok!).
// P241: leto 1882 = 4/13 (s45–s50, 26 vpisov, RESTART = s45-glava-PRED-vrstico-1!, 7 Griblje blokov, h1 = najnižja-hiša-KADARKOLI!, PEZDIRC ×5!).
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

// ——— P241: leto 1882 = 4/13 — s45–s50, 26 vpisov, RESTART = s45 (glava-PRED-vrstico-1!) ———

/** Bloki P241 (leto 1882) iz korpusa — izpeljano 1:1 (h35-nevesta · h38×h12 · h56-nevesta-vdova · h13×h52 · h8-nevesta · h1×h10 · h36-MERGE-z-P80-sidrom-1:1!). */
export const MARRIAGE_1882_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1882,
);

/** Št. Griblje porok 1882 v korpusu (meritev: 7 = 6-NOVIH + 1-MERGE-z-P80-sidrom-h36! — 3 POLNA ×2 (h38×h12 · h13×h52 · h1×h10!) + 4 Griblje-neveste/ženina; 2 X-OPEN-duela NISTA bloka). */
export const MARRIAGE_1882_GRIBLJE = MARRIAGE_1882_BLOCKS.length;

/** Hiše poročne linije 1882 (merjeni vrstni-red blokov: 35, 38, 56, 13, 8, 1, 36 [h36 = MERGE-z-P80-sidrom — na-koncu-arraya!]). */
export const MARRIAGE_1882_HOUSES = MARRIAGE_1882_BLOCKS.map((h) => h.houseNo);

/** Vsi vpisi leta 1882 (meritev: 26 številčenih — zap 1.–26., BREZ preskokov — 4. leto zapored!). Korpus: 6-NOVIH-blokov (+1-MERGE-z-P80-sidrom-h36!) — P238-h13-MERGE-vzorec! */
export const MARRIAGE_1882_TOTAL = 26;

/** X-open kandidati 1882 (v14-'Gradac/Griblje-2/Lette-40'-3-vasni-duel! + v17-'Nemiška-vas-9-vs-Griblje-8?'-Mličar/Mlinar-duel!) — NE-bloki! */
export const MARRIAGE_1882_XOPEN = [
  "v14 [~X-OPEN]",
  "v17 [~X-OPEN]",
] as const;

/** Meje leta 1882: restart = s45 (VELIKA-glava-'1882'-PRED-vrstico-1 — NOVA-4.-mejna-varianta!) · meja-1881/82 = s44→s45 · meja-1882/83 = s50-MID (P240-1:1!). */
export const MARRIAGE_1882_MEJA = {
  restartSi:
    "restart-vpis-1 = 1. Februar 1882 [~21.-Jänner-DUEL-2:2!] (s45, VELIKA-GLAVA-'1882'-PRED-VRSTICO-1-NE-V-GLAVI-STRANI!-NOVA-4.-MEJNA-VARIANTA!-ženin-Anton-TASIE!)",
  restartEn:
    "restart-entry-1 = Feb 1, 1882 [~Jan-21-DUEL-2:2!] (s45, the-BIG-'1882'-HEADING-BEFORE-row-1-NOT-in-the-page-head!-a-NEW-4th-BOUNDARY-VARIANT!-groom-Anton-TASIE!)",
  tailSi: "tail-vpis-26 = 26. November 1882 (s50-MID — Mathias-HRIZAN-GRIBLJE-36!-restart-1883-na-isti-strani-P240-1:1!)",
  tailEn: "tail-entry-26 = Nov 26, 1882 (s50-MID — Mathias-HRIZAN-GRIBLJE-36!-the-1883-restart-on-the-same-page-P240-1:1!)",
  boundarySi:
    "meja-1881/82 = s44→s45-glava (tail-1881-NI-na-s45-top!-1881-se-zaključi-na-s44!-p12-1:1!) · meja-1882/83 = s50-MID (P240-1:1!)",
  boundaryEn:
    "the-1881/82-boundary = s44→s45-heading (NO-1881-tail-on-s45-top!-1881-ends-on-s44!-p12-1:1!) · the-1882/83-boundary = s50-MID (P240-1:1!)",
} as const;

/** Številčenje strani 1882 (s45=1–4 · s46=5–8 · s47=9–12 · s48=13–17 · s49=18–23 · s50-tail=24–26) — nodat-trakovi-×5-1:1 → 26-VPISOV-BREZ-PRESKOKOV (4.-leto-zapored!-kontrast-1885-vpis-3-PRESKOČEN!). */
export const MARRIAGE_1882_NUMBERING =
  "s45 = restart-1–4 · s46 = 5–8 · s47 = 9–12 · s48 = 13–17 · s49 = 18–23 (nodat-trakovi-×5-1:1!) · s50-tail = 24–26 (P240-1:1!) — 26-VPISOV-BREZ-PRESKOKOV-4.-LETO-ZAPORED";

/** PEZDIRC-nit 1882: ×5-VPISOV (v9-Georg-ŽENIN-×-Margaretha-NEVESTA-OBA-PEZDIRC!-+ starši-oče-Georg-PEZDIRC-×-mati-Anna-roj.-Tomc-+ priča-Georg-PEZDIRC! + v15-nevesta-Maria-h52 + v16-ženin-Michael-Prusi-3-(oče-tudi-PEZDIRC!)-+ v18-nevesta-Anna-Otok-1-(priči-Matthias-×-Anton-PEZDIRC!)-+ v21-nevesta-Anna-[~Krupšiše-4]) = PEZDIRC-CONTINUUM-04104-×131→04455-v-4.-letu-predzgodovine! */
export const PEZDIRC_1882_NIT =
  "×5-vpisov (v9-OBA-Georg-×-Margaretha-PEZDIRC!-+ starši-PEZDIRC-×2-+ priča-PEZDIRC! + v15-Maria-h52 + v16-Michael-Prusi-3 + v18-Anna-Otok-1 + v21-Anna-[~]) + priče/starši-dodatno-×4 = continuum-04104-×131→04455-v-4.-letu!";

/** ★★★★★ h1-REKORD: vpis-23 = 1.-POROČNI-BLOK-NA-h1-KADARKOLI (najnižja-hiša!-preglasi-h2-P240-za-1-stopnjo!-h1-aktivna-v-04894-mrliški-1889/1890/1904!— poročna-zdaj-OUTRUNA-mrliško-tudi-na-h1-ZA-7-LET!-1882-vs-1889!). */
export const H1_1882_REKORD =
  "vpis-23-Nicolaus-LESIRO-GRIBLJE-1 = 1.-poročni-blok-na-h1-KADARKOLI! (najnižja-hiša!-preglasi-h2-P240!-h1-aktivna-04894-1889/1890/1904!-poročna-OUTRUNA-mrliško-tudi-na-h1-ZA-7-LET!)";

/** Duhovnik 1882: Franz-Dovgan-[~garble-dominanta]-×-v18-'Georg/Jurij-Dragon-[~]'-duel-1-read = DRUGI-duhovnik-kandidat-[~X-OPEN!]. */
export const PRIEST_1882 =
  "Franz Dovgan [~Dorgan/Dergan/Dorgam/Dorgun/Dvorjan-garble] — dominanta + v18-'Georg/Jurij-Dragon-[~]'-(p09-1-read!)- = DRUGI-DUHOVNIK-KANDIDAT-[~1-read-X-OPEN!]";

/** Foliacija-s45-branje-'93/94'-[~X-OPEN!]: pass-1-pageNote-je-prebrala-'Strani-93/94' — NE-ujema-s-pravilom-'Pag-=-sken−1'-(s45-→-Pag-44!)-P238/239/240-pravilo-je-bilo-preverjeno-samo-za-s56–s66! */
export const FOLIACIJA_1882_XOPEN =
  "s45-pass-1-branje-'Strani-93/94'-[~1-read!] vs pravilo-'Pag-=-sken−1'-(s45→Pag-44)-[~X-OPEN!]-P238/239/240-pravilo-preverjeno-samo-s56–s66-P240-sami-'[~predvidoma-NI-ločeno-preverjeno]'!";

/** BRINC/BRINEC-mreža 1882 (vpis-13: nevesta-Katharina-BRINC-vdova-h56 + oče-Ivan-Brinc + mati-Maria-roj.-Grunc-[~] + priči-Peter-×-Georg-BRINEC!). */
export const BRINC_1882_NIT =
  "v13-NEVESTA-Katharina-BRINC-vdova-48-let-h56! + oče-Ivan-Brinc + mati-Maria-roj.-Grunc-[~] + priči-Peter-×-Georg-BRINEC-[~Brinc-DUEL] = cf.-P238-BRINC/BRINEC-×2-bloki-+ usnjarska-veja!";

/** Vas-dueli 1882 (v14-'Gradac-5-vs-Griblje-2-vs-Lette-40'-3-branja! + v17-'Nemiška-vas-9-vs-Griblje-8?'-Mličar/Mlinar! + v21-'Krupšiše-4-[~]' + v2-'Mokre/Mohr-[~]'). */
export const MARRIAGE_1882_VILLAGE_DUELS = [
  "v14 »Gradac 5 vs Griblje 2 vs Lette 40« 3-branja [~X-OPEN]",
  "v17 »Nemiška vas 9 vs Griblje 8?« Mličar/Mlinar [~]",
  "v21 »Krupšiše 4« [~]",
  "v2 »Mokre 24 vs Mohr« [~]",
] as const;

// ——— P242: leto 1881 = 5/13 (s39–s44, 25 vpisov z 1-PRESKOKOM-12!, 9 Griblje blokov, RESTART = s39-letnica-v-stolpcu-NAD-vrstico-1!, h52-firstYear-DVIG-1882→1881!, PEZDIRC-ženi n-v14-h42!) ———

/** Bloki P242 (leto 1881) iz korpusa — izpeljano 1:1 (h27-ženi n · h4-nevesta · h28×h8-POLNI · h42-PEZDIRC-×-h27-POLNI · h41×h52-POLNI · h16-nevesta!). */
export const MARRIAGE_1881_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1881,
);

/** Št. Griblje porok 1881 v korpusu (meritev: 9 = 3-POLNA ×2 (h28×h8 · h42×h27 · h41×h52!) + h27-ženi n + h4-nevesta + h16-nevesta!-h27-×2-BLOKA-V-1-LETU-PRVIČ!). */
export const MARRIAGE_1881_GRIBLJE = MARRIAGE_1881_BLOCKS.length;

/** Hiše poročne linije 1881 (merjeni vrstni red blokov: 27, 4, 28, 8, 42, 27, 41, 52, 16). */
export const MARRIAGE_1881_HOUSES = MARRIAGE_1881_BLOCKS.map((h) => h.houseNo);

/** Vsi vpisi leta 1881 (meritev: 25 DISTINCT — 1–11 + 13–26!-PRESKOK-12!-kontrast-1882-26-BREZ-preskokov!). */
export const MARRIAGE_1881_TOTAL = 25;

/** Ordinalna anomalija: pisar je preskočil vpis 12 (s41-konec-11→s42-zacetek-13!-[X-OPEN-DUEL: ali-s42=12–15-preskok-16!]-5.-številčenjska-anomalija-linije-cf.-1885-vpis-3-P238!). */
export const MARRIAGE_1881_ZAP_SKIPPED = 12;

/** X-open hišni dueli 1881 (v4-nevesta-'4:8:47'-3-branja! + v13-ženi n-'28-vs-26'! — NE-bloki!-h4/h28-vzeti-kot-glavni-bloki). */
export const MARRIAGE_1881_XOPEN = [
  "v4-nevesta [~4:8:47]",
  "v13-ženi n [~28:26]",
] as const;

/** Meje leta 1881: restart = s39 (letnica-v-datumskem-stolpcu-NAD-vrstico-1 — NOVA-5.-mejna-varianta!) · meja-1880/81 = s38→s39 · meja-1881/82 = s44→s45-glava (P241-1:1!). */
export const MARRIAGE_1881_MEJA = {
  restartSi:
    "restart-vpis-1 = 16. Jänner 1881 (s39, letnica-'1881'-ročno-v-DATUMSKEM-STOLPCU-NAD-VRSTICO-zap.-št.-1!-NOVA-5.-MEJNA-VARIANTA-skromna!-cf.-1882-VELIKA-GLAVA-+ 1883-'1-8-8-3.'-razporejena-+ 1884/1885-vrhnja!)",
  restartEn:
    "restart-entry-1 = Jan 16, 1881 (s39, the-year-'1881'-handwritten-in-the-DATE-COLUMN-ABOVE-row-zap.-1!-a-NEW-5th-BOUNDARY-VARIANT-modest!-cf.-the-1882-BIG-HEADING-+ the-1883-scattered-+ the-1884/1885-top!)",
  tailSi: "tail-vpis-26 = 20. Dezember 1881 (s44 — P241-MEJA-IZPOLNJENA-1:1!-'1881-se-zaključi-na-s44'!-nič-1882-na-s44!)",
  tailEn: "tail-entry-26 = Dec 20, 1881 (s44 — the-P241-BOUNDARY-FULFILLED-1:1!-'1881-ends-on-s44'!-nothing-1882-on-s44!)",
  boundarySi:
    "meja-1880/81 = s38→s39 (tail-1880-pričakovan-na-s38-P243!-[X-OPEN!]) · meja-1881/82 = s44→s45-glava (P241-1:1-dokaz!)",
  boundaryEn:
    "the-1880/81-boundary = s38→s39 (the-1880-tail-expected-on-s38-P243!-[X-OPEN!]) · the-1881/82-boundary = s44→s45-heading (the-P241-1:1-proof!)",
} as const;

/** Številčenje strani 1881 (s39=1–4 · s40=5–7 · s41=8–11 · s42=13–16-PRESKOK-12! · s43=17–20 · s44=21–26) — 25-VPISOV-z-1-PRESKOKOM (kontrast-1882-26-BREZ-preskokov!-cf.-1885-vpis-3-P238!). */
export const MARRIAGE_1881_NUMBERING =
  "s39 = restart-1–4 · s40 = 5–7 · s41 = 8–11 · s42 = 13–16 (PRESKOK-12!-11→13!-· ali-s42=12–15-preskok-16-[~X-OPEN-DUEL!]) · s43 = 17–20 · s44 = 21–26 — 25-VPISOV-z-1-PRESKOKOM";

/** ★★★★ PEZDIRC-nit 1881: ženi n-v14-Georg-PEZDIRC-GRIBLJE-42 (črka-za-črko-uz-A-1:1!-56-let-[~DUEL!]-×-Anna-geb.-Hrizom-[~Križan!]-GRIBLJE-27-POLNI ×2!) + PEZDIRC-v-s40-v7-starši ('Michael-Kathar.-PEZDIREC-½-Gübly'!) = CONTINUUM-04104-×131→04455-v-5.-letu-predzgodovine (1881-×1-+ 1882-×5-+ 1883-×1-+ 1884-×4-+ 1885-×3!). */
export const PEZDIRC_1881_NIT =
  "v14-ŽENIN-Georg-PEZDIRC-GRIBLJE-42 (črka-za-črko-'P-e-z-d-i-r-c'-1:1!-NI-'Pegdirc'!) × Anna-geb.-Hrizom-GRIBLJE-27-POLNI ×2! + starši-v-s40-v7-'Michael-Kathar.-PEZDIREC-½-Gübly' = continuum-04104-×131→04455-v-5.-letu!";

/** ★★★★★ h52-FIRSTYEAR-DVIG: vpis-17 = nevesta-Anna-Petrič-GRIBLJE-52-24.-Okt-1881 (uz-B-'jasno-5-nad-2'-1:1!-NE-32/42!) — h52-firstYear-1882→1881-ZA-1-LETO!-P241-'poročna-prehiti-krstno-na-h52-ZA-5-LET'-→-sedaj-ZA-6-LET!-h52-9→10-blokov! */
export const H52_1881_DVIG =
  "vpis-17-Anna-Petrič-GRIBLJE-52-24.-Okt-1881 = h52-firstYear-DVIG-1882→1881! (uz-B-'jasno-5-nad-2'-1:1!-NE-32/42!-P241-ZA-5-LET-→-ZA-6-LET!-h52-9→10-blokov-p242Note!)";

/** ★★★ TAPIČ↔ŠILAR-KRIŽ 1881: v23-ženi n-Marcus-TAPIČ-Gersiče-33 × nevesta-Katharina-ŠILAR-GRIBLJE-16 — starši-neveste-Mathias-Šilar-×-Anna-geb.-TAPIČ (nevestina-mati-verjetno-ženi nova-sorodnica!-nova-nit-linije!) + priči-Martin-×-Markus-TAPIČ (dva-Tapič!). */
export const TAPIC_SILAR_1881_KRIŽ =
  "v23-Marcus-TAPIČ-×-Katharina-ŠILAR-h16! + starši-neveste-Mathias-Šilar-×-Anna-geb.-TAPIČ (mati-≈-ženi nova-sorodnica-[~]!) + priči-Martin-×-Markus-TAPIČ = NOVA-nit-linije-P242!";

/** Duhovnik 1881: Franz-Dovgan-DORGON-DORGAN-DERGANZ-variante-iste-roke-[~]-dominanta-×~20-podpisov + v23-DUEL-[Dovgan-vs-Jemiar/Janžar!] = DRUGI-duhovnik-kandidat-[~X-OPEN!] + s39-v3-Derganz-kapelan-[~duel!]. */
export const PRIEST_1881 =
  "Franz Dovgan [~Dorgon/Dorgan/Drougar/Derganz-garble-iste-roke!] — dominanta-×~20 + v23-DUEL-[Dovgan-vs-'Jemiar/Janžar'-1-read!] = DRUGI-DUHOVNIK-KANDIDAT-[~X-OPEN!]";

/** Foliacija-1881: 'Pag. 38'-s39-NEDVOUMNO-+ 'Pag. 42'-s43-+ 'Pag. 43'-s44 = pravilo-'Pag-=-sken−1'-potrjeno-3/3-P242!-s40/s41/s42-predpostavljeno-39/40/41-[~nepreverjeno]. */
export const FOLIACIJA_1881 =
  "s39-'Pag. 38'-NEDVOUMNO-(uz-C-izrez-5!-'3'-zaokrožena-zanka-+ '8'-zaprta-zanki!) + s43-'Pag. 42' + s44-'Pag. 43' = pravilo-'Pag-=-sken−1'-3/3!-s40/s41/s42-predpostavljeno-[~nepreverjeno!]-P241-s45-'93/94'-[~X-OPEN]-ostaja";

/** BRINC-nit-continuum 1881 (v13-ženi n-Peter-BRINC-h28-×-Katharina-Horvasinič-h8!-cf.-1882-v13-BRINC-vdova-h56-P241-+ 1885-BRINC/BRINEC-P238!). */
export const BRINC_1881_NIT =
  "v13-ŽENIN-Peter-BRINC-GRIBLJE-28-36-let!-×-Katharina-geb.-Horvasinič-[~PREČRTAN-'Bunc'!]-GRIBLJE-8-POLNI ×2! = cf.-1882-v13-BRINC-vdova-h48-48-let-P241-+ 1885-BRINC/BRINEC-×2-P238!-starši-žena-Johann-Brine-×-Maria-geb.-KLOBUČAR!";

/** Vas/hišni dueli 1881 (v4-nevesta-'4:8:47'-3-branja!-+ v13-ženi n-'28-vs-26'!-+ v23-'Gersiče-33-vs-Gortice'!-+ v14-nevesta-priimek-'Hrizom-vs-Križan'!). */
export const MARRIAGE_1881_VILLAGE_DUELS = [
  "v4-nevesta »Griblje 4 vs 47 vs 8« 3-branja [~X-OPEN]",
  "v13-ženi n »Griblje 28 vs 26« 2:1 [~]",
  "v23-ženi n »Gersiče 33 vs Gortice« [~]",
  "v14-nevesta »Hrizom vs Hrizan/Križan« [~]",
] as const;

// ——— P243: POROČNA PREDZGOVINA 04455, leto 1880 = 6/13 (s35–s38; restart-s35-DNO NOVA-7.-MEJNA-VARIANTA!) ———

/** Griblje bloki poročne linije 1880 v korpusu (merjeni vrstni red: h24-vpis-4-s36 · h63-vpis-14-s37 · h53-vpis-20-TAIL-s38!). */
export const MARRIAGE_1880_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1880,
);

/** Št. Griblje porok 1880 v korpusu (meritev: 3 = h24-BRINE + h63-KRIŽAN × Pegdirec + h53-PERDIRC-[~Pegdirc!]!-vsi-ženi n-bloki!). */
export const MARRIAGE_1880_GRIBLJE = MARRIAGE_1880_BLOCKS.length;

/** Hiše poročne linije 1880 (merjeni vrstni red blokov: 24, 63, 53). */
export const MARRIAGE_1880_HOUSES = MARRIAGE_1880_BLOCKS.map((h) => h.houseNo);

/** Vsi vpisi leta 1880 (meritev: 20 DISTINCT = 2-s35-dno-restart + 6-s36 + 6-s37 + 6-s38-tail!-BREZ-preskokov-kontrast-1881-PRESKOK-12!). */
export const MARRIAGE_1880_TOTAL = 20;

/** Meje leta 1880: RESTART-1880 = s35-DNO (NOVA-7.-MEJNA-VARIANTA: restart-1–2-na-dnu + letnica-v-datumskem-stolpcu-VRSTE-3-na-s36!) · meja-1879/80 = s35-mid (33→1–2!) · meja-1880/81 = s38→s39 (finis! + P242-2×-1:1!). */
export const MARRIAGE_1880_MEJA = {
  restartSi:
    "restart-vpisi-1–2 = s35-DNO (številčenje-31-32-33 → RESTART-1–2!-numcol-3×-1:1!-vpis-1 = 1. Jänner[~4.-DUEL]-Peter/Janez-Jakljevic[?]-'ž.-Griblan' × Martha-Juhlevič[?]-'zu-Grüble[?]'; vpis-2 = 4. Feb-Janez-Dragot-Dragote-4!) — NOVA-7.-MEJNA-VARIANTA (restart-na-dnu-prejšnje-strani-P240-1883-vzorec!-+ letnica-'1880'-v-datumskem-stolpcu-VRSTE-3-na-s36-'1880,-4.-Febr.'-pass-5-1:1!-kombinacija-P240+P242!)",
  restartEn:
    "restart-entries-1–2 = s35-BOTTOM (numbering-31-32-33 → RESTART-1–2!-numcol-3×-1:1!-entry-1 = Jan 1[~4.-DUEL]-Peter/Janez-Jakljevic[?]-'ž.-Griblan' × Martha-Juhlevič[?]-'zu-Grüble[?]'; entry-2 = Feb 4-Janez-Dragot-Dragote-4!) — a-NEW-7th-BOUNDARY-VARIANT (restart-at-the-bottom-of-the-previous-page-the-P240-1883-pattern!-+ the-year-'1880'-in-the-DATE-COLUMN-of-ROW-3-on-s36-pass-5-1:1!-the-P240+P242-combination!)",
  tailSi:
    "tail-vpis-20 = 21. November 1880 [~25.-DUEL-2:1-za-21!-TRETJI-DOKAZ-margine-'Gaveldzettel...21.-November-1880'!] (s38-TAIL!) + s38-dno-'finis / s 1880' = ZAKLJUČNA-OZNAKA-LETA (1.-ta-vrsta-v-poročni-predzgodovini!-cf.-mrliške-zaključne-opombe-P181!)",
  tailEn:
    "tail-entry-20 = Nov 21, 1880 [~25.-the-DUEL-2:1-for-21!-the-THIRD-PROOF-margine!] (s38-TAIL!) + s38-bottom-'finis / s 1880' = the-YEAR-END-MARK (the-1st-of-this-kind-in-the-early-marriage-line!)",
  boundarySi:
    "meja-1879/80 = s35-mid (33→1–2-restart!) · meja-1880/81 = s38→s39 (s39-top-letnica-'1881'-nad-vrsto-1-P242-2×-neodvisno-1:1!-REŠENA!)",
  boundaryEn:
    "the-1879/80-boundary = s35-mid (33→1–2-restart!) · the-1880/81-boundary = s38→s39 (the-s39-top-'1881'-P242-2×-independently-1:1!-RESOLVED!)",
} as const;

/** Številčenje strani 1880 (s35 = 31–33 + restart-1–2-dno! · s36 = 3–8 · s37 = 9–14 · s38 = 15–20-tail) — 20-VPISOV-BREZ-PRESKOKOV (3.-leto-BREZ-kontrast-1881!). */
export const MARRIAGE_1880_NUMBERING =
  "s35 = 31–33-1879 + RESTART-1–2-dno! · s36 = 3–8 (6-vrstic!-numcol-3×-3-nesmiselna-branja-konvergirala!) · s37 = 9–14 (pass-2-'[8]'-dan-'8.'-Februar-bleed-MISREAD!-pass-1-+ pass-3-9–14-1:1!) · s38 = 15–20-tail (vsi-passi-1:1!) → 20-VPISOV-BREZ-PRESKOKOV (kontrast-1881-PRESKOK-12!)";

/** ★★★ h53-firstYear-DVIG: vpis-20 = ženi n-Peter-PERDIRC-[~Pegdirc-DUEL!]-GRIBLJE-53-21.-Nov-1880 — h53-firstYear-04455-1890→1880-DVIG-ZA-10-LET! (+ margine-'Gaveldzettel-der-Gemeinde-Griblje'-1.-ta-vrsta-dokumenta!). */
export const H53_1880_DVIG =
  "vpis-20-Peter-PERDIRC-[~Pegdirc-DUEL!]-GRIBLJE-53-21.-Nov-1880 = h53-firstYear-04455-1890→1880! (DVIG-ZA-10-LET!-+ margine-'Gaveldzettel-der-Gemeinde-Griblje-vom-21.-November-1880'-+ 'Väterliche-Einwilligung'-očetova-privolitev-1.-ta-vrsta-dokumenta-v-predzgodovini!-h53-04105-firstYear-1887-→-poročna-OUTRUNA-krstno-na-h53-ZA-7-LET!-h53-21→22-blokov!)";

/** ★★★ h63-KRIŽAN-continuum: vpis-14 = ženi n-Križan-Miklavčič-GRIBLJE-63-4.-Juli-1880 × Magdalena-[?]-PEGDIREC-[~Pezdirc!] — cf.-P239-lead-mrliška-04106-1884-h63-KRIŽAN-×2 (nit-4-leta!) + PEZDIRC-continuum! */
export const KRIZAN_1880_NIT =
  "vpis-14-ženi n-Križan-Miklavčič-GRIBLJE-63 (ultra-zoom-2.4×-1:1!-priimek-duel-pass-1-'Bričan'-2:1!) × Magdalena-[?]-PEGDIREC-[~Pezdirc-DUEL!]-hči-Marka-Pegdirec-dekla-v-Gribljah = h63-KRIŽAN-nit-cf.-P239-lead-mrliška-1884-h63-KRIŽAN-×2 (NIT-4-LETA-1880→1884!) + PEZDIRC-CONTINUUM-×131→04455-v-6.-letu-predzgodovine (1880-×2-reads + s36-mater-[~Pedirec-×2-branja!] = ×3-reads!-cf.-1881-×1-1882-×5-1883-×1-1884-×4-1885-×3!)";

/** BRINC/BRINEC-mreža 1880: vpis-4 = ženi n-Mathias-BRINE-[~Brinc/Brinec-DUEL!]-GRIBLJE-24-s36 (ultra-zoom-2.2×-1:1!) — cf.-P238-h26-BRINEC-usnjar-+ P242-v13-Peter-BRINC-+ 1885-BRUNC-[~Brinc!]-mati! */
export const BRINC_1880_NIT =
  "vpis-4-ženi n-Mathias-BRINE-GRIBLJE-24 (bauernsohn-24-let!-ultra-zoom-2.2×-1:1!-priimek-DUEL-'Brine/Brinc/Brinec'-iskreno!) = h24-1.-poročni-dokaz-v-predzgodovini (h24-04455-1896-P125-→-poročna-OUTRUNA-sama-sabo-ZA-16-LET!) — cf.-P238-h26-BRINEC-+ P242-v13-Peter-BRINC-h28-+ P238-mati-'BRUNC-[~Brinc!]'-mreža-4-leti!";

/** GRIBLJAN-IZVOR-pripise 1880 (cf.-P242-s41-'z-Gribl.'-×9!): s35-dno-vpis-1-+ vpis-2-oba-ženi n-'ž.-Griblan'-[~'ged.-Griblan'?]-bivališča-Drilazje-30[?]-+ Dragote-4-NI-bloki-pošteno! */
export const GRIBLJAN_1880_IZVOR =
  "s35-dno-vpis-1 (Peter/Janez-Jakljevic[?]-'ž.-Griblan'-Drilazje-30[?]-×-Martha-Juhlevič[?]-'zu-Grüble[?]-brez-številke-[~X-OPEN!]') + vpis-2 (Janez-Dragot-'ž.-Griblan'-Dragote-4-×-Maria/Rozalija-Dragot!) = GRIBLJAN-IZVOR-pripise-×2 (rozen/izvor-Griblje-bivališče-drugje-NI-bloki!-pošteno!-cf.-P242-s41-'z-Gribl.'-×9-NOVA-podkategorija!)";

/** Foliacija-1880-[~X-OPEN-DUEL]: s38-TR-'Pag. 34.'-(2×-branja-pass-2-'34~'-+ pass-6b-3×-'34.')-vs-pričakovano-'Pag. 37'-(pravilo-Pag==sken−1; s39-'Pag. 38'-2×-1:1-potrjeno!). */
export const FOLIACIJA_1880_XOPEN =
  "s38-'Pag. 34.'-2×-branja-(pass-2-1:1-dvom-'34~'-+ pass-6b-3×-'34.')-vs-pričakovano-'Pag. 37'-(pravilo-Pag==sken−1-iz-s39-'Pag. 38'-2×-neodvisno-1:1!-[7-vs-4-Kurrent-zmeda-cf.-P162b!-ali-dup-vstavljen-list-cf.-P149-s175=s176!])-[~X-OPEN-DUEL-pošteno-ostaja!]";

/** Duhovnik 1880: Franz-Dovgan/Dovžan-[~Dorgano-garble!]-continuum-6-let (1880–1885!-s35-dno-×2-+ s37-v14-+ cf.-1881–1885-dominanta!). */
export const PRIEST_1880 =
  "Franz-Dovgan/Dovžan-[~Dorgano-garble!] — s35-dno-vpis-1-+ vpis-2-×2-+ s37-vpis-14-('Fran-Dovžan[?]-Fran-Dovjana[?]'!)-continuum-DOVGAN-6-LET-1880–1885 (1:1-kot-1881–1885-dominanta!)";

/** Datum-dueli 1880 (v20-'21-vs-25'-Nov!-v1-'1-vs-4'-Jän!-v15-'10-vs-16'-Okt!-v19-'11-vs-14'-Nov!). */
export const MARRIAGE_1880_DUELS = [
  "v20-datum »21. vs 25. November« 2:1 [~] (pass-3-+ pass-6-21!-+ margine-Gaveldzettel-21.-TRETJI-DOKAZ!)",
  "v1-datum »1. vs 4. Jänner 1880« [~X-OPEN] (pass-6-'1.-Jänner-18[80]'-vs-pass-5-'4.-Jänner-1880'!)",
  "v15-datum »10. vs 16. Oktober« [~X-OPEN] (pass-2-'10.-Okt'-vs-pass-1-'16.-Okt!')",
  "v19-datum »11. vs 14. November« [~X-OPEN] (pass-1-'11.-Nov'-vs-pass-3-'14.-Nov!')",
] as const;

/** Vse-nove-1880-meritve-v-obliki-za-QA (skupaj-04455: 223→226 · vitals: 1966→1969 · sidra: 216→219-1880:3! · dobe: 190→193-23-pred-linijskih!). */
export const MARRIAGE_1880_KORPUS = {
  skupaj04455: 226,
  skupajVitals: 1969,
  sidra: 219,
  dobe: 193,
} as const;

/** ——— P244: poročna predzgodovina 04455, leto 1879 = 7/13 (s27–s35; RESTART-s27-top velika-glava + GLAVA-PONOVLJENA-NA-VSAKEM-LISTU-NOVA-8.-MEJNA-VARIANTA! + FOLIACIJA-4/4→P243-DUEL-REŠEN!) — 33 VPISOV-BREZ-PRESKOKOV · 9-GRIBLJE-blokov (h16-×2-BLOKA!) ——— */
export const MARRIAGE_1879_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1879,
);
export const MARRIAGE_1879_GRIBLJE = MARRIAGE_1879_BLOCKS.length;
export const MARRIAGE_1879_HOUSES = MARRIAGE_1879_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1879_TOTAL = 33;

/** Meje 1879: RESTART-s27-top (velika-glava-'1879'-pred-vrstico-1!-vpis-1 = 29. Jänner[~März-DUEL] Klepec-[~TRIPLE-DUEL!]-h16 × Jurejevič-h10!) + MEJA-1878/79 = s26→s27 (tail-1878-Krugel-[~]-s26-dno!) + MEJA-1879/80 = s35-mid (P243-1:1!-vpisi-31–33-tail!) + GLAVA-PONOVLJENA-NA-VSAKEM-LISTU (s27–s34 VSE!-mrliški-vzorec-60.–74.-POTRDILO!-NOVA-8.-MEJNA-VARIANTA!) + tail-vpis-33 = 17. März-Tabor × Judnič-s35-top! */
export const MARRIAGE_1879_MEJA = {
  restartSi:
    "restart-vpis-1 = 29. Jänner 1879 [~März-DUEL-2-branja!-pass-1+2+3-za-Jänner!] = s27-TOP (VELIKA-glava-'1879'-na-ZAČETKU-leve-polovice-PRED-vrstico-zap.-št.-1!-cf.-P241-4.-VARIANTA!) — ženin-Georg-Klepec-[~Klejec/Klobučar/Pegdirc-TRIPLE-DUEL-4-branja!]-½-Güblar-GRIBLJE-16-[~DUEL-Otok-1!] ×-Marie-Jurejevič-GRIBLJE-10-[~3-branja!]-+ MODRI-pripis-'Civil-Beizag-präsent-...-Dechant-von-Admont-9.-Jänner-1879'-NOV-ELEMENT-[~X-OPEN!]",
  restartEn:
    "restart-entry-1 = Jan 29, 1879 [~März-DUEL!] = s27-TOP (the-BIG-heading-'1879'-BEFORE-entry-row-1!-cf.-P241-4th-VARIANT!) — groom-Georg-Klepec-[~TRIPLE-DUEL-4-readings!]-½-Güblar-GRIBLJE-16-[~DUEL-Otok-1!] ×-Marie-Jurejevič-GRIBLJE-10-[~3-readings!]-+ the-MARGIN-note-'Civil-Beizag-präsent'-NEW-element-[~X-OPEN!]",
  tailSi:
    "tail-vpis-33 = 17. März 1879 (s35-TOP-P243-1:1!) — Matthias-Tabor-'Grünzl[?]-Zühtnerig-v.-Knezina-13[?]' ×-Katherina-Judnič[~]-hiša-30[?]-+ v31-Jožef-Požeh[?]-'Griblje-77[?]'-×-Hrizan[~]-+ v32-'Lunnauševšč[?]'-×-Mravinec-NI-bloki-pošteno!-+ s35-tail-D-PODPIS-'Copulatus-sum...Dopgan'-1879!-+ starš-'½-Gübl.-Mileh'-[~MILEK-križ-kandidat!]",
  tailEn:
    "tail-entry-33 = Mar 17, 1879 (s35-TOP-P243-1:1!) — Matthias-Tabor × Katherina-Judnič[~]-+ v31-Jožef-Požeh[?]-×-Hrizan[~]-+ v32-NI-bloki-honestly!-+ the-s35-tail-D-SIGNATURE-'Copulatus-sum...Dopgan'-1879!-+ parent-'½-Gübl.-Mileh'-[~MILEK-cross-candidate!]",
  boundarySi:
    "meja-1878/79 = s26→s27 (tail-1878-Georg-Krugel-[~Krigel!]-½-Grubl-s26-DNO!-opomba-'dd.-12-Jänner-879'-priča-[~X-OPEN!]) · meja-1879/80 = s35-mid (33→restart-1–2-P243-1:1!) — GLAVA-'1879'-PONOVLJENA-NA-VSAKEM-RAZPRTEM-LISTU-s27–s34 (mrliški-vzorec-mej-60.–74.-POTRDILO-ČEZ-KNJIGE!) = NOVA-8.-MEJNA-VARIANTA!",
  boundaryEn:
    "the-1878/79-boundary = s26→s27 (the-tail-1878-Krugel-[~]-s26-BOTTOM!-note-'dd.-12-Jänner-879'-witness-[~X-OPEN!]) · the-1879/80-boundary = s35-mid (P243-1:1!) — the-'1879'-heading-REPEATED-ON-EVERY-SPREAD-s27–s34 (the-death-register-boundary-pattern-CONFIRMED-ACROSS-BOOKS!) = the-NEW-8th-MEJNA-VARIANT!",
} as const;

/** Številčenje strani 1879 (s27 = 1–2 · s28 = 3–8 · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33) — 33-VPISOV-BREZ-PRESKOKOV (5.-leto-BREZ-kontrast-1881!). */
export const MARRIAGE_1879_NUMBERING =
  "s27 = 1–2 (restart!) · s28 = 3–8 (6-vrstic-pass-1-samo-3-videl-krop-stolp-3×!-v3-Wingler-Cerknobl-vojak!-v5-Pezdirc-50!-v6-Luniri-Vranovice!) · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33-tail (P243!)";

/** ★★★★★ FOLIACIJA-1879-'Pag = sken−1'-4/4 (s27-'Pag. 26' + s30-'Pag. 29' + s34-'Pag. 33' + s35-'Pag. 34'!-vsi-ultra-zoom-1:1!) → P243-s38-'Pag. 34.'-X-OPEN-DUEL-REŠEN: pravilo-Pag==sken−1-OSTAJA (s38-branje-'34'-= MISREAD-'37'-0-vs-7-Kurrent-cf.-P162b!) — s31-'Pag. 36.'-[~MISREAD-'30'-0-vs-6-DUEL-podporjen!]. */
export const FOLIACIJA_1879_REŠITEV =
  "s27-'Pag. 26'-1:1-+ s30-'Pag. 29'-1:1-+ s34-'Pag. 33'-1:1-+ s35-'Pag. 34'-1:1 = 4/4-1879!-→ P243-X-OPEN-DUEL-REŠEN (s38-'Pag. 34.'-branje = MISREAD-'Pag. 37'!-pravilo-Pag==sken−1-NE-PRELAMA!-cf.-P162b-7-vs-4-Kurrent-zmeda-zdaj-tudi-0-vs-7-+ 0-vs-6!)";

/** ★★★ h50-PT-luknja-hiša-1.-poročni-dokaz-v-predzgodovini + h16-×2-BLOKA-V-1-LETU (2.×-linije-cf.-P242-h27!) + h63-KRIŽAN-2.-leto-ZAPORED (1879-nevesta-→-1880-ženin!-NIT-5-LET-z-mrliško-1884!) + PEZDIRC-×2-ženinov-v-1-letu (v5-Mathias-h50-+ v21-Georg-h42-[~Pegdirc!]-+ v16-priča-'Pezdire'-[~!] = 7.-leto-continuum!) + BRINC-5.-leto (v12-mati-v12-×-P243-v4-ženi n-h24-ZAPORED!) + ŠILAR-vdova (v9-verw.-Schilar!) + TOMC-×3-TRIPLET (v9-Georg + v20-Martin + v25-Matthius!) + Kralj-h17-cf.-P151-1922 (ISTO-DRUŽINA: Johann-1879 → Jurij-1922!). */
export const H50_1879_PT_LUKNJA =
  "vpis-5-Mathias-Pezdirc-GRIBLJE-50-×-Maria-Škuncelj-44-5.-Februar-1879 = h50-1.-POROČNI-DOKAZ-V-PREDZGODOVINI (PT-luknja-hiša-P191-dokazana-mrliško!-poročna-predzgodovina-zdaj-tudi-h50!-cf.-h24-P243-v4-→-h50-cf.-1896-P125-linija!)";

export const H16_1879_DVOJNA =
  "h16 = ×2-BLOKA-V-1879 (v1-ženin-Georg-Klepec-[~TRIPLE-DUEL!]-29.-Jänner-+ v25-ženin-Matthius-Tomc-4.-Mai!) = 2.×-linije-DA-ISTO-LETO-×2-BLOKA (cf.-P242-h27-×2-bloka-v-1881!-P243-h27-×2!-vzorec-DRUŽINSKIH-VEJ!)";

export const KRIZAN_1879_NIT =
  "v21-Georg-Pegdirec-[~Pezdirc!]-GRIBLJE-42-×-Dorothea-Hrizan-[~Križan!]-GRIBLJE-63-19.[~Feber?]-1879 (ultra-zoom-1:1-CLEARED!) = h63-KRIŽAN-2.-LETO-ZAPORED (1879-nevesta-→-1880-ženin-Križan-Miklavčič-P243-v14!-NIT-5-LET: 1879→1884-mrliška-×2-P239!) + margine-'Gesuchs-1879-...der-Gemein[de]'-[~GAVELDZETTEL-cf.-X-OPEN!]";

export const PEZDIRC_1879_CONTINUUM =
  "PEZDIRC-CONTINUUM-×131→04455-v-7.-LETU-predzgodovine: v5-ženin-Mathias-Pezdirc-h50-1:1-krop!-+ v21-ženin-Georg-Pegdirc-[~DUEL-grafija!]-h42-ultra-zoom!-+ v16-priča-'Pezdire'-[~!] — 2-ŽENINOV-×-1-PRIČA-v-1-letu = NAJBOLJŠI-1879-PODATKEK!";

export const BRINC_1879_NIT =
  "v12-Johann-Požeh-GRIBLJE-21-×-Maria-Brinc-[~Brüne/Princ-DUEL!]-GRIBLJE-24-12.-Feber-1879 = h24-2.-LETO-ZAPORED (1879-nevesta-→-1880-ženin-Mathias-BRINE-P243-v4!) + BRINC/BRINEC-MREŽA-5.-leto (P238-BRUNC-mati-+ P242-v13-Peter-BRINC-+ P243-v4-BRINE!) + DRAGOŠ-nit (mati-Maria-Dragos!) + h21-cf.-P151-1922-h21-Požek!";

export const DOVGAN_1879_PODALJŠITEV =
  "DOVGAN-CONTINUUM-PODALJŠAN-NA-7-LET (1879–1885!): s35-tail-D-podpis-'Copulatus-sum-Griblje-d.-14/9-1879.-Dopgan'-1:1!-+ v16-duhovnik-'Franc-[~Pasthic/Dovgan-DUEL!]'-+ s27-v1-modri-pripis-'Anton-Franz-von-Dovgan-Dechant'-omenjen-[~X-OPEN-kaj-točno!]";

export const MILEK_1879_KRIZ =
  "MILEK-križ-kandidat-IZVEN-korpusa (pošteno!): s35-tail-D-starš-'½-Gübl.-Mileh'-[~MILEH-1-branje!]-v-vpisu-31-Jožef-Požeh[?]-[~Griblje-77?] = križ-×237→×238-[~]-cf.-P240-Milleh-3-branja-+ P239-v18-mati-MILEK-+ P242-NI-+ P243-NI!-iskreno-odprto-X-OPEN";

/** Datum-dueli 1879 (v1-'29.-Jänner-vs-März'-2:1!-+ v15/v16/v17-'19.'-3-poroke-isti-dan-kandidat-[~X-OPEN!]-+ v24-'23-vs-24'-Feb-[~]-+ v20/v21-'19.'-[~]). */
export const MARRIAGE_1879_DUELS = [
  "v1-datum »29. Jänner vs 29. März« 2:1-za-Jänner [~] (pass-1+2+3-Jänner!-pass-4-'März'-'Jänner'-oboje-v-branju!)",
  "v15+v16+v17-datum »19.«-3-poroke-isti-dan-kandidat [~X-OPEN] (cf.-P240-v5+v6-ISTA-DAN-+ P241-v6/v7-IZMENA!)",
  "v24-datum »23. vs 24. Februar« [~X-OPEN] (pass-1-'23'-vs-pass-2-'24'!)",
  "v20+v21-datum »19.[~Feber?]« [~X-OPEN] (2-branja-'bruar-1879'!)",
] as const;

/** Vse-nove-1879-meritve-v-obliki-za-QA (skupaj-04455: 226→235 · vitals: 1969→1978 · sidra: 219→228-1879:9! · dobe: 193→202-32-pred-linijskih!). */
export const MARRIAGE_1879_KORPUS = {
  skupaj04455: 235,
  skupajVitals: 1978,
  sidra: 228,
  dobe: 202,
} as const;
