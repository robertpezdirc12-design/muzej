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
  PZ_ECONOMY_1825,
  PUA_CONTINUATION,
  PT_REVIEW_2026,
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4">
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

            <div className="grid gap-4 lg:grid-cols-2">
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
                  {t("Licence virov (589 vrstic)", "Source licenses (589 rows)")}
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4">
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4">
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4">
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4 lg:grid-cols-2">
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
                {t("Zemljevid 1812 — dokumentiran vir + pot do georeference", "Map 1812 — documented source + path to georeference")}
              </h3>
              <p className="mt-2 text-xs leading-relaxed text-foreground/80">
                {t(
                  `Slika v zbirki (${MAP_1812.museumRef}) je sodoben vektorski zemljevid: ${MAP_1812.actualSource.author}, ${MAP_1812.actualSource.year}, ${MAP_1812.actualSource.licence}.`,
                  `The collection image (${MAP_1812.museumRef}) is a modern vector map: ${MAP_1812.actualSource.author}, ${MAP_1812.actualSource.year}, ${MAP_1812.actualSource.licence}.`,
                )}
              </p>
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4">
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4">
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
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 grid gap-4">
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
              <div className="max-h-96 overflow-y-auto">
                <table className="w-full text-sm">
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
            <div className="grid gap-4 lg:grid-cols-3">
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
                    `PUA — nadaljevanje po A–B: strani 3–10, ${PUA_CONTINUATION.rows.length} vnosov (REVIEW)`,
                    `PUA — continuation after A–B: pages 3–10, ${PUA_CONTINUATION.rows.length} entries (REVIEW)`,
                  )}
                </h4>
              </div>
              <div className="max-h-72 divide-y overflow-y-auto">
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

            {/* PT pregled */}
            <div className="rounded-xl border bg-card p-6 shadow-sm">
              <h4 className="font-display text-base font-semibold">
                {t(
                  `PT — strokovni pregled registra (81/105 potrjenih, register nespremenjen)`,
                  `PT — professional review of the register (81/105 confirmed, register unchanged)`,
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
