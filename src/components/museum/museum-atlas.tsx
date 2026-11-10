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
import {
  BAPTISM_LINE_YEARS,
  BAPTISM_LINE_TOTALS,
  CROSS_YEAR_THREADS,
  PEZDIRC_PER_YEAR,
  PEZDIRC_TOTAL,
  X_OPEN_REMAINDERS,
} from "@/data/atlas/parish-synthesis";
import {
  FORENSIC_VERDICTS,
  H65_STATS,
  H69_ERAS,
  H69_TOTAL,
  MATHIAS_H65_SPAN,
  MATHIAS_H65_TOTAL,
  MILIC_FAMILY_TOTAL,
  MILIC_H69_OVERLAP,
  MILIC_PER_BOOK,
  PRIEST_CROSS,
} from "@/data/atlas/parish-forensics";
import {
  MARRIAGE_1885_BLOCKS,
  MARRIAGE_1885_GRIBLJE,
  MARRIAGE_1885_HOUSES,
  MARRIAGE_1885_TOTAL,
  MARRIAGE_1885_ZAP_SKIPPED,
  MARRIAGE_1885_XOPEN,
  PEZDIRC_1885,
  LEDERER_1885,
  BRINEC_1885,
  MARRIAGE_1885_MEJA,
  P84_CORRECTION,
  MARRIAGE_1885_OUT_OF_ORDER,
  PRIEST_1885,
  OLDEST_PAIR_1885,
  YOUNGEST_BRIDE_1885,
  MARRIAGE_1884_BLOCKS,
  MARRIAGE_1884_GRIBLJE,
  MARRIAGE_1884_HOUSES,
  MARRIAGE_1884_TOTAL,
  MARRIAGE_1884_XOPEN,
  MARRIAGE_1884_MEJA,
  MARRIAGE_1884_NUMBERING,
  PEZDIRC_1884_NIT,
  MILEK_1884_NIT,
  PRIEST_1884,
  OLDEST_PAIR_1884,
  MARRIAGE_1884_VILLAGE_DUELS,
  MARRIAGE_1883_BLOCKS,
  MARRIAGE_1883_GRIBLJE,
  MARRIAGE_1883_HOUSES,
  MARRIAGE_1883_TOTAL,
  MARRIAGE_1883_XOPEN,
  MARRIAGE_1883_MEJA,
  MARRIAGE_1883_NUMBERING,
  PEZDIRC_1883_NIT,
  MILEK_1883_KANDIDAT,
  PRIEST_1883,
  HROVALJ_1883_SIBLINGS,
  MARRIAGE_1883_VILLAGE_DUELS,
  MARRIAGE_1882_BLOCKS,
  MARRIAGE_1882_GRIBLJE,
  MARRIAGE_1882_HOUSES,
  MARRIAGE_1882_TOTAL,
  MARRIAGE_1882_XOPEN,
  MARRIAGE_1882_MEJA,
  MARRIAGE_1882_NUMBERING,
  PEZDIRC_1882_NIT,
  H1_1882_REKORD,
  PRIEST_1882,
  BRINC_1882_NIT,
  MARRIAGE_1882_VILLAGE_DUELS,
} from "@/data/atlas/parish-marriage-early";
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

