// parish-synthesis.ts — P236: SINTEZA KRSTNE PREDZGODOVINE 04104 (1871–1885 = 15/15!)
// Knjiga "PODZEMELJ-R-1871-1885" (nalepek 1:1!) je s P235 KOMPLETNO dokumentirana —
// ta modul združuje križnoletne niti, vzorce in X-open preostanke vseh 15 faz
// (P221 = 1885 … P235 = 1871). Vsi števci so preverljivi proti HOUSE_VITALS
// (parish.ts) — qa-p236 jih živi preverja; paleografski dokazi so v
// research/issue17/parish-baptism-<leto>-04104.json.

export interface BaptismYear {
  year: number;
  /** faza, ki je leto prebrala (P221 = 1885 … P235 = 1871) */
  phase: string;
  /** napredek branja linije tistega trenutka ("1/15" = 1885 je bil prvi prebran) */
  progress: string;
  /** skupno število vpisov v knjigi tisto leto (iz vrstne aritmetike, P-faza) */
  entries: number;
  /** prebrani Griblje-vpisi = bloki v parish.ts */
  griblje: number;
  /** različne Griblje-hiše tistega leta */
  houses: number;
  /** okvir skenov */
  scans: string;
  scanCount: number;
  /** foliacijska konvencija okna (pag/sken−3/sken−5/sken−6 + posebnosti) */
  foliation: string;
  /** meja s prejšnjim letom (naprej po knjigi) */
  boundaryNext: string;
  /** zaporedna potrditev invariante meje (60.–73.) */
  boundaryNo: number;
  /** restart-z1: dan · vas · hiša (vsi 15 let imajo restart!) */
  restart: string;
  highlights: string[];
}

