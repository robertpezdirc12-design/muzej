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

// ——— P252: SINTEZA POROČNE PREDZGODOVINE 04455 (1873–1885 = 13/13 KOMPLETNA!) ———
// Knjiga »Podzemelj P 1873–1922« (naslovnica 1:1, P151!) je s P251 KOMPLETNO dokumentirana
// po predzgodovini — ta modul združuje križnoletne niti, vzorce in X-open preostanke
// vseh 13 faz (P238 = 1885 … P251 = 1873). Vsi števci so preverljivi proti HOUSE_VITALS
// (parish.ts) — qa-p252 jih živo preverja; paleografski dokazi so v
// research/issue17/parish-marriage-<leto>-04455.json. NI NOVIH BRANJ, NI NOVIH SKENOV (MERI!):
// korpus 2012/269 NESPREMENJEN — sinteza je izpeljana 1:1 iz obstoječih faz (cf. P236).

export interface MarriageEarlyYear {
  year: number;
  /** faza, ki je leto prebrala (P238 = 1885 … P251 = 1873) */
  phase: string;
  /** napredek branja linije tistega trenutka ("1/13" = 1885 je bil prvi prebran) */
  progress: string;
  /** skupno število vpisov v knjigi tisto leto (števje iz zap-stolpca; 1873 = SAMO m18–m21!) */
  entries: number;
  /** prebrani Griblje-vpisi = bloki v parish.ts */
  griblje: number;
  /** različne Griblje-hiše tistega leta (med bloki) */
  houses: number;
  /** okvir skenov */
  scans: string;
  scanCount: number;
  /** foliacijska konvencija okna ('Pag. = sken−1' + posebnosti) */
  foliation: string;
  /** meja s prejšnjim (nazaj po knjigi) letom — P251-lead knjižnega odpiranja */
  boundaryNext: string;
  /** slog restarta/meje leta (13 različnih variant!) */
  boundaryVariant: string;
  /** restart-vpis-1: dan · pari */
  restart: string;
  highlights: string[];
}

