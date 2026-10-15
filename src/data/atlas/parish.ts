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
 * P79 (issue #18, 2026-10-15): VZORČNI PREPIS — polno leto 1886 (skeni
 * 2–15, strani 1–14 Krstne knjige 04105: vsi vpisi z Griblji v tem letu)
 * + sidro 1887 (verifikacija obstoječega zapisa hiše 61). Pred P79:
 * prepisana samo hiša 61. Kurrent branja imen z [~] (negotovost);
 * hišne številke preverjene z izrezi. PT usklajenost: 10/13 vpisov v
 * naboru PT 1825 (1–40 + 61–99), 54/56/57 v luknji 41–60 — dokaz
 * številčne evolucije (dokaz: research/issue17/parish-sample-transcription.json;
 * verifikator: scripts/p79_parish_sample.py --check, I1–I8).
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
  // ——— P79 vzorec: polno leto 1886 (vsi Griblje vpisi, strani 1–14) ———
  {
    houseNo: "8",
    bookSignature: "04105",
    year: 1886,
    scan: 2,
    page: 1,
    whatSi: "krščena Barbara (7. 1.) — oče Janez Jakofčič [~] ½ zemg., mati Marija roj. Meh [~]; hišna št. 8 [~] (drobna, bleda)",
    whatEn: "baptized Barbara (Jan 7) — father Janez Jakofčič [~] half-farmer, mother Marija née Meh [~]; house no. 8 [~] (tiny, faint)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04105",
    year: 1886,
    scan: 2,
    page: 1,
    whatSi: "krščena Marija (13. 1.) — oče Janez Pintec? [~] ½ zemg., mati Ana roj. Strauš [~]; hiša 54 v PT luknji 41–60 (evolucija številčenja)",
    whatEn: "baptized Marija (Jan 13) — father Janez Pintec? [~] half-farmer, mother Ana née Strauš [~]; house 54 in the PT 41–60 gap (numbering evolution)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1886,
    scan: 4,
    page: 3,
    whatSi: "krščena Neža (18. 2.) — oče Matija Plebučar? [~] ½ zemg., mati Katarina rojena Meh; poznejši pripis: umrla 19.3.1962 [~]",
    whatEn: "baptized Neža (Feb 18) — father Matija Plebučar? [~] half-farmer, mother Katarina née Meh; later note: died 19 Mar 1962 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "57",
    bookSignature: "04105",
    year: 1886,
    scan: 4,
    page: 3,
    whatSi: "krščen Jurij (1./2. 4.) — oče Peter Podolivec, hižar, mati Marija roj. Stupanič; hiša 57 (razločena od 54 na isti strani) v PT luknji 41–60",
    whatEn: "baptized Jurij (Apr 1/2) — father Peter Podolivec, cottager, mother Marija née Stupanič; house 57 (distinct from 54 on the same page) in the PT 41–60 gap",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04105",
    year: 1886,
    scan: 6,
    page: 5,
    whatSi: "krščen Anton (19. 5.) — oče Matija Kurnič [~] ½ zemg., mati Katarina roj. Dragoš",
    whatEn: "baptized Anton (May 19) — father Matija Kurnič [~] half-farmer, mother Katarina née Dragoš",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1886,
    scan: 7,
    page: 6,
    whatSi: "krščena Marija (10./12. 6.) — oče NI zapisan (prazna celica), mati Barbara Šimec roj. [~]; hiša 36, prvi od dveh vpisov 1886",
    whatEn: "baptized Marija (Jun 10/12) — father NOT recorded (empty cell), mother Barbara Šimec née [~]; house 36, first of two 1886 entries",
    status: "DOCUMENTED",
  },
  {
    houseNo: "94",
    bookSignature: "04105",
    year: 1886,
    scan: 9,
    page: 8,
    whatSi: "krščen Jožef (7./8. 8.) — oče Matija Rambič? [~] ½ zemg., mati Ana roj. Podlivc [~]; hiša 94 je v PT naboru (61–99 blok)",
    whatEn: "baptized Jožef (Aug 7/8) — father Matija Rambič? [~] half-farmer, mother Ana née Podlivc [~]; house 94 is in the PT set (61–99 block)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "39",
    bookSignature: "04105",
    year: 1886,
    scan: 12,
    page: 11,
    whatSi: "krščen Janez (23./24. 10.) — oče Nikolaj Šimec ½ zemg., mati Barbara roj. Jakopič; poznejši pripis: umrl 18.9.1961 v Gribljah št. 39 (potrjuje hišno št.)",
    whatEn: "baptized Janez (Oct 23/24) — father Nikolaj Šimec half-farmer, mother Barbara née Jakopič; later note: died 18 Sep 1961 in Griblje no. 39 (confirms the house number)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1886,
    scan: 12,
    page: 11,
    whatSi: "krščena Katarina (1. 11.) — oče Matija Jakopič? [~] ½ zemg., mati Marija roj. Podlivc? [~]; robovni zapis + 37/9.1887",
    whatEn: "baptized Katarina (Nov 1) — father Matija Jakopič? [~] half-farmer, mother Marija née Podlivc? [~]; marginal +37/9.1887",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04105",
    year: 1886,
    scan: 13,
    page: 12,
    whatSi: "krščen Matija (12./13. 11.) — oče Jurij Strauš ½ zemg., mati Barbara roj. Jakopič; robovni zapis + ½ 91",
    whatEn: "baptized Matija (Nov 12/13) — father Jurij Strauš half-farmer, mother Barbara née Jakopič; marginal +½91",
    status: "DOCUMENTED",
  },
  {
    houseNo: "56",
    bookSignature: "04105",
    year: 1886,
    scan: 14,
    page: 13,
    whatSi: "krščena Marija (21. 11.) — oče Janez Šimec ½ zemg., mati Dora roj. Podžire [~]; hiša 56 v PT luknji 41–60",
    whatEn: "baptized Marija (Nov 21) — father Janez Šimec half-farmer, mother Dora née Podžire [~]; house 56 in the PT 41–60 gap",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1886,
    scan: 15,
    page: 14,
    whatSi: "krščena Marija (23. 12.) — oče Matija Križan ½ zemg., mati Ana roj. Milavec; hiša 36, DRUGI vpis v 1886 (dve družini pod eno hišno št. [~])",
    whatEn: "baptized Marija (Dec 23) — father Matija Križan half-farmer, mother Ana née Milavec; house 36, SECOND 1886 entry (two families under one house number [~])",
    status: "DOCUMENTED",
  },
  // ——— P79 sidro 1887 (isti postopek, dodatni dokaz) ———
  {
    houseNo: "75",
    bookSignature: "04105",
    year: 1887,
    scan: 20,
    page: 19,
    whatSi: "krščen Janez (16. 4.) — oče Janez Jakobič? [~] ½ zemg., mati Marija roj. Stubler",
    whatEn: "baptized Janez (Apr 16) — father Janez Jakobič? [~] half-farmer, mother Marija née Stubler",
    status: "DOCUMENTED",
  },
  // ——— pred P79 (hiša 61; P79 ponovno prebral in potrdil sken 20) ———
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
