// P254+P255+P256+P257: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (regenerirano P257: +11 blokov 1830/1831!; 2026-11-11)
// SINTEZNA FAZA: agregacija celotnega korpusa HOUSE_VITALS (2043 vitalov) po hišah čez VSEH 6 knjig:
// 01738 (poročna-predhodnik 1828 + 1829 + 1830 + 1831 + 1873 — P257: +11 blokov!) + 04104 (krstna-predzgodovina 1871–1885)
// + 04105 (krstna-linija 1887–1919) + 04455 (poročna 1873–1922) + 04106 (mrliška-predzgodovina 1857–1885)
// + 04894 (mrliška-linija 1886–1924). 100 hišnih oznak = 78 Griblje (1–78) + 16 druga-vas (79–98) + 6 neznanek.
// ★★★★★ P257: 23 ŠEST-KNJIŽ-HIŠ (P254-9 → P255-12 → P256-16 → P257-23 — NAJVEČJI-SKOK!):
// 3, 5, 6, 10, 11, 12, 16, 18, 19, 20, 22, 26, 27, 28, 32, 33, 56, 61, 62, 63, 65, 73, 1!
// ★★★★★ P257-10-DVIGOV: h54-37 (2.-vseh-časov!) + h56-36 + h27-33 + h11-32 + h1-30 + h26-28[~] + h33-28[~] + h3-27 + h50-27 (PEZDIRC-NIT-42-let!) + h65-26 (bila-prva-hiša-1857!) + h22-3.-zaporedno-leto-1830!
// Razponi: h6-96/h62-95/h50+h20+h22-93/h11+h33-91/h26-90 — bothEra-poročna 17→26. Dokaz: research/issue17/parish-house-stories.json; verifikator: scripts/p254_house_stories.py --check; regenerator: scripts/tmp/p257_gen.py.

export interface HouseStory {
  houseNo: string;
  kind: "griblje" | "druga-vas" | "neznano";
  /** skupno število vitalnih blokov hiše v korpusu */
  blocks: number;
  /** število različnih knjig s hišnim blokom (1–6) */
  books: number;
  perBook: { sig: string; n: number }[];
  firstYear: number;
  lastYear: number;
  span: number;
}

export interface HouseStoryBookMeta {
  sig: string;
  roleSi: string;
  roleEn: string;
  years: string;
  blocks: number;
  houses: number;
  recordSi: string;
}

export const HOUSE_STORY_BOOKS: HouseStoryBookMeta[] = [
  { sig: "01738", roleSi: "poročna-predhodnik", roleEn: "marriage predecessor", years: "1828 + 1829 + 1830 + 1831 + 1873", blocks: 31, houses: 26, recordSi: "P257: 10 dvigov 1831 (h54-37 = 2. vseh časov!) + h22-3.-zaporedno-leto-1830! · m2-PESDIRZ-h50 (PEZDIRC-NIT-42-let!)" },
  { sig: "04104", roleSi: "krstna-predzgodovina", roleEn: "baptism prehistory", years: "1871–1885", blocks: 288, houses: 72, recordSi: "h6 · h40 · h[?] (8 blokov vsak)" },
  { sig: "04105", roleSi: "krstna-linija", roleEn: "baptism line", years: "1887–1919", blocks: 502, houses: 89, recordSi: "h24 (18 blokov!)" },
  { sig: "04455", roleSi: "poročna-linija + predzgodovina", roleEn: "marriage line + prehistory", years: "1873–1922", blocks: 269, houses: 82, recordSi: "h27 SEGINA (8 blokov)" },
  { sig: "04106", roleSi: "mrliška-predzgodovina", roleEn: "death prehistory", years: "1857–1885", blocks: 433, houses: 78, recordSi: "h13 · h65 (14 blokov vsak)" },
  { sig: "04894", roleSi: "mrliška-linija", roleEn: "death line", years: "1886–1924", blocks: 520, houses: 92, recordSi: "h35 HRIŽAN (15 blokov!)" },
];