/* P236: SINTEZA KRSTNE PREDZGODOVINE 04104 — časovnica 15 let (1871–1885 = 15/15!) */
function BaptismLineSynthesis() {
  const { t } = useLang();
  const [openYear, setOpenYear] = useState<number | null>(1871);
  const maxEntries = Math.max(...BAPTISM_LINE_YEARS.map((y) => y.entries));
  const maxPez = Math.max(...PEZDIRC_PER_YEAR.map((y) => y.count));

  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <Layers className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Krstna predzgodovina 04104: sinteza 15 let (1871–1885)",
          "The baptism prehistory 04104: a 15-year synthesis (1871–1885)",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t(
          `Knjiga »${BAPTISM_LINE_TOTALS.label}« (nalepek 1:1!) je s fazami P221–P235 dokumentirana od naslovnice do konca: ${BAPTISM_LINE_TOTALS.entries} vpisov, od tega ${BAPTISM_LINE_TOTALS.griblje} v Gribljih; meje let = ${BAPTISM_LINE_TOTALS.boundaryConfirmations}. potrditev invariante; restart-z1 v vseh 15 letih. Klikni stolpec za podrobnosti leta.`,
          `The book »${BAPTISM_LINE_TOTALS.label}« (a 1:1 sticker!) was fully documented by phases P221–P235, from the title page to the end: ${BAPTISM_LINE_TOTALS.entries} entries, ${BAPTISM_LINE_TOTALS.griblje} of them in Griblje; the year boundaries = the ${BAPTISM_LINE_TOTALS.boundaryConfirmations} invariant confirmations; a z1-restart in all 15 years. Click a column for the year's details.`,
        )}
      </p>

      {/* časovnica — 15 stolpcev */}
      <div className="mt-4 overflow-x-auto pb-1">
        <div
          className="flex min-w-[640px] items-end gap-1.5 sm:min-w-0"
          role="listbox"
          aria-label={t("Časovnica vpisov po letih", "Entries timeline by year")}
        >
          {[...BAPTISM_LINE_YEARS].reverse().map((y) => {
            const open = openYear === y.year;
            const h = Math.round((y.entries / maxEntries) * 100);
            const hg = Math.round((y.griblje / maxEntries) * 100);
            return (
              <button
                key={y.year}
                role="option"
                aria-selected={open}
                onClick={() => setOpenYear(open ? null : y.year)}
                className={`group flex flex-1 flex-col items-center gap-1 rounded-lg border px-1 py-2 transition ${
                  open ? "border-primary bg-accent" : "border-transparent hover:border-primary/30 hover:bg-accent/50"
                }`}
              >
                <span className="text-[11px] font-semibold tabular-nums text-foreground">{y.entries}</span>
                <span className="flex w-5 flex-col justify-end" style={{ height: 88 }} aria-hidden>
                  <span
                    className="w-full rounded-t-sm border border-primary/50 bg-primary/25"
                    style={{ height: `${h}%`, display: "flex", flexDirection: "column", justifyContent: "flex-end" }}
                  >
                    <span className="w-full rounded-t-sm bg-primary/70" style={{ height: `${(hg / h) * 100}%` }} />
                  </span>
                </span>
                <span className="text-[11px] font-medium tabular-nums">{y.year}</span>
                <span className="text-[9px] text-muted-foreground">{y.phase}</span>
              </button>
            );
          })}
        </div>
        <p className="mt-1 text-[10px] text-muted-foreground">
          {t(
            `polni stolpec = vpisi v knjigi · temnejši del = Griblje (${BAPTISM_LINE_YEARS.map((y) => y.griblje).join(" · ")})`,
            `full column = entries in the book · darker part = Griblje (${BAPTISM_LINE_YEARS.map((y) => y.griblje).join(" · ")})`,
          )}
        </p>
      </div>

      {/* podrobnosti izbranega leta */}
      {openYear != null &&
        (() => {
          const y = BAPTISM_LINE_YEARS.find((x) => x.year === openYear);
          if (!y) return null;
          return (
            <div key={y.year} className="mt-3 rounded-lg border bg-background/60 p-4">
              <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                <span className="font-display text-lg font-semibold tabular-nums">{y.year}</span>
                <Badge variant="outline" className="font-mono text-[10px]">{y.phase} · {y.progress}</Badge>
                <span className="text-sm text-muted-foreground">
                  {t(`${y.entries} vpisov · ${y.griblje} Griblje / ${y.houses} hiš`, `${y.entries} entries · ${y.griblje} Griblje / ${y.houses} houses`)}
                </span>
              </div>
              <dl className="mt-3 grid gap-x-6 gap-y-1.5 text-xs sm:grid-cols-2">
                <div>
                  <dt className="font-semibold text-muted-foreground">{t("okvir skenov", "scan window")}</dt>
                  <dd>{y.scans} ({y.scanCount}) · {y.foliation}</dd>
                </div>
                <div>
                  <dt className="font-semibold text-muted-foreground">{t("meja z naslednjim letom", "boundary with the next year")}</dt>
                  <dd>{y.boundaryNext}</dd>
                </div>
                <div>
                  <dt className="font-semibold text-muted-foreground">{t("restart-z1", "z1-restart")}</dt>
                  <dd>{y.restart}</dd>
                </div>
              </dl>
              <ul className="mt-3 space-y-1 text-xs">
                {y.highlights.map((hl) => (
                  <li key={hl} className="rounded border bg-card/60 px-2.5 py-1.5">{hl}</li>
                ))}
              </ul>
            </div>
          );
        })()}

      {/* PEZDIRC-continuum — mini grafikon */}
      <div className="mt-5 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("PEZDIRC-continuum", "The PEZDIRC continuum")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            ×{PEZDIRC_TOTAL} {t("vrstic / 15 let", "rows / 15 years")}
          </span>
        </h4>
        <div className="mt-2 flex items-end gap-1" aria-hidden>
          {[...PEZDIRC_PER_YEAR].reverse().map((p) => (
            <span key={p.year} className="flex flex-1 flex-col items-center gap-0.5">
              <span className="text-[9px] tabular-nums text-muted-foreground">{p.count}</span>
              <span
                className="w-full rounded-t-sm bg-primary/60"
                style={{ height: Math.max(4, Math.round((p.count / maxPez) * 56)) }}
              />
              <span className="text-[9px] tabular-nums text-muted-foreground">&rsquo;{String(p.year).slice(2)}</span>
            </span>
          ))}
        </div>
      </div>

      {/* križnoletne niti */}
      <div className="mt-5 grid gap-3 md:grid-cols-2">
        {CROSS_YEAR_THREADS.map((th) => (
          <div key={th.id} className="min-w-0 rounded-lg border bg-background/60 p-4">
            <h4 className="text-sm font-semibold">{t(th.nameSi, th.nameEn)}</h4>
            <p className="mt-1.5 text-xs text-muted-foreground [overflow-wrap:anywhere]">{t(th.summarySi, th.summaryEn)}</p>
            <p className="mt-2 text-xs [overflow-wrap:anywhere]">{t(th.detailSi, th.detailEn)}</p>
            {th.xOpen && (
              <p className="mt-2 rounded border border-amber-500/40 bg-amber-500/10 px-2 py-1 text-[11px] text-amber-900 dark:text-amber-100 [overflow-wrap:anywhere]">
                X-open: {t(th.xOpen, th.xOpen)}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* X-open preostanki */}
      <div className="mt-5">
        <h4 className="text-sm font-semibold">{t("X-open preostanki (P235-LEAD)", "X-open remainders (the P235-LEAD)")}</h4>
        <div className="mt-2 grid gap-2 md:grid-cols-3">
          {X_OPEN_REMAINDERS.map((x) => (
            <div key={x.id} className="rounded-lg border border-dashed p-3">
              <div className="text-xs font-semibold">{t(x.titleSi, x.titleEn)}</div>
              <p className="mt-1 text-[11px] text-muted-foreground">{t(x.bodySi, x.bodyEn)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function MarriageEarly1885() {
  const { t } = useLang();
  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <BookOpen className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Poročna predzgodovina 04455 (P238): leto 1885 = 1/13",
          "The marriage prehistory 04455 (P238): the year 1885 = 1/13",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t(
          `NOVA LINIJA (1873–1885, descending kot krstna 04104): skeni s56–s61 == Pag. 55–60 (pravilo Pag = sken−1 razširjeno na 55–66!), ${MARRIAGE_1885_TOTAL} vpisov leta 1885 — pisar je PRESKOČIL vpis 3 (zap-stolpec: 2, 4, 5, 6). Restart leta na s56 (vpis 1 = 25. januar), meja 1885/86 na s61 (vpis 22 = 22. november + restart 1886 na isti strani). Griblje: ${MARRIAGE_1885_GRIBLJE} porok (h58 × h34 · h60 · h32 · h71 · h29? · h26 · h13 × h23/28) + ${MARRIAGE_1885_XOPEN.length} X-open vas-dueli (h29/h15/h9).`,
          `A NEW LINE (1873–1885, descending like the baptism 04104): scans s56–s61 == Pag. 55–60 (the Pag = scan−1 rule extended to 55–66!), ${MARRIAGE_1885_TOTAL} entries of 1885 — the scribe SKIPPED entry 3 (the number column: 2, 4, 5, 6). The year restarts on s56 (entry 1 = Jan 25), the 1885/86 boundary on s61 (entry 22 = Nov 22 + the 1886 restart on the same page). Griblje: ${MARRIAGE_1885_GRIBLJE} marriages (h58 × h34 · h60 · h32 · h71 · h29? · h26 · h13 × h23/28) + ${MARRIAGE_1885_XOPEN.length} X-open village duels (h29/h15/h9).`,
        )}
      </p>

      {/* Griblje poroke 1885 — vrstni red blokov */}
      <div className="mt-4 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("Griblje poroke 1885 — vrstni red blokov", "The Griblje marriages 1885 — the block order")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            ×{MARRIAGE_1885_GRIBLJE}
          </span>
        </h4>
        <div className="mt-3 grid gap-2 sm:grid-cols-7">
          {MARRIAGE_1885_BLOCKS.map((h) => (
            <div key={h.houseNo + h.scan} className="rounded border bg-card/60 px-2 py-1.5 text-center">
              <div className="text-xs font-semibold tabular-nums">h{h.houseNo}</div>
              <div className="text-[9px] text-muted-foreground">s{h.scan} · Pag. {h.page}</div>
            </div>
          ))}
        </div>
        <p className="mt-1.5 text-[11px] font-mono text-muted-foreground">{MARRIAGE_1885_HOUSES.join(" → ")}</p>
        <p className="mt-2 text-[11px] text-muted-foreground">
          {t(
            `PEZDIRC ×${PEZDIRC_1885} (vpis 11 ženin 1:1 — continuum 04104 ×131 → 04455!) · BRINC/BRINEC ×${BRINEC_1885} blokov (mati roj. Brunc [~] + Georg Brinec h26 usnjar — P237-mreža širša!) · Lederer/usnjar ×${LEDERER_1885} (usnjarska veja vpisov 16–22).`,
            `PEZDIRC ×${PEZDIRC_1885} (entry 11 the groom 1:1 — the continuum 04104 ×131 → 04455!) · BRINC/BRINEC ×${BRINEC_1885} blocks (the mother née Brunc [~] + Georg Brinec h26 tanner — the P237 network wider!) · Lederer/tanner ×${LEDERER_1885} (the tanners' branch of entries 16–22).`,
          )}
        </p>
      </div>

      {/* anomalije */}
      <div className="mt-4 grid gap-3">
        <div className="rounded-lg border border-amber-500/40 bg-amber-500/10 p-4 text-amber-900 dark:text-amber-100">
          <h4 className="text-sm font-semibold">
            {t("Vpis 3 PRESKOČEN (zap 2, 4, 5, 6)", "Entry 3 SKIPPED (the number column 2, 4, 5, 6)")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(
              `${MARRIAGE_1885_TOTAL} številčenih vpisov — pisar je skočil od 2 na 4 (številka ${MARRIAGE_1885_ZAP_SKIPPED} ostala prazna) (s57, ultra-zoom zap-stolpec 1:1); datum izven vrsti: vpis 7 = 7. februar vpisan PO vpisih 5–6 (8. februar). Najstarejši par: ${OLDEST_PAIR_1885}; najmlajša nevesta: ${YOUNGEST_BRIDE_1885} let; duhovnik: ${PRIEST_1885}.`,
              `${MARRIAGE_1885_TOTAL} numbered entries — the scribe jumped from 2 to 4 (the number ${MARRIAGE_1885_ZAP_SKIPPED} left empty) (s57, the ultra-zoom number column 1:1); out of order: entry 7 = Feb 7 written AFTER entries 5–6 (Feb 8). The oldest pair: ${OLDEST_PAIR_1885}; the youngest bride: ${YOUNGEST_BRIDE_1885} y.; the priest: ${PRIEST_1885}.`,
            )}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">{t(MARRIAGE_1885_MEJA.restartSi, MARRIAGE_1885_MEJA.restartEn)} {t(MARRIAGE_1885_MEJA.tailSi, MARRIAGE_1885_MEJA.tailEn)} — {t(MARRIAGE_1885_OUT_OF_ORDER, MARRIAGE_1885_OUT_OF_ORDER)}.</p>
        </div>
        <div className="rounded-lg border border-dashed p-4">
          <h4 className="text-sm font-semibold">
            {t("X-open vas-dueli (pošteno ostajajo)", "X-open village duels (honestly remain)")}
          </h4>
          <p className="mt-1.5 text-xs text-muted-foreground">
            {t(
              `${MARRIAGE_1885_XOPEN.join(" · ")} — vpisi 11/12/13: »½-Gütl-Gern/Glob«-zapisi vs GRIBLJE (stan ≠ hiša!); hiša neveste vpisa 22: 23-vs-28-duel; veliko leto na s61: »1 8 8 6« vs krop-»1883«-misread (sidro P84: vpis 1 = 24. 1. 1886 1:1). ${P84_CORRECTION}.`,
              `${MARRIAGE_1885_XOPEN.join(" · ")} — entries 11/12/13: the »½-Gütl-Gern/Glob« readings vs GRIBLJE (a status ≠ a house!); the bride's house of entry 22: the 23-vs-28 duel; the big year on s61: »1 8 8 6« vs the crop-»1883«-misread (the P84 anchor: entry 1 = Jan 24, 1886 1:1). ${P84_CORRECTION}.`,
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

function MarriageEarly1882() {
  const { t } = useLang();
  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <BookOpen className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Poročna predzgodovina 04455 (P241): leto 1882 = 4/13",
          "The marriage prehistory 04455 (P241): the year 1882 = 4/13",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t(
          `4/13 poročne predzgodovine (1873–1885): skeni s45–s50, ${MARRIAGE_1882_TOTAL} vpisov leta 1882 — BREZ preskokov (4. leto zapored!-kontrast-1885-vpis-3!). Restart leta: VELIKA-glava-'1882'-PRED-vrstico-1 (NOVA-4.-mejna-varianta — ni v glavi strani!). P240-napoved (h36-predistopna-nit) IZPOLNJENA 1:1.`,
          `4/13 of the marriage prehistory (1873–1885): scans s45–s50, ${MARRIAGE_1882_TOTAL} entries of 1882 — NO skips (the 4th year in a row!-in-contrast-to-the-1885-entry-3!). The year restart: the-BIG-'1882'-heading-BEFORE-row-1 (a NEW 4th boundary variant — not in the page head!). The P240-forecast (the-h36-pre-stop-thread) FULFILLED 1:1.`,
        )}
      </p>

      {/* Griblje poroke 1882 — vrstni red blokov */}
      <div className="mt-4 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("Griblje poroke 1882 — vrstni red blokov", "The Griblje marriages 1882 — the block order")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            ×{MARRIAGE_1882_GRIBLJE}
          </span>
        </h4>
        <div className="mt-3 grid gap-2 sm:grid-cols-4">
          {MARRIAGE_1882_BLOCKS.map((h) => (
            <div key={h.houseNo + h.scan} className="rounded border bg-card/60 px-2 py-1.5 text-center">
              <div className="text-xs font-semibold tabular-nums">h{h.houseNo}</div>
              <div className="text-[9px] text-muted-foreground">s{h.scan} · Pag. {h.page}</div>
            </div>
          ))}
        </div>
        <p className="mt-1.5 text-[11px] font-mono text-muted-foreground">{MARRIAGE_1882_HOUSES.join(" → ")}</p>
        <p className="mt-2 text-[11px] text-muted-foreground">
          {t(
            `${PEZDIRC_1882_NIT} ${BRINC_1882_NIT}.`,
            `${PEZDIRC_1882_NIT} ${BRINC_1882_NIT}.`,
          )}
        </p>
      </div>

      {/* anomalije */}
      <div className="mt-4 grid gap-3">
        <div className="rounded-lg border border-emerald-600/40 bg-emerald-600/10 p-4 text-emerald-900 dark:text-emerald-100">
          <h4 className="text-sm font-semibold">
            {t("h1 = najnižja hiša s poročnim blokom kadarkoli!", "h1 = the lowest house with a marriage block ever!")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(
              `Vpis 23 (12. november 1882): ženin Nicolaus LESIRO [~Lesko-DUEL], GRIBLJE 1 × Katharina ŠKRCE [~] GRIBLJE 10 — POLNI ×2! ${H1_1882_REKORD}.`,
              `Entry 23 (Nov 12, 1882): the groom Nicolaus LESIRO [~Lesko-DUEL], GRIBLJE 1 × Katharina ŠKRCE [~] GRIBLJE 10 — FULL ×2! ${H1_1882_REKORD}.`,
            )}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">
            {t(MARRIAGE_1882_MEJA.restartSi, MARRIAGE_1882_MEJA.restartEn)} · {t(MARRIAGE_1882_MEJA.boundarySi, MARRIAGE_1882_MEJA.boundaryEn)} · {t(MARRIAGE_1882_NUMBERING, MARRIAGE_1882_NUMBERING)} · {t(PRIEST_1882, PRIEST_1882)}
          </p>
        </div>
        <div className="rounded-lg border border-dashed p-4">
          <h4 className="text-sm font-semibold">
            {t("X-open dueli (pošteno ostajajo)", "The X-open duels (honestly remain)")}
          </h4>
          <p className="mt-1.5 text-xs text-muted-foreground">
            {t(
              `${MARRIAGE_1882_XOPEN.join(" · ")} — v14: 3-vasni-duel »Gradac 5 / Griblje 2 / Lette 40«! Vas-dueli: ${MARRIAGE_1882_VILLAGE_DUELS.join(" · ")}. Foliacija: s45-'93/94'-[~X-OPEN] — ne-ujema-s-'pag-=-sken−1'!`,
              `${MARRIAGE_1882_XOPEN.join(" · ")} — v14: the-3-village-duel »Gradac 5 / Griblje 2 / Lette 40«! Village duels: ${MARRIAGE_1882_VILLAGE_DUELS.join(" · ")}. The foliation: s45-'93/94'-[~X-OPEN] — does-not-match-'pag-=-sken−1'!`,
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

function MarriageEarly1883() {
  const { t } = useLang();
  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <BookOpen className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Poročna predzgodovina 04455 (P240): leto 1883 = 3/13",
          "The marriage prehistory 04455 (P240): the year 1883 = 3/13",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t(
          `3/13 poročne predzgodovine (1873–1885): skeni s50–s52, ${MARRIAGE_1883_TOTAL} vpisov leta 1883 — BREZ preskokov (3. leto zapored!). Restart leta na s50-DNO (vpis 1 = 21. januar, ženin Jovan CRNIČ; števke »1 8 8 3.« razporejene črez stolpce!), meja 1882/83 = s50-sredina (tail-1882 = vpisi 24–26!), meja 1883/84 = s52→s53 (P239 1:1). Številčenje: s50 = restart-1 · s51 = 2–7 (nodat-ultra-zoom: »prva je 2., ne 1.!«) · s52 = 8–12. Griblje: ${MARRIAGE_1883_GRIBLJE} poroki (h13 · h2!) + ${MARRIAGE_1883_XOPEN.length} X-open kandidat.`,
          `3/13 of the marriage prehistory (1873–1885): scans s50–s52, ${MARRIAGE_1883_TOTAL} entries of 1883 — NO skips (the 3rd year in a row!). The year restarts at the s50-BOTTOM (entry 1 = Jan 21, groom Jovan CRNIČ; the digits »1 8 8 3.« spread across the columns!), the 1882/83 boundary = s50-middle (the 1882 tail = entries 24–26!), the 1883/84 boundary = s52→s53 (P239 1:1). The numbering: s50 = restart-1 · s51 = 2–7 (the nodat-ultra-zoom: »the first is 2., not 1.!«) · s52 = 8–12. Griblje: ${MARRIAGE_1883_GRIBLJE} marriages (h13 · h2!) + ${MARRIAGE_1883_XOPEN.length} X-open candidate.`,
        )}
      </p>

      {/* Griblje poroke 1883 — vrstni red blokov */}
      <div className="mt-4 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("Griblje poroke 1883 — vrstni red blokov", "The Griblje marriages 1883 — the block order")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            ×{MARRIAGE_1883_GRIBLJE}
          </span>
        </h4>
        <div className="mt-3 grid gap-2 sm:grid-cols-2">
          {MARRIAGE_1883_BLOCKS.map((h) => (
            <div key={h.houseNo + h.scan} className="rounded border bg-card/60 px-2 py-1.5 text-center">
              <div className="text-xs font-semibold tabular-nums">h{h.houseNo}</div>
              <div className="text-[9px] text-muted-foreground">s{h.scan} · Pag. {h.page}</div>
            </div>
          ))}
        </div>
        <p className="mt-1.5 text-[11px] font-mono text-muted-foreground">{MARRIAGE_1883_HOUSES.join(" → ")}</p>
        <p className="mt-2 text-[11px] text-muted-foreground">
          {t(
            `${PEZDIRC_1883_NIT} ${MILEK_1883_KANDIDAT}.`,
            `${PEZDIRC_1883_NIT} ${MILEK_1883_KANDIDAT}.`,
          )}
        </p>
      </div>

      {/* anomalije */}
      <div className="mt-4 grid gap-3">
        <div className="rounded-lg border border-emerald-600/40 bg-emerald-600/10 p-4 text-emerald-900 dark:text-emerald-100">
          <h4 className="text-sm font-semibold">
            {t("h2 = 1. poročni 04455-blok kadarkoli!", "h2 = the 1st marriage 04455-block ever!")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(
              `Vpis 6 (4. februar 1883): ženin Peter HLEBEC, GRIBLJE 2 — »nesumnjivo bralno zvest« (ultra-zoom 1:1!). h2 = najnižja aktivna hiša; prej je imela SAMO mrliški vpis (04894-1919, P148) — poročna knjiga je bila 36 let prehitevana, sedaj prehiteva! + h13 (vpis 5, RADOVIČ — roj. v Segečelu, župn. Vinica, pripis = rojstni kraj, NE hiša!). ${HROVALJ_1883_SIBLINGS}.`,
              `Entry 6 (Feb 4, 1883): the groom Peter HLEBEC, GRIBLJE 2 — »indisputably letter-faithful« (the ultra-zoom 1:1!). h2 = the lowest active house; previously it had ONLY a death entry (04894-1919, P148) — the marriage book was outrun for 36 years, now it overtakes! + h13 (entry 5, RADOVIČ — born in Segečelo, the parish of Vinica, the annotation = the birthplace, NOT the house!). ${HROVALJ_1883_SIBLINGS}.`,
            )}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">
            {t(MARRIAGE_1883_MEJA.restartSi, MARRIAGE_1883_MEJA.restartEn)} · {t(MARRIAGE_1883_MEJA.boundarySi, MARRIAGE_1883_MEJA.boundaryEn)} · {t(MARRIAGE_1883_MEJA.tailSi, MARRIAGE_1883_MEJA.tailEn)}
          </p>
        </div>
        <div className="rounded-lg border border-dashed p-4">
          <h4 className="text-sm font-semibold">
            {t("X-open kandidat + vas-dueli (pošteno ostajajo)", "The X-open candidate + village duels (honestly remain)")}
          </h4>
          <p className="mt-1.5 text-xs text-muted-foreground">
            {t(
              `${MARRIAGE_1883_XOPEN.join(" · ")} — v3: ženin Georg Vituh? (»Granc 25«-duel-»Nemški Rif« — ni Griblje!). Vas-dueli: ${MARRIAGE_1883_VILLAGE_DUELS.join(" · ")}. ${MARRIAGE_1883_NUMBERING}. Duhovnik: ${PRIEST_1883}.`,
              `${MARRIAGE_1883_XOPEN.join(" · ")} — v3: the groom Georg Vituh? (»Granc 25«-duel-»Nemški Rif« — not Griblje!). Village duels: ${MARRIAGE_1883_VILLAGE_DUELS.join(" · ")}. ${MARRIAGE_1883_NUMBERING}. The priest: ${PRIEST_1883}.`,
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

function MarriageEarly1884() {
  const { t } = useLang();
  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <BookOpen className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Poročna predzgodovina 04455 (P239): leto 1884 = 2/13",
          "The marriage prehistory 04455 (P239): the year 1884 = 2/13",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t(
          `2/13 poročne predzgodovine (1873–1885): skeni s52–s56, ${MARRIAGE_1884_TOTAL} vpisov leta 1884 — BREZ preskokov (kontrast 1885-vpis-3!). Restart leta na s53 (vpis 1 = 6. februar, ženin Martin PEZDIRC!), meja 1883/84 = s52→s53 (s52 = tail-1883), meja 1884/85 = s56-tail-vpisi-15–18 (P238 1:1). Številčenje strani razrešeno: s53 = 1–5 · s54 = 6–10 · s55 = 11–14 (ultra-zoom: »11.« = dve navpični črti, NE »12.«!) · s56 = 15–18. Griblje: ${MARRIAGE_1884_GRIBLJE} porok (h54 × h44 · h47 × h34 · h36) + ${MARRIAGE_1884_XOPEN.length} X-open kandidata.`,
          `2/13 of the marriage prehistory (1873–1885): scans s52–s56, ${MARRIAGE_1884_TOTAL} entries of 1884 — NO skips (in contrast to the 1885-entry-3!). The year restarts on s53 (entry 1 = Feb 6, groom Martin PEZDIRC!), the 1883/84 boundary = s52→s53 (s52 = the 1883 tail), the 1884/85 boundary = the s56-tail-entries-15–18 (P238 1:1). The page numbering resolved: s53 = 1–5 · s54 = 6–10 · s55 = 11–14 (the ultra-zoom: »11.« = two vertical strokes, NOT »12.«!) · s56 = 15–18. Griblje: ${MARRIAGE_1884_GRIBLJE} marriages (h54 × h44 · h47 × h34 · h36) + ${MARRIAGE_1884_XOPEN.length} X-open candidates.`,
        )}
      </p>

      {/* Griblje poroke 1884 — vrstni red blokov */}
      <div className="mt-4 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("Griblje poroke 1884 — vrstni red blokov", "The Griblje marriages 1884 — the block order")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            ×{MARRIAGE_1884_GRIBLJE}
          </span>
        </h4>
        <div className="mt-3 grid gap-2 sm:grid-cols-3">
          {MARRIAGE_1884_BLOCKS.map((h) => (
            <div key={h.houseNo + h.scan} className="rounded border bg-card/60 px-2 py-1.5 text-center">
              <div className="text-xs font-semibold tabular-nums">h{h.houseNo}</div>
              <div className="text-[9px] text-muted-foreground">s{h.scan} · Pag. {h.page}</div>
            </div>
          ))}
        </div>
        <p className="mt-1.5 text-[11px] font-mono text-muted-foreground">{MARRIAGE_1884_HOUSES.join(" → ")}</p>
        <p className="mt-2 text-[11px] text-muted-foreground">
          {t(
            `${PEZDIRC_1884_NIT}. ${MILEK_1884_NIT}`,
            `${PEZDIRC_1884_NIT}. ${MILEK_1884_NIT}`,
          )}
        </p>
      </div>

      {/* anomalije */}
      <div className="mt-4 grid gap-3">
        <div className="rounded-lg border border-amber-500/40 bg-amber-500/10 p-4 text-amber-900 dark:text-amber-100">
          <h4 className="text-sm font-semibold">
            {t("Dvojni h34-SILAH-križ (sestrski poroki!)", "The double h34-SILAH cross (sister weddings!)")}
          </h4>
          <p className="mt-1.5 text-xs">
            {t(
              `Vpis 16 (22. junij 1884): nevesta Maria SILAH h34, starši Johann Silah × Anna roj. Dehlin — ISTI starši kot nevesta vpisa 1/1885 (Barbara SILAH h34 × Nikolaus Pozek h58) = SESTRSKI poroki na h34 v dveh zaporednih letih. ${OLDEST_PAIR_1884}; duhovnik: ${PRIEST_1884}.`,
              `Entry 16 (Jun 22, 1884): the bride Maria SILAH h34, parents Johann Silah × Anna née Dehlin — THE SAME parents as the bride of entry 1/1885 (Barbara SILAH h34 × Nikolaus Pozek h58) = SISTER weddings at h34 in two consecutive years. ${OLDEST_PAIR_1884}; the priest: ${PRIEST_1884}.`,
            )}
          </p>
          <p className="mt-2 text-[11px] text-muted-foreground">
            {t(MARRIAGE_1884_MEJA.restartSi, MARRIAGE_1884_MEJA.restartEn)} · {t(MARRIAGE_1884_MEJA.boundarySi, MARRIAGE_1884_MEJA.boundaryEn)} · {t(MARRIAGE_1884_MEJA.tailSi, MARRIAGE_1884_MEJA.tailEn)}
          </p>
        </div>
        <div className="rounded-lg border border-dashed p-4">
          <h4 className="text-sm font-semibold">
            {t("X-open kandidati + vas-dueli (pošteno ostajajo)", "X-open candidates + village duels (honestly remain)")}
          </h4>
          <p className="mt-1.5 text-xs text-muted-foreground">
            {t(
              `${MARRIAGE_1884_XOPEN.join(" · ")} — v7: nevesta Anna Hrizan? (hiša »Griblje 2«-duel-Vrtok-5!); v10: nevesta Katharina dekla »Griblner dyfla« (Griblje-brej-hišne!). Vas-dueli: ${MARRIAGE_1884_VILLAGE_DUELS.join(" · ")}. ${MARRIAGE_1884_NUMBERING}.`,
              `${MARRIAGE_1884_XOPEN.join(" · ")} — v7: the bride Anna Hrizan? (the house »Griblje 2«-duel-Vrtok-5!); v10: the bride Katharina a maid »Griblner dyfla« (Griblje-without-a-house!). Village duels: ${MARRIAGE_1884_VILLAGE_DUELS.join(" · ")}. ${MARRIAGE_1884_NUMBERING}.`,
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

function ParishForensics() {
  const { t } = useLang();
  const maxMilic = Math.max(...MILIC_PER_BOOK.map((b) => b.mentions));
  const statusStyle: Record<string, string> = {
    "POTRJENO": "border-emerald-600/40 bg-emerald-600/10 text-emerald-900 dark:text-emerald-100",
    "RAZREŠENO-DELNO": "border-primary/40 bg-primary/10 text-primary",
    "X-OPEN-OSTAJA": "border-amber-500/40 bg-amber-500/10 text-amber-900 dark:text-amber-100",
  };
  const statusLabel: Record<string, [string, string]> = {
    "POTRJENO": ["potrjeno", "confirmed"],
    "RAZREŠENO-DELNO": ["razrešeno (delno)", "partially resolved"],
    "X-OPEN-OSTAJA": ["X-open ostaja", "X-open remains"],
  };
  const bookName: Record<string, string> = {
    "04104": t("krstna predzgodovina 1871–1885", "the baptism prehistory 1871–1885"),
    "04105": t("krstna 1886–1919", "baptisms 1886–1919"),
    "04106": t("mrliška predzgodovina 1857–1885", "the death prehistory 1857–1885"),
    "04894": t("mrliška 1886–1924", "deaths 1886–1924"),
    "04455": t("poročna 1886–1922", "marriages 1886–1922"),
  };

  return (
    <div className="rounded-xl border bg-card/60 p-5">
      <h3 className="flex items-center gap-2 font-serif text-lg font-semibold">
        <Users className="h-4 w-4 text-primary" aria-hidden />
        {t(
          "Forenzika niti (P237): križ čez vseh 5 knjig",
          "The threads forensics (P237): a cross across all 5 books",
        )}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {t(
          `Odprti X-open vprašanja sinteze so sedaj MERJENI čez celotni korpus (${HOUSE_VITALS.length} blokov): priimek MILIČ/MILEK/MIHELČ se pojavlja v ${MILIC_FAMILY_TOTAL} blokov čez vseh 5 knjig; veriga očeta Mathias/Matija na hiši 65 traja ${MATHIAS_H65_SPAN.first}–${MATHIAS_H65_SPAN.last} (${MATHIAS_H65_TOTAL} dokazov); hiša 69 ima ${H69_TOTAL} dokazov in je vodeniška hiša. Sodbe: ${FORENSIC_VERDICTS.map((v) => t(statusLabel[v.status][0], statusLabel[v.status][1])).join(" · ")}.`,
          `The open X-open questions of the synthesis are now MEASURED across the whole corpus (${HOUSE_VITALS.length} blocks): the surname MILIČ/MILEK/MIHELČ appears in ${MILIC_FAMILY_TOTAL} blocks across all 5 books; the father Mathias/Matija chain at house 65 spans ${MATHIAS_H65_SPAN.first}–${MATHIAS_H65_SPAN.last} (${MATHIAS_H65_TOTAL} proofs); house 69 has ${H69_TOTAL} proofs and is the miller's house. Verdicts: ${FORENSIC_VERDICTS.map((v) => t(statusLabel[v.status][0], statusLabel[v.status][1])).join(" · ")}.`,
        )}
      </p>

      {/* MILIČ-križ po knjigah — mini stolpci */}
      <div className="mt-4 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("MILIČ↔MILEK-križ po knjigah", "The MILIČ↔MILEK cross by book")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            ×{MILIC_FAMILY_TOTAL}
          </span>
        </h4>
        <div className="mt-3 grid gap-2 sm:grid-cols-5">
          {MILIC_PER_BOOK.map((b) => (
            <div key={b.signature} className="flex flex-col items-center gap-1">
              <span className="text-xs font-semibold tabular-nums">×{b.mentions}</span>
              <span
                className="w-full rounded-t-sm bg-primary/60"
                style={{ height: Math.max(4, Math.round((b.mentions / maxMilic) * 48)) }}
                aria-hidden
              />
              <span className="text-[10px] font-mono tabular-nums">{b.signature}</span>
              <span className="text-center text-[9px] leading-tight text-muted-foreground">{bookName[b.signature]}</span>
            </div>
          ))}
        </div>
        <p className="mt-2 text-[11px] text-muted-foreground">
          {t(
            `Kurent-garble MILIČ/MILEK/MIHELČ = isti priimek (h65-veja 1:1): ${MATHIAS_H65_TOTAL} dokazov očeta Mathias/Matija (${MATHIAS_H65_SPAN.first}–${MATHIAS_H65_SPAN.last}); hiša 65 = ${H65_STATS.total} blokov, od tega ${H65_STATS.family} družine (mrliška 1907: »h65 = MILEK-hiša!«).`,
            `The Kurrent garble MILIČ/MILEK/MIHELČ = one surname (the h65 branch 1:1): ${MATHIAS_H65_TOTAL} proofs of the father Mathias/Matija (${MATHIAS_H65_SPAN.first}–${MATHIAS_H65_SPAN.last}); house 65 = ${H65_STATS.total} blocks, ${H65_STATS.family} of the family (the 1907 death register: »h65 = the MILEK house!«).`,
          )}
        </p>
      </div>

      {/* h69 zgodba — obdobja */}
      <div className="mt-4 rounded-lg border bg-background/60 p-4">
        <h4 className="text-sm font-semibold">
          {t("h69 — vodeniška hiša (mlin)", "h69 — the miller's house (a mill)")}
          <span className="ml-2 rounded-full border px-2 py-0.5 text-[10px] font-medium text-primary">
            {H69_TOTAL} {t("dokazov", "proofs")}
          </span>
        </h4>
        <ol className="mt-2 space-y-1.5 text-xs">
          {H69_ERAS.map((e) => (
            <li key={e.id} className="rounded border bg-card/60 px-2.5 py-1.5">
              <span className="font-semibold">
                {t(e.labelSi, e.labelEn)} · {t(e.spanSi, e.spanEn)}{" "}
              </span>
              <span className="text-muted-foreground">— {t(e.familiesSi, e.familiesEn)}</span>
            </li>
          ))}
        </ol>
        <p className="mt-2 text-[11px] text-muted-foreground">
          {t(
            `»Vodenica« ×2 (1886 + 1924) + presek z Milek-družino ×${MILIC_H69_OVERLAP} (botra Katarina Milek 1898 — mreža h65↔h69).`,
            `»Miller's wife« ×2 (1886 + 1924) + the Milek-family overlap ×${MILIC_H69_OVERLAP} (godmother Katarina Milek 1898 — the h65↔h69 network).`,
          )}
        </p>
      </div>

      {/* sodbe */}
      <div className="mt-4 grid gap-3">
        {FORENSIC_VERDICTS.map((v) => (
          <div key={v.id} className={`rounded-lg border p-4 ${statusStyle[v.status]}`}>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <h4 className="text-sm font-semibold">{t(v.titleSi, v.titleEn)}</h4>
              <Badge variant="outline" className="shrink-0 bg-background/60 font-mono text-[10px]">
                {t(statusLabel[v.status][0], statusLabel[v.status][1])}
              </Badge>
            </div>
            <p className="mt-1.5 text-xs">{t(v.bodySi, v.bodyEn)}</p>
            {v.xOpenSi && (
              <p className="mt-2 rounded border border-dashed bg-background/60 px-2 py-1 text-[11px] text-muted-foreground">
                X-open: {t(v.xOpenSi, v.xOpenEn ?? v.xOpenSi)}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* duhovniški križ — rezultat */}
      <p className="mt-3 text-[11px] text-muted-foreground">
        {t(
          `Duhovniški križ (Weisel/Wenzel/Wessely): 04104 = ${PRIEST_CROSS["04104"]} (samo 1871) · 04105 = ${PRIEST_CROSS["04105"]} · 04106 = ${PRIEST_CROSS["04106"]} · 04894 = ${PRIEST_CROSS["04894"]} · 04455 = ${PRIEST_CROSS["04455"]} — brez neodvisnega dokaza, X-open pošteno ostaja.`,
          `The priests' cross (Weisel/Wenzel/Wessely): 04104 = ${PRIEST_CROSS["04104"]} (1871 only) · 04105 = ${PRIEST_CROSS["04105"]} · 04106 = ${PRIEST_CROSS["04106"]} · 04894 = ${PRIEST_CROSS["04894"]} · 04455 = ${PRIEST_CROSS["04455"]} — no independent proof, the X-open honestly remains.`,
        )}
      </p>
    </div>
  );
}

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

      {/* P236: sinteza krstne predzgodovine 04104 (1871–1885) */}
      <BaptismLineSynthesis />
      <ParishForensics />

      {/* P241: poročna predzgodovina 04455 — leto 1882 = 4/13 */}
      <MarriageEarly1882 />

      {/* P240: poročna predzgodovina 04455 — leto 1883 = 3/13 */}
      <MarriageEarly1883 />

      {/* P239: poročna predzgodovina 04455 — leto 1884 = 2/13 */}
      <MarriageEarly1884 />

      {/* P238: poročna predzgodovina 04455 (1873–1885) */}
      <MarriageEarly1885 />

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
              <div key={houseNo} className="min-w-0 rounded-lg border bg-background/60 p-4">
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
                <ul className="mt-3 min-w-0 space-y-2 text-sm [overflow-wrap:anywhere]">
                  {vitals.map((v, vi) => (
                    <li key={`${v.year}-${v.scan}-${vi}`} className="rounded border p-2">
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
