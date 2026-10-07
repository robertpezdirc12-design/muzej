"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useLang } from "./language-context";
import type { Exhibit } from "@/lib/museum";

/**
 * Leafletov zemljevid zbirke — naložen izključno na odjemalcu (next/dynamic,
 * ssr: false). Klinček zapisa (klik) odpre podrobnostni list, enako kot kartica.
 */
export function MapCanvas({
  exhibits,
  vintage,
  onOpen,
}: {
  exhibits: Exhibit[];
  vintage: boolean;
  onOpen: (slug: string) => void;
}) {
  const { lang } = useLang();
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<L.Map | null>(null);
  const layerRef = useRef<L.LayerGroup | null>(null);
  const openRef = useRef(onOpen);

  /* zadnja različica odprtega povratnega klica za klinčke */
  useEffect(() => {
    openRef.current = onOpen;
  }, [onOpen]);

  /* zemljevid ustvarimo enkrat */
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = L.map(containerRef.current, {
      center: [45.57246, 15.29257],
      zoom: 13,
      scrollWheelZoom: false,
      attributionControl: true,
    });

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> prispevali',
    }).addTo(map);

    /* kolesček omogočimo šele po prvem kliku na zemljevid (ne pobega scrolla strani) */
    map.on("click", () => map.scrollWheelZoom.enable());
    map.on("mouseout", () => map.scrollWheelZoom.disable());

    layerRef.current = L.layerGroup().addTo(map);
    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
      layerRef.current = null;
    };
  }, []);

  /* klinčki se preberejo ob spremembi filtra ali jezika */
  useEffect(() => {
    const layer = layerRef.current;
    if (!layer) return;
    layer.clearLayers();

    for (const ex of exhibits) {
      if (!ex.lat || !ex.lng) continue;
      const title = lang === "si" ? ex.titleSi : ex.titleEn;

      const icon = L.divIcon({
        className: "mvg-pin",
        html: `<span class="mvg-pin-dot" aria-hidden="true"></span>`,
        iconSize: [18, 18],
        iconAnchor: [9, 9],
      });

      const marker = L.marker([ex.lat, ex.lng], {
        icon,
        title: `${ex.museumNo} — ${title}`,
        alt: `${ex.museumNo} — ${title}`,
        keyboard: true,
      });

      marker.bindTooltip(
        `<strong class="mvg-tooltip-no">${ex.museumNo}</strong> ${title}`,
        { direction: "top", offset: [0, -8], className: "mvg-tooltip" },
      );

      marker.on("click", () => openRef.current(ex.slug));
      marker.addTo(layer);
    }
  }, [exhibits, lang]);

  /* zgodovinski (sepia) pogled — filter nad ploščicami */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    el.classList.toggle("mvg-vintage", vintage);
  }, [vintage]);

  return (
    <div
      ref={containerRef}
      className="h-[360px] w-full overflow-hidden rounded-xl border sm:h-[420px]"
      role="application"
      aria-label={
        lang === "si"
          ? "Zemljevid zapisov zbirke — kliknite klinček za odprtje zapisa"
          : "Map of collection records — click a pin to open the record"
      }
    />
  );
}
