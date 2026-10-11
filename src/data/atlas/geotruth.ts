/**
 * GEOTRUTH (issue #14, P0) — enoten, strojno berljiv model AR sidrov (anchorjev)
 * z dokazno potjo, hierarhijo virov, samodejnim detektorjem konfliktov in
 * pogodbo o pripravljenosti scene (readiness).
 *
 * Načelo: koordinata je RESNICA šele, če ima vir, status, natančnost in datum
 * preverjanja. »Že dolgo v kodi« ni dokaz (issue #14, točka 4).
 *
 * Razrešeni konflikt (točka 2 — dokazna pot, 2026-10-08):
 *  1. EŠD 2122 (Register nepremične kulturne dediščine, GisKD MK_EVRD/3602,
 *     STANJE_POD 07-10-2026): cerkev sv. Vida — poligon centroid 45,567610 N
 *     15,290311 E, »na pokopališču, na gričku južno od vasi«.
 *  2. OSM (way 284847361 »Sv. Vid« + pokopališče 284847363): 45,567677/15,290388 —
 *     znotraj uradnega poligona, ≤ 8 m.
 *  3. List A02: cerkev narisana na px(1995,577); stara afina iz model.ts je bila
 *     KROŽNA (cerkev = kontrolna točka s predpostavljeno koordinato).
 *  4. Struga Kolpe na listu (desni krak, VLM x≈2765–2890 pri y 100–1400) se s
 *     sodobno strugo ujema samo pod cerkveno zasidrano afino (6–30 m; stara
 *     afina odstopa 80–130 m).
 *  5. List A01: »jedro« (px 2091,1773) je po popravku cerkev+ pokopališče (34 m
 *     od EŠD 2122); »severna skupina« (px 2063,1477) = severni rob vasi 1825.
 *  ⇒ Vsi iz listov izpeljani podatki (156 stavb, raba tal) translirani za
 *    −0,005190 lat / −0,001889 lng (≈ −147 m E, +578 m J).
 *
 * Ne odpravlja: OSM zbirka je živa; uradni register se spreminja —
 * lastVerified zabeleži datum preverjanja posameznega sidra.
 */

import { TIME_SPOTS } from "./timespots";
import { distanceM } from "@/lib/geo";
import { exhibits as EXHIBITS } from "@/lib/museum";

/* ── 1. Hierarhija virov (issue #14, točka 4) ─────────────────────────── */

export type SourceKind =
  | "OFFICIAL_GIS" // 1. uradni GIS / register / geodetski vir
  | "ARCHIVAL_PRIMARY" // 2. primarni arhivski / georeferenčni vir
  | "CORROBORATING" // 3. neodvisen corroborating vir
  | "OWN_GEOREF" // 4. lastna georeferenca
  | "APPROX"; // 5. približna lokacija

export interface GeoSource {
  id: string;
  kind: SourceKind;
  nameSi: string;
  nameEn: string;
  url?: string;
  licenseSi?: string;
  retrievedAt: string;
}

export const GEO_SOURCES: GeoSource[] = [
  {
    id: "src-esd2122",
    kind: "OFFICIAL_GIS",
    nameSi: "EŠD 2122 — Griblje, Cerkev sv. Vida (Register nepremične kulturne dediščine, GisKD / Ministrstvo za kulturo, storitev MK_EVRD)",
    nameEn: "EŠD 2122 — Griblje, St. Vitus' church (Register of Immovable Cultural Heritage, GisKD / Ministry of Culture, MK_EVRD service)",
    url: "https://geohub.gov.si/ags/rest/services/MK/MK_EVRD/MapServer/3602",
    licenseSi: "uradni državni vir (GOV.SI / OPSI)",
    retrievedAt: "2026-10-08",
  },
  {
    id: "src-esd19326",
    kind: "OFFICIAL_GIS",
    nameSi: "EŠD 19326 — Griblje, Spomenik NOB (isti register; »spomenik stoji pred osnovno šolo v Gribljah«)",
    nameEn: "EŠD 19326 — Griblje, NOB memorial (same register; »the memorial stands in front of the primary school in Griblje«)",
    url: "https://geohub.gov.si/ags/rest/services/MK/MK_EVRD/MapServer/3603",
    licenseSi: "uradni državni vir (GOV.SI / OPSI)",
    retrievedAt: "2026-10-08",
  },
  {
    id: "src-esd10094",
    kind: "OFFICIAL_GIS",
    nameSi: "EŠD 10094 — Griblje, arheološko najdišče ob Kolpi (obkolpska ravnina med Krasincem in južnim delom vasi)",
    nameEn: "EŠD 10094 — Griblje, archaeological site by the Kolpa (river plain between Krasinec and the southern part of the village)",
    url: "https://geohub.gov.si/ags/rest/services/MK/MK_EVRD/MapServer/3605",
    licenseSi: "uradni državni vir (GOV.SI / OPSI)",
    retrievedAt: "2026-10-08",
  },
  {
    id: "src-osm",
    kind: "CORROBORATING",
    nameSi: "OpenStreetMap (stavba Sv. Vid way 284847361, pokopališče 284847363, place node Griblje 468490150, struga Kolpe)",
    nameEn: "OpenStreetMap (Sv. Vid building way 284847361, cemetery 284847363, Griblje place node 468490150, Kolpa channel)",
    url: "https://www.openstreetmap.org/",
    licenseSi: "© avtorji OpenStreetMap, ODbL",
    retrievedAt: "2026-10-08",
  },
  {
    id: "src-a02-sheet",
    kind: "ARCHIVAL_PRIMARY",
    nameSi: "Franciscejski kataster, list A02 (SI AS 176) — cerkev na px(1995,577) z apsido, križem in pokopališkim obroblom",
    nameEn: "Franciscean cadastre, sheet A02 (SI AS 176) — church at px(1995,577) with apse, cross and churchyard boundary",
    retrievedAt: "2026-10-07",
  },
  {
    id: "src-geotruth-fix",
    kind: "OWN_GEOREF",
    nameSi: "GEOTRUTH afina (issue #14): listi A01/A02 zasidrani na uradni EŠD 2122; struga Kolpe potrjena 6–30 m; translacija starih podatkov −0,005190 lat / −0,001889 lng",
    nameEn: "GEOTRUTH affine (issue #14): sheets A01/A02 anchored to the official EŠD 2122; Kolpa channel confirmed at 6–30 m; legacy data translated by −0.005190 lat / −0.001889 lng",
    retrievedAt: "2026-10-08",
  },
  {
    id: "src-commons-ribnik",
    kind: "CORROBORATING",
    nameSi: "Wikimedia Commons geotag fotografije vaškega ribnika (45,5766 N 15,2864 E) — v nasprotju s koordinato zapisnika MVG-016 (razlika ~650 m)",
    nameEn: "Wikimedia Commons geotag of the village pond photo (45.5766 N 15.2864 E) — contradicting the MVG-016 record coordinate (~650 m apart)",
    retrievedAt: "2026-10-08",
  },
  {
    id: "src-mvg-record",
    kind: "OWN_GEOREF",
    nameSi: "Koordinate zapisov zbirke MVG (muzejska georeferenca, issue #12: mlini MVG-009, letališče Otok MVG-013) — reprezentativne/grobe točke, terenska preverba čaka",
    nameEn: "MVG collection record coordinates (the museum's own georeference, issue #12: mills MVG-009, Otok airfield MVG-013) — representative/coarse points, field check pending",
    retrievedAt: "2026-10-08",
  },
];

