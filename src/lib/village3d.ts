/**
 * VILLAGE 3D — priprava podatkov za proceduralno 3D rekonstrukcijo vasi (issue #10).
 *
 * Metodologija (kot LagunAR 2023 — rekonstrukcija mesta iz zgodovinskega načrta):
 *  · 156 katastrskih podlatn (buildings.json, list A02, SI AS 176) → stavbe z
 *    dvokapnico, ekstrudirane iz izmerjenih w×h (metri) — RECONSTRUCTED;
 *  · raba tal ~1825 (VLM analiza listov) → barvne cone na tleh — RECONSTRUCTED ±;
 *  · Kolpa — georeferencirana struga (OSM, sidro 15,2994 E) — KORREKTNA;
 *  · ~1900: gostota jedra (ocena) — zgoščevanje ob jedru, jasno označeno OCENA;
 *  · danes: »duhovi« (žični obris 1825) za primerjavo — interpretacija.
 *
 * GEOTRUTH (issue #14, 2026-10-08): listi A01/A02 so zasidrani na uradni EŠD 2122
 * (cerkev sv. Vida, 45,567610 N 15,290311 E). Vsa izpeljana geometrija je bila
 * translirana za −0,005190 lat / −0,001889 lng glede na staro (krožno) afino.
 * Izhodišče lokalnega sistema ostaja sodobno jedro vasi (OSM place node) —
 * vas 1825 leži južno od njega (z ≈ 160–1500 m), zrasla je proti severu.
 *
 * Celotna enota: lokalni koordinatni sistem v metrih, izhodišče = sodobno jedro
 * vasi (45.5725 N 15.2926 E, CORROBORATED — OSM place node 468490150).
 * x = vzhod, z = jug (sever = −z), y = višina.
 */

import { VECTOR_BUILDINGS } from "@/data/atlas/model";
import { LANDUSE_ZONES } from "@/data/atlas/landuse";
import presentJson from "@/data/atlas/present.json";

/** izhodišče lokalnega sistema — SODOBNO jedro vasi (OSM place node, CORROBORATED).
 *  Ni jedro 1825 — to je ~370 m JZ (glej GEOTRUTH anchor-jedro-1825). */
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

/** središče jedra vasi 1825 (GEOTRUTH afina — pas z dvema sklopoma ob cerkvi) */
export const CORE_CENTER = { x: 15, z: 530 };

/** polmer jedra vasi 1825 (m) — stavbe znotraj = vas Grüble ~1825 */
export const CORE_R = 350;

/** je točka v jedru vasi 1825? (GEOTRUTH afina — center 2025-10-08) */
export function inVillageCore(x: number, z: number): boolean {
  return Math.hypot(x - CORE_CENTER.x, z - CORE_CENTER.z) <= CORE_R;
}

/** cerkev sv. Vida (EŠD 2122, VERIFIED — uradni register + OSM) — lokalne
 *  koordinate + višina strehe modela. Lega na pokopališkem gričku JZ od
 *  stare (krožne) predpostavke — glej GEOTRUTH A02_CORRECTION. */
