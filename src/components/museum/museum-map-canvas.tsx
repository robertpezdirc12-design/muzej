"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useLang } from "./language-context";
import type { Exhibit } from "@/lib/museum";
import type { GeoFix } from "@/lib/geo";
import { TIME_SPOTS, type TimeSpot } from "@/data/atlas/timespots";

/**
 * Leafletov zemljevid zbirke — naložen izključno na odjemalcu (next/dynamic,
 * ssr: false). Klinček zapisa (klik) odpre podrobnostni list, enako kot kartica.
 *
 * Razširitvi AR vodnika (issue #1):
 *  · uporabnikova lokacija (GPS) — utripajoča točka + krog natančnosti;
 *  · zgodovinska plast »vas ~1825« — poligon jedra in črtkane poti,
 *    VSAK element jasno označen kot interpretacija (kataster ~1825 ni ohranjen).
 *
 * AR TIME SPOTS (issue #11): plamenjače časovnih točk (TimeLens koncept) —
 * klik na točko odpre kartico s [POGLEJ V AR] na letnici točke.
 */

/** Leta zgodovinske plasti (izdih terezijansko-franciškanske dobe). */
export const HISTORIC_YEAR = 1825;

/** Interpretacija jedra vasi ~1825 (ni izvirni kataster!). */
const CORE_1825: [number, number][] = [
  [45.571, 15.2905],
  [45.5745, 15.29],
  [45.5758, 15.293],
  [45.5748, 15.2955],
  [45.5712, 15.2945],
];

/** Črtkane poti — interpretacije, smeri podprte z zapisi zbirke. */
const PATHS_1825: { points: [number, number][]; no: string; si: string; en: string }[] = [
  {
    points: [
      [45.5725, 15.2925],
      [45.5708, 15.2952],
      [45.5688, 15.2988],
    ],
    no: "MVG-006",
    si: "pot do Kolpe — interpretacija (meja in carinarnica ob reki: MVG-006, MVG-092, MVG-015)",
    en: "path to the Kolpa — interpretation (border and customs post by the river: MVG-006, MVG-092, MVG-015)",
  },
  {
    points: [
      [45.5725, 15.2925],
      [45.5735, 15.282],
      [45.576, 15.2643],
    ],
    no: "MVG-040",
    si: "stara pot proti Cerkvišču — interpretacija (tri cerkvice zahodno od vasi: MVG-040, 1408)",
    en: "old road towards Cerkvišče — interpretation (three churches west of the village: MVG-040, 1408)",
  },
  {
    points: [
      [45.5725, 15.2925],
      [45.5706, 15.2848],
      [45.569, 15.275],
    ],
    no: "MVG-028",
    si: "cesta proti Črnomlju — interpretacija (zaseda na cesti Črnomelj–Griblje 1941 dokazuje staro cesto: MVG-028)",
    en: "road towards Črnomelj — interpretation (the 1941 ambush on the Črnomelj–Griblje road proves the old road: MVG-028)",
  },
  {
    points: [
      [45.5725, 15.2925],
      [45.5688, 15.2988],
      [45.56, 15.308],
      [45.5315, 15.3119],
    ],
    no: "MVG-009",
    si: "pot ob Kolpi do mlinov — interpretacija (mlinov nekdaj ni bilo brez poti ob reki: MVG-009)",
    en: "path along the Kolpa to the mills — interpretation (mills needed a riverside path: MVG-009)",
  },
];

const SEPIA_LINE = "#9a5b2e";

