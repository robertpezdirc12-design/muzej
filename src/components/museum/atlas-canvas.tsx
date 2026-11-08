"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useLang } from "./language-context";
import { SHEET_GEOREFS, VECTOR_BUILDINGS, ATLAS_LOCATIONS } from "@/data/atlas/model";
import { HERITAGE_UNITS } from "@/data/atlas/sources";
import { LANDUSE_ZONES } from "@/data/atlas/landuse";
import leafletOverlayJson from "@/data/atlas/leaflet-overlay.json";
import type { GeoFix } from "@/lib/geo";

/**
 * ATLAS 1825 — zemljevidski list (Leaflet, izključno odjemalec).
 *
 * Sloji:
 *  · OSM — današnje stanje;
 *  · katastrska lista A01 / A02 — georeferencirana slikovna prekrivka
 *    (vir: SI AS 176/N/N83, Arhiv RS) z drsnikom prosojnosti;
 *  · katastrski listi A03 / A04 / A05 — slikovna prekrivka (P51, issue #14/§3):
 *    ovoj skena neodvisno preračunan iz P46 afine (== P50 boundsImageNWSE),
 *    privzeto IZKLOPLJENA; Leaflet ne podpira rotiranih prekrivk — odmik
 *    vogalov osne postavitve ≤ 20 m, del ±40/50 m negotovosti lista
 *    (overlayDeviationM v leaflet-overlay.json); ob prekrivki črtkani
 *    neatline okvir s statusom;
 *  · objekti ~1825 — vektorizacija z arhivskega lista (RECONSTRUCTED);
 *  · raba tal ~1825 — loke ob Kolpi, njivski mozaik, gozd (issue #7, RECONSTRUCTED);
 *  · cerkev sv. Vida (VERIFIED, EŠD 2122) in območje vasi (APPROXIMATE);
 *  · uradni register dediščine EŠD (GISKD) — ločen sodoben sloj;
 *  · muzejski zapis (točke zbirke).
 */

export interface AtlasLayers {
  osm: boolean;
  a01: boolean;
  a02: boolean;
  a03: boolean;
  a04: boolean;
  a05: boolean;
  buildings: boolean;
  landuse: boolean;
  heritage: boolean;
  museum: boolean;
  vintage: boolean;
}

interface OverlaySheet {
  sheet: "A03" | "A04" | "A05";
  cell: string;
  imageUrl: string;
  hullNWSE: [[number, number], [number, number]];
  neatlineNWSE: [[number, number], [number, number]];
  status: string;
  uncertaintyM: number;
  overlayDeviationM: { max: number };
}

const OVERLAY_SHEETS = leafletOverlayJson.sheets as unknown as Record<
  "A03" | "A04" | "A05",
  OverlaySheet
>;
const OVERLAY_KEYS = ["a03", "a04", "a05"] as const;
type OverlayKey = (typeof OVERLAY_KEYS)[number];

