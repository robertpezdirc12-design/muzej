/**
 * Postanki časovnega drsnika na zemljevidu (museum-map, način časovnega
 * potovanja). P18 — revizijski postavki 18/20.
 *
 * Vsak postanek je MEJNO leto zapisa zbirke (prvo oz. zadnje leto »od–do«
 * zapisa z GPS lokacijo). Ker se množica pik na karti (existsAt) spremeni
 * samo na mejnem letu, diskretni drsnik s postanki na VSEH mejnih letih
 * prikaže natanko enake množice kot prejšnji zvezni drsnik po letih —
 * ničesar ne izgubi, pridobi pa prazgodovino: prva tri postanka
 * (−1000, −800, −700) omogočajo pot do bronaste igle MVG-095 (−1000…−700),
 * ki je bila prej nedosegljiva (zvezni drsnik je šel šele od 1468, prve
 * pisne omembe vasi).
 *
 * Doslednost s podatki varuje test qa-p18-timeline-stops (src/lib/qa.ts):
 * če zbirki dodate zapis z novim mejnim letom, test pozove, da leto dodate
 * med postanke (oziroma ga samodejno razširi ta seznam).
 */

/** Urejeno naraščajoče; prvi element je prazgodovina, zadnji je "danes". */
export const YEAR_STOPS = [
  -1000, -800, -700, // prazgodovina: bronasta igla MVG-095, Kučar MVG-060
  1408, 1468, 1524, 1526, 1556, 1587, 1612, // srednji vek — Cerkvišče, Griblach, zaselki
  1750, 1809, 1813, 1854, 1875, 1876, 1879, 1898, // 19. stoletje
  1914, 1927, 1933, 1937, 1941, 1943, 1944, 1945, // vojna doba
  1951, 1961, 1991, 2011, 2017, 2023, 2024, 2025, 2026, // druga polovica — danes
] as const;

/**
 * Obljubljena zadnja vrednost (desni rob drsnika + začetno leto prikaza).
 * V zadnjem postanku mora biti enako letu "danes" (preverja QA).
 */
export const MAX_YEAR = 2026;

/**
 * Letnica za obiskovalca: −1000 → »1000 pr. n. št.« / »1000 BC«,
 * pozitivna ostane številka (oblika enaka časovnici, museum-timeline).
 */
export function formatStopYear(year: number, lang: "si" | "en"): string {
  if (year < 0) {
    return lang === "si" ? `${Math.abs(year)} pr. n. št.` : `${Math.abs(year)} BC`;
  }
  return String(year);
}