/** Vseh 100 hišnih oznak korpusa — Griblje (1–78) številsko, druga-vas (79–98), nato neznanke. */
export const HOUSE_STORIES: HouseStory[] = [
  { houseNo: "1", kind: "griblje", blocks: 42, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 8 }, { sig: "04105", n: 9 }, { sig: "04455", n: 7 }, { sig: "04106", n: 12 }, { sig: "04894", n: 5 }], firstYear: 1831, lastYear: 1914, span: 83 },
  { houseNo: "2", kind: "griblje", blocks: 32, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 6 }, { sig: "04455", n: 3 }, { sig: "04106", n: 7 }, { sig: "04894", n: 12 }], firstYear: 1858, lastYear: 1924, span: 66 },
  { houseNo: "3", kind: "griblje", blocks: 24, books: 6, perBook: [{ sig: "01738", n: 2 }, { sig: "04104", n: 4 }, { sig: "04105", n: 4 }, { sig: "04455", n: 2 }, { sig: "04106", n: 7 }, { sig: "04894", n: 5 }], firstYear: 1831, lastYear: 1917, span: 86 },
  { houseNo: "4", kind: "griblje", blocks: 7, books: 5, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 1 }, { sig: "04455", n: 2 }, { sig: "04106", n: 2 }, { sig: "04894", n: 1 }], firstYear: 1870, lastYear: 1906, span: 36 },
  { houseNo: "5", kind: "griblje", blocks: 32, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 5 }, { sig: "04105", n: 9 }, { sig: "04455", n: 1 }, { sig: "04106", n: 10 }, { sig: "04894", n: 6 }], firstYear: 1829, lastYear: 1919, span: 90 },
  { houseNo: "6", kind: "griblje", blocks: 36, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 8 }, { sig: "04105", n: 8 }, { sig: "04455", n: 5 }, { sig: "04106", n: 6 }, { sig: "04894", n: 8 }], firstYear: 1828, lastYear: 1924, span: 96 },
  { houseNo: "7", kind: "griblje", blocks: 24, books: 5, perBook: [{ sig: "04104", n: 6 }, { sig: "04105", n: 4 }, { sig: "04455", n: 5 }, { sig: "04106", n: 6 }, { sig: "04894", n: 3 }], firstYear: 1867, lastYear: 1921, span: 54 },
  { houseNo: "8", kind: "griblje", blocks: 38, books: 5, perBook: [{ sig: "04104", n: 6 }, { sig: "04105", n: 7 }, { sig: "04455", n: 7 }, { sig: "04106", n: 11 }, { sig: "04894", n: 7 }], firstYear: 1871, lastYear: 1919, span: 48 },
  { houseNo: "9", kind: "griblje", blocks: 23, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 5 }, { sig: "04455", n: 3 }, { sig: "04106", n: 3 }, { sig: "04894", n: 7 }], firstYear: 1862, lastYear: 1922, span: 60 },
  { houseNo: "10", kind: "griblje", blocks: 30, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 2 }, { sig: "04105", n: 6 }, { sig: "04455", n: 7 }, { sig: "04106", n: 11 }, { sig: "04894", n: 3 }], firstYear: 1862, lastYear: 1921, span: 59 },
  { houseNo: "11", kind: "griblje", blocks: 31, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 7 }, { sig: "04105", n: 7 }, { sig: "04455", n: 3 }, { sig: "04106", n: 7 }, { sig: "04894", n: 6 }], firstYear: 1831, lastYear: 1922, span: 91 },
  { houseNo: "12", kind: "griblje", blocks: 28, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 3 }, { sig: "04105", n: 14 }, { sig: "04455", n: 1 }, { sig: "04106", n: 3 }, { sig: "04894", n: 6 }], firstYear: 1869, lastYear: 1919, span: 50 },
  { houseNo: "13", kind: "griblje", blocks: 39, books: 5, perBook: [{ sig: "04104", n: 8 }, { sig: "04105", n: 7 }, { sig: "04455", n: 5 }, { sig: "04106", n: 14 }, { sig: "04894", n: 5 }], firstYear: 1857, lastYear: 1923, span: 66 },
  { houseNo: "14", kind: "griblje", blocks: 33, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 8 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 13 }], firstYear: 1861, lastYear: 1923, span: 62 },
  { houseNo: "15", kind: "griblje", blocks: 19, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 6 }, { sig: "04455", n: 4 }, { sig: "04106", n: 2 }, { sig: "04894", n: 5 }], firstYear: 1868, lastYear: 1921, span: 53 },
  { houseNo: "16", kind: "griblje", blocks: 34, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 5 }, { sig: "04105", n: 8 }, { sig: "04455", n: 6 }, { sig: "04106", n: 5 }, { sig: "04894", n: 9 }], firstYear: 1864, lastYear: 1924, span: 60 },
  { houseNo: "17", kind: "griblje", blocks: 18, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 3 }, { sig: "04455", n: 3 }, { sig: "04106", n: 3 }, { sig: "04894", n: 4 }], firstYear: 1875, lastYear: 1923, span: 48 },
  { houseNo: "18", kind: "griblje", blocks: 36, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 5 }, { sig: "04105", n: 6 }, { sig: "04455", n: 5 }, { sig: "04106", n: 10 }, { sig: "04894", n: 9 }], firstYear: 1861, lastYear: 1922, span: 61 },
  { houseNo: "19", kind: "griblje", blocks: 22, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 3 }, { sig: "04105", n: 3 }, { sig: "04455", n: 1 }, { sig: "04106", n: 9 }, { sig: "04894", n: 5 }], firstYear: 1829, lastYear: 1918, span: 89 },
  { houseNo: "20", kind: "griblje", blocks: 35, books: 6, perBook: [{ sig: "01738", n: 2 }, { sig: "04104", n: 5 }, { sig: "04105", n: 5 }, { sig: "04455", n: 4 }, { sig: "04106", n: 11 }, { sig: "04894", n: 8 }], firstYear: 1829, lastYear: 1922, span: 93 },
  { houseNo: "21", kind: "griblje", blocks: 38, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 10 }, { sig: "04455", n: 6 }, { sig: "04106", n: 9 }, { sig: "04894", n: 10 }], firstYear: 1859, lastYear: 1922, span: 63 },
  { houseNo: "22", kind: "griblje", blocks: 35, books: 6, perBook: [{ sig: "01738", n: 3 }, { sig: "04104", n: 7 }, { sig: "04105", n: 7 }, { sig: "04455", n: 5 }, { sig: "04106", n: 6 }, { sig: "04894", n: 7 }], firstYear: 1828, lastYear: 1921, span: 93 },
  { houseNo: "23", kind: "griblje", blocks: 22, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 7 }, { sig: "04455", n: 4 }, { sig: "04106", n: 3 }, { sig: "04894", n: 4 }], firstYear: 1865, lastYear: 1922, span: 57 },
  { houseNo: "24", kind: "griblje", blocks: 45, books: 5, perBook: [{ sig: "04104", n: 8 }, { sig: "04105", n: 18 }, { sig: "04455", n: 5 }, { sig: "04106", n: 5 }, { sig: "04894", n: 9 }], firstYear: 1859, lastYear: 1920, span: 61 },
  { houseNo: "25", kind: "griblje", blocks: 18, books: 5, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 3 }, { sig: "04105", n: 5 }, { sig: "04455", n: 2 }, { sig: "04894", n: 7 }], firstYear: 1873, lastYear: 1923, span: 50 },
  { houseNo: "26", kind: "griblje", blocks: 27, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 1 }, { sig: "04105", n: 5 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 12 }], firstYear: 1831, lastYear: 1921, span: 90 },
  { houseNo: "27", kind: "griblje", blocks: 30, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 3 }, { sig: "04105", n: 9 }, { sig: "04455", n: 8 }, { sig: "04106", n: 4 }, { sig: "04894", n: 5 }], firstYear: 1831, lastYear: 1918, span: 87 },
  { houseNo: "28", kind: "griblje", blocks: 26, books: 6, perBook: [{ sig: "01738", n: 2 }, { sig: "04104", n: 7 }, { sig: "04105", n: 3 }, { sig: "04455", n: 3 }, { sig: "04106", n: 7 }, { sig: "04894", n: 4 }], firstYear: 1865, lastYear: 1917, span: 52 },
  { houseNo: "29", kind: "griblje", blocks: 23, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 4 }, { sig: "04455", n: 3 }, { sig: "04106", n: 4 }, { sig: "04894", n: 7 }], firstYear: 1859, lastYear: 1921, span: 62 },
  { houseNo: "30", kind: "griblje", blocks: 40, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 14 }, { sig: "04455", n: 7 }, { sig: "04106", n: 6 }, { sig: "04894", n: 9 }], firstYear: 1860, lastYear: 1918, span: 58 },
  { houseNo: "31", kind: "griblje", blocks: 42, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 13 }, { sig: "04455", n: 7 }, { sig: "04106", n: 7 }, { sig: "04894", n: 10 }], firstYear: 1857, lastYear: 1921, span: 64 },
  { houseNo: "32", kind: "griblje", blocks: 27, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 1 }, { sig: "04105", n: 11 }, { sig: "04455", n: 4 }, { sig: "04106", n: 4 }, { sig: "04894", n: 6 }], firstYear: 1829, lastYear: 1915, span: 86 },
  { houseNo: "33", kind: "griblje", blocks: 31, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 4 }, { sig: "04105", n: 5 }, { sig: "04455", n: 5 }, { sig: "04106", n: 7 }, { sig: "04894", n: 9 }], firstYear: 1831, lastYear: 1922, span: 91 },
  { houseNo: "34", kind: "griblje", blocks: 35, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 11 }, { sig: "04455", n: 5 }, { sig: "04106", n: 5 }, { sig: "04894", n: 11 }], firstYear: 1864, lastYear: 1918, span: 54 },
  { houseNo: "35", kind: "griblje", blocks: 35, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 7 }, { sig: "04455", n: 5 }, { sig: "04106", n: 3 }, { sig: "04894", n: 15 }], firstYear: 1867, lastYear: 1922, span: 55 },
  { houseNo: "36", kind: "griblje", blocks: 33, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 12 }, { sig: "04455", n: 4 }, { sig: "04106", n: 6 }, { sig: "04894", n: 9 }], firstYear: 1857, lastYear: 1917, span: 60 },
  { houseNo: "37", kind: "griblje", blocks: 28, books: 5, perBook: [{ sig: "04104", n: 7 }, { sig: "04105", n: 4 }, { sig: "04455", n: 2 }, { sig: "04106", n: 10 }, { sig: "04894", n: 5 }], firstYear: 1859, lastYear: 1918, span: 59 },
  { houseNo: "38", kind: "griblje", blocks: 16, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 1 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 3 }], firstYear: 1867, lastYear: 1904, span: 37 },
  { houseNo: "39", kind: "griblje", blocks: 16, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 2 }, { sig: "04455", n: 3 }, { sig: "04106", n: 4 }, { sig: "04894", n: 3 }], firstYear: 1859, lastYear: 1912, span: 53 },
  { houseNo: "40", kind: "griblje", blocks: 28, books: 5, perBook: [{ sig: "04104", n: 8 }, { sig: "04105", n: 7 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 5 }], firstYear: 1867, lastYear: 1919, span: 52 },
  { houseNo: "41", kind: "griblje", blocks: 22, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 5 }, { sig: "04455", n: 4 }, { sig: "04106", n: 4 }, { sig: "04894", n: 7 }], firstYear: 1866, lastYear: 1921, span: 55 },
  { houseNo: "42", kind: "griblje", blocks: 27, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 5 }, { sig: "04455", n: 5 }, { sig: "04106", n: 6 }, { sig: "04894", n: 8 }], firstYear: 1861, lastYear: 1912, span: 51 },
  { houseNo: "43", kind: "griblje", blocks: 16, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 2 }, { sig: "04455", n: 2 }, { sig: "04106", n: 3 }, { sig: "04894", n: 5 }], firstYear: 1873, lastYear: 1924, span: 51 },
  { houseNo: "44", kind: "griblje", blocks: 39, books: 5, perBook: [{ sig: "04104", n: 6 }, { sig: "04105", n: 8 }, { sig: "04455", n: 6 }, { sig: "04106", n: 12 }, { sig: "04894", n: 7 }], firstYear: 1858, lastYear: 1923, span: 65 },
  { houseNo: "45", kind: "griblje", blocks: 21, books: 4, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 8 }, { sig: "04106", n: 2 }, { sig: "04894", n: 9 }], firstYear: 1864, lastYear: 1924, span: 60 },
  { houseNo: "46", kind: "griblje", blocks: 38, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 12 }, { sig: "04455", n: 7 }, { sig: "04106", n: 4 }, { sig: "04894", n: 11 }], firstYear: 1867, lastYear: 1920, span: 53 },
  { houseNo: "47", kind: "griblje", blocks: 18, books: 5, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 5 }, { sig: "04455", n: 2 }, { sig: "04106", n: 7 }, { sig: "04894", n: 3 }], firstYear: 1862, lastYear: 1919, span: 57 },
  { houseNo: "48", kind: "griblje", blocks: 32, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 8 }, { sig: "04455", n: 4 }, { sig: "04106", n: 8 }, { sig: "04894", n: 7 }], firstYear: 1857, lastYear: 1922, span: 65 },
  { houseNo: "49", kind: "griblje", blocks: 28, books: 4, perBook: [{ sig: "04104", n: 7 }, { sig: "04105", n: 6 }, { sig: "04106", n: 7 }, { sig: "04894", n: 8 }], firstYear: 1858, lastYear: 1918, span: 60 },
  { houseNo: "50", kind: "griblje", blocks: 12, books: 5, perBook: [{ sig: "01738", n: 1 }, { sig: "04105", n: 1 }, { sig: "04455", n: 3 }, { sig: "04106", n: 6 }, { sig: "04894", n: 1 }], firstYear: 1831, lastYear: 1924, span: 93 },
  { houseNo: "51", kind: "griblje", blocks: 11, books: 4, perBook: [{ sig: "04104", n: 2 }, { sig: "04455", n: 2 }, { sig: "04106", n: 3 }, { sig: "04894", n: 4 }], firstYear: 1867, lastYear: 1913, span: 46 },
  { houseNo: "52", kind: "griblje", blocks: 14, books: 4, perBook: [{ sig: "04105", n: 3 }, { sig: "04455", n: 2 }, { sig: "04106", n: 5 }, { sig: "04894", n: 4 }], firstYear: 1857, lastYear: 1908, span: 51 },
  { houseNo: "53", kind: "griblje", blocks: 33, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 7 }, { sig: "04455", n: 4 }, { sig: "04106", n: 6 }, { sig: "04894", n: 11 }], firstYear: 1863, lastYear: 1924, span: 61 },
  { houseNo: "54", kind: "griblje", blocks: 18, books: 5, perBook: [{ sig: "01738", n: 1 }, { sig: "04105", n: 6 }, { sig: "04455", n: 3 }, { sig: "04106", n: 6 }, { sig: "04894", n: 2 }], firstYear: 1831, lastYear: 1917, span: 86 },
  { houseNo: "55", kind: "griblje", blocks: 18, books: 4, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 3 }, { sig: "04106", n: 6 }, { sig: "04894", n: 4 }], firstYear: 1860, lastYear: 1924, span: 64 },
  { houseNo: "56", kind: "griblje", blocks: 14, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 2 }, { sig: "04105", n: 3 }, { sig: "04455", n: 3 }, { sig: "04106", n: 3 }, { sig: "04894", n: 2 }], firstYear: 1831, lastYear: 1908, span: 77 },
  { houseNo: "57", kind: "griblje", blocks: 21, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 5 }, { sig: "04455", n: 1 }, { sig: "04106", n: 7 }, { sig: "04894", n: 6 }], firstYear: 1859, lastYear: 1912, span: 53 },
  { houseNo: "58", kind: "griblje", blocks: 28, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 8 }, { sig: "04455", n: 2 }, { sig: "04106", n: 5 }, { sig: "04894", n: 11 }], firstYear: 1859, lastYear: 1918, span: 59 },
  { houseNo: "59", kind: "griblje", blocks: 10, books: 4, perBook: [{ sig: "04105", n: 4 }, { sig: "04455", n: 1 }, { sig: "04106", n: 1 }, { sig: "04894", n: 4 }], firstYear: 1875, lastYear: 1921, span: 46 },
  { houseNo: "60", kind: "griblje", blocks: 30, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 9 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 10 }], firstYear: 1857, lastYear: 1923, span: 66 },
  { houseNo: "61", kind: "griblje", blocks: 17, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 1 }, { sig: "04105", n: 4 }, { sig: "04455", n: 3 }, { sig: "04106", n: 2 }, { sig: "04894", n: 6 }], firstYear: 1828, lastYear: 1919, span: 91 },
  { houseNo: "62", kind: "griblje", blocks: 29, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 6 }, { sig: "04105", n: 4 }, { sig: "04455", n: 6 }, { sig: "04106", n: 6 }, { sig: "04894", n: 6 }], firstYear: 1829, lastYear: 1924, span: 95 },
  { houseNo: "63", kind: "griblje", blocks: 29, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 4 }, { sig: "04105", n: 8 }, { sig: "04455", n: 5 }, { sig: "04106", n: 7 }, { sig: "04894", n: 4 }], firstYear: 1862, lastYear: 1921, span: 59 },
  { houseNo: "64", kind: "griblje", blocks: 20, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 2 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 7 }], firstYear: 1857, lastYear: 1923, span: 66 },
  { houseNo: "65", kind: "griblje", blocks: 44, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 4 }, { sig: "04105", n: 11 }, { sig: "04455", n: 5 }, { sig: "04106", n: 14 }, { sig: "04894", n: 9 }], firstYear: 1831, lastYear: 1914, span: 83 },
  { houseNo: "66", kind: "griblje", blocks: 13, books: 4, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 4 }, { sig: "04106", n: 5 }, { sig: "04894", n: 2 }], firstYear: 1868, lastYear: 1909, span: 41 },
  { houseNo: "67", kind: "griblje", blocks: 5, books: 3, perBook: [{ sig: "04105", n: 1 }, { sig: "04455", n: 1 }, { sig: "04106", n: 3 }], firstYear: 1861, lastYear: 1900, span: 39 },
  { houseNo: "68", kind: "griblje", blocks: 19, books: 4, perBook: [{ sig: "04104", n: 6 }, { sig: "04455", n: 2 }, { sig: "04106", n: 8 }, { sig: "04894", n: 3 }], firstYear: 1861, lastYear: 1924, span: 63 },
  { houseNo: "69", kind: "griblje", blocks: 26, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 8 }, { sig: "04455", n: 3 }, { sig: "04106", n: 6 }, { sig: "04894", n: 5 }], firstYear: 1859, lastYear: 1924, span: 65 },
  { houseNo: "70", kind: "griblje", blocks: 9, books: 4, perBook: [{ sig: "04105", n: 3 }, { sig: "04455", n: 1 }, { sig: "04106", n: 3 }, { sig: "04894", n: 2 }], firstYear: 1865, lastYear: 1924, span: 59 },
  { houseNo: "71", kind: "griblje", blocks: 13, books: 4, perBook: [{ sig: "04105", n: 4 }, { sig: "04455", n: 3 }, { sig: "04106", n: 1 }, { sig: "04894", n: 5 }], firstYear: 1864, lastYear: 1923, span: 59 },
  { houseNo: "72", kind: "griblje", blocks: 25, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 8 }, { sig: "04455", n: 1 }, { sig: "04106", n: 5 }, { sig: "04894", n: 9 }], firstYear: 1869, lastYear: 1921, span: 52 },
  { houseNo: "73", kind: "griblje", blocks: 9, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 2 }, { sig: "04105", n: 2 }, { sig: "04455", n: 1 }, { sig: "04106", n: 2 }, { sig: "04894", n: 1 }], firstYear: 1869, lastYear: 1921, span: 52 },
  { houseNo: "74", kind: "griblje", blocks: 13, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 2 }, { sig: "04455", n: 2 }, { sig: "04106", n: 2 }, { sig: "04894", n: 4 }], firstYear: 1859, lastYear: 1918, span: 59 },
  { houseNo: "75", kind: "griblje", blocks: 6, books: 3, perBook: [{ sig: "04105", n: 3 }, { sig: "04106", n: 1 }, { sig: "04894", n: 2 }], firstYear: 1876, lastYear: 1920, span: 44 },
  { houseNo: "76", kind: "griblje", blocks: 4, books: 3, perBook: [{ sig: "04105", n: 1 }, { sig: "04455", n: 1 }, { sig: "04894", n: 2 }], firstYear: 1887, lastYear: 1913, span: 26 },
  { houseNo: "77", kind: "griblje", blocks: 10, books: 4, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 5 }, { sig: "04455", n: 1 }, { sig: "04894", n: 3 }], firstYear: 1878, lastYear: 1921, span: 43 },
  { houseNo: "78", kind: "griblje", blocks: 12, books: 5, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 3 }, { sig: "04455", n: 1 }, { sig: "04106", n: 4 }, { sig: "04894", n: 3 }], firstYear: 1877, lastYear: 1923, span: 46 },
  { houseNo: "79", kind: "druga-vas", blocks: 2, books: 2, perBook: [{ sig: "04105", n: 1 }, { sig: "04894", n: 1 }], firstYear: 1888, lastYear: 1912, span: 24 },
  { houseNo: "80", kind: "druga-vas", blocks: 1, books: 1, perBook: [{ sig: "04894", n: 1 }], firstYear: 1892, lastYear: 1892, span: 0 },
  { houseNo: "81", kind: "druga-vas", blocks: 4, books: 2, perBook: [{ sig: "04105", n: 1 }, { sig: "04894", n: 3 }], firstYear: 1900, lastYear: 1919, span: 19 },
  { houseNo: "82", kind: "druga-vas", blocks: 6, books: 3, perBook: [{ sig: "04105", n: 2 }, { sig: "04455", n: 1 }, { sig: "04894", n: 3 }], firstYear: 1899, lastYear: 1921, span: 22 },
  { houseNo: "83", kind: "druga-vas", blocks: 8, books: 2, perBook: [{ sig: "04105", n: 4 }, { sig: "04894", n: 4 }], firstYear: 1888, lastYear: 1908, span: 20 },
  { houseNo: "84", kind: "druga-vas", blocks: 1, books: 1, perBook: [{ sig: "04894", n: 1 }], firstYear: 1919, lastYear: 1919, span: 0 },
  { houseNo: "85", kind: "druga-vas", blocks: 5, books: 2, perBook: [{ sig: "04105", n: 2 }, { sig: "04894", n: 3 }], firstYear: 1888, lastYear: 1909, span: 21 },
  { houseNo: "86", kind: "druga-vas", blocks: 7, books: 4, perBook: [{ sig: "04105", n: 3 }, { sig: "04455", n: 1 }, { sig: "04106", n: 1 }, { sig: "04894", n: 2 }], firstYear: 1874, lastYear: 1920, span: 46 },
  { houseNo: "87", kind: "druga-vas", blocks: 10, books: 3, perBook: [{ sig: "04105", n: 3 }, { sig: "04455", n: 2 }, { sig: "04894", n: 5 }], firstYear: 1889, lastYear: 1912, span: 23 },
  { houseNo: "88", kind: "druga-vas", blocks: 12, books: 2, perBook: [{ sig: "04105", n: 6 }, { sig: "04894", n: 6 }], firstYear: 1886, lastYear: 1924, span: 38 },
  { houseNo: "89", kind: "druga-vas", blocks: 2, books: 2, perBook: [{ sig: "04105", n: 1 }, { sig: "04894", n: 1 }], firstYear: 1893, lastYear: 1898, span: 5 },
  { houseNo: "90", kind: "druga-vas", blocks: 16, books: 3, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 9 }, { sig: "04894", n: 6 }], firstYear: 1883, lastYear: 1919, span: 36 },
  { houseNo: "91", kind: "druga-vas", blocks: 16, books: 3, perBook: [{ sig: "04105", n: 6 }, { sig: "04455", n: 3 }, { sig: "04894", n: 7 }], firstYear: 1890, lastYear: 1914, span: 24 },
  { houseNo: "92", kind: "druga-vas", blocks: 3, books: 2, perBook: [{ sig: "04455", n: 1 }, { sig: "04894", n: 2 }], firstYear: 1913, lastYear: 1921, span: 8 },
  { houseNo: "94", kind: "druga-vas", blocks: 3, books: 3, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 1 }, { sig: "04106", n: 1 }], firstYear: 1873, lastYear: 1886, span: 13 },
  { houseNo: "98", kind: "druga-vas", blocks: 1, books: 1, perBook: [{ sig: "04894", n: 1 }], firstYear: 1893, lastYear: 1893, span: 0 },
  { houseNo: "13 [~]", kind: "neznano", blocks: 1, books: 1, perBook: [{ sig: "04455", n: 1 }], firstYear: 1879, lastYear: 1879, span: 0 },
  { houseNo: "17 [~]", kind: "neznano", blocks: 1, books: 1, perBook: [{ sig: "04455", n: 1 }], firstYear: 1879, lastYear: 1879, span: 0 },
  { houseNo: "32 [~]", kind: "neznano", blocks: 1, books: 1, perBook: [{ sig: "04455", n: 1 }], firstYear: 1879, lastYear: 1879, span: 0 },
  { houseNo: "29 [~X-OPEN]", kind: "neznano", blocks: 1, books: 1, perBook: [{ sig: "04455", n: 1 }], firstYear: 1885, lastYear: 1885, span: 0 },
  { houseNo: "[?]", kind: "neznano", blocks: 10, books: 2, perBook: [{ sig: "04104", n: 8 }, { sig: "04106", n: 2 }], firstYear: 1857, lastYear: 1885, span: 28 },
  { houseNo: "sub dioe.", kind: "neznano", blocks: 1, books: 1, perBook: [{ sig: "04105", n: 1 }], firstYear: 1918, lastYear: 1918, span: 0 },
];

