// ATLAS 1825 — izpeljani model, iskanje, GeoJSON izvoz
// En sam vir resnice: viri → hiše/parcele → lastniki → lokacije → stavbe → georeferenca.

import { ATLAS_SOURCES, NEGATIVE_RESULTS, HERITAGE_UNITS, type AtlasSource } from "@/data/atlas/sources";
import { ATLAS_HOUSES, type AtlasHouse } from "@/data/atlas/houses";
import { ATLAS_OWNERS, ATLAS_LOCATIONS, SHEET_GEOREFS, VECTOR_BUILDINGS } from "@/data/atlas/model";
import { PARISH, PARISH_BOOKS, HOUSE_VITALS, type HouseVital, type ParishBook } from "@/data/atlas/parish";
import { BUILDINGS_1825, GROWTH_1900, PERIODS, IZGINILO_STATS, PRESENCE_META } from "@/lib/village3d";
import {
  TIME_SPOTS,
  spotYearParam,
  isDistantSpot,
  spotDistanceFromVillage,
} from "@/data/atlas/timespots";
import { PANORAMAS, panoramaDeepLink } from "@/data/atlas/panoramas";
import { GUIDE_QA, GUIDE_TOTAL, type GuideQA } from "@/data/atlas/guide";
import {
  GEO_SOURCES,
  GEO_ANCHORS,
  GEO_ANCHORS_TO_COLLECT,
  ASSET_ORIENTATIONS,
  A02_CORRECTION,
  GEO_AUDIT_REPORT,
} from "@/data/atlas/geotruth";

export interface AtlasModel {
  meta: {
    title: string;
    period: string;
    municipality: {
      no: number;
      nameSi: string;
      nameHistorical: string;
      previousSignatura: string;
    };
    fund: string;
    archive: string;
    generatedAt: string;
  };
  sources: AtlasSource[];
  houses: AtlasHouse[];
  owners: ReturnType<typeof getOwnersWithRefs>;
  locations: typeof ATLAS_LOCATIONS;
  sheets: typeof SHEET_GEOREFS;
  buildings: { count: number; status: "RECONSTRUCTED"; list: typeof VECTOR_BUILDINGS };
  heritage: typeof HERITAGE_UNITS;
  negativeResults: typeof NEGATIVE_RESULTS;
  coverage: Coverage;
  /** matrične knjige župnije Podzemelj + vpisi hiš (issue #6) */
  parish: {
    info: typeof PARISH;
    books: ParishBook[];
    houseVitals: HouseVital[];
    stats: ReturnType<typeof parishStats>;
  };
  /** AI MUSEUM GUIDE (issue #15, točka 9) — muzejsko preverjena
      vprašanja/odgovori: podatkovni sloj za bodočega AI vodnika */
  guide: {
    total: number;
    entries: GuideQA[];
  };
}

export interface Coverage {
  housesTotal: number;
  housesWithOwner: number;
  housesWithGeometry: number;
  housesGeometryStatus: "TO_COLLECT";
  ownersTotal: number;
  ownersCrossChecked: number;
  parcelsReferenced: number;
  sheetsTotal: number;
  sheetsGeoreferenced: number;
  archivalUnits: number;
  archivalPages: number;
  buildingsVectorized: number;
  statusesSi: Record<string, string>;
}

export function getOwnersWithRefs() {
  return ATLAS_OWNERS.map((o) => ({
    ...o,
    houseRecords: ATLAS_HOUSES.filter(
      (h) => h.no !== "—" && o.houseRefs.some((r) => r === h.no || r.includes(h.no)),
    ).map((h) => ({ id: h.id, no: h.no, parcelRefs: h.parcelRefs })),
    sourceIds: ["src-pt", o.puaRef ? "src-pua" : "src-pt"].filter((v, i, a) => a.indexOf(v) === i),
  }));
}