/** 13 let predzgodovine 04455 — od zadnjega leta (1885, P238) do začetka knjige (1873, P251). */
export const MARRIAGE_EARLY_LINE_YEARS: MarriageEarlyYear[] = [
  {
    year: 1885,
    phase: "P238",
    progress: "1/13",
    entries: 22,
    griblje: 7,
    houses: 7,
    scans: "s56–s61",
    scanCount: 6,
    foliation: "Pag = sken−1 (55–60) — RAZŠIRJENO (prej P84: samo 61–66!)",
    boundaryNext: "meja 1885/86 = s61 (vpis 22 = TAIL 22. Nov + velike »1 8 8 6« + restart-vpisi-1–3/1886 1:1 z P84-korpusom!)",
    boundaryVariant: "1. vrsta: restart + tail prejšnjega leta NA ISTI STRANI (s56/s61)",
    restart: "vpis 1 = 25. Jänner 1885 (s56 — tail-1884-vpisi-15–18 + restart NA ISTI STRANI!)",
    highlights: [
      "vpis 3 PRESKOČEN (zap 2,4,5,6!) = 1. ordinalna anomalija linije + datum-izven-vrsti v7 (7. Feb po 8. Feb)",
      "★★★ h13-MERGE s P80-sidrom (1885-vpis-22 = h13 × h23[28-DUEL]-TAIL — P115-PEZDIREC-križ!)",
      "★★★ ŠTAJERSKA-OBLIKA 4-pasovi (h60-'60'-1:1 — blok bere se desno→levo!) + h58-Požek[~]-DUEL-RAZREŠEN",
      "3 X-OPEN-vas-dueli pošteno (h29/h15/h9 — »Gern/Gornje-29«, »Glob./Woh.-15«, »Griblje-9?«)",
      "LEDERER-usnjarska veja ×14-vpisov-16–22 + PEZDIRC ×3 + BRINC/BRINEC ×2 + najstarejši par 97 let (48+49) + najmlajša nevesta 17 [~19-duel]",
    ],
  },
  {
    year: 1884,
    phase: "P239",
    progress: "2/13",
    entries: 18,
    griblje: 3,
    houses: 3,
    scans: "s52–s56",
    scanCount: 5,
    foliation: "Pag = sken−1 (51–55) — s55-'11.'-ultra-zoom-3:1 (NE-'12.'!)",
    boundaryNext: "meja 1883/84 = s52→s53 (s52 = tail-1883-vpisi-8–12 vsi »1883«!) · meja 1884/85 = s56-tail 15–18 (P238-1:1!)",
    boundaryVariant: "2. vrsta: velika glava »1884« na restartu (s53)",
    restart: "vpis 1 = 6. Februar 1884 (s53 — velika-glava-»1884« + ženin Martin PEZDIRC!)",
    highlights: [
      "18 VPISOV BREZ preskoka (kontrast-1885-vpis-3-PRESKOČEN!)",
      "2 POLNI-GRIBLJE-pora (v6 h54×h44 SIMEC×STRUCELJ + v16 h47×h34 HLOBUČAR×SILAH — DVOJNI-h34-križ: sestrske poroki na h34 v 2 ZAPOREDNIH letih 1884+1885!)",
      "PEZDIRC ×4 ženini (v1-Martin + v2-Mathias-ista-hiša! + v14-Janez + v15-Matthias) + priče [~]×3",
      "MILEK-križ +2 (v6-priča-MIHELČ[~Milech!] + v18-mati-MILEK — križ ×235→×237!)",
      "duhovnik Dovgan EDINI vseh 18 (1:1-kot-1885!) + najstarejši par 97 let [~duel] (56+41 — ENAKO-kot-1885!) + 2 X-OPEN-kandidata (v7-'Griblje-2?'-vs-Vrtok-5 + v10-'Griblner-dyfla'-brez-hišne!)",
    ],
  },
  {
    year: 1883,
    phase: "P240",
    progress: "3/13",
    entries: 12,
    griblje: 2,
    houses: 2,
    scans: "s50–s52",
    scanCount: 3,
    foliation: "Pag = sken−1 (49–51) — s51-'2.-ne-1.'-ultra-zoom-Kurrent (2-navpični-lok!)",
    boundaryNext: "meja 1882/83 = s50-MID (tail-1882-vpisi-24–26 — #26-Mathias-HRIZAN-h36-tail = h36-predistopna-nit!)",
    boundaryVariant: "3. vrsta: števke »1 8 8 3.« RAZPOREJENE ČREZ STOLPCE (Štajerska-oblika-4-pasovi!)",
    restart: "vpis 1 = 21. Januar 1883 (s50-DNO — pass-1-'statistika-zakonskih-stanov'-MISREAD-RAZREŠEN-2:1!)",
    highlights: [
      "★★★★★ h2 = 1.-POROČNI-04455-BLOK KADARKOLI (najnižja-aktivna-hiša!-prej-samo-mrliška-04894-1919 — poročna PREHITELA za 36 let!)",
      "dve poroki ISTI DAN (v5+v6 = 4. Februar — 1.×-v-predzgodovini!) + HROVALJ-brat+sestra-ISTI-DAN (v8+v9 — ISTA-hiša-Kaplitz-8!)",
      "PEZDIRC-ženin v4-Miha-PEZDIRC-črka-za-črko-'NI-Pegdirc'! (+v5/v7-[~])",
      "MILEK-križ-kandidat IZVEN korpusa pošteno (v10-'Milleh' — križ ×237 NESPREMENJEN!)",
      "duhovnik-Dovgan-v1–v9 + v12-'Fandorf'-NOVI-DUHOVNIK-KANDIDAT [~X-OPEN!] + 4-vas-dueli",
    ],
  },
  {
    year: 1882,
    phase: "P241",
    progress: "4/13",
    entries: 26,
    griblje: 7,
    houses: 7,
    scans: "s45–s50",
    scanCount: 6,
    foliation: "Pag = sken−1 (44–49) — s45-'93/94' [~X-OPEN-duel pošteno odprt!]",
    boundaryNext: "meja 1881/82 = s44→s45-GLAVA (P242-1:1! — tail-1881 = v26-20.-Dezember-na-s44!) · meja 1882/83 = s50-MID (P240-1:1!)",
    boundaryVariant: "4. vrsta: VELIKA glava '1882' PRED vrstico zap.-št. 1 (s45)",
    restart: "vpis 1 = 1. Februar [~21. Jänner-DUEL] (s45 — P241-ULTRA-ZOOM-1:1!)",
    highlights: [
      "26 VPISOV BREZ preskoka (4. leto zapored!) + PRESKOK-12 v s41→s42 (5.-številčenjska-anomalija — 1874-mirror!)",
      "h1 = NAJNIŽJA-HIŠA-S-POROČNIM-BLOKOM KADARKOLI (prej-h2-1883 — preglasi-za-1-stopnjo!)",
      "h36-TAIL-MERGE z P80-sidrom (P240-napoved-IZPOLNJENA-1:1!) + h53-FIRSTYEAR-DVIG 1890→1882 (+8)",
      "PEZDIRC ×5 vpisov (v9-OBA-PEZDIRC — ženin+nevesta+starši+priča-×4-omembe-v-enem-vpisu! + v15 + v16 + v18 + v20-priča) + ×4-dodatnih-omemb",
      "v6/v7-IZMENA-VLOG (brat+sestra-TOMC/Berčopec-ISTI-DAN!) + v3/v4-ISTA-HIŠA-×2-zapored + Jakopič-križ v15×v16 + MILIČ-križ-×237",
    ],
  },
  {
    year: 1881,
    phase: "P242",
    progress: "5/13",
    entries: 25,
    griblje: 9,
    houses: 8,
    scans: "s39–s44",
    scanCount: 6,
    foliation: "Pag = sken−1 3/3 (38–43) — P243-s38-DUEL rešen s P244 (0-vs-7-Kurrent!)",
    boundaryNext: "meja 1880/81 = s38→s39 (2×-neodvisno-REŠENA!) · meja 1881/82 = s44→s45-glava (P241-1:1!)",
    boundaryVariant: "5. vrsta: letnica '1881' V DATUMSKEM STOLPCU nad vrstico 1 (skromna!)",
    restart: "vpis 1 = 16. Jänner 1881 (s39-TOP — posebna-naslovna-glava-NE-obstaja!)",
    highlights: [
      "9 blokov = 2. največ (za 11-1874!) + h27 ×2-BLOKA-V-1-LETU-PRVIČ-LINIJE (v4-ženin-KUTHAR + v14-nevesta!)",
      "h52-FIRSTYEAR-DVIG 1882→1881 (+1 — poročna-prehiti-krstno-na-h52-ZA-6-LET!)",
      "Georg-PEZDIRC-56-l-črka-za-črko-1:1 (uz-A-'NE-Pegdirc'!) + PEZDIRC ×5 + 'z-Gribl.'-IZVOR-pripisi ×9 (v8–v11-'rozen-v-Gribljeh'-bivališče-drugje — NOVA-podkategorija!)",
      "TAPIČ↔ŠILAR-križ v23 (starši-neveste-Mathias-Šilar × Anna-geb.-TAPIČ — nevestina-mati ≈ ženinova-sorodnica!)",
      "BRINC/BRINEC-mreža (v13-vdova-h56!) + PEZDIRC-pred-časi-v-s40-v7 (starši-'Michael-Kathar.-PEZDIREC-½-Gübly'!)",
    ],
  },
  {
    year: 1880,
    phase: "P243",
    progress: "6/13",
    entries: 20,
    griblje: 3,
    houses: 3,
    scans: "s35–s38",
    scanCount: 4,
    foliation: "Pag = sken−1 [~X-OPEN-DUEL s38-'Pag. 34.'-vs-'37' — REŠEN s P244: pravilo OSTAJA (0-vs-7-Kurrent-misread!)]",
    boundaryNext: "meja 1879/80 = s35-MID (P244-1:1 — tail-1879-vpisi-31–33!) · meja 1880/81 = s38→s39 (P242-2×-neodvisno!)",
    boundaryVariant: "7. vrsta: restart NA DNU prejšnje strani (s35-dno — zadnja-vrsta!)",
    restart: "vpis 1 = 1. Jänner [~4.-DUEL] (s35-DNO — številčenje-31–33 = tail-1879 → RESTART-1–2!)",
    highlights: [
      "3 bloki vsi ŽENINI (h24-BRINE = 1.-poročni-dokaz + h63-Križan-Miklavčič + h53-PERDIRC!)",
      "h53-FIRSTYEAR-DVIG 1890→1880 (+10 — poročna-PREHITI-krstno-na-h53-ZA-7-LET!)",
      "'Gaveldzettel'-očetova-privolitev = 1.-ta-vrsta-dokumenta-v-predzgodovini (h53-mladoletna-nevesta!)",
      "'finis / s 1880' = 1.-ZAKLJUČNA-OZNAKA-LETA-v-predzgodovini (s38-dno!)",
      "GRIBLJAN-IZVOR-pripisi ×2 ('ž. Griblan' — izvor ≠ bivališče — NI bloki pošteno!)",
    ],
  },
  {
    year: 1879,
    phase: "P244+P245",
    progress: "7/13",
    entries: 33,
    griblje: 9,
    houses: 8,
    scans: "s26–s35",
    scanCount: 10,
    foliation: "Pag = sken−1 5/5 (25–34) → P243-s38-DUEL-REŠEN! (pravilo-NE-prelama!)",
    boundaryNext: "meja 1878/79 = s25/s26 + 'FINIS PRO ANNO 1878' (2.-instance-SODA-vzorca!) · meja 1879/80 = s35-mid (P243-1:1!)",
    boundaryVariant: "8. vrsta: GLAVA '1879' PONOVLJENA NA VSAKEM RAZPRTEM LISTU (1. v predzgodovini!)",
    restart: "vpis 1 = 29. Jänner [~März-DUEL] (s26 — P245-KOREKCIJA: s26-NE-s27! številčenje-v-LEVI-MARGINI — Lfd.-stolpec-NE-obstaja!)",
    highlights: [
      "33 VPISOV = REKORD PREDZGODOVINE + P245-KOREKCIJA dokumentirana (P244-napaka-razkrita-in-POPOVLJENA: restart-s27→s26!)",
      "h16 ×2-BLOKA-V-1-LETU (v1-restart + v25!) + h50-PT-luknja-1.-poročni-dokaz (v5-Mathias-PEZDIRC!) + h63-KRIŽAN-2.-leto-ZAPORED",
      "PEZDIRC ×2-ženinov (v7+v21 — 7.-leto-continuuma!)",
      "MILEK-križ-kandidat IZVEN pošteno (s35-tail-'½-Gübl.-Mileh' [~] — križ ×237→×238!)",
      "33 vpisov = REKORD + finis-pro-anno-1878 = 2.-instance-SODA-vzorca + MODRI-pripis-'Civil-Beizag'-[~X-OPEN!]",
    ],
  },
  {
    year: 1878,
    phase: "P246",
    progress: "8/13",
    entries: 23,
    griblje: 7,
    houses: 7,
    scans: "s19–s25",
    scanCount: 7,
    foliation: "Pag = sken−1 6/6 (18–23) → skupaj-z-5/5-1879 = 11/11!",
    boundaryNext: "meja 1877/78 = s18→s19 (P247-1:1!) · meja 1878/79 = s25/s26 + finis (P245-1:1!)",
    boundaryVariant: "9. vrsta: GLAVA '1878' NI PONOVLJENA na listih — letnica SAMO INLINE (kontrast-1879!)",
    restart: "vpis 1 = 16. Jänner 1878 (s19-TOP — marginalna-'1'-FIZIČNO; '1878-Jänner-16'-INLINE!)",
    highlights: [
      "×3-INTRA-DVOJNI (h47×h43-KLOBUČAR×BRULA + h18×h65-ŠIMEC×MILEK + h1×h35-KELCHO×HRIŽAN!)",
      "HRIŽAN ×3-BLOKI-V-1-LETU = REKORD PREDZGODOVINE (v6+v17+v21 — vse neveste!)",
      "h47 = NOVA-hiša (hišna-sinhronizacija-9/10-SKLAD — novi-samo-h47!)",
      "PEZDIRC ×2-garble (v10-PEGDIRIC-Krasinec-2 + v20-PEGDIČ-Lahine-10 — izven-Griblje-NI-bloki-pošteno!)",
      "številčenje-v-LEVI-MARGINI 2.-leto + DISPENS-super-mixta-ac-prima (v1!) + m9-Wohnort-2-prečrtani-popravki",
    ],
  },
  {
    year: 1877,
    phase: "P247",
    progress: "9/13",
    entries: 18,
    griblje: 5,
    houses: 4,
    scans: "s15–s18",
    scanCount: 4,
    foliation: "Pag = sken−1 4/4 (14–17) → skupaj 15/15!",
    boundaryNext: "meja 1876/77 = s14→s15 + 'f-i-n-i-s / 1-8-7-6' (3.-instance-SODA-vzorca!) · meja 1877/78 = s18→s19 (P246-1:1!)",
    boundaryVariant: "9. vrsta v 2. LETU: GLAVA-INLINE (letnica-INLINE-v-1.-vpisu-vsakega-lista — 1877+1878!)",
    restart: "vpis 1 = '1877 Jänner 14' INLINE (s15-TOP — marginalna-'1'-FIZIČNO!)",
    highlights: [
      "★★★★★ MOH-TROJČEK (3 sorojenci-h51-v-3-tednih: v4-nevesta + v5-ženin + v7-nevesta — 1.-REKORD-TIPA!)",
      "★★★★★ MOH×BRODARIČ-DVOJNI-SORODSTVENI-ZAKON (brat+sestra × brat+sestra — 2 poroki med ISTIMA družinama v 3 tednih!)",
      "h51 = 1.-04455-BLOK-KADARKOLI (PT-luknja-hiša!-4 bloki — najtanjša-hiša-P191!)",
      "RE-NUMBERING-s18 (+1-×4-PREČRTANIH: 14→15-15→16-16→17-17→18 — razlog-dup-'14'!)",
      "firstYear-DVIG ×3 (h10+h69 +10-let + h8 +4!) + v16-IZVEN-KRONOLOGIJE (28. Dec PO 21. Nov!) + PEZDIRC ×1 [~] ('Prodaric'-garble — NI blok pošteno!)",
    ],
  },
  {
    year: 1876,
    phase: "P248",
    progress: "10/13",
    entries: 15,
    griblje: 6,
    houses: 6,
    scans: "s11–s14",
    scanCount: 4,
    foliation: "Pag = sken−1 4/4 (10–13) → skupaj 19/19!",
    boundaryNext: "meja 1875/76 = s10→s11-NA-ISTI-STRANI + violet-NAKNADNI-8-VMES! · meja 1876/77 = s14→s15 (P247-1:1!)",
    boundaryVariant: "10. vrsta: restart BREZ letnice + tail-violet-NAKNADNI-nad-nim (4-novi-elementi-v-1-meji — NOV-TIP!)",
    restart: "vpis 1 = 9. Februar 1876 BREZ letnice (s11-VRSTA-2 — mesec-'f'-mikro-forenzika-1:1!-sreda-ritem-9/16/23!)",
    highlights: [
      "★★★★★ PEZDIRC ×9 omenb = REKORD PREDZGODOVINE ('Leinmannstochter' ×2! + ×4-blokov-od-6 + 2×-Georg-Pegdire-oče!)",
      "★★★★★ 6-firstYear-DVIGOV-V-1-LETU = REKORD LINIJE (h44 +23 = NOV-ABSOLUTNI-1899→1876! + h30 +13 + h64 +12 + h31 +10 + h35 +6 + h41 +5!)",
      "INTRA-DVOJNI ×2 (v1-h31×h44-ŽUPANIČ×PEGDIRE + v8-h35×h64-HRIŽAN×POŽEH!) + IZMENA-VLOG ×2 (v3/v4 + v6/v7!)",
      "DISPENS-3.-GRAD-1:1 (v7!) + MLADOLETNICA ×2 (v10-17-l-Vormund! + v13-'PRO-DIE-MINDERJ.-BRAUT'!)",
      "tail-violet-8-NAKNADNI = kaplan-Daniel-Perschek (EDINI-ne-Dovgan-podpis-kontinuuma!) + TYPHUS-k.k.-sodišče-h30!",
    ],
  },
  {
    year: 1875,
    phase: "P249",
    progress: "11/13",
    entries: 18,
    griblje: 1,
    houses: 1,
    scans: "s8–s10",
    scanCount: 3,
    foliation: "Pag = sken−1 4/4 (6–9) → skupaj 23/23!",
    boundaryNext: "meja 1874/75 = s7→s8 (tail-1874-m28–m32: 28. Feb…18. Nov!) + 'f-i-n-i-s / 1-8-7-4' (4.-instance!) · meja 1875/76 = s10→s11 (P248-1:1!)",
    boundaryVariant: "11. vrsta: MARGINA-'21'-FIZIČNA-ANOMALIJA (aritmetika-VSILJUJE-restart-'1' — pisarska-napaka!)",
    restart: "vpis 1 = 16. Jänner 1875 (s8-TOP — velika-'1875'-INLINE-v-datumskem-stolpcu-4.-leto-vrste!)",
    highlights: [
      "★★★ MNOŽIČNI-POROČNI-DAN '4. Februar 1875' ×10 = REKORD-PREDZGODOVINE (v3–v12 — 10 porok v 1 dnevu!)",
      "DATUMSKI-VZOREC-MESEC-SAMO-OB-SPREMEMBI (v2-'Febr. 2.' → v3–v12-'4.' → v13-'Febr. 8.' → v15-'Mai 9.'!)",
      "17-rednih + 1-violet-NAKNADNI = 18 BREZ preskokov (8.-leto!) + DUP-8-ŠTEVILČENJA-KOLIZIJA (nova-anomalija-vrsta!)",
      "h8 = 1.-NEVESTA-poročni-dokaz-v-04455 (h8-04104-1873-krst-z65-BRODARIČ-matec-SKLAD — hišna-sinhronizacija!)",
      "PEZDIRC-MREŽA ×3-kontekst (v10-priča-Anton-Pegdire + v16-mati-'Anna-Pegedire' + v17-priča-Georg-Pegdire — NI-bloki-pošteno!) + najstarejša-nevesta-dozdaj-46-l (v13-Stubler!)",
    ],
  },
  {
    year: 1874,
    phase: "P250",
    progress: "12/13",
    entries: 32,
    griblje: 11,
    houses: 10,
    scans: "s2–s7",
    scanCount: 6,
    foliation: "Pag = sken−1 5/5 (1–5) → skupaj 28/28! (pravilo-NE-prelama!)",
    boundaryNext: "meja 1873/74 = s2-MID/DNO (P251-RE! — tail-m21-'26. Nov 1873' → restart-m1-NA-ISTI-STRANI!) · meja 1874/75 = s7→s8 (P249-1:1!)",
    boundaryVariant: "12. vrsta: restart NA DNU strani — zadnja-vrsta (s2-dno — dno-vzorec-2.-instance-cf.-P243!)",
    restart: "vpis 1 = 19. Jänner 1874 [~18-DUEL] (s2-DNO — Jakob-PAŠIČ-34 × Anna-KUNIČ-34-WITWA-Z-OTROKI-NI-blok!)",
    highlights: [
      "★★★★★ KNIŽNO-ODPIRANJE-04455: s1-VEZALO → 'Pag. 1' = s2-TOP = m18-'1873-Juni-11' (knjiga-se-odpre-SREDI-ŠTEVILČENJA-1873!)",
      "11-BLOKOV = NOV-REKORD (prej-6!-×1,83!) + 10-DVIGOV-V-1-LETU-REKORD (h43 +34 = NOV-ABSOLUTNI-1908→1874! + h29 +23-izenači-h44!)",
      "3-MNOŽIČNI-DANI ('8. Februar' ×5 + '11. Februar' ×5 = 10-POROK-V-2-DNEH! + '14. Juni' ×2)",
      "H43-BRULA-PARALELA (Marina-1874 == Katharina-1878 — ISTA-HIŠA-ISTA-PRIIMEK!) + h42-PROMOCIJA (Maria-Pegdirc-1874 == Georg-Pegdirc-1879!)",
      "HRIŽAN ×4 + MILEK ×3 (m5-h65 + m16-h29 + priča-Marcus!) + 52-l-nevesta = NAJSTAREJŠA-REKORD (m10-VIPAVEC!) + 63-l-ženin ×2 + MLADOLETNICA ×2 + P249-KOREKCIJA-m28 ('28.-Februar'→'28.-Avgust'!)",
    ],
  },
  {
    year: 1873,
    phase: "P251",
    progress: "13/13",
    entries: 4,
    griblje: 4,
    houses: 4,
    scans: "s1–s2 (+s3-križna-meja)",
    scanCount: 2,
    foliation: "Pag = sken−1 1/1 (s2-'Pag. 1' NA ODPRTANJU!) → SKUPAJ 29/29! (pravilo-drži-NA-ODPIRANJU-knjige!)",
    boundaryNext: "meja 1873/74 = s2-MID/DNO = 13.-VARIANTA-RE (m21-'26. Novembris 1873' → m1-'1874-Jänner-19.'-NA-ISTI-STRANI!)",
    boundaryVariant: "13. vrsta: meja SREDI strani brez finis/glave (s2-mid/dno — 13.-VARIANTA-1:1-RE-VERIFIKACIJA!)",
    restart: "vpis 1 = m18 (11. Juni 1873, s2-top — prva-marginala-NA-STRANI = 18: m1–m17-V-PREDHODNIKU-knjige!)",
    highlights: [
      "★★★★★ KONČNA-POTRDITEV-KNIŽNEGA-ODPIRANJA (s1 = VEZALO-knjige → s2 = 'Pag. 1' = PRVA-tabelarna-stran → prva-marginala-18 = m1–m17-leta-1873-V-PREDHODNIKU — 1873 = SAMO m18–m21!)",
      "2-POLNA-DVOJNA = 50%-količnik-REKORD (m18-h13×h62-GABOVŠIČ×HRIŽAN + m20-h22×h50-MILEK×PEGDIRE!)",
      "4-DVIGI (h22 +25 = 2.-največji! + h62 +20 = 3.-največji! + h13 +9 + h50 +6!)",
      "DOVGAN-13-LET (1873–1885!) + PEZDIRC-13/13-LET-VSEH (Maria-PEGDIRE-oče-Marcus — P249-napoved-IZPOLNJENA-KOT-BLOK!)",
      "m19-KLAGENFURT-MIGRANT-'von…IBERER'-1.-TE-VRSTE [X-OPEN!] + m21-'VETRHVIŠČE' [X-OPEN-VAS!] + MILEK ×2 + HRIŽAN ×3 + ŠIMEC ×3 + KUNIČ ×3",
    ],
  },
];

