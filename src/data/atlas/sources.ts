// ATLAS 1825 — arhivski viri in registri
// Recovery: stari atlas podatkovni model (atlas-map-data-model-1825, knowledge-graph-1825,
// story-graph-1825, georef-1825, parcel-register-1825, cadastre-a01) v NOBENEM od
// recovery virov (bundle, arhivski repozitoriji, diski, Vercel deploymenti) ni bil najden.
// Nadomeščeno z DEJANSKIMI javnimi arhivskimi viri: Arhiv Republike Slovenije,
// fond SI AS 176 (Franciscejski kataster za Kranjsko), katastrska občina Griblje (N83).
// Fizični viri preverjeni 2026-10-07 prek VAČ (Virtualna arhivska čitalnica).

export type SourceType =
  | "cadastral-map"
  | "sketch"
  | "boundary-description"
  | "parcel-register"
  | "building-protocol"
  | "owner-register"
  | "land-use"
  | "valuation"
  | "heritage-register"
  | "archival-mention";

/** strojno berljiv status prenosa digitalne kopije (issue #3 #11) */
export type TransferStatus =
  | "TRANSFERRED" /** digitalna kopija v repozitoriju */
  | "TO_COLLECT" /** enota je digitalizirana, kopija še ni prenesena */
  | "NOT_DIGITIZED" /** enota obstaja, a ni digitalizirana */
  | "NOT_APPLICABLE";

/** strojno berljiv status georeference (issue #3 #11) */
export type GeorefStatus =
  | "GEOREFERENCED"
  | "TO_COLLECT"
  | "NOT_APPLICABLE";

/** strojno berljivi statusi raziskave vsakega zgodovinskega podatka (issue #3 #13) */
export type ResearchStatus =
  | "VERIFIED"
  | "DOCUMENTED"
  | "REVIEW"
  | "RECONSTRUCTED"
  | "INFERRED"
  | "TO_COLLECT"
  | "NOT_FOUND"
  | "NOT_PUBLIC";

export interface AtlasSource {
  id: string;
  code: string;
  type: SourceType;
  titleSi: string;
  titleEn: string;
  /** oddaja v okviru N83 */
  unit?: string;
  vacId?: string;
  vacUrl?: string;
  /** datoteka v javni digitalni knjižnici (seja) */
  fileRef?: string;
  pages?: number;
  yearFrom?: number;
  yearTo?: number;
  fund: string;
  archive: string;
  licenceSi: string;
  licenceEn: string;
  thumb?: string;
  /** ali je list georeferenciran */
  georeferenced?: boolean;
  /** strojno berljiva statusa (issue #3) */
  transferStatus?: TransferStatus;
  georefStatus?: GeorefStatus;
  /** koliko vsebinskih zapisov enote je strukturiranih v Atlasu */
  structuredEntries?: number;
  /** datum zadnje preveritve vira (YYYY-MM-DD) */
  lastVerified?: string;
  noteSi?: string;
  noteEn?: string;
}

