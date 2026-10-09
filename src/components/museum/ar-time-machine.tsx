"use client";

/**
 * AR ČASOVNI STROJ (issue #10, razširjen #11 — TIME SPOTS) — 3D rekonstrukcija
 * vasi Griblje skozi čas.
 *
 * Zaslon telefona = okno v leto 1825 (ali ~1900 / danes):
 *  · zadaj živa kamera (getUserMedia), spredaj proceduralna 3D vas iz
 *    Franciscejskega katastra (156 stavb) zasidrana na GPS + kompas;
 *  · drsnik let: 1825 · ~1900 (ocena) · danes (duhovi);
 *  · zajem: gumb sprožilc → PNG s podpisom (prenos/deljenje);
 *  · tap na hišo → kartica stavbe s hišno zgodbo (register × matrike)
 *    in evidence čipom (REKONSTRUIRANO / OCENA + vir);
 *  · AR TIME SPOTS (issue #11): ko obiskovalec stopi znotraj radija točke,
 *    se ta odklene (TimeLens vzorec) in pokaže kartico »kaj je tu nekoč
 *    stalo« z viri; brez senzorjev se točko izbere ročno (pošten predogled);
 *  · KAJ JE IZGINILO? (issue #12): v letu »danes« so duhovi 1825 obarvani
 *    po usodi (🟢 obstaja · 🟡 negotovo · 🔴 ni je več — 1825 ∩ OSM posnetek);
 *  · 360° S CERKVE (issue #12): fiksno stališče pri cerkvi sv. Vida — obrat
 *    pogleda na žiroskopu/kompasu (ali vlečenju), preklapljanje 1825 ⇄ danes
 *    = pogovor preteklost ↔ sedanjost (Nîmes Tour Magne vzorec);
 *  · HISTORICAL PANORAMA (issue #13, P2): hero TimeSpoti (cerkev, jedro,
 *    kolpa) odprejo »Doživi 360°« — imerziven equirect prizor, ki ga obrača
 *    kompas/žiroskop (magic window, ne WebXR); proceduralna 3D vas ostane
 *    kot pošteno označen fallback; »primerjaj z danes« = živa kamera (danes
 *    je realnost, ne generirana slika); zajem/TTS/viri se ponovno uporabijo;
 *  · GLAS (P15): kartica točke se prebere naglas — deterministične govorne
 *    skripte (narrations.ts) prek skupnega narratorja in brskalnikove
 *    speechSynthesis (zastonj, lokalno, brez AI modelov); med predvajanjem
 *    se pokaže transkript skripte;
 *  · brez senzorjev: pošten predogled (vlečenje obrača pogled).
 *
 * Kot pri ar-camera: nič se ne izmišljuje — kar manjka (kamera, kompas, GPS),
 * komponenta to pove in ponudi alternativo.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  CheckCircle2,
  Clock,
  Compass,
  Crosshair,
  Download,
  Home,
  Lock,
  MapPin,
  Pause,
  RotateCw,
  Share2,
  Sparkles,
  Volume2,
  X,
} from "lucide-react";
import { useLang } from "./language-context";
import { useTimeMachine, type TimeYear } from "@/lib/time-machine-store";
import {
  PERIODS,
  toLocal,
  ORIGIN,
  inVillageCore,
  CHURCH,
  IZGINILO_STATS,
  BUILDING_NEAREST_PRESENT,
  PRESENCE_META,
  HOUSENO_FINDING,
  type BuildingPresence,
} from "@/lib/village3d";
import {
  angleDelta,
  bearingDeg,
  distanceM,
  formatDistance,
  type GeoFix,
} from "@/lib/geo";
import type { UseGeolocation } from "@/hooks/use-geolocation";
import { useCompass } from "@/hooks/use-compass";
import { useCompassCal } from "@/lib/compass-cal";
import {
  GPS_QUALITY_LABEL,
  sceneReadiness,
  type CompassStability,
} from "@/data/atlas/geotruth";
import type { PickResult } from "./village-scene";
import { HOUSE_VITALS } from "@/data/atlas/parish";
import {
  TIME_SPOTS,
  findNearestSpot,
  getSpotById,
  spotYearParam,
  isDistantSpot,
  spotDistanceFromVillage,
  type TimeSpot,
} from "@/data/atlas/timespots";
import { useTimespots } from "@/lib/timespots-store";
import { narrationText } from "@/data/atlas/narrations";
import { speakScript, stopNarration } from "@/lib/narrator";
import {
  getPanoramaForSpot,
  spotHasPanorama,
  type HistoricalPanorama,
} from "@/data/atlas/panoramas";
import { PanoramaViewer, type PanoramaScene } from "./panorama-viewer";

interface BuildingCard {
  kind: "1825" | "growth" | "present";
  w: number;
  d: number;
  dist: number;
  nearChurch: boolean;
  core: boolean;
  /** status stavbe 1825 (leto »danes« — Kaj je izginilo?) */
  presence?: BuildingPresence;
  /** razdalja do najbližje današnje stavbe (m) */
  nearestPresent?: number | null;
}

/** 360° stališče: vzpon pri cerkvi sv. Vida (virtualni pogled +6 m) */
const CHURCH_RISE = 6;

const COMPASS_LABEL: Record<CompassStability, { si: string; en: string }> = {
  unavailable: { si: "kompas ni na voljo", en: "compass unavailable" },
  unstable: { si: "poravnava kompasa …", en: "compass aligning …" },
  settling: { si: "kompas se umirja", en: "compass settling" },
  stable: { si: "kompas stabilen", en: "compass stable" },
};

const PRESENCE_CHIP: Record<
  BuildingPresence,
  { si: string; en: string; cls: string }
> = {
  exists: {
    si: "🟢 OBSTOJA",
    en: "🟢 STILL STANDS",
    cls: "border-emerald-300/40 bg-emerald-400/15 text-emerald-200",
  },
  uncertain: {
    si: "🟡 NEGOTOVO",
    en: "🟡 UNCERTAIN",
    cls: "border-amber-300/40 bg-amber-400/15 text-amber-200",
  },
  gone: {
    si: "🔴 NI JE VEČ",
    en: "🔴 GONE",
    cls: "border-red-300/40 bg-red-400/15 text-red-200",
  },
};

