// ATLAS 1825 — lastniki (navzkrižno preverjeni med PT in PUA) + georeferenca + model

export interface AtlasOwner {
  id: string;
  /** prepis iz vira (Kurrent, REVIEW) */
  nameAsWritten: string;
  /** sodobna približna različica */
  modernGuess?: string;
  /** hiše iz PT (parc. sklici) */
  houseRefs: string[];
  /** potrditev iz PUA (abecedni seznam) */
  puaRef?: string;
  status: "REVIEW" | "DOCUMENTED";
}

export const ATLAS_OWNERS: AtlasOwner[] = [
  { id: "lastnik-bring-weygandt", nameAsWritten: "Bring. Weygandt Bauern von Grüblen", modernGuess: "Bring", houseRefs: ["24", "31", "32", "36", "38", "39", "41"], puaRef: "PUA str. 4, črka B", status: "REVIEW" },
  { id: "lastnik-bring-math", nameAsWritten: "Bring. Math. Bauern von Grüblen", modernGuess: "Bring", houseRefs: ["25"], puaRef: "PUA str. 4, črka B", status: "REVIEW" },
  { id: "lastnik-simec", nameAsWritten: "Schimek / Šimec", modernGuess: "Šimec", houseRefs: ["3", "4", "63", "64", "66"], status: "REVIEW" },
  { id: "lastnik-leskovec", nameAsWritten: "Leskovec Matija", houseRefs: ["8", "8½"], status: "REVIEW" },
  { id: "lastnik-hrovat", nameAsWritten: "Hrovat Jhan", modernGuess: "Hrvat", houseRefs: ["18", "15"], status: "REVIEW" },
  { id: "lastnik-krisan", nameAsWritten: "Krišan Gregor", houseRefs: ["29", "30"], status: "REVIEW" },
  { id: "lastnik-milleg", nameAsWritten: "Milleg", houseRefs: ["34", "35", "37"], status: "REVIEW" },
  { id: "lastnik-glan", nameAsWritten: "Glan (Georg, Matthäus, Simonz)", houseRefs: ["—"], puaRef: "PUA str. 4–5", status: "REVIEW" },
  { id: "lastnik-greg", nameAsWritten: "Greg/Grög (Michael, Ulrich)", houseRefs: ["—"], status: "REVIEW" },
  { id: "lastnik-filak", nameAsWritten: "Filak (Peter, Mihel)", houseRefs: ["69", "70", "71"], status: "REVIEW" },
  { id: "lastnik-dikobutar", nameAsWritten: "Dikobutar (Rupre, Mihelo, Mihlo, Marko)", houseRefs: ["68", "72", "77", "78", "80"], status: "REVIEW" },
  { id: "lastnik-peutinger", nameAsWritten: "Peutinger (Jhan, Mihel)", houseRefs: ["61", "65", "73"], status: "REVIEW" },
  { id: "lastnik-drulak", nameAsWritten: "Drulak (Jhan, Peter)", houseRefs: ["74", "75"], status: "REVIEW" },
  { id: "lastnik-stenopfs", nameAsWritten: "Stenopfs Georg", houseRefs: ["76", "79"], status: "REVIEW" },
  { id: "lastnik-groy", nameAsWritten: "Groy (Hanž, Feidig, Khunz)", houseRefs: ["81–84", "92", "96"], status: "REVIEW" },
  { id: "lastnik-heurisch", nameAsWritten: "Heurisch Marko", houseRefs: ["87", "89", "91"], status: "REVIEW" },
  { id: "lastnik-kuncelj", nameAsWritten: "Kuncelj Miha", houseRefs: ["90"], status: "REVIEW" },
  { id: "lastnik-schmerz", nameAsWritten: "Schmerz Marko", houseRefs: ["95", "97"], status: "REVIEW" },
  { id: "lastnik-adlolschitz", nameAsWritten: "Adlolschitz, Wulff Ludwig (von)", houseRefs: ["1"], puaRef: "PUA str. 3, črka A — Dragosche", status: "REVIEW" },
  { id: "lastnik-ludvig", nameAsWritten: "Ludvig Gregor", houseRefs: ["23"], status: "REVIEW" },
  { id: "lastnik-zollnerd", nameAsWritten: "Zollnerd A. M.", houseRefs: ["98"], status: "REVIEW" },
];