/* ── 2. GeoTruth sidra (issue #14, točka 3 + 5) ────────────────────────── */

export type CoordinateStatus =
  | "VERIFIED" // uradni vir + vsaj 1 neodvisno potrditev
  | "CORROBORATED" // ≥ 2 neodvisna vira, brez uradnega
  | "RECONSTRUCTED" // izpeljano (npr. kataster pod afino)
  | "APPROXIMATE" // približek (vas, območje)
  | "REVIEW" // znan konflikt, čaka razrešitev
  | "TO_COLLECT"; // podatka še ni

export interface GeoAnchorTruth {
  id: string;
  museumRef?: string;
  heritageRef?: string;
  lat: number;
  lng: number;
  altitudeM?: number;
  sourceIds: string[];
  coordinateStatus: CoordinateStatus;
  accuracyM?: number;
  lastVerified?: string;
  /** odmik kompasa, če je bil kadarkoli izmerjen za to sidro (°, dokumentiran razlog) */
  headingOffsetDeg?: number;
  noteSi?: string;
  noteEn?: string;
  /** ali je sidro trenutno AR-ready (podatek + asset + orientacija) */
  arReady: boolean;
}

export const GEO_ANCHORS: GeoAnchorTruth[] = [
  {
    id: "anchor-cerkev",
    museumRef: "MVG-002",
    heritageRef: "EŠD 2122",
    lat: 45.56761,
    lng: 15.290311,
    sourceIds: ["src-esd2122", "src-osm", "src-a02-sheet"],
    coordinateStatus: "VERIFIED",
    accuracyM: 15,
    lastVerified: "2026-10-08",
    noteSi:
      "Poligon EŠD 2122 (centroid); stavba OSM 8 m znotraj. Konflikt razrešen 2026-10-08: stara predpostavka 45,5728/15,2922 (jedro vasi) je odstopala 595 m — izvirala iz krožne georeference (cerkev je bila lastna kontrolna točka). Glej src-geotruth-fix.",
    noteEn:
      "EŠD 2122 polygon (centroid); the OSM building lies 8 m inside it. Conflict resolved 2026-10-08: the old assumption 45.5728/15.2922 (village core) was 595 m off — it came from a circular georeference (the church was its own control point). See src-geotruth-fix.",
    arReady: true,
  },
  {
    id: "anchor-spomenik",
    museumRef: "MVG-029",
    heritageRef: "EŠD 19326",
    lat: 45.571396,
    lng: 15.292355,
    sourceIds: ["src-esd19326"],
    coordinateStatus: "VERIFIED",
    accuracyM: 12,
    lastVerified: "2026-10-08",
    noteSi:
      "Uradni poligon EŠD 19326: »Spomenik stoji pred osnovno šolo v Gribljah.« Prejšnja koordinata zapisa (45,5754) je odstopala 447 m.",
    noteEn:
      "Official EŠD 19326 polygon: »The memorial stands in front of the primary school in Griblje.« The record's previous coordinate (45.5754) was 447 m off.",
    arReady: true,
  },
  {
    id: "anchor-jedro-1825",
    museumRef: "MVG-001",
    lat: 45.57092,
    lng: 15.29435,
    sourceIds: ["src-a02-sheet", "src-geotruth-fix"],
    coordinateStatus: "RECONSTRUCTED",
    accuracyM: 80,
    lastVerified: "2026-10-08",
    noteSi:
      "Gostota severnega sklopa vasi 1825 po GEOTRUTH afini (severni konec pasu; vas 1825: z ≈ 160–1500 m, dva sklopa ob cerkvi). Današnje jedro (OSM place node) je ~370 m severneje — vas je po 1825 zrasla proti severu.",
    noteEn:
      "Density peak of the northern 1825 cluster under the GEOTRUTH affine (north end of the ribbon; the 1825 village spans z ≈ 160–1500 m, two clusters around the church). Today's centre (OSM place node) lies ~370 m further north — the village grew northward after 1825.",
    arReady: true,
  },
  {
    id: "anchor-kolpa",
    museumRef: "MVG-006",
    lat: 45.5688,
    lng: 15.2988,
    sourceIds: ["src-osm", "src-esd10094"],
    coordinateStatus: "CORROBORATED",
    accuracyM: 25,
    lastVerified: "2026-10-08",
    noteSi:
      "Točka ob sodobni strugi (OSM; 3 m) — carinarnica 1809–1813 (MVG-092) je zgodovinski zapis brez geometrije. Arheološka cona EŠD 10094 ob Kolpi.",
    noteEn:
      "A point by the modern channel (OSM; 3 m) — the 1809–1813 customs post (MVG-092) is a historical record without geometry. Archaeological zone EŠD 10094 lies by the Kolpa.",
    arReady: true,
  },
  {
    id: "anchor-ribnik",
    museumRef: "MVG-016",
    lat: 45.5735,
    lng: 15.294,
    sourceIds: ["src-commons-ribnik"],
    coordinateStatus: "REVIEW",
    accuracyM: 650,
    lastVerified: "2026-10-08",
    noteSi:
      "KONFLIKT: geotag Commons (45,5766 N 15,2864 E) ~650 m od koordinate zapisa MVG-016. Terenska preverba čaka — do takrat odklepanje deluje na obeh močnih legah.",
    noteEn:
      "CONFLICT: the Commons geotag (45.5766 N 15.2864 E) is ~650 m from the MVG-016 record coordinate. Field check pending — until then unlocking works at both candidate positions.",
    arReady: false,
  },
  {
    id: "anchor-meja",
    museumRef: "MVG-015",
    lat: 45.5675,
    lng: 15.2995,
    sourceIds: ["src-osm"],
    coordinateStatus: "APPROXIMATE",
    accuracyM: 120,
    lastVerified: "2026-10-08",
    noteSi: "Meja (1991) poteka ob Kolpi; točka leži ~60 m vzhodno od struge — približek za odklep, ne geometrija meje.",
    noteEn: "The border (1991) follows the Kolpa; the point lies ~60 m east of the channel — an approximation for unlocking, not border geometry.",
    arReady: true,
  },
  {
    id: "anchor-cerkvisce",
    museumRef: "MVG-040",
    lat: 45.5759667,
    lng: 15.2643167,
    sourceIds: ["src-osm"],
    coordinateStatus: "CORROBORATED",
    accuracyM: 100,
    lastVerified: "2026-10-08",
    noteSi: "OSM place node Cerkvišče — tri cerkvice, ki jih ni več (zgodovinski zapis). Mini-scena (issue #12): trije duhovi + kapelica 1994 — postavitev INTERPRETACIJA (lega tretje cerkvice neznana).",
    noteEn: "OSM place node Cerkvišče — three vanished churches (historical record). Mini-scene (issue #12): three ghosts + the 1994 chapel — placement is an INTERPRETATION (the third church's position unknown).",
    arReady: true,
  },
  {
    id: "anchor-mlini",
    museumRef: "MVG-009",
    lat: 45.5315,
    lng: 15.3119,
    sourceIds: ["src-mvg-record"],
    coordinateStatus: "APPROXIMATE",
    accuracyM: 1500,
    lastVerified: "2026-10-08",
    noteSi: "Mlini ob Kolpi — reprezentativna točka mlinarskega območja (Dol, Radenci, Pobrežje, Krasinec), ne lega posameznega mlina. Proceduralna mini-scena (issue #12) prikazuje VRSTO mlina (žimaln). Terenska preverba čaka.",
    noteEn: "Mills on the Kolpa — a representative point of the milling stretch (Dol, Radenci, Pobrežje, Krasinec), not a single mill's position. The procedural mini-scene (issue #12) shows the mill TYPE (žimaln). Field check pending.",
    arReady: true,
  },
  {
    id: "anchor-otok",
    museumRef: "MVG-013",
    lat: 45.665,
    lng: 15.323,
    sourceIds: ["src-mvg-record"],
    coordinateStatus: "APPROXIMATE",
    accuracyM: 1000,
    lastVerified: "2026-10-08",
    noteSi: "Partizansko letališče Otok (~10 km severno od Gribelj) — groba koordinata travnika; zapis je story-only (brez 3D, spomenik Dakota stoji fizično). Terenska preverba čaka.",
    noteEn: "The Otok partisan airfield (~10 km north of Griblje) — a coarse meadow coordinate; the spot is story-only (no 3D, the Dakota monument stands in the physical world). Field check pending.",
    arReady: true,
  },
  {
    id: "anchor-origin",
    lat: 45.5725,
    lng: 15.2926,
    sourceIds: ["src-osm"],
    coordinateStatus: "CORROBORATED",
    accuracyM: 60,
    lastVerified: "2026-10-08",
    noteSi:
      "Izhodišče lokalnega koordinatnega sistema 3D scene (sodobno jedro vasi, OSM place node 468490150). Ni zgodovinsko jedro 1825 — to je ~370 m JZ (anchor-jedro-1825).",
    noteEn:
      "Origin of the 3D scene's local coordinate system (modern village centre, OSM place node 468490150). Not the 1825 core — that lies ~370 m SW (anchor-jedro-1825).",
    arReady: true,
  },
];

