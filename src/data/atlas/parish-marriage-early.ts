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

/** ——— P244: poročna predzgovorina 04455, leto 1879 = 7/13 (s26–s35; P245-KOREKCIJA: RESTART = s26-TOP-velika-letnica-v-vpisu-1-Fritz-×-Blasnik + številčenje-v-LEVI-MARGINI + GLAVA-ponovljena-s27–s34-je-PONOVITEV! + FOLIACIJA-5/5→P243-DUEL-REŠEN!) — 33 VPISOV-BREZ-PRESKOKOV · 9-GRIBLJE-blokov (h16-×2-BLOKA!) ——— */
export const MARRIAGE_1879_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1879,
);
export const MARRIAGE_1879_GRIBLJE = MARRIAGE_1879_BLOCKS.length;
export const MARRIAGE_1879_HOUSES = MARRIAGE_1879_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1879_TOTAL = 33;

/** Meje 1879: RESTART-s27-top (velika-glava-'1879'-pred-vrstico-1!-vpis-1 = 29. Jänner[~März-DUEL] Klepec-[~TRIPLE-DUEL!]-h16 × Jurejevič-h10!) + MEJA-1878/79 = s26→s27 (tail-1878-Krugel-[~]-s26-dno!) + MEJA-1879/80 = s35-mid (P243-1:1!-vpisi-31–33-tail!) + GLAVA-PONOVLJENA-NA-VSAKEM-LISTU (s27–s34 VSE!-mrliški-vzorec-60.–74.-POTRDILO!-NOVA-8.-MEJNA-VARIANTA!) + tail-vpis-33 = 17. März-Tabor × Judnič-s35-top! */
export const MARRIAGE_1879_MEJA = {
  restartSi:
    "P245-KOREKCIJA: restart-vpis-1 = 1. Jänner 1879 = s26-TOP (velika-letnica-'1879'-kot-predpona-datuma-vpisa-1-NI-posebna-glava!-cf.-P238/P239!) — ženin-Wilhelm-Fritz-[~frih/Kritz-DUEL!]-Ökonom-Wolfsberg-41-v-Kärnthen-stanuje-LOKA-1 (34-l) ×-Anna-Blasnik-[~Blahnik!]-Cerno-melj.-38 (43-l!) + v2-Krupljen-Cerno-12.-Jänner + v3-Krugel-DOBRANIČ-18-26.-Jänner (½-Gübler!-NI-blok!) — številčenje-v-LEVI-MARGINI-1–3 (modro-sivo!-Lfd.-stolpec-ne-obstaja!) + Franz-DOVGAN-podpis-×3! — P244-napaka: pass-1-s26-vrnil-PRAZNO-→-napačen-restart-s27; Klepec-29.-Jänner = vpis-4 (NE-1!)",
  restartEn:
    "P245-CORRECTION: restart-entry-1 = Jan 1, 1879 = s26-TOP (the-BIG-year-'1879'-as-the-PREFIX-of-entry-1's-date-NOT-a-separate-heading!-cf.-P238/P239!) — groom-Wilhelm-Fritz-[~frih/Kritz-DUEL!]-Ökonom-Wolfsberg-41-in-Carinthia-lives-at-LOKA-1 (34-y) ×-Anna-Blasnik-[~Blahnik!]-Cerno-melj.-38 (43-y!) + v2-Krupljen-Cerno-Jan-12 + v3-Krugel-DOBRANIČ-18-Jan-26 (½-Gübler!-NOT-a-block!) — the-numbering-IN-THE-LEFT-MARGIN-1–3 (blue-grey!-no-printed-Lfd.-column!) + Franz-DOVGAN-×3-signatures! — the-P244-error: pass-1-on-s26-returned-EMPTY-→-the-restart-wrongly-placed-on-s27; Klepec-Jan-29 = entry-4 (NOT-1!)",
  tailSi:
    "tail-vpis-33 = 17. März 1879 (s35-TOP-P243-1:1!) — Matthias-Tabor-'Grünzl[?]-Zühtnerig-v.-Knezina-13[?]' ×-Katherina-Judnič[~]-hiša-30[?]-+ v31-Jožef-Požeh[?]-'Griblje-77[?]'-×-Hrizan[~]-+ v32-'Lunnauševšč[?]'-×-Mravinec-NI-bloki-pošteno!-+ s35-tail-D-PODPIS-'Copulatus-sum...Dopgan'-1879!-+ starš-'½-Gübl.-Mileh'-[~MILEK-križ-kandidat!]",
  tailEn:
    "tail-entry-33 = Mar 17, 1879 (s35-TOP-P243-1:1!) — Matthias-Tabor × Katherina-Judnič[~]-+ v31-Jožef-Požeh[?]-×-Hrizan[~]-+ v32-NI-bloki-honestly!-+ the-s35-tail-D-SIGNATURE-'Copulatus-sum...Dopgan'-1879!-+ parent-'½-Gübl.-Mileh'-[~MILEK-cross-candidate!]",
  boundarySi:
    "meja-1878/79 = s25→s26 (P245-KOREKCIJA!-tail-1878 = s25: margina-22–23-+ VELIKA-'finis-pro-anno-1878'-sredina-strani = 2.-instance-zaključne-oznake-cf.-P243-s38!-Krugel-s26-NI-tail-1878-ampak-vpis-3!) · meja-1879/80 = s35-mid (33→restart-1–2-P243-1:1!) — GLAVA-'1879'-PONOVLJENA-NA-VSAKEM-RAZPRTEM-LISTU-s27–s34 (mrliški-vzorec-mej-60.–74.-POTRDILO-ČEZ-KNJIGE!) = NOVA-8.-MEJNA-VARIANTA-vendar-PONOVITEV-ne-restart-marker (P244-napaka-popravljena!)",
  boundaryEn:
    "the-1878/79-boundary = s25→s26 (P245-CORRECTION!-the-1878-tail = s25: margin-22–23-+-the-BIG-'finis-pro-anno-1878'-mid-page = the-2nd-instance-of-the-year-end-marker-cf.-P243-s38!-Krugel-on-s26-is-NOT-the-tail-but-entry-3!) · the-1879/80-boundary = s35-mid (P243-1:1!) — the-'1879'-heading-REPEATED-ON-EVERY-SPREAD-s27–s34 (the-death-register-boundary-pattern-CONFIRMED-ACROSS-BOOKS!) = the-NEW-8th-MEJNA-VARIANT-but-a-REPETITION-not-a-restart-marker (the-P244-error-corrected!)",
} as const;

/** Številčenje strani 1879 (P245-KOREKCIJA! s26 = 1–3 · s27 = 4–5 · s28 = 6–8 · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33) — 33-VPISOV-BREZ-PRESKOKOV (5.-leto-BREZ-kontrast-1881!-vsota-33-NESPREMENJENA!). */
export const MARRIAGE_1879_NUMBERING =
  "s26 = 1–3 (P245-KOREKCIJA-restart!-margini-1/2/3!) · s27 = 4–5 (margini-4/5!-Klepec-je-v4!) · s28 = 6–8 (3-vrstice!-6-jasna-+ 7-poškodovana-trganje-papirja-aritmetično-6-[7]-8-+ 8-jasna!-v6-Wingler-NE-Griblje-v7-Pezdirc-50-v8-Kunič[~]) · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33-tail (P243!)";

/** ★★★★★ FOLIACIJA-1879-'Pag = sken−1'-5/5 (s26-'Pag. 25' + s27-'Pag. 26' + s30-'Pag. 29' + s34-'Pag. 33' + s35-'Pag. 34'!-vsi-ultra-zoom-1:1!-s26-P245-KOREKCIJA-nova!) → P243-s38-'Pag. 34.'-X-OPEN-DUEL-REŠEN: pravilo-Pag==sken−1-OSTAJA (s38-branje-'34'-= MISREAD-'37'-0-vs-7-Kurrent-cf.-P162b!) — s31-'Pag. 36.'-[~MISREAD-'30'-0-vs-6-DUEL-podporjen!]. */
export const FOLIACIJA_1879_REŠITEV =
  "s26-'Pag. 25'-1:1-+ s27-'Pag. 26'-1:1-+ s30-'Pag. 29'-1:1-+ s34-'Pag. 33'-1:1-+ s35-'Pag. 34'-1:1 = 5/5-1879!-→ P243-X-OPEN-DUEL-REŠEN (s38-'Pag. 34.'-branje = MISREAD-'Pag. 37'!-pravilo-Pag==sken−1-NE-PRELAMA!-cf.-P162b-7-vs-4-Kurrent-zmeda-zdaj-tudi-0-vs-7-+ 0-vs-6!)";

/** ★★★ h50-PT-luknja-hiša-1.-poročni-dokaz-v-predzgodovini + h16-×2-BLOKA-V-1-LETU (2.×-linije-cf.-P242-h27!) + h63-KRIŽAN-2.-leto-ZAPORED (1879-nevesta-→-1880-ženin!-NIT-5-LET-z-mrliško-1884!) + PEZDIRC-×2-ženinov-v-1-letu (v5-Mathias-h50-+ v21-Georg-h42-[~Pegdirc!]-+ v16-priča-'Pezdire'-[~!] = 7.-leto-continuum!) + BRINC-5.-leto (v12-mati-v12-×-P243-v4-ženi n-h24-ZAPORED!) + ŠILAR-vdova (v9-verw.-Schilar!) + TOMC-×3-TRIPLET (v9-Georg + v20-Martin + v25-Matthius!) + Kralj-h17-cf.-P151-1922 (ISTO-DRUŽINA: Johann-1879 → Jurij-1922!). */
export const H50_1879_PT_LUKNJA =
  "P245-KOREKCIJA: vpis-7-Mathias-Pezdirc-GRIBLJE-50-×-Maria-Škuncelj-44-5.-Februar-1879 (NE-vpis-5!-margina-fizično-poškodovana-trganje-papirja-aritmetično-vsiljena-6-[7]-8!) = h50-1.-POROČNI-DOKAZ-V-PREDZGODOVINI (PT-luknja-hiša-P191-dokazana-mrliško!-poročna-predzgodovina-zdaj-tudi-h50!-cf.-h24-P243-v4-→-h50-cf.-1896-P125-linija!)";

export const H16_1879_DVOJNA =
  "h16 = ×2-BLOKA-V-1879 (P245-KOREKCIJA: v4-ženin-Georg-Klepec-[~TRIPLE-DUEL!]-29.-Jänner-NE-vpis-1!-restart-je-v1-Fritz-s26!-+ v25-ženin-Matthius-Tomc-4.-Mai!) = 2.×-linije-DA-ISTO-LETO-×2-BLOKA (cf.-P242-h27-×2-bloka-v-1881!-P243-h27-×2!-vzorec-DRUŽINSKIH-VEJ!)";

export const KRIZAN_1879_NIT =
  "v21-Georg-Pegdirec-[~Pezdirc!]-GRIBLJE-42-×-Dorothea-Hrizan-[~Križan!]-GRIBLJE-63-19.[~Feber?]-1879 (ultra-zoom-1:1-CLEARED!) = h63-KRIŽAN-2.-LETO-ZAPORED (1879-nevesta-→-1880-ženin-Križan-Miklavčič-P243-v14!-NIT-5-LET: 1879→1884-mrliška-×2-P239!) + margine-'Gesuchs-1879-...der-Gemein[de]'-[~GAVELDZETTEL-cf.-X-OPEN!]";

export const PEZDIRC_1879_CONTINUUM =
  "PEZDIRC-CONTINUUM-×131→04455-v-7.-LETU-predzgodovine: P245-KOREKCIJA-v7-ženin-Mathias-Pezdirc-h50-1:1-krop! (NE-v5!)-+ v21-ženin-Georg-Pegdirc-[~DUEL-grafija!]-h42-ultra-zoom!-+ v16-priča-'Pezdire'-[~!] — 2-ŽENINOV-×-1-PRIČA-v-1-letu = NAJBOLJŠI-1879-PODATKEK!";

export const BRINC_1879_NIT =
  "v12-Johann-Požeh-GRIBLJE-21-×-Maria-Brinc-[~Brüne/Princ-DUEL!]-GRIBLJE-24-12.-Feber-1879 = h24-2.-LETO-ZAPORED (1879-nevesta-→-1880-ženin-Mathias-BRINE-P243-v4!) + BRINC/BRINEC-MREŽA-5.-leto (P238-BRUNC-mati-+ P242-v13-Peter-BRINC-+ P243-v4-BRINE!) + DRAGOŠ-nit (mati-Maria-Dragos!) + h21-cf.-P151-1922-h21-Požek!";

export const DOVGAN_1879_PODALJŠITEV =
  "DOVGAN-CONTINUUM-PODALJŠAN-NA-7-LET (1879–1885!-P245-KOREKCIJA-se-širi-OD-PRVEGA-VPISA!): Franz-Dovgan-podpis-×3-NA-s26 (v1-2-3!-januar-1879!-+ Befunde-v3-'Franz-Dovgan')-+ s35-tail-D-podpis-'Copulatus-sum-Griblje-d.-14/9-1879.-Dopgan'-1:1!-+ v16-duhovnik-'Franc-[~Pasthic/Dovgan-DUEL!]'-+ s27-v4-modri-pripis-'Anton-Franz-von-Dovgan-Dechant'-omenjen-[~X-OPEN-kaj-točno!]";

export const MILEK_1879_KRIZ =
  "MILEK-križ-kandidat-IZVEN-korpusa (pošteno!): s35-tail-D-starš-'½-Gübl.-Mileh'-[~MILEH-1-branje!]-v-vpisu-31-Jožef-Požeh[?]-[~Griblje-77?] = križ-×237→×238-[~]-cf.-P240-Milleh-3-branja-+ P239-v18-mati-MILEK-+ P242-NI-+ P243-NI!-iskreno-odprto-X-OPEN";

/** Datum-dueli 1879 (P245-KOREKCIJA: Klepec-je-v4!-v1-Fritz-1.-Jänner-BREZ-duela!-+ v15/v16/v17-'19.'-3-poroke-isti-dan-kandidat-[~X-OPEN!]-+ v24-'23-vs-24'-Feb-[~]-+ v20/v21-'19.'-[~]). */
export const MARRIAGE_1879_DUELS = [
  "P245-KOREKCIJA-v4-datum »29. Jänner vs 29. März« 2:1-za-Jänner [~] (pass-1+2+3-Jänner!-pass-4-'März'-'Jänner'-oboje-v-branju!-NE-vpis-1!-v1-Fritz-1.-Jänner-brez-duela!)",
  "v15+v16+v17-datum »19.«-3-poroke-isti-dan-kandidat [~X-OPEN] (cf.-P240-v5+v6-ISTA-DAN-+ P241-v6/v7-IZMENA!)",
  "v24-datum »23. vs 24. Februar« [~X-OPEN] (pass-1-'23'-vs-pass-2-'24'!)",
  "v20+v21-datum »19.[~Feber?]« [~X-OPEN] (2-branja-'bruar-1879'!)",
] as const;

/** ★★★★★ P245-KOREKCIJA: P244-napaka-RAZKRITA-in-POPRAVLJENA — restart-1879 = s26 (ne s27!): 3-januarskih-vpisov-na-s26 (v1-Fritz-×-Blasnik!-v2-Krupljen!-v3-Krugel!-Krugel-NI-tail-1878!)-številčenje-v-LEVI-MARGINI (Lfd.-stolpec-ne-obstaja!)-Klepec-je-v4-Pezdirc-je-v7-vsota-33-NESESPEMLJENA! */
export const MARRIAGE_1879_KOREKCIJA = {
  razkritje:
    "RESTART-1879 = s26 (ne s27!): 3-vpisa-januarja-1879-na-s26 (v1-Wilhelm-Fritz-LOKA-1-×-Anna-Blasnik-CERNO-38 · v2-Anton-Krupljen-CERNO-· v3-Georg-Krugel-DOBRANIČ-18-×-Katharina-Klobučar[~])-številčenje-v-levi-margini-1–3",
  vzrokNapake:
    "P244-pass-1-na-s26-vrnil-PRAZNO (vrstic=0-glave=[ni]!) → s26-obdelan-kot-'tail-kontekst'-brez-vpisov; s27-velika-glava-'1879'-napačno-tumačena-kot-restart-marker (glava-je-PONOVLJENA-na-vsakem-listu-P244-sama!); marginalne-številke-niso-bile-preverjene-fizično",
  dokazi: [
    "6-VLM-pregledov-živega-vira (margine-s25/s26/s27/s28 + s26-polna-stran + glava-stolpcev!)",
    "ultra-zoom: s26-'1'-cvak + s28-'6'-jasno + s28-'8'-jasno + s28-'7'-trganje-papirja-aritmetika-6-[7]-8",
    "s25-margina-22/23-+-velika-opomba-'finis-pro-anno-1878'",
    "foliacija-s26-'Pag. 25.'-1:1-→-pravilo-Pag==sken−1-5/5",
    "duhovnik-Franz-DOVGAN-×3-podpisa-na-s26 (v1–v3!)",
  ],
  nespremenjeno: [
    "33-vpisov-skupaj-BREZ-preskokov-5.-leto!",
    "9-Griblje-blokov-h16-h50-h61-h21-h32-h13-h42-h17-h16",
    "korpus-235-04455-·-1978-vitalov-·-228-sidra-·-202-dobe",
    "v9–v33-vse-vpisne-številke",
    "meja-1879/80-s35-mid-P243",
  ],
} as const;

/** ★★★ ŠTEVILČENJE-v-LEVI-MARGINI (nov-element-table-formata!): natisnjen-Lfd.-stolpec-NE-OBSTAJA ('Haus-Nr.'-je-med-Wohnort-in-imenom!) — letne-zaporedne-številke-pisane-v-levi-margini-modro-sivim-črnilom (s26-1/2/3 + s27-4/5 + s28-6/[7]/8 + s25-1878-22/23!) — pričakovano-tudi-za-ostala-leta-predzgodovine (kontrola-pri-P246!). */
export const MARGINA_1879_STEVILCENJE =
  "natisnjen-Lfd.-stolpec-ne-obstaja ('Haus-Nr.'-med-Wohnort-in-Tauname!)-letne-številke-v-LEVI-MARGINI-modro-sivo (1–3-s26-+ 4–5-s27-+ 6–8-s28-+ 22–23-s25!) — s28-'7'-fizično-poškodovana-trganje-papirja-aritmetično-vsiljena-6-[7]-8!";

