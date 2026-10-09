"use client";

/**
 * MUSEUM VISITOR EXPERIENCE v1 (issue #15) — obiskovniški sloj ČEZ
 * obstoječo AR infrastrukturo (ne čez njo, ne namesto nje).
 *
 * Pot obiskovalca:
 *   prihod → dobrodošlica → voden ogled → raziskovanje → zbiranje
 *   odkritij → zaključek obiska → deljenje spomina.
 *
 * Arhitektura (NIČ novega ni podvojeno):
 *  · odkritja          → obstoječi collection sistem useTimespots (#11);
 *  · postaje           → obstoječi TIME_SPOTS (vrstni red iz issue #15);
 *  · odpiranje AR      → obstoječi useTimeMachine.openTM (#10–#13);
 *  · razdalje/status   → obstoječi geo helperji + GeoTrust GPS quality (#14);
 *  · navigacija        → obstoječi OSM directions link;
 *  · Q&A (AI priprava) → podatkovni sloj GUIDE_QA (#15, točka 9).
 *
 * Stanje okvira obiska (start/oseba/zaključek/spomin) je v
 * visitor-store (localStorage) — zbirka odkritij ostaja v timespots-store.
 */

import { useEffect, useMemo, useState, useSyncExternalStore } from "react";
import { motion } from "framer-motion";
import {
  Award,
  CheckCircle2,
  ChevronUp,
  Clock,
  Compass,
  Download,
  Footprints,
  Gift,
  GraduationCap,
  HelpCircle,
  Hourglass,
  Languages,
  MapPin,
  Microscope,
  Navigation,
  RotateCcw,
  Share2,
  Ticket,
  Users,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { useLang } from "./language-context";
import {
  TIME_SPOTS,
  getSpotById,
  spotYearParam,
  isDistantSpot,
  type TimeSpot,
} from "@/data/atlas/timespots";
import { useTimespots } from "@/lib/timespots-store";
import { useTimeMachine } from "@/lib/time-machine-store";
import {
  useVisitor,
  personaStations,
  personaTime,
  type VisitorPersona,
} from "@/lib/visitor-store";
import { GUIDE_QA, GUIDE_TOTAL, getGuideForSpot, type GuideStatus } from "@/data/atlas/guide";
import { PANORAMAS } from "@/data/atlas/panoramas";
import { distanceM, formatDistance, osmDirectionsUrl, type GeoFix } from "@/lib/geo";
import { GPS_QUALITY_LABEL, type GpsQuality } from "@/data/atlas/geotruth";

/* 156 = VECTOR_BUILDINGS.length (src/data/atlas/buildings.json — list A02) */
const BUILDINGS_1825_COUNT = 156;
const TOTAL_SPOTS = TIME_SPOTS.length; /* 9 */
const PANORAMA_COUNT = PANORAMAS.length; /* 3 */

const GUIDE_STATUS_STYLE: Record<GuideStatus, string> = {
  VERIFIED: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
  DOCUMENTED: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100",
  RECONSTRUCTED: "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100",
  INTERPRETATION: "bg-orange-100 text-orange-900 dark:bg-orange-900/60 dark:text-orange-100",
};

const PERSONA_META: Record<
  VisitorPersona,
  { icon: typeof Users; si: string; en: string; descSi: string; descEn: string }
> = {
  druzina: {
    icon: Users,
    si: "Družina",
    en: "Family",
    descSi: "Krajša in bolj igriva pot — 3 postaje.",
    descEn: "A shorter, more playful route — 3 stations.",
  },
  sola: {
    icon: GraduationCap,
    si: "Šola",
    en: "School",
    descSi: "Učenje + vprašanja muzejskega vodnika.",
    descEn: "Learning + museum-guide questions.",
  },
  turist: {
    icon: Languages,
    si: "Turist",
    en: "Tourist",
    descSi: "Več jezikov, manj predznanja.",
    descEn: "More languages, less prior knowledge.",
  },
  raziskovalec: {
    icon: Microscope,
    si: "Raziskovalec",
    en: "Researcher",
    descSi: "Vseh 9 točk + viri in evidence.",
    descEn: "All 9 spots + sources and evidence.",
  },
};

interface VisitorGeo {
  fix: GeoFix | null;
  quality: GpsQuality;
  start: () => void;
}

/* hydration-varen »mounted« (vzorec language-context): false na strežniku,
   true na odjemalcu — brez setState v efektu */
const emptySubscribe = () => () => {};

function useMounted(): boolean {
  return useSyncExternalStore(
    emptySubscribe,
    () => true,
    () => false,
  );
}

/* ?obisk=1 (vstopna tablica) — prisilna dobrodošlica; prebere se iz
   URL ob vsakem izrisu, odpri/skrij pa počisti parameter */
function useObiskParam(): boolean {
  return useSyncExternalStore(
    emptySubscribe,
    () => new URLSearchParams(window.location.search).get("obisk") === "1",
    () => false,
  );
}

function clearObiskParam() {
  try {
    const url = new URL(window.location.href);
    if (url.searchParams.has("obisk")) {
      url.searchParams.delete("obisk");
      window.history.replaceState(null, "", url);
    }
  } catch {
    /* ignore */
  }
}

/* ════════════════════════════════════════════════════════════════════
   GLAVNA KOMPONENTA — vrata, odsek, dok
   ════════════════════════════════════════════════════════════════ */

export function VisitorExperience({ geo }: { geo: VisitorGeo }) {
  const { t } = useLang();
  const mounted = useMounted();
  const forceStart = useObiskParam();

  const started = useVisitor((s) => s.started);
  const startDismissed = useVisitor((s) => s.startDismissed);

  /* vhodni parametri: QR na lokaciji (?casovni&spot) samodejno začne
     obisk (brez blokade — AR se odpre direktno, kot doslej).
     ?obisk=1 (vstopna tablica muzeja) beremo zgoraj (useObiskParam). */
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const spotParam = params.get("spot");
    const yearParam = params.get("casovni");
    if (spotParam && yearParam && !useVisitor.getState().started) {
      useVisitor.getState().startVisit(null);
    }
  }, []);

  const showStart = mounted && !started && (!startDismissed || forceStart);

  return (
    <>
      {showStart && <VisitorStart geo={geo} forced={forceStart} />}
      {mounted && started && <VisitSection geo={geo} />}
      {mounted && <VisitDock geo={geo} />}
      <span className="sr-only">{t("Muzejski obisk", "Museum visit")}</span>
    </>
  );
}

