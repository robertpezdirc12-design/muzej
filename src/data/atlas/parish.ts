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
 * P80 (issue #18, 2026-10-16): RAZŠIRITEV VZORCA na mrliško (04894)
 * in poročno (04455) knjigo — okvir 1886 v obeh (mrliška: skeni 2–6 ==
 * strani 1–5, 46 vrstic, 13 Griblje vpisov / 11 hiš; poročna: skeni
 * 61–65 == Pag. 60–64, 24 vpisov, 7 Griblje vpisov / 10 hiš) + sidra
 * (mrliška 1887: sken 6, hiši 44 in 36; poročna: Nov 1885 sken 61
 * hiši 13/25, Nov 1882 sken 50 hiša 36 Križan, 1887 sken 66 hiši 71
 * in 15/29). KRIŽNE POVEZAVE (tri viri): hiša 13 (krst Matija Jakopič
 * + Marija Podlirc == starši ženina Janeza 1885 == smrt Ane Jakobuč
 * 1 leto Mar 1886), hiša 36 (krst brez očeta, mati Barbara Šimec +
 * smrt Ane Šimec neza. Jan 1887 + poroki Križan 1882 in Šimec 1886),
 * hiša 71 (krst Jurij Strauš + smrt Ane Strauš vdove Sep 1886 + poroki
 * Marije Straus Nov 1886 in Mathiasa Strausa Jan 1887 — Strauš v vseh
 * treh knjigah). P80 RE-READ: hiša 56 mati = Perdinec (ne »Podžire«)
 * — poročna 04455 sk. 62 vpis 4/1886, isti par. Dramatika vzorca: hiša
 * 29 — trije otroci (Mileh [~]) umrli v 4 dneh oktobra 1886, isti vzrok
 * »Kolera i. morbas« [~] (epidemija; februar 1887 se na hiši 29 poroki
 * Maria Brinec, katere mati je roj. Miletch [~]).
 * Dokaz: research/issue17/parish-md-transcription.json; verifikator:
 * scripts/p80_parish_md_books.py --check (I1–I10).
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
    whatSi: "krščena Marija (21. 11.) — oče Janez Šimec ½ zemg., mati Dora roj. Perdinec [~] (P80 re-read: poročna 04455 sk. 62 vpis 4/1886 — Johann Šimec × Dorothea Perdinec, isti par; prvotno P79 branje »Podžire« korigirano); hiša 56 v PT luknji 41–60",
    whatEn: "baptized Marija (Nov 21) — father Janez Šimec half-farmer, mother Dora née Perdinec [~] (P80 re-read: marriage register 04455 scan 62 entry 4/1886 — Johann Šimec × Dorothea Perdinec, same couple; the original P79 reading »Podžire« corrected); house 56 in the PT 41–60 gap",
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
  // ——— P80 razširitev: MRLIŠKA KNJIGA 04894 1886–1924 — okvir 1886 (skeni 2–6 == strani 1–5; leto 1887 se začne na strani 5 pri »Januarj 1887«) ———
  {
    houseNo: "16",
    bookSignature: "04894",
    year: 1886,
    scan: 2,
    page: 1,
    whatSi: "umrla Marija Šilah [~], ½ zemlj., 46 let (10. 1., pokop 12. 1.) — Sušica [~]; kapljan Andrej Griebel [~] (Kurrent)",
    whatEn: "died Marija Šilah [~], half-farmer, 46 years (Jan 10, buried Jan 12) — consumption [~]; curate Andrej Griebel [~] (Kurrent)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04894",
    year: 1886,
    scan: 3,
    page: 2,
    whatSi: "umrla Ana Jakobuč [~], ½ zemlj. hči, 1 leto (22. 3., pokop 23. 3.) — Davica [~]; isto gospodinjstvo kot krst Nov 1886 (oče Matija Jakopič + mati Marija Podlirc) [~]",
    whatEn: "died Ana Jakobuč [~], half-farmer's daughter, 1 year (Mar 22, buried Mar 23) — dysentery [~]; same household as the Nov 1886 baptism (father Matija Jakopič + mother Marija Podlirc) [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04894",
    year: 1886,
    scan: 3,
    page: 2,
    whatSi: "umrla Barbara Brinec [~], ½ zemlj. hči, 2 leti (28. 4., pokop 30. 4.) — Sušica [~]",
    whatEn: "died Barbara Brinec [~], half-farmer's daughter, 2 years (Apr 28, buried Apr 30) — consumption [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "59",
    bookSignature: "04894",
    year: 1886,
    scan: 3,
    page: 2,
    whatSi: "umrla Marija Podlirec [~], bajtarjeva hči, 17 let (23. 5., pokop 25. 5.) — Plunica [~]; hiša 59 v PT luknji 41–60 (izrez števk: 5, ne 3)",
    whatEn: "died Marija Podlirec [~], cottager's daughter, 17 years (May 23, buried May 25) — phthisis [~]; house 59 in the PT 41–60 gap (digit crops: 5, not 3)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04894",
    year: 1886,
    scan: 4,
    page: 3,
    whatSi: "umrl Nikolaj Muc [~], »Novac« [~], 63 let (9. 7., pokop 11. 7.) — Plunica [~]",
    whatEn: "died Nikolaj Muc [~], »Novac« [~], 63 years (Jul 9, buried Jul 11) — phthisis [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04894",
    year: 1886,
    scan: 4,
    page: 3,
    whatSi: "umrl Matija Šimer [~], ½ zemlj. sin, 4 leta (20. 7., pokop 21. 7.) — Božjask [~] (griža?)",
    whatEn: "died Matija Šimer [~], half-farmer's son, 4 years (Jul 20, buried Jul 21) — »Božjask« [~] (spasms?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "74",
    bookSignature: "04894",
    year: 1886,
    scan: 4,
    page: 3,
    whatSi: "umrl Jožef Hambeč [~], ½ zemlj. sin, 1 mesec (6. 9., pokop 8. 9.) — Slabost [~] (šibkost)",
    whatEn: "died Jožef Hambeč [~], half-farmer's son, 1 month (Sep 6, buried Sep 8) — weakness [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04894",
    year: 1886,
    scan: 5,
    page: 4,
    whatSi: "umrla Ana Straus [~], ½ zemlj. vdova, »v drugo omožena Križan« [~], 56 let (7. 9., pokop 8. 9.) — Vodenica [~] (vodna bolezen); hiša 71 = Strauš v VSEH treh knjigah",
    whatEn: "died Ana Straus [~], half-farmer's widow, »remarried Križan« [~], 56 years (Sep 7, buried Sep 8) — dropsy [~]; house 71 = Strauš in ALL THREE registers",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04894",
    year: 1886,
    scan: 5,
    page: 4,
    whatSi: "umrl Janez Mileh [~], ½ zemlj. sin, 8 let (10. 10., pokop 11. 10.) — Kolera i. morbas [~]; PRVI od trejeh otrok hiše 29, umrlih v 4 dneh (epidemija)",
    whatEn: "died Janez Mileh [~], half-farmer's son, 8 years (Oct 10, buried Oct 11) — cholera infantum [~]; FIRST of three house-29 children dead within 4 days (epidemic)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04894",
    year: 1886,
    scan: 5,
    page: 4,
    whatSi: "umrla Katarina Mileh [~], ½ zemlj. hči, 9 let (10. 10., pokop 11. 10.) — Kolera i. morbas [~]; DRUGI od trejeh",
    whatEn: "died Katarina Mileh [~], half-farmer's daughter, 9 years (Oct 10, buried Oct 11) — cholera infantum [~]; SECOND of the three",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04894",
    year: 1886,
    scan: 5,
    page: 4,
    whatSi: "umrla Katarina Marh [~], ½ zemlj. hči, 2 leti (12. 10., pokop 13. 10.) — Sušica [~]",
    whatEn: "died Katarina Marh [~], half-farmer's daughter, 2 years (Oct 12, buried Oct 13) — consumption [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04894",
    year: 1886,
    scan: 5,
    page: 4,
    whatSi: "umrla Ana Mileh [~], ½ zemlj. hči, 11 let (13. 10., pokop 15. 10.) — Kolera i. morbas [~]; TRETJI od trejeh — januarja 1887 se na hiši 29 poroki Maria Brinec, katere mati je roj. Miletch [~]",
    whatEn: "died Ana Mileh [~], half-farmer's daughter, 11 years (Oct 13, buried Oct 15) — cholera infantum [~]; THIRD of the three — in January 1887 Maria Brinec (mother née Miletch [~]) marries from house 29",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04894",
    year: 1886,
    scan: 6,
    page: 5,
    whatSi: "umrla Katarina (»Brginec« prečrtano), vdova Podec [~], 50 let (11. 12., pokop 11. 12.) — Vodenica [~]; zadnji gribeljski vpis 1886",
    whatEn: "died Katarina (»Brginec« struck through), widow Podec [~], 50 years (Dec 11, buried Dec 11) — dropsy [~]; last Griblje entry of 1886",
    status: "DOCUMENTED",
  },
  // ——— P80 sidri mrliške 1887 (isti sken 6, stran 5 — po prelomu »Januarj 1887«) ———
  {
    houseNo: "44",
    bookSignature: "04894",
    year: 1887,
    scan: 6,
    page: 5,
    whatSi: "umrl Matija Šproch [~], ½ zemlj., 48 let (1. 1., pokop 3. 1.) — Nadluka i. skovrh [~]; PRVI vpis leta 1887 (okvir: leto se začne na strani 5)",
    whatEn: "died Matija Šproch [~], half-farmer, 48 years (Jan 1, buried Jan 3) — croup and whooping cough [~]; FIRST entry of 1887 (the year begins on page 5)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04894",
    year: 1887,
    scan: 6,
    page: 5,
    whatSi: "umrla Ana Šimec [~], nezakonska, 2 leti (11. 1., pokop 12. 1.) — Sušica [~]; povezava z materjo Barbaro Šimec (krst Jun 1886, hiša 36, brez očeta) [~]",
    whatEn: "died Ana Šimec [~], illegitimate, 2 years (Jan 11, buried Jan 12) — consumption [~]; linked to mother Barbara Šimec (Jun 1886 baptism, house 36, no father) [~]",
    status: "DOCUMENTED",
  },
  // ——— P80 razširitev: POROČNA KNJIGA 04455 1873–1922 — okvir 1886 (skeni 61–65 == Pag. 60–64, vpisi 1–24; Pag. = sken − 1 v razponu 61–66) ———
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1886,
    scan: 61,
    page: 60,
    whatSi: "poroka (7. 2.) — ženin Martin Pavie [~], Gasthausmeister [~], 28, GRIBLJE 31 × Margareth Špelcer [~], 21 (bivališče neveste nečitljivo [~]); nevestini starši: Martin Straus + Maria née Stabek [~]",
    whatEn: "marriage (Feb 7) — groom Martin Pavie [~], innkeeper [~], 28, GRIBLJE 31 × Margareth Špelcer [~], 21 (bride's residence illegible [~]); bride's parents: Martin Straus + Maria née Stabek [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04455",
    year: 1886,
    scan: 62,
    page: 61,
    whatSi: "poroka (15. 2., vpis 4/1886) — ženin Johann Šimec [~], Lavrinc [~], 24, GRIBLJE 36 (starši: Johann Šimec + Maria née Jakobič [~]) × Dorothea Perdinec [~], 30, Krasinec 38 (starši: Peter Perdinec + Gertruda née Musie [~]) = ISTI PAR kot krst hiše 56 (Nov 1886: Janez Šimec + Dora roj. Perdinec) — osnova P80 re-reada",
    whatEn: "marriage (Feb 15, entry 4/1886) — groom Johann Šimec [~], day-labourer [~], 24, GRIBLJE 36 (parents: Johann Šimec + Maria née Jakobič [~]) × Dorothea Perdinec [~], 30, Krasinec 38 (parents: Peter Perdinec + Gertruda née Musie [~]) = SAME COUPLE as the house-56 baptism (Nov 1886: Janez Šimec + Dora née Perdinec) — the basis of the P80 re-read",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04455",
    year: 1886,
    scan: 63,
    page: 62,
    whatSi: "poroka (21. 2., vpis 11/1886) — nevesta Maria Bohor [~], Dienstmagd, 21, GRIBLJE 60 (starši: Georg Bohor + Katharina née Križan [~]) × Mathias Kukec [~], 30, Dragoše 2; hiša 60 v PT luknji 41–60",
    whatEn: "marriage (Feb 21, entry 11/1886) — bride Maria Bohor [~], maid, 21, GRIBLJE 60 (parents: Georg Bohor + Katharina née Križan [~]) × Mathias Kukec [~], 30, Dragoše 2; house 60 in the PT 41–60 gap",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04455",
    year: 1886,
    scan: 63,
    page: 62,
    whatSi: "poroka (21. 2., vpis 12/1886) — ženin Mathias Mileh [~], ½ Gutluner [~], 44, GRIBLJE 63 × Katharina Peršić [~], 18; priimek Mileh = umrli otroci hiše 29 (okt 1886) [~]",
    whatEn: "marriage (Feb 21, entry 12/1886) — groom Mathias Mileh [~], half-smallholder [~], 44, GRIBLJE 63 × Katharina Peršić [~], 18; the surname Mileh = the house-29 dead children (Oct 1886) [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04455",
    year: 1886,
    scan: 64,
    page: 63,
    whatSi: "poroka (20. 6., vpis 17/1886) — nevesta Ana Filak [~], 33, GRIBLJE 15 (starši: Mathias Filak + Anna née Gregorič [~]) × Georg Tomec [~], 45, Krivoglave 41; hiša 15 = smrt Nikolaja Muca (Jul 1886)",
    whatEn: "marriage (Jun 20, entry 17/1886) — bride Ana Filak [~], 33, GRIBLJE 15 (parents: Mathias Filak + Anna née Gregorič [~]) × Georg Tomec [~], 45, Krivoglave 41; house 15 = the death of Nikolaj Muc (Jul 1886)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04455",
    year: 1886,
    scan: 64,
    page: 63,
    whatSi: "poroka (8. 11., vpis 20/1886) — ženin Jurij Klepec [~], ½ zemlj. mož, 23, GRIBLJE 25 × Katharina Gomec [~], 23, Krasinec 35 (starši: Martin Gomec + Ana née Podlivc [~])",
    whatEn: "marriage (Nov 8, entry 20/1886) — groom Jurij Klepec [~], half-farmer, 23, GRIBLJE 25 × Katharina Gomec [~], 23, Krasinec 35 (parents: Martin Gomec + Ana née Podlivc [~])",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04455",
    year: 1886,
    scan: 65,
    page: 64,
    whatSi: "poroka (21. 11., vpis 23/1886) — nevesta Maria Straus [~], Leinwweber, 34, GRIBLJE 71 (starši: Janez Straus + Anna née Stubler [~]) × Marko Perzan [~], 41, Vinica 9; hiša 71 = Strauš v VSEH treh knjigah",
    whatEn: "marriage (Nov 21, entry 23/1886) — bride Maria Straus [~], linen weaver, 34, GRIBLJE 71 (parents: Janez Straus + Anna née Stubler [~]) × Marko Perzan [~], 41, Vinica 9; house 71 = Strauš in ALL THREE registers",
    status: "DOCUMENTED",
  },
  // ——— P80 sidri poročne (izven okvirja 1886 — veriga hiša→družina čez leta) ———
  {
    houseNo: "13",
    bookSignature: "04455",
    year: 1885,
    scan: 61,
    page: 60,
    whatSi: "poroka (22. 11. 1885) — ženin Janez Jakobič [~], Leinweber [~], 25, GRIBLJE 13 (starši: Mathias Jakobič + Maria née Podlirec [~] = STARŠI krsta hiše 13, Nov 1886) × Marija Stubler [~], 21, GRIBLJE 25; sidro pred okvirjem 1886",
    whatEn: "marriage (Nov 22, 1885) — groom Janez Jakobič [~], linen weaver [~], 25, GRIBLJE 13 (parents: Mathias Jakobič + Maria née Podlirec [~] = the PARENTS of the Nov 1886 house-13 baptism) × Marija Stubler [~], 21, GRIBLJE 25; anchor before the 1886 frame",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04455",
    year: 1882,
    scan: 50,
    page: 44,
    whatSi: "poroka (26. 11. 1882, vpis 26) — ženin Mathias Križan [~], Leinweber [~], 24, GRIBLJE 36 × Anna Matuschea [~], 18; = oče krsta hiše 36 (Dec 1886: oče Matija Križan, mati Ana roj. Milavec) — križni dokaz družine Križan na hiši 36",
    whatEn: "marriage (Nov 26, 1882, entry 26) — groom Mathias Križan [~], linen weaver [~], 24, GRIBLJE 36 × Anna Matuschea [~], 18; = the father of the house-36 baptism (Dec 1886: father Matija Križan, mother Ana née Milavec) — the cross evidence of the Križan family at house 36",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04455",
    year: 1887,
    scan: 66,
    page: 65,
    whatSi: "poroka (31. 1. 1887, vpis 3) — ženin Mathias Straus [~], Leinweber, 24, GRIBLJE 71 (starši: Mathias Straus + Katharina née Dragoš [~]) × Barbara Rusié [~], 21, GRIBLJE 37 (starši: Michael Rusié + Katharina née Šambiè [~]); sidro po okvirju 1886",
    whatEn: "marriage (Jan 31, 1887, entry 3) — groom Mathias Straus [~], linen weaver, 24, GRIBLJE 71 (parents: Mathias Straus + Katharina née Dragoš [~]) × Barbara Rusié [~], 21, GRIBLJE 37 (parents: Michael Rusié + Katharina née Šambiè [~]); anchor after the 1886 frame",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04455",
    year: 1887,
    scan: 66,
    page: 65,
    whatSi: "poroka (6. 2. 1887, vpis 4) — ženin Johann Šambie [~], Leinweber, 23, GRIBLJE 15 × Maria Brinec [~], 26, GRIBLJE 29 (starši: Mathias Brinec + Maria née Miletch [~] — družina umrlih otrok hiše 29); sidro",
    whatEn: "marriage (Feb 6, 1887, entry 4) — groom Johann Šambie [~], linen weaver, 23, GRIBLJE 15 × Maria Brinec [~], 26, GRIBLJE 29 (parents: Mathias Brinec + Maria née Miletch [~] — the family of the house-29 dead children); anchor",
    status: "DOCUMENTED",
  },
];
