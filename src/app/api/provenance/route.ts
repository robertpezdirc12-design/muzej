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
  ARCHIVE_TRANSFER_ROWS,
  ARCHIVE_NON_TRANSFERS,
  ARCHIVE_TRANSFER_AUDIT,
  PV_LAND_USE_1825,
  PR_BOUNDARY_1825,
  PS_RECAP_1826,
  PZ_ECONOMY_1825,
  PUA_CONTINUATION,
  PUA_PT_CROSS,
  PUA_PT_WBRIDGE,
  PT_REVIEW_2026,
  PT_PALEOGRAPHY_P3,
  ORAL_HISTORY_PROTOCOL,
  WEB_VERIFICATIONS,
  ISSUE17_MATRIX,
  ISSUE17_AUDIT,
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
        archiveTransfer: {
          audit: ARCHIVE_TRANSFER_AUDIT,
          rows: ARCHIVE_TRANSFER_ROWS,
          nonTransfers: ARCHIVE_NON_TRANSFERS,
        },
        p3: {
          ptPalaeographyP3: PT_PALEOGRAPHY_P3,
        },
        p5: {
          puaPtCross: PUA_PT_CROSS,
          puaPtWbridge: PUA_PT_WBRIDGE,
        },
        issue17: {
          audit: ISSUE17_AUDIT,
          matrix: ISSUE17_MATRIX,
          pvLandUse1825: PV_LAND_USE_1825,
          prBoundary1825: PR_BOUNDARY_1825,
          psRecap1826: PS_RECAP_1826,
          pzEconomy1825: PZ_ECONOMY_1825,
          puaContinuation: PUA_CONTINUATION,
          ptReview2026: PT_REVIEW_2026,
          oralHistoryProtocol: ORAL_HISTORY_PROTOCOL,
          webVerifications: WEB_VERIFICATIONS,
        },
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