export function MapCanvas({
  exhibits,
  vintage,
  historic,
  userFix,
  onOpen,
  onSpot,
}: {
  exhibits: Exhibit[];
  vintage: boolean;
  historic: boolean;
  userFix: GeoFix | null;
  onOpen: (slug: string) => void;
  onSpot: (spot: TimeSpot) => void;
}) {
  const { lang } = useLang();
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<L.Map | null>(null);
  const layerRef = useRef<L.LayerGroup | null>(null);
  const userLayerRef = useRef<L.LayerGroup | null>(null);
  const historicLayerRef = useRef<L.LayerGroup | null>(null);
  const spotLayerRef = useRef<L.LayerGroup | null>(null);
  const centeredRef = useRef(false);
  const openRef = useRef(onOpen);
  const onSpotRef = useRef(onSpot);

  /* zadnja različica odprtega povratnega klica za klinčke */
  useEffect(() => {
    openRef.current = onOpen;
    onSpotRef.current = onSpot;
  }, [onOpen, onSpot]);

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
    userLayerRef.current = L.layerGroup().addTo(map);
    historicLayerRef.current = L.layerGroup().addTo(map);
    spotLayerRef.current = L.layerGroup().addTo(map);
    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
      layerRef.current = null;
      userLayerRef.current = null;
      historicLayerRef.current = null;
      spotLayerRef.current = null;
      centeredRef.current = false;
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

  /* ── AR TIME SPOTS: terakota plamenjače z letnico (vedno na karti) ── */
  useEffect(() => {
    const layer = spotLayerRef.current;
    if (!layer) return;
    layer.clearLayers();

    for (const spot of TIME_SPOTS) {
      const title = lang === "si" ? spot.titleSi : spot.titleEn;
      const yearLabel = spot.year === 2026 ? "danes" : spot.year === 1900 ? "~1900" : "1825";

      const marker = L.marker([spot.lat, spot.lng], {
        icon: L.divIcon({
          className: "mvg-spot",
          html: `<span class="mvg-spot-badge" aria-hidden="true">${yearLabel}</span>`,
          iconSize: [52, 24],
          iconAnchor: [26, 12],
        }),
        title: `TimeSpot — ${title}`,
        alt: `TimeSpot — ${title}`,
        keyboard: true,
        zIndexOffset: 500,
      });

      marker.bindTooltip(
        `<strong class="mvg-tooltip-no">🕰 ${yearLabel}</strong> ${title}`,
        { direction: "top", offset: [0, -10], className: "mvg-tooltip" },
      );

      marker.on("click", () => onSpotRef.current(spot));
      marker.addTo(layer);
    }
  }, [lang]);

  /* ── uporabnikova lokacija: utripajoča točka + krog natančnosti ── */
  useEffect(() => {
    const layer = userLayerRef.current;
    const map = mapRef.current;
    if (!layer || !map) return;
    layer.clearLayers();
    if (!userFix) return;

    const pos: L.LatLngExpression = [userFix.lat, userFix.lng];

    if (userFix.accuracy != null && userFix.accuracy > 0) {
      L.circle(pos, {
        radius: userFix.accuracy,
        color: SEPIA_LINE,
        weight: 1,
        opacity: 0.5,
        fillColor: SEPIA_LINE,
        fillOpacity: 0.08,
        interactive: false,
      }).addTo(layer);
    }

    const me = L.marker(pos, {
      icon: L.divIcon({
        className: "mvg-me",
        html: `<span class="mvg-me-dot" aria-hidden="true"></span>`,
        iconSize: [18, 18],
        iconAnchor: [9, 9],
      }),
      keyboard: false,
      interactive: false,
    }).addTo(layer);

    me.bindTooltip(
      lang === "si"
        ? "tu ste — vaš GPS (ostane v brskalniku)"
        : "you are here — your GPS (stays in the browser)",
      { direction: "top", offset: [0, -8], className: "mvg-tooltip" },
    );

    /* prvi priklop: enkrat postavimo pogled nase */
    if (!centeredRef.current) {
      centeredRef.current = true;
      map.setView(pos, Math.max(map.getZoom(), 15), { animate: true });
    }
  }, [userFix, lang]);

  /* ── zgodovinska plast ~1825: interpretacija ── */
  useEffect(() => {
    const layer = historicLayerRef.current;
    if (!layer) return;
    layer.clearLayers();
    if (!historic) return;

    L.polygon(CORE_1825, {
      color: SEPIA_LINE,
      weight: 2,
      dashArray: "6 5",
      fillColor: SEPIA_LINE,
      fillOpacity: 0.07,
      interactive: true,
    })
      .bindTooltip(
        lang === "si"
          ? '<strong class="mvg-tooltip-no">interpretacija</strong> jedro vasi ~1825 — poligon je skica po prvi omembi vasi 1468 in njenih zaselkih (MVG-001, MVG-049); izvirni kataster ni ohranjen.'
          : '<strong class="mvg-tooltip-no">interpretation</strong> village core ~1825 — the polygon is a sketch following the 1468 first mention of the village and its hamlets (MVG-001, MVG-049); no original cadastre survives.',
        { sticky: true, className: "mvg-tooltip" },
      )
      .addTo(layer);

    for (const p of PATHS_1825) {
      L.polyline(p.points, {
        color: SEPIA_LINE,
        weight: 2.5,
        dashArray: "3 7",
        opacity: 0.85,
        lineCap: "round",
        interactive: true,
      })
        .bindTooltip(
          `<strong class="mvg-tooltip-no">interpretacija</strong> ${
            lang === "si" ? p.si : p.en
          }`,
          { sticky: true, className: "mvg-tooltip" },
        )
        .addTo(layer);
    }
  }, [historic, lang]);

  /* zgodovinski (sepia) pogled — filter nad ploščicami */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    el.classList.toggle("mvg-vintage", vintage);
  }, [vintage]);

  return (
    <div
      ref={containerRef}
      className="isolate h-[360px] w-full overflow-hidden rounded-xl border sm:h-[420px]"
      role="application"
      aria-label={
        lang === "si"
          ? "Zemljevid zapisov zbirke — kliknite klinček za odprtje zapisa"
          : "Map of collection records — click a pin to open the record"
      }
    />
  );
}