/** Sidra, ki jih še čakamo. P1 (issue #12) je vpisala mlini, otok in
 *  cerkvišče kot APPROXIMATE/CORROBORATED — terenska preverba njihovih
 *  leg ostaja odprta (zabeležena v note vsakega sidra). */
export const GEO_ANCHORS_TO_COLLECT: GeoAnchorTruth[] = [];

/* ── 2b. Resnica na ravni LISTOV katastra (issue #14, P45) ────────────────
 *
 * Listi A03/A04/A05 nimajo točkovnih sidrov vrste cerkev/most/sotočje
 * (ruralni listi brez takih objektov). P45 (2026-10-12) je namesto tega
 * izvedla VALIDACIJO PORAZDELITVE STAVB: rdeči stavbni simboli 1825
 * (detektor kalibriran na A02: F1 0,56, recall@50 0,94) proti sodobnim
 * stavbnim parcelam GURS (k.o. 1544 + 1552, < 800 m², 1.500 točk) pod
 * celično preslikavo eZKN. Kalibracija metode na A02 (156 stavb, GEOTRUTH):
 * merilo 0,805 m/px (celično 0,80 — soglasje < 1 %), rotacija +0,02°,
 * ostanek 2,4 m — celično izračunano merilo je zanesljiv prior.
 *
 * Rezultat: VSE TRI celične umestitve so kvantitativno potrjene (mediane
 * 89/70/27 m). Prosti fitovi so nestabilni (nafizikalna merila/rotacije)
 * ali premaknejo oznake s k.o.-validiranih mest → objavljena ostaja
 * CELIČNA preslikava s pošteno oceno napake. Dokaz: research/georef-n83/
 * p45-sheet-fits.json + scripts/p45-sheet-anchors.py + scripts/p45-verify.py. */