export function houseStoryByNo(no: string): HouseStory | undefined {
  return HOUSE_STORIES.find((h) => h.houseNo === no);
}

export interface HouseStorySix {
  houseNo: string;
  blocks: number;
  years: string;
  storySi: string;
  storyEn: string;
}

/** ★★★★★ 23 ŠEST-KNJIŽ-HIŠ (P257!) — blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste). */
export const HOUSE_STORY_SIX: HouseStorySix[] = [
  { houseNo: "1", blocks: 42, years: "1831–1914", storySi: "★★★ P257-hiša: m13-1831-ŽENIN-Math.-[Ianigl?~Muniz/Kranigh — 3-variant-GARBLE!] (ledina, GRIBLJE 1 × [Podierz?]-h11 — POLNI-DVOJNI!) — h1-firstYear-1861→1831 (DVIG 30!); 42 blokov 1831–1914 = 83 let (11 v 04106!); [~Muniz?-MUZ-kand. (1828-Semelj-nit!)]; h1 = ena-najstarejših-hiš-Griblja-številka-1!", storyEn: "★★★ The P257 house: the m13-1831 GROOM Math. [Ianigl?~3-variant-GARBLE!] (GRIBLJE 1 × the h11-bride — the FULL DOUBLE!) — the h1-firstYear-1861→1831 (LIFT 30!); 42 blocks 1831–1914 = 83 years (11 in 04106!); [~Muniz?-a-MUZ-cand.!]; h1 = the lowest Griblje house-number!" },
  { houseNo: "3", blocks: 24, years: "1831–1917", storySi: "HRIŽAN/KRIŽAN-hiša: ★★★★★ P257: m1-1831-ŽENIN-Peter-KRIŽAN (GRIBLJE 3 × [Dehligl?]-h33 — POLNI-DVOJNI!) + ★-mati-neveste-Dorothea-KRIŽAN = KRIŽAN-×2-V-ENI-VRSTICI! — h3-firstYear-1858→1831 (DVIG 27!) + 24 blokov 1831–1917 = 86 let; Peter-Hrižan krstni oče 1872–1881 (4 krsti) + †1888 Peter Križar/Križan 80 let; 1864 Georg DRAGOŠ †70 (najstarejša omemba); m11-HLEBEC-1873 (P253!); 1907 PEZDIREC-poroka.", storyEn: "The HRIŽAN/KRIŽAN house: ★★★★★ P257: the m1-1831 GROOM Peter KRIŽAN (GRIBLJE 3 — the FULL DOUBLE!) + the bride's mother Dorothea KRIŽAN = KRIŽAN-TWICE-IN-ONE-ROW! — the h3-firstYear-1858→1831 (LIFT 27!) + 24 blocks 1831–1917 = 86 years; Peter Hrižan the baptismal father 1872–1881 + Peter Križan †1888 aged 80; Georg DRAGOŠ †70 in 1864 (the oldest mention); the m11-HLEBEC-1873 (P253!); a PEZDIREC marriage 1907." },
  { houseNo: "5", blocks: 32, years: "1829–1919", storySi: "MÜLLER-hiša: m10-1829 ženin Mathe MÜLLER (26 l, GRIBLJE 5 × [Šimek?]-h19 — POLNI-DVOJNI, P256!) — h5-firstYear-1859→1829 (DVIG 30!); 31 blokov 1829–1924 — h5-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!); MÜLLER-×2-družini-1829 (h5-hiša + h22-Millerji!).", storyEn: "The MÜLLER house: the m10-1829 groom Mathe MÜLLER (26, GRIBLJE 5 × the h19-bride — the FULL DOUBLE, P256!) — the h5-firstYear-1859→1829 (LIFT 30!); 31 blocks 1829–1924 — h5-ENTERS-THE-SIX-BOOKS-CLUB (P256!); the MÜLLER-×2-families-of-1829 (the h5-house + the h22-Millers!)." },
  { houseNo: "6", blocks: 36, years: "1828–1924", storySi: "NAJDALJŠA-HIŠA-KORPUSA (96 let!): m6-1828-nevesta-Maria-[Jan/Spin]-GRIBLJE-6 × ženin-Jure-STARA = PRVI-GRIBLJE-VPIS-PREDHODNIKA-01738 (P255 — korpus 1857→1828!); h6-firstYear-1860→1828 (DVIG 32!); 04104-trospec (8) + 04106 (6) + 04455 (5 porok!) + 04105 (8) + 04894 (8) = 36 blokov 1828–1924 čez VSEH 6 knjig!", storyEn: "THE-LONGEST-SPAN-HOUSE-OF-THE-CORPUS (96 years!): the m6-1828 bride Maria-GRIBLJE-6 × groom Jure-STARA = the FIRST Griblje entry of the 01738 predecessor (P255 — the corpus 1857→1828!); the h6-firstYear-1860→1828 (LIFT 32!); 36 blocks 1828–1924 across ALL 6 books!" },
  { houseNo: "10", blocks: 30, years: "1862–1921", storySi: "MUC-hiša: m6-1873 poroka neveste Muc — KOLBEZEN h16 × MUC h10 polni dvojni (P253!); KRAUE-h10 52-letna nevesta 1874 = NAJSTAREJŠA PREDZGODOVINE (P250!); 11 mrliških blokov 04106 (1857–1885) — med najglobljimi smrtnimi zgodovinami.", storyEn: "The MUC house: the m6-1873 marriage of a Muc bride — KOLBEZEN h16 × MUC h10 the full double (P253!); the 52-year-old bride of 1874 = THE OLDEST OF THE PREHISTORY (P250!); 11 death blocks 04106 (1857–1885) — among the deepest death histories." },
  { houseNo: "11", blocks: 31, years: "1831–1922", storySi: "★★★ P257-hiša: m13-1831-NEVESTA-Catharina-[Podierz?~Pesdirz!—DUEL-'Pesdirz-ali-Podierz'] (ledina, GRIBLJE 11 × [Ianigl?]-h1 — POLNI-DVOJNI!) — h11-firstYear-1863→1831 (DVIG 32!); 31 blokov 1831–1922 = 91 let (IZENAČI-h33!-4.-5.-mesto); Pesdirz/Podierz-nit-1831-×4-vrstice (m2/m3/m7/m13!); 04104-prazna (4-knjige→5-01738-P257!→6?)", storyEn: "★★★ The P257 house: the m13-1831 BRIDE Catharina [Podierz?~Pesdirz!] (GRIBLJE 11 × the h1-groom — the FULL DOUBLE!) — the h11-firstYear-1863→1831 (LIFT 32!); 31 blocks 1831–1922 = 91 years (ties-h33!); the-Pesdirz-thread-1831-×4-rows (m2/m3/m7/m13!)" },
  { houseNo: "12", blocks: 28, years: "1869–1919", storySi: "DRAGOŠ-50-LET: 1869 Michael Dragos †27 → 1871 Joannes Dragoš krstni oče (z46!) → 1919 Franc DRAGOS poroka + Vincencij DRAGOS † — ISTA DRUŽINA 1869–1919! + PEZDIRC-continuum (z59-1872, P235!); 14 blokov v 04105 = 2.-največ v knjigi.", storyEn: "The DRAGOŠ 50 YEARS: 1869 Michael Dragos †27 → 1871 Joannes Dragoš the baptismal father (z46!) → 1919 Franc DRAGOS marries + Vincencij DRAGOS † — THE SAME FAMILY 1869–1919! + the PEZDIRC continuum (z59-1872, P235!); 14 blocks in 04105 = the 2nd most of the book." },
  { houseNo: "16", blocks: 34, years: "1864–1924", storySi: "KOLBEZEN-hiša: m6-1873 ženin Georg KOLBEZEN (h16 × h10 polni dvojni, P253!); 1918 Ana FILAK roj. NEMANIČ †75 (poročena 1879!); 1924 Alojzy NOVAK †27. 9. — zadnja leta mrliške linije (04894 se konča 31. 12. 1924, P190!).", storyEn: "The KOLBEZEN house: the m6-1873 groom Georg KOLBEZEN (h16 × h10 the full double, P253!); Ana FILAK née NEMANIČ †75 in 1918 (married 1879!); Alojzy NOVAK †Sep 27 1924 — the final years of the death line (04894 ends Dec 31 1924, P190!)." },
  { houseNo: "18", blocks: 36, years: "1861–1922", storySi: "ŠIMEC-hiša (P246-h18-ŠIMEC-1:1!): 1863 Georg Simic †53; 1878 dve INTRA-poroki v 1 letu (h18 × h65, P246!); 1921 Karolina PEZDIRC †1,3 (zadnji PEZDIRC-blok hiše); 36 blokov = najglasnejša šest-knjižna hiša (skupaj z h6!).", storyEn: "The ŠIMEC house (P246-h18-ŠIMEC-1:1!): Georg Simic †53 in 1863; two INTRA-marriages in one year 1878 (h18 × h65, P246!); Karolina PEZDIRC †1.3 in 1921 (the house's last PEZDIRC block); 36 blocks = the loudest six-book house (together with h6!)." },
  { houseNo: "19", blocks: 22, years: "1829–1918", storySi: "[ŠIMEK?]-hiša: m10-1829 nevesta Maria [ŠIMEK?~Knimek/Thimnik — 4-branja-DUEL!] (21 l, GRIBLJE 19 × Müller-h5, P256!) — oče Georg [Šimek?~'Shimek'-garble — ŠIMEC-marker-kand.!] + mati [Salva?] TILLAR! (TILLAR-NIT-1829!); h19-firstYear-1858→1829 (DVIG 29!) — h19-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (P256!).", storyEn: "The [ŠIMEK?] house: the m10-1829 bride Maria [ŠIMEK?~4-reads-DUEL!] (21, GRIBLJE 19 × the Müller-h5, P256!) — the father Georg [Šimek?~garble] + the mother [Salva?] TILLAR! (the-1829-TILLAR-thread!); the h19-firstYear-1858→1829 (LIFT 29!) — h19-ENTERS-THE-SIX-BOOKS-CLUB (P256!)." },
  { houseNo: "20", blocks: 35, years: "1829–1922", storySi: "BORŠT-h20: ★★★ P256: m2-1829 [MALEŠIČ?]-nevesta (Griblje 20 × [Dehlič?]-h32 — POLNI-DVOJNI!) = h20-ŽE-DRUGI-01738-blok (1829+1873-m7-P253!) — h20-firstYear-1859→1829 (DVIG 30!) + span-1829–1922 = 93-let (IZENAČI-h22 — delita-2.-3.-mesto!); z72/z73 DVOJČKI 1871 = 1. DVOJČKI KRSTNE LINIJE (P235!); PEZDIRC-nit čez 3 generacije (1859→1919 = 60 let!).", storyEn: "The BORŠT h20: ★★★ P256: the m2-1829 bride (Griblje 20 × the h32-groom — the FULL DOUBLE!) = h20-SECOND-01738-block (1829+1873!) — the h20-firstYear-1859→1829 (LIFT 30!) + span-1829–1922 = 93-years (ties-h22!); the z72/z73 TWINS 1871 (P235!); the PEZDIRC thread 1859→1919 (60 years!)." },
  { houseNo: "22", blocks: 35, years: "1828–1921", storySi: "REKORD-DVIGA-41-LET: m13-1828-nevesta-Catra-[~Miller-garble-'Križan'-kand.!]-GRIBLJE-22 × Miko-TILLAR-h61 = POLNI-DVOJNI (P255!) — h22-firstYear-1869→1828 = ABSOLUTNI-REKORD-DVIGA-MATRIČNE-LINIJE; P256: m18-1829-nevesta-Maria-MILLER (h22 × KRIŽAN-h62!); ★★★★★ P257: m4-1830-NEVESTA-Anna-MILEK (oče-Joh.-Milek!) = ★-3-ZAPOREDNA-LETA-NEVEST-IZ-h22 (1828+1829+1830 — edino-3-letno-zaporedje-v-01738!) — [~X-OPEN: Miller-ali-Milek-družina? + h65-Milek-1831-vezava-kand.!]; 35 blokov 1828–1921 = 93 let!", storyEn: "THE-41-YEAR-LIFT-RECORD: the m13-1828 bride Catra-GRIBLJE-22 × Miko-TILLAR-h61 = the FULL DOUBLE (P255!) — the h22-firstYear-1869→1828 = the ABSOLUTE-LIFT-RECORD; P256: the m18-1829 bride Maria MILLER (h22 × the KRIŽAN-h62!); ★★★★★ P257: the m4-1830 BRIDE Anna MILEK (father Joh. Milek!) = THREE-CONSECUTIVE-YEARS-OF-BRIDES-FROM-h22 (1828+1829+1830 — the only 3-year run in 01738!) — [~X-OPEN: Miller-or-Milek + the h65-1831-link-cand.!]; 35 blocks 1828–1921 = 93 years!" },
  { houseNo: "26", blocks: 27, years: "1831–1921", storySi: "★★★ P257-ANOMALIJA-hiša: m7-1831-'ženin'-MARIA-Pödiz? [~Pesdirz?~Podierz?—ŽENSKO-IME-V-ŽENINSKEM-STOLPCU!] ([~26|20-DUEL-w3-'26'-4:2], GRIBLJE 26 × [Maly?]-h27 — POLNI-DVOJNI-ANOMALIJA!) — h26-firstYear-1859→1831 (DVIG 28-[~]); 27 blokov 1831–1921 = 90 let (5.-mesto!); očeN-Georg-[Pödiz?]-istim-imenom-kot-m2-ženin!", storyEn: "★★★ The P257 ANOMALY house: the m7-1831-'groom'-MARIA-Pödiz? [~DUEL — A-FEMALE-NAME-IN-THE-GROOM'S-COLUMN!] (GRIBLJE 26 [~26|20] × the h27-bride — the ANOMALY-FULL-DOUBLE!) — the h26-firstYear-1859→1831 (LIFT 28-[~]); 27 blocks 1831–1921 = 90 years (5th!)" },
  { houseNo: "27", blocks: 30, years: "1831–1918", storySi: "★★★ P257-hiša: m7-1831-NEVESTA-Anna-[Maly?~Malež] (GRIBLJE 27 × ANOMALIJA-Maria-h26 — POLNI-DVOJNI!) — h27-firstYear-1864→1831 (DVIG 33 — 4.-največji-vseh-časov!); 30 blokov 1831–1918 = 87 let; h27 = SEGINA-rekord-poročne-04455 (8-blokov!)+031?-ne — zdaj-ŠEST-knjižna-prek-P257!", storyEn: "★★★ The P257 house: the m7-1831 BRIDE Anna [Maly?] (GRIBLJE 27 × the-Maria-h26-ANOMALY — the FULL DOUBLE!) — the h27-firstYear-1864→1831 (LIFT 33 — the-4th-largest!); 30 blocks 1831–1918 = 87 years; h27 = the-04455-marriage-record-SEGINA (8 blocks!) — now-SIX-book-via-P257!" },
  { houseNo: "28", blocks: 26, years: "1865–1917", storySi: "DVE-DRUŽINI-HIŠA — edina z ×2 blokoma v 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) krstni (P235-h28-dve-družini!); 1916/1917 Ana + Anton PEZDIREC — poročena 30. 1. 1861, Anton †78 let = 56-LETNA ZAKONSKA ZVEZA!", storyEn: "THE TWO-FAMILY HOUSE — the only one with ×2 blocks in 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) baptisms (P235-h28-two-families!); 1916/1917 Ana + Anton PEZDIREC — married Jan 30 1861, Anton †78 = A 56-YEAR MARRIAGE!" },
  { houseNo: "32", blocks: 27, years: "1829–1915", storySi: "[DEHLIČ?]-hiša: m2-1829 ženin Michael [DEHLIČ?~3-branja-DUEL] (28 l, GRIBLJE 32 [~DUEL-32|33!] × [Malešič?]-h20 — POLNI-DVOJNI, P256!) — MALEŠIČ×MALEŠIČ (mati-ženina + oče-neveste — KRVNO-SOROSTVO-KAND.!); h32-firstYear-1863→1829 (DVIG 34!) — h32-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (P256!).", storyEn: "The [DEHLIČ?] house: the m2-1829 groom Michael [DEHLIČ?~3-reads-DUEL] (28, GRIBLJE 32 [~DUEL-32|33!] × the h20-bride — the FULL DOUBLE, P256!) — the MALEŠIČ×MALEŠIČ-kinship-cand.!; the h32-firstYear-1863→1829 (LIFT 34!) — h32-ENTERS-THE-SIX-BOOKS-CLUB (P256!)." },
  { houseNo: "33", blocks: 31, years: "1831–1922", storySi: "★★★ P257-hiša: m1-1831-NEVESTA-Anna-[Dehligl?~Pehligh/Dölker—3-branja + očeN-Mario-Doblioz-DVOJMA!] (GRIBLJE 33 [~33|39-w3-'33'-3:2] × KRIŽAN-h3 — POLNI-DVOJNI!) — h33-firstYear-1859→1831 (DVIG 28-[~]); 31 blokov 1831–1922 = 91 let (IZENAČI-h11!); mati-Dorothea-KRIŽAN!", storyEn: "★★★ The P257 house: the m1-1831 BRIDE Anna [Dehligl?~3-reads + the father's-surname-DVOJMA!] (GRIBLJE 33 [~33|39] × the-KRIŽAN-h3 — the FULL DOUBLE!) — the h33-firstYear-1859→1831 (LIFT 28-[~]); 31 blocks 1831–1922 = 91 years (ties-h11!); the mother Dorothea KRIŽAN!" },
  { houseNo: "56", blocks: 14, years: "1831–1908", storySi: "P257-hiša: m3-1831-ŽENIN-Math.-[Kiniz?~Schimiz/Štimic—3-branja] (32, GRIBLJE 56 × [Pedierz?]-Podzemelj-3 — pol-dvojni!) — h56-firstYear-1867→1831 (DVIG 36 — 3.-največji-vseh-časov!); 14 blokov 1831–1908 = 77 let; mati-[Klepz?]-KLEPEC-nit-kand. (continuum-1828/1829!)", storyEn: "The P257 house: the m3-1831 GROOM Math. [Kiniz?~DUEL] (32, GRIBLJE 56 × the Podzemelj-3-bride — a half-double!) — the h56-firstYear-1867→1831 (LIFT 36 — the-3rd-largest!); 14 blocks 1831–1908 = 77 years; the-[Klepz?]-KLEPEC-thread" },
  { houseNo: "61", blocks: 17, years: "1828–1919", storySi: "TILLAR-hiša: m13-1828-ženin-Miko-TILLAR-½-Gütl-GRIBLJE-61 × nevesta-h22 = POLNI-DVOJNI (P255!) — TILLAR-NIT-×2 (m2-1828-mati-Anna-Tillar-Boršt-13!); h61-firstYear-1862→1828 (DVIG 34!); 3-poroke-04455 (1879-29 + …) + 04105-×4 + 04894-×6 = 17 blokov 1828–1919 = 91 let.", storyEn: "The TILLAR house: the m13-1828 groom Miko-TILLAR-½-Gütl-GRIBLJE-61 × the h22-bride = the FULL DOUBLE (P255!) — the TILLAR-thread-×2 (the m2-1828 mother Anna Tillar of Boršt 13!); the h61-firstYear-1862→1828 (LIFT 34!); 17 blocks 1828–1919 = 91 years." },
  { houseNo: "62", blocks: 29, years: "1829–1924", storySi: "★★★★★ KRIŽAN-HRIŽAN-hiša-44-LET: m18-1829 ŽENIN Matthe KRIŽAN (GRIBLJE 62 × Miller-h22 — POLNI-DVOJNI, P256!) + m18-1873 NEVESTA Maria HRIŽAN (h62 × Gabovšič-h13 — ŠIV-P253!) = ISTA-HIŠA-1829–1873!; h62-firstYear-1864→1829 (DVIG 35 = največji P256!); 29 blokov 1829–1924 = 95 let (2.-najdaljši-za-h6-96!)", storyEn: "★★★★★ THE-KRIŽAN-HRIŽAN-HOUSE-44-YEARS: the m18-1829 GROOM Matthe KRIŽAN (GRIBLJE 62 × the Miller-h22 — the FULL DOUBLE, P256!) + the m18-1873 BRIDE Maria HRIŽAN (h62 × the Gabovšič-h13 — the-P253-SEAM!) = THE-SAME-HOUSE-1829–1873!; the h62-firstYear-1864→1829 (LIFT 35 = the-largest-of-P256!); 29 blocks 1829–1924 = 95 years (the-2nd-longest-after-h6-96!)" },
  { houseNo: "63", blocks: 29, years: "1862–1921", storySi: "KRIŽAN-HIŠA (korpus-uradno: 'h63 = KRIŽAN-hiša'!): Križan/Hrižan-continuum 1862–1921 (9+ blokov); m1-KURE-29. 1. 1873 = PRVI VPIS PREDHODNIKA (P253-RESTART-1!); tri poroke Križan 1911/1912/1921; PEZDIRC-mati ×4 (1881–1896).", storyEn: "THE KRIŽAN HOUSE (officially in the corpus: 'h63 = KRIŽAN-hiša'!): the Križan/Hrižan continuum 1862–1921 (9+ blocks); the m1-KURE-Jan 29 1873 = THE FIRST ENTRY OF THE PREDECESSOR (the P253 RESTART-1!); three Križan marriages 1911/1912/1921; the PEZDIRC mother ×4 (1881–1896)." },
  { houseNo: "65", blocks: 44, years: "1831–1914", storySi: "★★★★★ P257-MILEK-hiša: m10-1831-ŽENIN-Nicol-MILEK ('-ek'-1:1!-oče-Janez!, GRIBLJE 65 × [Prodsanzig?]-Podzemelj-2) — h65-firstYear-1857→1831 (DVIG 26!) — ★-h65-BILA-PRVA-HIŠA-KORPUSA-1857 (korpus-prvi-vpis-PRE-P255!) + MILEK-h65-NIT: 1831↔1874-P250 = 43-LET-družine!; 44 blokov = 2.-najglasnejša (za-h24-45!) + 14 v 04106 = REKORD-skupaj-s-h13; zdaj-ŠEST-knjižna-prek-P257!", storyEn: "★★★★★ The P257-MILEK house: the m10-1831 GROOM Nicol MILEK (father-Janez!, GRIBLJE 65 × the Podzemelj-2-bride) — the h65-firstYear-1857→1831 (LIFT 26!) — ★-h65-WAS-THE-FIRST-HOUSE-OF-THE-CORPUS-1857 + THE-MILEK-THREAD: 1831↔1874 = A-43-YEAR-family!; 44 blocks = the-2nd-loudest (after h24-45!) + 14 in 04106 = the record-with-h13; now-SIX-book-via-P257!" },
  { houseNo: "73", blocks: 9, years: "1869–1921", storySi: "★ TIHA-HIŠA — samo 9 blokov v 6 knjigah (1–2 na knjigo, najtišja šest-knjižna — naslednja h61 ima 17!): m12-KUPAMIČ-1873 s pisarjevim popravkom '13'→'73' (P253!); Županič/Lupanič/Lepančič-garble-continuum 1869–1921; PEZDIRC-mati ×4 (Pezdire/Pegdire/Pozdirec/Pegdirec — 4 grafije!).", storyEn: "★ THE QUIET HOUSE — only 9 blocks in 6 books (1–2 per book, the quietest six-book house — the next, h61, has 17!): the m12-KUPAMIČ-1873 with the scribe's correction '13'→'73' (P253!); the Županič/Lupanič/Lepančič garble continuum 1869–1921; the PEZDIRC mother ×4 (four spellings!)." },
];

