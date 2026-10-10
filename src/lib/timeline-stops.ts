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
  1408, 1468, 1524, 1556, 1587, 1612, // srednji vek — Cerkvišče, Griblach (vas 1468), turški vpadi, čevljar
  // (1526 = prva omemba CERKVE sv. Vida, ne mejno leto zapisa — glej MVG-001/002/003)
  1669, 1679, // P22: matične knjige podzemeljske župnije (MVG-037/038) — arhiv rodbin na karti
  1750, 1800, 1809, 1813, 1843, 1848, 1850, 1854, 1857, 1869, 1873, 1875, 1876, 1879, 1880, 1885, 1890, 1891, 1894, 1898, 1899, // 19. stoletje (P22: zemljevidi 1843, Goranja lokva 1848, rudnik 1857, Matiček 1873; P25: hiša 1800, Milek 1850, šola/Kambič/Barle 1869, izseljenstvo 1880, Švarski 1885, žbul/križevo/Milek 1890, Sturm 1891, Katarina 1894, hiša do 1899)
  1903, 1907, 1908, 1914, 1917, 1918, 1920, 1927, 1928, 1929, 1933, 1937, 1941, 1943, 1944, 1945, 1947, 1950, // vojna doba in povojnje (P22: matične knjige do 1947, Matiček do 1950; P25: razglednica 1903, Dragoš 1907, jurjevo 1908, Švarski do 1917, španka 1918, tamburaši 1920/1929, pečnica 1928)
  1951, 1953, 1961, 1985, 1986, 1989, 1991, 1996, 1997, 2000, 2001, 2004, 2008, 2010, 2011, 2013, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, // druga polovica — danes (P22: Filak 1953, rudnik 1997, zvon 2008; P25: ŠD/močeril/Totter 1985/1986, tobak do 1989, DKŽ 1996, TD 2000, TULV/pajek 2001, pasuljada 2004, Valentina 2010, komasacija/lokostrelstvo/TULV 2013–2016, vrnitev 2019, Ciril Totter 2020, COVID 2021, učilnica 2022)
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