export const ATLAS_SOURCES: AtlasSource[] = [
  {
    id: "src-a01",
    code: "N083A01",
    type: "cadastral-map",
    titleSi: "Katastrski list A01 — občina Grüble",
    titleEn: "Cadastral sheet A01 — municipality of Grüble",
    unit: "list A01",
    vacId: "227666",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227666",
    fileRef: "IIIF: /vac/iiif/raster/f919e72f-862b-3300-a8e8-4b20d7fed9e9",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/a01-thumb.jpg",
    georeferenced: true,
    transferStatus: "TRANSFERRED",
    georefStatus: "GEOREFERENCED",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "Grafični list katastrske občine Griblje (Grüble). Reka Kolpa kot vzhodna meja, naselbina v jugovzhodnem delu. Sken 2826 × 2273 px. Digitalna kopija prenesena iz VAČ IIIF; meje parcel še niso vektorsko izrisane (TO_COLLECT).",
    noteEn:
      "Graphical sheet of the Griblje (Grüble) cadastral municipality. The Kolpa river as eastern boundary, settlement in the south-east. Scan 2826 × 2273 px. Digital copy transferred from VAČ IIIF; parcel boundaries not yet vectorised (TO_COLLECT).",
  },
  {
    id: "src-a02",
    code: "N083A02",
    type: "cadastral-map",
    titleSi: "Katastrski list A02 — občina Grüble, vas s cerkvijo sv. Vidom",
    titleEn: "Cadastral sheet A02 — Grüble with St. Vitus church",
    unit: "list A02",
    vacId: "227668",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227668",
    fileRef: "IIIF: /vac/iiif/raster/fb69b6eb-c538-3249-8f1e-28d804f3d698",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/a02-thumb.jpg",
    georeferenced: true,
    transferStatus: "TRANSFERRED",
    georefStatus: "GEOREFERENCED",
    structuredEntries: 156,
    lastVerified: "2026-10-07",
    noteSi:
      "List z jedrom vasi in cerkvijo St. Veith (sv. Vid, oznaka K, stavba z apsido). Sken 3010 × 2158 px. Iz lista je vektoriziranih 156 stavbnih objektov (RECONSTRUCTED).",
    noteEn:
      "Sheet with the village core and St. Veith church (marked K, apsidal building). Scan 3010 × 2158 px. 156 building objects vectorised from the sheet (RECONSTRUCTED).",
  },
  {
    id: "src-a03",
    code: "N083A03",
    type: "cadastral-map",
    titleSi: "Katastrski list A03 — občina Grüble, vzhodni predeli z razpršenimi zaselki",
    titleEn: "Cadastral sheet A03 — municipality of Grüble, eastern dispersed hamlets",
    unit: "list A03",
    vacId: "227670",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227670",
    fileRef: "IIIF: /vac/iiif/raster (uodid 227670)",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/n83-a03-thumb.jpg",
    georeferenced: false,
    transferStatus: "TRANSFERRED",
    georefStatus: "TO_COLLECT",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "List z razpršeno poselitvijo na vzhodnem delu k.o. in z obmejnimi predeli sosednjih občin. Digitalna kopija prenesena iz VAČ IIIF (2645 × 2154 px); georeferenca še ni izračunana — poskus P8 (2026-10-08, deterministično): zasidranje na reko Kolpo (ekstrakcija pasu med bregovnimi črtami + primerjava z moderno strugo iz OpenTopoMap) je na validaciji A02 izkazalo NEDELOVITNOST — Kolpa je tu premalo vijugasta za določitev smeri sever–jug in merila (napaka cerkve 0,9–1,6 km); raziskovalna pot v research/georef-n83/ (dokumentirana negativna ugotovitev; potreben VAČ metapodatek ali točkovno sidro).",
    noteEn:
      "Sheet with dispersed settlement in the eastern part of the cadastral municipality and boundary areas with neighbouring municipalities. Digital copy transferred from VAČ IIIF (2645 × 2154 px); georeference not yet computed — the P8 attempt (2026-10-08, deterministic): anchoring on the Kolpa river (bank-to-bank band extraction + comparison with the modern channel from OpenTopoMap) proved UNWORKABLE in A02 validation — the Kolpa meanders too weakly here to pin the north–south direction and scale (church error 0.9–1.6 km); research path in research/georef-n83/ (a documented negative finding; VAČ metadata or a point anchor needed).",
  },
  {
    id: "src-a04",
    code: "N083A04",
    type: "cadastral-map",
    titleSi: "Katastrski list A04 — občina Grüble, dolina Kolpe ob Adlešičih",
    titleEn: "Cadastral sheet A04 — municipality of Grüble, Kolpa valley by Adlešiči",
    unit: "list A04",
    vacId: "227671",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227671",
    fileRef: "IIIF: /vac/iiif/raster (uodid 227671)",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/n83-a04-thumb.jpg",
    georeferenced: false,
    transferStatus: "TRANSFERRED",
    georefStatus: "TO_COLLECT",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "List z dolino Kolpe kot vzhodno mejo in napisom sosednje občine Adlešiči (Adleschitz). Digitalna kopija prenesena iz VAČ IIIF (2645 × 2158 px); georeferenca še ni izračunana — poskus P8 (2026-10-08) prek reke Kolpe: negativna ugotovitev (see research/georef-n83/); možna prihodnja pot: napis Adleschitz kot točkovno sidro + reka [~] ob VLM dostopu.",
    noteEn:
      "Sheet with the Kolpa valley as eastern boundary and the label of the neighbouring municipality of Adlešiči (Adleschitz). Digital copy transferred from VAČ IIIF (2645 × 2158 px); georeference not yet computed — the P8 river-anchoring attempt (2026-10-08) had a negative outcome (see research/georef-n83/); a possible future path: the Adleschitz label as a point anchor + the river [~] once VLM access returns.",
  },
  {
    id: "src-a05",
    code: "N083A05",
    type: "cadastral-map",
    titleSi: "Katastrski list A05 — občina Grüble, južni predeli s poselitvijo",
    titleEn: "Cadastral sheet A05 — municipality of Grüble, southern settled outskirts",
    unit: "list A05",
    vacId: "227673",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227673",
    fileRef: "IIIF: /vac/iiif/raster (uodid 227673)",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/n83-a05-thumb.jpg",
    georeferenced: false,
    transferStatus: "TRANSFERRED",
    georefStatus: "TO_COLLECT",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "List z gručasto poselitvijo (rdeči nalič stavb in dvorišč) na vzhodnem delu in obmejnimi napisi sosednjih občin. Digitalna kopija prenesena iz VAČ IIIF (2634 × 2165 px); georeferenca še ni izračunana — poskus P8 (2026-10-08) prek reke Kolpe: negativna ugotovitev (see research/georef-n83/); reka na listu morda ni vidna (južna meja k.o. ni ob Kolpi).",
    noteEn:
      "Sheet with a clustered settlement (red tint of buildings and farmyards) in the eastern part and boundary labels of neighbouring municipalities. Digital copy transferred from VAČ IIIF (2634 × 2165 px); georeference not yet computed — the P8 river-anchoring attempt (2026-10-08) had a negative outcome (see research/georef-n83/); the river may not appear on this sheet at all (the southern k.o. boundary is not on the Kolpa).",
  },
  {
    id: "src-pg",
    code: "N083PG",
    type: "sketch",
    titleSi: "Indikacijska skica",
    titleEn: "Indication sketch",
    unit: "Skica",
    vacId: "373413",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373413",
    fileRef: "N083PG.pdf (1 stran)",
    pages: 1,
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pg-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 1,
    lastVerified: "2026-10-07",
  },
  {
    id: "src-pr",
    code: "N083PR",
    type: "boundary-description",
    titleSi: "Opis meje — Grenz-Beschreibung der Gemeinde „GRÜBLE“",
    titleEn: "Boundary description of the municipality of “GRÜBLE”",
    unit: "Opis meje",
    vacId: "373414",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373414",
    fileRef: "N083PR.pdf (4 strani)",
    pages: 4,
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pr-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 10,
    lastVerified: "2026-10-07",
    noteSi: "Opis meje v nemščini (Kurrent) — prepis iz leta 1825 ni izdelan (TO_COLLECT).",
    noteEn: "Boundary description in German (Kurrent script) — transcription not made yet (TO_COLLECT).",
  },
  {
    id: "src-ps",
    code: "N083PS",
    type: "parcel-register",
    titleSi: "Seznam zemljiških parcel",
    titleEn: "Register of land parcels",
    unit: "Seznam zemljiških parcel",
    vacId: "373415",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373415",
    fileRef: "N083PS.pdf (143 strani)",
    pages: 143,
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-ps-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 12,
    lastVerified: "2026-10-07",
    noteSi: "143 strani zemljiških parcel po sekcijah — prepis iz 1825 ni izdelan (TO_COLLECT). Parcelne vrstice iz dokumenta so v pripravljenem podatkovnem modelu (20 vrstic).",
    noteEn: "143 pages of land parcels by sections — the 1825 transcription not made yet (TO_COLLECT). Parcel rows from the document sit in a prepared data model (20 rows).",
  },
  {
    id: "src-pt",
    code: "N083PT",
    type: "building-protocol",
    titleSi: "Protokol stavbnih parcel — Protocoll der Bau Parcellen der Gemeinde „GRÜBLE“",
    titleEn: "Protocol of building parcels of the municipality of “GRÜBLE”",
    unit: "Seznam stavbnih parcel",
    vacId: "373416",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373416",
    fileRef: "N083PT.pdf (8 strani)",
    pages: 8,
    yearFrom: 1825,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pt-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 84,
    lastVerified: "2026-10-08",
    noteSi:
      "Glavni vir hišnega registra ~1825: hišne številke 1–99 z lastniki in parcelnimi sklici. Issue #17: pregled 101 vrstice (81 potrjenih, 15 popravkov, 4 manjkajoče). P3 paleografska preverba (2. krog, 2026-10-08): popravki APLICIRANI — 84 stavbnih vrstic (renumeracija str. 4: hiše 35–40, prečrtana dvojnica 34, hiša 41 ne obstaja; lastniki Veith/Lebing/Bödig/Brinig/Strauß/Ihmeyer/Zollamt; dodane vrstice 7/71½/76½/99). Statusi ostajajo REVIEW (strojno branje; dokončna potrditev = človeška paleografija).",
    noteEn:
      "Primary source of the ~1825 house register: house numbers 1–99 with owners and parcel references. Issue #17: review of 101 rows (81 confirmed, 15 corrections, 4 missing). P3 palaeographic verification (2nd pass, 2026-10-08): corrections APPLIED — 84 building rows (the p. 4 renumbering: houses 35–40, the struck duplicate 34, house 41 does not exist; owners Veith/Lebing/Bödig/Brinig/Strauß/Ihmeyer/Zollamt; added rows 7/71½/76½/99). Statuses stay REVIEW (machine reading; final confirmation = human palaeography).",
  },
  {
    id: "src-pua",
    code: "N083PUA",
    type: "owner-register",
    titleSi: "Abecedni seznam lastnikov zemljišč",
    titleEn: "Alphabetical register of land owners",
    unit: "Abecedni seznam lastnikov zemljišč",
    vacId: "373417",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373417",
    fileRef: "N083PUA.pdf (49 strani)",
    pages: 49,
    yearFrom: 1825,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pua-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 43,
    lastVerified: "2026-10-08",
    noteSi:
      "Lastniki po abecedi s hišnimi številkami in parcelami po sekcijah I–V. Prepisane strani A–B (21 lastnikov, navzkrižno preverjanje s PT) + issue #17: strani 3–10 (18 vnosov) + P3 (2026-10-08): stran 11, črka H — 4 vnosi (Hlebety/Huditsch/Husitsch Baron von Gradatz/Hutweiz zu Waldendorf). Skupaj 43 strukturiranih vnosov na 11/49 strani; strani 12–49 (H–Ž) ostajajo TO_COLLECT — P3: branje 12–20 prekinjeno (VLM gateway nedosegljiv po resetu peskovnika).",
    noteEn:
      "Owners alphabetically with house numbers and parcels by sections I–V. Transcribed pages A–B (21 owners, cross-checked with PT) + issue #17: pages 3–10 (18 entries) + P3 (2026-10-08): page 11, letter H — 4 entries (Hlebety/Huditsch/Husitsch Baron von Gradatz/Hutweiz zu Waldendorf). 43 structured entries over 11/49 pages; pages 12–49 (H–Ž) remain TO_COLLECT — P3: reading 12–20 interrupted (VLM gateway unreachable after the sandbox reset).",
  },
  {
    id: "src-pv",
    code: "N083PV",
    type: "land-use",
    titleSi: "Izkaz rabe zemljišč",
    titleEn: "Statement of land use",
    unit: "Izkaz rabe zemljišč",
    vacId: "373418",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373418",
    fileRef: "N083PV.pdf (1 stran)",
    pages: 1,
    yearFrom: 1825,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pv-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 10,
    lastVerified: "2026-10-07",
  },
  {
    id: "src-pz",
    code: "N083PZ",
    type: "valuation",
    titleSi: "Katastrski cenilni elaborat",
    titleEn: "Cadastral valuation elaborate",
    unit: "Katastrski cenilni elaborat",
    vacId: "373419",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373419",
    fileRef: "N083PZ.pdf (71 strani)",
    pages: 71,
    yearFrom: 1825,
    yearTo: 1830,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pz-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 10,
    lastVerified: "2026-10-07",
    noteSi: "Cenilni elaborat 71 strani — prepis ni izdelan (TO_COLLECT).",
    noteEn: "Valuation elaborate, 71 pages — transcription not made yet (TO_COLLECT).",
  },
  // Zunanji registri in poznejši viri — jasno ločeni od N83
  {
    id: "src-as749",
    code: "SI AS 749/3/8/12",
    type: "archival-mention",
    titleSi:
      "Izpisek zemljiških parcel iz katastrskih davčnih vpisnikov za davčne občine Vinji Vrh, Kot, Griblje, Kaltersberg, Loka, Petrova vas in Krasinec v gospostvih Krupa in Pobrežje za namene zemljiške odveze",
    titleEn:
      "Extract of land parcels from the cadastral tax registers for the tax municipalities of Vinji Vrh, Kot, Griblje, Kaltersberg, Loka, Petrova vas and Krasinec in the lordships of Krupa and Pobrežje for the purposes of land release",
    vacId: "4971617",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=4971617",
    yearFrom: 1851,
    yearTo: 1853,
    fund: "SI AS 749 Gospostva Krupa, Pobrežje in Pusti Gradac (1587–1901)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (konec nedostopnosti 31. 12. 1900)",
    licenceEn: "publicly accessible (closure ended 31 Dec 1900)",
    transferStatus: "NOT_DIGITIZED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "Potrjena enota v VAČ (2 zvezka, nemški Kurrent, prejšnja signatura fasc. 58). Enota je javno dostopna, a NI digitalizirana — vpogled le v čitalnici Arhiva RS. Vir za kasnejšo plast 1851–1853 in povezavo parcel skozi čas; digitalizacija je predlagan naslednji korak (TO_COLLECT).",
    noteEn:
      "Confirmed unit in VAČ (2 volumes, German Kurrent, previous signature fasc. 58). Publicly accessible but NOT digitized — consultation in the Arhiv RS reading room only. Source for the later 1851–1853 layer and parcel links through time; digitisation is the proposed next step (TO_COLLECT).",
  },
  {
    id: "src-as1138",
    code: "SI AS 1138/I/1204",
    type: "archival-mention",
    titleSi: "Katastrska občina Griblje — katastrski načrt (katastrski okraj Črnomelj, 1952)",
    titleEn: "Cadastral municipality Griblje — cadastral plan (Črnomelj district, 1952)",
    vacUrl: "https://vac.sjas.gov.si/vac/search/fieldSearch",
    yearFrom: 1952,
    yearTo: 1952,
    fund: "SI AS 1138",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    transferStatus: "TO_COLLECT",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "Povojni reambulirani katastrski načrt — pripravljen kot kasnejša plast za primerjavo 1825 → 1952 → danes. Natančna VAČ enota še ni identificirana (iskanje fieldSearch, TO_COLLECT).",
    noteEn:
      "Post-war reambulated cadastral plan — prepared as a later layer for the 1825 → 1952 → today comparison. The exact VAČ unit is not identified yet (fieldSearch lookup, TO_COLLECT).",
  },
  {
    id: "src-esd",
    code: "GISKD/EŠD",
    type: "heritage-register",
    titleSi: "Register nepremične kulturne dediščine (EŠD)",
    titleEn: "Register of immovable cultural heritage (EŠD)",
    vacUrl: "https://giskd.gov.si/egk",
    fund: "GISKD — Geografski informacijski sistem kulturne dediščine",
    archive: "Ministrstvo za kulturo RS",
    licenceSi: "javni register",
    licenceEn: "public register",
    transferStatus: "NOT_APPLICABLE",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 5,
    lastVerified: "2026-10-07",
    noteSi:
      "Identificirane enote za območje Griblje (uradno preverjene 2026-10-07 prek iskalnika EID): EŠD 2122 (Griblje — cerkev sv. Vida, spomenik lokalnega pomena), EŠD 19324 (Cerkvišče — spomenik NOB) in EŠD 19326 (Griblje — spomenik NOB, registrirana dediščina), EŠD 11118 (Podzemelj — arheološko najdišče Kučar, občina Metlika, spomenik lokalnega pomena) ter EŠD 10094 (Griblje — arheološko najdišče ob Kolpi, registrirana dediščina). Kučar (11118) in najdišče ob Kolpi (10094) sta dve ločeni enoti. Ločen sodoben uraden sloj.",
    noteEn:
      "Units identified for the Griblje area (officially verified 2026-10-07 via the EID search): EŠD 2122 (Griblje — Church of St. Vitus, local heritage monument), EŠD 19324 (Cerkvišče — WWII memorial) and EŠD 19326 (Griblje — WWII memorial, registered heritage), EŠD 11118 (Podzemelj — Kučar archaeological site, Municipality of Metlika, local heritage monument) and EŠD 10094 (Griblje — archaeological site by the Kolpa, registered heritage). Kučar (11118) and the Kolpa site (10094) are two separate units. A separate modern official layer.",
  },
];