export interface SheetGeorefTruth {
  sheet: string;
  /** eZKN sekcijska celica (okvirna oznaka lista = koda celice, GURS uradna geometrija) */
  cellCode: string;
  /** [sever, zahod], [jug, vzhod] celice */
  cellBounds: [[number, number], [number, number]];
  scaleMPerPixel: number;
  /** validacija porazdelitve stavb (P45) */
  validation: {
    detectedSymbols: number;
    modernBuildings: number;
    medianDistanceM: number;
    inlier30: number;
    constrainedFitMedianM: number;
    constrainedFitDeltaM: number;
    discrimination: number;
    lastVerified: string;
  };
  status: CoordinateStatus;
  noteSi: string;
  noteEn: string;
}

export const SHEET_TRUTH: SheetGeorefTruth[] = [
  {
    sheet: "A03",
    cellCode: "VKIX24dg",
    cellBounds: [[45.5575, 15.2485], [45.5437, 15.273]],
    scaleMPerPixel: 0.72,
    validation: {
      detectedSymbols: 30,
      modernBuildings: 51,
      medianDistanceM: 89,
      inlier30: 0.067,
      constrainedFitMedianM: 153.3,
      constrainedFitDeltaM: 278,
      discrimination: 0.103,
      lastVerified: "2026-10-12",
    },
    status: "REVIEW",
    noteSi:
      "P45: veriga ~30 stavbnih simbolov ob vzhodnem robu (x 86–93 %, y 13–86 %) pod celično preslikavo pade na sodobno verigo 51 stavb z mediano 89 m — nadaljevanje vasi proti jugu potrjeno. Prosti fit izboljša mediano le z nafizikalnimi parametri (rotacija +12°, merilo 0,60 m/px — zavrnjeno); omejeni fit (merilo = celično ±5 %, rotacija ±3°) je SLABŠI od celice (153 m) — celična preslikava ostaja najboljša objavljena. Oznaki TRIBUTSCH/WEIDENDORF pod celico padata v k.o. Tribuče/Bedenj (P10 ✓). Iskanje dodatnega sidra čaka na #12 (paleografija) / #13 (vektorizacija).",
    noteEn:
      "P45: a chain of ~30 building symbols along the eastern edge (x 86–93 %, y 13–86 %) under the cell mapping lands on the modern chain of 51 buildings at a median of 89 m — the village's southern continuation confirmed. The free fit improves the median only with non-physical parameters (rotation +12°, scale 0.60 m/px — rejected); the constrained fit (scale = cell ±5 %, rotation ±3°) is WORSE than the cell (153 m) — the cell mapping remains the best published. The TRIBUTSCH/WEIDENDORF labels under the cell fall in c.m. Tribuče/Bedenj (P10 ✓). The search for an additional anchor awaits #12 (palaeography) / #13 (vectorisation).",
  },
  {
    sheet: "A04",
    cellCode: "VKIX24cg",
    cellBounds: [[45.5574, 15.2728], [45.5436, 15.2973]],
    scaleMPerPixel: 0.72,
    validation: {
      detectedSymbols: 170,
      modernBuildings: 440,
      medianDistanceM: 69.7,
      inlier30: 0.118,
      constrainedFitMedianM: 55.1,
      constrainedFitDeltaM: 310,
      discrimination: 0.15,
      lastVerified: "2026-10-12",
    },
    status: "REVIEW",
    noteSi:
      "P45: 170 zaznanih simbolov po celem listu pod celično preslikavo doseže mediano 69,7 m do sodobnih stavb — celična umestitev POPRAVEK P10 kvantitativno potrjena (P9-lega je imela 636 m). Omejeni fit izboljša mediano na 55 m, a premakne težišče za 310 m in odnese oznako WEIDENDORF iz k.o. Bedenj (v k.o. Adlešiči) → zavrnjen v prid celice (križna preverba oznak zmaga nad 15 m izboljšave). Merilo fita 0,722 ≈ celično 0,717 (soglasje 0,6 %). Kolpa NI na listu (struga ~1,2 km V) — potrjeno tudi s P45.",
    noteEn:
      "P45: 170 detected symbols across the whole sheet under the cell mapping reach a median of 69.7 m to modern buildings — the P10 cell placement (the P10 CORRECTION) quantitatively confirmed (the P9 position had 636 m). The constrained fit improves the median to 55 m but shifts the centroid by 310 m and carries the WEIDENDORF label out of c.m. Bedenj (into c.m. Adlešiči) → rejected in favour of the cell (label cross-validation wins over a 15 m improvement). The fit's scale 0.722 ≈ the cell's 0.717 (0.6 % agreement). The Kolpa is NOT on the sheet (channel ~1.2 km E) — confirmed by P45 as well.",
  },
  {
    sheet: "A05",
    cellCode: "VKIX24ch",
    cellBounds: [[45.5437, 15.2726], [45.5299, 15.2971]],
    scaleMPerPixel: 0.73,
    validation: {
      detectedSymbols: 30,
      modernBuildings: 535,
      medianDistanceM: 27,
      inlier30: 0.6,
      constrainedFitMedianM: 23.2,
      constrainedFitDeltaM: 64,
      discrimination: 0.288,
      lastVerified: "2026-10-12",
    },
    status: "REVIEW",
    noteSi:
      "P45: sklop ~30 simbolov (x 52–86 %, y 14–34 %) pod celično preslikavo pade na sodobne stavbe z mediano 27 m (60 % znotraj 30 m!) — sklop pri (45,5404 N, 15,2908 E) = območje Fučkovci/Jankoviči. OMEJENI fit (merilo 0,692, rotacija −2,0°) neodvisno potrdi celično lego z odmikom le 64 m — dva neodvisna vira (eZKN celica + GURS stavbe) se strinjata. Oznaka ADLESC → naselje Fučkovci (k.o. Adlešiči ✓). ODPRTA DVOUMNOST: prosta translacija v coni najde višje ocene na VZ robu celice (score 0,915 pri 45,5328/15,2974 — brez naselja, zunaj celice) — gostota sodobnih stavb metrike ne loči popolnoma; zavrnjeno na dokazu okvirne kode (3× prebrana), dokumentirano za #12/#13.",
    noteEn:
      "P45: a cluster of ~30 symbols (x 52–86 %, y 14–34 %) under the cell mapping lands on modern buildings with a median of 27 m (60 % within 30 m!) — the cluster at (45.5404 N, 15.2908 E) = the Fučkovci/Jankoviči area. The CONSTRAINED fit (scale 0.692, rotation −2.0°) independently confirms the cell position with an offset of only 64 m — two independent sources (the eZKN cell + GURS buildings) agree. The ADLESC label → the settlement of Fučkovci (c.m. Adlešiči ✓). OPEN AMBIGUITY: a free translation within the zone finds higher scores at the cell's E-SE edge (score 0.915 at 45.5328/15.2974 — no settlement, outside the cell) — the density of modern buildings prevents full discrimination; rejected on the frame-code evidence (read 3×), documented for #12/#13.",
  },
];

