/**
 * VILLAGE 3D — priprava podatkov za proceduralno 3D rekonstrukcijo vasi (issue #10).
 *
 * Metodologija (kot LagunAR 2023 — rekonstrukcija mesta iz zgodovinskega načrta):
 *  · 156 katastrskih podlatn (buildings.json, list A02, SI AS 176) → stavbe z
 *    dvokapnico, ekstrudirane iz izmerjenih w×h (metri) — RECONSTRUCTED;
 *  · raba tal ~1825 (VLM analiza listov) → barvne cone na tleh — RECONSTRUCTED ±;
 *  · Kolpa — georeferencirana struga (sidro 15,2994 E, ujemanje 9/10) — REVIEW;
 *  · ~1900: gostota jedra (ocena) — zgoščevanje ob jedru, jasno označeno OCENA;
 *  · danes: »duhovi« (žični obris 1825) za primerjavo — interpretacija.
 *
 * Celotna enota: lokalni koordinatni sistem v metrih, izhodišče = jedro vasi
 * (45.5725 N 15.2926 E, VERIFIED). x = vzhod, z = jug (sever = −z), y = višina.
 */

import { VECTOR_BUILDINGS } from "@/data/atlas/model";
import { LANDUSE_ZONES } from "@/data/atlas/landuse";

/** izhodišče lokalnega sistema — jedro vasi Grüble (VERIFIED) */
export const ORIGIN = { lat: 45.5725, lng: 15.2926 };

const M_PER_DEG_LAT = 111_320;
const M_PER_DEG_LNG = 111_320 * Math.cos((ORIGIN.lat * Math.PI) / 180);

/** lat/lng → lokalna raven (x vzhod, z jug) v metrih */
export function toLocal(lat: number, lng: number): { x: number; z: number } {
  return {
    x: (lng - ORIGIN.lng) * M_PER_DEG_LNG,
    z: -(lat - ORIGIN.lat) * M_PER_DEG_LAT,
  };
}

export interface PreparedBuilding {
  index: number;
  x: number;
  z: number;
  /** širina (m) — vzhod↔zahod */
  w: number;
  /** globina (m) — sever↔jug */
  d: number;
  rotY: number;
  wallH: number;
  roofH: number;
  /** jedro vasi (≤ CORE_R)? */
  core: boolean;
}

export interface GrowthBuilding {
  x: number;
  z: number;
  w: number;
  d: number;
  rotY: number;
  wallH: number;
  roofH: number;
}

/** polmer jedra vasi (m) — stavbe znotraj = vas Grüble ~1825 */
export const CORE_R = 350;

/** cerkev sv. Vida (VERIFIED) — lokalne koordinate + višina stropa modela */
export const CHURCH = {
  ...toLocal(45.5728, 15.2922),
  targetH: 13,
};

/* ── deterministični psevdo-naključni (isti izid vsakič) ── */

function hash01(n: number): number {
  let t = (n + 0x6d2b79f5) | 0;
  t = Math.imul(t ^ (t >>> 15), 1 | t);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}

function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ── 1825: 156 stavb iz katastra ── */

export const BUILDINGS_1825: PreparedBuilding[] = VECTOR_BUILDINGS.map(
  (b, i) => {
    const { x, z } = toLocal(b.lat, b.lng);
    const r1 = hash01(i * 3 + 1);
    const r2 = hash01(i * 3 + 2);
    const isBarn = b.w > 18;
    const wallH = (isBarn ? 3.4 : 2.7) + r1 * 0.7;
    return {
      index: i,
      x,
      z,
      w: b.w,
      d: b.h,
      rotY: (r2 - 0.5) * 0.44, /* ±12° — orientacija ni zabeležena v vektorizaciji */
      wallH,
      roofH: wallH * 0.62,
      core: Math.hypot(x, z) <= CORE_R,
    };
  },
);

/* ── ~1900: gostota jedra (OCENA — ni katastra) ──
   Registracija hiš 1825 ≈ 80; do ~1900 se je jedro (kot povsod v Beli krajini
   po odpravi zaprtih okolišev in delitvi domačij) zgostilo s hlevi in kaščami.
   Deterministično zgoščevanje: ob vsaki jedrni domačiji en skednj/hlev,
   če je od vseh sosedov vsaj 9 m stran. Izrecno označeno kot ocena. */

