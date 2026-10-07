"use client";

/**
 * Kamera AR — zgodovinski objekt v objektivu telefona.
 *
 * Arhitektura (brez plačljivih AI storitev — samo brskalniški API-ji):
 *  · zadaj  <video>  iz getUserMedia (zadnja kamera, facingMode: environment)
 *  · spredaj <model-viewer> z GLB modelom, lebdi nad kamero
 *  · kompas (DeviceOrientation) + GPS azimut → model zasidran v smeri objekta:
 *    premikate telefon, model drsi po zaslonu, kot da stoji na svetu
 *  · GPS razdalja do prave lokacije; blizu → »na lokaciji«, daleč → predogled
 *  · tap na napis → muzejski zapis z viri; gumb → bralska sinteza (govor)
 *  · naprave z WebXR/Scene Viewer: gumb »Postavi v prostor« (activateAR)
 *
 * Vse je postopno: brez kamere → arhivsko ozadje; brez kompasa → fiksni model;
 * brez GPS → pošten predogled. Česa ni, komponenta ne izmišljuje.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  ArrowUp,
  Camera,
  CheckCircle2,
  Compass,
  Crosshair,
  Footprints,
  MapPin,
  Navigation,
  Volume2,
  VolumeX,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLang } from "./language-context";
import type { Exhibit } from "@/lib/museum";
import {
  angleDelta,
  bearingDeg,
  distanceM,
  formatDistance,
  osmDirectionsUrl,
  type GeoFix,
} from "@/lib/geo";
import { useCompass } from "@/hooks/use-compass";
import type { UseGeolocation } from "@/hooks/use-geolocation";
import { sceneReadiness } from "@/data/atlas/geotruth";

/** prag »na lokaciji« v metrih (natančnost GPS na telefonu ± 5–20 m) */
const ON_SITE_M = 300;

type ModelViewerElement = HTMLElement & {
  canActivateAR: boolean | null;
  activateAR: () => void;
};