/* ── 3. Orientacija/skala 3D assetov (issue #14, točka 13) ────────────── */

export type ScaleMode = "REAL_WORLD" | "FIT" | "INTERPRETATIVE";

export interface AssetOrientation {
  assetUrl: string;
  anchorId: string;
  scaleMode: ScaleMode;
  /** ciljna višina v metrih (dokumentirano) */
  targetHeightM?: number;
  /** zasuk modela okoli navpične osi (°, 0 = privzeta usmerjenost datoteke) */
  rotationYDeg: number;
  orientationNoteSi: string;
  orientationNoteEn: string;
  /** ali je usmerjenost proti severu terensko preverjena */
  fieldVerified: boolean;
}

export const ASSET_ORIENTATIONS: AssetOrientation[] = [
  {
    assetUrl: "/models/cerkev-sv-vida.glb",
    anchorId: "anchor-cerkev",
    scaleMode: "REAL_WORLD",
    targetHeightM: 13,
    rotationYDeg: 0,
    orientationNoteSi:
      "Realno merilo: višina modela 13 m (skala iz CHURCH.targetH). Zasuk proti severu ni dokumentiran v katastru — privzeta usmerjenost GLB (TO_COLLECT: terenska preverba z zvonikom).",
    orientationNoteEn:
      "Real-world scale: model height 13 m (from CHURCH.targetH). Northward rotation is not documented in the cadastre — the GLB's default orientation (TO_COLLECT: field check against the bell tower).",
    fieldVerified: false,
  },
  {
    assetUrl: "/models/cerkev-sv-vida.usdz",
    anchorId: "anchor-cerkev",
    scaleMode: "REAL_WORLD",
    targetHeightM: 13,
    rotationYDeg: 0,
    orientationNoteSi:
      "USDZ dvojnik GLB (iOS Quick Look) — ista pogodba o skali; usmerjenost odvisna od Quick Look postavitve (uporabnik postavi ročno).",
    orientationNoteEn:
      "USDZ twin of the GLB (iOS Quick Look) — same scale contract; orientation depends on Quick Look placement (the user places it manually).",
    fieldVerified: false,
  },
  {
    assetUrl: "procedural:mlini",
    anchorId: "anchor-mlini",
    scaleMode: "INTERPRETATIVE",
    targetHeightM: 4,
    rotationYDeg: 0,
    orientationNoteSi:
      "Proceduralna mini-scena vodnega mlina (issue #12, brez datoteke — < 1 MB): hiša ~4 m + kolo + jez + toča. INTERPRETACIJA vrste (žimaln — vodoravno kolo znotraj; vidno kolo je ikonografska interpretacija), merila po strokovni literaturi o slovenskih mlinih. Postavitev na reprezentativni točki mlinarskega območja — terenska preverba čaka.",
    orientationNoteEn:
      "Procedural water-mill mini-scene (issue #12, no file — < 1 MB): house ~4 m + wheel + weir + millstream. An INTERPRETATION of the type (žimaln — a horizontal wheel inside; the visible wheel is an iconographic interpretation), dimensions from the scholarly literature on Slovene mills. Placed at a representative point of the milling stretch — field check pending.",
    fieldVerified: false,
  },
  {
    assetUrl: "procedural:cerkvisce",
    anchorId: "anchor-cerkvisce",
    scaleMode: "INTERPRETATIVE",
    targetHeightM: 5,
    rotationYDeg: 0,
    orientationNoteSi:
      "Proceduralna mini-scena Cerkvišča (issue #12, brez datoteke): trije duhovi cerkvic (~5 m z zvonikom, rdeči žični — »ni jih več«) + bela kapelica 1994 (~2,2 m, trdna — edini ohranjeni kamen). Postavitev treh cerkvic je INTERPRETACIJA: za dve domnevno vaščani vesta, kje sta stali, za tretjo ne ve nihče. Lega sidra = OSM place node (CORROBORATED ~100 m).",
    orientationNoteEn:
      "Procedural Cerkvišče mini-scene (issue #12, no file): three church ghosts (~5 m with the tower, red wireframe — »no more«) + the white 1994 chapel (~2.2 m, solid — the only surviving stone). The three churches' placement is an INTERPRETATION: for two the villagers believe they know where they stood, of the third no one knows. Anchor = OSM place node (CORROBORATED ~100 m).",
    fieldVerified: false,
  },
];

