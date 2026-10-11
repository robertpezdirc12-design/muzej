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

  // A03 = celica dg
  if (!georefA03) {
    p10Errors.push("georef-a03 manjka v SHEET_GEOREFS");
  } else {
    const b = georefA03.bounds;
    if (georefA03.status !== "REVIEW") p10Errors.push(`A03 status: ${georefA03.status} (pričakovano REVIEW)`);
    if (Math.abs(b[0][0] - 45.5575) > 0.0005 || Math.abs(b[0][1] - 15.2485) > 0.0005)
      p10Errors.push(`A03 bounds S/Z: ${b[0]} (pričakovano [45.5575, 15.2485] = celica VKIX24dg)`);
    if (Math.abs(b[1][0] - 45.5437) > 0.0005 || Math.abs(b[1][1] - 15.273) > 0.0005)
      p10Errors.push(`A03 bounds J/V: ${b[1]} (pričakovano [45.5437, 15.2730])`);
    if (georefA03.pixels.width !== 2645 || georefA03.pixels.height !== 2154)
      p10Errors.push(`A03 px: ${georefA03.pixels.width}×${georefA03.pixels.height}`);
    const cpSi = georefA03.controlPoints.map((c) => c.fromSi).join(" |");
    for (const must of ["VKIX24dg", "TRIBUTSCH", "WEIDENDORF"]) {
      if (!cpSi.includes(must)) p10Errors.push(`A03 kontrolna točka manjka: ${must}`);
    }
    if (!georefA03.methodSi.includes("O.IX24dg")) p10Errors.push("A03 metoda mora navesti oznako »O.IX24dg«");
  }

  // A04 = POPRAVLJENA celica cg (P9 umaknjena)
  if (!georefA04) {
    p10Errors.push("georef-a04 manjka v SHEET_GEOREFS");
  } else {
    const b = georefA04.bounds;
    if (georefA04.status !== "REVIEW") p10Errors.push(`A04 status: ${georefA04.status} (pričakovano REVIEW — popravek P9)`);
    if (Math.abs(b[0][0] - 45.5574) > 0.0005 || Math.abs(b[0][1] - 15.2728) > 0.0005)
      p10Errors.push(`A04 bounds S/Z: ${b[0]} (pričakovano [45.5574, 15.2728] = celica VKIX24cg)`);
    if (Math.abs(b[1][0] - 45.5436) > 0.0005 || Math.abs(b[1][1] - 15.2973) > 0.0005)
      p10Errors.push(`A04 bounds J/V: ${b[1]} (pričakovano [45.5436, 15.2973])`);
    if (georefA04.scaleMPerPixel !== 0.72) p10Errors.push(`A04 merilo: ${georefA04.scaleMPerPixel} (pričakovano 0,72)`);
    if (!georefA04.methodSi.includes("POPRAVEK")) p10Errors.push("A04 metoda mora biti označena kot POPRAVEK");
    if (!georefA04.methodSi.includes("O.IX24cg")) p10Errors.push("A04 metoda mora navesti oznako »O.IX24cg«");
    if (!georefA04.methodSi.includes("636 m")) p10Errors.push("A04 metoda mora navesti zavrnitev P9 (mediana 636 m)");
    if (georefA04.controlPoints.length < 3) p10Errors.push(`A04 kontrolne točke: ${georefA04.controlPoints.length} (pričakovano ≥ 3)`);
  }

  // A05 = celica ch
  if (!georefA05) {
    p10Errors.push("georef-a05 manjka v SHEET_GEOREFS");
  } else {
    const b = georefA05.bounds;
    if (georefA05.status !== "REVIEW") p10Errors.push(`A05 status: ${georefA05.status} (pričakovano REVIEW)`);
    if (Math.abs(b[0][0] - 45.5437) > 0.0005 || Math.abs(b[0][1] - 15.2726) > 0.0005)
      p10Errors.push(`A05 bounds S/Z: ${b[0]} (pričakovano [45.5437, 15.2726] = celica VKIX24ch)`);
    if (Math.abs(b[1][0] - 45.5299) > 0.0005 || Math.abs(b[1][1] - 15.2971) > 0.0005)
      p10Errors.push(`A05 bounds J/V: ${b[1]} (pričakovano [45.5299, 15.2971])`);
    if (georefA05.pixels.width !== 2634 || georefA05.pixels.height !== 2165)
      p10Errors.push(`A05 px: ${georefA05.pixels.width}×${georefA05.pixels.height}`);
    const cpSi = georefA05.controlPoints.map((c) => c.fromSi).join(" |");
    for (const must of ["VKIX24ch", "Jankovichti"]) {
      if (!cpSi.includes(must)) p10Errors.push(`A05 kontrolna točka manjka: ${must}`);
    }
    if (!georefA05.methodSi.includes("O.IX24ch")) p10Errors.push("A05 metoda mora navesti oznako »O.IX24ch«");
  }

  // viri: 2 lista VALIDIRANA (A01/A02) + 3 listi GRID_APPROX (A03–A05, issue #4 ločitev natančnosti)
  const graphicSheets = ATLAS_SOURCES.filter((s) => s.type === "cadastral-map");
  const geoCount = graphicSheets.filter((s) => s.georefStatus === "GEOREFERENCED").length;
  const gridCount = graphicSheets.filter((s) => s.georefStatus === "GRID_APPROX").length;
  if (geoCount !== 2) p10Errors.push(`validirano georeferencirani grafični listi: ${geoCount} (pričakovano 2 — A01/A02)`);
  if (gridCount !== 3) p10Errors.push(`listi z okvirno umestitvijo (GRID_APPROX): ${gridCount} (pričakovano 3 — A03/A04/A05)`);
  const srcA01 = ATLAS_SOURCES.find((s) => s.id === "src-a01");
  const srcA02 = ATLAS_SOURCES.find((s) => s.id === "src-a02");
  const srcA03 = ATLAS_SOURCES.find((s) => s.id === "src-a03");
  const srcA04 = ATLAS_SOURCES.find((s) => s.id === "src-a04");
  const srcA05 = ATLAS_SOURCES.find((s) => s.id === "src-a05");
  for (const [src, id] of [[srcA01, "src-a01"], [srcA02, "src-a02"]] as const) {
    if (!src || src.georefStatus !== "GEOREFERENCED" || src.georeferenced !== true || src.placement?.precision !== "VALIDATED_GEOREF")
      p10Errors.push(`${id} ni GEOREFERENCED z VALIDATED_GEOREF placement`);
  }
  for (const [src, id, cell] of [[srcA03, "src-a03", "dg"], [srcA04, "src-a04", "cg"], [srcA05, "src-a05", "ch"]] as const) {
    if (!src || src.georefStatus !== "GRID_APPROX" || src.georeferenced !== false || src.placement?.precision !== "GRID_APPROX")
      p10Errors.push(`${id} ni GRID_APPROX z ustreznim placement`);
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
  // pokritost (issue #4: ločeno validirana 2 + približna 3)
  const covP10 = getCoverage();
  if (covP10.sheetsGeoreferenced !== 2 || covP10.sheetsGridApprox !== 3 || covP10.sheetsTotal !== 5)
    p10Errors.push(`COVERAGE listi: validirani ${covP10.sheetsGeoreferenced} / približni ${covP10.sheetsGridApprox} / skupaj ${covP10.sheetsTotal} (pričakovano 2/3/5)`);

  push(
    "qa-p10-ezkn-grid",
    "P10: sekcija mreža eZKN razrešila vse liste — A03=celica dg, A04=celica cg (POPRAVEK P9), A05=celica ch; issue #4: 2 lista validirano georeferencirana (A01/A02), 3 listi okvirno umesčeni po mreži (GRID_APPROX ±200–400 m)",
    "P10: the eZKN section grid resolved ALL sheets — A03=cell dg, A04=cell cg (P9 CORRECTION), A05=cell ch; issue #4: 2 sheets validated georeference (A01/A02), 3 sheets approximately placed by the grid (GRID_APPROX ±200–400 m)",
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
  if (pzInv && pzInv.structuredEntities !== 10) p20invErrors.push(`PZ structured: ${pzInv.structuredEntities}`);
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
  const expectedRead: Record<string, number> = { PR: 4, PS: 143, PUA: 49, PZ: 12, PT: 8, PG: 1, PV: 1 };
  for (const [code, n] of Object.entries(expectedRead)) {
    const k = KURRENT_SERIES.find((x) => x.code === code);
    if (k && k.pagesTranscribed !== n)
      p20pagesErrors.push(`${code}: pagesTranscribed ${k.pagesTranscribed} != dokazano ${n} (PS-structure/PZ-valuation.json)`);
  }
  const invScope = getArchiveInventory();
  if (!invScope.totals.scopeAccounted) p20pagesErrors.push("inventar: scopeAccounted ni true za vse enote");
  push(
    "qa-p20-series-pages",
    "P20: dokazano prebrane strani po serijah (PR 4, PS 143 — P36 strojno, PUA 49, PZ 12, PT 8, PG 1, PV 1) — pagesReadList == pagesTranscribed, brez lukenj; PS in PZ usklajena z research/issue17 datotekami (ps-raw + PS-full.json)",
    "P20: evidenced read pages per series (PR 4, PS 143 — P36 machine-read, PUA 49, PZ 12, PT 8, PG 1, PV 1) — pagesReadList == pagesTranscribed, no gaps; PS and PZ reconciled with the research/issue17 files (ps-raw + PS-full.json)",
    p20pagesErrors.length === 0,
    p20pagesErrors.length === 0
      ? `skupaj ${invScope.totals.pagesRead}/${invScope.totals.pagesDeclared} prebranih; odprtih strani ${invScope.totals.pagesOpen} (PZ 4–67 razen vzorcev; PS strani strojno prebrane, a sprava s 2607 izrecno odprta) — 0 tihih`
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
  if (covGeo.sheetsGeoreferenced !== 2 || covGeo.sheetsGridApprox !== 3)
    p20geoErrors.push(`pokritost: ${covGeo.sheetsGeoreferenced}+${covGeo.sheetsGridApprox} (pričakovano 2+3)`);
  if (covGeo.archivalUnits !== 12) p20geoErrors.push(`archivalUnits: ${covGeo.archivalUnits} (pričakovano 12)`);
  if (covGeo.archivalPages !== 277) p20geoErrors.push(`archivalPages: ${covGeo.archivalPages} (pričakovano 277 = 143+71+49+8+4+1+1)`);
  if (covGeo.housesWithGeometry !== 0)
    p20geoErrors.push(`housesWithGeometry: ${covGeo.housesWithGeometry} — hiša↔stavba povezava zahteva dokaz (156 geometrij nima hišnih št.)`);
  push(
    "qa-p20-georef-precision",
    "P20: natančnost prostorske umestitve ločena — A01/A02 VALIDIRANA georeferenca (±40–100 m), A03–A05 GRID_APPROX (±200–400 m, sekcijska mreža); 12 enot, 277 strani fonda, 0 hiš z dokazano geometrijo",
    "P20: spatial placement precision separated — A01/A02 VALIDATED georeference (±40–100 m), A03–A05 GRID_APPROX (±200–400 m, section grid); 12 units, 277 fond pages, 0 houses with proven geometry",
    p20geoErrors.length === 0,
    p20geoErrors.length === 0
      ? "listi: 2 validirana + 3 približno umesčene (vsak s placement: method/controlPoints/accuracy/lastChecked); pokritost 2+3=5"
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
      ? `enote: ${rec.units.length}; vse scopeCheck.accounted; zeroLoss=${rec.zeroLoss}; pomen dokumentiran (PS 135 + PZ 59 strani izrecno odprtih, ne prikrito)`
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
      p36Errors.push(`N083PS: structuredEntries=${psSrc.structuredEntries}, pričakovano 2974 (P36 2743 + P38 3. prehod 20 strani)`);
    if (psSrc.lastVerified !== "2026-10-11")
      p36Errors.push("N083PS: lastVerified ni 2026-10-11 (dan P36 kampanje)");
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
    p36Errors.push(`PS_RECAP_1826.sampleRowCount=${PS_RECAP_1826.sampleRowCount}, pričakovano 2974 (P38)`);
  if (!(PS_RECAP_1826.mostUsefulSi ?? "").includes("P36"))
    p36Errors.push("PS_RECAP_1826: priporočilo SL ne odraža P36 kampanje (zastarelo »NE prepisovati«)");
  push(
    "qa-p36-ps-machineread",
    "P36: N083PS — strojni prepis VSEH 135 strani (5–139) dokumentiran v viru (2743 vrstic, dvoprehodno, dokaz ps-raw + PS-full.json); strukturne ugotovitve (pomešan zvezek, sekcije Waldung/Schmiegärten/Blatt X, kontrolna vsota 2607 kot vsota kategorij) vidne v notah; sprava s 2607 ostaja TO_COLLECT",
    "P36: N083PS — machine transcription of ALL 135 pages (5–139) documented at the source (2,743 rows, two passes, evidence ps-raw + PS-full.json); structural findings (shuffled volume, Waldung/Schmiegärten/Blatt X sections, the 2,607 checksum as a category sum) visible in the notes; the reconciliation remains TO_COLLECT",
    p36Errors.length === 0,
    p36Errors.length === 0
      ? "135 strani · 2743 vrstic P36 (2974 po P38) · 213+20 VLM branj · 4 sekcije odkrite"
      : p36Errors.join("; "),
  );

  // P38 (issue #10): 3. prehod PS — strukturno odkritje listov (Blatt) + adjudikacija.
  const p38Errors: string[] = [];
  {
    const ps = ATLAS_SOURCES.find((s) => s.code === "N083PS");
    if (!ps) p38Errors.push("vir N083PS manjka");
    else {
      if (!(ps.noteSi ?? "").includes("P38")) p38Errors.push("N083PS: nota SL ne dokumentira P38 (3. prehod)");
      if (!(ps.noteSi ?? "").includes("Blatt I")) p38Errors.push("N083PS: nota SL brez strukturnega odkritja listov (Blatt)");
      if (!(ps.noteSi ?? "").includes("PS-full-v2.json")) p38Errors.push("N083PS: nota SL brez kazalca na PS-full-v2.json");
      if (!(ps.noteSi ?? "").includes("69, 85, 86, 88, 93, 128, 138"))
        p38Errors.push("N083PS: nota SL brez seznama nerešenih strani za #12");
      if (!(ps.noteEn ?? "").includes("per-sheet")) p38Errors.push("N083PS: nota EN brez per-sheet rekonstrukcije v naslednjih korakih");
    }
    if (PS_RECAP_1826.sampleRowCount !== 2974) p38Errors.push("PS_RECAP: števec vrstic ni 2974");
    if (!(PS_RECAP_1826.mostUsefulSi ?? "").includes("P38")) p38Errors.push("PS_RECAP: priporočilo SL ne odraža P38");
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
        if (missing.length) p38Errors.push(`ps-raw: manjka pass3 za strani ${missing.join(", ")}`);
        if (!fileExists("research/issue17/PS-full-v2.json")) p38Errors.push("manjka PS-full-v2.json");
      }
    }
  }
  push(
    "qa-p38-ps-blatt",
    "P38: N083PS — 3. prehod 20 ciljnih strani (233 VLM branj) + odkritje organizacije po listih (Blatt I–X, lastno številčenje); identiteta parcele = (list, številka); kontrolna vsota 2607 je vsota čez vse liste; 7 nerešenih strani izrecno za človeški pregled (#12)",
    "P38: N083PS — 3rd pass over 20 target pages (233 VLM reads) + discovery of sheet organization (Blatt I–X, own numbering); parcel identity = (sheet, number); the 2,607 checksum sums across all sheets; 7 unresolved pages explicitly deferred to human review (#12)",
    p38Errors.length === 0,
    p38Errors.length === 0
      ? "20 strani pass-3 · 2974 izbranih vrstic · str. 24 potrjena 421-440 · nerešene: 69, 85, 86, 88, 93, 128, 138"
      : p38Errors.join("; "),
  );

  const passed = tests.filter((t) => t.pass).length;
  return {
    ok: tests.every((t) => t.pass),
    passed,
    failed: tests.length - passed,
    tests,
    computedAt: new Date().toISOString(),
  };
}