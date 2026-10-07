"use client";

import { useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { Map, Sparkles } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { useLang } from "./language-context";
import { exhibits as allExhibits } from "@/lib/museum";

const MapCanvas = dynamic(
  () => import("./museum-map-canvas").then((m) => m.MapCanvas),
  {
    ssr: false,
    loading: () => (
      <div className="h-[360px] w-full animate-pulse rounded-xl border bg-secondary/50 sm:h-[420px]" />
    ),
  },
);

const MIN_YEAR = 1468;
const MAX_YEAR = 2026;

export function MuseumMap({ onOpen }: { onOpen: (slug: string) => void }) {
  const { t, lang } = useLang();
  const [vintage, setVintage] = useState(false);
  const [timeTravel, setTimeTravel] = useState(false);
  const [year, setYear] = useState(MAX_YEAR);

  const located = useMemo(
    () => allExhibits.filter((e) => e.lat && e.lng),
    [],
  );

  /* pri časovnem potovanju pokažemo zapise, ki so letnica obstajali;
     neznane letnice (null) obravnavamo kot »obstaja v ves času« */
  const visible = useMemo(() => {
    if (!timeTravel) return located;
    return located.filter(
      (e) =>
        (e.yearFrom ?? -Infinity) <= year &&
        (e.yearTo ?? Infinity) >= year,
    );
  }, [located, timeTravel, year]);

  return (
    <section
      id="zemljevid"
      className="scroll-mt-20 border-t border-border/60"
      aria-labelledby="zemljevid-naslov"
    >
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <h2
          id="zemljevid-naslov"
          className="flex items-center gap-3 font-display text-3xl font-semibold tracking-tight"
        >
          <Map className="size-7 text-primary" aria-hidden="true" />
          {t("Vas na zemljevidu", "The village on the map")}
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
          {t(
            "Od Griblacha leta 1468 do današnjih hiš — zapisi zbirke na karti kraja. Kliknite klinček in zapis se odpre.",
            "From Griblach in 1468 to the houses of today — collection records on the map of the place. Click a pin to open a record.",
          )}{" "}
          <button
            type="button"
            onClick={() => onOpen("stari-zemljevidi")}
            className="inline-flex items-center gap-1 font-medium text-primary underline decoration-border underline-offset-2 hover:decoration-primary"
          >
            {t("kako je vas prišla na papir", "how the village reached paper")}
            <Sparkles className="size-3" aria-hidden="true" />
          </button>
        </p>

        <div className="mt-6 flex flex-wrap items-center gap-x-8 gap-y-4 rounded-xl border bg-card p-4">
          <div className="flex items-center gap-3">
            <Switch
              id="pogled-zemljevid"
              checked={vintage}
              onCheckedChange={setVintage}
            />
            <Label
              htmlFor="pogled-zemljevid"
              className="cursor-pointer text-sm font-medium leading-tight"
            >
              {t("Zgodovinski pogled", "Historical view")}
              <span className="block text-xs font-normal text-muted-foreground">
                {t("kartiraj kot leta 1825", "mapped as in 1825")}
              </span>
            </Label>
          </div>

          <div className="flex items-center gap-3">
            <Switch
              id="casovno-potovanje"
              checked={timeTravel}
              onCheckedChange={(v) => {
                setTimeTravel(v);
                if (v) setYear((y) => Math.min(Math.max(y, MIN_YEAR), MAX_YEAR));
              }}
            />
            <Label
              htmlFor="casovno-potovanje"
              className="cursor-pointer text-sm font-medium leading-tight"
            >
              {t("Časovno potovanje", "Time travel")}
              <span className="block text-xs font-normal text-muted-foreground">
                {t("pokaži le zapise, obstoječe tistega leta", "show only records existing that year")}
              </span>
            </Label>
          </div>

          <div
            className={`flex min-w-56 flex-1 flex-col gap-1.5 transition-opacity ${
              timeTravel ? "opacity-100" : "pointer-events-none opacity-40"
            }`}
            aria-disabled={!timeTravel}
          >
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>{MIN_YEAR}</span>
              <span className="font-mono text-sm font-semibold text-primary">
                {timeTravel ? year : "—"}
              </span>
              <span>{MAX_YEAR}</span>
            </div>
            <input
              type="range"
              min={MIN_YEAR}
              max={MAX_YEAR}
              step={1}
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              aria-label={t("Leto prikaza", "Year to display")}
              className="h-2 w-full cursor-pointer accent-[color-mix(in_oklch,var(--primary)_80%,black)]"
            />
          </div>

          <p className="text-xs text-muted-foreground" aria-live="polite">
            {t(
              `Na zemljevidu: ${visible.length} od ${located.length} zapisov`,
              `On the map: ${visible.length} of ${located.length} records`,
            )}
          </p>
        </div>

        <div className="mt-4">
          <MapCanvas exhibits={visible} vintage={vintage} onOpen={onOpen} />
        </div>

        {timeTravel && (
          <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
            {t(
              "Leto je vodilo po letnicah zapisov (»od – do«); zapisi brez znane letnice ostanejo na karti.",
              "The year follows record dates (“from – to”); records without a known year stay on the map.",
            )}
          </p>
        )}
      </div>
    </section>
  );
}
