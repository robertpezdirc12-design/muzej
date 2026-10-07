"use client";

/**
 * COVERAGE ZBIRKE IN 3D/AR PRIPRAVA (GitLab issue #4 — zaključek obnove).
 *
 * Vse številke se izračunajo iz dejanskega podatkovnega modelja
 * (exhibits.json + Atlas): nobena številka ni ročno vpisana.
 *  - coverage 113 zapisov: GPS, slike, 3D, viri, evidenceStatus, obdobja
 *  - sistematična 3D/AR priprava: ORIGINAL/DERIVAT/RECONSTRUCTED/INFERRED
 *  - end-to-end QA testi (11) — enaki kot /api/qa
 *  - dokumentirana manjkajoča postaja 32 (NOT_FOUND)
 * Strojno berljivo: /api/coverage, /api/qa.
 */

import { motion } from "framer-motion";
import {
  BadgeCheck,
  Boxes,
  Compass,
  FileQuestion,
  Gauge,
  MapPin,
  ScanLine,
  ShieldCheck,
  XCircle,
} from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { useLang } from "./language-context";
import { computeCoverage, compute3DPipeline } from "@/lib/coverage";
import { runQA } from "@/lib/qa";
import { WALK_GAPS } from "@/lib/walks";

const KLASS_STYLE: Record<string, string> = {
  ORIGINAL: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
  DERIVAT: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100",
  RECONSTRUCTED: "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100",
  INFERRED: "bg-orange-100 text-orange-900 dark:bg-orange-900/60 dark:text-orange-100",
};

function Bar({ value, total, label }: { value: number; total: number; label: string }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;
  return (
    <li>
      <div className="flex items-center justify-between text-xs">
        <span className="text-foreground/85">{label}</span>
        <span className="font-mono text-muted-foreground">
          {value}/{total} · {pct} %
        </span>
      </div>
      <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-secondary">
        <div className="h-full rounded-full bg-primary transition-all" style={{ width: `${pct}%` }} />
      </div>
    </li>
  );
}