/** PEZDIRC/PEGDIRE-grafija-continuum po letih (omenjene vrstice — vpisi; [~]-garble pošteno štet). */
export const PEZDIRC_MARRIAGE_PER_YEAR: { year: number; count: number }[] = [
  { year: 1885, count: 3 },
  { year: 1884, count: 4 },
  { year: 1883, count: 1 },
  { year: 1882, count: 5 },
  { year: 1881, count: 1 },
  { year: 1880, count: 2 },
  { year: 1879, count: 2 },
  { year: 1878, count: 2 },
  { year: 1877, count: 1 },
  { year: 1876, count: 9 },
  { year: 1875, count: 3 },
  { year: 1874, count: 1 },
  { year: 1873, count: 1 },
];

/** Skupni PEZDIRC-omembe 1873–1885 (×35 vrstic — edini priimek v VSEH 13 letih!). */
export const PEZDIRC_MARRIAGE_TOTAL = PEZDIRC_MARRIAGE_PER_YEAR.reduce((s, y) => s + y.count, 0);

/** Križnoletne niti sinteze P252 (P236-vzorec). */
export const MARRIAGE_EARLY_THREADS: CrossThread[] = [
  {
    id: "pezdirc-marriage",
    nameSi: "PEZDIRC/PEGDIRE-continuum (×35 vrstic / 13/13 let)",
    nameEn: "The PEZDIRC/PEGDIRE continuum (×35 rows / 13/13 years)",
    summarySi:
      "Edini priimek, prisoten v VSEH 13 letih predzgodovine — grafija-continuum PEZDIRC/PEGDIRE/Pegdire/PEGDIČ/PERDIRC/'Prodaric'[~]; vrhunec 1876 (×9 = REKORD predzgodovine — 4 bloki od 6 + 'Leinmannstochter' ×2!), dno 1877/1883 (×1). Predzgodovina nadaljuje 04104-krstni-continuum ×131 (P236) — skupaj PEZDIRC v 28 od 28 let (1871–1885 = obe predzgodovini + vse 4 knjige!).",
    summaryEn:
      "The only surname present in ALL 13 prehistory years — a grapheme continuum PEZDIRC/PEGDIRE/Pegdire/PEGDIČ/PERDIRC/'Prodaric'[~]; the peak 1876 (×9 = the prehistory record — 4 blocks of 6 + 'Leinmannstochter' ×2!), the bottom 1877/1883 (×1). The prehistory continues the 04104-baptismal continuum ×131 (P236) — together PEZDIRC in 28 of 28 years (1871–1885 = both prehistories + all four books!).",
    detailSi:
      "P238 ×3 (h71-priča + h29-ženin-Georg + h13-mati) · P239 ×4-ženini (v1-Martin + v2-Mathias-ista-hiša! + v14-Janez + v15-Matthias) + priče [~]×3 · P240 ×1 (v4-Miha-črka-za-črko-'NI-Pegdirc'!) + v5/v7 [~] · P241 ×5-vpisov (v9-OBA-PEZDIRC — ženin+nevesta+starši+priča-×4-v-1-vpisu! + v15 + v16 + v18 + v20-priča) · P242 ×1 (v7-starši-'Michael-Kathar.-PEZDIREC-½-Gübly' — PRED-ČASI) · P243 ×2 (v14-Magdalena-PEGDIREC-hči-Marka + v20-Peter-PERDIRC) · P244 ×2-ženinov (v7 + v21-Georg-PEGDIRC-h42 — h42-PARALELA!) · P246 ×2-garble (v10-PEGDIRIC + v20-PEGDIČ — izven-Griblje-NI-bloki) · P247 ×1 [~] (v5-'Prodaric' — NI-blok-pošteno!) · P248 ×9-REKORD (v1+v8+v9+v13+v14 — ×4-bloki-od-6 + 'Leinmannstochter'×2 + 2×-Georg-Pegdire-oče!) · P249 ×3-kontekst (v10+v16+v17 — NI-bloki) · P250 ×1 (m32-Maria-Pegdirc-h42-PROMOCIJA! + 1873-kontekst-m20) · P251 ×1 (m20-Maria-PEGDIRE-h50-oče-Marcus!).",
    detailEn:
      "P238 ×3 · P239 ×4 grooms (+[~]×3) · P240 ×1 (v4 letter-by-letter-'NOT-Pegdirc'!) · P241 ×5 entries (v9 BOTH-PEZDIRC — ×4 mentions in one entry!) · P242 ×1 (v7-parents-'PRED-ČASI'!) · P243 ×2 · P244 ×2 grooms (incl. v21-Georg-PEGDIRC — the h42-PARALLEL!) · P246 ×2 garbles (outside-Griblje — honestly NOT blocks!) · P247 ×1 [~] ('Prodaric' — honestly NOT a block!) · P248 ×9-THE-RECORD (×4-blocks-of-6 + 'Leinmannstochter'×2 + twice-Georg-Pegdire-the-father!) · P249 ×3-context (NOT blocks!) · P250 ×1 (m32-Maria-Pegdirc — the h42-PROMOTION!) · P251 ×1 (m20-Maria-PEGDIRE — father Marcus!).",
    xOpen: "'Leinmannstochter' ×2 (1876 v13+v14) — PEGDIRE-LEINWEBER-DRUŽINA? (cf. P80-h13-'Leinann'-nit + P243-h63-'dekla'!) + 2×-Georg-Pegdire-oče (v9-Anna-TOME-vs-v13-Anna-BRINC — 2 ženi-kandidata [X-OPEN]?)",
  },
  {
    id: "dovgan-marriage",
    nameSi: "DOVGAN-continuum (13 let — 1873–1885!)",
    nameEn: "The DOVGAN continuum (13 years — 1873–1885!)",
    summarySi:
      "Franz Dovgan [~Dorgan/Dergan/Dorgun/Dorejan/Lovgan-garble-iste-roke!] podpisuje VSA 13 let predzgodovine — v 1883/1884/1885 EDINI duhovnik VSEH vpisov; v ostalih letih dominanta. P250-'12-let' PODALJŠAN na 13 ZA 1 LETO NAZAJ NA ODPRTANJU knjige (P251: m18+m20+m21-isti-roka-×3-parafa-'M.'!).",
    summaryEn:
      "Franz Dovgan [~ the garble of one hand!] signs ALL 13 prehistory years — in 1883/1884/1885 the ONLY priest of ALL entries; in the remaining years the dominant. The P250-'12-years' EXTENDED to 13 by one year BACK AT THE OPENING of the book (P251: m18+m20+m21 — the same hand ×3, the 'M.'-paraph!).",
    detailSi:
      "IZJEMI: 1875-violet-NAKNADNI-8 = kaplan-Daniel-Perschek (1.-in-EDINI-zagotovljeni-ne-Dovgan-podpis — kaplan-SAMO-NA-NAKNADNEM-vpisu!) + m19-1873-'Daniel-TERŽEK' [~'Dames-FERCHER'-MISREAD-kand.-X-OPEN!] + m27-1874-'Hegrič' [~X-OPEN-na-REDNEM-vpisu!]. Poseben-dokaz: s35-tail-'Copulatus sum Griblje d. 14/9 1879. Dopgan' + modri-pripis-'Anton-Franz-von-Dovgan-Dechant' [~X-OPEN!].",
    detailEn:
      "The exceptions: the 1875-violet-SUPPLEMENTARY-8 = the curate Daniel Perschek (the 1st and ONLY verified non-Dovgan signature — the curate ONLY on the supplementary entry!) + m19-1873-'Daniel TERŽEK' [~X-OPEN!] + m27-1874-'Hegrič' [~X-OPEN]. A special proof: the s35-tail-'Copulatus sum Griblje d. 14/9 1879. Dopgan' + the blue annotation 'Anton Franz von Dovgan Dechant' [~X-OPEN!].",
    xOpen: "m19-TERŽEK/FERCHER-garble (1873) + m27-'Hegrič' (1874) — 3. in 4. duhovnik-kandidata brez neodvisnega dokaza!",
  },
  {
    id: "foliacija-marriage",
    nameSi: "FOLIACIJA 'Pag. = sken−1' (29/29 + 1885-razširitev!)",
    nameEn: "The FOLIATION 'Pag. = scan − 1' (29/29 + the 1885 extension!)",
    summarySi:
      "Pravilo potrjeno na 29 straneh 1:1 v letih 1873–1879 (serija P246–P251 — vključno NA ODPRTANJU knjige: s2 = 'Pag. 1'!) + P238-razširitev na Pag. 55–60 (1885: 3×-1:1 + P80-sidro — prej P84: samo 61–66!). Pravilo NE PRELAMA niti na foliacijskih DUELIH.",
    summaryEn:
      "The rule confirmed 29 pages 1:1 in 1873–1879 (the P246–P251 series — incl. AT THE OPENING of the book: s2 = 'Pag. 1'!) + the P238 extension to Pag. 55–60 (1885: 3× 1:1 + the P80 anchor — previously P84: only 61–66!). The rule DOES NOT BREAK even on foliation DUELS.",
    detailSi:
      "Serija po letih (faze-branj): 1873 1/1 (s2-'Pag. 1' + kljukica-ozanka!) · 1874 5/5 (Pag. 1–5) · 1875 4/4 (Pag. 6–9) · 1876 4/4 (Pag. 10–13) · 1877 4/4 (Pag. 14–17) · 1878 6/6 (Pag. 18–23 — 2-VLM-misreada-KOREKCIJA!) · 1879 5/5 (Pag. 25–34 — s35-tail) = 29/29! DUELI pošteno rešeni/odprti: 1880-s38-'34'-vs-'37' (REŠENO-s-P244: 0-vs-7-Kurrent!) + 1882-s45-'93/94' [~X-OPEN-odprto] + 1885-s56-'55/35'-misreadi-dokumentirani.",
    detailEn:
      "The series by year (reading phases): 1873 1/1 · 1874 5/5 · 1875 4/4 · 1876 4/4 · 1877 4/4 · 1878 6/6 (2 VLM misreads corrected!) · 1879 5/5 = 29/29! The DUELS honestly resolved/open: 1880-s38 (RESOLVED by P244!) + 1882-s45-'93/94' [~X-OPEN] + 1885 documented misreads.",
    xOpen: "1882-s45-'93/94' (Pag. = sken−1 bi zahteval 44 — [~X-OPEN-pošteno-odprto-cf.-P149-dup-list!])",
  },
  {
    id: "meje-marriage",
    nameSi: "MEJNE VARIANTE (13 let = 13 slogov!) + FINIS-SODA-vzorec",
    nameEn: "The BOUNDARY VARIANTS (13 years = 13 styles!) + the FINIS-EVEN pattern",
    summarySi:
      "VSAKO leto ima svoj SLOG meje/restarta — sosednja leta se NE ponavljajo: velika glava na restartu (1884) · števke čez stolpce (1883) · glava PRED vrstico (1882) · letnica v datumskem stolpcu (1881/1875) · restart na dnu strani (1880/1874!) · glava ponovljena na vsakem listu (1879) · inline brez ponovitve (1878/1877!) · restart brez letnice + violet-naknadni (1876) · margina-'21'-pisarska-napaka (1875) · meja sredi strani brez finis (1873!). Izhodiščna številčenja 1.–13. z vrzeljo 6 [~ pošteno odprto].",
    summaryEn:
      "EVERY year has its own boundary/restart STYLE — neighbouring years do NOT repeat: the big heading at the restart (1884) · the digits across the columns (1883) · the heading BEFORE row 1 (1882) · the year in the date column (1881/1875) · the restart at the page bottom (1880/1874!) · the heading repeated on every page (1879) · inline without repetition (1878/1877!) · a restart without the year + the violet supplementary (1876) · the margin-'21' scribe's error (1875) · the boundary mid-page without finis (1873!). The original numbering 1.–13. with a gap at 6 [~ honestly open].",
    detailSi:
      "★★★ FINIS-SODA-VZOREC: okrasna zaključna oznaka 'finis / 1-8-7-X' SAMO v SODIH letih — 4 instance (1874-'f-i-n-i-s/-1-8-7-4' + 1876 + 1878-'FINIS PRO ANNO 1878' + 1880-'finis / s 1880'!), LIHA leta BREZ (1875/1877/1879 konzistentno — [~X-OPEN-vzorec]) · ★★★ KNIŽNO-ODPIRANJE-04455 (s1 = VEZALO → s2 = 'Pag. 1' — knjiga se odpre SREDI številčenja 1873: m1–m17 v PREDHODNIKU!) · RE-NUMBERING-s18-1877 (+1-×4-prečrtanih!) + DUP-8-1875 (kolizija!) = 2 vrsti popravkov številčenja.",
    detailEn:
      "★★★ The FINIS-EVEN pattern: the ornamental year-end mark 'finis / 1-8-7-X' ONLY in EVEN years — 4 instances (1874 + 1876 + 1878-'FINIS PRO ANNO' + 1880!), the ODD years without (1875/1877/1879 consistently!) · ★★★ The BOOK OPENING (s1 = the binding → s2 = 'Pag. 1' — the book opens MID-NUMBERING of 1873: m1–m17 in a predecessor!) · The RE-NUMBERING-s18-1877 (+1 over 4 struck-outs!) + the DUP-8-1875 (a collision!) = 2 kinds of numbering corrections.",
    xOpen: "FINIS-SODA-vzorec [~X-OPEN: vzorec-SODA-let-1874/1876/1878/1880-potrjen-v-4-instancah — liha-BREZ — splošna-slika-2026!] + izvirna-številčenja-variant-z-vrzeljo-6 [~pošteno-odprto]",
  },
  {
    id: "hise-marriage",
    nameSi: "Hišni continui + firstYear-DVIGI (26 dvigov — vsako leto nazaj = NOV dvig!)",
    nameEn: "The house continuums + the firstYear LIFTS (26 lifts — every year back = a NEW lift!)",
    summarySi:
      "Pošteni vzorec: VSAKO nazadnje prebrano leto je PONOVNO povišalo firstYear prej prebranih let — 26 izmerjenih dvigov: absolutni rekordi h43 +34 (1908→1874!) in h44 +23 (1899→1876!) + h22 +25 (1898→1873! — 2. največji). Skupaj z izenačenji (h29 = h44 +23) in PROMOCIJAMI (h42 1890→1874: tail-kontekst→blok!).",
    summaryEn:
      "The honest pattern: EVERY newly-read year back RE-LIFTED the firstYear of previously-read years — 26 measured lifts: the absolute records h43 +34 (1908→1874!) and h44 +23 (1899→1876!) + h22 +25 (1898→1873! — the 2nd largest). Together with the equalings (h29 = h44 +23) and the PROMOTIONS (h42 1890→1874: a tail-context→block!).",
    detailSi:
      "P241 (1882): h53 +8 → P243 (1880): h53 +10 (KONČNO!) · P242 (1881): h52 +1 · P247 (1877): h10 +10 + h69 +10 + h8 +4 · P248 (1876): h31 +10 + h44 +23-REKORD + h35 +6 + h64 +12 + h41 +5 + h30 +13 · P250 (1874): h4 +7 + h7 +15 + h10 +3 + h27 +7 + h29 +23-izenači + h30 +2 + h33 +14 + h42 +5-PROMOCIJA + h43 +34-NOV-ABSOLUTNI + h65 +12 · P251 (1873): h13 +9 + h62 +20 + h22 +25 + h50 +6. Hišne sinhronizacije: 1878 9/10 SKLAD (novi-samo-h47!) + h13-MERGE/h36-MERGE (P80-sidra!) + h8 = 1.-NEVESTA-dokaz (04104-1873-krst-SKLAD!) + h51 = 1.-04455-blok-kadarkoli (PT-luknja — najtanjša-hiša-P191: 4 bloki samo-predzgodovina!).",
    detailEn:
      "P241 (1882): h53 +8 → P243 (1880): h53 +10 (FINAL!) · P242 (1881): h52 +1 · P247 (1877): h10 + h69 (both +10) + h8 +4 · P248 (1876): 6 lifts incl. h44 +23-THE-RECORD · P250 (1874): 10 lifts incl. h43 +34-THE-NEW-ABSOLUTE + the h42-PROMOTION · P251 (1873): h13 +9 + h62 +20 + h22 +25 + h50 +6. The house synchronizations: 1878 9/10 (only h47 new!) + the h13/h36-MERGES (P80 anchors!) + h8 = the 1st BRIDE evidence + h51 = the 1st-ever 04455 block (the PT-gap house — the thinnest of P191: 4 blocks, prehistory only!).",
    xOpen: "h51 (4 bloki — SAMO predzgodovina 1877: MOH-trojček + h51-1881-krst-mati-BRODARIČ-paralela 4 let kasneje!)",
  },
  {
    id: "vzorci-marriage",
    nameSi: "Vzorci: MNOŽIČNI-DANI · POLNI-DVOJNI · IZMENA-VLOG · MLADOLETNICE",
    nameEn: "Patterns: MASS-DAYS · FULL-DOUBLES · ROLE-SWAPS · MINOR-BRIDES",
    summarySi:
      "MNOŽIČNI-DANI: '4. Februar 1875' ×10-REKORD + 1874 '8. Feb' ×5 + '11. Feb' ×5 (10 porok v 2 dneh!) + '14. Juni' ×2. POLNI-DVOJNI (oba iz Griblje!): 1873 2/4 = 50%-REKORD + 1874 2-v-11 + 1884 2-pora + 1876-v1/v8-INTRA. IZMENA-VLOG ×4 (1882-v6/v7 + 1876-v3/v4 + v6/v7-Štefanič + m21-GABOVŠIČ×GABOFAIČ!). MLADOLETNICE: m5-19-l-Konsens-k.k. + v16-Mötthling + v13-'PRO-DIE-MINDERJ.' + m18-17-l.",
    summaryEn:
      "MASS-DAYS: 'Feb 4, 1875' ×10-THE-RECORD + 1874 'Feb 8' ×5 + 'Feb 11' ×5 (10 weddings in 2 days!) + 'Jun 14' ×2. FULL-DOUBLES (both from Griblje!): 1873 2/4 = the 50% record + 1874 2-in-11 + 1884 2-pairs + 1876-v1/v8-INTER. ROLE-SWAPS ×4. MINOR-BRIDES: m5-19-with-a-court-consent + v16 + v13-'PRO-DIE-MINDERJ.' + m18-17.",
    detailSi:
      "Sestrski-pari: h34-SILAH (1884-Maria + 1885-Barbara!) + HROVALJ-brat+sestra-ISTI-DAN-1883 + MOH×BRODARIČ-1877 (dvojni-sorodstveni-zakon-1.×!) + v6/v7-TOMC/Berčopec-1882. Nastarejša nevesta 52-l (m10-VIPAVEC-1874-REKORD!) + najmlajša 16-l. KRIŽAN-nit-5-let (h63-1878/1879/1880!). DATUMSKI-VZOREC mesec-samo-ob-spremembi (1875!) + P249-KOREKCIJA-m28 ('28.-Februar'→'28.-Avgust'!).",
    detailEn:
      "The sister-pairs: h34-SILAH (1884+1885!) + the HROVALJ brother+sister the same day 1883 + the MOH×BRODARIČ-1877 double-in-law-wedding (a 1st!) + the 1882 role-swap. The oldest bride 52 (m10-1874-THE-RECORD!) + the youngest 16. The KRIŽAN 5-year thread (h63 1878/1879/1880!). The date pattern month-only-on-change (1875!) + the P249-CORRECTION m28.",
    xOpen: "m29–m31-1874-leta-kronološko-nemogoča-po-'28.-Avgust' [~X-OPEN — P251+-re-verifikacija!] + m19-IBERER + m21-VETRHVIŠČE (1873-X-OPEN-konteksta!)",
  },
];