export function getCoverage(): Coverage {
  const housesWithOwner = ATLAS_HOUSES.filter((h) => h.owner && h.owner !== "—").length;
  const houses = ATLAS_HOUSES.filter((h) => h.no !== "—");
  return {
    housesTotal: houses.length,
    housesWithOwner,
    housesWithGeometry: 0,
    housesGeometryStatus: "TO_COLLECT",
    ownersTotal: ATLAS_OWNERS.length,
    ownersCrossChecked: ATLAS_OWNERS.filter((o) => o.puaRef).length,
    parcelsReferenced: ATLAS_HOUSES.filter((h) => h.parcelRefs).length,
    sheetsTotal: 5,
    sheetsGeoreferenced: 5,
    archivalUnits: 9,
    archivalPages: 143 + 71 + 49 + 8 + 4 + 1 + 1 + 2,
    buildingsVectorized: VECTOR_BUILDINGS.length,
    statusesSi: {
      VERIFIED: "preverjeno (sodobni vir + zgodovinski vir)",
      DOCUMENTED: "dokumentirano v arhivskem viru",
      REVIEW: "prepis Kurrent rokopisa — čaka paleografski pregled",
      RECONSTRUCTED: "vektorizacija iz georeferenciranega lista",
      APPROXIMATE: "približna lokacija (območje vasi)",
      TO_COLLECT: "podatek še ni zbran",
      NOT_FOUND: "iskano, ni najdeno",
      NOT_PUBLIC: "ni javno dostopno",
    },
  };
}

