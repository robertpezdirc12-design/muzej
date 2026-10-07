"use client";

import { useCallback, useEffect, useState } from "react";
import { ThemeProvider } from "next-themes";
import { LangProvider, useLang } from "@/components/museum/language-context";
import { MuseumHeader } from "@/components/museum/museum-header";
import { MuseumHero } from "@/components/museum/museum-hero";
import { MuseumRegister } from "@/components/museum/museum-register";
import { MuseumTimeline } from "@/components/museum/museum-timeline";
import { MuseumMap } from "@/components/museum/museum-map";
import { MuseumAtlas } from "@/components/museum/museum-atlas";
import { MuseumResearch } from "@/components/museum/museum-research";
import { MuseumARGuide } from "@/components/museum/museum-ar";
import { MuseumCoverage } from "@/components/museum/museum-coverage";
import { MuseumStories, MuseumEvents } from "@/components/museum/museum-stories-events";
import { MuseumAbout } from "@/components/museum/museum-about";
import { MuseumFooter } from "@/components/museum/museum-footer";
import { ExhibitDetail } from "@/components/museum/exhibit-detail";
import { getExhibit } from "@/lib/museum";
import { useGeolocation } from "@/hooks/use-geolocation";
import { useTimeMachine, parseYearParam } from "@/lib/time-machine-store";
import { getSpotById } from "@/data/atlas/timespots";
import dynamic from "next/dynamic";

const ARTimeMachine = dynamic(
  () => import("@/components/museum/ar-time-machine").then((m) => m.ARTimeMachine),
  { ssr: false },
);

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

  /* GPS za zemljevid in AR vodnika — deljen med obema odsekom */
  const geo = useGeolocation();

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

  /* uvodni zaslon — kot v izvirniku; nato odpremo globo povezavo ?exponat=slug,
     ?odsek=id (npr. iz PWA bližnjic), ?casovni=1825|1900|danes (3D) ter
     ?spot=<id> AR Time Spota (QR tablice na lokaciji, issue #11) in
     &360=1 za virtualni 360° pogled s cerkve (issue #12) */
  useEffect(() => {
    const t1 = window.setTimeout(() => {
      setIntroDone(true);
      const params = new URLSearchParams(window.location.search);
      const slug = params.get("exponat");
      if (slug) {
        setActiveSlug(slug);
      } else {
        const spot = getSpotById(params.get("spot"));
        const casovni = parseYearParam(params.get("casovni")) ?? spot?.year ?? null;
        if (casovni) {
          const p360 = params.get("360") === "1";
          useTimeMachine.getState().openTM(casovni, spot?.id ?? null, p360);
        } else {
          const odsek = params.get("odsek");
          if (odsek) {
            const el = document.getElementById(odsek);
            if (el) el.scrollIntoView({ behavior: "auto", block: "start" });
          }
        }
      }
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
        <MuseumMap userFix={geo.fix} onOpen={openExhibit} />
        <MuseumAtlas userFix={geo.fix} onOpenMuseum={openExhibit} />
        <MuseumResearch />
        <MuseumARGuide geo={geo} onOpen={openExhibit} />
        <MuseumCoverage />
        <MuseumStories />
        <MuseumEvents />
        <MuseumAbout />
      </main>
      <MuseumFooter />
      <ExhibitDetail slug={activeSlug} onClose={closeExhibit} onOpen={openExhibit} />
      <ARTimeMachineGate geo={geo} onOpenExhibit={openExhibit} />
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

/* vratnica: AR časovni stroj se montira šele, ko je odprt (three.js izven
   glavnega snopa, kamera/GPS senzorji samo po potrebi) */
function ARTimeMachineGate({
  geo,
  onOpenExhibit,
}: {
  geo: ReturnType<typeof useGeolocation>;
  onOpenExhibit: (slug: string) => void;
}) {
  const open = useTimeMachine((s) => s.open);
  if (!open) return null;
  return <ARTimeMachine geo={geo} onOpenExhibit={onOpenExhibit} />;
}
