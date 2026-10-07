"use client";

import { motion } from "framer-motion";
import { Database, ShieldCheck, Landmark, FileJson, Scale, Accessibility } from "lucide-react";
import { useLang } from "./language-context";
import { evidenceScale, EVIDENCE_LABELS, STATS, type EvidenceCode } from "@/lib/museum";

export function MuseumAbout() {
  const { t } = useLang();

  return (
    <section id="o-muzeju" className="scroll-mt-20 border-t border-border/60" aria-labelledby="o-muzeju-naslov">
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <h2 id="o-muzeju-naslov" className="font-display text-3xl font-semibold tracking-tight">
          {t("O muzeju", "About the museum")}
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
          {t(
            "Muzej vasi Griblje je večjezični digitalni muzej resnične vasi v Beli krajini. Ustanovljen 2026, licenca vsebine CC BY-SA 4.0.",
            "The Griblje Village Museum is a multilingual digital museum of a real village in Bela krajina. Established 2026, content license CC BY-SA 4.0.",
          )}
        </p>

        <div className="mt-8 grid gap-4 lg:grid-cols-3">
          {/* lestvica zanesljivosti */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            className="rounded-xl border bg-card p-6 shadow-sm"
            aria-labelledby="lestvica"
          >
            <h3 id="lestvica" className="flex items-center gap-2 font-display text-lg font-semibold">
              <Scale className="size-4 text-primary" aria-hidden="true" />
              {t("Lestvica zanesljivosti", "Reliability scale")}
            </h3>
            <ul className="mt-4 space-y-3">
              {evidenceScale.map((level) => {
                const meta = EVIDENCE_LABELS[level.code as EvidenceCode];
                return (
                  <li key={level.code} className="flex flex-col gap-0.5">
                    <span className="inline-flex items-center gap-2 text-sm font-medium text-foreground">
                      <ShieldCheck className="size-3.5 text-primary" aria-hidden="true" />
                      {t(level.labelSi, level.labelEn)}
                    </span>
                    {meta && (
                      <span className="pl-6 text-xs leading-relaxed text-muted-foreground">
                        {t(meta.descSi, meta.descEn)}
                      </span>
                    )}
                  </li>
                );
              })}
            </ul>
          </motion.div>

          {/* odprti podatki */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ delay: 0.08 }}
            className="rounded-xl border bg-card p-6 shadow-sm"
            aria-labelledby="podatki"
          >
            <h3 id="podatki" className="flex items-center gap-2 font-display text-lg font-semibold">
              <Database className="size-4 text-primary" aria-hidden="true" />
              {t("Odprti podatki", "Open data")}
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-foreground/85">
              {t(
                `Celotna zbirka — ${STATS.exhibits} zapisov in ${STATS.sources} virov — je javno dostopna v JSON obliki, skupaj z Atlasom 1825, provenienčnim poročilom in testi kakovosti. Zemljevidski podatki © OpenStreetMap prispevali.`,
                `The entire collection — ${STATS.exhibits} records and ${STATS.sources} sources — is publicly available as JSON, together with the 1825 Atlas, the provenance report and the QA tests. Map data © OpenStreetMap contributors.`,
              )}
            </p>
            <ul className="mt-4 grid gap-2 sm:grid-cols-2">
              {[
                { href: "/api/exhibits", label: "/api/exhibits", si: "zbirka 113", en: "collection 113" },
                { href: "/api/events", label: "/api/events", si: "dogodki", en: "events" },
                { href: "/api/opendata", label: "/api/opendata", si: "odprti podatki + licence", en: "open data + licenses" },
                { href: "/api/atlas", label: "/api/atlas", si: "ATLAS 1825 (hiše, lastniki)", en: "ATLAS 1825 (houses, owners)" },
                { href: "/api/provenance", label: "/api/provenance", si: "provinienčni audit", en: "provenance audit" },
                { href: "/api/coverage", label: "/api/coverage", si: "coverage + 3D/AR", en: "coverage + 3D/AR" },
                { href: "/api/qa", label: "/api/qa", si: "testi kakovosti (11)", en: "quality tests (11)" },
                { href: "/api/atlas/reconciliation", label: "/api/atlas/reconciliation", si: "zero-loss uskladitev", en: "zero-loss reconciliation" },
              ].map((l) => (
                <li key={l.href}>
                  <a
                    href={l.href}
                    className="flex min-h-11 items-center gap-2 rounded-lg border px-3 py-2 font-mono text-xs text-primary transition-colors hover:border-primary/40 hover:bg-secondary"
                    title={t(l.si, l.en)}
                  >
                    <FileJson className="size-3.5 shrink-0" aria-hidden="true" />
                    <span className="min-w-0 break-all">{l.label}</span>
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* dostopnost */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ delay: 0.16 }}
            className="rounded-xl border bg-card p-6 shadow-sm"
            aria-labelledby="dostopnost"
          >
            <h3 id="dostopnost" className="flex items-center gap-2 font-display text-lg font-semibold">
              <Accessibility className="size-4 text-primary" aria-hidden="true" />
              {t("Dostopnost", "Accessibility")}
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-foreground/85">
              {t(
                "Spletišče sledi priporočilom WCAG 2.1 AA: semantična zgradba, tipkovna navigacija, opisi slik in spoštovanje sistemske teme. Izjava o dostopnosti: delno skladno.",
                "The site follows WCAG 2.1 AA recommendations: semantic structure, keyboard navigation, image descriptions and system theme respect. Accessibility statement: partially conformant.",
              )}
            </p>
            <dl className="mt-4 grid grid-cols-2 gap-3 text-sm">
              <div>
                <dt className="text-xs text-muted-foreground">{t("Zbirke", "Collections")}</dt>
                <dd className="font-display text-xl font-semibold">6</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">{t("Jeziki", "Languages")}</dt>
                <dd className="font-display text-xl font-semibold">SI · EN</dd>
              </div>
            </dl>
          </motion.div>
        </div>

        <div className="mt-8 flex flex-wrap items-center gap-3 rounded-xl border border-primary/30 bg-primary/5 p-5">
          <Landmark className="size-5 text-primary" aria-hidden="true" />
          <p className="text-sm leading-relaxed text-foreground/85">
            {t(
              "Digitalna sestra fizičnega muzeja v Gribljah — muzejska učilnica, QR oznaki in fizični registrator. Vsak domačin lahko doda svoj vir.",
              "The digital sister of the physical museum in Griblje — museum classroom, QR labels and the physical register. Every local can add their own source.",
            )}
          </p>
        </div>
      </div>
    </section>
  );
}