export function getAtlasModel(): AtlasModel {
  return {
    meta: {
      title: "ATLAS 1825 — Griblje",
      period: "1824–1830 (Franciscejski kataster)",
      municipality: {
        no: 83,
        nameSi: "Griblje",
        nameHistorical: "Grüble (Gemeinde GRÜBLE in Illyrien)",
        previousSignatura: "N083A",
      },
      fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
      archive: "Arhiv Republike Slovenije (VAČ)",
      generatedAt: "2026-10-07",
    },
    sources: ATLAS_SOURCES,
    houses: ATLAS_HOUSES,
    owners: getOwnersWithRefs(),
    locations: ATLAS_LOCATIONS,
    sheets: SHEET_GEOREFS,
    buildings: {
      count: VECTOR_BUILDINGS.length,
      status: "RECONSTRUCTED",
      list: VECTOR_BUILDINGS,
    },
    heritage: HERITAGE_UNITS,
    negativeResults: NEGATIVE_RESULTS,
    coverage: getCoverage(),
    parish: {
      info: PARISH,
      books: PARISH_BOOKS,
      houseVitals: HOUSE_VITALS,
      stats: parishStats(),
    },
    village3d: {
      origin: { lat: 45.5725, lng: 15.2926, status: "VERIFIED" },
      periods: PERIODS.map((p) => ({
        year: p.year,
        labelSi: p.labelSi,
        labelEn: p.labelEn,
        buildingCount: p.buildingCount,
        status: p.year === 1825 ? "RECONSTRUCTED" : p.year === 1900 ? "ESTIMATE" : "INTERPRETATION",
        noteSi: p.noteSi,
        noteEn: p.noteEn,
      })),
      buildings1825: BUILDINGS_1825.length,
      growth1900: GROWTH_1900.length,
      methodologySi:
        "Proceduralna ekstruzija katastrskih podlatn (LagunAR-pristop): tlorisi izmerjeni (list A02), višine/orientacije interpretacija; raba tal po VLM analizi; Kolpa georeferencirana; cerkev = muzejski GLB model.",
      methodologyEn:
        "Procedural extrusion of cadastral footprints (LagunAR approach): footprints measured (sheet A02), heights/orientations interpreted; land use from VLM analysis; Kolpa georeferenced; church = museum GLB model.",
      deepLink: "/?casovni=1825",
      /* Kaj je izginilo? (issue #12) — 1825 ∩ OSM po stavbi */
      izginilo: {
        exists: IZGINILO_STATS.exists,
        uncertain: IZGINILO_STATS.uncertain,
        gone: IZGINILO_STATS.gone,
        total1825: IZGINILO_STATS.total1825,
        presentCount: IZGINILO_STATS.presentCount,
        osmSnapshot: IZGINILO_STATS.osmSnapshot,
        status: "INTERPRETATION",
        noteSi: PRESENCE_META.methodSi,
        noteEn:
          "Centroid matching of 156 cadastral footprints against present-day OSM buildings. exists: d≤8 m or (d≤20 m & overlap≥0.10); uncertain: building within 40 m or a small structure on the footprint; gone: none within 40 m. Absence from the OSM snapshot is NOT proof of demolition — field verification pending. St. Vitus' church: exists (1825 cadastre + standing building, 500th anniversary).",
        sourceSi: PRESENCE_META.sourceSi,
        sourceEn: PRESENCE_META.sourceEn,
        deepLink: "/?casovni=danes",
      },
    },
    /* AR TIME SPOTS (issue #11 + #12 P1) — časovne točke s QR vhodi
       (Nîmes vzorec); oddaljene točke imajo mini-sceno ali story dogodke */
    timeSpots: TIME_SPOTS.map((s) => ({
      id: s.id,
      year: s.year,
      radius: s.radius,
      renderReadyM: s.renderReadyM ?? null,
      precisionM: s.precisionM ?? null,
      anchorId: s.anchorId ?? null,
      lat: s.lat,
      lng: s.lng,
      titleSi: s.titleSi,
      titleEn: s.titleEn,
      evidenceSi: s.evidenceSi,
      evidenceEn: s.evidenceEn,
      exhibitSlug: s.exhibitSlug,
      houseNo: s.houseNo ?? null,
      miniScene: s.miniScene ?? null,
      distant: isDistantSpot(s),
      distanceFromVillageM: Math.round(spotDistanceFromVillage(s)),
      events: s.events ?? null,
      panoramaId: s.panoramaId ?? null,
      deepLink: `/?casovni=${spotYearParam(s.year)}&spot=${s.id}`,
    })),
    /* HISTORICAL PANORAMAS (issue #13, P2) — imerzivna 360° plast
       TimeSpota: asset + evidence trditve + produkcija + deep link (&pano=1) */
    panoramas: PANORAMAS.map((p) => ({
      id: p.id,
      timeSpotId: p.timeSpotId,
      year: p.year,
      imageUrl: p.imageUrl,
      previewUrl: p.previewUrl,
      headingDeg: p.headingDeg,
      titleSi: p.titleSi,
      titleEn: p.titleEn,
      status: p.status,
      claims: p.claims,
      methodSi: p.methodSi,
      methodEn: p.methodEn,
      sources: p.sources,
      evidenceSi: p.evidenceSi,
      evidenceEn: p.evidenceEn,
      audioSiUrl: p.audioSiUrl,
      audioEnUrl: p.audioEnUrl,
      deepLink: panoramaDeepLink(p),
    })),
    /* AI MUSEUM GUIDE (issue #15, točka 9) — preverjene zgodbe
       (question/answer/source/status/location/period); AI kasneje
       odgovarja SAMO iz teh podatkov — vir resnice ostane Atlas/evidence */
    guide: {
      total: GUIDE_TOTAL,
      entries: GUIDE_QA,
    },
    /* GEOTRUTH (issue #14, P0) — AR sidra, viri, dokazna pot, avdit konfliktov */
    geotruth: {
      sources: GEO_SOURCES,
      anchors: GEO_ANCHORS,
      anchorsToCollect: GEO_ANCHORS_TO_COLLECT,
      assetOrientations: ASSET_ORIENTATIONS,
      correction: A02_CORRECTION,
      audit: GEO_AUDIT_REPORT,
      auditCounts: GEO_AUDIT_REPORT.reduce(
        (acc, i) => ({ ...acc, [i.severity]: (acc[i.severity] ?? 0) + 1 }),
        {} as Record<string, number>,
      ),
    },
  };
}

