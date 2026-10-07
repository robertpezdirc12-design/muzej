// ISSUE #4 — končni coverage pregled zbirke (113 zapisov) + sistematična
// 3D/AR priprava zgodovinskih objektov.
//
// Načelo: VSE številke se IZRAČUNAJO iz dejanskih podatkov
// (exhibits.json, extra.json, atlas hiše/stavbe/viri) — nič ni ročno
// vpisano. Pregled je povezan z dejanskim podatkovnim modelom.

import exhibitsRaw from "@/data/museum/exhibits.json";
import extraRaw from "@/data/museum/extra.json";
import { ATLAS_HOUSES } from "@/data/atlas/houses";
import { ATLAS_SOURCES, HERITAGE_UNITS } from "@/data/atlas/sources";
import { VECTOR_BUILDINGS } from "@/data/atlas/model";
import type { CategoryCode } from "./museum";

interface ExhibitRow {
  id: string;
  slug: string;
  museumNo: string;
  category: string;
  titleSi: string;
  titleEn: string;
  periodSi: string;
  periodEn: string;
  evidenceStatus: string;
  image: string | null;
  imageCredit: string | null;
  model3dUrl: string | null;
  yearFrom: number | null;
  yearTo: number | null;
  lat: number | null;
  lng: number | null;
  sources: { nameSi?: string | null; nameEn?: string | null; url?: string | null; license?: string | null }[] | null;
}

const EXHIBITS = (exhibitsRaw as { exhibits: ExhibitRow[] }).exhibits;
const EXTRA = extraRaw as Record<string, { walk?: { name?: string; station?: number } | null }>;

// ——— COVERAGE (issue #4 #3) ——————————————————————————

export interface CollectionCoverage {
  total: number;
  gps: { withGps: number; withoutGps: number };
  images: { withImage: number; withoutImage: number };
  models3d: { with3d: number; without3d: number };
  sources: { withSources: number; withoutSources: number };
  byEvidence: Record<string, number>;
  byCategory: Record<string, number>;
  byPeriod: { periodSi: string; periodEn: string; count: number }[];
  arReady: {
    /** model3dUrl + veljavna lat/lng → AR danes */
    readyNow: string[];
    /** ima lokacijo, manjka samo 3D model → kandidat */
    candidates: { slug: string; museumNo: string; titleSi: string; titleEn: string; lat: number; lng: number }[];
  };
  computedAt: string;
}

export function computeCoverage(): CollectionCoverage {
  const byEvidence: Record<string, number> = {};
  const byCategory: Record<string, number> = {};
  const byPeriodMap = new Map<string, { periodSi: string; periodEn: string; count: number }>();

  const readyNow: string[] = [];
  const candidates: CollectionCoverage["arReady"]["candidates"] = [];

  let withGps = 0;
  let withImage = 0;
  let with3d = 0;
  let withSources = 0;

  for (const e of EXHIBITS) {
    byEvidence[e.evidenceStatus ?? "(neznan)"] = (byEvidence[e.evidenceStatus ?? "(neznan)"] ?? 0) + 1;
    byCategory[e.category] = (byCategory[e.category] ?? 0) + 1;

    const pk = e.periodSi || "—";
    const rec = byPeriodMap.get(pk) ?? { periodSi: e.periodSi, periodEn: e.periodEn, count: 0 };
    rec.count++;
    byPeriodMap.set(pk, rec);

    const hasGps = e.lat != null && e.lng != null && Math.abs(e.lat) <= 90 && Math.abs(e.lng) <= 180;
    if (hasGps) withGps++;
    if (e.image) withImage++;
    if (e.model3dUrl) with3d++;
    if ((e.sources ?? []).length > 0) withSources++;

    if (e.model3dUrl && hasGps) {
      readyNow.push(e.museumNo);
    } else if (!e.model3dUrl && hasGps && e.lat != null && e.lng != null) {
      candidates.push({ slug: e.slug, museumNo: e.museumNo, titleSi: e.titleSi, titleEn: e.titleEn, lat: e.lat, lng: e.lng });
    }
  }

  const byPeriod = [...byPeriodMap.values()].sort((a, b) => b.count - a.count);

  return {
    total: EXHIBITS.length,
    gps: { withGps, withoutGps: EXHIBITS.length - withGps },
    images: { withImage, withoutImage: EXHIBITS.length - withImage },
    models3d: { with3d, without3d: EXHIBITS.length - with3d },
    sources: { withSources, withoutSources: EXHIBITS.length - withSources },
    byEvidence,
    byCategory,
    byPeriod,
    arReady: { readyNow, candidates },
    computedAt: new Date().toISOString(),
  };
}

