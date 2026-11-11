// P254+P255+P256: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (regenerirano P256: +5 blokov 1829/01738!; 2026-11-11)
// SINTEZNA FAZA: agregacija celotnega korpusa HOUSE_VITALS (2031 vitalov) po hišah čez VSEH 6 knjig:
// 01738 (poročna-predhodnik 1828 + 1829 + 1873 — P256: +5 blokov 1829!) + 04104 (krstna-predzgodovina 1871–1885)
// + 04105 (krstna-linija 1887–1919) + 04455 (poročna 1873–1922) + 04106 (mrliška-predzgodovina 1857–1885)
// + 04894 (mrliška-linija 1886–1924). 100 hišnih oznak = 78 Griblje (1–78) + 16 druga-vas (79–98) + 6 neznanek.
// ★★★★★ P255-VELIKI-PRELOM: KORPUS-PRVI-VPIS-1857→1828 (h6/h22/h61!) — ★★★★★ P256: 16 ŠEST-KNJIŽ-HIŠ (P254-9 → P255-12 → P256-16!:
// 3, 5, 6, 10, 12, 16, 18, 19, 20, 22, 28, 32, 61, 62, 63, 73!) + bothEra-poročna 10→13→17 + razponi: h6-96/h62-95-NOVO-2.!/h20+h22-93/h61-91/h5-90 — P256-preoblikuje-VRH-korpusa!
// Dokaz: research/issue17/parish-house-stories.json; verifikator: scripts/p254_house_stories.py --check (I1–I10);
// regenerator: scripts/tmp/p256_gen.py (po vzoru p255_gen.py).

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
  { sig: "01738", roleSi: "poročna-predhodnik", roleEn: "marriage predecessor", years: "1828 + 1829 + 1873", blocks: 20, houses: 17, recordSi: "P256: h62/h32/h5/h19 firstYear-1829! (h62 −35 = največji dvig P256! · m18-KRIŽAN-h62×h22 · h20-01738-span-1829+1873!)" },
  { sig: "04104", roleSi: "krstna-predzgodovina", roleEn: "baptism prehistory", years: "1871–1885", blocks: 288, houses: 72, recordSi: "h6 · h40 · h[?] (8 blokov vsak)" },
  { sig: "04105", roleSi: "krstna-linija", roleEn: "baptism line", years: "1887–1919", blocks: 502, houses: 89, recordSi: "h24 (18 blokov!)" },
  { sig: "04455", roleSi: "poročna-linija + predzgodovina", roleEn: "marriage line + prehistory", years: "1873–1922", blocks: 269, houses: 82, recordSi: "h27 SEGINA (8 blokov)" },
  { sig: "04106", roleSi: "mrliška-predzgodovina", roleEn: "death prehistory", years: "1857–1885", blocks: 433, houses: 78, recordSi: "h13 · h65 (14 blokov vsak)" },
  { sig: "04894", roleSi: "mrliška-linija", roleEn: "death line", years: "1886–1924", blocks: 520, houses: 92, recordSi: "h35 HRIŽAN (15 blokov!)" },
];

