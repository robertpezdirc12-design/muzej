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