/** 15 let knjige 04104 — od zadnjega leta (1885, P221) do začetka (1871, P235). */
export const BAPTISM_LINE_YEARS: BaptismYear[] = [
  {
    year: 1885,
    phase: "P221",
    progress: "1/15",
    entries: 104,
    griblje: 25,
    houses: 20,
    scans: "s185–s199",
    scanCount: 15,
    foliation: "pag = sken+13 (198–212) — folio-svinčnik arhivarja",
    boundaryNext: "meja 1884/85 = s186 (60. potrditev) + VSOTNA »1/8/8/5«",
    boundaryNo: 60,
    restart: "z1 · 1. 1. · Griblje h21",
    highlights: [
      "DVOJČKI Gradac ×2 (z92-umrla + z93-živ — page-VLM spojil v 1 vrstico!)",
      "z101-NEIDENTIFICIRANA vrstica — dokaz: POPRAVEK pisarja s199 (×2)",
      "naslovna glava 'Geburts- und Tauf-Buch.' ponovljena SREDI letnika (s190)",
      "poznejši pripisi = KRIŽ z mrliško 04106 (nova verifikacijska dimenzija!)",
    ],
  },
  {
    year: 1884,
    phase: "P222",
    progress: "2/15",
    entries: 112,
    griblje: 21,
    houses: 20,
    scans: "s173–s186",
    scanCount: 14,
    foliation: "pag = sken+13 (186–199)",
    boundaryNext: "meja 1883/84 = s173 (61. potrditev) + VSOTNA »1/8/8/4«",
    boundaryNo: 61,
    restart: "z1 · 1. 1. · Griblje h34 [~84-DUEL]",
    highlights: [
      "pisarjeve oštevilčevalske anomalije ×6 = REKORD strani (s175 prepiše 8–14!)",
      "z84-DUPLIKAT (nova tip!) + s177-REORIZENTACIJA (61–68 → 31–38)",
      "revizijske poševnice ×10 (matrični pregled!)",
      "s184 = 93–102 + 1 PRAZNA neštevilčena vrstica",
    ],
  },
  {
    year: 1883,
    phase: "P223",
    progress: "3/15",
    entries: 99,
    griblje: 19,
    houses: 18,
    scans: "s161–s173",
    scanCount: 13,
    foliation: "sken−5 (159–172) + dvojni foliacijski seriji",
    boundaryNext: "meja 1882/83 = s161 (62. potrditev) + VSOTNA »1 8 8 3.« + DVOJČKI-h68",
    boundaryNo: 62,
    restart: "z1 · 4. 1. · Gradac",
    highlights: [
      "ČISTA linija BREZ pisarjevih anomalij (kontrast P222 ×6!)",
      "mesec-carry-over vzorec + MÄRZ-label korekcija",
      "dvojni foliacijski seriji (2 nova odkritja)",
      "MMK-pripisi: umrla 23.10.1947 Ljubljana (restart!) itd.",
    ],
  },
  {
    year: 1882,
    phase: "P224",
    progress: "4/15",
    entries: 106,
    griblje: 25,
    houses: 23,
    scans: "s147–s161",
    scanCount: 15,
    foliation: "TRI serije: sken−6 (142–157) + LUKNJA »158« + sken−5 (1883)",
    boundaryNext: "meja 1881/82 = s147/s148 (63. potrditev) + 'finis' + 'Anni 1 8 8 1.'",
    boundaryNo: 63,
    restart: "z1 · 2. 1. · Dobravce h27",
    highlights: [
      "25 GRIBLJE = TIE-rekord s 1885!",
      "S160-'NOVEMBER' → DEZEMBER korekcija (DEZ-31 ×4!) + Z71-oktober-korekcija",
      "S149-z16-DUPLIKAT (2. instanca krstne linije)",
      "DVOJČKI-ZWILLINGE Griblje-h68 (P223-LEAD potrjen)",
    ],
  },
  {
    year: 1881,
    phase: "P225",
    progress: "5/15",
    entries: 89,
    griblje: 17,
    houses: 17,
    scans: "s135–s147",
    scanCount: 13,
    foliation: "sken−6 13/13 SEKVENČNO (129–141) — brez luknje",
    boundaryNext: "meja 1880/81 = s135/s136 (64. potrditev) + 'Finis' + 'Jahr 1881.'",
    boundaryNo: 64,
    restart: "z1 · 1. 1. · Griblje h55 (4. Griblje-restart!)",
    highlights: [
      "PEZDIRC ×9 = REKORD LETA (grafija-continuum 5 let!)",
      "17 hiš = VSE DISTINCT (brez duelev!)",
      "z48-botra-PRAZNA + z66-NEZAKONSKI",
      "2 poročni pripisi ('vnalila' — poroki 1958/1959 v blokih)",
    ],
  },
  {
    year: 1880,
    phase: "P226",
    progress: "6/15",
    entries: 122,
    griblje: 22,
    houses: 20,
    scans: "s119–s135",
    scanCount: 17,
    foliation: "sken−6 17/17 SEKVENČNO (113–129) — brez luknje",
    boundaryNext: "meja 1879/80 = s119/s120 (65. potrditev) + VELIKE-CIFRE »1880«",
    boundaryNo: 65,
    restart: "z1 · 3. 1. · Dobravce h11",
    highlights: [
      "PEZDIRC ×14 = REKORD LINIJE do P228 (grafija-continuum 6 let!)",
      "NEZAKONSKI ×7 = REKORD LINIJE (5,7 % — z114 Griblje-h5!)",
      "MODRI matičarski pripisi ×9 (1963–1990!)",
      "DVOJČKI Boršt-h20 + Mißgeburt ×2 + z110-krsten-prazen",
    ],
  },
  {
    year: 1879,
    phase: "P227",
    progress: "7/15",
    entries: 96,
    griblje: 22,
    houses: 19,
    scans: "s106–s119",
    scanCount: 14,
    foliation: "sken−6 14/14 SEKVENČNO (100–113) — LEAD-predikcija s112 potrjena",
    boundaryNext: "meja 1878/79 = s105/s106 (66. potrditev) + VSOTNA razpeta »1 8«/»79«",
    boundaryNo: 66,
    restart: "z1 · 8./9. 1. · Kloster h37 (†19.7.1942 MODRI)",
    highlights: [
      "DVOJČKI ×3 = REKORD (edini todtgeboren-dvojček z65/z66!)",
      "TODTGEBOREN-garble ×3 ('…blyaborn')",
      "z60-POGOJNI KRST ('sub conditione' — 1. v liniji!)",
      "duhovniška izmenjava Janičar ↔ Dovgan (alternirajoče celo leto)",
    ],
  },
  {
    year: 1878,
    phase: "P228",
    progress: "8/15",
    entries: 94,
    griblje: 16,
    houses: 14,
    scans: "s92–s105",
    scanCount: 14,
    foliation: "sken−5 (87–99) + s105-DUPLIKAT → razlaga 'sken−6' ARTEFAKTA!",
    boundaryNext: "meja 1877/78 = s92/s93 (67. potrditev)",
    boundaryNo: 67,
    restart: "z1 · [8↔9] 1. DUEL · Boginja vas h14",
    highlights: [
      "PEZDIRC ×17 = REKORD LINIJE (z2/z3/z4 matec ×3 ZAPOREDOMA!)",
      "s105-LEPLJENEC 1908 z ovalnim pečatom (terminus post quem!)",
      "duhovniška TROJNA izmenjava (Kroggj ↔ Dovgan ↔ Janičar)",
      "z28-TODTGEBOREN GRIBLJE (1. v Gribljih!)",
    ],
  },
  {
    year: 1877,
    phase: "P229",
    progress: "9/15",
    entries: 108,
    griblje: 20,
    houses: 18,
    scans: "s78–s92",
    scanCount: 15,
    foliation: "sken−5 15/15 SEKVENČNO (73–87) — LEAD-predikcija s85 potrjena",
    boundaryNext: "meja 1876/77 = s78-ENO-STRANSKA + 'Incipit annus Domini 1877' kalligrafija",
    boundaryNo: 68,
    restart: "z1 · 9./10. 1. · Zemelj h20",
    highlights: [
      "1. INCIPIT-kalligrafija krstne linije (čez sredino strani!)",
      "DVOJČKI ×4 = REKORD LINIJE (z67/z68 GRIBLJE-h14 'Zwillings'!)",
      "November-31-DUEL ×2 (dan ne obstoji!)",
      "retro-vpisi ×2 + MODRI-TORONTO-KANADA pripis",
    ],
  },
  {
    year: 1876,
    phase: "P230",
    progress: "10/15",
    entries: 100,
    griblje: 14,
    houses: 13,
    scans: "s65–s78",
    scanCount: 14,
    foliation: "sken−5 (60–73)",
    boundaryNext: "meja 1875/76 = s64/s65-DVO-STRANSKA + 'finis Anni 1875' kalligrafija",
    boundaryNo: 69,
    restart: "z1 · 5./5. 1. · Aloshor h24",
    highlights: [
      "'finis-Anni-1875' kalligrafija — pisar obkroži leto (PARALELA Incipit 1877!)",
      "NEZAKONSKI ×6 = REKORD LINIJE do P226",
      "z94-MODRA zap-številka (edinstvena!)",
      "WOLFGR-podpis + 'als Amtsvormund' (uradni skrbnik!)",
    ],
  },
  {
    year: 1875,
    phase: "P231",
    progress: "11/15",
    entries: 119,
    griblje: 17,
    houses: 16,
    scans: "s47–s64",
    scanCount: 18,
    foliation: "sken−3 (42–57) + TROJNI-DUPLIKAT s60=s61=s62 (folio 57!)",
    boundaryNext: "meja 1874/75 = s47-SREDI-PAGI (70. potrditev) + TAIL-1874 ×5 vrstic",
    boundaryNo: 70,
    restart: "z1 · 9./9. 1. · Dobravce h20 (MODRI umrl 2.1.1953!)",
    highlights: [
      "TROJNI-DUPLIKAT-SKENOV = NOVO ODKRITJE (3 različna md5!)",
      "VIOLET-retro-vpis z6 ('vom 11. October 1875 geschriben' — datiran retro!)",
      "PEZDIRC ×5 = NAJNIŽJA vrednost linije",
      "NEZAKONSKI ×2 Griblje + 'ledig.' nota (z4)",
    ],
  },
  {
    year: 1874,
    phase: "P232",
    progress: "12/15",
    entries: 92,
    griblje: 19,
    houses: 18,
    scans: "s37–s47",
    scanCount: 11,
    foliation: "sken−3 SEKVENČNO s36–s47 (33–44) — brez duplikatov v oknu",
    boundaryNext: "meja 1873/74 = s37-SREDI-PAGI + 'Initium anni Domini 1874' kalligrafija",
    boundaryNo: 71,
    restart: "z1 · 1. 1. · Gradac h31 (edini krst-4.!-babica-nota)",
    highlights: [
      "1. INITIUM-kalligrafija linije (pozicijska simetra 'finis 1875'!)",
      "BREZ praznih mesecev = 1. V LINIJI (vs. 1873: 4 prazni!)",
      "TRI duhovnika: Schwinger ↔ Dovgan ↔ Kragelj? (meja-duhovnikov = meja leta!)",
      "zap-pozicijska aritmetika 4/4 POTRJENA (z73=zap-73 …)",
    ],
  },
  {
    year: 1873,
    phase: "P233",
    progress: "13/15",
    entries: 98,
    griblje: 17,
    houses: 16,
    scans: "s26–s37",
    scanCount: 12,
    foliation: "sken−3 (23–33) + DUPLIKAT s28=s29 (folio 25)",
    boundaryNext: "meja 1872/73 = PRED-s28 (izven okna — aritmetično dokazana!)",
    boundaryNo: 72,
    restart: "z1 · 3. 1. · S26R1 (13. restart — aritmetično!)",
    highlights: [
      "X-aritmetični model zap +10-SISTEMATIČNI KURRENT-misread (9 ankerjev!)",
      "4 PRAZNI MESeci = rekord izenačen (J/Juni/Sep/D)",
      "PET duhovnikov 1873 = rekord linije (Dovgan/Pihlár?/Roblek/Bobleh/Dolenc?)",
      "P232-fantom 'z11–z21' razrešen — 98 total intakten",
    ],
  },
  {
    year: 1872,
    phase: "P234",
    progress: "14/15",
    entries: 115,
    griblje: 17,
    houses: 16,
    scans: "s14–s25",
    scanCount: 12,
    foliation: "sken−3 (11–22) — 12/12 visoko",
    boundaryNext: "meja 1871/72 = s13/s14 PAGE-BOUNDARY (1. page-boundary linije!)",
    boundaryNo: 73,
    restart: "z1 · 5. 1. · Griblje h11 (1. vpis leta = GRIBLJE!)",
    highlights: [
      "JUNI-kronologija vs 'Jänner' PRIMING-halucinacija RAZREŠENA (4 dokazi!)",
      "s24-r7-PREČRTANA KOPIJA vrstice (1. v liniji!)",
      "MODRI 'poročena 18.2.1919 †16.3.' (najnovejši pripis leta)",
      "PEZDIRC ×2 EKSPLICITNO DVOJNI ('Anna + Michael Pezdirc' z63!)",
    ],
  },
  {
    year: 1871,
    phase: "P235",
    progress: "15/15",
    entries: 108,
    griblje: 17,
    houses: 16,
    scans: "s3–s13",
    scanCount: 11,
    foliation: "sken−3 KOMPLETNA FORMULA (1–11) + DUPLIKAT s3=s4 (folio 1!)",
    boundaryNext: "meja 1870/71 = ZAČETEK KNJIGE (s1 vezava + s2 naslovna + nalepek!)",
    boundaryNo: 74,
    restart: "z1 · 3. 1. · Krasinec h27 (1. vpis leta = KRASINEC — vzorec prekinjen!)",
    highlights: [
      "108-vpisov-aritmetični model (116 vrstic − 8 DUPLIKAT-s4)",
      "DUPLIKAT-s3=s4 REŠITEV — obe knjižni duplikati rešena (s3=s4 + s28=s29!)",
      "duhovniki EKSTRAHIRANI: Weisel/Wenzel?/Wessely continuum + Dotto + Feršlan",
      "DVOJČKI z72/z73 'Zwillinge' (1. v liniji!) + z91-KRSTEN-PRAZNO",
    ],
  },
];

