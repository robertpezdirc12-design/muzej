"use client";

import { useCallback, useEffect, useState } from "react";
import { ThemeProvider } from "next-themes";
import { LangProvider, useLang } from "@/components/museum/language-context";
import { MuseumHeader } from "@/components/museum/museum-header";
import { MuseumHero } from "@/components/museum/museum-hero";
import { MuseumRegister } from "@/components/museum/museum-register";
import { MuseumTimeline } from "@/components/museum/museum-timeline";
import { MuseumMap } from "@/components/museum/museum-map";
import { MuseumStories, MuseumEvents } from "@/components/museum/museum-stories-events";
import { MuseumAbout } from "@/components/museum/museum-about";
import { MuseumFooter } from "@/components/museum/museum-footer";
import { ExhibitDetail } from "@/components/museum/exhibit-detail";
import { getExhibit } from "@/lib/museum";

const DEFAULT_TITLE = "Muzej vasi Griblje — digitalni muzej vasi ob Kolpi";

function MuseumIntro({ done }: { done: boolean }) {
  const { t } = useLang();
  return (
    <div
      aria-hidden={done}
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center gap-4 bg-background transition-opacity duration-700 ${
        done ? "pointer-events-none opacity-0" : "opacity-100"
      }`}
    >
      <div className="relative flex size-16 items-center justify-center">
        <span className="absolute inset-0 animate-ping rounded-full border border-primary/30" />
        <span className="flex size-12 items-center justify-center rounded-full border border-primary/40 bg-primary/10 font-display text-lg font-semibold text-primary">
          MV
        </span>
      </div>
      <p className="font-display text-lg font-semibold tracking-tight">
        {t("Odpiram muzej …", "Opening the museum …")}
      </p>
      <p className="text-xs text-muted-foreground">
        {t("Nalaganje zbirke …", "Loading the collection …")}
      </p>
    </div>
  );
}

function MuseumApp() {
  const [activeSlug, setActiveSlug] = useState<string | null>(null);
  const [introDone, setIntroDone] = useState(false);
  const { lang } = useLang();

  /* naslov zavihka sledi odprtemu zapisu (deljenje / zaznamki / zgodovina) */
  useEffect(() => {
    const ex = activeSlug ? getExhibit(activeSlug) : undefined;
    if (ex) {
      const title = lang === "si" ? ex.titleSi : ex.titleEn;
      document.title = `${ex.museumNo} — ${title} · Muzej vasi Griblje`;
    } else {
      document.title = DEFAULT_TITLE;
    }
  }, [activeSlug, lang]);

  /* uvodni zaslon — kot v izvirniku; nato odpremo globo povezavo ?exponat=slug */
  useEffect(() => {
    const t1 = window.setTimeout(() => {
      setIntroDone(true);
      const params = new URLSearchParams(window.location.search);
      const slug = params.get("exponat");
      if (slug) setActiveSlug(slug);
    }, 900);
    return () => window.clearTimeout(t1);
  }, []);

  const openExhibit = useCallback((slug: string) => {
    setActiveSlug(slug);
    const url = new URL(window.location.href);
    url.searchParams.set("exponat", slug);
    window.history.replaceState(null, "", url);
  }, []);

  const closeExhibit = useCallback(() => {
    setActiveSlug(null);
    const url = new URL(window.location.href);
    url.searchParams.delete("exponat");
    window.history.replaceState(null, "", url);
  }, []);

  return (
    <div className="flex min-h-screen flex-col">
      <MuseumIntro done={introDone} />
      <a
        href="#vsebina"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-primary-foreground"
      >
        Preskoči na vsebino
      </a>
      <MuseumHeader />
      <main id="vsebina" className="flex-1">
        <MuseumHero />
        <MuseumRegister onOpen={openExhibit} />
        <MuseumTimeline onOpen={openExhibit} />
        <MuseumMap onOpen={openExhibit} />
        <MuseumStories />
        <MuseumEvents />
        <MuseumAbout />
      </main>
      <MuseumFooter />
      <ExhibitDetail slug={activeSlug} onClose={closeExhibit} onOpen={openExhibit} />
    </div>
  );
}

export default function Home() {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
      <LangProvider>
        <MuseumApp />
      </LangProvider>
    </ThemeProvider>
  );
}
