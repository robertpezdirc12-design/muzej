"use client";

/**
 * 3D VAS 1825 — orbit pregledovalnik za ATLAS (issue #10).
 *
 * Isti prizor kot AR časovni stroj, brez kamere: prosto vrtenje in zoom,
 * preklop letnic, legenda in gumb v AR. Namizje in telefon.
 */

import { useEffect, useRef, useState } from "react";
import { Camera, Info, Layers, RotateCcw, X, Home, MapPin } from "lucide-react";
import { useLang } from "./language-context";
import { useTimeMachine, type TimeYear } from "@/lib/time-machine-store";
import {
  PERIODS,
  PRESENCE_LEGEND,
  IZGINILO_STATS,
  TREE_STATS,
  HOUSENO_FINDING,
  CHURCH,
  inVillageCore,
  BUILDING_NEAREST_PRESENT,
  type BuildingPresence,
} from "@/lib/village3d";
import type { PickResult } from "./village-scene";

interface OrbitCard {
  kind: PickResult["kind"];
  w: number;
  d: number;
  dist: number;
  presence?: BuildingPresence;
  core: boolean;
  nearChurch: boolean;
  nearestPresent?: number | null;
}

export function VillageViewer() {
  const { t, lang } = useLang();
  const { year, setYear, openTM } = useTimeMachine();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const sceneRef = useRef<import("./village-scene").VillageScene | null>(null);
  const yearRef = useRef(year);
  const [ready, setReady] = useState(false);
  const [failed, setFailed] = useState(false);
  const [card, setCard] = useState<OrbitCard | null>(null);

  const period = PERIODS.find((p) => p.year === year) ?? PERIODS[0];

  useEffect(() => {
    let cancelled = false;
    let scene: import("./village-scene").VillageScene | null = null;
    import("./village-scene")
      .then(({ VillageScene }) => {
        if (cancelled || !canvasRef.current) return;
        scene = new VillageScene(canvasRef.current, {
          mode: "orbit",
          onPick: (p: PickResult | null) => {
            if (!p) return;
            setCard({
              kind: p.kind,
              w: Math.round(p.w),
              d: Math.round(p.d),
              dist: p.dist,
              presence: p.presence,
              core: inVillageCore(p.x, p.z),
              nearChurch: Math.hypot(p.x - CHURCH.x, p.z - CHURCH.z) < 80,
              nearestPresent:
                p.kind === "1825" && p.index != null
                  ? BUILDING_NEAREST_PRESENT[p.index]
                  : undefined,
            });
          },
        });
        scene.setYear(yearRef.current);
        sceneRef.current = scene;
        setReady(true);
      })
      .catch(() => setFailed(true));
    return () => {
      cancelled = true;
      scene?.dispose();
      sceneRef.current = null;
    };
  }, []);

  /* preklop letnice (skupna trgovina — lahko pride tudi iz AR overlaya) */
  useEffect(() => {
    yearRef.current = year;
    sceneRef.current?.setYear(year);
    setCard(null);
  }, [year]);

  const yearButtons: [TimeYear, string, string][] = [
    [1825, "1825", "1825"],
    [1900, "~1900", "~1900"],
    [2026, "danes", "today"],
  ];

  return (
    <div className="grid gap-4 lg:grid-cols-[1fr_280px]">
      {/* platno */}
      <div className="relative overflow-hidden rounded-xl border bg-[radial-gradient(ellipse_at_top,#e9e0cd_0%,#cfc3a8_58%,#b3a787_100%)] dark:from-[#1d261e] dark:via-[#141a13] dark:to-[#0f1610]">
        <canvas
          ref={canvasRef}
          role="img"
          aria-label={t(
            "3D rekonstrukcija vasi Griblje ~1825 — zavrtite za ogled",
            "3D reconstruction of Griblje village ~1825 — rotate to explore",
          )}
          className="block h-[420px] w-full touch-none sm:h-[520px]"
        />
        {!ready && !failed && (
          <p className="absolute inset-x-0 bottom-3 text-center text-xs text-muted-foreground">
            {t("gradim vas — 156 podlatn, drevesa, Kolpa …", "building the village — 156 footprints, trees, the Kolpa …")}
          </p>
        )}
        {failed && (
          <p className="absolute inset-0 flex items-center justify-center p-6 text-center text-sm text-muted-foreground">
            {t(
              "Vaš brskalnik ne podpira WebGL — 3D rekonstrukcija ni mogoča.",
              "Your browser does not support WebGL — the 3D reconstruction is unavailable.",
            )}
          </p>
        )}
        <div className="absolute left-3 top-3 flex items-center gap-1.5 rounded-full border border-border/60 bg-background/80 px-3 py-1 text-[11px] font-medium backdrop-blur">
          <Layers className="size-3.5 text-primary" aria-hidden="true" />
          {t(
            " zavrtite · približajte kolescem/ščeck · tapnite hišo",
            " rotate · zoom with wheel/pinch · tap a house",
          )}
        </div>

        {/* P12: kartica izbrane stavbe (tap) — enaka vsebina kot v AR */}
        {card && (
          <div className="absolute inset-x-3 bottom-3 z-20 sm:left-auto sm:right-3 sm:w-[340px]">
            <div className="max-h-[40vh] overflow-y-auto rounded-xl border border-border bg-background/95 p-4 shadow-lg backdrop-blur">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="font-display text-sm font-semibold">
                    {card.kind === "present"
                      ? t("Današnja stavba — OSM", "Present-day building — OSM")
                      : card.kind === "growth"
                        ? t("Stavba ~1900 (ocena)", "Building ~1900 (estimate)")
                        : year === 2026
                          ? t("Stavba 1825 — duh", "Building of 1825 — ghost")
                          : t("Stavba ~1825 — kataster", "Building ~1825 — cadastre")}
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {t(
                      `tloris ≈ ${card.w} × ${card.d} m · ${Math.round(card.dist)} m od pogleda`,
                      `footprint ≈ ${card.w} × ${card.d} m · ${Math.round(card.dist)} m from view`,
                    )}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setCard(null)}
                  aria-label={t("Zapri kartico stavbe", "Close building card")}
                  className="shrink-0 rounded-full border border-border p-1.5 hover:bg-accent"
                >
                  <X className="size-4" aria-hidden="true" />
                </button>
              </div>
              <div className="mt-2 space-y-1.5 text-[11px] leading-relaxed text-muted-foreground">
                {card.kind === "1825" && year === 2026 && card.presence && (
                  <p className="font-medium">
                    {PRESENCE_LEGEND.find((l) => l.status === card.presence)?.dotSi}{" "}
                    {lang === "si"
                      ? PRESENCE_LEGEND.find((l) => l.status === card.presence)?.labelSi
                      : PRESENCE_LEGEND.find((l) => l.status === card.presence)?.labelEn}
                    {card.nearestPresent != null &&
                      ` · ${t("najbližja danes", "nearest today")}: ${Math.round(card.nearestPresent)} m`}
                  </p>
                )}
                {card.core && (
                  <p>{t("V jedru vasi 1825 (Grüble).", "In the 1825 village core (Grüble).")}</p>
                )}
                {card.nearChurch && (
                  <p>{t("Ob cerkvi sv. Vida — njen 3D model je v prizoru.", "By St. Vitus' church — its 3D model is in the scene.")}</p>
                )}
                {card.kind !== "present" && (
                  <p className="flex items-start gap-1.5">
                    <Home className="mt-0.5 size-3 shrink-0 text-primary" aria-hidden="true" />
                    <span>{lang === "si" ? HOUSENO_FINDING.si : HOUSENO_FINDING.en}</span>
                  </p>
                )}
                <a
                  href={`/?odsek=atlas`}
                  className="inline-flex items-center gap-1 pt-1 font-medium text-primary underline decoration-border underline-offset-2 hover:decoration-primary"
                >
                  <MapPin className="size-3" aria-hidden="true" />
                  {t("Atlas 1825 — viri in dokazi", "Atlas 1825 — sources and evidence")}
                </a>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* plošča */}
      <div className="space-y-4">
        <div>
          <h4 className="font-display text-base font-semibold">
            {t("Rekonstrukcija skozi čas", "Reconstruction through time")}
          </h4>
          <div
            role="radiogroup"
            aria-label={t("Letnica rekonstrukcije", "Reconstruction year")}
            className="mt-2 grid gap-1"
          >
            {yearButtons.map(([y, si, en]) => (
              <button
                key={y}
                type="button"
                role="radio"
                aria-checked={year === y}
                onClick={() => setYear(y)}
                className={`flex items-center justify-between rounded-lg border px-4 py-2.5 text-sm font-semibold transition ${
                  year === y
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-border hover:border-primary/40 hover:bg-accent"
                }`}
              >
                {t(si, en)}
                <span className="text-xs font-normal opacity-75">
                  {PERIODS.find((p) => p.year === y)?.buildingCount}{" "}
                  {t("stavb", "buildings")}
                </span>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-lg border bg-secondary/40 p-3 text-xs leading-relaxed text-muted-foreground">
          <p className="flex items-start gap-1.5">
            <Info className="mt-0.5 size-3.5 shrink-0 text-primary" aria-hidden="true" />
            {lang === "si" ? period.noteSi : period.noteEn}
          </p>
        </div>

        <div className="space-y-1.5 rounded-lg border p-3 text-xs">
          <p className="font-medium">{t("Legenda", "Legend")}</p>
          {year === 2026 ? (
            <>
              <p className="font-medium text-primary">
                {t("Kaj je izginilo? — 1825 ∩ OSM", "What has vanished? — 1825 ∩ OSM")}
              </p>
              {PRESENCE_LEGEND.map((l) => (
                <p key={l.status} className="flex items-center gap-2">
                  <span aria-hidden="true">{l.dotSi}</span>
                  <span>
                    <span className="font-medium">{lang === "si" ? l.labelSi : l.labelEn}</span>{" "}
                    ·{" "}
                    {l.status === "exists"
                      ? IZGINILO_STATS.exists
                      : l.status === "uncertain"
                        ? IZGINILO_STATS.uncertain
                        : IZGINILO_STATS.gone}{" "}
                    — {lang === "si" ? l.noteSi : l.noteEn}
                  </span>
                </p>
              ))}
              <p className="flex items-center gap-2">
                <span className="inline-block size-3 rounded-[2px] bg-[#6b7566]" aria-hidden="true" />
                {t(
                  `današnje stavbe — OSM posnetek ${IZGINILO_STATS.osmSnapshot} (${IZGINILO_STATS.presentCount})`,
                  `present-day buildings — OSM snapshot ${IZGINILO_STATS.osmSnapshot} (${IZGINILO_STATS.presentCount})`,
                )}
              </p>
            </>
          ) : (
            <>
              <p className="flex items-center gap-2">
                <span className="inline-block size-3 rounded-[2px] bg-[#d8cdb8]" aria-hidden="true" />
                {t("hiše ~1825 (apna/bela)", "houses ~1825 (whitewashed)")}
              </p>
              <p className="flex items-center gap-2">
                <span className="inline-block size-3 rounded-[2px] bg-[#c2b08c]" aria-hidden="true" />
                {t("zgostitev ~1900 (ocena)", "~1900 densification (estimate)")}
              </p>
            </>
          )}
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#9ec497]" aria-hidden="true" />
            {t("loke ob Kolpi", "meadows by the Kolpa")}
          </p>
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#d9c27a]" aria-hidden="true" />
            {t("njive/ornina", "fields/arable")}
          </p>
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-full bg-[#4d6b3f]" aria-hidden="true" />
            {t(
              `drevesa — gozd + razpršena (${TREE_STATS.total}; interpretacija iz con rabe tal)`,
              `trees — forest + scattered (${TREE_STATS.total}; interpretation from land-use zones)`,
            )}
          </p>
          {year !== 2026 && (
            <p className="flex items-center gap-2">
              <span className="text-sm" aria-hidden="true">💨</span>
              {t(
                "dim iz dimnikov — vasa živi (interpretacija)",
                "chimney smoke — the village lives (interpretation)",
              )}
            </p>
          )}
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#5d7355]" aria-hidden="true" />
            {t("gozd (Brezov gozd)", "forest (Brezov gozd)")}
          </p>
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#6f9ec4]" aria-hidden="true" />
            {t("Kolpa — georeferencirana struga", "Kolpa — georeferenced channel")}
          </p>
        </div>

        <div className="flex flex-col gap-2">
          <button
            type="button"
            onClick={() => openTM(year)}
            className="inline-flex h-10 items-center justify-center gap-2 rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
          >
            <Camera className="size-4" aria-hidden="true" />
            {t("Odpri v AR (kamera na lokaciji)", "Open in AR (camera on site)")}
          </button>
          <p className="text-[11px] leading-relaxed text-muted-foreground">
            {t(
              "AR odpre kamero telefona in postavi vas — na vašem stojišču — sredi vasi v izbranem letu; zajemite fotografijo.",
              "AR opens your phone camera and places you — at your standing point — inside the village in the chosen year; capture a photo.",
            )}
          </p>
        </div>

        <p className="flex items-start gap-1.5 text-[11px] leading-relaxed text-muted-foreground">
          <button
            type="button"
            onClick={() => sceneRef.current?.resetView()}
            className="inline-flex items-center gap-1.5 rounded-md border border-border px-2.5 py-1.5 font-medium text-foreground transition-colors hover:border-primary/40 hover:text-primary"
          >
            <RotateCcw className="size-3.5" aria-hidden="true" />
            {t("Ponastavi pogled", "Reset view")}
          </button>
        </p>
      </div>
    </div>
  );
}
