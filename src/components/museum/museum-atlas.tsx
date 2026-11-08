"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import {
  Search,
  Map as MapIcon,
  BookOpen,
  Users,
  Archive,
  Gauge,
  ExternalLink,
  ShieldQuestion,
  MapPin,
  Home,
  X,
  Flag,
  ChevronLeft,
  ChevronRight,
  Layers,
  Eye,
  EyeOff,
  Boxes,
} from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { useLang } from "./language-context";
import { AtlasCanvas, type AtlasLayers } from "./atlas-canvas";
import {
  searchAtlas,
  getEvidenceChain,
  type AtlasSearchHit,
} from "@/lib/atlas";
import { ATLAS_HOUSES } from "@/data/atlas/houses";
import { ATLAS_OWNERS, SHEET_GEOREFS } from "@/data/atlas/model";
import { ATLAS_SOURCES, NEGATIVE_RESULTS, HERITAGE_UNITS } from "@/data/atlas/sources";
import { PARISH, PARISH_BOOKS, HOUSE_VITALS, type HouseVital } from "@/data/atlas/parish";
import { LANDUSE_ZONES, LANDUSE_ENTITIES, HAMLETS } from "@/data/atlas/landuse";
import { getCoverage, getArchiveInventory, parishStats, getHouseStory } from "@/lib/atlas";
import type { GeoFix } from "@/lib/geo";

const Canvas = dynamic(() => import("./atlas-canvas").then((m) => m.AtlasCanvas), {
  ssr: false,
  loading: () => (
    <div className="h-[380px] w-full animate-pulse rounded-xl border bg-secondary/50 sm:h-[460px] lg:h-[520px]" />
  ),
});

type Tab = "map" | "3d" | "houses" | "owners" | "parish" | "landuse" | "sources" | "coverage";

const STATUS_STYLE: Record<string, string> = {
  VERIFIED: "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
  DOCUMENTED: "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100",
  REVIEW: "bg-orange-100 text-orange-900 dark:bg-orange-900/60 dark:text-orange-100",
  RECONSTRUCTED: "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100",
  APPROXIMATE: "bg-yellow-100 text-yellow-900 dark:bg-yellow-900/60 dark:text-yellow-100",
  TO_COLLECT: "bg-stone-100 text-stone-900 dark:bg-stone-800 dark:text-stone-100",
  NOT_FOUND: "bg-neutral-200 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300",
  NOT_PUBLIC: "bg-neutral-200 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300",
};

const HOUSES = ATLAS_HOUSES.filter((h) => h.no !== "—");
const PARCELS = ATLAS_HOUSES.filter((h) => h.no === "—");
const COVERAGE = getCoverage();
/* issue #4: inventar 12 enot N83 — izračunan, ne ročno napisan */
const INVENTORY = getArchiveInventory();

const VillageViewer = dynamic(
  () => import("./village-viewer").then((m) => m.VillageViewer),
  {
    ssr: false,
    loading: () => (
      <div className="h-[420px] w-full animate-pulse rounded-xl border bg-secondary/50 sm:h-[520px]" />
    ),
  },
);

