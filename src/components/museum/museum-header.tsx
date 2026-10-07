"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Landmark, Menu, X, Globe, Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import { useLang } from "./language-context";
import { STATS } from "@/lib/museum";

const NAV = [
  { href: "#register", si: "Zbirka", en: "Collection" },
  { href: "#timeline", si: "Časovnica", en: "Timeline" },
  { href: "#zemljevid", si: "Zemljevid", en: "Map" },
  { href: "#atlas", si: "Atlas 1825", en: "Atlas 1825" },
  { href: "#vodic", si: "AR vodnik", en: "AR guide" },
  { href: "#stories", si: "Zgodbe", en: "Stories" },
  { href: "#events", si: "Dogodki", en: "Events" },
  { href: "#o-muzeju", si: "O muzeju", en: "About" },
];

export function MuseumHeader() {
  const { t, lang, setLang } = useLang();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { theme, setTheme } = useTheme();
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-40 border-b transition-all ${
        scrolled
          ? "border-border/70 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80"
          : "border-transparent bg-background"
      }`}
    >
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-3 px-4 sm:px-6">
        <Link href="#vsebina" className="flex items-center gap-3" aria-label={t("Muzej vasi Griblje", "Griblje Village Museum")}>
          <span className="flex size-9 items-center justify-center rounded-lg border border-primary/30 bg-primary/10 text-primary">
            <Landmark className="size-5" aria-hidden="true" />
          </span>
          <span className="leading-tight">
            <span className="block font-display text-base font-semibold tracking-tight">
              {t("Muzej vasi Griblje", "Griblje Village Museum")}
            </span>
            <span className="block text-[11px] text-muted-foreground">
              {t("Digitalni muzej resnične vasi ob Kolpi", "A digital museum of a real village on the Kolpa")}
            </span>
          </span>
        </Link>

        <nav className="hidden items-center gap-1 md:flex" aria-label={t("Glavna navigacija", "Main navigation")}>
          {NAV.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
            >
              {t(item.si, item.en)}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setLang(lang === "si" ? "en" : "si")}
            className="flex h-9 items-center gap-1.5 rounded-md border border-border px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
            aria-label={t("Preklopi jezik", "Switch language")}
          >
            <Globe className="size-3.5" aria-hidden="true" />
            {lang === "si" ? "EN" : "SI"}
          </button>
          <button
            type="button"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="flex size-9 items-center justify-center rounded-md border border-border text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
            aria-label={t("Preklopi temni način", "Toggle dark mode")}
          >
            <Sun className="hidden size-4 dark:block" aria-hidden="true" />
            <Moon className="block size-4 dark:hidden" aria-hidden="true" />
          </button>
          <Button
            variant="outline"
            size="icon"
            className="md:hidden"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-label={t("Odpri meni", "Open menu")}
          >
            {open ? <X className="size-4" /> : <Menu className="size-4" />}
          </Button>
        </div>
      </div>

      {open && (
        <nav className="border-t bg-background px-4 py-3 md:hidden" aria-label={t("Mobilna navigacija", "Mobile navigation")}>
          <ul className="grid gap-1">
            {NAV.map((item) => (
              <li key={item.href}>
                <a
                  href={item.href}
                  onClick={() => setOpen(false)}
                  className="flex min-h-11 items-center rounded-md px-3 text-sm font-medium text-foreground/90 hover:bg-secondary"
                >
                  {t(item.si, item.en)}
                </a>
              </li>
            ))}
          </ul>
          <p className="mt-3 px-3 text-[11px] text-muted-foreground">
            {t(
              `${STATS.exhibits} zapisov · ${STATS.sources} virov · 1468 → danes`,
              `${STATS.exhibits} records · ${STATS.sources} sources · 1468 → present`,
            )}
          </p>
        </nav>
      )}
    </header>
  );
}