/* ── 4. Dokumentiran popravek georeference (dokazna pot zgoraj) ────────── */

export interface GeoCorrection {
  id: string;
  appliedToSi: string;
  dlat: number;
  dlng: number;
  eastM: number;
  southM: number;
  resolvedConflictSi: string;
  evidence: { stepSi: string; stepEn: string }[];
  appliedAt: string;
}

export const A02_CORRECTION: GeoCorrection = {
  id: "geotruth-a02-2026-10-08",
  appliedToSi:
    "buildings.json (156 stavb), raba tal (landuse.ts), CHURCH (village3d.ts), TimeSpot cerkev/jedro/gornje, MVG-002/003/029",
  dlat: -0.00519,
  dlng: -0.001889,
  eastM: -147,
  southM: 578,
  resolvedConflictSi:
    "Cerkev sv. Vida: stara koordinata (45,5728 N 15,2922 E, krožna georeferenca) ↔ uradni EŠD 2122 (45,567610 N 15,290311 E) — 595 m. Razrešeno v korist uradnega vira.",
  evidence: [
    {
      stepSi: "1. Uradni register (GisKD, layer 3602): poligon EŠD 2122, centroid 45,567610/15,290311, »na pokopališču, na gričku južno od vasi«.",
      stepEn: "1. Official register (GisKD, layer 3602): EŠD 2122 polygon, centroid 45.567610/15.290311, »at the cemetery, on a hill south of the village«.",
    },
    {
      stepSi: "2. OSM: stavba »Sv. Vid« + pokopališče znotraj uradnega poligona (≤ 8 m) — dva neodvisna vira se ujemata.",
      stepEn: "2. OSM: the »Sv. Vid« building + cemetery inside the official polygon (≤ 8 m) — two independent sources agree.",
    },
    {
      stepSi: "3. List A02: cerkev (apsida, križ, pokopališki obrobl) narisana na px(1995,577); stara afina je bila krožna (cerkev = lastna kontrolna točka).",
      stepEn: "3. Sheet A02: the church (apse, cross, churchyard) drawn at px(1995,577); the old affine was circular (the church was its own control point).",
    },
    {
      stepSi: "4. Struga Kolpe na listu (VLM: x 2765–2890 pri y 100–1400) se s sodobno strugo ujeme le pod cerkveno zasidrano afino (6–30 m); stara afina odstopa 80–130 m.",
      stepEn: "4. The Kolpa channel on the sheet (VLM: x 2765–2890 at y 100–1400) matches the modern channel only under the church-anchored affine (6–30 m); the old affine is off by 80–130 m.",
    },
    {
      stepSi: "5. Kontroli A01 se re-interpretirata konsistentno: »jedro« (px 2091,1773) = cerkev (34 m), »severna skupina« (px 2063,1477) = severni rob vasi 1825.",
      stepEn: "5. The A01 control points reinterpret consistently: the »core« (px 2091,1773) = the church (34 m), the »northern cluster« (px 2063,1477) = the north end of the 1825 village.",
    },
    {
      stepSi: "6. Porazdelitve razdalj stavb od cerkve: 1825 (list) in danes (OSM) se ujemata (p50 502 m : 509 m) — odnos vas↔cerkev se ohranja, absolutna lega pa sledi uradnemu sidru.",
      stepEn: "6. Building-distance distributions from the church: 1825 (sheet) and today (OSM) agree (p50 502 m : 509 m) — the village↔church relationship holds; the absolute position follows the official anchor.",
    },
  ],
  appliedAt: "2026-10-08",
};

/* ── 5. Samodejni detektor konfliktov (issue #14, točka 6) ─────────────── */

export type AuditSeverity = "INFO" | "REVIEW" | "CONFLICT" | "CRITICAL";

export interface GeoAuditIssue {
  severity: AuditSeverity;
  code: string;
  refs: string[];
  detailSi: string;
  detailEn: string;
}

/** Pragi (namenski, ne slepi): <5 m normalno; 5–30 m REVIEW; 30–300 m CONFLICT; >300 m CRITICAL */
export const GEO_THRESHOLDS = { ok: 5, review: 30, conflict: 300 } as const;

function findAnchor(id: string): GeoAnchorTruth | undefined {
  return [...GEO_ANCHORS, ...GEO_ANCHORS_TO_COLLECT].find((a) => a.id === id);
}

/**
 * Audit vseh AR sidrov: TimeSpot ↔ GeoTruth povezave, podvojeni museumRef,
 * VERIFIED brez uradnega/arhivskega vira, model3dUrl brez sidra/orientacije.
 * Čista funkcija — pokliči v testu ali iz API-ja.
 */