/** EŠD enote — sodoben uradni register dediščine (issue #3 #8: ločene, uradno dokumentirane) */
export interface HeritageUnit {
  esd: number;
  titleSi: string;
  titleEn: string;
  /** uradni naziv iz registra (EID) */
  officialNameSi?: string;
  officialNameEn?: string;
  /** vrsta enote npr. stavbe / arheološka najdišča / spominski objekti in kraji */
  unitTypeSi?: string;
  unitTypeEn?: string;
  /** status varstva npr. spomenik lokalnega pomena / registrirana dediščina */
  protectionSi?: string;
  protectionEn?: string;
  municipality?: string;
  registerUrl?: string;
  lat?: number;
  lng?: number;
  museumRef?: string;
  /** razlika med uradnim registrom in muzejevo interpretacijo */
  deltaSi?: string;
  deltaEn?: string;
  lastVerified?: string;
}

export const HERITAGE_UNITS: HeritageUnit[] = [
  {
    esd: 2122,
    titleSi: "Griblje — cerkev sv. Vida",
    titleEn: "Griblje — Church of St. Vitus",
    officialNameSi: "Griblje - Cerkev sv. Vida",
    unitTypeSi: "stavbe (podružnična cerkev)",
    unitTypeEn: "buildings (filial church)",
    protectionSi: "spomenik lokalnega pomena",
    protectionEn: "local heritage monument",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=2122",
    lat: 45.56761,
    lng: 15.290311,
    museumRef: "MVG-002",
    deltaSi: "GEOTRUTH (issue #14, 2026-10-08): uradni poligon EŠD 2122 (GisKD, MK_EVRD/3602) — centroid 45,567610 N 15,290311 E, »na pokopališču, na gričku južno od vasi«. Stara koordinata 45,5728/15,2922 (krožna georeferenca) je odstopala 595 m — razrešeno v korist uradnega vira. OSM way 284847361 potrjuje (≤ 8 m).",
    lastVerified: "2026-10-08",
  },
  {
    esd: 10094,
    titleSi: "Griblje — arheološko najdišče ob Kolpi",
    titleEn: "Griblje — archaeological site by the Kolpa",
    officialNameSi: "Griblje - Arheološko najdišče ob Kolpi",
    unitTypeSi: "arheološka najdišča",
    unitTypeEn: "archaeological sites",
    protectionSi: "registrirana dediščina",
    protectionEn: "registered heritage",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=10094",
    lastVerified: "2026-10-07",
    deltaSi:
      "Sinonimi registra: Kohane, Požekov vrt, Krasinec - Vrh. Datiranje: mlajši neolitik do zgodnje rimske doba (naselbine, gomila, ravno grobišče). Vodnik ZVKD Novo mesto, usmeritve 2008. Ni mešan z EŠD 11118 (Kučar, Podzemelj) — dve ločeni enoti. Register ne objavlja koordinat v besedilu; lokacija bo dodana, ko bo pridobljena geometrija iz GISKD (TO_COLLECT).",
  },
  {
    esd: 11118,
    titleSi: "Podzemelj — arheološko najdišče Kučar",
    titleEn: "Podzemelj — Kučar archaeological site",
    officialNameSi: "Podzemelj - Arheološko najdišče Kučar",
    unitTypeSi: "arheološka najdišča",
    unitTypeEn: "archaeological sites",
    protectionSi: "spomenik lokalnega pomena",
    protectionEn: "local heritage monument",
    municipality: "Metlika",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=11118",
    lastVerified: "2026-10-07",
    deltaSi:
      "Občina je Metlika (ne Črnomelj). Železnodobno gradišče in zgodnjekrščansko središče z dvema cerkvama in krstilnico. Muzej v prejšnjih zapisih kraj ni navedel — popravek iz uradnega registra 2026-10-07.",
  },
  {
    esd: 19324,
    titleSi: "Cerkvišče — spomenik NOB",
    titleEn: "Cerkvišče — WWII memorial",
    officialNameSi: "Cerkvišče - Spomenik NOB",
    unitTypeSi: "spominski objekti in kraji",
    unitTypeEn: "memorial monuments and sites",
    protectionSi: "spomenik lokalnega pomena",
    protectionEn: "local heritage monument",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=19324",
    lastVerified: "2026-10-07",
    deltaSi: "Postavljen 1960, avtor Janez Savinšek. Vsebina: štirje partizani, ki so septembra 1941 napadli italijansko patruljo. Register ne objavlja koordinat v besedilu (TO_COLLECT).",
  },
  {
    esd: 19326,
    titleSi: "Griblje — spomenik NOB",
    titleEn: "Griblje — WWII memorial",
    officialNameSi: "Griblje - Spomenik NOB",
    unitTypeSi: "spominski objekti in kraji",
    unitTypeEn: "memorial monuments and sites",
    protectionSi: "registrirana dediščina",
    protectionEn: "registered heritage",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=19326",
    lastVerified: "2026-10-07",
    deltaSi: "Steber z imeni 11 padlih borcev in dveh žrtev 2. svetovne vojne, postavljen 1961. Register ne objavlja koordinat v besedilu (TO_COLLECT).",
  },
];

