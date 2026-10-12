// ISSUE #5 — KONTROLA POPOLNOSTI: N83 arhiv → Atlas brez izgubljenih zapisov.
//
// Zero-loss pravilo: vsak izvorni zapis (vrstica PT/PUA/PS, list, stran) ima
// vrstico v reconciliation poročilu z eksplicitnim stanjem. Noben zapis ni
// tiho izpuščen, če ga ni mogoče povezati — dobi status in razlog.
//
// Veriga (issue #5 #1): izvorni dokument/list/stran → izvorna vrstica →
// interna entiteta → ID → status → geometrija (če obstaja) → povezani vir.
// Kurrent sled (issue #5 #5): sken → stran → prepis → entiteta (+ različica).

import { ATLAS_SOURCES } from "@/data/atlas/sources";
import { ATLAS_HOUSES } from "@/data/atlas/houses";
import { ATLAS_OWNERS, VECTOR_BUILDINGS } from "@/data/atlas/model";
import { KURRENT_SERIES, PUA_CONTINUATION } from "@/data/atlas/research";
import { getArchiveInventory } from "./atlas";
import { DATA_VERSION } from "./provenance";

export type ReconState =
  | "STRUCTURED_LINKED" /** preneseno, strukturirano, povezano */
  | "STRUCTURED_UNRESOLVED" /** strukturirano, a povezava ni mogoča (ohranjeno!) */
  | "SHEET_VECTORISED" /** grafični list: vektorizirane entitete */
  | "SHEET_TRANSFERRED" /** list prenesen, vektorizacija TO_COLLECT */
  | "PENDING_TRANSCRIPTION" /** enota obstaja, prepis še ni izdelan */
  | "CROSS_CHECKED"; /** navzkrižno potrjeno (PUA ↔ PT) */

export interface ReconRow {
  /** enota vira (N083PT, N083A02 …) */
  unit: string;
  /** list/stran */
  locatorSi: string;
  locatorEn: string;
  /** identifikator izvorne vrstice, kadar obstaja */
  rowId: string;
  /** povezana entiteta Atlasa (hiša/parcela/lastnik/stavba) */
  entitySi: string;
  entityEn: string;
  entityId: string | null;
  state: ReconState;
  evidenceStatus: string;
  /** geometrija, če obstaja */
  geometry: string | null;
  /** št. izpeljanih strukturiranih entitet iz te vrstice (npr. 156 stavb z lista) */
  derivedCount: number;
  /** manjkajoča povezava / razlog, zakaj je zapis odprt */
  openSi: string | null;
  openEn: string | null;
}

export interface UnitRecon {
  code: string;
  titleSi: string;
  titleEn: string;
  vacUrl: string | null;
  transferStatus: string | null;
  georefStatus: string | null;
  pages: number | null;
  /** obseg, ki ga enota zajema po evidenci (vrstice/objekti) */
  declaredScope: number;
  /** strojno prešteti obdelani zapisi (vključno z izpeljanimi entitetami) */
  processedRows: number;
  /** št. vrstic poročila za to enoto */
  reportRows: number;
  structured: number;
  linked: number;
  unresolved: number;
  /** ISSUE #4: kontrola obsega po INVENTARJU — deklarirane strani == dokazano
   *  prebrane + izrecno odprte (strani), ne samo statusev ustvarjenih vrstic */
  scopeCheck: {
    pagesDeclared: number | null;
    pagesRead: number | null;
    pagesOpen: number | null;
    pagesOpenRangesSi: string | null;
    accounted: boolean;
  };
  zeroLoss: boolean;
}

export interface ReconciliationReport {
  generatedAt: string;
  dataVersion: string;
  units: UnitRecon[];
  rows: ReconRow[];
  totals: {
    originalRows: number;
    processedRows: number;
    linked: number;
    unresolved: number;
    /** izgubljeni (brez statusa) — MORA biti 0 */
    lost: number;
    sheetsVectorised: number;
    sheetsTransferred: number;
  };
  zeroLoss: boolean;
  /** ISSUE #4: kaj zeroLoss POTRDIUJE in česa NE — poštena opredelitev,
   *  da števec ne more prikriti manjkajočih izvornih vrstic */
  zeroLossMeaningSi: string;
  zeroLossMeaningEn: string;
  kurrentTrail: {
    code: string;
    scan: string;
    pages: number;
    pagesTranscribed: number;
    chainSi: string;
    chainEn: string;
    version: string;
    status: string;
  }[];
}

