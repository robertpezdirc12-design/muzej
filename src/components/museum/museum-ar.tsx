"use client";

/**
 * AR vodnik po vasi — GPS, bližina točk, kamera AR in vodeni sprehod.
 *
 * Odsek je vozlišče treh zmožnosti (issue #1):
 *  1. GPS: priklop, natančnost, uporabnik na zemljevidu (glej MuseumMap),
 *     razvrščena bližina točk, navigacija (OSM peš);
 *  2. kamera AR: zapisi z 3D-modelom IN lokacijo se prikažejo SAMODEJNO
 *     (pipeline: nov zapis z model3dUrl + lat/lng pride sem brez posredovanja);
 *  3. vodeni sprehod: obstoječe muzejske poti (extra.json → walk).
 */

import { useMemo, useState } from "react";
import dynamic from "next/dynamic";
import {
  Camera,
  Crosshair,
  LocateFixed,
  MapPin,
  Navigation,
  Radar,
  Satellite,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLang } from "./language-context";
import { exhibits } from "@/lib/museum";
import { GuidedWalk } from "./guided-walk";
import type { UseGeolocation } from "@/hooks/use-geolocation";
import {
  bearingDeg,
  compassLabelSi,
  distanceM,
  formatDistance,
  type GeoFix,
} from "@/lib/geo";

const ARCameraView = dynamic(
  () => import("./ar-camera").then((m) => m.ARCameraView),
  { ssr: false },
);

/** Pipeline AR: zapis z 3D-modelom in znano lokacijo (dokumentirano). */
const AR_READY = exhibits.filter((e) => e.model3dUrl && e.lat && e.lng);

/** Zemljevidne točke za bližino. */
const LOCATED = exhibits.filter((e) => e.lat && e.lng);