export function auditGeoAnchors(): GeoAuditIssue[] {
  const issues: GeoAuditIssue[] = [];
  const anchors = [...GEO_ANCHORS, ...GEO_ANCHORS_TO_COLLECT];

  /* TimeSpot brez GeoTruth povezave ali z odmikom */
  for (const spot of TIME_SPOTS) {
    const anchorId = (spot as TimeSpotWithAnchor).anchorId;
    if (!anchorId) {
      issues.push({
        severity: "CONFLICT",
        code: "SPOT_NO_ANCHOR",
        refs: [spot.id],
        detailSi: `TimeSpot »${spot.id}« nima GeoTruth povezave.`,
        detailEn: `Time spot »${spot.id}« has no GeoTruth link.`,
      });
      continue;
    }
    const anchor = findAnchor(anchorId);
    if (!anchor) {
      issues.push({
        severity: "CONFLICT",
        code: "SPOT_ANCHOR_MISSING",
        refs: [spot.id, anchorId],
        detailSi: `TimeSpot »${spot.id}« se sklicuje na neobstoječe sidro »${anchorId}«.`,
        detailEn: `Time spot »${spot.id}« references a missing anchor »${anchorId}«.`,
      });
      continue;
    }
    const d = distanceM(spot, anchor);
    if (d > GEO_THRESHOLDS.conflict) {
      issues.push({
        severity: "CRITICAL",
        code: "SPOT_ANCHOR_DRIFT",
        refs: [spot.id, anchorId],
        detailSi: `TimeSpot »${spot.id}« odstopa ${Math.round(d)} m od sidra »${anchorId}« (> ${GEO_THRESHOLDS.conflict} m).`,
        detailEn: `Time spot »${spot.id}« drifts ${Math.round(d)} m from anchor »${anchorId}« (> ${GEO_THRESHOLDS.conflict} m).`,
      });
    } else if (d > GEO_THRESHOLDS.review) {
      issues.push({
        severity: "CONFLICT",
        code: "SPOT_ANCHOR_DRIFT",
        refs: [spot.id, anchorId],
        detailSi: `TimeSpot »${spot.id}« odstopa ${Math.round(d)} m od sidra »${anchorId}« (5–30 m).`,
        detailEn: `Time spot »${spot.id}« drifts ${Math.round(d)} m from anchor »${anchorId}« (5–30 m).`,
      });
    } else if (d > GEO_THRESHOLDS.ok) {
      issues.push({
        severity: "REVIEW",
        code: "SPOT_ANCHOR_DRIFT",
        refs: [spot.id, anchorId],
        detailSi: `TimeSpot »${spot.id}« odstopa ${Math.round(d)} m od sidra »${anchorId}« (5–30 m).`,
        detailEn: `Time spot »${spot.id}« drifts ${Math.round(d)} m from anchor »${anchorId}« (5–30 m).`,
      });
    }
  }

  /* isti museumRef na različnih koordinatah */
  const byRef = new Map<string, GeoAnchorTruth[]>();
  for (const a of anchors) {
    if (!a.museumRef) continue;
    byRef.set(a.museumRef, [...(byRef.get(a.museumRef) ?? []), a]);
  }
  for (const [ref, list] of byRef) {
    for (let i = 0; i < list.length; i += 1) {
      for (let j = i + 1; j < list.length; j += 1) {
        const d = distanceM(list[i], list[j]);
        if (d > GEO_THRESHOLDS.ok) {
          issues.push({
            severity: d > GEO_THRESHOLDS.conflict ? "CRITICAL" : "CONFLICT",
            code: "DUP_MUSEUM_REF",
            refs: [list[i].id, list[j].id],
            detailSi: `${ref} na dveh koordinatah (${list[i].id}, ${list[j].id}), razlika ${Math.round(d)} m.`,
            detailEn: `${ref} at two coordinates (${list[i].id}, ${list[j].id}), ${Math.round(d)} m apart.`,
          });
        }
      }
    }
  }

  /* VERIFIED brez uradnega/arhivskega vira ali brez evidence */
  for (const a of anchors) {
    if (a.coordinateStatus !== "VERIFIED") continue;
    const kinds = a.sourceIds.map((sid) => GEO_SOURCES.find((s) => s.id === sid)?.kind);
    const hasStrong = kinds.some((k) => k === "OFFICIAL_GIS" || k === "ARCHIVAL_PRIMARY");
    if (!hasStrong) {
      issues.push({
        severity: "CRITICAL",
        code: "VERIFIED_NO_SOURCE",
        refs: [a.id],
        detailSi: `Sidro »${a.id}« je VERIFIED brez uradnega/arhivskega vira.`,
        detailEn: `Anchor »${a.id}« is VERIFIED without an official/archival source.`,
      });
    }
    if (a.sourceIds.length < 2) {
      issues.push({
        severity: "REVIEW",
        code: "VERIFIED_SINGLE_SOURCE",
        refs: [a.id],
        detailSi: `Sidro »${a.id}« je VERIFIED z enim samim virom.`,
        detailEn: `Anchor »${a.id}« is VERIFIED from a single source.`,
      });
    }
    if (!a.lastVerified) {
      issues.push({
        severity: "REVIEW",
        code: "VERIFIED_NO_DATE",
        refs: [a.id],
        detailSi: `Sidro »${a.id}« nima datuma preverjanja.`,
        detailEn: `Anchor »${a.id}« lacks a verification date.`,
      });
    }
  }

  /* REVIEW — znani konflikti ostanejo vidni */
  for (const a of anchors) {
    if (a.coordinateStatus === "REVIEW") {
      issues.push({
        severity: "CONFLICT",
        code: "ANCHOR_REVIEW",
        refs: [a.id],
        detailSi: `Sidro »${a.id}« je v REVIEW: ${(a.noteSi ?? "").slice(0, 140)}…`,
        detailEn: `Anchor »${a.id}« is in REVIEW: ${(a.noteEn ?? "").slice(0, 140)}…`,
      });
    }
  }

  /* model3dUrl brez stabilnega sidra / orientacije */
  for (const ex of EXHIBITS) {
    if (!ex.model3dUrl) continue;
    const anchor = anchors.find((a) => a.museumRef === ex.museumNo);
    if (!anchor) {
      issues.push({
        severity: "CONFLICT",
        code: "MODEL_NO_ANCHOR",
        refs: [ex.museumNo],
        detailSi: `3D model (${ex.model3dUrl}) nima GeoTruth sidra z museumRef ${ex.museumNo}.`,
        detailEn: `The 3D model (${ex.model3dUrl}) has no GeoTruth anchor with museumRef ${ex.museumNo}.`,
      });
      continue;
    }
    const lat = ex.lat ?? null;
    const lng = ex.lng ?? null;
    if (lat == null || lng == null) {
      issues.push({
        severity: "CONFLICT",
        code: "MODEL_NO_COORD",
        refs: [ex.museumNo],
        detailSi: `3D model (${ex.model3dUrl}) pripada zapisu brez koordinate.`,
        detailEn: `The 3D model (${ex.model3dUrl}) belongs to a record without coordinates.`,
      });
      continue;
    }
    const d = distanceM({ lat, lng }, anchor);
    if (d > GEO_THRESHOLDS.review) {
      issues.push({
        severity: "CONFLICT",
        code: "MODEL_ANCHOR_DRIFT",
        refs: [ex.museumNo, anchor.id],
        detailSi: `Zapis ${ex.museumNo} s 3D modelom odstopa ${Math.round(d)} m od sidra ${anchor.id}.`,
        detailEn: `Record ${ex.museumNo} with a 3D model drifts ${Math.round(d)} m from anchor ${anchor.id}.`,
      });
    }
    if (!ASSET_ORIENTATIONS.some((o) => o.anchorId === anchor.id && o.assetUrl === ex.model3dUrl)) {
      issues.push({
        severity: "REVIEW",
        code: "MODEL_NO_ORIENTATION",
        refs: [ex.museumNo],
        detailSi: `3D model (${ex.model3dUrl}) nima dokumentirane orientacije/skale.`,
        detailEn: `The 3D model (${ex.model3dUrl}) lacks documented orientation/scale.`,
      });
    }
  }

  /* headingOffset brez dokumentiranega razloga (v pripravo za #13) */
  for (const a of anchors) {
    if (a.headingOffsetDeg != null && !a.noteSi?.includes("headingOffset")) {
      issues.push({
        severity: "REVIEW",
        code: "HEADING_UNDOCUMENTED",
        refs: [a.id],
        detailSi: `Sidro »${a.id}« ima headingOffsetDeg ${a.headingOffsetDeg} brez dokumentiranega razloga.`,
        detailEn: `Anchor »${a.id}« has headingOffsetDeg ${a.headingOffsetDeg} without a documented reason.`,
      });
    }
  }

  return issues;
}

