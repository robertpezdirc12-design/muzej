// ISSUE #3 #12 — avtomatski provenience audit vseh 113 zapisov zbirke.
// Poročilo se IZRAČUNA iz podatkov (exhibits.json + sources v njem) —
// nobena številka ni ročno vpisana.

import exhibitsRaw from "@/data/museum/exhibits.json";
import { ATLAS_SOURCES, NEGATIVE_RESULTS, HERITAGE_UNITS } from "@/data/atlas/sources";
import { KURRENT_SERIES, GEODATA_SOURCES, SCHOOL_ARCHIVE, ORAL_INTERVIEWS, ORAL_TOPICS } from "@/data/atlas/research";

/** ISSUE #16 — revizija prenosa iz arhiva (0 prenosov, nadnabor) je
    vstopila v raziskovalni model; različica podatkov ostaja enaka, ker se
    vsebinski podatki niso spremenili (dodana je le revizija sama). */
export const DATA_VERSION = "2026-10-07";

interface ExhibitSource {
  sourceType?: string | null;
  license?: string | null;
  url?: string | null;
  nameSi?: string | null;
  nameEn?: string | null;
  creator?: string | null;
}

interface Exhibit {
  id: string;
  slug: string;
  museumNo: string;
  category: string;
  titleSi: string;
  evidenceStatus?: string | null;
  image?: string | null;
  imageCredit?: string | null;
  lat?: number | null;
  lng?: number | null;
  sources?: ExhibitSource[] | null;
}

const EXHIBITS = (exhibitsRaw as { exhibits: Exhibit[] }).exhibits;

const hasDirectSource = (s: ExhibitSource) => Boolean(s.url && s.url.startsWith("http"));
const hasLicense = (s: ExhibitSource) => Boolean(s.license && s.license.trim().length > 0);

export interface ProvenanceFlag {
  museumNo: string;
  slug: string;
  flag:
    | "no_sources"
    | "no_direct_source"
    | "missing_license"
    | "null_source_url"
    | "null_source_name"
    | "no_location"
    | "no_image_credit"
    | "unclear_evidence";
  detailSi: string;
  detailEn: string;
}

export interface ProvenanceAudit {
  totalRecords: number;
  sources: {
    withAtLeastOneSource: number;
    withoutAnySource: number;
    withDirectSource: number;
    onlySecondarySource: number;
    nullSourceUrl: number;
    nullSourceName: number;
    missingLicense: number;
    licenseDistribution: Record<string, number>;
    sourceTypeDistribution: Record<string, number>;
    totalSourceRows: number;
  };
  images: {
    withImage: number;
    withoutImage: number;
    withImageCredit: number;
    withoutImageCredit: number;
  };
  locations: {
    withGps: number;
    withoutGps: number;
  };
  evidence: {
    distribution: Record<string, number>;
    /** statusi iz evidenceScale, ki jih podatki dejansko uporabljajo */
    unknownStatuses: string[];
  };
  flags: ProvenanceFlag[];
  atlas: {
    n83Units: number;
    n83UnitsTransferred: number;
    n83UnitsGeoreferenced: number;
    externalSources: number;
    negativeResults: number;
    heritageUnits: number;
    kurrentPages: number;
    kurrentPagesTranscribed: number;
    kurrentStructuredEntries: number;
    geodataSources: number;
    schoolArchiveUnits: number;
    oralInterviews: number;
    oralTopics: number;
  };
  computedAt: string;
  dataVersion: string;
}

