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
  { id: "lastnik-bring-weygandt", nameAsWritten: "Bring. Weygandt Bauern von Grüblen", modernGuess: "Bring", houseRefs: ["24", "31", "32", "36", "38", "39", "41"], puaRef: "PUA str. 4, črka B; issue #17: PUA str. 4 vrstica 3 = Bring Michael/Migan Bauern hiesig, Haus 24 [~] — navzkrižna potrditev hiše 24", status: "REVIEW" },
  { id: "lastnik-bring-math", nameAsWritten: "Bring. Math. Bauern von Grüblen", modernGuess: "Bring", houseRefs: ["25"], puaRef: "PUA str. 4, črka B; issue #17: PUA str. 4 vrstica 4 = Bring Miß/Martin Bauern hiesig, Haus 25 [~] — navzkrižna potrditev", status: "REVIEW" },
  { id: "lastnik-simec", nameAsWritten: "Schimek / Šimec", modernGuess: "Šimec", houseRefs: ["3", "4", "63", "64", "66"], status: "REVIEW" },
  { id: "lastnik-leskovec", nameAsWritten: "Leskovec Matija", houseRefs: ["8", "8½"], status: "REVIEW" },
  { id: "lastnik-hrovat", nameAsWritten: "Hrovat Jhan", modernGuess: "Hrvat", houseRefs: ["18", "15"], status: "REVIEW" },
  { id: "lastnik-krisan", nameAsWritten: "Krišan Gregor", houseRefs: ["29", "30"], status: "REVIEW" },
  { id: "lastnik-milleg", nameAsWritten: "Milleg", houseRefs: ["34", "35", "37"], status: "REVIEW" },
  { id: "lastnik-glan", nameAsWritten: "Glan (Georg, Matthäus, Simonz)", houseRefs: ["—"], puaRef: "PUA str. 4–5", status: "REVIEW" },
  { id: "lastnik-greg", nameAsWritten: "Greg/Grög (Michael, Ulrich)", houseRefs: ["—"], status: "REVIEW" },
  { id: "lastnik-filak", nameAsWritten: "Filak (Peter, Mihel)", houseRefs: ["69", "70", "71"], puaRef: "PUA str. 9–10, črka F — Fillah (Michael, Maria, Jetter, Miho) v hišah 16/34/36/61 [~]: ista družina, hišne št. divergentne s PT [~]", status: "REVIEW" },
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

// ——— GEOREFERENCA (GEOTRUTH, issue #14, 2026-10-08) ——————————————————
// Listi A01/A02 so zasidrani na uradni EŠD 2122 (Register nepremične kulturne
// dediščine, GisKD): cerkev sv. Vida na listu A02 (px 1995,577) ↔ uradni poligon
// 45,567610 N 15,290311 E. Struga Kolpe na listu (desni krak, VLM x 2765–2890)
// se pod to afino ujema s sodobno strugo 6–30 m — pod staro (krožno) afino je
// odstopala 80–130 m. Vsi izpeljani podatki so bili translirani za
// −0,005190 lat / −0,001889 lng (≈ −147 m E / +578 m J).