/** Vseh 100 hišnih oznak korpusa — Griblje (1–78) številsko, druga-vas (79–98), nato neznanke. */
export const HOUSE_STORIES: HouseStory[] = [
  { houseNo: "1", kind: "griblje", blocks: 41, books: 5, perBook: [{ sig: "04104", n: 8 }, { sig: "04105", n: 9 }, { sig: "04455", n: 7 }, { sig: "04106", n: 12 }, { sig: "04894", n: 5 }], firstYear: 1861, lastYear: 1914, span: 53 },
  { houseNo: "2", kind: "griblje", blocks: 32, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 6 }, { sig: "04455", n: 3 }, { sig: "04106", n: 7 }, { sig: "04894", n: 12 }], firstYear: 1858, lastYear: 1924, span: 66 },
  { houseNo: "3", kind: "griblje", blocks: 23, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 4 }, { sig: "04105", n: 4 }, { sig: "04455", n: 2 }, { sig: "04106", n: 7 }, { sig: "04894", n: 5 }], firstYear: 1858, lastYear: 1917, span: 59 },
  { houseNo: "4", kind: "griblje", blocks: 7, books: 5, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 1 }, { sig: "04455", n: 2 }, { sig: "04106", n: 2 }, { sig: "04894", n: 1 }], firstYear: 1870, lastYear: 1906, span: 36 },
  { houseNo: "5", kind: "griblje", blocks: 32, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 5 }, { sig: "04105", n: 9 }, { sig: "04455", n: 1 }, { sig: "04106", n: 10 }, { sig: "04894", n: 6 }], firstYear: 1829, lastYear: 1919, span: 90 },
  { houseNo: "6", kind: "griblje", blocks: 36, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 8 }, { sig: "04105", n: 8 }, { sig: "04455", n: 5 }, { sig: "04106", n: 6 }, { sig: "04894", n: 8 }], firstYear: 1828, lastYear: 1924, span: 96 },
  { houseNo: "7", kind: "griblje", blocks: 24, books: 5, perBook: [{ sig: "04104", n: 6 }, { sig: "04105", n: 4 }, { sig: "04455", n: 5 }, { sig: "04106", n: 6 }, { sig: "04894", n: 3 }], firstYear: 1867, lastYear: 1921, span: 54 },
  { houseNo: "8", kind: "griblje", blocks: 38, books: 5, perBook: [{ sig: "04104", n: 6 }, { sig: "04105", n: 7 }, { sig: "04455", n: 7 }, { sig: "04106", n: 11 }, { sig: "04894", n: 7 }], firstYear: 1871, lastYear: 1919, span: 48 },
  { houseNo: "9", kind: "griblje", blocks: 23, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 5 }, { sig: "04455", n: 3 }, { sig: "04106", n: 3 }, { sig: "04894", n: 7 }], firstYear: 1862, lastYear: 1922, span: 60 },
  { houseNo: "10", kind: "griblje", blocks: 30, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 2 }, { sig: "04105", n: 6 }, { sig: "04455", n: 7 }, { sig: "04106", n: 11 }, { sig: "04894", n: 3 }], firstYear: 1862, lastYear: 1921, span: 59 },
  { houseNo: "11", kind: "griblje", blocks: 30, books: 5, perBook: [{ sig: "04104", n: 7 }, { sig: "04105", n: 7 }, { sig: "04455", n: 3 }, { sig: "04106", n: 7 }, { sig: "04894", n: 6 }], firstYear: 1863, lastYear: 1922, span: 59 },
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
  { houseNo: "22", kind: "griblje", blocks: 34, books: 6, perBook: [{ sig: "01738", n: 2 }, { sig: "04104", n: 7 }, { sig: "04105", n: 7 }, { sig: "04455", n: 5 }, { sig: "04106", n: 6 }, { sig: "04894", n: 7 }], firstYear: 1828, lastYear: 1921, span: 93 },
  { houseNo: "23", kind: "griblje", blocks: 22, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 7 }, { sig: "04455", n: 4 }, { sig: "04106", n: 3 }, { sig: "04894", n: 4 }], firstYear: 1865, lastYear: 1922, span: 57 },
  { houseNo: "24", kind: "griblje", blocks: 45, books: 5, perBook: [{ sig: "04104", n: 8 }, { sig: "04105", n: 18 }, { sig: "04455", n: 5 }, { sig: "04106", n: 5 }, { sig: "04894", n: 9 }], firstYear: 1859, lastYear: 1920, span: 61 },
  { houseNo: "25", kind: "griblje", blocks: 18, books: 5, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 3 }, { sig: "04105", n: 5 }, { sig: "04455", n: 2 }, { sig: "04894", n: 7 }], firstYear: 1873, lastYear: 1923, span: 50 },
  { houseNo: "26", kind: "griblje", blocks: 26, books: 5, perBook: [{ sig: "04104", n: 1 }, { sig: "04105", n: 5 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 12 }], firstYear: 1859, lastYear: 1921, span: 62 },
  { houseNo: "27", kind: "griblje", blocks: 29, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 9 }, { sig: "04455", n: 8 }, { sig: "04106", n: 4 }, { sig: "04894", n: 5 }], firstYear: 1864, lastYear: 1918, span: 54 },
  { houseNo: "28", kind: "griblje", blocks: 26, books: 6, perBook: [{ sig: "01738", n: 2 }, { sig: "04104", n: 7 }, { sig: "04105", n: 3 }, { sig: "04455", n: 3 }, { sig: "04106", n: 7 }, { sig: "04894", n: 4 }], firstYear: 1865, lastYear: 1917, span: 52 },
  { houseNo: "29", kind: "griblje", blocks: 23, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 4 }, { sig: "04455", n: 3 }, { sig: "04106", n: 4 }, { sig: "04894", n: 7 }], firstYear: 1859, lastYear: 1921, span: 62 },
  { houseNo: "30", kind: "griblje", blocks: 40, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 14 }, { sig: "04455", n: 7 }, { sig: "04106", n: 6 }, { sig: "04894", n: 9 }], firstYear: 1860, lastYear: 1918, span: 58 },
  { houseNo: "31", kind: "griblje", blocks: 42, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 13 }, { sig: "04455", n: 7 }, { sig: "04106", n: 7 }, { sig: "04894", n: 10 }], firstYear: 1857, lastYear: 1921, span: 64 },
  { houseNo: "32", kind: "griblje", blocks: 27, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 1 }, { sig: "04105", n: 11 }, { sig: "04455", n: 4 }, { sig: "04106", n: 4 }, { sig: "04894", n: 6 }], firstYear: 1829, lastYear: 1915, span: 86 },
  { houseNo: "33", kind: "griblje", blocks: 30, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 5 }, { sig: "04455", n: 5 }, { sig: "04106", n: 7 }, { sig: "04894", n: 9 }], firstYear: 1859, lastYear: 1922, span: 63 },
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
  { houseNo: "50", kind: "griblje", blocks: 11, books: 4, perBook: [{ sig: "04105", n: 1 }, { sig: "04455", n: 3 }, { sig: "04106", n: 6 }, { sig: "04894", n: 1 }], firstYear: 1858, lastYear: 1924, span: 66 },
  { houseNo: "51", kind: "griblje", blocks: 11, books: 4, perBook: [{ sig: "04104", n: 2 }, { sig: "04455", n: 2 }, { sig: "04106", n: 3 }, { sig: "04894", n: 4 }], firstYear: 1867, lastYear: 1913, span: 46 },
  { houseNo: "52", kind: "griblje", blocks: 14, books: 4, perBook: [{ sig: "04105", n: 3 }, { sig: "04455", n: 2 }, { sig: "04106", n: 5 }, { sig: "04894", n: 4 }], firstYear: 1857, lastYear: 1908, span: 51 },
  { houseNo: "53", kind: "griblje", blocks: 33, books: 5, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 7 }, { sig: "04455", n: 4 }, { sig: "04106", n: 6 }, { sig: "04894", n: 11 }], firstYear: 1863, lastYear: 1924, span: 61 },
  { houseNo: "54", kind: "griblje", blocks: 17, books: 4, perBook: [{ sig: "04105", n: 6 }, { sig: "04455", n: 3 }, { sig: "04106", n: 6 }, { sig: "04894", n: 2 }], firstYear: 1868, lastYear: 1917, span: 49 },
  { houseNo: "55", kind: "griblje", blocks: 18, books: 4, perBook: [{ sig: "04104", n: 5 }, { sig: "04105", n: 3 }, { sig: "04106", n: 6 }, { sig: "04894", n: 4 }], firstYear: 1860, lastYear: 1924, span: 64 },
  { houseNo: "56", kind: "griblje", blocks: 13, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 3 }, { sig: "04455", n: 3 }, { sig: "04106", n: 3 }, { sig: "04894", n: 2 }], firstYear: 1867, lastYear: 1908, span: 41 },
  { houseNo: "57", kind: "griblje", blocks: 21, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 5 }, { sig: "04455", n: 1 }, { sig: "04106", n: 7 }, { sig: "04894", n: 6 }], firstYear: 1859, lastYear: 1912, span: 53 },
  { houseNo: "58", kind: "griblje", blocks: 28, books: 5, perBook: [{ sig: "04104", n: 2 }, { sig: "04105", n: 8 }, { sig: "04455", n: 2 }, { sig: "04106", n: 5 }, { sig: "04894", n: 11 }], firstYear: 1859, lastYear: 1918, span: 59 },
  { houseNo: "59", kind: "griblje", blocks: 10, books: 4, perBook: [{ sig: "04105", n: 4 }, { sig: "04455", n: 1 }, { sig: "04106", n: 1 }, { sig: "04894", n: 4 }], firstYear: 1875, lastYear: 1921, span: 46 },
  { houseNo: "60", kind: "griblje", blocks: 30, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 9 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 10 }], firstYear: 1857, lastYear: 1923, span: 66 },
  { houseNo: "61", kind: "griblje", blocks: 17, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 1 }, { sig: "04105", n: 4 }, { sig: "04455", n: 3 }, { sig: "04106", n: 2 }, { sig: "04894", n: 6 }], firstYear: 1828, lastYear: 1919, span: 91 },
  { houseNo: "62", kind: "griblje", blocks: 29, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 6 }, { sig: "04105", n: 4 }, { sig: "04455", n: 6 }, { sig: "04106", n: 6 }, { sig: "04894", n: 6 }], firstYear: 1829, lastYear: 1924, span: 95 },
  { houseNo: "63", kind: "griblje", blocks: 29, books: 6, perBook: [{ sig: "01738", n: 1 }, { sig: "04104", n: 4 }, { sig: "04105", n: 8 }, { sig: "04455", n: 5 }, { sig: "04106", n: 7 }, { sig: "04894", n: 4 }], firstYear: 1862, lastYear: 1921, span: 59 },
  { houseNo: "64", kind: "griblje", blocks: 20, books: 5, perBook: [{ sig: "04104", n: 3 }, { sig: "04105", n: 2 }, { sig: "04455", n: 3 }, { sig: "04106", n: 5 }, { sig: "04894", n: 7 }], firstYear: 1857, lastYear: 1923, span: 66 },
  { houseNo: "65", kind: "griblje", blocks: 43, books: 5, perBook: [{ sig: "04104", n: 4 }, { sig: "04105", n: 11 }, { sig: "04455", n: 5 }, { sig: "04106", n: 14 }, { sig: "04894", n: 9 }], firstYear: 1857, lastYear: 1914, span: 57 },
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