export function ARCameraView({
  exhibit,
  fix,
  geoQuality,
  geoActive,
  onStartGps,
  onClose,
  onOpenExhibit,
}: {
  exhibit: Exhibit;
  fix: GeoFix | null;
  geoQuality: UseGeolocation["quality"];
  geoActive: boolean;
  onStartGps: () => void;
  onClose: () => void;
  onOpenExhibit: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const mvRef = useRef<ModelViewerElement | null>(null);

  const [camera, setCamera] = useState<"starting" | "live" | "unavailable">(
    "starting",
  );
  const [speaking, setSpeaking] = useState(false);
  const [canNativeAR, setCanNativeAR] = useState(false);

  /* kompas (issue #14): glajen + stabilnost + iOS dovoljenje */
  const {
    heading,
    stability: compassStability,
    needsPermission: iosCompassBlocked,
    requestPermission: enableCompass,
  } = useCompass();

  const lat = exhibit.lat;
  const lng = exhibit.lng;
  const title = lang === "si" ? exhibit.titleSi : exhibit.titleEn;

  /* ── registracija <model-viewer> (ločen chunk, enako kot 3D-list) ── */
  useEffect(() => {
    import("@google/model-viewer").catch((err) => {
      console.error("model-viewer load failed", err);
    });
  }, []);

  /* ── kamera: zadnji objektiv, če je na voljo ── */
  useEffect(() => {
    let cancelled = false;
    const request: Promise<MediaStream> = navigator.mediaDevices?.getUserMedia
      ? navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: "environment" } },
          audio: false,
        })
      : Promise.reject(new Error("getUserMedia not available"));
    request
      .then((stream) => {
        if (cancelled) {
          stream.getTracks().forEach((tr) => tr.stop());
          return;
        }
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play().catch(() => undefined);
        }
        setCamera("live");
      })
      .catch(() => !cancelled && setCamera("unavailable"));
    return () => {
      cancelled = true;
      streamRef.current?.getTracks().forEach((tr) => tr.stop());
      streamRef.current = null;
    };
  }, []);

  /* ── kompas: iOS dovoljenje (dogodki sami prihajajo iz use-compass) ── */

  /* ── govorna sinteza (brezplačna, v brskalniku) ── */
  useEffect(() => {
    return () => speechSynthesis?.cancel();
  }, []);
  const toggleSpeech = useCallback(() => {
    if (typeof speechSynthesis === "undefined") return;
    if (speaking) {
      speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }
    const summary = lang === "si" ? exhibit.summarySi : exhibit.summaryEn;
    const u = new SpeechSynthesisUtterance(`${title}. ${summary}`);
    u.lang = lang === "si" ? "sl-SI" : "en-GB";
    u.onend = () => setSpeaking(false);
    u.onerror = () => setSpeaking(false);
    speechSynthesis.speak(u);
    setSpeaking(true);
  }, [lang, speaking, exhibit.summarySi, exhibit.summaryEn, title]);

  /* ── naravni AR (WebXR / Scene Viewer), če ga naprava ponuja ── */
  useEffect(() => {
    const el = mvRef.current;
    if (!el) return;
    const check = () => setCanNativeAR(Boolean(el.canActivateAR));
    el.addEventListener("load", check);
    const probe = window.setTimeout(check, 1200);
    return () => {
      el.removeEventListener("load", check);
      window.clearTimeout(probe);
    };
  }, []);

  /* ── matematika zasidranja: kam glede telefona stoji objekt ── */
  const distance =
    fix && lat != null && lng != null ? distanceM(fix, { lat, lng }) : null;
  const onSite = distance != null && distance <= ON_SITE_M;
  const targetBearing =
    fix && lat != null && lng != null ? bearingDeg(fix, { lat, lng }) : null;
  const delta =
    heading != null && targetBearing != null
      ? angleDelta(heading, targetBearing)
      : null;

  /* kotro drsi model po zaslonu: ±90° → ±45 % širine; prek roba izgine */
  const offsetX = delta != null ? Math.max(-90, Math.min(90, delta)) * 0.5 : 0;
  const visible = delta == null || Math.abs(delta) <= 100;

  /* ESC zapre tudi s tipkovnico */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={t(`AR kamero: ${title}`, `AR camera: ${title}`)}
      className="fixed inset-0 z-50 flex flex-col bg-foreground/95 text-foreground"
    >
      {/* ── ozadje: kamera ali arhivsko ozadje ── */}
      <video
        ref={videoRef}
        playsInline
        muted
        autoPlay
        aria-hidden="true"
        className={`absolute inset-0 h-full w-full object-cover ${
          camera === "live" ? "" : "hidden"
        }`}
      />
      {camera !== "live" && (
        <div
          aria-hidden="true"
          className="mvg-ar-backdrop absolute inset-0"
        />
      )}

      {/* gradienta za berljivost */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-28 bg-gradient-to-b from-black/70 to-transparent"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-black/80 to-transparent"
      />

      {/* ── zgornja vrstica ── */}
      <div className="relative z-10 flex items-center justify-between gap-3 p-4">
        <button
          type="button"
          onClick={onClose}
          className="flex size-10 shrink-0 items-center justify-center rounded-full border border-white/25 bg-black/40 text-white backdrop-blur transition-colors hover:bg-black/60"
          aria-label={t("Zapri AR kamero", "Close AR camera")}
        >
          <X className="size-5" aria-hidden="true" />
        </button>
        <div className="min-w-0 flex-1 text-right">
          <p className="truncate font-display text-sm font-semibold text-white">
            {t("AR — ", "AR — ")}
            {title}
          </p>
          <p className="truncate text-[11px] text-white/70">
            {exhibit.museumNo} ·{" "}
            {t("dokumentirana lokacija", "documented location")}
          </p>
        </div>
      </div>

      {/* ── statusni čip lokacije + pripravljenost (issue #14, točka 11) ── */}
      <div className="relative z-10 flex flex-wrap gap-2 px-4">
        <div className="inline-flex max-w-full items-center gap-2 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white backdrop-blur">
          {onSite ? (
            <>
              <CheckCircle2 className="size-3.5 shrink-0 text-emerald-300" aria-hidden="true" />
              <span>
                {t(
                  `na lokaciji — ${formatDistance(distance ?? 0, lang)}`,
                  `on site — ${formatDistance(distance ?? 0, lang)}`,
                )}
              </span>
            </>
          ) : distance != null ? (
            <>
              <MapPin className="size-3.5 shrink-0 text-amber-200" aria-hidden="true" />
              <span>
                {t(
                  `predogled — do objekta ${formatDistance(distance, lang)}`,
                  `preview — ${formatDistance(distance, lang)} to the object`,
                )}
              </span>
            </>
          ) : geoActive ? (
            <>
              <MapPin className="size-3.5 shrink-0 text-white/80" aria-hidden="true" />
              <span>{t("čakam na GPS …", "waiting for GPS …")}</span>
            </>
          ) : (
            <>
              <Camera className="size-3.5 shrink-0 text-white/80" aria-hidden="true" />
              <span>{t("predogled — GPS ni priključen", "preview — GPS not connected")}</span>
            </>
          )}
        </div>
        {/* pripravljenost scene (issue #14): HIGH/MEDIUM/LOW — vidna negotovost,
            nikoli tiha napačna zasidranost modela */}
        {(() => {
          const r = sceneReadiness({ gps: geoQuality, compass: compassStability });
          if (r.anchor === "HIGH" && !onSite) return null;
          return (
            <div
              className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs backdrop-blur ${
                r.anchor === "HIGH"
                  ? "border-emerald-300/40 bg-emerald-400/15 text-emerald-100"
                  : r.anchor === "MEDIUM"
                    ? "border-amber-300/40 bg-amber-400/15 text-amber-100"
                    : "border-white/20 bg-black/45 text-white/80"
              }`}
              role="status"
            >
              {r.anchor === "HIGH" ? (
                <Crosshair className="size-3.5 shrink-0" aria-hidden="true" />
              ) : (
                <Compass
                  className={`size-3.5 shrink-0 ${r.anchor === "MEDIUM" ? "animate-pulse" : ""}`}
                  aria-hidden="true"
                />
              )}
              <span className="font-medium">
                {r.anchor === "HIGH"
                  ? t("SCENA PORAVNANA", "SCENE ALIGNED")
                  : r.anchor === "MEDIUM"
                    ? t("Poravnava scene …", "Scene aligning …")
                    : t("približno — raziskovanje", "approximate — exploring")}
              </span>
            </div>
          );
        })()}
        {fix?.accuracy != null && (
          <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white/80 backdrop-blur">
            <MapPin className="size-3.5 shrink-0" aria-hidden="true" />
            <span>GPS ±{Math.round(fix.accuracy)} m</span>
          </div>
        )}
        {camera === "unavailable" && (
          <p className="mt-2 max-w-sm text-[11px] leading-relaxed text-white/60">
            {t(
              "Kamera ni na voljo (dovoljenje ali naprava) — prikazujem arhivsko ozadje.",
              "Camera unavailable (permission or device) — showing an archival backdrop.",
            )}
          </p>
        )}
      </div>

      {/* ── sredina: model, zasidran na smer ── */}
      <div className="relative z-10 flex flex-1 items-center justify-center overflow-hidden px-4">
        <div
          className="w-[92vw] max-w-lg transition-transform duration-200 ease-linear sm:w-[440px]"
          style={{
            transform: `translateX(${offsetX}vw)`,
            opacity: visible ? 1 : 0,
            transitionProperty: "transform, opacity",
          }}
        >
          {/* videnica za berljivost modela nad ozadjem */}
          <div
            aria-hidden="true"
            className="pointer-events-none mx-auto h-40 w-52 rounded-full bg-black/25 blur-2xl"
          />
          {exhibit.model3dUrl && (
            <model-viewer
              ref={mvRef}
              src={exhibit.model3dUrl}
              /* iOS nima WebXR — USDZ dvojnik odpre AR Quick Look (Nîmes vzorec) */
              ios-src={exhibit.model3dUrl.replace(/\.glb$/, ".usdz")}
              alt={t(
                `Interpretativni 3D-model: ${title}`,
                `Interpretive 3D model: ${title}`,
              )}
              camera-controls
              auto-rotate
              rotation-per-second="18deg"
              camera-orbit="0deg 72deg 48m"
              min-camera-orbit="auto 15deg 22m"
              max-camera-orbit="auto 179deg 95m"
              shadow-intensity="0.6"
              shadow-softness="0.8"
              exposure="1.15"
              field-of-view="24deg"
              max-field-of-view="26deg"
              min-field-of-view="12deg"
              ar
              ar-modes="webxr scene-viewer quick-look"
              ar-placement="floor"
              ar-scale="auto"
              className="block h-[46vh] w-full [&::part(default-progress-bar)]:hidden [&::part(default-ar-button)]:hidden"
            />
          )}
          {/* mehka senca — model stoji na tleh, ne plava */}
          <div
            aria-hidden="true"
            className="pointer-events-none mx-auto -mt-5 h-8 w-48 rounded-[50%] bg-black/45 blur-md"
          />
        </div>

        {/* puščica »proti objektu«, ko telefon gleda drugam */}
        {delta != null && Math.abs(delta) > 35 && (
          <div className="absolute bottom-2 left-1/2 -translate-x-1/2">
            <div className="flex size-16 items-center justify-center rounded-full border border-white/25 bg-black/45 backdrop-blur">
              <ArrowUp
                className="size-7 text-white"
                style={{ transform: `rotate(${delta}deg)` }}
                aria-hidden="true"
              />
            </div>
            <p className="sr-only">
              {t(
                `Obrnite telefon za ${Math.abs(Math.round(delta))} stopinj`,
                `Turn the phone by ${Math.abs(Math.round(delta))} degrees`,
              )}
            </p>
          </div>
        )}
      </div>

      {/* ── spodnja vrstica: zapis, govor, navigacija, AR ── */}
      <div className="relative z-10 space-y-3 p-4 pb-[max(1rem,env(safe-area-inset-bottom))]">
        {/* kompas: iOS blokada ali sporočilo o fiksno prikazanem modelu */}
        {heading == null &&
          (iosCompassBlocked ? (
            <button
              type="button"
              onClick={enableCompass}
              className="mx-auto flex items-center gap-1.5 rounded-full border border-white/25 bg-black/40 px-4 py-2 text-xs text-white backdrop-blur transition-colors hover:bg-black/60"
            >
              <Compass className="size-3.5" aria-hidden="true" />
              {t("Omogoči kompas", "Enable compass")}
            </button>
          ) : (
            <p className="text-center text-[11px] text-white/60">
              {t(
                "Kompas ni na voljo — model je prikazan fiksno.",
                "Compass unavailable — the model is shown fixed.",
              )}
            </p>
          ))}
        <button
          type="button"
          onClick={() => onOpenExhibit(exhibit.slug)}
          className="flex w-full items-center gap-3 rounded-xl border border-white/20 bg-black/50 p-3 text-left text-white backdrop-blur transition-colors hover:bg-black/70"
        >
          <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary/20 font-mono text-[10px] font-semibold text-primary-foreground/90">
            {exhibit.museumNo.replace("MVG-", "")}
          </span>
          <span className="min-w-0 flex-1">
            <span className="block truncate text-sm font-semibold">
              {t("Zapis in viri — povečaj", "Record & sources — open")}
            </span>
            <span className="block truncate text-xs text-white/70">{title}</span>
          </span>
          <span aria-hidden="true" className="text-white/50">→</span>
        </button>

        <div className="flex flex-wrap gap-2">
          <Button
            type="button"
            variant="secondary"
            size="sm"
            onClick={toggleSpeech}
            aria-pressed={speaking}
            className="gap-1.5"
          >
            {speaking ? (
              <VolumeX className="size-4" aria-hidden="true" />
            ) : (
              <Volume2 className="size-4" aria-hidden="true" />
            )}
            {speaking ? t("Ustavi govor", "Stop speech") : t("Preberi naglas", "Read aloud")}
          </Button>

          {lat != null && lng != null && (
            <a
              href={osmDirectionsUrl({ lat, lng }, fix)}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex h-8 items-center gap-1.5 rounded-md border border-white/25 bg-black/40 px-3 text-xs font-medium text-white backdrop-blur transition-colors hover:bg-black/60"
            >
              <Navigation className="size-3.5" aria-hidden="true" />
              {t("Navigiraj", "Navigate")}
            </a>
          )}

          {!geoActive && (
            <button
              type="button"
              onClick={onStartGps}
              className="inline-flex h-8 items-center gap-1.5 rounded-md border border-white/25 bg-black/40 px-3 text-xs font-medium text-white backdrop-blur transition-colors hover:bg-black/60"
            >
              <Footprints className="size-3.5" aria-hidden="true" />
              {t("Priklopi GPS", "Connect GPS")}
            </button>
          )}

          {canNativeAR && exhibit.model3dUrl && (
            <button
              type="button"
              onClick={() => mvRef.current?.activateAR()}
              className="inline-flex h-8 items-center gap-1.5 rounded-md border border-white/25 bg-primary/70 px-3 text-xs font-semibold text-primary-foreground backdrop-blur transition-colors hover:bg-primary"
            >
              <Footprints className="size-3.5" aria-hidden="true" />
              {t("Postavi v prostor (AR)", "Place in space (AR)")}
            </button>
          )}
        </div>

        {exhibit.model3dCredit && (
          <p className="text-[10px] leading-relaxed text-white/50">
            {exhibit.model3dCredit}
          </p>
        )}
      </div>
    </div>
  );
}