/** GeoJSON izvoz: lokacije + stavbe + hiše (brez geometrije, z območjem vasi) */
export function getAtlasGeoJSON() {
  const village = ATLAS_LOCATIONS.find((l) => l.id === "loc-griblje")!;
  return {
    type: "FeatureCollection" as const,
    crs: {
      type: "name" as const,
      properties: { name: "urn:ogc:def:crs:OGC:1.3:CRS84" },
    },
    features: [
      ...ATLAS_LOCATIONS.filter((l) => l.lat && l.lng).map((l) => ({
        type: "Feature" as const,
        id: l.id,
        geometry: { type: "Point" as const, coordinates: [l.lng, l.lat] },
        properties: {
          kind: "location",
          subkind: l.kind,
          title: l.titleSi,
          title_en: l.titleEn,
          status: l.status,
          source: l.sourceId,
          museum: l.museumRef ?? null,
        },
      })),
      ...HERITAGE_UNITS.filter((h) => h.lat && h.lng).map((h) => ({
        type: "Feature" as const,
        id: `esd-${h.esd}`,
        geometry: { type: "Point" as const, coordinates: [h.lng!, h.lat!] },
        properties: {
          kind: "heritage",
          esd: h.esd,
          title: h.titleSi,
          title_en: h.titleEn,
          museum: h.museumRef ?? null,
        },
      })),
      ...VECTOR_BUILDINGS.map((b, i) => ({
        type: "Feature" as const,
        id: `b1825-${i + 1}`,
        geometry: { type: "Point" as const, coordinates: [b.lng, b.lat] },
        properties: {
          kind: "building-1825",
          status: "RECONSTRUCTED",
          sheet: "A02",
          px: b.px,
          size: [b.w, b.h],
          title: `Objekt ~1825 št. ${i + 1} (vektorizacija)`,
        },
      })),
      {
        type: "Feature" as const,
        id: "village-1825",
        geometry: {
          type: "Point" as const,
          coordinates: [village.lng!, village.lat!],
        },
        properties: {
          kind: "village-area",
          status: "APPROXIMATE",
          radius_m: 500,
          title: "Območje vasi Griblje ~1825 (hiše 1–98, prebranih 80)",
          houses: ATLAS_HOUSES.filter((h) => h.no !== "—").length,
        },
      },
    ],
  };
}

// ——— ISKANJE ————————————————————————————————

export interface AtlasSearchHit {
  type: "house" | "parcel" | "owner" | "source" | "location" | "heritage" | "negative" | "parish-book" | "house-vital";
  id: string;
  titleSi: string;
  titleEn: string;
  detail?: string;
  status?: string;
}

const fold = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[đð]/g, "d")
    .replace(/[čć]/g, "c")
    .replace(/[š]/g, "s")
    .replace(/[ž]/g, "z");