/** ★★★ FINIS-PRO-ANNO-1878 = s25 (2.-instance-zaključne-oznake-leta-v-poročni-predzgovorini!-cf.-P243-s38-'finis-/-s-1880'-1.-ODKRITA!-vzorec-se-ponavlja-čez-leta!). */
export const FINIS_1878_S25 =
  "s25-sredina-strani-POD-vrstama-22–23: velika-rokopisna-opomba-'finis-pro-anno-1878' = zaključna-oznaka-leta-2.-instance (P243-'1.-ta-vrsta'-drži-kot-1.-ODKRITA-ampak-s25-zgodnejša-v-knjigi!)-meja-1878/79-=-s25→s26!";

/** ★★ KONTEKST-vpis-1–5-1879-NI-bloki-pošteno (izven-Griblje!): v1-Fritz-LOKA-1 + v2-Krupljen-CERNO + v3-Krugel-DOBRANIČ-18 + v5-Štefanik[~]-DOBRANE-8. */
export const MARRIAGE_1879_KONTEKST = [
  "v1-1.-Jänner-Wilhelm-Fritz-[~frih/Kritz!]-Ökonom-Wolfsberg-41-Kärnthen-stanuje-LOKA-1-34-l-×-Anna-Blasnik-[~Blahnik!]-Cerno-38-43-l-gostilničarjeva-hči-NI-blok (izven-Griblje!)",
  "v2-12.-Jänner-Anton-Krupljen-[~Krystan/Pristan!]-k.k.-Postwärth-Cernomelj-37-l-×-Elisabeth-[~Rubin/Krslin!]-18-l-MLADOLETNICA-minderjährig-Einwilligung-starši-NI-blok",
  "v3-26.-Jänner-Georg-Krugel-[~Krigel/Krügel!]-½-Gübler-DOBRANIČ-18-63-l-×-Katharina-geb.-Klobučar-[~Hrab/Klepec-DUEL-verw.!]-Boršt-22-44-l-VDOVA-NI-blok (½-Gübler-STATUS-ni-hiša-Griblje!)-P244-ga-je-štel-kot-'tail-1878'-NAPAČNO!",
  "v5-2.[~10.?]-Februar-Georg-Štefanik[~]-½-Gübler-DOBRANE-8-NI-blok-[~X-OPEN-datum-duel!]",
] as const;

/** Vse-nove-1879-meritve-v-obliki-za-QA (skupaj-04455: 226→235 · vitals: 1969→1978 · sidra: 219→228-1879:9! · dobe: 193→202-32-pred-linijskih!). */
export const MARRIAGE_1879_KORPUS = {
  skupaj04455: 235,
  skupajVitals: 1978,
  sidra: 228,
  dobe: 202,
} as const;

/** ——— P246: poročna predzgovorina 04455, leto 1878 = 8/13 (s19–s24; RESTART = s19-TOP-marginal-'1'-fizično!-GLAVA-'1878'-NI-ponovljena-kontrast-1879!-FOLIACIJA-6/6!) — 23 VPISOV-BREZ-PRESKOKOV · 7-GRIBLJE-blokov (×3-INTRA-DVOJNI!) ——— */
export const MARRIAGE_1878_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1878,
);
export const MARRIAGE_1878_GRIBLJE = MARRIAGE_1878_BLOCKS.length;
export const MARRIAGE_1878_HOUSES = MARRIAGE_1878_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1878_TOTAL = 23;

/** Meje 1878: RESTART-s19-top (marginal-'1'-fizično-1:1!-vpis-1 = Jänner-'1878-Jänner-16[~24]-DUEL'-Šelah-[~MULTI-DUEL!]-Gremelj[~]-20-'&-Güblam'-×-Jureješič-Primez-11-DISPENS!) + MEJA-1877/78 = s18→s19 (tail-1877 = s18-margine-14–17-NOVEMBER!) + MEJA-1878/79 = s25→s26 (P245-1:1!-'finis-pro-anno-1878'-s25-2.-instance!) + GLAVA-'1878'-NI-PONOVLJENA (KONTRAST-1879!-letnica-INLINE-v-1.-vpisu-vsakega-lista!-9.-MEJNA-VARIANTA!). */
export const MARRIAGE_1878_MEJA = {
  restartSi:
    "restart-vpis-1 = Jänner 1878 = s19-TOP (marginalna-'1'-FIZIČNO-1:1-Read-očesa-P244-LEKCIJA-upoštevana!-velika-letnica-NI-posebna-glava-letnica-samo-INLINE-v-datumu!) — ženin-Johann-Šelah-[~Filak/Hilač/Kelchler-MULTI-DUEL-5-branj!]-'&-Güblam'-(½-Gübler-stand!)-Gremelj-[~Kremel/Kriblje-DUEL-3-branj!]-20-[~2a/24-DUEL!]-32-l-×-Anna-Jureješič-[~Perzta-DUEL!]-Primez-[~Drima-DUEL!]-11-[~]-26-l-+ Befunde-DISPENS-super-mixta-ac-prima-(consistoriale-dioecesane!-cf.-P244-v1-'Civil-Beizag'-VZOREC!)+ Franz-DOVGAN-podpis!",
  restartEn:
    "restart-entry-1 = January 1878 = s19-TOP (the-margin-'1'-PHYSICALLY-1:1-the-P244-lesson-applied!-no-separate-big-year-heading-the-year-INLINE-in-entry-1's-date!) — groom-Johann-Šelah-[~MULTI-DUEL!]-'&-Güblam'-(½-Gübler-stand!)-Gremelj-[~DUEL!]-20-[~]-32-y-×-Anna-Jureješič-[~DUEL!]-Primez-[~DUEL!]-11-[~]-26-y-+ the-Befunde-DISPENS-super-mixta-ac-prima-(cf.-P244-v1-'Civil-Beizag'-PATTERN!)+ Franz-DOVGAN-signature!",
  tailSi:
    "tail-vpis-23 = [Nov?-P245!] 1878 (s25-margina-22–23-P245-1:1!) — 22-=-1878-Okt.-[24~27-DUEL!]-Martin-[~]-Mrivo-glavre-38-+ 23-=-Novem.-10.-Mathias-[~]-Gornji-Dovc.-67-+ VELIKA-'finis-pro-anno-1878'-sredina-strani = 2.-instance-zaključne-oznake-P245!",
  tailEn:
    "tail-entry-23 = [Nov?-P245!] 1878 (s25-margin-22–23-P245-1:1!) — 22-=-Oct-1878-Martin-[~]-×-[~]-+ 23-=-Nov-10-Mathias-[~]-+ the-BIG-'finis-pro-anno-1878'-mid-page = the-2nd-instance-of-the-year-end-marker-P245!",
  boundarySi:
    "meja-1877/78 = s18→s19 (tail-1877 = s18: margine-14[~74]-15-16[~76]-17-NOVEMBER-1877-vsi!-'Pag. 17'-prečrtani-popravki-številk!) · meja-1878/79 = s25→s26 (P245-1:1!) — GLAVA-'1878'-NI-PONOVLJENA-NA-LISTIH (kontrast-1879-kjer-'1879'-ponovljena-s27–s34!-letnica-samo-INLINE-v-1.-vpisu-vsakega-lista-s19–s24!) = 9.-MEJNA-VARIANTA (ponavljanje-glave-je-LETO-specifično-ne-knjižno!)",
  boundaryEn:
    "the-1877/78-boundary = s18→s19 (the-1877-tail = s18: margins-14–17-NOVEMBER-1877!-'Pag. 17'!) · the-1878/79-boundary = s25→s26 (P245-1:1!) — the-'1878'-heading-NOT-REPEATED-on-the-leaves (in-contrast-to-1879-where-'1879'-repeats-s27–s34!-the-year-only-INLINE-in-each-leaf's-1st-entry!) = the-9th-BOUNDARY-VARIANT (heading-repetition-is-YEAR-specific-not-book-wide!)",
} as const;

/** Številčenje strani 1878 (s19 = 1–3 · s20 = 4–7 · s21 = 8–11 · s22 = 12–14 · s23 = 15–17 · s24 = 18–21 · s25-22–23-P245!) — 23-VPISOV-BREZ-PRESKOKOV (6.-leto!-ŠTEVILČENJE-v-LEVI-MARGINI-POTRJENO-2.-LETO!-margine-fizično-Read-očesa-1:1-×6-strani!). */
export const MARRIAGE_1878_NUMBERING =
  "s19 = 1–3 (margine-1/2/3-fizično!) · s20 = 4–7 (4/5/6/7!) · s21 = 8–11 (8/9/10/11!-m9-Wohnort-prečrti!) · s22 = 12–14 (12/13/14!) · s23 = 15–17 (15/16/17!) · s24 = 18–21 (18/19/20/21!) · s25 = 22–23-tail (P245-1:1!) — 23-VPISOV-BREZ-PRESKOKOV-6.-leto!";

/** ★★★★★ FOLIACIJA-1878-'Pag = sken−1'-6/6 (s19-'Pag. 18' + s20-'Pag. 19' + s21-'Pag. 20' + s22-'Pag. 21' + s23-'Pag. 22' + s24-'Pag. 23'!-2-VLM-pass-1-misreadi-KOREKCIJA-s21-'21'-→-'20' + s24-'25'-→-'23'-10×-Read-očesa!) — skupaj-z-5/5-1879 = 11/11-V-ZAPOREDNIH-LETIH-pravilo-NE-PRELAMA! */
export const FOLIACIJA_1878 =
  "s19-'Pag. 18'-1:1-+ s20-'Pag. 19'-1:1-+ s21-'Pag. 20'-1:1 (10×!-VLM-misread-'21'-KOREKCIJA!)-+ s22-'Pag. 21'-1:1-+ s23-'Pag. 22'-1:1-+ s24-'Pag. 23'-1:1 (10×!-VLM-misread-'25'-KOREKCIJA!) = 6/6-1878!-→ skupaj-z-5/5-1879 = 11/11-v-zaporednih-letih (pravilo-Pag==sken−1-NE-PRELAMA!)";

/** ★★★ GLAVA-'1878'-NI-PONOVLJENA-NA-LISTIH (9.-MEJNA-VARIANTA-kontrast-1879!): letnica-samo-INLINE-v-datumu-1.-vpisa-vsakega-lista (s19-r1-'1878-Jänner-16'-+ s20-r4-'1878-Febr-20'-+ s21-r8-'1878-Februar-24'-+ s22-r12-'1878-Februar-27'-+ s23-r15-'1878-Mai-26[~Juni-DUEL!]'-+ s24-r18-'1878-Juni-23')-nadaljnji-vpisi-samo-mesec+dan (s20-'20.'×3-+ s22-'März-3'-'Mai-12'!). */
export const GLAVA_1878_NI =
  "velika-glava-'1878'-NE-OBSTAJA-na-nobenem-listu-s19–s24 (kontrast-1879-kjer-velika-glava-'1879'-ponovljena-s27–s34-P244/245!)-letnica-samo-INLINE-v-datumu-1.-vpisa-vsakega-lista-+ nadaljnji-vpisi-samo-mesec+dan = ponavljanje-glave-je-LETO-specifično-ne-knjižno-vzorec (9.-MEJNA-VARIANTA!)";

/** ★★★ HRIŽAN-×3-BLOKI-V-1-LETU (h63-v6-+ h35-v17-+ h36-v21!-H-forma-10×-na-vseh-treh!-h35-HRIŽAN-1:1-P229-z79!-h36-Križan-družina-P80!-h63-hišna-nit-3.-leto-1878→1880!) + INTRA-DVOJNI-BLOKI-×3 (h47×h43-v5-+ h18×h65-v7-+ h1×h35-v17!) + MILEK-h65-1.-poročni-dokaz + ŠIMEC-h18-1.-poročni-dokaz + h47-NOVA-hiša + h23-1.-poročni-dokaz + h1-KELCHO-continuum-P231! */
export const HRIZAN_1878_TROJNA =
  "HRIŽAN-×3-BLOKI-V-1-LETU-1878 (REKORD-POROČNE-PREDZGOVINE!): v6-nevesta-Anna-Hrižan-[~Križan!]-GRIBLJE-63 (10×-'63'!)-+ v17-nevesta-Maria-Hrižan-[~Križan!]-GRIBLJE-35 (10×-'35'!-cf.-P229-z79-'Mathias-Hrižan-[~HRIŽAN!]'-h35-ISTO-DRUŽINA!)-+ v21-nevesta-Maria-Hrižan-[~Križan!]-GRIBLJE-36 (10×-'36'!-cf.-P80-h36-Križan-1882-poroka!) = 3-neveste-iz-3-hiš-v-1-letu (H-forma-10×-na-vseh-treh!-Križan-DUEL-pošteno-2-od-3!-h63-hišna-nit-3.-LETO-ZAPORED-1878-Anna→1879-Dorothea→1880-Križan!)";

export const MILEK_1878_H65 =
  "v7-nevesta-Anna-MILEK-GRIBLJE-65 (10×-'65'-1:1!-NE-63/68!) = h65-MILEK-družina-1.-POROČNI-DOKAZ (cf.-P218/P220-h65-MILEK-oče-krstna!-+ P224-z55-h65!-+ P239-v18-mati-MILEK-mrliška!-MILEK-ZDAJ-V-VSEH-4-KNJIGAH!-×4-vir-križ!)-+ ženin-Georg-ŠIMEC-h18 (10×-'18'!-cf.-P232-z21-h18-SIMEC-oče!-ŠIMEC-1.-poročni-dokaz!)-INTRA-DVOJNI-blok!";

export const PEZDIRC_1878_KONTEKST =
  "PEZDIRC-CONTINUUM-×131→04455-v-8.-LETU-predzgodovine-NI-bloki-pošteno (IZVEN-Griblje!): v10-ženin-Johann-Pegdiric-[~Pezdirc!]-Krasinec-2-37-l-×-Katharina-Beličič-[~Deličič-DUEL!]-Črnomelj-152-+ v20-ženin-Johann-Pegdič-[~Pejdič!]-Lahine-10-28-l-×-Katharina-Buthovec-[~Buchovec!]-Cerhovje-27 = 2-PEZDIRC-GARBLE-v-1-letu (cf.-grafija-continuum-8-let-P228-×17-REKORD!)";

export const DOVGAN_1878_PODALJŠITEV =
  "DOVGAN-CONTINUUM-PODALJŠAN-NA-8-LET (1878–1885!): Franz-Dovgan-podpisi-na-VSIH-6-glavnih-listih-s19–s24 (od-vpisa-1-restart!-garble-grafije-'Dorgan/Dolgan/Dorejan/Dorezan'-po-listih!-cf.-DOVGAN_1879_PODALJŠITEV-7-let-→-ZDAJ-8!)";

/** Datum-dueli 1878 (v1-'16-vs-24'-Jän!-v2-'30.-Jän-vs-Feber-25'-celica!-v11-'27.-mesec'!-v15-'Mai-vs-Juni-26'!-v21-'23.-Aug-vs-Nov'!-v20-'10.-9'tbr'!). */
export const MARRIAGE_1878_DUELS = [
  "v1-datum »Jänner 16 vs 24« 2:1-za-16 [~] (Read-očesa-'16'-+ pass-1-'16'!-pass-3-'24'-1-branje!)",
  "v2-datum »30.-[Jän?]...25«-celica-DUEL [~X-OPEN] (krop-'30.'-+ 'Gezm/Feber-25'-2-vrstici!)",
  "v11-mesec »Feber? vs März vs Jänner« [~X-OPEN] (pass-1-'März'-pass-3-'Jänner'-sestava-za-Feber!)",
  "v15-mesec »Mai vs Juni 26« [~X-OPEN] (pass-1-'Mai'-margin-krop-'Mai/Juni'!)",
  "v21-mesec »23. Aug vs Nov« [~X-OPEN] (pass-1-'Aug?'-Read-'Nov?'-X-OPEN!)",
  "v20-datum »10. 9'tbr« = 10.-OKTOBER-okrajšava-1:1 (margin-'9'ti-Mhbzy'-cf.-OKT!)",
] as const;

/** ★★ KONTEKST-izven-Griblje-1878-NI-bloki-pošteno: v1-Šelah-Gremelj[~]-20-DISPENS-+ v2-Šelah[~]-×-Bulhovec[~]-18-+ v3-Horvatini[~]-Hrova-sinc-38-×-Mušič-17-+ v8-Kompare-Melično[~]-35-×-Perleie[~]-Gradec-4-+ v9-Hure-vid.-Germ[~]-29-×-Hrižan-Krašhar[~]-29-+ v12-Jablenik-Krasinec-13/37-+ v13-Mavrecic-Štaple-5-×-Bahorič-Krasinec[~]-44-+ v14-Simonič-×-Judnič-Dobravce-10-+ v15-Murko-Gremelj[~]-24-×-Vidic-vdova-Prilozje-45-+ v16-Šlepec-Krasinec-36-×-Tome-Primez-19-16-l-MLADOLETNICA-+ v18-Janšov[~Rabnov!]-Krasinec-30-×-Novak-Gradec-15-+ v19-Hovarič-Gradac-39[~32!]-×-Jureješič-Boršt-O. */
export const MARRIAGE_1878_KONTEKST = [
  "v1-Jänner-1878-Johann-Šelah-[~MULTI-DUEL!]-'&-Güblam'-Gremelj[~]-20-DISPENS-super-mixta-×-Anna-Jureješič-Primez-11-NI-blok (izven-Griblje!)",
  "v2-Johann-Šelah[~]-'&-Gübl'-×-Maria-Bulhovec-[~Butarová/Dulavec-DUEL!]-18-NI-blok",
  "v3-Februar-Mathias-Horvatini-[~Hovath!]-Müllner-Hrova-sinc-38-×-Katharina-Mušič-17-NI-blok",
  "v8-Februar-Josef-Kompare-Bauer-Melično[~]-35-×-Anna-Perleie[~]-Gradec-4-NI-blok",
  "v9-Mathias-Hure-[~Kure!]-vid.[VDOVEC!]-28-'Germ'[~]-29-×-Katharina-Hrižan-[~Križan!]-23-Krašhar[~]-29-prečrti-NI-blok",
  "v12-Februar-Nikolaus-Jablenik-[~!]-½-Gübl-Krasinec-13-×-Anna-Šlepec-[~Hlepec!]-Krasinec-37-NI-blok",
  "v13-März-Mathias-Mavrecic-[~Mavrenk!]-½-gütl-Sohn-Štaple-5-×-Maria-geb.-Bahorič-Krasinec[~]-44-NI-blok",
  "v14-Mai-Johann-Simonič-Gärtner-×-Maria-Judnič-[~!]-Dobravce-10-NI-blok (JUDNIČ-cf.-P244-v33-tail!)",
  "v15-Mai[~Juni-DUEL!]-Markus-Mur.-[~Murko!]-Gremelj[~]-24-×-Anna-Vidic-[~]-vdova-Prilozje-45-NI-blok",
  "v16-Nikol.-Šlepec-Krasinec-36-×-Barbara-Tome-[~]-Primez-19-16-l-MLADOLETNICA-NI-blok",
  "v18-Juni-Johann-Janšov-[~Rabnov-DUEL!]-Krasinec-30-×-Maria-Novak-geb.-Mavrenk-Gradec-15-NI-blok",
  "v19-Sept-Mathias-Hovarič-Gradac-39[~32-DUEL!]-×-Katharina-Jureješič-Boršt-O.-34-NI-blok",
  "v20-10.-Okt-Johann-Pegdič-[~PEZDIRC!]-Lahine-10-×-Katharina-Buthovec-Cerhovje-27-NI-blok",
] as const;

