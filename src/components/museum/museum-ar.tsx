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
import { VECTOR_BUILDINGS, ATLAS_LOCATIONS } from "@/data/atlas/model";
import { LANDUSE_ZONES } from "@/data/atlas/landuse";
import { HOUSE_VITALS } from "@/data/atlas/parish";
import type { UseGeolocation } from "@/hooks/use-geolocation";
import {
  bearingDeg,
  compassLabelSi,
  distanceM,
  formatDistance,
  type GeoFix,
} from "@/lib/geo";
import { Clock, Landmark, Trees, Wheat, Hourglass } from "lucide-react";
import { useTimeMachine } from "@/lib/time-machine-store";

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

        {/* ── časovna plast 1825 (issue #9) ── */}
        <TimeLayer1825 fix={fix} />

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

/* ——— ČASOVNA PLAST 1825 (issue #9): kje stojite na katastru ~1825 ——— */

function pointInZone(lat: number, lng: number, z: { bounds: [[number, number], [number, number]] }) {
  const [[n, w], [s, e]] = z.bounds;
  return lat <= n && lat >= s && lng >= w && lng <= e;
}

function TimeLayer1825({ fix }: { fix: GeoFix | null }) {
  const { t, lang } = useLang();
  const { openTM } = useTimeMachine();

  /* stojite v coni rabe tal? + najbližje 1825 stavbe (vektorizacija A02) */
  const info = useMemo(() => {
    if (!fix) return null;
    const zone = LANDUSE_ZONES.find((z) => pointInZone(fix.lat, fix.lng, z));
    const nearestBuildings = VECTOR_BUILDINGS.map((b) => ({
      b,
      d: distanceM(fix, { lat: b.lat, lng: b.lng }),
    }))
      .sort((a, c) => a.d - c.d)
      .slice(0, 3);
    const church = ATLAS_LOCATIONS.find((l) => l.id === "loc-cerkev");
    const village = ATLAS_LOCATIONS.find((l) => l.id === "loc-griblje");
    return {
      zone,
      nearestBuildings,
      church: church && church.lat && church.lng ? { d: distanceM(fix, { lat: church.lat, lng: church.lng }) } : null,
      village: village && village.lat && village.lng ? { d: distanceM(fix, { lat: village.lat, lng: village.lng }) } : null,
    };
  }, [fix]);

  const zoneIcon = (kind: string) =>
    kind === "meadow" ? <Trees className="size-4" aria-hidden /> :
    kind === "forest" ? <Trees className="size-4" aria-hidden /> :
    <Wheat className="size-4" aria-hidden />;

  return (
    <div className="mt-6 rounded-xl border border-primary/30 bg-card p-4 sm:p-6">
      <h3 className="flex flex-wrap items-center gap-2 font-display text-lg font-semibold">
        <Clock className="size-5 text-primary" aria-hidden="true" />
        {t("Časovna plast 1825 — kaj je tu stalo pred 200 leti", "Time layer 1825 — what stood here 200 years ago")}
        <button
          type="button"
          onClick={() => openTM(1825)}
          className="ml-auto inline-flex items-center gap-1.5 rounded-lg bg-primary px-3 py-1.5 text-xs font-semibold text-primary-foreground transition hover:bg-primary/90"
        >
          <Hourglass className="size-3.5" aria-hidden="true" />
          {t("Stopi v 3D vas 1825 (AR)", "Step into the 3D village of 1825 (AR)")}
        </button>
      </h3>

      {!fix ? (
        <p className="mt-2 text-sm text-muted-foreground">
          {t(
            "Priklopite GPS in časovna plast pokaže, na kateri rabi tal katastra ~1825 stojite, ter najbližje tedanje stavbe (vektorizacija lista A02), hišne zgodbe in povezavo do Atlasa.",
            "Connect GPS and the time layer will show which ~1825 cadastral land use you are standing on, the nearest buildings of that era (vectorised from sheet A02), house stories and a link to the Atlas.",
          )}
        </p>
      ) : (
        <div className="mt-3 space-y-3">
          {/* raba tal pod nogami */}
          <div className="rounded-lg border bg-secondary/40 p-3">
            <div className="flex items-center gap-2 text-sm font-medium">
              <Landmark className="size-4 text-primary" aria-hidden />
              {info?.zone ? (
                <>
                  {zoneIcon(info.zone.kind)}
                  {t("Stojite na:", "You are standing on:")}
                  <span className="font-semibold">{lang === "si" ? info.zone.labelSi : info.zone.labelEn}</span>
                  <span className="rounded bg-rose-100 px-1.5 py-0.5 text-[10px] font-semibold text-rose-900 dark:bg-rose-900/60 dark:text-rose-100">
                    RECONSTRUCTED
                  </span>
                </>
              ) : (
                <>{t("Stojite izven vrisanih con rabe tal ~1825 (katastrska občina Griblje).", "You are standing outside the drawn ~1825 land-use zones (cadastral municipality of Griblje).")}</>
              )}
            </div>
            {info?.zone && (
              <p className="mt-1 text-xs text-muted-foreground">
                {lang === "si" ? info.zone.noteSi : info.zone.noteEn}{" "}
                <a
                  href={`/?atlas=${info.zone.id}&odsek=atlas`}
                  className="font-medium text-primary underline decoration-border underline-offset-2 hover:decoration-primary"
                >
                  {t("Odpri v Atlasu", "Open in the Atlas")}
                </a>
              </p>
            )}
            {info?.church && info?.village && (
              <p className="mt-1 text-xs text-muted-foreground">
                {t(
                  `Do cerkve sv. Vida ~1825 (VERIFIED): ${formatDistance(info.church.d, lang)} · do jedra vasi Grüble: ${formatDistance(info.village.d, lang)}.`,
                  `To St. Vitus' church ~1825 (VERIFIED): ${formatDistance(info.church.d, lang)} · to the core of Grüble village: ${formatDistance(info.village.d, lang)}.`,
                )}
              </p>
            )}
          </div>

          {/* najbližje stavbe 1825 */}
          <div className="grid gap-2 sm:grid-cols-3">
            {info?.nearestBuildings.map(({ b, d }, i) => (
              <div key={i} className="rounded-lg border bg-background/60 p-3 text-xs">
                <div className="font-medium">
                  {t(`Stavba ~1825 · ${i + 1}. najbližja`, `Building ~1825 · ${i + 1}. nearest`)}
                </div>
                <div className="mt-1 text-muted-foreground">
                  {t("vektorizacija A02", "vectorised from A02")} · {formatDistance(d, lang)}
                </div>
              </div>
            ))}
          </div>

          {/* hišne zgodbe (matrike) */}
          <div className="rounded-lg border bg-background/60 p-3 text-xs">
            <span className="font-medium">{t("Hišne zgodbe (matrike × register 1825):", "House stories (parish registers × 1825 register):")}</span>{" "}
            {t(
              `${HOUSE_VITALS.length} vpisa za hišo 61 (1887 Katarina, 1897 Anton) — več v zavihku Matrike Atlasa. Lastniki vseh 80 hiš: zavihek Register hiš.`,
              `${HOUSE_VITALS.length} entries for house no. 61 (1887 Katarina, 1897 Anton) — more in the Atlas »Parish registers« tab. Owners of all 80 houses: the »House register« tab.`,
            )}{" "}
            <a
              href="/?odsek=atlas"
              className="font-medium text-primary underline decoration-border underline-offset-2 hover:decoration-primary"
            >
              {t("Odpri Atlas", "Open the Atlas")}
            </a>
          </div>

          <p className="text-[11px] leading-relaxed text-muted-foreground">
            {t(
              "Vsak podatek ima vir: lastniki (N083PT, REVIEW), raba tal (VLM analiza listov, RECONSTRUCTED ±100–150 m), matrike (Matricula Online, župnija Podzemelj). Kjer podatka ni, je to izrecno — nič ni izmišljeno.",
              "Every datum has a source: owners (N083PT, REVIEW), land use (VLM sheet analysis, RECONSTRUCTED ±100–150 m), parish registers (Matricula Online, Podzemelj parish). Where a datum is missing, this is stated — nothing is invented.",
            )}
          </p>
        </div>
      )}
    </div>
  );
}