// ——— SISTEMATIČNA 3D/AR PRIPRAVA (issue #4 #2) ——————————

/**
 * Enoten 3D/AR podatkovni tok, ZDAJŽEN z Atlasom #2 (ni ločen sistem):
 * zgodovinski objekt iz Atlasa (hiša/cerkev/stavba) + muzejski zapis
 * → samodejna kandidatura za 3D/AR brez dvojnega vnosa.
 *
 * Klasifikacija po issue #4:
 *  ORIGINAL      — obstoječi 3D model (cerkev sv. Vida)
 *  DERIVAT       — izpeljan iz obstoječega (ni še)
 *  RECONSTRUCTED — geometrija iz georeferenciranega lista (vektorizacija)
 *  INFERRED      — samo tipologija, brez dokazane geometrije
 */
export type ThreeDClass = "ORIGINAL" | "DERIVAT" | "RECONSTRUCTED" | "INFERRED";

export interface ThreeDPipelineEntry {
  id: string;
  /** muzejski zapis (kjer obstaja) */
  museumRef: string | null;
  titleSi: string;
  titleEn: string;
  klass: ThreeDClass;
  /** dokazano (iz vira) */
  evidenceSi: string;
  evidenceEn: string;
  /** kaj je interpretirano */
  interpretationSi: string;
  interpretationEn: string;
  hasIdentity: boolean;
  hasGeometry: boolean;
  hasLocation: boolean;
  hasModel: boolean;
  /** AR pripravljenost 0–5 (identiteta, vir, geometrija, lokacija, model) */
  readiness: { score: number; of: number };
  sourceCode: string;
}

