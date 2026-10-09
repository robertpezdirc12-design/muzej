"use client";

import { useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { CheckCircle2, Hourglass, Map, QrCode, RotateCw, Sparkles, X } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { useLang } from "./language-context";
import { exhibits as allExhibits } from "@/lib/museum";
import type { GeoFix } from "@/lib/geo";
import { distanceM, formatDistance } from "@/lib/geo";
import {
  TIME_SPOTS,
  spotDeepLink,
  spotYearParam,
  isDistantSpot,
  spotDistanceFromVillage,
  type TimeSpot,
} from "@/data/atlas/timespots";
import { useTimeMachine } from "@/lib/time-machine-store";
import { useTimespots } from "@/lib/timespots-store";
import { YEAR_STOPS, MAX_YEAR, formatStopYear } from "@/lib/timeline-stops";

const MapCanvas = dynamic(
  () => import("./museum-map-canvas").then((m) => m.MapCanvas),
  {
    ssr: false,
    loading: () => (
      <div className="h-[360px] w-full animate-pulse rounded-xl border bg-secondary/50 sm:h-[420px]" />
    ),
  },
);

const HISTORIC_YEAR = 1825;

export function MuseumMap({
  userFix,
  onOpen,
}: {
  userFix: GeoFix | null;
  onOpen: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const { openTM } = useTimeMachine();
  const { isUnlocked } = useTimespots();
  const [vintage, setVintage] = useState(false);
  const [timeTravel, setTimeTravel] = useState(false);
  const [year, setYear] = useState(MAX_YEAR);
  const [historic, setHistoric] = useState(false);
  const [activeSpot, setActiveSpot] = useState<TimeSpot | null>(null);

  const located = useMemo(
    () => allExhibits.filter((e) => e.lat && e.lng),
    [],
  );

  /* zapis obstaja v danem letu; neznane letnice = »obstaja ves čas«
     (enaka logika kot časovno potovanje) */
  const existsAt = (year: number) =>
    located.filter(
      (e) => (e.yearFrom ?? -Infinity) <= year && (e.yearTo ?? Infinity) >= year,
    );

  const visible = useMemo(() => {
    if (historic) return existsAt(HISTORIC_YEAR);
    if (!timeTravel) return located;
    return existsAt(year);
  }, [located, timeTravel, year, historic]);

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
            "Od bronaste igle pred tremi tisočletji in Griblacha leta 1468 do današnjih hiš — zapisi zbirke na karti kraja. Kliknite klinček in zapis se odpre.",
            "From a bronze pin three millennia back and Griblach in 1468 to the houses of today — collection records on the map of the place. Click a pin to open a record.",
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
              disabled={historic}
            />
            <Label
              htmlFor="pogled-zemljevid"
              className={`cursor-pointer text-sm font-medium leading-tight ${
                historic ? "opacity-50" : ""
              }`}
            >
              {t("Zgodovinski pogled", "Historical view")}
              <span className="block text-xs font-normal text-muted-foreground">
                {t("kartiraj kot leta 1825", "mapped as in 1825")}
              </span>
            </Label>
          </div>

          <div className="flex items-center gap-3">
            <Switch
              id="vas-1825"
              checked={historic}
              onCheckedChange={(v) => setHistoric(v)}
            />
            <Label
              htmlFor="vas-1825"
              className="cursor-pointer text-sm font-medium leading-tight"
            >
              {t("Vas ~1825 (interpretacija)", "Village ~1825 (interpretation)")}
              <span className="block text-xs font-normal text-muted-foreground">
                {t(
                  "jedro vasi in poti — skica, ne kataster",
                  "core and paths — a sketch, not a cadastre",
                )}
              </span>
            </Label>
          </div>

          <div className="flex items-center gap-3">
            <Switch
              id="casovno-potovanje"
              checked={timeTravel}
              disabled={historic}
              onCheckedChange={(v) => {
                setTimeTravel(v);
                /* obrambno: leto mora vedno biti eden od postankov drsnika */
                if (v)
                  setYear((y) =>
                    (YEAR_STOPS as readonly number[]).includes(y)
                      ? y
                      : MAX_YEAR,
                  );
              }}
            />
            <Label
              htmlFor="casovno-potovanje"
              className={`cursor-pointer text-sm font-medium leading-tight ${
                historic ? "opacity-50" : ""
              }`}
            >
              {t("Časovno potovanje", "Time travel")}
              <span className="block text-xs font-normal text-muted-foreground">
                {t("pokaži le zapise, obstoječe tistega leta", "show only records existing that year")}
              </span>
            </Label>
          </div>

          <div
            className={`flex min-w-56 flex-1 flex-col gap-1.5 transition-opacity ${
              timeTravel && !historic ? "opacity-100" : "pointer-events-none opacity-40"
            }`}
            aria-disabled={!timeTravel || historic}
          >
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>{formatStopYear(YEAR_STOPS[0], lang)}</span>
              <span className="font-mono text-sm font-semibold text-primary">
                {timeTravel && !historic ? formatStopYear(year, lang) : "—"}
              </span>
              <span>{MAX_YEAR}</span>
            </div>
            {/* Diskretni drsnik po postankih = vsa mejna leta zapisov na karti
                (enake množice pik kot zvezni drsnik, vključno s prazgodovino
                za piko MVG-095 — P18, dokumentirano v src/lib/timeline-stops.ts) */}
            <input
              type="range"
              min={0}
              max={YEAR_STOPS.length - 1}
              step={1}
              value={Math.max(0, (YEAR_STOPS as readonly number[]).indexOf(year))}
              onChange={(e) => setYear(YEAR_STOPS[Number(e.target.value)])}
              aria-label={t("Leto prikaza", "Year to display")}
              className="h-2 w-full cursor-pointer accent-[color-mix(in_oklch,var(--primary)_80%,black)]"
            />
          </div>

          <p className="text-xs text-muted-foreground" aria-live="polite">
            {t(
              `Na zemljevidu: ${visible.length} od ${located.length} zapisov`,
              `On the map: ${visible.length} of ${located.length} records`,
            )}
            {userFix && t(` · vi ste na karti`, ` · you are on the map`)}
          </p>

          {/* 3D časovni stroj (issue #10) — celotna vas na podlatnah katastra */}
          <button
            type="button"
            onClick={() => openTM(1825)}
            className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
          >
            <Hourglass className="size-4" aria-hidden="true" />
            {t("3D časovni stroj — 1825/1900/danes", "3D time machine — 1825/1900/today")}
          </button>
        </div>

        <div className="mt-4">
          <MapCanvas
            exhibits={visible}
            vintage={vintage || historic}
            historic={historic}
            userFix={userFix}
            onOpen={onOpen}
            onSpot={(s) => setActiveSpot(s)}
          />
        </div>

        {/* ── AR TIME SPOT: kartica točke (klik na 🕰 na zemljevidu) ── */}
        {activeSpot && (
          <div
            className="mt-4 rounded-xl border bg-card p-4 shadow-sm sm:p-5"
            role="region"
            aria-label={t("Kartica časovne točke", "Time spot card")}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="flex flex-wrap items-center gap-2">
                  <span className="inline-flex items-center rounded-full bg-primary px-2.5 py-1 text-xs font-bold text-primary-foreground">
                    🕰 {spotYearParam(activeSpot.year)}
                  </span>
                  <span className="font-display text-base font-semibold leading-snug">
                    {lang === "si" ? activeSpot.titleSi : activeSpot.titleEn}
                  </span>
                  {isUnlocked(activeSpot.id) && (
                    <span className="inline-flex items-center gap-1 rounded-full border border-emerald-600/30 bg-emerald-600/10 px-2 py-0.5 text-[11px] font-medium text-emerald-700 dark:text-emerald-300">
                      <CheckCircle2 className="size-3" aria-hidden="true" />
                      {t("odklenjeno", "unlocked")}
                    </span>
                  )}
                  {isDistantSpot(activeSpot) && (
                    <span className="inline-flex items-center gap-1 rounded-full border border-primary/40 bg-primary/10 px-2 py-0.5 text-[11px] font-semibold text-primary">
                      {t(
                        `oddaljena točka · ${formatDistance(spotDistanceFromVillage(activeSpot), lang)} od vasi — lastna mini vsebina`,
                        `distant spot · ${formatDistance(spotDistanceFromVillage(activeSpot), lang)} from the village — own mini content`,
                      )}
                    </span>
                  )}
                </p>
                <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
                  {lang === "si" ? activeSpot.descSi : activeSpot.descEn}
                </p>
                {userFix && (
                  <p className="mt-1.5 text-xs text-muted-foreground">
                    {t(
                      `od vas ≈ ${formatDistance(distanceM(userFix, { lat: activeSpot.lat, lng: activeSpot.lng }), lang)}`,
                      `from you ≈ ${formatDistance(distanceM(userFix, { lat: activeSpot.lat, lng: activeSpot.lng }), lang)}`,
                    )}
                  </p>
                )}
              </div>
              <button
                type="button"
                onClick={() => setActiveSpot(null)}
                aria-label={t("Zapri kartico točke", "Close the spot card")}
                className="shrink-0 rounded-full border p-1.5 text-muted-foreground transition-colors hover:bg-secondary"
              >
                <X className="size-4" aria-hidden="true" />
              </button>
            </div>

            <div className="mt-3 flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={() => {
                  openTM(activeSpot.year, activeSpot.id);
                  setActiveSpot(null);
                }}
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
              >
                <Hourglass className="size-4" aria-hidden="true" />
                {t(
                  `POGLEJ V AR — ${spotYearParam(activeSpot.year)}`,
                  `VIEW IN AR — ${spotYearParam(activeSpot.year)}`,
                )}
              </button>
              {/* DOŽIVI 360° (issue #13): hero TimeSpot ima Historical
                  Panorama — imerzivni zgodovinski pogled (magic window) */}
              {activeSpot.panoramaId && (
                <button
                  type="button"
                  onClick={() => {
                    openTM(activeSpot.year, activeSpot.id, false, true);
                    setActiveSpot(null);
                  }}
                  className="inline-flex items-center gap-2 rounded-lg border border-primary/40 bg-primary/10 px-4 py-2.5 text-sm font-semibold text-primary transition-colors hover:bg-primary/20"
                >
                  <Sparkles className="size-4" aria-hidden="true" />
                  {t("DOŽIVI 360°", "EXPERIENCE 360°")}
                </button>
              )}
              {/* 360° s cerkve (issue #12): virtualni pogled za doma/iOS brez GPS */}
              {activeSpot.id === "cerkev" && (
                <button
                  type="button"
                  onClick={() => {
                    openTM(1825, "cerkev", true);
                    setActiveSpot(null);
                  }}
                  className="inline-flex items-center gap-2 rounded-lg border border-primary/40 px-4 py-2.5 text-sm font-semibold text-primary transition-colors hover:bg-primary/10"
                >
                  <RotateCw className="size-4" aria-hidden="true" />
                  {t("360° S CERKVE", "360° FROM THE CHURCH")}
                </button>
              )}
              <button
                type="button"
                onClick={() => {
                  onOpen(activeSpot.exhibitSlug);
                  setActiveSpot(null);
                }}
                className="inline-flex items-center gap-2 rounded-lg border px-4 py-2.5 text-sm font-semibold transition-colors hover:bg-secondary"
              >
                {t("Zapis zbirke", "Collection record")}
              </button>
              {/* QR natisnjene tablice — ista koda kot na lokaciji */}
              <img
                src={`/qr/spot-${activeSpot.id}.png`}
                alt={t(`QR koda točke ${activeSpot.titleSi}`, `QR code of the ${activeSpot.titleEn} spot`)}
                width={64}
                height={64}
                loading="lazy"
                className="h-16 w-16 rounded-md border bg-[#F7F3EB]"
              />
              <span className="min-w-0 flex-1 truncate font-mono text-[11px] text-muted-foreground">
                {spotDeepLink(activeSpot)}
              </span>
            </div>

            <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
              {t("Vir: ", "Source: ")}
              {lang === "si" ? activeSpot.evidenceSi : activeSpot.evidenceEn}
            </p>
          </div>
        )}

        {/* ── QR tablice za fizični muzej (natisni) ── */}
        <details className="group mt-4 rounded-xl border bg-card">
          <summary className="flex cursor-pointer list-none items-center gap-2 p-4 text-sm font-semibold">
            <QrCode className="size-4 text-primary" aria-hidden="true" />
            {t(
              "Časovne točke po vasi — QR tablice (natisni za fizični muzej)",
              "Time spots around the village — QR plates (print for the physical museum)",
            )}
          </summary>
          <div className="grid gap-4 border-t p-4 sm:grid-cols-2 lg:grid-cols-3">
            {/* vstopni QR (issue #15) — prvi zaslon obiskovalca iz fizičnega vhoda */}
            <div className="flex items-center gap-3 rounded-lg border border-primary/40 bg-primary/5 p-3">
              <img
                src="/qr/vstop.png"
                alt={t("Vstopna QR koda muzeja", "The museum's entrance QR code")}
                width={88}
                height={88}
                loading="lazy"
                className="h-[88px] w-[88px] shrink-0 rounded-md border bg-[#F7F3EB]"
              />
              <div className="min-w-0">
                <p className="text-sm font-semibold leading-tight">
                  {t("VSTOP — dobrodošlica obiskovalca", "ENTRANCE — visitor welcome")}
                </p>
                <p className="mt-1 break-all font-mono text-[10px] leading-tight text-muted-foreground">
                  https://griblje-museum.vercel.app/?obisk=1
                </p>
              </div>
            </div>
            {TIME_SPOTS.map((s) => (
              <div key={s.id} className="flex items-center gap-3 rounded-lg border p-3">
                <img
                  src={`/qr/spot-${s.id}.png`}
                  alt={t(`QR koda točke ${s.titleSi}`, `QR code of the ${s.titleEn} spot`)}
                  width={88}
                  height={88}
                  loading="lazy"
                  className="h-[88px] w-[88px] shrink-0 rounded-md border bg-[#F7F3EB]"
                />
                <div className="min-w-0">
                  <p className="text-sm font-semibold leading-tight">
                    🕰 {spotYearParam(s.year)} · {lang === "si" ? s.titleSi : s.titleEn}
                  </p>
                  <p className="mt-1 break-all font-mono text-[10px] leading-tight text-muted-foreground">
                    {spotDeepLink(s)}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <p className="px-4 pb-4 text-xs leading-relaxed text-muted-foreground">
            {t(
              "Vsaka koda odpre časovni stroj na točki in letnici — skeniraj na lokaciji (Nîmes vzorec: brez namestitve, brez računa) ali natisni A6 tabelo za fizični muzej.",
              "Each code opens the time machine at the spot and year — scan on site (Nîmes pattern: no install, no account) or print an A6 plate for the physical museum.",
            )}
          </p>
        </details>

        {historic ? (
          <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
            {t(
              "Poligon jedra vasi in črtkane poti so INTERPRETACIJA — izvirni terezijanski kataster ~1825 se ni ohranil, geometrija je skica, podprta z zapisi (MVG-001, MVG-049, MVG-028, MVG-040, MVG-009). Klinčki so zapisi, znani za leto 1825.",
              "The village-core polygon and dashed paths are INTERPRETATION — the original Theresian cadastre of ~1825 has not survived; the geometry is a sketch supported by records (MVG-001, MVG-049, MVG-028, MVG-040, MVG-009). Pins mark records known to exist in 1825.",
            )}
          </p>
        ) : timeTravel ? (
          <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
            {t(
              "Leto je vodilo po letnicah zapisov (»od – do«); zapisi brez znane letnice ostanejo na karti.",
              "The year follows record dates (“from – to”); records without a known year stay on the map.",
            )}
          </p>
        ) : null}
      </div>
    </section>
  );
}