/** Negativni rezultati — del raziskovalne provenience */
export interface NegativeResult {
  id: string;
  whatSi: string;
  whatEn: string;
  status: "NOT_FOUND" | "NOT_PUBLIC" | "REVIEW" | "TO_COLLECT";
  detailSi: string;
  detailEn: string;
}

export const NEGATIVE_RESULTS: NegativeResult[] = [
  {
    id: "neg-atlas-model",
    whatSi: "Star Atlas 1825 podatkovni model (atlas-map-data-model-1825, knowledge-graph-1825, story-graph-1825, georef-1825, parcel-register-1825, cadastre-a01)",
    whatEn: "The old Atlas 1825 data model (atlas-map-data-model-1825, knowledge-graph-1825, story-graph-1825, georef-1825, parcel-register-1825, cadastre-a01)",
    status: "NOT_FOUND",
    detailSi:
      "Preiskani: git bundle muzej-backup-20261007, arhivski repozitoriji (markec-group/muzej-arhiv ne obstaja več), lokalni diski, vsi Vercel deploymenti (28). Datoteke niso bile obnovljive — Atlas je znova zgrajen neposredno iz primarnega arhivskega vira SI AS 176/N/N83.",
    detailEn:
      "Searched: the muzej-backup-20261007 git bundle, archive repositories (markec-group/muzej-arhiv no longer exists), local disks, all Vercel deployments (28). The files were not recoverable — the Atlas was rebuilt directly from the primary archival source SI AS 176/N/N83.",
  },
  {
    id: "neg-kurrent",
    whatSi: "Popoln prepis Kurrent rokopisov (vseh 7 spisovnih enot N83)",
    whatEn: "Complete transcription of the Kurrent manuscripts (all 7 written units of N83)",
    status: "REVIEW",
    detailSi:
      "Vsi prepisi v Atlasu so pomožni strojni očrti rokopisa in zahtevajo paleografsko potrditev. Stanje po issue #17 (2026-10-08, podrobnosti v research.ts KURRENT_SERIES): PR 4/4 strani, PG 1/1, PV 1/1 (12 kultur), PS 9 strani vzorčeno + rekapitulacija, PUA 10/49 strani (38 vrstic), PZ 10 strani vzorčeno, PT 8/8 pregledan. Poln prepis PS/PUA/PZ ostaja TO_COLLECT; vsi statusi REVIEW.",
    detailEn:
      "All transcriptions in the Atlas are machine-assisted readings requiring palaeographic confirmation. Status after issue #17 (2026-10-08, detail in research.ts KURRENT_SERIES): PR 4/4 pages, PG 1/1, PV 1/1 (12 cultures), PS 9 pages sampled + recapitulation, PUA 10/49 pages (38 rows), PZ 10 pages sampled, PT 8/8 reviewed. The full PS/PUA/PZ transcription remains TO_COLLECT; all statuses REVIEW.",
  },
  {
    id: "neg-1812",
    whatSi: "Napoleonov zemljevid ~1812 za območje Griblje",
    whatEn: "Napoleonic map ~1812 for the Griblje area",
    status: "TO_COLLECT",
    detailSi:
      "Slika v zbirki (MVG-092) je sodoben vektorski zemljevid Ilirskih provinc (TRAJAN 117, Wikimedia Commons, 2018, CC BY-SA 3.0) — ne izvirnik iz 1812. Ugotovitev 2026-10-07: javnodostopni obdobjeni izvirniki obstajajo na Wikimedii (npr. 'Provinces Illyriennes Servie et Bosnie 1812', javna last) — pridobitev izvirnika in afina georeferenca sta pripravljena naslednja koraka (TO_COLLECT, metoda enaka A01/A02). Prostorski sloj za 1812 v Atlasu še ni vzpostavljen; obdobje zajeta z MVG-092.",
    detailEn:
      "The collection image (MVG-092) is a modern vector map of the Illyrian Provinces (TRAJAN 117, Wikimedia Commons, 2018, CC BY-SA 3.0) — not an 1812 original. Finding of 2026-10-07: public-domain period originals exist on Wikimedia (e.g. 'Provinces Illyriennes Servie et Bosnie 1812') — acquiring the original and an affine georeference are prepared next steps (TO_COLLECT, method identical to A01/A02). No spatial 1812 layer in the Atlas yet; the period is covered by MVG-092.",
  },
  {
    id: "neg-georef-vector",
    whatSi: "Vektorizacija parcel iz listov A01/A02",
    whatEn: "Vectorization of parcels from sheets A01/A02",
    status: "TO_COLLECT",
    detailSi:
      "Listi sta georeferencirani (slikovno prekrivanje), parcelne meje pa še niso vektorsko izrisane. Samo zazidana pozicija je avtomatsko vektorizirana (156 objektov, status RECONSTRUCTED).",
    detailEn:
      "The sheets are georeferenced (image overlay) but parcel boundaries are not yet vectorised. Only built structures were auto-vectorised (156 objects, RECONSTRUCTED status).",
  },
  {
    id: "neg-sem",
    whatSi: "Digitalna kopija fotografije SEM F0000212 (domnevna rojstna hiša Nika Županiča)",
    whatEn: "Digital copy of the SEM F0000212 photograph (presumed birth house of Niko Županič)",
    status: "NOT_FOUND",
    detailSi:
      "Fotografija je dokumentirana v zbirki SEM (opis: enonadstropna hiša na pero, rojstna hiša dr. Nika Županiča), a digitalna kopija ni v muzejski zbirki (113 zapisov). Provenienca je vzpostavljena v research.ts (F0000212_PROVENANCE): vir SEM digitalne zbirke, pravice 'navedi vir', fotograf/datum ni znan (TO_COLLECT). Povezava hiša 73 / parcela 942/4 ↔ MVG-010 ostaja REVIEW, dokler primarni vir ne potrdi.",
    detailEn:
      "The photograph is documented in the SEM collection (description: one-storey house with a gallery, birth house of Dr. Niko Županič) but a digital copy is not in the museum collection (113 records). Provenance is established in research.ts (F0000212_PROVENANCE): source SEM digital collections, rights 'cite the source', photographer/date unknown (TO_COLLECT). The link house 73 / parcel 942/4 ↔ MVG-010 stays REVIEW until a primary source confirms it.",
  },
  {
    id: "neg-houses-geo",
    whatSi: "Natančne lokacije hiš 1–98 na sodobnem zemljevidu",
    whatEn: "Precise positions of houses 1–98 on the modern map",
    status: "TO_COLLECT",
    detailSi:
      "Hišne številke so na listih A01/A02 zapisane ob stavbah, vendar razdelava številk na listu za posamezno hišo še ni izvedena. Hiše imajo sklic na območje vasi (APPROXIMATE), ne na točko.",
    detailEn:
      "House numbers are written next to buildings on sheets A01/A02, but mapping individual numbers to buildings has not been done yet. Houses reference the village area (APPROXIMATE), not a point.",
  },
  {
    id: "neg-walk-station-32",
    whatSi: "Postaja 32 vodenga sprehoda »Vas in njeni ljudje«",
    whatEn: "Station 32 of the guided walk “The village and its people”",
    status: "NOT_FOUND",
    detailSi:
      "Preiskani VSI razpoložljivi viri (2026-10-07): (1) trenutni extra.json — postaje 1–31, 33–35; (2) izvirni repo pred incidentom (git bundle muzej-backup-20261007, VSEH 25 commitov od 2d9ac9b do 4896f35) — postaja 32 v nobeni različici ni nikoli obstajala; (3) vir podatkov = scrape izvirnega spletišča (zadnji delujoči Vercel deployment 2026-10-06 11:32) — vrzel izhaja že iz izvirnika; (4) surove scrape datoteke (download/) niso ohranjene. Sklep: postaja 32 v izvirniku ni bila objavljena ali je bila izpuščena pred objavo. Po pravilu issueja #4 vsebine NE izmišljujemo — vrzel je vidno označena v sprehodu (mesto 32) in v QA (zaporedje 1–35 z eksplicitnim NOT_FOUND).",
    detailEn:
      "All available sources searched (2026-10-07): (1) current extra.json — stations 1–31, 33–35; (2) the pre-incident original repo (git bundle muzej-backup-20261007, ALL 25 commits from 2d9ac9b to 4896f35) — station 32 never existed in any version; (3) the data source = a scrape of the original website (last working Vercel deployment 2026-10-06 11:32) — the gap originates in the original itself; (4) raw scrape files (download/) are not preserved. Conclusion: station 32 was never published in the original, or was dropped before publication. Per issue #4 no content is invented — the gap is visibly marked in the walk (slot 32) and in QA (sequence 1–35 with an explicit NOT_FOUND).",
  },
  {
    id: "neg-matice",
    whatSi: "matice.si — domnevni portal katastrskih skenov",
    whatEn: "matice.si — an assumed portal of cadastral scans",
    status: "NOT_FOUND",
    detailSi:
      "Iskano 2026-10-08 (issue #17): DNS domene matice.si se ne razreši; spletni iskalniki takega vira ne poznajo (poizvedbe 'matice.si Črnomelj', 'matice.si kataster Griblje'). SKLEP: vir ne obstaja (ali je ugasnjen). Skeni franciscejskega katastra za Griblje ostajajo na VAČ (N083, javno) — to je potrjena pot.",
    detailEn:
      "Searched 2026-10-08 (issue #17): the matice.si DNS does not resolve; search engines do not know such a source (queries 'matice.si Črnomelj', 'matice.si kataster Griblje'). CONCLUSION: the source does not exist (or is defunct). The Griblje Franciscean cadastre scans remain on VAČ (N083, public) — that is the confirmed path.",
  },
  {
    id: "neg-e-ars",
    whatSi: "www.e-ars.si — domnevni portal digitaliziranih enot Arhiva RS",
    whatEn: "www.e-ars.si — an assumed portal of digitised Arhiv RS units",
    status: "NOT_FOUND",
    detailSi:
      "Iskano 2026-10-08 (issue #17): DNS www.e-ars.si je mrtev. Celoten SI AS 176/N83 Griblje pa JE javno dostopen v VAČ (OPSI zbirka 'Digitalizirano arhivsko gradivo starih katastrov') — digitalizacija ARS torej obstaja, dostopna je prek VAČ, ne prek ločenega portala e-ars.si.",
    detailEn:
      "Searched 2026-10-08 (issue #17): the www.e-ars.si DNS is dead. The whole SI AS 176/N83 Griblje IS however publicly accessible via VAČ (the OPSI collection 'Digitalised archival material of the old cadastres') — the ARS digitisation exists, reachable through VAČ, not through a separate e-ars.si portal.",
  },
  {
    id: "neg-pz-recap",
    whatSi: "PZ — Rekapitulacija kultur/razredov na koncu elaborata",
    whatEn: "PZ — a recapitulation of cultures/classes at the end of the elaborate",
    status: "NOT_FOUND",
    detailSi:
      "Iskano 2026-10-08 (issue #17): vzorčene končne strani PZ 68–71 vsebujejo IZKLJUČNO administrativne protokole (Vorlage, Geprüft, Nachtrag s 'hus Zins' seznamom, zaključek 'Gemacht den 28ten Juli 1825') — kulturna rekapitulacija NI tam. Cenilne tabele po kulturah in razredih so v sredini (str. ~4–67; vzorčene str. 20/30/40/50/60). Naslednji korak: ciljano branje str. 4–67.",
    detailEn:
      "Searched 2026-10-08 (issue #17): the sampled end pages PZ 68–71 contain ONLY administrative protocols (Vorlage, Geprüft, a Nachtrag with the 'hus Zins' list, the closing 'Gemacht den 28ten Juli 1825') — no culture recapitulation is there. The valuation tables by culture and class sit in the middle (pp. ~4–67; sampled pp. 20/30/40/50/60). Next step: a targeted read of pp. 4–67.",
  },
  {
    id: "neg-oral-interviews",
    whatSi: "Posneti intervjuji ustne zgodovine",
    whatEn: "Recorded oral-history interviews",
    status: "TO_COLLECT",
    detailSi:
      "Iskano 2026-10-08 (issue #17): javno dostopnih posnetih pričevanj domačinov Gribelj NI (teme obstajajo: Pasuljada, tamburaši, dogodki, šola). Pripravljen je raziskovalni protokol v1.0 (research.ts ORAL_HISTORY_PROTOCOL: 4 faze, soglasje, pravice, 5 pravil). ORAL_INTERVIEWS ostane prazen — ne izmišljujemo intervjujev; prvi snemalni korak je na živi strani.",
    detailEn:
      "Searched 2026-10-08 (issue #17): no publicly accessible recorded testimonies of Griblje villagers exist (the topics do: the bean feast, tamburica players, events, school). A research protocol v1.0 is prepared (research.ts ORAL_HISTORY_PROTOCOL: 4 stages, consent, rights, 5 rules). ORAL_INTERVIEWS stays empty — no interviews are invented; the first recording step is on the live side.",
  },
];