// ——— GEOREFERENCA ——————————————————————————————

export interface SheetGeoref {
  id: string;
  sheet: string;
  imageUrl: string;
  /** [severni, zahodni], [južni, vzhodni] */
  bounds: [[number, number], [number, number]];
  pixels: { width: number; height: number };
  scaleMPerPixel: number;
  status: "REVIEW";
  methodSi: string;
  methodEn: string;
  controlPoints: { fromSi: string; a01x?: number; a01y?: number; modernLat: number; modernLng: number; noteSi?: string }[];
  accuracySi: string;
  accuracyEn: string;
}

export const SHEET_GEOREFS: SheetGeoref[] = [
  {
    id: "georef-a01",
    sheet: "A01",
    imageUrl: "/atlas/n83-a01.jpg",
    bounds: [
      [45.5888, 15.2622],
      [45.5666, 15.3016],
    ],
    pixels: { width: 2826, height: 2273 },
    scaleMPerPixel: 1.09,
    status: "REVIEW",
    methodSi:
      "Afina transformacija brez rotacije (Web Mercator): sidrišči — jedro vasi Grüble (list ~74 % š / ~78 % v) ↔ moderni center vasi 45,5725 N 15,2926 E; severna skupina hiš ↔ 45,5754 N; reka Kolpa pri vasi (~91 % š) ↔ sodobna struga 15,2994 E. Iterativno izboljšanje s prekrivko na OSM (3 koraki) — vizualna ocena ujemanja: vas 8/10, reka 9/10.",
    methodEn:
      "Affine transform without rotation (Web Mercator): anchors — Grüble village core (~74 % w / ~78 % h) ↔ modern village centre 45.5725 N 15.2926 E; northern house cluster ↔ 45.5754 N; the Kolpa at the village latitude (~91 % w) ↔ modern channel 15.2994 E. Iteratively refined on an OSM overlay (3 steps) — visual match: village 8/10, river 9/10.",
    controlPoints: [
      { fromSi: "jedro vasi Grüble (A01 px 2091, 1773)", a01x: 2091, a01y: 1773, modernLat: 45.5725, modernLng: 15.2926, noteSi: "muzejska točka MVG-001" },
      { fromSi: "severna skupina (A01 px 2063, 1477)", a01x: 2063, a01y: 1477, modernLat: 45.5754, modernLng: 15.2928 },
      { fromSi: "reka Kolpa pri vasi (A01 px 2580, 1773)", a01x: 2580, a01y: 1773, modernLat: 45.5725, modernLng: 15.2994, noteSi: "izsledek struge iz OSM ploščic" },
    ],
    accuracySi:
      "Ocena natančnosti ±75–120 m (vizualno). List ni rotiran; razmerje stranic preslikave 1,246 ≈ razmerje slike 1,243 (konsistenčni test). Kotni odmik lokalne katastrske projekcije ni odstranjen.",
    accuracyEn:
      "Estimated accuracy ±75–120 m (visual). The sheet is unrotated; transform aspect 1.246 ≈ image aspect 1.243 (consistency test). The angular offset of the local cadastral projection was not removed.",
  },
  {
    id: "georef-a02",
    sheet: "A02",
    imageUrl: "/atlas/n83-a02.jpg",
    bounds: [
      [45.576998, 15.271679],
      [45.561308, 15.302635],
    ],
    pixels: { width: 3010, height: 2158 },
    scaleMPerPixel: 0.79,
    status: "REVIEW",
    methodSi:
      "Afina transformacija: sidrišči — cerkev sv. Vida na listu (px 1995, 577; stavba z apsido, oznaka K, napis St. Veith) ↔ moderna cerkev MVG-002 (45,5728 N 15,2922 E) — ujemitev križa na piksel točno; reka Kolpa (med. stolpec 89,5 %) ↔ sodobna struga. Vizualna ocena 9/10.",
    methodEn:
      "Affine transform: anchors — St. Vitus church on the sheet (px 1995, 577; apsidal building, mark K, label St. Veith) ↔ modern church MVG-002 (45.5728 N 15.2922 E) — crosshair match exact to the pixel; the Kolpa (median column 89.5 %) ↔ modern channel. Visual match 9/10.",
    controlPoints: [
      { fromSi: "cerkev sv. Vida (A02 px 1995, 577)", a01x: 1995, a01y: 577, modernLat: 45.5728, modernLng: 15.2922, noteSi: "MVG-002, EŠD 2122 — validirano tudi z vektorizacijo (izluščena stavba na 45,57287 N 15,29217 E)" },
      { fromSi: "reka Kolpa ob cerkvi (A02 px 2695, 577)", a01x: 2695, a01y: 577, modernLat: 45.5728, modernLng: 15.2994 },
    ],
    accuracySi: "Ocena natančnosti ±50–80 m. Skala lista ~0,79 m/px (višja ločljivost skena kot A01).",
    accuracyEn: "Estimated accuracy ±50–80 m. Sheet scale ~0.79 m/px (higher scan resolution than A01).",
  },
];

