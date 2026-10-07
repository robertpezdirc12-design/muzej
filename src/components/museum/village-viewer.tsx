"use client";

/**
 * 3D VAS 1825 — orbit pregledovalnik za ATLAS (issue #10).
 *
 * Isti prizor kot AR časovni stroj, brez kamere: prosto vrtenje in zoom,
 * preklop letnic, legenda in gumb v AR. Namizje in telefon.
 */

import { useEffect, useRef, useState } from "react";
import { Camera, Info, Layers, RotateCcw } from "lucide-react";
import { useLang } from "./language-context";
import { useTimeMachine, type TimeYear } from "@/lib/time-machine-store";
import { PERIODS } from "@/lib/village3d";

export function VillageViewer() {
  const { t, lang } = useLang();
  const { year, setYear, openTM } = useTimeMachine();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const sceneRef = useRef<import("./village-scene").VillageScene | null>(null);
  const yearRef = useRef(year);
  const [ready, setReady] = useState(false);
  const [failed, setFailed] = useState(false);

  const period = PERIODS.find((p) => p.year === year) ?? PERIODS[0];

  useEffect(() => {
    let cancelled = false;
    let scene: import("./village-scene").VillageScene | null = null;
    import("./village-scene")
      .then(({ VillageScene }) => {
        if (cancelled || !canvasRef.current) return;
        scene = new VillageScene(canvasRef.current, { mode: "orbit" });
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
            {t("gradim vas iz 156 katastrskih podlatn …", "building the village from 156 cadastral footprints …")}
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
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#d8cdb8]" aria-hidden="true" />
            {t("hiše ~1825 (apna/bela)", "houses ~1825 (whitewashed)")}
          </p>
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#c2b08c]" aria-hidden="true" />
            {t("zgostitev ~1900 (ocena)", "~1900 densification (estimate)")}
          </p>
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#9ec497]" aria-hidden="true" />
            {t("loke ob Kolpi", "meadows by the Kolpa")}
          </p>
          <p className="flex items-center gap-2">
            <span className="inline-block size-3 rounded-[2px] bg-[#d9c27a]" aria-hidden="true" />
            {t("njive/ornina", "fields/arable")}
          </p>
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