export function MuseumCoverage() {
  const { t, lang } = useLang();
  const cov = computeCoverage();
  const pipeline = compute3DPipeline();
  const qa = runQA();
  const gap32 = WALK_GAPS[0];

  return (
    <section id="coverage" className="scroll-mt-20 border-t border-border/60" aria-labelledby="coverage-naslov">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 id="coverage-naslov" className="font-display text-3xl font-semibold tracking-tight">
              {t("Coverage zbirke in 3D/AR", "Collection coverage & 3D/AR")}
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              {t(
                "Končni strojno izračunan pregled: koliko zapisov ima lokacijo, sliko, vir in dokaz — in kako je vzpostavljena pot do 3D/AR za zgodovinske objekte.",
                "The final machine-computed overview: how many records carry a location, image, source and evidence — and how the 3D/AR path for historical objects is set up.",
              )}
            </p>
          </div>
          <div className="flex flex-col items-start gap-1 text-[11px] font-mono text-muted-foreground sm:items-end">
            <a href="/api/coverage" className="inline-flex items-center gap-1 text-primary hover:underline">
              <Gauge className="size-3" aria-hidden="true" /> /api/coverage
            </a>
            <a href="/api/qa" className="inline-flex items-center gap-1 text-primary hover:underline">
              <ShieldCheck className="size-3" aria-hidden="true" /> /api/qa
            </a>
          </div>
        </div>

        <div className="mt-8 grid gap-4 lg:grid-cols-3">
          {/* ——— coverage števci ——— */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            className="min-w-0 rounded-xl border bg-card p-6 shadow-sm"
            aria-labelledby="cov-stevci"
          >
            <h3 id="cov-stevci" className="flex items-center gap-2 font-display text-lg font-semibold">
              <Compass className="size-4 text-primary" aria-hidden="true" />
              {t(`Coverage ${cov.total} zapisov`, `Coverage of ${cov.total} records`)}
            </h3>
            <ul className="mt-4 space-y-3">
              <Bar value={cov.gps.withGps} total={cov.total} label={t("z GPS lokacijo", "with GPS location")} />
              <Bar value={cov.images.withImage} total={cov.total} label={t("s sliko", "with an image")} />
              <Bar value={cov.models3d.with3d} total={cov.total} label={t("z 3D modelom", "with a 3D model")} />
              <Bar value={cov.sources.withSources} total={cov.total} label={t("z vsaj enim virom", "with ≥ 1 source")} />
              <Bar value={cov.arReady.readyNow.length} total={cov.total} label={t("AR pripravljeni (model + GPS)", "AR-ready (model + GPS)")} />
            </ul>
            <div className="mt-4 flex flex-wrap gap-1.5">
              {Object.entries(cov.byEvidence).map(([k, v]) => (
                <span
                  key={k}
                  className="rounded-full bg-secondary px-2 py-0.5 font-mono text-[10px] font-semibold text-secondary-foreground"
                >
                  {k} {v}
                </span>
              ))}
            </div>
          </motion.div>

          {/* ——— po obdobjih ——— */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ delay: 0.08 }}
            className="min-w-0 rounded-xl border bg-card p-6 shadow-sm"
            aria-labelledby="cov-obdobja"
          >
            <h3 id="cov-obdobja" className="flex items-center gap-2 font-display text-lg font-semibold">
              <MapPin className="size-4 text-primary" aria-hidden="true" />
              {t("Po zgodovinskih obdobjih", "By historical period")}
            </h3>
            <ul className="mt-4 max-h-72 space-y-2.5 overflow-y-auto pr-2">
              {cov.byPeriod.map((p) => (
                <Bar key={p.periodSi} value={p.count} total={cov.total} label={lang === "si" ? p.periodSi : p.periodEn} />
              ))}
            </ul>
          </motion.div>

          {/* ——— QA testi ——— */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ delay: 0.16 }}
            className={`min-w-0 rounded-xl border p-6 shadow-sm ${
              qa.ok ? "border-emerald-200 bg-emerald-50/40 dark:border-emerald-900/50 dark:bg-emerald-950/20" : "border-orange-200 bg-orange-50/40 dark:border-orange-900/50 dark:bg-orange-950/20"
            }`}
            aria-labelledby="cov-qa"
          >
            <h3 id="cov-qa" className="flex items-center gap-2 font-display text-lg font-semibold">
              {qa.ok ? (
                <BadgeCheck className="size-4 text-emerald-700 dark:text-emerald-400" aria-hidden="true" />
              ) : (
                <XCircle className="size-4 text-orange-700 dark:text-orange-400" aria-hidden="true" />
              )}
              {t(`End-to-end QA: ${qa.passed}/${qa.tests.length}`, `End-to-end QA: ${qa.passed}/${qa.tests.length}`)}
            </h3>
            <p className="mt-1 text-xs text-muted-foreground">
              {t(
                "Testi tečejo ob vsakem odpiranju strani (enaki kot /api/qa): integriteta, duplikati, AR-GPS, evidence, sprehodi, coverage, zero-loss.",
                "Tests run on every page load (same as /api/qa): integrity, duplicates, AR-GPS, evidence, walks, coverage, zero-loss.",
              )}
            </p>
            <ul className="mt-4 max-h-72 space-y-1.5 overflow-y-auto pr-2">
              {qa.tests.map((test) => (
                <li key={test.id} className="flex items-start gap-2 text-xs">
                  <span className={test.pass ? "text-emerald-700 dark:text-emerald-400" : "text-orange-700 dark:text-orange-400"}>
                    {test.pass ? "✓" : "✗"}
                  </span>
                  <span className="min-w-0">
                    <span className="text-foreground/90">{lang === "si" ? test.nameSi : test.nameEn}</span>
                    <span className="block break-words font-mono text-[10px] leading-snug text-muted-foreground/80" title={test.detail}>
                      {test.detail}
                    </span>
                  </span>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>

        {/* ——— 3D/AR tok ——— */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          className="mt-4 min-w-0 rounded-xl border bg-card p-6 shadow-sm"
          aria-labelledby="cov-3d"
        >
          <h3 id="cov-3d" className="flex items-center gap-2 font-display text-lg font-semibold">
            <Boxes className="size-4 text-primary" aria-hidden="true" />
            {t("Sistematična 3D/AR priprava zgodovinske vasi", "Systematic 3D/AR preparation of the historical village")}
          </h3>
          <p className="mt-1 max-w-3xl text-xs leading-relaxed text-muted-foreground">
            {t(
              "Tok (združen z Atlasom 1825, brez dvojnega vnosa): zgodovinski objekt → dokaz → tipologija → geometrija → 3D rekonstrukcija → lokacija → AR. Ločeno je razvidno, kaj je dokazano in kaj interpretirano; obstoječi model cerkve sv. Vida ostaja delujoč.",
              "Flow (unified with Atlas 1825, no double entry): historical object → evidence → typology → geometry → 3D reconstruction → location → AR. What is proven vs interpreted is kept separate; the existing St. Vitus church model keeps working.",
            )}
          </p>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {pipeline.map((e) => (
              <li key={e.id} className="rounded-lg border bg-secondary/30 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-semibold text-foreground">
                    {lang === "si" ? e.titleSi : e.titleEn}
                  </span>
                  <span
                    className={`inline-flex items-center rounded-full px-2 py-0.5 font-mono text-[10px] font-semibold ${KLASS_STYLE[e.klass]}`}
                  >
                    {e.klass}
                  </span>
                </div>
                <div className="mt-2 flex items-center gap-2">
                  <Progress value={(e.readiness.score / e.readiness.of) * 100} className="h-1.5" aria-label={t("3D pripravljenost", "3D readiness")} />
                  <span className="shrink-0 font-mono text-[10px] text-muted-foreground">
                    {e.readiness.score}/{e.readiness.of}
                  </span>
                </div>
                <p className="mt-2 text-xs leading-relaxed text-foreground/85">
                  <ScanLine className="mr-1 inline size-3 text-emerald-700 dark:text-emerald-400" aria-hidden="true" />
                  {lang === "si" ? e.evidenceSi : e.evidenceEn}
                </p>
                <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                  {lang === "si" ? e.interpretationSi : e.interpretationEn}
                </p>
                <p className="mt-2 font-mono text-[10px] text-muted-foreground/70">
                  {t("vir", "source")}: {e.sourceCode}
                  {e.museumRef ? ` · ${e.museumRef}` : ""}
                </p>
              </li>
            ))}
          </ul>
          <p className="mt-3 text-xs text-muted-foreground">
            {t(
              `Muzejski zapisi s lokacijo brez 3D modela: ${cov.arReady.candidates.length} kandidatov — nov objekt z veljavno identiteto, lokacijo in modelom samodejno vstopi v AR tok.`,
              `Museum records with a location but no 3D model: ${cov.arReady.candidates.length} candidates — a new object with a valid identity, location and model enters the AR flow automatically.`,
            )}
          </p>
        </motion.div>

        {/* ——— postaja 32 ——— */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          className="mt-4 rounded-xl border border-dashed border-border bg-secondary/20 p-6"
          aria-labelledby="cov-32"
        >
          <h3 id="cov-32" className="flex items-center gap-2 font-display text-lg font-semibold text-muted-foreground">
            <FileQuestion className="size-4" aria-hidden="true" />
            {t("Postaja 32 sprehoda »Vas in njeni ljudje« — dokumentirana vrzel", "Station 32 of “The village and its people” — a documented gap")}
          </h3>
          <p className="mt-2 max-w-3xl text-xs leading-relaxed text-muted-foreground">
            {gap32 && (lang === "si" ? gap32.reasonSi : gap32.reasonEn)}
          </p>
          <p className="mt-2 text-[11px] font-mono text-muted-foreground/80">
            {t("Dokaz:", "Evidence:")}{" "}
            <a href="#raziskave" className="underline decoration-dotted hover:text-foreground">
              {gap32?.negativeResultId}
            </a>{" "}
            · {t("zaporedje 1–35 z eksplicitnim mestom 32", "sequence 1–35 with the explicit slot 32")}
          </p>
        </motion.div>
      </div>
    </section>
  );
}