/* ════════════════════════════════════════════════════════════════════
   1. DOBRODOŠLICA — prvi zaslon obiskovalca (deluje iz QR kode)
   ════════════════════════════════════════════════════════════════ */

function VisitorStart({ geo, forced }: { geo: VisitorGeo; forced: boolean }) {
  const { t, lang } = useLang();
  const startVisit = useVisitor((s) => s.startVisit);
  const dismissStart = useVisitor((s) => s.dismissStart);
  const [persona, setPersona] = useState<VisitorPersona | null>(null);

  const time = personaTime(persona);

  const begin = () => {
    clearObiskParam();
    startVisit(persona);
  };

  return (
    <div
      role="dialog"
      aria-modal="false"
      aria-label={t("Dobrodošli v Muzeju Griblje", "Welcome to the Griblje Museum")}
      className="fixed inset-0 z-40 flex items-end justify-center overflow-y-auto bg-background/95 p-4 backdrop-blur-sm sm:items-center"
    >
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        className="my-auto w-full max-w-lg"
      >
        <div className="rounded-2xl border bg-card shadow-xl">
          {/* glava */}
          <div className="rounded-t-2xl bg-primary px-6 py-6 text-primary-foreground">
            <p className="text-xs font-semibold uppercase tracking-widest opacity-90">
              {forced
                ? t("Vstopna točka muzeja", "Museum entrance")
                : t("Digitalni muzej vasi ob Kolpi", "A digital village museum on the Kolpa")}
            </p>
            <h2 className="mt-1.5 font-display text-3xl font-semibold leading-tight">
              {t("Dobrodošli v Muzej Griblje", "Welcome to the Griblje Museum")}
            </h2>
            <p className="mt-2 text-sm leading-relaxed opacity-95">
              {t(
                "Odkrivajte vas, kot je izgledala leta 1825 — na pravih lokacijah, skozi telefon.",
                "Discover the village as it looked in 1825 — on the real locations, through your phone.",
              )}
            </p>
          </div>

          <div className="px-6 py-5">
            {/* čaka vas */}
            <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {t("Čaka vas", "Awaiting you")}
            </p>
            <ul className="mt-2 space-y-1.5 text-sm">
              <li className="flex items-center gap-2">
                <span aria-hidden>⛪</span>
                {t("Cerkev sv. Vida — 500-letnica", "St. Vitus' church — 500th anniversary")}
              </li>
              <li className="flex items-center gap-2">
                <span aria-hidden>🏘</span>
                {t("Zgodovinska vas — 156 stavb 1825", "Historic village — 156 buildings of 1825")}
              </li>
              <li className="flex items-center gap-2">
                <span aria-hidden>🌊</span>
                {t("Življenje ob Kolpi", "Life on the Kolpa")}
              </li>
            </ul>

            {/* osebe (issue #15, točka 8) */}
            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {t("Kdo ste? (lahko preskočite)", "Who are you? (skippable)")}
            </p>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {(Object.keys(PERSONA_META) as VisitorPersona[]).map((p) => {
                const m = PERSONA_META[p];
                const active = persona === p;
                return (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPersona(active ? null : p)}
                    aria-pressed={active}
                    className={`flex items-start gap-2 rounded-lg border p-2.5 text-left transition ${
                      active
                        ? "border-primary bg-primary/10"
                        : "border-border hover:border-primary/40 hover:bg-accent"
                    }`}
                  >
                    <m.icon className="mt-0.5 size-4 shrink-0 text-primary" aria-hidden />
                    <span className="min-w-0">
                      <span className="block text-xs font-semibold">
                        {lang === "si" ? m.si : m.en}
                      </span>
                      <span className="block text-[11px] leading-snug text-muted-foreground">
                        {lang === "si" ? m.descSi : m.descEn}
                      </span>
                    </span>
                  </button>
                );
              })}
            </div>

            {/* AR onboarding — 3 koraki (issue #15, točka 6) */}
            <ArOnboarding geo={geo} />

            <p className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
              <Clock className="size-3.5 shrink-0" aria-hidden />
              {t("Predviden čas", "Estimated time")}:{" "}
              <strong className="font-semibold text-foreground">
                {lang === "si" ? time.si : time.en}
              </strong>
              {persona === null && (
                <span>· {t("6 postaj po vasi", "6 stations around the village")}</span>
              )}
            </p>

            {/* akcije */}
            <div className="mt-5 flex flex-col gap-2 sm:flex-row">
              <Button
                type="button"
                size="lg"
                onClick={begin}
                className="h-12 flex-1 text-base"
              >
                <Footprints className="size-5" aria-hidden />
                {t("Začni raziskovanje", "Start exploring")}
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="lg"
                onClick={() => {
                  clearObiskParam();
                  dismissStart();
                }}
                className="h-12"
              >
                {t("Brskaj brez ogleda", "Browse without the tour")}
              </Button>
            </div>
            <p className="mt-3 text-center text-[11px] leading-relaxed text-muted-foreground">
              {t(
                "Brez namestitve, brez računa. Odkrivanja se shranijo v vaš brskalnik.",
                "No install, no account. Your discoveries are saved in your browser.",
              )}
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   6. AR ONBOARDING — zakaj GPS, kako držati telefon, kompas
      (povezan z obstoječim GeoTruth GPS quality)
   ════════════════════════════════════════════════════════════════ */

function ArOnboarding({ geo }: { geo: VisitorGeo }) {
  const { t, lang } = useLang();
  const quality = GPS_QUALITY_LABEL[geo.quality];

  return (
    <div className="mt-5 rounded-lg border border-primary/30 bg-primary/5 p-3.5">
      <p className="flex items-center gap-2 text-xs font-semibold text-primary">
        <Compass className="size-4" aria-hidden />
        {t("Za najboljši AR (3 koraki)", "For the best AR (3 steps)")}
      </p>
      <ol className="mt-2 space-y-1.5 text-[13px] leading-snug text-foreground/90">
        <li className="flex gap-2">
          <span className="font-mono font-semibold text-primary">1.</span>
          {t("Dovoli lokacijo", "Allow location")} —{" "}
          <span className="text-muted-foreground">
            {lang === "si" ? quality.si : quality.en}
          </span>
        </li>
        <li className="flex gap-2">
          <span className="font-mono font-semibold text-primary">2.</span>
          {t("Obrni telefon počasi", "Turn your phone slowly")}
        </li>
        <li className="flex gap-2">
          <span className="font-mono font-semibold text-primary">3.</span>
          {t("Počakaj na poravnavo scene", "Wait for the scene to align")}
        </li>
      </ol>
      <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
        {t(
          "Scena se poravna iz GPS + kompasa (GeoTruth); kompas se umiri, ko telefon nekajkrat počasi obrnete v krog.",
          "The scene aligns from GPS + compass (GeoTruth); the compass settles as you slowly turn the phone a full circle.",
        )}
      </p>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   2.–5. ODSEK MUZEJSKI OBISK — voden ogled, napredek, zaključek, spomin
   ════════════════════════════════════════════════════════════════ */

function VisitSection({ geo }: { geo: VisitorGeo }) {
  const { t, lang } = useLang();
  const started = useVisitor((s) => s.started);
  const completed = useVisitor((s) => s.completed);
  const persona = useVisitor((s) => s.persona);

  if (!started) return null;

  const stations = personaStations(persona);
  const personaMeta = persona ? PERSONA_META[persona] : null;

  return (
    <section
      id="obisk"
      aria-labelledby="obisk-naslov"
      className="scroll-mt-20 border-b border-border/60 bg-gradient-to-b from-primary/5 to-transparent"
    >
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:py-14">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <Ticket className="size-7 text-primary" aria-hidden />
              <h2
                id="obisk-naslov"
                className="font-display text-3xl font-semibold tracking-tight sm:text-4xl"
              >
                {t("Muzejski obisk", "Museum visit")}
              </h2>
            </div>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              {t(
                "Vodeni ogled po časovnih portalih vasi — postaja za postajo, na lokaciji se vsaka odklene.",
                "A guided tour of the village's time portals — station by station, each unlocks on location.",
              )}
            </p>
          </div>
          {personaMeta && (
            <Badge variant="outline" className="gap-1.5 border-primary/40 px-3 py-1 text-xs text-primary">
              <personaMeta.icon className="size-3.5" aria-hidden />
              {lang === "si" ? personaMeta.si : personaMeta.en}
            </Badge>
          )}
        </div>

        {completed ? (
          <CompletionCard stations={stations} />
        ) : (
          <StationGuide geo={geo} stations={stations} />
        )}
      </div>
    </section>
  );
}

/* ── voden ogled: trenutna postaja + napredek + Q&A ── */

function StationGuide({ geo, stations }: { geo: VisitorGeo; stations: string[] }) {
  const { t } = useLang();
  const completeVisit = useVisitor((s) => s.completeVisit);
  const unlocked = useTimespots((s) => s.unlocked);

  const stationIds = stations;
  const doneIds = stationIds.filter((id) => unlocked.includes(id));
  const currentId = stationIds.find((id) => !unlocked.includes(id)) ?? null;
  const current = currentId ? getSpotById(currentId) : null;
  const currentIdx = currentId ? stationIds.indexOf(currentId) : stationIds.length;
  const progressPct = Math.round((doneIds.length / stationIds.length) * 100);
  const doneCount = doneIds.length;
  const totalCount = stationIds.length;

  /* samodejni zaključek: vse postaje poti odklenjene (issue #15, točka 4) */
  useEffect(() => {
    if (totalCount > 0 && doneCount === totalCount) {
      completeVisit();
    }
  }, [doneCount, totalCount, completeVisit]);

  return (
    <div className="mt-6 grid gap-4 lg:grid-cols-[1.2fr_1fr]">
      {/* levo: trenutna postaja */}
      <div className="min-w-0 space-y-4">
        {current ? (
          <StationCard
            geo={geo}
            spot={current}
            num={currentIdx + 1}
            total={stationIds.length}
          />
        ) : null}

        {/* ročni zaključek — obisk je njegov */}
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border bg-card p-4">
          <p className="text-xs text-muted-foreground">
            {t(
              `Odklenjenih ${doneIds.length} od ${stationIds.length} postaj.`,
              `${doneIds.length} of ${stationIds.length} stations unlocked.`,
            )}
          </p>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={completeVisit}
            disabled={doneIds.length === 0}
            className="gap-1.5"
          >
            <Award className="size-4" aria-hidden />
            {t("Zaključi obisk", "Finish the visit")}
          </Button>
        </div>

        {/* oddaljene točke — izven osnovne poti (raziskovalcu na poti) */}
        <DistantExtras />
      </div>

      {/* desno: napredek + vprašanja */}
      <div className="min-w-0 space-y-4">
        <ProgressList stations={stationIds} />
        {current && <StationQA spotId={current.id} defaultOpen={false} />}
      </div>
      <span className="sr-only">{t("Napredek", "Progress")}: {progressPct}%</span>
    </div>
  );
}

/* ── kartica trenutne postaje (issue #15, točka 2) ── */

function StationCard({
  geo,
  spot,
  num,
  total,
}: {
  geo: VisitorGeo;
  spot: TimeSpot;
  num: number;
  total: number;
}) {
  const { t, lang } = useLang();
  const openTM = useTimeMachine((s) => s.openTM);
  const isUnlocked = useTimespots((s) => s.isUnlocked);
  const sawOnboarding = useVisitor((s) => s.sawOnboarding);
  const [help, setHelp] = useState(false);

  const unlocked = isUnlocked(spot.id);
  const dist = geo.fix ? distanceM(geo.fix, { lat: spot.lat, lng: spot.lng }) : null;
  const inRadius = dist != null && dist <= spot.radius;

  const status =
    unlocked
      ? { tone: "ok", si: "Odklenjeno — odkritje v zbirki ✓", en: "Unlocked — a discovery in your collection ✓" }
      : geo.fix == null
        ? { tone: "wait", si: "GPS izklopljen — odklene se na lokaciji", en: "GPS off — it unlocks on location" }
        : inRadius
          ? { tone: "ok", si: "AR pripravljen — odkleni se na lokaciji", en: "AR ready — unlocks on location" }
          : {
              tone: "wait",
              si: `Oddaljeni ${formatDistance(dist!, "si")} — radij odklepa ${spot.radius} m`,
              en: `${formatDistance(dist!, "en")} away — unlock radius ${spot.radius} m`,
            };

  const toneClass =
    status.tone === "ok"
      ? "border-emerald-600/30 bg-emerald-600/10 text-emerald-700 dark:text-emerald-300"
      : "border-border bg-secondary/60 text-muted-foreground";

  return (
    <div className="rounded-xl border bg-card p-4 shadow-sm sm:p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-mono text-xs font-bold text-primary">
            {t(`Postaja ${num}/${total}`, `Station ${num}/${total}`)}
          </p>
          <h3 className="mt-1 font-display text-xl font-semibold leading-snug">
            {lang === "si" ? spot.titleSi : spot.titleEn}
          </h3>
          <p className="mt-1 inline-flex items-center gap-1.5 rounded-full bg-primary px-2.5 py-0.5 text-xs font-bold text-primary-foreground">
            🕰 {spotYearParam(spot.year)}
          </p>
        </div>
        <Button
          type="button"
          variant="ghost"
          size="icon"
          aria-label={t("Pomoč za AR", "AR help")}
          onClick={() => {
            setHelp((h) => !h);
            if (!useVisitor.getState().onboardingSeen) sawOnboarding();
          }}
          className="size-8 shrink-0"
        >
          <HelpCircle className="size-4" aria-hidden />
        </Button>
      </div>

      <p className="mt-2.5 max-w-xl text-sm leading-relaxed text-muted-foreground">
        {lang === "si" ? spot.descSi : spot.descEn}
      </p>

      {help && (
        <div className="mt-3">
          <ArOnboarding geo={geo} />
        </div>
      )}

      {/* razdalja + status */}
      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        <div className={`rounded-lg border px-3 py-2 ${toneClass}`}>
          <p className="text-[11px] font-semibold uppercase tracking-wider opacity-80">
            {t("Razdalja", "Distance")}
          </p>
          <p className="text-sm font-semibold">
            {geo.fix && dist != null ? formatDistance(dist, lang) : t("—", "—")}
          </p>
        </div>
        <div className={`rounded-lg border px-3 py-2 ${toneClass}`}>
          <p className="text-[11px] font-semibold uppercase tracking-wider opacity-80">
            {t("Status", "Status")}
          </p>
          <p className="text-sm font-semibold">
            {lang === "si" ? status.si : status.en}
          </p>
        </div>
      </div>

      {/* akcije — obstoječi sistemi */}
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <Button type="button" size="lg" onClick={() => openTM(spot.year, spot.id)} className="gap-2">
          <Hourglass className="size-4" aria-hidden />
          {unlocked
            ? t("Odpri v AR", "Open in AR")
            : inRadius
              ? t("Odpri v AR", "Open in AR")
              : t("Odpri (predogled)", "Open (preview)")}
        </Button>
        {spot.panoramaId && (
          <Button
            type="button"
            variant="secondary"
            size="lg"
            onClick={() => openTM(spot.year, spot.id, false, true)}
            className="gap-2"
          >
            {t("Doživi 360°", "Experience 360°")}
          </Button>
        )}
        <a
          href={osmDirectionsUrl({ lat: spot.lat, lng: spot.lng }, geo.fix)}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex h-11 items-center gap-1.5 rounded-md border px-4 text-sm font-medium transition-colors hover:border-primary/40 hover:bg-accent"
        >
          <Navigation className="size-4" aria-hidden />
          {t("Navigiraj", "Navigate")}
        </a>
        <a
          href="#zemljevid"
          className="inline-flex h-11 items-center gap-1.5 rounded-md border px-4 text-sm font-medium transition-colors hover:border-primary/40 hover:bg-accent"
        >
          <MapPin className="size-4" aria-hidden />
          {t("Na zemljevid", "On the map")}
        </a>
        {geo.fix == null && (
          <Button type="button" variant="outline" size="lg" onClick={geo.start} className="gap-2">
            <Compass className="size-4" aria-hidden />
            {t("Vklopi GPS", "Turn on GPS")}
          </Button>
        )}
      </div>

      <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
        {t("Vir: ", "Source: ")}
        {lang === "si" ? spot.evidenceSi : spot.evidenceEn}
      </p>
    </div>
  );
}

/* ── napredek: Moje raziskovanje (issue #15, točka 3) ── */

function ProgressList({ stations }: { stations: string[] }) {
  const { t, lang } = useLang();
  const unlocked = useTimespots((s) => s.unlocked);
  const pct = Math.round((stations.filter((id) => unlocked.includes(id)).length / stations.length) * 100);

  return (
    <div className="rounded-xl border bg-card p-4 sm:p-5">
      <h3 className="font-display text-lg font-semibold">
        {t("Moje raziskovanje", "My exploration")}
      </h3>
      <div className="mt-3">
        <div className="mb-1.5 flex items-center justify-between text-xs text-muted-foreground">
          <span>
            {t(
              `${stations.filter((id) => unlocked.includes(id)).length}/${stations.length}`,
              `${stations.filter((id) => unlocked.includes(id)).length}/${stations.length}`,
            )}
          </span>
          <span className="font-mono">{pct} %</span>
        </div>
        <Progress value={pct} aria-label={t("Napredek obiska", "Visit progress")} />
      </div>
      <ul className="mt-3 space-y-1">
        {stations.map((id) => {
          const s = getSpotById(id);
          if (!s) return null;
          const done = unlocked.includes(id);
          return (
            <li
              key={id}
              className={`flex items-center gap-2 rounded-md px-2 py-1.5 text-sm ${
                done ? "text-foreground" : "text-muted-foreground"
              }`}
            >
              {done ? (
                <CheckCircle2 className="size-4 shrink-0 text-primary" aria-hidden />
              ) : (
                <span className="ml-0.5 mr-0.5 inline-block size-3.5 shrink-0 rounded-full border-2 border-border" aria-hidden />
              )}
              <span className={done ? "font-medium" : undefined}>
                {lang === "si" ? s.titleSi : s.titleEn}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

/* ── Q&A: vprašanja muzejskega vodnika (issue #15, točka 9 — šola) ── */

function StationQA({ spotId, defaultOpen }: { spotId: string; defaultOpen: boolean }) {
  const { t, lang } = useLang();
  const [openAll, setOpenAll] = useState(defaultOpen);
  const qa = useMemo(() => getGuideForSpot(spotId), [spotId]);
  const [open, setOpen] = useState<Record<string, boolean>>({});

  if (qa.length === 0) return null;

  return (
    <div className="rounded-xl border bg-card p-4 sm:p-5">
      <div className="flex items-center justify-between gap-2">
        <h3 className="flex items-center gap-2 font-display text-lg font-semibold">
          <HelpCircle className="size-5 text-primary" aria-hidden />
          {t("Vprašajte vodnika", "Ask the guide")}
        </h3>
        <button
          type="button"
          onClick={() => setOpenAll((v) => !v)}
          className="text-xs font-medium text-primary underline decoration-dotted underline-offset-2"
        >
          {openAll ? t("skrči", "collapse") : t("odpri vse", "expand all")}
        </button>
      </div>
      <ul className="mt-3 space-y-2">
        {qa.map((g) => {
          const isOpen = openAll || open[g.id];
          return (
            <li key={g.id} className="rounded-lg border bg-secondary/40">
              <button
                type="button"
                onClick={() => setOpen((p) => ({ ...p, [g.id]: !isOpen }))}
                aria-expanded={isOpen}
                className="flex w-full items-start justify-between gap-2 p-3 text-left"
              >
                <span className="text-sm font-semibold">
                  {lang === "si" ? g.questionSi : g.questionEn}
                </span>
                <span className="mt-0.5 shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold text-muted-foreground">
                  {g.period}
                </span>
              </button>
              {isOpen && (
                <div className="border-t px-3 pb-3 pt-2.5">
                  <p className="text-sm leading-relaxed text-foreground/90">
                    {lang === "si" ? g.answerSi : g.answerEn}
                  </p>
                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold ${GUIDE_STATUS_STYLE[g.status]}`}>
                      {g.status}
                    </span>
                    <span className="font-mono text-[11px] text-muted-foreground">{g.source}</span>
                  </div>
                </div>
              )}
            </li>
          );
        })}
      </ul>
      <AllQuestions />
    </div>
  );
}

function AllQuestions() {
  const { t, lang } = useLang();
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-3 border-t pt-3">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="text-xs font-medium text-muted-foreground underline decoration-dotted underline-offset-2 hover:text-foreground"
      >
        {open
          ? t("skrči vsa vprašanja", "collapse all questions")
          : t(`vsa vprašanja vodnika (${GUIDE_TOTAL}) — AI priprava`, `all guide questions (${GUIDE_TOTAL}) — AI prep`)}
      </button>
      {open && (
        <ul className="mt-2 max-h-72 space-y-1 overflow-y-auto pr-1 text-[13px] leading-snug">
          {GUIDE_QA.map((g) => {
            const s = getSpotById(g.spotId);
            return (
              <li key={g.id} className="rounded border bg-secondary/30 px-2.5 py-1.5">
                <span className="font-semibold">
                  {lang === "si" ? g.questionSi : g.questionEn}
                </span>
                <span className="ml-2 text-muted-foreground">
                  · {s ? (lang === "si" ? s.titleSi : s.titleEn) : g.location} · {g.period}
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

/* ── oddaljene točke: izven osnovne poti ── */

function DistantExtras() {
  const { t, lang } = useLang();
  const openTM = useTimeMachine((s) => s.openTM);
  const unlocked = useTimespots((s) => s.unlocked);
  const persona = useVisitor((s) => s.persona);
  const spots = useMemo(
    () => TIME_SPOTS.filter((s) => isDistantSpot(s)),
    [],
  );

  /* raziskovalcu so oddaljene točke ŽE na poti — ne podvajamo */
  if (persona === "raziskovalec") return null;

  return (
    <details className="group rounded-xl border bg-card">
      <summary className="flex cursor-pointer list-none items-center gap-2 p-4 text-sm font-semibold">
        <MapPin className="size-4 text-primary" aria-hidden />
        {t(
          "Izven osnovne poti — mlini, letališče Otok, Cerkvišče",
          "Beyond the main route — the mills, the Otok airfield, Cerkvišče",
        )}
      </summary>
      <div className="grid gap-3 border-t p-4 sm:grid-cols-2 lg:grid-cols-1">
        {spots.map((s) => (
          <div key={s.id} className="flex items-center justify-between gap-3 rounded-lg border p-3">
            <div className="min-w-0">
              <p className="flex items-center gap-2 text-sm font-semibold">
                {unlocked.includes(s.id) && (
                  <CheckCircle2 className="size-3.5 shrink-0 text-primary" aria-hidden />
                )}
                {lang === "si" ? s.titleSi : s.titleEn}
              </p>
              <p className="mt-0.5 text-[11px] text-muted-foreground">
                🕰 {spotYearParam(s.year)} · {t("lastna mini vsebina", "own mini content")}
              </p>
            </div>
            <Button type="button" variant="outline" size="sm" onClick={() => openTM(s.year, s.id)}>
              {t("Odpri", "Open")}
            </Button>
          </div>
        ))}
      </div>
    </details>
  );
}

/* ── zaključek obiska (issue #15, točka 4) + spomin (točka 5) ── */

function CompletionCard({ stations }: { stations: string[] }) {
  const { t, lang } = useLang();
  const reopenVisit = useVisitor((s) => s.reopenVisit);
  const resetVisit = useVisitor((s) => s.resetVisit);
  const resetSpots = useTimespots((s) => s.reset);
  const souvenirSavedAt = useVisitor((s) => s.souvenirSavedAt);

  const unlocked = useTimespots((s) => s.unlocked);
  const spotsUnlocked = unlocked.length;
  const panoUnlocked = unlocked.filter((id) => getSpotById(id)?.panoramaId).length;
  const allFound = stations.every((id) => unlocked.includes(id));

  /* nov obisk: počisti okvir OBISKA in zbirko odkritij (obstoječi akciji
     reset — zbirka ostane drugače takoj »zaključena«) */
  const startNewVisit = () => {
    resetVisit();
    resetSpots();
  };

  return (
    <div className="mt-6 grid gap-4 lg:grid-cols-[1fr_1.2fr]">
      {/* čestitamo */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="rounded-xl border bg-card p-5 shadow-sm sm:p-6"
      >
        <div className="flex items-center gap-3">
          <span className="flex size-12 items-center justify-center rounded-full bg-primary/10">
            <Award className="size-6 text-primary" aria-hidden />
          </span>
          <h3 className="font-display text-2xl font-semibold">
            {t("Čestitamo!", "Congratulations!")}
          </h3>
        </div>
        <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
          {allFound
            ? t(
                "Zaključili ste Muzej Griblje — vsa odkritja vaše poti so v zbirki.",
                "You have completed the Griblje Museum — every discovery of your route is in the collection.",
              )
            : t(
                "Zaključili ste obisk Muzeja Griblje.",
                "You have finished your visit to the Griblje Museum.",
              )}
        </p>

        <p className="mt-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          {t("Odkrili ste", "You discovered")}
        </p>
        <dl className="mt-2 grid grid-cols-2 gap-2.5">
          {[
            {
              v: `${spotsUnlocked}/${TOTAL_SPOTS}`,
              si: "časovnih portalov",
              en: "time portals",
            },
            {
              v: `${panoUnlocked}/${PANORAMA_COUNT}`,
              si: "zgodovinskih panoram",
              en: "historic panoramas",
            },
            {
              v: String(BUILDINGS_1825_COUNT),
              si: "zgodovinskih stavb 1825",
              en: "historic buildings of 1825",
            },
            {
              v: String(GUIDE_TOTAL),
              si: "preverjenih zgodovinskih zgodb",
              en: "verified historical stories",
            },
          ].map((s) => (
            <div key={s.si} className="rounded-lg border bg-secondary/40 px-3 py-2.5">
              <dd className="font-display text-xl font-bold text-primary">{s.v}</dd>
              <dt className="text-[11px] leading-snug text-muted-foreground">{t(s.si, s.en)}</dt>
            </div>
          ))}
        </dl>

        <div className="mt-4 flex flex-wrap gap-2">
          <SouvenirActions />
          {allFound ? (
            <Button type="button" variant="outline" onClick={startNewVisit} className="gap-1.5">
              <RotateCcw className="size-4" aria-hidden />
              {t("Začni nov obisk", "Start a new visit")}
            </Button>
          ) : (
            <Button type="button" variant="outline" onClick={reopenVisit} className="gap-1.5">
              <RotateCcw className="size-4" aria-hidden />
              {t("Nadaljuj raziskovanje", "Keep exploring")}
            </Button>
          )}
        </div>
        {souvenirSavedAt && (
          <p className="mt-2 text-xs text-muted-foreground">
            {t("Spomin shranjen", "Memory saved")}:{" "}
            {new Intl.DateTimeFormat(lang === "si" ? "sl-SI" : "en-GB", {
              timeStyle: "short",
              dateStyle: "short",
            }).format(new Date(souvenirSavedAt))}
          </p>
        )}
      </motion.div>

      {/* digitalni spomin — razglednica */}
      <SouvenirCard />
    </div>
  );
}

/* ── digitalni spomin (issue #15, točka 5): razglednica + deljenje ── */

function SouvenirActions() {
  const { t } = useLang();
  return (
    <Button type="button" size="lg" onClick={() => downloadPostcard()} className="gap-2">
      <Gift className="size-4" aria-hidden />
      {t("Shrani spomin", "Save the memory")}
    </Button>
  );
}

function SouvenirCard() {
  const { t, lang } = useLang();
  const startAt = useVisitor((s) => s.startAt);
  const souvenirSavedAt = useVisitor((s) => s.souvenirSavedAt);
  const unlocked = useTimespots((s) => s.unlocked);
  const [copied, setCopied] = useState(false);

  const dateLabel = startAt
    ? new Intl.DateTimeFormat(lang === "si" ? "sl-SI" : "en-GB", { dateStyle: "long" }).format(
        new Date(startAt),
      )
    : "—";

  const share = async () => {
    const url = "https://griblje-museum.vercel.app/";
    const text =
      lang === "si"
        ? `Moj obisk Muzeja Griblje: odklenjenih ${unlocked.length} od ${TOTAL_SPOTS} časovnih portalov. Muzej vasi ob Kolpi — priporočam!`
        : `My visit to the Griblje Village Museum: ${unlocked.length} of ${TOTAL_SPOTS} time portals unlocked. A village museum on the Kolpa — recommended!`;
    try {
      if (navigator.share) {
        await navigator.share({ title: "Muzej vasi Griblje", text, url });
        return;
      }
      throw new Error("no share");
    } catch {
      try {
        await navigator.clipboard.writeText(`${text}\n${url}`);
        setCopied(true);
        window.setTimeout(() => setCopied(false), 2600);
      } catch {
        /* tiho — uporabnik ima klembordo zaprt */
      }
    }
  };

  return (
    <div className="overflow-hidden rounded-xl border bg-card shadow-sm">
      {/* zgornji trak razglednice */}
      <div className="bg-primary px-5 py-4 text-primary-foreground">
        <p className="text-[11px] font-semibold uppercase tracking-widest opacity-90">
          {t("Digitalni spomin", "Digital souvenir")} · 1526–2026
        </p>
        <h3 className="mt-1 font-display text-2xl font-semibold">
          {t("Moj obisk Muzeja Griblje", "My visit to the Griblje Museum")}
        </h3>
      </div>

      <div className="grid gap-0 sm:grid-cols-[1fr_180px]">
        <div className="p-5">
          <dl className="space-y-2.5 text-sm">
            <div>
              <dt className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                {t("Datum", "Date")}
              </dt>
              <dd className="font-medium">{dateLabel}</dd>
            </div>
            <div>
              <dt className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                {t("Odkrite lokacije", "Discovered locations")}
              </dt>
              <dd className="mt-0.5">
                <ul className="space-y-0.5">
                  {TIME_SPOTS.map((s) => {
                    const done = unlocked.includes(s.id);
                    return (
                      <li
                        key={s.id}
                        className={`flex items-center gap-1.5 ${done ? "" : "text-muted-foreground/60"}`}
                      >
                        {done ? "✓" : "○"} {lang === "si" ? s.titleSi : s.titleEn}
                      </li>
                    );
                  })}
                </ul>
                <p className="mt-1 text-xs text-muted-foreground">
                  {t(
                    `${unlocked.length}/${TOTAL_SPOTS} odklenjenih`,
                    `${unlocked.length}/${TOTAL_SPOTS} unlocked`,
                  )}
                </p>
              </dd>
            </div>
            <div>
              <dt className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                {t("Zgodbe", "Stories")}
              </dt>
              <dd className="font-medium">
                {GUIDE_TOTAL} {t("preverjenih zgodb", "verified stories")}
              </dd>
            </div>
          </dl>
        </div>

        <figure className="border-t sm:border-l sm:border-t-0">
          <img
            src="/images/authentic/griblje-vas.jpg"
            alt={t(
              "Vas Griblje ob Kolpi — spominska fotografija obiska",
              "The village of Griblje on the Kolpa — a visit keepsake photo",
            )}
            className="h-44 w-full object-cover sm:h-full"
            loading="lazy"
          />
          <figcaption className="px-2 py-1.5 text-[10px] leading-tight text-muted-foreground">
            Foto: Andrejj · Wikimedia Commons · CC BY-SA 3.0
          </figcaption>
        </figure>
      </div>

      <div className="flex flex-wrap items-center gap-2 border-t p-4">
        <Button type="button" variant="secondary" onClick={() => downloadPostcard()} className="gap-2">
          <Download className="size-4" aria-hidden />
          {t("Prenesi razglednico (PNG)", "Download the postcard (PNG)")}
        </Button>
        <Button type="button" variant="outline" onClick={share} className="gap-2">
          <Share2 className="size-4" aria-hidden />
          {t("Deli spomin", "Share the memory")}
        </Button>
        {copied && (
          <span role="status" className="text-xs font-medium text-primary">
            {t("Povzetek s povezavo kopiran ✓", "Summary with link copied ✓")}
          </span>
        )}
        {souvenirSavedAt && (
          <span className="text-xs text-muted-foreground">
            <CheckCircle2 className="mr-1 inline size-3.5 text-primary" aria-hidden />
            {t("shranjeno", "saved")}
          </span>
        )}
      </div>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   DOCK — plavajoča vodica na mobilnem (naslednja postaja vedno pri roki)
   ════════════════════════════════════════════════════════════════ */

function VisitDock({ geo }: { geo: VisitorGeo }) {
  const { t, lang } = useLang();
  const started = useVisitor((s) => s.started);
  const completed = useVisitor((s) => s.completed);
  const persona = useVisitor((s) => s.persona);
  const dockDismissed = useVisitor((s) => s.dockDismissed);
  const dismissDock = useVisitor((s) => s.dismissDock);
  const souvenirSavedAt = useVisitor((s) => s.souvenirSavedAt);
  const openTM = useTimeMachine((s) => s.openTM);
  const tmOpen = useTimeMachine((s) => s.open);
  const unlocked = useTimespots((s) => s.unlocked);

  /* dober bonton: dok ne moti — skrit med AR, po zaključku le opomnik
     na spomin, potem čisto gor */
  if (
    !started ||
    dockDismissed ||
    tmOpen ||
    (completed && souvenirSavedAt)
  ) {
    return null;
  }

  const stations = personaStations(persona);
  const currentId = stations.find((id) => !unlocked.includes(id)) ?? null;

  if (completed && !souvenirSavedAt) {
    return (
      <div className="fixed inset-x-4 bottom-4 z-40 lg:hidden">
        <div className="mx-auto flex max-w-md items-center justify-between gap-3 rounded-xl border bg-card p-3 shadow-lg">
          <p className="min-w-0 text-sm font-semibold">
            <CheckCircle2 className="mr-1.5 inline size-4 text-primary" aria-hidden />
            {t("Obisk zaključen", "Visit completed")}
          </p>
          <a
            href="#obisk"
            className="inline-flex items-center gap-1.5 rounded-md bg-primary px-3 py-2 text-xs font-semibold text-primary-foreground"
          >
            <Gift className="size-3.5" aria-hidden />
            {t("Shrani spomin", "Save the memory")}
          </a>
          <button
            type="button"
            onClick={dismissDock}
            aria-label={t("Skrij", "Hide")}
            className="rounded-full border p-1 text-muted-foreground"
          >
            <X className="size-3.5" aria-hidden />
          </button>
        </div>
      </div>
    );
  }

  if (!currentId) return null;
  const spot = getSpotById(currentId);
  if (!spot) return null;
  const num = stations.indexOf(currentId) + 1;
  const dist = geo.fix ? distanceM(geo.fix, { lat: spot.lat, lng: spot.lng }) : null;
  const pct = Math.round(
    (stations.filter((id) => unlocked.includes(id)).length / stations.length) * 100,
  );

  return (
    <div className="fixed inset-x-4 bottom-4 z-40 lg:hidden">
      <div className="mx-auto max-w-md rounded-xl border bg-card/95 p-3 shadow-lg backdrop-blur">
        <div className="flex items-center justify-between gap-3">
          <div className="min-w-0 flex-1">
            <p className="font-mono text-[10px] font-bold text-primary">
              {t(`OBISK · POSTAJA ${num}/${stations.length}`, `VISIT · STATION ${num}/${stations.length}`)}
            </p>
            <p className="truncate text-sm font-semibold">
              {lang === "si" ? spot.titleSi : spot.titleEn}
              {dist != null && (
                <span className="ml-1.5 font-normal text-muted-foreground">
                  · {formatDistance(dist, lang)}
                </span>
              )}
            </p>
            <Progress
              value={pct}
              className="mt-1.5 h-1"
              aria-label={t("Napredek obiska", "Visit progress")}
            />
          </div>
          <Button type="button" size="sm" onClick={() => openTM(spot.year, spot.id)} className="shrink-0">
            <Hourglass className="size-3.5" aria-hidden />
            {t("Odpri", "Open")}
          </Button>
          <a
            href="#obisk"
            aria-label={t("Odpri vodeni ogled", "Open the guided tour")}
            className="shrink-0 rounded-full border p-1.5 text-muted-foreground"
          >
            <ChevronUp className="size-4" aria-hidden />
          </a>
          <button
            type="button"
            onClick={dismissDock}
            aria-label={t("Skrij vodico", "Hide the guide bar")}
            className="shrink-0 rounded-full border p-1.5 text-muted-foreground"
          >
            <X className="size-4" aria-hidden />
          </button>
        </div>
      </div>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   RAZGLEDNICA — canvas PNG (digitalni spomin, issue #15, točka 5)
   ════════════════════════════════════════════════════════════════ */

function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

async function drawPostcard(lang: "si" | "en", startAt: string | null): Promise<Blob | null> {
  const W = 1200;
  const H = 840;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const ctx = c.getContext("2d");
  if (!ctx) return null;

  const unlocked = useTimespots.getState().unlocked;
  const TERA = "#9F4A2B";
  const SMET = "#F2EEE6";
  const TEMNA = "#0F1610";
  const SIVA = "rgba(15,22,16,0.62)";

  /* ozadje + glava */
  ctx.fillStyle = SMET;
  ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = TERA;
  ctx.fillRect(0, 0, W, 118);
  ctx.fillStyle = "#FFFFFF";
  ctx.font = "700 34px Georgia, 'Times New Roman', serif";
  ctx.fillText("MUZEJ VASI GRIBLJE", 48, 72);
  ctx.textAlign = "right";
  ctx.font = "600 22px Georgia, serif";
  ctx.fillText("500 let · 1526–2026", W - 48, 72);
  ctx.textAlign = "left";

  /* naslov + datum */
  const dateLabel = startAt
    ? new Intl.DateTimeFormat(lang === "si" ? "sl-SI" : "en-GB", { dateStyle: "long" }).format(
        new Date(startAt),
      )
    : "";
  ctx.fillStyle = TEMNA;
  ctx.font = "700 44px Georgia, serif";
  ctx.fillText(lang === "si" ? "Moj obisk Muzeja Griblje" : "My visit to the Griblje Museum", 48, 200);
  ctx.fillStyle = SIVA;
  ctx.font = "400 24px system-ui, sans-serif";
  ctx.fillText(dateLabel, 48, 240);

  /* fotografija (desno) — cover, zaobljeni ogli */
  const PX = 640;
  const PY = 300;
  const PW = 512;
  const PH = 320;
  try {
    const photo = await loadImage("/images/authentic/griblje-vas.jpg");
    const scale = Math.max(PW / photo.width, PH / photo.height);
    const dw = photo.width * scale;
    const dh = photo.height * scale;
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(PX, PY, PW, PH, 14);
    ctx.clip();
    ctx.drawImage(photo, PX + (PW - dw) / 2, PY + (PH - dh) / 2, dw, dh);
    ctx.restore();
    ctx.strokeStyle = TERA;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(PX, PY, PW, PH, 14);
    ctx.stroke();
    ctx.fillStyle = SIVA;
    ctx.font = "400 15px system-ui, sans-serif";
    ctx.fillText("Foto: Andrejj · Wikimedia Commons · CC BY-SA 3.0 — vas Griblje ob Kolpi", PX, PY + PH + 26);
  } catch {
    ctx.strokeStyle = TERA;
    ctx.lineWidth = 2;
    ctx.strokeRect(PX, PY, PW, PH);
  }

  /* odkritja (levo) */
  ctx.fillStyle = TEMNA;
  ctx.font = "700 22px Georgia, serif";
  ctx.fillText(lang === "si" ? "Odkrita odkritja" : "Discovered", 48, 306);
  ctx.font = "400 20px system-ui, sans-serif";
  let y = 344;
  for (const s of TIME_SPOTS) {
    const done = unlocked.includes(s.id);
    ctx.fillStyle = done ? TEMNA : "rgba(15,22,16,0.38)";
    const title = lang === "si" ? s.titleSi : s.titleEn;
    ctx.fillText(`${done ? "✓" : "○"} ${title.length > 34 ? title.slice(0, 33) + "…" : title}`, 48, y);
    y += 30;
  }

  /* statistika */
  const stats = [
    `${unlocked.length}/${TOTAL_SPOTS} ${lang === "si" ? "portalov" : "portals"}`,
    `${PANORAMA_COUNT} ${lang === "si" ? "panorame" : "panoramas"}`,
    `${BUILDINGS_1825_COUNT} ${lang === "si" ? "stavb 1825" : "buildings 1825"}`,
    `${GUIDE_TOTAL} ${lang === "si" ? "zgodb" : "stories"}`,
  ];
  ctx.fillStyle = TERA;
  ctx.fillRect(48, 706, W - 96, 58);
  ctx.fillStyle = "#FFFFFF";
  ctx.font = "600 20px system-ui, sans-serif";
  ctx.fillText(stats.join("  ·  "), 66, 742);

  /* noga */
  ctx.fillStyle = TEMNA;
  ctx.fillRect(0, H - 44, W, 44);
  ctx.fillStyle = SMET;
  ctx.font = "500 18px system-ui, sans-serif";
  ctx.fillText("griblje-museum.vercel.app", 48, H - 17);
  ctx.textAlign = "right";
  ctx.fillText(lang === "si" ? "Digitalni muzej vasi ob Kolpi" : "A digital village museum on the Kolpa", W - 48, H - 17);
  ctx.textAlign = "left";

  return new Promise((resolve) => c.toBlob((b) => resolve(b), "image/png", 0.92));
}

function downloadPostcard() {
  void (async () => {
    try {
      const lang = (localStorage.getItem("mvg-lang") === "en" ? "en" : "si") as "si" | "en";
      const blob = await drawPostcard(lang, useVisitor.getState().startAt);
      if (!blob) return;
      useVisitor.getState().saveSouvenir();
      const a = document.createElement("a");
      const d = new Date();
      const stamp = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, "0")}${String(d.getDate()).padStart(2, "0")}`;
      a.href = URL.createObjectURL(blob);
      a.download = `griblje-spomin-${stamp}.png`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    } catch {
      /* tiho — canvas/BLob ni na voljo */
    }
  })();
}

/* AnimatePresence ni potreben — dok animira z lastno montažo; tukaj je
   še izvoz pomožne kljuke za page (odmik noge, ko je dok viden). */
export function useVisitDockActive(): boolean {
  const started = useVisitor((s) => s.started);
  const completed = useVisitor((s) => s.completed);
  const dockDismissed = useVisitor((s) => s.dockDismissed);
  const souvenirSavedAt = useVisitor((s) => s.souvenirSavedAt);
  const tmOpen = useTimeMachine((s) => s.open);
  const mounted = useMounted();
  return (
    mounted &&
    started &&
    !dockDismissed &&
    !tmOpen &&
    !(completed && souvenirSavedAt)
  );
}