export interface SheetGeoref {
  id: string;
  sheet: string;
  imageUrl: string;
  /** [severni, zahodni], [južni, vzhodni] — GEOTRUTH (EŠD 2122) afina */
  bounds: [[number, number], [number, number]];
  pixels: { width: number; height: number };
  scaleMPerPixel: number;
  status: "CORROBORATED" | "RECONSTRUCTED" | "REVIEW";
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
      [45.58361, 15.26031],
      [45.56141, 15.29971],
    ],
    pixels: { width: 2826, height: 2273 },
    scaleMPerPixel: 1.09,
    status: "RECONSTRUCTED",
    methodSi:
      "GEOTRUTH afina (issue #14): staro sidro A01 »jedro vasi« (px 2091,1773) se po popravku izkaže za cerkev+ pokopališče (34 m od EŠD 2122), »severna skupina« (px 2063,1477) pa za severni rob vasi 1825. Translacija lista: −0,005190 lat / −0,001889 lng. Struga Kolpa ostaja neodvisen vir E–Z kontrole (OSM ploščice).",
    methodEn:
      "GEOTRUTH affine (issue #14): the old A01 anchor »village core« (px 2091,1773) re-identifies, after the correction, as the church + churchyard (34 m from EŠD 2122); the »northern cluster« (px 2063,1477) is the north end of the 1825 village. Sheet translation: −0.005190 lat / −0.001889 lng. The Kolpa channel remains an independent E–W control (OSM tiles).",
    controlPoints: [
      { fromSi: "cerkev sv. Vida / »jedro« (A01 px 2091, 1773)", a01x: 2091, a01y: 1773, modernLat: 45.56761, modernLng: 15.290311, noteSi: "EŠD 2122 (uradni vir) — prej razlagano kot jedro vasi, krožna georeferenca" },
      { fromSi: "severna skupina hiš (A01 px 2063, 1477)", a01x: 2063, a01y: 1477, modernLat: 45.57022, modernLng: 15.290913, noteSi: "severni rob vasi 1825 po GEOTRUTH afini" },
      { fromSi: "reka Kolpa pri vasi (A01 px 2580, 1773)", a01x: 2580, a01y: 1773, modernLat: 45.56761, modernLng: 15.2994, noteSi: "izsledek struge iz OSM ploščic (neodvisen vir E–Z)" },
    ],
    accuracySi:
      "Ocena natančnosti ±60–100 m na območju vasi (struga potrjena 6–30 m, translacija ena za oba lista). Kotni odmik lokalne katastrske projekcije ni odstranjen (ocena ≤ 2,5°).",
    accuracyEn:
      "Estimated accuracy ±60–100 m over the village area (the river channel confirmed at 6–30 m, one shared translation for both sheets). The angular offset of the local cadastral projection was not removed (estimated ≤ 2.5°).",
  },
  {
    id: "georef-a02",
    sheet: "A02",
    imageUrl: "/atlas/n83-a02.jpg",
    bounds: [
      [45.571808, 15.26979],
      [45.556118, 15.300746],
    ],
    pixels: { width: 3010, height: 2158 },
    scaleMPerPixel: 0.79,
    status: "CORROBORATED",
    methodSi:
      "GEOTRUTH afina (issue #14): cerkev sv. Vida na listu (px 1995,577 — apsida, križ, pokopališki obrobl) ↔ uradni poligon EŠD 2122 (45,567610 N 15,290311 E, GisKD MK_EVRD/3602, STANJE_POD 07-10-2026); stavba OSM 284847361 znotraj poligona (≤ 8 m). Struga Kolpe na listu (desni krak, VLM x 2765–2890 pri y 100–1400) se s sodobno strugo ujeme 6–30 m. Stara afina je bila KROŽNA — cerkev je bila lastna kontrolna točka s predpostavljeno koordinato 45,5728/15,2922.",
    methodEn:
      "GEOTRUTH affine (issue #14): St. Vitus' church on the sheet (px 1995,577 — apse, cross, churchyard) ↔ the official EŠD 2122 polygon (45.567610 N 15.290311 E, GisKD MK_EVRD/3602, status 07-10-2026); the OSM building 284847361 lies inside the polygon (≤ 8 m). The Kolpa channel on the sheet (right branch, VLM x 2765–2890 at y 100–1400) matches the modern channel at 6–30 m. The old affine was CIRCULAR — the church was its own control point with an assumed coordinate 45.5728/15.2922.",
    controlPoints: [
      { fromSi: "cerkev sv. Vida (A02 px 1995, 577)", a01x: 1995, a01y: 577, modernLat: 45.56761, modernLng: 15.290311, noteSi: "EŠD 2122 — uradni register (GisKD) + OSM way 284847361 + pokopališče 284847363" },
      { fromSi: "reka Kolpa ob cerkvi (A02 px 2695, 577 — desni krak x≈2827)", a01x: 2695, a01y: 577, modernLat: 45.56761, modernLng: 15.29866, noteSi: "sodobna struga pri latitudi cerkve (OSM); na listu narisana pri x≈2827, ujemanje 6–30 m" },
    ],
    accuracySi:
      "Ocena natančnosti ±40–80 m na območju vasi. Skala lista ~0,79 m/px. Prisotnost OSM stavb (15 obstoječih od 156 po novi shemi) dodatno podpira afino.",
    accuracyEn:
      "Estimated accuracy ±40–80 m over the village area. Sheet scale ~0.79 m/px. The OSM building presence (15 of 156 matching under the new scheme) further supports the affine.",
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
    lat: 45.57092,
    lng: 15.29435,
    status: "VERIFIED",
    sourceId: "src-a02",
    museumRef: "MVG-001",
    noteSi: "Razpotegnjeno jedro z dvema sklopoma hiš na listu A02 (GEOTRUTH afina, issue #14); 156 vektoriziranih objektov (status RECONSTRUCTED). Današnje jedro (OSM place node 45,5725/15,2926) je ~370 m severno — vas je zrasla proti severu.",
  },
  {
    id: "loc-cerkev",
    kind: "cerkev",
    titleSi: "Cerkev sv. Vida (St. Veith) ~1825",
    titleEn: "St. Vitus church (St. Veith) ~1825",
    lat: 45.56761,
    lng: 15.290311,
    status: "VERIFIED",
    sourceId: "src-a02",
    museumRef: "MVG-002",
    noteSi: "Stavba z apsido, križem in pokopališkim obroblom na listu A02 (px 1995,577). EŠD 2122: »na pokopališču, na gričku južno od vasi«. Uradni vir (GisKD) + OSM (way 284847361) — koordinata VERIFIED (issue #14, konflikt 595 m razrešen). Pripravljena za 3D/AR (GLB model MVG-002, realno merilo 13 m).",
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
