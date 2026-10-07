// ATLAS 1825 — ŽUPNIJA PODZEMELJ: matične knjige 1669–1947 (issue #6)
// Vir: Matricula Online — Nadškofijski arhiv Ljubljana, župnija Podzemelj.
// Dostop preverjen 2026-10-07: Griblje je izrecno navedeno v zgodovinskem
// matičnem območju župnije; sv. Vid v Gribljah je 3. podružnica.
// Vse signature in obdobja so prepisane s seznama knjig na Matricula Online.

export type ParishBookType = "baptism" | "marriage" | "death";

export interface ParishBook {
  /** signatura v Nadškofijem arhivu Ljubljana (npr. 01723) */
  signature: string;
  type: ParishBookType;
  from: number;
  to: number;
  /** javna povezava na Matricula Online (preverjena 2026-10-07) */
  url: string;
  status: "DOCUMENTED";
}

/** Župnija, katere matično območje pokriva Griblje (vir: Matricula Online) */
export const PARISH = {
  nameSi: "Župnija Podzemelj",
  nameEn: "Parish of Podzemelj",
  patronSi: "sv. Martin",
  patronEn: "St. Martin",
  archiveSi: "Nadškofijski arhiv Ljubljana",
  archiveEn: "Archdiocesan Archive of Ljubljana",
  /** sv. Vid, Griblje — 3. podružnica (Krasinec, Zemelj, Griblje, Klošter, Dobravice) */
  filialSi: "sv. Vid, Griblje — 3. podružnica",
  filialEn: "St. Vitus, Griblje — 3rd filial church",
  url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/",
  /** obdobje po naslovu fonda na Matricula (1669–1947); zvezki sami segajo do 1924 */
  period: "1669–1947",
  /** 22 zvezka na seznamu župnije — vseh 22 v spodnjem registru */
  noteSi:
    "Matično območje župnije (vir): Adlešiči niso — Griblje, Podzemelj, Gradac, Klošter, Krasinec, Zemelj, Dobravice, Geršiči, Dragoši, Boršt, Mlake, Otok, Prilozje, Primostek, Škrilje, Vranoviči, Kapljišče, Cerkvišče, Boginja vas, Grm, Pribinci, Pavičiči pri Zastavi.",
  noteEn:
    "Historical parish territory (source): Griblje, Podzemelj, Gradac, Klošter, Krasinec, Zemelj, Dobravice, Geršiči, Dragoši, Boršt, Mlake, Otok, Prilozje, Primostek, Škrilje, Vranoviči, Kapljišče, Cerkvišče, Boginja vas, Grm and more.",
  accessedAt: "2026-10-07",
} as const;

export const PARISH_BOOKS: ParishBook[] = [
  // KRSTNE (Taufbuch) 1675–1919
  { signature: "01723", type: "baptism", from: 1675, to: 1703, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01723/", status: "DOCUMENTED" },
  { signature: "01724", type: "baptism", from: 1719, to: 1725, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01724/", status: "DOCUMENTED" },
  { signature: "01725", type: "baptism", from: 1726, to: 1740, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01725/", status: "DOCUMENTED" },
  { signature: "01726", type: "baptism", from: 1740, to: 1756, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01726/", status: "DOCUMENTED" },
  { signature: "01727", type: "baptism", from: 1756, to: 1797, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01727/", status: "DOCUMENTED" },
  { signature: "01728", type: "baptism", from: 1784, to: 1795, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01728/", status: "DOCUMENTED" },
  { signature: "01729", type: "baptism", from: 1797, to: 1828, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01729/", status: "DOCUMENTED" },
  { signature: "01730", type: "baptism", from: 1829, to: 1847, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01730/", status: "DOCUMENTED" },
  { signature: "01731", type: "baptism", from: 1848, to: 1870, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01731/", status: "DOCUMENTED" },
  { signature: "04104", type: "baptism", from: 1871, to: 1885, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/", status: "DOCUMENTED" },
  { signature: "04105", type: "baptism", from: 1886, to: 1919, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/", status: "DOCUMENTED" },
  // MRLIŠKE (Sterbebuch) 1725–1924
  { signature: "01732", type: "death", from: 1725, to: 1768, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01732/", status: "DOCUMENTED" },
  { signature: "01733", type: "death", from: 1728, to: 1803, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01733/", status: "DOCUMENTED" },
  { signature: "01734", type: "death", from: 1771, to: 1828, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01734/", status: "DOCUMENTED" },
  { signature: "01735", type: "death", from: 1829, to: 1856, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01735/", status: "DOCUMENTED" },
  { signature: "04106", type: "death", from: 1857, to: 1885, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04106/", status: "DOCUMENTED" },
  { signature: "04894", type: "death", from: 1886, to: 1924, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/", status: "DOCUMENTED" },
  // POROČNE (Trauungsbuch) 1669–1922
  { signature: "04795", type: "marriage", from: 1669, to: 1679, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04795/", status: "DOCUMENTED" },
  { signature: "01736", type: "marriage", from: 1723, to: 1770, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01736/", status: "DOCUMENTED" },
  { signature: "01737", type: "marriage", from: 1771, to: 1827, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01737/", status: "DOCUMENTED" },
  { signature: "01738", type: "marriage", from: 1828, to: 1873, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/", status: "DOCUMENTED" },
  { signature: "04455", type: "marriage", from: 1873, to: 1922, url: "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/", status: "DOCUMENTED" },
];

/**
 * HIŠNE ZGODBE — matrični vpisi z gribeljskimi hišnimi številkami.
 * Dokumentirano iz zapisa sveti-vid (Krstna knjiga 04105, vpisi z Griblji).
 * Ostale hiše: status TO_COLLECT (vpisov še nismo prebrali/prepisali).
 */
export interface HouseVital {
  houseNo: string;
  bookSignature: string;
  year: number;
  scan?: number;
  page?: number;
  whatSi: string;
  whatEn: string;
  status: "DOCUMENTED";
}

export const HOUSE_VITALS: HouseVital[] = [
  {
    houseNo: "61",
    bookSignature: "04105",
    year: 1887,
    scan: 20,
    whatSi: "krščena Katarina — oče Miha P.— (priimek v Kurrentu negotovo: P—žar/P—žt)",
    whatEn: "baptized Katarina — father Miha P.— (surname in Kurrent uncertain)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04105",
    year: 1897,
    scan: 100,
    page: 49,
    whatSi: "krščen Anton — oče Miha P.—",
    whatEn: "baptized Anton — father Miha P.—",
    status: "DOCUMENTED",
  },
];