/** ★★★★★ 16 ŠEST-KNJIŽ-HIŠ (P256!) — blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste). */
export const HOUSE_STORY_SIX: HouseStorySix[] = [
  { houseNo: "3", blocks: 23, years: "1858–1917", storySi: "HRIŽAN/KRIŽAN-hiša: Peter Hrižan krstni oče 1872–1881 (4 krsti) + †1888 Peter Križar/Križan 80 let; 1864 Georg DRAGOŠ †70 (najstarejša omemba); m11-HLEBEC-1873 v predhodniku (P253!); 1907 PEZDIREC-poroka (h3 = 2. poročni dokaz).", storyEn: "The HRIŽAN/KRIŽAN house: Peter Hrižan the baptismal father 1872–1881 (4 baptisms) + Peter Križan †1888 aged 80; Georg DRAGOŠ †70 in 1864 (the oldest mention); the m11-HLEBEC-1873 in the predecessor (P253!); a PEZDIREC marriage 1907." },
  { houseNo: "5", blocks: 32, years: "1829–1919", storySi: "MÜLLER-hiša: m10-1829 ženin Mathe MÜLLER (26 l, GRIBLJE 5 × [Šimek?]-h19 — POLNI-DVOJNI, P256!) — h5-firstYear-1859→1829 (DVIG 30!); 31 blokov 1829–1924 — h5-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!); MÜLLER-×2-družini-1829 (h5-hiša + h22-Millerji!).", storyEn: "The MÜLLER house: the m10-1829 groom Mathe MÜLLER (26, GRIBLJE 5 × the h19-bride — the FULL DOUBLE, P256!) — the h5-firstYear-1859→1829 (LIFT 30!); 31 blocks 1829–1924 — h5-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!); the MÜLLER-×2-families-of-1829 (the h5-house + the h22-Millers!)." },
  { houseNo: "6", blocks: 36, years: "1828–1924", storySi: "NAJDALJŠA-HIŠA-KORPUSA (96 let!): m6-1828-nevesta-Maria-[Jan/Spin]-GRIBLJE-6 × ženin-Jure-STARA = PRVI-GRIBLJE-VPIS-PREDHODNIKA-01738 (P255 — korpus 1857→1828!); h6-firstYear-1860→1828 (DVIG 32!); 04104-trospec (8) + 04106 (6) + 04455 (5 porok!) + 04105 (8) + 04894 (8) = 36 blokov 1828–1924 čez VSEH 6 knjig!", storyEn: "THE-LONGEST-SPAN-HOUSE-OF-THE-CORPUS (96 years!): the m6-1828 bride Maria-GRIBLJE-6 × groom Jure-STARA = the FIRST Griblje entry of the 01738 predecessor (P255 — the corpus 1857→1828!); the h6-firstYear-1860→1828 (LIFT 32!); 36 blocks 1828–1924 across ALL 6 books!" },
  { houseNo: "10", blocks: 30, years: "1862–1921", storySi: "MUC-hiša: m6-1873 poroka neveste Muc — KOLBEZEN h16 × MUC h10 polni dvojni (P253!); KRAUE-h10 52-letna nevesta 1874 = NAJSTAREJŠA PREDZGODOVINE (P250!); 11 mrliških blokov 04106 (1857–1885) — med najglobljimi smrtnimi zgodovinami.", storyEn: "The MUC house: the m6-1873 marriage of a Muc bride — KOLBEZEN h16 × MUC h10 the full double (P253!); the 52-year-old bride of 1874 = THE OLDEST OF THE PREHISTORY (P250!); 11 death blocks 04106 (1857–1885) — among the deepest death histories." },
  { houseNo: "12", blocks: 28, years: "1869–1919", storySi: "DRAGOŠ-50-LET: 1869 Michael Dragos †27 → 1871 Joannes Dragoš krstni oče (z46!) → 1919 Franc DRAGOS poroka + Vincencij DRAGOS † — ISTA DRUŽINA 1869–1919! + PEZDIRC-continuum (z59-1872, P235!); 14 blokov v 04105 = 2.-največ v knjigi.", storyEn: "The DRAGOŠ 50 YEARS: 1869 Michael Dragos †27 → 1871 Joannes Dragoš the baptismal father (z46!) → 1919 Franc DRAGOS marries + Vincencij DRAGOS † — THE SAME FAMILY 1869–1919! + the PEZDIRC continuum (z59-1872, P235!); 14 blocks in 04105 = the 2nd most of the book." },
  { houseNo: "16", blocks: 34, years: "1864–1924", storySi: "KOLBEZEN-hiša: m6-1873 ženin Georg KOLBEZEN (h16 × h10 polni dvojni, P253!); 1918 Ana FILAK roj. NEMANIČ †75 (poročena 1879!); 1924 Alojzy NOVAK †27. 9. — zadnja leta mrliške linije (04894 se konča 31. 12. 1924, P190!).", storyEn: "The KOLBEZEN house: the m6-1873 groom Georg KOLBEZEN (h16 × h10 the full double, P253!); Ana FILAK née NEMANIČ †75 in 1918 (married 1879!); Alojzy NOVAK †Sep 27 1924 — the final years of the death line (04894 ends Dec 31 1924, P190!)." },
  { houseNo: "18", blocks: 36, years: "1861–1922", storySi: "ŠIMEC-hiša (P246-h18-ŠIMEC-1:1!): 1863 Georg Simic †53; 1878 dve INTRA-poroki v 1 letu (h18 × h65, P246!); 1921 Karolina PEZDIRC †1,3 (zadnji PEZDIRC-blok hiše); 36 blokov = najglasnejša šest-knjižna hiša (skupaj z h6!).", storyEn: "The ŠIMEC house (P246-h18-ŠIMEC-1:1!): Georg Simic †53 in 1863; two INTRA-marriages in one year 1878 (h18 × h65, P246!); Karolina PEZDIRC †1.3 in 1921 (the house's last PEZDIRC block); 36 blocks = the loudest six-book house (together with h6!)." },
  { houseNo: "19", blocks: 22, years: "1829–1918", storySi: "[ŠIMEK?]-hiša: m10-1829 nevesta Maria [ŠIMEK?~Knimek/Thimnik — 4-branja-DUEL!] (21 l, GRIBLJE 19 × Müller-h5, P256!) — oče Georg [Šimek?~'Shimek'-garble — ŠIMEC-marker-kand.!] + mati [Salva?] TILLAR! (TILLAR-NIT-1829!); h19-firstYear-1858→1829 (DVIG 29!) — h19-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!).", storyEn: "The [ŠIMEK?] house: the m10-1829 bride Maria [ŠIMEK?~4-reads-DUEL!] (21, GRIBLJE 19 × the Müller-h5, P256!) — the father Georg [Šimek?~garble] + the mother [Salva?] TILLAR! (the-1829-TILLAR-thread!); the h19-firstYear-1858→1829 (LIFT 29!) — h19-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!)." },
  { houseNo: "20", blocks: 35, years: "1829–1922", storySi: "BORŠT-h20: ★★★ P256: m2-1829 [MALEŠIČ?]-nevesta (Griblje 20 × [Dehlič?]-h32 — POLNI-DVOJNI!) = h20-ŽE-DRUGI-01738-blok (1829+1873-m7-P253!) — h20-firstYear-1859→1829 (DVIG 30!) + span-1829–1922 = 93-let (IZENAČI-h22 — delita-2.-3.-mesto!); z72/z73 DVOJČKI 1871 = 1. DVOJČKI KRSTNE LINIJE (P235!); PEZDIRC-nit čez 3 generacije (1859→1919 = 60 let!).", storyEn: "The BORŠT h20: ★★★ P256: the m2-1829 bride (Griblje 20 × the h32-groom — the FULL DOUBLE!) = h20-SECOND-01738-block (1829+1873!) — the h20-firstYear-1859→1829 (LIFT 30!) + span-1829–1922 = 93-years (ties-h22-for-2nd-3rd!); the z72/z73 TWINS 1871 (P235!); the PEZDIRC thread 1859→1919 (60 years!)." },
  { houseNo: "22", blocks: 34, years: "1828–1921", storySi: "REKORD-DVIGA-41-LET: m13-1828-nevesta-Catra-[~Miller-garble-'Križan'-kand.!]-GRIBLJE-22 × Miko-TILLAR-h61 = POLNI-DVOJNI (P255!) — h22-firstYear-1869→1828 = ABSOLUTNI-REKORD-DVIGA-MATRIČNE-LINIJE (prej h43-34, P250!); cf.-P251-m20-MILEK-'Griblje-[22~26]-DUEL'-1873; ★★★★★ P256: m18-1829-nevesta-Maria-MILLER (h22 × KRIŽAN-h62 — POLNI-DVOJNI!) = 2-LETNI-ZAPORED-MILLERjevih-nevest-na-h22 (1828-Catra-[Miller-garble] + 1829-Maria-MILLER — oče-Josc.-Miller!); 5-porok-04455 (1879–1919) + 35 blokov 1828–1921 = 93 let!", storyEn: "THE-41-YEAR-LIFT-RECORD: the m13-1828 bride Catra-GRIBLJE-22 × Miko-TILLAR-h61 = the FULL DOUBLE (P255!) — the h22-firstYear-1869→1828 = the ABSOLUTE-LIFT-RECORD-of-the-matricular-line (the previous record h43-34, P250!); cf.-the-P251-m20-MILEK-'Griblje-[22~26]-DUEL'-1873; ★★★★★ P256: the m18-1829 bride Maria MILLER (h22 × the KRIŽAN-h62 — the FULL DOUBLE!) = TWO-CONSECUTIVE-YEARS-OF-MILLER-BRIDES-ON-h22 (1828-Catra-[Miller-garble] + 1829-Maria-MILLER!); 5 marriages 04455 (1879–1919) + 35 blocks 1828–1921 = 93 years!" },
  { houseNo: "28", blocks: 26, years: "1865–1917", storySi: "DVE-DRUŽINI-HIŠA — edina z ×2 blokoma v 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) krstni (P235-h28-dve-družini!); 1916/1917 Ana + Anton PEZDIREC — poročena 30. 1. 1861, Anton †78 let = 56-LETNA ZAKONSKA ZVEZA!", storyEn: "THE TWO-FAMILY HOUSE — the only one with ×2 blocks in 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) baptisms (P235-h28-two-families!); 1916/1917 Ana + Anton PEZDIREC — married Jan 30 1861, Anton †78 = A 56-YEAR MARRIAGE!" },
  { houseNo: "32", blocks: 27, years: "1829–1915", storySi: "[DEHLIČ?]-hiša: m2-1829 ženin Michael [DEHLIČ?~3-branja-DUEL] (28 l, GRIBLJE 32 [~DUEL-32|33!] × [Malešič?]-h20 — POLNI-DVOJNI, P256!) — MALEŠIČ×MALEŠIČ (mati-ženina + oče-neveste — KRVNO-SOROSTVO-KAND.!); h32-firstYear-1863→1829 (DVIG 34!) — h32-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!).", storyEn: "The [DEHLIČ?] house: the m2-1829 groom Michael [DEHLIČ?~3-reads-DUEL] (28, GRIBLJE 32 [~DUEL-32|33!] × the h20-bride — the FULL DOUBLE, P256!) — the MALEŠIČ×MALEŠIČ-kinship-cand.!; the h32-firstYear-1863→1829 (LIFT 34!) — h32-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!)." },
  { houseNo: "61", blocks: 17, years: "1828–1919", storySi: "TILLAR-hiša: m13-1828-ženin-Miko-TILLAR-½-Gütl-GRIBLJE-61 × nevesta-h22 = POLNI-DVOJNI (P255!) — TILLAR-NIT-×2 (m2-1828-mati-Anna-Tillar-Boršt-13!); h61-firstYear-1862→1828 (DVIG 34!); 3-poroke-04455 (1879-29 + …) + 04105-×4 + 04894-×6 = 17 blokov 1828–1919 = 91 let.", storyEn: "The TILLAR house: the m13-1828 groom Miko-TILLAR-½-Gütl-GRIBLJE-61 × the h22-bride = the FULL DOUBLE (P255!) — the TILLAR-thread-×2 (the m2-1828 mother Anna Tillar of Boršt 13!); the h61-firstYear-1862→1828 (LIFT 34!); 3 marriages 04455 (the 1879-29 + …) + 04105-×4 + 04894-×6 = 17 blocks 1828–1919 = 91 years." },
  { houseNo: "62", blocks: 29, years: "1829–1924", storySi: "★★★★★ KRIŽAN-HRIŽAN-hiša-44-LET: m18-1829 ŽENIN Matthe KRIŽAN (GRIBLJE 62 × Miller-h22 — POLNI-DVOJNI, P256!) + m18-1873 NEVESTA Maria HRIŽAN (h62 × Gabovšič-h13 — ŠIV-P253!) = ISTA-HIŠA-1829–1873!; oče Nikl. KRIŽAN + mati [TILLAR-garble — Barbara?|Dorothea?-DUEL!]; h62-firstYear-1864→1829 (DVIG 35 = največji P256!) — h62-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!); 29 blokov 1829–1924 = 95 let (2.-najdaljši-za-h6-96!)", storyEn: "★★★★★ THE-KRIŽAN-HRIŽAN-HOUSE-44-YEARS: the m18-1829 GROOM Matthe KRIŽAN (GRIBLJE 62 × the Miller-h22 — the FULL DOUBLE, P256!) + the m18-1873 BRIDE Maria HRIŽAN (h62 × the Gabovšič-h13 — the-P253-SEAM!) = THE-SAME-HOUSE-1829–1873!; the father Nikl. KRIŽAN + the mother [TILLAR-garble — Barbara?|Dorothea?-DUEL!]; the h62-firstYear-1864→1829 (LIFT 35 = the-largest-of-P256!) — h62-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!); 29 blocks 1829–1924 = 95 years (the-2nd-longest-after-h6-96!)" },
  { houseNo: "63", blocks: 29, years: "1862–1921", storySi: "KRIŽAN-HIŠA (korpus-uradno: 'h63 = KRIŽAN-hiša'!): Križan/Hrižan-continuum 1862–1921 (9+ blokov); m1-KURE-29. 1. 1873 = PRVI VPIS PREDHODNIKA (P253-RESTART-1!); tri poroke Križan 1911/1912/1921; PEZDIRC-mati ×4 (1881–1896).", storyEn: "THE KRIŽAN HOUSE (officially in the corpus: 'h63 = KRIŽAN-hiša'!): the Križan/Hrižan continuum 1862–1921 (9+ blocks); the m1-KURE-Jan 29 1873 = THE FIRST ENTRY OF THE PREDECESSOR (the P253 RESTART-1!); three Križan marriages 1911/1912/1921; the PEZDIRC mother ×4 (1881–1896)." },
  { houseNo: "73", blocks: 9, years: "1869–1921", storySi: "★ TIHA-HIŠA — samo 9 blokov v 6 knjigah (1–2 na knjigo, najtišja šest-knjižna — naslednja h61 ima 17!): m12-KUPAMIČ-1873 s pisarjevim popravkom '13'→'73' (P253!); Županič/Lupanič/Lepančič-garble-continuum 1869–1921; PEZDIRC-mati ×4 (Pezdire/Pegdire/Pozdirec/Pegdirec — 4 grafije!).", storyEn: "★ THE QUIET HOUSE — only 9 blocks in 6 books (1–2 per book, the quietest six-book house — the next, h61, has 17!): the m12-KUPAMIČ-1873 with the scribe's correction '13'→'73' (P253!); the Županič/Lupanič/Lepančič garble continuum 1869–1921; the PEZDIRC mother ×4 (four spellings!)." },
];