/** Vse-nove-1878-meritve-v-obliki-za-QA (skupaj-04455: 235→242 · vitals: 1978→1985 · sidra: 228→235-1878:7! · dobe: 202→209-39-pred-linijskih!). */
export const MARRIAGE_1878_KORPUS = {
  skupaj04455: 242,
  skupajVitals: 1985,
  sidra: 235,
  dobe: 209,
} as const;

/** ——— P247: poročna predzgovorina 04455, leto 1877 = 9/13 (s15–s18; RESTART = s15-TOP-marginal-'1'-fizično!-GLAVA-INLINE-kot-1878-POTRJENO-2.-LETO!-FOLIACIJA-4/4-15/15!) — 18 VPISOV-BREZ-PRESKOKOV · 5-GRIBLJE-blokov (h51-×2!) ——— */
export const MARRIAGE_1877_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1877,
);
export const MARRIAGE_1877_GRIBLJE = MARRIAGE_1877_BLOCKS.length;
export const MARRIAGE_1877_HOUSES = MARRIAGE_1877_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1877_TOTAL = 18;

/** Meje 1877: RESTART-s15-TOP (marginal-'1'-fizično!-vpis-1 = '1877-Jänner-14'-INLINE-Levstih-×-Grubanič-GRIBLJE-10!) + MEJA-1876/77 = s14→s15 (finis-1876-3.-instance!-Pegdire-GRIBLJE-30-1876!) + MEJA-1877/78 = s18→s19 (P246-1:1!) + GLAVA-'1877'-NI-PONOVLJENA (=1878!-9.-MEJNA-VARIANTA-POTRJENA-V-2.-LETU!). */
export const MARRIAGE_1877_MEJA = {
  restartSi:
    "restart-vpis-1 = 14. Jänner 1877 = s15-TOP (marginalna-'1'-FIZIČNO-1:1-Read-očesa-P244-LEKCIJA!-velika-letnica-NI-posebna-glava-letnica-INLINE-v-datumu!) — ženin-Georg-Levstih-[~Levstik/Lovišič-DUEL-3-branj!]-29-[~24-DUEL!]-Bauer-'Vranu-vice'[~X-OPEN!]-20-×-nevesta-Cäcilie-Grubanič-[~Kukamič/Kukhanic-DUEL!]-GRIBLJE-10-40-[~16-pass-1-DUEL-KOREKCIJA!]-NEVESTA-BLOK-h10!-+ Franz-DOVGAN-podpis!",
  restartEn:
    "restart-entry-1 = Jan 14, 1877 = s15-TOP (the-margin-'1'-PHYSICALLY-1:1!-no-separate-big-year-heading-the-year-INLINE!) — groom-Georg-Levstih-[~3-way-DUEL!]-×-bride-Cäcilie-Grubanič-[~DUEL!]-GRIBLJE-10-BRIDE-BLOCK-h10!-+ Franz-DOVGAN-signature!",
  tailSi:
    "tail-vpisi-15–18 = s18 (NOVEMBER/DECEMBER-1877!): 15-=-Novb.-14-Dobravice-14-Hrusovec-×-Košuva-2-· 16-=-28.-December-IZVEN-KRONOLOGIJE-Terdić-×-GRIBLJE-69-Allešič-BRINC-opomba!-· 17-=-Nov-21-'Kblo.-šter.-36'[~KLOŠTER!]-Pluh-×-Dobravce-11-· 18-=-Nov-25-Cerki-31[~X]-Stubler-×-Primostek-2-Stubler!",
  tailEn:
    "tail-entries-15–18 = s18 (NOV/DEC-1877!): 15-=-Novb.-14-· 16-=-Dec-28-OUT-OF-CHRONOLOGY-Terdić-×-GRIBLJE-69-BRINC-annotation!-· 17-=-Nov-21-'Klo-šter'-36[~]-Pluh-· 18-=-Nov-25-Stubler-×-Stubler!",
  boundarySi:
    "meja-1876/77 = s14→s15 (tail-1876 = s14: margine-14–15-NOVEMBER-1876-+ VELIKA-'f i n i s / 1 8 7 6'-sredina-strani = 3.-instance-zaključne-oznake-leta-cf.-P243-s38-1.-+ P245-s25-2.!-vzorec-SODA-leta-1876/1878/1880!-m14-nevesta-Anna-Pegdire-[~PEZDIRC!]-GRIBLJE-30-kontekst!) · meja-1877/78 = s18→s19 (P246-1:1!) — GLAVA-'1877'-NI-PONOVLJENA-NA-LISTIH (=1878!-9.-MEJNA-VARIANTA-POTRJENA-V-2.-LETU!)",
  boundaryEn:
    "the-1876/77-boundary = s14→s15 (the-1876-tail = s14: margins-14–15-+ the-BIG-'finis-1876'-mid-page = the-3rd-instance-of-the-year-end-marker!-EVEN-years-only-so-far-1876/1878/1880!) · the-1877/78-boundary = s18→s19 (P246-1:1!) — the-'1877'-heading-NOT-REPEATED (=1878!-the-9th-BOUNDARY-VARIANT-CONFIRMED-IN-THE-2nd-YEAR!)",
} as const;

/** Številčenje strani 1877 (s15 = 1–5 · s16 = 6–9 · s17 = 10–14 · s18 = 15–18-po-popravkih!) — 18-VPISOV-BREZ-PRESKOKOV + ★★★ RE-NUMBERING-s18-+1-×4-PREČRTANIH (NOVA-tipa-'sistematični-popravek-+1'!). */
export const MARRIAGE_1877_NUMBERING =
  "s15 = 1–5 (margine-1/2/3/4/5-fizično!) · s16 = 6–9 (6/7/8/9!) · s17 = 10–14 (10/11/12/13/14!) · s18 = 14/15/16/17-VSE-PREČRTANE-→-15/16/17/18-po-popravkih (modro-sivo!-dup-'14'-s17/s18-razlog!-VLM-pass-2-+ očesa-1:1!) — 18-VPISOV-BREZ-PRESKOKOV-+ RE-NUMBERING-s18-+1-×4 (NOVA-numbering-anomalija-cf.-P245-s28-'6-[7]-8'-aritmetična!)";

/** ★★★★★ FOLIACIJA-1877-'Pag = sken−1'-4/4 (s15-'Pag. 14' + s16-'Pag. 15' + s17-'Pag. 16' + s18-'Pag. 17' + s14-'Pag. 13'-kontekst!) — skupaj-z-11/11-(1878+1879) = 15/15-V-ZAPOREDNIH-LETIH! */
export const FOLIACIJA_1877 =
  "s15-'Pag. 14'-1:1-+ s16-'Pag. 15'-1:1-+ s17-'Pag. 16'-1:1-+ s18-'Pag. 17'-1:1-+ s14-'Pag. 13'-kontekst-1:1 = 4/4-1877!-→ skupaj-z-6/6-1878-+ 5/5-1879 = 15/15-v-zaporednih-letih (pravilo-Pag==sken−1-NE-PRELAMA-4.-leto!)";

/** ★★★ GLAVA-INLINE-POTRJENA-2.-LETO (1877+1878!): velika-glava-NE-OBSTAJA-leta-1877-letnica-samo-INLINE-v-1.-vpisu-vsakega-lista (s15-r1-'1877-Jänner-14'-+ s16-r6-'1877-Februar-7[~6-DUEL]'-+ s17-r10-'1877-April-24[~29-DUEL]'-+ s18-r1-'1877-Novb.-14'-letterform-forenzika-N-dvojni-lok-vs-J-VLM-misread-'Jänner'-×2-KOREKCIJA!)-→ ponavljanje-velike-glave-je-LETO-specifično: 1877+1878-INLINE-vs-1879-ponovljena-vs-1880-restart-na-dnu! */
export const GLAVA_1877_INLINE =
  "velika-glava-'1877'-NE-OBSTAJA-na-s15–s18 (=1878-vzorec!)-letnica-samo-INLINE-v-datumu-1.-vpisa-vsakega-lista-+ nadaljnji-vpisi-samo-mesec+dan = 9.-MEJNA-VARIANTA-POTRJENA-V-2.-LETU-zapored (ponavljanje-glave-je-LETO-specifično-ne-knjižno!-1877+1878-vs-1879-vs-1880!)";

/** ★★★★★ MOH-TROJČEK-V-1-MESECU + MOH×BRODARIČ-DVOJNI-SORODSTVENI-ZAKON (1.×-ČEZ-DVE-DRUŽINI!): v4-Maria-Moh-h51-×-Gahofič-h8-+ v5-Mathias-Moh-h51-×-Maria-Brodarič-Krasinec-7-+ v7-Johann-Brodavič-Krasinec-7-×-Katharina-Moh-h51 = 3-SOROJENCI-MOH-iz-h51-v-3-tednih + 2-od-3-zakona-ČEZ-ISTA-DRUŽINA (brat+sestra-×-brat+sestra!-cf.-HROVALJ-brat+sestra-ISTI-DAN-P240!-h34-SILAH-sestrski-1884+1885!). */
export const MOH_1877_TROJCEK =
  "★★★★★ MOH-TROJČEK-V-1-MESECU-h51 (REKORD-TIPA!): v4-nevesta-Maria-Moh-GRIBLJE-51-[~31-DUEL!]-26-l-+ v5-ženin-Mathias-Moh-GRIBLJE-51-[~31-DUEL!]-29-l-+ v7-nevesta-Katharina-Moh-GRIBLJE-51-[~31-DUEL!]-16-l-MLADOLETNICA = 3-SOROJENCI-iz-iste-hiše-v-3-tednih-Januar/Februar-1877 (isti-glif-3×!-P2-VLM-'31'-vs-glif-forenzika-'51'-+ h51-1881-PARALELA!) + ★★★★★ MOH×BRODARIČ-DVOJNI-SORODSTVENI-ZAKON: v5-Mathias-MOH-h51-×-Maria-BRODARIČ-Krasinec-7-+ v7-Johann-BRODAVIČ-[~Brodarič!]-Krasinec-7-×-Katharina-MOH-h51 = brat+sestra-×-brat+sestra-ISTA-HIŠA-obeh-strani (1.×-ČEZ-DVE-DRUŽINI-v-predzgodovini!)";

/** ★★★★★ h51-PT-LUKNJA-HIŠA + h51-1877→1881-BRODARIČ-PARALELA: h51-1.-04455-BLOK-KADARKOLI (v5-ženin!-cf.-h50-P244!) — h51-1877-poroka-Mathias-MOH-×-Maria-BRODARIČ-→-h51-1881-krst-MATI-Maria-BRODARIČ (oče-'Matthias-Brodnik/BRINAR-garble-DUEL'-MATTHIAS-MATCH!) = 1:1-IME+HIŠA-PARALELA-4-leta-kasneje! */
export const H51_1877_PT_LUKNJA =
  "h51-1.-04455-BLOK-KADARKOLI (PT-LUKNJA-HIŠA-cf.-h50-P244-v7!): v5-ženin-Mathias-MOH-GRIBLJE-51-[~31-DUEL!] + v7-nevesta-Katharina-MOH-GRIBLJE-51 = h51-×2-BLOKA-V-1-LETU (2.×-linije-cf.-P244-h16-×2!-P242-h27-×2!) + ★★★★★ PARALELA: h51-1877-poroka-Mathias-MOH-×-Maria-BRODARIČ-→-h51-1881-krst-mati-Maria-BRODARIČ (oče-'Matthias-Brodnik/BRINAR-garble-DUEL'-MATTHIAS-MATCH-ženin-v5!-MOH-garble-kandidat-X-OPEN!) = 1:1-IME+HIŠA-PARALELA-4-leta-kasneje!";

/** firstYear-DVIG-×3-1877: h10-1887→1877-ZA-10-LET + h69-1887→1877-ZA-10-LET (PODVOJEN-10-LET-DVIG!) + h8-1881→1877-ZA-4-LET — cf.-h53-DVIG-1890→1880-ZA-10-LET-P243! */
export const FIRSTYEAR_1877_DVIG =
  "firstYear-04455-DVIG-×3-v-1-letu: h10-1887→1877-ZA-10-LET (v1-nevesta!-cf.-h53-DVIG-P243-1890→1880-tudi-ZA-10-LET!) + h69-1887→1877-ZA-10-LET (v16-nevesta!) = PODVOJEN-10-LET-DVIG-V-1-LETU-NOV-REKORD + h8-1881→1877-ZA-4-LET (v4-ženin-INTRA!) + h51-1.-BLOK-KADARKOLI";

export const BRINC_1877_OPOMBA =
  "BRINC-MREŽA-dokaz-v-1877: v16-nevesta-Katharina-Allešič-[~Ažetič!]-GRIBLJE-69-opomba-'vmožitva/Witwe-BRINC'-pod-priimkom = BRINC-družinska-vez-na-h69 (cf.-h24-1880-Mathias-BRINE-P243!-h21-1879-BRINC-P244!-P237-h65-BRINC-pred-doba!-BRINC-mreža-širša-čez-leta!)";

export const PEZDIRC_1877_KONTEKST =
  "PEZDIRC-CONTINUUM-×131→04455-v-9.-LETU-predzgodovine-NI-bloki-pošteno: v5-nevesta-'Prodaric'[~PEZDIRC-garble-kandidat!]-Krasinec-7-BRODARIČ-2:1-korpus-nit (h8-1873-mati-Anna-BRODARIČ-3/3!-h31-1879-mati-BRODARIČ!-h51-1881-mati-BRODARIČ!)-+ s14-KONTEKST-1876-m14-nevesta-Anna-'Pegdire'[~PEZDIRC!]-GRIBLJE-30 (cf.-P246-×2-garble-8.-leto!-grafija-continuum!)";

export const DOVGAN_1877_PODALJŠITEV =
  "DOVGAN-CONTINUUM-PODALJŠAN-NA-9-LET (1877–1885!): Franz-Dovgan-podpisi-na-VSIH-4-glavnih-listih-s15–s18 (od-vpisa-1-restart!-garble-'Dorgan'-pass-3-v5!-cf.-DOVGAN_1878_PODALJŠITEV-8-let-→-ZDAJ-9!)";

/** Datum-dueli 1877 (v1-'13-Jänner'!-v4/v5-'7-vs-4-Februar'!-v6-'6-vs-7'!-v10-'24-vs-29-April'!-v16-'Desembris-vs-Desinc'-garble!-v16-IZVEN-KRONOLOGIJE!). */
export const MARRIAGE_1877_DUELS = [
  "v10-datum »24 vs 29. April« [~X-OPEN] (pass-1-'24'-Read-očesa-'29'!)",
  "v4/v5-datum »7. vs 4. Februar« [~X-OPEN] (m3-'Februar-5'-vmes!-kronološko-vrstni-red-v4≥v5!)",
  "v6-datum »Februar 6 vs 7« [~X-OPEN] (pass-2-'Feber-6'-Read-'bruar-7'!)",
  "v16-datum »28. Desembris [~'Desinc'-garble]« + IZVEN-KRONOLOGIJE (po-vpisu-17-'21.-November'!-leta-NI-'d.-19-Jänner-1878'-pripis!)",
  "v2-starost »18 vs 32« [~X-OPEN] (pass-1-'18'-Read-'32'-+ vdošenka-opomba!)",
  "s18-r1-mesec »Novb. vs Jänner« REŠEN-2:1-za-NOVEMBER (letterform-forenzika-N-dvojni-lok!-VLM-misread-'Jänner'-pass-1-+ pass-2-KOREKCIJA-10×!)",
] as const;