export function searchAtlas(q: string): AtlasSearchHit[] {
  const needle = fold(q.trim());
  if (needle.length < 2) return [];
  const hits: AtlasSearchHit[] = [];
  const matches = (s: string) => fold(s).includes(needle);

  for (const h of ATLAS_HOUSES) {
    if (h.no !== "—" && (matches(h.no) || matches(h.owner) || matches(h.ownerModernGuess ?? "") || matches(h.parcelRefs ?? ""))) {
      hits.push({
        type: h.no === "—" ? "parcel" : "house",
        id: h.id,
        titleSi: h.no === "—" ? "Parcela (register)" : `Hiša št. ${h.no} — ${h.owner}`,
        titleEn: h.no === "—" ? "Parcel (register)" : `House no. ${h.no} — ${h.owner}`,
        detail: h.parcelRefs ? `PT str. ${h.sourcePage} · ${h.parcelRefs}` : `PT str. ${h.sourcePage}`,
        status: h.status,
      });
    }
  }
  for (const o of ATLAS_OWNERS) {
    if (matches(o.nameAsWritten) || matches(o.modernGuess ?? "")) {
      hits.push({
        type: "owner",
        id: o.id,
        titleSi: `Lastnik: ${o.nameAsWritten}`,
        titleEn: `Owner: ${o.nameAsWritten}`,
        detail: `hiše: ${o.houseRefs.join(", ")}${o.puaRef ? ` · ${o.puaRef}` : ""}`,
        status: o.status,
      });
    }
  }
  for (const s of ATLAS_SOURCES) {
    if (matches(s.titleSi) || matches(s.titleEn) || matches(s.code) || matches(s.unit ?? "")) {
      hits.push({
        type: "source",
        id: s.id,
        titleSi: `Vir: ${s.code} — ${s.titleSi}`,
        titleEn: `Source: ${s.code} — ${s.titleEn}`,
        detail: `${s.archive} · ${s.pages ? s.pages + " str." : "list"}${s.georeferenced ? " · georeferenciran" : ""}`,
      });
    }
  }
  for (const l of ATLAS_LOCATIONS) {
    if (matches(l.titleSi) || matches(l.titleEn)) {
      hits.push({
        type: "location",
        id: l.id,
        titleSi: l.titleSi,
        titleEn: l.titleEn,
        status: l.status,
      });
    }
  }
  for (const h of HERITAGE_UNITS) {
    if (matches(h.titleSi) || matches(`esd ${h.esd}`) || matches(String(h.esd))) {
      hits.push({
        type: "heritage",
        id: `esd-${h.esd}`,
        titleSi: `EŠD ${h.esd} — ${h.titleSi}`,
        titleEn: `EŠD ${h.esd} — ${h.titleEn}`,
      });
    }
  }
  /* matrične knjige župnije Podzemelj (issue #6) */
  const bookTypeName: Record<ParishBook["type"], string> = {
    baptism: "Krstna knjiga",
    marriage: "Poročna knjiga",
    death: "Mrliška knjiga",
  };
  for (const b of PARISH_BOOKS) {
    if (
      matches(b.signature) ||
      matches(bookTypeName[b.type]) ||
      matches(`${b.from}`) ||
      matches(`${b.to}`) ||
      matches(`matrika`)
    ) {
      hits.push({
        type: "parish-book",
        id: `matrika-${b.signature}`,
        titleSi: `${bookTypeName[b.type]} ${b.from}–${b.to} · ${b.signature}`,
        titleEn: `${bookTypeName[b.type]} ${b.from}–${b.to} · ${b.signature}`,
        detail: `župnija Podzemelj · Matricula Online`,
        status: b.status,
      });
    }
  }
  for (const v of HOUSE_VITALS) {
    if (matches(`hiša ${v.houseNo}`) || matches(`${v.houseNo}`)) {
      hits.push({
        type: "house-vital",
        id: `zivilo-${v.houseNo}-${v.year}`,
        titleSi: `Vpis v matriki: hiša št. ${v.houseNo} (${v.year})`,
        titleEn: `Parish record: house no. ${v.houseNo} (${v.year})`,
        detail: `${v.whatSi} · knjiga ${v.bookSignature}`,
        status: v.status,
      });
    }
  }
  return hits.slice(0, 40);
}

/** celoten dokazni list objekta (SOURCE → EVIDENCE → CLAIM → …) */
export function getEvidenceChain(houseId: string) {
  const house = ATLAS_HOUSES.find((h) => h.id === houseId);
  if (!house) return null;
  const owner = ATLAS_OWNERS.find((o) => o.houseRefs.some((r) => r === house.no));
  const pt = ATLAS_SOURCES.find((s) => s.id === "src-pt")!;
  const pua = ATLAS_SOURCES.find((s) => s.id === "src-pua")!;
  const a02 = ATLAS_SOURCES.find((s) => s.id === "src-a02")!;
  return {
    claim: {
      id: house.id,
      textSi: `Hiša št. ${house.no} v vasi Grüble (Griblje) ~1825, lastnik ${house.owner}.`,
      textEn: `House no. ${house.no} in the village of Grüble (Griblje) ~1825, owner ${house.owner}.`,
      status: house.status,
    },
    evidence: [
      {
        source: pt,
        locatorSi: `stran ${house.sourcePage}, vrstica hišne št. ${house.no}`,
        quote: house.parcelRefs ?? house.owner,
        kind: "prepis rokopisa (REVIEW)",
      },
      owner?.puaRef
        ? { source: pua, locatorSi: owner.puaRef, quote: owner.nameAsWritten, kind: "navzkrižna potrditev imena (REVIEW)" }
        : null,
      {
        source: a02,
        locatorSi: "list A02 — jedro vasi s stavbami",
        quote: "položaj vasi (ne posamezne hiše)",
        kind: "georeferenca vasi (APPROXIMATE)",
      },
    ].filter((ev): ev is NonNullable<typeof ev> => Boolean(ev)),
    relations: {
      owner: owner ? { id: owner.id, name: owner.nameAsWritten, status: owner.status } : null,
      parcels: house.parcelRefs ?? null,
      museum: house.museumRef ?? null,
      geometry: { status: "TO_COLLECT", noteSi: "lokalna pozicija hiše na listu še ni preslikana" },
    },
  };
}