/** PEZDIRC-grafija-continuum po letih (omenjene vrstice, vključno ne-Griblje). */
export const PEZDIRC_PER_YEAR: { year: number; count: number }[] = [
  { year: 1885, count: 4 },
  { year: 1884, count: 4 },
  { year: 1883, count: 6 },
  { year: 1882, count: 4 },
  { year: 1881, count: 9 },
  { year: 1880, count: 14 },
  { year: 1879, count: 12 },
  { year: 1878, count: 17 },
  { year: 1877, count: 11 },
  { year: 1876, count: 17 },
  { year: 1875, count: 5 },
  { year: 1874, count: 7 },
  { year: 1873, count: 8 },
  { year: 1872, count: 5 },
  { year: 1871, count: 8 },
];

/** Skupni PEZDIRC-omenbe 1871–1885 (×131 vrstic!). */
export const PEZDIRC_TOTAL = PEZDIRC_PER_YEAR.reduce((s, y) => s + y.count, 0);

export interface CrossThread {
  id: string;
  nameSi: string;
  nameEn: string;
  summarySi: string;
  summaryEn: string;
  detailSi: string;
  detailEn: string;
  xOpen?: string;
}

/** Križnoletne niti sinteze (P236). */
export const CROSS_YEAR_THREADS: CrossThread[] = [
  {
    id: "pezdirc",
    nameSi: "PEZDIRC-continuum (×131 vrstic / 15 let)",
    nameEn: "The PEZDIRC continuum (×131 rows / 15 years)",
    summarySi:
      "Edini priimek, prisoten v VSEH 15 letih — grafija-continuum Pezdirc/Perdisek/Ležir/Pedice/Pegdire/Bezdirč/Perdiuc/Pedire/Peghirc/Pegdic … vrhunec 1878+1876 (×17!), dno 1875 (×5). 'Peter' je najpogostejše ime (×3 linije le 1871).",
    summaryEn:
      "The only surname present in ALL 15 years — a grapheme continuum Pezdirc/Perdisek/Ležir/Pedice/Pegdire/Bezdirč … peaking 1878+1876 (×17!), bottom 1875 (×5). 'Peter' is the most frequent given name (×3 lines in 1871 alone).",
    detailSi:
      "P221 ×4 · P222 ×4 · P223 ×6 · P224 ×4 · P225 ×9 (rekord leta) · P226 ×14 · P227 ×12 · P228 ×17 (rekord linije — z2/z3/z4 matec ×3 ZAPOREDOMA!) · P229 ×11 · P230 ×17 · P231 ×5 (najnižja) · P232 ×7 (+z51-'Zgajdire' hipoteza → ×8) · P233 ×8 · P234 ×5 · P235 ×8 ('Peter-Pezdirc-in-Griblach' z81 EKSPLICITNO X-ZOOM!).",
    detailEn:
      "P221 ×4 · P222 ×4 · P223 ×6 · P224 ×4 · P225 ×9 (the year's record) · P226 ×14 · P227 ×12 · P228 ×17 (the line record — z2/z3/z4 mother ×3 CONSECUTIVE!) · P229 ×11 · P230 ×17 · P231 ×5 (the lowest) · P232 ×7 (+ the z51-'Zgajdire' hypothesis → ×8) · P233 ×8 · P234 ×5 · P235 ×8 ('Peter-Pezdirc-in-Griblach' z81 EXPLICIT X-ZOOM!).",
    xOpen: "h40-PEZDIRC-nit čez leta (1872 z74 · 1873 z51 · 1874 z82 · 1879 z95-†15.6.1941) — isti gospodarski kompleks?",
  },
  {
    id: "milek",
    nameSi: "MILIČ/MILEK/MIHELČ-hipoteza (ista družina?)",
    nameEn: "The MILIČ/MILEK/MIHELČ hypothesis (one family?)",
    summarySi:
      "1871 MILIČ ×5 oseb (rekord) ↔ MILEK po letih (1874 ×7 · 1875 ×4 · 1877 ×5 vse-Griblje · 1879 ×6) ↔ MIHELČ/MILCH/MIHELIČ-garble. Kurrent-'MIC/MILEK/HELČ' zmeda — X-open hipoteza, da so vse tri grafije isti priimek.",
    summaryEn:
      "1871 MILIČ ×5 persons (a record) ↔ MILEK across years (1874 ×7 · 1875 ×4 · 1877 ×5 all-Griblje · 1879 ×6) ↔ MIHELČ/MILCH/MIHELIČ garble. The Kurrent 'MIC/MILEK/HELČ' confusion — the X-open hypothesis that all three graphies are the same surname.",
    detailSi:
      "1871: z16-'Mihelik'-matec + z91/z96-oče-MILIČ. 1874: ×7 oseb-'MILCH' z73. 1879: ×6 (6/6 KOMPLET-nit!). 1882: z55-oče-'Milech'-h65. 1883: z59/z88-'Mihelč'-botri. 1885: z105-botra-MILEK-nit (P218/P220-h65!).",
    detailEn:
      "1871: z16-'Mihelik'-mother + z91/z96-father-MILIČ. 1874: ×7 persons-'MILCH' z73. 1879: ×6 (a 6/6 COMPLETE thread!). 1882: z55-father-'Milech'-h65. 1883: z59/z88-'Mihelč'-godmothers. 1885: z105-godmother-MILEK-thread (P218/P220-h65!).",
    xOpen: "Ali so MILIČ (1871) in MILEK (1874–1885) ista družina? — potreben mrliški/poročni križ.",
  },
  {
    id: "duhovniki",
    nameSi: "Duhovniki 1871–1885 (podpisi + izmene)",
    nameEn: "The priests 1871–1885 (signatures + rotations)",
    summarySi:
      "1871: Weisel-'D.H. Cap.' → Wenzel?/Wessely-continuum (WEISEL/WENZEL/WESSELY garble — ista oseba? X-open!). Srednja leta: Dovgan-continuum + Pihlár?/Roblek/Bobleh/Dolenc? (1873 = PET duhovnikov, rekord!) + Schwinger/Kragelj? (1874) + Hoggia/Roggja-DUEL (1875/1877) + Kroggj (1878) + Janičar (1878–1880, menjava okoli z106-1880).",
    summaryEn:
      "1871: Weisel-'D.H. Cap.' → the Wenzel?/Wessely continuum (the WEISEL/WENZEL/WESSELY garble — one person? X-open!). Middle years: the Dovgan continuum + Pihlár?/Roblek/Bobleh/Dolenc? (1873 = FIVE priests, the line record!) + Schwinger/Kragelj? (1874) + the Hoggia/Roggja DUEL (1875/1877) + Kroggj (1878) + Janičar (1878–1880, the mid-1880 rotation).",
    detailSi:
      "Meje-duhovnikov pogosto sovpadajo z mejami-let: s37-r1 Dovgan-1873 → s37-r2 Schwinger-1874 (1:1 z mejo leta!); 1880: Janičar z1–z105 → Dovgan z106–z122 (menjava okoli novembra).",
    detailEn:
      "Priest boundaries often coincide with year boundaries: s37-r1 Dovgan-1873 → s37-r2 Schwinger-1874 (1:1 with the year boundary!); 1880: Janičar z1–z105 → Dovgan z106–z122 (a rotation around November).",
    xOpen: "Weisel = Wenzel = Wessely? (1871 — trije podpisi, ista roka?)",
  },
  {
    id: "hise",
    nameSi: "Hišni continui (h40/h69/h12/h28/h1/h11/h65)",
    nameEn: "House continuums (h40/h69/h12/h28/h1/h11/h65)",
    summarySi:
      "h40 = PEZDIRC-continuum (1872 z74-×4-v-3-letih · 1873 z51 · 1874 z51/z82-DUEL · 1879 z95-†15.6.1941). h69 = ×3-v-3-letih z RAZLIČNIMI družinami (1871 z44-HUSIČ + 1872 z97-BORIN + 1873 z55!). h12 = DRAGOŠ→PEZDIRC→DRAGOŠ (1871→1872→1874). h1 = 5 dokazov čez 15 let (1871 z69-SAKOFČIČ ×3-TROJNI · 1873 z47/z92 · 1875 z111 · 1885 z33/z100-×2).",
    summaryEn:
      "h40 = the PEZDIRC continuum (1872 z74-×4-in-3-years · 1873 z51 · 1874 z51/z82-DUEL · 1879 z95-†15.6.1941). h69 = ×3-in-3-years with DIFFERENT families (1871 z44-HUSIČ + 1872 z97-BORIN + 1873 z55!). h12 = DRAGOŠ→PEZDIRC→DRAGOŠ (1871→1872→1874). h1 = 5 attestations across 15 years (1871 z69-SAKOFČIČ ×3-TRIPLE · 1873 z47/z92 · 1875 z111 · 1885 z33/z100-×2).",
    detailSi:
      "h28 = 3.-LETO-vzorec duelov (1871 z81-Pezdirc-vs-z83-Požek · 1879 z92-MILEK · 1880 h28-Anna). h11 = restart-hiša (1872 z1!) + TAIL-1875-z3t-Anna. h65 = MILIČ 1871 → MILEK 1882 → PEZDIRC-†1965 1879-nit.",
    detailEn:
      "h28 = the 3rd-YEAR duels pattern (1871 z81-Pezdirc-vs-z83-Požek · 1879 z92-MILEK · 1880 h28-Anna). h11 = the restart house (1872 z1!) + the TAIL-1875-z3t-Anna. h65 = MILIČ 1871 → MILEK 1882 → PEZDIRC-†1965 1879-thread.",
    xOpen: "h69: trije različni priimki v treh letih — hiša je menjala lastnike ali je hišna št. prenosna?",
  },
  {
    id: "vzorci",
    nameSi: "Vzorci: DVOJČKI · PREČRTANI · DUPLIKATI · NEZAKONSKI",
    nameEn: "Patterns: TWINS · STRUCK-OUTS · DUPLICATES · ILLEGITIMATE",
    summarySi:
      "DVOJČKI v 8/15 letih (1. z72/z73-1871 'Zwillinge'; rekord ×4-1877; edini todtgeboren-dvojček z65/z66-1879). PREČRTANI: z37/z38-1871 (mrtvorojeni?) · s24-r7-1872 · z84-dup-1884 · z111/z112-tail-1885. DUPLIKATI-SKENOV ×4 + 1 TROJNI: s3=s4 (fol-1) · s28=s29 (fol-25) · s60=s61=s62 (fol-57!) · s105-LEPLJENEC-1908 (pečat!) + LUKNJA-'158'.",
    summaryEn:
      "TWINS in 8/15 years (the 1st z72/z73-1871 'Zwillinge'; the record ×4-1877; the only stillborn twin z65/z66-1879). STRUCK-OUTS: z37/z38-1871 (stillborn?) · s24-r7-1872 · z84-dup-1884 · z111/z112-tail-1885. SCAN-DUPLICATES ×4 + 1 TRIPLE: s3=s4 (fol-1) · s28=s29 (fol-25) · s60=s61=s62 (fol-57!) · s105-PASTED-1908 (a seal!) + the '158' GAP.",
    detailSi:
      "NEZAKONSKI: rekord ×6-1876 in ×7-1880 (edini Griblje: z114-h5); 1874 ×0 Griblje. MODRI-matičarski pripisi: od 1882 ('preseljen 19.3.1882' = najstarejši!) do 1871 ('umrl 20.12.1957' = najnovejši datum linije!); vrhunec ×12-1879.",
    detailEn:
      "ILLEGITIMATE: the records ×6-1876 and ×7-1880 (the only Griblje: z114-h5); 1874 ×0 Griblje. BLUE registrar annotations: from 1882 ('moved 19.3.1882' = the oldest!) to 1871 ('died 20.12.1957' = the newest date of the line!); the peak ×12-1879.",
  },
];