export function computeProvenanceAudit(): ProvenanceAudit {
  const flags: ProvenanceFlag[] = [];

  let withAtLeastOneSource = 0;
  let withDirectSource = 0;
  let onlySecondarySource = 0;
  let nullSourceUrl = 0;
  let nullSourceName = 0;
  let missingLicense = 0;
  let totalSourceRows = 0;
  const licenseDistribution: Record<string, number> = {};
  const sourceTypeDistribution: Record<string, number> = {};

  let withImage = 0;
  let withImageCredit = 0;
  let withGps = 0;
  const evidenceDistribution: Record<string, number> = {};

  for (const e of EXHIBITS) {
    const srcs = e.sources ?? [];
    totalSourceRows += srcs.length;

    if (srcs.length === 0) {
      flags.push({
        museumNo: e.museumNo,
        slug: e.slug,
        flag: "no_sources",
        detailSi: "zapis nima nobenega vira",
        detailEn: "record has no source at all",
      });
    } else {
      withAtLeastOneSource++;
    }

    const direct = srcs.filter(hasDirectSource);
    if (srcs.length > 0 && direct.length > 0) withDirectSource++;
    if (srcs.length > 0 && direct.length === 0) {
      onlySecondarySource++;
      flags.push({
        museumNo: e.museumNo,
        slug: e.slug,
        flag: "no_direct_source",
        detailSi: `noben od ${srcs.length} virov nima neposredne povezave`,
        detailEn: `none of the ${srcs.length} sources carries a direct URL`,
      });
    }

    for (const s of srcs) {
      if (!s.url || !s.url.startsWith("http")) nullSourceUrl++;
      if (!s.nameSi && !s.nameEn) nullSourceName++;
      if (!hasLicense(s)) missingLicense++;
      const lic = (s.license ?? "(brez licence)").trim() || "(brez licence)";
      licenseDistribution[lic] = (licenseDistribution[lic] ?? 0) + 1;
      const st = s.sourceType ?? "(neznana vrsta)";
      sourceTypeDistribution[st] = (sourceTypeDistribution[st] ?? 0) + 1;
    }
    if (srcs.length > 0 && srcs.every((s) => !hasLicense(s))) {
      flags.push({
        museumNo: e.museumNo,
        slug: e.slug,
        flag: "missing_license",
        detailSi: "noben vir zapisa nima podatka o licenci",
        detailEn: "no source of the record carries license data",
      });
    }
    if (srcs.some((s) => !s.url || !s.url.startsWith("http"))) {
      flags.push({
        museumNo: e.museumNo,
        slug: e.slug,
        flag: "null_source_url",
        detailSi: "vsaj eden od virov nima URL",
        detailEn: "at least one source lacks a URL",
      });
    }

    if (e.image) withImage++;
    if (e.image && !e.imageCredit) {
      flags.push({
        museumNo: e.museumNo,
        slug: e.slug,
        flag: "no_image_credit",
        detailSi: "slika brez navedbe avtorja/pravic",
        detailEn: "image without author/rights credit",
      });
    }
    if (e.image && e.imageCredit) withImageCredit++;

    if (e.lat && e.lng) withGps++;
    else
      flags.push({
        museumNo: e.museumNo,
        slug: e.slug,
        flag: "no_location",
        detailSi: "brez GPS lokacije",
        detailEn: "no GPS location",
      });

    const st = e.evidenceStatus ?? "(neznan)";
    evidenceDistribution[st] = (evidenceDistribution[st] ?? 0) + 1;
  }

  const knownStatuses = new Set(["DOCUMENTED", "CORROBORATED", "TRADITION", "TESTIMONY"]);
  const unknownStatuses = Object.keys(evidenceDistribution).filter((k) => !knownStatuses.has(k));

  const n83 = ATLAS_SOURCES.filter((s) => s.code.startsWith("N083"));

  return {
    totalRecords: EXHIBITS.length,
    sources: {
      withAtLeastOneSource,
      withoutAnySource: EXHIBITS.length - withAtLeastOneSource,
      withDirectSource,
      onlySecondarySource,
      nullSourceUrl,
      nullSourceName,
      missingLicense,
      licenseDistribution,
      sourceTypeDistribution,
      totalSourceRows,
    },
    images: {
      withImage,
      withoutImage: EXHIBITS.length - withImage,
      withImageCredit,
      withoutImageCredit: withImage - withImageCredit,
    },
    locations: {
      withGps,
      withoutGps: EXHIBITS.length - withGps,
    },
    evidence: {
      distribution: evidenceDistribution,
      unknownStatuses,
    },
    flags,
    atlas: {
      n83Units: n83.length,
      n83UnitsTransferred: n83.filter((s) => s.transferStatus === "TRANSFERRED").length,
      n83UnitsGeoreferenced: n83.filter((s) => s.georefStatus === "GEOREFERENCED").length,
      externalSources: ATLAS_SOURCES.length - n83.length,
      negativeResults: NEGATIVE_RESULTS.length,
      heritageUnits: HERITAGE_UNITS.length,
      kurrentPages: KURRENT_SERIES.reduce((a, s) => a + s.pages, 0),
      kurrentPagesTranscribed: KURRENT_SERIES.reduce((a, s) => a + s.pagesTranscribed, 0),
      kurrentStructuredEntries: KURRENT_SERIES.reduce((a, s) => a + s.structuredEntries, 0),
      geodataSources: GEODATA_SOURCES.length,
      schoolArchiveUnits: SCHOOL_ARCHIVE.units.length,
      oralInterviews: ORAL_INTERVIEWS.length,
      oralTopics: ORAL_TOPICS.length,
    },
    computedAt: new Date().toISOString(),
    dataVersion: DATA_VERSION,
  };
}

/** število zapisov z vsaj eno pomanjkljivostjo (za UI povzetek) */
export function countFlaggedRecords(audit: ProvenanceAudit): number {
  return new Set(audit.flags.map((f) => f.museumNo)).size;
}