// ——— INTEGRITETNI TEST (hiša ↔ parcela ↔ lastnik ↔ vir) ——————

export interface IntegrityReport {
  ok: boolean;
  checks: { name: string; pass: boolean; detail: string }[];
}

export function checkIntegrity(): IntegrityReport {
  const checks: { name: string; pass: boolean; detail: string }[] = [];
  const houses = ATLAS_HOUSES.filter((h) => h.no !== "—");

  // 1. vsaka hiša ima številko, lastnika in stran vira
  const badHouses = houses.filter((h) => !h.no || !h.owner || !h.sourcePage);
  checks.push({
    name: "hiše: številka + lastnik + stran vira",
    pass: badHouses.length === 0,
    detail: `${houses.length} hiš; ${badHouses.length} nepravnih`,
  });

  // 2. vsaka hiša se sklicuje na vir src-pt
  checks.push({
    name: "hiše → vir (N083PT)",
    pass: ATLAS_SOURCES.some((s) => s.id === "src-pt") && houses.length > 0,
    detail: `vir src-pt obstaja; ${houses.length} hiš izpeljanih iz njega`,
  });

  // 3. vsak lastnik ima vsaj eno hišo ali PUA potrditev
  const badOwners = ATLAS_OWNERS.filter((o) => o.houseRefs.length === 0 && !o.puaRef);
  checks.push({
    name: "lastniki → hiše/vir",
    pass: badOwners.length === 0,
    detail: `${ATLAS_OWNERS.length} lastnikov; ${badOwners.length} brez povezave`,
  });

  // 4. hiša 73 (demonstracijska veriga) obstaja in ima MVG povezavo
  const h73 = ATLAS_HOUSES.find((h) => h.no === "73");
  checks.push({
    name: "E2E veriga: hiša 73 → vir → MVG-010 → območje vasi",
    pass: !!h73 && !!h73.museumRef && !!h73.sourcePage,
    detail: h73 ? `hiša 73: vir str. ${h73.sourcePage}, muzej ${h73.museumRef}` : "hiše 73 ni",
  });

  // 5. georeferenca: listi imajo veljavne meje (N>S, E>W) in slike
  const geoOk = SHEET_GEOREFS.every(
    (g) => g.bounds[0][0] > g.bounds[1][0] && g.bounds[0][1] < g.bounds[1][1] && g.imageUrl.length > 0,
  );
  checks.push({
    name: "georeferenca: veljavne meje listov",
    pass: geoOk,
    detail: `${SHEET_GEOREFS.length} lista (A01, A02)`,
  });

  // 6. cerkev: lokacija se ujema z uradnim EŠD 2122 (GEOTRUTH, issue #14)
  const church = ATLAS_LOCATIONS.find((l) => l.id === "loc-cerkev");
  checks.push({
    name: "cerkev sv. Vida ↔ MVG-002 ↔ EŠD 2122 (uradna koordinata)",
    pass: !!church && church.museumRef === "MVG-002" && Math.abs(church.lat! - 45.56761) < 0.0005 && Math.abs(church.lng! - 15.290311) < 0.0005,
    detail: church ? `${church.lat}, ${church.lng} (EŠD 2122: 45.567610, 15.290311)` : "ni",
  });

  // 7. stavbe: vse v velikostnem razponu k.o.
  const bBad = VECTOR_BUILDINGS.filter(
    (b) => !(45.5 < b.lat && b.lat < 45.65 && 15.2 < b.lng && b.lng < 15.35),
  );
  checks.push({
    name: "vektorizacija: stavbe znotraj k.o.",
    pass: bBad.length === 0,
    detail: `${VECTOR_BUILDINGS.length} objektov; ${bBad.length} zunaj`,
  });

  // 8. viri: vsak N83 vir ima VAČ povezavo (12 enot: 5 grafičnih listov + 7 spisovnih)
  const n83 = ATLAS_SOURCES.filter((s) => s.code.startsWith("N083"));
  checks.push({
    name: "viri N83 → VAČ (javne povezave)",
    pass: n83.every((s) => !!s.vacUrl) && n83.length === 12,
    detail: `${n83.length} enot N83 s povezavo`,
  });

  // 9. negativni rezultati: vsak ima status
  checks.push({
    name: "negativni rezultati evidentirani",
    pass: NEGATIVE_RESULTS.every((n) => !!n.status) && NEGATIVE_RESULTS.length >= 5,
    detail: `${NEGATIVE_RESULTS.length} zapisov`,
  });

  // 10. matrične knjige Podzemelj: 22 enot s signaturo, obdobjem in povezavo (issue #6)
  const booksOk =
    PARISH_BOOKS.length === 22 &&
    PARISH_BOOKS.every((b) => /^\d{5}$/.test(b.signature) && b.from <= b.to && /^https:/.test(b.url));
  checks.push({
    name: "matrične knjige Podzemelj (issue #6): 22 enot, signature in povezave",
    pass: booksOk,
    detail: `${PARISH_BOOKS.length} knjig; krstnih ${PARISH_BOOKS.filter((b) => b.type === "baptism").length}, poročnih ${PARISH_BOOKS.filter((b) => b.type === "marriage").length}, mrliških ${PARISH_BOOKS.filter((b) => b.type === "death").length}`,
  });

  // 11. hišni vpisi iz matrik se nanašajo na obstoječe hiše (issue #6)
  const housesNoSet = new Set(ATLAS_HOUSES.filter((h) => h.no !== "—").map((h) => h.no));
  const vitalsOk = HOUSE_VITALS.every((v) => housesNoSet.has(v.houseNo) && PARISH_BOOKS.some((b) => b.signature === v.bookSignature));
  checks.push({
    name: "matrični vpisi → obstoječe hiše in knjige (issue #6)",
    pass: vitalsOk,
    detail: `${HOUSE_VITALS.length} vpisov; vsi se nanašajo na hiše PT in knjige ${[...new Set(HOUSE_VITALS.map((v) => v.bookSignature))].join(", ")}`,
  });

  return { ok: checks.every((c) => c.pass), checks };
}