/** ★★ KONTEKST-izven-Griblje-1877-NI-bloki-pošteno: v2-Kulišič-Bubnjar-sie?-33-×-Videbič-+ v3-Hocjan-Dra-sie-9-×-Nogrin-Dobravce-26-+ v6-Čupanič-Krasinec-16-×-Harasinič-Krasinec-24-+ v8-Škala-Godze-melj?-5-×-Perjan-Mokob-34-+ v9-Jakofčič[~]-×2-ISTA-PRIIMKA-hiši-[~X]!-+ v10-Zegennan-Grabrovec-19-×-Hrovač-Podgora-8-+ v11-Habič-Gorem-33-×-Hoharič-Boršt-18-+ v12-Mežnarič-Metlika-9-×-Kremer-Primostek-1-+ v13-Plut-'des-Pfarrers-v.-Črnomelj'-×-Guek-Kloster-27[~3]!-+ v14-Muec-Primostek-7-×-Križan!-+ v15-Hrusovec-Dobravice-14-×-Dubala-Košuva-2-+ v17-Pluh-Kloster-36[~]-×-Hugelč-Dobravce-11-+ v18-Stubler-Cerki-31[~X]-×-Stubler-Primostek-2. */
export const MARRIAGE_1877_KONTEKST = [
  "v2-30.-Jänner-Georg-Kulišič-[~Kulik-DUEL!]-Bubnjar-sie?-33-[~23-DUEL!]-×-Barbara-Videbič-Dvortan?-Krtičke?[~X]-18-[~32-DUEL!]-vdošenka?-opomba-NI-blok",
  "v3-5.-Februar-Mathias-Hocjan-[~Hrojan-DUEL!]-Dra.-sie?-9-[Drašiči?]-×-Katharina-Nogrin-[~Dagensin-DUEL!]-Dobravce-26-28-l-NI-blok",
  "v6-7[~6].-Februar-Johann-Čupanič-[~Trupanič/Županič-DUEL!-cf.-h31-1876-ŽUPANIČ!]-Krasinec-16-38-l-×-Margaretha-Harasinič-[~Škarasič/HRIŽAN-variant-paralela!]-Krasinec-24-22-l-NI-blok",
  "v8-Februar-Martin-Škala-[~Skalar!]-Godze-melj?[~X]-5-Adligsmann-30-l-×-Margaretha-Perjan-[~Ptičjan-DUEL!]-Mokob-34-17-l-NI-blok",
  "v9-6.-Februar-Peter-Jakofčič-[~Jagerfeir-DUEL!]-[?]-2-23-l-×-Margaretha-Jakofčič-[~DUEL!]-[?]-9-19-l-ISTA-PRIIMKA-oboje-strani-INTRA-kandidat-hiši-[~X-OPEN]-NE-varn-NI-blok",
  "v10-24[~29]-April-Franz-Zegennan-[~Hegnaur-DUEL!]-Grabrovec-19-30-l-×-Maria-Hrovač-[~Horvat-DUEL!]-Podgora?-8-30-l-NI-blok",
  "v11-27.-Mai-Mathias-Habič-[~Filak-DUEL!-cf.-1878-Šelah-Filak!]-Gorem/Krm-33-24-l-×-Maria-Hoharič-[~Horvat-DUEL!]-Boršt-18-22-l-NI-blok",
  "v12-11.-Juni-Franz-Mežnarič-[~Mežnarišič!]-Metlika-9-Leinweber-31-l-×-Helena-Kremer-[~Cremez-DUEL!]-Primostek-1-30-l-NI-blok",
  "v13-1.-August-Josef-Plut-[~Pore/Pleivc-DUEL!]-'des-Pfarrers-v.-Črnomelj'-pripis-unehelich-kandidat-26-l-×-Agnes-Guek-[~Plut-DUEL!]-Kloster-27-[~3-DUEL!]-20-l-+ pripis-'M.P.-Leingang-Graz-1877-dd.-22-März-1877'[~X] NI-blok",
  "v14-16.-September-Johann-Muec-[~Mic-DUEL!]-Primostek-7-[~1-DUEL!]-Häusler-29-l-×-Maria-geb.-KRIŽAN-[~Pežjan-DUEL!-HRIŽAN-kontekst!]-Primostek-30-l-NI-blok",
  "v15-14.-November-Johann-Hrusovec-gostilnar-Dobravice-14-25-l-×-Maria-Dubala-[~Brubala-DUEL!]-Košuva-2-20-l-NI-blok",
  "v17-21.-November-Josef-Pluh-[~Bluh/Blat-DUEL!]-'Kblo.-šter.-36'[~KLOŠTER-split!-vs-GRIBLJE-36-P2-DUEL-X-OPEN!]-25-[~23-DUEL!]-×-Katharina-Hugelč-[~Kugelj-DUEL!]-Dobravce-11-19-l-NI-blok (h36-firstYear-OSTAJA-1878-P246!)",
  "v18-25.-November-Josef-Stubler-Cerki-31-[~X-OPEN-'Cerkež'/'Cerkvi'?]-gärtner?-24-l-×-Barbara-Stubler-Primostek-2-gospodarica-35-l-+ pripis-'unbemittelt-in-Reichenau?'[~] NI-blok (Stubler×Stubler-različni-kraji!)",
] as const;

/** Vse-nove-1877-meritve-v-obliki-za-QA (skupaj-04455: 242→247 · vitals: 1985→1990 · sidra: 235→240-1877:5! · dobe: 209→214-44-pred-linijskih!). */
export const MARRIAGE_1877_KORPUS = {
  skupaj04455: 247,
  skupajVitals: 1990,
  sidra: 240,
  dobe: 214,
} as const;

/** ——— P248: poročna predzgovorina 04455, leto 1876 = 10/13 (s11–s14; RESTART = s11-VRSTA-2-tail-violet-8-nad-nim!-TAIL-1875 = NAKNADNI-VPIS!-10.-MEJNA-VARIANTA!) — 15 VPISOV-BREZ-PRESKOKOV · 6-GRIBLJE-blokov-6-DVIGOV-V-1-LETU-REKORD (h44-ZA-23-LET!) ——— */
export const MARRIAGE_1876_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1876,
);
export const MARRIAGE_1876_GRIBLJE = MARRIAGE_1876_BLOCKS.length;
export const MARRIAGE_1876_HOUSES = MARRIAGE_1876_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1876_TOTAL = 15;

/** Meje 1876: RESTART-s11-VRSTA-2 (marginal-'1'-fizično!-tail-violet-8-nad-nim!-vpis-1 = '9.-Februar'-BREZ-letnice!-mesec-mikro-forenzika-'f'!) + MEJA-1875/76 = s10→s11 (NAKNADNI-VPIS-VMES!-kaplan-Perschek!) + MEJA-1876/77 = s14→s15 (finis-1876-3.-instance-P247-1:1!). */
export const MARRIAGE_1876_MEJA = {
  restartSi:
    "restart-vpis-1 = 9. Februar 1876 = s11-VRSTA-2 (druga-vrsta!-marginalna-'1'-FIZIČNO-1:1!-tail-violet-8-NAD-nim!-velika-glava-NE-obstaja-AMPAK-vpis-1-BREZ-letnice-'de.-fbruar-9'-mesec-mikro-forenzika-'f'-ena-zanka+spodnja-zanka-NI-J-1:1!-X-OPEN-anomalija!) — ženin-GRIBLJE-31-Nicolaus-Krupanič-[~Zupanič/Grupanič-K-DUEL-3-branja!]-34-l-×-nevesta-GRIBLJE-44-Katharina-PEGDIRE-20-l = INTRA-DVOJNI-BLOK-h31×h44!-+ zettel-'woher-Güblje-dd.-8.-Februar-1876'-1:1-(permit-dan-pred!)-+ sreda-ritem-9/16/23!",
  restartEn:
    "restart-entry-1 = Feb 9, 1876 = s11-ROW-2 (the-second-row!-the-margin-'1'-PHYSICALLY-1:1!-the-violet-8-ABOVE!-no-big-heading-BUT-entry-1-WITHOUT-year!-the-month-mikro-forensics-'f'-1:1!) — groom-GRIBLJE-31-Nicolaus-Krupanič-[~DUEL!]-×-bride-GRIBLJE-44-Katharina-PEGDIRE = INTRA-DOUBLE-BLOCK!-+ zettel-'dd.-8.-February-1876'-1:1!",
  tailSi:
    "★★★ TAIL-1875 = s11-VRSTA-1-VPIS-8-VIOLET-NAKNADNI-VPIS (marginalna-'8'-fizično-ENA-številka-1:1!-VIJOLIČNO-ČRNILO!-podpis-KAPLAN-Daniel-Perschek-[~Fošbek-P/O-DUEL!]-≠-DOVGAN-1.-ne-Dovgan-podpis-1875–1885!-datum-'1875'+'3.'-mesec-MAREC~AUGUST-TRIPLE-DUEL-[Mikro-'M'-p2-'August'-P1-'Februar'!]-zettel-'den-3.-August-1875'-PODPORA-AUGUST!-ženin-Johann-Blažek-31-l-'Gornje-Kamenice-[~]'-Mühlbauer-×-Klemenčič-Hinenzia-[~DUEL!]-23-l-'Graßac-[~]-1'-opomba-'Privat'!) = NAKNADNO-DOPISAN-ČEZ-MEJO → NAPAVED-P249: preskok-8-v-1875-margine-s8–s10 (1–7-+-9–17!)",
  tailEn:
    "★★★ THE-1875-TAIL = s11-ROW-1-ENTRY-8-VIOLET-THE-LATE-ADDED-ENTRY (the-margin-'8'-physically-ONE-digit-1:1!-VIOLET-ink!-signature-the-CHAPLAIN-Daniel-Perschek-[~Fošbek-DUEL!]-≠-DOVGAN!-date-'1875'+'3.'-month-MARCH~AUGUST-TRIPLE-DUEL-zettel-'Aug-3-1875'-SUPPORTS-AUGUST!-groom-Johann-Blažek-×-Klemenčič-Hinenzia-[~DUEL!]-annotation-'Privat'!) = LATE-ADDED-ACROSS-THE-BOUNDARY → the-P249-FORECAST: the-skip-of-8-in-1875-margins-s8–s10",
  boundarySi:
    "meja-1875/76 = s10→s11-NA-ISTI-STRANI (tail-1875-REGULARNO = s10-vpis-17-'Juli-20'-očesa!-margine-13–17-April–Juli!-+ s11-VRSTA-1-NAKNADNI-violet-8-+ s11-VRSTA-2-RESTART-'1'!) · meja-1876/77 = s14→s15 (P247-1:1!-'f-i-n-i-s-/-1-8-7-6'-s14 = 3.-instance-zaključne-oznake-re-verifikacija-P248-očesa-krop-1:1!-vzorec-SODA-leta-1876/1878/1880!)",
  boundaryEn:
    "the-1875/76-boundary = s10→s11-ON-THE-SAME-PAGE (the-regular-1875-tail = s10-entry-17-'Juli-20'!-+ the-s11-ROW-1-LATE-violet-8-+ the-s11-ROW-2-RESTART-'1'!) · the-1876/77-boundary = s14→s15 (P247-1:1!-the-'finis-1876'-s14 = the-3rd-instance-re-verified-P248!)",
} as const;

/** Številčenje 1876 (s11-restart-1–5 · s12-6–9-'8'-'2'-glif-RAZREŠEN! · s13-10–13 · s14-14–15) — 15-VPISOV-BREZ-PRESKOKOV-7.-leto + margin-številčenje-4.-leto. */
export const MARRIAGE_1876_NUMBERING =
  "s11 = restart-1–5 (margine-1/2/3/4/5-fizično-margins-krop-1:1!) · s12 = 6–9 (6/7/8/9!-margina-'8'-dvom-'2'-glif-RAZREŠEN-margins-krop-8×-dvojni-lok-1:1!) · s13 = 10–13 · s14 = 14–15 — 15-VPISOV-BREZ-PRESKOKOV-7.-leto-zapored (1876–1882!-NODAT-×0-3.-leto!-margin-številčenje-4.-leto-1879-1.·1878-2.·1877-3.·1876-4.!-svetlo-modro-sivo!)";

/** ★★★★★ FOLIACIJA-1876-'Pag = sken−1'-4/4 (s11-'Pag. 10'-2×-neodvisno! + s12-'Pag. 11'-pass-1-'4'-MISREAD-KOREKCIJA! + s13-'Pag. 12'-2×! + s14-'Pag. 13'-3×!-P247-kontekst!) — skupaj-z-19/19! */
export const FOLIACIJA_1876 =
  "s11-'Pag. 10'-2×-neodvisno-1:1-+ s12-'Pag. 11'-očesa-1:1-pass-1-'Pag. 4'-MISREAD-KOREKCIJA!-+ s13-'Pag. 12'-2×-1:1-+ s14-'Pag. 13'-3×-1:1-(P247-kontekst!)= 4/4-1876!-→ skupaj-z-4/4-1877-+ 6/6-1878-+ 5/5-1879 = 19/19-v-zaporednih-letih (pravilo-Pag==sken−1-NE-PRELAMA-5.-leto!)";

/** ★★★ 10.-MEJNA-VARIANTA (1876): restart-VRSTA-2-NA-ISTI-STRANI-kot-tail + tail-violet-NAKNADNI + restart-BREZ-letnice + INLINE-od-2.-lista. */
export const MEJNA_10_VARIANTA_1876 =
  "10.-MEJNA-VARIANTA-1876: restart = s11-VRSTA-2-(druga-vrsta!-NE-top-kot-1877/1878!-NE-dno-kot-1880-P243!-NE-glava-kot-1879-P244!)-+ tail-violet-NAKNADNI-VPIS-NAD-nim-(kaplan-Perschek!)-+ restart-vpis-1-BREZ-letnice-(vs-P246/P247-INLINE-v-1.-vpisu-VSAKEGA-lista!)-+ INLINE-letnica-od-2.-lista-(s12-'1876.-Febr.-16.'-+ s13-'1876.-Februar-23.'-+ s14-'1876.-Novembris-15.'-3/3-fizično!)-= 4-nove-elemente-v-1-meji-NOV-TIP (ponavljanje-glave-je-LETO-specifično: 1877+1878+1876-INLINE!-velike-glave-samo-1879!-restart-na-dnu-samo-1880!)";

/** ★★★★★ 6-firstYear-DVIGOV-V-1-LETU = REKORD-LINIJE: h44-ZA-23-LET-NOV-ABSOLUTNI-REKORD + h30-ZA-13 + h64-ZA-12 + h31-ZA-10 + h35-ZA-6 + h41-ZA-5. */
export const FIRSTYEAR_1876_REKORD =
  "★★★★★ 6-firstYear-04455-DVIGOV-V-1-LETU = REKORD-LINIJE: h44-1899→1876-ZA-23-LET-NOV-ABSOLUTNI-REKORD-(prejšnji-h53-10-let-P243!-h10-h69-10-let-P247!-h44-04455-do-zdaj-1899/1903/1905/1908/1912!)-+ h30-1889→1876-ZA-13-LET-+ h64-1888→1876-ZA-12-LET-(NOVA-HIŠA-V-04455!)-+ h31-1886→1876-ZA-10-LET-+ h35-1882→1876-ZA-6-LET-+ h41-1881→1876-ZA-5-LET-6-blokov-VSI-6-hiše-PRVIČ-v-04455-predzgodovini";

/** ★★★★★ PEZDIRC/PEGDIRE-×9-omemb-V-1-LETU = REKORD-POROČNE-PREDZGOVINE (×4-BLOKOV!-'Leinmannstochter'-×2!-PEGDIRE-LEINWEBER-DRUŽINA-kandidat!). */
export const PEZDIRC_1876_REKORD =
  "★★★★★ PEZDIRC/PEGDIRE-×9-omemb-V-1-LETU-REKORD-POROČNE-PREDZGOVINE (cf.-P243-×3!-P241-×5-vpisov!-P242-×5!-P246-×2!): v1-nevesta-Katharina-Pegdire-h44-+ v8-mati-Maria-née-Pegdire-h64-mikro-1:1!-+ v9-nevesta-Barbara-Pegdire-+ v9-oče-Georg-Pegdire-×-Anna-TOME-+ v9-priča-Georg-Pegdire-+ v13-nevesta-Maria-Pegdire-h41-'Leinmannstochter'-+ v13-oče-Georg-Pegdire-×-Anna-BRINC-+ v14-nevesta-Anna-Pegdire-h30-'Leinmannstochter'-+ v14-mati-Mathiewa-née-Pegdire = ×9!-od-toga-×4-BLOKOV-(h44-+ h64-mati-+ h41-+ h30!)-+ ★ 'Leinmannstochter'-×2-(v13+v14!)-= PEGDIRE-LEINWEBER-DRUŽINA-kandidat-[X-OPEN!-cf.-P80-h13-Leinann-nit-+ P241-v26-Križan-'Leinweber'-+ P243-h63-'dekla-v-Gribljeh'!]-+ ★ 2×-Georg-Pegdire-(v9-×-Anna-Tome-vs-v13-×-Anna-Brinc!)-ISTA-IME-2-ženi-kandidat-X-OPEN";

/** ★★★ h35-PARALELA-1:1 ('Mathias-Hrižan'-h35 == P229-z79-krst!) + DOVGAN-10-LET. */
export const H35_1876_PARALELA =
  "★★★ h35-PARALELA-1:1: v8-ženin-'Mathias-Hrižan-[~Križan-H-forma-DUEL!]'-h35-22-l == P229-z79-krst-04104-'Mathias-Hrižan'-h35 (ISTO-IME+ISTO-HIŠA-1:1!-oče-v8-'Nicolaus'-vs-krstni-oče-DUEL!-OČE-SIN-ISTO-IME-kandidat-X-OPEN-cf.-P231-z111-Kelcho-veriga!)-+ h35-HRIŽAN-veja-cf.-P246-v17-nevesta-1878-1:1-SKLAD-P229!";

export const DOVGAN_1876_ZACETEK =
  "DOVGAN-CONTINUUM-PODALJŠAN-NA-10-LET (1876–1885!): Georg/Franz-Dovgan-podpisi-na-VSIH-4-glavnih-listih-od-restarta-vpis-1-(garble-'Porger'-'Dorgar'-'Dorgun'-pass!)-cf.-DOVGAN_1877_PODALJŠITEV-9-let-→-ZDAJ-10!-+ ★ TAIL-1875-KAPLAN: 'Daniel-Perschek-[~Fošbek-P/O-DUEL!]'-vijolični-NAKNADNI-VPIS-s11-top = 1.-NE-DOVGAN-podpis-Dovgan-začenja-ŠELE-z-restartom-1876!";

/** Datum-dueli 1876 + INTRA-×2 + IZMENA-×2 + DISPENS-3.-GRAD + MLADOLETNICA-×2. */
export const MARRIAGE_1876_DUELS = [
  "v1-mesec »Januar vs Februar 9« REŠEN-mikro-forenzika-'f'-1:1-za-FEBRUAR (ena-zanka+spodnja-zanka-NI-J!-permit-'dd.-8.-Februar'-konsistentno!-sreda-ritem-9/16/23!)",
  "v13-datum »22. Oktober vs Sept 17« REŠEN-2:1-za-OKTOBER (mikro-'O'-poudarjen-+pass-1!-zettel-'dd.-16.-7ber'-(September)-5-tednov-prej!-'7~8-ber'-POPRAVEK-kandidat-X-OPEN!)",
  "v12-datum »17. Septembris [~14-DUEL-mikro-'7'-jasen-vertikal-2:1!]«",
  "tail-1875-mesec »MAREC vs AUGUST vs FEBRUAR« TRIPLE-DUEL-[X-OPEN!]-(mikro-'M'-z-lokoma!-p2-'August'-+ zettel-'3.-VIII'-PODPORA-AUGUST!-P1-'Februar'!)",
  "v8-starost »22 vs 20« REŠEN-mikro-2:1-za-22 ('2'-zaključen-lok-1:1!)",
  "s12-margina »8 vs 2« REŠEN-fizično-1:1-za-8 (margins-krop-8×-DVOJNI-lok!-full-page-'2'-glif-MISREAD!)",
  "v6-Wohnort »Drašiče-36-pf.-Möbling vs Gradac-36« REŠEN-3:1-za-DRAŠIČE (pass-1+p2+p4!-Metlika-pfarrei-pripis!)",
] as const;