// ——— LOKACIJSKE entitete (LOCATION sloj) ——————————

export interface AtlasLocation {
  id: string;
  kind: "vas" | "cerkev" | "reka" | "pot" | "meja";
  titleSi: string;
  titleEn: string;
  lat?: number;
  lng?: number;
  status: "VERIFIED" | "DOCUMENTED" | "APPROXIMATE";
  sourceId: string;
  museumRef?: string;
  noteSi?: string;
}

export const ATLAS_LOCATIONS: AtlasLocation[] = [
  {
    id: "loc-griblje",
    kind: "vas",
    titleSi: "Griblje (Grüble) — jedro vasi ~1825",
    titleEn: "Griblje (Grüble) — village core ~1825",
    lat: 45.5725,
    lng: 15.2926,
    status: "VERIFIED",
    sourceId: "src-a02",
    museumRef: "MVG-001",
    noteSi: "Razpotegnjeno jedro z dvema sklopoma hiš na listu A02; 156 vektoriziranih objektov (status RECONSTRUCTED).",
  },
  {
    id: "loc-cerkev",
    kind: "cerkev",
    titleSi: "Cerkev sv. Vida (St. Veith) ~1825",
    titleEn: "St. Vitus church (St. Veith) ~1825",
    lat: 45.5728,
    lng: 15.2922,
    status: "VERIFIED",
    sourceId: "src-a02",
    museumRef: "MVG-002",
    noteSi: "Stavba z apsido, oznaka K ob napisu St. Veith na listu A02; ista lokacija kot današnja cerkev (EŠD 2122). Pripravljena za 3D/AR (GLB model MVG-002).",
  },
  {
    id: "loc-kolpa",
    kind: "reka",
    titleSi: "Reka Kolpa — vzhodna meja občine ~1825",
    titleEn: "The Kolpa river — eastern municipality boundary ~1825",
    status: "VERIFIED",
    sourceId: "src-a01",
    noteSi: "Na obeh listih označena kot meja proti CROATIEN / KÖNIGREICH CROATIEN; struga se v glavnem ujema s sodobno.",
  },
  {
    id: "loc-meja",
    kind: "meja",
    titleSi: "Meja katastrske občine (k.o. št. 83)",
    titleEn: "Boundary of the cadastral municipality (c.m. no. 83)",
    status: "DOCUMENTED",
    sourceId: "src-pr",
    noteSi: "Grenz-Beschreibung der Gemeinde „GRÜBLE“ — opis meje v N083PR (4 strani, Kurrent, še ni prebran v celoti).",
  },
];

// ——— Stavbe — vektorizacija iz lista A02 (RECONSTRUCTED) ————

export interface VectorBuilding {
  lat: number;
  lng: number;
  w: number;
  h: number;
  px: [number, number];
}

import buildingsJson from "./buildings.json";
export const VECTOR_BUILDINGS = buildingsJson as VectorBuilding[];