export const CHURCH = {
  ...toLocal(45.567610, 15.290311),
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
      core: inVillageCore(x, z),
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
    if (!inVillageCore(x, z)) continue;
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

/* ── KAJ JE IZGINILO? (issue #12, P1) — 1825 ∩ današnji OSM ──
   Današnje stavbe: OpenStreetMap posnetek 2026-10-07 (ODbL, api.openstreetmap.org
   bbox 15.273–15.301 × 45.562–45.5785). Primerjava težišč katastrskih podlatn
   z današnjimi stavbami → status po stavbi (OBSTOJA / NEGOTOVO / NI VEČ).
   Odsotnost v OSM posnetku NI dokaz porušitve — status čaka terensko preverbo
   (dokajeno ravnanje z negotovostjo po vzoru TimeLens/Himera). */

/** status stavbe 1825 glede na današnji OSM posnetek */
export type BuildingPresence = "exists" | "uncertain" | "gone";

export interface PresentBuilding {
  id: number;
  x: number;
  z: number;
  w: number;
  d: number;
  area: number;
  type: string;
}

interface PresentFile {
  _meta: { osmSnapshot: string; methodSi: string; noteSi: string };
  present: PresentBuilding[];
  match: { status: BuildingPresence; d: number | null; osmId: number | null }[];
}

const PRESENT_FILE = presentJson as unknown as PresentFile;

/** današnje stavbe iz OSM posnetka (lokalni metri, hiše + gospodarske) */
export const PRESENT_BUILDINGS: PresentBuilding[] = PRESENT_FILE.present;

/** status vsake od 156 stavb 1825 (indeksno usklajeno z BUILDINGS_1825) */
export const BUILDING_STATUS: BuildingPresence[] = PRESENT_FILE.match.map(
  (m) => m.status,
);

/** razdalja do najbližje današnje stavbe (m, null = >9000) */
export const BUILDING_NEAREST_PRESENT: (number | null)[] =
  PRESENT_FILE.match.map((m) => m.d);

/** datum OSM posnetka */
export const OSM_SNAPSHOT = PRESENT_FILE._meta.osmSnapshot;

export const PRESENCE_META = {
  osmSnapshot: PRESENT_FILE._meta.osmSnapshot,
  methodSi: PRESENT_FILE._meta.methodSi,
  sourceSi:
    "Današnje stavbe: OpenStreetMap (posnetek " +
    PRESENT_FILE._meta.osmSnapshot +
    ", © avtorji OSM, ODbL) · kataster 1825: list A02 (SI AS 176)",
  sourceEn:
    "Present-day buildings: OpenStreetMap (snapshot " +
    PRESENT_FILE._meta.osmSnapshot +
    ", © OSM contributors, ODbL) · 1825 cadastre: sheet A02 (SI AS 176)",
};

export interface PresenceLegendItem {
  status: BuildingPresence;
  dotSi: string;
  dotEn: string;
  labelSi: string;
  labelEn: string;
  noteSi: string;
  noteEn: string;
}

/** legenda statusov (🟢/🟡/🔴) — enako v AR kot v ATLAS 3D */
export const PRESENCE_LEGEND: PresenceLegendItem[] = [
  {
    status: "exists",
    dotSi: "🟢",
    dotEn: "🟢",
    labelSi: "obstaja",
    labelEn: "still stands",
    noteSi: "današnja stavba stoji na tlorisu 1825",
    noteEn: "a present-day building stands on the 1825 footprint",
  },
  {
    status: "uncertain",
    dotSi: "🟡",
    dotEn: "🟡",
    labelSi: "negotovo",
    labelEn: "uncertain",
    noteSi: "stavba v 40 m — morda ista domačija, morda ne",
    noteEn: "a building within 40 m — perhaps the same farmstead, perhaps not",
  },
  {
    status: "gone",
    dotSi: "🔴",
    dotEn: "🔴",
    labelSi: "ni je več",
    labelEn: "gone",
    noteSi: "brez stavbe v 40 m — verjetno porušena (terenska preverba čaka)",
    noteEn: "no building within 40 m — likely demolished (field check pending)",
  },
];

/** seštevek statusov 156 stavb + cerkev (obstaja) */
export const IZGINILO_STATS = (() => {
  const count = (s: BuildingPresence) =>
    BUILDING_STATUS.filter((x) => x === s).length;
  return {
    exists: count("exists") + 1, /* + cerkev sv. Vida */
    uncertain: count("uncertain"),
    gone: count("gone"),
    total1825: BUILDINGS_1825.length + 1, /* 156 + cerkev */
    presentCount: PRESENT_BUILDINGS.length,
    osmSnapshot: OSM_SNAPSHOT,
  };
})();

/** status hiše (kataster + OSM); cerkev = poseben primer */
export function presenceOf(index: number): BuildingPresence {
  return BUILDING_STATUS[index] ?? "uncertain";
}

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
      "Franciscejski kataster: 156 stavb k.o. Grüble (vektorizacija lista A02), raba tal po VLM analizi. RECONSTRUCTED — tlorisi so izmerjeni, višine/orientacije so interpretacija; drevesa (gozdne cone + razpršena) in dim iz dimnikov so interpretacija (P12), ki vasi da živost.",
    noteEn:
      "Franciscean cadastre: 156 buildings of c.m. Grüble (vectorised from sheet A02), land use from VLM analysis. RECONSTRUCTED — footprints measured, heights/orientations interpreted; trees (forest zones + scattered) and chimney smoke are interpretation (P12) that brings the village to life.",
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
      "Kaj je izginilo? Duhovi 1825 na današnji pokrajini, obarvani po stanju: 🟢 obstaja · 🟡 negotovo · 🔴 ni je več (primerjava s stavbami OpenStreetMap, posnetek " +
      OSM_SNAPSHOT +
      "). V AR se danes vidi skozi kamero — duhovi povedo, kje je stalo. Odsotnost v OSM posnetku ni dokaz porušitve.",
    noteEn:
      "What has vanished? Ghosts of 1825 over today's landscape, coloured by fate: 🟢 still stands · 🟡 uncertain · 🔴 gone (matched against OpenStreetMap buildings, snapshot " +
      OSM_SNAPSHOT +
      "). In AR the present shows through the camera — the ghosts mark where things stood. Absence from the OSM snapshot is not proof of demolition.",
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

/* ── P12 (2026-10-08): DRESEVA + DIM ────────────────────────────────────
   RAZISKOVALNA UGOTOVITEV (negativna, dokumentirana): hišne številke NA
   listu A02 NISO zapisane. Slepi VLM testi 6 stavb (8–14× povečava, 3
   ponovitve) → BLIZINA_BREZ; 43 »številka-podobnih« rdečih madežev v
   stavbah (povezane komponente, 15–250 px) → nečitljivi (razpad skena);
   rdeče 4-mestne PARCELNE številke v parcelah (1009–1106 ob jedru) so
   berljive, a povezava parcela↔hiša bi zahtevala ~50+ strani PS (143 str.
   registra Grund-Parzellen) pri akutnem VLM rate-limitu → TO_COLLECT.
   Glej research/p12/README.md.

   DRESEVA (interpretacija, jasno označena): gozdne cone (Brezov gozd,
   RECONSTRUCTED iz VLM analize listov) dobijo gost gozd (~1 drevo /
   500 m², listavci + iglavci), loke redko razpršena drevesa (~1 /
   15000 m²), njive brez. Deterministično (mulberry32) — vedno isti prizor.
   DIM: 8 dimnikov v jedru — veda, da vas ŽIVI (interpretacija); vidno
   samo v 1825/~1900, ne v »danes«. */

export interface TreeSpot {
  x: number;
  z: number;
  kind: "dec" | "con";
  /** višina drevesa (m) */
  h: number;
  /** v gozdu (strnjena sestoj) ali posamič (loka/vrt) */
  forest: boolean;
}

const TREES_SEED = 1225;

export const TREES: TreeSpot[] = (() => {
  const rnd = mulberry32(TREES_SEED);
  const out: TreeSpot[] = [];
  for (const g of GROUND_ZONES) {
    const [x1, z1, x2, z2] = g.rect;
    const w = x2 - x1;
    const d = z2 - z1;
    if (w < 20 || d < 20) continue;
    const per =
      g.kind === "forest" ? 1 / 500 : g.kind === "meadow" ? 1 / 15000 : 0;
    if (per === 0) continue;
    const n = Math.min(1600, Math.round(w * d * per));
    for (let i = 0; i < n; i++) {
      const x = x1 + rnd() * w;
      const z = z1 + rnd() * d;
      /* izogibaj se stavbam (min 7 m od središča) — enostaven test je
         dovolj: drevesa ob hišah niso dokumentirana, zato jih umikamo */
      let near = false;
      for (const b of BUILDINGS_1825) {
        if (Math.abs(b.x - x) < b.w / 2 + 7 && Math.abs(b.z - z) < b.d / 2 + 7) {
          near = true;
          break;
        }
      }
      if (near) continue;
      const con = rnd() < (g.kind === "forest" ? 0.3 : 0.08);
      out.push({
        x,
        z,
        kind: con ? "con" : "dec",
        h: (con ? 6 : 4) + rnd() * (con ? 5 : 4),
        forest: g.kind === "forest",
      });
    }
  }
  return out;
})();

export const TREE_STATS = {
  total: TREES.length,
  forest: TREES.filter((t) => t.forest).length,
  scattered: TREES.filter((t) => !t.forest).length,
  seed: TREES_SEED,
};

/** 8 dimnikov v jedru vasi (deterministično — vsaka 3. jedrna stavba,
    mešani grajski; dim = interpretacija, veda živosti) */
export const SMOKE_CHIMNEYS: { x: number; z: number; top: number }[] = (() => {
  const core = BUILDINGS_1825.filter((b) => b.core && b.w >= 7 && b.w <= 18);
  const out: { x: number; z: number; top: number }[] = [];
  for (let i = 0; i < core.length && out.length < 8; i += 3) {
    const b = core[i];
    /* dimnik ob severovzhodnem vogalu tlorisa */
    out.push({
      x: b.x + b.w / 2 - 1,
      z: b.z + b.d / 2 - 1,
      top: b.wallH + b.roofH,
    });
  }
  return out;
})();

/** P12 dokumentirana ugotovitev o hišnih številkah (za kartice stavb) */
export const HOUSENO_FINDING = {
  si: "Hišne številke na listu A02 niso zapisane — preverjeno (P12, 2026-10-08): slepi VLM testi stavb, analiza rdečih znamenj. Rdeče številke na listu so PARCELNE (ob jedru 1009–1106). Register hiš 1825 (PT) šteje ~80 lastnikov; povezava parcela↔hiša čaka branje PS (143 str.).",
  en: "House numbers are not written on sheet A02 — verified (P12, 2026-10-08): blind VLM tests of buildings, analysis of red marks. The red numbers on the sheet are PARCEL numbers (1009–1106 near the core). The 1825 house register (PT) holds ~80 owners; the parcel↔house link awaits reading the PS (143 pages).",
};