/**
 * Avtomatsko poročilo — IZRAČUNANO iz ATLAS_HOUSES/ATLAS_OWNERS/
 * VECTOR_BUILDINGS/ATLAS_SOURCES, ne ročno napisano.
 */
export function buildReconciliation(): ReconciliationReport {
  const rows: ReconRow[] = [];

  const ptSource = ATLAS_SOURCES.find((s) => s.id === "src-pt");
  const puaSource = ATLAS_SOURCES.find((s) => s.id === "src-pua");
  const ptScan = ptSource?.fileRef ?? "IIIF";

  // ——— PT: protokol stavbnih parcel (hišne vrstice str. 3–4 + parcelni del str. 5–7) ———
  for (const h of ATLAS_HOUSES) {
    const owner = ATLAS_OWNERS.find((o) => o.houseRefs.some((r) => r === h.no));
    const isParcel = h.no === "—";
    rows.push({
      unit: "N083PT",
      /* issue #4: parcelne vrstice (str. 5–7) so DEL PROTOKOLA PT (»str. 5 = parcele 41–60«
         po PT-review), ne register PS — prejšnja oznaka je bila zavajajoča */
      locatorSi: `stran ${h.sourcePage}${isParcel ? " (parcelni del protokola PT)" : ""}`,
      locatorEn: `page ${h.sourcePage}${isParcel ? " (the parcel part of protocol PT)" : ""}`,
      rowId: isParcel ? h.parcelRefs?.split("·")[0]?.trim() ?? h.id : `hiša št. ${h.no}`,
      entitySi: isParcel
        ? `Parcelna vrstica: ${h.owner} — ${h.parcelRefs}`
        : `Hiša št. ${h.no} — ${h.owner}`,
      entityEn: isParcel
        ? `Parcel row: ${h.owner} — ${h.parcelRefs}`
        : `House no. ${h.no} — ${h.owner}`,
      entityId: h.id,
      state: owner ? "STRUCTURED_LINKED" : "STRUCTURED_UNRESOLVED",
      evidenceStatus: h.status,
      geometry: null,
      derivedCount: 1,
      openSi: owner
        ? h.museumRef
          ? null
          : "muzejska povezava ni utemeljena (ni vnosa v zbirki)"
        : `lastnik ni povezan v seznam lastnikov (PUA) — izvorni zapis ohranjen: ${h.owner}`,
      openEn: owner
        ? h.museumRef
          ? null
          : "museum link not substantiated (no collection record)"
        : `owner not linked in the owner register (PUA) — original row preserved: ${h.owner}`,
    });
  }

  // ——— PUA: abecedni seznam lastnikov (navzkrižna potrditev) ———
  for (const o of ATLAS_OWNERS) {
    const houseMatch = o.houseRefs.some((r) => ATLAS_HOUSES.some((h) => h.no === r));
    rows.push({
      unit: "N083PUA",
      locatorSi: o.puaRef ?? "lastniški model (strani A–B) — brez PUA potrditve",
      locatorEn: o.puaRef ?? "owners model (pages A–B) — without PUA confirmation",
      rowId: o.id,
      entitySi: `Lastnik: ${o.nameAsWritten}`,
      entityEn: `Owner: ${o.nameAsWritten}`,
      entityId: o.id,
      state: o.puaRef && houseMatch ? "CROSS_CHECKED" : "STRUCTURED_LINKED",
      evidenceStatus: o.status,
      geometry: null,
      derivedCount: 1,
      openSi: o.puaRef
        ? houseMatch
          ? null
          : "hišne številke iz PUA se ne ujemajo s PT (razrez vrstic)"
        : "ime iz PT (REVIEW); v PUA branju (49/49 strani) potrditev s to hišno št. ni bila najdena — številčenje PUA↔PT je dokazano deloma divergentno",
      openEn: o.puaRef
        ? houseMatch
          ? null
          : "house numbers from PUA do not match PT (row split)"
        : "name from PT (REVIEW); no confirmation with this house number found in the PUA reading (49/49 pages) — the PUA↔PT numbering is partly divergent (evidenced)",
    });
  }

  // ——— PUA nadaljevanje (strani 3–49, 101 vrstic, REVIEW — issue #4 popravljena oznaka) ———
  for (const r of PUA_CONTINUATION.rows) {
    rows.push({
      unit: "N083PUA",
      locatorSi: `stran ${r.page}, vrstica ${r.row}`,
      locatorEn: `page ${r.page}, row ${r.row}`,
      rowId: `pua-p${r.page}-r${r.row}`,
      entitySi: `Lastnik (PUA str. ${r.page}): ${r.nameAsWritten} — hiše: ${r.houseNos.join(", ") || "—"}`,
      entityEn: `Owner (PUA p. ${r.page}): ${r.nameAsWritten} — houses: ${r.houseNos.join(", ") || "—"}`,
      entityId: `pua-p${r.page}-r${r.row}`,
      state: "STRUCTURED_UNRESOLVED",
      evidenceStatus: PUA_CONTINUATION.status,
      geometry: null,
      derivedCount: 1,
      openSi: `strojni očrt (REVIEW, ${r.confidence}); del hišnih št. divergenten s PT (dokazano različno številčenje) — povezava čaka paleografijo`,
      openEn: `machine reading (REVIEW, ${r.confidence}); part of the house numbers diverge with PT (different numbering evidenced) — linking awaits palaeography`,
    });
  }

  // ——— PS: seznam zemljiških parcel (issue #4: prej preskočen — enota v poročilu NI smela manjkati) ———
  const psSeries = KURRENT_SERIES.find((k) => k.code === "PS");
  if (psSeries) {
    const psOpenRanges = psSeries.pagesReadList
      ? (() => {
          const readSet = new Set(psSeries.pagesReadList!);
          const missing: [number, number][] = [];
          let start: number | null = null;
          for (let p = 1; p <= psSeries.pages; p++) {
            if (!readSet.has(p)) {
              if (start == null) start = p;
            } else if (start != null) {
              missing.push([start, p - 1]);
              start = null;
            }
          }
          if (start != null) missing.push([start, psSeries.pages]);
          return missing.map(([a, b]) => (a === b ? `${a}` : `${a}–${b}`)).join(", ");
        })()
      : "";
    rows.push({
      unit: "N083PS",
      locatorSi: `strani 1–143 (P36: strojni prepis vseh strani — kampanja 5–139 + struktura/rekapitulacija 1–4, 140–143); odprto: ${psOpenRanges}`,
      locatorEn: `pages 1–143 (P36: machine transcription of all pages — the 5–139 campaign + structure/recapitulation 1–4, 140–143); open: ${psOpenRanges}`,
      rowId: "N083PS",
      entitySi: `Seznam zemljiških parcel — ${psSeries.structuredEntries} vrstic strojno prebranih (P36, dvoprehodno); kontrolna vsota 102+2505=2607 (str. 143)`,
      entityEn: `Register of land parcels — ${psSeries.structuredEntries} rows machine-read (P36, two passes); the checksum 102+2505=2607 (p. 143)`,
      entityId: null,
      state: "STRUCTURED_UNRESOLVED",
      evidenceStatus: psSeries.status,
      geometry: null,
      derivedCount: psSeries.structuredEntries,
      openSi: `sprava s kontrolno vsoto 2607: sekcije P38 (GRUND 1889/2505 + NADALJEVANJE 95 + WALDUNG 81 + Blatt X 60), razdvojitev v model parcela×raba P39 (2134 vnosov, 2632 parov, /api/atlas/ps-landuse) — še odprto: 3. prehod ~15 dvoumnih strani, primerjava z rekapitulacijo 140–143, paleografska potrditev; izrecno odprto, ne izgubljeno`,
      openEn: `the reconciliation against the checksum 2607: P38 sections (GRUND 1,889/2,505 + CONTINUATION 95 + WALDUNG 81 + Blatt X 60), split into the parcel×culture model P39 (2,134 entries, 2,632 pairs, /api/atlas/ps-landuse) — still open: a 3rd pass over ~15 ambiguous pages, comparison with the 140–143 recapitulation, palaeographic confirmation; explicitly open, not lost`,
    });
  }

  // ——— grafični listi: pokritost + vektorizirane entitete ———
  const sheetUnits = ATLAS_SOURCES.filter((s) => s.type === "cadastral-map" && s.code.startsWith("N083"));
  for (const s of sheetUnits) {
    const vectorised = s.code === "N083A02" ? VECTOR_BUILDINGS.length : 0;
    rows.push({
      unit: s.code,
      locatorSi: s.unit ?? "list",
      locatorEn: s.unit ?? "sheet",
      rowId: s.code,
      entitySi: vectorised
        ? `List ${s.unit} — ${vectorised} vektoriziranih stavbnih objektov`
        : `List ${s.unit} — digitalna kopija prenesena, vektorizacija parcel TO_COLLECT`,
      entityEn: vectorised
        ? `Sheet ${s.unit} — ${vectorised} vectorised building objects`
        : `Sheet ${s.unit} — digital copy transferred, parcel vectorisation TO_COLLECT`,
      entityId: vectorised ? "b1825-1…b1825-156" : null,
      state: vectorised ? "SHEET_VECTORISED" : "SHEET_TRANSFERRED",
      evidenceStatus: "RECONSTRUCTED",
      geometry: s.georefStatus === "GEOREFERENCED" ? "georeferenciran (afina, REVIEW)" : null,
      derivedCount: vectorised || 1,
      openSi: s.georefStatus === "GEOREFERENCED" ? null : "georeferenca lista še ni izdelana",
      openEn: s.georefStatus === "GEOREFERENCED" ? null : "sheet georeference not made yet",
    });
  }

  // ——— spisovne enote PG/PR/PV/PZ (issue #17: delno ali v celoti prebrane) ———
  for (const k of KURRENT_SERIES) {
    if (k.code === "PT" || k.code === "PUA" || k.code === "PS") continue;
    const unitCode = `N083${k.code}`;
    const fullyRead = k.pagesTranscribed >= k.pages;
    const structured = k.structuredEntries;
    rows.push({
      unit: unitCode,
      locatorSi: `${k.pagesTranscribed}/${k.pages} ${k.pages === 1 ? "strani" : "strani"}`,
      locatorEn: `${k.pagesTranscribed}/${k.pages} ${k.pages === 1 ? "page" : "pages"}`,
      rowId: unitCode,
      entitySi:
        structured > 0
          ? `${k.unitSi} — ${structured} strukturiranih zapisov (REVIEW, strojni očrt${fullyRead ? "; vse strani prebrane" : ""})`
          : `${k.unitSi} — enota je digitalizirana, vsebinskih zapisov ni strukturiranih`,
      entityEn:
        structured > 0
          ? `${k.unitEn} — ${structured} structured entries (REVIEW, machine-assisted${fullyRead ? "; all pages read" : ""})`
          : `${k.unitEn} — unit digitised, no content rows structured`,
      entityId: null,
      state: structured > 0 ? "STRUCTURED_LINKED" : "PENDING_TRANSCRIPTION",
      evidenceStatus: k.status,
      geometry: null,
      derivedCount: Math.max(1, structured),
      openSi: fullyRead
        ? `prepis je strojni (REVIEW) — paleografska potrditev čaka; nič ni izgubljeno`
        : `prepis ni zaključen (${k.pagesTranscribed}/${k.pages} strani, ${k.status}) — nič ni izgubljeno, enota čaka`,
      openEn: fullyRead
        ? `the transcription is machine-assisted (REVIEW) — palaeographic confirmation pending; nothing lost`
        : `transcription not finished (${k.pagesTranscribed}/${k.pages} pages, ${k.status}) — nothing lost, the unit awaits`,
    });
  }

  // ——— povzetki po enotah (issue #4: + scopeCheck iz inventarja) ———
  const inventory = getArchiveInventory();
  const unitCodes = [...new Set(rows.map((r) => r.unit))];
  const units: UnitRecon[] = unitCodes.map((code) => {
    const src = ATLAS_SOURCES.find((s) => s.code === code);
    const uRows = rows.filter((r) => r.unit === code);
    const structured = uRows.filter((r) => r.state !== "PENDING_TRANSCRIPTION" && r.state !== "SHEET_TRANSFERRED").length;
    const linked = uRows.filter((r) => r.state === "STRUCTURED_LINKED" || r.state === "CROSS_CHECKED" || r.state === "SHEET_VECTORISED").length;
    const unresolved = uRows.length - linked;
    const declared = src?.structuredEntries ?? 0;
    /** št. obdelanih zapisov vključuje izpeljane entitete (npr. 156 stavb z lista) */
    const processed = uRows.reduce((a, r) => a + r.derivedCount, 0);
    /* ISSUE #4: kontrola obsega izračunana iz INVENTARJA — dokazano prebrane
       strani + izrecno odprte strani morajo vsoti v deklarirane strani vira.
       To NI samoizpolnjujoče: declaredScope (structuredEntries) šteje vrstice,
       scopeCheck pa strani fonda — ločeni metriki, obe morata stati. */
    const inv = inventory.units.find((u) => u.code === code);
    const scopeAccounted = inv ? inv.scopeAccounted : true;
    return {
      code,
      titleSi: src?.titleSi ?? code,
      titleEn: src?.titleEn ?? code,
      vacUrl: src?.vacUrl ?? null,
      transferStatus: src?.transferStatus ?? null,
      georefStatus: src?.georefStatus ?? null,
      pages: src?.pages ?? null,
      declaredScope: declared,
      processedRows: processed,
      reportRows: uRows.length,
      structured,
      linked,
      unresolved,
      scopeCheck: {
        pagesDeclared: inv?.pagesDeclared ?? null,
        pagesRead: inv?.pagesRead ?? null,
        pagesOpen: inv?.pagesOpen ?? null,
        pagesOpenRangesSi: inv?.pagesOpenRangesSi ?? null,
        accounted: scopeAccounted,
      },
      /** zeroLoss (issue #4, dvojna kontrola): (1) obseg — VSE strani vira so
       *  dokazano prebrane ali izrecno zabeležene kot odprte (inventar);
       *  (2) vrstice — vsaka vrstica poročila ima status in razlog (lost = 0). */
      zeroLoss: scopeAccounted && processed >= declared,
    };
  });

  // ——— Kurrent sled: sken → stran → prepis → entiteta (+ različica) ———
  const kurrentTrail = KURRENT_SERIES.map((k) => ({
    code: k.code,
    scan: ptScan,
    pages: k.pages,
    pagesTranscribed: k.pagesTranscribed,
    chainSi: `sken N083${k.code} (VAČ IIIF) → ${k.pages} strani → prepis (REVIEW, strojni očrt) → ${k.structuredEntries} strukturiranih zapisov v Atlasu`,
    chainEn: `scan N083${k.code} (VAČ IIIF) → ${k.pages} pages → transcription (REVIEW, machine-assisted) → ${k.structuredEntries} structured entries in the Atlas`,
    version: DATA_VERSION,
    status: k.status,
  }));

  const linked = rows.filter(
    (r) => r.state === "STRUCTURED_LINKED" || r.state === "CROSS_CHECKED" || r.state === "SHEET_VECTORISED",
  ).length;
  const unresolved = rows.length - linked;
  /** izgubljeni = vrstice brez statusa/razloga — mora biti 0 */
  const lost = rows.filter((r) => !r.evidenceStatus || (!r.openSi && r.state === "STRUCTURED_UNRESOLVED")).length;

  return {
    generatedAt: new Date().toISOString(),
    dataVersion: DATA_VERSION,
    units,
    rows,
    totals: {
      originalRows:
        ATLAS_HOUSES.length + // PT hiše + PS parcele
        ATLAS_OWNERS.length + // PUA lastniki
        sheetUnits.length + // grafični listi
        KURRENT_SERIES.filter((k) => ["PG", "PR", "PV", "PZ"].includes(k.code)).length, // nereprepisane serije
      processedRows: rows.length,
      linked,
      unresolved,
      lost,
      sheetsVectorised: sheetUnits.filter((s) => s.code === "N083A02").length,
      sheetsTransferred: sheetUnits.length,
    },
    zeroLoss: lost === 0 && units.every((u) => u.zeroLoss),
    zeroLossMeaningSi:
      "zeroLoss = true potrjuje: (1) za VSAKO spisovno enoto N83 so vse deklarirane strani vira bodisi dokazano prebrane (pagesReadList iz surovih raziskav) bodisi izrecno zabeležene kot odprte z razlogom (scopeCheck) — brez tihih lukenj; (2) vsaka vrstica poročila ima status in razlog (lost = 0). zeroLoss NE potrjuje: da je prepis spravljen s kontrolno vsoto (P36: PS strani strojno prebrane — 2743 vrstic dvoprehodno; P38: sekcije spravljene, glavni niz 1889/2505; P39: razdvojitev v model parcela×raba 2134 vnosov — 3. prehod dvoumnih strani in primerjava z rekapitulacijo 140–143 ostajata odprti; PZ 59 strani odprtih), da so strojna branja dokaz (vse REVIEW), ali da obstajajo povezave hiša↔stavba (156 geometrij nima dokazanih hišnih št.).",
    zeroLossMeaningEn:
      "zeroLoss = true certifies: (1) for EVERY written N83 unit, all declared source pages are either evidenced as read (pagesReadList from the raw research) or explicitly recorded as open with a reason (scopeCheck) — no silent gaps; (2) every report row carries a state and a reason (lost = 0). zeroLoss does NOT certify: that the transcription is reconciled with the checksum (P36: the PS pages are machine-read — 2,743 rows in two passes; P38: sections reconciled, main series 1,889/2,505; P39: split into the parcel×culture model, 2,134 entries — a 3rd pass over ambiguous pages and the 140–143 recapitulation comparison remain open; PZ 59 pages open), that machine readings are evidence (all REVIEW), or that house↔building links exist (the 156 geometries carry no proven house numbers).",
    kurrentTrail,
  };
}
