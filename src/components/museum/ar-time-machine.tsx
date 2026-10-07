"use client";

/**
 * AR ČASOVNI STROJ (issue #10) — 3D rekonstrukcija vasi Griblje skozi čas.
 *
 * Zaslon telefona = okno v leto 1825 (ali ~1900 / danes):
 *  · zadaj živa kamera (getUserMedia), spredaj proceduralna 3D vas iz
 *    Franciscejskega katastra (156 stavb) zasidrana na GPS + kompas;
 *  · drsnik let: 1825 · ~1900 (ocena) · danes (duhovi);
 *  · zajem: gumb sprožilc → PNG s podpisom (prenos/deljenje);
 *  · tap na hišo → kartica stavbe s hišno zgodbo (register × matrike);
 *  · brez senzorjev: pošten predogled (vlečenje obrača pogled).
 *
 * Kot pri ar-camera: nič se ne izmišljuje — kar manjka (kamera, kompas, GPS),
 * komponenta to pove in ponudi alternativo.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  Camera,
  CheckCircle2,
  Clock,
  Compass,
  Download,
  Home,
  MapPin,
  Share2,
  X,
} from "lucide-react";
import { useLang } from "./language-context";
import { useTimeMachine, type TimeYear } from "@/lib/time-machine-store";
import { PERIODS, toLocal, ORIGIN, CORE_R } from "@/lib/village3d";
import { distanceM, formatDistance, type GeoFix } from "@/lib/geo";
import type { UseGeolocation } from "@/hooks/use-geolocation";
import type { PickResult } from "./village-scene";
import { HOUSE_VITALS } from "@/data/atlas/parish";

interface DeviceOrientationEventIOS extends DeviceOrientationEvent {
  webkitCompassHeading?: number;
}

interface BuildingCard {
  kind: "1825" | "growth";
  w: number;
  d: number;
  dist: number;
  nearChurch: boolean;
  core: boolean;
}

export function ARTimeMachine({
  geo,
  onOpenExhibit,
}: {
  geo: UseGeolocation;
  onOpenExhibit: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const { year, setYear, close } = useTimeMachine();
  const { fix, status, start } = geo;

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const sceneRef = useRef<import("./village-scene").VillageScene | null>(null);
  const yearRef = useRef(year);

  const [camera, setCamera] = useState<"starting" | "live" | "unavailable">("starting");
  const [heading, setHeading] = useState<number | null>(null);
  const [iosCompassBlocked, setIosCompassBlocked] = useState(false);
  const [card, setCard] = useState<BuildingCard | null>(null);
  const [hint, setHint] = useState(true);
  const [flash, setFlash] = useState(false);
  const [saved, setSaved] = useState<"none" | "saved" | "shared" | "error">("none");

  const period = PERIODS.find((p) => p.year === year) ?? PERIODS[0];

  /* ── 3D prizor (three.js dinamično — izven glavnega snopa) ── */
  useEffect(() => {
    let cancelled = false;
    let scene: InstanceType<
      typeof import("./village-scene").VillageScene
    > | null = null;
    import("./village-scene").then(({ VillageScene }) => {
      if (cancelled || !canvasRef.current) return;
      scene = new VillageScene(canvasRef.current, {
        mode: "ar",
        onPick: (p: PickResult | null) => {
          if (!p) return;
          setCard({
            kind: p.kind,
            w: Math.round(p.w),
            d: Math.round(p.d),
            dist: p.dist,
            nearChurch: Math.hypot(p.x - 0, p.z - 0) < 80,
            core: Math.hypot(p.x, p.z) <= CORE_R,
          });
          setHint(false);
        },
      });
      scene.setYear(yearRef.current);
      sceneRef.current = scene;
    });
    return () => {
      cancelled = true;
      scene?.dispose();
      sceneRef.current = null;
    };
  }, []);

  /* ── kamera ── */
  useEffect(() => {
    let cancelled = false;
    navigator.mediaDevices
      ?.getUserMedia({
        video: { facingMode: { ideal: "environment" } },
        audio: false,
      })
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

  /* ── kompas ── */
  useEffect(() => {
    const onOrient = (e: DeviceOrientationEvent) => {
      const ios = e as DeviceOrientationEventIOS;
      if (typeof ios.webkitCompassHeading === "number") {
        setHeading(ios.webkitCompassHeading);
      } else if (e.alpha != null) {
        setHeading((360 - e.alpha) % 360);
      }
    };
    window.addEventListener("deviceorientation", onOrient, true);
    const probe = window.setTimeout(() => {
      const DOE = DeviceOrientationEvent as typeof DeviceOrientationEvent & {
        requestPermission?: () => Promise<"granted" | "denied">;
      };
      if (typeof DOE.requestPermission === "function") setIosCompassBlocked(true);
    }, 800);
    return () => {
      window.removeEventListener("deviceorientation", onOrient, true);
      window.clearTimeout(probe);
    };
  }, []);

  useEffect(() => {
    sceneRef.current?.setCompassYaw(heading);
  }, [heading]);

  /* ── preklop letnice → prizor ── */
  useEffect(() => {
    yearRef.current = year;
    sceneRef.current?.setYear(year);
    setCard(null);
  }, [year]);

  /* ── GPS → sidro prizora ── */
  useEffect(() => {
    if (fix) {
      const { x, z } = toLocal(fix.lat, fix.lng);
      sceneRef.current?.setFix(x, z);
    }
  }, [fix]);

  /* ── ESC ── */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && close();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [close]);

  const enableCompass = useCallback(async () => {
    const DOE = DeviceOrientationEvent as typeof DeviceOrientationEvent & {
      requestPermission?: () => Promise<"granted" | "denied">;
    };
    if (typeof DOE.requestPermission === "function") {
      try {
        const r = await DOE.requestPermission();
        if (r !== "granted") return;
      } catch {
        return;
      }
    }
    setIosCompassBlocked(false);
  }, []);

  /* razdalja uporabnika od jedra vasi (predogled/na lokaciji) */
  const coreDistance =
    fix && fix.lat != null && fix.lng != null
      ? distanceM(fix, { lat: ORIGIN.lat, lng: ORIGIN.lng })
      : null;
  const onSite = coreDistance != null && coreDistance <= 1500;

  /* ── zajem fotografije ── */
  const capture = useCallback(async () => {
    setFlash(true);
    window.setTimeout(() => setFlash(false), 260);
    const sc = sceneRef.current;
    if (!sc) return;
    const y = year === 2026 ? "danes" : year === 1900 ? "~1900" : "1825";
    const data = sc.capture(videoRef.current, {
      title: t(
        `Griblje ${y} — rekonstrukcija vasi`,
        `Griblje ${y} — village reconstruction`,
      ),
      sub: t(
        "Muzej vasi Griblje · 3D rekonstrukcija iz Franciscejskega katastra (list A02, SI AS 176)",
        "Museum of Griblje village · 3D reconstruction from the Franciscean cadastre (sheet A02, SI AS 176)",
      ),
      credit: "griblje-museum.vercel.app · RECONSTRUCTED",
    });
    if (!data) {
      setSaved("error");
      window.setTimeout(() => setSaved("none"), 2600);
      return;
    }
    const fname = `griblje-${year === 2026 ? "danes" : year}.png`;
    /* najprej deljenje (telefon), sicer prenos */
    try {
      const blob = await (await fetch(data)).blob();
      const file = new File([blob], fname, { type: "image/png" });
      const nav = navigator as Navigator & {
        canShare?: (d: { files: File[] }) => boolean;
      };
      if (nav.share && nav.canShare?.({ files: [file] })) {
        await nav.share({
          files: [file],
          title: `Griblje ${y}`,
        });
        setSaved("shared");
        window.setTimeout(() => setSaved("none"), 2600);
        return;
      }
    } catch {
      /* preklic deljenja ni napaka — nadaljuj s prenosom */
    }
    const a = document.createElement("a");
    a.href = data;
    a.download = fname;
    a.click();
    setSaved("saved");
    window.setTimeout(() => setSaved("none"), 2600);
  }, [year, t]);

  const yearButtons: [TimeYear, string, string][] = [
    [1825, "1825", "1825"],
    [1900, "~1900", "~1900"],
    [2026, "danes", "today"],
  ];

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={t(
        "Časovni stroj — 3D rekonstrukcija vasi Griblje",
        "Time machine — 3D reconstruction of Griblje village",
      )}
      className="fixed inset-0 z-50 flex flex-col bg-foreground/95 text-foreground"
    >
      {/* ozadje: kamera ali temna kulisa */}
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
        <div aria-hidden="true" className="mvg-ar-backdrop absolute inset-0" />
      )}

      {/* 3D vas čez kamero */}
      <canvas
        ref={canvasRef}
        aria-label={t(
          "3D rekonstrukcija vasi — vlecite za obrat pogleda, tapnite hišo",
          "3D village reconstruction — drag to look around, tap a house",
        )}
        className="absolute inset-0 h-full w-full touch-none"
      />

      {/* gradienta berljivosti */}
      <div aria-hidden="true" className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-black/70 to-transparent" />
      <div aria-hidden="true" className="pointer-events-none absolute inset-x-0 bottom-0 h-64 bg-gradient-to-t from-black/85 to-transparent" />

      {/* blisk zajema */}
      {flash && <div aria-hidden="true" className="pointer-events-none absolute inset-0 bg-white/80 animate-out fade-out duration-200" />}

      {/* zgornja vrstica */}
      <div className="relative z-10 flex items-center justify-between gap-3 p-4">
        <button
          type="button"
          onClick={close}
          className="flex size-10 shrink-0 items-center justify-center rounded-full border border-white/25 bg-black/40 text-white backdrop-blur transition-colors hover:bg-black/60"
          aria-label={t("Zapri časovni stroj", "Close the time machine")}
        >
          <X className="size-5" aria-hidden="true" />
        </button>
        <div className="min-w-0 flex-1 text-right">
          <p className="truncate font-display text-sm font-semibold text-white">
            {t("Časovni stroj — Griblje", "Time machine — Griblje")}
          </p>
          <p className="truncate text-[11px] text-white/70">
            {t("3D rekonstrukcija vasi skozi čas", "3D village reconstruction through time")}
          </p>
        </div>
      </div>

      {/* statusni čipi */}
      <div className="relative z-10 flex flex-wrap gap-2 px-4">
        <div className="inline-flex max-w-full items-center gap-2 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white backdrop-blur">
          {onSite ? (
            <>
              <CheckCircle2 className="size-3.5 shrink-0 text-emerald-300" aria-hidden="true" />
              <span>
                {t(
                  `na lokaciji vasi${coreDistance != null ? ` — ${formatDistance(coreDistance, lang)} do jedra` : ""}`,
                  `on village site${coreDistance != null ? ` — ${formatDistance(coreDistance, lang)} to the core` : ""}`,
                )}
              </span>
            </>
          ) : coreDistance != null ? (
            <>
              <MapPin className="size-3.5 shrink-0 text-amber-200" aria-hidden="true" />
              <span>
                {t(
                  `predogled — ${formatDistance(coreDistance, lang)} od vasi`,
                  `preview — ${formatDistance(coreDistance, lang)} from the village`,
                )}
              </span>
            </>
          ) : (
            <>
              <MapPin className="size-3.5 shrink-0 text-white/80" aria-hidden="true" />
              <span>
                {status === "watching"
                  ? t("čakam na GPS …", "waiting for GPS …")
                  : t("predogled — GPS ni priključen", "preview — GPS not connected")}
              </span>
            </>
          )}
        </div>
        <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white backdrop-blur">
          <Clock className="size-3.5 shrink-0 text-white/80" aria-hidden="true" />
          <span>
            {period.labelSi} ·{" "}
            {period.buildingCount}{" "}
            {t("stavb", "buildings")}
          </span>
        </div>
        {status !== "watching" && (
          <button
            type="button"
            onClick={start}
            className="inline-flex items-center gap-1.5 rounded-full border border-white/25 bg-black/45 px-3 py-1.5 text-xs font-medium text-white backdrop-blur transition-colors hover:bg-black/60"
          >
            <MapPin className="size-3.5" aria-hidden="true" />
            {t("Priklopi GPS", "Connect GPS")}
          </button>
        )}
        {iosCompassBlocked && (
          <button
            type="button"
            onClick={enableCompass}
            className="inline-flex items-center gap-1.5 rounded-full border border-white/25 bg-black/45 px-3 py-1.5 text-xs font-medium text-white backdrop-blur transition-colors hover:bg-black/60"
          >
            <Compass className="size-3.5" aria-hidden="true" />
            {t("Omogoči kompas", "Enable compass")}
          </button>
        )}
      </div>

      {/* prvi namig */}
      {hint && (
        <div className="relative z-10 mx-auto mt-8 max-w-sm rounded-xl border border-white/20 bg-black/50 p-4 text-center backdrop-blur">
          <p className="text-sm leading-relaxed text-white/90">
            {t(
              "Usmerite telefon — vas 1825 stoji pred vami. Vlecite po zaslonu za obrat pogleda, tapnite hišo za njeno zgodbo.",
              "Point your phone — the village of 1825 stands before you. Drag the screen to look around, tap a house for its story.",
            )}
          </p>
          <button
            type="button"
            onClick={() => setHint(false)}
            className="mt-2 text-xs font-medium text-white/70 underline underline-offset-2 hover:text-white"
          >
            {t("Razumem", "Got it")}
          </button>
        </div>
      )}

      {/* kartica stavbe (tap) */}
      {card && (
        <div className="absolute inset-x-4 bottom-44 z-20 sm:left-1/2 sm:right-auto sm:w-[440px] sm:-translate-x-1/2">
          <div className="rounded-xl border border-white/20 bg-black/70 p-4 text-white backdrop-blur">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="font-display text-sm font-semibold">
                  {card.kind === "growth"
                    ? t("Stavba ~1900 (ocena)", "Building ~1900 (estimate)")
                    : t("Stavba ~1825 — kataster", "Building ~1825 — cadastre")}
                </p>
                <p className="mt-1 text-xs text-white/75">
                  {t(
                    `tloris ≈ ${card.w} × ${card.d} m · ${formatDistance(card.dist, lang)} od vas`,
                    `footprint ≈ ${card.w} × ${card.d} m · ${formatDistance(card.dist, lang)} from you`,
                  )}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setCard(null)}
                aria-label={t("Zapri kartico stavbe", "Close building card")}
                className="shrink-0 rounded-full border border-white/25 p-1.5 hover:bg-white/10"
              >
                <X className="size-4" aria-hidden="true" />
              </button>
            </div>

            <div className="mt-3 space-y-2 text-xs leading-relaxed text-white/80">
              {card.kind === "growth" ? (
                <p>
                  {t(
                    "OCENA ~1900: hlev/kašča, zgoščevanje jedra po delitvi domačij — ni v katastru 1825.",
                    "ESTIMATE ~1900: barn/granary, core densification after farm divisions — not in the 1825 cadastre.",
                  )}
                </p>
              ) : (
                <>
                  <p className="flex items-start gap-1.5">
                    <Home className="mt-0.5 size-3.5 shrink-0 text-amber-200" aria-hidden="true" />
                    <span>
                      {t(
                        "Kdo je tu živel? Hišna številka na listu A02 še ni prebrana (TO_COLLECT) — v Registru hiš 1825 je 80 lastnikov, matične knjige (1669–1947) pa dokumentirajo rojstva/poroke/smrti po hišah.",
                        "Who lived here? The house number on sheet A02 has not been read yet (TO_COLLECT) — the 1825 house register holds 80 owners, and the parish registers (1669–1947) document births/marriages/deaths by house.",
                      )}
                    </span>
                  </p>
                  {card.core && (
                    <p>
                      {t(
                        `Primer dokumentirane zgodbe — hiša št. 61: ${HOUSE_VITALS[0].year} ${HOUSE_VITALS[0].whatSi}; ${HOUSE_VITALS[1]?.year ?? ""} ${HOUSE_VITALS[1]?.whatSi ?? ""}.`,
                        `Example of a documented story — house no. 61: ${HOUSE_VITALS[0].year} ${HOUSE_VITALS[0].whatEn}; ${HOUSE_VITALS[1]?.year ?? ""} ${HOUSE_VITALS[1]?.whatEn ?? ""}.`,
                      )}
                    </p>
                  )}
                  {card.nearChurch && (
                    <p>
                      {t(
                        "Stavba stoji ob cerkvi sv. Vida (1526) — njen 3D model je v prizoru na dokumentirani lokaciji.",
                        "The building stands by St. Vitus' church (1526) — its 3D model is in the scene at the documented location.",
                      )}
                    </p>
                  )}
                </>
              )}
              <div className="flex flex-wrap gap-x-4 gap-y-1 pt-1">
                <a
                  href={`/?atlas=hi%C5%A1a-61&odsek=atlas`}
                  className="font-medium text-amber-200 underline decoration-white/30 underline-offset-2 hover:decoration-amber-200"
                >
                  {t("Register hiš 1825", "1825 house register")}
                </a>
                <a
                  href={`/?odsek=atlas`}
                  className="font-medium text-amber-200 underline decoration-white/30 underline-offset-2 hover:decoration-amber-200"
                >
                  {t("Matrike (22 knjig)", "Parish registers (22 books)")}
                </a>
                <button
                  type="button"
                  onClick={() => {
                    close();
                    onOpenExhibit("sveti-vid");
                  }}
                  className="font-medium text-amber-200 underline decoration-white/30 underline-offset-2 hover:decoration-amber-200"
                >
                  {t("Zapis cerkve (MVG-002)", "Church record (MVG-002)")}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* spodnja plošča: časovni drsnik + zajem */}
      <div className="relative z-10 mt-auto space-y-3 p-4 pb-[max(1rem,env(safe-area-inset-bottom))]">
        {/* metodologija leta */}
        <p className="mx-auto max-w-lg text-center text-[11px] leading-relaxed text-white/70">
          {lang === "si" ? period.noteSi : period.noteEn}
        </p>

        {/* drsnik let */}
        <div
          role="radiogroup"
          aria-label={t("Letnica rekonstrukcije", "Reconstruction year")}
          className="mx-auto flex max-w-lg items-stretch gap-1 rounded-full border border-white/25 bg-black/50 p-1 backdrop-blur"
        >
          {yearButtons.map(([y, si, en]) => (
            <button
              key={y}
              type="button"
              role="radio"
              aria-checked={year === y}
              onClick={() => {
                setYear(y);
                setCard(null);
              }}
              className={`flex-1 rounded-full px-3 py-2 text-sm font-semibold transition ${
                year === y
                  ? "bg-primary text-primary-foreground"
                  : "text-white/85 hover:bg-white/10"
              }`}
            >
              {t(si, en)}
            </button>
          ))}
        </div>

        {/* zajem + obvestilo */}
        <div className="flex items-center justify-center gap-4">
          <button
            type="button"
            onClick={capture}
            disabled={camera === "starting"}
            aria-label={t("Posni in shrani trenutek", "Capture and save the moment")}
            className="relative flex size-16 items-center justify-center rounded-full border-[3px] border-white bg-white/10 backdrop-blur transition hover:bg-white/20 active:scale-95 disabled:opacity-40"
          >
            <span className="size-11 rounded-full bg-white" aria-hidden="true" />
          </button>
          {saved !== "none" && (
            <p className="text-xs font-medium text-white" role="status">
              {saved === "saved" && (
                <span className="flex items-center gap-1.5">
                  <Download className="size-3.5" aria-hidden="true" />
                  {t("shranjeno (PNG)", "saved (PNG)")}
                </span>
              )}
              {saved === "shared" && (
                <span className="flex items-center gap-1.5">
                  <Share2 className="size-3.5" aria-hidden="true" />
                  {t("deljeno", "shared")}
                </span>
              )}
              {saved === "error" && t("zajem ni uspel", "capture failed")}
            </p>
          )}
        </div>

        {camera === "unavailable" && (
          <p className="text-center text-[11px] leading-relaxed text-white/60">
            {t(
              "Kamera ni na voljo — rekonstrukcija stoji na temni kulisi; zajem deluje vseeno.",
              "Camera unavailable — the reconstruction stands on a dark backdrop; capture still works.",
            )}
          </p>
        )}
        {heading == null && !iosCompassBlocked && (
          <p className="text-center text-[11px] text-white/60">
            {t(
              "Kompas ni na voljo — vlecite po zaslonu za obrat pogleda.",
              "Compass unavailable — drag the screen to look around.",
            )}
          </p>
        )}
      </div>
    </div>
  );
}