export function ARTimeMachine({
  geo,
  onOpenExhibit,
}: {
  geo: UseGeolocation;
  onOpenExhibit: (slug: string) => void;
}) {
  const { t, lang } = useLang();
  const {
    year,
    setYear,
    close,
    spot: storeSpot,
    p360,
    setP360,
    pano: storePano,
    setPano,
  } = useTimeMachine();
  const { unlock, isUnlocked, unlocked } = useTimespots();
  const { fix, status, start, quality } = geo;

  /* kompas (issue #14): glajen + zavrnitev odstopnikov + stabilnost + kalibracija */
  const {
    heading,
    rawHeading,
    stability: compassStability,
    needsPermission: iosCompassBlocked,
    requestPermission: enableCompass,
  } = useCompass();
  const cal = useCompassCal();

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const sceneRef = useRef<import("./village-scene").VillageScene | null>(null);
  const yearRef = useRef(year);

  const [camera, setCamera] = useState<"starting" | "live" | "unavailable">("starting");
  const [card, setCard] = useState<BuildingCard | null>(null);
  const [hint, setHint] = useState(true);
  const [flash, setFlash] = useState(false);
  const [saved, setSaved] = useState<"none" | "saved" | "shared" | "error">("none");
  const [spotCard, setSpotCard] = useState<TimeSpot | null>(null);
  const [spotJustUnlocked, setSpotJustUnlocked] = useState<TimeSpot | null>(null);
  const autoSpotRef = useRef<string | null>(null);

  /* mini-scena oddaljene točke (issue #12): mlini/cerkvišče — lastna
     proceduralna vsebina namesto praznega pogleda na vas 2–10 km stran */
  const [mini, setMini] = useState<"mlini" | "cerkvisce" | null>(null);
  const miniRef = useRef<"mlini" | "cerkvisce" | null>(null);
  miniRef.current = mini;
  const miniSpot = mini
    ? (TIME_SPOTS.find((s) => s.miniScene === mini) ?? null)
    : null;

  /* ── HISTORICAL PANORAMA (issue #13, P2): imerzivna plast ──
     aktivna panorama (null = proceduralna 3D vas), njena scena, blend z
     danes (živa kamera) in razprte evidence trditve */
  const [pano, setPanoState] = useState<HistoricalPanorama | null>(null);
  const panoRef = useRef<HistoricalPanorama | null>(null);
  panoRef.current = pano;
  const panoSceneRef = useRef<PanoramaScene | null>(null);
  const [todayBlend, setTodayBlend] = useState(false);
  const [panoClaimsOpen, setPanoClaimsOpen] = useState(false);
  const panoSpot = pano
    ? (TIME_SPOTS.find((s) => s.id === pano.timeSpotId) ?? null)
    : null;

  /* vstop v 360° zgodovinski pogled — 3D vas se skrije (GPU miruje),
     karta točke se zapre, p360/mini se ugasneta (samo ena plast naenkrat) */
  const enterPano = useCallback(
    (spot: TimeSpot) => {
      const p = getPanoramaForSpot(spot.id);
      if (!p) return;
      setPanoState(p);
      setTodayBlend(false);
      setPanoClaimsOpen(false);
      setP360(false);
      setMini(null);
      setCard(null);
      setSpotCard(null);
      setHint(false);
      sceneRef.current?.setHidden(true);
    },
    [setP360],
  );

  const exitPano = useCallback(() => {
    setPanoState(null);
    setTodayBlend(false);
    setPanoClaimsOpen(false);
    setPano(false);
    sceneRef.current?.setHidden(false);
  }, [setPano]);

  /* globa povezava ?spot=<id>&pano=1 → direktno v 360° pogled (QR/ mapa) */
  const panoFlagRef = useRef(storePano);
  panoFlagRef.current = storePano;
  useEffect(() => {
    const sp = getSpotById(storeSpot);
    if (sp) {
      if (panoFlagRef.current) {
        enterPano(sp);
      } else {
        setSpotCard(sp);
        setMini(sp.miniScene ?? null);
        setHint(false);
      }
    }
  }, [storeSpot, enterPano]);

  /* kalibracija kompasa (issue #14, točka 7) — prostovoljna, enkrat na napravo */
  const [showCal, setShowCal] = useState(false);
  const calOfferedRef = useRef(false);

  /* diagnostika (issue #14, točka 15): samo ?debug=ar ali localhost */
  const [debug] = useState(() => {
    if (typeof window === "undefined") return false;
    const p = new URLSearchParams(window.location.search).get("debug");
    return p === "ar" || window.location.hostname === "localhost";
  });
  const [debugOpen, setDebugOpen] = useState(false);

  /* GLAS (P15): govorna skripta točke prek determinističnega narratorja */
  const [playing, setPlaying] = useState(false);

  const period = PERIODS.find((p) => p.year === year) ?? PERIODS[0];

  /* ── mini-scena → prizor (issue #12) ── */
  useEffect(() => {
    const sc = sceneRef.current;
    if (!sc) return;
    const sp = mini ? TIME_SPOTS.find((s) => s.miniScene === mini) : null;
    sc.setMiniScene(mini, sp ? { lat: sp.lat, lng: sp.lng } : null);
  }, [mini]);

  /* ── ponudba kalibracije ob prvem AR odpiranju (issue #14, točka 7) ──
     Prikazemo jo enkrat: kompas deluje, kalibracija še ni bila narejena niti
     preskočena, GPS ima opravek (brez njega cilja ne moremo izračunati). */
  useEffect(() => {
    if (calOfferedRef.current) return;
    if (heading == null || cal.offsetDeg != null || cal.dismissed) return;
    if (!fix) return;
    calOfferedRef.current = true;
    setShowCal(true);
    setHint(false);
  }, [heading, fix, cal.offsetDeg, cal.dismissed]);

  /* cilj kalibracije: najbližja točka, ki je vsaj 10 m stran (azimut na
     lastnem stališču nima pomena — na bližini nič možno meriti) */
  const calTarget = fix
    ? (() => {
        const sorted = TIME_SPOTS.map((s) => ({ s, d: distanceM(fix, s) })).sort(
          (a, b) => a.d - b.d,
        );
        const far = sorted.find((x) => x.d >= 10);
        return far ? { spot: far.s, dist: far.d } : null;
      })()
    : null;

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
            nearChurch: Math.hypot(p.x - CHURCH.x, p.z - CHURCH.z) < 80,
            core: inVillageCore(p.x, p.z),
            presence: p.presence,
            nearestPresent:
              p.kind === "1825" && p.index != null
                ? BUILDING_NEAREST_PRESENT[p.index]
                : undefined,
          });
          setHint(false);
        },
      });
      scene.setYear(yearRef.current);
      /* začetno sidro: 360° stališče pri cerkvi ali GPS (ali predogled) */
      if (useTimeMachine.getState().p360) {
        scene.setFix(CHURCH.x, CHURCH.z, CHURCH_RISE);
      } else if (fixRef.current) {
        const { x, z } = toLocal(fixRef.current.lat, fixRef.current.lng);
        scene.setFix(x, z);
      }
      /* mini-scena iz globo povezave (?spot=mlini) lahko čaka, odkar se
         prizor ustvari — uporabi miniRef (izven odvisnosti učinka) */
      if (miniRef.current) {
        const sp = TIME_SPOTS.find((s) => s.miniScene === miniRef.current);
        scene.setMiniScene(
          miniRef.current,
          sp ? { lat: sp.lat, lng: sp.lng } : null,
        );
      }
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

  /* kompas: glajen heading iz use-compass → prizor (issue #14: brez sunkov);
     v 360° panorami isti heading obrača magic-window pogled */
  useEffect(() => {
    sceneRef.current?.setCompassYaw(heading);
    panoSceneRef.current?.setCompassYaw(heading);
  }, [heading]);

  /* primerjaj z danes (issue #13): sfera → duh, živa kamera → danes */
  useEffect(() => {
    panoSceneRef.current?.setTodayBlend(todayBlend && camera === "live");
  }, [todayBlend, camera]);

  /* ── preklop letnice → prizor ── */
  useEffect(() => {
    yearRef.current = year;
    sceneRef.current?.setYear(year);
    setCard(null);
  }, [year]);

  /* ── GPS / 360° → sidro prizora ── */
  const fixRef = useRef(fix);
  fixRef.current = fix;
  useEffect(() => {
    const sc = sceneRef.current;
    if (!sc) return;
    if (p360) {
      /* 360°: fiksno stališče pri cerkvi sv. Vida (virtualni vzpon +6 m) */
      sc.setFix(CHURCH.x, CHURCH.z, CHURCH_RISE);
    } else if (fix) {
      const { x, z } = toLocal(fix.lat, fix.lng);
      sc.setFix(x, z);
    } else {
      sc.setFix(null, null);
    }
  }, [fix, p360]);

  /* ── GPS → bližina TIME SPOTA: odklep ob prihodu (TimeLens vzorec) ── */
  useEffect(() => {
    if (!fix) return;
    const { spot, dist } = findNearestSpot(fix);
    if (dist > spot.radius) {
      if (autoSpotRef.current === spot.id) autoSpotRef.current = null;
      return;
    }
    if (autoSpotRef.current === spot.id) return;
    autoSpotRef.current = spot.id;
    setSpotCard(spot);
    setMini(spot.miniScene ?? null);
    setHint(false);
    if (!isUnlocked(spot.id)) {
      unlock(spot.id);
      setSpotJustUnlocked(spot);
      window.setTimeout(() => setSpotJustUnlocked(null), 3600);
    }
  }, [fix, unlock, isUnlocked]);

  /* ── ESC ── */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && close();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [close]);

  /* ── potrditev kalibracije (issue #14, točka 7): odmik = azimut do cilja − heading ── */
  const confirmCalibration = useCallback(() => {
    if (!fix || !calTarget || rawHeading == null) return;
    const targetBearing = bearingDeg(fix, {
      lat: calTarget.spot.lat,
      lng: calTarget.spot.lng,
    });
    const offset = angleDelta(rawHeading, targetBearing);
    cal.setCalibration(offset, calTarget.spot.titleSi);
    setShowCal(false);
  }, [fix, calTarget, rawHeading, cal]);

  const skipCalibration = useCallback(() => {
    cal.dismiss();
    setShowCal(false);
  }, [cal]);

  /* ── GLAS (P15): poslušaj zgodbo točke ──
     Deterministična govorna skripta (narrations.ts) prek skupnega
     narratorja (src/lib/narrator.ts) — brskalnikova speechSynthesis:
     zastonj, lokalno, brez AI modelov in brez omrežnih klicev. */
  const stopAudio = useCallback(() => {
    stopNarration();
    setPlaying(false);
  }, []);

  const toggleSpotAudio = useCallback(
    (spot: TimeSpot) => {
      if (playing) {
        stopAudio();
        return;
      }
      stopAudio();
      const started = speakScript(narrationText(spot, lang), lang, () =>
        setPlaying(false),
      );
      setPlaying(started);
    },
    [lang, playing, stopAudio],
  );

  /* konec predvajanja ob zaprtju / zamenjavi kartice */
  useEffect(() => stopAudio, [stopAudio]);
  useEffect(() => {
    if (!spotCard) stopAudio();
  }, [spotCard, stopAudio]);

  /* razdalja uporabnika od jedra vasi (predogled/na lokaciji) —
     v mini sceni (issue #12) referenčna točka = točka scene same */
  const refLat = miniSpot ? miniSpot.lat : ORIGIN.lat;
  const refLng = miniSpot ? miniSpot.lng : ORIGIN.lng;
  const coreDistance =
    fix && fix.lat != null && fix.lng != null
      ? distanceM(fix, { lat: refLat, lng: refLng })
      : null;
  const onSite = miniSpot
    ? coreDistance != null && coreDistance <= miniSpot.radius
    : coreDistance != null && coreDistance <= 1500;

  /* pripravljenost scene (issue #14, točki 11–12): GPS kakovost × kompas */
  const readiness = sceneReadiness({ gps: quality, compass: compassStability });
  const nearest = fix ? findNearestSpot(fix) : null;

  /* ── deljenje/prenos PNG (skupno 3D/mini/panorama zajemu) ── */
  const setSaveError = useCallback(() => {
    setSaved("error");
    window.setTimeout(() => setSaved("none"), 2600);
  }, []);

  const shareOrDownload = useCallback(
    async (data: string, fname: string, title: string) => {
      /* najprej deljenje (telefon), sicer prenos */
      try {
        const blob = await (await fetch(data)).blob();
        const file = new File([blob], fname, { type: "image/png" });
        const nav = navigator as Navigator & {
          canShare?: (d: { files: File[] }) => boolean;
        };
        if (nav.share && nav.canShare?.({ files: [file] })) {
          await nav.share({ files: [file], title });
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
    },
    [],
  );

  /* ── zajem fotografije (3D vas, mini-scena ALI 360° panorama — isti
     deljivi PNG sistem, druga napisnica) ── */
  const capture = useCallback(async () => {
    setFlash(true);
    window.setTimeout(() => setFlash(false), 260);

    /* 360° zgodovinski pogled (issue #13): zajem gledišča panorame */
    const p = panoRef.current;
    const ps = panoSceneRef.current;
    if (p && ps) {
      const yy = p.year === 2026 ? "danes" : p.year === 1900 ? "~1900" : "1825";
      const data = ps.capture(videoRef.current, {
        title: `${p.titleSi} — ${yy}${todayBlend ? t(" (danes skozi 1825)", " (today through 1825)") : ""}`,
        sub: t(
          "Muzej vasi Griblje · 360° zgodovinski pogled · INTERPRETACIJA na dokumentiranih legah",
          "Museum of Griblje village · 360° historical view · INTERPRETATION on documented positions",
        ),
        credit: `griblje-museum.vercel.app · ${p.id} · ${p.status}`,
      });
      if (data) await shareOrDownload(data, `griblje-${p.id}.png`, `Griblje ${yy}`);
      else setSaveError();
      return;
    }

    const sc = sceneRef.current;
    if (!sc) return;
    const y = year === 2026 ? "danes" : year === 1900 ? "~1900" : "1825";
    const data = sc.capture(videoRef.current, {
      title: miniSpot
        ? `${miniSpot.titleSi} — ${y}${mini === "mlini" && year === 2026 ? " (duh)" : ""}`
        : year === 2026
          ? t(`Griblje ${y} — kaj je izginilo?`, `Griblje ${y} — what has vanished?`)
          : t(`Griblje ${y} — rekonstrukcija vasi`, `Griblje ${y} — village reconstruction`),
      sub: miniSpot
        ? t(
            "Muzej vasi Griblje · proceduralna mini-scena (issue #12) · interpretacija, ne kataster",
            "Museum of Griblje village · procedural mini-scene (issue #12) · interpretation, not cadastre",
          )
        : t(
            "Muzej vasi Griblje · 3D rekonstrukcija iz Franciscejskega katastra (list A02, SI AS 176)",
            "Museum of Griblje village · 3D reconstruction from the Franciscean cadastre (sheet A02, SI AS 176)",
          ),
      credit: miniSpot
        ? `griblje-museum.vercel.app · ${miniSpot.id.toUpperCase()} · INTERPRETACIJA`
        : year === 2026
          ? t(
              `griblje-museum.vercel.app · 1825 ∩ OSM ${IZGINILO_STATS.osmSnapshot}`,
              `griblje-museum.vercel.app · 1825 ∩ OSM ${IZGINILO_STATS.osmSnapshot}`,
            )
          : "griblje-museum.vercel.app · RECONSTRUCTED",
    });
    if (!data) {
      setSaved("error");
      window.setTimeout(() => setSaved("none"), 2600);
      return;
    }
    const fname = miniSpot ? `griblje-${miniSpot.id}.png` : `griblje-${year === 2026 ? "danes" : year}.png`;
    await shareOrDownload(data, fname, `Griblje ${y}`);
  }, [year, t, miniSpot, mini, todayBlend]);

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

      {/* 3D vas čez kamero — skrita, ko je aktivna 360° panorama (GPU miruje) */}
      <canvas
        ref={canvasRef}
        aria-label={t(
          "3D rekonstrukcija vasi — vlecite za obrat pogleda, tapnite hišo",
          "3D village reconstruction — drag to look around, tap a house",
        )}
        className={`absolute inset-0 h-full w-full touch-none ${
          pano ? "invisible" : ""
        }`}
      />

      {/* HISTORICAL PANORAMA (issue #13): imerzivni 360° zgodovinski pogled —
          magic window na kompas/žiroskop, vlečenje kot fallback, lazy nalaganje
          (predogled → polna slika), sfera se zna prelije v duha nad kamero */}
      {pano && (
        <PanoramaViewer
          pano={pano}
          heading={heading}
          onExit={exitPano}
          sceneRef={panoSceneRef}
        />
      )}

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
            {pano
              ? t("360° zgodovinski pogled — Griblje", "360° historical view — Griblje")
              : t("Časovni stroj — Griblje", "Time machine — Griblje")}
          </p>
          <p className="truncate text-[11px] text-white/70">
            {pano
              ? t("Obrni telefon in poglej okoli sebe", "Turn your phone and look around")
              : t("3D rekonstrukcija vasi skozi čas", "3D village reconstruction through time")}
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
                {miniSpot
                  ? t(
                      `na lokaciji — ${lang === "si" ? miniSpot.titleSi : miniSpot.titleEn}`,
                      `on site — ${lang === "si" ? miniSpot.titleSi : miniSpot.titleEn}`,
                    )
                  : t(
                      `na lokaciji vasi${coreDistance != null ? ` — ${formatDistance(coreDistance, lang)} do jedra` : ""}`,
                      `on village site${coreDistance != null ? ` — ${formatDistance(coreDistance, lang)} to the core` : ""}`,
                    )}
              </span>
            </>
          ) : coreDistance != null ? (
            <>
              <MapPin className="size-3.5 shrink-0 text-amber-200" aria-hidden="true" />
              <span>
                {miniSpot
                  ? t(
                      `mini scena — predogled, ${formatDistance(coreDistance, lang)} do točke`,
                      `mini scene — preview, ${formatDistance(coreDistance, lang)} to the spot`,
                    )
                  : t(
                      `predogled — ${formatDistance(coreDistance, lang)} od vasi`,
                      `preview — ${formatDistance(coreDistance, lang)} from the village`,
                    )}
              </span>
            </>
          ) : (
            <>
              <MapPin className="size-3.5 shrink-0 text-white/80" aria-hidden="true" />
              <span>
                {miniSpot
                  ? t("mini scena — predogled (GPS ni priključen)", "mini scene — preview (GPS not connected)")
                  : status === "watching"
                    ? t("čakam na GPS …", "waiting for GPS …")
                    : t("predogled — GPS ni priključen", "preview — GPS not connected")}
              </span>
            </>
          )}
        </div>
        {/* period chip: skrit v 360° panorami (panorama ima svoje leto) */}
        {!pano && (
          <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white backdrop-blur">
            <Clock className="size-3.5 shrink-0 text-white/80" aria-hidden="true" />
            <span>
              {period.labelSi} ·{" "}
              {period.buildingCount}{" "}
              {t("stavb", "buildings")}
            </span>
          </div>
        )}
        {/* 360° panorama: chip statusa vizualizacije (issue #13) */}
        {pano && (
          <div
            className="inline-flex items-center gap-2 rounded-full border border-amber-300/40 bg-amber-400/15 px-3 py-1.5 text-xs font-semibold text-amber-100 backdrop-blur"
            role="status"
          >
            <Sparkles className="size-3.5 shrink-0" aria-hidden="true" />
            {pano.status} · {t("vizualizacija na dokumentiranih legah", "visualisation on documented positions")}
          </div>
        )}
        {/* sidro scene (issue #14, točka 11): HIGH = poravnana, MEDIUM = poravnava …, LOW = približno */}
        <div
          className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs backdrop-blur ${
            readiness.anchor === "HIGH"
              ? "border-emerald-300/40 bg-emerald-400/15 text-emerald-100"
              : readiness.anchor === "MEDIUM"
                ? "border-amber-300/40 bg-amber-400/15 text-amber-100"
                : "border-white/20 bg-black/45 text-white/80"
          }`}
          role="status"
        >
          {readiness.anchor === "HIGH" ? (
            <Crosshair className="size-3.5 shrink-0" aria-hidden="true" />
          ) : (
            <Compass
              className={`size-3.5 shrink-0 ${readiness.anchor === "MEDIUM" ? "animate-pulse" : ""}`}
              aria-hidden="true"
            />
          )}
          <span className="font-medium">
            {readiness.anchor === "HIGH"
              ? t("SCENA PORAVNANA", "SCENE ALIGNED")
              : readiness.anchor === "MEDIUM"
                ? t("Poravnava scene …", "Scene aligning …")
                : t("približno — raziskovanje", "approximate — exploring")}
          </span>
        </div>
        {/* kompas/GPS kakovost (issue #14, točki 8–9) — le ko je podatka */}
        {compassStability !== "unavailable" && compassStability !== "stable" && (
          <div
            className="inline-flex animate-pulse items-center gap-2 rounded-full border border-amber-300/40 bg-amber-400/15 px-3 py-1.5 text-xs text-amber-100 backdrop-blur"
            role="status"
          >
            <Compass className="size-3.5 shrink-0" aria-hidden="true" />
            <span>{t(COMPASS_LABEL[compassStability].si, COMPASS_LABEL[compassStability].en)}</span>
          </div>
        )}
        {fix?.accuracy != null && (
          <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white/80 backdrop-blur">
            <MapPin className="size-3.5 shrink-0" aria-hidden="true" />
            <span>
              {t(`GPS ±${Math.round(fix.accuracy)} m`, `GPS ±${Math.round(fix.accuracy)} m`)} ·{" "}
              {t(GPS_QUALITY_LABEL[quality].si, GPS_QUALITY_LABEL[quality].en)}
            </span>
          </div>
        )}
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
        {/* 360° s cerkve (issue #12): fiksno stališče, žiroskop/kompas obrača pogled
            (v mini sceni in 360° panorami skrito — ena plast naenkrat) */}
        {!mini && !pano && (
          <button
            type="button"
            onClick={() => {
              setP360(!p360);
              setHint(false);
            }}
            aria-pressed={p360}
            className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium backdrop-blur transition-colors ${
              p360
                ? "border-primary bg-primary text-primary-foreground"
                : "border-white/25 bg-black/45 text-white hover:bg-black/60"
            }`}
          >
            <RotateCw className="size-3.5" aria-hidden="true" />
            {t("360° s cerkve", "360° from the church")}
          </button>
        )}
      </div>

      {/* ── KAJ JE IZGINILO? legenda (leto »danes«, issue #12; v mini sceni
          ima duhov lasten pomen — cerkvišče/mlin; v panorami svoj pomen ni) ── */}
      {year === 2026 && !mini && !pano && (
        <div
          className="relative z-10 mt-2 flex flex-wrap items-center gap-2 px-4"
          role="group"
          aria-label={t("Kaj je izginilo — legenda statusov", "What has vanished — status legend")}
        >
          <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-white/25 bg-black/45 px-3 py-1.5 text-xs font-semibold text-white backdrop-blur">
            {t("Kaj je izginilo?", "What has vanished?")}
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white/90 backdrop-blur">
            🟢 {t("obstaja", "stands")} · {IZGINILO_STATS.exists}
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white/90 backdrop-blur">
            🟡 {t("negotovo", "uncertain")} · {IZGINILO_STATS.uncertain}
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-xs text-white/90 backdrop-blur">
            🔴 {t("ni je več", "gone")} · {IZGINILO_STATS.gone}
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-[11px] text-white/70 backdrop-blur">
            {t(
              `OSM posnetek ${IZGINILO_STATS.osmSnapshot} · od ${IZGINILO_STATS.total1825} stavb 1825`,
              `OSM snapshot ${IZGINILO_STATS.osmSnapshot} · of ${IZGINILO_STATS.total1825} buildings of 1825`,
            )}
          </span>
        </div>
      )}

      {/* ── 360° PANORAMA (issue #13): poudarjena plošča z naslovom, letnico
          in navodilom (TimeLens UX — uporabnik ve, da gleda zgodovinski
          trenutek, ne 3D maketo) ── */}
      {pano && (
        <div
          className="relative z-10 mx-auto mt-3 max-w-md rounded-xl border border-primary/50 bg-black/60 p-3 text-center backdrop-blur"
          role="region"
          aria-label={t("360° zgodovinski pogled", "360° historical view")}
        >
          <p className="font-display text-sm font-bold tracking-wide text-white">
            {t("360° ZGODOVINSKI POGLED", "360° HISTORICAL VIEW")}
          </p>
          <p className="mt-0.5 text-xs font-semibold text-amber-200">
            {pano.titleSi}
          </p>
          <p className="mt-1 text-[11px] leading-relaxed text-white/75">
            {compassStability === "unavailable" && !iosCompassBlocked
              ? t(
                  "Kompas ni na voljo — vlecite po zaslonu za obrat pogleda.",
                  "Compass unavailable — drag the screen to look around.",
                )
              : t(
                  "Obrni telefon in poglej okoli sebe — pogled sledi kompasu.",
                  "Turn your phone and look around — the view follows the compass.",
                )}
          </p>
        </div>
      )}

      {/* ── AR TIME SPOTS: izbirnik točk (odklop GPS → ročna izbira, pošteno) —
          vaške točke + oddaljene (issue #12) z lastno vsebino; v 360° panorami
          samo izhod na 3D rekonstrukcijo (enoben fokus) ── */}
      {pano ? (
        <div className="relative z-10 mt-2 flex items-center gap-2 overflow-x-auto px-4 pb-1">
          <button
            type="button"
            onClick={exitPano}
            className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-primary/60 bg-primary/20 px-3 py-1.5 text-xs font-semibold text-white backdrop-blur transition-colors hover:bg-primary/30"
          >
            <Home className="size-3.5 shrink-0" aria-hidden="true" />
            {t("← nazaj na 3D rekonstrukcijo", "← back to the 3D reconstruction")}
          </button>
          {heading == null && (
            <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-white/20 bg-black/45 px-3 py-1.5 text-[11px] text-white/70 backdrop-blur">
              {t("brez kompasa — vlečenje", "no compass — dragging")}
            </span>
          )}
        </div>
      ) : (
      <div
        className="relative z-10 mt-2 flex items-center gap-2 overflow-x-auto px-4 pb-1"
        role="group"
        aria-label={t("Časovne točke po vasi in okolici", "Time spots around the village and its surroundings")}
      >
        <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-white/25 bg-black/45 px-3 py-1.5 text-xs font-semibold text-white backdrop-blur">
          <Clock className="size-3.5 shrink-0" aria-hidden="true" />
          {t(`točke ${unlocked.length}/${TIME_SPOTS.length}`, `spots ${unlocked.length}/${TIME_SPOTS.length}`)}
        </span>
        {/* nazaj na vas, ko je aktivna mini scena (issue #12) */}
        {mini && (
          <button
            type="button"
            onClick={() => {
              setMini(null);
              setSpotCard(null);
              setP360(false);
            }}
            className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-primary/60 bg-primary/20 px-3 py-1.5 text-xs font-semibold text-white backdrop-blur transition-colors hover:bg-primary/30"
          >
            <Home className="size-3.5 shrink-0" aria-hidden="true" />
            {t("← nazaj na vas", "← back to the village")}
          </button>
        )}
        {TIME_SPOTS.filter((s) => !isDistantSpot(s)).map((s) => (
          <button
            key={s.id}
            type="button"
            onClick={() => {
              setSpotCard(s);
              setMini(null);
              setCard(null);
              setHint(false);
            }}
            aria-pressed={spotCard?.id === s.id}
            className={`inline-flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs backdrop-blur transition-colors ${
              spotCard?.id === s.id
                ? "border-primary bg-primary text-primary-foreground"
                : "border-white/25 bg-black/45 text-white/90 hover:bg-black/60"
            }`}
          >
            {isUnlocked(s.id) ? (
              <CheckCircle2 className="size-3.5 shrink-0" aria-hidden="true" />
            ) : (
              <Lock className="size-3.5 shrink-0 text-white/60" aria-hidden="true" />
            )}
            <span className="font-semibold">{spotYearParam(s.year)}</span>
            <span className="max-w-32 truncate">
              {lang === "si" ? s.titleSi : s.titleEn}
            </span>
          </button>
        ))}
        {/* oddaljene točke (issue #12) — ločena skupina z razdaljo od vasi */}
        <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-primary/40 bg-primary/10 px-2.5 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-amber-200 backdrop-blur">
          {t("oddaljene", "distant")}
        </span>
        {TIME_SPOTS.filter((s) => isDistantSpot(s)).map((s) => (
          <button
            key={s.id}
            type="button"
            onClick={() => {
              setSpotCard(s);
              setMini(s.miniScene ?? null);
              setP360(false);
              setCard(null);
              setHint(false);
            }}
            aria-pressed={spotCard?.id === s.id}
            className={`inline-flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs backdrop-blur transition-colors ${
              spotCard?.id === s.id
                ? "border-primary bg-primary text-primary-foreground"
                : "border-white/25 bg-black/45 text-white/90 hover:bg-black/60"
            }`}
          >
            {isUnlocked(s.id) ? (
              <CheckCircle2 className="size-3.5 shrink-0" aria-hidden="true" />
            ) : (
              <Lock className="size-3.5 shrink-0 text-white/60" aria-hidden="true" />
            )}
            <span className="font-semibold">{spotYearParam(s.year)}</span>
            <span className="max-w-32 truncate">
              {lang === "si" ? s.titleSi : s.titleEn}
            </span>
            <span
              className={spotCard?.id === s.id ? "text-primary-foreground/80" : "text-white/50"}
            >
              · {formatDistance(spotDistanceFromVillage(s), lang)}
            </span>
          </button>
        ))}
      </div>
      )}

      {/* KALIBRACIJA POGLEDA (issue #14, točka 7) — enkrat na napravo, prostovoljna */}
      {showCal && calTarget && (
        <div className="absolute inset-x-4 bottom-44 z-20 sm:left-1/2 sm:right-auto sm:w-[440px] sm:-translate-x-1/2">
          <div
            className="rounded-xl border border-amber-300/40 bg-black/75 p-4 text-white backdrop-blur"
            role="region"
            aria-label={t("Kalibracija pogleda", "View calibration")}
          >
            <p className="flex items-center gap-2 font-display text-sm font-semibold">
              <Crosshair className="size-4 text-amber-200" aria-hidden="true" />
              {t("KALIBRACIJA POGLEDA", "VIEW CALIBRATION")}
            </p>
            <ol className="mt-2 list-decimal space-y-1 pl-5 text-xs leading-relaxed text-white/85">
              <li>
                {t(
                  `Obrni telefon proti: ${calTarget.spot.titleSi}.`,
                  `Point your phone at: ${calTarget.spot.titleEn}.`,
                )}
              </li>
              <li>
                {t(
                  `Počakaj na stabilen kompas (${
                    compassStability === "stable" ? "✓" : "…"
                  }).`,
                  `Wait for a stable compass (${
                    compassStability === "stable" ? "✓" : "…"
                  }).`,
                )}
              </li>
              <li>{t("Potrdi — scena se zamakne v pravo smer.", "Confirm — the scene shifts to the right direction.")}</li>
            </ol>
            <div className="mt-3 flex items-center gap-2">
              <button
                type="button"
                onClick={confirmCalibration}
                disabled={compassStability !== "stable"}
                className="inline-flex items-center gap-1.5 rounded-full border border-amber-300/50 bg-amber-400/20 px-3 py-1.5 text-xs font-semibold text-amber-100 transition-colors hover:bg-amber-400/30 disabled:opacity-40"
              >
                <CheckCircle2 className="size-3.5" aria-hidden="true" />
                {t("Potrdi smer", "Confirm direction")}
              </button>
              <button
                type="button"
                onClick={skipCalibration}
                className="rounded-full border border-white/25 px-3 py-1.5 text-xs text-white/70 transition-colors hover:bg-white/10"
              >
                {t("preskoči", "skip")}
              </button>
              <span className="ml-auto text-[10px] text-white/50">
                {t("shranjeno samo na tej napravi", "stored on this device only")}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* AR DEBUG (issue #14, točka 15) — samo ?debug=ar / localhost, privzeto skrito.
          Na majhnih zaslonih zložljiv, da ne pokriva statusnih čipov. */}
      {debug && (
        <div className="absolute left-2 top-24 z-30" role="status" aria-label="AR debug">
          <button
            type="button"
            onClick={() => setDebugOpen((o) => !o)}
            className="rounded-md border border-emerald-300/40 bg-black/80 px-2 py-1 font-mono text-[10px] font-bold tracking-widest text-emerald-300 backdrop-blur"
          >
            AR DEBUG {debugOpen ? "▾" : "▸"}
          </button>
          {debugOpen && (
          <div
            className="mt-1 max-w-[240px] rounded-lg border border-emerald-300/30 bg-black/80 p-2.5 font-mono text-[10px] leading-relaxed text-emerald-200 backdrop-blur"
          >
          <p>lat: {fix ? fix.lat.toFixed(5) : "—"}</p>
          <p>lng: {fix ? fix.lng.toFixed(5) : "—"}</p>
          <p>acc: {fix?.accuracy != null ? `±${Math.round(fix.accuracy)} m` : "—"}</p>
          <p>gps: {quality}</p>
          <p>heading: {heading != null ? `${Math.round(heading)}°` : "—"}</p>
          <p>
            raw: {rawHeading != null ? `${Math.round(rawHeading)}°` : "—"} · off:{" "}
            {cal.offsetDeg != null ? `${Math.round(cal.offsetDeg)}°` : "—"}
          </p>
          <p>kompas: {compassStability}</p>
          <p>
            spot: {nearest ? `${nearest.spot.id} @ ${Math.round(nearest.dist)} m` : "—"}
          </p>
          <p>
            sidro: {readiness.anchor} · scena: {readiness.sceneStatus}
          </p>
          <p>asset: {sceneRef.current ? "3D pripravljen" : "nalaga …"}</p>
          {cal.calibratedAt != null && (
            <button
              type="button"
              onClick={cal.reset}
              className="mt-1 rounded border border-emerald-300/40 px-1.5 py-0.5 text-[9px] hover:bg-emerald-300/10"
            >
              reset kalibracije
            </button>
          )}
          </div>
          )}
        </div>
      )}

      {/* prvi namig */}
      {hint && !spotCard && !p360 && !pano && (
        <div className="relative z-10 mx-auto mt-8 max-w-sm rounded-xl border border-white/20 bg-black/50 p-4 text-center backdrop-blur">
          <p className="text-sm leading-relaxed text-white/90">
            {t(
              "Usmerite telefon — vas 1825 stoji pred vami. Vlecite po zaslonu za obrat pogleda, tapnite hišo za njeno zgodbo. Časovne točke po vasi izberete na čipih — na lokaciji se odklenejo same.",
              "Point your phone — the village of 1825 stands before you. Drag the screen to look around, tap a house for its story. Pick time spots on the chips — on site they unlock by themselves.",
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

      {/* 360° način: poudarjena plošča z navodilom (issue #12) */}
      {p360 && !pano && (
        <div className="relative z-10 mx-auto mt-4 max-w-md rounded-xl border border-primary/40 bg-black/55 p-3 text-center backdrop-blur">
          <p className="text-sm font-semibold text-white">
            <RotateCw className="mr-1.5 inline size-4" aria-hidden="true" />
            {t("360° s cerkve sv. Vida", "360° from St. Vitus' church")}
          </p>
          <p className="mt-1 text-xs leading-relaxed text-white/80">
            {t(
              "Obrni se okoli sebe (ali vleci po zaslonu) in preklapljaj leta — ista točka, dva svetova: 1825 ⇄ danes. Virtualno stališče: vzpon pri cerkvi, +6 m.",
              "Turn around yourself (or drag the screen) and switch years — one spot, two worlds: 1825 ⇄ today. Virtual viewpoint: the rise by the church, +6 m.",
            )}
          </p>
          <button
            type="button"
            onClick={() => setP360(false)}
            className="mt-2 text-xs font-medium text-amber-200 underline underline-offset-2 hover:text-amber-100"
          >
            {t("nazaj na svoj GPS", "back to my own GPS")}
          </button>
        </div>
      )}

      {/* ── VIRI 360° PANORAME (issue #13, §10): Himera plast — vsaka
          vizualna trditev ima status + vir; uporabnik vidi, kaj je
          DOKUMENTIRANO in kesa je INTERPRETACIJA/TO_COLLECT ── */}
      {pano && panoClaimsOpen && (
        <div className="absolute inset-x-4 bottom-44 z-20 sm:left-1/2 sm:right-auto sm:w-[440px] sm:-translate-x-1/2">
          <div
            className="max-h-[46vh] overflow-y-auto rounded-xl border border-white/20 bg-black/75 p-4 text-white backdrop-blur"
            role="region"
            aria-label={t("Viri panorame — evidence trditve", "Panorama sources — evidence claims")}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="flex items-center gap-2 font-display text-sm font-semibold">
                  <Sparkles className="size-4 text-amber-200" aria-hidden="true" />
                  {t("Kaj je dokazano v tem prizoru?", "What is evidenced in this scene?")}
                </p>
                <p className="mt-1 text-[11px] text-white/60">
                  {lang === "si" ? pano.evidenceSi : pano.evidenceEn}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setPanoClaimsOpen(false)}
                aria-label={t("Zapri vire", "Close sources")}
                className="shrink-0 rounded-full border border-white/25 p-1.5 hover:bg-white/10"
              >
                <X className="size-4" aria-hidden="true" />
              </button>
            </div>
            <ul className="mt-3 space-y-2.5">
              {pano.claims.map((c, i) => (
                <li key={i} className="text-[11px] leading-relaxed">
                  <p className="flex flex-wrap items-center gap-1.5">
                    <span
                      className={`inline-flex shrink-0 items-center gap-1 rounded-full border px-2 py-0.5 font-semibold ${
                        c.status === "DOCUMENTED"
                          ? "border-emerald-300/40 bg-emerald-400/15 text-emerald-200"
                          : c.status === "RECONSTRUCTED"
                            ? "border-sky-300/40 bg-sky-400/15 text-sky-200"
                            : c.status === "ESTIMATE"
                              ? "border-amber-300/40 bg-amber-400/15 text-amber-200"
                              : c.status === "TO_COLLECT"
                                ? "border-white/25 bg-white/10 text-white/70"
                                : "border-amber-300/40 bg-amber-400/15 text-amber-200"
                      }`}
                    >
                      {c.status}
                    </span>
                    <span className="font-medium text-white/90">
                      {lang === "si" ? c.whatSi : c.whatEn}
                    </span>
                  </p>
                  <p className="mt-0.5 pl-1 text-white/60">
                    {lang === "si" ? c.sourceSi : c.sourceEn}
                  </p>
                </li>
              ))}
            </ul>
            <p className="mt-3 border-t border-white/15 pt-2 text-[11px] leading-relaxed text-white/70">
              {t(
                "Izjava o poštenosti: visual realism ≠ historical certainty — lepa slika ni bolj resnična samo zato, ker izgleda realistično.",
                "Honesty statement: visual realism ≠ historical certainty — a beautiful image is not more true just because it looks realistic.",
              )}
            </p>
          </div>
        </div>
      )}

      {/* kartica AR TIME SPOTA (odklep / izbira / globa povezava) —
          omejena višina z notranjim drsenjem, da ne prekrije čipov točk */}
      {spotCard && !pano && (
        <div className="absolute inset-x-4 bottom-44 z-20 sm:left-1/2 sm:right-auto sm:w-[440px] sm:-translate-x-1/2">
          <div
            className="max-h-[46vh] overflow-y-auto rounded-xl border border-white/20 bg-black/70 p-4 text-white backdrop-blur"
            role="region"
            aria-label={t("Kartica časovne točke", "Time spot card")}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="flex flex-wrap items-center gap-2">
                  <span className="inline-flex items-center rounded-full bg-primary px-2.5 py-1 text-xs font-bold text-primary-foreground">
                    🕰 {spotYearParam(spotCard.year)}
                  </span>
                  <span className="font-display text-sm font-semibold">
                    {lang === "si" ? spotCard.titleSi : spotCard.titleEn}
                  </span>
                  {spotJustUnlocked?.id === spotCard.id ? (
                    <span className="inline-flex animate-pulse items-center gap-1 rounded-full border border-emerald-300/40 bg-emerald-400/20 px-2 py-0.5 text-[11px] font-semibold text-emerald-200">
                      <Sparkles className="size-3" aria-hidden="true" />
                      {t("pravkar odklenjeno!", "just unlocked!")}
                    </span>
                  ) : isUnlocked(spotCard.id) ? (
                    <span className="inline-flex items-center gap-1 rounded-full border border-emerald-300/30 bg-emerald-400/10 px-2 py-0.5 text-[11px] font-medium text-emerald-200">
                      <CheckCircle2 className="size-3" aria-hidden="true" />
                      {t("odklenjeno", "unlocked")}
                    </span>
                  ) : fix ? (
                    <span className="inline-flex items-center gap-1 rounded-full border border-white/25 bg-white/10 px-2 py-0.5 text-[11px] font-medium text-white/80">
                      <Lock className="size-3" aria-hidden="true" />
                      {t(
                        `odklenjeno bo na lokaciji (${formatDistance(
                          distanceM(fix, { lat: spotCard.lat, lng: spotCard.lng }),
                          lang,
                        )} od vas)`,
                        `unlocks on site (${formatDistance(
                          distanceM(fix, { lat: spotCard.lat, lng: spotCard.lng }),
                          lang,
                        )} from you)`,
                      )}
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 rounded-full border border-white/25 bg-white/10 px-2 py-0.5 text-[11px] font-medium text-white/80">
                      <Lock className="size-3" aria-hidden="true" />
                      {t("odklenjeno bo na lokaciji", "unlocks on site")}
                    </span>
                  )}
                </p>
                <p className="mt-2 text-xs leading-relaxed text-white/85">
                  {lang === "si" ? spotCard.descSi : spotCard.descEn}
                </p>
                {/* dogodki (issue #12 — Otok story-only): mini časovnica na kartici */}
                {spotCard.events && (
                  <ol className="mt-2.5 space-y-1.5 border-l border-amber-300/40 pl-3">
                    {spotCard.events.map((ev, i) => (
                      <li key={i} className="text-[11px] leading-relaxed">
                        <span className="font-semibold text-amber-200">
                          {lang === "si" ? ev.whenSi : ev.whenEn}
                        </span>{" "}
                        <span className="text-white/80">
                          {lang === "si" ? ev.textSi : ev.textEn}
                        </span>
                      </li>
                    ))}
                  </ol>
                )}
                {/* dinamični radij (issue #14, točka 10): odklep ≠ natančna poravnava */}
                {fix && isUnlocked(spotCard.id) && (() => {
                  const d = distanceM(fix, { lat: spotCard.lat, lng: spotCard.lng });
                  const rr = spotCard.renderReadyM ?? 25;
                  return d > rr ? (
                    <p className="mt-1.5 flex items-center gap-1.5 text-[11px] text-amber-200">
                      <Crosshair className="size-3 shrink-0" aria-hidden="true" />
                      {t(
                        `portal odklenjen — približaj se na ${rr} m za natančno poravnavo scene`,
                        `portal unlocked — come within ${rr} m for precise scene alignment`,
                      )}
                    </p>
                  ) : null;
                })()}
              </div>
              <button
                type="button"
                onClick={() => setSpotCard(null)}
                aria-label={t("Zapri kartico točke", "Close the spot card")}
                className="shrink-0 rounded-full border border-white/25 p-1.5 hover:bg-white/10"
              >
                <X className="size-4" aria-hidden="true" />
              </button>
            </div>

            <p className="mt-2 text-[11px] leading-relaxed text-white/60">
              {t("Vir: ", "Source: ")}
              {lang === "si" ? spotCard.evidenceSi : spotCard.evidenceEn}
            </p>

            {/* DOŽIVI 360° (issue #13): hero TimeSpot odpre Historical Panorama —
                imerzivni prizor na kompasu; jasno ločeno od 3D rekonstrukcije */}
            {spotHasPanorama(spotCard.id) && (
              <button
                type="button"
                onClick={() => enterPano(spotCard)}
                className={`mt-2.5 inline-flex items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-xs font-semibold transition-colors ${
                  pano
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-primary/60 bg-primary/25 text-white hover:bg-primary/35"
                }`}
              >
                <Sparkles className="size-3.5" aria-hidden="true" />
                {t("DOŽIVI 360° — zgodovinski pogled", "EXPERIENCE 360° — historical view")}
              </button>
            )}

            {/* GLAS (P15): poslušaj zgodbo točke — govorna skripta + transkript */}
            <button
              type="button"
              onClick={() => toggleSpotAudio(spotCard)}
              className={`mt-2.5 inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium transition-colors ${
                playing
                  ? "border-primary/60 bg-primary/20 text-white"
                  : "border-white/25 bg-white/10 text-white/90 hover:bg-white/20"
              }`}
              aria-pressed={playing}
            >
              {playing ? (
                <>
                  <Pause className="size-3.5" aria-hidden="true" />
                  {t("Ustavi pripoved", "Stop narration")}
                </>
              ) : (
                <>
                  <Volume2 className="size-3.5" aria-hidden="true" />
                  {t("Poslušaj — pripoved", "Listen — narration")}
                </>
              )}
            </button>

            {/* transkript skripte — viden med predvajanjem (dostopnost) */}
            {playing && (
              <div
                className="mt-2.5 max-h-44 overflow-y-auto rounded-lg border border-white/20 bg-black/40 p-3 text-xs leading-relaxed text-white/85"
                aria-live="polite"
              >
                <p className="mb-1.5 font-mono text-[10px] font-semibold uppercase tracking-wider text-amber-200">
                  {t("Govorna skripta", "Narration script")}
                </p>
                <p className="whitespace-pre-line">
                  {narrationText(spotCard, lang)}
                </p>
              </div>
            )}

            <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 border-t border-white/15 pt-2 text-xs">
              <button
                type="button"
                onClick={() => {
                  close();
                  onOpenExhibit(spotCard.exhibitSlug);
                }}
                className="font-medium text-amber-200 underline decoration-white/30 underline-offset-2 hover:decoration-amber-200"
              >
                {t("Zapis zbirke (MVG)", "Collection record (MVG)")}
              </button>
              {spotCard.houseNo && (
                <a
                  href={`/?atlas=hi%C5%A1a-61&odsek=atlas`}
                  className="font-medium text-amber-200 underline decoration-white/30 underline-offset-2 hover:decoration-amber-200"
                >
                  {t("Register hiš 1825", "1825 house register")}
                </a>
              )}
              <button
                type="button"
                onClick={() => setYear(spotCard.year)}
                className="font-medium text-amber-200 underline decoration-white/30 underline-offset-2 hover:decoration-amber-200"
              >
                {t(
                  `postavi leto na ${spotYearParam(spotCard.year)}`,
                  `set year to ${spotYearParam(spotCard.year)}`,
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* kartica stavbe (tap) — enaka omejitev višine */}
      {card && !spotCard && (
        <div className="absolute inset-x-4 bottom-44 z-20 sm:left-1/2 sm:right-auto sm:w-[440px] sm:-translate-x-1/2">
          <div className="max-h-[46vh] overflow-y-auto rounded-xl border border-white/20 bg-black/70 p-4 text-white backdrop-blur">
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
                {/* evidence čip po stavbi (TimeLens/Himera: domneve nikoli kot dejstva) */}
                <p className="mt-1.5 flex flex-wrap items-center gap-2 text-[11px]">
                  {card.kind === "present" ? (
                    <>
                      <span className="inline-flex items-center gap-1.5 rounded-full border border-sky-300/40 bg-sky-400/15 px-2 py-0.5 font-semibold text-sky-200">
                        <span className="size-1.5 rounded-full bg-sky-300" aria-hidden="true" />
                        {t("DOKUMENTIRANO · OSM", "DOCUMENTED · OSM")}
                      </span>
                      <span className="text-white/70">
                        {lang === "si" ? PRESENCE_META.sourceSi : PRESENCE_META.sourceEn}
                      </span>
                    </>
                  ) : card.kind === "growth" ? (
                    <>
                      <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-300/40 bg-amber-400/15 px-2 py-0.5 font-semibold text-amber-200">
                        <span className="size-1.5 rounded-full bg-amber-300" aria-hidden="true" />
                        OCENA
                      </span>
                      <span className="text-white/70">
                        {t(
                          "ocena zgoščevanja jedra ~1900 — ni v katastru 1825",
                          "core-densification estimate ~1900 — not in the 1825 cadastre",
                        )}
                      </span>
                    </>
                  ) : year === 2026 && card.presence ? (
                    <>
                      <span
                        className={`inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 font-semibold ${
                          PRESENCE_CHIP[card.presence].cls
                        }`}
                      >
                        {lang === "si"
                          ? PRESENCE_CHIP[card.presence].si
                          : PRESENCE_CHIP[card.presence].en}
                      </span>
                      <span className="text-white/70">
                        {card.presence === "gone"
                          ? t(
                              `najbližja današnja stavba: ${
                                card.nearestPresent != null
                                  ? formatDistance(card.nearestPresent, lang)
                                  : t("več kot 1 km", "more than 1 km")
                              } · viri: kataster 1825 (A02) + OSM posnetek ${IZGINILO_STATS.osmSnapshot} — terenska preverba čaka`,
                              `nearest present-day building: ${
                                card.nearestPresent != null
                                  ? formatDistance(card.nearestPresent, lang)
                                  : t("more than 1 km", "more than 1 km")
                              } · sources: 1825 cadastre (A02) + OSM snapshot ${IZGINILO_STATS.osmSnapshot} — field check pending`,
                            )
                          : card.presence === "uncertain"
                            ? t(
                                `današnja stavba v ${
                                  card.nearestPresent != null
                                    ? formatDistance(card.nearestPresent, lang)
                                    : ""
                                } — morda ista domačija · viri: kataster 1825 (A02) + OSM`,
                                `a present-day building within ${
                                  card.nearestPresent != null
                                    ? formatDistance(card.nearestPresent, lang)
                                    : ""
                                } — perhaps the same farmstead · sources: 1825 cadastre (A02) + OSM`,
                              )
                            : t(
                                "današnja stavba stoji na tlorisu 1825 · viri: kataster 1825 (A02) + OSM",
                                "a present-day building stands on the 1825 footprint · sources: 1825 cadastre (A02) + OSM",
                              )}
                      </span>
                    </>
                  ) : (
                    <>
                      <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-300/40 bg-emerald-400/15 px-2 py-0.5 font-semibold text-emerald-200">
                        <span className="size-1.5 rounded-full bg-emerald-300" aria-hidden="true" />
                        REKONSTRUIRANO
                      </span>
                      <span className="text-white/70">
                        {t(
                          "Vir: franciscejski kataster, list A02 (SI AS 176) · tloris izmerjen, višina interpretirana",
                          "Source: Franciscean cadastre, sheet A02 (SI AS 176) · footprint measured, height interpreted",
                        )}
                      </span>
                    </>
                  )}
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
              {card.kind === "present" ? (
                <p>
                  {t(
                    "Siva masa = digitalni dvojček današnjih stavb vasi (samo v 3D pregledu). Višine niso zabeležene v OSM — prikazane so ocena. V AR se današnje vidi skozi kamero, duhovi 1825 pa povedo, kje je kaj stalo.",
                    "The grey mass = digital twin of today's village buildings (3D viewer only). Heights are not recorded in OSM — shown as an estimate. In AR the present shows through the camera, while the ghosts of 1825 mark what stood where.",
                  )}
                </p>
              ) : card.kind === "growth" ? (
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
                        `Kdo je tu živel? ${HOUSENO_FINDING.si}`,
                        `Who lived here? ${HOUSENO_FINDING.en}`,
                      )}
                    </span>
                  </p>
                  {year === 2026 && (
                    <p className="text-white/75">
                      {t(
                        `Kaj je izginilo: iz ${IZGINILO_STATS.total1825} stavb 1825 jih današnji posnetek pozna le ${IZGINILO_STATS.exists} · ${IZGINILO_STATS.uncertain} negotovih · ${IZGINILO_STATS.gone} jih ni več. Zaselki na zahodu so jih pogoltnili gozdovi.`,
                        `What has vanished: of the ${IZGINILO_STATS.total1825} buildings of 1825, today's snapshot knows only ${IZGINILO_STATS.exists} · ${IZGINILO_STATS.uncertain} uncertain · ${IZGINILO_STATS.gone} are gone. The western hamlets were swallowed by forests.`,
                      )}
                    </p>
                  )}
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

      {/* spodnja plošča: 360° panorama kontrole (issue #13) ALI časovni drsnik + zajem */}
      <div className="relative z-10 mt-auto space-y-3 p-4 pb-[max(1rem,env(safe-area-inset-bottom))]">
        {pano ? (
          <>
            {/* metodologija panorame — poštena opomba TimeLens pipeline */}
            <p className="mx-auto max-w-lg text-center text-[11px] leading-relaxed text-white/70">
              {lang === "si" ? pano.methodSi : pano.methodEn}
            </p>

            {/* 360° kontrole: Poslušaj · Viri · Primerjaj z danes · poravnava (issue #13, §14) */}
            <div
              className="mx-auto flex max-w-lg flex-wrap items-center justify-center gap-2"
              role="group"
              aria-label={t("Kontrole 360° pogleda", "360° view controls")}
            >
              <button
                type="button"
                onClick={() => panoSpot && void toggleSpotAudio(panoSpot)}
                className={`inline-flex items-center gap-1.5 rounded-full border px-3.5 py-2 text-xs font-semibold backdrop-blur transition-colors ${
                  playing
                    ? "border-primary/60 bg-primary/25 text-white"
                    : "border-white/25 bg-black/50 text-white/90 hover:bg-black/70"
                }`}
                aria-pressed={playing}
              >
                {playing ? (
                  <Pause className="size-3.5" aria-hidden="true" />
                ) : (
                  <Volume2 className="size-3.5" aria-hidden="true" />
                )}
                {playing
                  ? t("Ustavi pripoved", "Stop narration")
                  : t("Poslušaj", "Listen")}
              </button>
              <button
                type="button"
                onClick={() => setPanoClaimsOpen((o) => !o)}
                aria-pressed={panoClaimsOpen}
                className={`inline-flex items-center gap-1.5 rounded-full border px-3.5 py-2 text-xs font-semibold backdrop-blur transition-colors ${
                  panoClaimsOpen
                    ? "border-primary/60 bg-primary/25 text-white"
                    : "border-white/25 bg-black/50 text-white/90 hover:bg-black/70"
                }`}
              >
                <Sparkles className="size-3.5" aria-hidden="true" />
                {t("Viri — kaj je dokazano", "Sources — what is evidenced")}
              </button>
              {camera === "live" ? (
                <button
                  type="button"
                  onClick={() => setTodayBlend((b) => !b)}
                  aria-pressed={todayBlend}
                  className={`inline-flex items-center gap-1.5 rounded-full border px-3.5 py-2 text-xs font-semibold backdrop-blur transition-colors ${
                    todayBlend
                      ? "border-primary bg-primary text-primary-foreground"
                      : "border-white/25 bg-black/50 text-white/90 hover:bg-black/70"
                  }`}
                >
                  <RotateCw className="size-3.5" aria-hidden="true" />
                  {todayBlend
                    ? t("danes — živa kamera · 1825 kot duh", "today — live camera · 1825 as a ghost")
                    : t("Primerjaj z danes", "Compare with today")}
                </button>
              ) : (
                <span
                  className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-black/40 px-3.5 py-2 text-[11px] text-white/60 backdrop-blur"
                  title={t("Kamera ni na voljo — primerjava z danes potrebuje živo kamero", "Camera unavailable — comparing with today needs the live camera")}
                >
                  <MapPin className="size-3.5" aria-hidden="true" />
                  {t("danes: kamera ni na voljo", "today: camera unavailable")}
                </span>
              )}
              <button
                type="button"
                onClick={() => panoSceneRef.current?.realign()}
                className="inline-flex items-center gap-1.5 rounded-full border border-white/25 bg-black/50 px-3.5 py-2 text-xs font-semibold text-white/90 backdrop-blur transition-colors hover:bg-black/70"
              >
                <Crosshair className="size-3.5" aria-hidden="true" />
                {t("Poravnaj pogled", "Realign view")}
              </button>
            </div>
          </>
        ) : (
        <>
        {/* metodologija leta — v mini sceni (issue #12) lastna poštena opomba */}
        {mini ? (
          <p className="mx-auto max-w-lg text-center text-[11px] leading-relaxed text-white/70">
            {mini === "mlini"
              ? t(
                  "Mini scena mlina je PROCEDURALNA INTERPRETACIJA vrste (žimaln — vodoravno kolo znotraj, vidno kolo je ikonografska) · ni rekonstrukcija konkretnega mlina · v letu »danes« mlin postane duh",
                  "The mill mini scene is a PROCEDURAL INTERPRETATION of the type (žimaln — a horizontal wheel inside, the visible wheel is iconographic) · not a reconstruction of a particular mill · in the “today” year the mill becomes a ghost",
                )
              : t(
                  "Postavitev treh cerkvic je INTERPRETACIJA (za dve domnevno znani legi, tretja neznana) · kapelica 1994 stoji na dokumentirani lokaciji · viri: MVG-040",
                  "The three churches' placement is an INTERPRETATION (two positions believed known, the third unknown) · the 1994 chapel stands at its documented position · sources: MVG-040",
                )}
          </p>
        ) : (
          <p className="mx-auto max-w-lg text-center text-[11px] leading-relaxed text-white/70">
            {lang === "si" ? period.noteSi : period.noteEn}
          </p>
        )}

        {/* drsnik let (skrit v 360° panorami — panorama JE svoje leto) */}
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
        </>
        )}

        {/* zajem + obvestilo (skupno: 3D, mini scena in 360° panorama) */}
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
        {compassStability === "unavailable" && !iosCompassBlocked && (
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
