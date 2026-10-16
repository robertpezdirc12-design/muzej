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
 * P82 (issue #18, 2026-10-16): ŠIRITEV VZORCA NA LETO 1887 — krstna 04105
 * skeni 16–27 == strani 15–26 (glava »Leto 18_87« na str. 15; leto 1888 se
 * začne na str. 26 po row 106 z velikimi ciframi »1 8 8 8«): vsi vpisi z
 * Griblji = 20 vpisov / 19 različnih hiš (2, 15, 17, 21, 24, 26 [~], 27,
 * 31×2, 34, 35, 47, 52→04→15 [~], 55, 61, 62, 63, 65, 66, 78) — NOVI
 * luknji 47 in 55 (52 izvirno row 78; trojna korekcija); P79 SIDRA hiša 61
 * re-verificirana (row 28, oče zdaj »Miko Požek« [~]) in hiša 78 P82 RE-READ
 * KOREKCIJA (P79 je prebral »75« — izrez: dve zaprti zanki = 8, isti vzorec
 * forenzike kot P80 3-vs-5); NEZAKONSKI vpisi 2
 * (52, 55 — očeta stolpec prazen); ANOMALIJA row 93 (žensko ime v očetovem
 * stolpcu); trije duhovniki 1887 (Griebel [~] 14×, Dovgan, »Jos. Povmij« [~]);
 * babica Marija Brinec 9×. Dokaz: research/issue17/parish-baptism-1887.json;
 * verifikator: scripts/p82_parish_baptism_1887.py --check (I1–I10).
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
  // ——— P79 sidro (verifikacija obstoječega zapisa hiše »75«); P82 RE-READ
  // KOREKCIJA: hiša 78, ne 75 — izrez Kurrent: dve zaprti zanki = 8 (ist
  // vzorec kot P80 forenzika 3 vs 5); starši/otrok/datum == P79 branje ———
  {
    houseNo: "78",
    bookSignature: "04105",
    year: 1887,
    scan: 20,
    page: 19,
    whatSi: "krščen Janez (16. 4.) — oče Janez Jakobič ½ zemg., mati Marija roj. Stubler; botra Miha Brodnec [~] + Marija Jakobič [~]; hišna št. 78 (P82 RE-READ: ne 75 — izrez: dve zaprti zanki = 8)",
    whatEn: "baptized Janez (Apr 16) — father Janez Jakobič half-farmer, mother Marija née Stubler; godparents Miha Brodnec [~] + Marija Jakobič [~]; house no. 78 (P82 RE-READ: not 75 — the crop: two closed loops = 8)",
    status: "DOCUMENTED",
  },
  // ——— pred P79 (hiša 61; P79 ponovno prebral in potrdil sken 20; P82 izrez:
  // oče = »Miko Požek« [~] — prej branje »Miha P.—« ohranjeno kot zgodovina) ———
  {
    houseNo: "61",
    bookSignature: "04105",
    year: 1887,
    scan: 20,
    page: 19,
    whatSi: "krščena Katarina (31. 4. [sic]) — oče Miha P.— (priimek v Kurrentu negotovo: P—žar/P—žt; P82 izrez: Miko Požek [~]), mati Bara roj. Filath [~]; botra Matija Meh + Ana Pezdirc",
    whatEn: "baptized Katarina (Apr 31 [sic]) — father Miha P.— (surname in Kurrent uncertain; P82 crop: Miko Požek [~]), mother Bara née Filath [~]; godparents Matija Meh + Ana Pezdirc",
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
  // ——— P82 razširitev: KRSTNA KNJIGA 04105 — polno leto 1887 (skeni 16–27 ==
  // strani 15–26; glava »Leto 18_87« na str. 15; leto 1888 se začne na str. 26
  // po row 106 z velikimi ciframi »1 8 8 8«) — vsi vpisi z Griblji (20) ———
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1887,
    scan: 17,
    page: 16,
    whatSi: "krščena Katarina (20./21. 1.) — oče Nikolaj Prižan [~] ½ zemlj., mati Barbara roj. Pezdirec [~]; botra Matve Pezdirec + Barbara Brodarič [~]",
    whatEn: "baptized Katarina (Jan 20/21) — father Nikolaj Prižan [~] half-farmer, mother Barbara née Pezdirec [~]; godparents Matve Pezdirec + Barbara Brodarič [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04105",
    year: 1887,
    scan: 17,
    page: 16,
    whatSi: "krščena Marija (1./3. 3.) — oče Jurc Briuc [~] (ali Brine) ¼ zemlj., mati Katarina roj. Jakobič; hišna št. 26 [~] (isti kodrasti 2 kot hiša 2 na str. 24)",
    whatEn: "baptized Marija (Mar 1/3) — father Jurc Briuc [~] (or Brine) quarter-farmer, mother Katarina née Jakobič; house no. 26 [~] (the same curly 2 as house 2 on p. 24)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04105",
    year: 1887,
    scan: 21,
    page: 20,
    whatSi: "krščena Marjeta (13. 5.) — oče Anton Kure [~] ½ zemlj., mati Barbara roj. Hrižan [~]; botra Matija Milek + Bara Brodarič [~]; poznejši pripis: umrla 4. 7. 1958",
    whatEn: "baptized Marjeta (May 13) — father Anton Kure [~] half-farmer, mother Barbara née Hrižan [~]; godparents Matija Milek + Bara Brodarič [~]; later note: died Jul 4, 1958",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1887,
    scan: 23,
    page: 22,
    whatSi: "krščena Katarina (20. 7.) — oče Janez Kukar [~] (ali Kuhar) ½ zemljašt., mati Katarina Klobučar [~]; botra Janez Požek + Marija Anie [~]",
    whatEn: "baptized Katarina (Jul 20) — father Janez Kukar [~] (or Kuhar) half-smallholder, mother Katarina Klobučar [~]; godparents Janez Požek + Marija Anie [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1887,
    scan: 23,
    page: 22,
    whatSi: "krščena Ana (1./2. 8.) — oče Matija Urh [~] ½ zemljašt., mati Marija Brodarič; botra Jurij Pezdirc + Ana Hrižan [~]; drugi vpis na hiši 31 v 1887 (mrliška 1886: Katarina Marh — P80)",
    whatEn: "baptized Ana (Aug 1/2) — father Matija Urh [~] half-smallholder, mother Marija Brodarič; godparents Jurij Pezdirc + Ana Hrižan [~]; the second entry at house 31 in 1887 (death register 1886: Katarina Marh — P80)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "66",
    bookSignature: "04105",
    year: 1887,
    scan: 24,
    page: 23,
    whatSi: "krščena Ana (2. 9.) — oče Janez Hrižan ¼ zemlj., mati Katarina Milek [~]; botra Janez Brinec + Katarina Pezdirc [~]; babica Marija Brinec; poznejši pripis: umrla 7. 5. 1957 [~]",
    whatEn: "baptized Ana (Sep 2) — father Janez Hrižan quarter-farmer, mother Katarina Milek [~]; godparents Janez Brinec + Katarina Pezdirc [~]; midwife Marija Brinec; later note: died May 7, 1957 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1887,
    scan: 24,
    page: 23,
    whatSi: "krščen Janez (6. 9.) — oče Martin Papič [~] ½ zemljašt., mati Margaretha Straus; botra Marko Klobučar + Marija Jakobič [~]; babica Marija Brinec; drugi vpis na hiši 31 v 1887",
    whatEn: "baptized Janez (Sep 6) — father Martin Papič [~] half-smallholder, mother Margaretha Straus; godparents Marko Klobučar + Marija Jakobič [~]; midwife Marija Brinec; the second entry at house 31 in 1887",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1887,
    scan: 25,
    page: 24,
    whatSi: "krščena Katarina (25. 9.) — oče Matija Milek ½ zemljašt., mati Katarina Požek; botra Peter Pezdirc + Barbara Adlešič; babica Marija Brinec",
    whatEn: "baptized Katarina (Sep 25) — father Matija Milek half-smallholder, mother Katarina Požek; godparents Peter Pezdirc + Barbara Adlešič; midwife Marija Brinec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "2",
    bookSignature: "04105",
    year: 1887,
    scan: 25,
    page: 24,
    whatSi: "krščen Nikolaj (3./4. 10.) — oče Peter Hlebec ¼ zemljašt., mati Ana Jakobič; botra Janez Klobučar + Katarina Zumri [~]; babica Marija Brinec; pripisa: umrl 4. 9. 1961 v Gribljah št. 2 + poročen 18. 5. 1919",
    whatEn: "baptized Nikolaj (Oct 3/4) — father Peter Hlebec quarter-smallholder, mother Ana Jakobič; godparents Janez Klobučar + Katarina Zumri [~]; midwife Marija Brinec; notes: died Sep 4, 1961 in Griblje no. 2 + married May 18, 1919",
    status: "DOCUMENTED",
  },
  {
    houseNo: "52",
    bookSignature: "04105",
    year: 1887,
    scan: 25,
    page: 24,
    whatSi: "krščena Terezija (12. 10.) — očeta stolpec PRAZEN (nezakonska), mati Marija Muc [~]; TROJNA KOREKCIJA hišne št. 52 → 04 → 15 [~] (izvirno 52 v luknji, končna 15 v naboru — obe klasifikaciji); botra Janez Jakobič + Katarina Kure [~]; babica Marija Filath [~]",
    whatEn: "baptized Terezija (Oct 12) — father's column EMPTY (illegitimate), mother Marija Muc [~]; TRIPLE CORRECTION of house no. 52 → 04 → 15 [~] (the original 52 in the gap, the final 15 in the set — both classifications); godparents Janez Jakobič + Katarina Kure [~]; midwife Marija Filath [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "55",
    bookSignature: "04105",
    year: 1887,
    scan: 25,
    page: 24,
    whatSi: "krščena Eva (13./14. 10.) — očeta stolpec PRAZEN (nezakonska), mati Ana Smič [~] ¼ zemlj.; botra Janez Vrbiščar [~] + Marg. Pezolivec [~]; hiša 55 v PT luknji 41–60 (nova luknja)",
    whatEn: "baptized Eva (Oct 13/14) — father's column EMPTY (illegitimate), mother Ana Smič [~] quarter-farmer; godparents Janez Vrbiščar [~] + Marg. Pezolivec [~]; house 55 in the PT 41–60 gap (a new gap house)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "17",
    bookSignature: "04105",
    year: 1887,
    scan: 25,
    page: 24,
    whatSi: "krščen Jožef (14./15. 10.) — oče Janez Kralj ¼ zemlj., mati Ana Jakobič; botra Janez Pezdirc + Marija Jakofčič; babica Marija Brinec",
    whatEn: "baptized Jožef (Oct 14/15) — father Janez Kralj quarter-farmer, mother Ana Jakobič; godparents Janez Pezdirc + Marija Jakofčič; midwife Marija Brinec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1887,
    scan: 26,
    page: 25,
    whatSi: "krščen Janez (1./2. 11.) — oče Janez Šimec ½ zemlj., mati Ana Šmucelj [~]; botra Anton Brodarič [~] + Barbara Lozar; modri pripisi 20. st.",
    whatEn: "baptized Janez (Nov 1/2) — father Janez Šimec half-farmer, mother Ana Šmucelj [~]; godparents Anton Brodarič [~] + Barbara Lozar; blue 20th-century notes",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04105",
    year: 1887,
    scan: 26,
    page: 25,
    whatSi: "krščena Marija (7./8. 11.) — oče Janez Jakšič [~] ½ zemlj., mati Marija Brinec; botra Janez Adlešič [~] + Katarina Klobučar [~]; babica Marija Brinec; pripis »+ ½ 88«(?) [~]",
    whatEn: "baptized Marija (Nov 7/8) — father Janez Jakšič [~] half-farmer, mother Marija Brinec; godparents Janez Adlešič [~] + Katarina Klobučar [~]; midwife Marija Brinec; note »+ ½ 88«(?) [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04105",
    year: 1887,
    scan: 26,
    page: 25,
    whatSi: "krščen Janez (18. 11.) — ANOMALIJA ZAPISA: v očetovem stolpcu »Marija Hrižan ½ zemljašt.«, v materinem »Ana Požek« [~] (možno mati Marija Hrižan roj. Požek); botra prazna; pripis »+ ½ 93« [~]",
    whatEn: "baptized Janez (Nov 18) — RECORDING ANOMALY: the father's column holds »Marija Hrižan ½ zemljašt.«, the mother's »Ana Požek« [~] (possibly mother Marija Hrižan née Požek, split across columns); godparents empty; note »+ ½ 93« [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "47",
    bookSignature: "04105",
    year: 1887,
    scan: 26,
    page: 25,
    whatSi: "krščena Barbara (18. 11.) — oče Peter Klobučar [~] ½ zemljašt., mati Marija Filath [~]; botra Janez Lasič + Katarina Straus; babica Marija Brinec; hiša 47 v PT luknji 41–60 (nova luknja)",
    whatEn: "baptized Barbara (Nov 18) — father Peter Klobučar [~] half-smallholder, mother Marija Filath [~]; godparents Janez Lasič + Katarina Straus; midwife Marija Brinec; house 47 in the PT 41–60 gap (a new gap house)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1887,
    scan: 27,
    page: 26,
    whatSi: "krščen Nikolaj (18. 12.) — oče Janez Požek ½ zemlj., mati Marija Brinec; botra Anton Brodarič [~] + Katarina Kuhtar [~]; babica Marija Brinec; pripis »+ 4/6. …« [~]",
    whatEn: "baptized Nikolaj (Dec 18) — father Janez Požek half-farmer, mother Marija Brinec; godparents Anton Brodarič [~] + Katarina Kuhtar [~]; midwife Marija Brinec; note »+ 4/6. …« [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1887,
    scan: 27,
    page: 26,
    whatSi: "krščena Marija (29. 12.) — oče Matija Brinec ½ zemljašt., mati Barbara Jakobec [~]; botra Peter Pezdirc [~] + Marija Milek [~]; babica Marija Brinec",
    whatEn: "baptized Marija (Dec 29) — father Matija Brinec half-smallholder, mother Barbara Jakobec [~]; godparents Peter Pezdirc [~] + Marija Milek [~]; midwife Marija Brinec",
    status: "DOCUMENTED",
  },
];
