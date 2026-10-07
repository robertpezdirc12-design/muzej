"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useLang } from "./language-context";
import { SHEET_GEOREFS, VECTOR_BUILDINGS, ATLAS_LOCATIONS } from "@/data/atlas/model";
import { HERITAGE_UNITS } from "@/data/atlas/sources";
import type { GeoFix } from "@/lib/geo";

/**
 * ATLAS 1825 — zemljevidski list (Leaflet, izključno odjemalec).
 *
 * Sloji:
 *  · OSM — današnje stanje;
 *  · katastrska lista A01 / A02 — georeferencirana slikovna prekrivka
 *    (vir: SI AS 176/N/N83, Arhiv RS) z drsnikom prosojnosti;
 *  · objekti ~1825 — vektorizacija z arhivskega lista (RECONSTRUCTED);
 *  · cerkev sv. Vida (VERIFIED, EŠD 2122) in območje vasi (APPROXIMATE);
 *  · uradni register dediščine EŠD (GISKD) — ločen sodoben sloj;
 *  · muzejski zapis (točke zbirke).
 */

export interface AtlasLayers {
  osm: boolean;
  a01: boolean;
  a02: boolean;
  buildings: boolean;
  heritage: boolean;
  museum: boolean;
  vintage: boolean;
}

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
  const buildingsRef = useRef<L.LayerGroup | null>(null);
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
    apply(buildingsRef.current, layers.buildings);
    apply(heritageRef.current, layers.heritage || layers.buildings);
  }, [layers]);

  /* prosojnost prekrivk */
  useEffect(() => {
    a01Ref.current?.setOpacity(opacity);
    a02Ref.current?.setOpacity(opacity);
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