/** zapečaten poročilo (izračunano ob zagonu modula — enako za API in test) */
export const GEO_AUDIT_REPORT: GeoAuditIssue[] = auditGeoAnchors();

/* ── 6. GPS kakovost (issue #14, točka 9) ──────────────────────────────── */

export type GpsQuality = "NO_FIX" | "ACQUIRING" | "APPROXIMATE" | "GOOD" | "EXCELLENT";

/** Pragi prilagojeni merilu scene (vas, hiše ~15 m): EXCELLENT ≤ 8 m, GOOD ≤ 20 m. */
export const GPS_THRESHOLDS = { excellent: 8, good: 20 } as const;

export function gpsQualityFrom(
  watching: boolean,
  hasFix: boolean,
  accuracy: number | null,
): GpsQuality {
  if (!hasFix) return watching ? "ACQUIRING" : "NO_FIX";
  if (accuracy == null) return "APPROXIMATE";
  if (accuracy <= GPS_THRESHOLDS.excellent) return "EXCELLENT";
  if (accuracy <= GPS_THRESHOLDS.good) return "GOOD";
  return "APPROXIMATE";
}

export const GPS_QUALITY_LABEL: Record<GpsQuality, { si: string; en: string }> = {
  NO_FIX: { si: "brez GPS", en: "no GPS" },
  ACQUIRING: { si: "GPS se lovi", en: "GPS acquiring" },
  APPROXIMATE: { si: "GPS približno", en: "GPS approximate" },
  GOOD: { si: "GPS dobro", en: "GPS good" },
  EXCELLENT: { si: "GPS odlično", en: "GPS excellent" },
};

/* ── 7. Pogodba o pripravljenosti scene (issue #14, točki 11–12) ───────── */

export type AnchorConfidence = "HIGH" | "MEDIUM" | "LOW";
export type CompassStability = "unavailable" | "unstable" | "settling" | "stable";

export interface SceneReadiness {
  anchor: AnchorConfidence;
  sceneStatus: "READY" | "ALIGNING" | "APPROXIMATE";
  reasonSi: string;
  reasonEn: string;
}

/**
 * HIGH (SCENA PORAVNANA): GPS GOOD/EXCELLENT + kompas stabilen (± natančnost
 * scene). MEDIUM (Poravnava scene …): GPS APPROXIMATE ali kompas se umirja.
 * LOW (približno — raziskovanje): brez GPS ali brez kompasa (ročni obrat).
 */
export function sceneReadiness(args: {
  gps: GpsQuality;
  compass: CompassStability;
}): SceneReadiness {
  const { gps, compass } = args;
  if (gps === "NO_FIX" || gps === "ACQUIRING") {
    return {
      anchor: "LOW",
      sceneStatus: "APPROXIMATE",
      reasonSi: "brez GPS — prikaz za raziskovanje",
      reasonEn: "no GPS — exploration view",
    };
  }
  if (compass === "unavailable") {
    return {
      anchor: "LOW",
      sceneStatus: "APPROXIMATE",
      reasonSi: "kompas ni na voljo — obrat pogleda z vlečenjem",
      reasonEn: "compass unavailable — look around by dragging",
    };
  }
  if (gps === "APPROXIMATE") {
    return {
      anchor: "MEDIUM",
      sceneStatus: "ALIGNING",
      reasonSi: "GPS približen — poravnava scene je okvirna",
      reasonEn: "GPS approximate — scene alignment is coarse",
    };
  }
  if (compass === "unstable" || compass === "settling") {
    return {
      anchor: "MEDIUM",
      sceneStatus: "ALIGNING",
      reasonSi: "poravnava kompasa …",
      reasonEn: "compass aligning …",
    };
  }
  return {
    anchor: "HIGH",
    sceneStatus: "READY",
    reasonSi: "scena poravnana",
    reasonEn: "scene aligned",
  };
}

/* pomoč za tipiziran (obstoječi) anchorId na TimeSpotu (brez cikla uvozov) */
interface TimeSpotWithAnchor {
  id: string;
  lat: number;
  lng: number;
  anchorId?: string;
}
