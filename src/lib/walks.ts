/**
 * Vodeni sprehodi — izpeljani IZKLJUČNO iz obstoječih podatkov zbirke
 * (extra.json → walk: ime, številka postaje, kuratorsko besedilo).
 *
 * Pipeline: nov zapis, ki dobi `walk` (ime + postaja) ter lat/lng,
 * se v sprehodu samodejno prikaže z navigacijo — brez ročnega podvajanja.
 */

import { exhibits, getExtra, type Exhibit } from "./museum";

export interface WalkStop {
  station: number;
  slug: string;
  exhibit: Exhibit;
  /** kuratorsko besedilo postaje (iz extra.json) */
  note: string | null;
}

export interface WalkDef {
  /** ključ iz podatkov (ime sprehoda v extra.json brez predpone) */
  key: string;
  nameSi: string;
  nameEn: string;
  descSi: string;
  descEn: string;
  stops: WalkStop[];
}

/** Zemljevid SI → EN imen in opisov sprehodov (samo za prikaz). */
const WALK_META: Record<string, { en: string; dSi: string; dEn: string }> = {
  "Vas in njeni ljudje": {
    en: "The village and its people",
    dSi:
      "Glavna pot po vasi: od prve omembe 1468 prek cerkve, zvonov in ljudi do današnje razsvetljave.",
    dEn:
      "The main route through the village: from the first mention in 1468, past the church, bells and people, to today's street lights.",
  },
  "Iz Gribelj v svet": {
    en: "From Griblje into the world",
    dSi:
      "Gribeljci, ki so odšli v svet — učitelji, kozmopoliti, izumitelji in njihove poti nazaj.",
    dEn:
      "The people of Griblje who went out into the world — teachers, cosmopolitans, inventors, and their roads home.",
  },
  "Kruh, platno in vino": {
    en: "Bread, linen and wine",
    dSi:
      "Delo, ki je vas hranilo: njive, mlini, platno in trta — od zore do mraka.",
    dEn:
      "The work that fed the village: fields, mills, linen and vines — from dawn to dusk.",
  },
  "Vojna in svoboda": {
    en: "War and freedom",
    dSi:
      "Vojna krajina, zasede, letališče Otok in SNOS — pot skozi najtemnejša leta do svobode.",
    dEn:
      "The Military Frontier, ambushes, the Otok airfield and SNOS — the road through the darkest years to freedom.",
  },
  "Voda je življenje": {
    en: "Water is life",
    dSi:
      "Kolpa, mlini, ribnik in reka, ki se zavije — voda kot življenjska žila vasi.",
    dEn:
      "The Kolpa, mills, the pond and the river's bend — water as the village's lifeline.",
  },
};

/** Vsi sprehodi, razvrščeni po številu postaj (najdaljši najprej). */
export const WALKS: WalkDef[] = (() => {
  const byWalk = new Map<string, { station: number; slug: string; note: string | null }[]>();

  for (const ex of exhibits) {
    const extra = getExtra(ex.slug);
    const w = extra?.walk;
    if (!w?.name || w.station == null) continue;
    // ime v podatkih nosi predpono »Zapis na sprehodu« (izvoz izvorne baze)
    const key = w.name.startsWith("Zapis na sprehodu")
      ? w.name.slice("Zapis na sprehodu".length)
      : w.name;
    let list = byWalk.get(key);
    if (!list) {
      list = [];
      byWalk.set(key, list);
    }
    list.push({ station: w.station, slug: ex.slug, note: w.note });
  }

  const defs: WalkDef[] = [];
  for (const [key, rawStops] of byWalk) {
    rawStops.sort((a, b) => a.station - b.station);
    const stops: WalkStop[] = [];
    for (const s of rawStops) {
      const exhibit = exhibits.find((e) => e.slug === s.slug);
      if (!exhibit) continue;
      stops.push({ station: s.station, slug: s.slug, exhibit, note: s.note });
    }
    const meta = WALK_META[key];
    defs.push({
      key,
      nameSi: key,
      nameEn: meta?.en ?? key,
      descSi: meta?.dSi ?? "",
      descEn: meta?.dEn ?? "",
      stops,
    });
  }
  defs.sort((a, b) => b.stops.length - a.stops.length);
  return defs;
})();

/** Zapi, ki jih je sprehod postavil na karto (imajo koordinate). */
export function walkLocatedCount(w: WalkDef): number {
  return w.stops.filter((s) => s.exhibit.lat && s.exhibit.lng).length;
}
