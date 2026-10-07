import { NextResponse } from "next/server";
import { computeProvenanceAudit, countFlaggedRecords, DATA_VERSION } from "@/lib/provenance";
import { ATLAS_SOURCES, NEGATIVE_RESULTS, HERITAGE_UNITS } from "@/data/atlas/sources";
import {
  KURRENT_SERIES,
  GEODATA_SOURCES,
  SCHOOL_ARCHIVE,
  GASPARI_RESEARCH,
  F0000212_PROVENANCE,
  MAP_1812,
  ORAL_INTERVIEWS,
  ORAL_TOPICS,
} from "@/data/atlas/research";

export const dynamic = "force-static";

/**
 * ISSUE #3 — avtomatski provenienčni in raziskovalni poročili (strojno berljivo).
 * /api/provenance:
 *  - audit 113 zapisov zbirke (viri, licence, lokacije, evidenceStatus, zastavice)
 *  - raziskovalni model: stanje prepisov Kurrent, geodetski viri, šolski arhiv,
 *    Gaspari, F0000212, zemljevid 1812, ustna zgodovina
 *  - katalog 12 enot N83 s statusi prenosa/georeference
 */
export async function GET() {
  const audit = computeProvenanceAudit();

  return NextResponse.json(
    {
      dataVersion: DATA_VERSION,
      audit,
      auditSummary: {
        totalRecords: audit.totalRecords,
        flaggedRecords: countFlaggedRecords(audit),
        withAtLeastOneSource: audit.sources.withAtLeastOneSource,
        withDirectSource: audit.sources.withDirectSource,
        withGps: audit.locations.withGps,
      },
      n83Catalog: ATLAS_SOURCES.filter((s) => s.code.startsWith("N083")).map((s) => ({
        id: s.id,
        code: s.code,
        type: s.type,
        title: { sl: s.titleSi, en: s.titleEn },
        unit: s.unit ?? null,
        vacId: s.vacId ?? null,
        vacUrl: s.vacUrl ?? null,
        pages: s.pages ?? null,
        transferStatus: s.transferStatus ?? null,
        georefStatus: s.georefStatus ?? null,
        structuredEntries: s.structuredEntries ?? 0,
        lastVerified: s.lastVerified ?? null,
      })),
      research: {
        kurrentSeries: KURRENT_SERIES,
        geodataSources: GEODATA_SOURCES,
        schoolArchive: SCHOOL_ARCHIVE,
        gaspari: GASPARI_RESEARCH,
        f0000212: F0000212_PROVENANCE,
        map1812: MAP_1812,
        oralHistory: {
          interviews: ORAL_INTERVIEWS,
          topics: ORAL_TOPICS,
          modelSi:
            "Model intervjuja: pripovedovalec, datum, lokacija, intervjuvar, soglasje, avdio/video, prepis z različico, povezani zapisi, pravice uporabe. Nič vsebine ni izmišljeno — prazen seznam čaka prve posnete intervjuje.",
          modelEn:
            "Interview model: narrator, date, location, interviewer, consent, audio/video, transcript with version, related records, usage rights. No content is invented — the empty list awaits the first recorded interviews.",
        },
        negativeResults: NEGATIVE_RESULTS,
        heritageUnits: HERITAGE_UNITS,
      },
    },
    {
      headers: {
        "Cache-Control": "public, max-age=3600",
        "Access-Control-Allow-Origin": "*",
      },
    },
  );
}