/** ★★ KONTEKST-izven-Griblje-1876-NI-bloki-pošteno. */
export const MARRIAGE_1876_KONTEKST = [
  "v2-16.-Februar-Johann-Tomc-24-l-[~27-DUEL!]-'Škri.še-1'[~Škrilje?-š-háček-forenzika-NE-'Gri.'!]-½-g.-Rofpunnwirth[?]-×-Mlakve-11-Maria-Juraješič[~Jurejevič!]-18-l-NI-blok",
  "v3-16.-Februar-Mathias-Pasič-45-l-Desinec-pp.-Cernomelj-3-×-Cerhin.še-15-[~18-DUEL!]-Anna-Movrin-41-l-NI-blok",
  "v4-16.-Februar-Georg-Movrin-29-l-Cerhin.še-15-×-Desinec-3-Margareh-Pasič-19-l-★★★ IZMENA-VLOG-v3/v4 (Pasič×Movrin→Movrin×Pasič!-cf.-P241-v6/v7-TOMC-BERČOPEC!)-NI-blok",
  "v5-16.-Februar-Georg-Jurejevič[~Jeroschinich!]-40-l-Cerhin.še-17-'½-Gübl.'-PRIPIS!-×-Krasinec-20-Dorothea-Škrabanič[~Krasinič-DUEL!]-26-l-★★ '½-Gübler'-status-cf.-P244-v3-Krugel!-NI-blok",
  "v6-16.-Februar-Mathias-Mohlorič[~Mahlorič!]-28-l-'Drašiče-36'-pf.-Möbling-(Metlika!)-3×-branja!-×-Dobranice-8-Margareta-Štefanič-22-l-NI-blok",
  "v7-16.-Februar-Jakob-Štefanič-25-l-Dobranice-8-×-Podzgemeľ-6-Barbara-Tome-40-l-★★★ DISPENS-3.-GRAD-1:1-'Christliche-Dispens-vom-dritten-Grad-dd.-12.-Febr.'-+'zweifache-Dispens-dd.-15.-Febr.-876'-dve!-starost-razlika-15-let!-★★ IZMENA-ŠTEFANIČ-v6-nevesta→v7-ženin-ISTA-HIŠA-Dobranice-8!-NI-blok",
  "v9-23.-Februar-Nikolaus-Mihelič[~Milek-DUEL!-MILIČ-križ-kandidat-IZVEN-korpusa-cf.-P244-'Mileh'-×238!]-22-l-'Zemelj[~Femelj/Podgemelj-DUEL!]'-19-×-Boršt-23-Barbara-PEGDIRE-21-l-★★ starši-neveste-Georg-PEGDIRE-×-Anna-née-TOME-(3×-branja!)+ priča-Georg-Pegdire!-zettel-Podgemelj-dd.-22.-Januar-+ Consens-Decan-15.-Februar-NI-blok",
  "v10-23.-Februar-[letnica-INLINE!] Johann-Kupanič[~Županič-DUEL!-cf.-v1-Krupanič-TRIPLE-ISTO-DUEL-SKOUPINA!]-23-l-Vinica-1-×-Krasina-63-[~43-DUEL-6-vs-4-P246-lekcija!]-Anna-Bahovič-17-l-MLADOLETNICA-Aufgebot-4.-und-13.-Febr-+ Consens-Vormund-k.k.-Bez.-dd.-9.-Febr-NI-blok",
  "v11-27.-Februar-Janko-Mihelec-26-l-Velika-Gorica-Lipnik-Kroatien-9-×-Adlešiči-16-Barbara-Novak-22-l-zettel-25.-Febr-+ dispens-Eheconsens-4.-Jänner-1876[~]-Mülling!-NI-blok",
  "v12-17.-Septembris-[~14]-Eduard-Lingl-30-l-Graz-Windberg-48-OFFICIER-Infanterie!-×-Graz-Blae-23-Josepa-29-l-vojaški-vpis-Konsens-Militärbehörde!-NI-blok (cf.-v8-vojaška-omemba!)",
  "v15-20.-Novembris-Anton-Novak-33-l-Gradac-3-×-Gradac-14-Rosalia-Mascle[~Marcele!]-18-l-zettel-19.-Novembris-1876-NI-blok",
] as const;

/** Vse-nove-1876-meritve-v-obliki-za-QA (skupaj-04455: 247→253 · vitals: 1990→1996 · sidra: 240→246-1876:6! · dobe: 214→220-50-pred-linijskih!). */
export const MARRIAGE_1876_KORPUS = {
  skupaj04455: 253,
  skupajVitals: 1996,
  sidra: 246,
  dobe: 220,
} as const;

/** ——— P249: poročna predzgovorina 04455, leto 1875 = 11/13 (s8–s10 + s7-tail-1874-kontekst; RESTART = s8-TOP!-margina-'21'-ANOMALIJA!-preskok-8-FALSIFICIRANA-dup-8!-MNOŽIČNI-DAN-4.-Februar-×10!-FINIS-1874-s7!-DOVGAN-11-LET!) — 17-rednih + 1-violet-NAKNADNI = 18-vpisov · 1-GRIBLJE-blok (h8!) ——— */
export const MARRIAGE_1875_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1875,
);
export const MARRIAGE_1875_GRIBLJE = MARRIAGE_1875_BLOCKS.length;
export const MARRIAGE_1875_HOUSES = MARRIAGE_1875_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1875_TOTAL = 18;

/** Meje 1875: RESTART-s8-TOP ('21'-anomalija-margine!-velika-'1875'-INLINE!) + MEJA-1874/75 = s7→s8 (finis-1874-4.-instance-SODA-vzorec!-h42-tail-kandidat!) + MEJA-1875/76 = s10→s11 (P248-1:1-re-verifikacija!-violet-8-dup-kolizija!). */
export const MARRIAGE_1875_MEJA = {
  restartSi:
    "★★★ RESTART-1875 = s8-TOP (vpis-1 = 16. Jänner 1875 — velika-letnica-'1875'-v-datumskem-stolpcu-1.-vrste-INLINE-vzorec!-velika-naslovna-glava-NE-obstaja!) — vpis-1 = Jakob-Šolnar-[~Lovar-DUEL!]-vrtnar-migrant-iz-Sajevce-Pf.-Ribnica-38-l-×-Maria-Jurmanič-[~Družamič!]-Gradac-33-l-NI-blok + ★★★ MARGINA-r1 = '21'-FIZIČNO-ANOMALIJA (dve-števki-6×-mikro-1:1!-r2–r7-'2'–'7'-enostavno!-→-aritmetika-VSILJUJE-'1'-pisarska-napaka-cf.-P245-s28-'7'!)",
  restartEn:
    "★★★ THE-1875-RESTART = s8-TOP (entry-1 = Jan-16-1875 — the-big-'1875'-INLINE-in-the-date-column!-no-separate-heading!) — groom-Jakob-Šolnar-[~Lovar!]-gardener-migrant-from-Ribnica-×-Maria-Jurmanič-Gradac-NOT-a-block + ★★★ THE-ROW-1-MARGIN = '21'-PHYSICAL-ANOMALY (two-digits-6×-mikro-1:1!-rows-2–7-'2'–'7'-single!-→-arithmetic-FORCES-'1'-a-clerical-error!)",
  tailSi:
    "★★★ MEJA-1874/75 = s7→s8: tail-1874 = s7-margine-28–32 (28.-Februar…18.-November-1874-5-vpisov!-Dovgan-podpisi!) + ★★★ FINIS-'f-i-n-i-s-/-1-8-7-4'-s7-dno = 4.-INSTANCE-ZAKLJUČNE-OZNAKE-LETA (vzorec-SODA-let-1874/1876/1878/1880-POTRJEN!-LIHA-leta-1875/1877/1879-BREZ-finis-konzistentno!-'7'~'y'+'4'~'A.'-letterform[~]) + ★★★ TAIL-KANDIDAT: m32-Maria-Pegdirc-GRIBLJE-42 (mikro-6×-1:1!-'1a'-ZAVRŽEN!-ženin-Nicolaus-Marasinič-Krasinice-12) = h42-PARALELA-1:1-z-Georg-Pegdirc-1879-P244-v21 → NAPAVED-P250-PROMOCIJA!",
  tailEn:
    "★★★ THE-1874/75-BOUNDARY = s7→s8: the-1874-tail = s7-margins-28–32 (Feb-28…Nov-18-1874-5-entries!-Dovgan-signatures!) + ★★★ THE-'f-i-n-i-s-/-1-8-7-4'-ORNAMENT-at-the-s7-bottom = the-4th-INSTANCE-of-the-YEAR-CLOSING-MARK (the-EVEN-YEAR-pattern-1874/1876/1878/1880-CONFIRMED!-odd-years-WITHOUT-finis-consistently!) + ★★★ THE-TAIL-CANDIDATE: m32-Maria-Pegdirc-GRIBLJE-42 (mikro-6×-1:1!) = the-h42-PARALLEL-1:1-with-Georg-Pegdirc-1879 → the-P250-FORECAST-PROMOTION!",
  boundarySi:
    "meja-1875/76 = s10→s11 (P248-1:1-RE-VERIFIKACIJA-P249!-tail-1875-REGULARNO = s10-vpis-17-'Juli-20'-re-1:1-očesa-+ margina-'17'!-+ s11-violet-NAKNADNI-8-P248-1:1-+ s11-VRSTA-2-restart-'1'-1876!) · ★ P248-NAPAVED-preskok-8-FALSIFICIRANA: regularni-margina-'8'-'9'-'10'-FIZIČNO-1:1-s9 → DUP-8-ŠTEVILČENJA-KOLIZIJA (redni-run-1–17-BREZ-preskoka + naknadni-vpis-tudi-'8'-prištevan-po-lastni-glavi!)",
  boundaryEn:
    "the-1875/76-boundary = s10→s11 (P248-1:1-RE-VERIFIED!-the-regular-1875-tail = s10-entry-17-'Juli-20'-re-1:1!-+ the-violet-LATE-8-P248-1:1!) · ★ the-P248-skip-of-8-FORECAST-FALSIFIED: the-regular-margins-'8'-'9'-'10'-PHYSICALLY-1:1-on-s9 → the-DUP-8-NUMBERING-COLLISION (the-regular-run-1–17-WITHOUT-skip + the-late-entry-also-'8'!)",
} as const;

/** Številčenje 1875 (s8-1–7-'21'-anomalija!-· s9-8–12-· s10-13–17) — 17-rednih-BREZ-preskokov-8.-leto + violet-NAKNADNI-'8'-dup-kolizija! */
export const MARRIAGE_1875_NUMBERING =
  "s8 = restart-1–7 (margina-r1-'21'-FIZIČNO-ANOMALIJA-dve-števki-6×!-aritmetika-VSILJUJE-'1'-r2–r7-'2'–'7'-1:1!) · s9 = 8–12 (margine-'8'/'9'/'10'-FIZIČNO-1:1-5×!-NAPAVED-preskok-8-FALSIFICIRANA!) · s10 = 13–17 (margina-'17'-tail-1:1!) — 17-REDNIH-VPISOV-BREZ-PRESKOKOV-8.-leto-zapored (1875–1882!-NODAT-×0-4.-leto!-margin-številčenje-5.-leto-1879-1.·1878-2.·1877-3.·1876-4.·1875-5.!-svetlo-modro-sivo!) + DUP-8: violet-NAKNADNI-s11-top-tudi-'8'-P248-1:1 = total-18-vpisov";

/** ★★★★★ FOLIACIJA-1875-'Pag = sken−1'-4/4 (s7-'Pag. 6' + s8-'Pag. 7' + s9-'Pag. 8.' + s10-'Pag. 9.'!-VSE-1:1-BREZ-misreadov!) — 23/23-v-zaporednih-letih-6.-leto! */
export const FOLIACIJA_1875 =
  "s7-'Pag. 6'-1:1-+ s8-'Pag. 7'-1:1-+ s9-'Pag. 8.'-1:1-+ s10-'Pag. 9.'-1:1-(očesa-+pass-1-BREZ-misreadov!-s11-'Pag. 10'-P248-2×-že-1:1!)= 4/4-1875!-→ skupaj-z-5/5-1879-+ 6/6-1878-+ 4/4-1877-+ 4/4-1876 = 23/23-v-zaporednih-letih-6.-leto (pravilo-Pag==sken−1-NE-PRELAMA!)";

/** ★★★ MNOŽIČNI-POROČNI-DAN-'4. Februar 1875'-×10 (v3–v12!) = REKORD-poroke-v-1-dnevu-v-predzgodovini + datumski-vzorec-mesec-samo-ob-spremembi. */
export const MNOZICNI_DAN_1875 =
  "★★★ MNOŽIČNI-POROČNI-DAN-'4. Februar-1875'-×10 (v3–v12-VSE-datumi-'4.'-fizično-kropi-2.2×–2.6×-1:1!-REKORD-poroke-v-1-dnevu-v-predzgodovini-cf.-P244-1879-'19.-Februar'-×3!) + ★★★ DATUMSKI-VZOREC-MESEC-SAMO-OB-SPREMEMBI: v2-'Febr. 2.'-polno → v3–v12-SAMO-'4.'-(mesec-impliciten!) → v13-'1875. Febr. 8.'-(ob-listi-začetek-z-letnico!) → v14-'8'-SAMO-DAN → v15-'Mai 9.'-(nov-mesec-polno!) → v16-'Juni 13.' → v17-'Juli 20.' — letnica-SAMO-na-1.-vpisu-lista (s8/s9/s10-3/3-fizično!)";

/** ★★★ DOVGAN-KONTINUUM-PODALJŠAN-NA-11-LET (1875–1885!) — vsi-17-rednih-vpisov + edina-izjema-violet-NAKNADNI-kaplan-Perschek. */
export const DOVGAN_1875_PODALJŠITEV =
  "★★★ DOVGAN-KONTINUUM-PODALJŠAN-NA-11-LET (1875–1885!): Franz-Dovgan-podpisi-na-VSIH-17-REDNIH-vpisih-s8–s10 (visual-kropi-s8-r1–r4-×4-1:1-+ s9-×3-1:1-+ v10/v17-1:1-+ pass-1-VSI!-garble-'Dorgan/Dorgon'!)-→ P248-'10-let-(1876–1885)'-PODALJŠAN-ZA-1-LETO-NAZAJ!-★ IZJEMA-EDINA: s11-top-violet-NAKNADNI-8 = KAPLAN-Daniel-Perschek (P248-1:1!) = 1.-in-EDINI-ne-Dovgan-podpis-v-kontinuumu-→-kaplan-samo-NAKNADNI-vpisi-[~X-OPEN!-1874-tail-s7-vsi-Dovgan!]";

/** ★★★ h42-PARALELA-1:1 (Maria-Pegdirc-1874-tail == Georg-Pegdirc-1879-P244!) + NAPAVED-P250-PROMOCIJA. */
export const H42_1874_PARALELA =
  "★★★ h42-TAIL-PARALELA-1:1: s7-m32-nevesta-'Maria-Pegdirc'-GRIBLJE-42-(mikro-6×-1:1-'Griblje-42.'-'1a'-'13'-'12'-vs-branja-RAZREŠENI!)-18.-November-1874 == P244-v21-ženin-'Georg-Pegdirc'-GRIBLJE-42-ultra-zoom-1:1-1879 (ISTA-HIŠA-ISTA-DRUŽINA-PRIIMEK-2-dokaza-5-let-narazen!-oče-hči-brat-sestra-kandidat-X-OPEN!)-+ TAIL-1874-KANDIDAT-BLOK-→-NAPAVED-P250: PROMOCIJA-tail-kontekst→blok-(cf.-P248-h30-vzorec!)-korpus-04455-ŽE-ŠTEJE-h42-×2-(1890-1896...-pt-luknja!)-04455-tail-blok-bi-bil-3.-(ali-1.-po-leta-obratno!)";

/** ★★★ PEZDIRC-MREŽA-×3-kontekst-1875-NI-bloki-pošteno (+ tail-kandidat!). */
export const PEZDIRC_1875_KONTEKST =
  "PEZDIRC-CONTINUUM-×131→04455-v-7.-LETU-predzgodovine-NI-bloki-pošteno: v10-priča-'Anton-Pegdire'-[~PEZDIRC!-vs-očesi-'Jakob'-A/J-DUEL-krop-1:1-'Anton'!]-+ v16-mati-neveste-'Anna-Pegedire'-[~PEZDIRE!-starši-Math.-Štubler!-cf.-P248-v8-'Maria-née-PEGDIRE'-+ v14-'Mathiewa-née-PEGDIRE'-mama-nit!]-+ v17-priča-'Georg-Pegdire' = ×3-kontekst-+ ★ tail-m32-'Maria-Pegdirc'-h42-KANDIDAT (grafija-continuum-7-let!-Pegdire/Pegedire/Perdirc!-cf.-P246-×2-8.-od-zadaj!)";

/** ★ MLADOLETNICA-v16 + najstarejša-nevesta-v13-46-l + Mötthling-vzorec. */
export const MLADOLETNICA_1875 =
  "★★ MLADOLETNICA-×1: v16-nevesta-Margaret-Stubler-18-l-+ 'Vormundschaft-spect.-Consens-v.-k.k.-Bez.'-+ 'Mötthling-dd.-9.-Juni-1875'-garble-(ISTI-VZOREC-kot-P248-v14-'Mötthling'-k.k.-Bez.Gericht-Metlika!)-★ v12-nevesta-27-l-NI-mladoletnica-(očesi-'17'-VLM-'24'-KROP-4×-1:1-'27'-ZMAGA!-starostni-DUEL-pošteno!)-★ v13-nevesta-Katharina-Stubler-46-l = NAJVIŠJA-starost-neveste-v-predzgodovini-do-zdaj (cf.-P245-v1-43-l!-VDOVA-kandidat!-Stubler-×2-v-1-letu-v13+v16-ISTA-vas-Verlinišče!)";