/** Tok: zgodovinska hiša → dokaz → tipologija → geometrija → 3D → lokacija → AR */
export function compute3DPipeline(): ThreeDPipelineEntry[] {
  const entries: ThreeDPipelineEntry[] = [];

  // 1. ORIGINAL — cerkev sv. Vida (obstoječi interpretativni model, MVG-002)
  const churchEx = EXHIBITS.find((e) => e.museumNo === "MVG-002");
  if (churchEx && churchEx.model3dUrl && churchEx.lat != null && churchEx.lng != null) {
    entries.push({
      id: "3d-cerkev-sv-vida",
      museumRef: "MVG-002",
      titleSi: "Cerkev sv. Vida — 3D model (obstoječi)",
      titleEn: "St. Vitus church — 3D model (existing)",
      klass: "ORIGINAL",
      evidenceSi: "Lokacija: EŠD 2122 + OSM; tloris z apsido na listu A02 (oznaka K); višine iz splošne tipologije.",
      evidenceEn: "Location: EŠD 2122 + OSM; apsidal plan on sheet A02 (mark K); heights from general typology.",
      interpretationSi: "Oblika strehe, razporeditev odprtin in materiali so interpretacija (baročna tipologija Belokranjske).",
      interpretationEn: "Roof shape, opening layout and materials are an interpretation (Bela krajina baroque typology).",
      hasIdentity: true,
      hasGeometry: true,
      hasLocation: true,
      hasModel: true,
      readiness: { score: 5, of: 5 },
      sourceCode: "N083A02",
    });
  }

  // 2. RECONSTRUCTED — vektorizirane stavbe z lista A02 (156 objektov)
  //    ZDAJŽENO z Atlasom: VECTOR_BUILDINGS je isti podatkovni vir.
  const villageHouses = ATLAS_HOUSES.filter((h) => h.no !== "—" && h.no !== "7½" && h.no !== "8½");
  entries.push({
    id: "3d-stavbe-a02",
    museumRef: null,
    titleSi: `Stavbe vasi ~1825 — ${VECTOR_BUILDINGS.length} vektoriziranih objektov (list A02)`,
    titleEn: `Village buildings ~1825 — ${VECTOR_BUILDINGS.length} vectorised objects (sheet A02)`,
    klass: "RECONSTRUCTED",
    evidenceSi: "Tlorisi iz georeferenciranega katastrskega lista A02 (sekcija jedro vasi); velikosti v metrih.",
    evidenceEn: "Plans from the georeferenced cadastral sheet A02 (village-core section); sizes in metres.",
    interpretationSi: "Višine in strešne konstrukcije še niso izdelane — tipologija belokranjske hiše (zid + trsna streha) je pripravljena kot naslednji korak.",
    interpretationEn: "Heights and roof structures are not made yet — the Bela krajina house typology (stone walls + thatched roof) is prepared as the next step.",
    hasIdentity: true,
    hasGeometry: true,
    hasLocation: true,
    hasModel: false,
    readiness: { score: 3, of: 5 },
    sourceCode: "N083A02",
  });

  // 3. INFERRED — hiše iz PT z lastniki, a brez lokalne geometrije
  const housesWithMuseum = villageHouses.filter((h) => h.museumRef);
  entries.push({
    id: "3d-hise-pt",
    museumRef: housesWithMuseum.map((h) => h.museumRef).filter(Boolean).join(", ") || null,
    titleSi: `Hiše 1–98 (PT 1825) — ${villageHouses.length} identitet, ${housesWithMuseum.length} z muzejsko povezavo`,
    titleEn: `Houses 1–98 (PT 1825) — ${villageHouses.length} identities, ${housesWithMuseum.length} with a museum link`,
    klass: "INFERRED",
    evidenceSi: "Imena lastnikov + hišne št. iz Protokola stavbnih parcel (REVIEW prepis Kurrent); območje vasi APPROXIMATE.",
    evidenceEn: "Owner names + house numbers from the building-parcel protocol (REVIEW Kurrent transcription); village area APPROXIMATE.",
    interpretationSi: "Lokacija posamezne hiše na listu A02 še ni preslikana (razdelava številk ob stavbah = TO_COLLECT), zato je geometrija posamezne hiše sklep (tipologija).",
    interpretationEn: "The position of an individual house on sheet A02 is not yet mapped (assigning numbers to buildings = TO_COLLECT), so an individual house's geometry is an inference (typology).",
    hasIdentity: true,
    hasGeometry: false,
    hasLocation: false,
    hasModel: false,
    readiness: { score: 1, of: 5 },
    sourceCode: "N083PT",
  });

  // 4. kandidati iz zbirke (imajo GPS, manjka 3D) — AR-ready ko bo model
  const cov = computeCoverage();
  entries.push({
    id: "3d-kandidati-zbirka",
    museumRef: null,
    titleSi: `Muzejski zapisi s lokacijo brez 3D modela — ${cov.arReady.candidates.length} kandidatov`,
    titleEn: `Museum records with a location but no 3D model — ${cov.arReady.candidates.length} candidates`,
    klass: "INFERRED",
    evidenceSi: "GPS lokacije zapisov (osnovno stanje iz evidenceStatus); objekti iz zbirke z dejansko lokacijo v vasi.",
    evidenceEn: "Record GPS locations (baseline from evidenceStatus); collection objects with an actual village location.",
    interpretationSi: "3D model za posamezen objekt se izdela šele, ko so podatki (izmere, fotografije, viri) zadosti dobri — brez izmišljanja.",
    interpretationEn: "A 3D model for an object is made only when its data (measurements, photographs, sources) is good enough — nothing invented.",
    hasIdentity: true,
    hasGeometry: false,
    hasLocation: true,
    hasModel: false,
    readiness: { score: 2, of: 5 },
    sourceCode: "MVG",
  });

  return entries;
}

/** Povzetek 3D/AR pripravljenosti (strojno izračunan). */
export function compute3DSummary() {
  const entries = compute3DPipeline();
  const cov = computeCoverage();
  const atlasN83 = ATLAS_SOURCES.filter((s) => s.code.startsWith("N083"));
  return {
    classes: {
      ORIGINAL: entries.filter((e) => e.klass === "ORIGINAL").length,
      DERIVAT: entries.filter((e) => e.klass === "DERIVAT").length,
      RECONSTRUCTED: entries.filter((e) => e.klass === "RECONSTRUCTED").length,
      INFERRED: entries.filter((e) => e.klass === "INFERRED").length,
    } as Record<ThreeDClass, number>,
    modelsInCollection: cov.models3d.with3d,
    arReadyNow: cov.arReady.readyNow,
    arCandidates: cov.arReady.candidates.length,
    vectorizedBuildings: VECTOR_BUILDINGS.length,
    atlasHouses: ATLAS_HOUSES.filter((h) => h.no !== "—" && h.no !== "7½" && h.no !== "8½").length,
    heritageUnits: HERITAGE_UNITS.length,
    /** enote N83, iz katerih se 3D izpeljuje */
    atlasUnits: atlasN83.length,
    computedAt: new Date().toISOString(),
  };
}