export interface HouseStoryTier {
  books: number;
  houses: number;
  labelSi: string;
}

/** Pokritje po številu knjig: 16/46/14/8/8/8 = 100 (P256: 12/50 → 16/46!). */
export const HOUSE_STORY_TIERS: HouseStoryTier[] = [
  { books: 6, houses: 16, labelSi: "šešt-knjižne (polni cikel!)" },
  { books: 5, houses: 46, labelSi: "pet-knjižne" },
  { books: 4, houses: 14, labelSi: "štiri-knjižne" },
  { books: 3, houses: 8, labelSi: "tri-knjižne" },
  { books: 2, houses: 8, labelSi: "dvo-knjižne" },
  { books: 1, houses: 8, labelSi: "eno-knjižne" },
];

export const HOUSE_STORY_TOTALS = {
  houses: 100,
  griblje: 78,
  drugaVas: 16,
  neznano: 6,
  blocks: 2032,
  sixBook: 16,
  fiveBook: 46,
  fourBook: 14,
  bothEraKrstna: 69,
  bothEraMrliska: 75,
  bothEraPorocna: 17,
  loudest: "24",
  loudestBlocks: 45,
  quietest6: "73",
  quietest6Blocks: 9,
  longestSpan: 96,
  longestSpanHouses: ["6"],
  deathsGap: "25",
  p256Dvigi: "h62/h32/h5/h20/h19 = 35/34/30/30/29 (1829!)",
} as const;

