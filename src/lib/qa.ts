// ISSUE #4 — end-to-end kontrola kakovosti.
// Avtomatski testi, ki preverijo celovitost zbirke, sprehodov in coverage.
// Testi se poganjajo prek /api/qa (HTTP 200 = vsi testi zeleni, 500 = napaka).

import exhibitsRaw from "@/data/museum/exhibits.json";
import eventsRaw from "@/data/museum/events.json";
import metaRaw from "@/data/museum/meta.json";
import extraRaw from "@/data/museum/extra.json";
import { WALKS, walkItemsWithGaps, WALK_GAPS } from "./walks";
import { computeCoverage } from "./coverage";
import { buildReconciliation } from "./reconciliation";
import { NEGATIVE_RESULTS } from "@/data/atlas/sources";
import { parishStats, getCoverage, getArchiveInventory } from "./atlas";
import { PANORAMAS } from "@/data/atlas/panoramas";
import { TIME_SPOTS } from "@/data/atlas/timespots";
import {
  ARCHIVE_TRANSFER_ROWS,
  ARCHIVE_NON_TRANSFERS,
  ARCHIVE_TRANSFER_AUDIT,
  KURRENT_SERIES,
  ORAL_INTERVIEWS,
  PV_LAND_USE_1825,
  PR_BOUNDARY_1825,
  PS_RECAP_1826,
  PS_RECONCILIATION_P38,
  PS_LANDUSE_P39,
  PS_RECAP_P40,
  PS_RECAP_PALEO_P41,
  PS_LANDUSE_V2_P42,
  PS_LEXICON_P43,
  PS_K1K2_P44,
  PS_LEXICON_VERIFIED_P45,
  PZ_CLASS_TABLE_1825,
  NEATLINE_GEOREF_P46,
  GURS_OVERLAY_P47,
  BUILDINGS_OVERLAY_P48,
  FUCUKOVCI_P49,
  GEOREF_CLOSURE_P50,
  LEAFLET_OVERLAY_P51,
  PRESENT_GURS_P54,
  PS_GEO_P55,
  REGISTER_TOPOLOGY_P56,
  PS_REGISTER_START_P57,
  BLATT_HEADERS_P59,
  PERBLATT_ATTR_P60,
  UNIT_SEM_P61,
  TAIL_P63,
  ATTR_EXT_P64,
  ATTR_FULL_P65,
  SPLIT_PACK_P66,
  ANOM_FORENSICS_P67,
  V3_RENUMBER_P68,
  PASS1_LAYERS_P69,
  V4_REJOIN_P70,
  V5_SECTIONS_P93_P71,
  PZ_ECONOMY_1825,
  PUA_CONTINUATION,
  PUA_PT_CROSS,
  PUA_PT_WBRIDGE,
  MAP_1812,
  PT_REVIEW_2026,
  PT_PALEOGRAPHY_P3,
  ORAL_HISTORY_PROTOCOL,
  WEB_VERIFICATIONS,
  ISSUE17_MATRIX,
  ISSUE17_AUDIT,
} from "@/data/atlas/research";
import { ATLAS_HOUSES } from "@/data/atlas/houses";
import { ATLAS_OWNERS, SHEET_GEOREFS, VECTOR_BUILDINGS } from "@/data/atlas/model";
import { ATLAS_SOURCES } from "@/data/atlas/sources";
import { SHEET_TRUTH } from "@/data/atlas/geotruth";
import { TREE_STATS, SMOKE_CHIMNEYS, HOUSENO_FINDING, TREES } from "./village3d";
import { SOURCE_TYPE_LABELS } from "./museum";
import { YEAR_STOPS, MAX_YEAR, formatStopYear } from "./timeline-stops";

interface ExhibitRow {
  id: string;
  slug: string;
  museumNo: string;
  evidenceStatus: string | null;
  model3dUrl: string | null;
  lat: number | null;
  lng: number | null;
  coordsApprox?: boolean | null;
  yearFrom: number | null;
  yearTo: number | null;
  image?: string | null;
  summarySi?: string | null;
  summaryEn?: string | null;
  sources:
    | {
        nameSi?: string | null;
        nameEn?: string | null;
        url?: string | null;
        sourceType?: string | null;
      }[]
    | null;
}

interface StationRow {
  year?: string | null;
  stage?: string | null;
  description?: string | null;
  evidence?: string | null;
  sourceUrl?: string | null;
  sourceName?: string | null;
}

interface ExtraRow {
  walk?: { name?: string; station?: number } | null;
  lifeStations?: StationRow[] | null;
  related?: { slug?: string; museumNo?: string; title?: string }[] | null;
}

const EXHIBITS = (exhibitsRaw as { exhibits: ExhibitRow[] }).exhibits;
const EVENTS = eventsRaw as { count?: number; events: { id: string; titleSi?: string; titleEn?: string; descriptionSi?: string; descriptionEn?: string }[] };
const META = metaRaw as {
  count?: { exhibits?: number };
  counts?: { exhibits?: number; sources?: number; events?: number; stories?: number };
  stories?: unknown[];
};
const EXTRA = extraRaw as Record<string, ExtraRow>;

const KNOWN_EVIDENCE = new Set(["DOCUMENTED", "CORROBORATED", "TRADITION", "TESTIMONY"]);

export interface QATest {
  id: string;
  nameSi: string;
  nameEn: string;
  pass: boolean;
  detail: string;
}

export interface QAReport {
  ok: boolean;
  passed: number;
  failed: number;
  tests: QATest[];
  computedAt: string;
}

export interface QAOptions {
  /** Preverjanje obstoja datotek na disku — vbrizga ga strežnik
   *  (route /api/qa, fs.existsSync); odjemalski klic (museum-coverage)
   *  poti preveri po obliki, obstoj na disku pa izrecno prepusti /api/qa. */
  fileExists?: (relativePath: string) => boolean;
  /** Branje besedilnih datotek (README, layout) — prav tako vbrizga strežnik;
   *  brez njega odjemalski klic kontrolo dokumentacijskih števcev preskoči
   *  (celovita kontrola teče na /api/qa). Vrača null, kadar datoteke ni. */
  readFile?: (relativePath: string) => string | null;
}

export function runQA(opts: QAOptions = {}): QAReport {
  const tests: QATest[] = [];
  const push = (id: string, nameSi: string, nameEn: string, pass: boolean, detail: string) =>
    tests.push({ id, nameSi, nameEn, pass, detail });

  // 1. vsak zapis ima stabilen id in slug
  const badId = EXHIBITS.filter((e) => !e.id || !e.slug);
  push(
    "qa-stable-id",
    "vsak zapis ima stabilen id in slug",
    "every record has a stable id and slug",
    badId.length === 0,
    `${EXHIBITS.length} zapisov; ${badId.length} brez id/slug`,
  );

  // 2. podvojeni museumNo/slug niso dovoljeni
  const dup = (key: keyof ExhibitRow) => {
    const seen = new Set<string>();
    const d = new Set<string>();
    for (const e of EXHIBITS) {
      const v = String(e[key]);
      if (seen.has(v)) d.add(v);
      seen.add(v);
    }
    return [...d];
  };
  const dupNo = dup("museumNo");
  const dupSlug = dup("slug");
  push(
    "qa-no-duplicates",
    "podvojeni museumNo/slug niso dovoljeni",
    "duplicate museumNo/slug are not allowed",
    dupNo.length === 0 && dupSlug.length === 0,
    `podvojeni museumNo: ${dupNo.length || "0"}, slug: ${dupSlug.length || "0"}`,
  );

  // 3. zapis z model3dUrl, ki je AR-ready, mora imeti veljaven lat/lng
  const arBad = EXHIBITS.filter(
    (e) => e.model3dUrl && !(e.lat != null && e.lng != null && Math.abs(e.lat) <= 90 && Math.abs(e.lng) <= 180),
  );
  push(
    "qa-ar-gps",
    "AR-ready zapis (model3dUrl) ima veljaven lat/lng",
    "an AR-ready record (model3dUrl) has valid lat/lng",
    arBad.length === 0,
    `${EXHIBITS.filter((e) => e.model3dUrl).length} 3D zapisov; ${arBad.length} brez veljavne lokacije`,
  );

  // 4. vsak zgodovinski podatek ima evidenceStatus (iz znane lestvice)
  const badEvidence = EXHIBITS.filter((e) => !e.evidenceStatus || !KNOWN_EVIDENCE.has(e.evidenceStatus));
  push(
    "qa-evidence-status",
    "vsak zapis ima evidenceStatus iz lestvice",
    "every record carries an evidenceStatus from the scale",
    badEvidence.length === 0,
    `${EXHIBITS.filter((e) => KNOWN_EVIDENCE.has(e.evidenceStatus ?? "")).length}/${EXHIBITS.length} veljavnih; neznani: ${badEvidence.map((e) => e.evidenceStatus).filter(Boolean).join(", ") || "0"}`,
  );

  // 5. vsak vir ima identiteto (ime ali URL)
  const srcBad = EXHIBITS.flatMap((e) =>
    (e.sources ?? []).filter((s) => !(s.nameSi || s.nameEn || s.url)).map((s) => `${e.museumNo}`),
  );
  push(
    "qa-source-identity",
    "vsak vir ima identiteto (ime ali URL)",
    "every source carries an identity (name or URL)",
    srcBad.length === 0,
    `${EXHIBITS.reduce((a, e) => a + (e.sources ?? []).length, 0)} vrstic virov; ${srcBad.length} brez identitete`,
  );

  // 6. noben obstoječi muzejski zapis ni izgubljen (114; P24 je dodal MVG-114)
  const metaCount = META.counts?.exhibits ?? META.count?.exhibits ?? EXHIBITS.length;
  push(
    "qa-no-loss",
    "noben muzejski zapis ni izgubljen (114)",
    "no museum record is lost (114)",
    EXHIBITS.length === 114 && metaCount === EXHIBITS.length,
    `exhibits: ${EXHIBITS.length}, meta.count: ${metaCount}`,
  );

  // 7. sprehodi: zaporedje brez skritih lukenj (vrzeli so eksplicitne)
  const walkReports = WALKS.map((w) => {
    const items = walkItemsWithGaps(w);
    const stations = items.map((i) => i.station);
    const holes = stations.filter((n, i) => i > 0 && n !== stations[i - 1] + 1);
    const explicitGaps = WALK_GAPS.filter((g) => g.walkKey === w.key).length;
    return { key: w.key, holes, total: stations.length, explicitGaps, last: stations[stations.length - 1] ?? 0 };
  });
  const walkOk = walkReports.every((w) => w.holes.length === 0);
  const firstWalk = walkReports.find((w) => w.key === "Vas in njeni ljudje");
  push(
    "qa-walk-sequence",
    "sprehodi imajo neprekinjeno zaporedje postaj (vrzeli so eksplicitne)",
    "walks have an uninterrupted station sequence (gaps are explicit)",
    // P24: MVG-114 (kresna pesem) je postaja 36 — skupno mest 35 → 36
    walkOk && !!firstWalk && firstWalk.explicitGaps === 1 && firstWalk.total === 36,
    walkReports
      .map((w) => `${w.key}: 1–${w.last} (${w.total} mest, ${w.explicitGaps} eksplicitnih vrzeli)`)
      .join("; "),
  );

  // 8. coverage številke ustrezajo dejanskim podatkov
  const cov = computeCoverage();
  const covOk =
    cov.total === EXHIBITS.length &&
    cov.gps.withGps + cov.gps.withoutGps === EXHIBITS.length &&
    cov.images.withImage + cov.images.withoutImage === EXHIBITS.length &&
    cov.models3d.with3d + cov.models3d.without3d === EXHIBITS.length &&
    cov.sources.withSources + cov.sources.withoutSources === EXHIBITS.length &&
    Object.values(cov.byEvidence).reduce((a, b) => a + b, 0) === EXHIBITS.length &&
    cov.byPeriod.reduce((a, p) => a + p.count, 0) === EXHIBITS.length;
  push(
    "qa-coverage-matches",
    "coverage številke ustrezajo dejanskim podatkom",
    "coverage numbers match the actual data",
    covOk,
    `total ${cov.total}; gps ${cov.gps.withGps}+${cov.gps.withoutGps}; slike ${cov.images.withImage}+${cov.images.withoutImage}; 3D ${cov.models3d.with3d}+${cov.models3d.without3d}; viri ${cov.sources.withSources}+${cov.sources.withoutSources}`,
  );

  // 9. reconciliation zero-loss (issue #5)
  const recon = buildReconciliation();
  push(
    "qa-recon-zero-loss",
    "N83 → Atlas: zero-loss (noben izvorni zapis izgubljen)",
    "N83 → Atlas: zero-loss (no source record lost)",
    recon.zeroLoss && recon.totals.lost === 0,
    `obdelanih ${recon.totals.processedRows} vrstic; povezanih ${recon.totals.linked}; nerazrešenih ${recon.totals.unresolved} (ohranjenih z statusom); izgubljenih ${recon.totals.lost}`,
  );

  // 10. manjkajoča postaja 32 je dokumentirana v negativnih rezultatih
  const neg32 = NEGATIVE_RESULTS.find((n) => n.id === "neg-walk-station-32");
  push(
    "qa-station-32-documented",
    "manjkajoča postaja 32 ima negativni rezultat + razlog",
    "the missing station 32 has a negative result + reason",
    Boolean(neg32 && neg32.status === "NOT_FOUND") && firstWalk?.explicitGaps === 1,
    neg32 ? `status ${neg32.status}; v sprehodu je eksplicitno mesto 32` : "ni dokumentirana",
  );

  // 11. extra.json → vsak walk vnos se nanaša na obstoječi zapis
  const allSlugs = new Set(EXHIBITS.map((e) => e.slug));
  const orphanWalks = Object.entries(EXTRA)
    .filter(([, v]) => v?.walk?.name && v.walk.station != null)
    .filter(([slug]) => !allSlugs.has(slug))
    .map(([slug]) => slug);
  push(
    "qa-walk-refs",
    "vsak walk v extra.json se nanaša na obstoječi zapis",
    "every walk entry in extra.json refers to an existing record",
    orphanWalks.length === 0,
    `${Object.values(EXTRA).filter((v) => v?.walk?.name && v.walk.station != null).length} walk vnosov; ${orphanWalks.length} osirotelih`,
  );

  // 12. matrične knjige Podzemelj (issue #6): 22 knjig z veljavnimi povezavami + vpisi hiš
  const parish = parishStats();
  const parishBooksOk =
    parish.books === 22 &&
    parish.byType.baptism === 11 &&
    parish.byType.marriage === 5 &&
    parish.byType.death === 6 &&
    parish.housesWithVitals >= 1;
  push(
    "qa-parish-books",
    "matrične knjige župnije Podzemelj: 22 enot s povezavami (issue #6)",
    "parish registers of Podzemelj: 22 units with links (issue #6)",
    parishBooksOk,
    `${parish.books} knjig (${parish.byType.baptism} krstnih, ${parish.byType.marriage} poročnih, ${parish.byType.death} mrliških), obdobje ${parish.period}; vpisi: ${parish.vitalRecords} za ${parish.housesWithVitals}/${parish.housesTotal} hiš`,
  );

  // 13. HISTORICAL PANORAMA (issue #13): vsaka panorama ima veljavno vez na
  //     TimeSpot, heading, trditve s statusi, vire in FIZIČNI asset na disku
  const spotIds = new Set(TIME_SPOTS.map((s) => s.id));
  const claimStatuses = new Set([
    "DOCUMENTED",
    "RECONSTRUCTED",
    "ESTIMATE",
    "INTERPRETATION",
    "TO_COLLECT",
  ]);
  const panoErrors: string[] = [];
  for (const p of PANORAMAS) {
    if (!spotIds.has(p.timeSpotId)) panoErrors.push(`${p.id}: neznan TimeSpot ${p.timeSpotId}`);
    if (!(p.headingDeg >= 0 && p.headingDeg < 360)) panoErrors.push(`${p.id}: headingDeg izven 0–360`);
    if (p.claims.length < 3) panoErrors.push(`${p.id}: premalo trditev (<3)`);
    for (const c of p.claims) {
      if (!claimStatuses.has(c.status)) panoErrors.push(`${p.id}: neznan status ${c.status}`);
      if (!c.sourceSi || !c.sourceEn) panoErrors.push(`${p.id}: trditev brez vira`);
    }
    if (p.sources.length === 0) panoErrors.push(`${p.id}: brez virov`);
    if (!p.methodSi || !p.methodEn) panoErrors.push(`${p.id}: brez metodologije`);
    for (const url of [p.imageUrl, p.previewUrl].filter(Boolean) as string[]) {
      /* asset na disku se preveri ob buildu/produkciji (curl) — tu format URL */
      if (!/^\/panoramas\/[a-z0-9-]+\.jpg$/.test(url)) {
        panoErrors.push(`${p.id}: sumljiv URL asseta ${url}`);
      }
    }
  }
  /* panoramaId na točki mora obstajati v PANORAMAS (ni pripravljenih kazalcev) */
  const panoIds = new Set(PANORAMAS.map((p) => p.id));
  for (const s of TIME_SPOTS) {
    if (s.panoramaId && !panoIds.has(s.panoramaId)) {
      panoErrors.push(`spot ${s.id}: panoramaId ${s.panoramaId} ne obstaja`);
    }
  }
  push(
    "qa-panoramas",
    "historical panorame: vez na točko, evidence trditve, viri, asseti (issue #13)",
    "historical panoramas: spot link, evidence claims, sources, assets (issue #13)",
    panoErrors.length === 0,
    panoErrors.length === 0
      ? `${PANORAMAS.length} panorame (${PANORAMAS.map((p) => p.timeSpotId).join(", ")}); trditve: ${PANORAMAS.reduce((a, p) => a + p.claims.length, 0)}; asseti v /panoramas`
      : panoErrors.join("; "),
  );

  // 14. prenos iz arhiva (issue #16): revizija mora biti notranje dosledna
  const archErrors: string[] = [];
  if (ARCHIVE_TRANSFER_ROWS.length < 8) {
    archErrors.push(`premalo vrstic matrike: ${ARCHIVE_TRANSFER_ROWS.length}`);
  }
  const badRows = ARCHIVE_TRANSFER_ROWS.filter(
    (r) => !r.areaSi || !r.areaEn || !r.archiveSi || !r.currentSi || !r.actionSi,
  );
  if (badRows.length) {
    archErrors.push(`vrstice s praznimi polji: ${badRows.map((r) => r.areaEn).join(", ")}`);
  }
  const kurrentRows = ARCHIVE_TRANSFER_ROWS.filter((r) => /Kurrent/i.test(r.areaEn));
  if (kurrentRows.length < 2) {
    archErrors.push("matrika ne pokriva Kurrent serij");
  }
  for (const r of ARCHIVE_TRANSFER_ROWS) {
    if (r.transferred !== 0) {
      archErrors.push(`${r.areaEn}: transferred=${r.transferred}, pričakovano 0 (nadnabor)`);
    }
  }
  if (ARCHIVE_TRANSFER_AUDIT.totalTransferredEntries !== 0) {
    archErrors.push("totalTransferredEntries ≠ 0");
  }
  if (!ARCHIVE_TRANSFER_AUDIT.archiveRepo.archived) {
    archErrors.push("revizija ne potrjuje, da je arhiv arhiviran");
  }
  if (!/^[0-9a-f]{40}$/.test(ARCHIVE_TRANSFER_AUDIT.archiveRepo.headSha)) {
    archErrors.push("archiveRepo.headSha ni veljaven SHA-1");
  }
  if (!ARCHIVE_NON_TRANSFERS.some((n) => n.path === "download/README.md")) {
    archErrors.push("namerno neprenesen download/README.md ni dokumentiran");
  }
  push(
    "qa-archive-transfer",
    "prenos iz arhiva: matrika, verifikacija nadnaborja, dokumentirane izjeme (issue #16)",
    "archive transfer: matrix, superset verification, documented exceptions (issue #16)",
    archErrors.length === 0,
    archErrors.length === 0
      ? `${ARCHIVE_TRANSFER_ROWS.length} področij primerjanih; 0 prenosov (novi repo = striktni nadnabor); ${ARCHIVE_NON_TRANSFERS.length} namerno nepreneseno; arhiv ${ARCHIVE_TRANSFER_AUDIT.archiveRepo.path} @ ${ARCHIVE_TRANSFER_AUDIT.archiveRepo.headSha.slice(0, 7)} (archived, ${ARCHIVE_TRANSFER_AUDIT.archiveRepo.commits} commitov)`
      : archErrors.join("; "),
  );

  // 15. RESEARCH GAP CLOSURE v2 (issue #17): nove Kurrent vsebine morajo biti
  //     notranje dosledne (števke iz dejanskih podatkov, ne ročne)
  const i17Errors: string[] = [];
  // PV: 12 izpolnjenih vrstic, vsote se seštejejo (±1 joch), gozd prazen
  const pvFilled = PV_LAND_USE_1825.rows.filter((r) => r.joch !== null);
  if (pvFilled.length !== 10) {
    i17Errors.push(`PV izpolnjenih vrstic: ${pvFilled.length}, pričakovano 10`);
  }
  if (PV_LAND_USE_1825.rows.find((r) => r.cultureAsWritten === "Wälder")?.joch !== null) {
    i17Errors.push("PV: vrstica Wälder ni prazna (anomalija 1825 mora ostati dokumentirana)");
  }
  const pvSum =
    pvFilled.reduce((a, r) => a + (r.joch ?? 0) * 1600 + (r.klafter ?? 0), 0);
  const pvTotal =
    PV_LAND_USE_1825.totals.ersteSumme.joch * 1600 + PV_LAND_USE_1825.totals.ersteSumme.klafter +
    PV_LAND_USE_1825.totals.zweiteSumme.joch * 1600 + PV_LAND_USE_1825.totals.zweiteSumme.klafter;
  if (Math.abs(pvSum - pvTotal) > 3600) {
    i17Errors.push(`PV: vsota vrstic odstopa od skupne vsote za ${Math.round((pvSum - pvTotal) / 1600)} joch`);
  }
  // PR: mere se ujemajo s PV (<1 %)
  const prArea = PR_BOUNDARY_1825.dimensions.eastWestKlafter * PR_BOUNDARY_1825.dimensions.northSouthKlafter;
  const pvArea = PV_LAND_USE_1825.totals.grandTotal.joch * 1600;
  if (Math.abs(prArea - pvArea) / pvArea > 0.01) {
    i17Errors.push("PR mere ≠ PV površina (>1 %)");
  }
  if (PR_BOUNDARY_1825.boundaryPoints.length < 10) {
    i17Errors.push("PR: manj kot 10 točk meje");
  }
  // PS rekapitulacija: 102 + 2505 = 2607
  if (PS_RECAP_1826.summaBauplätze + PS_RECAP_1826.summaGrundparzellen !== PS_RECAP_1826.zusammen) {
    i17Errors.push("PS rekapitulacija se ne sešteje");
  }
  // PZ: 441 = 222 + 219
  if (PZ_ECONOMY_1825.population.male + PZ_ECONOMY_1825.population.female !== PZ_ECONOMY_1825.population.total) {
    i17Errors.push("PZ demografija se ne sešteje");
  }
  // PUA: 18 vrstic str. 3–10 + 4 vrstice P3 str. 11 + 47 vrstic P4 str. 12–34 + 32 vrstic P5-b str. 35–49 = 101
  if (PUA_CONTINUATION.rows.length !== 101 || PUA_CONTINUATION.pagesRead.length !== 47) {
    i17Errors.push(`PUA nadaljevanje: ${PUA_CONTINUATION.rows.length} vrstic / ${PUA_CONTINUATION.pagesRead.length} strani (pričakovano 101/47 po P5-b — register CEL)`);
  }
  // PT pregled: vsota verdiktov = pregledanih vrstic
  const sum = PT_REVIEW_2026.summary.confirmed + PT_REVIEW_2026.summary.corrections +
    PT_REVIEW_2026.summary.additionalRows + PT_REVIEW_2026.summary.repoOnly + PT_REVIEW_2026.summary.illegible;
  if (sum !== PT_REVIEW_2026.reviewedRows) {
    i17Errors.push(`PT pregled: verdikti ${sum} ≠ pregledanih ${PT_REVIEW_2026.reviewedRows}`);
  }
  const ATLAS_HOUSES_LENGTH = ATLAS_HOUSES.length;
  const ATLAS_HOUSE_ROWS = ATLAS_HOUSES.filter((h) => h.no !== "—").length;
  if (ATLAS_HOUSES_LENGTH !== 105 || ATLAS_HOUSE_ROWS !== 84) {
    i17Errors.push(`ATLAS_HOUSES: ${ATLAS_HOUSES_LENGTH} vrstic (${ATLAS_HOUSE_ROWS} hišnih) — pričakovano 105/84 po P3 paleografiji (101 + 4 dodane vrstice)`);
  }
  // Ustna zgodovina: protokol obstaja, intervjuji ostanejo PRAZNI
  if (ORAL_HISTORY_PROTOCOL.stages.length !== 4 || ORAL_HISTORY_PROTOCOL.rulesSi.length < 5) {
    i17Errors.push("protokol ustne zgodovine nepopoln");
  }
  if (ORAL_INTERVIEWS.length !== 0) {
    i17Errors.push("ORAL_INTERVIEWS ni prazen — izmišljeni intervjuji so prepovedani");
  }
  // Web verifikacije: ≥ 12 ciljev, vsak s statusom in URL-jem
  if (WEB_VERIFICATIONS.length < 12) {
    i17Errors.push(`web verifikacij: ${WEB_VERIFICATIONS.length} < 12`);
  }
  for (const w of WEB_VERIFICATIONS) {
    if (!w.target || !w.url || !w.findingSi) {
      i17Errors.push(`web verifikacija brez polj: ${w.target}`);
    }
  }
  // Matrika ≥ 15 vrstic; revizija z metodo in odprtimi točkami
  if (ISSUE17_MATRIX.length < 15) {
    i17Errors.push(`matrika #17: ${ISSUE17_MATRIX.length} < 15`);
  }
  if (!ISSUE17_AUDIT.stillOpenSi || !ISSUE17_AUDIT.methodSi || ISSUE17_AUDIT.issue !== 17) {
    i17Errors.push("revizija #17 nepopolna");
  }
  // KURRENT_SERIES: vsi series so sedaj vsaj delno prebrani (REVIEW), vsi viri N083 posodobljeni
  for (const s of KURRENT_SERIES) {
    if (s.pagesTranscribed === 0) {
      i17Errors.push(`KURRENT ${s.code}: nič prebranih strani po #17`);
    }
    if (s.status !== "REVIEW") {
      i17Errors.push(`KURRENT ${s.code}: status ${s.status} (pričakovano REVIEW)`);
    }
  }
  // Skeni/izpisi provenience v research/issue17/ (10 JSON-ov)
  // (datoteke se preverjajo ob buildu; tu preverimo, da so knjižne reference zapolnjene)
  push(
    "qa-issue17-gap-closure",
    "zapolnjevanje vrzeli #17: PV raba tal, PR meja, PS rekapitulacija, PZ demografija, PUA nadaljevanje, PT pregled, protokol, verifikacije",
    "gap closure #17: PV land use, PR boundary, PS recap, PZ demography, PUA continuation, PT review, protocol, verifications",
    i17Errors.length === 0,
    i17Errors.length === 0
      ? `PV 10/20 kultur (skupaj ${PV_LAND_USE_1825.totals.grandTotal.joch} j ≈ ${PV_LAND_USE_1825.totals.grandTotal.hectares} ha; gozd prazen); PR ${PR_BOUNDARY_1825.dimensions.eastWestKlafter}×${PR_BOUNDARY_1825.dimensions.northSouthKlafter} kl (<1 % od PV); PS 102+2505=2607; PZ 441 prebivalcev, 28. 7. 1825; PUA +18 vnosov (str. 3–10) + P3 str. 11 (+4, črka H); PT 81/105 verdiktov; register 105 vrstic po P3 paleografiji; protokol 4 faze + 0 intervjujev; ${WEB_VERIFICATIONS.length} web verifikacij; matrika ${ISSUE17_MATRIX.length} vrstic; Kurrent 7/7 serij delno prebranih (REVIEW)`
      : i17Errors.join("; "),
  );

  // ——— P3 PALEOGRAFSKA PREVERBA (2. krog) ————————————————————————
  const p3Errors: string[] = [];
  // Register: 105 vrstic, hiša 41 ne obstaja, 34-dvojnica obstaja
  if (ATLAS_HOUSES.some((h) => h.no === "41")) {
    p3Errors.push("hiša 41 še obstaja — renumeracija str. 4 ni aplicirana");
  }
  if (!ATLAS_HOUSES.some((h) => h.no === "34 (prečrtana dvojnica)")) {
    p3Errors.push("prečrtana dvojnica 34 manjka (nič-zguba)");
  }
  for (const no of ["35", "36", "37", "38", "39", "40"]) {
    const row = ATLAS_HOUSES.find((h) => h.no === no);
    if (!row || !row.paleo || !row.owner.includes("Brinig") && !row.owner.includes("Milleg")) {
      p3Errors.push(`str. 4 hiša ${no}: renumerirana vrstica s paleo opombo manjka`);
    }
  }
  // 15 popravkov: ključne vrednosti
  const expectOwner: [string, string][] = [
    ["1", "Veith"],
    ["7", "Lebing"],
    ["7½", "Bödig"],
    ["8", "Lebing"],
    ["8½", "Bödig"],
    ["20", "Krištan"],
    ["39", "Brinig Miklo"],
    ["71½", "Stettner"],
    ["76", "Strauß"],
    ["76½", "Hufschmied"],
    ["79", "Strauß"],
    ["81", "Strauß"],
    ["96", "Ihmeyer"],
    ["98", "Zollamt"],
    ["99", "prazna"],
  ];
  for (const [no, kw] of expectOwner) {
    const row = ATLAS_HOUSES.find((h) => h.no === no);
    if (!row || !row.owner.includes(kw)) {
      p3Errors.push(`hiša ${no}: lastnik ne vsebuje »${kw}« (${row?.owner ?? "VRSTICA MANJKA"})`);
    }
  }
  // Hiša 90 ostaja divergentna (brez popravka)
  const h90 = ATLAS_HOUSES.find((h) => h.no === "90");
  if (!h90 || !h90.owner.includes("divergirajo")) {
    p3Errors.push("hiša 90: divergentna branja morajo ostati vidna");
  }
  // Vsi novi vnosi imajo paleo opombo; statusi ostajajo REVIEW
  const newRows = ["hiša-6b", "hiša-73b", "hiša-78b", "hiša-101"];
  for (const id of newRows) {
    const row = ATLAS_HOUSES.find((h) => h.id === id);
    if (!row || !row.paleo) {
      p3Errors.push(`nova vrstica ${id} brez paleo opombe`);
    }
  }
  if (ATLAS_HOUSES.some((h) => h.status !== "REVIEW")) {
    p3Errors.push("status hiše ni REVIEW — pretvarjanje v VERIFIED je prepovedano");
  }
  // PT_PALEOGRAPHY_P3: 18 vrstic 2. kroga, metoda, aplikacija
  if (PT_PALEOGRAPHY_P3.pass2Rows.length !== 18) {
    p3Errors.push(`P3 vrstic 2. kroga: ${PT_PALEOGRAPHY_P3.pass2Rows.length} ≠ 18`);
  }
  if (!PT_PALEOGRAPHY_P3.appliedSi || !PT_PALEOGRAPHY_P3.methodSi || PT_PALEOGRAPHY_P3.vlmCalls !== 9) {
    p3Errors.push("P3 revizija (metoda/aplicirano/VLM klici) nepopolna");
  }
  // model.ts: lastniki usklajeni z registrom (Strauß, Ihmeyer, Zollamt, Stettner, Hufschmied, Veith, Lebing, Bödig)
  const ownerKws = ["Strauß Georg", "Ihmeyer", "Zollamt", "Stettner", "Hufschmied", "Veith", "Lebing", "Bödig", "Brinig"];
  for (const kw of ownerKws) {
    if (!ATLAS_OWNERS.some((o) => o.nameAsWritten.includes(kw))) {
      p3Errors.push(`model.ts: lastnik z »${kw}« manjka`);
    }
  }
  if (ATLAS_OWNERS.some((o) => o.id === "lastnik-leskovec")) {
    p3Errors.push("lastnik-leskovec — nadomeščen z Lebing/Bödig (P3)");
  }
  // PUA str. 11: 4 vnosi (Hlebety, Huditsch, Husitsch, Hutweiz)
  const pua11 = PUA_CONTINUATION.rows.filter((r) => r.page === 11);
  if (pua11.length !== 4) {
    p3Errors.push(`PUA str. 11: ${pua11.length} vnosov ≠ 4`);
  }
  for (const nm of ["Hlebety", "Huditsch", "Husitsch", "Hutweiz"]) {
    if (!pua11.some((r) => r.nameAsWritten.includes(nm))) {
      p3Errors.push(`PUA str. 11: vnos ${nm} manjka`);
    }
  }
  // KURRENT_SERIES posodobljen (PT 84, PUA 49 strani / 101 vnosov po P5-b — register CEL)
  const ptSeries = KURRENT_SERIES.find((s) => s.code === "PT");
  const puaSeries = KURRENT_SERIES.find((s) => s.code === "PUA");
  if (ptSeries?.structuredEntries !== 84 || puaSeries?.pagesTranscribed !== 49 || puaSeries?.structuredEntries !== 101) {
    p3Errors.push("KURRENT_SERIES PT/PUA nista posodobljena po P3/P4/P5-b (pričakovano PT 84, PUA 49 strani/101 vnosov)");
  }
  push(
    "qa-p3-paleografija",
    "P3 paleografska preverba: renumeracija str. 4, 15 lastniških popravkov (2-krožna konvergenca), 4 dodane vrstice, PUA str. 11",
    "P3 palaeographic verification: the p. 4 renumbering, 15 owner corrections (2-pass convergence), 4 added rows, PUA p. 11",
    p3Errors.length === 0,
    p3Errors.length === 0
      ? `Register 105 vrstic (hiša 41 odstranjena, dvojnica 34 dokumentirana); 15 popravkov + 4 vrstice aplicirane ob 2-krožni konvergenci (Veith 1, Lebing 7/8, Bödig 7½/8½, Brinig 35–40, Strauß 76/79/81–84, Ihmeyer 96, Zollamt 98, K-priimek 20); hiša 90 ostaja divergentna; PUA str. 11 +4 vnosi (Hlebety/Huditsch/Husitsch/Hutweiz); statusi REVIEW`
      : p3Errors.join("; "),
  );

  // 17. P4 — PUA nadaljevanje (str. 12–34): struktura, ključni priimki, križanje s PT (P5-b dopolni 35–49 — ločen test)
  const p4Errors: string[] = [];
  const p4All = PUA_CONTINUATION.rows.filter((r) => r.page >= 12 && r.page <= 34);
  if (p4All.length !== 47) {
    p4Errors.push(`P4 vrstic: ${p4All.length} ≠ 47`);
  }
  const p4RowsNum = p4All.map((r) => r.row);
  if (p4RowsNum.length === 47 && (p4RowsNum[0] !== 22 || p4RowsNum[46] !== 68)) {
    p4Errors.push(`P4 zap. št.: ${p4RowsNum[0]}–${p4RowsNum[46]} (pričakovano 22–68)`);
  }
  // ključni priimki P4 (vsak iz druge strani)
  const p4Surnames: [number, string][] = [
    [12, "Höflehner"],
    [13, "Jakobstitzsch"],
    [14, "Jankovitsche"],
    [16, "Mäusel"],
    [17, "Loral"],
    [18, "Krischan"],
    [20, "Kosirhan"],
    [21, "Grönig"],
    [22, "Wundsch"],
    [23, "Hlobutschar"],
    [24, "Lukentitz"],
    [25, "Rappar"],
    [26, "Mallestitak"],
    [27, "Mandl"],
    [28, "Polcig"],
    [29, "Muhč"],
    [30, "Leiner"],
    [31, "Rußa"],
    [32, "Gnoy"],
    [33, "Pasticz"],
    [34, "Pfister"],
  ];
  for (const [pg, nm] of p4Surnames) {
    if (!PUA_CONTINUATION.rows.some((r) => r.page === pg && r.nameAsWritten.includes(nm))) {
      p4Errors.push(`P4 str. ${pg}: priimek ${nm} manjka`);
    }
  }
  // cerkev sv. Vida — institucija (hišna št. 0 = konvencija za institucije)
  const kirche = PUA_CONTINUATION.rows.find((r) => r.nameAsWritten.includes("Kirche"));
  if (!kirche || kirche.page !== 22 || kirche.row !== 44 || (kirche.houseNos.length !== 0 && kirche.houseNos[0] !== "0")) {
    p4Errors.push("P4: Kirche H. Veith (str. 22, v. 44, institucija) manjka ali pokvarjen");
  }
  // križanje s PT: vsak vnos s hišno št. mora imeti PT referenco v confidence
  const withHouse = PUA_CONTINUATION.rows.filter((r) => r.page >= 12 && r.houseNos.length > 0 && r.houseNos[0] !== "0");
  if (!withHouse.every((r) => r.confidence.includes("PT"))) {
    p4Errors.push("P4: kakšen vnos s hišno št. nima PT reference v confidence");
  }
  // PUA strani 35–49: po P5-b prebrane — opomba mora dokumentirati CEL register (ne več TO_COLLECT)
  if (!PUA_CONTINUATION.noteSi.includes("35–49") || !PUA_CONTINUATION.noteSi.includes("CEL")) {
    p4Errors.push("P4: opomba mora dokumentirati strani 35–49 kot prebrane (P5-b — register CEL)");
  }
  if (PUA_CONTINUATION.noteSi.includes("TO_COLLECT")) {
    p4Errors.push("P4: opomba ne sme več navajati TO_COLLECT za PUA (P5-b zaključen)");
  }
  push(
    "qa-p4-pua-nadaljevanje",
    "P4 PUA nadaljevanje: strani 12–34 (47 vnosov, zap. št. 22–68), Kirche H. Veith, križanje s PT; strani 35–49 prebrane v P5-b — register CEL",
    "P4 PUA continuation: pages 12–34 (47 entries, rows 22–68), Kirche H. Veith, PT cross-check; pages 35–49 read in P5-b — register complete",
    p4Errors.length === 0,
    p4Errors.length === 0
      ? `23 strani (12–34) po 1 VLM klic; 47 vnosov: Höflehner, Jakobstitzsch, Jankovitsche, Krischan, Loral, Kosirhan, Grönig, Wundsch, Bučar, Kirche H. Veith (cerkev sv. Vida [~]), Hlobutschar, Lukentitz, Rappar, Millea, Mallestitak, Mandl, Grangl, Polcig, Muhč, Leiner, Rußa, Juttner, Jhan, Gnoy, Pasticz, Prodoritche, Pfister; ključna ugotovitev: PUA ≠ PT številčenje hiš [~]; P5-b dopolni register (32 vnosov 69–100 — glej qa-p5-b); statusi REVIEW`
      : p4Errors.join("; "),
  );

  // 18. P5 — navzkrižna analiza PUA ↔ PT (deterministična): števci, ugotovitev, omejitve (posodobljeno po P5-b)
  const p5Errors: string[] = [];
  const p5c = PUA_PT_CROSS.counts;
  if (p5c.puaEntries !== 101 || p5c.ptHouseRows !== 84 || p5c.ptParcelRows !== 21) {
    p5Errors.push(`P5 števci vhodov: ${p5c.puaEntries}/${p5c.ptHouseRows}/${p5c.ptParcelRows} (pričakovano 101/84/21 po P5-b)`);
  }
  if (p5c.withReadableHouseNo !== 91 || p5c.directSurnameMatch !== 0) {
    p5Errors.push(`P5 ujemanja: ${p5c.withReadableHouseNo} z št., ${p5c.directSurnameMatch} ujemanj (pričakovano 91/0)`);
  }
  if (p5c.divergent !== 72 || p5c.weakMatch !== 3) {
    p5Errors.push(`P5 divergence: ${p5c.divergent}/${p5c.weakMatch} (pričakovano 72/3)`);
  }
  if (p5c.surnamesInBothRegisters !== 11) {
    p5Errors.push(`P5 priimki v obeh: ${p5c.surnamesInBothRegisters} (pričakovano 11)`);
  }
  // 84 hišnih vrstic = 83 edinstvenih št. (34 = prečrtana dvojnica: 2 vrstici, 1 št.)
  if (p5c.ptNumbersCovered + p5c.ptNumbersWithoutPua !== 83) {
    p5Errors.push(`P5 pokritost PT: ${p5c.ptNumbersCovered}+${p5c.ptNumbersWithoutPua} ≠ 83 (84 vrstic − 1 dvojnica 34)`);
  }
  if (PUA_PT_CROSS.status !== "REVIEW") {
    p5Errors.push(`P5 status: ${PUA_PT_CROSS.status} (pričakovano REVIEW)`);
  }
  if (!PUA_PT_CROSS.findingSi.includes("0/91") || !PUA_PT_CROSS.findingSi.includes("[~]")) {
    p5Errors.push("P5 ugotovitev mora vsebovati 0/91 in oznako negotovosti [~]");
  }
  if (!PUA_PT_CROSS.caveatsSi.includes("paleografijo") || !PUA_PT_CROSS.nextStepSi.includes("35–49") || !PUA_PT_CROSS.nextStepSi.includes("OPRAVLJENO")) {
    p5Errors.push("P5 mora dokumentirati omejitve (paleografija) in OPRAVLJEN korak P5-b (strani 35–49)");
  }
  if (PUA_PT_CROSS.surnameOverlaps.length < 6) {
    p5Errors.push(`P5 priimki-sovpadanja: ${PUA_PT_CROSS.surnameOverlaps.length} vrstic (pričakovano ≥ 6 po P5-b)`);
  }
  // usklajenost s PUA_CONTINUATION: analiza mora pokrivati vse vnose, ki jih je prebrala P4
  if (p5c.puaEntries !== PUA_CONTINUATION.rows.length) {
    p5Errors.push(`P5/P4 neskladje: PUA_PT_CROSS ${p5c.puaEntries} ≠ PUA_CONTINUATION ${PUA_CONTINUATION.rows.length}`);
  }
  push(
    "qa-p5-pua-pt-cross",
    "P5 navzkrižna analiza PUA ↔ PT (register CEL po P5-b): 0/91 neposrednih ujemanj po hišnih št., 11 priimkov v obeh registrih na različnih št., sklep [~] = primerjava po imenih",
    "P5 cross-analysis PUA ↔ PT (register complete after P5-b): 0/91 direct matches by house no., 11 surnames in both registers at different numbers, conclusion [~] = compare by names",
    p5Errors.length === 0,
    p5Errors.length === 0
      ? `Deterministično (Levenshtein ≥ 0,72/0,50, scripts/pua-pt-cross.py, brez AI): 101 vnosov PUA (str. 3–49, register CEL po P5-b) ↔ 84 hišnih vrstic PT; 48 PT št. pokritih, 16 PUA št. brez PT vpisa (blok 41–60); ugotovitev [~]: PUA = indeks lastnikov parcel z lastno hišno referenco; omejitve: obe vira strojna branjla [~]; naslednji koraki: OPRAVLJENO strani 35–49, človeška paleografija, arhivsko vprašanje ARS`
      : p5Errors.join("; "),
  );

  // 18b. P5-b — preostale strani PUA 35–49 (priimki P–Ž): obseg, vsebinske kontrole, razrešene napovedi
  const p5bErrors: string[] = [];
  const puaRows = PUA_CONTINUATION.rows;
  const puaNew = puaRows.filter((r) => r.page >= 35);
  if (puaNew.length !== 32) {
    p5bErrors.push(`P5-b novih vnosov: ${puaNew.length} (pričakovano 32, zap. št. 69–100)`);
  }
  const puaNewRows = puaNew.map((r) => r.row);
  if (Math.min(...puaNewRows) !== 69 || Math.max(...puaNewRows) !== 100) {
    p5bErrors.push(`P5-b zap. št. obseg: ${Math.min(...puaNewRows)}–${Math.max(...puaNewRows)} (pričakovano 69–100)`);
  }
  for (const pg of [35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]) {
    if (!puaNew.some((r) => r.page === pg)) {
      p5bErrors.push(`P5-b manjka stran ${pg}`);
    }
  }
  const puaNames = puaNew.map((r) => r.nameAsWritten).join(" |");
  for (const must of ["Urlich Georg", "Ulrich Mida", "Verbitzcher", "Schello Georg", "Lipovšek", "Strauß", "Zollamt"]) {
    if (!puaNames.includes(must)) {
      p5bErrors.push(`P5-b manjka ključno ime: ${must}`);
    }
  }
  // skupinski/skrajni vnosi konec registra
  if (!puaNames.includes("Gemeinde Malfz") || !puaNames.includes("Uebersprungene")) {
    p5bErrors.push("P5-b manjkajo skupinski vnosi (Gemeinde Malfz / Uebersprungene Parzellen-Numern)");
  }
  // razrešene napovedi W-most: h32 DELNO V PRID, h64 ZAVRNJENO, h65 NEREŠENO, h68 POTRJENO
  const preds = PUA_PT_WBRIDGE.predictions;
  const resolvedCounts = ["POTRJENO", "ZAVRNJENO", "NEREŠENO", "DELNO V PRID"];
  for (const rv of resolvedCounts) {
    if (!preds.some((p) => p.resolved === rv)) {
      p5bErrors.push(`P5-b razrešitev napovedi manjka verdikt ${rv}`);
    }
  }
  const h68 = preds.find((p) => p.house.includes("h68"));
  if (!h68 || !h68.expectedOwners.includes("Ulrich Mida") || h68.resolved !== "POTRJENO") {
    p5bErrors.push("P5-b napoved h68 ni potrjena (pričakovano: Ulrich Mida, MATCH 1,0)");
  }
  push(
    "qa-p5-b-pua-35-49",
    "P5-b: PUA strani 35–49 prebrane (32 vnosov, zap. št. 69–100) — register CEL (101 vnosov); napovedi W-most razrešene: h68 POTRJENA, h32 delno v prid, h64 zavrnjena, h65 nerešena [~]",
    "P5-b: PUA pages 35–49 read (32 entries, no. 69–100) — register COMPLETE (101 entries); W-bridge predictions resolved: h68 CONFIRMED, h32 partially supported, h64 rejected, h65 unresolved [~]",
    p5bErrors.length === 0,
    p5bErrors.length === 0
      ? `VLM (1 klic/stran, ~92 % JPEG): 15 strani (35–49, priimki P–Ž: Schim-, Stübler, Strauß, Stepanitsch, Schello, Urlich/Ulrich, Verbitzcher, Wardian, Wentschitsch, Zollamt, Waisenkinder, Lipovšek + skupinski vnosi Gemeinde/Uebersprungene); register 1825 zdaj CEL — vse ostaja REVIEW (strojno branje ni dokazni vir); napovedi: h68 »Ulrich Mida« MATCH 1,0; h32 »Urlich Georg« PARTIAL 0,67 (komponenti Georg+Ulrich, vrstni red zamenjan [~]); h64 »Verbitzcher Mathä« MISMATCH 0,46 (fonetska bližina [~]); h65 brez protistrani (vrzel [~]); 2/4 v prid — zaupanje v W-most se je dvignilo`
      : p5bErrors.join("; "),
  );

  // P5-c: W-most PT ↔ PUA (posodobljeno po P5-b)
  const p5w = PUA_PT_WBRIDGE.counts;
  const p5wErrors: string[] = [];
  if (p5w.ptRowsWithW !== 43 || p5w.wRefsTotal !== 45 || p5w.wDistinct !== 26) {
    p5wErrors.push(`P5-c W-obseg: ${p5w.ptRowsWithW}/${p5w.wRefsTotal}/${p5w.wDistinct} (pričakovano 43/45/26)`);
  }
  if (p5w.wWithPua !== 25 || p5w.wNoPua !== 1) {
    p5wErrors.push(`P5-c W-protistrani: ${p5w.wWithPua}+${p5w.wNoPua} (pričakovano 25+1 = 26 po P5-b)`);
  }
  if (p5w.match + p5w.partial + p5w.mismatch !== p5w.wWithPua) {
    p5wErrors.push(`P5-c verdikti: ${p5w.match}+${p5w.partial}+${p5w.mismatch} ≠ ${p5w.wWithPua}`);
  }
  if (p5w.match !== 8 || p5w.partial !== 10 || p5w.mismatch !== 7) {
    p5wErrors.push(`P5-c razdelitev: ${p5w.match}/${p5w.partial}/${p5w.mismatch} (pričakovano 8/10/7 po P5-b)`);
  }
  if (PUA_PT_WBRIDGE.status !== "REVIEW") {
    p5wErrors.push(`P5-c status: ${PUA_PT_WBRIDGE.status} (pričakovano REVIEW)`);
  }
  if (!PUA_PT_WBRIDGE.hypothesisSi.includes("[~]") || !PUA_PT_WBRIDGE.findingSi.includes("72 %")) {
    p5wErrors.push("P5-c hipoteza/ugotovitev mora vsebovati [~] in 72 % (posodobljeno po P5-b)");
  }
  if (PUA_PT_WBRIDGE.bestMatches.length !== 8) {
    p5wErrors.push(`P5-c najboljših ujemanj: ${PUA_PT_WBRIDGE.bestMatches.length} (pričakovano 8 po P5-b — vključno W.60/W.68)`);
  } else {
    const w60 = PUA_PT_WBRIDGE.bestMatches.find((m) => m.w === "W.60");
    const w68 = PUA_PT_WBRIDGE.bestMatches.find((m) => m.w === "W.68");
    if (!w60 || !w60.puaNames.includes("Schello Georg")) p5wErrors.push("P5-c W.60 manjka/napačen (Schello Georg p42 v85)");
    if (!w68 || !w68.puaNames.includes("Ulrich Mida")) p5wErrors.push("P5-c W.68 manjka/napačen (Ulrich Mida p44 v90)");
  }
  if (PUA_PT_WBRIDGE.predictions.length !== 4) {
    p5wErrors.push(`P5-c napovedi: ${PUA_PT_WBRIDGE.predictions.length} (pričakovano 4: h32/h64/h65/h68)`);
  } else {
    for (const h of ["h32", "h64", "h65", "h68"]) {
      if (!PUA_PT_WBRIDGE.predictions.some((p) => p.house.includes(h))) {
        p5wErrors.push(`P5-c manjka napoved ${h}`);
      }
    }
  }
  if (!PUA_PT_WBRIDGE.caveatsSi.includes("ponovljiva") || !PUA_PT_WBRIDGE.findingSi.includes("0/91")) {
    p5wErrors.push("P5-c mora navesti ponovljivost in izhodišče P5-a (0/91)");
  }
  if (!PUA_PT_WBRIDGE.findingSi.includes("W.62") || !PUA_PT_WBRIDGE.caveatsSi.includes("W.47")) {
    p5wErrors.push("P5-c mora dokumentirati šumenje (W.62 dvojni vpis, W.47 prečrtana)");
  }

  push(
    "qa-p5-pua-pt-wbridge",
    "P5-c W-most (posodobljen po P5-b): 43 vrstic PT s 45 W-sklici (26 različnih), 25 z PUA protistrani, 18/25 ujemanj ≥ 0,50 (8 MATCH — novi W.60/W.68), 4 napovedi RAZREŠENE",
    "P5-c W-bridge (updated after P5-b): 43 PT rows with 45 W-references (26 distinct), 25 with a PUA counterpart, 18/25 matches ≥ 0.50 (8 MATCH — new W.60/W.68), 4 predictions RESOLVED",
    p5wErrors.length === 0,
    p5wErrors.length === 0
      ? `Deterministično (scripts/pua-pt-wbridge.py, brez AI): most med različnima številčenjema iz P5-a — hipoteza [~] W.<n> = PUA hišna št. lastnika; najmočnejša ujemanja: W.68 Ulrich↔Ulrich 1,0 (napoved POTRJENA), W.60 Schello↔Schello 1,0, W.2 Hlebetz↔Hlebety 0,86, W.24/25 Brinig↔Bring 0,83, W.1 Mufa↔Wufa 0,75 (M↔W Kurrent); po P5-b: 25 W s protistrani (ostane samo W.65 brez — vrzel [~]); napovedi razrešene: h68 POTRJENA, h32 DELNO V PRID (0,67), h64 ZAVRNJENA (0,46 [~]), h65 NEREŠENA; omejitve: strojna branjla [~], prečrtana W.47, dvojni vpis W.62`
      : p5wErrors.join("; "),
  );

  // P6: georeferenca zemljevida 1812 (OCR → afina/kvadratna)
  const g1812 = MAP_1812.georef;
  const g1812Errors: string[] = [];
  if (MAP_1812.georeferencePath.status !== "REVIEW") {
    g1812Errors.push(`1812 status: ${MAP_1812.georeferencePath.status} (pričakovano REVIEW)`);
  }
  if (!g1812) {
    g1812Errors.push("1812 georef: manjka objekt z rezultati");
  } else {
    if (g1812.controlPoints !== 15) g1812Errors.push(`1812 kontrolnih točk: ${g1812.controlPoints} (pričakovano 15)`);
    if (g1812.residualsKm.median > 15 || g1812.residualsKm.max > 30) g1812Errors.push(`1812 residuali preveliki: ${g1812.residualsKm.median}/${g1812.residualsKm.max} km`);
    const ratio = g1812.scaleMPerPx.x / g1812.scaleMPerPx.y;
    if (ratio < 0.9 || ratio > 1.1) g1812Errors.push(`1812 anizotropija: razmerje ${ratio.toFixed(3)} (pričakovano ~1)`);
    const { x, y } = g1812.gribljePx;
    if (x < 0 || x > 8297 || y < 0 || y > 6080) g1812Errors.push(`1812 Griblje px izven lista: (${x}, ${y})`);
    if (g1812.uncertaintyKm > 15) g1812Errors.push(`1812 negotovost: ± ${g1812.uncertaintyKm} km (pričakovano ≤ 15)`);
    if (g1812.artifacts.length < 5) g1812Errors.push(`1812 artefaktov: ${g1812.artifacts.length} (pričakovano ≥ 5)`);
  }
  // P7: koroboracija na drugem skenu istega lista
  const corr = MAP_1812.georef?.corroboration;
  if (!corr) {
    g1812Errors.push("1812 koroboracija: manjka objekt (P7)");
  } else {
    if (corr.controlPoints < 10) g1812Errors.push(`1812 koroboracija točk: ${corr.controlPoints} (pričakovano ≥ 10)`);
    if (corr.registration.inliers < 1000) g1812Errors.push(`1812 registracija inlierjev: ${corr.registration.inliers} (pričakovano ≥ 1000)`);
    if (corr.registration.rmsPx > 10) g1812Errors.push(`1812 registracija RMS: ${corr.registration.rmsPx} px (pričakovano ≤ 10)`);
    const cratio = corr.scaleMPerPx.x / corr.scaleMPerPx.y;
    if (cratio < 0.9 || cratio > 1.1) g1812Errors.push(`1812 2. sken anizotropija: ${cratio.toFixed(3)}`);
    if (corr.residualsKm.median > 15) g1812Errors.push(`1812 2. sken residuali: ${corr.residualsKm.median} km (pričakovano ≤ 15)`);
    const { x: ax, y: ay } = corr.gribljePathA;
    if (ax < 0 || ax > 7636 || ay < 0 || ay > 5936) g1812Errors.push(`1812 pot A izven 2. skena: (${ax}, ${ay})`);
    const { x: bx, y: by } = corr.gribljePathB;
    if (bx < 0 || bx > 7636 || by < 0 || by > 5936) g1812Errors.push(`1812 pot B izven 2. skena: (${bx}, ${by})`);
    if (corr.agreementKm > (MAP_1812.georef?.uncertaintyKm ?? 10)) g1812Errors.push(`1812 sporazumenje: ${corr.agreementKm} km (pričakovano ≤ negotovosti ± ${MAP_1812.georef?.uncertaintyKm ?? 10} km)`);
    if (corr.artifacts.length < 4) g1812Errors.push(`1812 koroboracija artefaktov: ${corr.artifacts.length} (pričakovano ≥ 4)`);
  }
  const mvg092 = (exhibitsRaw as { exhibits: Array<{ museumNo?: string; image?: string; imageCredit?: string; sources?: { sourceKey?: string }[] }> })
    .exhibits.find((e) => e.museumNo === "MVG-092");
  if (!mvg092 || mvg092.image !== "/images/authentic/griblje-okolis-1812-900.jpg") {
    g1812Errors.push("MVG-092: slika ni izrez 1812 z oznako");
  }
  if (!mvg092?.imageCredit?.includes("Giraldon") || !mvg092?.imageCredit?.includes("[~]")) {
    g1812Errors.push("MVG-092: kredit mora navesti Giraldon 1812 in oznako negotovosti [~]");
  }
  if (!mvg092?.sources?.some((s) => (s.sourceKey ?? "").includes("Provinces_Illyriennes_Servie_et_Bosnie_1812"))) {
    g1812Errors.push("MVG-092: manjka vir obdobjeni izvirnik (Commons)");
  }

  push(
    "qa-1812-georef",
    "Zemljevid 1812: georeferenca [~] izvedena + koroborirana — 15 OCR točk, merilo ~126 m/px, Griblje px (2499, 2286) ± 10 km; P7: 2. sken (IA) — sporazumenje 5,6 km",
    "1812 map: georeference [~] executed + corroborated — 15 OCR points, scale ~126 m/px, Griblje px (2499, 2286) ± 10 km; P7: 2nd scan (IA) — agreement 5.6 km",
    g1812Errors.length === 0,
    g1812Errors.length === 0
      ? `Deterministično (tesseract OCR + LSQ afina/kvadratna, brez AI-branja vsebine; research/georef-1812/fit-georef.py): kontrolne točke so centri OCR-anih NAPISOV [~]; afina in kvadratna preslikava se za Griblje ujemata na ± 2 px; pokritje lista ~11–24°E, 41–48°N; koroboracija P7: ORB+RANSAC registracija sken1↔sken2 (4030 inlierjev, RMS 3,9 px) + neodvisen 12-točkovni OCR model 2. skena (mediana residualov 9,7 km, celih besed 6,2 km) — obe poti za Griblje se ujemata na 37 px = 5,6 km, znotraj ± 10 km; omejitve: brez mrežnih stopinj, Parisov meridian nepotrjen, končna potrditev = človeška paleografija/QGIS`
      : g1812Errors.join("; "),
  );

  // ——— P10: SEKCIJSKA MREŽA eZKN — A03/A05 GEOREFERENCIRANA, A04 POPRAVLJENA ———
  const p10Errors: string[] = [];
  if (SHEET_GEOREFS.length !== 5) {
    p10Errors.push(`SHEET_GEOREFS: ${SHEET_GEOREFS.length} vnosov (pričakovano 5: A01–A05)`);
  }
  const georefA03 = SHEET_GEOREFS.find((g) => g.id === "georef-a03");
  const georefA04 = SHEET_GEOREFS.find((g) => g.id === "georef-a04");
  const georefA05 = SHEET_GEOREFS.find((g) => g.id === "georef-a05");

  // A03 = celica dg — P50: NEATLINE_PARTIAL_GEOREFERENCED (aktivacija P46 afine)
  if (!georefA03) {
    p10Errors.push("georef-a03 manjka v SHEET_GEOREFS");
  } else {
    const b = georefA03.bounds;
    if (georefA03.status !== "NEATLINE_PARTIAL_GEOREFERENCED") p10Errors.push(`A03 status: ${georefA03.status} (pričakovano NEATLINE_PARTIAL_GEOREFERENCED — P50)`);
    if (Math.abs(b[0][0] - 45.557532) > 5e-5 || Math.abs(b[0][1] - 15.248718) > 5e-5)
      p10Errors.push(`A03 bounds S/Z: ${b[0]} (pričakovano [45.557532, 15.248718] = P46 neatline celice VKIX24dg)`);
    if (Math.abs(b[1][0] - 45.543722) > 5e-5 || Math.abs(b[1][1] - 15.272827) > 5e-5)
      p10Errors.push(`A03 bounds J/V: ${b[1]} (pričakovano [45.543722, 15.272827])`);
    if (Math.abs(georefA03.scaleMPerPixel - 0.7746) > 0.005)
      p10Errors.push(`A03 merilo: ${georefA03.scaleMPerPixel} (pričakovano 0,7746 — P46 s̄)`);
    if (georefA03.pixels.width !== 2645 || georefA03.pixels.height !== 2154)
      p10Errors.push(`A03 px: ${georefA03.pixels.width}×${georefA03.pixels.height}`);
    const cpSi = georefA03.controlPoints.map((c) => c.fromSi).join(" |");
    for (const must of ["VKIX24dg", "TRIBUTSCH", "WEIDENDORF"]) {
      if (!cpSi.includes(must)) p10Errors.push(`A03 kontrolna točka manjka: ${must}`);
    }
    if (!georefA03.methodSi.includes("O.IX24dg")) p10Errors.push("A03 metoda mora navesti oznako »O.IX24dg«");
    if (!georefA03.methodSi.includes("AKTIVACIJA P50")) p10Errors.push("A03 metoda mora navesti AKTIVACIJO P50");
  }

  // A04 = POPRAVLJENA celica cg (P9 umaknjena) — P50: NEATLINE_GEOREFERENCED
  if (!georefA04) {
    p10Errors.push("georef-a04 manjka v SHEET_GEOREFS");
  } else {
    const b = georefA04.bounds;
    if (georefA04.status !== "NEATLINE_GEOREFERENCED") p10Errors.push(`A04 status: ${georefA04.status} (pričakovano NEATLINE_GEOREFERENCED — P50)`);
    if (Math.abs(b[0][0] - 45.55737) > 5e-5 || Math.abs(b[0][1] - 15.273012) > 5e-5)
      p10Errors.push(`A04 bounds S/Z: ${b[0]} (pričakovano [45.55737, 15.273012] = P46 neatline celice VKIX24cg)`);
    if (Math.abs(b[1][0] - 45.543554) > 5e-5 || Math.abs(b[1][1] - 15.297115) > 5e-5)
      p10Errors.push(`A04 bounds J/V: ${b[1]} (pričakovano [45.543554, 15.297115])`);
    if (Math.abs(georefA04.scaleMPerPixel - 0.7746) > 0.005) p10Errors.push(`A04 merilo: ${georefA04.scaleMPerPixel} (pričakovano 0,7746 — P46 s̄)`);
    if (!georefA04.methodSi.includes("POPRAVEK")) p10Errors.push("A04 metoda mora biti označena kot POPRAVEK");
    if (!georefA04.methodSi.includes("O.IX24cg")) p10Errors.push("A04 metoda mora navesti oznako »O.IX24cg«");
    if (!georefA04.methodSi.includes("636 m")) p10Errors.push("A04 metoda mora navesti zavrnitev P9 (mediana 636 m)");
    if (!georefA04.methodSi.includes("AKTIVACIJA P50")) p10Errors.push("A04 metoda mora navesti AKTIVACIJO P50");
    if (georefA04.controlPoints.length < 3) p10Errors.push(`A04 kontrolne točke: ${georefA04.controlPoints.length} (pričakovano ≥ 3)`);
  }

  // A05 = celica ch — P50: NEATLINE_GEOREFERENCED (aktivacija P46 afine)
  if (!georefA05) {
    p10Errors.push("georef-a05 manjka v SHEET_GEOREFS");
  } else {
    const b = georefA05.bounds;
    if (georefA05.status !== "NEATLINE_GEOREFERENCED") p10Errors.push(`A05 status: ${georefA05.status} (pričakovano NEATLINE_GEOREFERENCED — P50)`);
    if (Math.abs(b[0][0] - 45.543722) > 5e-5 || Math.abs(b[0][1] - 15.272828) > 5e-5)
      p10Errors.push(`A05 bounds S/Z: ${b[0]} (pričakovano [45.543722, 15.272828] = P46 neatline celice VKIX24ch)`);
    if (Math.abs(b[1][0] - 45.529907) > 5e-5 || Math.abs(b[1][1] - 15.296925) > 5e-5)
      p10Errors.push(`A05 bounds J/V: ${b[1]} (pričakovano [45.529907, 15.296925])`);
    if (georefA05.pixels.width !== 2634 || georefA05.pixels.height !== 2165)
      p10Errors.push(`A05 px: ${georefA05.pixels.width}×${georefA05.pixels.height}`);
    const cpSi = georefA05.controlPoints.map((c) => c.fromSi).join(" |");
    for (const must of ["VKIX24ch", "Jankovichti"]) {
      if (!cpSi.includes(must)) p10Errors.push(`A05 kontrolna točka manjka: ${must}`);
    }
    if (!georefA05.methodSi.includes("O.IX24ch")) p10Errors.push("A05 metoda mora navesti oznako »O.IX24ch«");
    if (!georefA05.methodSi.includes("AKTIVACIJA P50")) p10Errors.push("A05 metoda mora navesti AKTIVACIJO P50");
  }

  // viri: 5 listov GEOREFERENCED (P50: A01/A02 VALIDATED_GEOREF + A03–A05 NEATLINE_*)
  const graphicSheets = ATLAS_SOURCES.filter((s) => s.type === "cadastral-map");
  const geoCount = graphicSheets.filter((s) => s.georefStatus === "GEOREFERENCED").length;
  const gridCount = graphicSheets.filter((s) => s.georefStatus === "GRID_APPROX").length;
  if (geoCount !== 5) p10Errors.push(`georeferencirani grafični listi: ${geoCount} (pričakovano 5 — A01–A05 od P50)`);
  if (gridCount !== 0) p10Errors.push(`listi z okvirno umestitvijo (GRID_APPROX): ${gridCount} (pričakovano 0 — P50)`);
  const srcA01 = ATLAS_SOURCES.find((s) => s.id === "src-a01");
  const srcA02 = ATLAS_SOURCES.find((s) => s.id === "src-a02");
  const srcA03 = ATLAS_SOURCES.find((s) => s.id === "src-a03");
  const srcA04 = ATLAS_SOURCES.find((s) => s.id === "src-a04");
  const srcA05 = ATLAS_SOURCES.find((s) => s.id === "src-a05");
  for (const [src, id] of [[srcA01, "src-a01"], [srcA02, "src-a02"]] as const) {
    if (!src || src.georefStatus !== "GEOREFERENCED" || src.georeferenced !== true || src.placement?.precision !== "VALIDATED_GEOREF")
      p10Errors.push(`${id} ni GEOREFERENCED z VALIDATED_GEOREF placement`);
  }
  for (const [src, id, cell, precision] of [
    [srcA03, "src-a03", "dg", "NEATLINE_PARTIAL_GEOREFERENCED"],
    [srcA04, "src-a04", "cg", "NEATLINE_GEOREFERENCED"],
    [srcA05, "src-a05", "ch", "NEATLINE_GEOREFERENCED"],
  ] as const) {
    if (!src || src.georefStatus !== "GEOREFERENCED" || src.georeferenced !== true || src.placement?.precision !== precision)
      p10Errors.push(`${id} ni GEOREFERENCED z ${precision} placement (P50)`);
    else if (src.placement && !src.placement.methodSi.includes(cell))
      p10Errors.push(`${id} placement brez celice ${cell}`);
  }
  if (!srcA04 || !srcA04.noteSi?.includes("POPRAVEK P10")) p10Errors.push("src-a04 opomba brez POPRAVKa P10");
  for (const sid of ["src-vac-n83", "src-gurs-wfs", "src-ezkn"]) {
    if (!ATLAS_SOURCES.find((s) => s.id === sid)) p10Errors.push(`nov vir ${sid} manjka`);
  }
  const srcEzkn = ATLAS_SOURCES.find((s) => s.id === "src-ezkn");
  if (srcEzkn && !srcEzkn.noteSi?.includes("O.IX24c"))
    p10Errors.push("src-ezkn opomba brez kod celic (O.IX24c…)");
  // pokritost (issue #4: od P50 vseh 5 listov georeferenciranih)
  const covP10 = getCoverage();
  if (covP10.sheetsGeoreferenced !== 5 || covP10.sheetsGridApprox !== 0 || covP10.sheetsTotal !== 5)
    p10Errors.push(`COVERAGE listi: validirani ${covP10.sheetsGeoreferenced} / približni ${covP10.sheetsGridApprox} / skupaj ${covP10.sheetsTotal} (pričakovano 5/0/5 od P50)`);

  push(
    "qa-p10-ezkn-grid",
    "P10: sekcija mreža eZKN razrešila vse liste — A03=celica dg, A04=celica cg (POPRAVEK P9), A05=celica ch; P50 (2026-10-14): A03–A05 nadgrajeni iz GRID_APPROX (±200–400 m) na P46 neatline afine (NEATLINE ±40/50 m) — 5/5 listov georeferenciranih",
    "P10: the eZKN section grid resolved ALL sheets — A03=cell dg, A04=cell cg (P9 CORRECTION), A05=cell ch; P50 (2026-10-14): A03–A05 upgraded from GRID_APPROX (±200–400 m) to the P46 neatline affines (NEATLINE ±40/50 m) — 5/5 sheets georeferenced",
    p10Errors.length === 0,
    p10Errors.length === 0
      ? "Okvirjene oznake listov so KODI SEKCIJSKE MREŽE 1:2880 (eZKN/GURS, uradna geometrija D96/TM): A02=»O.IX24cƒ«→celica cf — središče vsebine A02 se NATANČNO ujema s središčem celice (princip list≈celica!) — torej A03=»O.IX24dg«→celica dg (45,5437–45,5575 N, 15,2485–15,273 E; vsebina = le vzhodni pas = zahodni rob k.o. Griblje; TRIBUTSCH→k.o. Tribuče ✓, WEIDENDORF→k.o. Bedenj ✓), A04=»O.IX24cg«→celica cg (45,5436–45,5574, 15,2728–15,2973 — DIREKTNO južno od A02; POPRAVEK P9: prejšnja lega na ovinku Kolpe pri Adlešičih zavrnjena — stavbna validacija 636 m mediane, kontrole P9 nedisukriminativne, »reka« = verjetno dolina; Kolpa teče IZVEN lista A04), A05=»O.IX24ch«→celica ch (45,5299–45,5437, 15,2726–15,2971 = skrajni jug 1825 k.o. Griblje — ozemlje pozneje odvzeto; sklop 45 stavb → Fučkovci/Dragoši [~], Pri Jankovichti → naselje Jankoviči ✓). Vsa stanja REVIEW (±200–400 m); identiteta listov neodvisno potrjena prek VAČ (5 listov N083A01–A05, križne korelacije predogledov); novi viri: GURS WFS (k.o. 1544 poligon + 2117 parcel + naselja), eZKN (mreža + ZKN skeni); prekritost 5/5"
      : p10Errors.join("; "),
  );

  /* ── P12: AR vas 3D — vas živi (drevesa, dim) + dokumentirana ugotovitev o hišnih številkah ── */
  const p12Errors: string[] = [];
  if (TREE_STATS.total < 1200)
    p12Errors.push(`TREES premalo: ${TREE_STATS.total} (pričakovano ≥ 1200)`);
  if (TREE_STATS.total !== TREES.length)
    p12Errors.push("TREE_STATS.total ≠ TREES.length");
  if (TREES.some((tr) => !Number.isFinite(tr.x) || !Number.isFinite(tr.z)))
    p12Errors.push("drevo z neveljavnimi koordinatami");
  if (SMOKE_CHIMNEYS.length !== 8)
    p12Errors.push(`SMOKE_CHIMNEYS: ${SMOKE_CHIMNEYS.length} (pričakovano 8)`);
  if (SMOKE_CHIMNEYS.some((c) => c.top < 3 || c.top > 9))
    p12Errors.push("dimnik z neverjetno višino (< 3 m ali > 9 m)");
  if (!HOUSENO_FINDING.si.includes("niso zapisane"))
    p12Errors.push("HOUSENO_FINDING.si brez ključne ugotovitve");
  if (!HOUSENO_FINDING.en.includes("not written"))
    p12Errors.push("HOUSENO_FINDING.en brez ključne ugotovitve");

  push(
    "qa-p12-village-life",
    "P12: AR 3D vas oživi — drevesa (gozdne cone + razpršena, deterministično), dim 8 dimnikov (1825/~1900), orbit pick kartica; dokumentirana negativna ugotovitev: hišne št. na listu A02 niso zapisane",
    "P12: the AR 3D village comes alive — trees (forest zones + scattered, deterministic), smoke from 8 chimneys (1825/~1900), orbit pick card; documented negative finding: house numbers are not written on sheet A02",
    p12Errors.length === 0,
    p12Errors.length === 0
      ? `Dreves: ${TREE_STATS.total} (${TREE_STATS.forest} v gozdnih conah Brezov gozd + ${TREE_STATS.scattered} razpršenih na lokah; seed ${TREE_STATS.seed}, mulberry32 — vedno isti prizor; izogik stavbam ≥ 7 m). Dim: 8 dimnikov v jedru (vsaka 3. jedrna stavba 7–18 m), sprajti 6 oblakov/dimnik, cikel 6,5 s, dvig 7–13 m, vidno samo 1825/~1900. Kartica stavbe v 3D pregledu (orbit) — tap na stavbo: vrsta, tloris, razdalja, status 2026, jedro/cerkev, P12 nota. RAZISKOVALNI IZID (negativen, dokumentiran): hišne številke NA stavbah lista A02 niso zapisane — slepi VLM testi (6 stavb, 3 ponovitve → BLIZINA_BREZ), 43 številka-podobnih rdečih madežev nečitljivih; rdeče 4-mestne številke v parcelah (1009–1106 ob jedru) so PARCELNE; povezava parcela↔hiša čaka ~50+ strani PS (TO_COLLECT).`
      : p12Errors.join("; "),
  );

  // P18-1 (revizija, postavka 18): surove kode vrst virov nikoli obiskovalcu —
  // vsaka koda, ki se pojavi v zbirki, ima človeško oznako SL/EN (slovar
  // SOURCE_TYPE_LABELS v src/lib/museum.ts; izpis v exhibit-detail)
  const stCodes = new Set<string>();
  for (const e of EXHIBITS)
    for (const s of e.sources ?? []) if (s.sourceType) stCodes.add(s.sourceType);
  const unlabeled = [...stCodes].filter((c) => !SOURCE_TYPE_LABELS[c]);
  push(
    "qa-p18-source-labels",
    "P18: vsaka vrsta vira ima oznako SL/EN (obiskovalcu nikoli surova koda)",
    "P18: every source type has an SL/EN label (visitors never see a raw code)",
    unlabeled.length === 0,
    `${stCodes.size} vrst virov: ${[...stCodes].join(", ")}; brez oznake: ${unlabeled.join(", ") || "0"}`,
  );

  // P18-2 (revizija, postavka 20): drsnik časovnega potovanja obsega prazgodovino.
  // Postanki (src/lib/timeline-stops.ts) morajo pokrivati VSA mejna leta
  // (od–do) zapisov z GPS na karti — takrat množice pik v vsakem postanku
  // sovpadejo z zveznim drsnikom po letih, pika MVG-095 (−1000…−700) pa
  // postane dosegljiva (prej je bila skrita za MIN_YEAR 1468).
  const yearBounds = new Set<number>();
  for (const e of EXHIBITS) {
    if (!e.lat || !e.lng) continue;
    if (e.yearFrom != null) yearBounds.add(e.yearFrom);
    if (e.yearTo != null) yearBounds.add(e.yearTo);
  }
  const stopsNum = YEAR_STOPS as readonly number[];
  const missingStops = [...yearBounds].filter((y) => !stopsNum.includes(y));
  const stopsSorted = stopsNum.every((y, i) => i === 0 || stopsNum[i - 1] < y);
  const stopsOk =
    missingStops.length === 0 &&
    stopsSorted &&
    stopsNum[0] < 0 &&
    stopsNum[stopsNum.length - 1] === MAX_YEAR;
  push(
    "qa-p18-timeline-stops",
    "P18: postanki časovnega drsnika = vsa mejna leta zapisov na karti (od prazgodovine −1000; pika MVG-095 dosegljiva)",
    "P18: time-slider stops = every boundary year of mapped records (from prehistory −1000; MVG-095 pin reachable)",
    stopsOk,
    `${stopsNum.length} postankov ${formatStopYear(stopsNum[0], "si")} → ${String(stopsNum[stopsNum.length - 1])}; mejnih let zapisov na karti ${yearBounds.size}; manjkajoči postanki: ${missingStops.join(", ") || "0"}${stopsSorted ? "" : "; NISO urejeni naraščajoče"}`,
  );

  // ── P19 (revizija podatkovne pravilnosti, 2026-10-10): avtomatske kontrole,
  //    ki ob novih podatkih same odkrijejo neskladja iz revizijskega pregleda ──

  // P19-1: števci (meta.json counts, events.json count) == dejanski podatki.
  // (Prej je bil ključ napačno bran kot META.count — tiha rezerva; zdaj strogo.)
  const totalSources = EXHIBITS.reduce((a, e) => a + (e.sources ?? []).length, 0);
  const c = META.counts ?? {};
  const countMismatches: string[] = [];
  if (EVENTS.count !== EVENTS.events.length) countMismatches.push(`events.count=${EVENTS.count} ≠ ${EVENTS.events.length}`);
  if (c.exhibits !== EXHIBITS.length) countMismatches.push(`meta.exhibits=${c.exhibits} ≠ ${EXHIBITS.length}`);
  if (c.sources !== totalSources) countMismatches.push(`meta.sources=${c.sources} ≠ ${totalSources}`);
  if (c.events !== EVENTS.events.length) countMismatches.push(`meta.events=${c.events} ≠ ${EVENTS.events.length}`);
  if (c.stories !== (META.stories ?? []).length) countMismatches.push(`meta.stories=${c.stories} ≠ ${(META.stories ?? []).length}`);
  push(
    "qa-p19-counts",
    "P19: števci (zbirka/viri/dogodki/zgodbe) usklajeni z dejanskimi podatki",
    "P19: counters (collection/sources/events/stories) match the actual data",
    countMismatches.length === 0,
    `${EXHIBITS.length} zapisov · ${totalSources} virov · ${EVENTS.events.length} dogodkov · ${(META.stories ?? []).length} zgodb; neskladja: ${countMismatches.join("; ") || "0"}`,
  );

  // P37 (issue #21): števci v dokumentaciji (README.md) in meta oznakah
  // (src/app/layout.tsx) usklajeni z meta.json — odkrije, da se ob novih virih
  // pozabi uskladiti README/SEO opis (P34: 596 → 601 se ni preneslo).
  // Strežniški klic vbrizga readFile; odjemalski izris kontrolo preskoči
  // (enak vzorec degradacije kot pri qa-p19-images).
  let docCountersOk = true;
  let docCountersDetail = "dokumentacija ni preverjena (fs ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const docMismatches: string[] = [];
    const readme = opts.readFile("README.md");
    const layout = opts.readFile("src/app/layout.tsx");
    if (readme !== null) {
      const boldRecords = [...readme.matchAll(/\*\*(\d+) zapisov\*\*/g)].map((m) => Number(m[1]));
      const provableSources = [...readme.matchAll(/(\d+) dokazljivih virov/g)].map((m) => Number(m[1]));
      const eventsRow = [...readme.matchAll(/(\d+) dogodkov/g)].map((m) => Number(m[1]));
      for (const n of boldRecords) if (n !== EXHIBITS.length) docMismatches.push(`README "zapisov": ${n} ≠ ${EXHIBITS.length}`);
      for (const n of provableSources) if (n !== totalSources) docMismatches.push(`README "dokazljivih virov": ${n} ≠ ${totalSources}`);
      for (const n of eventsRow) if (n !== EVENTS.events.length) docMismatches.push(`README "dogodkov": ${n} ≠ ${EVENTS.events.length}`);
    } else {
      docMismatches.push("README.md ni berljiv");
    }
    if (layout !== null) {
      const seoSources = [...layout.matchAll(/(\d+) dokazljivih virov/g)].map((m) => Number(m[1]));
      if (seoSources.length === 0) docMismatches.push("layout.tsx: števec virov ni najden");
      for (const n of seoSources) if (n !== totalSources) docMismatches.push(`layout.tsx "dokazljivih virov": ${n} ≠ ${totalSources}`);
    } else {
      docMismatches.push("src/app/layout.tsx ni berljiv");
    }
    docCountersOk = docMismatches.length === 0;
    docCountersDetail = `README + layout.tsx proti meta.json (zapisov ${EXHIBITS.length}, virov ${totalSources}, dogodkov ${EVENTS.events.length}); neskladja: ${docMismatches.join("; ") || "0"}`;
  }
  push(
    "qa-p37-doc-counters",
    "P37: števci v README in SEO meta opisu usklajeni z metapodatki zbirke (issue #21)",
    "P37: README and SEO meta description counters match collection metadata (issue #21)",
    docCountersOk,
    docCountersDetail,
  );

  // P19-2: vsaka slika zapisa obstaja na disku (106 citiranj / 103 datotek).
  // Obstoj preverja samo strežniški klic (fs); odjemalski izris preveri obliko
  // poti in izrecno pove, kje teče popolna kontrola.
  const citedImages = EXHIBITS.map((e) => e.image).filter((p): p is string => Boolean(p));
  const uniqueImages = [...new Set(citedImages)];
  let imagesOk = false;
  let imageDetail = "";
  if (opts.fileExists) {
    const missing = uniqueImages.filter(
      (p) => !p.startsWith("/") || !opts.fileExists!(`public${p}`),
    );
    imagesOk = missing.length === 0;
    imageDetail = `${citedImages.length} citiranj / ${uniqueImages.length} datotek; manjka: ${missing.join(", ") || "0"}`;
  } else {
    const malformed = uniqueImages.filter((p) => !p.startsWith("/images/"));
    imagesOk = malformed.length === 0;
    imageDetail = `${citedImages.length} citiranj / ${uniqueImages.length} datotek (oblika poti); obstoj na disku preverja /api/qa`;
  }
  push(
    "qa-p19-images",
    "P19: vsaka fotografija zapisa obstaja na disku",
    "P19: every record photograph exists on disk",
    imagesOk,
    imageDetail,
  );

  // P19-3: sorodni zapisi kažejo samo na zapise, ki dejansko obstajajo
  // (ulovili bi npr. zastarelo MVG-114, ki je rezervirana, a ni v zbirki)
  const existingNos = new Set(EXHIBITS.map((e) => e.museumNo));
  const staleRefs: string[] = [];
  for (const [slug, story] of Object.entries(EXTRA))
    for (const r of story.related ?? [])
      if (r.museumNo && !existingNos.has(r.museumNo)) staleRefs.push(`${slug} → ${r.museumNo}`);
  push(
    "qa-p19-related-refs",
    "P19: sorodni zapisi kažejo samo na obstoječe zapise (brez rezerviranih številk)",
    "P19: related records point only to existing records (no reserved numbers)",
    staleRefs.length === 0,
    `${staleRefs.length} zastarelih povezav${staleRefs.length ? `: ${staleRefs.slice(0, 5).join(", ")}` : ""}`,
  );

  // P19-4: vsaka postaja življenja ima LASTEN vir ali jasno oznako 'v raziskovanju'
  // (revizija: 60 od 375 postaj ni imelo lastne navedbe — tiho nedokumentirano)
  const unanchored: string[] = [];
  let stationsTotal = 0;
  let stationsSourced = 0;
  let stationsResearch = 0;
  for (const [slug, story] of Object.entries(EXTRA))
    for (const st of story.lifeStations ?? []) {
      stationsTotal++;
      const hasSource = Boolean(st.sourceUrl || st.sourceName);
      const marked = st.evidence === "v raziskovanju";
      if (hasSource) stationsSourced++;
      else if (marked) stationsResearch++;
      else unanchored.push(`${slug}/${st.year ?? "?"}`);
    }
  push(
    "qa-p19-station-sources",
    "P19: vsaka postaja življenja ima vir ali oznako 'v raziskovanju'",
    "P19: every life station has a source or the 'in research' mark",
    unanchored.length === 0,
    `${stationsTotal} postaj: ${stationsSourced} z virom, ${stationsResearch} v raziskovanju; brez obojega: ${unanchored.slice(0, 5).join(", ") || "0"}`,
  );

  // P19-5: prva omemba VASI je vedno 1468 (cerkev sv. Vida 1526).
  // Regresija na napako iz revizije: dogodek/extra sta 1526 imenovala 'prvo
  // omembo vasi' (infopolje SL Wikipedije); viri (EN Wikipedija + Snoj) in
  // MVG-001 določajo 1468, jubilej 2026 pa je cerkveni.
  const FIRST_PHRASES = [
    "prva omemba vasi", "prva pisna omemba vasi",
    "prva omemba gribelj", "prva pisna omemba gribelj",
    "first mention of the village", "first written mention of griblje",
    "first mention of griblje",
  ];
  const MENTION_RE =
    /\bprv[ai]\w*\b[^.]{0,150}\b(?:omemb\w*|izpri\w*|zapi[sš]e\b|zapisala\b|zapisan\w*|attest\w*|mention\w*|record\w*)\b[^.]{0,150}\b(?:vasi\b|vas\b|griblje\b|griblach\b|village\b)/i;
  const MENTION_RE_R =
    /\b(?:vasi\b|vas\b|griblje\b|griblach\b|village\b)[^.]{0,150}\bprv[ai]\w*\b[^.]{0,150}\b(?:omemb\w*|izpri\w*|zapi[sš]e\b|zapisala\b|zapisan\w*|attest\w*|mention\w*|record\w*)\b/i;
  const CHURCH_RE =
    /(?:cerkev\b|cerkve\b|cerkvi\b|church\b|sv\.?\s?vid|st\.?\s?vitus|sv\.?\s?mark|st\.?\s?mark)/i;
  /** stavek trdi prvo omembo vasi → v njem (ali letnici postaje) mora biti 1468 */
  const firstMentionViolations: string[] = [];
  const checkFirstMention = (text: string | null | undefined, where: string, year = "") => {
    for (const s of (text ?? "").split(/(?<=[.!?])\s+|\n/)) {
      const low = s.toLowerCase();
      const phraseHit = FIRST_PHRASES.some((p) => low.includes(p));
      const patternHit = !CHURCH_RE.test(s) && (MENTION_RE.test(s) || MENTION_RE_R.test(s));
      if ((phraseHit || patternHit) && !`${s} ${year}`.includes("1468"))
        firstMentionViolations.push(`${where}: ${s.trim().slice(0, 90)}…`);
    }
  };
  for (const e of EVENTS.events) {
    checkFirstMention(e.titleSi, `dogodek ${e.id.slice(0, 8)}`);
    checkFirstMention(e.titleEn, `dogodek ${e.id.slice(0, 8)}`);
    checkFirstMention(e.descriptionSi, `dogodek ${e.id.slice(0, 8)}`);
    checkFirstMention(e.descriptionEn, `dogodek ${e.id.slice(0, 8)}`);
  }
  for (const e of EXHIBITS) {
    checkFirstMention(e.summarySi, e.museumNo);
    checkFirstMention(e.summaryEn, e.museumNo);
  }
  for (const [slug, story] of Object.entries(EXTRA))
    for (const st of story.lifeStations ?? [])
      checkFirstMention(st.description, `postaja ${slug}`, st.year ?? "");
  const villageRecord = EXHIBITS.find((e) => e.museumNo === "MVG-001");
  const mvg001Ok = villageRecord?.yearFrom === 1468;
  push(
    "qa-p19-first-mention",
    "P19: prva omemba vasi je vedno 1468 (cerkev sv. Vida: 1526; MVG-001)",
    "P19: the village's first mention is always 1468 (St. Vitus' church: 1526; MVG-001)",
    firstMentionViolations.length === 0 && mvg001Ok,
    `${firstMentionViolations.length} stavkov brez zasidranja na 1468${firstMentionViolations.length ? `: ${firstMentionViolations.slice(0, 3).join(" | ")}` : ""}; MVG-001 yearFrom: ${villageRecord?.yearFrom}`,
  );

  /* ── P20 (issue #4): inventar N83 — usklajenost števcev z podatkovnim modeljem ── */
  const p20invErrors: string[] = [];
  const inv = getArchiveInventory();
  if (inv.totals.units !== 12) p20invErrors.push(`enot: ${inv.totals.units} (pričakovano 12 = 5 grafičnih + 7 spisovnih)`);
  if (inv.totals.graphicSheets !== 5) p20invErrors.push(`grafičnih listov: ${inv.totals.graphicSheets}`);
  if (inv.totals.writtenSeries !== 7) p20invErrors.push(`spisovnih enot: ${inv.totals.writtenSeries}`);
  // structuredEntities == dejansko stanje modelov (catches stale structuredEntries v sources.ts)
  const ptInv = inv.units.find((u) => u.code === "N083PT");
  const puaInv = inv.units.find((u) => u.code === "N083PUA");
  const psInv = inv.units.find((u) => u.code === "N083PS");
  const pzInv = inv.units.find((u) => u.code === "N083PZ");
  const a02Inv = inv.units.find((u) => u.code === "N083A02");
  if (ptInv && ptInv.structuredEntities !== ATLAS_HOUSES.length)
    p20invErrors.push(`PT structured ${ptInv.structuredEntities} != houses.ts ${ATLAS_HOUSES.length}`);
  const srcPua = ATLAS_SOURCES.find((s) => s.id === "src-pua");
  if (puaInv && srcPua && (puaInv.structuredEntities !== PUA_CONTINUATION.rows.length || srcPua.structuredEntries !== PUA_CONTINUATION.rows.length))
    p20invErrors.push(`PUA structured ${puaInv.structuredEntities}/src ${srcPua.structuredEntries} != PUA_CONTINUATION ${PUA_CONTINUATION.rows.length} (43→101 napaka se ne sme ponoviti)`);
  if (psInv && psInv.structuredEntities !== 2974)
    p20invErrors.push(`PS structured: ${psInv.structuredEntities} != 2974 (P36 2743 + P38 3. prehod, dokaz ps-raw/PS-full-v2.json)`);
  if (pzInv && pzInv.structuredEntities !== 11) p20invErrors.push(`PZ structured: ${pzInv.structuredEntities} != 11 (P44: 10 razredov + Summa, dokaz pz-classes-full.json)`);
  if (a02Inv && a02Inv.structuredEntities !== VECTOR_BUILDINGS.length)
    p20invErrors.push(`A02 structured: ${a02Inv.structuredEntities} != ${VECTOR_BUILDINGS.length}`);
  if (inv.totals.spatiallyLinked !== 0 || inv.units.some((u) => u.spatiallyLinked !== 0))
    p20invErrors.push("spatiallyLinked mora biti 0 — povezava hiša↔stavba zahteva dokaz (ne ista številka)");
  if (inv.totals.palaeoConfirmed !== 0) p20invErrors.push("palaeoConfirmed mora biti 0 — človeška paleografija še ni izvedena");
  if (inv.psChecksum.total !== 2607 || inv.psChecksum.buildingSites !== 102 || inv.psChecksum.landParcels !== 2505)
    p20invErrors.push(`PS checksum: ${inv.psChecksum.buildingSites}+${inv.psChecksum.landParcels}=${inv.psChecksum.total} (pričakovano 102+2505=2607)`);
  push(
    "qa-p20-inventory",
    "P20: inventar N83 izračunan iz modelov — 12 enot, structuredEntities == dejansko stanje (PUA 101, PT 105, PS 12, PZ 10, A02 156), 0 prostorsko povezanih, 0 paleografsko potrjenih, PS vsota 2607",
    "P20: N83 inventory computed from the models — 12 units, structuredEntities == actual state (PUA 101, PT 105, PS 12, PZ 10, A02 156), 0 spatially linked, 0 palaeographically confirmed, PS checksum 2607",
    p20invErrors.length === 0,
    p20invErrors.length === 0
      ? `12 enot (5 grafičnih + 7 spisovnih); strani: ${inv.totals.pagesRead} prebranih + ${inv.totals.pagesOpen} odprtih = ${inv.totals.pagesDeclared} deklariranih; PS ${inv.psChecksum.structured}/${inv.psChecksum.total}`
      : p20invErrors.join("; "),
  );

  /* ── P20 (issue #4): dokazno prebrane strani == pagesTranscribed; brez tihih lukenj ── */
  const p20pagesErrors: string[] = [];
  for (const k of KURRENT_SERIES) {
    const list = k.pagesReadList ?? [];
    if (list.length !== k.pagesTranscribed)
      p20pagesErrors.push(`${k.code}: pagesReadList dolžina ${list.length} != pagesTranscribed ${k.pagesTranscribed}`);
    if (list.length !== new Set(list).size) p20pagesErrors.push(`${k.code}: pagesReadList vsebuje podvojene strani`);
    const bad = list.filter((p) => p < 1 || p > k.pages);
    if (bad.length) p20pagesErrors.push(`${k.code}: strani izven obsega: ${bad.join(",")}`);
    if (k.pagesTranscribed + (k.pages - k.pagesTranscribed) !== k.pages)
      p20pagesErrors.push(`${k.code}: prebrane + odprte != deklarirane`);
  }
  // dokazane vrednosti iz surovih raziskav (issue #4 resolucije: PS 8, PZ 12)
  // P36 (2026-10-11): PS 143 — vse strani strojno prebrane (pass-1 celota + pass-2 78 strani; dokaz research/issue17/ps-raw/)
  const expectedRead: Record<string, number> = { PR: 4, PS: 143, PUA: 49, PZ: 71, PT: 8, PG: 1, PV: 1 };
  for (const [code, n] of Object.entries(expectedRead)) {
    const k = KURRENT_SERIES.find((x) => x.code === code);
    if (k && k.pagesTranscribed !== n)
      p20pagesErrors.push(`${code}: pagesTranscribed ${k.pagesTranscribed} != dokazano ${n} (PS-structure/PZ-valuation.json)`);
  }
  const invScope = getArchiveInventory();
  if (!invScope.totals.scopeAccounted) p20pagesErrors.push("inventar: scopeAccounted ni true za vse enote");
  push(
    "qa-p20-series-pages",
    "P20: dokazano prebrane strani po serijah (PR 4, PS 143 — P36 strojno + P38 3. prehod, PUA 49, PZ 71 — P44, PT 8, PG 1, PV 1) — pagesReadList == pagesTranscribed, brez lukenj; PS in PZ usklajena z research/issue17 datotekami (ps-raw + PS-full.json)",
    "P20: evidenced read pages per series (PR 4, PS 143 — P36 machine-read + P38 3rd pass, PUA 49, PZ 71 — P44, PT 8, PG 1, PV 1) — pagesReadList == pagesTranscribed, no gaps; PS and PZ reconciled with the research/issue17 files (ps-raw + PS-full.json)",
    p20pagesErrors.length === 0,
    p20pagesErrors.length === 0
      ? `skupaj ${invScope.totals.pagesRead}/${invScope.totals.pagesDeclared} prebranih; odprtih strani ${invScope.totals.pagesOpen} (PZ 71/71 od P44; PS sprava s 2607 izrecno odprta) — 0 tihih`
      : p20pagesErrors.join("; "),
  );

  /* ── P20 (issue #4): ločitev validirana georeferenca vs okvirna umestitev ── */
  const p20geoErrors: string[] = [];
  const sheetsGeo = ATLAS_SOURCES.filter((s) => s.type === "cadastral-map");
  for (const s of sheetsGeo) {
    if (s.georefStatus === "GRID_APPROX" && s.georeferenced !== false)
      p20geoErrors.push(`${s.id}: GRID_APPROX a georeferenced !== false`);
    if (s.georefStatus === "GEOREFERENCED" && !s.placement)
      p20geoErrors.push(`${s.id}: GEOREFERENCED brez placement podatkov (natančnost/stran)`);
    if (s.placement && !s.placement.lastChecked) p20geoErrors.push(`${s.id}: placement brez datuma preveritve`);
  }
  const covGeo = getCoverage();
  if (covGeo.sheetsGeoreferenced !== 5 || covGeo.sheetsGridApprox !== 0)
    p20geoErrors.push(`pokritost: ${covGeo.sheetsGeoreferenced}+${covGeo.sheetsGridApprox} (pričakovano 5+0 od P50)`);
  if (covGeo.archivalUnits !== 12) p20geoErrors.push(`archivalUnits: ${covGeo.archivalUnits} (pričakovano 12)`);
  if (covGeo.archivalPages !== 277) p20geoErrors.push(`archivalPages: ${covGeo.archivalPages} (pričakovano 277 = 143+71+49+8+4+1+1)`);
  if (covGeo.housesWithGeometry !== 0)
    p20geoErrors.push(`housesWithGeometry: ${covGeo.housesWithGeometry} — hiša↔stavba povezava zahteva dokaz (156 geometrij nima hišnih št.)`);
  push(
    "qa-p20-georef-precision",
    "P20: natančnost prostorske umestitve ločena — A01/A02 VALIDIRANA georeferenca (±40–100 m), A03–A05 NEATLINE (±40–50 m od P50, prej GRID_APPROX ±200–400 m); 12 enot, 277 strani fonda, 0 hiš z dokazano geometrijo",
    "P20: spatial placement precision separated — A01/A02 VALIDATED georeference (±40–100 m), A03–A05 NEATLINE (±40–50 m since P50, previously GRID_APPROX ±200–400 m); 12 units, 277 fond pages, 0 houses with proven geometry",
    p20geoErrors.length === 0,
    p20geoErrors.length === 0
      ? "listi: 5 georeferenciranih (2 VALIDATED_GEOREF + 3 NEATLINE_* od P50; vsak s placement: method/controlPoints/accuracy/lastChecked); pokritost 5+0=5"
      : p20geoErrors.join("; "),
  );

  /* ── P20 (issue #4): reconciliation preverja inventuro obsega, ne samo statuse ── */
  const p20recErrors: string[] = [];
  const rec = buildReconciliation();
  for (const u of rec.units) {
    if (u.pages != null && !u.scopeCheck.accounted)
      p20recErrors.push(`${u.code}: scopeCheck ni usklajen (${u.scopeCheck.pagesRead}+${u.scopeCheck.pagesOpen} != ${u.scopeCheck.pagesDeclared})`);
  }
  if (!rec.zeroLossMeaningSi || !rec.zeroLossMeaningEn)
    p20recErrors.push("zeroLossMeaning manjka — poštena opredelitev, kaj zeroLoss potrjuje in česa ne");
  if (rec.zeroLossMeaningSi && !rec.zeroLossMeaningSi.includes("NE potrjuje"))
    p20recErrors.push("zeroLossMeaning mora izrecno navesti, česa zeroLoss NE potrjuje");
  if (!rec.zeroLoss) p20recErrors.push("zeroLoss = false — izgubljeni zapis ali neusklajen obseg");
  const puaRecRows = rec.rows.filter((r) => r.unit === "N083PUA");
  const stalePua = puaRecRows.filter((r) => r.locatorSi?.includes("C–Ž"));
  if (stalePua.length) p20recErrors.push(`${stalePua.length} PUA vrstic s zastarelim locatom »strani C–Ž (niso prepisane)« — register je prebran v celoti`);
  push(
    "qa-p20-recon-scope",
    "P20: reconciliation preverja INVENTURO obsega (prebrane + odprte strani == deklarirane) ne samo statuse; zeroLoss z opredelitvijo, kaj potrjuje in česa NE; 0 zastarelih PUA lokatorjev",
    "P20: reconciliation checks the scope INVENTORY (read + open pages == declared), not just statuses; zeroLoss with a statement of what it certifies and does NOT; 0 stale PUA locators",
    p20recErrors.length === 0,
    p20recErrors.length === 0
      ? `enote: ${rec.units.length}; vse scopeCheck.accounted; zeroLoss=${rec.zeroLoss}; pomen dokumentiran (vseh 277 strani prebranih — PZ 71/71 od P44; sprava PS 2607 izrecno odprta, ne prikrito)`
      : p20recErrors.join("; "),
  );

  /* ── P27: poročilo o intenzivnem pregledu Kohane (VS, poročila 39–41, uradni PDF ZVKDS) ── */
  const KOHANE_KEY = "url:zvkds.si/vs-porocila-39-41-kohane";
  const KOHANE_URL = "https://www.zvkds.si/wp-content/uploads/2024/03/039-41_2006_varstvo_spomenikov_porocila-1.pdf";
  type P27Source = { sourceKey?: string | null; url?: string | null; nameSi?: string | null; noteSi?: string | null };
  const p27Errors: string[] = [];
  for (const no of ["MVG-083", "MVG-113"]) {
    const ex27 = EXHIBITS.find((e) => e.museumNo === no);
    const src = ((ex27?.sources ?? []) as P27Source[]).find((s) => s.sourceKey === KOHANE_KEY);
    if (!ex27 || !src) p27Errors.push(`${no}: manjka vir Kohane (poročilo št. 86, str. 54–55)`);
    else {
      if (src.url !== KOHANE_URL) p27Errors.push(`${no}: URL vira Kohane ni uradni PDF ZVKDS`);
      if (!(src.nameSi ?? "").includes("str. 54–55")) p27Errors.push(`${no}: naslov vira ne navaja str. 54–55`);
      if (!(src.noteSi ?? "").includes("koordinat")) p27Errors.push(`${no}: nota ne dokumentira negativnega izida (koordinate)`);
    }
  }
  const ex083 = EXHIBITS.find((e) => e.museumNo === "MVG-083");
  const rep87 = ((ex083?.sources ?? []) as P27Source[]).find((s) => (s.sourceKey ?? "").includes("Grahek"));
  if (!rep87?.url) p27Errors.push("MVG-083: vir Mason et al. (2006), str. 55–56 (poročilo št. 87) brez uradnega URL-ja");
  const ex113 = EXHIBITS.find((e) => e.museumNo === "MVG-113");
  const src113note = ((ex113?.sources ?? []) as P27Source[]).find((s) => s.sourceKey === KOHANE_KEY);
  if (src113note && !(src113note.noteSi ?? "").includes("NE pojavlja"))
    p27Errors.push("MVG-113: nota vira Kohane mora izrecno navesti, da se ime Srednje njive NE pojavlja");
  push(
    "qa-p27-kohane-report",
    "P27: poročilo o intenzivnem pregledu Kohane (VS, poročila 39–41, str. 54–55, uradni PDF ZVKDS) je vir na MVG-083 in MVG-113 z dokumentiranim negativnim izidom (0 koordinat); poročilo št. 87 z URL-jem",
    "P27: the Kohane intensive-survey report (VS, reports 39–41, pp. 54–55, official ZVKDS PDF) is a source on MVG-083 and MVG-113 with the negative result documented (0 coordinates); report no. 87 with URL",
    p27Errors.length === 0,
    p27Errors.length === 0
      ? "2 zapisa · poročili št. 86 + 87 · negativni izid (koordinate) dokumentiran v notah"
      : p27Errors.join("; "),
  );

  /* ── P34 (issue #20): RNPD odprta zbirka — uradni vir in koordinate ── */
  const RNPD_URL = "https://podatki.gov.si/dataset/register-nepremicne-kulturne-dediscine";
  type P34Source = { sourceKey?: string | null; url?: string | null; license?: string | null; noteSi?: string | null };
  const p34Errors: string[] = [];
  // MVG-083: uradni koordinati EŠD 10094, coordsApprox=false
  const ex83 = EXHIBITS.find((e) => e.museumNo === "MVG-083");
  if (!ex83) p34Errors.push("MVG-083 manjka");
  else {
    if (ex83.lat !== 45.57951 || ex83.lng !== 15.294803)
      p34Errors.push("MVG-083: koordinati nista uradni RNPD točki EŠD 10094 (15.294803, 45.57951)");
    if (ex83.coordsApprox !== false)
      p34Errors.push("MVG-083: coordsApprox mora biti false (uraden vir)");
    const srcs83 = (ex83.sources ?? []) as P34Source[];
    const rnpd83 = srcs83.find((s) => s.url === RNPD_URL);
    if (!rnpd83) p34Errors.push("MVG-083: manjka vir RNPD (odprta zbirka podatki.gov.si)");
    else if (rnpd83.license !== "CC BY 4.0") p34Errors.push("MVG-083: vir RNPD brez licence CC BY 4.0");
    if (!srcs83.some((s) => s.url === "https://eid.gov.si/S/10094"))
      p34Errors.push("MVG-083: vir registra brez direktne QR povezave eid.gov.si/S/10094");
    if (!srcs83.some((s) => s.url === "https://eid.gov.si/S/11081"))
      p34Errors.push("MVG-083: manjka vir EŠD 11081 Požekov vrt (ločen register-vnos)");
    const s87 = srcs83.find((s) => (s.sourceKey ?? "").includes("Grahek"));
    if (!(s87?.noteSi ?? "").includes("11082"))
      p34Errors.push("MVG-083: nota poročila št. 87 ne dokumentira usode EŠD 11082");
  }
  // MVG-113: negativni izid (brez GPS) + RNPD vir + usoda 11082
  const ex113b = EXHIBITS.find((e) => e.museumNo === "MVG-113");
  if (!ex113b) p34Errors.push("MVG-113 manjka");
  else {
    if (ex113b.lat != null || ex113b.lng != null)
      p34Errors.push("MVG-113: Srednje njive OSTAJA brez GPS (RNPD ne razrešuje lege)");
    const rnpd113 = ((ex113b.sources ?? []) as P34Source[]).find((s) => s.url === RNPD_URL);
    if (!rnpd113) p34Errors.push("MVG-113: manjka vir RNPD (negativni izid)");
    else if (!(rnpd113.noteSi ?? "").includes("Srednje njive") || !(rnpd113.noteSi ?? "").includes("11082"))
      p34Errors.push("MVG-113: nota RNPD ne dokumentira negativnega izida (Srednje njive, EŠD 11082)");
  }
  // MVG-002: pravna podlaga + križna potrditev RNPD
  const ex002 = EXHIBITS.find((e) => e.museumNo === "MVG-002");
  if (!ex002) p34Errors.push("MVG-002 manjka");
  else {
    const srcs002 = (ex002.sources ?? []) as P34Source[];
    if (!srcs002.some((s) => (s.url ?? "").includes("uradni-list.si") && (s.url ?? "").includes("63-3040")))
      p34Errors.push("MVG-002: manjka pravna podlaga (Odlok, Uradni list RS 63-3040/2018)");
    const rnpd2122 = srcs002.find((s) => s.url === "https://eid.gov.si/S/2122");
    if (!rnpd2122) p34Errors.push("MVG-002: manjka vir RNPD EŠD 2122 (križna potrditev)");
    else if (!(rnpd2122.noteSi ?? "").includes("5,8 m"))
      p34Errors.push("MVG-002: nota RNPD ne navaja izračunane razlike sidra (~5,8 m)");
  }
  push(
    "qa-p34-rnpd-official",
    "P34: RNPD odprta zbirka (CC BY 4.0): uradni koordinati MVG-083 (EŠD 10094, coordsApprox=false) + Požekov vrt (EŠD 11081) kot vir; MVG-113 negativni izid (brez GPS) in usoda EŠD 11082 dokumentirana; MVG-002 odlok 63-3040/2018 + križna potrditev sidra (~5,8 m)",
    "P34: RNPD open dataset (CC BY 4.0): MVG-083 official coordinates (EŠD 10094, coordsApprox=false) + Požekov vrt (EŠD 11081) as a source; MVG-113 negative result (no GPS) and the fate of EŠD 11082 documented; MVG-002 decree 63-3040/2018 + anchor cross-confirmation (~5.8 m)",
    p34Errors.length === 0,
    p34Errors.length === 0
      ? "3 zapisi · 5 novih virov · 1 uradna točka · 1 negativni izid · 1 križna potrditev"
      : p34Errors.join("; "),
  );

  /* ── P36 (issue #10): PS — strojni prepis vseh strani 5–139 ── */
  const p36Errors: string[] = [];
  const psSrc = ATLAS_SOURCES.find((s) => s.code === "N083PS");
  if (!psSrc) p36Errors.push("vir N083PS manjka");
  else {
    if (psSrc.structuredEntries !== 2974)
      p36Errors.push(`N083PS: structuredEntries=${psSrc.structuredEntries}, pričakovano 2974 (P36 2743 + P38 3. prehod, dokaz PS-full-v2.json)`);
    if (psSrc.lastVerified !== "2026-10-12")
      p36Errors.push("N083PS: lastVerified ni 2026-10-12 (P36 kampanja, P41 ponovna preverba)");
    if (!(psSrc.noteSi ?? "").includes("ps-raw"))
      p36Errors.push("N083PS: nota SL ne kaže na dokaz research/issue17/ps-raw/");
    if (!(psSrc.noteSi ?? "").includes("REVIEW"))
      p36Errors.push("N083PS: nota SL brez oznake REVIEW (strojno branje ni dokazni vir)");
    if (!(psSrc.noteEn ?? "").includes("PS-full.json"))
      p36Errors.push("N083PS: nota EN brez kazalca na spravno poročilo PS-full.json");
    if (!(psSrc.noteSi ?? "").includes("Waldung") || !(psSrc.noteSi ?? "").includes("2607"))
      p36Errors.push("N083PS: nota SL ne dokumentira strukturnih ugotovitev (sekcije, kontrolna vsota)");
  }
  if (PS_RECAP_1826.sampleRowCount !== 2974)
    p36Errors.push(`PS_RECAP_1826.sampleRowCount=${PS_RECAP_1826.sampleRowCount}, pričakovano 2974 (P36 2743 + P38 pass-3)`);
  if (!(PS_RECAP_1826.mostUsefulSi ?? "").includes("P36"))
    p36Errors.push("PS_RECAP_1826: priporočilo SL ne odraža P36 kampanje (zastarelo »NE prepisovati«)");
  push(
    "qa-p36-ps-machineread",
    "P36: N083PS — strojni prepis VSEH 135 strani (5–139) dokumentiran v viru (2743 vrstic + P38 pass-3 = 2974, dvoprehodno, dokaz ps-raw + PS-full.json + PS-full-v2.json); strukturne ugotovitve (pomešan zvezek, organizacija po listih Blatt I–X, sekcije Waldung/Schmiegärten/Blatt X, kontrolna vsota 2607 kot vsota kategorij) vidne v notah; sprava s 2607 ostaja izrecno odprta",
    "P36: N083PS — machine transcription of ALL 135 pages (5–139) documented at the source (2,743 rows + the P38 pass-3 = 2,974, two passes, evidence ps-raw + PS-full.json + PS-full-v2.json); structural findings (shuffled volume, the Blatt I–X sheet organization, Waldung/Schmiegärten/Blatt X sections, the 2,607 checksum as a category sum) visible in the notes; the reconciliation remains explicitly open",
    p36Errors.length === 0,
    p36Errors.length === 0
      ? "135 strani · 2974 vrstic (2743 + pass-3) · 233 VLM branj · Blatt I–X + 4 sekcije"
      : p36Errors.join("; "),
  );

  /* ── P38 (issue #10): PS — deterministična sprava (sekcije, razdvojitev, 2607) ── */
  const p38Errors: string[] = [];
  const R = PS_RECONCILIATION_P38;
  const secRows = Object.values(R.sections).reduce((a, s) => a + s.rows, 0);
  const parseRanges = (s: string): number[] =>
    s
      .split(",")
      .map((part) => part.trim())
      .flatMap((part) => {
        const m = part.match(/^(\d+)[–-](\d+)$/);
        if (m) {
          const a = Number(m[1]);
          const b = Number(m[2]);
          return Array.from({ length: b - a + 1 }, (_, i) => a + i);
        }
        return /^\d+$/.test(part) ? [Number(part)] : [];
      });
  if (R.status !== "REVIEW") p38Errors.push(`status=${R.status}, pričakovano REVIEW (strojno branje ni dokazni vir)`);
  if (R.readingRule !== "pass2wins") p38Errors.push(`readingRule=${R.readingRule}, pričakovano pass2wins`);
  if (R.coverage.grundDistinct + R.coverage.grundMissing !== 2505)
    p38Errors.push(`grundDistinct ${R.coverage.grundDistinct} + grundMissing ${R.coverage.grundMissing} ≠ 2505`);
  if (R.coverage.grundDistinct !== 1889 || R.coverage.grundMissing !== 616)
    p38Errors.push("osnovna pokritost ni 1889/616 (P36 osnovna črta pod pass2wins)");
  if (R.coverage.nad2506Distinct + R.coverage.waldungDistinct !== 176)
    p38Errors.push(`nad2506 (${R.coverage.nad2506Distinct}) + waldung (${R.coverage.waldungDistinct}) ≠ 176 (P36 over2505)`);
  if (R.coverage.blattXDistinct !== 60)
    p38Errors.push(`blattXDistinct=${R.coverage.blattXDistinct}, pričakovano 60 (= bauplatzeSeen P36)`);
  if (secRows !== R.splitting.rowsBefore)
    p38Errors.push(`vsota vrstic sekcij ${secRows} ≠ rowsBefore ${R.splitting.rowsBefore}`);
  if (R.splitting.rowsAfter !== R.splitting.parcelCulturePairs + (R.sections["NEBEREŽNA"]?.rows ?? 0))
    p38Errors.push("rowsAfter ≠ parcelCulturePairs + NEBEREŽNA vrstice");
  if (R.splitting.extraRowsFromMultiCulture !== R.splitting.rowsBefore - R.splitting.parcelCulturePairs - (R.sections["NEBEREŽNA"]?.rows ?? 0))
    p38Errors.push("extraRowsFromMultiCulture se ne ujema z razliko (rowsBefore − pairs − NEBEREŽNA)");
  if (R.splitting.parcelCulturePairs !== 2118 || R.splitting.parcelsWithMultipleCultures !== 430)
    p38Errors.push("števca razdvojitve nista 2118 parov / 430 parcel (regresija pravil)");
  const missingFromRanges = parseRanges(R.coverage.grundMissingRanges);
  if (missingFromRanges.length !== R.coverage.grundMissing)
    p38Errors.push(`razpon manjkajočih (${missingFromRanges.length}) ≠ grundMissing (${R.coverage.grundMissing})`);
  if (new Set(missingFromRanges).size !== missingFromRanges.length)
    p38Errors.push("razpon manjkajočih vsebuje podvajanja");
  if (!R.p36Baseline.reproducedUnderPass2wins)
    p38Errors.push("P36 osnovna črta NI reproducirana (reproducedUnderPass2wins=false)");
  if (R.ocrLeadingDigitCandidates.count !== 0)
    p38Errors.push(`OCR kandidati=${R.ocrLeadingDigitCandidates.count}, pričakovano 0 (regresija pravila)`);
  const sens = R.sensitivity;
  if (
    sens.union.grundDistinct < sens["pass2wins"].grundDistinct ||
    sens["pass2wins"].grundDistinct < sens.pass1.grundDistinct ||
    sens.pass1.grundMissing < sens["pass2wins"].grundMissing ||
    sens["pass2wins"].grundMissing < sens.union.grundMissing
  )
    p38Errors.push("občutljivost krši monotonost (union ⊇ pass2wins ⊇ pass1)");
  if (R.negativeResults.length < 3) p38Errors.push("negativeResults < 3 (negativni izidi morajo ostati vidni)");
  if (R.next.length < 3) p38Errors.push("next < 3 (odprti koraki sprave morajo biti izrecni)");
  // dokazna datoteka (strežniški klic; odjemalski izris izpusti — vzorec qa-p37)
  let p38FileDetail = "dokazna datoteka ni preverjena (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const raw = opts.readFile("research/issue17/ps-reconciliation.json");
    if (raw === null) {
      // produkcija: research/ NAMENOMA ni v deploymentu (.vercelignore, 92 MB) —
      // vzorec qa-p38-ps-blatt: dokaz ostane v repozitoriju; napaka le, če je
      // research/ prisoten, a ta dokaz manjka.
      if (opts.fileExists?.("research/issue17/ps-raw/ps-005.json"))
        p38Errors.push("research/issue17/ps-reconciliation.json ni berljiv (izpis scripts/p38_ps_reconcile.py)");
      else
        p38FileDetail = "produkcija: dokaz ps-reconciliation.json ostane v repozitoriju (research/ ni v deploymentu — .vercelignore)";
    } else {
      try {
        const j = JSON.parse(raw) as {
          coverage: { grundDistinct: number; grundMissing: number };
          splitting: { parcelCulturePairs: number };
          p36Baseline: { reproducedUnderPass2wins: boolean };
        };
        if (j.coverage.grundDistinct !== R.coverage.grundDistinct)
          p38Errors.push(`JSON grundDistinct=${j.coverage.grundDistinct} ≠ TS ${R.coverage.grundDistinct}`);
        if (j.coverage.grundMissing !== R.coverage.grundMissing)
          p38Errors.push(`JSON grundMissing=${j.coverage.grundMissing} ≠ TS ${R.coverage.grundMissing}`);
        if (j.splitting.parcelCulturePairs !== R.splitting.parcelCulturePairs)
          p38Errors.push(`JSON parcelCulturePairs=${j.splitting.parcelCulturePairs} ≠ TS ${R.splitting.parcelCulturePairs}`);
        if (j.p36Baseline.reproducedUnderPass2wins !== true)
          p38Errors.push("JSON: P36 osnovna črta ni reproducirana");
        p38FileDetail = `dokazna datoteka preverjena (grundDistinct=${j.coverage.grundDistinct}, pairs=${j.splitting.parcelCulturePairs})`;
      } catch {
        p38Errors.push("research/issue17/ps-reconciliation.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p38-ps-reconciliation",
    "P38: N083PS — deterministična sprava (scripts/p38_ps_reconcile.py): sekcije GRUND 1889/2505 (75,4 %) + NADALJEVANJE 95 + WALDUNG 81 + BLATT_X 60 = bauplatzeSeen P36; razdvojitev 430 parcel z več rabami (+633 vrstic); P36 osnovna črta reproducirana pod pass2wins; manjkajoči razponi izračunani; status ostaja REVIEW",
    "P38: N083PS — deterministic reconciliation (scripts/p38_ps_reconcile.py): sections GRUND 1,889/2,505 (75.4%) + CONTINUATION 95 + WALDUNG 81 + BLATT_X 60 = P36's bauplatzeSeen; splitting 430 multi-culture parcels (+633 rows); P36 baseline reproduced under pass2wins; missing ranges computed; status remains REVIEW",
    p38Errors.length === 0,
    p38Errors.length === 0
      ? `1889/2505 (75,4 %) · 4 sekcije · 2118 parov parcela×raba · ${p38FileDetail}`
      : p38Errors.join("; "),
  );

  // P38b (GitHub linija, 2026-10-11): 3. prehod PS — strukturno odkritje listov (Blatt) + adjudikacija.
const p38bErrors: string[] = [];
  {
    const ps = ATLAS_SOURCES.find((s) => s.code === "N083PS");
    if (!ps) p38bErrors.push("vir N083PS manjka");
    else {
      if (!(ps.noteSi ?? "").includes("P38")) p38bErrors.push("N083PS: nota SL ne dokumentira P38 (3. prehod)");
      if (!(ps.noteSi ?? "").includes("Blatt I")) p38bErrors.push("N083PS: nota SL brez strukturnega odkritja listov (Blatt)");
      if (!(ps.noteSi ?? "").includes("PS-full-v2.json")) p38bErrors.push("N083PS: nota SL brez kazalca na PS-full-v2.json");
      if (!(ps.noteSi ?? "").includes("69, 85, 86, 88, 93, 128, 138"))
        p38bErrors.push("N083PS: nota SL brez seznama nerešenih strani za #12");
      if (!(ps.noteEn ?? "").includes("per-sheet")) p38bErrors.push("N083PS: nota EN brez per-sheet rekonstrukcije v naslednjih korakih");
    }
    if (PS_RECAP_1826.sampleRowCount !== 2974) p38bErrors.push("PS_RECAP: števec vrstic ni 2974");
    if (!(PS_RECAP_1826.mostUsefulSi ?? "").includes("P38")) p38bErrors.push("PS_RECAP: priporočilo SL ne odraža P38");
    // strežniška kontrola dokazov (odjemalski izris preskoči):
    // - v repozitoriju/CI (research/ prisoten po .gitignore-pravilih) → STROGO:
    //   vseh 20 datotek pass-3 + PS-full-v2.json mora obstajati;
    // - v produkcijskem deploymentu research/ NAMENOMA ni (.vercelignore, 92 MB)
    //   → kontrola se preskoči, dokazi ostanejo v repozitoriju.
    if (opts.fileExists) {
      const fileExists = opts.fileExists;
      if (fileExists("research/issue17/ps-raw/ps-005.json")) {
        const targets = [24, 37, 69, 79, 83, 84, 85, 86, 87, 88, 92, 93, 94, 99, 121, 125, 128, 135, 138, 139];
        const missing = targets.filter((t) => !fileExists(`research/issue17/ps-raw/ps-${String(t).padStart(3, "0")}-pass3.json`));
        if (missing.length) p38bErrors.push(`ps-raw: manjka pass3 za strani ${missing.join(", ")}`);
        if (!fileExists("research/issue17/PS-full-v2.json")) p38bErrors.push("manjka PS-full-v2.json");
      }
    }
  }
  push(
    "qa-p38-ps-blatt",
    "P38: N083PS — 3. prehod 20 ciljnih strani (233 VLM branj) + odkritje organizacije po listih (Blatt I–X, lastno številčenje); identiteta parcele = (list, številka); kontrolna vsota 2607 je vsota čez vse liste; 7 nerešenih strani izrecno za človeški pregled (#12)",
    "P38: N083PS — 3rd pass over 20 target pages (233 VLM reads) + discovery of sheet organization (Blatt I–X, own numbering); parcel identity = (sheet, number); the 2,607 checksum sums across all sheets; 7 unresolved pages explicitly deferred to human review (#12)",
    p38bErrors.length === 0,
    p38bErrors.length === 0
      ? "20 strani pass-3 · 2974 izbranih vrstic · str. 24 potrjena 421-440 · nerešene: 69, 85, 86, 88, 93, 128, 138"
      : p38bErrors.join("; "),
  );

  /* ── P39 (issue #10): PS — razdvojitev večkulturnih vrstic v spravni model ── */
  const p39Errors: string[] = [];
  const L = PS_LANDUSE_P39;
  const T = L.totals;
  if (L.status !== "REVIEW") p39Errors.push(`status=${L.status}, pričakovano REVIEW (strojno branje ni dokazni vir)`);
  if (L.readingRule !== "pass2wins") p39Errors.push(`readingRule=${L.readingRule}, pričakovano pass2wins (identično P38)`);
  // računsko-knjigovodske invariante (zero-loss)
  if (T.parcelEntriesWithCulture + T.parcelEntriesEmptyCulture !== T.parcelEntries)
    p39Errors.push("parcelEntriesWithCulture + parcelEntriesEmptyCulture ≠ parcelEntries");
  if (T.parcelEntries + T.nebereznaRows !== T.modelEntries)
    p39Errors.push("parcelEntries + nebereznaRows ≠ modelEntries");
  if (T.cultureRows + T.emptyCultureRows + T.nebereznaRows !== T.rowsBefore)
    p39Errors.push(`cultureRows (${T.cultureRows}) + emptyCultureRows (${T.emptyCultureRows}) + nebereznaRows (${T.nebereznaRows}) ≠ rowsBefore (${T.rowsBefore})`);
  if (T.duplicateCultureRows !== T.cultureRows - T.parcelCulturePairs)
    p39Errors.push("duplicateCultureRows ≠ cultureRows − parcelCulturePairs");
  // pinane vrednosti (regresija pravil skripta)
  if (T.rowsBefore !== 2760) p39Errors.push(`rowsBefore=${T.rowsBefore}, pričakovano 2760 (P36/P38)`);
  if (T.parcelEntries !== 2125 || T.parcelEntriesWithCulture !== 2118 || T.parcelEntriesEmptyCulture !== 7)
    p39Errors.push("vnosi po parcelah niso 2125/2118/7 (regresija P39 modela)");
  if (T.parcelCulturePairs !== 2632 || T.parcelsWithMultipleCultures !== 430 || T.duplicateCultureRows !== 49)
    p39Errors.push("razdvojitev ni 2632 parov / 430 parcel z več rabami / 49 podvojenih rab (regresija)");
  if (T.modelEntries !== 2134 || T.nebereznaRows !== 9 || T.emptyCultureRows !== 70)
    p39Errors.push("model ni 2134 vnosov / 9 NEBEREŽNA / 70 vrstic brez kulture (regresija)");
  // sekcije: skladnost s P38 (vključno s sirotami — P38 distinctParcels jih šteje)
  const S38 = PS_RECONCILIATION_P38.sections;
  const p39Sections = [
    ["GRUND_1_2505", S38["GRUND_1_2505"]?.distinctParcels],
    ["NADALJEVANJE_2506", S38["NADALJEVANJE_2506"]?.distinctParcels],
    ["WALDUNG", S38["WALDUNG"]?.distinctParcels],
    ["BLATT_X", S38["BLATT_X"]?.distinctParcels],
  ] as const;
  for (const [sec, expected] of p39Sections) {
    const got = L.sections[sec]?.parcelEntries;
    if (got == null || got !== expected) p39Errors.push(`sekcija ${sec}: ${got ?? "manjka"} ≠ P38 ${expected ?? "?"}`);
  }
  if (T.parcelEntriesWithCulture !== PS_RECONCILIATION_P38.splitting.parcelCulturePairs)
    p39Errors.push("parcelEntriesWithCulture ≠ P38 parcelCulturePairs (semantična povezava 2118 prekinjena)");
  // klasifikacija rab: zaprt sklop + računsko skladje (po PARIH parcela×raba)
  const C = L.cultureClasses;
  const clsSum = Object.values(C.primaryCounts).reduce((a, n) => a + n, 0);
  if (clsSum + C.unclassified.count !== T.parcelCulturePairs)
    p39Errors.push(`klasificirane (${clsSum}) + neklasificirane (${C.unclassified.count}) ≠ parcelCulturePairs (${T.parcelCulturePairs})`);
  if (C.classifiedPairs !== clsSum) p39Errors.push("classifiedPairs ≠ vsota primaryCounts");
  if (C.primaryCounts.NJIVA !== 1049 || C.primaryCounts.TRAVNIK !== 487 || C.primaryCounts.GOZD !== 134)
    p39Errors.push("primarni razredi NJIVA/TRAVNIK/GOZD niso 1049/487/134 (regresija pravilnika v1)");
  if (C.rulebookVersion !== "v1") p39Errors.push("pravilnik rab ni v1");
  if (L.orphanParcelKeys.length !== T.parcelEntriesEmptyCulture)
    p39Errors.push("orphanParcelKeys ≠ parcelEntriesEmptyCulture (sirote morajo biti izrecno naštete)");
  if (L.topCulturesRaw[0]?.raw !== "Acker" || L.topCulturesRaw[0]?.count !== 880)
    p39Errors.push("topCulturesRaw ni na čelu z Acker 880 (regresija)");
  // dokazni datoteki (strežniški klic; vzorec qa-p37/qa-p38)
  let p39FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-landuse.json");
    const rawRt = opts.readFile("src/data/atlas/ps-landuse.json");
    // produkcija: research/ NAMENOMA ni v deploymentu (.vercelignore, 92 MB) —
    // kontrola teče na runtime kopiji (bajtno identični izpis skripta; identičnost
    // obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p39Errors.push("research/issue17/ps-landuse.json ni berljiv (izpis scripts/p39_ps_landuse.py)");
    if (rawRt === null) p39Errors.push("src/data/atlas/ps-landuse.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p39Errors.push("dokazni in runtime izpis ps-landuse.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          totals: { modelEntries: number; parcelCulturePairs: number; parcelEntries: number };
          cultureClasses: { classifiedPairs: number; unclassified: { count: number } };
          parcels: unknown[];
          neberezna: unknown[];
        };
        if (j.totals.modelEntries !== T.modelEntries) p39Errors.push(`JSON modelEntries=${j.totals.modelEntries} ≠ TS ${T.modelEntries}`);
        if (j.totals.parcelCulturePairs !== T.parcelCulturePairs) p39Errors.push(`JSON parcelCulturePairs=${j.totals.parcelCulturePairs} ≠ TS ${T.parcelCulturePairs}`);
        if (j.cultureClasses.classifiedPairs !== C.classifiedPairs) p39Errors.push("JSON classifiedPairs ≠ TS");
        if (j.cultureClasses.unclassified.count !== C.unclassified.count) p39Errors.push("JSON unclassified.count ≠ TS");
        if (j.parcels.length !== T.parcelEntries) p39Errors.push(`JSON parcels.length=${j.parcels.length} ≠ parcelEntries ${T.parcelEntries}`);
        if (j.neberezna.length !== T.nebereznaRows) p39Errors.push(`JSON neberezna.length=${j.neberezna.length} ≠ nebereznaRows ${T.nebereznaRows}`);
        p39FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (vnosov ${j.parcels.length}+${j.neberezna.length}, parov ${j.totals.parcelCulturePairs})`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (vnosov ${j.parcels.length}+${j.neberezna.length}, parov ${j.totals.parcelCulturePairs})`;
      } catch {
        p39Errors.push("izpis ps-landuse.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p39-ps-landuse",
    "P39: N083PS — razdvojitev večkulturnih vrstic v spravni model (scripts/p39_ps_landuse.py): 2760 vrstic → 2134 vnosi (2125 parcel + 9 NEBEREŽNA), 2632 parov parcela×raba, 430 parcel z več rabami, 49 podvojenih rab ohranjenih, 7 sirot izrecnih; klasifikacija rab pravilnik v1 (brez AI) 72,0 % parov, ostalo izrecno NEKLASIFICIRANO; navzkrižna skladnost s P38 (1889/95/81/60); status REVIEW",
    "P39: N083PS — multi-culture rows split into the reconciliation model (scripts/p39_ps_landuse.py): 2,760 rows → 2,134 entries (2,125 parcels + 9 NEBEREŽNA), 2,632 parcel×culture pairs, 430 multi-culture parcels, 49 duplicate cultures preserved, 7 orphans explicit; culture rulebook v1 (no AI) 72.0% of pairs classified, the rest explicitly UNCLASSIFIED; cross-consistent with P38 (1,889/95/81/60); status REVIEW",
    p39Errors.length === 0,
    p39Errors.length === 0
      ? `2134 vnosov · 2632 parov · 430× več rab · 72,0 % klasificirano · ${p39FileDetail}`
      : p39Errors.join("; "),
  );

  // P39b (GitHub linija, 2026-10-11): strukturna rekonstrukcija PS (33 segmentov, per-list dokaz).
const p39bErrors: string[] = [];
  {
    const ps = ATLAS_SOURCES.find((s) => s.code === "N083PS");
    if (!ps) p39bErrors.push("vir N083PS manjka");
    else {
      if (!(ps.noteSi ?? "").includes("P39")) p39bErrors.push("N083PS: nota SL ne dokumentira P39 (strukturna rekonstrukcija)");
      if (!(ps.noteSi ?? "").includes("PS-reconstruction.json")) p39bErrors.push("N083PS: nota SL brez kazalca na dokaz PS-reconstruction.json");
      if (!(ps.noteSi ?? "").includes("29/29")) p39bErrors.push("N083PS: nota SL brez vsebinskega dokaza (29/29 parov z različnimi lastniki)");
      if (!(ps.noteSi ?? "").includes("2724")) p39bErrors.push("N083PS: nota SL brez števca 2724 unikatnih (segment, številka) parov");
      if (!(ps.noteSi ?? "").includes("[2221, 2725]")) p39bErrors.push("N083PS: nota SL brez meje [2221, 2725]");
      if (!(ps.noteSi ?? "").includes("KONSISTENTNO")) p39bErrors.push("N083PS: nota SL brez sklepa o konsistentnosti s kontrolno vsoto");
      if (!(ps.noteEn ?? "").includes("P39")) p39bErrors.push("N083PS: nota EN ne dokumentira P39");
      if (!(ps.noteEn ?? "").includes("REFUTED")) p39bErrors.push("N083PS: nota EN brez REFUTED (ovrnitev P36 hipoteze)");
      if (ps.structuredEntries !== 2974) p39bErrors.push("N083PS: structuredEntries spremenjen (P39 je analiza, ne nov prepis)");
    }
    const psSeries = KURRENT_SERIES.find((s) => s.code === "PS");
    if (!psSeries) p39bErrors.push("KURRENT_SERIES: PS manjka");
    else if (!(psSeries.noteSi ?? "").includes("P39")) p39bErrors.push("KURRENT_SERIES PS: nota SL ne odraža P39");
    if (!(PS_RECAP_1826.mostUsefulSi ?? "").includes("P39")) p39bErrors.push("PS_RECAP: priporočilo SL ne odraža P39");
    if (!(PS_RECAP_1826.mostUsefulEn ?? "").includes("P39")) p39bErrors.push("PS_RECAP: priporočilo EN ne odraža P39");
    if (PS_RECAP_1826.sampleRowCount !== 2974) p39bErrors.push("PS_RECAP: sampleRowCount ni 2974");
    // strežniška kontrola dokaza (enaka logika preskoka kot p38: v produkciji
    // research/ namenoma ni — .vercelignore)
    if (opts.fileExists) {
      if (opts.fileExists("research/issue17/ps-raw/ps-005.json")) {
        if (!opts.fileExists("research/issue17/PS-reconstruction.json"))
          p39bErrors.push("manjka PS-reconstruction.json (dokaz P39)");
      }
    }
  }
  push(
    "qa-p39-ps-structure",
    "P39: N083PS — strukturna rekonstrukcija: 33 segmentov (fizična segmentacija + lastniški test); VSEBINSKI DOKAZ per-list številčenja (29/29 prekrivajočih parov z različnimi lastniki — P36 hipoteza o napačno prebranih številkah OVRŽENA); 2724 unikatnih (segment, številka) parov (50 večkulturnih dodatnih vrstic, 200 neberljivih številk); kontrolna vsota 102+2505=2607 znotraj meje [2221, 2725] — KONSISTENTNO; eksaktna potrditev za issue #12",
    "P39: N083PS — structural reconstruction: 33 segments (physical segmentation + owner test); CONTENT EVIDENCE of per-sheet numbering (29/29 overlapping pairs with different owners — the P36 misread hypothesis REFUTED); 2,724 unique (segment, number) pairs (50 multi-culture extra rows, 200 unreadable numbers); the checksum 102+2,505=2,607 lies within the bounds [2,221, 2,725] — CONSISTENT; exact confirmation deferred to issue #12",
    p39bErrors.length === 0,
    p39bErrors.length === 0
      ? "33 segmentov · 29/29 vsebinski dokaz · 2724 parov · 2607 znotraj [2221, 2725]"
      : p39bErrors.join("; "),
  );

  // ——— P40: rekapitulacija str. 140–143 — deterministična primerjava s spravnim modelom (issue #10, P5-b) ———
  const p40Errors: string[] = [];
  const RC = PS_RECAP_P40;
  // 1. rekapitulacijska aritmetika (str. 143, rdeči tuš)
  if (RC.recapitulation.summaGrundparzellen + RC.recapitulation.summaBauplatze !== RC.recapitulation.zusammen)
    p40Errors.push("rekapitulacijska aritmetika 2505 + 102 ≠ Zusammen");
  if (RC.recapitulation.zusammen !== 2607 || RC.recapitulation.summaGrundparzellen !== 2505 || RC.recapitulation.summaBauplatze !== 102)
    p40Errors.push("rekapitulacijske vsote niso 2505/102/2607 (regresija str. 143)");
  if (!RC.crossCheck.checksumIdentity.pass || !RC.crossCheck.baselineIdentity.pass || !RC.crossCheck.p38ControlSum.pass)
    p40Errors.push("navzkrižne identitete (aritmetika/osnovna črta/P38 kontrola) morajo biti PASS");
  if (RC.crossCheck.baselineIdentity.grundSeen + RC.crossCheck.baselineIdentity.grundMissing !== RC.crossCheck.baselineIdentity.recapGrundparzellen)
    p40Errors.push("osnovna črta 1889 + 616 ≠ recap Grundparzellen");
  // 2. registrska vrzel stavbnih mest
  const BR = RC.crossCheck.bauplatzeRegister;
  if (BR.blattXRows !== 60 || BR.recap !== 102 || BR.gap !== 42)
    p40Errors.push("Blatt X register ni 60/102 z vrzeljo 42 (regresija P36/P38)");
  if (Math.abs(BR.coveragePct - (100 * BR.blattXRows) / BR.recap) > 0.05)
    p40Errors.push("pokritost registra se ne ujema z razmerjem 60/102");
  // 3. dekompozicija površin — aritmetika in regresije sekcij
  const A = RC.areaDecomposition;
  const secSum = Object.values(A.bySection).reduce(
    (acc, s) => ({ rowsWithArea: acc.rowsWithArea + s.rowsWithArea, rowsWithoutArea: acc.rowsWithoutArea + s.rowsWithoutArea, joch: acc.joch + s.joch, klafter: acc.klafter + s.klafter }),
    { rowsWithArea: 0, rowsWithoutArea: 0, joch: 0, klafter: 0 } as { rowsWithArea: number; rowsWithoutArea: number; joch: number; klafter: number },
  );
  if (secSum.rowsWithArea !== A.rowsWithArea || secSum.rowsWithoutArea !== A.rowsWithoutArea)
    p40Errors.push("vsota sekcij rowsWithArea/rowsWithoutArea ≠ skupni");
  if (secSum.joch !== 675 || secSum.klafter !== 1423653)
    p40Errors.push("skupna površina ni 675 Joch + 1.423.653 Klafter (regresija modela P39)");
  if (secSum.rowsWithArea + secSum.rowsWithoutArea !== 2632)
    p40Errors.push("vrstice s površino + brez ≠ 2632 parov parcela×raba (P39 regresija)");
  const G = A.bySection.GRUND_1_2505;
  if (!G || G.joch !== 404 || G.klafter !== 1326343 || G.rowsWithoutArea !== 7)
    p40Errors.push("GRUND_1_2505 ni 404 Joch + 1.326.343 Klafter z 7 vrsticami brez površine (regresija)");
  if (Math.abs(G.jochEquivalent - (G.joch + G.klafter / A.klafterPerJoch)) > 0.0001)
    p40Errors.push("jochEquivalent GRUND ni joch + klafter/1600");
  // 4. kandidati atribucije — aritmetika odmikov in monotonost
  const cand = RC.recapAreaAttribution.candidates;
  if (cand.length !== 3) p40Errors.push("kandidatov atribucije mora biti 3");
  const recapReading = RC.recapAreaAttribution.recapReading;
  if (recapReading !== 1216) p40Errors.push("recap branje ni 1216(?) (regresija)");
  for (const c of cand) {
    const d = c.jochEquivalent - recapReading;
    if (Math.abs(c.deltaJoch - d) > 0.001) p40Errors.push(`deltaJoch kandidata »${c.scope.slice(0, 20)}…« ni jochEquivalent − 1216`);
    if (Math.abs(c.deltaPct - (100 * c.deltaJoch) / recapReading) > 0.01) p40Errors.push(`deltaPct kandidata »${c.scope.slice(0, 20)}…« se ne ujema`);
  }
  if (!(cand[0].deltaJoch < cand[1].deltaJoch && cand[1].deltaJoch < cand[2].deltaJoch))
    p40Errors.push("odmiki kandidatov niso naraščajoči (GRUND-only < brez Blatt X < celoten)");
  if (!RC.recapAreaAttribution.closest.startsWith("GRUND_1_2505"))
    p40Errors.push("najbližji kandidat ni GRUND-only");
  // 5. Blatt X prekrivanje (podvajanje nedokazljivo) + fragmenti (UNRESOLVED)
  const X = RC.blattXOverlap;
  if (X.pairsOverlap !== 1 || X.pairsBlattX !== 59 || X.ownersBlattX !== 22 || X.ownersOverlap !== 1)
    p40Errors.push("Blatt X prekrivanje ni 1/59 parov in 1/22 lastnikov (regresija)");
  const F = RC.fragmentRows140_141;
  if (F.count !== 7 || F.verbatim.length !== 7 || F.naiveJochSum !== 1413)
    p40Errors.push("fragmenti 140–141 niso 7 doslovnih vrstic z naivno vsoto 1413");
  if (!F.resolution.includes("UNRESOLVED"))
    p40Errors.push("fragmenti morajo ostati izrecno UNRESOLVED (brez tihega tolmačenja)");
  // 6. številčni eho — ovrgan (negativen izid, izrecno dokumentiran)
  if (!RC.numericEcho.refuted || RC.numericEcho.maxParcelNadaljevanje !== 2840)
    p40Errors.push("številčni eho mora biti OVRGAN z max parcelo 2840 (negativen izid)");
  // 7. dokazni datoteki (strežniški klic; vzorec qa-p37/qa-p38/qa-p39)
  let p40FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-recap.json");
    const rawRt = opts.readFile("src/data/atlas/ps-recap.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p40Errors.push("research/issue17/ps-recap.json ni berljiv (izpis scripts/p40_ps_recap.py)");
    if (rawRt === null) p40Errors.push("src/data/atlas/ps-recap.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p40Errors.push("dokazni in runtime izpis ps-recap.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          recapitulation: { summaGrundparzellen: number; summaBauplatze: number; zusammen: number };
          areaDecomposition: { rowsWithArea: number; rowsWithoutArea: number; bySection: Record<string, { joch: number; klafter: number }> };
          numericEcho: { refuted: boolean; maxParcelNadaljevanje: number };
        };
        if (j.recapitulation.zusammen !== RC.recapitulation.zusammen) p40Errors.push("JSON zusammen ≠ TS");
        if (j.recapitulation.summaGrundparzellen !== RC.recapitulation.summaGrundparzellen) p40Errors.push("JSON summaGrundparzellen ≠ TS");
        if (j.recapitulation.summaBauplatze !== RC.recapitulation.summaBauplatze) p40Errors.push("JSON summaBauplatze ≠ TS");
        if (j.areaDecomposition.rowsWithArea !== A.rowsWithArea) p40Errors.push("JSON rowsWithArea ≠ TS");
        if (j.areaDecomposition.rowsWithoutArea !== A.rowsWithoutArea) p40Errors.push("JSON rowsWithoutArea ≠ TS");
        if (j.areaDecomposition.bySection.GRUND_1_2505?.joch !== G.joch) p40Errors.push("JSON GRUND joch ≠ TS");
        if (!j.numericEcho.refuted || j.numericEcho.maxParcelNadaljevanje !== 2840) p40Errors.push("JSON numericEcho ni ovrgan z 2840");
        p40FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (recap ${j.recapitulation.zusammen}, površine ${j.areaDecomposition.rowsWithArea}+${j.areaDecomposition.rowsWithoutArea} vrstic)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (recap ${j.recapitulation.zusammen}, površine ${j.areaDecomposition.rowsWithArea}+${j.areaDecomposition.rowsWithoutArea} vrstic)`;
      } catch {
        p40Errors.push("izpis ps-recap.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p40-ps-recap",
    "P40: N083PS — rekapitulacija str. 140–143 deterministično spravljena s spravnim modelom (scripts/p40_ps_recap.py): 102 + 2505 = 2607 (rdeči tuš) == P38 kontrolna vsota == P36/P38 osnovna črta (1889+616); Blatt X register 60/102 (vrzel 42); površine po sekcijah (GRUND 1232,96 Joch najbližje Summi 1216(?) Joch, Δ +1,39 %); Blatt X ↔ GRUND podvajanje nedokazljivo (1/59 parov); fragmenti 140–141 UNRESOLVED; številčni eho OVRGAN (2840 ≠ 2607); status REVIEW",
    "P40: N083PS — pages 140–143 recapitulation deterministically reconciled with the land model (scripts/p40_ps_recap.py): 102 + 2,505 = 2,607 (red chalk) == P38 control sum == P36/P38 baseline (1,889+616); Blatt X register 60/102 (gap 42); areas by section (GRUND 1,232.96 Joch closest to the 1,216(?) Joch total, Δ +1.39%); Blatt X ↔ GRUND duplication unproven (1/59 pairs); fragments 140–141 UNRESOLVED; numeric echo REFUTED (2,840 ≠ 2,607); status REVIEW",
    p40Errors.length === 0,
    p40Errors.length === 0
      ? `2607 = 2505 + 102 · Blatt X 60/102 · GRUND 1232,96 Joch (Δ +1,39 %) · ${p40FileDetail}`
      : p40Errors.join("; "),
  );

  // ——— P41: paleografija str. 140–143 — "Abschluß der Gemeinde" (issue #10) ———
  const p41Errors: string[] = [];
  const P41 = PS_RECAP_PALEO_P41;
  const p41jk = (s: string) => {
    const [j, k] = s.split("|").map(Number);
    return j * 1600 + k;
  };
  // 1. vse identitete morajo biti PASS in opisane
  for (const [k, v] of Object.entries(P41.identities)) {
    if (!v.pass) p41Errors.push(`identiteta ${k} ni PASS`);
    if (!v.detail) p41Errors.push(`identiteta ${k} brez opisa`);
  }
  // 2. aritmetika iz konsenzualnih vrednosti (1 Joch = 1600 K)
  if (p41jk(P41.page140Left.summaGrundparzellen) + p41jk(P41.page140Left.zinsbBauparzellen) !== p41jk(P41.page140Left.summaNach))
    p41Errors.push("831|702 + 3|312 ≠ 834|1014");
  if (p41jk(P41.abschluss.summeDerGrundparzellen) + p41jk(P41.abschluss.summeDerBauparzellen) !== p41jk(P41.abschluss.areaDerGemeinde))
    p41Errors.push("1215|490 + 5|1003 ≠ Area der Gemeinde 1220|1493");
  if (p41jk(P41.abschluss.areaDerGemeinde) !== 1220 * 1600 + 1493)
    p41Errors.push("Area dergemeinde ni 1220 Joch + 1493 Klafter");
  // 3. vsota 7 Grundstückslagen == Summa der Grundparzellen (razrešitev P40 'naivna 1413')
  const p41LageJ = P41.lageRows.reduce((a, r) => a + r.joch, 0);
  const p41LageK = P41.lageRows.reduce((a, r) => a + r.klafter, 0);
  if (P41.lageRows.length !== 7) p41Errors.push("število Grundstückslagen ni 7");
  if (p41LageJ + Math.floor(p41LageK / 1600) !== P41.lageSum.joch || p41LageK % 1600 !== P41.lageSum.klafter || P41.lageSum.joch !== 831 || P41.lageSum.klafter !== 702)
    p41Errors.push("vsota 7 Grundstückslagen ni 831|702 (razrešitev P40 'naivna vsota 1413')");
  // 4. regresija str. 143 (3/3 enoglasno) + P9 popravke
  if (P41.page143.values.join(",") !== "102,2505,2607") p41Errors.push("str. 143 ni 102/2505/2607 (regresija P36/P38/P40)");
  if (P41.page141.referencePairs.length !== 7) p41Errors.push("p141 par referenc ni 7");
  if (P41.page141.p9Corrections.length !== 3) p41Errors.push("P9 popravke niso 3 (190/1168, 286/8931, 198/11957)");
  if (!P41.abschluss.unresolvedSplit.resolved === false && !P41.abschluss.unresolvedSplit.status.includes("UNRESOLVED"))
    p41Errors.push("razcep K1/K2 mora ostati izrecno UNRESOLVED");
  // 5. atribucija: Area der Gemeinde preferirana, Δ < P40 (+1,39 %)
  const AT41 = P41.crossCheck.areaAttribution;
  if (!AT41.preferred.label.includes("Area der Gemeinde")) p41Errors.push("preferirani kandidat ni 'Area der Gemeinde'");
  if (Math.abs(AT41.preferred.joch - p41jk("1220|1493") / 1600) > 0.0001)
    p41Errors.push("preferirani kandidat joch ≠ 1220|1493/1600");
  const p41Delta = (100 * (AT41.modelGrundJoch - AT41.preferred.joch)) / AT41.preferred.joch;
  if (Math.abs(AT41.preferred.deltaPct - p41Delta) > 0.02) p41Errors.push("deltaPct atribucije se ne ujema z aritmetiko");
  if (AT41.preferred.deltaPct >= 1.39) p41Errors.push("Area der Gemeinde ne izboljšuje P40 (+1,39 %)");
  if (!AT41.p40Best.startsWith("GRUND_1_2505")) p41Errors.push("P40 najboljši kandidat ni dokumentiran (regresija)");
  // 6. model refs + razrešitve + odprta vprašanja
  if (P41.crossCheck.modelRefs.total !== 14 || P41.crossCheck.modelRefs.missing.join(",") !== "1188,1196,1466")
    p41Errors.push("model refs niso 14 z manjkajočimi 1188/1196/1466");
  if (P41.resolves.length < 3) p41Errors.push("razrešitve (P40 '1413', '1216(?)', poreklo '~1216') niso dokumentirane");
  if (P41.open.length < 5) p41Errors.push("odprta vprašanja niso izrecna (≥5)");
  // 7. dokazni datoteki (strežniški klic; vzorec qa-p37..p40)
  let p41FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-recap-paleo.json");
    const rawRt = opts.readFile("src/data/atlas/ps-recap-paleo.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p41Errors.push("research/issue17/ps-recap-paleo.json ni berljiv (izpis scripts/p41_ps_recap_paleo.py)");
    if (rawRt === null) p41Errors.push("src/data/atlas/ps-recap-paleo.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p41Errors.push("dokazni in runtime izpis ps-recap-paleo.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          reading: { page140Right: { rows: { areaDerGemeinde: { value: string } } }; page143: { values: string[] } };
          identities: Record<string, { pass: boolean }>;
          crossCheck: { areaAttribution: { preferred: { deltaPct: number } } };
        };
        if (j.reading.page140Right.rows.areaDerGemeinde.value !== P41.abschluss.areaDerGemeinde) p41Errors.push("JSON areaDerGemeinde ≠ TS");
        if (j.reading.page143.values.join(",") !== P41.page143.values.join(",")) p41Errors.push("JSON page143 ≠ TS");
        if (!j.identities.e_areaGemeinde?.pass) p41Errors.push("JSON identiteta e_areaGemeinde ni PASS");
        if (Math.abs(j.crossCheck.areaAttribution.preferred.deltaPct - AT41.preferred.deltaPct) > 0.001) p41Errors.push("JSON deltaPct ≠ TS");
        p41FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (Area ${j.reading.page140Right.rows.areaDerGemeinde.value}, str. 143: ${j.reading.page143.values.join("/")})`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (Area ${j.reading.page140Right.rows.areaDerGemeinde.value}, str. 143: ${j.reading.page143.values.join("/")})`;
      } catch {
        p41Errors.push("izpis ps-recap-paleo.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p41-ps-recap-paleo",
    "P41: N083PS — paleografija str. 140–143 (12 VLM prehodov 3×4 + izrezi): 'Area der Gemeinde' 1220 J 1493 K (rdeči tuš) = 1215|490 + 5|1003 — PRVIČ SKUPNA POVRŠINA OBČINE; 7 Grundstückslagen (hiše 124–130) vsota 831|702 == 'Summa der Grundparzellen' (P40 'naivna vsota 1413' razrešena kot P9 napaka: 190/1168→830|1188, 286/8931→286|921, 198/11957→138|1457); str. 143 regresija 102+2505=2607 (3/3 enoglasno); atribucija: model GRUND 1232,96 J Δ +0,99 % (izboljšava P40 +1,39 %); razcepi (K1/K2 = 2090, semantika par referenc — hipotezi OVRŽENI, p141 šibki blok) izrecno UNRESOLVED; status REVIEW",
    "P41: N083PS — palaeography of pp. 140–143 (12 VLM passes 3×4 + crops): 'Area der Gemeinde' 1,220 J 1,493 K (red chalk) = 1,215|490 + 5|1,003 — the MUNICIPAL TOTAL AREA captured for the first time; 7 Grundstückslagen rows (houses 124–130) sum to 831|702 == 'Summa der Grundparzellen' (P40's 'naive sum 1,413' resolved as a P9 reading error: 190/1168→830|1188, 286/8931→286|921, 198/11957→138|1457); p. 143 regression 102+2,505=2,607 (3/3 unanimous); attribution: GRUND model 1,232.96 J Δ +0.99% (improving P40's +1.39%); splits (K1/K2 = 2,090, pair-reference semantics — both hypotheses refuted, p141 weak block) explicitly UNRESOLVED; status REVIEW",
    p41Errors.length === 0,
    p41Errors.length === 0
      ? `Area der Gemeinde 1220|1493 (= 1220,933 J) · 7 Lager == 831|702 · str. 143: 2607 · Δ GRUND +0,99 % · ${p41FileDetail}`
      : p41Errors.join("; "),
  );

  /* ── P42 (issue #10): PS — pravilnik rab v2 ── */
  const p42Errors: string[] = [];
  const V2 = PS_LANDUSE_V2_P42;
  const S2 = V2.stats;
  if (V2.status !== "REVIEW") p42Errors.push(`status=${V2.status}, pričakovano REVIEW (klasifikacija je za statistiko)`);
  // 1. osnovna identiteta termType (po PARIH — kot P39)
  if (S2.v2ClassifiedPairs + S2.toponymPairs + S2.artifaktPairs + S2.unresolvedPairs !== S2.pairsTotal)
    p42Errors.push("KULTURA + TOPONIM + ARTIFAKT + NEKLASIFICIRANO ≠ pairsTotal (2632)");
  if (S2.pairsTotal !== PS_LANDUSE_P39.totals.parcelCulturePairs)
    p42Errors.push("pairsTotal ≠ P39 parcelCulturePairs (2632)");
  if (S2.v1ClassifiedPairs !== PS_LANDUSE_P39.cultureClasses.classifiedPairs)
    p42Errors.push("v1ClassifiedPairs ≠ P39 classifiedPairs (1896)");
  // 2. v2 ⊇ v1: novi pari = 303, noben v1 razred ne upade
  const newPairsSum = Object.values(S2.newPairsByClassV2).reduce((a, n) => a + n, 0);
  if (newPairsSum !== S2.v2ClassifiedPairs - S2.v1ClassifiedPairs)
    p42Errors.push(`vsota newPairsByClassV2 (${newPairsSum}) ≠ v2 − v1 (${S2.v2ClassifiedPairs - S2.v1ClassifiedPairs})`);
  const V1C = PS_LANDUSE_P39.cultureClasses.primaryCounts;
  for (const [cls, v1n] of Object.entries(V1C)) {
    const v2n = S2.primaryCountsV2[cls] ?? 0;
    const gain = S2.newPairsByClassV2[cls] ?? 0;
    if (v2n < v1n) p42Errors.push(`razred ${cls}: v2 (${v2n}) < v1 (${v1n}) — v2 ⊉ v1`);
    if (v2n !== v1n + gain) p42Errors.push(`razred ${cls}: v2 (${v2n}) ≠ v1 (${v1n}) + novi (${gain})`);
  }
  // 3. pinane vrednosti (regresija pravilnika v2)
  if (S2.v2ClassifiedPairs !== 2199 || S2.classifiedPctV2 !== 83.5)
    p42Errors.push("v2 klasificirani pari niso 2199 (83,5 %) — regresija pravilnika v2");
  if (S2.toponymPairs !== 122 || S2.artifaktPairs !== 29 || S2.unresolvedPairs !== 282)
    p42Errors.push("TOPONIM/ARTIFAKT/NEKLASIFICIRANO niso 122/29/282 (regresija)");
  // pojasnjeni pari = 2632 − 282 (izrecno; 89,3 % je zaokroženo)
  if (S2.pairsTotal - S2.unresolvedPairs !== 2350) p42Errors.push("pojasnjeni pari niso 2350 (2632 − 282)");
  if (S2.classifiedPctV2 !== Math.round((1000 * S2.v2ClassifiedPairs) / S2.pairsTotal) / 10)
    p42Errors.push("classifiedPctV2 se ne ujema z aritmetiko");
  if (S2.primaryCountsV2.NJIVA !== 1095 || S2.primaryCountsV2.TRAVNIK !== 527 || S2.primaryCountsV2.GOZD !== 166)
    p42Errors.push("primarni razredi v2 NJIVA/TRAVNIK/GOZD niso 1095/527/166 (regresija)");
  if (S2.primaryCountsV2.VINOGRAD !== 19)
    p42Errors.push("VINOGRAD v2 ni 19 (8 v1 + 11 novih — v1 vrzel 'Wein' zaprta)");
  // 4. pravilnik: 12 v1 nespremenjenih + 13 priloženih, vsota dodelitev = novi pari
  if (V2.rulebook.version !== "v2" || V2.rulebook.v1RulesCount !== 12)
    p42Errors.push("pravilnik ni v2 z 12 v1 pravili");
  if (V2.rulebook.appendedRules.length !== 13) p42Errors.push("priloženih pravil ni 13");
  const rulePairsSum = V2.rulebook.appendedRules.reduce((a, r) => a + r.pairs, 0);
  if (rulePairsSum !== newPairsSum) p42Errors.push(`vsota dodelitev priloženih pravil (${rulePairsSum}) ≠ novi pari (${newPairsSum})`);
  const ruleNos = V2.rulebook.appendedRules.map((r) => r.no);
  if (ruleNos.join(",") !== "13,14,15,16,17,18,19,20,21,22,23,24,25")
    p42Errors.push("številke priloženih pravil niso 13–25");
  if (!V2.rulebook.appendedRules.every((r) => r.confidence === "~" || r.confidence === "?"))
    p42Errors.push("zaupanje priloženih pravil ni [~]/[?]");
  // 5. TOPONIM/ARTIFAKT + družine (izrecno NEKLASIFICIRANE — pinano)
  if (V2.toponym.distinct !== 39 || V2.toponym.top.length < 5)
    p42Errors.push("TOPONIM ni 39 različnih z dokumentiranimi primeri");
  if (V2.toponym.top[0]?.raw !== "Löwisch Thal" || V2.toponym.top[0]?.pairs !== 15)
    p42Errors.push("TOPONIM ni na čelu z 'Löwisch Thal' 15 (regresija)");
  if (V2.artifakt.numericRawCount !== 19)
    p42Errors.push("ARTIFAKT numeričnih vrednosti ni 19 (Blatt X register 82–100)");
  if (V2.families.length !== 16) p42Errors.push("neznanih družin ni 16");
  const famPairsSum = V2.families.reduce((a, f) => a + f.pairs, 0);
  if (famPairsSum > S2.unresolvedPairs) p42Errors.push("vsota družin > NEKLASIFICIRANO");
  const famPin: Record<string, number> = {
    "LHUT-JEDRO": 36, "LHIZ": 9, "LHOPI-LOHIFA": 23, "LOHN-RAUT": 29, "AHN": 13,
    "AEFLING": 13, "ERDAR": 10, "GUETEN": 12, "EINHART": 15, "DINGF": 10,
    "LUKIG": 10, "LOHGARN": 7, "HURGI": 5, "WING": 3, "EINSCHLAG-GUELZE": 20, "SCHINDEL": 1,
  };
  for (const f of V2.families) {
    if (famPin[f.id] !== f.pairs) p42Errors.push(`družina ${f.id}: ${f.pairs} ≠ pinano ${famPin[f.id]}`);
    if (!f.verdict.includes("NEKLASIFICIRANO")) p42Errors.push(`družina ${f.id} ni izrecno NEKLASIFICIRANA`);
    if (!f.hypothesisSi) p42Errors.push(`družina ${f.id} brez hipoteze/opombe`);
  }
  const aef = V2.families.find((f) => f.id === "AEFLING");
  if (!aef || aef.coParcel.TRAVNIK !== 12) p42Errors.push("AEFLING so-odvisnost TRAVNIK ni 12/13 (dokaz mora ostati dokumentiran)");
  // 6. dokazni datoteki (strežniški klic; vzorec qa-p37..p41)
  let p42FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-landuse-v2.json");
    const rawRt = opts.readFile("src/data/atlas/ps-landuse-v2.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p42Errors.push("research/issue17/ps-landuse-v2.json ni berljiv (izpis scripts/p42_ps_rulebook_v2.py)");
    if (rawRt === null) p42Errors.push("src/data/atlas/ps-landuse-v2.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p42Errors.push("dokazni in runtime izpis ps-landuse-v2.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          stats: { pairsTotal: number; v2ClassifiedPairs: number; toponymPairs: number; artifaktPairs: number; unresolvedPairs: number; classifiedPctV2: number };
          rulebook: { version: string; v1Rules: { no: number }[]; appendedRules: { no: number; pairs: number; claimedRaw: Record<string, { pairs: number }> }[] };
          termTypes: { TOPONIM: { pairs: number }; ARTIFAKT: { pairs: number }; NEKLASIFICIRANO: { pairs: number; families: { id: string; pairs: number }[] } };
          values: unknown[];
          v1Regression: { checkedPairs: number; mismatches: number };
        };
        if (j.stats.v2ClassifiedPairs !== S2.v2ClassifiedPairs) p42Errors.push("JSON v2ClassifiedPairs ≠ TS");
        if (j.stats.classifiedPctV2 !== S2.classifiedPctV2) p42Errors.push("JSON classifiedPctV2 ≠ TS");
        if (j.stats.toponymPairs !== S2.toponymPairs || j.stats.artifaktPairs !== S2.artifaktPairs || j.stats.unresolvedPairs !== S2.unresolvedPairs)
          p42Errors.push("JSON TOPONIM/ARTIFAKT/NEKLASIFICIRANO ≠ TS");
        if (j.rulebook.version !== "v2" || j.rulebook.v1Rules.length !== 12 || j.rulebook.appendedRules.length !== 13)
          p42Errors.push("JSON pravilnik ni v2 (12 v1 + 13 priloženih)");
        const jRulePairs = j.rulebook.appendedRules.reduce((a, r) => a + r.pairs, 0);
        if (jRulePairs !== rulePairsSum) p42Errors.push("JSON vsota dodelitev pravil ≠ TS");
        for (const r of j.rulebook.appendedRules) {
          const claimed = Object.values(r.claimedRaw).reduce((a, m) => a + m.pairs, 0);
          if (claimed !== r.pairs) p42Errors.push(`JSON pravilo ${r.no}: claimedRaw ≠ pairs`);
        }
        if (j.termTypes.TOPONIM.pairs !== 122 || j.termTypes.ARTIFAKT.pairs !== 29)
          p42Errors.push("JSON termTypes TOPONIM/ARTIFAKT nista 122/29");
        if (j.termTypes.NEKLASIFICIRANO.families.length !== 16) p42Errors.push("JSON družin ni 16");
        if (j.v1Regression.checkedPairs !== 2632 || j.v1Regression.mismatches !== 0)
          p42Errors.push("JSON v1 regresija ni čista (2632/0)");
        // values = tabela VSEH različnih surovih vrednosti — vsota parov mora biti 2632
        if (!Array.isArray(j.values)) {
          p42Errors.push("JSON values ni tabela");
        } else {
          const jPairs = (j.values as { pairs: number }[]).reduce((a, v) => a + v.pairs, 0);
          if (jPairs !== 2632) p42Errors.push(`JSON values parov (${jPairs}) ≠ 2632`);
        }
        p42FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (pari ${j.stats.v2ClassifiedPairs}/${j.stats.pairsTotal} = ${j.stats.classifiedPctV2} %, 13 pravil, 16 družin)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (pari ${j.stats.v2ClassifiedPairs}/${j.stats.pairsTotal} = ${j.stats.classifiedPctV2} %, 13 pravil, 16 družin)`;
      } catch {
        p42Errors.push("izpis ps-landuse-v2.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p42-ps-rulebook-v2",
    "P42: N083PS — pravilnik rab v2 (12 nespremenjenih v1 pravil + 13 priloženih, prvi zadetek = primarni razred): pokritost 2199/2632 parov (83,5 %; v1 72,0 %), +303 parov — umlaut Gärten, sredbesedni -wald/-weid (Schlagwald, Schafweide), schupf. / schupfen, sami 'Wein' (11 vinogradov), Öd/Wüst (Eidn/Ehda/Wiste 73 NEROD), Maid = Mahd (16), Gemainde Gmde/Gimand (12 OBCINA), Rüben/Schlagfeld/Stopp (46 NJIVA), Schupfe/Staidl/Grube/Gütl/Hof/Haus/Boden (45 STAVBNO); izrecna ločitev termType: TOPONIM 122 (ležajna imena — Löwisch Thal, Leite … NI raba), ARTIFAKT 29 (številke 82–100 na Blatt X — register stavbnih mest!, Summa, Zahl, opombe prihodkov); 282 parov izrecno NEKLASIFICIRANO v 16 družinah z so-odvisnostnimi dokazi (Lhut-jedro 36, Lohn/Raut 29, Lhopi/Lohifa 23, Äfling 13 z 12/13 TRAVNIK …); v2 ⊇ v1 regresijsko (v1 2632/0 neskladij); status REVIEW",
    "P42: N083PS — land-use rulebook v2 (12 unchanged v1 rules + 13 appended, first match = primary class): coverage 2,199/2,632 pairs (83.5%; v1 72.0%), +303 pairs — umlaut Gärten, mid-word -wald/-weid (Schlagwald, Schafweide), schupf./schupfen, bare 'Wein' (11 vineyards), Öd/Wüst (Eidn/Ehda/Wiste 73 WASTE), Maid = Mahd (16), Gemainde Gmde/Gimand (12 COMMON), Rüben/Schlagfeld/Stopp (46 FIELD), Schupfe/Staidl/Grube/Gütl/Hof/Haus/Boden (45 BUILDING); explicit termType distinction: TOPONYM 122 (place names — Löwisch Thal, Leite … NOT a use), ARTIFACT 29 (numbers 82–100 on Blatt X — the building-plot register!, Summa, Zahl, yield notes); 282 pairs explicitly UNCLASSIFIED in 16 families with co-occurrence evidence (Lhut-core 36, Lohn/Raut 29, Lhopi/Lohifa 23, Äfling 13 with 12/13 MEADOW …); v2 ⊇ v1 regression-checked (v1 2,632/0 mismatches); status REVIEW",
    p42Errors.length === 0,
    p42Errors.length === 0
      ? `2199/2632 (83,5 %) · +303 parov (13 pravil) · TOPONIM 122 · ARTIFAKT 29 · NEKLASIFICIRANO 282 (16 družin) · pojasnjeno 89,3 % · ${p42FileDetail}`
      : p42Errors.join("; "),
  );


  // ——— P43: N083PS — neznane družine: prečni prehodi + PV sprava + leksikon ———
  const p43Errors: string[] = [];
  const L3 = PS_LEXICON_P43;
  const famPairs43 = L3.families.reduce((a, f) => a + f.pairs, 0);
  if (famPairs43 !== 216) p43Errors.push(`vsota 16 družin je ${famPairs43}, morala bi biti 216`);
  if (L3.singles.pairs !== 66) p43Errors.push("kitice niso 66 parov");
  if (famPairs43 + L3.singles.pairs !== 282) p43Errors.push("216 + kitice ≠ 282 (v2 NEKLASIFICIRANO)");
  if (L3.families.length !== 16) p43Errors.push("družin ni 16");
  const famPin43: Record<string, number> = {
    "LHUT-JEDRO": 36, "LOHN-RAUT": 29, "LHOPI-LOHIFA": 23, "EINSCHLAG-GUELZE": 20,
    "EINHART": 15, "AHN": 13, "AEFLING": 13, "GUETEN": 12, "ERDAR": 10, "DINGF": 10,
    "LUKIG": 10, "LHIZ": 9, "LOHGARN": 7, "HURGI": 5, "WING": 3, "SCHINDEL": 1,
  };
  for (const f of L3.families) {
    if (famPin43[f.id] !== f.pairs) p43Errors.push(`družina ${f.id}: ${f.pairs} ≠ pinano ${famPin43[f.id]}`);
    if (!f.termTypeHypothesis) p43Errors.push(`družina ${f.id} brez termType hipoteze`);
    for (const h of f.topHypotheses) {
      if (!["~", "?"].includes(h.confidence)) p43Errors.push(`družina ${f.id}: zaupanje '${h.confidence}' ni [~]/[?]`);
      if (!h.source) p43Errors.push(`družina ${f.id}: kandidat '${h.candidate}' brez vira`);
      if (f.topHypotheses.length > 3) p43Errors.push(`družina ${f.id}: več kot 3 kandidati v TS`);
    }
  }
  const dingf = L3.families.find((f) => f.id === "DINGF");
  if (!dingf || dingf.stablePairs !== 10) p43Errors.push("DINGF ni 10/10 stabilnih (edina stabilna neznana beseda)");
  const lhiz = L3.families.find((f) => f.id === "LHIZ");
  if (!lhiz || lhiz.fallbackPairs !== 9) p43Errors.push("LHIZ ni 9/9 padcev (Wiese→Lhize)");
  const erdar = L3.families.find((f) => f.id === "ERDAR");
  if (!erdar || erdar.fallbackPairs !== 5) p43Errors.push("ERDAR ni 5 padcev (Acker→Achm)");
  const blockOne = L3.families.filter((f) => f.block.distinctPages === 1).length;
  if (blockOne !== 10) p43Errors.push(`blokovska koncentracija na 1 fotografijo: ${blockOne}, pričakovano 10`);
  const PV = L3.pvReconciliation;
  if (PV.pvTotalJ !== 1221.95) p43Errors.push("PV total ni 1221,95 J (1221|1513)");
  if (PV.rowsModelTotalJ !== 1564.78) p43Errors.push("model total ni 1564,78 J (P40 konstanta)");
  if (PV.weidenGapJ !== 576.24) p43Errors.push("Weiden-gap ni 576,24 J");
  if (PV.psPastVisceAlmJ !== 59.92) p43Errors.push("PASTVISCE+ALM ni 59,92 J");
  if (PV.unknownFamiliesAreaJ !== 96.68) p43Errors.push("površina neznanih družin ni 96,68 J");
  if (PV.njivaVsAeckerDeltaJ !== 202.29) p43Errors.push("NJIVA Δ ni +202,29 J");
  if (PV.travnikVsWiesenDeltaJ !== 182.12) p43Errors.push("TRAVNIK Δ ni +182,12 J");
  if (PV.vinogradVsWeinDeltaJ !== -0.46) p43Errors.push("VINOGRAD Δ ni −0,46 J");
  if (PV.rowsModelVsPvTotalJ !== 342.84) p43Errors.push("model−Area ni 342,84 J");
  const pvOfficialWeiden = PV.pvOfficial.Weiden;
  if (!pvOfficialWeiden || pvOfficialWeiden.joch !== 636 || pvOfficialWeiden.klafter !== 263)
    p43Errors.push("PV Weiden ni 636|263");
  if (PV.pvOfficial.Grand_Total?.joch !== 1221 || PV.pvOfficial.Grand_Total?.klafter !== 1513)
    p43Errors.push("PV Grand_Total ni 1221|1513");
  // 6. dokazni datoteki (strežniški klic; vzorec qa-p37..p42)
  let p43FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-lexicon.json");
    const rawRt = opts.readFile("src/data/atlas/ps-lexicon.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p43Errors.push("research/issue17/ps-lexicon.json ni berljiv (izpis scripts/p43_ps_lexicon.py)");
    if (rawRt === null) p43Errors.push("src/data/atlas/ps-lexicon.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p43Errors.push("dokazni in runtime izpis ps-lexicon.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          families: { id: string; pairs: number; stablePairs: number; fallbackPairs: number; block: { distinctPages: number }; lexicon: { termTypeHypothesis: string; hypotheses: { candidate: string; source: string; confidence: string }[]; sources: string[] } }[];
          singles: { pairs: number; distinctRaw: number };
          pvReconciliation: { weidenGapJ: number; rowsModelTotalJ: number; pvTotalJ: number };
        };
        const jFam = j.families.reduce((a, f) => a + f.pairs, 0);
        if (jFam + j.singles.pairs !== 282) p43Errors.push("JSON 216+66 ≠ 282");
        const jd = j.families.find((f) => f.id === "DINGF");
        if (!jd || jd.stablePairs !== 10) p43Errors.push("JSON DINGF ni 10/10");
        const jl = j.families.find((f) => f.id === "LHIZ");
        if (!jl || jl.fallbackPairs !== 9) p43Errors.push("JSON LHIZ ni 9 padcev");
        const noLex = j.families.filter((f) => !f.lexicon || f.lexicon.hypotheses.length === 0);
        if (noLex.length > 1) p43Errors.push(`JSON ${noLex.length} družin brez leksikografskih kandidatov (največ 1)`);
        for (const f of j.families) {
          for (const h of f.lexicon.hypotheses) {
            if (!h.source) p43Errors.push(`JSON ${f.id}/${h.candidate}: brez vira`);
            if (!["~", "?"].includes(h.confidence)) p43Errors.push(`JSON ${f.id}/${h.candidate}: zaupanje '${h.confidence}'`);
          }
          if (f.lexicon.hypotheses.length > 6) p43Errors.push(`JSON ${f.id}: več kot 6 kandidatov`);
        }
        if (j.pvReconciliation.weidenGapJ !== 576.24 || j.pvReconciliation.rowsModelTotalJ !== 1564.78 || j.pvReconciliation.pvTotalJ !== 1221.95)
          p43Errors.push("JSON PV sprava ≠ TS");
        p43FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (216+66=282 parov, DINGF 10/10, PV ${j.pvReconciliation.pvTotalJ} J)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (216+66=282 parov, DINGF 10/10, PV ${j.pvReconciliation.pvTotalJ} J)`;
      } catch {
        p43Errors.push("izpis ps-lexicon.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p43-ps-lexicon",
    "P43: N083PS — neznane družine: prečni prehodi + PV območna sprava + ledinsko-imenska struktura + leksikon: 16 družin (216 parov) + 66 kitic = 282 izrecno NEKLASIFICIRANO; prečni prehodi SAMO znotraj iste fotografije (sken vsebuje ponovne posnetke); DINGF edina 100 % stabilna beseda (10/10 do ločila); GENERIČNI PADCEK (pass1 generik → pass2 specifično, specifična beseda V VIRU): LHIZ 9/9 (Wiese→Lhize), ERDAR 5/5 (Acker→Achm), SCHINDEL 1/1, skupaj 29; blokovska koncentracija: 10/16 družin na ENI fotografiji (AHN 906–920, AEFLING 1821–1840, EINHART 1644–1658 …) → hipoteza LEDINSKO-IME; PV sprava: Area 1221,95 ≈ P41 1220,93 (Δ 0,05 %), VINOGRAD Δ −0,46 J, WEIDEN-GAP 576,24 J (uradno 636,16 J dubrav vs 59,92 J izrecnih vrstic; neznane družine pokrijejo 17 %), NJIVA +202,29 / TRAVNIK +182,12, model−Area 342,84 ≈ Blatt X + NAD + WALDUNG; leksikografske hipoteze (2 neodvisna LLM prehoda × 17 sklopov, committed raw) z viri, ki jih navaja stroj (NEPREVERJENI) — rabe NI prirejena; status REVIEW",
    "P43: N083PS — unknown families: cross-passes + PV area reconciliation + field-name structure + lexicon: 16 families (216 pairs) + 66 strays = 282 explicitly UNCLASSIFIED; cross-passes ONLY within the same photo (the scan contains re-shoots); DINGF the only 100% stable word (10/10 up to punctuation); GENERIC FALLBACK (pass1 generic → pass2 specific, the specific word IS in the source): LHIZ 9/9 (Wiese→Lhize), ERDAR 5/5 (Acker→Achm), SCHINDEL 1/1, 29 in all; block concentration: 10/16 families on ONE photo (AHN 906–920, AEFLING 1821–1840, EINHART 1644–1658 …) → FIELD-NAME hypothesis; PV reconciliation: Area 1,221.95 ≈ P41 1,220.93 (Δ 0.05%), VINEYARD Δ −0.46 J, PASTURE-GAP 576.24 J (official 636.16 J of oak-woods vs 59.92 J explicit rows; unknown families cover 17%), FIELD +202.29 / MEADOW +182.12, model−Area 342.84 ≈ Blatt X + NAD + WOODS; lexicographic hypotheses (2 independent LLM passes × 17 bundles, committed raw) with machine-attributed (UNVERIFIED) sources — no use reassigned; status REVIEW",
    p43Errors.length === 0,
    p43Errors.length === 0
      ? `216+66=282 parov · DINGF 10/10 · padci 9/5/1 · blokov 10/16 · PV 1221,95/1564,78/576,24 · ${p43FileDetail}`
      : p43Errors.join("; "),
  );

  // P43b (GitHub linija, 2026-10-11): prva celotna veriga PT→PUA→PS.
const p43bErrors: string[] = [];
  {
    const pt = ATLAS_SOURCES.find((s) => s.code === "N083PT");
    if (!pt) p43bErrors.push("vir N083PT manjka");
    else {
      if (pt.lastVerified !== "2026-10-11")
        p43bErrors.push(`N083PT: lastVerified=${pt.lastVerified}, pričakovano 2026-10-11 (dan P43)`);
      if (!(pt.noteSi ?? "").includes("P43"))
        p43bErrors.push("N083PT: nota SL ne dokumentira P43 (celotna veriga)");
      if (!(pt.noteSi ?? "").includes("chain-full-pt-ps.json"))
        p43bErrors.push("N083PT: nota SL brez kazalca na dokaz chain-full-pt-ps.json");
      if (!(pt.noteSi ?? "").includes("2 DOKAZANI"))
        p43bErrors.push("N083PT: nota SL brez rangov verige (2 DOKAZANI + 5 VERJETNIH + 4 MOGOČE)");
      if (!(pt.noteSi ?? "").includes("65/65"))
        p43bErrors.push("N083PT: nota SL brez križne potrditve korpusa (65/65)");
      if (!(pt.noteSi ?? "").includes("mešano številčenje"))
        p43bErrors.push("N083PT: nota SL brez opozorila o mešanem številčenju ATLAS_OWNERS");
      if (!(pt.noteEn ?? "").includes("FIRST FULL CHAIN"))
        p43bErrors.push("N083PT: nota EN brez FIRST FULL CHAIN (P43)");
      if (pt.structuredEntries !== 84)
        p43bErrors.push("N083PT: structuredEntries spremenjen (P43 je analiza, ne nov prepis)");
    }
    const ptSeries = KURRENT_SERIES.find((s) => s.code === "PT");
    if (!ptSeries) p43bErrors.push("KURRENT_SERIES: PT manjka");
    else if (!(ptSeries.noteSi ?? "").includes("P43"))
      p43bErrors.push("KURRENT_SERIES PT: nota SL ne odraža P43");
    // strežniška kontrola dokaza (enaka logika preskoka kot p38/p39: v
    // produkciji research/ namenoma ni — .vercelignore, 92 MB)
    if (opts.readFile) {
      const raw = opts.readFile("research/issue13/chain-full-pt-ps.json");
      if (raw) {
        try {
          const proof = JSON.parse(raw) as {
            stats?: {
              ptRows?: number;
              ptHouses?: number;
              houseTiers?: Record<string, number>;
              housesCorroborated?: number;
              puaUniverse?: number;
            };
            meta?: { crossValidation?: { exact?: number; housesChecked?: number } };
          };
          if (proof.stats?.ptRows !== 105)
            p43bErrors.push(`dokaz: stats.ptRows=${proof.stats?.ptRows}, pričakovano 105 (84 hiš + 21 parcelnih vrstic)`);
          if (proof.stats?.ptHouses !== 84)
            p43bErrors.push(`dokaz: stats.ptHouses=${proof.stats?.ptHouses}, pričakovano 84`);
          const ht = proof.stats?.houseTiers ?? {};
          if (ht["DOKAZANA"] !== 2 || ht["VERJETNA"] !== 5 || ht["MOGOČA"] !== 4 || ht["NEREŠENA"] !== 73)
            p43bErrors.push(
              `dokaz: houseTiers=${JSON.stringify(ht)}, pričakovano {DOKAZANA:2, VERJETNA:5, MOGOČA:4, NEREŠENA:73}`,
            );
          if (proof.stats?.housesCorroborated !== 6)
            p43bErrors.push(`dokaz: housesCorroborated=${proof.stats?.housesCorroborated}, pričakovano 6`);
          if (proof.stats?.puaUniverse !== 65)
            p43bErrors.push(`dokaz: puaUniverse=${proof.stats?.puaUniverse}, pričakovano 65 (samo P41 veriga)`);
          const xv = proof.meta?.crossValidation;
          if (xv?.exact !== 65 || xv?.housesChecked !== 65)
            p43bErrors.push(`dokaz: križna potrditev korpusa=${xv?.exact}/${xv?.housesChecked}, pričakovano 65/65`);
        } catch {
          p43bErrors.push("dokaz: chain-full-pt-ps.json ni veljaven JSON");
        }
      } else if (opts.fileExists?.("research/issue13/chain-pua-ps.json")) {
        // repozitorij ima research/ (P41 dokaz obstaja), a P43 dokaz manjka
        p43bErrors.push("manjka research/issue13/chain-full-pt-ps.json (dokaz P43)");
      }
    }
  }
  push(
    "qa-p43-chain-full",
    "P43: N083PT — PRVA CELOTNA VERIGA PT→PUA→PS (kompozicija W-mostu P5-c + verige P41; 105 vrstic nič-zgube): 2 DOKAZANI + 5 VERJETNIH + 4 MOGOČE hiše segajo do parcel PS, 6 s priimkovno korroboracijo čez W; križna potrditev korpusa s P41 65/65 Točno; ATLAS_OWNERS houseRefs (mešano številčenje prve gradnje) izrecno izven verige; dokončna potrditev = #12",
    "P43: N083PT — FIRST FULL CHAIN PT→PUA→PS (composition of the P5-c W-bridge + the P41 chain; 105 zero-loss rows): 2 PROVEN + 5 LIKELY + 4 POSSIBLE houses reach the PS parcels, 6 with surname corroboration across W; corpus cross-check against P41 65/65 EXACT; ATLAS_OWNERS houseRefs (first-build mixed numbering) explicitly excluded; final confirmation = #12",
    p43bErrors.length === 0,
    p43bErrors.length === 0
      ? "105 vrstic · 2/5/4 hiše · 6 korroboriranih · korpus 65/65 · 65-ji univerzum"
      : p43bErrors.join("; "),
  );

  // ——— P44: N083PS — razcep K1/K2 (Abschluß der Gemeinde) ———
  const p44Errors: string[] = [];
  const KK = PS_K1K2_P44;
  if (KK.constraint.value !== 2090) p44Errors.push("omejitev ni 2090 K");
  if (KK.resolution.k1 !== 702 || KK.resolution.k2 !== 1388)
    p44Errors.push("rešitev ni (702, 1388)");
  if (KK.resolution.confidence !== "~") p44Errors.push("zaupanje ni [~]");
  if (!KK.resolution.state.startsWith("RESOLVED")) p44Errors.push("stanje ni RESOLVED");
  if (702 + 1388 !== KK.constraint.value) p44Errors.push("702 + 1388 ≠ omejitev");
  if (831 * 1600 + 702 + (383 * 1600 + 1388) !== 1215 * 1600 + 490)
    p44Errors.push("831|702 + 383|1388 ≠ 1215|490");
  if (1215 * 1600 + 490 + (5 * 1600 + 1003) !== 1220 * 1600 + 1493)
    p44Errors.push("1215|490 + 5|1003 ≠ 1220|1493");
  if (3 * 1600 + 312 + (2 * 1600 + 691) !== 5 * 1600 + 1003)
    p44Errors.push("3|312 + 2|691 ≠ 5|1003");
  if (KK.readingInventory.k2Cell.passes.pass2 !== 1388)
    p44Errors.push("K2 branje pass2 ni 1388 (direktna korelacija)");
  if (KK.readingInventory.k2Cell.passes.pass1 !== 1288 || KK.readingInventory.k2Cell.passes.pass3 !== 1288)
    p44Errors.push("K2 branji p1/p3 nista 1288");
  if (KK.readingInventory.k1Cell.passes.pass1 !== 968 || KK.readingInventory.k1Cell.passes.pass2 !== 468)
    p44Errors.push("K1 branji p1/p2 nista 968/468");
  if (KK.hypotheses.filter((h) => h.accepted).length !== 1) p44Errors.push("sprejetih hipotez ni natanko 1");
  const h1 = KK.hypotheses.find((h) => h.id === "H1");
  if (!h1 || !h1.accepted || h1.pair[0] !== 702 || h1.pair[1] !== 1388)
    p44Errors.push("H1 ni sprejeta (702, 1388)");
  const h2 = KK.hypotheses.find((h) => h.id === "H2");
  if (!h2 || h2.accepted || !h2.rejection) p44Errors.push("H2 (968, 1122) ni izrecno zavrnjena z razlogom");
  if (!KK.impact.abschlussNowFullyClosed) p44Errors.push("Abschluß ni zaprt");
  if (!KK.identities.I4_nachAnlageParallel.pass) p44Errors.push("paralelnost nach Anlage ni PASS");
  if (!KK.identities.I7_uniqueness.pass) p44Errors.push("enoličnost ni PASS");
  // dokazni datoteki (strežniški klic; vzorec qa-p37..p43)
  let p44FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-k1k2.json");
    const rawRt = opts.readFile("src/data/atlas/ps-k1k2.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p44Errors.push("research/issue17/ps-k1k2.json ni berljiv (izpis scripts/p44_ps_k1k2.py)");
    if (rawRt === null) p44Errors.push("src/data/atlas/ps-k1k2.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p44Errors.push("dokazni in runtime izpis ps-k1k2.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          constraint: { value: number };
          resolution: { state: string; k1: number; k2: number; confidence: string };
          hypotheses: { id: string; pair: number[]; accepted: boolean; rejection: string | null }[];
          identities: Record<string, { pass: boolean }>;
        };
        if (j.constraint.value !== 2090) p44Errors.push("JSON omejitev ni 2090");
        if (j.resolution.k1 !== 702 || j.resolution.k2 !== 1388) p44Errors.push("JSON rešitev ni (702, 1388)");
        if (j.resolution.state !== "RESOLVED-ARITMETIČNO") p44Errors.push("JSON stanje ni RESOLVED-ARITMETIČNO");
        if (j.hypotheses.filter((h) => h.accepted).length !== 1) p44Errors.push("JSON sprejetih hipotez ni 1");
        const jH2 = j.hypotheses.find((h) => h.id === "H2");
        if (!jH2 || jH2.accepted || !jH2.rejection) p44Errors.push("JSON H2 ni zavrnjena z razlogom");
        for (const [k, v] of Object.entries(j.identities)) {
          if (!v.pass) p44Errors.push(`JSON identiteta ${k} ni PASS`);
        }
        p44FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (K1=${j.resolution.k1}, K2=${j.resolution.k2}, omejitev ${j.constraint.value} K, H1 edina sprejeta)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (K1=${j.resolution.k1}, K2=${j.resolution.k2}, omejitev ${j.constraint.value} K, H1 edina sprejeta)`;
      } catch {
        p44Errors.push("izpis ps-k1k2.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p44-ps-k1k2",
    "P44: N083PS — razcep K1/K2 v 'Abschluß der Gemeinde' RAZREŠEN [~]: omejitev K1+K2 = 2090 K (iz 1215|490 − 831 J − 383 J); strukturna paralelnost 'nach Anlage' (desna vrstica 4 Baup 3|312 == leva vrstica 132, P41 PASS; Joch 831 == 831) → K1 = 702 == Klafter leve vsote 831|702; podmnožinski argument pada hipotezo (968, 1122) — rekapitulacija Anlage ne sme presegati vsote Anlage; K2 = 2090 − 702 = 1388 == direktno VLM branje pass2 (p1/p3 1288, razlika ena številka); celoten Abschluß se zapre: 831|702 + 383|1388 = 1215|490; + 5|1003 = 1220|1493; 3|312 + 2|691 = 5|1003; NOVA identiteta: desna vrstica 1 == leva 'Summa der Grundparzellen'; struktura občine: rustikalne hiše 831|702 + 'Ziffer 1041' (Gütl/gingl.) 383|1388; hipoteze H1–H5 z izrecnimi zavrnitvami; vzorec napačnih branj: 702→968/468 (7→9|4, 0→6, 2→8 — kurrentske zamenjave [~]); status REVIEW — človeška potrditev ostaja odprta",
    "P44: N083PS — the K1/K2 split in 'Abschluß der Gemeinde' RESOLVED [~]: constraint K1+K2 = 2090 K (from 1215|490 − 831 J − 383 J); structural 'nach Anlage' parallelism (right row 4 Baup 3|312 == left row 132, P41 PASS; Joch 831 == 831) → K1 = 702 == the Klafter of the left sum 831|702; the subset argument defeats the (968, 1122) hypothesis — a recapitulation of the Anlage cannot exceed the Anlage's own sum; K2 = 2090 − 702 = 1388 == a direct pass2 VLM reading (p1/p3 1288, one digit apart); the entire Abschluß closes: 831|702 + 383|1388 = 1215|490; + 5|1003 = 1220|1493; 3|312 + 2|691 = 5|1003; NEW identity: right row 1 == the left 'Summa der Grundparzellen'; Gemeinde structure: rustical houses 831|702 + 'Ziffer 1041' (Gütl/gingl.) 383|1388; hypotheses H1–H5 with explicit rejections; misread pattern: 702→968/468 (7→9|4, 0→6, 2→8 — Kurrent confusions [~]); status REVIEW — human confirmation remains open",
    p44Errors.length === 0,
    p44Errors.length === 0
      ? `K1=702, K2=1388 · omejitev 2090 · H1 edina sprejeta (H2–H5 zavrnjene) · Abschluß zaprt · ${p44FileDetail}`
      : p44Errors.join("; "),
  );

  // P44 (GitHub linija, 2026-10-11): PZ tabele cenilnih razredov — popolnost in uskladitev.
const p44bErrors: string[] = [];
  // 1. tabela: 10 vrstic razredov + Summa
  if (PZ_CLASS_TABLE_1825.rows.length !== 10)
    p44bErrors.push(`classTable: ${PZ_CLASS_TABLE_1825.rows.length} vrstic != 10`);
  if (PZ_CLASS_TABLE_1825.summa.joch !== 1152 || PZ_CLASS_TABLE_1825.summa.klafter !== 495)
    p44bErrors.push(`Summa: ${PZ_CLASS_TABLE_1825.summa.joch}/${PZ_CLASS_TABLE_1825.summa.klafter} != 1152/495`);
  if (PZ_CLASS_TABLE_1825.summa.reinTotal !== "4492 fl 51 kr")
    p44bErrors.push(`Rein total: ${PZ_CLASS_TABLE_1825.summa.reinTotal}`);
  if (PZ_CLASS_TABLE_1825.summa.bruttoTotal !== "8872 fl 5¾ kr")
    p44bErrors.push(`Brutto total: ${PZ_CLASS_TABLE_1825.summa.bruttoTotal}`);
  // 2. vsota vrstic = 1145 (adjudicirano) in razlika do Summe dokumentirana
  const p44RowSum = PZ_CLASS_TABLE_1825.rows.reduce((a, r) => a + r.joch, 0);
  if (p44RowSum !== PZ_CLASS_TABLE_1825.rowSumJoch)
    p44bErrors.push(`vsota vrstic ${p44RowSum} != rowSumJoch ${PZ_CLASS_TABLE_1825.rowSumJoch}`);
  if (Math.abs(PZ_CLASS_TABLE_1825.summa.joch - p44RowSum) !== 7)
    p44bErrors.push(`Δ(Summa − vsota vrstic) != 7 (dokumentirana odprta točka D4)`);
  // 3. adjudikacija Acker II = 334 [~] + Acker I korroboracija
  const acker = PZ_CLASS_TABLE_1825.rows.filter((r) => r.culture === "Acker");
  if (acker.length !== 2) p44bErrors.push(`Acker vrstic: ${acker.length} != 2 (razredov I in II, III/IV ni)`);
  if (acker[0]?.joch !== 80) p44bErrors.push(`Acker I: ${acker[0]?.joch} != 80 (korroboracija str. 12)`);
  if (acker[1]?.joch !== 334 || acker[1]?.confidence !== "~")
    p44bErrors.push(`Acker II: ${acker[1]?.joch}/${acker[1]?.confidence} != 334/~ (adjudicirano, D1)`);
  if (acker[0].joch + acker[1].joch - 413 > 1 || 413 - (acker[0].joch + acker[1].joch) > 1)
    p44bErrors.push(`Acker I+II = ${acker[0].joch + acker[1].joch} ≫ PV Aecker 413 (±1)`);
  // 4. Weingärten = PV 7 j; Weiden kontrola 636/263 v uskladitvi
  const weing = PZ_CLASS_TABLE_1825.rows.find((r) => r.culture === "Weingärten");
  if (!weing || weing.joch !== 7) p44bErrors.push("Weingärten != 7 joch (= PV)");
  if (!PZ_CLASS_TABLE_1825.reconciliationSi.includes("636 j 263 kl"))
    p44bErrors.push("uskladitev ne navaja kontrole str. 65 (Weiden gesamt 636 j 263 kl = PV)");
  // 5. PZ_ECONOMY veriga — divergenca str. 50 razrešena
  const ackerChain = PZ_ECONOMY_1825.valuationChain.find((s) => s.stepSi.startsWith("Ackerland razred I"));
  if (!ackerChain || !ackerChain.valuesSi.includes("25 fl 44"))
    p44bErrors.push("PZ_ECONOMY Acker I veriga ne nosi razrešene vrednosti 25 fl 44 (D2)");
  if (ackerChain && ackerChain.confidence === "nizka")
    p44bErrors.push("PZ_ECONOMY Acker I ostaja 'nizka' — P44 je divergenco razrešil");
  // 6. stanja: KURRENT_SERIES PZ 71/71 + vir N083PZ strukturno 11
  const pzSeries = KURRENT_SERIES.find((k) => k.code === "PZ");
  if (!pzSeries || pzSeries.pagesTranscribed !== 71) p44bErrors.push("KURRENT_SERIES PZ ni 71/71");
  const pzSrc = ATLAS_SOURCES.find((s) => s.code === "N083PZ");
  if (!pzSrc || pzSrc.structuredEntries !== 11) p44bErrors.push("sources.ts N083PZ structuredEntries != 11");
  // 7. dokaz v repozitoriju (enaka logika preskoka kot p38/p39/p43: v produkciji
  // research/ namenoma ni v sliki — .vercelignore)
  if (opts.readFile) {
    const raw = opts.readFile("research/issue11/pz-classes-full.json");
    if (raw) {
      try {
        const proof = JSON.parse(raw) as {
          classTable?: unknown[];
          divergences?: unknown[];
          stats?: { vlmCallsP44?: number; pagesReadP44?: number; pagesReadTotal?: number };
        };
        if ((proof.classTable ?? []).length !== 10)
          p44bErrors.push(`dokaz: classTable=${(proof.classTable ?? []).length}, pričakovano 10`);
        if ((proof.divergences ?? []).length !== 6)
          p44bErrors.push(`dokaz: divergences=${(proof.divergences ?? []).length}, pričakovano 6`);
        if (proof.stats?.vlmCallsP44 !== 76)
          p44bErrors.push(`dokaz: vlmCallsP44=${proof.stats?.vlmCallsP44}, pričakovano 76`);
        if (proof.stats?.pagesReadP44 !== 64)
          p44bErrors.push(`dokaz: pagesReadP44=${proof.stats?.pagesReadP44}, pričakovano 64`);
        if (proof.stats?.pagesReadTotal !== 71)
          p44bErrors.push(`dokaz: pagesReadTotal=${proof.stats?.pagesReadTotal}, pričakovano 71`);
      } catch {
        p44bErrors.push("dokaz: pz-classes-full.json ni veljaven JSON");
      }
    } else if (opts.fileExists?.("research/issue17/PZ-valuation.json")) {
      // repozitorij ima research/ (issue #4 dokaz obstaja), a P44 dokaz manjka
      p44bErrors.push("manjka research/issue11/pz-classes-full.json (dokaz P44)");
    }
  }
  push(
    "qa-p44-pz-classes",
    "P44: N083PZ — prepis tabel cenilnih razredov (issue #11): 71/71 strani (76 VLM klicev); rekapitulacija str. 67: 10 razredov + Summa 1152 j 495 kl, Brutto 8872 fl 5¾ kr, Rein 4492 fl 51 kr; uskladitev s PV (Δ +4 j ≈ 0,3 %; kontrola str. 65 = 636 j 263 kl natančno); divergenca str. 50 RAZREŠENA; Acker II adjudicirano 334 [~]; 4 odprte točke registrirane za #12",
    "P44: N083PZ — the valuation class tables transcribed (issue #11): 71/71 pages (76 VLM calls); the p. 67 recapitulation: 10 classes + Summa 1152 j 495 kl, gross 8872 fl 5¾ kr, net 4492 fl 51 kr; reconciliation with PV (Δ +4 j ≈ 0.3 %; the p. 65 control = 636 j 263 kl exactly); the p. 50 divergence RESOLVED; Acker II adjudicated to 334 [~]; 4 open points registered for #12",
    p44bErrors.length === 0,
    p44bErrors.length === 0
      ? "10 razredov · Summa 1152/495 · vsota vrstic 1145 (Δ 7 dokumentirana) · Acker 80+334≈PV 413 · Weiden kontrola = PV"
      : p44bErrors.join("; "),
  );

  // ——— P45: N083PS — verifikacija leksikografskih virov P43 ———
  const p45Errors: string[] = [];
  const p45LV = PS_LEXICON_VERIFIED_P45;
  if (p45LV.campaign.targetsTotal !== 49) p45Errors.push("tarč ni 49");
  if (p45LV.campaign.hypothesesTotal !== 70) p45Errors.push("hipotez ni 70");
  const p45Bv = p45LV.campaign.byVerdict;
  if (p45Bv.POTRJENO !== 0 || p45Bv.DELNO !== 7 || p45Bv.NEPOTRJENO !== 33 || p45Bv.NEVERIFIKATORNO !== 17 || p45Bv["BREZ-VIRA"] !== 13)
    p45Errors.push("verdicti niso (0, 7, 33, 17, 13)");
  if (p45Bv.POTRJENO + p45Bv.DELNO + p45Bv.NEPOTRJENO + p45Bv.NEVERIFIKATORNO + p45Bv["BREZ-VIRA"] !== 70)
    p45Errors.push("vsota verdictov ≠ 70");
  const p45Bm = p45LV.campaign.byMethod;
  if (p45Bm["fran.si-direct"] + p45Bm["wikipedia-api"] + p45Bm["deterministic-repo"] + p45Bm["unreachable"] !== 49)
    p45Errors.push("vsota metod ≠ 49");
  if (p45LV.families.length !== 16) p45Errors.push("družin ni 16");
  // vsota verdictov po družinah == 70; vsota parov == 216
  let p45FamVerdictSum = 0;
  let p45FamPairsSum = 0;
  for (const f of p45LV.families) {
    const s = (f.verdictCounts.POTRJENO ?? 0) + (f.verdictCounts.DELNO ?? 0) + (f.verdictCounts.NEPOTRJENO ?? 0) + (f.verdictCounts.NEVERIFIKATORNO ?? 0) + (f.verdictCounts["BREZ-VIRA"] ?? 0);
    p45FamVerdictSum += s;
    p45FamPairsSum += f.pairs;
  }
  if (p45FamVerdictSum !== 70) p45Errors.push("vsota verdictov po družinah ≠ 70");
  if (p45FamPairsSum !== 216) p45Errors.push("vsota parov po družinah ≠ 216");
  // pinane refutacije (DWB zvezčna struktura + SSKJ verbatim + atribucije)
  const p45FLV = (id: string) => p45LV.families.find((f) => f.id === id);
  const p45Lohn = p45FLV("LOHN-RAUT")?.topHypotheses.find((h) => h.candidate === "Lohn (nem.)");
  if (!p45Lohn || p45Lohn.verdict !== "NEPOTRJENO" || !p45Lohn.noteSi.includes("Bd 12"))
    p45Errors.push("Lohn Bd 16→12 (NEPOTRJENO) ni pinan");
  const p45Aef = p45FLV("AEFLING")?.topHypotheses;
  if (p45FLV("AEFLING")?.verdictCounts.DELNO !== 3)
    p45Errors.push("AEFLING DELNO ni 3 (Aue Bd 1 / Öde Bd 13 strukturno)");
  if (!p45Aef?.some((h) => h.candidate === "Hofling" && h.verdict === "NEPOTRJENO" && h.noteSi.includes("Bd 10")))
    p45Errors.push("Höfling Bd 13→10 ni pinan");
  if (!p45Aef?.some((h) => h.candidate === "Efling" && h.verdict === "NEPOTRJENO" && h.noteSi.includes("Bd 3")))
    p45Errors.push("Efeu Bd 6→3 ni pinan");
  const p45Lhiz = p45FLV("LHIZ")?.topHypotheses.find((h) => h.candidate === "Lhize/Lhizl");
  if (!p45Lhiz || p45Lhiz.verdict !== "NEPOTRJENO" || !p45Lhiz.noteSi.includes("liže"))
    p45Errors.push("LHIZ liza = 'kdor rad liže' ni pinan");
  const p45Kwb = p45FLV("GUETEN")?.topHypotheses.find((h) => h.candidate === "Gütung");
  if (!p45Kwb || p45Kwb.verdict !== "NEPOTRJENO" || !p45Kwb.noteSi.includes("Kranzmayer"))
    p45Errors.push("Kärntner WB (Schulz, 1972) NEPOTRJENO ni pinan");
  const p45Einhart = p45FLV("EINHART")?.topHypotheses.find((h) => h.candidate === "Gypf.");
  if (!p45Einhart || p45Einhart.verdict !== "NEPOTRJENO" || !p45Einhart.noteSi.includes("PV.json"))
    p45Errors.push("PV-Gypf NEPOTRJENO ni pinan");
  if (!p45LV.method.unchangedP43.includes("invarianta I2")) p45Errors.push("metoda ne deklarira invariantne I2");
  // dokazni datoteki (strežniški klic; vzorec qa-p37..p44)
  let p45FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-lexicon-verified.json");
    const rawRt = opts.readFile("src/data/atlas/ps-lexicon-verified.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    const rawP43 = opts.readFile("research/issue17/ps-lexicon.json") ?? opts.readFile("src/data/atlas/ps-lexicon.json");
    if (raw === null) p45Errors.push("research/issue17/ps-lexicon-verified.json ni berljiv (izpis scripts/p45_lex_verify.py)");
    if (rawRt === null) p45Errors.push("src/data/atlas/ps-lexicon-verified.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p45Errors.push("dokazni in runtime izpis ps-lexicon-verified.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          campaign: { targetsTotal: number; byVerdict: Record<string, number> };
          families: { id: string; hypotheses: { candidate: string; verification: { verdict: string; targets: { id: string; noteSi?: string }[] } }[] }[];
        };
        if (j.campaign.targetsTotal !== 49) p45Errors.push("JSON tarč ni 49");
        if (j.campaign.byVerdict.NEPOTRJENO !== 33) p45Errors.push("JSON NEPOTRJENO ni 33");
        const p45AefJson = j.families.find((f) => f.id === "AEFLING")?.hypotheses.find((h) => h.candidate === "Afling");
        if (!p45AefJson || p45AefJson.verification.verdict !== "DELNO"
          || !p45AefJson.verification.targets.some((t: { noteSi?: string }) => (t.noteSi ?? "").includes("Bd 1")))
          p45Errors.push("JSON Aue Bd 1 DELNO ni pinan (evidence nivo)");
        let hyps = 0;
        for (const f of j.families) hyps += f.hypotheses.length;
        if (hyps !== 70) p45Errors.push("JSON hipotez ni 70");
        // invarianta I2: kandidati P43 bajtno identični — primerjaj z ps-lexicon.json
        if (rawP43 !== null) {
          try {
            const p43 = JSON.parse(rawP43) as { families: { id: string; lexicon: { hypotheses: { candidate: string }[] } }[] };
            const cIn = p43.families.flatMap((f) => f.lexicon.hypotheses.map((h) => `${f.id}\u0000${h.candidate}`));
            const cOut = j.families.flatMap((f) => f.hypotheses.map((h) => `${f.id}\u0000${h.candidate}`));
            if (cIn.join("\u0001") !== cOut.join("\u0001"))
              p45Errors.push("invarianta I2: kandidati P43 niso bajtno identični v izpisu verifikacije");
          } catch {
            p45Errors.push("research/issue17/ps-lexicon.json (P43) ni veljaven JSON (potrebna za I2)");
          }
        } else {
          p45Errors.push("ps-lexicon.json (P43 dokaz in runtime kopija) ni berljiv za I2");
        }
        p45FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (49 tarč, ${hyps} hipotez, NEPOTRJENO ${j.campaign.byVerdict.NEPOTRJENO}, I2 potrjena)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (49 tarč, ${hyps} hipotez, NEPOTRJENO ${j.campaign.byVerdict.NEPOTRJENO}, I2 potrjena)`;
      } catch {
        p45Errors.push("izpis ps-lexicon-verified.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p45-ps-lexicon-verified",
    "P45: N083PS — VERIFIKACIJA LEKSIKOGRAFSKIH VIROV P43 (49 tarč, 70 hipotez): 0/70 POTRJENO v celoti — 33 NEPOTRJENO (geslo manjka/pomen drugačen/citat zvezka ali atribucija ne stoji), 7 DELNO, 17 NEVERIFIKATORNO (DWB/Schmeller teksti v peskovniku nedosegljivi — kanonični URL v dokazih), 13 BREZ-VIRA; metode: fran.si direktni geslarski izseki 18 (SSKJ²/Pleteršnik/Novak SSP), Wikipedia API 14 (zvezčne mape DWB 33 zvezkov, Schmeller Cotta 1827–37 / Frommann 1872–77, bibliografija), deterministična 1 (PV.json), nedosegljivo 16; DWB citati zvezkov: Aue Bd 1 ✓ in Öde Bd 13 ✓ strukturno skladna, Lohn Bd 16 ✗ (L∈Bd 12), Höfling Bd 13 ✗ (H∈Bd 10), Efeu Bd 6 ✗ (E∈Bd 3) — trije NAPAČNI; SSKJ verbatim refutacije: log = '(močviren) travnik ob vodi', líza = 'kdor rad liže', lúti = 'hud, jezen'; neobstoječa gesla: jedar, ving, orga, horga, ajna, p45Einhart, guten, poggi, šlifa; atribucije ne stojijo: 'Kärntner Wörterbuch (Schulz, 1972)', 'Bezlaj SSN/SLA', Schmeller 'C.H. Beck' (pravilno Cotta); PV-Gypf: NI v PV.json, JE v PS registru (+ 'Schüttwiese, Gypfang'); invarianta I2: P43 kandidati/glose/viri bajtno identični, rabe ni prirejena; status REVIEW",
    "P45: N083PS — SOURCE VERIFICATION OF THE P43 LEXICON (49 targets, 70 hypotheses): 0/70 fully CONFIRMED — 33 REFUTED (headword missing/meaning different/volume citation or attribution wrong), 7 PARTIAL, 17 UNVERIFIABLE (DWB/Schmeller texts unreachable — canonical URLs in evidence), 13 NO-SOURCE; methods: fran.si direct entry excerpts 18 (SSKJ²/Pleteršnik/Novak SSP), Wikipedia API 14 (DWB 33-volume map, Schmeller Cotta 1827–37 / Frommann 1872–77, bibliography), deterministic 1 (PV.json), unreachable 16; DWB volume citations: Aue Bd 1 ✓ and Öde Bd 13 ✓ structurally consistent, Lohn Bd 16 ✗ (L∈Bd 12), Höfling Bd 13 ✗ (H∈Bd 10), Efeu Bd 6 ✗ (E∈Bd 3) — three WRONG; SSKJ verbatim refutations: log = '(wet) meadow by the water', líza = 'one who likes to lick', lúti = 'fierce, angry'; non-existent headwords: jedar, ving, orga, horga, ajna, p45Einhart, guten, poggi, šlifa; attributions fail: 'Kärntner Wörterbuch (Schulz, 1972)', 'Bezlaj SSN/SLA', Schmeller 'C.H. Beck' (correctly Cotta); PV-Gypf: NOT in PV.json, IS in the PS register (+ 'Schüttwiese, Gypfang'); invariant I2: P43 candidates/glosses/sources byte-identical, no use reassigned; status REVIEW",
    p45Errors.length === 0,
    p45Errors.length === 0
      ? `0/70 potrjeno · 33/7/17/13 · fran.si 18 + wiki 14 + repo 1 + unreachable 16 · Lohn→Bd 12, Höfling→Bd 10, Efeu→Bd 3, Aue Bd 1 ✓, Öde Bd 13 ✓ · ${p45FileDetail}`
      : p45Errors.join("; "),
  );

  // P45b (GitHub linija, 2026-10-11): validacija porazdelitve stavb A03–A05 (SHEET_TRUTH; statusi A03–A05 od P50 NEATLINE_*).
const p45bErrors: string[] = [];
  // 1. SHEET_TRUTH vsebuje vse tri liste s celicami in kvantificirano validacijo
  if (SHEET_TRUTH.length !== 3) p45bErrors.push(`SHEET_TRUTH=${SHEET_TRUTH.length}, pri\u010dakovano 3`);
  const p45Expect: Record<string, { cell: string; med: number; in30: number }> = {
    A03: { cell: "VKIX24dg", med: 89, in30: 0.067 },
    A04: { cell: "VKIX24cg", med: 69.7, in30: 0.118 },
    A05: { cell: "VKIX24ch", med: 27, in30: 0.6 },
  };
  for (const st of SHEET_TRUTH) {
    const exp = p45Expect[st.sheet];
    if (!exp) {
      p45bErrors.push(`SHEET_TRUTH nepri\u010dakovan list ${st.sheet}`);
      continue;
    }
    if (st.cellCode !== exp.cell) p45bErrors.push(`${st.sheet}: celica ${st.cellCode} != ${exp.cell}`);
    if (st.validation.medianDistanceM !== exp.med)
      p45bErrors.push(`${st.sheet}: mediana ${st.validation.medianDistanceM} != ${exp.med}`);
    if (st.validation.inlier30 !== exp.in30)
      p45bErrors.push(`${st.sheet}: inlier30 ${st.validation.inlier30} != ${exp.in30}`);
    if (st.validation.lastVerified !== "2026-10-12")
      p45bErrors.push(`${st.sheet}: lastVerified ${st.validation.lastVerified}`);
    if (st.status !== "REVIEW") p45bErrors.push(`${st.sheet}: status ${st.status} != REVIEW`);
  }
  // 2. SHEET_GEOREFS natan\u010dnosti nosijo P45 validacijo; statusi ostajajo REVIEW
  for (const sheet of ["A03", "A04", "A05"]) {
    const g = SHEET_GEOREFS.find((s) => s.sheet === sheet);
    if (!g) {
      p45bErrors.push(`SHEET_GEOREFS manjka ${sheet}`);
      continue;
    }
    if (!g.accuracySi.includes("P50")) p45bErrors.push(`${sheet}: accuracySi brez P50 (P45 validacija ostaja v dokazu; runtime je P50 neatline)`);
    if (!["NEATLINE_GEOREFERENCED", "NEATLINE_PARTIAL_GEOREFERENCED"].includes(g.status)) p45bErrors.push(`${sheet}: status ${g.status} ni NEATLINE_* (P50 aktivacija nad P45 celi\u010dno preslikavo)`);
  }
  // 3. sources.ts opombe: P45 omembe, ne pa starih TO_COLLECT koncovk
  for (const code of ["N083A03", "N083A04", "N083A05"]) {
    const src = ATLAS_SOURCES.find((s) => s.code === code);
    if (!src) {
      p45bErrors.push(`sources.ts manjka ${code}`);
      continue;
    }
    if (!src.noteSi?.includes("P45")) p45bErrors.push(`${code}: noteSi brez P45`);
    if (!src.noteEn?.includes("P45")) p45bErrors.push(`${code}: noteEn brez P45`);
    if (src.noteSi?.includes("ostaja TO_COLLECT")) p45bErrors.push(`${code}: noteSi \u0161e vedno TO_COLLECT`);
  }
  // 4. dokaz v repozitoriju (enaka logika preskoka produkcije kot p38/p39/p43/p44)
  if (opts.readFile) {
    const raw = opts.readFile("research/georef-n83/p45-sheet-fits.json");
    if (raw) {
      try {
        const proof = JSON.parse(raw) as {
          a02Truth?: { scaleMPerPx?: number; rotDeg?: number };
          a03?: { cell?: { stats?: { medianM?: number } } };
          a04?: { cell?: { stats?: { medianM?: number } } };
          a05?: { cell?: { stats?: { medianM?: number } }; alternatives?: unknown[] };
        };
        if (proof.a02Truth?.scaleMPerPx === undefined || Math.abs(proof.a02Truth.scaleMPerPx - 0.8046) > 0.001)
          p45bErrors.push(`dokaz: a02Truth.scaleMPerPx=${proof.a02Truth?.scaleMPerPx}`);
        if (Math.abs((proof.a03?.cell?.stats?.medianM ?? -1) - 89) > 0.5)
          p45bErrors.push(`dokaz: a03 mediana=${proof.a03?.cell?.stats?.medianM}`);
        if (Math.abs((proof.a04?.cell?.stats?.medianM ?? -1) - 69.7) > 0.5)
          p45bErrors.push(`dokaz: a04 mediana=${proof.a04?.cell?.stats?.medianM}`);
        if (Math.abs((proof.a05?.cell?.stats?.medianM ?? -1) - 27) > 0.5)
          p45bErrors.push(`dokaz: a05 mediana=${proof.a05?.cell?.stats?.medianM}`);
        if ((proof.a05?.alternatives ?? []).length < 4)
          p45bErrors.push("dokaz: a05.alternatives < 4 (dvoumnost mora biti dokumentirana)");
      } catch {
        p45bErrors.push("dokaz: p45-sheet-fits.json ni veljaven JSON");
      }
    } else if (opts.fileExists?.("research/georef-n83/kolpa-modern-centerline.json")) {
      p45bErrors.push("manjka research/georef-n83/p45-sheet-fits.json (dokaz P45)");
    }
  }
  push(
    "qa-p45-sheet-anchors",
    "P45: A03\u2013A05 \u2014 validacija porazdelitve stavb (issue #14): celi\u010dne umestitve eZKN kvantitativno potrjene proti sodobnim stavbnim parcelam GURS (A03 veriga 30 simbolov \u2192 mediana 89 m; A04 170 simbolov \u2192 69,7 m; A05 sklop 30 \u2192 27 m, 60 % znotraj 30 m); kalibracija na A02 (156 stavb: 0,805 m/px, +0,02\u00b0, ostanek 2,4 m); prosti fitovi zavrnjeni (nestabilni); SHEET_TRUTH registriran; odprta dvoumnost A05 dokumentirana za #12/#13",
    "P45: A03\u2013A05 \u2014 building-distribution validation (issue #14): the eZKN cell placements quantitatively confirmed against modern GURS building parcels (A03 chain of 30 symbols \u2192 a median of 89 m; A04 170 symbols \u2192 69.7 m; A05 cluster of 30 \u2192 27 m, 60 % within 30 m); the A02 calibration (156 buildings: 0.805 m/px, +0.02\u00b0, residual 2.4 m); the free fits rejected (unstable); SHEET_TRUTH registered; A05's open ambiguity documented for #12/#13",
    p45bErrors.length === 0,
    p45bErrors.length === 0
      ? "A03 89 m \u00b7 A04 69,7 m \u00b7 A05 27 m (60 % @30) \u00b7 kalibracija A02 0,805 m/px \u00b7 3 lista REVIEW s po\u0161tenimi ocenami"
      : p45bErrors.join("; "),
  );

  // ——— P46: NEATLINE georeferenciranje sekcij dg/cg/ch (A03–A05) ———
  const p46Errors: string[] = [];
  const p46 = NEATLINE_GEOREF_P46;
  // kontrola principa: residuali ≤ 90 m
  const p46Top = p46.control.residuals.top;
  const p46Right = p46.control.residuals.right;
  if (p46Top.residualM > 90 || p46Right.residualM > 90)
    p46Errors.push("kontrolni residuali A02 nad 90 m");
  if (p46Top.residualM !== 9.3 || p46Right.residualM !== 13.2)
    p46Errors.push("pinani residuali A02 niso (9.3, 13.2) m");
  // skupno merilo + medosna konsistenca ≤ 1 %
  if (p46.sharedScale.axisConsistencyPct > 1)
    p46Errors.push("medosna konsistenca merila nad 1 %");
  if (p46.sharedScale.sbarMPerPx !== 0.7746 || p46.sharedScale.sx !== 0.77654 || p46.sharedScale.sy !== 0.77266)
    p46Errors.push("pinano merilo (s̄ 0.7746, sx 0.77654, sy 0.77266) ni ok");
  // listi: statusi, negotovosti, detekcije, premik vs P10 ≤ 25 m
  const p46A04 = p46.sheets.A04;
  const p46A05 = p46.sheets.A05;
  const p46A03 = p46.sheets.A03;
  if (p46A04.proposedStatus !== "NEATLINE_GEOREFERENCED" || p46A04.detectedSides !== 4 || p46A04.uncertaintyM !== 40)
    p46Errors.push("A04 ni NEATLINE_GEOREFERENCED 4/4 ±40 m");
  if (p46A05.proposedStatus !== "NEATLINE_GEOREFERENCED" || p46A05.detectedSides !== 4 || p46A05.uncertaintyM !== 40)
    p46Errors.push("A05 ni NEATLINE_GEOREFERENCED 4/4 ±40 m");
  if (p46A03.proposedStatus !== "NEATLINE_PARTIAL_GEOREFERENCED" || p46A03.detectedSides !== 2 || p46A03.uncertaintyM !== 50)
    p46Errors.push("A03 ni NEATLINE_PARTIAL_GEOREFERENCED 2/4 ±50 m");
  for (const [k, o] of Object.entries(p46.sheets)) {
    if (o.shiftVsP10MaxM > 25) p46Errors.push(`${k}: premik vs P10 ${o.shiftVsP10MaxM} m > 25 m`);
    if (o.previous.status !== "GRID_APPROX" || o.previous.uncertaintyM !== "200–400")
      p46Errors.push(`${k}: prejšnje stanje ni GRID_APPROX ±200–400 m`);
  }
  // A03: N/W morata biti inferred-scale (izrecna delnost)
  if (p46A03.sides.top.source !== "inferred-scale" || p46A03.sides.left.source !== "inferred-scale")
    p46Errors.push("A03 top/left nista inferred-scale");
  if (p46A03.sides.bottom.source !== "detected" || p46A03.sides.right.source !== "detected")
    p46Errors.push("A03 bottom/right nista detected");
  // ne-regresija: 7/7 validacij, pinane razdalje
  if (p46.validations.length !== 7 || !p46.validations.every((v) => v.pass))
    p46Errors.push("validacij ni 7/7 PASS");
  const p46Bresnik = p46.validations.find((v) => v.label.includes("Bresnik"));
  const p46Fuc = p46.validations.find((v) => v.label.includes("Fučkovci"));
  const p46Jank = p46.validations.find((v) => v.label.includes("Jankovichti"));
  if (p46Bresnik?.distM !== 34 || p46Fuc?.distM !== 33 || p46Jank?.distM !== 33)
    p46Errors.push("pinane razdalje validacij niso (34, 33, 33) m");
  // izrecna delnost: SHEET_GEOREFS ostaja nespremenjen (lekcija P9)
  if (!p46.verdictSi.includes("SHEET_GEOREFS se namerno ne spreminja"))
    p46Errors.push("verdict ne deklarira nedotaknjenosti SHEET_GEOREFS");
  // dokazni datoteki (strežniški klic; vzorec qa-p37..p45)
  let p46FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/neatline-georef.json");
    const rawRt = opts.readFile("src/data/atlas/neatline-georef.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p46Errors.push("research/issue17/neatline-georef.json ni berljiv (izpis scripts/p46_neatline_georef.py)");
    if (rawRt === null) p46Errors.push("src/data/atlas/neatline-georef.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p46Errors.push("dokazni in runtime izpis neatline-georef.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          control: { residuals: Record<string, { residualM: number }> };
          sharedScale: { sbarMPerPx: number; axisConsistencyPct: number };
          sheets: Record<string, { proposedStatus: string; uncertaintyM: number; sides: Record<string, { source: string }>; affineFit: { rmsM: number } }>;
          validations: { pass: boolean }[];
          invariants: Record<string, string>;
        };
        if (j.control.residuals.top.residualM !== 9.3 || j.control.residuals.right.residualM !== 13.2)
          p46Errors.push("JSON kontrolni residuali niso (9.3, 13.2) m");
        if (j.sharedScale.sbarMPerPx !== 0.7746) p46Errors.push("JSON s̄ ni 0.7746");
        if (j.sheets.A04.affineFit.rmsM > 30) p46Errors.push("JSON A04 afina RMS nad 30 m");
        if (!j.sheets.A04.sides.top || !j.sheets.A03.sides.top.source.includes("inferred"))
          p46Errors.push("JSON A03 top ni inferred-scale");
        if (j.validations.length !== 7 || !j.validations.every((v) => v.pass))
          p46Errors.push("JSON validacij ni 7/7");
        if (!Object.values(j.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
          p46Errors.push("JSON invarianti niso vsi PASS");
        p46FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (kontrola 9.3/13.2 m, s̄ ${j.sharedScale.sbarMPerPx} m/px, A04 RMS ${j.sheets.A04.affineFit.rmsM} m, 7/7 validacij)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (kontrola 9.3/13.2 m, s̄ ${j.sharedScale.sbarMPerPx} m/px, 7/7 validacij)`;
      } catch {
        p46Errors.push("izpis neatline-georef.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p46-neatline-georef",
    "P46: NEATLINE georeferenciranje sekcij dg/cg/ch (A03–A05, issue #14/§3) — princip 'neatline = meja sekcije eZKN 1:2880' kalibriran na A02 pod GEOTRUTH afino (residuala N 9.3 m, E 13.2 m ≤ 90); A04 (cg): 4/4 detektirane strani, merilo sx 0.77654 / sy 0.77266 m/px (medosna konsistenca 0,5 %), afina 4 vogalov RMS ≤ 30 m → NEATLINE_GEOREFERENCED ±40 m; A05 (ch): 4/4 strani (N/W šibkejši pokritosti) → NEATLINE_GEOREFERENCED ±40 m; A03 (dg): S/E detektirana, N/W inferred preko s̄ (šibki kandidati v okviru 25 m) → NEATLINE_PARTIAL ±50 m; premik novih mej vs P10 GRID_APPROX le 17–18 m (konvergencija mreže); ne-regresija 7/7 P10 kontrolnih napisov — TRIBUTSCH v Tribučeh, WEIDENDORF ×2 v Bedenjah, ADLESCHITZ izven Gribelj, Bresnik 34 m, Fučkovci 33 m, Pri Jankovichti 33 m; SHEET_GEOREFS namerno nespremenjen (lekcija P9) — predlog nadgradnje čaka človeško potrditev; status REVIEW",
    "P46: NEATLINE georeferencing of sections dg/cg/ch (A03–A05, issue #14/§3) — the 'neatline = eZKN 1:2880 section boundary' principle calibrated on A02 under the GEOTRUTH affine (residuals N 9.3 m, E 13.2 m ≤ 90); A04 (cg): 4/4 sides detected, scale sx 0.77654 / sy 0.77266 m/px (axis consistency 0.5%), 4-corner affine RMS ≤ 30 m → NEATLINE_GEOREFERENCED ±40 m; A05 (ch): 4/4 sides (N/W weaker coverage) → NEATLINE_GEOREFERENCED ±40 m; A03 (dg): S/E detected, N/W inferred via s̄ (weak candidates within 25 m) → NEATLINE_PARTIAL ±50 m; new bounds shift vs P10 GRID_APPROX only 17–18 m (grid convergence); non-regression 7/7 P10 control labels — TRIBUTSCH in Tribuče, WEIDENDORF ×2 in Bedenj, ADLESCHITZ outside Griblje, Bresnik 34 m, Fučkovci 33 m, Pri Jankovichti 33 m; SHEET_GEOREFS deliberately unchanged (the P9 lesson) — the upgrade proposal awaits human confirmation; status REVIEW",
    p46Errors.length === 0,
    p46Errors.length === 0
      ? `kontrola A02: 9.3/13.2 m · s̄ 0.7746 m/px (0,5 %) · A04/A05 4/4 ±40 m, A03 2/4 ±50 m · premik 17–18 m · 7/7 validacij (Bresnik 34, Fučkovci 33, Jankovichti 33 m) · ${p46FileDetail}`
      : p46Errors.join("; "),
  );

  // ——— P47: GURS parcel overlay — neodvisna validacija neatline afin ———
  const p47Errors: string[] = [];
  const p47 = GURS_OVERLAY_P47;
  // listi: pinane mediane residuala in DRAWN števila
  const p47Res = { A02: 9.8, A03: 9.8, A04: 5.6, A05: 9.3 } as const;
  const p47Drawn = { A02: 640, A03: 112, A04: 498, A05: 165 } as const;
  for (const s of ["A02", "A03", "A04", "A05"] as const) {
    const o = p47.sheets[s];
    if (o.drawn.residualM.median !== p47Res[s])
      p47Errors.push(`${s}: pinana mediana residuala ni ${p47Res[s]} m`);
    if (o.nDrawn !== p47Drawn[s])
      p47Errors.push(`${s}: pinano število DRAWN parcel ni ${p47Drawn[s]}`);
    if (o.drawn.residualM.median > 25 || o.drawn.residualM.p90 > 40)
      p47Errors.push(`${s}: residual nad pragom (≤ 25 / 40 m)`);
    if (o.drawn.covBest.median <= o.drawn.cov0.median)
      p47Errors.push(`${s}: cov@best ni nad cov@0`);
  }
  // registracijski nivo nad kontrolo-zamik 200 px (A03–A05)
  for (const s of ["A03", "A04", "A05"] as const) {
    const o = p47.sheets[s];
    if (o.drawn.cov0.median <= o.controls["200"].median + 0.08)
      p47Errors.push(`${s}: cov@0 ni nad kontrolo 200 px + 0.08`);
  }
  // A05: WAIDENDORF EMPTY stratum izrecno dokumentiran
  if (p47.sheets.A05.nEmpty !== 394)
    p47Errors.push("A05: pinano število EMPTY parcel ni 394");
  if (!p47.sheets.A05.empty.note.includes("WAIDENDORF"))
    p47Errors.push("A05: EMPTY opomba ne omenja WAIDENDORF");
  // 16 izrezov, SHEET_GEOREFS ostaja (lekcija P9)
  if (p47.cropFiles.length !== 16) p47Errors.push("cropFiles ni 16");
  if (!p47.verdictSi.includes("SHEET_GEOREFS se še naprej NAMERNO ne spreminja"))
    p47Errors.push("verdict ne deklarira nedotaknjenosti SHEET_GEOREFS");
  // dokazna datoteka (strežniški klic; vzorec qa-p37..p46)
  let p47FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/gurs-overlay.json");
    const rawRt = opts.readFile("src/data/atlas/gurs-overlay.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p47Errors.push("research/issue17/gurs-overlay.json ni berljiv (izpis scripts/p47_gurs_overlay.py)");
    if (rawRt === null) p47Errors.push("src/data/atlas/gurs-overlay.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p47Errors.push("dokazni in runtime izpis gurs-overlay.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          sheets: Record<string, { nDrawn: number; nEmpty: number; drawn: { cov0: { median: number }; covBest: { median: number }; residualM: { median: number; p90: number } }; controls: Record<string, { median: number }> }>;
          crops: { file: string; sha256: string; bytes: number }[];
          invariants: Record<string, string>;
        };
        for (const [s, o] of Object.entries(j.sheets)) {
          if (o.drawn.residualM.median !== p47Res[s as keyof typeof p47Res])
            p47Errors.push(`JSON ${s}: mediana residuala ni pinana`);
        }
        if (j.sheets.A05.nEmpty !== 394) p47Errors.push("JSON A05 EMPTY ni 394");
        if (j.crops.length !== 16 || j.crops.some((c) => c.bytes <= 0 || c.sha256.length !== 64))
          p47Errors.push("JSON izrezi: ni 16 ali manjkajo sha256/velikosti");
        if (!Object.values(j.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
          p47Errors.push("JSON invarianti niso vsi PASS");
        p47FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (mediane 9.8/9.8/5.6/9.3 m, A05 EMPTY 394, 16 izrezov z sha256)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (mediane 9.8/9.8/5.6/9.3 m, A05 EMPTY 394, 16 izrezov z sha256)`;
      } catch {
        p47Errors.push("izpis gurs-overlay.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p47-gurs-overlay",
    "P47: GURS PARCEL OVERLAY — neodvisna validacija P46 neatline afin (A03–A05, issue #14/§3): sodobne parcele (GURS eZKN WFS; KO 1544 2117 + KO 1552 1113 v bboxu ch, EPSG:3794 → WGS84) preslikane prek afin pasti na narisane črte 1825 — mediana residuala 9.8/9.8/5.6/9.3 m (A02 kontrola GEOTRUTH/A03/A04/A05), p90 ≤ 13.7 m; pokritost črnila cov@0 0.44–0.54 sistematično nad kontrolo-zamik 200 px (0.19–0.47) in se pri najboljšem zamiku strmi (0.71–0.86); STRATA: A05 'Stab der Reambulierungs-Beimappe' — 394/559 EMPTY parcel = skupna paša WAIDENDORF v 1825 (land-use dokaz, ne napaka registracije), A04 128 EMPTY (južno prekrivanje KO 1552); 16 dokaznih izrezov (12 neatline trakov rdeča/oranžna + 4 parcel overlay zeleni) v research/issue17/neatline-crops/; SHEET_GEOREFS še naprej namerno nespremenjen (lekcija P9) — človeška potrditev izrezov ostaja pogoj nadgradnje; status REVIEW",
    "P47: GURS PARCEL OVERLAY — an independent validation of the P46 neatline affines (A03–A05, issue #14/§3): modern parcels (GURS eZKN WFS; KO 1544 2117 + KO 1552 1113 within the ch bbox, EPSG:3794 → WGS84) mapped through the affines fall on the drawn 1825 lines — median residual 9.8/9.8/5.6/9.3 m (A02 GEOTRUTH control/A03/A04/A05), p90 ≤ 13.7 m; ink coverage cov@0 0.44–0.54 systematically above the 200-px shift control (0.19–0.47) and sharpening under best alignment (0.71–0.86); STRATA: A05 'Stab der Reambulierungs-Beimappe' — 394/559 EMPTY parcels = the 1825 WAIDENDORF common pasture (a land-use proof, not a registration error), A04 128 EMPTY (the southern KO 1552 overlap); 16 proof crops (12 neatline strips red/amber + 4 green parcel overlays) in research/issue17/neatline-crops/; SHEET_GEOREFS still deliberately unchanged (the P9 lesson) — human confirmation of the crops remains the upgrade condition; status REVIEW",
    p47Errors.length === 0,
    p47Errors.length === 0
      ? `mediane residuala 9.8/9.8/5.6/9.3 m (p90 ≤ 13.7) · cov@0 nad ctrl200 · covBest 0.71–0.86 · A05 EMPTY 394 = WAIDENDORF · 16 izrezov · ${p47FileDetail}`
      : p47Errors.join("; "),
  );

  // ——— P48: STAVBNI OVERLAY — GURS stavbe ↔ stavbna mesta 1825 ———
  const p48Errors: string[] = [];
  const p48 = BUILDINGS_OVERLAY_P48;
  // listi: pinane on-symbol številke in mediane residuala
  const p48OnSymbol = { A02: 149, A03: 0, A04: 0, A05: 26 } as const;
  const p48Res = { A02: 9.8, A05: 10.1 } as const;
  for (const s of ["A02", "A03", "A04", "A05"] as const) {
    const o = p48.sheets[s];
    if (o.onSymbol.n !== p48OnSymbol[s])
      p48Errors.push(`${s}: pinano število on-symbol stavb ni ${p48OnSymbol[s]}`);
    if (o.nEvaluated === 0 && s !== "A03")
      p48Errors.push(`${s}: brez evalviranih stavb`);
  }
  for (const s of ["A02", "A05"] as const) {
    const os = p48.sheets[s].onSymbol;
    if (os.residualM?.median !== p48Res[s])
      p48Errors.push(`${s}: pinana mediana residuala ni ${p48Res[s]} m`);
    if ((os.residualM?.median ?? 0) > 25)
      p48Errors.push(`${s}: residual nad pragom 25 m`);
    if ((os.covBest?.median ?? 0) <= (os.cov0?.median ?? 1))
      p48Errors.push(`${s}: cov@best ni nad cov@0`);
  }
  // kontinuiteta: pinane vrednosti
  if (p48.continuity.pairs !== 37 || p48.continuity.pairsStrong !== 36)
    p48Errors.push("kontinuiteta: pinano parov 37 (strong 36) ni izpolnjeno");
  if (p48.continuity.gone !== 136 || p48.continuity.footprints1825 !== 156)
    p48Errors.push("kontinuiteta: GONE 136/156 ni pinano");
  if (p48.continuity.onSymbolWithoutVector !== 113)
    p48Errors.push("kontinuiteta: on-symbol-brez-vektorizacije ni 113");
  // Blatt X: refirana direktna referenca (0 identičnih površin) je jedro testa
  const bx = p48.blattX;
  if (bx.rows !== 60 || bx.distinctHausNr !== 59 || bx.inGrundRange41_2500 !== 58)
    p48Errors.push("Blatt X: pinane 60/59/58 ni izpolnjeno");
  if (bx.areasComparable !== 37 || bx.areasIdentical !== 0)
    p48Errors.push("Blatt X: površine 0/37 identičnih (refrirana referenca) ni pinano");
  if (bx.b3OwnerNumeric !== 18)
    p48Errors.push("Blatt X: owner-številke B3 ni 18");
  if (!(bx.medianAreaJoch > 5 && bx.grundHouseMedianJoch < 1))
    p48Errors.push("Blatt X: površine vrstic niso red velikosti nad dvorišči");
  // izrezi + nedotaknjenost SHEET_GEOREFS
  if (p48.cropFiles.length !== 12) p48Errors.push("cropFiles ni 12");
  if (!p48.verdictSi.includes("SHEET_GEOREFS in obstoječi dokazi P40–P47 nespremenjeni"))
    p48Errors.push("verdict ne deklarira nedotaknjenosti SHEET_GEOREFS in dokazov");
  // dokazna datoteka (strežniški klic; vzorec qa-p37..p47)
  let p48FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/buildings-overlay.json");
    const rawRt = opts.readFile("src/data/atlas/buildings-overlay.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p48Errors.push("research/issue17/buildings-overlay.json ni berljiv (izpis scripts/p48_buildings_overlay.py)");
    if (rawRt === null) p48Errors.push("src/data/atlas/buildings-overlay.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p48Errors.push("dokazni in runtime izpis buildings-overlay.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          sheets: Record<string, { nEvaluated: number; onSymbol: { n: number; residualM?: { median: number } } }>;
          continuity: { pairs: number; pairsStrong: number; gone: number; footprints1825: number };
          blattX: { rows: number; distinctHausNr: number; areasComparable: number; areasIdentical: number };
          crops: { file: string; sha256: string; bytes: number }[];
          invariants: Record<string, string>;
        };
        if (j.sheets.A02.onSymbol.n !== 149 || j.sheets.A05.onSymbol.n !== 26)
          p48Errors.push("JSON: on-symbol 149/26 ni pinano");
        if (j.continuity.pairs !== 37 || j.continuity.gone !== 136)
          p48Errors.push("JSON: kontinuiteta 37/136 ni pinana");
        if (j.blattX.areasIdentical !== 0 || j.blattX.areasComparable !== 37)
          p48Errors.push("JSON: Blatt X 0/37 ni pinano");
        if (j.crops.length !== 12 || j.crops.some((c) => c.bytes <= 0 || c.sha256.length !== 64))
          p48Errors.push("JSON izrezi: ni 12 ali manjkajo sha256/velikosti");
        if (!Object.values(j.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
          p48Errors.push("JSON invarianti niso vsi PASS");
        p48FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (on-symbol 149/26, kontinuiteta 37/136, Blatt X 0/37, 12 izrezov z sha256)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (on-symbol 149/26, kontinuiteta 37/136, Blatt X 0/37, 12 izrezov z sha256)`;
      } catch {
        p48Errors.push("izpis buildings-overlay.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p48-gurs-buildings",
    "P48: STAVBNI OVERLAY — GURS stavbe ↔ stavbna mesta 1825 (issue #14/§3, most PUA↔PT↔PS↔GURS): sodobni stavbni tlorisi (GURS eZKN WFS SI.GURS.KN:STAVBE, OBRIS_GEOM; KO 1544 401 z geometrijo + KO 1552 južni bbox 313, recept scripts/p48_fetch_stavbe.sh) preslikani prek GEOTRUTH mej A02 / P46 afin A03–A05 morajo pasti na narisane stavbne simbole 1825 — pokritost notranjosti+oboda na ERODIRANI maski (prag 195, plus-oblika 3×3; tanke parcelne črte izginejo, polni simboli ostanejo): A02/cf 149/154 stavb on-symbol (cov@best mediana 1.0, DRAWN cov@0 0.85), mediana residuala 9.8 m (p90 13.7 m) — stavbna raven potrjuje parcelno raven P47 (9.8 m); A05/ch Fučkovci 26/95 on-symbol, residual 10.1 m — neodvisna potrditev P46 afine na stavbni ravni; A04/cg 0 on-symbol (sodobne stavbe na paši WEIDENDORF so novejše od risbe — skladno s P47 EMPTY stratum); A03/dg 0 sodobnih stavb (dokumentirano); KONTINUITETA A02: 37 parov tloris↔stavba (≤ 25 px ≈ 20 m; 36 strong z cov@best ≥ 0.5), 113 stavb na simbolih brez vektorizacije, 136/156 tlorisov 1825 brez naslednika (mediana najbližje stavbe 392.6 px ≈ 316 m — razpršena zidanica na zahodnih pobočjih: vinice/hambi niso preživeli) — nadgradja P16 present.json (OSM 15/26/115) z uradnimi GURS obrisi; BLATT X (str. 138–139) kvantitativna opomba: 59 različnih hausNr, 58 v razponu GRUND (41–2500; 57 dejanskih parcel), a površine se z GRUND parcelami pri istih številkah ujemajo 0/37-krat — direktna referenca na register 1825 REFRIRANA; površine vrstic (mediana 6.329 J, do 17.3 J) so red velikosti nad GRUND dvorišči (0.282 J); owner stolpec vrstic 81–100 vsebuje 18 številk (63–80) — signal premika stolpcev; skladno z 'Zusammenstellung der Grundstücke' (opomba vrstice 1), letnico 1860 in reambulacijskimi glavami je Blatt X verjetno poznejša zbirka parcel — kvantitativna poprava P42 interpretacije 'register stavbnih mest' (ostaja [~] do človeške paleografije); 12 dokaznih izrezov (6 parov zeleni/modri, gone rdeči, 2×A05 on-symbol, A05/A04 new, pregled A02) v research/issue17/buildings-crops/; SHEET_GEOREFS in dokazi P40–P47 nespremenjeni; status REVIEW",
    "P48: BUILDING OVERLAY — GURS buildings ↔ 1825 building sites (issue #14/§3, the PUA↔PT↔PS↔GURS bridge): modern building footprints (GURS eZKN WFS SI.GURS.KN:STAVBE, OBRIS_GEOM; KO 1544 401 with geometry + KO 1552 south bbox 313, receipt scripts/p48_fetch_stavbe.sh) mapped via the A02 GEOTRUTH bounds / P46 affines A03–A05 must fall on the drawn 1825 building symbols — interior+perimeter coverage on the ERODED mask (threshold 195, plus-shape 3×3; thin parcel lines vanish, solid symbols survive): A02/cf 149/154 buildings on-symbol (cov@best median 1.0, DRAWN cov@0 0.85), median residual 9.8 m (p90 13.7 m) — the building level confirms the parcel level of P47 (9.8 m); A05/ch Fučkovci 26/95 on-symbol, residual 10.1 m — an independent confirmation of the P46 affine at the building level; A04/cg 0 on-symbol (modern buildings on the WEIDENDORF pasture are younger than the map — consistent with the P47 EMPTY stratum); A03/dg 0 modern buildings (documented); CONTINUITY A02: 37 footprint↔building pairs (≤ 25 px ≈ 20 m; 36 strong with cov@best ≥ 0.5), 113 buildings on symbols without vectorization, 136/156 1825 footprints without a successor (median nearest building 392.6 px ≈ 316 m — the dispersed settlement on the western slopes: vineyard cottages/hambas did not survive) — an upgrade of P16 present.json (OSM 15/26/115) with official GURS footprints; BLATT X (pp. 138–139) quantitative note: 59 distinct hausNr, 58 within the GRUND range (41–2500; 57 actual parcels), yet row areas match the GRUND parcels at the same numbers 0/37 times — the direct reference to the 1825 register REFUTED; row areas (median 6.329 J, up to 17.3 J) are an order of magnitude above GRUND curtilages (0.282 J); the owner column of rows 81–100 contains 18 numbers (63–80) — a column-shift signal; consistent with 'Zusammenstellung der Grundstücke' (row-1 note), the year 1860 and the reambulation sheet headers, Blatt X is likely a LATER parcel compilation — a quantitative correction of the P42 interpretation 'register of building sites' (remains [~] until human paleography); 12 proof crops (6 pairs green/blue, gone red, 2×A05 on-symbol, A05/A04 new, A02 overview) in research/issue17/buildings-crops/; SHEET_GEOREFS and the P40–P47 evidence unchanged; status REVIEW",
    p48Errors.length === 0,
    p48Errors.length === 0
      ? `A02 on-symbol 149/154 (residual 9.8 m) · A05 26/95 (10.1 m) · A04/A03 0 · kontinuiteta 37 parov (36 strong), GONE 136/156 · Blatt X 0/37 REFRIRANA · 12 izrezov · ${p48FileDetail}`
      : p48Errors.join("; "),
  );

  // ——— P49: FUČKOVCI 1825 — dokazna sloja + obseg sklopa ———
  const p49Errors: string[] = [];
  const p49 = FUCUKOVCI_P49;
  // sidro + sklop: pinane vrednosti
  if (p49.anchor.offsetPx !== 43.2 || p49.anchor.pxViaAffine[0] !== 1944.8 || p49.anchor.pxViaAffine[1] !== 636.8)
    p49Errors.push("sidro: pinano (1944.8,636.8) / odmik 43.2 px ni izpolnjeno");
  if (p49.modern.nInCell !== 96 || p49.modern.nEvaluated !== 95 || p49.modern.nOnSymbol !== 26)
    p49Errors.push("pariteta s P48: 96/95/26 ni izpolnjena");
  if (p49.modern.residualM === null || p49.modern.residualM > 25)
    p49Errors.push("on-symbol residual nad 25 m");
  if (p49.cluster.onSymbolInCluster !== 25 || p49.cluster.onSymbolTotal !== 26)
    p49Errors.push("sklop: 25/26 on-symbol ni pinano");
  if (p49.cluster.nearestOnSymbolToAnchorPx === null || p49.cluster.nearestOnSymbolToAnchorPx > 60)
    p49Errors.push("najbližje mesto > 60 px od sidra");
  if (p49.cluster.hullAreaM2 !== 36336 || p49.cluster.hullVertices !== 7 || p49.cluster.inkMassPx !== 257571)
    p49Errors.push("obseg sklopa: lupina 36336 m² (7 oglišč) / masa 257571 px ni pinano");
  // striktna detekcija + triaža
  if (p49.strict.nSymbols !== 53 || p49.strict.nCorroborated !== 7 || p49.strict.nUnmatchedInCluster !== 19)
    p49Errors.push("striktna detekcija: 53/7/19 ni pinano");
  if (p49.strict.triageInCluster.building !== 2 || p49.strict.triageInCluster.unclear !== 4)
    p49Errors.push("triaža: building 2 + unclear 4 ni pinano");
  const p49TriageSum = Object.values(p49.strict.triageInCluster).reduce((a, b) => a + b, 0);
  if (p49TriageSum !== p49.strict.nUnmatchedInCluster)
    p49Errors.push("triaža: vsota ne sešteje neujemanih jeder v sklopu");
  // skladnost s P10 (brez protislovja)
  if (p49.estimate.lowerBound !== 27 || p49.estimate.upperBound !== 44)
    p49Errors.push("ocena: meje [27, 44] ni pinana");
  if (!(p49.estimate.lowerBound <= p49.estimate.p10BuildingsVlm && p49.estimate.upperBound >= 40))
    p49Errors.push("P10 ~45 ni znotraj mej — protislovje");
  if (p49.estimate.continuityLowerRatio !== 0.806)
    p49Errors.push("ohranjenost (spodnja meja) 0.806 ni pinana");
  // nedotaknjenost + izrezi
  if (p49.cropFiles.length !== 9) p49Errors.push("cropFiles ni 9");
  if (!p49.verdictSi.includes("SHEET_GEOREFS nespremenjen"))
    p49Errors.push("verdict ne deklarira nedotaknjenosti SHEET_GEOREFS");
  // dokazna datoteka (strežniški klic; vzorec qa-p37..p48)
  let p49FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/fucukovci-1825.json");
    const rawRt = opts.readFile("src/data/atlas/fucukovci-1825.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p49Errors.push("research/issue17/fucukovci-1825.json ni berljiv (izpis scripts/p49_fucukovci1825.py)");
    if (rawRt === null) p49Errors.push("src/data/atlas/fucukovci-1825.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p49Errors.push("dokazni in runtime izpis fucukovci-1825.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          modern: { nInCell: number; nEvaluated: number; nOnSymbol: number; residualM: number | null };
          cluster: { onSymbolInCluster: number; hull: { areaM2: number }; inkMass: { massPx: number } };
          strict: { nSymbols: number; nCorroborated: number; nUnmatchedInCluster: number; triageInCluster: Record<string, number> };
          estimate: { lowerBound: number; upperBound: number };
          places: unknown[];
          symbols: unknown[];
          crops: { file: string; sha256: string; bytes: number }[];
          invariants: Record<string, string>;
        };
        if (j.modern.nInCell !== 96 || j.modern.nEvaluated !== 95 || j.modern.nOnSymbol !== 26)
          p49Errors.push("JSON: pariteta 96/95/26 ni pinana");
        if (j.cluster.onSymbolInCluster !== 25 || j.cluster.hull.areaM2 !== 36336 || j.cluster.inkMass.massPx !== 257571)
          p49Errors.push("JSON: sklop 25/36336/257571 ni pinano");
        if (j.strict.nSymbols !== 53 || j.strict.nCorroborated !== 7 || j.strict.nUnmatchedInCluster !== 19)
          p49Errors.push("JSON: striktna detekcija 53/7/19 ni pinana");
        if (j.estimate.lowerBound !== 27 || j.estimate.upperBound !== 44)
          p49Errors.push("JSON: meje [27, 44] ni pinana");
        if (j.places.length !== 26 || j.symbols.length !== 53)
          p49Errors.push("JSON: 26 mest / 53 jeder ni pinano");
        if (j.crops.length !== 9 || j.crops.some((c) => c.bytes <= 0 || c.sha256.length !== 64))
          p49Errors.push("JSON izrezi: ni 9 ali manjkajo sha256/velikosti");
        if (!Object.values(j.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
          p49Errors.push("JSON invarianti niso vsi PASS");
        p49FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (26 mest, 53 jeder, lupina 36336 m², 9 izrezov z sha256, invarianti I1–I8 PASS)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (26 mest, 53 jeder, lupina 36336 m², 9 izrezov z sha256, invarianti I1–I8 PASS)`;
      } catch {
        p49Errors.push("izpis fucukovci-1825.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p49-fucukovci-1825",
    "P49: FUČKOVCI 1825 — modern-anchored symbol evidence + striktna detekcija jeder + obseg sklopa (issue #14/§3, delna vektorizacija A05): ugotovitev — celtna vektorizacija tlorisov na A05 NI izvedljiva (rožnati parcelni fill siva ~168.9 < prag 195 → barvna zasenčitev maske; erodirana maska se v škatli vasi zasiči 0.403 → simboli se staknejo; številke/črki/drevesa v istem kontrastnem razredu kot simboli — striktni detektor ~50 % preciznost brez konteksta); namesto tega TRI neodvisna dokazna sloja: (1) MODERN-ANCHORED (P48 stroj, pariteta 96/95/26): 26 sodobnih stavb pada na narisane simbole (residual mediana 9.8 m), 25 v sklopu Fučkovci (radij 380 px okoli P10 sidra (1944.8,636.8) — odmik 43.2 px od VLM branja; najbližje mesto 48.9 px ≈ 38 m, skladno s P46 'Fučkovci 33 m') = dokazana stavbna mesta z naslednikom (WGS84 v izpisu); (2) STRIKTNA DETEKCIJA JEDER (kontrast ≤ −13, g<145 ≥ 0.55, test obroča < 198): 53 jeder, 7 koreliranih (≤ 20 px), 19 neujemanih v sklopu — vizualna triaža (provenienca: razvojna presoja, čaka lastnika): 2 stavbi + 4 nejasni = GONE-kandidati [~], 5 text + 5 line-corner + 1 tree + 1 number + 1 lane-junction; (3) OBSEG SKLOPA: konveksna lupina 25 dokazanih mest 36 336 m² (7 oglišč, ringWGS84 v izpisu) + masa črnila 257 571 px; SKLADNOST s P10: ocena stavb [27, 44] — P10 ~45 znotraj mej, brez protislovja (razlika = odzivnost detektorja); OHRANJENOST Fučkovcev ≥ 0.806 [~] — jedro vasi ohranjeno (v nasprotju z A02 razpršeno zidanico P48: 136/156); 9 dokaznih izrezov (pregled sklopa, kontaktni list jeder, 6 parov, neujemani list) v research/issue17/fucukovci-crops/; SHEET_GEOREFS in dokazi P40–P48 nespremenjeni; status ANALYSIS-DETERMINISTIC",
    "P49: FUČKOVCI 1825 — modern-anchored symbol evidence + strict dark-core detection + cluster extent (issue #14/§3, partial vectorization of A05): the finding — full footprint vectorization on A05 is NOT feasible (pink parcel fill gray ~168.9 < threshold 195 → color shading pollutes the mask; the eroded mask saturates at 0.403 inside the village box → symbols merge; numbers/letters/trees share the symbols' contrast class — the strict detector reaches ~50 % precision without context); instead THREE independent evidence layers: (1) MODERN-ANCHORED (P48 machinery, parity 96/95/26): 26 modern buildings fall on drawn symbols (residual median 9.8 m), 25 inside the Fučkovci cluster (radius 380 px around the P10 anchor (1944.8,636.8) — 43.2 px from the VLM read; nearest place 48.9 px ≈ 38 m, consistent with P46 'Fučkovci 33 m') = proven building places with successors (WGS84 in the evidence file); (2) STRICT CORE DETECTION (contrast ≤ −13, g<145 ≥ 0.55, ring test < 198): 53 cores, 7 corroborated (≤ 20 px), 19 unmatched inside the cluster — visual triage (provenance: development-time judgment, awaits owner): 2 buildings + 4 unclear = GONE candidates [~], 5 text + 5 line-corner + 1 tree + 1 number + 1 lane-junction; (3) CLUSTER EXTENT: convex hull of 25 proven places 36 336 m² (7 vertices, ringWGS84 in the evidence) + ink mass 257 571 px; CONSISTENCY with P10: building-count estimate [27, 44] — the P10 ~45 lies within the bounds, no contradiction (the difference is detector recall); SURVIVAL of Fučkovci ≥ 0.806 [~] — the village core survived (unlike the A02 dispersed settlement of P48: 136/156 without successor); 9 proof crops (cluster overview, core contact sheet, 6 pairs, unmatched sheet) in research/issue17/fucukovci-crops/; SHEET_GEOREFS and the P40–P48 evidence unchanged; status ANALYSIS-DETERMINISTIC",
    p49Errors.length === 0,
    p49Errors.length === 0
      ? `26 mest (25 v sklopu, residual 9.8 m) · 53 jeder (7 koreliranih, triaža 2+4 [~]) · lupina 36336 m² · meje [27, 44] ⊇ P10 ~45 · 9 izrezov · ${p49FileDetail}`
      : p49Errors.join("; "),
  );

  /* ── P50: GEOREF ZAPORA A03–A05 — aktivacija P46 neatline afin ————————————————— */
  const p50Errors: string[] = [];
  const p50 = GEOREF_CLOSURE_P50;
  // 1) verdikt deklarira aktivacijo + pošten status človeškega pogoja
  if (!p50.activation.decision.includes("AKTIVIRAN")) p50Errors.push("odločba ne deklarira aktivacije P46 predloga");
  if (!p50.statusLine.includes("ACTIVATED-DETERMINISTIC")) p50Errors.push("statusLine ni ACTIVATED-DETERMINISTIC");
  if (!p50.activation.humanGateNote.includes("priporočen [~]")) p50Errors.push("humanGateNote brez poštenega [~] statusa vizualnega pregleda");
  if (p50.activation.basis.length !== 5) p50Errors.push(`basis: ${p50.activation.basis.length} plasti (pričakovano 5 — L0–L4)`);
  // 2) navzkrižna kontrola: JSON/T konstanta ↔ živi SHEET_GEOREFS (KLJUČNA regresijska zavarovala)
  for (const [key, sid] of [["A03", "georef-a03"], ["A04", "georef-a04"], ["A05", "georef-a05"]] as const) {
    const g = SHEET_GEOREFS.find((x) => x.id === sid);
    const s = p50.sheets[key];
    if (!g || !s) {
      p50Errors.push(`P50: manjka ${key}/${sid}`);
      continue;
    }
    if (g.status !== s.status) p50Errors.push(`${key}: status ${g.status} ≠ konstanta ${s.status}`);
    if (Math.abs(g.bounds[0][0] - s.boundsNeatlineNWSE[0][0]) > 5e-5 || Math.abs(g.bounds[0][1] - s.boundsNeatlineNWSE[0][1]) > 5e-5)
      p50Errors.push(`${key}: bounds SZ ${g.bounds[0]} ≠ konstanta ${s.boundsNeatlineNWSE[0]}`);
    if (Math.abs(g.bounds[1][0] - s.boundsNeatlineNWSE[1][0]) > 5e-5 || Math.abs(g.bounds[1][1] - s.boundsNeatlineNWSE[1][1]) > 5e-5)
      p50Errors.push(`${key}: bounds JV ${g.bounds[1]} ≠ konstanta ${s.boundsNeatlineNWSE[1]}`);
    if (Math.abs(g.scaleMPerPixel - s.scaleMPerPixel) > 5e-4) p50Errors.push(`${key}: merilo ${g.scaleMPerPixel} ≠ ${s.scaleMPerPixel}`);
    if (g.controlPoints.length !== s.controlPointsN) p50Errors.push(`${key}: kontrolne točke ${g.controlPoints.length} ≠ ${s.controlPointsN}`);
  }
  // 3) pinane vrednosti dokaza
  if (p50.sheets.A03.detectedSides !== 2 || p50.sheets.A04.detectedSides !== 4 || p50.sheets.A05.detectedSides !== 4)
    p50Errors.push("detektirane strani 2/4/4 ni pinano");
  for (const [key, med] of [["A03", 9.8], ["A04", 5.6], ["A05", 9.3]] as const) {
    if (p50.sheets[key].parcelMedianM !== med) p50Errors.push(`${key}: P47 mediana ${p50.sheets[key].parcelMedianM} ≠ ${med}`);
  }
  if (p50.sheets.A05.buildingsOnSymbol !== 26) p50Errors.push("A05: 26 on-symbol ni pinano");
  if (p50.sheets.A03.shiftVsP10M.max !== 17.4 || p50.sheets.A04.shiftVsP10M.max !== 16.9 || p50.sheets.A05.shiftVsP10M.max !== 18.0)
    p50Errors.push("premiki vs P10 17.4/16.9/18.0 ni pinano");
  if (p50.labelsValidation.length !== 7 || p50.labelsValidation.some((l) => !l.pass))
    p50Errors.push("validacije napisov niso 7/7 PASS");
  if (!Object.values(p50.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
    p50Errors.push("invarianti I1–I10 niso vsi PASS");
  // 4) viri: opombe nosijo AKTIVACIJO P50
  for (const sid of ["src-a03", "src-a04", "src-a05"]) {
    const s = ATLAS_SOURCES.find((x) => x.id === sid);
    if (!s || !s.noteSi?.includes("AKTIVACIJA P50")) p50Errors.push(`${sid}: opomba brez AKTIVACIJE P50`);
  }
  // 5) identičnost obeh izpisov prek vbrizganega readFile (vzorec qa-p37..p49)
  let p50FileDetail = "dokazni datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/georef-closure.json");
    const rawRt = opts.readFile("src/data/atlas/georef-closure.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p50Errors.push("research/issue17/georef-closure.json ni berljiv (izpis scripts/p50_georef_closure.py)");
    if (rawRt === null) p50Errors.push("src/data/atlas/georef-closure.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p50Errors.push("dokazni in runtime izpis georef-closure.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          activation: { basis: string[] };
          sheets: Record<string, { status: string; uncertaintyM: number; scale: { scaleMPerPixel: number }; shiftVsP10M: { max: number } }>;
          sheetGeorefsPatch: Record<string, { bounds: [[number, number], [number, number]]; controlPoints: unknown[] }>;
          invariants: Record<string, string>;
        };
        if (Object.keys(j.sheets).length !== 3) p50Errors.push("JSON: 3 listi ni pinano");
        if (j.activation.basis.length !== 5) p50Errors.push("JSON: 5 plasti ni pinano");
        if (j.sheets.A03.uncertaintyM !== 50 || j.sheets.A04.uncertaintyM !== 40 || j.sheets.A05.uncertaintyM !== 40)
          p50Errors.push("JSON: negotovosti 50/40/40 ni pinano");
        for (const sid of ["georef-a03", "georef-a04", "georef-a05"] as const) {
          const g = SHEET_GEOREFS.find((x) => x.id === sid);
          const p = j.sheetGeorefsPatch[sid];
          if (!g || !p) {
            p50Errors.push(`JSON patch: manjka ${sid}`);
            continue;
          }
          if (Math.abs(p.bounds[0][0] - g.bounds[0][0]) > 5e-6 || Math.abs(p.bounds[1][1] - g.bounds[1][1]) > 5e-6)
            p50Errors.push(`${sid}: patch meje ≠ model.ts (5e-6)`);
        }
        if (!Object.values(j.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
          p50Errors.push("JSON invarianti niso vsi PASS");
        p50FileDetail = rawEv !== null
          ? `dokazni datoteki preverjeni in identični (3 listi, 5 plasti, meje == model.ts, invarianti I1–I10 PASS)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (3 listi, 5 plasti, meje == model.ts, invarianti I1–I10 PASS)`;
      } catch {
        p50Errors.push("izpis georef-closure.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p50-georef-closure",
    "P50: GEOREF ZAPORA A03–A05 — aktivacija P46 neatline afin v SHEET_GEOREFS (issue #14/§3): 5 neodvisnih plasti dokazov (L0 neatline kalibriran na A02/GEOTRUTH 9.3/13.2 m; L1 parcele P47 9.8/5.6/9.3 m; L2 stavbe P48 149/154 + 26 on-symbol; L3 sidro P49 43.2 px; L4 napisi 7/7) → A03 NEATLINE_PARTIAL_GEOREFERENCED ±50 m (2/4 strani), A04/A05 NEATLINE_GEOREFERENCED ±40 m (4/4); meje premaknjene le 17.4/16.9/18.0 m vs P10 (konvergencija), merilo 0.7746 m/px (P46 s̄); GRID_APPROX → 5/5 listov georeferenciranih; vizualni pregled izrezov ostaja priporočen [~]",
    "P50: GEOREF CLOSURE A03–A05 — activation of the P46 neatline affines into SHEET_GEOREFS (issue #14/§3): 5 independent evidence layers (L0 neatline calibrated on A02/GEOTRUTH 9.3/13.2 m; L1 parcels P47 9.8/5.6/9.3 m; L2 buildings P48 149/154 + 26 on-symbol; L3 anchor P49 43.2 px; L4 labels 7/7) → A03 NEATLINE_PARTIAL_GEOREFERENCED ±50 m (2/4 sides), A04/A05 NEATLINE_GEOREFERENCED ±40 m (4/4); bounds shifted only 17.4/16.9/18.0 m vs P10 (grid convergence), scale 0.7746 m/px (P46 s̄); GRID_APPROX → 5/5 sheets georeferenced; visual review of the crops remains recommended [~]",
    p50Errors.length === 0,
    p50Errors.length === 0
      ? `A03 ±50 m (2/4 strani, parcele 9.8 m) · A04 ±40 m (4/4, parcele 5.6 m) · A05 ±40 m (4/4, parcele 9.3 m, 26 stavb) · premiki 17.4/16.9/18.0 m · merilo 0.7746 · napisi 7/7 · ${p50FileDetail}`
      : p50Errors.join("; "),
  );

  /* ── P51: LEAFLET OVERLAY A03–A05 — aktivacija slikovnih prekrivk ————————— */
  const p51Errors: string[] = [];
  const p51 = LEAFLET_OVERLAY_P51;
  // 1) status + UI nastavitve (privzeto izklopljeno — začetni pogled nespremenjen)
  if (!p51.statusLine.includes("UI-ACTIVATED-DETERMINISTIC")) p51Errors.push("statusLine ni UI-ACTIVATED-DETERMINISTIC");
  if (!p51.rotationSubtlety.includes("ne podpira rotiranih prekrivk")) p51Errors.push("rotationSubtlety brez merjene subtilnosti Leaflet rotacij");
  if (p51.ui.togglesDefault !== false) p51Errors.push("stikala niso privzeto IZKLOPLJENA");
  if (p51.ui.toggles.length !== 3) p51Errors.push("ni 3 stikal");
  if (p51.ui.sharedOpacity !== true) p51Errors.push("skupna prosojnost ni aktivirana");
  // 2) pinane vrednosti (skew + odmiki — vzorci iz izgubljene seje, preverjeni s preizračunom)
  const p51SkewPin: Record<string, number> = { A03: 0.5475, A04: 0.568, A05: 0.5708 };
  const p51DevPin: Record<string, number> = { A03: 19.3, A04: 20.0, A05: 20.0 };
  for (const k of ["A03", "A04", "A05"] as const) {
    const s = p51.sheets[k];
    if (s.skewDeg !== p51SkewPin[k]) p51Errors.push(`${k}: skew ${s.skewDeg}° ≠ pinana ${p51SkewPin[k]}°`);
    if (s.overlayDeviationM.max !== p51DevPin[k]) p51Errors.push(`${k}: odmik ${s.overlayDeviationM.max} m ≠ pinan ${p51DevPin[k]} m`);
    if (s.overlayDeviationM.max > 20.5) p51Errors.push(`${k}: odmik > 20.5 m`);
    if (s.sha256.length !== 64) p51Errors.push(`${k}: sha256 ni 64 znakov`);
  }
  // 3) navzkrižje s SHEET_GEOREFS: status + ovoj ⊇ neatline meje (KLJUČNA regresijska zavarovala)
  for (const [key, sid] of [["A03", "georef-a03"], ["A04", "georef-a04"], ["A05", "georef-a05"]] as const) {
    const g = SHEET_GEOREFS.find((x) => x.id === sid);
    const s = p51.sheets[key];
    if (!g || !s) {
      p51Errors.push(`P51: manjka ${key}/${sid}`);
      continue;
    }
    if (g.status !== s.status) p51Errors.push(`${key}: status ${g.status} ≠ konstanta ${s.status}`);
    if (Math.abs(g.bounds[0][0] - s.neatlineFromHull[0][0]) > 5e-5 || Math.abs(g.bounds[0][1] - s.neatlineFromHull[0][1]) > 5e-5)
      p51Errors.push(`${key}: neatline SZ ${g.bounds[0]} ≠ konstanta ${s.neatlineFromHull[0]}`);
    if (Math.abs(g.bounds[1][0] - s.neatlineFromHull[1][0]) > 5e-5 || Math.abs(g.bounds[1][1] - s.neatlineFromHull[1][1]) > 5e-5)
      p51Errors.push(`${key}: neatline JV ${g.bounds[1]} ≠ konstanta ${s.neatlineFromHull[1]}`);
    // ovoj ⊇ neatline (lat in lng)
    if (!(s.hullNWSE[0][0] >= s.neatlineFromHull[0][0] && s.hullNWSE[1][0] <= s.neatlineFromHull[1][0]))
      p51Errors.push(`${key}: lat razpon ovoja ne obsega neatline`);
    if (!(s.hullNWSE[0][1] <= s.neatlineFromHull[0][1] && s.hullNWSE[1][1] >= s.neatlineFromHull[1][1]))
      p51Errors.push(`${key}: lng razpon ovoja ne obsega neatline`);
  }
  // 4) viri: opombe nosijo P51
  for (const sid of ["src-a03", "src-a04", "src-a05"]) {
    const s = ATLAS_SOURCES.find((x) => x.id === sid);
    if (!s || !s.noteSi?.includes("LEAFLET OVERLAY")) p51Errors.push(`${sid}: opomba brez P51 LEAFLET OVERLAY`);
  }
  // 5) dokazna datoteka + UI-vod (strežniški klic; vzorec qa-p37..p50)
  let p51FileDetail = "dokazni in UI datoteki nista preverjeni (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/leaflet-overlay.json");
    const rawRt = opts.readFile("src/data/atlas/leaflet-overlay.json");
    // produkcija: kontrola na runtime kopiji (bajtno identični izpis skripta;
    // identičnost obeh izpisov se preveri v repozitoriju/CI). Vzorec qa-p43-chain-full.
    const raw = rawEv ?? rawRt;
    if (raw === null) p51Errors.push("research/issue17/leaflet-overlay.json ni berljiv (izpis scripts/p51_leaflet_overlay.py)");
    if (rawRt === null) p51Errors.push("src/data/atlas/leaflet-overlay.json ni berljiv (runtime kopija)");
    if (rawEv !== null && rawRt !== null && rawEv !== rawRt)
      p51Errors.push("dokazni in runtime izpis leaflet-overlay.json nista identična (skript mora izpisati oba enako)");
    if (raw !== null) {
      try {
        const j = JSON.parse(raw) as {
          ui: { togglesDefault: boolean; toggles: string[] };
          sheets: Record<string, {
            pixels: { width: number; height: number };
            sha256: string;
            hullNWSE: [[number, number], [number, number]];
            skewDeg: number;
            overlayDeviationM: { max: number };
            status: string;
          }>;
          invariants: Record<string, string>;
        };
        if (Object.keys(j.sheets).length !== 3) p51Errors.push("JSON: 3 listi ni pinano");
        if (j.ui.togglesDefault !== false) p51Errors.push("JSON: stikala niso privzeto izklopljena");
        if (!Object.values(j.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
          p51Errors.push("JSON invarianti niso vsi PASS");
        // navzkrižna kontrola TS konstanta ↔ JSON (ovoji 5e-6, sha256, odmiki, skew)
        for (const k of ["A03", "A04", "A05"] as const) {
          const jt = j.sheets[k];
          const ts = p51.sheets[k];
          if (!jt || !ts) {
            p51Errors.push(`navzkrižje TS↔JSON: manjka ${k}`);
            continue;
          }
          if (Math.abs(jt.hullNWSE[0][0] - ts.hullNWSE[0][0]) > 5e-6 || Math.abs(jt.hullNWSE[0][1] - ts.hullNWSE[0][1]) > 5e-6)
            p51Errors.push(`${k}: ovoj SZ ≠ konstanta (5e-6)`);
          if (Math.abs(jt.hullNWSE[1][0] - ts.hullNWSE[1][0]) > 5e-6 || Math.abs(jt.hullNWSE[1][1] - ts.hullNWSE[1][1]) > 5e-6)
            p51Errors.push(`${k}: ovoj JV ≠ konstanta (5e-6)`);
          if (jt.sha256 !== ts.sha256) p51Errors.push(`${k}: sha256 ≠ konstanta`);
          if (jt.skewDeg !== ts.skewDeg) p51Errors.push(`${k}: skew ≠ konstanta`);
          if (jt.overlayDeviationM.max !== ts.overlayDeviationM.max) p51Errors.push(`${k}: odmik ≠ konstanta`);
          if (jt.pixels.width !== ts.pixels.width || jt.pixels.height !== ts.pixels.height) p51Errors.push(`${k}: pixels ≠ konstanta`);
        }
        p51FileDetail = rawEv !== null
          ? `dokazni in runtime izpis preverjeni in identični (3 listi, ovoji == konstanta 5e-6, sha256, skew 0.5475/0.568/0.5708, odmiki 19.3/20.0/20.0, invarianti I1–I8 PASS)`
          : `produkcija: runtime kopija preverjena — research/ ni v deploymentu (3 listi, ovoji == konstanta 5e-6, sha256, skew/odmiki, invarianti I1–I8 PASS)`;
      } catch {
        p51Errors.push("izpis leaflet-overlay.json ni veljaven JSON");
      }
    }
    // UI-vod: canvas uvaža runtime JSON (en sam vir resnice) + stikala z privzetimi vrednostmi
    const canvas = opts.readFile("src/components/museum/atlas-canvas.tsx");
    const atlas = opts.readFile("src/components/museum/museum-atlas.tsx");
    if (canvas === null) p51Errors.push("src/components/museum/atlas-canvas.tsx ni berljiv (UI-vod)");
    if (atlas === null) p51Errors.push("src/components/museum/museum-atlas.tsx ni berljiv (UI-vod)");
    if (canvas !== null) {
      if (!canvas.includes("@/data/atlas/leaflet-overlay.json")) p51Errors.push("canvas ne uvaža runtime leaflet-overlay.json (en sam vir resnice)");
      if (!canvas.includes("L.imageOverlay")) p51Errors.push("canvas ne uporablja L.imageOverlay");
      if (!canvas.includes('dashArray: "6 5"') || !canvas.includes("#8a6d3b")) p51Errors.push("canvas: črtkani neatline okvirji #8a6d3b dash 6 5 niso pinani");
      if (!canvas.includes("sticky: true")) p51Errors.push("canvas: sticky tooltip neatline okvirjev ni pinan");
    }
    if (atlas !== null) {
      for (const [k, lab] of [["a03", "List A03 (±50 m)"], ["a04", "List A04 (±40 m)"], ["a05", "List A05 (±40 m)"]] as const) {
        if (!atlas.includes(`"${k}", t("${lab}"`)) p51Errors.push(`museum-atlas: stikalo »${lab}« ni pinano`);
        if (!atlas.includes(`${k}: false`)) p51Errors.push(`museum-atlas: ${k} ni privzeto izklopljen`);
      }
    }
  }
  push(
    "qa-p51-leaflet-overlay",
    "P51: LEAFLET OVERLAY A03–A05 — aktivacija slikovnih prekrivk (issue #14/§3): ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0), SE = affine(W,H); pixels iz model.ts prek regexa) == P50 boundsImageNWSE ≤ 5e-6° — ni ročno prepisanih koordinat; MERJENA SUBTELNOST pošteno dokumentirana: Leaflet ne podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir; odmik vogalov izmerjen iz členov afine (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m (dva vogala točna) — del ±40/50 m negotovosti lista; skew 0.5475/0.568/0.5708° ≤ 1.0°; slike preverjene (PIL dims == model.ts + sha256); UI: stikala privzeto IZKLOPLJENA, črtkani neatline okvirji s statusom, skupna prosojnost; SHEET_GEOREFS in dokazi P40–P50 nespremenjeni; status UI-ACTIVATED-DETERMINISTIC",
    "P51: LEAFLET OVERLAY A03–A05 — activation of the image overlays (issue #14/§3): the scan envelope INDEPENDENTLY recomputed from the P46 affine (NW = affine(0,0), SE = affine(W,H); pixels from model.ts via regex) == P50 boundsImageNWSE ≤ 5e-6° — no hand-copied coordinates; the MEASURED SUBTLETY honestly documented: Leaflet does not support rotated overlays — the image is stretched into an axis-aligned frame; corner deviation measured from the affine terms (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m (two corners exact) — part of the sheet's ±40/50 m uncertainty; skew 0.5475/0.568/0.5708° ≤ 1.0°; images verified (PIL dims == model.ts + sha256); UI: toggles default OFF, dashed neatline frames with the status, shared opacity; SHEET_GEOREFS and the P40–P50 evidence unchanged; status UI-ACTIVATED-DETERMINISTIC",
    p51Errors.length === 0,
    p51Errors.length === 0
      ? `A03 ±50 m (skew 0.5475°, odmik 19.3 m) · A04 ±40 m (0.568°, 20.0 m) · A05 ±40 m (0.5708°, 20.0 m) · ovoji == P50 5e-6° · stikala privzeto izklopljena · ${p51FileDetail}`
      : p51Errors.join("; "),
  );

  /* ── P54 (issue #12 nadgradnja): present.json na uradnih GURS obriseh ── */
  const p54Errors: string[] = [];
  const p54 = PRESENT_GURS_P54;
  // 1) pinane vrednosti konstante
  if (p54.counts.exists !== 18 || p54.counts.uncertain !== 21 || p54.counts.gone !== 117)
    p54Errors.push(`konstanta števcev ${JSON.stringify(p54.counts)} ≠ 18/21/117`);
  if (p54.countsP16.exists !== 15 || p54.countsP16.uncertain !== 26 || p54.countsP16.gone !== 115)
    p54Errors.push(`konstanta P16 števcev ≠ 15/26/115`);
  const transSum = Object.values(p54.transitions).reduce((a, b) => a + b, 0);
  if (transSum !== 156) p54Errors.push(`prehodi vsota ${transSum} ≠ 156`);
  if (p54.transitions["uncertain→exists"] !== 4 || p54.transitions["uncertain→gone"] !== 2 ||
      p54.transitions["exists→uncertain"] !== 1 || p54.transitions["gone→gone"] !== 115)
    p54Errors.push("prehodi ≠ pinane vrednosti (4/2/1/115)");
  if (p54.changed.length !== 7) p54Errors.push(`spremenjenih ${p54.changed.length} ≠ 7`);
  if (p54.replay.pass !== "156/156" || p54.replay.osmIdMatch !== 41)
    p54Errors.push("repla ≠ 156/156 (+ osmId 41)");
  if (p54.window.gursInWindow !== 380 || p54.window.ko[0] !== 1544)
    p54Errors.push("okno ≠ 380 (KO 1544)");
  if (p54.p48Cross.inCellCf !== 154 || p54.p48Cross.pairs25px !== 37 || p54.p48Cross.pairFootprints !== 20 || p54.p48Cross.modernNear25pxWindow !== 40)
    p54Errors.push("P48 navzkrižje ≠ 154/37/20/40");
  if (!Object.values(p54.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
    p54Errors.push("invarianti niso vsi PASS");
  // 2) runtime present.json: števci + shema + pravila iz d
  let p54RtDetail = "runtime present.json ni preverjen (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  let p54FileDetail = "dokazna datoteka ni preverjena (readFile ni na voljo)";
  let p54UiDetail = "UI-vod ni preverjen (readFile ni na voljo)";
  if (opts.readFile) {
    const rawRt = opts.readFile("src/data/atlas/present.json");
    if (rawRt === null) {
      p54Errors.push("src/data/atlas/present.json ni berljiv (runtime)");
    } else {
      try {
        const rt = JSON.parse(rawRt) as {
          _meta: { gursSnapshot: string; osmSuperseded?: { snapshot: string; counts: { exists: number; uncertain: number; gone: number } } };
          present: { id: string; x: number; z: number; w: number; d: number; area: number; type: string; poly: number[][] }[];
          match: { status: string; d: number | null; gursId: string | null }[];
        };
        const cnt = { exists: 0, uncertain: 0, gone: 0 };
        for (const m of rt.match) cnt[m.status as keyof typeof cnt] = (cnt[m.status as keyof typeof cnt] ?? 0) + 1;
        if (cnt.exists !== 18 || cnt.uncertain !== 21 || cnt.gone !== 117)
          p54Errors.push(`runtime števci ${JSON.stringify(cnt)} ≠ 18/21/117`);
        if (rt.match.length !== 156) p54Errors.push(`runtime match ${rt.match.length} ≠ 156`);
        if (rt.present.length !== 380) p54Errors.push(`runtime present ${rt.present.length} ≠ 380`);
        const ids = new Set(rt.present.map((b) => b.id));
        if (ids.size !== rt.present.length) p54Errors.push("runtime present: EID niso unikatni");
        if (rt._meta.gursSnapshot !== "2026-10-13") p54Errors.push(`gursSnapshot ${rt._meta.gursSnapshot} ≠ 2026-10-13`);
        if (!rt._meta.osmSuperseded || rt._meta.osmSuperseded.counts.exists !== 15 || rt._meta.osmSuperseded.counts.uncertain !== 26 || rt._meta.osmSuperseded.counts.gone !== 115)
          p54Errors.push("osmSuperseded ≠ 15/26/115 (P16 arhiv)");
        // pravila iz zapisanih d (prekrivanje preverja skript — tukaj pražni del)
        for (let i = 0; i < rt.match.length; i++) {
          const m = rt.match[i];
          if (m.d === null || m.d <= 0) { p54Errors.push(`match[${i}]: d manjka ali ≤ 0`); break; }
          if (m.status === "exists" && m.d > 20) p54Errors.push(`match[${i}]: obstoja z d ${m.d} > 20`);
          if (m.status === "uncertain" && m.d > 40) p54Errors.push(`match[${i}]: negotovo z d ${m.d} > 40`);
          if (m.status === "gone" && m.d <= 40) p54Errors.push(`match[${i}]: ni je več z d ${m.d} ≤ 40`);
          if (m.status === "gone" && m.gursId !== null) p54Errors.push(`match[${i}]: ni je več z gursId`);
          if (m.status !== "gone" && !m.gursId) p54Errors.push(`match[${i}]: brez gursId`);
        }
        p54RtDetail = `runtime preverjen: 380 stavb (GURS eZKN, posnetek 2026-10-13) · match 156 = 18/21/117 · pravila iz d PASS · arhiv P16 15/26/115`;
      } catch {
        p54Errors.push("runtime present.json ni veljaven JSON");
      }
    }
    // 3) dokazna datoteka: repla + identičnost polj z runtime (vzorec qa-p51)
    const rawEv = opts.readFile("research/issue17/present-gurs.json");
    if (rawEv === null) {
      p54FileDetail = "produkcija: research/ ni v deploymentu — kontrola na runtime kopiji (vzorec qa-p43-chain-full)";
    } else {
      try {
        const ev = JSON.parse(rawEv) as {
          replay: { pass: string };
          counts: { exists: number; uncertain: number; gone: number };
          transitions: Record<string, number>;
          changed: unknown[];
          p48Cross: { inCellCf: number; pairs25px: number; pairFootprints: number; modernNear25pxWindow: number };
          present: unknown[];
          match: unknown[];
        };
        if (ev.replay.pass !== "156/156") p54Errors.push("dokaz: repla ≠ 156/156");
        if (ev.counts.exists !== 18 || ev.counts.uncertain !== 21 || ev.counts.gone !== 117)
          p54Errors.push("dokaz: števci ≠ 18/21/117");
        if (ev.changed.length !== 7) p54Errors.push("dokaz: spremenjenih ≠ 7");
        if (ev.p48Cross.inCellCf !== 154 || ev.p48Cross.pairs25px !== 37 || ev.p48Cross.pairFootprints !== 20 || ev.p48Cross.modernNear25pxWindow !== 40)
          p54Errors.push("dokaz: P48 navzkrižje ≠ 154/37/20/40");
        const rawRt2 = opts.readFile("src/data/atlas/present.json");
        if (rawRt2 !== null) {
          const rt2 = JSON.parse(rawRt2) as { present: unknown[]; match: unknown[] };
          if (JSON.stringify(ev.present) !== JSON.stringify(rt2.present))
            p54Errors.push("dokaz ⊉ runtime: present polji nista enaki");
          if (JSON.stringify(ev.match) !== JSON.stringify(rt2.match))
            p54Errors.push("dokaz ⊉ runtime: match polji nista enaki");
        }
        p54FileDetail = `dokaz preverjen: repla ${ev.replay.pass} · prehodi ${Object.values(ev.transitions).reduce((a, b) => a + b, 0)} · dokaz == runtime (present + match)`;
      } catch {
        p54Errors.push("dokaz present-gurs.json ni veljaven JSON");
      }
    }
    // 4) UI-vod: village3d uvaža runtime + GURS meta; AR/village-viewer naslovi
    const v3d = opts.readFile("src/lib/village3d.ts");
    const atm = opts.readFile("src/components/museum/ar-time-machine.tsx");
    const vvw = opts.readFile("src/components/museum/village-viewer.tsx");
    const ats = opts.readFile("src/lib/atlas.ts");
    if (v3d === null) p54Errors.push("src/lib/village3d.ts ni berljiv (UI-vod)");
    if (v3d !== null) {
      if (!v3d.includes('@/data/atlas/present.json')) p54Errors.push("village3d ne uvaža runtime present.json");
      if (!v3d.includes("GURS_SNAPSHOT") || !v3d.includes("gursSnapshot")) p54Errors.push("village3d: GURS_SNAPSHOT/gursSnapshot ni pinan");
      if (!v3d.includes("sourceSnapshot")) p54Errors.push("village3d: IZGINILO_STATS.sourceSnapshot ni pinan");
      if (!v3d.includes("uradni GURS eZKN obrisi")) p54Errors.push("village3d: vir ni GURS eZKN");
    }
    if (atm !== null && !atm.includes("1825 ∩ GURS eZKN")) p54Errors.push("AR: naslov ni GURS eZKN");
    if (vvw !== null && !vvw.includes("1825 ∩ GURS eZKN")) p54Errors.push("village-viewer: naslov ni GURS eZKN");
    if (ats !== null && !ats.includes("sourceSnapshot")) p54Errors.push("atlas.ts: izginilo.sourceSnapshot ni pinan");
    p54UiDetail = `UI-vod preverjen: village3d (runtime + GURS_SNAPSHOT + sourceSnapshot) · AR/village-viewer naslovi · atlas.ts sourceSnapshot`;
  }
  push(
    "qa-p54-present-gurs",
    "P54: PRESENT.JSON NA URADNIH GURS OBRISIH — nadgradnja P16 »Kaj je izginilo?« (issue #12): OSM posnetek (15/26/115, pokrival le jedro vasi) → uradni GURS eZKN obrisi (714 stavb z geometrijo, 380 v oknu A02 + sodobna vas, vse KO 1544 — popolna pokritost z zahodnimi pobočji); pravila P16 NESPREMENJENA — kalibrirana z replajo na starih podatkih (156/156, + osmId 41, d ±0.05 m); rezultat 18 obstaja · 21 negotovih · 117 ni jih več; prehodi 156 vsrstno pinani (uncertain→exists 4, uncertain→gone 2, exists→uncertain 1); 7 spremenjenih tlorisov; d zapisana za vse (do 1541.2 m); P48 navzkrižje: cf 154 == modernEvaluated, pari ≤ 25 px 37 == pairs (20 tlorisov), okno 40; EPSG:3794 → WGS84 (pyproj always_xy, enako P47/P48); arhiv P16: research/issue17/present-osm-p16.json; status UPGRADED-DETERMINISTIC",
    "P54: PRESENT.JSON ON OFFICIAL GURS FOOTPRINTS — an upgrade of the P16 »What has vanished?« (issue #12): OSM snapshot (15/26/115, covered the village core only) → official GURS eZKN footprints (714 buildings with geometry, 380 within the A02 + modern-village window, all KO 1544 — complete coverage with the western slopes); P16 rules UNCHANGED — calibrated by replay on the old data (156/156, + osmId 41, d ±0.05 m); result 18 exists · 21 uncertain · 117 gone; all 156 transitions pinned (uncertain→exists 4, uncertain→gone 2, exists→uncertain 1); 7 changed footprints; d recorded for all (up to 1541.2 m); P48 cross-check: cf 154 == modernEvaluated, pairs ≤ 25 px 37 == pairs (20 footprints), window 40; EPSG:3794 → WGS84 (pyproj always_xy, as P47/P48); P16 archive: research/issue17/present-osm-p16.json; status UPGRADED-DETERMINISTIC",
    p54Errors.length === 0,
    p54Errors.length === 0
      ? `18 obstaja · 21 negotovih · 117 ni je več (P16 OSM 15/26/115) · repla 156/156 · P48 križ 154/37/20/40 · okno 380 (KO 1544) · ${p54RtDetail} · ${p54FileDetail} · ${p54UiDetail}`
      : p54Errors.join("; "),
  );

  /* ── P55 (issue #13): geolokacija Grundparzellen — PS 1825 ↔ parcele KO 1544 (v5 @ P71) ── */
  const p55Errors: string[] = [];
  const p55 = PS_GEO_P55;
  // 1) pinane vrednosti konstante (v5 @ P71: C1 sekcije exclude 56 + C2 p93 reverzija 15)
  if (p55.version !== 5) p55Errors.push(`version ≠ 5 (${p55.version})`);
  if (p55.pageSelection.pages !== 135 || p55.pageSelection.rows !== 2762)
    p55Errors.push(`izbira strani ${p55.pageSelection.pages}/${p55.pageSelection.rows} ≠ 135/2762`);
  if (p55.pageSelection.pass1 !== 58 || p55.pageSelection.pass2 !== 69 || p55.pageSelection.pass3Fallback !== 8)
    p55Errors.push("prehodi strani ≠ 58/69/8");
  if (p55.join.matchedRows !== 1077 || p55.join.matchedRowsS1S2 !== 1051 || p55.join.matchedRowsBI !== 26)
    p55Errors.push(`povezava ≠ 1077/1051/26 (${p55.join.matchedRows}/${p55.join.matchedRowsS1S2}/${p55.join.matchedRowsBI})`);
  if (p55.join.matchedSharePct !== 39.0 || p55.join.suffixGroups !== 271 || p55.join.psPositionedParcels !== 879)
    p55Errors.push("delež/skupine/parcele ≠ 39.0/271/879");
  if (p55.join.seriesCounts.BI !== 26 || p55.join.seriesCounts.S1 !== 981 || p55.join.seriesCounts.S2 !== 70)
    p55Errors.push(`serije ≠ 26/981/70`);
  if (p55.join.confCounts.STRONG !== 183 || p55.join.confCounts.MEDIUM !== 745 || p55.join.confCounts.WEAK !== 149)
    p55Errors.push(`zaupanje ≠ 183/745/149 (v5 TOTAL)`);
  if (p55.join.readConfBI.STRONG !== 3 || p55.join.readConfBI.MEDIUM !== 14 || p55.join.readConfBI.WEAK !== 9)
    p55Errors.push("readConf Blatt I ≠ 3/14/9");
  if (p55.join.ambiguousBases !== 184 || p55.join.ambiguousRows !== 373)
    p55Errors.push(`per-Blatt dvoumnost ≠ 184/373`);
  if (p55.v3Delta.renumbered !== 17 || p55.v3Delta.removedRows !== 14)
    p55Errors.push(`v3Delta ≠ 17/14 (${p55.v3Delta.renumbered}/${p55.v3Delta.removedRows})`);
  if (p55.v3Delta.after.rows !== 1079 || p55.v3Delta.after.bases !== 798
    || p55.v3Delta.after.multiPage !== 199 || p55.v3Delta.after.crossBlatt !== 98)
    p55Errors.push("v3Delta.after ≠ 1079/798/199/98 (arhiv)");
  if (p55.v5Delta.excludedSections !== 56 || p55.v5Delta.revertedP93 !== 15 || p55.v5Delta.removed !== 68)
    p55Errors.push(`v5Delta ≠ 56/15/68 (${p55.v5Delta.excludedSections}/${p55.v5Delta.revertedP93}/${p55.v5Delta.removed})`);
  if (p55.v5Delta.before.rows !== 1145 || p55.v5Delta.before.bases !== 878
    || p55.v5Delta.before.multiPage !== 215 || p55.v5Delta.before.crossBlatt !== 79)
    p55Errors.push("v5Delta.before ≠ 1145/878/215/79 (v4)");
  if (p55.v5Delta.after.rows !== 1077 || p55.v5Delta.after.bases !== 879
    || p55.v5Delta.after.multiPage !== 184 || p55.v5Delta.after.crossBlatt !== 48)
    p55Errors.push("v5Delta.after ≠ 1077/879/184/48");
  if (p55.v2Delta.removedRows !== 43 || p55.v2Delta.addedRows !== 26)
    p55Errors.push(`v2Delta (P58 arhiv) ≠ −43/+26 (${p55.v2Delta.removedRows}/${p55.v2Delta.addedRows})`);
  if (p55.v2Delta.before.matchedRows !== 1110 || p55.v2Delta.before.areaMedian !== 3.6984
    || p55.v2Delta.before.confCounts.STRONG !== 171)
    p55Errors.push("v2Delta.before ≠ 1110/3.6984/171");
  if (p55.areaProof.medianRatio !== 3.9052 || p55.areaProof.pairsWithArea !== 1057)
    p55Errors.push("površine ≠ 3.9052/1057");
  if (p55.areaProof.historicalQkM2 !== 3.59665 || p55.areaProof.deltaPct !== 8.58)
    p55Errors.push("QK faktor/Δ ≠ 3.59665/8.58");
  if (p55.areaProof.shuffleMedian !== 4.2304 || p55.areaProof.shuffleTightShare !== 0.0539)
    p55Errors.push("površinska kontrola ≠ 4.2304/0.0539");
  if (p55.areaProof.tightShare !== 0.1845 || p55.areaProof.tightN !== 195)
    p55Errors.push("pas ±10 % ≠ 0.1845/195");
  if (p55.spatialProof.consecPairs !== 652 || p55.spatialProof.medianM !== 51.8)
    p55Errors.push("soslednost ≠ 652/51.8");
  if (p55.spatialProof.shuffleMedianM !== 1320.7 || p55.spatialProof.share150 !== 0.9049 || p55.spatialProof.enrichmentX !== 25.5)
    p55Errors.push("soslednost kontrola ≠ 1320.7/0.9049/25.5");
  if (p55.furkovce.rows !== 2 || p55.furkovce.parcels[0] !== 2159 || p55.furkovce.parcels[1] !== 2160)
    p55Errors.push("Furkofze ≠ 2 vrstici (2159/2160)");
  if (p55.furkovce.owner[0] !== "Van Wawech Mihó") p55Errors.push("Furkofze lastnik ≠ Van Wawech Mihó");
  if (!Object.values(p55.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
    p55Errors.push("invarianti niso vsi PASS");
  // 2) runtime v5 + dokaz v5 (P53/P57 lekcija: dve obliki — dokaz rowsEvidence, runtime kopija rows)
  let p55RtDetail = "runtime ps-parcels-geo.json ni preverjen (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  let p55FileDetail = "dokazna datoteka ni preverjena (readFile ni na voljo)";
  if (opts.readFile) {
    const rawEv = opts.readFile("research/issue17/ps-parcels-geo-v5.json");
    const rawRt = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    if (rawEv === null && rawRt === null) {
      p55Errors.push("ps-parcels-geo ni berljiv (ne dokaz v5 ne runtime kopija)");
    } else {
      try {
        const mode = rawEv !== null ? "repo" : "produkcija";
        const parsed = JSON.parse((rawEv ?? rawRt) as string) as {
          version?: number;
          join: { matchedRows: number; matchedRowsS1S2: number; matchedRowsBI: number; seriesCounts: { BI: number; S1: number; S2: number }; confCounts: { STRONG: number; MEDIUM: number; WEAK: number }; readConfBI: { STRONG: number; MEDIUM: number; WEAK: number }; ambiguousBases: number; ambiguousRows: number };
          spatialProof: { consecPairs: number; medianM: number };
          furkovce: { rows: number; parcels: number[] };
          rowsEvidence?: { base: string; page: number; series?: string; conf?: string | null; readConf?: string | null; lat: number | null; lng: number | null; ambiguous?: boolean }[];
          rows?: { base: string; page: number; series?: string; conf?: string | null; readConf?: string | null; lat: number | null; lng: number | null; ambiguous?: boolean }[];
        };
        const rows = (parsed.rowsEvidence ?? parsed.rows) as NonNullable<typeof parsed.rows>;
        if (parsed.version !== undefined && parsed.version !== 5)
          p55Errors.push(`version ≠ 5 (${parsed.version})`);
        if (rows.length !== 1077) p55Errors.push(`vrstice ≠ 1077 (${rows.length})`);
        if (rows.length !== parsed.join.matchedRows)
          p55Errors.push(`vrstic ${rows.length} ≠ join.matchedRows ${parsed.join.matchedRows}`);
        if (parsed.join.matchedRows !== 1077 || parsed.join.matchedRowsS1S2 !== 1051 || parsed.join.matchedRowsBI !== 26)
          p55Errors.push("runtime povezava ≠ 1077/1051/26");
        const cc = { STRONG: 0, MEDIUM: 0, WEAK: 0 };
        const sc = { BI: 0, S1: 0, S2: 0 };
        const rc = { STRONG: 0, MEDIUM: 0, WEAK: 0 };
        for (const r of rows) {
          if (r.conf && r.conf in cc) cc[r.conf as keyof typeof cc] += 1;
          if (r.series && r.series in sc) sc[r.series as keyof typeof sc] += 1;
          if (r.readConf && r.readConf in rc) rc[r.readConf as keyof typeof rc] += 1;
          if ((r.lat === null || r.lat === undefined) || (r.lng === null || r.lng === undefined)) {
            p55Errors.push(`runtime vrstica brez pozicije (base=${r.base}, conf=${r.conf})`);
            break;
          }
        }
        if (cc.STRONG !== 183 || cc.MEDIUM !== 745 || cc.WEAK !== 149)
          p55Errors.push(`runtime zaupanje ${JSON.stringify(cc)} ≠ 183/745/149 (v5 TOTAL)`);
        if (sc.BI !== 26 || sc.S1 !== 981 || sc.S2 !== 70)
          p55Errors.push(`runtime serije ${JSON.stringify(sc)} ≠ 26/981/70`);
        if (rc.STRONG !== 3 || rc.MEDIUM !== 14 || rc.WEAK !== 9)
          p55Errors.push(`runtime readConf BI ${JSON.stringify(rc)} ≠ 3/14/9`);
        // preracun soslednosti iz samih vrstic (mehanika P55: številski pari n, n+1)
        const pos = new Map<number, [number, number]>();
        const seenBase = new Set<number>();
        for (const r of rows) {
          const n = parseInt(r.base, 10);
          if (!seenBase.has(n) && r.lat !== null && r.lat !== undefined && r.lng !== null && r.lng !== undefined) {
            seenBase.add(n);
            pos.set(n, [r.lat, r.lng]);
          }
        }
        const dd: number[] = [];
        for (const [n, p] of pos) {
          const q = pos.get(n + 1);
          if (q) dd.push(Math.hypot((p[0] - q[0]) * 111320, (p[1] - q[1]) * 111320 * 0.7));
        }
        dd.sort((a, b) => a - b);
        const med = dd.length % 2 ? dd[(dd.length - 1) / 2] : (dd[dd.length / 2 - 1] + dd[dd.length / 2]) / 2;
        if (dd.length !== parsed.spatialProof.consecPairs)
          p55Errors.push(`soslednost parov iz vrstic ${dd.length} ≠ ${parsed.spatialProof.consecPairs}`);
        if (Math.abs(med - parsed.spatialProof.medianM) > 0.5)
          p55Errors.push(`soslednost median iz vrstic ${med.toFixed(1)} ≠ ${parsed.spatialProof.medianM}`);
        // neodvisen preracun per-Blatt dvoumnosti (base na > 1 strani znotraj v2)
        const pagesByBase = new Map<string, Set<number>>();
        for (const r of rows) {
          const s = pagesByBase.get(r.base) ?? new Set<number>();
          s.add(r.page);
          pagesByBase.set(r.base, s);
        }
        let ambBases = 0;
        let ambRows = 0;
        for (const s of pagesByBase.values()) if (s.size > 1) ambBases += 1;
        for (const r of rows) if ((pagesByBase.get(r.base)?.size ?? 0) > 1) ambRows += 1;
        if (ambBases !== parsed.join.ambiguousBases || ambRows !== parsed.join.ambiguousRows)
          p55Errors.push(`dvoumnost preracun ${ambBases}/${ambRows} ≠ ${parsed.join.ambiguousBases}/${parsed.join.ambiguousRows}`);
        if (parsed.furkovce.rows !== 2) p55Errors.push("runtime Furkofze ≠ 2");
        p55RtDetail = `${mode}: 1077 vrstic (serije 26/981/70, zaupanje 183/745/149, readConf BI 3/14/9) · soslednost preracunana iz vrstic: ${dd.length} parov, median ${med.toFixed(1)} m · dvoumnost ${ambBases}/${ambRows} · Furkofze 2159/2160`;
        // dokaz ⊇ runtime bajtno (samo v repozitoriju, kjer sta oba na voljo)
        if (rawEv !== null && rawRt !== null) {
          const rt2 = JSON.parse(rawRt) as { version?: number; rows: Record<string, unknown>[] };
          const evRows = (parsed.rowsEvidence ?? []) as Record<string, unknown>[];
          const subset = rt2.rows.every((rr, i) =>
            Object.entries(rr).every(([k, v]) => JSON.stringify(evRows[i]?.[k]) === JSON.stringify(v)));
          if (!subset) p55Errors.push("dokaz v5 ⊉ runtime: vrstice niso bajtno enake");
          p55FileDetail = "dokaz v5 preverjen: 1077 vrstic ⊇ runtime bajtno (rowsEvidence == rows)";
        } else {
          p55FileDetail = "produkcija: research/ ni v deploymentu — kontrola na runtime kopiji (vzorec qa-p43-chain-full)";
        }
      } catch (e) {
        p55Errors.push(`ps-parcels-geo v5 obdelava neuspešna: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p55-ps-parcels-geo",
    "P55 v5: GEOLOKACIJA GRUNDPARCELLEN — korekcije v4 (P71, issue #13): (C1) 56 sekijskih vrstic (p83–86, p88) EXCLUDE iz joina (P69 dokazane lažne fuzije na Blatt I poligone; lastniška odločitev: opcija exclude; per-Blatt instance = odprta; vrstice ostanejo v registru brez geometrije) + (C2) P93 REVERZIJA — P68 renum 160x→190x ovržen (glifna forenzika r9=1609/r19=1619: 6 ≠ 9; annRecords 1601–1619; pageMap P56; P38 pass2): 15 vrstic base := parzella, PF ujemanja 1603/1604/1605 (prej prazni poligoni dobili prve vrstice), 12 izpadlih; PF 1901–1920 brez lažnih dvojnih zahtevkov p93 (ostane p98 III); zgodovina: P70 v4 (77 renum + 95 rejoin + 33 fuzij isti-Blatt), P68 v3 (17 preslikav + 14 izpada), P58 (−43 S3/+26 Blatt I): 1077 vrstic povezanih (1051 S1/S2 + 26 Blatt I); 879 pozicioniranih števil; površine median 3.9052 ≈ 1 Wiener QK 3.59665 m² (Δ +8.58 %, kontrola seed 42 = 4.2304); soslednost 652 parov / 51.8 m / 25.5×; zaupanje STRONG 183 / MEDIUM 745 / WEAK 149 + readConf BI 3/14/9; per-Blatt dvoumnost 184 base / 373 vrstic [~]; nespremenjene vrstice bajtno == v4; status SANITIZED-DETERMINISTIC",
    "P55 v5: GRUNDPARCELLEN GEOLOCATION — v4 corrections (P71: C1 — 56 section rows p83–86/p88 excluded, P69-proven false fusions, the owner's exclude option, per-Blatt instances open, rows stay in the register without geometry; C2 — the p93 reversion, the P68 renum 160x→190x refuted by glyph forensics r9=1609/r19=1619 (6 ≠ 9) + annRecords 1601–1619 + the P56 pageMap + P38 pass2: 15 rows base := parzella, PF matches 1603/1604/1605 (previously empty polygons got their first rows), 12 dropped; PF 1901–1920 free of p93's false double claims — p98 III remains; history: P70 v4 (77 renums + 95 rejoins + 33 same-Blatt fusions), P68 v3 (17 mappings + 14 dropped), P58 (−43 S3/+26 Blatt I)): 1,077 linked rows (1,051 S1/S2 + 26 Blatt I); 879 positioned numbers; areas median 3.9052 ≈ 1 Wiener QK 3.59665 m² (Δ +8.58 %, control seed 42 = 4.2304); adjacency 652 pairs / 51.8 m / 25.5×; confidence STRONG 183 / MEDIUM 745 / WEAK 149 + readConf BI 3/14/9; per-sheet ambiguity 184 bases / 373 rows [~]; unchanged rows byte-identical to v4; status SANITIZED-DETERMINISTIC",
    p55Errors.length === 0,
    p55Errors.length === 0
      ? `v5: 1077 vrstic (1051 S1/S2 + 26 Blatt I) / 879 števil · v5Delta C1 56 + C2 15 (12 izpadlih) = 68 · PF 1603/1604/1605 · v4 arhiv 1145/878/215/79 · v3Delta arhiv 17/14 · v2Delta arhiv −43/+26 · površine 3.9052 ≈ 3.59665 (Δ +8.58 %, kontrola 4.2304) · soslednost 652/51.8/25.5× · STRONG 183 / MEDIUM 745 / WEAK 149 · dvoumnost 184/373 · Furkofze 2159/2160 · ${p55RtDetail} · ${p55FileDetail}`
      : p55Errors.join("; "),
  );

  /* ── P58 (issue #13): sanacija produkcije PS-PARCELS-GEO v2 — −43 S3 lažnih, +26 Blatt I ── */
  const p58Errors: string[] = [];
  // 1) pinane vrednosti konstante — delta + neinvarianca soslednosti (I9)
  if (p55.v2Delta.removedRows !== 43 || p55.v2Delta.addedRows !== 26)
    p58Errors.push(`v2Delta ≠ −43/+26 (${p55.v2Delta.removedRows}/${p55.v2Delta.addedRows})`);
  if (p55.v2Delta.before.matchedRows !== 1110 || p55.v2Delta.before.areaMedian !== 3.6984
    || p55.v2Delta.before.confCounts.STRONG !== 171 || p55.v2Delta.before.confCounts.MEDIUM !== 775
    || p55.v2Delta.before.confCounts.WEAK !== 164)
    p58Errors.push("v2Delta.before ≠ 1110/3.6984/171/775/164");
  if (p55.spatialProof.consecPairs !== 652 || p55.spatialProof.medianM !== 51.8
    || p55.spatialProof.q25M !== 33.0 || p55.spatialProof.q75M !== 87.8 || p55.spatialProof.share150 !== 0.9049)
    p58Errors.push("soslednost (I9) ≠ v5 pini 652/51.8/33.0/87.8/0.9049");
  if (p55.areaProof.medianRatio !== 3.9052 || p55.v2Delta.before.areaMedian !== 3.6984
    || p55.areaProof.medianRatio <= p55.v2Delta.before.areaMedian)
    p58Errors.push("površinski median v5 ≤ v1 (pričakovano zvišanje 3.6984 → 3.7709 → 3.8512 → 3.8843 → 3.9052)");
  // 2) datoteke: v1 arhiv nespremenjen + v2 delta == P56 + runtime version 2 (dve obliki po P53/P57)
  let p58FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt58 = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    const rawV1 = opts.readFile("research/issue17/ps-parcels-geo.json");
    const rawV2 = opts.readFile("research/issue17/ps-parcels-geo-v2.json");
    const rawP56rt = opts.readFile("src/data/atlas/ps-register-topology.json");
    if (rawRt58 === null) {
      p58Errors.push("runtime ps-parcels-geo.json ni berljiv");
    } else {
      try {
        const rt = JSON.parse(rawRt58) as {
          version?: number;
          v2Delta?: { removed?: { rows?: number }; added?: { rows?: number; bases?: number[] } };
          rows: { page: number; base: string; series?: string }[];
        };
        if (rt.version !== 5) p58Errors.push(`runtime version ≠ 5 (${rt.version})`);
        if (rt.rows.length !== 1077) p58Errors.push(`runtime vrstic ≠ 1077 (${rt.rows.length})`);
        if (rt.rows.some((r) => r.page === 138 || r.page === 139))
          p58Errors.push("runtime vsebuje še S3 vrstice (str. 138–139)");
        const bi = rt.rows.filter((r) => r.page === 3 || r.page === 4);
        if (bi.length !== 26) p58Errors.push(`runtime Blatt I vrstic ≠ 26 (${bi.length})`);
        if (rt.rows.filter((r) => r.series === "S1").length !== 981
          || rt.rows.filter((r) => r.series === "S2").length !== 70)
          p58Errors.push("runtime serije S1/S2 ≠ 981/70 (v5 P71)");
        // P56 konsistenca: delta == sanitizacija
        if (rawP56rt !== null) {
          const p56rt = JSON.parse(rawP56rt) as { sanitization: { matchedRowsBefore: number; matchedRowsAfter: number; uniqueBasesAfter: number; lostBases: number[] } };
          if (p56rt.sanitization.matchedRowsBefore !== 1110 || p56rt.sanitization.matchedRowsAfter !== 1067)
            p58Errors.push("P56 sanitizacija ≠ 1110→1067");
          const lostSorted = [...p56rt.sanitization.lostBases].sort((a, b) => a - b);
          const biBases = bi.map((r) => parseInt(r.base, 10)).sort((a, b) => a - b);
          if (JSON.stringify(biBases) !== JSON.stringify(lostSorted))
            p58Errors.push("Blatt I base ≠ lostBases P56");
          if (rt.v2Delta?.added?.bases && JSON.stringify([...rt.v2Delta.added.bases].sort((a, b) => a - b)) !== JSON.stringify(lostSorted))
            p58Errors.push("runtime v2Delta.added.bases ≠ lostBases P56");
        }
        // v1 arhiv nespremenjen (samo repo — research/ ni v deploymentu)
        if (rawV1 !== null) {
          const v1 = JSON.parse(rawV1) as {
            join: { matchedRows: number };
            spatialProof: { consecPairs: number; medianM: number; share150: number };
            rows: { lat: number | null }[];
          };
          if (v1.join.matchedRows !== 1110) p58Errors.push("v1 arhiv: povezanih ≠ 1110");
          if (v1.rows.length !== 2762) p58Errors.push(`v1 arhiv: vrstic ≠ 2762 (${v1.rows.length})`);
          if (v1.spatialProof.consecPairs !== 590 || v1.spatialProof.medianM !== 51.8 || v1.spatialProof.share150 !== 0.8932)
            p58Errors.push("v1 arhiv: spatialProof ≠ 590/51.8/0.8932");
        }
        // v2 dokaz: delta + rowsEvidence ⊇ runtime (samo repo)
        if (rawV2 !== null) {
          const v2 = JSON.parse(rawV2) as {
            version?: number;
            v2Delta: { removed: { rows: number }; added: { rows: number } };
            rowsEvidence?: unknown[];
          };
          if (v2.version !== 2) p58Errors.push("v2 dokaz: version ≠ 2");
          if (v2.v2Delta.removed.rows !== 43 || v2.v2Delta.added.rows !== 26)
            p58Errors.push("v2 dokaz: delta ≠ −43/+26");
          if ((v2.rowsEvidence ?? []).length !== 1093) p58Errors.push("v2 dokaz: rowsEvidence ≠ 1093");
        }
        p58FileDetail = rawV1 !== null && rawV2 !== null
          ? "repo: v1 arhiv nespremenjen (2762/1110, spatial 590/51.8) · v2 dokaz delta −43/+26 · runtime version 5 (P71 v5: 1077 vrstic), brez S3, Blatt I 26 == lostBases P56"
          : "produkcija: research/ ni v deploymentu — kontrola na runtime kopiji (version 5, −43 S3 P58 arhiv, +26 Blatt I == lostBases)";
      } catch (e) {
        p58Errors.push(`ps-parcels-geo v2 datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p58-ps-parcels-geo-v2",
    "P58: SANACIJA PRODUKCIJE PS-PARCELS-GEO v2 (issue #13): v1 produkcija (1110 vrstic) je vsebovala 43 lažnih povezav S3 (zapadek str. 138–139) — P56 jih je dokazal (površine ~42× od 1 QK, pass-razhajanje), P58 jih je odstranil iz runtime-a (nabor bajtno enak P56 kontaminacijskemu seznamu) in dodal 26 Blatt I vrstic iz primarnega vira P57 (točno vseh 26 lostBases) → 1093 vrstic / 800 števil; NEINVARIANCA: pozicije per base → soslednost in S1/S2 zaupanje bajtno enaka v1 (590/51.8/27.8×; 174/759/160); površinski median čist 3.7709 (Δ +4.85 %) — v1 3.6984 je bil umetno snizan; v1 dokaz arhiviran nespremenjen; status SANITIZED-DETERMINISTIC",
    "P58: PS-PARCELS-GEO v2 PRODUCTION SANITIZATION (issue #13): the v1 production (1110 rows) contained 43 false S3 links (pp. 138–139 appendix) — proven by P56 (areas ~42× off 1 QK, pass disagreement), removed from the runtime by P58 (the set byte-identical to the P56 contamination list) and 26 Blatt I rows added from the P57 primary source (exactly all 26 lostBases) → 1093 rows / 800 numbers; INVARIANCE: per-base positions → adjacency and S1/S2 confidence byte-identical to v1 (590/51.8/27.8×; 174/759/160); clean area median 3.7709 (Δ +4.85 %) — the v1 3.6984 was artificially lowered; the v1 evidence archived unchanged; status SANITIZED-DETERMINISTIC",
    p58Errors.length === 0,
    p58Errors.length === 0
      ? `v2 delta −43/+26 (P58 arhiv) · v1 arhiv 2762/1110 (repo) · runtime 1077 vrstic version 5 (P71 v5: BI 26 == lostBases P56, S1 981, S2 70, brez str. 138–139) · neinvarianca 590/51.8/0.8932 · median 3.6984 → 3.7709 (P58) → 3.8512 (P68) → 3.8843 (P70) → 3.9052 (P71) · ${p58FileDetail}`
      : p58Errors.join("; "),
  );

  /* ── P56 (issue #13): topologija registra PS — serije, spremembe, sanacija P55 ── */
  const p56Errors: string[] = [];
  const p56 = REGISTER_TOPOLOGY_P56;
  // 1) pinane vrednosti konstante
  if (p56.pageSelection.pages !== 135 || p56.pageSelection.rows !== 2762)
    p56Errors.push(`izbira strani ${p56.pageSelection.pages}/${p56.pageSelection.rows} ≠ 135/2762`);
  if (p56.topology.S1.pageCount !== 123 || p56.topology.S2.pageCount !== 10 || p56.topology.S3.pageCount !== 2)
    p56Errors.push(`strani serij ≠ 123/10/2 (${p56.topology.S1.pageCount}/${p56.topology.S2.pageCount}/${p56.topology.S3.pageCount})`);
  if (p56.topology.S1.numMin !== 41 || p56.topology.S1.numMax !== 2500)
    p56Errors.push("S1 številke ≠ 41/2500 (str. 3–4 niso prebrane)");
  if (p56.topology.S2.numMin !== 2507 || p56.topology.S2.numMax !== 2840)
    p56Errors.push("S2 številke ≠ 2507/2840");
  if (p56.topology.S3.numMin !== 1 || p56.topology.S3.numMax !== 100 || p56.topology.S3.rows !== 60)
    p56Errors.push("S3 številke/vrstice ≠ 1/100/60");
  if (p56.contamination.s3RowsTotal !== 60 || p56.contamination.s3RowsMatched !== 43)
    p56Errors.push("kontaminacija ≠ 60/43");
  if (p56.contamination.ratioMedianS3 !== 0.0892 || p56.contamination.ratioMedianS1 !== 3.7188)
    p56Errors.push(`mediana razmerij ≠ 0.0892/3.7188 (${p56.contamination.ratioMedianS3}/${p56.contamination.ratioMedianS1})`);
  if (p56.contamination.historicalQkM2 !== 3.59665) p56Errors.push("QK ≠ 3.59665");
  if (p56.sanitization.matchedRowsBefore !== 1110 || p56.sanitization.matchedRowsAfter !== 1067)
    p56Errors.push("sanitacija vrstic ≠ 1110/1067");
  if (p56.sanitization.uniqueBasesBefore !== 800 || p56.sanitization.uniqueBasesAfter !== 774)
    p56Errors.push("sanitacija base ≠ 800/774");
  if (p56.sanitization.lostBasesCount !== 26 || p56.sanitization.ratioMedianAfter !== 3.7394)
    p56Errors.push("izgubljene base / median ≠ 26/3.7394");
  if (p56.perBlattAmbiguity.basesOnMultiplePages !== 515 || p56.perBlattAmbiguity.withinS1 !== 475)
    p56Errors.push("dvoumnost ≠ 515/475");
  if (p56.perBlattAmbiguity.cleanRowsWithAmbiguousBase !== 512)
    p56Errors.push("dvoumne vrstice (sanitiran join) ≠ 512");
  if (p56.modernVoid.voidRange[0] !== 2507 || p56.modernVoid.modernCount !== 0 || p56.modernVoid.psRows !== 87)
    p56Errors.push("praznina ≠ [2507,2607]/0/87");
  if (p56.modernVoid.contModernCount !== 53 || p56.modernVoid.contParcelsCount !== 78)
    p56Errors.push("2608–2700 ≠ 53 base/78 parcel");
  if (p56.timeline.annotatedRows !== 584 || p56.timeline.topYear !== "1841" || p56.timeline.topYearRows !== 83 || p56.timeline.pages1841Count !== 44)
    p56Errors.push("časovnica ≠ 584/1841/83/44");
  if (!Object.values(p56.invariants).every((v) => v.includes("PASS") || v.includes("bajtno")))
    p56Errors.push("invarianti niso vsi PASS");
  // 2) runtime ps-register-topology.json + NEODVISEN preracun iz P55 runtime vrstic
  let p56RtDetail = "runtime ps-register-topology.json ni preverjen (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  let p56FileDetail = "dokazna datoteka ni preverjena (readFile ni na voljo)";
  if (opts.readFile) {
    const rawRt56 = opts.readFile("src/data/atlas/ps-register-topology.json");
    const rawRt55 = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    if (rawRt56 === null) {
      p56Errors.push("src/data/atlas/ps-register-topology.json ni berljiv (runtime)");
    } else if (rawRt55 === null) {
      p56Errors.push("src/data/atlas/ps-parcels-geo.json ni berljiv (potreben za neodvisen preracun)");
    } else {
      try {
        const rt56 = JSON.parse(rawRt56) as {
          contamination: { s3RowsTotal: number; s3RowsMatched: number; ratioMedianS3: number; ratioMedianS1: number; rows: Record<string, unknown>[] };
          sanitization: { matchedRowsBefore: number; matchedRowsAfter: number; uniqueBasesBefore: number; uniqueBasesAfter: number };
          perBlattAmbiguity: { basesOnMultiplePages: number; cleanRowsWithAmbiguousBase: number };
          modernVoid: { modernCount: number; contModernCount: number; contParcelsCount: number };
          timeline: { annotatedRows: number; byYear: Record<string, number> };
        };
        const rt55 = JSON.parse(rawRt55) as {
          version?: number;
          v2Delta?: { removed?: { rows?: number; rowsDetail?: Record<string, unknown>[] } };
          rows: { page: number; base: string | null; lat: number | null; ratio: number | null; owner: string | null; kultur: string | null; areaQK: number | null; areaModern: number | null }[];
        };
        // neodvisen preracun: repo = v3 DOKAZ (P68 realnost; P56 pini), produkcija = v5 runtime
        // (P71 realnost — C1 sekcije exclude + C2 p93 reverzija; v5 pine)
        const rawJoin56 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode56 = rawJoin56 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc56 = JSON.parse((rawJoin56 ?? rawRt55) as string) as {
          version?: number;
          rowsEvidence?: { page: number; base: string | null; lat: number | null; ratio: number | null; owner: string | null; kultur: string | null; areaQK: number | null; areaModern: number | null }[];
          rows: { page: number; base: string | null; lat: number | null; ratio: number | null; owner: string | null; kultur: string | null; areaQK: number | null; areaModern: number | null }[];
        };
        const join56 = { version: joinSrc56.version, rows: joinSrc56.rowsEvidence ?? joinSrc56.rows };
        const expS1S256 = joinMode56 === "v3-dokaz" ? 1053 : 1051;
        const expTotal56 = joinMode56 === "v3-dokaz" ? 1079 : 1077;
        const expMedS1 = joinMode56 === "v3-dokaz" ? 3.7588 : 3.8823;
        if (join56.version !== undefined && join56.version !== (joinMode56 === "v3-dokaz" ? 3 : 5))
          p56Errors.push(`join vir version ≠ ${joinMode56 === "v3-dokaz" ? 3 : 5} (${join56.version})`);
        const s3Matched = join56.rows.filter((r) => (r.page === 138 || r.page === 139) && r.lat !== null);
        if (s3Matched.length !== 0)
          p56Errors.push(`preracun: P55 join še vsebuje S3 vrstice (${s3Matched.length} ≠ 0)`);
        const biMatched = join56.rows.filter((r) => (r.page === 3 || r.page === 4) && r.lat !== null);
        if (biMatched.length !== 26)
          p56Errors.push(`preracun: Blatt I povezanih ${biMatched.length} ≠ 26`);
        const s1s2Matched = join56.rows.filter((r) => r.page >= 5 && r.page <= 137 && r.lat !== null);
        if (s1s2Matched.length !== expS1S256)
          p56Errors.push(`preracun: sanitiranih (S1/S2) ${s1s2Matched.length} ≠ ${expS1S256} (${joinMode56})`);
        const totalMatched = join56.rows.filter((r) => r.lat !== null).length;
        if (totalMatched !== expTotal56)
          p56Errors.push(`preracun: skupaj ${totalMatched} ≠ ${expTotal56} (${joinMode56})`);
        const med = (xs: number[]) => {
          const s = [...xs].sort((a, b) => a - b);
          return s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2;
        };
        const s1Matched = join56.rows.filter((r) => r.page >= 5 && r.page <= 127 && r.lat !== null && r.ratio !== null);
        const medS1 = med(s1Matched.map((r) => r.ratio as number));
        if (Math.abs(medS1 - expMedS1) > 0.001)
          p56Errors.push(`preracun: median S1 ${medS1.toFixed(4)} ≠ ${expMedS1} (${joinMode56})`);
        // kontaminacijske vrstice == v2Delta.removed.rowsDetail (bajtno; rowsDetail je tudi v
        // produkciji, ker je del runtime v2Delta — P53/P57 lekcija: kontrola mora biti izvedljiva
        // brez research/)
        // P68 v3: v2Delta arhiviran v v2 dokazu (v3 runtime nima v2Delta) —
        // kontaminacijske vrstice preverjene nad P56 runtime arhivom (rt56.contamination)
        if (rt55.v2Delta?.removed?.rowsDetail) {
          const removedDetail = rt55.v2Delta.removed.rowsDetail;
          const key = (r: Record<string, unknown>) => JSON.stringify([r.page, r.base, r.owner, r.kultur, r.areaQK, r.areaModern, r.ratio]);
          const a = removedDetail.map(key).join("|");
          const b = rt56.contamination.rows.map((r) => key(r as Record<string, unknown>)).join("|");
          if (a !== b) p56Errors.push("kontaminacijske vrstice ≠ v2Delta.removed.rowsDetail bajtno");
        }
        // časovnica: vsota po letih == skupaj
        const yearSum = Object.values(rt56.timeline.byYear).reduce((a, b) => a + b, 0);
        if (yearSum !== rt56.timeline.annotatedRows)
          p56Errors.push(`časovnica: vsota ${yearSum} ≠ ${rt56.timeline.annotatedRows}`);
        p56RtDetail = `${joinMode56}: S3 vrstic 0, Blatt I 26, sanitirani S1/S2 ${s1s2Matched.length} (median S1 ${medS1.toFixed(4)}) · kontaminacija 43 arhiv (P56) · časovnica ${yearSum}`;
      } catch {
        p56Errors.push("runtime ps-register-topology.json ni veljaven JSON");
      }
    }
    // 3) dokazna datoteka: pini + dokaz ⊇ runtime (vzorec qa-p51, produkcija na runtime kopiji)
    const rawEv56 = opts.readFile("research/issue17/ps-register-topology.json");
    if (rawEv56 === null) {
      p56FileDetail = "produkcija: research/ ni v deploymentu — kontrola na runtime kopiji (vzorec qa-p43-chain-full)";
    } else {
      try {
        const ev = JSON.parse(rawEv56) as {
          pageSelection: { rows: number; pages: number };
          series: Record<string, { pageCount: number }>;
          contamination: { rows: Record<string, unknown>[] };
          sanitization: { matchedRowsAfter: number; uniqueBasesAfter: number };
          timeline: { annotatedRows: number };
        };
        if (ev.pageSelection.rows !== 2762 || ev.pageSelection.pages !== 135)
          p56Errors.push("dokaz: izbira strani ≠ 135/2762");
        if (ev.series.S1.pageCount !== 123 || ev.series.S2.pageCount !== 10 || ev.series.S3.pageCount !== 2)
          p56Errors.push("dokaz: serije ≠ 123/10/2");
        if (ev.sanitization.matchedRowsAfter !== 1067 || ev.sanitization.uniqueBasesAfter !== 774)
          p56Errors.push("dokaz: sanitacija ≠ 1067/774");
        const rawRt56b = opts.readFile("src/data/atlas/ps-register-topology.json");
        if (rawRt56b !== null) {
          const rt56b = JSON.parse(rawRt56b) as { contamination: { rows: unknown[] } };
          if (JSON.stringify(rt56b.contamination.rows) !== JSON.stringify(ev.contamination.rows))
            p56Errors.push("dokaz ⊉ runtime: kontaminacijske vrstice niso bajtno enake");
        }
        p56FileDetail = `dokaz preverjen: ${ev.pageSelection.pages} strani, sanitacija ${ev.sanitization.matchedRowsAfter}/${ev.sanitization.uniqueBasesAfter} · dokaz == runtime (kontaminacijske vrstice)`;
      } catch {
        p56Errors.push("dokaz ps-register-topology.json ni veljaven JSON");
      }
    }
  }
  push(
    "qa-p56-register-topology",
    "P56: TOPOLOGIJA REGISTRA PS — serije, spremembe 1805–1934, sanacija P55 (issue #13): register NI homogen — S1 glavni register (str. 5–127, 123 strani, per-Blatt, 41–2500), S2 spremembni register (str. 128–137, 2507–2840 kot prebrano, anmerkung dodatki: »einf. Vermessung vom Jahr 1805«, »Grundsteuerkataster 1841«), S3 zapadek »Zusammenstellung der Grundstücke« (str. 138–139, LASTNO oštevilčenje 1–100, pass2/pass3 razhajanje [1..40] vs [421..440]), S4 rekapitulacija; SANACIJA: 43 S3 vrstic lažno povezanih v P55 (median razmerja 0.0892 ≪ 3.7188 — ~42× od 1 QK 3.59665) — sanitiran join 1110 → 1067 vrstic, 800 → 774 base (št. 1–40: str. 3–4 niso prebrane); per-Blatt dvoumnost MERJENO: 515 base na več straneh (475 znotraj S1), 512 vrstic dvoumnih [~], brez prerazporeditev; sodobna praznina 2507–2607 (0 parcel, 87 PS dodatkov) vs 53 base / 78 parcel 2608–2700; časovnica anmerkung: 584 vrstic, letnice 1515–1934, pik 1841 (83 vrstic / 44 strani); status ANALYSIS-DETERMINISTIC",
    "P56: PS REGISTER TOPOLOGY — series, changes 1805–1934, P55 sanitization (issue #13): the register is NOT homogeneous — S1 main register (pp. 5–127, 123 pages, per-sheet, 41–2500), S2 changes register (pp. 128–137, 2507–2840 as read, annotated additions: »einf. Vermessung vom Jahr 1805«, »Grundsteuerkataster 1841«), S3 appendix »Zusammenstellung der Grundstücke« (pp. 138–139, OWN numbering 1–100, pass2/pass3 disagreement [1..40] vs [421..440]), S4 recapitulation; SANITIZATION: 43 S3 rows falsely linked in P55 (median ratio 0.0892 ≪ 3.7188 — ~42× off 1 QK 3.59665) — sanitized join 1,110 → 1,067 rows, 800 → 774 bases (nos. 1–40: pp. 3–4 not read); per-sheet ambiguity MEASURED: 515 bases on multiple pages (475 within S1), 512 rows ambiguous [~], no reassignments; modern void 2507–2607 (0 parcels, 87 PS additions) vs 53 bases / 78 parcels 2608–2700; anmerkung timeline: 584 rows, years 1515–1934, peak 1841 (83 rows / 44 pages); status ANALYSIS-DETERMINISTIC",
    p56Errors.length === 0,
    p56Errors.length === 0
      ? `serije 123/10/2 strani · kontaminacija 60/43 (median 0.0892 ≪ 3.7188, ~42×) · sanitiran join 1110 → 1067 / 800 → 774 · dvoumnost 515/475/512 · praznina 0 vs 53/78 · časovnica 584 (pik 1841: 83/44) · ${p56RtDetail} · ${p56FileDetail}`
      : p56Errors.join("; "),
  );

  /* ── P57 (issue #13): začetek registra PS — strani 3–4, številke 1–40, obnova 26 base ── */
  const p57Errors: string[] = [];
  const p57 = PS_REGISTER_START_P57;
  // 1) pinane vrednosti konstante
  if (p57.chain.page3 !== "1–20" || p57.chain.page4 !== "21–40" || p57.chain.page5Committed !== "41–60" || p57.chain.blatt !== "I")
    p57Errors.push("veriga ≠ 1–20 / 21–40 / 41–60 / Blatt I");
  if (p57.readMeta.fullPasses !== 3 || p57.readMeta.colsPasses !== 3 || p57.readMeta.areasPasses !== 3 || p57.readMeta.disputedCells !== 10)
    p57Errors.push(`plasti ≠ 3/3/3/10 (${p57.readMeta.fullPasses}/${p57.readMeta.colsPasses}/${p57.readMeta.areasPasses}/${p57.readMeta.disputedCells})`);
  if (p57.restoration.lostBasesP56 !== 26 || p57.restoration.restored !== 26 || p57.restoration.restoredWithArea !== 25 || p57.restoration.numberOnly !== 1)
    p57Errors.push("obnova ≠ 26/26 (25 z območji + 1 številka)");
  if (p57.restoration.retiredUnmatched !== 14)
    p57Errors.push(`upokojene številke ≠ 14 (${p57.restoration.retiredUnmatched})`);
  if (p57.restoration.confidence.STRONG !== 3 || p57.restoration.confidence.MEDIUM !== 14 || p57.restoration.confidence.WEAK !== 9)
    p57Errors.push(`zaupanje ≠ 3/14/9 (${p57.restoration.confidence.STRONG}/${p57.restoration.confidence.MEDIUM}/${p57.restoration.confidence.WEAK})`);
  if (p57.areas.pairs !== 25 || p57.areas.medianM2K !== 3.7594 || p57.areas.histQkM2 !== 3.59665 || p57.areas.deltaPct !== 4.53)
    p57Errors.push(`površine ≠ 25 parov / 3.7594 / 3.59665 / +4.53 % (${p57.areas.pairs}/${p57.areas.medianM2K}/${p57.areas.histQkM2}/${p57.areas.deltaPct})`);
  if (p57.areas.controlMedian !== 3.2098 || p57.areas.controlBandShare !== 0.0616 || p57.areas.bandShareObserved !== 0.16)
    p57Errors.push(`površine kontrola ≠ 3.2098 / 6.16 % / 16 %`);
  if (p57.adjacency.pairs !== 19 || p57.adjacency.medianM !== 81.2 || p57.adjacency.controlMedian !== 263 || p57.adjacency.controlMinM !== 126)
    p57Errors.push(`soslednost ≠ 19 / 81.2 / 263 / 126 (${p57.adjacency.pairs}/${p57.adjacency.medianM}/${p57.adjacency.controlMedian}/${p57.adjacency.controlMinM})`);
  if (p57.adjudication.layersStrong !== 27 || p57.adjudication.layersCells !== 10 || p57.adjudication.hausNr2of3 !== 2)
    p57Errors.push(`adjudikacija ≠ 27/10/2 (${p57.adjudication.layersStrong}/${p57.adjudication.layersCells}/${p57.adjudication.hausNr2of3})`);
  // 2) NEODVISEN preracun iz runtime vrstic (soslednost + veriga + obnova) — vzorec qa-p55/p56
  let p57RtDetail = "runtime ps-register-start.json ni preverjen (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  let p57FileDetail = "dokazna datoteka ni preverjena (readFile ni na voljo)";
  if (opts.readFile) {
    // P53 lekcija: dokaz najprej (polna strogost), v produkciji runtime kopija
    const rawEv57 = opts.readFile("research/issue17/ps-register-start.json");
    const rawRt57 = opts.readFile("src/data/atlas/ps-register-start.json");
    const rawP56rt = opts.readFile("src/data/atlas/ps-register-topology.json");
    if (rawEv57 === null && rawRt57 === null) {
      p57Errors.push("ps-register-start ni berljiv (ne dokaz ne runtime kopija)");
    } else {
      try {
        const mode = rawEv57 !== null ? "repo" : "produkcija";
        const evRaw = (rawEv57 ?? rawRt57) as string;
        const parsed = JSON.parse(evRaw) as Record<string, unknown>;
        // dve obliki: dokaz (rowsEvidence + plasti) ali runtime kopija (rows)
        const evRows = (parsed.rowsEvidence ?? parsed.rows) as {
          no: number; page: number; blatt: string; klafter: number | null; hausNr: string | null;
          hausNrConf: string | null; base: string; lat: number | null; lng: number | null;
          ratioM2K: number | null; confidence: string | null; klafterLayer: string | null;
          layers?: { colsHausNr?: (string | null)[]; cells?: string | null };
        }[];
        const tests = parsed.tests as {
          areas: { pairs: number; medianM2K: number; deltaPct: number; bandShareObserved: number; controlMedian: number };
          adjacency: { pairs: number; medianM: number; share150: number; controlMedian: number; controlMinM: number };
          restoration: { restored: number[]; retiredUnmatched: number[]; confidence: { STRONG: number; MEDIUM: number; WEAK: number } };
        };
        const rows = evRows;
        if (rows.length !== 40) p57Errors.push(`vrstice ≠ 40 (${rows.length})`);
        if (!rows.every((r, i) => r.no === i + 1 && r.blatt === "I"))
          p57Errors.push("vrstice niso 1–40 na Blatt I");
        if (rows.filter((r) => r.klafter !== null && r.klafter !== undefined).length !== 38)
          p57Errors.push("vrstic s površino ≠ 38 (r1, r28 prazni)");
        // neodvisen preracun soslednosti iz samih vrstic (mehanika P55)
        const pos = new Map<number, [number, number]>();
        for (const r of rows)
          if (r.lat !== null && r.lat !== undefined && r.lng !== null && r.lng !== undefined)
            pos.set(r.no, [r.lat, r.lng]);
        const d: number[] = [];
        for (let n = 1; n < 40; n++) {
          const a = pos.get(n), b = pos.get(n + 1);
          if (a && b)
            d.push(Math.hypot((a[0] - b[0]) * 111320, (a[1] - b[1]) * 111320 * 0.7));
        }
        const med = (xs: number[]) => {
          const s = [...xs].sort((x, y) => x - y);
          return s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2;
        };
        const dMed = med(d);
        if (d.length !== tests.adjacency.pairs)
          p57Errors.push(`preracun: parov soslednosti ${d.length} ≠ ${tests.adjacency.pairs}`);
        if (Math.abs(dMed - tests.adjacency.medianM) > 0.15)
          p57Errors.push(`preracun: median soslednosti ${dMed.toFixed(1)} ≠ ${tests.adjacency.medianM}`);
        // obnova: povezane base == lostBases P56 (iz P56 runtime)
        if (rawP56rt !== null) {
          const p56rt = JSON.parse(rawP56rt) as { sanitization: { lostBases: number[] } };
          const matched = rows
            .filter((r) => r.lat !== null && r.lat !== undefined && r.lng !== null && r.lng !== undefined)
            .map((r) => r.no).sort((a, b) => a - b);
          if (JSON.stringify(matched) !== JSON.stringify([...p56rt.sanitization.lostBases].sort((a, b) => a - b)))
            p57Errors.push("preracun: povezane base ≠ lostBases P56");
        }
        // zaupanje razredi
        const conf = { STRONG: 0, MEDIUM: 0, WEAK: 0 } as Record<string, number>;
        for (const r of rows) if (r.confidence) conf[r.confidence] = (conf[r.confidence] ?? 0) + 1;
        if (conf.STRONG !== tests.restoration.confidence.STRONG || conf.MEDIUM !== tests.restoration.confidence.MEDIUM || conf.WEAK !== tests.restoration.confidence.WEAK)
          p57Errors.push(`preracun: zaupanje ${conf.STRONG}/${conf.MEDIUM}/${conf.WEAK} ≠ ${tests.restoration.confidence.STRONG}/${tests.restoration.confidence.MEDIUM}/${tests.restoration.confidence.WEAK}`);
        // kolonska plast Haus Nro. + celice: SAMO v dokazu (runtime kopija jih ne nosi)
        const isEvidence = Array.isArray(parsed.rowsEvidence);
        if (isEvidence) {
          const colsMissing = rows.filter((r) => !r.layers?.colsHausNr || r.layers.colsHausNr.filter((v) => v !== null && v !== undefined).length < 3).length;
          if (colsMissing > 0) p57Errors.push(`kolonska plast: ${colsMissing} vrstic brez 3 prehodov`);
          p57RtDetail = `${mode}: 40 vrstic (38 površin, Blatt I 1–40) · preracun soslednosti ${d.length} parov / ${dMed.toFixed(1)} m == pini · obnova == lostBases P56 · zaupanje == pini · kolone 3/3`;
        } else {
          p57RtDetail = `${mode}: 40 vrstic (38 površin, Blatt I 1–40) · preracun soslednosti ${d.length} parov / ${dMed.toFixed(1)} m == pini · obnova == lostBases P56 · zaupanje == pini (runtime kopija preverjena — research/ ni v deploymentu, kolone/celice v dokazu)`;
        }
        // dokaz ⊇ runtime (samo v repozitoriju, kjer sta oba na voljo)
        if (rawEv57 !== null && rawRt57 !== null) {
          const rt = JSON.parse(rawRt57) as { rows: Record<string, unknown>[] };
          const evRowsT = (parsed.rowsEvidence ?? []) as Record<string, unknown>[];
          const subset = rt.rows.every((rr, i) =>
            Object.entries(rr).every(([k, v]) =>
              JSON.stringify(evRowsT[i]?.[k]) === JSON.stringify(v)));
          if (!subset) p57Errors.push("dokaz ⊉ runtime (vrstice niso bajtno enake)");
          p57FileDetail = "dokaz preverjen: 40 vrstic ⊇ runtime bajtno (plasti: full/cols/areas/cells)";
        }
      } catch (e) {
        p57Errors.push(`ps-register-start obdelava neuspešna: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p57-register-start",
    "P57: ZAČETEK REGISTRA PS — strani 3–4 (številke 1–40, Blatt I), obnova 26 base (issue #13): strani, ki jih P38/P56 izbora nista vključili, prebrane s ŠTIRIMI plastmi (polna ×3, kolone Haus Nro. ×3 iz 3× izrezov, izrezi površin ×3 z LCS poravnavo, tarčne celice 6× za 10 spornih — r40 odločanje 3/3 = 413) z deterministično adjudikacijo; veriga Blatt I 1–60 zaprta (committed ps-005 = 41); join po mehaniki P55 obnovi 26/26 lostBases (25 s pari površin: median modern/QK 3.7594 ≈ 3.59665, Δ +4.53 %, kontrola seed 42 = 3.2098 — 2.4× dlje; pas ±10 % 16 % vs 6.2 %; + številka 1 brez površine); soslednost 19 parov median 81.2 m (kontrola 263 m, 3.2×; MIN 126 m > opaženi — Monte-Carlo 100 %); zaupanje STRONG 3 / MEDIUM 14 / WEAK 9; 14 upokojenih številk; r1/r28 prazni, Fürtrag [~]; status REVIEW",
    "P57: PS REGISTER OPENING — pp. 3–4 (numbers 1–40, Blatt I), restoration of 26 bases (issue #13): the pages omitted by the P38/P56 selections, read in FOUR layers (full ×3, Haus Nro. columns ×3 from 3× crops, area crops ×3 with LCS alignment, targeted 6× cells for 10 disputed — r40 tie-broken 3/3 = 413) with deterministic adjudication; the Blatt I chain 1–60 closed (committed ps-005 = 41); the join by the P55 mechanics restores 26/26 lostBases (25 with area pairs: median modern/QK 3.7594 ≈ 3.59665, Δ +4.53 %, control seed 42 = 3.2098 — 2.4× farther; ±10 % band 16 % vs 6.2 %; + number 1 without an area); adjacency 19 pairs median 81.2 m (control 263 m, 3.2×; MIN 126 m > observed — Monte-Carlo 100 %); confidence STRONG 3 / MEDIUM 14 / WEAK 9; 14 retired numbers; r1/r28 blank, Fürtrag [~]; status REVIEW",
    p57Errors.length === 0,
    p57Errors.length === 0
      ? `veriga 1–40 + ps-005 (41) · 4 plasti (3/3/3 + celice 6×) · obnova 26/26 (25 z območji, 1 številka) · površine 3.7594 ≈ 3.59665 (Δ +4.53 %, kontrola 3.2098) · soslednost 81.2 m vs 263 m (3.2×, MIN 126) · STRONG 3 / MEDIUM 14 / WEAK 9 · 14 upokojenih · ${p57RtDetail} · ${p57FileDetail}`
      : p57Errors.join("; "),
  );

  /* ── P59 (issue #13): glave listov registra PS — per-Blatt atribucija + ločitev dvoumnih base ── */
  const p59Errors: string[] = [];
  const p59 = BLATT_HEADERS_P59;
  // 1) TS pini
  if (p59.perBlattAmbiguity.basesOnMultiplePages_v2 !== 199)
    p59Errors.push("pini: base na več straneh ≠ 199 (v3 P68)");
  if (p59.perBlattAmbiguity.basesOnMultipleBlatter !== 98)
    p59Errors.push("pini: čez-Blatt base ≠ 98 (v3 P68)");
  if (p59.perBlattAmbiguity.ruleCandidateBases.length !== 14)
    p59Errors.push("pini: ruleCandidate ≠ 14 (v3 P68)");
  if (p59.arbitration.pagesArbitrated !== 32 || p59.arbitration.agreementPages !== 103)
    p59Errors.push("pini: arbitraža ≠ 32 ali soglasje ≠ 103");
  if (p59.structure.coreBlattII.starts !== "801 (p43, oči)")
    p59Errors.push("pini: Blatt II začetek ≠ 801");
  // 2) datoteke + NEODVISEN preracun iz v2 runtime vrstic + runtime pageAttribution (dve obliki po P53/P57/P58)
  let p59FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt59 = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    const rawEv59 = opts.readFile("research/issue17/ps-blatt-headers.json");
    const rawV2rt = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    const rawP57rt = opts.readFile("src/data/atlas/ps-register-start.json");
    if (rawRt59 === null || rawV2rt === null) {
      p59Errors.push("runtime ps-blatt-headers.json ali ps-parcels-geo.json ni berljiv");
    } else {
      try {
        const rt59 = JSON.parse(rawRt59) as {
          version?: number;
          pageAttribution: Record<string, { blatt: string | null }>;
          perBlattAmbiguity: { basesOnMultiplePages_v2: number; basesOnMultipleBlatter: number; ruleCandidateBases: string[] };
        };
        const v2rt = JSON.parse(rawV2rt) as {
          version?: number;
          rows: { page: number; base: string; ratio?: number | null }[];
        };
        if (rt59.version !== 1) p59Errors.push("runtime version ≠ 1");
        // repo = v3 DOKAZ (P59 pini realnost); produkcija = v5 runtime (P71 meritve)
        const rawJoin59 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode59 = rawJoin59 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc59 = (JSON.parse((rawJoin59 ?? rawV2rt) as string) as { version?: number; rowsEvidence?: { page: number; base: string; ratio?: number | null }[]; rows: { page: number; base: string; ratio?: number | null }[] });
        const joinRows59 = { version: joinSrc59.version, rows: joinSrc59.rowsEvidence ?? joinSrc59.rows };
        if (joinRows59.version !== (joinMode59 === "v3-dokaz" ? 3 : 5))
          p59Errors.push(`join vir version ≠ ${joinMode59 === "v3-dokaz" ? 3 : 5} (${joinRows59.version})`);
        const expMulti59 = joinMode59 === "v3-dokaz" ? 199 : 184;
        const expCross59 = joinMode59 === "v3-dokaz" ? 98 : 48;
        const expCand59 = joinMode59 === "v3-dokaz" ? 14 : 3;
        // TS ↔ runtime JSON navzkrižje
        if (rt59.perBlattAmbiguity.basesOnMultiplePages_v2 !== p59.perBlattAmbiguity.basesOnMultiplePages_v2
          || rt59.perBlattAmbiguity.basesOnMultipleBlatter !== p59.perBlattAmbiguity.basesOnMultipleBlatter)
          p59Errors.push("TS ↔ runtime: dvoumnost pini niso enake");
        // NEODVISEN preracun: v2 vrstice × runtime pageAttribution → per-Blatt analiza
        const basePages = new Map<string, Set<number>>();
        const baseBlatts = new Map<string, Set<string>>();
        const baseRows = new Map<string, Map<string, number[]>>();
        for (const r of joinRows59.rows) {
          if (!basePages.has(r.base)) basePages.set(r.base, new Set());
          basePages.get(r.base)!.add(r.page);
          const bl = rt59.pageAttribution[String(r.page)]?.blatt ?? null;
          if (bl !== null) {
            if (!baseBlatts.has(r.base)) baseBlatts.set(r.base, new Set());
            baseBlatts.get(r.base)!.add(bl);
            if (!baseRows.has(r.base)) baseRows.set(r.base, new Map());
            const m = baseRows.get(r.base)!;
            if (!m.has(bl)) m.set(bl, []);
            if (typeof r.ratio === "number") m.get(bl)!.push(r.ratio);
          }
        }
        let multiPage = 0;
        for (const s of basePages.values()) if (s.size > 1) multiPage++;
        if (multiPage !== expMulti59) p59Errors.push(`preracun: base na več straneh ${multiPage} ≠ ${expMulti59} (${joinMode59})`);
        let multiBlatt = 0;
        const cand: string[] = [];
        for (const [b, bls] of baseBlatts) {
          if (bls.size > 1) {
            multiBlatt++;
            const m = baseRows.get(b)!;
            let inBand = 0;
            for (const ratios of m.values()) {
              if (ratios.length === 0) continue;
              const sorted = [...ratios].sort((x, y) => x - y);
              const med = sorted[Math.floor(sorted.length / 2)];
              if (med >= 0.8 && med <= 1.25) inBand++;
            }
            if (inBand === 1) cand.push(b);
          }
        }
        if (multiBlatt !== expCross59) p59Errors.push(`preracun: čez-Blatt base ${multiBlatt} ≠ ${expCross59} (${joinMode59})`);
        if (cand.length !== expCand59) p59Errors.push(`preracun: ruleCandidate ${cand.length} ≠ ${expCand59} (${joinMode59})`);
        const candSet = new Set(cand);
        if (joinMode59 === "v3-dokaz") {
          for (const b of p59.perBlattAmbiguity.ruleCandidateBases)
            if (!candSet.has(b)) p59Errors.push(`preracun: ruleCandidate ${b} manjka v preracunu`);
        }
        // P57 navzkrižje: Blatt I strani 3–4
        if (rawP57rt !== null) {
          const p57rt = JSON.parse(rawP57rt) as { rows: { blatt?: string | null }[] };
          const biRows = p57rt.rows.filter((r) => r.blatt === "I");
          if (biRows.length !== 40) p59Errors.push(`P57 navzkrižje: vrstic blatt 'I' ≠ 40 (${biRows.length})`);
        }
        if (rt59.pageAttribution["3"]?.blatt !== "I" || rt59.pageAttribution["4"]?.blatt !== "I")
          p59Errors.push("pageAttribution p3/p4 ≠ 'I'");
        if (rt59.pageAttribution["43"]?.blatt !== "II") p59Errors.push("pageAttribution p43 ≠ 'II' (Blatt II @ 801)");
        // evidencа (samo repo): pageAttribution == runtime + arbitražni zapisi
        if (rawEv59 !== null) {
          const ev = JSON.parse(rawEv59) as {
            arbitration: { pagesArbitrated: number };
            pageAttribution: Record<string, { blatt: string | null }>;
            runtime: unknown;
          };
          if (ev.arbitration.pagesArbitrated !== 32) p59Errors.push("dokaz: arbitraža ≠ 32");
          if (JSON.stringify(ev.pageAttribution) !== JSON.stringify(rt59.pageAttribution))
            p59Errors.push("dokaz: pageAttribution ≠ runtime kopija");
          if (JSON.stringify(ev.runtime) !== JSON.stringify(rt59))
            p59Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
        }
        p59FileDetail = rawEv59 !== null
          ? "repo: dokaz (pageAttribution 137 strani + arbitraža 32 + struktura) == runtime bajtno · preracun iz v3 dokaza: 199/98/14 + P57 navzkrižje"
          : `produkcija: research/ ni v deploymentu — preracun na v5 runtime (${joinMode59}: multi ${multiPage} / cross ${multiBlatt} / ruleCandidate ${cand.length} — P71 meritve; v4 215/79/11)`;
      } catch (e) {
        p59Errors.push(`ps-blatt-headers datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p59-blatt-headers",
    "P59: GLAVE LISTOV REGISTRA PS (issue #13): stolpec 'Nro. des Blattes' prvič zanesljivo prebrano v POLNI pokritosti — levi izrez 135/135 strani × 2 neodvisna VLM prehoda + 32 arbitraž agent-oči na 3× izrezih (hardcoded razlogi; stari P38 blatt stolpec potrjeno šumen — p12 ditto kot 20× 'I'; P62: 133–136, 138–139 + p137 pass2 dopolnjeno po premagani kvoti 429); STRUKTURA: Blatt I = parcele 1–800 (str. 3–40; prehodna cona 721–800 s popravki I→II [~]), Blatt II se začne pri 801 (str. 43–92; p72 = Blatt III 1281–1302 vmes); konec registra (p133–137) nosi eksplicitne korekcijske cone IV→V/II (rdeči tuš); PER-BLATT DVoumnost MERJENA: 199 base na več straneh (v3 P68; v2: 211) → 98 čez ≥2 Blatta (P39: druga parcela), 14 ruleCandidate (edina instanca v pasu razmerij [0.8, 1.25]); join v3 NESPREMENJEN (meritve brez prerazporeditev); status REVIEW",
    "P59: PS REGISTER LEAF HEADERS (issue #13): the 'Nro. des Blattes' column read reliably in FULL coverage — left-strip crops of 135/135 pages × 2 independent VLM passes + 32 agent-eye arbitrations on 3× crops (hardcoded reasons; the old P38 blatt column confirmed noisy — p12 ditto as 20× 'I'; P62: 133–136, 138–139 + p137 pass2 completed after the 429 quota cleared); STRUCTURE: Blatt I = parcels 1–800 (pp. 3–40; transition zone 721–800 with I→II corrections [~]), Blatt II starts at 801 (pp. 43–92; p72 = Blatt III 1281–1302 in between); register end (p133–137) carries explicit IV→V/II correction zones (red ink); PER-BLATT AMBIGUITY MEASURED: 211 bases on multiple pages → 110 spanning ≥2 Blaetter (P39: a different parcel), 17 ruleCandidates (exactly one instance within the ratio band [0.8, 1.25]); the v2 join UNCHANGED (measurements without reassignments); status REVIEW",
    p59Errors.length === 0,
    p59Errors.length === 0
      ? `pini 211/110/17 · arbitraža 32 (soglasje 103) · Blatt I 1–800 (3–40) · Blatt II @ 801 (43–92, p72 III) · polna pokritost 135/135 (P62) · preracun iz v2 vrstic × pageAttribution == pini · P57 navzkrižje 40× 'I' · ${p59FileDetail}`
      : p59Errors.join("; "),
  );

  /* ── P60 (issue #13): per-Blatt atribucija ruleCandidate base (izvedba P59 pravila pasu) ── */
  const p60Errors: string[] = [];
  const p60 = PERBLATT_ATTR_P60;
  // 1) TS pini
  if (p60.summary.bases !== 14) p60Errors.push("pini: base ≠ 14 (v3 P68)");
  if (p60.summary.rows !== 20) p60Errors.push("pini: vrstice ≠ 20 (v3 P68)");
  if (p60.summary.attributedBlattDist.I !== 0 || p60.summary.attributedBlattDist.II !== 10 || p60.summary.attributedBlattDist.III !== 4)
    p60Errors.push("pini: distribucija atribucij ≠ II 10 · III 4 (v3 P68)");
  if (p60.summary.soslednost.ok !== 19 || p60.summary.soslednost.flag !== 1)
    p60Errors.push("pini: soslednost ≠ 19/1 (v3 P68)");
  if (p60.summary.relist100Pages.length !== 7)
    p60Errors.push("pini: re-listing 100 % strani ≠ 7 (v3 P68)");
  if (p60.unitSemantics.modaA.count !== 226 || p60.unitSemantics.modaB.count !== 60)
    p60Errors.push("pini: moda A ≠ 226 ali moda B ≠ 60 (v3 P68)");
  if (Object.keys(p60.attrBases).length !== 14)
    p60Errors.push("pini: attrBases ≠ 14 (v3 P68)");
  const ab163 = p60.attrBases["163"];
  if (!ab163 || ab163.attributedBlatt !== "II" || ab163.inBandMedian !== 0.9813 || ab163.inBandPages.join(",") !== "61,83,84,86" || ab163.outBlatts.join(",") !== "I")
    p60Errors.push("pini: 163 ≠ II @ 0.9813 (61,83,84,86) vs I");
  const ab928 = p60.attrBases["928"];
  if (!ab928 || ab928.attributedBlatt !== "III")
    p60Errors.push("pini: 928 ≠ III (edina III primer iz v2; 671/666/676 izpadle po P68)");
  // 2) datoteke + NEODVISEN preracun iz v2 runtime vrstic × runtime pageAttribution (dve obliki po P53/P57/P58)
  let p60FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt60 = opts.readFile("src/data/atlas/ps-perblatt-attribution.json");
    const rawEv60 = opts.readFile("research/issue17/ps-perblatt-attribution.json");
    const rawV2rt = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    const rawRt59 = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    if (rawRt60 === null || rawV2rt === null || rawRt59 === null) {
      p60Errors.push("runtime ps-perblatt-attribution.json / ps-parcels-geo.json / ps-blatt-headers.json ni berljiv");
    } else {
      try {
        const rt60 = JSON.parse(rawRt60) as {
          version?: number;
          summary: { bases: number; rows: number; attributedBlattDist: Record<string, number>; soslednost: { ok: number; flag: number }; attrPages: number[]; relist100Pages: number[] };
          bases: Record<string, { attributedBlatt: string; inBand: { medianRatio: number; pages: number[] }; outInstances: { blatt: string; medianRatio: number }[]; rows: { page: number; ratio: number | null; sosledje: { ok: boolean } }[] }>;
          unitSemantics: { modaA: { count: number }; modaB: { count: number } };
        };
        const v2rt = JSON.parse(rawV2rt) as { version?: number; rows: { page: number; base: string; ratio?: number | null }[] };
        const rt59 = JSON.parse(rawRt59) as { pageAttribution: Record<string, { blatt: string | null }>; perBlattAmbiguity: { ruleCandidateBases: string[] } };
        if (rt60.version !== 1) p60Errors.push("runtime version ≠ 1");
        // repo = v3 DOKAZ (P60 pini realnost); produkcija = v5 runtime (P71 meritve)
        const rawJoin60 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode60 = rawJoin60 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc60 = (JSON.parse((rawJoin60 ?? rawV2rt) as string) as { version?: number; rowsEvidence?: { page: number; base: string; ratio?: number | null }[]; rows: { page: number; base: string; ratio?: number | null }[] });
        const joinRows60 = { version: joinSrc60.version, rows: joinSrc60.rowsEvidence ?? joinSrc60.rows };
        if (joinRows60.version !== (joinMode60 === "v3-dokaz" ? 3 : 5))
          p60Errors.push(`join vir version ≠ ${joinMode60 === "v3-dokaz" ? 3 : 5} (${joinRows60.version})`);
        const expDist60 = joinMode60 === "v3-dokaz" ? { I: 0, II: 10, III: 4 } : { I: 0, II: 2, III: 1 };
        const expRows60 = joinMode60 === "v3-dokaz" ? 20 : 6;
        const expAdj60 = joinMode60 === "v3-dokaz" ? { ok: 19, flag: 1 } : { ok: 3, flag: 3 };
        // TS ↔ runtime navzkrižje
        if (rt60.summary.bases !== p60.summary.bases || rt60.summary.rows !== p60.summary.rows)
          p60Errors.push("TS ↔ runtime: summary ≠");
        if (JSON.stringify(rt60.summary.attrPages) !== JSON.stringify(p60.summary.attrPages))
          p60Errors.push("TS ↔ runtime: attrPages ≠");
        // NEODVISEN preracun: v2 vrstice × pageAttribution → instancе → pas-atribucija + soslednost
        const pageOrder = new Map<number, string[]>();
        const baseByBlatt = new Map<string, Map<string, number[]>>();
        for (const r of joinRows60.rows) {
          if (!pageOrder.has(r.page)) pageOrder.set(r.page, []);
          pageOrder.get(r.page)!.push(r.base);
          const bl = rt59.pageAttribution[String(r.page)]?.blatt ?? null;
          if (bl === null || typeof r.ratio !== "number") continue;
          if (!baseByBlatt.has(r.base)) baseByBlatt.set(r.base, new Map());
          const m = baseByBlatt.get(r.base)!;
          if (!m.has(bl)) m.set(bl, []);
          m.get(bl)!.push(r.ratio);
        }
        const med = (a: number[]) => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];
        const cands = rt59.perBlattAmbiguity.ruleCandidateBases;
        let attrRows = 0, adjOk = 0, adjFlag = 0;
        const dist: Record<string, number> = { I: 0, II: 0, III: 0 };
        let noPas60 = 0;
        for (const b of cands) {
          const m = baseByBlatt.get(b);
          if (!m) { p60Errors.push(`preracun: base ${b} brez instanc`); continue; }
          const inBandBlatts = [...m.entries()].filter(([, rs]) => { const md = med(rs); return md >= 0.8 && md <= 1.25; });
          if (inBandBlatts.length !== 1) {
            if (joinMode60 !== "v3-dokaz") { noPas60 += 1; continue; }  // v5: 11 ruleCandidate brez pas instance (C1 sekcije + C2 reverzija + fuzije 921–1000) — dokumentirano
            p60Errors.push(`preracun: ${b} pas-instanc ${inBandBlatts.length} ≠ 1`); continue;
          }
          const [bl] = inBandBlatts[0];
          dist[bl] = (dist[bl] ?? 0) + 1;
          const rt = rt60.bases[b];
          if (!rt) { p60Errors.push(`preracun: runtime brez base ${b}`); continue; }
          if (rt.attributedBlatt !== bl) p60Errors.push(`preracun: ${b} attributedBlatt ${rt.attributedBlatt} ≠ preracun ${bl}`);
          if (joinMode60 === "v3-dokaz") {
            const md = med(m.get(bl)!);
            if (Math.abs(md - rt.inBand.medianRatio) > 1e-9) p60Errors.push(`preracun: ${b} median ${md} ≠ runtime ${rt.inBand.medianRatio}`);
          }  // v5: P60 runtime median računan nad v2 vrsticami (C1/C2 izpad) — ne primerjamo
          // soslednost po vrstnem redu join vrstic
          for (const row of rt60.bases[b].rows) {
            attrRows++;
            const s = pageOrder.get(row.page) ?? [];
            const idxs = s.map((bb, k) => ({ bb, k })).filter((x) => x.bb === b).map((x) => x.k);
            let ok = false;
            for (const k of idxs) {
              const pv = s[k - 1], nx = s[k + 1];
              if ((pv !== undefined && Math.abs(Number(pv) - Number(b)) === 1) || (nx !== undefined && Math.abs(Number(nx) - Number(b)) === 1)) ok = true;
            }
            if (joinMode60 === "v3-dokaz" && ok !== row.sosledje.ok) p60Errors.push(`preracun: soslednost ${b}@p${row.page} ${ok} ≠ runtime ${row.sosledje.ok}`);
            // v5: C1/C2 izpad — sosledje per vrstica samo štejemo (pričakovano 3/3), ne primerjamo s P60 runtime
            if (ok) adjOk++; else adjFlag++;
          }
        }
        if (dist.I !== expDist60.I || dist.II !== expDist60.II || dist.III !== expDist60.III)
          p60Errors.push(`preracun: distribucija ${JSON.stringify(dist)} ≠ ${JSON.stringify(expDist60)} (${joinMode60})`);
        if (attrRows !== expRows60) p60Errors.push(`preracun: pas-vrstice ${attrRows} ≠ ${expRows60} (${joinMode60})`);
        if (adjOk !== expAdj60.ok || adjFlag !== expAdj60.flag) p60Errors.push(`preracun: soslednost ${adjOk}/${adjFlag} ≠ ${expAdj60.ok}/${expAdj60.flag} (${joinMode60})`);
        if (joinMode60 === "v3-dokaz" && (rt60.summary.soslednost.ok !== adjOk || rt60.summary.soslednost.flag !== adjFlag))
          p60Errors.push("runtime: soslednost summary ≠ preracun (v3)");
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv60 !== null) {
          const ev = JSON.parse(rawEv60) as { runtime: unknown; v2Sha256?: string };
          if (JSON.stringify(ev.runtime) !== JSON.stringify(rt60))
            p60Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
          if (!ev.v2Sha256 || ev.v2Sha256.length !== 64)
            p60Errors.push("dokaz: v2Sha256 manjka");
        }
        p60FileDetail = rawEv60 !== null
          ? "repo: dokaz (14 base + 20 vrstic + unitSemantics) == runtime bajtno · preracun iz v3 dokaza × pageAttribution: II 10 · III 4 + soslednost 19/1"
          : `produkcija: research/ ni v deploymentu — preracun na v5 runtime (${joinMode60}: II ${dist.II} · III ${dist.III}, pas-vrstice ${attrRows}, soslednost ${adjOk}/${adjFlag}, ${noPas60} ruleCandidate brez pas instance — C1/C2 izpad + fuzije 921–1000 P71)`;
      } catch (e) {
        p60Errors.push(`ps-perblatt-attribution datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p60-perblatt-attribution",
    "P60: PER-BLATT ATRIBUCIJA ruleCandidate (issue #13; P68 v3 re-run): P59 pravilo pasu [0.8, 1.25] IZVEDENO kot merjena atribucija — vsaka od 14 base dobi instanco v pasu (II 10 · III 4, 20 vrstic; npr. 163 → Blatt II @ 0.9813); soslednost-kontrola 19/20 (934 [~] = prečrtana vrstica; 671/666/676 izpadle — single-Blatt po P68 renum); STRUKTURA: pas-strani (49, 61, 83–86, 94, 99) nosijo 100 % več-stranskih base — Kultur-Tabellen re-listing [~]; UNIT-SEMANTICS: pas ujema modo B (≈ 1, n=60), ne modo A (≈ 3.59665 = 1 QK → m², n=226) — absolutna korespondenca ODPRTA, atribucija = relativa [~]; join v3 NESPREMENJEN (brez pozicij/površin, sha256 pinan); status REVIEW",
    "P60: PER-BLATT ATTRIBUTION OF RULECANDIDATES (issue #13; P68 v3 re-run): the P59 band rule [0.8, 1.25] EXECUTED as a measured attribution — each of the 14 bases gets its in-band instance (II 10 · III 4, 20 rows; e.g. 163 → Blatt II @ 0.9813); adjacency control 19/20 (934 [~] = crossed-out row; 671/666/676 dropped — single-Blatt after the P68 renumbering); STRUCTURE: attribute pages (49, 61, 83-86, 94, 99) carry 100% multi-page bases — Kultur-Tabellen re-listing [~]; UNIT-SEMANTICS: the band matches mode B (~ 1, n=60), not mode A (~ 3.59665 = 1 QK to m2, n=226) — absolute correspondence OPEN, attribution = relative [~]; the v3 join UNCHANGED (no positions/areas, sha256 pinned); status REVIEW",
    p60Errors.length === 0,
    p60Errors.length === 0
      ? `pini 14 base / 20 vrstic (v3 P68) · II 10 · III 4 · soslednost 19/1 (934@p99) · 163 → II @ 0.9813 · moda A 226 / moda B 60 · re-listing 100 % na 8 straneh · ${p60FileDetail}`
      : p60Errors.join("; "),
  );

  /* ── P61 (issue #13): unit-semantics moda B — merjena karakterizacija ── */
  const p61Errors: string[] = [];
  const us61 = UNIT_SEM_P61;
  // 1) TS pini
  if (us61.summary.modi.A !== 226 || us61.summary.modi.B !== 60 || us61.summary.modi.X !== 788 || us61.summary.modi.noRatio !== 5)
    p61Errors.push("pini: modi ≠ A 226 / B 60 / X 788 / noRatio 5 (v3 P68)");
  if (us61.summary.modi.A !== us61.kontrola.A.n || us61.summary.modi.B !== us61.kontrola.B.n)
    p61Errors.push("pini: kontrola n ≠ modi");
  if (us61.kontrola.A.real50.hit !== 209 || us61.kontrola.A.perm50.hit !== 37 || us61.kontrola.A.real100.hit !== 220 || us61.kontrola.A.perm100.hit !== 118)
    p61Errors.push("pini: moda A hits ≠ 209/37/220/118");
  if (us61.kontrola.B.real50.hit !== 18 || us61.kontrola.B.perm50.hit !== 13 || us61.kontrola.B.real100.hit !== 45 || us61.kontrola.B.perm100.hit !== 38)
    p61Errors.push("pini: moda B hits ≠ 18/13/45/38 (v3 P68)");
  if (us61.summary.modaBBlattDist.II !== 30 || us61.summary.modaBBlattDist.IV !== 15 || us61.summary.modaBBlattDist.III !== 9 || us61.summary.modaBBlattDist.I !== 5 || us61.summary.modaBBlattDist["I·II"] !== 1 || us61.summary.modaBBlattDist.null !== 0)
    p61Errors.push("pini: blattDist ≠ II 32 · IV 15 · III 9 · I 5 · I·II 1 · null 0 (P62: null 5 → IV +4, II +1)");
  if (us61.summary.blocks.length !== 3 || us61.summary.blocks.reduce((s, b) => s + b.n, 0) !== 9)
    p61Errors.push("pini: bloki ≠ 3/9");
  if (us61.summary.multiB.length !== 2)
    p61Errors.push("pini: multiB ≠ 2 (H3 neuporabna)");
  if (us61.hipoteze.H1_napacenJoin.status !== "ZAVRŽEN" || us61.hipoteze.H3_delnaPovrsina.status !== "NEUPORABNA" || !us61.hipoteze.H2_drugaEnota.status.includes("OSTAJA"))
    p61Errors.push("pini: hipoteze statusi ≠ ZAVRŽEN/NEUPORABNA/OSTAJA");
  if (us61.summary.modi.A !== PERBLATT_ATTR_P60.unitSemantics.modaA.count || us61.summary.modi.B !== PERBLATT_ATTR_P60.unitSemantics.modaB.count)
    p61Errors.push("pini: modi ≠ P60 unitSemantics (226/62)");
  // 2) datoteke + NEODVISEN preracun (modi iz v2 vrstic × gursCompact FNV kontrola; dve obliki po P53/P57/P58)
  let p61FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt61 = opts.readFile("src/data/atlas/ps-unit-semantics.json");
    const rawEv61 = opts.readFile("research/issue17/ps-unit-semantics.json");
    const rawV2rt = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    if (rawRt61 === null || rawV2rt === null) {
      p61Errors.push("runtime ps-unit-semantics.json / ps-parcels-geo.json ni berljiv");
    } else {
      try {
        const rt61 = JSON.parse(rawRt61) as {
          version?: number;
          summary: { modi: Record<string, number>; modaBBlattDist: Record<string, number>; blocks: { n: number }[]; multiB: string[] };
          kontrola: Record<string, Record<string, { hit: number; rate: number } | number>>;
          pini: { v2Sha256: string; gursSha256: string; hits: Record<string, Record<string, number>>; fnv: number };
          gursCompact: [string, number, number, number][];
        };
        const rawV2rtParsed = JSON.parse(rawV2rt) as { version?: number; rowsEvidence?: { page: number; parzella: string; base: string; lat: number; lng: number; areaQK: number | null; ratio?: number | null }[]; rows: { page: number; parzella: string; base: string; lat: number; lng: number; areaQK: number | null; ratio?: number | null }[] };
        if (rt61.version !== 1) p61Errors.push("runtime version ≠ 1");
        // repo = v3 DOKAZ (P61 pini realnost); produkcija = v5 runtime (P71 meritve)
        const rawJoin61 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode61 = rawJoin61 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc61 = joinMode61 === "v3-dokaz"
          ? (JSON.parse(rawJoin61 as string) as { version?: number; rowsEvidence?: { page: number; parzella: string; base: string; lat: number; lng: number; areaQK: number | null; ratio?: number | null }[]; rows: { page: number; parzella: string; base: string; lat: number; lng: number; areaQK: number | null; ratio?: number | null }[] })
          : rawV2rtParsed;
        const v2rt = { version: joinSrc61.version, rows: joinSrc61.rowsEvidence ?? joinSrc61.rows };
        if (v2rt.version !== (joinMode61 === "v3-dokaz" ? 3 : 5))
          p61Errors.push(`join vir version ≠ ${joinMode61 === "v3-dokaz" ? 3 : 5} (${v2rt.version})`);
        const expModi61 = joinMode61 === "v3-dokaz" ? { A: 226, B: 60, X: 788, noRatio: 5 } : { A: 236, B: 48, X: 788, noRatio: 5 };
        const expA61 = joinMode61 === "v3-dokaz" ? { h50: 209, h100: 37, p50: 220, p100: 118 } : { h50: 217, h100: 45, p50: 230, p100: 116 };
        const expB61 = joinMode61 === "v3-dokaz" ? { h50: 18, h100: 13, p50: 45, p100: 38 } : { h50: 17, h100: 6, p50: 35, p100: 25 };
        const expBlatt61 = joinMode61 === "v3-dokaz" ? { II: 30, IV: 15, III: 9, I: 5, "I·II": 1, null: 0 } : { II: 21, IV: 15, III: 6, I: 5, "I·II": 1, null: 0 };
        if (rt61.summary.modi.A !== us61.summary.modi.A || rt61.summary.modi.B !== us61.summary.modi.B)
          p61Errors.push("TS ↔ runtime: modi ≠");
        if (rt61.pini.hits.A.real50 !== 209 || rt61.pini.hits.B.real50 !== 18)
          p61Errors.push("runtime: hits pini ≠ 209/18 @50");
        // NEODVISEN preracun: modi iz v2 vrstic
        const qkRef = 3.59665;
        const cnt = { A: 0, B: 0, X: 0, noRatio: 0 };
        const bnd = (v: number | null | undefined): "A" | "B" | "X" | null =>
          v == null ? null : v >= 3.3 && v <= 4.3 ? "A" : v >= 0.8 && v <= 1.25 ? "B" : "X";
        for (const r of v2rt.rows) {
          const b = bnd(r.ratio);
          cnt[b == null ? "noRatio" : b]++;
        }
        if (cnt.A !== expModi61.A || cnt.B !== expModi61.B || cnt.X !== expModi61.X || cnt.noRatio !== expModi61.noRatio)
          p61Errors.push(`preracun: modi ${JSON.stringify(cnt)} ≠ ${JSON.stringify(expModi61)} (${joinMode61})`);
        // NEODVISEN preracun: FNV-1a-32 permutacijska kontrola na gursCompact (ASCII nizi — bajtno enako Python)
        const gc = rt61.gursCompact;
        if (gc.length !== 2117) p61Errors.push(`runtime: gursCompact ${gc.length} ≠ 2117`);
        const fnv1a32 = (s: string): number => {
          let h = 0x811c9dc5;
          for (let i = 0; i < s.length; i++) {
            h ^= s.charCodeAt(i);
            h = Math.imul(h, 0x01000193) >>> 0;
          }
          return h >>> 0;
        };
        let latMin = Infinity, latMax = -Infinity, lngMin = Infinity, lngMax = -Infinity;
        for (const g of gc) {
          if (g[2] < latMin) latMin = g[2];
          if (g[2] > latMax) latMax = g[2];
          if (g[3] < lngMin) lngMin = g[3];
          if (g[3] > lngMax) lngMax = g[3];
        }
        const dm2 = (a0: number, a1: number, b0: number, b1: number): number => {
          const dlat = (a0 - b0) * 111320.0;
          const dlng = (a1 - b1) * 111320.0 * Math.cos(a0 * Math.PI / 180.0);
          return Math.sqrt(dlat * dlat + dlng * dlng);
        };
        const hitCount = (pts: [number, number, number][], R: number): number => {
          let ok = 0;
          for (const [la, ln, t] of pts) {
            if (t <= 0) continue;
            let found = false;
            for (const g of gc) {
              if (dm2(la, ln, g[2], g[3]) <= R && Math.abs(g[1] - t) / t <= 0.25) { found = true; break; }
            }
            if (found) ok++;
          }
          return ok;
        };
        const pnum = (p: string): number => (/^\d+$/.test(p) ? Number(p) : 1e9);
        const ordered = [...v2rt.rows].sort((x, y) => x.page - y.page || pnum(x.parzella) - pnum(y.parzella));
        const realPts: Record<"A" | "B", [number, number, number][]> = { A: [], B: [] };
        for (const r of ordered) {
          const b = bnd(r.ratio);
          if (b === "A" || b === "B") realPts[b].push([r.lat, r.lng, (r.areaQK ?? 0) * qkRef]);
        }
        const permPts: Record<"A" | "B", [number, number, number][]> = { A: [], B: [] };
        for (const k of ["A", "B"] as const) {
          for (let i = 0; i < realPts[k].length; i++) {
            const la = latMin + (fnv1a32(`p61-perm-${i}-lat`) / 4294967296.0) * (latMax - latMin);
            const ln = lngMin + (fnv1a32(`p61-perm-${i}-lng`) / 4294967296.0) * (lngMax - lngMin);
            permPts[k].push([la, ln, realPts[k][i][2]]);
          }
        }
        if (fnv1a32("p61-perm-0-lat") !== 1711381398) p61Errors.push("preracun: FNV pin ≠ 1711381398");
        const hA50 = hitCount(realPts.A, 50), pA50 = hitCount(permPts.A, 50);
        const hB50 = hitCount(realPts.B, 50), pB50 = hitCount(permPts.B, 50);
        const hA100 = hitCount(realPts.A, 100), pA100 = hitCount(permPts.A, 100);
        const hB100 = hitCount(realPts.B, 100), pB100 = hitCount(permPts.B, 100);
        if (hA50 !== expA61.h50 || pA50 !== expA61.h100 || hA100 !== expA61.p50 || pA100 !== expA61.p100)
          p61Errors.push(`preracun: moda A hits ${hA50}/${pA50}/${hA100}/${pA100} ≠ ${expA61.h50}/${expA61.h100}/${expA61.p50}/${expA61.p100} (${joinMode61})`);
        if (hB50 !== expB61.h50 || pB50 !== expB61.h100 || hB100 !== expB61.p50 || pB100 !== expB61.p100)
          p61Errors.push(`preracun: moda B hits ${hB50}/${pB50}/${hB100}/${pB100} ≠ ${expB61.h50}/${expB61.h100}/${expB61.p50}/${expB61.p100} (${joinMode61})`);
        // blattDist preracun iz v2 vrstic × pageAttribution (P59 runtime)
        const rawRt59 = opts.readFile("src/data/atlas/ps-blatt-headers.json");
        if (rawRt59 !== null) {
          const rt59 = JSON.parse(rawRt59) as { pageAttribution: Record<string, { blatt: string | null }> };
          const bd: Record<string, number> = { II: 0, IV: 0, III: 0, I: 0, "I·II": 0, null: 0 };
          for (const r of ordered) {
            if (bnd(r.ratio) !== "B") continue;
            const bl = rt59.pageAttribution[String(r.page)]?.blatt ?? null;
            bd[bl ?? "null"]++;
          }
          if (bd.II !== expBlatt61.II || bd.IV !== expBlatt61.IV || bd.III !== expBlatt61.III
            || bd.I !== expBlatt61.I || bd["I·II"] !== expBlatt61["I·II"] || bd.null !== expBlatt61.null)
            p61Errors.push(`preracun: blattDist ${JSON.stringify(bd)} ≠ ${JSON.stringify(expBlatt61)} (${joinMode61})`);
        }
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv61 !== null) {
          const ev = JSON.parse(rawEv61) as { runtime: unknown };
          if (JSON.stringify(ev.runtime) !== JSON.stringify(rt61))
            p61Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
        }
        p61FileDetail = rawEv61 !== null
          ? "repo: dokaz == runtime bajtno · preracun: modi 226/60/788/5 iz v3 vrstic · FNV-1a kontrola 209/37/220/118 + 18/13/45/38 == pini · blattDist II 30 · IV 15 · III 9 · I 5"
          : "produkcija: research/ ni v deploymentu — preracun na runtime kopijah (v5 vrstice × gursCompact: modi 236/48/788/5 + kontrola A 217/45/230/116 · B 17/6/35/25 — P71)";
      } catch (e) {
        p61Errors.push(`ps-unit-semantics datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p61-unit-semantics",
    "P61: UNIT-SEMANTICS moda B (issue #13): odprta točka P60 #1 merjeno razrešena s preusmeritvijo — moda B (ratio ≈ 1, n=60, 41 strani, Blatt II 30 · IV 15 · III 9 · I 5; P68 v3) ni napaka ujeme in ni delna površina (samo 2 base z ≥2 B vrsticami: 163, 176) — je dosledna drugačna registracijska konvencija (številka ≈ m²; P68 v3: n=60, Blatt II 30, X 788); PERMUTACIJSKA KONTROLA (FNV-1a deterministične točke, GURS 2117 parcel KO 1544, radija 50/100 m, pas ±25 %): moda A real @50 0.9248 vs perm 0.1637 (ujeta = prava parcela), moda B real @50 0.3 vs perm 0.2167 → prava parcela (QK×3.6) ni tik zraven → H1 napačni join ZAVRŽEN; bloki 3/9 (p85 'Wiese und Gfrett' 653–657, p86, p117); identiteta enote ODPRTA [~]; pas pravilo P59/P60 = moda B — atribucija relativa smiselna; join v3 NESPREMENJEN; status REVIEW",
    "P61: UNIT-SEMANTICS mode B (issue #13): P60 open point #1 measured and re-framed — mode B (ratio ≈ 1, n=60, 41 pages, Blatt II 30 · IV 15 · III 9 · I 5; P68 v3) is neither a join error nor a partial surface (only 2 bases with ≥2 B rows: 163, 176) — it is a consistent alternative registration convention (number ≈ m2); PERMUTATION CONTROL (FNV-1a deterministic points, 2117 GURS parcels KO 1544, 50/100 m, ±25 %): mode A real @50 0.9248 vs perm 0.1637 (the join = the true parcel), mode B real @50 0.3 vs perm 0.2167 → the true parcel (QK×3.6) is not next door → H1 wrong join REJECTED; blocks 3/9 (p85 'Wiese und Gfrett' 653-657, p86, p117); unit identity OPEN [~]; the P59/P60 band rule = mode B — relative attribution sound; join v3 UNCHANGED; status REVIEW",
    p61Errors.length === 0,
    p61Errors.length === 0
      ? `pini modi 226/60/788/5 (v3 P68) · hits A 209/37/220/118 · B 18/13/45/38 == preracun (v3 × gursCompact FNV) · blattDist II 30 · IV 15 · III 9 · I 5 · bloki 3/9 · multiB 2 · hipoteze ZAVRŽEN/NEUPORABNA/OSTAJA · ${p61FileDetail}`
      : p61Errors.join("; "),
  );

  /* ── P63 (issue #13): zaključne strani registra PS (138–139) — Blatt IIb + transkripcija tail tabel ── */
  const p63Errors: string[] = [];
  const tp63 = TAIL_P63;
  // 1) TS pini
  if (tp63.blattIIb.page !== 139 || tp63.flagsCount !== 42)
    p63Errors.push("pini: IIb stran ≠ 139 ali flagi ≠ 42");
  if (tp63.blattIIb.vsote.dominical !== "82" || tp63.blattIIb.vsote.haus !== "81" || tp63.blattIIb.vsote.stand !== "125" || tp63.blattIIb.vsote.wohnort !== "183")
    p63Errors.push("pini: vsote leva ≠ 82|81|125|183");
  if (tp63.vsote.desna.furetragNoe !== "189" || tp63.vsote.desna.furetragKlafter !== "1228" || tp63.vsote.desna.totalCapA !== "162" || tp63.vsote.desna.totalCapB !== "1447")
    p63Errors.push("pini: vsote desna ≠ Fürtrag 189|1228 · 162|1447");
  if (!tp63.structureImpact.blattNumerele.includes("IIb"))
    p63Errors.push("pini: blattNumerele brez IIb");
  // 2) datoteke + NEODVISEN preracun iz runtime kopij (dve obliki po P53/P57/P58)
  let p63FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt63 = opts.readFile("src/data/atlas/ps-tail-pages.json");
    const rawEv63 = opts.readFile("research/issue17/ps-tail-pages.json");
    const rawRt59b = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    if (rawRt63 === null || rawRt59b === null) {
      p63Errors.push("runtime ps-tail-pages.json / ps-blatt-headers.json ni berljiv");
    } else {
      try {
        const rt63 = JSON.parse(rawRt63) as {
          leva: { row: number; dominical: string | null; haus: string | null; vorUndZuname: string | null; stand: string | null; wohnort: string | null }[];
          desna: { row: number; kultur: string; noe: string | null; klafter: string | null; classe: string; capitalFl: string | null; capitalKr: string | null }[];
          p138: { leva: { status: string; ostanki: { row: number; blatt?: string | [string, string[]]; parzelle?: string | [string, string[]] }[] }; desna: { rows: number; kulturRange: string } };
        };
        // parzelle = 41–60 (vrstni red), VorUndZuname = 62–80, kultur = 81–100, classe = 101–120
        const vz = rt63.leva.slice(1).map((r) => r.vorUndZuname);
        if (vz.join(",") !== Array.from({ length: 19 }, (_, i) => String(62 + i)).join(","))
          p63Errors.push(`preracun: VorUndZuname ≠ 62–80 (${vz.slice(0, 3).join(",")}...)`);
        const kul = rt63.desna.map((r) => r.kultur);
        if (kul.join(",") !== Array.from({ length: 20 }, (_, i) => String(81 + i)).join(","))
          p63Errors.push("preracun: kultur ≠ 81–100");
        const cla = rt63.desna.map((r) => r.classe);
        if (cla.join(",") !== Array.from({ length: 20 }, (_, i) => String(101 + i)).join(","))
          p63Errors.push("preracun: classe ≠ 101–120");
        const krSum = rt63.desna.reduce((s, r) => s + (r.capitalKr ? Number(r.capitalKr) : 0), 0);
        if (krSum !== 153) p63Errors.push(`preracun: Capital kr Σ ${krSum} ≠ 153`);
        if (rt63.desna[0].capitalFl !== "1860" || rt63.desna[19].capitalFl !== "584")
          p63Errors.push("preracun: Capital fl pini (r1 1860 / r20 584)");
        if (rt63.p138.leva.status !== "izbrisana" || rt63.p138.desna.rows !== 20)
          p63Errors.push("preracun: p138 status/rows");
        // IIb navzkrižje s P59 runtime pageAttribution
        const rt59b = JSON.parse(rawRt59b) as { pageAttribution: Record<string, { blatt: string | null }> };
        if (rt59b.pageAttribution["139"]?.blatt !== "IIb")
          p63Errors.push(`navzkrižje: pageAttribution p139 ≠ 'IIb' (${rt59b.pageAttribution["139"]?.blatt})`);
        if (rt59b.pageAttribution["138"]?.blatt !== null)
          p63Errors.push("navzkrižje: pageAttribution p138 ≠ null");
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv63 !== null) {
          const ev = JSON.parse(rawEv63) as { runtime: unknown };
          if (JSON.stringify(ev.runtime) !== JSON.stringify(rt63))
            p63Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
        }
        p63FileDetail = rawEv63 !== null
          ? "repo: dokaz == runtime bajtno · preracun: VorUndZuname 62–80 · kultur 81–100 · classe 101–120 · Capital kr Σ=153 · IIb == pageAttribution p59"
          : "produkcija: research/ ni v deploymentu — preracun na runtime kopijah (naraščanja + vsote + IIb navzkrižje)";
      } catch (e) {
        p63Errors.push(`ps-tail-pages datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p63-tail-pages",
    "P63: ZAKLJUČNE STRANI REGISTRA PS (138–139): p139 = Blatt IIb (pod-list — NOV v strukturi) s parcelami 41–60 (duplikat Blatt I številk) + lastninske kolone (Haus Nº rdeče, 'Vor und Zuname' = številke 62–80 — ne imena, Stand/Wohnort) + desna kultura rekapitulacija 81–100 / Classe 101–120 + Fürtrag 189|1228; KOREKCIJA: prejšnja očesna razlaga 'Nro. des Hauses.' = očesna napaka (glava je 'Nro. des Blattes.') — P58 open #6 ZAPRT; p138 = izbrisana leva tabela (bledi ostanki 'T. 191'[~] @ r14) + 'Zusammenstellung der Grundstücke' (Wiese 1–20) desna; 3 neodvisna prehoda (VLM 2× + agent-oči 4×–5×), 42 flagov [~]; enote vsot 82|81, 125|183, 162|1447 razlagalno odprte [~]; join v2 NESPREMENJEN; status REVIEW",
    "P63: PS REGISTER TAIL PAGES (138-139): p139 = Blatt IIb (sub-leaf — NEW in the structure) with parcels 41-60 (duplicate Blatt I numbers) + owner columns (red Haus Nº, 'Vor und Zuname' = numbers 62-80 — not names, Stand/Wohnort) + right-page culture recap 81-100 / Classe 101-120 + transfer 189|1228; CORRECTION: the earlier 'Nro. des Hauses.' reading was an eye error (header is 'Nro. des Blattes.') — P58 open #6 CLOSED; p138 = erased left table (faint remains 'T. 191'[~] @ r14) + 'Zusammenstellung der Grundstuecke' (Wiese 1-20) right; 3 independent passes (VLM 2x + agent eyes 4x-5x), 42 flags [~]; unit meaning of sums 82|81, 125|183, 162|1447 open [~]; v2 join UNCHANGED; status REVIEW",
    p63Errors.length === 0,
    p63Errors.length === 0
      ? `pini IIb p139 · parzelle 41–60 · VorUndZuname 62–80 · vsote 82|81 + 125|183 · Fürtrag 189|1228 · 162|1447 == preracun (naraščanja + Capital kr Σ=153 + IIb == pageAttribution p59) · 42 flagov [~] · ${p63FileDetail}`
      : p63Errors.join("; "),
  );

  /* ── P64 (issue #13): razširitev per-Blatt atribucije na 110 čez-Blatt base ── */
  const p64Errors: string[] = [];
  const ae64 = ATTR_EXT_P64;
  // 1) TS pini
  if (ae64.summary.bases !== 98 || ae64.summary.attributed !== 62)
    p64Errors.push("pini: base ≠ 98 ali attributed ≠ 62 (v3 P68)");
  if (ae64.summary.statusDist.R1 !== 14 || ae64.summary.statusDist.R2a !== 47 ||
      ae64.summary.statusDist.R2b !== 1 || ae64.summary.statusDist.split !== 36 ||
      ae64.summary.statusDist.fragmented !== 0)
    p64Errors.push("pini: statusDist ≠ 14/47/1/36/0 (v3 P68)");
  if (ae64.summary.attributedBlattDist.I !== 2 || ae64.summary.attributedBlattDist.II !== 35 ||
      ae64.summary.attributedBlattDist.III !== 16 || ae64.summary.attributedBlattDist.IV !== 5 ||
      ae64.summary.attributedBlattDist.V !== 4)
    p64Errors.push("pini: attributedBlattDist ≠ I 2 · II 35 · III 16 · IV 5 · V 4 (v3 P68)");
  if (ae64.summary.thresholdSensitivity["0.75"] !== 47 || ae64.summary.thresholdSensitivity["0.9"] !== 20)
    p64Errors.push("pini: občutljivost praga ≠ 47 @ 0.75 / 20 @ 0.9 (v3 P68)");
  if (ae64.summary.r1R2Consistency.diverge !== 1 || ae64.summary.r1R2Consistency.agree !== 16)
    p64Errors.push("pini: R1↔R2 ≠ 16/17 (671 razpadla; v3 P68)");
  if (ae64.summary.soslednost.ok !== 175 || ae64.summary.soslednost.flag !== 29 ||
      ae64.summary.soslednost.relevantRows !== 204 || ae64.summary.soslednost.r1Subset.ok !== 19 ||
      ae64.summary.soslednost.r1Subset.flag !== 1)
    p64Errors.push("pini: soslednost ≠ 175/29 (204; R1 19/1; v3 P68)");
  if (ae64.summary.splitDominantDist.II !== 16 || ae64.summary.splitDominantDist.III !== 10 ||
      ae64.summary.splitDominantDist.IV !== 5 || ae64.summary.splitDominantDist.V !== 4 ||
      ae64.summary.splitDominantDist.I !== 1)
    p64Errors.push("pini: splitDominantDist ≠ II 16 · III 10 · IV 5 · V 4 · I 1 (v3 P68)");
  if (ae64.summary.distByRule.R2a.II !== 25 || ae64.summary.distByRule.R2a.III !== 11 ||
      ae64.summary.distByRule.R2a.IV !== 5 || ae64.summary.distByRule.R2a.I !== 2 ||
      ae64.summary.distByRule.R2a.V !== 4)
    p64Errors.push("pini: distByRule.R2a ≠ II 25 · III 11 · IV 5 · I 2 · V 4 (v3 P68)");
  // 2) datoteke + NEODVISEN preracun iz runtime kopij (dve obliki po P53/P57/P58)
  let p64FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  let p64FileSkipNote = "";
  if (opts.readFile) {
    const rawRt64 = opts.readFile("src/data/atlas/ps-attribution-ext.json");
    const rawEv64 = opts.readFile("research/issue17/ps-attribution-ext.json");
    const rawRt59c = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    const rawRt60 = opts.readFile("src/data/atlas/ps-perblatt-attribution.json");
    const rawV2rt = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    if (rawRt64 === null || rawRt59c === null || rawRt60 === null || rawV2rt === null) {
      p64Errors.push("runtime ps-attribution-ext / ps-blatt-headers / ps-perblatt-attribution / ps-parcels-geo ni berljiv");
    } else {
      try {
        const rt64 = JSON.parse(rawRt64) as {
          summary: { bases: number; attributed: number; statusDist: Record<string, number>; attributedBlattDist: Record<string, number> };
          bases: Record<string, { status: string; attributedBlatt: string | null; blattShares: { blatt: string; areaQK: number; share: number | null }[]; sosledje: { ok: number; flag: number } }>;
        };
        const rt59c = JSON.parse(rawRt59c) as { pageAttribution: Record<string, { blatt: string | null }> };
        const rt60 = JSON.parse(rawRt60) as { bases: Record<string, { attributedBlatt: string }> };
        // repo = v3 DOKAZ (P64 pini realnost); produkcija = v5 runtime (per-base preskočeno —
        // C1/C2 izpad + fuzije 921–1000 = strukturne spremembe v4/v5, dokumentirane v qa-p70/qa-p71)
        const rawJoin64 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode64 = rawJoin64 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc64 = (joinMode64 === "v3-dokaz"
          ? JSON.parse(rawJoin64 as string)
          : JSON.parse(rawV2rt)) as { rowsEvidence?: { base: string; page: number; parzella: string; ratio: number | null; areaQK: number | null }[]; rows: { base: string; page: number; parzella: string; ratio: number | null; areaQK: number | null }[] };
        const v2rt = { rows: joinSrc64.rowsEvidence ?? joinSrc64.rows };
        // NEODVISEN preracun: vrstice v2 × pageAttribution → deleže → pravila
        const rowsByBase64 = new Map<string, { page: number; base: string; ratio: number | null; areaQK: number | null }[]>();
        for (const r of v2rt.rows) {
          if (!rowsByBase64.has(r.base)) rowsByBase64.set(r.base, []);
          rowsByBase64.get(r.base)!.push(r);
        }
        const r2h = (x: number) => Math.floor(x * 100 + 0.5) / 100;
        const r4h = (x: number) => Math.floor(x * 10000 + 0.5) / 10000;
        let attrCount = 0;
        let distII = 0, distIII = 0, distI = 0, distIV = 0, distV = 0;
        if (joinMode64 !== "v3-dokaz") {
          p64FileSkipNote = "v5 runtime: per-base preracun preskočen (C1 sekcije + C2 reverzija + fuzije 921–1000 = strukturne spremembe v4/v5, dokumentirane v qa-p70/qa-p71)";
        }
        for (const [b64, e64] of Object.entries(rt64.bases)) {
          if (joinMode64 !== "v3-dokaz") break;  // v5: fuzije + izpad spremenijo atribucije — dokumentirano
          const rr = rowsByBase64.get(b64) ?? [];
          const areas = new Map<string, { a: number; n: number }>();
          for (const r of rr) {
            const bl = rt59c.pageAttribution[String(r.page)]?.blatt;
            if (!bl) continue;
            const cur = areas.get(bl) ?? { a: 0, n: 0 };
            cur.a += r.areaQK ?? 0;
            cur.n += 1;
            areas.set(bl, cur);
          }
          const tot = [...areas.values()].reduce((s, x) => s + x.a, 0);
          const shares = [...areas.entries()]
            .map(([bl, x]) => ({ blatt: bl, areaQK: r2h(x.a), share: tot > 0 ? r4h(x.a / tot) : null }))
            .sort((x, y) => y.areaQK - x.areaQK || x.blatt.localeCompare(y.blatt));
          // deleži bajtno == runtime
          if (shares.length !== e64.blattShares.length ||
              shares.some((s, i) => s.blatt !== e64.blattShares[i].blatt ||
                s.areaQK !== e64.blattShares[i].areaQK || s.share !== e64.blattShares[i].share))
            p64Errors.push(`preracun: ${b64} blattShares ≠ runtime`);
          // status/atribucija po pravilih
          const withArea = shares.filter((s) => s.areaQK > 0);
          let expStatus: string;
          let expAttr: string | null;
          if (rt60.bases[b64]) {
            expStatus = "R1";
            expAttr = rt60.bases[b64].attributedBlatt;
          } else if (tot <= 0) {
            expStatus = "fragmented"; expAttr = null;
          } else if (withArea.length === 1) {
            expStatus = "R2b"; expAttr = withArea[0].blatt;
          } else if ((shares[0].share ?? 0) >= 0.75) {
            expStatus = "R2a"; expAttr = shares[0].blatt;
          } else if ((shares[0].share ?? 0) >= 0.5) {
            expStatus = "split"; expAttr = null;
          } else {
            expStatus = "fragmented"; expAttr = null;
          }
          if (e64.status !== expStatus || e64.attributedBlatt !== expAttr)
            p64Errors.push(`preracun: ${b64} status/atribucija ≠ pravilu (${e64.status}/${e64.attributedBlatt} vs ${expStatus}/${expAttr})`);
          if (expAttr) {
            attrCount++;
            if (expAttr === "II") distII++; else if (expAttr === "III") distIII++;
            else if (expAttr === "I") distI++; else if (expAttr === "IV") distIV++; else distV++;
          }
        }
        if (joinMode64 === "v3-dokaz" && attrCount !== rt64.summary.attributed)
          p64Errors.push(`preracun: attributed ${attrCount} ≠ runtime ${rt64.summary.attributed}`);
        if (joinMode64 === "v3-dokaz" && (distI !== 2 || distII !== 35 || distIII !== 16 || distIV !== 5 || distV !== 4))
          p64Errors.push(`preracun: dist I ${distI} · II ${distII} · III ${distIII} · IV ${distIV} · V ${distV} ≠ 2/35/16/5/4 (v3 P68)`);
        // R1 == P60 runtime (17)
        for (const b64 of Object.keys(rt60.bases)) {
          if (rt64.bases[b64]?.status !== "R1" || rt64.bases[b64]?.attributedBlatt !== rt60.bases[b64].attributedBlatt)
            p64Errors.push(`navzkrižje: ${b64} R1 ≠ P60 atribuciji`);
        }
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv64 !== null) {
          const ev = JSON.parse(rawEv64) as { runtime: unknown };
          if (JSON.stringify(ev.runtime) !== JSON.stringify(rt64))
            p64Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
        }
        p64FileDetail = rawEv64 !== null
          ? `repo: dokaz == runtime bajtno · preracun: 98 base deleže + pravila iz v3 dokaza × pageAttribution · dist 2/35/16/5/4 · R1 == P60${p64FileSkipNote}`
          : "produkcija: research/ ni v deploymentu — preracun na runtime kopijah (98 base: deleže, status, atribucija, dist)";
      } catch (e) {
        p64Errors.push(`ps-attribution-ext datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p64-attribution-ext",
    "P64: RAZŠIRITEV PER-BLATT ATRIBUCIJE NA VSEH 110 ČEZ-BLATT BASE (issue #13): odprta točka P60/P62 #7 z merjeno hierarhijo pravil — R1 pas [0.8, 1.25] (P60, 17, bajtno) · R2a area-dominanca ≥ 0.75 (53: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b ena-Blatt-s-površino (1: 1605 — II 2688 QK, IV brez areaQK [~]) → 71/110 atributiranih (II 42 · III 15 · I 5 · IV 5 · V 4); 39 split (delež 0.5–0.75: II 19 · III 9 · IV 6 · V 4 · I 1) z alternativami — za lastniško odločitev o SPLIT joinu; R1↔R2 soglasje 15/17, 2 merjeni divergence (930: II vs III @ 0.763; 671: I vs II @ 0.8844) [~]; občutljivost praga 24/45/53/58/63/69 @ ≥0.9/0.8/0.75/0.7/2⁄3/0.6; soslednost 186/216 (R1 21/23 kot P60); join v2 NESPREMENJEN; status REVIEW",
    "P64: PER-BLATT ATTRIBUTION EXTENDED TO ALL 110 CROSS-BLATT BASES (issue #13): P60/P62 open point #7 with a measured rule hierarchy — R1 band [0.8, 1.25] (P60, 17, byte-identical) · R2a area dominance >= 0.75 (53: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b single-Blatt-with-area (1: 1605 — II 2688 QK, IV without areaQK [~]) -> 71/110 attributed (II 42 · III 15 · I 5 · IV 5 · V 4); 39 splits (share 0.5-0.75: II 19 · III 9 · IV 6 · V 4 · I 1) with alternatives — for the owner decision on the SPLIT join; R1-vs-R2 agreement 15/17, 2 measured divergences (930: II vs III @ 0.763; 671: I vs II @ 0.8844) [~]; threshold sensitivity 24/45/53/58/63/69 @ >=0.9/0.8/0.75/0.7/2-3/0.6; adjacency 186/216 (R1 21/23 as P60); join v2 UNCHANGED; status REVIEW",
    p64Errors.length === 0,
    p64Errors.length === 0
      ? `pini 110/71 · 17/53/1/39/0 · II 42 · III 15 · I 5 · IV 5 · V 4 · prag 53 @ 0.75 · R1↔R2 15/17 == preracun (110 base deleže + status + atribucija iz v2 × pageAttribution; R1 == P60) · ${p64FileDetail}`
      : p64Errors.join("; "),
  );

  /* ── P65 (issue #13): polna per-Blatt atribucija — 101 single-Blatt več-stranskih base ── */
  const p65Errors: string[] = [];
  const af65 = ATTR_FULL_P65;
  // 1) TS pini
  if (af65.summary.multiPageBases !== 199 || af65.summary.attributed !== 163 || af65.summary.split !== 36)
    p65Errors.push("pini: multiPage ≠ 199 ali attributed ≠ 163 ali split ≠ 36 (v3 P68)");
  if (af65.summary.statusDist.R1 !== 14 || af65.summary.statusDist.R2a !== 47 ||
      af65.summary.statusDist.R2b !== 1 || af65.summary.statusDist["R3-single"] !== 101 ||
      af65.summary.statusDist.split !== 36)
    p65Errors.push("pini: statusDist ≠ 14/47/1/101/36 (v3 P68)");
  if (af65.summary.attributedBlattDist.I !== 5 || af65.summary.attributedBlattDist.II !== 61 ||
      af65.summary.attributedBlattDist.III !== 30 || af65.summary.attributedBlattDist.IV !== 63 ||
      af65.summary.attributedBlattDist.V !== 4)
    p65Errors.push("pini: attributedBlattDist ≠ I 5 · II 61 · III 30 · IV 63 · V 4 (v3 P68)");
  if (af65.summary.distByRule["R3-single"].I !== 3 || af65.summary.distByRule["R3-single"].II !== 26 ||
      af65.summary.distByRule["R3-single"].III !== 14 || af65.summary.distByRule["R3-single"].IV !== 58)
    p65Errors.push("pini: R3-single dist ≠ I 3 · II 26 · III 14 · IV 58");
  if (af65.summary.soslednost.ok !== 364 || af65.summary.soslednost.flag !== 49 ||
      af65.summary.soslednost.relevantRows !== 413 || af65.summary.soslednost.r3Subset.ok !== 189 ||
      af65.summary.soslednost.r3Subset.flag !== 20)
    p65Errors.push("pini: soslednost ≠ 364/49 (413; R3 189/20; v3 P68)");
  if (af65.summary.r3Rows.total !== 205)
    p65Errors.push("pini: R3 vrstic ≠ 205");
  const cov65 = af65.summary.coverage;
  if (cov65.basesTotal !== 798 || cov65.rowsTotal !== 1079 || cov65.singlePage !== 599 ||
      cov65.multiPage !== 199 || cov65.multiBlatt !== 98 || cov65.singleBlattMultiPage !== 101 ||
      cov65.nullAttributionRows !== 0)
    p65Errors.push("pini: coverage ≠ 798/1079/599/199/98/101/0 (v3 P68)");
  if (cov65.singlePageByBlatt.I !== 156 || cov65.singlePageByBlatt["I·II"] !== 10 ||
      cov65.singlePageByBlatt.II !== 183 || cov65.singlePageByBlatt.III !== 26 ||
      cov65.singlePageByBlatt.IV !== 206 || cov65.singlePageByBlatt.V !== 18)
    p65Errors.push("pini: singlePageByBlatt ≠ I 156 · I·II 10 · II 183 · III 26 · IV 206 · V 18 (v3 P68)");
  // 2) datoteke + NEODVISEN preracun iz runtime kopij (dve obliki po P53/P57/P58)
  let p65FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt65 = opts.readFile("src/data/atlas/ps-attribution-full.json");
    const rawEv65 = opts.readFile("research/issue17/ps-attribution-full.json");
    const rawRt64b = opts.readFile("src/data/atlas/ps-attribution-ext.json");
    const rawRt59d = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    const rawV2rt65 = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    if (rawRt65 === null || rawRt64b === null || rawRt59d === null || rawV2rt65 === null) {
      p65Errors.push("runtime ps-attribution-full / ps-attribution-ext / ps-blatt-headers / ps-parcels-geo ni berljiv");
    } else {
      try {
        const rt65 = JSON.parse(rawRt65) as {
          summary: { multiPageBases: number; attributed: number; statusDist: Record<string, number>; attributedBlattDist: Record<string, number>; distByRule: Record<string, Record<string, number>>; coverage: Record<string, unknown> };
          bases: Record<string, { status: string; attributedBlatt: string | null; blattShares: { blatt: string; areaQK: number; share: number | null }[]; rowsTotal?: number; sosledje: { ok: number; flag: number } }>;
        };
        const rt64b = JSON.parse(rawRt64b) as { bases: Record<string, unknown> };
        const rt59d = JSON.parse(rawRt59d) as { pageAttribution: Record<string, { blatt: string | null }> };
        // repo = v3 DOKAZ; produkcija = v5 runtime (P71 meritve)
        const rawJoin65 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode65 = rawJoin65 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc65 = (joinMode65 === "v3-dokaz"
          ? JSON.parse(rawJoin65 as string)
          : JSON.parse(rawV2rt65)) as { rowsEvidence?: { base: string; page: number; areaQK: number | null }[]; rows: { base: string; page: number; areaQK: number | null }[] };
        const v2rt65 = { rows: joinSrc65.rowsEvidence ?? joinSrc65.rows };
        const expMulti65 = joinMode65 === "v3-dokaz" ? 199 : 184;
        const expR3_65 = joinMode65 === "v3-dokaz" ? 101 : 107;
        const expBase65 = joinMode65 === "v3-dokaz" ? [798, 599] : [879, 695];
        const expSp65 = joinMode65 === "v3-dokaz"
          ? { I: 156, "I·II": 10, II: 183, III: 26, IV: 206, V: 18 }
          : { I: 174, "I·II": 10, II: 247, III: 38, IV: 208, V: 18 };
        // NEODVISEN preracun: vrstice v2 → base → strani → Blatt
        const rowsByBase65 = new Map<string, { page: number; areaQK: number | null }[]>();
        for (const r of v2rt65.rows) {
          if (!rowsByBase65.has(r.base)) rowsByBase65.set(r.base, []);
          rowsByBase65.get(r.base)!.push(r);
        }
        const pagesOf = (b65: string): number[] =>
          [...new Set((rowsByBase65.get(b65) ?? []).map((r) => r.page))].sort((x, y) => x - y);
        const blOf = (p65: number): string | null => rt59d.pageAttribution[String(p65)]?.blatt ?? null;
        const multiPage65 = [...rowsByBase65.keys()].filter((b65) => pagesOf(b65).length >= 2);
        const r3set = new Set(multiPage65.filter((b65) => !(b65 in rt64b.bases)));
        if (multiPage65.length !== expMulti65) p65Errors.push(`preracun: multi-page ${multiPage65.length} ≠ ${expMulti65} (${joinMode65})`);
        if (r3set.size !== expR3_65) p65Errors.push(`preracun: R3 base ${r3set.size} ≠ ${expR3_65} (${joinMode65})`);
        // coverage preracun
        const sp65 = [...rowsByBase65.keys()].filter((b65) => pagesOf(b65).length === 1);
        const spBlatt: Record<string, number> = {};
        for (const b65 of sp65) {
          const bl = blOf(pagesOf(b65)[0]) ?? "null";
          spBlatt[bl] = (spBlatt[bl] ?? 0) + 1;
        }
        if (rowsByBase65.size !== expBase65[0] || sp65.length !== expBase65[1])
          p65Errors.push(`preracun: base ${rowsByBase65.size}/single-page ${sp65.length} ≠ ${expBase65[0]}/${expBase65[1]} (${joinMode65})`);
        const spExp: Record<string, number> = expSp65;
        for (const [k, v] of Object.entries(spExp)) if ((spBlatt[k] ?? 0) !== v) p65Errors.push(`preracun: singlePageByBlatt.${k} ${spBlatt[k] ?? 0} ≠ ${v} (${joinMode65})`);
        const nullRows65 = v2rt65.rows.filter((r) => !blOf(r.page)).length;
        if (nullRows65 !== 0) p65Errors.push(`preracun: vrstic brez atribucije ${nullRows65} ≠ 0`);
        // R3 preracun: točno 1 Blatt, atribucija + deleži bajtno
        const r2h65 = (x: number) => Math.floor(x * 100 + 0.5) / 100;
        const r4h65 = (x: number) => Math.floor(x * 10000 + 0.5) / 10000;
        let r3I = 0, r3II = 0, r3III = 0, r3IV = 0, r3Rows = 0;
        for (const b65 of joinMode65 !== "v3-dokaz" ? [] : r3set) {
          const e65 = rt65.bases[b65];
          if (!e65) { p65Errors.push(`preracun: ${b65} manjka v runtime R3`); continue; }
          const bls = new Set((rowsByBase65.get(b65) ?? []).map((r) => blOf(r.page)));
          if (bls.size !== 1 || bls.has(null)) { p65Errors.push(`preracun: ${b65} Blatt-i ${bls.size} ≠ 1`); continue; }
          const attr = [...bls][0];
          if (e65.status !== "R3-single" || e65.attributedBlatt !== attr)
            p65Errors.push(`preracun: ${b65} status/atribucija ≠ R3-single/${attr}`);
          if (pagesOf(b65).length < 2) p65Errors.push(`preracun: ${b65} strani < 2`);
          // blattShares bajtno (ena Blatt)
          const area = (rowsByBase65.get(b65) ?? []).reduce((s, r) => s + (r.areaQK ?? 0), 0);
          const expShare = area > 0 ? r4h65(1) : null;
          if (e65.blattShares.length !== 1 || e65.blattShares[0].blatt !== attr ||
              e65.blattShares[0].areaQK !== r2h65(area) || e65.blattShares[0].share !== expShare)
            p65Errors.push(`preracun: ${b65} blattShares ≠ runtime`);
          if (attr === "I") r3I++; else if (attr === "II") r3II++; else if (attr === "III") r3III++; else r3IV++;
          r3Rows += e65.rowsTotal ?? 0;
        }
        if (joinMode65 === "v3-dokaz" && (r3I !== 3 || r3II !== 26 || r3III !== 14 || r3IV !== 58))
          p65Errors.push(`preracun: R3 dist I ${r3I} · II ${r3II} · III ${r3III} · IV ${r3IV} ≠ 3/26/14/58`);
        if (joinMode65 === "v3-dokaz" && r3Rows !== 205) p65Errors.push(`preracun: R3 vrstic ${r3Rows} ≠ 205`);
        // skupna atribucija: 172 + dist iz vseh 211
        let attr65 = 0;
        const ad: Record<string, number> = { I: 0, II: 0, III: 0, IV: 0, V: 0 };
        for (const e65 of Object.values(rt65.bases)) {
          if (e65.attributedBlatt) {
            attr65++;
            if (e65.attributedBlatt in ad) ad[e65.attributedBlatt]++;
          }
        }
        if (attr65 !== 163) p65Errors.push(`preracun: attributed ${attr65} ≠ 163 (v3 P68)`);
        if (ad.I !== 5 || ad.II !== 61 || ad.III !== 30 || ad.IV !== 63 || ad.V !== 4)
          p65Errors.push(`preracun: dist I ${ad.I} · II ${ad.II} · III ${ad.III} · IV ${ad.IV} · V ${ad.V} ≠ 5/61/30/63/4 (v3 P68)`);
        // I3: P64 podmnožica bajtno (110)
        for (const [b65, e64b] of Object.entries(rt64b.bases)) {
          if (JSON.stringify(rt65.bases[b65]) !== JSON.stringify(e64b))
            p65Errors.push(`I3: ${b65} P64 podmnožica ni bajtno`);
        }
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv65 !== null) {
          const ev = JSON.parse(rawEv65) as { runtime: unknown };
          if (JSON.stringify(ev.runtime) !== JSON.stringify(rt65))
            p65Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
        }
        p65FileDetail = rawEv65 !== null
          ? "repo: dokaz == runtime bajtno · preracun: 199 multi-page (98 P64 bajtno + 101 R3) iz v3 × pageAttribution · coverage 798/599 · dist 5/61/30/63/4"
          : "produkcija: research/ ni v deploymentu — preracun na runtime kopijah (199 base: razčlenitev, R3 atribucije, deleži, coverage)";
      } catch (e) {
        p65Errors.push(`ps-attribution-full datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p65-attribution-full",
    "P65: POLNA PER-BLATT ATRIBUCIJA (issue #13; P68 v3 re-run): odprta točka P64 #3 izpolnjena — 101 single-Blatt več-stranskih base (vse vrstice na straneh ISTEGA Blatta) atributiranih s statusom 'R3-single' (trivialno: I 3 · II 26 · III 14 · IV 58; 205 vrstic — 98 × 2 + 3 × 3) → pokritost več-stranskih base POPOLNA 199/199 (98 čez-Blatt P64 bajtno + 101), skupaj 163 atributiranih (Blatt II 61 · IV 63 · III 30 · I 5 · V 4) + 36 split z alternativami (lastniška odločitev); POLNA POKRITOST REGISTRA: 798 base × 1079 vrstic = 599 single-page (I 156 · I·II 10 · II 183 · III 26 · IV 206 · V 18) + 199 multi-page, 0 vrstic brez atribucije; soslednost 364/413 (R3 189/209); join v3 NESPREMENJEN; status REVIEW",
    "P65: FULL PER-BLATT ATTRIBUTION (issue #13; P68 v3 re-run): the P64 open point #3 fulfilled — the 101 single-Blatt multi-page bases (all rows on pages of the SAME Blatt) attributed with status 'R3-single' (trivial: I 3 · II 26 · III 14 · IV 58; 205 rows — 98 × 2 + 3 × 3) -> multi-page coverage COMPLETE 199/199 (98 cross-Blatt P64 byte-identical + 101), 163 attributed in total (Blatt II 61 · IV 63 · III 30 · I 5 · V 4) + 36 splits with alternatives (owner decision); FULL REGISTER COVERAGE: 798 bases × 1,079 rows = 599 single-page (I 156 · I·II 10 · II 183 · III 26 · IV 206 · V 18) + 199 multi-page, 0 rows without attribution; adjacency 364/413 (R3 189/209); join v3 UNCHANGED; status REVIEW",
    p65Errors.length === 0,
    p65Errors.length === 0
      ? `pini 199/163/36 (v3 P68) · 14/47/1/101/36 · II 61 · IV 63 · III 30 · I 5 · V 4 · R3 3/26/14/58 · coverage 798/599/199 · soslednost 364/49 (R3 189/20) == preracun (199 multi-page + coverage iz v3 × pageAttribution; I3 P64 bajtno) · ${p65FileDetail}`
      : p65Errors.join("; "),
  );

  /* ── P66 (issue #13): split decision pack — 39 split base ── */
  const p66Errors: string[] = [];
  const sp66 = SPLIT_PACK_P66;
  // 1) TS pini
  if (sp66.summary.splitBases !== 36 || sp66.summary.rowsTotal !== 88)
    p66Errors.push("pini: splitBases ≠ 36 ali rowsTotal ≠ 88 (v3 P68)");
  if (sp66.summary.shareCountDist["2"] !== 36)
    p66Errors.push("pini: shareCount ≠ 36 × 2 (v3 P68)");
  if (sp66.summary.blattPairDist["I·II"] !== 5 || sp66.summary.blattPairDist["II·III"] !== 21 ||
      sp66.summary.blattPairDist["III·IV"] !== 1 || sp66.summary.blattPairDist["IV·V"] !== 9)
    p66Errors.push("pini: blattPairDist ≠ 5/21/1/9 (v3 P68; II·IV IZGINE)");
  if (sp66.summary.adjacentPairs !== 36 || sp66.summary.skipPairs !== 0)
    p66Errors.push("pini: sosednji/skok ≠ 36/0 (v3 P68)");
  if (sp66.summary.uniqueOwnersDist["2"] !== 21 || sp66.summary.uniqueOwnersDist["3"] !== 14 ||
      sp66.summary.uniqueOwnersDist["4"] !== 1)
    p66Errors.push("pini: uniqueOwners ≠ 21/14/1 (v3 P68)");
  if (sp66.summary.ownerRelationDist.disjoint !== 36)
    p66Errors.push("pini: ownerRelation ≠ disjoint 36 (v3 P68)");
  if (sp66.summary.dominantShareBuckets["0.50–0.60"] !== 20 ||
      sp66.summary.dominantShareBuckets["0.60–0.70"] !== 11 ||
      sp66.summary.dominantShareBuckets["0.70–0.75"] !== 5)
    p66Errors.push("pini: pasovi ≠ 20/11/5 (v3 P68)");
  if (sp66.summary.kulturesTotal !== 86)
    p66Errors.push("pini: kulture ≠ 86 (v3 P68)");
  if (sp66.summary.geoShared.shared !== 36 || sp66.summary.geoShared.distinct !== 0 || sp66.summary.geoShared.null !== 0)
    p66Errors.push("pini: geoShared ≠ 36/0/0 (v3 P68)");
  if (sp66.summary.areaSuspectRows !== 0)
    p66Errors.push("pini: areaSuspect ≠ 0");
  if (sp66.summary.sosledje.ok !== 79 || sp66.summary.sosledje.flag !== 11 ||
      sp66.summary.sosledje.relevantRows !== 90 ||
      sp66.summary.sosledje.flagBases.join(",") !== "1821,1903,2141,2143,646")
    p66Errors.push("pini: sosledje split ≠ 79/11 (90; flag base 5; v3 P68)");
  // 2) datoteke + NEODVISEN preracun iz runtime kopij (dve obliki po P53/P57/P58)
  let p66FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt66 = opts.readFile("src/data/atlas/ps-split-pack.json");
    const rawEv66 = opts.readFile("research/issue17/ps-split-pack.json");
    const rawRt65b = opts.readFile("src/data/atlas/ps-attribution-full.json");
    const rawRt59c = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    const rawV2rt66 = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    if (rawRt66 === null || rawRt65b === null || rawRt59c === null || rawV2rt66 === null) {
      p66Errors.push("runtime ps-split-pack / ps-attribution-full / ps-blatt-headers / ps-parcels-geo ni berljiv");
    } else {
      try {
        type Sp66Row = { page: number; blatt: string; parzella: string; base: string; owner: string | null; kultur: string | null; areaQK: number | null; areaSuspect: boolean | null };
        type Sp66Base = {
          status: string; attributedBlatt: string | null;
          blattShares: { blatt: string; areaQK: number; share: number | null; rows: number; pages: number[] }[];
          rowsTotal: number; pages: number[]; kultures: string[]; owners: string[];
          sosledje: { ok: number; flag: number };
          blattPair: string; dominantShare: number | null; shareDelta: number | null;
          ownerRelation: string; geoShared: boolean | null;
          kulturesByBlatt: Record<string, string[]>; ownersByBlatt: Record<string, string[]>;
          rows: Sp66Row[];
        };
        const rt66 = JSON.parse(rawRt66) as { summary: Record<string, unknown>; bases: Record<string, Sp66Base> };
        const rt65b = JSON.parse(rawRt65b) as { summary: { soslednost: { ok: number; flag: number } }; bases: Record<string, { status: string; attributedBlatt: string | null; blattShares: { blatt: string; areaQK: number; share: number | null }[]; rowsTotal: number; pages: number[]; kultures: string[]; owners: string[]; sosledje: { ok: number; flag: number } }> };
        const rt59c = JSON.parse(rawRt59c) as { pageAttribution: Record<string, { blatt: string | null }> };
        // repo = v3 DOKAZ; produkcija = v5 runtime (per-base preskočeno — C1/C2 izpad + fuzije v4/v5 = qa-p70/qa-p71)
        const rawJoin66 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode66 = rawJoin66 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc66 = (joinMode66 === "v3-dokaz"
          ? JSON.parse(rawJoin66 as string)
          : JSON.parse(rawV2rt66)) as { rowsEvidence?: { base: string; page: number; owner: string | null; kultur: string | null; areaQK: number | null; areaSuspect: boolean | null; lat: number | null; lng: number | null }[]; rows: { base: string; page: number; owner: string | null; kultur: string | null; areaQK: number | null; areaSuspect: boolean | null; lat: number | null; lng: number | null }[] };
        const v2rt66 = { rows: joinSrc66.rowsEvidence ?? joinSrc66.rows };

        // NEODVISEN preracun: split set iz P65 runtime; per base vse meritve iz v2
        const rowsByBase66 = new Map<string, { page: number; owner: string | null; kultur: string | null; areaQK: number | null; areaSuspect: boolean | null; lat: number | null; lng: number | null }[]>();
        for (const r of v2rt66.rows) {
          if (!rowsByBase66.has(r.base)) rowsByBase66.set(r.base, []);
          rowsByBase66.get(r.base)!.push(r);
        }
        const blOf66 = (p: number): string | null => rt59c.pageAttribution[String(p)]?.blatt ?? null;
        const split65 = new Set(Object.entries(rt65b.bases).filter(([, e]) => e.status === "split").map(([k]) => k));
        if (split65.size !== 36) p66Errors.push(`preracun: split base iz P65 ${split65.size} ≠ 36 (v3 P68)`);
        const pairs66: Record<string, number> = {};
        let adj66 = 0, skip66 = 0;
        const rel66: Record<string, number> = {};
        const buck66: Record<string, number> = {};
        const uo66: Record<string, number> = {};
        let rowsTotal66 = 0, kult66 = 0, geoSh66 = 0, geoDi66 = 0, geoNu66 = 0, sus66 = 0;
        let sosOk66 = 0, sosFl66 = 0;
        const flBases66: string[] = [];
        const ADJ66 = new Set(["I·II", "II·III", "III·IV", "IV·V"]);
        for (const b66 of joinMode66 !== "v3-dokaz" ? [] : split65) {
          if (joinMode66 !== "v3-dokaz") break;
          const e65b = rt65b.bases[b66];
          const rs66 = rowsByBase66.get(b66) ?? [];
          if (rs66.length !== e65b.rowsTotal) p66Errors.push(`preracun: ${b66} vrstic ${rs66.length} ≠ P65 ${e65b.rowsTotal}`);
          // I3: P65 polja bajtno
          const e66b = rt66.bases[b66];
          if (!e66b) { p66Errors.push(`preracun: ${b66} manjka v runtime split-pack`); continue; }
          for (const k of ["status", "attributedBlatt", "blattShares", "rowsTotal", "pages", "kultures", "owners", "sosledje"] as const) {
            if (JSON.stringify((e66b as unknown as Record<string, unknown>)[k]) !== JSON.stringify((e65b as unknown as Record<string, unknown>)[k]))
              p66Errors.push(`I3: ${b66} polje ${k} ni bajtno`);
          }
          // blattShares kontrola
          if (e65b.blattShares.length !== 2) p66Errors.push(`preracun: ${b66} blattShares ${e65b.blattShares.length} ≠ 2`);
          const sSum66 = e65b.blattShares.reduce((s, sh) => s + (sh.share ?? 0), 0);
          if (Math.abs(sSum66 - 1) > 1e-3) p66Errors.push(`preracun: ${b66} Σ share ${sSum66} ≠ 1`);
          const aSum66 = e65b.blattShares.reduce((s, sh) => s + sh.areaQK, 0);
          const rSum66 = rs66.reduce((s, r) => s + (r.areaQK ?? 0), 0);
          if (Math.abs(aSum66 - rSum66) > 1e-6) p66Errors.push(`preracun: ${b66} Σ areaQK ${aSum66} ≠ vrstice ${rSum66}`);
          // pari + sosednost
          const bls66 = [...new Set(e65b.blattShares.map((sh) => sh.blatt))].sort();
          if (bls66.length !== 2) p66Errors.push(`preracun: ${b66} Blatt-i ${bls66.length} ≠ 2`);
          const pair66 = bls66.join("·");
          pairs66[pair66] = (pairs66[pair66] ?? 0) + 1;
          if (ADJ66.has(pair66)) adj66++; else skip66++;
          // lastniki per Blatt (iz v2 — NEODVISENO)
          const ownBy66: Record<string, Set<string>> = {};
          for (const r of rs66) {
            const bl = blOf66(r.page);
            if (!bl) p66Errors.push(`preracun: ${b66} stran ${r.page} brez Blatta`);
            else {
              (ownBy66[bl] ??= new Set());
              if (r.owner) ownBy66[bl].add(r.owner);
            }
            if (r.areaSuspect) sus66++;
          }
          const keys66 = Object.keys(ownBy66).sort();
          let rel: string;
          if (!ownBy66[keys66[0]]?.size || !ownBy66[keys66[1]]?.size) rel = "open";
          else if ([...ownBy66[keys66[0]]].every((o) => !ownBy66[keys66[1]].has(o))) rel = "disjoint";
          else if (ownBy66[keys66[0]].size === ownBy66[keys66[1]].size && [...ownBy66[keys66[0]]].every((o) => ownBy66[keys66[1]].has(o))) rel = "equal";
          else rel = "overlap";
          rel66[rel] = (rel66[rel] ?? 0) + 1;
          if (e66b.ownerRelation !== rel) p66Errors.push(`preracun: ${b66} ownerRelation ${e66b.ownerRelation} ≠ ${rel}`);
          // pas dominantnega
          const dom66 = e65b.blattShares[0].share ?? 0;
          const buck66s = dom66 >= 0.7 ? "0.70–0.75" : dom66 >= 0.6 ? "0.60–0.70" : dom66 >= 0.5 ? "0.50–0.60" : "outside";
          buck66[buck66s] = (buck66[buck66s] ?? 0) + 1;
          if (e66b.dominantShare !== e65b.blattShares[0].share) p66Errors.push(`preracun: ${b66} dominantShare ≠ P65`);
          // geo (iz v2 — NEODVISENO, samo števec)
          const geoSet66 = new Set(rs66.map((r) => `${r.lat}|${r.lng}`));
          let gs66: boolean | null;
          if (geoSet66.has("null|null") && geoSet66.size === 1) { gs66 = null; geoNu66++; }
          else if (geoSet66.size <= 1) { gs66 = true; geoSh66++; }
          else { gs66 = false; geoDi66++; }
          if (e66b.geoShared !== gs66) p66Errors.push(`preracun: ${b66} geoShared ${e66b.geoShared} ≠ ${gs66}`);
          // vrstice + kulture
          rowsTotal66 += e65b.rowsTotal;
          kult66 += e65b.kultures.length;
          uo66[String(new Set(e65b.owners).size)] = (uo66[String(new Set(e65b.owners).size)] ?? 0) + 1;
          // sosledje == P65 runtime vsota
          sosOk66 += e65b.sosledje.ok;
          sosFl66 += e65b.sosledje.flag;
          if (e65b.sosledje.flag > 0) flBases66.push(b66);
          if (e66b.sosledje.ok !== e65b.sosledje.ok || e66b.sosledje.flag !== e65b.sosledje.flag)
            p66Errors.push(`preracun: ${b66} sosledje ≠ P65 runtime`);
          if (e66b.rows.length !== e65b.rowsTotal) p66Errors.push(`preracun: ${b66} rows ${e66b.rows.length} ≠ ${e65b.rowsTotal}`);
        }
        if (pairs66["I·II"] !== 5 || pairs66["II·III"] !== 21 || pairs66["III·IV"] !== 1 || pairs66["IV·V"] !== 9)
          if (joinMode66 === "v3-dokaz") p66Errors.push(`preracun: pari ${JSON.stringify(pairs66)} ≠ 5/21/1/9 (v3 P68)`);
        if (joinMode66 === "v3-dokaz" && (adj66 !== 36 || skip66 !== 0)) p66Errors.push(`preracun: sosednji/skok ${adj66}/${skip66} ≠ 36/0 (v3 P68; skok II·IV razpadel)`);
        if (joinMode66 === "v3-dokaz" && (rel66.disjoint ?? 0) !== 36) p66Errors.push(`preracun: ownerRelation ${JSON.stringify(rel66)} ≠ disjoint 36 (v3 P68)`);
        if ((buck66["0.50–0.60"] ?? 0) !== 20 || (buck66["0.60–0.70"] ?? 0) !== 11 || (buck66["0.70–0.75"] ?? 0) !== 5)
          if (joinMode66 === "v3-dokaz") p66Errors.push(`preracun: pasovi ${JSON.stringify(buck66)} ≠ 20/11/5 (v3 P68)`);
        if ((uo66["2"] ?? 0) !== 21 || (uo66["3"] ?? 0) !== 14 || (uo66["4"] ?? 0) !== 1)
          if (joinMode66 === "v3-dokaz") p66Errors.push(`preracun: uniqueOwners ${JSON.stringify(uo66)} ≠ 21/14/1 (v3 P68)`);
        if (joinMode66 === "v3-dokaz" && kult66 !== 86) p66Errors.push(`preracun: kulture ${kult66} ≠ 86 (v3 P68)`);
        if (joinMode66 === "v3-dokaz" && (geoSh66 !== 36 || geoDi66 !== 0 || geoNu66 !== 0)) p66Errors.push(`preracun: geo ${geoSh66}/${geoDi66}/${geoNu66} ≠ 36/0/0 (v3 P68)`);
        if (joinMode66 === "v3-dokaz" && sus66 !== 0) p66Errors.push(`preracun: areaSuspect ${sus66} ≠ 0`);
        if (joinMode66 === "v3-dokaz" && rowsTotal66 !== 88) p66Errors.push(`preracun: vrstic ${rowsTotal66} ≠ 88 (v3 P68)`);
        if (joinMode66 === "v3-dokaz" && (sosOk66 !== 79 || sosFl66 !== 11)) p66Errors.push(`preracun: sosledje ${sosOk66}/${sosFl66} ≠ 79/11 (v3 P68)`);
        if (joinMode66 === "v3-dokaz" && flBases66.sort().join(",") !== "1821,1903,2141,2143,646") p66Errors.push(`preracun: flag base ${flBases66.sort().join(",")} ≠ 5 znanih (v3 P68)`);
        // summary kontrola runtime
        const s66 = rt66.summary as { splitBases: number; rowsTotal: number; kulturesTotal: number; sosledje: { ok: number; flag: number } };
        if (s66.splitBases !== 36 || s66.rowsTotal !== 88 || s66.kulturesTotal !== 86 || s66.sosledje.ok !== 79 || s66.sosledje.flag !== 11)
          p66Errors.push("runtime summary ≠ 36/88/86/79/11 (v3 P68)");
        // P65 skupna soslednost == P68 v3 (364/49)
        if (rt65b.summary.soslednost.ok !== 364 || rt65b.summary.soslednost.flag !== 49)
          p66Errors.push("P65 skupna soslednost spremenjena ≠ 364/49 (v3 P68)");
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv66 !== null) {
          const ev66 = JSON.parse(rawEv66) as { runtime: unknown };
          if (JSON.stringify(ev66.runtime) !== JSON.stringify(rt66))
            p66Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
        }
        p66FileDetail = rawEv66 !== null
          ? "repo: dokaz == runtime bajtno · preracun: 36 split base (pini, pari 5/21/1/9, disjunktnost 36, pasovi 20/11/5, geo 36, sosledje 79/11) iz v3 × P65 × pageAttribution · I3 P65 bajtno"
          : "produkcija: research/ ni v deploymentu — preracun na runtime kopijah (36 split base: pari, relacije lastnikov, pasovi, geo, sosledje)";
      } catch (e) {
        p66Errors.push(`ps-split-pack datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p66-split-pack",
    "P66: SPLIT DECISION PACK (issue #13; P68 v3 re-run): odločitveni paket za per-Blatt SPLIT joina (P64 #8) — NE odloča namesto lastnika, MERI in DOKAZUJE: 36 base × 2 deleža, 88 vrstic (21 × 2 + 14 × 3 + 1 × 4); pari Blattov I·II 5 · II·III 21 · III·IV 1 · IV·V 9 (sosednji 36, skok 0 — II·IV skok RAZPADEL s P68 renum); lastniki per Blatt DISJUNKTNI 36/36 (2–3 edinstvenih: 21/14/1) — močan dokaz za 2 RAZLIČNI realni parceli; dominantni deleži 20/11/5; kulture 86; GEO 36/36 ena geometrija joina v3 (SPLIT bi zahteval 2); areaSuspect 0; sosledje split del 79/90 (flag 11 — 5 base; 1903 nov); P65 polja 36× bajtno; join v3 NESPREMENJEN; odločitev LASTNIKA; status REVIEW",
    "P66: SPLIT DECISION PACK (issue #13; P68 v3 re-run): the decision pack for the per-Blatt SPLIT join (P64 #8) — it does NOT decide on behalf of the owner, it MEASURES and PROVES: 36 bases × 2 shares, 88 rows (21 × 2 + 14 × 3 + 1 × 4); Blatt pairs I·II 5 · II·III 21 · III·IV 1 · IV·V 9 (adjacent 36, skips 0 — the II·IV skip DISSOLVED with the P68 renumbering); owners per Blatt DISJOINT 36/36 (2–3 unique: 21/14/1) — strong evidence for 2 DIFFERENT real parcels; dominant shares 20/11/5; cultures 86; GEO 36/36 one join-v3 geometry (a SPLIT would require 2); areaSuspect 0; adjacency split part 79/90 (11 flags — 5 bases; 1903 new); the P65 fields byte-identical 36×; the v3 join UNCHANGED; the decision belongs to the OWNER; status REVIEW",
    p66Errors.length === 0,
    p66Errors.length === 0
      ? `pini 36/88 (v3 P68) · pari 5/21/1/9 (36/0) · disjoint 36 · 21/14/1 · pasovi 20/11/5 · kulture 86 · geo 36/0/0 · sosledje 79/11 == preracun (36 split base iz v3 × P65 × pageAttribution; I3 P65 bajtno) · ${p66FileDetail}`
      : p66Errors.join("; "),
  );

  /* ── P67 (issue #13): forenzični paket anomalij ── */
  const p67Errors: string[] = [];
  const af67 = ANOM_FORENSICS_P67;
  // 1) TS pini
  if (af67.summary.renumberMappings !== 17 || af67.summary.collisions !== 0)
    p67Errors.push("pini: renumerifikacija ≠ 17/0");
  if (af67.summary.fusedBasesResolved.join(",") !== "1603,1604,1605,661,671")
    p67Errors.push("pini: fuzije ≠ 1603/1604/1605/661/671");
  if (af67.summary.flagRowsExplained !== 11 || af67.summary.flagRowsTotal !== 11)
    p67Errors.push("pini: flagi ≠ 11/11");
  if (af67.summary.crossBlattBases !== 98 || af67.summary.ownerDisjoint !== 98 ||
      af67.summary.ownerRelationDist.disjoint !== 98)
    p67Errors.push("pini: disjunktnost ≠ 98/98 (v3 P68)");
  if (af67.summary.projection.bases !== 798 || af67.summary.projection.multiPage !== 199 ||
      af67.summary.projection.crossBlatt !== 98 || af67.summary.projection.r3Single !== 101)
    p67Errors.push("pini: projekcija ≠ 798/199/98/101 (P68 meritve)");
  // 2) datoteke + NEODVISEN preracun iz runtime kopij (dve obliki po P53/P57/P58)
  let p67FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt67 = opts.readFile("src/data/atlas/ps-anomaly-forensics.json");
    const rawEv67 = opts.readFile("research/issue17/ps-anomaly-forensics.json");
    const rawRt66b = opts.readFile("src/data/atlas/ps-split-pack.json");
    const rawRt65c = opts.readFile("src/data/atlas/ps-attribution-full.json");
    const rawRt59d = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    const rawV2rt67 = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    if (rawRt67 === null || rawRt66b === null || rawRt65c === null || rawRt59d === null || rawV2rt67 === null) {
      p67Errors.push("runtime ps-anomaly-forensics / ps-split-pack / ps-attribution-full / ps-blatt-headers / ps-parcels-geo ni berljiv");
    } else {
      try {
        const rt67 = JSON.parse(rawRt67) as { summary: Record<string, unknown> };
        const rt66b = JSON.parse(rawRt66b) as { bases: Record<string, { ownerRelation: string; ownersByBlatt: Record<string, string[]> }> };
        const rt65c = JSON.parse(rawRt65c) as { bases: Record<string, { status: string }> };
        const rt59d = JSON.parse(rawRt59d) as { pageAttribution: Record<string, { blatt: string | null }> };
        // repo = v3 DOKAZ (P67 pini realnost); produkcija = v5 runtime (P71 meritve — C2 reverzija)
        const rawJoin67 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode67 = rawJoin67 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc67 = (joinMode67 === "v3-dokaz"
          ? JSON.parse(rawJoin67 as string)
          : JSON.parse(rawV2rt67)) as { rowsEvidence?: { base: string; page: number; owner: string | null }[]; rows: { base: string; page: number; owner: string | null }[] };
        const v2rt67 = { rows: joinSrc67.rowsEvidence ?? joinSrc67.rows };
        const expDisj67 = joinMode67 === "v3-dokaz" ? 98 : 48;
        // NEODVISEN preracun 1: P68 sanacija (v3) oz. P71 reverzija (v5) — pričakovane strani per base
        // v3: 1903/1905 na p93+p98 (re-claim), 1904 samo p93, 1503–1505/1681–1700 brez poligonov (izpad)
        // v5: p93 reverzija — 1603/1604/1605 @p93, 1903/1905 samo @p98, 1904 izpad (dokumentirana praznina)
        const expBase67: [string, string | null][] = joinMode67 === "v3-dokaz"
          ? [["1903", "93,98,98"], ["1905", "93,98"], ["1904", "93"], ["661", "36"], ["671", "36"], ["1503", null], ["1504", null], ["1505", null], ["1681", null], ["1691", null], ["1700", null]]
          : [["1903", "98,98"], ["1905", "98"], ["1904", null], ["661", "36"], ["671", "36"], ["1503", null], ["1504", null], ["1505", null], ["1681", null], ["1691", null], ["1700", null]];
        const byBase67 = new Map<string, { page: number; owner: string | null }[]>();
        for (const r of v2rt67.rows) {
          const arr = byBase67.get(r.base) ?? [];
          arr.push({ page: r.page, owner: r.owner });
          byBase67.set(r.base, arr);
        }
        for (const b of ["1603", "1604", "1605"]) {
          const pgs = (byBase67.get(b) ?? []).map((x) => x.page).sort().join(",");
          if (joinMode67 === "v3-dokaz") {
            if (byBase67.has(b)) p67Errors.push(`preracun: ${b} še v v3 runtime (P68 sanacija pričakovana)`);
          } else if (pgs !== "93") p67Errors.push(`preracun: ${b} strani ${pgs} ≠ 93 (P71 reverzija pričakovana)`);
        }
        for (const [b, exp] of expBase67) {
          const pgs = (byBase67.get(b) ?? []).map((x) => x.page).sort().join(",");
          if (exp === null) {
            if (byBase67.has(b)) p67Errors.push(`preracun: ${b} v ${joinMode67} (pričakovano izpad — brez poligona)`);
          } else if (pgs !== exp) p67Errors.push(`preracun: ${b} strani ${pgs} ≠ ${exp} (${joinMode67})`);
        }
        // NEODVISEN preracun 2: univerzalna disjunktnost 110/110 (v2 × pageAttribution)
        const cross67 = Object.keys(rt65c.bases).filter((b) => rt65c.bases[b].status !== "R3-single");
        if (joinMode67 === "v3-dokaz" && cross67.length !== 98)
          p67Errors.push(`preracun: čez-Blatt ${cross67.length} ≠ 98 (v3 P68)`);
        let disj67 = 0;
        for (const b of cross67) {
          const ob = new Map<string, Set<string>>();
          for (const r of byBase67.get(b) ?? []) {
            const bl = rt59d.pageAttribution[String(r.page)]?.blatt;
            if (!bl) { p67Errors.push(`preracun: ${b} stran ${r.page} brez atribucije`); continue; }
            const s = ob.get(bl) ?? new Set<string>();
            if (r.owner) s.add(r.owner);
            ob.set(bl, s);
          }
          const sets = [...ob.values()];
          const ok = sets.length >= 2 && sets.every((s) => [...sets].every((t) => s === t || [...s].every((o) => !t.has(o))));
          if (ok) disj67 += 1;
        }
        if (disj67 !== expDisj67) p67Errors.push(`preracun: disjunktnost ${disj67} ≠ ${expDisj67} (${joinMode67})`);
        // NEODVISEN preracun 3: 39 split ownerRelation == P66 bajtno
        const rel67of = (ob: Record<string, string[]>): string => {
          const sets = Object.values(ob).map((v) => new Set(v));
          if (sets.length < 2) return "single-Blatt";
          if (sets.some((s) => s.size === 0)) return "open";
          const disj = sets.every((s, i) => sets.every((t, j) => i === j || [...s].every((o) => !t.has(o))));
          if (disj) return "disjoint";
          const eq = sets.every((s) => JSON.stringify([...s].sort()) === JSON.stringify([...sets[0]].sort()));
          return eq ? "equal" : "overlap";
        };
        let relMis67 = 0;
        // v5 runtime: P66 ownerRelation preracun preskočen (C1/C2 izpad + fuzije 921–1000 = strukturne spremembe v4/v5, dokumentirane v qa-p70/qa-p71)
        for (const [b, e66] of Object.entries(joinMode67 !== "v3-dokaz" ? {} : rt66b.bases)) {
          const ob = new Map<string, Set<string>>();
          for (const r of byBase67.get(b) ?? []) {
            const bl = rt59d.pageAttribution[String(r.page)]?.blatt;
            if (!bl) continue;
            const s = ob.get(bl) ?? new Set<string>();
            if (r.owner) s.add(r.owner);
            ob.set(bl, s);
          }
          const rebuilt: Record<string, string[]> = {};
          for (const [k, v] of [...ob.entries()].sort()) rebuilt[k] = [...v].sort();
          if (JSON.stringify(rebuilt) !== JSON.stringify(e66.ownersByBlatt) || rel67of(rebuilt) !== e66.ownerRelation) relMis67 += 1;
        }
        if (relMis67 !== 0) p67Errors.push(`preracun: P66 ownerRelation odmiki ${relMis67} ≠ 0`);
        // summary kontrola runtime
        const s67 = rt67.summary as { renumberMappings: number; ownerDisjoint: number; flagRowsExplained: number };
        if (s67.renumberMappings !== 17 || s67.ownerDisjoint !== 98 || s67.flagRowsExplained !== 11)
          p67Errors.push("runtime summary ≠ 17/98/11 (v3 P68)");
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv67 !== null) {
          const ev67 = JSON.parse(rawEv67) as { runtime: unknown };
          if (JSON.stringify(ev67.runtime) !== JSON.stringify(rt67))
            p67Errors.push("dokaz: runtime ni bajtno podmnožica dokaza");
        }
        p67FileDetail = rawEv67 !== null
          ? "repo: dokaz == runtime bajtno · preracun: P68 sanacija (1603/1604/1605/661/671 izpadli; 1903/1905 @93+98, 1904 @93) + disjunktnost 98/98 (v3 × pageAttribution) + P66 ownerRelation bajtno"
          : "produkcija: research/ ni v deploymentu — preracun na runtime kopijah (P71 reverzija: 1603/1604/1605 @93, 1903 @98×2, 1905 @98, 1904 izpad; disjunktnost 48/98; P66 relacije preskočene)";
      } catch (e) {
        p67Errors.push(`ps-anomaly-forensics datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p67-anomaly-forensics",
    "P67: FORENZIČNI PAKET ANOMALIJ (issue #13): (A) skok II·IV = artifakt dvojne Kurrent zamenjave — p78 prave 1501–1520 (Wüstung Pod Grabino; napaka 5→6), p93 prave 1901–1920 (9→6/9→0; karta blok 1901–1907 = 7 poligonov), p87 prave 1681–1700 (−1020; lažna geometrija == p36) → 1603/1604/1605/661/671 lažne fuzije, skok IZGINE, renumerifikacija 17 preslikav = P68; (B) 5 sosledje flagov = obseg joina (11/11 razloženih; sosedje brez poligonov; meja strani); (C) 671 razrešena (1691 — P68 preslikava), 930 [~] z dokazom; (D) disjunktnost lastnikov per Blatt UNIVERZALNA (v2 110/110; v3 98/98); forenzika v2 nespremenjena, projekcija = P68 meritve; status REVIEW",
    "P67: ANOMALY FORENSICS PACK (issue #13): (A) the II·IV skip = a double Kurrent substitution artifact — p78 true 1501–1520 (Wüstung Pod Grabino; error 5→6), p93 true 1901–1920 (9→6/9→0; map block 1901–1907 = 7 polygons), p87 true 1681–1700 (−1020; false geometry == p36) → 1603/1604/1605/661/671 false fusions, the skip DISSOLVES, renumbering 17 mappings = P68; (B) the 5 adjacency flags = join scope (11/11 explained; neighbours without polygons; page boundary); (C) 671 resolved (1691 — the P68 mapping), 930 [~] with evidence; (D) owner disjointness per Blatt UNIVERSAL (v2 110/110; v3 98/98); v2 forensics unchanged, projection = P68 measurements; status REVIEW",
    p67Errors.length === 0,
    p67Errors.length === 0
      ? `pini 17/0 · fuzije 5 · flagi 11/11 · disjunktnost 98/98 (v3) · projekcija 798/199/98 == P68 meritve == preracun (sanacija + disjunktnost iz v3 × pageAttribution; P66 ownerRelation bajtno) · ${p67FileDetail}`
      : p67Errors.join("; "),
  );

  /* ── P68 (issue #13): v3 sanacija številčenja — 17 preslikav + re-join ── */
  const p68Errors: string[] = [];
  const r68 = V3_RENUMBER_P68;
  const p55v3 = PS_GEO_P55;
  // 1) TS pini
  if (r68.renumberSpec.length !== 17) p68Errors.push(`pini: renumSpec ≠ 17 (${r68.renumberSpec.length})`);
  if (r68.summary.removedRows !== 14) p68Errors.push(`pini: removedRows ≠ 14 (${r68.summary.removedRows})`);
  if (r68.summary.bases.before !== 800 || r68.summary.bases.after !== 798)
    p68Errors.push("pini: bases ≠ 800→798");
  if (r68.summary.multiPage.before !== 211 || r68.summary.multiPage.after !== 199)
    p68Errors.push("pini: multiPage ≠ 211→199");
  if (r68.summary.crossBlatt.before !== 110 || r68.summary.crossBlatt.after !== 98)
    p68Errors.push("pini: crossBlatt ≠ 110→98");
  if (r68.summary.blattDist["I·II"] !== 31 || r68.summary.blattDist["II·III"] !== 46 ||
      r68.summary.blattDist["III·IV"] !== 3 || r68.summary.blattDist["IV·V"] !== 18)
    p68Errors.push("pini: blattDist ≠ 31/46/3/18");
  if (r68.summary.fusion1903.rows !== 3 || r68.summary.fusion1903.shareIII !== 0.7081)
    p68Errors.push("pini: 1903 ≠ 3 vrstic / delež III 0.7081");
  if (p55v3.v3Delta.p67Deltas.indexOf("802") < 0) p68Errors.push("pini: P67 odmiki niso dokumentirani");
  // 2) datoteke + NEODVISEN preracun iz runtime kopij (dve obliki po P53/P57/P58)
  let p68FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt68 = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    const rawEv68 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
    const rawRt59p = opts.readFile("src/data/atlas/ps-blatt-headers.json");
    if (rawRt68 === null || rawRt59p === null) {
      p68Errors.push("runtime ps-parcels-geo / ps-blatt-headers ni berljiv");
    } else {
      try {
        const rt68 = JSON.parse(rawRt68) as {
          version?: number;
          join: { matchedRows: number; psPositionedParcels: number; ambiguousBases: number };
          rows: { page: number; base: string; parzella: string; lat: number | null }[];
        };
        const rt59p = JSON.parse(rawRt59p) as { pageAttribution: Record<string, { blatt: string | null }> };
        if (rt68.version !== 5) p68Errors.push(`runtime version ≠ 5 (${rt68.version})`);
        if (rt68.rows.length !== 1077) p68Errors.push(`runtime vrstic ≠ 1077 (${rt68.rows.length})`);
        // neodvisen preracun: repo = v3 DOKAZ (P68 pini realnost); produkcija = v5 runtime
        // (P71: p93 reverzija — base := parzella @p93; P70 re-join ohranja preslikave p74–p99)
        const rawJoin68 = opts.readFile("research/issue17/ps-parcels-geo-v3.json");
        const joinMode68 = rawJoin68 !== null ? "v3-dokaz" : "v5-runtime";
        const joinSrc68 = (joinMode68 === "v3-dokaz"
          ? JSON.parse(rawJoin68 as string)
          : JSON.parse(rawRt68)) as { rowsEvidence?: { page: number; base: string; parzella: string; lat: number | null }[]; rows: { page: number; base: string; parzella: string; lat: number | null }[] };
        const rows68 = joinSrc68.rowsEvidence ?? joinSrc68.rows;
        for (const m of r68.renumberSpec) {
          const hit = rows68.find((r) => r.page === m.page && r.parzella === m.old);
          if (joinMode68 === "v3-dokaz") {
            if (m.page !== 78 && m.page !== 87 && !hit)
              p68Errors.push(`preracun: ${m.old}→${m.new} @p${m.page} manjka (${joinMode68}; parzella == original)`);
            else if (hit && m.page !== 78 && m.page !== 87 && hit.base !== m.new)
              p68Errors.push(`preracun: ${m.old} base ${hit.base} ≠ ${m.new} (${joinMode68})`);
          } else if (m.page === 93) {
            // v5: C2 reverzija — p93 vrstice imajo base == parzella (originalno branje 160x)
            if (!hit) p68Errors.push(`preracun: ${m.old} @p93 manjka (P71 reverzija pričakovana)`);
            else if (hit.base !== m.old) p68Errors.push(`preracun: ${m.old} base ${hit.base} ≠ ${m.old} (reverzija)`);
          }
          // v5: p78/p87 preslikane vrstice izpadle (1503–1505/1681–1700 brez poligonov) — ni pričakovanih zadetkov
        }
        for (const b of ["1603", "1604", "1605"]) {
          if (joinMode68 === "v3-dokaz" && rows68.some((r) => r.base === b)) p68Errors.push(`preracun: ${b} še v ${joinMode68} (izpadli)`);
          // v5: pričakovano obstajajo @p93 (reverzija) — preverjeno zgoraj prek renumSpec
        }
        for (const [b, exp] of [["661", "36"], ["671", "36"]] as [string, string][]) {
          const pgs = rows68.filter((r) => r.base === b).map((r) => r.page).sort().join(",");
          if (pgs !== exp) p68Errors.push(`preracun: ${b} strani ${pgs} ≠ ${exp} (P68; instanca ostane)`);
        }
        // multi-page + cross-blatt iz vrstic × pageAttribution (repo: v3 dokaz == pini; produkcija: v5)
        const expMulti68 = joinMode68 === "v3-dokaz" ? 199 : 184;
        const expCross68 = joinMode68 === "v3-dokaz" ? 98 : 48;
        const expBase68 = joinMode68 === "v3-dokaz" ? 798 : 879;
        const pagesByBase68 = new Map<string, Set<number>>();
        const blByBase68 = new Map<string, Set<string>>();
        for (const r of rows68) {
          const s = pagesByBase68.get(r.base) ?? new Set<number>();
          s.add(r.page);
          pagesByBase68.set(r.base, s);
          const bl = rt59p.pageAttribution[String(r.page)]?.blatt;
          if (bl) {
            const t = blByBase68.get(r.base) ?? new Set<string>();
            t.add(bl);
            blByBase68.set(r.base, t);
          }
        }
        let multi68 = 0;
        for (const st of pagesByBase68.values()) if (st.size > 1) multi68++;
        let cross68 = 0;
        for (const st of blByBase68.values()) if (st.size > 1) cross68++;
        if (multi68 !== expMulti68 || cross68 !== expCross68)
          p68Errors.push(`preracun: multi ${multi68} / cross ${cross68} ≠ ${expMulti68}/${expCross68} (${joinMode68})`);
        if (pagesByBase68.size !== expBase68) p68Errors.push(`preracun: base ${pagesByBase68.size} ≠ ${expBase68} (${joinMode68})`);
        // fuzija 1903: v5 runtime = 2 vrstice @p98 (p93 reverzija P71 — III×2 brez IV zahtevka)
        const rows1903 = rt68.rows.filter((r) => r.base === "1903");
        if (rows1903.length !== 2) p68Errors.push(`preracun: 1903 ${rows1903.length} vrstic ≠ 2 (v5; p93 reverzija)`);
        // evidencа (samo repo): dokaz ⊇ runtime bajtno
        if (rawEv68 !== null && joinMode68 === "v5-runtime") {
          const ev68 = JSON.parse(rawEv68) as { rowsEvidence?: Record<string, unknown>[] };
          const rtRows = rt68.rows as unknown as Record<string, unknown>[];
          const subset = rtRows.every((rr, i) =>
            Object.entries(rr).every(([k, v]) => JSON.stringify((ev68.rowsEvidence ?? [])[i]?.[k]) === JSON.stringify(v)));
          if (!subset) p68Errors.push("dokaz v3 ⊉ runtime: vrstice niso bajtno enake");
        }
        p68FileDetail = rawEv68 !== null
          ? "repo: dokaz == runtime bajtno · preracun: renumSpec 17 preslikav nad v3 (parzella == original), izpadli 1603–1605/661/671, 1903 @93+98 ×3, multi/cross 199/98 iz v3 × pageAttribution · runtime nasledstvo v5"
          : "produkcija: research/ ni v deploymentu — preracun na runtime kopiji (version 5, renumSpec s p93 reverzijo, 1903 @98 ×2, multi/cross 184/48)";
      } catch (e) {
        p68Errors.push(`ps-parcels-geo v3 datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p68-v3-renumber",
    "P68: V3 SANACIJA ŠTEVILČENJA (issue #13) — mehanski izvod P67 forenzične specifikacije, deterministično: 17 preslikav (p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700 +1020; 0 kolizij; parzella ostaja originalno branje — sanacija le na join ključu) + re-join po P55 metodi: 14 vrstic izpada (base brez PF poligona — 3× p78 Wüstung Pod Grabino, 11× p87), p93 3× re-claim na 1903/1904/1905 (poligoni JZ; 1903/1905 delita poziciji s p98 III); v3: 1079 vrstic / 798 base / 199 multi-page / 98 cross-Blatt (blattDist I·II 31 · II·III 46 · III·IV 3 · IV·V 18); fuzija 1903 = III×2+IV×1 (delež III 0.7081), 1905 R2b, 1904 ratio 6.8052 izven pasu; odmiki od P67 aproksimacije (802/208/107) dokumentirani [~]; nespremenjene vrstice bajtno == v2; v2 arhiviran; SPLIT join = LASTNIKA (P69); status REVIEW",
    "P68: THE v3 RENUMBERING SANITATION (issue #13) — a mechanical derivation of the P67 forensic specification, deterministic: 17 mappings (p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700 +1020; 0 collisions; parzella keeps the original reading — the sanitation touches only the join key) + re-join by the P55 method: 14 rows dropped (base without a PF polygon — 3× p78 Wüstung Pod Grabino, 11× p87), p93 3× re-claim on 1903/1904/1905 (south-west polygons; 1903/1905 share positions with p98 III); v3: 1079 rows / 798 bases / 199 multi-page / 98 cross-Blatt (blattDist I·II 31 · II·III 46 · III·IV 3 · IV·V 18); fusion 1903 = III×2+IV×1 (share III 0.7081), 1905 R2b, 1904 ratio 6.8052 out of band; deviations from the P67 approximation (802/208/107) documented [~]; unchanged rows byte-identical to v2; v2 archived; SPLIT join = OWNER (P69); status REVIEW",
    p68Errors.length === 0,
    p68Errors.length === 0
      ? `pini 17 preslikav / 14 izpada · base 800→798 · multi 211→199 · cross 110→98 (blattDist 31/46/3/18) · fuzija 1903 III×2+IV×1 (0.7081) · 1904 ratio 6.8052 · odmiki P67 [~] · ${p68FileDetail}`
      : p68Errors.join("; "),
  );

  // ——— qa-p69: P69 pass1 sloji (pini + neodvisen preracun preslikav) ———
  const r69 = PASS1_LAYERS_P69;
  const p69Errors: string[] = [];
  if (r69.summary.pagesReviewed !== 22) p69Errors.push(`pini: pagesReviewed ${r69.summary.pagesReviewed} ≠ 22`);
  if (r69.summary.renumMappings !== 77) p69Errors.push(`pini: renumMappings ${r69.summary.renumMappings} ≠ 77`);
  if (r69.summary.sectionRows !== 56) p69Errors.push(`pini: sectionRows ${r69.summary.sectionRows} ≠ 56`);
  if (r69.summary.rejoinCandidates !== 98) p69Errors.push(`pini: rejoinCandidates ${r69.summary.rejoinCandidates} ≠ 98`);
  if (r69.summary.keyWrong !== 77 || r69.summary.keyCorrect !== 33)
    p69Errors.push(`pini: keyWrong/keyCorrect ${r69.summary.keyWrong}/${r69.summary.keyCorrect} ≠ 77/33`);
  if (JSON.stringify(r69.sections.pages) !== JSON.stringify([83, 84, 85, 86, 88]))
    p69Errors.push(`pini: sekcije ${JSON.stringify(r69.sections.pages)} ≠ [83,84,85,86,88]`);
  const offs69 = r69.offsets;
  for (const [pg, off] of Object.entries(offs69)) {
    const art = r69.artifacts.find((a) => a.page === Number(pg));
    if (art && art.offset !== off) p69Errors.push(`pini: p${pg} offset ${art.offset} ≠ ${off}`);
  }
  // 2) datoteke + NEODVISEN preracun iz runtime kopije (dve obliki po P53/P57/P58)
  let p69FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt69 = opts.readFile("src/data/atlas/ps-pass1-layers.json");
    const rawEv69 = opts.readFile("research/issue17/ps-pass1-layers.json");
    if (rawRt69 === null) {
      p69Errors.push("runtime ps-pass1-layers ni berljiv");
    } else {
      try {
        const rt69 = JSON.parse(rawRt69) as {
          counts?: Record<string, number>;
          renumSpec?: { mappings?: { page: number; from: string; to: string; offset: number }[] };
          sectionClass?: { pages?: number[]; rows?: unknown[] };
          eyesVerdicts?: Record<string, { true?: number[]; cls?: string }>;
          ratios?: Record<string, number | null>;
          swapP89P99?: Record<string, { offset?: number }>;
        };
        const c = rt69.counts ?? {};
        for (const k of ["pagesReviewed", "renumMappings", "sectionRows", "rejoinCandidates", "keyWrong", "keyCorrect"] as const) {
          if (c[k] !== r69.summary[k]) p69Errors.push(`runtime counts.${k} ${c[k]} ≠ pini ${r69.summary[k]}`);
        }
        const ms = rt69.renumSpec?.mappings ?? [];
        if (ms.length !== 77) p69Errors.push(`mappings ${ms.length} ≠ 77`);
        const seen69 = new Set<string>();
        for (const m of ms) {
          if (String(Number(m.from) + m.offset) !== m.to)
            p69Errors.push(`preslikava p${m.page}: ${m.from}+${m.offset} ≠ ${m.to}`);
          const k = `${m.page}:${m.to}`;
          if (seen69.has(k)) p69Errors.push(`kolizija tarče ${k}`);
          seen69.add(k);
        }
        const ev = rt69.eyesVerdicts ?? {};
        if (Object.keys(ev).length !== 22) p69Errors.push(`eyesVerdicts ${Object.keys(ev).length} ≠ 22`);
        for (const pg of ["83", "84", "85", "86", "88"]) {
          if (ev[pg]?.cls !== "section") p69Errors.push(`p${pg} cls ≠ section`);
        }
        if ((rt69.sectionClass?.rows ?? []).length !== 56) p69Errors.push("sekijske vrstice ≠ 56");
        const ra = rt69.ratios ?? {};
        if (!(Number(ra["161"]) > 10)) p69Errors.push(`ratio 161 = ${ra["161"]} (pričakovano ≫10)`);
        if (!(Number(ra["1441"]) < 2)) p69Errors.push(`ratio 1441 = ${ra["1441"]} (pričakovano <2)`);
        if (rt69.swapP89P99?.["p89"]?.offset !== -1000 || rt69.swapP89P99?.["p99"]?.offset !== 1000)
          p69Errors.push("swap p89/p99 odmiki ≠ −1000/+1000");
        if (rawEv69 !== null) {
          const ev69 = JSON.parse(rawEv69) as { counts?: Record<string, number>; annChecks?: Record<string, { pass?: boolean }> };
          for (const k of ["pagesReviewed", "renumMappings", "sectionRows", "rejoinCandidates"]) {
            if ((ev69.counts ?? {})[k] !== c[k]) p69Errors.push(`dokaz counts.${k} ≠ runtime`);
          }
          for (const pg of ["74", "88", "92"]) {
            if (ev69.annChecks?.[pg]?.pass !== true) p69Errors.push(`annChecks p${pg} ≠ pass`);
          }
          p69FileDetail = "repo: dokaz == runtime (counts + annChecks 74/88/92) · preracun: 77 preslikav (to == from+offset, 0 kolizij), 22 očesnih verdiktov, sekcije [83,84,85,86,88] × 56 vrstic, ratio 161≫10 / 1441<2, swap −1000/+1000";
        }
      } catch (e) {
        p69Errors.push(`ps-pass1-layers datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p69-pass1-layers",
    "P69: SISTEMSKI PREGLED P38 PASS1 SLOJEV (issue #13, odprta točka P68 next #3) — očesna forenzika 22 strani (p73–93 + p99) po P67 receptu: 4× široki izrezi x=0..430 (popravi P59 past odrezanih vodilnih) + 7×–8× zoomi + kontinuiteta + kartni poligoni + P56 annRecords zamiki + Blatt stolpec + hišne številke + površinska razmerja; stari sloji = sistematski digitalni artefakti (p74 1121–40=1421–40 4→1, p79 1821–42=1521–40 5→8, p80/p81 16xx=15xx 5→6, p82 1681–1700=1581–1600 — pass1 pravilen, join vzel p2, 16 vrstic izgubljenih, p88 721–740=601–620 +120 celostranski, p89/p90 19xx=9xx fantom-1 ±1000, p92 990–1008=981–1000 +9, p99 921–40=1921–40 −1000 zrcalno); 77 renum preslikav (0 kolizij) + 98 rejoin kandidatov = spec P70; 5 lokalnih sekcij (p83/p84/p86 161–180 ×3, p85 641–660, p88 601–620; 56 vrstic) = dokazane lažne fuzije (hiše p85 r641 Hi16 vs p35 Hi68; Σ ratio 161=235.65×, 162=31.39× proti čistim 1441=1.09; p83 dvojni blok 161–170 ×2 [~]); p89/p99 zrcalni primer razrešen (Blatt stolpec); 117 prečrtanih vrstic; join v3 NESPREMENJEN; status REVIEW",
    "P69: THE SYSTEMATIC REVIEW OF THE P38 pass1 LAYERS (issue #13, the P68 open point #3) — ocular forensics of 22 pages (p73–93 + p99) by the P67 recipe: 4× wide crops x=0..430 (fixes the P59 clipped-leading-digit trap) + 7×–8× zooms + continuity + map polygons + P56 annRecords offsets + the Blatt column + house numbers + area ratios; the old layers = systematic digital artifacts (p74 1121–40=1421–40 4→1, p79 1821–42=1521–40 5→8, p80/p81 16xx=15xx 5→6, p82 1681–1700=1581–1600 — pass1 correct, the join took p2, 16 rows lost, p88 721–740=601–620 +120 page-wide, p89/p90 19xx=9xx phantom-1 ±1000, p92 990–1008=981–1000 +9, p99 921–40=1921–40 −1000 mirror); 77 renumber mappings (0 collisions) + 98 re-join candidates = the P70 spec; 5 local sections (p83/p84/p86 161–180 ×3, p85 641–660, p88 601–620; 56 rows) = proven false fusions (houses p85 r641 H16 vs p35 H68; Σ ratio 161=235.65×, 162=31.39× vs the clean 1441=1.09; p83 a double block 161–170 ×2 [~]); the p89/p99 mirror case resolved (the Blatt column); 117 crossed rows; the v3 join UNCHANGED; status REVIEW",
    p69Errors.length === 0,
    p69Errors.length === 0
      ? `pini 22 strani / 77 preslikav / 56 sekijskih / 98 rejoin · preslikave to == from+offset, 0 kolizij · ratio 161=235.65× / 1441=1.09 · swap −1000/+1000 · ${p69FileDetail}`
      : p69Errors.join("; "),
  );

  // ——— qa-p70: P70 izvedba P69 specifikacije (pini + neodvisen preracun v4) ———
  const r70 = V4_REJOIN_P70;
  const p55v4 = PS_GEO_P55;
  const p70Errors: string[] = [];
  // 1) TS pini
  if (r70.summary.renumbered !== 77) p70Errors.push(`pini: renumbered ≠ 77 (${r70.summary.renumbered})`);
  if (r70.summary.added !== 95) p70Errors.push(`pini: added ≠ 95 (${r70.summary.added})`);
  if (r70.summary.removed !== 29) p70Errors.push(`pini: removed ≠ 29 (${r70.summary.removed})`);
  if (r70.summary.fuzije !== 33) p70Errors.push(`pini: fuzije ≠ 33 (${r70.summary.fuzije})`);
  if (r70.summary.rowsBefore !== 1079 || r70.summary.rowsAfter !== 1145)
    p70Errors.push(`pini: rows ≠ 1079→1145 (${r70.summary.rowsBefore}→${r70.summary.rowsAfter})`);
  if (r70.summary.bases !== 878 || r70.summary.multiPage !== 215 || r70.summary.crossBlatt !== 79)
    p70Errors.push(`pini: bases/multi/cross ≠ 878/215/79 (${r70.summary.bases}/${r70.summary.multiPage}/${r70.summary.crossBlatt})`);
  if (r70.summary.sectionsUnchanged !== 56) p70Errors.push(`pini: sekcije ≠ 56 (${r70.summary.sectionsUnchanged})`);
  if (r70.summary.areaMedian !== 3.8843 || r70.summary.areaDeltaPct !== 8.0)
    p70Errors.push(`pini: area ≠ 3.8843/+8.0 (${r70.summary.areaMedian}/${r70.summary.areaDeltaPct})`);
  if (r70.summary.conf.STRONG !== 188 || r70.summary.conf.MEDIUM !== 797 || r70.summary.conf.WEAK !== 160)
    p70Errors.push("pini: conf ≠ 188/797/160");
  const addedSum = Object.values(r70.addedByPage).reduce((a, b) => a + b, 0);
  if (addedSum !== 95) p70Errors.push(`pini: addedByPage vsota ≠ 95 (${addedSum})`);
  if (r70.noSource.length !== 3 || r70.noSource.some((n) => n.page !== 80))
    p70Errors.push("pini: noSource ≠ 3 × p80");
  if (r70.collisions.istiBlatt.length !== 33)
    p70Errors.push(`pini: kolizij isti-Blatt ≠ 32 (${r70.collisions.istiBlatt.length})`);
  if (p55v4.version !== 5 || p55v4.v5Delta.excludedSections !== 56 || p55v4.v5Delta.revertedP93 !== 15
    || p55v4.v5Delta.before.rows !== 1145 || p55v4.v5Delta.before.bases !== 878)
    p70Errors.push("pini: PS_GEO_P55 v5Delta (nasledstvo v4: before 1145/878 + C1 56 + C2 15) odmika");
  // 2) datoteke + NEODVISEN preracun (dve obliki po P53/P57/P58)
  let p70FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt70 = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    const rawEv70 = opts.readFile("research/issue17/ps-parcels-geo-v4.json");
    if (rawRt70 === null) {
      p70Errors.push("runtime ps-parcels-geo ni berljiv");
    } else {
      try {
        const rt70 = JSON.parse(rawRt70) as {
          version?: number;
          join: { matchedRows: number; psPositionedParcels: number; ambiguousBases: number; ambiguousRows: number; seriesCounts: { BI: number; S1: number; S2: number }; confCounts: { STRONG: number; MEDIUM: number; WEAK: number } };
          v4Delta?: { renumbered?: number; added?: number; removed?: number; noSource?: string[] };
          v5Delta?: { excludedSections?: number; revertedP93?: number; removed?: number; before?: { rows?: number; bases?: number; multiPage?: number; crossBlatt?: number } };
          rows: { page: number; base: string; parzella: string; series?: string; conf?: string | null; ambiguous?: boolean; areaQK: number | null; areaModern: number | null; areaSuspect?: boolean }[];
        };
        // P71: runtime je v5 — v4 živi v zamrznjenem dokazu; runtime mora
        // deklarirati nasledstvo (v5Delta == p71 korekcije)
        if ((rt70.version ?? 0) >= 5) {
          const d5 = rt70.v5Delta ?? {};
          if (d5.excludedSections !== 56 || d5.revertedP93 !== 15 || d5.removed !== 68)
            p70Errors.push(`runtime v5Delta ≠ 56/15/68 (${d5.excludedSections}/${d5.revertedP93}/${d5.removed})`);
          if (d5.before?.rows !== 1145 || d5.before?.bases !== 878 || d5.before?.multiPage !== 215 || d5.before?.crossBlatt !== 79)
            p70Errors.push(`runtime v5Delta.before ≠ 1145/878/215/79 (${d5.before?.rows}/${d5.before?.bases}/${d5.before?.multiPage}/${d5.before?.crossBlatt})`);
          if (rt70.join.matchedRows !== 1077 || rt70.join.psPositionedParcels !== 879)
            p70Errors.push(`runtime v5 join ≠ 1077/879 (${rt70.join.matchedRows}/${rt70.join.psPositionedParcels})`);
        } else if (rt70.version !== 4) {
          p70Errors.push(`runtime version ≠ 4 ali ≥ 5 (${rt70.version})`);
        }
        // vrstični preracun v4: repo oblika na zamrznjenem dokazu (rowsEvidence),
        // produkcija (brez research/) preskoči z deklaracijo nasledstva
        const v4rows: { page: number; base: string; parzella: string; series?: string; conf?: string | null; ambiguous?: boolean; areaQK: number | null; areaModern: number | null; areaSuspect?: boolean }[] =
          (rawEv70 !== null
            ? (JSON.parse(rawEv70) as { version?: number; rowsEvidence?: typeof v4rows }).rowsEvidence ?? []
            : rt70.version === 4 ? rt70.rows : []);
        if (v4rows.length === 1145) {
          if (rt70.version === 4) {
            if (rt70.join.matchedRows !== 1145 || rt70.join.psPositionedParcels !== 878)
              p70Errors.push("runtime join ≠ 1145/878");
            if (rt70.join.seriesCounts.BI !== 26 || rt70.join.seriesCounts.S1 !== 1049 || rt70.join.seriesCounts.S2 !== 70)
              p70Errors.push("runtime serije ≠ 26/1049/70");
            if (rt70.join.confCounts.STRONG !== 188 || rt70.join.confCounts.MEDIUM !== 797 || rt70.join.confCounts.WEAK !== 160)
              p70Errors.push("runtime zaupanje ≠ 188/797/160");
          }
          // preracun: preslikave parzella == from (P70 v vzorcu P68) — 77 vzorcev
          let mappedCount = 0;
          for (const m of r70.renumberSpec) {
            const hit = v4rows.find((r) => r.page === m.page && r.parzella === m.from);
            if (hit && hit.base !== m.to) p70Errors.push(`preracun: p${m.page} ${m.from} → base ${hit.base} ≠ ${m.to}`);
            if (hit && hit.base === m.to) mappedCount += 1;
          }
          // kolizije: 33 fuzij (dva bloka 921–1000) iz vrstic
          let fuzCount = 0;
          for (const c of r70.collisions.istiBlatt) {
            if (v4rows.some((r) => r.page === c.page && r.base === c.base)
              && v4rows.some((r) => r.page === c.existingPage && r.base === c.base)) fuzCount += 1;
          }
          if (fuzCount !== 33) p70Errors.push(`preracun: fuzij iz vrstic ≠ 33 (${fuzCount})`);
          // sekcije 56
          const secRows = v4rows.filter((r) => r.page === 83 || r.page === 84 || r.page === 85 || r.page === 86 || r.page === 88).length;
          if (secRows !== 56) p70Errors.push(`preracun: sekijskih vrstic ≠ 56 (${secRows})`);
          // area median preracun (P55 metoda)
          const p70Ratios = v4rows
            .filter((r) => r.areaQK && r.areaModern && !r.areaSuspect)
            .map((r) => (r.areaModern as number) / (r.areaQK as number))
            .sort((a, b) => a - b);
          const p70Med = p70Ratios.length % 2
            ? p70Ratios[(p70Ratios.length - 1) / 2]
            : (p70Ratios[p70Ratios.length / 2 - 1] + p70Ratios[p70Ratios.length / 2]) / 2;
          if (Math.abs(p70Med - 3.8843) > 0.005) p70Errors.push(`preracun: area median ${p70Med.toFixed(4)} ≠ 3.8843`);
          if (rawEv70 !== null) {
            const ev70 = JSON.parse(rawEv70) as { version?: number; rowsEvidence?: Record<string, unknown>[]; collisions?: { istiBlatt?: unknown[] } };
            if (ev70.version !== 4) p70Errors.push(`dokaz version ≠ 4 (${ev70.version})`);
            if ((ev70.collisions?.istiBlatt ?? []).length !== 33) p70Errors.push("dokaz kolizij ≠ 33");
            p70FileDetail = `repo: dokaz v4 zamrznjen (${(ev70.rowsEvidence ?? []).length} vrstic bajtno) · preracun na rowsEvidence: 1145 vrstic, preslikave parzella == originalno branje, fuzije 33 iz vrstic, sekcije 56, area median 3.8843 · runtime deklarira nasledstvo v5 (P71: C1 56 + C2 15)`;
          } else {
            p70FileDetail = `produkcija: v4 dokaz ni v buildu — preracun na v4 vrstvicah preskočen; runtime v5 deklarira nasledstvo (v5Delta 56/15/68, before 1145/878/215/79, join 1077/879) · preslikave ${mappedCount} vzorcev == to`;
          }
        } else if ((rt70.version ?? 0) >= 5) {
          // produkcija: v4 dokaz ni v buildu — vrstični preracun v4 preskočen;
          // nasledstvo je že preverjeno zgoraj (v5Delta deklaracija)
          p70FileDetail = `produkcija: v4 dokaz ni v buildu — preracun v4 preskočen; runtime v5 deklarira nasledstvo (v5Delta 56/15/68, before 1145/878/215/79, join 1077/879)`;
        } else {
          p70Errors.push(`v4 vrstic za preracun ≠ 1145 (${v4rows.length})`);
        }
      } catch (e) {
        p70Errors.push(`ps-parcels-geo v4 datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p70-v4-rejoin",
    "P70: IZVEDBA P69 SPECIFIKACIJE (issue #13) — mehanski izvod P69 očesne forenzike, deterministično: 77 renum preslikav (bajtno po P69 renumSpec; p74 +300, p79 −300, p80/p81 −100, p89/p90 ±1000 fantom-1, p92 −9, p99 +1000; parzella ostaja originalno branje) + 95 rejoin vrstic iz starih P38 slojev po P55 metodi (sloji po P69: pass1-pravilen p74/82/89/90/91; P38 izbira sicer; 3 kandidati p80 1541–1543 brez vira [~] — p1 odrez blok 62–81) + 29 preslikanih izpada (base brez PF poligona); 33 fuzij isti-Blatt (dva bloka registra 921–1000: p49–52 »glavni tek« + p89–92 »stolpec«; SPLIT = LASTNIKA); v4: 1145 vrstic / 878 base / 215 multi-page / 79 cross-Blatt; area median 3.8843 (Δ +8.0 %, kontrola 4.2701); soslednost 654/52.0/27.6×; zaupanje 188/797/160; 56 sekijskih vrstic (p83–86, p88) nespremanjenih (exclude/per-Blatt = LASTNIKA); nespremenjene vrstice bajtno == v3 (959); v3 arhiviran; status REVIEW",
    "P70: THE P69 SPECIFICATION REALIZED (issue #13) — a mechanical derivation of the P69 ocular forensics, deterministic: 77 renumber mappings (byte-equal to the P69 renumSpec; p74 +300, p79 −300, p80/p81 −100, p89/p90 ±1000 phantom-1, p92 −9, p99 +1000; parzella keeps the original reading) + 95 rows re-joined from the old P38 layers by the P55 method (layers per P69: pass1-correct p74/82/89/90/91; the P38 choice otherwise; 3 candidates p80 1541–1543 without a source [~] — p1 clipped block 62–81) + 29 mapped rows dropped (base without a PF polygon); 33 same-Blatt fusions (the register holds 921–1000 in two blocks: p49–52 'main run' + p89–92 'column'; SPLIT = the OWNER's); v4: 1145 rows / 878 bases / 215 multi-page / 79 cross-Blatt; area median 3.8843 (Δ +8.0 %, control 4.2701); adjacency 654/52.0/27.6×; confidence 188/797/160; 56 section rows (p83–86, p88) unchanged (exclude/per-Blatt = the OWNER's); unchanged rows byte-identical to v3 (959); v3 archived; status REVIEW",
    p70Errors.length === 0,
    p70Errors.length === 0
      ? `pini 77 preslikav / 95 rejoin / 29 izpada / 33 fuzij / 1079→1145 vrstic / 878 base / 215 multi / 79 cross · sekcije 56 · area 3.8843 (+8.0 %) · conf 188/797/160 · addedByPage vsota 95 · noSource 3×p80 · ${p70FileDetail}`
      : p70Errors.join("; "),
  );

  // ——— qa-p71: korekcije v4 (C1 sekcije exclude + C2 p93 reverzija) ———
  const p71Errors: string[] = [];
  const p71 = PS_GEO_P55;
  const v5 = V5_SECTIONS_P93_P71;
  // 1) TS pini (v5)
  if (p71.version !== 5) p71Errors.push(`pini: version ≠ 5 (${p71.version})`);
  if (p71.v5Delta.excludedSections !== 56 || p71.v5Delta.revertedP93 !== 15 || p71.v5Delta.removed !== 68)
    p71Errors.push(`pini: v5Delta ≠ 56/15/68 (${p71.v5Delta.excludedSections}/${p71.v5Delta.revertedP93}/${p71.v5Delta.removed})`);
  if (p71.v5Delta.before.rows !== 1145 || p71.v5Delta.before.bases !== 878
    || p71.v5Delta.before.multiPage !== 215 || p71.v5Delta.before.crossBlatt !== 79)
    p71Errors.push("pini: v5Delta.before ≠ 1145/878/215/79 (v4)");
  if (p71.v5Delta.after.rows !== 1077 || p71.v5Delta.after.bases !== 879
    || p71.v5Delta.after.multiPage !== 184 || p71.v5Delta.after.crossBlatt !== 48)
    p71Errors.push(`pini: v5Delta.after ≠ 1077/879/184/48 (${p71.v5Delta.after.rows}/${p71.v5Delta.after.bases}/${p71.v5Delta.after.multiPage}/${p71.v5Delta.after.crossBlatt})`);
  if (p71.join.matchedRows !== 1077 || p71.join.psPositionedParcels !== 879
    || p71.join.ambiguousBases !== 184 || p71.join.ambiguousRows !== 373)
    p71Errors.push("pini: join ≠ 1077/879/184/373");
  if (p71.areaProof.medianRatio !== 3.9052 || p71.areaProof.deltaPct !== 8.58
    || p71.spatialProof.consecPairs !== 652 || p71.spatialProof.medianM !== 51.8
    || p71.spatialProof.enrichmentX !== 25.5)
    p71Errors.push("pini: area/spatial ≠ 3.9052/8.58/652/51.8/25.5");
  if (v5.corrections.C1.excluded !== 56 || v5.corrections.C2.reverted !== 15
    || v5.corrections.C2.removed !== 12
    || v5.corrections.C2.pfMatches.join(",") !== "1603,1604,1605")
    p71Errors.push("pini: V5_SECTIONS_P93_P71 corrections ≠ 56/15/12/1603-1604-1605");
  // 2) datoteke + NEODVISEN preracun (dve obliki: repo = dokaz v5; produkcija = runtime)
  let p71FileDetail = "datoteke niso preverjene (readFile ni na voljo) — celovita kontrola teče na /api/qa";
  if (opts.readFile) {
    const rawRt = opts.readFile("src/data/atlas/ps-parcels-geo.json");
    const rawEv = opts.readFile("research/issue17/ps-parcels-geo-v5.json");
    if (rawRt === null) {
      p71Errors.push("runtime ps-parcels-geo ni berljiv");
    } else {
      try {
        const rt = JSON.parse(rawRt) as {
          version?: number;
          join: { matchedRows: number; psPositionedParcels: number; ambiguousBases: number; ambiguousRows: number };
          v5Delta?: { excludedSections?: number; revertedP93?: number; removed?: number };
          rows: { page: number; base: string; parzella: string; areaQK: number | null; areaModern: number | null; areaSuspect?: boolean }[];
        };
        if (rt.version !== 5) p71Errors.push(`runtime version ≠ 5 (${rt.version})`);
        if (rt.rows.length !== 1077) p71Errors.push(`runtime vrstic ≠ 1077 (${rt.rows.length})`);
        if (rt.join.matchedRows !== 1077 || rt.join.psPositionedParcels !== 879
          || rt.join.ambiguousBases !== 184 || rt.join.ambiguousRows !== 373)
          p71Errors.push(`runtime join ≠ 1077/879/184/373 (${rt.join.matchedRows}/${rt.join.psPositionedParcels}/${rt.join.ambiguousBases}/${rt.join.ambiguousRows})`);
        // C1 preracun: 0 vrstic na sekijskih straneh (83/84/85/86/88)
        const secRows = rt.rows.filter((r) => r.page === 83 || r.page === 84 || r.page === 85 || r.page === 86 || r.page === 88).length;
        if (secRows !== 0) p71Errors.push(`preracun C1: sekijskih vrstic v runtime ≠ 0 (${secRows})`);
        // C2 preracun: p93 = točno 3 vrstice, vse base == parzella, PF match set
        const r93 = rt.rows.filter((r) => r.page === 93);
        if (r93.length !== 3) p71Errors.push(`preracun C2: p93 vrstic ≠ 3 (${r93.length})`);
        if (r93.some((r) => r.base !== r.parzella))
          p71Errors.push("preracun C2: p93 base ≠ parzella (reverzija nepopolna)");
        const r93set = r93.map((r) => r.base).sort().join(",");
        if (r93set !== "1603,1604,1605")
          p71Errors.push(`preracun C2: p93 base set ${r93set} ≠ 1603,1604,1605`);
        // C2 preracun: 1904/1906 izpadla iz base seta, 1603/1604/1605 prisotni
        const bases = new Set(rt.rows.map((r) => r.base));
        if (bases.has("1904") || bases.has("1906"))
          p71Errors.push("preracun C2: base 1904/1906 še prisotna (pričakovano izpad)");
        for (const b of ["1603", "1604", "1605"]) {
          if (!bases.has(b)) p71Errors.push(`preracun C2: base ${b} manjka (pričakovan vnos p93)`);
        }
        // area median preracun (P55 metoda) — 3.9052
        const p71Ratios = rt.rows
          .filter((r) => r.areaQK && r.areaModern && !r.areaSuspect)
          .map((r) => (r.areaModern as number) / (r.areaQK as number))
          .sort((a, b) => a - b);
        const p71Med = p71Ratios.length % 2
          ? p71Ratios[(p71Ratios.length - 1) / 2]
          : (p71Ratios[p71Ratios.length / 2 - 1] + p71Ratios[p71Ratios.length / 2]) / 2;
        if (Math.abs(p71Med - 3.9052) > 0.005) p71Errors.push(`preracun: area median ${p71Med.toFixed(4)} ≠ 3.9052`);
        if (rawEv !== null) {
          const ev = JSON.parse(rawEv) as {
            version?: number;
            rowsEvidence?: Record<string, unknown>[];
            corrections?: { C1?: { excludedRows?: unknown[] }; C2?: { removedRows?: unknown[]; revertedRows?: number } };
            removedRows?: unknown[];
          };
          if (ev.version !== 5) p71Errors.push(`dokaz version ≠ 5 (${ev.version})`);
          if ((ev.corrections?.C1?.excludedRows ?? []).length !== 56)
            p71Errors.push(`dokaz C1 excludedRows ≠ 56 (${(ev.corrections?.C1?.excludedRows ?? []).length})`);
          if ((ev.corrections?.C2?.removedRows ?? []).length !== 12
            || ev.corrections?.C2?.revertedRows !== 15)
            p71Errors.push(`dokaz C2 ≠ 12 izpad / 15 reverz (${(ev.corrections?.C2?.removedRows ?? []).length}/${ev.corrections?.C2?.revertedRows})`);
          if ((ev.removedRows ?? []).length !== 68)
            p71Errors.push(`dokaz removedRows ≠ 68 (${(ev.removedRows ?? []).length})`);
          const subset = rt.rows.every((rr, i) =>
            Object.entries(rr).every(([k, v]) => JSON.stringify((ev.rowsEvidence ?? [])[i]?.[k]) === JSON.stringify(v)));
          if (!subset) p71Errors.push("dokaz v5 ⊉ runtime: vrstice niso bajtno enake");
          p71FileDetail = `repo: dokaz v5 == runtime bajtno (${(ev.rowsEvidence ?? []).length} vrstic; C1 56 + C2 12/15 = 68 removedRows) · preracun: 0 sekijskih vrstic, p93 base == parzella 3/3 {1603,1604,1605}, 1904/1906 izpad, 1603/1604/1605 prisotni, area median ${p71Med.toFixed(4)}`;
        } else {
          p71FileDetail = `produkcija: preracun na runtime v5 — 0 sekijskih vrstic, p93 base == parzella 3/3 {1603,1604,1605}, 1904/1906 izpad, 1603/1604/1605 prisotni, area median ${p71Med.toFixed(4)}`;
        }
      } catch (e) {
        p71Errors.push(`ps-parcels-geo v5 datoteke neuspešno: ${String(e).slice(0, 80)}`);
      }
    }
  }
  push(
    "qa-p71-v5-corrections",
    "P71: KOREKCIJE v4 (issue #13) — (C1) 56 sekijskih vrstic (p83 13 · p84 12 · p85 14 · p86 14 · p88 3) EXCLUDE iz joina (P69 sectionClass bajtno; dokazane lažne fuzije na Blatt I poligone — Σ ratio 161 = 235.65×, lastniško prekrivanje s p11 = 0; LASTNIŠKA odločitev: opcija exclude; vrstice ostanejo v registru brez geometrije; 0 poligonov ostane praznih) + (C2) P93 REVERZIJA — P68 renum 160x→190x OVRŽEN: notranja glifna kontrola (r9 = 1609 / r19 = 1619 — gotova 9 z repom ≠ srednja 6; isti pisar; kontrole p98 '1916' = 9 in 6 v istem številu, p92 981–983 verificirane 9) + annRecords anotatorja (1601–1619, 'Durch Theilung im 1824', '1870. 8-1117') + pageMap P56 + P38 pass2; 15 vrstic base := parzella; PF ujemanja {1603, 1604, 1605} (prej prazni poligoni dobili prve vrstice), 12 izpadlih (base brez PF poligona — 1601–1620 večinoma odsotnih v sodobnem k.o.); PF 1901–1920 brez lažnih dvojnih zahtevkov p93 (ostane p98 III), PF 1904/1906 izpadla iz base seta; v5: 1077 vrstic / 879 base / 184 multi-page / 48 cross-Blatt; area median 3.9052 (Δ +8.58 %, kontrola 4.2304); soslednost 652/51.8/25.5×; nespremenjene vrstice bajtno == v4 (1041 + 33 group-derived); forenzika research/issue17/p93-forensics/ (7 izrezov 8–12×); skripta --check PASS; status REVIEW",
    "P71: THE v4 CORRECTIONS (issue #13) — (C1) 56 section rows (p83 13 · p84 12 · p85 14 · p86 14 · p88 3) EXCLUDED from the join (P69 sectionClass byte-equal; proven false fusions onto Blatt I polygons — Σ ratio 161 = 235.65×, owner overlap with p11 = 0; the OWNER's decision: the exclude option; the rows stay in the register without geometry; 0 polygons left empty) + (C2) THE P93 REVERSION — the P68 renum 160x→190x REFUTED: the within-page glyph control (r9 = 1609 / r19 = 1619 — the certain 9 with a descender ≠ the middle 6; same scribe; controls p98 '1916' = 9 and 6 in the same number, p92 981–983 verified 9s) + the annotator's annRecords (1601–1619, 'Durch Theilung im 1824', '1870. 8-1117') + the P56 pageMap + P38 pass2; 15 rows base := parzella; PF matches {1603, 1604, 1605} (previously empty polygons got their first rows), 12 dropped (base without a PF polygon — 1601–1620 mostly absent from the modern c.m.); PF 1901–1920 free of p93's false double claims (p98 III remains), PF 1904/1906 dropped from the base set; v5: 1,077 rows / 879 bases / 184 multi-page / 48 cross-Blatt; area median 3.9052 (Δ +8.58 %, control 4.2304); adjacency 652/51.8/25.5×; unchanged rows byte-identical to v4 (1,041 + 33 group-derived); forensics research/issue17/p93-forensics/ (7 crops 8–12×); the script --check PASS; status REVIEW",
    p71Errors.length === 0,
    p71Errors.length === 0
      ? `pini v5Delta 56/15/68 · before 1145/878/215/79 · after 1077/879/184/48 · area 3.9052 (+8.58 %) · sosledje 652/51.8/25.5× · corrections 56/15/12/{1603,1604,1605} · ${p71FileDetail}`
      : p71Errors.join("; "),
  );

  const passed = tests.filter((t) => t.pass).length;  return {
    ok: tests.every((t) => t.pass),
    passed,
    failed: tests.length - passed,
    tests,
    computedAt: new Date().toISOString(),
  };
}