export function AtlasCanvas({
  layers,
  opacity,
  userFix,
  onSelect,
  focus,
}: {
  layers: AtlasLayers;
  opacity: number;
  userFix: GeoFix | null;
  onSelect: (id: string, kind: string) => void;
  focus: { lat: number; lng: number; zoom?: number } | null;
}) {
  const { lang } = useLang();
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<L.Map | null>(null);
  const a01Ref = useRef<L.ImageOverlay | null>(null);
  const a02Ref = useRef<L.ImageOverlay | null>(null);
  const overlayRef = useRef<Record<OverlayKey, { img: L.ImageOverlay; rect: L.Rectangle } | null>>({
    a03: null,
    a04: null,
    a05: null,
  });
  const buildingsRef = useRef<L.LayerGroup | null>(null);
  const landuseRef = useRef<L.LayerGroup | null>(null);
  const heritageRef = useRef<L.LayerGroup | null>(null);
  const museumRef = useRef<L.LayerGroup | null>(null);
  const baseRef = useRef<L.TileLayer | null>(null);
  const userLayerRef = useRef<L.LayerGroup | null>(null);
  const selectRef = useRef(onSelect);

  useEffect(() => {
    selectRef.current = onSelect;
  }, [onSelect]);

  const a01 = SHEET_GEOREFS[0];
  const a02 = SHEET_GEOREFS[1];

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = L.map(containerRef.current, {
      center: [45.5755, 15.289],
      zoom: 14,
      minZoom: 12,
      maxZoom: 18,
      scrollWheelZoom: false,
      attributionControl: true,
    });

    baseRef.current = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> · katastrski listi: Arhiv RS (SI AS 176/N/N83)',
    }).addTo(map);

    map.on("click", () => map.scrollWheelZoom.enable());
    map.on("mouseout", () => map.scrollWheelZoom.disable());

    a01Ref.current = L.imageOverlay(a01.imageUrl, a01.bounds, {
      opacity,
      interactive: false,
    });
    a02Ref.current = L.imageOverlay(a02.imageUrl, a02.bounds, {
      opacity,
      interactive: false,
    });

    /* listi A03–A05 (P51) — slikovna prekrivka + črtkani neatline okvir;
       ovoj iz leaflet-overlay.json (en sam vir resnice), privzeto izklopljena */
    (Object.keys(OVERLAY_SHEETS) as ("A03" | "A04" | "A05")[]).forEach((k) => {
      const s = OVERLAY_SHEETS[k];
      const key = ("a" + k.slice(1)) as OverlayKey; // A03 → a03
      const img = L.imageOverlay(
        s.imageUrl,
        [
          [s.hullNWSE[0][0], s.hullNWSE[0][1]],
          [s.hullNWSE[1][0], s.hullNWSE[1][1]],
        ],
        { opacity, interactive: false },
      );
      const rect = L.rectangle(
        [
          [s.neatlineNWSE[0][0], s.neatlineNWSE[0][1]],
          [s.neatlineNWSE[1][0], s.neatlineNWSE[1][1]],
        ],
        {
          color: "#8a6d3b",
          weight: 1.5,
          dashArray: "6 5",
          fill: false,
          className: "mvg-atlas-neatline",
        },
      );
      rect.bindTooltip(
        lang === "si"
          ? `List ${s.sheet} (${s.cell}) — ${s.status} ±${s.uncertaintyM} m · prekrivka: odmik osne postavitve ≤ ${s.overlayDeviationM.max} m (dva vogala točna, Leaflet brez rotacij) · P51`
          : `Sheet ${s.sheet} (${s.cell}) — ${s.status} ±${s.uncertaintyM} m · overlay: axis-aligned deviation ≤ ${s.overlayDeviationM.max} m (two corners exact, Leaflet without rotation) · P51`,
        { className: "mvg-tooltip", direction: "top", sticky: true },
      );
      overlayRef.current[key] = { img, rect };
    });

    /* objekti ~1825 — vektorizacija (RECONSTRUCTED) */
    const bl = L.layerGroup();
    VECTOR_BUILDINGS.forEach((b, i) => {
      const m = L.circleMarker([b.lat, b.lng], {
        radius: Math.max(3, Math.min(5, b.w / 8)),
        color: "#9a5b2e",
        weight: 1,
        fillColor: "#c47a3d",
        fillOpacity: 0.55,
        className: "mvg-atlas-bld",
      });
      m.bindTooltip(
        lang === "si"
          ? `Objekt ~1825 · ${i + 1}/156 (vektorizacija lista A02)`
          : `Building ~1825 · ${i + 1}/156 (vectorised from sheet A02)`,
        { className: "mvg-tooltip", direction: "top" },
      );
      m.on("click", (e) => {
        L.DomEvent.stopPropagation(e);
        selectRef.current(`b1825-${i + 1}`, "building");
      });
      bl.addLayer(m);
    });
    buildingsRef.current = bl;

    /* raba tal ~1825 (issue #7) — približne cone, RECONSTRUCTED */
    const lu = L.layerGroup();
    LANDUSE_ZONES.forEach((z) => {
      const [[n, w], [s, e]] = z.bounds;
      const rect = L.rectangle(
        [
          [n, w],
          [s, e],
        ],
        {
          color: z.color,
          weight: 1.5,
          dashArray: "4 5",
          fillColor: z.fillColor,
          fillOpacity: 0.28,
          className: "mvg-atlas-landuse",
        },
      );
      rect.bindTooltip(
        lang === "si"
          ? `${z.labelSi} — RECONSTRUCTED (±100–150 m)`
          : `${z.labelEn} — RECONSTRUCTED (±100–150 m)`,
        { className: "mvg-tooltip", direction: "top" },
      );
      rect.on("click", (ev) => {
        L.DomEvent.stopPropagation(ev);
        selectRef.current(z.id, "landuse");
      });
      lu.addLayer(rect);
    });
    landuseRef.current = lu;

    /* cerkev + vas (lokacijski sloj) */
    const hl = L.layerGroup();
    ATLAS_LOCATIONS.forEach((loc) => {
      if (!loc.lat || !loc.lng) return;
      if (loc.kind === "cerkev") {
        const m = L.marker([loc.lat, loc.lng], {
          icon: L.divIcon({
            className: "",
            html: `<div class="mvg-atlas-church" role="img" aria-label="cerkev sv. Vida"><span>†</span></div>`,
            iconSize: [26, 26],
            iconAnchor: [13, 13],
          }),
        });
        m.bindTooltip(
          lang === "si"
            ? `${loc.titleSi} — VERIFIED (MVG-002, EŠD 2122)`
            : `${loc.titleEn} — VERIFIED (MVG-002, EŠD 2122)`,
          { className: "mvg-tooltip", direction: "top" },
        );
        m.on("click", (e) => {
          L.DomEvent.stopPropagation(e);
          selectRef.current("loc-cerkev", "location");
        });
        hl.addLayer(m);
      } else if (loc.kind === "vas") {
        const c = L.circle([loc.lat, loc.lng], {
          radius: 500,
          color: "#9a5b2e",
          weight: 1.5,
          dashArray: "5 6",
          fillColor: "#c47a3d",
          fillOpacity: 0.07,
        });
        c.bindTooltip(
          lang === "si"
            ? "Območje vasi Griblje ~1825 — hiše 1–98, prebranih 80 (APPROXIMATE)"
            : "Area of Griblje village ~1825 — houses 1–98, 80 read (APPROXIMATE)",
          { className: "mvg-tooltip", direction: "top" },
        );
        c.on("click", (e) => {
          L.DomEvent.stopPropagation(e);
          selectRef.current("village-1825", "village");
        });
        hl.addLayer(c);
      }
    });
    heritageRef.current = hl;

    userLayerRef.current = L.layerGroup().addTo(map);
    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
      a01Ref.current = null;
      a02Ref.current = null;
      overlayRef.current = { a03: null, a04: null, a05: null };
    };
     
  }, []);

  /* preklop slojev */
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    const apply = (layer: L.Layer | null, on: boolean) => {
      if (!layer) return;
      if (on && !map.hasLayer(layer)) map.addLayer(layer);
      if (!on && map.hasLayer(layer)) map.removeLayer(layer);
    };
    apply(a01Ref.current, layers.a01);
    apply(a02Ref.current, layers.a02);
    for (const key of OVERLAY_KEYS) {
      const pair = overlayRef.current[key];
      if (!pair) continue;
      const on = layers[key];
      if (on && !map.hasLayer(pair.img)) map.addLayer(pair.img);
      if (on && !map.hasLayer(pair.rect)) map.addLayer(pair.rect);
      if (!on && map.hasLayer(pair.img)) map.removeLayer(pair.img);
      if (!on && map.hasLayer(pair.rect)) map.removeLayer(pair.rect);
    }
    apply(buildingsRef.current, layers.buildings);
    apply(landuseRef.current, layers.landuse);
    apply(heritageRef.current, layers.heritage || layers.buildings);
  }, [layers]);

  /* prosojnost prekrivk (skupaj z A03–A05; neatline okvir ostaja viden) */
  useEffect(() => {
    a01Ref.current?.setOpacity(opacity);
    a02Ref.current?.setOpacity(opacity);
    for (const key of OVERLAY_KEYS) {
      const pair = overlayRef.current[key];
      if (!pair) continue;
      pair.img.setOpacity(opacity);
      pair.rect.setStyle({ opacity: Math.min(1, 0.35 + 0.65 * opacity) });
    }
  }, [opacity]);

  /* sepija sodobnih ploščic */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    el.classList.toggle("mvg-vintage", layers.vintage);
  }, [layers.vintage]);

  /* uporabnikova lokacija */
  useEffect(() => {
    const map = mapRef.current;
    const ul = userLayerRef.current;
    if (!map || !ul) return;
    ul.clearLayers();
    if (userFix?.lat && userFix?.lng) {
      L.circleMarker([userFix.lat, userFix.lng], {
        radius: 6,
        color: "#1a7f4b",
        weight: 2,
        fillColor: "#35c07f",
        fillOpacity: 0.9,
        className: "mvg-me-dot",
      })
        .addTo(ul)
        .bindTooltip(
          lang === "si" ? "Vaša lokacija" : "Your location",
          { className: "mvg-tooltip", direction: "top" },
        );
    }
  }, [userFix, lang]);

  /* fokus na objekt */
  useEffect(() => {
    if (focus && mapRef.current) {
      mapRef.current.flyTo([focus.lat, focus.lng], focus.zoom ?? 16, { duration: 0.8 });
    }
  }, [focus]);

  return (
    <div
      ref={containerRef}
      className="isolate h-[380px] w-full rounded-xl border bg-secondary/40 sm:h-[460px] lg:h-[520px]"
      role="application"
      aria-label={lang === "si" ? "Zemljevid ATLAS 1825" : "ATLAS 1825 map"}
    />
  );
}