/** Datum-dueli + kontekst-izven-Griblje-1875-NI-bloki-pošteno. */
export const MARRIAGE_1875_DUELS = [
  "s8-margina-r1 »21 vs 1« REŠEN-aritmetiko-za-'1' (FIZIČNO-'21'-dve-števki-6×-1:1!-r2–r7-'2'–'7'-enostavno → restart-'1'-pisarska-napaka-cf.-P245-s28!-X-OPEN-tumačenje!)",
  "s9-v8-datum »24. Jänner vs 8. Februar vs 4. Februar« REŠEN-mikro-5×-za-'1875. Febr. 4.' (VLM-'24-Jän'-ZAVRŽEN-očesi-'8-Febr'-ZAVRŽEN!)",
  "v10-nevesta-ime »Katharina vs Maria« REŠEN-2.6×-krop-za-MARIA (VLM-'Maria-Zahopir'-+ krop-'Maria-Jatnopir'!-priimek »Zahopir vs Jatnopir vs Janopirić« TRIPLE-DUEL-[~X-OPEN!])",
  "v10-hišna »Griblje 8 vs 6« REŠEN-mikro-2.6×-za-8 (jasen-'8'-s-piko!)",
  "v12-starost »17 vs 24 vs 27« REŠEN-mikro-4×-za-27 (sedmica-s-prečko-1:1!)",
  "v8-starost »24 vs 29« REŠEN-mikro-1.9×-za-29 (MILEK-Anna-Zemelj-19!)",
  "v17-starost »19 vs 22« REŠEN-mikro-4×-za-19",
  "v15-hišna »Gradac 26 vs 11« REŠEN-mikro-5×-za-26",
  "s7-m32-hišna »Griblje 42 vs 1a vs 13 vs 12« REŠEN-mikro-6×-za-42 ('4'+jasen-'2'-2:1!-h42-PARALELA-podpora!)",
  "s7-finis »1-8-7-4« letterform-duel »7~y + 4~A.« [~X-OPEN!] (okrasni-Kurrent!-vzorec-SODA-let-podpora-2:1!)",
  "v14-datum »Februar 8 vs März 8« REŠEN-vzorec-mesec-samo-ob-spremembi-za-8.-FEBRUAR (mesec-impliciten!-v15-'Mai'-šele-nov-mesec!)",
] as const;

export const MARRIAGE_1875_KONTEKST = [
  "v1-16.-Jänner-1875-RESTART-Jakob-Šolnar-[~Lovar-DUEL!]-vrtnar-38-l-'iz-Sajevce-Pf.-Ribnica'-MIGRANT-×-Maria-Jurmanič-[~Družamič!]-Gradac-28[~38]-33-l-NI-blok (Befunde-'Ehefähigkeitsattest'-polit.-Gemeinde!)",
  "v2-2.-Februar-Mathias-Govednik-[~Grecdnich-DUEL!]-Ledner-[~]-25-l-Schönstein/Sebnica-[~X]-23-pf.-Kaurlain-×-Katharina-Muc-19-l-Grimoschitz-[~Primostek!]-8-NI-blok (zettel-31.-Jänner!)",
  "v3-4.-Februar-Nicolaus-Simonič-Ledner-28-l-Drašiče-15-pf.-Kaurlain-×-Katharina-Muc-18-l-Zemelj/Gemelj-[~DUEL!]-12-★★ Muc-sestra-paralela-v2/v3-obe-'Katharina-Muc'!-NI-blok",
  "v4-4.-Februar-Johann-Harasinic-30-l-Gradac-48-'aus-Gem.-Nr.-27'[~]-×-Maria-Hvalič-17-l-Podzemelj-11-NI-blok",
  "v5-4.-Februar-Martin-Rus-Ledner-42-l-Dobravice-12-[~Dobrau-ee!]-×-Maria-Jurejevič-26-l-Primostek/Gorica-[~DUEL!]-11-NI-blok",
  "v6-4.-Februar-Mathias-Štefanič-Ledner-23-l-Dobravice-12-×-Margaretha-Gluk-24-l-Hloshelj-[~Hrošelj?]-37-NI-blok",
  "v7-4.-Februar-Johann-Malerič-30-l-Adlig-Kaurlain-148-[~]-Podvinic-[~]-×-Anna-Gluk-25-l-Hloshelj-32-★★ Gluk-sestra-paralela-v6/v7!-NI-blok",
  "v8-4.-Februar-1875-INLINE-Martin-Rus-[~Ruž/Pues!]-Bauer-31-l-Dobrave-13-[~Zemelj-DUEL!]-×-Anna-MILEK-29-l-Zemelj-19-★★★ MILEK-kontekst-(mreža-NI-blok-cf.-h65!-starost-'29'-krop-1:1!)-zettel-Podzemelj-23.-Jänner-NI-blok",
  "v9-4.-Februar-Nicolaus-Prant-[~Åtrand/Strnad-DUEL!]-Bauer-24-l-Jersič/Gersič-5-[~Goršiči!]-×-Maria-Kralj-18-l-Boršt-17-NI-blok (zettel-2.-Februar!)",
  "v11-4.-Februar-Georg-Jurgejič-Bauer-41-l-Kaplšiče/Kraplišče-6-[~]-×-Anna-TOME-23-l-Kaplšiče-3-★★★ TOME-×2-(v10-ženin!)-+ DISPENS-blutsverwandtschaft-omemba-[~X-OPEN!]-NI-blok",
  "v12-4.-Februar-Johann-Žakšon-[~Jakšič-DUEL!]-25-l-Vranovič-2-[~'Vrano-vič'!]-×-Barbara-Čeklho-[~Helfrich-DUEL!]-27-l-Vojna-vas-4-pf.-Vrhnovec/Černomelj-NI-blok (zettel-30.-Jänner!)",
  "v13-8.-Februar-1875-INLINE-Johann-Škarasinič-[~Harasinič!]-Inwohner-33-l-Verlinišče/Lešče-11-[~14-DUEL!]-×-Katharina-Stubler-46-l-Verlinišče/Lešče-20-★★ NAJSTAREJŠA-nevesta-predzgodovine-46-l!-VDOVA-kandidat-NI-blok (Stubler-×1-od-×2!)",
  "v14-8.-Februar-Michael-Segina-Inwohner-25-l-Gologge/Srobotnik-[~X]-27-×-Margar.-Šrambič/Kumber-26-l-Silegje/Srobotnik-27-[~]-NI-blok (priče-Nicolaus-Tome-TOME-×3!-+ Peter-Segina)",
  "v15-9.-Mai-Johann-Schinigman-Cigarenschmied-26-l-Gradac-1-'aus-[Steyr?-X]-Aufenthalt-Dermänice[?]'-MIGRANT-×-Anna-Simončič-22-l-Gradac-26-NI-blok (cf.-P242-v12-Lingl-OFFICIER!)",
  "v16-13.-Juni-Johann-Mihelečič-[~Mihelič!]-Inwohner-23-l-Verlinišče/Lešče-24-×-Margaret-Stubler-18-l-Verlinišče-23-★★ MLADOLETNICA-Vormundschaft-Consens-k.k.-+ Mötthling-9.-Juni-1875!-★★ mati-neveste-Anna-Pegedire-[~PEZDIRE!] × Math.-Štubler!-NI-blok (priče-Math.-Marasinič-+ Peter-Stubler!)",
  "v17-20.-Juli-1875-TAIL-REGULARNO-Josef-Kristl-[~Verbič/Kristlin-DUEL!]-Knecht-27-l-Gradac-81-'aus-Gorenje-pri-Mužnemu[?]'-[~]-×-Anna-Novak-19-l-Gradac-81-NI-blok (priče-Martin-Škala[~Štrale!]-+ ★ Georg-Pegdire-PEZDIRC!-zettel-Gradac-19.-Juni!)",
  "TAIL-1874-s7-kontekst-NI-bloki-pošteno: m28-28.-Februar-1874-Johann-Bajuk/Baynik-25-l-Primostek-12-×-Maria-Pavč/Keržan-Toma-23-l-Primostek-8[~16-DUEL!]-+ m29-8.-März-Martin-Tome-24-l-Primostek-16-×-Katharina-Angelj/Regel-[~DUEL!]-24-l-Dobrau-ee-21-+ m30-21.-April-Mathias-Kopač/Lepičič-40-l-Gradac-10-×-Cecilia-Kukanč/Harvan-38-l-Gostovac-22-(obe-VDOVA-kandidat!)-+ m31-21.-Mai-Jakob-Hrošavec/Brandovec-24-l-Krasinice-11-×-Anna-Klemenčič-20-l-Cermo/Gorica-maloj-14-(priča-'Georg-Podgorec'[~PEZDIRC-križ-kandidat-X-OPEN!])-+ m32-18.-November-Maria-Pegdirc-GRIBLJE-42-KANDIDAT-BLOK!-— vsi-Dovgan-podpisi-tudi-1874!",
] as const;

/** Vse-nove-1875-meritve-v-obliki-za-QA (skupaj-04455: 253→254 · vitals: 1996→1997 · sidra: 246→247-1875:1! · dobe: 220→221-59-pred-linijskih!). */
export const MARRIAGE_1875_KORPUS = {
  skupaj04455: 254,
  skupajVitals: 1997,
  sidra: 247,
  dobe: 221,
} as const;

// ——— P250: leto 1874 = 12/13 (s1–s7 + P249-tail-re-verifikacija; md5-7/7!-s7-križ-1:1-identičen-P249!-s1-vezalo!-Read-očesa-NAJPREJ-×7!-VLM-pass-1-×5 + krops-×83 + mikro-8×-×3!) — 32-VPISOV-BREZ-PRESKOKOV-9.-leto + 11-BLOKOV-NOV-REKORD + 10-DVIGOV + restart-s2-DNO-12.-varianta + KNIJIŽNO-ODPIRANJE-m18/1873! ———

export const MARRIAGE_1874_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1874,
);
export const MARRIAGE_1874_GRIBLJE = MARRIAGE_1874_BLOCKS.length;
export const MARRIAGE_1874_HOUSES = MARRIAGE_1874_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1874_TOTAL = 32;

/** Meje 1874: RESTART-s2-DNO-12.-varianta + KNIŽNO-ODPIRANJE-m18/1873-Pag.-1! + MEJA-1873/74 = s2-MID/DNO-13.-varianta + MEJA-1874/75 = s7→s8-P249-re-verifikacija (m28-'28.-Februar'-KOREKCIJA→'28.-Avgust'!). */
export const MARRIAGE_1874_MEJA = {
  restartSi:
    "★★★ RESTART-1874 = s2-DNO (ZADNJA-vrsta-strani!-vpis-1 = '1874 Jänner 19.'-[~18-DUEL-pass1!]-Jakob-PAŠIČ-[~]-34-l-[Kramarše~?]-4-×-Anna-KUNIČ-[~]-34-l-WITWA-Z-OTROKI-(per-Befunde-pass1!)-NI-blok!) = 12.-MEJNA-VARIANTA (dno-vzorec-2.-instance-cf.-P243-'restart-1880 = s35-DNO'-7.!-P249-napoved-'restart-pričakovan-na-s5-top-ali-s6'-FALSIFICIRANA-2×: s5-top-=-m12!-s4-top-=-m7!)",
  restartEn:
    "★★★ THE-1874-RESTART = s2-BOTTOM (the-LAST-row-of-the-page!-entry-1 = Jan-19-1874-[~18-DUEL!]-Jakob-PAŠIČ-34-y-×-Anna-KUNIČ-34-y-a-WIDOW-WITH-CHILDREN!-NOT-a-block!) = the-12th-BOUNDARY-VARIANT (the-bottom-pattern-2nd-instance-cf.-P243!-the-P249-forecast-FALSIFIED-twice!)",
  knjiznoSi:
    "★★★ NOV-STRUKTURNI-DOKAZ — KNIJIŽNO-ODPIRANJE-04455: s1-=-VEZALO-KNJIGE (rjava-usnjena-povezava!-brez-tabele!) → Pag.-1-=-s2-TOP-=-m18-'1873-Juni-11' (očesi+VLM-2:1!-pass1-'Nov-8'-ZAVRŽEN!) — knjiga-se-odpira-**SREDI-ŠTEVILČENJA-1873**: vpisi-m1–m17-1873-NISO-V-TEJ-KNJIGI (nadaljevanje-iz-predhodnika!)-1873-=-SAMO-m18–m21! + 1873-kontekst: m18-=-Griblje-13-[~62!]-×-Maria-HRIŽAN-[62~66]-POLNI-DVOJNI-KANDIDAT-1873!-m19-=-podpis-'Dames-FERCHER' [~X-OPEN]-2.-duhovnik!-m20-=-**Johann-MILEK-GRIBLJE-[22~26]-×-Maria-POZDIRC/[~PEGDIRC]-GRIBLJE-[50~51]-POLNI-DVOJNI!**-PEZDIRC-že-1873!",
  knjiznoEn:
    "★★★ NEW-STRUCTURAL-EVIDENCE — THE-BOOK-OPENING-04455: s1-=-the-BOOK-COVER → Pag.-1-=-s2-TOP-=-m18-'Jun-11-1873' (2:1!-the-pass1-'Nov-8'-REJECTED!) — the-book-opens-MID-NUMBERING-of-1873: entries-m1–m17-are-NOT-IN-THIS-BOOK (continuation-from-a-predecessor!)-1873-=-ONLY-m18–m21! + the-1873-context: m18-=-the-FULL-DOUBLE-CANDIDATE-GRIBLJE-13-×-HRIŽAN!-m19-=-the-'Dames-FERCHER'-signature!-m20-=-**Johann-MILEK-GRIBLJE-×-Maria-PEGDIRC-GRIBLJE-FULL-DOUBLE!**-PEZDIRC-already-1873!",
  tailSi:
    "★★★ MEJA-1873/74 = s2-MID/DNO = 13.-MEJNA-VARIANTA (tail-1873-=-s2-margine-18–21-(11.-Juni–26.-Novembris-1873!)-→-RESTART-m1-NA-ISTI-STRANI-dno!-brez-finis!-brez-velike-glave!) · ★★★ MEJA-1874/75 = s7→s8-P249-1:1-RE-VERIFIKACIJA (finis-'f-i-n-i-s-/-1-8-7-4'-4.-instance-SODA-vzorec!-m32-=-18.-November!) · ★★★ P249-KOREKCIJA: m28-'28.-Februar'-MISREAD-→-**'28.-Avgust-1874'-1:1-KROP** (kronologija-m26/27-'5.-August'→m28-SKLAD!-+ Befunde-'23./8.-Aug'-PRED-poroko!-+ NADEL-POPPRAVEK-rjavo-'23.-Aug'→vijolično-'28.-Aug'-cf.-P242-v9!-m28-=-Josef-BAJUK-Primostek-[12~16]-25-l-×-NI-blok!-★-m29–m31-P249-leta-'8.-März'-'21.-April'-'21.-Mai'-kronološko-nemogoče-po-'28.-Aug'→[~X-OPEN-P251+-re-verifikacija!])",
  tailEn:
    "★★★ THE-1873/74-BOUNDARY = s2-MID/BOTTOM = the-13th-VARIANT (the-tail-on-the-same-page!) · ★★★ THE-1874/75-BOUNDARY = s7→s8-P249-RE-VERIFIED (the-finis-4th-instance!-m32-=-Nov-18!) · ★★★ THE-P249-CORRECTION: m28-'Feb-28'-MISREAD-→-**'Aug-28-1874'-1:1** (chronology-FITS!-+ the-NADEL-CORRECTION-brown-'23.'→violet-'28.-Aug'-cf.-P242-v9!)",
} as const;

/** Številčenje 1874 (s2-dno-1 · s3-2–6 · s4-7–11 · s5-12–18 · s6-19–27 · s7-28–32-P249!) — 32-vpisov-BREZ-preskokov-9.-leto! */
export const MARRIAGE_1874_NUMBERING =
  "s2-=-m1-DNO-restart-·-s3-=-2–6-·-s4-=-7–11-·-s5-=-12–18-·-s6-=-19–27-·-s7-=-28–32-P249!-— **32-VPISOV-BREZ-PRESKOKOV-9.-leto-zapored** (P249-napoved-'1–27'-FALSIFICIRANA!-NODAT-×0-5.-leto!-margine-modro-sivo-6.-leto!-m3-datum-celica-=-samo-'28'-BREZ-meseca-MESEC-SAMO-OB-SPREMEMBI-vzorec!)";

/** ★★★★★ FOLIACIJA-1874-'Pag = sken−1'-5/5 (s2-'Pag. 1' + s3-'Pag. 2' + s4-'Pag. 3' + s5-'Pag. 4' + s6-'Pag. 5'!-VSE-1:1-očesa+VLM!) — 28/28-v-zaporednih-letih-7.-leto! */
export const FOLIACIJA_1874 =
  "s2-'Pag. 1'-1:1-+ s3-'Pag. 2'-1:1-+ s4-'Pag. 3'-1:1-+ s5-'Pag. 4'-1:1-+ s6-'Pag. 5'-1:1-(očesa-+pass-1-DVOKRAT!-+ s1-vezalo-brez-Pag!)= 5/5-1874!-→ skupaj-z-4/4-1875-+ 4/4-1876-+ 4/4-1877-+ 6/6-1878-+ 5/5-1879-+ 4/4-1880 = 28/28-v-zaporednih-letih-7.-leto (+1873-kontekst-s2–s7-6/6!)";

/** ★★★ 3-MNOŽIČNI-POROČNI-DANI-v-1-letu: '8. Februar' ×5 (m7–m11!) + '11. Februar' ×5 (m12–m16!-mikro-6×-×3-m12/m13/m14!) + '14. Juni' ×2 (m24–m25!) = 10-porok-v-2-dneh! */
export const MNOZICNI_DANI_1874 =
  "'8. Februar 1874'-×5-(m7–m11-VSE-'8.'-1:1!)-+-'11. Februar 1874'-×5-(m12–m16-'11.'-mikro-6×-m12/m13/m14-1:1-×3!-Kurrent-'4'-odprti-vrh-vs-'874'-referenca!)-+-'14. Juni'-×2-(m24–m25!)-= 10-POROK-V-2-DNEH (cf.-P249-'4.-Februar'-×10-1-dan!-vzorec-3.-leto!-+ m12-DATE-DUEL-'Jänner-11'-očesi/pass1-→-'11.-Februar'-KROP-1:1-kronologija-VSILJUJE!-+ prečrtan-'Jänner'-ostanek-[~X-OPEN-pisarski-popravek-cf.-P242-v9!])";