export interface HouseStoryNotable {
  id: string;
  titleSi: string;
  titleEn: string;
  bodySi: string;
  bodyEn: string;
}

/** Osamelci, rekordi in vrzeli mreže — 7 zgodb. */
export const HOUSE_STORY_NOTABLES: HouseStoryNotable[] = [
  { id: "najglasnejsa", titleSi: "h24 = najglasnejša hiša korpusa", titleEn: "The h24 = the loudest house of the corpus", bodySi: "45 blokov (1859–1920) — 18 v 04105 = REKORD KRSTNE LINIJE; a samo 5 knjig: 01738 je nima (niti 1873 niti 1828 — P255!). 8 blokov tudi v 04104.", bodyEn: "45 blocks (1859–1920) — 18 in 04105 = THE BAPTISM LINE RECORD; but only 5 books: 01738 lacks it (neither 1873 nor 1828 — P255!). Also 8 blocks in 04104." },
  { id: "h65", titleSi: "h65 = 43 blokov, rekord mrliške predzgodovine", titleEn: "The h65 = 43 blocks, the death-prehistory record", bodySi: "43 blokov (1857–1914); 14 v 04106 = REKORD skupaj s h13; MILEK-družina (P218/P220/P224/P246 — 4 viri!); 11 blokov v 04105. Najgloblja smrtna zgodovina med pet-knjižnimi.", bodyEn: "43 blocks (1857–1914); 14 in 04106 = THE RECORD together with h13; the MILEK family (4 sources!); 11 blocks in 04105. The deepest death history among the five-book houses." },
  { id: "h35", titleSi: "h35 = rekord mrliške linije 04894", titleEn: "The h35 = the death-line 04894 record", bodySi: "15 blokov v 04894 (1886–1924) = NAJVEČ V ENI KNJIGI med vsemi hišami; HRIŽAN-družina (P229!). Skupaj 24 blokov 1857–1922.", bodyEn: "15 blocks in 04894 (1886–1924) = THE MOST IN ONE BOOK of all houses; the HRIŽAN family (P229!). Altogether 24 blocks 1857–1922." },
  { id: "h27", titleSi: "h27 = rekord poročne knjige 04455", titleEn: "The h27 = the marriage-book 04455 record", bodySi: "8 blokov v 04455 = REKORD POROČNE (SEGINA-hiša: 1875 + 1881 + 1882 + 1884 + …); Jacob-63-l-×-Anna-HRIŽAN-1875 (P250). Skupaj 30 blokov 1857–1922.", bodyEn: "8 blocks in 04455 = THE MARRIAGE RECORD (the SEGINA house: 1875 + 1881 + 1882 + 1884 + …); Jacob-63-y-o × Anna HRIŽAN 1875 (P250). Altogether 30 blocks 1857–1922." },
  { id: "smrtna-vrzeli", titleSi: "h25 = SMRTNA VRZEL 29 let", titleEn: "The h25 = A 29-YEAR DEATH GAP", bodySi: "5 knjig a BREZ 04106: noben mrliški zapis 1857–1885 (29 let!) kljub krstnim blokom 1876 + 1883 ×2 in poroki v 01738 (m3-kandidat, P253!). Šele 04894 prinese 7 blokov (1888–1923) — mrežna luknja, ne stvarna.", bodyEn: "5 books but WITHOUT 04106: no death record 1857–1885 (29 years!) despite the baptism blocks 1876 + 1883 ×2 and a marriage in 01738 (the m3 candidate, P253!). Only 04894 brings 7 blocks (1888–1923) — a network hole, not a real one." },
  { id: "razponi-96", titleSi: "P255: h6 = 96-letni razpon (nov rekord!)", titleEn: "P255: the h6 = a 96-year span (the new record!)", bodySi: "h6 dokumentirana 1828→1924 (96 let!) — m6-1828-v-predhodniku × 04894-1924-mrliška; sledita h22 (93: 1828–1921) in h61 (91: 1828–1919) — ★★★ P256: h20 zdaj 93 let (1829–1922 — IZENAČI-h22!) + h62 95 let (1829–1924 — 2.-mesto!-KRIŽAN-ženin-44-let-pred-HRIŽAN-ŠIV!) + h5 90 (5.); stari-rekord-66 (h2/h13/h50/h60/h64) ostaja za štiri-knjižnimi.", bodyEn: "The h6 documented 1828→1924 (96 years!) — then h22 (93) and h61 (91) — ★★★ P256: h20 now 93 years (1829–1922 — ties-h22!) + h62 95 years (1829–1924 — 2nd place!) + h5 90 (5th); the old record 66 remains for the four-book houses." },
  { id: "skrita-hisa", titleSi: "h[?] = skrita hiša brez številke", titleEn: "The h[?] = the hidden house without a number", bodySi: "10 blokov 1857–1885 (8 v 04104 + 2 v 04106) z izpraznjeno hišno celico — edina hiša korpusa brez številke; P235/P220 X-OPEN. V kasnejših knjigah izgine (razrešena številka?).", bodyEn: "10 blocks 1857–1885 (8 in 04104 + 2 in 04106) with an emptied house cell — the only corpus house without a number; P235/P220 X-OPEN. It vanishes in the later books (a resolved number?)." },
];