export const GROWTH_1900: GrowthBuilding[] = (() => {
  const rnd = mulberry32(1900);
  const core = BUILDINGS_1825.filter((b) => b.core).sort(
    (a, b) => a.x * 31 + a.z - (b.x * 31 + b.z),
  );
  const taken: { x: number; z: number }[] = BUILDINGS_1825.map((b) => ({
    x: b.x,
    z: b.z,
  }));
  const out: GrowthBuilding[] = [];
  for (const b of core) {
    if (out.length >= 52) break;
    const ang = rnd() * Math.PI * 2;
    const dist = 9 + rnd() * 8;
    const x = b.x + Math.cos(ang) * dist;
    const z = b.z + Math.sin(ang) * dist;
    if (Math.hypot(x, z) > CORE_R) continue;
    if (taken.some((t) => Math.hypot(t.x - x, t.z - z) < 9.5)) continue;
    taken.push({ x, z });
    const wallH = 2.0 + rnd() * 0.5;
    out.push({
      x,
      z,
      w: 4.5 + rnd() * 2,
      d: 3.5 + rnd() * 1.5,
      rotY: (rnd() - 0.5) * 0.44,
      wallH,
      roofH: wallH * 0.55,
    });
  }
  return out;
})();

/* ── cone rabe tal na tleh (RECONSTRUCTED ±100–150 m) ── */

export interface GroundZone {
  kind: string;
  labelSi: string;
  labelEn: string;
  color: number;
  opacity: number;
  /** [x1, z1, x2, z2] lokalni metri */
  rect: [number, number, number, number];
}

export const GROUND_ZONES: GroundZone[] = LANDUSE_ZONES.map((z) => {
  const [[n, w], [s, e]] = z.bounds;
  const a = toLocal(n, w);
  const b = toLocal(s, e);
  return {
    kind: z.kind,
    labelSi: z.labelSi,
    labelEn: z.labelEn,
    color:
      z.kind === "meadow"
        ? 0x9ec497
        : z.kind === "forest"
          ? 0x5d7355
          : 0xd9c27a,
    opacity: z.kind === "forest" ? 0.55 : 0.42,
    rect: [Math.min(a.x, b.x), Math.min(a.z, b.z), Math.max(a.x, b.x), Math.max(a.z, b.z)],
  };
});

/* ── Kolpa — georeferencirana struga (REVIEW ±75–120 m) ── */

/** kontrolne točke struge (lat, lng) — A01 sidro + meji lista */
const KOLPA_PTS: [number, number][] = [
  [45.5672, 15.2978],
  [45.5700, 15.2990],
  [45.5725, 15.2994],
  [45.5760, 15.2992],
  [45.5800, 15.2980],
  [45.5880, 15.2960],
];

export const KOLPA_LOCAL = KOLPA_PTS.map(([lat, lng]) => toLocal(lat, lng));

/* ── periode ── */

export interface PeriodInfo {
  year: 1825 | 1900 | 2026;
  labelSi: string;
  labelEn: string;
  noteSi: string;
  noteEn: string;
  buildingCount: number;
}

export const PERIODS: PeriodInfo[] = [
  {
    year: 1825,
    labelSi: "1825",
    labelEn: "1825",
    noteSi:
      "Franciscejski kataster: 156 stavb k.o. Grüble (vektorizacija lista A02), raba tal po VLM analizi. RECONSTRUCTED — tlorisi so izmerjeni, višine/orientacije so interpretacija.",
    noteEn:
      "Franciscean cadastre: 156 buildings of c.m. Grüble (vectorised from sheet A02), land use from VLM analysis. RECONSTRUCTED — footprints measured, heights/orientations interpreted.",
    buildingCount: BUILDINGS_1825.length,
  },
  {
    year: 1900,
    labelSi: "~1900",
    labelEn: "~1900",
    noteSi: `OCENA: jedro vasi se zgosti s hlevi in kaščami (${GROWTH_1900.length} novih stavb) — kataster za ~1900 še ni uporabljen; prikaz ilustrira rast po delitvi domačij. Poudarjene stavbe = ocena.`,
    noteEn: `ESTIMATE: the village core densifies with barns and granaries (${GROWTH_1900.length} new buildings) — no ~1900 cadastre used; the growth after farm divisions is illustrated. Highlighted buildings = estimate.`,
    buildingCount: BUILDINGS_1825.length + GROWTH_1900.length,
  },
  {
    year: 2026,
    labelSi: "danes",
    labelEn: "today",
    noteSi:
      "Duhovi 1825 (žični obris) na današnji pokrajini — primerjava z današnjim stanjem v kameri. Današnje stavbe se rišejo iz ločenega vira (OSM), tu samo obris.",
    noteEn:
      "Ghosts of 1825 (wireframe) over today's landscape — compare with the present in your camera. Present-day buildings come from a separate source (OSM); only the outline is shown here.",
    buildingCount: BUILDINGS_1825.length,
  },
];

/** najbližja stavba 1825 točki (lokalni metri) */
export function nearestBuilding1825(
  x: number,
  z: number,
): { b: PreparedBuilding; d: number } {
  let best = BUILDINGS_1825[0];
  let bd = Infinity;
  for (const b of BUILDINGS_1825) {
    const d = Math.hypot(b.x - x, b.z - z);
    if (d < bd) {
      bd = d;
      best = b;
    }
  }
  return { b: best, d: bd };
}