/** ★★★★★ 10-DVIGOV-V-1-LETU-REKORD (prej-6-P248!) — h43-34-let-NOV-ABSOLUTNI-REKORD-DVIGA! */
export const FIRSTYEAR_1874_REKORDI =
  "h4-1881→1874-ZA-7-LET-+ h7-1889→1874-ZA-15-LET-+ h10-1877→1874-ZA-3-LET-+ h27-1881→1874-ZA-7-LET-+ h29-1897→1874-ZA-23-LET-IZENAČUJE-h44-P248-+ h30-1876→1874-ZA-2-LET-+ h33-1888→1874-ZA-14-LET-+ h42-1879→1874-ZA-5-LET-PROMOCIJA!-+ h43-1908→1874-ZA-34-LET-**NOV-ABSOLUTNI-REKORD-DVIGA**-+ h65-1886→1874-ZA-12-LET = 10-DVIGOV-V-1-LETU (prej-6-P248!-×1.67!)";

/** ★ H43-BRULA-PARALELA-1:1 (Marina-1874 == Katharina-1878-P246-bride-KONTEKST!-ISTA-HIŠA-ISTA-PRIIMEK!-'43'-forenzika-8×!) + h42-PROMOCIJA-NAPAVED-IZPOLNJENA! */
export const H43_1874_PARALELA =
  "Marina-[~Martin!]-BRULA-27-l-GRIBLJE 43-1874-m25-==-Katharina-BRULA-1878-P246-v5-bride-KONTEKST (ISTA-HIŠA-h43-ISTA-PRIIMEK!-hišna-'43'-ultra-8×-Kurrent-'4'-odprti-vrh-NE-'93'/'33'!-P249-h42-vzorec-2.-instance-cf.-P248-h30!)-+ h42-m32-Maria-PEGDIRC-PROMOCIJA (NAPAVED-P250-IZPOLNJENA!-h42-PARALELA-z-Georg-Pegdirc-1879-P244-v21!)";

/** ★★★ HRIŽAN-×4 + MILEK-×3 v 1 letu! */
export const HRIZAN_MILEK_1874 =
  "HRIŽAN-×4-omemb-v-1-letu (m5-mati-Maria-Hrižan!-+ m6-nevesta-Katharina-Hrižan-GRIBLJE 4-BLOK!-+ m10-nevesta-Anna-Hrižan-×-h27-BLOK!-+ m22-ženin-Joseph-Hrižan-63-l-[Pribež-P-forenzika-NI-Griblje!]-cf.-P246-'×3-BLOKI'-1874-=-×2-BLOKI-+ ×2-kontekst!)-+ MILEK-×3-V-1-LETU (m5-ženin-h65-BLOK-+ m16-ženin-h29-BLOK-+ m16-priča-Marcus-MILEK!-+ 1873-kontekst-m20-Johann-MILEK-×-PEGDIRC!)-MILIČ-križ-cf.-P248!";

/** ★★★ DOVGAN-KONTINUUM-PODALJŠAN-NA-12-LET (1874–1885!) — izjemi ×2! */
export const DOVGAN_1874_PODALJŠITEV =
  "Franz-Dovgan-podpisi-NA-VSIH-glavnih-vrstah-s2–s6-(m1–m27!)-+ s7-tail-P249!-garble-'Dorgor/Dorgan'!-kontinuum-**1874–1885-=-12-LET** (P249-'11-let'-PODALJŠAN-ZA-1-LETO-NAZAJ!)-IZJEMI-×2: (a)-m27-podpis-'[Justinius?]-HEGRIČ'-[~X-OPEN]-na-REDNEM-vpisu (cf.-P248-kaplan-Perschek-na-NAKNADNEM-violet!-NOV-vzorec!)-+ (b)-1873-kontekst-m19-'Dames-FERCHER' [~X-OPEN]-že-v-prvi-tabeli-knjige = 3-duhovniki-kontekst!";

/** m17-nevesta 52 l = NAJSTAREJŠA-nevesta-predzgodovine (prej 46 P249!) + 63-l-ženin ×2 + mladoletnici ×2! */
export const STAROSTI_1874 =
  "**m17-Anna-Vipavec-52-l-NAJSTAREJŠA-NEVESTA-PREDZGOVINE-REKORD** (prej-P249-v13-Katharina-Stubler-46!-+ m16-50-l-+ m22-48-l-+ m15-40-l!)-+ **63-l-ŽENIN-×2-V-1-LETU** (m10-Jacob-[Skulhan~Brikhan]-h27-+ m22-Joseph-Hrižan-[Pribež!]-cf.-P243-v11-'69'-[~X-OPEN]!)-+ MLADOLETNICA-×2-POTRJENA (m5-19-l-Konsens-st.-Minderjährig-der-Braut-k.k.-31.-Jänner!-+ m18-Maria-Jurajevič-17-l!)-+ m23-ženin-22-l-[~]-+ m1-WITWA-Z-OTROKI-[~]-+ m16/m26/m27-WITVE!";

/** P249-KOREKCIJE + krops-metodika (pasma-artefakti!-forenzika!) — P250-metoda. */
export const MARRIAGE_1874_METODA =
  "7-skenov-s1–s7-md5-7/7 (s7-križna-md5-2.-neodvisen-prenos-1:1-identičen-P249-disku-4d5ef99c!-s1-vezalo-1664×1800!) + Read-očesi-NAJPREJ-×7-P244-LEKCIJA (restart-s2-dno-najden-NA-OČESA!) + VLM-pass-1-×5-5/5-1.-poskus + krops-×48-+ pass-2b/2c/2d/2e/2f-korektne-pasme-×35 (očesi-na-krops-razkrila-pasme-zamik-×4!-s4-'Črneč-14'-artefakt-=-m11-'Premez 14'!-s6-komprimirane-vrstice!-s2-m1-pri-0.66!)+ solo-klici-×6-KRITIČNI + serije-×13 + mikro-forenzika-8×-×3 (m5-hiša-'65'-MILEK-P246-1:1!-m5-starost-'19'-'9'-z-repkom!-m25-hiša-'43'-BRULA-'4'-odprti-vrh!) + letterform-forenzika ('3'-dvojna-zanka-vs-'5'-enojna+kavelj!-'P'-vs-'G'-m22!-'1'-vs-'4'-m12!-'9'-z-repkom!-'2'-vs-'3'-m14-[X-OPEN]!) + reconciliacija-z-P249-tail (m28-KOREKCIJA!-m32-PROMOCIJA!) + hišna-sinhronizacija (h65-MILEK-P246-ODLOČILNA!) + pasme-artefakti-DOKUMENTIRANI ('Griblje-27'-vs-'Milozze'-vs-'Črneč-14'!-'Gribje-33'-vs-'Bojmavas 14'!)";

/** MARRIAGE_1874_DUELS — glavni dueli (rešeni + odprti pošteno). */
export const MARRIAGE_1874_DUELS = [
  "m12-datum-'Jänner-11'-očesi+pass1-vs-'11.-Februar'-KROP+kronologija-REŠEN-3:1-(+ prečrtan-'Jänner'-ostanek-[~X-OPEN-pisarski-popravek!]!)",
  "m5-hiša-'63'-očesi1+K-solo-4/5-vs-'65'-ultra-8×-forenzika+P246-MILEK-SKLAD-REŠEN-2:1!",
  "m6-nevesta-starost-'16'-očesi-vs-'26'-mikro+pass1-REŠEN-2:1-NI-mladoletnica!",
  "m22-wn-'Griblje'-očesi1-vs-'Pribež'-'P'-forenzika-K-solo+mikro-REŠEN-2:1-NI-blok-pošteno!",
  "m25-bride-wn-'33'-očesi1-vs-'93'-pass1-vs-'43'-ultra-8×-Kurrent-'4'+P246-BRULA-SKLAD-REŠEN!",
  "m25-bride-ime-'Anna'-očesi-vs-'Marina'-pass1+mikro-2:1-[~Martin-DUEL-ostaja-pošteno!]",
  "m25-ženin-ime-'Vlašič'-pass1-vs-'Rotte'-očesi-vs-'Gmeind-Vorsteher'-mikro-X-OPEN-3-branja!",
  "m14-starost-'23'-pass1+očesi-vs-'33'-X-OPEN-ostaja!-+ m14-bride-wn-'Uranoviče~Crnaviče~Hrastovice'-[14~19]-X-OPEN!",
  "m28-datum-'28.-Februar'-P249-vs-'28.-Avgust'-KROP+Befunde-chronologija-REŠEN-P249-KOREKCIJA!",
  "m1-datum-'19'-očesi-vs-'18'-pass1-X-OPEN!",
  "m16-groom-'Johann-Milek'-mikro-1:1-vs-'Verček'-pass1-vs-'Hafell'-serija-pasme-artefakt-REŠEN!",
  "m10-groom-'Skulhan~Brikhan~Kruhar'-3-branja-X-OPEN!",
  "m7-groom-'Hvalič'-pass1/batch-vs-'Hrovalj'-očesi-vs-'Hralj'-eltern-X-OPEN!-+ m26-'Johann-HRAUJ/HROVALJ'-mikro-1:1-H-jasna!-HROVALJ-nit-×2-kand.!",
  "m26-bride-'Maria-geb./w.-Hambič'-mikro-×2-vs-'Kraml'-pass1-vs-'Smuklič'-očesi-REŠEN-2:1-[Witwa-vs-geb.-X-OPEN]!",
  "m18-wn-'Otok~Stokl'-X-OPEN-(oba-ženi n-nevesta-para!)",
  "m1-wn-'Kramarše~?'-vs-'Vrhovlje'-pass1-X-OPEN!",
  "m3-datum-celica-'28'-BREZ-meseca-VLM-'Februar'-hallucinacija-ZAVRŽENA-kronologija-vsiljuje-'Jänner'-[~]!",
] as const;

/** MARRIAGE_1874_KONTEKST — ni-bloki-pošteno (1874 + 1873-tail!). */
export const MARRIAGE_1874_KONTEKST = [
  "m1-19.[~18.]-Jänner-Jakob-PAŠIČ-34-l-[Kramarše~?]-4-×-Anna-KUNIČ-34-l-WITWA-Z-OTROKI-[~]-zettel-[8~3.]-Jänner-RESTART-NI-blok",
  "m2-28.-Jänner-Johann-ORLIČ-25-l-[Hrastje~Skavin?]-14-×-Maria-[Hügel~Engel]-19-l-Dobrave-9-Möttling-pripis-dd.-26.-Jänner!-+ Consens-17.-Jänner!-NI-blok",
  "m3-28.[Jänner~]-Georg-[Grabowiec~]-27-l-[Cerhovice~]-[5~7]-×-Katharina-KRALJ-18-l-Mlake-10-zettel-Podzemelj-28.-Jänner-NI-blok",
  "m4-2.-Februar-Jakob-[Engel~]-39-l-[Vriho-glavce~]-31-×-Maria-[Rus~]-24-l-[Pudlo-vica~]-NI-blok",
  "m7-8.-Februar-Mathias-[Hvalič~Hrovalj~Hralj]-48-l-Boršt-[17~19]-×-Maria-[Šilah~Miklah~Filah]-19-l-Geriče-1-★ elternBride-Michael-ŠILAH-×-Kath.-Jaklič-(cf.-h34-SILAH-P247!)-NI-blok",
  "m8-8.-Februar-Georg-[Hvalič~Hralj]-Tischler-28-l-[Kapl.-9~]-×-Katharina-PLEH-24-l-Dolenec-42-NI-blok",
  "m9-8.-Februar-Peter-[Mušič~]-40-l-[Grendal~]-×-Maria-OGULIN-25-l-Gradac-1-NI-blok",
  "m11-8.-Februar-Marcus-Bertogneć-38-l-Premez-14-×-Anna-TASIČ-23-l-Begine-12-Möttling-dd.-27.-Jänner!-NI-blok",
  "m12-11.-Februar-Georg-SEGINA-24-l-[Pritlze~Milozze]-28-×-Katharina-KLEPEC-19-l-Boršt-21-NI-blok (SEGINA-×1!)",
  "m13-11.-Februar-Joseph-[Zeličko~]-31-l-[Orlova~Cerovice]-[16~18]-×-Katharina-[Herbanec~]-19-l-**KLOSTER-40**-(cf.-P247-'Klo-šter'-diskusija!)-NI-blok",
  "m18-26.-Februar-Nikolaus-ZUGELJ-30-l-½-Hübl-[Otok~Stokl]-18-×-Maria-JURAJEVIČ-17-l-[Otok~Stokl]-9-starši-n.-†Miha-Jurajevič-×-Anna-**ZUGELJ**-NI-blok",
  "m19-19.-April-Heinrich-[Telesnik~]-42-l-Gradac-1-×-Maria-[Horosec~Horvat]-22-l-Gradac-51-zettel-Vinica-15.-April-[~]-NI-blok",
  "m20-3.-Mai-Joseph-[Perdese~Gerdesić]-34-l-[Črnomelj~Cerhovice]-5-×-Maria-MIHELČIČ-24-l-[Črnomelj-24~Cerhovce-35]-NI-blok",
  "m21-3.-Mai-Franz-Sopčič-32-l-Rtiče-5-×-[Katharina~Barbara]-POŽEG-24-l-[Podljune~Dobrinovo]-14-zettel-[Primostek~Adlešiči]-25.-Apr-NI-blok",
  "m22-17.-Mai-Joseph-HRIŽAN-Weber-**63-l**-[Pribež-P-forenzika!]-×-Anna-HLEBEC-48-l-[Temelj~Kemel]-11-(+2.-vrstica-'[Griboie~Griblje?]-№25'-[~X-OPEN!])-zettel-'Griblje-4.-Mai'-[~]-NI-blok",
  "m23-17.-Mai-Marko-ČERNIČ-22-l-MLADOLETNIK-[~]-[Ceroviše~]-22-×-Maria-[Butkovec~Hrušič]-28-l-[Ceroviše~]-11-zettel-Adlešiči-15.-Mai-NI-blok",
  "m24-14.-Juni-Georg-GRABRIJAN-45-l-Ceroviše-25-×-Apollonia-[Zimrec~]-[44~49]-l-Ceroviše-1-'oba-vdova/vdovec?'-[~]-NI-blok",
  "m26-5.-Aug-Johann-HROVALJ-[~Hrauj!]-28-l-Mlake-10-×-Maria-[Witwa~geb.]-HAMBIČ-[~24~26]-l-[Boginjevas~Boginove]-14-starši-ž.-†Georg-Hrovalj-×-Anna-Jaklič-prečrtan-prvotni-datum!-NI-blok (HROVALJ-×2-kand.-z-m7!)",
  "m27-5.-Aug-Jacob-KRIŽE-37-l-Gradac-1-×-Helena-FERWIGA-33-l-WITWA-Gradac-16-podpis-'[Justinius?]-HEGRIČ' [~X-OPEN]-zettel-Gradac-25.-Juni-NI-blok",
  "m28-28.-Aug-POPPRAVEK-rjavo-'23.'-Josef-BAJUK-25-l-Primostek-[12~16]-×-[Katharina-Angelj-batch-konflacija~Maria-Pavč-Keržan-Toma-P249]-[Dobraviče~Dobravlje]-24-l-NI-blok",
  "TAIL-1873-s2-kontekst-NI-bloki-pošteno (v-04455!): m18-11.-Juni-1873-Mathias-Gahofčič-[~Jahnssepić!]-GRIBLJE-13-42-l-×-Maria-HRIŽAN-GRIBLJE-[62~66]-32-l-POLNI-DVOJNI-KANDIDAT-1873!-+ m19-23.-Sept-Josef-[Gloser~]-Klagenfurt-34-l-×-Maria-[Ema-Augustina-Homolsch~]-19-l-Gradac-1-podpis-'Dames-FERCHER'!-+ m20-5.-Dez-Johann-MILEK-34-l-GRIBLJE-[22~26]-×-Maria-POZDIRC/[~PEGDIRC]-26-l-GRIBLJE-[50~51]-POLNI-DVOJNI-★-PEZDIRC!-+ m21-26.-Dez-Mathias-Gahofčič-32-l-Certovica-12-×-Maria-Gahofčič-22-l-Certovica-10",
] as const;

/** Vse-nove-1874-meritve-v-obliki-za-QA (skupaj-04455: 254→265 · vitals: 1997→2008 · sidra: 247→258-1874:11! · dobe: 221→232-62-pred-linijskih!). */
export const MARRIAGE_1874_KORPUS = {
  skupaj04455: 265,
  skupajVitals: 2008,
  sidra: 258,
  dobe: 232,
} as const;

/** ————— P251 — POROČNA PREDZGOVINA 04455, leto 1873 = 13/13 KONČNO (ZAKLJUČEK predzgodovine!) ————— */

/** m18–m21 = TAIL 1873 na Pag. 1 (s2): 4 vpisi, m1–m17 v predhodniku-knjigi. Griblje bloki: m18 (h13×h62-POLNI-DVOJNI!) + m20 (h22×h50-POLNI-DVOJNI!) = 4 hiše / 2 bloka-polna-dvojna. */
export const MARRIAGE_1873_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "04455" && h.year === 1873,
);
export const MARRIAGE_1873_GRIBLJE = MARRIAGE_1873_BLOCKS.length;
export const MARRIAGE_1873_HOUSES = MARRIAGE_1873_BLOCKS.map((h) => h.houseNo);
export const MARRIAGE_1873_TOTAL = 4;

/** KONČNO-potrditev knjižnega odpiranja (P250-napoved-IZPOLNJENA): s1 = vezalo (nalepka '…KNJIGA' [?], brez naslovnice/pečatov!) → s2 = 'Pag. 1' = prva tabelarna stran z marginalo **18** = m1–m17-1873-NISO-v-tej-knjigi! + meja-1873/74 = s2-MID/DNO re-verifikacija (m1 = Wranovič 14 obé!). */
export const KNIŽNO_ODPIRANJE_1873 = {
  si: "★★★ KONČNA-POTRDITEV-P251: s1-vezalo (arhivska-nalepka-'…KNJIGA'-[?]-brez-naslovnice/pečatov!) → s2-'Pag. 1'-prva-tabelarna-stran-prva-marginala-**18** = m1–m17-1873-NISO-V-TEJ-KNJIGI (predhodnik!) — 1873-SAMO-m18–m21 (4-vpisi!) — PREDZGOVINA-13/13-ZAKLJUČENA · m1-1874-očesi-re: Jakob-PAŠIČ-×-Anna-KUNIČ-OBÉ-'Wranovič-14' [~VRANOVIČI!]-P250-'Kramarše~?'-kand.-RAZREŠEN!",
  en: "★★★ THE-P251-FINAL-CONFIRMATION: s1-=-the-BOOK-COVER (archive-label-'…KNJIGA'-[?]-no-title-page/seals!) → s2-'Pag. 1'-the-FIRST-table-page-the-first-margin-number-**18** = m1–m17-1873-are-NOT-IN-THIS-BOOK (a-predecessor!) — 1873-ONLY-m18–m21 (4-entries!) — THE-PREHISTORY-13/13-COMPLETE · m1-1874-eyes-re: Jakob-PAŠIČ-×-Anna-KUNIČ-BOTH-'Wranovič-14' [~VRANOVIČI!]-the-P250-'Kramarše~?'-candidate-RESOLVED!",
} as const;

