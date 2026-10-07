"use client";

/**
 * Vodeni sprehod po vasi — izberi pot → postaja za postajo.
 *
 * Vsaka postaja je PRAVI muzejski zapis (vir: extra.json → walk):
 * kuratorsko besedilo, gumb za zapis, navigacija do lokacije (OSM),
 * govor (bralska sinteza brskalnika — brezplačna), AR če zapis ima model.
 * Zadnja postaja začne od začetka — pot deluje od začetka do konca.
 */

import { useMemo, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Flag,
  Navigation,
  RotateCcw,
  Volume2,
  VolumeX,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLang } from "./language-context";
import { WALKS, walkLocatedCount, type WalkDef } from "@/lib/walks";
import { distanceM, formatDistance, osmDirectionsUrl, type GeoFix } from "@/lib/geo";

export function GuidedWalk({
  fix,
  onOpen,
  onStartAr,
}: {
  fix: GeoFix | null;
  onOpen: (slug: string) => void;
  onStartAr: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const [walk, setWalk] = useState<WalkDef>(WALKS[0]);
  const [idx, setIdx] = useState(0);
  const [speaking, setSpeaking] = useState(false);

  const stop = walk.stops[idx];
  const ex = stop.exhibit;
  const located = ex.lat != null && ex.lng != null;
  const arReady = Boolean(ex.model3dUrl && located);
  const distance =
    fix && located ? distanceM(fix, { lat: ex.lat!, lng: ex.lng! }) : null;
  const done = idx === walk.stops.length - 1;

  const stopCount = useMemo(() => walk.stops.length, [walk]);

  const pick = (w: WalkDef) => {
    speechSynthesis?.cancel();
    setSpeaking(false);
    setWalk(w);
    setIdx(0);
  };

  const go = (next: number) => {
    speechSynthesis?.cancel();
    setSpeaking(false);
    setIdx(Math.max(0, Math.min(stopCount - 1, next)));
  };

  const toggleSpeech = () => {
    if (typeof speechSynthesis === "undefined") return;
    if (speaking) {
      speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }
    const title = lang === "si" ? ex.titleSi : ex.titleEn;
    const note =
      stop.note ??
      (lang === "si" ? ex.summarySi : ex.summaryEn);
    const u = new SpeechSynthesisUtterance(
      t(`Postaja ${stop.station}. ${title}.`, `Stop ${stop.station}. ${title}. `) +
        note,
    );
    u.lang = lang === "si" ? "sl-SI" : "en-GB";
    u.onend = () => setSpeaking(false);
    u.onerror = () => setSpeaking(false);
    speechSynthesis.speak(u);
    setSpeaking(true);
  };

  return (
    <div className="rounded-xl border bg-card p-4 sm:p-6">
      <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
        <Flag className="size-5 text-primary" aria-hidden="true" />
        {t("Vodeni sprehod", "Guided walk")}
      </h3>
      <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
        {t(
          "Izberite pot in sledite postajam — besedilo, govor, navigacija in AR na lokaciji.",
          "Pick a route and follow the stops — text, speech, navigation and AR on location.",
        )}
      </p>

      {/* izbira poti */}
      <div className="mt-4 flex flex-wrap gap-2" role="tablist" aria-label={t("Izbira sprehoda", "Walk selection")}>
        {WALKS.map((w) => {
          const active = w.key === walk.key;
          return (
            <button
              key={w.key}
              type="button"
              role="tab"
              aria-selected={active}
              onClick={() => pick(w)}
              className={`rounded-full border px-3 py-1.5 text-xs font-medium transition-colors ${
                active
                  ? "border-primary bg-primary text-primary-foreground"
                  : "border-border bg-secondary/50 text-muted-foreground hover:border-primary/40 hover:text-foreground"
              }`}
            >
              {lang === "si" ? w.nameSi : w.nameEn}
              <span className="ml-1.5 font-mono text-[10px] opacity-70">
                {w.stops.length}
              </span>
            </button>
          );
        })}
      </div>

      <p className="mt-2 text-[11px] text-muted-foreground">
        {lang === "si" ? walk.descSi : walk.descEn}{" "}
        {t(
          `${walkLocatedCount(walk)} od ${walk.stops.length} postaj ima lokacijo za navigacijo.`,
          `${walkLocatedCount(walk)} of ${walk.stops.length} stops have a location for navigation.`,
        )}
      </p>

      {/* napredek */}
      <div className="mt-4">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>
            {t(
              `Postaja ${idx + 1} od ${stopCount}`,
              `Stop ${idx + 1} of ${stopCount}`,
            )}
          </span>
          <span className="font-mono">{Math.round(((idx + 1) / stopCount) * 100)} %</span>
        </div>
        <div
          className="mt-1 h-1.5 overflow-hidden rounded-full bg-secondary"
          role="progressbar"
          aria-valuemin={1}
          aria-valuemax={stopCount}
          aria-valuenow={idx + 1}
          aria-label={t("Napredek sprehoda", "Walk progress")}
        >
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${((idx + 1) / stopCount) * 100}%` }}
          />
        </div>
      </div>

      {/* kartica postaje */}
      <div className="mt-4 rounded-lg border bg-secondary/40 p-4">
        <p className="font-mono text-[11px] font-semibold text-primary">
          {t("postaja", "stop")} {stop.station} · {ex.museumNo}
        </p>
        <h4 className="mt-1 font-display text-base font-semibold">
          {lang === "si" ? ex.titleSi : ex.titleEn}
        </h4>
        {stop.note && (
          <p className="mt-2 text-sm leading-relaxed text-foreground/90">
            {stop.note}
          </p>
        )}

        <div className="mt-3 flex flex-wrap items-center gap-2">
          <Button type="button" variant="outline" size="sm" onClick={() => onOpen(ex.slug)}>
            {t("Odpri zapis", "Open record")}
          </Button>
          <Button
            type="button"
            variant="secondary"
            size="sm"
            onClick={toggleSpeech}
            aria-pressed={speaking}
            className="gap-1.5"
          >
            {speaking ? <VolumeX className="size-4" aria-hidden="true" /> : <Volume2 className="size-4" aria-hidden="true" />}
            {speaking ? t("Ustavi", "Stop") : t("Preberi", "Read aloud")}
          </Button>
          {located && (
            <a
              href={osmDirectionsUrl({ lat: ex.lat!, lng: ex.lng! }, fix)}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex h-8 items-center gap-1.5 rounded-md border border-border px-3 text-xs font-medium transition-colors hover:border-primary/40 hover:text-foreground"
            >
              <Navigation className="size-3.5" aria-hidden="true" />
              {distance != null
                ? t(`Navigiraj (${formatDistance(distance, lang)})`, `Navigate (${formatDistance(distance, lang)})`)
                : t("Navigiraj", "Navigate")}
            </a>
          )}
          {arReady && (
            <Button type="button" size="sm" onClick={() => onStartAr(ex.slug)} className="gap-1.5">
              <Navigation className="size-3.5" aria-hidden="true" />
              {t("Odpri v AR", "Open in AR")}
            </Button>
          )}
        </div>
      </div>

      {/* krmiljenje */}
      <div className="mt-4 flex items-center justify-between gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => go(idx - 1)}
          disabled={idx === 0}
          className="gap-1.5"
        >
          <ArrowLeft className="size-4" aria-hidden="true" />
          {t("Prejšnja", "Previous")}
        </Button>

        {done ? (
          <div className="flex items-center gap-2">
            <CheckCircle2 className="size-4 text-primary" aria-hidden="true" />
            <span className="text-xs font-medium text-muted-foreground">
              {t("Konec poti", "Route complete")}
            </span>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => go(0)}
              className="gap-1.5"
            >
              <RotateCcw className="size-3.5" aria-hidden="true" />
              {t("Od začetka", "Restart")}
            </Button>
          </div>
        ) : (
          <Button type="button" size="sm" onClick={() => go(idx + 1)} className="gap-1.5">
            {t("Naslednja postaja", "Next stop")}
            <ArrowRight className="size-4" aria-hidden="true" />
          </Button>
        )}
      </div>
    </div>
  );
}