export function MuseumAtlas({
  userFix,
  onOpenMuseum,
}: {
  userFix: GeoFix | null;
  onOpenMuseum: (slug: string) => void;
}) {
  const { lang, t } = useLang();
  const [tab, setTab] = useState<Tab>("map");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<AtlasSearchHit[]>([]);
  const hits = query.trim().length < 2 ? [] : results;
  const [selected, setSelected] = useState<AtlasSearchHit | null>(null);
  const [layers, setLayers] = useState<AtlasLayers>({
    osm: true,
    a01: true,
    a02: true,
    a03: false,
    a04: false,
    a05: false,
    buildings: true,
    landuse: false,
    heritage: false,
    museum: false,
    vintage: false,
  });
  const [opacity, setOpacity] = useState(0.55);
  const [page, setPage] = useState(0);
  const [houseFilter, setHouseFilter] = useState("");
  const [focus, setFocus] = useState<{ lat: number; lng: number; zoom?: number } | null>(null);

  const PAGE = 24;

  /* iskanje (debounce) — prazni zadetki izpeljani, ne v efektu */
  useEffect(() => {
    if (query.trim().length < 2) return;
    const id = setTimeout(() => setResults(searchAtlas(query)), 180);
    return () => clearTimeout(id);
  }, [query]);

  /* globa povezava ?atlas=<id> — po hydraciji (asinhrono, izven telesa efekta) */
  useEffect(() => {
    const read = () => {
      const id = new URLSearchParams(window.location.search).get("atlas");
      if (!id) return;
      const all = searchAtlas(id.replace(/[-– ]/g, " "));
      const house = id.startsWith("hiša-") ? ATLAS_HOUSES.find((h) => h.id === id) : undefined;
      const hit =
        all.find((h) => h.id === id) ??
        (house
          ? {
              type: "house" as const,
              id,
              titleSi: `Hiša št. ${house.no} — ${house.owner}`,
              titleEn: `House no. ${house.no} — ${house.owner}`,
              detail: house.parcelRefs ? `PT str. ${house.sourcePage} · ${house.parcelRefs}` : `PT str. ${house.sourcePage}`,
              status: house.status,
            }
          : id.startsWith("hiša-")
            ? {
                type: "house" as const,
                id,
                titleSi: `Hiša št. ${id.replace("hiša-", "")}`,
                titleEn: `House no. ${id.replace("hiša-", "")}`,
                status: "REVIEW",
              }
            : all[0]);
      if (hit) {
        setSelected(hit);
        setTab((prev) => (prev === "map" ? prev : "map"));
      }
    };
    const t = setTimeout(read, 350);
    return () => clearTimeout(t);
  }, []);

  const clearSearch = useCallback(() => {
    setQuery("");
    setResults([]);
  }, []);

  const select = useCallback(
    (id: string, kind: string) => {
      const found = searchAtlas(id.replace(/[-–]/g, " "))[0] ?? null;
      /* raba tal (issue #7): klik na cono → hišni pogled cone */
      if (kind === "landuse") {
        const zone = LANDUSE_ZONES.find((z) => z.id === id);
        if (zone) {
          setSelected({
            type: "house",
            id: zone.id,
            titleSi: zone.labelSi,
            titleEn: zone.labelEn,
            detail: lang === "si" ? zone.noteSi : zone.noteEn,
            status: zone.status,
          });
          const [[n, w], [s, e]] = zone.bounds;
          setFocus({ lat: (n + s) / 2, lng: (w + e) / 2, zoom: 15 });
          return;
        }
      }
      const obj =
        found ??
        (kind === "building"
          ? {
              type: "house" as const,
              id,
              titleSi: "Objekt ~1825 (vektorizacija)",
              titleEn: "Building ~1825 (vectorised)",
              status: "RECONSTRUCTED",
            }
          : null);
      if (obj) {
        setSelected(obj);
        const b = SHEET_GEOREFS[1].bounds;
        setFocus({ lat: (b[0][0] + b[1][0]) / 2, lng: (b[0][1] + b[1][1]) / 2, zoom: 15 });
      }
    },
    [lang],
  );

  const evidence = useMemo(
    () => (selected && selected.type === "house" ? getEvidenceChain(selected.id) : null),
    [selected],
  );

  const filteredHouses = useMemo(() => {
    const q = houseFilter.trim().toLowerCase();
    if (!q) return HOUSES;
    return HOUSES.filter(
      (h) =>
        h.no.toLowerCase().includes(q) ||
        h.owner.toLowerCase().includes(q) ||
        (h.ownerModernGuess ?? "").toLowerCase().includes(q),
    );
  }, [houseFilter]);

  const paged = filteredHouses.slice(page * PAGE, (page + 1) * PAGE);
  const pages = Math.max(1, Math.ceil(filteredHouses.length / PAGE));

  const church = HERITAGE_UNITS.find((h) => h.esd === 2122);

  const openSourceTab = () => setTab("sources");

  return (
    <section
      id="atlas"
      className="scroll-mt-20 border-t border-border/60 bg-gradient-to-b from-secondary/30 to-transparent"
    >
      <div className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6 lg:px-8">
        {/* glava */}
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="flex items-center gap-3">
              <Archive className="h-7 w-7 text-primary" aria-hidden />
              <h2 className="font-serif text-3xl font-bold tracking-tight sm:text-4xl">
                {t("ATLAS 1825", "ATLAS 1825")}
              </h2>
              <Badge variant="outline" className="border-primary/40 text-primary">
                k.o. št. 83
              </Badge>
            </div>
            <p className="mt-3 max-w-2xl text-muted-foreground">
              {t(
                "Zgodovinska katastrska slika vasi Griblje (Grüble) iz franciscejskega katastra: 5/5 listov z georeferenco — A01/A02 z VALIDIRANO afino (GEOTRUTH na cerkvi EŠD 2122, ±40–100 m) + A03/A04/A05 s P46 neatline afinami (P50: meje = uradne meje celic eZKN 1:2880, ±40–50 m; prej GRID_APPROX ±200–400 m), register hiš 1–98 z lastniki, arhivski viri z dokazno verigo in primerjava 1825 ↔ danes.",
                "The historical cadastral picture of the village of Griblje (Grüble) from the Franciscan cadastre: 5/5 sheets georeferenced — A01/A02 with a VALIDATED affine (GEOTRUTH on the EŠD 2122 church, ±40–100 m) + A03/A04/A05 with the P46 neatline affines (P50: bounds = the official boundaries of the eZKN 1:2880 cells, ±40–50 m; previously GRID_APPROX ±200–400 m), a register of houses 1–98 with owners, archival sources with an evidence chain, and an 1825 ↔ today comparison.",
              )}
            </p>
          </div>
          <div className="text-sm text-muted-foreground">
            <div className="font-medium">{t("Vir", "Source")}</div>
            <div>Arhiv RS · SI AS 176/N/N83</div>
            <div>{t("Franciscejski kataster, 1824–1830", "Franciscan cadastre, 1824–1830")}</div>
          </div>
        </div>

        {/* pokritost */}
        <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6" role="status">
          {[
            { v: COVERAGE.housesTotal, si: "hiš 1825", en: "houses of 1825" },
            { v: COVERAGE.ownersTotal, si: "lastnikov", en: "owners" },
            { v: COVERAGE.archivalUnits, si: "arhivskih enot", en: "archival units" },
            { v: COVERAGE.archivalPages, si: "strani fonda", en: "pages in fond" },
            { v: `${COVERAGE.sheetsGeoreferenced}+${COVERAGE.sheetsGridApprox}`, si: "listi georef. / približno", en: "sheets georef. / approx." },
            { v: COVERAGE.buildingsVectorized, si: "objektov vektoriziranih", en: "objects vectorised" },
          ].map((s, i) => (
            <div key={i} className="rounded-lg border bg-card/60 p-3 text-center">
              <div className="font-serif text-2xl font-bold text-primary">{s.v}</div>
              <div className="text-xs text-muted-foreground">{t(s.si, s.en)}</div>
            </div>
          ))}
        </div>

        {/* iskanje */}
        <div className="relative mb-6">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" aria-hidden />
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={t(
                "Išči po hišni št., lastniku, parceli, viru, EŠD, muzejski št. …",
                "Search by house no., owner, parcel, source, EŠD, museum no. …",
              )}
              className="pl-9 pr-10"
              aria-label={t("Iskanje po Atlasu", "Atlas search")}
            />
            {query && (
              <button
                onClick={clearSearch}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                aria-label={t("Počisti iskanje", "Clear search")}
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          {hits.length > 0 && (
            <div className="absolute z-30 mt-1 max-h-80 w-full overflow-y-auto rounded-lg border bg-popover shadow-lg">
              {hits.map((h) => (
                <button
                  key={`${h.type}-${h.id}`}
                  onClick={() => {
                    setSelected(h);
                    setQuery(h.id);
                    if (h.type === "location" || h.type === "house" || h.type === "heritage") setTab("map");
                  }}
                  className="flex w-full items-start gap-2 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-accent"
                >
                  <span className="mt-0.5 shrink-0 text-muted-foreground">
                    {h.type === "house" ? <Home className="h-4 w-4" /> : h.type === "owner" ? <Users className="h-4 w-4" /> : h.type === "source" ? <Archive className="h-4 w-4" /> : <MapPin className="h-4 w-4" />}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium">{lang === "si" ? h.titleSi : h.titleEn}</span>
                    {h.detail && <span className="block truncate text-xs text-muted-foreground">{h.detail}</span>}
                  </span>
                  {h.status && (
                    <span className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold ${STATUS_STYLE[h.status] ?? ""}`}>
                      {h.status}
                    </span>
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* zavihki */}
        <div className="mb-6 flex flex-wrap gap-2" role="tablist" aria-label={t("Razdelki Atlasa", "Atlas sections")}>
          {(
            [
              ["map", <MapIcon key="i" className="h-4 w-4" />, "Zemljevid", "Map"],
              ["3d", <Boxes key="i3d" className="h-4 w-4" />, "3D vas", "3D village"],
              ["houses", <Home key="i" className="h-4 w-4" />, "Register hiš", "House register"],
              ["owners", <Users key="i" className="h-4 w-4" />, "Lastniki", "Owners"],
              ["parish", <BookOpen key="i" className="h-4 w-4" />, "Matrike 1669–1947", "Parish registers"],
              ["landuse", <Layers key="i" className="h-4 w-4" />, "Raba tal", "Land use"],
              ["sources", <Archive key="i" className="h-4 w-4" />, "Viri in dokazi", "Sources & evidence"],
              ["coverage", <Gauge key="i" className="h-4 w-4" />, "Pokritost", "Coverage"],
            ] as [Tab, React.ReactNode, string, string][]
          ).map(([id, icon, si, en]) => (
            <button
              key={id}
              role="tab"
              aria-selected={tab === id}
              onClick={() => setTab(id)}
              className={`inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-sm font-medium transition ${
                tab === id
                  ? "border-primary bg-primary text-primary-foreground"
                  : "border-border hover:border-primary/40 hover:bg-accent"
              }`}
            >
              {icon}
              {t(si, en)}
            </button>
          ))}
        </div>

        {/* ZEMLJEVID */}
        {tab === "map" && (
          <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
            <div className="min-w-0">
              <Canvas
                layers={layers}
                opacity={opacity}
                userFix={userFix}
                onSelect={select}
                focus={focus}
              />
              <div className="mt-3 flex flex-wrap items-center gap-x-5 gap-y-3 rounded-lg border bg-card/60 px-4 py-3">
                <div className="flex items-center gap-2">
                  <Layers className="h-4 w-4 text-primary" aria-hidden />
                  <span className="text-sm font-medium">{t("Sloji", "Layers")}</span>
                </div>
                {(
                  [
                    ["a01", t("List A01", "Sheet A01")],
                    ["a02", t("List A02", "Sheet A02")],
                    ["a03", t("List A03 (±50 m)", "Sheet A03 (±50 m)")],
                    ["a04", t("List A04 (±40 m)", "Sheet A04 (±40 m)")],
                    ["a05", t("List A05 (±40 m)", "Sheet A05 (±40 m)")],
                    ["buildings", t("Objekti ~1825", "Buildings ~1825")],
                    ["landuse", t("Raba tal ~1825", "Land use ~1825")],
                    ["heritage", t("EŠD register", "EŠD register")],
                    ["vintage", t("Sepia (danes)", "Sepia (today)")],
                  ] as [keyof AtlasLayers, string][]
                ).map(([key, label]) => (
                  <div key={key} className="flex items-center gap-2">
                    <Switch
                      id={`atlas-layer-${key}`}
                      checked={layers[key]}
                      onCheckedChange={(v) => setLayers((p) => ({ ...p, [key]: v }))}
                    />
                    <Label htmlFor={`atlas-layer-${key}`} className="text-xs">
                      {label}
                    </Label>
                  </div>
                ))}
                <div className="flex min-w-40 flex-1 items-center gap-3">
                  <span className="text-xs text-muted-foreground">{t("Prosojnost", "Opacity")}</span>
                  <Slider
                    value={[Math.round(opacity * 100)]}
                    min={0}
                    max={100}
                    step={5}
                    onValueChange={([v]) => setOpacity(v / 100)}
                    className="flex-1"
                    aria-label={t("Prosojnost katastrskih listov", "Opacity of cadastral sheets")}
                  />
                  <span className="w-9 text-right text-xs tabular-nums text-muted-foreground">
                    {Math.round(opacity * 100)}%
                  </span>
                </div>
              </div>
              <p className="mt-2 text-xs text-muted-foreground">
                {t(
                  "Listi A01 in A02: Arhiv Republike Slovenije, SI AS 176/N/N83, javno dostopno prek VAČ. Georeferenca: cerkev sv. Vida (±50–80 m), vas (±75–120 m) — status REVIEW. Objekti ~1825 so vektorizacija lista A02 (RECONSTRUCTED), ne izvirne meje parcel. Listi A03–A05 (P51, privzeto izklopljeni): slikovna prekrivka po P50 neatline georeferenci (±40–50 m); Leaflet ne podpira rotiranih prekrivk — odmik vogalov osne postavitve ≤ 19,3/20,0/20,0 m (dva vogala točna), del negotovosti lista; ob prekrivki črtkani neatline okvir s statusom.",
                  "Sheets A01 and A02: Archives of the Republic of Slovenia, SI AS 176/N/N83, publicly accessible via VAČ. Georeference: St. Vitus church (±50–80 m), village (±75–120 m) — REVIEW status. Buildings ~1825 are a vectorisation of sheet A02 (RECONSTRUCTED), not original parcel boundaries. Sheets A03–A05 (P51, default off): image overlay per the P50 neatline georeference (±40–50 m); Leaflet does not support rotated overlays — the corner deviation of the axis-aligned placement is ≤ 19.3/20.0/20.0 m (two corners exact), part of the sheet's uncertainty; a dashed neatline frame with the status accompanies each overlay.",
                )}
              </p>
            </div>

            {/* desni stolpec: izbrani objekt / dokazi */}
            <div className="min-w-0">
              {selected ? (
                <div className="rounded-xl border bg-card/70 p-4">
                  <div className="mb-3 flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <div className="text-xs uppercase tracking-wide text-muted-foreground">
                        {t("Izbrani objekt", "Selected object")}
                      </div>
                      <h3 className="font-serif text-lg font-semibold leading-snug">
                        {lang === "si" ? selected.titleSi : selected.titleEn}
                      </h3>
                    </div>
                    <button
                      onClick={() => setSelected(null)}
                      className="shrink-0 rounded-md p-1 text-muted-foreground hover:bg-accent"
                      aria-label={t("Zapri podrobnost", "Close details")}
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                  {selected.status && (
                    <span className={`mb-3 inline-block rounded px-2 py-0.5 text-xs font-semibold ${STATUS_STYLE[selected.status] ?? ""}`}>
                      {selected.status}
                    </span>
                  )}

                  {evidence ? (
                    <div className="space-y-4">
                      <div className="text-sm">
                        <div className="mb-1 flex items-center gap-1.5 font-medium">
                          <BookOpen className="h-3.5 w-3.5 text-primary" aria-hidden />
                          {t("Trditev", "Claim")}
                        </div>
                        <p className="text-muted-foreground">{lang === "si" ? evidence.claim.textSi : evidence.claim.textEn}</p>
                      </div>
                      <div>
                        <div className="mb-2 flex items-center gap-1.5 text-sm font-medium">
                          <ShieldQuestion className="h-3.5 w-3.5 text-primary" aria-hidden />
                          {t("Dokazni viri", "Evidence sources")}
                        </div>
                        <ul className="space-y-2">
                          {evidence.evidence.map((ev, i) => (
                            <li key={i} className="rounded-lg border bg-background/60 p-2.5 text-xs">
                              <div className="font-medium">
                                {ev.source.code} — {lang === "si" ? ev.source.titleSi : ev.source.titleEn}
                              </div>
                              <div className="mt-0.5 text-muted-foreground">
                                {ev.locatorSi} · {ev.kind}
                              </div>
                              {ev.source.vacUrl && (
                                <a
                                  href={ev.source.vacUrl}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="mt-1 inline-flex items-center gap-1 text-primary hover:underline"
                                >
                                  {t("Odpri v arhivu VAČ", "Open in the VAČ archive")}
                                  <ExternalLink className="h-3 w-3" aria-hidden />
                                </a>
                              )}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div className="rounded-lg border bg-secondary/40 p-3 text-xs">
                        <div className="mb-1 font-medium">{t("Povezave", "Relations")}</div>
                        <dl className="space-y-1 text-muted-foreground">
                          <div className="flex gap-2">
                            <dt className="w-20 shrink-0">{t("Lastnik", "Owner")}</dt>
                            <dd>{evidence.relations.owner?.name ?? "—"}</dd>
                          </div>
                          <div className="flex gap-2">
                            <dt className="w-20 shrink-0">{t("Parcele", "Parcels")}</dt>
                            <dd>{evidence.relations.parcels ?? "—"}</dd>
                          </div>
                          <div className="flex gap-2">
                            <dt className="w-20 shrink-0">{t("Geometrija", "Geometry")}</dt>
                            <dd>
                              {evidence.relations.geometry.status} — {evidence.relations.geometry.noteSi}
                            </dd>
                          </div>
                        </dl>
                      </div>
                      {evidence.relations.museum && (
                        <Button
                          onClick={() => {
                            const slug = evidence.relations.museum === "MVG-002"
                              ? "sveti-vid"
                              : evidence.relations.museum === "MVG-010"
                                ? "niko-zupanic"
                                : "griblje-vas";
                            onOpenMuseum(slug);
                          }}
                          variant="outline"
                          className="w-full"
                        >
                          <ExternalLink className="mr-2 h-4 w-4" aria-hidden />
                          {t(`Odpri muzejski zapis ${evidence.relations.museum}`, `Open museum record ${evidence.relations.museum}`)}
                        </Button>
                      )}
                    </div>
                  ) : selected.type === "source" ? (
                    <SourceCard source={ATLAS_SOURCES.find((s) => s.id === selected.id)!} compact />
                  ) : (
                    <div className="text-sm text-muted-foreground">
                      {t(
                        "Objekt iz vektorizacije lista — lokacija je rekonstrukt (RECONSTRUCTED). Dokumentirana pozicija: lista A02, točna izvorna pozicija na arhivskem listu.",
                        "A vectorised object — the location is a reconstruction (RECONSTRUCTED). Documented position: sheet A02, exact original position on the archival sheet.",
                      )}
                      <Button onClick={openSourceTab} variant="outline" className="mt-3 w-full">
                        <Archive className="mr-2 h-4 w-4" aria-hidden />
                        {t("Poglej vire", "View sources")}
                      </Button>
                    </div>
                  )}
                </div>
              ) : (
                <div className="rounded-xl border bg-card/70 p-4 text-sm text-muted-foreground">
                  <div className="mb-2 font-medium text-foreground">
                    {t("Dokazni vmesnik", "Evidence explorer")}
                  </div>
                  {t(
                    "Klikni objekt na zemljevidu ali rezultat iskanja in pokazala se bo celotna dokazna veriga: vir → trditev → dokaz → povezave.",
                    "Click an object on the map or a search result and the full evidence chain will be shown: source → claim → evidence → relations.",
                  )}
                  <ul className="mt-3 space-y-1.5 text-xs">
                    <li className="flex items-center gap-2">
                      <span className="inline-block h-2.5 w-2.5 rounded-full border border-[#9a5b2e] bg-[#c47a3d]/60" />
                      {t("objekt ~1825 (vektorizacija)", "building ~1825 (vectorised)")}
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="inline-block h-2.5 w-2.5 rounded-full bg-[#9a5b2e]" />
                      {t("cerkev sv. Vida (VERIFIED, EŠD 2122)", "St. Vitus church (VERIFIED, EŠD 2122)")}
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="inline-block h-2.5 w-2.5 rounded-full border border-dashed border-[#9a5b2e]" />
                      {t("območje vasi (APPROXIMATE)", "village area (APPROXIMATE)")}
                    </li>
                    {church && (
                      <li className="flex items-center gap-2">
                        <Flag className="h-3 w-3 text-primary" aria-hidden />
                        {t("EŠD register dediščine (sodoben)", "EŠD heritage register (modern)")}
                      </li>
                    )}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {/* REGISTER HIŠ */}
        {tab === "3d" && (
          <div>
            <h3 className="font-display text-lg font-semibold">
              {t("3D rekonstrukcija vasi — iz katastra v prostor", "3D village reconstruction — from cadastre into space")}
            </h3>
            <p className="mt-1 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              {t(
                "156 stavb k.o. Grüble, vektorsko prepisanih z lista A02 Franciscejskega katastra, je izrisanih kot prostorske hiše z dvokapnico — na rabi tal ~1825 in ob Kolpi. P12: prizor je oživel z drevesi (gozdne cone + razpršena) in dimom iz dimnikov (interpretacija, jasno označena). Zavrtite, približajte, preklopite letnico — ali stopite vanjo z AR kamero na vašem stojišču (gumb spodaj desno).",
                "156 buildings of c.m. Grüble, vectorised from sheet A02 of the Franciscean cadastre, are drawn as spatial houses with gable roofs — on the ~1825 land use and by the Kolpa. P12: the scene now lives — trees (forest zones + scattered) and chimney smoke (interpretation, clearly labelled). Rotate, zoom, switch the year — or step inside with the AR camera at your standing point (button below right).",
              )}
            </p>
            <div className="mt-4">
              <VillageViewer />
            </div>
          </div>
        )}

        {tab === "houses" && (
          <div>
            <div className="mb-4 flex flex-wrap items-center gap-3">
              <div className="relative w-full max-w-xs">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" aria-hidden />
                <Input
                  value={houseFilter}
                  onChange={(e) => {
                    setHouseFilter(e.target.value);
                    setPage(0);
                  }}
                  placeholder={t("Filtriraj hiše (številka/lastnik)", "Filter houses (number/owner)")}
                  className="pl-9"
                />
              </div>
              <span className="text-sm text-muted-foreground">
                {filteredHouses.length} {t("hiš", "houses")} · {PARCELS.length} {t("parcelnih vrstic", "parcel rows")}
              </span>
            </div>
            <div className="overflow-hidden rounded-xl border">
              <table className="w-full text-sm">
                <thead className="bg-secondary/60 text-left text-xs uppercase tracking-wide text-muted-foreground">
                  <tr>
                    <th className="px-3 py-2">{t("Hiša 1825", "House 1825")}</th>
                    <th className="px-3 py-2">{t("Lastnik (prepis, REVIEW)", "Owner (transcription, REVIEW)")}</th>
                    <th className="hidden px-3 py-2 sm:table-cell">{t("Parcelni sklici", "Parcel refs")}</th>
                    <th className="hidden px-3 py-2 md:table-cell">{t("Vir", "Source")}</th>
                    <th className="px-3 py-2 text-right">{t("Status", "Status")}</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {paged.map((h) => (
                    <tr key={h.id} className="hover:bg-accent/40">
                      <td className="px-3 py-2 font-medium">{h.no}</td>
                      <td className="px-3 py-2">
                        {h.owner}
                        {h.ownerModernGuess && (
                          <span className="ml-1 text-xs text-muted-foreground">({h.ownerModernGuess})</span>
                        )}
                        {h.paleo && (
                          <span
                            title={h.paleo}
                            className="ml-1.5 cursor-help rounded bg-primary/15 px-1 py-0.5 align-middle font-mono text-[9px] font-bold text-primary"
                          >
                            P3
                          </span>
                        )}
                      </td>
                      <td className="hidden px-3 py-2 text-xs text-muted-foreground sm:table-cell">{h.parcelRefs ?? "—"}</td>
                      <td className="hidden px-3 py-2 text-xs text-muted-foreground md:table-cell">N083PT str. {h.sourcePage}</td>
                      <td className="px-3 py-2 text-right">
                        <span className={`rounded px-1.5 py-0.5 text-[10px] font-semibold ${STATUS_STYLE[h.status]}`}>
                          {h.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {pages > 1 && (
              <div className="mt-3 flex items-center justify-center gap-3">
                <Button variant="outline" size="sm" onClick={() => setPage((p) => Math.max(0, p - 1))} disabled={page === 0}>
                  <ChevronLeft className="h-4 w-4" aria-hidden />
                  {t("Nazaj", "Back")}
                </Button>
                <span className="text-sm text-muted-foreground">
                  {page + 1} / {pages}
                </span>
                <Button variant="outline" size="sm" onClick={() => setPage((p) => Math.min(pages - 1, p + 1))} disabled={page >= pages - 1}>
                  {t("Naprej", "Next")}
                  <ChevronRight className="h-4 w-4" aria-hidden />
                </Button>
              </div>
            )}
            <p className="mt-3 text-xs text-muted-foreground">
              {t(
                "Vsi vnosi so pomožen prepis nemškega rokopisa (Kurrent) iz Protokola stavbnih parcel (N083PT, str. 3–7) in čakajo paleografski pregled. Prepis posamezne hiše na arhivskem listu (natančna geometrija) je status TO_COLLECT.",
                "All entries are a machine-assisted transcription of the German Kurrent manuscript from the building-parcel protocol (N083PT, pp. 3–7) awaiting palaeographic review. Mapping an individual house onto the archival sheet (precise geometry) has TO_COLLECT status.",
              )}
            </p>
          </div>
        )}

        {/* LASTNIKI */}
        {tab === "owners" && (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {ATLAS_OWNERS.map((o) => (
              <div key={o.id} className="rounded-xl border bg-card/60 p-4">
                <div className="flex items-start justify-between gap-2">
                  <div className="font-medium">{o.nameAsWritten}</div>
                  <span className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold ${STATUS_STYLE[o.status]}`}>
                    {o.status}
                  </span>
                </div>
                {o.modernGuess && <div className="text-xs text-muted-foreground">≈ {o.modernGuess}</div>}
                <div className="mt-2 text-xs">
                  <span className="text-muted-foreground">{t("Hiše:", "Houses:")}</span>{" "}
                  <span className="font-medium">{o.houseRefs.join(", ")}</span>
                </div>
                {o.puaRef && (
                  <div className="mt-1 text-xs text-muted-foreground">
                    {t("potrjeno v", "confirmed in")} PUA ({o.puaRef})
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* MATRIKE (issue #6) */}
        {tab === "parish" && <ParishTab />}

        {/* RABA TAL (issue #7) */}
        {tab === "landuse" && <LandUseTab />}

        {/* VIRI */}
        {tab === "sources" && (
          <div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {ATLAS_SOURCES.map((s) => (
                <SourceCard key={s.id} source={s} />
              ))}
            </div>
            <div className="mt-6 rounded-xl border bg-card/60 p-4">
              <h3 className="mb-3 flex items-center gap-2 font-serif text-lg font-semibold">
                <Eye className="h-4 w-4 text-primary" aria-hidden />
                {t("Georeferenca listov", "Sheet georeference")}
              </h3>
              <div className="grid gap-4 sm:grid-cols-2">
                {SHEET_GEOREFS.map((g) => (
                  <div key={g.id} className="rounded-lg border bg-background/60 p-3 text-xs">
                    <div className="font-medium">
                      {t("List", "Sheet")} {g.sheet} · {g.pixels.width}×{g.pixels.height} px · ~{g.scaleMPerPixel} m/px
                    </div>
                    <div className="mt-1 text-muted-foreground">{lang === "si" ? g.methodSi : g.methodEn}</div>
                    <div className="mt-1 text-muted-foreground">
                      {lang === "si" ? g.accuracySi : g.accuracyEn}
                    </div>
                    <div className="mt-1 text-muted-foreground">
                      {t("Kontrolne točke", "Control points")}: {g.controlPoints.map((c) => c.fromSi).join(" · ")}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* POKRITOST */}
        {tab === "coverage" && (
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-xl border bg-card/60 p-5">
              <h3 className="mb-4 flex items-center gap-2 font-serif text-lg font-semibold">
                <Gauge className="h-4 w-4 text-primary" aria-hidden />
                {t("Pokritost podatkov", "Data coverage")}
              </h3>
              <dl className="space-y-2 text-sm">
                {[
                  [t("Identificirane hiše ~1825", "Identified houses ~1825"), `${COVERAGE.housesTotal}`],
                  [t("… z lastnikom", "… with an owner"), `${COVERAGE.housesWithOwner}`],
                  [t("… z natančno geometrijo", "… with precise geometry"), `${COVERAGE.housesWithGeometry} (${t("156 stavb ima geometrijo, a brez dokazane hišne št.", "156 buildings have geometry, without proven house numbers")})`],
                  [t("Lastniki (različni)", "Distinct owners"), `${COVERAGE.ownersTotal}`],
                  [t("… navzkrižno potrjeni (PT+PUA)", "… cross-checked (PT+PUA)"), `${COVERAGE.ownersCrossChecked}`],
                  [t("Vrstic s parcelnimi sklici", "Rows with parcel references"), `${COVERAGE.parcelsReferenced}`],
                  [t("Katastrski listi: validirana georeferenca / okvirna umestitev", "Cadastral sheets: validated georeference / approximate placement"), `${COVERAGE.sheetsGeoreferenced} / ${COVERAGE.sheetsGridApprox} (od ${COVERAGE.sheetsTotal})`],
                  [t("Vektoriziranih objektov", "Vectorised objects"), `${COVERAGE.buildingsVectorized} (RECONSTRUCTED)`],
                ].map(([k, v], i) => (
                  <div key={i} className="flex items-center justify-between border-b pb-2 last:border-0">
                    <dt className="text-muted-foreground">{k}</dt>
                    <dd className="font-semibold tabular-nums">{v}</dd>
                  </div>
                ))}
              </dl>
              <div className="mt-4">
                <div className="mb-2 text-sm font-medium">{t("Legenda statusov", "Status legend")}</div>
                <div className="flex flex-wrap gap-1.5">
                  {Object.entries(COVERAGE.statusesSi).map(([s, si]) => (
                    <span key={s} title={si} className={`rounded px-2 py-0.5 text-[10px] font-semibold ${STATUS_STYLE[s] ?? ""}`}>
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <div className="rounded-xl border bg-card/60 p-5 lg:col-span-2">
              <h3 className="mb-1 flex items-center gap-2 font-serif text-lg font-semibold">
                <Archive className="h-4 w-4 text-primary" aria-hidden />
                {t("Inventar arhivskih enot N83 (issue #4)", "Inventory of the N83 archival units (issue #4)")}
              </h3>
              <p className="mb-4 max-w-3xl text-xs leading-relaxed text-muted-foreground">
                {t(INVENTORY.noteSi, INVENTORY.noteEn)}
              </p>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[720px] text-left text-xs">
                  <thead>
                    <tr className="border-b text-muted-foreground">
                      <th className="py-2 pr-3 font-medium">{t("Enota", "Unit")}</th>
                      <th className="py-2 pr-3 font-medium">{t("Strani (vir)", "Pages (source)")}</th>
                      <th className="py-2 pr-3 font-medium">{t("Prebrane", "Read")}</th>
                      <th className="py-2 pr-3 font-medium">{t("Odprte", "Open")}</th>
                      <th className="py-2 pr-3 font-medium">{t("Strukturirane entitete", "Structured entities")}</th>
                      <th className="py-2 pr-3 font-medium">{t("Navzkrižno", "Cross-chk")}</th>
                      <th className="py-2 pr-3 font-medium">{t("Prostorsko", "Spatial")}</th>
                      <th className="py-2 font-medium">{t("Odprto — razlog", "Open — reason")}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {INVENTORY.units.map((u) => (
                      <tr key={u.code} className="border-b last:border-0 align-top">
                        <td className="py-2 pr-3">
                          <span className="font-mono text-primary">{u.code}</span>
                          <div className="text-[10px] text-muted-foreground">
                            {u.kind === "graphic-sheet" ? t("grafični list", "graphic sheet") : t("spisovna enota", "written series")}
                            {u.georefStatus === "GRID_APPROX" ? " · " + t("umesčen približno", "placed approximately") : ""}
                          </div>
                        </td>
                        <td className="py-2 pr-3 tabular-nums">{u.pagesDeclared ?? "—"}</td>
                        <td className="py-2 pr-3 tabular-nums">{u.pagesRead ?? "—"}</td>
                        <td className="py-2 pr-3 tabular-nums">
                          {u.pagesOpen != null && u.pagesOpen > 0 ? (
                            <span title={u.pagesOpenRangesSi ?? ""}>{u.pagesOpen}</span>
                          ) : (
                            <span className="text-emerald-700 dark:text-emerald-400">0</span>
                          )}
                        </td>
                        <td className="py-2 pr-3">
                          <span className="tabular-nums font-semibold">{u.structuredEntities}</span>
                          <div className="text-[10px] text-muted-foreground">{lang === "si" ? u.structuredModelSi : u.structuredModelEn}</div>
                        </td>
                        <td className="py-2 pr-3 tabular-nums">{u.crossChecked}</td>
                        <td className="py-2 pr-3 tabular-nums">{u.spatiallyLinked}</td>
                        <td className="py-2 text-muted-foreground">{lang === "si" ? u.openSi : u.openEn}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="mt-3 text-xs text-muted-foreground">
                {t(
                  `Skupaj: ${INVENTORY.totals.units} enot (${INVENTORY.totals.graphicSheets} grafičnih + ${INVENTORY.totals.writtenSeries} spisovnih), ${INVENTORY.totals.pagesRead}/${INVENTORY.totals.pagesDeclared} strani prebranih, ${INVENTORY.totals.pagesOpen} izrecno odprtih. PS kontrolna vsota: ${INVENTORY.psChecksum.buildingSites} stavbnih mest + ${INVENTORY.psChecksum.landParcels} parcel = ${INVENTORY.psChecksum.total}. Prostorsko povezanih entitet: ${INVENTORY.totals.spatiallyLinked} — povezava hiša↔stavba zahteva dokaz, ne ista številka.`,
                  `Totals: ${INVENTORY.totals.units} units (${INVENTORY.totals.graphicSheets} graphic + ${INVENTORY.totals.writtenSeries} written), ${INVENTORY.totals.pagesRead}/${INVENTORY.totals.pagesDeclared} pages read, ${INVENTORY.totals.pagesOpen} explicitly open. PS checksum: ${INVENTORY.psChecksum.buildingSites} building sites + ${INVENTORY.psChecksum.landParcels} parcels = ${INVENTORY.psChecksum.total}. Spatially linked entities: ${INVENTORY.totals.spatiallyLinked} — a house↔building link requires evidence, not a shared number.`,
                )}
              </p>
            </div>
            <div className="rounded-xl border bg-card/60 p-5">
              <h3 className="mb-4 flex items-center gap-2 font-serif text-lg font-semibold">
                <EyeOff className="h-4 w-4 text-primary" aria-hidden />
                {t("Negativni rezultati (provenienca)", "Negative results (provenance)")}
              </h3>
              <ul className="space-y-3 text-sm">
                {NEGATIVE_RESULTS.map((n) => (
                  <li key={n.id} className="rounded-lg border bg-background/60 p-3">
                    <div className="flex items-start justify-between gap-2">
                      <div className="font-medium">{lang === "si" ? n.whatSi : n.whatEn}</div>
                      <span className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold ${STATUS_STYLE[n.status] ?? ""}`}>
                        {n.status}
                      </span>
                    </div>
                    <p className="mt-1 text-xs text-muted-foreground">{lang === "si" ? n.detailSi : n.detailEn}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

function SourceCard({
  source,
  compact,
}: {
  source: (typeof ATLAS_SOURCES)[number];
  compact?: boolean;
}) {
  const { lang, t } = useLang();
  return (
    <div className={`rounded-xl border bg-card/60 ${compact ? "p-3" : "p-4"}`}>
      {source.thumb && (
         
        <img
          src={source.thumb}
          alt={lang === "si" ? source.titleSi : source.titleEn}
          className={`mb-3 w-full rounded-lg border object-cover ${compact ? "max-h-32" : "h-36"}`}
          loading="lazy"
        />
      )}
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 font-medium leading-snug">
          <span className="text-xs font-mono text-primary">{source.code}</span>
          <div>{lang === "si" ? source.titleSi : source.titleEn}</div>
        </div>
        {source.georefStatus === "GEOREFERENCED" && (
          <span className="shrink-0 rounded bg-emerald-100 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100" title={t("validirana georeferenca (kontrolne točke)", "validated georeference (control points)")}>
            georef ±
          </span>
        )}
        {source.georefStatus === "GRID_APPROX" && (
          <span className="shrink-0 rounded bg-amber-100 px-1.5 py-0.5 text-[10px] font-semibold text-amber-900 dark:bg-amber-900/60 dark:text-amber-100" title={t("okvirna umestitev po sekcijski mreži (±200–400 m), ni afina", "approximate placement by the section grid (±200–400 m), not an affine")}>
            približno ±
          </span>
        )}
      </div>
      <div className="mt-1 text-xs text-muted-foreground">
        {source.archive} · {source.pages ? `${source.pages} ${t("strani", "pages")}` : t("list", "sheet")}
        {source.yearFrom ? ` · ${source.yearFrom}${source.yearTo && source.yearTo !== source.yearFrom ? `–${source.yearTo}` : ""}` : ""}
      </div>
      {(source.noteSi || compact) && (
        <p className="mt-2 text-xs text-muted-foreground">
          {compact ? (lang === "si" ? source.noteSi ?? "" : source.noteEn ?? "") : (lang === "si" ? source.noteSi ?? "" : source.noteEn ?? "")}
        </p>
      )}
      <div className="mt-2 flex items-center justify-between text-xs">
        <span className="text-muted-foreground">{source.licenceSi}</span>
        {source.vacUrl && (
          <a
            href={source.vacUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-primary hover:underline"
          >
            {t("VAČ", "VAČ")}
            <ExternalLink className="h-3 w-3" aria-hidden />
          </a>
        )}
      </div>
    </div>
  );
}

/* ——— MATRIKE 1669–1947 (issue #6): brskalnik knjig + hišne zgodbe ——— */

function ParishTab() {
  const { lang, t } = useLang();
  const [type, setType] = useState<"all" | "baptism" | "marriage" | "death">("all");

  const stats = parishStats();
  const books = useMemo(
    () => PARISH_BOOKS.filter((b) => type === "all" || b.type === type),
    [type],
  );
  const vitalsByHouse = useMemo(() => {
    const m = new Map<string, HouseVital[]>();
    for (const v of HOUSE_VITALS) {
      const arr = m.get(v.houseNo) ?? [];
      arr.push(v);
      m.set(v.houseNo, arr);
    }
    return m;
  }, []);

  const typeLabel: Record<"all" | "baptism" | "marriage" | "death", string> = {
    all: t("Vse knjige", "All books"),
    baptism: t("Krstne", "Baptisms"),
    marriage: t("Poročne", "Marriages"),
    death: t("Mrliške", "Deaths"),
  };
  const typeName: Record<"baptism" | "marriage" | "death", string> = {
    baptism: t("Krstna knjiga", "Baptismal register"),
    marriage: t("Poročna knjiga", "Marriage register"),
    death: t("Mrliška knjiga", "Death register"),
  };

  return (
    <div className="space-y-6">
      {/* župnija — info */}
      <div className="rounded-xl border bg-card/60 p-5">
        <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
          <BookOpen className="h-4 w-4 text-primary" aria-hidden />
          {t("Matične knjige župnije Podzemelj", "Parish registers of Podzemelj")}
        </h3>
        <p className="mt-2 text-sm text-muted-foreground">
          {t(
            `Griblje so bile v zgodovinskem matičnem območju župnije Podzemelj (${PARISH.patronSi}); sv. Vid v Gribljah je njena 3. podružnica. Nadškofijski arhiv Ljubljana je digitaliziral in javno objavil ${stats.books} zvezkov (${stats.period}) — krstne, poročne in mrliške vpise Gribeljcev.`,
            `Griblje lay in the historical parish territory of Podzemelj (${PARISH.patronEn}); St. Vitus in Griblje is its 3rd filial church. The Archdiocesan Archive of Ljubljana digitised and published ${stats.books} volumes (${stats.period}) — baptisms, marriages and deaths of the people of Griblje.`,
          )}
        </p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="rounded-full border px-3 py-1">{PARISH.archiveSi}</span>
          <span className="rounded-full border px-3 py-1">
            {stats.byType.baptism} {t("krstnih", "baptismal")} · {stats.byType.marriage} {t("poročnih", "marriage")} · {stats.byType.death} {t("mrliških", "death")}
          </span>
          <span className="rounded-full border px-3 py-1">
            {t("dostop", "access")}: {PARISH.accessedAt}
          </span>
          <a
            href={PARISH.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 rounded-full border border-primary/40 px-3 py-1 text-primary hover:bg-accent"
          >
            Matricula Online
            <ExternalLink className="h-3 w-3" aria-hidden />
          </a>
        </div>
      </div>

      {/* brskalnik knjig */}
      <div>
        <div className="mb-3 flex flex-wrap items-center gap-2" role="group" aria-label={t("Filter po vrsti knjige", "Filter by register type")}>
          {(["all", "baptism", "marriage", "death"] as const).map((k) => (
            <button
              key={k}
              role="radio"
              aria-checked={type === k}
              onClick={() => setType(k)}
              className={`rounded-full border px-4 py-1.5 text-sm font-medium transition ${
                type === k ? "border-primary bg-primary text-primary-foreground" : "border-border hover:border-primary/40 hover:bg-accent"
              }`}
            >
              {typeLabel[k]}
            </button>
          ))}
          <span className="ml-auto text-sm text-muted-foreground">
            {books.length} {t("zvezkov", "volumes")}
          </span>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {books.map((b) => (
            <a
              key={b.signature}
              href={b.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group rounded-xl border bg-card/60 p-4 transition hover:border-primary/40 hover:bg-accent"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <span className="text-xs font-mono text-primary">{b.signature}</span>
                  <div className="font-medium leading-snug">{typeName[b.type]}</div>
                </div>
                <ExternalLink className="h-3.5 w-3.5 shrink-0 text-muted-foreground group-hover:text-primary" aria-hidden />
              </div>
              <div className="mt-2 text-2xl font-semibold tabular-nums">
                {b.from}–{b.to}
              </div>
              <div className="mt-1 text-xs text-muted-foreground">
                {t(`${b.to - b.from} let vpisov · Matricula Online`, `${b.to - b.from} years of entries · Matricula Online`)}
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* hišne zgodbe */}
      <div className="rounded-xl border bg-card/60 p-5">
        <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
          <Home className="h-4 w-4 text-primary" aria-hidden />
          {t("Hišne zgodbe: matrike × register hiš 1825", "House stories: parish registers × 1825 house register")}
        </h3>
        <p className="mt-2 text-sm text-muted-foreground">
          {t(
            `Krstna knjiga 04105 vpisuje rojstva v Gribljih s hišnimi številkami — te se nanašajo na konskripcijske številke iz registra hiš (PT, 1825). Prepisov je doslej ${stats.vitalRecords} za ${stats.housesWithVitals} hišo; ostalih ${stats.housesTotal - stats.housesWithVitals} hiš čaka branje (TO_COLLECT).`,
            `Baptismal register 04105 records births in Griblje with house numbers — these refer to the conscription numbers of the 1825 house register (PT). ${stats.vitalRecords} entries transcribed so far for ${stats.housesWithVitals} house(s); the remaining ${stats.housesTotal - stats.housesWithVitals} await reading (TO_COLLECT).`,
          )}
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          {[...vitalsByHouse.entries()].map(([houseNo, vitals]) => {
            const story = getHouseStory(houseNo);
            if (!story) return null;
            return (
              <div key={houseNo} className="rounded-lg border bg-background/60 p-4">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="text-xs uppercase tracking-wide text-muted-foreground">
                      {t("Hiša št.", "House no.")} {houseNo}
                    </div>
                    <div className="font-medium">{story.house.owner}</div>
                    {story.ownerCrossRef?.puaRef && (
                      <div className="text-xs text-muted-foreground">
                        {t("potrjeno v", "confirmed in")} PUA ({story.ownerCrossRef.puaRef})
                      </div>
                    )}
                  </div>
                  <span className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold ${STATUS_STYLE.DOCUMENTED}`}>
                    {t("vpisi DOCUMENTED", "entries DOCUMENTED")}
                  </span>
                </div>
                <ul className="mt-3 space-y-2 text-sm">
                  {vitals.map((v) => (
                    <li key={`${v.year}-${v.scan}`} className="rounded border p-2">
                      <span className="font-semibold tabular-nums">{v.year}</span> —{" "}
                      {lang === "si" ? v.whatSi : v.whatEn}
                      <div className="mt-1 text-xs text-muted-foreground">
                        {t("knjiga", "book")} {v.bookSignature}
                        {v.scan != null ? ` · ${t("sken", "scan")} ${v.scan}` : ""}
                        {v.page != null ? ` · ${t("str.", "p.")} ${v.page}` : ""}
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
        <p className="mt-3 text-xs text-muted-foreground">
          {t(
            "Vir vseh vpisov: Matricula Online, Krstna knjiga 04105 (1886–1919) — Nadškofijski arhiv Ljubljana; transkribirano v zapisu sveti-vid. Priimki v Kurrentu so negotovi (REVIEW) in čakajo paleografski pregled.",
            "Source of all entries: Matricula Online, baptismal register 04105 (1886–1919) — Archdiocesan Archive of Ljubljana; transcribed in the sveti-vid record. Surnames in Kurrent script are uncertain (REVIEW) and await palaeographic review.",
          )}
        </p>
      </div>
    </div>
  );
}

/* ——— RABA TAL 1825 (issue #7): cone, posebnosti, zaselki ——— */

function LandUseTab() {
  const { lang, t } = useLang();

  return (
    <div className="space-y-6">
      {/* cone rabe tal */}
      <div className="rounded-xl border bg-card/60 p-5">
        <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
          <Layers className="h-4 w-4 text-primary" aria-hidden />
          {t("Raba tal ~1825 — kje so Gribeljci obdelovali", "Land use ~1825 — where the people of Griblje farmed")}
        </h3>
        <p className="mt-2 text-sm text-muted-foreground">
          {t(
            "Vzorci so razbrani iz katastrskih listov A01 in A02 (VLM analiza 2026-10-07) in georeference: reka Kolpa teče po vzhodnem robu, njivski mozaik s parcelnimi številkami obdaja vas, poplavne loke ležijo med jedrom vasi in reko, gozdni kompleks se pojavi na južnem robu lista A02. Vklopi plast »Raba tal ~1825« na zemljevidu za prikaz con.",
            "Patterns were read from sheets A01 and A02 (VLM analysis 2026-10-07) and the georeference: the Kolpa flows along the eastern edge, a field mosaic with parcel numbers surrounds the village, flood meadows lie between the village core and the river, and a forest complex appears on the southern edge of sheet A02. Turn on the »Land use ~1825« layer on the map to show the zones.",
          )}
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          {LANDUSE_ZONES.map((z) => (
            <div key={z.id} className="rounded-lg border bg-background/60 p-3">
              <div className="flex items-center gap-2">
                <span
                  className="inline-block h-3 w-3 shrink-0 rounded"
                  style={{ background: z.fillColor, border: `1.5px solid ${z.color}` }}
                  aria-hidden
                />
                <div className="font-medium leading-tight">{lang === "si" ? z.labelSi : z.labelEn}</div>
              </div>
              <p className="mt-2 text-xs text-muted-foreground">{lang === "si" ? z.noteSi : z.noteEn}</p>
              <p className="mt-2 text-[11px] text-muted-foreground">
                <span className="font-semibold">VLM:</span> {z.vlmHintSi}
              </p>
              <span className={`mt-2 inline-block rounded px-1.5 py-0.5 text-[10px] font-semibold ${STATUS_STYLE[z.status]}`}>
                {z.status} (±100–150 m)
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* krajevne posebnosti */}
      <div>
        <h3 className="mb-3 flex items-center gap-2 font-serif text-lg font-semibold">
          <MapPin className="h-4 w-4 text-primary" aria-hidden />
          {t("Gozd, lokva, rudna peč, studenci", "Forest, pond, iron rock, springs")}
        </h3>
        <div className="grid gap-3 sm:grid-cols-2">
          {LANDUSE_ENTITIES.map((e) => (
            <div key={e.id} className="rounded-xl border bg-card/60 p-4">
              <div className="flex items-start justify-between gap-2">
                <div className="font-medium">{lang === "si" ? e.labelSi : e.labelEn}</div>
                <span className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold ${STATUS_STYLE[e.status] ?? ""}`}>
                  {e.status === "DOCUMENTED" ? t("dokumentirano", "documented") : "TO_COLLECT"}
                </span>
              </div>
              <p className="mt-2 text-sm text-muted-foreground">{lang === "si" ? e.descriptionSi : e.descriptionEn}</p>
              {e.museumRef && (
                <div className="mt-2 text-xs text-primary">{e.museumRef}</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* zaselki */}
      <div>
        <h3 className="mb-3 flex items-center gap-2 font-serif text-lg font-semibold">
          <Flag className="h-4 w-4 text-primary" aria-hidden />
          {t("Zaselki: kje so živeli", "Hamlets: where they lived")}
        </h3>
        <p className="mb-3 text-sm text-muted-foreground">
          {t(
            "Griblje se razprostirajo v štirih zaselkih (Wikipedija in uradna stran KS Griblje). Konskripcijske hišne številke (1825) so zapisane v eno zaporedje po obhodu davkarja — katere hiše spadajo k kateremu zaselku, ni znano; domači pregled je vabljen.",
            "Griblje stretches across four hamlets (Wikipedia and the official KS Griblje page). The conscription house numbers (1825) were recorded in a single sequence following the tax collector's walk — which houses belong to which hamlet is unknown; local review is invited.",
          )}
        </p>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {HAMLETS.map((h) => (
            <div key={h.id} className="rounded-xl border bg-card/60 p-4">
              <div className="font-medium">{lang === "si" ? h.nameSi : h.nameEn}</div>
              <p className="mt-2 text-xs text-muted-foreground">{lang === "si" ? h.noteSi : h.noteEn}</p>
            </div>
          ))}
        </div>
      </div>

      {/* primerjava danes */}
      <div className="rounded-xl border bg-card/60 p-5">
        <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
          <Gauge className="h-4 w-4 text-primary" aria-hidden />
          {t("Kmetijska krajina: 1825 ↔ danes", "Agricultural landscape: 1825 ↔ today")}
        </h3>
        <dl className="mt-3 grid gap-3 text-sm sm:grid-cols-2">
          <div className="rounded-lg border bg-background/60 p-3">
            <dt className="font-medium">1825</dt>
            <dd className="mt-1 text-muted-foreground">
              {t(
                "Dolgotenhno kolonatsko njivsko gospodarstvo: ozki trakovi (Gewan) okoli vasi, poplavne loke ob Kolpi skupne vaške, travniki v jedru; gozd le na južnem robu; 80 hišnih parcel znotraj k.o.",
                "Strip-field agriculture: narrow Gewan strips around the village, common flood meadows along the Kolpa, meadows in the core; forest only on the southern edge; 80 building parcels within the municipality.",
              )}
            </dd>
          </div>
          <div className="rounded-lg border bg-background/60 p-3">
            <dt className="font-medium">{t("Danes", "Today")}</dt>
            <dd className="mt-1 text-muted-foreground">
              {t(
                "Po komasaciji in agromelioracijah 20. stoletja so majhna polja združena v večje bloke; ob Kolpi kopališče in izletišče; ribnik zahodno od vasi (MVG-016); vas ima 329 prebivalcev in je najbolj suh kraj Bela krajine.",
                "After 20th-century land consolidation and agro-melioration the small fields were merged into larger blocks; along the Kolpa there is now a bathing site; a pond lies west of the village (MVG-016); the village has 329 inhabitants and is the driest place in Bela krajina.",
              )}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