/** X-open preostanki sinteze (P235-LEAD). */
export const X_OPEN_REMAINDERS: { id: string; titleSi: string; titleEn: string; bodySi: string; bodyEn: string }[] = [
  {
    id: "z81-hisna",
    titleSi: "z81-hisna 28/20 (1871)",
    titleEn: "z81 house no. 28/20 (1871)",
    bodySi:
      "'Peter Pezdirc in Griblach' (z81, EKSPLICITNO X-ZOOM) nosi hišno DUEL 28 vs 20 — h28-×2-DELO-DUEL (z81-vs-z83-Požek) ostaja odprta; '20' lahko prelivi iz sosednje celice.",
    bodyEn:
      "'Peter Pezdirc in Griblach' (z81, EXPLICIT X-ZOOM) carries the house DUEL 28 vs 20 — the h28-×2-DELO-DUEL (z81-vs-z83-Požek) stays open; '20' may bleed from the neighbouring cell.",
  },
  {
    id: "z37-z38",
    titleSi: "z37/z38-obseg (1871)",
    titleEn: "the z37/z38 extent (1871)",
    bodySi:
      "PREČRTANI-DVOJNI (Krasinec-h12-Harasinič, April 22, vijugasta črta) — mrtvorojeni ali dvojni zapis istega otroka? Obseg prečrtanja (oba-vrstici vs ena) ostaja odprt.",
    bodyEn:
      "The STRUCK-OUT-DOUBLE (Krasinec-h12-Harasinič, April 22, a wavy line) — stillborn or a double entry of the same child? The extent of the strike-out (both rows vs one) stays open.",
  },
  {
    id: "weisel-wessely",
    titleSi: "Weisel = Wenzel = Wessely?",
    titleEn: "Weisel = Wenzel = Wessely?",
    bodySi:
      "Trije podpisi 1871 (Weisel-'D.H. Cap.' z1–z13 · Wenzel?-Coop. z92/93 skupni-podpis · Wessely-'cop.' z98) — garble-continuum suggests ISTA oseba (obrat kaplana), a X-open brez neodvisnega dokaza.",
    bodyEn:
      "Three signatures of 1871 (Weisel-'D.H. Cap.' z1–z13 · Wenzel?-Coop. z92/93 a joint signature · Wessely-'cop.' z98) — the garble continuum suggests ONE person (a curate's rotation), but X-open without independent proof.",
  },
];

/** Skupne statistike linije (izpeljano, konsistentno z BAPTISM_LINE_YEARS). */
export const BAPTISM_LINE_TOTALS = {
  years: BAPTISM_LINE_YEARS.length,
  entries: BAPTISM_LINE_YEARS.reduce((s, y) => s + y.entries, 0),
  griblje: BAPTISM_LINE_YEARS.reduce((s, y) => s + y.griblje, 0),
  housesSeen: new Set(BAPTISM_LINE_YEARS.map((y) => y.year)).size,
  twinsYears: 8,
  restarts: 15,
  boundaryConfirmations: "60.–74.",
  label: "PODZEMELJ-R-1871-1885",
} as const;

/** Živi seštevek za qa-p236: Griblje-vpisi po letih IZ parish-synthesis (mora = parish.ts bloki). */
export function baptismGribljeByYear(): Map<number, number> {
  return new Map(BAPTISM_LINE_YEARS.map((y) => [y.year, y.griblje]));
}
