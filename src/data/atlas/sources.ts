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
    noteSi:
      "Grafični list katastrske občine Griblje (Grüble). Reka Kolpa kot vzhodna meja, naselbina v jugovzhodnem delu. Sken 2826 × 2273 px.",
    noteEn:
      "Graphical sheet of the Griblje (Grüble) cadastral municipality. The Kolpa river as eastern boundary, settlement in the south-east. Scan 2826 × 2273 px.",
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
    noteSi:
      "List z jedrom vasi in cerkvijo St. Veith (sv. Vid, oznaka K, stavba z apsido). Sken 3010 × 2158 px.",
    noteEn:
      "Sheet with the village core and St. Veith church (marked K, apsidal building). Scan 3010 × 2158 px.",
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
    noteSi:
      "Glavni vir hišnega registra ~1825: hišne številke 1–98 z lastniki in parcelnimi sklici. Prepis rokopisa (Kurrent) je DELNO dokončan — vsi vnosi imajo status REVIEW.",
    noteEn:
      "Primary source of the ~1825 house register: house numbers 1–98 with owners and parcel references. The Kurrent manuscript transcription is PARTIAL — all entries carry REVIEW status.",
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
    noteSi:
      "Lastniki po abecedi s hišnimi številkami in parcelami po sekcijah I–V. Uporabljeno za navzkrižno preverjanje imen iz protokola stavbnih parcel.",
    noteEn:
      "Owners alphabetically with house numbers and parcels by sections I–V. Used to cross-check owner names from the building-parcel protocol.",
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
  },
  // Zunanji registri in poznejši viri — jasno ločeni od N83
  {
    id: "src-as749",
    code: "SI AS 749/3/8/12",
    type: "archival-mention",
    titleSi:
      "Izpisek parcel iz katastrskih davčnih vpisnikov za davčni občini Griblje in sosedne (19. st.)",
    titleEn:
      "Extract of parcels from cadastral tax registers for the tax municipalities of Griblje and neighbours (19th c.)",
    vacId: "227666-",
    vacUrl: "https://vac.sjas.gov.si/vac/search/fieldSearch",
    yearFrom: 1851,
    yearTo: 1853,
    fund: "SI AS 749",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    noteSi:
      "Kasnejši kataster za davčne občine Vinji Vrh, Kot, Griblje, Kaltersberg, Loka, Petrova vas, Krasinec. Sloj 1851–1853, pripravljen v modelu kot kasnejše obdobje.",
    noteEn:
      "Later cadastre for tax municipalities Vinji Vrh, Kot, Griblje, Kaltersberg, Loka, Petrova vas, Krasinec. An 1851–1853 layer, prepared in the model as a later period.",
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
    noteSi:
      "Povojni reambulirani katastrski načrt — pripravljen kot kasnejša plast za primerjavo 1825 → 1952 → danes.",
    noteEn:
      "Post-war reambulated cadastral plan — prepared as a later layer for the 1825 → 1952 → today comparison.",
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
    noteSi:
      "Identificirane enote za območje Griblje: EŠD 2122 (cerkev sv. Vida), EŠD 19324 in 19326 (spominski obeležji), EŠD 11118 (arheološko območje Kučar). Ločen sodoben uraden sloj.",
    noteEn:
      "Units identified for the Griblje area: EŠD 2122 (St. Vitus church), EŠD 19324 & 19326 (memorials), EŠD 11118 (Kučar archaeological site). A separate modern official layer.",
  },
];

/** EŠD enote — sodoben uradni register dediščine */
export interface HeritageUnit {
  esd: number;
  titleSi: string;
  titleEn: string;
  lat?: number;
  lng?: number;
  museumRef?: string;
}

export const HERITAGE_UNITS: HeritageUnit[] = [
  {
    esd: 2122,
    titleSi: "Cerkev sv. Vida, Griblje",
    titleEn: "Church of St. Vitus, Griblje",
    lat: 45.5728,
    lng: 15.2922,
    museumRef: "MVG-002",
  },
  {
    esd: 19324,
    titleSi: "Spominsko obeležje (Griblje)",
    titleEn: "Memorial marker (Griblje)",
  },
  {
    esd: 19326,
    titleSi: "Spominsko obeležje (Griblje)",
    titleEn: "Memorial marker (Griblje)",
  },
  {
    esd: 11118,
    titleSi: "Arheološko območje Kučar",
    titleEn: "Kučar archaeological site",
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
    whatSi: "Popoln prepis Kurrent rokopisov (PT, PUA, PS, PZ)",
    whatEn: "Complete transcription of the Kurrent manuscripts (PT, PUA, PS, PZ)",
    status: "REVIEW",
    detailSi:
      "Vsi prepisi v Atlasu so pomožni strojni očrti rokopisa in zahtevajo paleografsko potrditev. Vnosi iz PT (hiše 1–98) in PUA (lastniki A–B) so prebrani le delno; strani PS (143) in PZ (71) še niso prepisane.",
    detailEn:
      "All transcriptions in the Atlas are machine-assisted readings requiring palaeographic confirmation. Entries from PT (houses 1–98) and PUA (owners A–B) are only partially read; pages of PS (143) and PZ (71) are not transcribed yet.",
  },
  {
    id: "neg-1812",
    whatSi: "Napoleonov zemljevid ~1812 za območje Griblje",
    whatEn: "Napoleonic map ~1812 for the Griblje area",
    status: "TO_COLLECT",
    detailSi:
      "V fondeh SI AS 176–182 (VAČ) ni ločenega lista ~1812 za Griblje. Vir bi bil v drugem fondu (obdobje Ilirskih provinc) — pripravljena plasc v modelu je prazna in čaka vir.",
    detailEn:
      "Within fonds SI AS 176–182 (VAČ) there is no separate ~1812 sheet for Griblje. The source would sit in a different fonds (Illyrian Provinces era) — the model layer is empty and awaits a source.",
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
    whatSi: "Fotografija SEM F0000212 (domnevna rojstna hiša, hiša št. 73)",
    whatEn: "Photograph SEM F0000212 (presumed birth house, house no. 73)",
    status: "NOT_FOUND",
    detailSi:
      "Fotografija je omenjena v starih raziskavah, v muzejski zbirki (113 zapisov) pa je ni. Povezava hiša 73 ↔ Niko Županič (MVG-010) ostaja REVIEW/TO_COLLECT, dokler arhivski vir ni priskrbljen.",
    detailEn:
      "The photograph is referenced in the old research but is not in the museum collection (113 records). The link house 73 ↔ Niko Županič (MVG-010) stays REVIEW/TO_COLLECT until an archival source is supplied.",
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
];
