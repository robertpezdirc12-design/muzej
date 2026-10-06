"use client";

import Link from "next/link";
import { Landmark } from "lucide-react";
import { useLang } from "./language-context";
import { STATS } from "@/lib/museum";

export function MuseumFooter() {
  const { t } = useLang();

  return (
    <footer className="mt-auto border-t bg-secondary/40">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <div className="grid gap-8 md:grid-cols-[1.4fr_1fr_1fr]">
          <div>
            <div className="flex items-center gap-3">
              <span className="flex size-9 items-center justify-center rounded-lg border border-primary/30 bg-primary/10 text-primary">
                <Landmark className="size-5" aria-hidden="true" />
              </span>
              <div className="leading-tight">
                <p className="font-display text-base font-semibold">
                  {t("Muzej vasi Griblje", "Griblje Village Museum")}
                </p>
                <p className="text-[11px] text-muted-foreground">
                  {t("Digitalni muzej resnične vasi ob Kolpi", "A digital museum of a real village on the Kolpa")}
                </p>
              </div>
            </div>
            <p className="mt-4 max-w-sm text-xs leading-relaxed text-muted-foreground">
              {t(
                "Razpoložljivo v slovenščini in angleščini. Vsebina zbirke pod licenco CC BY-SA 4.0 · Zemljevid © OpenStreetMap prispevali.",
                "Available in Slovenian and English. Collection content under CC BY-SA 4.0 · Map © OpenStreetMap contributors.",
              )}
            </p>
          </div>

          <nav aria-label={t("Ogled", "Browse")}>
            <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {t("Ogled", "Browse")}
            </h2>
            <ul className="mt-3 space-y-2">
              {[
                { href: "#register", si: "Domov", en: "Home" },
                { href: "#register", si: "Zbirka", en: "Collection" },
                { href: "#timeline", si: "Časovnica", en: "Timeline" },
                { href: "#stories", si: "Zgodbe", en: "Stories" },
                { href: "#events", si: "Dogodki", en: "Events" },
              ].map((l) => (
                <li key={l.si}>
                  <a href={l.href} className="text-sm text-foreground/80 transition-colors hover:text-primary">
                    {t(l.si, l.en)}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          <nav aria-label={t("Podatki", "Data")}>
            <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {t("Podatki", "Data")}
            </h2>
            <ul className="mt-3 space-y-2">
              <li>
                <a href="/api/exhibits" className="text-sm text-foreground/80 transition-colors hover:text-primary">
                  {t("Odprti podatki (JSON)", "Open data (JSON)")}
                </a>
              </li>
              <li>
                <a href="/api/opendata" className="text-sm text-foreground/80 transition-colors hover:text-primary">
                  /api/opendata
                </a>
              </li>
              <li>
                <a href="#o-muzeju" className="text-sm text-foreground/80 transition-colors hover:text-primary">
                  {t("Izjava o dostopnosti", "Accessibility statement")}
                </a>
              </li>
            </ul>
          </nav>
        </div>

        <div className="mt-8 flex flex-wrap items-center justify-between gap-2 border-t pt-6 text-[11px] text-muted-foreground">
          <p>
            © 2026 · {t("Digitalni muzej · postavitev 2026", "Digital museum · established 2026")}
          </p>
          <p>
            {t(
              `${STATS.exhibits} zapisov · ${STATS.sources} virov · 1468 → danes`,
              `${STATS.exhibits} records · ${STATS.sources} sources · 1468 → present`,
            )}
          </p>
          <Link href="#vsebina" className="underline decoration-border underline-offset-2 hover:text-foreground">
            {t("Na začetek", "Back to top")}
          </Link>
        </div>
      </div>
    </footer>
  );
}