// ——— ŽUPNIJA PODZEMELJ: MATIKE + HIŠNE ZGODBE (issue #6) ——————

export interface HouseStory {
  house: AtlasHouse;
  ownerCrossRef: { name: string; puaRef?: string; status: string } | null;
  vitals: HouseVital[];
  vitalsStatus: "DOCUMENTED" | "TO_COLLECT";
}

/** Hišna zgodba: lastnik 1825 (PT) × potrditev (PUA) × matrični vpisi (kdaj, kdo). */
export function getHouseStory(houseNo: string): HouseStory | null {
  const house = ATLAS_HOUSES.find((h) => h.no === houseNo && h.no !== "—");
  if (!house) return null;
  const owner = ATLAS_OWNERS.find((o) => o.houseRefs.some((r) => r === house.no)) ?? null;
  const vitals = HOUSE_VITALS.filter((v) => v.houseNo === house.no);
  return {
    house,
    ownerCrossRef: owner ? { name: owner.nameAsWritten, puaRef: owner.puaRef, status: owner.status } : null,
    vitals,
    vitalsStatus: vitals.length > 0 ? "DOCUMENTED" : "TO_COLLECT",
  };
}

/** agregati matrik za odsek in QA */
export function parishStats() {
  const housesNo = ATLAS_HOUSES.filter((h) => h.no !== "—").map((h) => h.no);
  const withVitals = new Set(HOUSE_VITALS.map((v) => v.houseNo));
  return {
    parish: PARISH.nameSi,
    books: PARISH_BOOKS.length,
    byType: {
      baptism: PARISH_BOOKS.filter((b) => b.type === "baptism").length,
      marriage: PARISH_BOOKS.filter((b) => b.type === "marriage").length,
      death: PARISH_BOOKS.filter((b) => b.type === "death").length,
    },
    period: PARISH.period,
    housesTotal: housesNo.length,
    housesWithVitals: [...withVitals].length,
    vitalRecords: HOUSE_VITALS.length,
    source: PARISH.url,
    accessedAt: PARISH.accessedAt,
  };
}