export interface HouseStoryTier {
  books: number;
  houses: number;
  labelSi: string;
}

/** Pokritje po številu knjig: 23/41/12/8/8/8 = 100 (P257: 16/46 → 23/41!). */
export const HOUSE_STORY_TIERS: HouseStoryTier[] = [
  { books: 6, houses: 23, labelSi: "šešt-knjižne (polni cikel!)" },
  { books: 5, houses: 41, labelSi: "pet-knjižne" },
  { books: 4, houses: 12, labelSi: "štiri-knjižne" },
  { books: 3, houses: 8, labelSi: "tri-knjižne" },
  { books: 2, houses: 8, labelSi: "dvo-knjižne" },
  { books: 1, houses: 8, labelSi: "eno-knjižne" },
];

export const HOUSE_STORY_TOTALS = {
  houses: 100,
  griblje: 78,
  drugaVas: 16,
  neznano: 6,
  blocks: 2043,
  sixBook: 23,
  fiveBook: 41,
  fourBook: 12,
  bothEraKrstna: 69,
  bothEraMrliska: 75,
  bothEraPorocna: 26,
  loudest: "24",
  loudestBlocks: 45,
  quietest6: "73",
  quietest6Blocks: 9,
  longestSpan: 96,
  longestSpanHouses: ["6"],
  deathsGap: "25",
  p256Dvigi: "h62/h32/h5/h20/h19 = 35/34/30/30/29 (1829!)",
  p257Dvigi: "h54/h56/h27/h11/h1/h26/h33/h3/h50/h65 = 37/36/33/32/30/28/28/27/27/26 (1831!) + h22-3-leto-1830!",
} as const;

