"use client";

/**
 * RAZISKAVE IN PROVIENENCA (GitLab issue #3 — dopolnilo k Atlasu #2).
 *
 * Prikaz celotnega raziskovalnega stanja muzeja, izračunanega IZKLJUČNO
 * iz podatkov (research.ts, sources.ts, provenance.ts):
 *  - provenienčni audit vseh 113 zapisov (viri, licence, lokacije, statusi)
 *  - stanje prepisov Kurrent rokopisov (PT, PUA, PS, PZ, PR, PG, PV)
 *  - inventar javnih geodetskih virov za območje Griblje
 *  - šolski arhiv ZAL NME (4118864, 747512) + kronika (REVIEW)
 *  - Gaspari (TO_COLLECT), F0000212 (dokazna veriga), zemljevid 1812
 *  - ustna zgodovina (model, brez izmišljene vsebine)
 *  - negativni rezultati — nikoli izbrisani
 * Strojno berljivo: /api/provenance, /api/atlas/reconciliation, /api/opendata.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Archive,
  BookOpen,
  CheckCircle2,
  Crosshair,
  Database,
  ExternalLink,
  FileJson,
  FileX2,
  GraduationCap,
  Home,
  Landmark,
  Map as MapIcon,
  MapPin,
  MessageSquareQuote,
  Microscope,
  Search,
  ScrollText,
  Users,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { useLang } from "./language-context";
import { computeProvenanceAudit, countFlaggedRecords, DATA_VERSION } from "@/lib/provenance";
import { buildReconciliation } from "@/lib/reconciliation";
import {
  KURRENT_SERIES,
  GEODATA_SOURCES,
  SCHOOL_ARCHIVE,
  GASPARI_RESEARCH,
  F0000212_PROVENANCE,
  MAP_1812,
  ORAL_TOPICS,
  ORAL_INTERVIEWS,
  ARCHIVE_TRANSFER_ROWS,
  ARCHIVE_NON_TRANSFERS,
  ARCHIVE_TRANSFER_AUDIT,
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
import { ATLAS_SOURCES, NEGATIVE_RESULTS } from "@/data/atlas/sources";

const STATUS_STYLE: Record<string, string> = {
  VERIFIED: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
  DOCUMENTED: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100",
  REVIEW: "bg-orange-100 text-orange-900 dark:bg-orange-900/60 dark:text-orange-100",
  RECONSTRUCTED: "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100",
  INFERRED: "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100",
  APPROXIMATE: "bg-yellow-100 text-yellow-900 dark:bg-yellow-900/60 dark:text-yellow-100",
  TO_COLLECT: "bg-stone-100 text-stone-900 dark:bg-stone-800 dark:text-stone-100",
  NOT_FOUND: "bg-neutral-200 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300",
  NOT_PUBLIC: "bg-neutral-200 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300",
  TRANSFERRED: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
  GEOREFERENCED: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
  GRID_APPROX: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100",
  "NOT_DIGITIZED": "bg-neutral-200 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300",
  "NOT_APPLICABLE": "bg-neutral-100 text-neutral-600 dark:bg-neutral-800/60 dark:text-neutral-400",
};

function StatusBadge({ status }: { status: string }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 font-mono text-[10px] font-semibold tracking-wide ${
        STATUS_STYLE[status] ?? "bg-secondary text-secondary-foreground"
      }`}
    >
      {status}
    </span>
  );
}

type Tab = "audit" | "kurrent" | "geodata" | "sola" | "posebno" | "negativni" | "arhiv" | "vrzeli";

const TABS: { id: Tab; si: string; en: string; icon: React.ComponentType<{ className?: string }> }[] = [
  { id: "audit", si: "Provinienca 113", en: "Provenance 113", icon: Microscope },
  { id: "kurrent", si: "Prepisi Kurrent", en: "Kurrent transcriptions", icon: ScrollText },
  { id: "geodata", si: "Geodetski viri", en: "Geodetic sources", icon: MapIcon },
  { id: "sola", si: "Šolski arhiv", en: "School archive", icon: GraduationCap },
  { id: "posebno", si: "Posebne raziskave", en: "Special research", icon: Users },
  { id: "negativni", si: "Negativni rezultati", en: "Negative results", icon: FileX2 },
  { id: "arhiv", si: "Prenos iz arhiva", en: "Archive transfer", icon: Archive },
  { id: "vrzeli", si: "Zapolnjevanje vrzeli #17", en: "Gap closure #17", icon: Search },
];

export function MuseumResearch() {
  const { t, lang } = useLang();
  const [tab, setTab] = useState<Tab>("audit");

  const audit = computeProvenanceAudit();
  const flagged = countFlaggedRecords(audit);
  const recon = buildReconciliation();
  const n83 = ATLAS_SOURCES.filter((s) => s.code.startsWith("N083"));
  const kurrentPages = KURRENT_SERIES.reduce((a, s) => a + s.pages, 0);
  const kurrentDone = KURRENT_SERIES.reduce((a, s) => a + s.pagesTranscribed, 0);

  return (
    <section id="raziskave" className="scroll-mt-20 border-t border-border/60" aria-labelledby="raziskave-naslov">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 id="raziskave-naslov" className="font-display text-3xl font-semibold tracking-tight">
              {t("Raziskave in provenienca", "Research & provenance")}
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              {t(
                "Kakšna je dokazljivost zbirke? Vsak zgodovinski podatek ima status, vir in sled — nič ni izmišljeno, negativni rezultati ostanejo vidni.",
                "How provable is the collection? Every historical datum carries a status, a source and a trail — nothing is invented, negative results stay visible.",
              )}
            </p>
          </div>
          <div className="flex flex-col items-start gap-1 text-[11px] font-mono text-muted-foreground sm:items-end">
            <span>{t(`različica podatkov ${DATA_VERSION}`, `data version ${DATA_VERSION}`)}</span>
            <a href="/api/provenance" className="inline-flex items-center gap-1 text-primary hover:underline">
              <FileJson className="size-3" aria-hidden="true" /> /api/provenance
            </a>
          </div>
        </div>

        {/* zavihki */}
        <div className="mt-6 flex flex-wrap gap-2" role="tablist" aria-label={t("Raziskovalni pregledi", "Research views")}>
          {TABS.map(({ id, si, en, icon: Icon }) => {
            const active = tab === id;
            return (
              <button
                key={id}
                type="button"
                role="tab"
                aria-selected={active}
                onClick={() => setTab(id)}
                className={`inline-flex min-h-11 items-center gap-2 rounded-full border px-4 text-xs font-medium transition-colors ${
                  active
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-border bg-secondary/50 text-muted-foreground hover:border-primary/40 hover:text-foreground"
                }`}
              >
                <Icon className="size-3.5" aria-hidden="true" />
                {t(si, en)}
              </button>
            );
          })}
        </div>

        {/* ——— 1. PROVIENENČNI AUDIT 113 ZAPISOV ——— */}
        {tab === "audit" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4">
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {[
                { label: t("zapisov skupaj", "records total"), value: audit.totalRecords },
                { label: t("z vsaj enim virom", "with ≥ 1 source"), value: audit.sources.withAtLeastOneSource },
                { label: t("z neposrednim virom (URL)", "with a direct source (URL)"), value: audit.sources.withDirectSource },
                { label: t("s sliko", "with an image"), value: audit.images.withImage },
                { label: t("s kreditom slike", "with image credit"), value: audit.images.withImageCredit },
                { label: t("z GPS lokacijo", "with GPS location"), value: audit.locations.withGps },
                { label: t("vrstic virov", "source rows"), value: audit.sources.totalSourceRows },
                { label: t("z pomanjkljivostjo (flag)", "flagged records"), value: flagged },
              ].map((s) => (
                <div key={s.label} className="rounded-xl border bg-card p-4 shadow-sm">
                  <p className="font-display text-2xl font-semibold text-foreground">{s.value}</p>
                  <p className="mt-0.5 text-[11px] leading-tight text-muted-foreground">{s.label}</p>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <div className="rounded-xl border bg-card p-6 shadow-sm">
                <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                  <CheckCircle2 className="size-4 text-primary" aria-hidden="true" />
                  {t("Porazdelitev evidenceStatus", "evidenceStatus distribution")}
                </h3>
                <ul className="mt-4 space-y-2">
                  {Object.entries(audit.evidence.distribution).map(([k, v]) => (
                    <li key={k} className="flex items-center justify-between gap-2 text-sm">
                      <StatusBadge status={k} />
                      <span className="font-mono text-muted-foreground">
                        {v} · {Math.round((v / audit.totalRecords) * 100)} %
                      </span>
                    </li>
                  ))}
                </ul>
                {audit.evidence.unknownStatuses.length > 0 && (
                  <p className="mt-3 text-xs text-orange-700 dark:text-orange-300">
                    {t("neznan status:", "unknown status:")} {audit.evidence.unknownStatuses.join(", ")}
                  </p>
                )}
              </div>

              <div className="rounded-xl border bg-card p-6 shadow-sm">
                <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                  <Database className="size-4 text-primary" aria-hidden="true" />
                  {t(
                    `Licence virov (${audit.sources.totalSourceRows} navedb)`,
                    `Source licenses (${audit.sources.totalSourceRows} citations)`,
                  )}
                </h3>
                <ul className="mt-4 max-h-48 space-y-2 overflow-y-auto pr-2 text-sm">
                  {Object.entries(audit.sources.licenseDistribution)
                    .sort((a, b) => b[1] - a[1])
                    .map(([k, v]) => (
                      <li key={k} className="flex items-start justify-between gap-3">
                        <span className="min-w-0 break-words text-foreground/85" title={k}>
                          {k}
                        </span>
                        <span className="shrink-0 font-mono text-xs text-muted-foreground">{v}</span>
                      </li>
                    ))}
                </ul>
                <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
                  {t(
                    "Licenca CC BY-SA 4.0 velja samo za lastne metapodatke sklopa — vsak vir in slika ima svoje pravice (/api/opendata).",
                    "The CC BY-SA 4.0 license applies only to the dataset's own metadata — each source and image carries its own rights (/api/opendata).",
                  )}
                </p>
              </div>
            </div>

            {/* zastavice po zapisih */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Search className="size-4 text-primary" aria-hidden="true" />
                {t(
                  `Pomanjkljivosti po zapisih (${flagged} zapisov z vsaj eno)`,
                  `Flags by record (${flagged} records with at least one)`,
                )}
              </h3>
              <p className="mt-1 text-xs text-muted-foreground">
                {t(
                  "Vsaka pomanjkljivost je vidna — nič se ne skrije. Seznam je izračunan iz podatkov ob vsakem odpiranju.",
                  "Every deficiency is visible — nothing is hidden. The list is computed from the data on every load.",
                )}
              </p>
              <ul className="mt-4 max-h-72 space-y-1.5 overflow-y-auto pr-2">
                {audit.flags.map((f, i) => (
                  <li key={`${f.museumNo}-${f.flag}-${i}`} className="flex flex-wrap items-baseline gap-x-2 gap-y-0.5 text-xs">
                    <span className="font-mono font-semibold text-primary">{f.museumNo}</span>
                    <span className="font-mono text-[10px] text-muted-foreground/80">{f.flag}</span>
                    <span className="text-muted-foreground">{lang === "si" ? f.detailSi : f.detailEn}</span>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {/* ——— 2. PREPISI KURRENT ——— */}
        {tab === "kurrent" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4">
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <ScrollText className="size-4 text-primary" aria-hidden="true" />
                {t("Stanje prepisov nemških Kurrent rokopisov N83", "State of the German Kurrent N83 transcriptions")}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  `Skupaj ${kurrentPages} strani rokopisa; prepisanih ${kurrentDone}. Prioriteta po issue #3: PR, PS, PUA, PZ, nato ostale. Prepisi hranijo izvorno obliko, normalizirano obliko in status.`,
                  `${kurrentPages} manuscript pages in total; ${kurrentDone} transcribed. Priority per issue #3: PR, PS, PUA, PZ, then the rest. Transcriptions keep the original form, a normalised form and a status.`,
                )}
              </p>
              <ul className="mt-4 space-y-3">
                {KURRENT_SERIES.map((s) => (
                  <li key={s.code} className="rounded-lg border bg-secondary/30 p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="font-mono text-sm font-semibold text-primary">{s.code}</span>
                      <StatusBadge status={s.status} />
                    </div>
                    <p className="mt-1 text-sm font-medium text-foreground">
                      {lang === "si" ? s.unitSi : s.unitEn}
                    </p>
                    <div className="mt-2 flex items-center gap-3">
                      <Progress value={(s.pagesTranscribed / s.pages) * 100} className="h-1.5" aria-label={`${s.code} prepis`} />
                      <span className="shrink-0 font-mono text-[11px] text-muted-foreground">
                        {s.pagesTranscribed}/{s.pages} {t("str.", "pp.")}
                      </span>
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">
                      {lang === "si" ? s.noteSi : s.noteEn}
                    </p>
                  </li>
                ))}
              </ul>
            </div>

            {/* PS 1825 — sprava in model rabe tal (P38 + P39, issue #10) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <Microscope className="size-4 text-primary" aria-hidden="true" />
                {t("PS 1825 — sprava in model rabe tal (P38 + P39)", "PS 1825 — reconciliation & land-use model (P38 + P39)")}
                <StatusBadge status={PS_LANDUSE_P39.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Strojni prepis 135 strani (P36, 2743 vrstic) je spravljen po sekcijah (P38) in razdvojen v model po parcelah (P39) — deterministično, brez AI ob delovanju; surove rabe ostanejo nedotaknjene.",
                  "The machine transcription of 135 pages (P36, 2,743 rows) is reconciled by sections (P38) and split into a parcel-level model (P39) — deterministically, no AI at runtime; raw cultures stay untouched.",
                )}
              </p>

              {/* P38: pokritost glavnega niza */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P38 — glavni niz 1–2505 (GRUND)", "P38 — main series 1–2505 (GRUND)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_RECONCILIATION_P38.coverage.grundDistinct}/2505 · {PS_RECONCILIATION_P38.coverage.grundCoveragePct} %
                  </span>
                </div>
                <Progress
                  value={PS_RECONCILIATION_P38.coverage.grundCoveragePct}
                  className="mt-2 h-1.5"
                  aria-label="GRUND pokritost"
                />
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    `Sekcije: NADALJEVANJE_2506 ${PS_RECONCILIATION_P38.sections.NADALJEVANJE_2506?.distinctParcels ?? "—"} · WALDUNG ${PS_RECONCILIATION_P38.sections.WALDUNG?.distinctParcels ?? "—"} · Blatt X ${PS_RECONCILIATION_P38.sections.BLATT_X?.distinctParcels ?? "—"} (stavbna mesta, P36 cilj 102). P36 osnovna črta pod pravilom pass2wins reproducirana natanko.`,
                    `Sections: CONTINUATION_2506 ${PS_RECONCILIATION_P38.sections.NADALJEVANJE_2506?.distinctParcels ?? "—"} · WALDUNG ${PS_RECONCILIATION_P38.sections.WALDUNG?.distinctParcels ?? "—"} · Blatt X ${PS_RECONCILIATION_P38.sections.BLATT_X?.distinctParcels ?? "—"} (building plots, P36 target 102). The P36 baseline is reproduced exactly under the pass2wins rule.`,
                  )}
                </p>
              </div>

              {/* P39: model po parcelah */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P39 — model parcela × raba", "P39 — parcel × culture model")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_LANDUSE_P39.totals.rowsBefore} {t("vrstic", "rows")} → {PS_LANDUSE_P39.totals.modelEntries} {t("vnosov", "entries")}
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`${PS_LANDUSE_P39.totals.parcelEntries} parcel`, `${PS_LANDUSE_P39.totals.parcelEntries} parcels`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`${PS_LANDUSE_P39.totals.parcelCulturePairs} parov`, `${PS_LANDUSE_P39.totals.parcelCulturePairs} pairs`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`${PS_LANDUSE_P39.totals.parcelsWithMultipleCultures} × več rab`, `${PS_LANDUSE_P39.totals.parcelsWithMultipleCultures} multi-culture`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`${PS_LANDUSE_P39.totals.duplicateCultureRows} podvojenih rab`, `${PS_LANDUSE_P39.totals.duplicateCultureRows} duplicate cultures`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`${PS_LANDUSE_P39.totals.parcelEntriesEmptyCulture} sirot (brez rabe)`, `${PS_LANDUSE_P39.totals.parcelEntriesEmptyCulture} orphans (no culture)`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`${PS_LANDUSE_P39.totals.nebereznaRows} NEBEREŽNA`, `${PS_LANDUSE_P39.totals.nebereznaRows} UNREADABLE`)}
                  </span>
                </div>

                {/* klasifikacija rab — pravilnik v1 */}
                {(() => {
                  const C = PS_LANDUSE_P39.cultureClasses;
                  const clsLabels: Record<string, [string, string]> = {
                    NJIVA: ["njiva (Acker)", "arable (Acker)"],
                    TRAVNIK: ["travnik (Wiese)", "meadow (Wiese)"],
                    GOZD: ["gozd (Wald)", "forest (Wald)"],
                    PASTVISCE: ["pašnik (Weide)", "pasture (Weide)"],
                    STAVBNO: ["stavbna/gospodarska", "building/farm"],
                    VRT: ["vrt (Garten)", "garden (Garten)"],
                    ALM: ["planina (Alm)", "alpine pasture (Alm)"],
                    NEROD: ["nerodovoljna (Ödung)", "waste land (Ödung)"],
                    OBCINA: ["občinska (Gemeinde)", "communal (Gemeinde)"],
                    VINOGRAD: ["vinograd", "vineyard"],
                    CESTA: ["pot/cesta (Weg)", "path/road (Weg)"],
                  };
                  const clsColors: Record<string, string> = {
                    NJIVA: "#c9a35a",
                    TRAVNIK: "#9ec497",
                    GOZD: "#5a7a52",
                    PASTVISCE: "#b5c99a",
                    STAVBNO: "#a89c8a",
                    VRT: "#8fb573",
                    ALM: "#c4b39a",
                    NEROD: "#b3a28e",
                    OBCINA: "#93a8a0",
                    VINOGRAD: "#8e5a68",
                    CESTA: "#9b9485",
                  };
                  const rows = Object.entries(C.primaryCounts);
                  const max = rows.length ? rows[0][1] : 1;
                  return (
                    <div className="mt-3">
                      <p className="text-[11px] font-medium">
                        {t(
                          `Klasifikacija rab — pravilnik ${C.rulebookVersion} (brez AI): ${C.classifiedPairs} parov (${C.classifiedPct} %), preostalih ${C.unclassified.count} izrecno NEKLASIFICIRANO (${C.unclassified.distinctRaw} surovih vrednosti)`,
                          `Culture classification — rulebook ${C.rulebookVersion} (no AI): ${C.classifiedPairs} pairs (${C.classifiedPct} %), the remaining ${C.unclassified.count} explicitly UNCLASSIFIED (${C.unclassified.distinctRaw} raw values)`,
                        )}
                      </p>
                      <ul className="mt-2 space-y-1">
                        {rows.map(([cls, n]) => (
                          <li key={cls} className="flex items-center gap-2 text-[11px]">
                            <span className="w-40 shrink-0 truncate text-muted-foreground">
                              {(clsLabels[cls] ?? [cls, cls])[lang === "si" ? 0 : 1]}
                            </span>
                            <span className="h-2 min-w-0 flex-1 overflow-hidden rounded-full bg-muted">
                              <span
                                className="block h-full rounded-full"
                                style={{ width: `${(n / max) * 100}%`, backgroundColor: clsColors[cls] ?? "#a8a29e" }}
                              />
                            </span>
                            <span className="w-12 shrink-0 text-right font-mono text-muted-foreground">{n}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  );
                })()}

                <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    "Novosti nasproti P38: 7 sirot (parcela brez nobene rabe) izrecno v modelu, pravih parov parcela×raba 2632 (P38 »2118 parov« so v resnici vnosi po parcelah), 49 podvojenih rab ohranjenih. Strojno berljivo: /api/atlas/ps-landuse.",
                    "New against P38: 7 orphans (a parcel with no culture at all) are explicit in the model, the true parcel×culture pair count is 2,632 (P38's »2,118 pairs« are in fact parcel entries), 49 duplicate cultures preserved. Machine-readable: /api/atlas/ps-landuse.",
                  )}
                </p>
              </div>
            </div>

            {/* PS 1825 — rekapitulacija str. 140–143 (P40, issue #10) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <Microscope className="size-4 text-primary" aria-hidden="true" />
                {t("PS 1825 — rekapitulacija str. 140–143 (P40)", "PS 1825 — recapitulation pp. 140–143 (P40)")}
                <StatusBadge status={PS_RECAP_P40.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Kontrolne vsote str. 143 (rdeči tuš) so deterministično spravljene s spravnim modelom (P38 + P39) — brez AI ob delovanju; dvoumna branja ostanejo izrecno UNRESOLVED.",
                  "The page-143 control sums (red chalk) are deterministically reconciled with the land model (P38 + P39) — no AI at runtime; ambiguous readings stay explicitly UNRESOLVED.",
                )}
              </p>

              {/* P40: kontrolne vsote str. 143 */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P40 — kontrolna vsota str. 143", "P40 — page-143 control sum")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_RECAP_P40.recapitulation.summaBauplatze} + {PS_RECAP_P40.recapitulation.summaGrundparzellen} = {PS_RECAP_P40.recapitulation.zusammen}
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t("== P38 kontrolna vsota", "== P38 control sum")}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t("== 1889 + 616 (osnovna črta)", "== 1,889 + 616 (baseline)")}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`Blatt X ${PS_RECAP_P40.crossCheck.bauplatzeRegister.blattXRows}/102 (vrzel ${PS_RECAP_P40.crossCheck.bauplatzeRegister.gap})`, `Blatt X ${PS_RECAP_P40.crossCheck.bauplatzeRegister.blattXRows}/102 (gap ${PS_RECAP_P40.crossCheck.bauplatzeRegister.gap})`)}
                  </span>
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    "Rekapitulacija (rdeči tuš, str. 143) je natanko tista kontrolna vsota, ki jo sprava uporablja od P38. Blatt X (str. 138) pokrije 60/102 stavbnih mest — 42 je zunaj registra.",
                    "The recapitulation (red chalk, p. 143) is exactly the control sum the reconciliation has used since P38. Blatt X (p. 138) covers 60/102 building plots — 42 are outside the register.",
                  )}
                </p>
              </div>

              {/* P40: površine po sekcijah + kandidati */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P40 — površine po sekcijah modela", "P40 — areas by model section")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_RECAP_P40.areaDecomposition.rowsWithArea}+{PS_RECAP_P40.areaDecomposition.rowsWithoutArea} = 2632 vrstic
                  </span>
                </div>
                <div className="mt-2 space-y-1">
                  {Object.entries(PS_RECAP_P40.areaDecomposition.bySection).map(([sec, a]) => (
                    <div key={sec} className="flex flex-wrap items-center justify-between gap-2 font-mono text-[10px]">
                      <span className="rounded-full border bg-background px-2 py-0.5">{sec}</span>
                      <span className="text-muted-foreground">
                        {a.joch} Joch + {a.klafter.toLocaleString("de-DE")} Klafter = {a.jochEquivalent.toFixed(2)} Joch
                      </span>
                    </div>
                  ))}
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    `Summa ${PS_RECAP_P40.recapAreaAttribution.recapReading}(?) Joch (str. 141, branje izrecno negotovo) se najbolj sklada z GRUND-only: 1232,96 Joch (Δ +1,39 %). Podvajanje Blatt X površin ni dokazljivo (prekrivanje parov ${PS_RECAP_P40.blattXOverlap.pairsOverlap}/${PS_RECAP_P40.blattXOverlap.pairsBlattX}) — celotna vsota je samo zgornja meja. ${PS_RECAP_P40.fragmentRows140_141.count} per-house vrstic ostaja UNRESOLVED; številčni eho OVRGAN (2840 ≠ 2607). Strojno berljivo: /api/atlas/ps-recap.`,
                    `The ${PS_RECAP_P40.recapAreaAttribution.recapReading}(?) Joch total (p. 141, explicitly uncertain reading) best matches GRUND-only: 1,232.96 Joch (Δ +1.39%). Blatt X area duplication is unproven (pair overlap ${PS_RECAP_P40.blattXOverlap.pairsOverlap}/${PS_RECAP_P40.blattXOverlap.pairsBlattX}) — the whole-register sum is only an upper bound. ${PS_RECAP_P40.fragmentRows140_141.count} per-house rows remain UNRESOLVED; the numeric echo is REFUTED (2,840 ≠ 2,607). Machine-readable: /api/atlas/ps-recap.`,
                  )}
                </p>
              </div>
            </div>

            {/* PS 1825 — paleografija str. 140–143: Abschluß der Gemeinde (P41, issue #10) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <Microscope className="size-4 text-primary" aria-hidden="true" />
                {t("PS 1825 — paleografija str. 140–143: Abschluß der Gemeinde (P41)", "PS 1825 — palaeography pp. 140–143: Abschluß der Gemeinde (P41)")}
                <StatusBadge status={PS_RECAP_PALEO_P41.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "12 neodvisnih VLM prehodov (3×4 strani) + paleografska arbitracija iz povečanih izrezov; deterministična sprava brez AI ob delovanju. PRVIČ ujeta SKUPNA POVRŠINA OBČINE.",
                  "12 independent VLM passes (3×4 pages) + palaeographic arbitration from zoomed crops; deterministic reconciliation with no AI at runtime. The MUNICIPAL TOTAL AREA is captured for the first time.",
                )}
              </p>

              {/* P41: Area der Gemeinde */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P41 — Area der Gemeinde (rdeči tuš, str. 140)", "P41 — Area der Gemeinde (red chalk, p. 140)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_RECAP_PALEO_P41.abschluss.areaDerGemeinde} = {(1220 + 1493 / 1600).toFixed(4)} Joch
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t("1215|490 + 5|1003 = 1220|1493 ✓", "1,215|490 + 5|1,003 = 1,220|1,493 ✓")}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`model GRUND Δ +${(PS_RECAP_PALEO_P41.crossCheck.areaAttribution.preferred.deltaPct).toFixed(2)} %`, `GRUND model Δ +${(PS_RECAP_PALEO_P41.crossCheck.areaAttribution.preferred.deltaPct).toFixed(2)}%`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">{t("nadomešča P40 »Summa 1216(?)« (+1,39 %)", "supersedes P40 »Summa 1216(?)« (+1.39%)")}</span>
                </div>
              </div>

              {/* P41: 7 Grundstückslagen */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P41 — 7 Grundstückslagen (hiše 124–130)", "P41 — 7 Grundstückslagen (houses 124–130)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    = {PS_RECAP_PALEO_P41.lageSum.joch}|{PS_RECAP_PALEO_P41.lageSum.klafter} {t("(Summa der Grundparzellen)", "(Summa der Grundparzellen)")}
                  </span>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-1.5 font-mono text-[10px] sm:grid-cols-4">
                  {PS_RECAP_PALEO_P41.lageRows.map((r) => (
                    <span key={r.lage} className="rounded-full border bg-background px-2 py-0.5">
                      {r.lage}. {r.haus}: {r.joch}|{r.klafter}
                    </span>
                  ))}
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    "Vsota 7 vrstic je natanko 'Summa der Grundparzellen' (831|702) — P40 'naivna vsota 1413' razrešena kot P9 napaka branja (190/1168→830|1188, 286/8931→286|921, 198/11957→138|1457). Razcepi ostajajo izrecno UNRESOLVED: razcep K1/K2 v Abschlußu (K1+K2 = 2090), semantika par referenc (hipotezi OVRŽENI), spodnji vsotni blok str. 141 (šibko). Strojno berljivo: /api/atlas/ps-recap-paleo.",
                    "The 7-row sum is exactly the 'Summa der Grundparzellen' (831|702) — P40's 'naive sum 1,413' resolved as a P9 reading error (190/1168→830|1188, 286/8931→286|921, 198/11957→138|1457). Splits stay explicitly UNRESOLVED: the K1/K2 split in the Abschluß (K1+K2 = 2,090), pair-reference semantics (both hypotheses refuted), the p. 141 lower sum block (weak). Machine-readable: /api/atlas/ps-recap-paleo.",
                  )}
                </p>
              </div>
            </div>

            {/* PS 1825 — pravilnik rab v2 (P42, issue #10) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <Microscope className="size-4 text-primary" aria-hidden="true" />
                {t("PS 1825 — pravilnik rab v2 (P42)", "PS 1825 — land-use rulebook v2 (P42)")}
                <StatusBadge status={PS_LANDUSE_V2_P42.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "12 nespremenjenih v1 pravil + 13 priloženih (prvi zadetek = primarni razred); deterministično nad P39 modelom, brez AI ob delovanju. V2 ⊇ V1 — noben v1 razred ni spremenjen.",
                  "12 unchanged v1 rules + 13 appended (first match = primary class); deterministic over the P39 model, no AI at runtime. V2 ⊇ V1 — not a single v1 class changed.",
                )}
              </p>

              {/* P42: pokritost */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P42 — pokritost klasifikacije po parih", "P42 — pair classification coverage")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_LANDUSE_V2_P42.stats.v2ClassifiedPairs}/{PS_LANDUSE_V2_P42.stats.pairsTotal} {t("parov", "pairs")} = {PS_LANDUSE_V2_P42.stats.classifiedPctV2} % ({t("v1", "v1")} {PS_LANDUSE_V2_P42.stats.classifiedPctV1} %)
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`+${PS_LANDUSE_V2_P42.stats.v2ClassifiedPairs - PS_LANDUSE_V2_P42.stats.v1ClassifiedPairs} novih parov (13 pravil)`, `+${PS_LANDUSE_V2_P42.stats.v2ClassifiedPairs - PS_LANDUSE_V2_P42.stats.v1ClassifiedPairs} new pairs (13 rules)`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`TOPONIM ${PS_LANDUSE_V2_P42.toponym.pairs} (ni raba)`, `TOPONYM ${PS_LANDUSE_V2_P42.toponym.pairs} (not a use)`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`ARTIFAKT ${PS_LANDUSE_V2_P42.artifakt.pairs} (številke/opombe)`, `ARTIFACT ${PS_LANDUSE_V2_P42.artifakt.pairs} (numbers/notes)`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`NEKLASIFICIRANO ${PS_LANDUSE_V2_P42.stats.unresolvedPairs}`, `UNCLASSIFIED ${PS_LANDUSE_V2_P42.stats.unresolvedPairs}`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`pojasnjeno ${PS_LANDUSE_V2_P42.stats.explainedPctV2} %`, `explained ${PS_LANDUSE_V2_P42.stats.explainedPctV2}%`)}
                  </span>
                </div>
                <div className="mt-2 space-y-1">
                  {Object.entries(PS_LANDUSE_V2_P42.stats.primaryCountsV2).map(([cls, n]) => (
                    <div key={cls} className="flex items-center justify-between gap-2 font-mono text-[10px]">
                      <span className="rounded-full border bg-background px-2 py-0.5">{cls}</span>
                      <span className="text-muted-foreground">{n}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* P42: zaprte vrzeli v1 */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P42 — vrzeli v1, ki jih v2 zapira", "P42 — v1 gaps closed by v2")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">v1 12 + {PS_LANDUSE_V2_P42.rulebook.appendedRules.length} = 25 pravil</span>
                </div>
                <div className="mt-2 max-h-56 space-y-1 overflow-y-auto pr-1">
                  {PS_LANDUSE_V2_P42.rulebook.appendedRules.map((r) => (
                    <div key={r.no} className="flex flex-wrap items-center justify-between gap-2 rounded border bg-background px-2 py-1 font-mono text-[10px]">
                      <span className="text-muted-foreground">{r.no}. {r.class} [{r.confidence}]</span>
                      <span className="text-muted-foreground">+{r.pairs}</span>
                      <span className="basis-full text-[10px] leading-snug text-muted-foreground/80">{r.noteSi}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* P42: družine za paleografijo */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t(`P42 — ${PS_LANDUSE_V2_P42.families.length} neznanih družin (dokazi za paleografijo)`, `P42 — ${PS_LANDUSE_V2_P42.families.length} unknown families (evidence for palaeography)`)}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">{PS_LANDUSE_V2_P42.stats.unresolvedPairs} {t("parov", "pairs")}</span>
                </div>
                <div className="mt-2 max-h-56 space-y-1 overflow-y-auto pr-1">
                  {PS_LANDUSE_V2_P42.families.map((f) => (
                    <div key={f.id} className="rounded border bg-background px-2 py-1 text-[10px]">
                      <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                        <span className="font-semibold">{f.id}</span>
                        <span className="text-muted-foreground">{f.pairs} {t("parov", "pairs")} · so-odvisnost: {Object.keys(f.coParcel).length ? Object.entries(f.coParcel).map(([k, v]) => `${k} ${v}`).join(", ") : "—"}</span>
                      </div>
                      <p className="mt-0.5 leading-snug text-muted-foreground">{f.hypothesisSi}</p>
                    </div>
                  ))}
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    "Vse neznane družine ostajajo izrecno NEKLASIFICIRANE (ni ugibanj); so-odvisnost = primarne rabe na istih parcelah. TOPONIM = ležajna imena (Löwisch Thal, Leite …) — niso raba; ARTIFAKT vključuje številke 82–100 v stolpcu rabe na Blatt X — dodatni dokaz, da je Blatt X register stavbnih mest. Strojno berljivo: /api/atlas/ps-landuse-v2.",
                    "All unknown families remain explicitly UNCLASSIFIED (no guessing); co-occurrence = primary classes on the same parcels. TOPONYM = place names (Löwisch Thal, Leite …) — not a land use; ARTIFACT includes numbers 82–100 in the culture column on Blatt X — further evidence that Blatt X is the building-plot register. Machine-readable: /api/atlas/ps-landuse-v2.",
                  )}
                </p>
              </div>
            </div>

            {/* PS 1825 — neznane družine: prečni prehodi + PV sprava + leksikon (P43, issue #10) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <Microscope className="size-4 text-primary" aria-hidden="true" />
                {t("PS 1825 — neznane družine: prečni prehodi, PV sprava, leksikon (P43)", "PS 1825 — unknown families: cross-passes, PV reconciliation, lexicon (P43)")}
                <StatusBadge status={PS_LEXICON_P43.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Prečni prehodi SAMO znotraj iste fotografije (sken vsebuje ponovne posnetke); rabe se NE prireja — vse ostaja NEKLASIFICIRANO; leksikografske hipoteze so izrecno HIPOTEZE z viri, ki jih navaja stroj (NEPREVERJENI).",
                  "Cross-passes ONLY within the same photo (the scan contains re-shoots); no use is reassigned — everything remains UNCLASSIFIED; lexicographic hypotheses are explicitly HYPOTHESES with machine-attributed (UNVERIFIED) sources.",
                )}
              </p>

              {/* P43: prečni prehodi */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P43 — prečni prehodi po družinah", "P43 — cross-passes by family")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_LEXICON_P43.families.reduce((a, f) => a + f.pairs, 0)} + {PS_LEXICON_P43.singles.pairs} = 282 {t("parov NEKLASIFICIRANO", "pairs UNCLASSIFIED")}
                  </span>
                </div>
                <div className="mt-2 max-h-64 space-y-1 overflow-y-auto pr-1">
                  {PS_LEXICON_P43.families.map((f) => (
                    <div key={f.id} className="rounded border bg-background px-2 py-1 text-[10px]">
                      <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                        <span className="font-semibold">{f.id}</span>
                        <span className="text-muted-foreground">
                          {f.pairs} {t("parov", "pairs")} · {f.block.distinctPages === 1 ? t("1 fotografija", "1 photo") : `${f.block.distinctPages} ${t("fotografij", "photos")}`} · {t("teki", "runs")} {f.block.contiguousRuns}
                          {f.stablePairs > 0 ? ` · ${t("stabilnih", "stable")} ${f.stablePairs}` : ""}
                          {f.fallbackPairs > 0 ? ` · ${t("padcek", "fallback")} ${f.fallbackPairs}` : ""}
                        </span>
                      </div>
                      <p className="mt-0.5 leading-snug text-muted-foreground/80">
                        {Object.entries(f.variants).map(([k, v]) => `${k} ×${v}`).join(", ")}
                      </p>
                      {f.topHypotheses.length > 0 && (
                        <p className="mt-0.5 leading-snug text-muted-foreground/70">
                          {t("hipoteze", "hypotheses")}: {f.topHypotheses.map((h) => `${h.candidate} [${h.confidence}]`).join(" · ")}
                        </p>
                      )}
                    </div>
                  ))}
                  <div className="rounded border bg-background px-2 py-1 text-[10px]">
                    <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                      <span className="font-semibold">{t("KITICE", "STRAYS")}</span>
                      <span className="text-muted-foreground">{PS_LEXICON_P43.singles.pairs} {t("parov", "pairs")} · {PS_LEXICON_P43.singles.distinctRaw} {t("različnih", "distinct")} · {t("padcev", "fallbacks")} {PS_LEXICON_P43.singles.fallbackPairs}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* P43: PV sprava */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P43 — območna sprava s PV (Nutzungs-Ausweis 10. 1. 1825)", "P43 — area reconciliation with the PV (Nutzungs-Ausweis 10 Jan 1825)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    PV {PS_LEXICON_P43.pvReconciliation.pvTotalJ} J · {t("model", "model")} {PS_LEXICON_P43.pvReconciliation.rowsModelTotalJ} J
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`PV Area ≈ P41 Area (Δ 0,05 %)`, `PV Area ≈ P41 Area (Δ 0.05%)`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`VINOGRAD Δ ${PS_LEXICON_P43.pvReconciliation.vinogradVsWeinDeltaJ} J ✓`, `VINEYARD Δ ${PS_LEXICON_P43.pvReconciliation.vinogradVsWeinDeltaJ} J ✓`)}
                  </span>
                  <span className="rounded-full border bg-orange-600/10 px-2 py-0.5 text-orange-700 dark:text-orange-400">
                    {t(`WEIDEN-GAP ${PS_LEXICON_P43.pvReconciliation.weidenGapJ} J`, `PASTURE-GAP ${PS_LEXICON_P43.pvReconciliation.weidenGapJ} J`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`NJIVA +${PS_LEXICON_P43.pvReconciliation.njivaVsAeckerDeltaJ} J`, `FIELD +${PS_LEXICON_P43.pvReconciliation.njivaVsAeckerDeltaJ} J`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`TRAVNIK +${PS_LEXICON_P43.pvReconciliation.travnikVsWiesenDeltaJ} J`, `MEADOW +${PS_LEXICON_P43.pvReconciliation.travnikVsWiesenDeltaJ} J`)}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    {t(`model − Area = ${PS_LEXICON_P43.pvReconciliation.rowsModelVsPvTotalJ} J ≈ Blatt X + NAD + WALDUNG [~]`, `model − Area = ${PS_LEXICON_P43.pvReconciliation.rowsModelVsPvTotalJ} J ≈ Blatt X + NAD + WOODS [~]`)}
                  </span>
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    `Uradni izkaz navaja 636,16 J pašnikov (Weiden — belokranjske dubrave), izrecne Weide/Alm vrstice registra pa le ${PS_LEXICON_P43.pvReconciliation.psPastVisceAlmJ} J; neznane družine pokrijejo le ${PS_LEXICON_P43.pvReconciliation.unknownFamiliesAreaJ} J (17 %) vrzeli — preostanek leži v presežkih NJIVA/TRAVNIK nad uradnima kategorijama. PV »Walder« vrstica v transkripciji PRAZNA [?] — gozd uradni izkaz ne navaja, PS pa ima 76,79 J GOZD.`,
                    `The official return lists 636.16 J of pastures (Weiden — the White Carniolan oak woods), while the register's explicit Weide/Alm rows carry only ${PS_LEXICON_P43.pvReconciliation.psPastVisceAlmJ} J; unknown families cover only ${PS_LEXICON_P43.pvReconciliation.unknownFamiliesAreaJ} J (17%) of the gap — the remainder sits in the FIELD/MEADOW surpluses over the official categories. The PV »Walder« row is EMPTY in the transcription [?] — the official return lists no forest, while the PS has 76.79 J of FOREST.`,
                  )}
                </p>
              </div>
            </div>

            {/* PS 1825 — razcep K1/K2 (P44, issue #10) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <Microscope className="size-4 text-primary" aria-hidden="true" />
                {t("PS 1825 — razcep K1/K2: Abschluß der Gemeinde (P44)", "PS 1825 — the K1/K2 split: Abschluß der Gemeinde (P44)")}
                <StatusBadge status={PS_K1K2_P44.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Razcep iz P41 §21 je aritmetično razrešen [~]: K1 = 702, K2 = 1388 — celoten Abschluß se zapre. Rešitev je vsiljena z dvema neodvisnima korelacijama; človeška paleografska potrditev ostaja odprta.",
                  "The P41 §21 split is resolved arithmetically [~]: K1 = 702, K2 = 1388 — the entire Abschluß closes. The solution is forced by two independent corroborations; human palaeographic confirmation remains open.",
                )}
              </p>

              {/* P44: rešitev */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P44 — rešitev razcepa", "P44 — the split solution")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {t(`omejitev K1+K2 = ${PS_K1K2_P44.constraint.value} K`, `constraint K1+K2 = ${PS_K1K2_P44.constraint.value} K`)}
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    K1 = {PS_K1K2_P44.resolution.k1} {t("(831|702 == leva vsota)", "(831|702 == the left sum)")}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    K2 = {PS_K1K2_P44.resolution.k2} {t("(383|1388; branje pass2)", "(383|1388; pass2 reading)")}
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    831|702 + 383|1388 = 1215|490 ✓
                  </span>
                  <span className="rounded-full border bg-background px-2 py-0.5">
                    1215|490 + 5|1003 = 1220|1493 ✓
                  </span>
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    "Paralelnost 'nach Anlage': desna vrstica 4 (Baup 3|312) == leva vrstica 132 (3|312) — po istem vzorcu mora desna vrstica 1 (Grund 831|K1) rekapitulirati levo 'Summa der Grundparzellen' 831|702 (Joch 831 == 831). Hipoteza (968, 1122) pade: 831|968 bi presegla vsoto Anlage pri istem Joch — podmnožina ne more presegati nadmnožine.",
                    "The 'nach Anlage' parallelism: right row 4 (Baup 3|312) == left row 132 (3|312) — by the same pattern, right row 1 (Grund 831|K1) must recapitulate the left 'Summa der Grundparzellen' 831|702 (Joch 831 == 831). The (968, 1122) hypothesis falls: 831|968 would exceed the Anlage's own sum at the same Joch — a subset cannot exceed its superset.",
                  )}
                </p>
              </div>

              {/* P44: branja + hipoteze */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P44 — inventar branj in hipoteze", "P44 — reading inventory and hypotheses")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    H1 ✓ · H2–H5 ✗
                  </span>
                </div>
                <div className="mt-2 max-h-64 space-y-1 overflow-y-auto pr-1">
                  <div className="rounded border bg-background px-2 py-1 text-[10px]">
                    <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                      <span className="font-semibold">K1</span>
                      <span className="text-muted-foreground">
                        {Object.entries(PS_K1K2_P44.readingInventory.k1Cell.passes).map(([k, v]) => `${k}: ${v}`).join(" · ")} · {PS_K1K2_P44.readingInventory.k1Cell.visual}
                      </span>
                    </div>
                    <p className="mt-0.5 leading-snug text-muted-foreground/80">{PS_K1K2_P44.readingInventory.k1Cell.note}</p>
                  </div>
                  <div className="rounded border bg-background px-2 py-1 text-[10px]">
                    <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                      <span className="font-semibold">K2</span>
                      <span className="text-muted-foreground">
                        {Object.entries(PS_K1K2_P44.readingInventory.k2Cell.passes).map(([k, v]) => `${k}: ${v}`).join(" · ")} · {PS_K1K2_P44.readingInventory.k2Cell.visual}
                      </span>
                    </div>
                    <p className="mt-0.5 leading-snug text-muted-foreground/80">{PS_K1K2_P44.readingInventory.k2Cell.note}</p>
                  </div>
                  {PS_K1K2_P44.hypotheses.map((h) => (
                    <div key={h.id} className="rounded border bg-background px-2 py-1 text-[10px]">
                      <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                        <span className="font-semibold">{h.id}: K1={h.pair[0]}, K2={h.pair[1]} {h.accepted ? "✓" : "✗"}</span>
                        <span className="text-muted-foreground">{h.accepted ? t("sprejeta", "accepted") : t("zavrnjena", "rejected")}</span>
                      </div>
                      <p className="mt-0.5 leading-snug text-muted-foreground/70">
                        {h.accepted ? h.reasons[1] : h.rejection}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* P44: struktura občine */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("NOVA identiteta: ", "NEW identity: ")}</span>
                  {t(
                    "desna vrstica 1 (831|702) == leva 'Summa der Grundparzellen'. Struktura občine: rustikalne hiše po Anlagi 831|702 (hiše 124–130) + 'Ziffer 1041' (Gütl/gingl. kategorija) 383|1388 = 1215|490. Strojno berljivo: /api/atlas/ps-k1k2.",
                    "right row 1 (831|702) == the left 'Summa der Grundparzellen'. Gemeinde structure: rustical houses per the Anlage 831|702 (houses 124–130) + 'Ziffer 1041' (Gütl/gingl. category) 383|1388 = 1215|490. Machine-readable: /api/atlas/ps-k1k2.",
                  )}
                </p>
              </div>
            </div>

            {/* PS 1825 — verifikacija leksikografskih virov P43 (P45, issue #10) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <BookOpen className="size-4 text-primary" aria-hidden="true" />
                {t("PS 1825 — verifikacija leksikografskih virov (P45)", "PS 1825 — verification of the lexicographic sources (P45)")}
                <StatusBadge status={PS_LEXICON_VERIFIED_P45.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "49 tarč nad 70 hipotezami P43: direktni geslarski izseki (fran.si: SSKJ², Pleteršnik, Novak SSP), Wikipedia API (zvezčne mape DWB/Schmeller, bibliografija), deterministična preverba PV.json. 0/70 hipotez potrjenih v celoti — opozorilo P43 'viri navaja stroj, NEPREVERJENI' se potrdi. Nič ne spreminja hipotez ali rabe.",
                  "49 targets over the 70 P43 hypotheses: direct dictionary excerpts (fran.si: SSKJ², Pleteršnik, Novak SSP), Wikipedia API (DWB/Schmeller volume maps, bibliography), a deterministic check of PV.json. 0/70 hypotheses fully confirmed — the P43 warning 'machine-attributed, UNVERIFIED sources' is borne out. Nothing changes the hypotheses or the classification.",
                )}
              </p>

              {/* P45: pokritost */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P45 — izid kampanje", "P45 — campaign outcome")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_LEXICON_VERIFIED_P45.campaign.targetsTotal} {t("tarč", "targets")} · {PS_LEXICON_VERIFIED_P45.campaign.hypothesesTotal} {t("hipotez", "hypotheses")}
                  </span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">POTRJENO {PS_LEXICON_VERIFIED_P45.campaign.byVerdict.POTRJENO}</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">DELNO {PS_LEXICON_VERIFIED_P45.campaign.byVerdict.DELNO}</span>
                  <span className="rounded-full border bg-amber-100 px-2 py-0.5 dark:bg-amber-950/40">NEPOTRJENO {PS_LEXICON_VERIFIED_P45.campaign.byVerdict.NEPOTRJENO}</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">NEVERIFIKATORNO {PS_LEXICON_VERIFIED_P45.campaign.byVerdict.NEVERIFIKATORNO}</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">BREZ-VIRA {PS_LEXICON_VERIFIED_P45.campaign.byVerdict["BREZ-VIRA"]}</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">{t("fran.si", "fran.si")} {PS_LEXICON_VERIFIED_P45.campaign.byMethod["fran.si-direct"]} · wiki {PS_LEXICON_VERIFIED_P45.campaign.byMethod["wikipedia-api"]} · repo {PS_LEXICON_VERIFIED_P45.campaign.byMethod["deterministic-repo"]} · {t("nedosegljivo", "unreachable")} {PS_LEXICON_VERIFIED_P45.campaign.byMethod["unreachable"]}</span>
                </div>
              </div>

              {/* P45: ključne ugotovitve */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P45 — ključne ugotovitve", "P45 — key findings")}
                </span>
                <div className="mt-2 max-h-64 space-y-1 overflow-y-auto pr-1">
                  {PS_LEXICON_VERIFIED_P45.keyFindingsSi.map((f, i) => (
                    <p key={i} className="rounded border bg-background px-2 py-1 text-[10px] leading-snug text-muted-foreground/90">
                      {f}
                    </p>
                  ))}
                </div>
              </div>

              {/* P45: verifikacija po družinah */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P45 — verifikacija po družinah", "P45 — verification by family")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {PS_LEXICON_VERIFIED_P45.families.length}/16
                  </span>
                </div>
                <div className="mt-2 max-h-72 space-y-1 overflow-y-auto pr-1">
                  {PS_LEXICON_VERIFIED_P45.families.map((f) => (
                    <div key={f.id} className="rounded border bg-background px-2 py-1 text-[10px]">
                      <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                        <span className="font-semibold">{f.id}</span>
                        <span className="text-muted-foreground">
                          {f.pairs} {t("parov", "pairs")} · ✗{f.verdictCounts.NEPOTRJENO} ~{f.verdictCounts.DELNO} ?{f.verdictCounts.NEVERIFIKATORNO} —{f.verdictCounts["BREZ-VIRA"]}
                        </span>
                      </div>
                      <div className="mt-1 space-y-0.5">
                        {f.topHypotheses.map((h, hi) => (
                          <p key={hi} className="leading-snug text-muted-foreground/80">
                            <span className="font-mono">{h.verdict === "NEPOTRJENO" ? "✗" : h.verdict === "DELNO" ? "~" : "?"}</span>{" "}
                            <span className="font-medium">{h.candidate}</span> — {h.source}: {h.noteSi}
                          </p>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* P45: nepristranskost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Nepristranskost: ", "Fairness: ")}</span>
                  {t(
                    "kandidati/glose/viri P43 ostajajo bajtno identični (invarianta I2) — verifikacija samo presoji opornost citatov; rabe ni prirejena (282 parov NEKLASIFICIRANO). Kanonični URL za 16 nedosegljivih tarč v dokazih; strojno berljivo: /api/atlas/ps-lexicon-verified.",
                    "the P43 candidates/glosses/sources remain byte-identical (invariant I2) — verification only assesses the citations; no use reassigned (282 pairs UNCLASSIFIED). Canonical URLs for the 16 unreachable targets are in the evidence; machine-readable: /api/atlas/ps-lexicon-verified.",
                  )}
                </p>
              </div>
            </div>

            {/* Georeferenca N83 — neatline sidra dg/cg/ch (P46, issue #14) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Crosshair className="size-4 text-primary" aria-hidden="true" />
                {t("Georeferenca N83 — neatline sidra A03–A05 (P46)", "N83 georeference — neatline anchors A03–A05 (P46)")}
                <StatusBadge status={NEATLINE_GEOREF_P46.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Narisana neatline franciscejske sekcije = meja sekcije eZKN 1:2880. Uradna geometrija celic (GURS) je znana → preslikava px ↔ WGS84 brez prostih parametrov. Princip kalibriran na A02 (GEOTRUTH, EŠD 2122): residuala 9 in 13 m. Rezultat: A03–A05 iz GRID_APPROX (±200–400 m) na ±40–50 m — 4–8× izboljšanje.",
                  "The drawn neatline of a Franciscean section = the eZKN 1:2880 section boundary. The official cell geometry (GURS) is known → a px ↔ WGS84 mapping with no free parameters. The principle is calibrated on A02 (GEOTRUTH, EŠD 2122): residuals of 9 and 13 m. Result: A03–A05 upgraded from GRID_APPROX (±200–400 m) to ±40–50 m — a 4–8× improvement.",
                )}
              </p>

              {/* P46: kontrola principa + skupno merilo */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P46 — kontrola principa (A02) in skupno merilo", "P46 — principle control (A02) and shared scale")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">s̄ = {NEATLINE_GEOREF_P46.sharedScale.sbarMPerPx} m/px</span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                  <span className="rounded-full border bg-background px-2 py-0.5">A02 N: {NEATLINE_GEOREF_P46.control.residuals.top.residualM} m</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">A02 E: {NEATLINE_GEOREF_P46.control.residuals.right.residualM} m</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">sx = {NEATLINE_GEOREF_P46.sharedScale.sx} m/px</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">sy = {NEATLINE_GEOREF_P46.sharedScale.sy} m/px</span>
                  <span className="rounded-full border bg-background px-2 py-0.5">{t("medosna konsistenca", "axis consistency")} {NEATLINE_GEOREF_P46.sharedScale.axisConsistencyPct} %</span>
                </div>
              </div>

              {/* P46: listi */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P46 — listi: detekcija strani in nova meja", "P46 — sheets: side detection and new bounds")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">{t("premik vs P10 le 17–18 m", "shift vs P10 only 17–18 m")}</span>
                </div>
                <div className="mt-2 space-y-1">
                  {(Object.keys(NEATLINE_GEOREF_P46.sheets) as ("A03" | "A04" | "A05")[]).map((s) => {
                    const o = NEATLINE_GEOREF_P46.sheets[s];
                    const sides = Object.entries(o.sides);
                    return (
                      <div key={s} className="rounded border bg-background px-2 py-1.5 text-[10px]">
                        <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                          <span className="font-semibold">
                            {s} ({o.cell}) — {o.proposedStatus === "NEATLINE_GEOREFERENCED" ? t("zasidran", "anchored") : t("delno zasidran", "partially anchored")}
                          </span>
                          <span className="text-muted-foreground">
                            ±{o.uncertaintyM} m · {t("prej", "was")} ±{o.previous.uncertaintyM} m · {o.detectedSides}/4 {t("strani", "sides")}
                          </span>
                        </div>
                        <div className="mt-1 flex flex-wrap gap-1 font-mono text-[9px] text-muted-foreground">
                          {sides.map(([side, d]) => (
                            <span key={side} className={d.source === "detected" ? "rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40" : "rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40"}>
                              {side} {d.px} px {d.source === "detected" ? "✓" : "≈"}
                            </span>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* P46: ne-regresija */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P46 — ne-regresija: 7/7 P10 kontrolnih napisov", "P46 — non-regression: 7/7 P10 control labels")}
                </span>
                <div className="mt-2 max-h-44 space-y-1 overflow-y-auto pr-1">
                  {NEATLINE_GEOREF_P46.validations.map((v, i) => (
                    <p key={i} className="rounded border bg-background px-2 py-1 text-[10px] leading-snug text-muted-foreground/90">
                      <span className="font-mono text-emerald-700 dark:text-emerald-400">✓</span> <span className="font-mono">{v.label}</span> → {v.target}
                      {typeof v.distM === "number" ? ` — ${v.distM} m` : ""}
                    </p>
                  ))}
                </div>
              </div>

              {/* P46: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "SHEET_GEOREFS se namerno NE spreminja — rezultat je determinističen predlog nadgradnje (invarianti I1–I7), človeška potrditev detektiranih neatline črt pa ostaja odprta (lekcija P9: brez človeške potrditve ne objavljamo nadgradenj statusa). Strojno berljivo: /api/atlas/neatline-georef.",
                    "SHEET_GEOREFS is deliberately NOT changed — the result is a deterministic upgrade proposal (invariants I1–I7); human confirmation of the detected neatlines remains open (the P9 lesson: no status upgrades without human confirmation). Machine-readable: /api/atlas/neatline-georef.",
                  )}
                </p>
              </div>
            </div>

            {/* Georeferenca N83 — GURS parcel overlay (P47, issue #14) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Crosshair className="size-4 text-primary" aria-hidden="true" />
                {t("Georeferenca N83 — GURS parcel overlay (P47)", "N83 georeference — GURS parcel overlay (P47)")}
                <StatusBadge status={GURS_OVERLAY_P47.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Neodvisna validacija P46 neatline afin z zunanjim virom: sodobne katastrske parcele (GURS eZKN, KO 1544 + KO 1552) preslikane prek afin nazaj na skene morajo pasti na narisane črte 1825. Merimo pokritost črnila oboda in residual najboljšega zamika (±12 px); kontrole = isti obodi zamaknjeni 100–400 px v 8 smeri.",
                  "An independent validation of the P46 neatline affines with an external source: modern cadastral parcels (GURS eZKN, KO 1544 + KO 1552) mapped back onto the scans must fall on the drawn 1825 lines. We measure perimeter ink coverage and the best-shift residual (±12 px); controls = the same perimeters shifted 100–400 px in 8 directions.",
                )}
              </p>

              {/* P47: mediane residuala po listih */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P47 — mediana residuala registracije (DRAWN stratum)", "P47 — median registration residual (DRAWN stratum)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">{t("kontrola metode A02 (GEOTRUTH)", "method control A02 (GEOTRUTH)")}</span>
                </div>
                <div className="mt-2 space-y-1">
                  {(Object.keys(GURS_OVERLAY_P47.sheets) as ("A02" | "A03" | "A04" | "A05")[]).map((s) => {
                    const o = GURS_OVERLAY_P47.sheets[s];
                    return (
                      <div key={s} className="rounded border bg-background px-2 py-1.5 text-[10px]">
                        <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                          <span className="font-semibold">
                            {s} ({o.cell}) — {o.affineSource.startsWith("P46") ? t("P46 afina", "P46 affine") : t("GEOTRUTH meje", "GEOTRUTH bounds")}
                          </span>
                          <span className="text-muted-foreground">
                            {o.nDrawn} DRAWN · {o.nEmpty} EMPTY · {o.nInCell} {t("v celici", "in cell")}
                          </span>
                        </div>
                        <div className="mt-1 flex flex-wrap gap-1 font-mono text-[9px]">
                          <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">residual {o.drawn.residualM.median} m (p90 {o.drawn.residualM.p90} m)</span>
                          <span className="rounded border px-1.5 py-0.5">cov@0 {o.drawn.cov0.median}</span>
                          <span className="rounded border px-1.5 py-0.5">{t("najboljši", "best")} {o.drawn.covBest.median}</span>
                          <span className="rounded border px-1.5 py-0.5">{t("kontrola", "ctrl")} 200 px {o.controls["200"].median}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* P47: WAIDENDORF — land-use dokaz */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P47 — strata: A05/ch »Stab der Reambulierungs-Beimappe«", "P47 — strata: A05/ch 'Stab der Reambulierungs-Beimappe'")}
                </span>
                <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground/90">
                  {t(
                    "394/559 evalviranih parcel na A05 pada na v 1825 NENARISANE površine (lokalna gostota črnila < 0.06): velikanska skupna paša WAIDENDORF, označena s proslimi črkami sredi lista, + gozd. Nizka pokritost tam je pričakovana lastnost rabe tal (1825 paša → poznejša delitev), ne napaka registracije — kvantitativno dokumentiran dokaz o rabi na strani P43 (WEIDEN-GAP).",
                    "394/559 evaluated parcels on A05 fall on surfaces NOT drawn in 1825 (local ink density < 0.06): the giant common pasture WAIDENDORF, marked with spread letters across the sheet, plus forest. Low coverage there is an expected property of land use (1825 pasture → later subdivision), not a registration error — a quantitatively documented proof of land use on the P43 side (WEIDEN-GAP).",
                  )}
                </p>
              </div>

              {/* P47: izrezi za človeško potrditev */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P47 — dokazni izrezi za človeško potrditev (16)", "P47 — proof crops for human confirmation (16)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">research/issue17/neatline-crops/</span>
                </div>
                <div className="mt-2 max-h-32 space-y-1 overflow-y-auto pr-1">
                  {GURS_OVERLAY_P47.cropFiles.map((c) => (
                    <p key={c.file} className="rounded border bg-background px-2 py-1 font-mono text-[10px] leading-snug text-muted-foreground/90">
                      {c.file} — {c.kind === "neatline" ? (c.source === "detected" ? t("detektirana črta (rdeča)", "detected line (red)") : t("inferirana črta (oranžna, prekrimljena)", "inferred line (amber, dashed)")) : t("overlay sodobnih parcel (zelena)", "modern parcel overlay (green)")}
                    </p>
                  ))}
                </div>
              </div>

              {/* P47: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Overlay je neodvisna validacija P46 (mediana 5.6–9.8 m, p90 ≤ 13.2 m), a SHEET_GEOREFS se še naprej NAMERNO ne spreminja — človeška potrditev neatline črt prek izrezov ostaja pogoj nadgradnje (lekcija P9). Na gosto narisanih listih so kontrole-zamiki prav tako visoke (gosta risba) — zato je odločilna metrika residual. Strojno berljivo: /api/atlas/gurs-overlay.",
                    "The overlay is an independent validation of P46 (median 5.6–9.8 m, p90 ≤ 13.2 m), yet SHEET_GEOREFS still deliberately remains unchanged — human confirmation of the neatlines via the crops remains the upgrade condition (the P9 lesson). On densely drawn sheets the shift controls are also high (dense drawing) — hence the residual is the decisive metric. Machine-readable: /api/atlas/gurs-overlay.",
                  )}
                </p>
              </div>
            </div>

            {/* Georeferenca N83 — stavbni overlay (P48, issue #14) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Crosshair className="size-4 text-primary" aria-hidden="true" />
                {t("Georeferenca N83 — stavbni overlay: GURS stavbe ↔ stavbna mesta 1825 (P48)", "N83 georeference — building overlay: GURS buildings ↔ 1825 building sites (P48)")}
                <StatusBadge status={BUILDINGS_OVERLAY_P48.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Most PUA↔PT↔PS↔GURS: sodobni stavbni tlorisi (GURS eZKN WFS, SI.GURS.KN:STAVBE — KO 1544 401 + KO 1552 južni bbox 313) preslikani prek GEOTRUTH meja A02 / P46 afin A03–A05 nazaj na skene morajo pasti na narisane stavbne simbole 1825. Merimo pokritost črnila notranjosti+oboda na erodirani maski (tanke parcelne črte izginejo, polni simboli ostanejo) in residual najboljšega zamika (±12 px).",
                  "The PUA↔PT↔PS↔GURS bridge: modern building footprints (GURS eZKN WFS, SI.GURS.KN:STAVBE — KO 1544 401 + KO 1552 south bbox 313) mapped back through the A02 GEOTRUTH bounds / P46 affines must fall on the drawn 1825 building symbols. We measure interior+perimeter ink coverage on the eroded mask (thin parcel lines vanish, solid symbols survive) and the best-shift residual (±12 px).",
                )}
              </p>

              {/* P48: registracija po listih */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P48 — registracija na stavbni ravni (on-symbol = cov@best ≥ 0.5)", "P48 — building-level registration (on-symbol = cov@best ≥ 0.5)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">{t("714 stavb prenesenih", "714 buildings fetched")}</span>
                </div>
                <div className="mt-2 space-y-1">
                  {(Object.keys(BUILDINGS_OVERLAY_P48.sheets) as ("A02" | "A03" | "A04" | "A05")[]).map((s) => {
                    const o = BUILDINGS_OVERLAY_P48.sheets[s];
                    const os = o.onSymbol;
                    return (
                      <div key={s} className="rounded border bg-background px-2 py-1.5 text-[10px]">
                        <div className="flex flex-wrap items-center justify-between gap-2 font-mono">
                          <span className="font-semibold">
                            {s} ({o.cell}) — {o.affineSource.startsWith("P46") ? t("P46 afina", "P46 affine") : t("GEOTRUTH meje", "GEOTRUTH bounds")}
                          </span>
                          <span className="text-muted-foreground">
                            {o.nEvaluated} {t("evalviranih", "evaluated")} · {o.nDrawn} DRAWN · {o.nEmpty} EMPTY
                          </span>
                        </div>
                        <div className="mt-1 flex flex-wrap gap-1 font-mono text-[9px]">
                          {os.n > 0 && os.residualM ? (
                            <>
                              <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">on-symbol {os.n} ({Math.round((100 * os.n) / o.nEvaluated)}%)</span>
                              <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">residual {os.residualM.median} m (p90 {os.residualM.p90} m)</span>
                              <span className="rounded border px-1.5 py-0.5">cov@0 {os.cov0?.median}</span>
                              <span className="rounded border px-1.5 py-0.5">{t("najboljši", "best")} {os.covBest?.median}</span>
                            </>
                          ) : (
                            <span className="rounded border px-1.5 py-0.5 text-muted-foreground">
                              {s === "A03" ? t("brez sodobnih stavb v celici (dokumentirano)", "no modern buildings in the cell (documented)") : t("brez ujemanj — vse sodobne stavbe so novejše od risbe", "no matches — all modern buildings are younger than the map")}
                            </span>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* P48: kontinuiteta 1825 ↔ danes */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P48 — kontinuiteta stavbnih mest 1825 ↔ danes (list A02)", "P48 — building-site continuity 1825 ↔ today (sheet A02)")}
                </span>
                <div className="mt-2 flex flex-wrap gap-1 font-mono text-[9px]">
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{BUILDINGS_OVERLAY_P48.continuity.pairs} {t("parov tloris↔stavba ≤ 25 px", "footprint↔building pairs ≤ 25 px")}</span>
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{BUILDINGS_OVERLAY_P48.continuity.pairsStrong} strong</span>
                  <span className="rounded border px-1.5 py-0.5">{BUILDINGS_OVERLAY_P48.continuity.onSymbolWithoutVector} {t("na simbolih brez vektorizacije", "on symbols without vectorization")}</span>
                  <span className="rounded bg-red-100 px-1.5 py-0.5 dark:bg-red-950/40">{BUILDINGS_OVERLAY_P48.continuity.gone}/156 {t("tlorisov brez naslednika", "footprints without successor")}</span>
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground/90">
                  {t(
                    "Jedro vasi (Grüble, St. Veith) je stavbno kontinuirano: 149/154 sodobnih stavb v celici cf pada na narisane simbole 1825. Nasprotno pa 136 od 156 vektoriziranih tlorisov 1825 nima sodobne stavbe v bližini (mediana najbližje stavbe 392.6 px ≈ 316 m) — razpršena zidanica na zahodnih pobočjih (vinice, hambi) ni preživela. Nadgradja P16 present.json (OSM podlaga: 15 obstaja · 26 negotovih · 115 ni jih več) z uradnimi GURS obrisi — izvedeno v P54 (spodaj: 18/21/117, repla pravil 156/156).",
                    "The village core (Grüble, St. Veith) is building-continuous: 149/154 modern buildings in cell cf fall on the drawn 1825 symbols. Conversely, 136 of 156 vectorized 1825 footprints have no modern building nearby (median nearest 392.6 px ≈ 316 m) — the dispersed settlement on the western slopes (vineyard cottages, hambas) did not survive. An upgrade of P16 present.json (OSM basis: 15 existing · 26 uncertain · 115 gone) with official GURS footprints — carried out in P54 (below: 18/21/117, rules replay 156/156).",
                  )}
                </p>
              </div>

              {/* P48: Blatt X kvantitativna opomba */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P48 — Blatt X (str. 138–139): kvantitativna opomba k P40/P42", "P48 — Blatt X (pp. 138–139): a quantitative note on P40/P42")}
                </span>
                <div className="mt-2 flex flex-wrap gap-1 font-mono text-[9px]">
                  <span className="rounded border px-1.5 py-0.5">{BUILDINGS_OVERLAY_P48.blattX.rows} vrstic</span>
                  <span className="rounded border px-1.5 py-0.5">{BUILDINGS_OVERLAY_P48.blattX.inGrundRange41_2500}/{BUILDINGS_OVERLAY_P48.blattX.distinctHausNr} hausNr v razponu GRUND</span>
                  <span className="rounded bg-red-100 px-1.5 py-0.5 dark:bg-red-950/40">površine identične {BUILDINGS_OVERLAY_P48.blattX.areasIdentical}/{BUILDINGS_OVERLAY_P48.blattX.areasComparable} — REFRIRANA referenca</span>
                  <span className="rounded border px-1.5 py-0.5">mediana vrstic {BUILDINGS_OVERLAY_P48.blattX.medianAreaJoch} J vs dvorišča {BUILDINGS_OVERLAY_P48.blattX.grundHouseMedianJoch} J</span>
                  <span className="rounded border px-1.5 py-0.5">owner-številke vrstic 81–100: {BUILDINGS_OVERLAY_P48.blattX.b3OwnerNumeric}</span>
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground/90">
                  {t(
                    "'hausNr' stolpec Blatt X se sklada z razponom parcel GRUND (58/59), a površine vrstic se z register 1825 pri istih številkah NE ujemajo (0/37) — in so red velikosti nad tipičnimi dvorišči (mediana 6.3 vs 0.28 Joch). Skladno z opombo vrstice 1 'Zusammenstellung der Grundstücke', letnico 1860 v branjih in reambulacijskimi glavami listov je Blatt X verjetno poznejša zbirka parcel (reambulacija), NE register stavbnih mest — kvantitativna poprava P42 interpretacije (ARTIFAKT številke 82–100 = lastno štetje vrstic). Ostaja [~] do človeške paleografije.",
                    "The Blatt X 'hausNr' column aligns with the GRUND parcel range (58/59), yet row areas do NOT match the 1825 register at the same numbers (0/37) — and are an order of magnitude above typical curtilages (median 6.3 vs 0.28 Joch). Consistent with the row-1 note 'Zusammenstellung der Grundstücke', the year 1860 in the reads and the reambulation sheet headers, Blatt X is likely a LATER parcel compilation (reambulation), NOT a register of building sites — a quantitative correction of the P42 interpretation (the ARTIFAKT numbers 82–100 = the rows' own counting). Remains [~] until human paleography.",
                  )}
                </p>
              </div>

              {/* P48: izrezi */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P48 — dokazni izrezi (12)", "P48 — proof crops (12)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">research/issue17/buildings-crops/</span>
                </div>
                <div className="mt-2 max-h-32 space-y-1 overflow-y-auto pr-1">
                  {BUILDINGS_OVERLAY_P48.cropFiles.map((c) => (
                    <p key={c.file} className="rounded border bg-background px-2 py-1 font-mono text-[10px] leading-snug text-muted-foreground/90">
                      {c.file} — {c.kind === "continuity-pair" ? t(`par tloris↔stavba (${c.distPx} px)`, `footprint↔building pair (${c.distPx} px)`) : c.kind === "on-symbol" ? t("stavba na narisanim simbolom (zelena)", "building on drawn symbol (green)") : c.kind === "gone" ? t("tlorisi 1825 brez naslednika (rdeči)", "1825 footprints without successor (red)") : c.kind === "overview" ? t("pregled listov A02", "sheet A02 overview") : t("nove stavbe na nenarisanih površinah", "new buildings on undrawn surfaces")}
                    </p>
                  ))}
                </div>
              </div>

              {/* P48: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Kontinuiteta je prikazana na ravni so-lociranosti (≤ 25 px ≈ 20 m) — pari NISO potrjeni za posamezne domačije PT (za to bo potrebna humanca potrditev simbolov in številk na karti). Blatt X interpretacija je kvantitativna opomba, ne verdikt. SHEET_GEOREFS in dokazi P40–P47 nespremenjeni. Strojno berljivo: /api/atlas/buildings-overlay.",
                    "Continuity is shown at the co-location level (≤ 25 px ≈ 20 m) — pairs are NOT confirmed as individual PT homesteads (that will require human confirmation of the map symbols and numbers). The Blatt X interpretation is a quantitative note, not a verdict. SHEET_GEOREFS and the P40–P47 evidence unchanged. Machine-readable: /api/atlas/buildings-overlay.",
                  )}
                </p>
              </div>
            </div>

            {/* Georeferenca N83 — Fučkovci 1825 (P49, issue #14) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Crosshair className="size-4 text-primary" aria-hidden="true" />
                {t("Georeferenca N83 — Fučkovci 1825: dokazna sloja + obseg sklopa (P49)", "N83 georeference — Fučkovci 1825: evidence layers + cluster extent (P49)")}
                <StatusBadge status={FUCUKOVCI_P49.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Razširitev vektorizacije stavb 1825 na A05 (Fučkovci) — ugotovitev: celtna vektorizacija tlorisov NI izvedljiva (rožnati parcelni fill ima sivo ~169 < prag 195, erodirana maska se v vasi zasiči, številke/črki/drevesa so v istem kontrastnem razredu kot simboli). Namesto tega tri neodvisna deterministična dokazna sloja: modern-anchored mesta, striktna temna jedra s triažo in obseg sklopa.",
                  "Extending the 1825 building vectorization to A05 (Fučkovci) — the finding: full footprint vectorization is NOT feasible (pink parcel fill has gray ~169 < threshold 195, the eroded mask saturates inside the village, numbers/letters/trees share the contrast class of the symbols). Instead, three independent deterministic evidence layers: modern-anchored places, strict dark cores with triage, and the cluster extent.",
                )}
              </p>

              {/* P49: tri sloji */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P49 — tri neodvisna dokazna sloja (list A05 / celica ch)", "P49 — three independent evidence layers (sheet A05 / cell ch)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">scripts/p49_fucukovci1825.py</span>
                </div>
                <div className="mt-2 grid gap-1 text-[10px] sm:grid-cols-3">
                  <div className="rounded border bg-background px-2 py-1.5">
                    <div className="font-mono font-semibold">1) {t("modern-anchored", "modern-anchored")}</div>
                    <div className="mt-1 flex flex-wrap gap-1 font-mono text-[9px]">
                      <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{FUCUKOVCI_P49.modern.nOnSymbol} {t("mest z naslednikom", "places with successor")}</span>
                      <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{FUCUKOVCI_P49.cluster.onSymbolInCluster} {t("v sklopu", "in cluster")}</span>
                      <span className="rounded border px-1.5 py-0.5">residual {FUCUKOVCI_P49.modern.residualM} m</span>
                    </div>
                  </div>
                  <div className="rounded border bg-background px-2 py-1.5">
                    <div className="font-mono font-semibold">2) {t("striktna jedra", "strict cores")}</div>
                    <div className="mt-1 flex flex-wrap gap-1 font-mono text-[9px]">
                      <span className="rounded border px-1.5 py-0.5">{FUCUKOVCI_P49.strict.nSymbols} {t("jeder", "cores")}</span>
                      <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{FUCUKOVCI_P49.strict.nCorroborated} {t("koreliranih", "corroborated")}</span>
                      <span className="rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40">{FUCUKOVCI_P49.strict.nUnmatchedInCluster} {t("v sklopu neujemanih", "unmatched in cluster")}</span>
                    </div>
                  </div>
                  <div className="rounded border bg-background px-2 py-1.5">
                    <div className="font-mono font-semibold">3) {t("obseg sklopa", "cluster extent")}</div>
                    <div className="mt-1 flex flex-wrap gap-1 font-mono text-[9px]">
                      <span className="rounded border px-1.5 py-0.5">lupina {FUCUKOVCI_P49.cluster.hullAreaM2.toLocaleString("sl-SI")} m²</span>
                      <span className="rounded border px-1.5 py-0.5">{t("masa črnila", "ink mass")} {FUCUKOVCI_P49.cluster.inkMassPx.toLocaleString("sl-SI")} px</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* P49: sidro + skladnost s P10 */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P49 — P10 sidro in skladnost ocene števila stavb", "P49 — P10 anchor and building-count consistency")}
                </span>
                <div className="mt-2 flex flex-wrap gap-1 font-mono text-[9px]">
                  <span className="rounded border px-1.5 py-0.5">{t("sidro", "anchor")} ({FUCUKOVCI_P49.anchor.pxViaAffine[0]}, {FUCUKOVCI_P49.anchor.pxViaAffine[1]}) · odmik {FUCUKOVCI_P49.anchor.offsetPx} px</span>
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{t("najbližje mesto", "nearest place")} {FUCUKOVCI_P49.cluster.nearestOnSymbolToAnchorPx} px ≈ 38 m</span>
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{t("ocena", "estimate")} [{FUCUKOVCI_P49.estimate.lowerBound}, {FUCUKOVCI_P49.estimate.upperBound}] ⊇ P10 ~{FUCUKOVCI_P49.estimate.p10BuildingsVlm}</span>
                  <span className="rounded border px-1.5 py-0.5">GONE {FUCUKOVCI_P49.estimate.goneCandidatesBuilding} + {FUCUKOVCI_P49.estimate.goneCandidatesUnclear} [~]</span>
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{t("ohranjenost ≥", "survival ≥")} {FUCUKOVCI_P49.estimate.continuityLowerRatio}</span>
                </div>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground/90">
                  {t(
                    "26 sodobnih stavb pada na narisane simbole 1825 (residual mediana 9.8 m) — 25 v sklopu vasi = dokazana stavbna mesta z naslednikom (WGS84 v izpisu). Neodvisna striktna detekcija: 53 temnih jeder, 7 koreliranih, 19 neujemanih v sklopu — vizualna triaža pokaže 2 stavbi + 4 nejasne GONE-kandidate [~] (ostalo text/črta/drevo/številka). P10 ocena ~45 stavb je znotraj mej [27, 44] — brez protislovja; razlika = odzivnost detektorja (hatchirani simboli se staknejo z gostoto vasi). Jedro Fučkovcev je ohranjeno (ohranjenost ≥ 0.806 [~]) — v nasprotju z razpršeno zidanico A02 (P48: 136/156 brez naslednika).",
                    "26 modern buildings fall on the drawn 1825 symbols (residual median 9.8 m) — 25 inside the village cluster = proven building places with successors (WGS84 in the evidence file). Independent strict detection: 53 dark cores, 7 corroborated, 19 unmatched inside the cluster — visual triage shows 2 buildings + 4 unclear GONE candidates [~] (rest text/line/tree/number). The P10 estimate of ~45 buildings lies within the bounds [27, 44] — no contradiction; the difference is detector recall (hatched symbols merge with the village density). The Fučkovci core survived (survival ≥ 0.806 [~]) — unlike the A02 dispersed settlement (P48: 136/156 without successor).",
                  )}
                </p>
              </div>

              {/* P49: izrezi */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P49 — dokazni izrezi (9)", "P49 — proof crops (9)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">research/issue17/fucukovci-crops/</span>
                </div>
                <div className="mt-2 max-h-32 space-y-1 overflow-y-auto pr-1">
                  {FUCUKOVCI_P49.cropFiles.map((c) => (
                    <p key={c.file} className="rounded border bg-background px-2 py-1 font-mono text-[10px] leading-snug text-muted-foreground/90">
                      {c.file} — {c.kind === "pair" ? t(`modern-anchored mesto ↔ jedro (${c.distPx} px)`, `modern-anchored place ↔ core (${c.distPx} px)`) : c.kind === "cluster-overview" ? t("pregled sklopa: mesta + jedra + masa črnila + sidro", "cluster overview: places + cores + ink mass + anchor") : c.kind === "contact-sheet" ? t("kontaktni list vseh striktnih jeder", "contact sheet of all strict cores") : t("neujemana jedra v sklopu (GONE-kandidati, triaža)", "unmatched cores in cluster (GONE candidates, triage)")}
                    </p>
                  ))}
                </div>
              </div>

              {/* P49: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Celtna vektorizacija tlorisov na A05 NI izvedljiva — P49 dostavi dokazna sloja namesto popolnega seznama tlorisov. GONE-kandidati in ocena števila stavb ostajajo [~]: triaža jeder je razvojna presoja (provenienca v izpisu) in čaka potrditev lastnika prek kontaktnega lista. WGS84 koordinate 26 mest so vezane na sodobne stavbe (residual ~10 m), ne na neodvisno segmentacijo simbolov. SHEET_GEOREFS in dokazi P40–P48 nespremenjeni. Strojno berljivo: /api/atlas/fucukovci-1825.",
                    "Full footprint vectorization on A05 is NOT feasible — P49 delivers evidence layers instead of a complete footprint list. GONE candidates and the building-count estimate remain [~]: the core triage is a development-time judgment (provenance in the evidence file) and awaits owner confirmation via the contact sheet. The WGS84 coordinates of the 26 places are bound to modern buildings (residual ~10 m), not to independent symbol segmentation. SHEET_GEOREFS and the P40–P48 evidence unchanged. Machine-readable: /api/atlas/fucukovci-1825.",
                  )}
                </p>
              </div>
            </div>

            {/* Georeferenca N83 — zapora A03–A05 (P50, issue #14) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Crosshair className="size-4 text-primary" aria-hidden="true" />
                {t("Georeferenca N83 — zapora A03–A05: aktivacija P46 neatline afin (P50)", "N83 georeference — closure of A03–A05: activation of the P46 neatline affines (P50)")}
                <StatusBadge status={GEOREF_CLOSURE_P50.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "P50 aktivira P46 predlog nadgradnje: meje listov A03–A05 = narisane neatline = uradne meje celic eZKN 1:2880. Odločbo nosi 5 neodvisnih plasti dokazov, ki merijo isto afino (neatline kalibriran na A02/EŠD 2122, parcele P47, stavbe P48, sidro P49, napisi 7/7) — negotovost pada iz ±200–400 m na ±40–50 m (4–8× izboljšava), 5/5 listov serije je zdaj georeferenciranih.",
                  "P50 activates the P46 upgrade proposal: the bounds of sheets A03–A05 = the drawn neatlines = the official boundaries of the eZKN 1:2880 cells. The decision rests on 5 independent evidence layers measuring the same affine (neatline calibrated on A02/EŠD 2122, parcels P47, buildings P48, anchor P49, labels 7/7) — the uncertainty drops from ±200–400 m to ±40–50 m (a 4–8× improvement), and 5/5 sheets of the series are now georeferenced.",
                )}
              </p>

              {/* P50: plasti dokazov */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P50 — 5 neodvisnih plasti, ki merijo isto afino", "P50 — 5 independent layers measuring the same affine")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">scripts/p50_georef_closure.py</span>
                </div>
                <div className="mt-2 space-y-1">
                  {GEOREF_CLOSURE_P50.activation.basis.map((b, i) => (
                    <p key={i} className="rounded border bg-background px-2 py-1 font-mono text-[10px] leading-snug text-muted-foreground/90">
                      {b}
                    </p>
                  ))}
                </div>
              </div>

              {/* P50: per-sheet rezultati */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P50 — nove meje in statusi (SHEET_GEOREFS)", "P50 — new bounds and statuses (SHEET_GEOREFS)")}
                </span>
                <div className="mt-2 space-y-1">
                  {(["A03", "A04", "A05"] as const).map((k) => {
                    const s = GEOREF_CLOSURE_P50.sheets[k];
                    return (
                      <div key={k} className="rounded border bg-background px-2 py-1.5">
                        <div className="flex flex-wrap items-center gap-1 font-mono text-[9px]">
                          <span className="font-semibold">{k} · {s.cell}</span>
                          <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{s.status} ±{s.uncertaintyM} m</span>
                          <span className="rounded border px-1.5 py-0.5">{s.detectedSides}/4 {t("strani detektiranih", "sides detected")}</span>
                          <span className="rounded border px-1.5 py-0.5">{t("parcele", "parcels")} {s.parcelMedianM} m</span>
                          <span className="rounded border px-1.5 py-0.5">{t("premik vs P10", "shift vs P10")} {s.shiftVsP10M.max} m</span>
                          <span className="rounded border px-1.5 py-0.5">{s.scaleMPerPixel} m/px</span>
                          {k === "A05" && <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">26 {t("stavb on-symbol", "buildings on-symbol")}</span>}
                        </div>
                        <div className="mt-1 font-mono text-[9px] text-muted-foreground/80">
                          {s.boundsNeatlineNWSE[0].join(", ")} → {s.boundsNeatlineNWSE[1].join(", ")}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* P50: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Aktivacija sledi dogovorjenemu pravilu »če je dokaz, aktiviraj«: pogoj iz P46/P47 (človeška potrditev črt) je izpolnjen s tremi post-P46 neodvisnimi validacijami (parcele, stavbe, sidro). Vizualni pregled izrezov s strani lastnika ostaja priporočen [~]; nesoglasje → povratni commit (premik mej je le 17–18 m). Meje = neatline (celica), ne ovoj skena — robovi skena so v izpisu (boundsImageNWSE). Merilo ima ~1 % projekcijsko subtelnost (TM bbox vs geodetski rob) — vpliva le na ocene velikosti, ne na lege. A01/A02 (GEOTRUTH) nespremenjena. Strojno berljivo: /api/atlas/georef-closure.",
                    "The activation follows the agreed rule »if there is evidence, activate«: the P46/P47 condition (human confirmation of the lines) is fulfilled by three post-P46 independent validations (parcels, buildings, anchor). The owner's visual review of the crops remains recommended [~]; disagreement → a revert commit (the bounds shift is only 17–18 m). Bounds = the neatline (cell), not the scan envelope — scan corners are in the evidence (boundsImageNWSE). The scale carries ~1 % projection subtlety (TM bbox vs geodesic edge) — it affects size estimates only, not positions. A01/A02 (GEOTRUTH) unchanged. Machine-readable: /api/atlas/georef-closure.",
                  )}
                </p>
              </div>
            </div>

            {/* Georeferenca N83 — Leaflet overlay A03–A05 (P51, issue #14) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Crosshair className="size-4 text-primary" aria-hidden="true" />
                {t("Georeferenca N83 — Leaflet overlay A03–A05 (P51)", "N83 georeference — Leaflet overlay A03–A05 (P51)")}
                <StatusBadge status={LEAFLET_OVERLAY_P51.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "P51 aktivira P50 boundsImageNWSE v atlasnem UI: listi A03/A04/A05 kot slikovne prekrivke (privzeto izklopljene, skupna prosojnost, ob vsaki črtkani neatline okvir s statusom ±40/50 m). Ovoj skena je NEODVISNO preračunan iz P46 afine — ni ročno prepisanih koordinat. MERJENA SUBTELNOST: Leaflet ne podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir; odmik vogalov ≤ 20 m, dva vogala sta točna.",
                  "P51 activates the P50 boundsImageNWSE in the atlas UI: sheets A03/A04/A05 as image overlays (default off, shared opacity, each with a dashed neatline frame showing the ±40/50 m status). The scan envelope is INDEPENDENTLY recomputed from the P46 affine — no hand-copied coordinates. MEASURED SUBTLETY: Leaflet does not support rotated overlays — the image is stretched into an axis-aligned frame; corner deviation ≤ 20 m, two corners exact.",
                )}
              </p>

              {/* P51: per-sheet ovoji + odmiki */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P51 — ovoji skena (L.imageOverlay) in merjeni odmiki", "P51 — scan envelopes (L.imageOverlay) and measured deviations")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">scripts/p51_leaflet_overlay.py</span>
                </div>
                <div className="mt-2 space-y-1">
                  {(["A03", "A04", "A05"] as const).map((k) => {
                    const s = LEAFLET_OVERLAY_P51.sheets[k];
                    return (
                      <div key={k} className="rounded border bg-background px-2 py-1.5">
                        <div className="flex flex-wrap items-center gap-1 font-mono text-[9px]">
                          <span className="font-semibold">{k} · {s.cell} · {s.pixels.width}×{s.pixels.height}</span>
                          <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{s.status} ±{s.uncertaintyM} m</span>
                          <span className="rounded border px-1.5 py-0.5">skew {s.skewDeg}°</span>
                          <span className="rounded border px-1.5 py-0.5">odmik ≤ {s.overlayDeviationM.max} m (dva vogala točna)</span>
                        </div>
                        <div className="mt-1 font-mono text-[9px] text-muted-foreground/80">
                          {s.hullNWSE[0].join(", ")} → {s.hullNWSE[1].join(", ")} · {s.imageUrl} · sha256 {s.sha256.slice(0, 12)}…
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* P51: UI */}
              <div className="mt-3 rounded-lg border bg-secondary/30 p-3">
                <span className="text-sm font-semibold">
                  {t("P51 — aktivacija v UI", "P51 — UI activation")}
                </span>
                <div className="mt-2 space-y-1">
                  {LEAFLET_OVERLAY_P51.ui.toggles.map((tg) => (
                    <p key={tg} className="rounded border bg-background px-2 py-1 font-mono text-[10px] leading-snug text-muted-foreground/90">
                      stikalo »{tg}« — privzeto IZKLOPLJENO
                    </p>
                  ))}
                  <p className="rounded border bg-background px-2 py-1 font-mono text-[10px] leading-snug text-muted-foreground/90">
                    {LEAFLET_OVERLAY_P51.ui.neatlineFrames} · skupna prosojnost z A01/A02
                  </p>
                </div>
              </div>

              {/* P51: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Ovoj je preračunan iz P46 afine == P50 boundsImageNWSE (≤ 5e-6°) — en sam vir resnice (runtime JSON, ki ga uvažata UI in QA). MERJENA SUBTELNOST je poštno dokumentirana: Leaflet ne podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir pravega štirikotnika; odmik vogalov izmerjen iz členov afine (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m (dva vogala točna) — del ±40/50 m negotovosti lista. Skew ≤ 0.571° → osna postavitev je prikaz, ne meritev. Prekrivke so privzeto izklopljene — začetni pogled nespremenjen. Vizualni pregled s strani lastnika priporočen [~]. SHEET_GEOREFS in dokazi P40–P50 nespremenjeni. Strojno berljivo: /api/atlas/leaflet-overlay.",
                    "The envelope is recomputed from the P46 affine == P50 boundsImageNWSE (≤ 5e-6°) — a single source of truth (the runtime JSON imported by both UI and QA). The MEASURED SUBTLETY is honestly documented: Leaflet does not support rotated overlays — the image is stretched into an axis-aligned frame of the true quadrilateral; corner deviation measured from the affine terms (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m (two corners exact) — part of the sheet's ±40/50 m uncertainty. Skew ≤ 0.571° → the axis-aligned placement is a display, not a measurement. Overlays are default OFF — the initial view is unchanged. The owner's visual review recommended [~]. SHEET_GEOREFS and the P40–P50 evidence unchanged. Machine-readable: /api/atlas/leaflet-overlay.",
                  )}
                </p>
              </div>
            </div>

            {/* Kaj je izginilo? — present.json na uradnih GURS obriseh (P54, issue #12) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Home className="size-4 text-primary" aria-hidden="true" />
                {t("Kaj je izginilo? — present.json na uradnih GURS obriseh (P54)", "What has vanished? — present.json on official GURS footprints (P54)")}
                <StatusBadge status={PRESENT_GURS_P54.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "P54 nadgradi P16 primerjavo »1825 ∩ danes« z OSM posnetka na uradne GURS eZKN obrise (380 stavb v oknu A02 + sodobna vas, vse KO 1544 — popolna pokritost, tudi zahodna pobočja, kjer OSM posnetka sploh ni bilo). Pravila P16 so NESPREMENJENA — skript jih najprej kalibrira z replajo na starih podatkih (156/156, vključno z osmId in d), šele nato uporabi na uradnih obriseh.",
                  "P54 upgrades the P16 »1825 ∩ today« comparison from the OSM snapshot to official GURS eZKN footprints (380 buildings within the A02 + modern-village window, all KO 1544 — complete coverage, including the western slopes where the OSM snapshot had none at all). The P16 rules are UNCHANGED — the script first calibrates them by replay on the old data (156/156, including osmId and d), then applies them to the official footprints.",
                )}
              </p>

              {/* P54: števci + prehodi */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P54 — prehodi statusov (P16 OSM → P54 GURS)", "P54 — status transitions (P16 OSM → P54 GURS)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">scripts/p54_present_gurs.py</span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">🟢 {t("obstaja", "exists")} {PRESENT_GURS_P54.counts.exists} <span className="text-muted-foreground">(P16: {PRESENT_GURS_P54.countsP16.exists})</span></span>
                  <span className="rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40">🟡 {t("negotovo", "uncertain")} {PRESENT_GURS_P54.counts.uncertain} <span className="text-muted-foreground">(P16: {PRESENT_GURS_P54.countsP16.uncertain})</span></span>
                  <span className="rounded bg-red-100 px-1.5 py-0.5 dark:bg-red-950/40">🔴 {t("ni je več", "gone")} {PRESENT_GURS_P54.counts.gone} <span className="text-muted-foreground">(P16: {PRESENT_GURS_P54.countsP16.gone})</span></span>
                </div>
                <div className="mt-2 space-y-1 font-mono text-[11px]">
                  {Object.entries(PRESENT_GURS_P54.transitions).map(([k, v]) => (
                    <div key={k} className="rounded border bg-background px-2 py-1">
                      {k}: <span className="font-semibold">{v}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* P54: repla + navzkrižje P48 */}
              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Repla pravil (I1)", "Rules replay (I1)")}</p>
                  <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                    {t(
                      `Pravila P16 na starih OSM podatkih reproducirajo stare statuse ${PRESENT_GURS_P54.replay.pass} (+ osmId ${PRESENT_GURS_P54.replay.osmIdMatch}/41, d ±0.05 m) — pravila so pravilno prebrana, vir se spreminja, metoda ne.`,
                      `The P16 rules on the old OSM data reproduce the old statuses ${PRESENT_GURS_P54.replay.pass} (+ osmId ${PRESENT_GURS_P54.replay.osmIdMatch}/41, d ±0.05 m) — the rules are correctly read; the source changes, the method does not.`,
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Navzkrižje s P48 (I5)", "Cross-check with P48 (I5)")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    cf {PRESENT_GURS_P54.p48Cross.inCellCf} == modernEvaluated · pari ≤ 25 px {PRESENT_GURS_P54.p48Cross.pairs25px} == pairs ({PRESENT_GURS_P54.p48Cross.pairFootprints} tlorisov) · okno {PRESENT_GURS_P54.p48Cross.modernNear25pxWindow} stavb blizu tlorisa · {PRESENT_GURS_P54.p48Cross.mPerPx} m/px
                  </p>
                </div>
              </div>

              {/* P54: spremenjeni tlorisi */}
              <div className="mt-3 rounded-lg border bg-background p-3">
                <p className="text-xs font-semibold">{t("Spremenjeni tlorisi (7)", "Changed footprints (7)")}</p>
                <div className="mt-1 space-y-0.5 font-mono text-[11px] text-muted-foreground">
                  {PRESENT_GURS_P54.changed.map((c) => (
                    <div key={c.i}>
                      fp{c.i}: {c.p16} → <span className="font-semibold text-foreground">{c.p54}</span> (d {c.d} m)
                    </div>
                  ))}
                </div>
                <p className="mt-1 text-[11px] text-muted-foreground">
                  {t(
                    `d od P54 zapisana za vse 156 tlorisov (obstoja ≤ ${PRESENT_GURS_P54.dRanges.existsMax} m; ni je več do ${PRESENT_GURS_P54.dRanges.goneMax} m na zahodnih pobočjih).`,
                    `Since P54, d is recorded for all 156 footprints (exists ≤ ${PRESENT_GURS_P54.dRanges.existsMax} m; gone up to ${PRESENT_GURS_P54.dRanges.goneMax} m on the western slopes).`,
                  )}
                </p>
              </div>

              {/* P54: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Odsotnost stavbe še zmeraj NI dokaz porušitve — terenska preverba ostaja priporočena [~]. Pravila in P16 praga (8/20/40 m, prekrivanje 0.10) nespremenjena; spreminja se LE vir (OSM → uradni GURS eZKN) in pokritost (380 stavb namesto 350; Zahodna pobočja zdaj pokrita). Arhiv P16 OSM artefakta: research/issue17/present-osm-p16.json (bajtna kopija). Strojno berljivo: research/issue17/present-gurs.json + runtime src/data/atlas/present.json (uvaža village3d.ts).",
                    "Absence of a building still does NOT prove demolition — field verification remains recommended [~]. The rules and P16 thresholds (8/20/40 m, overlap 0.10) are unchanged; only the SOURCE changes (OSM → official GURS eZKN) and the coverage (380 buildings instead of 350; western slopes now covered). The P16 OSM artifact is archived: research/issue17/present-osm-p16.json (byte copy). Machine-readable: research/issue17/present-gurs.json + the runtime src/data/atlas/present.json (imported by village3d.ts).",
                  )}
                </p>
              </div>
            </div>

            {/* Geolokacija Grundparzellen — PS protokol 1825 ↔ parcele (P55, issue #13) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <MapPin className="size-4 text-primary" aria-hidden="true" />
                {t("Geolokacija Grundparzellen — PS protokol 1825 ↔ sodobne parcele (P55, v2 @ P58)", "Grundparzellen geolocation — PS protocol 1825 ↔ modern parcels (P55, v2 @ P58)")}
                <StatusBadge status={PS_GEO_P55.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "PS = »Protocol der Grund-Parcellen der Gemeinde GRÜBLE« (2505 Grundparzellen + 102 Bauplätze = 2607): lastniki, rabe, površine — brez geometrije. P55 protokol prvič geolocira: številke parcel se še vedno ujemajo s sodobnimi parcelami k.o. 1544 (delitve po 1825 = base + pripona). Vztrajnost oštevilčenja dokazana z dvema neodvisnima testoma. P58 (v2): produkcija sanirana — 43 lažnih S3 povezav odstranjenih (P56 dokaz), 26 Blatt I vrstic dodanih (P57 primarni vir).",
                  "PS = »Protocol der Grund-Parcellen der Gemeinde GRÜBLE« (2505 Grundparzellen + 102 Bauplätze = 2607): owners, uses, areas — no geometry. P55 geolocates the protocol for the first time: the parcel numbers still match the modern parcels of c.m. 1544 (post-1825 subdivisions = base + suffix). The numbering persistence is proven by two independent tests. P58 (v2): production sanitized — 43 false S3 links removed (P56 proof), 26 Blatt I rows added (P57 primary source).",
                )}
              </p>

              {/* P55: povezava + zaupanje */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P55 v2 — povezava in zaupanje vrstic (sanacija P58)", "P55 v2 — row linking and confidence (P58 sanitization)")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">scripts/p58_ps_parcels_geo_v2.py</span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{t("povezanih", "linked")} {PS_GEO_P55.join.matchedRows} <span className="text-muted-foreground">({PS_GEO_P55.join.matchedSharePct} % {t("+ 26 Blatt I izven izbora", "+ 26 Blatt I outside selection")})</span></span>
                  <span className="rounded bg-stone-100 px-1.5 py-0.5 dark:bg-stone-800">{t("parcel", "parcels")} {PS_GEO_P55.join.psPositionedParcels}</span>
                  <span className="rounded bg-stone-100 px-1.5 py-0.5 dark:bg-stone-800">{t("skupin s pripono", "suffix groups")} {PS_GEO_P55.join.suffixGroups}</span>
                  <span className="rounded bg-sky-100 px-1.5 py-0.5 dark:bg-sky-950/40">BI {PS_GEO_P55.join.seriesCounts.BI} · S1 {PS_GEO_P55.join.seriesCounts.S1} · S2 {PS_GEO_P55.join.seriesCounts.S2}</span>
                  <span className="rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40">−{PS_GEO_P55.v2Delta.removedRows} S3 · +{PS_GEO_P55.v2Delta.addedRows} BI</span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[11px]">
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">STRONG {PS_GEO_P55.join.confCounts.STRONG}</span>
                  <span className="rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40">MEDIUM {PS_GEO_P55.join.confCounts.MEDIUM}</span>
                  <span className="rounded bg-red-100 px-1.5 py-0.5 dark:bg-red-950/40">WEAK {PS_GEO_P55.join.confCounts.WEAK}</span>
                  <span className="text-muted-foreground">{t("(identifikacija posamezne parcele [~])", "(per-parcel identification [~])")}</span>
                </div>
              </div>

              {/* P55: dokaza vztrajnosti */}
              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Dokaz A — površine", "Proof A — areas")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    median modern/QK {PS_GEO_P55.areaProof.medianRatio} ≈ 1 Wiener QK {PS_GEO_P55.areaProof.historicalQkM2} m² (Δ +{PS_GEO_P55.areaProof.deltaPct} %) · {PS_GEO_P55.areaProof.pairsWithArea} parov · pas ±10 %: {(PS_GEO_P55.areaProof.tightShare * 100).toFixed(1)} % {t("proti", "vs")} {(PS_GEO_P55.areaProof.shuffleTightShare * 100).toFixed(1)} % ({t("naključno", "shuffled")}) · {t("kontrola", "control")} {PS_GEO_P55.areaProof.shuffleMedian}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Dokaz B — prostorska soslednost (odločilni)", "Proof B — spatial adjacency (decisive)")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {PS_GEO_P55.spatialProof.consecPairs} {t("zaporednih parov", "consecutive pairs")} · median {PS_GEO_P55.spatialProof.medianM} m ({t("naključno", "shuffled")} {PS_GEO_P55.spatialProof.shuffleMedianM} m — {PS_GEO_P55.spatialProof.enrichmentX}×) · {(PS_GEO_P55.spatialProof.share150 * 100).toFixed(1)} % ≤ 150 m ({t("naključno", "shuffled")} {(PS_GEO_P55.spatialProof.shuffleShare150 * 100).toFixed(1)} %)
                  </p>
                </div>
              </div>

              {/* P55: Furkofze odkritje */}
              <div className="mt-3 rounded-lg border bg-background p-3">
                <p className="text-xs font-semibold">{t("Odkritje: »Furkofze« (Fučkovci)", "Discovery: »Furkofze« (Fučkovci)")}</p>
                <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                  {t(
                    `Sekcija wohnort »Furkofze« = ${PS_GEO_P55.furkovce.rows} vrstici (parceli ${PS_GEO_P55.furkovce.parcels.join("/")}, lastnik ${PS_GEO_P55.furkovce.owner.join(", ")}) — prvi imenovani prebivalci Fučkovci v arhivu; obe parceli obstajata še danes (P47). ${PS_GEO_P55.furkovce.note}`, 
                    `The wohnort section »Furkofze« = ${PS_GEO_P55.furkovce.rows} rows (parcels ${PS_GEO_P55.furkovce.parcels.join("/")}, owner ${PS_GEO_P55.furkovce.owner.join(", ")}) — the first named inhabitants of Fučkovci in the archive; both parcels still exist (P47). ${PS_GEO_P55.furkovce.note}`,
                  )}
                </p>
              </div>

              {/* P55: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Vztrajnost oštevilčenja je dokazana na POPULACIJSKI ravni (površine + soslednost); identifikacija POSAMEZNE parcele ostaja [~] (šumne VLM površine Kurrent + delitve/renumbering po 1825) — zato zaupanje vsake vrstice razvrščeno (STRONG = oba dokaza). Omejitev: protokol je organiziran po listih z lastnim številčenjem (P39: ista številka na različnih listih = druga parcela) — join po sami številki vleče tudi čez-listske napačne povezave; per-Blatt ločitev ostaja odprta. Izbira strani: za 8 strani izbranih na pass3 uporabljen pass1 (pass3 parsed ni na voljo, številčno nezanesljivo — odmik od PS-full-v2 dokumentiran). SANACIJI IZVEDENI: P58 (v2) — 43 lažnih povezav S3 odstranjenih (nabor bajtno enak P56 seznamu) in 26 Blatt I vrstic dodanih (vseh 26 lostBases); P68 (v3, AKTUALNO) — 17 preslikav P67 forenzične specifikacije (dvojna Kurrent zamenjava p78/p93/p87) + re-join → 1079 vrstic / 798 števil; površinski median 3.8512, soslednost 590/51.8/28.3×. Zgodovina arhivirana (v1 + v2 dokaza, v2Delta/v3Delta); glej kartici P56/P57/P68. Strojno berljivo: research/issue17/ps-parcels-geo-v3.json + runtime src/data/atlas/ps-parcels-geo.json (/api/atlas/ps-parcels-geo).",
                    "The numbering persistence is proven at the POPULATION level (areas + adjacency); the identification of an INDIVIDUAL parcel remains [~] (noisy VLM Kurrent areas + post-1825 subdivisions/renumbering) — hence the per-row confidence tier (STRONG = both proofs). Limitation: the protocol is organized by sheets with their own numberings (P39: the same number on different sheets is a different parcel) — the number-only join also draws cross-sheet false links; the per-Blatt separation remains open. Page selection: pass1 used for the 8 pass3-chosen pages (pass3 has no parsed rows and is numerically unreliable — the deviation from PS-full-v2 is documented). SANITATIONS REALIZED: P58 (v2) — 43 false S3 links removed (the set byte-identical to the P56 list) and 26 Blatt I rows added (all 26 lostBases); P68 (v3, CURRENT) — 17 mappings of the P67 forensic specification (the double Kurrent substitution p78/p93/p87) + re-join → 1079 rows / 798 numbers; area median 3.8512, adjacency 590/51.8/28.3×. History archived (v1 + v2 evidences, v2Delta/v3Delta); see the P56/P57/P68 cards. Machine-readable: research/issue17/ps-parcels-geo-v3.json + the runtime src/data/atlas/ps-parcels-geo.json (/api/atlas/ps-parcels-geo).",
                  )}
                </p>
              </div>
            </div>

            {/* Topologija registra PS — serije, spremembe, sanacija P55 (P56, issue #13) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Landmark className="size-4 text-primary" aria-hidden="true" />
                {t("Topologija registra PS — serije, spremembe 1805–1934, sanacija P55 (P56)", "PS register topology — series, changes 1805–1934, P55 sanitization (P56)")}
                <StatusBadge status={REGISTER_TOPOLOGY_P56.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Register PS NI homogen: poleg glavnega registra (per-Blatt številčenje) vsebuje spremembni register (dodatki z anmerkung — »Vermessung 1805«, »Grundsteuerkataster 1841«) in zapadek »Zusammenstellung der Grundstücke« z lastnim oštevilčenjem 1–100 — ki ga je P55 join napačno povezal s sodobnimi parcelami. P56 kontaminacijo kvantificira, sanira in meritve neodvisno ponovi.",
                  "The PS register is NOT homogeneous: besides the main register (per-sheet numbering) it contains a changes register (annotated additions — »Vermessung 1805«, »Grundsteuerkataster 1841«) and the appendix »Zusammenstellung der Grundstücke« with its own numbering 1–100 — which the P55 join falsely linked to modern parcels. P56 quantifies and sanitizes the contamination with independent measurements.",
                )}
              </p>

              {/* P56: serije */}
              <div className="mt-4 rounded-lg border bg-secondary/30 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold">
                    {t("P56 — štiri serije registra", "P56 — four register series")}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground">scripts/p56_ps_register_topology.py</span>
                </div>
                <div className="mt-2 grid gap-1.5 font-mono text-[11px] sm:grid-cols-2">
                  <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">
                    S1 {t("glavni register", "main register")} {REGISTER_TOPOLOGY_P56.topology.S1.pages} ({REGISTER_TOPOLOGY_P56.topology.S1.pageCount} {t("str.", "pp.")}) · {REGISTER_TOPOLOGY_P56.topology.S1.numMin}–{REGISTER_TOPOLOGY_P56.topology.S1.numMax}
                  </span>
                  <span className="rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40">
                    S2 {t("spremembni register", "changes register")} {REGISTER_TOPOLOGY_P56.topology.S2.pages} ({REGISTER_TOPOLOGY_P56.topology.S2.pageCount} {t("str.", "pp.")}) · {REGISTER_TOPOLOGY_P56.topology.S2.numMin}–{REGISTER_TOPOLOGY_P56.topology.S2.numMax}
                  </span>
                  <span className="rounded bg-red-100 px-1.5 py-0.5 dark:bg-red-950/40">
                    S3 {t("zapadek", "appendix")} {REGISTER_TOPOLOGY_P56.topology.S3.pages} · {REGISTER_TOPOLOGY_P56.topology.S3.numMin}–{REGISTER_TOPOLOGY_P56.topology.S3.numMax} ({t("lastno oštevilčenje", "own numbering")})
                  </span>
                  <span className="rounded bg-stone-100 px-1.5 py-0.5 dark:bg-stone-800">
                    S4 {t("rekapitulacija + Abschluß (str. 140–143)", "recapitulation + Abschluß (pp. 140–143)")}
                  </span>
                </div>
              </div>

              {/* P56: sanacija */}
              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Sanacija P55 — lažne povezave S3", "P55 sanitization — false S3 links")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {REGISTER_TOPOLOGY_P56.contamination.s3RowsMatched} {t("lažnih povezav", "false links")} ({REGISTER_TOPOLOGY_P56.contamination.s3RowsTotal} {t("vrstic S3", "S3 rows")}) · median modern/QK {REGISTER_TOPOLOGY_P56.contamination.ratioMedianS3} ≪ {REGISTER_TOPOLOGY_P56.contamination.ratioMedianS1} (S1) · ~{Math.round(REGISTER_TOPOLOGY_P56.contamination.ratioMedianS1 / REGISTER_TOPOLOGY_P56.contamination.ratioMedianS3)}× {t("odmik od 1 QK", "off 1 QK")} {REGISTER_TOPOLOGY_P56.contamination.historicalQkM2} m² · pass2 [1..40] vs pass3 [421..440]
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Sanitiran join", "Sanitized join")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {REGISTER_TOPOLOGY_P56.sanitization.matchedRowsBefore} → {REGISTER_TOPOLOGY_P56.sanitization.matchedRowsAfter} {t("vrstic", "rows")} · {t("base", "bases")} {REGISTER_TOPOLOGY_P56.sanitization.uniqueBasesBefore} → {REGISTER_TOPOLOGY_P56.sanitization.uniqueBasesAfter} (−{REGISTER_TOPOLOGY_P56.sanitization.lostBasesCount}: št. 1–40, {t("str. 3–4 niso prebrane", "pp. 3–4 not read")}) · median {REGISTER_TOPOLOGY_P56.sanitization.ratioMedianAfter}
                  </p>
                </div>
              </div>

              {/* P56: dvoumnost + praznina + časovnica */}
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Per-Blatt dvoumnost (merjeno)", "Per-sheet ambiguity (measured)")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {REGISTER_TOPOLOGY_P56.perBlattAmbiguity.basesOnMultiplePages} {t("base na več straneh", "bases on multiple pages")} ({REGISTER_TOPOLOGY_P56.perBlattAmbiguity.withinS1} {t("znotraj S1", "within S1")}) · {REGISTER_TOPOLOGY_P56.perBlattAmbiguity.cleanRowsWithAmbiguousBase} {t("vrstic dvoumnih [~]", "ambiguous rows [~]")} · {t("brez prerazporeditev", "no reassignments")}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Sodobna praznina 2507–2607", "Modern void 2507–2607")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    0 {t("parcel", "parcels")} ({REGISTER_TOPOLOGY_P56.modernVoid.psRows} PS {t("dodatkov", "additions")}) {t("proti", "vs")} {REGISTER_TOPOLOGY_P56.modernVoid.contModernCount} base / {REGISTER_TOPOLOGY_P56.modernVoid.contParcelsCount} {t("parcelam", "parcels")} {REGISTER_TOPOLOGY_P56.modernVoid.contRange.join("–")} · {t("vzrok [~]", "cause [~]")}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Časovnica sprememb", "Timeline of changes")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {REGISTER_TOPOLOGY_P56.timeline.annotatedRows} {t("označenih vrstic", "annotated rows")} · {REGISTER_TOPOLOGY_P56.timeline.earliest}–{REGISTER_TOPOLOGY_P56.timeline.latest} · {t("pik", "peak")} {REGISTER_TOPOLOGY_P56.timeline.topYear}: {REGISTER_TOPOLOGY_P56.timeline.topYearRows} {t("vrstic", "rows")} / {REGISTER_TOPOLOGY_P56.timeline.pages1841Count} {t("strani", "pages")} (Grundsteuerkataster)
                  </p>
                </div>
              </div>

              {/* P56: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Vse vrednosti so MERITVE nad committed artefakti (P55 evidence, ps-raw branja, PS-full-v2 adjudikacije, P47 parcele) — nič ni ugibano in nič ni prerazporejeno: S3 zapadek je odstranjen iz joina z dvema dokazoma (pass-razhajanje + površine ~42× off), per-Blatt instanci pa ostajata dvoumni [~] (4. VLM prehod na glave listov IZVEDEN v P59 — od 211 dvoumnih base jih 110 sega čez ≥2 Blatta (P62 polna pokritost), 17 ruleCandidate; join še naprej nespremenjen, glej kartico P59). P55 runtime (ps-parcels-geo.json) je od P58 SANIRAN v v2 — 43 lažnih S3 povezav odstranjenih (nabor bajtno enak spodnjemu seznamu) in 26 Blatt I vrstic dodanih (P57) → 1093 vrstic; glej kartico P55 v2. Letnice anmerkung so per-row [~] VLM branja (1515/1522 najverjetneje navedbe starih urbarijev). Strojno berljivo: research/issue17/ps-register-topology.json + runtime src/data/atlas/ps-register-topology.json (/api/atlas/ps-register-topology).",
                    "All values are MEASUREMENTS over committed artifacts (P55 evidence, ps-raw reads, PS-full-v2 adjudications, P47 parcels) — nothing guessed, nothing reassigned: the S3 appendix is removed from the join with two proofs (pass disagreement + areas ~42× off), while per-sheet instances remain ambiguous [~] (the 4th VLM pass on leaf headers was DONE in P59 — of 211 ambiguous bases 110 span ≥2 Blaetter (P62 full coverage), 17 ruleCandidates; the join remains unchanged, see the P59 card). Since P58 the P55 runtime (ps-parcels-geo.json) is SANITIZED to v2 — 43 false S3 links removed (the set byte-identical to the list below) and 26 Blatt I rows added (P57) → 1093 rows; see the P55 v2 card. The anmerkung years are per-row [~] VLM readings (1515/1522 most likely references to old urbaria). Machine-readable: research/issue17/ps-register-topology.json + the runtime src/data/atlas/ps-register-topology.json (/api/atlas/ps-register-topology).",
                  )}
                </p>
              </div>

              {/* P57 zapora: strani 3–4 prebrane */}
              <div className="mt-3 rounded-lg border border-amber-200 bg-amber-50/60 p-3 dark:border-amber-900/50 dark:bg-amber-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("NADGRADNJA v P57: ", "SUPERSEDED IN P57: ")}</span>
                  {t(
                    "strani 3–4 (številke 1–40 glavnega registra) so ZDAJ prebrane s štirimi plastmi — vseh 26 izgubljenih base je obnovljenih s primarnim virom (Blatt I); glej kartico P57.",
                    "pp. 3–4 (numbers 1–40 of the main register) are NOW read in four layers — all 26 lost bases are restored from the primary source (Blatt I); see the P57 card.",
                  )}
                </p>
              </div>
            </div>

            {/* P57 — začetek registra PS: strani 3–4, številke 1–40, Blatt I (issue #13) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <BookOpen className="size-4 text-primary" aria-hidden="true" />
                {t("Začetek registra PS — strani 3–4, številke 1–40, obnova 26 base (P57)", "PS register opening — pp. 3–4, numbers 1–40, restoration of 26 bases (P57)")}
                <StatusBadge status={PS_REGISTER_START_P57.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Strani 3–4 protokola (začetek glavnega registra, Blatt I) — ki jih P38/P56 izbora nista vključila — so prebrane s ŠTIRIMI neodvisnimi plastmi in deterministično adjudicirane; join po mehaniki P55 obnovi TOČNO vseh 26 base, ki jih je P56 moral sanirati (edini vir teh številk je bil zapadek str. 138–139). Veriga Blatt I 1–60 je zaprta (committed ps-005 začne 41).",
                  "Pages 3–4 of the protocol (the main register opening, Blatt I) — omitted by the P38/P56 selections — were read in FOUR independent layers and deterministically adjudicated; the join by the P55 mechanics restores EXACTLY the 26 bases P56 had to drop (whose only source was the pp. 138–139 appendix). The Blatt I chain 1–60 is closed (committed ps-005 starts at 41).",
                )}
              </p>

              {/* P57: plasti branja */}
              <div className="mt-3 rounded-lg border bg-background p-3">
                <p className="text-xs font-semibold">{t("Štiri plasti branja (glm-5v-turbo)", "Four reading layers (glm-5v-turbo)")}</p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  {t("polna stran", "full page")} ×{PS_REGISTER_START_P57.readMeta.fullPasses} · {t("kolone Haus Nro.", "Haus Nro. columns")} ×{PS_REGISTER_START_P57.readMeta.colsPasses} (3× {t("izrez", "crop")}) · {t("izrezi površin", "area crops")} ×{PS_REGISTER_START_P57.readMeta.areasPasses} (LCS) · {t("celice 6×", "6× cells")} ×{PS_REGISTER_START_P57.readMeta.cellsArbitration} ({PS_REGISTER_START_P57.readMeta.disputedCells} {t("spornih", "disputed")})
                </p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  {t("adjudikacija", "adjudication")}: {PS_REGISTER_START_P57.adjudication.layersStrong} {t("vrstic izrezi+polna", "rows areas+full")} · {PS_REGISTER_START_P57.adjudication.layersCells} {t("celic [~]", "cells [~]")} · {PS_REGISTER_START_P57.adjudication.hausNr2of3} Haus Nro. 2/3
                </p>
              </div>

              {/* P57: obnova + testi */}
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Obnova lostBases P56", "Restoration of P56 lostBases")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {PS_REGISTER_START_P57.restoration.restored}/{PS_REGISTER_START_P57.restoration.lostBasesP56} {t("obnovljenih", "restored")} ({PS_REGISTER_START_P57.restoration.restoredWithArea} {t("z območji", "with areas")}, {PS_REGISTER_START_P57.restoration.numberOnly} {t("samo številka", "number only")}) · {t("zaupanje", "confidence")} STRONG {PS_REGISTER_START_P57.restoration.confidence.STRONG} / MEDIUM {PS_REGISTER_START_P57.restoration.confidence.MEDIUM} / WEAK {PS_REGISTER_START_P57.restoration.confidence.WEAK} · {PS_REGISTER_START_P57.restoration.retiredUnmatched} {t("upokojenih številk", "retired numbers")}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Test (A) površine", "Test (A) areas")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    median modern/QK {PS_REGISTER_START_P57.areas.medianM2K} ≈ {PS_REGISTER_START_P57.areas.histQkM2} ({PS_REGISTER_START_P57.areas.deltaPct > 0 ? "+" : ""}{PS_REGISTER_START_P57.areas.deltaPct} %) · {t("kontrola", "control")} {PS_REGISTER_START_P57.areas.controlMedian} (2.4× {t("dlje", "farther")}) · {t("pas ±10 %", "±10 % band")}: {Math.round(PS_REGISTER_START_P57.areas.bandShareObserved * 100)} % vs {Math.round(PS_REGISTER_START_P57.areas.controlBandShare * 100)} %
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Test (B) soslednost", "Test (B) adjacency")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {PS_REGISTER_START_P57.adjacency.pairs} {t("parov", "pairs")} · median {PS_REGISTER_START_P57.adjacency.medianM} m ({Math.round(PS_REGISTER_START_P57.adjacency.share150 * 100)} % ≤ 150 m) · {t("kontrola", "control")} {PS_REGISTER_START_P57.adjacency.controlMedian} m ({PS_REGISTER_START_P57.adjacency.controlRatio}×), MIN {PS_REGISTER_START_P57.adjacency.controlMinM} m &gt; {t("opaženi", "observed")} — Monte-Carlo 100 %
                  </p>
                </div>
              </div>

              {/* P57: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Vse vrednosti so MERITVE nad committed artefakti (21 novih ps-raw datotek + P55 mehanika + P47 parcele) — nič ni prepisano na slepo: 10 spornih celic odločenih s tarčnimi 6× izrezi (r40 z odločanjem 3/3 = 413), Haus Nro. iz kolonskih izrezov (polnostransko branje je sistematično mešalo dvomestne številke s črkami); r1/r28 celici površin PRAZNI na originalu; vsotni vrsti ('Fürtrag') delno berljivi [~]; 14 številk brez sodobne naslednice = upokojene s konsolidacijo [~]; identifikacija posamezne parcele ostaja [~] (strojno branje ni dokazni vir). P55/P56 runtime nespremenjena (pini qa-p55/p56). Strojno berljivo: research/issue17/ps-register-start.json + runtime src/data/atlas/ps-register-start.json (/api/atlas/ps-register-start).",
                    "All values are MEASUREMENTS over committed artifacts (21 new ps-raw files + the P55 mechanics + P47 parcels) — nothing copied blindly: 10 disputed cells decided with targeted 6× crops (r40 tie-broken 3/3 = 413), Haus Nro. from column crops (the full-page reading systematically confused two-digit numbers with letters); the r1/r28 area cells are BLANK on the original; the carry-forward ('Fürtrag') rows partly legible [~]; 14 numbers without a modern successor = retired by consolidation [~]; per-parcel identification remains [~] (machine reading is not an evidentiary source). The P55/P56 runtimes are unchanged (qa-p55/p56 pins). Machine-readable: research/issue17/ps-register-start.json + the runtime src/data/atlas/ps-register-start.json (/api/atlas/ps-register-start).",
                  )}
                </p>
              </div>
            </div>

            {/* P59 — glave listov registra PS: Nro. des Blattes (issue #13) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <BookOpen className="size-4 text-primary" aria-hidden="true" />
                {t("Glave listov registra PS — Nro. des Blattes (P59)", "PS register leaf headers — Nro. des Blattes (P59)")}
                <StatusBadge status={BLATT_HEADERS_P59.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Prvo zanesljivo branje stolpca »Nro. des Blattes«: levi izrez 135 strani × 2 neodvisna prehoda + 25 arbitraž agent-oči na 3× izrezih (stari P38 blatt stolpec potrjeno šumen). Rezultat: Blatt I = parcele 1–800, Blatt II se začne pri 801; isto številka pod različnima Blattoma = druga parcela (P39) — per-Blatt ločitev 211 dvoumnih base v2 je ZDAJ MERLJIVA. Join ostaja nespremenjen (meritve brez prerazporeditev).",
                  "First reliable reading of the 'Nro. des Blattes' column: left-strip crops of 135 pages × 2 independent passes + 25 agent-eye arbitrations on 3× crops (the old P38 blatt column confirmed noisy). Result: Blatt I = parcels 1–800, Blatt II starts at 801; the same number under different Blaetter = a different parcel (P39) — the per-Blatt disambiguation of the 211 ambiguous v2 bases is now MEASURABLE. The join remains unchanged (measurements without reassignments).",
                )}
              </p>

              {/* P59: pokritost + metoda */}
              <div className="mt-3 rounded-lg border bg-background p-3">
                <p className="text-xs font-semibold">{t("Metoda in pokritost", "Method and coverage")}</p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  {t("izrezi levega stolpca", "left-strip crops")} 135 × 3× Lanczos · 2 {t("prehoda", "passes")} (glm-5v-turbo) · {BLATT_HEADERS_P59.arbitration.agreementPages} {t("strani soglasja", "agreement pages")} · <span className="rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40">{BLATT_HEADERS_P59.arbitration.pagesArbitrated} {t("arbitraža-oči", "agent-eye arbitrations")}</span> · {t("polna pokritost 135/135 × 2 (P62)", "full coverage 135/135 × 2 (P62)")}
                </p>
              </div>

              {/* P59: struktura Blatt */}
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Blatt I", "Blatt I")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {t("parcele", "parcels")} 1–800 · {t("strani", "pages")} 3–40 · {t("prehodna cona", "transition zone")} 721–800: popravki I→II [~] (p40/p41/p42)
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Blatt II", "Blatt II")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {t("se začne pri", "starts at")} 801 (p43) · {t("strani", "pages")} 43–92 · p72 = Blatt III (1281–1302) {t("vmes", "in between")} · {t("cona", "zone")} 1100–1640 {t("prepletena", "interleaved")}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Lokalne sekcije", "Local sections")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    161–180 / 101–120 / 601–620 / 921–960 {t("sredi globalnega teka", "within the global run")} · p101 {t("z ulomki", "with fractions")} (196½)
                  </p>
                </div>
              </div>

              {/* P59: per-Blatt dvoumnost */}
              <div className="mt-3 rounded-lg border bg-background p-3">
                <p className="text-xs font-semibold">{t("Per-Blatt dvoumnost v2 (merjeno)", "Per-Blatt ambiguity of v2 (measured)")}</p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  <span className="rounded bg-stone-100 px-1.5 py-0.5 dark:bg-stone-800">{BLATT_HEADERS_P59.perBlattAmbiguity.basesOnMultiplePages_v2} {t("base na več straneh", "bases on multiple pages")}</span> → <span className="rounded bg-sky-100 px-1.5 py-0.5 dark:bg-sky-950/40">{BLATT_HEADERS_P59.perBlattAmbiguity.basesOnMultipleBlatter} {t("čez ≥2 Blatta", "span ≥2 Blaetter")}</span> · <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{BLATT_HEADERS_P59.perBlattAmbiguity.ruleCandidateBases.length} ruleCandidate</span> ({t("edina instanca v pasu razmerij", "exactly one instance in the ratio band")} [0.8, 1.25])
                </p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  {t("primer", "example")}: 163 — Blatt I @ 7.0 {t("proti", "vs")} Blatt II @ 0.981 ≈ 1 QK; {BLATT_HEADERS_P59.perBlattAmbiguity.ruleCandidateBases.slice(0, 8).join(", ")} ...
                </p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  {t("ruleCandidate", "ruleCandidates")}: <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{t("IZVEDENO v P60", "DONE in P60")}</span> — {t("glej kartico P60", "see the P60 card")}
                </p>
              </div>

              {/* P59: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Numeralе visoka zaupanja (2-prehodno soglasje + 32 arbitraž s hardcoded razlogi); parzella razponi svežih branj NIZKA zaupanja — Kurrent pasti dokumentirane (4↔8, 7→1, odrezane vodilne števke), avtoritativni ostajajo v2/pageMap podatki; sred-stranske numeralе = extras [~]; ruleCandidate = MERJEN kandidat — IZVEDEN v P60 (kartica P60), join v2 NESPREMENJEN (brez dokaza se NE prerazporeja — disciplina P56/P58); polna pokritost 135/135 × 2 — P62: 133–136, 138–139 + p137 pass2 dopolnjena po premagani kvoti 429 (konec registra p133–137 nosi korekcijske cone IV→V/II [~]); identifikacija per-Blatt instanc [~] (strojno branje ni dokazni vir). Strojno berljivo: research/issue17/ps-blatt-headers.json + runtime src/data/atlas/ps-blatt-headers.json (/api/atlas/ps-blatt-headers).",
                    "The numerals are high-confidence (2-pass agreement + 32 arbitrations with hardcoded reasons); the fresh parzella ranges are LOW-confidence — Kurrent pitfalls documented (4↔8, 7→1, dropped leading digits), the authoritative data remain the v2/pageMap; mid-page numerals = extras [~]; ruleCandidate = a MEASURED candidate — DONE in P60 (the P60 card), the v2 join UNCHANGED (nothing reassigned without proof — P56/P58 discipline); full coverage 135/135 × 2 — P62: pp. 133–136, 138–139 + p137 pass2 completed after the 429 quota cleared (register end p133–137 carries IV→V/II correction zones [~]); per-Blatt instance identification [~] (machine reading is not an evidentiary source). Machine-readable: research/issue17/ps-blatt-headers.json + the runtime src/data/atlas/ps-blatt-headers.json (/api/atlas/ps-blatt-headers).",
                  )}
                </p>
              </div>
            </div>

            {/* P60 — per-Blatt atribucija ruleCandidate (issue #13) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <BookOpen className="size-4 text-primary" aria-hidden="true" />
                {t("Per-Blatt atribucija ruleCandidate (P60)", "Per-Blatt attribution of ruleCandidates (P60)")}
                <StatusBadge status={PERBLATT_ATTR_P60.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Izvedba P59 pravila pasu [0.8, 1.25]: vsaka od 17 ruleCandidate base dobi instanco v pasu kot attributedBlatt — merjeno, brez prerazporeditev joina (disciplina P56/P58/P59). Soslednost-kontrola po vrstnem redu vrstic; strukturni prinos: pas-strani = 100 % več-stranskih base (Kultur-Tabellen re-listing). Unit-semantics opomba: pas ujema modo B (≈ 1), ne modo A (≈ 3.59665 = 1 QK → m²) — absolutna korespondenca ostaja odprta.",
                  "Execution of the P59 band rule [0.8, 1.25]: each of the 17 ruleCandidate bases gets its in-band instance as the attributedBlatt — measured, without reassigning the join (P56/P58/P59 discipline). Adjacency control in row order; structural gain: the attribute pages carry 100% multi-page bases (Kultur-Tabellen re-listing). Unit-semantics note: the band matches mode B (≈ 1), not mode A (≈ 3.59665 = 1 QK → m²) — the absolute correspondence remains open.",
                )}
              </p>

              {/* P60: atribucije */}
              <div className="mt-3 rounded-lg border bg-background p-3">
                <p className="text-xs font-semibold">{t("Atribucije (merjeno)", "Attributions (measured)")}</p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  <span className="rounded bg-stone-100 px-1.5 py-0.5 dark:bg-stone-800">{PERBLATT_ATTR_P60.summary.bases} base</span> · <span className="rounded bg-sky-100 px-1.5 py-0.5 dark:bg-sky-950/40">II {PERBLATT_ATTR_P60.summary.attributedBlattDist.II} · I {PERBLATT_ATTR_P60.summary.attributedBlattDist.I} · III {PERBLATT_ATTR_P60.summary.attributedBlattDist.III}</span> · {PERBLATT_ATTR_P60.summary.rows} {t("vrstic", "rows")} · {t("soslednost", "adjacency")} <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{PERBLATT_ATTR_P60.summary.soslednost.ok}/{PERBLATT_ATTR_P60.summary.rows}</span> ({PERBLATT_ATTR_P60.summary.soslednost.flaggedRows.join(", ")} [~] = {t("prečrtane vrstice", "crossed-out rows")})
                </p>
              </div>

              {/* P60: primeri + struktura */}
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Primer 163", "Example 163")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    → Blatt II @ {PERBLATT_ATTR_P60.attrBases["163"].inBandMedian} · {t("4 kulture", "4 cultures")} (Wiese/Prunigad/Weide/Aehn @ 61/83/84/86) · Blatt I @ 7.0 @ p11
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Kultur-Tabellen", "Kultur-Tabellen")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {PERBLATT_ATTR_P60.summary.relist100Pages.length} {t("pas-strani z 100 % več-stranskih base", "attribute pages with 100% multi-page bases")} (36, 49, 61, 83–87, 99) · p85 = Wiese und Gfrett (644–657) · p99 = Wiesen (928–939)
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Unit-semantics (odprto)", "Unit semantics (open)")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {t("moda A", "mode A")} ≈ 3.59665 (1 QK → m², n=226) · {t("moda B", "mode B")} ≈ 1 (n=62) · {t("faktor", "factor")} ~3.6 · {t("atribucija = relativa", "attribution = relative")} [~] · <span className="text-primary">{t("→ P61 merjeno: moda B = drugačna konvencija, ne napaka ujeme", "→ P61 measured: mode B = a different convention, not a join error")}</span>
                  </p>
                </div>
              </div>

              {/* P60: poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Atribucija = RELATIVNA (najboljše ujemanje med instancami baze) — absolutna korespondenca ni dokazana (unit gap moda A/B ~3.6, odprto); join v2 NESPREMENJEN (izpisi brez pozicij/površin; sha256 v2 vhoda pinan — I4 po gradnji); soslednost = kontrola kakovosti, ne diskriminator; P59 pokritost POPOLNA (P62: 135/135 × 2) — razširitev na 110 čez-Blatt base je odprta faza. Strojno berljivo: research/issue17/ps-perblatt-attribution.json + runtime src/data/atlas/ps-perblatt-attribution.json (/api/atlas/ps-perblatt-attribution).",
                    "The attribution is RELATIVE (the best match among a base's instances) — the absolute correspondence is not proven (mode A/B unit gap ~3.6, open); the v2 join UNCHANGED (outputs contain no positions/areas; the v2 input sha256 pinned — I4 by construction); adjacency = a quality control, not a discriminator; P59 coverage FULL (P62: 135/135 × 2) — extension to 110 cross-Blatt bases is an open phase. Machine-readable: research/issue17/ps-perblatt-attribution.json + the runtime src/data/atlas/ps-perblatt-attribution.json (/api/atlas/ps-perblatt-attribution).",
                  )}
                </p>
              </div>
            </div>

            {/* P61 — unit-semantics moda B (issue #13) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <BookOpen className="size-4 text-primary" aria-hidden="true" />
                {t("Unit-semantics moda B — merjena karakterizacija (P61)", "Unit-semantics mode B — measured characterization (P61)")}
                <StatusBadge status={UNIT_SEM_P61.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Odprta točka P60 #1 ('kolonialna enota ali delna površina?') merjeno RAZREŠENA s preusmeritvijo: moda B ni napaka ujeme in ni delna površina — je dosledna drugačna registracijska konvencija površin (številka ≈ sodobna meritev v m²). Permutacijska kontrola na GURS parcelah KO 1544 z determinističnimi FNV-1a točkami (bajtno enako Python/TS) — identiteta enote ostaja odprta [~].",
                  "P60 open point #1 ('a colonial unit or a partial surface?') measured and RE-FRAMED: mode B is neither a join error nor a partial surface — it is a consistent alternative registration convention (number ≈ modern m2). Permutation control on the GURS parcels KO 1544 with deterministic FNV-1a points (byte-identical Python/TS) — the unit identity remains open [~].",
                )}
              </p>

              {/* P61: modi + kontrola */}
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Modi (pasovi == P60)", "Modes (bands == P60)")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {t("moda A", "mode A")} [3.3, 4.3] n=226 · {t("moda B", "mode B")} [0.8, 1.25] n=62 · {t("ostali", "other")} n=800 · {t("brez razmerja", "no ratio")} n=5
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Kontrola @ 50 m (ključni)", "Control @ 50 m (key)")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    {t("moda A", "mode A")} {UNIT_SEM_P61.kontrola.A.real50.rate} vs {UNIT_SEM_P61.kontrola.A.perm50.rate} ({t("5.6×", "5.6×")}) · {t("moda B", "mode B")} {UNIT_SEM_P61.kontrola.B.real50.rate} vs {UNIT_SEM_P61.kontrola.B.perm50.rate} (1.6×) · @100 m {t("gostota", "density")} ({UNIT_SEM_P61.kontrola.A.perm100.rate}/{UNIT_SEM_P61.kontrola.B.perm100.rate})
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="text-xs font-semibold">{t("Struktura moda B", "Mode B structure")}</p>
                  <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                    42 {t("strani", "pages")} (5–137) · Blatt II 32 · IV 15 · III 9 · I 5 · {t("bloki", "blocks")} 3/9 (p85 'Wiese und Gfrett' 653–657, p86, p117)
                  </p>
                </div>
              </div>

              {/* P61: hipoteze */}
              <div className="mt-3 rounded-lg border bg-background p-3">
                <p className="text-xs font-semibold">{t("Hipoteze (merjeno)", "Hypotheses (measured)")}</p>
                <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                  H1 {t("napačni številčni join", "wrong-number join")}: <span className="rounded bg-rose-100 px-1.5 py-0.5 dark:bg-rose-950/40">{UNIT_SEM_P61.hipoteze.H1_napacenJoin.status}</span> ({UNIT_SEM_P61.hipoteze.H1_napacenJoin.dokaz}) · H3 {t("delna površina", "partial surface")}: <span className="rounded bg-amber-100 px-1.5 py-0.5 dark:bg-amber-950/40">{UNIT_SEM_P61.hipoteze.H3_delnaPovrsina.status}</span> ({t("samo", "only")} 2 base: 163, 176) · H2 {t("druga enota", "different unit")}: <span className="rounded bg-emerald-100 px-1.5 py-0.5 dark:bg-emerald-950/40">{UNIT_SEM_P61.hipoteze.H2_drugaEnota.status}</span>
                </p>
              </div>

              {/* P61: implikacija + poštenost */}
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Identiteta enote ODPRTA [~] (paleografija/dokumenti — naslednja faza); Implikacija za P60: pas pravilo [0.8, 1.25] izbere vrstico v konvenciji, številčno primerljivi s sodobno meritvijo — atribucija smiselna kot RELATIVA, atribucije P60 NESPREMENJENE; join v2 NESPREMENJEN (sha256 == P60 dokaz, I2); P59 pokritost POPOLNA (P62: 135/135 × 2 — moda B blattDist II 32 · IV 15). Strojno berljivo: research/issue17/ps-unit-semantics.json + runtime src/data/atlas/ps-unit-semantics.json (/api/atlas/ps-unit-semantics; gursCompact za produkcijo preracun).",
                    "Unit identity OPEN [~] (paleography/documents — next phase); implication for P60: the [0.8, 1.25] band selects the row in the convention numerically comparable with the modern measurement — attribution sound as RELATIVE, P60 attributions UNCHANGED; join v2 UNCHANGED (sha256 == P60 evidence, I2); P59 coverage FULL (P62: 135/135 × 2 — mode B blattDist II 32 · IV 15). Machine-readable: research/issue17/ps-unit-semantics.json + the runtime src/data/atlas/ps-unit-semantics.json (/api/atlas/ps-unit-semantics; gursCompact for the production re-computation).",
                  )}
                </p>
              </div>
            </div>

            {/* P63 — zaključne strani registra PS (Blatt IIb + tail transkripcija) */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <ScrollText className="size-4 text-primary" aria-hidden="true" />
                {t("Zaključne strani registra — Blatt IIb (P63)", "Register tail pages — Blatt IIb (P63)")}
                <StatusBadge status={TAIL_P63.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Paleografska zaključitev repa registra (str. 138–139) s 3 neodvisnimi prehodi (VLM 2× + agent-oči na izrezih 4×–5×; 2-od-3 konsenz, 42 flagov [~]).",
                  "Paleographic completion of the register tail (pp. 138–139) with 3 independent passes (VLM 2× + agent eyes on 4×–5× crops; 2-of-3 consensus, 42 flags [~]).",
                )}
              </p>
              <div className="mt-4 grid gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Blatt IIb @ p139 (KOREKCIJA)", "Blatt IIb @ p139 (CORRECTION)")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Glava je 'Nro. des Blattes.' — prejšnja očesna razlaga 'Nro. des Hauses.' NAPAČNA → P58 open #6 ZAPRT; numerele 'IIb' @ r1 (2-od-3) — pod-list NOV v strukturi; Parzelle 41–60 (duplikat Blatt I številk)",
                      "The header is 'Nro. des Blattes.' — the earlier 'Nro. des Hauses.' eye reading was WRONG → P58 open #6 CLOSED; numeral 'IIb' @ r1 (2-of-3) — a sub-leaf NEW to the structure; parcels 41–60 (duplicate Blatt I numbers)",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Lastninske kolone (p139 leva)", "Owner columns (p139 left)")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Haus Nº rdeče (1082, 1030, 998[~], 266, 695, 88, ...) · 'Vor und Zuname' = ŠTEVILKE 62–80 (ne imena; r1 'G. l. fin.'[~]) · Stand + Wohnort (rdeče); vsote 82|81, 125|183",
                      "Red Haus Nº (1082, 1030, 998[~], 266, 695, 88, ...) · 'Vor und Zuname' = NUMBERS 62–80 (not names; r1 'G. l. fin.'[~]) · Stand + Wohnort (red); sums 82|81, 125|183",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Kultura rekapitulacija (p139 desna)", "Culture recap (p139 right)")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Kulturs Gattung 81–100 · Classe 101–120 · Fürtrag 189|1228 · Capital fl (rdeče: 1860, 1146, —, 831, ...) + kr (Σ=153) · vsota 162|1447 [~]",
                      "Kulturs Gattung 81–100 · Classe 101–120 · transfer 189|1228 · Capital fl (red: 1860, 1146, —, 831, ...) + kr (Σ=153) · total 162|1447 [~]",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("p138: izbrisana leva + 'Zusammenstellung' desna", "p138: erased left + 'Zusammenstellung' right")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Bledi ostanki: 'T. 191'[~] @ r14, parzelle 23/24[~], '89/86'[~] @ r27; desna: Wiese 1–20, Classe 21–40, vsota 101|15320 [~]",
                      "Faint remains: 'T. 191'[~] @ r14, parcels 23/24[~], '89/86'[~] @ r27; right: Wiese 1–20, Classe 21–40, total 101|15320 [~]",
                    )}
                  </p>
                </div>
              </div>
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Razlaga števil 62–80 @ 'Vor und Zuname' (konskripcija/Einlage?) ODPRTA [~]; enote vsot 82|81, 125|183, 162|1447 ODPRETE [~]; join v2 NESPREMENJEN (p138/139 brez vrstic v v2 — 211/110/17 nespremenjeni). Strojno berljivo: research/issue17/ps-tail-pages.json + runtime src/data/atlas/ps-tail-pages.json (/api/atlas/ps-tail-pages).",
                    "Interpretation of numbers 62–80 @ 'Vor und Zuname' (conscription/Einlage?) OPEN [~]; unit meaning of sums 82|81, 125|183, 162|1447 OPEN [~]; join v2 UNCHANGED (p138/139 without v2 rows — 211/110/17 unchanged). Machine-readable: research/issue17/ps-tail-pages.json + the runtime src/data/atlas/ps-tail-pages.json (/api/atlas/ps-tail-pages).",
                  )}
                </p>
              </div>
            </div>

            {/* P64 — razširitev per-Blatt atribucije na 110 čez-Blatt base */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <ScrollText className="size-4 text-primary" aria-hidden="true" />
                {t("Per-Blatt atribucija — razširitev na 110 (P64)", "Per-Blatt attribution — extended to 110 (P64)")}
                <StatusBadge status={ATTR_EXT_P64.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Odprta točka P60/P62 #7: atribucija razširjena z merjeno hierarhijo pravil (R1 pas · R2a area-dominanca ≥ 0.75 · R2b ena-area) — 71/110 atributiranih, 39 split z alternativami.",
                  "P60/P62 open point #7: attribution extended with a measured rule hierarchy (R1 band · R2a area-dominance >= 0.75 · R2b single-area) — 71/110 attributed, 39 splits with alternatives.",
                )}
              </p>
              <div className="mt-4 grid gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Hierarhija pravil (merjeno)", "Rule hierarchy (measured)")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "R1 pas [0.8, 1.25] = P60 (17, bajtno) · R2a dominanca ≥ 0.75 (53: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b ena-Blatt-s-površino (1: 1605) → 71/110 (II 42 · III 15 · I 5 · IV 5 · V 4)",
                      "R1 band [0.8, 1.25] = P60 (17, byte-identical) · R2a dominance >= 0.75 (53: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b single-Blatt-with-area (1: 1605) -> 71/110 (II 42 · III 15 · I 5 · IV 5 · V 4)",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("R1↔R2 konsistenca", "R1-vs-R2 consistency")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "15/17 soglasij; 2 merjeni divergence: 930 (R1 II vs R2 dom III @ 0.763), 671 (R1 I vs R2 dom II @ 0.8844) — pas (moda B) ima prednost [~]",
                      "15/17 agreements; 2 measured divergences: 930 (R1 II vs R2 dom III @ 0.763), 671 (R1 I vs R2 dom II @ 0.8844) — the band (mode B) takes precedence [~]",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Split base (39) + prag", "Split bases (39) + threshold")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Dominantni delež 0.5–0.75 (II 19 · III 9 · IV 6 · V 4 · I 1) z alternativami po deležih — npr. 642: I 0.5187 vs II 0.4813 (2 kulturi, 2 lastnika); občutljivost: 24 @ ≥0.9 · 45 @ ≥0.8 · 53 @ ≥0.75 · 69 @ ≥0.6",
                      "Dominant share 0.5-0.75 (II 19 · III 9 · IV 6 · V 4 · I 1) with per-share alternatives — e.g. 642: I 0.5187 vs II 0.4813 (2 cultures, 2 owners); sensitivity: 24 @ >=0.9 · 45 @ >=0.8 · 53 @ >=0.75 · 69 @ >=0.6",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Soslednost + join", "Adjacency + join")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Soslednost relevantnih vrstic 186/216 (flag 30 — prečrtane vrstice [~]; R1 del 21/23 kot P60); join v2 NESPREMENJEN — meritve brez prerazporeditev",
                      "Adjacency of relevant rows 186/216 (30 flags — crossed-out rows [~]; the R1 part 21/23 as P60); the v2 join UNCHANGED — measurements without reassignments",
                    )}
                  </p>
                </div>
              </div>
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "39 split base ostaja NEATRIBUTIRANIH [~] z alternativami — odločitev lastnika za per-Blatt SPLIT joina (#8); 2 R1↔R2 divergenci nerazloženi [~] (moda B vs area-dominanca); strojna atribucija ni dokazni vir. Strojno berljivo: research/issue17/ps-attribution-ext.json + runtime src/data/atlas/ps-attribution-ext.json (/api/atlas/ps-attribution-ext).",
                    "39 split bases remain UNATTRIBUTED [~] with alternatives — the owner decision for the per-Blatt SPLIT join (#8); 2 R1-vs-R2 divergences unexplained [~] (mode B vs area dominance); machine attribution is not an evidentiary source. Machine-readable: research/issue17/ps-attribution-ext.json + the runtime src/data/atlas/ps-attribution-ext.json (/api/atlas/ps-attribution-ext).",
                  )}
                </p>
              </div>
            </div>

            {/* P65 — polna per-Blatt atribucija: 101 single-Blatt + pokritost 211/211 */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <ScrollText className="size-4 text-primary" aria-hidden="true" />
                {t("Per-Blatt atribucija — polna pokritost 211/211 (P65)", "Per-Blatt attribution — full coverage 211/211 (P65)")}
                <StatusBadge status={ATTR_FULL_P65.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Odprta točka P64 #3: 101 single-Blatt več-stranskih base atributiranih (vse vrstice na straneh istega Blatta — trivialno, R3-single) → pokritost več-stranskih base POPOLNA: 211/211.",
                  "P64 open point #3: the 101 single-Blatt multi-page bases attributed (all rows on pages of the same Blatt — trivial, R3-single) -> multi-page coverage COMPLETE: 211/211.",
                )}
              </p>
              <div className="mt-4 grid gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("R3-single (merjeno)", "R3-single (measured)")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "I 3 · II 26 · III 14 · IV 58 (101 base, 205 vrstic — 98 × 2 + 3 × 3; vse z izmerjeno površino) → skupaj 172 atributiranih (Blatt II 68 · IV 63 · III 29 · I 8 · V 4)",
                      "I 3 · II 26 · III 14 · IV 58 (101 bases, 205 rows — 98 × 2 + 3 × 3; all with measured area) -> 172 attributed in total (Blatt II 68 · IV 63 · III 29 · I 8 · V 4)",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Polna pokritost registra", "Full register coverage")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "800 base × 1093 vrstic = 589 single-page (implicitno prek strani: I 145 · I·II 10 · II 183 · III 28 · IV 205 · V 18) + 211 multi-page (110 čez-Blatt + 101 single-Blatt); 0 vrstic brez atribucije",
                      "800 bases × 1,093 rows = 589 single-page (implicit via the page: I 145 · I·II 10 · II 183 · III 28 · IV 205 · V 18) + 211 multi-page (110 cross-Blatt + 101 single-Blatt); 0 rows without attribution",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Soslednost", "Adjacency")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Relevantnih vrstic skupaj 375/425 (flag 50); R3 del 189/209 — prečrtane vrstice [~]; P64 del 186/216 nespremenjen",
                      "Relevant rows 375/425 in total (50 flags); the R3 part 189/209 — crossed-out rows [~]; the P64 part 186/216 unchanged",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Konsistenca + join", "Consistency + join")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "110 P64 atribucij bajtno nespremenjenih (I3); R3 nesoglasij s P64: 0 (disjunktni množici); join v2 NESPREMENJEN — meritve brez prerazporeditev",
                      "The 110 P64 attributions byte-unchanged (I3); R3 conflicts with P64: 0 (disjoint sets); the v2 join UNCHANGED — measurements without reassignments",
                    )}
                  </p>
                </div>
              </div>
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "39 split base ostaja NEATRIBUTIRANIH [~] (odločitev lastnika za SPLIT joina); 'I·II' prehodne strani (10 single-page base) razlagalno odprte [~]; strojna atribucija ni dokazni vir. Strojno berljivo: research/issue17/ps-attribution-full.json + runtime src/data/atlas/ps-attribution-full.json (/api/atlas/ps-attribution-full).",
                    "39 split bases remain UNATTRIBUTED [~] (owner decision on the SPLIT join); 'I·II' transition pages (10 single-page bases) open [~]; machine attribution is not an evidentiary source. Machine-readable: research/issue17/ps-attribution-full.json + the runtime src/data/atlas/ps-attribution-full.json (/api/atlas/ps-attribution-full).",
                  )}
                </p>
              </div>
            </div>

            {/* P66 — split decision pack: 39 split base */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <ScrollText className="size-4 text-primary" aria-hidden="true" />
                {t("Split decision pack — 39 base z deleži (P66)", "Split decision pack — 39 bases with shares (P66)")}
                <StatusBadge status={SPLIT_PACK_P66.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Odločitveni paket za per-Blatt SPLIT joina (odprta točka P64 #8): NE odloča namesto lastnika — meri in dokazuje dejstva nad 39 split base iz P65 (bajtni vir).",
                  "The decision pack for the per-Blatt SPLIT join (P64 open point #8): it does NOT decide on behalf of the owner — it measures and proves the facts over the 39 split bases from P65 (byte source).",
                )}
              </p>
              <div className="mt-4 grid gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Razčlenitev (merjeno)", "Partition (measured)")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "39 base × 2 deleža; 93 vrstic (25 × 2 + 13 × 3 + 1 × 4); pari Blattov I·II 7 · II·III 21 · II·IV 2 · IV·V 9 (sosednji 37, skok 2: 1603/1604 — isti kulturi)",
                      "39 bases × 2 shares; 93 rows (25 × 2 + 13 × 3 + 1 × 4); Blatt pairs I·II 7 · II·III 21 · II·IV 2 · IV·V 9 (adjacent 37, skips 2: 1603/1604 — same cultures)",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Lastniki per Blatt", "Owners per Blatt")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "DISJUNKTNI 39/39 — vsak split base ima različne lastnike po Blattih (2–3 edinstvenih: 25/13/1) → močan dokaz za 2 RAZLIČNI realni parceli",
                      "DISJOINT 39/39 — every split base has different owners per Blatt (2–3 unique: 25/13/1) -> strong evidence for 2 DIFFERENT real parcels",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Deleži + kulture", "Shares + cultures")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Dominantni delež [0.50,0.60) 23 · [0.60,0.70) 11 · [0.70,0.75) 5; kulture 92 z razčlenitvijo per Blatt (kulturesByBlatt)",
                      "Dominant share [0.50,0.60) 23 · [0.60,0.70) 11 · [0.70,0.75) 5; cultures 92 with the per-Blatt partition (kulturesByBlatt)",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Geometrija + kakovost", "Geometry + quality")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "GEO 39/39: vse vrstice base nosijo ENAKO geometrijo joina v2 (na nivoju številke) → SPLIT bi zahteval 2 geometriji; areaSuspect 0; sosledje 82/93 (flag 11 — 5 base)",
                      "GEO 39/39: all rows of a base carry the SAME join-v2 geometry (at the number level) -> a SPLIT would require 2 geometries; areaSuspect 0; adjacency 82/93 (11 flags — 5 bases)",
                    )}
                  </p>
                </div>
              </div>
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "P66 NE odloča o SPLIT joinu — odločitev je LASTNIŠKA (2 geometriji; razdelitev per deleži ali per lastnika); P65 polja 39× bajtno (I3); join v2 NESPREMENJEN; strojna atribucija ni dokazni vir. Strojno berljivo: research/issue17/ps-split-pack.json + runtime src/data/atlas/ps-split-pack.json (/api/atlas/ps-split-pack).",
                    "P66 does NOT decide the SPLIT join — the decision belongs to the OWNER (2 geometries; split per shares or per owner); the P65 fields byte-identical 39× (I3); the v2 join UNCHANGED; machine attribution is not an evidentiary source. Machine-readable: research/issue17/ps-split-pack.json + the runtime src/data/atlas/ps-split-pack.json (/api/atlas/ps-split-pack).",
                  )}
                </p>
              </div>
            </div>

            {/* P67 — forenzični paket anomalij: skok II·IV, flagi, R1↔R2, disjunktnost */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <ScrollText className="size-4 text-primary" aria-hidden="true" />
                {t("Forenzika anomalij — skok II·IV, flagi, disjunktnost (P67)", "Anomaly forensics — II·IV skip, flags, disjointness (P67)")}
                <StatusBadge status={ANOM_FORENSICS_P67.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Štiri merjena dela (kandidati P66 next + P64/P65 divergenci): forenzika 2 skokov II·IV, 5 sosledje flagov, R1↔R2 divergenc in univerzalna lastniška disjunktnost — deterministično, brez AI ob delovanju.",
                  "Four measured parts (P66 next candidates + P64/P65 divergences): forensics of the 2 II·IV skips, the 5 adjacency flags, the R1↔R2 divergences and universal owner disjointness — deterministic, no AI at runtime.",
                )}
              </p>
              <div className="mt-4 grid gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("A — skok II·IV = artifakt cifr", "A — the II·IV skip = a digit artifact")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "p78 prave 1501–1520 (Wüstung Pod Grabino; napaka 5→6), p93 prave 1901–1920 (napaka 9→6/9→0), p87 prave 1681–1700 (napaka −1020 + lažna geometrija); 1603/1604/1605/661/671 = lažne fuzije — skok IZGINE; renumerifikacija 17 preslikav = P68",
                      "p78 true 1501–1520 (Wüstung Pod Grabino; error 5→6), p93 true 1901–1920 (error 9→6/9→0), p87 true 1681–1700 (error −1020 + false geometry); 1603/1604/1605/661/671 = false fusions — the skip DISSOLVES; renumbering 17 mappings = P68",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("B — 5 sosledje flagov", "B — the 5 adjacency flags")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "11/11 razloženih = artefakt obsega joina: manjkajoči sosedje obstajajo v registru (P38 z imeni), a brez poligonov v karti → izpad iz v2 (38,6 % pokritost); 1821/2141/661 = začetki strani (meja strani)",
                      "11/11 explained = a join-scope artifact: the missing neighbours exist in the register (P38 with names) but have no map polygons → dropped from v2 (38.6 % coverage); 1821/2141/661 = page starts (page boundary)",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("C — R1↔R2 divergenci", "C — the R1↔R2 divergences")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "671 RAZREŠENA (II instanca @p87 = 1691 — druga parcela; 671 ostane I-only); 930 ostaja [~] z merjenim dokazom (moda B ✓@p49 ✗@p99, disjunktna lastnika, sosedi ±1 na obeh straneh)",
                      "671 RESOLVED (the II instance @p87 = 1691 — a different parcel; 671 stays I-only); 930 remains [~] with measured evidence (mode B ✓@p49 ✗@p99, disjoint owners, ±1 neighbours on both pages)",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("D — univerzalna disjunktnost", "D — universal disjointness")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "Lastniki per Blatt DISJUNKTNI 110/110 čez-Blatt base (39 split == P66 bajtno, 71 atributiranih 71/71) → ista številka pod različnima Blattoma = 2 RAZLIČNI realni parceli; projekcija: base 802, multi-page 208",
                      "Owners per Blatt DISJOINT 110/110 cross-Blatt bases (39 split byte-equal P66, 71 attributed 71/71) → the same number under different Blatts = 2 DIFFERENT real parcels; projection: 802 bases, 208 multi-page",
                    )}
                  </p>
                </div>
              </div>
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "P67 forenzika meri NAPAKE v2 (v2 join ostaja arhivsko nespremenjen v tem dokazu); 17 preslikav je bila SPECIFIKACIJA za P68 — P68 jo je IZVEDEL (v3 runtime; odmiki aproksimacije 802/208/107 vs P68 meritve 798/199/98 dokumentirani); 930 ostaja [~]; strojna forenzika ni dokazni vir. Strojno berljivo: research/issue17/ps-anomaly-forensics.json + runtime src/data/atlas/ps-anomaly-forensics.json (/api/atlas/ps-anomaly-forensics).",
                    "P67 forensics measures the v2 ERRORS (the v2 join stays archived-unchanged in this evidence); the 17 mappings were a SPECIFICATION for P68 — P68 has REALIZED it (the v3 runtime; the approximation deviations 802/208/107 vs the P68 measurements 798/199/98 documented); 930 remains [~]; machine forensics is not an evidentiary source. Machine-readable: research/issue17/ps-anomaly-forensics.json + the runtime src/data/atlas/ps-anomaly-forensics.json (/api/atlas/ps-anomaly-forensics).",
                  )}
                </p>
              </div>
            </div>

            {/* P68 — v3 sanacija številčenja: 17 preslikav + re-join */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
                <ScrollText className="size-4 text-primary" aria-hidden="true" />
                {t("Sanacija številčenja v3 — 17 preslikav + re-join (P68)", "Numbering sanitation v3 — 17 mappings + re-join (P68)")}
                <StatusBadge status={V3_RENUMBER_P68.status} />
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Mehanski izvod P67 forenzične specifikacije (dvojna Kurrent zamenjava p78/p93/p87) — deterministično, brez AI ob delovanju; registrska branja nespremenjena, sanacija le na join ključu.",
                  "A mechanical derivation of the P67 forensic specification (the double Kurrent substitution p78/p93/p87) — deterministic, no AI at runtime; the register reads unchanged, the sanitation touches only the join key.",
                )}
              </p>
              <div className="mt-4 grid gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("17 preslikav, 0 kolizij", "17 mappings, 0 collisions")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "p78 1603/1604/1605→1503/1504/1505 (Blatt II, Wüstung Pod Grabino; napaka 5→6); p93 →1903/1904/1905 (Blatt IV; napaka 9→6/9→0); p87 661–680→1681–1700 (+1020; izguba vodilne 1 + 8→6) — parzella ostaja originalno branje",
                      "p78 1603/1604/1605→1503/1504/1505 (Blatt II, Wüstung Pod Grabino; error 5→6); p93 →1903/1904/1905 (Blatt IV; error 9→6/9→0); p87 661–680→1681–1700 (+1020; lost leading 1 + 8→6) — parzella keeps the original reading",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Re-join po P55 metodi", "Re-join by the P55 method")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "14 vrstic izpada (base brez PF poligona — kartni priči P67: 1503–1505 in 1681–1700 NE obstajajo); p93 3× re-claim na 1903/1904/1905 (jugozahodna lokacija; 1903/1905 delita poziciji s p98 III); nespremenjene vrstice bajtno == v2",
                      "14 rows dropped (base without a PF polygon — the P67 map witnesses: 1503–1505 and 1681–1700 do NOT exist); p93 3× re-claim on 1903/1904/1905 (south-west location; 1903/1905 share positions with p98 III); unchanged rows byte-identical to v2",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Meritve v3", "v3 measurements")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "1079 vrstic / 798 base / 199 multi-page / 98 cross-Blatt (blattDist I·II 31 · II·III 46 · III·IV 3 · IV·V 18); površine median 3.8512 (Δ +7.08 %, kontrola 4.2771); soslednost 590/51.8/28.3×; zaupanje 171/735/147",
                      "1079 rows / 798 bases / 199 multi-page / 98 cross-Blatt (blattDist I·II 31 · II·III 46 · III·IV 3 · IV·V 18); area median 3.8512 (Δ +7.08 %, control 4.2771); adjacency 590/51.8/28.3×; confidence 171/735/147",
                    )}
                  </p>
                </div>
                <div className="rounded-lg border bg-background p-3">
                  <p className="font-semibold">{t("Fuzije in odmiki", "Fusions and deviations")}</p>
                  <p className="mt-1 leading-relaxed text-muted-foreground">
                    {t(
                      "1903 = III×2+IV×1 (delež III 0.7081 == P67; split kandidat — LASTNIKA); 1905 = R2b profil (p93 brez areaQK); 1904 = nova base, ratio 6.8052 izven pasu (prečrtana vrstica registra); odmiki od P67 aproksimacije 802/208/107 → 798/199/98 dokumentirani [~]",
                      "1903 = III×2+IV×1 (share III 0.7081 == P67; split candidate — OWNER); 1905 = R2b profile (p93 without areaQK); 1904 = a new base, ratio 6.8052 out of band (a crossed register row); deviations from the P67 approximation 802/208/107 → 798/199/98 documented [~]",
                    )}
                  </p>
                </div>
              </div>
              <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900/50 dark:bg-emerald-950/30">
                <p className="text-[11px] leading-relaxed text-foreground/80">
                  <span className="font-semibold">{t("Pošten status: ", "Honest status: ")}</span>
                  {t(
                    "Skok II·IV IZGINE iz joina (lažni fuziji 1603/1604 razpadeta); čez-Blatt lažni pari 661/671 razpadejo (Blatt I instanci ostanejo čisti); per-Blatt instanca 1903/1905 (III vs IV) ostane fuzija v v3 [~] — SPLIT join odločitev ostaja LASTNIKA (P69); veriga re-run P59–P66 s posodobljenimi pini izvedena. Strojno berljivo: research/issue17/ps-parcels-geo-v3.json + runtime src/data/atlas/ps-parcels-geo.json (/api/atlas/ps-parcels-geo).",
                    "The II·IV skip DISSOLVES from the join (the false 1603/1604 fusions collapse); the cross-Blatt false pairs 661/671 collapse (the Blatt I instances stay clean); the per-Blatt instance 1903/1905 (III vs IV) remains fused in v3 [~] — the SPLIT join decision remains the OWNER's (P69); the re-run chain P59–P66 with updated pins realized. Machine-readable: research/issue17/ps-parcels-geo-v3.json + the runtime src/data/atlas/ps-parcels-geo.json (/api/atlas/ps-parcels-geo).",
                  )}
                </p>
              </div>
            </div>

            {/* N83 katalog 12 enot + reconciliation */}
            <div className="min-w-0 rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Landmark className="size-4 text-primary" aria-hidden="true" />
                {t(`Katalog N83 — ${n83.length} enot + uskladitev zero-loss`, `N83 catalog — ${n83.length} units + zero-loss reconciliation`)}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  `Uskladitev arhiva z Atlasom (issue #5): obdelanih ${recon.totals.processedRows} zapisov, izgubljenih ${recon.totals.lost}. Strojno berljivo: /api/atlas/reconciliation.`,
                  `Archive ↔ Atlas reconciliation (issue #5): ${recon.totals.processedRows} records processed, ${recon.totals.lost} lost. Machine-readable: /api/atlas/reconciliation.`,
                )}
              </p>
              <div className="mt-4 overflow-x-auto">
                <table className="w-full min-w-[640px] text-left text-xs">
                  <thead>
                    <tr className="border-b text-muted-foreground">
                      <th className="px-2 py-2 font-medium">{t("Enota", "Unit")}</th>
                      <th className="px-2 py-2 font-medium">{t("Prenos", "Transfer")}</th>
                      <th className="px-2 py-2 font-medium">{t("Georefenca", "Georef")}</th>
                      <th className="px-2 py-2 font-medium">{t("Strani", "Pages")}</th>
                      <th className="px-2 py-2 font-medium">{t("Strukturirano", "Structured")}</th>
                      <th className="px-2 py-2 font-medium">{t("Zero-loss", "Zero-loss")}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recon.units.map((u) => (
                      <tr key={u.code} className="border-b border-border/50">
                        <td className="px-2 py-2 font-mono font-semibold text-primary">
                          {u.vacUrl ? (
                            <a href={u.vacUrl} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 hover:underline">
                              {u.code}
                              <ExternalLink className="size-3" aria-hidden="true" />
                            </a>
                          ) : (
                            u.code
                          )}
                        </td>
                        <td className="px-2 py-2">
                          <StatusBadge status={u.transferStatus ?? "—"} />
                        </td>
                        <td className="px-2 py-2">
                          <StatusBadge status={u.georefStatus ?? "—"} />
                        </td>
                        <td className="px-2 py-2 font-mono text-muted-foreground">{u.pages ?? "—"}</td>
                        <td className="px-2 py-2 font-mono text-muted-foreground">{u.processedRows}</td>
                        <td className="px-2 py-2">{u.zeroLoss ? "✓" : "✗"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </motion.div>
        )}

        {/* ——— 3. GEODETSKI VIRI ——— */}
        {tab === "geodata" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4">
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <MapIcon className="size-4 text-primary" aria-hidden="true" />
                {t(
                  `Inventar javnih geodetskih virov za območje Griblje (${GEODATA_SOURCES.length})`,
                  `Inventory of public geodetic sources for the Griblje area (${GEODATA_SOURCES.length})`,
                )}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Vsak vir ima preverjen status pokritosti — tudi negativen (LiDAR 2014–2015 Gribelj NE pokriva). Datum zadnje preveritve: 2026-10-07.",
                  "Each source carries a verified coverage status — including negative ones (the 2014–2015 LiDAR does NOT cover Griblje). Last verified: 2026-10-07.",
                )}
              </p>
              <ul className="mt-4 grid gap-3 md:grid-cols-2">
                {GEODATA_SOURCES.map((g) => (
                  <li key={g.id} className="rounded-lg border bg-secondary/30 p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="text-sm font-semibold text-foreground">{lang === "si" ? g.nameSi : g.nameEn}</span>
                      <StatusBadge status={g.status} />
                    </div>
                    <p className="mt-0.5 text-[11px] text-muted-foreground">
                      {g.provider} · {lang === "si" ? g.kindSi : g.kindEn}
                    </p>
                    <p className="mt-1.5 text-xs leading-relaxed text-foreground/80">
                      <span className={g.coversGriblje ? "text-emerald-700 dark:text-emerald-400" : "text-orange-700 dark:text-orange-400"}>
                        {g.coversGriblje ? t("pokriva Griblje ✓", "covers Griblje ✓") : t("NE pokriva / ni potrjeno ✗", "does NOT cover / unconfirmed ✗")}
                      </span>
                      {" — "}
                      {lang === "si" ? (g.coversNoteSi ?? "") : (g.coversNoteEn ?? "")}
                    </p>
                    <p className="mt-1.5 text-[10px] text-muted-foreground">
                      {g.licence} ·{" "}
                      <a href={g.url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                        {t("vir", "source")} <ExternalLink className="inline size-2.5" aria-hidden="true" />
                      </a>
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {/* ——— 4. ŠOLSKI ARHIV ——— */}
        {tab === "sola" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4">
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <GraduationCap className="size-4 text-primary" aria-hidden="true" />
                {t("Šolski arhiv ZAL NME — povezan z MVG-026", "School archive ZAL NME — linked to MVG-026")}
              </h3>
              <ul className="mt-4 grid gap-3 md:grid-cols-2">
                {SCHOOL_ARCHIVE.units.map((u) => (
                  <li key={u.vacId} className="rounded-lg border bg-secondary/30 p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="text-sm font-semibold text-foreground">
                        {lang === "si" ? u.titleSi : u.titleEn}
                      </span>
                      <StatusBadge status={u.status} />
                    </div>
                    <p className="mt-1 font-mono text-[10px] text-muted-foreground">
                      {u.signature} · {u.years}
                    </p>
                    <p className="mt-1.5 text-xs leading-relaxed text-foreground/80">
                      {lang === "si" ? u.contentSi : u.contentEn}
                    </p>
                    <p className="mt-1.5 text-[10px] text-muted-foreground">
                      {u.archiveSi} ·{" "}
                      <a href={u.vacUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                        VAČ {u.vacId} <ExternalLink className="inline size-2.5" aria-hidden="true" />
                      </a>
                    </p>
                  </li>
                ))}
              </ul>
              <div className="mt-4 rounded-lg border border-orange-200 bg-orange-50/60 p-4 dark:border-orange-900/50 dark:bg-orange-950/30">
                <div className="flex flex-wrap items-center gap-2">
                  <BookOpen className="size-4 text-orange-700 dark:text-orange-400" aria-hidden="true" />
                  <span className="text-sm font-semibold text-foreground">
                    {t("Šolska kronika — status popravljen v REVIEW", "School chronicle — status corrected to REVIEW")}
                  </span>
                  <StatusBadge status={SCHOOL_ARCHIVE.chronicle.status} />
                </div>
                <p className="mt-1.5 text-xs leading-relaxed text-foreground/80">
                  {lang === "si" ? SCHOOL_ARCHIVE.chronicle.noteSi : SCHOOL_ARCHIVE.chronicle.noteEn}
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* ——— 5. POSEBNE RAZISKAVE ——— */}
        {tab === "posebno" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
            {/* Gaspari */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Users className="size-4 text-primary" aria-hidden="true" />
                {t("Maksim Gaspari — stopnja dokazljivosti", "Maksim Gaspari — level of provability")}
              </h3>
              <div className="mt-2 flex items-center gap-2">
                <StatusBadge status={GASPARI_RESEARCH.status} />
                <span className="text-xs text-muted-foreground">
                  {t("primarni predmet NI potrjen", "primary object NOT confirmed")}
                </span>
              </div>
              <p className="mt-2 text-xs leading-relaxed text-foreground/80">
                {lang === "si" ? GASPARI_RESEARCH.mentionSi : GASPARI_RESEARCH.mentionEn}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                {lang === "si" ? GASPARI_RESEARCH.noteSi : GASPARI_RESEARCH.noteEn}
              </p>
            </div>

            {/* F0000212 */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Database className="size-4 text-primary" aria-hidden="true" />
                {t("SEM F0000212 — dokazna veriga", "SEM F0000212 — evidence chain")}
              </h3>
              <p className="mt-1 text-xs text-muted-foreground">
                {F0000212_PROVENANCE.holder} · {t("pravice:", "rights:")} {lang === "si" ? F0000212_PROVENANCE.rightsSi : F0000212_PROVENANCE.rightsEn}
              </p>
              <ol className="mt-3 space-y-1.5">
                {F0000212_PROVENANCE.chain.map((c, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs">
                    <span className="mt-0.5 shrink-0 font-mono text-[10px] text-muted-foreground/70">{i + 1}.</span>
                    <span className="text-foreground/85">{lang === "si" ? c.stepSi : c.stepEn}</span>
                    <span className="ml-auto shrink-0">
                      <StatusBadge status={c.status} />
                    </span>
                  </li>
                ))}
              </ol>
              <p className="mt-3 text-[11px] leading-relaxed text-orange-700 dark:text-orange-300">
                {lang === "si" ? F0000212_PROVENANCE.houseLink.noteSi : F0000212_PROVENANCE.houseLink.noteEn}
              </p>
            </div>

            {/* Zemljevid 1812 */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <MapIcon className="size-4 text-primary" aria-hidden="true" />
                {t("Zemljevid 1812 — georeferenca [~] izvedena + koroborirana", "Map 1812 — georeference [~] executed + corroborated")}
              </h3>
              <div className="mt-3 overflow-hidden rounded-lg border">
                <img
                  src="/images/authentic/griblje-okolis-1812-900.jpg"
                  alt={t(
                    "Izrez zemljevida Ilirskih provinc 1812 (Giraldon, javna last) ± 63 km okoli Gribelj z rdečo oznako izračunane lege [~] in oranžnim krogom negotovosti ± 10 km",
                    "Crop of the 1812 Illyrian Provinces map (Giraldon, public domain) ± 63 km around Griblje with a red marker of the computed position [~] and an orange uncertainty circle ± 10 km",
                  )}
                  className="h-auto w-full"
                  width={900}
                  height={900}
                  loading="lazy"
                />
              </div>
              <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                {t(
                  "Izrez obdobjenega izvirnika (Giraldon 1812, javna last) ± 63 km okoli izračunane lege Gribelj; rdeča oznaka + oranžni krog = strojna georeferenca [~]. Slika v zbirki MVG-092.",
                  "Crop of the period original (Giraldon 1812, public domain) ± 63 km around Griblje's computed position; red marker + orange circle = machine georeference [~]. Collection image MVG-092.",
                )}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-foreground/80">
                {t(
                  `Georeferenca: ${MAP_1812.georef?.controlPoints ?? 15} OCR kontrolnih točk, merilo ${MAP_1812.georef?.scaleMPerPx.x ?? 126} × ${MAP_1812.georef?.scaleMPerPx.y ?? 124} m/px, residuali (mediana) ± ${MAP_1812.georef?.residualsKm.median ?? 10} km; Griblje px (${MAP_1812.georef?.gribljePx.x ?? 2499}, ${MAP_1812.georef?.gribljePx.y ?? 2286}) ± ${MAP_1812.georef?.uncertaintyKm ?? 10} km. Pokritje lista: ~11–24° E, 41–48° N (širše od meja Ilirskih provinc).`,
                  `Georeference: ${MAP_1812.georef?.controlPoints ?? 15} OCR control points, scale ${MAP_1812.georef?.scaleMPerPx.x ?? 126} × ${MAP_1812.georef?.scaleMPerPx.y ?? 124} m/px, residuals (median) ± ${MAP_1812.georef?.residualsKm.median ?? 10} km; Griblje px (${MAP_1812.georef?.gribljePx.x ?? 2499}, ${MAP_1812.georef?.gribljePx.y ?? 2286}) ± ${MAP_1812.georef?.uncertaintyKm ?? 10} km. Sheet coverage: ~11–24° E, 41–48° N (wider than the Illyrian Provinces).`,
                )}
              </p>
              {MAP_1812.georef?.corroboration && (
                <p className="mt-2 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 text-xs leading-relaxed text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-200">
                  {t(
                    `KOROBORACIJA (P7, neodvisen drugi sken istega lista — Internet Archive): ORB+RANSAC registracija obeh skenov (${MAP_1812.georef.corroboration.registration.inliers} inlierjev, RMS ${MAP_1812.georef.corroboration.registration.rmsPx} px) + neodvisen ${MAP_1812.georef.corroboration.controlPoints}-točkovni OCR geo-model drugega skena (merilo ${MAP_1812.georef.corroboration.scaleMPerPx.x}×${MAP_1812.georef.corroboration.scaleMPerPx.y} m/px, residuali mediana ${MAP_1812.georef.corroboration.residualsKm.median} km, celih besed ${MAP_1812.georef.corroboration.residualsKm.medianFullWords} km). Obe poti za lego Gribelj se ujemata na ${MAP_1812.georef.corroboration.agreementPx} px = ${MAP_1812.georef.corroboration.agreementKm} km — znotraj ± ${MAP_1812.georef.uncertaintyKm} km negotovosti. Rezultat georeference NI artefakt skeniranja. [~] 7/12 točk drugega skena so fragmenti oznak; napisi na pregibih knjižnega skena (Laibach, Fiume, Trst, Banya Luka) neberljivi.`,
                    `CORROBORATION (P7, an independent second scan of the same sheet — Internet Archive): ORB+RANSAC registration of both scans (${MAP_1812.georef.corroboration.registration.inliers} inliers, RMS ${MAP_1812.georef.corroboration.registration.rmsPx} px) + an independent ${MAP_1812.georef.corroboration.controlPoints}-point OCR geo-model of the second scan (scale ${MAP_1812.georef.corroboration.scaleMPerPx.x}×${MAP_1812.georef.corroboration.scaleMPerPx.y} m/px, residuals median ${MAP_1812.georef.corroboration.residualsKm.median} km, full words ${MAP_1812.georef.corroboration.residualsKm.medianFullWords} km). Both paths for Griblje's position agree to ${MAP_1812.georef.corroboration.agreementPx} px = ${MAP_1812.georef.corroboration.agreementKm} km — within the ± ${MAP_1812.georef.uncertaintyKm} km uncertainty. The georeference result is NOT a scanning artifact. [~] 7/12 points of the second scan are label fragments; labels on the book scan's fold creases (Laibach, Fiume, Trieste, Banya Luka) unreadable.`,
                  )}
                </p>
              )}
              <ul className="mt-2 space-y-1 text-xs">
                {MAP_1812.periodOriginals.map((p) => (
                  <li key={p.title}>
                    <a href={p.sourceUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                      {p.title}
                    </a>{" "}
                    <span className="text-muted-foreground">({p.licence})</span>
                  </li>
                ))}
              </ul>
              <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                {lang === "si" ? MAP_1812.georeferencePath.methodSi : MAP_1812.georeferencePath.methodEn}
              </p>
            </div>

            {/* Ustna zgodovina */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <MessageSquareQuote className="size-4 text-primary" aria-hidden="true" />
                {t("Ustna zgodovina — model, čaka snemanja", "Oral history — model, awaiting recordings")}
              </h3>
              <p className="mt-2 text-xs leading-relaxed text-foreground/80">
                {t(
                  "Model intervjuja: pripovedovalec, datum, lokacija, soglasje, avdio/video, prepis z različico, pravice uporabe. Seznam intervjujev je PRAZEN — nič ni izmišljeno.",
                  "Interview model: narrator, date, location, consent, audio/video, versioned transcript, usage rights. The interview list is EMPTY — nothing invented.",
                )}
              </p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {ORAL_TOPICS.map((o) => (
                  <Badge key={o.id} variant="outline" className="border-border text-[10px] font-normal">
                    {lang === "si" ? o.topicSi : o.topicEn}
                  </Badge>
                ))}
              </div>
              <p className="mt-2 text-[11px] text-muted-foreground">
                {t("5 tem iz starih raziskav, vse TO_COLLECT.", "5 topics from the old research, all TO_COLLECT.")}
              </p>
            </div>
          </motion.div>
        )}

        {/* ——— 6. NEGATIVNI REZULTATI ——— */}
        {tab === "negativni" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4">
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <FileX2 className="size-4 text-primary" aria-hidden="true" />
                {t(
                  `Negativni rezultati (${NEGATIVE_RESULTS.length}) — nikoli izbrisani`,
                  `Negative results (${NEGATIVE_RESULTS.length}) — never deleted`,
                )}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {t(
                  "Kaj smo iskali in NI bilo najdeno. Iz teh zapisov je razvidno, kaj je izgubljeno, kaj čaka in kje je meja dokazljivosti.",
                  "What was searched for and NOT found. These records show what is lost, what awaits and where the limit of provability lies.",
                )}
              </p>
              <ul className="mt-4 grid gap-3 md:grid-cols-2">
                {NEGATIVE_RESULTS.map((n) => (
                  <li key={n.id} className="rounded-lg border bg-secondary/30 p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="text-sm font-semibold text-foreground">
                        {lang === "si" ? n.whatSi : n.whatEn}
                      </span>
                      <StatusBadge status={n.status} />
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">
                      {lang === "si" ? n.detailSi : n.detailEn}
                    </p>
                    <p className="mt-1.5 font-mono text-[10px] text-muted-foreground/70">{n.id}</p>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {/* ——— 7. PRENOS IZ ARHIVA (issue #16) ——— */}
        {tab === "arhiv" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4">
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Archive className="size-4 text-primary" aria-hidden="true" />
                {t(
                  `Prenos iz arhiva markec-group/muzej-arhiv (issue #16)`,
                  `Transfer from the markec-group/muzej-arhiv archive (issue #16)`,
                )}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {lang === "si"
                  ? ARCHIVE_TRANSFER_AUDIT.verdictSi
                  : ARCHIVE_TRANSFER_AUDIT.verdictEn}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                <strong className="text-foreground">{t("Metoda:", "Method:")}</strong>{" "}
                {lang === "si" ? ARCHIVE_TRANSFER_AUDIT.methodSi : ARCHIVE_TRANSFER_AUDIT.methodEn}
              </p>
              <div className="mt-3 flex flex-wrap gap-2 text-[10px] font-mono text-muted-foreground">
                <span className="rounded-full bg-secondary px-2 py-0.5">
                  arhiv @ {ARCHIVE_TRANSFER_AUDIT.archiveRepo.headSha.slice(0, 7)} ·{" "}
                  {ARCHIVE_TRANSFER_AUDIT.archiveRepo.commits} commitov · archived
                </span>
                <span className="rounded-full bg-secondary px-2 py-0.5">
                  primerjava {ARCHIVE_TRANSFER_AUDIT.comparedAt}
                </span>
                <span className="rounded-full bg-secondary px-2 py-0.5">
                  {t(
                    `preneseno vnosov: ${ARCHIVE_TRANSFER_AUDIT.totalTransferredEntries}`,
                    `transferred entries: ${ARCHIVE_TRANSFER_AUDIT.totalTransferredEntries}`,
                  )}
                </span>
              </div>
            </div>

            {/* primerjalna matrika */}
            <div className="overflow-hidden rounded-xl border bg-card shadow-sm">
              <div className="border-b bg-secondary/40 px-6 py-4">
                <h4 className="font-display text-base font-semibold">
                  {t("Primerjalna matrika (številke iz datotek)", "Comparison matrix (numbers from files)")}
                </h4>
              </div>
              <div className="divide-y">
                {ARCHIVE_TRANSFER_ROWS.map((r) => (
                  <div key={r.areaEn} className="grid gap-2 px-6 py-4 md:grid-cols-[1.1fr_1fr_1fr_1.1fr]">
                    <p className="text-sm font-semibold text-foreground">
                      {lang === "si" ? r.areaSi : r.areaEn}
                    </p>
                    <div className="text-xs leading-relaxed text-muted-foreground">
                      <p className="mb-0.5 font-mono font-bold text-[10px] uppercase tracking-wide">
                        {t("Arhiv", "Archive")}
                      </p>
                      {lang === "si" ? r.archiveSi : r.archiveEn}
                    </div>
                    <div className="text-xs leading-relaxed text-muted-foreground">
                      <p className="mb-0.5 font-mono font-bold text-[10px] uppercase tracking-wide">
                        {t("Novi muzej", "New museum")}
                      </p>
                      {lang === "si" ? r.currentSi : r.currentEn}
                    </div>
                    <div className="text-xs leading-relaxed">
                      <p className="mb-0.5 font-mono font-bold text-[10px] uppercase tracking-wide text-primary">
                        {t("Akcija", "Action")}
                      </p>
                      {lang === "si" ? r.actionSi : r.actionEn}
                      <span className="ml-1.5 inline-flex items-center rounded-full bg-emerald-100 px-1.5 py-0.5 font-mono text-[10px] font-semibold text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100">
                        {t(`+${r.transferred}`, `+${r.transferred}`)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* namerno NE preneseno */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h4 className="flex items-center gap-2 font-display text-base font-semibold">
                <FileX2 className="size-4 text-muted-foreground" aria-hidden="true" />
                {t(
                  `Namerno NE preneseno (${ARCHIVE_NON_TRANSFERS.length})`,
                  `Deliberately NOT transferred (${ARCHIVE_NON_TRANSFERS.length})`,
                )}
              </h4>
              <ul className="mt-3 grid gap-3">
                {ARCHIVE_NON_TRANSFERS.map((n) => (
                  <li key={n.path} className="rounded-lg border bg-secondary/30 p-3">
                    <p className="font-mono text-xs font-semibold text-foreground">{n.path}</p>
                    <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                      {lang === "si" ? n.reasonSi : n.reasonEn}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}
        {/* ——— 8. ZAPOLNJEVANJE VRZELI (issue #17) ——— */}
        {tab === "vrzeli" && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid grid-cols-1 gap-4">
            {/* glava: verdikt */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
                <Search className="size-4 text-primary" aria-hidden="true" />
                {t(
                  `Research gap closure v2 — Kurrent, 1812–1853, hiše/parcele, viri (issue #17)`,
                  `Research gap closure v2 — Kurrent, 1812–1853, houses/parcels, sources (issue #17)`,
                )}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                {lang === "si" ? ISSUE17_AUDIT.principleSi : ISSUE17_AUDIT.principleEn}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                <strong className="text-foreground">{t("Metoda:", "Method:")}</strong>{" "}
                {lang === "si" ? ISSUE17_AUDIT.methodSi : ISSUE17_AUDIT.methodEn}
              </p>
              <div className="mt-3 flex flex-wrap gap-2 text-[10px] font-mono text-muted-foreground">
                <span className="rounded-full bg-secondary px-2 py-0.5">
                  {t(`VLM klicev: ${ISSUE17_AUDIT.vlmCallsTotal}`, `VLM calls: ${ISSUE17_AUDIT.vlmCallsTotal}`)}
                </span>
                <span className="rounded-full bg-secondary px-2 py-0.5">
                  {t(`serij delno prebranih: 7/7 (REVIEW)`, `series partially read: 7/7 (REVIEW)`)}
                </span>
                <span className="rounded-full bg-secondary px-2 py-0.5">research/issue17/ · surovi izpisi</span>
                <span className="rounded-full bg-secondary px-2 py-0.5">{ISSUE17_AUDIT.closedAt}</span>
              </div>
            </div>

            {/* PV — raba tal 1825 */}
            <div className="overflow-hidden rounded-xl border bg-card shadow-sm">
              <div className="border-b bg-secondary/40 px-6 py-4">
                <h4 className="font-display text-base font-semibold">
                  {t(
                    `PV — Izkaz rabe tal 1825 (10. 1. 1825): 10 izpolnjenih kultur, skupaj 1221 joch ≈ 703 ha`,
                    `PV — statement of land use 1825 (10 Jan 1825): 10 filled cultures, total 1221 joch ≈ 703 ha`,
                  )}
                </h4>
                <p className="mt-1 text-xs text-muted-foreground">
                  {t(
                    "Vsaka izpolnjena celica potrjena z vsaj dvema neodvisnima branjema; vrstica Wälder (gozd) je PRAZNA — dokumentirana anomalija.",
                    "Every filled cell confirmed by at least two independent readings; the Wälder (forest) row is EMPTY — a documented anomaly.",
                  )}
                </p>
              </div>
              <div className="max-h-96 overflow-y-auto overflow-x-auto">
                <table className="w-full min-w-[480px] text-sm">
                  <thead className="sticky top-0 bg-secondary/60 text-left text-[10px] font-mono uppercase tracking-wide text-muted-foreground">
                    <tr>
                      <th className="px-6 py-2">{t("Kultura (kot zapisano)", "Culture (as written)")}</th>
                      <th className="px-3 py-2">{t("Joch", "Joch")}</th>
                      <th className="px-3 py-2">{t("Klafter", "Klafter")}</th>
                      <th className="px-6 py-2">{t("Zanesljivost", "Confidence")}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    {PV_LAND_USE_1825.rows.map((r) => (
                      <tr key={r.cultureAsWritten} className={r.joch === null ? "text-muted-foreground/60" : ""}>
                        <td className="px-6 py-2 font-medium">{r.cultureAsWritten}</td>
                        <td className="px-3 py-2 font-mono">{r.joch ?? "—"}</td>
                        <td className="px-3 py-2 font-mono">{r.klafter ?? "—"}</td>
                        <td className="px-6 py-2 font-mono text-[10px]">{r.confidence}</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot className="border-t bg-secondary/30 font-mono text-xs">
                    <tr>
                      <td className="px-6 py-2">{PV_LAND_USE_1825.totals.ersteSumme.label}</td>
                      <td className="px-3 py-2">{PV_LAND_USE_1825.totals.ersteSumme.joch}</td>
                      <td className="px-3 py-2">{PV_LAND_USE_1825.totals.ersteSumme.klafter}</td>
                      <td className="px-6 py-2 text-[10px]">clear</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-2">{PV_LAND_USE_1825.totals.zweiteSumme.label}</td>
                      <td className="px-3 py-2">{PV_LAND_USE_1825.totals.zweiteSumme.joch}</td>
                      <td className="px-3 py-2">{PV_LAND_USE_1825.totals.zweiteSumme.klafter}</td>
                      <td className="px-6 py-2 text-[10px]">clear</td>
                    </tr>
                    <tr className="font-semibold">
                      <td className="px-6 py-2">{PV_LAND_USE_1825.totals.grandTotal.label}</td>
                      <td className="px-3 py-2">{PV_LAND_USE_1825.totals.grandTotal.joch}</td>
                      <td className="px-3 py-2">{PV_LAND_USE_1825.totals.grandTotal.klafter}</td>
                      <td className="px-6 py-2 text-[10px]">≈ {PV_LAND_USE_1825.totals.grandTotal.hectares} ha</td>
                    </tr>
                  </tfoot>
                </table>
              </div>
              <p className="border-t bg-orange-50 px-6 py-3 text-xs leading-relaxed text-orange-900 dark:bg-orange-950/40 dark:text-orange-200">
                ⚠ {lang === "si" ? PV_LAND_USE_1825.anomalySi : PV_LAND_USE_1825.anomalyEn}
              </p>
            </div>

            {/* PR + PS + PZ grid */}
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
              <div className="rounded-xl border bg-card p-6 shadow-sm">
                <h4 className="font-display text-base font-semibold">{t("PR — opis meje (8. 4. 1825)", "PR — boundary description (8 Apr 1825)")}</h4>
                <dl className="mt-3 space-y-2 text-xs">
                  <div className="flex justify-between gap-2">
                    <dt className="text-muted-foreground">{t("mere (V×S)", "dimensions (E×W)")}</dt>
                    <dd className="font-mono">{PR_BOUNDARY_1825.dimensions.eastWestKlafter} × {PR_BOUNDARY_1825.dimensions.northSouthKlafter} kl</dd>
                  </div>
                  <div className="flex justify-between gap-2">
                    <dt className="text-muted-foreground">{t("točk meje (prebranih)", "boundary points (read)")}</dt>
                    <dd className="font-mono">{PR_BOUNDARY_1825.boundaryPoints.length} [~]</dd>
                  </div>
                  <div className="flex justify-between gap-2">
                    <dt className="text-muted-foreground">{t("navzkrižna kontrola", "cross-check")}</dt>
                    <dd className="font-mono">{t("<1 % od PV", "<1 % of PV")}</dd>
                  </div>
                </dl>
                <ul className="mt-3 max-h-40 space-y-1 overflow-y-auto pr-2 text-[11px] text-muted-foreground">
                  {PR_BOUNDARY_1825.neighbours.map((n) => (
                    <li key={n.nameAsWritten} className="flex items-center justify-between gap-2">
                      <span>{n.nameAsWritten}</span>
                      <span className="font-mono text-[9px]">{n.confidence.slice(0, 24)}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-xl border bg-card p-6 shadow-sm">
                <h4 className="font-display text-base font-semibold">{t("PS — rekapitulacija (str. 143)", "PS — recapitulation (p. 143)")}</h4>
                <div className="mt-3 grid grid-cols-3 gap-2 text-center">
                  <div className="rounded-lg bg-secondary/40 p-2">
                    <p className="font-display text-xl font-semibold">{PS_RECAP_1826.summaBauplätze}</p>
                    <p className="text-[10px] leading-tight text-muted-foreground">{t("stavbnih mest", "building sites")}</p>
                  </div>
                  <div className="rounded-lg bg-secondary/40 p-2">
                    <p className="font-display text-xl font-semibold">{PS_RECAP_1826.summaGrundparzellen}</p>
                    <p className="text-[10px] leading-tight text-muted-foreground">{t("zemljiških parcel", "land parcels")}</p>
                  </div>
                  <div className="rounded-lg bg-primary/10 p-2">
                    <p className="font-display text-xl font-semibold text-primary">{PS_RECAP_1826.zusammen}</p>
                    <p className="text-[10px] leading-tight text-muted-foreground">{t("skupaj", "total")}</p>
                  </div>
                </div>
                <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
                  {lang === "si" ? PS_RECAP_1826.mostUsefulSi.slice(0, 260) + "…" : PS_RECAP_1826.mostUsefulEn.slice(0, 260) + "…"}
                </p>
              </div>
              <div className="rounded-xl border bg-card p-6 shadow-sm">
                <h4 className="font-display text-base font-semibold">{t("PZ — cenilni elaborat (28. 7. 1825)", "PZ — valuation elaborate (28 Jul 1825)")}</h4>
                <div className="mt-3 grid grid-cols-3 gap-2 text-center">
                  <div className="rounded-lg bg-secondary/40 p-2">
                    <p className="font-display text-xl font-semibold">{PZ_ECONOMY_1825.population.total}</p>
                    <p className="text-[10px] leading-tight text-muted-foreground">{t("prebivalcev", "inhabitants")}</p>
                  </div>
                  <div className="rounded-lg bg-secondary/40 p-2">
                    <p className="font-display text-xl font-semibold">{PZ_ECONOMY_1825.population.houses}</p>
                    <p className="text-[10px] leading-tight text-muted-foreground">{t("hiš [~]", "houses [~]")}</p>
                  </div>
                  <div className="rounded-lg bg-secondary/40 p-2">
                    <p className="font-display text-xl font-semibold">{PZ_ECONOMY_1825.areaTotal.joch}</p>
                    <p className="text-[10px] leading-tight text-muted-foreground">{t("joch [~]", "joch [~]")}</p>
                  </div>
                </div>
                <ul className="mt-3 space-y-1 text-[11px] text-muted-foreground">
                  {PZ_ECONOMY_1825.valuationChain.slice(0, 3).map((v) => (
                    <li key={v.stepSi}>
                      <span className="text-foreground">{v.stepSi}:</span> {v.valuesSi}
                    </li>
                  ))}
                </ul>
                <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                  {lang === "si" ? PZ_ECONOMY_1825.economicProfileSi.slice(0, 200) + "…" : PZ_ECONOMY_1825.economicProfileEn.slice(0, 200) + "…"}
                </p>
              </div>
            </div>

            {/* PUA nadaljevanje */}
            <div className="overflow-hidden rounded-xl border bg-card shadow-sm">
              <div className="border-b bg-secondary/40 px-6 py-4">
                <h4 className="font-display text-base font-semibold">
                  {t(
                    `PUA — nadaljevanje po A–B: strani ${PUA_CONTINUATION.pagesRead[0]}–${PUA_CONTINUATION.pagesRead[PUA_CONTINUATION.pagesRead.length - 1]}, ${PUA_CONTINUATION.rows.length} vnosov (REVIEW)`,
                    `PUA — continuation after A–B: pages ${PUA_CONTINUATION.pagesRead[0]}–${PUA_CONTINUATION.pagesRead[PUA_CONTINUATION.pagesRead.length - 1]}, ${PUA_CONTINUATION.rows.length} entries (REVIEW)`,
                  )}
                </h4>
                <p className="mt-1 text-[11px] text-muted-foreground">
                  {t(
                    `P4: strani 12–34 (47 vnosov, zap. št. 22–68) · vključno Kirche H. Veith — cerkev sv. Vida [~] · PUA številči hiše drugače kot PT [~] · P5-b: strani 35–49 prebrane (32 vnosov, zap. št. 69–100) — register CEL (101 vnosov); napovedi W-most: h68 POTRJENA (Ulrich Mida), h32 delno v prid, h64/h65 [~]`,
                    `P4: pages 12–34 (47 entries, rows 22–68) · incl. Kirche H. Veith — the church of St. Vitus [~] · PUA numbers houses differently from PT [~] · P5-b: pages 35–49 read (32 entries, rows 69–100) — register COMPLETE (101 entries); W-bridge predictions: h68 CONFIRMED (Ulrich Mida), h32 partially supported, h64/h65 [~]`,
                  )}
                </p>
              </div>
              <div className="max-h-96 divide-y overflow-y-auto">
                {PUA_CONTINUATION.rows.map((r) => (
                  <div key={`pua-${r.page}-${r.row}`} className="grid gap-1 px-6 py-2.5 sm:grid-cols-[80px_1fr_120px_60px]">
                    <p className="font-mono text-[10px] text-muted-foreground">str. {r.page} · v. {r.row}</p>
                    <p className="text-sm text-foreground">{r.nameAsWritten}</p>
                    <p className="font-mono text-xs text-muted-foreground">{r.houseNos.join(", ") || "—"}</p>
                    <p className="font-mono text-[10px] text-muted-foreground">{r.confidence.slice(0, 12)}</p>
                  </div>
                ))}
              </div>
              <ul className="border-t bg-secondary/20 px-6 py-3 space-y-1 text-[11px] leading-relaxed text-muted-foreground">
                {PUA_CONTINUATION.divergences.map((d) => (
                  <li key={d}>• {d}</li>
                ))}
              </ul>
            </div>

            {/* P5 navzkrižna analiza PUA ↔ PT */}
            <div className="rounded-xl border-2 border-primary/30 bg-card p-6 shadow-sm">
              <h4 className="flex items-center gap-2 font-display text-base font-semibold">
                <span className="inline-flex items-center gap-1 rounded-full bg-primary px-2.5 py-0.5 font-mono text-[10px] font-bold text-primary-foreground">P5</span>
                {t(
                  `Navzkrižna analiza PUA ↔ PT — ${PUA_PT_CROSS.date}, deterministična (brez AI)`,
                  `Cross-analysis PUA ↔ PT — ${PUA_PT_CROSS.date}, deterministic (no AI)`,
                )}
              </h4>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">{PUA_PT_CROSS.method}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {[
                  { label: t("PUA vnosov", "PUA entries"), value: PUA_PT_CROSS.counts.puaEntries, cls: "bg-secondary text-muted-foreground" },
                  { label: t("z berljivo hišno št.", "with house no."), value: PUA_PT_CROSS.counts.withReadableHouseNo, cls: "bg-secondary text-muted-foreground" },
                  { label: t("neposrednih ujemanj", "direct matches"), value: PUA_PT_CROSS.counts.directSurnameMatch, cls: "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100" },
                  { label: t("divergenc", "divergences"), value: PUA_PT_CROSS.counts.divergent, cls: "bg-orange-100 text-orange-900 dark:bg-orange-900/60 dark:text-orange-100" },
                  { label: t("priimkov v obeh registrih", "surnames in both"), value: PUA_PT_CROSS.counts.surnamesInBothRegisters, cls: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100" },
                ].map((s) => (
                  <span key={s.label} className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 font-mono text-xs font-semibold ${s.cls}`}>
                    {s.value} {s.label}
                  </span>
                ))}
              </div>
              <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
                <strong className="text-foreground">{t("Ugotovitev:", "Finding:")}</strong>{" "}
                {lang === "si" ? PUA_PT_CROSS.findingSi : PUA_PT_CROSS.findingEn}
              </p>
              <div className="mt-3 overflow-hidden rounded-lg border">
                <div className="max-h-60 overflow-y-auto overflow-x-auto">
                  <table className="w-full min-w-[420px] text-left text-[11px]">
                    <thead className="sticky top-0 bg-secondary/60 backdrop-blur">
                      <tr className="font-mono text-[10px] uppercase tracking-wide text-muted-foreground">
                        <th className="px-3 py-2">{t("PUA priimek", "PUA surname")}</th>
                        <th className="px-3 py-2">{t("PT priimek", "PT surname")}</th>
                        <th className="px-3 py-2">{t("PUA hiše", "PUA houses")}</th>
                        <th className="px-3 py-2">{t("opomba", "note")}</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {PUA_PT_CROSS.surnameOverlaps.map((r) => (
                        <tr key={r.puaSurname} className="align-top">
                          <td className="px-3 py-2 font-mono font-semibold text-foreground">{r.puaSurname}</td>
                          <td className="px-3 py-2 text-muted-foreground">{r.ptSurname}</td>
                          <td className="whitespace-nowrap px-3 py-2 font-mono text-muted-foreground">{r.puaHouses}</td>
                          <td className="px-3 py-2 text-muted-foreground">{r.noteSi}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              <p className="mt-3 rounded-lg bg-amber-50 p-3 text-[11px] leading-relaxed text-muted-foreground dark:bg-amber-950/30">
                <strong className="text-foreground">{t("Omejitve:", "Caveats:")}</strong>{" "}
                {lang === "si" ? PUA_PT_CROSS.caveatsSi : PUA_PT_CROSS.caveatsEn}
              </p>
              <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                <strong className="text-foreground">{t("Naslednji koraki:", "Next steps:")}</strong>{" "}
                {lang === "si" ? PUA_PT_CROSS.nextStepSi : PUA_PT_CROSS.nextStepEn}
              </p>
            </div>

            {/* P5-c W-most PT ↔ PUA */}
            <div className="rounded-xl border-2 border-primary/30 bg-card p-6 shadow-sm">
              <h4 className="flex items-center gap-2 font-display text-base font-semibold">
                <span className="inline-flex items-center gap-1 rounded-full bg-primary px-2.5 py-0.5 font-mono text-[10px] font-bold text-primary-foreground">P5-c</span>
                {t(
                  `W-most PT ↔ PUA — ${PUA_PT_WBRIDGE.date}, deterministična (brez AI)`,
                  `W-bridge PT ↔ PUA — ${PUA_PT_WBRIDGE.date}, deterministic (no AI)`,
                )}
              </h4>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">{PUA_PT_WBRIDGE.method}</p>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                <strong className="text-foreground">{t("Hipoteza:", "Hypothesis:")}</strong>{" "}
                {lang === "si" ? PUA_PT_WBRIDGE.hypothesisSi : PUA_PT_WBRIDGE.hypothesisEn}
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                {[
                  { label: t("PT vrstic z W", "PT rows with W"), value: PUA_PT_WBRIDGE.counts.ptRowsWithW, cls: "bg-secondary text-muted-foreground" },
                  { label: t("različnih W", "distinct W"), value: PUA_PT_WBRIDGE.counts.wDistinct, cls: "bg-secondary text-muted-foreground" },
                  { label: t("z PUA protistrani", "with PUA side"), value: PUA_PT_WBRIDGE.counts.wWithPua, cls: "bg-secondary text-muted-foreground" },
                  { label: t("MATCH ≥ 0,72", "MATCH ≥ 0.72"), value: PUA_PT_WBRIDGE.counts.match, cls: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100" },
                  { label: t("PARTIAL ≥ 0,50", "PARTIAL ≥ 0.50"), value: PUA_PT_WBRIDGE.counts.partial, cls: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100" },
                  { label: t("MISMATCH", "MISMATCH"), value: PUA_PT_WBRIDGE.counts.mismatch, cls: "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100" },
                  { label: t("brez PUA protistrani", "without PUA side"), value: PUA_PT_WBRIDGE.counts.wNoPua, cls: "bg-orange-100 text-orange-900 dark:bg-orange-900/60 dark:text-orange-100" },
                ].map((s) => (
                  <span key={s.label} className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 font-mono text-xs font-semibold ${s.cls}`}>
                    {s.value} {s.label}
                  </span>
                ))}
              </div>
              <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
                <strong className="text-foreground">{t("Ugotovitev:", "Finding:")}</strong>{" "}
                {lang === "si" ? PUA_PT_WBRIDGE.findingSi : PUA_PT_WBRIDGE.findingEn}
              </p>
              <div className="mt-3 overflow-hidden rounded-lg border">
                <div className="max-h-60 overflow-y-auto overflow-x-auto">
                  <table className="w-full min-w-[560px] text-left text-[11px]">
                    <thead className="sticky top-0 bg-secondary/60 backdrop-blur">
                      <tr className="font-mono text-[10px] uppercase tracking-wide text-muted-foreground">
                        <th className="px-3 py-2">W</th>
                        <th className="px-3 py-2">{t("podobnost", "sim")}</th>
                        <th className="px-3 py-2">{t("par (normaliziran)", "pair (normalised)")}</th>
                        <th className="px-3 py-2">PT</th>
                        <th className="px-3 py-2">PUA</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {PUA_PT_WBRIDGE.bestMatches.map((r) => (
                        <tr key={r.w} className="align-top">
                          <td className="whitespace-nowrap px-3 py-2 font-mono font-semibold text-foreground">{r.w}</td>
                          <td className="whitespace-nowrap px-3 py-2 font-mono text-muted-foreground">{r.sim}</td>
                          <td className="whitespace-nowrap px-3 py-2 font-mono text-muted-foreground">{r.pair}</td>
                          <td className="px-3 py-2 text-muted-foreground">{r.ptOwners}</td>
                          <td className="px-3 py-2 text-muted-foreground">{r.puaNames}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              <div className="mt-3 rounded-lg border border-orange-300/60 bg-orange-50 p-3 text-[11px] leading-relaxed dark:border-orange-800/60 dark:bg-orange-950/30">
                <strong className="text-foreground">{t("Napovedi za strani 35–49 — RAZREŠENE po P5-b:", "Predictions for pages 35–49 — RESOLVED after P5-b:")}</strong>
                <ul className="mt-1 space-y-1 text-muted-foreground">
                  {PUA_PT_WBRIDGE.predictions.map((p) => (
                    <li key={p.house} className="flex flex-wrap items-baseline gap-x-1.5">
                      <span className="font-mono font-semibold text-foreground">{p.house}</span>
                      <span
                        className={`inline-flex items-center rounded-full px-1.5 py-0.5 font-mono text-[10px] font-bold ${
                          p.resolved === "POTRJENO"
                            ? "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100"
                            : p.resolved === "DELNO V PRID"
                              ? "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100"
                              : p.resolved === "NEREŠENO"
                                ? "bg-secondary text-muted-foreground"
                                : "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100"
                        }`}
                      >
                        {p.resolved}
                      </span>
                      <span>: {p.expectedOwners}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <p className="mt-3 rounded-lg bg-amber-50 p-3 text-[11px] leading-relaxed text-muted-foreground dark:bg-amber-950/30">
                <strong className="text-foreground">{t("Omejitve:", "Caveats:")}</strong>{" "}
                {lang === "si" ? PUA_PT_WBRIDGE.caveatsSi : PUA_PT_WBRIDGE.caveatsEn}
              </p>
            </div>

            {/* PT pregled */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h4 className="font-display text-base font-semibold">
                {t(
                  `PT — strokovni pregled registra (81/105 potrjenih; popravki aplicirani v P3)`,
                  `PT — professional review of the register (81/105 confirmed; corrections applied in P3)`,
                )}
              </h4>
              <div className="mt-3 flex flex-wrap gap-2">
                {[
                  { label: t("potrjenih", "confirmed"), value: PT_REVIEW_2026.summary.confirmed, cls: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100" },
                  { label: t("popravkov [~]", "corrections [~]"), value: PT_REVIEW_2026.summary.corrections, cls: "bg-orange-100 text-orange-900 dark:bg-orange-900/60 dark:text-orange-100" },
                  { label: t("dodatnih vrstic", "additional rows"), value: PT_REVIEW_2026.summary.additionalRows, cls: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100" },
                  { label: t("nepreberljivih", "illegible"), value: PT_REVIEW_2026.summary.illegible, cls: "bg-secondary text-muted-foreground" },
                ].map((s) => (
                  <span key={s.label} className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 font-mono text-xs font-semibold ${s.cls}`}>
                    {s.value} {s.label}
                  </span>
                ))}
              </div>
              <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
                <strong className="text-foreground">{t("Strukturna ugotovitev:", "Structural finding:")}</strong>{" "}
                {lang === "si" ? PT_REVIEW_2026.structuralFindingSi : PT_REVIEW_2026.structuralFindingEn}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                {lang === "si" ? PT_REVIEW_2026.decisionSi : PT_REVIEW_2026.decisionEn}
              </p>
            </div>

            {/* P3 paleografska preverba — 2. krog */}
            <div className="rounded-xl border-2 border-primary/30 bg-card p-6 shadow-sm">
              <h4 className="flex items-center gap-2 font-display text-base font-semibold">
                <span className="inline-flex items-center gap-1 rounded-full bg-primary px-2.5 py-0.5 font-mono text-[10px] font-bold text-primary-foreground">P3</span>
                {t(
                  `Paleografska preverba PT — 2. krog (${PT_PALEOGRAPHY_P3.date}, ${PT_PALEOGRAPHY_P3.vlmCalls} VLM klicev, črka-za-črko)`,
                  `Palaeographic verification of PT — 2nd pass (${PT_PALEOGRAPHY_P3.date}, ${PT_PALEOGRAPHY_P3.vlmCalls} VLM calls, letter-by-letter)`,
                )}
              </h4>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                {lang === "si" ? PT_PALEOGRAPHY_P3.methodSi : PT_PALEOGRAPHY_P3.methodEn}
              </p>
              <div className="mt-3 overflow-hidden rounded-lg border">
                <div className="max-h-96 overflow-y-auto overflow-x-auto">
                  <table className="w-full min-w-[420px] text-left text-[11px]">
                    <thead className="sticky top-0 bg-secondary/60 backdrop-blur">
                      <tr className="font-mono text-[10px] uppercase tracking-wide text-muted-foreground">
                        <th className="px-3 py-2">{t("hiša", "house")}</th>
                        <th className="px-3 py-2">{t("prej", "before")}</th>
                        <th className="px-3 py-2">{t("2. krog", "2nd pass")}</th>
                        <th className="px-3 py-2">{t("verdikt", "verdict")}</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {PT_PALEOGRAPHY_P3.pass2Rows.map((r) => (
                        <tr key={r.houseNo} className="align-top">
                          <td className="whitespace-nowrap px-3 py-2 font-mono font-semibold text-foreground">{r.houseNo}</td>
                          <td className="px-3 py-2 text-muted-foreground">{r.before}</td>
                          <td className="px-3 py-2 text-foreground">{r.pass2}</td>
                          <td className={`px-3 py-2 font-medium ${r.verdict.includes("OSTAJA") ? "text-orange-700 dark:text-orange-300" : "text-emerald-700 dark:text-emerald-300"}`}>{r.verdict}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              <p className="mt-3 rounded-lg bg-secondary/40 p-3 text-xs leading-relaxed text-muted-foreground">
                {lang === "si" ? PT_PALEOGRAPHY_P3.appliedSi : PT_PALEOGRAPHY_P3.appliedEn}
              </p>
              <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
                {lang === "si" ? PT_PALEOGRAPHY_P3.integritySi : PT_PALEOGRAPHY_P3.integrityEn}
              </p>
            </div>

            {/* ustna zgodovina protokol */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h4 className="flex items-center gap-2 font-display text-base font-semibold">
                <MessageSquareQuote className="size-4 text-primary" aria-hidden="true" />
                {t(
                  `Ustna zgodovina — protokol v${ORAL_HISTORY_PROTOCOL.version} (${ORAL_HISTORY_PROTOCOL.stages.length} faze, intervjujev: ${ORAL_INTERVIEWS.length})`,
                  `Oral history — protocol v${ORAL_HISTORY_PROTOCOL.version} (${ORAL_HISTORY_PROTOCOL.stages.length} stages, interviews: ${ORAL_INTERVIEWS.length})`,
                )}
              </h4>
              <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {ORAL_HISTORY_PROTOCOL.stages.map((s) => (
                  <div key={s.no} className="rounded-lg bg-secondary/30 p-3">
                    <p className="font-mono text-[10px] text-muted-foreground">{t("faza", "stage")} {s.no}</p>
                    <p className="text-sm font-semibold text-foreground">{lang === "si" ? s.nameSi : s.nameEn}</p>
                    <p className="mt-1 text-[11px] leading-tight text-muted-foreground">
                      {(lang === "si" ? s.descSi : s.descEn).slice(0, 140)}…
                    </p>
                  </div>
                ))}
              </div>
              <ul className="mt-3 space-y-1 text-[11px] leading-relaxed text-muted-foreground">
                {ORAL_HISTORY_PROTOCOL.rulesSi.slice(0, 3).map((r, i) => (
                  <li key={r}>• {lang === "si" ? r : ORAL_HISTORY_PROTOCOL.rulesEn[i]}</li>
                ))}
              </ul>
            </div>

            {/* web verifikacije */}
            <div className="overflow-hidden rounded-xl border bg-card shadow-sm">
              <div className="border-b bg-secondary/40 px-6 py-4">
                <h4 className="font-display text-base font-semibold">
                  {t(
                    `Verifikacija virov na spletu (${WEB_VERIFICATIONS.length} ciljev, 2026-10-08)`,
                    `Web verification of sources (${WEB_VERIFICATIONS.length} targets, 2026-10-08)`,
                  )}
                </h4>
              </div>
              <div className="max-h-96 divide-y overflow-y-auto">
                {WEB_VERIFICATIONS.map((w) => (
                  <div key={w.target} className="flex flex-wrap items-center justify-between gap-2 px-6 py-3">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-semibold text-foreground">{w.target}</p>
                      <p className="mt-0.5 text-[11px] leading-relaxed text-muted-foreground">{w.findingSi.slice(0, 220)}{w.findingSi.length > 220 ? "…" : ""}</p>
                      <a href={w.url} target="_blank" rel="noopener noreferrer" className="mt-0.5 inline-flex items-center gap-1 font-mono text-[10px] text-primary hover:underline">
                        <ExternalLink className="size-3" aria-hidden="true" /> {w.url.slice(0, 72)}
                      </a>
                    </div>
                    <StatusBadge status={w.status} />
                  </div>
                ))}
              </div>
            </div>

            {/* matrika pred/zares */}
            <div className="overflow-hidden rounded-xl border bg-card shadow-sm">
              <div className="border-b bg-secondary/40 px-6 py-4">
                <h4 className="font-display text-base font-semibold">
                  {t("Matrika pred → po (številke iz datotek)", "Matrix before → after (numbers from files)")}
                </h4>
              </div>
              <div className="divide-y">
                {ISSUE17_MATRIX.map((r) => (
                  <div key={r.areaSi} className="grid gap-2 px-6 py-3 md:grid-cols-[120px_1fr_1.3fr_110px]">
                    <p className="text-sm font-semibold text-foreground">{r.areaSi}</p>
                    <p className="text-xs text-muted-foreground">{r.beforeSi}</p>
                    <p className="text-xs text-foreground/90">{r.afterSi}</p>
                    <p className="font-mono text-[10px] text-primary">{r.delta}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* ostaja odprto */}
            <div className="rounded-xl border border-orange-200 bg-orange-50 p-6 shadow-sm dark:border-orange-900/60 dark:bg-orange-950/30">
              <h4 className="font-display text-base font-semibold text-orange-900 dark:text-orange-200">
                {t("Kaj ostaja odprto (pošteno)", "What remains open (honest)")}
              </h4>
              <p className="mt-2 text-xs leading-relaxed text-orange-900 dark:text-orange-200">
                {lang === "si" ? ISSUE17_AUDIT.stillOpenSi : ISSUE17_AUDIT.stillOpenEn}
              </p>
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
}