/** X-open preostanki sinteze (P252 — pošteno odprti [~]). */
export const MARRIAGE_EARLY_X_OPEN: {
  id: string;
  titleSi: string;
  titleEn: string;
  bodySi: string;
  bodyEn: string;
}[] = [
  {
    id: "leinmannstochter",
    titleSi: "'Leinmannstochter' ×2 (1876)",
    titleEn: "the 'Leinmannstochter' ×2 (1876)",
    bodySi:
      "v13-Maria-PEGDIRE-'Leinmannstochter'-Gri.šte-41 + v14-Anna-PEGDIRE-'Leinmannstochter'-Griblje-30 — PEGDIRE-LEINWEBER-družina-kandidat [X-OPEN]: če sta hči istega očeta (2×-Georg-Pegdire-oče — v9-Anna-TOME-vs-v13-Anna-BRINC!), potem 'Leinann/Leinweber'-grafija (P80-h13-nit + P243-h63-'dekla' + P241-v26-'Leinannin') pomeni isti poklic-družino.",
    bodyEn:
      "v13-Maria + v14-Anna PEGDIRE both 'Leinmannstochter' — the PEGDIRE-WEAVER-family hypothesis [X-OPEN]: if both are daughters of the same father (twice-Georg-Pegdire!), then the 'Leinann/Leinweber' graphy (the P80-h13 thread) denotes the same occupational family.",
  },
  {
    id: "prodaric-1877",
    titleSi: "v5-'Prodaric' (1877) — PEZDIRC-garble?",
    titleEn: "the v5-'Prodaric' (1877) — a PEZDIRC garble?",
    bodySi:
      "P247-v5-nevesta-'Prodaric'[~PEZDIRC-garble-kandidat!]-BRODARIČ-2:1-korpus-nit — iskreno [~]: NI blok (h8-1873-mati-Anna-BRODARIČ-3/3 + h31-1879-mati-BRODARIČ + h51-1881-mati-BRODARIČ!). Preostanek odprt brez neodvisnega dokaza.",
    bodyEn:
      "The P247-v5 bride 'Prodaric' [~a PEZDIRC garble candidate] — honestly [~]: NOT a block (the BRODARIČ corpus thread remains). Open without independent proof.",
  },
  {
    id: "vas-dueli-1885",
    titleSi: "3-vas-dueli 1885 (h29/h15/h9)",
    titleEn: "the 3-village duels of 1885 (h29/h15/h9)",
    bodySi:
      "vpis-11-'Gern/Gornje-29'-vs-GRIBLJE-29 (h29-Mileh-epidemija-1886-PRED-1-leto!) + vpis-12-'Glob./Woh.-15'-vs-GRIBLJE-15 (h15!) + vpis-13-GRIBLJE-9? (h9!) — trije vpisi na meji bloka pošteno ostajajo odprti.",
    bodyEn:
      "The entry-11 'Gern/Gornje-29' vs GRIBLJE-29 + the entry-12 'Glob./Woh.-15' vs GRIBLJE-15 + the entry-13 GRIBLJE-9? — three entries on the block boundary stay honestly open.",
  },
  {
    id: "duhovniki-izjeme",
    titleSi: "duhovniške izjeme: TERŽEK/Hegrič (1873/1874)",
    titleEn: "the priest exceptions: TERŽEK/Hegrič (1873/1874)",
    bodySi:
      "m19-1873-'Daniel-TERŽEK' [~'Dames-FERCHER'-MISREAD-kand.-X-OPEN!-6×-krop-'T'-z-vodoravno-'z/ž'-zanka!] + m27-1874-'[Justinius?]-HEGRIČ'-NA-REDNEM-vpisu [~X-OPEN] — 3. in 4. duhovnik-kandidata kontinuuma brez neodvisnega dokaza (edini ZAGOTOVLJENI ne-Dovgan = kaplan-Perschek-1875-violet!).",
    bodyEn:
      "m19-1873-'Daniel TERŽEK' [~X-OPEN!] + m27-1874-'Hegrič' on a REGULAR entry [~X-OPEN] — the 3rd and 4th priest candidates of the continuum without independent proof (the only VERIFIED non-Dovgan = the curate Perschek 1875!).",
  },
  {
    id: "m19-m21-1873",
    titleSi: "m19-IBERER-KLAGENFURT + m21-VETRHVIŠČE (1873)",
    titleEn: "m19-IBERER-KLAGENFURT + m21-VETRHVIŠČE (1873)",
    bodySi:
      "m19-ženin-'von-Josef-Narzis-IBERER-[~Überer]-h.h.-Leining-genannt…'-34-l-KLAGENFURT-34-[~348]-MIGRANT = uradnik/plemič-vzorec-1.-TE-VRSTE [X-OPEN] + m21-'VETRHVIŠČE'-12-×-10 [X-OPEN-VAS!] — edini predzgodovinski konteksti z nerazrešeno lokacijo.",
    bodyEn:
      "m19-the-groom-'IBERER'-34-KLAGENFURT = an official/nobleman pattern of the 1st kind [X-OPEN] + m21-'VETRHVIŠČE' [X-OPEN-a-VILLAGE!] — the only prehistory contexts with an unresolved location.",
  },
];

/** Skupne statistike linije (izpeljano, konsistentno z MARRIAGE_EARLY_LINE_YEARS). */
export const MARRIAGE_EARLY_TOTALS = {
  years: MARRIAGE_EARLY_LINE_YEARS.length,
  entries: MARRIAGE_EARLY_LINE_YEARS.reduce((s, y) => s + y.entries, 0),
  griblje: MARRIAGE_EARLY_LINE_YEARS.reduce((s, y) => s + y.griblje, 0),
  restarts: 13,
  boundaryVariants: "1.–13.",
  finisInstances: 4,
  label: "Podzemelj P 1873–1922",
} as const;

/** Živi seštevek za qa-p252: Griblje-bloki po letih IZ parish-synthesis (mora = parish.ts bloki). */
export function marriageGribljeByYear(): Map<number, number> {
  return new Map(MARRIAGE_EARLY_LINE_YEARS.map((y) => [y.year, y.griblje]));
}
