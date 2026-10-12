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
  Database,
  ExternalLink,
  FileJson,
  FileX2,
  GraduationCap,
  Landmark,
  Map as MapIcon,
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