/** Meje-1873-re: 13.-VARIANTA-1:1-očesi + foliacija Pag. 1 = sken−1 = 29/29 (8. leto!) + številčenje 18–21 nakladalno iz predhodnika + NODAT-×0-6.-leto. */
export const MARRIAGE_1873_MEJA = {
  si: "★★★ MEJA-1873/74 = s2-MID/DNO = 13.-VARIANTA-1:1-RE-VERIFIKACIJA-očesi (m21-'26.-Novembris'→m1-'1874 Jänner [19~18-DUEL!]'-NA-ISTI-STRANI!) · ★★★★★ FOLIACIJA-'Pag-=-sken−1'-1/1-1873 (s2-'Pag. 1'!) → SKUPAJ-29/29-V-ZAPOREDNIH-LETIH-8.-LETO (pravilo-drži-tudi-NA-ODPIRANJU!) · številčenje: marginala-18–21-nakladalno-iz-predhodnika-BREZ-preskokov-v-vidnem-delu · NODAT-×0-6.-LETO!",
  en: "★★★ THE-1873/74-BOUNDARY-=-s2-MID/BOTTOM-=-the-13th-VARIANT-1:1-EYES-RE-VERIFIED · ★★★★★ FOLIATION-'Pag-=-sken−1'-1/1-1873 → 29/29-TOTAL-ACROSS-CONSECUTIVE-YEARS-THE-8th-YEAR (the-rule-HOLDS-EVEN-AT-THE-BOOK-OPENING!) · numbering: margins-18–21-continuing-from-the-predecessor-NO-gaps-in-the-visible-part · NODAT-×0-THE-6th-YEAR!",
} as const;

/** ★★★★★ 4 DVIGI-V-1-LETU-ZAKLJUČEK: h22-ZA-25-LET (2.-NAJVEČJI-za-h44-23!) · h62-ZA-20-LET (3.!) · h13-ZA-9-LET · h50-ZA-6-LET. */
export const FIRSTYEAR_1873_DVIGI = {
  si: "★★★★★ 4-DVIGI-V-1-LETU-ZAKLJUČEK-PREDZGOVINE: h22-04455-firstYear-1898→1873-DVIG-ZA-25-LET (2.-NAJVEČJI-v-predzgodovini-za-h44-23-P248!-Johann-MILEK-Innmann!) + h62-1893→1873-ZA-20-LET (3.!-Maria-HRIŽAN!-h62-že-5-blokov-1893–1908!) + h13-1882→1873-ZA-9-LET (P241-continuum!) + h50-1879→1873-ZA-6-LET (P244-Pezdirc!) — cf.-P250-10-DVIGOV-REKORD!",
  en: "★★★★★ 4-FIRSTYEAR-RISES-IN-1-YEAR-THE-PREHISTORY-FINALE: h22-1898→1873-BY-25-YEARS (the-2nd-BIGGEST-in-prehistory-after-h44-23!) + h62-1893→1873-BY-20 (the-3rd!) + h13-1882→1873-BY-9 + h50-1879→1873-BY-6 — cf.-the-P250-10-rises-record!",
} as const;

/** ★★★★★ DOVGAN-continuum-PODALJŠAN-NA-13-LET (1873–1885!) — podpisi že na odpiranju knjige (m18+m20+m21, isti roka ×3!). */
export const DOVGAN_1873_ZAČETEK = {
  si: "★★★★★ DOVGAN-CONTINUUM-PODALJŠAN-NA-13-LET (1873–1885!): m18+m20+m21 = 'Franz-Dovgan' (solo-VLM-'D'-z-zanko-'-gan'-konec-ZAVRŽEN-'Vogran'-duel!-isti-roka-×3-parafa-'M.'!) — P250-'12-LET'-PODALJŠAN-ZA-1-LETO-NAZAJ-NA-ODPIRANJE-KNJIGE!-izjemi-×2: m19-'Daniel-TERŽEK' [~Teršek; cf.-P250-'Dames-FERCHER'-MISREAD-kand.-X-OPEN!-6×-krop-'T'-z-vodoravno-'z/ž'-zanka-'-ek'-konec!]-+'Hegrič'-1884-m27 [~X-OPEN]",
  en: "★★★★★ THE-DOVGAN-CONTINUUM-EXTENDED-TO-13-YEARS (1873–1885!): signatures-already-at-the-book-opening (m18+m20+m21-=-same-hand-×3!) — the-P250-'12-YEARS'-EXTENDED-BY-1-YEAR-BACK!-exceptions-×2: m19-'Daniel-TERŽEK' [~cf.-P250-'FERCHER'-MISREAD-candidate!]-+'Hegrič'-1884!",
} as const;

/** ★★★★★ PEZDIRC-marriage-continuum 1873–1885 = 13/13 let VSEH — Maria PEGDIRE (h50, oče Marcus!) že na odpiranju. */
export const PEZDIRC_1873_ODPIRANJE = {
  si: "★★★★★ PEZDIRC-MARRIAGE-CONTINUUM-1873–1885-=-13/13-LET-VSEH (cf.-krstna-04104-PEZDIRC-×131-edini-v-vseh-15-letih!): m20-NEVESTA-Maria-PEGDIRE-GRIBLJE-50 (oče-Marcus-PEGDIRE-mikro-1:1-'Pegdire'-NE-'Pozdič'!) = PEZDIRC-že-NA-ODPIRANJU-knjige — P249-napoved-'PEZDIRC-že-1873!'-IZPOLNJENA-KOT-BLOK!-+ P250-dueli-'[50~51]'→50!-'POZDIRC'→PEGDIRE!",
  en: "★★★★★ THE-PEZDIRC-MARRIAGE-CONTINUUM-1873–1885-=-13/13-YEARS-ALL: bride-Maria-PEGDIRE-GRIBLJE-50 (father-Marcus!) = PEZDIRC-already-AT-THE-BOOK-OPENING — the-P249-forecast-FULFILLED-AS-A-BLOCK!",
} as const;

/** 2 POLNA-DVOJNA-v-4-vpisih (50%-količnik-REKORD!) + MILEK-nit + HRIŽAN-×3 + ŠIMEC-×3 + KUNIČ-križ-×3 + Klagenfurt-migrant + istoimenski-par + Vetrhvišče-X-OPEN. */
export const MARRIAGE_1873_NITI = {
  si: "★★★ 2-POLNA-DVOJNA-V-4-VPISIH-=-50%-količnik-REKORD-predzgovine (h13×h62-+-h22×h50!-cf.-P250-2-v-11!) · ★★★ MILEK-×2-v-1-letu-1873 (m20-ženin-Johann-h22-NOVA-Milek-hiša-≠-h65-Mathias-P246/P250!-+ m18-mati-Maria-Milek!-h65-PARALELA!) · ★★★ HRIŽAN-×3 (m18-nevesta-+ m18-oče-Mathias-+ m20-priča-Marcus!) · ★★★ ŠIMEC-×3 (m18-mati-Barbara-+ m20-mati-Anna-+ m20-priča-Anton!) · ★★★ KUNIČ-križ-×3 (m21-mati-+ priča-Mathias-+ 1874-m1-Anna-kontekst!) · ★★★ MIGRANT-KLAGENFURT-'von-Josef-Narzis-IBERER-h.h.-Leining-genannt…' [X-OPEN]-uradnik/plemič-vzorec-1.-TE-VRSTE (m19!-cf.-P248-Lingl-Graz-P249-Šolnar-Ribnica!)-+ m19-MÖTTLING-pripis + priča-Martin-JUBARZ + nevesta-'Maria-Eva-Auguška-HOMOLSCH' [~Homolitsch-'Stomašek'-RAZREŠEN!]-mati-'Maria-JEZERNIK' [~Jeßernig!] · ★★★ ISTOIMENSKI-PAR-m21 (Mathias-[J/G]abovšič-×-Maria-GABOFAIČ [~]-cf.-P246-IZMENA-VLOG!)-'VETRHVIŠČE'-12-×-10 [X-OPEN-VAS!]",
  en: "★★★ 2-FULL-DOUBLES-IN-4-ENTRIES-=-50%-RATIO-RECORD (h13×h62-+-h22×h50!) · MILEK-×2 (h22-NEW-Milek-house-≠-h65!-+ mother-Maria-Milek!) · HRIŽAN-×3 · ŠIMEC-×3 · KUNIČ-cross-×3 · KLAGENFURT-MIGRANT-'von-Josef-Narzis-IBERER-h.h.-Leining-genannt…' [X-OPEN]-official/noble-pattern-the-1st-OF-ITS-KIND (m19!)-+ MÖTTLING-note + witness-Martin-JUBARZ + bride-'Maria-Eva-Auguška-HOMOLSCH'-mother-'Maria-JEZERNIK' · ISTOIMENSKI-PAR-m21-'VETRHVIŠČE'-12-×-10 [X-OPEN-VILLAGE!]",
} as const;

/** Datumi-1873-končno: 4-brez-duelov + m19-'Augst. 23.'-kronološko-rešeno. */
export const DATUMI_1873 = {
  si: "4-datumov-BREZ-duelov-v-končnem-stanju: m18-'1873 Juni 11.'-letnica-samo-na-vrhu-stolpca-1× · m19-'Augst. 23.'-[očesi-7×-'Augst'-=avgust!-kronologija-Juni<Aug<Nov-SKLAD!-pass1-'avgust'-2:1!-'Jänner'-očesna-zamik-RAZREŠENA!] · m20-'Novem(b). 5.' · m21-'26. Nov(emb).' — m1-1874-'[19~18]-DUEL'-X-OPEN-pošteno (P250-19!-očesi-'18.'-Kurrent-9~8-11×!)",
  en: "4-dates-NO-duels-in-the-final-state · m19-'Augst. 23.'-chronology-RESOLVED (Juni<Aug<Nov-FITS!) · m1-1874-'[19~18]-DUEL'-X-OPEN-honestly",
} as const;

/** Metoda P251: 2 skena + s3-križna, md5 2× neodvisen 1:1, očesi-NAJPREJ, VLM-pass-1 ×2, solo ×12, očesi-deciser ×6. */
export const MARRIAGE_1873_METODA =
  "2-skena-s1–s2-(+s3-križna-meja)-md5-2×-neodvisen-prenos-1:1 (s1-ad8dac44…-s2-e5e80851…-s3-2618ab67…!-inventar-192-URL-base64-dekodiran!) + Read-očesi-NAJPREJ-×2-strani-P244-LEKCIJA (knjižno-odpiranje-18-NA-OČESA!-Pag.-1!) + VLM-pass-1-×2 (s1-vezalo-specialni-+ s2-polni-prepis!-2/2-1.-poskus!) + solo-krops-×7 (priest-compare-3-image!-m18-bride-m20-groom-m21-vase-m18-groom-m19-groom!) + solo2-zoomi-×5 (m19-priest-6×!-m20-ghouse-6×!-m21-bname-5×!-m19-bride-4×!-m18-bhouse-6×-MIS!) + očesi-deciser-×6 (m18_bhouse-5×!-m19_bridecell-5×!-m19_gname-5×!-m19_gw-6×!-m19_date-7×!-m20_growcell-4×!-m18_bnum-11×-2×!) + mikro-forenzika-letterform ('2'-vs-'3'-'b'-referenca-m20-'22'!-'H'-vs-'K'-'D'-vs-'V'-'F'-vs-'T'!) + kronološka-verifikacija (Juni<Aug<Nov-SKLAD!) + reconciliacija-z-P250-tail";

/** Vse-nove-1873-meritve-v-obliki-za-QA (skupaj-04455: 265→269 · vitals: 2008→2012 · sidra: 258→262-1873:4! · dobe: 232→236-66-pred-linijskih!). */
export const MARRIAGE_1873_KORPUS = {
  skupaj04455: 269,
  skupajVitals: 2012,
  sidra: 262,
  dobe: 236,
} as const;


// ——— P253: PREDHODNIK-KNJIGE-04455 = 01738 (Poročna 1828–1873) — leto 1873 m1–m17 + ŠIV-MED-KNJIGAMA! ———
/** m1–m17 = leto 1873 v PREDHODNIKU (01738): 29. 1.–25. 5. 1873 — meja z m18 (11. 6. 1873, 04455 'Pag. 1') = ŠIV-MED-KNJIGAMA! */
export const PREDHODNIK_1873_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "01738" && h.year === 1873,
);
export const PREDHODNIK_1873_HOUSES = PREDHODNIK_1873_BLOCKS.map((h) => h.houseNo);
export const PREDHODNIK_1873_TOTAL = 17;
export const PREDHODNIK_1873_BLOCKI = 11;

/** ★★★★★ ŠIV-MED-KNJIGAMA (s146 = zadnja stran 01738): zadnji FIZIČNI zapis = ISTI PAR kot 04455-m18! */
export const PREDHODNIK_1873_SEAM = {
  si: "★★★★★ ŠIV-MED-KNJIGAMA-FIZIČNO-DOKAZAN (P253!): s146 = ZADNJA-stran-01738 — zadnji-FIZIČNI-zapis-na-njej = Mathias-[Gabovšič-grable] (GRIBLJE 13!) × Maria HRIŽAN (GRIBLJE 62!) = ISTI-PAR-KOT-04455-'Pag. 1'-m18 (11. 6. 1873!!) — [~prekrižan?-X-OPEN]-začetek-VPISA-v-STARI-knigi → NADALJEVANJE-v-NOVI — štetje-17→18-TEČE-ČEZ-MEJO-KNJIG (1–21-leta-1873-SKUPAJ!) — P250/P251-'knjižno-odpiranje'-napoved-IZPOLNJENA-KOT-FIZIK! (seam3-zoom: hiša-13-1:1! · seam4-zoom: 'Griblje 62. Maria Hrižan'-1:1! · b1-datum-'Jün 11'-kand.)",
  en: "THE-BOOK-SEAM-PHYSICALLY-PROVEN (P253!): s146 = the-LAST-page-of-01738 — its-last-PHYSICAL-entry = the-SAME-COUPLE-as-04455's-'Pag. 1'-m18 (Jun 11, 1873!!) — the-entry-STARTED-in-the-OLD-book → CONTINUED-in-the-NEW — the-numbering-17→18-RUNS-ACROSS-the-book-boundary (1–21-for-1873-TOGETHER!) — the-P250/P251-book-opening-forecast-FULFILLED-PHYSICALLY!",
} as const;

/** RESTART-1873-z-1 + 1872-tail-26–29 + meja-1872/73 na s143 (aritmetična!). */
export const PREDHODNIK_1873_RESTART = {
  si: "★★★★★ RESTART-1873-z-1 (s143): 1872-štetje-26–29 (Nov-1872–Jänner-1873-tail!) → 1873-RESTARTA-z-m1 (29. Jänner 1873!) — MEJA-1872/73-NA-SAMI-STRANI (aritmetična!); m1–m17-17-VPISOV-BREZ-PRESKOKOV (29. 1.–25. 5. 1873) — kronologija-SKLAD-cf.-m18-11. 6.! · datumi: m1-29. 1. [24-DUEL-REŠEN-3:1!]-m2-3. 2.-m4-9. 2.-m5-[~10. 2]-m6-[~12. 2]-m7/m8/m9/m10-19. 2.-m11-[~18. 2]-m12/m13-[~19. 2]-m14-[~1. 3]-m15/m16-27. 4.-m17-25. 5. [~'März'-PREČRTANO-POPRAVLJENO-'Mai'!]",
  en: "THE-1873-RESTART-at-1 (s143): 1872's-tail-26–29 → 1873-restarts-at-m1 (Jan 29, 1873!) — the-1872/73-boundary-ON-ONE-PAGE; 17-entries-m1–m17-NO-gaps (Jan 29–May 25, 1873) — chronology-fits-m18-Jun-11!",
} as const;

/** PEZDIRC-nit-v-predhodniku + DOVGAN-vsi + POLNA-DVOJNA-m6 + bratje-Silak + h28-×2. */
export const PREDHODNIK_1873_NITI = {
  si: "★★★★★ PEZDIRC-NIT-V-PREDHODNIKU (m7-nevesta-Anna-PEZDIRC-oče-Martin!-[~+ m11-mati-'Pegdire' + m13/m14-Pegdirc/Legdire-garble-X-OPEN] — PEZDIRC-podaljšan-IZVEN-04455!) · ★★★★★ DOVGAN-PODPISUJE-VSE-m1–m17-+-1872-tail ([~Dergan-garble] — continuum-1872–1885!) · ★★★ POLNI-DVOJNI-m6 (h16-Kolbezen-×-h10-Muc!) + m3-[~h25×h18-DUEL] · ★★★ BRATJE-SILAK-m8×m9 (ISTA-starši-Mathias-Silak-+-Catharina!) · ★★★ h28-×2-DVOJNA (m2-ženin-MAVRIN-+-m4-nevesta-TOMC-ISTA-hiša-2-družini-cf.-krstna-1871!) · ★★★ MNOŽIČNI-DAN-19. 2.-×4-+[~6-kand.] + 27. 4.-×2 · MLADOLETNICE-m1-19-l-+-m11-18-l · ★★★ m12-POPRAVEK-h73←h13-PREČRTANO (pisarjev-popravek-cf.-P249-'21'!)",
  en: "the-PEZDIRC-thread-IN-THE-PREDECESSOR (m7-bride-Anna-PEZDIRC-father-Martin!) + DOVGAN-signs-ALL + the-FULL-DOUBLE-m6 (h16×h10!) + the-SILAK-BROTHERS-m8×m9 (same-parents!) + h28-×2 (m2+m4!) + Feb-19-×4 + Apr-27-×2 + the-minors + the-h73←h13-correction!",
} as const;

/** P253-korpus: 11 blokov / 17 vpisov; vitals 2012→2023; 01738 = nova knjiga v korpusu! */
export const PREDHODNIK_1873_KORPUS = {
  noviBloki: 11,
  vpisi: 17,
  skupaj1873: 21,
  vitalsTotal: 2023,
  byBook01738: 11,
} as const;