export function MuseumARGuide({
  geo,
  onOpen,
}: {
  geo: UseGeolocation;
  onOpen: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const [arSlug, setArSlug] = useState<string | null>(null);
  const { fix, status, error, start, stop } = geo;

  /* bližnje točke, razvrščene po oddaljenosti od uporabnika */
  const nearby = useMemo(() => {
    if (!fix) return [];
    return LOCATED.map((e) => ({
      exhibit: e,
      distance: distanceM(fix, { lat: e.lat!, lng: e.lng! }),
      bearing: bearingDeg(fix, { lat: e.lat!, lng: e.lng! }),
    }))
      .sort((a, b) => a.distance - b.distance)
      .slice(0, 6);
  }, [fix]);

  const arExhibit = arSlug
    ? AR_READY.find((e) => e.slug === arSlug) ?? null
    : null;

  const statusText = () => {
    switch (status) {
      case "watching":
        return fix
          ? t(
              `GPS aktiven · natančnost ± ${Math.round(fix.accuracy ?? 0)} m`,
              `GPS active · accuracy ± ${Math.round(fix.accuracy ?? 0)} m`,
            )
          : t("GPS aktiven — čakam na prvo opravilo …", "GPS active — waiting for the first fix …");
      case "denied":
        return t(
          "Dovoljenje za lokacijo je zavrnjeno — omogočite ga v nastavitvah brskalnika.",
          "Location permission denied — enable it in the browser settings.",
        );
      case "unsupported":
        return t(
          "Ta brskalnik ne ponuja geolokacije.",
          "This browser does not offer geolocation.",
        );
      case "error":
        return t(
          `Lokacije ne morem izslediti${error ? `: ${error}` : "."}`,
          `Cannot obtain the location${error ? `: ${error}` : "."}`,
        );
      default:
        return t(
          "Priklopite GPS in vas bom postavil na karto vasi.",
          "Connect GPS and I will place you on the village map.",
        );
    }
  };

  return (
    <section
      id="vodic"
      className="scroll-mt-20 border-t border-border/60"
      aria-labelledby="vodic-naslov"
    >
      <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <h2
          id="vodic-naslov"
          className="flex items-center gap-3 font-display text-3xl font-semibold tracking-tight"
        >
          <Camera className="size-7 text-primary" aria-hidden="true" />
          {t("AR vodnik po vasi", "AR guide through the village")}
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
          {t(
            "Kamera, GPS in telefonski zaslon za vodnika: stojite pred cerkvijo sv. Vida in njena zgodovina se odpre v objektivu. Vsak zapis z lokacijo in 3D-modelom se v AR vodniku prikaže samodejno — brez ročnega prenašanja podatkov.",
            "Camera, GPS and your phone screen as a guide: stand in front of the church of St. Vitus and its history opens in your lens. Every record with a location and a 3D model appears in the AR guide automatically — no manual data copying.",
          )}
        </p>

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          {/* ── GPS kartica ── */}
          <div className="rounded-xl border bg-card p-4 sm:p-6">
            <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
              <Satellite className="size-5 text-primary" aria-hidden="true" />
              {t("GPS na telefonu", "GPS on your phone")}
            </h3>
            <p
              className={`mt-1 text-xs leading-relaxed ${
                status === "watching" ? "text-primary" : "text-muted-foreground"
              }`}
              aria-live="polite"
            >
              {statusText()}
            </p>

            {fix && (
              <dl className="mt-3 grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
                <div className="rounded-lg bg-secondary/50 p-2">
                  <dt className="text-muted-foreground">{t("širina", "lat")}</dt>
                  <dd className="font-mono">{fix.lat.toFixed(5)}</dd>
                </div>
                <div className="rounded-lg bg-secondary/50 p-2">
                  <dt className="text-muted-foreground">{t("dolžina", "lng")}</dt>
                  <dd className="font-mono">{fix.lng.toFixed(5)}</dd>
                </div>
                <div className="rounded-lg bg-secondary/50 p-2">
                  <dt className="text-muted-foreground">{t("natančnost", "accuracy")}</dt>
                  <dd className="font-mono">
                    ± {Math.round(fix.accuracy ?? 0)} m
                  </dd>
                </div>
                <div className="rounded-lg bg-secondary/50 p-2">
                  <dt className="text-muted-foreground">{t("smer", "heading")}</dt>
                  <dd className="font-mono">
                    {fix.heading != null
                      ? `${Math.round(fix.heading)}°`
                      : "—"}
                  </dd>
                </div>
              </dl>
            )}

            <div className="mt-4 flex flex-wrap gap-2">
              {status === "watching" ? (
                <Button type="button" variant="outline" size="sm" onClick={stop}>
                  <LocateFixed className="mr-1.5 size-4" aria-hidden="true" />
                  {t("Izklopi GPS", "Disconnect GPS")}
                </Button>
              ) : (
                <Button type="button" size="sm" onClick={start}>
                  <Crosshair className="mr-1.5 size-4" aria-hidden="true" />
                  {t("Priklopi GPS", "Connect GPS")}
                </Button>
              )}
              <a
                href="#zemljevid"
                className="inline-flex h-8 items-center gap-1.5 rounded-md border border-border px-3 text-xs font-medium text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
              >
                <MapPin className="size-3.5" aria-hidden="true" />
                {t("Pokaži me na zemljevidu", "Show me on the map")}
              </a>
            </div>
            <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
              {t(
                "Lokacija ostaja v vašem brskalniku — ne pošiljamo je nikamor.",
                "Your location stays in your browser — we never send it anywhere.",
              )}
            </p>
          </div>

          {/* ── AR objekti (pipeline) ── */}
          <div className="rounded-xl border bg-card p-4 sm:p-6">
            <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
              <Radar className="size-5 text-primary" aria-hidden="true" />
              {t("Objekti v AR", "Objects in AR")}
              <span className="ml-auto rounded-full border border-primary/30 bg-primary/10 px-2 py-0.5 font-mono text-[11px] text-primary">
                {AR_READY.length}
              </span>
            </h3>
            <ul className="mt-3 space-y-2">
              {AR_READY.map((e) => {
                const d = fix && e.lat ? distanceM(fix, { lat: e.lat!, lng: e.lng! }) : null;
                return (
                  <li
                    key={e.slug}
                    className="flex items-center gap-3 rounded-lg border bg-secondary/40 p-3"
                  >
                    <span className="flex size-10 shrink-0 items-center justify-center rounded-lg border border-primary/30 bg-primary/10 font-mono text-[10px] font-semibold text-primary">
                      {e.museumNo.replace("MVG-", "")}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block truncate text-sm font-medium">
                        {lang === "si" ? e.titleSi : e.titleEn}
                      </span>
                      <span className="block text-xs text-muted-foreground">
                        {t("3D-model · dokumentirana lokacija", "3D model · documented location")}
                        {d != null && ` · ${formatDistance(d, lang)}`}
                      </span>
                    </span>
                    <Button type="button" size="sm" onClick={() => setArSlug(e.slug)} className="shrink-0 gap-1.5">
                      <Camera className="size-3.5" aria-hidden="true" />
                      {t("Odpri AR", "Open AR")}
                    </Button>
                  </li>
                );
              })}
              {AR_READY.length === 0 && (
                <li className="rounded-lg border border-dashed p-3 text-xs text-muted-foreground">
                  {t(
                    "Zaenkrat še ni zapisa s 3D-modelom in lokacijo.",
                    "No record with a 3D model and a location yet.",
                  )}
                </li>
              )}
            </ul>
            <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
              {t(
                "Pravila pipeline-a: zapisu dodajte lokacijo (lat/lng) in 3D-model (model3dUrl) in se bo sam pojavil tukaj, na zemljevidu in v sprehodih — brez dvojnega vnašanja.",
                "Pipeline rule: give a record a location (lat/lng) and a 3D model (model3dUrl) and it will appear here, on the map and in the walks by itself — no double entry.",
              )}
            </p>
          </div>
        </div>

        {/* ── bližnje točke ── */}
        {nearby.length > 0 && (
          <div className="mt-6 rounded-xl border bg-card p-4 sm:p-6">
            <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
              <Navigation className="size-5 text-primary" aria-hidden="true" />
              {t("Najbližje točke zbirke", "Nearest collection points")}
            </h3>
            <ul className="mt-3 grid gap-2 sm:grid-cols-2">
              {nearby.map(({ exhibit: e, distance, bearing }) => (
                <li
                  key={e.slug}
                  className="flex items-center gap-3 rounded-lg border bg-secondary/40 p-3"
                >
                  <span className="flex size-10 shrink-0 items-center justify-center rounded-lg border bg-background font-mono text-[10px] font-semibold text-primary">
                    {e.museumNo.replace("MVG-", "")}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-sm font-medium">
                      {lang === "si" ? e.titleSi : e.titleEn}
                    </span>
                    <span className="block text-xs text-muted-foreground">
                      {formatDistance(distance, lang)} ·{" "}
                      {t(compassLabelSi(bearing), compassLabelSi(bearing))}
                      {" · "}
                      <button
                        type="button"
                        onClick={() => onOpen(e.slug)}
                        className="font-medium text-primary underline decoration-border underline-offset-2 hover:decoration-primary"
                      >
                        {t("zapis", "record")}
                      </button>
                    </span>
                  </span>
                  <a
                    href={`https://www.openstreetmap.org/directions?engine=fossgis_osrm_foot&route=${fix!.lat},${fix!.lng};${e.lat},${e.lng}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={t(`Navigiraj do ${e.titleSi}`, `Navigate to ${e.titleEn}`)}
                    className="flex size-9 shrink-0 items-center justify-center rounded-md border border-border text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
                  >
                    <Navigation className="size-4" aria-hidden="true" />
                  </a>
                </li>
              ))}
            </ul>
            <p className="mt-2 text-[11px] text-muted-foreground" aria-live="polite">
              {t(
                `Razvrščeno po oddaljenosti od vas · skupaj ${LOCATED.length} točk z lokacijo`,
                `Sorted by distance from you · ${LOCATED.length} located points in total`,
              )}
            </p>
          </div>
        )}

        {/* ── vodeni sprehod ── */}
        <div className="mt-6">
          <GuidedWalk fix={fix} onOpen={onOpen} onStartAr={setArSlug} />
        </div>
      </div>

      {/* ── AR kamera (fullscreen, dinamično) ── */}
      {arExhibit && (
        <ARCameraView
          exhibit={arExhibit}
          fix={fix}
          geoActive={status === "watching"}
          onStartGps={start}
          onClose={() => setArSlug(null)}
          onOpenExhibit={(slug) => {
            setArSlug(null);
            onOpen(slug);
          }}
        />
      )}
    </section>
  );
}