export interface HouseStoryNotable {
  id: string;
  titleSi: string;
  titleEn: string;
  bodySi: string;
  bodyEn: string;
}

/** Osamelci, rekordi in vrzeli mreže — 7 zgodb (P257-posodobljene). */
export const HOUSE_STORY_NOTABLES: HouseStoryNotable[] = [
  { id: "najglasnejsa", titleSi: "h24 = najglasnejša hiša korpusa", titleEn: "The h24 = the loudest house of the corpus", bodySi: "45 blokov (1859–1920) — 18 v 04105 = REKORD KRSTNE LINIJE; a samo 5 knjig: 01738 je nima (niti 1873 niti 1828–1831 — P255/P257!). 8 blokov tudi v 04104.", bodyEn: "45 blocks (1859–1920) — 18 in 04105 = THE BAPTISM LINE RECORD; but only 5 books: 01738 lacks it (neither 1873 nor 1828–1831 — P255/P257!). Also 8 blocks in 04104." },
  { id: "h65", titleSi: "h65 = 44 blokov (P257! +1), rekord mrliške predzgodovine", titleEn: "The h65 = 44 blocks (P257! +1), the death-prehistory record", bodySi: "★★★★★ P257: h65-BILA-PRVA-HIŠA-KORPUSA-1857 — zdaj-firstYear-1831 (DVIG 26!) + MILEK-NIT-1831↔1874 = 43-let!; 44 blokov (1831–1914); 14 v 04106 = REKORD skupaj s h13; MILEK-družina (P218/P220/P224/P246 + P257 = 5 virov!); zdaj ŠEST-knjižna (16→23!)", bodyEn: "★★★★★ P257: h65-WAS-THE-FIRST-HOUSE-1857 — now-firstYear-1831 (LIFT 26!) + THE-MILEK-THREAD-1831↔1874 = 43 years!; 44 blocks (1831–1914); 14 in 04106 = THE RECORD with h13; the MILEK family (5 sources!); now SIX-book (16→23!)" },
  { id: "h35", titleSi: "h35 = rekord mrliške linije 04894", titleEn: "The h35 = the death-line 04894 record", bodySi: "15 blokov v 04894 (1886–1924) = NAJVEČ V ENI KNJIGI med vsemi hišami; HRIŽAN-družina (P229!). Skupaj 24 blokov 1857–1922.", bodyEn: "15 blocks in 04894 (1886–1924) = THE MOST IN ONE BOOK of all houses; the HRIŽAN family (P229!). Altogether 24 blocks 1857–1922." },
  { id: "h27", titleSi: "h27 = rekord poročne knjige 04455 — zdaj šest-knjižna (P257!)", titleEn: "The h27 = the 04455 marriage record — now six-book (P257!)", bodySi: "★★★ P257: m7-1831-NEVESTA-Anna-[Maly?] (Griblje 27!) — h27-firstYear-1864→1831 (DVIG 33 — 4.!) + 30 blokov 1831–1918; 8 blokov v 04455 = REKORD POROČNE (SEGINA-hiša: 1875 + 1881 + 1882 + 1884 + …); Jacob-63-l-×-Anna-HRIŽAN-1875 (P250).", bodyEn: "★★★ P257: the m7-1831 BRIDE Anna [Maly?] (Griblje 27!) — the h27-firstYear-1864→1831 (LIFT 33!) + 30 blocks 1831–1918; 8 blocks in 04455 = THE MARRIAGE RECORD (the SEGINA house); Jacob-63-y-o × Anna HRIŽAN 1875 (P250)." },
  { id: "smrtna-vrzeli", titleSi: "h25 = SMRTNA VRZEL 29 let", titleEn: "The h25 = A 29-YEAR DEATH GAP", bodySi: "5 knjig a BREZ 04106: noben mrliški zapis 1857–1885 (29 let!) kljub krstnim blokom 1876 + 1883 ×2 in poroki v 01738 (m3-kandidat, P253!). Šele 04894 prinese 7 blokov (1888–1923) — mrežna luknja, ne stvarna.", bodyEn: "5 books but WITHOUT 04106: no death record 1857–1885 (29 years!) despite the baptism blocks 1876 + 1883 ×2 and a marriage in 01738 (the m3 candidate, P253!). Only 04894 brings 7 blocks (1888–1923) — a network hole, not a real one." },
  { id: "razponi-96", titleSi: "P255: h6 = 96-letni razpon (ostaja rekord!)", titleEn: "P255: the h6 = a 96-year span (the standing record!)", bodySi: "h6 dokumentirana 1828→1924 (96 let!); sledita h62 (95: 1829–1924) in ★★★ P257: h50/h20/h22 (93: h50-1831–1924-NOVO-3.-mesto-izenači-h20/h22!) + h11/h33 (91: 1831–1922!) + h26 (90: 1831–1921!) + h27 (87); stari-rekord-66 (h2/h13/h50/h60/h64) ostaja za štiri-knjižnimi.", bodyEn: "The h6 documented 1828→1924 (96 years!); then h62 (95) and ★★★ P257: h50/h20/h22 (93 — h50's new 3rd place!) + h11/h33 (91!) + h26 (90!) + h27 (87); the old record 66 remains for the four-book houses." },
  { id: "skrita-hisa", titleSi: "h[?] = skrita hiša brez številke", titleEn: "The h[?] = the hidden house without a number", bodySi: "10 blokov 1857–1885 (8 v 04104 + 2 v 04106) z izpraznjeno hišno celico — edina hiša korpusa brez številke; P235/P220 X-OPEN. V kasnejših knjigah izgine (razrešena številka?).", bodyEn: "10 blocks 1857–1885 (8 in 04104 + 2 in 04106) with an emptied house cell — the only corpus house without a number; P235/P220 X-OPEN. It vanishes in the later books (a resolved number?)." },
];
