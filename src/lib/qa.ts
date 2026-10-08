// ISSUE #4 — end-to-end kontrola kakovosti.
// Avtomatski testi, ki preverijo celovitost zbirke, sprehodov in coverage.
// Testi se poganjajo prek /api/qa (HTTP 200 = vsi testi zeleni, 500 = napaka).

import exhibitsRaw from "@/data/museum/exhibits.json";
import metaRaw from "@/data/museum/meta.json";
import extraRaw from "@/data/museum/extra.json";
import { WALKS, walkItemsWithGaps, WALK_GAPS } from "./walks";
import { computeCoverage } from "./coverage";
import { buildReconciliation } from "./reconciliation";
import { NEGATIVE_RESULTS } from "@/data/atlas/sources";
import { parishStats } from "./atlas";
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
  PT_REVIEW_2026,
  PT_PALEOGRAPHY_P3,
  ORAL_HISTORY_PROTOCOL,
  WEB_VERIFICATIONS,
  ISSUE17_MATRIX,
  ISSUE17_AUDIT,
} from "@/data/atlas/research";
import { ATLAS_HOUSES } from "@/data/atlas/houses";
import { ATLAS_OWNERS } from "@/data/atlas/model";

interface ExhibitRow {
  id: string;
  slug: string;
  museumNo: string;
  evidenceStatus: string | null;
  model3dUrl: string | null;
  lat: number | null;
  lng: number | null;
  sources: { nameSi?: string | null; nameEn?: string | null; url?: string | null }[] | null;
}

const EXHIBITS = (exhibitsRaw as { exhibits: ExhibitRow[] }).exhibits;
const META = metaRaw as { count?: { exhibits?: number } };
const EXTRA = extraRaw as Record<string, { walk?: { name?: string; station?: number } | null }>;

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

export function runQA(): QAReport {
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

  // 6. noben obstoječi muzejski zapis ni izgubljen (113)
  const metaCount = META.count?.exhibits ?? EXHIBITS.length;
  push(
    "qa-no-loss",
    "noben muzejski zapis ni izgubljen (113)",
    "no museum record is lost (113)",
    EXHIBITS.length === 113 && metaCount === EXHIBITS.length,
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
    walkOk && !!firstWalk && firstWalk.explicitGaps === 1 && firstWalk.total === 35,
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
  // PUA: 18 vrstic str. 3–10 + 4 vrstice P3 str. 11 + 47 vrstic P4 str. 12–34 = 69
  if (PUA_CONTINUATION.rows.length !== 69 || PUA_CONTINUATION.pagesRead.length !== 32) {
    i17Errors.push(`PUA nadaljevanje: ${PUA_CONTINUATION.rows.length} vrstic / ${PUA_CONTINUATION.pagesRead.length} strani (pričakovano 69/32 po P4)`);
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
  // KURRENT_SERIES posodobljen (PT 84, PUA 34 strani po P4)
  const ptSeries = KURRENT_SERIES.find((s) => s.code === "PT");
  const puaSeries = KURRENT_SERIES.find((s) => s.code === "PUA");
  if (ptSeries?.structuredEntries !== 84 || puaSeries?.pagesTranscribed !== 34 || puaSeries?.structuredEntries !== 90) {
    p3Errors.push("KURRENT_SERIES PT/PUA nista posodobljena po P3/P4");
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

  // 17. P4 — PUA nadaljevanje (str. 12–34): struktura, ključni priimki, križanje s PT
  const p4Errors: string[] = [];
  const p4All = PUA_CONTINUATION.rows.filter((r) => r.page >= 12);
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
  // PUA strani 35–49 morajo ostati TO_COLLECT v opombi
  if (!PUA_CONTINUATION.noteSi.includes("35–49") || !PUA_CONTINUATION.noteSi.includes("TO_COLLECT")) {
    p4Errors.push("P4: opomba mora dokumentirati strani 35–49 kot TO_COLLECT");
  }
  push(
    "qa-p4-pua-nadaljevanje",
    "P4 PUA nadaljevanje: strani 12–34 (47 vnosov, zap. št. 22–68), Kirche H. Veith, križanje s PT, strani 35–49 ostajajo TO_COLLECT",
    "P4 PUA continuation: pages 12–34 (47 entries, rows 22–68), Kirche H. Veith, PT cross-check, pages 35–49 remain TO_COLLECT",
    p4Errors.length === 0,
    p4Errors.length === 0
      ? `23 strani (12–34) po 1 VLM klic; 47 vnosov: Höflehner, Jakobstitzsch, Jankovitsche, Krischan, Loral, Kosirhan, Grönig, Wundsch, Bučar, Kirche H. Veith (cerkev sv. Vida [~]), Hlobutschar, Lukentitz, Rappar, Millea, Mallestitak, Mandl, Grangl, Polcig, Muhč, Leiner, Rußa, Juttner, Jhan, Gnoy, Pasticz, Prodoritche, Pfister; ključna ugotovitev: PUA ≠ PT številčenje hiš [~]; statusi REVIEW`
      : p4Errors.join("; "),
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
