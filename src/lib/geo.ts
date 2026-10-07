/**
 * Geodetski pripomočki za AR vodnika — čiste funkcije, brez odvisnosti.
 * Izračuni: haversinska razdalja, azimut (severna smer), formatiranje.
 */

export interface GeoFix {
  lat: number;
  lng: number;
  /** natančnost v metrih (1σ) */
  accuracy: number | null;
  /** smer gibanja v stopinjah (0 = sever), če jo naprava poda */
  heading: number | null;
  timestamp: number;
}

export interface GeoPoint {
  lat: number;
  lng: number;
}

const R = 6_371_000; // povprečni radij Zemlje v metrih

/** Haversinska razdalja med dvema točkama v metrih. */
export function distanceM(a: GeoPoint, b: GeoPoint): number {
  const φ1 = (a.lat * Math.PI) / 180;
  const φ2 = (b.lat * Math.PI) / 180;
  const dφ = φ2 - φ1;
  const dλ = ((b.lng - a.lng) * Math.PI) / 180;
  const h =
    Math.sin(dφ / 2) ** 2 +
    Math.cos(φ1) * Math.cos(φ2) * Math.sin(dλ / 2) ** 2;
  return 2 * R * Math.asin(Math.min(1, Math.sqrt(h)));
}

/** Azimut od a proti b v stopinjah [0, 360). 0 = sever, 90 = vzhod. */
export function bearingDeg(a: GeoPoint, b: GeoPoint): number {
  const φ1 = (a.lat * Math.PI) / 180;
  const φ2 = (b.lat * Math.PI) / 180;
  const dλ = ((b.lng - a.lng) * Math.PI) / 180;
  const y = Math.sin(dλ) * Math.cos(φ2);
  const x =
    Math.cos(φ1) * Math.sin(φ2) - Math.sin(φ1) * Math.cos(φ2) * Math.cos(dλ);
  const θ = Math.atan2(y, x);
  return (θ * (180 / Math.PI) + 360) % 360;
}

/** Relativni kot v stopinjah [−180, 180]: kotro vrtim komp, da gledam tarčo. */
export function angleDelta(from: number, to: number): number {
  return ((to - from + 540) % 360) - 180;
}

/** Osnovna smer kompasa za prikaz puščice (S/SV/Z/JZ …). */
export function compassLabelSi(deg: number): string {
  const labels = [
    "S", // sever
    "SV",
    "V",
    "JV",
    "J",
    "JZ",
    "Z",
    "SZ",
  ];
  return labels[Math.round(((deg % 360) + 360) % 360 / 45) % 8];
}

export function compassLabelEn(deg: string | number): string {
  const labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  const d = typeof deg === "number" ? deg : 0;
  return labels[Math.round(((d % 360) + 360) % 360 / 45) % 8];
}

/** Razdalja v človeški obliki: »35 m« / »2,4 km« / »2.4 km«. */
export function formatDistance(m: number, lang: "si" | "en"): string {
  if (m < 1000) {
    const v = Math.round(m / 5) * 5;
    return lang === "si" ? `${v} m` : `${v} m`;
  }
  const km = m / 1000;
  const v = km >= 10 ? Math.round(km) : Math.round(km * 10) / 10;
  const s = v.toLocaleString(lang === "si" ? "sl-SI" : "en-GB", {
    maximumFractionDigits: 1,
  });
  return `${s} km`;
}

/**
 * URL za pešaško navigacijo na OpenStreetMap.
 * `from` izpustimo, če GPS še ni priključen — OSM potem ponudi lastno lokacijo.
 */
export function osmDirectionsUrl(
  to: GeoPoint,
  from: GeoFix | null,
): string {
  const base = "https://www.openstreetmap.org/directions?engine=fossgis_osrm_foot";
  if (from) {
    return `${base}&route=${from.lat},${from.lng};${to.lat},${to.lng}`;
  }
  return `https://www.openstreetmap.org/?mlat=${to.lat}&mlon=${to.lng}#map=17/${to.lat}/${to.lng}`;
}

/** Povezava na točko na OSM (brez poti). */
export function osmMarkerUrl(p: GeoPoint): string {
  return `https://www.openstreetmap.org/?mlat=${p.lat}&mlon=${p.lng}#map=17/${p.lat}/${p.lng}`;
}
