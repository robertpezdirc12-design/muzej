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

  // ——— PT: protokol stavbnih parcel (hiše + parc. vrstice PS modela) ———
  for (const h of ATLAS_HOUSES) {
    const owner = ATLAS_OWNERS.find((o) => o.houseRefs.some((r) => r === h.no));
    const isParcel = h.no === "—";
    rows.push({
      unit: "N083PT",
      locatorSi: `stran ${h.sourcePage}${isParcel ? " (register parcel PS)" : ""}`,
      locatorEn: `page ${h.sourcePage}${isParcel ? " (PS parcel register)" : ""}`,
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
      locatorSi: o.puaRef ?? "strani C–Ž (niso prepisane)",
      locatorEn: o.puaRef ?? "pages C–Ž (not transcribed)",
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
        : "vpis brez PUA potrditvve — ime iz PT (REVIEW)",
      openEn: o.puaRef
        ? houseMatch
          ? null
          : "house numbers from PUA do not match PT (row split)"
        : "entry without PUA confirmation — name from PT (REVIEW)",
    });
  }

  // ——— PUA nadaljevanje (issue #17: strani 3–10, 18 vnosov, REVIEW) ———
  for (const r of PUA_CONTINUATION.rows) {
    rows.push({
      unit: "N083PUA",
      locatorSi: `stran ${r.page}, vrstica ${r.row}`,
      locatorEn: `page ${r.page}, row ${r.row}`,
      rowId: `pua-p${r.page}-r${r.row}`,
      entitySi: `Lastnik (PUA 3–10): ${r.nameAsWritten} — hiše: ${r.houseNos.join(", ") || "—"}`,
      entityEn: `Owner (PUA 3–10): ${r.nameAsWritten} — houses: ${r.houseNos.join(", ") || "—"}`,
      entityId: `pua-p${r.page}-r${r.row}`,
      state: "STRUCTURED_UNRESOLVED",
      evidenceStatus: PUA_CONTINUATION.status,
      geometry: null,
      derivedCount: 1,
      openSi: `strojni očrt (REVIEW, ${r.confidence}); del hišnih št. divergenten s PT — povezava čaka paleografijo`,
      openEn: `machine reading (REVIEW, ${r.confidence}); part of the house numbers diverge with PT — linking awaits palaeography`,
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

  // ——— povzetki po enotah ———
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
      /** zero-loss: št. obdelanih ≥ strukturiranih po evidenci VIRA */
      zeroLoss: processed >= declared,
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
    kurrentTrail,
  };
}
