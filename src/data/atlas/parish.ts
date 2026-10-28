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
 * »Kolera i. morbas« [~] (epidemija; feb. 1887 se poroki Maria Brinec —
 * P116 re-read: iz GRIBLJE 23, ne 29; povezava z h29 ostaja pri materi
 * roj. Milek [~]).
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
    page: 97,
    whatSi: "krščen Anton (20./20. 11.) — oče Janez Muc [~] bajtar (P79-era placeholder je bral »Miha P.—« [~] pri strani 49 po stari predpostavki — P92 5x forenzika: jasno Janez Muc bajtar; stran == sken − 3 po noveli P92), mati Ana Kure [~]; hišna 61 forenzika: jasno 61 — 5. pin (1887 sidro + 1891 + 1892 + 1897); botra Nikolaj Željko [~] + Katarina Kure [~] = h1 PAR KOT BOTRA (ŽELJKO × KURE — začarani krog familije kot P91 h1); pripis 20. st.: »Zakonca Mihelk Katarina umrla 26.5.1979 (MMK Griblje 1.1979)« + EHS ČG 2012894500081; babica PRAZNA; podpis Fr. Klun [~] (P92 sidro — blok posodobljen in združen s P92 razširitvijo)",
    whatEn: "baptized Anton (Nov 20/20) — father Janez Muc [~] cottager (the P79-era placeholder read »Miha P.—« [~] at page 49 under the old assumption — P92 5x forensics: clearly Janez Muc cottager; page == scan − 3 per the P92 novel), mother Ana Kure [~]; house no. 61 (forensics: clearly 61) — the 5th pin (1887 anchor + 1891 + 1892 + 1897); godparents Nikolaj Željko [~] + Katarina Kure [~] = THE h1 COUPLE AS GODPARENTS (ŽELJKO × KURE — the family's closed circle like P91 h1); 20th-c. notes: »the spouse Mihelk Katarina died May 26, 1979 (MMK Griblje 1.1979)« + EHS ČG 2012894500081; midwife EMPTY; signature Fr. Klun [~] (P92 anchor — the block updated and merged with the P92 extension)",
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
    whatSi: "umrla Ana Mileh [~], ½ zemlj. hči, 11 let (13. 10., pokop 15. 10.) — Kolera i. morbas [~]; TRETJI od trejeh — feb. 1887 se poroki Maria Brinec (P116 re-read: iz GRIBLJE 23, ne 29 — poročna hiša; mati neveste roj. Milek [~] = povezava z to družino)",
    whatEn: "died Ana Mileh [~], half-farmer's daughter, 11 years (Oct 13, buried Oct 15) — cholera infantum [~]; THIRD of the three — in February 1887 Maria Brinec marries (the P116 re-read: from GRIBLJE 23, not 29 — the marriage house; the bride's née-Milek mother [~] = the link to this family)",
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
  // ——— P153: MRLIŠKA 04894, leto 1887 = 1. POLNO leto mrliške linije (71 vrstic / 13 Griblje-vpisov / 13 hiš = ISTA številka kot 1886!) — meja 1888 = veliki cifri »1 8 8 8« na s13 + letnica-glava »Leto 18 ....« PRAZNA (1. primer!); 11 novih blokov (P80 sidra r1 h44 + r4 h36 zgoraj); max-zoom popravki: r66 hiša 58 (ne 53!) · r55 Matija-Požek (ne Marija-Požit!) · r61 Matija-Milek (ne Marija!) · r63 ¼ ure (ne ½!) — dokaz research/issue17/parish-death-1887.json ———
  {
    houseNo: "65",
    bookSignature: "04894",
    year: 1887,
    scan: 8,
    page: 7,
    whatSi: "umrl Mihael Milek [~], samski kmetlji sluga [~ samsk-kmetlj.], 49 let (23. 3., pokop 25. 3.) — Sušica; Andrej Glibel; 1. od DVEH Milek-smrti 1887 (h22 Oktober!)",
    whatEn: "died Mihael Milek [~], an unmarried smallholders' servant [~], 49 years (Mar 23, buried Mar 25) — consumption; Andrej Glibel; the 1st of TWO Milek deaths 1887 (h22 October!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04894",
    year: 1887,
    scan: 8,
    page: 7,
    whatSi: "umrla Katarina Klobučar [~], ½ zemljičarjeva vdova, 74 let (27. 3., pokop 29. 3.) — Plučni mrah [~ Pluni-mrahund]; Andrej Glibel; NAJSTAREJŠA umrla 1887 (74)",
    whatEn: "died Katarina Klobučar [~], a half-farmer's widow, 74 years (Mar 27, buried Mar 29) — pulmonary marasmus [~]; Andrej Glibel; the OLDEST death of 1887 (74)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04894",
    year: 1887,
    scan: 9,
    page: 8,
    whatSi: "umrla Marija Šimec [~], ½ Hobarjeva žena [~ holarjeva], 62 let (2. 4., pokop 3. 4.) — Vodenica; Andrej Glibel; 2. ŠIMEC-smrt 1887 (po h36-Ana Januar!)",
    whatEn: "died Marija Šimec [~], a half-holar's wife [~], 62 years (Apr 2, buried Apr 3) — dropsy; Andrej Glibel; the 2nd ŠIMEC death of 1887 (after h36-Ana January!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "76",
    bookSignature: "04894",
    year: 1887,
    scan: 9,
    page: 8,
    whatSi: "umrla Barbara Husič [~], gemž. ¼ zemlj. žena [~ gemžgarjeva], 54 let (26. 4., pokop 28. 4.) — Plunica; Andrej Glibel; hiša 76 = Husič — 26 let pred 1. krstnim blokom (1913)!",
    whatEn: "died Barbara Husič [~], a gemžar's wife [~], 54 years (Apr 26, buried Apr 28) — pneumonia [~]; Andrej Glibel; house 76 = the Husič — 26 years before its 1st baptism block (1913)!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04894",
    year: 1887,
    scan: 11,
    page: 10,
    whatSi: "umrla Doroteja Križan [~ z/ž], gemžgina [~ omžgina], 39 let (31. 8., pokop 1. 9.) — Sušica; previdena (izpisano!); Ant./And. Glibe coop. [~ t/d]; 140-dnevna vrzel brez gribeljske smrti se zapre (13. 4. → 31. 8.)",
    whatEn: "died Doroteja Križan [~ z/ž], a gemžar's widow [~], 39 years (Aug 31, buried Sep 1) — consumption; previdena (written out!); Ant./And. Glibe coop. [~ t/d]; the 140-day gap without a Griblje death closes (Apr 13 → Aug 31)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04894",
    year: 1887,
    scan: 12,
    page: 11,
    whatSi: "umrl Matija Požek [~ — max-zoom: Matija, NE 'Marija Požit'!], ¼ zemljakov sin, 2¾ leta (8. 9., pokop 10. 9.) — Gliste; And. Glibe coop. [~ t/d]",
    whatEn: "died Matija Požek [~ — the max-zoom: Matija, NOT the full-page 'Marija Požit'!], a quarter-farmer's son, 2¾ years (Sep 8, buried Sep 10) — Gliste [~]; And. Glibe coop. [~ t/d]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04894",
    year: 1887,
    scan: 12,
    page: 11,
    whatSi: "umrla Katarina Jakofčič [~ e?], ½ zemlj. hči, 1 leto (27. 9., pokop 29. 9.) — Griža; Andrej Glibel; hiša 13 = Jakopič — 3. otroška smrt na h13 v 2 letih (1886 Ana 1 let. + Nov 1886 krstni Matija + 1887 Katarina!)",
    whatEn: "died Katarina Jakofčič [~ e?], a half-farmer's daughter, 1 year (Sep 27, buried Sep 29) — dysentery; Andrej Glibel; house 13 = the Jakopič — the 3rd child event on h13 within 2 years (1886 Ana 1-y + the Nov 1886 baptism Matija + 1887 Katarina!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04894",
    year: 1887,
    scan: 12,
    page: 11,
    whatSi: "umrl Matija Milek [~ — max-zoom: Matija, NE 'Marija'!], ½ zemljakov sin, 3 leta (29. 10., pokop 31. 10.) — Jetika (= jetika/sušica); Ant./And. Glibe coop. [~ t/d]; rdeča ✓ (revizija); 2. Milek-smrt 1887 (po h65-Marzec!)",
    whatEn: "died Matija Milek [~ — the max-zoom: Matija, NOT 'Marija'!], a half-farmer's son, 3 years (Oct 29, buried Oct 31) — phthisis; Ant./And. Glibe coop. [~ t/d]; a red ✓ (revision); the 2nd Milek death of 1887 (after h65-March!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04894",
    year: 1887,
    scan: 12,
    page: 11,
    whatSi: "umrl Janez Križan [~ z/ž], ½ zemljakov sin, ¼ ure [~ — max-zoom ¼, ne '½ ure'!] (18. 11., pokop 19. 11.) — Slabost; Ant./And. Glibe coop. [~ t/d]; najhitrejša smrt leta (15 minut [~])",
    whatEn: "died Janez Križan [~ z/ž], a half-farmer's son, a QUARTER hour [~ — max-zoom ¼, not '½ hour'!] (Nov 18, buried Nov 19) — weakness; Ant./And. Glibe coop. [~ t/d]; the fastest death of the year (15 minutes [~])",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04894",
    year: 1887,
    scan: 13,
    page: 12,
    whatSi: "umrl Marko Požek [~], ženjen ¼ zemlj. Holar [~ Kolar?], 66 let (6. 12., pokop 8. 12.) — Mertvod [~ Mertvud/Mestruod — NOV VZROK!]; prejel sv. posl. olje (poslednje maziljenje — 1. izpisani sakrament mrliške linije!); Jos. Romej; ★ max-zoom hiša = 58 (celostanska '53' NAPAČNA!)",
    whatEn: "died Marko Požek [~], a married quarter-farmer holar [~], 66 years (Dec 6, buried Dec 8) — Mertvod [~ — a NEW cause!]; received the holy last oil (the extreme unction — the 1st written-out sacrament of the death line!); Jos. Romej; ★ the max-zoom house = 58 (the full-page '53' WRONG!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "43",
    bookSignature: "04894",
    year: 1887,
    scan: 13,
    page: 12,
    whatSi: "umrl Matija Lašič [~ — 'sin' = moški; priimek tudi 'Šašič' [~]], ½ zemlj. sin, 3 leta (28. 12., pokop 30. 12.) — Sušica; Ant./And. Glibe coop. [~ t/d]; rdeča ✓; ZADNJI gribeljski vpis 1887",
    whatEn: "died Matija Lašič [~ — 'sin' = male; the surname also 'Šašič' [~]], a half-farmer's son, 3 years (Dec 28, buried Dec 30) — consumption; Ant./And. Glibe coop. [~ t/d]; a red ✓; the LAST Griblje entry of 1887",
    status: "DOCUMENTED",
  },
// ——— P154: MRLIŠKA KNJIGA 04894 — leto 1888 = 3. polno leto mrliške linije = REKORDNO leto ———
// 29 Griblje-vpisov / 102 vrstic (13 → 13 → 29 = ×2.2!) — s13-dno (r1–5) + s14–s21 (r6–r102);
// meja 1889 = »1 8 8 9« na s21 (9 z dolgim repom — forenzično!); glave s14–s21 IZPISANE (»Leto 18ſſ..«);
// ★★ 2 porodni smrti (r6 h72 'Na porodu' + r23 h83 'Vsled těžkega poroda') · ★★ Željko/Želičo 4 otroci ·
// ★★ h61 Požek ×3 · ★ h83 NOVA p80-hiša + h47 · ★ 'Starost' kot vzrok (r102, 80 let!) · podpisi-kolaps (8/29);
// dokaz: research/issue17/parish-death-1888.json (13 izključenih skupin + 12 anomalij + 10 križnih)
  {
    houseNo: "72",
    bookSignature: "04894",
    year: 1888,
    scan: 13,
    page: 12,
    whatSi: "umrla Marija Straus [~ Štraus], ½ zemlj. hči, 1 DAN (31. 1., pokop 2. 2.) — Slabost; And. Glibe coop. (P153-lead forenzika — 1. gribeljski vpis 1888; h72 = ŠTRAVS poročne 1921-№22!)",
    whatEn: "died Marija Straus [~], a half-farmer's daughter, 1 DAY old (Jan 31, buried Feb 2) — weakness; And. Glibe coop. (the P153-lead forensics — the 1st Griblje entry of 1888; h72 = the ŠTRAVS marriage 1921 №22!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04894",
    year: 1888,
    scan: 14,
    page: 13,
    whatSi: "umrla Barbara Strauš [~], omgena [~] ½ žemljakinja, 22 let (3. 2., pokop 5. 2.) — NA PORODU (= porodna smrt!); And. Glibe coop.; ★★ h72 DRAMA ×2: mati Barbara (22) umrla na porodu 3 dni po hči Mariji (1 dan, 31. 1.) — novorojenček + mati v 4 dneh!",
    whatEn: "died Barbara Strauš [~], a [~] half-smallholder woman, 22 years (Feb 3, buried Feb 5) — IN CHILDBIRTH (= a maternal death!); And. Glibe coop.; ★★ the h72 DRAMA ×2: mother Barbara (22) died in childbirth 3 days after her daughter Marija (1 day, Jan 31) — the newborn + the mother within 4 days!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04894",
    year: 1888,
    scan: 14,
    page: 13,
    whatSi: "umrla Katarina Požek [~ — celostanska 'Poreht' NAPAČNA, max-zoom jasno PožeK!], ¼ žemlj. hči, 10 mesecev (11. 2., pokop 13. 2.) — Božjast; And. Glibe coop.",
    whatEn: "died Katarina Požek [~ — the full-page 'Poreht' WRONG, the max-zoom clearly PožeK!], a quarter-smallholder's daughter, 10 months (Feb 11, buried Feb 13) — cramps; And. Glibe coop.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04894",
    year: 1888,
    scan: 14,
    page: 13,
    whatSi: "umrla Marija Požek [~ — celostanska 'Požeš' popravljena], ½ žemljatka hči, 3 leta (15. 2., pokop 17. 2.) — Išiste [~ — neberljivo, 2. VLM 'Iliste']; And. Glibe coop.; ★ h61 DRAMA: dve hči Požekovih (10 mesecev + 3 leta) v 4 dneh!",
    whatEn: "died Marija Požek [~ — the full-page 'Požeš' corrected], a half-smallholderess's daughter, 3 years (Feb 15, buried Feb 17) — Išiste [~ — illegible]; And. Glibe coop.; ★ the h61 DRAMA: two Požek daughters (10 months + 3 years) within 4 days!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04894",
    year: 1888,
    scan: 14,
    page: 13,
    whatSi: "umrl Matija Križan [~ Hrižan — Kurrent varianta], ½ žemlj. sin, 3 leta (26. 2., pokop 28. 2.) — Angina; And. Glibe coop.",
    whatEn: "died Matija Križan [~ Hrižan — the Kurrent variant], a half-farmer's son, 3 years (Feb 26, buried Feb 28) — angina; And. Glibe coop.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04894",
    year: 1888,
    scan: 14,
    page: 13,
    whatSi: "umrla Marija Brinec [~ — celostanska 'Brune' NAPAČNA!], ½ žemljat. hči, 5 DNI (4. 3., pokop 5. 3.) — Slabost; And. Glibe coop.",
    whatEn: "died Marija Brinec [~ — the full-page 'Brune' WRONG!], a half-smallholder's daughter, 5 DAYS (Mar 4, buried Mar 5) — weakness; And. Glibe coop.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04894",
    year: 1888,
    scan: 15,
    page: 14,
    whatSi: "umrl Janez Perdinec [~ — celostanska 'Simon Pozdinec h88' = ×2 NAPAČNA! max-zoom: Janez Perdinec h53!], vdovec in kolar, 75 let (3. 4., pokop 5. 4.) — Nadluka; previden (1); BREZ PODPISA; h53 = P153-1887 (Marija Šimec 62!) + P155-1889-lead (Ana Perdihec 67 Mertvod [~]!) — PERDINEC-mreža!",
    whatEn: "died Janez Perdinec [~ — the full-page 'Simon Pozdinec h88' DOUBLY WRONG! the max-zoom: Janez Perdinec h53!], a widower and wheelwright, 75 years (Apr 3, buried Apr 5) — diphtheria; received the sacraments (1); NO SIGNATURE; h53 = P153-1887 (Marija Šimec 62!) + the P155-1889-lead (Ana Perdihec 67 Mertvod [~]!) — the PERDINEC network!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04894",
    year: 1888,
    scan: 15,
    page: 14,
    whatSi: "umrla Katarina Milek [~ — VLM 'Štriten/Mulek' zavrnjena], ½ žeml'atovs hči, 9 let (9. 4., pokop 11. 4.) — Bule [~ — neberljivo, 'Ruda?']; BREZ PODPISA; h65 = P153-1887 (Mihael Milek 49, Marec!) — Milek-hiša 2. leto zapored!",
    whatEn: "died Katarina Milek [~ — the VLM 'Štriten/Mulek' rejected], a half-smallholder's daughter, 9 years (Apr 9, buried Apr 11) — Bule [~ — illegible]; NO SIGNATURE; h65 = P153-1887 (Mihael Milek 49, March!) — the Milek house 2 years running!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04894",
    year: 1888,
    scan: 15,
    page: 14,
    whatSi: "umrla Marija Brinec [~], omgjena [~] ¼ žemlj. žena, 63 let [~ — Kurrent 3/9!] (16. 4., pokop 18. 4.) — Pljučnica [~ Pljuunica]; previdna (1); BREZ PODPISA; h26 = BRINEC-hiša (poročna 1887 №4!) — 2. Brinec smrt 1888 (r82 h24!)",
    whatEn: "died Marija Brinec [~], a [~] quarter-farmer's wife, 63 years [~ — the Kurrent 3/9!] (Apr 16, buried Apr 18) — pneumonia [~]; received the sacraments (1); NO SIGNATURE; h26 = the BRINEC house (marriage 1887 №4!) — the 2nd Brinec death of 1888 (r82 h24!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "83",
    bookSignature: "04894",
    year: 1888,
    scan: 15,
    page: 14,
    whatSi: "umrla Marija Radovič [~], krajčeva hči [~ krojačeva; 3. vrstica 'o viši' neberljiva [?]], starost NEIZPISANA (— [?]) (18. 4., pokop 19. 4.) — VSLED TĚŽKEGA PORODA (= po težkem porodu — 2. porodna smrt leta!); BREZ PODPISA; ★★ NOVA HIŠA h83 (max-zoom potrdila 83, ne 68/88!) = p80-hiša #78",
    whatEn: "died Marija Radovič [~], a tailor's daughter [~; the 3rd line illegible [?]], age NOT WRITTEN (— [?]) (Apr 18, buried Apr 19) — AFTER A DIFFICULT CHILDBIRTH (= the 2nd maternal death of the year!); NO SIGNATURE; ★★ A NEW HOUSE h83 (the max-zoom confirmed 83, not 68/88!) = the p80-house #78",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04894",
    year: 1888,
    scan: 15,
    page: 14,
    whatSi: "umrla Barbara Požek [~ — celostanska 'Povelt' NAPAČNA!], 24 let (19. 4., pokop 21. 4.) — Jetika; previdna (1); BREZ PODPISA; ★★ h61 = 3. SMRT na isti hiši 1888 (r7 Katarina 10-mes + r10 Marija 3-let Februar + Barbara 24 April) = POŽEK-TRAGEDIJA h61!",
    whatEn: "died Barbara Požek [~ — the full-page 'Povelt' WRONG!], 24 years (Apr 19, buried Apr 21) — Jetika (dropsy); received the sacraments (1); NO SIGNATURE; ★★ h61 = the 3rd DEATH at the same house of 1888 (r7 Katarina 10-mo + r10 Marija 3-yr February + Barbara 24 April) = the POŽEK TRAGEDY of h61!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04894",
    year: 1888,
    scan: 16,
    page: 15,
    whatSi: "umrl Matija Želičo [~ — Kurrent 'Žefičo/Željko'; 1. od 4 Želičo/Željko-smrti 1888!], ½ žemljatov sin, 3 leta (23. 5., pokop 24. 5.) — Vrhjatinka [~ — neberljiv ljudski izraz, paralela Strgjatinka!]; BREZ PODPISA",
    whatEn: "died Matija Želičo [~ — the Kurrent 'Žefičo/Željko'; the 1st of 4 Želičo/Željko deaths of 1888!], a half-smallholder's son, 3 years (May 23, buried May 24) — Vrhjatinka [~ — an illegible folk term, parallel to Strgjatinka!]; NO SIGNATURE",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04894",
    year: 1888,
    scan: 16,
    page: 15,
    whatSi: "umrla Marija Jakobčič [~], ½ žemljatova hči, 5½ let (8. 6., pokop 8./9. 6.) — Strgjatinka [~ — nerazrešen ljudski izraz, 1. od 3!]; BREZ PODPISA; h13 = P153 'Jakopič 3 dogodka v 2 letih' hiša — 4. dogodek!",
    whatEn: "died Marija Jakobčič [~], a half-smallholder's daughter, 5½ years (Jun 8, buried Jun 8/9) — Strgjatinka [~ — an unresolved folk term, the 1st of 3!]; NO SIGNATURE; h13 = the P153 'Jakopič 3-events-in-2-years' house — the 4th event!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04894",
    year: 1888,
    scan: 16,
    page: 15,
    whatSi: "umrl Nikolaj Požek [~ Požett/Povelt — Kurrent zmeda], ½ žemljatov sin, 6 mesecev (10. 6., pokop 11. 6.) — Sušica; BREZ PODPISA; h21 = P153-1887 (Matija Požek 2¾!) — Požek-hiša 2. leto!",
    whatEn: "died Nikolaj Požek [~ Požett/Povelt — the Kurrent confusion], a half-smallholder's son, 6 months (Jun 10, buried Jun 11) — consumption; NO SIGNATURE; h21 = P153-1887 (Matija Požek 2¾!) — the Požek house 2 years running!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04894",
    year: 1888,
    scan: 18,
    page: 17,
    whatSi: "umrl Janez Klepec, ½ žemlj. sin, 1 mesec (27. 7., pokop 28. 7.) — Davica; BREZ PODPISA; ★ max-zoom hiša = 25 (5-forma identična s59-'35'; 6 ima visok ovinek!) — celostanska '26' zavrnjena; h25 [~ — Kurrent 5/6]",
    whatEn: "died Janez Klepec, a half-farmer's son, 1 month (Jul 27, buried Jul 28) — croup; NO SIGNATURE; ★ the max-zoom house = 25 (the 5-form identical to s59-'35'; the 6 has a tall loop!) — the full-page '26' rejected; h25 [~ — the Kurrent 5/6]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04894",
    year: 1888,
    scan: 18,
    page: 17,
    whatSi: "umrla Doroteja Želičo [~ Željko], ½ žemlj. hči, 14 let (10. 8., pokop 12. 8.) — Strgjatinka [~]; BREZ PODPISA; ★★ h60 ŽELIČO/ŽELJKO-TRAGEDIJA 1/2: 6 dni pred sestro Barbaro (r66, 3 let) — isti vzrok!",
    whatEn: "died Doroteja Želičo [~ Željko], a half-farmer's daughter, 14 years (Aug 10, buried Aug 12) — Strgjatinka [~]; NO SIGNATURE; ★★ the h60 ŽELIČO/ŽELJKO-TRAGEDY 1/2: 6 days before her sister Barbara (r66, 3 years) — the same cause!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04894",
    year: 1888,
    scan: 18,
    page: 17,
    whatSi: "umrla Barbara Želičo [~ Žefiko/Željko], ½ žemlj. hči, 3 let (16. 8., pokop 18. 8.) — Strgjatinka [~ — celostanska 'Marbmila/Grižatnica' zavrnjeni!]; BREZ PODPISA; ★★ h60 ŽELIČO/ŽELJKO-TRAGEDIJA 2/2: sestra Doroteje (14) — obe 'Strgjatinka' v 6 dneh!",
    whatEn: "died Barbara Želičo [~ Žefiko/Željko], a half-farmer's daughter, 3 years (Aug 16, buried Aug 18) — Strgjatinka [~ — the full-page 'Marbmila/Grižatnica' rejected!]; NO SIGNATURE; ★★ the h60 ŽELIČO/ŽELJKO-TRAGEDY 2/2: Doroteja's (14) sister — both 'Strgjatinka' within 6 days!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04894",
    year: 1888,
    scan: 18,
    page: 17,
    whatSi: "umrl Anton Željko [~], ½ žemlj. sin, 4 mesece [~] (20. 8., pokop 22. 8.) — Davica; BREZ PODPISA; ★★ ŽELIČO/ŽELJKO = 4 MRTVIH OTROK 1888 na dveh hišah (h1: Matija 3-let maj + Anton 4-mes avg; h60: Doroteja 14 + Barbara 3 avg)!",
    whatEn: "died Anton Željko [~], a half-farmer's son, 4 months [~] (Aug 20, buried Aug 22) — croup; NO SIGNATURE; ★★ ŽELIČO/ŽELJKO = 4 DEAD CHILDREN of 1888 at two houses (h1: Matija 3-yr May + Anton 4-mo Aug; h60: Doroteja 14 + Barbara 3 Aug)!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "47",
    bookSignature: "04894",
    year: 1888,
    scan: 19,
    page: 18,
    whatSi: "umrla Marija Klobučar [~], ½ žemlj. hči, 3 leta (26. 8., pokop 27. 8.) — Davica; Jos. Romey; ★ NOVA p80-HIŠA h47 (P153-1887: Katarina Klobučar h46, 74 — sosednja hiša! Klobučar-mreža ×2 zaporedni leti!)",
    whatEn: "died Marija Klobučar [~], a half-farmer's daughter, 3 years (Aug 26, buried Aug 27) — croup; Jos. Romey; ★ A NEW p80-HOUSE h47 (P153-1887: Katarina Klobučar h46, 74 — the neighbouring house! The Klobučar network ×2 consecutive years!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04894",
    year: 1888,
    scan: 19,
    page: 18,
    whatSi: "umrl Matija Križan [~ Hrižan], ½ žemlj. sin, 2 leti (29. 8., pokop 30. 8.) — Difteritis [~ Diſenteritis — dolgi-s zmeda!]; Jos. Romey; h26 = 2. smrt hiše 1888 (r22 Marija Brinec 63, April!)",
    whatEn: "died Matija Križan [~ Hrižan], a half-farmer's son, 2 years (Aug 29, buried Aug 30) — Difteritis [~ Diſenteritis — the long-s confusion!]; Jos. Romey; h26 = the house's 2nd death of 1888 (r22 Marija Brinec 63, April!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04894",
    year: 1888,
    scan: 19,
    page: 18,
    whatSi: "umrla Ana Križan [~ Hrižan], ½ žemlj. hči, 4 leta [~ — celostanska '9' popravljena po R-alignment!] (8. 9., pokop 9. 9.) — Gliste; BREZ PODPISA; h36 = P153-1887 (Šimec-Ana sidro!) + P115-1886 (Pegdirc-ženin!) — 3-virska hiša",
    whatEn: "died Ana Križan [~ Hrižan], a half-farmer's daughter, 4 years [~ — the full-page '9' corrected by R-alignment!] (Sep 8, buried Sep 9) — Gliste (worms); NO SIGNATURE; h36 = P153-1887 (the Šimec-Ana anchor!) + P115-1886 (the Pegdirc-groom!) — a 3-source house",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04894",
    year: 1888,
    scan: 19,
    page: 18,
    whatSi: "umrla Barbara Brinec, ½ žemljatova hči, 16 let (13. 9., pokop 15. 9.) — Pljučnica [~]; Andrej Glibe coop. (POLNI podpis 'Andrej' — potrditev And.-kratic!); h24 = BRINEC-mreža (r15 h69 + r22 h26 = 3 Brinec-smrti 1888!)",
    whatEn: "died Barbara Brinec, a half-smallholder's daughter, 16 years (Sep 13, buried Sep 15) — pneumonia [~]; Andrej Glibe coop. (the FULL signature 'Andrej' — a confirmation of the And. abbreviations!); h24 = the BRINEC network (r15 h69 + r22 h26 = 3 Brinec deaths of 1888!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04894",
    year: 1888,
    scan: 20,
    page: 19,
    whatSi: "umrl Matija Hlusič [~ — celostanska 'Marija Mušič' = ×2 NAPAČNA! max-zoom: Matija Hlusič!], ¼ žemljatov sin, 3½ leta (22. 9., pokop 24. 9.) — Difteritis (JASNA forma — dihtagija!); BREZ PODPISA",
    whatEn: "died Matija Hlusič [~ — the full-page 'Marija Mušič' DOUBLY WRONG! the max-zoom: Matija Hlusič!], a quarter-smallholder's son, 3½ years (Sep 22, buried Sep 24) — Difteritis (a CLEAR form — diphtheria!); NO SIGNATURE",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04894",
    year: 1888,
    scan: 20,
    page: 19,
    whatSi: "umrl Jožef Totter [~ Fotter — P150-№27-vez!], ½ žemlj. sin, 5 let (11. 10., pokop 12. 10.) — Vodernica; BREZ PODPISA; h7 = poročna 1921-№27-hiša (Fotter-ženin!) — TOTTER/FOTTER čez 33 leta!",
    whatEn: "died Jožef Totter [~ Fotter — the P150-№27 link!], a half-farmer's son, 5 years (Oct 11, buried Oct 12) — Vodernica (dropsy); NO SIGNATURE; h7 = the marriage-1921-№27 house (the Fotter groom!) — TOTTER/FOTTER across 33 years!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04894",
    year: 1888,
    scan: 20,
    page: 19,
    whatSi: "umrl Martin Jakobčič [~], ½ žemljatov sin, 1 URO (20. 10., pokop 22. 10.) — Difteritis in slabost — v sih Kruščen [? — 2. del neberljiv, morebiti nem. 'Krämpfen' = krči!] = NAJKRAJŠA ŽIVLJENJSKA DOBA 1888 + nerazrešen vzrok; BREZ PODPISA",
    whatEn: "died Martin Jakobčič [~], a half-smallholder's son, 1 HOUR old (Oct 20, buried Oct 22) — Difteritis and weakness — v sih Kruščen [? — the 2nd part illegible, possibly the German 'Krämpfen' = convulsions!] = the SHORTEST LIFESPAN of 1888 + an unresolved cause; NO SIGNATURE",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04894",
    year: 1888,
    scan: 21,
    page: 20,
    whatSi: "umrl Mihael Jakobčič [~], ½ žemlj. kolar, vdovec, 68 let [~ — VLM '65' zavrnjeno!] (18. 11., pokop 20. 11.) — Nadluka; previden (1); BREZ PODPISA; ★ h8 DRAMA ×2: 29 dni po Martinu (r89, 1 ura!) — oče/syn? dedek? (kolar-vdovec)",
    whatEn: "died Mihael Jakobčič [~], a half-farmer wheelwright, a widower, 68 years [~ — the VLM '65' rejected!] (Nov 18, buried Nov 20) — Nadluka (diphtheria); received the sacraments (1); NO SIGNATURE; ★ the h8 DRAMA ×2: 29 days after Martin (r89, 1 hour!) — father/son? grandfather? (a widower wheelwright)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04894",
    year: 1888,
    scan: 21,
    page: 20,
    whatSi: "umrla Ana Križan [~ Hrižan], ¼ žemljaNova hči, 8 let [~ — VLM '3' zavrnjeno!] (24. 11., pokop 26. 11.) — Pljučnica; BREZ PODPISA; h35 = 2. smrt hiše 1888 (r13 Matija 3-let, Februar!) — KRIŽAN-hiša ×2!",
    whatEn: "died Ana Križan [~ Hrižan], a quarter-smallholder's daughter, 8 years [~ — the VLM '3' rejected!] (Nov 24, buried Nov 26) — pneumonia; NO SIGNATURE; h35 = the house's 2nd death of 1888 (r13 Matija 3-yr, February!) — the KRIŽAN house ×2!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04894",
    year: 1888,
    scan: 21,
    page: 20,
    whatSi: "umrla Marija Požek [~ — celostanska 'Povelt' zavrnjena!], omgina [~] ¼ žemljatinja, 38 let [~ — celostanska '2½' zavrnjena!] (26. 11., pokop 28. 11.) — Vodernica; previdna (1); BREZ PODPISA; h21 = 2. smrt hiše 1888 (r44 Nikolaj 6-mes, Junij!) + P153-1887 (Matija 2¾) — Požek ×3 čez 2 leti!",
    whatEn: "died Marija Požek [~ — the full-page 'Povelt' rejected!], a [~] quarter-smallholderess, 38 years [~ — the full-page '2½' rejected!] (Nov 26, buried Nov 28) — Vodernica (dropsy); received the sacraments (1); NO SIGNATURE; h21 = the house's 2nd death of 1888 (r44 Nikolaj 6-mo, June!) + P153-1887 (Matija 2¾) — Požek ×3 across 2 years!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04894",
    year: 1888,
    scan: 21,
    page: 20,
    whatSi: "umrl Peter Križan [~ Hrižan], ½ žemlj. kolar in vdovec, 80 let (25. 12., pokop 27. 12.) — STAROST (= starostni vohun — 1. 'starost' kot vzrok mrliške linije!); previden (1); BREZ PODPISA; ZADNJI gribeljski vpis 1888; h3 = P153-1887 (Doroteja 39!) — Križan-hiša ×2; 5 dni pred koncem leta",
    whatEn: "died Peter Križan [~ Hrižan], a half-farmer wheelwright and widower, 80 years (Dec 25, buried Dec 27) — OLD AGE (= the 1st 'old age' cause of the death line!); received the sacraments (1); NO SIGNATURE; the LAST Griblje entry of 1888; h3 = P153-1887 (Doroteja 39!) — the Križan house ×2; 5 days before the year's end",
    status: "DOCUMENTED",
  },
  // ——— P155: MRLIŠKA KNJIGA 04894 — leto 1889 = 4. polno leto mrliške linije = NAJNIŽE leto ———
  // 8 Griblje-vpisov / 36 vrstic (13 → 13 → 29 → 8 = povratek na dno!) — s21-dno (r1–6) + s22–s24 (r7–r36);
  // meja 1890 = INLINE »1890.« v mesec-stolpcu restartne vrstice na s24 (3. stil meje!); glave s22–s24 izpisane;
  // ★★★ 92-letni REKORD linije (r27 h55 Peter Šimec kolar!) + ★★★ 2 krstna↔mrliška vezi dojenčkov (h69 Janez 16 dni
  // + h65 Barbara 13 dni — SKLAD NA DAN!) + ★★ h83 sib-swap (†31.10. → krst nov.!) + ★★ P154-lead-popravek 67→49
  // (marker-9 forenzika!) + ★ ¼ ure (izenačen rekord!) + 0 novih p80-hiš (h30/h48/h55 = 1. mrliški vpisi!);
  // dokaz: research/issue17/parish-death-1889.json (10 izključenih skupin + 8 anomalij + 10 križnih)
  {
    houseNo: "53",
    bookSignature: "04894",
    year: 1889,
    scan: 21,
    page: 20,
    whatSi: "umrla Ana Perdihec [~ Perdirec — cf. cluster Perdinec/Pendirec/Pozdirec/Pegdirec/Perdivec!], omgina [~] ¼ žemlj., 49 let [~ — ★★★ P154-LEAD-POPRAVEK: provizorna 67 → max-zoom 8×: 49 (4-forma + 9-forma z dolgim repom; VLM 47 TUDI napačen — VLM bere 9 kot 7!); marker-9 referenca!] (25. 1., pokop 27. 1.) — Mertvod [~]; 'sv. olje' [~] izpisano v previden-stolpcu (= poslednje maziljenje — 2. izpisani sakrament linije!); BREZ PODPISA; P155-LEAD (P154-napovedan!); h53 = 3. smrt v 3. letih (1887 Marija Šimec 62 + 1888 Janez Perdinec + 1889 Ana!)",
    whatEn: "died Ana Perdihec [~ Perdirec — cf. the Perdinec/Pendirec/Pozdirec/Pegdirec/Perdivec cluster!], a [~] widow of a quarter-smallholder, 49 years [~ — ★★★ THE P154-LEAD CORRECTION: the provisional 67 → the max-zoom 8×: 49 (the 4-form + the 9-form with a long tail; the VLM's 47 ALSO wrong — the VLM reads 9 as 7!); the marker-9 reference!] (Jan 25, buried Jan 27) — Mertvod [~ childbed fever?]; 'holy oil' [~] written in the sacraments column (= the last rites — the 2nd WRITTEN sacrament of the line!); NO SIGNATURE; the P155-LEAD (announced by P154!); h53 = the 3rd death in 3 consecutive years (1887 Marija Šimec 62 + 1888 Janez Perdinec + 1889 Ana!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04894",
    year: 1889,
    scan: 22,
    page: 21,
    whatSi: "umrl Janez Brinec, ½ žemljaškov sin, 16 DNI (16. 4., pokop 17. 4.) — Božjast; brez oznake; BREZ PODPISA; ★★★ KRSTNA↔MRLIŠKA VEZ #1 mrliške linije: krstna 04105-1889 h69 Janez 1./2. 4. (oče Janez Brinec × mati Barbara Strauš) → † 16./17. 4. = ISTI OTROK — SKLAD NA DAN!; h69 = Brinec-hiša (1886 vdova Podec + 1888 Marija 5 dni + poročna 1887 + krsti 1888–1895 — isti oče Janez ×5!)",
    whatEn: "died Janez Brinec, a half-farmer's son, 16 DAYS old (Apr 16, buried Apr 17) — cramps; no mark; NO SIGNATURE; ★★★ THE BAPTISM↔DEATH LINK #1 of the death line: the baptism register 04105-1889 h69 Janez born Apr 1/2 (father Janez Brinec × mother Barbara Strauš) → died Apr 16/17 = THE SAME CHILD — agreement to the day!; h69 = the Brinec house (1886 the widow Podec + 1888 Marija 5 days + the 1887 marriage + the baptisms 1888–1895 — the same father Janez ×5!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04894",
    year: 1889,
    scan: 22,
    page: 21,
    whatSi: "umrla Marija Milek [~ Mileš], omgjena [~] ½ žemljatkinja, 66 let (16. 6., pokop 17. 6.) — Pljučnica; previdna (1); BREZ PODPISA; h30 = 1. MRLIŠKI vpis hiše 30 (poročna 1889 №8 ženin Johann MILEK 60 LET, GRIBLJE 30 — poroka 14. 10. 1889, 4 meseci PO tej smrti! + krstna 1890 dvojčka oče Janez Milek × mati Marjeta Pendirec [~]!) — Milek-mreža h30/65/22!",
    whatEn: "died Marija Milek [~ Mileš], a [~] married half-smallholderess, 66 years (Jun 16, buried Jun 17) — pneumonia; received the sacraments (1); NO SIGNATURE; h30 = the 1st DEATH entry of house 30 (the marriage 1889 №8 groom Johann MILEK, 60 YEARS OLD, GRIBLJE 30 — married Oct 14, 1889, 4 months AFTER this death! + the baptism 1890 twins father Janez Milek × mother Marjeta Pendirec [~]!) — the Milek network h30/65/22!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "55",
    bookSignature: "04894",
    year: 1889,
    scan: 23,
    page: 22,
    whatSi: "umrl Peter Šimec, ½ žemlj. in KOLAR (2. kolar linije za 1888-r102 Križan h3!), 92 LET (26. 10., pokop 28. 10.) — Vodenica; previden (1); Andrej Glibe (POLNI PODPIS!); ★★★ REKORD LINIJE: najstarejši človek 04894 (prej 80-P154-r102 / 78-P154-r99 / 74-P153!) + ★★ hiša 55 FORENZIKA: 8× = DVE ISTI 5-formi (ne 53/58! — cf. r4-h53 5+3!); 1. mrliški vpis h55 (krstna 1890: 'Šimec zdaj tudi na luknji 55' — ŠIMEC-VEZ!); VLM '72' ZAVRJEN (9-as-7!)",
    whatEn: "died Peter Šimec, a half-smallholder AND WHEELWRIGHT (the 2nd wheelwright of the line after 1888-r102 Križan h3!), 92 YEARS old (Oct 26, buried Oct 28) — dropsy; received the sacraments (1); Andrej Glibe (the FULL SIGNATURE!); ★★★ THE LINE RECORD: the oldest person of 04894 (the previous 80-P154-r102 / 78-P154-r99 / 74-P153!) + ★★ house 55 FORENSICS: 8× = TWO IDENTICAL 5-forms (not 53/58! — cf. r4-h53 5+3!); the 1st death entry of h55 (the baptism 1890: 'Šimec now also on the gap-house 55' — the ŠIMEC link!); the VLM '72' REJECTED (the 9-as-7 error!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "83",
    bookSignature: "04894",
    year: 1889,
    scan: 23,
    page: 22,
    whatSi: "umrla Barbara Radovič, hčimika? [?] in čevljarjeva? [~] hiči (stan delno neberljiv!), ¼ URE (31. 10., pokop 1. 11. — pokop z mesecem 'Nov.'!) — Slabost; brez oznake (—); Antn. Glibe; ★★ ¼ URE = IZENAČEN najkrajši rekord linije (P153-r35!; VLM '4 ure' ZAVRJEN — ulomek 1/4 forenzično!) + ★★ h83 SIB-SWAP: † Barbara (31. 10.) → krstna-1889 Barbara (nov.) = IMENSKA NASLEDNICA v istem mesecu!; h83 = 2. smrt hiše (1888 r23 Marija 'Vsled těžkega poroda'!)",
    whatEn: "died Barbara Radovič, a [?] little-daughter? in the shoemaker's? [~] house (the status partly illegible!), ¼ of an HOUR (Oct 31, buried Nov 1 — the burial with the month 'Nov.'!) — weakness; no mark (—); Antn. Glibe; ★★ ¼ HOUR = TIED for the shortest lifespan of the line (P153-r35!; the VLM '4 hours' REJECTED — the 1/4 fraction forensically!) + ★★ h83 SIB-SWAP: † Barbara (Oct 31) → the baptism-1889 Barbara (Nov.) = THE NAMESAKE SUCCESSOR in the same month!; h83 = the house's 2nd death (1888 r23 Marija 'after a difficult childbirth'!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04894",
    year: 1889,
    scan: 23,
    page: 22,
    whatSi: "umrla Katarina Strauciž [~ Straucif/Strucelj — konec neberljiv, 3 branja! — paralela Strauš-clusteru h69/h72], samska [~] ½ žemlj. hiči [~ hči], 58 let (20. 11., pokop 22. 11.) — Vodenica; previdna (1); Jos. Romey [~ Rauq]; ★ hiša 5 FORENZIKA: 7× = ena 5-forma + pika = h5 (ne 6/65!); h5 že v mrliškem 1886 (Barbara Brinec 2 leti) + krstna 1891–1919 (Torec/Štrucelj!)",
    whatEn: "died Katarina Strauciž [~ Straucif/Strucelj — the surname ending illegible, 3 readings! — a parallel to the Strauš cluster of h69/h72], single [~], of the half-farm house [~ daughter], 58 years (Nov 20, buried Nov 22) — dropsy; received the sacraments (1); Jos. Romey [~ Rauq]; ★ house 5 FORENSICS: 7× = a single 5-form + a period = h5 (not 6/65!); h5 already in the 1886 death register (Barbara Brinec, 2 years) + the baptisms 1891–1919 (Torec/Štrucelj!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04894",
    year: 1889,
    scan: 23,
    page: 22,
    whatSi: "umrla Barbara Milek [~ Mileš], ½ žemljaškova hiči, 13 DNI (6. 12., pokop 7. 12.) — Gliste; brez oznake (—); Jos. Romey [~ Rauq]; ★★★ KRSTNA↔MRLIŠKA VEZ #2: krstna 04105-1889 h65 Barbara 23. 11. (oče Matija Milek) → † 6./7. 12. = ISTA OTROK — SKLAD NA DAN! + ★★ HIŠA-FORENZIKA: max-zoom '65.' (začetna branja '68' NAPAČNA!); h65 = Milek-hiša (1887 Mihael 49 + 1888 Katarina 9 + poročna 1903 MÜCK [~ Milek]!)",
    whatEn: "died Barbara Milek [~ Mileš], of the half-farmer's house, 13 DAYS old (Dec 6, buried Dec 7) — worms; no mark (—); Jos. Romey [~ Rauq]; ★★★ THE BAPTISM↔DEATH LINK #2: the baptism register 04105-1889 h65 Barbara baptized Nov 23 (father Matija Milek) → died Dec 6/7 = THE SAME CHILD — agreement to the day! + ★★ HOUSE FORENSICS: the max-zoom '65.' (the initial readings '68' WRONG!); h65 = the Milek house (1887 Mihael 49 + 1888 Katarina 9 + the 1903 marriage MÜCK [~ Milek]!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04894",
    year: 1889,
    scan: 24,
    page: 23,
    whatSi: "umrl Jurij Klobučar (č jasno — 3×!), ½ žemljaškov sin, 30 let (7. 12., pokop 9. 12.) — Jetika; previden (1); Jos. Romey [~ Rauq]; ZADNJI gribeljski vpis 1889 (meja 1890 v isti strani!); ★ hiša 48 FORENZIKA: 8× = 4-forma + pravi 8 (nasprotje 5-formi r27!) = h48 — 1. MRLIŠKI vpis h48 (poročna 1898 Anna KLOBUČAR + krstna 1898 mati Katarina Klobučar + Klobučar-soseda h46-1887!)",
    whatEn: "died Jurij Klobučar (the č clear — 3×!), a half-farmer's son, 30 years (Dec 7, buried Dec 9) — diphtheria; received the sacraments (1); Jos. Romey [~ Rauq]; the LAST Griblje entry of 1889 (the 1890 boundary on the very same page!); ★ house 48 FORENSICS: 8× = the 4-form + a true 8 (contrasting the 5-forms of r27!) = h48 — the 1st DEATH entry of h48 (the 1898 marriage Anna KLOBUČAR + the 1898 baptism mother Katarina Klobučar + the Klobučar-neighbour h46-1887!)",
    status: "DOCUMENTED",
  },
  // ——— P156: MRLIŠKA KNJIGA 04894 — leto 1890 = 5. polno leto mrliške linije (55 vrstic / 15 Griblje-vpisov / 14 hiš;
  // meja 1890/91 = velik podčrtan »1891« + Januarij na s28 — INLINE-stil, 2 skena prej kot P155-lead-napoved!) ———
  // evidence: research/issue17/parish-death-1890.json — ★★★ učiteljska zamenjava 1890 POTRJENA prek smrti
  // (r8 Klambič-učitelj † jan ↔ krstna-Kopitar-učitelj nov!) + 1. izpisani 'Mrtvorojeno' (r53 — leksikonska referenca)
  // + 1. poklic 'mizarjeva žena' (r32) + NOV duhovnik Šašelj-Adlešiči + STRAUS-mreža ×3 + h30-dvojčki-smrti
  {
    houseNo: "90",
    bookSignature: "04894",
    year: 1890,
    scan: 24,
    page: 23,
    whatSi: "umrl g. Peter Klambič [~], UČITELJ, 20½ let (26. 1., pokop 28. 1.) — Jetika; previden (1.); Jos. Rauq [~ Rauž]; ★★★ 1. STAN 'učitelj' mrliške linije + ★★★ UČITELJSKA ZAMENJAVA 1890 POTRJENA PREK SMRTI: učitelj Klambič † 26. 1. 1890 na ŠOLSKI HIŠI h90 (20½ let — izjemno mlad!) ↔ krstna 04105-1890 h90 (16./17. 11.) oče Franc Kopitar [~] UČITELJ = P155-lead-hipoteza DOKAZANA (Kopitar → Vetrovnik 1898 → Kalan 1908 → Šušteršič 1914!); h90 = 1. MRLIŠKI vpis (krstni 1890–1919 izven p80-filtra) → p80 hiše 81 → 82 = EDINA nova p80-hiša 1890!; LEAD-1890 potrjen",
    whatEn: "died Mr. Peter Klambič [~], a TEACHER, 20½ years (Jan 26, buried Jan 28) — jaundice; received the sacraments (1.); Jos. Rauq [~ Rauž]; ★★★ the 1st 'teacher' STATUS of the death line + ★★★ the TEACHER REPLACEMENT of 1890 PROVEN THROUGH DEATH: teacher Klambič † Jan 26, 1890 at the SCHOOLHOUSE h90 (only 20½!) ↔ the baptism 04105-1890 h90 (Nov 16/17) father Franc Kopitar [~] TEACHER = the P155-lead hypothesis PROVEN (Kopitar → Vetrovnik 1898 → Kalan 1908 → Šušteršič 1914!); h90 = the 1st DEATH entry (baptisms 1890–1919 outside the p80-filter) → p80 houses 81 → 82 = the ONLY new p80-house of 1890!; the LEAD-1890 confirmed",
    status: "DOCUMENTED",
  },
  {
    houseNo: "37",
    bookSignature: "04894",
    year: 1890,
    scan: 25,
    page: 24,
    whatSi: "umrl Jožef Tafrič? [~ Jafrič], ¼ žemlj. sin, 2 URI (5. 2., pokop 6. 2.) — Prezgodnji porod [IZPISANO — 1. v mrliški liniji!]; —; Jos. Rauq; ★ NAJKRAJŠA življenjska doba 1890 (2 uri) + h37 = 1. MRLIŠKI vpis (krstni/poročni 1887–1917 izven mrliške!)",
    whatEn: "died Jožef Tafrič? [~ Jafrič], a quarter-farmer's son, 2 HOURS old (Feb 5, buried Feb 6) — premature birth [SPELLED OUT — the 1st in the death line!]; —; Jos. Rauq; ★ the SHORTEST life of 1890 (2 hours) + h37 = the 1st DEATH entry (baptisms/marriages 1887–1917 outside the death book!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04894",
    year: 1890,
    scan: 25,
    page: 24,
    whatSi: "umrla Katarina Kušlan [~ Kustlan], ¼ žemlj. hči, 2¾ leta (23. 2., pokop 25. 2.) — Božjast [~]; —; Jos. Rauq; ★ h27 = 1. MRLIŠKI vpis (krstna-1887 že + krstna-1890 + poročna 1894 = 3. mesto!); cf. h27-menjava-gospodinjstev Kukar/Stubhar → Pozdirec 1892",
    whatEn: "died Katarina Kušlan [~ Kustlan], a quarter-farmer's daughter, 2¾ years (Feb 23, buried Feb 25) — Božjast [~]; —; Jos. Rauq; ★ h27 = the 1st DEATH entry (the baptisms 1887 + 1890 + the marriage 1894 already!); cf. the h27 household change Kukar/Stubhar → Pozdirec 1892",
    status: "DOCUMENTED",
  },
  {
    houseNo: "42",
    bookSignature: "04894",
    year: 1890,
    scan: 25,
    page: 24,
    whatSi: "umrl Matija Straus, ¼ žemlj. sin, 8 mesecev (27. 2., pokop vpisan '29' [~ 1. 3.?]) — Božjast [~]; —; Jos. Rauq; ★★ STRAUS-MREŽA #2: 1888-h72-Marija-1-DAN (P154-lead!) + 1890-h42-Matija-8-MES + 1890-h71-Marija-8-MES = 3 otroške smrti v 2 letih + poročna 1921-№22!; ★ h42 = NAJZGODNEJŠI vpis (poročna 04455-1894 CERNIČ-hiša prekašana!)",
    whatEn: "died Matija Straus, a quarter-farmer's son, 8 months (Feb 27, burial written '29' [~ Mar 1?]) — Božjast [~]; —; Jos. Rauq; ★★ the STRAUS NETWORK #2: the 1888-h72-Marija-1-DAY (the P154-lead!) + 1890-h42-Matija-8-MONTHS + 1890-h71-Marija-8-MONTHS = 3 child deaths in 2 years + the 1921-№22 marriage!; ★ h42 = the EARLIEST entry (the 1894 marriage — the CERNIČ house — outrun!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04894",
    year: 1890,
    scan: 26,
    page: 25,
    whatSi: "umrla Marija Brinec, ¼ žemlj. hči, 3 leta (7. 5., pokop 9. 5.) — Vodenica; —; ★ C. g. [~ č. g.] Joann ŠAŠELJ, župnik v ADLEŠIČIH — 1. ZUNANJI duhovnik mrliške linije (maj–avg 1890, 2 GRIBLJE-vpisa!); h26 = 3. mrliški vpis (1888×2 + 1890); Brinec-net",
    whatEn: "died Marija Brinec, a quarter-farmer's daughter, 3 years (May 7, buried May 9) — dropsy; —; ★ C. g. [~ č. g.] Joann ŠAŠELJ, the parish priest of ADLEŠIČI — the 1st OUTSIDE priest of the death line (May–Aug 1890, 2 GRIBLJE entries!); h26 = the 3rd death entry (1888×2 + 1890); the Brinec network",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04894",
    year: 1890,
    scan: 26,
    page: 25,
    whatSi: "umrl Matija Milek, ¼ žemlj. sin, 3 DNI (16. 6., pokop 18. 6.) — Slabost; —; Jos. Rauq; ★★ h30 DOJENČKI ×2 v 5 DNEH (r28 + r29 — ISTI vzrok!) = 4. družinski-dvojni-smrti-par linije; h30 = Milek-hiša (1889-1. mrliški + poročna 1902/1909!)",
    whatEn: "died Matija Milek, a quarter-farmer's son, 3 DAYS old (Jun 16, buried Jun 18) — weakness; —; Jos. Rauq; ★★ h30 INFANTS ×2 within 5 DAYS (r28 + r29 — the SAME cause!) = the 4th double-child-death pair of the line; h30 = the Milek house (1889 the 1st death entry + marriages 1902/1909!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04894",
    year: 1890,
    scan: 26,
    page: 25,
    whatSi: "umrl Janez Milek, ¼ žemlj. sin, 9 DNI (21. 6., pokop 23. 6.) — Slabost; —; Jos. Rauq; ★★ h30-DOJENČKI-DVOJČKI-SMRTI #2 (9 dni po Matiji!) — ISTI vzrok, ISTI mesec = epidemija-ga-dojenčka; h30 = EDINA hiša z 2 vpisoma v 1890 (14 hiš — h30 ×2!)",
    whatEn: "died Janez Milek, a quarter-farmer's son, 9 DAYS old (Jun 21, buried Jun 23) — weakness; —; Jos. Rauq; ★★ the h30 INFANT-DOUBLE-DEATH #2 (9 days after Matija!) — the SAME cause, the SAME month = an epidemic-hit-household; h30 = the ONLY house with 2 entries in 1890 (14 houses — h30 ×2!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04894",
    year: 1890,
    scan: 26,
    page: 25,
    whatSi: "umrla Marjeta Požek, MIZARJEVA ŽENA (poklic-status — 1. 'mizar' mrliške linije! cf. P155-r27 KOLAR), 28 let (6. 7., pokop 8. 7.) — Plučnica [~]; previden (1.); Jos. Rauq; ★ max-zoom 'mizarjeva žena' 2×; h7 = 2. mrliški vpis (1888-1.); Požek-net",
    whatEn: "died Marjeta Požek, a CARPENTER'S WIFE (a trade-status — the 1st 'mizar/joiner' of the death line! cf. P155-r27 KOLAR), 28 years (Jul 6, buried Jul 8) — lung-consumption [~]; received the sacraments (1.); Jos. Rauq; ★ max-zoom 'mizarjeva žena' confirmed 2×; h7 = the 2nd death entry (1888 the 1st); the Požek network",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04894",
    year: 1890,
    scan: 26,
    page: 25,
    whatSi: "umrla Marjeta Muc, ¼ žemlj. vdova, 53 let (4. 8., pokop 6. 8.) — Mertvoud [~ NERAZREŠEN — odrasli ×3 (P153-66 + P155-49 + 1890-53) ≠ mrtvorojeno! cf. X6]; —; Jos. Rauq; ★★ h91 = 1. MRLIŠKI vpis (max-zoom '91' jasna!; poročna 04455-1890 27. 1. Johann MUC = 2. familia po krstni-1887!; poročna-1890 že v p80-filtru → 0 sprememb); MUC-mreža (h61-bajtar + krstne-matere ×4)",
    whatEn: "died Marjeta Muc, a quarter-farmer's widow, 53 years (Aug 4, buried Aug 6) — Mertvoud [~ UNRESOLVED — adults ×3 (P153-66 + P155-49 + 1890-53) ≠ stillborn! cf. X6]; —; Jos. Rauq; ★★ h91 = the 1st DEATH entry (max-zoom '91' clear!; the 1890 marriage Jan 27 Johann MUC = the 2nd family after the 1887 baptism!; the marriage-1890 already in the p80-filter → 0 change); the MUC network",
    status: "DOCUMENTED",
  },
  {
    houseNo: "38",
    bookSignature: "04894",
    year: 1890,
    scan: 27,
    page: 26,
    whatSi: "umrl Jurij Šimec [~ Šimek], oženjen bajtar, 48 let (21. 8., pokop 23. 8.) — Plučnica [~]; previden (1.); Šašelj (Adlešiči!); ★ max-zoom hiša '38' NE 58 (3-forma brez f-črte — nasprotje r54-'58' ISTA STRAN = referenčni par Kurrent 3/5!); ★ h38 = 1. MRLIŠKI vpis (poročna 1904 GANSLER prekašana!); ★ ŠIMEC-net: 1889-h55-Peter-92-REKORD + 1890-h38-Jurij-48; 2. ŠAŠELJ-Griblje!",
    whatEn: "died Jurij Šimec [~ Šimek], a married cottager, 48 years (Aug 21, buried Aug 23) — lung-consumption [~]; received the sacraments (1.); Šašelj (Adlešiči!); ★ max-zoom house '38' NOT 58 (the 3-form without the f-stroke — contrasting r54-'58' THE SAME PAGE = the reference pair Kurrent 3/5!); ★ h38 = the 1st DEATH entry (the 1904 GANSLER marriages outrun!); ★ the ŠIMEC network: 1889-h55-Peter-92-RECORD + 1890-h38-Jurij-48; the 2nd ŠAŠELJ-Griblje!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04894",
    year: 1890,
    scan: 27,
    page: 26,
    whatSi: "umrla Marija Straus, ¼ žemlj. hči, 8 mesecev (30. 10., pokop 1. 11.) — Božjast [~]; —; Jos. Rauq; ★★ STRAUS-MREŽA #3 (2× 'Marija Straus' v 2 letih!); ★ HIŠA-FORENZIKA: max-zoom '71' = γ-7-forma + 1 (NE 72! — nasprotje P154-lead-h72); h71 = 04894-1886 že (kontinuiteta 1886→1890)",
    whatEn: "died Marija Straus, a quarter-farmer's daughter, 8 months (Oct 30, buried Nov 1) — Božjast [~]; —; Jos. Rauq; ★★ the STRAUS NETWORK #3 (2× 'Marija Straus' in 2 years!); ★ HOUSE FORENSICS: the max-zoom '71' = the γ-7-form + 1 (NOT 72! — contrasting the P154-lead-h72); h71 already in 04894-1886 (the continuity 1886→1890)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04894",
    year: 1890,
    scan: 28,
    page: 27,
    whatSi: "umrl Matija Jaklič [~], ¼ žemlj. sin, 3 leta (15. 12., pokop 16. 12.) — Bele [~ Bule? NERAZREŠEN — cf. r54/r55!]; —; Jos. Rauq; ★ h18 = NAJZGODNEJŠI vpis kadarkoli (poročna 04455-1896 Klobučar-EDINA-1896 prekašana za 6 let!); cf. 1891-r2 'N. Jaklič' Otok 18 (P157-lead!)",
    whatEn: "died Matija Jaklič [~], a quarter-farmer's son, 3 years (Dec 15, buried Dec 16) — Bele [~ Bule? UNRESOLVED — see r54/r55!]; —; Jos. Rauq; ★ h18 = the EARLIEST entry ever (the 1896 marriage — the ONLY 1896 Griblje one — outrun by 6 years!); cf. the 1891-r2 'N. Jaklič' Otok 18 (a P157-lead!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04894",
    year: 1890,
    scan: 28,
    page: 27,
    whatSi: "mrtvorojen N. Križan (brez krstnega imena), ¼ žemljaškovo DETE [neuterska forma — edinstvena!], starost '—', SMRT = POKOP ISTI DAN (19./19. 12.) — Mrtvorojeno [IZPISANO — 1. LEKSIKONSKA REFERENCA linije! ampak Mertvod-odrasli ×3 ≠ enostavna enačba — X6!]; BREZ PODPISA (črtica); h35 = 4. mrliški vpis (1887 + 1888×2 + 1890); Križan-net (1888-r102-Peter-80!)",
    whatEn: "stillborn N. Križan (no first name), a quarter-farmer's CHILD [the neuter form — unique!], age '—', DEATH = BURIAL THE SAME DAY (Dec 19/19) — Mrtvorojeno [SPELLED OUT — the 1st LEXICON REFERENCE of the line! but Mertvod-adults ×3 ≠ a simple equation — X6!]; NO SIGNATURE (a dash); h35 = the 4th death entry (1887 + 1888×2 + 1890); the Križan network (1888-r102-Peter-80!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04894",
    year: 1890,
    scan: 28,
    page: 27,
    whatSi: "umrl Anton Požek, ¼ žemlj. sin, 2 leti (19. 12., pokop 21. 12.) — Bele [~ Bule? — december-kompleks r51/r54/r55!]; —; Jos. Rauq; ★ max-zoom hiša '58' (5-forma z f-črto! nasprotje r35-'38' ISTA STRAN — 2. potrjena!); ★ h58 = Požek-net: 1887-r58-Marko-66-Mertvod + 1890-Anton-2 = ×2 čez 3 leta",
    whatEn: "died Anton Požek, a quarter-farmer's son, 2 years (Dec 19, buried Dec 21) — Bele [~ Bule? — the December complex r51/r54/r55!]; —; Jos. Rauq; ★ max-zoom house '58' (the 5-form with the f-stroke! contrasting r35-'38' THE SAME PAGE — confirmed 2×); ★ h58 = the Požek network: 1887-r58-Marko-66-Mertvod + 1890-Anton-2 = ×2 across 3 years",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04894",
    year: 1890,
    scan: 28,
    page: 27,
    whatSi: "umrla Ana Urh, ¼ žemlj. hči, 1½ leta (21. 12., pokop 23. 12.) — Bele [~ Bule?]; —; Jos. Rauq; ZADNJI gribeljski vpis 1890 (meja 1891 ISTA STRAN — inline!); ★ h32 = 1. MRLIŠKI vpis (krstni oče Matija Urh ×3 1889/1890/1892 ISTA FAMILIJA!) — Urh-veriga 1887–1892",
    whatEn: "died Ana Urh, a quarter-farmer's daughter, 1½ years (Dec 21, buried Dec 23) — Bele [~ Bule?]; —; Jos. Rauq; the LAST Griblje entry of 1890 (the 1891 boundary on the SAME page — inline!); ★ h32 = the 1st DEATH entry (the baptism father Matija Urh ×3 1889/1890/1892 the SAME FAMILY!) — the Urh chain 1887–1892",
    status: "DOCUMENTED",
  },
  // ——— P80 razširitev: POROČNA KNJIGA 04455 1873–1922 — okvir 1886 (skeni 61–65 == Pag. 60–64, vpisi 1–24; Pag. = sken − 1 v razponu 61–66) ———
  // P115 (faza 2) RE-READ: 8 blokov popravljenih na podlagi max-zoom branja (h36→56, h63→65, h15→16, h25→Priložje
  // + priimki Pegdirec/Klepec/Požek/Tomec/Straus/Križan) — evidence: research/issue17/parish-marriage-1886.json
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1886,
    scan: 61,
    page: 60,
    whatSi: "poroka (7. 2., vpis 2/1886) — ženin Martin Papič [~], Gärtler und Mygenum? [~], 28, GRIBLJE 31 × Margareth STRAUS, 21, ½ Dienstmagd z (pri) Vöblhar? [~], Gorsiče? 5 [~] (P115 re-read: priimek = Straus, ne P80 »Špelcer« — oče Martin Straus ½ Gütler + priča Nikolaus Straus!); nevestini starši: Martin Straus (½ Gütler) + Maria née Fabrak? [~] (P80 »Stabek« = napaka); priče: Andreas Papič + Nikolaus Straus; duhovnik: franz Dovgan",
    whatEn: "marriage (Feb 7, entry 2/1886) — groom Martin Papič [~], Gärtler und Mygenum? [~], 28, GRIBLJE 31 × Margareth STRAUS, 21, half maid at Vöblhar? [~], Gorsiče? 5 [~] (P115 re-read: the surname is Straus, not the P80 »Špelcer« — father Martin Straus half-smallholder + witness Nikolaus Straus!); bride's parents: Martin Straus (½ Gütler) + Maria née Fabrak? [~] (the P80 »Stabek« wrong); witnesses: Andreas Papič + Nikolaus Straus; priest: franz Dovgan",
    status: "DOCUMENTED",
  },
  {
    houseNo: "56",
    bookSignature: "04455",
    year: 1886,
    scan: 62,
    page: 61,
    whatSi: "poroka (15. 2., vpis 4/1886) — ženin Johann Šimec, Lavřin, 24, GRIBLJE 56 (P115 re-read: hiša = 56, NE P80 »36«!; starši: Johann Šimec + Maria née Jakobič) × Dorothea PEGDIREC, 30, LandwirthsTochter, Krasinec 28 (P115: priimek = Pegdirec, ne P80 »Perdinec«; hiša 28, ne »38«; starši: Peter Pegdirec ½ Gütler + Anna née Musié) = ISTI PAR kot krst hiše 56 (Nov 1886) — SESTRIN+BRAT DVOJNI POROKI ISTEGA DNE: brat Peter Pegdirec poročen ISTEGA 15.2. (vpis 5, ISTI starši!); duhovnik: BREZ PODPISA (vpisi 4–19 neodpisani!)",
    whatEn: "marriage (Feb 15, entry 4/1886) — groom Johann Šimec, Lavřin, 24, GRIBLJE 56 (the P115 re-read: house = 56, NOT the P80 »36«!; parents: Johann Šimec + Maria née Jakobič) × Dorothea PEGDIREC, 30, farmer's daughter, Krasinec 28 (the P115: surname = Pegdirec, not the P80 »Perdinec«; house 28, not »38«; parents: Peter Pegdirec ½ Gütler + Anna née Musié) = SAME COUPLE as the house-56 baptism (Nov 1886) — SIBLING DOUBLE WEDDING THE SAME DAY: brother Peter Pegdirec married THE SAME Feb 15 (entry 5, the SAME parents!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04455",
    year: 1886,
    scan: 63,
    page: 62,
    whatSi: "poroka (21. 2., vpis 11/1886) — nevesta Maria Bohor, LandwirthsTochter (P115: NE P80 »Dienstmagd«), 21, GRIBLJE 60 (starši: Georg Bohor + Katharina née Križan ✓) × Mathias KLEPEC (P115 re-read: priimek = Klepec, ne P80 »Kukec«!), 30, Dragoše 2 (starši: Mathias Klepec + Anna née Šimec = ŠIMEC-mreža h56!); hiša 60 v PT luknji 41–60; duhovnik: BREZ PODPISA",
    whatEn: "marriage (Feb 21, entry 11/1886) — bride Maria Bohor, farmer's daughter (the P115: NOT the P80 »maid«), 21, GRIBLJE 60 (parents: Georg Bohor + Katharina née Križan ✓) × Mathias KLEPEC (the P115 re-read: the surname is Klepec, not the P80 »Kukec«!), 30, Dragoše 2 (parents: Mathias Klepec + Anna née Šimec = the ŠIMEC network h56!); house 60 in the PT 41–60 gap",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04455",
    year: 1886,
    scan: 63,
    page: 62,
    whatSi: "poroka (21. 2., vpis 12/1886) — ženin Mathias Milek (mrliška piše »Mileh« = pisateljska varianta [~]), ½ Gütler, 44, GRIBLJE 65 (P115 re-read: hiša = 65, NE P80 »63« — številka jasno!) × Katharina POŽEK (P115: NE P80 »Peršić«), 18, LandwirthsTochter, GRIBLJE 64 (P115: NE P80 »Gradec 61« — NOVA Griblje hiša 64 v okviru!; nečitljiva oznaka »Klad?/Zlad?« nad Griblje [~]); starši neveste: Mathias Požek + Maria née PEGDIREC; priča: Michael Pegdirec (= ženin vpis 1!) + k.k. Kreisgericht Tschernembl konsenz dd. 20.1.1886; duhovnik: BREZ PODPISA",
    whatEn: "marriage (Feb 21, entry 12/1886) — groom Mathias Milek (the death register writes »Mileh« = a scribal variant [~]), ½ Gütler, 44, GRIBLJE 65 (the P115 re-read: house = 65, NOT the P80 »63« — the number is clear!) × Katharina POŽEK (the P115: NOT the P80 »Peršić«), 18, farmer's daughter, GRIBLJE 64 (the P115: NOT the P80 »Gradec 61« — a NEW Griblje house 64 in the frame!; an illegible qualifier »Klad?/Zlad?« above Griblje [~]); bride's parents: Mathias Požek + Maria née PEGDIREC; witness: Michael Pegdirec (= groom of entry 1!) + the k.k. Kreisgericht Tschernembl consent Feb 20, 1886",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04455",
    year: 1886,
    scan: 64,
    page: 63,
    whatSi: "poroka (20. 6., vpis 17/1886) — nevesta Ana Filak, Lavřin, 33, GRIBLJE 16 (P115 re-read: hiša = 16, NE P80 »15« — številka 6 brez zastavice, 1:1 primerjava z znano »65«; starši: Mathias Filak + Anna née Gregorič ✓) × Georg Tomec, ½ Gütler, 45, Krivoglave 41; P80 povezava »hiša 15 = smrt Nikolaja Muca (Jul 1886)« ostaja pri h15 — h15 še vedno sidro 1887 (Jaklič × Brinec)!; duhovnik: BREZ PODPISA",
    whatEn: "marriage (Jun 20, entry 17/1886) — bride Ana Filak, Lavřin, 33, GRIBLJE 16 (the P115 re-read: house = 16, NOT the P80 »15« — the digit 6 without a flag, a 1:1 comparison with the known »65«; parents: Mathias Filak + Anna née Gregorič ✓) × Georg Tomec, ½ Gütler, 45, Krivoglave 41; the P80 link »house 15 = the death of Nikolaj Muc (Jul 1886)« stays with h15 — h15 remains the 1887 anchor (Jaklič × Brinec)!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04455",
    year: 1886,
    scan: 64,
    page: 63,
    whatSi: "poroka (8. 11., vpis 20/1886) — ženin Jurij Klepec, ½ zemlj. sin, 23, PRILOŽJE 25 (P115 re-read: vas = Priložje, NE P80 »GRIBLJE 25«! — max zoom + IZBRISAN zapis pod vasjo; hiša 25 Griblje brez poročnega dokaza 1886!) × Katharina TOMEC (P115: NE P80 »Gomec«), 23, ½ STIEFTOCHTER, Krasinec 35 (starši: Mathias Tomec + Anna roj. PEGDIREC); priče: Mathias Tomec (nevestin oče) + Martin Berkovec?; Urkunden: vojaška privolitev dd. 8.11.1886; duhovnik: franz Dovgan",
    whatEn: "marriage (Nov 8, entry 20/1886) — groom Jurij Klepec, half-farmer's son, 23, PRILOŽJE 25 (the P115 re-read: the village is Priložje, NOT the P80 »GRIBLJE 25«! — max zoom + an ERASED entry below the village; house 25 Griblje without a marriage proof 1886!) × Katharina TOMEC (the P115: NOT the P80 »Gomec«), 23, ½ STEP-DAUGHTER, Krasinec 35 (parents: Mathias Tomec + Anna née PEGDIREC); witnesses: Mathias Tomec (the bride's father) + Martin Berkovec?; Urkunden: the military consent Nov 8, 1886; priest: franz Dovgan",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04455",
    year: 1886,
    scan: 65,
    page: 64,
    whatSi: "poroka (21. 11., vpis 23/1886) — nevesta Maria Straus, Lavřin + MÜNDEL (varovanka!), 34, GRIBLJE 71 (starši: Janez Straus, Landwirth + Anna née Stubler ✓) × Martin KRIŽAN (P115 re-read: NE P80 »Marko Perzan«!), Landwirth (1. poln kmet vzorca!), 41, Krasinec 9 (NE P80 »Vinica 9«); MÜNDEL-TIMELINE: mati Ana Strauš † 7.9.1886 (mrliška!) → hči (34) poročena 21.11.1886 kot varovanka; hiša 71 = Strauš v VSEH treh knjigah; duhovnik: franz Dovgan",
    whatEn: "marriage (Nov 21, entry 23/1886) — bride Maria Straus, Lavřin + a WARD (Mündel!), 34, GRIBLJE 71 (parents: Janez Straus, farmer + Anna née Stubler ✓) × Martin KRIŽAN (the P115 re-read: NOT the P80 »Marko Perzan«!), a FULL FARMER (Landwirth — the 1st of the sample!), 41, Krasinec 9 (NOT the P80 »Vinica 9«); the WARD TIMELINE: the mother Ana Strauš † Sep 7, 1886 (death register!) → the daughter (34) married Nov 21, 1886 as a ward; house 71 = Strauš in ALL THREE registers; priest: franz Dovgan",
    status: "DOCUMENTED",
  },
  // ——— P80 sidri poročne (izven okvirja 1886 — veriga hiša→družina čez leta) ———
  {
    houseNo: "13",
    bookSignature: "04455",
    year: 1885,
    scan: 61,
    page: 60,
    whatSi: "poroka (22. 11. 1885) — ženin Janez Jakobič, Leinweber, 25, GRIBLJE 13 (starši: Mathias Jakobič + Maria née PEGDIREC — P115 re-read: NE P80 »Podlirec«! = STARŠI krsta hiše 13, Nov 1886) × Marija Stubler, 21, GRIBLJE 25; sidro pred okvirjem 1886; duhovnik: franz Dovgan",
    whatEn: "marriage (Nov 22, 1885) — groom Janez Jakobič, linen weaver, 25, GRIBLJE 13 (parents: Mathias Jakobič + Maria née PEGDIREC — the P115 re-read: NOT the P80 »Podlirec«! = the PARENTS of the Nov 1886 house-13 baptism) × Marija Stubler, 21, GRIBLJE 25; anchor before the 1886 frame; priest: franz Dovgan",
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
    whatSi: "poroka (31. 1. 1887, vpis 3) — ženin Mathias Straus, Leinweber, 24, GRIBLJE 71 (starši: Mathias Straus + Katharina née Dragoš ✓) × Barbara Rusić? [~], 21, GRIBLJE 37 (starši: Michael Rusić × Katharina née KAMBIČ — P116 re-read: ne »Šambiè«!); duhovnik franz Dovgan; Befünden: Ehenichtschild Griblje 31.1.1887 + »Mütterl. …«? [~]; sidro po okvirju 1886 (P116 POTRJEN 1:1); Straus-mreža h71: krst Jurij + smrt Ane vdove + Maria Mündel 21.11.1886 + Mathias 31.1. + Katharina 20.2.1887 (vpis 11!) = 5 dokazov",
    whatEn: "marriage (Jan 31, 1887, entry 3) — groom Mathias Straus, linen weaver, 24, GRIBLJE 71 (parents: Mathias Straus + Katharina née Dragoš ✓) × Barbara Rusić? [~], 21, GRIBLJE 37 (parents: Michael Rusić × Katharina née KAMBIČ — the P116 re-read: not »Šambiè«!); priest franz Dovgan; Befunden: Ehenichtschild Griblje Jan 31, 1887 + »Mütterl. …«? [~]; anchor after the 1886 frame (P116 CONFIRMED 1:1); the Straus network h71: the Jurij baptism + the widow Ana's death + Maria Mündel Nov 21, 1886 + Mathias Jan 31 + Katharina Feb 20, 1887 (entry 11!) = 5 pieces of evidence",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04455",
    year: 1887,
    scan: 66,
    page: 65,
    whatSi: "poroka (6. 2. 1887, vpis 4) — ženin Johann FABLIĆ, Leinweber, 23, GRIBLJE 15 (starši: Nikolaus Fablić × Maria geb. Kambič — P116 re-read: ne »Šambie«! = BRAT Mathiasa Fablića vpisa 1/1887, Boršt 44!) × Maria Brinec, 26, GRIBLJE 23 (P116 re-read: ne »29«!; starši: Mathias Brinec + Maria geb. Milek — povezava z umrlimi otroki h29 ostaja pri materi roj. Milek); duhovnik franz Dovgan; Befünden: Ehenichtschild Griblje 6.2. + Großjährigkeits-Schein k.k. Bez.-Ger. 31.1.; sidro (P116)",
    whatEn: "marriage (Feb 6, 1887, entry 4) — groom Johann FABLIĆ, linen weaver, 23, GRIBLJE 15 (parents: Nikolaus Fablić × Maria née Kambič — the P116 re-read: not »Šambie«! = the BROTHER of Mathias Fablić, entry 1/1887, Boršt 44!) × Maria Brinec, 26, GRIBLJE 23 (the P116 re-read: not »29«!; parents: Mathias Brinec + Maria née Milek — the link to the house-29 dead children stays with the née-Milek mother); priest franz Dovgan; Befunden: Ehenichtschild Griblje Feb 6 + Großjährigkeits-Schein k.k. district court Jan 31; anchor (P116)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04455",
    year: 1887,
    scan: 66,
    page: 65,
    whatSi: "poroka (6. 2. 1887, vpis 4) — NEVESTA Maria Brinec, 26, GRIBLJE 23 (P116 re-read: NOVA hiša — P80 branje »29« = popravljen na 23; max zoom: jasno »23«; starši: Mathias Brinec + Maria geb. Milek) × Johann Fablić, Leinweber, 23, GRIBLJE 15; duhovnik franz Dovgan; Befstände h23 = Mathias Milek (¼ G. — dedek po materi?); povezava: mati roj. Milek = družina umrlih otrok h29 (mrliška okt. 1886); crossCheck: Mathias BRINEC iz GRIBLJE 23 poročen 30.1.1888 (P117 re-read: ne »Michael« [faza-1] — max zoom jasno »Mathias«!) = Brinec-družina na h23 potrjena ×2 (BRATA: sestra Maria 1887 + brat Mathias 1888, isti starši!)",
    whatEn: "marriage (Feb 6, 1887, entry 4) — the BRIDE Maria Brinec, 26, GRIBLJE 23 (the P116 re-read: A NEW house — the P80 »GRIBLJE 29« corrected to 23; max zoom: clearly »23«; parents: Mathias Brinec + Maria née Milek) × Johann Fablić, linen weaver, 23, GRIBLJE 15; priest franz Dovgan; Befstände h23 = Mathias Milek (¼ G. — the maternal grandfather?); the link: the née-Milek mother = the family of the house-29 dead children (death register Oct 1886); cross-check: Mathias BRINEC from GRIBLJE 23 married Jan 30, 1888 (the P117 re-read: not »Michael« [faza-1] — the max zoom clearly »Mathias«!) = the Brinec family at h23 confirmed ×2 (BROTHERS: sister Maria 1887 + brother Mathias 1888, the same parents)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "37",
    bookSignature: "04455",
    year: 1887,
    scan: 66,
    page: 65,
    whatSi: "poroka (31. 1. 1887, vpis 3) — NEVESTA Barbara Rusić? [~], 21, GRIBLJE 37 (NOVA hiša; starši: Michael Rusić × Katharina née Kambič — P116 re-read: ne »Šambiè«) × Mathias Straus, Leinweber, 24, GRIBLJE 71; duhovnik franz Dovgan; status neveste = »Fraus-murd«? [~] (neprepoznana oznaka »…frau.«)",
    whatEn: "marriage (Jan 31, 1887, entry 3) — the BRIDE Barbara Rusić? [~], 21, GRIBLJE 37 (A NEW house; parents: Michael Rusić × Katharina née Kambič — the P116 re-read: not »Šambiè«) × Mathias Straus, linen weaver, 24, GRIBLJE 71; priest franz Dovgan; the bride's status = »Fraus-murd«? [~] (an unrecognized »…frau.« label)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04455",
    year: 1887,
    scan: 68,
    page: 67,
    whatSi: "poroka (20. 2. 1887, vpis 11) — ženin Johann Brine? [~ Brinec?], Leinweber, 22, GRIBLJE 69 (P116 re-read: NOVA hiša — max zoom jasno »69« z repkom; faza 1 »64« = NAPAKA, h64 ostaja P115 vpis 12/1886 nevesta Požek!) × Katharina Straus, 19, GRIBLJE 71 (2. Straus-poroka h71 v letu!); duhovnik franz Dovgan; Befünden: Ehenichtschild Griblje 20.2. + Großjährigkeits-Schein; datum 20. (ne 21. — faza 1 popravka)",
    whatEn: "marriage (Feb 20, 1887, entry 11) — groom Johann Brine? [~ Brinec?], linen weaver, 22, GRIBLJE 69 (the P116 re-read: A NEW house — the max zoom clearly »69« with a tail; the faza-1 »64« = WRONG, h64 remains the P115 entry 12/1886 bride Požek!) × Katharina Straus, 19, GRIBLJE 71 (the 2nd Straus marriage at h71 in the year!); priest franz Dovgan; Befunden: Ehenichtschild Griblje Feb 20 + Großjährigkeits-Schein; the date 20 (not 21 — the faza-1 correction)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04455",
    year: 1887,
    scan: 70,
    page: 69,
    whatSi: "poroka (4. 9. 1887, vpis 20) — ženin Peter Križan? [Vrižan? ~], ¼ Gütler, 40 (najstarejši Griblje-ženin 1887!), GRIBLJE 3 (NOVA hiša) × Catharina Križe, ¼ Gütlerstochter, 27, GRIBLJE 10 (NOVA hiša); duhovnik Jos. Rouy [~]; starši: Peter Križan (¼ Gübler) × Ana Deblič | Janez Hriže/Križe (½ Güblersohn) × Katharina Jaklič? [~]; Befünden: Ehenichtschild Griblje 27.8.1887 št. 16; KRIŽAN × KRIŽE = istoimenska mreža (cf. P115 Martin KRIŽAN Krasinec 9 + h36 Križan 1882!)",
    whatEn: "marriage (Sep 4, 1887, entry 20) — groom Peter Križan? [Vrižan? ~], ¼ smallholder, 40 (the oldest Griblje groom of 1887!), GRIBLJE 3 (A NEW house) × Catharina Križe, ¼ smallholder's daughter, 27, GRIBLJE 10 (A NEW house); priest Jos. Rouy [~]; parents: Peter Križan × Ana Deblič | Janez Križe (½ smallholder's son) × Katharina Jaklič? [~]; Befunden: Ehenichtschild Griblje Aug 27, 1887 no. 16; KRIŽAN × KRIŽE = the same-root network (cf. the P115 Martin KRIŽAN Krasinec 9 + the h36 Križan 1882!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04455",
    year: 1887,
    scan: 70,
    page: 69,
    whatSi: "poroka (4. 9. 1887, vpis 20) — NEVESTA Catharina Križe, ¼ Gütlerstochter, 27, GRIBLJE 10 (P116 re-read: NOVA hiša — faza 1 »19« = 10 popravka, max zoom čista ovalna 0) × Peter Križan? [~], ¼ Gütler, 40, GRIBLJE 3; duhovnik Jos. Rouy [~]; starši neveste: Janez Hriže/Križe (½ Güblersohn) × Katharina Jaklič? [~]; Befstände h10 = Jakob Hriže/Križe (½ Gübler)",
    whatEn: "marriage (Sep 4, 1887, entry 20) — the BRIDE Catharina Križe, ¼ smallholder's daughter, 27, GRIBLJE 10 (the P116 re-read: A NEW house — the faza-1 »19« corrected to 10, the max zoom's clean oval 0) × Peter Križan? [~], ¼ smallholder, 40, GRIBLJE 3; priest Jos. Rouy [~]; the bride's parents: Janez Križe (½ smallholder's son) × Katharina Jaklič? [~]; Befstände h10 = Jakob Križe (½ smallholder)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04455",
    year: 1888,
    scan: 71,
    page: 70,
    whatSi: "poroka (30. 1. 1888, vpis 2) — ženin Mathias BRINEC, ½ Gütlsohn, 24, GRIBLJE 23 (P117 re-read: ne »Michael« [faza-1] — max zoom jasno »Mathias«; starši = ISTI kot 1887 v4: Mathias Brinec + Maria roj. Milek!) × Maria Dehlič? [~], ½ Gütlstochter, 23, GRIBLJE 33 (NOVA hiša; starši: Mathias Dehlič × Maria roj. Husič? [~]); priče: Martin Klobučar? [~] (¼ Gütl.) + Johann Milek (½ Gütl. — cf. mati roj. Milek!); duhovnik Jos. Rauy provisor; Befünden: zglasnica občine Griblje 30.1.1888 št. 4 + mündliche Einwilligung; 2. poročni blok h23 (cf. 1887 v4 nevesta Maria Brinec — BRATA Brinec, isti starši!)",
    whatEn: "marriage (Jan 30, 1888, entry 2) — groom Mathias BRINEC, half smallholder's son, 24, GRIBLJE 23 (the P117 re-read: not »Michael« [faza-1] — the max zoom clearly »Mathias«; parents = THE SAME as 1887 v4: Mathias Brinec + Maria née Milek!) × Maria Dehlič? [~], half smallholder's daughter, 23, GRIBLJE 33 (A NEW house; parents: Mathias Dehlič × Maria née Husič? [~]); witnesses: Martin Klobučar? [~] (¼ smallholder) + Johann Milek (½ smallholder — cf. the née-Milek mother!); priest Jos. Rauy provisor; Befunden: the commune-Griblje announcement Jan 30, 1888 no. 4 + a mündliche Einwilligung; the 2nd marriage block of h23 (cf. 1887 v4 bride Maria Brinec — the BRINEC BROTHERS, the same parents!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04455",
    year: 1888,
    scan: 71,
    page: 70,
    whatSi: "poroka (30. 1. 1888, vpis 2) — NEVESTA Maria Dehlič? [~], ½ Gütlstochter, 23, GRIBLJE 33 (NOVA hiša; starši: Mathias Dehlič × Maria roj. Husič? [~] — cf. 1887 v3 nevesta »Rusić/Husić«) × Mathias Brinec, ½ Gütlsohn, 24, GRIBLJE 23; priče: Martin Klobučar? + Johann Milek (½ Gütl.); duhovnik Jos. Rauy provisor; Befünden: zglasnica Griblje 30.1.1888 št. 4",
    whatEn: "marriage (Jan 30, 1888, entry 2) — the BRIDE Maria Dehlič? [~], half smallholder's daughter, 23, GRIBLJE 33 (A NEW house; parents: Mathias Dehlič × Maria née Husič? [~] — cf. 1887 v3 bride »Rusić/Husić«) × Mathias Brinec, half smallholder's son, 24, GRIBLJE 23; witnesses: Martin Klobučar? + Johann Milek (½ smallholder); priest Jos. Rauy provisor; Befunden: the Griblje announcement Jan 30, 1888 no. 4",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04455",
    year: 1888,
    scan: 71,
    page: 70,
    whatSi: "poroka (14. 5. 1888, vpis 7) — ženin Mathias STRAUS, ¼ Gütlsohn?, 26, GRIBLJE 32 (NOVA hiša — 2. Straus-hiša v liniji!; P117 re-read: ne »Kravce?«; starši: MARCUS Straus × Katharina Dragoševič? [~] — cf. 1887 v3: Mathias Straus h71 × Katharina née Dragoš = 2 veje!) × Maria Jakoš? [~], ½? Gütlsohnstochter?, 19, Krasinec 43; priče: Joh. Brodarič? + Math. Bahrič? (½ Gütl.); duhovnik Jos. Rauy provisor; Befünden: zglasnica Podzemelj 14.5.1888 št. 15 + očetovo dovoljenje v prisotnosti dveh prič",
    whatEn: "marriage (May 14, 1888, entry 7) — groom Mathias STRAUS, quarter smallholder's son?, 26, GRIBLJE 32 (A NEW house — the 2nd Straus house in the line!; the P117 re-read: not »Kravce?«; parents: MARCUS Straus × Katharina Dragoševič? [~] — cf. 1887 v3: Mathias Straus h71 × Katharina née Dragoš = 2 branches!) × Maria Jakoš? [~], half smallholder's daughter?, 19, Krasinec 43; witnesses: Joh. Brodarič? + Math. Bahrič? (½ smallholder); priest Jos. Rauy provisor; Befunden: the Podzemelj announcement May 14, 1888 no. 15 + the father's consent in the presence of two witnesses",
    status: "DOCUMENTED",
  },
  {
    houseNo: "64",
    bookSignature: "04455",
    year: 1888,
    scan: 73,
    page: 72,
    whatSi: "poroka (27. 8. 1888, vpis 12) — ženin Johann Marhiščar? [~ — N/V/M dvom], ¼ Gütl., 24, GRIBLJE 64 (2. poročni dokaz h64 po 1886 v12 Milek × Požek!; P82 krstna »26 [~]« dvom REŠEN → 64; mati = Anna PEGDIREC — mreža!) × Margareth Klepec, ½ Gütlstochter, 26, Cerkvišče? [~] 29 (starši: Jakob Klepec × Margareth Vipavec); priče: Georg? Klepec (½ Gütl.) + Peter PEGDIREC (Gütlstar? [~] — = P115 v5 ŽENIN 1886!); duhovnik Jos. Rauy provisor; Befünden: zglasnica Griblje 27.7.1888 št. 23",
    whatEn: "marriage (Aug 27, 1888, entry 12) — groom Johann Marhiščar? [~ — N/V/M doubt], quarter smallholder, 24, GRIBLJE 64 (the 2nd marriage evidence of h64 after the 1886 v12 Milek × Požek!; the P82 baptism »26 [~]« doubt RESOLVED → 64; the mother = Anna PEGDIREC — the network!) × Margareth Klepec, half smallholder's daughter, 26, Cerkvišče? [~] 29 (parents: Jakob Klepec × Margareth Vipavec); witnesses: Georg? Klepec (½ smallholder) + Peter PEGDIREC (Gütlstar? [~] — = the P115 v5 GROOM of 1886!); priest Jos. Rauy provisor; Befunden: the Griblje announcement Jul 27, 1888 no. 23",
    status: "DOCUMENTED",
  },
  // ——— P118 razširitev: POROČNA KNJIGA 04455 — polno leto 1889 (skeni 75–76 ==
  // strani 74–75; glava 1889 brez velike glave [~]; vrstice restart na 1;
  // 10 vpisov = 6+4; LANDSCAPE geometrija) — 7 novih blokov (1. poročni dokazi
  // h7/h21/h30/h40/h54/h87 — vse hiše že v krstni 04105! + h32 2. dokaz)
  {
    houseNo: "32",
    bookSignature: "04455",
    year: 1889,
    scan: 75,
    page: 74,
    whatSi: "poroka (11. 2. 1889, vpis 2) — ženin Mathias URB, ¼ Gütlsohn, 24, GRIBLJE 32 (2. poročni dokaz h32 v 2 letih po 1888 v7 Straus!; P118 faza-1 oris »Matthias Mech?« = popravek → Urb; starši: Urb (¼ Gütl.? [~]) × Maria DOHLIČ — cf. 1888 v2 nevesta Maria Dehlič h33 = Dohlič-mreža med leti!) × Margareth PERDINEC, ½ Gütlstochter, 21, GRIBLJE 40 (1. poročni dokaz h40; faza-1 oris »Lechne? h16« = popravek!; starši: Perdinec (¼ Gütl.? [~]) × Jakošeč? [~]); priča: Michael Bezkopec? [~] (½ Gütl.); duhovnik Jos. Rauy; Befünden: zglasnica občine Griblje 26.1.1889 št. 3 + mündliche väterliche Einwilligung für die mj. (minderjährige!) Braut; PERDINEC ×3 v 1889!",
    whatEn: "marriage (Feb 11, 1889, entry 2) — groom Mathias URB, quarter smallholder's son, 24, GRIBLJE 32 (the 2nd marriage evidence of h32 within 2 years after the 1888 v7 Straus!; the P118 faza-1 outline »Matthias Mech?« = a correction → Urb; parents: Urb (¼ smallholder? [~]) × Maria DOHLIČ — cf. the 1888 v2 bride Maria Dehlič h33 = the Dohlič network across years!) × Margareth PERDINEC, half smallholder's daughter, 21, GRIBLJE 40 (the 1st marriage evidence of h40; the faza-1 outline »Lechne? h16« = a correction!; parents: Perdinec (¼ smallholder? [~]) × Jakošeč? [~]); witness: Michael Bezkopec? [~] (½ smallholder); priest Jos. Rauy; Befunden: the commune-Griblje announcement Jan 26, 1889 no. 3 + the mündliche väterliche Einwilligung for the mj. (underage!) bride; PERDINEC ×3 in 1889!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04455",
    year: 1889,
    scan: 75,
    page: 74,
    whatSi: "poroka (11. 2. 1889, vpis 2) — NEVESTA Margareth PERDINEC, ½ Gütlstochter, 21, GRIBLJE 40 (1. poročni dokaz h40 — krstna 04105 že ×7!; starši: Perdinec (¼ Gütl.? [~]) × Jakošeč? [~]) × Mathias Urb, ¼ Gütlsohn, 24, GRIBLJE 32; priča: Michael Bezkopec? [~] (½ Gütl.); duhovnik Jos. Rauy; Befünden: zglasnica občine Griblje 26.1.1889 št. 3 + väterliche Einwilligung (mj. Braut); PERDINEC ×3 v 1889 — Perdinec-mreža! (cf. 1888 »Pegdirec« ×9 + P115 v5 ženin Peter 1886 — ista družina, 2 pisavi!)",
    whatEn: "marriage (Feb 11, 1889, entry 2) — the BRIDE Margareth PERDINEC, half smallholder's daughter, 21, GRIBLJE 40 (the 1st marriage evidence of h40 — the baptism register 04105 already ×7!; parents: Perdinec (¼ smallholder? [~]) × Jakošeč? [~]) × Mathias Urb, quarter smallholder's son, 24, GRIBLJE 32; witness: Michael Bezkopec? [~] (½ smallholder); priest Jos. Rauy; Befunden: the commune-Griblje announcement Jan 26, 1889 no. 3 + the väterliche Einwilligung (the underage bride); PERDINEC ×3 in 1889 (cf. the 1888 »Pegdirec« ×9 + the P115 v5 groom Peter 1886 — the same family, 2 spellings!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04455",
    year: 1889,
    scan: 75,
    page: 74,
    whatSi: "poroka (15. 2. 1889, vpis 3) — ženin Johann POŽEK, ¼ Gütl., 39, GRIBLJE 21 (2. poročni dokaz h21 po 1888 v3!; h21 ×2 zapored!; faza-1 oris »Perich?« = popravek → Požek!; starši: Johan Požek (¼ Gütl.) × Barbara DRAGOŠ) × Anna SIMEC, ¼ Gütlstochter, 23, GRIBLJE 54 (1. poročni dokaz h54; faza-1 oris »Maria Simic? GRIBLJE 24« = popravek ×2 → Anna h54!; starši: Georg Simec (¼ Gütl.) × Anna PERDINEC!); priče: Anton Podarič? [~] (½ Gütl.) + [—] Požek? [~]; duhovnik Jos. Rauy; Befünden: zglasnica občine Griblje 7.2.1889 št. 4 + Obschau-mündschaftl. Einwilligung k.k. Bez.-Ger. Črnomelj 21.1.1889 Z: 1118 (mj. Braut); POŽEK ×3 v 1889 (v3 + v4 ženin + v6 mati neveste!) + DRAGOŠ-mreža",
    whatEn: "marriage (Feb 15, 1889, entry 3) — groom Johann POŽEK, quarter smallholder, 39, GRIBLJE 21 (the 2nd marriage evidence of h21 after 1888 v3!; h21 ×2 in a row!; the faza-1 outline »Perich?« = a correction → Požek!; parents: Johan Požek (¼ smallholder) × Barbara DRAGOŠ) × Anna SIMEC, quarter smallholder's daughter, 23, GRIBLJE 54 (the 1st marriage evidence of h54; the faza-1 outline »Maria Simic? GRIBLJE 24« = a double correction → Anna h54!; parents: Georg Simec (¼ smallholder) × Anna PERDINEC!); witnesses: Anton Podarič? [~] (½ smallholder) + [—] Požek? [~]; priest Jos. Rauy; Befunden: the commune-Griblje announcement Feb 7, 1889 no. 4 + the Obschau-mündschaftliche Einwilligung of the k.k. Bez.-Ger. Črnomelj Jan 21, 1889 Z: 1118 (the underage bride); POŽEK ×3 in 1889 (v3 + the v4 groom + the v6 bride's mother!) + the DRAGOŠ network",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04455",
    year: 1889,
    scan: 75,
    page: 74,
    whatSi: "poroka (15. 2. 1889, vpis 3) — NEVESTA Anna SIMEC, ¼ Gütlstochter, 23, GRIBLJE 54 (1. poročni dokaz h54 — krstna 04105 že ×6!; faza-1 oris »Maria Simic? GRIBLJE 24« = popravek ×2: ime Anna, hiša 54!) × Johann Požek, ¼ Gütl., 39, GRIBLJE 21; starši: Georg Simec (¼ Gütl.) × Anna PERDINEC (Perdinec-mreža!); duhovnik Jos. Rauy; Befünden: zglasnica Griblje 7.2.1889 št. 4 + sodna Einwilligung k.k. Bez.-Ger. Črnomelj 21.1.1889 Z: 1118",
    whatEn: "marriage (Feb 15, 1889, entry 3) — the BRIDE Anna SIMEC, quarter smallholder's daughter, 23, GRIBLJE 54 (the 1st marriage evidence of h54 — the baptism register 04105 already ×6!; the faza-1 outline »Maria Simic? GRIBLJE 24« = a double correction: the name Anna, the house 54!) × Johann Požek, quarter smallholder, 39, GRIBLJE 21; parents: Georg Simec (¼ smallholder) × Anna PERDINEC (the Perdinec network!); priest Jos. Rauy; Befunden: the Griblje announcement Feb 7, 1889 no. 4 + the court Einwilligung of the k.k. Bez.-Ger. Črnomelj Jan 21, 1889 Z: 1118",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04455",
    year: 1889,
    scan: 75,
    page: 74,
    whatSi: "poroka (25. 2. 1889, vpis 4) — NEVESTA Margareth TOTTER, ½ Gütlstochter, 23, GRIBLJE 7 (1. POROČNI dokaz h7 — krstna 04105 že ×4!) × Michael POŽEK, Ziegler? [~], 30, ADLEŠIČE 9 (tuja župnija/občina!; POŽEK ×2 ženina v 2 tednih — brata? [~]); starši neveste: Totter (¼ Gütl.) × Margareth Kruzej? [~]; priče: Martin Vukšenič (½ Gütl.) + Michael GRABRIJAN (cf. 1887 popravek!); duhovnik Jos. Rauy; Befünden ×3: zglasnica občine Adlešiče 7.2.1889 št. 22 + oznamni list ženinov župn. urada Adlešiči 24.2. št. 28 (NOV dokument!) + mündliche väterliche Einwilligung (mj. Braut)",
    whatEn: "marriage (Feb 25, 1889, entry 4) — the BRIDE Margareth TOTTER, half smallholder's daughter, 23, GRIBLJE 7 (the 1st MARRIAGE evidence of h7 — the baptism register 04105 already ×4!) × Michael POŽEK, Ziegler? [~ (tiler)], 30, ADLEŠIČE 9 (a foreign parish/municipality!; POŽEK ×2 grooms within 2 weeks — brothers? [~]); the bride's parents: Totter (¼ smallholder) × Margareth Kruzej? [~]; witnesses: Martin Vukšenič (½ smallholder) + Michael GRABRIJAN (cf. the 1887 correction!); priest Jos. Rauy; Befunden ×3: the commune-Adlešiče announcement Feb 7, 1889 no. 22 + the oznamni list of the groom(s) from the parish office Adlešiči Feb 24 no. 28 (A NEW document!) + the mündliche väterliche Einwilligung (the underage bride)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04455",
    year: 1889,
    scan: 76,
    page: 75,
    whatSi: "poroka (14. 10. 1889, vpis 8) — ženin Johann MILEK, ½ Gütl., 60 LET, GRIBLJE 30 (1. POROČNI dokaz h30 — krstna 04105 že ×14!; faza-1 oris »Mulek?/Melek« = popravek → Milek; cf. 1887 v4 mati roj. Milek h23 = Milek-mreža med leti!) × Margareth PERDINEC, ½ Gütlstochter, 23, GRIBLJE 87 (1. poročni dokaz h87 — NAJVIŠJA hiša poročne linije!; starši: MARCUS Perdinec, ⅓ Gütl. [NOV ULOMEK!], × Margareth KLEJPEC — faza-1 »Kleklvec« popravek!); priče: Michael Bezkopec? [~] + Johann Jurajevič (½ Gütl.); duhovnik AMBROSIJ GLIHA coop. [~] — 2. duhovnik 1889 (Rauy absent!); Befünden ×3: zglasnica občine Griblje 14.10.1889 št. 26 + [G?upjäftigit-Knitt-Etbürning ~] + Obschau-mündschaftl. Genehm. k.k. Bez.-Ger. Črnomelj 7.10. Z: 8062 (mj. Braut); 60 × 23 = 37 LET RAZLIKE!",
    whatEn: "marriage (Oct 14, 1889, entry 8) — groom Johann MILEK, half smallholder, 60 YEARS, GRIBLJE 30 (the 1st MARRIAGE evidence of h30 — the baptism register 04105 already ×14!; the faza-1 outline »Mulek?/Melek« = a correction → Milek; cf. the 1887 v4 bride's mother née Milek h23 = the Milek network across years!) × Margareth PERDINEC, half smallholder's daughter, 23, GRIBLJE 87 (the 1st marriage evidence of h87 — THE HIGHEST house number of the marriage line!; parents: MARCUS Perdinec, ⅓ smallholder [A NEW FRACTION!], × Margareth KLEJPEC — the faza-1 »Kleklvec« correction!); witnesses: Michael Bezkopec? [~] + Johann Jurajevič (½ smallholder); priest AMBROSIJ GLIHA coop. [~] — the 2nd priest of 1889 (Rauy absent!); Befunden ×3: the commune-Griblje announcement Oct 14, 1889 no. 26 + [G?upjäftigit-Knitt-Etbürning ~] + the Obschau-mündschaftliche Genehm. of the k.k. Bez.-Ger. Črnomelj Oct 7 Z: 8062 (the underage bride); 60 × 23 = 37 YEARS APART!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "87",
    bookSignature: "04455",
    year: 1889,
    scan: 76,
    page: 75,
    whatSi: "poroka (14. 10. 1889, vpis 8) — NEVESTA Margareth PERDINEC, ½ Gütlstochter, 23, GRIBLJE 87 (1. poročni dokaz h87 — NAJVIŠJA hiša poročne linije!; krstna 04105 že ×3; starši: MARCUS Perdinec, ⅓ Gütl. [nov ulomek], × Margareth Klejpec) × Johann Milek, ½ Gütl., 60, GRIBLJE 30; duhovnik Ambrosij Gliha coop. [~]; Befünden ×3 (zgłasnica št. 26 + sodna Genehm. Z: 8062); PERDINEC ×3 v 1889 — največja mreža leta!",
    whatEn: "marriage (Oct 14, 1889, entry 8) — the BRIDE Margareth PERDINEC, half smallholder's daughter, 23, GRIBLJE 87 (the 1st marriage evidence of h87 — THE HIGHEST house of the marriage line!; the baptism register 04105 already ×3; parents: MARCUS Perdinec, ⅓ smallholder [a new fraction], × Margareth Klejpec) × Johann Milek, half smallholder, 60, GRIBLJE 30; priest Ambrosij Gliha coop. [~]; Befunden ×3 (the announcement no. 26 + the court Genehm. Z: 8062); PERDINEC ×3 in 1889 — the year's biggest network!",
    status: "DOCUMENTED",
  },
  // ——— P119 razširitev: POROČNA KNJIGA 04455 — polno leto 1890 (skeni 77–79 ==
  // strani 76–78; velika glava »Traunungs=Buch« na Pag. 76; 16 vpisov =
  // NAJVEČJE LETO LINIJE! 1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16) —
  // vpisi z Griblji (3 poroke / 4 hiše: h91+h10 v1, h53 v6 NOVA, h61 v15):
  // h91 2. familia (krstna 1887 Novak/Kure!), h10 2. poročni dokaz (1887 v20),
  // h53 = NOVA hiša (1. dokaz sploh!), h61 2. familia (krstna 1887 Anton Muc —
  // anomalija A11 Muc-vs-Požek!); NOVELE: dvojni poročni vikend 23–24.11. ×4
  // (v13–v16!) + PREKRIŽANA POROKA HVALJ × HARASIMIČ (v13↔v16) + 2
  // sorodstveni dispensaciji (v11 3. st. bratranca Ord. Laibach № 1840 + v14
  // 4. st. № 2619!) + Zugelj bratski par (v10+v11 Dobravice 11, isti starši!)
  // + nevesta 45 (v5 Ana Agnič = rekord linije!) + simetrija 41=41 (v4) +
  // lomek 19¾ (v7) + Inwohnerin-nevesta (v3) + Vormund-v-očetovem-stolpcu
  // (v3) + Kürschner-poklic (v5) + Wirt-priča (v10) + ¾ Gütl (v14) + 4.
  // duhovnik MICHAEL BULOVEC pro t. deleg. Semič (v4!) + Ordinariat Laibach
  // številke ×3 (Z:132/№ 1840/№ 2619) + mladoletnost 6/16 = 37.5% (edino
  // mütterl. soglasje v2!) + zgłasnice 16/16 (Podzemelj ×8 + Gradac ×4 +
  // Griblje ×4; Griblje 1→16→36→39 + Gradac 11→16 časovno 1:1!) + Metlika
  // ×2 (Mößling 22+24!) + Pf. Borovnica migracija (v9 rojen Zavrh 41!);
  // mreže: PERDINEC/PEGDIREC ×8 + MARENTIČ ×5 + ŠURAJEVČIČ ×5 + ZUGELJ ×6 +
  // MUC ×5 + BRINEC ×4 + POŽEK ×5 + TOME ×5 + HRIŽAN ×5 + JAKŠA ×4 + STRAUS
  // ×4; faza-1 oris popravki ×12 (v13 »Haaspić/Wolf« → Cerkvišče 9/Hvalj! +
  // v16 »Nov 27/Kokoljič« → Nov 24/Harasimič!); glava 1891 = Pag. 79 = s80
  // (v1–4 orisani) = P120 LEAD. Dokaz: research/issue17/parish-marriage-
  // 1890.json; verifikator: scripts/p119_parish_marriage_1890.py --check
  // (I1–I11).
  {
    houseNo: "91",
    bookSignature: "04455",
    year: 1890,
    scan: 77,
    page: 76,
    whatSi: "poroka (27. 1. 1890, vpis 1) — ženin Johann MUC, ¼ Gütlar(s)sohn? [~] (+ »und Vgornjed?« [~]), 23, GRIBLJE 91 (2. familia v hiši po krstni 1887 Alojzija = Janez Novak × Ana Kure!; faza-1 oris »Nuc« = popravek → MUC po očetu Nicolaus Muc!; MUC-mreža: Janez Muc bajtar h61 + †1886 Nikolaj + v2 mati Katharina!) × Anna KURE, ¼ Gütl.Tochter und Magd (= »hči in dekla« — Kurrent »Wayd« = Magd, cf. P118 ×2!), 23, GRIBLJE 10 (2. poročni dokaz h10 po 1887 v20 Catharina Križe!; KURE ×3: nevesta + oče Marcus + krstna mati Ana Kure!); priče: Math. Japplič? [~] + Nicol. Zeliško? [~] (¼ Gribljah); duhovnik Jos. Rauy; Befünden: traut. zglasnica občine Griblje 11/1. 1890 st: 1 + [Grofsjäftig?-Knitt? ~] ×2 sodna ddo 19. + 22.1.1890 (Bez. Ger. Černomelj, f. Braut + f. Bräutigam!)",
    whatEn: "marriage (Jan 27, 1890, entry 1) — groom Johann MUC, quarter smallholder's son? [~] (+ »und Vgornjed?« [~]), 23, GRIBLJE 91 (the 2nd family in the house after the 1887 baptism of Alojzija = Janez Novak × Ana Kure!; the faza-1 outline »Nuc« = a correction → MUC after the father Nicolaus Muc!; the MUC network: Janez Muc cottager h61 + †1886 Nikolaj + the v2 bride's mother Katharina!) × Anna KURE, ¼ smallholder's daughter and MAID (Kurrent »Wayd« = Magd, cf. P118 ×2!), 23, GRIBLJE 10 (the 2nd marriage evidence of h10 after 1887 v20 Catharina Križe!; the KURE network ×3: the bride + father Marcus + the baptism mother Ana Kure!); witnesses: Math. Japplič? [~] + Nicol. Zeliško? [~] (¼ Gribljah); priest Jos. Rauy; Befunden: the traut. announcement of the Griblje commune Jan 11, 1890 no. 1 + [Grofsjäftig?-Knitt? ~] ×2 court docs ddo Jan 19 + 22, 1890 (Bez. Ger. Černomelj, for the bride + for the groom!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04455",
    year: 1890,
    scan: 77,
    page: 76,
    whatSi: "poroka (27. 1. 1890, vpis 1) — NEVESTA Anna KURE, ¼ Gütl.Tochter und Magd, 23, GRIBLJE 10 (2. poročni dokaz h10 po 1887 v20!; oče Marcus Kure ¼ × Anna Špala) × Johann Muc, ¼ Gütlar(s)sohn?, 23, GRIBLJE 91; duhovnik Jos. Rauy; Befünden: zglasnica Griblje 11/1. 1890 st: 1 + ×2 sodna Bez. Ger. Černomelj 19./22.1.; odprtje leta 1890 pod veliko glavo Traunungs=Buch (5. potrditev Pag. == sken − 1)",
    whatEn: "marriage (Jan 27, 1890, entry 1) — the BRIDE Anna KURE, quarter smallholder's daughter and maid, 23, GRIBLJE 10 (the 2nd marriage evidence of h10 after 1887 v20!; father Marcus Kure ¼ × Anna Špala) × Johann Muc, quarter smallholder's son?, 23, GRIBLJE 91; priest Jos. Rauy; Befunden: the announcement of Griblje Jan 11, 1890 no. 1 + ×2 court docs Bez. Ger. Černomelj Jan 19/22; the opening of 1890 under the big Traunungs=Buch header (the 5th confirmation of Pag. == scan − 1)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04455",
    year: 1890,
    scan: 77,
    page: 76,
    whatSi: "poroka (11. 5. 1890, vpis 6) — ženin Johann PERDINEC/PEGD. [~ — kurent variira, cf. 1888 »Pegdirec« ×9], ¼ [Gribljah], 51 LET (najstarejši Griblje-ženin 1890 — cf. 1887 Peter Križan 40!), GRIBLJE 53 (NOVA HIŠA — 1. dokaz sploh v vzorcu!) × Maria HRIŽAN, ¼ Gütlarstochter, 29, Otok 20 (HRIŽAN ×3: 1888 v9 + v4 mati + v12!; oče Peter Hrižan ¼ × Margareth Rižman? [~]); priče: Nic. Novak (½ Gribljah) + Anton Brodarič (½ Gribljah); duhovnik Jos. Rauy; Befünden: zglasnica občine Griblje 30. 4. 1890 št. 16; PERDINEC/PEGDIREC ×8 v 1890 — največja mreža leta (2 pisavi!)",
    whatEn: "marriage (May 11, 1890, entry 6) — groom Johann PERDINEC/PEGD. [~ — the Kurrent varies, cf. 1888 »Pegdirec« ×9], ¼ [Gribljah], 51 YEARS (the oldest Griblje groom of 1890 — cf. 1887 Peter Križan 40!), GRIBLJE 53 (A NEW HOUSE — the 1st evidence ever in the sample!) × Maria HRIŽAN, quarter smallholder's daughter, 29, Otok 20 (the HRIŽAN network ×3: 1888 v9 + the v4 mother + v12!; father Peter Hrižan ¼ × Margareth Rižman? [~]); witnesses: Nic. Novak (½ Gribljah) + Anton Brodarič (½ Gribljah); priest Jos. Rauy; Befunden: the announcement of the Griblje commune Apr 30, 1890 no. 16; PERDINEC/PEGDIREC ×8 in 1890 — the year's biggest network (2 spellings!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04455",
    year: 1890,
    scan: 79,
    page: 78,
    whatSi: "poroka (24. 11. 1890, vpis 15) — ženin Nicolaus POŽEK, ¼ [Gribljah], 29, GRIBLJE 61 (2. familia v hiši — krstna 1887 Anton = Janez Muc bajtar h61!; anomalija A11 Muc-vs-Požek: 2 familiji ali menjava najemnika!; POŽEK ×5 po 1889 ×3!) × Ana DRAGOŠ, ¼ Gütlarstochter, 26, Dragoše? 5 [~] (DRAGOŠ ×3: 1887 v17 + 1889 mati Barbara + 1890!; oče Nicolaus Dragoš ¼ × Catharina STRAUS — STRAUS ×4!); priče: Math. Straus (¼ Gribljah) + Joh. Pegdirec/Perdinec (¼ Gribljah); duhovnik Jos. Rauy; Befünden: zgłas. občine Griblje 24/11. 1890 št. 39 (Griblje številčenje 1→16→36→39 časovno 1:1!); BRINEC ×4 (mati Anna cf. 1887/1888!)",
    whatEn: "marriage (Nov 24, 1890, entry 15) — groom Nicolaus POŽEK, ¼ [Gribljah], 29, GRIBLJE 61 (the 2nd family in the house — the 1887 baptism of Anton = Janez Muc cottager h61!; the anomaly A11 Muc-vs-Požek: 2 families or a tenant change!; POŽEK ×5 after 1889 ×3!) × Ana DRAGOŠ, quarter smallholder's daughter, 26, Dragoše? 5 [~] (the DRAGOŠ network ×3: 1887 v17 + the 1889 mother Barbara + 1890!; father Nicolaus Dragoš ¼ × Catharina STRAUS — STRAUS ×4!); witnesses: Math. Straus (¼ Gribljah) + Joh. Pegdirec/Perdinec (¼ Gribljah); priest Jos. Rauy; Befunden: the announcement of the Griblje commune Nov 24, 1890 no. 39 (the Griblje numbering 1→16→36→39 chronological 1:1!); BRINEC ×4 (the mother Anna cf. 1887/1888!)",
    status: "DOCUMENTED",
  },
  // ——— P120 razširitev: POROČNA KNJIGA 04455 — polno leto 1891 (skeni 80–83 ==
  // strani 79–82; letna glava 1891 brez velike glave; 18 vpisov = 2. največje
  // leto: 1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18!) — vpisi z
  // Griblji (2 poroki / 2 hiši: h87 v6 2. DOKAZ po 1889 v8 + h20 v7 NOVA):
  // NOVELE: ROSETTA statusa »[Hofname]s. Sohn/Tochter« (v14 — razrešitev
  // skrivnostne končnice 1886–1890!) + deležni sistem imenja Griblje (½/¼ ×14
  // oseb!) + 1. VD-OVI POROKI LINIJE ×2 (v14 Šimonič geb. Konda 32 + v15 35!)
  // + 1. ŽANDAR + 1. HRVAŠKA (v15 Pintar rod. Dolenja Pušća 3 + 4 hrvaška
  // dokumenta + 2 Zagrebčana-priče!) + 1. APOSTOLSKA dispensacija (v11
  // bratranca 2. kanc. stopnje iste linije + Landesreg. Z:5672!) + PEZDIREC
  // ×12 oseb = rekord mreže! + dnevne gruče 26.1.×3 / 3.2.×3 / 21.+23.11.×4!
  // Dokaz: research/issue17/parish-marriage-1891.json; verifikator:
  // scripts/p120_parish_marriage_1891.py --check (I1–I11).
  {
    houseNo: "87",
    bookSignature: "04455",
    year: 1891,
    scan: 81,
    page: 80,
    whatSi: "poroka (3. 2. 1891, vpis 6) — ženin Marcus PEZDIREC, ¼ Griblers. Sohn, 29, GRIBLJE 87 (2. POROČNI DOKAZ h87 po 1889 v8 Milek×Klejpec — v 2 letih!; oče Marcus Pezdirec ½ Gribler × Margaret KLEPEC = 1889 nevesta Klejpec → Klepec-mreža h87!) × Anna ŽELJKO, ¼ Griblers. Toht.? [~], 20, GRIBLJE 60 (NOVA hiša poročnega vzorca — krstna 1886 poroka Maria Bohor!; ŽELJKO ×3 h1/h60/h91 cf. krstna 1887!); priče: Johann MILEK (1887 h23 + 1889 h30 mreža!) + Nicolaus Željko (} ¼ gbl. — brat neveste?); duhovnik Jos. Rauy; Befünden: zglasnica občine Griblje 23/1. 1891 št: 5 + mündl. väterl. Einwilligung f. d. mj. Braut; PEZDIREC ×12 = rekord mreže linije",
    whatEn: "marriage (Feb 3, 1891, entry 6) — groom Marcus PEZDIREC, quarter smallholder's son, 29, GRIBLJE 87 (the 2nd MARRIAGE EVIDENCE of h87 after 1889 v8 Milek×Klejpec — within 2 years!; father Marcus Pezdirec ½ Gribler × Margaret KLEPEC = the 1889 bride Klejpec → the Klepec network of h87!) × Anna ŽELJKO, quarter smallholder's daughter? [~], 20, GRIBLJE 60 (A NEW house of the marriage sample — the 1886 baptism marriage Maria Bohor!; ŽELJKO ×3 h1/h60/h91 cf. the 1887 baptism!); witnesses: Johann MILEK (the 1887 h23 + 1889 h30 network!) + Nicolaus Željko (} ¼ gbl. — the bride's brother?); priest Jos. Rauy; Befünden: the announcement of the Griblje commune Jan 23, 1891 no. 5 + the verbal paternal consent for the minor bride; PEZDIREC ×12 = the record network of the line",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04455",
    year: 1891,
    scan: 81,
    page: 80,
    whatSi: "poroka (3. 2. 1891, vpis 7) — ženin Peter PEZDIREC, ¼ Griblers. Sohn, 24, GRIBLJE 20 (NOVA HIŠA — 1. poročni dokaz sploh!; oče Peter Pezdirec ½ Gribler × Catharina Deblič? [~]; PEZDIREC ×2 ISTI DAN z v6 Marcus 29 — brata? [~]!) × Dorothea KLEPEC, ½ Griblers. Toht.? [~], 20, Krasinec 37 (KLEPEC ×2 isti dan z v6 mati Margaret!; oče Peter Klepec ½ Gribler × Anna Marasinič?); priče: Johan Marasinič + Anton Brodarič? [~] (} ½ gbl.); duhovnik Jos. Rauy; Befünden: zglasnica občine Griblje 2/2. 1891 st: 7 + mündl. väterl. Einwilligung f. d. mj. Braut; 3.2. = TROJNO poročni dan (v5+v6+v7!)",
    whatEn: "marriage (Feb 3, 1891, entry 7) — groom Peter PEZDIREC, quarter smallholder's son, 24, GRIBLJE 20 (A NEW HOUSE — the 1st marriage evidence ever!; father Peter Pezdirec ½ Gribler × Catharina Deblič? [~]; PEZDIREC ×2 the SAME DAY with v6 Marcus 29 — brothers? [~]!) × Dorothea KLEPEC, half smallholder's daughter? [~], 20, Krasinec 37 (KLEPEC ×2 the same day with the v6 mother Margaret!; father Peter Klepec ½ Gribler × Anna Marasinič?); witnesses: Johan Marasinič + Anton Brodarič? [~] (} ½ gbl.); priest Jos. Rauy; Befünden: the announcement of the Griblje commune Feb 2, 1891 no. 7 + the verbal paternal consent for the minor bride; Feb 3 = a TRIPLE wedding day (v5+v6+v7!)",
    status: "DOCUMENTED",
  },
  // ——— P123 razširitev: POROČNA KNJIGA 04455 — polno leto 1894 (skeni 91–93 ==
  // strani 90–92; VELIKA GLAVA »Traunungs=Buch« + rokopisno »1894« na s91 =
  // Pag. 90 POTRJENA — P123 lead!; 15 vpisov: 1886:7 → 1887:21 → 1888:20 →
  // 1889:10 → 1890:16 → 1891:18 → 1892:15 → 1893:20 → 1894:15; razpored 6+5+4)
  // — vpisi z Griblji (2 poroke / 4 poročna bloka: h27 v3 ženin × h42 v3
  // nevesta CERNIČ-hiša! + h9 v11 ženin × h11 v11 nevesta): NOVELE: ★ REKORD-PAR
  // VSEH ČASOV v5 (64+48 = 112 let skupaj!) + REKORD nevesta 56 (v1 Tasič!) +
  // ★ 1. PREČRTANI PRIČA linije (v12 Vojka→Justin zasebnik) + ★ PFARRAMT IDRIA
  // (v12 = najdaljši župnijski lok ~110 km!) + ★ VOJSKA Infanterie-Regiments-
  // Colonel №267 (v9 — ženin aktivni vojak!) + ★ DISPENS 3. stopnje №2680
  // (v14 ZUGELJ × TOME) + ★ LANDSREGIERUNG Laibach Ž8667 (v11 — 1. v liniji;
  // datirana 9/9. = 3 tedne PO poroki [~]!) + ENAČNOPRIIMEŠKI poroki ×2 (v3 +
  // v6 Tome×Tome) + ZURAJOVIČ očetovski cross-link 1893→1894 (Zemelj 18!) +
  // »1« namesto ulomka (v12 — 2. primer!) + občina Orašče [~] neznanka +
  // Laipšl-mreža 4. leto ×5 + PEZDIREC-cluster ×10 (3 pisave).
  // Dokaz: research/issue17/parish-marriage-1894.json; verifikator:
  // scripts/p123_parish_marriage_1894.py --check (I1–I11).
  {
    houseNo: "27",
    bookSignature: "04455",
    year: 1894,
    scan: 91,
    page: 90,
    whatSi: "poroka (5. 2. 1894, vpis 3) — ženin Marcus PERDINEC, ¼ Gribler, 33, GRIBLJE 27 (2. poročni dokaz h27; oče Marcus Perdinec ¼ Gribler × Margareth KLEPSEC) × Margareth PERDINEC, ¼ Griblers=tochter + Ans. [~], 27, GRIBLJE 42 (CERNIČ-hiša P117 v6+v16 — 3. dokaz hiše, 1. poročni!; oče Georg Perdinec ¼ Gribler × Catharina MARASINIČ) — ★ ENAČNOPRIIMEŠKA POROKA Perdinec × Perdinec (različna starša — bratranci/sorojenci? [~]); priče: Marcus Hlebec + Michael Segina (} ¼ gbl. — cf. P122 v3 ženin Peter Segina!); duhovnik Jos. Rauy (»M.!« [~]); Befünden: zemljšov. zglašnica občine Griblje od 4. februarja št: 1",
    whatEn: "marriage (Feb 5, 1894, entry 3) — groom Marcus PERDINEC, quarter smallholder, 33, GRIBLJE 27 (the 2nd marriage evidence of h27; father Marcus Perdinec quarter smallholder × Margareth KLEPSEC) × Margareth PERDINEC, quarter smallholder's daughter + Ans. [~], 27, GRIBLJE 42 (the CERNIČ house of P117 v6+v16 — the 3rd house evidence, the 1st marriage one!; father Georg Perdinec quarter smallholder × Catharina MARASINIČ) — ★ the SAME-SURNAME MARRIAGE Perdinec × Perdinec (different parents — cousins/siblings? [~]); witnesses: Marcus Hlebec + Michael Segina (} ¼ gbl. — cf. P122 v3 groom Peter Segina!); priest Jos. Rauy (»M.!« [~]); Befünden: the land registry certificate of the Griblje commune from Feb 4 no. 1",
    status: "DOCUMENTED",
  },
  {
    houseNo: "42",
    bookSignature: "04455",
    year: 1894,
    scan: 91,
    page: 90,
    whatSi: "poroka (5. 2. 1894, vpis 3) — nevesta Margareth PERDINEC, ¼ Griblers=tochter + Ans. [~], 27, GRIBLJE 42 (CERNIČ-hiša: P117 v6+v16 sestre ČERNIČ obe h42! — 3. dokaz h42, 1. POROČNI; h42 = Perdinec-gospodinjstvo 1894) × Marcus PERDINEC, ¼ Gribler, 33, GRIBLJE 27 (enačnopriimeška poroka!); oče Georg Perdinec ¼ Gribler × Catharina MARASINIČ (MARASINIČ cf. P121 v2+v3 sestrski dvozakon!); duhovnik Jos. Rauy (»M.!« [~]); Befünden: zglašnica občine GRIBLJE 4. 2. št: 1",
    whatEn: "marriage (Feb 5, 1894, entry 3) — bride Margareth PERDINEC, quarter smallholder's daughter + Ans. [~], 27, GRIBLJE 42 (the CERNIČ house: P117 v6+v16 the ČERNIČ sisters both h42! — the 3rd h42 evidence, the 1st MARRIAGE one; h42 = the Perdinec household in 1894) × Marcus PERDINEC, quarter smallholder, 33, GRIBLJE 27 (the same-surname marriage!); father Georg Perdinec quarter smallholder × Catharina MARASINIČ (MARASINIČ cf. P121 v2+v3 the sister double-wedding!); Befünden: the certificate of the GRIBLJE commune Feb 4 no. 1",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04455",
    year: 1894,
    scan: 92,
    page: 91,
    whatSi: "poroka (19. 8. 1894, vpis 11) — ženin Georg JAKOBČIČ, ¼ Gribler, 22 (mladoleten!), GRIBLJE 9 (2. poročni dokaz h9; oče Johann Jakobčič ½ Gribler × Maria JAKOBČIČ) × Maria ZURNIČ [~], ½ Griblers=tochter, 25, GRIBLJE 11 (oče Mathias Zurnič [~] ½ Gribler × Catharina DRAGOŠ); ★ 1. LANDSREGIERUNG-dokument poročne linije: »amtliche Genehmigung von der k.k. Landesregierung in Laibach vom 9/9. 1894 Ž 8667« [~ — datirana 3 TEDNE PO poroki — retro-vpis?] + Großjährigkeitserklärung ženina Bez.Ger. Črnomelj 9.8. №5642 (10 dni pred!); priče: Nicol. Požek (cf. P118!) + Johann Dragoš (} ¼ gbl.); duhovnik Jos. Rauy; Befünden: zglašnica občine Gribelj-ske od 13/8. 94 št: 1; ob robu tiskar »Laibach. Druck u. Verlag v. Möttling.«!",
    whatEn: "marriage (Aug 19, 1894, entry 11) — groom Georg JAKOBČIČ, quarter smallholder, 22 (a minor!), GRIBLJE 9 (the 2nd marriage evidence of h9; father Johann Jakobčič half smallholder × Maria JAKOBČIČ) × Maria ZURNIČ [~], half smallholder's daughter, 25, GRIBLJE 11 (father Mathias Zurnič [~] half smallholder × Catharina DRAGOŠ); ★ the 1st LANDSREGIERUNG document of the marriage line: »the official approval of the k.k. Landesregierung in Laibach from Sep 9, 1894 Ž 8667« [~ — dated 3 WEEKS AFTER the wedding — a retro-entry?] + the groom's coming-of-age declaration Bez.Ger. Črnomelj Aug 9 №5642 (10 days before!); witnesses: Nicol. Požek (cf. P118!) + Johann Dragoš (} ¼ gbl.); priest Jos. Rauy; Befünden: the certificate of the Gribelj-ske commune from Aug 13, 94 no. 1; the printer »Laibach. Druck u. Verlag v. Möttling.« at the page edge!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04455",
    year: 1894,
    scan: 92,
    page: 91,
    whatSi: "poroka (19. 8. 1894, vpis 11) — nevesta Maria ZURNIČ [~], ½ Griblers=tochter, 25, GRIBLJE 11 (2. poročni dokaz h11; h11 = Zurnič-gospodinjstvo 1894) × Georg JAKOBČIČ, ¼ Gribler, 22 (mladoleten), GRIBLJE 9 (2. GRIBLJE poroka 1894 — h9 × h11!); oče Mathias Zurnič [~] ½ Gribler × Catharina DRAGOŠ (DRAGOŠ cf. P117 Jaklič-mreža!); ★ Landesregierung Laibach Ž8667 (1. v liniji!); duhovnik Jos. Rauy; Befünden: zglašnica občine Gribelj-ske 13/8. 94 št: 1",
    whatEn: "marriage (Aug 19, 1894, entry 11) — bride Maria ZURNIČ [~], half smallholder's daughter, 25, GRIBLJE 11 (the 2nd marriage evidence of h11; h11 = the Zurnič household in 1894) × Georg JAKOBČIČ, quarter smallholder, 22 (a minor), GRIBLJE 9 (the 2nd GRIBLJE marriage of 1894 — h9 × h11!); father Mathias Zurnič [~] half smallholder × Catharina DRAGOŠ (DRAGOŠ cf. the P117 Jaklič network!); ★ the Landesregierung Laibach Ž8667 (the 1st in the line!); Befünden: the certificate of the Gribelj-ske commune Aug 13, 94 no. 1",
    status: "DOCUMENTED",
  },
  // ——— P124 razširitev: POROČNA KNJIGA 04455 — polno leto 1895 (skeni 94–96 ==
  // strani 93–95; Pag. == sken − 1, 10. potrditev; velja v 61–96). VELIKA GLAVA
  // »Trauungs=Buch« + rokopisno »1895« na s94 (P124 lead POTRJEN).
  // 16 vpisov (1886:7 → … → 1893:20 → 1894:15 → 1895:16; razpored 6+5+5) —
  // vpisi z Griblji (3 poroke / 3 poročni bloki: h16 v10 ženin NOVA HIŠA +
  // h27 v11 ženin 3. poročni dokaz + h52 v13 ženin NOVA v PT-luknji 41–60!):
  // NOVELE: ★ 1. ČASTNIK linije — Oberleutnant Stal + priča k.k. Hauptmann +
  // Garnisons-Propstei Metlika (v15) + ★ 1. hrvaški dokumenti (v6: in Croalien
  // + smrtni list dekanate v Lipniku [~] + Broj 485 občine Griblje!) + ★
  // POPRAVEK STAROSTI 40→54 (v6 vdovec!) + ★ DISPENS-REKORD ×4 (v7 №504 3. st.
  // krvno + v8 №613 2. st. svarstvo + v12 Ž/L:4994 »Wittwenschaft« [~] — PO
  // poroki! + v16 3.[u2.?] lineae collateralis) + ★ 2. LANDSREGIERUNG Laibach
  // №181 (v8) + ★ »Möttling« = nemško ime METLIKE (Bez. Ger. ×4!) + ★ homonima
  // Marcus Perdinec (v11 ≠ P123 v3) + Johann Starasinič (v8 ≠ v14) + ★ dva
  // priča isto ime Peter Jakofčič ×2 (v4!) + ZUGELJ ×3 + MAYD ×2 + Großjährig-
  // keits-Erklärung ×3 + formula »in Ungarn … Närnk« [~] ×4 + Kralj ×6 +
  // Marentič ×5 + Jakša ×5 + Rauy 16/16 (»M.!« ×7).
  // Dokaz: research/issue17/parish-marriage-1895.json; verifikator:
  // scripts/p124_parish_marriage_1895.py --check (I1–I11).
  {
    houseNo: "16",
    bookSignature: "04455",
    year: 1895,
    scan: 95,
    page: 94,
    whatSi: "poroka (19. 5. 1895, vpis 10) — ženin Anton BRODARIČ, ½ Griblar, 35, GRIBLJE 16 (NOVA HIŠA vzorca! — h16 že v mrliškem vzorcu 1886; oče Michaël Brodarič ½ Griblar × Anna ADAM) × Anna HARASINIČ, ½ Griblarjstochter [~], 25, Krasinec 23 (oče Mathias Harasinič ½ Griblar × Anna Harasinič — oče in mati ISTI PRIIMEK!); priče: Johan Brodarič (Pofn- [~] — hišni vzdevek, cf. P123 Valur/Pofn!) + Michael Harasinič (} ½ gbl.); duhovnik Jos. Rauy; Befünden: zemljšov. zglašnica občine Griblje od 18/5. 1895 №: 1 (1. od DVEH zaporednih dokumentov občine Griblje isti dan — cf. v11 št: 2!)",
    whatEn: "marriage (May 19, 1895, entry 10) — groom Anton BRODARIČ, half smallholder, 35, GRIBLJE 16 (a NEW house of the sample! — h16 already in the 1886 death sample; father Michaël Brodarič half smallholder × Anna ADAM) × Anna HARASINIČ, half smallholder's daughter [~], 25, Krasinec 23 (father Mathias Harasinič half smallholder × Anna Harasinič — father and mother the SAME SURNAME!); witnesses: Johan Brodarič (Pofn- [~] — house nickname, cf. P123 Valur/Pofn!) + Michael Harasinič (} ½ gbl.); priest Jos. Rauy; Befünden: the land registry certificate of the Griblje commune from May 18, 1895 no. 1 (the 1st of TWO consecutive Griblje-commune documents the same day — cf. v11 no. 2!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04455",
    year: 1895,
    scan: 95,
    page: 94,
    whatSi: "poroka (19. 5. 1895, vpis 11) — ženin Marcus PERDINEC, ½ Griblar, 34, GRIBLJE 27 (3. poročni dokaz h27!; oče Marcus Perdinec ¼ Griblar × Margareth KLEPEC) × Catharina ZUGELJ, ¼ Griblarjš. + »Aleffon« [~ — hišni vzdevek?], 25, Otok 22 (oče Michaël Zugelj ¼ Griblar × Catharina Kramarič); ★ HOMONIM: ta Marcus Perdinec (f. Marcus, ½ Griblar) ≠ P123 v3 Marcus Perdinec (f. Michaël, 33, ¼ Gribler × Margareth PERDINEC) — dva različna moška z istim imenom in ISTO HIŠO 27!; ZUGELJ ×3 v letu (cf. v8 nevesta »geb. Zugelj«!); priče: Johan Jurajevič + Nikol. Križan (} ½ gbl.); duhovnik Jos. Rauy (»M.!« [~]); Befünden: zglašnica občine Griblje dado 18/5. 1895 št: 2",
    whatEn: "marriage (May 19, 1895, entry 11) — groom Marcus PERDINEC, half smallholder, 34, GRIBLJE 27 (the 3rd marriage evidence of h27!; father Marcus Perdinec quarter smallholder × Margareth KLEPEC) × Catharina ZUGELJ, quarter smallholder's + »Aleffon« [~ — house nickname?], 25, Otok 22 (father Michaël Zugelj quarter smallholder × Catharina Kramarič); ★ HOMONYM: this Marcus Perdinec (f. Marcus, ½ smallholder) ≠ the P123 v3 Marcus Perdinec (f. Michaël, 33, ¼ smallholder × Margareth PERDINEC) — two different men with the same name and the SAME HOUSE 27!; ZUGELJ ×3 in the year (cf. v8 bride »geb. Zugelj«!); witnesses: Johan Jurajevič + Nikol. Križan (} ½ gbl.); priest Jos. Rauy (»M.!« [~]); Befünden: the certificate of the Griblje commune dated May 18, 1895 no. 2",
    status: "DOCUMENTED",
  },
  {
    houseNo: "52",
    bookSignature: "04455",
    year: 1895,
    scan: 96,
    page: 95,
    whatSi: "poroka (26. 5. 1895, vpis 13) — ženin Mathias PERDINEC, ½ Griblarjsohn [~], 26, GRIBLJE 52 (NOVA HIŠA vzorca — v PT-luknji 41–60!; oče Johann Perdinec ½ Griblar × Maria Novak) × Anna JAKOBIČ, ½ gbl + »Žugffan« [~ — hišni vzdevek?], 21, Cerkvišče 26 (oče Nicolaus Jakobič ½ Griblar × Anna Mušič); PERDINEC ×2 v letu 1895 (v11 f. Marcus + v13 f. Johann — dve veji!); kratka vrstica formularja (575–700); priče: Nicol. Novak + Math. Jakobič (} ¼ gbl [~]); duhovnik Jos. Rauy (»M.!« [~]); Befünden: zglašnica občine Griblje od 20/5. 95 št: 3 + mündl. väterl. fürwellig für die ml. Braut in Ungarn ward [~] obigen šti. Närnk [~]",
    whatEn: "marriage (May 26, 1895, entry 13) — groom Mathias PERDINEC, half smallholder's son [~], 26, GRIBLJE 52 (a NEW house of the sample — in the PT gap 41–60!; father Johann Perdinec half smallholder × Maria Novak) × Anna JAKOBIČ, ½ smallholder + »Žugffan« [~ — house nickname?], 21, Cerkvišče 26 (father Nicolaus Jakobič half smallholder × Anna Mušič); PERDINEC ×2 in the year 1895 (v11 f. Marcus + v13 f. Johann — two branches!); a short form row (575–700); witnesses: Nicol. Novak + Math. Jakobič (} ¼ gbl [~]); priest Jos. Rauy (»M.!« [~]); Befünden: the certificate of the Griblje commune from May 20, 95 no. 3 + mündl. väterl. fürwellig für die ml. Braut in Ungarn ward [~] obigen šti. Närnk [~]",
    status: "DOCUMENTED",
  },
  // ——— P125 razširitev: POROČNA KNJIGA 04455 — dopolnitev 1895 (s97 = Pag. 96:
  // v17–v19!) + polno leto 1896 (s98–s101 == Pag. 97–100; Pag. == sken − 1,
  // 11. potrditev; velja v 61–100). ROKOPISNA GLAVA »1896.« na s98 POTRJENA +
  // rokopisna glava »1897« + v1/1897 ŽE na s101 (P126 lead!).
  // 1895 = 19 vpisov (16 P124 + 3 P125 ext: okt 29 + nov 10 + nov 28!);
  // 1896 = 15 vpisov (razpored feb 5 + apr 1 + maj 4 + avg 2 + okt 2 + nov 1).
  // NOVELE: ★ ⅓ GRIBLAR = NOV ULOMEK LINIJE (v6 Kolih + v10 Jakofčič — oče+sin
  // oba ⅓!) + 1 GRIBLAR (v2) + ★ 1. NEZAKONSKI ŽENIN POROČNE LINIJE (v14:
  // starši [—] + »ledige Magd«!) + ★ 3. duhovnik linije Franz Herms coop.
  // (v12 — edina prekinitev Rauy-monopola 17/18!) + ★ 2. ŽANDAR (v4 Eduard
  // (Hubert [~]) Röthl) + k.k. Beamte oče (1.!) + Rudolfswert/Gottschee/
  // Adelsberg/Laibach + »Indifferenz« + ★ ŽAKANJE = HRVAŠKA (v11 — slovensko
  // »otlični list«!) + ★ »hoc« = hic commorans REŠEN ×7 + ★ mütterl. fürwellig
  // (v7 — 1. MATICA!) + »in Ungarn« ×4 (isti števec kot P124!) + GROSSJÄHRIGKEIT
  // za ženina (v3 — 1.!) + DISPENS №2906 (v17-1895) + №293 (v3) + ★ MUC 3.
  // dokaz (v1 oče = P121 v12 ISTA!) + ★ 2. REKORD-PAR (v18-1895: 59+50 = 109!)
  // + občinske kontinuitete Griblje št:4 / Gradac 21→22→23 / Podzemelj 4→121[~]
  // + h14 CROSS-LINK (v17 par = krstna 1896 ISTI PAR!).
  // GRIBLJE: 2 poroke / 3 poročna bloka (h24 + h14 NOVA poročna × h18 NOVA!).
  // Dokaz: research/issue17/parish-marriage-1896.json; verifikator:
  // scripts/p125_parish_marriage_1896.py --check (I1–I11).
  {
    houseNo: "24",
    bookSignature: "04455",
    year: 1895,
    scan: 97,
    page: 96,
    whatSi: "poroka (29. 10. 1895, vpis 17 — DOPOLNITEV P124: 1895 ima 19 vpisov!) — ženin Johann BRINSEC [~ Brinec], ½ Griblarš Sohn [~], 33, GRIBLJE 24 (1. POROČNI DOKAZ h24 — krstna 1887–1893 gosta = Brinec × Jakobec familija!; oče Peter Brinsec ½ Griblar × Anna STRAOS [~]) × Maria PERDINEC [~ Pexdinec], ½ Gbl. Tojfter [~], 28, GRIBLJE 14 (oče Michaël Perdinec ¼ Griblar × Anna Brinsec — OBE MATI/NEVESTA BRINSEC = sorodstvo!); ★ GRIBLJE × GRIBLJE (h24 × h14) + ★ DISPENS №2906: 3. stopnja krvnega sorodstva lineae collat. 2ti gradus [~], f.b. Ordinariat Laibach 7/10. 1895 (3 tedna pred poroko!); ★ h14 CROSS-LINK: ISTI PAR kot krstna 04105 s85 h14 1896 (oče Janez Brinec × mati Marija Pendirec) — ženin oženj v nevestino hišo (vzorec h56-1886!); občina Griblje št: 4 = ZAPOREDNA kontinuiteta (P124 št:1-3 maj → št:4 okt!); priče: Mathias Sakljič [~] + Mathias Brinsec (obe imeni v ISTI celici!) + gändlbr [~] ¼ Griblar; duhovnik Jos. Rauy",
    whatEn: "marriage (Oct 29, 1895, entry 17 — the P124 SUPPLEMENT: 1895 has 19 entries!) — groom Johann BRINSEC [~ Brinec], half smallholder's son [~], 33, GRIBLJE 24 (the 1st MARRIAGE evidence of h24 — the baptisms 1887–1893 host = the Brinec × Jakobec family!; father Peter Brinsec half smallholder × Anna STRAOS [~]) × Maria PERDINEC [~ Pexdinec], half smallholder's daughter [~], 28, GRIBLJE 14 (father Michaël Perdinec quarter smallholder × Anna Brinsec — BOTH the mother/bride BRINSEC = kinship!); ★ GRIBLJE × GRIBLJE (h24 × h14) + ★ DISPENSATION №2906: the 3rd degree of consanguinity lineae collat. 2ti gradus [~], the f.b. Ordinariat Laibach Oct 7, 1895 (3 weeks before the wedding!); ★ the h14 CROSS-LINK: the SAME couple as the baptism 04105 s85 h14 1896 (father Janez Brinec × mother Marija Pendirec) — the groom married INTO the bride's house (the h56-1886 pattern!); the Griblje commune no. 4 = a SEQUENTIAL continuity (the P124 nos. 1-3 May → no. 4 Oct!); witnesses: Mathias Sakljič [~] + Mathias Brinsec (both names in the SAME cell!) + gändlbr [~] quarter smallholder; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04455",
    year: 1895,
    scan: 97,
    page: 96,
    whatSi: "poroka (29. 10. 1895, vpis 17) — nevesta Maria PERDINEC [~], ½ Gbl. Tojfter [~], 28, GRIBLJE 14 (1. POROČNI DOKAZ h14 — krstna 1896 h14 NOVA HIŠA vzorca!; oče Michaël Perdinec ¼ Griblar × Anna BRINSEC) × Johann BRINSEC [~], ½ Griblarš Sohn [~], 33, GRIBLJE 24 (drubel poroka — oba bloka!); ★ KRSTNI CROSS-LINK 1896: h14 krst (04105 s85) = oče Janez Brinec × mati Marija Pendirec = ISTI PAR — 1. otrok h14 po poroki!; dispens №2906 (3. st. krvno — mati neveste Anna Brinsec × ženinova familija Brinec h24!); duhovnik Jos. Rauy",
    whatEn: "marriage (Oct 29, 1895, entry 17) — bride Maria PERDINEC [~], half smallholder's daughter [~], 28, GRIBLJE 14 (the 1st MARRIAGE evidence of h14 — the baptism 1896 h14 NEW HOUSE of the sample!; father Michaël Perdinec quarter smallholder × Anna BRINSEC) × Johann BRINSEC [~], half smallholder's son [~], 33, GRIBLJE 24 (a double-Griblje marriage — both blocks!); ★ THE BAPTISM CROSS-LINK 1896: the h14 baptism (04105 s85) = father Janez Brinec × mother Marija Pendirec = the SAME couple — the 1st child of h14 after the wedding!; dispensation №2906 (3rd degree consanguinity — the bride's mother Anna Brinsec × the groom's Brinec family h24!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04455",
    year: 1896,
    scan: 101,
    page: 100,
    whatSi: "poroka (23. 11. 1896, vpis 15) — nevesta Catharina KLOBUČAR [~], ½ Griblaršdojft. + hoc [hic commorans], 21 (mladoletna — GROSSJÄHRIGKEITS-ERKÄRUNG vom k.k. Bez.G. Črnomelj 12/11. 1896 ko 8364 [~]!), GRIBLJE 18 (1. POROČNI DOKAZ h18 — krstna 1898 h18 NOVA ŠTEVILKA (Matija Šimec × Ana Kukar — IZMENA gospodinjstva?!); oče Johann Klobučar ¼ Griblar × Barbara PERDINEC) × Johann BERKOVEC [~], ½ Griblarššohn [~], 28, Lomelj [~] 14 (oče Marcus Berkovec ½ Griblar × Catharina KLEPEC — KLEPEC ×3 v letu!); edina GRIBLJE poroka 1896; priče: Peter Perdinec + Juri(j) Klepec (} ½ Gbl.); duhovnik Jos. Rauy (»M.!« [~]); Befünden: zglašnica občine Podzemelj nov. 1896 št: 121 [~]",
    whatEn: "marriage (Nov 23, 1896, entry 15) — bride Catharina KLOBUČAR [~], half smallholder's daughter + hoc [hic commorans], 21 (a minor — the COMING-OF-AGE DECLARATION of the k.k. district court Črnomelj Nov 12, 1896 ko 8364 [~]!), GRIBLJE 18 (the 1st MARRIAGE evidence of h18 — the baptism 1898 h18 A NEW NUMBER (Matija Šimec × Ana Kukar — a HOUSEHOLD CHANGE?!); father Johann Klobučar quarter smallholder × Barbara PERDINEC) × Johann BERKOVEC [~], half smallholder's son [~], 28, Lomelj [~] 14 (father Marcus Berkovec half smallholder × Catharina KLEPEC — KLEPEC ×3 in the year!); the only GRIBLJE marriage of 1896; witnesses: Peter Perdinec + Juri(j) Klepec (} ½ Gbl.); priest Jos. Rauy (»M.!« [~]); Befünden: the certificate of the Podzemelj commune Nov 1896 no. 121 [~]",
    status: "DOCUMENTED",
  },
  // ——— P126 razširitev: POROČNA KNJIGA 04455 — polno leto 1897 (s101–s104 ==
  // Pag. 100–103; Pag. == sken − 1, 12. potrditev; velja v 61–104). Rokopisna
  // glava »1897« na s101 + rokopisna glava »1898.« + v1/1898 ŽE na s104
  // (P127 lead!). 1897 = 18 vpisov (razpored jan 1 + feb 8 + maj 2 + jul 2 +
  // avg 2 + okt 2 + nov 1; 15.2. ×5 = 2. največji dan linije!).
  // NOVELE: ★ GRIBLJE poroke ×5 = REKORD LINIJE (prej 3 P121!) + ★ 2.
  // prekinitev Rauy-monopola: v1 Johann Hofstetter [~], Dechant? in
  // ADELSBERG, per deleg. (poroka verjetno v Postojni — nevestin oče k.k.
  // pension. Förster!) + ★ 1. FOTOGRAF-PRIČA (v1 Pfüllkojf? [~] Photograph!)
  // + ★ MEGA CROSS-LINK v10: Mathias Simec h18 × Anna Kuchar h27 = PAR iz
  // krstne 04105 1898 h18 (»izmena gospodinjstva« P125 bloka REŠENA!) + ★
  // DVOJNA SODNA POLNOLETNOST (v15: Rudolfovo 23/8. + Metlika 22/8.!) + ★
  // SAMSKI LIST (v16: »Upričevalo samskiga stana«, Dragatus 23/9. št:405!) +
  // ★ NADOARSTVENO dovoljenje (v12 Metlika 1/7. št:103 — slov. Vormundschaft)
  // + ★ SLOVENSKA sodna polnoletnost (v5 Črnomelj Ž:1307) + ★ 1. MÜTTERLICH
  // sodna privolitev (v10 Ž:3791) + ★ »in Ungarn« ×8 = REKORD (v6/v7/v8/
  // v11-ženin/v14/v16-ženin/v17 + v4[~]) + ženin 55½ NEZAKONSKI (v3 — 2.
  // nezakonski ženin, mati ledig.!) + DVOJNI status (v13 »½ gbl. Sohn und
  // Zimmermann«) + DVA ženina h40 (v9 Brodarič + v11 Predanic — A6!) +
  // Predanic/Perdinec varianta (v11!) + občinske vrste: Podzemelj 1→2–6
  // (MEŠANI vrstni red 12/2.!)→9→10 | Griblje 1→2→3→4 POPOLNA | Gradac
  // 26→8?[~]→27 (A5) | Smihel? Škofjič? 46.
  // GRIBLJE: 5 porok / 9 poročnih blokov (h8 NOVA + h40 ×2 NOVA + h29 NOVA +
  // h18 2. dokaz MEGA + h27 + h39 NOVA + h33 NOVA + h28 NOVA).
  // Dokaz: research/issue17/parish-marriage-1897.json; verifikator:
  // scripts/p126_parish_marriage_1897.py --check (I1–I11).
  {
    houseNo: "8",
    bookSignature: "04455",
    year: 1897,
    scan: 102,
    page: 101,
    whatSi: "poroka (15. 2. 1897, vpis 5 — 1. od 5 porok 15.2. = 2. največji dan linije!) — nevesta Maria JAKOBČIČ [~], ⅓? Griblarš-toyftn [~], 23, GRIBLJE 8 (1. POROČNI DOKAZ h8 — Jakobčič-hiša!; oče Johann Jakobčič ¼ Griblar × Anna BRODARIČ) × Nicolaus Zupanič [~], ⅓? Griblarš-Jofn [~], 31, Krasinec 18 (oče Mathias Zupanič ½? Griblar [~] × Catharina STARASINIČ — cf. P124!); ★ 1. GRIBLJE poroka 1897 (REKORD-leto!); ★ SLOVENSKA sodna polnoletnost: »Ml. nevesta pol. veljetna sprozana od c.k. okr. sodisča v Črnomlju? z dnom 6. febr. 1897. Ž:1307«; priče Georg Štarasinič? + Johan Brodarič (obe ⅓ gbl [~]); duhovnik Jos. Rauy; Befünden: zglasmica občine Podzemelj od 12/2. št:3",
    whatEn: "marriage (Feb 15, 1897, entry 5 — the 1st of 5 weddings on Feb 15 = the 2nd largest day of the line!) — bride Maria JAKOBČIČ [~], ⅓? smallholder's daughter [~], 23, GRIBLJE 8 (the 1st MARRIAGE evidence of h8 — the Jakobčič house!; father Johann Jakobčič quarter smallholder × Anna BRODARIČ) × Nicolaus Zupanič [~], ⅓? smallholder's son [~], 31, Krasinec 18 (father Mathias Zupanič ½? smallholder [~] × Catharina STARASINIČ — cf. P124!); ★ the 1st GRIBLJE marriage of 1897 (the RECORD year!); ★ the SLOVENE coming-of-age: »Ml. nevesta pol. veljetna sprozana od c.k. okr. sodisča v Črnomlju? z dnom 6. febr. 1897. Ž:1307«; witnesses Georg Štarasinič? + Johan Brodarič (both ⅓ gbl [~]); priest Jos. Rauy; Befünden: the Podzemelj commune certificate Feb 12 no. 3",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04455",
    year: 1897,
    scan: 102,
    page: 101,
    whatSi: "poroka (22. 2. 1897, vpis 9) — ženin Nicolaus BRODARIČ, ½ Griblar, 31, GRIBLJE 40 (1. POROČNI DOKAZ h40; oče Anton Brodarič ½ Griblar × Barbara PERDINEC) × Maria MILEK, ½ Griblarš-tojš? [~], 24, GRIBLJE 29 (1. POROČNI DOKAZ h29; oče Peter Milek ½ Griblar × Anna KRIŽAN); ★ GRIBLJE × GRIBLJE (h40 × h29) + ★ A6: h40 ima ŠE drugega ženina istega leta (v11 Predanic!); priče Nicolaus Željko? [~ — cf. P120 ŽELJKO-hiša!] + Mathias Brinec (½ göbl); duhovnik Jos. Rauy; Befünden: zglasmica občine GRIBLJE od 20/2. štev:1 (1. Griblje zglasmica 1897!)",
    whatEn: "marriage (Feb 22, 1897, entry 9) — groom Nicolaus BRODARIČ, half smallholder, 31, GRIBLJE 40 (the 1st MARRIAGE evidence of h40; father Anton Brodarič half smallholder × Barbara PERDINEC) × Maria MILEK, half smallholder's daughter? [~], 24, GRIBLJE 29 (the 1st MARRIAGE evidence of h29; father Peter Milek half smallholder × Anna KRIŽAN); ★ GRIBLJE × GRIBLJE (h40 × h29) + ★ A6: h40 has ANOTHER groom the same year (v11 Predanic!); witnesses Nicolaus Željko? [~ — cf. the P120 ŽELJKO house!] + Mathias Brinec (½ göbl); priest Jos. Rauy; Befünden: the GRIBLJE commune certificate Feb 20 no:1 (the 1st Griblje certificate of 1897!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04455",
    year: 1897,
    scan: 102,
    page: 101,
    whatSi: "poroka (22. 2. 1897, vpis 9) — nevesta Maria MILEK, ½ Griblarš-tojš? [~], 24, GRIBLJE 29 (1. POROČNI DOKAZ h29; oče Peter Milek ½ Griblar × Anna KRIŽAN — KRIŽAN cf. v8/v10!) × Nicolaus BRODARIČ, ½ Griblar, 31, GRIBLJE 40 (drubel poroka — oba bloka!); ★ 2. GRIBLJE poroka 1897; Milek cf. v7 mati ženina + v17 mati neveste (×3 leta!); duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 22, 1897, entry 9) — bride Maria MILEK, half smallholder's daughter? [~], 24, GRIBLJE 29 (the 1st MARRIAGE evidence of h29; father Peter Milek half smallholder × Anna KRIŽAN — KRIŽAN cf. v8/v10!) × Nicolaus BRODARIČ, half smallholder, 31, GRIBLJE 40 (a double-Griblje marriage — both blocks!); ★ the 2nd GRIBLJE marriage of 1897; Milek cf. the v7 groom's mother + the v17 bride's mother (×3 in the year!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04455",
    year: 1897,
    scan: 102,
    page: 101,
    whatSi: "poroka (31. 5. 1897, vpis 10) — ženin Mathias SIMEC, ½ Griblar, 23, GRIBLJE 18 (2. POROČNI DOKAZ h18 — MEGA CROSS-LINK: par iz krstne 04105 1898 h18 (oče Matija Šimec × mati Ana Kukar) = TOČNO TA PAR — »izmena gospodinjstva« iz P125 bloka h18 REŠENA: Klobučar-hči se 1896 poroči ven (Berkovec), Simec×Kuchar preživi h18 od 1897!; oče Georg Simec ¼? Griblar [~] × Theresia KLEPEC) × Anna KUCHAR [~ Kučar], ½ Griblarš-tojštno, 16 (MLADOLETNA!; oče Jacob Kuchar ½? Griblar [~] × Anna KRIŽAN); ★ GRIBLJE × GRIBLJE (h18 × h27); ★ 1. MÜTTERLICH sodna privolitev linije: »mütterlich fürwillig für mj. Braut vom k.k. Bez. Ger. Črnomelj ddto 7/5.1897 Ž:3791« + väterl. mündl. für Bräutigam; priče Mathias Klepec + Johann Perdinec (½ göbl); duhovnik Jos. Rauy; Befünden: zglasmica občine Griblje od 30/5. št:3",
    whatEn: "marriage (May 31, 1897, entry 10) — groom Mathias SIMEC, half smallholder, 23, GRIBLJE 18 (the 2nd MARRIAGE evidence of h18 — MEGA CROSS-LINK: the couple from the 1898 baptism 04105 h18 (father Matija Šimec × mother Ana Kukar) = EXACTLY THIS COUPLE — the »household change« from the P125 h18 block SOLVED: the Klobučar daughter married out 1896 (Berkovec), Simec×Kuchar occupy h18 from 1897!; father Georg Simec ¼? smallholder [~] × Theresia KLEPEC) × Anna KUCHAR [~ Kučar], half smallholder's daughter, 16 (A MINOR!; father Jacob Kuchar ½? smallholder [~] × Anna KRIŽAN); ★ GRIBLJE × GRIBLJE (h18 × h27); ★ the 1st MÜTTERLICH court consent of the line: »mütterlich fürwillig für mj. Braut vom k.k. Bez. Ger. Črnomelj ddto 7/5.1897 Ž:3791« + väterl. mündl. for the groom; witnesses Mathias Klepec + Johann Perdinec (½ göbl); priest Jos. Rauy; Befünden: the Griblje commune certificate May 30 no. 3",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04455",
    year: 1897,
    scan: 102,
    page: 101,
    whatSi: "poroka (31. 5. 1897, vpis 10) — nevesta Anna KUCHAR [~ Kučar], ½ Griblarš-tojštno, 16 (MLADOLETNA — mütterl. sodna privolitev Ž:3791!), GRIBLJE 27 (oče Jacob Kuchar ½? Griblar [~] × Anna KRIŽAN) × Mathias SIMEC, ½ Griblar, 23, GRIBLJE 18 (drubel poroka — h18 MEGA cross-link!); ★ Simec ×2 v 2 dnevih (cf. v11 nevesta Maria Simec h39!); KRIŽAN ×2 (cf. v8/v9); duhovnik Jos. Rauy",
    whatEn: "marriage (May 31, 1897, entry 10) — bride Anna KUCHAR [~ Kučar], half smallholder's daughter, 16 (A MINOR — the mütterl. court consent Ž:3791!), GRIBLJE 27 (father Jacob Kuchar ½? smallholder [~] × Anna KRIŽAN) × Mathias SIMEC, half smallholder, 23, GRIBLJE 18 (a double-Griblje marriage — the h18 MEGA cross-link!); ★ Simec ×2 in 2 days (cf. the v11 bride Maria Simec h39!); KRIŽAN ×2 (cf. v8/v9); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "39",
    bookSignature: "04455",
    year: 1897,
    scan: 103,
    page: 102,
    whatSi: "poroka (31. 5. 1897, vpis 11) — nevesta Maria SIMEC, ½ Griblarš-tojšt, 17 (MLADOLETNA — väterl. sodna privolitev Ž:3584!), GRIBLJE 39 (1. POROČNI DOKAZ h39; oče Nicolaus Simec ¼ Griblar × Catharina JAKOBČIČ) × Nikolaus PREDANIC [~ — oče Johann PERDINEC! varianta A7], ½ Griblar, 22, GRIBLJE 40 (A6: 2. ženin h40 v letu!; oče Johann Perdinec ¼ Griblar × Anna JAKOBČIČ — OBE MATI JAKOBČIČ!); ★ 2. GRIBLJE poroka ISTI DAN (31/5. — cf. v10!); ★ »in Ungarn« formula za ženina (8. instanca!); Griblje št:2 (izdano 29/5. — PRED št:3!); priče Mathias [Mrh.?] [~] + Mathias Simec (¼ göbl); duhovnik Jos. Rauy; Befünden: zglasmica občine Griblje od 29/5. št:2 + k.k. Bez.Ger. Črnomelj Ž:3584",
    whatEn: "marriage (May 31, 1897, entry 11) — bride Maria SIMEC, half smallholder's daughter, 17 (A MINOR — the väterl. court consent Ž:3584!), GRIBLJE 39 (the 1st MARRIAGE evidence of h39; father Nicolaus Simec quarter smallholder × Catharina JAKOBČIČ) × Nikolaus PREDANIC [~ — the father Johann PERDINEC! variant A7], half smallholder, 22, GRIBLJE 40 (A6: the 2nd groom of h40 in the year!; father Johann Perdinec quarter smallholder × Anna JAKOBČIČ — BOTH MOTHERS JAKOBČIČ!); ★ the 2nd GRIBLJE marriage the SAME DAY (May 31 — cf. v10!); ★ the »in Ungarn« formula for the groom (the 8th instance!); Griblje no:2 (issued May 29 — BEFORE no:3!); witnesses Mathias [Mrh.?] [~] + Mathias Simec (¼ göbl); priest Jos. Rauy; Befünden: the Griblje commune certificate May 29 no:2 + k.k. Bez.Ger. Črnomelj Ž:3584",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04455",
    year: 1897,
    scan: 103,
    page: 102,
    whatSi: "poroka (31. 5. 1897, vpis 11) — ženin Nikolaus PREDANIC [~ — oče Johann PERDINEC! varianta A7], ½ Griblar, 22, GRIBLJE 40 (A6: 2. ženin h40 v letu — v9 Brodarič!; oče Johann Perdinec ¼ Griblar × Anna JAKOBČIČ — obe mati JAKOBČIČ z nevestino!) × Maria SIMEC, ½ Griblarš-tojšt, 17 (MLADOLETNA), GRIBLJE 39 (drubel poroka — oba bloka!); ★ 2. GRIBLJE poroka ISTI DAN (31/5. — cf. v10!) + ★ »in Ungarn« formula za ženina (8. instanca!); priče Mathias [Mrh.?] [~] + Mathias Simec (¼ göbl); duhovnik Jos. Rauy; Befünden: zglasmica občine Griblje od 29/5. št:2 (izdana PRED št:3!) + väterl. mündl. fürwillig za ženina in UNGARN + väterl. privolitev za nevesto k.k. Bez.Ger. Črnomelj Ž:3584",
    whatEn: "marriage (May 31, 1897, entry 11) — groom Nikolaus PREDANIC [~ — the father Johann PERDINEC! variant A7], half smallholder, 22, GRIBLJE 40 (A6: the 2nd groom of h40 in the year — v9 Brodarič!; father Johann Perdinec quarter smallholder × Anna JAKOBČIČ — BOTH mothers JAKOBČIČ with the bride's side!) × Maria SIMEC, half smallholder's daughter, 17 (A MINOR), GRIBLJE 39 (a double-Griblje marriage — both blocks!); ★ the 2nd GRIBLJE marriage the SAME DAY (May 31 — cf. v10!) + ★ the »in Ungarn« formula for the groom (the 8th instance!); witnesses Mathias [Mrh.?] [~] + Mathias Simec (¼ göbl); priest Jos. Rauy; Befünden: the Griblje commune certificate May 29 no:2 (issued BEFORE no:3!) + väterl. mündl. fürwillig for the groom in UNGARN + the väterl. consent for the bride k.k. Bez.Ger. Črnomelj Ž:3584",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04455",
    year: 1897,
    scan: 104,
    page: 103,
    whatSi: "poroka (22. 11. 1897, vpis 18) — ženin Mathias DEBLIČ? [~ Teblič], ½ griblarš? Jofm [~], 25, GRIBLJE 33 (1. POROČNI DOKAZ h33; oče Mathias Deblič? [~] ½ Griblar × Maria Hrsič? [~]) × Maria POŽEK? [~ Ložek], ½ gbl. Tochkr [~], 22, GRIBLJE 28 (1. POROČNI DOKAZ h28; oče Georg Ložek? [~] ¼? Griblar [~] × Margareth Mihovič? [~]); ★ GRIBLJE × GRIBLJE (h33 × h28) — 5. in ZADNJA GRIBLJE poroka 1897 = REKORD LINIJE!; priče Mathias Brinec (BRINEC ×2 = v9!) + Johann Kučar? [~] (½ gbl); duhovnik Jos. Rauy; Befünden: zglasmica občine Griblje od 21/11. št:4 (vrsta ZAKLJUČENA 1→2→3→4!) + elterlich? fürwillig za nevesto od 8/9.1897",
    whatEn: "marriage (Nov 22, 1897, entry 18) — groom Mathias DEBLIČ? [~ Teblič], ½ smallholder's? Jofm [~], 25, GRIBLJE 33 (the 1st MARRIAGE evidence of h33; father Mathias Deblič? [~] half smallholder × Maria Hrsič? [~]) × Maria POŽEK? [~ Ložek], ½ gbl. Tochkr [~], 22, GRIBLJE 28 (the 1st MARRIAGE evidence of h28; father Georg Ložek? [~] ¼? smallholder [~] × Margareth Mihovič? [~]); ★ GRIBLJE × GRIBLJE (h33 × h28) — the 5th and LAST GRIBLJE marriage of 1897 = the RECORD of the line!; witnesses Mathias Brinec (BRINEC ×2 = v9!) + Johann Kučar? [~] (½ gbl); priest Jos. Rauy; Befünden: the Griblje commune certificate Nov 21 no:4 (the series CLOSED 1→2→3→4!) + elterlich? consent for the bride from Sep 8, 1897",
    status: "DOCUMENTED",
  },
  {
    houseNo: "28",
    bookSignature: "04455",
    year: 1897,
    scan: 104,
    page: 103,
    whatSi: "poroka (22. 11. 1897, vpis 18) — nevesta Maria POŽEK? [~ Ložek], ½ gbl. Tochkr [~], 22, GRIBLJE 28 (1. POROČNI DOKAZ h28; oče Georg Ložek? [~] ¼? Griblar [~] × Margareth Mihovič? [~]) × Mathias DEBLIČ? [~ Teblič], ½ griblarš? Jofm [~], 25, GRIBLJE 33 (drubel poroka — oba bloka!); ★ ZADNJA GRIBLJE poroka rekordnega leta; duhovnik Jos. Rauy",
    whatEn: "marriage (Nov 22, 1897, entry 18) — bride Maria POŽEK? [~ Ložek], ½ gbl. Tochkr [~], 22, GRIBLJE 28 (the 1st MARRIAGE evidence of h28; father Georg Ložek? [~] ¼? smallholder [~] × Margareth Mihovič? [~]) × Mathias DEBLIČ? [~ Teblič], ½ smallholder's? Jofm [~], 25, GRIBLJE 33 (a double-Griblje marriage — both blocks!); ★ the LAST GRIBLJE marriage of the record year; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  // ——— P127 razširitev: POROČNA KNJIGA 04455 — polno leto 1898 (s104–s109 ==
  // Pag. 103–108; Pag. == sken − 1, 13. potrditev; velja 61–108). Rokopisna
  // glava »1898.« na s104 + glava »1899.« + v1–5/1899 ŽE na s110 (P128
  // lead!). 1898 = 27 vpisov = REKORD LINIJE (prej 21 P122!) — razpored jan 2
  // + feb 8 + maj 4 + jun 3 + jul 2 + okt 1 + nov 7 (21.11. ×6 = 2. največji
  // dan linije!).
  // NOVELE: ★ GRIBLJE poroke ×6 = NOVI REKORD (prej 5 P126!) — 9 poročnih
  // blokov (h48 NOVA + h22 ×2 ISTI DAN A6 + h67 NOVA + h54 2. dokaz SIMEC +
  // h62 NOVA + h70 NOVA + h34 1. dokaz + h46 NOVA) + ★ BRAT/SESTRA ŽUPANIČ
  // cross-entry (v8 ženin Johann + v13 nevesta Dorothea = otroci Mathiasa
  // Županiča ½ griblar + Catharine Šaradinič, Krasinec 18!) + ★ ⅛ griblar
  // (v23 — NOVI najnižji ulomek, prej 3/16!) + ★ k.k. LANDESREGIERUNG Laibach
  // Z:12527 (28.8.1898) za OBA mladoletna (v20 »Braut und mlj. Bräutigam«!) +
  // ★ MÖTTLING = nemško Metlika 5.–6. dokaz (v9 k.k. Bez.Ger. + v17 [?]amte +
  // tiskar »Bindig in Möttlig.«) + ★ SLOV. EKVIVALENT formule »v navzočnosti
  // [zgornjih prič]« (v11/v12) = »in Gegenwart obiger Beystände« ×5 (v10/v15/
  // v19/v20/v27) — skupaj 7 + ★ Herms ×2 ZAPORED (v13 coop. + v14 coad.) — Rauy 25/27 + ★
  // Umrtveni list prve žene ženinove (v23, Sv. Vid pri Žatičmi?) + ★
  // Decanatsamt Rudolfswert + Bischofs-Akt L:275 (v21) + ★ Jamški list
  // BOROVNICA (v25) + ★ 1. NEZAKONSKI ženin 1898 (v16 prazna očetova celica +
  // Taglöhnerin mati!) + ★ vdovec 41 Holzarbeiter-Aufseher geb. ČRNI VRH OB
  // IDRIJI (v23) + ★ Zaiflner stand ×5–6 + ★ PLUT familija ×3 + ★ Pedirec/
  // Perdinec varianta ×7 + občinske vrste: Podzemelj 7→8→9→10→12→14 | Griblje
  // 1→2→4 | Gradac 31→32→33→34→35 POPOLNA | Smihel-Dopine? 29→39 | Krasinec
  // 13 | Črni Vrh 15 | Suho 2.
  // Dokaz: research/issue17/parish-marriage-1898.json; verifikator:
  // scripts/p127_parish_marriage_1898.py --check (I1–I11).
  {
    houseNo: "48",
    bookSignature: "04455",
    year: 1898,
    scan: 105,
    page: 104,
    whatSi: "poroka (30. 1. 1898, vpis 2) — nevesta Anna KLOBUČAR, 19, GRIBLJE 48 (1. POROČNI DOKAZ h48 — NOVA HIŠA!) × Peter Jakljevič? [~], »z güblarštofa« [~], 25, Pniloxje? 30 [~ — toponim neznana, oblika 6× potrjena; kandidat Ponikve?]; ženin ½ griblarški sohn ✓; duhovnik Jos. Rauy",
    whatEn: "marriage (Jan 30, 1898, entry 2) — the bride Anna KLOBUČAR, 19, GRIBLJE 48 (the 1st MARRIAGE evidence of h48 — A NEW HOUSE!) × Peter Jakljevič? [~], »z güblarštofa« [~], 25, Pniloxje? 30 [~ — an unresolved toponym, shape 6× confirmed; candidate Ponikve?]; the groom a half-smallholder's son ✓; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04455",
    year: 1898,
    scan: 105,
    page: 104,
    whatSi: "poroka (20. 2. 1898, vpis 7) — ženin Nicolaus STRAUS, 26, GRIBLJE 22 (1. POROČNI DOKAZ h22 — domačija »Nikolaus« ✓ pass 1!; oče ¼ Griblar [~]) × Maria Jakofčič, 30, GRIBLJE 67 (1. POROČNI DOKAZ h67 — NOVA!); ★ A6: h22 ×2 ženina ISTI DAN (cf. v9 Milek — vzorec P126 h40!) + št. zglasmic Griblje 1; duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 20, 1898, entry 7) — the groom Nicolaus STRAUS, 26, GRIBLJE 22 (the 1st MARRIAGE evidence of h22 — the homestead »Nikolaus« ✓ pass 1!; father a quarter smallholder [~]) × Maria Jakofčič, 30, GRIBLJE 67 (the 1st MARRIAGE evidence of h67 — NEW!); ★ A6: h22 has TWO grooms THE SAME DAY (cf. v9 Milek — the P126 h40 pattern!) + the Griblje certificate no. 1; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "67",
    bookSignature: "04455",
    year: 1898,
    scan: 105,
    page: 104,
    whatSi: "poroka (20. 2. 1898, vpis 7) — nevesta Maria JAKOFČIČ, 30, GRIBLJE 67 (1. POROČNI DOKAZ h67 — NOVA HIŠA!) × Nicolaus Straus, 26, GRIBLJE 22 (drubel poroka — h22 ×2 isti dan!); duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 20, 1898, entry 7) — the bride Maria JAKOFČIČ, 30, GRIBLJE 67 (the 1st MARRIAGE evidence of h67 — A NEW HOUSE!) × Nicolaus Straus, 26, GRIBLJE 22 (a double marriage — h22 ×2 the same day!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04455",
    year: 1898,
    scan: 106,
    page: 105,
    whatSi: "poroka (20. 2. 1898, vpis 9) — ženin Nicolaus MILEK, »z güblarštofa« [~], 28, GRIBLJE 22 (A6: 2. ženin h22 ISTI DAN — 2. blok h22!; oče Johann Milek × Maria KRIŽAN) × Maria Klepec, 22, Horst? 21 [~ a/o — usklajeno Hrast pri Vinici] (oče Georg Klepec × Barbara KRIŽAN — OBE MATI KRIŽAN!); Befünden: zglasmica občine Griblje d° 19/2. št:2 + »Erklärung für die mlj. Braut vom k.k. Bez. Ger. MÖTTLING d. 9/2. 1898« (★ Möttling = nemško METLIKA — 6. dokaz linije!); duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 20, 1898, entry 9) — the groom Nicolaus MILEK, »z güblarštofa« [~], 28, GRIBLJE 22 (A6: the 2nd groom of h22 THE SAME DAY — the 2nd h22 block!; father Johann Milek × Maria KRIŽAN) × Maria Klepec, 22, Horst? 21 [~ a/o — aligned with Hrast pri Vinici] (father Georg Klepec × Barbara KRIŽAN — BOTH MOTHERS KRIŽAN!); Befünden: the Griblje commune certificate Feb 19 no:2 + »Erklärung für die mlj. Braut vom k.k. Bez. Ger. MÖTTLING d. 9/2. 1898« (★ Möttling = German METLIKA — the 6th proof of the line!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04455",
    year: 1898,
    scan: 106,
    page: 105,
    whatSi: "poroka (9. 5. 1898, vpis 11) — ženin Johann SIMEC, 39, GRIBLJE 54 (2. POROČNI DOKAZ h54 — 1889 nevesta Anna SIMEC ¼ Gütlstochter: SIMEC-familija hiša!; starši Peter Jakobrič? ½ griblar × Catharina Brodarič) × Maria Kure, 29, GRIBLJE 62 (1. POROČNI DOKAZ h62 poroko!; starši Nicolaus Klepec ½ griblar × Barbara Tome); priči Mathias Grabus? [~] ½ griblar + Josef PEDIREC ¾ gbl (¾ ulomek + Perdinec-varianta!); Befünden: zglasnica občine Podzemelj od 1.5. št:9 + proglasenje od c. kr. sodišča v Metliki 23/4. + dovoljenje za ml. nevesto »v navzočnosti [zgornjih prič]« (★ SLOV. EKVIVALENT »in Gegenwart obiger Beystände«!); duhovnik Jos. Rauy",
    whatEn: "marriage (May 9, 1898, entry 11) — the groom Johann SIMEC, 39, GRIBLJE 54 (the 2nd MARRIAGE evidence of h54 — 1889 bride Anna SIMEC: the SIMEC-family house!; parents Peter Jakobrič? half smallholder × Catharina Brodarič) × Maria Kure, 29, GRIBLJE 62 (the 1st MARRIAGE evidence of h62!; parents Nicolaus Klepec half smallholder × Barbara Tome); witnesses Mathias Grabus? [~] half smallholder + Josef PEDIREC ¾ gbl (a ¾ fraction + the Perdinec variant!); Befünden: the Podzemelj commune certificate May 1 no:9 + the announcement by the Metlika court Apr 23 + the consent for the minor bride »v navzočnosti [zgornjih prič]« (★ the SLOVENE EQUIVALENT of »in Gegenwart obiger Beystände«!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04455",
    year: 1898,
    scan: 106,
    page: 105,
    whatSi: "poroka (9. 5. 1898, vpis 11) — nevesta Maria KURE, 29, GRIBLJE 62 (1. POROČNI DOKAZ h62; starši Nicolaus Klepec ½ griblar × Barbara Tome) × Johann Simec, 39, GRIBLJE 54 (2. dokaz h54 — SIMEC-familija!); KURE cf. P91 h1 botra Katarina Kure; duhovnik Jos. Rauy",
    whatEn: "marriage (May 9, 1898, entry 11) — the bride Maria KURE, 29, GRIBLJE 62 (the 1st MARRIAGE evidence of h62; parents Nicolaus Klepec half smallholder × Barbara Tome) × Johann Simec, 39, GRIBLJE 54 (the 2nd h54 evidence — the SIMEC family!); KURE cf. the P91 h1 godmother Katarina Kure; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "70",
    bookSignature: "04455",
    year: 1898,
    scan: 107,
    page: 106,
    whatSi: "poroka (6. 6. 1898, vpis 15) — nevesta Maria PERDINEC, 21, GRIBLJE 70 (1. POROČNI DOKAZ h70 — NOVA HIŠA!; starši Mathias PEDRINEC ½ griblar × Dorothea Jakofčič — Perdinec-varianta!) × Marcus Grabrijan, 29, Cerkvišče? 31 [~] (starši Georg Grabrijan ½ griblar × Maria Mavrin); priči Nicolaus Kraij? [~] + Johann Stuhljar? [~] (½ gbl); Befünden: [izkaznica?] občine Podzemelj d° 30/5. + mündl. väterl. fürwillig für die mlj. Braut in Gegenwart obiger Beystände ✓; duhovnik Jos. Rauy",
    whatEn: "marriage (Jun 6, 1898, entry 15) — the bride Maria PERDINEC, 21, GRIBLJE 70 (the 1st MARRIAGE evidence of h70 — A NEW HOUSE!; parents Mathias PEDRINEC half smallholder × Dorothea Jakofčič — the Perdinec variant!) × Marcus Grabrijan, 29, Cerkvišče? 31 [~] (parents Georg Grabrijan half smallholder × Maria Mavrin); witnesses Nicolaus Kraij? [~] + Johann Stuhljar? [~] (½ gbl); Befünden: the [ID card?] of the Podzemelj commune May 30 + the mündl. väterl. fürwillig for the minor bride in Gegenwart obiger Beystände ✓; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04455",
    year: 1898,
    scan: 108,
    page: 107,
    whatSi: "poroka (17. 10. 1898, vpis 20) — ženin Nicolaus FILAK, ½ güblnšsohn, 20 (MLADOLETEN!), GRIBLJE 34 (1. POROČNI DOKAZ h34!; starši Johann Filak ½ griblar × Anna Dehlič? [~]) × Catharina Klobučar, ½ güblnštocht, 21 (MLADOLETNA!), GRIBLJE 46 (1. POROČNI DOKAZ h46 — NOVA!; starši Marcus Klobučar ½ griblar × Catharina MILEK — cf. v9 Milek h22!); ★ GRIBLJE × GRIBLJE »isti-vasi« + ★ OBA mladoletna: formula »mündlich väterlich fürwillig für die mlj. Braut UND mlj. Bräutigam« + k.k. LANDESREGIERUNG IN LAIBACH ddo 28. August 1898 Z: 12527 (2. Landesregierung-dokument linije!) + zglasmica občine GRIBLJE od 16/10. št:4; priči Nicolaus Joček? [~] + Joseph Brucel? [~]; duhovnik Jos. Rauy",
    whatEn: "marriage (Oct 17, 1898, entry 20) — the groom Nicolaus FILAK, ½ smallholder's son, 20 (A MINOR!), GRIBLJE 34 (the 1st MARRIAGE evidence of h34!; parents Johann Filak half smallholder × Anna Dehlič? [~]) × Catharina Klobučar, ½ smallholder's daughter, 21 (A MINOR!), GRIBLJE 46 (the 1st MARRIAGE evidence of h46 — NEW!; parents Marcus Klobučar half smallholder × Catharina MILEK — cf. v9 Milek h22!); ★ GRIBLJE × GRIBLJE »same-village« + ★ BOTH minors: the formula »mündlich väterlich fürwillig für die mlj. Braut UND mlj. Bräutigam« + the k.k. LANDESREGIERUNG IN LAIBACH ddo Aug 28, 1898 Z: 12527 (the 2nd Landesregierung document of the line!) + the Griblje commune certificate Oct 16 no:4; witnesses Nicolaus Joček? [~] + Joseph Brucel? [~]; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04455",
    year: 1898,
    scan: 108,
    page: 107,
    whatSi: "poroka (17. 10. 1898, vpis 20) — nevesta Catharina KLOBUČAR, ½ güblnštocht, 21 (MLADOLETNA!), GRIBLJE 46 (1. POROČNI DOKAZ h46 — NOVA HIŠA!; starši Marcus Klobučar ½ griblar × Catharina Milek) × Nicolaus Filak, 20 (MLADOLETEN), GRIBLJE 34 (drubel poroka — oba bloka!); ★ k.k. Landesregierung Laibach Z:12527 (28.8.1898) za OBA + Griblje št:4; duhovnik Jos. Rauy",
    whatEn: "marriage (Oct 17, 1898, entry 20) — the bride Catharina KLOBUČAR, ½ smallholder's daughter, 21 (A MINOR!), GRIBLJE 46 (the 1st MARRIAGE evidence of h46 — A NEW HOUSE!; parents Marcus Klobučar half smallholder × Catharina Milek) × Nicolaus Filak, 20 (A MINOR), GRIBLJE 34 (a double marriage — both blocks!); ★ the k.k. Landesregierung Laibach Z:12527 (Aug 28, 1898) for BOTH + Griblje no:4; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  // ——— P128 razširitev: POROČNA KNJIGA 04455 — polno leto 1899 (skeni 110–111 ==
  // Pag. 109–110; Pag. = sken − 1, 14. potrditev; glava »1899.« na s110 potrjena;
  // glava »1900.« na s112 = P129 lead — v1/1900 Krasinec 18 ŽUPANIČ!) —
  // 9 vpisov obojestransko = 2. najmanjše leto linije (min 1886:7; −18 po
  // rekordnem 1898:27!) — vpisi z Griblji (3 poroke / 6 poročnih blokov:
  // h34 v1 2. dokaz + h44 v1 NOVA + h1 v3 NOVA NAJNIŽJA + h10 v3 3. dokaz +
  // h20 v4 2. dokaz + h16 v4 3. dokaz): NOVELE: ★ NAJSTAREJŠI PAR LINIJE
  // (v1: 66 + 68 = 134, OBA status 1!) + ★ ¾ GIBLAR (v7 oče+hči — NOVI
  // NAJVIŠJI ulomek, prej ½!) + ★ 1. ženin izven sistema (v9 Pf. St. Michel
  // b. Rudolfswerth = Novo mesto!) + ★ zglasmica-PENTAGON 5 občin (Griblje
  // 2/3/5 · Podzemelj 1/3/4 · Gradac 57 · na Gori? 2 · Šmihel-Štopriče? 65) +
  // ★ DUHOVNIKI: Novak 5/9 dominanta (1898 Rauy 25/27!) + 1. dokaz Franz
  // STURM Coop. ×2 (v4+v6!) + ★ oče kot priča v istem vpisu (v3 Željko!) +
  // ★ CROSS-ENTRY v1→v4 (ženin Žibak priča 4 dni po poroki!) + priča-link
  // v6→v9 Županič + ★ KURE/MUC kompleks (v3 == h10 1890!) + ŽURAJEVIČ ×4 +
  // ★ VRANOVIČE 5 hiš čez 1898–99 (h2/h4/h9/h27/h28) + ★ SODRAŽICA Pfarramt
  // (v8) + ★ dispens № 2319 fb. Ord. Laibach (v7) + LAIFSKLAR/LAIFFLER ×5
  // (cf. P127 Zaiflner — identiteta? odprto).
  // Dokaz: research/issue17/parish-marriage-1899.json; verifikator:
  // scripts/p128_parish_marriage_1899.py --check (I1–I11).
  {
    houseNo: "34",
    bookSignature: "04455",
    year: 1899,
    scan: 110,
    page: 109,
    whatSi: "poroka (9. 1. 1899, vpis 1) — ženin Johann ŽIBAK? [~ — 6×: Ž/J z zavihkom + descender + zanka b; NI F/l! glej honesty], Štrigžingtar? [~ — poklic, m. forma; 1887 brez zadetka], 66 (status 1!), GRIBLJE 34 (2. POROČNI DOKAZ h34 po 1898 v20 Nicolaus FILAK — tension priimkov!) × Maria [Ś/H]rudej? [~], Štrigžingtarin? [~ — ž. forma ISTEGA termina → poklic], 68 (status 1!) = ★ NAJSTAREJŠI PAR LINIJE (134 let skupaj, OBA 1. poroka!); starši: Mathias Žibak ½ griblar × Catharina Pendirec / Mathias Klobučar ¼ griblar × Anna Horvat; priči Marcus KLOBUČAR (= oče neveste v20/1898 h46 — cross-link!) + Johann Hrbalj? [~] ½ griblar [~]; Befünden: ženitovanjska zglasmica občine Griblje d° 9/1. 1899 št: 2; duhovnik Jos. Novak (P.f.) — 1899 NOVA DOMINANTA (5/9; 1898: Rauy 25/27!)",
    whatEn: "marriage (Jan 9, 1899, entry 1) — the groom Johann ŽIBAK? [~ — 6×: Ž/J with a hook + descender + b with a bowl; NOT F/l! see honesty], Štrigžingtar? [~ — an occupation, the masculine form; no match in 1887], 66 (status 1!), GRIBLJE 34 (the 2nd MARRIAGE evidence of h34 after the 1898 v20 Nicolaus FILAK — a surname tension!) × Maria [Ś/H]rudej? [~], Štrigžingtarin? [~ — the feminine form of the SAME term → an occupation], 68 (status 1!) = ★ THE OLDEST COUPLE OF THE LINE (134 years together, BOTH 1st marriages!); parents: Mathias Žibak ½ smallholder × Catharina Pendirec / Mathias Klobučar ¼ smallholder × Anna Horvat; witnesses Marcus KLOBUČAR (= the father of the 1898 v20 bride, h46 — a cross-link!) + Johann Hrbalj? [~] ½ smallholder [~]; Befünden: the Griblje commune marriage certificate Jan 9, 1899 no: 2; priest Jos. Novak (P.f.) — the NEW 1899 DOMINANT (5/9; 1898: Rauy 25/27!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04455",
    year: 1899,
    scan: 110,
    page: 109,
    whatSi: "poroka (9. 1. 1899, vpis 1) — nevesta Maria [Ś/H]rudej? [~], Štrigžingtarin? [~], 68 (status 1 — 1. poroka pri 68 letih = LINIJSKI REKORD!), GRIBLJE 44 (1. POROČNI DOKAZ h44 — NOVA poročna!; hiša že v mrliški 04894-1887 + krstni 04105-1888+) × Johann Žibak? [~], 66, GRIBLJE 34 (2. dokaz h34); starši neveste: Mathias KLOBUČAR ¼ griblar × Anna Horvat (DRUGA Klobučar-veja kot h46 Marcus ½!); priči Marcus Klobučar + Johann Hrbalj? [~]; zglasmica Griblje št: 2; duhovnik Jos. Novak (P.f.)",
    whatEn: "marriage (Jan 9, 1899, entry 1) — the bride Maria [Ś/H]rudej? [~], Štrigžingtarin? [~], 68 (status 1 — a FIRST marriage at 68 = the LINE RECORD!), GRIBLJE 44 (the 1st MARRIAGE evidence of h44 — NEW!; the house already in the death register 04894-1887 + the baptism 04105-1888+) × Johann Žibak? [~], 66, GRIBLJE 34 (the 2nd h34 evidence); the bride's parents: Mathias KLOBUČAR ¼ smallholder × Anna Horvat (a DIFFERENT Klobučar branch than the h46 Marcus ½!); witnesses Marcus Klobučar + Johann Hrbalj? [~]; the Griblje certificate no: 2; priest Jos. Novak (P.f.)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04455",
    year: 1899,
    scan: 110,
    page: 109,
    whatSi: "poroka (30. 1. 1899, vpis 3) — ženin Georg ŽELJKO, ½ gbl. [B/P]ohu? [~ — kratka pripomba za ulomkom, 3× v vpisu], 31, GRIBLJE 1 (1. POROČNI DOKAZ h1 — NAJNIŽJA hišna številka poročne linije!; hiša že v krstni 04105 9× 1888–1914: P87 sidro h1 oče Nikolaj Željko ¼ × Katarina Kure!) × Barbara KURE, ½ gbl. [K]allan? [~], 27, GRIBLJE 10 (3. poročni dokaz h10 — 1887 Križe + 1890 Anna KURE!); starši: Nicolaus Željko ½ gbl [B/P]ohu? × Anna Jakobič / Marcus Kure ¼ griblar × Anna Škala [~ — h10 1890 branje »Špala«, varianta!]; ★ priči Nicolaus ŽELJKO (OČE ženina KOT PRIČA v istem vpisu — 1. tak dokaz linije!) + Johann MUC [Piharnik? ~] (= h10 1890 ŽENIN! + P92 h61 Muc × Ana Kure 1897!); zglasmica Griblje od dne 29/1. št: 3; duhovnik Jos. Rauy",
    whatEn: "marriage (Jan 30, 1899, entry 3) — the groom Georg ŽELJKO, ½ sml. [B/P]ohu? [~ — a short annotation after the fraction, 3× in the entry], 31, GRIBLJE 1 (the 1st MARRIAGE evidence of h1 — the LOWEST house number of the marriage line!; the house already in the baptism 04105 9× 1888–1914: the P87 h1 anchor father Nikolaj Željko ¼ × Katarina Kure!) × Barbara KURE, ½ sml. [K]allan? [~], 27, GRIBLJE 10 (the 3rd marriage evidence of h10 — 1887 Križe + 1890 Anna KURE!); parents: Nicolaus Željko ½ sml [B/P]ohu? × Anna Jakobič / Marcus Kure ¼ smallholder × Anna Škala [~ — the h10 1890 reading »Špala«, a variant!]; ★ witnesses Nicolaus ŽELJKO (the groom's FATHER AS WITNESS in the same entry — the 1st such proof of the line!) + Johann MUC [Piharnik? ~] (= the h10 1890 GROOM! + P92 h61 Muc × Ana Kure 1897!); the Griblje certificate Jan 29 no: 3; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04455",
    year: 1899,
    scan: 110,
    page: 109,
    whatSi: "poroka (30. 1. 1899, vpis 3) — nevesta Barbara KURE, ½ gbl. [K]allan? [~], 27, GRIBLJE 10 (3. poročni dokaz h10!) × Georg Željko, 31, GRIBLJE 1 (1. dokaz h1!); ★ KURE SESTRI?: Anna Kure (1890 v1, 23, ¼ Gütlstochter) + Barbara (1899, 27) — OBA oče Marcus Kure ¼ griblar, mati Anna Špala/Škala [~ varianta]; priča Johann MUC = h10 1890 ŽENIN (MUC×KURE kompleks: P92 h61 Muc × Ana Kure 1897!); zglasmica Griblje št: 3; duhovnik Jos. Rauy",
    whatEn: "marriage (Jan 30, 1899, entry 3) — the bride Barbara KURE, ½ sml. [K]allan? [~], 27, GRIBLJE 10 (the 3rd marriage evidence of h10!) × Georg Željko, 31, GRIBLJE 1 (the 1st h1 evidence!); ★ the KURE SISTERS?: Anna Kure (1890 v1, 23, ¼ smallholder's daughter) + Barbara (1899, 27) — BOTH father Marcus Kure ¼ smallholder, mother Anna Špala/Škala [~ a variant]; the witness Johann MUC = the h10 1890 GROOM (the MUC×KURE complex: P92 h61 Muc × Ana Kure 1897!); the Griblje certificate no: 3; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04455",
    year: 1899,
    scan: 110,
    page: 109,
    whatSi: "poroka (13. 2. 1899, vpis 4) — ženin Alois NOVAK, Zimmermannsmeister, 24, geb: in Toplice No 50 [~ — rojstna župnija Toplice!], GRIBLJE 20 (2. POROČNI DOKAZ h20 po 1891 v7 Peter Pezdirec!) × Maria ŽIBAK? [~ — cf. v1; Filak-varianta?], ½ gbl. Tochter, 19, GRIBLJE 16 (3. poročni dokaz h16 — 1886 Ana FILAK + 1895 Anton Brodarič!); starši: Joseph Novak [Inwohner? ~] × Maria Pircel? [~] / Mathias Žibak ½ griblar × Anna Numanic? [~]; ★ priči Johann ŽIBAK Štrigžingar (= v1 ŽENIN — CROSS-ENTRY, 4 dni po lastni poroki!) + Matthias SIMEC Laifsklar? [~] (= h54 1898 ženin Johann Simec familija + h18 oče!); Befünden: ženitovanjska zglasmica Griblje od 12/2. št: 5 + dovoljenje iz sodnišča o Černomlju z dne 1. feb. 1899 + jamstvo list za ženina [pregelnega srada? ~] na Toplica z dnem 22/1. 1899 (3 dokumenti!); duhovnik Franz STURM Coop. (1. dokaz — ×2 v 1899!)",
    whatEn: "marriage (Feb 13, 1899, entry 4) — the groom Alois NOVAK, a master carpenter, 24, born in Toplice No 50 [~ — the birth parish Toplice!], GRIBLJE 20 (the 2nd MARRIAGE evidence of h20 after the 1891 v7 Peter Pezdirec!) × Maria ŽIBAK? [~ — cf. v1; a Filak variant?], ½ smallholder's daughter, 19, GRIBLJE 16 (the 3rd marriage evidence of h16 — 1886 Ana FILAK + 1895 Anton Brodarič!); parents: Joseph Novak [an Inwohner? ~] × Maria Pircel? [~] / Mathias Žibak ½ smallholder × Anna Numanic? [~]; ★ witnesses Johann ŽIBAK Štrigžingar (= the v1 GROOM — a CROSS-ENTRY, 4 days after his own wedding!) + Matthias SIMEC Laifsklar? [~] (= the h54 1898 groom Johann Simec family + the h18 father!); Befünden: the Griblje marriage certificate Feb 12 no: 5 + the permission from the court at Tschernomel Feb 1, 1899 + the guarantee letter for the groom re Toplice Jan 22, 1899 (3 documents!); priest Franz STURM Coop. (the 1st proof — ×2 in 1899!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04455",
    year: 1899,
    scan: 110,
    page: 109,
    whatSi: "poroka (13. 2. 1899, vpis 4) — nevesta Maria ŽIBAK? [~], ½ gbl. Tochter, 19, GRIBLJE 16 (3. poročni dokaz h16!) × Alois Novak, Zimmermannsmeister, 24, GRIBLJE 20 (2. dokaz h20!); ★ ŽIBAK veriga [~ hipoteza]: v1 ženin Johann Žibak 66 (oče Mathias ½ × Pendirec) → sin? Mathias Žibak ½ × Numanic → Maria 19 — oče IME = v1 ženinov oče! (Filak-tension: h16 1886 Ana FILAK oče Mathias!); priča Matthias SIMEC + Johann Žibak (= v1 ženin!); zglasmica Griblje št: 5 + sodišče Črnomelj 1.2. + jamstvo Toplice 22/1.; duhovnik Franz Sturm Coop.",
    whatEn: "marriage (Feb 13, 1899, entry 4) — the bride Maria ŽIBAK? [~], ½ smallholder's daughter, 19, GRIBLJE 16 (the 3rd marriage evidence of h16!) × Alois Novak, a master carpenter, 24, GRIBLJE 20 (the 2nd h20 evidence!); ★ the ŽIBAK chain [~ a hypothesis]: the v1 groom Johann Žibak 66 (father Mathias ½ × Pendirec) → son? Mathias Žibak ½ × Numanic → Maria 19 — the father's NAME = the v1 groom's father! (the Filak tension: h16 1886 Ana FILAK father Mathias!); witnesses Matthias SIMEC + Johann Žibak (= the v1 groom!); the Griblje certificate no: 5 + the Tschernomel court Feb 1 + the Toplice guarantee Jan 22; priest Franz Sturm Coop.",
    status: "DOCUMENTED",
  },
  // ——— P129 razširitev: POROČNA KNJIGA 04455 — polno leto 1900 (skeni 112–113 ==
  // Pag. 111–112; Pag. = sken − 1, 15. potrditev; glava »1900.« na s112 potrjena;
  // glava »1901.« na s114 = P130 lead POTRJEN — v1/1901 Jänner 28 Otok 34 Joseph
  // KRIŽAN × Otok 21 Barbara PALČIČ — P130-lead KOREKCIJE ×4 (Jan 18→28 ·
  // Otok 14→34 · Kurjan?→Križan · Pačaj?→Palčič!) —
  // 8 vpisov obojestransko = 2. najmanjše leto linije (min 1886:7 → 1900:8 →
  // 1899:9 padne na 3.!) — EDINA GRIBLJE poroka (2 poročna bloka: h7 v2 NOVA +
  // h8 v2 NOVA — 1. POROČNA DOKAZA OBEH HIŠ!): NOVELE: ★ ŽUPANIČ KONTINUUM
  // (v1 ženin Nicolaus Županič ¼ Krasinec 18 = ISTA HIŠA P127 v8/v13 — 3.
  // poročni dokaz! + v3 priča Johann Županič ½ = P127 v8 ženin — priča 7 dni
  // po lastni poroki!) + ★ 3 DVOJNA DNEVA = NOVI REKORD (Febr 12 ×2 + Febr
  // 19 ×2 + Nov 5 ×2; prej 1 P128!) + ★ RAUY 8/8 = 100% dominanta (povratek
  // P127-vzorca; P128 Novak 5/9!) + ★ 1. NEZAKONSKA NEVESTA? (v7 oče = ČRTA!)
  // + ★ KLOSTER ×3 hiše (69+40+76!) + ★ GRADAC 18 ×2 ženina + v7 nevesta
  // (vzorec A6!) + ★ pentagon 5 občin (+Adlešič + SVETI-JURZEJ NOVA!) + ★
  // SAMSKI LIST izrecno (v8!) + nadvarstveno ×2 + PEZDIREC ×4 (8. leto mreže!).
  // Dokaz: research/issue17/parish-marriage-1900.json; verifikator:
  // scripts/p129_parish_marriage_1900.py --check (I1–I11).
  {
    houseNo: "7",
    bookSignature: "04455",
    year: 1900,
    scan: 112,
    page: 111,
    whatSi: "poroka (12. 2. 1900, vpis 2) — ženin Jacobus TÖLLER? [~ — cf. Teller/Döller; P127 v23 Tomič familija-vprašanje odprto], ½ griblar, 37, GRIBLJE 7 (1. POROČNI DOKAZ h7!) × Catharina Jakobčič? [~ — cf. P80 hiša 13 Jakobič priimek-tension!], ½ gbl. Točla? [~], 21, GRIBLJE 8 (1. POROČNI DOKAZ h8!) = EDINA GRIBLJE poroka 1900 (2 bloka!); starši: Andrea Töller ½ × Margareth Strucelj? [~] / Johann Jakobčič ¼ × Maria Met? [~]; priči Martin Veršinič? [~] + Anton Brodanič? [~]; zglasmica občine Griblje 1/2. 1900 št: 1 (polnoletnost za nevesto — 21!); dvojni dan #1 (Febr 12 ×2!); duhovnik Jos. Rauy — 1900 RAUY 8/8 = 100% DOMINANTA!",
    whatEn: "marriage (Feb 12, 1900, entry 2) — the groom Jacobus TÖLLER? [~ — cf. Teller/Döller; the P127 v23 Tomič family question open], half smallholder, 37, GRIBLJE 7 (the 1st MARRIAGE evidence of h7!) × Catharina Jakobčič? [~ — cf. P80 house 13 Jakobič surname-tension!], half smallholder's Točla? [~], 21, GRIBLJE 8 (the 1st MARRIAGE evidence of h8!) = the ONLY Griblje wedding of 1900 (2 blocks!); parents: Andrea Töller ½ × Margareth Strucelj? [~] / Johann Jakobčič ¼ × Maria Met? [~]; witnesses Martin Veršinič? [~] + Anton Brodanič? [~]; the Griblje commune certificate Feb 1, 1900 no: 1 (the majority for the 21-year-old bride!); the double day #1 (Feb 12 ×2!); priest Jos. Rauy — 1900 RAUY 8/8 = the 100% DOMINANT!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04455",
    year: 1900,
    scan: 112,
    page: 111,
    whatSi: "poroka (12. 2. 1900, vpis 2) — nevesta Catharina JAKOBČIČ? [~], ½ gbl. Točla? [~], 21, GRIBLJE 8 (1. POROČNI DOKAZ h8!) × Jacobus Töller? [~], ½ griblar, 37, GRIBLJE 7 (1. POROČNI DOKAZ h7!); ★ EDINA GRIBLJE poroka 1900 (najmanj od P115!) + zglasmica polnoletnosti občine Griblje (1. tak za nevesto 21!) + Jakobčič/Jakobič tension (P80 h13!); duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 12, 1900, entry 2) — the bride Catharina JAKOBČIČ? [~], half smallholder's Točla? [~], 21, GRIBLJE 8 (the 1st MARRIAGE evidence of h8!) × Jacobus Töller? [~], half smallholder, 37, GRIBLJE 7 (the 1st MARRIAGE evidence of h7!); ★ the ONLY Griblje wedding of 1900 (the fewest since P115!) + the majority certificate of the Griblje commune (the 1st such for a 21-year-old bride!) + the Jakobčič/Jakobič tension (P80 h13!)",
    status: "DOCUMENTED",
  },
  // ——— P130 razširitev: POROČNA KNJIGA 04455 — polno leto 1901 (skeni 114–116 ==
  // strani 113–115; Pag. == sken − 1, 16. potrditev; rokopisna glava »1901.« na
  // s114 potrjena — P130-lead KOREKCIJE ×4: Jan 18→28 · Otok 14→34 · Kurjan?→
  // KRIŽAN · Pačaj?→PALČIČ!; rokopisna glava »1902.« ŽE na s116 = P131-lead
  // KOREKCIJA — s117 je samo nadaljevanje!). 11 vpisov obojestransko = 4.
  // najmanjše leto linije (min 1886:7 → 1900:8 → 1899:9 → 1901:11) — razpored
  // 4+5+2) — ★ 1901 = 1. leto poročne linije 1886–1901 BREZ VSAKE omembe
  // Griblje (0/11! — cf. krstna 1901 P96 = vsi vpisi Griblje = ASIMETRIJA!) →
  // 0 novih blokov (vitals 595, bloki 04455 = 78, sidra 71, p80 hiše 58, PT
  // luknja 12 VSE NESPREMENJENE). NOVELE: ★ 6 POROK NA 11.2.1901 (v3–v8 = 2.
  // največji dan linije — rekord 1893:7 6.2. P122!; 3× P129-rekord!) + ★ RAUY
  // 11/11 = 100% ABSOLUTNI REKORD (P129 8/8!) + ★ ¾ griblar 2. dokaz (v7 oče
  // Ignac Prevec + hči Engelbetha, Primostek 1 — vzorec P128 v7 Žugelj!) + ★
  // 1. DISPENS AFINOSTI linije (v1 Anverwandtschaft 2. dum? № 138? Laibach
  // 15/1.!; v8 consanguinitas 4. kolena št 236 + potestate delegata) + ★
  // POLNOLETNOST ZA ŽENINA (v4 21! Metlika IV 218/89 + deželna vlada št 1786;
  // v11 za OBA!) + ★ MUC ×3 (P128 v3 priča Johann Muc == v11 Weißstand!) + ★
  // Vranoviče 8 = 6. hiša vasi + ★ 1. činovniki-priče (c.k. poštni asistent +
  // zagrebški arhivar-protokolist robno!) + ★ nove vasi? (Primostek ×2 ·
  // Cerkvišče ×2 · Zastava · Dobraviče? · Borit? · Hast? · Grišiče?) + mreže:
  // Palčič ×3 · Muc ×3 · Jurajevič ×3 · Križan ×2 · Žimec ×2 · Jakša ×2 ·
  // Novačič ×2 + čez-faze: Jakljevič 1898→1901 · Štrucelj 1900→1901 · Kambič
  // 1893→1901 · Simonič 1893+1900→1901 · Hočevar 1898→1901.
  // Dokaz: research/issue17/parish-marriage-1901.json; verifikator:
  // scripts/p130_parish_marriage_1901.py --check (I1–I11).
  // ——— P131 razširitev: POROČNA KNJIGA 04455 — polno leto 1902 (skeni 116–117 ==
  // strani 115–116; Pag. == sken − 1, 17. potrditev; rokopisna glava »1902.« na
  // s116 potrjena ŽE od P130-lead — P131-lead KOREKCIJE ×2: [G]pbyke?→GRIBLJE 5!
  // (v2 ženinova vas = Griblje, NE nova vas!) + v6 datum Sept 15 (P129-lead
  // napaka »April 15«!) — glava »1903.« POTRJENA na s118 (r1 = 1903 Febr 3
  // Dragatuš? 1 × GRIBLJE 11 Agnes Žunjič? = P132 LEAD, 3. GRIBLJE poroka v
  // vrsti!). 6 vpisov obojestransko = NAJMANJŠE LETO POROČNE LINIJE 1886–1902
  // (prej min 1900:8 po skupnih vpisih / 1886:7 po okvirni konvenciji P128–P130
  // — 6 < 7 < 8 = NOVI MINIMUM V OBEH MERAH!; opomba: »min 1886:7« konvencija
  // meri GRIBLJE okvir 1886, skupni vpisi 1886 = 24 po P115 json — odprta
  // terminološka vprašanja linije) = Jänner 27 ×3 (v1–v3) + Mai 12 + Mai 26 +
  // Sept 15. 2 GRIBLJE poroke / 4 poročna bloka (h5 v2 1. POROČNI DOKAZ +
  // h31 v2 1. POROČNI DOKAZ = DRUBEL poroka! + h30 v4 3. dokaz po 1889+1892 +
  // h24 v4 2. dokaz po 1895 = DRUBEL poroka!) — vitals 595 → **599**; bloki
  // 04455 78 → **82**; sidra 71 → **75** (+1902:4); p80 hiše 58 + PT luknja 12
  // NESPREMENJENA (h5/h24/h30/h31 že v vzorci). NOVELE: ★ NAJMANJŠE LETO
  // LINIJE (6!) + ★ 2. DUHOVNIŠKA MENJAVA 1902: Hanislav DOSTÁL kaplan v5
  // (1. DOSTÁL linije — Rauy 5/6!) + ★ 2. NEZAKONSKI ŽENIN Z IZRECNO opombo
  // (v6 Thomas Černe: oče = črta + mati Ursula Černe »lediga? Ehe.« — 1.
  // IZRECNA nezakonska-opomba v poročni liniji!) + ★ 2 ženina IZVEN župnije v
  // enem letu (v6 Črnomelj 134 mesto + v6 nevesta Bukoraj? pf. Črnomelj 1 —
  // NOVA VAS? + očina PLANINA št: 10 NOVA!) + ★ priče činovniki (v6: vojak
  // Eugen Sorbea? 12 R. Leu. Bor'zd. off'Anwt. [~] + železniški Johann
  // Peterly? k.k. Bahndienst [~] — vzorec P130!) + ★ ženitovanjska zglašnica
  // = REŠITEV SERIJSKE FORMULE (prej »Porifovanjška/žerifovanjška« P128–P130
  // [~] — semantična rešitev: Trauungs-Anzeige!) + ★ ŠTRUPEC = NOVI PRIIMEK
  // LINIJE ×3 (v2 ženin Mathias + oče Johann + v6 nevestina mati Maria
  // Strupec!) + ★ LEGINA NOVI ×3 (v4 ženin + oče + priča Georg!) + ★ KOCJAN
  // NOVI (v6 nevesta + oče Peter ¼ griblar — griblar-status IZVEN Griblje!) +
  // ★ DRUBEL-GRIBLJE poroki ×2 v enem letu (v2 h5×h31 + v4 h30×h24 — 3. leto
  // z ≥2 po P121 ×3 + P122 ×2 + P127 ×3!) + PEZDIREC ×3 povratek (7. leto
  // mreže po 1901-pavzi!) + DRAGOŠ priča v2 (10. leto mreže 1886–1902!) +
  // MUC ×3 (v1 nevesta Terezia + v3 priča Johann == P128 v3 priča! + v5 mati
  // Maria) + ŽUPANIČ 4. leto (v3 mati neveste — pavza 1901!) + KLEPEC 16.+
  // leto + BRODARIČ 14.+ leto + ŠKALA 4. leto + ČERNE 3. leto + KRALJ 7.+
  // leto + STRAVS/Straus 3. leto + TOMC/Tomič 3.+ leto (P132-lead Barbara
  // Tomc!) + nadvarstveno dovoljenje ×3 (v4 sodišče Črnomelj P62/99 18. [~] +
  // v5 okrajno sodišče Metlika 13. maja + za ml. nevesto!) + Wagnermeister
  // (v3 — 1. v poročni liniji!) + Fabriksarbeiter (v3 oče — 1.!) + Besitzer
  // (v6 — 1.!). P131-lead stale: »min 6 vpisov« → točno 6; »[G]pbyke?« →
  // GRIBLJE 5 (korekcija!).
  // Dokaz: research/issue17/parish-marriage-1902.json; verifikator:
  // scripts/p131_parish_marriage_1902.py --check (I1–I11).
  {
    houseNo: "5",
    bookSignature: "04455",
    year: 1902,
    scan: 116,
    page: 115,
    whatSi: "poroka (27. 1. 1902, vpis 2) — ženin Mathias ŠTRUPEC? [~ — 1. NASTOP priimka v poročni liniji!], ¼ griblar, 29, GRIBLJE 5 (1. POROČNI DOKAZ h5!; h5 že v mrliškem okvirju 1886 P80!) × Maria MULH? [~ — cf. Mula/Muh; branje odprto], ½ gbl. Tochter, 20, GRIBLJE 31 (1. POROČNI DOKAZ h31!; h31 že v poročnem okvirju 1886 P80!) = ★ DRUBEL-GRIBLJE poroka (h5 × h31 — 1. poroka 1902; P131-lead KOREKCIJA: [G]pbyke?→GRIBLJE 5!); starši: Johann Štrupec ¼ griblar × Maria Harasinič? [~] / Mathias Mulh? ½ griblar × Maria Brodarič (BRODARIČ 14.+ leto mreže!); priče: Jacob Jetter? [~] (¼) + Jos. Dragoš? [~] (½) griblar — DRAGOŠ 10.+ leto (1886–1895, 1900, 1902!); zglasmica: ženitovanjska zglašnica očine Griblje od 26/1. št: 23, mit väterlichen mündl. Einwilligung für die mi. Braut in Gegenwart obiger Beifügenden [~ — vzorec P122 v16!]; TRIPLO-DATUM (Jänner 27 ×3 = v1+v2+v3!); duhovnik Jos. Rauy",
    whatEn: "marriage (Jan 27, 1902, entry 2) — the groom Mathias ŠTRUPEC? [~ — the 1st APPEARANCE of the surname in the marriage line!], quarter smallholder, 29, GRIBLJE 5 (the 1st MARRIAGE EVIDENCE of h5!; h5 already in the 1886 death frame P80!) × Maria MULH? [~ — cf. Mula/Muh; the reading open], half smallholder's daughter, 20, GRIBLJE 31 (the 1st MARRIAGE EVIDENCE of h31!; h31 already in the 1886 marriage frame P80!) = ★ the DOUBLE-GRIBLJE wedding (h5 × h31 — the 1st wedding of 1902; the P131-lead CORRECTION: [G]pbyke?→GRIBLJE 5!); parents: Johann Štrupec ¼ smallholder × Maria Harasinič? [~] / Mathias Mulh? ½ smallholder × Maria Brodarič (BRODARIČ the 14th+ year of the network!); witnesses: Jacob Jetter? [~] (¼) + Jos. Dragoš? [~] (½) smallholder — DRAGOŠ the 10th+ year (1886–1895, 1900, 1902!); certificate: the marriage banns (ženitovanjska zglašnica) of the Griblje commune from Jan 26 no: 23, with the verbal paternal consent for the minor bride in the presence of the above-attached [~ — the P122 v16 pattern!]; the TRIPLE DATE (Jan 27 ×3 = v1+v2+v3!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1902,
    scan: 116,
    page: 115,
    whatSi: "poroka (27. 1. 1902, vpis 2) — nevesta Maria MULH? [~], ½ gbl. Tochter, 20, GRIBLJE 31 (1. POROČNI DOKAZ h31! — h31 v poročnem okvirju 1886 ženinova [P80], 16 let čakanja na lasten dokaz!) × Mathias Štrupec? [~], ¼ griblar, 29, GRIBLJE 5 (1. POROČNI DOKAZ h5!) = DRUBEL-GRIBLJE poroka; oče Mathias Mulh? ½ griblar × Maria Brodarič (BRODARIČ ×14+!); zglasmica občine Griblje 26/1. št: 23 + väterliche mündl. Einwilligung (nevesta 20 = »mi.« [~ mladoletna-po-obliki, ne po starosti? vprašanje odprto]); duhovnik Jos. Rauy",
    whatEn: "marriage (Jan 27, 1902, entry 2) — the bride Maria MULH? [~], half smallholder's daughter, 20, GRIBLJE 31 (the 1st MARRIAGE EVIDENCE of h31! — h31 in the 1886 marriage frame as a groom's [P80], 16 years of waiting for its own evidence!) × Mathias Štrupec? [~], quarter smallholder, 29, GRIBLJE 5 (the 1st MARRIAGE EVIDENCE of h5!) = the DOUBLE-GRIBLJE wedding; father Mathias Mulh? ½ smallholder × Maria Brodarič (BRODARIČ ×14+!); the Griblje commune certificate Jan 26 no: 23 + the verbal paternal consent (the bride 20 = »mi.« [~ a minor-by-form, not by age? the question open]); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04455",
    year: 1902,
    scan: 117,
    page: 116,
    whatSi: "poroka (12. 5. 1902, vpis 4) — ženin Nicolaus LEGINA? [~ — 1. NASTOP priimka v poročni liniji!], ¼ griblar, 43 (najstarejši ženin leta!), GRIBLJE 30 (3. POROČNI DOKAZ h30 po 1889 P118 + 1892 P121 v5!) × Catharina BRIŠEC? [~ — cf. BRINEC-tension P122 h26!], ½ gbl. Tochter, 20, GRIBLJE 24 (2. poročni dokaz h24 po 1895 P124!) = ★ DRUBEL-GRIBLJE poroka (h30 × h24); starši: Johann Legina ¼ griblar × Dorothea Hrižan? [~] / Mathias Brišec ½ griblar × Barbara Jakobič? [~ — JAKOBIČ-link na P122 h26 starša Georg Jakobič!]; priče: Johan Brišec + Georg Legina ¼ griblar; nadvarstveno dovoljenje: ženitovanjska zglašnica očine Griblje-ske z dne 17.5.1902 štev: 2, po nadvarstveno dovoljenje && uml. rovetja [~] od c. kr. okr. sodišča Črnomelj od 1. maja 1902 P62/99 18. [~ — sodna odločba 11 dni pred poroko!]; duhovnik Jos. Rauy",
    whatEn: "marriage (May 12, 1902, entry 4) — the groom Nicolaus LEGINA? [~ — the 1st APPEARANCE of the surname in the marriage line!], quarter smallholder, 43 (the oldest groom of the year!), GRIBLJE 30 (the 3rd MARRIAGE EVIDENCE of h30 after 1889 P118 + 1892 P121 v5!) × Catharina BRIŠEC? [~ — cf. the BRINEC-tension P122 h26!], half smallholder's daughter, 20, GRIBLJE 24 (the 2nd marriage evidence of h24 after 1895 P124!) = ★ the DOUBLE-GRIBLJE wedding (h30 × h24); parents: Johann Legina ¼ smallholder × Dorothea Hrižan? [~] / Mathias Brišec ½ smallholder × Barbara Jakobič? [~ — the JAKOBIČ-link to the P122 h26 parent Georg Jakobič!]; witnesses: Johan Brišec + Georg Legina ¼ smallholder; the guardianship permission: the marriage banns of the Griblje commune May 17, 1902 no: 2, by the guardianship permission && uml. rovetja [~] from the c.k. district court of Črnomelj from May 1, 1902 P62/99 18. [~ — the court decision 11 days before the wedding!]; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04455",
    year: 1902,
    scan: 117,
    page: 116,
    whatSi: "poroka (12. 5. 1902, vpis 4) — nevesta Catharina BRIŠEC? [~], ½ gbl. Tochter, 20, GRIBLJE 24 (2. poročni dokaz h24 po 1895 P124 — 7 let vrzel!) × Nicolaus Legina? [~], ¼ griblar, 43, GRIBLJE 30 (3. POROČNI DOKAZ!) = DRUBEL-GRIBLJE poroka; oče Mathias Brišec ½ griblar × Barbara Jakobič? [~] — BRIŠEC/BRINEC-tension (P122 h26 Catharina BRINEC oče Georg JAKOBIČ — isti Jakobič-krog? odprto!); nadvarstveno dovoljenje okrajnega sodišča Črnomelj (1. maja 1902 — za nevesto 20!); duhovnik Jos. Rauy",
    whatEn: "marriage (May 12, 1902, entry 4) — the bride Catharina BRIŠEC? [~], half smallholder's daughter, 20, GRIBLJE 24 (the 2nd marriage evidence of h24 after 1895 P124 — a 7-year gap!) × Nicolaus Legina? [~], quarter smallholder, 43, GRIBLJE 30 (the 3rd MARRIAGE EVIDENCE!) = the DOUBLE-GRIBLJE wedding; father Mathias Brišec ½ smallholder × Barbara Jakobič? [~] — the BRIŠEC/BRINEC-tension (the P122 h26 Catharina BRINEC father Georg JAKOBIČ — the same Jakobič circle? open!); the guardianship permission of the district court of Črnomelj (May 1, 1902 — for the 20-year-old bride!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  // ——— P132 razširitev: POROČNA KNJIGA 04455 — polno leto 1903 (skeni 118–121 ==
  // strani 117–120; Pag. == sken − 1, 18. potrditev; rokopisna glava »1903.« na
  // s118 potrjena — P131-lead!) — P132-lead KOREKCIJA ×2: »min 5 vpisov
  // s118–s119« → **20 vpisov s118–s121** (4× podcenjeno — največja lead-napaka
  // linije!) + v1 nevesta »Žunjič?« → Žunič [~ Žumič]. VELIKA TISKANA GLAVA
  // »1904.« na s122 = P133 LEAD (v1–v5 = Febr 8 ×5 = MASA!). 20 vpisov
  // obojestransko = Febr 3 + Febr 9 ×3 + Febr 16 ×4 + Febr 23 ×2 (v9/v10
  // »März«-prevarda zavrnjena z zoomom 8× — ponedeljkovski vzorec!) + Jun 7 +
  // Jun 22 ×2 + Jul 6 + Jul 27 + Avg 3 + Avg 17 + Sept 13 + Okt 12 + Nov 23.
  // 8 GRIBLJE porok / 12 poročnih blokov (h11 v1 1. POROČNI DOKAZ + h65/h41 v3
  // DRUBEL 1. dokaza + h46 v9 2. dokaz + h56 v11 1. dokaz [DVOJNI DISPENS!] +
  // h11 v12 2. blok + h9 v12 1. dokaz + h6 v14 1. dokaz + h20/h48 v17 DRUBEL
  // 1. dokaza + h50 v20 1. dokaz + h44 v20 2. dokaz) — vitals 599 → **611**;
  // bloki 04455 82 → **94**; sidra 75 → **87** (+1903:12); p80 hiše 58 + PT
  // luknja 12 NESPREMENJENA. NOVELE: ★ v11 DVOJNI
  // DISPENS 1. STOPNJE SCHWÄGERSCHAFT (fb. Ordinariat Laibach št: 2244 + deželna
  // vlada št: 4444 — linijski rekord!) + ★ ¾ GRIBLAR NOVI NAJVIŠJI ULOMEK (v16
  // Kozjan Božakovo 43 — oče+tan!) + ★ CROSS-ENTRY ×4 (v1-ženin priča v12 ·
  // v1-priča priča v12 · v11-ženin priča v17 · v13-ženin priča v19!) + ★
  // BRAT-SESTRA ×2 (v12 ženin = brat v1-neveste h11! · v19 ženin = brat
  // v13-neveste Vranoviče 10!) + ★ 4. NEZAKONSKI ženin (v18 Mische — oče ni
  // vpisan!) + ★ 1. HÄUSLERIN (v18 Adamič!) + ★ nove vasi/fare: Božakovo 43 pf.
  // Metlika · Sodji vrh 11 pf. SEMIČ · Boginja vas 14 · Bilonje? 32 · Mavhe? 10
  // · občina LOKA · Zastava 8+9 · Grišiče? 35 · Vranoviče 10+27+29 + ★ oklicni
  // list ×5 + deželna vlada ×2 (št: 3254 + 4444!) + ★ status-vaha güblar/griblar
  // + Hübler/Gübler G/H ×7 + 'Kofre' [~] ×4 + zervljak? [~] + güblark. [~] +
  // Invohner 1. dokaz + mreže: HARAŠINIČ ×10 · JAKOFČIČ/JAKOBČIČ ×10 (dve
  // pisavi!) · PEZDIREC ×7 (8. leto!) · ŽUNIČ ×5 · KAMBIČ ×6 · JURAJEVČIČ ×5 ·
  // MÜCK/MILEK ×6 · KRIŽAN ×4 · ŠTRUCELJ 3. leto · DRAGOŠ 11. leto · KLEPEC 17.
  // leto · ŽUPANIČ Krasinec 18 4. dokaz hiše + NOVI priimki ×20+. Rauy 19/20 +
  // Dostál kaplan 1/20 (v18 — 2. dokaz!).
  // Dokaz: research/issue17/parish-marriage-1903.json; verifikator:
  // scripts/p132_parish_marriage_1903.py --check (I1–I11).
  {
    houseNo: "11",
    bookSignature: "04455",
    year: 1903,
    scan: 118,
    page: 117,
    whatSi: "poroka (3. 2. 1903, vpis 1) — nevesta Agnes ŽUNIČ [~ Žumič; P131-lead »Žunjič?« KOREKCIJA — brez j!], ½ gbl. Tochter, 20, GRIBLJE 11 (1. POROČNI DOKAZ h11!) × Johann Adamič, ½ güblarštofn [~ — cf. status-vaha G/H/ü/i], 25, Dragoše [~ Dragatuš?] 1; starši neveste: Matthias Žunič ¼ Hübler [~ Gübler] × Catharina DRAGOŠ (DRAGOŠ 11. leto mreže 1886–1903!); starši ženina: Johann Adamič ½ griblar × Barbara Milek [~ Mück]; priče: Marcus KLOBUČAR [~ '?äußer' — morda Häusler] + Georg Žunič ½ griblar; zglasmica občine Adlešič od 20/1. 1903 št: 33 + mündlich väterliche Einwilligung; duhovnik Jos. Rauy — ★ P132-ODPRTA GRIBLJE-poroka (h11 = tudi v12-ženinova hiša — BRAT-SESTRA!)",
    whatEn: "marriage (Feb 3, 1903, entry 1) — the bride Agnes ŽUNIČ [~ Žumič; the P131-lead »Žunjič?« CORRECTION — without j!], half smallholder's daughter, 20, GRIBLJE 11 (the 1st MARRIAGE EVIDENCE of h11!) × Johann Adamič, half güblar-hold [~ — cf. the status-vowel G/H/ü/i], 25, Dragoše [~ Dragatuš?] 1; the bride's parents: Matthias Žunič ¼ Hübler [~ Gübler] × Catharina DRAGOŠ (DRAGOŠ the 11th year of the network 1886–1903!); the groom's parents: Johann Adamič ½ smallholder × Barbara Milek [~ Mück]; witnesses: Marcus KLOBUČAR [~ '?äußer' — perhaps Häusler] + Georg Žunič ½ smallholder; certificate of the Adlešič commune from Jan 20, 1903 no: 33 + verbal paternal consent; priest Jos. Rauy — ★ the P132-OPENING GRIBLJE-wedding (h11 = also the v12 groom's house — BROTHER-SISTER!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04455",
    year: 1903,
    scan: 118,
    page: 117,
    whatSi: "poroka (9. 2. 1903, vpis 3) — ženin Matthias MÜCK [~ Milek], ½ griblarštofa, 25, GRIBLJE 65 (1. POROČNI DOKAZ h65!) × Maria Huestič [~ Hrustič/Husič], ½ griblarštofa, 20, GRIBLJE 41 (1. POROČNI DOKAZ h41!) = ★ DRUBEL-GRIBLJE poroka; starši: Matthias Mück ½ griblar × Catharina HARAŠINIČ [~ G/Š] / Matthias Huestič ¼ griblar × Agnes Jakobčič; priče: Matthias Harašinič + Michael PEZDIREC ½ griblar (8. leto mreže!); ★ 1. občina-GRIBLJE zglašnica (od 1/2. 1903 štev: 24) + mündlich väterlich fürwilligt; duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 9, 1903, entry 3) — the groom Matthias MÜCK [~ Milek], half smallholder-hold, 25, GRIBLJE 65 (the 1st MARRIAGE EVIDENCE of h65!) × Maria Huestič [~ Hrustič/Husič], half smallholder-hold, 20, GRIBLJE 41 (the 1st MARRIAGE EVIDENCE of h41!) = ★ the DOUBLE-GRIBLJE wedding; parents: Matthias Mück ½ smallholder × Catharina HARAŠINIČ [~ G/Š] / Matthias Huestič ¼ smallholder × Agnes Jakobčič; witnesses: Matthias Harašinič + Michael PEZDIREC ½ smallholder (the 8th year of the network!); ★ the 1st GRIBLJE-commune certificate (from Feb 1, 1903 no: 24) + verbally paternally consented; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04455",
    year: 1903,
    scan: 118,
    page: 117,
    whatSi: "poroka (9. 2. 1903, vpis 3) — nevesta Maria HUESTIČ [~ Hrustič/Husič], ½ griblarštofa, 20, GRIBLJE 41 (1. POROČNI DOKAZ h41!; h41 že v krstnem vzorcu 1890 P85 — 13 let čakanja!) × Matthias Mück [~ Milek], ½ griblarštofa, 25, GRIBLJE 65 (1. POROČNI DOKAZ!) = DRUBEL-GRIBLJE poroka; oče Matthias Huestič ¼ griblar × Agnes Jakobčič (JAKOBČIČ-oblika vs JAKOFČIČ v5/v8/v10!); zglasmica občine Griblje 1/2. štev: 24; duhovnik Jos. Rauy — h41 tudi P133-lead v2/1904 ženinova hiša (Georg Perdinec?)",
    whatEn: "marriage (Feb 9, 1903, entry 3) — the bride Maria HUESTIČ [~ Hrustič/Husič], half smallholder-hold, 20, GRIBLJE 41 (the 1st MARRIAGE EVIDENCE of h41!; h41 already in the 1890 baptism sample P85 — 13 years of waiting!) × Matthias Mück [~ Milek], half smallholder-hold, 25, GRIBLJE 65 (the 1st MARRIAGE EVIDENCE!) = the DOUBLE-GRIBLJE wedding; father Matthias Huestič ¼ smallholder × Agnes Jakobčič (the JAKOBČIČ-form vs JAKOFČIČ in v5/v8/v10!); the Griblje commune certificate Feb 1 no: 24; priest Jos. Rauy — h41 also the P133-lead v2/1904 groom's house (Georg Perdinec?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04455",
    year: 1903,
    scan: 119,
    page: 118,
    whatSi: "poroka (23. 2. 1903, vpis 9) — nevesta Catharina KRIŽAN, ½ gbl. Tochter, 28, GRIBLJE 46 (2. poročni dokaz h46 po 1898 P127 v20 — 5 let vrzel!) × Jakob Bohte, ½ gbl. Kofre [~ NEREŠENO kvalifikator ×4!], 24, Zastava 9; starši: Jakob Bohte ¼ griblar × Agnes Majerle? [~] / Johann Križan ¼ gübler [~] × Catharina Mück [~ Milek]; priče: Nicol. BRODARIČ (2. dokaz v letu — tudi v5!) + Georg Mavec ½ gbl.; zglasmica občine Loka (NOVA občina!) od 15. febr. št: 50; duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 23, 1903, entry 9) — the bride Catharina KRIŽAN, half smallholder's daughter, 28, GRIBLJE 46 (the 2nd marriage evidence of h46 after 1898 P127 v20 — a 5-year gap!) × Jakob Bohte, half gbl. Kofre [~ UNRESOLVED qualifier ×4!], 24, Zastava 9; parents: Jakob Bohte ¼ smallholder × Agnes Majerle? [~] / Johann Križan ¼ gübler [~] × Catharina Mück [~ Milek]; witnesses: Nicol. BRODARIČ (the 2nd evidence in the year — also v5!) + Georg Mavec ½ gbl.; certificate of the Loka commune (A NEW commune!) from Feb 15 no: 50; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04455",
    year: 1903,
    scan: 120,
    page: 119,
    whatSi: "poroka (22. 6. 1903, vpis 12) — ženin Johann ŽUNIČ, ½ griblar, 25, GRIBLJE 11 (2. POROČNI DOKAZ h11 — 2. poroka hiše v ENELETU!) × Maria Jakofčič, ½ gbl. Tochter, 23, GRIBLJE 9 (1. POROČNI DOKAZ h9!) = ★ DRUBEL-GRIBLJE poroka; starši ženina: Matthias Žunič ½ gübler [~ status-varianca vs v1 ¼ Hübler!] × Catharina DRAGOŠ (×2 v letu — v1 mati!) = ★ ženin = BRAT v1-neveste Agnes Žunič!; starši neveste: Johann Jakofčič ½ gbl. × Maria Jakofčič; ★ priči: Johann ADAMIČ ½ [= v1-ŽENIN kot priča!] + Georg ŽUNIČ ½ gbl. [= v1-PRIČA ponovno!] — CROSS-ENTRY REPEAT (vzorec P128 v1→v4!); zglasmica občine Gribelj? [~ varianta!] od 22. junija št: 77 + polnoletnost neveste (sodišče Črnomelj 27. maja); duhovnik Jos. Rauy",
    whatEn: "marriage (Jun 22, 1903, entry 12) — the groom Johann ŽUNIČ, half smallholder, 25, GRIBLJE 11 (the 2nd MARRIAGE EVIDENCE of h11 — the house's 2nd wedding IN ONE YEAR!) × Maria Jakofčič, half smallholder's daughter, 23, GRIBLJE 9 (the 1st MARRIAGE EVIDENCE of h9!) = ★ the DOUBLE-GRIBLJE wedding; the groom's parents: Matthias Žunič ½ gübler [~ status-variance vs v1 ¼ Hübler!] × Catharina DRAGOŠ (×2 in the year — the v1 mother!) = ★ the groom = the BROTHER of the v1-bride Agnes Žunič!; the bride's parents: Johann Jakofčič ½ gbl. × Maria Jakofčič; ★ witnesses: Johann ADAMIČ ½ [= the v1-GROOM as witness!] + Georg ŽUNIČ ½ gbl. [= the v1-WITNESS again!] — the CROSS-ENTRY REPEAT (the P128 v1→v4 pattern!); certificate of the Gribelj? [~ variant!] commune from Jun 22 no: 77 + the bride's majority (the Črnomelj court May 27); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04455",
    year: 1903,
    scan: 120,
    page: 119,
    whatSi: "poroka (22. 6. 1903, vpis 12) — nevesta Maria JAKOFČIČ, ½ gbl. Tochter, 23, GRIBLJE 9 (1. POROČNI DOKAZ h9!) × Johann Žunič, ½ griblar, 25, GRIBLJE 11 (2. POROČNI DOKAZ!) = DRUBEL-GRIBLJE poroka; starši neveste: Johann Jakofčič ½ gbl. × Maria Jakofčič (obe ISTI priimek!); zglasmica občine Gribelj? od 22. junija št: 77; duhovnik Jos. Rauy",
    whatEn: "marriage (Jun 22, 1903, entry 12) — the bride Maria JAKOFČIČ, half smallholder's daughter, 23, GRIBLJE 9 (the 1st MARRIAGE EVIDENCE of h9!) × Johann Žunič, half smallholder, 25, GRIBLJE 11 (the 2nd MARRIAGE EVIDENCE!) = the DOUBLE-GRIBLJE wedding; the bride's parents: Johann Jakofčič ½ gbl. × Maria Jakofčič (both the SAME surname!); the Gribelj? commune certificate Jun 22 no: 77; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04455",
    year: 1903,
    scan: 120,
    page: 119,
    whatSi: "poroka (6. 7. 1903, vpis 14) — ženin Georg JAKOBČIČ [~], ¼ gübler [~], 24, GRIBLJE 6 (1. POROČNI DOKAZ h6 — NAJNIŽJA hišna št. 1903!) × Catharina Jakobčič [~], ¼ gbl. Tocht., 22, Cerkvišče? 16 = ★ ISTI PRIIMEK-par (cf. v7 Harašinič!) + JAKOBČIČ ×5 v enem vpisu; starši: Matthias Jakobčič ½ gübler × Ana Željko? [~ Želiko] / Peter Jakobčič ¼ gübler × Anna Mihelčič; priče: Josef Željko? [~] + Mathias LOPAVEC ½ gübler (NOV!); zglasmica občine Griblje 5. julija št: 86 + očetovo ustno dovoljenje; duhovnik Jos. Rauy — nevestina hiša Cerkvišče 16 = 2. poroka iz iste hiše v letu (v10 — RAZLIČNA očeta!)",
    whatEn: "marriage (Jul 6, 1903, entry 14) — the groom Georg JAKOBČIČ [~], quarter gübler [~], 24, GRIBLJE 6 (the 1st MARRIAGE EVIDENCE of h6 — the LOWEST house number of 1903!) × Catharina Jakobčič [~], quarter gbl. daughter, 22, Cerkvišče? 16 = ★ the SAME-SURNAME couple (cf. v7 Harašinič!) + JAKOBČIČ ×5 in one entry; parents: Matthias Jakobčič ½ gübler × Ana Željko? [~ Želiko] / Peter Jakobčič ¼ gübler × Anna Mihelčič; witnesses: Josef Željko? [~] + Mathias LOPAVEC ½ gübler (NEW!); the Griblje commune certificate Jul 5 no: 86 + the father's verbal consent; priest Jos. Rauy — the bride's house Cerkvišče 16 = the house's 2nd wedding in the year (v10 — DIFFERENT fathers!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04455",
    year: 1903,
    scan: 121,
    page: 120,
    whatSi: "poroka (17. 8. 1903, vpis 17) — ženin Georg PEZDIREC, ½ griblarštofa Kofre [~], 30, GRIBLJE 20 (1. POROČNI DOKAZ h20!; h20 = 2. poročni dokaz 1899 P128 v4!) × Catharina Berkoprec? [~ Verkoprec], ¼ griblarin, 27, GRIBLJE 48 (1. POROČNI DOKAZ h48!; h48 že v poročnem okvirju 1898 P127 v2!) = ★ DRUBEL-GRIBLJE poroka; ★ PEZDIREC ×3 v enem vpisu (ženin + oba starša: Peter Pezdirec ½ griblar × Cathar. Debelec? [~]) / Johann KLOBUČAR ¼ gübler × Barbara Pezdirec; priče: Peter JAKLJEVIČ (P130-mreža!) + Georg KRALJ ¼ griblar [= v11-ŽENIN kot priča — cross-entry #3!]; zglasmica občine Griblje 16. avgusta št: 87; duhovnik Jos. Rauy",
    whatEn: "marriage (Aug 17, 1903, entry 17) — the groom Georg PEZDIREC, half smallholder-hold Kofre [~], 30, GRIBLJE 20 (the 1st MARRIAGE EVIDENCE of h20!; h20 = the 2nd marriage evidence 1899 P128 v4!) × Catharina Berkoprec? [~ Verkoprec], quarter smallholderess, 27, GRIBLJE 48 (the 1st MARRIAGE EVIDENCE of h48!; h48 already in the 1898 marriage frame P127 v2!) = ★ the DOUBLE-GRIBLJE wedding; ★ PEZDIREC ×3 in one entry (the groom + both parents: Peter Pezdirec ½ smallholder × Cathar. Debelec? [~]) / Johann KLOBUČAR ¼ gübler × Barbara Pezdirec; witnesses: Peter JAKLJEVIČ (the P130 network!) + Georg KRALJ ¼ smallholder [= the v11-GROOM as witness — cross-entry #3!]; the Griblje commune certificate Aug 16 no: 87; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04455",
    year: 1903,
    scan: 121,
    page: 120,
    whatSi: "poroka (17. 8. 1903, vpis 17) — nevesta Catharina BERKOPREC? [~ Verkoprec — NOV priimek!], ¼ griblarin, 27, GRIBLJE 48 (1. POROČNI DOKAZ h48!) × Georg Pezdirec, ½ griblarštofa Kofre [~], 30, GRIBLJE 20 (1. POROČNI DOKAZ!) = DRUBEL-GRIBLJE poroka; oče neveste: Johann Klobučar ¼ gübler × Barbara PEZDIREC (PEZDIREC ×3!); zglasmica občine Griblje 16. avgusta št: 87; duhovnik Jos. Rauy",
    whatEn: "marriage (Aug 17, 1903, entry 17) — the bride Catharina BERKOPREC? [~ Verkoprec — a NEW surname!], quarter smallholderess, 27, GRIBLJE 48 (the 1st MARRIAGE EVIDENCE of h48!) × Georg Pezdirec, half smallholder-hold Kofre [~], 30, GRIBLJE 20 (the 1st MARRIAGE EVIDENCE!) = the DOUBLE-GRIBLJE wedding; the bride's father: Johann Klobučar ¼ gübler × Barbara PEZDIREC (PEZDIREC ×3!); the Griblje commune certificate Aug 16 no: 87; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "50",
    bookSignature: "04455",
    year: 1903,
    scan: 121,
    page: 120,
    whatSi: "poroka (23. 11. 1903, vpis 20) — ženin Bartholomäus JERČINOVIČ? [~ — NOV priimek!], Invohner [1. dokaz statusa linije!], 27, GRIBLJE 50 (1. POROČNI DOKAZ h50!) × Dorothea ŠTRUCELJ, ½ güblark. Tochter [~ ženska forma!], 24, GRIBLJE 44 (2. poročni dokaz h44 po 1898 P127 v1!) = ★ DRUBEL-GRIBLJE poroka; starši: Matthias Jerčinovič Besitzer? [~] × Maria Sopec? [~] / Matthias Štrucelj ½ griblar × Agnes Klobučar; priče: Klobučar Fabian? [~ Marcus?] + Jerčinovič Inwohner?/Besitzer? [~ — morda oče kot priča]; zglasmica: Štrivnik? [~ NEREŠENO mesto] od 20/11. št: [—] + oklicni list za ženina od župnega urada v Štrivniku? od 22/11. (5. dokaz!); duhovnik Jos. Rauy",
    whatEn: "marriage (Nov 23, 1903, entry 20) — the groom Bartholomäus JERČINOVIČ? [~ — a NEW surname!], lodger [the 1st evidence of the status in the line!], 27, GRIBLJE 50 (the 1st MARRIAGE EVIDENCE of h50!) × Dorothea ŠTRUCELJ, half güblark daughter [~ the female form!], 24, GRIBLJE 44 (the 2nd marriage evidence of h44 after 1898 P127 v1!) = ★ the DOUBLE-GRIBLJE wedding; parents: Matthias Jerčinovič Besitzer? [~] × Maria Sopec? [~] / Matthias Štrucelj ½ smallholder × Agnes Klobučar; witnesses: Klobučar Fabian? [~ Marcus?] + Jerčinovič Inwohner?/Besitzer? [~ — perhaps the father as witness]; certificate: Štrivnik? [~ UNRESOLVED place] from Nov 20 no: [—] + the groom's banns list from the parish office in Štrivnik? from Nov 22 (the 5th evidence!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04455",
    year: 1903,
    scan: 121,
    page: 120,
    whatSi: "poroka (23. 11. 1903, vpis 20) — nevesta Dorothea ŠTRUCELJ, ½ güblark. Tochter [~], 24, GRIBLJE 44 (2. poročni dokaz h44 po 1898 P127 v1 — 5 let vrzel!) × Bartholomäus Jerčinovič? [~], Invohner, 27, GRIBLJE 50 (1. POROČNI DOKAZ!) = DRUBEL-GRIBLJE poroka; ŠTRUCELJ 3. leto mreže (P130 mati 1900→1901 → 1903!); starši neveste: Matthias Štrucelj ½ griblar × Agnes Klobučar (KLOBUČAR ×3 v letu — v1 priča + v17 oče + v20!); duhovnik Jos. Rauy",
    whatEn: "marriage (Nov 23, 1903, entry 20) — the bride Dorothea ŠTRUCELJ, half güblark daughter [~], 24, GRIBLJE 44 (the 2nd marriage evidence of h44 after 1898 P127 v1 — a 5-year gap!) × Bartholomäus Jerčinovič? [~], lodger, 27, GRIBLJE 50 (the 1st MARRIAGE EVIDENCE!) = the DOUBLE-GRIBLJE wedding; ŠTRUCELJ the 3rd year of the network (P130 mother 1900→1901 → 1903!); the bride's parents: Matthias Štrucelj ½ smallholder × Agnes Klobučar (KLOBUČAR ×3 in the year — the v1 witness + the v17 father + v20!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "56",
    bookSignature: "04455",
    year: 1903,
    scan: 120,
    page: 119,
    whatSi: "poroka (7. 6. 1903, vpis 11) — nevesta Dorothea ŠIMEC, ¼ griblarin, 47, GRIBLJE 56 (1. POROČNI DOKAZ h56!) × Georg Kralj [~], ½ griblar, 61 (2. najstarejši ženin linije za 66 P128 v1!), Mavhe? 10 [~ NOVA VAS?] = ★ DVOJNI DISPENS 1. STOPNJE SCHWÄGERSCHAFT (fb. Ordinariat Laibach ddo 3/6. 1903 št: 2244 + k. k. Landesregierung ddo 27/2. 1903 št: 4444 — NAJBLIŽJA stopnja + 2. dispens afinosti linije [P130 v1 2. stopnje!] = linijski rekord dispensev!); starši: Georg Kralj ½ gübler × Anna Yaklič? [~ Jaklič] / Peter PEZDIREC ¼ griblar × Anna Mück [~ Milek]; priče: Peter Kralj + Peter PEZDIREC ½ griblar [= OČE NEVESTE kot priča!]; zglasmica občine Podzemelj od 1/6. štev: 11; duhovnik Jos. Rauy — par 61×47 = 108 let = 2. rekord-par linije (za 134 P128 v1!); ŠIMEC-mreža (v4 nevesta + cf. P127 h54!)",
    whatEn: "marriage (Jun 7, 1903, entry 11) — the bride Dorothea ŠIMEC, quarter smallholderess, 47, GRIBLJE 56 (the 1st MARRIAGE EVIDENCE of h56!) × Georg Kralj [~], half smallholder, 61 (the 2nd oldest groom of the line after 66 P128 v1!), Mavhe? 10 [~ A NEW VILLAGE?] = ★ the DOUBLE DISPENSATION of the 1st DEGREE OF AFFINITY (the Laibach ordinariate ddo Jun 3, 1903 no: 2244 + the k. k. provincial government ddo Feb 27, 1903 no: 4444 — the CLOSEST degree + the 2nd affinity dispensation of the line [P130 v1 2nd degree!] = the line record of dispensations!); parents: Georg Kralj ½ gübler × Anna Yaklič? [~ Jaklič] / Peter PEZDIREC ¼ smallholder × Anna Mück [~ Milek]; witnesses: Peter Kralj + Peter PEZDIREC ½ smallholder [= the BRIDE'S FATHER as witness!]; certificate of the Podzemelj commune from Jun 1 no: 11; priest Jos. Rauy — the couple 61×47 = 108 years = the 2nd record couple of the line (after 134 P128 v1!); the ŠIMEC network (the v4 bride + cf. P127 h54!)",
    status: "DOCUMENTED",
  },
  // ——— P133 razširitev: POROČNA KNJIGA 04455 — polno leto 1904 (skeni 122–125 ==
  // strani 121–124; VELIKA TISKANA GLAVA »1904.« na s122 POTRJENA — P132 lead!;
  // rokopisna glava »1905.« na s125 = P134 LEAD; 15 vpisov obojestransko =
  // P133-lead »min 5 s122–s123« 3× pocenjen; razpored 5+4+5+1) — vpisi z
  // Griblji (5 porok / 8 poročnih blokov: h42 v2 ženin 2. dokaz + h32 v5 ženin
  // 3. dokaz + h38 v5 nevesta 1. DOKAZ + h38 v8 ženin 2. blok = BRAT-SESTRA +
  // h39 v8 nevesta 2. dokaz + h62 v13 ženin 3. dokaz + h46 v14 ženin 3. dokaz
  // + h22 v14 nevesta 3. dokaz = 3 DRUBEL!): NOVELE: ★ ⅜ NOVI ULOMEK LINIJE
  // (v13 nevesta+oče!) + ★ NAJMLAJŠI ŽENIN LINIJE 18 (v2!) + ★ MASA-REKORD 5
  // porok 8.2. + ★ DVOJNA KRVNA DISPENSA (v6: 2. koleno №697 + 4. koleno
  // №2814!) + 2. krvna dispensa (v10 3. koleno №2063) + ★ 6 DRUŽINSKIH
  // KONTINUITET (h42 PERDINEC 1894→04 · h32 STRAUS 1888→ŠRAUS 04 · h39 SIMEC
  // 1897→04 · h62 KURE 1893+98→04 · h46 2. leto · h22 STRAUS 98→MILEK 04!) +
  // CROSS-ENTRY ×2 (v5-ženin Šraus priča v8 · v2-priča Kure = v13-oče!) +
  // NOVE VASI: Zemelj 17 + Vojna vas 18 pf. Črnomelj + Sirnica 4 pf. Črnomelj
  // + Boršt 18 + Prilozje 25 (4. hiša) + NOVE FARE: Dragatuš + Radovica
  // (oklicni) + mestna občina Metlika + občina Loka 2. + Vode? [~] + 1. ne-Rauy
  // duhovnik 1904 (Stan. Costal [~ Dostal?] v12) + deželna vlada №1992/1993
  // zapored + №22190 NAJVIŠJA + 1. TRGOVEC + 2 mrtvaška lista + Invohner-priče
  // ×2 + polnoletnost-glasila ×2. Dokaz: research/issue17/parish-marriage-1904.json;
  // verifikator: scripts/p133_parish_marriage_1904.py --check (I1–I11).
  {
    houseNo: "42",
    bookSignature: "04455",
    year: 1904,
    scan: 122,
    page: 121,
    whatSi: "poroka (8. 2. 1904, vpis 2) — ženin Georg Perdinec, ¼ gübler, 18 (★ NAJMLAJŠI ŽENIN LINIJE 1886–1904 — prej min 20!), GRIBLJE 42 (2. poročni dokaz h42 — 1894 P123 nevesta Margareth PERDINEC = ★ PERDINEC-kontinuiteta 10 let!) × Catharina Jurajevčič, ½ güblerštoft [~], 20, Krasinec 21; starši: Georg Perdinec ¼ gübler × Dorothea KRIŽAN / Matthias Jurajevčič ½ gübler × Maria Šimec; priče: Anton KURE [= v13-oče! CROSS-ENTRY] + Mich. Jurajevčič ½ gübler; zglasmica občine Griblje od 4/2. 04 št: 1 + zemljno dovolilje za zemljo (sodišče Črnomelj 13/1. 04 + deželna vlada Laibach 26/1. 1904 št: 1992 — cf. v3 № 1993 zapored!) + ustno očetovo dovoljenje (mlada nevesta); duhovnik Jos. Rauy — P132-lead KOREKCIJA h41 → h42 + Perdinec POTRJEN",
    whatEn: "marriage (Feb 8, 1904, entry 2) — the groom Georg Perdinec, quarter smallholder, 18 (★ the YOUNGEST GROOM of the line 1886–1904 — previously min 20!), GRIBLJE 42 (the 2nd marriage evidence of h42 — 1894 P123 the bride Margareth PERDINEC = ★ the PERDINEC continuity of 10 years!) × Catharina Jurajevčič, half smallholder-hold [~], 20, Krasinec 21; parents: Georg Perdinec ¼ smallholder × Dorothea KRIŽAN / Matthias Jurajevčič ½ smallholder × Maria Šimec; witnesses: Anton KURE [= the v13 father! CROSS-ENTRY] + Mich. Jurajevčič ½ smallholder; certificate of the Griblje commune from Feb 4, 1904 no: 1 + the land permission (the Črnomelj court Jan 13, 1904 + the Laibach provincial government Jan 26, 1904 no: 1992 — cf. v3 no: 1993 consecutive!) + the father's verbal consent (the young bride); priest Jos. Rauy — the P132-lead CORRECTION h41 → h42 + Perdinec CONFIRMED",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04455",
    year: 1904,
    scan: 122,
    page: 121,
    whatSi: "poroka (8. 2. 1904, vpis 5) — ženin Matthias ŠRAUS [~ Straus], ¼ gübler, 42, GRIBLJE 32 (3. poročni dokaz h32 — 1888 P117 Mathias STRAUS + 1889 P118 Mathias Urb = ★ STRAUS/ŠRAUS-kontinuiteta 16 let, dve pisavi!) × Margareth Šimec, Gänslerhofstochter [~ pisava 'hofstoftn'], 28, GRIBLJE 38 (1. POROČNI DOKAZ h38 = GANSLER-hiša!) = ★ DRUBEL-GRIBLJE; starši: Marcus Šraus ¼ gübler × Catharina DRAGOŠ (DRAGOŠ 12. leto!) / Georg Šimec gänsler × Anna KRIŽAN (= v8 BRAT-SESTRA!); priče: Johann Dragoš ½ gübler + Nicol(aus) Željko [~] ¼ gbl (= v8-priča!); zglasmica občine Griblje od 1/2. 1904 št: 2; duhovnik Jos. Rauy — P132-lead KOREKCIJA: nevesta h30 → h38 + ženin 'Šimec' → ŠRAUS",
    whatEn: "marriage (Feb 8, 1904, entry 5) — the groom Matthias ŠRAUS [~ Straus], quarter smallholder, 42, GRIBLJE 32 (the 3rd marriage evidence of h32 — 1888 P117 Mathias STRAUS + 1889 P118 Mathias Urb = ★ the STRAUS/ŠRAUS continuity of 16 years, two spellings!) × Margareth Šimec, the Gänsler-farm daughter [~ spelling 'hofstoftn'], 28, GRIBLJE 38 (the 1st MARRIAGE EVIDENCE of h38 = the GANSLER farm!) = ★ the DOUBLE-GRIBLJE wedding; parents: Marcus Šraus ¼ smallholder × Catharina DRAGOŠ (DRAGOŠ the 12th year!) / Georg Šimec gänsler × Anna KRIŽAN (= the v8 BROTHER-SISTER!); witnesses: Johann Dragoš ½ smallholder + Nicol(aus) Željko [~] ¼ smallholder (= the v8 witness!); certificate of the Griblje commune from Feb 1, 1904 no: 2; priest Jos. Rauy — the P132-lead CORRECTION: the bride h30 → h38 + the groom 'Šimec' → ŠRAUS",
    status: "DOCUMENTED",
  },
  {
    houseNo: "38",
    bookSignature: "04455",
    year: 1904,
    scan: 122,
    page: 121,
    whatSi: "poroka (8. 2. 1904, vpis 5) — nevesta Margareth ŠIMEC, Gänslerhofstochter [~], 28, GRIBLJE 38 (1. POROČNI DOKAZ h38 — GANSLER-hiša: oče Georg Šimec gänsler!) × Matthias Šraus [~], ¼ gübler, 42, GRIBLJE 32 (3. dokaz) = ★ DRUBEL; starši: Georg Šimec gänsler × Anna KRIŽAN (= starši v8-ženina — BRAT-SESTRA!) / Marcus Šraus ¼ gübler × Catharina Dragoš; priče Johann Dragoš + Nicol. Željko; zglasmica občine Griblje 1/2. 1904 št: 2; duhovnik Jos. Rauy — h38 = edina NOVA poročna hiša 1904, a takoj 2 bloka (v5 + v8)!",
    whatEn: "marriage (Feb 8, 1904, entry 5) — the bride Margareth ŠIMEC, the Gänsler-farm daughter [~], 28, GRIBLJE 38 (the 1st MARRIAGE EVIDENCE of h38 — the GANSLER farm: the father Georg Šimec gänsler!) × Matthias Šraus [~], quarter smallholder, 42, GRIBLJE 32 (the 3rd evidence) = ★ the DOUBLE wedding; parents: Georg Šimec gänsler × Anna KRIŽAN (= the v8 groom's parents — BROTHER-SISTER!) / Marcus Šraus ¼ smallholder × Catharina Dragoš; witnesses Johann Dragoš + Nicol. Željko; the Griblje commune certificate Feb 1, 1904 no: 2; priest Jos. Rauy — h38 = the only NEW marriage house of 1904, yet immediately 2 blocks (v5 + v8)!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "38",
    bookSignature: "04455",
    year: 1904,
    scan: 123,
    page: 122,
    whatSi: "poroka (30. 5. 1904, vpis 8) — ženin Georg Šimec, gänsler, 22, GRIBLJE 38 (2. poročni dokaz h38 v ISTEM LETU = ★ BRAT-SESTRA v5/v8 — ista starša Georg Šimec gänsler × Anna KRIŽAN!) × Anna Šimec, ¼ güblers. Tochter [~], 21, GRIBLJE 39 (2. poročni dokaz h39 — 1897 P126 nevesta Maria SIMEC 17! = ★ ŠIMEC-kontinuiteta 7 let!) = DRUBEL + ISTI PRIIMEK Šimec ×4; starši: Georg Šimec gänsler × Anna Križan / Nicolaus Šimec ¼ gübler × Catharina Jakobčič; priče: Nicolaus ŽELJKO ¼ gbl (= v5-priča — 2×!) + Matthias ŠRAUS ¼ gbl (= v5-ŽENIN! CROSS-ENTRY — vzorec P128 v1→v4!); zglasmica občine Gribeljske [~] od 29. maja 1904 št: 6 + Br. glas polnoletnosti za OBOJE (okrajno sodišče Črnomelj 27/4. + 5/5. 1904!); duhovnik Jos. Rauy",
    whatEn: "marriage (May 30, 1904, entry 8) — the groom Georg Šimec, gänsler, 22, GRIBLJE 38 (the 2nd marriage evidence of h38 IN THE SAME YEAR = ★ BROTHER-SISTER v5/v8 — the same parents Georg Šimec gänsler × Anna KRIŽAN!) × Anna Šimec, quarter smallholder's daughter [~], 21, GRIBLJE 39 (the 2nd marriage evidence of h39 — 1897 P126 the bride Maria SIMEC 17! = ★ the ŠIMEC continuity of 7 years!) = DOUBLE + the SAME SURNAME Šimec ×4; parents: Georg Šimec gänsler × Anna Križan / Nicolaus Šimec ¼ smallholder × Catharina Jakobčič; witnesses: Nicolaus ŽELJKO ¼ smallholder (= the v5 witness — 2×!) + Matthias ŠRAUS ¼ smallholder (= the v5 GROOM! CROSS-ENTRY — the P128 v1→v4 pattern!); the Griblje commune certificate from May 29, 1904 no: 6 + the majority certificates for BOTH (the Črnomelj district court Apr 27 + May 5, 1904!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "39",
    bookSignature: "04455",
    year: 1904,
    scan: 123,
    page: 122,
    whatSi: "poroka (30. 5. 1904, vpis 8) — nevesta Anna ŠIMEC, ¼ güblers. Tochter [~], 21, GRIBLJE 39 (2. poročni dokaz h39 — 1897 P126 nevesta Maria SIMEC = ★ ŠIMEC-kontinuiteta 7 let!) × Georg Šimec, gänsler, 22, GRIBLJE 38 (2. dokaz — BRAT-SESTRA v5!) = DRUBEL + ISTI PRIIMEK; starši: Nicolaus Šimec ¼ gübler × Catharina JAKOBČIČ / Georg Šimec gänsler × Anna Križan; priče Nicolaus Željko + Matthias Šraus (= v5-ženin!); zglasmica občine Gribeljske 29. maja 1904 št: 6 + glas polnoletnosti za nevesto (sodišče Črnomelj 5/5. 1904); duhovnik Jos. Rauy — h39 tudi P134-lead (v2/1905 ženinova hiša Johann Markočič?)",
    whatEn: "marriage (May 30, 1904, entry 8) — the bride Anna ŠIMEC, quarter smallholder's daughter [~], 21, GRIBLJE 39 (the 2nd marriage evidence of h39 — 1897 P126 the bride Maria SIMEC = ★ the ŠIMEC continuity of 7 years!) × Georg Šimec, gänsler, 22, GRIBLJE 38 (the 2nd evidence — the v5 BROTHER-SISTER!) = DOUBLE + the SAME SURNAME; parents: Nicolaus Šimec ¼ smallholder × Catharina JAKOBČIČ / Georg Šimec gänsler × Anna Križan; witnesses Nicolaus Željko + Matthias Šraus (= the v5 groom!); the Griblje commune certificate May 29, 1904 no: 6 + the majority certificate for the bride (the Črnomelj court May 5, 1904); priest Jos. Rauy — h39 also the P134-lead (the v2/1905 groom's house Johann Markočič?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04455",
    year: 1904,
    scan: 124,
    page: 123,
    whatSi: "poroka (3. 10. 1904, vpis 13) — ženin Nikolaus Kure [~], ¼ güblerssohn, 28, GRIBLJE 62 (3. poročni dokaz h62 — 1893 P122 nevesta Anna KURE + 1898 P127 Maria KURE = ★ KURE-kontinuiteta 11 let!) × Anna Štefanič [~], ★ ⅜ güblers-hofsohn [~ ženska oblika — NOVI ULOMEK LINIJE!], 21, Otok 10 (= P132 v16-nevestina hiša Jurajevčič — 2. poroka hiše, drug priimek!); starši: Anton KURE ¼ gübler [= v2-PRIČA! CROSS-ENTRY] × Barbara KRIŽAN / Georg Štefanič ⅜ gübler × Marija Medoš [~]; priče: Nicolaus Kure ½ gbl + Georg Vlasič [~]; zglasmica občine Griblje od 2/10. 1904 št: 1 + zapustki? [~ 'Zamski'] in oklicni list nevestin od župnega vrada v DRAGATUŠU 2/10. 1904 št: 190 (NOVA FARNA REF.!) + očetovo ustno dovoljenje; duhovnik Jos. Rauy — KURE ×3 v vpisu (ženin + oče + priča!)",
    whatEn: "marriage (Oct 3, 1904, entry 13) — the groom Nikolaus Kure [~], quarter smallholder's son, 28, GRIBLJE 62 (the 3rd marriage evidence of h62 — 1893 P122 the bride Anna KURE + 1898 P127 Maria KURE = ★ the KURE continuity of 11 years!) × Anna Štefanič [~], ★ ⅜ smallholder-hold-son [~ female form — the NEW FRACTION of the line!], 21, Otok 10 (= the P132 v16 bride's house Jurajevčič — the house's 2nd wedding, a different surname!); parents: Anton KURE ¼ smallholder [= the v2 WITNESS! CROSS-ENTRY] × Barbara KRIŽAN / Georg Štefanič ⅜ smallholder × Marija Medoš [~]; witnesses: Nicolaus Kure ½ smallholder + Georg Vlasič [~]; the Griblje commune certificate from Oct 2, 1904 no: 1 + the inheritance? [~ 'Zamski'] and banns list of the bride from the Dragatuš parish office Oct 2, 1904 no: 190 (A NEW PARISH REFERENCE!) + the father's verbal consent; priest Jos. Rauy — KURE ×3 in the entry (the groom + father + witness!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04455",
    year: 1904,
    scan: 124,
    page: 123,
    whatSi: "poroka (7. 11. 1904, vpis 14) — ženin Anton Brodarič [~], ¼ gübler, 44, GRIBLJE 46 (3. POROČNI DOKAZ h46 — P127 1898 + P132 v9 1903: 3. leto zapored!) × Catharina Milek [~ Mück], ½ güblershofstochter [~], 28, GRIBLJE 22 (3. poročni dokaz h22 — 1898 P127 ×2: ženin Nicolaus STRAUS! = ★ STRAUS-hiša → zdaj MILEK, menjava družine!) = ★ DRUBEL-GRIBLJE; starši: Michael Brodarič ¼ gübler × Anna Adam (NOVI!) / Johann Milek ½ gübler × Maria PERDINEC; priče: Nikol. KRIŽAN + Martin Brodarič (½ gbl [~]) (= BRODARIČ ×3 v vpisu!); zglasmica občine Griblje od 6/11. 1904 št: 2 + oklicni list župnega vrada na RADOVICI 6/11. 1904 za nevesto (NOVA FARNA REF.!); duhovnik Jos. Rauy — BRODARIČ-mreža: cf. v9-mati Catharina Brodarič!",
    whatEn: "marriage (Nov 7, 1904, entry 14) — the groom Anton Brodarič [~], quarter smallholder, 44, GRIBLJE 46 (the 3rd MARRIAGE EVIDENCE of h46 — P127 1898 + P132 v9 1903: the 3rd year in a row!) × Catharina Milek [~ Mück], half smallholder-farm daughter [~], 28, GRIBLJE 22 (the 3rd marriage evidence of h22 — 1898 P127 ×2: the groom Nicolaus STRAUS! = ★ the STRAUS house → now MILEK, a family change!) = ★ the DOUBLE-GRIBLJE wedding; parents: Michael Brodarič ¼ smallholder × Anna Adam (NEW!) / Johann Milek ½ smallholder × Maria PERDINEC; witnesses: Nikol. KRIŽAN + Martin Brodarič (½ smallholder [~]) (= BRODARIČ ×3 in the entry!); the Griblje commune certificate from Nov 6, 1904 no: 2 + the banns list of the parish office at RADOVICA Nov 6, 1904 for the bride (A NEW PARISH REFERENCE!); priest Jos. Rauy — the BRODARIČ network: cf. the v9 mother Catharina Brodarič!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04455",
    year: 1904,
    scan: 124,
    page: 123,
    whatSi: "poroka (7. 11. 1904, vpis 14) — nevesta Catharina MILEK [~ Mück], ½ güblershofstochter [~], 28, GRIBLJE 22 (3. poročni dokaz h22 — 1898 P127 ×2 Nicolaus STRAUS = menjava družine STRAUS → MILEK!) × Anton Brodarič [~], ¼ gübler, 44, GRIBLJE 46 (3. dokaz — 3. leto zapored!) = ★ DRUBEL; starši: Johann Milek ½ gübler × Maria PERDINEC (5./5!) / Michael Brodarič ¼ gübler × Anna Adam; priče Nikol. Križan + Martin Brodarič; zglasmica občine Griblje 6/11. 1904 št: 2 + oklicni list na Radovici 6/11. 1904; duhovnik Jos. Rauy — MILEK/MÜCK dve pisavi (cf. P132 Mück/Milek!)",
    whatEn: "marriage (Nov 7, 1904, entry 14) — the bride Catharina MILEK [~ Mück], half smallholder-farm daughter [~], 28, GRIBLJE 22 (the 3rd marriage evidence of h22 — 1898 P127 ×2 Nicolaus STRAUS = the family change STRAUS → MILEK!) × Anton Brodarič [~], quarter smallholder, 44, GRIBLJE 46 (the 3rd evidence — the 3rd year in a row!) = ★ the DOUBLE wedding; parents: Johann Milek ½ smallholder × Maria PERDINEC (5th of 5!) / Michael Brodarič ¼ smallholder × Anna Adam; witnesses Nikol. Križan + Martin Brodarič; the Griblje commune certificate Nov 6, 1904 no: 2 + the banns list at Radovica Nov 6, 1904; priest Jos. Rauy — MILEK/MÜCK two spellings (cf. P132 Mück/Milek!)",
    status: "DOCUMENTED",
  },
  // ——— P134 razširitev: POROČNA KNJIGA 04455 — polno leto 1905 (skeni 125–129 ==
  // strani 124–128; ROKOPISNA GLAVA »1905.« na s125 POTRJENA — P133 lead!;
  // velika tiskana glava »Traunungs=Buč.« na s126/s127/s128; rokopisna glava
  // »1906« na s129 = P135 LEAD; 17 vpisov obojestransko = P134-lead »min 5
  // s125–s126« 3× pocenjen; razpored 3+4+4+5+1) — vpisi z Griblji (8 porok /
  // 13 poročnih blokov: h34 v2 ženin 3. dokaz + h24 v4 ženin 3. dokaz × h30
  // v4 nevesta 4. dokaz DRUBEL + h44 v5 ženin 3. dokaz + h24 v12 ženin 4. dokaz
  // = ★ BRATA BRNC! × h65 v12 nevesta 3. dokaz DRUBEL + h18 v13 ženin 3. dokaz
  // + h34 v13 nevesta 4. dokaz = ★ SESTRA v2! DRUBEL + h10 v14 ženin 4. dokaz
  // × h35 v14 nevesta 1. DOKAZ [korekcija 34→35!] DRUBEL + h1 v15 nevesta 2.
  // dokaz + h27 v17 ženin 4. dokaz × h1 v17 nevesta 3. dokaz DRUBEL = 4
  // DRUBEL!): NOVELE: ★ 11/11 PONEDELJKOV = 100% (1. popolno leto!) + ★ RAUY
  // 17/17 = 100% (3. popolno leto: P129 8/8, P130 11/11!) + ★ 3 HIŠE Z 2 BLOKI
  // V ENEM LETU (h24 BRATA Brnc v4+v12! · h34 BRAT-SESTRA Kambič v2+v13! ·
  // h1 2 nevesti Željko v15+v17 — ⚠️ 2 različna Nicolaus-očeta!) = NOVI
  // REKORD + ★ 3 JURAJEVČIČ-ženińi v 3 tednih maja (v8 Johann 27 Otok 11 + v9
  // Johann 28 Kapljiše? 6 + v11 Michael 27 Krasinec 21) + ★ 1. AMERIŠKI
  // DRŽAVLJAN LINIJE (v8 — konzul ZDA v Trstu: »ni denarnega zadržka« 27.3.!)+
  // ★ 2 DISPENSI 3. KOLENA (v7 № 342 + v9 № 1816 — vzorec 1890!) + ★ 1.
  // SCHMIEDMEISTER-ŽENIN × 1. SCHMIEDMEISTERS-WITWE (v16 obrtniški par; oče
  // Wagner-Meister = 2. dokaz P131!) + ★ VMET nem. k.k. Landesregierung Krain
  // № 15129 (v12 — »Taufname des Brunc richtig Anna lautet« [~] = 1. nemški
  // vmet poročne linije!) + ★ 6 KONTINUITET (h18 SIMEC 1897→05 8 let + isto
  // ime! · h27 KUČAR/KUKAR 1897→05 8 let dve pisavi! · h44 ŠTRUCELJ 1903→05 ·
  // h65 MÜCK/MILEK 1903→05 dve pisavi! · h1 ŽELJKO 1899→05 ×2! · h30 4. dokaz)
  // + 4 MENJAVE DRUŽIN (h24 Brišec?→BRNC ×2! · h30 LEGINA→Grabrijan · h34
  // FILAK/ŠILAK→KAMBIČ ×2! · h10 KURE→PERDINEC) + NOVE VASI/HIŠE: Škrilje? 1
  // [~] + Kapljiše? 4+6 [~] + Gakova? 3 draga Virodina? u Croatien [~ — 2.
  // hrvaški vpis!] + Metlika 36 (mesto!) + Črnomelj 158 (mesto!) + Gradac 27 +
  // Otok 11/20 + Krasinec 21?/22/6 + Dobravice 16 + Zastava 7 + Vranoviče 14 +
  // Priložje 26 + Primostek 8/17 + Cerkvišče 4/9 + NOVI PRIIMKI: SLOBODNIK ·
  // Strugar · Plut · Urbanek (hrvaški) · Kapuršinič? [~] · Pabič? [~] · Šešak
  // · Jötter? [~] + KUKAR 2. dokaz (P133 v11 mati — zdaj družina h27!) +
  // MILEK-mreža ×3 + KLOBUČAR ×2 + KRIŽAN ×3 + HARAŠINIČ ×3 + ŽUNIČ + statusi:
  // ¼ gbl.Pofu? [~] ×2 + griblarst.Hofe/Hofsa? [~] ×4 + griblarin + ½ Hübler
  // skupni status prič (v2!) + polnoletnost ×5 (2× ZA OBA!) + nadvarstveno ×2
  // + 1. pisava »Liubljani« za Laibach (v4!) + Pag. == sken−1 20. potrditev
  // (124–128). Dokaz: research/issue17/parish-marriage-1905.json; verifikator:
  // scripts/p134_parish_marriage_1905.py --check (I1–I11).
  {
    houseNo: "34",
    bookSignature: "04455",
    year: 1905,
    scan: 125,
    page: 124,
    whatSi: "poroka (20. 2. 1905, vpis 2) — ženin Johann Kambič, ¼ griblar, 27, GRIBLJE 34 (3. poročni dokaz h34 — 1898 P127 ženin Nicolaus FILAK + 1899 P128 2. dokaz = ★ MENJAVA FILAK/ŠILAK → KAMBIČ!) × Maria Dragoš, ½ gbl. Tochter, 19, Cerkvišče 4; starši: Mathias Kambič ¼ griblar × Catharina Brnc (= starši v13-neveste — ★ BRAT-SESTRA!) / Joseph Dragoš ½ griblar × Dorotha Brodarič (DRAGOŠ-mreža + BRODARIČ!); priče: Johann Požek [~] + Mathias Muek [~] ({ skupni status obe priči ½ Hübler [~] — 1. SKUPNI STATUS PRIČ LINIJE!); zglasmnica občine Griblje 19/2. 1905 št: 1 + očetovo ustno dovoljenje za ml. nevesto v navzočnosti zgornjih prič (formula rešena cf. v3!); duhovnik Jos. Rauy — P134-lead KOREKCIJA: »v2 Griblje 39 Markočič?« → h34 + KAMBIČ (lead-v2 je bil v resnici v4!)",
    whatEn: "marriage (Feb 20, 1905, entry 2) — the groom Johann Kambič, quarter smallholder, 27, GRIBLJE 34 (the 3rd marriage evidence of h34 — 1898 P127 the groom Nicolaus FILAK + 1899 P128 the 2nd = ★ the FAMILY CHANGE FILAK/ŠILAK → KAMBIČ!) × Maria Dragoš, half smallholder's daughter, 19, Cerkvišče 4; parents: Mathias Kambič ¼ smallholder × Catharina Brnc (= the v13 bride's parents — ★ BROTHER-SISTER!) / Joseph Dragoš ½ smallholder × Dorotha Brodarič (the DRAGOŠ network + BRODARIČ!); witnesses: Johann Požek [~] + Mathias Muek [~] ({ the SHARED status both witnesses ½ Hübler [~] — the 1st SHARED WITNESS STATUS of the line!); the Griblje commune certificate Feb 19, 1905 no: 1 + the father's verbal consent for the young bride in the presence of the above witnesses (the formula solved cf. v3!); priest Jos. Rauy — the P134-lead CORRECTION: »v2 Griblje 39 Markočič?« → h34 + KAMBIČ (the lead-v2 was in fact v4!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04455",
    year: 1905,
    scan: 126,
    page: 125,
    whatSi: "poroka (27. 2. 1905, vpis 4) — ženin Mathias Brnce [~ Brnc], 21, ¼ gbl.Pofu? [~ — sistematski nejasni status, cf. v14 + P135-lead v4!], GRIBLJE 24 (3. poročni dokaz h24 — 1895 P124 + 1902 nevesta Catharina BRIŠEC? [~] = menjava družine!) × Maria Grabrijan, güblerin [~ güblerin/griblerin vaha], 28, GRIBLJE 30 (4. poročni dokaz h30 — 1889 + 1892 + 1902 ženin Nicolaus LEGINA 43 = menjava družine!) = ★ DRUBEL-GRIBLJE (2. poroka hišne parice 24+30 po 1902!); starši: Mathias Brnce ¼ griblar × Barbara Jakobič (= starši v12-ženina — ★ BRATA BRNC V ENEM LETU!) / Mathias Perdinec gübler × Dorotha Jakobič; priče: Marcus Perdinec gübler + Mathias Jakofčič (¼ griblar [~]); zglasmnica občine Griblje 26/2. 1905 št: 2 + proglas polnoletnosti za ženina (sodišče Črnomelj 28/1. 1905 — ženin 21!) + dovoljenje c.kr. deželne vlade v LIUBLJANI 20/2. 1905 št: 3360 (1. pisava »Liubljani« za Laibach!); duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 27, 1905, entry 4) — the groom Mathias Brnce [~ Brnc], 21, quarter smallholder-Pofu? [~ — a systematic unclear status, cf. v14 + the P135-lead v4!], GRIBLJE 24 (the 3rd marriage evidence of h24 — 1895 P124 + 1902 the bride Catharina BRIŠEC? [~] = a family change!) × Maria Grabrijan, güblerin [~ güblerin/griblerin vaha], 28, GRIBLJE 30 (the 4th marriage evidence of h30 — 1889 + 1892 + 1902 the groom Nicolaus LEGINA 43 = a family change!) = ★ the DOUBLE-GRIBLJE wedding (the 2nd wedding of the house pair 24+30 after 1902!); parents: Mathias Brnce ¼ smallholder × Barbara Jakobič (= the v12 groom's parents — ★ THE BRNC BROTHERS IN ONE YEAR!) / Mathias Perdinec gübler × Dorotha Jakobič; witnesses: Marcus Perdinec gübler + Mathias Jakofčič (¼ smallholder [~]); the Griblje commune certificate Feb 26, 1905 no: 2 + the majority certificate for the groom (the Črnomelj court Jan 28, 1905 — the groom 21!) + the permission of the k.k. provincial government in LIUBLJANA Feb 20, 1905 no: 3360 (the 1st spelling »Liubljani« for Laibach!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04455",
    year: 1905,
    scan: 126,
    page: 125,
    whatSi: "poroka (27. 2. 1905, vpis 4) — nevesta Maria GRABRIJAN, güblerin [~], 28, GRIBLJE 30 (4. poročni dokaz h30 — 1889 + 1892 + 1902 LEGINA 43 najstarejši = MENJAVA DRUŽINE Legina → Grabrijan!) × Mathias Brnce [~], 21, ¼ gbl.Pofu? [~], GRIBLJE 24 (3. dokaz) = ★ DRUBEL; starši: Mathias Perdinec gübler × Dorotha Jakobič / Mathias Brnce ¼ griblar × Barbara Jakobič (= starši v12!); priči Marcus Perdinec gübler + Mathias Jakofčič; zglasmnica občine Griblje 26/2. 1905 št: 2 + polnoletnost za ženina (Črnomelj 28/1. 1905) + deželna vlada Liubljani 20/2. 1905 № 3360; duhovnik Jos. Rauy — GRABRIJAN nov priimek h30 (cf. v15-priča Johann Grabrijan!)",
    whatEn: "marriage (Feb 27, 1905, entry 4) — the bride Maria GRABRIJAN, güblerin [~], 28, GRIBLJE 30 (the 4th marriage evidence of h30 — 1889 + 1892 + 1902 LEGINA 43 the oldest = the FAMILY CHANGE Legina → Grabrijan!) × Mathias Brnce [~], 21, quarter smallholder-Pofu? [~], GRIBLJE 24 (the 3rd evidence) = ★ the DOUBLE; parents: Mathias Perdinec gübler × Dorotha Jakobič / Mathias Brnce ¼ smallholder × Barbara Jakobič (= the v12 parents!); witnesses Marcus Perdinec gübler + Mathias Jakofčič; the Griblje commune certificate Feb 26, 1905 no: 2 + the majority for the groom (Črnomelj Jan 28, 1905) + the provincial government Liubljana Feb 20, 1905 no: 3360; priest Jos. Rauy — GRABRIJAN a new h30 surname (cf. the v15 witness Johann Grabrijan!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04455",
    year: 1905,
    scan: 126,
    page: 125,
    whatSi: "poroka (27. 2. 1905, vpis 5) — ženin Joseph Štrucelj, ½ griblar, 22, GRIBLJE 44 (3. poročni dokaz h44 — 1899 P128 1. dokaz + 1903 P132 nevesta Dorothea ŠTRUCELJ = ★ ŠTRUCELJ-kontinuiteta!) × Barbara Černe, ½ gbl. Tochter, 21, Škrilje? 1 [~ NOVA VAS?]; starši: Mathias Štrucelj ½ griblar × Agnes KLOBUČAR (h44-družina — cf. P128 v1-priča Marcus Klobučar!) / Johann Černe ½ griblar × Barbara Malevič [~]; priče: Jakob Jötter? [~] ¼ griblar + Marcus Šešak ½ griblar; zglasmnica občine Griblje 26/2. 1905 št: 3 + proglas polnoletnosti za ženina (sodišče Črnomelj 28/1. 1905 — ISTI DAN kot v4!) + očetovo ustno dovoljenje za ml. nevesto v navzočnosti zgornjih prič; duhovnik Jos. Rauy — ČERNE (cf. P131 v6 ženin Thomas Černe nezakonski!)",
    whatEn: "marriage (Feb 27, 1905, entry 5) — the groom Joseph Štrucelj, half smallholder, 22, GRIBLJE 44 (the 3rd marriage evidence of h44 — 1899 P128 the 1st + 1903 P132 the bride Dorothea ŠTRUCELJ = ★ the ŠTRUCELJ continuity!) × Barbara Černe, half smallholder's daughter, 21, Škrilje? 1 [~ A NEW VILLAGE?]; parents: Mathias Štrucelj ½ smallholder × Agnes KLOBUČAR (the h44 family — cf. the P128 v1 witness Marcus Klobučar!) / Johann Černe ½ smallholder × Barbara Malevič [~]; witnesses: Jakob Jötter? [~] ¼ smallholder + Marcus Šešak ½ smallholder; the Griblje commune certificate Feb 26, 1905 no: 3 + the majority certificate for the groom (the Črnomelj court Jan 28, 1905 — the SAME DAY as v4!) + the father's verbal consent for the young bride in the presence of the above witnesses; priest Jos. Rauy — ČERNE (cf. P131 v6 the illegitimate groom Thomas Černe!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04455",
    year: 1905,
    scan: 128,
    page: 127,
    whatSi: "poroka (22. 5. 1905, vpis 12) — ženin Johann Brnce [~], 24, ½ griblar, GRIBLJE 24 (4. poročni dokaz h24 — 2. V TEM LETU = ★ BRATA BRNC v4 Mathias 21 + v12 Johann 24, isti starši Mathias Brnce × Barbara Jakobič — 3. hiša z 2 bloki v enem letu [h11-1903, h38-1904!]!) × Catharina Milek, ½ griblarß-tochter [~], 17, GRIBLJE 65 (3. poročni dokaz h65 — 1903 ženin Matthias MÜCK [~ Milek] = ★ MÜCK/MILEK-kontinuiteta, dve pisavi!) = ★ DRUBEL; starši: Mathias Brnce ½ griblar × Barbara Jakobič (= v4!) / Mathias Milek ½ griblar × Catharina POŽEK (POŽEK = v2-priča!); priči: Nicolaus Segna? [~] ¼ griblar + Marcus KLOBUČAR (gbl-žiglb? [~]); zglasmnica občine Griblje 24/5. 1905 št: 4 + očetovo ustno dovoljenje za ml. nevesto; ★ VMET (nem.): »Auf Folge-Erlasses der k.k. Landesregierung für Krain vom 26/4. 1905 Z: 15129 wird angemerkt, dass der Taufname des Brunc richtig Anna lautet« [~ — 1. NEMŠKI VMET poročne linije; kdo? morda krstno ime v družini Brunc!]; duhovnik Jos. Rauy",
    whatEn: "marriage (May 22, 1905, entry 12) — the groom Johann Brnce [~], 24, half smallholder, GRIBLJE 24 (the 4th marriage evidence of h24 — the 2nd THIS YEAR = ★ THE BRNC BROTHERS v4 Mathias 21 + v12 Johann 24, the same parents Mathias Brnce × Barbara Jakobič — the 3rd house with 2 blocks in one year [h11-1903, h38-1904!]!) × Catharina Milek, half smallholder's daughter [~], 17, GRIBLJE 65 (the 3rd marriage evidence of h65 — 1903 the groom Matthias MÜCK [~ Milek] = ★ the MÜCK/MILEK continuity, two spellings!) = ★ the DOUBLE; parents: Mathias Brnce ½ smallholder × Barbara Jakobič (= v4!) / Mathias Milek ½ smallholder × Catharina POŽEK (POŽEK = the v2 witness!); witnesses: Nicolaus Segna? [~] ¼ smallholder + Marcus KLOBUČAR (gbl-žiglb? [~]); the Griblje commune certificate May 24, 1905 no: 4 + the father's verbal consent for the young bride; ★ INSERT (Ger.): »Auf Folge-Erlasses der k.k. Landesregierung für Krain vom 26/4. 1905 Z: 15129 wird angemerkt, dass der Taufname des Brunc richtig Anna lautet« [~ — the 1st GERMAN INSERT of the marriage line; who? perhaps a baptismal name in the Brunc family!]; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04455",
    year: 1905,
    scan: 128,
    page: 127,
    whatSi: "poroka (22. 5. 1905, vpis 12) — nevesta Catharina MILEK, ½ griblarß-tochter [~], 17, GRIBLJE 65 (3. poročni dokaz h65 — 1903 P132 v3 ženin Matthias MÜCK [~ Milek] = ★ MÜCK/MILEK-kontinuiteta 2 leti, dve pisavi!) × Johann Brnce [~], 24, ½ griblar, GRIBLJE 24 (4. dokaz — ★ BRAT v4!) = ★ DRUBEL; starši: Mathias Milek ½ griblar × Catharina Požek / Mathias Brnce ½ griblar × Barbara Jakobič (= v4!); priči Nicolaus Segna? [~] + Marcus Klobučar; zglasmnica občine Griblje 24/5. 1905 št: 4 + nemški vmet k.k. Landesregierung für Krain № 15129 [~]; duhovnik Jos. Rauy — MILEK ×2 v letu (v12-nevesta + v13-mati Anna Milek!)",
    whatEn: "marriage (May 22, 1905, entry 12) — the bride Catharina MILEK, half smallholder's daughter [~], 17, GRIBLJE 65 (the 3rd marriage evidence of h65 — 1903 P132 v3 the groom Matthias MÜCK [~ Milek] = ★ the MÜCK/MILEK continuity of 2 years, two spellings!) × Johann Brnce [~], 24, half smallholder, GRIBLJE 24 (the 4th evidence — ★ the v4 BROTHER!) = ★ the DOUBLE; parents: Mathias Milek ½ smallholder × Catharina Požek / Mathias Brnce ½ smallholder × Barbara Jakobič (= v4!); witnesses Nicolaus Segna? [~] + Marcus Klobučar; the Griblje commune certificate May 24, 1905 no: 4 + the German insert k.k. Landesregierung für Krain no: 15129 [~]; priest Jos. Rauy — MILEK ×2 in the year (the v12 bride + the v13 mother Anna Milek!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04455",
    year: 1905,
    scan: 128,
    page: 127,
    whatSi: "poroka (29. 5. 1905, vpis 13) — ženin Mathias Simec, ¼ griblar, 31, GRIBLJE 18 (3. poročni dokaz h18 — 1897 P126 ženin Mathias SIMEC ½ = ★ SIMEC-kontinuiteta 8 LET + ISTO IME Mathias!) × Maria Kambic, ¼ gbl. Tochter, 30, GRIBLJE 34 (4. poročni dokaz h34 — 2. V TEM LETU = ★ SESTRA v2-ženina Johann KAMBIČ, isti starši Mathias Kambič × Catharina Brnc — vzorec BRAT-SESTRA P132 h11!) = ★ DRUBEL; starši: Georg Simec ¼ griblar × Anna MILEK (MILEK 2. dokaz v letu!) / Mathias Kambic ¼ griblar × Catharina Brnce (= v2!); priči: Joseph Dragoš (= v2-nevestin priimek!) + Mathias Klepec ½ griblar (KLEPEC-mreža!); zglasmnica občine Griblje 28/5. 1905 št: 5; duhovnik Jos. Rauy",
    whatEn: "marriage (May 29, 1905, entry 13) — the groom Mathias Simec, quarter smallholder, 31, GRIBLJE 18 (the 3rd marriage evidence of h18 — 1897 P126 the groom Mathias SIMEC ½ = ★ the SIMEC continuity of 8 YEARS + the SAME NAME Mathias!) × Maria Kambic, quarter smallholder's daughter, 30, GRIBLJE 34 (the 4th marriage evidence of h34 — the 2nd THIS YEAR = ★ the SISTER of the v2 groom Johann KAMBIČ, the same parents Mathias Kambič × Catharina Brnc — the BROTHER-SISTER pattern P132 h11!) = ★ the DOUBLE; parents: Georg Simec ¼ smallholder × Anna MILEK (the 2nd MILEK of the year!) / Mathias Kambic ¼ smallholder × Catharina Brnce (= v2!); witnesses: Joseph Dragoš (= the v2 bride's surname!) + Mathias Klepec ½ smallholder (the KLEPEC network!); the Griblje commune certificate May 28, 1905 no: 5; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04455",
    year: 1905,
    scan: 128,
    page: 127,
    whatSi: "poroka (29. 5. 1905, vpis 13) — nevesta Maria KAMBIC, ¼ gbl. Tochter, 30, GRIBLJE 34 (4. poročni dokaz h34 — 2. V TEM LETU = ★ SESTRA v2-ženina Johann, isti starši = ★ BRAT-SESTRA vzorec P132 h11!) × Mathias Simec, ¼ griblar, 31, GRIBLJE 18 (3. dokaz — ★ SIMEC 1897→05 8 let!) = ★ DRUBEL; starši: Mathias Kambic ¼ griblar × Catharina Brnce (= v2!) / Georg Simec ¼ griblar × Anna Milek; priči Joseph Dragoš + Mathias Klepec; zglasmnica občine Griblje 28/5. 1905 št: 5; duhovnik Jos. Rauy — h34 MENJAVA: FILAK/ŠILAK (1898–99) → KAMBIČ (1905 ×2!)",
    whatEn: "marriage (May 29, 1905, entry 13) — the bride Maria KAMBIC, quarter smallholder's daughter, 30, GRIBLJE 34 (the 4th marriage evidence of h34 — the 2nd THIS YEAR = ★ the SISTER of the v2 groom Johann, the same parents = ★ the BROTHER-SISTER pattern P132 h11!) × Mathias Simec, quarter smallholder, 31, GRIBLJE 18 (the 3rd evidence — ★ SIMEC 1897→05 8 years!) = ★ the DOUBLE; parents: Mathias Kambic ¼ smallholder × Catharina Brnce (= v2!) / Georg Simec ¼ smallholder × Anna Milek; witnesses Joseph Dragoš + Mathias Klepec; the Griblje commune certificate May 28, 1905 no: 5; priest Jos. Rauy — the h34 CHANGE: FILAK/ŠILAK (1898–99) → KAMBIČ (1905 ×2!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04455",
    year: 1905,
    scan: 128,
    page: 127,
    whatSi: "poroka (29. 5. 1905, vpis 14) — ženin Joseph Perdinec, 25, ¼ gbl.Pofu? [~ — 2. dokaz statusa cf. v4!], GRIBLJE 10 (4. poročni dokaz h10 — 1890 + 1899 nevesta Barbara KURE = ★ MENJAVA KURE → PERDINEC [~ vzorec menjav!]) × Anna Križan, ¼ gbl. Tochter, 34, GRIBLJE 35 (★ 1. POROČNI DOKAZ h35 — hiša 34 PREČRTANO → 35 popravljeno V VPISU! EDINA nova poročna hiša 1905; cf. krstne h35 ×7!) = ★ DRUBEL; starši: Johann Perdinec ¼ griblar × Anna Jakobič / Johann Križan ¼ gbl × Anna STRAUSS (STRAUSS-mreža!); priči: Mathias Muek? [~ Muh] + Mathias Jakobič (¼ griblar); zglasmnica občine Griblje 28/5. 1905 št: 6; duhovnik Jos. Rauy — KRIŽAN ×2 v letu (v7-nevesta Margareth + v14-nevesta Anna!)",
    whatEn: "marriage (May 29, 1905, entry 14) — the groom Joseph Perdinec, 25, quarter smallholder-Pofu? [~ — the 2nd status evidence cf. v4!], GRIBLJE 10 (the 4th marriage evidence of h10 — 1890 + 1899 the bride Barbara KURE = ★ the CHANGE KURE → PERDINEC [~ the change pattern!]) × Anna Križan, quarter smallholder's daughter, 34, GRIBLJE 35 (★ the 1st MARRIAGE EVIDENCE of h35 — house 34 CROSSED OUT → 35 corrected IN THE ENTRY! the ONLY new marriage house of 1905; cf. the h35 baptisms ×7!) = ★ the DOUBLE; parents: Johann Perdinec ¼ smallholder × Anna Jakobič / Johann Križan ¼ smallholder × Anna STRAUSS (the STRAUSS network!); witnesses: Mathias Muek? [~ Muh] + Mathias Jakobič (¼ smallholder); the Griblje commune certificate May 28, 1905 no: 6; priest Jos. Rauy — KRIŽAN ×2 in the year (the v7 bride Margareth + the v14 bride Anna!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04455",
    year: 1905,
    scan: 128,
    page: 127,
    whatSi: "poroka (29. 5. 1905, vpis 14) — nevesta Anna KRIŽAN, ¼ gbl. Tochter, 34, GRIBLJE 35 (★ 1. POROČNI DOKAZ h35 — hiša 34 PREČRTANO → 35 popravljeno v vpisu! EDINA nova poročna hiša 1905) × Joseph Perdinec, 25, ¼ gbl.Pofu? [~], GRIBLJE 10 (4. dokaz — menjava KURE→PERDINEC) = ★ DRUBEL; starši: Johann Križan ¼ gbl × Anna Strauss / Johann Perdinec ¼ griblar × Anna Jakobič; priči Mathias Muek? [~] + Mathias Jakobič; zglasmnica občine Griblje 28/5. 1905 št: 6; duhovnik Jos. Rauy — KRIŽAN ×3 v letu (v7-nevesta + v14-nevesta + v15-mati Maria Križan!)",
    whatEn: "marriage (May 29, 1905, entry 14) — the bride Anna KRIŽAN, quarter smallholder's daughter, 34, GRIBLJE 35 (★ the 1st MARRIAGE EVIDENCE of h35 — house 34 CROSSED OUT → 35 corrected in the entry! the ONLY new marriage house of 1905) × Joseph Perdinec, 25, quarter smallholder-Pofu? [~], GRIBLJE 10 (the 4th evidence — the change KURE→PERDINEC) = ★ the DOUBLE; parents: Johann Križan ¼ smallholder × Anna Strauss / Johann Perdinec ¼ smallholder × Anna Jakobič; witnesses Mathias Muek? [~] + Mathias Jakobič; the Griblje commune certificate May 28, 1905 no: 6; priest Jos. Rauy — KRIŽAN ×3 in the year (the v7 bride + the v14 bride + the v15 mother Maria Križan!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04455",
    year: 1905,
    scan: 128,
    page: 127,
    whatSi: "poroka (3. 7. 1905, vpis 15) — nevesta Maria Željko, ½ griblarst.Hofsa? [~ ženska pisava cf. v7/v17!], 25, GRIBLJE 1 (2. poročni dokaz h1 — 1899 P128 ženin Georg ŽELJKO ½ = ★ ŽELJKO-kontinuiteta 6 let!) × Michael Jakofčič, ¼ griblar, 19, Cerkvišče 9 (= P119 v13 Johann HVALJ-hiša? [~ menjava!]); starši: Nicolaus Željko ½ griblar × Maria KRIŽAN (⚠️ cf. v17-oče Nicolaus ¼ × Catharina Kure — 2 različna Nicolaus!) / Michael Jakofčič ¼ griblar × Maria ŽUNIČ (ŽUNIČ-mreža!); priči: Johann Grabrijan (= v4-nevestin priimek!) + Georg Željko ¼ griblar (= priimek neveste — brat/oče?); zglasmnica občine Podzemelj 3/7. 1905 št: 5 + dovoljenje deželne vlade v Liubljani 15. 6. 1905 št: 11955 + očetovo ustno dovoljenje za ml. ŽENINA (19!) v navzočnosti zgornjih prič; duhovnik Jos. Rauy",
    whatEn: "marriage (Jul 3, 1905, entry 15) — the bride Maria Željko, half smallholder-hold-Hofsa? [~ a female spelling cf. v7/v17!], 25, GRIBLJE 1 (the 2nd marriage evidence of h1 — 1899 P128 the groom Georg ŽELJKO ½ = ★ the ŽELJKO continuity of 6 years!) × Michael Jakofčič, quarter smallholder, 19, Cerkvišče 9 (= the P119 v13 Johann HVALJ house? [~ a change!]); parents: Nicolaus Željko ½ smallholder × Maria KRIŽAN (⚠️ cf. the v17 father Nicolaus ¼ × Catharina Kure — 2 different Nicolaus!) / Michael Jakofčič ¼ smallholder × Maria ŽUNIČ (the ŽUNIČ network!); witnesses: Johann Grabrijan (= the v4 bride's surname!) + Georg Željko ¼ smallholder (= the bride's surname — a brother/father?); the Podzemelj commune certificate Jul 3, 1905 no: 5 + the permission of the provincial government in Liubljana Jun 15, 1905 no: 11955 + the father's verbal consent for the young GROOM (19!) in the presence of the above witnesses; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04455",
    year: 1905,
    scan: 129,
    page: 128,
    whatSi: "poroka (7. 8. 1905, vpis 17) — ženin Mathias Kukar [~ Hukav], 21, ¼ griblasd-Hofsa? [~], GRIBLJE 27 (4. poročni dokaz h27 — 1897 P126 nevesta Anna KUCHAR [~ Kučar] = ★ KUČAR/KUKAR-kontinuiteta 8 LET, dve pisavi!) × Barbara Željko, ½ griblastochf, 21, GRIBLJE 1 (3. poročni dokaz h1 — 2. V TEM LETU = 2. ŽELJKO-nevesta (v15 Maria!); ⚠️ 2 različna očeta Nicolaus Željko [½ × Maria Križan / ¼ × Catharina Kure] — oče+sin?) = ★ DRUBEL; starši: Johann KUKAR ¼ griblar × Catharina KLOBUČAR (KLOBUČAR = v5-mati Agnes! h44-mreža!) / Nicolaus Željko ¼ griblar × Catharina KURE; priči: Nicolaus Željko (= oče neveste?) + Georg Harašinič (HARAŠINIČ = v10 oče+priča — 3. dokaz!); zglasmnica občine Griblje 6/8. 1905 št: 7 + dovoljenje deželne vlade 4/7. 1905 № 12937 + proglas polnoletnosti za OBA (okrajna sodnija Črnomelj 17. 5. 1905); duhovnik Jos. Rauy — ZADNJA poroka 1905",
    whatEn: "marriage (Aug 7, 1905, entry 17) — the groom Mathias Kukar [~ Hukav], 21, quarter smallholder-hold-Hofsa? [~], GRIBLJE 27 (the 4th marriage evidence of h27 — 1897 P126 the bride Anna KUCHAR [~ Kučar] = ★ the KUČAR/KUKAR continuity of 8 YEARS, two spellings!) × Barbara Željko, half smallholder's daughter, 21, GRIBLJE 1 (the 3rd marriage evidence of h1 — the 2nd THIS YEAR = the 2nd ŽELJKO bride (v15 Maria!); ⚠️ 2 different fathers Nicolaus Željko [½ × Maria Križan / ¼ × Catharina Kure] — father+son?) = ★ the DOUBLE; parents: Johann KUKAR ¼ smallholder × Catharina KLOBUČAR (KLOBUČAR = the v5 mother Agnes! the h44 network!) / Nicolaus Željko ¼ smallholder × Catharina KURE; witnesses: Nicolaus Željko (= the bride's father?) + Georg Harašinič (HARAŠINIČ = v10 father+witness — the 3rd evidence!); the Griblje commune certificate Aug 6, 1905 no: 7 + the permission of the provincial government Jul 4, 1905 no: 12937 + the majority certificate for BOTH (the Črnomelj district court May 17, 1905); priest Jos. Rauy — the LAST wedding of 1905",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04455",
    year: 1905,
    scan: 129,
    page: 128,
    whatSi: "poroka (7. 8. 1905, vpis 17) — nevesta Barbara ŽELJKO, ½ griblastochf, 21, GRIBLJE 1 (3. poročni dokaz h1 — 2. V TEM LETU: v15 Maria + v17 Barbara; ⚠️ 2 različna Nicolaus Željko-očeta [½ × Maria Križan / ¼ × Catharina Kure] — oče+sin?) × Mathias Kukar [~], 21, ¼ griblasd-Hofsa? [~], GRIBLJE 27 (4. dokaz — ★ KUČAR/KUKAR 1897→05 8 let!) = ★ DRUBEL; starši: Nicolaus Željko ¼ griblar × Catharina KURE / Johann Kukar ¼ griblar × Catharina Klobučar; priči Nicolaus Željko + Georg Harašinič; zglasmnica občine Griblje 6/8. 1905 št: 7 + deželna vlada № 12937 + polnoletnost za OBA; duhovnik Jos. Rauy — ŽELJKO ×3 v letu (2 nevesti + 1 priča Georg v15!)",
    whatEn: "marriage (Aug 7, 1905, entry 17) — the bride Barbara ŽELJKO, half smallholder's daughter, 21, GRIBLJE 1 (the 3rd marriage evidence of h1 — the 2nd THIS YEAR: v15 Maria + v17 Barbara; ⚠️ 2 different fathers Nicolaus Željko [½ × Maria Križan / ¼ × Catharina Kure] — father+son?) × Mathias Kukar [~], 21, quarter smallholder-hold-Hofsa? [~], GRIBLJE 27 (the 4th evidence — ★ KUČAR/KUKAR 1897→05 8 years!) = ★ the DOUBLE; parents: Nicolaus Željko ¼ smallholder × Catharina KURE / Johann Kukar ¼ smallholder × Catharina Klobučar; witnesses Nicolaus Željko + Georg Harašinič; the Griblje commune certificate Aug 6, 1905 no: 7 + the provincial government no: 12937 + the majority for BOTH; priest Jos. Rauy — ŽELJKO ×3 in the year (2 brides + 1 witness Georg in v15!)",
    status: "DOCUMENTED",
  },
  // ——— P135 razširitev: POROČNA KNJIGA 04455 — polno leto 1906 (skeni 129–131 ==
  // strani 128–130; ROKOPISNA GLAVA »1906« na s129 POTRJENA — P134 lead! (pod njo
  // še 1905-vpis 17); velike tiskane glave na s130/s131; rokopisna glava »1907«
  // na s132 = P136 LEAD; 12 vpisov obojestransko = P135-lead »min 4 vpisov
  // s129« 3× pocenjen; razpored 4+5+3 — ★ 1. NEOSTEVCEN vpis (Mai 27, med v8
  // in v9!) — vpisi z Griblji (3 poroke / 5 poročnih blokov: h73 v8 ženin 1.
  // DOKAZ = ★ NOVI MAKSIMUM h65→h73! + h31 v9 ženin 3. dokaz × h35 v9 nevesta
  // 2. dokaz DRUBEL + h62 v11 ženin 4. dokaz KURE × h21 v11 nevesta 2. poročni
  // dokaz [1887→06 = 19-letna luknja!] DRUBEL): NOVELE: ★ 62-LETNI ŽENIN =
  // NAJSTAREJŠI LINIJE (v10 Hüblar? — prej Kralj 61⅔ P132!) + ★ 1. GOSTUJOČI
  // DUHOVNIK »pro delegato« (v9m: Hx.? Herr? Jacobus Pavlovič?, Phluser? [~],
  // SUHOR — RAUY 11/12!) + ★ DVOJNI-IZMENJAVNI DRUBEL 29.1. (v2+v3: Krasinec
  // 35 Brodarič × Krasinec 18 Županič in obratno — 2 NIKOLAUSA; ⚠️ 2 različna
  // Brodarič-očeta v h35 [Johann×Vorne? / Nicolaus×Tome]!) + ★ 1. HIŠA Z 3
  // BLOKI V ENEM LETU = NOVI REKORD (h18 Županič v2+v3+v6 — ISTI starši
  // Mathias × Catharina Harašinič!) + ★ SPREGLED DVEH OKLICEV (v9m ord.
  // Ljubljana № 2170 = NOV dokument-tip!) + ★ 2 NEDELJSKI POROKI (27.5. +
  // 10.6. — P134 je bilo 11/11 pon!) + ★ sodno dovoljenje »za voj.
  // neveljavnost?« (v3 [~]) + ★ 17-letna nevesta Perušič (v7 — izenači P134
  // Milek 17; 1. mladoletniško sodno dovoljenje za NEVESTO pri 17!) + ★
  // deželna vlada Ljubljana № 23993 = NOVI NAJVIŠJI št. (prej 22190 P133!) +
  // ★ 1. IZOSTANI nevestin konsent (v1 — samo ženinova stran Krašić/HRVAŠKA!)
  // + ★ ISTI-DNEVNI konsent (v9: 10/6 = dan poroke!) + TOME-MREŽA ×5 (v3/v4/
  // v5/v7 matere + v8 nevesta!) + HÜBLER-mreža ×7 (status kot priimek!) +
  // KURE 4. dokaz (3 osebe v v11!) + NOVE VASI/HIŠE: Lahinja 5 pf. Črnomelj
  // (NOVA VAS!) + Griblje 73+21 + Kloster 16 + Krasinec 48 + Zemelj 15 +
  // Grišiče? 35 [~ P132!] + Đeleković? 1, plane? Krašić? u Croatiën [~] +
  // nazaj: Zemelj 13 (12 let!) · Primostek 18 (13!) · Podzemelj 32 (10!) ·
  // Germ 28 (8!) · Otok 14 · Gradac 6 · Boginja vas 14 · Griblje 31/35/62 +
  // NOVI PRIIMKI: Perušič · Paprič? [~] · Jaklič? [~] · Seidrisper? [~] ·
  // Šuparnič?/Šiparnič? [~ dve pisavi] · Delijanec? [~] + statusi: ½
  // griblarst?-Sohn [~] ×5 + Hausbesitzerin u. Wittwe (1. kombinacija!) +
  // MASA 12.2 ×3 + formula »v navzočnosti zgornjih prič« ×2 + Pag. == sken−1
  // 21. potrditev (128–130). Dokaz: research/issue17/parish-marriage-1906.json;
  // verifikator: scripts/p135_parish_marriage_1906.py --check (I1–I11).
  {
    houseNo: "73",
    bookSignature: "04455",
    year: 1906,
    scan: 130,
    page: 129,
    whatSi: "poroka (19. 2. 1906, vpis 8) — ženin Johann Šuparnič? [~ Šiparnič? — dve pisavi cf. v6!], ½ griblarst?-Sohn [~], 26, GRIBLJE 73 (★ 1. POROČNI DOKAZ h73 = NOVA HIŠA = NOVI MAKSIMUM LINIJE h65→h73!) × Helena TOME, ½ griblarstocha? [~], 21, Primostek 18 (1893→06 — 13-letna luknja!); starši: Nicolaus Šuparnič? ½ griblar × Catharina PERDINEC / Martin Tome ½ griblar × Margareth KAMBIČ (h34/35-mreža!); priči: Johann Šuparnič? (½ Hübler) + Mathias Delijanec? [~] (1 Hübler [~ »ein Hübler«] — ločena statusa!); zglasmnica občine Griblje 19/2. 1906 št: 1 + proglas polnoletnosti za nevesto (okrajno sodišče Metlika 18/4. 1905); duhovnik Jos. Rauy — TOME-mreža 5/5 (v8 nevesta + matere v3/v4/v5/v7!)",
    whatEn: "marriage (Feb 19, 1906, entry 8) — the groom Johann Šuparnič? [~ Šiparnič? — two spellings cf. v6!], half smallholder's?-son [~], 26, GRIBLJE 73 (★ the 1st MARRIAGE EVIDENCE of h73 = A NEW HOUSE = THE NEW MAXIMUM of the line h65→h73!) × Helena TOME, half smallholder's daughter? [~], 21, Primostek 18 (1893→06 — a 13-year gap!); parents: Nicolaus Šuparnič? ½ smallholder × Catharina PERDINEC / Martin Tome ½ smallholder × Margareth KAMBIČ (the h34/35 network!); witnesses: Johann Šuparnič? (½ Hübler) + Mathias Delijanec? [~] (1 Hübler [~ »ein Hübler«] — separate statuses!); the Griblje commune certificate Feb 19, 1906 no: 1 + the majority certificate for the bride (the Metlika district court Apr 18, 1905); priest Jos. Rauy — the TOME network 5/5 (the v8 bride + mothers in v3/v4/v5/v7!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1906,
    scan: 131,
    page: 130,
    whatSi: "poroka (10. 6. 1906, vpis 9 — ★ NEDELJA!) — ženin Martin PAPRIČ? [~ — NOV PRIIMEK], Wagner (poklic!), 49, WITWER?, GRIBLJE 31 (3. poročni dokaz h31 — 1901×2 → 06!) × Barbara SIMEC, ½ Hüblers-Tochter (explicitno!), 48, GRIBLJE 35 (2. dokaz h35 — 1905→06!) = ★ DRUBEL-GRIBLJE; starši: Georg Paprič? ½ Hübler × Margareth ŽUGELJ (P128-mreža!) / Johann Simec ½ Hübler × Maria JAKOFČIČ (P132 dve pisavi!); priči: Martin Škala + Marko PEZDIREC? [~ — slavna družina!] ({ ¼ Hübler? [~]); zglasmnica občine Griblje x dne 10/6. 1906 št: 48 (★ ISTI DAN kot poroka!); duhovnik Jos. Rauy — ★ 2. NEDELJSKI porok leta (9 dni za v9m!)",
    whatEn: "marriage (Jun 10, 1906, entry 9 — ★ SUNDAY!) — the groom Martin PAPRIČ? [~ — A NEW SURNAME], Wagner (a craft!), 49, a widower?, GRIBLJE 31 (the 3rd marriage evidence of h31 — 1901×2 → 06!) × Barbara SIMEC, half Hübler's daughter (explicit!), 48, GRIBLJE 35 (the 2nd evidence of h35 — 1905→06!) = ★ the DOUBLE-GRIBLJE wedding; parents: Georg Paprič? ½ Hübler × Margareth ŽUGELJ (the P128 network!) / Johann Simec ½ Hübler × Maria JAKOFČIČ (the P132 two spellings!); witnesses: Martin Škala + Marko PEZDIREC? [~ — the famous family!] ({ ¼ Hübler? [~]); the Griblje commune certificate ON Jun 10, 1906 no: 48 (★ the SAME DAY as the wedding!); priest Jos. Rauy — ★ the 2nd SUNDAY wedding of the year (9 days after v9m!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04455",
    year: 1906,
    scan: 131,
    page: 130,
    whatSi: "poroka (10. 6. 1906, vpis 9) — nevesta Barbara SIMEC, ½ Hüblers-Tochter, 48, GRIBLJE 35 (2. poročni dokaz h35 — 1905 P134 nevesta Anna KRIŽAN → 1906!) × Martin PAPRIČ? [~], Wagner, 49, WITWER?, GRIBLJE 31 (3. dokaz) = ★ DRUBEL; starši: Johann Simec ½ Hübler × Maria Jakofčič / Georg Paprič? ½ Hübler × Margareth Žugelj; priči Martin Škala + Marko Pezdirec? [~]; zglasmnica občine Griblje 10/6. 1906 št: 48 (isti dan!); duhovnik Jos. Rauy — ★ nevesta 48 × ženin 49 = 2. najstarejša poročna kombinacija linije (cf. v10 62×24!); SIMEC ×2 v letu (v1 nevesta-vdova + v9!)",
    whatEn: "marriage (Jun 10, 1906, entry 9) — the bride Barbara SIMEC, half Hübler's daughter, 48, GRIBLJE 35 (the 2nd marriage evidence of h35 — 1905 P134 the bride Anna KRIŽAN → 1906!) × Martin PAPRIČ? [~], Wagner, 49, a widower?, GRIBLJE 31 (the 3rd evidence) = ★ the DOUBLE; parents: Johann Simec ½ Hübler × Maria Jakofčič / Georg Paprič? ½ Hübler × Margareth Žugelj; witnesses Martin Škala + Marko Pezdirec? [~]; the Griblje commune certificate Jun 10, 1906 no: 48 (the same day!); priest Jos. Rauy — ★ the bride 48 × the groom 49 = the 2nd oldest marriage combination of the line (cf. v10 62×24!); SIMEC ×2 in the year (the v1 widow-bride + v9!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04455",
    year: 1906,
    scan: 131,
    page: 130,
    whatSi: "poroka (26. 11. 1906, vpis 11) — ženin Johan KURE, ½ griblarsh-Sohn? [~], 22, GRIBLJE 62 (★ 4. poročni dokaz h62 — 1893 + 1898 + 1904 P133 → 1906 = 13-letna KURE-kontinuiteta; 3 KURE-osebe v enem vpisu!) × Maria Požek? [~ Poček?], ½ griblarsh-Hofstochter? [~ »½ griblarsh-Hoftar?« cf. P134 griblarst.Hofe?], 24, GRIBLJE 21 (2. poročni dokaz h21 — 1887 Ana Petrík → 06 = 19-LETNA LUKNJA poročne linije! + 1914-krstna marginalia Danica!) = ★ DRUBEL; starši: Anton Kure ½ Hübler × Barbara KRIŽAN / Johan Požek? ¼ Hübler × Maria Brinec? [~]; priči: Nicolaus Kure (= ženinova družina!) + Johann DRAGOŠ (11.+ leto mreže!) ({ skupni ½ Hübler; zglasmnica občine Griblje 26. 11. 1906 št: 3 + Hofmeister? [~] sodno dovoljenje za ml. ženina v navzočnosti zgornjih prič (formula!) + dovoljenje c. kr. dežel. predsedstva? v Ljubljani 24. 11. 1906 № 23993 (★ NOVI NAJVIŠJI št. — prej 22190 P133!); duhovnik Jos. Rauy",
    whatEn: "marriage (Nov 26, 1906, entry 11) — the groom Johan KURE, half smallholder's-son? [~], 22, GRIBLJE 62 (★ the 4th marriage evidence of h62 — 1893 + 1898 + 1904 P133 → 1906 = a 13-year KURE continuity; 3 KURE persons in one entry!) × Maria Požek? [~ Poček?], half smallholder's-hold-daughter? [~], 24, GRIBLJE 21 (the 2nd marriage evidence of h21 — 1887 Ana Petrík → 06 = a 19-YEAR GAP of the marriage line! + the 1914 baptism marginalia Danica!) = ★ the DOUBLE; parents: Anton Kure ½ Hübler × Barbara KRIŽAN / Johan Požek? ¼ Hübler × Maria Brinec? [~]; witnesses: Nicolaus Kure (= the groom's family!) + Johann DRAGOŠ (the 11th+ year of the network!) ({ the shared ½ Hübler; the Griblje commune certificate Nov 26, 1906 no: 3 + Hofmeister? [~] the court permission for the young groom in the presence of the above witnesses (the formula!) + the permission of the k.k. provincial presidency? in Ljubljana Nov 24, 1906 no: 23993 (★ THE NEW HIGHEST no. — previously 22190 P133!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04455",
    year: 1906,
    scan: 131,
    page: 130,
    whatSi: "poroka (26. 11. 1906, vpis 11) — nevesta Maria POŽEK? [~ Poček?], ½ griblarsh-Hofstochter? [~], 24, GRIBLJE 21 (2. poročni dokaz h21 — 1887 P116 v3 nevesta Ana PETRÍK 44 → 1906 = 19-LETNA LUKNJA poročne linije!; 1914-krstna marginalia: Danica, poročena 1947 v Gradcu!) × Johan KURE, 22, ½ griblarsh-Sohn? [~], GRIBLJE 62 (4. dokaz KURE!) = ★ DRUBEL; starši: Johan Požek? ¼ Hübler × Maria Brinec? [~] / Anton Kure ½ Hübler × Barbara Križan; priči Nicolaus Kure + Johann Dragoš; zglasmnica občine Griblje 26. 11. 1906 št: 3 + deželna vlada Ljubljana № 23993; duhovnik Jos. Rauy — POŽEK ×3 v letu (v5 mati + v11 nevesta+oče!)",
    whatEn: "marriage (Nov 26, 1906, entry 11) — the bride Maria POŽEK? [~ Poček?], half smallholder's-hold-daughter? [~], 24, GRIBLJE 21 (the 2nd marriage evidence of h21 — 1887 P116 v3 the bride Ana PETRÍK 44 → 1906 = a 19-YEAR GAP of the marriage line!; the 1914 baptism marginalia: Danica, married 1947 in Gradec!) × Johan KURE, 22, half smallholder's-son? [~], GRIBLJE 62 (the 4th KURE evidence!) = ★ the DOUBLE; parents: Johan Požek? ¼ Hübler × Maria Brinec? [~] / Anton Kure ½ Hübler × Barbara Križan; witnesses Nicolaus Kure + Johann Dragoš; the Griblje commune certificate Nov 26, 1906 no: 3 + the provincial government Ljubljana no: 23993; priest Jos. Rauy — POŽEK ×3 in the year (the v5 mother + the v11 bride+father!)",
    status: "DOCUMENTED",
  },

  // ——— P136 razširitev: POROČNA KNJIGA 04455 — polno leto 1907 (skeni 132–134 ==
  // Pag. 131–133; glava »1907« na s132 + »1908« na s134 = P137 lead) — 12 vpisov
  // (P136-lead »min 5« 2,4× podcenjen — 22. leto zapored!); ★ 12/12 PONEDELJKOV =
  // 2. popolno ponedeljkovsko leto (po P134 11/11!); ★ DISPENSA 2. kolena stranske
  // vrste (ordinariat Ljubljana 28/8. 1907 — v11!); ★ 2 KOVAČ-družini na h6 (Nicolaus
  // + Georg!) = 2 bloka hiše v letu; ★ 20-LETNA LUKNJA h3; ★ NOVA hiša h19; ★
  // PEZDIREC-mreža ×5 + MUC ×3 + NOVAK ×3; ★ 1. ne-Rauy podpis [~ Pavlič?] (v7);
  // pokojni oče Žugelj † (v12); zglašnica št. 119 (občina Dobliče? [~]) ———
  {
    houseNo: "19",
    bookSignature: "04455",
    year: 1907,
    scan: 132,
    page: 131,
    whatSi: "poroka (18. 2. 1907, vpis 4) — ženin Nikolaus HRANC [~ Hranč? — nov priimek!], ¼ griblar, 22 (mladoleten — proglas polnoletnosti!), GRIBLJE 19 (★ 1. POROČNI DOKAZ h19 = NOVA HIŠA = 66. poročna hiša korpusa!) × Catharina KLEPEC, ¼ griblarjeva hči, 18 (mladoletna!), Krasinec 36; starši: Nicolaus Hranc ½ Hübler × Maria KRALJ / Nicolaus Klepec ½ Hübler × Barbara DORN [~ Dornik? — cf. P127-v23 popravek Dornik→DOMUŠEK!]; priči Peter STRAUS [~ — STRAUS-mreža h32/h46/h22!] + Joseph PEZDIREC ½ Hübler; zglašnica občine Podzemelj [20/1?] 1907 št. 4 + proglas polnoletnosti za ženina od okrajnega sodišča v Metliki [15/1?] 1907; duhovnik Jos. Rauy — OBA mladoletna!",
    whatEn: "marriage (Feb 18, 1907, entry 4) — the groom Nikolaus HRANC [~ Hranc? — a new surname!], quarter smallholder, 22 (a minor — the majority declaration!), GRIBLJE 19 (★ the 1st MARRIAGE EVIDENCE of h19 = A NEW HOUSE = the 66th marriage house of the corpus!) × Catharina KLEPEC, quarter smallholder's daughter, 18 (a minor!), Krasinec 36; parents: Nicolaus Hranc ½ Hübler × Maria KRALJ / Nicolaus Klepec ½ Hübler × Barbara DORN [~ Dornik? — cf. the P127-v23 correction Dornik→DOMUŠEK!]; witnesses Peter STRAUS [~ — the STRAUS network h32/h46/h22!] + Joseph PEZDIREC ½ Hübler; the Podzemelj commune certificate [Jan 20?] 1907 no. 4 + the majority declaration for the groom from the Metlika district court [Jan 15?] 1907; priest Jos. Rauy — BOTH minors!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04455",
    year: 1907,
    scan: 132,
    page: 131,
    whatSi: "poroka (25. 2. 1907, vpis 5) — ženin Franz KOVAČ, ½ griblar, [24? — starost neberljiva!], GRIBLJE 6 (2. poročni dokaz h6 — 1903 P132 v14 Jakobčič!) × Theresia KRIŽAN, ½ griblarjeva hči, [24?], GRIBLJE 7 (3. poročni dokaz h7 — 1889 Totter + 1900 Töller!) = ★ DRUBEL sosednjih hiš (6×7 — 1. drubel po P135!); starši: Nicolaus Kovač ½ Hübler × Catharina DORN [~] (★ ≠ v11-oče Georg — DVE Kovač-družini na h6!) / Johann Križan ½ Hübler × Maria BAJUK; priči Martin PEZDIREC + Johann [~]; zglašnica občine Podzemelj [30/1?] 1907 št. 3; duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 25, 1907, entry 5) — the groom Franz KOVAČ, half smallholder, [24? — the age illegible!], GRIBLJE 6 (the 2nd marriage evidence of h6 — 1903 P132 v14 Jakobčič!) × Theresia KRIŽAN, half smallholder's daughter, [24?], GRIBLJE 7 (the 3rd marriage evidence of h7 — 1889 Totter + 1900 Töller!) = ★ the DOUBLE of the neighboring houses (6×7 — the 1st double since P135!); parents: Nicolaus Kovač ½ Hübler × Catharina DORN [~] (★ ≠ the v11 father Georg — TWO Kovač families at h6!) / Johann Križan ½ Hübler × Maria BAJUK; witnesses Martin PEZDIREC + Johann [~]; the Podzemelj commune certificate [Jan 30?] 1907 no. 3; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04455",
    year: 1907,
    scan: 132,
    page: 131,
    whatSi: "poroka (25. 2. 1907, vpis 5) — nevesta Theresia KRIŽAN, ½ griblarjeva hči, [24?], GRIBLJE 7 (3. poročni dokaz h7 — 1889 P118 v4 Totter + 1900 P129 v2 Töller? + 1907 = 7-letna vrzel!) × Franz KOVAČ, GRIBLJE 6 = ★ DRUBEL sosednjih hiš; starši: Johann Križan ½ Hübler × Maria BAJUK (BAJUK-mreža!) / Nicolaus Kovač ½ Hübler × Catharina Dorn [~]; priči Martin Pezdirec + Johann [~]; zglašnica občine Podzemelj [30/1?] 1907 št. 3; duhovnik Jos. Rauy — KRIŽAN ×2 v letu (v5-nevesta + v1-mati Županič!)",
    whatEn: "marriage (Feb 25, 1907, entry 5) — the bride Theresia KRIŽAN, half smallholder's daughter, [24?], GRIBLJE 7 (the 3rd marriage evidence of h7 — 1889 P118 v4 Totter + 1900 P129 v2 Töller? + 1907 = a 7-year gap!) × Franz KOVAČ, GRIBLJE 6 = ★ the DOUBLE of the neighboring houses; parents: Johann Križan ½ Hübler × Maria BAJUK (the BAJUK network!) / Nicolaus Kovač ½ Hübler × Catharina Dorn [~]; witnesses Martin Pezdirec + Johann [~]; the Podzemelj commune certificate [Jan 30?] 1907 no. 3; priest Jos. Rauy — KRIŽAN ×2 in the year (the v5 bride + the v1 Županič mother!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04455",
    year: 1907,
    scan: 133,
    page: 132,
    whatSi: "poroka (3. 6. 1907, vpis 9) — ženin Johann PEZDIREC, ½ griblarjev sin, 29, GRIBLJE 3 (2. poročni dokaz h3 — 1887 P116 → 1907 = ★ 20-LETNA LUKNJA poročne linije, 2. najdaljša po h21 [19 let]!; PEZDIREC-družina doslej Griblje 20 [P132 v17] — NOVA veja!) × Magdalena HLEBEC, 25, Vranoviče 5; starši: Michael Pezdirec ½ Hübler × Maria JAKŠEVIĆ [~ Jakšew? — 1. -ić-priimek po Đeleković 1906!] / Johann Hlebec ½ Hübler × Ana ŠIKORNY [~ — nov priimek!]; priči Nicolaus ŠIKORNY [~ — brat matere?] + Georg [~]; zglašnica občine DOBLIČE? [~] z dne 2/6. 1907 št: 119 (★ najvišja številka dokumenta leta!) + list od župnega urada [~]; duhovnik Jos. Rauy — PEZDIREC-mreža ×5 v letu (v3-mati + v5-priča + v6/v7-nevesti + v9-ženin!)",
    whatEn: "marriage (Jun 3, 1907, entry 9) — the groom Johann PEZDIREC, half smallholder's son, 29, GRIBLJE 3 (the 2nd marriage evidence of h3 — 1887 P116 → 1907 = ★ a 20-YEAR GAP of the marriage line, the 2nd longest after h21 [19 years]!; the PEZDIREC family previously Griblje 20 [P132 v17] — A NEW branch!) × Magdalena HLEBEC, 25, Vranoviče 5; parents: Michael Pezdirec ½ Hübler × Maria JAKŠEVIĆ [~ Jakšew? — the 1st -ić surname after Đeleković 1906!] / Johann Hlebec ½ Hübler × Ana ŠIKORNY [~ — a new surname!]; witnesses Nicolaus ŠIKORNY [~ — the mother's brother?] + Georg [~]; the DOBLIČE? [~] commune certificate of Jun 2, 1907 no: 119 (★ the highest document number of the year!) + a sheet from the parish office [~]; priest Jos. Rauy — the PEZDIREC network ×5 in the year (the v3 mother + the v5 witness + the v6/v7 brides + the v9 groom!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04455",
    year: 1907,
    scan: 134,
    page: 133,
    whatSi: "poroka (16. 9. 1907, vpis 11) — nevesta Barbara KOVAČ, ¼ griblarjeva hči, 21, GRIBLJE 6 (3. poročni dokaz h6 — 1903 Jakobčič + v5 Franz ISTEM LETU = ★ 2. BLOK hiše v letu, edini leta!) × Mathäus ŽUGELJ, ¼ griblar, 24, Krasinec 4 [~]; ★ DISPENSA OD KRVNEGA SORODSTVA V 2. KOLENU STRANSKE VRSTE od knj. čh. ordinarijata v LJUBLJANI od 28/8. 1907 (1. dispensa po P134-1905! — bratranci!); starši: Mathias Žugelj ¼ Hübler × Anna Justarič? [~ Lustari?] / Georg Kovač ½ Hübler (★ ≠ v5-oče Nicolaus — DVE Kovač-družini na h6, brata?!) × Anna JAKOFČIČ (Jakofčič-mreža h9/h16!); priči Nicolaus Vodlovnič? [~] ½ Hübler + Anton [~]; zglašnica [mestne?] občine Podzemelj od 14/9. 1907 št. 10; duhovnik Jos. Rauy — ŽUGELJ ×2 v 2 tednih (v11-ženin + v12-nevesta!)",
    whatEn: "marriage (Sep 16, 1907, entry 11) — the bride Barbara KOVAČ, quarter smallholder's daughter, 21, GRIBLJE 6 (the 3rd marriage evidence of h6 — 1903 Jakobčič + the v5 Franz THE SAME YEAR = ★ the 2ND BLOCK of the house in the year, the only one of the year!) × Mathäus ŽUGELJ, quarter smallholder, 24, Krasinec 4 [~]; ★ THE DISPENSATION FROM THE BLOOD RELATIONSHIP IN THE 2ND DEGREE OF THE COLLATERAL LINE from the episcopal ordinariate in LJUBLJANA of Aug 28, 1907 (the 1st dispensation since P134-1905! — cousins!); parents: Mathias Žugelj ¼ Hübler × Anna Justarič? [~ Lustari?] / Georg Kovač ½ Hübler (★ ≠ the v5 father Nicolaus — TWO Kovač families at h6, brothers?!) × Anna JAKOFČIČ (the Jakofčič network h9/h16!); witnesses Nicolaus Vodlovnič? [~] ½ Hübler + Anton [~]; the [town?] Podzemelj commune certificate of Sep 14, 1907 no. 10; priest Jos. Rauy — ŽUGELJ ×2 in 2 weeks (the v11 groom + the v12 bride!)",
    status: "DOCUMENTED",
  },

  // ——— P137 razširitev: POROČNA KNJIGA 04455 — polno leto 1908 (skeni 134–138 ==
  // Pag. 133–137; glava »1908« na s134 dno (y≈980) POTRJENA + glava »1909« na
  // s138 (y≈600) = P138 lead) — 17 vpisov (P137-lead »min 2« 8,5× podcenjen —
  // 23. leto zapored!); ★★ 73-LETNI ŽENIN (v16) = NOVI REKORD LINIJE (prej 62
  // P135!); ★★★ INTRA-HIŠNA POROKA h14 × h14 (v17 — 1. v 23 letih!); ★★★
  // AFINITETNA DISPENSA 1. KOLENA (v17: ženin × SESTRA pokojne žene! — hčerka
  // krščena 16. 2. 1908, 9 mesecev PRED poroko!); ★★ 4 DISPENZE v letu (v3 št.
  // 265 + v5 + v15 št. 4208 + v17 — vs 1 v 1907!); ★★ 1. RAZVEZANI ŽENIN (v5 —
  // modri zapis o sodbi!); ★ RECIPROČNA poroka Požek×Kure po Kure×Požek 1906
  // (v1); ★ GRIBLJE-DRUBEL h39 × h44 (v10); ★ NOVA hiša h43 (v9 — 67. poročna
  // hiša korpusa); ★ MASA 10. 2. ×3 (v5+v6+v7); ★ 4 NEDELJSKE poroke (v1+v2 isti
  // dan 26. 1. + v15 + v16); ★ DEHLIČ × DEHLIČ istopriimčna (v14); NOVI DUHOVNIK
  // Jos. Dami [~] (krstna linija 1908!) + NOVE VASI (Mehovce pf. Podgrad ·
  // Drašiči · Vranoviče 28/30 · Cerkvišče 35/10 povrat · Kapljišče?) ———
  {
    houseNo: "21",
    bookSignature: "04455",
    year: 1908,
    scan: 134,
    page: 133,
    whatSi: "poroka (26. 1. 1908, vpis 1 — NEDELJA) — ženin Johann POŽEK, ¼ griblar, 58, GRIBLJE 21 (3. poročni dokaz h21 — 1888 v3 + 1889 v3 → 1908 = 19-LETNA LUKNJA; ★ ženin = ISTI KOT 1889-v3 (starši ISTI Johann Požek × Barbara Dragoš!; 39 → 58 let) — 2. poroka po 19 letih; 1. žena Anna Simec h54 †) × Catharina KURE, ¼ griblarjeva hči [~], 28, GRIBLJE 62 (5. poročni dokaz h62 — 1893+1898+1904+1906+1908!; sestra 1906-v11 ženina Johana Kure!) = ★ RECIPROČNA poroka po 1906-v11 (Kure × Požek h62×h21 → zrcalni h21×h62!); starši: Johann Požek ¼ Hübler × Barbara Dragoš (DRAGOŠ-mreža 13.+ leto!) / Anton Kure ½ Hübler × Barbara Križan (= 1906-v11 starši ISTI!); priči Johann Dragoš + Johann Brinovec [~ Brinec?] Hübler; zglašnica občine Griblje od 25/1. 1908 št. 1; duhovnik Jos. Rauy p.f.",
    whatEn: "marriage (Jan 26, 1908, entry 1 — SUNDAY) — the groom Johann POŽEK, quarter smallholder, 58, GRIBLJE 21 (the 3rd marriage evidence of h21 — 1888 v3 + 1889 v3 → 1908 = a 19-YEAR GAP; ★ the groom = THE SAME as 1889-v3 (the parents the same Johann Požek × Barbara Dragoš!; 39 → 58 years) — the 2nd marriage after 19 years; the 1st wife Anna Simec of h54 †) × Catharina KURE, quarter smallholder's daughter [~], 28, GRIBLJE 62 (the 5th marriage evidence of h62 — 1893+1898+1904+1906+1908!; the sister of the 1906-v11 groom Johan Kure!) = ★ the RECIPROCAL marriage after 1906-v11 (Kure × Požek h62×h21 → the mirror h21×h62!); parents: Johann Požek ¼ Hübler × Barbara Dragoš (the 13th+ year of the DRAGOŠ network!) / Anton Kure ½ Hübler × Barbara Križan (= the 1906-v11 parents the same!); witnesses Johann Dragoš + Johann Brinovec [~ Brinec?] Hübler; the Griblje commune certificate of Jan 25, 1908 no. 1; priest Jos. Rauy p.f.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04455",
    year: 1908,
    scan: 134,
    page: 133,
    whatSi: "poroka (26. 1. 1908, vpis 1 — nevesta) — Catharina KURE, ¼ griblarjeva hči [~], 28, GRIBLJE 62 (5. poročni dokaz h62 — KURE-kontinuiteta 15 let!; krstna h62 1887+1891+1907 → poroka 1908 [Kure × Požek!] — 3. knjiga povezuje!) × Johann POŽEK, 58, GRIBLJE 21 (★ = 1889-v3 ženin ISTI — druga poroka!); starši: Anton Kure ½ Hübler × Barbara Križan (ISTA kot 1906-v11!) / Johann Požek ¼ Hübler × Barbara Dragoš (ISTA kot 1889!); priči Johann Dragoš + Johann Brinovec [~]; zglašnica Griblje 25/1. 1908 št. 1; duhovnik Jos. Rauy — ★ RECIPROČNI par z 1906-v11 (h62×h21 ↔ h21×h62)!",
    whatEn: "marriage (Jan 26, 1908, entry 1 — the bride) — Catharina KURE, quarter smallholder's daughter [~], 28, GRIBLJE 62 (the 5th marriage evidence of h62 — a 15-year KURE continuity!; the h62 baptisms 1887+1891+1907 → the 1908 marriage [Kure × Požek!] — the 3rd book connects!) × Johann POŽEK, 58, GRIBLJE 21 (★ = the 1889-v3 groom the same — a second marriage!); parents: Anton Kure ½ Hübler × Barbara Križan (the same as 1906-v11!) / Johann Požek ¼ Hübler × Barbara Dragoš (the same as 1889!); witnesses Johann Dragoš + Johann Brinovec [~]; the Griblje certificate Jan 25, 1908 no. 1; priest Jos. Rauy — ★ the RECIPROCAL pair with 1906-v11 (h62×h21 ↔ h21×h62)!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "28",
    bookSignature: "04455",
    year: 1908,
    scan: 135,
    page: 134,
    whatSi: "poroka (10. 2. 1908, vpis 5 — ponedeljek, 1. od 3 porok dne = MASA!) — nevesta Catharina POŽEK, ¼ griblarjeva hči, 24, GRIBLJE 28 (★ 1. POROČNI DOKAZ h28 v poročni knjigi — h28 = POŽEK-VERIGA krstne (h79 1888 → h77 1890 → h28 1891); 17-letna poročna luknja po krstu 1891!) × Georg ŽARKOVIČ [~ — nov priimek!], ¾ griblar, 26, [Trbeneč? ~ pf. Adlešiči]; ★ MODRI ZAPIS ŽENINA: 1. zakon RAZVEZAN (sodba [okrajnega sodišča v Novem mestu? ~] — ★★ 1. RAZVEZA LINIJE 1886–1908!); starši: Georg [Jurij] Požek Hübler × Margareth [Marjeta] Milkovič (= 1891-krst h28 starša ISTA — Milkovič = Milek-varianta!) / Georg Žarkovič Hübler × Ana Škalič [~]; priči Joseph Kostelič [~] + Johann Černič [~] (Hübler); zglašnica občine [Vrbičice? ~] od 8/2. 1908 št. 32 + [oklicni list?] od oblasti v Adlešičih 9/2. 1908 št. 33 + ★ DISPENSA [v 3. kolenu? ~] od kr. šk. ordinarijata (2. od 4-ih leta!); duhovnik Jos. Rauy",
    whatEn: "marriage (Feb 10, 1908, entry 5 — Monday, the 1st of 3 weddings of the day = the MASS!) — the bride Catharina POŽEK, quarter smallholder's daughter, 24, GRIBLJE 28 (★ the 1st MARRIAGE EVIDENCE of h28 in the marriage book — h28 = the baptismal POŽEK CHAIN (h79 1888 → h77 1890 → h28 1891); a 17-year marriage gap after the 1891 baptism!) × Georg ŽARKOVIČ [~ — a new surname!], three-quarter smallholder, 26, [Trbeneč? ~ pf. Adlešiči]; ★ the groom's BLUE NOTE: the 1st marriage DISSOLVED (a judgment [of the Novo mesto district court? ~] — ★★ the 1st DIVORCE of the line 1886–1908!); parents: Georg [Jurij] Požek Hübler × Margareth [Marjeta] Milkovič (= the 1891 baptism h28 parents the same — Milkovič = a Milek variant!) / Georg Žarkovič Hübler × Ana Škalič [~]; witnesses Joseph Kostelič [~] + Johann Černič [~] (Hübler); the [Vrbičice? ~] commune certificate of Feb 8, 1908 no. 32 + [a banns list?] of the Adlešiči authority Feb 9, 1908 no. 33 + ★ a DISPENSATION [in the 3rd degree? ~] of the episcopal ordinariate (the 2nd of 4 of the year!); priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "43",
    bookSignature: "04455",
    year: 1908,
    scan: 136,
    page: 135,
    whatSi: "poroka (17. 2. 1908, vpis 9 — ponedeljek) — nevesta Maria LASIČ [~ Losic? — LASIč: boter h47 1887!], 29, GRIBLJE 43 (★ 1. POROČNI DOKAZ h43 = NOVA HIŠA = 67. poročna hiša korpusa! PT luknja 41–60!) × Michael ŽUPANIČ, ¼ griblarjev sin, 30, Krasinec 18 (POVRAT hiše po 1897 — brat 1897-v5 ženina Nicolusa Županiča!) — ★ 2. POROČNA NEDOBLJENEGA RAZMERJA: nevesta Griblje × ženin Krasinec (medsebojni vzorec 1908!); starši: Johan Lasič [~] ¼ Hübler × Maria Vrčul [~] / Matija Županič ¼ Hübler (= 1897-v5 oče Mathias ISTI!) × Catharina Kramarič [~ — 1897-mati Štarasinič/Šaradinič? 2. žena? MERI!] (KRAMARIČ korpus ×10!); priči Nicolaus Brodarič (BRODARIČ ×2 leta!) + Peter Fiebler [~] ¼ Hübler; zglašnica občine Podzemelj od 16/2. [1908]; duhovnik Jos. Rauy — ŽUPANIČ ×2 leta (v1-nevesta Županič 1907 + v9-ženin!)",
    whatEn: "marriage (Feb 17, 1908, entry 9 — Monday) — the bride Maria LASIČ [~ Losic? — LASIč: an h47 godfather 1887!], 29, GRIBLJE 43 (★ the 1st MARRIAGE EVIDENCE of h43 = A NEW HOUSE = the 67th marriage house of the corpus! a PT gap house 41–60!) × Michael ŽUPANIČ, quarter smallholder's son, 30, Krasinec 18 (the house RETURNS after 1897 — the brother of the 1897-v5 groom Nicolaus Županič!); parents: Johan Lasič [~] ¼ Hübler × Maria Vrčul [~] / Matija Županič ¼ Hübler (= the 1897-v5 father Mathias the same!) × Catharina Kramarič [~ — the 1897 mother Štarasinič/Šaradinič? a 2nd wife? MERI!] (KRAMARIČ in the corpus ×10!); witnesses Nicolaus Brodarič (BRODARIČ ×2 in the year!) + Peter Fiebler [~] ¼ Hübler; the Podzemelj commune certificate of Feb 16 [1908]; priest Jos. Rauy — ŽUPANIČ ×2 in the year (the 1907 v1 bride Županič + the v9 groom!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "39",
    bookSignature: "04455",
    year: 1908,
    scan: 136,
    page: 135,
    whatSi: "poroka (2. 3. 1908, vpis 10 — ponedeljek) — ženin Johann ŠIMEC, ¼ griblarjev sin, 21, GRIBLJE 39 (2. poročni dokaz h39 — 1897-v11 nevesta Maria Simec = Sestra!; starši ISTI!) × Barbara KLOBUČAR, ¼ griblarjeva hči [~], 20 (mladoletna — vlada!), GRIBLJE 44 = ★ GRIBLJE-DRUBEL h39 × h44 (2. drubel zapored po h6×h7 1907!); ★ Barbara = 1887-krst h47 ISTA (Peter Klobučar × Marija Filath/Tilak — 20. november 1887 → poročena 2. 3. 1908!); starši: Nikolaus Šimec ¼ Hübler × Catharina Jakobčič (= 1897-v11 starši ISTI!) / Peter Klobučar (= 1887-krst oče!) × Maria Tilak [~ Filath/Filak/Šilak — 3 pisave!]; priči [Mathias Hušić? ~] + [Mathias Moh? ~] ¼ Hübler; zglašnica občine Griblje [13/1?] 1908 št. 2 + [prijava ženina ~ Mihael? Drenovlje?] od 13/12. 1907 št. 3 + ★ DOVOLJENJE c. kr. vlade v Ljubljani od 19/2. 1908 št. 4167 (mladoletna nevesta!); duhovnik [Jos. Dami? ~ — novi kaplan 1908!]",
    whatEn: "marriage (Mar 2, 1908, entry 10 — Monday) — the groom Johann ŠIMEC, quarter smallholder's son, 21, GRIBLJE 39 (the 2nd marriage evidence of h39 — the 1897-v11 bride Maria Simec = his sister!; the parents the same!) × Barbara KLOBUČAR, quarter smallholder's daughter [~], 20 (a minor — the government!), GRIBLJE 44 = ★ the DOUBLE-GRIBLJE h39 × h44 (the 2nd double in a row after h6×h7 of 1907!); ★ Barbara = the 1887 baptism h47 the same (Peter Klobučar × Marija Filath/Tilak — Nov 20, 1887 → married Mar 2, 1908!); parents: Nikolaus Šimec ¼ Hübler × Catharina Jakobčič (= the 1897-v11 parents the same!) / Peter Klobučar (= the 1887-baptism father!) × Maria Tilak [~ Filath/Filak/Šilak — 3 spellings!]; witnesses [Mathias Hušić? ~] + [Mathias Moh? ~] ¼ Hübler; the Griblje commune certificate [Jan 13?] 1908 no. 2 + [the groom's application ~ Mihael? Drenovlje?] of Dec 13, 1907 no. 3 + ★ the GOVERNMENT permission of the k.k. government in Ljubljana of Feb 19, 1908 no. 4167 (an underage bride!); priest [Jos. Dami? ~ — the new curate of 1908!]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04455",
    year: 1908,
    scan: 136,
    page: 135,
    whatSi: "poroka (2. 3. 1908, vpis 10 — nevesta) — Barbara KLOBUČAR, ¼ griblarjeva hči [~], 20 (mladoletna!), GRIBLJE 44 (3. poročni dokaz h44 — 1899-v1 Mathias Klobučar-hiša + 1903-v20 Štrucelj — ★ KLOBUČAR POVRAT na hišo!; Barbara rojena na h47 (krst 1887) — poročena s h44!) × Johann ŠIMEC, 21, GRIBLJE 39 = ★ DRUBEL h44 × h39; starši: Peter Klobučar (= h47-krst 1887!) × Maria Tilak [~ Filath!] / Nikolaus Šimec × Catharina Jakobčič (= h39 ISTA družina!); priči [~]; zglašnica Griblje št. 2 + vlada-dovoljenje št. 4167 (19/2. 1908!); duhovnik [Jos. Dami? ~] — KLOBUČAR ×2 leta (v10-nevesta + priča?)",
    whatEn: "marriage (Mar 2, 1908, entry 10 — the bride) — Barbara KLOBUČAR, quarter smallholder's daughter [~], 20 (a minor!), GRIBLJE 44 (the 3rd marriage evidence of h44 — the 1899-v1 Mathias Klobučar house + the 1903-v20 Štrucelj — ★ a KLOBUČAR RETURN to the house!; Barbara born at h47 (the 1887 baptism) — married from h44!) × Johann ŠIMEC, 21, GRIBLJE 39 = ★ the DOUBLE h44 × h39; parents: Peter Klobučar (= the h47 baptism 1887!) × Maria Tilak [~ Filath!] / Nikolaus Šimec × Catharina Jakobčič (= the h39 same family!); witnesses [~]; the Griblje certificate no. 2 + the government permission no. 4167 (Feb 19, 1908!); priest [Jos. Dami? ~] — KLOBUČAR ×2 in the year (the v10 bride + a witness?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04455",
    year: 1908,
    scan: 137,
    page: 136,
    whatSi: "poroka (22. 6. 1908, vpis 14 — ponedeljek) — nevesta Catharina DEHLIČ, ½ griblarjeva hči, 24, GRIBLJE 33 (2. poročni dokaz h33 — 1888-v2 Maria Dehlič (23) → 1908 Catharina (24) = ★ ISTA DRUŽINA Mathias Dehlič × Maria Husič po 20 LETIH — 2. najdaljša hišna kontinuiteta poročne linije!) × Thomas DEHLIČ, lastnik, 49, Krasinec 53 (★ DEHLIČ × DEHLIČ — 1. istopriimčna poroka po P135-v2/v3!; sorodstvo? — BREZ dispensa-zapisa [~]); starši: Matthias Dehlič ½ Hübler × Marica Hušič (= 1888-v2 starša ISTA!) / Thomas Dehlič kmet [~] × Rosa Vurnas [~]; priči Johann Vurnas [~] + Matthias Brinsec [~] ¼ Hübler (BRINEC-mreža!); [uradna? svetba? ~ Poglavarstva občine v Ribnici? ~ — NOV TIP DOKUMENTA? ~] dne [14.?] 1908 br. 1555; duhovnik [Jos. Rauy P.f.? ~]",
    whatEn: "marriage (Jun 22, 1908, entry 14 — Monday) — the bride Catharina DEHLIČ, half smallholder's daughter, 24, GRIBLJE 33 (the 2nd marriage evidence of h33 — the 1888-v2 Maria Dehlič (23) → the 1908 Catharina (24) = ★ the SAME FAMILY Mathias Dehlič × Maria Husič after 20 YEARS — the 2nd longest house continuity of the marriage line!) × Thomas DEHLIČ, owner, 49, Krasinec 53 (★ DEHLIČ × DEHLIČ — the 1st same-surname wedding after P135-v2/v3!; kinship? — WITHOUT a dispensation note [~]); parents: Matthias Dehlič ½ Hübler × Marica Hušič (= the 1888-v2 parents the same!) / Thomas Dehlič a peasant [~] × Rosa Vurnas [~]; witnesses Johann Vurnas [~] + Matthias Brinsec [~] ¼ Hübler (the BRINEC network!); [an official certificate? ~ of the municipality of Ribnica? ~ — a NEW document type? ~] of [the 14th?] 1908 no. 1555; priest [Jos. Rauy P.f.? ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04455",
    year: 1908,
    scan: 138,
    page: 137,
    whatSi: "poroka ([25. 11.?] 1908, vpis 17 — ZADNJI 1908) — ženin Johann BRINEC, ¼ griblar, 46 (vdovec!), GRIBLJE 14 (2. poročni dokaz h14 — ★ ženin = 1895-v17 ISTI (33 → 46 let; starši Peter Brinec × Anna Štraus ISTI!) — oženil se je v nevestino hišo h14 1895, žena Maria Pezdirec †, ŽE 9 MESECEV ZAČETEK Z Dorotheo!) × Dorothea PEZDIREC, ¼ griblarjeva hči, 27, GRIBLJE 14 (★★ ISTA HIŠA kot ženin — 1. INTRA-HIŠNA POROKA LINIJE 1886–1908 (h14 × h14)!; ★★ hčerka krščena 16. 2. 1908 na h14 (oče Janez Brinec × Doroteja Perdinec — P103! — 9 mesecev PRED poroko!); sestra pokojne ženinove 1. žene Marije!); ★★ DISPENSA V 1. KOLENU [AFINITETE? — ženin × SESTRA pokojne žene = sororate! — najhujša sorodstvena zapreka linije!] od knj. šk. ordinarijata v Ljubljani [22. okt. 1908 št. 10.350? ~] + [dovoljenje c. kr. vlade? ~]; zglašnica občine Griblje od 15. okt. 1908 št. 1; starši: Peter Brinec ½ Hiebler × Anna Štraus (ISTA 1895!) / Michael Pezdirec ¼ Hiebler × Anna Brinec (= 1895 nevestina starša ISTA! — mati roj. Brinec!); priči Martin Gregorič [~] + Simončič [~] (Häusler); duhovnik Jos. Rauy pf. — 4. dispensa leta 1908!",
    whatEn: "marriage ([Nov 25?] 1908, entry 17 — the LAST of 1908) — the groom Johann BRINEC, quarter smallholder, 46 (a widower!), GRIBLJE 14 (the 2nd marriage evidence of h14 — ★ the groom = the 1895-v17 same (33 → 46 years; the parents Peter Brinec × Anna Štraus the same!) — he married into the bride's house h14 in 1895, the wife Maria Pezdirec †, ALREADY 9 MONTHS WITH Dorothea!) × Dorothea PEZDIREC, quarter smallholder's daughter, 27, GRIBLJE 14 (★★ the SAME HOUSE as the groom — the 1st INTRA-HOUSE WEDDING of the line 1886–1908 (h14 × h14)!; ★★ a daughter baptized Feb 16, 1908 at h14 (father Janez Brinec × Doroteja Perdinec — P103! — 9 months BEFORE the wedding!); the sister of the groom's deceased 1st wife Maria!); ★★ the DISPENSATION in the 1st degree [of AFFINITY? — the groom × the SISTER of the deceased wife = sororate! — the gravest impediment of the line!] of the episcopal ordinariate in Ljubljana [Oct 22, 1908 no. 10.350? ~] + [a k.k. government permission? ~]; the Griblje commune certificate of Oct 15, 1908 no. 1; parents: Peter Brinec ½ Hiebler × Anna Štraus (the same as 1895!) / Michael Pezdirec ¼ Hiebler × Anna Brinec (= the 1895 bride's parents the same! — the mother née Brinec!); witnesses Martin Gregorič [~] + Simončič [~] (Häusler); priest Jos. Rauy pf. — the 4th dispensation of the year 1908!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04455",
    year: 1908,
    scan: 138,
    page: 137,
    whatSi: "poroka ([25. 11.?] 1908, vpis 17 — nevesta) — Dorothea PEZDIREC, ¼ griblarjeva hči, 27, GRIBLJE 14 (★★ 1. INTRA-HIŠNA POROKA (h14 × h14 — ista hiša obakrat!); h14 = PEZDIREC-hiša: 1895-v17 sestra Maria (28) poročila Johanna Brineca → † → 1908 Dorothea (27) poroči ISTEGA moža!; krst h14 16. 2. 1908 [P103]: oče Janez Brinec × Doroteja Perdinec — hčerka rojena PRED poroko!) × Johann BRINEC, 46 (vdovec), GRIBLJE 14; ★★ AFINITETNA DISPENSA 1. KOLENA (sestra pokojne žene!) + zglašnica Griblje 15/10 št. 1 + [vlada? ~]; starši: Michael Pezdirec ¼ Hiebler × Anna Brinec (ISTA 1895!) / Peter Brinec × Anna Štraus (ISTA 1895!); priči [~]; duhovnik Jos. Rauy pf. — PEZDIREC-mreža 1907 ×5 → 1908 ×2 (v15-nevesta Drašiči + v17!)",
    whatEn: "marriage ([Nov 25?] 1908, entry 17 — the bride) — Dorothea PEZDIREC, quarter smallholder's daughter, 27, GRIBLJE 14 (★★ the 1st INTRA-HOUSE WEDDING (h14 × h14 — the same house both times!); h14 = the PEZDIREC house: the 1895-v17 sister Maria (28) married Johann Brinec → † → in 1908 Dorothea (27) marries the SAME man!; the h14 baptism Feb 16, 1908 [P103]: father Janez Brinec × Doroteja Perdinec — a daughter born BEFORE the wedding!) × Johann BRINEC, 46 (a widower), GRIBLJE 14; ★★ the AFFINITY DISPENSATION of the 1st degree (the sister of the deceased wife!) + the Griblje certificate Oct 15 no. 1 + [the government? ~]; parents: Michael Pezdirec ¼ Hiebler × Anna Brinec (the same as 1895!) / Peter Brinec × Anna Štraus (the same as 1895!); witnesses [~]; priest Jos. Rauy pf. — the PEZDIREC network 1907 ×5 → 1908 ×2 (the v15 bride of Drašiči + v17!)",
    status: "DOCUMENTED",
  },

  // ——— P138 razširitev: POROČNA KNJIGA 04455 — polno leto 1909 (skeni 138–141 ==
  // Pag. 137–140; letnica 1909 se PIŠE V VSAKEM VPISU — NI letne glave (P137-lead
  // »glava s138« = prvi vpis!); 15 vpisov (№1–4 s138 + №5–8 s139 + NEŠTEVILČEN
  // 5. 7. + №8–12 s140 + №13–14 s141; P138-lead »min 4« 3,75× podcenjen — 24. leto
  // zapored!); ★★★ INTRA-HIŠNA POROKA h46 × h46 + DISPENSA 3. KOLENA (№11 — 2. v 2
  // letih po h14×h14!); ★★★ SPREGLED 1. KOLENA + SODNO DOVOLJENJE (№14 ordinariat
  // št. 4786 + deželno sodišče št. 27036 — dvojna zapreka!); ★★ SPREGLED 3. KOLENA
  // dotikajočega se 2. kolena (№13 TOME×TOME — ordinariat št. 4995); ★★ 14
  // PONEDDELJKOV + 1 NEDELJA = 93% PON (REKORD linije!); ★★ NEŠTEVILČEN VPIS =
  // VOJAŠKA POROKA Z DELEGACIJO (5. 7. — k.k. pehotni polk št. 9 št. 2045 +
  // delegacija 4/7 Z. 200 — poroka po pooblaščencu!); ★★ 2 GENDARMSKI POROKI (№7
  // Titular-Wachtmeister + №9); ★ NOVA HIŠA h57 (68. poročna hiša! Pezdirec 3.
  // hiša h20+h87+h57); ★ №4 ženin LEDIG 63 + nevesta 58 = par 121 let; ★ NOVE
  // OBLASTI: Videm + Dobrepolje + Rudolfštat/Novo mesto; ★ ~27 NOVIH PRIIMKOV;
  // ★ NOVI DUHOVNIKI Gregor Petar? + Pavlič? + Danijel; 1910 se začne na s141
  // (№1 Jakobčič × Jakobčič — intra-priimek lead P139!) ———
  {
    houseNo: "17",
    bookSignature: "04455",
    year: 1909,
    scan: 138,
    page: 137,
    whatSi: "poroka (25. 1. 1909, vpis 1 — PONEDELJEK) — nevesta Maria KRALJ, ¼ griblarjeva hči, 27, GRIBLJE 17 (2. poročni dokaz h17 — 1892-v10 Johann Kralj ¼ griblar 48 h17 → 1909 Maria 27 = oče→hči [~ VERIF]; 17-LETNA LUKNJA h17!) × Joseph STABJAN, hišar, 23, CERKVIŠČE 36 (★ NOV PRIIMEK za korpus — 1. pojav v 24 letih linije!); starši: Joseph Stübljan [~ Stabjan sr.] hišar × Barbara geb. Stübljan [~ — ista priimka?! VERIF] / Johan Kalj [~ Kralj? VERIF] Hübler × Anna Jakobčič; priči Georg Gnaubrijan? [~] + Georg Straus Hübler (STRARUS-korpus h32 1888!); zglašnica Podzemelj + očetovo ustno privoljenje; duhovnik Jos. Rauy P.P.",
    whatEn: "marriage (Jan 25, 1909, entry 1 — MONDAY) — the bride Maria KRALJ, quarter smallholder's daughter, 27, GRIBLJE 17 (the 2nd marriage evidence of h17 — the 1892-v10 Johann Kralj quarter smallholder 48 of h17 → the 1909 Maria 27 = father→daughter [~ VERIF]; a 17-YEAR GAP of h17!) × Joseph STABJAN, cottager, 23, CERKVIŠČE 36 (★ a NEW SURNAME for the corpus — the 1st appearance in 24 years of the line!); parents: Joseph Stübljan [~ Stabjan sr.] cottager × Barbara née Stübljan [~ — the same surname?! VERIF] / Johan Kalj [~ Kralj? VERIF] Hübler × Anna Jakobčič; witnesses Georg Gnaubrijan? [~] + Georg Straus Hübler (the STRAUS corpus h32 1888!); the Podzemelj certificate + the father's oral consent; priest Jos. Rauy P.P.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "74",
    bookSignature: "04455",
    year: 1909,
    scan: 139,
    page: 138,
    whatSi: "poroka (14. 6. 1909, vpis 6 — PONEDELJEK) — ženin Johann KAMBIČ, ¼ griblar, 32, GRIBLJE 74 (2. poročni dokaz h74 — 1893-v16 nevesta Catharina Kambič 22 h74 → 1909 Johann 32 = ISTA HIŠA-DRUŽINA po 16 letih!) × Maria MLEK [~ Milek — pisateljska varianta!], ¼ griblarjeva hči, 18, GRIBLJE 30 (3. poročni dokaz h30 — 1889-v8 Johann Milek 60 h30 → 1909 oče Johann Milek ¼ Hübler — MILEK-kontinuiteta 20 let!); ★ GRIBLJE × GRIBLJE poroka (h74 × h30 — 2. medsebojna v letu!); ★ 4 MREŽE v enem vpisu: Kambič + Milek + BRINEC (ženitova mati Catharina geb. Brinec!) + PEZDIREC (nevestina mati Margareta geb. Pezdirec!); starši: Mathias Kambič ¼ Hübler (1893-v16 sorodnik? [~]) × Catharina geb. Brinec / Johann Milek ¼ Hübler × Margareta geb. Pezdirec; priči [~ VERIF]; zglašnica OBČINE GRIBLJE 11. 6. 1909 št. 49 + sodno dovoljenje za ml. nevesto (okrajno sodišče Črnomelj 27. 5. 1909); duhovnik Jos. Rauy P.P.",
    whatEn: "marriage (Jun 14, 1909, entry 6 — MONDAY) — the groom Johann KAMBIČ, quarter smallholder, 32, GRIBLJE 74 (the 2nd marriage evidence of h74 — the 1893-v16 bride Catharina Kambič 22 of h74 → the 1909 Johann 32 = THE SAME HOUSE-FAMILY after 16 years!) × Maria MLEK [~ Milek — a scribal variant!], quarter smallholder's daughter, 18, GRIBLJE 30 (the 3rd marriage evidence of h30 — the 1889-v8 Johann Milek 60 of h30 → the 1909 father Johann Milek — a MILEK continuity of 20 years!); ★ a GRIBLJE × GRIBLJE wedding (h74 × h30 — the 2nd mutual one of the year!); ★ 4 NETWORKS in one entry: Kambič + Milek + BRINEC (the groom's mother née Brinec!) + PEZDIREC (the bride's mother née Pezdirec!); parents: Mathias Kambič ¼ Hübler (a 1893-v16 relative? [~]) × Catharina née Brinec / Johann Milek ¼ Hübler × Margareta née Pezdirec; witnesses [~ VERIF]; the GRIBLJE COMMUNE certificate Jun 11, 1909 no. 49 + the court permit for the minor bride (the district court of Črnomelj May 27, 1909); priest Jos. Rauy P.P.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04455",
    year: 1909,
    scan: 139,
    page: 138,
    whatSi: "poroka (14. 6. 1909, vpis 6 — nevesta) — Maria MLEK [~ Milek], ¼ griblarjeva hči, 18, GRIBLJE 30 (3. poročni dokaz h30 — MILEK-kontinuiteta 1889→1909 = 20 let!; sestrska hiša h29 [1897-v9 Maria Milek] — obe Milek-hiši!) × Johann KAMBIČ, 32, GRIBLJE 74 (2. poročni dokaz h74 — KAMBIČ-hiša 1893→1909!); starši: Johann Milek ¼ Hübler × Margareta geb. Pezdirec (PEZDIREC-mreža!) / Mathias Kambič ¼ Hübler × Catharina geb. Brinec (BRINEC-mreža!); zglašnica Griblje št. 49 + sodišče Črnomelj 27. 5.; duhovnik Jos. Rauy — ★ GRIBLJE × GRIBLJE (h74 × h30!)",
    whatEn: "marriage (Jun 14, 1909, entry 6 — the bride) — Maria MLEK [~ Milek], quarter smallholder's daughter, 18, GRIBLJE 30 (the 3rd marriage evidence of h30 — a MILEK continuity 1889→1909 = 20 years!; the sister house h29 [the 1897-v9 Maria Milek] — both Milek houses!) × Johann KAMBIČ, 32, GRIBLJE 74 (the 2nd marriage evidence of h74 — the KAMBIČ house 1893→1909!); parents: Johann Milek ¼ Hübler × Margareta née Pezdirec (the PEZDIREC network!) / Mathias Kambič ¼ Hübler × Catharina née Brinec (the BRINEC network!); the Griblje certificate no. 49 + the Črnomelj court May 27; priest Jos. Rauy — ★ a GRIBLJE × GRIBLJE wedding (h74 × h30!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "57",
    bookSignature: "04455",
    year: 1909,
    scan: 140,
    page: 139,
    whatSi: "poroka (19. 7. 1909, vpis 8 — PONEDELJEK) — nevesta Maria PEZDIREC, hišarjeva hči [~ VERIF stand], 24, GRIBLJE 57 (★ 1. POROČNI DOKAZ h57 — ZOOM-potrjeno 57 ≠ 87; ★★ h57 = PEZDIREC-HIŠA s krstmi 1888–1901: 1888 Marija (Peter Podolivec? [~ Pezdirec!] × Marija Borjanc) + 1889 Rudolf + 1894 Janez + 1899 Alojzij (VSI oče Peter Pezdirec [~ Pegdirec], mati Marija Županič [~]!) → 1909 poroka hčere = 20-LETNA PEZDIREC-kontinuiteta h57!; ★ starši poroke = ISTA starša kot krsti 1889–1899 (Peter Pezdirec × Maria Županič)!; [h20 1891-v7 ženin Peter Pezdirec = DRUGI Peter? ~ VERIF — glej h57-kriste!]) × Mathias MAVRETIČ [~ — 4 branjа: Klaventio/Marentič/Haverstic; ZOOM-potrjeno Mavretič!], ½ griblar, 39, GRADAC 15 (oče Mathias Mavretič sr. ½ Hübler — ista imeni!); starši: Mathias Mavretič sr. ½ Hübler × Maria geb. Novak / Peter Pezdirec Hübler (1891-v7!) × Maria geb. Županič; priči Nicolaus Lupanič? [~] + Anton Pezdirec (družinski priča!); zglašnica občine GRADAC 19/4 1909 št. 11; duhovnik Gregor Petar? [~ O.T. coop. — NOV DUHOVNIK? VERIF]",
    whatEn: "marriage (Jul 19, 1909, entry 8 — MONDAY) — the bride Maria PEZDIREC, cottager's daughter [~ VERIF status], 24, GRIBLJE 57 (★ the 1st MARRIAGE EVIDENCE of h57 — zoom-confirmed 57 ≠ 87; ★★ h57 = the PEZDIREC HOUSE with baptisms 1888–1901: the 1888 Marija (Peter Podolivec? [~ Pezdirec!] × Marija Borjanc) + the 1889 Rudolf + the 1894 Janez + the 1899 Alojzij (ALL the father Peter Pezdirec [~ Pegdirec], the mother Marija Županič [~]!) → the 1909 marriage of the daughter = a 20-YEAR PEZDIREC continuity of h57!; ★ the marriage parents = THE SAME parents as the 1889–1899 baptisms (Peter Pezdirec × Maria Županič)!; [the h20 1891-v7 groom Peter Pezdirec = ANOTHER Peter? ~ VERIF — see the h57 baptisms!]) × Mathias MAVRETIČ [~ — 4 readings: Klaventio/Marentič/Haverstic; zoom-confirmed Mavretič!], half smallholder, 39, GRADAC 15 (the father Mathias Mavretič sr. ½ Hübler — the same names!); parents: Mathias Mavretič sr. ½ Hübler × Maria née Novak / Peter Pezdirec Hübler (the 1891-v7!) × Maria née Županič; witnesses Nicolaus Lupanič? [~] + Anton Pezdirec (a family witness!); the GRADAC commune certificate Apr 19, 1909 no. 11; priest Gregor Petar? [~ O.T. coop. — a NEW PRIEST? VERIF]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04455",
    year: 1909,
    scan: 140,
    page: 139,
    whatSi: "poroka (8. 11. 1909, vpis 11 — PONEDELJEK) — ženin Johan ŽUGELJ [~ Zugel], ¼ griblarjev sin, 24, GRIBLJE 46 (2. poročni dokaz h46 — 1898-v20 Klobučar + Filak h46 → 1909 Žugelj — hiša ZAMENJA družino!; ŽUGELJ-mreža ×3 v letu: №5 Otok 9 + №10 Dobravice 21 + №11 h46!) × Agnes KLOBUČAR, ¼ griblarjeva hči, 23, GRIBLJE 46 (★★ INTRA-HIŠNA POROKA h46 × h46 — 2. v 2 letih po h14×h14 [1908-v17]!; KLOBUČAR-h46 kontinuiteta: 1898-v20 Catharina Klobučar 21 h46 [oče Markus?] → 1909 Agnes 23 = ISTA DRUŽINA po 11 letih!); ★★ DISPENSA 3. KOLENA enake stranske stopnje (šk. ordinariat Ljubljana 12. 10. 1909 št. 4571 — sorodstvo znotraj hiše!); starši: Mathias Žugelj ¼ Hübler × Ana geb. Kalj / Markus Klobučar ¼ Hübler (1898-v20 oče! [~ VERIF]) × Catharina geb. Milek (MILEK-mreža ×3 v letu!); priči Nicolaus FILAK (= 1898-v20 ženin h46 — 11-letna priča-kontinuiteta!) + Johann Kalj ½ Hübler (ženitova mati geb. Kalj!); zglašnica Podzemelj 4. 11. 1909 št. 8 + dispensa + očetovo dovoljenje; duhovnik Jos. Rauy",
    whatEn: "marriage (Nov 8, 1909, entry 11 — MONDAY) — the groom Johan ŽUGELJ [~ Zugel], quarter smallholder's son, 24, GRIBLJE 46 (the 2nd marriage evidence of h46 — the 1898-v20 Klobučar + Filak of h46 → the 1909 Žugelj — the house CHANGES family!; the ŽUGELJ network ×3 of the year: №5 Otok 9 + №10 Dobravice 21 + №11 h46!) × Agnes KLOBUČAR, quarter smallholder's daughter, 23, GRIBLJE 46 (★★ the INTRA-HOUSE WEDDING h46 × h46 — the 2nd in 2 years after h14×h14 [1908-v17]!; the KLOBUČAR-h46 continuity: the 1898-v20 Catharina Klobučar 21 of h46 [father Markus?] → the 1909 Agnes 23 = THE SAME FAMILY after 11 years!); ★★ the DISPENSATION of the 3rd DEGREE of the equal lateral line (the episcopal ordinariate of Ljubljana Oct 12, 1909 no. 4571 — kinship within the house!); parents: Mathias Žugelj ¼ Hübler × Ana née Kalj / Markus Klobučar ¼ Hübler (the 1898-v20 father! [~ VERIF]) × Catharina née Milek (the MILEK network ×3 of the year!); witnesses Nicolaus FILAK (= the 1898-v20 groom of h46 — an 11-year witness continuity!) + Johann Kalj ½ Hübler (the groom's mother née Kalj!); the Podzemelj certificate Nov 4, 1909 no. 8 + the dispensation + the father's permit; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04455",
    year: 1909,
    scan: 140,
    page: 139,
    whatSi: "poroka (8. 11. 1909, vpis 11 — nevesta) — Agnes KLOBUČAR, ¼ griblarjeva hči, 23, GRIBLJE 46 (★★ INTRA-HIŠNA POROKA h46 × h46 — 2. po h14×h14 1908!; KLOBUČAR-kontinuiteta h46: 1898-v20 Catharina → 1909 Agnes = 11 let!) × Johan ŽUGELJ, 24, GRIBLJE 46 (ŽUGELJ ×3 v letu + priča Filak = 1898-v20 ženin ISTA hiša!); ★★ DISPENSA 3. KOLENA (ordinariat Ljubljana 12/10 1909 št. 4571); starši: Markus Klobučar ¼ Hübler × Catharina geb. Milek (MILEK-mreža!) / Mathias Žugelj ¼ Hübler × Ana geb. Kalj (KALJ-mreža ×4 leta!); priči Nicolaus Filak + Johann Kalj; zglašnica št. 8; duhovnik Jos. Rauy",
    whatEn: "marriage (Nov 8, 1909, entry 11 — the bride) — Agnes KLOBUČAR, quarter smallholder's daughter, 23, GRIBLJE 46 (★★ the INTRA-HOUSE WEDDING h46 × h46 — the 2nd after the 1908 h14×h14!; the KLOBUČAR continuity of h46: the 1898-v20 Catharina → the 1909 Agnes = 11 years!) × Johan ŽUGELJ, 24, GRIBLJE 46 (the ŽUGELJ ×3 of the year + the witness Filak = the 1998-v20 groom of the SAME house!); ★★ the DISPENSATION of the 3rd DEGREE (the ordinariate of Ljubljana Oct 12, 1909 no. 4571); parents: Markus Klobučar ¼ Hübler × Catharina née Milek (the MILEK network!) / Mathias Žugelj ¼ Hübler × Ana née Kalj (the KALJ network ×4 of the year!); witnesses Nicolaus Filak + Johann Kalj; the certificate no. 8; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04455",
    year: 1909,
    scan: 141,
    page: 140,
    whatSi: "poroka (22. 11. 1909, vpis 13 — PONEDELJEK, isti dan kot №14!) — ženin Johann TOME [~ Toma — nov priimek 04455], ½ griblarjev sin, 29, GRIBLJE 1 (★ 3. poročni dokaz h1 — 1899-v3 Barbara Kure 27 h1 × Georg Željko → 1909 Johann Tome — hiša KURE/ŽELJKO/TOME!; 10-letna luknja h1) × Maria KURE, ½ griblarjeva hči, 18, GRIBLJE 29 (★ 3. poročni dokaz h29 — 1897-v9 Maria Milek 24 h29 (sestrska Milek-hiša h30!) → 1909 Maria Kure — hiša zamenja družino MILEK→KURE!; KURE-mreža 20 zadetkov 04455: h62 + h10 + zdaj h29!); ★ GRIBLJE × GRIBLJE (h1 × h29 — 3. medsebojna leta!); ★★ SPREGLED 3. KOLENA dotikajočega se 2. kolena (šk. ordinariat Ljubljana 9. 11. 1909 št. 4995 — ženin TOME × nevestina mati geb. TOME: sorodstvo po krvi IN afiniteta!); ★ priči = ENAKA PRIIMKA KOT ZAKONCA (Michael Tome ½ Hübler + Johan Kure ¼ Hübler — obe družini!); starši: Johann Tome sr. ½ Hübler × Barbara geb. Malevič [~ VERIF] / Nicolaus Kure ½ Hübler × Maria geb. Tome (★ ženinov priimek = nevestina mati!); zglašnica Podzemelj št. 11 d.d. 21. 11. 1909 + spregled + ustno dovoljenje za ml. nevesto; duhovnik Jos. Pavlič? [~ branje »Jos. Paul« — VERIF]",
    whatEn: "marriage (Nov 22, 1909, entry 13 — MONDAY, the same day as №14!) — the groom Johann TOME [~ Toma — a new surname of 04455], half smallholder's son, 29, GRIBLJE 1 (★ the 3rd marriage evidence of h1 — the 1899-v3 Barbara Kure 27 of h1 × Georg Željko → the 1909 Johann Tome — the house of KURE/ŽELJKO/TOME!; a 10-year gap of h1) × Maria KURE, half smallholder's daughter, 18, GRIBLJE 29 (★ the 3rd marriage evidence of h29 — the 1897-v9 Maria Milek 24 of h29 (the sister Milek house h30!) → the 1909 Maria Kure — the house changes family MILEK→KURE!; the KURE network 20 hits of 04455: h62 + h10 + now h29!); ★ a GRIBLJE × GRIBLJE wedding (h1 × h29 — the 3rd mutual one of the year!); ★★ the DISPENSATION of the 3rd DEGREE touching the 2nd degree (the ordinariate of Ljubljana Nov 9, 1909 no. 4995 — the groom TOME × the bride's mother née TOME: consanguinity AND affinity!); ★ the witnesses = THE SAME SURNAMES AS THE COUPLE (Michael Tome ½ Hübler + Johan Kure ¼ Hübler — both families!); parents: Johann Tome sr. ½ Hübler × Barbara née Malevič [~ VERIF] / Nicolaus Kure ½ Hübler × Maria née Tome (★ the groom's surname = the bride's mother!); the Podzemelj certificate no. 11 of Nov 21, 1909 + the dispensation + the minor bride's oral permit; priest Jos. Pavlič? [~ read »Jos. Paul« — VERIF]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04455",
    year: 1909,
    scan: 141,
    page: 140,
    whatSi: "poroka (22. 11. 1909, vpis 13 — nevesta) — Maria KURE, ½ griblarjeva hči, 18, GRIBLJE 29 (★ 3. poročni dokaz h29 — 1897-v9 Milek → 1909 Kure: hiša zamenja družino!; KURE-mreža h62+h10+h29) × Johann TOME, 29, GRIBLJE 1 (★ 3. poročni dokaz h1 — 1899-v3 Kure×Željko → 1909 Tome; 10 let!); ★★ SPREGLED 3. KOLENA + 2. KOLENO (ordinariat Ljubljana 9/11 1909 št. 4995 — mati geb. TOME = ženinov priimek!); starši: Nicolaus Kure ½ Hübler × Maria geb. Tome / Johann Tome sr. ½ Hübler × Barbara geb. Malevič? [~]; priči Michael Tome + Johan Kure (družinski!); zglašnica št. 11; duhovnik Jos. Pavlič? [~] — ★ GRIBLJE × GRIBLJE h1 × h29!",
    whatEn: "marriage (Nov 22, 1909, entry 13 — the bride) — Maria KURE, half smallholder's daughter, 18, GRIBLJE 29 (★ the 3rd marriage evidence of h29 — the 1897-v9 Milek → the 1909 Kure: the house changes family!; the KURE network h62+h10+h29) × Johann TOME, 29, GRIBLJE 1 (★ the 3rd marriage evidence of h1 — the 1899-v3 Kure×Željko → the 1909 Tome; 10 years!); ★★ the DISPENSATION of the 3rd + the 2nd DEGREE (the ordinariate of Ljubljana Nov 9, 1909 no. 4995 — the mother née TOME = the groom's surname!); parents: Nicolaus Kure ½ Hübler × Maria née Tome / Johann Tome sr. ½ Hübler × Barbara née Malevič? [~]; witnesses Michael Tome + Johan Kure (family!); the certificate no. 11; priest Jos. Pavlič? [~] — ★ a GRIBLJE × GRIBLJE wedding h1 × h29!",
    status: "DOCUMENTED",
  },

  // ——— P139 razširitev: POROČNA KNJIGA 04455 — polno leto 1910 (skeni
  // s141–s145 == Pag. 140–144; letnica V VSAKEM vpisu — brez letne glave
  // [nadaljevanje lekcije P138]; 25. leto poročne linije P115=1886 → P139=1910)
  // — 19 vpisov (№1 s141 + №2–6 s142 + №7–10 s143 + №11–14 s144 + №15–19
  // s145; №-stolpci pasovno potrjeni): ★★★ №1 INTRA-GRIBLJE INTRA-PRIIMEK
  // h13 × h6 (2 × JAKOBČIČ + DISPENSA 3. KOLENA ordinariat 13/1 1910 št. 159
  // [~] + starši-dvojček Mathias Jakobčič ½ × Mathias Jakobčič ¼ + priči =
  // strica obeh mater Pezdirec + Željko!) + ★★★ №14 GRIBLJE × GRIBLJE h86 ×
  // h31 + DVOJNA ZAPREKA (ordinariat št. 2058 [~] + spregled sodišče št. 12448
  // [~]) + h86 NOVA POROČNA HIŠA (67 → 68 — sin h85-družine Marko Križan ×
  // Marija Strauš 1888 na novi hiši!) + ★★★ 24. 1. ×5 = MASA-DAN REKORD
  // linije 1886–1910 + ★★ 12 PON + 7 NED = 100% vikend-poroke (19/19!) +
  // ★★ №17 NEVESTA 16 LET + deželna vlada Ljubljana št. 18796 (1. deželna
  // vlada v liniji!) + ★★ №3+№4 DVOJNA POROKA SOROJENCEV DRAGOŠ isti dan +
  // ★★ №18 69-LETNI ŽENIN LEDIG (2. po 1908-v16 73!) + ★ Jakobčič ×3 ženini
  // + Butala ×3 + Tome ×2 + Bajuk ×2 + trije sorodstveni dokumenti (št. 159
  // [~] + 158 [~] zaporedni isti dan!) + nove oblasti (Škofle pri Brežicah
  // na Štajerskem! + sv. Jernej + Loka + deželna vlada + Vrhovska vas) +
  // novi poklici (Perkušec/perkar! + Schmiedmeister + Einwohner +
  // Hufschmied) + ~25 novih priimkov + DANIJEL 2. pojav (№9 1909 + №9 1910!)
  // — vpisi z Griblji (3 poroke / 5 poročnih blokov: h13 №1 ženin 2. dokaz +
  // h6 №1 nevesta 4. dokaz + h86 №14 ženin NOVA + h31 №14 nevesta 4. dokaz +
  // h8 №17 ženin 3. dokaz). Dokaz: research/issue17/parish-marriage-1910.json;
  // verifikator: scripts/p139_parish_marriage_1910.py --check (I1–I11).
  {
    houseNo: "13",
    bookSignature: "04455",
    year: 1910,
    scan: 141,
    page: 140,
    whatSi: "poroka (23. 1. 1910, vpis 1 — NEDELJA) — ženin Mathias JAKOBČIČ, ½ hüller, 53, ledig, GRIBLJE 13 (2. poročni dokaz h13 — 1885 Janez Jakobič Leinweber 25 [starša Mathias Jakobič × Maria née PEZDIREC — ISTA STARŠA KOT 1910 ŽENIN!] = 25-LETNA KONTINUITETA!; P139-lead №1 VSE POTRJENO) × Marija JAKOBČIČ, ¼ hüllerjeva hči, 32, ledig, GRIBLJE 6 (4. poročni dokaz h6 — 1903 Georg Jakobčič 24 + 1907 Kovač ×2 + krsti 1904/05 Jurij × Katarina Jakobič z botroma ŽELJKO ×2 = nevestina mati Anna geb. Željko — ŽELJKO-veja na h6!); ★★★ INTRA-GRIBLJE INTRA-PRIIMEK POROKA h13 × h6 (obe družini JAKOBČIČ — 1. takšna v 25 letih linije!); ★★ DISPENSA od krvnega sorodstva v 3. kolenu enake stranske vrste (šk. ordinariat Ljubljana 13. 1. 1910 št. 159 [~ — štiri branjа 159/359/138/239; zaporednost z №7-št. 158 isto-dnevna govori za 159]); ★ starši-dvojček: Mathias Jakobčič ½ Hübler (h13!) × Mathias Jakobčič ¼ Hübler (h6!) — DVA Mathiasa Jakobčiča [~ ali sorodnika?]; mati Maria geb. Pezdirec / Anna geb. Željko; ★ priči = strica OBEH mater (Mathias Pezdirec + Joseph Željko ¼ Hübler — STRICEVSKI DVOJČEK!); ženin 53 + nevesta 32 = pozni prvi poroki; zglašnica občine Griblje 22. 1. 1910 št. 1 + dispensa; duhovnik Jos. Rauy P.P.",
    whatEn: "marriage (Jan 23, 1910, entry 1 — SUNDAY) — the groom Mathias JAKOBČIČ, half smallholder, 53, single, GRIBLJE 13 (the 2nd marriage evidence of h13 — the 1885 Janez Jakobič Linenweaver 25 [parents Mathias Jakobič × Maria née PEZDIREC — THE SAME PARENTS AS THE 1910 GROOM!] = a 25-YEAR CONTINUITY!) × Marija JAKOBČIČ, quarter smallholder's daughter, 32, single, GRIBLJE 6 (the 4th marriage evidence of h6 — the 1903 Georg Jakobčič 24 + the 1907 Kovač ×2 + the baptisms 1904/05 Jurij × Katarina Jakobič with the godparents ŽELJKO ×2 = the bride's mother Anna née Željko — the ŽELJKO branch at h6!); ★★★ the INTRA-GRIBLJE INTRA-SURNAME WEDDING h13 × h6 (both families JAKOBČIČ — the 1st such in 25 years of the line!); ★★ the DISPENSATION of consanguinity in the 3rd degree of the equal lateral line (the episcopal ordinariate of Ljubljana Jan 13, 1910 no. 159 [~ — four readings 159/359/138/239; the same-day sequence with №7's no. 158 points to 159]); ★ the parents-twin: Mathias Jakobčič ½ Hübler (h13!) × Mathias Jakobčič ¼ Hübler (h6!) — TWO Mathias Jakobčičes [~ or relatives?]; the mothers Maria née Pezdirec / Anna née Željko; ★ the witnesses = the maternal uncles of BOTH (Mathias Pezdirec + Joseph Željko ¼ Hübler — an UNCULAR TWIN!); the groom 53 + the bride 32 = late first marriages; the Griblje commune certificate Jan 22, 1910 no. 1 + the dispensation; priest Jos. Rauy P.P.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04455",
    year: 1910,
    scan: 141,
    page: 140,
    whatSi: "poroka (23. 1. 1910, vpis 1 — nevesta) — Marija JAKOBČIČ, ¼ hüllerjeva hči, 32, ledig, GRIBLJE 6 (4. poročni dokaz h6 — 1903 Georg Jakobčič + krsti 1904/05 + 1907 Kovač ×2; Željko-botri na h6 = nevestina mati Željko!) × Mathias JAKOBČIČ, ½ hüller, 53, ledig, GRIBLJE 13 (2. dokaz h13 — 1885 brat Janez, ISTA starša!); ★★★ INTRA-GRIBLJE INTRA-PRIIMEK h13 × h6 — obe družini JAKOBČIČ; ★★ DISPENSA 3. KOLENA (ordinariat Ljubljana 13/1 1910 št. 159 [~]); starši: Mathias Jakobčič ¼ Hübler (h6) × Anna geb. Željko / Mathias Jakobčič ½ Hübler (h13) × Maria geb. Pezdirec (STARŠI-DVOJČEK po imenu očeta!); priči Mathias Pezdirec + Joseph Željko ¼ Hübler (strica obeh mater!); zglašnica Griblje št. 1 + dispensa; duhovnik Jos. Rauy — ★ ženin 53 + nevesta 32 = par 85 let!",
    whatEn: "marriage (Jan 23, 1910, entry 1 — the bride) — Marija JAKOBČIČ, quarter smallholder's daughter, 32, single, GRIBLJE 6 (the 4th marriage evidence of h6 — the 1903 Georg Jakobčič + the baptisms 1904/05 + the 1907 Kovač ×2; the Željko godparents at h6 = the bride's mother Željko!) × Mathias JAKOBČIČ, half smallholder, 53, single, GRIBLJE 13 (the 2nd evidence of h13 — the 1885 brother Janez, THE SAME parents!); ★★★ the INTRA-GRIBLJE INTRA-SURNAME h13 × h6 — both families JAKOBČIČ; ★★ the DISPENSATION of the 3rd DEGREE (the ordinariate of Ljubljana Jan 13, 1910 no. 159 [~]); parents: Mathias Jakobčič ¼ Hübler (h6) × Anna née Željko / Mathias Jakobčič ½ Hübler (h13) × Maria née Pezdirec (a PARENTS-TWIN by the father's name!); witnesses Mathias Pezdirec + Joseph Željko ¼ Hübler (the maternal uncles!); the Griblje certificate no. 1 + the dispensation; priest Jos. Rauy — ★ the groom 53 + the bride 32 = an 85-year couple!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "86",
    bookSignature: "04455",
    year: 1910,
    scan: 144,
    page: 143,
    whatSi: "poroka (4. 7. 1910, vpis 14 — PONEDELJEK) — ženin Marcus KRIŽAN [~ branjа Kipžan/Kiprian/Kripian — KRIŽAN po črko-za-črko zoomu + korpus], ¼ griblarjev sin, 24, ledig, GRIBLJE 86 (★★ h86 = NOVA POROČNA HIŠA korpusa — 67. → 68.! GRID-definitivno: 8 = dve zaprti zanki + 6 = ascender z zanko; prejšnja branjа 36/85/17 NAPAČNA — 85 = 1/4-ulomek zamenjan za številko, 36 = korpus-prior!; h86 prvi korpusni dokaz 2 LETI PRED 1912 Brinec-krstom — sin Marka Križana × Marije Strauš h85 [krst Janeza 1888!] = ROD 1886, na novi hiši ~1908? [~ VERIF selitev]) × Catharina STRAUS, ¼ griblarjeva hči, 18, ledig, GRIBLJE 31 (4. poročni dokaz h31 — 1886 Papič × Straus + 1902 + 1906 + krst 1897 Janez Straus × Barbara Jakobič = №14 STARŠA!); ★★ GRIBLJE × GRIBLJE poroka h86 × h31 (2. intra-vasična leta po №1!); ★★ DVOJNA SORODSTVENA ZAPREKA: [dispenza ~ ordinariat?] 24. 5. 1910 št. 2058 + SPREGLED [deželno sodišče?] 25. 6. 1910 št. 12448 [~ tipa listin VERIF] + zglašnica občine Griblje 3. 7. 1910 št. 2; ★★ KRIŽAN × STRAUS DRUŽINSKI DVOJČEK: ženinov oče Marko Križan × mati Marija Strauš (h85 1888!) + nevesta Straus — ženin se poroči z MOSKO DVOJNICO priimka svoje matere!; starši: Marcus [Marko] Križan [~ branje »Mareus«] × Maria geb. [Strauš? ~] / [Johann/Janez? ~] Straus × Barbara geb. [Jakobič? ~] (h31 1897!); priča Mihelič [mesnar?/mesar? ~]; nevesta 18 let — 3. mladoletna nevesta leta (№4 18 + №11 18 + №17 16!); duhovnik Jos. [Rauy ~]",
    whatEn: "marriage (Jul 4, 1910, entry 14 — MONDAY) — the groom Marcus KRIŽAN [~ readings Kipžan/Kiprian/Kripian — KRIŽAN by the letter-by-letter zoom + corpus], quarter smallholder's son, 24, single, GRIBLJE 86 (★★ h86 = A NEW MARRIAGE HOUSE of the corpus — the 67th → 68th! GRID-definitive: 8 = two closed loops + 6 = ascender with a loop; the earlier readings 36/85/17 WRONG — 85 = the 1/4 fraction mistaken for a number, 36 = a corpus-prior!; the first corpus evidence of h86 TWO YEARS BEFORE the 1912 Brinec baptism — the son of Marko Križan × Marija Strauš of h85 [the baptism of Janez 1888!] = born 1886, at the new house ~1908? [~ VERIF the move]) × Catharina STRAUS, quarter smallholder's daughter, 18, single, GRIBLJE 31 (the 4th marriage evidence of h31 — the 1886 Papič × Straus + 1902 + 1906 + the baptism 1897 Janez Straus × Barbara Jakobič = THE 1910 №14 PARENTS!); ★★ a GRIBLJE × GRIBLJE wedding h86 × h31 (the 2nd intra-village of the year after №1!); ★★ a DOUBLE IMPEDIMENT: [a dispensation ~ ordinariate?] May 24, 1910 no. 2058 + the OVERSIGHT [a provincial court?] Jun 25, 1910 no. 12448 [~ the document types VERIF] + the Griblje commune certificate Jul 3, 1910 no. 2; ★★ the KRIŽAN × STRAUS FAMILY TWIN: the groom's father Marko Križan × mother Marija Strauš (h85 1888!) + the bride Straus — the groom marries the FEMALE TWIN of his mother's surname!; parents: Marcus [Marko] Križan [~ the reading »Mareus«] × Maria née [Strauš? ~] / [Johann/Janez? ~] Straus × Barbara née [Jakobič? ~] (h31 1897!); the witness Mihelič [a sexton?/butcher? ~]; the bride 18 — the 3rd minor bride of the year (№4 18 + №11 18 + №17 16!); priest Jos. [Rauy ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1910,
    scan: 144,
    page: 143,
    whatSi: "poroka (4. 7. 1910, vpis 14 — nevesta) — Catharina STRAUS, ¼ griblarjeva hči, 18, ledig, GRIBLJE 31 (4. poročni dokaz h31 — 1886 Martin Papič × Margareth Straus [1. dokaz] + 1902 Maria Mulh? + 1906 Martin Paprič WITWER + krsti 1887–1900 Papič × Straus; 1897 krst Janez Straus × Barbara Jakobič = 2. STRAUS-DRUŽINA na h31 — №14 starša!) × Marcus KRIŽAN, ¼ griblarjev sin, 24, ledig, GRIBLJE 86 (★★ NOVA POROČNA HIŠA 67→68 — sin h85-družine Marko Križan × Marija Strauš!); ★★ GRIBLJE × GRIBLJE h86 × h31 + DVOJNA ZAPREKA (št. 2058 + spregled št. 12448 [~]); starši: [Johann/Janez? ~] Straus ½ [Hübler] × Barbara geb. [Jakobič? ~] (h31 1897!) / Marcus [Marko] Križan × Maria geb. [Strauš? ~] (h85 1888 — MATERIN PRIIMEK = NEVESTIN!); priča Mihelič [~]; zglašnica Griblje 3. 7. 1910 št. 2 + [dva sorodstvena lista ~]; duhovnik Jos. [Rauy ~] — ★ STRAUS-h31 kontinuiteta 1886 → 1910 = 24 let!",
    whatEn: "marriage (Jul 4, 1910, entry 14 — the bride) — Catharina STRAUS, quarter smallholder's daughter, 18, single, GRIBLJE 31 (the 4th marriage evidence of h31 — the 1886 Martin Papič × Margareth Straus [the 1st evidence] + the 1902 Maria Mulh? + the 1906 Martin Paprič WIDOWER + the baptisms 1887–1900 Papič × Straus; the 1897 baptism Janez Straus × Barbara Jakobič = the 2nd STRAUS FAMILY at h31 — the 1910 №14 parents!) × Marcus KRIŽAN, quarter smallholder's son, 24, single, GRIBLJE 86 (★★ A NEW MARRIAGE HOUSE 67→68 — the son of the h85 family Marko Križan × Marija Strauš!); ★★ a GRIBLJE × GRIBLJE h86 × h31 + a DOUBLE IMPEDIMENT (no. 2058 + the oversight no. 12448 [~]); parents: [Johann/Janez? ~] Straus ½ [Hübler] × Barbara née [Jakobič? ~] (h31 1897!) / Marcus [Marko] Križan × Maria née [Strauš? ~] (h85 1888 — THE MOTHER'S SURNAME = THE BRIDE'S!); the witness Mihelič [~]; the Griblje certificate Jul 3, 1910 no. 2 + [two kinship documents ~]; priest Jos. [Rauy ~] — ★ the STRAUS-h31 continuity 1886 → 1910 = 24 years!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04455",
    year: 1910,
    scan: 145,
    page: 144,
    whatSi: "poroka (8. 8. 1910, vpis 17 — PONEDELJEK) — ženin Johann JAKOBČIČ, ¼ griblarjev sin, 20, ledig, GRIBLJE 8 (3. poročni dokaz h8 — 1897 Maria Jakobčič 23 [1. dokaz] + 1900 Catharina Jakobčič 21 [2.]; krstna h8 1886–89 Janez/Anton Jakobič; 1912 krst Janez Jakofčič ¾ × Neza JAKLJEVIČ = NEVESTIN PRIIMEK ŽE na h8-družini!; GRID-definitivno: 8 = dve zaprti zanki — NE 7 [~ prejšnja branjа]!) × Agnes JAKLJEVIČ, ¼ hüllerjeva hči, 16 (!!), ledig, PRILOZJE 30 (★★ NEVESTA 16 LET — 2. najmlajša linije! + DOVOLJENJE CESARSKE KRALJEVSKE DEŽELNE VLADE V LJUBLJANI 1. 8. 1910 št. 18796 = 1. deželna vlada v 04455-liniji! [P138 №14 = deželno SODIŠČE št. 27036]); par 20 + 16 = 36 let skupaj — NAJMLAJŠI PAR linije? [~]; 3. GRIBLJE poroka leta (№1 INTRA + №14 + №17 — največ z 1909!); JAKOBČIČ ×3 ženini leta (№1 h13 + №5 Cerkvišče + №17 h8!); starši: Johann Jakobčič ¼ Hübler (h8!) × Maria geb. [Luh? Lut? ~ VERIF] / Peter Jakljevič ¼ Hübler × Maria geb. [Kralj? Kalj? ~ — KRALJ korpus h17!]; priči Johann [Dragoš? ~] + Nicolaus [Jaklič? ~]; zglašnica [Griblje? ~ branjе »Gorenje«??] 7. 8. 1910 št. 3 + deželna vlada št. 18796 + proglas [Črnomelj 22/2? ~ VERIF] + lastno ustno dovoljenje; duhovnik Jos. Rauy",
    whatEn: "marriage (Aug 8, 1910, entry 17 — MONDAY) — the groom Johann JAKOBČIČ, quarter smallholder's son, 20, single, GRIBLJE 8 (the 3rd marriage evidence of h8 — the 1897 Maria Jakobčič 23 [the 1st evidence] + the 1900 Catharina Jakobčič 21 [the 2nd]; the baptisms of h8 1886–89 Janez/Anton Jakobič; the 1912 baptism Janez Jakofčič ¾ × Neza JAKLJEVIČ = THE BRIDE'S SURNAME ALREADY in the h8 family!; GRID-definitive: 8 = two closed loops — NOT 7 [~ earlier readings]!) × Agnes JAKLJEVIČ, quarter smallholder's daughter, 16 (!!), single, PRILOZJE 30 (★★ THE BRIDE 16 YEARS — the 2nd youngest of the line! + the PERMIT OF THE IMPERIAL ROYAL PROVINCIAL GOVERNMENT OF LJUBLJANA Aug 1, 1910 no. 18796 = the 1st provincial government in the 04455 line! [P138 №14 = a provincial COURT no. 27036]); the couple 20 + 16 = 36 years together — THE YOUNGEST COUPLE of the line? [~]; the 3rd GRIBLJE wedding of the year (№1 INTRA + №14 + №17 — the most with 1909!); the JAKOBČIČ ×3 grooms of the year (№1 h13 + №5 Cerkvišče + №17 h8!); parents: Johann Jakobčič ¼ Hübler (h8!) × Maria née [Luh? Lut? ~ VERIF] / Peter Jakljevič ¼ Hübler × Maria née [Kralj? Kalj? ~ — the KRALJ corpus h17!]; witnesses Johann [Dragoš? ~] + Nicolaus [Jaklič? ~]; the certificate [Griblje? ~ the reading »Gorenje«??] Aug 7, 1910 no. 3 + the provincial government no. 18796 + the banns [Črnomelj Feb 22? ~ VERIF] + the personal oral permit; priest Jos. Rauy",
    status: "DOCUMENTED",
  },

  // ——— P140 razširitev: POROČNA KNJIGA 04455 — polno leto 1911 (skeni
  // s146–s148 == Pag. 145–147; letnica V VSAKEM vpisu — brez letne glave
  // [3. leto lekcije]; 26. leto poročne linije P115=1886 → P140=1911)
  // — 13 vpisov (№1–6 s146 + №7–11 s147 + №12–13 s148; štetje potrjeno s
  // STRIP-tehniko [celi datumski stolpec] + zaporednimi branjí + GRID-№):
  // ★★★ №7 ZGODOVINSKA DUNAJSKA POROKA: Julius BETETTO k.k. Hofopern-Sänger
  // (25, Wien IV/8 Wallergasse 3/11) × Irma-Maria STUKELY (19, Rudolfsheim
  // 132) — 4. 7. 1911 TOR (EDINA nevikend leta: 8 PON + 4 NED + 1 TOR!) +
  // listine pri Standesamt Rudolfsheim + RAUY PER DELEGATIONEM (1. podpis
  // po delegaciji!) + mati Julia SKRBEC (slovenske korenine dunajskega
  // zvezdnika!) + ★★★ ISTA-HIŠA REKORD ×3 (№6 Podzemelj 2 + №8 Vranoviči 3 +
  // №11 Gradac 3 — prejšnji maks 1/leto!) + ★★ INTRA-GRIBLJE ×2 (№1 h31 × h63
  // + №2 h15 × h34 — rekord z 1910) + ★★ №1 REHABILITACIJSKA (Katarina
  // Križan 'samka' h63-1909 → poroka 30. 1. 1911) + №1 dvojno zunanje sidro
  // (krst h31-1887 Janez + EMŠO-1919 'Katarina r. Herian por. 30/1 1911'!) +
  // №8 BUTALA-SESTRI (Anna 1911 = sestra Marije 1910!) + №12 VDOVEC +
  // korpus-sinhronizacija (krst Terezije 1912 Martin Papič × Ana Tomc h33) +
  // №12 'Giriči' = GRIBLJE (genetska-vas 3. pojav) + MASA-DAN 6. 2. ×3 +
  // POSTNA VRZEL 6.2.→15.5. ('15. März' zavrnjeno — sredina posta!) + novi
  // poklici (Hofopern-Sänger! + Zuckermeister + Köppersohn + Knecht +
  // Gemeinde-Beamter + Doltar-kovaška dinastija oče+sin) + ~20 novih
  // priimkov (Betetto, Stukely, Skrbec, Millner, Doltar, Filetič, Malovič,
  // Petrowic, Marovič, Zadravec, Berkopec...) + nove oblasti (Standesamt
  // Rudolfsheim Dunaj! + župni urad Črnomelj št. 316 + ordinariat Ljubljana
  // 7. 11. 1911 [~] + županstvo Gradac) — vpisi z Griblji (4 poroke / 6
  // poročnih blokov: h31 №1 ženin 5. dokaz + h63 №1 nevesta NOVA 68.→69. +
  // h15 №2 ženin + h34 №2 nevesta Kambič-dinastija + h9 №3 ženin 4.
  // Jakobčič-hiša + h33 №12 ženin vdovec). Dokaz:
  // research/issue17/parish-marriage-1911.json; verifikator:
  // scripts/p140_parish_marriage_1911.py --check (I1–I11).
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1911,
    scan: 146,
    page: 145,
    whatSi: "poroka (30. 1. 1911, vpis 1 — PONEDELJEK) — ženin Johann (Janez) PAPIČ, ¼ hübler, 23, ledig, GRIBLJE 31 (5. poročni dokaz h31 — 1886 Martin Papič × Margareth Straus [1.] + 1902 Maria Mulh [2.] + 1906 Paprič-WITWER × Barbara Simec [3.] + 1910 №14 nevesta Straus [4.] → 1911 ŽENIN IZ h31!; ★★ ŽENINOV KRST V KORPUSU: h31-04105 6. 9. 1887 Janez — oče Martin Papič ½ zemlj. × Margaretha Straus = starost 23 ✓ 25-LETNA KONTINUITETA STRAUS-h31!) × Catharina (Katarina) KRIŽAN [~ branjа Hrižan/Škrixan — KRIŽAN po očetu Nikolaju + h63-1909 'Katarina Križan samka' + 1919-EMŠO 'Katarina r. Herian (2.2.1887; por. 30/1 1911)' = TROJNO neodvisno sidro!], ¼ hüblerjeva hči, 23, ledig, GRIBLJE 63 (★★ h63 = NOVA POROČNA HIŠA korpusa — 68. → 69.!; 1. poročni dokaz h63; 04105-h63 1887–1909 krsti — 1909 Jožefa (12. 6.) mati 'Katarina Križan SAMKA ½ zemljaka' = NEVESTA SAMA 19 mesecev prej!); ★★ GRIBLJE × GRIBLJE poroka h31 × h63 (3. leto ZAPORED z intra-poroko: 1910 №1 h13 × h6 + №14 h86 × h31 → 1911 №1!); ★★★ REHABILITACIJSKA POROKA? [~ očetovstvo VERIF]: nevesta je 1909 kot samka vpisala hčer Jožefo — poroči se 30. 1. 1911 z Janezom Papičem; starši ženina: Martin Papič [zemljak/Wagner ~ 'foretnik?' branjе] × Margaretha geb. Straus [~ R-branjе 'Škrixan' — kontradikcija s 1886-Straus; korpus pravi Straus]; starši neveste: Nikolaus Križan ¼ Hübler (h63!) × Catharina geb. [Pečinek? ~]; priči [~ VERIF — branjе 'Joseph Branc?']; zglašnica [Griblje?] od 29. 1. 1911 [št. ~]; duhovnik Jos. Rauy",
    whatEn: "marriage (Jan 30, 1911, entry 1 — MONDAY) — the groom Johann (Janez) PAPIČ, quarter smallholder, 23, single, GRIBLJE 31 (the 5th marriage evidence of h31 — the 1886 Martin Papič × Margareth Straus [1st] + the 1902 Maria Mulh [2nd] + the 1906 Paprič-WIDOWER × Barbara Simec [3rd] + the 1910 №14 bride Straus [4th] → 1911 A GROOM FROM h31!; ★★ THE GROOM'S BAPTISM IN THE CORPUS: h31-04105 Sep 6, 1887 Janez — the father Martin Papiç ½ smallholder × Margaretha Straus = the age 23 ✓ a 25-YEAR STRAUS-h31 CONTINUITY!) × Catharina (Katarina) KRIŽAN [~ readings Hrižan/Škrixan — KRIŽAN by the father Nikolaus + the h63-1909 'Katarina Križan a single mother' + the 1919 personal-ID 'Katarina née Herian (Feb 2, 1887; m. Jan 30, 1911)' = a TRIPLE independent anchor!], quarter smallholder's daughter, 23, single, GRIBLJE 63 (★★ h63 = A NEW MARRIAGE HOUSE of the corpus — the 68th → 69th!; the 1st marriage evidence of h63; the 04105-h63 1887–1909 baptisms — the 1909 Jožefa (Jun 12) by 'Katarina Križan A SINGLE MOTHER ½ smallholder' = THE BRIDE HERSELF 19 months earlier!); ★★ a GRIBLJE × GRIBLJE wedding h31 × h63 (the 3rd consecutive year with an intra-wedding: 1910 №1 h13 × h6 + №14 h86 × h31 → 1911 №1!); ★★★ a REHABILITATION WEDDING? [~ paternity VERIF]: the bride registered a daughter Jožefa as a single mother in 1909 — she marries Janez Papič on Jan 30, 1911; the groom's parents: Martin Papič [a smallholder/Wagner ~ the 'foretnik?' reading] × Margaretha née Straus [~ the R-reading 'Škrixan' — a contradiction with the 1886-Straus; the corpus says Straus]; the bride's parents: Nikolaus Križan ¼ Hübler (h63!) × Catharina née [Pečinek? ~]; the witnesses [~ VERIF — the reading 'Joseph Branc?']; the banns [Griblje?] of Jan 29, 1911 [no. ~]; priest Jos. Rauy",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04455",
    year: 1911,
    scan: 146,
    page: 145,
    whatSi: "poroka (30. 1. 1911, vpis 1 — nevesta) — Catharina KRIŽAN [~ Hrižan/Škrixan branjа; KRIŽAN po očetu + h63-1909-samka + EMŠO-1919 trojno sidro], ¼ hüblerjeva hči, 23, ledig, GRIBLJE 63 (★★ NOVA POROČNA HIŠA korpusa — 68. → 69.! 1. poročni dokaz h63; 04105-h63: 1887/1889/1890/1892/1896/1898/1903/1909 krsti — 8 blokov IZVEN p80-filtra → h63 vstopi v p80 šele s to poroko!; 1909 'Katarina Križan samka' hči Jožefa 12. 6. 1909 = REHABILITACIJSKA poroka 19 mesecev pozneje!) × Johann (Janez) PAPIČ, ¼ hübler, 23, ledig, GRIBLJE 31 (ženinov krst h31-1887 v korpusu!); ★★ GRIBLJE × GRIBLJE h31 × h63; starši neveste: Nikolaus Križan ¼ Hübler (h63) × Catharina geb. [Pečinek? ~]; zglašnica 29. 1. 1911; duhovnik Jos. Rauy — ★ KRIŽAN-ženska mreža: №1 nevesta h63 + 1912 №1 Barbara Križan h63 (sestri? [~ P141 VERIF]) + 1905 Anna Križan h35 + 1910 №14 Marcus Križan h86!",
    whatEn: "marriage (Jan 30, 1911, entry 1 — the bride) — Catharina KRIŽAN [~ the Hrižan/Škrixan readings; KRIŽAN by the father + the h63-1909-single-mother + the 1919 personal-ID triple anchor], quarter smallholder's daughter, 23, single, GRIBLJE 63 (★★ A NEW MARRIAGE HOUSE of the corpus — the 68th → 69th! The 1st marriage evidence of h63; the 04105-h63: the 1887/1889/1890/1892/1896/1898/1903/1909 baptisms — 8 blocks OUTSIDE the p80 filter → h63 enters p80 only through this wedding!; the 1909 'Katarina Križan a single mother' with the daughter Jožefa of Jun 12, 1909 = a REHABILITATION wedding 19 months later!) × Johann (Janez) PAPIČ, quarter smallholder, 23, single, GRIBLJE 31 (the groom's h31-1887 baptism in the corpus!); ★★ a GRIBLJE × GRIBLJE h31 × h63; the bride's parents: Nikolaus Križan ¼ Hübler (h63) × Catharina née [Pečinek? ~]; the banns of Jan 29, 1911; priest Jos. Rauy — ★ the KRIŽAN female network: the 1911 №1 bride h63 + the 1912 №1 Barbara Križan h63 (sisters? [~ P141 VERIF]) + the 1905 Anna Križan h35 + the 1910 №14 Marcus Križan h86!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04455",
    year: 1911,
    scan: 146,
    page: 145,
    whatSi: "poroka (6. 2. 1911, vpis 2 — PONEDELJEK, 1. od masovnega dne 6. 2. ×3!) — ženin Johann JAKLIČ [~ 1. JAKLIČ-ŽENIN v liniji; ali Jaklič/Jakljevič ista družina 1910 №7+№12?], ¼ [Hübler ~], 26, [ledig ~], GRIBLJE 15 [~ hiša 15 ali 16 — VERIF; h15 že v mrliškem vzorcu 1886 + poročni 1887] × Anna KAMBIČ, 30, GRIBLJE 34 (★★ KAMBIČ-DINASTIJA h34: 1905 №13 nevesta Maria Kambič 30 h34 + sestra isto leto → Anna 30 v 1911 = 3. KAMBIČ-NEVESTA iz h34 v 6 letih! [~ sorodstvo VERIF]); ★★ GRIBLJE × GRIBLJE poroka h15 × h34 (2. intra-vasična leta — ob №1 rekord 2 INTRA!); starši [~ vse VERIF — zmedeni branjä]: [Matthias Jaklič Wirth × Maria geb. Simec?] / [Matthias Kambič Wirth × Maria geb. Krinec/Križanec?]; priči [~ VERIF]; zglašnica občine GRIBLJE od 5. 2. 1911 št. 2; duhovnik Jos. Rauy [~]",
    whatEn: "marriage (Feb 6, 1911, entry 2 — MONDAY, the 1st of the mass-day Feb 6 ×3!) — the groom Johann JAKLIČ [~ the 1st JAKLIČ-GROOM of the line; or the Jaklič/Jakljevič the same family as 1910 №7+№12?], quarter [smallholder ~], 26, [single ~], GRIBLJE 15 [~ house 15 or 16 — VERIF; h15 already in the 1886 death sample + the 1887 marriage] × Anna KAMBIČ, 30, GRIBLJE 34 (★★ the KAMBIČ DYNASTY h34: the 1905 №13 bride Maria Kambič 30 h34 + a sister the same year → Anna 30 in 1911 = the 3rd KAMBIČ BRIDE from h34 in 6 years! [~ kinship VERIF]); ★★ a GRIBLJE × GRIBLJE wedding h15 × h34 (the 2nd intra-village of the year — with №1 a record of 2 INTRA!); the parents [~ all VERIF — confused readings]: [Matthias Jaklič a farmer × Maria née Simec?] / [Matthias Kambič a farmer × Maria née Krinec/Križanec?]; the witnesses [~ VERIF]; the Griblje commune certificate of Feb 5, 1911 no. 2; priest Jos. Rauy [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04455",
    year: 1911,
    scan: 146,
    page: 145,
    whatSi: "poroka (6. 2. 1911, vpis 2 — nevesta) — Anna KAMBIČ, 30, GRIBLJE 34 (★★ KAMBIČ-DINASTIJA: 1905 №13 Maria Kambič 30 + sestra isto leto → 1911 Anna 30 = 3. Kambič-nevesta iz h34 v 6 letih! h34 poročni dokazi: 1893 №16 nevesta Catharina Kambič [mati Brinc → dispens №1661!] + 1903 h34 + 1905 ×2 → 1911 = 6. poročni dokaz h34!) × Johann JAKLIČ, 26, GRIBLJE 15; ★★ GRIBLJE × GRIBLJE h15 × h34 (2. intra leta!); zglašnica Griblje 5. 2. 1911 št. 2; duhovnik Jos. Rauy — ★ KAMBIČ-ženske mreže leta: №2 nevesta h34 + №8 mati Barbara Kambič (Butala!) + [№8 mati ženina Kambič? ~] = 3 omembe!",
    whatEn: "marriage (Feb 6, 1911, entry 2 — the bride) — Anna KAMBIČ, 30, GRIBLJE 34 (★★ the KAMBIČ DYNASTY: the 1905 №13 Maria Kambič 30 + a sister the same year → the 1911 Anna 30 = the 3rd Kambič bride from h34 in 6 years! The h34 marriage evidences: the 1893 №16 bride Catharina Kambič [the mother Brinc → the dispensation no. 1661!] + the 1903 h34 + the 1905 ×2 → 1911 = the 6th marriage evidence of h34!) × Johann JAKLIČ, 26, GRIBLJE 15; ★★ a GRIBLJE × GRIBLJE h15 × h34 (the 2nd intra of the year!); the Griblje certificate Feb 5, 1911 no. 2; priest Jos. Rauy — ★ the KAMBIČ female networks of the year: the №2 bride h34 + the №8 mother Barbara Kambič (Butala!) + [the №8 groom's mother Kambič? ~] = 3 mentions!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04455",
    year: 1911,
    scan: 146,
    page: 145,
    whatSi: "poroka (6. 2. 1911, vpis 3 — PONEDELJEK, 2. od masovnega dne 6. 2. ×3!) — ženin Leopold JAKOBČIČ, ¼ hüller, 25 [~ ali 21 — VERIF], ledig, GRIBLJE 9 (h9 poročni dokazi: 1894 + 1903 → 1911 = [3.-4.] dokaz h9; 4. JAKOBČIČ-hiša korpusa po h13/h6/h8 — JAKOBČIČ kontinuiteta 1885 → 1911 = 26 LET!) × Terezija KLEPEC, ½ hüblerjeva hči, 20, ledig, KRASINEC 20 [~ ali 37 — VERIF] (KLEPEC-mreža: 1886 Priložje-Jurij + 1889 Milek×Klejpec h87 + №13-1911 mati Ana Klepec = priimkovna mreža leta!); ★★ JAKOBČIČ-TROJNA MREŽA v enem vpisu: ženin Leopold + priča Michael Jakobčič + nevestina mati Marija geb. JAKOBČIČ!; starši: Georg Jakobčič ½ Hüller (h9?) × Marija geb. [Kurnik? ~ branjе 'Kurnig'] / Peter Klepec ½ Hüller (Krasinec) × Marija geb. Jakobčič; priči: Michael Jakobčič + Mathäus [Motnikov? ~ VERIF]; zglašnica [Griblje?] od 5. 2. 1911 [št. 33? ~] + [potrditev za ženina od Škoflj? ~ — cf. 1910 №2 Škofle pri Brežicah!]; duhovnik Jos. Rauy — ★ KLEPEC ×2 v letu (№3 nevesta + №13 mati ženina)",
    whatEn: "marriage (Feb 6, 1911, entry 3 — MONDAY, the 2nd of the mass-day Feb 6 ×3!) — the groom Leopold JAKOBČIČ, quarter smallholder, 25 [~ or 21 — VERIF], single, GRIBLJE 9 (the h9 marriage evidences: the 1894 + the 1903 → 1911 = the [3rd-4th] evidence of h9; the 4th JAKOBČIČ house of the corpus after h13/h6/h8 — a JAKOBČIČ continuity 1885 → 1911 = 26 YEARS!) × Terezija KLEPEC, half smallholder's daughter, 20, single, KRASINEC 20 [~ or 37 — VERIF] (the KLEPEC network: the 1886 Priložje-Jurij + the 1889 Milek×Klejpec h87 + the 1911 №13 mother Ana Klepec = the surname network of the year!); ★★ a JAKOBČIČ TRIPLE NETWORK in one entry: the groom Leopold + the witness Michael Jakobčič + the bride's mother Marija née JAKOBČIČ!; parents: Georg Jakobčič ½ Hüller (h9?) × Marija née [Kurnik? ~ the 'Kurnig' reading] / Peter Klepec ½ Hüller (Krasinec) × Marija née Jakobčič; the witnesses: Michael Jakobčič + Mathäus [Motnikov? ~ VERIF]; the banns [Griblje?] of Feb 5, 1911 [no. 33? ~] + [a confirmation for the groom from Škoflje? ~ — cf. the 1910 №2 Škofle pri Brežicah!]; priest Jos. Rauy — ★ KLEPEC ×2 in the year (the №3 bride + the №13 groom's mother)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04455",
    year: 1911,
    scan: 148,
    page: 147,
    whatSi: "poroka (5. 11. 1911, vpis 12 — NEDELJA) — ženin Martin PAPIČ, Knecht (hlapec!), ~42 [b. ~1869], WITWER (★★★ VDOVEC — 1. vdovec po 1910-№18!), GRIBLJE 33 (★ 'Giriči 33' branjе = GENETSKA-GRIBLJE lekcija 3. pojav [04105-1911 'Grišice'→Griblje 3]!; h33-DEHLIČ era 1888/1897/1908 poroke → PAPIČ-družina na h33 od ~1909; 4. poročni dokaz h33) × Ana TOMEC, ~23 [b. ~1888], ledig, KRIVOGLAVE 30 [~ branjа Krivoglavice/Hrušovlje — VERIF; 1. vpis vasi Krivoglave v poročni knjigi!]; ★★★ KORPUS-SINHRONIZACIJA: 04105-h33 krst Terezije 5. 10. 1912 — oče Martin Papič ¾ zemljak × mati ANA TOMC = PAR POTRDJEN z neodvisnim krstom 11 mesecev po poroki!; ★★ VDOVČEV PRVI ZAKON: Marija Mlut [~ branjа Milek/Mlut/Mut/Muh — 04105-h33 mati 1909+1911] — hčeri Katarina (3. 6. 1909) + Marija († 9 dni, 23. 5. 1911!) → poroči se 5. 11. 1911, 5+ mesecev po smrti prve žene!; ★ PAPIČ ×2 v letu (№1 Janez h31 + №12 Martin h33 [~ sorodstvo VERIF]); starši [zapis 'Martin Papič foretnik? × Marija Milek' ~ — VERIF ali oče-sin ali prvi-zakon zapis]; nevestini starši: Martin TOMEC × Marija geb. ŽUGELJ (ŽUGELJ ×3 leta!); priči: Peter POŽEK (Požek-mreža 1890+1893!) + Jurij [? ~]; zglašnica [županstva Podzemelj] od 5. 11. 1911 [št. ~]; duhovnik Jos. Rauy — ★ starostna razlika 42 × 23 = 19 let",
    whatEn: "marriage (Nov 5, 1911, entry 12 — SUNDAY) — the groom Martin PAPIČ, a farmhand (Knecht!), ~42 [b. ~1869], A WIDOWER (★★★ the 1st widower after the 2010 №18!), GRIBLJE 33 (★ the 'Giriči 33' reading = the GENETIC-GRIBLJE lesson's 3rd appearance [the 04105-1911 'Grišice'→Griblje 3]!; the h33-DEHLIČ era 1888/1897/1908 weddings → the PAPIČ family at h33 from ~1909; the 4th marriage evidence of h33) × Ana TOMEC, ~23 [b. ~1888], single, KRIVOGLAVE 30 [~ the Krivoglavice/Hrušovlje readings — VERIF; the 1st entry of the Krivoglave village in the marriage book!]; ★★★ a CORPUS SYNCHRONIZATION: the 04105-h33 baptism of Terezija Oct 5, 1912 — the father Martin Papič ¾ smallholder × the mother ANA TOMC = THE COUPLE CONFIRMED by an independent baptism 11 months after the wedding!; ★★ the WIDOWER'S FIRST MARRIAGE: Marija Mlut [~ the Milek/Mlut/Mut/Muh readings — the 04105-h33 mother 1909+1911] — the daughters Katarina (Jun 3, 1909) + Marija († 9 days, May 23, 1911!) → he marries on Nov 5, 1911, 5+ months after his first wife's death!; ★ PAPIČ ×2 in the year (the №1 Janez h31 + the №12 Martin h33 [~ kinship VERIF]); the parents [the entry 'Martin Papič foretnik? × Marija Milek' ~ — VERIF whether a father-son or a first-marriage note]; the bride's parents: Martin TOMEC × Marija née ŽUGELJ (ŽUGELJ ×3 of the year!); the witnesses: Peter POŽEK (the Požek network 1890+1893!) + Jurij [? ~]; the banns [of the Podzemelj commune] of Nov 5, 1911 [no. ~]; priest Jos. Rauy — ★ the age gap 42 × 23 = 19 years",
    status: "DOCUMENTED",
  },
  // ——— P141 razširitev: POROČNA KNJIGA 04455 — polno leto 1912 (skeni
  // s148-dno + s149–s151 == Pag. 147–150; s152 = ŽE 1913 = P142-lead!;
  // letnica V VSAKEM vpisu; 27. leto poročne linije P115=1886 → P141=1912)
  // — 17 vpisov (№1 s148-dno + №2–6 s149 + №7–11 s150 + №12–17 s151;
  // štetje potrjeno s STRIP-tehniko [celi datumski stolpci s148–s151] +
  // s152-1913-mejo!): ★★★ RECIPROČNI DVOJNI PAR SOROJENCEV (№11+№12,
  // 20. 5. 1912: Muc-sorojenca Primostek 10 × Jakljevič-sorojenca
  // Krasinec 13 — KRIŽNO-IZMENJČNE HIŠE = 1. tak primer v celotni liniji
  // 1886–1912!) + ★★★ INTRA-PRIIMEK ×2 V ENEM LETU (№7 PEZDIREC ×
  // PEZDIREC [Mihaelova vs Matijeva linija — zrcalo 1910 №1 Jakobčič!] +
  // №14 ŽUGELJ × ŽUGELJ [Jakobova vs Matijeva] = 3 intra-priimek poroke
  // linije, 2 v samem 1912 = REKORD!) + ★★★ SESTRI KRIŽAN h63 V
  // ZAPOREDNIH JANUARJIH (1911 №1 Katarina Papič + 1912 №1 Barbara Lozar
  // — obe hčereti Nikolaja Križana!; P140-lead 'sestri?' POTRJENO s
  // korpusom) + ★★★ DVOJNA KORPUS-SINHRONIZACIJA №8 (OBA STARŠA-PARA
  // ženina in neveste sta že v poročnem korpusu: 1891 №12 Jakša × Jakša
  // + 1890 №2 Schweiger × Jakša — 1. tak primer!) + ★★ №9 NEVESTA 46 LET
  // (Barbara Straus bajtarica — 2. po 1886-v1 56; par 31+46; h46 =
  // 3. poročni dokaz [1909 №11 INTRA-h46!]) + ★★ №17 KORPUS-SINHRO 1913
  // (sin Julij krst 8. 8. 1913 h31 Griblje Černič × Požek — par + selitev
  // potrjena!) + ★★ №4+№6 JAKOFČIČ DVOJČEK (brat ženin + sestra nevesta —
  // otroka Petra Jakofčiča Čerkvišče 16/17!) + ★★ HRAŠINOVIČ-DVOJČEK
  // (№6 Nikolaj 24 + №16 Nikolaj 49, očeta Anton + Janez + №1 mati geb.
  // Harasinč = 3. pojav!) + ★★ ŠTRAVS-MREŽA ×4 (№9+№10+№15 neveste +
  // priča = 3 Straus-neveste leta = REKORD!) + ★ MASA-DNEVI ×3 (29. 1.
  // №2+№3+№4 + 12. 2. №6+№7 + 20. 5. №11+№12) + ★ NOVE OBLASTI (sodišče
  // Črnomelj №17 1. v liniji! + vojaško oblastno poveljstvo №8 + deželna
  // vlada №5 + Radovica-listine №13 + ordinariat št. 5473 [~]) + ★ №13
  // ALFRED trgovski pomočnik [~] Podzemelj 11 (1. latinsko ime!) + ★
  // KRIVOGLAVCI 3. pojav (1898+1911+1912 №14!) + ★ h78 1. poročni dokaz (№1
  // Lozar — nova v 04455, ŽE v p80 prek 1887-sidra → hiše 69 nespremenjene!) + GENETSKA-VAS
  // 'Girišice' = Griblje 3. pojav (№15) + METODE: ~190 VLM branj v 6
  // krogih + STRIP + GRID-geometrija (REZIDENCA JE PRED IMENOM!) +
  // multi-render pasovi (o/i/d) — 1912 = SLOVENŠČINA + najhitrejša pisava
  // linije! Dokaz: research/issue17/parish-marriage-1912.json;
  // verifikator: scripts/p141_parish_marriage_1912.py --check (I1–I12).
  {
    houseNo: "78",
    bookSignature: "04455",
    year: 1912,
    scan: 148,
    page: 147,
    whatSi: "poroka (16. 1. 1912, vpis 1 — TOREK, izjema!) — ženin Anton LOZAR, [1/2 ~] zemljak, 21, ledig, GRIBLJE 78 (★ h78 = 1. POROČNI DOKAZ — NOVA v poročni knjigi 04455, a ŽE V p80-korpusu prek 04105-1887-sidra [P79/P80-era] → p80 hiše 69 NESPREMENJENE (razlika od h63/h86 P140/P139: njuni 04105-bloki IZVEN p80-filtra!); ★ KORPUS-KRST: rojen 5. 5. 1890 Griblje h38 — oče Miha(el) Lozar ČEVLJAR × Barbara geb. Harasinč [korpus 1890!] → starost 21 ✓; ★ KORPUS-1915: krst hči Jožefe 22. 3. 1915 na h78 ['Anton Ložar ½ × Barbara roj. Križan r. 20/6 1889'] = PAR + NOVA HIŠA POTRJENA!) × Barbara KRIŽAN, [1/4 ~] zemljakova hči, 22, ledig, GRIBLJE 63 (2. poročni dokaz h63; ★ KORPUS-KRST: rojena 20. 6. 1889 h63 — oče Nikolaj Križan ¼ × Katarina geb. Pezdirec → starost 22 ✓); ★★★ SESTRI KRIŽAN h63 V ZAPOREDNIH JANUARJIH: 1911 №1 Katarina (r. 20. 1. 1887, × Janez Papič h31) + 1912 №1 Barbara = obe hčereti Nikolaja Križana × Katarina geb. Pezdirec — P140-lead 'sestri? [~ P141 VERIF]' → POTRJENO S KORPUSOM!; ★ GRIBLJE × GRIBLJE h78 × h63 (2. intra-vasična zapored po 1911 №1!); starši ženina: Mihael Lozar čevljar × Barbara geb. Harasinč; starši neveste: Nikolaj Križan ¼ (h63) × Katarina geb. Pezdirec; zglašnica županstva [Metlika ~] 15/1. 1912 št. [1 ~]; duhovnik [Jos. Rauy ~]",
    whatEn: "marriage (Jan 16, 1912, entry 1 — TUESDAY, an exception!) — the groom Anton LOZAR, [half ~] a smallholder, 21, single, GRIBLJE 78 (★ h78 = the 1st MARRIAGE EVIDENCE — new in the marriage book 04455, but ALREADY IN the p80 corpus through the 04105-1887 anchor [the P79/P80 era] → the p80 houses 69 UNCHANGED (unlike h63/h86 of P140/P139: their 04105 blocks OUTSIDE the p80 filter!); ★ a CORPUS BAPTISM: born May 5, 1890 in Griblje h38 — the father Miha(el) Lozar a COBBLER × Barbara née Harasinč [the 1890 corpus!] → the age 21 ✓; ★ the 1915 CORPUS: the baptism of the daughter Jožefa Mar 22, 1915 at h78 ['Anton Ložar ½ × Barbara née Križan b. Jun 20, 1889'] = THE COUPLE + THE NEW HOUSE CONFIRMED!) × Barbara KRIŽAN, [a quarter ~] a smallholder's daughter, 22, single, GRIBLJE 63 (the 2nd marriage evidence of h63; ★ a CORPUS BAPTISM: born Jun 20, 1889 at h63 — the father Nikolaj Križan ¼ × Katarina née Pezdirec → the age 22 ✓); ★★★ THE KRIŽAN SISTERS OF h63 IN CONSECUTIVE JANUARIES: the 1911 №1 Katarina (b. Jan 20, 1887, × Janez Papič h31) + the 1912 №1 Barbara = both daughters of Nikolaj Križan × Katarina née Pezdirec — the P140-lead 'sisters?' → CONFIRMED BY THE CORPUS!; ★ a GRIBLJE × GRIBLJE wedding h78 × h63 (the 2nd consecutive intra-village after the 1911 №1!); the groom's parents: Mihael Lozar a cobbler × Barbara née Harasinč; the bride's parents: Nikolaj Križan ¼ (h63) × Katarina née Pezdirec; the banns of the [Metlika ~] commune Jan 15, 1912 no. [1 ~]; priest [Jos. Rauy ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04455",
    year: 1912,
    scan: 148,
    page: 147,
    whatSi: "poroka (16. 1. 1912, vpis 1 — nevesta) — Barbara KRIŽAN, [1/4 ~], 22, ledig, GRIBLJE 63 (2. poročni dokaz h63; krst 20. 6. 1889 h63 — starost 22 ✓; ★★★ SESTRI KRIŽAN h63 V ZAPOREDNIH JANUARJIH (1911 №1 Katarina + 1912 №1 Barbara!); ★★ SESTRA 1911-№1 Katarine [ista starša Nikolaj × Katarina geb. Pezdirec] — 2. hčerka h63 v 2 letih poročena!; 04105-h63 1887–1909: 8 krstnih blokov [Katarina 1887 + Barbara 1889 + Marjeta 1890 + Nikolaj 1892 + Ana 1896 + Jožef 1898 + Ana 1903 + Jožefa-samka 1909]) × Anton LOZAR, 21, GRIBLJE 78 (1. poročni dokaz h78 — nova v 04455, ŽE v p80 (1887-sidro!); oče Mihael čevljar × Barbara geb. Harasinč; krst h38 1890); ★ GRIBLJE × GRIBLJE h63 × h78; duhovnik [Jos. Rauy ~] — ★ KRIŽAN-ženska mreža: 1911 №1 Katarina h63 + 1912 №1 Barbara h63 (SESTRI!) + 1905 Anna h35 + 1910 №14 Marcus h86!",
    whatEn: "marriage (Jan 16, 1912, entry 1 — the bride) — Barbara KRIŽAN, [a quarter ~], 22, single, GRIBLJE 63 (the 2nd marriage evidence of h63; the baptism Jun 20, 1889 at h63 — the age 22 ✓; ★★★ THE KRIŽAN SISTERS OF h63 IN CONSECUTIVE JANUARIES (the 1911 №1 Katarina + the 1912 №1 Barbara!); ★★ THE SISTER of the 1911 №1 Katarina [the same parents Nikolaj × Katarina née Pezdirec] — the 2nd daughter of h63 married within 2 years!; the 04105-h63 1887–1909: 8 baptism blocks [Katarina 1887 + Barbara 1889 + Marjeta 1890 + Nikolaj 1892 + Ana 1896 + Jožef 1898 + Ana 1903 + Jožefa-single 1909]) × Anton LOZAR, 21, GRIBLJE 78 (the 1st marriage evidence of h78 — new in 04455, ALREADY in p80 [the 1887 anchor!]; the father Mihael a cobbler × Barbara née Harasinč; the h38 baptism 1890); ★ a GRIBLJE × GRIBLJE h63 × h78; priest [Jos. Rauy ~] — ★ the KRIŽAN female network: the 1911 №1 Katarina h63 + the 1912 №1 Barbara h63 (SISTERS!) + the 1905 Anna h35 + the 1910 №14 Marcus h86!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04455",
    year: 1912,
    scan: 150,
    page: 149,
    whatSi: "poroka (15. 4. 1912, vpis 9 — PONEDELJEK) — nevesta Barbara STRAUS [~ branjа 'Wurba ou Strovs' = Štrovs/STRAUS], bajtarica [~], 46, [ledig/vdova ~ VERIF], GRIBLJE 46 (★ 3. poročni dokaz h46 — 1909 №11 INTRA-h46 Žugelj × Klobučar + krstna 1885–1898; ★★ NAJSTAREJŠA NEVESTA LINIJE PO 1886-v1 (56)! Par 31+46 = 77 let; bajtar/bajtarica obe strani!) × Vincencij [SPUDIČ? ~ 7 variant branj — VERIF], bajtar, 31, ledig, GRADAC 80 (oče [Janez Spudič? drvinar ~]); ★ h46-ŽUGELJ veza (№14 Žugelj-ženin isto leto!) + ŠTRAVS-mreža ×4 leta (№9+№10+№15 neveste + priča Jožef = 3 Straus-neveste 1912 = REKORD!); zglašnica županstva Gradac 15. 4. 1912 št. 25; duhovnik [~]",
    whatEn: "marriage (Apr 15, 1912, entry 9 — MONDAY) — the bride Barbara STRAUS [~ the readings 'Wurba ou Strovs' = Štrovs/STRAUS], a cottager [~], 46, [single/widow ~ VERIF], GRIBLJE 46 (★ the 3rd marriage evidence of h46 — the 1909 №11 the INTRA-h46 Žugelj × Klobučar + the baptisms 1885–1898; ★★ THE OLDEST BRIDE OF THE LINE AFTER THE 1886-v1 (56)! The couple 31+46 = 77 years; a cottager/cottageress on both sides!) × Vincencij [SPUDIČ? ~ 7 reading variants — VERIF], a cottager, 31, single, GRADAC 80 (the father [Janez Spudič? a woodcutter ~]); ★ the h46-ŽUGELJ link (the №14 Žugelj groom the same year!) + the ŠTRAVS network ×4 of the year (the №9+№10+№15 brides + the witness Jožef = 3 Straus brides of 1912 = A RECORD!); the banns of the Gradac commune Apr 15, 1912 no. 25; priest [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04455",
    year: 1912,
    scan: 151,
    page: 150,
    whatSi: "poroka (9. 9. 1912, vpis 15 — PONEDELJEK, STRIP-9.9. NE 29.9.!) — nevesta Marija ŠTRAVS [~Straus], [bajtajeva? ~], 26, ledig, GRIBLJE 44 (~ branjа 'Girišice 44' = GENETSKA-VAS Griblje 3. pojav [1911 №12 'Giriči' + 04105-1911 'Grišice' + 1912 'Girišice']!; 1. poročni dokaz h44) × Marko KRALJ [~ branjа 'Hvalj'/'Žužeklj' — KRALJ po očetu Janezu + korpus], ½ zemljak, 28, ledig, [BOGINJA ~ 14 — korpus-vas 1896 №8 Brodarič 'Boginja vas 15'; branjа 'Griblje vas/Begunja' VERIF]; ★★ mati neveste = Marija geb. PAPIČ [~ 'Gapič' — h31 Papič × Straus 1886 = 25-LETNA STRAUS-PAPIČ VEZA!]; starši neveste: Peter Štravs/Straus bajtar × Marija geb. Papič; starši ženina: Janez Kralj ½ × Marija geb. [Ložek? ~]; priči: Jožef Štravs + Jurij Klepec (KLEPEC ×3 leta: №2+№15-priča+№16!); zglašnica [Podzemelj ~ 23/8. 1912 št. 9 — prekrivanje z №14 VERIF]; duhovnik [~]; ★ KRALJ-mreža leta (№10 mati geb. Kralj + №14 mati geb. Kralj + №15 ženin Kralj!)",
    whatEn: "marriage (Sep 9, 1912, entry 15 — MONDAY, the STRIP-9.9. NOT 29.9.!) — the bride Marija ŠTRAVS [~Straus], [a cottager's? ~], 26, single, GRIBLJE 44 (~ the reading 'Girišice 44' = the GENETIC-VILLAGE Griblje the 3rd appearance [the 1911 №12 'Giriči' + the 04105-1911 'Grišice' + the 1912 'Girišice']!; the 1st marriage evidence of h44) × Marko KRALJ [~ the readings 'Hvalj'/'Žužeklj' — KRALJ by the father Janez + the corpus], a half smallholder, 28, single, [BOGINJA ~ 14 — the corpus village of the 1896 №8 Brodarič 'Boginja vas 15'; the readings 'Griblje vas/Begunja' VERIF]; ★★ the bride's mother = Marija née PAPIČ [~ 'Gapič' — the h31 Papič × Straus 1886 = a 25-YEAR STRAUS-PAPIČ LINK!]; the bride's parents: Peter Štravs/Straus a cottager × Marija née Papič; the groom's parents: Janez Kralj ½ × Marija née [Ložek? ~]; the witnesses: Jožef Štravs + Jurij Klepec (KLEPEC ×3 of the year: №2 + the №15 witness + №16!); the banns [Podzemelj ~ Aug 23, 1912 no. 9 — an overlap with №14 VERIF]; priest [~]; ★ the KRALJ network of the year (the №10 mother née Kralj + the №14 mother née Kralj + the №15 groom Kralj!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04455",
    year: 1912,
    scan: 151,
    page: 150,
    whatSi: "poroka (4. 11. 1912 [~ branjа 24./28.11. — STRIP 4.11. PON ✓], vpis 17 — PONEDELJEK) — nevesta Ana POŽEK [korpus ×3: krst 3. 4. 1890 'Janez Pošek/Požek ½ × Ana Šimec' → starost 22 ✓ + 1913-krst 'Ana Počelf' + 1908 №5 'Catharina Požek GRIBLJE 28'!; POŽEK = MEŽNARJI: 1890 'Miha Požek mežnar iz Adlešič'!], ¼ zemljakova hči, 22, ledig, GRIBLJE 21 (1. poročni dokaz h21 [~ VERIF hiša — branjа 'Griblje 21' 2×]) × Jožef ČERNIČ [korpus-1913: 'Jožef Černič ¼ zemljak' — par POTRJEN!], ¼ zemljak, 23, ledig, [ADLEŠIČI ~ 28 — band-branjе + listina 's Adlešičih 3. 11. 1912 št. 1278'!; alternativno Griblje 21 — VERIF; korpus-1913: par na GRIBLJE h31 = preselitev!]; ★★ KORPUS-SINHRONIZACIJA 1913: sin JULIJ krščen 8. 8. 1913 Griblje h31 ('Jožef Černič ¼ × Ana Počelf [=Požek]') = PAR + PRESELITEV [Adlešič?/Griblje 21 → h31] POTRJENA!; starši ženina: Matija Černič ¼ × Marija geb. Škalič [~ NOV PRIIMEK]; starši neveste: Janez Požek ½ [~ branjа 'Ložar/Barich' — korpus POŽEK!] × Ana geb. Šimec [korpus 1890 ✓]; priči: Janez DRAGOŠ [korpus-družina 1910 №3+№4!] + Janez [Bohle? ~ VERIF — NOV PRIIMEK]; ★ PROGLAS POLNOLETNOSTI za ženina — SODIŠČE ČRNOMELJ 10. 11. 1912 (1. Črnomelj-sodišče v liniji!) + za nevesto [3/11. 1912 ~] + zglašnica občine [Stari Trg ~ 'Stribudje'] št. [124 ~] + list iz Adlešič [št. 1278 ~]; duhovnik [~ 'Jož. Lamut']",
    whatEn: "marriage (Nov 4, 1912 [~ the readings 24./28.11. — the STRIP Nov 4 MON ✓], entry 17 — MONDAY) — the bride Ana POŽEK [the corpus ×3: the baptism Apr 3, 1890 'Janez Pošek/Požek ½ × Ana Šimec' → the age 22 ✓ + the 1913 baptism 'Ana Počelf' + the 1908 №5 'Catharina Požek GRIBLJE 28'!; the POŽEKS = SEXTONS: the 1890 'Miha Požek a sexton from Adlešiči'!], a quarter smallholder's daughter, 22, single, GRIBLJE 21 (the 1st marriage evidence of h21 [~ the house VERIF — the reading 'Griblje 21' twice]) × Jožef ČERNIČ [the 1913 corpus: 'Jožef Černič a quarter smallholder' — THE COUPLE CONFIRMED!], a quarter smallholder, 23, single, [ADLEŠIČI ~ 28 — a band reading + the document 'from Adlešiči Nov 3, 1912 no. 1278'!; alternatively Griblje 21 — VERIF; the 1913 corpus: the couple at GRIBLJE h31 = a move!]; ★★ a CORPUS SYNCHRONIZATION of 1913: the son JULIJ baptized Aug 8, 1913 in Griblje h31 ('Jožef Černič ¼ × Ana Počelf [=Požek]') = THE COUPLE + THE MOVE [Adlešič?/Griblje 21 → h31] CONFIRMED!; the groom's parents: Matija Černič ¼ × Marija née Škalič [~ a NEW SURNAME]; the bride's parents: Janez Požek ½ [~ the readings 'Ložar/Barich' — the corpus POŽEK!] × Ana née Šimec [the 1890 corpus ✓]; the witnesses: Janez DRAGOŠ [the corpus family of the 1910 №3+№4!] + Janez [Bohle? ~ VERIF — a NEW SURNAME]; ★ a MAJORITY DECLARATION for the groom — the ČRNOMELJ COURT Nov 10, 1912 (the 1st Črnomelj court of the line!) + for the bride [Nov 3, 1912 ~] + the banns of the [Stari Trg ~ 'Stribudje'] commune no. [124 ~] + a document from Adlešiči [no. 1278 ~]; priest [~ 'Jož. Lamut']",
    status: "DOCUMENTED",
  },

  // ——— P142 razširitev: POROČNA KNJIGA 04455 — polno leto 1913 (skeni
  // s152–s154 top == Pag. 151–153; s154 y≈780 = rokopisna letna glava
  // »1914« = meja leta DOKAZANA — 1. letna glava po 1908!; 13 vpisov:
  // 1886:7 → … → 1912:17 → 1913:13; letnica 1913 v vsakem vpisu + letni
  // glavi »/1913« s152; 8 PON + 5 NED = 13/13 VIKENDI — 1. popolno
  // vikend-leto po 1907 »12/12 PON«; postna vrzel 27.1.→31.3. — 3. zapored;
  // 0 masa-dnevov = 1. leto brez skupnega dne po 2010!) — vpisi z Griblji
  // (5 porok / 6 blokov: h25 №2 + h53 №3 + h1 №6 + h76+h91 №10 INTRA! +
  // h35 №11 'Gorišice' = genetska-vas 4. pojav!): NOVELE: ★★★ №13 INTRA-
  // KRALJ + 1. DISPENSA 3. KOLENA (ordinariat Ljubljana 31/10.1913 št.
  // 47845 — 4. intra-priimek poroka linije!) + DVOJNI 1911-KORPUS-ANKER
  // (obenem starši = 1911 №6 Georg Kralj × Anna Pezdirec + 1911 №13
  // Matija Kralj × Anna Klepec — sestra hiše Kapljišče 8 ISTA!) + ★★★ №3
  // Marjeta Pezdirec h53 = DVOTERNA korpus-sinhronizacija (krst 14.8.1891
  // h53 + par-krsti 1915/1918 h53 'Dragos × Pezdirc'!) + ★★★ №10 INTRA-
  // GRIBLJE h76 × h91 (5. intra-vasični par!) + VSEBOVANA POROKA (hčer
  // Vilhelmina krščena 9.9.1913 h76 = 7 tednov po poroki!) + h76 = NOVA
  // p80-hiša 69. → 70. + ★★ №11 'Gorišice' = GRIBLJE (genetska-vas 4.:
  // Giriči/Girišice/Gorišice) + Rajmund = 1. ime + ★★ №1 DATUMSKA ANKETA
  // ('24.1.'/'junij 27'/'27.1.' — dokument 25/1 + PON = 27.1.!) + ★★
  // PEZDIREC-MREŽA ×7 oseb + JUVANČIČ ×2 (№1 ženin + №5 nevesta — 2 veji!)
  // + ★ №12 najstarejši par (66+44 = 110 let!) + ★ №9 DRUGO-ŽUPNIJSKI
  // ženin (Petrova vas i. Črnomelj!) + korpus-1918 [~] + ★ NOVE OBLASTI
  // (ordinariat Ljubljana! + podčastništvo Metlika + kr. kotarsko sodišče
  // Bela Krajina št. 2165 + škofni urad Črnomelj št. 239 + župni urad
  // VINICA št. 26 + izpostava Podnanos [~] + [Stari trg pri Ptuju? ~]) +
  // ★ NOVI POKLICI (c.k. poštar! + prostovoljka [~] + kovač-posestnik) +
  // ~16 NOVIH PRIIMKOV (Macel, Vasić, Mihelčič, Jesih, Marovšič [~],
  // Šoflak, Polda, Miklavčič, Štukelj, Vranešič, Mlec, Čeveljak [~],
  // Režek, Simončič, Žitav, Juvančič-poročna-prvojavitev) + 7 mladoletnih
  // oseb (rekord!) + SISTEMSKA H/K/M-INITIAL CONFUSION (Klepec/Hlepec,
  // Kralj/Hvali/Mal, Krasinec/Hrašinec, Macel/Mavrel, Kapljišče/Harpišče)!
  // Dokaz: research/issue17/parish-marriage-1913.json; verifikator:
  // scripts/p142_parish_marriage_1913.py --check (I1–I12).
  {
    houseNo: "25",
    bookSignature: "04455",
    year: 1913,
    scan: 152,
    page: 151,
    whatSi: "poroka (31. 3. 1913, vpis 2 — PONEDELJEK, 1. po postu!) — nevesta Marija KLEPEC [~ branjа Hlepec/Mavrel — K/H zmeda; priimek po očetu!], ¼ zemlj. hči, 23, samska, GRIBLJE 25 (★ KORPUS-HIŠA: h25 Klepec-družina — krst 1896 'Janez Klepec? × Katarina Tome?'; Marija r. ~1890 = starejša hči pred korpusnim krstom!) × Nikolaj VASIĆ [~ branjа Vršič/Javrič/Javornik — priimek po očetu Nikolaju Vasiću!; NOV PRIIMEK], ¼ zemlj. sin, 23, samski, KAPLJIŠČE 4; starši neveste: Jurij Klepec [~ Janez po korpusu] ¼ kmet × Katarina [Čop?/Tome? ~]; starši ženina: Nikolaj Vasić ¼ × Marija [Staričnič?/Starišnik? ~]; priči: Martin Jurjevčič [~] + Ivan Vlasić [~] ¼; ženitovanjska poglašnica župništva Podzemelj 24.3. 1913 št. 14 + občinski list župnega sodišča Črnomelj; duhovnik [Jos. Pavc? ~]",
    whatEn: "marriage (Mar 31, 1913, entry 2 — MONDAY, the 1st after Lent!) — the bride Marija KLEPEC [~ the readings Hlepec/Mavrel — the K/H confusion; the surname after the father!], a quarter smallholder's daughter, 23, single, GRIBLJE 25 (★ a CORPUS HOUSE: the h25 Klepec family — the 1896 baptism 'Janez Klepec? × Katarina Tome?'; Maria b. ~1890 = the elder daughter before the corpus baptism!) × Nikolaj VASIĆ [~ the readings Vršič/Javrič/Javornik — the surname after the father Nikolaj Vasić!; a NEW SURNAME], a quarter smallholder's son, 23, single, KAPLJIŠČE 4; the bride's parents: Jurij Klepec [~ Janez per the corpus] ¼ a farmer × Katarina [Čop?/Tome? ~]; the groom's parents: Nikolaj Vasić ¼ × Marija [Staričnič?/Starišnik? ~]; the witnesses: Martin Jurjevčič [~] + Ivan Vlasić [~] ¼; the wedding banns of the Podzemelj parish Mar 24, 1913 no. 14 + the communal document of the Črnomelj parish court; priest [Jos. Pavc? ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04455",
    year: 1913,
    scan: 152,
    page: 151,
    whatSi: "poroka (21. 4. 1913, vpis 3 — PONEDELJEK) — nevesta Marjeta PEZDIREC, ¼ [gomiljarova ~], 21, samska, GRIBLJE 53 (★★★ DVOTERNA KORPUS-SINHRONIZACIJA: (1) KORPUS-KRST: rojena 14. 8. 1891 h53 — oče Janez Pozdirec ¼ × Marija Križan [korpus!] → starost 21 let 8 mesecev ✓ + ISTA HIŠA 53!; (2) PAR-KRSTI: sin Janez 18. 12. 1915 h53 'Jure Dragos × Marjeta Pezdirc' + sin Nikolaj 9. 8. 1918 h53 = PAR + PRESELITEV NA NEVESTINO HIŠO POTRJENA ×2!) × Jurij DRAGOŠ [~ branjа Ivan/Jure/Janez — korpus 1915 'Jure Dragos' + 1918 'Janez Dragoš? roj. 23.11.[1887]' — starost 25 ✓!], ¼ gomiljar [~], 25, samski, ŽUŽKOVCI 4 [~ branjа 'Vučkoviči']; starši neveste: Janez Pezdirec ¼ [KORPUS-SINHRONO!] × Marija Križan [~ Hrižan — korpus piše oba]; starši ženina: [Janez? ~ Nikolaj?] Dragoš × Katarina [?]; priči: Nikolaj Željko [korpus h1/h60!] + Nikolaj Krivuda ¼ [~]; oglašnica županije Adlešiči 12./22.4. 1913 št. 118 [~ dan dvoven] + vojaški + krstni list; duhovnik [Jožef Ž.? ~]",
    whatEn: "marriage (Apr 21, 1913, entry 3 — MONDAY) — the bride Marjeta PEZDIREC, a quarter [~], 21, single, GRIBLJE 53 (★★★ a DOUBLE-ANCHOR CORPUS SYNCHRONIZATION: (1) a CORPUS BAPTISM: born Aug 14, 1891 at h53 — the father Janez Pozdirec ¼ × Marija Križan [the corpus!] → the age 21 years 8 months ✓ + THE SAME HOUSE 53!; (2) the COUPLE'S BAPTISMS: the son Janez Dec 18, 1915 at h53 'Jure Dragos × Marjeta Pezdirc' + the son Nikolaj Aug 9, 1918 at h53 = THE COUPLE + THE MOVE TO THE BRIDE'S HOUSE CONFIRMED twice!) × Jurij DRAGOŠ [~ the readings Ivan/Jure/Janez — the 1915 corpus 'Jure Dragos' + the 1918 'Janez Dragoš? b. Nov 23 [1887]' — the age 25 ✓!], a quarter [~], 25, single, ŽUŽKOVCI 4 [~ the reading 'Vučkoviči']; the bride's parents: Janez Pezdirec ¼ [CORPUS-SYNCHRONOUS!] × Marija Križan [~ Hrižan — the corpus has both]; the groom's parents: [Janez? ~ Nikolaj?] Dragoš × Katarina [?]; the witnesses: Nikolaj Željko [the corpus h1/h60!] + Nikolaj Krivuda ¼ [~]; the banns of the Adlešiči municipality Apr 12/22, 1913 no. 118 [~ a doubled day] + the military + the baptismal certificate; priest [Jožef Ž.? ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04455",
    year: 1913,
    scan: 152,
    page: 151,
    whatSi: "poroka (26. 5. 1913, vpis 6 — PONEDELJEK) — nevesta Marijeta ŽELJKO, ¼ gospod. hči, 23, samska, GRIBLJE 1 (★★ KORPUS: h1 Željko-družina — oče Nikolaj Željko ¼/½ × Katarina Kure [korpus: krsti 1892 Neža + 1896 Anton h1!]; Marijeta r. ~1890 = prvi otrok pred korpusnima krstoma!; oče 'Nikolaj Željko' 2 R-branjā ✓) × Janez MAROVŠIČ [~★ branjа Marošinič/Marovšinč/Hudavičič/Adamič/Javornik/Krajinec — 8 VARIANT = najtrša beseda leta; VERIF odprto!], ¼ zemljak, 33, samski, KRASINEC 26 [~ branjа 'Krajinec 26']; starši neveste: Nikolaj Željko ¼ [KORPUS!] × [Katarina Kure ~ — korpus h1!]; starši ženina: Matija [Marovšič? ~] ¼ × Katarina geb. ŽUGELJ [korpus-priimek + 1912 №14 intra-Žugelj!]; priči: [imena nejasna] ¼ zemljaka; zemljiška knjiga okrajnega sodišča Črnomelj št. 16 [~] + poglas/prošnja sodišča Črnomelj 5/11. 1912 (dokument 7 mesecev pred poroko!); duhovnik [Jos. Šumi? ~]",
    whatEn: "marriage (May 26, 1913, entry 6 — MONDAY) — the bride Marijeta ŽELJKO, a quarter farmer's daughter, 23, single, GRIBLJE 1 (★★ a CORPUS: the h1 Željko family — the father Nikolaj Željko ¼/½ × Katarina Kure [the corpus: the baptisms 1892 Neža + 1896 Anton at h1!]; Marijeta b. ~1890 = the first child before the corpus baptisms!; the father 'Nikolaj Željko' confirmed by 2 R-readings) × Janez MAROVŠIČ [~★ the readings Marošinič/Marovšinč/Hudavičič/Adamič/Javornik/Krajinec — 8 VARIANTS = the hardest word of the year; VERIF open!], a quarter farmer, 33, single, KRASINEC 26 [~ the reading 'Krajinec 26']; the bride's parents: Nikolaj Željko ¼ [a CORPUS!] × [Katarina Kure ~ — the h1 corpus!]; the groom's parents: Matija [Marovšič? ~] ¼ × Katarina née ŽUGELJ [a corpus surname + the 1912 №14 intra-Žugelj!]; the witnesses: [names unclear] a quarter farmers; the land register of the Črnomelj district court no. 16 [~] + the request of the Črnomelj court Nov 5, 1912 (a document 7 months before the wedding!); priest [Jos. Šumi? ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "76",
    bookSignature: "04455",
    year: 1913,
    scan: 153,
    page: 152,
    whatSi: "poroka (27. 7. 1913 [~ branjа '7.7./9.7.' — zamaknjen '2'; kronologija №9 = 21.7.! + NED], vpis 10 — NEDELJA) — ženin Janko VRANEŠIČ [~ branjа Vranovič/Kranedič — 3 branjā VRANEŠIČ; 'Žugan' = hišno ime? ~], zemljak [~ čolnar?], 20, samski (mladoletnik!), GRIBLJE 76 (★★ h76 = 1. POROČNI DOKAZ — NOVA p80-hiša 69. → 70.! [04105-h76-krst 1913 izven p80-filtra]; ★ KORPUS: hčer Vilhelmina krščena 9. 9. 1913 h76 ['Janez Kramec? ~ Kranec šoždar? × Alojzija Muc[=Mlec ~]'] = VSEBOVANA POROKA — rojena ~7 tednov po poroki!) × nevesta Alojzija MLEC [~ korpus-branjа 'Muc' — ista h91-družina!], ¼ zemlj. hči, 20, samska (mladoletna!), GRIBLJE 91 (★★ KORPUS-KRST: rojena 9. 5. 1893 h91 — oče Janez M[uc→Mlec ~] × Ana Kure [korpus!] → starost 20 ✓!); ★★★ INTRA-GRIBLJE h76 × h91 = 5. intra-vasični par linije (1910 №1 + 1911 №1+№2 + 1912 №1 + 1913 №10!) + obe mladoletni (proglaš polnoletnosti za nevesto — sodišče Črnomelj 26/6. 1913!); starši ženina: [Kafija?/Jožef? ~] Vranešič posestnik × Katarina Urbas [~ Vrbas]; starši neveste: Janez Mlec [korpus ~ 'Muc'] ¼ × Ana Kure [korpus!]; priči: Martin Jurajevič [~ — sorodnik №1-ženina Juvančiča?!] + [Katapina? ~]; škofni urad Črnomelj 19/4. ali 19/7. 1913 št. 239 [~] + zvestilni list žup. urada VINICA 21/4. 1913 št. 26 [drugo-župnijski!] + poročna potrditev kr. kotarskega sodišča v BELI KRAJINI 22/7. 1913 št. 2165 [~]; duhovnik [nejasen podpis]",
    whatEn: "marriage (Jul 27, 1913 [~ the readings '7.7./9.7.' — a swallowed '2'; the chronology of №9 = Jul 21! + SUNDAY], entry 10 — SUNDAY) — the groom Janko VRANEŠIČ [~ the readings Vranovič/Kranedič — 3 readings VRANEŠIČ; 'Žugan' = a house name? ~], a farmer [~ a boatman?], 20, single (a minor!), GRIBLJE 76 (★★ h76 = the 1st MARRIAGE EVIDENCE — a NEW p80 house, the 69th → 70th! [the 04105-h76 baptism of 1913 outside the p80 filter]; ★ a CORPUS: the daughter Vilhelmina baptized Sep 9, 1913 at h76 ['Janez Kramec? ~ Kranec? × Alojzija Muc [=Mlec ~]'] = A SHOTGUN WEDDING — born ~7 weeks after the wedding!) × the bride Alojzija MLEC [~ the corpus reading 'Muc' — the same h91 family!], a quarter farmer's daughter, 20, single (a minor!), GRIBLJE 91 (★★ a CORPUS BAPTISM: born May 9, 1893 at h91 — the father Janez M[uc→Mlec ~] × Ana Kure [the corpus!] → the age 20 ✓!); ★★★ the INTRA-GRIBLJE h76 × h91 = the 5th intra-village couple of the line (the 1910 №1 + the 1911 №1+№2 + the 1912 №1 + the 1913 №10!) + both minors (a majority declaration for the bride — the Črnomelj court Jun 26, 1913!); the groom's parents: [Kafija?/Jožef? ~] Vranešič a farmer × Katarina Urbas [~ Vrbas]; the bride's parents: Janez Mlec [the corpus ~ 'Muc'] ¼ × Ana Kure [the corpus!]; the witnesses: Martin Jurajevič [~ — a relative of the №1 groom Juvančič?!] + [Katapina? ~]; the episcopal office of Črnomelj Apr 19 or Jul 19, 1913 no. 239 [~] + a certificate of the VINICA parish office Apr 21, 1913 no. 26 [another parish!] + the marriage confirmation of the ROYAL DISTRICT COURT OF BELA KRAJINA Jul 22, 1913 no. 2165 [~]; priest [an unclear signature]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04455",
    year: 1913,
    scan: 153,
    page: 152,
    whatSi: "poroka (27. 7. 1913, vpis 10 — NEDELJA) — nevesta Alojzija MLEC [~ korpus-branjа 'Muc' — korpus piše h91-družino kot 'Muc' [~], poročna knjiga 1913 kot 'Mlec' ×3 — ista družina (Janez × Ana Kure h91)!], ¼ zemlj. hči, 20, samska (mladoletna!), GRIBLJE 91 (★★ KORPUS-KRST: rojena 9. 5. 1893 h91 — 'oče Janez Novak?[~] (=Mlec!) × Ana Kure' [korpus 1893!] → starost 20 ✓; 2. poročni dokaz h91 [1. = 1909 №? — korpus-hiša od P119!]) × Janko VRANEŠIČ, zemljak [~ čolnar?], 20, samski (mladoletnik!), GRIBLJE 76 (1. poročni dokaz h76 — NOVA p80-hiša!); ★★★ INTRA-GRIBLJE h91 × h76 = 5. intra-vasični par linije + ★★ VSEBOVANA POROKA: hčer Vilhelmina krščena 9. 9. 1913 h76 = rojena 7 tednov po poroki (nevra sta bila noseča ~2 meseca — obe mladoletni!); ★ KORPUS-1913 [~ VERIF]: krst hčere piše očeta 'Janez Kramec? [~ Kranec] šoždar?' ≠ poročni 'Janko Vranešič' — zmeden podpis istega para?; starši neveste: Janez Mlec [korpus ~ 'Muc'] ¼ zemljak × Ana Kure [korpus!]; starši ženina: [Kafija?/Jožef? ~] Vranešič posestnik × Katarina Urbas [~ Vrbas]; priči: Martin Jurajevič [~] + [Katapina? ~]; listine: škofni urad Črnomelj št. 239 [~] + proglaš polnoletnosti neveste — sodišče Črnomelj 26/6. 1913 + zvestilni list žup. urada Vinica št. 26 [drugo-župnijski!] + potrditev kr. kotarskega sodišča Bela Krajina št. 2165; duhovnik [nejasen podpis]",
    whatEn: "marriage (Jul 27, 1913, entry 10 — SUNDAY) — the bride Alojzija MLEC [~ the corpus reading 'Muc' — the corpus writes the h91 family as 'Muc' [~], the 1913 marriage book as 'Mlec' ×3 — the same family (Janez × Ana Kure of h91)!], a quarter farmer's daughter, 20, single (a minor!), GRIBLJE 91 (★★ a CORPUS BAPTISM: born May 9, 1893 at h91 — 'the father Janez Novak?[~] (=Mlec!) × Ana Kure' [the 1893 corpus!] → the age 20 ✓; the 2nd marriage evidence of h91 [the 1st = a 1909 corpus-house since P119!]) × Janko VRANEŠIČ, a farmer [~ a boatman?], 20, single (a minor!), GRIBLJE 76 (the 1st marriage evidence of h76 — a NEW p80 house!); ★★★ the INTRA-GRIBLJE h91 × h76 = the 5th intra-village couple of the line + ★★ A SHOTGUN WEDDING: the daughter Vilhelmina baptized Sep 9, 1913 at h76 = born 7 weeks after the wedding (the couple ~2 months pregnant — both minors!); ★ the 1913 CORPUS [~ VERIF]: the daughter's baptism writes the father as 'Janez Kramec? [~ Kranec]?' ≠ the marriage 'Janko Vranešič' — a confused signature of the same couple?; the bride's parents: Janez Mlec [the corpus ~ 'Muc'] ¼ a farmer × Ana Kure [the corpus!]; the groom's parents: [Kafija?/Jožef? ~] Vranešič a farmer × Katarina Urbas [~ Vrbas]; the witnesses: Martin Jurajevič [~] + [Katapina? ~]; the documents: the episcopal office of Črnomelj no. 239 [~] + the bride's majority declaration — the Črnomelj court Jun 26, 1913 + a certificate of the Vinica parish office no. 26 [another parish!] + the confirmation of the royal district court of Bela Krajina no. 2165; priest [an unclear signature]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04455",
    year: 1913,
    scan: 153,
    page: 152,
    whatSi: "poroka (24. 8. 1913 [~ VERIF: STRIP 'avgust' vs row 'Sept. 24.' — NED-kader + 4-tedenski ritem po №10 (27.7.) govorita za avgust], vpis 11 — NEDELJA) — ženin Rajmund ČEVELJAK [~ 'Čeh' — 1. ime RAJMUND v liniji (latinsko!); priimek ČEVELJAK 95 % zoom [~ morda poklic 'čeveljar'?!]; NOV PRIIMEK ~], [zemljak? ~], 29, samski [~], GORIŠICE 35 (★★★ 'GORIŠICE' = GENETSKA-VAS za GRIBLJE — 4. pojav! [1910 + 1911 + 1912 'Giriči/Girišice' + 1913 'Gorišice' — korpus-hiša h35!]; 1. poročni dokaz h35 v 20. stoletju [1895 'Giriči' 1. pojav? ~]) × Marijeta REŽEK [~ branjа 'Ržek/Rezek'; NOV PRIIMEK], [?], 39, [samska? ~ VDOVA?! — smrtni list v dokumentih!], KRAJNJI VRH 25 [~ 'Krajni vrh' — vas nad Adlešiči]; ★ par 29+39 = 2. najstarejši par leta + verjetna VDOVA (smrtni list = 1. vdovski dokument 1913 [~ VERIF]); starši ženina: [Anton? ~ 'Antonija Gril, hranopotna oseba'? — skoraj neberljivo! NAJMANJ BERLJIV VPIS LETA] × [Matko Reček? ~ — REŽEK?! morda sorodnica neveste [~]]; starši neveste: [skoraj neberljivi — 'Ana Vrvoda?/Nikolaj Judnič? ~ — ŽUNIČ?!']; priči: [nejasni] ¼ zemljaka; domovnica [~ 'Št. Hrilošof, okraj Lele' — neberljivo!] + krstni, SMRTNI in birmanski list za nevesto + proglaš potrditev kr. kotarskega sodišča Bela Krajina [~ br. 7/65]; duhovnik [~ 'P. Mikeln Polak, Čop.' — delegirani duhovnik?]",
    whatEn: "marriage (Aug 24, 1913 [~ VERIF: the STRIP 'avgust' vs the row 'Sept 24' — the SUNDAY cadence + the 4-week rhythm after №10 (Jul 27) favor August], entry 11 — SUNDAY) — the groom Rajmund ČEVELJAK [~ 'Čeh' — the 1st name RAJMUND of the line (Latin!); the surname ČEVELJAK a 95 % zoom [~ perhaps the occupation 'a cobbler'?!]; a NEW SURNAME ~], [a farmer? ~], 29, single [~], GORIŠICE 35 (★★★ 'GORIŠICE' = a GENETIC NAME for GRIBLJE — the 4th appearance! [1910 + 1911 + 1912 'Giriči/Girišice' + 1913 'Gorišice' — the corpus house h35!]; the 1st marriage evidence of h35 in the 20th century) × Marijeta REŽEK [~ the readings 'Ržek/Rezek'; a NEW SURNAME], [?], 39, [single? ~ a WIDOW?! — a death certificate among the documents!], KRAJNJI VRH 25 [~ 'Krajni vrh' — a village above Adlešiči]; ★ the couple 29+39 = the 2nd oldest of the year + a probable WIDOW (the death certificate = the 1st widow evidence of 1913 [~ VERIF]); the groom's parents: [Anton? ~ 'Antonija Gril, a pauper'? — almost illegible! THE LEAST LEGIBLE ENTRY OF THE YEAR] × [Matko Reček? ~ — REŽEK?! perhaps the bride's relative [~]]; the bride's parents: [almost illegible — 'Ana Vrvoda?/Nikolaj Judnič? ~ — ŽUNIČ?!']; the witnesses: [unclear] a quarter farmers; a residence certificate [~ 'Št. Hrilošof, okraj Lele' — illegible!] + the baptismal, DEATH and confirmation certificates of the bride + a declaration of the royal district court of Bela Krajina [~ no. 7/65]; priest [~ 'P. Mikeln Polak, Čop.' — a delegated priest?]",
    status: "DOCUMENTED",
  },

  // ——— P143 razširitev: POROČNA KNJIGA 04455 — polno leto 1914 (skeni
  // s154-dno + s155 == Pag. 153–154; meja 1914/1915: s155-dno = 2 prazna
  // pasova + diagonala + s156 = letna glava »1915«; 7 vpisov: 1886:7 → … →
  // 1913:13 → 1914:7 — VOJNO LETO: zadnja poroka 7. 7. 1914 (3 tedne pred
  // avstrijsko napovedjo vojne Srbiji 28. 7.!) → 10-mesečna vrzel do 1915
  // №1 (2. 5. 1915) = 1. ZLOM KONTINUITETE LINIJE; 3 PON + 3 NED + 1 TOR =
  // 6/7 vikendov (№7 = 1. torek po 1912 №1!); postna vrzel 22. 2. → 3. 5.
  // (4. zapored)) — vpisi z Griblji (3 INTRA-GRIBLJE poroke = REKORD:
  // №3 h91 × h68 + №4 h68 × h68 ISTA HIŠA (1. tak primer v celi liniji!) +
  // №5 h65 × h31): NOVELE: ★★★ №4+№5 MATI-IN-SIN POROČNA TEDNA (№4 3. 5.:
  // Ivan Mih h68, 71 — NAJSTAREJŠI ŽENIN LINIJE! × Katarina geb. Požek,
  // MILEKOVA VDOVA 48 (vdova Matija Mileka st. h65 — M1903 №3 Milek-poroka
  // (25-letni ženin!) = SIN → kronologija 2 generacij razrešena!) + №5
  // 11. 5. (8 DNI ZA №4!): NJUN SIN Anton Milek 21 × Barbara Straus 19 —
  // mati se poroči, sin 8 dni za njo!) + ★★★ №5 DVOTERNA KORPUS-SINHRONI-
  // ZACIJA (Anton = krst 1893 h65 + Barbara = krst 1894 h71 'Jurij Straus ×
  // Barbara Jakobčič' + SEJEM SELITEV Straus h71 → h31 (6× hiper-zoom!) =
  // 2. 'dvoterna' po 1913 №3!) + ★★★ №4 ISTA-HIŠA h68 × h68 + par 71 × 48 =
  // 119 let (2. rekord!) + ★★ MLAJKOVA-MREŽA ×2 (№3 nevesta Marija
  // Mlakova h68 [hčer Janeza Mlaka 1/8 × Marija geb. Žitav — 2. pojav
  // Žitav po 1913 №12!] + №6 nevesta Marija geb. Jakobčič 'Mlakova vdova'
  // 55 [Dobravice 5] — MLAK = 1. pravi pojav!) + ★★ №7 ROJSTNA DATUMA-novini
  // ('12. VII. 1879' ženin = poroka NA 35. ROJSTNI DAN! + '8. XII. 1885'
  // nevesta — 1. rojstni datumi v blokih linije!) + №7 TOR-izjema (7. 7.
  // [hiper-zoom ×4 '7 z zastavico' vs STRIP '12.7.'!]) + ★ №1 SEGINA-ANKETA
  // (5 variant: Lipovec/Straus/Jegliča/Legina/Segina — S/J/L-INITIAL
  // CONFUSION! + korpus h70/h30 Nikolaj Segina × Marjeta geb. Milek: Ani
  // 1893+1899 — a starost 19 ≠ 21/15 + '(ž.) Adlešiči' → adlešiška veja
  // [~ VERIF] + mladoletna dekle/služabnica [~] na Brodaričevi h46!) + ★
  // №2 HOLBEC ×3 potrjen (branjа Fojek/Votovec = F/H/V-zmeda!) + LEOPOLD
  // 'župni upravitelj' = NOV PODPIS + ★ 3 VDOVSKI vpisi (№2 + №4 + №6 —
  // rekord!) + №6 42 × 55 + ★ NOVE OBLASTI (DEKANIJA METLIKA št. 148 — 1.! +
  // županstvo V GRIBLJAH št. 11 + županstvo Dobravice [~] + škof Ljubljana
  // št. 3 + deželna vlada št. [12648 ~] + župno sodišče Črnomelj št. 69) +
  // NOVI POKLICI (finančni spravnik! + gostilničar + kovač [~]) + ~6 NOVIH
  // PRIIMKOV (Pajzar [~], Holbec [~], Mih [~], Mlak, Cajnar [~], Željko-
  // poročna-prvojavitev) + M-PRIIMKI 5-družinska zmeda (Muc/Milek/Mlak/
  // Mih/Mikc!) + 'HLOŠČA' = KLOSTER 2. pojav! + 'LOKA' = OTOK!
  // Dokaz: research/issue17/parish-marriage-1914.json; verifikator:
  // scripts/p143_parish_marriage_1914.py --check (I1–I12).
  {
    houseNo: "91",
    bookSignature: "04455",
    year: 1914,
    scan: 154,
    page: 153,
    whatSi: "poroka (22. 2. 1914, vpis 3 — NEDELJA, 3 dni pred pepelnično sredo!) — ženin Janez MUC [~ branje 'Mikc' — M-priimek Muc/Milek/Mlak/Mih/Mikc = 5-družinska zmeda leta!], ¼ zemljak, kovač [~ — poklic ali hišno ime?], 47 [~ samski], GRIBLJE 91 (★★ korpus Muc-družina h91: Janez Muc × Ana Kure, otroci 1893–1908 [korpus piše 'Muc', poročna 1913 №10 'Mlec' — ista družina!]; a 47-letni Janez (r. ~1867) = PREDKORPUSNA generacija — čez korpusno okno 1885+!; 2. poročni dokaz h91 po №10-1913) × Marija MLAKOVA [★★ hiper-zoom ×3: M-l-a-k-o-v-a (NE Milekova/Mihova!) + VDOVA: NE — hči Janeza Mlaka; MLAJKOVA-MREŽA ×2 z №6!], 44 [~ branje tudi 47 — 4/7-zmeda], samska, GRIBLJE 68 (★★★ 1. KORPUSNI POJAV hiše 68 — NOVA p80-hiša 70. → 71.! [0 zapisov 1885–1913 — Mlak/Mih-hiša!]; ★★★ INTRA-GRIBLJE h91 × h68 = 1. od REKORDNIH 3 intra-Griblje porok 1914!); starši ženina: Nikolaj Muc ¼ zemlj. × Marija geb. Jakšič [~ — 2. Muc-veja pred korpusom]; starši neveste: Janez Mlak 1/8 [~ 'kmetovali'?] × Marija geb. ŽITAV [★ korpus: Žitav = Zemelj-42 družina (1913 №12 Ana Žitav, oče Franc Žitav bajtar!) — 2. pojav priimka!]; priči: Nikolaj Željko ¼ zemlj. [korpus-priimek!] + Janez Jakšič ¼; zglašnica županstva V GRIBLJAH 21/2. 1914 št. 11 [~ 1/117 — 1. 'županstvo Griblje' po 1903?]; duhovnik [Jos. Punc?/Bauež? ~]",
    whatEn: "marriage (Feb 22, 1914, entry 3 — SUNDAY, 3 days before Ash Wednesday!) — the groom Janez MUC [~ the reading 'Mikc' — the M-surname Muc/Milek/Mlak/Mih/Mikc = a 5-family confusion of the year!], a quarter farmer, a smith [~ an occupation or a house name?], 47 [~ single], GRIBLJE 91 (★★ the corpus Muc family of h91: Janez Muc × Ana Kure, children 1893–1908 [the corpus writes 'Muc', the 1913 marriage book №10 'Mlec' — the same family!]; but the 47-year-old Janez (b. ~1867) = a PRE-CORPUS generation — beyond the corpus window 1885+!; the 2nd marriage evidence of h91 after the 1913 №10) × Marija MLAKOVA [★★ a hyper-zoom ×3: M-l-a-k-o-v-a (NOT Milekova/Mihova!) + WIDOW: NO — the daughter of Janez Mlak; the MLAK NETWORK ×2 with №6!], 44 [~ a reading also 47 — a 4/7 confusion], single, GRIBLJE 68 (★★★ the 1st CORPUS APPEARANCE of the house 68 — a NEW p80 house, the 70th → 71st! [0 records 1885–1913 — the Mlak/Mih house!]; ★★★ the INTRA-GRIBLJE h91 × h68 = the 1st of the RECORD 3 intra-Griblje marriages of 1914!); the groom's parents: Nikolaj Muc ¼ a farmer × Marija née Jakšič [~ — a 2nd Muc branch before the corpus]; the bride's parents: Janez Mlak 1/8 [~] × Marija née ŽITAV [★ the corpus: Žitav = the Zemelj-42 family (the 1913 №12 Ana Žitav, the father Franc Žitav a cottager!) — the 2nd appearance of the surname!]; the witnesses: Nikolaj Željko ¼ a farmer [a corpus surname!] + Janez Jakšič ¼; the banns of the municipality IN GRIBLJE Feb 21, 1914 no. 11 [~ 1/117 — the 1st 'Griblje municipality' after 1903?]; priest [Jos. Punc?/Bauež? ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "68",
    bookSignature: "04455",
    year: 1914,
    scan: 155,
    page: 154,
    whatSi: "poroka (3. 5. 1914, vpis 4 — NEDELJA, 1. po postu!) — ženin Ivan MIH [★★★ potrjen ×3 hiper-zoom 95 % — 'Hafner' IZKLJUČEN (1. napačno branje!); ~ vdovec], ¼ zemljak, 71 (!!), GRIBLJE 68 (★ NAJSTAREJŠI ŽENIN CELE LINIJE 1886–1914 — prej 66 = 1913 №12 Janez Simončič!) × Katarina geb. POŽEK, MILEKOVA VDOVA [★ hiper-zoom ×3: M-i-l-e-k-o-v-a + 'vdova' ×2/3], 48, GRIBLJE 68 (★★★ ISTA-HIŠA poroka h68 × h68 — 1. TAK PRIMER V CELI LINIJI! + ★★★ vdova MATIJE MILEKA ST. s h65 = MATI №5-ŽENINA Antona Mileka (poroki 3. 5. + 11. 5. = 8 DNI NARAZEN — MATI-IN-SIN POROČNA TEDNA!) + ★★ kronologija 2 generacij h65: M1903 №3 'Matthias Milek (25!) × Maria Huestič' = SIN → korpus-otroci h65 1887–1901 (mati Katarina geb. Požek = STAREŠI par) + 1904–1913 (mati Marija geb. Hrišič = SINOV par) → Katarina (r. ~1866) je lahko živa 1914 kot vdova = NEVESTA (48 ✓) [~ VERIF]; par 71 × 48 = 119 let skupaj = 2. rekord linije (za 134 P128 v1!); nevestini starši: Matija Požek ¼ zemljak [~ Fojek — F/P-zmeda] × Marija geb. Pezdirec [PEZDIREC-MREŽA!] = Požek×Pezdirec-rod); starši ženina: Marko Mih [~ Muh] ¼ zemljak × Marija geb. [Horvatini?/Kapušinič? ~]; priči: Janez Primožič [~ Primož] ¼ + Matija [?]; listine: pregled prošnje v 2. kol. [~ dispensa?] — [škof/ordinariat Ljubljana 20/4. 1914 št. 2004 ~] + deželna vlada [Ljubljana] 23/4. 1914 št. [12648/2498 ~]; duhovnik [Jos. Tomc?/Bamp? ~]; ★ isto leto: №3-nevesta Marija Mlakova (hčer Janeza Mlaka!) Z ISTO HIŠE h68 — Mlak-hči poročena 22. 2., Mih-vdovec prevzame hišo 3. 5.!",
    whatEn: "marriage (May 3, 1914, entry 4 — SUNDAY, the 1st after Lent!) — the groom Ivan MIH [★★★ confirmed ×3 hyper-zoom 95 % — 'Hafner' EXCLUDED (a 1st wrong reading!); ~ a widower], a quarter farmer, 71 (!!), GRIBLJE 68 (★ THE OLDEST GROOM OF THE WHOLE LINE 1886–1914 — before: 66 = the 1913 №12 Janez Simončič!) × Katarina née POŽEK, MILEK'S WIDOW [★ a hyper-zoom ×3: M-i-l-e-k-o-v-a + 'widow' ×2/3], 48, GRIBLJE 68 (★★★ a SAME-HOUSE marriage h68 × h68 — THE 1ST SUCH CASE IN THE WHOLE LINE! + ★★★ the widow of MATIJA MILEK SR. of h65 = THE MOTHER OF THE №5 GROOM Anton Milek (the marriages May 3 + May 11 = 8 DAYS APART — A MOTHER-AND-SON WEDDING WEEK!) + ★★ the chronology of the 2 generations of h65: the M1903 №3 'Matthias Milek (25!) × Maria Huestič' = THE SON → the corpus children of h65 1887–1901 (the mother Katarina née Požek = the SENIOR couple) + 1904–1913 (the mother Marija née Hrišič = the son's couple) → Katarina (b. ~1866) can be alive in 1914 as a widow = THE BRIDE (48 ✓) [~ VERIF]; the couple 71 × 48 = 119 years together = the 2nd record of the line (after 134 P128 v1!); the bride's parents: Matija Požek ¼ a farmer [~ Fojek — an F/P confusion] × Marija née Pezdirec [the PEZDIREC NETWORK!] = the Požek×Pezdirec lineage); the groom's parents: Marko Mih [~ Muh] ¼ a farmer × Marija née [Horvatini?/Kapušinič? ~]; the witnesses: Janez Primožič [~ Primož] ¼ + Matija [?]; the documents: a review of the petition in the 2nd column [~ a dispensation?] — [the bishop/ordinariat of Ljubljana Apr 20, 1914 no. 2004 ~] + the provincial government [of Ljubljana] Apr 23, 1914 no. [12648/2498 ~]; priest [Jos. Tomc?/Bamp? ~]; ★ the same year: the №3 bride Marija Mlakova (the daughter of Janez Mlak!) FROM THE SAME HOUSE h68 — the Mlak daughter married Feb 22, the Mih widower takes over the house May 3!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04455",
    year: 1914,
    scan: 155,
    page: 154,
    whatSi: "poroka (11. 5. 1914 [~ branjа tudi '18. 5.' — oba PON!], vpis 5 — PONEDELJEK, 8 dni za materino poroko №4!) — ženin Anton MILEK [★★ KORPUS-KRST: rojen 1893 h65 — 'Matija Milek ½ × Katarina Požek' [korpus!] → starost 21 ✓ ISTA HIŠA!], ½ [~ 'gomljahovšin'? — zemljak-sin formula], 21, samski (mladoletnik!), GRIBLJE 65 (korpus-hiša Milek 1887–1913 — DVE GENERACIJI: stariški par Matija Milek × Katarina geb. Požek (otroci 1887–1901) + sinov par Matija ml. × Marija geb. Hrišič (1904–1913; poroka M1903 №3!); ženinova mati = №4-NEVESTA Katarina geb. Požek — porokа 8 dni prej!) × Barbara STRAUS [★★ KORPUS-KRST: rojena 1894 h71 — 'Jurij Straus ¼ × Barbara Jakobčič' [korpus!] → starost 19 ✓], ¼, 19, samska (mladoletna — proglaš!), GRIBLJE 31 [★ hiper-zoom ×6: hiša 31 (NE 71!) — korpus-krst na h71 = SEJEM SELITEV Strausovih h71 → h31 [h31 = Papič/Križan-Jakobičeva hiša 1911 №1!]]; ★★★ INTRA-GRIBLJE h65 × h31 (3. intra v letu — REKORD!) + ★★★ DVOTERNA KORPUS-SINHRONIZACIJA (OBE strani krščeni v korpusu — 2. 'dvoterna' po 1913 №3!); starši ženina: Matija Milek [pokojni?] ½ × Katarina geb. Požek [★ = №4-nevesta! ~ branje 'Gojek' — G/P-zmeda]; starši neveste: Jurij Straus ¼ zemljak [korpus ✓] × Barbara geb. Jakobčič [korpus ✓ — JAKOBČIČ-mreža + №6-nevesta roj. Jakobčičeva!]; priči: Matija Hrižan [~ Hričan] + Janez Jakša [~ Žakšič — 3. Jakša-pojav leta!]; zglašnica županstva V DOBRAVICAH [~ 'o Deželah'!] 10/5. 1914 št. 3 + proglaš polnoletnosti [za nevesto? ~] — sodišče Črnomelj; duhovnik [Jos. Pavl?/Povl ~]",
    whatEn: "marriage (May 11, 1914 [~ a reading also 'May 18' — both MONDAYS!], entry 5 — MONDAY, 8 days after his mother's marriage №4!) — the groom Anton MILEK [★★ a CORPUS BAPTISM: born 1893 at h65 — 'Matija Milek ½ × Katarina Požek' [the corpus!] → the age 21 ✓ THE SAME HOUSE!], a half [~], 21, single (a minor!), GRIBLJE 65 (the corpus house of the Mileks 1887–1913 — TWO GENERATIONS: the senior couple Matija Milek × Katarina née Požek (children 1887–1901) + the son's couple Matija jr. × Marija née Hrišič (1904–1913; the marriage M1903 №3!); the groom's mother = THE №4 BRIDE Katarina née Požek — her marriage 8 days earlier!) × Barbara STRAUS [★★ a CORPUS BAPTISM: born 1894 at h71 — 'Jurij Straus ¼ × Barbara Jakobčič' [the corpus!] → the age 19 ✓], a quarter, 19, single (a minor — a majority declaration!), GRIBLJE 31 [★ a hyper-zoom ×6: the house 31 (NOT 71!) — the corpus baptism at h71 = THE STRAUS MOVE h71 → h31 [h31 = the Papič/Križan-Jakobič house of the 1911 №1!]]; ★★★ the INTRA-GRIBLJE h65 × h31 (the 3rd intra of the year — A RECORD!) + ★★★ a DOUBLE CORPUS SYNCHRONIZATION (BOTH sides baptized in the corpus — the 2nd 'double' after the 1913 №3!); the groom's parents: Matija Milek [the late?] ½ × Katarina née Požek [★ = the №4 bride! ~ the reading 'Gojek' — a G/P confusion]; the bride's parents: Jurij Straus ¼ a farmer [the corpus ✓] × Barbara née Jakobčič [the corpus ✓ — the JAKOBČIČ network + the №6 bride born a Jakobčič!]; the witnesses: Matija Hrižan [~ Hričan] + Janez Jakša [~ Žakšič — the 3rd Jakša appearance of the year!]; the banns of the municipality IN DOBRAVICE [~] May 10, 1914 no. 3 + a majority declaration [for the bride? ~] — the Črnomelj court; priest [Jos. Pavl?/Povl ~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1914,
    scan: 155,
    page: 154,
    whatSi: "poroka (11. 5. 1914, vpis 5 — PONEDELJEK) — nevesta Barbara STRAUS [★★ KORPUS-KRST: rojena 1894 h71 — 'Jurij Straus ¼ × Barbara Jakobčič' [korpus!] → starost 19 ✓; STRAUS-mreža: 3 Straus-neveste 1912 + Barbara bajtarica h46 1912 №9!], ¼, 19, samska (mladoletna!), GRIBLJE 31 (★★ hiper-zoom ×6: hiša 31 (NE 71!) — korpus-krst 1894 na h71 = SEJEM SELITEV Strausovih h71 → h31 (1911 №1 Papič h31!) [~]; 1. poročni dokaz h31 v 20. stoletju [1892 №4 'Jakobčičeva h13/h31'? — VERIF]; sestra Marija roj. 1890 h71 [korpus]!) × Anton MILEK (21 — korpus-krst 1893 h65!; MATI = №4-nevesta Katarina geb. Požek — porokа 8 dni prej!), ½, 21, samski (mladoletnik!), GRIBLJE 65; ★★★ INTRA-GRIBLJE h31 × h65 (3. intra-Griblje poroka leta = REKORD LINIJE [1910 №1 + 1911 №1+№2 + 1912 №1 + 1913 №10 + 1914 №3+№4+№5!]) + DVOTERNA KORPUS-SINHRONIZACIJA; starši neveste: Jurij Straus ¼ zemljak [korpus ✓] × Barbara geb. Jakobčič [korpus ✓]; starši ženina: Matija Milek ½ [pokojni?] × Katarina geb. Požek [№4-nevesta!]; priči: Matija Hrižan + Janez Jakša [~]; zglašnica županstva v Dobravicah 10/5. 1914 št. 3 + proglaš polnoletnosti — sodišče Črnomelj [~]; duhovnik [Jos. Pavl? ~]",
    whatEn: "marriage (May 11, 1914, entry 5 — MONDAY) — the bride Barbara STRAUS [★★ a CORPUS BAPTISM: born 1894 at h71 — 'Jurij Straus ¼ × Barbara Jakobčič' [the corpus!] → the age 19 ✓; the STRAUS network: 3 Straus brides of 1912 + Barbara a cottager of h46 in the 1912 №9!], a quarter, 19, single (a minor!), GRIBLJE 31 (★★ a hyper-zoom ×6: the house 31 (NOT 71!) — the corpus baptism of 1894 at h71 = THE STRAUS MOVE h71 → h31 (the 1911 №1 Papič of h31!) [~]; the 1st marriage evidence of h31 in the 20th century [the 1892 №4 'a Jakobčič of h13/h31'? — VERIF]; the sister Marija born 1890 at h71 [the corpus]!) × Anton MILEK (21 — the corpus baptism of 1893 at h65!; his MOTHER = the №4 bride Katarina née Požek — her marriage 8 days earlier!), a half, 21, single (a minor!), GRIBLJE 65; ★★★ the INTRA-GRIBLJE h31 × h65 (the 3rd intra-Griblje marriage of the year = THE LINE RECORD [the 1910 №1 + the 1911 №1+№2 + the 1912 №1 + the 1913 №10 + the 1914 №3+№4+№5!]) + a DOUBLE CORPUS SYNCHRONIZATION; the bride's parents: Jurij Straus ¼ a farmer [the corpus ✓] × Barbara née Jakobčič [the corpus ✓]; the groom's parents: Matija Milek ½ [the late?] × Katarina née Požek [the №4 bride!]; the witnesses: Matija Hrižan + Janez Jakša [~]; the banns of the Dobravice municipality May 10, 1914 no. 3 + a majority declaration — the Črnomelj court [~]; priest [Jos. Pavl? ~]",
    status: "DOCUMENTED",
  },

  // ——— P144 razširitev: POROČNA KNJIGA 04455 — polno leto 1915 (skeni
  // s156 + s157 == Pag. 155–156; meja 1915/1916: s157-dno = PRAZEN pas +
  // diagonala + s158 = letna glava »1916« (№1 27.1.1916 — štetje ponovno
  // od №1!); 6 vpisov: 1886:7 → … → 1913:13 → 1914:7 → 1915:6 — VOJNO
  // LETO = najšibkejše leto linije (prej 1886: 7!); 4 NED + 1 PON + 1 TOR
  // (№4 21.9. = 3. torek po 1912 №1 + 1914 №7 — VOJAŠKI termini!) — vpisi z
  // Griblji (1 poroka = najmanj od P115!: №1 ISTA-HIŠA h82 × h82!):
  // NOVELE: ★★★ №3 PRVA ROMSKA POROKA LINIJE 1886–1915 (Katarina
  // HUDOROVIČ 'samostna ciganka' Dobravice 48 + priči 'oba cigana' (Fran +
  // Mate Hudorovič!) + mati Ana roj. Hudorovič ciganka = ENDOGAMNA romska
  // družina! + korpus-potrditvi B1917 h5 Mara Hudorovac CIGANKA
  // [nezakonska!] + B1919 h47 Barbara n. Hudorovac = 3 romske ženske
  // Griblij 1915–1919!) + ★★★ №1 DVOTERNA KORPUS-SINHRONIZACIJA VREBEC-MUC
  // (korpus-krst neveste B1887 h52: 'Terezija, očeta stolpec PRAZEN —
  // nezakonska, mati Marija Muc bajtkr. žena' = EXACT MATCH z vpisom [oče
  // PRAZEN + mati Marija Muc bajtarica + r. 12.10.1887 → 27 ✓!] + PAR-KRSTI
  // na poročni hiši: B1916 Ana + B1919 Peter, oba h82 — 'Peter Vrebec
  // tesarski mojster × Terezija roj. Muc, 12.10.1887' [korpus!] = poročni
  // par POTRJEN ×2!) + ★★★ 3 VOJAKI NA DOPUSTU = REKORD LINIJE (№3 Jakob
  // Hošec Dobravice 48 [soglasje glavarstva Črnomelj + ordinariat Ljubljana
  // + c.k. VOJNI SUPERIORAT GRAZ — 3 oblasti!] + №4 Jožef Kostelec Drašiči
  // 65 [Verkündmachtigungsschein k.k. Feldsuperiorata Graz št. 4804 — nem.
  // vojaška listina!] + №6 Janez Curnar Gradac 95 [zglašnica iz KRANJSKE
  // GORE!]) + ★★ №1+№3 DVE ISTA-HIŠA poroki v enem letu (h82 × h82 Griblje
  // + h48 × h48 Dobravice — po 1. primeru 1914 №4 h68 kar 2 novi = 3 v
  // liniji!) + ★★ №2 STARŠA-OBE-STRANI V KORPUSU (ženinovi Krasinec-35
  // Brodarič-veja [M1906 №2+№3 RECIPROČNI par Brodarič 35 ↔ Županič 18 +
  // M1909 №2 Nikolaj Brodarič × Marija Kambič = verjetno №2-oče!] +
  // nevestini M1893 №3 Peter Segina × Barbara Kambič [ISTI PAR!] — 'Rambič'
  // = Kambič!) + ★★ №6 KRANJSKA GORA — najbolj oddaljena oblast linije
  // (železniški delavec z Gorenjske na Belokranjski progi + priči žel.
  // usluž. = kolegi!) + ★ NOVE OBLASTI (Feldsuperiorat Graz ×2 — 1. vojaška
  // oblast linije! + županstvo TRIBUČE [1.!] + žup. urad ADLEŠIČI + sodišče
  // Metlika [1.!] + županstvo Kranjska Gora + deželna vlada št. 12236 +
  // ordinariat Ljubljana) + ★ NOVI POKLICI (železniški delavec — 1.! +
  // tesar → tesarski mojster [1916!] + sluškinja + samostna ciganka —
  // unikat!) + ROJSTNI DATUMI V VSEH 6 VPISIH (1914-novina postane PRAVILO
  // — vse starosti aritmetično ✓!) + ~10 NOVIH PRIIMKOV (Vrebec ·
  // Ritmanič · Globič · Hošec · Cinca · Hudorovič · Kostelec · Maverin [~
  // Martin?] · Curnar · Robič · Jurešič [~] · Pleš [~]) + WWI-PROFIL: 1.
  // leto BREZ postne vrzeli po 4-letni seriji 1911–1914 (vojna: letnica se
  // začne 2.5. = 4 tedne po veliki noči!) + vrzel №1→№2 (2.5.→22.8.) = 3,5
  // meseca (fronta!)
  // Dokaz: research/issue17/parish-marriage-1915.json; verifikator:
  // scripts/p144_parish_marriage_1915.py --check (I1–I12).
  {
    houseNo: "82",
    bookSignature: "04455",
    year: 1915,
    scan: 156,
    page: 155,
    whatSi: "poroka (2. 5. 1915, vpis 1 — NEDELJA, 1. poroka po 10-mesečni WWI-vrzeli [zadnja predvojna 7. 7. 1914!] + 1. po veliki noči 4. 4. 1915) — ženin Peter VREBEC [~ branjа Vrabe/Vreber — V/B-zmeda; korpus-1916: 'Vrebec', 1919: 'Vreber'], tesar, 32 [~ 33 — r. 16. VII. 1882 [~ V — VERIF], ženin, GRIBLJE 82 (★ 1. poročni dokaz h82 — NOVA p80-hiša 71. → 72.! [04105-h82-krsti 1916/1919 IZVEN p80-filtra!]; PAR-KRSTI: B1916 Ana + B1919 Peter, oba h82 — 'Peter Vrebec tesarski mojster × Terezija roj. Muc, 12.10.1887' [korpus!] = razvoj poklica tesar → TESARSKI MOJSTER 1916!) × Terezija MUC [~ korpus Muc-mreža h91 (Janez Muc × Ana Kure 1893–1908) — veja?], bajtarska hči, 27 (r. 12. X. 1887 — 27 ✓ aritmetika), devica, GRIBLJE 82 (★★★ ISTA-HIŠA h82 × h82 — 2. tak primer linije po 1914 №4 h68 × h68! + ★★★ NEVESTA NEZAKONSKA hči: oče PRAZEN v vpisu + korpus-krst B1887 Griblje h52 'Terezija, očeta stolpec PRAZEN — nezakonska, mati Marija Muc bajtkr. žena' = EXACT MATCH → DVOTERNA KORPUS-SINHRONIZACIJA [edini dvojni dokaz tega vzorca v korpusu!] + PAR-KRSTI 1916/1919 na poročni hiši h82 = zakonska pot potrjena ×2!); starši ženina: Peter Vrebec bajtar (ISTO IME — oče in sin Peter!) × Katarina geb. Ritmanič [~ NOV priimek — korpus 0]; starši neveste: oče — (PRAZNO — NEZAKONSKA!) × Marija Muc bajtarica [korpus B1887 ✓]; priči: Muc Janez [~ poklic neberljiv 'polzumljaka' — VERIF; Muc-mreža?] + Globič Jure [~ NOV priimek — korpus 0] (oba kat.); listine: zglašnica županstva TRIBUČE [~ 'Stribuče' — 1. pojav oblasti!] 30. 4. 1915 št. 144 [~ 147 — VERIF] + sprječevalo samskega stanu ŽENINA od žup. urada ADLEŠIČI 15. 4. 1915 (★ drugo-župnijski izvor — Vrebec registriran v Adlešičih!; 2. adlešiška oblast po 1912 №17!) + krstni list (sicut sub 2) + birmovalni list ženina; duhovnik P. Valerian Mikčak [~ Miklavžič/Miklavič — VERIF; 'Valerijan' = 1. v liniji — podpis na vseh 6 vpisih 1915!]; ★ INTRA-GRIBLJE ISTA-HIŠA (1. v letu — edini Griblje-vpis leta: VOJNO LETO — 6 porok = najšibkejše leto linije!)",
    whatEn: "marriage (May 2, 1915, entry 1 — SUNDAY, the 1st marriage after the 10-month WWI gap [the last pre-war one Jul 7, 1914!] + the 1st after Easter Apr 4, 1915) — the groom Peter VREBEC [~ the readings Vrabe/Vreber — a V/B confusion; the 1916 corpus: 'Vrebec', 1919: 'Vreber'], a carpenter, 32 [~ 33 — b. Jul 16, 1882 [~ May — VERIF], single, GRIBLJE 82 (★ the 1st marriage evidence of h82 — a NEW p80 house, the 71st → 72nd! [the 04105-h82 baptisms 1916/1919 outside the p80 filter!]; the COUPLE'S BAPTISMS: B1916 Ana + B1919 Peter, both h82 — 'Peter Vrebec a master carpenter × Terezija née Muc, Oct 12, 1887' [the corpus!] = the career carpenter → MASTER CARPENTER 1916!) × Terezija MUC [~ the corpus Muc network of h91 (Janez Muc × Ana Kure 1893–1908) — a branch?], a cottager's daughter, 27 (b. Oct 12, 1887 — 27 ✓ arithmetic), single, GRIBLJE 82 (★★★ a SAME-HOUSE marriage h82 × h82 — the 2nd such case of the line after the 1914 №4 h68 × h68! + ★★★ AN ILLEGITIMATE BRIDE: the father EMPTY in the entry + the corpus baptism B1887 Griblje h52 'Terezija, the father's column EMPTY — illegitimate, the mother Marija Muc a cottager's wife' = an EXACT MATCH → a DOUBLE-ANCHOR CORPUS SYNCHRONIZATION [the only double proof of this pattern in the corpus!] + the couple's baptisms 1916/1919 at the marriage house h82 = the marriage confirmed twice!); the groom's parents: Peter Vrebec a cottager (the SAME NAME — father and son Peter!) × Katarina née Ritmanič [~ a NEW surname — 0 in the corpus]; the bride's parents: father — (EMPTY — ILLEGITIMATE!) × Marija Muc a cottager [the corpus B1887 ✓]; the witnesses: Muc Janez [~ an unreadable occupation 'polzumljaka' — VERIF; the Muc network?] + Globič Jure [~ a NEW surname — 0 in the corpus] (both Catholic); the documents: the banns of the TRIBUČE municipality [~ 'Stribuče' — the 1st appearance of this authority!] Apr 30, 1915 no. 144 [~ 147 — VERIF] + the groom's single-status certificate from the ADLEŠIČI parish office Apr 15, 1915 (★ an another-parish origin — the Vrebecs registered in Adlešiči!; the 2nd Adlešiči authority after the 1912 №17!) + a baptismal certificate (sicut sub 2) + the groom's confirmation certificate; priest P. Valerian Mikčak [~ Miklavžič/Miklavič — VERIF; 'Valerijan' = the 1st of the line — the signature on all 6 entries of 1915!]; ★ an INTRA-GRIBLJE SAME-HOUSE marriage (the only Griblje entry of the year: THE WAR YEAR — 6 marriages = the weakest year of the line!)",
    status: "DOCUMENTED",
  },

  // ——— P149 razširitev: POROČNA KNJIGA 04455 — polno leto 1920 (skeni
  // s175/s176 (DUPLIKAT! obe = Pag. 174) – s182 == Pag. 174–180; meja
  // 1919/1920 = veliki cifri »1 9« (L) / »2 0« (R) na s175 — 8. marker-dokaz,
  // zdaj RAZPOREJEN po razporedu!); 37 vpisov (36 oštevilčenih №1–36 + 1
  // NEŠTEVILČEN Vode-Ljubljana 15.8.!) = 2. NAJVEČJE LETO LINIJE (1919:40 →
  // 1920:37 — povojni boom se nadaljuje!); 24 PON (64,9% — padec od 82,5%!)
  // + 10 NED (rekord povojnega obdobja!) + 2 PETKA (№21/№22 — edini!) + 1
  // TOR (№11); vpisi z Griblji (4 poroke!): №10 h46×h41 INTRA · №27 h18 ·
  // №28 h21 · №34 h6×h36 INTRA = 6 Griblje-številk; NOVELE: ★★★ 2. VPIS
  // BREZ ŠTEVILKE (Vode-Štefanc 15.8. 'v LJUBLJANI' — učiteljski par! Mar.
  // Ormay! Zagreb-listina!) + ★★★ MATRICULA-DUPLIKAT s175=s176 (invarianta
  // Pag==sken−1 LOMLJENA — s177+ == sken−2!) + ★★★ SIBLING-SWAP №2+№3
  // (Škala × Berkoper obojestransko, ISTI starši + ISTI priči!) + ★★ MRLŠKI
  // LIST prilepljen (Anton Novak? hišar Gradac 59 † 2.10.1920 — izdal ISTI
  // župnik!) + ★★ DISPENS-SLIP 1918 (Trebnje-par!) + ★★ 4 FAMILIJSKI
  // DVOJNI POROČNI DANI (Dragos brat+sestra 26.1. · Oberman brata 9.2. ·
  // Perdivec sestra+brat 14.5. · Štipanič sestri 11.4.+7.11.) + ★ INTRA-HIŠE
  // ×3 (№25 Krasinec 34×34 stari par 53×44! · №33 Dobravice 9×9 levirat? ·
  // №21/№22 Otok 1) + INTRA-PRIIMKI ×3 + IZVEN REDA ×2 + 16-letna nevesta
  // (NAJMLAJŠA!) + 17-letni ženin (NAJMLAJŠI!) + KRIŽAN ×5 vpisov + 4 VDOVE
  // + 1 vdovec + 5 samokorekcij + anotacija 1936 + 4 duhovniki (Cerar ~25×
  // + kaplan Lopar ×6 + Vajgar + Ormay-Ljubljana!)
  // Dokaz: research/issue17/parish-marriage-1920.json; verifikator:
  // scripts/p149_parish_marriage_1920.py --check (I1–I12).
  {
    houseNo: "46",
    bookSignature: "04455",
    year: 1920,
    scan: 177,
    page: 175,
    whatSi: "poroka (2. 2. 1920, vpis 10 — PONEDELJEK) — ženin Matija BRODARIČ [K/R — ne 'Brodavič'!], kmet. povest. sin, 21 [r. 26. I. 1899 ✓], rim. kat., GRIBLJE 46 (★ NOVA Griblje-hiša — 1. poročni dokaz h46!) × nevesta Barbara MILCH roj. ŠTRAVS, PUNOSTIVKA (VDOVA!), 25 [r. 4. X. 1894 ✓], GRIBLJE 41 (h41 = poročna 1919 №20!); ★★★ INTRA-GRIBLJE h46 × h41 + 4. GRIBLJE-vpis 1920; starši/Urkunden [faza-2 zoom čaka — honesty H19]",
    whatEn: "marriage (Feb 2, 1920, entry 10 — MONDAY) — groom Matija BRODARIČ [K/R — not 'Brodavič'!], a smallholder landowner's son, 21 [b. Jan 26, 1899 ✓], Roman Catholic, GRIBLJE 46 (★ a NEW Griblje house — the 1st marriage evidence of h46!) × bride Barbara MILCH née ŠTRAVS, a WIDOW, 25 [b. Oct 4, 1894 ✓], GRIBLJE 41 (h41 = the 1919 №20 marriage!); ★★★ an INTRA-GRIBLJE marriage h46 × h41 + the 4th Griblje entry of 1920; parents/documents [phase-2 zoom pending — honesty H19]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04455",
    year: 1920,
    scan: 180,
    page: 178,
    whatSi: "poroka (6. 9. 1920, vpis 27 — PONEDELJEK) — ženin Anton POŽEK, kmet. povest. sin, 29 [r. 25. VIII. 1891 [~ '25/9' → aritmetika 29 zahteva avgust!] — H10], rim. kat., GRIBLJE 18 (★ NOVA Griblje-hiša — 1. poročni dokaz h18!; oče †Jurij Požek — cf. 1919 №6 h77 Požek-rod!) × nevesta Marija KRIŽAN, RIHTARJA hči (2. rihtar po №5-Tafjan!), 18 [r. 28. V. 1902 ✓ — '1903' faza-1 → zoom '1902'!], Krasinec 47 (★ KRIŽAN ×160-mreža! oče = Miko Križan RIHTAR × Ana roj. Jakofčič); ★★★ GRIBLJE-VPIS h18 + priči Jakob Bohte + Marko ŠTABLJAR (cf. P145 Stubljar!) + otroško dovoljenje za 18-letno nevesto",
    whatEn: "marriage (Sep 6, 1920, entry 27 — MONDAY) — groom Anton POŽEK, a smallholder landowner's son, 29 [b. Aug 25, 1891 [~ 'Sep 25' → arithmetic 29 requires August!] — H10], Roman Catholic, GRIBLJE 18 (★ a NEW Griblje house — the 1st marriage evidence of h18!; father †Jurij Požek — cf. the 1919 №6 h77 Požek kin!) × bride Marija KRIŽAN, a bailiff's daughter (the 2nd bailiff after №5-Tafjan!), 18 [b. May 28, 1902 ✓ — '1903' phase-1 → the zoom shows '1902'!], Krasinec 47 (★ the KRIŽAN ×160 network! father = Miko Križan a BAILIFF × Ana née Jakofčič); ★★★ the GRIBLJE entry h18 + witnesses Jakob Bohte + Marko ŠTABLJAR (cf. P145 Stubljar!) + a child-consent for the 18-year-old bride",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04455",
    year: 1920,
    scan: 181,
    page: 179,
    whatSi: "poroka (13. 9. 1920, vpis 28 — PONEDELJEK) — ženin Jožef HUKAR [~ Huchar], kmet. povest. sin, 21 [r. 31. I. 1899 ✓], rim. kat., GRIBLJE 21 (★ NOVA Griblje-hiša — 1. poročni dokaz h21!; cf. priča 'Anton Hrugar hivar' 1921 №1 = Hukar-mreža? [~]) × nevesta Nera MOTYJEC [~ Matijec], kmet. povest. hči, 22 [r. 1. I. 1898 ✓], Bedenj 47, ŽUPNIJA ZGORNJI ADLEŠIČI (izven-župnijska!); ★★★ GRIBLJE-VPIS h21 + priči Marko ŠTABLJAR + Anton POŽEK (Griblje sosedi! — cf. №27!) + 3 listine (Adlešiči!)",
    whatEn: "marriage (Sep 13, 1920, entry 28 — MONDAY) — groom Jožef HUKAR [~ Huchar], a smallholder landowner's son, 21 [b. Jan 31, 1899 ✓], Roman Catholic, GRIBLJE 21 (★ a NEW Griblje house — the 1st marriage evidence of h21!; cf. the witness 'Anton Hrugar a house-farmer' 1921 №1 = a Hukar network? [~]) × bride Nera MOTYJEC [~ Matijec], a smallholder landowner's daughter, 22 [b. Jan 1, 1898 ✓], Bedenj 47, THE PARISH OF ZGORNJI ADLEŠIČI (out-of-parish!); ★★★ the GRIBLJE entry h21 + witnesses Marko ŠTABLJAR + Anton POŽEK (Griblje neighbours! — cf. №27!) + 3 documents (Adlešiči!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04455",
    year: 1920,
    scan: 182,
    page: 180,
    whatSi: "poroka (8. 11. 1920, vpis 34 — PONEDELJEK) — ženin Janez KURE, povest., 35 [r. 8. XII. 1884 ✓], rim. kat., GRIBLJE 6 (h6 = poročna 1903 №14 Jakobčič! 2. poročni dokaz h6; starši †Anton Kure povest. × Bara roj. KRIŽAN!) × nevesta Marija KRIŽAN, kmet. povest. hči, 24 [r. 19. III. 1896 ✓], GRIBLJE 36 (★ NOVA Griblje-hiša — 1. poročni dokaz h36!; starši Janez Križan povest. × Katarina roj. Štunf); ★★★ INTRA-GRIBLJE h6 × h36 + KRIŽAN OBEH straneh (mama-ženina roj. Križan + oče-neveste Križan — ×160-mreža!) + faza-1-№-kolizija rešena (s181 = №28–33, s182 = №34–36!)",
    whatEn: "marriage (Nov 8, 1920, entry 34 — MONDAY) — groom Janez KURE, a landowner, 35 [b. Dec 8, 1884 ✓], Roman Catholic, GRIBLJE 6 (h6 = the 1903 №14 Jakobčič marriage! the 2nd marriage evidence of h6; parents †Anton Kure × Bara née KRIŽAN!) × bride Marija KRIŽAN, a smallholder landowner's daughter, 24 [b. Mar 19, 1896 ✓], GRIBLJE 36 (★ a NEW Griblje house — the 1st marriage evidence of h36!; parents Janez Križan × Katarina née Štunf); ★★★ an INTRA-GRIBLJE marriage h6 × h36 + KRIŽAN on BOTH sides (the groom's mother née Križan + the bride's father Križan — the ×160 network!) + the phase-1 №-collision resolved (s181 = №28–33, s182 = №34–36!)",
    status: "DOCUMENTED",
  },

  // ——— P148 razširitev: POROČNA KNJIGA 04455 — polno leto 1919 (skeni
  // s165–s175 == Pag. 164–174; letna glava »Leto 1919.« ročno VELIKO na
  // s165 [7. zaporedna!]; meja 1919/1920 = veliki cifri »19«/»20« na
  // s175-sredini — 7. marker-tehnika!); 40 vpisov (39 oštevilčenih №1–№39
  // + 1 NEŠTEVILČEN Boren 24.2.!) = ★★★ REKORD LINIJE (prej 1912: 17 —
  // ×2,35!) — povojni poročni boom (1914:7 → 1915:6 → 1916:4 → 1917:8 →
  // 1918:4 → 1919:40!); 33 PON + 6 NED + 1 SOB (82,5 % ponedeljkov!);
  // vpisi z Griblji (10 porok!): №3 h22[~] · №6 h77×87 · №13 h12×30 ·
  // №18 h2×58 · №20 h41×64[~] · №21 h20×13 · №27 h48 · №33 h61 · №34
  // h26×24 · №35 h15 = 16 Griblje-številk (REKORD pokritosti!):
  // NOVELE: ★★★ 10 GRIBLJE-VPISOV (P147-lead napovedal 1!) + ★★★ VPIS
  // BREZ ŠTEVILKE (1. v liniji 1886–1919!) + ★★★ PEZDIRC-DELAŽA = 25
  // omenb (neveste ×4 · ženini ×3 · matere ×5 · priče ×7 · intra-priimek
  // №24 Otok 4×1! · intra-starši №26/№33!) + ★★ 2 VDOVI PO WWI-VOJAKIH
  // (№13 Kambič † sodno potrdilo 14.2.1919! + №15 Hosteler LAJTNANT †
  // 1918!) + ★★ FAMILIJSKI DVOJNI POROČNI DANI ×4 (brat+sestra Mališič
  // Otok 13 oba 10.2. ISTI priči! · sistri Rovnik Lemelj 41 24.+29.11.
  // ISTI priči! · brata Klepec 27.1.+20.10. oče-župan! · sestra+brat
  // Pezdirc Krasinec 28!) + ★ 5 VPISOV NA ISTI DAN 10.2. (№7–№11 =
  // rekord dneva!) + ★ INTRA-HIŠE ×3 (№4 Gradac 4 · №10 Primostek 15 ·
  // №11 Lemelj 22 = REKORD LINIJE!) + ★ POSTNA VRZEL nazaj 2.3.→28.4.
  // (Veliko noč 20.4.1919 — 1. od 1914!) + ★ SHS-TRANZICIJA (Narodna
  // vlada Ljubljana + deželna vlada za Slovenijo poleg k.u.k. glavarjev!)
  // + ★ NOVI POKLICI (žandar №25! · poštar №14! · parna žaga №37! ·
  // svihtar/sakristan ×3!) + ★ 9 nedoletnih nevest + 2 ženina (večjost
  // 24!) + proglasitev polnoletnosti №36 (1. v liniji!) + ★ 4 KASNEJŠE
  // ANOTACIJE 1975–1980 (№19 · №20 'Husič Anton † 29.4.1975 v Gribljah
  // št. 90!' · №33 'Požek Peter † 18.6.1975' · №3 modra 1980!) + ★ 2
  // samokorekciji pisarja (№15 prečrtan bivališč · №28 avg→sept!) +
  // duhovnik Gregor Cerar ~20× (nov dominantni!) + Valerian Urban dekan
  // ×5 (10.2.-blok!) + kaplan ×2
  // Dokaz: research/issue17/parish-marriage-1919.json; verifikator:
  // scripts/p148_parish_marriage_1919.py --check (I1–I12).
  {
    houseNo: "22",
    bookSignature: "04455",
    year: 1919,
    scan: 165,
    page: 164,
    whatSi: "poroka (27. 1. 1919, vpis 3 — PONEDELJEK) — ženin Janez KLEPEC, kmet. povestnika sin, 25 [r. 19. IX. 1894 — aritmetika 24 [~ zapis 25!]], rim. kat., Krasinec 36 (oče Miklo [~ Nikolaj] Klepec ŽUPAN × Katarina roj. Segina — cf. №32 BRAT!) × nevesta Katarina STRAVS, kmet. povestnika hči, 21 [r. 27. III. 1898], GRIBLJE 22 [~ — zoom 'lje 22'; faza-1 'Apilje 42' ZAVRŽENO!] (starši Matija Stravs × Marija roj. Jakofčič †); ★ 1. GRIBLJE-vpis 1919 (P147-lead pričakoval šele №6!) + priči: Jožef PEZDIRC, povest. + Miklo Požek, povest. (PEZDIRC 1./7!); duhovnik Miklavčič [~ — 6. branje!]; modra svinčnica-anotacija 1980 o ženinu",
    whatEn: "marriage (Jan 27, 1919, entry 3 — MONDAY) — groom Janez KLEPEC, a smallholder landowner's son, 25 [b. Sep 19, 1894 — arithmetic 24 [~ the entry says 25!]], Roman Catholic, Krasinec 36 (father Miklo [~ Nikolaj] Klepec the MAYOR × Katarina née Segina — cf. №32 BROTHER!) × bride Katarina STRAVS, a smallholder landowner's daughter, 21 [b. Mar 27, 1898], GRIBLJE 22 [~ — the zoom shows 'lje 22'; the phase-1 'Apilje 42' REJECTED!] (parents Matija Stravs × Marija née Jakofčič †); ★ the 1st GRIBLJE entry of 1919 (the P147-lead expected №6!); witnesses: Jožef PEZDIRC, landowner + Miklo Požek, landowner (PEZDIRC 1st/7!); priest Miklavčič [~ — the 6th reading!]; a blue-pencil annotation of 1980 about the groom",
    status: "DOCUMENTED",
  },
  {
    houseNo: "77",
    bookSignature: "04455",
    year: 1919,
    scan: 166,
    page: 165,
    whatSi: "poroka (3. 2. 1919, vpis 6 — PONEDELJEK) — ženin Jurij POŽEK, hišar, 35 [r. 6. V. 1883 ✓], rim. kat., GRIBLJE 77 (starši Jurij Požek hišar † × Katarina roj. KRIŽAN) × nevesta Marija PEZDIRC, dekla, 27 [r. 4. XII. 1892 — aritmetika 26 [~]], GRIBLJE 87 [KOREKCIJA P147-lead '37/8'!] (starši Marko Pezdirc hišar † × Ana roj. Željko); ★★★ INTRA-GRIBLJE h77 × h87 (Požek × PEZDIRC!) + priči: Miklo Željko ŽUPAN + Miklo Požek povest. (3. župan-priča 1919!); zglasnica županstva Griblje št. 1/1919",
    whatEn: "marriage (Feb 3, 1919, entry 6 — MONDAY) — groom Jurij POŽEK, a house-farmer, 35 [b. May 6, 1883 ✓], Roman Catholic, GRIBLJE 77 (parents Jurij Požek a house-farmer † × Katarina née KRIŽAN) × bride Marija PEZDIRC, a maidservant, 27 [b. Dec 4, 1892 — arithmetic 26 [~]], GRIBLJE 87 [a CORRECTION of the P147-lead '37/8'!] (parents Marko Pezdirc a house-farmer † × Ana née Željko); ★★★ an INTRA-GRIBLJE marriage h77 × h87 (Požek × PEZDIRC!); witnesses: Miklo Željko the MAYOR + Miklo Požek (the 3rd mayor-witness of 1919!); the banns of the Griblje municipality no. 1/1919",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04455",
    year: 1919,
    scan: 168,
    page: 167,
    whatSi: "poroka (24. 2. 1919, vpis 13 — PONEDELJEK) — ženin Franc DRAGOS, živžar [~ poklic nejasen — cf. №15!], 25 [r. 28. I. 1894 ✓], rim. kat., GRIBLJE 12 [zoom potrjuje '12' — faza-1 '42' ZAVRŽENO!] (starši Janez Dragos × Barbara roj. Cvilkovič [~]) × nevesta Marija MILEK, VDOVA KAMBIČ, povestnica, 27 [r. 13. IV. 1891 ✓], GRIBLJE 30 [zoom hišni stolpec '30.' — faza-1 '50' ZAVRŽENO!] (starši Janez Milek † × Marija roj. PEZDIRC †); ★★★ NEVESTA = VDOVA PO WWI-VOJAKU: potrdilo okrajnega sodišča Črnomelj 14.2.1919 o smrti Janeza KAMBIČA, VOJAKA, prvega moža! + priča Marko PEZDIRC (3./7!) + INTRA-GRIBLJE h12 × h30",
    whatEn: "marriage (Feb 24, 1919, entry 13 — MONDAY) — groom Franc DRAGOS, a 'živžar' [~ an unclear trade — cf. №15!], 25 [b. Jan 28, 1894 ✓], Roman Catholic, GRIBLJE 12 [the zoom confirms '12' — the phase-1 '42' REJECTED!] (parents Janez Dragos × Barbara née Cvilkovič [~]) × bride Marija MILEK, a KAMBIČ WIDOW, a landowneress, 27 [b. Apr 13, 1891 ✓], GRIBLJE 30 [the zoom of the house-number column shows '30.' — the phase-1 '50' REJECTED!] (parents Janez Milek † × Marija née PEZDIRC †); ★★★ the BRIDE IS A WWI-SOLDIER'S WIDOW: the district court of Črnomelj's certificate of Feb 14, 1919 on the death of Janez KAMBIČ, a SOLDIER, her first husband! + witness Marko PEZDIRC (3rd/7!) + an INTRA-GRIBLJE marriage h12 × h30",
    status: "DOCUMENTED",
  },
  {
    houseNo: "2",
    bookSignature: "04455",
    year: 1919,
    scan: 170,
    page: 169,
    whatSi: "poroka (18. 5. 1919, vpis 18 — NEDELJA) — ženin Nikolaj HLEBEC [~ Kleber/Klepec — 'lebec' jasno!], povest. sin, 31 [r. 3. X. 1887 ✓], rim. kat., GRIBLJE 2. (starši Peter Hlebec × Ana roj. Jakofčič †) × nevesta Barbara KAMBIČ, povest. hči, 26 [r. 19/24. IX. 1893 [~]], GRIBLJE 58 (starši Matija Kambič † × Ana roj. PEZDIRC †); ★★ INTRA-GRIBLJE h2 × h58 + mati neveste roj. PEZDIRC † (5./25!) + priča Matija PEZDIRC (1./7!)",
    whatEn: "marriage (May 18, 1919, entry 18 — SUNDAY) — groom Nikolaj HLEBEC [~ Kleber/Klepec — 'lebec' is clear!], a landowner's son, 31 [b. Oct 3, 1887 ✓], Roman Catholic, GRIBLJE 2. (parents Peter Hlebec × Ana née Jakofčič †) × bride Barbara KAMBIČ, a landowner's daughter, 26 [b. Sep 19/24 [~], 1893], GRIBLJE 58 (parents Matija Kambič † × Ana née PEZDIRC †); ★★ an INTRA-GRIBLJE marriage h2 × h58 + the bride's mother née PEZDIRC † (5th/25!) + witness Matija PEZDIRC (1st/7!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04455",
    year: 1919,
    scan: 170,
    page: 169,
    whatSi: "poroka (26. 5. 1919, vpis 20 — PONEDELJEK) — ženin Anton KLUSIČ [~ Hlusič/Husič — anotacija 1975 piše 'Husič'!], povestniški sin, 22 [r. 9. IV. 1896 ✓], rim. kat., GRIBLJE 41. (starši Matija Hlusič [~] × Vera roj. Jakofčič) × nevesta Jozefa ŠTRAVS, povestniška hči, 19 [r. 10. II. 1900 ✓ — NEDOLETNA!], GRIBLJE 64 [~ 65?] (starši Nikolaj Štravs × Marija roj. Jakofčič); ★★ INTRA-GRIBLJE h41 × h64[~] + OBE matere JAKOFČIČ! + priča Matija PEZDIRC (2./7!) + KASNEJŠA ANOTACIJA 1975: 'Zakonec Husič Anton umrl 29.4.1975 v Gribljah št. 90' (nova hišna referenca 90!); 6 urdnih postavk (sodišče + glavarstvo)",
    whatEn: "marriage (May 26, 1919, entry 20 — MONDAY) — groom Anton KLUSIČ [~ Hlusič/Husič — the 1975 annotation writes 'Husič'!], a landowner's son, 22 [b. Apr 9, 1896 ✓], Roman Catholic, GRIBLJE 41. (parents Matija Hlusič [~] × Vera née Jakofčič) × bride Jozefa ŠTRAVS, a landowner's daughter, 19 [b. Feb 10, 1900 ✓ — a MINOR!], GRIBLJE 64 [~ 65?] (parents Nikolaj Štravs × Marija née Jakofčič); ★★ an INTRA-GRIBLJE marriage h41 × h64[~] + BOTH mothers JAKOFČIČ! + witness Matija PEZDIRC (2nd/7!) + a LATER 1975 ANNOTATION: 'the spouse Husič Anton died Apr 29, 1975 in Griblje no. 90' (a new house reference 90!); 6 official documents (the court + the district authority)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04455",
    year: 1919,
    scan: 171,
    page: 170,
    whatSi: "poroka (26. 5. 1919, vpis 21 — PONEDELJEK) — ženin Peter PEZDIRC, povestnik, 32 [r. 25. X. 1886 ✓], rim. kat., GRIBLJE 20. (starši Peter Pezdirc † × Katarina roj. Deklič [~]) × nevesta Barbara JAKOFČIČ, povestniška hči, 30 [r. 3. IV. 1888 — aritmetika 31 [~]], GRIBLJE 13. (starši Matija Jakofčič × Marija roj. PEZDIRC †); ★★★ ŽENIN = PEZDIRC! + mati neveste roj. PEZDIRC + OBA priča PEZDIRC (Matija 3./7! + Jure 1./7!) = 5 PEZDIRC-oseb v enem vpisu! + INTRA-GRIBLJE h20 × h13",
    whatEn: "marriage (May 26, 1919, entry 21 — MONDAY) — groom Peter PEZDIRC, a landowner, 32 [b. Oct 25, 1886 ✓], Roman Catholic, GRIBLJE 20. (parents Peter Pezdirc † × Katarina née Deklič [~]) × bride Barbara JAKOFČIČ, a landowner's daughter, 30 [b. Apr 3, 1888 — arithmetic 31 [~]], GRIBLJE 13. (parents Matija Jakofčič × Marija née PEZDIRC †); ★★★ THE GROOM IS A PEZDIRC! + the bride's mother née PEZDIRC + BOTH witnesses PEZDIRC (Matija 3rd/7! + Jure 1st/7!) = 5 PEZDIRC persons in one entry! + an INTRA-GRIBLJE marriage h20 × h13",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04455",
    year: 1919,
    scan: 172,
    page: 171,
    whatSi: "poroka (25. 8. 1919, vpis 27 — PONEDELJEK) — ženin Janez GUSTAVIN [~ Šustavin?], povestniška sin, 28 [r. 25. XII. 1890 ✓], rim. kat., [~ Šmilovje/Sutloga?] 31 (starši Janez(?) Gustavin × Ana roj. Jakofčič) × nevesta Marija BERKOPER, povestniška hči, 19 [r. 26. X. 1898 [~ aritmetika 20!]], GRIBLJE 48. (starši Janez Berkoper × Katarina roj. HLEBEC, umrla kot Pezdirc? [~]); ★★ NEVESTA IZ GRIBLJE 48 + mati roj. HLEBEC (cf. №18 ženin!) + priča Peter PEZDIRC (7./7!) + podpis žup. Kapl. + 'per delegatis nem.' [~]",
    whatEn: "marriage (Aug 25, 1919, entry 27 — MONDAY) — groom Janez GUSTAVIN [~ Šustavin?], a landowner's son, 28 [b. Dec 25, 1890 ✓], Roman Catholic, [~ Šmilovje/Sutloga?] 31 (parents Janez(?) Gustavin × Ana née Jakofčič) × bride Marija BERKOPER, a landowner's daughter, 19 [b. Oct 26, 1898 [~ arithmetic 20!]], GRIBLJE 48. (parents Janez Berkoper × Katarina née HLEBEC, died as Pezdirc? [~]); ★★ the BRIDE IS FROM GRIBLJE 48 + the mother née HLEBEC (cf. №18 the groom!) + witness Peter PEZDIRC (7th/7!) + the signature 'žup. Kapl.' + 'per delegatis nem.' [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04455",
    year: 1919,
    scan: 173,
    page: 172,
    whatSi: "poroka (3. 11. 1919, vpis 33 — PONEDELJEK) — ženin Peter POŽEK, povestnika sin, 23 [r. 28. VI. 1896 ✓], rim. kat., GRIBLJE 61. (starši Nikolaj Požek × Ana roj. Dragos) × nevesta Marija PEZDIRC, povestniška hči, 22 [r. 12. XI. 1896 ✓], Krasinec 28. (starši Peter PEZDIRC × Marija roj. PEZDIRC = ISTI STARŠI KOT №26 ŽENIN!); ★★★ NEVESTA = SESTRA ženina №26 (Peter Pezdirc Krasinec 28 — oba poročena 1919: 11.8. + 3.11.!) + Griblje 61 + priča Anton Jakofčič + KASNEJŠA ANOTACIJA 1975/76: 'Zakonec Požek Peter umrl 18.6.1975 v Gribljah'",
    whatEn: "marriage (Nov 3, 1919, entry 33 — MONDAY) — groom Peter POŽEK, a landowner's son, 23 [b. Jun 28, 1896 ✓], Roman Catholic, GRIBLJE 61. (parents Nikolaj Požek × Ana née Dragos) × bride Marija PEZDIRC, a landowner's daughter, 22 [b. Nov 12, 1896 ✓], Krasinec 28. (parents Peter PEZDIRC × Marija née PEZDIRC = THE SAME PARENTS AS THE №26 GROOM!); ★★★ THE BRIDE IS THE SISTER of the №26 groom (Peter Pezdirc Krasinec 28 — both married in 1919: Aug 11 + Nov 3!) + Griblje 61 + witness Anton Jakofčič + a LATER 1975/76 ANNOTATION: 'the spouse Požek Peter died Jun 18, 1975 in Griblje'",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04455",
    year: 1919,
    scan: 173,
    page: 172,
    whatSi: "poroka (10. 11. 1919, vpis 34 — PONEDELJEK) — ženin Matija KRALJ, povestniška sin, 25 [r. 4. XI. 1894 ✓], rim. kat., GRIBLJE 26. (starši Nikolaj Kralj † × Katarina roj. Jakofčič) × nevesta Ana BRINEC, povestnika hči, 24 [r. 19. IV. 1895 — faza-1 '19/9 1893' ZAVRŽENO, aritmetika!], GRIBLJE 24. (starši Matija Brinec † × Barbara roj. Jakofčič); ★★ INTRA-GRIBLJE h26 × h24 + OBE matere JAKOFČIČ! + priča Jurij Štravs SVIHTAR (sakristan — 1. sistematični pojav poklica!) + Nikolaj Milek sameški fant [~]",
    whatEn: "marriage (Nov 10, 1919, entry 34 — MONDAY) — groom Matija KRALJ, a landowner's son, 25 [b. Nov 4, 1894 ✓], Roman Catholic, GRIBLJE 26. (parents Nikolaj Kralj † × Katarina née Jakofčič) × bride Ana BRINEC, a landowner's daughter, 24 [b. Apr 19, 1895 — the phase-1 'Sep 19, 1893' REJECTED by arithmetic!], GRIBLJE 24. (parents Matija Brinec † × Barbara née Jakofčič); ★★ an INTRA-GRIBLJE marriage h26 × h24 + BOTH mothers JAKOFČIČ! + witness Jurij Štravs a SVIHTAR (the sexton — the 1st systematic appearance of the trade!) + Nikolaj Milek a bachelor lad [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04455",
    year: 1919,
    scan: 174,
    page: 173,
    whatSi: "poroka (17. 11. 1919, vpis 35 — PONEDELJEK) — ženin Matija JURAJEVIČ [~ — cf. №29 Juragec!], povestnika sin, 25 [r. 11. VIII. 1894 ✓], rim. kat., Krasinec 5. (starši Nikolaj Juragevič [~] × Katarina roj. Klepec) × nevesta Barbara JAKLIČ, povestnika hči, 22 [r. 14. IX. 1897 ✓], GRIBLJE 15. (starši Janez Jaklič × Marija roj. Brinec †); ★ NEVESTA IZ GRIBLJE 15 (h15 = 1917 №3 poročna hiša Jakljič × Šimec — 2. poroka h15 v vzorcu!) + priča Matija Berkoper [~]",
    whatEn: "marriage (Nov 17, 1919, entry 35 — MONDAY) — groom Matija JURAJEVIČ [~ — cf. №29 Juragec!], a landowner's son, 25 [b. Aug 11, 1894 ✓], Roman Catholic, Krasinec 5. (parents Nikolaj Juragevič [~] × Katarina née Klepec) × bride Barbara JAKLIČ, a landowner's daughter, 22 [b. Sep 14, 1897 ✓], GRIBLJE 15. (parents Janez Jaklič × Marija née Brinec †); ★ the BRIDE IS FROM GRIBLJE 15 (h15 = the 1917 №3 marriage house Jakljič × Šimec — the 2nd h15 marriage in the sample!) + witness Matija Berkoper [~]",
    status: "DOCUMENTED",
  },

  // ——— P146 razširitev: POROČNA KNJIGA 04455 — polno leto 1917 (skeni
  // s160–s163 == Pag. 159–162; letna glava »Leto 1917« ročno VELIKO na s160
  // [5. zaporedna!]; meja 1917/1918: s163 vsebuje ŽE letno glavo »1918« +
  // 1918 №1 = KNJIGA SE NADALJUJE! + NASLOVNICA s192 = »Podzemelj
  // P 1873–1922« → poročna knjiga do 1922 — README-popravek!); 8 vpisov:
  // … → 1915:6 → 1916:4 → 1917:8 — OBNOVA po 1916 (še vedno pod vojno
  // ravnjo!); 5 NED + 1 PON + 2 SRE — vpisi z Griblji (1 poroka: №3 h15 ×
  // h38 INTRA!):
  // NOVELE: ★★★ №2–№5 = 4 POROKE NA ISTI DAN 18. 2. 1917 (nedelja) = 2.
  // REKORD LINIJE (po 1893: 7!) + ★★★ VOJAŠKI WWI-REŽIM (№1 Franc Vrhovnik
  // zidar-SANITETNI vojak + Genehmigung der k.k. Feld-Sanitäts-Abtheilung +
  // DISPENS von 3 Aufgeboten [tempora clausa — vojna NUJNA poroka na sredo
  // 3.1.!] + №6 Jožef Jager k.u.k. VOJNI delavec + №8 Andrej Višček vojni
  // INVALID-fotograf »PRI VOJAKIH« [1. vojaški Wohnort linije!] +
  // Trauungsermächtigung des Feldsuperiors Štabbuch 4982/17 + 2. DISPENS!) +
  // ★★ №4 1. MLADOLETEN ŽENIN LINIJE (Lovrencij Štrukelj 21 < 24! — čevljar
  // + žel. uslužbenec, 2 poklica!) + mladoletna nevesta = OBA MLADOLETA (1.
  // tak par!) + zglašnica KRANJSKA GORA (2. pojav — žel. mobilnost!) + ★★
  // №7 oče-ŽENINA PRAZEN (3. primer!) + Janez Butala 70 LET [r. 1846 — 2.
  // najstarejši ženin po 71 = 1914 №4!] + 33-letna razlika + GRAĐNIK-priča
  // (Jožef Ronda — NOV poklic!) + ★★ №3 PREDKORPUSNA generacija (Janez
  // Jakljič b. 8. 6. 1863 — 53! = najstarejši rojen ženin z rojstnim letom!)
  // + 4 pokojni starši + zglašnica NA POROČNI DAN št. 1 + ★ №5 30-letna
  // razlika (Nikolaj Adlešič 65 × Katarina Kambič 35!) + TRIBUČE (2. pojav
  // P144-oblasti!) + №2 M1906-ŽENIN-HIŠA (Županič-18 recipročni par!) v 2.
  // zakonu [~ vdovec] + ISTA-HIŠE 1917 = 0 (2. leto!) + duhovnik Valerijan
  // Miklavčič ×8 (4. branje!) + ~7 NOVIH PRIIMKOV (Jager · Drganec · Višček
  // · Šarašinič [~] · Lugnar · Ronda · Halčič [~])
  // Dokaz: research/issue17/parish-marriage-1917.json; verifikator:
  // scripts/p146_parish_marriage_1917.py --check (I1–I12).
  {
    houseNo: "15",
    bookSignature: "04455",
    year: 1917,
    scan: 161,
    page: 160,
    whatSi: "poroka (18. 2. 1917, vpis 3 — NEDELJA; 2. od 4 POROK NA ISTI DAN [№2–№5!] = 2. REKORD LINIJE po 1893: 7!) — ženin Janez JAKLJIČ [korpus ×14!], posestnik, 53 [r. 8. VI. 1863 — 53 ✓ aritmetika — PREDKORPUSNA generacija: najstarejši rojen ženin z rojstnim letom v liniji!], rim. kat., GRIBLJE 15 (h15 = poročna 1887 №4 Fablić! znana hiša; starši +Miko Jakljič posestnik † × +Marija roj. Šambič [~] †) × Ana ŠIMEC [korpus ×223 = NAJVEČJA priimška mreža!], posestnica samostne hiše, 44 [r. 2. V. 1872 — 44 ✓], GRIBLJE 38 (h38 = znana hiša; starši +Jure Šimec posestnik † × +Ana roj. Križan † = KRIŽAN-mreža!); ★ INTRA-GRIBLJE (h15 × h38 — obe znani!) + 4 pokojni starši (obe strani!) + zglašnica ženinova od županstva Griblje NA POROČNI DAN 18. 2. 1917 št. 1 (hitri zakon!); priči: Matija Jakljič, posest. + Matija Štraus, posest. (ŠTRAUS-mreža — h71→h31 selitev P143!), oba rim. kat.; duhovnik Val. Miklavčič [~ — 4. branje!]",
    whatEn: "marriage (Feb 18, 1917, entry 3 — SUNDAY; the 2nd of 4 MARRIAGES ON THE SAME DAY [№2–№5!] = the 2nd RECORD OF THE LINE after 1893: 7!) — groom Janez JAKLJIČ [the corpus ×14!], a landowner, 53 [b. Jun 8, 1863 — 53 ✓ arithmetic — a PRE-CORPUS generation: the oldest groom with a birth year in the line!], Roman Catholic, GRIBLJE 15 (h15 = the 1887 marriage №4 Fablić! a known house; parents +Miko Jakljič landowner † × +Marija née Šambič [~] †) × Ana ŠIMEC [the corpus ×223 = THE LARGEST surname network!], an independent house's owneress, 44 [b. May 2, 1872 — 44 ✓], GRIBLJE 38 (h38 = a known house; parents +Jure Šimec landowner † × +Ana née Križan † = the KRIŽAN network!); ★ an INTRA-GRIBLJE marriage (h15 × h38 — both known!) + 4 deceased parents (both sides!) + the banns of the groom from the Griblje municipality ON THE WEDDING DAY Feb 18, 1917 no. 1 (a swift marriage!); the witnesses: Matija Jakljič, landowner + Matija Štraus, landowner (the ŠTRAUS network — the h71→h31 move P143!), both Roman Catholic; priest Val. Miklavčič [~ — the 4th reading!]",
    status: "DOCUMENTED",
  },

  // ——— P145 razširitev: POROČNA KNJIGA 04455 — polno leto 1916 (skeni
  // s158 + s159 == Pag. 157–158; s158 = letna glava »1916« [P144-pričakovano!];
  // meja 1916/1917: s159-dno = PRAZEN pas + DIAGONALA (obe strani!) + s160 =
  // letna glava »1917« + reset štetja №1!); 4 vpisov: 1886:7 → … → 1914:7 →
  // 1915:6 → 1916:4 — WWI VRHUNEC = NAJŠIBKEJŠE LETO LINIJE (padec 6 → 4!);
  // 1 ČET №1 (1. četrtek linije — vojaški termin!) + 2 NED + 1 PON — vpisi z
  // Griblji (1 poroka: №2 h37 × h27 INTRA!):
  // NOVELE: ★★★ №1 VOJAK 5. ARMade — SOŠKA FRONTA (Franc Moretič, voj.
  // rezervist v vojski, Rinče na Goriškem 241 [~ 24] — najbolj oddaljen dom
  // linije ~180 km! + Ermächtigungsschein des Feldsup. d. V-Armee 25. I. 1916
  // = 2. vojaška listina linije po 1915 №4!) + ★★★ №2 TROJNA
  // KORPUS-SINHRONIZACIJA STUBLJAR-KUHAR (poroka 27. 2. 1916 EXACT v
  // korpusu-krsti 1918/19 'mati Ivana roj. Kukar (7. 5. 1893; por. 27. 2.
  // 1916)' + roj. 7. 5. 1893 EXACT + starša neveste = korpus-par 'Kuhar?/
  // Kuklar? [~] ½ zemljak × Katarina Klobučar [~]' iz krst h29 1888–1892!) +
  // ★★ №2 3 POPRAVKE P144-leada (POSESTNIK ne vdovec! + 26 let ne 37! + h27
  // ne 34! = PERDINČEVA hiša — oče HIŠAR = najemnik = nov socialni vzorec!) +
  // ★★ №2+№4 DVE MLADOLETNI nevesti (22 + 20) = REKORD LINIJE + №2 ustno
  // dovoljenje očeta pred gorenjima pričama (1. privolitveni režim!) + ★★ №3
  // OČE-ŽENINA PRAZEN (2. primer po 1915 №1!) + nevesta POSESTRICA [~] + roj.
  // GORJE (2. Gorenjska-žel. mobilnost po 1915 №6!) + ★★ №4 7 listin a–g
  // (miliški list št. 321 + škof. odredba ZA ČAS VOJSKE + obč. TALIČVRH [~]
  // NEidentificirana!) + ★★ №3+№4 DVOTERNA hiša h4 VRANOVIČE (hišna veriga!) +
  // ISTE-HIŠE 1916 = 0 (1. leto z 0 po 1913!) + duhovnik Valerijan Miklavčič
  // ×4 (3. branje podpira korpus-Miklavč-!) + ~8 NOVIH PRIIMKOV (Moretič ·
  // Fajt · Kupanič [~] · Skvarča · Štrukelj · Grahek · Malnerič · Kohanič [~])
  // Dokaz: research/issue17/parish-marriage-1916.json; verifikator:
  // scripts/p145_parish_marriage_1916.py --check (I1–I12).
  {
    houseNo: "37",
    bookSignature: "04455",
    year: 1916,
    scan: 158,
    page: 157,
    whatSi: "poroka (27. 2. 1916, vpis 2 — NEDELJA; korpus-krsti 1918/19: 'por. 27. 2. 1916' EXACT!) — ženin Marko STUBLJAR [~ Stublar — korpus-1918/19: 'Stublar? [~ Stubljar]'], posestnik [P144-lead 'vdovec 37 let' = PRAVKA POPRAVKA!], 26 [r. 30. VII. 1889 — 26 ✓ aritmetika], ženin, GRIBLJE 37 (1825-cenzus 1.0 — P81 Stubler @30; oče +Marko Stubljar posest. † — ISTO IME oče-sin! × mati Ana roj. Grabrijan [korpus ×40!]) × Frana KUHAR [~ Ivana po korpusu-krsti 1918/19 ('mati Ivana roj. Kukar') — 2 roki!; Kuhar/Kukar — K/H-linija], hišarjeva hči samostne hiše, 22 [r. 7. V. 1893 — korpus EXACT ✓✓; 22 ✓], MLADOLETNA ženina (22 < 24 — avstrijska polnoletnost!), GRIBLJE 27 [P144-lead '34' = PRAVKA POPRAVKA!; h27 = PERDINČEVA hiša (korpus v3/v11 Marcus Perdinec ¼ × Margareth Klepec) — oče Fran Kuhar [~ Kukar] HIŠAR = najemnik/gospodar na tuji hiši = NOV socialni vzorec linije! × mati Katarina roj. Klobučar [korpus ×135! = korpus-par 'Kuhar?/Kuklar? [~] × Katarina Klobučar [~]' iz krst h29 1888–1892 — TROJNA SINHRONIZACIJA!]); ★ INTRA-GRIBLJE (h37 × h27 — edini Griblje-vpis leta: WWI VRHUNEC — 4 poroke = najšibkejše leto linije 1915: 6 → 4!); priči: Peter Kohanič [~ Kohanić/Kohanec — nov priimek!] + Janez Grabrijan (ženinova mati-rodbina!), oba posest. kat.; listine: ženitovanjska zglašnica županstva Griblje št. 1 z dne 25. 2. 1916 (poroka 2 dni kasneje ✓) + ZA MLADOLETNO NEVESTO ustno dovoljenje očeta pred gorenjima pričama (★ 1. 'ustno dovoljenje očeta pred pričami' linije — prej listine/sodne privolitve!); duhovnik Val. Miklavčič [~ Mikčak/Miklavžič — 3. branje!]",
    whatEn: "marriage (Feb 27, 1916, entry 2 — SUNDAY; the 1918/19 baptism corpus: 'm. Feb 27, 1916' EXACT!) — groom Marko STUBLJAR [~ Stublar — the 1918/19 corpus: 'Stublar? [~ Stubljar]'], a landowner [the P144 lead 'a 37-year-old widower' = THE CORRECTED READING!], 26 [b. Jul 30, 1889 — 26 ✓ arithmetic], single, GRIBLJE 37 (the 1825 census 1.0 — P81 Stubler @30; father +Marko Stubljar landowner † — THE SAME NAME father-son! × mother Ana née Grabrijan [the corpus ×40!]) × Frana KUHAR [~ Ivana per the 1918/19 baptism corpus ('the mother Ivana née Kukar') — 2 hands!; Kuhar/Kukar — the K/H line], a house-keeper's daughter of an own house, 22 [b. May 7, 1893 — the corpus EXACT ✓✓; 22 ✓], a MINOR bride (22 < 24 — the Austrian majority!), GRIBLJE 27 [the P144 lead '34' = THE CORRECTED READING!; h27 = the PERDINEC house (the corpus v3/v11 Marcus Perdinec ¼ × Margareth Klepec) — the father Fran Kuhar [~ Kukar] a HOUSE-Keeper = a tenant on someone else's house = a NEW social pattern of the line! × mother Katarina née Klobučar [the corpus ×135! = the corpus couple 'Kuhar?/Kuklar? [~] × Katarina Klobučar [~]' from the h29 baptisms 1888–1892 — a TRIPLE SYNCHRONIZATION!]); ★ an INTRA-GRIBLJE marriage (h37 × h27 — the only Griblje entry of the year: THE WWI PEAK — 4 marriages = the weakest year of the line 1915: 6 → 4!); the witnesses: Peter Kohanič [~ Kohanić/Kohanec — a new surname!] + Janez Grabrijan (the groom's mother-kin!), both landowners Catholic; the documents: the marriage banns of the Griblje municipality no. 1 of Feb 25, 1916 (the marriage 2 days later ✓) + FOR THE MINOR BRIDE the father's oral consent before the two witnesses (★ the 1st 'oral father's consent before witnesses' of the line — before: documents/court consents!); priest Val. Miklavčič [~ Mikčak/Miklavžič — the 3rd reading!]",
    status: "DOCUMENTED",
  },

  // ——— P122 razširitev: POROČNA KNJIGA 04455 — polno leto 1893 (skeni 87–90 ==
  // strani 86–89; VELIKA GLAVA »Traunungs=Buch« + rokopisno »1893« na s87 =
  // Pag. 86 POTRJENA — P122 lead!; 20 vpisov: 1886:7 → 1887:21 → 1888:20 →
  // 1889:10 → 1890:16 → 1891:18 → 1892:15 → 1893:20 = 2. največje leto
  // linije; razpored 6+5+5+4) — vpisi z Griblji (3 poroke / 5 poročnih blokov:
  // h26 v10 nevesta NOVA + h69 v15 ženin 2. dokaz 04455 + h62 v15 nevesta +
  // h58 v16 ženin + h74 v16 nevesta NOVA): NOVELE: 7 porok na isti dan 6.2. =
  // REKORD VSEH ČASOV! + BRAT-SESTRA PERDINEC dvozakon isti dan (v4+v6 — isti
  // starša!) + ★ RENOVACIJA ZAKONA 8.9.1898 (v8 latinski blok — dispensacija
  // 3. st. + Jeglič [~] + priči Maur + Skala = NOV DOKUMENT-TIP) + ★ 2.
  // DUHOVNIK LINIJE Michael Klemenčič Coop. ×2 (konec Rauy-monopola!) + ★ 1.
  // dokument občine GRIBLJE (v15!) + ★ INHABER nov status (v19) + ★ VOJSKA
  // nadvarstveno dovoljenje okrožja RUDOLFOVO=Novo mesto + proxy-zastopstvo
  // (v12!) + ★ DISPENS 3. kan. stopnje №1661 (v16 — starša oba BRINC!) +
  // deleži ¼/½ ×32 oseb + nevesta 17 tied-rekord + ženin 58 + Laipšl ×8.
  // Dokaz: research/issue17/parish-marriage-1893.json; verifikator:
  // scripts/p122_parish_marriage_1893.py --check (I1–I11).
  {
    houseNo: "26",
    bookSignature: "04455",
    year: 1893,
    scan: 88,
    page: 87,
    whatSi: "poroka (30. 4. 1893, vpis 10) — ženin Nicolaus KRALJ, ½ Gribler, 49, Fučkovec 14 pf. Adlešič [~ — nova vas poročnega vzorca] (oče Nicolaus Kralj ½ Gribler × Catharina KRALJ; KRALJ ×3 1893 cf. v7 ženin Georg + P121 v10!) × Catharina BRINEC, ¼ Griblerin, 37, GRIBLJE 26 (NOVA HIŠA poročnega vzorca — P122 lead popravka 26 NE 36!; krstna 1887 »Jurc Briuc [~] ali Brine« + 1889/1896/1906/1912 — h26 krstna vrzel 1889–1896 povezana s poroko!; oče Georg JAKOBIČ ¼ Gribler × Catharina Lukanič? [~]); priče: Georg Straus (STRAUS-mreža) + Math. Jankovič (} ½ gbl.); ★ 2. DUHOVNIK LINIJE: Michael KLEMENČIČ Coop. (1. podpis — konec Rauy-monopola od P117!); Befünden: zemljiška zglednica občine Adlešič od 27. aprila 1893 + oblični [~] list GJUPNIJSKEGA urada v Adlešičih od 30/4. 1893 št: 34 (slovenskojezični + hrvaška oblika »gjupnijski!«)",
    whatEn: "marriage (Apr 30, 1893, entry 10) — groom Nicolaus KRALJ, half smallholder, 49, Fučkovec 14 pf. Adlešič [~ — a new village of the marriage sample] (father Nicolaus Kralj ½ Gribler × Catharina KRALJ; KRALJ ×3 in 1893 cf. the v7 groom Georg + P121 v10!) × Catharina BRINEC, quarter smallholderess, 37, GRIBLJE 26 (A NEW HOUSE of the marriage sample — the P122 lead correction: 26 NOT 36!; the 1887 baptism »Jurc Briuc [~] or Brine« + 1889/1896/1906/1912 — the h26 baptism gap 1889–1896 is connected by the marriage!; father Georg JAKOBIČ quarter smallholder × Catharina Lukanič? [~]); witnesses: Georg Straus (the STRAUS network) + Math. Jankovič (} ½ gbl.); ★ the 2nd PRIEST OF THE LINE: Michael KLEMENČIČ Coop. (the 1st signature — the end of the Rauy monopoly since P117!); Befünden: the land registry certificate of the Adlešič commune from Apr 27, 1893 + the [marriage] list of the PARISH office (the Croatian form »gjupnijski«!) in Adlešiči from Apr 30, 1893 no. 34 (Slovenian-language!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04455",
    year: 1893,
    scan: 89,
    page: 88,
    whatSi: "poroka (12. 6. 1893, vpis 15) — ženin Johann BRINEC, ½ Gribler, 29, GRIBLJE 69 (2. poročni dokaz h69 04455 po 1887!; h69 = Brinec-gospodinjstvo krstna 1888–95 (P93: 5 vpisov) z menjavo na Straus 1898 — poroka = razlog menjave [~]; oče Johann Brinec ½ Gribler × Catharina ADLEŠIČ) × Anna KURE, ½ Griblers=tochft. + Ans [~], 24, GRIBLJE 62 (oče Anton KURE ½ Gribler × Anna KRIŽAN — KURE ×3 1893 cf. v7!); ★ DRUBEL-GRIBLJE poroka #1 (h69 × h62)!; ★ 1. dokument občine GRIBLJE v poročni liniji (dotlej vse druge občine!); priče: Johan Adlešič + Georg Perdinec (} ¼ gbl. — v4 ženin ISTI dan!); duhovnik Jos. Rauy; Befünden: zemljovanjska zglednica občine Griblje od 11/6. 1893 št: 1",
    whatEn: "marriage (Jun 12, 1893, entry 15) — groom Johann BRINEC, half smallholder, 29, GRIBLJE 69 (the 2nd marriage evidence of h69 in 04455 after 1887!; h69 = the Brinec household of the baptisms 1888–95 (P93: 5 entries) with the 1898 change to Straus — the marriage is the reason for the household change [~]; father Johann Brinec ½ Gribler × Catharina ADLEŠIČ) × Anna KURE, half smallholder's daughter + Ans [~], 24, GRIBLJE 62 (father Anton KURE half smallholder × Anna KRIŽAN — KURE ×3 in 1893 cf. v7!); ★ the DOUBLE-GRIBLJE marriage #1 (h69 × h62)!; ★ the 1st document of the GRIBLJE commune in the marriage line (so far always other communes!); witnesses: Johan Adlešič + Georg Perdinec (} ¼ gbl. — the v4 groom the same day!); priest Jos. Rauy; Befünden: the land registry certificate of the GRIBLJE commune from Jun 11, 1893 no. 1",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04455",
    year: 1893,
    scan: 89,
    page: 88,
    whatSi: "poroka (12. 6. 1893, vpis 15) — nevesta Anna KURE, ½ Griblers=tochft. + Ans [~], 24, GRIBLJE 62 (NOVA hiša poročnega vzorca; h62 = Kure-hiša: krstna 1887 Marjeta oče Anton KURE = v15 oče ISTI! + 1891 + 1907/1917 — krstna vrzel 1891→1907 povezana s poroko!) × Johann BRINEC, ½ Gribler, 29, GRIBLJE 69 (drubel poroka!); oče neveste Anton Kure ½ Gribler × Anna KRIŽAN (KRIŽAN ×3 1893!); duhovnik Jos. Rauy; Befünden: zglednica občine GRIBLJE 11/6. 1893 št: 1",
    whatEn: "marriage (Jun 12, 1893, entry 15) — bride Anna KURE, half smallholder's daughter + Ans [~], 24, GRIBLJE 62 (A NEW house of the marriage sample; h62 = the Kure house: the 1887 baptism Marjeta with father Anton KURE = the same as the v15 father! + 1891 + 1907/1917 — the baptism gap 1891→1907 is connected by the marriage!) × Johann BRINEC, half smallholder, 29, GRIBLJE 69 (the double-Griblje marriage!); the bride's father Anton Kure ½ Gribler × Anna KRIŽAN (KRIŽAN ×3 in 1893!); Befünden: the certificate of the GRIBLJE commune Jun 11, 1893 no. 1",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04455",
    year: 1893,
    scan: 89,
    page: 88,
    whatSi: "poroka (23. 7. 1893, vpis 16) — ženin Johann POŽEK, ¼ Gribler, 36, GRIBLJE 58 (1. POROČNI DOKAZ h58 sploh!; krstna 1889–1905 gosta = POŽEK/Požek-vrzel; P122 lead popravka: POŽEK ne »Joreh«!; oče Marcus Požek ¼ Gribler × Anna BRINEC — BRINC-mreža!) × Catharina KAMBIČ, ¼ Griblers=tochft, 22 (mladoletna!), GRIBLJE 74 (NOVA hiša poročnega vzorca — krstna 1893 + 1911 — ISTO LETO v obeh knjigah!); ★ DRUBEL-GRIBLJE poroka #2 (h58 × h74)!; ★ DISPENSACIJA 3. kanonične stopnje: Fürstbischöfl. Ordinariat Laibach delto 17.7.1893 №: 1661 (6 dni pred poroko!) — oče+mati neveste: Mathias Kambič × Catharina BRINEC → OBA MATERI BRINC = sorodstvo skozi Brinc-line!; priče: Nicol Požek (P121 v1 priča ISTI!) + Johan Kambič (} ½ gbl.); duhovnik Jos. Rauy; Befünden: zglasnica občine Griblje od 13/7. 1893 + dispens №1661 + mündl. freiwilligg f. d. mj. Braut",
    whatEn: "marriage (Jul 23, 1893, entry 16) — groom Johann POŽEK, quarter smallholder, 36, GRIBLJE 58 (the 1st MARRIAGE EVIDENCE of h58 ever!; the dense baptisms 1889–1905 = the POŽEK/Požek gap; the P122 lead correction: POŽEK not »Joreh«!; father Marcus Požek ¼ Gribler × Anna BRINEC — the BRINC network!) × Catharina KAMBIČ, quarter smallholder's daughter, 22 (a minor!), GRIBLJE 74 (A NEW house of the marriage sample — the baptisms 1893 + 1911 — the SAME YEAR in both books!); ★ the DOUBLE-GRIBLJE marriage #2 (h58 × h74)!; ★ the DISPENSATION of the 3rd canonical degree: the Prince-Bishop's Ordinariat Laibach dated Jul 17, 1893 №: 1661 (6 days before the wedding!) — the bride's parents: Mathias Kambič × Catharina BRINEC → BOTH MOTHERS BRINC = the kinship through the Brinc line!; witnesses: Nicol Požek (the P121 v1 witness the same!) + Johan Kambič (} ½ gbl.); priest Jos. Rauy; Befünden: the certificate of the Griblje commune from Jul 13, 1893 + the dispensation №1661 + the verbal consent for the minor bride",
    status: "DOCUMENTED",
  },
  {
    houseNo: "74",
    bookSignature: "04455",
    year: 1893,
    scan: 89,
    page: 88,
    whatSi: "poroka (23. 7. 1893, vpis 16) — nevesta Catharina KAMBIČ, ¼ Griblers=tochft, 22 (mladoletna), GRIBLJE 74 (NOVA hiša poročnega vzorca; krstna 1893 + 1911 = poročna-krstna sovpadnost isto leto!) × Johann POŽEK, ¼ Gribler, 36, GRIBLJE 58 (drubel poroka!); oče Mathias Kambič ¼ Gribler × Catharina BRINEC (mati = Brinc → dispens 3. stopnje №1661!); KAMBIČ ×5 1893 = najmočnejši priimek (v2 priča + v3 nevesta + v13 ženin + v16 + v19); duhovnik Jos. Rauy",
    whatEn: "marriage (Jul 23, 1893, entry 16) — bride Catharina KAMBIČ, quarter smallholder's daughter, 22 (a minor), GRIBLJE 74 (A NEW house of the marriage sample; the baptisms 1893 + 1911 = the marriage-baptism coincidence in the same year!) × Johann POŽEK, quarter smallholder, 36, GRIBLJE 58 (the double-Griblje marriage!); father Mathias Kambič quarter smallholder × Catharina BRINEC (the mother = Brinc → the 3rd-degree dispensation №1661!); KAMBIČ ×5 in 1893 = the strongest surname (the v2 witness + v3 bride + v13 groom + v16 + v19)",
    status: "DOCUMENTED",
  },
  // ——— P121 razširitev: POROČNA KNJIGA 04455 — polno leto 1892 (skeni 84–86 ==
  // strani 83–85; VELIKA GLAVA »Traunungs=Buch« 1892 na s84 = Pag. 83 POTRJENA!
  // 15 vpisov: 1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 →
  // 1892:15 = 6+4+5) — vpisi z Griblji (3 poroke / 4 poročna bloka: h60 v1
  // 2. DOKAZ po 1886 + h49 dokumentiran + h30 v5 nevesta + h17 v10 NOVA +
  // h34 dokumentiran + h36 v15 + h44 NOVA dokumentirana): NOVELE: DRUBEL-
  // GRIBLJE poroke ×3 = REKORD LINIJE! + deležni sistem ¼/½/¾ ×21 oseb = rekord
  // (¾ prvič!) + Griblers=Sohn/Tochter ROSETTA ×9 + 1. AMERIŠKI KONSULAT
  // (v11 Philadelphia Z:3074!) + 1. KNECHT ×2 (v6+v12) + 1. MUC-priimek z
  // deležem (v12 oče ½ Gribler!) + SESTRSKI DVOZAKON isti dan (v2+v3!) + 4
  // poroke 22.2. = rekord dneva + ženin 56 NOV rekord + nevesta 17 NOV rekord
  // + Wittwen-dispensa Z:9123 (v13) + Laipšl ×5 + BezHauptm. Črnomelj ×3 +
  // Bez. Ger. Möttling (Metlika!) ×2. Dokaz:
  // research/issue17/parish-marriage-1892.json; verifikator:
  // scripts/p121_parish_marriage_1892.py --check (I1–I11).
  {
    houseNo: "60",
    bookSignature: "04455",
    year: 1892,
    scan: 84,
    page: 83,
    whatSi: "poroka (15. 2. 1892, vpis 1) — ženin Nicolaus ŽELJKO, ¼ Gribler, 24, GRIBLJE 60 (2. POROČNI DOKAZ h60 po 1886 v? — ŽELJKO-hiša cf. P120 v6 nevesta Anna h60!; oče Gregor Željko ¼ Gribler × Catharina KRIŽAN) × Maria BRODARIČ, ½ Griblers=tochter [~], 17 = NAJMLAJŠA nevesta linije (NOV rekord mladosti — prej 19!), GRIBLJE 49 (NOVA hiša poročnega vzorca; oče Anton Brodarič ½ Gribler × Barbara POZDIREC = PEZDIREC-pisava!); DRUBEL-GRIBLJE poroka #1 (h60 × h49) = rekord linije!; priče: Nicol. Požek + Josef Dragos (} ½ gbl.); trojni poročni dan 15.2. (v1+v2+v3!); duhovnik Jos. Rauy; Befünden: ženitovanjska zglasnica občine Griblje 14/2. 1892 št: 6 + missigl. Rathsbeschluss f. d. mj. Braut in Gegenwart obigen Befände",
    whatEn: "marriage (Feb 15, 1892, entry 1) — groom Nicolaus ŽELJKO, quarter smallholder, 24, GRIBLJE 60 (the 2nd MARRIAGE EVIDENCE of h60 after 1886 — the ŽELJKO house cf. the P120 v6 bride Anna h60!; father Gregor Željko ¼ Gribler × Catharina KRIŽAN) × Maria BRODARIČ, half smallholder's daughter [~], 17 = THE YOUNGEST BRIDE OF THE LINE (a new youth record — previously 19!), GRIBLJE 49 (A NEW house of the marriage sample; father Anton Brodarič ½ Gribler × Barbara POZDIREC = the PEZDIREC spelling!); the DOUBLE-GRIBLJE marriage #1 (h60 × h49) = the line record!; witnesses: Nicol. Požek + Josef Dragos (} ½ gbl.); the triple wedding day Feb 15 (v1+v2+v3!); priest Jos. Rauy; Befünden: the marriage announcement of the Griblje commune Feb 14, 1892 no. 6 + the minor-bride council consent in the presence of the above findings",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04455",
    year: 1892,
    scan: 84,
    page: 83,
    whatSi: "poroka (22. 2. 1892, vpis 5) — ženin Nicolaus SEGINA, ½ Griblers=[S]ohn [~] (»Jofs«), 33, Trilje 28 (SEGINA-mreža cf. v15 mati Anna Segina!; oče Johann Segina ½ Gribler × Dorothea KRIŽAN) × Margareth MILEK, ¼ Griblerin, 26, GRIBLJE 30 (blok; oče Marcus POZDIREC ½ Gribler = OČE IN PRIČA ISTI MOŽ! × Margarett KLEPEC = h87-Klepec-mreža); priče: Marcus Pozdirec (oče!) + Math. Marasinič (¾ gribler? [~]); k.k. Bez. Hauptmannschaft Črnomelj d.d. 25/1. 1892 Z: 798 (Bescheid!); duhovnik Jos. Rauy; Befünden: ženitovanjska zglasnica občine Griblje 14/2. 1892 št: 7 + bezüglich des Bescheides der k.k. Bez.Hauptmannsch.",
    whatEn: "marriage (Feb 22, 1892, entry 5) — groom Nicolaus SEGINA, half smallholder's son [~], 33, Trilje 28 (the SEGINA network cf. the v15 bride-mother Anna Segina!; father Johann Segina ½ Gribler × Dorothea KRIŽAN) × Margareth MILEK, quarter smallholder's daughter, 26, GRIBLJE 30 (block; father Marcus POZDIREC ½ Gribler = THE FATHER AND WITNESS THE SAME MAN! × Margarett KLEPEC = the h87-Klepec network); witnesses: Marcus Pozdirec (the father!) + Math. Marasinič (¾ gribler? [~]); the k.k. Bez. Hauptmannschaft Črnomelj Jan 25, 1892 Z: 798 (the official decision!); priest Jos. Rauy; Befünden: the marriage announcement of the Griblje commune Feb 14, 1892 no. 7 + regarding the decision of the k.k. district headquarters",
    status: "DOCUMENTED",
  },
  {
    houseNo: "17",
    bookSignature: "04455",
    year: 1892,
    scan: 85,
    page: 84,
    whatSi: "poroka (18. 9. 1892, vpis 10) — ženin Johann KRALJ, ¼ Gribler, 48, GRIBLJE 17 (NOVA HIŠA — 1. poročni dokaz sploh!; oče Johann Kralj ¼ Gribler × Margareth JAKŠA; KRALJ ×2 v letu cf. v6!) × Dorothea FILAK, ¼ Griblers=todter + Ans [~], 24, GRIBLJE 34 (oče Johann FILAK ½ Gribler × Anna Deblinč? [~] — 1. FILAK poročni dokazi; v6 priča Matthias Filak — brat?); DRUBEL-GRIBLJE poroka #2 (h17 × h34)!; najstarejši ženin 1892 (48); priče: Nicol. Požek (v1 isti!) + Georg Kralj (} ½ gbl.); duhovnik Jos. Rauy; Befünden: ženitov. zglasmica občine Griblje-vke 18. 9. 1892 št: 2",
    whatEn: "marriage (Sep 18, 1892, entry 10) — groom Johann KRALJ, quarter smallholder, 48, GRIBLJE 17 (A NEW HOUSE — the 1st marriage evidence ever!; father Johann Kralj ¼ Gribler × Margareth JAKŠA; KRALJ ×2 in the year cf. v6!) × Dorothea FILAK, quarter smallholder's daughter + Ans [~], 24, GRIBLJE 34 (father Johann FILAK ½ Gribler × Anna Deblinč? [~] — the 1st FILAK marriage evidences; the v6 witness Matthias Filak — a brother?); the DOUBLE-GRIBLJE marriage #2 (h17 × h34)!; the oldest groom of 1892 (48); witnesses: Nicol. Požek (the same as v1!) + Georg Kralj (} ½ gbl.); priest Jos. Rauy; Befünden: the marriage announcement of the Griblje-vke commune Sep 18, 1892 no. 2",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04455",
    year: 1892,
    scan: 86,
    page: 85,
    whatSi: "poroka (21. 11. 1892, vpis 15) — ženin Johann KRIŽAN, ¼ Gribler, 31, GRIBLJE 36 (blok; h36 krstna 1882/1886/1887-mreža!; oče Marcus Križan ¼ Gribler × Anna SEGINA — SEGINA ×2 cf. v5!) × Catharina STRUNCELJ [~], ½ Griblers=Tochter, 18 (mladoletna — mj. Braut!), GRIBLJE 44 (NOVA hiša poročnega vzorca; oče Mathias Struncelj ½ Gribler × Agnes KLOBUČAR = v6 mati-mreža!); DRUBEL-GRIBLJE poroka #3 (h36 × h44) = 3. drubel poroka v enem letu = REKORD LINIJE!; KRIŽAN ×3 v letu (v1 mati + v2 + ženin!); priče: Nic. Klepec (½ gbl.) + Marcus Klobučar (¼ gribler); duhovnik Jos. Rauy; Befünden: ženitovanjska zglasnica občine Griblje 21. 11. 1892 št: 2 + Rathsbeschluss f. d. mj. Braut",
    whatEn: "marriage (Nov 21, 1892, entry 15) — groom Johann KRIŽAN, quarter smallholder, 31, GRIBLJE 36 (block; the h36 baptism 1882/1886/1887 network!; father Marcus Križan ¼ Gribler × Anna SEGINA — SEGINA ×2 cf. v5!) × Catharina STRUNCELJ [~], half smallholder's daughter, 18 (a minor — the mj. Braut!), GRIBLJE 44 (A NEW house of the marriage sample; father Mathias Struncelj ½ Gribler × Agnes KLOBUČAR = the v6 mother network!); the DOUBLE-GRIBLJE marriage #3 (h36 × h44) = the 3rd double-Griblje marriage in one year = THE LINE RECORD!; KRIŽAN ×3 in the year (the v1 mother + v2 + the groom!); witnesses: Nic. Klepec (½ gbl.) + Marcus Klobučar (¼ gribler); priest Jos. Rauy; Befünden: the marriage announcement of the Griblje commune Nov 21, 1892 no. 2 + the council consent for the minor bride",
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
  // ——— P83 razširitev: KRSTNA KNJIGA 04105 — polno leto 1888 (skeni 27–35 ==
  // strani 26–34; prelom 1888 na str. 26 po row 106, prelom 1889 »1 8 8 9« na
  // str. 34 row 1; PISANE OZNAKE VRSTIC SE PRI PRELOMU LETA PONASTAVIJO NA 1 —
  // str. 27 se začne z oznako 3, P82 »row 107« = zvezno štetje 106+1) — vsi
  // vpisi z Griblji (15; 3 nezakonski; PT luknja 41–60 potrjena 44/56/57) ———
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1888,
    scan: 28,
    page: 27,
    whatSi: "krščen Anton (16./17. 1.) — oče Nikolaj Zeljth [~] ½ zemljišt, mati Katarina Kure [~]; botra Jurij Zeljth + Katarina Kure [~]; marginalija »+ 1878« [~] (7/8 forenzika)",
    whatEn: "baptized Anton (Jan 16/17) — father Nikolaj Zeljth [~] half-farmer, mother Katarina Kure [~]; godparents Jurij Zeljth + Katarina Kure [~]; margin note »+ 1878« [~] (7/8 forensics)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1888,
    scan: 28,
    page: 27,
    whatSi: "krščena Marija (31. 1.) — oče Matija Strauš [~] ½ zemljišt (P84 re-read: prej »Hraus«), mati Barbara Husič [~]; babica Neža Straucelj [~]; + 3. 9. 1888; Strauš JE v vesolju 1825 (P81 0.8571)",
    whatEn: "baptized Marija (Jan 31) — father Matija Strauš [~] half-farmer (P84 re-read: earlier read »Hraus«), mother Barbara Husič [~]; midwife Neža Straucelj [~]; died Sep 3, 1888; Strauš IS in the 1825 universe (P81 0.8571)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1888,
    scan: 28,
    page: 27,
    whatSi: "krščena Katarina (23./24. 2.) — oče Matija Hlevič [~] ¼ zemljišt, mati Nera Hlevič [~]; hiša 44 v PT luknji 41–60 (P80 sidro 1887 — potrditev)",
    whatEn: "baptized Katarina (Feb 23/24) — father Matija Hlevič [~] quarter-farmer, mother Nera Hlevič [~]; house 44 in the PT 41–60 gap (the P80 anchor 1887 — confirmation)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1888,
    scan: 28,
    page: 27,
    whatSi: "krščena Marija (28. 2.) — oče Janez Brinec [~] ½ zemljišt, mati Katarina Strauš [~] (P84 re-read: prej »Hraus«); botra Marko Križan [~] + Marija Adlešič [~]",
    whatEn: "baptized Marija (Feb 28) — father Janez Brinec [~] half-farmer, mother Katarina Strauš [~] (P84 re-read: earlier read »Hraus«); godparents Marko Križan [~] + Marija Adlešič [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "57",
    bookSignature: "04105",
    year: 1888,
    scan: 29,
    page: 28,
    whatSi: "krščena Marija (29. 2.) — oče Peter Pezdirec [~] ¼ zemljišt, mati Marija Borjanc [~]; hiša 57 v PT luknji 41–60 (P79 1886 Podolivec/Stupanič — menjava družine)",
    whatEn: "baptized Marija (Feb 29) — father Peter Pezdirec [~] quarter-farmer, mother Marija Borjanc [~]; house 57 in the PT 41–60 gap (P79 1886 Podolivec/Stupanič — a family change)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "78",
    bookSignature: "04105",
    year: 1888,
    scan: 29,
    page: 28,
    whatSi: "krščena Jozefa (29. 3.) — oče Mihail Poxan [~] — OSKRBAR (opomba o prevzemu [~]), mati Barbara Hardeium [~]; hiša 78 [~] (v zavihku; 1886/1887 Jakobič → 1888 oskrbar Poxan)",
    whatEn: "baptized Jozefa (Mar 29) — father Mihail Poxan [~] — the CARETAKER (oskrbar, a takeover note [~]), mother Barbara Hardeium [~]; house 78 [~] (in the gutter; 1886/1887 Jakobič → 1888 caretaker Poxan)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "83",
    bookSignature: "04105",
    year: 1888,
    scan: 29,
    page: 28,
    whatSi: "krščena Marija (18. 4.) — oče Jurij Radovič [~] Mrgaič [~] (dvodelni priimek), mati Katarina Mettovič [~]; botra prazna; + 1. 7. 1889; hiša 83 NOVA",
    whatEn: "baptized Marija (Apr 18) — father Jurij Radovič [~] Mrgaič [~] (a double surname), mother Katarina Mettovič [~]; godparents EMPTY; died Jul 1, 1889; house 83 NEW",
    status: "DOCUMENTED",
  },
  {
    houseNo: "79",
    bookSignature: "04105",
    year: 1888,
    scan: 30,
    page: 29,
    whatSi: "krščena Barbara (11./12. 5.) — oče Jurij Požek [~] bajtar, mati Katarina Križan [~]; botra Anton Kure [~] + Barbara Požek [~]; hiša 79 NOVA; Požek NI v vesolju 1825",
    whatEn: "baptized Barbara (May 11/12) — father Jurij Požek [~] cottager, mother Katarina Križan [~]; godparents Anton Kure [~] + Barbara Požek [~]; house 79 NEW; Požek NOT in the 1825 universe",
    status: "DOCUMENTED",
  },
  {
    houseNo: "85",
    bookSignature: "04105",
    year: 1888,
    scan: 30,
    page: 29,
    whatSi: "krščen Janez (21. 5.) — oče Marko Križan [~] ½ zemljišt, mati Marija Strauš [~] (P84 re-read: prej »Hraus«); botra Matija Urh [~] + Ana Brinec [~]; hiša 85 NOVA; + 9. 12. 1889 [~]",
    whatEn: "baptized Janez (May 21) — father Marko Križan [~] half-farmer, mother Marija Strauš [~] (P84 re-read: earlier read »Hraus«); godparents Matija Urh [~] + Ana Brinec [~]; house 85 NEW; died Dec 9, 1889 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1888,
    scan: 30,
    page: 29,
    whatSi: "krščena Musca [~] (2./3. 6.) — očeta stolpec PRAZEN (nezakonska), mati Barbara Melith [~] — samata, ¼ zemljatka; babica Marija Križan [~] (zapis prečrtan)",
    whatEn: "baptized Musca [~] (Jun 2/3) — father's column EMPTY (illegitimate), mother Barbara Melith [~] — unmarried, quarter smallholder; midwife Marija Križan [~] (a struck-through entry)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "56",
    bookSignature: "04105",
    year: 1888,
    scan: 31,
    page: 30,
    whatSi: "krščen Alex [~] (27./28. 6.) — očeta stolpec PRAZEN (nezakonski), mati Ana Šimec [~] — samostojna, ½ zemlj. nova hiča; hiša 56 v PT luknji; marginalija »Umrla 25. 5. 1965« [~] proti kolonam moški [~] — nasprotje",
    whatEn: "baptized Alex [~] (Jun 27/28) — father's column EMPTY (illegitimate), mother Ana Šimec [~] — unmarried, half smallholder of the new cottage; house 56 in the PT gap; the margin note »Umrla May 25, 1965« [~] against the male columns [~] — a contradiction",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1888,
    scan: 31,
    page: 30,
    whatSi: "krščena Barbara (2. 6.) — oče Matija Jakobič [~] ½ zemljišt, mati Marija Perdinec [~]; TRI-VIRSKA hiša (1885 poročna + 1886 krst/mrliška + 1888 krst) — Jakobič/Jakopič čez leta: prva per-hišna imenska veriga",
    whatEn: "baptized Barbara (Jun 2) — father Matija Jakobič [~] half-farmer, mother Marija Perdinec [~]; the THREE-SOURCE house (1885 marriage + 1886 baptism/death + 1888 baptism) — Jakobič/Jakopič across years: the first per-house name chain",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1888,
    scan: 33,
    page: 32,
    whatSi: "krščen »Kaxmarp« [~] (9./11. 9.; morda Kasimir [~]) — očeta stolpec PRAZEN (nezakonski), mati Marija Požek [~] — samata, ¼ zemljatka (1887 oče Janez Požek — isti priimek)",
    whatEn: "baptized »Kaxmarp« [~] (Sep 9/11; possibly Kasimir [~]) — father's column EMPTY (illegitimate), mother Marija Požek [~] — unmarried, quarter smallholder (the 1887 house father was Janez Požek — the same surname)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04105",
    year: 1888,
    scan: 33,
    page: 32,
    whatSi: "krščen Martin (20. 10.) — oče Jang [~] Jatkebčič [~] ½ zemljišt, mati Marija Urh [~]; + 29. 10. 1888 (9 dni); hiša 8 NOVA (1886 Jakofčič/Meh — menjava)",
    whatEn: "baptized Martin (Oct 20) — father Jang [~] Jatkebčič [~] half-farmer, mother Marija Urh [~]; died Oct 29, 1888 (9 days); house 8 NEW (1886 Jakofčič/Meh — a family change)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04105",
    year: 1888,
    scan: 34,
    page: 33,
    whatSi: "krščena Marjeta (4. 11.) — oče Peter Milek [~] ½ zemljišt, mati Ana Križan [~]; hiša epidemije 1886 (Mileh ×3) → 1888 Milek — isti rod; poročena 7. 2. 1914 [~]",
    whatEn: "baptized Marjeta (Nov 4) — father Peter Milek [~] half-farmer, mother Ana Križan [~]; the 1886 epidemic house (Mileh ×3) → 1888 Milek — the same kin; married Feb 7, 1914 [~]",
    status: "DOCUMENTED",
  },
  // ——— P84 razširitev: KRSTNA KNJIGA 04105 — polno leto 1889 (skeni 35–43 ==
  // strani 34–42; prelom 1889 na str. 34 row 1, prelom 1890 »Leto 1890« na
  // str. 42 row 1; 1889 ima 106 zveznih vrstic) — NOVELI P84: ① ŠTEVILČENJE
  // STR. 40 — duhovnikove oznake PONOVLJENE 68–8x, modri svinčnik popravi
  // zvezno 81–93 (str. 41 zvezno 94–106 — neodvisna potrditev); ② RE-READ
  // P83 — »HRAUS/HRAUCELJ« = STRAUŠ/STRAUCELJ (Kurrent ſt brana kot H;
  // familija JE v vesolju 1825, P81 0.8571) — P83 vpisi zgoraj popavljeni
  // vidno — vpisi z Griblji (19; 1 nezakonski + 1 anomalija; 2 neberljive
  // hišne št. — evidence-only; PT luknja: 58 NOVA, 59/57 potrditvi) ———
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1889,
    scan: 35,
    page: 34,
    whatSi: "krščen Anton (4. 1.) — oče Franz Požek [~] ¼ zemljišč, mati Ana Dragoš [~]; hiša 58 NOVA luknjana št.; botra Matija Strauš [~] + Ana Podirec [~]; babica Marjeta Sotter [~]; + 14. 9. 1893 [~]",
    whatEn: "baptized Anton (Jan 4) — father Franz Požek [~] quarter smallholder, mother Ana Dragoš [~]; house 58 NEW gap number; godparents Matija Strauš [~] + Ana Podirec [~]; midwife Marjeta Sotter [~]; died Sep 14, 1893 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04105",
    year: 1889,
    scan: 36,
    page: 35,
    whatSi: "krščena Marija (21. 2.) — oče Matija Brinec [~] ¼ zemljak, mati Marija Dolenc [~]; hiša 33 NOVA; botra Peter Podirec [~] + Marija Jakljič? [~]; babica Marija Brinec; + 8. 11. 1897 [~]",
    whatEn: "baptized Marija (Feb 21) — father Matija Brinec [~] quarter smallholder, mother Marija Dolenc [~]; house 33 NEW; godparents Peter Podirec [~] + Marija Jakljič? [~]; midwife Marija Brinec; died Nov 8, 1897 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04105",
    year: 1889,
    scan: 36,
    page: 35,
    whatSi: "krščen Jožef (22./23. 2.) — oče Nikolaj Županič? [~] ¼ zemljišt, mati Katarina Pezdirec [~]; hiša 3 [~] (dvoumni zapis »mölüo?/3« + »Tomma Vrh'möz«); botra Oskar Cojmar? [~] + Haken Strašimiö? [~]; babica Marija Brinec; pok. 15. 5. 1921 [~]",
    whatEn: "baptized Jožef (Feb 22/23) — father Nikolaj Županič? [~] quarter smallholder, mother Katarina Pezdirec [~]; house 3 [~] (ambiguous record); godparents Oskar Cojmar? [~] + Haken Strašimiö? [~]; midwife Marija Brinec; buried May 15, 1921 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "64",
    bookSignature: "04105",
    year: 1889,
    scan: 36,
    page: 35,
    whatSi: "krščena Doroteja (26. 2.) — oče Anton Kern? [~] ¼ zemljak, mati Barbara Tržan [~]; hiša 64 NOVA (= ATLAS 1825 Šimec @64); botra Matija Milek [~] + Marjeta Pezdirec [~]; babica Katarina Tržan; umrla 21. 7. 1964",
    whatEn: "baptized Doroteja (Feb 26) — father Anton Kern? [~] quarter smallholder, mother Barbara Tržan [~]; house 64 NEW (= the 1825 ATLAS Šimec @64); godparents Matija Milek [~] + Marjeta Pezdirec [~]; midwife Katarina Tržan; died Jul 21, 1964",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04105",
    year: 1889,
    scan: 36,
    page: 35,
    whatSi: "krščena Marija (27./28. 2.) — oče Janez Jatkobič? [~] ¼ zemlj.at., mati Marija Hrušljar? [~]; botra Matija Jakobič [~] (veriga h13) + Barbara Brinec [~]; babica Katarina Brinec; pok. 10. 4. 1921, + 15. 3. 1940",
    whatEn: "baptized Marija (Feb 27/28) — father Janez Jatkobič? [~] quarter smallholder, mother Marija Hrušljar? [~]; godparents Matija Jakobič [~] (the h13 chain) + Barbara Brinec [~]; midwife Katarina Brinec; buried Apr 10, 1921, died Mar 15, 1940",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1889,
    scan: 36,
    page: 35,
    whatSi: "krščen Janez (1./2. 4.) — oče Janez Brinec [~] ¼ zemljišt, mati Barbara Strauš [~]; botra Jurij Strauš [~] + Marija Hengan? [~]; babica Marjeta Sotter [~]; isti oče kot 1888 (P83)",
    whatEn: "baptized Janez (Apr 1/2) — father Janez Brinec [~] quarter smallholder, mother Barbara Strauš [~]; godparents Jurij Strauš [~] + Marija Hengan? [~]; midwife Marjeta Sotter [~]; the same father as 1888 (P83)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "59",
    bookSignature: "04105",
    year: 1889,
    scan: 37,
    page: 36,
    whatSi: "krščena Marinka (21. 4.) — očeta stolpec PRAZEN (nezakonska), mati Katarina Podirec [~] (»a samka?«); hiša 59 [~] (potrditev P80); botra Nikolaj Cetro? [~] + Ana Podirec [~]; babica Marija Brinec; Marinče 26. 4. 1957 [~]",
    whatEn: "baptized Marinka (Apr 21) — father's column EMPTY (illegitimate), mother Katarina Podirec [~] (»a samka?«); house 59 [~] (confirms P80); godparents Nikolaj Cetro? [~] + Ana Podirec [~]; midwife Marija Brinec; Marinče Apr 26, 1957 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1889,
    scan: 38,
    page: 37,
    whatSi: "krščena Barbara (20. 6.) — oče Hrigian? [~] (ali Hrižan) ¼ zemlj.at., mati Katarina Pezdirec [~]; SIDRO hiša 63 = ATLAS 1825 Šimec @63 (PT lastnik »Šimec Ripane«), botr Janez Šimec [~]; babica Marija Brinec; + 16. 4. 1912",
    whatEn: "baptized Barbara (Jun 20) — father Hrigian? [~] (or Hrižan) quarter smallholder, mother Katarina Pezdirec [~]; ANCHOR house 63 = the 1825 ATLAS Šimec @63 (the PT owner »Šimec Ripane«), godfather Janez Šimec [~]; midwife Marija Brinec; died Apr 16, 1912",
    status: "DOCUMENTED",
  },
  {
    houseNo: "57",
    bookSignature: "04105",
    year: 1889,
    scan: 39,
    page: 38,
    whatSi: "krščen Rudolf (2. 7.) — oče Peter Pezdirec [~] ⅛ zemljak, mati Marija Županič [~]; hiša 57 (luknja, potrditev P79); botra Jurij Brodarič [~] + Marija Straucelj [~] (re-read: 1888 »Hraucelj«); babica Marija Brinec; + 24. 7. 1892",
    whatEn: "baptized Rudolf (Jul 2) — father Peter Pezdirec [~] one-eighth smallholder, mother Marija Županič [~]; house 57 (gap, confirms P79); godparents Jurij Brodarič [~] + Marija Straucelj [~] (re-read: 1888 »Hraucelj«); midwife Marija Brinec; died Jul 24, 1892",
    status: "DOCUMENTED",
  },
  {
    houseNo: "64",
    bookSignature: "04105",
    year: 1889,
    scan: 39,
    page: 38,
    whatSi: "krščena Marjeta (13./14. 7.) — oče Janez Vehbiščar? [~] ⅛ zemljat., mati Marjeta Klepec [~]; hiša 64 (2. vpis 1889 — multi-vpisna); botra Martin Papič [~] mizar + Barbara Klepec [~]; babica Marija Brinec",
    whatEn: "baptized Marjeta (Jul 13/14) — father Janez Vehbiščar? [~] one-eighth smallholder, mother Marjeta Klepec [~]; house 64 (2nd 1889 entry — the multi-entry house); godparents Martin Papič [~] joiner + Barbara Klepec [~]; midwife Marija Brinec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1889,
    scan: 39,
    page: 38,
    whatSi: "krščena Ana (17./18. 7.) — oče Matija Urh [~] ¼ zemljat., mati Marjeta Pezdirec [~]; hiša 32 NOVA; botra Peter Pezdirec [~] + Barbara Strauš [~]; babica Ana Hrižan [~] (Griblje 63)",
    whatEn: "baptized Ana (Jul 17/18) — father Matija Urh [~] quarter smallholder, mother Marjeta Pezdirec [~]; house 32 NEW; godparents Peter Pezdirec [~] + Barbara Strauš [~]; midwife Ana Hrižan [~] (Griblje 63)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1889,
    scan: 39,
    page: 38,
    whatSi: "krščena Marija (22. 7.) — oče Matija Strauš [~] ¼ zemljat. (re-read P83: 1888 »Hraus« = isti oče), mati Marija Jakobič? [~]; botra Matija Bahorič? [~] + Neža Straucelj [~]; babica Ana Hrižan [~]; + 22. 3. 1890",
    whatEn: "baptized Marija (Jul 22) — father Matija Strauš [~] quarter smallholder (P84 re-read: 1888 »Hraus« = the same father), mother Marija Jakobič? [~]; godparents Matija Bahorič? [~] + Neža Straucelj [~]; midwife Ana Hrižan [~]; died Mar 22, 1890",
    status: "DOCUMENTED",
  },
  {
    houseNo: "2",
    bookSignature: "04105",
    year: 1889,
    scan: 40,
    page: 39,
    whatSi: "krščena Marija (28. 8.) — oče Peter Hlebec [~] ¼ zemljak, mati Ana Jakobič? [~]; hiša 2 (ponovitev P82); botra Janez Klobučar [~] + Katarina Šimec? [~]; babica —; umrla 5. 3. 1975",
    whatEn: "baptized Marija (Aug 28) — father Peter Hlebec [~] quarter smallholder, mother Ana Jakobič? [~]; house 2 (repeat of P82); godparents Janez Klobučar [~] + Katarina Šimec? [~]; midwife —; died Mar 5, 1975",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04105",
    year: 1889,
    scan: 41,
    page: 40,
    whatSi: "krščen Janez (26. 10.) — oče Anton Jakobič? [~] ¼ zemljat., mati Marija Urh [~] (ista mati kot 1888 h8); hiša 8 [~]; SIDRO botr Janez Dragoš [~] (P81 1.0) + Katarina Klobučar [~]; babica Ana Hrižan [~]; umrl 11. 12. 1969",
    whatEn: "baptized Janez (Oct 26) — father Anton Jakobič? [~] quarter smallholder, mother Marija Urh [~] (the same mother as 1888 h8); house 8 [~]; ANCHOR godfather Janez Dragoš [~] (P81 1.0) + Katarina Klobučar [~]; midwife Ana Hrižan [~]; died Dec 11, 1969",
    status: "DOCUMENTED",
  },
  {
    houseNo: "83",
    bookSignature: "04105",
    year: 1889,
    scan: 41,
    page: 40,
    whatSi: "krščena Barbara (november, datum pod trakom [~]) — oče [?] Radovič [~] (»m čuvžar?«), mati Katarina Milkovič [~]; hiša 83 [~] (Radovič 2. leto — vzporednica P83); botra —; babica Ana Hrižan [~]",
    whatEn: "baptized Barbara (November, date under tape [~]) — father [?] Radovič [~] (»m čuvžar?«), mother Katarina Milkovič [~]; house 83 [~] (Radovič 2nd year — parallels P83); godparents —; midwife Ana Hrižan [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1889,
    scan: 42,
    page: 41,
    whatSi: "krščena Barbara (23. 11.) — oče Matija Milek [~] ¼ zemljak, mati Katarina Trojžif? [~]; hiša 65 (ponovitev P82); botra Janez Adlešič [~] + Katarina Podirec [~]; babica —; + 6. 12. 1897",
    whatEn: "baptized Barbara (Nov 23) — father Matija Milek [~] quarter smallholder, mother Katarina Trojžif? [~]; house 65 (repeat of P82); godparents Janez Adlešič [~] + Katarina Podirec [~]; midwife —; died Dec 6, 1897",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04105",
    year: 1889,
    scan: 42,
    page: 41,
    whatSi: "krščen Janez (16. 12.) — oče Jurij Brinec [~] ¼ zemljak, mati Katarina Jakobič? [~]; hiša 26 [~] (potrditev P82); botra Peter Jakobič? [~] + Katarina Podirec [~]; babica —; zadnji 1889 vpis (106. vrstica)",
    whatEn: "baptized Janez (Dec 16) — father Jurij Brinec [~] quarter smallholder, mother Katarina Jakobič? [~]; house 26 [~] (confirms P82); godparents Peter Jakobič? [~] + Katarina Podirec [~]; midwife —; the last 1889 entry (row 106)",
    status: "DOCUMENTED",
  },
  // ——— P85 razširitev: KRSTNA KNJIGA 04105 — polno leto 1890 (skeni 43–49 ==
  // strani 42–48; prelom 1891 »1891.« na str. 48 row 1 po row 86; leto 1890
  // ima 86 zveznih vrstic) — NOVELA P85: STATUS = ULOMEK (Kurrent znak pred
  // »zemljak«, P79–P84 brana »ž«, je z jasnimi izrezi 1890 ulomek ½/¼ —
  // 15/24 vpisov) — vpisi z Griblji (24; 0 nezakonskih, 2 anomaliji z
  // ženskim imenom v očetovem stolpcu r19/r85 — r85 = čez-letna potrditev
  // P82 row 93 na hiši 35; prvi dvojčki v vzorcu r51/r52 h30; 3 neberljive
  // hišne št. — evidence-only; PT luknja: 41 NOVA (2 vpisa), 47/55/58
  // potrditvi) ———
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1890,
    scan: 43,
    page: 42,
    whatSi: "krščen Anton (6./7. 1.) — oče Janez Stubhar [~] ½ zemljak (RE-READ P84 okvir: prej »Kukhar«), mati Katarina Klobučar [~]; prvi 1890 Griblje vpis; hiša 27 (ponovitev P82); botra Janez Pojžef [~] + Ana Tiurc [~]; babica Marija Brinec; + 12. 12. 1908 [~]",
    whatEn: "baptized Anton (Jan 6/7) — father Janez Stubhar [~] half smallholder (P84 frame RE-READ: earlier »Kukhar«), mother Katarina Klobučar [~]; the first 1890 Griblje entry; house 27 (repeat of P82); godparents Janez Pojžef [~] + Ana Tiurc [~]; midwife Marija Brinec; died Dec 12, 1908 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1890,
    scan: 44,
    page: 43,
    whatSi: "krščen Jožef (roj. 5. 2., krst nevpisan [~]) — oče Martin Papič [~] ½ zemljak, mati Marjeta Straus [~] (P81 0.8571); hiša 31 (ponovitev P80/P82); botra PRAZNA (—); babica Marija Brinec; + 6. 2. 1890",
    whatEn: "baptized Jožef (born Feb 5, baptism date unwritten [~]) — father Martin Papič [~] half smallholder, mother Marjeta Straus [~] (P81 0.8571); house 31 (repeat of P80/P82); godparents EMPTY (—); midwife Marija Brinec; died Feb 6, 1890",
    status: "DOCUMENTED",
  },
  {
    houseNo: "47",
    bookSignature: "04105",
    year: 1890,
    scan: 44,
    page: 43,
    whatSi: "krščen Matija (6./7. 2.) — oče Peter Klobučar [~] ¼ zemljak [~], mati Marija Filak [~] (P81 1.0); hiša 47 = luknja POTRDITEV (P82; forenzika 4+7 = ni 8); botra Janez Lazič [~] + Marija Straus [~]; babica Marija Brinec",
    whatEn: "baptized Matija (Feb 6/7) — father Peter Klobučar [~] quarter smallholder [~], mother Marija Filak [~] (P81 1.0); house 47 = gap CONFIRMATION (P82; forensics 4+7 = not 8); godparents Janez Lazič [~] + Marija Straus [~]; midwife Marija Brinec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1890,
    scan: 44,
    page: 43,
    whatSi: "krščen Anton (21./21. 2.) — očetov stolpec »Marija Brinec [~] ½ zemljak« ANOMALIJA (žensko ime; vzporednica P82 row 93), mati Barbara Jakofčič [~]; hiša 24 (ponovitev P82/P83); botra Peter Pendirec [~] + Marija Butala [~]; babica Marija Brinec; + 29. 10. 1891",
    whatEn: "baptized Anton (Feb 21/21) — father column »Marija Brinec [~] half smallholder« ANOMALY (a female name; parallels P82 row 93), mother Barbara Jakofčič [~]; house 24 (repeat of P82/P83); godparents Peter Pendirec [~] + Marija Butala [~]; midwife Marija Brinec; died Oct 29, 1891",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1890,
    scan: 44,
    page: 43,
    whatSi: "krščen Jožef (6./6. 3.) — oče Janez Pošek/Požek [~] ½ zemljak, mati Ana Dragoš [~] (P81 1.0, 3. leto); hiša 58 = luknja POTRDITEV (P84 — ista hiša kot Franz Požek 1889); botra Marko Straus [~] + Ana Pendirec [~]; babica Marija Brinec",
    whatEn: "baptized Jožef (Mar 6/6) — father Janez Pošek/Požek [~] half smallholder, mother Ana Dragoš [~] (P81 1.0, 3rd year); house 58 = gap CONFIRMATION (P84 — the same house as Franz Požek 1889); godparents Marko Straus [~] + Ana Pendirec [~]; midwife Marija Brinec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04105",
    year: 1890,
    scan: 44,
    page: 43,
    whatSi: "krščena Marija (7./8. 3.) — oče Jurij Straus [~] ½ zemljak (h71 = tri-virska P80 + PUA Strauß Niklo @71, P81 0.8571 — 1890 živ oče), mati Barbara Jakobčič [~]; botra Janez Štralj [~] + Marjeta Urh [~]; babica Marija Brinec",
    whatEn: "baptized Marija (Mar 7/8) — father Jurij Straus [~] half smallholder (h71 = the three-source P80 house + PUA Strauß Niklo @71, P81 0.8571 — a living father in 1890), mother Barbara Jakobčič [~]; godparents Janez Štralj [~] + Marjeta Urh [~]; midwife Marija Brinec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "38",
    bookSignature: "04105",
    year: 1890,
    scan: 46,
    page: 45,
    whatSi: "krščen Anton (5./5. 5.) — oče Miha Lozar [~] ČEVLJAR (prvi obrtnik v vzorcu), mati Barbara Harasimč [~]; hiša 38 NOVA (ATLAS 1825 Šimer @38); botra Anton Brodarič [~] + Barbara Klobučar [~]; babica Marija Brinec; podpis C. g. Jurcan Šašelj, župr v D. Lazič [~]",
    whatEn: "baptized Anton (May 5/5) — father Miha Lozar [~] SHOEMAKER (the first craftsman in the sample), mother Barbara Harasimč [~]; house 38 NEW (the 1825 ATLAS Šimer @38); godparents Anton Brodarič [~] + Barbara Klobučar [~]; midwife Marija Brinec; signed C. g. Jurcan Šašelj, priest in D. Lazič [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04105",
    year: 1890,
    scan: 46,
    page: 45,
    whatSi: "krščen Anton (19./19. 5.) — oče Janez Jakflevič [~] ½ zemljak, mati Marija Brinec [~]; hiša 15 (ponovitev P80); botra Marko Klobučar [~] + Marija Adlešič [~]; babica Marija Brinec (mati in babica isti priimek)",
    whatEn: "baptized Anton (May 19/19) — father Janez Jakflevič [~] half smallholder, mother Marija Brinec [~]; house 15 (repeat of P80); godparents Marko Klobučar [~] + Marija Adlešič [~]; midwife Marija Brinec (mother and midwife the same surname)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "77",
    bookSignature: "04105",
    year: 1890,
    scan: 46,
    page: 45,
    whatSi: "krščen Peter (22./22. 5.) — oče Jurij Pošek/Požek [~] BAJTAR (= P83 sidro h79 oče 1888!), mati Katarina Šotter roj. Križan [~] (P81 0.8333 [~]); hiša 77 NOVA (forenzika: dve 7 = ni 9); botra Jurij Šimec [~] (P81 1.0) + Barbara Požek [~] (= P83 h79 botra); babica Marija Brinec",
    whatEn: "baptized Peter (May 22/22) — father Jurij Pošek/Požek [~] cottager (= the P83 h79 anchor father of 1888!), mother Katarina Šotter née Križan [~] (P81 0.8333 [~]); house 77 NEW (forensics: two 7s = not 9); godparents Jurij Šimec [~] (P81 1.0) + Barbara Požek [~] (= the P83 h79 godmother); midwife Marija Brinec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1890,
    scan: 46,
    page: 45,
    whatSi: "krščen Janez (13./13. 6.) — DVOJČEK 1/2 — oče Janez Milek [~] ½ zemljak, mati Marjeta Pendirec [~]; hiša 30 NOVA (Milek rod h29 → h30); botra Matija Milek [~] + Katarina Križan [~] (P81 0.8333 [~]); babica Ana Križan [~]; + 2. 6. 1893",
    whatEn: "baptized Janez (Jun 13/13) — TWIN 1/2 — father Janez Milek [~] half smallholder, mother Marjeta Pendirec [~]; house 30 NEW (the Milek kin h29 → h30); godparents Matija Milek [~] + Katarina Križan [~] (P81 0.8333 [~]); midwife Ana Križan [~]; died Jun 2, 1893",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1890,
    scan: 46,
    page: 45,
    whatSi: "krščena Marija (13./13. 6.) — DVOJČEK 2/2 — isti starši kot dvojček 1 (Janez Milek [~] × Marjeta Pendirec [~]); hiša 30; marginalija † 19. 6. 1890 (6 dni); botra/babica po skupni celici (rob strani odrezan) [~]",
    whatEn: "baptized Marija (Jun 13/13) — TWIN 2/2 — the same parents as twin 1 (Janez Milek [~] × Marjeta Pendirec [~]); house 30; margin † Jun 19, 1890 (6 days old); godparents/midwife per the shared cells (page edge cut) [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04105",
    year: 1890,
    scan: 47,
    page: 46,
    whatSi: "krščena Alojzija (/Ana/) (14./15. 6.) — oče Miha Požek [~] MEŽNAR IZ ADLEŠIČ (zunanji), mati Marjeta Šotter [~]; hiša 7 NOVA; botra Janez Duerjm [~] + Marjeta Šotter [~]; babica Marjeta Šotter",
    whatEn: "baptized Alojzija (/Ana/) (Jun 14/15) — father Miha Požek [~] SEXTON FROM ADLEŠIČ (an outsider), mother Marjeta Šotter [~]; house 7 NEW; godparents Janez Duerjm [~] + Marjeta Šotter [~]; midwife Marjeta Šotter",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1890,
    scan: 47,
    page: 46,
    whatSi: "krščena Ana (21./21. 7.) — oče Janez Brinec [~] ½ zemljak, mati Katarina Straus [~] (P81 0.8571); hiša 69 (ponovitev P80/P83; forenzika 6+9 = ni 60); botra Jurij Straus [~] (= oče r23 h71!) + Marija Hrižan [~] (P81 0.8333 [~]); babica Marjeta Šotter",
    whatEn: "baptized Ana (Jul 21/21) — father Janez Brinec [~] half smallholder, mother Katarina Straus [~] (P81 0.8571); house 69 (repeat of P80/P83; forensics 6+9 = not 60); godparents Jurij Straus [~] (= the row-23 h71 father!) + Marija Hrižan [~] (P81 0.8333 [~]); midwife Marjeta Šotter",
    status: "DOCUMENTED",
  },
  {
    houseNo: "55",
    bookSignature: "04105",
    year: 1890,
    scan: 48,
    page: 47,
    whatSi: "krščen Jožef (26./26. 8.) — oče Nikolaj Šimec [~] ½ zemljak [~] (Šimec zdaj tudi na luknji 55 — najtrajnejša familija, 6. hiša), mati Marija Pendirec [~]; hiša 55 = luknja POTRDITEV (P82); botra Nikolaj Požek [~] + Marija Straus [~]; babica Marija Brinec; + 22. 8. 1891",
    whatEn: "baptized Jožef (Aug 26/26) — father Nikolaj Šimec [~] half smallholder [~] (Šimec now also on gap number 55 — the most persistent family, its 6th house), mother Marija Pendirec [~]; house 55 = gap CONFIRMATION (P82); godparents Nikolaj Požek [~] + Marija Straus [~]; midwife Marija Brinec; died Aug 22, 1891",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1890,
    scan: 48,
    page: 47,
    whatSi: "krščen Matija (9./9. 9.) — oče Matija Urh [~] ½ zemljak (Urh veriga 1887/88/89/90), mati Marjeta Pendirec [~]; hiša 32 (ponovitev P80/P84); botra Peter Pendirec [~] + Barbara Straus [~] (P81 0.8571); babica Marija Brinec; + 27. 2. 1909",
    whatEn: "baptized Matija (Sep 9/9) — father Matija Urh [~] half smallholder (the Urh chain 1887/88/89/90), mother Marjeta Pendirec [~]; house 32 (repeat of P80/P84); godparents Peter Pendirec [~] + Barbara Straus [~] (P81 0.8571); midwife Marija Brinec; died Feb 27, 1909",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04105",
    year: 1890,
    scan: 48,
    page: 47,
    whatSi: "krščena Barbara (27./27. 9.) — oče Matija Zumik [~] ½ zemljak, mati Katarina Dragoš [~] (P81 1.0, 2. pojav 1890); hiša 11 (ponovitev P79); botra Peter Klepec [~] + Ana Jakofčič [~]; babica Marjeta Šotter; poročena 1910 v Pittsburgh [~]",
    whatEn: "baptized Barbara (Sep 27/27) — father Matija Zumik [~] half smallholder, mother Katarina Dragoš [~] (P81 1.0, 2nd appearance in 1890); house 11 (repeat of P79); godparents Peter Klepec [~] + Ana Jakofčič [~]; midwife Marjeta Šotter; married 1910 in Pittsburgh [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04105",
    year: 1890,
    scan: 48,
    page: 47,
    whatSi: "krščena Ana (12./13. 10.) — oče Janez Muc [~] BAJTAR, mati Ana Hiše [~]; hiša 41 = PT LUKNJA NOVA (prvi dokaz 41!); botra Nikol Želiško [~] + Katarina Hiše [~]; babica Marija Šotter; modra marginalija »Martin Nomani…« [~]",
    whatEn: "baptized Ana (Oct 12/13) — father Janez Muc [~] cottager, mother Ana Hiše [~]; house 41 = NEW GAP NUMBER (the first evidence of 41!); godparents Nikol Želiško [~] + Katarina Hiše [~]; midwife Marija Šotter; blue margin »Martin Nomani…« [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04105",
    year: 1890,
    scan: 48,
    page: 47,
    whatSi: "krščena Barbara (24./24. 10.) — oče Matija Hrušič [~] ½ zemljak, mati Neža Jakobčič [~]; hiša 41 MULTI-VPISNA (2. vpis istega leta — druga družina kot row 71; vzorec h36/h64); botra Janez Jakobčič [~] + Ana Pendirec [~]; babica Marjeta Šotter; + 19. 8. 1892",
    whatEn: "baptized Barbara (Oct 24/24) — father Matija Hrušič [~] half smallholder, mother Neža Jakobčič [~]; house 41 MULTI-ENTRY (2nd entry the same year — a different family than row 71; the h36/h64 pattern); godparents Janez Jakobčič [~] + Ana Pendirec [~]; midwife Marjeta Šotter; died Aug 19, 1892",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1890,
    scan: 48,
    page: 47,
    whatSi: "krščena Marjeta (5./5. 11.) — oče Nikolaj Križan [~] ½ zemljak (prvi KRIŽAN hišni oče v vzorcu; P81 0.8333 [~]), mati Katarina Pendirec [~]; hiša 63 = P84 Šimec ATLAS sidro (4. gospodinjstvo: Šimec → Križan); botra Marko Pegdirec [~] + Barbara Brodarič [~]; babica Marjeta Pegdirec [~]",
    whatEn: "baptized Marjeta (Nov 5/5) — father Nikolaj Križan [~] half smallholder (the first KRIŽAN house-father in the sample; P81 0.8333 [~]), mother Katarina Pendirec [~]; house 63 = the P84 Šimec ATLAS anchor (the 4th household: Šimec → Križan); godparents Marko Pegdirec [~] + Barbara Brodarič [~]; midwife Marjeta Pegdirec [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1890,
    scan: 49,
    page: 48,
    whatSi: "krščena Elizabeta (16./17. 11.) — oče Franc Kopitar [~] UČITELJ, mati Marija Schweiger [~]; hiša 90 NOVA (šolska hiša — oče + botr učitelj); botra Janez Barle [~] učitelj + Johana [~]; babica Jožefa Uren [~]",
    whatEn: "baptized Elizabeta (Nov 16/17) — father Franc Kopitar [~] TEACHER, mother Marija Schweiger [~]; house 90 NEW (the school house — teacher father + teacher godparent); godparents Janez Barle [~] teacher + Johana [~]; midwife Jožefa Uren [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04105",
    year: 1890,
    scan: 49,
    page: 48,
    whatSi: "krščen otrok brez imena (»N. moškega spola«, 19./17.[prečrtano] 12.) — očetov stolpec »Marija Hrižan [~] ½ zemljak« ANOMALIJA, mati Ana Požek [~]; hiša 35 — ISTI anomaljski vzorec kot P82 row 93 1887 (čez-letna potrditev!); botra PRAZNA; babica Marjeta Šotter; podpis prazen",
    whatEn: "baptized an unnamed child (»male sex«, Dec 19/17.[crossed out]) — father column »Marija Hrižan [~] half smallholder« ANOMALY, mother Ana Požek [~]; house 35 — THE SAME anomalous pattern as P82 row 93 of 1887 (cross-year confirmation!); godparents EMPTY; midwife Marjeta Šotter; signature empty",
    status: "DOCUMENTED",
  },
  // ——— P86 razširitev: KRSTNA KNJIGA 04105 — polno leto 1891 (okvir skeni
  // 49–56 == strani 48–55; leto se začne na str. 48 row 1 po 1890 rows 78–86;
  // glava »Leto 1892« na str. 55 row 1 — oznake ponastavljene, novela P83
  // potrjena 4. leto; leto 1891 ima 75 zveznih vrstic) — vpisi z Griblji
  // (10; 9 zasidranih + 1 prekrita evidence-only r52; 0 nezakonskih; NOVELA:
  // vsi 9 statusi = ¼ ulomek — novela P85 potrjena 2. leto; DVE menjavi
  // matere na zasidranih hišah — h61 Filak→Dragos, h72 Husič→Jakobič;
  // popolna kontinuiteta h30 z P85 dvojčki; PT luknja: 53 NOVA — 14.
  // dokazana; Šimec 0× — prvo leto brez najtrajnejše familije; NOVE hiše 2
  // (28, 53) + ponovitve 7 (h5 ČEZ KNJIGE — mrliška 04894 1886; h61
  // 1887+1897; h62 1887)) ———
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1891,
    scan: 50,
    page: 49,
    whatSi: "krščen Janez (30./31. 1.) — oče Matija Straus [~] ¼ zemljak (ISTI očet kot P83 1888 — re-read Hraus→Strauš; mati menjana: 1888 Barbara Husič [~] → 1891 Marija Jakobič [~]), mati Marija Jakobič [~]; hiša 72 (tri-virska P80 + PUA Strauß Niklo @71, P81 0.8571); botra Matija Straucelj [~] + Barbara Oašovie [~]; babica Marija Brinec (6. leto)",
    whatEn: "baptized Janez (Jan 30/31) — father Matija Straus [~] quarter smallholder (THE SAME father as P83 1888 — re-read Hraus→Strauš; mother changed: 1888 Barbara Husič [~] → 1891 Marija Jakobič [~]), mother Marija Jakobič [~]; house 72 (the three-source P80 + PUA Strauß Niklo @71, P81 0.8571); godparents Matija Straucelj [~] + Barbara Oašovie [~]; midwife Marija Brinec (6th year)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1891,
    scan: 51,
    page: 50,
    whatSi: "krščena Marija (13./13. 4.) — oče Janez Milek [~] ¼ zemljak, mati Marjeta Pozdirec [~]; hiša 30 (P85 dvojčka rows 51+52 1890 — ISTI starši + ISTA botra Matija Milek + Katarina Križan: popolna dvoletna kontinuiteta; Milek = P81 near-miss); babica Marija Brinec; modri pripis: umrla 5.8.1983 v Gribljih (MNK 1/1983)",
    whatEn: "baptized Marija (Apr 13/13) — father Janez Milek [~] quarter smallholder, mother Marjeta Pozdirec [~]; house 30 (P85 twins rows 51+52 of 1890 — THE SAME parents + THE SAME godparents Matija Milek + Katarina Križan: complete two-year continuity; Milek = P81 near-miss); midwife Marija Brinec; blue note: died Aug 5, 1983 in Griblje (MNK 1/1983)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04105",
    year: 1891,
    scan: 52,
    page: 51,
    whatSi: "krščen Jožef (6./6. 8.) — oče Anton Muern [~] ¼ gemžgah, mati Barbara Hrižan [~]; hiša 62 (PONOVITEV P82 1887 — Križan gospodinjstvo tudi 1887; h63 P85 sidro Nikolaj Križan sosed); botra Matija Milek [~] (2. pojav 1891) + Barbara Brodarič [~]; babica Ana Hrižan [~]; + 19/8 91",
    whatEn: "baptized Jožef (Aug 6/6) — father Anton Muern [~] quarter smallholder's helper, mother Barbara Hrižan [~]; house 62 (REPEAT of P82 1887 — a Križan household also in 1887; h63 the P85 anchor Nikolaj Križan next door); godparents Matija Milek [~] (2nd appearance 1891) + Barbara Brodarič [~]; midwife Ana Hrižan [~]; died Aug 19, 1891",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04105",
    year: 1891,
    scan: 52,
    page: 51,
    whatSi: "krščen Nikolaj (roj. 11., krst 1. avg. [~]) — oče Nikolaj Pošek/Požek [~] ¼ zemljak (P82 SIDRO 1887: oče Miko Požek — ISTA OSEBA po 4 letih), mati Ana Dragos [~ Dragoš] (MENJAVA MATERE: 1887 Bara Filak → 1891 Dragos — prvi dokaz menjave na zasidrani hiši); botra PRAZNA (edini vpis brez botre); babica Ana Hrižan [~]; podpis prazen; + 1/8 91 [~]",
    whatEn: "baptized Nikolaj (born 11th, baptized Aug 1 [~]) — father Nikolaj Pošek/Požek [~] quarter smallholder (the P82 ANCHOR of 1887: father Miko Požek — THE SAME person 4 years later), mother Ana Dragos [~ Dragoš] (MOTHER CHANGE: 1887 Bara Filak → 1891 Dragos — the first evidence of a household change on an anchored house); godparents EMPTY (the only entry without godparents); midwife Ana Hrižan [~]; signature empty; died Aug 1, 1891 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1891,
    scan: 52,
    page: 51,
    whatSi: "krščena Marijeta (14./14. 8. [~]) — oče Janez Pozdirec [~] ¼ zemljak, mati Marija Križan [~]; hiša 53 = PT LUKNJA NOVA (14. dokazana številka!; forenzika izrez 4x: jasno 53 — prvi prebir »33« [~], Kurrent 3/5); botra Anton Podjarič [~] + Ana Križan [~]; babica Ana Križan [~]; modri pripis: umrla 22.4.1958 v Šempetru št. 64",
    whatEn: "baptized Marijeta (Aug 14/14 [~]) — father Janez Pozdirec [~] quarter smallholder, mother Marija Križan [~]; house 53 = NEW GAP NUMBER (the 14th proven!; 4x crop forensics: clearly 53 — first read »33« [~], Kurrent 3/5); godparents Anton Podjarič [~] + Ana Križan [~]; midwife Ana Križan [~]; blue note: died Apr 22, 1958 in Šempeter no. 64",
    status: "DOCUMENTED",
  },
  {
    houseNo: "2",
    bookSignature: "04105",
    year: 1891,
    scan: 53,
    page: 52,
    whatSi: "krščena Marjeta (30./30. 8.) — oče Peter Hlebec [~] ¼ gemžgah, mati Ana Jaklpič [~]; hiša 2 TROJNA KONTINUITETA (P82 1887 + P84 1889 + 1891 — ISTI starši Peter Hlebec + Ana Jakobič/Jaklpič ×3 čez 5 let); botra Matija Zimnc [~] + Katarina Hlebec [~]; babica Marjeta Fojter [~] (nova); + 19/1 93",
    whatEn: "baptized Marjeta (Aug 30/30) — father Peter Hlebec [~] quarter smallholder's helper, mother Ana Jaklpič [~]; house 2 TRIPLE CONTINUITY (P82 1887 + P84 1889 + 1891 — THE SAME parents Peter Hlebec + Ana Jakobič/Jaklpič ×3 across 5 years); godparents Matija Zimnc [~] + Katarina Hlebec [~]; midwife Marjeta Fojter [~] (new); died Jan 19, 1893",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1891,
    scan: 53,
    page: 52,
    whatSi: "krščen Frančišek (11./11. 9.) — oče Martin Tepič [~] ¼ gemžgah (1887/1890 Martin Papič [~] — Kurrent P/T [~]), mati Marjeta Straus [~] (ISTA OSEBA 1887 Margaretha + 1890 + 1891 — 3 vpise čez 5 let, P81 0.8571); hiša 31 (4. vpis); botra Martin Klobučar [~] (4. leto) + Ana Podirec [~]; babica Marjeta Fojter [~] (ISTA kot r43)",
    whatEn: "baptized Frančišek (Sep 11/11) — father Martin Tepič [~] quarter smallholder's helper (1887/1890 Martin Papič [~] — Kurrent P/T [~]), mother Marjeta Straus [~] (THE SAME person 1887 Margaretha + 1890 + 1891 — 3 entries across 5 years, P81 0.8571); house 31 (4th entry); godparents Martin Klobučar [~] (4th year) + Ana Podirec [~]; midwife Marjeta Fojter [~] (THE SAME as r43)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1891,
    scan: 53,
    page: 52,
    whatSi: "krščena Jožefa (13./13. 9. [~]) — oče Mihael Torec [~] ¼ gemžgah, mati Ana Torec [~]; hiša 5 (PONOVITEV ČEZ KNJIGE — mrliška 04894 1886: umrla Barbara Brinec [~] 2 leti — Brinec gospodinjstvo 1886 → Torec 1891 = menjava gospodinjstva); botra Janez Torec [~] + Barbara Torec [~]; babica Katarina [~]; modri pripis: umrla 12.8.1984 v Crnem potoku + modro ime »Terezija?« [~] (nasprotuje tmavemu Jožefa)",
    whatEn: "baptized Jožefa (Sep 13/13 [~]) — father Mihael Torec [~] quarter smallholder's helper, mother Ana Torec [~]; house 5 (CROSS-BOOK REPEAT — mrliška 04894 1886: died Barbara Brinec [~] aged 2 — a Brinec household in 1886 → Torec 1891 = household change); godparents Janez Torec [~] + Barbara Torec [~]; midwife Katarina [~]; blue note: died Aug 12, 1984 in Crni potok + blue name »Terezija?« [~] (contradicts the dark-ink Jožefa)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "28",
    bookSignature: "04105",
    year: 1891,
    scan: 54,
    page: 53,
    whatSi: "krščen Anton (25./26. 10.) — oče Jurij Požek [~] ¼ zemljak (POŽEK VERIGA: h79 1888 → h77 1890 → h28 1891 — 3. hiša familije v 4 letih), mati Marjeta Milkovič [~] (= Milek varianta); hiša 28 NOVA; botra Anton Muern [~] (ISTI kot oče h62) + Katarina Milek [~]; babica Ana Hrižan [~]; marginalija: poročen 16.4.1922, + 18.4.1926",
    whatEn: "baptized Anton (Oct 25/26) — father Jurij Požek [~] quarter smallholder (THE POŽEK CHAIN: h79 1888 → h77 1890 → h28 1891 — the family's 3rd house in 4 years), mother Marjeta Milkovič [~] (= Milek variant); house 28 NEW; godparents Anton Muern [~] (THE SAME as the h62 father) + Katarina Milek [~]; midwife Ana Hrižan [~]; margin: married Apr 16, 1922, died Apr 18, 1926",
    status: "DOCUMENTED",
  },
  // ——— P87 razširitev: KRSTNA KNJIGA 04105 — polno leto 1892 (okvir skeni
  // 56–63 == strani 55–62; glava »Leto 1892« na str. 55 row 1; velike cifre
  // »1893~« na str. 62 po row 82 — oznake ponastavljene, novela P83
  // potrjena 5. leto; leto 1892 ima 82 zveznih vrstic) — vpisi z Griblji
  // (12 / 12 hiš — NARE, 0 neberljivih; NOVELA: statusi ulomki, novela P85
  // potrjena 3. leto — ½ zemljak 5 + ¼ zemljak 4 + bajtar 2 + učitelj 1;
  // h61 KONTINUITETA SIDRA 2. leto (Požek × Dragos, brez botre/podpisa
  // kot 1891); h58 Požek × Dragos 3. leto; h63 oče ISTI 4× (Križan/
  // Hrižan); h1 Željko × Kure 1888+1892; h29 Milek × Križan 1888+1892;
  // h32 Urh 3× 1889+1890+1892; h90 šolska hiša (učitelj 1890+1892);
  // h24 + h27 menjavi gospodinjstva; NOVE hiše
  // 3 (12, 73, 75) + ponovitve 9; Šimec 0× 2. leto zapored) ———
  {
    houseNo: "75",
    bookSignature: "04105",
    year: 1892,
    scan: 56,
    page: 55,
    whatSi: "krščena Ana (19./19. 1.) — oče Janez Jakobčič [~] ½ zemljak, mati Marija Sušljar [~]; hiša 75 NOVA v vzorcu (prvi dokaz čez tri knjige); botra Janez Pozdirec [~] + Barbara Brinec [~]; babica Marija Brinec (8. leto); modri pripis: umrla 6.7.1952 v Gribljah št. 49",
    whatEn: "baptized Ana (Jan 19/19) — father Janez Jakobčič [~] half smallholder, mother Marija Sušljar [~]; house 75 NEW in the sample (first evidence across three books); godparents Janez Pozdirec [~] + Barbara Brinec [~]; midwife Marija Brinec (8th year); blue note: died Jul 6, 1952 in Griblje no. 49",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04105",
    year: 1892,
    scan: 56,
    page: 55,
    whatSi: "krščena Marija (24./24. 1.) — oče Peter Milek [~] ¼ zemljak, mati Ana Križan [~] (ISTA ZVEZA 1888+1892: P84 1888 Peter Milek ½ × Ana Križan — »hiša epidemije«; status ½→¼ [~]; mrliška 04894 1886: trije Mileh [~] otroci v koleri); hiša 29; botra Janez Adlešič [~] + Barbara Adlešič [~]; babica Marija Brinec; modri pripis: umrl 20.4.1958 [~]",
    whatEn: "baptized Marija (Jan 24/24) — father Peter Milek [~] quarter smallholder, mother Ana Križan [~] (THE SAME COUPLE 1888+1892: P84 1888 Peter Milek ½ × Ana Križan — »the epidemic house«; status ½→¼ [~]; mrliška 04894 1886: three Mileh [~] children in the cholera); house 29; godparents Janez Adlešič [~] + Barbara Adlešič [~]; midwife Marija Brinec; blue note: died Apr 20, 1958 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "73",
    bookSignature: "04105",
    year: 1892,
    scan: 57,
    page: 56,
    whatSi: "krščen Anton (29./30. 1.) — oče Nikolaj Županič [~] ½ zemljak, mati Katarina Pozdirec [~]; hiša 73 NOVA v vzorcu (prvi dokaz čez tri knjige); botra Nikol. Starčinič [~] + Katarina Cajnar [~]; babica Marija Brinec; podpis celo ime »Franc Češarek« (P86 »St. Češarek« — Kurrent Fr/St [~])",
    whatEn: "baptized Anton (Jan 29/30) — father Nikolaj Županič [~] half smallholder, mother Katarina Pozdirec [~]; house 73 NEW in the sample (first evidence across three books); godparents Nikol. Starčinič [~] + Katarina Cajnar [~]; midwife Marija Brinec; signature with full name »Franc Češarek« (P86 »St. Češarek« — Kurrent Fr/St [~])",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1892,
    scan: 57,
    page: 56,
    whatSi: "krščen Jožef (3./3. 2.) — oče Janez Dragos [~] ½ zemljak, mati Barbara Civlkovič [~]; hiša 12 NOVA v vzorcu (prvi dokaz čez tri knjige; Dragos/Dragoš 2. hiša familije — mati na h58 1890+1892); botra Janez Jakobič [~] + Marija Jakobič [~]; babica Marija Brinec; svinčnik: ?12.2.1929 + 27.12.1995 [~]",
    whatEn: "baptized Jožef (Feb 3/3) — father Janez Dragos [~] half smallholder, mother Barbara Civlkovič [~]; house 12 NEW in the sample (first evidence across three books; Dragos/Dragoš the family's 2nd house — mother on h58 1890+1892); godparents Janez Jakobič [~] + Marija Jakobič [~]; midwife Marija Brinec; pencil: ?Feb 12, 1929 + Dec 27, 1995 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1892,
    scan: 57,
    page: 56,
    whatSi: "krščena Marija (4./5. 2.) — oče Marko Pozdirec [~] bajtar, mati Ana Želičo [~]; hiša 27 (3. vpis — MENJAVA GOSPODINJSTVA: oče 1887 Kukar [~] = 1890 Stubhar [~] ISTI (re-read) → 1892 Pozdirec — 2. familija); botra Nikol. Križan [~] + Marija Brodarič [~]; babica Ana Križan; modri pripis: poročena 5.5.1919 + 8.1.1935 [~]",
    whatEn: "baptized Marija (Feb 4/5) — father Marko Pozdirec [~] cottager, mother Ana Želičo [~]; house 27 (the 3rd entry — HOUSEHOLD CHANGE: the father 1887 Kukar [~] = 1890 Stubhar [~] THE SAME (re-read) → 1892 Pozdirec — the 2nd family); godparents Nikol. Križan [~] + Marija Brodarič [~]; midwife Ana Križan; blue note: married May 5, 1919, died Jan 8, 1935 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1892,
    scan: 60,
    page: 59,
    whatSi: "krščena Neža (6./6. 6.) — oče Nikolaj Željko [~] ¼ zemljak (P83 1888 »Zeljth« [~] — re-read, ISTA ZVEZA 1888+1892; status ½→¼ [~]), mati Katarina Kure [~]; hiša 1 — NAJNIŽJA številka v vzorcu; botra Jurij Željko [~] + Katarina Kure [~] (ISTA priimka kot mati); babica Marjeta Trotter [~] (nova)",
    whatEn: "baptized Neža (Jun 6/6) — father Nikolaj Željko [~] quarter smallholder (P83 1888 »Zeljth« [~] — re-read, THE SAME COUPLE 1888+1892; status ½→¼ [~]), mother Katarina Kure [~]; house 1 — THE LOWEST number in the sample; godparents Jurij Željko [~] + Katarina Kure [~] (THE SAME surname as the mother); midwife Marjeta Trotter [~] (new)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1892,
    scan: 60,
    page: 59,
    whatSi: "krščena Marija (21./21. 6.) — oče Matija Urh [~] ¼ zemljak (ISTI OČE 3×: 1889 + 1890 + 1892 — Urh veriga 1887–1892, 6 let; Urh = PUA urh 1.0), mati Margaretha Pegdirec [~] (Pezdirec/Pendirec vseh 3 let — ISTA žena? [~]); hiša 32; botra Marko Hrižan [~] + Barbara Strauš [~] (Straus signal 0.8571); babica Ana Križan",
    whatEn: "baptized Marija (Jun 21/21) — father Matija Urh [~] quarter smallholder (THE SAME father 3×: 1889 + 1890 + 1892 — the Urh chain 1887–1892, 6 years; Urh = PUA urh 1.0), mother Margaretha Pegdirec [~] (Pezdirec/Pendirec all 3 years — THE SAME wife? [~]); house 32; godparents Marko Hrižan [~] + Barbara Strauš [~] (the Straus signal 0.8571); midwife Ana Križan",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1892,
    scan: 61,
    page: 60,
    whatSi: "krščen Nikolaj (6./6. 8.) — oče Janez Požek [~] ½ zemljak, mati Ana Dragos [~ Dragoš] (POŽEK × DRAGOS na h58 3. LETO: 1889 Franz + 1890 Janez + 1892 Janez — najdaljša zasidrana zveza familije); hiša 58 (forenzika izrez 2x: jasno 58 — prvi prebir »53« [~], Kurrent 3/5); botra Janez Pegdirec [~] + Marija Strauš [~]; babica Marija Trotter [~]; + 9/9. 92",
    whatEn: "baptized Nikolaj (Aug 6/6) — father Janez Požek [~] half smallholder, mother Ana Dragos [~ Dragoš] (POŽEK × DRAGOS on h58 for the 3rd YEAR: 1889 Franz + 1890 Janez + 1892 Janez — the family's longest anchored couple); house 58 (2x crop forensics: clearly 58 — first read »53« [~], Kurrent 3/5); godparents Janez Pegdirec [~] + Marija Strauš [~]; midwife Marija Trotter [~]; died Sep 9, 1892",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1892,
    scan: 61,
    page: 60,
    whatSi: "krščen Francišek (10./11. 9.) — oče Franc Kopitac [~] učitelj (ISTA UČITELJSKA DRUŽINA 1890+1892: Kopitar/Kopitac × Schweiger/Schweizer — učitelj ostal vsaj 1890–1892), mati Marija Schweizer [~]; ŠOLSKA HIŠA 90; botra Janez Barle [~] nadučitelj (prvi nadučitelj v vzorcu) + Marija Trotter [~] sopuga; podpis delno [~]",
    whatEn: "baptized Francišek (Sep 10/11) — father Franc Kopitac [~] teacher (THE SAME TEACHER FAMILY 1890+1892: Kopitar/Kopitac × Schweiger/Schweizer — the teacher stayed at least 1890–1892), mother Marija Schweizer [~]; the SCHOOL HOUSE 90; godparents Janez Barle [~] head teacher (the first head teacher in the sample) + Marija Trotter [~] his wife; signature partial [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1892,
    scan: 61,
    page: 60,
    whatSi: "krščen Nikolaj (10./10. 10.) — oče Nikolaj Hrižan [~] ¼ zemljak (ISTI OČE — ime+priimek — 4×: 1887 Prižan [Križan] + 1889 Hrigian? [nezakonska] + 1890 Križan ½ + 1892 Hrižan; P85 SIDRO potrjeno; Kurrent K/H varianta; status ½→¼ [~]), mati Katarina Pegdirec [~] (≈ 1889 Pezdirec [~] — ISTA žena? [~]); hiša 63; botra Marko Pegdirec [~] + Barbara Brodarič [~]; modri pripis: umrl 24.2.1967 [~]",
    whatEn: "baptized Nikolaj (Oct 10/10) — father Nikolaj Hrižan [~] quarter smallholder (THE SAME father — first name+surname — 4×: 1887 Prižan [Križan] + 1889 Hrigian? [illegitimate] + 1890 Križan ½ + 1892 Hrižan; the P85 ANCHOR confirmed; the Kurrent K/H variant; status ½→¼ [~]), mother Katarina Pegdirec [~] (≈ 1889 Pezdirec [~] — THE SAME wife? [~]); house 63; godparents Marko Pegdirec [~] + Barbara Brodarič [~]; blue note: died Feb 24, 1967 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "61",
    bookSignature: "04105",
    year: 1892,
    scan: 61,
    page: 60,
    whatSi: "krščena Ana (roj. 25. 11. [~], »s teh. krščena« [~]) — oče Nikolaj Požek [~] ½ zemljak, mati Ana Dragos [~ Dragoš] (KONTINUITETA SIDRA 2. LETO: P86 1891 oče Nikolaj Pošek/Požek + mati Ana Dragos — ISTA ZVEZA 1891+1892; status ¼→½ [~] — menjava statusa na zasidrani hiši [~]); hiša 61 (P82 sidro 1887 + 1897 + 1891 + 1892); botra PRAZNA + podpis PRAZEN (ISTI vzorec kot 1891 r39 — edini v obeh letih); babica Ana Križan; † 24/9. 9? [~]",
    whatEn: "baptized Ana (born Nov 25 [~], »baptized the same day« [~]) — father Nikolaj Požek [~] half smallholder, mother Ana Dragos [~ Dragoš] (ANCHOR CONTINUITY for the 2nd YEAR: P86 1891 father Nikolaj Pošek/Požek + mother Ana Dragos — THE SAME COUPLE 1891+1892; status ¼→½ [~] — a status change on an anchored house [~]); house 61 (the P82 anchor 1887 + 1897 + 1891 + 1892); godparents EMPTY + signature EMPTY (THE SAME pattern as 1891 r39 — the only one in both years); midwife Ana Križan; died Sep 24, 189? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1892,
    scan: 62,
    page: 61,
    whatSi: "krščen Martin [~] (26./27. 12.; ime delno pod modrimi pripisi) — oče Martin Jurajevič [~] bajtar, mati Marjana Krajnovec [~]; hiša 24 (4. vpis — MENJAVA GOSPODINJSTVA: Brinec gospodinjstvo 1887 + anomalija 1890 → Jurajevič 1892; forenzika izrez 4x: kraj jasno Griblje, modri pripisi so mrliški »umrl … 1968 v Gradac«); botra Danijel Muhr [~] + Ana Vdovič [~]; babica Ana Krajnovec [~]; podpis Jos. Rauq",
    whatEn: "baptized Martin [~] (Dec 26/27; name partially under blue notes) — father Martin Jurajevič [~] cottager, mother Marjana Krajnovec [~]; house 24 (the 4th entry — HOUSEHOLD CHANGE: the Brinec household 1887 + the anomaly 1890 → Jurajevič 1892; 4x crop forensics: the place clearly Griblje, the blue notes are death notes »died … 1968 in Gradac«); godparents Danijel Muhr [~] + Ana Vdovič [~]; midwife Ana Krajnovec [~]; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  // ——— P88 razširitev: KRSTNA KNJIGA 04105 — polno leto 1893 (okvir skeni
  // 63–70 == strani 62–69; glava »1893~« na str. 62 po 1892 row 82; velike
  // cifre »1894« na str. 69 po row 83 — oznake ponastavljene, novela P83
  // potrjena 6. leto; leto 1893 ima 83 zveznih vrstic) — vpisi z Griblji
  // (17 / 16 hiš — h27 DVOJČICI z eksplicitnim pripisom; NOVELA: ulomki,
  // novela P85 potrjena 4. leto — ½ zemljak 13 + ¼ zemljak 4; SIDRA: h72
  // Strauš SIDRO 3. VPIS (oče ISTI 3×: 1888+1891+1893), h65 Milek oče ISTI
  // 3× (1887+1889+1893), h27 dvojčici (oče Stukar/Stubhar, ISTA mati
  // Klobučar kot 1887+1890), h21 ŠIMEC NAZAJ (mati Ana Šimec + botra Janez
  // Šimec — prvič od 1890; oče Požek ISTI 1887+1893, MATI MENJANA Brinec→
  // Šimec — 3. dokazana menjava matere), h24 ISTA zveza Brinec × Jakobec
  // 1887+1893 (5. vpis; izmenjava z Jurajevič 1892), h30 MENJAVA
  // GOSPODINJSTVA (Milek → Jakljevič), h41 ISTA zveza 1890+1893, h15 ISTA
  // zveza 1887+1893 (Jakšič/Jaklič), h60 NOVA (Željko 2. hiša: h1→h60),
  // h91 NOVA (botra Željko + Kure); NOVE hiše 4 (23, 46, 70, 91) +
  // ponovitve 12 (h60 nova krstna — poroka 04455 1886); duhovnik NOV Janez
  // Jelovšek? od septembra (Rauq 14×);
  // babica Trotter 9×) ———
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1893,
    scan: 63,
    page: 62,
    whatSi: "krščen Anton (3./4. 1.) — oče Nikolaj Željko [~] ½ zemljak (ISTI oče kot h1 1888+1892 — ŽELJKO 2. HIŠA: h1 → h60), mati Marija Brodarič [~]; hiša 60 NOVA v krstnem vzorcu (poroka 04455 1886 Maria Bohor); botra Marko Pegdirec [~] + Marija Klepec [~]; babica Ana Hrižan [~]; modri pripis: umrl 25.9.1955 v Novem mestu",
    whatEn: "baptized Anton (Jan 3/4) — father Nikolaj Željko [~] half smallholder (THE SAME father as h1 1888+1892 — ŽELJKO'S 2nd HOUSE: h1 → h60), mother Marija Brodarič [~]; house 60 NEW in the baptism sample (the 1886 marriage 04455 Maria Bohor); godparents Marko Pegdirec [~] + Marija Klepec [~]; midwife Ana Hrižan [~]; blue note: died Sep 25, 1955 in Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1893,
    scan: 64,
    page: 63,
    whatSi: "krščen Anton (3./3. 3.) — oče Matija Milek [~] ½ zemljak (OČE ISTI 3×: 1887 + 1889 + 1893; mati variante Požek/Trojžif?/Jožek? [~]), mati Katarina Jožek? [~]; hiša 65 (forenzika izrez 5x: jasno 65 — prvi prebir 60 [~]); botra Peter Pegdirec [~] + Barbara Adlešič [~]; babica Barbara Adlešič [~]",
    whatEn: "baptized Anton (Mar 3/3) — father Matija Milek [~] half smallholder (THE SAME father 3×: 1887 + 1889 + 1893; mother variants Požek/Trojžif?/Jožek? [~]), mother Katarina Jožek? [~]; house 65 (5x crop forensics: clearly 65 — first read 60 [~]); godparents Peter Pegdirec [~] + Barbara Adlešič [~]; midwife Barbara Adlešič [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04105",
    year: 1893,
    scan: 64,
    page: 63,
    whatSi: "krščena Marjeta (28./29. 3.) — oče Matija Hušič? [~] ½ zemljak, mati Neža Jakobič [~] (ISTA ZVEZA kot 1890 Barbara vpis: Hrušič × Jakobčič); hiša 41 = PT LUKNJA (3. vpis: 1890 ×2 + 1893); botra Janez Jakobič [~] + Ana Pegdirec [~]; babica Marjeta Trotter [~]",
    whatEn: "baptized Marjeta (Mar 28/29) — father Matija Hušič? [~] half smallholder, mother Neža Jakobič [~] (THE SAME COUPLE as the 1890 Barbara entry: Hrušič × Jakobčič); house 41 = the PT GAP (3rd entry: 1890 ×2 + 1893); godparents Janez Jakobič [~] + Ana Pegdirec [~]; midwife Marjeta Trotter [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "70",
    bookSignature: "04105",
    year: 1893,
    scan: 65,
    page: 64,
    whatSi: "krščena Ana (9./9. 4.) — oče Nikolaj Segina [~] ½ zemljak, mati Marjeta Milek [~] roj. Pegdirec [~]; hiša 70 NOVA v vzorcu (forenzika izrez 5x: jasno 70); botra Matija Milek [~] (oče h65 3×) + Ana Križan [~]; babica Ana Križan [~]",
    whatEn: "baptized Ana (Apr 9/9) — father Nikolaj Segina [~] half smallholder, mother Marjeta Milek [~] née Pegdirec [~]; house 70 NEW in the sample (5x crop forensics: clearly 70); godparents Matija Milek [~] (the h65 father 3×) + Ana Križan [~]; midwife Ana Križan [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04105",
    year: 1893,
    scan: 65,
    page: 64,
    whatSi: "krščen Matko (24./25. 5.) — oče Matija Brinec [~] ½ zemljak, mati Marija Debič [~]; hiša 23 NOVA v vzorcu (forenzika izrez 5x: jasno 23); botra Janez Jaklič [~] + Doroteja Pegdirec [~]; babica Ana Klepec [~]; svinčnik: poročen 6.2.1927; modri pripisi: Italijani 1941, umrl 30.6.2000 (MMK 204–29/2000)",
    whatEn: "baptized Matko (May 24/25) — father Matija Brinec [~] half smallholder, mother Marija Debič [~]; house 23 NEW in the sample (5x crop forensics: clearly 23); godparents Janez Jaklič [~] + Doroteja Pegdirec [~]; midwife Ana Klepec [~]; pencil: married Feb 6, 1927; blue notes: Italians 1941, died Jun 30, 2000 (MMK 204–29/2000)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04105",
    year: 1893,
    scan: 65,
    page: 64,
    whatSi: "krščena Alojzija (9./9. 5.) — oče Janez Novak [~] ½ zemljak, mati Ana Kure [~]; hiša 91 NOVA v vzorcu (forenzika izrez 5x: jasno 91); botra Nikolaj Željko [~] + Katarina Kure [~] (ISTI priimki kot starši h1 — Željko signal 3. hiša: h1, h60, h91); babica Marjeta Trotter [~]; modri pripis: umrla 3.9.1957 v Ljubljani",
    whatEn: "baptized Alojzija (May 9/9) — father Janez Novak [~] half smallholder, mother Ana Kure [~]; house 91 NEW in the sample (5x crop forensics: clearly 91); godparents Nikolaj Željko [~] + Katarina Kure [~] (THE SAME surnames as the h1 parents — the Željko signal, a 3rd house: h1, h60, h91); midwife Marjeta Trotter [~]; blue note: died Sep 3, 1957 in Ljubljana",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1893,
    scan: 65,
    page: 64,
    whatSi: "krščena Antonija (7./8. 5.) — DVOJČICA (vertikalni pripis »dvojčice«; † 13/9. 93) — oče Janez Stukar/Stubhar [~] ½ zemljak (h27 oče ISTI: 1887 Kukar + 1890 Stubhar + 1893 — Kurrent varianta), mati Katarina Klobučar [~] (ISTA kot 1887+1890); hiša 27 (forenzika izrez 5x: jasno 27 — prvi prebir 24 [~]); botra Anton Kure [~] + Ana Tojžet? [~]; babica Marjeta Trotter [~]",
    whatEn: "baptized Antonija (May 7/8) — TWIN GIRL (the vertical note »dvojčice«; died Sep 13, 1893) — father Janez Stukar/Stubhar [~] half smallholder (the h27 father THE SAME: 1887 Kukar + 1890 Stubhar + 1893 — the Kurrent variant), mother Katarina Klobučar [~] (THE SAME as 1887+1890); house 27 (5x crop forensics: clearly 27 — first read 24 [~]); godparents Anton Kure [~] + Ana Tojžet? [~]; midwife Marjeta Trotter [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1893,
    scan: 65,
    page: 64,
    whatSi: "krščena Ivana (9.?/8. 5. [~]) — DVOJČICA (vertikalni pripis »dvojčice«; vsi starševski stolpci »isto« = r33) — oče Janez Stukar/Stubhar [~] ½ zemljak (isto), mati Katarina Klobučar [~] (isto); hiša 27; botra isto (Anton Kure + Ana Tojžet?); babica Marjeta Trotter [~]; modri pripis: »Franci 27.2.1916« [~] — 2. dvojčki v vzorcu (po P85 h30), prvi z eksplicitnim pripisom",
    whatEn: "baptized Ivana (May 9?/8 [~]) — TWIN GIRL (the vertical note »dvojčice«; all parent columns »isto« = ditto r33) — father Janez Stukar/Stubhar [~] half smallholder (ditto), mother Katarina Klobučar [~] (ditto); house 27; godparents ditto (Anton Kure + Ana Tojžet?); midwife Marjeta Trotter [~]; blue note: »Franci 27.2.1916« [~] — the 2nd twins in the sample (after the P85 h30 twins), the first with an explicit note",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04105",
    year: 1893,
    scan: 66,
    page: 65,
    whatSi: "krščena Marija (4./5. 6.) — oče Janez Jaklič [~] ½ zemljak (1887 Jakšič [~] — ISTA ZVEZA 1887+1893), mati Marija Brinec [~] (ISTA kot 1887); hiša 15 (mrliška 04894 1886 + poroki 04455); botra Matija Brinec [~] (oče h24/h28) + Ana Adlešič [~]; babica Barbara Adlešič [~]; modri pripis: umrla 15.9.1952 v Črnomlju",
    whatEn: "baptized Marija (Jun 4/5) — father Janez Jaklič [~] half smallholder (1887 Jakšič [~] — THE SAME COUPLE 1887+1893), mother Marija Brinec [~] (THE SAME as 1887); house 15 (mrliška 04894 1886 + marriages 04455); godparents Matija Brinec [~] (the h24/h28 father) + Ana Adlešič [~]; midwife Barbara Adlešič [~]; blue note: died Sep 15, 1952 in Črnomelj",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1893,
    scan: 66,
    page: 65,
    whatSi: "krščen Janez (3./3. 7.) — oče Anton Brodarič [~] ½ zemljak, mati Marija Klobučar [~]; hiša 46 NOVA v vzorcu (forenzika izrez 5x: jasno 46); botra Janez Jakobič? [~] + Neža Strauš? [~] (Straus signal 0.8571); babica Marjeta Trotter [~]; modri pripis: umrl 5.1.1957 v Gribljih 21/38",
    whatEn: "baptized Janez (Jul 3/3) — father Anton Brodarič [~] half smallholder, mother Marija Klobučar [~]; house 46 NEW in the sample (5x crop forensics: clearly 46); godparents Janez Jakobič? [~] + Neža Strauš? [~] (the Straus signal 0.8571); midwife Marjeta Trotter [~]; blue note: died Jan 5, 1957 in Griblje 21/38",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1893,
    scan: 66,
    page: 65,
    whatSi: "krščena Ana (22./23. 7.) — oče Matija Strauš [~] ½ zemljak (SIDRO 3. VPIS: ISTI oče 3× čez 6 let — 1888 P83 sidro + 1891 P86 + 1893; mati 1891+1893 ISTA Marija Jakobič; 1888 Barbara Husič menjana), mati Marija Jakobič [~]; tri-virska hiša P80 + PUA Strauß Niklo @71 (P81 0.8571); botra Miha Jakobič? [~] + Marija Straucelj [~] (ISTA botra kot 1891); babica Marjeta Trotter [~]; forenzika izrez 5x: jasno 72",
    whatEn: "baptized Ana (Jul 22/23) — father Matija Strauš [~] half smallholder (the ANCHOR'S 3rd ENTRY: THE SAME father 3× across 6 years — 1888 the P83 anchor + 1891 P86 + 1893; the mother 1891+1893 THE SAME Marija Jakobič; 1888 Barbara Husič changed), mother Marija Jakobič [~]; the three-source house P80 + PUA Strauß Niklo @71 (P81 0.8571); godparents Miha Jakobič? [~] + Marija Straucelj [~] (THE SAME godmother as 1891); midwife Marjeta Trotter [~]; 5x crop forensics: clearly 72",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1893,
    scan: 67,
    page: 66,
    whatSi: "krščena Neža (2./2. 8.) — oče Peter Jakljevič [~] ¼ zemljak, mati Marija Kralj [~] (MENJAVA GOSPODINJSTVA: Milek 1890 dvojčka + 1891 → Jakljevič 1893); hiša 30; botra Janez Jakljevič [~] + Katarina Segina [~]; babica PRAZNA (edini vpis 1893 brez babice); podpis obiskni G. Ambrož? [~] m.p.; modri pripis: umrla 15.9.1954 v Gribljih št. 8",
    whatEn: "baptized Neža (Aug 2/2) — father Peter Jakljevič [~] quarter smallholder, mother Marija Kralj [~] (HOUSEHOLD CHANGE: Milek 1890 twins + 1891 → Jakljevič 1893); house 30; godparents Janez Jakljevič [~] + Katarina Segina [~]; midwife EMPTY (the only 1893 entry without a midwife); visiting signature G. Ambrož? [~] m.p.; blue note: died Sep 15, 1954 in Griblje no. 8",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1893,
    scan: 67,
    page: 66,
    whatSi: "krščena Barbara (17./18. 8.) — oče Matija Brinec [~] ¼ zemljak, mati Barbara Jakobčič [~] (ISTA ZVEZA kot 1887: Brinec × Jakobec; h24 5. VPIS — gospodinjstvi Brinec ↔ Jurajevič se izmenjujeta: 1887 → 1892 Jurajevič → 1893 Brinec nazaj); hiša 24; botra Janez Brinec [~] + Ana Stubljar? [~]; babica Marjeta Trotter [~]; modri pripis: umrla 10.7.1979 v Metliki (MMK Metlika 1/1979, št. 436)",
    whatEn: "baptized Barbara (Aug 17/18) — father Matija Brinec [~] quarter smallholder, mother Barbara Jakobčič [~] (THE SAME COUPLE as 1887: Brinec × Jakobec; the h24 5th ENTRY — the Brinec ↔ Jurajevič households alternate: 1887 → 1892 Jurajevič → 1893 Brinec back); house 24; godparents Janez Brinec [~] + Ana Stubljar? [~]; midwife Marjeta Trotter [~]; blue note: died Jul 10, 1979 in Metlika (MMK Metlika 1/1979, no. 436)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "74",
    bookSignature: "04105",
    year: 1893,
    scan: 67,
    page: 66,
    whatSi: "krščena Barbara (19./19. 9.) — oče Matija Kambič? [~] ½ zemljak, mati Ana Brodarič? [~]; hiša 74 (PONOVITEV ČEZ KNJIGE — mrliška 04894 1886: umrl Jožef Hambeč [~] 1 mesec — Hambeč/Kambič [~] varianta); botra Miha Jakobič? [~] + Ana Pegdirec [~]; babica Marija Trotter [~]; podpis NOV Janez Jelovšek? [~] (od septembra 1893); modri pripisi: poročena 11/5 1919 [~]",
    whatEn: "baptized Barbara (Sep 19/19) — father Matija Kambič? [~] half smallholder, mother Ana Brodarič? [~]; house 74 (CROSS-BOOK REPEAT — mrliška 04894 1886: died Jožef Hambeč [~] aged 1 month — the Hambeč/Kambič [~] variant household); godparents Miha Jakobič? [~] + Ana Pegdirec [~]; midwife Marija Trotter [~]; signature NEW Janez Jelovšek? [~] (from September 1893); blue notes: married May 11, 1919 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1893,
    scan: 68,
    page: 67,
    whatSi: "krščena Katarina (1./1. 10.) — oče Janez Požek [~] ¼ zemljišt (ISTI oče kot 1887), mati Ana Šimec [~] (MATI MENJANA: 1887 Marija Brinec → 1893 Šimec — 3. dokazana menjava matere po h61/h72); ŠIMEC NAZAJ NA GRIBLJIH — prvič od 1890 (mati + botra Janez Šimec — Gerišče 1893 = ISTI? [~]); hiša 21 (1887 + 1888 nezakonska); botra Janez Šimec [~] + Katarina Kukar [~]; babica Ana Hrižan [~]; modri pripis: † 13/10. 1975",
    whatEn: "baptized Katarina (Oct 1/1) — father Janez Požek [~] quarter smallholder (THE SAME father as 1887), mother Ana Šimec [~] (MOTHER CHANGE: 1887 Marija Brinec → 1893 Šimec — the 3rd proven mother change after h61/h72); ŠIMEC BACK IN GRIBLJE — the first time since 1890 (mother + godfather Janez Šimec — Gerišče 1893 = THE SAME? [~]); house 21 (1887 + 1888 illegitimate); godparents Janez Šimec [~] + Katarina Kukar [~]; midwife Ana Hrižan [~]; blue note: died Oct 13, 1975",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04105",
    year: 1893,
    scan: 68,
    page: 67,
    whatSi: "krščena Katarina (21./22. 10.) — oče Matija Hrižan [~] ¼ zemljak (2. Hrižan oče poleg h63 Nikolaj), mati Ana Požek [~]; hiša 25 (PONOVITEV ČEZ KNJIGE — poroka 04455 1886: ženin Jurij Klepec GRIBLJE 25 → menjava gospodinjstva); botra Jurij Željko [~] (h1/h60 familija) + Marija Mek/Milek? [~]; babica Ana Hrižan [~] (ISTA kot r1/r62)",
    whatEn: "baptized Katarina (Oct 21/22) — father Matija Hrižan [~] quarter smallholder (the 2nd Hrižan father besides h63 Nikolaj), mother Ana Požek [~]; house 25 (CROSS-BOOK REPEAT — the 1886 marriage 04455: groom Jurij Klepec GRIBLJE 25 → a household change); godparents Jurij Željko [~] (the h1/h60 family) + Marija Mek/Milek? [~]; midwife Ana Hrižan [~] (THE SAME as r1/r62)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1893,
    scan: 68,
    page: 67,
    whatSi: "krščen Janez (5./5. 11.) — oče Matija Meh/Mrh? [~] ½ zemljak (MERI: h32 1889–1892 oče Matija Urh [~] — ISTA mati + ISTA botra kot 1892 → ali isti oče z novo brano priimko ali drug mož [~]), mati Marjeta Pegdirec [~] (≈ Margaretha 1892); hiša 32 (4. vpis: 1889+1890+1892+1893); botra Marko Hrižan [~] + Barbara Strauš [~] (ISTA kot 1892); babica Marjeta Trotter [~]; podpis Janez Jelovšek? [~] (2.)",
    whatEn: "baptized Janez (Nov 5/5) — father Matija Meh/Mrh? [~] half smallholder (MEASURES: the h32 1889–1892 father Matija Urh [~] — THE SAME mother + THE SAME godparents as 1892 → either the same father with a newly read surname or another husband [~]), mother Marjeta Pegdirec [~] (≈ Margaretha 1892); house 32 (the 4th entry: 1889+1890+1892+1893); godparents Marko Hrižan [~] + Barbara Strauš [~] (THE SAME as 1892); midwife Marjeta Trotter [~]; signature Janez Jelovšek? [~] (2nd)",
    status: "DOCUMENTED",
  },
  // ——— P89 razširitev: KRSTNA KNJIGA 04105 — polno leto 1894 (okvir skeni
  // 70–78 == strani 69–76; glava »1894« na str. 69 po 1893 row 83; velike
  // cifre »1895~« na str. 76 po row 90 — oznake ponastavljene, novela P83
  // potrjena 7. leto; leto 1894 ima 90 zveznih vrstic) — NOVELA OKVIRA:
  // sken 73 je PODOVOJEN sken str. 71 (matricula re-scan, prvi v seriji) —
  // stran == sken − 1 velja do skena 72, od skena 74 naprej − 2; vpisi z
  // Griblji (14 / 14 hiš — prvo leto brez ponovitev znotraj leta in PRVO
  // leto z 0 NOVIH hiš — vseh 14 že zasidranih, vzorec se zasiča; NOVELA:
  // ulomki, novela P85 potrjena 5. leto — ½ zemljak 8 + ¼ zemljak 6; SIDRA:
  // h2 ŠTIRIKRATNA kontinuiteta (ISTI starši Hlebec × Jakobič 4×: 1887+
  // 1889+1891+1894 — najdaljša zveza vzorca), h71 ISTA zveza Jurij Strauš ×
  // Barbara čez 8 let (P77 1886 r83; Strauš na DVEH hišah h71+h72; PUA @71
  // 0.8571), h36 Križan 2. GENERACIJA (4. vir tri-virske hiše), h31 4. VPIS
  // (oče Papič/Fapič ISTI + mati Straus ISTA + botra Klobučar), h17 ISTI
  // oče Kralj ¼ + MATER MENJANA (Jakobič → Firlak? — 5. dokazana), h57 ISTA
  // botra pa čez 8 let (P77), h60 + h23 ISTA botra pa 2. leto (P88), h12/
  // h53/h73/h75 ISTA zvezi (2. vpis); duhovnik Jan Jelenuš? 11× (≈ P88
  // »Jelovšek?«) + Rauq 3× (Feb/Sep/Dec); babica Trotter 11×) ———
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1894,
    scan: 70,
    page: 69,
    whatSi: "krščen Frančišek (28./28. 1.) — oče Janez Dragoš [~] ½ zemljak (ISTI oče kot P87 1892 — h12 2. VPIS), mati Barbara Druppovič? [~] (P87 »Civlkovič?« — varianti branja iste matere ali druga žena [~] MERI); hiša 12 (forenzika izrez 5x: jasno 12); botra Janez Jakobčič? [~] + Marija Strauš? [~]; babica Marija Trotter [~]; moder pripis: poročen 24/2. 1949",
    whatEn: "baptized Frančišek (Jan 28/28) — father Janez Dragoš [~] half smallholder (THE SAME father as P87 1892 — h12 2nd entry), mother Barbara Druppovič? [~] (P87 »Civlkovič?« — reading variants of the same mother or another wife [~]); house 12 (5x crop forensics: clearly 12); godparents Janez Jakobčič? [~] + Marija Strauš? [~]; midwife Marija Trotter [~]; blue note: married Feb 24, 1949",
    status: "DOCUMENTED",
  },
  {
    houseNo: "2",
    bookSignature: "04105",
    year: 1894,
    scan: 71,
    page: 70,
    whatSi: "krščen Matija (23./24. 2.) — oče Peter Hlebec [~] ¼ zemljak, mati Ana Jakobič [~]; hiša 2 (4. VPIS — ŠTIRIKRATNA KONTINUETETA: ISTI starši vseh 4× 1887+1889+1891+1894, 8 let — najdaljša zasidrana zveza vzorca); botra Janez Jakljič? [~] + Katarina? Klobučar [~]; babica Margareta (Margan.) Trotter [~]; moder pripis: mati umrla 2.9.1965? v Novem mestu (HMIC NM 1965, str. 469)",
    whatEn: "baptized Matija (Feb 23/24) — father Peter Hlebec [~] quarter smallholder, mother Ana Jakobič [~]; house 2 (the 4th entry — QUADRUPLE CONTINUITY: THE SAME parents all 4× 1887+1889+1891+1894, 8 years — the longest anchored couple in the sample); godparents Janez Jakljič? [~] + Katarina? Klobučar [~]; midwife Margareta Trotter [~]; blue note: mother died Sep 2, 1965? in Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1894,
    scan: 71,
    page: 70,
    whatSi: "krščen Jožef (13./13. 2.) — oče Janez Pegdirec? [~] ¼ zemljak, mati Marija Hrižan? [~] (ISTA ZVEZA kot P86 1891 »Pozdirec × Križan« — Kurrent P/K in K/H variante); hiša 53 = PT LUKNJA (2. vpis; babica Ana Hrižan ISTA kot 1891); botra Anton Brodarič? [~] + Ana Kure [~]; podpis Jos. Rauq",
    whatEn: "baptized Jožef (Feb 13/13) — father Janez Pegdirec? [~] quarter smallholder, mother Marija Hrižan? [~] (THE SAME COUPLE as P86 1891 »Pozdirec × Križan« — Kurrent P/K and K/H variants); house 53 = the PT GAP (2nd entry; midwife Ana Hrižan THE SAME as 1891); godparents Anton Brodarič? [~] + Ana Kure [~]; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1894,
    scan: 71,
    page: 70,
    whatSi: "krščena Joana (21./21. 2.) — oče Janez Brinec [~] ½ zemljak, mati Ana Kure [~]; hiša 69 NOV krstni vpis (čez knjige: mrliška 04894 1886 P78); botra Janez Muč? [~] + Katarina Požek? [~] (Požek familija botra — 7. leto); babica Marija Trotter [~]",
    whatEn: "baptized Joana (Feb 21/21) — father Janez Brinec [~] half smallholder, mother Ana Kure [~]; house 69 NEW baptism entry (cross-book: death register 04894 1886 P78); godparents Janez Muč? [~] + Katarina Požek? [~] (the Požek family as godparent — 7th year); midwife Marija Trotter [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1894,
    scan: 72,
    page: 71,
    whatSi: "krščen Janez (5./5. 5.) — oče Janez Križan? [~] ¼ zemljak, mati Katarina Straucelj? [~]; hiša 36 = TRI-VIRSKA (poroka 04455 1882 Mathias Križan + krstna 1886 ×2 P77 + mrliška 04894 1887) — 4. VIR: KRIŽAN 2. GENERACIJA (Matija 1882/1886 → Janez 1894 — mogoč sin [~] MERI; forenzika izrez 5x: jasno 36); botra Marija Straus? [~] + Marija Pegdirec? [~]; babica Marija Trotter [~]",
    whatEn: "baptized Janez (May 5/5) — father Janez Križan? [~] quarter smallholder, mother Katarina Straucelj? [~]; house 36 = THREE-SOURCE (the 1882 marriage 04455 Mathias Križan + the 1886 baptisms ×2 P77 + the 1887 death 04894) — a 4th source: KRIŽAN 2nd GENERATION (Matija 1882/1886 → Janez 1894 — possibly the son [~]; 5x crop forensics: clearly 36); godparents Marija Straus? [~] + Marija Pegdirec? [~]; midwife Marija Trotter [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "57",
    bookSignature: "04105",
    year: 1894,
    scan: 74,
    page: 72,
    whatSi: "krščen Janez (6./7. 7.) — oče Peter Pegdirec? [~] ½ zemljak [~] (frakcija z zaprto zanko — ½ ali ⅛? [~]), mati Marija Županc? [~]; hiša 57 = PT LUKNJA (2. vpis čez 8 let — P77 1886: starša »Podolivec/Stupanič« = varianti ali drugi [~] MERI); BOTRA PA ISTA čez 8 let (P77 r20: Jurij Brodarič? + Marija Strauš?); babica Marija Trotter [~]; moder: + 2/9. 94?",
    whatEn: "baptized Janez (Jul 6/7) — father Peter Pegdirec? [~] half smallholder [~] (fraction with a closed loop — ½ or ⅛? [~]), mother Marija Županc? [~]; house 57 = the PT GAP (2nd entry over 8 years — P77 1886 parents »Podolivec/Stupanič« = variants or another couple [~]); THE SAME godparent pair over 8 years (P77 r20: Jurij Brodarič? + Marija Strauš?); midwife Marija Trotter [~]; blue: + Sep 2, 94?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "73",
    bookSignature: "04105",
    year: 1894,
    scan: 75,
    page: 73,
    whatSi: "krščen Mihael (16./16. 7.) — oče Nikolaj Županič? [~] ½ zemljak, mati Katarina? Pegdirec? [~] (ISTA ZVEZA kot P87 1892 »Županič × Pozdirec« — 2. VPIS; botra menjana od 1892); hiša 73 (forenzika izrez 5x: jasno 73); botra Nikol Harasimič? [~] + Marjeta Pegdirec? [~]; babica Marija Trotter [~]; pripisi: roj. 31.3.1942 + umrl 8.1.1968",
    whatEn: "baptized Mihael (Jul 16/16) — father Nikolaj Županič? [~] half smallholder, mother Katarina? Pegdirec? [~] (THE SAME COUPLE as P87 1892 »Županič × Pozdirec« — 2nd entry; godparents changed since 1892); house 73 (5x crop forensics: clearly 73); godparents Nikol Harasimič? [~] + Marjeta Pegdirec? [~]; midwife Marija Trotter [~]; notes: born Mar 31, 1942 + died Jan 8, 1968",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1894,
    scan: 75,
    page: 73,
    whatSi: "krščena Joana (25./25. 7.) — oče Martin Fapič? [~] ½ zemljak (ISTI oče: Papič/Fapič/Tepič — Kurrent P/F/T), mati Marjeta Straus? [~] (ISTA vseh 4×); hiša 31 (4. VPIS: 1887+1890+1891+1894 — najbolj popolna trojica oče+mati+botra); botra Marko Klobučar? [~] (ISTI kot 1887) + Marjeta Pegdirec? [~]; babica Marija Trotter [~]; moder: + 29/6. 96",
    whatEn: "baptized Joana (Jul 25/25) — father Martin Fapič? [~] half smallholder (THE SAME father: Papič/Fapič/Tepič — Kurrent P/F/T), mother Marjeta Straus? [~] (THE SAME all 4×); house 31 (the 4th entry: 1887+1890+1891+1894 — the most complete father+mother+godparent trio); godparents Marko Klobučar? [~] (THE SAME as 1887) + Marjeta Pegdirec? [~]; midwife Marija Trotter [~]; blue: + Jun 29, 96",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1894,
    scan: 75,
    page: 73,
    whatSi: "krščen Jožef (28./29. 7.) — oče Matija Jakljevič? [~] (ali Jakobčič?) ½ zemljak (ISTI oče ime+status kot P77 1886 »Matija Jakopič? ½« — 2. vpis čez 8 let), mati Marija Pegdirec? [~] (P77 »Podlivc?« — varianta [~] MERI); hiša 13 TRI-VIRSKA (P77 krstna + P78 mrliška 04894); botra Matija Kambič? [~] + Katarina Križan? [~]; babica PRAZNA (druga po P88 r50)",
    whatEn: "baptized Jožef (Jul 28/29) — father Matija Jakljevič? [~] (or Jakobčič?) half smallholder (THE SAME father's name+status as P77 1886 »Matija Jakopič? ½« — 2nd entry over 8 years), mother Marija Pegdirec? [~] (P77 »Podlivc?« — a variant [~]); house 13 THREE-SOURCE (P77 baptismal + P78 death 04894); godparents Matija Kambič? [~] + Katarina Križan? [~]; midwife EMPTY (the second after P88 r50)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "75",
    bookSignature: "04105",
    year: 1894,
    scan: 76,
    page: 74,
    whatSi: "krščen Mihael (3./4. 9.) — oče Janez Jakobič? [~] ½ zemljak, mati Marija Stubljar? [~] (ISTA ZVEZA kot P87 1892 »Jakobčič × Sušljar« — 2. VPIS; Kurrent variante); hiša 75 (forenzika izrez 5x: jasno 75); botra Nikol. Pegdirec? [~] + Barb. Brinec? [~] (ženska botra ISTA 2. leto); babica Marija Hrižan? [~]; moder: + 19/9. 94",
    whatEn: "baptized Mihael (Sep 3/4) — father Janez Jakobič? [~] half smallholder, mother Marija Stubljar? [~] (THE SAME COUPLE as P87 1892 »Jakobčič × Sušljar« — 2nd entry; Kurrent variants); house 75 (5x crop forensics: clearly 75); godparents Nikol. Pegdirec? [~] + Barb. Brinec? [~] (the female godparent THE SAME 2nd year); midwife Marija Hrižan? [~]; blue: + Sep 19, 94",
    status: "DOCUMENTED",
  },
  {
    houseNo: "17",
    bookSignature: "04105",
    year: 1894,
    scan: 76,
    page: 74,
    whatSi: "krščen Mihael (7./7. 9.) — oče Janez Kralj? [~] ¼ zemljak (ISTI oče ISTA frakcija kot P82 1887 r82), mati Doroteja Firlak? [~] (P82 »Ana Jakobič« → MATER MENJANA — 5. dokazana po h61/h72/h21 — ali druga branja [~] MERI); hiša 17 (2. vpis čez 7 let; forenzika izrez 5x: jasno 17); botra Jurij Straus? [~] + Marija Jakobčič? [~]; babica Marija Trotter [~]; podpis Jos. Rauq",
    whatEn: "baptized Mihael (Sep 7/7) — father Janez Kralj? [~] quarter smallholder (THE SAME father with THE SAME fraction as P82 1887 r82), mother Doroteja Firlak? [~] (P82 »Ana Jakobič« → MOTHER CHANGED — the 5th documented after h61/h72/h21 — or other readings [~]); house 17 (2nd entry over 7 years; 5x crop forensics: clearly 17); godparents Jurij Straus? [~] + Marija Jakobčič? [~]; midwife Marija Trotter [~]; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04105",
    year: 1894,
    scan: 77,
    page: 75,
    whatSi: "krščena Barbara (7./7. 10.) — oče Jurij Straus? [~] ¼ zemljak, mati Barbara Jakobčič? [~] (ISTA ZVEZA čez 8 let — P77 1886 r83 »Jurij Strauš ½ × Barbara Jakopič«; status ½→¼); hiša 71 = TRI-VIRSKA (P77 krstna + P78 mrliška ×3) — STRAUŠ na DVEH sosednjih hišah (h71 Jurij + h72 Matija SIDRO 3 vpise; PUA @71 0.8571); botra Janez Kralj? [~] + Marijeta Mue? [~]; babica Marija Trotter [~]",
    whatEn: "baptized Barbara (Oct 7/7) — father Jurij Straus? [~] quarter smallholder, mother Barbara Jakobčič? [~] (THE SAME COUPLE over 8 years — P77 1886 r83 »Jurij Strauš ½ × Barbara Jakopič«; status ½→¼); house 71 = THREE-SOURCE (P77 baptismal + P78 deaths ×3) — STRAUŠ on TWO adjacent houses (h71 Jurij + h72 Matija, the ANCHOR with 3 entries; PUA @71 0.8571); godparents Janez Kralj? [~] + Marijeta Mue? [~]; midwife Marija Trotter [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04105",
    year: 1894,
    scan: 78,
    page: 76,
    whatSi: "krščen Janez (23./24. 11.) — oče Matija Brinec [~] ½ zemljak (ISTI oče kot P88 1893 — 2. VPIS), mati Marija Žehlič? [~] (P88 »Debič?« — varianti ali druga žena [~] MERI); hiša 23 (forenzika izrez 5x: jasno 23); botra Janez Jakljič? [~] + Doroteja Pegdirec? [~] (ISTA BOTRA PA 2. leto — P88 r28); babica Marija Trotter [~]; moder: poročen 28.11.1925",
    whatEn: "baptized Janez (Nov 23/24) — father Matija Brinec [~] half smallholder (THE SAME father as P88 1893 — 2nd entry), mother Marija Žehlič? [~] (P88 »Debič?« — variants or another wife [~]); house 23 (5x crop forensics: clearly 23); godparents Janez Jakljič? [~] + Doroteja Pegdirec? [~] (THE SAME godparent pair 2nd year — P88 r28); midwife Marija Trotter [~]; blue: married Nov 28, 1925",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1894,
    scan: 78,
    page: 76,
    whatSi: "krščena Marija (27./28. 12.) — oče Nikolaj Željko [~] ¼ zemljak, mati Marija Brodarič [~] (ISTA ZVEZA kot P88 1893 — h60 2. VPIS; status ½→¼ [~] menjava statusa); ŽELJKO VERIGA: h1 (1888+1892) + h60 (1893+1894) + h91 botra (1893) + h25 botra (1893); hiša 60 (forenzika izrez 5x: jasno 60); botra Marko Pegdirec [~] + Marija Klepec [~] (ISTA BOTRA PA 2. leto); babica Marija Trotter [~]; podpis Jos. Rauq; modri: + 6.3.1939 + grob Celovec",
    whatEn: "baptized Marija (Dec 27/28) — father Nikolaj Željko [~] quarter smallholder, mother Marija Brodarič [~] (THE SAME COUPLE as P88 1893 — h60 2nd entry; status ½→¼ [~] a status change); THE ŽELJKO CHAIN: h1 (1888+1892) + h60 (1893+1894) + h91 godparent (1893) + h25 godparent (1893); house 60 (5x crop forensics: clearly 60); godparents Marko Pegdirec [~] + Marija Klepec [~] (THE SAME godparent pair 2nd year); midwife Marija Trotter [~]; signature Jos. Rauq; blue: + Mar 6, 1939 + grave Celovec",
    status: "DOCUMENTED",
  },
  // ——— P90 razširitev: KRSTNA KNJIGA 04105 — polno leto 1895 (okvir skeni
  // 78–84 == strani 76–82; stran == sken − 2 ZA CELO LETO — novela P89
  // potrjena 2. leto; sken 73 podvojen, NI citiran; glava »1895.~« na str. 76
  // po 1894 row 90; leto 1895 ima 73 zveznih vrstic; prelom 1896 na str. 83 =
  // sken 85 po row 73 — oznake ponastavljene, novela P83 potrjena 8. leto) —
  // 15 vpisov / 14 hiš (h24 DVOM 2×: r22 Brime + r48 Toško?/Simec — prva
  // ponovitev hiše znotraj leta po P87 NARE; 3 NOVE hiše 20/37/87 po P89
  // »0 novih«; kumulativno 185 vpisov / 68 hiš čez tri knjige in DESET let;
  // NOVELA BABICA: stolpec babice na VSEH 15 vrsticah PRAZEN — 1894: Trotter
  // 11× — Trotter žene pa 7× kot BOTRA, vloga prestopila; NOVELA BOTRA: 4×
  // PRAZNA (r53/r54/r55/r66, september–december); TRIJE duhovniki: Jelenuš 9×
  // + Rauq 4× (apr–sep) + NOV Franc Klunng 2× (od septembra); MATI PODCELICA
  // (X × Y) prvič eksplicitno dokumentirana — semantika ODPRTA; SIDRA: h58
  // 4. VPIS + MATI MENJANA (Dragoš → Kambic?), h32 + h72 5. VPIS — NAJDALJŠI
  // zvezi vzorca (1889–1895), h69 oče ISTI 5×, h30 3. DRUŽINA (2× menjava —
  // najbolj nestabilna hiša), h29 MENJAVA (»hiša kuge« → Kuhar? × Klobučar),
  // h91 oče MENJAN (Novak → Muc), h46/h24/h12/h65 kontinuitete; h87 podcelica
  // Željko veriga; PEGDIREC prvič STARŠI 2× (h87 + h37)) ———
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1895,
    scan: 79,
    page: 77,
    whatSi: "krščena Katarina (28./28. 2.) — oče Janez Požek [~] ½ zemljak (ISTI oče 3. leto zapored: 1890 r22 + 1892 r60 + 1895; 1889 r3 »Franz Požek ¼« = ista oseba [~], status ¼→½), mati Katarina Kambic? [~] (MATI MENJANA: 1889–1892 Ana Dragoš/Dragos → 1895 Kambic? — smrt prve žene ali ločitev, mrliška 04894 bi dokazala; podcelica: Nikol. Požek × Marija Pegdirec — semantika ODPRTA [~]); hiša 58 (4. VPIS); botra Marjka Trotter [~] (Kurrent J/T »Jotter«); babica stolpec PRAZEN; podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Katarina (Feb 28/28) — father Janez Požek [~] half smallholder (THE SAME father 3rd year running: 1890 r22 + 1892 r60 + 1895; 1889 r3 »Franz Požek ¼« = the same person [~], status ¼→½), mother Katarina Kambic? [~] (MOTHER CHANGED: 1889–1892 Ana Dragoš/Dragos → 1895 Kambic? — death of the first wife or divorce, the death register 04894 would prove it; sub-cell: Nikol. Požek × Marija Pegdirec — semantics OPEN [~]); house 58 (4th entry); godparent Marjka Trotter [~] (Kurrent J/T »Jotter«); midwife column EMPTY; signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1895,
    scan: 80,
    page: 78,
    whatSi: "krščen Anton (12./13. 3.) — oče Anton Brodarič [~] ¼ zemljak [~] (1893 ½ — status menjava [~] ali napačno), mati Marija Klobučan? [~] (podcelica: Janez Jakobič × Neža Strauš? [~]); hiša 46 = PT LUKNJA (2. VPIS ISTA ZVEZA — P88 1893 r43 Brodarič × Klobučar; 15. dokaz v luknji 41–60, brez novih števil); botra Marjka Trotter [~]; babica PRAZEN; siv/moder pripis: »† 1?. 3. 95« (smrt otroka 1895, datum nejasen [~]); podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Anton (Mar 12/13) — father Anton Brodarič [~] quarter smallholder [~] (1893 ½ — a status change [~] or an error), mother Marija Klobučan? [~] (sub-cell: Janez Jakobič × Neža Strauš? [~]); house 46 = the PT GAP (2nd entry THE SAME COUPLE — P88 1893 r43 Brodarič × Klobučar; the 15th proof in the 41–60 gap, no new numbers); godparent Marjka Trotter [~]; midwife EMPTY; grey/blue note: »† Mar 1?, 95« (child death 1895, date unclear [~]); signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "87",
    bookSignature: "04105",
    year: 1895,
    scan: 80,
    page: 78,
    whatSi: "krščena Ana (22./22. 3.) — oče Marko Pegdirec [~] bajtar, mati Marjeta Pegdirec [~] (podcelica: Nikol. Hrižan × Marija Željko — povezava na h63, oče Hrižan 1887–1892 4×, in Željko verigo [~]); hiša 87 NOVA HIŠA v vzorcu (brez priora P77–P89); PEGDIREC prvič STARŠI (2×: h87 Marko + Marjeta in h37 r49) — familija, ki je do zdaj prevladovala kot botra/matere; botra Marija Hrižan [~]; babica PRAZEN; podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Ana (Mar 22/22) — father Marko Pegdirec [~] cottager, mother Marjeta Pegdirec [~] (sub-cell: Nikol. Hrižan × Marija Željko — a link to h63, father Hrižan 1887–1892 4×, and the Željko chain [~]); house 87 NEW HOUSE in the sample (no prior P77–P89); PEGDIREC as PARENTS for the first time (2×: h87 Marko + Marjeta and h37 r49) — the family that until now dominated as godparents/mothers; godparent Marija Hrižan [~]; midwife EMPTY; signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1895,
    scan: 80,
    page: 78,
    whatSi: "krščena Ana (10./10. 4.) — oče Matija Brime [~] ½ zemljak, mati Barbara Jakobič [~] (podcelica: Janez Brime × Marja Jastobec? [~]); hiša 24 (3. VPIS ISTA ZVEZA Brinec/Brime × Jakobec/Jakobič: 1887 + 1893 + 1895; 1892 Jurajevič = menjava gospodinjstva, 1890 ANOMALIJA »Marija Brinec«); botra Marjeta Trotter [~]; babica PRAZEN; moder pripis 20. st.: »poročena 14. 5. 1912« [~]; podpis Jos. Rauq",
    whatEn: "baptized Ana (Apr 10/10) — father Matija Brime [~] half smallholder, mother Barbara Jakobič [~] (sub-cell: Janez Brime × Marja Jastobec? [~]); house 24 (3rd entry THE SAME COUPLE Brinec/Brime × Jakobec/Jakobič: 1887 + 1893 + 1895; 1892 Jurajevič = household change, 1890 ANOMALY »Marija Brinec«); godparent Marjeta Trotter [~]; midwife EMPTY; blue 20th-century note: »married May 14, 1912« [~]; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1895,
    scan: 80,
    page: 78,
    whatSi: "krščen Janez (29./29. 4.) — oče Janez Dragoš [~] ½ zemljak (Kurrent: Dragov/Dragoš; ISTI oče 3×), mati Barbara Cvitkovič? [~] (P87 »Civlkovič?« + P89 »Druppovič?« — trije bralci iste/nenavadne matere [~] MERI; podcelica: Martin?/Matija? Straus × Marija Jakobič — Straus mreža h71/h72); hiša 12 (3. VPIS); botra Marjeta Trotter [~]; babica PRAZEN; podpis Jos. Rauq",
    whatEn: "baptized Janez (Apr 29/29) — father Janez Dragoš [~] half smallholder (Kurrent: Dragov/Dragoš; THE SAME father 3×), mother Barbara Cvitkovič? [~] (P87 »Civlkovič?« + P89 »Druppovič?« — three readings of the same/remarkable mother [~]); sub-cell: Martin?/Matija? Straus × Marija Jakobič — the Straus network h71/h72); house 12 (3rd entry); godparent Marjeta Trotter [~]; midwife EMPTY; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1895,
    scan: 80,
    page: 78,
    whatSi: "krščen Nikolaj (4./4. 5.) — oče Nikolaj Šegina? [~] ½ zemljak, mati Marjeta Mihelt [~] (podcelica: Matija? Mihelt × Katarina Hrižan — Mihelt mreža h65/h20 + Hrižan h63 [~]); hiša 30 (3. DRUŽINA v 6 letih — 2× MENJAVA GOSPODINJSTVA: Milek 1890–91 → Jakljevič 1893 → Šegina 1895 — najbolj nestabilna hiša vzorca); botra Ana Krajan? [~]; babica PRAZEN; pripis: »† 9. 95« [~] (smrt otroka); podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Nikolaj (May 4/4) — father Nikolaj Šegina? [~] half smallholder, mother Marjeta Mihelt [~] (sub-cell: Matija? Mihelt × Katarina Hrižan — the Mihelt network h65/h20 + Hrižan h63 [~]); house 30 (the 3rd FAMILY in 6 years — 2× HOUSEHOLD CHANGE: Milek 1890–91 → Jakljevič 1893 → Šegina 1895 — the most unstable house in the sample); godparent Ana Krajan? [~]; midwife EMPTY; note: »† Sep 95« [~] (child death); signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04105",
    year: 1895,
    scan: 82,
    page: 80,
    whatSi: "krščen Matija (6./6. 8.) — oče Peter Pezdirec? [~] ¼ zemljak, mati Doroteja Šlepec [~] (podcelica: Matija Mihelt × Ana? Požek — zelo blizu starševskega para h65 r43: Mihelt oče z dvema ženama? ali napaka [~] MERI); hiša 20 NOVA HIŠA v vzorcu (brez priora P77–P89); ANOMALIJA: isti oče »Peter Pezdirec ¼« tudi na h37 (r49, 3,5 tedna kasneje, druga žena!) — dva istoimenska moža (oče+sin?) ali napaka [~]; botra Marjeta Trotter [~]; babica PRAZEN; pripis: »† 1896« [~] (datum nejasen); podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Matija (Aug 6/6) — father Peter Pezdirec? [~] quarter smallholder, mother Doroteja Šlepec [~] (sub-cell: Matija Mihelt × Ana? Požek — very close to the h65 r43 parent pair: a Mihelt father with two wives? or an error [~]); house 20 NEW HOUSE in the sample (no prior P77–P89); ANOMALY: the same father »Peter Pezdirec ¼« also at h37 (r49, 3.5 weeks later, another wife!) — two namesake men (father+son?) or an error [~]; godparent Marjeta Trotter [~]; midwife EMPTY; note: »† 1896« [~] (date unclear); signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1895,
    scan: 82,
    page: 80,
    whatSi: "krščena Neža (15./15. 8.) — oče Matija Mihelt [~] ½ zemljak (1887–1893 branec »Milek« — Kurrent varianta istega priimka [~]), mati Katarina Požek [~] (ISTA 2×: 1887 + 1895; podcelica: Peter Pezdirec? × Barbara ? [~]); hiša 65 (4. VPIS: 1887 + 1889 + 1893 + 1895 — mati Katarina Požek 2× enaka); botra Barbara Adlešič? [~]; babica PRAZEN; podpis Jos. Rauq",
    whatEn: "baptized Neža (Aug 15/15) — father Matija Mihelt [~] half smallholder (1887–1893 read as »Milek« — a Kurrent variant of the same surname [~]), mother Katarina Požek [~] (THE SAME 2×: 1887 + 1895; sub-cell: Peter Pezdirec? × Barbara ? [~]); house 65 (4th entry: 1887 + 1889 + 1893 + 1895 — mother Katarina Požek THE SAME twice); godparent Barbara Adlešič? [~]; midwife EMPTY; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1895,
    scan: 82,
    page: 80,
    whatSi: "krščena Marjeta (23./25. 8.) — oče Matija Urh [~] ½ zemljak, mati Marjeta Pegdirec [~] (podcelica: Jurij Straus × Barbara Straus — Straus mreža, h71 1894 oče Jurij Straus! [~] MERI); hiša 32 (5. VPIS — NAJDALJŠA ZVEZA VZORCA: Urh × Pegdirec/Pendirec/Margaretha ISTA 5× 1889–1895, statusi ¼/½/¼/½/½ [~]); botra Marjeta Trotter [~]; babica PRAZEN; moder pripis 20. st. nad vrstico: »umrla dne 3. 8. 1977« [~]; podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Marjeta (Aug 23/25) — father Matija Urh [~] half smallholder, mother Marjeta Pegdirec [~] (sub-cell: Jurij Straus × Barbara Straus — the Straus network; h71 1894 father Jurij Straus! [~]); house 32 (5th entry — THE LONGEST COUPLE IN THE SAMPLE: Urh × Pegdirec/Pendirec/Margaretha THE SAME 5× 1889–1895, statuses ¼/½/¼/½/½ [~]); godparent Marjeta Trotter [~]; midwife EMPTY; blue 20th-century note above the line: »died Aug 3, 1977« [~]; signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1895,
    scan: 82,
    page: 80,
    whatSi: "krščena Neža (28./28. 8.) — oče Janez Toško? [~] ½ zemljak, mati Ana Simec [~] (podcelica: Janez Kustec? × Ana Simec [~]); hiša 24 DVOM — forenzika izrezov 8–10× vztraja »24« (kot r22!), a DVE različni zvezi na isti hiši v 4 mesecih je anormalno; alternative: 21 (Požek hiša, P82) ali 27 [~] MERI, NE odloča — prva ponovitev hiše znotraj leta v vzorcu (P87 NARE); botra Marjeta Trotter [~]; babica PRAZEN; podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Neža (Aug 28/28) — father Janez Toško? [~] half smallholder, mother Ana Simec [~] (sub-cell: Janez Kustec? × Ana Simec [~]); house 24 DOUBTFUL — 8–10× crop forensics insist on »24« (as r22!), yet TWO different couples at the same house within 4 months is abnormal; alternatives: 21 (the Požek house, P82) or 27 [~] MEASURE, do not decide — the first within-year house repeat in the sample (P87 NARE); godparent Marjeta Trotter [~]; midwife EMPTY; signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "37",
    bookSignature: "04105",
    year: 1895,
    scan: 82,
    page: 80,
    whatSi: "krščena Ana (29./30. 8.) — oče Peter Pezdirec [~] ¼ zemljak (ANOMALIJA: isto ime+status kot h20 oče r40, druga žena! [~] MERI), mati Marija Lužanič? [~] (podcelica: Nikolaj Šelfo?/Željko? × Marija Šimec — Šelfo/Željko varianta? Simec mreža [~]); hiša 37 NOVA HIŠA v vzorcu (brez priora P77–P89); botra Marija Muh? [~]; babica PRAZEN; moder pripis matičarja 20. st.; podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Ana (Aug 29/30) — father Peter Pezdirec [~] quarter smallholder (ANOMALY: the same name+status as the h20 father r40, another wife! [~]), mother Marija Lužanič? [~] (sub-cell: Nikolaj Šelfo?/Željko? × Marija Šimec — a Šelfo/Željko variant? the Simec network [~]); house 37 NEW HOUSE in the sample (no prior P77–P89); godparent Marija Muh? [~]; midwife EMPTY; blue 20th-century registrar note; signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1895,
    scan: 83,
    page: 81,
    whatSi: "krščen Nikolaj (8./9. 9.) — oče Janez Brimec/Brinec [~] ½ zemljak (ISTI oče vseh 5×: 1888+1889+1890+1894+1895), mati Ana Mure? [~] (5. različno branje matere: Strauš → Strauš → Straus → Kure → Mure? — verjetno variante 1–2 pravih imen [~] MERI; podcelica: Janez Muc novac × Katarina Požek — Muc mreža r55/h91!); hiša 69 (5. VPIS); BOTRA PRAZNA (prva od 4 praznih botr septembra–decembra); babica PRAZEN; podpis Jan Jelez/Jelenuš?",
    whatEn: "baptized Nikolaj (Sep 8/9) — father Janez Brimec/Brinec [~] half smallholder (THE SAME father all 5×: 1888+1889+1890+1894+1895), mother Ana Mure? [~] (the 5th different reading of the mother: Strauš → Strauš → Straus → Kure → Mure? — probably variants of 1–2 real names [~]); sub-cell: Janez Muc novac × Katarina Požek — the Muc network r55/h91!); house 69 (5th entry); GODPARENT EMPTY (the first of 4 empty godparents Sep–Dec); midwife EMPTY; signature Jan Jelez/Jelenuš?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1895,
    scan: 83,
    page: 81,
    whatSi: "krščen Mihael (13./13. 9.) — oče Matija Straus [~] ½ zemljak, mati Marija Jakobič [~] (ISTA ZVEZA — 5. VPIS: 1889+1891+1893+1895; 1888 »Barbara Husič?« = varianta [~]; podcelica: Matija Straus × Barbara Jakobič — okolščno ujema očetovo ime: ali podcelica = starši očeta? semantika ODPRTA [~] MERI); hiša 72 — Straus veriga h71/h72; BOTRA PRAZNA; babica PRAZEN; moder pripis matičarja 20. st.; podpis Jos. Rauq",
    whatEn: "baptized Mihael (Sep 13/13) — father Matija Straus [~] half smallholder, mother Marija Jakobič [~] (THE SAME COUPLE — 5th entry: 1889+1891+1893+1895; 1888 »Barbara Husič?« = a variant [~]); sub-cell: Matija Straus × Barbara Jakobič — curiously matches the father's name: is the sub-cell the father's parents? semantics OPEN [~]); house 72 — the Straus chain h71/h72; GODPARENT EMPTY; midwife EMPTY; blue 20th-century registrar note; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04105",
    year: 1895,
    scan: 83,
    page: 81,
    whatSi: "krščen Janez (25./26. 9.) — oče Janez Muc [~] (stan: »mlinar in kovač?« [~]; OČE MENJAN: Novak 1893 → Muc 1895 — ponovna poroka ali napaka branja [~] MERI), mati Ana Kure [~] (ISTA kot 1893; podcelica: Jožef Željko × Katarina Kure — ŽELJKO VERIGA: h1 1892 Željko × Kure + h60 1894 Nikolaj Željko + podcelica h87 [~]); hiša 91 (2. VPIS); BOTRA PRAZNA; babica PRAZEN; podpis Franc Klunng? (NOV duhovnik od septembra — Klunnq/Klunng variante)",
    whatEn: "baptized Janez (Sep 25/26) — father Janez Muc [~] (occupation: »miller and smith?« [~]; FATHER CHANGED: Novak 1893 → Muc 1895 — remarriage or a reading error [~]), mother Ana Kure [~] (THE SAME as 1893; sub-cell: Jožef Željko × Katarina Kure — THE ŽELJKO CHAIN: h1 1892 Željko × Kure + h60 1894 Nikolaj Željko + the h87 sub-cell [~]); house 91 (2nd entry); GODPARENT EMPTY; midwife EMPTY; signature Franc Klunng? (a NEW priest from September — Klunnq/Klunng variants)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04105",
    year: 1895,
    scan: 84,
    page: 82,
    whatSi: "krščena Marija (1./1. 12.) — oče Janez Kuhar?/Kuklar? [~] ½ zemljak (Kurrent K/H), mati Katarina Klobučar [~] (podcelica: Janez Požek × Barbara Kure — ISTI »Janez Požek« kot h58 oče r15! Požek × Kure mreža (h21 1887: Janez Požek × Marija Brinec) [~] MERI); hiša 29 (MENJAVA GOSPODINJSTVA — hiša epidemije 1886 (Mileh ×3, P78) + »hiša kuge« Milek × Križan 1888+1892 → povsem nova zveza Kuhar? × Klobučar; epidemija popolnoma prekinjena); BOTRA PRAZNA; babica PRAZEN; podpis Franc Klunng?",
    whatEn: "baptized Marija (Dec 1/1) — father Janez Kuhar?/Kuklar? [~] half smallholder (Kurrent K/H), mother Katarina Klobučar [~] (sub-cell: Janez Požek × Barbara Kure — THE SAME »Janez Požek« as the h58 father r15! the Požek × Kure network (h21 1887: Janez Požek × Marija Brinec) [~]); house 29 (HOUSEHOLD CHANGE — the 1886 epidemic house (Mileh ×3, P78) + the »plague house« Milek × Križan 1888+1892 → a brand-new couple Kuhar? × Klobučar; the epidemic fully broken); GODPARENT EMPTY; midwife EMPTY; signature Franc Klunng?",
    status: "DOCUMENTED",
  },
  // ——— P91 razširitev: KRSTNA KNJIGA 04105 — polno leto 1896 (okvir skeni
  // 85–92 == strani 83–90; stran == sken − 2 ZA CELO LETO — novela P89
  // potrjena 3. leto; sken 73 podvojen, NI citiran; glava »1896« na str. 83
  // po 1895 row 73; leto 1896 ima 94 zveznih vrstic — NAJDALJŠE doslej;
  // prelom 1897 na str. 83+8 = str. 91 = sken 93 po row 94 — oznake
  // ponastavljene, novela P83 potrjena 9. leto) — 14 vpisov / 14 hiš — NARE
  // (3. leto po P87/P89; 0 neberljivih; 3 NOVE hiše 9/14/45 po P90 »3 nove«;
  // kumulativno 199 vpisov / 71 hiš čez tri knjige in ENAJST LET; NOVA
  // LUKNJA ŠTEVILKA 45 — 16. dokazana v 41–60, prva nova od P88; NOVELA
  // babica potrjena 2. leto — 14/14 PRAZNO, Trotter žene 0×; NOV duhovnik
  // Fr. Šuvar? dominanten 9/14 (Rauq 4×, r5 brez podpisa); statusi ½ × 12 +
  // bajtar × 2 — prvo leto brez ¼; SIDRA: h1 Željko × Kure 3. VPIS ISTA
  // zveza (1888+1892+1896 — 8 let; botra ISTI priimki kot starši vse 3×),
  // h63 oče ISTI 5× (1887–1896), h30 Šegina × Mihelt ISTA zveza 2. leto,
  // h41 Hušič × Jakobič 4. VPIS ISTA zveze, h15 Jaklič × Brinec 3. VPIS,
  // h36 Križan × Straucelj 2. VPIS, h53 Pendirec? × Hrižan 3. VPIS variante,
  // h31 MENJAVA (Fapič → Pendirec bajtar), h25 KLEPEC NAZAJ, h46 mati
  // menjana/varianta (Klobučar → Kramarič?), h26 Jakobič × Stubljar na
  // DRUGI hiši (75 → 26 — selitev ali napaka [~]), h14 neimenovan otrok +
  // brez botre/podpisa, h45 Straus signal 3. hiša) ———
  {
    houseNo: "9",
    bookSignature: "04105",
    year: 1896,
    scan: 85,
    page: 83,
    whatSi: "krščena Neža (10./10. 1.) — oče Janez Jakobič? [~] ½ zemljak, mati Marija Žumič? [~]; hiša 9 NOVA HIŠA v vzorcu (forenzika 5x: jasno 9); pripis: »† 3/3. 96« — smrt dojenčke (starost ~7 tednov); botra Nikol. Požek [~] + Marija Strauš? [~] (Požek botra 8. leto); mati Žumič = ISTA branja kot Vtok r80 (Oktober) [~] MERI; babica PRAZNA; podpis Fr. Šuvar?",
    whatEn: "baptized Neža (Jan 10/10) — father Janez Jakobič? [~] half smallholder, mother Marija Žumič? [~]; house 9 NEW HOUSE in the sample (5x forensics: clearly 9); note: »† Mar 3, 96« — infant death (~7 weeks); godparents Nikol. Požek [~] + Marija Strauš? [~] (Požek godparent, the 8th year); the mother Žumič = THE SAME reading as Vtok r80 (October) [~]; midwife EMPTY; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1896,
    scan: 85,
    page: 83,
    whatSi: "N. moškega spola (neimenovan; druga vrstica pod reparaturnim trakom neberljiva [?]) — rojstva 21., KRSTA PRAZNA (morda umrl pred krstom [~]); oče Janez Brinec [~] ½ zemljak, mati Marija Pendirec? [~]; hiša 14 NOVA HIŠA v vzorcu (forenzika 5x: jasno 14); BREZ botre + BREZ podpisa — 3. primer vzorca (po P86 r39 h61, P87 r70 h61); oče Brinec = h69 familija? [~] MERI; babica PRAZNA",
    whatEn: "N. male sex (unnamed; the 2nd line under the repair tape illegible [?]) — born Jan 21, BAPTISM EMPTY (perhaps died before baptism [~]); father Janez Brinec [~] half smallholder, mother Marija Pendirec? [~]; house 14 NEW HOUSE in the sample (5x forensics: clearly 14); NO godparents + NO signature — the 3rd such case in the sample (after P86 r39 h61, P87 r70 h61); father Brinec = the h69 family? [~]; midwife EMPTY",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1896,
    scan: 86,
    page: 84,
    whatSi: "krščen Matija (23./23. 2.) — oče Marko Pendirec? [~] bajtar, mati Katarina Žugelj? [~]; hiša 31 MENJAVA GOSPODINJSTVA (1894 Fapič × Straus 4. VPIS → 1896 Pendirec bajtar × Žugelj — povsem nova zveza; 2. menjava na h31; forenzika 7x: jasno 31, prvi prebir 37 [~]); botra Nikol. Hrižan [~] (h63 oče familija) + Marija Žugelj? [~] (ISTA priimek kot mati — sorodstvo? [~]); babica PRAZNA; moder: umrl 9.11.1971; podpis Fr. Šuvar?",
    whatEn: "baptized Matija (Feb 23/23) — father Marko Pendirec? [~] cottager, mother Katarina Žugelj? [~]; house 31 HOUSEHOLD CHANGE (1894 Fapič × Straus, the 4th entry → 1896 Pendirec cottager × Žugelj — a brand-new couple; the 2nd change on h31; 7x forensics: clearly 31, first read 37 [~]); godparents Nikol. Hrižan [~] (the h63 father family) + Marija Žugelj? [~] (THE SAME surname as the mother — kinship? [~]); midwife EMPTY; blue: died Nov 9, 1971; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1896,
    scan: 86,
    page: 84,
    whatSi: "krščena Marija (14./14. 2.) — oče Janez Križan? [~] ½ zemljak (status ¼ → ½ [~]), mati Katarina Straucelj? [~] (ISTA ZVEZA kot 1894 — 2. VPIS; KRIŽAN 2. GENERACIJA kontinuiteta); hiša 36 TRI-VIRSKA (poroka 04455 1882 + krstna 1886 ×2 + mrliška 04894 1887) dobi 5. in 6. vir (forenzika 5x: jasno 36); botra Matija Pendirec? [~] + Marija Straus? [~]; babica PRAZNA; moder: umrla 22.5.1966; podpis Jos. Rauq",
    whatEn: "baptized Marija (Feb 14/14) — father Janez Križan? [~] half smallholder (status ¼ → ½ [~]), mother Katarina Straucelj? [~] (THE SAME COUPLE as 1894 — the 2nd entry; KRIŽAN 2nd GENERATION continuity); house 36 THREE-SOURCE (the 1882 marriage + the 1886 baptisms ×2 + the 1887 death) gains its 5th and 6th sources (5x forensics: clearly 36); godparents Matija Pendirec? [~] + Marija Straus? [~]; midwife EMPTY; blue: died May 22, 1966; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1896,
    scan: 87,
    page: 85,
    whatSi: "krščen Anton (13./13. 4.) — oče Nikolaj Željko [~] ½ zemljak, mati Katarina Kure [~]; hiša 1 (forenzika 5x: jasno 1 — najnižja hiša vzorca) — 3. VPIS ISTA ZVEZA (P83 1888 »Zeljth« [~] + P87 1892 + 1896 — 8 let, 2. najdaljša zveza vzorca); botra Nikolaj Željko [~] + Katarina Kure [~] — ISTI PRIIMKI KOT STARŠI vse 3× (začarani krog familije); ŽELJKO VERIGA 8 signalov; babica PRAZNA; moder: umrl 14.2.1972 v Gribljah; podpis Fr. Šuvar?",
    whatEn: "baptized Anton (Apr 13/13) — father Nikolaj Željko [~] half smallholder, mother Katarina Kure [~]; house 1 (5x forensics: clearly 1 — the lowest house number in the sample) — the 3rd ENTRY THE SAME COUPLE (P83 1888 »Zeljth« [~] + P87 1892 + 1896 — 8 years, the 2nd longest couple in the sample); godparents Nikolaj Željko [~] + Katarina Kure [~] — THE SAME SURNAMES AS THE PARENTS all 3× (the family's closed circle); THE ŽELJKO CHAIN 8 signals; midwife EMPTY; blue: died Feb 14, 1972 in Griblje; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04105",
    year: 1896,
    scan: 87,
    page: 85,
    whatSi: "krščena Ana (19./18. 4. [~]) — oče Janez Klepec?/Mlepec? [~] ½ zemljak, mati Katarina Tome? [~]; hiša 25 (forenzika 10x + REFERENČNA PRIMERJAVA Gradac 25: jasno 25 — PRVI PREBIR 26 NAPAČEN, Kurrent 5/6) — KLEPEC NAZAJ (poroka 04455 1886 »Klepec GRIBLJE 25«; 1893 Hrižan × Požek menjava → 1896 vrnitev originalne familije [~] MERI); botra Miha Berkopec? [~] + Ana Berkopec? [~]; babica PRAZNA; moder: poročena 6.1.1932 + umrla 10.9.1984 (ENŠO — sodobni matični vir); podpis Fr. Šuvar?",
    whatEn: "baptized Ana (Apr 19/18 [~]) — father Janez Klepec?/Mlepec? [~] half smallholder, mother Katarina Tome? [~]; house 25 (10x forensics + REFERENCE COMPARISON with Gradac 25: clearly 25 — THE FIRST READ 26 WRONG, Kurrent 5/6) — KLEPEC BACK (the 1886 marriage »Klepec GRIBLJE 25«; the 1893 Hrižan × Požek change → 1896 the original family returns [~]); godparents Miha Berkopec? [~] + Ana Berkopec? [~]; midwife EMPTY; blue: married Jan 6, 1932 + died Sep 10, 1984 (ENŠO — a modern registrar source); signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1896,
    scan: 87,
    page: 85,
    whatSi: "krščen Nikolaj (16./16. 4.) — oče Anton Brodarič [~] ½ zemljak, mati Ana Kramarič? [~] (MATI MENJANA ali varianta: 1893+1895 Klobučar/Klobučan? → 1896 Kramarič? [~] MERI); hiša 46 = PT LUKNJA (forenzika 5x: jasno 46 — PRVI PREBIR 16 NAPAČEN) — 3. VPIS Brodarič (P88+P90+P91), 3. DOKAZ LUKNJE 41–60; botra Nikolaj Željko [~] (ŽELJKO VERIGA 8. signal) + Neža Štrauš? [~]; pripis: »† 29/3. 97?/96?« [~]; babica PRAZNA; podpis Fr. Šuvar?",
    whatEn: "baptized Nikolaj (Apr 16/16) — father Anton Brodarič [~] half smallholder, mother Ana Kramarič? [~] (MOTHER CHANGED or a variant: 1893+1895 Klobučar/Klobučan? → 1896 Kramarič? [~]); house 46 = the PT GAP (5x forensics: clearly 46 — THE FIRST READ 16 WRONG) — the 3rd ENTRY Brodarič (P88+P90+P91), the 3rd PROOF of the 41–60 gap; godparent Nikolaj Željko [~] (THE ŽELJKO CHAIN, the 8th signal) + Neža Štrauš? [~]; note: »† Mar 29, 97?/96?« [~]; midwife EMPTY; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04105",
    year: 1896,
    scan: 88,
    page: 86,
    whatSi: "krščen Matija (9./9. 6.) — oče Janez Jakobič? [~] ½ zemljak, mati Marija Stubljar?/Stubljan? [~]; hiša 26 (forenzika 10x: jasno 26 — sklenjeni lok 6 v nasprotju s 5 v r25) — ISTI PRIIMKI kot h75 zveza (P87 1892 + P89 1894: Janez Jakobič × Marija Stubljar) — 3. vpis zveze na DRUGI hiši (75 → 26: selitev gospodinjstva ali napaka hiše [~] MERI, forenzika vztraja 26); botra Matija Brimec? [~] + Ana Požek [~] (Požek 8. leto); babica PRAZNA; moder: por. 10/2. 1948 + umrla 2.9.1975; podpis Fr. Šuvar?",
    whatEn: "baptized Matija (Jun 9/9) — father Janez Jakobič? [~] half smallholder, mother Marija Stubljar?/Stubljan? [~]; house 26 (10x forensics: clearly 26 — the closed loop 6 in contrast with the 5 in r25) — THE SAME SURNAMES as the h75 couple (P87 1892 + P89 1894: Janez Jakobič × Marija Stubljar) — the 3rd entry of the couple on ANOTHER house (75 → 26: a household move or a house error [~], forensics insist on 26); godparents Matija Brimec? [~] + Ana Požek [~] (Požek the 8th year); midwife EMPTY; blue: married Feb 10, 1948 + died Sep 2, 1975; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04105",
    year: 1896,
    scan: 88,
    page: 86,
    whatSi: "krščen Anton (9./9. 6.) — oče Matija Hušič? [~] ½ zemljak, mati Neža Jakobič? [~]; hiša 41 = PT LUKNJA (forenzika 5x: jasno 41) — 4. VPIS ISTA ZVEZA Hušič/Hrušič × Jakobič/Jakobčič (P85 1890 ×2 + P88 1893 + 1896 — najbolj stabilna zveza na luknji), 4. DOKAZ LUKNJE 41–60; botra Miha Pozdirec? [~] (Pegdirec familija) + Marija Jakobič? [~] (ISTA priimek kot mati — sorodstvo? [~]); ime otroka Anton (prvi prebir Jožef [~]); babica PRAZNA; moder: poročen 26/5 1919 + 6.2.1975; podpis Fr. Šuvar?",
    whatEn: "baptized Anton (Jun 9/9) — father Matija Hušič? [~] half smallholder, mother Neža Jakobič? [~]; house 41 = the PT GAP (5x forensics: clearly 41) — the 4th ENTRY THE SAME COUPLE Hušič/Hrušič × Jakobič/Jakobčič (P85 1890 ×2 + P88 1893 + 1896 — the most stable couple on the gap), the 4th PROOF of the 41–60 gap; godparents Miha Pozdirec? [~] (the Pegdirec family) + Marija Jakobič? [~] (THE SAME surname as the mother — kinship? [~]); the child's name Anton (first read Jožef [~]); midwife EMPTY; blue: married May 26, 1919 + Feb 6, 1975; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04105",
    year: 1896,
    scan: 89,
    page: 87,
    whatSi: "krščena Ana (31./31. 7.) — oče Janez Jaklič? [~] ½ zemljak, mati Marija Brinec [~]; hiša 15 (forenzika 5x: jasno 15) — 3. VPIS ISTA ZVEZA (P82 1887 »Jakšič?« + P88 1893 + 1896 — Kurrent J/Š variante istega priimka [~]); botra Matija Jaklič? [~] + Barbara Adlešič? [~] (Adlešič 3. leto signalov); pripis: »† 1977?« [~]; babica PRAZNA; podpis Fr. Šuvar?",
    whatEn: "baptized Ana (Jul 31/31) — father Janez Jaklič? [~] half smallholder, mother Marija Brinec [~]; house 15 (5x forensics: clearly 15) — the 3rd ENTRY THE SAME COUPLE (P82 1887 »Jakšič?« + P88 1893 + 1896 — Kurrent J/Š variants of the same surname [~]); godparents Matija Jaklič? [~] + Barbara Adlešič? [~] (Adlešič, the 3rd year of signals); note: »† 1977?« [~]; midwife EMPTY; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1896,
    scan: 89,
    page: 87,
    whatSi: "krščena Ana (21./21. 8.) — oče Nikolaj Hrižan? [~] ½ zemljak, mati Katarina Pendirec? [~]; hiša 63 (forenzika 5x: jasno 63) — 5. VPIS: OČE ISTI VSEH 5× (1887 »Prižan?« + 1889 Hrigian? + 1890 Križan + 1892 Hrižan + 1896 — najbolj konstanten oče na eni hiši; Kurrent K/H variante); mati Pendirec/Pegdirec variante; botra Nikolaj Šegina? [~] (h30 oče familija) + Katarina Pendirec? [~] (ISTA priimek kot mati — sorodstvo? [~]); pripis: »† 19.96?« [~]; babica PRAZNA; podpis Fr. Šuvar?",
    whatEn: "baptized Ana (Aug 21/21) — father Nikolaj Hrižan? [~] half smallholder, mother Katarina Pendirec? [~]; house 63 (5x forensics: clearly 63) — the 5th ENTRY: THE FATHER THE SAME ALL 5× (1887 »Prižan?« + 1889 Hrigian? + 1890 Križan + 1892 Hrižan + 1896 — the most constant father on one house; Kurrent K/H variants); the mother Pendirec/Pegdirec variants; godparents Nikolaj Šegina? [~] (the h30 father family) + Katarina Pendirec? [~] (THE SAME surname as the mother — kinship? [~]); note: »† 1896?« [~]; midwife EMPTY; signature Fr. Šuvar?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1896,
    scan: 90,
    page: 88,
    whatSi: "krščen Martin (19./19. 9.) — oče Martin Straus? [~] bajtar, mati Barbara Doroteja? [~] (rod. celica: priimek ali drugo ime nejasno [~]); hiša 45 NOVA HIŠA v vzorcu + NOVA LUKNJA ŠTEVILKA (45 — 16. dokazana v 41–60, prva nova od P88; forenzika 5x: jasno 45 — NI 46, primerjava z r31 s87); ime otroka Martin (prvi prebir Marija [~]); Straus signal na TRETJI hiši (h71 Jurij + h72 Matija + h45 Martin [~] MERI); botra POD TRAKOM NEBERLJIVA [?]; babica PRAZNA?; podpis Jos. Rauq",
    whatEn: "baptized Martin (Sep 19/19) — father Martin Straus? [~] cottager, mother Barbara Doroteja? [~] (the род. cell: surname or another name unclear [~]); house 45 NEW HOUSE in the sample + A NEW GAP NUMBER (45 — the 16th proven in 41–60, the first new one since P88; 5x forensics: clearly 45 — NOT 46, compared with r31 s87); the child's name Martin (first read Marija [~]); the Straus signal on a THIRD house (h71 Jurij + h72 Matija + h45 Martin [~]); godparents UNDER THE REPAIR TAPE, illegible [?]; midwife EMPTY?; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1896,
    scan: 91,
    page: 89,
    whatSi: "krščena Barbara (20./20. 10.) — oče Janez Pendirec? [~] ½ zemljak, mati Marija Hrižan [~]; hiša 53 = PT LUKNJA (forenzika 5x: jasno 53) — ISTA ZVEZA VARIANTE, 3. VPIS (P86 1891 »Pozdirec × Križan« + P89 1894 »Pegdirec × Hrižan« + 1896 »Pendirec × Hrižan« — Kurrent P/K + K/H variante istih dveh familij), 3. DOKAZ LUKNJE 41–60; botra Anton Brodarič? [~] (h46 oče familija) + Ana Šlce?/Štoc? [~]; babica Ana Hrižan (1891/1894) izgine — mati Marija Hrižan (sorodstvo? [~]); babica PRAZNA; podpis Jos. Rauq",
    whatEn: "baptized Barbara (Oct 20/20) — father Janez Pendirec? [~] half smallholder, mother Marija Hrižan [~]; house 53 = the PT GAP (5x forensics: clearly 53) — THE SAME COUPLE IN VARIANTS, the 3rd ENTRY (P86 1891 »Pozdirec × Križan« + P89 1894 »Pegdirec × Hrižan« + 1896 »Pendirec × Hrižan« — Kurrent P/K + K/H variants of the same two families), the 3rd PROOF of the 41–60 gap; godparent Anton Brodarič? [~] (the h46 father family) + Ana Šlce?/Štoc? [~]; the midwife Ana Hrižan (1891/1894) disappears — the mother Marija Hrižan (kinship? [~]); midwife EMPTY; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1896,
    scan: 92,
    page: 90,
    whatSi: "krščena Katarina (14./16. 12.) — oče Nikolaj Šegina? [~] ½ zemljak, mati Marjeta Mihelt? [~]; hiša 30 (forenzika 10x: jasno 30 — PRVI PREBIR 25 NAPAČEN, podolgovata zanka 0 ne kljukasta 5; starša Šegina × Mihelt = h30 familija 1895 to potrdita) — ISTA ZVEZA 2. leto (P90 1895 r27 — 3. DRUŽINA se je UNESELILA, po 2 menjavah končno kontinuiteta 1895+1896); botra Nikolaj Hrižan? [~] (h63 oče familija) + Katarina Mehle? [~]; babica PRAZNA; moder: umrla 16.11.1971 v Komorah; podpis Jos. Rauq",
    whatEn: "baptized Katarina (Dec 14/16) — father Nikolaj Šegina? [~] half smallholder, mother Marjeta Mihelt? [~]; house 30 (10x forensics: clearly 30 — THE FIRST READ 25 WRONG, an elongated closed loop 0 not a hooked 5; the parents Šegina × Mihelt = the h30 family of 1895 confirm it) — THE SAME COUPLE 2nd year (P90 1895 r27 — the 3rd FAMILY has SETTLED, after 2 changes finally continuity 1895+1896); godparents Nikolaj Hrižan? [~] (the h63 father family) + Katarina Mehle? [~]; midwife EMPTY; blue: died Nov 16, 1971 in Komore; signature Jos. Rauq",
    status: "DOCUMENTED",
  },

  // ——— P92 razširitev: KRSTNA KNJIGA 04105 — polno leto 1897 (okvir skeni
  // 93–101 == strani 91–98; NOVELA P92: sken 97 = PODVOJEN (duplikat s96 =
  // str. 94, 2. znani duplikat po skenu 73) — NOVELA P89 (stran == sken − 2)
  // velja samo do skena 96, od skena 98 stran == sken − 3 (artefakt
  // duplikata, ne nova številčenja); glava »Leto 1897« na str. 91 po 1896 row
  // 94; leto 1897 ima 85 vrstic; prelom 1898 na str. 98 = sken 101 po row 85
  // — oznake ponastavljene, novela P83 potrjena 10. leto) — 19 vpisov / 18
  // hiš — NARE (4. leto po P87/P89/P91; 0 neberljivih; h31 2 vpisa v enem
  // letu; kumulativno 217 vpisov / 74 hiš čez tri knjige in DVANAEST LET
  // (h61 sidro združeno s P79-era placeholderjem — ne dupliran); 3
  // NOVE hiše 10/40/43; NOVA LUKNJA ŠTEVILKA 43 — 17. dokazana v 41–60;
  // NOVELA babica 3. leto — 19/19 PRAZNO; DUHOVNIKI: Šuvar IZGINE, Klun 11×
  // + Rauq 8× — mešano leto; PRVI NEZAKONSKI vpis od P90: r31 sama mati
  // Pozdirec; DOJENČIJSKA UMRLJIVOST 7/19 — najvišje doslej; KURRENT
  // FORENZIKA 6 popravkov: h23/h24 dve hiši, Grisice≠Griblje (r11
  // izključen), Otok≠Griblje (r65 izključen), h16≠10, row 59/62/64, h45 mati
  // Spudič = POPRAVEK P91 prebira »Doroteja?«; SIDRA: h45 Straus × Spudič
  // 2. VPIS ISTA ZVEZA (1896+1897), h46 Brodarič 4. VPIS + mati 3. varianta
  // (Klobučar → Kramarič? → Harašimovič?), h31 Straus kompleks (1894 Fapič?×
  // Straus + 1896 Pendirec?×Žugelj + 1897 obe nazaj), h60 Željko 4. dokaz
  // luknje, h61 botra = h1 PAR (Željko × Kure — ŽELJKO VERIGA), h63 IZGINE
  // (konec 5-letne serije istega očeta), botra Hrižan 3× po izgini h63) ———
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1897,
    scan: 93,
    page: 91,
    whatSi: "krščen Anton (22./22. 1.) — oče Janez Dragar [~] ½ zemljak, mati Barbara Divkovič [~]; hišna 12 forenzika 5x: jasno 12; botra Marija Straus [~] + Marija Jakobič [~] (Straus veriga); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Anton (Jan 22/22) — father Janez Dragar [~] half smallholder, mother Barbara Divkovič [~]; house no. 12 (5x forensics: clearly 12); godparents Marija Straus [~] + Marija Jakobič [~] (the Straus chain); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1897,
    scan: 94,
    page: 92,
    whatSi: "krščena Marija (3./4. 2.) — oče Matija Perdune [~] ½ zemljak, mati Ana Jakobič [~]; hišna 32 forenzika 5x: jasno 32; botra Anton Pozdarič [~] + Katarina Hrižan [~]; pripis »† 24/1. 98« [~] — smrt ~11-mesečne (dojenčijska umrljivost 1/7); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Feb 3/4) — father Matija Perdune [~] half smallholder, mother Ana Jakobič [~]; house no. 32 (5x forensics: clearly 32); godparents Anton Pozdarič [~] + Katarina Hrižan [~]; note »† Jan 24, 98« [~] — death at ~11 months (infant mortality 1/7); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04105",
    year: 1897,
    scan: 94,
    page: 92,
    whatSi: "krščen Jožef (3./3. 3.) — oče Janez Brinec [~] ½ zemljak, mati Marija Perdune [~]; hiša 10 NOVA HIŠA v vzorcu (brez priora P77–P91; PT hiša hiša-11 v atlasu) — forenzika 5x: jasno 10; botra Martin Hrižan [~] + Katarina Požek [~]; pripis »† 5/9. 97« [~] — smrt ~6-mesečnega (2/7); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Jožef (Mar 3/3) — father Janez Brinec [~] half smallholder, mother Marija Perdune [~]; house 10 A NEW HOUSE in the sample (no prior P77–P91; a PT house, hiša-11 in the atlas) — 5x forensics: clearly 10; godparents Martin Hrižan [~] + Katarina Požek [~]; note »† Sep 5, 97« [~] — death at ~6 months (2/7); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1897,
    scan: 94,
    page: 92,
    whatSi: "krščena Marjeta (10./10. 3.) — oče Matija Brinec [~] ½ zemljak, mati Barbara Jakobič [~]; hišna 24 forenzika 5x: jasno 24 — KRITIČNO: vzporedna r38 = jasno 23, DVE RAZLIČNI Brinec hiši (prvi prebir »oba 23« napačen); botra Janez Brinec + Marija Jakobič (ISTI priimki kot starši); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Marjeta (Mar 10/10) — father Matija Brinec [~] half smallholder, mother Barbara Jakobič [~]; house no. 24 (5x forensics: clearly 24 — CRITICAL: the parallel r38 = clearly 23, TWO DIFFERENT Brinec houses; the first read »both 23« wrong); godparents Janez Brinec + Marija Jakobič (THE SAME surnames as the parents); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "37",
    bookSignature: "04105",
    year: 1897,
    scan: 95,
    page: 93,
    whatSi: "krščena Marta (15./16. 4.) — oče Matko Pendirec [~] ½ zemljak (ime delno raztrgano), mati Katarina Zugelj [~]; hišna 37 forenzika 5x: jasno 37 (odprta zanka 3, ne 8); botra Nikolaj Željko [~] (ŽELJKO VERIGA — botra signal) + Katarina Hrižan [~]; pripis »† 17/9. 97« [~] (3/7); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Marta (Apr 15/16) — father Matko Pendirec [~] half smallholder (name partly torn), mother Katarina Zugelj [~]; house no. 37 (5x forensics: clearly 37 — an open loop 3, not 8); godparents Nikolaj Željko [~] (THE ŽELJKO CHAIN — godparent signal) + Katarina Hrižan [~]; note »† Sep 17, 97« [~] (3/7); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04105",
    year: 1897,
    scan: 95,
    page: 93,
    whatSi: "krščena Marija (21./22. 4.) — oče Anton Brinec [~] ½ zemljak, mati Ana Šutala [~]; hiša 54 = PT LUKNJA (forenzika 5x: jasno 54) — 2. DOKAZ LUKNJE po P79 1886; botra Janez Požek? [~] + Katarina Hrižan [~] (Hrižan botra 3× v letu); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Marija (Apr 21/22) — father Anton Brinec [~] half smallholder, mother Ana Šutala [~]; house 54 = the PT GAP (5x forensics: clearly 54) — the 2nd PROOF OF THE GAP after P79 1886; godparents Janez Požek? [~] + Katarina Hrižan [~] (Hrižan godmother 3× in the year); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1897,
    scan: 95,
    page: 93,
    whatSi: "krščena Ana (26./26. 4.) — oče Nikolaj Željko [~] ½ zemljak, mati Marija Brodarič [~]; hiša 60 = PT LUKNJA — 4. DOKAZ (P87+P89+P91+1897); ISTA ZVEZA Željko × Brodarič; botra Marta Pozdirec [~] + Marija Plepec [~]; pripis »† 16/2. 98« [~] (4/7); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Ana (Apr 26/26) — father Nikolaj Željko [~] half smallholder, mother Marija Brodarič [~]; house 60 = the PT GAP — the 4th PROOF (P87+P89+P91+1897); THE SAME COUPLE Željko × Brodarič; godparents Marta Pozdirec [~] + Marija Plepec [~]; note »† Feb 16, 98« [~] (4/7); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "2",
    bookSignature: "04105",
    year: 1897,
    scan: 95,
    page: 93,
    whatSi: "krščen Peter (29./29. 4.) — oče Miha Vhebec? [~] ½ zemljak (Vehovec/Vrbec? — Kurrent V/H), mati Ana Jakobič [~]; hiša 2 (5. pin; s93 r11 »Grisice 2 Marija« je DRUGA vas — forenzika: jasno ne-Griblje, izključen); botra Janez Botkovec [~] + Ana Žumič? [~]; pripis »† 7/6. 97« — smrt ~5-tedenskega (5/7); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Peter (Apr 29/29) — father Miha Vhebec? [~] half smallholder (Vehovec/Vrbec? — Kurrent V/H), mother Ana Jakobič [~]; house 2 (the 5th pin; s93 r11 »Grisice 2 Marija« is ANOTHER village — forensics: clearly not-Griblje, excluded); godparents Janez Botkovec [~] + Ana Žumič? [~]; note »† Jun 7, 97« — death at ~5 weeks (5/7); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "43",
    bookSignature: "04105",
    year: 1897,
    scan: 95,
    page: 93,
    whatSi: "krščen Florijan (4./4. 5.) — OČE PRAZEN (NEZAKONSKI VPIS — prvi od P90!), mati Katarina Pozdirec [~] SAMA MATI ¼ zemljatva; hiša 43 = NOVA LUKNJA ŠTEVILKA (17. dokazana v 41–60 — prva dokumentacija; forenzika 5x: jasno 43 [~] NA RAZPOKI); botra Nikolaj Požek [~] + Marija Veh? [~]; pripis 20. st.: »Doučena, due 9. julij 1949« + EHS ČG 0605891505079 (20.12.1982); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Florijan (May 4/4) — FATHER EMPTY (AN ILLEGITIMATE ENTRY — the first since P90!), mother Katarina Pozdirec [~] SOLO MOTHER ¼ land; house 43 = A NEW GAP NUMBER (the 17th proven in 41–60 — the first documentation; 5x forensics: clearly 43 [~] ON THE CREASE); godparents Nikolaj Požek [~] + Marija Veh? [~]; 20th-c. note: »Doučena, due Jul 9, 1949« + EHS ČG 0605891505079 (Dec 20, 1982); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04105",
    year: 1897,
    scan: 96,
    page: 94,
    whatSi: "krščen Peter (24./24. 6.) — oče Matija Brinec [~] ½ zemljak, mati Marija Petrlie? [~]; hišna 23 forenzika 5x: jasno 23 — vzporedna r21 = jasno 24, DVE RAZLIČNI Brinec hiši (desni rob str. 94 raztrgan — starši brani iz duplikata s97); botra Janez Jaklič [~] + Katarina Pozdirec [~]; pripis »† 3/9. 99« [~] — smrt ~2-letnega (6/7); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Peter (Jun 24/24) — father Matija Brinec [~] half smallholder, mother Marija Petrlie? [~]; house no. 23 (5x forensics: clearly 23 — the parallel r21 = clearly 24, TWO DIFFERENT Brinec houses; the right edge of p. 94 torn — the parents read from the s97 duplicate); godparents Janez Jaklič [~] + Katarina Pozdirec [~]; note »† Sep 3, 99« [~] — death at ~2 years (6/7); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1897,
    scan: 96,
    page: 94,
    whatSi: "krščena Ana (26./27. 6.) — oče Anton Brodarič [~] ½ zemljak, mati Ana Harašimovič? [~] (5x forenzika: jasno H- — NE Kramarič; 3. VARIANTA MATERE: 1893+1895 Klobučar/Klobučan? → 1896 Kramarič? → 1897 Harašimovič?); hiša 46 = PT LUKNJA — 4. VPIS Brodarič (P88+P90+P91+1897); botra Nikolaj Željko [~] (ŽELJKO VERIGA) + Neža Struclj? [~]; pripis »† 15.3.1931« (odrasla, matičar); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Ana (Jun 26/27) — father Anton Brodarič [~] half smallholder, mother Ana Harašimovič? [~] (5x forensics: clearly H- — NOT Kramarič; the 3rd MOTHER VARIANT: 1893+1895 Klobučar/Klobučan? → 1896 Kramarič? → 1897 Harašimovič?); house 46 = the PT GAP — the 4th ENTRY Brodarič (P88+P90+P91+1897); godparents Nikolaj Željko [~] (THE ŽELJKO CHAIN) + Neža Struclj? [~]; note »† Mar 15, 1931« (an adult, the registrar); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1897,
    scan: 98,
    page: 95,
    whatSi: "krščena Marija (9./10. 9.) — oče Martin Sapič? [~] ½ zemljak (S/F Kurrent varianta — P89 1894 »Fapič × Straus« ista zveza!), mati Margareta Straus [~]; hišna 31 forenzika 5x: jasno 31 — STRAUS KOMPLEKS: 1894 Fapič?×Straus → 1896 Pendirec?×Žugelj (menjava) → 1897 OBÉ nazaj (2 vpisa v enem letu!); botra Marko Klobučar [~] + Katarina Pozdirec [~]; pripis 20. st.: »Umrla 14.4.1953 v Gribljah« + MMK Novo mesto 1932; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Sep 9/10) — father Martin Sapič? [~] half smallholder (an S/F Kurrent variant — P89 1894 »Fapič × Straus« the same couple!), mother Margareta Straus [~]; house no. 31 (5x forensics: clearly 31) — THE STRAUS COMPLEX: 1894 Fapič?×Straus → 1896 Pendirec?×Žugelj (a change) → 1897 BOTH back (2 entries in one year!); godparents Marko Klobučar [~] + Katarina Pozdirec [~]; 20th-c. note: »Died Apr 14, 1953 in Griblje« + MMK Novo mesto 1932; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1897,
    scan: 98,
    page: 95,
    whatSi: "krščena Barbara (12./13. 9.) — oče Janez Jaklič? [~] ½ zemljak, mati Marija Brinec [~]; hišna 16 forenzika 5x: jasno 16 (PRVI PREBIR »10« NAPAČEN) — 3. pin; botra Matija Brinec [~] + Barb. Adlešič? [~]; pripis 20. st.: »poročena 19/9. 1919« + »Umrla 22.7.1981 v Gradcu (MMU Gradec 1.1981, str. 87)«; babica PRAZNA; podpis Jos. Rauq? [~] (pega)",
    whatEn: "baptized Barbara (Sep 12/13) — father Janez Jaklič? [~] half smallholder, mother Marija Brinec [~]; house no. 16 (5x forensics: clearly 16 — THE FIRST READ »10« WRONG) — the 3rd pin; godparents Matija Brinec [~] + Barb. Adlešič? [~]; 20th-c. notes: »married Sep 19, 1919« + »died Jul 22, 1981 in Gradec (MMU Gradec 1.1981, p. 87)«; midwife EMPTY; signature Jos. Rauq? [~] (a stain)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1897,
    scan: 99,
    page: 96,
    whatSi: "krščen Janez (12./12. 10.) — oče Janez Berkovec? [~] ½ zemljak (Botkovec/Barkovec? — Kurrent o/a + r/t), mati Katarina Klobučar [~]; hiša 40 NOVA HIŠA v vzorcu (brez priora P77–P91; PT hiša v atlasu) — forenzika 5x: jasno 40; row 59 (Kurrent 5/6 — prej prebir 60; kontinuiteta s98 51–58 → s99 59); botra Nik. Brodarič [~] + Ana Klobučar [~]; pripis »† 3/9. 98« [~] (7/7); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Janez (Oct 12/12) — father Janez Berkovec? [~] half smallholder (Botkovec/Barkovec? — Kurrent o/a + r/t), mother Katarina Klobučar [~]; house 40 A NEW HOUSE in the sample (no prior P77–P91; a PT house in the atlas) — 5x forensics: clearly 40; row 59 (Kurrent 5/6 — first read 60; the continuity s98 51–58 → s99 59); godparents Nik. Brodarič [~] + Ana Klobučar [~]; note »† Sep 3, 98« [~] (7/7); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04105",
    year: 1897,
    scan: 99,
    page: 96,
    whatSi: "krščena Marija (18./19. 10.) — oče Peter Pendirec [~] ½ zemljak, mati Doroteja Klepec? [~] (Kurrent D/P); hišna 20 forenzika 5x: jasno 20 — 2. pin; row 62; botra Martin Mihelč? [~] + Marija Požek? [~]; pripis 20. st.: »Umrla 2.1.1980 v Gribljah (MMK Griblje 1.1980, str. 115)«; babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Marija (Oct 18/19) — father Peter Pendirec [~] half smallholder, mother Doroteja Klepec? [~] (Kurrent D/P); house no. 20 (5x forensics: clearly 20) — the 2nd pin; row 62; godparents Martin Mihelč? [~] + Marija Požek? [~]; 20th-c. note: »died Jan 2, 1980 in Griblje (MMK Griblje 1.1980, p. 115)«; midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1897,
    scan: 99,
    page: 96,
    whatSi: "krščena Ana (25./26. 10.) — oče Janez Straus? [~] ½ zemljak, mati Barbara Jakobič [~]; hiša 31 — 2. VPIS NA h31 V ENEM LETU (r51 Sapič?×Straus + r64 Straus?×Jakobič — dve družini Straus kompleksa; forenzika 5x: jasno 31; datum forenzika 8x: roj 25, krst 26 — krsta NI prazno!); row 64; botra Matija Ula? [~] + Doroteja Ule? [~] (Vla? — Kurrent U/V); pripis 20. st.: »poročena 29.1.1934«; babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Ana (Oct 25/26) — father Janez Straus? [~] half smallholder, mother Barbara Jakobič [~]; house 31 — the 2nd ENTRY ON h31 IN ONE YEAR (r51 Sapič?×Straus + r64 Straus?×Jakobič — two families of the Straus complex; 5x forensics: clearly 31; 8x date forensics: born 25, baptized 26 — the baptism is NOT empty!); row 64; godparents Matija Ula? [~] + Doroteja Ule? [~] (Vla? — Kurrent U/V); 20th-c. note: »married Jan 29, 1934«; midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1897,
    scan: 100,
    page: 97,
    whatSi: "krščen Nikolaj (24./25. 11.) — oče Matija Mihek? [~] ½ zemljak (Mihelk/Mihk), mati Katarina Šošt? [~]; hišna 65 forenzika: jasno 65 — 5. pin (P87+P89+P90+P91 priori); botra Janez Adlešič? [~] + Doroteja Pozdirec [~]; pripis 20. st.: »Umrl 14.05.1989 v Gribljah (MMU Griblje 2.1989, št. 21)« + EHS ČG; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Nikolaj (Nov 24/25) — father Matija Mihek? [~] half smallholder (Mihelk/Mihk), mother Katarina Šošt? [~]; house no. 65 (forensics: clearly 65) — the 5th pin (P87+P89+P90+P91 priors); godparents Janez Adlešič? [~] + Doroteja Pozdirec [~]; 20th-c. notes: »died May 14, 1989 in Griblje (MMU Griblje 2.1989, no. 21)« + EHS ČG; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1897,
    scan: 101,
    page: 98,
    whatSi: "krščena Marija (30./30. 12.) — oče Martin Straus [~] bajtar, mati Barbara Spudič [~] (5x: jasno Spudič — POPRAVEK P91 prebira »Doroteja? [~]«); hiša 45 = PT LUKNJA — 2. VPIS ISTA ZVEZA (P91 1896 r70 + 1897) — Straus × Spudič; ZADNJA Griblje vrstica leta 1897 (pred prelomom 1898 row 86); botra Matija Brinec [~] + Ana Brinec [~] (h16/h23/h24 familija); babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Marija (Dec 30/30) — father Martin Straus [~] cottager, mother Barbara Spudič [~] (5x: clearly Spudič — CORRECTING the P91 read »Doroteja? [~]«); house 45 = the PT GAP — the 2nd ENTRY THE SAME COUPLE (P91 1896 r70 + 1897) — Straus × Spudič; the LAST Griblje row of 1897 (before the 1898 break at row 86); godparents Matija Brinec [~] + Ana Brinec [~] (the h16/h23/h24 family); midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  // ——— P93 vzorec: polno leto 1898 (vsi Griblje vpisi, strani 98–106) ———
  // okvir: sken 101 row 86 (glava »1898.«) … sken 109 row 96; 96 vrstic;
  // stran == sken − 3 za celo leto (novela P92 potrjena — brez duplikatov);
  // prelom 1899 = sken 109 row 97→1 (1899 row 1 = Griblje 12!)
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1898,
    scan: 102,
    page: 99,
    whatSi: "krščena Marija (7./8. 3.) — oče Anton Brodarič [ime prečrtano v izvirniku, ne zamenjano] ½ zemljak [~], mati Marija Milek; hiša 40 (2. pin) — MENJAVA: 1897 Berkovec? × Klobučar → Brodarič (Berkopne selitev na h48; Anton Brodarič = h46 oče 1893–97 — rotacija [~]); botra Janez Berkopne [~ — ista oseba kot h48 oče?] + Marija Željko (ŽELJKO VERIGA); pripis: »Umrła 17.1.1975 — Griblah« + poroka 1922; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Mar 7/8) — father Anton Brodarič [first name struck out in the original, not replaced] half smallholder [~], mother Marija Milek; house 40 (the 2nd pin) — HOUSEHOLD CHANGE: 1897 Berkovec? × Klobučar → Brodarič (Berkopne moving to h48; Anton Brodarič = the h46 father 1893–97 — rotation [~]); godparents Janez Berkopne [~ — the same person as the h48 father?] + Marija Željko (THE ŽELJKO CHAIN); notes: »died Jan 17, 1975 — in Griblje« + marriage 1922; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1898,
    scan: 103,
    page: 100,
    whatSi: "krščen Alojzij (24./24. 4.) — oče Nikolaj Straus ¼ zemljak [~], mati Marija Jakobšič [~]; hiša 69 (7. pin) — MENJAVA GOSPODINJSTVA: Brinec (5 vpisov 1888–1895) → Straus (Straus signal na 4. hiši h71/h72/h45/h69); botra Matija Straus + Katarina Milek/Mibek [~]; pripisi: EMŠO 2404898500042 (1982) + »Umrł 6.1.1983 v Gribljah« (register sam potrjuje vas) + poroka 1928; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Alojzij (Apr 24/24) — father Nikolaj Straus ¼ smallholder [~], mother Marija Jakobšič [~]; house 69 (the 7th pin) — HOUSEHOLD CHANGE: Brinec (5 entries 1888–1895) → Straus (the Straus signal on a 4th house h71/h72/h45/h69); godparents Matija Straus + Katarina Milek/Mibek [~]; notes: EMŠO 2404898500042 (1982) + »died Jan 6, 1983 in Griblje« (the register itself confirms the village) + marriage 1928; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "89",
    bookSignature: "04105",
    year: 1898,
    scan: 103,
    page: 100,
    whatSi: "krščena Katarina (27./27. 6.) — oče Marko Podrinc [Pendirec cluster] ½ zemljak, mati Katarina Žugelj; hiša 89 = NOVA ŠTEVILKA (prvi vitals; izven 41–60 luknje; Kurrent 9 z dolgim repom — 5x: jasno 8+9); botra Nikolaj Željko + Katarina Križan [~ Hrižan] (ŽELJKO VERIGA 11. signal); pripisi: »Umrła 21.10.1951 v Ljubljani« + vdovana 1951; matičar Šimec; babica PRAZNA; podpis Fr. Šturm",
    whatEn: "baptized Katarina (Jun 27/27) — father Marko Podrinc [Pendirec cluster] half smallholder, mother Katarina Žugelj; house 89 = A NEW NUMBER (first vitals; outside the 41–60 gap; Kurrent 9 with a long tail — 5x: clearly 8+9); godparents Nikolaj Željko + Katarina Križan [~ Hrižan] (the ŽELJKO CHAIN, 11th signal); notes: »died Oct 21, 1951 in Ljubljana« + widowed 1951; registrar Šimec; midwife EMPTY; signature Fr. Šturm",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04105",
    year: 1898,
    scan: 104,
    page: 101,
    whatSi: "krščen Janez (21./21. 6.) — oče Matija Šimec ½ zemljak, mati Ana Kukar [~]; hiša 18 = NOVA ŠTEVILKA (prvi vitals; izven 41–60 luknje); Šimec familija 5. hiša (h39/h34/h55/h65-Mihelt/h18); botra Peter Hrižan [~ Hrigovc] + Marija Podrinc [Pendirec]; marginalija † (datum delno neberljiv — možna zgodnja smrt [~]); babica PRAZNA; podpis Fr. Šturm",
    whatEn: "baptized Janez (Jun 21/21) — father Matija Šimec half smallholder, mother Ana Kukar [~]; house 18 = A NEW NUMBER (first vitals; outside the 41–60 gap); the Šimec family's 5th house (h39/h34/h55/h65-Mihelt/h18); godparents Peter Hrižan [~ Hrigovc] + Marija Podrinc [Pendirec]; marginal † (date partly illegible — possible early death [~]); midwife EMPTY; signature Fr. Šturm",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1898,
    scan: 104,
    page: 101,
    whatSi: "krščen Peter (1./2. 7.) — oče Matija Urk [~ Urh] ½ zemljak, mati Marija Podrinc [~ Marjeta Pendirec cluster]; hiša 32 (8. pin) — Urh oče variante: Urh 1889–92 → Meh/Mrh? 1893 → Urh 1895 → Perdune? 1897 → Urk 1898 [~ isti Matija]; botra Jurij [~] Straus + Barbara Straus; pripisi: »poročen s Terezijo 25.2.1924« + »Umlal 22.4.1981 v Novem mestu«; babica PRAZNA; podpis neberljiv [~]",
    whatEn: "baptized Peter (Jul 1/2) — father Matija Urk [~ Urh] half smallholder, mother Marija Podrinc [~ Marjeta Pendirec cluster]; house 32 (the 8th pin) — the Urh father variants: Urh 1889–92 → Meh/Mrh? 1893 → Urh 1895 → Perdune? 1897 → Urk 1898 [~ the same Matija]; godparents Jurij [~] Straus + Barbara Straus; notes: »married to Terezija Feb 25, 1924« + »died Apr 22, 1981 in Novo mesto«; midwife EMPTY; signature illegible [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1898,
    scan: 106,
    page: 103,
    whatSi: "krščena Katarina (20./20. 9.) — oče Janez Hrigar [~ Hrižan/Križan] ½ zemljak, mati Katarina Straus [Straucelj]; hiša 36 (tri-virska) — 3. VPIS ISTA ZVEZA (1894 + 1896 + 1898; 7. in 8. vir hiše); botra Marija Straus + Marija Podrinc [Pendirec]; hišna 36 forenzika 5x: jasno 36 (prvi prebir »56« napačen); pripisi: poroka 1921 + † 1974?; matičar Šimec; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Katarina (Sep 20/20) — father Janez Hrigar [~ Hrižan/Križan] half smallholder, mother Katarina Straus [Straucelj]; house 36 (three-source) — the 3rd ENTRY THE SAME COUPLE (1894 + 1896 + 1898; the house's 7th and 8th sources); godparents Marija Straus + Marija Podrinc [Pendirec]; house no. 36 forensics 5x: clearly 36 (the first read »56« wrong); notes: marriage 1921 + † 1974?; registrar Šimec; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04105",
    year: 1898,
    scan: 107,
    page: 104,
    whatSi: "krščena Marija (21./22. 10.) — oče Matija Dehlič [~] ½ zemljak, mati Marija Rožek [~]; hiša 33 (2. pin) — MENJAVA: Brinec (1889 Matija Brinec × Marija Dolenc) → Dehlič × Rožek; STARI h33 oče Matija Brinec zdaj BOTRA (skupaj z Marjeta Rožek); marginalija † 4/3. 8? [~]; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Oct 21/22) — father Matija Dehlič [~] half smallholder, mother Marija Rožek [~]; house 33 (the 2nd pin) — HOUSEHOLD CHANGE: Brinec (1889 Matija Brinec × Marija Dolenc) → Dehlič × Rožek; the OLD h33 father Matija Brinec now a GODPARENT (together with Marjeta Rožek); marginal † Mar 4, 8? [~]; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1898,
    scan: 107,
    page: 104,
    whatSi: "krščena Marija (26./26. 10.) — oče Janez Berkopne [Berhope] ¼ zemljak [~], mati Katarina Klobučar; hiša 48 = NOVA LUKNJA ŠTEVILKA (18. dokazana v 41–60 — PT_GAP_KNOWN + 48); forenzika 6x: jasno 48 (ne 40 — dvojna zanka = 8); SELITEV: Berkopne × Klobučar h40 (1897) → h48 (1898) — ISTA ZVEZA, druga hiša; botra Nikolaj Brodarič [~] + Ana Jakljevič; pripis: poroka 1929; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Oct 26/26) — father Janez Berkopne [Berhope] ¼ smallholder [~], mother Katarina Klobučar; house 48 = A NEW GAP NUMBER (the 18th proven in 41–60 — PT_GAP_KNOWN + 48); forensics 6x: clearly 48 (not 40 — the double loop = 8); THE MOVE: Berkopne × Klobučar h40 (1897) → h48 (1898) — THE SAME COUPLE, another house; godparents Nikolaj Brodarič [~] + Ana Jakljevič; note: marriage 1929; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1898,
    scan: 107,
    page: 104,
    whatSi: "krščen Jožef (7./7. 11., † 6/6.1900 — dojenčijska smrt) — oče Nikolaj Hrižan [Križan/Prižan] ½ zemljak, mati Katarina Podrinc [Pendirec cluster]; hiša 63 VRNITEV po 1897 — OČE ISTI 6× (1887 + 1889 + 1890 + 1892 + 1896 + 1898; P92 »konec serije« POPRAVLJEN — najbolj konstanten oče vzorca); botra Marko Podrinc [= h89 oče r30] + Marjeta Šegina; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Jožef (Nov 7/7, † Jun 6, 1900 — an infant death) — father Nikolaj Hrižan [Križan/Prižan] half smallholder, mother Katarina Podrinc [Pendirec cluster]; house 63 RETURNS after 1897 — THE FATHER THE SAME 6× (1887 + 1889 + 1890 + 1892 + 1896 + 1898; the P92 »end of the series« CORRECTED — the most constant father in the sample); godparents Marko Podrinc [= the h89 father r30] + Marjeta Šegina; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "52",
    bookSignature: "04105",
    year: 1898,
    scan: 107,
    page: 104,
    whatSi: "krščena Barbara (9./9. 11.) — oče Matija Podrinc [Pendirec] ½ zemljak, mati Ana Jakobič; hiša 52 PRVI TRDNI PIN (1887 block [~] preživel trojno korekcijo 52→04→15; 1898 forenzika 5x: jasno 52) — NOVA DRUŽINA Podrinc × Jakobič; botra Anton Brodarič [~ Šbrodarič] + Katarina Hrižan (= h63 mati familija); marginalija † 1/3.63 (1963); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Barbara (Nov 9/9) — father Matija Podrinc [Pendirec] half smallholder, mother Ana Jakobič; house 52 THE FIRST SOLID PIN (the 1887 block [~] survived the triple correction 52→04→15; the 1898 forensics 5x: clearly 52) — A NEW FAMILY Podrinc × Jakobič; godparents Anton Brodarič [~ Šbrodarič] + Katarina Hrižan (= the h63 mother family); marginal † Mar 1, 63 (1963); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1898,
    scan: 108,
    page: 105,
    whatSi: "krščen Anton (9./10. 12.) — oče Janez Podrinc [Pendirec/Pozdirec] ½ zemljak, mati Marija Hrižan; hiša 53 (PT LUKNJA) — 4. VPIS ISTA ZVEZA (1891 + 1894 + 1896 + 1898; Kurrent P/K + K/H variante); botra Matija Šimec [= h18 oče r37 — ista oseba oče + botra] + Ana Kure (h1 mati familija — Kure signal); babica PRAZNA; podpis Fr. Šturm",
    whatEn: "baptized Anton (Dec 9/10) — father Janez Podrinc [Pendirec/Pozdirec] half smallholder, mother Marija Hrižan; house 53 (the PT GAP) — the 4th ENTRY THE SAME COUPLE (1891 + 1894 + 1896 + 1898; the Kurrent P/K + K/H variants); godparents Matija Šimec [= the h18 father r37 — the same person father + godparent] + Ana Kure (the h1 mother family — a Kure signal); midwife EMPTY; signature Fr. Šturm",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1898,
    scan: 109,
    page: 106,
    whatSi: "krščen Alojzij (24./29. 12.) — oče Alojzij Vetročnik [~] UČITELJ, mati Leopolda Schmelzer; hiša 90 ŠOLSKA HIŠA (3. pin) — NOVI UČITELJ: Kopitar (1890 + 1892) → Vetročnik (1898); mati nemški priimek Schmelzer; botra Ivan Vrhovec [~ Arhovec] UČITELJ + Apolonija Majnik [~] gazdinica? [~] — tretja učiteljska generacija na šolski hiši (1890 botra Janez Barle, 1892 nadučitelj botra); ZADNJA Griblje vrstica leta 1898 (pred prelomom 1899 row 97); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Alojzij (Dec 24/29) — father Alojzij Vetročnik [~] TEACHER, mother Leopolda Schmelzer; house 90 THE SCHOOL HOUSE (the 3rd pin) — A NEW TEACHER: Kopitar (1890 + 1892) → Vetročnik (1898); the mother's German surname Schmelzer; godparents Ivan Vrhovec [~ Arhovec] TEACHER + Apolonija Majnik [~] gazdinica? [~] — the third teacher generation at the school house (1890 godparent Janez Barle, 1892 the head teacher); the LAST Griblje row of 1898 (before the 1899 break at row 97); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },

  // ——— P94 vzorec: polno leto 1899 (vsi Griblje vpisi, strani 106–115) ———
  // okvir: skeni 109 row 97 – 118 row 104 == strani 106–115; 104 vrstic; stran == sken − 3;
  // prelom 1900 na SREDINI str. 115 (sken 118 row 105 — prvič ne na novi strani); NARE 6. leto:
  // 15 vpisov / 15 hiš (brez ponovitev); 2 NOVI hiši (22 PT nabor + 49 NOVA LUKNJA — 19.);
  // h60 trdno zasidran (4. vpis iste zveze + 3. ista botra para)
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1899,
    scan: 109,
    page: 106,
    whatSi: "krščena Marija (5./5. 1.) — oče Janez Dragar [Dragoš? — Kurrent r/s] ½ zemljak, mati Barbara Cvitkovič [~]; PRELOMNA VRSTICA — 1899 row 1, novo leto se začne z Griblji (P93 napoved); † 25/6.99 [~] — dojenčnica; mati MENJAVA [~]: 1897 (P92) »Marija Straus [~]« → 1899 Barbara Cvitkovič [~] (botra 1899 = Marija Straus — možna zamenjava celic v P92 ali prava menjava); botra Marija Straus [~] + Katarina Jakobič [~]; babica PRAZNA; podpis Fr. Šturm [~]",
    whatEn: "baptized Marija (Jan 5/5) — father Janez Dragar [Dragoš? — Kurrent r/s] half smallholder, mother Barbara Cvitkovič [~]; THE BREAK ROW — 1899 row 1, the new year begins with Griblje (as P93 predicted); † Jun 25, 99 [~] — an infant; MOTHER CHANGE [~]: 1897 (P92) 'Marija Straus [~]' → 1899 Barbara Cvitkovič [~] (the 1899 godparent = Marija Straus — a possible cell swap in the P92 reading or a real change); godparents Marija Straus [~] + Katarina Jakobič [~]; midwife EMPTY; signature Fr. Šturm [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1899,
    scan: 110,
    page: 107,
    whatSi: "krščena Marija (26./26. 1.) — oče Anton Brodarič ½ zemljak, mati Ana Škaradinič? [~ — 4. varianta matere h46]; h46 5. VPIS ISTA ZVEZA očeta (1893+1895+1896+1897+1899); matere: Klobučar/Klobučan? → Kramarič? → Harašimovič? → Škaradinič? (enaki konci -arič; verjetno ista oseba); botra Nikolaj Željko [~] + Neža Štruncelj? [~] — ISTA BOTRA PARA kot 1896+1897 (3. leto); priimek Škaradinič potrjen pri r2 (Krasinec 32); pripis: † 24.3.1964 v Gribljih; babica PRAZNA; podpis Fr. Šturm",
    whatEn: "baptized Marija (Jan 26/26) — father Anton Brodarič half smallholder, mother Ana Škaradinič? [~ — the 4th variant of the h46 mother]; h46 the 5th ENTRY of the same father's couple (1893+1895+1896+1897+1899); mothers: Klobučar/Klobučan? → Kramarič? → Harašimovič? → Škaradinič? (the same -arič endings; probably the same woman); godparents Nikolaj Željko [~] + Neža Štruncelj? [~] — THE SAME GODPARENT PAIR as 1896+1897 (the 3rd year); the surname Škaradinič confirmed at r2 (Krasinec 32); note: † Mar 24, 1964 in Griblje; midwife EMPTY; signature Fr. Šturm",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1899,
    scan: 110,
    page: 107,
    whatSi: "krščen Jožef [~ — ime delno pod pripisom] (31./31. 1.) — oče Janez Knekar? [~ — 1893 branje »Stukar/Stubhar«; 2. branje priimka] ½ zemljak, mati Katarina Klobučar; h27 6. VPIS; ISTA ZVEZA kot 1893 dvojčki (Janez × Katarina Klobučar); botra Janez Pojak? [Požak?] + Ana Pojak? [~]; pripisi: † 16.1.1902 (~3 leta), por. 1910, 2. poroka 19.2.1939(?); botra h21 (r37 Apr) = Janez Knekar — KRIŽNI SKLIC z očetom h27; babica PRAZNA; podpis Fr. Klun [~] (vrnitev iz 1897)",
    whatEn: "baptized Jožef [~ — the name partly under a note] (Jan 31/31) — father Janez Knekar? [~ — the 1893 reading was 'Stukar/Stubhar'; the 2nd reading of the h27 father's surname] half smallholder, mother Katarina Klobučar; h27 the 6th entry; THE SAME COUPLE as the 1893 twins (Janez × Katarina Klobučar); godparents Janez Pojak? [Požak?] + Ana Pojak? [~]; notes: † Jan 16, 1902 (~3 years old), married 1910, a 2nd marriage Feb 19, 1939(?); the h21 godparent (r37 Apr) = Janez Knekar — A CROSS-LINK with the h27 father; midwife EMPTY; signature Fr. Klun [~] (back from 1897)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1899,
    scan: 110,
    page: 107,
    whatSi: "krščen Matija (13./13. 2.) — oče Nikolaj Željko ½ zemljak, mati Marija Brodarič (forenzika 10x: jasno »Broda…«); hiša 60 TRDNI PIN — hišna pod modrim pripisom, kanalna forenzika (temen »…o 6o«) + STRUKTURNA POTRDITEV (oče = h60 oče 1893/94/97 + botra para Pendirec × Klepac = h60 1893/94); h60 4. VPIS ISTA ZVEZA Željko × Brodarič (1893+1894+1897+1899) + 3. ISTA BOTRA PARA (1893+1894+1899); ŽELJKO VERIGA 13. signal; matičar: † 9.1.1965 v Gribljah, por. 1919(?); babica PRAZNA; podpis Fr. Šturm [~]",
    whatEn: "baptized Matija (Feb 13/13) — father Nikolaj Željko half smallholder, mother Marija Brodarič (forensics 10x: clearly 'Broda…'); house 60 THE SOLID PIN — the house number under a blue note, channel forensics (dark '…o 6o') + STRUCTURAL CONFIRMATION (the father = the h60 father 1893/94/97 + the godparent pair Pendirec × Klepac = h60 1893/94); h60 the 4th ENTRY of the same couple Željko × Brodarič (1893+1894+1897+1899) + the 3rd SAME GODPARENT PAIR (1893+1894+1899); the ŽELJKO CHAIN's 13th signal; the registrar: † Jan 9, 1965 in Griblje, married 1919(?); midwife EMPTY; signature Fr. Šturm [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "59",
    bookSignature: "04105",
    year: 1899,
    scan: 110,
    page: 107,
    whatSi: "krščen Jožef (15./15. 2.) — oče Janez Simič? [~] ½ zemljak, mati Marija Kure; hiša 59 forenzika 5x: jasno 59 (5 raven vrh + Kurrent 9 z repom, ne 39); h59 2. VPIS (1889 Marinka — NEZAKONSKA, mati Katarina Podirec [~]; 1899 PRVI imenovani oče na h59 — NOVA ZVEZA Simič × Kure, Kure familija); botra Janez Jožek? [~] + Ana Brinec? [~] (Brinec cluster); matičar: † 1969(?); babica PRAZNA; podpis Fr. Šturm [~]",
    whatEn: "baptized Jožef (Feb 15/15) — father Janez Simič? [~] half smallholder, mother Marija Kure; house 59 forensics 5x: clearly 59 (a flat-topped 5 + a Kurrent 9 with the long tail, not 39); h59 the 2nd entry (1889 Marinka — ILLEGITIMATE, mother Katarina Podirec [~]; 1899 THE FIRST named father at h59 — A NEW COUPLE Simič × Kure, the Kure family); godparents Janez Jožek? [~] + Ana Brinec? [~] (the Brinec cluster); the registrar: † 1969(?); midwife EMPTY; signature Fr. Šturm [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1899,
    scan: 111,
    page: 108,
    whatSi: "krščena Marija (20./20. 3.) — oče Nikolaj Milek [Milih?] [~] ½ zemljak, mati Marija Klepec; hiša 22 = NOVA ŠTEVILKA VZORCA (prvi matrični dokaz; hiša v PT naboru 1825 — ATLAS_HOUSES že vsebuje 22); forenzika 7x: jasno 22; NOVA ZVEZA Milek × Klepec (Milek cluster: h65/h29/h30/h70 — brez tega para; mati [~ ista oseba kot botra h60 Marija Klepac — botra 13.3. + mati 20.3. v 1 tednu]); botra Marko Pendirec? [~] (½) + Katarina Hrižan (¼); † 2/[5-6].99 [~] — dojenčnica; babica PRAZNA; podpis Fr. Šturm",
    whatEn: "baptized Marija (Mar 20/20) — father Nikolaj Milek [Milih?] [~] half smallholder, mother Marija Klepec; house 22 = A NEW SAMPLE NUMBER (the first documentary proof; the house is in the 1825 PT set — ATLAS_HOUSES already contains 22); forensics 7x: clearly 22; A NEW COUPLE Milek × Klepec (the Milek cluster: h65/h29/h30/h70 — without this pair; the mother [~ the same person as the h60 godparent Marija Klepac — godparent Mar 13 + mother Mar 20 within a week]); godparents Marko Pendirec? [~] (½) + Katarina Hrižan (¼); † May/Jun 2, 99 [~] — an infant; midwife EMPTY; signature Fr. Šturm",
    status: "DOCUMENTED",
  },
  {
    houseNo: "41",
    bookSignature: "04105",
    year: 1899,
    scan: 112,
    page: 109,
    whatSi: "krščena Neža (9./9. 4.) — oče Matija Kušič [Hrušič 1890 / Hušič 1893+1896] ½ zemljak, mati Neža Jakobič [Jakobčič?]; hiša 41 (PT LUKNJA) forenzika 7x: jasno 41; h41 4. VPIS ISTA ZVEZA (1890+1893+1896+1899; 3. pisavska varianta priimka očeta); botra Milka Pozdirec? + Katarina Jakobič [~ — ~ista para kot 1896]; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Neža (Apr 9/9) — father Matija Kušič [Hrušič 1890 / Hušič 1893+1896] half smallholder, mother Neža Jakobič [Jakobčič?]; house 41 (the PT GAP) forensics 7x: clearly 41; h41 the 4th ENTRY of the same couple (1890+1893+1896+1899; the 3rd written variant of the father's surname); godparents Milka Pozdirec? + Katarina Jakobič [~ — about the same pair as 1896]; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1899,
    scan: 112,
    page: 109,
    whatSi: "krščena Marjeta (17./17. 4.) — oče Janez Požek ½ zemljak, mati Ana Šimec; hiša 21 forenzika 7x: jasno 21 (ne 27); h21 4. vpis (1887 + 1888 nezakonski + 1893 + 1899) — 2. VPIS ISTA ZVEZA Požek × Šimec (1893+1899); botra Janez Knekar? [~ = oče h27 r11 — križni sklic] + Marija Šimec (mati familija); pripis: † 4.3.1926; babica PRAZNA; podpis Fr. Klun [~]",
    whatEn: "baptized Marjeta (Apr 17/17) — father Janez Požek half smallholder, mother Ana Šimec; house 21 forensics 7x: clearly 21 (not 27); h21 the 4th entry (1887 + 1888 illegitimate + 1893 + 1899) — the 2nd ENTRY of the same couple Požek × Šimec (1893+1899); godparents Janez Knekar? [~ = the h27 father r11 — a cross-link] + Marija Šimec (the mother's family); note: † Mar 4, 1926; midwife EMPTY; signature Fr. Klun [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1899,
    scan: 113,
    page: 110,
    whatSi: "krščen Janez (13./13. 5.) — oče Martin Straus bajtar, mati Barbara Spudič; hiša 40 forenzika: jasno 40 (0 = zaprt oval); h40 TRETJA DRUŽINA V TRIH LETIH (Berkopne 1897 → Brodarič 1898 [~] → Straus 1899) — najgostejša rotacija vzorca; STRAUS × SPUDIČ = POTRDITEV poročnega lead-a 04455 (nextSteps P93); Straus cluster: h69 Nikolaj, h40 Martin, Jurij 1898 [~]; botra Janez Pegdirec? [~] + Marija Urh [~] (Urk cluster); babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Janez (May 13/13) — father Martin Straus a cotter, mother Barbara Spudič; house 40 forensics: clearly 40 (a closed-oval 0); h40 THE THIRD FAMILY IN THREE YEARS (Berkopne 1897 → Brodarič 1898 [~] → Straus 1899) — the sample's densest rotation; STRAUS × SPUDIČ = the CONFIRMATION of the marriage lead 04455 (P93 nextSteps); the Straus cluster: h69 Nikolaj, h40 Martin, Jurij 1898 [~]; godparents Janez Pegdirec? [~] + Marija Urh [~] (the Urk cluster); midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1899,
    scan: 114,
    page: 111,
    whatSi: "krščena Ana (30./30. 8.) — oče Nikolaj Segina [Šegina?] ½ zemljak, mati Marjeta Milek [~ — ista mati kot h70 1893 + h30 1895 (»Mihelt«)]; kraj zapisan »Griblja« (varianta) — smrtna opomba POTRJUJE Griblje († 31.3.1975 v Gribljah); h1 MENJAVA GOSPODINJSTVA: Željko (1888+1892+1896) → Segina (1899); SEGINA VERIGA: h70 (1893) → h30 (1895) → h1 (1899) — 3 hiše / 6 let; botra Nikolaj Hrižan [~] + Katarina Milek [~]; pripis: por. 6/6 1921; babica PRAZNA; podpis Jos. Rauq [~ — poškodovan]",
    whatEn: "baptized Ana (Aug 30/30) — father Nikolaj Segina [Šegina?] half smallholder, mother Marjeta Milek [~ — the same mother as h70 1893 + h30 1895 ('Mihelt')]; the village written 'Griblja' (a variant) — the death note CONFIRMS Griblje († Mar 31, 1975 in Griblje); h1 A HOUSEHOLD CHANGE: Željko (1888+1892+1896) → Segina (1899); the SEGINA CHAIN: h70 (1893) → h30 (1895) → h1 (1899) — 3 houses / 6 years; godparents Nikolaj Hrižan [~] + Katarina Milek [~]; note: married Jun 6, 1921; midwife EMPTY; signature Jos. Rauq [~ — damaged]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1899,
    scan: 114,
    page: 111,
    whatSi: "krščena Marija (30./31. 9.) — oče Janez Županič [Župarič/Šuparic?] [~] ½ zemljak, mati Marija Finek? [~]; hiša 30 forenzika: jasno 30; h30 4. DRUŽINA V 9 LETIH (3. MENJAVA): Milek (1890–91) → Jakljevič (1893) → Šegina (1895) → Županič (1899); ŽUPANIČ CLUSTER 3 signali (h73 Nikolaj 1894 + h30 Janez 1899 + botra Ana Županič 1899 — verjetno sestra očeta); botra Matija? Novak [~] + Ana Županič [~] (bajtarja?); matičar: † 4.3.1984 Črni Potok; babica PRAZNA; podpis Fr. Šturm [~]",
    whatEn: "baptized Marija (Sep 30/31) — father Janez Županič [Župarič/Šuparic?] [~] half smallholder, mother Marija Finek? [~]; house 30 forensics: clearly 30; h30 THE 4TH FAMILY IN 9 YEARS (the 3rd change): Milek (1890–91) → Jakljevič (1893) → Šegina (1895) → Županič (1899); the ŽUPANIČ CLUSTER's 3 signals (h73 Nikolaj 1894 + h30 Janez 1899 + the godparent Ana Županič 1899 — probably the father's sister); godparents Matija? Novak [~] + Ana Županič [~] (bajtarja?); the registrar: † Mar 4, 1984 Črni Potok; midwife EMPTY; signature Fr. Šturm [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "75",
    bookSignature: "04105",
    year: 1899,
    scan: 115,
    page: 112,
    whatSi: "krščen Nikolaj (23.?/3.? 10. [~ — rojstva »23« + popravek »2« zgoraj; verjetno 2.10. + krst 3.10.]) — oče Janez Jakobič [Jakobčič?] [~] ½ zemljak, mati Marija Stubljar [Sušljar?/Stubler/Štubfar? — 4. pisavska varianta] [~]; hiša 75 forenzika 10x: jasno 75 (7 s poševnim prečkanjem, ne 25/45); h75 3. VPIS ISTA ZVEZA (1892+1894+1899); botra Marko Jakobič [~ — sorodnik očeta?] + Katarina Štrinec? [~]; babica PRAZNA; podpis raztrgan",
    whatEn: "baptized Nikolaj (Oct 23?/3? [~ — born '23' + the correction '2' above; probably Oct 2 + baptized Oct 3]) — father Janez Jakobič [Jakobčič?] [~] half smallholder, mother Marija Stubljar [Sušljar?/Stubler/Štubfar? — the 4th written variant] [~]; house 75 forensics 10x: clearly 75 (a 7 with the diagonal cross-stroke, not 25/45); h75 the 3rd ENTRY of the same couple (1892+1894+1899); godparents Marko Jakobič [~ — the father's relative?] + Katarina Štrinec? [~]; midwife EMPTY; signature torn away",
    status: "DOCUMENTED",
  },
  {
    houseNo: "57",
    bookSignature: "04105",
    year: 1899,
    scan: 116,
    page: 113,
    whatSi: "krščen Alojzij (datum UNIČEN — raztrgan spodnji rob str. 113; ~november po sosedi r90 = 10.11.) — oče Miha Pozdirec [Pezdirec?] [~] ½ zemljak, mati Marija Županič [~ — ista mati kot 1888–94]; hiša 57 (PT LUKNJA) forenzika 8x: jasno 57; h57 4. vpis (1888+1889+1894+1899) — OČE MENJAVA: Peter Pezdirec (1888–94) → Miha Pozdirec (brata? sin?) [~]; Miha = botra h41 1896 → oče h57 1899; botra Nikolaj Željko [~ — 14. ŽELJKO signal] + Marija Šturovc? [~]; babica [~ poškodovano]; podpis Jos. Rauq [~ — poškodovan]",
    whatEn: "baptized Alojzij (the date DESTROYED — the torn bottom edge of p. 113; ~November per the neighbour r90 = Nov 10) — father Miha Pozdirec [Pezdirec?] [~] half smallholder, mother Marija Županič [~ — the same mother as 1888–94]; house 57 (the PT GAP) forensics 8x: clearly 57; h57 the 4th entry (1888+1889+1894+1899) — THE FATHER CHANGE: Peter Pezdirec (1888–94) → Miha Pozdirec (a brother? a son?) [~]; Miha = the h41 1896 godparent → the h57 1899 father; godparents Nikolaj Željko [~ — the 14th ŽELJKO signal] + Marija Šturovc? [~]; midwife [~ damaged]; signature Jos. Rauq [~ — damaged]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "49",
    bookSignature: "04105",
    year: 1899,
    scan: 117,
    page: 114,
    whatSi: "krščena Marija (15./15. 11.) — oče Nikolaj Brodarič ½ zemljak, mati Marjeta Milek; hiša 49 = NOVA LUKNJA ŠTEVILKA (19. dokazana v 41–60 — PT_GAP_KNOWN + 49; luknja zdaj 42/50/51); forenzika 8x: jasno 49 (4 + 9 z repom); NOVA ZVEZA Brodarič × Milek (Nikolaj Brodarič = botra h48 1898 → oče h49 1899); botra Nikolaj Žegina? [Segina?] [~] + Katarina Berkopeč [Berkopne?] [~] (¼); † 24/6.00 — dojenčnica (~7 mesecev); babica PRAZNA; podpis Jos. [neberljiv — Kergo?] [~]",
    whatEn: "baptized Marija (Nov 15/15) — father Nikolaj Brodarič half smallholder, mother Marjeta Milek; house 49 = A NEW GAP NUMBER (the 19th proven in 41–60 — PT_GAP_KNOWN + 49; the gap now 42/50/51); forensics 8x: clearly 49 (a 4 + a 9 with the tail); A NEW COUPLE Brodarič × Milek (Nikolaj Brodarič = the h48 1898 godparent → the h49 1899 father); godparents Nikolaj Žegina? [Segina?] [~] + Katarina Berkopeč [Berkopne?] [~] (¼); † Jun 24, 1900 — an infant (~7 months); midwife EMPTY; signature Jos. [unreadable — Kergo?] [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1899,
    scan: 117,
    page: 114,
    whatSi: "krščena Marija (8./8. 12.) — oče Nikolaj Šilak? [Silak/Šimak?] [~] ½ zemljak, mati Katarina Klobučar; hiša 34 forenzika 9x: jasno 34; h34 2. DRUŽINA (Šimec 1887 → Šilak 1899 — MENJAVA po 12 letih); botra Nikolaj Segina [= oče h1 r61 — 2. pojav v 1 mesecu; SEGINA 3 signali v letu] + Katarina Šilak [~ — žena/mat očeta?]; ZADNJA Griblje vrstica leta 1899; babica PRAZNA; podpis Jos. [neberljiv — Kergo?] [~]",
    whatEn: "baptized Marija (Dec 8/8) — father Nikolaj Šilak? [Silak/Šimak?] [~] half smallholder, mother Katarina Klobučar; house 34 forensics 9x: clearly 34; h34 THE 2ND FAMILY (Šimec 1887 → Šilak 1899 — a change after 12 years); godparents Nikolaj Segina [= the h1 father r61 — a 2nd appearance within a month; SEGINA's 3 signals in the year] + Katarina Šilak [~ — the father's wife/mother?]; the LAST Griblje row of 1899; midwife EMPTY; signature Jos. [unreadable — Kergo?] [~]",
    status: "DOCUMENTED",
  },

  // ——— P95 vzorec: polno leto 1900 (vsi Griblje vpisi, strani 115–121) ———
  // okvir: skeni 118 row 105 (SREDINA str. 115 — prelom sredi strani, P94 dokazano) –
  // 124 row 77 == strani 115–121; 77 vrstic; stran == sken − 3; sken 121 = 2 podatkovna
  // panela (r33–44 + r45–56), sken 122 = 2 starševska panela; r51–56 FIZIČNO RAZTRGANE;
  // NARE 7. leto: 16 vpisov / 16 hiš (2. leto brez ponovitev); NOVA HIŠA 67 (prvi
  // matrični dokaz — Straus gumbar); NOVELA: stolpec babice PRVIČ izpolnjen (Fottre 7×);
  // Šturm 0× (PRVIČ) — Rauq 9× + Perg 4× + Klunček 2×; h67 → vitals 254
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1900,
    scan: 118,
    page: 115,
    whatSi: "krščena Anea [Aneža? — Kurrent; 3. črka e/ž [~]] (16./17. 1.) — oče Jurij Željko [~] ½ zemljak, mati Barbara Kure [~]; h1 = 5. VPIS; ŽELJKO VRNITEV: 1888–96 Nikolaj Željko × Katarina Kure → 1899 Segina → 1900 Jurij Željko × Barbara Kure — nov par ISTE RUŠIČNE mreže (Jurij Željko = BOTER h1 1888!; Kure = mati rodbina 1888–96) — ŽELJKO signal 15; marginalija pod imenom: † 6/…1907 [~ — mesec neberljiv] — otrok † ~7 let; botra Jakob Tolher? [~] (½ zemljak) + Ana Muc (kovačeva žena) [~]; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Anea [Aneža? — Kurrent; the 3rd letter e/ž [~]] (Jan 16/17) — father Jurij Željko [~] half smallholder, mother Barbara Kure [~]; h1 = the 5th ENTRY; THE ŽELJKO RETURN: 1888–96 Nikolaj Željko × Katarina Kure → 1899 Segina → 1900 Jurij Željko × Barbara Kure — a new couple of the SAME household web (Jurij Željko = the h1 1888 GODPARENT!; Kure = the mother's family 1888–96) — the ŽELJKO signal 15; marginal note under the name: † Jun 6, 1907 [~ — month illegible] — the child † ~7 years old; godparents Jakob Tolher? [~] (half smallholder) + Ana Muc (the smith's wife) [~]; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "67",
    bookSignature: "04105",
    year: 1900,
    scan: 118,
    page: 115,
    whatSi: "krščena Jožla (10./10. 2.) — oče Nikolaj Straus [~] (gumbar [~ — status: »2 gumbar« ali »½ gumbar« — Kurrent 2/½ dvom]), mati Marija Jakopič [~]; h67 = NOVA HIŠA VZORCA (prvi matrični dokaz; hiša v PT naboru 1825 — ATLAS_HOUSES vsebuje 67 v bloku 61–99) — 80. hiša vzorca; STRAUS priimek na novi hiši (mreža: h45 Martin Straus, h31 mati Straus, botri Straus na h58/h32/h28); EMŠO matičarja 1002900505074 (roj. 10.02.1900 — ujema se z vrstico!); matičar: † 2.1.1984 Novo mesto, por. 16/5.19?? [leto neberljivo]; botra Antonija Mihel? [~] + Marija Hrast? [~]; babica PRAZNA; podpis v raztrganem robu — neberljiv",
    whatEn: "baptized Jožla (Feb 10/10) — father Nikolaj Straus [~] (a cooper [~ — status: '2 gumbar' or '½ gumbar' — the Kurrent 2/½ doubt]), mother Marija Jakopič [~]; h67 = A NEW SAMPLE HOUSE (the first documentary proof; the house is in the 1825 PT set — ATLAS_HOUSES contains 67 in the 61–99 block) — the 80th house of the sample; the STRAUS surname at the new house (the web: h45 Martin Straus, h31 mother Straus, Straus godparents at h58/h32/h28); the registrar's EMŠO 1002900505074 (born Feb 10, 1900 — matches the row!); the registrar: † Jan 2, 1984 Novo mesto, married May 16, 19?? [year illegible]; godparents Antonija Mihel? [~] + Marija Hrast? [~]; midwife EMPTY; signature in the torn edge — illegible",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04105",
    year: 1900,
    scan: 119,
    page: 116,
    whatSi: "krščena Marija (28./28. 2.) — oče Marko Grabrijan [~ — scoping »Gmajrjan?« POPRAVLJENO] ½ zemljak, mati Marija Pozdirec [~]; h10 = 2. VPIS (1897 Janez Brinec × Marija Perdune → 1900 Grabrijan × Pozdirec — MENJAVA GOSPODINJSTVA); botra Nikolaj Hrižan? [~ — Kurrent Hrdlž/Hrižan; verjetno isti oče kot h63 6×] + Marjeta Grabrijan [~] (½ zemlj.); matičar: † 27.8.1977 v Gribljah; druga matičar opomba: žena [Mouc? Houža?] † 26.4.1984 Novo mesto (smrt moža [~]); por. 24/7.1921; opomba »Matičor/Matičar?« [~] pod imenom; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Feb 28/28) — father Marko Grabrijan [~ — the scoping 'Gmajrjan?' CORRECTED] half smallholder, mother Marija Pozdirec [~]; h10 = the 2nd ENTRY (1897 Janez Brinec × Marija Perdune → 1900 Grabrijan × Pozdirec — A HOUSEHOLD CHANGE); godparents Nikolaj Hrižan? [~ — Kurrent Hrdlž/Hrižan; probably the same father as h63 6×] + Marjeta Grabrijan [~] (half smallholder); the registrar: † Aug 27, 1977 in Griblje; a 2nd registrar note: the wife [Mouc? Houža?] † Apr 26, 1984 Novo mesto (the husband's death [~]); married Jul 24, 1921; a note 'Matičor/Matičar?' [~] under the name; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1900,
    scan: 119,
    page: 116,
    whatSi: "krščen Alojzij (rojstvo+krsta FIZIČNO RAZTRGANA — levi rob str. 116, odtrgan trak; ~april po kontekstu) — oče Matija Meh [~ — 1893 tudi »Meh/Mrh?«; 1889–98 Urh/Urk [~] — KURRENT U/M dvom: isti oče ali dva?; forenzika 1900: jasno Meh] (zemljak), mati Marija [IME PREČRTANO — »Šimec?« prečrtano, popravek neberljiv [~]; 1889–98 mati Marjeta Pendirec [~]]; h32 = 8. PIN; oče Matija 7. VPIS ISTI OČETOVSKO IME (1889–1900); 1893 (P88) »Meh/Mrh?« POTRJENO z 1900 »Meh« — KURRENT U/M varianta istega priimka [~] ALI prava menjava — MERI, ne odloča; mati: prečrtano ime = redna korekcija matičarja; ali nova žena (1898 Marjeta Pendirec → 1900 Marija?) [~]; botra Jurij Straus [~] + Barbara Hrast? [~] (½ zemljak); babica PRAZNA; podpis Jo. Perg? [~]",
    whatEn: "baptized Alojzij (born+baptized days PHYSICALLY TORN — the left edge of p. 116, a torn-off strip; ~April by context) — father Matija Meh [~ — 1893 also 'Meh/Mrh?'; 1889–98 Urh/Urk [~] — the KURRENT U/M doubt: one father or two?; the 1900 forensics: clearly Meh] (a smallholder), mother Marija [NAME CROSSED OUT — 'Šimec?' crossed out, the correction illegible [~]; 1889–98 the mother Marjeta Pendirec [~]]; h32 = the 8th PIN; the father Matija the 7th ENTRY of the same father's name (1889–1900); the 1893 (P88) 'Meh/Mrh?' CONFIRMED by the 1900 'Meh' — a KURRENT U/M variant of the same surname [~] OR a real change — MERI, undecided; the mother: the crossed-out name = a regular registrar correction; or a new wife (1898 Marjeta Pendirec → 1900 Marija?) [~]; godparents Jurij Straus [~] + Barbara Hrast? [~] (half smallholder); midwife EMPTY; signature Jo. Perg? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1900,
    scan: 120,
    page: 117,
    whatSi: "krščena Marija (3./4. 5.) — oče Matija Milek [~ — Kurrent variante Milek/Mihelt/Mihek 1887–97] ½ zemljak, mati Katarina Tožek? [~ — 5. varianta: Požek 1887/1895, Trojžif 1889, Jožek 1893, Šošt 1897, Tožek 1900 — isti priimek v Kurrentu [~]]; h65 = 6. VPIS ISTI OČE (Matija [Milek] 1887+1889+1893+1895+1897+1900); pripis: † 2/6.00 — DOJENČNICA † ~1 mesec; botra Peter Pezdirec [~] + Barbara Adlešič [~] (½ zemljak/žena); babica PRAZNA; podpis Jo. Perg? [~]",
    whatEn: "baptized Marija (May 3/4) — father Matija Milek [~ — the Kurrent variants Milek/Mihelt/Mihek 1887–97] half smallholder, mother Katarina Tožek? [~ — the 5th variant: Požek 1887/1895, Trojžif 1889, Jožek 1893, Šošt 1897, Tožek 1900 — the same surname in the Kurrent [~]]; h65 = the 6th ENTRY of the same FATHER (Matija [Milek] 1887+1889+1893+1895+1897+1900); note: † Jun 2, 1900 — AN INFANT † ~1 month; godparents Peter Pezdirec [~] + Barbara Adlešič [~] (half smallholder/wife); midwife EMPTY; signature Jo. Perg? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04105",
    year: 1900,
    scan: 120,
    page: 117,
    whatSi: "krščena Terin [Jerin?/Therin? — Kurrent T/J dvom; žensko po matičarjem »Umrla«] (17./17. 5.) — oče Peter Pendirec [~ — 1895 »Pezdirec?«; 1897 »Pendirec«] ½ zemljak, mati Doroteja Klepec [~ — 1895 »Šlepec«; 1897 »Klepec?«]; h20 = 3. PIN (2. VPIS ISTA ZVEZA Pendirec × Klepec 1897+1900; 1895 Šlepec [~] = Klepec Kurrent?); EMŠO matičarja 170590… (roj. 17.05.1900 — ujema se z vrstico!); matičar: † 2.11.1985 v Gribljah, por. 20.2.1933; botra Martin Milek [~] (½ zemljaka?) + Ana Požek (hči? [~]); babica Margareta Fottre [~]; podpis Jo. Perg R. Klunček? [~]",
    whatEn: "baptized Terin [Jerin?/Therin? — the Kurrent T/J doubt; female per the registrar's 'Umrla'] (May 17/17) — father Peter Pendirec [~ — 1895 'Pezdirec?'; 1897 'Pendirec'] half smallholder, mother Doroteja Klepec [~ — 1895 'Šlepec'; 1897 'Klepec?']; h20 = the 3rd PIN (the 2nd ENTRY of the same couple Pendirec × Klepec 1897+1900; 1895 Šlepec [~] = Klepec in the Kurrent?); the registrar's EMŠO 170590… (born May 17, 1900 — matches the row!); the registrar: † Nov 2, 1985 in Griblje, married Feb 20, 1933; godparents Martin Milek [~] (half smallholder?) + Ana Požek (a daughter? [~]); midwife Margareta Fottre [~]; signature Jo. Perg R. Klunček? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1900,
    scan: 120,
    page: 117,
    whatSi: "krščena Marija (25./26. 5.) — oče Janez Brinec [~] ½ zemljak, mati Marija Pegdinec? [~ — Pozdinec/Šegdinec? Kurrent]; h14 = 2. VPIS; 1896 (P91) oče »Janez Brinec [~]« z MERI dvomom (»ali drug Janez Brinec?« — isti priimek+ime kot h69 oče 1888–95); 1900 forenzika: Janez Brinec → REŠUJE P91 vprašanje očeta [~]; botra Marko Hrižan [~] + Marija Hrižan [~] (½ zemljak); matičar: † 6.7.1991 Žužemberk (scoping jebral 5.7.1991, forenzika: 06.07.1991); babica Margareta Foča? [~ — Fottre?]; podpis Jo. Perg? [~]",
    whatEn: "baptized Marija (May 25/26) — father Janez Brinec [~] half smallholder, mother Marija Pegdinec? [~ — Pozdinec/Šegdinec? Kurrent]; h14 = the 2nd ENTRY; 1896 (P91) the father 'Janez Brinec [~]' with a MERI doubt ('another Janez Brinec?' — the same surname+name as the h69 father 1888–95); the 1900 forensics: Janez Brinec → RESOLVES the P91 father question [~]; godparents Marko Hrižan [~] + Marija Hrižan [~] (half smallholder); the registrar: † Jul 6, 1991 Žužemberk (the scoping read Jul 5, 1991, the forensics: Jul 6, 1991); midwife Margareta Foča? [~ — Fottre?]; signature Jo. Perg? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1900,
    scan: 120,
    page: 117,
    whatSi: "krščena Leopoldina (»40 jun« [neberljivo — morda 4./10. junij; EMŠO pravi 24. maj]) — oče Alojzij Vetročnik [~] UČITELJ, mati Leopolda Schmelzer [~]; KONFLIKT DATUMA: vrstica »40 jun« [~] vs matičarjev EMŠO 2405900505109 = roj. 24.05.1900 — MERI: EMŠO avtoritativno za rojstni datum (matičar je bral civilni register); vrstica ostaja neberljiva; h90 = ŠOLSKA HIŠA, 4. PIN: ISTA UČITELJSKA DRUŽINA kot 1898 (Vetročnik × Schmelzer — 1898 r27 Alojzij) — hči Leopoldina po materi Leopoldi!; učitelji na h90: Kopitar (1890–92) → Vetročnik (1898–1900); botra g. Richard Megušar? [~] (nadučitelj? [~]) + g. Hermine Megušar? [~] (soproga); matičar opomba v celici: »Umrla dne 14.3.1954 …« [~ — pripisnost r30/r31 dvomna — glej h23]; babica PRAZNA; podpis Jos. Rauq [~]",
    whatEn: "baptized Leopoldina ('40 jun' [illegible — maybe Jun 4/10; the EMŠO says May 24]) — father Alojzij Vetročnik [~] a TEACHER, mother Leopolda Schmelzer [~]; THE DATE CONFLICT: the row '40 jun' [~] vs the registrar's EMŠO 2405900505109 = born May 24, 1900 — MERI: the EMŠO is authoritative for the birth date (the registrar read the civil register); the row stays illegible; h90 = THE SCHOOL HOUSE, the 4th PIN: the SAME TEACHER FAMILY as 1898 (Vetročnik × Schmelzer — 1898 r27 Alojzij) — the daughter Leopoldina after her mother Leopolda!; the teachers at h90: Kopitar (1890–92) → Vetročnik (1898–1900); godparents g. Richard Megušar? [~] (the head teacher? [~]) + g. Hermine Megušar? [~] (his wife); the registrar's note in the cell: 'Umrla dne 14.3.1954 …' [~ — the attribution to r30/r31 doubtful — see h23]; midwife EMPTY; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04105",
    year: 1900,
    scan: 120,
    page: 117,
    whatSi: "krščena Katarina (28./28. 5.) — oče Matija Brinec [~] ½ zemljak, mati Marija Dehlič [~ — P88 1893 »Debič?« = Dehlič — REŠENO z 1900 forenziko]; h23 = 4. PIN ISTA ZVEZA Brinec × Dehlič (1893+1894+1897+1900); EMŠO matičarja 2805900505146 (roj. 28.05.1900 — ujema se z vrstico!); matičar: † 17.11.1984 Bukovec? [~]; opomba »Umrla dne 14.3.1954 Hri?ičeva vas št. 33« [~] — pripisna celica r30/r31 NEJASNA (umrla = ženska; obe kandidatinji) — MERI: pripisana r31 po položaju črte, dvom v honesty; botra Peter Milek [~] + Katarina Dehlič [~] (½ zemlj.); babica Marjeta Fottre [~]; podpis Jos. Rauq [~]",
    whatEn: "baptized Katarina (May 28/28) — father Matija Brinec [~] half smallholder, mother Marija Dehlič [~ — the P88 1893 'Debič?' = Dehlič — RESOLVED by the 1900 forensics]; h23 = the 4th PIN of the same couple Brinec × Dehlič (1893+1894+1897+1900); the registrar's EMŠO 2805900505146 (born May 28, 1900 — matches the row!); the registrar: † Nov 17, 1984 Bukovec? [~]; the note 'Umrla dne 14.3.1954 Hri?ičeva vas št. 33' [~] — the attribution cell r30/r31 UNCLEAR (the deceased is female; both are candidates) — MERI: attributed to r31 by the line position, the doubt in honesty; godparents Peter Milek [~] + Katarina Dehlič [~] (half smallholder); midwife Marjeta Fottre [~]; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04105",
    year: 1900,
    scan: 121,
    page: 118,
    whatSi: "krščena Marija (18. 6.; krsta [prepas — neberljivo]) — oče Janez Muc [~] (bajtar in kovač), mati Ana Kure [~]; hišna forenzika 6x: jasno 9 + svinčnik »Štumer?« [~] (poznejši pripis — priimek kasnejše družine?); h9 = 2. VPIS (1896 Janez Jakobič? × Marija Žumič? → 1900 Muc × Kure — MENJAVA GOSPODINJSTVA; Kure = h1 mati rodbina — križni sklic); botra Jurij Jakobčič [~] + Katarina Lajko [~] (½ zemlj.); matičar: † 15.4.1955 Karlovec [~]; babica Marjeta Fottre [~]; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Jun 18; baptism [a fold — illegible]) — father Janez Muc [~] (a cotter and smith), mother Ana Kure [~]; the house forensics 6x: clearly 9 + a pencil 'Štumer?' [~] (a later note — the surname of a later family?); h9 = the 2nd ENTRY (1896 Janez Jakobič? × Marija Žumič? → 1900 Muc × Kure — A HOUSEHOLD CHANGE; Kure = the h1 mother's family — a cross-link); godparents Jurij Jakobčič [~] + Katarina Lajko [~] (half smallholder); the registrar: † Apr 15, 1955 Karlovac [~]; midwife Marjeta Fottre [~]; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04105",
    year: 1900,
    scan: 121,
    page: 118,
    whatSi: "krščena Ana (21./22. 8.) — starši + botra + babica + duhovnik RAZTRGANI (starševska celica na sken 122 levo fizično odtrgana — podatkovna stran sije skozi; edina izguba staršev med Griblje vpisi 1900); h54 = 3. VPIS (1886 Pintec? × Strauš; 1897 Anton Brinec × Ana Šutala → 1900 starši neznani); matičar: † 29.11.1965 v Gribljah (MMK SO Črnomelj, naselje Griblje l. 1965, št. 34)",
    whatEn: "baptized Ana (Aug 21/22) — the parents + godparents + midwife + priest TORN AWAY (the parents' cell on scan 122 left physically torn off — the data page shines through; the only loss of parents among the 1900 Griblje entries); h54 = the 3rd ENTRY (1886 Pintec? × Strauš; 1897 Anton Brinec × Ana Šutala → 1900 the parents unknown); the registrar: † Nov 29, 1965 in Griblje (MMK SO Črnomelj, the settlement Griblje 1965, no. 34)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1900,
    scan: 121,
    page: 118,
    whatSi: "krščena Marija (29./29. 8.) — oče Alojzij Novak [~] (bajtar), mati Marija Šilak [~]; h16 = 4. VPIS (1886 Plebučar? × Meh; 1897 Janez Jaklič? × Marija Brinec → 1900 Novak × Šilak — MENJAVA); ŠILAK/ŠILAH = h16 1886 mrliška (umrla Marija Šilah ½ zemlj.) — priimek na isti hiši 14 let prej [~ križni sklic]; pripis: † 7/11.02 [~ — dojenčnica † ~2 leti? ali 7./11. 1902 — mesec/dan dvom]; vrstica na DESNEM panelu str. 118 (r45–56) — scoping je IZPUSTIL to vrstico (celostranski pregled 1900); botra Janez Muc [~] (bajtar) + Marija Jakofčič [~] (½ zemljakinja); babica Marjeta Fottre [~]; podpis Jos. Rauq [~]",
    whatEn: "baptized Marija (Aug 29/29) — father Alojzij Novak [~] (a cotter), mother Marija Šilak [~]; h16 = the 4th ENTRY (1886 Plebučar? × Meh; 1897 Janez Jaklič? × Marija Brinec → 1900 Novak × Šilak — A CHANGE); ŠILAK/ŠILAH = the h16 1886 death register (the deceased Marija Šilah, half smallholder) — the surname at the same house 14 years earlier [~ a cross-link]; note: † Feb/Nov 7, 1902 [~ — an infant † ~2 years? or Feb/Nov 7, 1902 — the month/day doubtful]; the row on the RIGHT panel of p. 118 (r45–56) — the scoping OMITTED this row (the full-page survey of 1900); godparents Janez Muc [~] (a cotter) + Marija Jakofčič [~] (half smallholder); midwife Marjeta Fottre [~]; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1900,
    scan: 121,
    page: 118,
    whatSi: "krščen Alojzij (9./9. 9.) — oče Janez Požek [~] ½ zemljak (ISTI oče kot 1890/92/95; 1889 »Franz Požek ¼«), mati Katarina Kranbič [~ — NOVA ŽENA: 1889–95 mati Ana Dragoš → 1900 Katarina Kranbič — MENJAVA ŽENE [~]]; h58 = 5. PIN (Požek kontinuiteta 1889–1900) + PRVA MENJAVA ŽENE na h58 v vzorcu; pripis: † 8/5.03 [~ — dojenček/otrok † ~8 mesecev ali 8.5.1903]; scoping je IZPUSTIL to vrstico (celostranski pregled 1900); botra Marko Hlebec [~] + Ana Požak [~] (½ zemljak); babica [neberljivo — kratica?]; podpis Jos. Rauq [~]",
    whatEn: "baptized Alojzij (Sep 9/9) — father Janez Požek [~] half smallholder (the SAME father as 1890/92/95; 1889 'Franz Požek ¼'), mother Katarina Kranbič [~ — A NEW WIFE: 1889–95 the mother Ana Dragoš → 1900 Katarina Kranbič — A WIFE CHANGE [~]]; h58 = the 5th PIN (the Požek continuity 1889–1900) + the FIRST WIFE CHANGE at h58 in the sample; note: † May 8, 1903 [~ — an infant/child † ~8 months or May 8, 1903]; the scoping OMITTED this row (the full-page survey of 1900); godparents Marko Hlebec [~] + Ana Požak [~] (half smallholder); midwife [illegible — an abbreviation?]; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1900,
    scan: 123,
    page: 120,
    whatSi: "krščen Alojzij (18./18. 10.) — oče Martin Papič [~ — Papič/Fapič/Tepič/Sapič Kurrent] ½ zemljak, mati Marjeta Straus [~]; h31 = 11. VPIS; 6. PIN ISTA ZVEZA Martin Papič × Marjeta Straus (1887+1890+1891+1894+1897+1900 — najdaljša zaporedna zveza vzorca); opomba »Matičar« [~] v krajnem stolpcu (matičarjeva oznaka, ne del kraja); matičar: † 28.12.1980 Murska Sobota (MMU M. Sobota l. 1980, str. 114, zop. št. 88); scoping je IZPUSTIL to vrstico (celostranski pregled 1900); botra Marko Pezdirec [~] + Katarina Hlobučan? [~] (½ zemlj.); babica Marjeta Fottre [~]; podpis Jos. Rauq [~]",
    whatEn: "baptized Alojzij (Oct 18/18) — father Martin Papič [~ — Papič/Fapič/Tepič/Sapič Kurrent] half smallholder, mother Marjeta Straus [~]; h31 = the 11th ENTRY; the 6th PIN of the same couple Martin Papič × Marjeta Straus (1887+1890+1891+1894+1897+1900 — the sample's longest consecutive couple); a note 'Matičar' [~] in the village column (the registrar's mark, not part of the village); the registrar: † Dec 28, 1980 Murska Sobota (MMU M. Sobota 1980, p. 114, no. 88); the scoping OMITTED this row (the full-page survey of 1900); godparents Marko Pezdirec [~] + Katarina Hlobučan? [~] (half smallholder); midwife Marjeta Fottre [~]; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04105",
    year: 1900,
    scan: 123,
    page: 120,
    whatSi: "krščena Barbara (5./5. 11.) — oče Matija Brinec [~] ½ zemljak, mati Katarina Segina [~]; h25 = 4. VPIS (1886 poroka Klepec × Gomec; 1893 Matija Hrižan × Ana Požek; 1896 Janez Klepec? × Katarina Tome? → 1900 Brinec × Segina — MENJAVA); SEGINA signal 4: mati Katarina Segina + boter Leopold Šegina (veriga h70 1893 Nikolaj Segina → h1 1899 Nikolaj Segina → 1900 boter/mati); babica Ana Hrižan (HRIŽAN signal); matičar: † 12/3-[1964?1969 — števka neberljiva] v Gribljah; scoping je IZPUSTIL to vrstico (celostranski pregled 1900); botra Leopold Šegina [~] + Ana Brinec [~] (½ zemlj.); podpis Jos. Rauq [~]",
    whatEn: "baptized Barbara (Nov 5/5) — father Matija Brinec [~] half smallholder, mother Katarina Segina [~]; h25 = the 4th ENTRY (1886 the marriage Klepec × Gomec; 1893 Matija Hrižan × Ana Požek; 1896 Janez Klepec? × Katarina Tome? → 1900 Brinec × Segina — A CHANGE); the SEGINA signal 4: the mother Katarina Segina + the godparent Leopold Šegina (the chain h70 1893 Nikolaj Segina → h1 1899 Nikolaj Segina → 1900 the godparent/mother); the midwife Ana Hrižan (the HRIŽAN signal); the registrar: † Mar/Dec 12-[1964?1969 — the digit illegible] in Griblje; the scoping OMITTED this row (the full-page survey of 1900); godparents Leopold Šegina [~] + Ana Brinec [~] (half smallholder); signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1900,
    scan: 124,
    page: 121,
    whatSi: "krščen Nikolaj (17./17. 11.) — oče Martin Straus [~] (bajtar), mati Barbara Spudič [~]; h45 = 3. PIN ISTA ZVEZA Martin Straus × Barbara Spudič (1896+1897+1900) — 04455 POROČNI LEAD: krstno 3× POTRJENA ista zveza — iskati poroko v 04455; pripis: † 9/2.03 — otrok † ~15 mesecev (9.2.1903); botra Matija Urh [~] + Marija Urh [~] (½ zemlj.) — Urh = h32/h90 mreža; babica Marjeta Fottre [~]; podpis Janez R. Klunček? [~]",
    whatEn: "baptized Nikolaj (Nov 17/17) — father Martin Straus [~] (a cotter), mother Barbara Spudič [~]; h45 = the 3rd PIN of the same couple Martin Straus × Barbara Spudič (1896+1897+1900) — the 04455 MARRIAGE LEAD: the same couple christened 3× CONFIRMED — look for the marriage in 04455; note: † Feb 9, 1903 — the child † ~15 months (Feb 9, 1903); godparents Matija Urh [~] + Marija Urh [~] (half smallholder) — Urh = the h32/h90 web; midwife Marjeta Fottre [~]; signature Janez R. Klunček? [~]",
    status: "DOCUMENTED",
  },
  // ——— P96: polno leto 1901 (vsi Griblje vpisi, str. 122–129 = skeni 125–135) ———
  // NOVELA P96: TRIJE podvojeni skeni (127/128, 129/130, 133/134); sken 128 =
  // str. 124 z nalepkama PREPOGNJENIMA (r32/r33 rešeni); stran == sken − 3
  // (125–127) / − 4 (129–130) / − 5 (131–132) / − 6 (135). 10 vpisov / 9 hiš —
  // h12 ×2 = PRVA PONOVITEV znotraj leta po 1893 (NARE 1894–1900 prekinjeno;
  // r1 Juvan? × Cvetkovič vs r36 Straus × Jakobič — več-družinska hiša).
  // NOVA HIŠA h19 (prvi matrični dokaz; PT nabor; oče bajtar). h44 + h54 v PT
  // luknji (že v PT_GAP_KNOWN). Meseci: r65–r69 NOVEMBER (EMŠO r66/r68),
  // December od r70; r36 »Jurij«? = JUNI. Duhovniki: Kulbinek? 7× (= P95
  // »Klunček?«) + Rauq 2× + NOV podpis Fran. Dostál. Babica Toter 6×.
  // Excluded: r35 (Griblje [~], hiša pod trakom), r47 (nalepka 26.01.1989).
  // Dokaz: research/issue17/parish-baptism-1901.json;
  // verifikator: scripts/p96_parish_baptism_1901.py --check (I1–I10).
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1901,
    scan: 125,
    page: 122,
    whatSi: "krščen Peter (3./4. 1.) — oče Gregor Juvan? [~] ½ zemljak, mati Barbura Cvetkovič [~]; glava-vrstica 1901 (r1 pod veliko glavo); h12 = 6. VPIS (1892 Dragoš, 1894, 1895, 1897, 1899); pripomba † 14.12.1970 v Gribljah (MMK) + modra imenska varianta [~]; botra Peter Toter + Marija Straus [~]; babica Marjeta Toter; podpis Janez R. Kulbinek? [~]",
    whatEn: "baptized Peter (Jan 3/4) — father Gregor Juvan? [~] half smallholder, mother Barbura Cvetkovič [~]; the header row of 1901 (r1 under the large heading); h12 = the 6th ENTRY (1892 Dragoš, 1894, 1895, 1897, 1899); note † Dec 14, 1970 in Griblje (MMK) + a blue name variant [~]; godparents Peter Toter + Marija Straus [~]; midwife Marjeta Toter; signature Janez R. Kulbinek? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1901,
    scan: 129,
    page: 125,
    whatSi: "krščen Alojzij (17./17. 6.) — oče Matija Straus [~] ½ zemljak, mati Marija Jakobič [~]; h12 = 7. VPIS — PRVA PONOVITEV znotraj leta po 1893 (NARE 1894–1900 prekinjeno po 8 letih); ISTA hiša kot r1 z RAZLIČNIMA starševskima paroma (več-družinska hiša/menjava); mesec »Jurij«? [~] = JUNI (sekvence r39 July 10); pripis † 17/6.02 — dojenček; botra Matija Straus + Barbura Jakobič; babica Marjeta Toter; podpis Kulbinek? [~]",
    whatEn: "baptized Alojzij (Jun 17/17) — father Matija Straus [~] half smallholder, mother Marija Jakobič [~]; h12 = the 7th ENTRY — the FIRST within-year repeat since 1893 (the NARE run 1894–1900 broken after 8 years); the SAME house as r1 with a DIFFERENT parent couple (a multi-family house/change); the month »Jurij«? [~] = JUNE (the sequence r39 July 10); note † Jun 17, 1902 — an infant; godparents Matija Straus + Barbura Jakobič; midwife Marjeta Toter; signature Kulbinek? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04105",
    year: 1901,
    scan: 131,
    page: 126,
    whatSi: "krščena Marija (21./28. 7.) — oče Jakob Toter [~] ½ zemljak, mati Katarina Jakobšič [~]; h7 = 2. VPIS (1890 prvi); EMŠO pripomba 2107901505598 → 21.07.1901 (sidro); hišna Kurrent 2/7 dvom [~], kraj Griblje berljiv pod pripombo; babica Marjeta Toter (oče Jakob = njena rodbina — 6× babica 1901); poročena 21.11.1927, † 16.10.1967 Črnomelj; matičar Simonović Nuša 15.12.1987; podpis Kulbinek? [~]",
    whatEn: "baptized Marija (Jul 21/28) — father Jakob Toter [~] half smallholder, mother Katarina Jakobšič [~]; h7 = the 2nd ENTRY (1890 the first); EMŠO note 2107901505598 → Jul 21, 1901 (an anchor); the house number Kurrent 2/7 doubt [~], the village Griblje legible under the note; midwife Marjeta Toter (the father Jakob = her family — 6× midwife 1901); married Nov 21, 1927, † Oct 16, 1967 Črnomelj; registrar Simonović Nuša Dec 15, 1987; signature Kulbinek? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04105",
    year: 1901,
    scan: 131,
    page: 126,
    whatSi: "krščen Anton (13./13. 8.) — oče Peter Gruzec? [~] žajfar, mati Ana Butala [~]; h54 = 4. VPIS (1886, 1897, 1900) — hiša v PT luknji (PT_GAP_KNOWN vsebuje 54 — brez nove številke); babica Marija Tolar? [~]; podpis Kulbinek? [~]",
    whatEn: "baptized Anton (Aug 13/13) — father Peter Gruzec? [~] a linen-weaver, mother Ana Butala [~]; h54 = the 4th ENTRY (1886, 1897, 1900) — the house in the PT gap (PT_GAP_KNOWN already contains 54 — no new number); midwife Marija Tolar? [~]; signature Kulbinek? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "2",
    bookSignature: "04105",
    year: 1901,
    scan: 131,
    page: 126,
    whatSi: "krščen Nikolaj (17./17. 8.) — oče Nikolaj Tome [~] ½ zemljak, mati Barbura Jurajevič [~]; h2 = 6. VPIS (1887, 1889, 1891, 1894, 1897); pripis † 17/3.03 — dojenček; babica Barbura Tome; podpis Kulbinek? [~]",
    whatEn: "baptized Nikolaj (Aug 17/17) — father Nikolaj Tome [~] half smallholder, mother Barbura Jurajevič [~]; h2 = the 6th ENTRY (1887, 1889, 1891, 1894, 1897); note † Mar 17, 1903 — an infant; midwife Barbura Tome; signature Kulbinek? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "17",
    bookSignature: "04105",
    year: 1901,
    scan: 131,
    page: 126,
    whatSi: "krščen Anton (11./11. 9.) — oče Janez Kralj [~] ½ zemljak, mati Doroteja Finlak? [~]; h17 = 3. VPIS (1887, 1894); botra Jurij Straus [~] + Marija Mikl [~]; babica Marjeta Toter; † 2.2.1976 Metlika (MMK l. 1976 str. 374 zap. št. 51); poročen 21.10.1950; podpis Kulbinek? [~]",
    whatEn: "baptized Anton (Sep 11/11) — father Janez Kralj [~] half smallholder, mother Doroteja Finlak? [~]; h17 = the 3rd ENTRY (1887, 1894); godparents Jurij Straus [~] + Marija Mikl [~]; midwife Marjeta Toter; † Feb 2, 1976 Metlika (MMK 1976 p. 374 no. 51); married Oct 21, 1950; signature Kulbinek? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1901,
    scan: 131,
    page: 126,
    whatSi: "krščena Doroteja (11./12. 10.) — oče Matija Mitek? [Mrtek?] ½ zemljak, mati Katarina Pošek? [~]; h65 = 7. VPIS (1887, 1889, 1893, 1895, 1897, 1900); EMŠO pripomba 1110901503024 → 11.10.1901 (sidro); babica Marija Mikl; poročena 6.6.1932, † 9.11.1991; matičar Simonović Nuša 13.12.1982; podpis Kulbinek? [~]",
    whatEn: "baptized Doroteja (Oct 11/12) — father Matija Mitek? [Mrtek?] half smallholder, mother Katarina Pošek? [~]; h65 = the 7th ENTRY (1887, 1889, 1893, 1895, 1897, 1900); EMŠO note 1110901503024 → Oct 11, 1901 (an anchor); midwife Marija Mikl; married Jun 6, 1932, † Nov 9, 1991; registrar Simonović Nuša Dec 13, 1982; signature Kulbinek? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1901,
    scan: 132,
    page: 127,
    whatSi: "krščena Ivana (5./5. 11.) — oče Janez Božek? [~] ½ zemljak, mati Ana Finec? [Simec? — F/S dvom]; h24 = 9. VPIS (1887, 1888, 1890, 1892, 1893, 1895 ×2, 1897); pripis »Umrła 11.10.1946 griblje št 24« SAMOPOTRJUJE hišo; babica Marjeta Toter; podpis Jos. Rauq",
    whatEn: "baptized Ivana (Nov 5/5) — father Janez Božek? [~] half smallholder, mother Ana Finec? [Simec? — F/S doubt]; h24 = the 9th ENTRY (1887, 1888, 1890, 1892, 1893, 1895 ×2, 1897); the note »Umrła 11.10.1946 griblje št 24« SELF-CONFIRMS the house; midwife Marjeta Toter; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "19",
    bookSignature: "04105",
    year: 1901,
    scan: 132,
    page: 127,
    whatSi: "krščena Katarina (21./21. 11.) — oče Nikolaj Hriče? [~] bajtar, mati Cecilija Hvalica? [~]; h19 = NOVA HIŠA — PRVI MATRIČNI DOKAZ (81. hiša v vitals; hiša v PT naboru 1825); oče bajtar (najemnik kmeta); botra pod madežem [~]; babica Marjeta Toter; podpis Jos. Rauq",
    whatEn: "baptized Katarina (Nov 21/21) — father Nikolaj Hriče? [~] a cotter, mother Cecilija Hvalica? [~]; h19 = A NEW HOUSE — THE FIRST REGISTRY PROOF (the 81st house in vitals; the house in the 1825 PT nabor); the father a cotter; godparents under a stain [~]; midwife Marjeta Toter; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1901,
    scan: 134,
    page: 128,
    whatSi: "krščen Francišek (13./14. 12.) — oče Martin Jurajevič [~] bajtar, mati Marjana Krašovec [~]; h44 = 3. VPIS (1887, 1888) — hiša v PT luknji (PT_GAP_KNOWN vsebuje 44 — brez nove številke); kraj z dodatnim koncem »v Mašperar?« [~ — neberljiv mikrotoponim]; NOV DUHOVNIK podpis Fran. Dostál (češko — tudi ne-Griblje r63/r67/r70/r71/r80/r83); botra Danijel Murn (trgovec) + Ana Krambič; babica Ana Mavrefič; † 6.11.1969 Novo mesto",
    whatEn: "baptized Francišek (Dec 13/14) — father Martin Jurajevič [~] a cotter, mother Marjana Krašovec [~]; h44 = the 3rd ENTRY (1887, 1888) — the house in the PT gap (PT_GAP_KNOWN already contains 44 — no new number); the village carries an extra ending »v Mašperar?« [~ — an illegible microtoponym]; A NEW PRIEST signature Fran. Dostál (Czech — also non-Griblje r63/r67/r70/r71/r80/r83); godparents Danijel Murn (a merchant) + Ana Krambič; midwife Ana Mavrefič; † Nov 6, 1969 Novo mesto",
    status: "DOCUMENTED",
  },

  // ——— P97: polno leto 1902 (vsi Griblje vpisi, str. 129 dno – 136 = skeni 135–144) ———
  // NOVELA P97: 1902 = NOVA TISKANA knjiga (»Rojstna in krstna knjiga.« — vse
  // kolone na ENI strani, predtisk »Leto 18|02«); DVA dup para (137/138 = str.
  // 131, 141/142 = str. 134); stran == sken − 6 (135–137) / − 7 (139–141) /
  // − 8 (143–144). 12 vpisov / 12 hiš — NARE se nadaljuje (8. leto) + PRVO
  // LETO BREZ NOVIH HIŠ (h3 = 1889, h87 = 1895 — že v vitals). PT 11/1 (h58
  // že v PT_GAP_KNOWN). Duhovniki: Dostál 8× (»Stanislav Dostál« jasno 3×;
  // P96 »Fran. Dostál« — isti z dvema zapisoma ALI dva — MERI) + Rauq 4×;
  // Kulbinek 0×. Babica Toter 9× (12/12). ŽELJKO signali 16+17 (r12 botra
  // Marija Željko, r50 boter Nikolaj Željko?); SEGINA vrnitev h30 (r16 —
  // signal 5) + h25 (r59 — 5+6); STRAUS × SPUDIČ h16 (r46 — 3. hiša istega
  // para; 04455 lead 5× krstno). Excluded: r33 (hiša pod zapisom), r62
  // (nalepka). Dokaz: research/issue17/parish-baptism-1902.json;
  // verifikator: scripts/p97_parish_baptism_1902.py --check (I1–I10).
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1902,
    scan: 136,
    page: 130,
    whatSi: "krščena Ivana (27./27. 1.) — oče Janez Povk? [~] ½ zemljak, mati Katarina Hambič? [~]; h58 = 6. VPIS (1889, 1890, 1892, 1895, 1900; 1900 P95 menjava žene Dragoš → Kranbič) — 1902 NOVA branja očeta »Povk?« (ali menjava družine — MERI, odprt); pripis † 13/1.04 [~] — otrok; botra Marko Hlebce + Marija Hambič? (½ zemljak); babica Barbura Adamič? [~]; podpis Jos. Rauq [~]",
    whatEn: "baptized Ivana (Jan 27/27) — father Janez Povk? [~] half smallholder, mother Katarina Hambič? [~]; h58 = the 6th ENTRY (1889, 1890, 1892, 1895, 1900; the 1900 P95 wife change Dragoš → Kranbič) — 1902 a NEW reading of the father »Povk?« (or a family change — MERI, open); note † Jan 13, 1904 [~] — a child; godparents Marko Hlebce + Marija Hambič? (half smallholder); midwife Barbura Adamič? [~]; signature Jos. Rauq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "87",
    bookSignature: "04105",
    year: 1902,
    scan: 136,
    page: 130,
    whatSi: "krščen Anton (9./10. 3.) — oče Marko Perdinec? [~] bajtar, mati Katarina Žugelj; h87 = 2. VPIS (1895 oče Marko Pegdirec? [~] bajtar — P90) → 1902 oče Marko Perdinec? [= Pegdirec? — KURRENT varianta ISTEGA očeta — MERI]; boter Martin Čapič? [~] bajtar + botra Marija Željko (½ zemljak — ŽELJKO signal 16; 1895 podcelica že Nikol. Hrižan × Marija Željko!); babica Marjeta Toter [Tota? ~]; podpis Dostál [~]",
    whatEn: "baptized Anton (Mar 9/10) — father Marko Perdinec? [~] a cotter, mother Katarina Žugelj; h87 = the 2nd ENTRY (the 1895 father Marko Pegdirec? [~] a cotter — P90) → 1902 the father Marko Perdinec? [= Pegdirec? — a KURRENT variant of the SAME father — MERI]; godfather Martin Čapič? [~] a cotter + godmother Marija Željko (half smallholder — the ŽELJKO signal 16; the 1895 sub-cell already Nikol. Hrižan × Marija Željko!); midwife Marjeta Toter [Tota? ~]; signature Dostál [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1902,
    scan: 136,
    page: 130,
    whatSi: "krščen Jožef (18./18. 3.) — oče Nikolaj Segina [~] ½ zemljak, mati Marjeta Milek [~]; h30 = 5. DRUŽINA — SEGINA VRNITEV (1895 mati Katarina Segina → 1902 oče Nikolaj Segina — SEGINA veriga h70 1893 → h30 1895 → h1 1899 → h30 1902, signal 5); hišna forenzika 4×: jasno 30 (ne 36!); botra Janez + Katarina Vrižan? [~]; babica Marija Adamič? [~]; podpis Dostál [~]; † 8/2.03 [~]",
    whatEn: "baptized Jožef (Mar 18/18) — father Nikolaj Segina [~] half smallholder, mother Marjeta Milek [~]; h30 = the 5th FAMILY — THE SEGINA RETURN (1895 the mother Katarina Segina → 1902 the father Nikolaj Segina — the SEGINA chain h70 1893 → h30 1895 → h1 1899 → h30 1902, the signal 5); the house forensics 4×: clearly 30 (not 36!); godparents Janez + Katarina Vrižan? [~]; midwife Marija Adamič? [~]; signature Dostál [~]; † Feb 8, 1903 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1902,
    scan: 137,
    page: 131,
    whatSi: "krščen Alojzij (17./18. 5.) — oče Nikolaj Milek ½ zemljak, mati Ana Žurrič? [~]; h22 = 2. VPIS (1899 prvi — P94 NOVA HIŠA, oče Nikolaj Milek × Marija Klepec) → 1902 MENJAVA ŽENE (Klepec → Žurrič?) ALI druga branja — MERI; ime otroka pod modrimi matičarskimi zapisi (temno črnilo: »Alojzij« — 4× zoom); botra Janez + Marija Brinec (½ zemljak); babica Marjeta Toter [~]; podpis Stanislav Dostál [~]; matičar † 7.12.1961 + poročen 15.2.1943",
    whatEn: "baptized Alojzij (May 17/18) — father Nikolaj Milek half smallholder, mother Ana Žurrič? [~]; h22 = the 2nd ENTRY (1899 the first — the P94 NEW HOUSE, father Nikolaj Milek × Marija Klepec) → 1902 a WIFE CHANGE (Klepec → Žurrič?) OR other readings — MERI; the child's name under the blue registrar's notes (dark ink: »Alojzij« — a 4× zoom); godparents Janez + Marija Brinec (half smallholder); midwife Marjeta Toter [~]; signature Stanislav Dostál [~]; the registrar † Dec 7, 1961 + married Feb 15, 1943",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04105",
    year: 1902,
    scan: 139,
    page: 132,
    whatSi: "krščen Janez (3./3. 6.) — oče Matija Papič? [~] ½ zemljak, mati Katarina Novak; h3 = 2. VPIS (1889 oče Nikolaj Županič? × Katarina Pezdirec — P84) → 1902 MENJAVA družine (Papič? × Novak); botra Jožef + Katarina Žudmič? [~] (½ zemljak); babica Marija Papič? [~]; podpis Dostál [~]; † 25/8.1912 [~] — otrok † pri 10 letih",
    whatEn: "baptized Janez (Jun 3/3) — father Matija Papič? [~] half smallholder, mother Katarina Novak; h3 = the 2nd ENTRY (the 1889 father Nikolaj Županič? × Katarina Pezdirec — P84) → 1902 a FAMILY CHANGE (Papič? × Novak); godparents Jožef + Katarina Žudmič? [~] (half smallholder); midwife Marija Papič? [~]; signature Dostál [~]; † Aug 25, 1912 [~] — the child † at 10 years",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1902,
    scan: 139,
    page: 132,
    whatSi: "krščen Alojzij (3./3. 7.) — oče Janez Šimec ½ zemljak, mati Marija Kure; h27 = 7. VPIS (1887, 1890, 1892, 1893 ×2, 1899 — Knekar?/Stukar? menjava branja) → 1902 NOVA DRUŽINA Šimec × Kure (ŠIMEC križni sklic h34 1887; KURE mreža h1/h9/h59); EMŠO pripomba 0307902505120 [~ — sredina raztrgana] → 03.07.1902 (sidro); botra Janez Pček? [~] + Ana Brinec (½ zemljak); babica Marjeta Toter; podpis Stanislav Dostál [~]; † 10.8.1976 Črnomelj, poročen 16.11.1930",
    whatEn: "baptized Alojzij (Jul 3/3) — father Janez Šimec half smallholder, mother Marija Kure; h27 = the 7th ENTRY (1887, 1890, 1892, 1893 ×2, 1899 — the Knekar?/Stukar? reading change) → 1902 A NEW FAMILY Šimec × Kure (the ŠIMEC cross-link h34 1887; the KURE web h1/h9/h59); the EMŠO note 0307902505120 [~ — the middle torn] → Jul 3, 1902 (an anchor); godparents Janez Pček? [~] + Ana Brinec (half smallholder); midwife Marjeta Toter; signature Stanislav Dostál [~]; † Aug 10, 1976 Črnomelj, married Nov 16, 1930",
    status: "DOCUMENTED",
  },
  {
    houseNo: "77",
    bookSignature: "04105",
    year: 1902,
    scan: 140,
    page: 133,
    whatSi: "krščen Alojzij (29./29. 7.) — oče Nikolaj Cindrič cevljar, mati Marija Maovar? [~]; h77 = 2. VPIS (1890 prvi — P85: oče Jurij Pošek bajtar) → 1902 MENJAVA družine (Pošek → Cindrič); botra Matija Milek + Marjeta Šorek? [~] (½ zemljak); babica Marjeta Toter; podpis Jos. Rauq; matičar † 14.2.1968 Črnomelj (MMK ČB 1968)",
    whatEn: "baptized Alojzij (Jul 29/29) — father Nikolaj Cindrič a shoemaker, mother Marija Maovar? [~]; h77 = the 2nd ENTRY (1890 the first — the P85: father Jurij Pošek a cotter) → 1902 a FAMILY CHANGE (Pošek → Cindrič); godparents Matija Milek + Marjeta Šorek? [~] (half smallholder); midwife Marjeta Toter; signature Jos. Rauq; the registrar † Feb 14, 1968 Črnomelj (MMK ČB 1968)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1902,
    scan: 140,
    page: 133,
    whatSi: "krščen Alojzij (7./8. 8.) — oče Martin Straus bajtar, mati Barbura Spudič; h16 = 4. VPIS (1886, 1897, 1900 — 1900 Novak × Šilak) → 1902 STRAUS × SPUDIČ — ISTA ZVEZA kot h45 (1896+1897+1900) + h40 (1899): zdaj na TRETJI hiši (h45 → h40 → h16); 04455 POROČNI LEAD krstno 5× POTRJEN; botra Matija Ule + Amalija? [~] Šimec (½ zemljak); babica Marjeta Toter; podpis Jos. Rauq; † 1/9.03 [~]",
    whatEn: "baptized Alojzij (Aug 7/8) — father Martin Straus a cotter, mother Barbura Spudič; h16 = the 4th ENTRY (1886, 1897, 1900 — the 1900 Novak × Šilak) → 1902 STRAUS × SPUDIČ — THE SAME COUPLE as h45 (1896+1897+1900) + h40 (1899): now at the THIRD house (h45 → h40 → h16); the 04455 MARRIAGE LEAD christened 5× CONFIRMED; godparents Matija Ule + Amalija? [~] Šimec (half smallholder); midwife Marjeta Toter; signature Jos. Rauq; † Sep 1, 1903 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04105",
    year: 1902,
    scan: 140,
    page: 133,
    whatSi: "krščen Matija (26./26. 8.) — oče Janez Murov? [Muc? ~ — 1895 Janez Muc mlinar/kovač] kovač? [~], mati Ana Kure; h91 = 3. VPIS (1893 Novak, 1895 Muc — OČE MENJAN) → 1902 Muc?/Murov? × Kure — 1895+1902 VERJETNO ISTA ZVEZA (MERI); boter Nikolaj Željko? [~] + botra Marija Jakofčič? [~] (½ zemljak) — ŽELJKO signal 17 (h1 rodbina; boter Željko že 1893!); babica Marjeta Toter; podpis Stanislav Dostál [~]; matičar žig »dne 03.09.2007 Matičar-ka: Belopavlonič«",
    whatEn: "baptized Matija (Aug 26/26) — father Janez Murov? [Muc? ~ — the 1895 Janez Muc a miller/smith] a smith? [~], mother Ana Kure; h91 = the 3rd ENTRY (1893 Novak, 1895 Muc — the father CHANGED) → 1902 Muc?/Murov? × Kure — 1895+1902 PROBABLY THE SAME COUPLE (MERI); godfather Nikolaj Željko? [~] + godmother Marija Jakofčič? [~] (half smallholder) — the ŽELJKO signal 17 (the h1 family; the godfather Željko already 1893!); midwife Marjeta Toter; signature Stanislav Dostál [~]; the registrar stamp »Sep 3, 2007 registrar: Belopavlonič«",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1902,
    scan: 140,
    page: 133,
    whatSi: "krščena Frančiška (27./27. 8.) — oče Janez Vrižan? [Križan? ~] ½ zemljak, mati Katarina Straus; h36 = 6. VPIS (1886 ×2, 1894, 1896, 1898) — 1902 Vrižan? × Straus (botri Straus par!); botra Matija + Amalija? [Doroteja? ~] Straus (½ zemljak); babica Marjeta Toter; podpis Jos. Rauq; † 1/5.03 [~]",
    whatEn: "baptized Frančiška (Aug 27/27) — father Janez Vrižan? [Križan? ~] half smallholder, mother Katarina Straus; h36 = the 6th ENTRY (1886 ×2, 1894, 1896, 1898) — the 1902 Vrižan? × Straus (the Straus godparent couple!); godparents Matija + Amalija? [Doroteja? ~] Straus (half smallholder); midwife Marjeta Toter; signature Jos. Rauq; † May 1, 1903 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04105",
    year: 1902,
    scan: 141,
    page: 134,
    whatSi: "krščen Jožef (1./2. 10.) — oče Matija Brinec ½ zemljak, mati Katarina Segina; h25 = 4. VPIS (1893, 1896, 1900) — 1900+1902 ISTA ZVEZA Brinec × Segina (SEGINA signal 4 = P95) — 1902 signali 5+6: mati Katarina Segina + boter Danijel Segina + botra Marija Brinec (½ zemljak); babica Marjeta Toter; podpis Stanislav Dostál (jasno!); pripis poročen 27.4.1929 [~]",
    whatEn: "baptized Jožef (Oct 1/2) — father Matija Brinec half smallholder, mother Katarina Segina; h25 = the 4th ENTRY (1893, 1896, 1900) — 1900+1902 the SAME COUPLE Brinec × Segina (the SEGINA signal 4 = P95) — 1902 the signals 5+6: the mother Katarina Segina + the godfather Danijel Segina + the godmother Marija Brinec (half smallholder); midwife Marjeta Toter; the signature Stanislav Dostál (clear!); the note married Apr 27, 1929 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1902,
    scan: 143,
    page: 135,
    whatSi: "krščena Ana (13./13. 12.) — oče Janez Brinec ½ zemljak, mati Marija Podirec; h14 = 3. VPIS (1896, 1900) — oče Janez Brinec (1896 dvom P91 → 1900 REŠENO → 1902 potrjeno); botra Marko + Marija Hrižan (½ zemljak); babica Marjeta Toter; podpis Stanislav Dostál [~]; matičar Umrła dne 15.5.1984 Hodošan (MMK nas. Hodošan 1984, št. 29, zap. št. 1)",
    whatEn: "baptized Ana (Dec 13/13) — father Janez Brinec half smallholder, mother Marija Podirec; h14 = the 3rd ENTRY (1896, 1900) — the father Janez Brinec (the 1896 doubt P91 → the 1900 RESOLVED → the 1902 confirmed); godparents Marko + Marija Hrižan (half smallholder); midwife Marjeta Toter; signature Stanislav Dostál [~]; the registrar † May 15, 1984 Hodošan (MMK nas. Hodošan 1984, no. 29, entry 1)",
    status: "DOCUMENTED",
  },

  // ——— P98: polno leto 1903 (vsi Griblje vpisi, str. 136 sredina – 143 = skeni 141–152) ———
  // NOVELA P98: EN podvojen par skenov (148/149 = str. 140, rows 46–57;
  // s149 bolj čitljiv); stran == sken − 8 (141–148) / − 9 (150–152 — premik za dup par). Format 1903 = NOVA
  // TISKANA knjiga (kot 1902 — »Rojstna in krstna knjiga.«, predtiskano
  // »Leto 18|03«). Okvir: glava »1903.« NA SREDINI str. 136 (sken 144, P97
  // dokazano; r1 = Griblje 24 4./5. Januar) – row 82 na str. 143 (sken 152;
  // glava »1904« pod r82 — 1904 r1 = Krasinec 37, P99 lead); 82 vrstic.
  // 12 vpisov / 12 hiš — NARE 9. leto (vsaka hiša 1×; 1901 edini prelom z
  // h12 ×2) + DRUGO LETO ZAPORED BREZ NOVIH HIŠ (h83 luknja 1890–1902
  // zaplodana — 3. VPIS; vse 12 že v vitals). PT 11/1 (h58 v luknji — že v
  // PT_GAP_KNOWN). Duhovniki (celo leto): Dostál 44× + Jos. Ravq 32× +
  // Levic? 1× + manjkajoči 5×; na Gribljih: Dostál 6× (Stanislav jasno 1×)
  // + Ravq 6×; Kulbinek 0×. Babica (celo leto): 76 imenovanih / 2 prazni
  // (r52+r53); na Gribljih: Toter 6× + Mavretič 2× + Mih 2× + Perdinec 1×
  // + Delak 1× (12/12). Sidra: r1 h24 10. VPIS (najbolj vpisovana hiša);
  // r55 REŠITEV P97 MERI (»Povk? × Hambič?« = »Požek × Kambič« — ISTI PAR);
  // r76 h30 2. VPIS ZAPORED (menjava žene Milek → Brinec — MERI); SEGINA
  // signali 7+8; ŽELJKO signali 18–21 (4× botra); DRAGOS signal 7. Excluded:
  // NI (vse 12 čitljive; r82 = Dragoše → anomalija razveza).
  // Dokaz: research/issue17/parish-baptism-1903.json;
  // verifikator: scripts/p98_parish_baptism_1903.py --check (I1–I10).
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1903,
    scan: 144,
    page: 136,
    whatSi: "krščen Jožef (4./5. 1. — svinčnik »Matijo?« nad imenom — MERI) — oče Matevž Juvančič? [~ (ime+priimek pod trakom — branje »…vež Jucajveč/Juvanjveč«); stan neberljiv], mati Marijana Krašovec; h24 = 10. VPIS (1887, 1888, 1890, 1892, 1893, 1895×2, 1897, 1901) — NAJBOLJ VPISOVANA gibriljska hiša registra; botra Danijel Muen [~ (stan: kmetunar?/Argovec?)] + Ana Kambič; babica Ana Mavretič; podpis Jos. Ravq [~]; marginalija (modro, delno neberljivo): »Zakonec Juvarič? Jožef umrl dne 28.9.1976 (MMK … l.1976, črn. 26, zop. št. 15); Gradac 15.11.1976; Velencič Jože 15.12.1982« [~]",
    whatEn: "baptized Jožef (Jan 4/5 — the pencil 'Matijo?' above the name — MERI) — father Matevž Juvančič? [~ (the name+surname under a strip — the reading '…vež Jucajveč/Juvanjveč'); the status illegible], mother Marijana Krašovec; h24 = the 10th ENTRY (1887, 1888, 1890, 1892, 1893, 1895×2, 1897, 1901) — THE MOST-ENTERED Griblje house of the register; godparents Danijel Muen [~ (the status: a farmhand?/Argovec?)] + Ana Kambič; midwife Ana Mavretič; signature Jos. Ravq [~]; a blue marginalia (partly illegible): 'The spouse Juvarič? Jožef died Sep 28, 1976 (MMK … 1976, no. 26, ref. 15); Gradac Nov 15, 1976; Velencič Jože Dec 15, 1982' [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1903,
    scan: 144,
    page: 136,
    whatSi: "krščen Matija (5./5. 1.) — oče Matija Štrucelj? [~ (branja »Švrucej/Švagelj« — Kurrent), ½ zemljak? (stan pod trakom)], mati Marija Mehle? [~]; h5 = 2. VPIS (1891 — P86); fold-damage str. 136 (lepilni trak) — očetova celica pod njim; boter Janez Dragoš + Katarina Toter (½ zemljak) — DRAGOS signal 7 (boter = h12 oče 1892–93); babica Marjeta Toter; podpis Jos. Ravq [~]",
    whatEn: "baptized Matija (Jan 5/5) — father Matija Štrucelj? [~ (the readings 'Švrucej/Švagelj' — Kurrent), a half smallholder? (the status under a strip)], mother Marija Mehle? [~]; h5 = the 2nd ENTRY (1891 — P86); the fold damage of p. 136 (adhesive tape) — the father's cell beneath it; godparents Janez Dragoš + Katarina Toter (half smallholder) — the DRAGOS signal 7 (the godfather = the h12 father 1892–93); midwife Marjeta Toter; signature Jos. Ravq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1903,
    scan: 144,
    page: 136,
    whatSi: "krščena Marija (22./22. 1.) — oče Dragoš [ime pod trakom; ~ Janez — h12 1892/93 oče Janez Dragos ½ zemljak], ½ zemljašt., mati Barbara [rodčina pod trakom; ~ Držibovič?/Kržibomič?]; h12 = 8. VPIS (1892, 1894, 1895, 1897, 1899, 1901×2); DRAGOS signal 7 (1902/03 botra/boter Janez Dragoš ×2); botra Matija Špas [~] + Katarina Toter; babica Marjeta Toter; podpis Dostál [~]; marginalija: »† 22/1.03« [~] — dojenček (živel ~14 dni)",
    whatEn: "baptized Marija (Jan 22/22) — father Dragoš [the name under a strip; ~ Janez — the h12 1892/93 father Janez Dragos a half smallholder], a half smallholder's son, mother Barbara [the surname under a strip; ~ Držibovič?/Kržibomič?]; h12 = the 8th ENTRY (1892, 1894, 1895, 1897, 1899, 1901×2); the DRAGOS signal 7 (1902/03 the godparent Janez Dragoš ×2); godparents Matija Špas [~] + Katarina Toter; midwife Marjeta Toter; signature Dostál [~]; the marginalia: '† Jan 22, 1903' [~] — an infant (lived ~14 days)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1903,
    scan: 145,
    page: 137,
    whatSi: "krščen Jožef (8./9. 3.) — oče Matija Urh? [~ (branja »Uleh/Udih/Urh« — Kurrent)], ½ zemljak, mati Marjeta Perdinec; h32 = 8. VPIS (1889, 1890, 1892, 1893, 1895, 1897, 1898, 1900); botra Janez Požek + Marija Mih (½ zemljak); babica Marjeta Toter; podpis Jos. Ravq; pripis: † 6.10.1963 Novo mesto (MMK Novo mesto 2.1963, št. 702, joh. 1929), 13.10.1963; poročen 17.11.1930; maticar Vrabič? Plec? [~]",
    whatEn: "baptized Jožef (Mar 8/9) — father Matija Urh? [~ (the readings 'Uleh/Udih/Urh' — Kurrent)], a half smallholder, mother Marjeta Perdinec; h32 = the 8th ENTRY (1889, 1890, 1892, 1893, 1895, 1897, 1898, 1900); godparents Janez Požek + Marija Mih (half smallholder); midwife Marjeta Toter; signature Jos. Ravq; the note: † Oct 6, 1963 Novo mesto (MMK Novo mesto 2.1963, no. 702, ref. 1929), Oct 13, 1963; married Nov 17, 1930; the registrar Vrabič? Plec? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04105",
    year: 1903,
    scan: 146,
    page: 138,
    whatSi: "krščena Marija (1./1. 5.) — oče [ime pod trakom — brez berljivega dela], stan neberljiv, mati Ana Kušar? [~]; h35 = 4. VPIS (1887, 1889, 1890); botra Peter Švigan? [~ (½ zemljak)] + Ana Mir (bajtarica?); babica Marjeta Toter; podpis Jos. Ravq; pripis: † 10.5.1979 Griblje (MMK … l.1979, št. 14, 20.9., št. 2), Gradac 21.5.1979, maticar Šimec Nina [~]",
    whatEn: "baptized Marija (May 1/1) — the father [the name under a strip — no legible part], the status illegible, mother Ana Kušar? [~]; h35 = the 4th ENTRY (1887, 1889, 1890); godparents Peter Švigan? [~ (a half smallholder)] + Ana Mir (a cotteress?); midwife Marjeta Toter; signature Jos. Ravq; the note: † May 10, 1979 Griblje (MMK … 1979, no. 14, Sep 20, no. 2), Gradac May 21, 1979, the registrar Šimec Nina [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04105",
    year: 1903,
    scan: 147,
    page: 139,
    whatSi: "krščen Jaroslav? [~] (31./31. 7.) — oče [? Kerbanec/Herbanec [~ — ime pod razivom], ¼ zemljak, mati Ana Južna [~]; h23 = 5. VPIS (1893, 1894, 1897, 1900); botra Matija Novak (bajtar) + Barbara Južna (bajtarica); babica Alojzija Delak; podpis Jos. Ravq; pripis: † 18.09.1990 Šmarje? (AlJo … 1.1990, zop. št. 14), deleževalec 18.01.1991; poročen 14.11.1931; modri pripisi delno neberljivi (MMK … št. 1874 [~])",
    whatEn: "baptized Jaroslav? [~] (Jul 31/31) — the father [? Kerbanec/Herbanec [~ — the name under a wrinkle], a quarter smallholder, mother Ana Južna [~]; h23 = the 5th ENTRY (1893, 1894, 1897, 1900); godparents Matija Novak (a cotter) + Barbara Južna (a cotteress); midwife Alojzija Delak; signature Jos. Ravq; the note: † Sep 18, 1990 Šmarje? (AlJo … 1.1990, ref. 14), the heir Jan 18, 1991; married Nov 14, 1931; the blue notes partly illegible (MMK … no. 1874 [~])",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1903,
    scan: 147,
    page: 139,
    whatSi: "krščena Ana (2./3. 8.) — oče Nikolaj Uhr? [~ (ime pod razivom)], ½ zemljak, mati Marija Lehniyer? [~]; h63 = 7. VPIS (1887, 1889, 1890, 1892, 1896, 1898); botra Matija Jakljič? [~] + Ana Jakljič? [~ (½ zemljak)]; babica Ana Mavretič; podpis Dostál [~]; pripis: † 30.11.1972 Rake?/Ravna gora (MMK Rama gora? l.1972, št. 10), 14.12.1972; poročen 28.6.1975 [~ (ali 1935 — Kurrent 3/5)]",
    whatEn: "baptized Ana (Aug 2/3) — father Nikolaj Uhr? [~ (the name under a wrinkle)], a half smallholder, mother Marija Lehniyer? [~]; h63 = the 7th ENTRY (1887, 1889, 1890, 1892, 1896, 1898); godparents Matija Jakljič? [~] + Ana Jakljič? [~ (a half smallholder)]; midwife Ana Mavretič; signature Dostál [~]; the note: † Nov 30, 1972 Rake?/Ravna gora (MMK Rama gora? 1972, no. 10), Dec 14, 1972; married Jun 28, 1975 [~ (or 1935 — the Kurrent 3/5)]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1903,
    scan: 149,
    page: 140,
    whatSi: "krščena Katarina (13. [~ (delno pod pečatom)]/1. [~] 8.) — oče Nikolaj Žilak? [~], ½ zemljak?, mati Katarina Klobučar? [~]; h34 = 3. VPIS (1887, 1899); SEGINA signal 7 (boter Nikol Segina — isti kot h30 oče 1902 r16; HRIŽAN signal — botrinja Katarina Hrižan, ½ zemljak); babica Marija Mih; podpis Stanislav Dostál (jasno!); marginalija: nalepka »umrla dne 04.03.1991 v Ptuju. MKU NO Ptuj, kšt. 1991, nbr. 190, zop. št. 290. Matičar, nam. Adamič drug« [~] — † 24.9.03? [~ svinčnik tudi]",
    whatEn: "baptized Katarina (Aug 13 [~ (partly under the stamp)]/1 [~]) — father Nikolaj Žilak? [~], a half smallholder?, mother Katarina Klobučar? [~]; h34 = the 3rd ENTRY (1887, 1899); the SEGINA signal 7 (the godfather Nikol Segina — the same as the h30 father 1902 r16; the HRIŽAN signal — the godmother Katarina Hrižan, a half smallholder); midwife Marija Mih; the signature Stanislav Dostál (clear!); the marginalia: a slip 'she died Mar 4, 1991 in Ptuj. MKU NO Ptuj, 1991, no. 190, ref. 290. The registrar, named Adamič' [~] — † Sep 24, 1903? [~ a pencil note too]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1903,
    scan: 149,
    page: 140,
    whatSi: "krščena Neža (3./4. 10.) — oče Janez Požek ¾ zemljak, mati Katarina Kambič; h58 = 7. VPIS (1889, 1890, 1892, 1895, 1900, 1902); REŠITEV P97 MERI: 1902 r8 oče »Janez Povk? × Katarina Hambič?« = ISTI PAR kot 1903 »Janez Požek × Katarina Kambič« (Kurrent varianta — NI menjava družine); 1892 Požek × Dragos → menjava žene pred 1900 ostaja potrjena; botra Marko Hlebec + Marija Kambič (½ zemljak); babica Marjeta Toter; podpis Dostál",
    whatEn: "baptized Neža (Oct 3/4) — father Janez Požek a three-quarter smallholder, mother Katarina Kambič; h58 = the 7th ENTRY (1889, 1890, 1892, 1895, 1900, 1902); THE RESOLUTION OF THE P97 MERI: the 1902 r8 father 'Janez Povk? × Katarina Hambič?' = THE SAME COUPLE as the 1903 'Janez Požek × Katarina Kambič' (a Kurrent variant — NOT a family change); the 1892 Požek × Dragos → the wife change before 1900 remains confirmed; godparents Marko Hlebec + Marija Kambič (half smallholder); midwife Marjeta Toter; signature Dostál",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04105",
    year: 1903,
    scan: 150,
    page: 141,
    whatSi: "krščena Ana (20./21. 10.) — oče Peter Perdinec ¾ zemljak, mati Doroteja Klepec; h20 = 4. VPIS (1895, 1897, 1900); EMŠO Ž: 2010903505047 → 20.10.1903 (SIDRO; izdano 26.10.1982, Šumovič Nina); botra Matija Milek + Katarina Perdinec (½ zemljak); babica Katarina Perdinec; podpis Dostál; pripis: † 12.08.1995 Griblje? (MKU NO Črnomelj l.1995, št. 55), 08.03.2001 [~]; poročen 17.5.1931 [~]",
    whatEn: "baptized Ana (Oct 20/21) — father Peter Perdinec a three-quarter smallholder, mother Doroteja Klepec; h20 = the 4th ENTRY (1895, 1897, 1900); the personal ID: 2010903505047 → Oct 20, 1903 (AN ANCHOR; issued Oct 26, 1982, Šumovič Nina); godparents Matija Milek + Katarina Perdinec (half smallholder); midwife Katarina Perdinec; signature Dostál; the note: † Aug 12, 1995 Griblje? (MKU NO Črnomelj 1995, no. 55), Mar 8, 2001 [~]; married May 17, 1931 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1903,
    scan: 151,
    page: 142,
    whatSi: "krščen Alojzij (9./9. 12.) — oče Nikolaj Segina ½ zemljak, mati Katarina Brinec; h30 = 2. VPIS ZAPORED (1902 r16 + 1903 r76 — oče ISTI: Nikolaj Segina; MENJAVA ŽENE: Marjeta Milek (1902) → Katarina Brinec (1903) — MERI); SEGINA signal 8 (h30 + h34 v istem letu: r47 boter Nikol Segina); botra Matija Mitek? [~] + Marija Križan (½ zemljak); babica Marija Mih; podpis Jos. Ravq; pripis: † 3.3.1944 (modri pripis: »dne 3.3.1944 padel …« [~ — neberljivo]); poročen 16.7.1939",
    whatEn: "baptized Alojzij (Dec 9/9) — father Nikolaj Segina a half smallholder, mother Katarina Brinec; h30 = the 2nd CONSECUTIVE ENTRY (the 1902 r16 + the 1903 r76 — the father THE SAME: Nikolaj Segina; THE WIFE CHANGE: Marjeta Milek (1902) → Katarina Brinec (1903) — MERI); the SEGINA signal 8 (h30 + h34 in the same year: the r47 godfather Nikol Segina); godparents Matija Mitek? [~] + Marija Križan (half smallholder); midwife Marija Mih; signature Jos. Ravq; the note: † Mar 3, 1944 (the blue note: 'on Mar 3, 1944 fell …' [~ — illegible]); married Jul 16, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "83",
    bookSignature: "04105",
    year: 1903,
    scan: 151,
    page: 142,
    whatSi: "krščena Neža (25./26. 12.) — oče Jožef Željko [~ (ime/priimek obrnjen — branje »Željko Jožef«)], ½ zemljak?, mati Nina Gorše? [~]; h83 = 3. VPIS (1888, 1889) — LUKNJA 1890–1902 (13 let) zaplodana s 1903!; ŽELJKO signal 21 (boter Nikolaj Željko — 1903 botra Željko 4×: r27 Janez, r48 Nikol, r74 Janez, r81 Nikolaj = signali 18–21); botra Nikolaj + Marija Željko [~]; babica Marjeta Toter; podpis Dostál [~]",
    whatEn: "baptized Neža (Dec 25/26) — father Jožef Željko [~ (the name/surname reversed — the reading 'Željko Jožef')], a half smallholder?, mother Nina Gorše? [~]; h83 = the 3rd ENTRY (1888, 1889) — THE GAP 1890–1902 (13 years) filled with 1903!; the ŽELJKO signal 21 (the godfather Nikolaj Željko — in 1903 the Željko godparents 4×: r27 Janez, r48 Nikol, r74 Janez, r81 Nikolaj = the signals 18–21); godparents Nikolaj + Marija Željko [~]; midwife Marjeta Toter; signature Dostál [~]",
    status: "DOCUMENTED",
  },
  // ——— P99: krstna 1904 (04105, skeni 152–160 == str. 143–150; 90 vrstic;
  // dup par 155/156 = str. 146) — 20 vpisov / 19 hiš (+r69 hiša neberljiva,
  // brez bloka) NARE 10. leto; 3 NOVE HIŠE (h6 nabor, h42+h50 = 20./21.
  // dokazana luknja 41–60 — ostaja samo h51); h24 = 11. VPIS (rekord),
  // h16 = 6. VPIS (Straus × Spudič), h36 = 10. VPIS, h91 = MUC kontinuiteta;
  // SPUDIČ signal r78; MENJAVA KAPLANOV: Dostál »Kaplan« (jan) → Hugo
  // Hengsfeld (od r67, 13×); EMŠO kampanja 1982–84 (Šimonič Miri); 2
  // mrtvorojena (r41+r84 »Z.mrtvorajen«, krsta »—«); r19 vstavljen vpis
  // (excluded, EMŠO 2007); glava 1905 pod r90 = P100 lead. Dokaz:
  // research/issue17/parish-baptism-1904.json; verifikator:
  // scripts/p99_parish_baptism_1904.py --check (I1–I10).
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1904,
    scan: 152,
    page: 143,
    whatSi: "krščena Ana (8./8. 1.) — oče Nikolaj Milek ½ zemljak, mati Ana Žunič; h22 = 3. VPIS (1902, 1904); botra Janez Požek + Marjeta Žunič (POŽEK signal); babica Barbara Aleksič; podpis Stanislav Dostál, KAPLAN; † 8.7.1963 [~], poročena 31.3.1940",
    whatEn: "baptized Ana (Jan 8/8) — father Nikolaj Milek, a half smallholder, mother Ana Žunič; h22 = the 3rd ENTRY (1902, 1904); godparents Janez Požek + Marjeta Žunič (the POŽEK signal); midwife Barbara Aleksič; signature Stanislav Dostál, A CURATE (KAPLAN); † Jul 8, 1963 [~], married Mar 31, 1940",
    status: "DOCUMENTED",
  },
  {
    houseNo: "87",
    bookSignature: "04105",
    year: 1904,
    scan: 153,
    page: 144,
    whatSi: "krščen Alojzij (16./16. 2.) — oče Marko Podrinec bajtar [~], mati Katarina Zugelj; h87 = 3. VPIS (1895 Pegdirec/Perdinec?, 1902, 1904 — KURRENT ISTI oče, NI menjava); botra Nikolaj Žugelj? + Marija Hrižan?; babica Marija Mih [~]; podpis Stanislav Dostál; † 5.12.1942 Novo mesto, poročen 4.10.1933 [~]",
    whatEn: "baptized Alojzij (Feb 16/16) — father Marko Podrinec, a cottager [~], mother Katarina Zugelj; h87 = the 3rd ENTRY (1895 Pegdirec/Perdinec?, 1902, 1904 — the KURRENT father IS THE SAME, NO change); godparents Nikolaj Žugelj? + Marija Hrižan?; midwife Marija Mih [~]; signature Stanislav Dostál; † Dec 5, 1942 Novo mesto, married Oct 4, 1933 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04105",
    year: 1904,
    scan: 153,
    page: 144,
    whatSi: "krščenec [ime neberljivo pod lisom] (18./18. 2.) — oče Janez Jaklič ½ zemljak, mati Marija Brinec? (BRINEC signal); h15 = 8. VPIS (…1896, 1904); botra Matija Jaklič bajtar + Barbara Adamič goličarica?; babica Marjeta Toter; podpis Stanislav Dostál; † 9.2.1973, poročen 1928 [~]",
    whatEn: "baptized a boy [the name illegible under a stain] (Feb 18/18) — father Janez Jaklič, a half smallholder, mother Marija Brinec? (the BRINEC signal); h15 = the 8th ENTRY (…1896, 1904); godparents Matija Jaklič, a cottager + Barbara Adamič, a goličarica? (a landless woman); midwife Marjeta Toter; signature Stanislav Dostál; † Feb 9, 1973, married 1928 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1904,
    scan: 153,
    page: 144,
    whatSi: "krščena Jožefa (19./19. 2.) — oče Peter Brinec? bajtar [~ pod trakom], mati Alma Šecalja? [~]; h88 = PRVI KRSTNI VPIS (hiša že v mrliški 04894/1886); botra Janez Brinec? + Marija Grabrijan? (BRINEC signal; pod trakom); babica [pod trakom — neberljivo]; podpis Stanislav Dostál [~]; † 18.11.1965, poročena 30.10.1932",
    whatEn: "baptized Jožefa (Feb 19/19) — father Peter Brinec?, a cottager [~ under a strip], mother Alma Šecalja? [~]; h88 = THE FIRST BAPTISM ENTRY (the house already in the death register 04894/1886); godparents Janez Brinec? + Marija Grabrijan? (the BRINEC signal; under a strip); midwife [under a strip — illegible]; signature Stanislav Dostál [~]; † Nov 18, 1965, married Oct 30, 1932",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1904,
    scan: 153,
    page: 144,
    whatSi: "krščena Alojzija (29./29. 2. — PRESTOPNI dan) — oče Martin Jurajevič bajtar, mati Marijana Krašovec; h24 = 11. VPIS (1887–1903; ŠE VEDNO najbolj vpisovana hiša registra); botra Danijel Murn?/Muen? Bogovec + Ana Kambič (isti boter kot 1903 r1); babica Ana Mavretič; podpis Stanislav Dostál; pripis razveljavitve zakona 1947/48; † 30.1.1983 Zagreb [~]",
    whatEn: "baptized Alojzija (Feb 29/29 — THE LEAP day) — father Martin Jurajevič, a cottager, mother Marijana Krašovec; h24 = the 11th ENTRY (1887–1903; STILL the most-entered house of the register); godparents Danijel Murn?/Muen?, from Bogovo + Ana Kambič (the same godfather as 1903 r1); midwife Ana Mavretič; signature Stanislav Dostál; a note on the ANNULMENT of the marriage 1947/48; † Jan 30, 1983 Zagreb [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04105",
    year: 1904,
    scan: 154,
    page: 145,
    whatSi: "krščen Anton (12./13. 5.) — oče Jurij Župančič? ½ zemljak, mati Ana Vardjan? [~]; h54 = 5. VPIS (1886, 1897, 1900, 1901, 1904); botra Janez Župančič? + Marija Vrščaj?; babica Ana Mavretič; podpis Jos. Ravq [~]; † 28.4.1971, poročen 15.11.1931",
    whatEn: "baptized Anton (May 12/13) — father Jurij Župančič?, a half smallholder, mother Ana Vardjan? [~]; h54 = the 5th ENTRY (1886, 1897, 1900, 1901, 1904); godparents Janez Župančič? + Marija Vrščaj?; midwife Ana Mavretič; signature Jos. Ravq [~]; † Apr 28, 1971, married Nov 15, 1931",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1904,
    scan: 154,
    page: 145,
    whatSi: "krščen Alojzij (16./16. 5.) — oče Anton Ivec?/Ivc ½ zemljak, mati Marija Kočevar; h16 = 6. VPIS (1886×2, 1897, 1902 STRAUS × SPUDIČ, 1904) — Strausova/Spudičeva hiša, poročna 04455 lead ostaja; botra Julij + Jožepina Maxelle foršnjarka?; babica Ana Mavretič; podpis Stanislav Dostál",
    whatEn: "baptized Alojzij (May 16/16) — father Anton Ivec?/Ivc, a half smallholder, mother Marija Kočevar; h16 = the 6th ENTRY (1886 ×2, 1897, 1902 STRAUS × SPUDIČ, 1904) — the Straus/Spudič house, the marriage-register 04455 lead remains; godparents Julij + Jožepina Maxelle, a foršnjarka?; midwife Ana Mavretič; signature Stanislav Dostál",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1904,
    scan: 154,
    page: 145,
    whatSi: "krščena Barbara (16./16. 5.) — oče Alojz Novak bajtar, mati Marija Frlah? [~]; h60 = 6. VPIS (…1899, 1904); botra Jurij Jakobič? + Ana Muc bajtarica; babica Marija Mih [~]; podpis Stanislav Dostál; † 14.2.1929/30 [~]",
    whatEn: "baptized Barbara (May 16/16) — father Alojz Novak, a cottager, mother Marija Frlah? [~]; h60 = the 6th ENTRY (…1899, 1904); godparents Jurij Jakobič? + Ana Muc, a cottager woman; midwife Marija Mih [~]; signature Stanislav Dostál; † Feb 14, 1929/30 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1904,
    scan: 156,
    page: 146,
    whatSi: "krščena Jožefa (9./9. 6.) — oče Rudolf Miše bajtar, mati Frančiška Adamič; h36 = 10. VPIS (…1902, 1904); botra Jožef Haškovič? + Ana Sika?; babica Alojzija Delak; podpis Jos. Ravq [~]; † 29.8.1943, poročena 25.2.1929",
    whatEn: "baptized Jožefa (Jun 9/9) — father Rudolf Miše, a cottager, mother Frančiška Adamič; h36 = the 10th ENTRY (…1902, 1904); godparents Jožef Haškovič? + Ana Sika?; midwife Alojzija Delak; signature Jos. Ravq [~]; † Aug 29, 1943, married Feb 25, 1929",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1904,
    scan: 156,
    page: 146,
    whatSi: "krščena Marija (10./10. 7.) — oče Jurij Jakobič? ½ zemljak, mati Katarina Jakobič; NOVA HIŠA h6 — prvi vpis (nabor PT 1–40); botra Nikol Željko + Marija Klepec (ŽELJKO signal); babica Marjeta Toter; podpis Stanislav Dostál; † 10.11.1918 [~ ali 1915]",
    whatEn: "baptized Marija (Jul 10/10) — father Jurij Jakobič?, a half smallholder, mother Katarina Jakobič; THE NEW HOUSE h6 — the first entry (in the PT set 1–40); godparents Nikol Željko + Marija Klepec (the ŽELJKO signal); midwife Marjeta Toter; signature Stanislav Dostál; † Nov 10, 1918 [~ or 1915]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "66",
    bookSignature: "04105",
    year: 1904,
    scan: 157,
    page: 147,
    whatSi: "krščen Janez (17./17. 7.) — oče Jakob Bohte ½ zemljak, mati Katarina Hrižan? [~]; h66 = 2. VPIS (1887, 1904); botra Nikol Brodarič? + Marija Škral?; babica Marjeta Toter; podpis Stanislav Dostál; † 4.5.1946",
    whatEn: "baptized Janez (Jul 17/17) — father Jakob Bohte, a half smallholder, mother Katarina Hrižan? [~]; h66 = the 2nd ENTRY (1887, 1904); godparents Nikol Brodarič? + Marija Škral?; midwife Marjeta Toter; signature Stanislav Dostál; † May 4, 1946",
    status: "DOCUMENTED",
  },
  {
    houseNo: "43",
    bookSignature: "04105",
    year: 1904,
    scan: 157,
    page: 147,
    whatSi: "krščena Katarina (17./17. 8.) — oče Jurij Perdinec ½ zemljak, mati Katarina Boršnec? [~]; h43 = 2. VPIS (1897 nezakonski, 1904); botra Nikol Brodarič? + Ana Jakljevič?; babica Marjeta Toter; podpis Jos. Ravq [~]; † 11.9.1904? [~ — dojenček]",
    whatEn: "baptized Katarina (Aug 17/17) — father Jurij Perdinec, a half smallholder, mother Katarina Boršnec? [~]; h43 = the 2nd ENTRY (1897 illegitimate, 1904); godparents Nikol Brodarič? + Ana Jakljevič?; midwife Marjeta Toter; signature Jos. Ravq [~]; † Sep 11, 1904? [~ — an infant]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1904,
    scan: 157,
    page: 147,
    whatSi: "krščena Amalija (21./21. 8.) — oče Nikolaj Cindrič čevljar [~], mati Marija Mavar [~]; h21 = 5. VPIS (…1899, 1904; PT MOGOČA Šture Majzel); botra Matija Milek + Marjeta Požek (MILEK + POŽEK signal); babica Marija Mih; podpis Jos. Ravq [~]; † 1.8.1906? [~]",
    whatEn: "baptized Amalija (Aug 21/21) — father Nikolaj Cindrič, a shoemaker [~], mother Marija Mavar [~]; h21 = the 5th ENTRY (…1899, 1904; the PT POSSIBLE Šture Majzel); godparents Matija Milek + Marjeta Požek (the MILEK + POŽEK signals); midwife Marija Mih; signature Jos. Ravq [~]; † Aug 1, 1906? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "50",
    bookSignature: "04105",
    year: 1904,
    scan: 158,
    page: 148,
    whatSi: "krščena Franciška (3./4. 9.) — oče Janez Jercinovič? ½ zemljak, mati Doroteja Štrucelj (ŠTRUCELJ signal — h22 1902); NOVA HIŠA h50 = 21. dokazana številka luknje 41–60 (PT_GAP_KNOWN += 50); botra Matija Pozdirec [~] + Katarina Hrižan?; babica Marjeta Toter; podpis Stanislav Dostál; † 10.1.1960 Griblje",
    whatEn: "baptized Franciška (Sep 3/4) — father Janez Jercinovič?, a half smallholder, mother Doroteja Štrucelj (the ŠTRUCELJ signal — the h22 family 1902); THE NEW HOUSE h50 = the 21st proven number of the gap 41–60 (PT_GAP_KNOWN += 50); godparents Matija Pozdirec [~] + Katarina Hrižan?; midwife Marjeta Toter; signature Stanislav Dostál; † Jan 10, 1960 Griblje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1904,
    scan: 159,
    page: 149,
    whatSi: "krščena Marija (20./21. 10.) — oče Matija Milek ½ zemljak (MILEK signal), mati Marija Hrišič? [~]; h65 = 8. VPIS (…1901 EV-only, 1904); botra Peter + Doroteja Pozdirec; babica Marjeta Toter; podpis Jos. Ravq [~]; † 4.9.1905 — dojenčka",
    whatEn: "baptized Marija (Oct 20/21) — father Matija Milek, a half smallholder (the MILEK signal), mother Marija Hrišič? [~]; h65 = the 8th ENTRY (…1901 EV-only, 1904); godparents Peter + Doroteja Pozdirec; midwife Marjeta Toter; signature Jos. Ravq [~]; † Sep 4, 1905 — an infant girl",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1904,
    scan: 159,
    page: 149,
    whatSi: "krščena Katarina (26./27. 10.) — oče Martin Škrac bajtar, mati Barbara SPUDIČ (SPUDIČ signal — poročna 04455 lead; h16 Strausova hiša 6. VPIS istega leta); h45 = 4. VPIS (1896, …, 1904); EMŠO 2610904505164 = 26.10.1904; botra Matija + Marija Mih; babica Marjeta Toter; podpis Jos. Ravq [~]; † 14.10.2003 Metlika (98 let — najdaljše življenje 1904)",
    whatEn: "baptized Katarina (Oct 26/27) — father Martin Škrac, a cottager, mother Barbara SPUDIČ (the SPUDIČ signal — the marriage-register 04455 lead; the Straus house h16 the 6th ENTRY the same year); h45 = the 4th ENTRY (1896, …, 1904); the personal ID 2610904505164 = Oct 26, 1904; godparents Matija + Marija Mih; midwife Marjeta Toter; signature Jos. Ravq [~]; † Oct 14, 2003 Metlika (98 years — the longest life of 1904)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04105",
    year: 1904,
    scan: 159,
    page: 149,
    whatSi: "krščen Frančišek (3./4. 11.) — oče Janez Muc bajtar, mati Ana Kure; h91 = 4. VPIS (1895 MUC!, 1902 Murov? [~], 1904) — MUC KONTINUITETA potrjena; botra Jurij Jakofčič? + Ana Šimec?; babica Marjeta Toter; podpis Hugo Hengsfeld; † 18.4.1979 Novo mesto",
    whatEn: "baptized Frančišek (Nov 3/4) — father Janez Muc, a cottager, mother Ana Kure; h91 = the 4th ENTRY (1895 MUC!, 1902 Murov? [~], 1904) — the MUC CONTINUITY proven; godparents Jurij Jakofčič? + Ana Šimec?; midwife Marjeta Toter; signature Hugo Hengsfeld; † Apr 18, 1979 Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1904,
    scan: 159,
    page: 149,
    whatSi: "krščen Nikolaj (9./9. 11.) — oče Janez Željko bajtar (ŽELJKO signal), mati Marjeta Žumič [~]; h69 = 8. VPIS (…1898, 1904); botra Janez Adamič + Barbara Željko; babica Marjeta Toter; podpis Jos. Ravq [~]",
    whatEn: "baptized Nikolaj (Nov 9/9) — father Janez Željko, a cottager (the ŽELJKO signal), mother Marjeta Žumič [~]; h69 = the 8th ENTRY (…1898, 1904); godparents Janez Adamič + Barbara Željko; midwife Marjeta Toter; signature Jos. Ravq [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "42",
    bookSignature: "04105",
    year: 1904,
    scan: 160,
    page: 150,
    whatSi: "krščen Jožef (29./29. 12.) — oče Matija Štraus? ½ zemljak (ŠTRAUS signal — 2. Strausova oseba 1904), mati Marjeta Šimec [~]; NOVA HIŠA h42 = 20. dokazana številka luknja 41–60 (PT_GAP_KNOWN += 42) — zadnja vrstica 1904, glava 1905 pod r90; botra Jožef Štrucelj? + Barb. Jakobič? (pod trakom); babica Marjeta Toter; podpis [neberljivo — izbledelo/pod trakom]",
    whatEn: "baptized Jožef (Dec 29/29) — father Matija Štraus?, a half smallholder (the ŠTRAUS signal — the 2nd Straus person of 1904), mother Marjeta Šimec [~]; THE NEW HOUSE h42 = the 20th proven number of the gap 41–60 (PT_GAP_KNOWN += 42) — the last row of 1904, the 1905 heading below r90; godparents Jožef Štrucelj? + Barb. Jakobič? (under a strip); midwife Marjeta Toter; signature [illegible — faded/under a strip]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1905,
    scan: 161,
    page: 151,
    whatSi: "krščena Neža (12./12. 1.) — oče Janez Dragoš [~] ½ zemljak (isti kot 1892–1899), mati Barbara Cvitkovič [~]; h12 = 9. VPIS; RAZVELJAVITEV ZAKONA (sodišče Novo mesto 23.5.1949 — 1. gribeljska!); botra Marija Štrucelj + Katarina Toter; babica Marjeta Toter; podpis Jos. Ravq; EMŠO ž 1201905505202 (sidro); umrla 11.1.1984 Novo mesto",
    whatEn: "baptized Neža (Jan 12/12) — father Janez Dragoš [~] half smallholder (the same as 1892–1899), mother Barbara Cvitkovič [~]; h12 = the 9th ENTRY; MARRIAGE ANNULLED (the Novo mesto court May 23, 1949 — the 1st Griblje annulment!); godparents Marija Štrucelj + Katarina Toter; midwife Marjeta Toter; signature Jos. Ravq; EMŠO 1201905505202 (an anchor); died Jan 11, 1984 Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1905,
    scan: 161,
    page: 151,
    whatSi: "krščena Ana (3./4. 2.) — oče Matija? Štrucelj [~ — 1903 isti oče], mati Marija Muh [~ — 1903 »Mehle?«]; h5 = 3. VPIS (vrzel 1 leto); botra Janez Dragoš? + Katarina Toter? [~ pod folijo]; babica Marjeta Toter; podpis H. Hengsfeld; EMŠO ž 0302905505218; umrla 7.5.1933 Griblje",
    whatEn: "baptized Ana (Feb 3/4) — father Matija? Štrucelj [~ — the 1903 same father], mother Marija Muh [~ — 1903 »Mehle?«]; h5 = the 3rd ENTRY (a 1-year gap); godparents Janez Dragoš? + Katarina Toter? [~ under film]; midwife Marjeta Toter; signature H. Hengsfeld; EMŠO 0302905505218; died May 7, 1933 Griblje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1905,
    scan: 161,
    page: 151,
    whatSi: "krščena Ana (10./16.? 2. [~]) — oče Matija? Štraus/Šimec? [~ pod folijo; 1901 h12 2. družina = Matija Straus], mati Ana [neberljiva]; h12 = 10. VPIS — NARE PRELOM (h12 ×2 v 1905, 2. primer po 1901 — več-družinska hiša); botra Janez Muc + Katarina Hrižan, kovač; babica Marjeta Toter? [~]; podpis odrezan",
    whatEn: "baptized Ana (Feb 10/16.? [~]) — father Matija? Štraus/Šimec? [~ under film; the 1901 h12 2nd family = Matija Straus], mother Ana [illegible]; h12 = the 10th ENTRY — the NARE BREAK (h12 twice in 1905, the 2nd case after 1901 — a multi-family house); godparents Janez Muc + Katarina Hrižan, a blacksmith; midwife Marjeta Toter? [~]; signature cut off",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1905,
    scan: 162,
    page: 152,
    whatSi: "krščena Ana (1./2. 3.) — oče Nikolaj Šulak? [~] ½ zemljak, mati Katarina Klobučar; h34 = 4. VPIS; botra Nikolaj Šegina + Katarina Hrižan (SEGINA signal + HRIŽAN); babica Mih [~ Muh] Marija; podpis H. Hengsfeld; EMŠO ž 0103905505058 (sidro); umrla 11.3.1933 Griblje",
    whatEn: "baptized Ana (Mar 1/2) — father Nikolaj Šulak? [~] half smallholder, mother Katarina Klobučar; h34 = the 4th ENTRY; godparents Nikolaj Šegina + Katarina Hrižan (the SEGINA signal + HRIŽAN); midwife Mih [~ Muh] Marija; signature H. Hengsfeld; EMŠO 0103905505058 (an anchor); died Mar 11, 1933 Griblje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "39",
    bookSignature: "04105",
    year: 1905,
    scan: 163,
    page: 153,
    whatSi: "krščena Jožefa (13./14. 4.) — oče Jurij Šimec [~] ½ zemljak, mati Ana Šimec; h39 = 2. VPIS — VRZEL 18 LET (1886→1905, najdaljša v vzorcu!); botra Jakob Toter + Marija Štraus; babica Marjeta Toter; podpis Jos. Ravq; umrla 19.5.1963 Griblje",
    whatEn: "baptized Jožefa (Apr 13/14) — father Jurij Šimec [~] half smallholder, mother Ana Šimec; h39 = the 2nd ENTRY — an 18-YEAR GAP (1886→1905, the longest in the sample!); godparents Jakob Toter + Marija Štraus; midwife Marjeta Toter; signature Jos. Ravq; died May 19, 1963 Griblje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "42",
    bookSignature: "04105",
    year: 1905,
    scan: 163,
    page: 153,
    whatSi: "krščen Anton (19./19. 4.) — oče Jurij Perdinec? [~ Pezdirec] ¼ zemljak, mati Katarina Jurajevič? [~]; h42 = 2. VPIS + MENJAVA DRUŽINE (1904 Štraus → 1905 Perdinec/Pezdirec — nova družina že naslednje leto!); botra Marija Muh + Katarina? Pezdirec?; babica Marjeta Toter; podpis H. Hengsfeld",
    whatEn: "baptized Anton (Apr 19/19) — father Jurij Perdinec? [~ Pezdirec] quarter smallholder, mother Katarina Jurajevič? [~]; h42 = the 2nd ENTRY + a FAMILY CHANGE (1904 Štraus → 1905 Perdinec/Pezdirec — a new family the very next year!); godparents Marija Muh + Katarina? Pezdirec?; midwife Marjeta Toter; signature H. Hengsfeld",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04105",
    year: 1905,
    scan: 163,
    page: 153,
    whatSi: "krščena Marija (13./14. 5.) — oče Janez Žumě? [~ Žunič] ¼ zemljak, mati Marija Jakofčič? [~]; h11 = 3. VPIS — VRZEL 15 LET (1890→1905); botra Janez Albreič? + Neža Albreič? [~]; babica Marjeta Toter; podpis H. Hengsfeld",
    whatEn: "baptized Marija (May 13/14) — father Janez Žumě? [~ Žunič] quarter smallholder, mother Marija Jakofčič? [~]; h11 = the 3rd ENTRY — a 15-YEAR GAP (1890→1905); godparents Janez Albreič? + Neža Albreič? [~]; midwife Marjeta Toter; signature H. Hengsfeld",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04105",
    year: 1905,
    scan: 164,
    page: 154,
    whatSi: "krščen Alojzij (17./18. 6.) — oče Matija Brinec [~] ½ zemljak (isti oče-priimek kot r66 h25!), mati Marija Deblič? [~]; h23 = 6. VPIS; botra Janez Jakljič? + Katarina Deblič? [~]; babica Mih Marija; podpis Jos. Ravq",
    whatEn: "baptized Alojzij (Jun 17/18) — father Matija Brinec [~] half smallholder (the same father-surname as r66 h25!), mother Marija Deblič? [~]; h23 = the 6th ENTRY; godparents Janez Jakljič? + Katarina Deblič? [~]; midwife Mih Marija; signature Jos. Ravq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1905,
    scan: 164,
    page: 154,
    whatSi: "krščen Janez (5.?/6. 7. — EMŠO 6.7.) — oče Jurij Jakobič/Jakobčič [~] ½ zemljak (ISTI kot 1904), mati Katarina Jakobič/Jakobčič; h6 = 2. VPIS ZAPORED (ista starša + ISTA botra Nikolaj Željko + Marija Klepec kot 1904!); babica Marjeta Toter; podpis H. Hengsfeld; vijolični pripis »Po odloči Okrajnega sodišča v Črnomelju«; EMŠO ž 0607905500076 (neskladje spola!); umrl 20.10.1970 Griblje",
    whatEn: "baptized Janez (Jul 5.?/6 — EMŠO Jul 6) — father Jurij Jakobič/Jakobčič [~] half smallholder (the same as 1904), mother Katarina Jakobič/Jakobčič; h6 = the 2nd CONSECUTIVE ENTRY (the same parents + the SAME godparents Nikolaj Željko + Marija Klepec as 1904!); midwife Marjeta Toter; signature H. Hengsfeld; the violet note »By the decision of the Okrajno sodišče in Črnomelj«; EMŠO 0607905500076 (a sex mismatch!); died Oct 20, 1970 Griblje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04105",
    year: 1905,
    scan: 164,
    page: 154,
    whatSi: "krščen Janez (6./6. 7.) — oče Jakob Toter ¼ zemljak (ISTI par kot 1901 h7), mati Katarina Jakobšič; h7 = 3. VPIS (vrzel 3 leta); botra Marija Štrucelj + Barbara Dragoš? [~]; babica Marjeta Toter (očetova družina); podpis H. Hengsfeld; umrl 2.2.1967",
    whatEn: "baptized Janez (Jul 6/6) — father Jakob Toter quarter smallholder (the same couple as the 1901 h7), mother Katarina Jakobšič; h7 = the 3rd ENTRY (a 3-year gap); godparents Marija Štrucelj + Barbara Dragoš? [~]; midwife Marjeta Toter (the father's family); signature H. Hengsfeld; died Feb 2, 1967",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1905,
    scan: 166,
    page: 155,
    whatSi: "krščena Ana (21./21. 8.) — oče Jurij Pezdirec [~] ¼ zemljak, mati Katarina Berkovec [~]; h48 = 2. VPIS — VRZEL 7 LET (1898→1905; h48 = dokumentirana številka luknje 41–60); botra Nikol Brodarič + Dorotea? Pezdirec? [~]; babica Mih Marija; podpis Jos. Ravq; umrla 20.12.1975 Trbovlje",
    whatEn: "baptized Ana (Aug 21/21) — father Jurij Pezdirec [~] quarter smallholder, mother Katarina Berkovec [~]; h48 = the 2nd ENTRY — a 7-YEAR GAP (1898→1905; h48 = a proven number of the gap 41–60); godparents Nikol Brodarič + Dorotea? Pezdirec? [~]; midwife Mih Marija; signature Jos. Ravq; died Dec 20, 1975 Trbovlje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1905,
    scan: 166,
    page: 155,
    whatSi: "krščen Mihael (16./16. 9.) — oče Nikolaj Milek ¼ zemljak (ISTI kot 1904 h22), mati Ana [priimek pod modrim pripisom — ~ Žunič]; h22 = 4. VPIS (2. zapored); botra Nikolaj Križan + Ana Požek (POŽEK signal); babica Marjeta Toter; podpis H. Hengsfeld; umrl 27.11.1975 Novo mesto; žena Ana Milek † 19.3.1982 Griblje",
    whatEn: "baptized Mihael (Sep 16/16) — father Nikolaj Milek quarter smallholder (the same as the 1904 h22), mother Ana [the surname under a blue note — ~ Žunič]; h22 = the 4th ENTRY (the 2nd consecutive); godparents Nikolaj Križan + Ana Požek (the POŽEK signal); midwife Marjeta Toter; signature H. Hengsfeld; died Nov 27, 1975 Novo mesto; the wife Ana Milek † Mar 19, 1982 Griblje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1905,
    scan: 167,
    page: 156,
    whatSi: "krščena Katarina (24./24. 9.) — oče Jurij Željko? [~] ¼ zemljak (ŽELJKO signal), mati Barbara Kure? [~]; h1 = 6. VPIS (vrzel 4 leta od 1900); botra Jakob Toter + Barbara Nukan? [~]; babica Marjeta Toter; podpis Jos. Ravq; † 20.12.1931? [~]",
    whatEn: "baptized Katarina (Sep 24/24) — father Jurij Željko? [~] quarter smallholder (the ŽELJKO signal), mother Barbara Kure? [~]; h1 = the 6th ENTRY (a 4-year gap from 1900); godparents Jakob Toter + Barbara Nukan? [~]; midwife Marjeta Toter; signature Jos. Ravq; † Dec 20, 1931? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "25",
    bookSignature: "04105",
    year: 1905,
    scan: 167,
    page: 156,
    whatSi: "krščen Matija (1./2. 10.) — oče Matija Brinec ¼ zemljak, mati Katarina Šegina (ISTI PAR kot h25 1900+1902 — SEGINA signal); h25 = 5. VPIS (3. dokumentacija para Brinec × Šegina); botra Danijel Šegina + Katarina Šegina; babica Marjeta Toter; podpis Jos. Ravq; † 17/11.1905? dojenček [~]",
    whatEn: "baptized Matija (Oct 1/2) — father Matija Brinec quarter smallholder, mother Katarina Šegina (the SAME couple as h25 1900+1902 — the SEGINA signal); h25 = the 5th ENTRY (the 3rd documentation of the Brinec × Šegina couple); godparents Danijel Šegina + Katarina Šegina; midwife Marjeta Toter; signature Jos. Ravq; † Nov 17, 1905? an infant [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "58",
    bookSignature: "04105",
    year: 1905,
    scan: 167,
    page: 156,
    whatSi: "krščen Matija (23./23. 10.) — oče Janez Požek ¼ zemljak, mati Katarina Kambič (ISTI PAR kot h58 1902+1903 — P98 rešitev 3.Potrjena!); h58 = 8. VPIS; botra Marko Hlebec? + Marija Šimec? [~]; babica Ana Kambič? [~]; podpis Jos. Ravq; † 26.2.1906 dojenček",
    whatEn: "baptized Matija (Oct 23/23) — father Janez Požek quarter smallholder, mother Katarina Kambič (the SAME couple as h58 1902+1903 — the P98 resolution confirmed the 3rd time!); h58 = the 8th ENTRY; godparents Marko Hlebec? + Marija Šimec? [~]; midwife Ana Kambič? [~]; signature Jos. Ravq; † Feb 26, 1906 an infant",
    status: "DOCUMENTED",
  },
  {
    houseNo: "66",
    bookSignature: "04105",
    year: 1905,
    scan: 168,
    page: 157,
    whatSi: "krščen Jakob (9./10. 12.) — oče Jakob Bohle? [~ Boble] ½ zemljak, mati Katarina Hrižan? [~] (HRIŽAN signal); h66 = 3. VPIS (2. zapored; prej vrzel 17 let 1887→1904); botra Nikol Brodarič + Marija Štraus; babica Marjeta Toter; podpis H. Hengsfeld; poročen 17.5.1931?; umrl 7.3.1944 (2. svetovna vojna)",
    whatEn: "baptized Jakob (Dec 9/10) — father Jakob Bohle? [~ Boble] half smallholder, mother Katarina Hrižan? [~] (the HRIŽAN signal); h66 = the 3rd ENTRY (the 2nd consecutive; previously a 17-year gap 1887→1904); godparents Nikol Brodarič + Marija Štraus; midwife Marjeta Toter; signature H. Hengsfeld; married May 17, 1931?; died Mar 7, 1944 (WWII)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1906,
    scan: 170,
    page: 158,
    whatSi: "krščen Leopold (21./22. 1.) — oče Mihael Jakofčič ½ zemljak (NOVA DRUŽINA na h16), mati Marija Mihelič [~]; h16 = 7. VPIS (1886, 1897, 1900, 1902 STRAUS×SPUDIČ, 1904 → 1906); botra Jožef Dragoš + Marija Jakofčič ¾ zemlj; babica Marija Mihelič [~ Mih? — mati in babica isti zapis]; podpis Jos. Ravq; svinčnik: Umrl 16. II. 1944 (2. svetovna vojna)",
    whatEn: "baptized Leopold (Jan 21/22) — father Mihael Jakofčič half smallholder (A NEW FAMILY at h16), mother Marija Mihelič [~]; h16 = the 7th ENTRY (1886, 1897, 1900, 1902 STRAUS×SPUDIČ, 1904 → 1906); godparents Jožef Dragoš + Marija Jakofčič; midwife Marija Mihelič [~ Mih? — the mother and the midwife share the record]; signature Jos. Ravq; pencil: died Feb 16, 1944 (WWII)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "49",
    bookSignature: "04105",
    year: 1906,
    scan: 172,
    page: 159,
    whatSi: "krščen Jožef (24./25. 2.) — oče Nikolaj Brodarič ½ zemljak, mati Marija Miheč [~]; h49 = 2. VPIS (1899 Brodarič × Milek → 1906 — MENJAVA ŽENE [MERI]); botra Nikolaj Željko [~ Želko] + Katarina Pendijeva [~] ½ zemlj — BRODARIČ↔ŽELJKO izmena (r16 boter Željko + r19 boter Brodarič); babica Marija Mih; podpis Hugo Hengsfeld; EMŠO m 2102906500234 (sidro); poročen 12.2.1937 v Beogradom(?)",
    whatEn: "baptized Jožef (Feb 24/25) — father Nikolaj Brodarič half smallholder, mother Marija Miheč [~]; h49 = the 2nd ENTRY (1899 Brodarič × Milek → 1906 — A WIFE CHANGE [MERI]); godparents Nikolaj Željko [~ Želko] + Katarina Pendijeva [~] — the BRODARIČ↔ŽELJKO exchange (r16 godfather Željko + r19 godfather Brodarič); midwife Marija Mih; signature Hugo Hengsfeld; EMŠO 2102906500234 (an anchor); married Feb 12, 1937 in Beograd(?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1906,
    scan: 172,
    page: 159,
    whatSi: "krščen Nikolaj (27./28. 2.) — oče Janez Simec ½ zemljak (POVRAT ŠIMCEve hiše — 1887 Šimec × Šmucelj → 1899–1905 Šilak/Šulak × Klobučar → 1906 Šimec, druga žena [MERI]), mati Marija Kere [~ Kerec?]; h34 = 5. VPIS — MENJAVA DRUŽINE 2×; botra Janez Fožič [~ Božič?] + Marija Mih ½ zemlj; babica Marija Mih; podpis Jos. Ravq; svinčnik + 1.7.1942; poročen 5.5.1933(?)",
    whatEn: "baptized Nikolaj (Feb 27/28) — father Janez Simec half smallholder (the ŠIMEC HOUSE RETURNS — 1887 Šimec × Šmucelj → 1899–1905 Šilak/Šulak × Klobučar → 1906 Šimec, a second wife [MERI]), mother Marija Kere [~ Kerec?]; h34 = the 5th ENTRY — a DOUBLE FAMILY CHANGE; godparents Janez Fožič [~ Božič?] + Marija Mih; midwife Marija Mih; signature Jos. Ravq; pencil + Jul 1, 1942; married May 5, 1933(?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1906,
    scan: 172,
    page: 159,
    whatSi: "krščena Jožefa (27./28. 2. — pod trakom) — oče Nikolaj Željko ½ zemljak, mati Marija Brodarič; h60 = 7. VPIS — PAR Željko × Brodarič POVRAT po 1904 intermezzu (5. OTROK istega para: 1893+1894+1897+1899 → 1906); botra Nikol. Brodarič + Marija Klepec ½ zemlj (botrinja = 3. ista Klepec para!); babica Marija Mih; podpis Jos. Ravq; umrla 17.5.1974 v Prilogju(?); z dvorim(?) 7.11.1932, poleg poročena 28.3.1947",
    whatEn: "baptized Jožefa (Feb 27/28 — under a film) — father Nikolaj Željko half smallholder, mother Marija Brodarič; h60 = the 7th ENTRY — the ŽELJKO × BRODARIČ COUPLE RETURNS after the 1904 intermezzo (the 5th CHILD of the same couple: 1893+1894+1897+1899 → 1906); godparents Nikol. Brodarič + Marija Klepec (the godmother = the 3rd same Klepec of the couple!); midwife Marija Mih; signature Jos. Ravq; died May 17, 1974 in Priloge(?); married Nov 7, 1932(?), also married Mar 28, 1947",
    status: "DOCUMENTED",
  },
  {
    houseNo: "19",
    bookSignature: "04105",
    year: 1906,
    scan: 173,
    page: 160,
    whatSi: "krščen Janez (10./11. 4.) — oče PRAZNO — NEZAKONSKI (edini gibriljski v letu), mati Ana Kovač [~] samostojna, (dela?) ¼ zemlja, krava hir? [~]; h19 = 2. VPIS (1901 Katarina — prvi dokaz); botra Alojzij Novak + Ana Simec, bajfarja; babica Marjeta Vötter [~]; podpis Hugo Hengsfeld",
    whatEn: "baptized Janez (Apr 10/11) — father EMPTY — ILLEGITIMATE (the only Griblje one in the year), mother Ana Kovač [~] unmarried, (a hired?) quarter farmland, cow hire? [~]; h19 = the 2nd ENTRY (1901 Katarina — the first proof); godparents Alojzij Novak + Ana Simec, cotter couple; midwife Marjeta Vötter [~]; signature Hugo Hengsfeld",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1906,
    scan: 174,
    page: 161,
    whatSi: "krščen Anton [~ — ime pod modrim pripisom; moški obrazci umrl/poročen] (16./17. 5.) — oče Jožef Štrucelj ½ zemljak (ŠTRUCELJ signal), mati Barbara Urvne [~]; h44 = 3. VPIS (1888, 1901 → 1906); botra Janez Hrižan + Doroteja Jevršovič [~] ¼ zemlj (HRIŽAN signal); babica Marjeta Vötter; podpis J. R. Kulbinek, o.t.cap. — PRVI KULBINEK (nov kaplan, prvi podpis r38 = 12.5.1906); umrl 27.1.1974 v Ljubljani; poročen na št. Videm pri Griblj(?)",
    whatEn: "baptized Anton [~ — the name under a blue note; male forms died/married] (May 16/17) — father Jožef Štrucelj half smallholder (the ŠTRUCELJ signal), mother Barbara Urvne [~]; h44 = the 3rd ENTRY (1888, 1901 → 1906); godparents Janez Hrižan + Doroteja Jevršovič [~] (the HRIŽAN signal); midwife Marjeta Vötter; signature J. R. Kulbinek, o.t.cap. — THE FIRST KULBINEK (a new chaplain, first signature r38 = May 12, 1906); died Jan 27, 1974 in Ljubljana; married at št. Videm pri Griblj(?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1906,
    scan: 174,
    page: 161,
    whatSi: "krščena Ana (4./4. 6.) — oče Matija Brinec ½ zemljak, mati Marija Grabrijan; h30 = 10. VPIS — MENJAVA DRUŽINE (Segina 1902/1903 → Brinec); botra Janez Brinec + Katarina Brinec ¼ zemlj (BRINEC signal ×3 — še r62); babica Marija Adlešič; podpis Jos. Ravq; umrla 17.10.1964 v Novem mestu; poročena 15.2.1943",
    whatEn: "baptized Ana (Jun 4/4) — father Matija Brinec half smallholder, mother Marija Grabrijan; h30 = the 10th ENTRY — a FAMILY CHANGE (Segina 1902/1903 → Brinec); godparents Janez Brinec + Katarina Brinec (the BRINEC signal ×3 — also r62); midwife Marija Adlešič; signature Jos. Ravq; died Oct 17, 1964 in Novo mesto; married Feb 15, 1943",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1906,
    scan: 174,
    page: 161,
    whatSi: "krščen Alois (15./15. 7.) — oče Janez Požek ½ zemljak (POŽEK signal = h58 oče 1903+1905!), mati Ana Šimec; h21 = 6. VPIS (1887, 1888, 1893, 1899, 1904 → 1906); botra Janez Kukar + Maria Šimec ½ zemljak; babica Marija Burek [~]; podpis J. R. Kulbinek, o.t.cap.; svinčnik † 29.1.1907 (dojenček)",
    whatEn: "baptized Alois (Jul 15/15) — father Janez Požek half smallholder (the POŽEK signal = the h58 father of 1903+1905!), mother Ana Šimec; h21 = the 6th ENTRY (1887, 1888, 1893, 1899, 1904 → 1906); godparents Janez Kukar + Maria Šimec; midwife Marija Burek [~]; signature J. R. Kulbinek, o.t.cap.; pencil † Jan 29, 1907 (an infant)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "4",
    bookSignature: "04105",
    year: 1906,
    scan: 175,
    page: 162,
    whatSi: "krščena Ana (31./31. 7.) — oče Janez Hrižan ¼ zemljak (HRIŽAN), mati Katarina Štrucel (ŠTRUCELJ); h4 = NOVA HIŠA — prvi krstni vpis (85. hiša v vitals; po dveh letih 1904+1905 brez novih; h4 JE v PT naboru); botra Matija Štraus (ŠTRAUS signal = h42 oče 1904 + h16 oče 1902 + h15 oče 1906!) + Doroteja Jerčimovič [~] ¼ zemlj; babica Marjeta Vötter; podpis Jos. Ravq; EMŠO ž 3107906505454 (sidro); DVOJNI modri pripis: Jože(?) umrl 11.3.1994 v Črnomlju + umrla 25.3.2004; poročena 26.9.1934(?)",
    whatEn: "baptized Ana (Jul 31/31) — father Janez Hrižan quarter smallholder (HRIŽAN), mother Katarina Štrucel (ŠTRUCELJ); h4 = A NEW HOUSE — the first baptism entry (the 85th house in vitals; after two years 1904+1905 with none; h4 IS in the PT nabor); godparents Matija Štraus (the ŠTRAUS signal = the h42 father 1904 + h16 father 1902 + h15 father 1906!) + Doroteja Jerčimovič [~]; midwife Marjeta Vötter; signature Jos. Ravq; EMŠO 3107906505454 (an anchor); a DOUBLE blue note: Jože(?) died Mar 11, 1994 in Črnomelj + died Mar 25, 2004; married Sep 26, 1934(?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04105",
    year: 1906,
    scan: 175,
    page: 162,
    whatSi: "krščen Alojzij (2./3. 8.) — oče Matija Simec ½ zemljak, mati Marija Kambič; h18 = 2. VPIS — VRZEL 8 LET (1898→1906); botra Janez Muc, bajtar + Marija Kambič ¼ zemlj; babica Marjeta Vötter; podpis J. R. Kulbinek, o.t.cap.; svinčnik † 24.12.06 (dojenček — umrl božični večer)",
    whatEn: "baptized Alojzij (Aug 2/3) — father Matija Simec half smallholder, mother Marija Kambič; h18 = the 2nd ENTRY — an 8-YEAR GAP (1898→1906); godparents Janez Muc, a cotter + Marija Kambič; midwife Marjeta Vötter; signature J. R. Kulbinek, o.t.cap.; pencil † Dec 24, 06 (an infant — died on Christmas eve)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "20",
    bookSignature: "04105",
    year: 1906,
    scan: 175,
    page: 162,
    whatSi: "krščena Katarina (10./10. 8.) — oče Peter Pozdirec [~ Pezdirec/Perdinec] ½ zemljak, mati Doroteja Klepec; h20 = 5. VPIS — ISTA DRUŽINA kot 1903 (Perdinec/Pozdirec × Klepec — kurrent priimka; 1903 EMŠO 20.10.1903 + babica Katarina Perdinec); botra Jurij Pozdirec + Marija Milek ¼ zemlj; babica Marija Mih; podpis Jos. Ravq; svinčnik † 23.11.08",
    whatEn: "baptized Katarina (Aug 10/10) — father Peter Pozdirec [~ Pezdirec/Perdinec] half smallholder, mother Doroteja Klepec; h20 = the 5th ENTRY — the SAME FAMILY as 1903 (Perdinec/Pozdirec × Klepec — a kurrent surname; 1903 EMŠO Oct 20, 1903 + midwife Katarina Perdinec); godparents Jurij Pozdirec + Marija Milek; midwife Marija Mih; signature Jos. Ravq; pencil † Nov 23, 08",
    status: "DOCUMENTED",
  },
  {
    houseNo: "42",
    bookSignature: "04105",
    year: 1906,
    scan: 175,
    page: 162,
    whatSi: "krščen Julij (20./20. 8.) — oče Jožef Pozdirec [~ Pezdirec] ½ zemljak, mati Katarina Jurasovič [~ Jurajevič]; h42 = 3. VPIS ZAPORED (1904 NOVA Štraus → 1905 Jurij Perdinec/Pezdirec × Katarina Jurajevič → 1906 Jožef — ISTA DRUŽINA 2. leto; Jožef = brat Jurija? MERI); botra Matija Mih + Katarina Pozdirec ¼ zemlj; babica Marija Mih; podpis J. R. Kulbinek, o.t.cap.; »26.3.1938 na Traki(?)«",
    whatEn: "baptized Julij (Aug 20/20) — father Jožef Pozdirec [~ Pezdirec] half smallholder, mother Katarina Jurasovič [~ Jurajevič]; h42 = the 3rd CONSECUTIVE ENTRY (1904 NEW Štraus → 1905 Jurij Perdinec/Pezdirec × Katarina Jurajevič → 1906 Jožef — the SAME FAMILY for a 2nd year; Jožef = Jurij's brother? MERI); godparents Matija Mih + Katarina Pozdirec; midwife Marija Mih; signature J. R. Kulbinek, o.t.cap.; »Mar 26, 1938 na Traki(?)«",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1906,
    scan: 176,
    page: 163,
    whatSi: "krščen Janez (6./7. 9.) — oče Janez Brinec ½ zemljak (POVRAT Brincove hiše 1887–1897), mati Ana Mitek [~ Mih]; h24 = 12. VPIS — ŠE VEDNO najbolj vpisovana hiša registra (1887–1904: 11 → 1906; MENJAVA: Jurajevič/Krašovec 1904 → Brinec); botra Matija Brinec + Marija Brinec ¼ zemlj; babica Katarina Dragoš; podpis Jos. Ravq; EMŠO m 0609906500161 (sidro); Črnomelj 1.1997(?), Metlika 30.12.1997; poročen 4.6.1939",
    whatEn: "baptized Janez (Sep 6/7) — father Janez Brinec half smallholder (the BRINEC HOUSE RETURNS 1887–1897), mother Ana Mitek [~ Mih]; h24 = the 12th ENTRY — STILL the most-entered house of the register (1887–1904: 11 → 1906; a CHANGE: Jurajevič/Krašovec 1904 → Brinec); godparents Matija Brinec + Marija Brinec; midwife Katarina Dragoš; signature Jos. Ravq; EMŠO 0609906500161 (an anchor); Črnomelj 1.1997(?), Metlika Dec 30, 1997; married Jun 4, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "69",
    bookSignature: "04105",
    year: 1906,
    scan: 176,
    page: 163,
    whatSi: "krščen Anton (18./18. 9.) — oče Janez Željko, bajtar (ISTI oče kot 1904), mati Marjeta Zamec [~ Žumič/Ženič]; h69 = 9. VPIS (1888–1904: 8 → 1906); botra Janez Dragoš + Marija Kralj ¾ zemlj; babica Marjeta Vötter; podpis J. R. Kulbinek, o.t.cap.; svinčnik † 9.2.07 (dojenček)",
    whatEn: "baptized Anton (Sep 18/18) — father Janez Željko, a cottager (the SAME father as 1904), mother Marjeta Zamec [~ Žumič/Ženič]; h69 = the 9th ENTRY (1888–1904: 8 → 1906); godparents Janez Dragoš + Marija Kralj; midwife Marjeta Vötter; signature J. R. Kulbinek, o.t.cap.; pencil † Feb 9, 07 (an infant)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04105",
    year: 1906,
    scan: 176,
    page: 163,
    whatSi: "krščena Barbara (13./14. 10.) — oče Nikolaj Šegina ½ zemljak (ŠEGINA signal = h30 oče 1902/1903!), mati Katarina Brinec; h26 = 4. VPIS — VRZEL 10 LET (1896→1906); botra Nikolaj Hrižan + Marija Malok [~] ½ zemlj (HRIŽAN signal); babica Marija Mih; podpis Kulbinek [bleda — izblidla; ~]; umrla 23.5.1969 v Metliki; poročena 5.10.1935(?)",
    whatEn: "baptized Barbara (Oct 13/14) — father Nikolaj Šegina half smallholder (the SEGINA signal = the h30 father of 1902/1903!), mother Katarina Brinec; h26 = the 4th ENTRY — a 10-YEAR GAP (1896→1906); godparents Nikolaj Hrižan + Marija Malok [~] (the HRIŽAN signal); midwife Marija Mih; signature Kulbinek [faded; ~]; died May 23, 1969 in Metlika; married Oct 5, 1935(?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1906,
    scan: 177,
    page: 164,
    whatSi: "krščena Barbara (24./25. 11.) — oče Marko Pozdirec [~ Pezdirec], bajtar (PEZDIREC signal), mati Katarina Žugelj; h27 = 8. VPIS (1887–1902: 7 → 1906); botra Nikol. Željko + Katar. Hrižan ¼ zemlj (HRIŽAN signal — Katarina = h34 botrinja 1903!); babica Marija Mih; podpis P. Kazimir Škrabec, coop. — NOV DUHOVNIK; svinčnik † 9.1.07 (dojenček)",
    whatEn: "baptized Barbara (Nov 24/25) — father Marko Pozdirec [~ Pezdirec], a cottager (the PEZDIREC signal), mother Katarina Žugelj; h27 = the 8th ENTRY (1887–1902: 7 → 1906); godparents Nikol. Željko + Katar. Hrižan (the HRIŽAN signal — Katarina = the h34 godmother 1903!); midwife Marija Mih; signature P. Kazimir Škrabec, coop. — A NEW PRIEST; pencil † Jan 9, 07 (an infant)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04105",
    year: 1906,
    scan: 178,
    page: 165,
    whatSi: "krščena Marija (13./19. 12.) — oče Jožef Pozdirec [~ Pezdirec] ½ zemljak (PEZDIREC signal), mati Ana Hrižan (HRIŽAN signal ×2 — mati + botrinja); h35 = 5. VPIS (1887, 1889, 1890, 1903 → 1906); botra Matija Mih + Marija Hrižan ¼ zemlj; babica Marija Mih; podpis P. Kazimir Škrabec, coop.; umrla 1.6.1959 v Gribljih št. 26(?); poročena",
    whatEn: "baptized Marija (Dec 13/19) — father Jožef Pozdirec [~ Pezdirec] half smallholder (the PEZDIREC signal), mother Ana Hrižan (the HRIŽAN signal ×2 — the mother + the godmother); h35 = the 5th ENTRY (1887, 1889, 1890, 1903 → 1906); godparents Matija Mih + Marija Hrižan; midwife Marija Mih; signature P. Kazimir Škrabec, coop.; died Jun 1, 1959 in Griblje no. 26(?); married",
    status: "DOCUMENTED",
  },
  {
    houseNo: "15",
    bookSignature: "04105",
    year: 1906,
    scan: 178,
    page: 165,
    whatSi: "krščen Francišek (22./22. 12.) — oče Matija Štraus ½ zemljak (ŠTRAUS signal — lead 04455 na 4. hiši h45→h40→h16→h15; VENDAR mati Marjeta Simec, NE Barbura Spudič — 2. Štrausov par [MERI]), mati Marjeta Simec; h15 = 6. VPIS (1887, 1890, 1893, 1896, 1904 → 1906); botra Jožef Štrucel (ŠTRUCELJ signal = r40 oče) + Barb. Jakobeč ¾ zemlj; babica Marija Mih; podpis P. Kazimir Škrabec, coop.; svinčnik † 1945? [~]",
    whatEn: "baptized Francišek (Dec 22/22) — father Matija Štraus half smallholder (the ŠTRAUS signal — the 04455 lead at a 4th house h45→h40→h16→h15; HOWEVER the mother Marjeta Simec, NOT Barbura Spudič — a 2nd Štraus couple [MERI]), mother Marjeta Simec; h15 = the 6th ENTRY (1887, 1890, 1893, 1896, 1904 → 1906); godparents Jožef Štrucel (the ŠTRUCELJ signal = the r40 father) + Barb. Jakobeč; midwife Marija Mih; signature P. Kazimir Škrabec, coop.; pencil † 1945? [~]",
    status: "DOCUMENTED",
  },
  // ——— P102 vzorec: polno leto 1907 (vsi Griblje vpisi, strani 165–172; r4 hiša neberljivo = pričevanje-samo brez bloka; NARE PRELOM h10 ×2; 0 novih hiš; NOVI kaplan Gregor Pecar; MIH 0×; EMŠO 6 sidr; dva nova dup para skenov 180/181 + 183/184; glava 1908 = P103 lead) ———
  {
    houseNo: "11",
    bookSignature: "04105",
    year: 1907,
    scan: 181,
    page: 166,
    whatSi: "krščena Ana (23./23. 2.) — oče Janez Žumič? [~ — 1905 »Žume?/Žunič?«, 1890 Zumik — ISTA familija; Kurrent varianta], ½ zemljak, mati Marija Jakolič? [~ — 1905 »Jakofčič?«]; h11 = 4. VPIS (1886, 1890, 1905 → 1907; vrzel 2 leti); kraj forenzika: »Grišlje« zapis = Griblje (genetska potrditev: Zumik = h11); botra Janez Adlešič + Marjeta Adlešič ½ zemlj [~ — 1905 »Albreič?« isti par? MERI]; babica Marjeta Šotter; podpis Jos. Ravq; modri pripis: umrla 6.8.1992 Novo mesto (MW NO NM kž. 1982(?), str. 231, zap. 401)",
    whatEn: "baptized Ana (Feb 23/23) — father Janez Žumič? [~ — 1905 »Žume?/Žunič?«, 1890 Zumik — the SAME family; a Kurrent variant], a half smallholder, mother Marija Jakolič? [~ — 1905 »Jakofčič?«]; h11 = the 4th ENTRY (1886, 1890, 1905 → 1907; a 2-year gap); village forensics: the »Grišlje« spelling = Griblje (genetic confirmation: Zumik = h11); godparents Janez Adlešič + Marjeta Adlešič [~ — 1905 »Albreič?« the same couple? MERI]; midwife Marjeta Šotter; signature Jos. Ravq; blue note: died Aug 6, 1992 Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04105",
    year: 1907,
    scan: 185,
    page: 169,
    whatSi: "krščen Alojzij (10./10. 7.) — oče Matija Papič? [~ — Kurrent P/T: »Tapič«; 1902 ISTI oče — ISTA družina], ¼ zemljak, mati Katarina Novak; h3 = 3. VPIS (1889 Županič? → 1902 MENJAVA Papič? → 1907 ISTA); botra Nikol. Novak + Ana Novak ¼ zemlj; babica Marija Papič? [~ Tapič?]; podpis Jos. Ravq; svinčnik: porojen 10.2.1950(?) [~] + umrl 4.9.1970 Novo mesto",
    whatEn: "baptized Alojzij (Jul 10/10) — father Matija Papič? [~ — the Kurrent P/T: »Tapič«; the 1902 SAME father — the SAME family], a quarter smallholder, mother Katarina Novak; h3 = the 3rd ENTRY (1889 Županič? → 1902 the CHANGE Papič? → 1907 the SAME); godparents Nikol. Novak + Ana Novak; midwife Marija Papič? [~ Tapič?]; signature Jos. Ravq; pencil: married Feb 10, 1950(?) [~] + died Sep 4, 1970 Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04105",
    year: 1907,
    scan: 185,
    page: 169,
    whatSi: "krščena Marjeta (27./27. 8.) — oče Jakob Toter [~ Toller] ½ zemljak (TOTER kot hišni oče — babica-priimek na hišni vlogi!), mati Katarina Jakobič [~ Jakobšič]; h7 = 4. VPIS (1890, 1901, 1905 → 1907 — ISTA družina kot 1901+1905); botra Janez Dragoš + Marija Štrucel ½ zemlj; babica Marjeta Šotter; podpis Jos. Ravq; EMŠO k: 2708907505219 (SKLADNO — sidro); modri pripis: umrla 18.7.1990 na Gribljah (MW NO Črnomelj, str. 124, zap. 59) + VPIS popravljen v matrični register 13.11.2007",
    whatEn: "baptized Marjeta (Aug 27/27) — father Jakob Toter [~ Toller], a half smallholder (TOTER as the house-father — the midwife surname on the house role!), mother Katarina Jakobič [~ Jakobšič]; h7 = the 4th ENTRY (1890, 1901, 1905 → 1907 — the SAME family as 1901+1905); godparents Janez Dragoš + Marija Štrucel; midwife Marjeta Šotter; signature Jos. Ravq; EMŠO 2708907505219 (CONSISTENT — the anchor); blue note: died Jul 18, 1990 at Griblje + the ENTRY CORRECTED into the civil register Nov 13, 2007",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1907,
    scan: 185,
    page: 169,
    whatSi: "krščen Nikolaj (27./27. 8.) — oče Janez Dragoš ½ zemljak, mati Barbara Cvitkovič [~ — 1892/96 »Civlkovič?/Druppovič?« cluster]; h12 = 11. VPIS — ISTA familija kot 1892/1894/1896 POVRAT po 1901/1905 Štraus/Šimec interludu (več-družinska hiša h12); botra Matija Štrucel? [~] + Ana Požek? [~]; babica Marjeta Šotter; podpis Jos. Ravq; EMŠO k: 2708907500520 (SKLADNO — sidro; istega dne kot r52 h7); modri pripis: žena(?) umrla 25.12.2005(?) v Gribljah [~ — datumi neskladni]",
    whatEn: "baptized Nikolaj (Aug 27/27) — father Janez Dragoš, a half smallholder, mother Barbara Cvitkovič [~ — the 1892/96 »Civlkovič?/Druppovič?« cluster]; h12 = the 11th ENTRY — the SAME family as 1892/1894/1896 BACK after the 1901/1905 Štraus/Šimec interlude (the multi-family h12); godparents Matija Štrucel? [~] + Ana Požek? [~]; midwife Marjeta Šotter; signature Jos. Ravq; EMŠO 2708907500520 (CONSISTENT — the anchor; the same day as r52 h7); blue note: the wife(?) died Dec 25, 2005(?) at Griblje [~ — inconsistent dates]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1907,
    scan: 186,
    page: 170,
    whatSi: "krščena Marija (17./18. 9.) — oče Matija Štrucel [~ Štrucelj] ¼ zemljak, mati Marija Meh [~ — 1903 »Mehle?«, 1905 »Muh«]; h5 = 4. VPIS (1891, 1903, 1905 → 1907 — ISTA družina kot 1903+1905); botra Janez Dragoš ½ zemljak + Alojzija Požek zamka gospa(?); babica Marjeta Šotter; podpis Gregor Pecar, kaplan — NOV KAPLAN, prvi podpis v letu 1907!; EMŠO k: 1709907505092 (SKLADNO — sidro); modri pripis: umrla 25.2.1983 v Gribljah (MW Griblje kž. 1983, str. 124); svinčnik na r60/r61 meji: »Umrl 31.5.1941« [~]",
    whatEn: "baptized Marija (Sep 17/18) — father Matija Štrucel [~ Štrucelj], a quarter smallholder, mother Marija Meh [~ — 1903 »Mehle?«, 1905 »Muh«]; h5 = the 4th ENTRY (1891, 1903, 1905 → 1907 — the SAME family as 1903+1905); godparents Janez Dragoš + Alojzija Požek; midwife Marjeta Šotter; signature Gregor Pecar, a curate — THE NEW CURATE, the first signature of 1907!; EMŠO 1709907505092 (CONSISTENT — the anchor); blue note: died Feb 25, 1983 at Griblje; pencil at the r60/r61 edge: »died May 31, 1941« [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04105",
    year: 1907,
    scan: 186,
    page: 170,
    whatSi: "krščen Alojzij (25./26. 9.) — oče Peter Brinec [~ — Kurrent B/W], bajtar, mati Ana Butala [~]; h18 = 3. VPIS (1898, 1906 → 1907) — MENJAVA DRUŽINE: Šimec (1898 Ana Kukar; 1906 Marija Kambič) → Brinec (1907); BRINEC signal 1/4; botra Matija Brinec? [~] + Katarina Požek? [~ Pohek?] ¼ zemlj; babica Marija Meh; podpis Gr. Pecar, kaplan; svinčnik: »Umrl 31.5.1941« [~] + modri pripis: poročen 21.5.1950(?) [~ — NESKLADJE]",
    whatEn: "baptized Alojzij (Sep 25/26) — father Peter Brinec [~ — the Kurrent B/W], a cottager, mother Ana Butala [~]; h18 = the 3rd ENTRY (1898, 1906 → 1907) — A FAMILY CHANGE: Šimec (1898 Ana Kukar; 1906 Marija Kambič) → Brinec (1907); the BRINEC signal 1/4; godparents Matija Brinec? [~] + Katarina Požek? [~ Pohek?]; midwife Marija Meh; signature Gr. Pecar, a curate; pencil: »died May 31, 1941« [~] + blue note: married May 21, 1950(?) [~ — a CONFLICT]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1907,
    scan: 186,
    page: 170,
    whatSi: "krščen Julij (9./10. 10.) — oče Janez Kure, bajtar, mati Barbara Mlajič? [~ Mlajn?]; h48 = 3. VPIS (1898, 1905 → 1907) — MENJAVA DRUŽINE: Pezdirec (1905 Jurij Pezdirec × Katarina Berkovec) → Kure (1907); PT luknja 41–60 (ponovitev dokumentirane); EMŠO k: 0910907500078 (SKLADNO — sidro); botra Martin Gregorič, viničar? [~] + Marija Pozdirec ¼ zemlj; babica Ana Muc; podpis Gr. Pecar, kaplan; modri pripis: umrl 8.3.1985 Novo mesto; svinčnik: poročen 6.6.1937(?) [~]; dva Janez Kure očetja v 1907 (h48 + h62) [MERI]",
    whatEn: "baptized Julij (Oct 9/10) — father Janez Kure, a cottager, mother Barbara Mlajič? [~ Mlajn?]; h48 = the 3rd ENTRY (1898, 1905 → 1907) — A FAMILY CHANGE: Pezdirec (1905 Jurij Pezdirec × Katarina Berkovec) → Kure (1907); the PT gap 41–60 (a repeat of a documented number); EMŠO 0910907500078 (CONSISTENT — the anchor); godparents Martin Gregorič + Marija Pozdirec; midwife Ana Muc; signature Gr. Pecar, a curate; blue note: died Mar 8, 1985 Novo mesto; pencil: married Jun 6, 1937(?) [~]; two Janez Kure fathers in 1907 (h48 + h62) [MERI]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1907,
    scan: 186,
    page: 170,
    whatSi: "krščen Jožef (14./14. 10.) — oče Jožef Kapucina? [~ — Kurrent: »Kapeusina/Hapušina« — branje negotovo], ½ zemljak, mati Barbara Moravec; h6 = 3. VPIS (1904, 1905 → 1907) — MENJAVA DRUŽINE: Jakobič (1904/05) → Kapucina? × Moravec (1907); botra Matija Štrausime? [~ — Kurrent nejasen] + Marjeta Štrausime? [~] ¼ zemlj; babica Marija Klepec; podpis Gregor Pecar, kaplan? [~ — bled, rob]; modri pripis [~ nejasno]",
    whatEn: "baptized Jožef (Oct 14/14) — father Jožef Kapucina? [~ — the Kurrent: »Kapeusina/Hapušina« — an uncertain reading], a half smallholder, mother Barbara Moravec; h6 = the 3rd ENTRY (1904, 1905 → 1907) — A FAMILY CHANGE: Jakobič (1904/05) → Kapucina? × Moravec (1907); godparents Matija Štrausime? [~ — an unclear Kurrent] + Marjeta Štrausime? [~]; midwife Marija Klepec; signature Gregor Pecar, a curate? [~ — faded, page edge]; a blue note [~ unclear]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "49",
    bookSignature: "04105",
    year: 1907,
    scan: 187,
    page: 171,
    whatSi: "krščen Nikolaj (18./19. 10.) — oče Nikolaj Brodarič ½ zemljak, mati Ana Milek [~ — 1906 mati »Marija Miheč« — menjava žene 2.× ali Kurrent varianta? MERI]; h49 = 3. VPIS (1899, 1906 → 1907 — ISTI oče; žene: Milek 1899 → Miheč 1906 → Milek? 1907); PT luknja 41–60 (ponovitev); botra Nikolaj Željko + Barb. Klobučar ¼ zunlj? [~]; babica Marija Meh; podpis Gregor Pecar, kaplan; svinčnik: † 17.11.1907 — DOJENČEK (30 dni); ŽELJKO signal",
    whatEn: "baptized Nikolaj (Oct 18/19) — father Nikolaj Brodarič, a half smallholder, mother Ana Milek [~ — the 1906 mother »Marija Miheč« — a 2nd wife change or a Kurrent variant? MERI]; h49 = the 3rd ENTRY (1899, 1906 → 1907 — the SAME father; wives: Milek 1899 → Miheč 1906 → Milek? 1907); the PT gap 41–60 (a repeat); godparents Nikolaj Željko + Barb. Klobučar; midwife Marija Meh; signature Gregor Pecar, a curate; pencil: † Nov 17, 1907 — an INFANT (30 days); the ŽELJKO signal",
    status: "DOCUMENTED",
  },
  {
    houseNo: "27",
    bookSignature: "04105",
    year: 1907,
    scan: 187,
    page: 171,
    whatSi: "krščena Helena (5./5. 11.) — oče Marko Pozdirec [~ Pezdirec], bajtar, mati Katarina Žugelj [~ Zugelj]; h27 = 9. VPIS (1887–1906: 8 → 1907) — ISTA družina kot 1906 + ISTA BOTRA 2. leto (Nikol. Željko + Katar. Hrižan — kot P101 r79); PEZDIREC + HRIŽAN signali; hišna forenzika: zapis »8y« = Kurrent »27« (genetska potrditev: familija + botra = h27/1906); EMŠO k: 0511907305286 [~ — 8. števka 3/5 dvom] (SKLADNO — sidro); babica Marija Meh; podpis Gregor Pecar, kaplan; modri pripis: umrla 18.1.1993 Metlika + poročena 12.6.1939",
    whatEn: "baptized Helena (Nov 5/5) — father Marko Pozdirec [~ Pezdirec], a cottager, mother Katarina Žugelj [~ Zugelj]; h27 = the 9th ENTRY (1887–1906: 8 → 1907) — the SAME family as 1906 + THE SAME GODPARENTS for a 2nd year (Nikol. Željko + Katar. Hrižan — like P101 r79); the PEZDIREC + HRIŽAN signals; house forensics: the spelling »8y« = the Kurrent »27« (the genetic confirmation: family + godparents = h27/1906); EMŠO 0511907305286 [~ — the 8th digit 3/5 doubt] (CONSISTENT — the anchor); midwife Marija Meh; signature Gregor Pecar, a curate; blue note: died Jan 18, 1993 Metlika + married Jun 12, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1907,
    scan: 187,
    page: 171,
    whatSi: "krščena Marija (12./12. 11.) — oče Matija Šimec ¼ zemljak, mati Marija Kambič; h13 = 6. VPIS (…1894 → 1907) — VRZEL 13 LET + MENJAVA DRUŽINE: Jakopič (…–1894) → Šimec × Kambič (1907); ŠIMEC×KAMBIČ SELITEV h18→h13 (ista zveza kot h18 1906 P101!); h18 prevzel Peter Brinec (r61); botra Janez Muc, bajtar + Ana Kambič ¼ zemlj; babica Marjeta Šotter; podpis Jos. Ravq; modri pripis: umrla 19.10.1971 v Gribljah (MW Griblje kž. 1971, str. 95) + poročen 30.9.1939 [~ mš. oblika]",
    whatEn: "baptized Marija (Nov 12/12) — father Matija Šimec, a quarter smallholder, mother Marija Kambič; h13 = the 6th ENTRY (…1894 → 1907) — a 13-YEAR GAP + A FAMILY CHANGE: Jakopič (…–1894) → Šimec × Kambič (1907); the ŠIMEC×KAMBIČ HOUSE MOVE h18→h13 (the same couple as h18 1906 P101!); h18 was taken over by Peter Brinec (r61); godparents Janez Muc, a cottager + Ana Kambič; midwife Marjeta Šotter; signature Jos. Ravq; blue note: died Oct 19, 1971 at Griblje + married Sep 30, 1939 [~ a masc. form]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "83",
    bookSignature: "04105",
    year: 1907,
    scan: 187,
    page: 171,
    whatSi: "krščen Jožef (26./27. 11.) — oče Jožef Željko ¼ zemljak [~], mati Ana Peruš? [~ Perše? — 1903 mati »Nina Gorše?« — ista žena? MERI]; h83 = 4. VPIS (1888/1889, 1903 → 1907; luknja 1890–1902) — ISTA družina kot 1903 (Jožef Željko) — brez menjave; ŽELJKO signal (oče + boter Nikolaj Željko); botra Nikolaj Željko + Katar. Jakofčič? [~] ½ zunlj? [~]; babica Marjeta Šotter; podpis Gr. Pecar, kaplan; svinčnik: † 21.3.1927(?) [~]; hiša 83 forenzika: jasno 83 (8+ʒ konvencija)",
    whatEn: "baptized Jožef (Nov 26/27) — father Jožef Željko, a quarter smallholder [~], mother Ana Peruš? [~ Perše? — the 1903 mother »Nina Gorše?« — the same wife? MERI]; h83 = the 4th ENTRY (1888/1889, 1903 → 1907; the 1890–1902 gap) — the SAME family as 1903 (Jožef Željko) — no change; the ŽELJKO signal (the father + godfather Nikolaj Željko); godparents Nikolaj Željko + Katar. Jakofčič? [~]; midwife Marjeta Šotter; signature Gr. Pecar, a curate; pencil: † Mar 21, 1927(?) [~]; house 83 forensics: clearly 83 (the 8+ʒ convention)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04105",
    year: 1907,
    scan: 188,
    page: 172,
    whatSi: "krščen Jožef (14./14. 12.) — DVOJČEK (r85+r86) — oče Janez Brinec ½ zemljak, mati Ana Klepec [~ Kleme?]; h10 = 3. VPIS (1897, 1900 → 1907) — VRZEL 7 LET; BRINEC POVRAT (1897 Janez Brinec × Marija Per? → 1900 Grabrijan × Pozdirec → 1907 Janez Brinec × Ana Klepec — druga žena MERI); NARE PRELOM — 1. intra-letna ponovitev hiše po 1905 (h12 ×2); botra Janez Muc, kovač + Katarina Kure ¼ zemlj (KURE signal); babica Marjeta Toter (zapis »Toter« — r86 »Šotter« ISTA Marjeta!); podpis Grg. Pecar, kaplan; svinčnik: † 25.12.1907 — DOJENČEK (11 dni; božič)",
    whatEn: "baptized Jožef (Dec 14/14) — a TWIN (r85+r86) — father Janez Brinec, a half smallholder, mother Ana Klepec [~ Kleme?]; h10 = the 3rd ENTRY (1897, 1900 → 1907) — a 7-YEAR GAP; the BRINEC RETURN (1897 Janez Brinec × Marija Per? → 1900 Grabrijan × Pozdirec → 1907 Janez Brinec × Ana Klepec — another wife MERI); THE NARE BREAK — the 1st intra-year house repeat since 1905 (h12 ×2); godparents Janez Muc, a smith + Katarina Kure (the KURE signal); midwife Marjeta Toter (spelled »Toter« — r86 »Šotter« the SAME Marjeta!); signature Grg. Pecar, a curate; pencil: † Dec 25, 1907 — an INFANT (11 days; Christmas)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04105",
    year: 1907,
    scan: 188,
    page: 172,
    whatSi: "krščen Anton (14./14. 12.) — DVOJČEK r85 (isti dan; oče Janez Brinec ½ zemljak + mati Ana Klepec [~ Kleme?] — isti starši + ISTA botra Janez Muc kovač + Katarina Kure); h10 = 3. VPIS — 2. vpis h10 v letu 1907 (NARE PRELOM, 2. primer po 1905 h12 ×2); babica Marjeta Šotter (zapis »Šotter« — r85 »Toter« ISTA Marjeta!); podpis Greg. Pecar, kaplan; svinčnik: † 19/12 07 — DOJENČEK (5 dni — PREJ kot brat Jožef † 25.12.)",
    whatEn: "baptized Anton (Dec 14/14) — a TWIN of r85 (the same day; father Janez Brinec + mother Ana Klepec — the same parents + THE SAME godparents Janez Muc, a smith + Katarina Kure); h10 = the 3rd ENTRY — the 2nd h10 entry of 1907 (THE NARE BREAK, the 2nd case after 1905 h12 ×2); midwife Marjeta Šotter (spelled »Šotter« — r85 »Toter« the SAME Marjeta!); signature Greg. Pecar, a curate; pencil: † Dec 19, 07 — an INFANT (5 days — BEFORE his brother Jožef † Dec 25)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04105",
    year: 1907,
    scan: 188,
    page: 172,
    whatSi: "krščen Alojzij (15./15. 12.) — oče Janez Kure ½ zemljak, mati Marija Požek; h62 = 3. VPIS (1887, 1891 → 1907) — VRZEL 16 LET (2. najdaljša v vzorcu za h39 18 let); BRINEC signal 4/4 (boter Janez Brinec = oče r85/86!) + KURE signal (oče + botrinja Marjeta Kure ¼ zemlj); boter Janez Brinec ½ zemljak; babica Marija Urh; podpis Greg. Pecar, kaplan; pripisa: poročen 16.2.1941 + † 1.7.1942 (skladna); drugi Janez Kure oče 1907 = h48 (r64) [MERI]",
    whatEn: "baptized Alojzij (Dec 15/15) — father Janez Kure, a half smallholder, mother Marija Požek; h62 = the 3rd ENTRY (1887, 1891 → 1907) — a 16-YEAR GAP (the 2nd longest in the sample after h39's 18); the BRINEC signal 4/4 (godfather Janez Brinec = the r85/86 father!) + the KURE signal (the father + godmother Marjeta Kure); godfather Janez Brinec; midwife Marija Urh; signature Greg. Pecar, a curate; the notes: married Feb 16, 1941 + † Jul 1, 1942 (consistent); the other Janez Kure father of 1907 = h48 (r64) [MERI]",
    status: "DOCUMENTED",
  },
  // ——— P103 vzorec: polno leto 1908 (vsi Griblje vpisi, strani 173–180; r84 hiša neberljivo = pričevanje-samo brez bloka; NARE 18/18; 0 novih hiš; NOV duhovnik Jos. Dami; nujni krst r41; trije novi dup pari 189/190 + 193/194 + 197/198; glava 1909 INLINE r91 = P104 lead) ———
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1908,
    scan: 191,
    page: 174,
    whatSi: "krščena Marija (16./16. 2.) — oče Janez Brinec ¼ zemljak (+ gost pripis o posestvu na očetovi celici [~ — nerazumljiv]), mati Doroteja Perdinec? [~ — ali Pezdirec/Pozdinec cf. 1900/02 mati Marija Pegdinec?/Podirec]; h14 = 4. VPIS ISTA familija (1896 neimenovani, 1900, 1902 — BRINEC kontinuiteta); mati menjava (Marija P… → Doroteja P…) [MERI]; botra = babica ISTA oseba Barbara Adlešič (botra ½ zemlj. hiša); podpis Gregor Cerar; svinčnik: † 9/11.1911",
    whatEn: "baptized Marija (Feb 16/16) — father Janez Brinec, a quarter smallholder (+ a dense property note on the father's cell [~ — wholly illegible]), mother Doroteja Perdinec? [~ — or Pezdirec/Pozdinec cf. the 1900/02 mother Marija Pegdinec?/Podirec]; h14 = the 4th ENTRY the SAME family (1896 unnamed, 1900, 1902 — the BRINEC continuity); a mother change (Marija P… → Doroteja P…) [MERI]; the godmother = midwife the SAME person Barbara Adlešič; signature Gregor Cerar; pencil: † Nov 9, 1911",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1908,
    scan: 191,
    page: 174,
    whatSi: "krščena Katarina (29./29. 2. — PRESTOPNI dan) — oče Nikolaj Željko ¼ zemljak, mati Marija Brodarič? [~ — pisano »Prodarvič/Šrodarvič«; genetsko h60 = Željko × Brodarič 1888+1894+1897+1899+1906]; h60 = 8. VPIS ISTA ZVEZA (Željko × Brodarič — 5. OTROK istega para; 1906 je bil 7. VPIS); botrinja Marija Klepec 4.× (P101 r19: 3.× 1906); botra Nikol. Brodarič? [~ — isti zapis kot mati] + Marija Klepec ¼ zemlj; babica Marija Muc; podpis Gregor Cerar; svinčnik: † 30.9.1922",
    whatEn: "baptized Katarina (Feb 29/29 — the LEAP day) — father Nikolaj Željko, a quarter smallholder, mother Marija Brodarič? [~ — spelled »Prodarvič/Šrodarvič«; genetically h60 = Željko × Brodarič 1888+1894+1897+1899+1906]; h60 = the 8th ENTRY the SAME couple (the 5th CHILD of the same parents; 1906 was the 7th); godmother Marija Klepec the 4th time (P101 r19: the 3rd in 1906); godparents Nikol. Brodarič? [~ — the same spelling as the mother] + Marija Klepec; midwife Marija Muc; signature Gregor Cerar; pencil: † Sep 30, 1922",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1908,
    scan: 191,
    page: 174,
    whatSi: "krščena Marija (rojstva 16. 3.; krsta skrita pod matičnim pripisom) — oče Janez Brinec ¼ zemljak, mati Ana Milek? [~ — cf. 1906 mati Ana Mitek? — morda ista Ana]; h24 = 13. VPIS — ŠE VEDNO najbolj vpisovana hiša registra (POVRAT Brincove hiše: 1906 Janez Brinec ½ × Ana Mitek? → 1908 Janez Brinec ¼ × Ana Milek?); botra Matija Brinec + Marija Brinec ¼ zemlj; babica Barbara Adlešič; podpis Jos. Dami [~ — morda Damiš/Damijan; NOV DUHOVNIK — 1. podpis na Gribljih 1908]; matični pripis: umrla 21.10.1986",
    whatEn: "baptized Marija (born Mar 16; the baptism hidden under a civil-registry note) — father Janez Brinec, a quarter smallholder, mother Ana Milek? [~ — cf. the 1906 mother Ana Mitek? — perhaps the same Ana]; h24 = the 13th ENTRY — STILL the most-entered house of the register (the BRINEC HOUSE RETURNS: 1906 Janez Brinec × Ana Mitek? → 1908 Janez Brinec × Ana Milek?); godparents Matija Brinec + Marija Brinec; midwife Barbara Adlešič; signature Jos. Dami [~ — perhaps Damiš/Damijan; A NEW PRIEST — the 1st Griblje signature of 1908]; civil note: died Oct 21, 1986",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1908,
    scan: 192,
    page: 175,
    whatSi: "krščena Amalija (30./30. 3.) — oče Narciz? [~ — branje negotovo »…vziž/Narciz«] Novak, bajtar, mati Marija Tilak? [~ — ali Šilak cf. 1900]; h16 = 8. VPIS — NOVAK bajtar POVRAT cf. 1900 (Alojzij Novak bajtar × Marija Šilak); h16 = več-družinska hiša (7 menjav 1886–1908: Plebučar → Jaklič → Novak → Straus → Ivec → Jakofčič → Novak); CROSS-ROW: boter Janez Muc kovač = r31 h91 oče (bajtar) [MERI]; botra Janez Muc kovač + Marija Jakofčič ¼ zemlj; babica Marija Muc; podpis Jos. Dami [~]; modri pripis: poročena 23.12.1946 v Brežjah + matičar Simonič Ivān",
    whatEn: "baptized Amalija (Mar 30/30) — father Narciz? [~ — an uncertain reading »…vziž/Narciz«] Novak, a cottager, mother Marija Tilak? [~ — or Šilak cf. 1900]; h16 = the 8th ENTRY — the NOVAK cottager RETURNS cf. 1900 (Alojzij Novak × Marija Šilak); h16 = a multi-family house (7 changes 1886–1908); CROSS-ROW: the godfather Janez Muc, a smith = the r31 h91 father (a cottager) [MERI]; godparents Janez Muc + Marija Jakofčič; midwife Marija Muc; signature Jos. Dami [~]; blue note: married Dec 23, 1946 at Brežje + the registrar Simonič Ivān",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04105",
    year: 1908,
    scan: 192,
    page: 175,
    whatSi: "krščen Jožef (22./23. 4.) — oče Janez Muc, bajtar, mati Ana Kure; h91 = 5. VPIS ISTA (1895/1902/1904/1908 — MUC bajtar × Kure kontinuiteta potrjena); EMŠO č. 2204908500557 (22.04.1908 m — SKLADNO — sidro); botra Marija Šimco? [~ — cf. Šimec] + Marija Jakofčič? [~ — ali Jatiščič] ¼ zemlj; babica Marija Meh; podpis Gregor Cerar; nerazumljiv pripis pod krajem »… dvahican … Šhulac Štucora? [~]«; pripisno neskladje poroke (modri 6.10.1938 v Karlovci vs zeleni 16.3.1938 [~]); umrl 04.02.1990 v Novem mestu",
    whatEn: "baptized Jožef (Apr 22/23) — father Janez Muc, a cottager, mother Ana Kure; h91 = the 5th ENTRY the SAME (1895/1902/1904/1908 — the MUC × KURE continuity confirmed); personal ID 2204908500557 (Apr 22, 1908 m — CONSISTENT — an anchor); godparents Marija Šimco? + Marija Jakofčič? [~]; midwife Marija Meh; signature Gregor Cerar; an illegible note under the village »… Šhulac Štucora? [~]«; a marriage note conflict (blue Oct 6, 1938 vs green Mar 16, 1938 [~]); died Feb 4, 1990 in Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "85",
    bookSignature: "04105",
    year: 1908,
    scan: 193,
    page: 176,
    whatSi: "krščen Jožef (24./24. 5.) — NUJNI KRST (pripis »v sili krščen? [~ — ali klican]«; botra in podpis PRAZNA — črti!) — oče Jožef Pezdirec ¼ zemljak, mati Ana Kržan? [~ — Križan/Kržan]; h85 = 2. VPIS — VRZEL 20 LET (1888 Marko Križan × Marija Strauš → 1908 NOVA DRUŽINA Pezdirec × Kržan); babica Marija Muc kot krstiteljica; podpis PRAZEN; dup par 193/194 (r41 identična na obojih); svinčnik: † 29/5.08 — DOJENČEK (5 dni)",
    whatEn: "baptized Jožef (May 24/24) — an EMERGENCY BAPTISM (the note »baptized in necessity?«; the godparents and signature EMPTY — dashes!) — father Jožef Pezdirec, a quarter smallholder, mother Ana Kržan? [~]; h85 = the 2nd ENTRY — a 20-YEAR GAP (1888 Marko Križan × Marija Strauš → 1908 a NEW FAMILY Pezdirec × Kržan); midwife Marija Muc as the baptizer; the signature EMPTY; the dup pair 193/194 (identical on both); pencil: † May 29, 08 — an INFANT (5 days)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "52",
    bookSignature: "04105",
    year: 1908,
    scan: 193,
    page: 176,
    whatSi: "krščen Janez (23./24. 6.) — oče Matija Pezdirec ¼ zemljak, mati Ana Jakobčič; h52 = 3. VPIS — ISTA ZVEZA čez 10 LET (1898 Matija Podrinc [Pendirec] × Ana Jakobič = 1908 Pezdirec × Jakobčič — Kurrent variante ISTEGA para; VRZEL 1899–1907); botra Anton Brodarič? + Katarina Kržan? ½ zemlj; babica Marija Muc; podpis Gregor Cerar; hišna forenzika: jasno 52 (3 pogledi)",
    whatEn: "baptized Janez (Jun 23/24) — father Matija Pezdirec, a quarter smallholder, mother Ana Jakobčič; h52 = the 3rd ENTRY — the SAME couple across 10 YEARS (1898 Matija Podrinc [Pendirec] × Ana Jakobič = 1908 Pezdirec × Jakobčič — Kurrent variants of the SAME couple; the 1899–1907 gap); godparents Anton Brodarič? + Katarina Kržan?; midwife Marija Muc; signature Gregor Cerar; house forensics: clearly 52 (3 looks)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1908,
    scan: 193,
    page: 176,
    whatSi: "krščena Ana (7./8. 7.) — oče Jožef Štrucelj ½ zemljak, mati Barbara Šome [~ — 1906 mati »Barbara Urvne?« — morda ISTA Barbara]; h44 = 5. VPIS (1887 mrliška, 1888 Hlevič, 1901 Jurajevič, 1906 → 1908 Štrucelj ISTA OČE); na skenu 193 pod trakom — forenzika na dup skenu 194 (jasnejši); r47 botrinja Doroteja (Jerčinovič?) = r69 mati Doroteja Štrucelj — CROSS-ROW [MERI]; botra Janez Križan? [~ — Hrižan?] + Doroteja Jerčinovič? ¼ zemlj; babica Marija Muc; podpis Gregor Cerar",
    whatEn: "baptized Ana (Jul 7/8) — father Jožef Štrucelj, a half smallholder, mother Barbara Šome [~ — the 1906 mother »Barbara Urvne?« — perhaps the SAME Barbara]; h44 = the 5th ENTRY (1887 a death, 1888 Hlevič, 1901 Jurajevič, 1906 → 1908 Štrucelj the SAME father); under the strip on scan 193 — the forensics on the dup scan 194 (clearer); the r47 godmother Doroteja (Jerčinovič?) = the r69 mother Doroteja Štrucelj — a CROSS-ROW [MERI]; godparents Janez Križan? + Doroteja Jerčinovič?; midwife Marija Muc; signature Gregor Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04105",
    year: 1908,
    scan: 195,
    page: 177,
    whatSi: "krščena Amalija (11./12. 8.) — oče Brinec? [~ — očetova celica RAZTRGANA (vertikalni strgljek); konec »-inec«; cf. h23 = Brincova hiša Matija Brinec 1893–1905], mati Marija Dehlič; h23 = 7. VPIS — ISTA ZVEZA čez 8 LET (1900 Matija Brinec × Marija Dehlič = 1908 [Brinec?] × Marija Dehlič — MATI ISTA!); botra Tomaž Dehlič + Katarina Dehlič ¼ zemlj (DEHLIČ ×3 v eni vrstici); babica Marija Meh; podpis Gregor Cerar",
    whatEn: "baptized Amalija (Aug 11/12) — father Brinec? [~ — the father's cell TORN (a vertical scrape); the ending »-inec«; cf. h23 = the Brinec house Matija Brinec 1893–1905], mother Marija Dehlič; h23 = the 7th ENTRY — the SAME couple across 8 YEARS (1900 Matija Brinec × Marija Dehlič = 1908 [Brinec?] × Marija Dehlič — the MOTHER the SAME!); godparents Tomaž Dehlič + Katarina Dehlič (DEHLIČ ×3 in one row); midwife Marija Meh; signature Gregor Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1908,
    scan: 195,
    page: 177,
    whatSi: "krščena Marija (20./20. 8.) — oče Matija Milek ¼ zemljak (MILEK kontinuiteta — Kurrent variante Milek/Mihelt/Mihek/Mitek 1887–1904), mati Marija Hevič? [~ — cf. 1904 mati Marija Hrišič? — morda ISTA]; h65 = 9. VPIS — MILEK 1887–1908 (mati menjava: Katarina P…/Š… 1887–1901 → Marija H… 1904 → 1908); boter Peter Pezdirec ISTA kot 1887 — 21 LET kasneje!; babica Barbara Adlešič = botrinja 1887!; botra Peter Pezdirec + Katarina Hevič? ¼ zemlj; podpis Gregor Cerar; svinčnik: † 4/9.1919",
    whatEn: "baptized Marija (Aug 20/20) — father Matija Milek, a quarter smallholder (the MILEK continuity — the Kurrent variants Milek/Mihelt/Mihek/Mitek 1887–1904), mother Marija Hevič? [~ — cf. the 1904 mother Marija Hrišič? — perhaps the SAME]; h65 = the 9th ENTRY — MILEK 1887–1908 (the mother changes: Katarina P…/Š… 1887–1901 → Marija H… 1904 → 1908); godfather Peter Pezdirec the SAME as 1887 — 21 YEARS later!; midwife Barbara Adlešič = the 1887 godmother!; godparents Peter Pezdirec + Katarina Hevič?; signature Gregor Cerar; pencil: † Sep 4, 1919",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1908,
    scan: 196,
    page: 178,
    whatSi: "krščen Alojzij (3./4. 10.) — oče Anton Brodarič ¼ zemljak, mati Katarina Milek; h46 = 6. VPIS — ISTA OČE Anton Brodarič cf. 1893–1899 (VRZEL 9 LET 1900–1907; 6. mati? Katarina Milek NOVA); EMŠO č. 0310908500848 (3.10.1908 ž — SKLADNO — sidro); boter Nikolaj Željko (ŽELJKO signal); botra Nikolaj Željko + Ana Pezdirec ¼ zemlj; babica Marija Adlešič; podpis Jos. Ravq; modri pripis: poročen 16.9.1939",
    whatEn: "baptized Alojzij (Oct 3/4) — father Anton Brodarič, a quarter smallholder, mother Katarina Milek; h46 = the 6th ENTRY — the SAME father Anton Brodarič cf. 1893–1899 (a 9-YEAR GAP 1900–1907; a 6th mother? Katarina Milek NEW); personal ID 0310908500848 (Oct 3, 1908 f — CONSISTENT — an anchor); godfather Nikolaj Željko (the ŽELJKO signal); godparents Nikolaj Željko + Ana Pezdirec; midwife Marija Adlešič; signature Jos. Ravq; blue note: married Sep 16, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1908,
    scan: 196,
    page: 178,
    whatSi: "krščen Leopold (4./5. 10.) — oče Nikolaj Segina ¼ zemljak, mati Katarina Brinec; h30 = 11. VPIS — SEGINA POVRAT po 1906 Brinec interludu (1895/96 Šegina? → 1902/03 Nikolaj Segina → 1906 Matija Brinec → 1908 Nikolaj Segina!); mati Katarina Brinec ISTA kot 1903 — par POVRAT po 5 letih; EMŠO č. 0410908500444 (4.10.1908 m — SKLADNO — sidro); botra Marija Milek + Katarina Kržan? ¼ zemlj; babica Barbara Adlešič; podpis Gregor Cerar; modri pripis: poročen 18.10.1951 [~]",
    whatEn: "baptized Leopold (Oct 4/5) — father Nikolaj Segina, a quarter smallholder, mother Katarina Brinec; h30 = the 11th ENTRY — the SEGINA RETURN after the 1906 Brinec interlude (1895/96 Šegina? → 1902/03 Nikolaj Segina → 1906 Matija Brinec → 1908 Nikolaj Segina!); the mother Katarina Brinec the SAME as 1903 — the couple RETURNS after 5 years; personal ID 0410908500444 (Oct 4, 1908 m — CONSISTENT — an anchor); godparents Marija Milek + Katarina Kržan?; midwife Barbara Adlešič; signature Gregor Cerar; blue note: married Oct 18, 1951 [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "49",
    bookSignature: "04105",
    year: 1908,
    scan: 196,
    page: 178,
    whatSi: "krščena Barbara (8./9. 10.) — oče Nikolaj Brodarič ½ zemljak, mati Marija Milek? [~ — 1906 Marija Miheč?, 1907 Ana Milek? — variante]; h49 = 4. VPIS ISTA — Brodarič kontinuiteta (1899 NOVA, 1906, 1907 dojenček † 17.11. → 1908); EMŠO č. 0810908505763 (8.10.1908 ž — SKLADNO — sidro); botra Jurij Pezdirec + Katarina Boble? [~] ¼ zemlj (boter 1./3 v 1908); babica Marija Muc; podpis Jos. Ravq; modri pripisi: poročena 13.3.1936 + umrla 16.9.1987 v Gribljah",
    whatEn: "baptized Barbara (Oct 8/9) — father Nikolaj Brodarič, a half smallholder, mother Marija Milek? [~ — 1906 Marija Miheč?, 1907 Ana Milek? — variants]; h49 = the 4th ENTRY the SAME — the Brodarič continuity (1899 NEW, 1906, 1907 an infant † Nov 17 → 1908); personal ID 0810908505763 (Oct 8, 1908 f — CONSISTENT — an anchor); godparents Jurij Pezdirec + Katarina Boble? [~] (the godfather 1st of 3 in 1908); midwife Marija Muc; signature Jos. Ravq; blue notes: married Mar 13, 1936 + died Sep 16, 1987 in Griblje",
    status: "DOCUMENTED",
  },
  {
    houseNo: "56",
    bookSignature: "04105",
    year: 1908,
    scan: 196,
    page: 178,
    whatSi: "krščen Danijel (17./17. 10.) — oče Janez Jerčinovič? [~ — Jereinovič/Jercimovič] ¼ zemljak, mati Doroteja Štrucelj; h56 = 3. VPIS — VRZEL 20 LET (1886 Janez Šimec × Dora Perdinec → 1888 nezakonski → 1908 NOVA DRUŽINA Jerčinovič? × Štrucelj); mati = r47 botrinja (CROSS-ROW); botra Jurij Pezdirec + Katarina Kržan? ¼ zemlj (boter 2./3 v 1908 — 2. dan zapored po r68!); babica Barbara Adlešič; podpis Gregor Cerar; modri pripisi: poročen 13.5.1934 + umrl 12.3.1976 v Novem mestu",
    whatEn: "baptized Danijel (Oct 17/17) — father Janez Jerčinovič? [~ — Jereinovič/Jercimovič], a quarter smallholder, mother Doroteja Štrucelj; h56 = the 3rd ENTRY — a 20-YEAR GAP (1886 Janez Šimec × Dora Perdinec → 1888 illegitimate → 1908 a NEW FAMILY Jerčinovič? × Štrucelj); the mother = the r47 godmother (a CROSS-ROW); godparents Jurij Pezdirec + Katarina Kržan? (the godfather 2nd of 3 in 1908 — the 2nd consecutive day after r68!); midwife Barbara Adlešič; signature Gregor Cerar; blue notes: married May 13, 1934 + died Mar 12, 1976 in Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1908,
    scan: 196,
    page: 178,
    whatSi: "krščena Amalija (21./21. 10.) — oče Janez Križan ¼ zemljak, mati Katarina Štrucelj [~ — 1894–1902 mati Katarina Straucelj/Straus — ISTA]; h36 = 11. VPIS — KRIŽAN POVRAT (1894/1896/1898/1902 Janez Križan × Katarina Straucelj → 1904 Miše interlud → 1908 ISTA ZVEZA vrne); botra Matija Štraus + Marija Perdinec? [Pezdirec?] ¼ zemlj (ŠTRAUS kampanja); babica Barbara Adlešič; podpis Gregor Cerar; poznejši pripis [~ — + 1961?]",
    whatEn: "baptized Amalija (Oct 21/21) — father Janez Križan, a quarter smallholder, mother Katarina Štrucelj [~ — the 1894–1902 mother Katarina Straucelj/Straus — the SAME]; h36 = the 11th ENTRY — the KRIŽAN RETURN (1894/1896/1898/1902 Janez Križan × Katarina Straucelj → the 1904 Miše interlude → 1908 the SAME couple returns); godparents Matija Štraus + Marija Perdinec? [Pezdirec?] (the ŠTRAUS campaign); midwife Barbara Adlešič; signature Gregor Cerar; a later note [~ — + 1961?]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1908,
    scan: 197,
    page: 179,
    whatSi: "krščen Frančišek (rojstva 20. 11.; krsta pokrita s pripisom) — oče Franjo Kalan, učitelj [~ — »Fran. Kalan«], mati Marija Verhovnik? [~]; h90 = 5. VPIS — TRETJA UČITELJSKA DRUŽINA (1890/92 Kopitar uč. → 1898/1900 Vetročnik uč. → 1908 Kalan uč.! — hiša = učiteljski stan); VRZEL 8 LET; hišna forenzika: jasno 90 na OBOJIH dup skenih (na 197 pod belo nalepko); botra Jurij Pezdirec + Marija Županič ¼ zemlj (boter 3./3 v 1908); babica Ana Mavrenič; podpis Jos. Ravq; modri pripisi: poročen 28.11.1940 v Subotici? [~] + žena umrla 23.08.2001; žig FRIEDMANN (moderni)",
    whatEn: "baptized Frančišek (born Nov 20; the baptism covered by a note) — father Franjo Kalan, a teacher [~ — »Fran. Kalan«], mother Marija Verhovnik? [~]; h90 = the 5th ENTRY — the THIRD TEACHER FAMILY (1890/92 Kopitar → 1898/1900 Vetročnik → 1908 Kalan! — the house = the teacher's post); an 8-YEAR GAP; house forensics: clearly 90 on BOTH dup scans (under a white sticker on 197); godparents Jurij Pezdirec + Marija Županič (the godfather 3rd of 3 in 1908); midwife Ana Mavrenič; signature Jos. Ravq; blue notes: married Nov 28, 1940 in Subotica? [~] + the wife died Aug 23, 2001; the FRIEDMANN stamp (modern)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04105",
    year: 1908,
    scan: 199,
    page: 180,
    whatSi: "krščen Janez (26./27. 12.) — oče Janez Žumič ¼ zemljak, mati Marija Jakobčič [~ — 1905 mati Marija Jakofčič? — ISTA]; h11 = 5. VPIS ISTA familija — ŽUMIČ (1890 Zumik, 1905 Žumě?, 1907 Žumič); EMŠO č. 2612908500224 (26.12.1908 m — SKLADNO — sidro); botra Janez Adlešič + Neža Adlešič ½ zemlj; babica Marjeta Vötter — VRNITEV (1907: Vötter 0× na Gribljih; Sotter 1889 → Toter 1901–05 → Vötter 1906 → 1908 ISTA Marjeta? MERI); podpis Gregor Cerar; modri pripis: poročen 3.2.1931",
    whatEn: "baptized Janez (Dec 26/27) — father Janez Žumič, a quarter smallholder, mother Marija Jakobčič [~ — the 1905 mother Marija Jakofčič? — the SAME]; h11 = the 5th ENTRY the SAME family — ŽUMIČ (1890 Zumik, 1905 Žumě?, 1907 Žumič); personal ID 2612908500224 (Dec 26, 1908 m — CONSISTENT — an anchor); godparents Janez Adlešič + Neža Adlešič; midwife Marjeta Vötter — a RETURN (1907: Vötter 0× in Griblje; Sotter 1889 → Toter 1901–05 → Vötter 1906 → 1908 the SAME Marjeta? MERI); signature Gregor Cerar; blue note: married Feb 3, 1931",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04105",
    year: 1908,
    scan: 199,
    page: 180,
    whatSi: "krščen Matija (28./29. 12.) — ZADNJA vrstica 1908 (glava 1909 INLINE na r91 = isti sken!) — oče Janez Brinec ¼ zemljak, mati Ana Kure [~ — 1907 mati Ana Klepec? — MATI MENJAVA]; h10 = 4. VPIS (1897 NOVA, 1900 Grabrijan interlud, 1907 dvojčka = 3. → 1908 BRINEC ISTA); EMŠO č. 2812908500042 (28.12.1908 m — SKLADNO — sidro); botra Janez Muc, bajtar (= r31 h91 oče; CROSS-ROW 2× v 1908; cf. 1907 r85 botra Janez Muc kovač + Katarina Kure — ISTI BOTER PAR!) + Marija Kure ¼ zemlj; babica Barbara Adlešič; podpis Gregor Cerar; modri pripisi: poročen 14.5.1933 + umrl 20.04.1986 v Novem mestu",
    whatEn: "baptized Matija (Dec 28/29) — the LAST row of 1908 (the 1909 heading INLINE on r91 = the same scan!) — father Janez Brinec, a quarter smallholder, mother Ana Kure [~ — the 1907 mother Ana Klepec? — a MOTHER CHANGE]; h10 = the 4th ENTRY (1897 NEW, the 1900 Grabrijan interlude, the 1907 twins = the 3rd → 1908 the BRINEC SAME); personal ID 2812908500042 (Dec 28, 1908 m — CONSISTENT — an anchor); godparents Janez Muc, a cottager (= the r31 h91 father; a CROSS-ROW 2× in 1908; cf. the 1907 r85 godparents Janez Muc, a smith + Katarina Kure — the SAME GODPARENT COUPLE!) + Marija Kure; midwife Barbara Adlešič; signature Gregor Cerar; blue notes: married May 14, 1933 + died Apr 20, 1986 in Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "77",
    bookSignature: "04105",
    year: 1909,
    scan: 201,
    page: 181,
    whatSi: "krščen Alojzij (23./23. 1.) — oče Jurij Požek, bajtar, mati Katarina Veselič? [~]; h77 = 3. VPIS — POŽEK POVRAT po 19 LETIH (1890 Jurij Pošek/Požek bajtar × Katarina Šotter r. Križan → 1902 MENJAVA Nikolaj Cindrič cevljar → 1909 ISTI oče Jurij Požek bajtar vrne z NOVO ženo!); VRZEL 19 LET (najdaljša hišna vrzel 1909); mati menjava (Šotter → Veselič?); cf. P101 h21 = 6. VPIS POŽEK — Požek karusela h77→h21?→h77; hišna forenzika: jasno 77 (dve ločeni sedmici, zoom 5x); botra Marija Smec? + Barbara Krijan? ¼ gmůj; babica Marija Meh; podpis Gregor Cerar",
    whatEn: "baptized Alojzij (Jan 23/23) — father Jurij Požek, a cottager, mother Katarina Veselič? [~]; h77 = the 3rd ENTRY — the POŽEK RETURN after 19 YEARS (1890 Jurij Pošek/Požek, a cottager × Katarina Šotter b. Križan → 1902 the CHANGE Nikolaj Cindrič, a ropemaker → 1909 the SAME father Jurij Požek returns with a NEW wife!); a 19-YEAR GAP (the longest house gap of 1909); a mother change (Šotter → Veselič?); cf. P101 h21 = the 6th POŽEK entry — the Požek carousel h77→h21?→h77; house forensics: clearly 77 (two distinct sevens, 5x zoom); godparents Marija Smec? + Barbara Krijan?; midwife Marija Meh; signature Gregor Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04105",
    year: 1909,
    scan: 201,
    page: 181,
    whatSi: "krščen Anton (30./30. 1.) — oče Matija Brinec? ¼ zemljak, mati Marija Grabrijan [~ Grabrijan maj. Pezdire? — ISTA ZVEZA kot h30 1906 (Matija Brinec ½ × Marija Grabrijan)!]; h10 = 6. VPIS — SELITEV h30→h10 (1906 h30 = ISTA ZVEZA → 1909 v h10; h10 Brincova hiša: 1907 dvojčka Janez+Anton (Janez Brinec × Ana Klepec?) → 1908 Janez Brinec × Ana Kure → 1909 Matija Brinec × Marija Grabrijan — TRIJE Brincovi možje zapored!); EMŠO č. 3001909500735 (30.01.1909 m — SKLADNO — sidro); botra Janez Brinec + Ana Brinec ¼ zemlj; babica Barbara Adlešič; podpis Gregor Cerar; modri pripis: žena Brinec Glogovca? umrla 15.1.1982 v Metliki (MKU Metlika 1.1981, str. 243, zap. št. 85; Gradac 15.2.1982) + črni pripis umrl 1.12.1985 v Mariji Bori? [~]",
    whatEn: "baptized Anton (Jan 30/30) — father Matija Brinec? [~], a quarter smallholder, mother Marija Grabrijan [~ — the SAME COUPLE as h30 1906 (Matija Brinec ½ × Marija Grabrijan)!]; h10 = the 6th ENTRY — the MOVE h30→h10 (1906 h30 = the same couple → 1909 in h10; the Brinec house: the 1907 twins Janez+Anton (Janez Brinec × Ana Klepec?) → 1908 Janez Brinec × Ana Kure → 1909 Matija Brinec × Marija Grabrijan — THREE Brinec husbands in a row!); personal ID 3001909500735 (Jan 30, 1909 m — CONSISTENT — an anchor); godparents Janez Brinec + Ana Brinec; midwife Barbara Adlešič; signature Gregor Cerar; blue note: the wife Brinec Glogovca? died Jan 15, 1982 in Metlika (MKU Metlika 1.1981, p. 243, no. 85; Gradac Feb 15, 1982) + a black note died Dec 1, 1985 in Marija Bora? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "42",
    bookSignature: "04105",
    year: 1909,
    scan: 201,
    page: 181,
    whatSi: "krščena Jožefa (13./14. 4.) — oče Jurij Pezdirec ¼ zemljak, mati Katarina Jurajevič [~ — ISTA MATI kot 1905 (Jurij Perdinec?/Pezdirec × Katarina Jurajevič?) + 1906 (Jurasovič?) — ISTA ZVEZA VRNE]; h42 = 4. VPIS — PEZDIREC POVRAT (1904 NOVA Štraus? × Šimec → 1905 MENJAVA Jurij Perdinec?/Pezdirec × Katarina Jurajevič → 1906 Jožef Pozdirec/Pezdirec × Katarina Jurasovič → 1907–08 VRZEL → 1909 ISTA ZVEZA kot 1905!); hišna forenzika: jasno 42 (zoom-r17-left3; oče genetsko = 1905 Jurij!); botra Matija Meh + Katarina Pezdirec ¼ zemlj; babica Marija Meh; podpis Gregor Cerar; črni pripisi: mož umrl 1943 na Zabru? + vpisana v MK Kranj—Trbovlje 1951, št. 6, zap. št. 2 + umrla 26.4.1982 v Črnomlju; poročena 20.11.1938",
    whatEn: "baptized Jožefa (Apr 13/14) — father Jurij Pezdirec, a quarter smallholder, mother Katarina Jurajevič [~ — the SAME MOTHER as 1905 (Jurij Perdinec?/Pezdirec × Katarina Jurajevič?) + 1906 (Jurasovič?) — the SAME COUPLE RETURNS]; h42 = the 4th ENTRY — the PEZDIREC RETURN (1904 NEW Štraus? × Šimec → the 1905 CHANGE Jurij Perdinec?/Pezdirec × Katarina Jurajevič → 1906 Jožef Pozdirec/Pezdirec × Katarina Jurasovič → the 1907–08 GAP → 1909 the SAME COUPLE as 1905!); house forensics: clearly 42 (zoom-r17-left3; the father genetically = the 1905 Jurij!); godparents Matija Meh + Katarina Pezdirec; midwife Marija Meh; signature Gregor Cerar; black notes: the husband died 1943 na Zabru? + entered in the MK Kranj—Trbovlje 1951, no. 6, zap. 2 + died Apr 26, 1982 in Črnomelj; married Nov 20, 1938",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1909,
    scan: 202,
    page: 182,
    whatSi: "krščen Matija (18./18. 4.) — DVOJČEK 1/2 (r20+r21 — isti starši + ISTA BOTRA Nikolaj Segina + Katarina Šuštar na obeh vrsticah!) — oče Nikolaj Šulak? [~ Šulak/Šulek?] ¼ zemljak, mati Katarina Hlebecar? [~]; † 18/4. 09 (pencil — UMRL ISTI DAN kot rojstvo+krsta!); h34 = 6. VPIS (1887, 1899, 1903, 1905, 1906 → 1909; VRZEL 1907–08) — ŠIMEC/ŠULAK KARUSELA (1887 Šimec × Šmucelj → 1899–1905 Šilak/Šulak? → 1906 Janez Šimec POV RAT → 1909 Šulak? VRNE!); majhna svinčnica »N 29?« ob hišni št.; babica Marija Meh; podpis Gregor Cerar",
    whatEn: "baptized Matija (Apr 18/18) — TWIN 1/2 (r20+r21 — the same parents + the SAME GODPARENTS Nikolaj Segina + Katarina Šuštar on both rows!) — father Nikolaj Šulak? [~], a quarter smallholder, mother Katarina Hlebecar? [~]; died Apr 18, 1909 (pencil — DIED THE SAME DAY as the birth+december baptism!); h34 = the 6th ENTRY (1887, 1899, 1903, 1905, 1906 → 1909; the 1907–08 GAP) — the ŠIMEC/ŠULAK CAROUSEL (1887 Šimec × Šmucelj → 1899–1905 Šilak/Šulak? → 1906 Janez Šimec RETURNS → 1909 Šulak? RETURNS!); a small pencil mark »N 29?« by the house number; midwife Marija Meh; signature Gregor Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1909,
    scan: 202,
    page: 182,
    whatSi: "krščen Nikolaj (18./19. 4.) — DVOJČEK 2/2 (r21 po vzoru r20; rojen isti dan 18. 4., krščen naslednji dan; oče Nikolaj Šulak? + mati Katarina Hlebecar? — isti starši; botra Nikolaj Segina + Katarina Šuštar ¼ zemlj — ISTA; babica Marija Meh; podpis Gregor Cerar); † 3/4. 10. [~ — umrl kot dojenček oktobra 1909]; h34 2. vpis letos (NARE PRELOM — prva hišna ponovitev po 1907 h10 dvojčkih)",
    whatEn: "baptized Nikolaj (Apr 18/19) — TWIN 2/2 (r21 following r20; born the same day Apr 18, baptized the next day; father Nikolaj Šulak? + mother Katarina Hlebecar? — the same parents; godparents Nikolaj Segina + Katarina Šuštar — the SAME; midwife Marija Meh; signature Gregor Cerar); died Oct 3/4 [~ — died as an infant in October 1909]; h34 the 2nd entry this year (the NARE BREAK — the first intra-year house repeat after the 1907 h10 twins)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1909,
    scan: 203,
    page: 182,
    whatSi: "krščen Danijel (2.?/29.? 6. [~ — dan stolpci poškodovani; EMŠO 2.6.]) — oče Matija Straus? [~ Štravc/Štraus — ISTI OČE kot h72 1888–1895 (Matija Strauš!) + h42 1904 (Matija Štraus?)] ¼ zemljak, mati Marjeta Šimec [~ — MATI MENJAVA #3: 1888 Barbara Husič? → 1891–95 Marija Jakobič → 1904 (h42) + 1909 Marjeta Šimec]; h72 = 6. VPIS — STRAUŠ POVRAČNICA po 14 LETIH (1888–1895 Matija Strauš 5 vpisov v h72 → 1904 h42 interlude → 1909 DOMA v h72!); h42↔h72 ŠTRAUS↔PEZDIREC KARUSELJA (1904 Štraus v h42 → 1905 Pezdirec prevzame h42 → 1909 h42 = Pezdirec (r17) + h72 = Strauš (r28) — OBE familiji doma!); EMŠO č. 020609500254 (02.06.1909 m — sidro; prepog obojih dup 202/203: krsta »29.?« [~] — dvom); botra Jožef Štrucelj + Barbara Jakobič ¼ zemlj = ISTI BOTRA PAR kot h42 1904 (P89!); babica Katarina Štraus (ŠTRAUS mreža); podpis Gregor Cerar",
    whatEn: "baptized Danijel (Jun 2.?/29.? [~ — the day cells damaged; the ID says Jun 2]) — father Matija Straus? [~ — the SAME FATHER as h72 1888–1895 (Matija Strauš!) + h42 1904 (Matija Štraus?)], a quarter smallholder, mother Marjeta Šimec [~ — a MOTHER CHANGE #3: 1888 Barbara Husič? → 1891–95 Marija Jakobič → 1904 (h42) + 1909 Marjeta Šimec]; h72 = the 6th ENTRY — the STRAUŠ HOMECOMING after 14 YEARS (1888–1895 Matija Strauš, 5 entries in h72 → the 1904 h42 interlude → 1909 HOME in h72!); the h42↔h72 ŠTRAUS↔PEZDIREC CAROUSEL (1904 Štraus in h42 → 1905 Pezdirec takes h42 → 1909 h42 = Pezdirec (r17) + h72 = Strauš (r28) — BOTH families home!); personal ID 020609500254 (Jun 2, 1909 m — an anchor; a double check of both dups 202/203: the baptism »29.?« [~] — a doubt); godparents Jožef Štrucelj + Barbara Jakobič = the SAME GODPARENT COUPLE as h42 1904 (P89!); midwife Katarina Štraus (the ŠTRAUS network); signature Gregor Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04105",
    year: 1909,
    scan: 204,
    page: 183,
    whatSi: "krščena Katarina (3./4. 6.) — oče Martin Papič? [~ Tapič — Kurrent P/T] ½ zemljak (celica s 6 vrsticami drobnih opomb [~ — delno berljivo]), mati Marija Mlut? [~ Mut/Muh?]; h33 = 3. VPIS — MENJAVA DRUŽINE #3 (1889 Matija Brinec × Marija Dolenc → 1898 Matija Dehlič × Marija Rožek → 1909 Martin Papič? × Marija Mlut?); VRZEL 11 LET (1898→1909); VPIS PRENESEN V MRLIŠKI REGISTER (črni pripis ob imenu + modri pripis; EMŠO č. 0306095050335 — 03.06.1909 ž, SKLADNO — sidro); botra Mihael Papič? + Katarina Papič? (ISTI PRIIMEK kot oče!) ½ zemlj; babica Ana Mavrenič; podpis Gregor Cerar, coop. — COOP. zaznamovan (edini v 1909)",
    whatEn: "baptized Katarina (Jun 3/4) — father Martin Papič? [~ Tapič — the Kurrent P/T doubt], a half smallholder (the cell with 6 lines of small notes [~ — partly legible]), mother Marija Mlut? [~]; h33 = the 3rd ENTRY — a FAMILY CHANGE #3 (1889 Matija Brinec × Marija Dolenc → 1898 Matija Dehlič × Marija Rožek → 1909 Martin Papič? × Marija Mlut?); an 11-YEAR GAP (1898→1909); THE ENTRY TRANSFERRED TO THE DEATH REGISTER (a black note by the name + a blue note; personal ID 0306095050335 — Jun 3, 1909 f, CONSISTENT — an anchor); godparents Mihael Papič? + Katarina Papič? (the SAME SURNAME as the father!); midwife Ana Mavrenič; signature Gregor Cerar, coop. — the COOP. marked (the only one in 1909)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "63",
    bookSignature: "04105",
    year: 1909,
    scan: 205,
    page: 183,
    whatSi: "krščena Jožefa (12./12. 6.) — oče Janez Papič? [~ Tepič — ISTI priimek-dvom kot r30 oče Martin Papič?] ½ zemljak, mati Katarina Križan, »samka ½ zemljaka« [~ — SAMKA = neporočena/samo gospodinjstvo — MOŽEN NEZAKONSKI VPIS (stanu kolone nerazločne); KRIŽAN = h36 familija!]; h63 = 9. VPIS (1886–1903 8 vpisov → 1909; VRZEL 6 LET); MATI »SAMKA« — redki statusni zapis v vzorcu; nota »Matičar« pod hišno št.; hišna forenzika: jasno 63 (zoom 5x — 6+3); botra Anton Brodarič + Marija Milek? [~ Mlek/Meh] ¼; babica [neberljivo — cf. s204-A »Marija Meh« [~]]; podpis Gregor Cerar",
    whatEn: "baptized Jožefa (Jun 12/12) — father Janez Papič? [~ Tepič — the same surname-doubt as the r30 father Martin Papič?], a half smallholder, mother Katarina Križan, »samka ½ zemljaka« [~ — SAMKA = unmarried/alone household — a POSSIBLE ILLEGITIMATE ENTRY (the stanu columns unclear); KRIŽAN = the h36 family!]; h63 = the 9th ENTRY (1886–1903, 8 entries → 1909; a 6-YEAR GAP); the MOTHER »SAMKA« — a rare status record in the sample; the note »Matičar« under the house number; house forensics: clearly 63 (5x zoom — 6+3); godparents Anton Brodarič + Marija Milek? [~]; midwife [illegible — cf. s204-A »Marija Meh« [~]]; signature Gregor Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "54",
    bookSignature: "04105",
    year: 1909,
    scan: 205,
    page: 183,
    whatSi: "krščena Jožefa (26./26. 6.) — oče Janez Šimec ¼ zemljak, mati Marija Kure? [~ Hure/Kune — K/H paleografija; Kure = korpusna familija]; h54 = 6. VPIS (1886, 1897, 1900, 1901, 1904 → 1909; VRZEL 5 LET) — ŠIMEC NOVA DRUŽINA (h54 karusela: Pintec? → Brinec × Butala → Gruzec? × Butala → Župančič? × Vardjan? → Šimec × Kure?); ŠIMEC = P102 selitvena familija (h18→h13) + r57 mati Katarina Šimec; boter Ivan Požek = POŽEK signal (cf. r6 oče Jurij Požek h77!); botrinja Ana Brinec; babica Marija Meh; podpis Gregor Cerar; † 18.4.1978 v Črnomlju (MV Črnomelj 1.1978, ostr. 253, zap. št. 171; Gradac 9.4.1978); nota »Matičar — Simonič Nina«",
    whatEn: "baptized Jožefa (Jun 26/26) — father Janez Šimec, a quarter smallholder, mother Marija Kure? [~ — the K/H paleography; Kure = a corpus family]; h54 = the 6th ENTRY (1886, 1897, 1900, 1901, 1904 → 1909; a 5-YEAR GAP) — the ŠIMEC NEW FAMILY (the h54 carousel: Pintec? → Brinec × Butala → Gruzec? × Butala → Župančič? × Vardjan? → Šimec × Kure?); ŠIMEC = the P102 migrating family (h18→h13) + the r57 mother Katarina Šimec; the godfather Ivan Požek = the POŽEK signal (cf. the r6 father Jurij Požek h77!); the godmother Ana Brinec; midwife Marija Meh; signature Gregor Cerar; died Apr 18, 1978 in Črnomelj (MV Črnomelj 1.1978, p. 253, zap. 171; Gradac Apr 9, 1978); the note »Matičar — Simonič Nina«",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1909,
    scan: 205,
    page: 183,
    whatSi: "krščena Amalija (30./31. 6.) — oče Jurij Željko ¼ zemljak, mati Barbara Kure [~ — ISTA ZVEZA kot 1900 + 1905!]; h1 = 7. VPIS — ISTA ZVEZA 3. VPIS (1900 Anea? + 1905 Katarina + 1909 Amalija — Jurij Željko × Barbara Kure; 1888–96 Nikolaj Željko × Katarina Kure = prejšnja generacija ISTA hiša); † 5.5.1925 (pencil — umrla mlada, 15 let!); hiša 1 = NAJNIŽJA hiša vzorca; botra Jožef Željko (ŽELJKO signal — familija v isti hiši) + Barbara Vukas? ¼ zemlj; babica Marija Meh; podpis Gregor Cerar",
    whatEn: "baptized Amalija (Jun 30/31) — father Jurij Željko, a quarter smallholder, mother Barbara Kure [~ — the SAME COUPLE as 1900 + 1905!]; h1 = the 7th ENTRY — the SAME COUPLE's 3rd ENTRY (1900 Anea? + 1905 Katarina + 1909 Amalija — Jurij Željko × Barbara Kure; 1888–96 Nikolaj Željko × Katarina Kure = the previous generation of the SAME house); died May 5, 1925 (pencil — died young, 15!); house 1 = the LOWEST house number in the sample; the godfather Jožef Željko (the ŽELJKO signal — the family in the same house) + Barbara Vukas?; midwife Marija Meh; signature Gregor Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1909,
    scan: 205,
    page: 183,
    whatSi: "krščena Ana (12. 8.; krsta pokrita) — oče Jurij Jakobič? [~ Jakobčič] ¼ zemljak, mati Katarina Jakobič [~ — ISTA ZVEZA kot h6 1904 + 1905!]; h6 = 4. VPIS (1904, 1905, 1907 Kapucina? MENJAVA → 1909 ISTA ZVEZA VRNE; VRZEL 2 LETI) — HIŠA GENETSKO: hišna celica POKRITA z modrim pripisom (celica prazna/pokrita — forenzika 3x na obojih dup 204/205), starši = ISTA ZVEZA kot h6 1904+1905 + botrinja Marija Klepec = ISTA botrinja kot h6 1904/05 (Nikolaj Željko + Marija Klepec) — genetska rešitev h6; EMŠO č. 120809505944 [~ — zadnje številke razmazane] (12.08.1909 ž — SKLADNO — sidro); boter Jožef Čeliko? [~ Željko]; babica Marija Uri? [~]; podpis Jos. Rauq; modri pripis: poročena 8.11.1952 v Gradcu s Lešek Jožefom? + † 13.11.1999 v Metliki (MKU MO Metlika 1.1999)",
    whatEn: "baptized Ana (Aug 12; the baptism covered) — father Jurij Jakobič? [~ Jakobčič], a quarter smallholder, mother Katarina Jakobič [~ — the SAME COUPLE as h6 1904 + 1905!]; h6 = the 4th ENTRY (1904, 1905, the 1907 Kapucina? CHANGE → 1909 the SAME COUPLE RETURNS; a 2-YEAR GAP) — the HOUSE GENETICALLY: the house cell COVERED by a blue note (the cell empty/covered — forensics 3x on both dups 204/205), the parents = the SAME COUPLE as h6 1904+1905 + the godmother Marija Klepec = the SAME godmother as h6 1904/05 (Nikolaj Željko + Marija Klepec) — the genetic solution h6; personal ID 120809505944 [~ — the last digits smeared] (Aug 12, 1909 f — CONSISTENT — an anchor); the godfather Jožef Čeliko? [~ Željko]; midwife Marija Uri? [~]; signature Jos. Rauq; blue note: married Nov 8, 1952 in Gradac s Lešek Jožefom? + died Nov 13, 1999 in Metlika (MKU MO Metlika 1.1999)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1909,
    scan: 206,
    page: 184,
    whatSi: "krščena Ana (26./26. 7.) — oče Janez Brinec ¼ zemljak, mati Ana Mlek? [~ Meh/Milek]; h24 = 14. VPIS ZAPORED — NAJBOLJ VPISOVANA HIŠA REGISTRA še naprej (1887–1909 brez vrzeli); BRINCOVA hiša (oče Janez Brinec = ISTI oče kot h10 1907/1908!); botra Matija Brinec + Marija Brinec ¼ zemlja (BRINEC mreža — cf. r9 botra Janez+Ana Brinec); babica Marija Meh; podpis Jos. Rauq; EMŠO č. 26079095?5231 [~] (26.07.1909 ž — SKLADNO — sidro); MODRI+ČRNI pripisi: PONESREČI UMRLA 23.10.1965 pri božjani s šolskim kolektivom (MK Ljubljana 1.1965, ostr. 6, št. 1711; matica črnilo ime z 16.10.1965; Gradac 12.1965) + umrla 30.10.1988 v Celovcu? [~] (MRK MO Metlika 1.1988) — dvojna smrtna pripisa",
    whatEn: "baptized Ana (Jul 26/26) — father Janez Brinec, a quarter smallholder, mother Ana Mlek? [~]; h24 = the 14th CONSECUTIVE ENTRY — the MOST-ENTERED HOUSE of the register continues (1887–1909 without a gap); the BRINEC house (the father Janez Brinec = the SAME father as h10 1907/1908!); godparents Matija Brinec + Marija Brinec (the BRINEC network — cf. the r9 godparents Janez+Ana Brinec); midwife Marija Meh; signature Jos. Rauq; personal ID 26079095?5231 [~] (Jul 26, 1909 f — CONSISTENT — an anchor); BLUE+BLACK notes: SHE DIED IN AN ACCIDENT Oct 23, 1965 during a pilgrimage with a school group (MK Ljubljana 1.1965, p. 6, no. 1711; the register inked the name from Oct 16, 1965; Gradac Dec 1965) + died Oct 30, 1988 in Celovec? [~] (MRK MO Metlika 1.1988) — a double death note",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1909,
    scan: 207,
    page: 185,
    whatSi: "krščen Frančišek (16./19. 9.) — oče France Martinovič? [~ Martinkovič/Martin kovač — NOV priimek v vzorcu] ½ zemljak, mati Katarina Šimec (ŠIMEC — cf. r35 oče Janez Šimec h54!); h30 = 12. VPIS — 7. DRUŽINA v h30 (Milek 1890–91 → Jakljevič 1893 → Šegina 1895–96 → Županič? 1899 → Segina 1902–03 → Brinec 1906 → Segina 1908 → Martinovič? 1909!); hišna forenzika: jasno 30 na OBOJIH dup 207/208 (zoom 7x — 3+0, ni 36/50); botra Janez Žugelj + Marjeta Žugelj ½ zemlj; babica Ana Novak; podpis Jos. Rauq; † 25.6.1943 um. Pako? [~]",
    whatEn: "baptized Frančišek (Sep 16/19) — father France Martinovič? [~ — a NEW surname in the sample], a half smallholder, mother Katarina Šimec (ŠIMEC — cf. the r35 father Janez Šimec h54!); h30 = the 12th ENTRY — the 7th FAMILY in h30 (Milek 1890–91 → Jakljevič 1893 → Šegina 1895–96 → Županič? 1899 → Segina 1902–03 → Brinec 1906 → Segina 1908 → Martinovič? 1909!); house forensics: clearly 30 on BOTH dups 207/208 (7x zoom — 3+0, not 36/50); godparents Janez Žugelj + Marjeta Žugelj; midwife Ana Novak; signature Jos. Rauq; died Jun 25, 1943 um. Pako? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1909,
    scan: 207,
    page: 185,
    whatSi: "krščena Ana (21./24. 9.) — oče Janez Drgoš [~ — NOV priimek; cf. 1910 r3 boter Ivan Drgoš?] ¼ zemljak, mati Barbara Cvitkovič; h12 = 12. VPIS (1892–1907 11 vpisov → 1909; VRZEL 1908) — ISTA ZVEZA (1907 Janez Dragoš × Barbara Cvitkovič = 1909 Drgoš × Cvitkovič — Kurrent variante ISTEGA para!); VÖTTER DVOJNO: babica Marjeta Vötter + botrinja Katarina Vötter (isti zapis; Vötter/Toter/Sotter MERI linija); boter Matija Štrucelj (ŠTRUCELJ — cf. 1910 r3 oče Matija Štrucelj h5!) ½ gmůj; podpis Jos. Rauq; nota: VPisana v MMK Ljubljana 1.1978? + modri pripis umrla 5.4.1981 v Otokih? [~] + † 15.1.1943 mu Pako? [~ — dva pripisa]",
    whatEn: "baptized Ana (Sep 21/24) — father Janez Drgoš [~ — a NEW surname; cf. the 1910 r3 godfather Ivan Drgoš?], a quarter smallholder, mother Barbara Cvitkovič; h12 = the 12th ENTRY (1892–1907, 11 entries → 1909; the 1908 GAP) — the SAME COUPLE (the 1907 Janez Dragoš × Barbara Cvitkovič = the 1909 Drgoš × Cvitkovič — Kurrent variants of the SAME couple!); the VÖTTER DOUBLE: the midwife Marjeta Vötter + the godmother Katarina Vötter (the same record; the Vötter/Toter/Sotter MERI line); the godfather Matija Štrucelj (ŠTRUCELJ — cf. the 1910 r3 father Matija Štrucelj h5!); signature Jos. Rauq; the note: entered in the MMK Ljubljana 1.1978? + a blue note died Apr 5, 1981 v Otokih? [~] + died Jan 15, 1943 mu Pako? [~ — two notes]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04105",
    year: 1909,
    scan: 208,
    page: 185,
    whatSi: "krščen Jožef (24./24. 9.) — oče Jožef Pezdirec, bajtar, mati Ana [PRIIMEK NEZAPISAN — anomalija; GENETSKO = Ana Hrižan, ISTA MATI kot h35 1906 (Jožef Pozdirec/Pezdirec × Ana Hrižan)!]; h35 = 6. VPIS (1887, 1889, 1890, 1903, 1906 → 1909; VRZEL 1907–08) — ISTA ZVEZA (oče Jožef Pozdirec/Pezdirec 1906 = Jožef Pezdirec bajtar 1909; mati Ana Hrižan 1906 = »Ana« brez priimka 1909!); MATI BREZ PRIIMKA — edini tak vpis v vzorcu (genetsko rešen = Hrižan); botra Matija Meh + Marija Šuštar ¼ zemlj (MEH — cf. r61/r64 babica + h32 oče!); babica Marija Meh; podpis Jos. Rauq",
    whatEn: "baptized Jožef (Sep 24/24) — father Jožef Pezdirec, a cottager, mother Ana [THE SURNAME NOT RECORDED — an anomaly; GENETICALLY = Ana Hrižan, the SAME MOTHER as h35 1906 (Jožef Pozdirec/Pezdirec × Ana Hrižan)!]; h35 = the 6th ENTRY (1887, 1889, 1890, 1903, 1906 → 1909; the 1907–08 GAP) — the SAME COUPLE (the father Jožef Pozdirec/Pezdirec 1906 = Jožef Pezdirec the cottager 1909; the mother Ana Hrižan 1906 = »Ana« without a surname 1909!); THE MOTHER WITHOUT A SURNAME — the only such entry in the sample (genetically resolved = Hrižan); godparents Matija Meh + Marija Šuštar (MEH — cf. the r61/r64 midwife + the h32 father!); midwife Marija Meh; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1909,
    scan: 208,
    page: 185,
    whatSi: "krščena Jožefa (29./30. 9.) — oče Matija Meh [~ — ISTI oče-kot-branja kot h32 1893 »Meh/Mrh?« + 1900 »Meh«; 1889–98 večinoma Urh/Urk — Meh/UrH Kurrent dvom rešen kot Meh] ¼ zemljak, mati Marjeta Pezdirec [~ Pendirec/Perdinec — ISTA MATI kot 1889–1895!]; h32 = 10. VPIS (1889–1903 8 vpisov → 1909; VRZEL 6 LET 1904–08) — ISTA ZVEZA (Meh × Pezdirec = 1889/90/92/93/95 variante ISTEGA para); botra Jožef Pezdirec + Marija Meh ¼ zemlj; babica Marija Meh; podpis [podpis v koloni = Paulin Bitenc — MATICARKA nota ob smrtnem pripisu; izvirni duhovniški podpis pokrit/nezapisan]; poročena 1.2.1936; † 15.11.1952 v Kostanjevici? (strip: »Umrła dne 15.11.1952 … 57.39« + maticarka Paulin Bitenc); NOVELA: podpis-kolono od r61 dalje pogosto prevzame maticarka Paulina Bitenc",
    whatEn: "baptized Jožefa (Sep 29/30) — father Matija Meh [~ — the SAME father-as-read as h32 1893 »Meh/Mrh?« + 1900 »Meh«; 1889–98 mostly Urh/Urk — the Meh/UrH Kurrent doubt resolved as Meh], a quarter smallholder, mother Marjeta Pezdirec [~ — the SAME MOTHER as 1889–1895!]; h32 = the 10th ENTRY (1889–1903, 8 entries → 1909; a 6-YEAR GAP 1904–08) — the SAME COUPLE (Meh × Pezdirec = the 1889/90/92/93/95 variants of the SAME couple); godparents Jožef Pezdirec + Marija Meh; midwife Marija Meh; signature [the signature column = Paulin Bitenc — the REGISTRAR's note by a death annotation; the original priest's signature covered/unrecorded]; married Feb 1, 1936; died Nov 15, 1952 v Kostanjevici? (a strip: »Umrła dne 15.11.1952 … 57.39« + the registrar Paulin Bitenc); a NOVELTY: from r61 on the signature column is often taken over by the registrar Paulina Bitenc",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1909,
    scan: 208,
    page: 185,
    whatSi: "krščena Jožefa (18./19. 10.) — oče Jurij Pezdirec ¼ zemljak, mati Katarina Benkovec? [~ Bertovec/Benkovec]; h48 = 4. VPIS (1898, 1905, 1907 → 1909); EMŠO č. 1910909505186 (19.10.1909 ž) — ANOMALIJA: EMŠO datum = KRSTNI datum (19.10), register piše rojstvo 18.10 — maticar je uporabil krstni datum (edinski tak primer v vzorcu); botra Nikolaj Brodarič + Cvetlja? Pezdirec? [~ Cvetelja/Varolja] ¼ zemlj; babica Marija Meh; podpis Jos. Rauq; modri pripis: poročin 22.1.1933 KLEPEC — MOŽ UMRL + Črnomelj št. 60-14/1961 z dne 15.3.1961 + priimek Weiss? vdanl wajen? [~] + † 25.4.1959 v mestu Metlika (MKU MO Metlika 1.1959, ostr. 31, zap. št. 175; obnova 06.10.2002)",
    whatEn: "baptized Jožefa (Oct 18/19) — father Jurij Pezdirec, a quarter smallholder, mother Katarina Benkovec? [~]; h48 = the 4th ENTRY (1898, 1905, 1907 → 1909); personal ID 1910909505186 (Oct 19, 1909 f) — an ANOMALY: the ID date = the BAPTISM date (Oct 19), the register says the birth Oct 18 — the registrar used the baptism date (the only such case in the sample); godparents Nikolaj Brodarič + Cvetlja? Pezdirec? [~]; midwife Marija Meh; signature Jos. Rauq; blue note: married Jan 22, 1933 KLEPEC — the HUSBAND DIED + Črnomelj no. 60-14/1961 of Mar 15, 1961 + the surname Weiss? vdanl wajen? [~] + died Apr 25, 1959 in the town Metlika (MKU MO Metlika 1.1959, p. 31, zap. 175; a renewal Oct 6, 2002)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "66",
    bookSignature: "04105",
    year: 1909,
    scan: 210,
    page: 186,
    whatSi: "krščena Marija (5./6. 10.) — oče Jakob Bohte [~ — NOV priimek v Gribljih] ¼ zemljak, mati Katarina Križan (KRIŽAN — h36 familija; cf. r32 mati Katarina Križan!); h66 = 4. VPIS (1887, 1904, 1905 → 1909; VRZEL 4 LETE) — ISTI OČE (1905 Jakob Bohle?/Boble × Katarina Hrižan? = 1909 Jakob Bohte × Katarina Križan — Kurrent variante ISTEGA očeta + MATI MENJAVA!); hišna forenzika: jasno 66 (zoom 5x — DVE ŠESTERKI; prva branja »22«/»72« NAPAČNA); boter Nikolaj Brodarič = ISTI BOTER kot r64 (2× v 1909 — CROSS-ROW) + botrinja Marija Straus (ŠTRAUS mreža) ¼ zemlj; babica Marija Meh; podpis [podpis v koloni = Paulin Bitenc — maticarka nota]; EMŠO č. 051090505628 [~ — 12-mestni zapis, morda 0510909505628] (05.10.1909 ž — SKLADNO — sidro); modri pripis: umrla 30.08.1994 v Gribljah (MKU MO Metlika 1.1994, str. 189, zap. št. 64; Metlika 23.9.1994)",
    whatEn: "baptized Marija (Oct 5/6) — father Jakob Bohte [~ — a NEW surname in Griblje], a quarter smallholder, mother Katarina Križan (KRIŽAN — the h36 family; cf. the r32 mother Katarina Križan!); h66 = the 4th ENTRY (1887, 1904, 1905 → 1909; a 4-YEAR GAP) — the SAME FATHER (the 1905 Jakob Bohle?/Boble × Katarina Hrižan? = the 1909 Jakob Bohte × Katarina Križan — a Kurrent variant of the SAME father + a MOTHER CHANGE!); house forensics: clearly 66 (5x zoom — TWO SIXES; the first readings »22«/»72« WRONG); the godfather Nikolaj Brodarič = the SAME GODFATHER as r64 (2× in 1909 — a CROSS-ROW) + the godmother Marija Straus (the ŠTRAUS network); midwife Marija Meh; signature [the signature column = Paulin Bitenc — the registrar's note]; personal ID 051090505628 [~ — a 12-digit record, perhaps 0510909505628] (Oct 5, 1909 f — CONSISTENT — an anchor); blue note: died Aug 30, 1994 in Griblje (MKU MO Metlika 1.1994, p. 189, zap. 64; Metlika Sep 23, 1994)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1910,
    scan: 211,
    page: 187,
    whatSi: "krščena [ime neberljivo — Kurrent »?exa«: L/T + e + x/ž + a; P104 lead je ugibal »Jožefa« — NAPAČNA ugiba, cf. r29 Jožefa drugačne oblike] (8./9. 1.) — oče Matija Štrucelj ¾ zemljak, mati Marija Meh; h5 = 5. VPIS (1891 Jožefa, 1903 Matija, 1905 Ana, 1907 Marija → 1910 — ISTA družina Štrucelj × Meh 5. skupaj!); VRZEL 3 LETA; botra Ivan Dragos ¾ zemljak + Antonija Toter; babica Marjeta Toter; podpis Laulin Bitnar [~ — NOV PODPIS 1910]; EMŠO ž 0801910505931 (SKLADNO — sidro); modri pripis: umrla dne 19.11.1983 v Gribljah (MMS mrliška 1983, ob. 129, št. 9, 19.12.1983); ime: kapitalka = ISTA oblika kot »L« v podpisih (zanka + spuščaj levo), brez prečke = ni T",
    whatEn: "baptized [name illegible — Kurrent »?exa«: L/T + e + x/ž + a; the P104 lead guessed »Jožefa« — a WRONG guess, cf. r29 Jožefa with different letterforms] (Jan 8/9) — father Matija Štrucelj, a three-quarter smallholder, mother Marija Meh; h5 = the 5th ENTRY (1891 Jožefa, 1903 Matija, 1905 Ana, 1907 Marija → 1910 — the SAME Štrucelj × Meh family, the 5th time!); a 3-YEAR GAP; godparents Ivan Dragos + Antonija Toter; midwife Marjeta Toter; signature Laulin Bitnar [~ — a NEW SIGNATURE of 1910]; personal ID 0801910505931 (CONSISTENT — an anchor); blue note: died Nov 19, 1983 in Griblje (MMS death register 1983, p. 129, no. 9; Dec 19, 1983); the name: the capital = the SAME shape as the »L« in the Laulin Bitnar signatures (a top loop + a left descender), no crossbar = not T",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1910,
    scan: 211,
    page: 187,
    whatSi: "krščen Jožef (15./16. 1.) — oče Peter Strmec? [~ — robovi natrgani], mati Ana Rutala? [~]; h88 = 2. VPIS (1904 Jožefa — Peter Brinec? bajtar × Alma Šecalja? → 1910; genetsko drugačna družina ALI napake berjanja na natrganem robu); VRZEL 6 LET; spodnji rob str. 187 NATRGAN — starševska/botrinjska/podpisna celica delno manjkajo; poroka dne 23.11.1938 v Reginci? [~]; botra Matija Brinec? [~] + Ana Brinec? [~]; babica Meh [~ — samo priimek]; podpis Jos. Rauq [~ — bled]; forenzika 88 (dve osmici, zoom)",
    whatEn: "baptized Jožef (Jan 15/16) — father Peter Strmec? [~ — torn edges], mother Ana Rutala? [~]; h88 = the 2nd ENTRY (1904 Jožefa — Peter Brinec? a cottager × Alma Šecalja? → 1910; genetically a different family OR reading errors on the torn edge); a 6-YEAR GAP; the bottom edge of p. 187 TORN — the parents'/godmother's/signature cells partly missing; married Nov 23, 1938 at Reginci? [~]; godparents Matija Brinec? + Ana Brinec?; midwife Meh [~ — surname only]; signature Jos. Rauq [~ — faded]; forensics 88 (two eights, zoom)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "29",
    bookSignature: "04105",
    year: 1910,
    scan: 212,
    page: 188,
    whatSi: "krščen Anton (17./18. 2.) — očetova celica PRAZNA (NEZAKONSKI), mati Barbara Milek, sama, dojka? [~], ¼ zemlj., brez; h29 = 4. VPIS — VRZEL 15 LET (1888 Marjeta + 1892 Marija — Peter Milek × Ana Križan; 1895 Marija — Kuhar?/Kuklar? intermezzo → 1910); GENETIKA: mati Barbara MILEK = h29 Milekova familija (1888/1892 Peter Milek!); botra Jakob Bohte ½ zemljak + Katarina Milek (MILEK mreža); babica Marija Meh; podpis Jos. Rauq",
    whatEn: "baptized Anton (Feb 17/18) — the father's cell EMPTY (ILLEGITIMATE), mother Barbara Milek, alone, a day-girl? [~], a quarter smallholder, without; h29 = the 4th ENTRY — a 15-YEAR GAP (1888 Marjeta + 1892 Marija — Peter Milek × Ana Križan; 1895 Marija — a Kuhar?/Kuklar? interlude → 1910); GENETICS: the mother Barbara MILEK = the h29 Milek family (1888/1892 Peter Milek!); godparents Jakob Bohte + Katarina Milek (the MILEK network); midwife Marija Meh; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04105",
    year: 1910,
    scan: 212,
    page: 188,
    whatSi: "krščena Neža (7./7. 3.) — oče Matija Šimec ¾ zemljak, mati Marija Kambič; h18 = 4. VPIS — POVRAT Šimec × Kambič (1898 Janez — Matija Šimec × Ana Kukar; 1906 Alojzij — Matija × Marija Kambič; 1907 intermezzo Peter Brinec × Ana Butala → 1910 ISTI PAR kot 1906!); botra Janez Muc ¾ zemljak? + Ana Kambič; babica Marija Meh; podpis Jos. Rauq; EMŠO ž 0703910505638 (SKLADNO — sidro); VPIS PRENEŠEN v register dna: 23.06.2003, matičarka [~ neberljivo — »Bela Janovič?«]",
    whatEn: "baptized Neža (Mar 7/7) — father Matija Šimec, a three-quarter smallholder, mother Marija Kambič; h18 = the 4th ENTRY — the Šimec × Kambič COUPLE RETURNS (1898 Janez — Matija Šimec × Ana Kukar; 1906 Alojzij — Matija × Marija Kambič; a 1907 interlude Peter Brinec × Ana Butala → 1910 the SAME COUPLE as 1906!); godparents Janez Muc + Ana Kambič; midwife Marija Meh; signature Jos. Rauq; personal ID 0703910505638 (CONSISTENT — an anchor); THE ENTRY TRANSFERRED to the register on Jun 23, 2003, the registrar [~ illegible — »Bela Janovič?«]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1910,
    scan: 213,
    page: 189,
    whatSi: "krščen Jožef (4./9. 3. — rojstva po EMŠO) — oče Jožef Štrucelj ¾ zemljak, mati Barbara Trence; h44 = 5. VPIS (1888 Hlevič, 1901 Jurajevič, 1906 Anton, 1908 Ana → 1910 — oče Jožef Štrucelj 3. skupaj zapored 1906/08/10!); v PT luкnji 41–60; botra Janez Hrižan ¾ zemljak? + Doroteja Fecimonvič? [~]; babica Marija Meh; podpis Laulin Bitnar [~]; EMŠO k 0403910500260 (SKLADNO — sidro; rojstva 4. Marec → branje rojstev »9« = NAPAČNO, Kurrent 4/9); modri pripisi: umrla dne 15.02.2004 Novo mesto (žena Cvetka Bole, poroka 5.10.1978; matičarka 20.04.2004)",
    whatEn: "baptized Jožef (Mar 4/9 — the birth per the personal ID) — father Jožef Štrucelj, a three-quarter smallholder, mother Barbara Trence; h44 = the 5th ENTRY (1888 Hlevič, 1901 Jurajevič, 1906 Anton, 1908 Ana → 1910 — the father Jožef Štrucelj the 3rd time in a row 1906/08/10!); in the PT gap 41–60; godparents Janez Hrižan + Doroteja Fecimonvič? [~]; midwife Marija Meh; signature Laulin Bitnar [~]; personal ID 0403910500260 (CONSISTENT — an anchor; the birth Mar 4 → the reading of the birth column »9« WRONG, a Kurrent 4/9); blue notes: died Feb 15, 2004 in Novo mesto (wife Cvetka Bole, married Oct 5, 1978)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1910,
    scan: 213,
    page: 189,
    whatSi: "krščen Jožef (24./25. 3.) — oče Nikolaj Šulak? [~ — prvotno branje »Vidak«; GENETSKO = h34 1909 ISTI oče Nikolaj Šulak? — celica pod lepilnim trakom], mati Katarina Hlebecar? [~ — »Hlobuec?.va«; GENETSKO = h34 1909 ISTI]; h34 = 8. VPIS (1887 Janez, 1899 Marija, 1903 Katarina, 1905 Ana, 1906 Nikolaj, 1909 DVOJČKI Matija+Nikolaj → 1910) — TRETJE leto zapored (1909/1910/1911 lead!); ISTI BOTER Nikolaj Segina 3. skupaj (1909 dvojčki ×2 + 1910!) — SEGINA mreža (h30); botrinja Katarina Hrižan? [~ — »Hrižarne«]; babica Marija Meh; podpis Laulin Bitnar [~]; † 30.10.1963 v Gribljah št. 73 (maticar Trvižan? Tomaž) — umrl v hiši 73!",
    whatEn: "baptized Jožef (Mar 24/25) — father Nikolaj Šulak? [~ — the first reading »Vidak«; GENETICALLY = the h34 1909 SAME father Nikolaj Šulak? — the cell under adhesive tape], mother Katarina Hlebecar? [~ — »Hlobuec?.va«; GENETICALLY = the h34 1909 SAME]; h34 = the 8th ENTRY (1887 Janez, 1899 Marija, 1903 Katarina, 1905 Ana, 1906 Nikolaj, the 1909 TWINS Matija+Nikolaj → 1910) — the THIRD consecutive year (1909/1910/the 1911 lead!); the SAME GODFATHER Nikolaj Segina the 3rd time (1909 twins ×2 + 1910!) — the SEGINA network (h30); the godmother Katarina Hrižan? [~]; midwife Marija Meh; signature Laulin Bitnar [~]; died Oct 30, 1963 in Griblje no. 73 — died in house 73!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1910,
    scan: 214,
    page: 190,
    whatSi: "krščena Ivana (21./22. 4.) — oče Nikolaj Željko [~ — branje »Kolehko«; GENETSKO = h60 Nikolaj Željko 1893–1908], mati Marija Brodarič; h60 = 9. VPIS (1893, 1894, 1897, 1899, 1904 Novak intermezzo, 1906, 1908 → 1910 — Željko × Brodarič 7. skupaj!); v PT luкnji 41–60 (meja); botra Marko Brozdinec? [~] ¾ zemljak + Marija Klepec (KLEPEC mreža); babica Marija Meh; podpis Laulin Bitnar [~]; VPIS PRENEŠEN v matični register dna: 23.05.2001, matičarka [~ neberljivo]",
    whatEn: "baptized Ivana (Apr 21/22) — father Nikolaj Željko [~ — the reading »Kolehko«; GENETICALLY = the h60 Nikolaj Željko 1893–1908], mother Marija Brodarič; h60 = the 9th ENTRY (1893, 1894, 1897, 1899, a 1904 Novak interlude, 1906, 1908 → 1910 — Željko × Brodarič the 7th time!); in the PT gap 41–60 (the boundary); godparents Marko Brozdinec? + Marija Klepec (the KLEPEC network); midwife Marija Meh; signature Laulin Bitnar [~]; THE ENTRY TRANSFERRED to the civil register on May 23, 2001",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1910,
    scan: 214,
    page: 190,
    whatSi: "krščen Vincencij (25./26. 4.) — oče Gregor Kalan, učitelj, mati Marija Vrhovnik; h90 = 6. VPIS — UČITELJSKA HIŠA (1890/1892 Kopitar → 1898/1900 Vetročnik → 1908 Frančišek Kalan → 1910 Vincencij Kalan — 2. Kalanov otrok, 4. učiteljska družina v hiši!); botra Jurij Šupanič? [~] ¾ zemljak + Marija Šupanič? [~]; babica Ana Mavrenič; podpis Laulin Bitnar [~]; † 19.10.1910 (dojenček, 6 mesecev); CROSS-ROW: r72 botrinja »Marija Kalan učiteljeva žena« = ISTA oseba (Kalanova žena iz h90!) — botrinja iz ISTOLETNEga vpisa",
    whatEn: "baptized Vincencij (Apr 25/26) — father Gregor Kalan, a teacher, mother Marija Vrhovnik; h90 = the 6th ENTRY — THE TEACHER HOUSE (1890/1892 Kopitar → 1898/1900 Vetročnik → 1908 Frančišek Kalan → 1910 Vincencij Kalan — Kalan's 2nd child, the 4th teacher family in the house!); godparents Jurij Šupanič? + Marija Šupanič? [~]; midwife Ana Mavrenič; signature Laulin Bitnar [~]; died Oct 19, 1910 (an infant, 6 months); CROSS-ROW: the r72 godmother »Marija Kalan, the teacher's wife« = the SAME person (Kalan's wife from h90!) — a godmother from the SAME-YEAR entry",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1910,
    scan: 214,
    page: 190,
    whatSi: "krščen Anton (23./23. 5.) — oče Kazimir? Požek [~ — natrgani rob, berljivo samo »…mir/…mer«; GENETSKA HIPOTEZA: h21 1888 nezakonski »Kaxmarp« (Kasimir/Kazimir?) POVRAT kot oče; ALI isti Janez 1887–1906], mati Katarina Kure [~ — MATI MENJANA: 1893–1906 Ana Šimec]; h21 = 7. VPIS (1887 Nikolaj, 1888 »Kaxmarp« nezakonski, 1893, 1899, 1904 Cindrič intermezzo, 1906 → 1910); POŽEK mreža: h21 (Janez) + h77 (Jurij) + boter Ivan Požek r47; mati Katarina KURE = KURE mreža (h91 Ana Kure / h1 Barbara Kure); botra Janez Šukan? [~] ¾ zemljak + Marija Šimec; babica Marija Meh [~]; podpis Jos. Rauq; + 13.7.1928 (umrl pri 18)",
    whatEn: "baptized Anton (May 23/23) — father Kazimir? Požek [~ — a torn edge, only »…mir/…mer« legible; the GENETIC HYPOTHESIS: the h21 1888 illegitimate »Kaxmarp« (Kasimir/Kazimir?) RETURNS as the father; OR the same Janez 1887–1906], mother Katarina Kure [~ — a MOTHER CHANGE: 1893–1906 Ana Šimec]; h21 = the 7th ENTRY (1887 Nikolaj, the 1888 illegitimate »Kaxmarp«, 1893, 1899, a 1904 Cindrič interlude, 1906 → 1910); the POŽEK network: h21 (Janez) + h77 (Jurij) + the godfather Ivan Požek r47; the mother Katarina KURE = the KURE network (h91 Ana Kure / h1 Barbara Kure); godparents Janez Šukan? + Marija Šimec; midwife Marija Meh [~]; signature Jos. Rauq; died Jul 13, 1928 (aged 18)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "35",
    bookSignature: "04105",
    year: 1910,
    scan: 214,
    page: 190,
    whatSi: "krščen Alojzij (1./1. 6.) — oče Peter Kraj? [~] ¾ zemljak, mati Barbara Križan? [~ — Hrižan?; 1906/1909 mati = Ana (genetsko Hrižan) — MATI MENJAVA ali priimek menjava]; h35 = 7. VPIS (1887 anomaliya, 1889, 1890, 1903, 1906, 1909 → 1910); forenzika 35 (prvo branje »85« NAPAČNO — zoom: jasno 35); babica PRAZNA (—) — redko!; botra Nikolaj? Kraj? [~] + Ana Kraj ¾ zemlj. (KRAJ mreža: cf. 1911 r1 Begunja vas Peter Kraj!); podpis Laulin Bitnar [~]; + 26/6.1910 (dojenček, ~3 tedne)",
    whatEn: "baptized Alojzij (Jun 1/1) — father Peter Kraj? [~], a three-quarter smallholder, mother Barbara Križan? [~ — Hrižan?; the 1906/1909 mother = Ana (genetically Hrižan) — a MOTHER CHANGE or a surname change]; h35 = the 7th ENTRY (an 1887 anomaly, 1889, 1890, 1903, 1906, 1909 → 1910); forensics 35 (the first reading »85« WRONG — zoom: clearly 35); THE MIDWIFE EMPTY (—) — rare!; godparents Nikolaj? Kraj? + Ana Kraj (the KRAJ network: cf. the 1911 r1 Begunja vas Peter Kraj!); signature Laulin Bitnar [~]; died Jun 26, 1910 (an infant, ~3 weeks)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1910,
    scan: 215,
    page: 191,
    whatSi: "krščena Jožefa (25./26. 6.) — oče Nikolaj Milek ¾ zemljak, mati Ana Žurrič? [~ — 1904 branje »Žunič« — ISTA oseba]; h22 = 5. VPIS (1899 Marija — × Marija Klepec; 1902 Alojzij, 1904 Ana, 1905 Mihael → 1910 — oče Nikolaj Milek ISTI 5×!); forenzika 22 (prvo branje »23« NAPAČNO); botra Ivan Požek, bajtar + Katar. Križan? [~] (POŽEK signal — cf. P104 r35 h54 boter Ivan Požek); babica Marija Meh; podpis Jos. Rauq; EMŠO ž 2506910505074 (SKLADNO — sidro); † 8.3.1974 Črnomelj (poroka 3.8.1936)",
    whatEn: "baptized Jožefa (Jun 25/26) — father Nikolaj Milek, a three-quarter smallholder, mother Ana Žurrič? [~ — the 1904 reading »Žunič« — the SAME person]; h22 = the 5th ENTRY (1899 Marija — × Marija Klepec; 1902 Alojzij, 1904 Ana, 1905 Mihael → 1910 — the father Nikolaj Milek the SAME 5×!); forensics 22 (the first reading »23« WRONG); godparents Ivan Požek, a cottager + Katar. Križan? [~] (the POŽEK signal — cf. the P104 r35 h54 godfather Ivan Požek); midwife Marija Meh; signature Jos. Rauq; personal ID 2506910505074 (CONSISTENT — an anchor); died Mar 8, 1974 Črnomelj (married Aug 3, 1936)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "91",
    bookSignature: "04105",
    year: 1910,
    scan: 215,
    page: 191,
    whatSi: "krščen Alojzij (26./26. 6.) — oče Matija Muc? [~ — OČE MENJAVA: 1895–1908 Janez Muc bajtar → 1910 Matija Muc bajtar (brat/sin?)], mati Ana Kure; h91 = 6. VPIS (1893 Novak, 1895 Muc, 1902, 1904, 1908 → 1910); mati Ana Kure ISTA 6×!; botra Jurij Jakofčič ¾ zemljak (h6 oče — CROSS-ROW!) + Marija Šimec; babica Marija Meh; podpis Laulin Bitnar [~]; + 18/9.1910 (dojenček)",
    whatEn: "baptized Alojzij (Jun 26/26) — father Matija Muc? [~ — a FATHER CHANGE: 1895–1908 Janez Muc, a cottager → 1910 Matija Muc, a cottager (a brother/son?)], mother Ana Kure; h91 = the 6th ENTRY (1893 Novak, 1895 Muc, 1902, 1904, 1908 → 1910); the mother Ana Kure the SAME 6×!; godparents Jurij Jakofčič (the h6 father — a CROSS-ROW!) + Marija Šimec; midwife Marija Meh; signature Laulin Bitnar [~]; died Sep 18, 1910 (an infant)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1910,
    scan: 215,
    page: 191,
    whatSi: "krščena Marija (18./20. 7. — rojstva po EMŠO [~]) — oče [Anton?] Brodarič [~ — natrgano/pod plastiko; GENETSKO = h46 Anton Brodarič 1893–1908], mati Katarina Milek [~]; h46 = 7. VPIS (1893, 1895, 1896, 1897, 1899, 1908 → 1910 — oče Anton Brodarič ISTI; mati Katarina Milek ISTA kot 1908); forenzika 46 (prva branja »6/14/16« NAPAČNE — zoom: jasno 46, odprta štirica); botra [boter neberljiv] + Marija Pendovec? [~ — Perdovec?] ¾ zemlj.; babica Marija Meh [~]; podpis [bled — verjetno Laulin Bitnar ~]; EMŠO ž 180791055019 [~ — 18.07.1910]; modri pripis: umrla dne 8.2.1965 v Zagrebu 7124/15 (Gradac 12.12.1985, matičarka Nina [~])",
    whatEn: "baptized Marija (Jul 18/20 — the birth per the personal ID [~]) — father [Anton?] Brodarič [~ — torn/under film; GENETICALLY = the h46 Anton Brodarič 1893–1908], mother Katarina Milek [~]; h46 = the 7th ENTRY (1893, 1895, 1896, 1897, 1899, 1908 → 1910 — the father Anton Brodarič the SAME; the mother Katarina Milek the SAME as 1908); forensics 46 (the first readings »6/14/16« WRONG — zoom: clearly 46, an open four); godparents [the godfather illegible] + Marija Pendovec? [~]; midwife Marija Meh [~]; signature [faded — probably Laulin Bitnar ~]; personal ID 180791055019 [~ — Jul 18, 1910]; blue note: died Feb 8, 1965 in Zagreb 7124/15 (Gradac Dec 12, 1985)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1910,
    scan: 216,
    page: 192,
    whatSi: "krščen Anton (28./29. 9. — rojstva po EMŠO) — oče Matija Milek ¾ zemljak, mati Marija Hrošič? [~ — Hrišič?; 1904 branje »Marija Hrišič?«]; h65 = 10. VPIS (1887–1908 — oče Matija Milek 10. skupaj! MILEK kontinuiteta: Milek/Mihelt/Mihek/Mitek variante); forenzika 65 NA OBOJIH dup (216+217); POPRAVEK »Griblje št. 45« (modri svinčnik) = NAPAČEN — genetika: Milek = h65 (10 vpisov!); botra Peter Poradinec? [~] ¾ zemlj. + Katarina Goricar? [~]; babica Barbara Adlešič; podpis Jos. Rauq; EMŠO k 2809910500547 (SKLADNO — sidro; rojstva 28. September → branje »19/19« = NAPAČNO, Kurrent 28/19); modri pripisi: žena Milek? Katarina umrla 10.11.1982 Novo mesto; poroka 9.5.1937 (Simonič? Nataša? [~])",
    whatEn: "baptized Anton (Sep 28/29 — the birth per the personal ID) — father Matija Milek, a three-quarter smallholder, mother Marija Hrošič? [~ — Hrišič?]; h65 = the 10th ENTRY (1887–1908 — the father Matija Milek the 10th time! the MILEK continuity: the Milek/Mihelt/Mihek/Mitek variants); forensics 65 on BOTH dups (216+217); the CORRECTION »Griblje št. 45« (a blue pencil) = WRONG — the genetics: Milek = h65 (10 entries!); godparents Peter Poradinec? + Katarina Goricar? [~]; midwife Barbara Adlešič; signature Jos. Rauq; personal ID 2809910500547 (CONSISTENT — an anchor; the birth Sep 28 → the reading »19/19« WRONG, a Kurrent 28/19); blue notes: the wife Milek? Katarina died Nov 10, 1982 Novo mesto; married May 9, 1937",
    status: "DOCUMENTED",
  },
  {
    houseNo: "49",
    bookSignature: "04105",
    year: 1910,
    scan: 216,
    page: 192,
    whatSi: "krščena Jozifa (23. 9.) — oče Nikolaj Brodarič ¾ zemljak, mati Marija Milek; h49 = 5. VPIS (1899 Marija, 1906 Jožef, 1907 Nikolaj, 1908 Barbara → 1910 — oče Nikolaj Brodarič ISTI; mati MILEK kontinuiteta: Marjeta/Marija/Ana/Marija/Marija); botra Jakop Bohte ¾ zemljak (ISTI kot r10 boter — 2× v letu!) + Katarina Perdinec? [~ — Pendrvec?]; babica Marija Meh; podpis Laulin Bitnar [~]; VPIS PRENEŠEN dne 5.5.1957 (modri pripis); modri svinčnik »fwin?« [~] ob forenziki 49",
    whatEn: "baptized Jozifa (Sep 23) — father Nikolaj Brodarič, a three-quarter smallholder, mother Marija Milek; h49 = the 5th ENTRY (1899 Marija, 1906 Jožef, 1907 Nikolaj, 1908 Barbara → 1910 — the father Nikolaj Brodarič the SAME; the mother MILEK continuity: Marjeta/Marija/Ana/Marija/Marija); godparents Jakop Bohte (the SAME as the r10 godfather — 2× in the year!) + Katarina Perdinec? [~]; midwife Marija Meh; signature Laulin Bitnar [~]; THE ENTRY TRANSFERRED on May 5, 1957 (a blue note); a blue pencil »fwin?« [~] by the forensics 49",
    status: "DOCUMENTED",
  },
  {
    houseNo: "28",
    bookSignature: "04105",
    year: 1910,
    scan: 218,
    page: 193,
    whatSi: "krščena Marjeta (3./5. 11.) — očetova celica PRAZNA (NEZAKONSKA), mati Marjeta Sodek? [~], samota, ¼ gazdinske? hči [~]; h28 = 2. VPIS — VRZEL 19 LET (1891 Anton — Jurij Požek? → 1910; izenačen REKORD z h77 1909: 1890→1909 = 19!); botra Jurij Škrbovič? [~] ¾ zemljak + Marija Kalan, učiteljeva žena (CROSS-ROW = h90 Kalanova žena, r33 ISTO leto!); babica Marija Meh; podpis Laulin Bitnar [~]; umrla dne 18.1.1982 v Mariboru (MMO Maribor 1.1982, str. 245, zap. št. 85; Gradac 15.2.1982, matičar Simonič?); poroka 23.5.1933 v Metlikah (Brina? Ambrožič? [~])",
    whatEn: "baptized Marjeta (Nov 3/5) — the father's cell EMPTY (ILLEGITIMATE), mother Marjeta Sodek? [~], alone, a quarter of a farm-wife's? daughter [~]; h28 = the 2nd ENTRY — a 19-YEAR GAP (1891 Anton — Jurij Požek? → 1910; TIED with the h77 1909 record: 1890→1909 = 19!); godparents Jurij Škrbovič? [~] + Marija Kalan, the teacher's wife (a CROSS-ROW = the h90 Kalan's wife, r33 the same year!); midwife Marija Meh; signature Laulin Bitnar [~]; died Jan 18, 1982 in Maribor (MMO Maribor 1.1982, p. 245, zap. 85; Gradac Feb 15, 1982); married May 23, 1933 in Metlika",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1910,
    scan: 218,
    page: 193,
    whatSi: "krščen Jurej (19./19. 11.) — oče Jurij Jakobič? [~ — Jakofčič] ¾ zemljak, mati Katarina Jakobič [~]; h6 = 5. VPIS (1904 Marija, 1905 Janez, 1907 Kapucina? intermezzo, 1909 Ana → 1910 — ISTI PAR Jakobič 4. skupaj!); botra Jožef Željko? [~] ¾ zemlj. + Marija Klepec (botrinja ISTA kot 1904 + 1909 — 3. skupaj!); babica Marija Meh; podpis Laulin Bitnar [~]; + 19/11.1910 — ISTI DAN kot krst (dojenček); forenzika 6 [~ pod zavihkom]",
    whatEn: "baptized Jurej (Nov 19/19) — father Jurij Jakobič? [~ — Jakofčič], a three-quarter smallholder, mother Katarina Jakobič [~]; h6 = the 5th ENTRY (1904 Marija, 1905 Janez, a 1907 Kapucina? interlude, 1909 Ana → 1910 — the SAME Jakobič COUPLE the 4th time!); godparents Jožef Željko? [~] + Marija Klepec (the godmother the SAME as 1904 + 1909 — the 3rd time!); midwife Marija Meh; signature Laulin Bitnar [~]; died Nov 19, 1910 — the SAME DAY as the baptism (an infant); forensics 6 [~ under a fold]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "42",
    bookSignature: "04105",
    year: 1910,
    scan: 218,
    page: 193,
    whatSi: "krščena Marija (22./26.? 11. [~ — spodnji rob natrgan]) — oče Jurij Pezdirec ¾ zemljak, mati Katarina Jurajevič; h42 = 5. VPIS (1904 Štraus intermezzo, 1905, 1906, 1909 → 1910 — ISTA ZVEZA Pezdirec × Jurajevič 2. leto zapored po 1909 VRNITEV!); GENETSKA REŠITEV forenzike: berljiva kot »16«, vendar GENETSKO h42 — h16 1910 = Novak (r84) kolizija nemogoča + h16 1900/1907/1908 = Novak; Kurrent 4→1 + 2→6; botra Marija Uih? [~] ¾ zemlj. + Katarina Perdinec? [~]; babica Marija Meh; podpis Jos. Rauq; + 22/12.1911? [~ — pripis nad naslednjo vrstico]",
    whatEn: "baptized Marija (Nov 22/26? [~ — the bottom edge torn]) — father Jurij Pezdirec, a three-quarter smallholder, mother Katarina Jurajevič; h42 = the 5th ENTRY (a 1904 Štraus interlude, 1905, 1906, 1909 → 1910 — the SAME Pezdirec × Jurajevič COUPLE the 2nd consecutive year after the 1909 RETURN!); the GENETIC SOLUTION of the forensics: legible as »16«, but GENETICALLY h42 — h16 1910 = Novak (r84) an impossible collision + h16 1900/1907/1908 = Novak; a Kurrent 4→1 + 2→6; godparents Marija Uih? [~] + Katarina Perdinec? [~]; midwife Marija Meh; signature Jos. Rauq; died Dec 22, 1911? [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1910,
    scan: 219,
    page: 194,
    whatSi: "krščen Jožef (9./9. 12.) — oče Janez Trome ½ zemljak (OČE MENJAVA: h1 1888–1909 Željko — 7 vpisov — → 1910 Trome!), mati Marija Meh [~ — Mure?]; h1 = 8. VPIS — POPOLNA MENJAVA DRUŽINE (1888–1909 Nikolaj/Jurij Željko × Katarina/Barbara Kure → 1910 Janez Trome × Marija Meh); ŽELJKO hkrati na h60 (r32 ISTO leto — Nikolaj Željko!); botra Jožef Štrucelj? [~] ¾ zemlj. + Marija Klepec (3. v letu — r32/r78/r83!); babica Ana Meh (MEH ×2 — mati + babica ISTI priimek!); podpis Paulin Bitnar (jasni P — DOKAZ: ISTA roka kot »Laulin Bitnar«!); poročim 17.2.1936, umrl 14.3.1936 — MESEC PO POROKI (pri 25!)",
    whatEn: "baptized Jožef (Dec 9/9) — father Janez Trome, a half smallholder (a FATHER CHANGE: h1 1888–1909 Željko — 7 entries — → 1910 Trome!), mother Marija Meh [~ — Mure?]; h1 = the 8th ENTRY — a COMPLETE FAMILY CHANGE (1888–1909 Nikolaj/Jurij Željko × Katarina/Barbara Kure → 1910 Janez Trome × Marija Meh); the ŽELJKO simultaneously at h60 (r32 the same year — Nikolaj Željko!); godparents Jožef Štrucelj? [~] + Marija Klepec (the 3rd of the year — r32/r78/r83!); midwife Ana Meh (MEH ×2 — the mother + the midwife the SAME surname!); signature Paulin Bitnar (a clear P — PROOF: the SAME hand as »Laulin Bitnar«!); married Feb 17, 1936, died Mar 14, 1936 — A MONTH AFTER THE WEDDING (aged 25!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "16",
    bookSignature: "04105",
    year: 1910,
    scan: 219,
    page: 194,
    whatSi: "krščena Ana (11./11. 12.) — oče Alojzij Novak, bajtar, mati Marija Frlah? [~ — cf. h60 1904 mati Marija Frlah? — ISTA žena Alojzija Novaka!]; h16 = 9. VPIS (1886×2, 1897, 1900 Novak, 1902 Straus, 1904 Ivec, 1906 Jakofčič, 1908 Narciz? Novak → 1910 Alojzij Novak bajtar POVRAČNICA); GENETIKA: Alojzij Novak bajtar × Marija Frlah? = ISTI PAR kot h60 1904 intermezzo! (Novak karusela h60↔h16); botra PRAZNA (—/—) — redko!; babica Marija Meh; podpis Laulin Bitnar [~]; + 11/12.1910 — ISTI DAN kot krst (dojenček); ZADNJA vrstica 1910",
    whatEn: "baptized Ana (Dec 11/11) — father Alojzij Novak, a cottager, mother Marija Frlah? [~ — cf. the h60 1904 mother Marija Frlah? — the SAME wife of Alojzij Novak!]; h16 = the 9th ENTRY (1886×2, 1897, 1900 Novak, 1902 Straus, 1904 Ivec, 1906 Jakofčič, 1908 Narciz? Novak → 1910 Alojzij Novak, a cottager, RETURNS); GENETICS: Alojzij Novak × Marija Frlah? = the SAME COUPLE as the h60 1904 interlude! (the Novak carousel h60↔h16); THE GODMOTHER EMPTY (—/—) — rare!; midwife Marija Meh; signature Laulin Bitnar [~]; died Dec 11, 1910 — the SAME DAY as the baptism (an infant); the LAST row of 1910",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1911,
    scan: 219,
    page: 194,
    whatSi: "krščena Antonija (10./11. 1.) — oče Janez Brinec ¾ zemljak, mati Ana Milek; h24 = 15. VPIS (1887–1909 — najbolj vpisovana hiša registra!); VRZEL 1 LETO (1910 brez); P105 lead »h34 TRETJE leto« NAPAČEN — hiša 24 (6× forenzika, ne 34!), genetsko SKLADNO: oče Janez Brinec = h24 Brinčeva familija; botra Marija Brinec (ISTI PRIIMEK = familija) + Marija Hribel? [~]; babica Barbara Adlešič = ISTA kot 1910 r66 h65!; podpis Paulin Bitnar; modri pripisi: »Umrła, dne 18.10.1973 v Dragatušu (LMMK nas. Dragatuš, vas št. 32, zap. 25.10.1973)« + »poročena 27.11.1933« + »tvr. poročena dne 25.9.1941 št. Rundtić? ohična v Radovljici?«",
    whatEn: "baptized Antonija (Jan 10/11) — father Janez Brinec, a three-quarter smallholder, mother Ana Milek; h24 = the 15th ENTRY (1887–1909 — the MOST-ENTERED house of the register!); a 1-YEAR GAP (none in 1910); the P105 lead »h34 the THIRD year« WRONG — house 24 (6× forensics, not 34!), genetically CONSISTENT: the father Janez Brinec = the h24 Brinec family; godmother Marija Brinec (the SAME SURNAME = the family) + Marija Hribel? [~]; midwife Barbara Adlešič = the SAME as 1910 r66 h65!; signature Paulin Bitnar; blue notes: died Oct 18, 1973 in Dragatuš (LMMK Dragatuš settlement, house no. 32, filed Oct 25, 1973) + married Nov 27, 1933 + re-married Sep 25, 1941 no. Rundtić? a widow's house in Radovljica?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1911,
    scan: 222,
    page: 197,
    whatSi: "krščena Vida (+16/7.1911 — dojenček) (12./13. 4.) — oče Jurij Podravec? [~ — 1. branje »Janez«] ¾ zemljak, mati Katarina Bedelarič? [~ Bedernivec?]; h48 = 5. VPIS (1909 4. VPIS EMŠO=krsta, 1908, 1904, 1897 → 1911); VRZEL 1 LETO; botra Nikolaj Brodarič + Doroteja Podravec ¾ zemnj; babica Marija Pletić? [~ Piletič?]; podpis Paulin Bitnar; modri pripis: »umrla dne 01.05.2003 v Novem mestu? (NKU NO 1.2003, št. 46, zap. št. 10, Metlika 22.08.2005, Matičarka nam. Tesnie Šimonič)« + »Drežljanka to Republike Slovenije, Upravna enota Črnomelj, class 201-2015/103 z dne 27.06.2013«",
    whatEn: "baptized Vida (died Jul 16, 1911 — an infant) (Apr 12/13) — father Jurij Podravec? [~ — first reading »Janez«], a three-quarter smallholder, mother Katarina Bedelarič? [~ Bedernivec?]; h48 = the 5th ENTRY (1909 the 4th with the ID = the baptism date, 1908, 1904, 1897 → 1911); a 1-YEAR GAP; godfather Nikolaj Brodarič + godmother Doroteja Podravec; midwife Marija Pletić? [~]; signature Paulin Bitnar; blue note: died May 1, 2003 in Novo mesto? (NKU NO 1.2003, no. 46, file no. 10, Metlika Aug 22, 2005, deputy registrar Tesnie Šimonič) + a Drežnica certificate of the Republic of Slovenia, Administrative Unit Črnomelj, class 201-2015/103 of Jun 27, 2013",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1911,
    scan: 222,
    page: 197,
    whatSi: "krščena Terezija (14./14. 4.) — oče Janez Hrižan ¾ zemljak, mati Katarina Štrucelj; h36 = 9. VPIS (1886–1908); VRZEL 2 LETI; GENETIKA SKLADNO: h36 = HRIŽAN/KRIŽAN hiša (1908 »KRIŽAN POVRAT«) — oče Janez Hrižan!; botra Matija Podravec? [~ Pecdrnec] + Marjeta Štraus? [~ Straov] = ŠTRAUS signal (1908 boter Štraus); babica Marija Meh; podpis Paulin Bitnar; EMŠO ž 1704911305004 — DATUMSKI POPRAVEK: EMŠO 17.4. vs register 14.4.! (3. popravek vzorca cf. P105 r22/r66); modri pripis: »umrla dne 01.05.2003 v Novem mestu? (NKU NO, št. 46, zap. št. 10, Metlika 22.08.2005)«",
    whatEn: "baptized Terezija (Apr 14/14) — father Janez Hrižan, a three-quarter smallholder, mother Katarina Štrucelj; h36 = the 9th ENTRY (1886–1908); a 2-YEAR GAP; GENETICS CONSISTENT: h36 = the HRIŽAN/KRIŽAN house (1908 »KRIŽAN RETURNS«) — the father Janez Hrižan!; godfather Matija Podravec? [~] + godmother Marjeta Štraus? [~] = the ŠTRAUS signal (1908 the godfather Štraus); midwife Marija Meh; signature Paulin Bitnar; personal ID 1704911305004 — a BIRTH-DATE CORRECTION: the ID Apr 17 vs the register Apr 14! (the 3rd correction of the sample cf. P105 r22/r66); blue note: died May 1, 2003 in Novo mesto? (NKU NO, no. 46, file no. 10, Metlika Aug 22, 2005)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1911,
    scan: 222,
    page: 197,
    whatSi: "krščen Anton (4./5. 5.) — oče Matija Jakofič ¾ zemnjak, mati Marija Jakofič; h13 = 5. VPIS (1886, 1888, 1894, 1907 → 1911); VRZEL 4 LETI; MENJAVA #2: 1907 Šimec × Kambič (selitev h18→h13) → 1911 Jakofič par; botri Janez Kambič + Marija Kambič = povezava s prejšnjo h13 familijo!; babica Marija Meh; podpis Jos. Rauq?; EMŠO mo 0405911500574 — SKLADNO — SIDRO (04.05.911, 10. števka 0 = moški); modri pripisi: »umrl dne 9.4.1934 v Novem mestu (obč. nosič 1.1934, št. 385 od 12.2.)« + »(devec nosič 1.1934, št. 856 od 14.03)«",
    whatEn: "baptized Anton (May 4/5) — father Matija Jakofič, a three-quarter smallholder, mother Marija Jakofič; h13 = the 5th ENTRY (1886, 1888, 1894, 1907 → 1911); a 4-YEAR GAP; the FAMILY CHANGE #2: 1907 Šimec × Kambič (a move h18→h13) → 1911 the Jakofič couple; the godparents Janez + Marija Kambič = a link to the previous h13 family!; midwife Marija Meh; signature Jos. Rauq?; personal ID 0405911500574 — CONSISTENT — an ANCHOR (May 4, 1911, the 10th digit 0 = male); blue notes: died Apr 9, 1934 in Novo mesto (municipal file 1.1934, no. 385 of Feb 12) + (the second file 1.1934, no. 856 of Mar 14)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04105",
    year: 1911,
    scan: 222,
    page: 197,
    whatSi: "krščena Marija (+9/9.1911 — dojenček) (23./24. 5.) — oče Martin Papič? [~ Tapič] ¾ zemnjak, mati Marija Plet? [~ Mlut? — 1909 branje]; GENETSKA REŠITEV vasi: napisano »Grišice« — genetsko GRIBLJE 33! (oče Martin Papič = ISTI oče kot h33 1909; botri ISTI PRIIMEK Papič; hiša 33 = h33) — cf. P102 r11 »Grišlje« = Griblje genetsko; h33 = 4. VPIS (1889, 1898, 1909 → 1911); VRZEL 1 LETO — praktično ZAPORED; botra Mihal Papič? + Katarina Papič?; babica Ana Mavrenič; podpis Paulin Bitnar; dojenček † +9/9.1911 (3.5 meseca); mati menjava? (1909 »Mlut?« → 1911 »Plet?« — morda ISTA oseba)",
    whatEn: "baptized Marija (died Sep 9, 1911 — an infant) (May 23/24) — father Martin Papič? [~ Tapič], a three-quarter smallholder, mother Marija Plet? [~ Mlut? — the 1909 reading]; THE GENETIC SOLUTION OF THE VILLAGE: written »Grišice« — genetically GRIBLJE 33! (the father Martin Papič = the SAME father as h33 1909; the godparents the SAME SURNAME Papič; house 33 = h33) — cf. P102 r11 »Grišlje« = Griblje genetically; h33 = the 4th ENTRY (1889, 1898, 1909 → 1911); a 1-YEAR GAP — practically CONSECUTIVE; godparents Mihal Papič? + Katarina Papič?; midwife Ana Mavrenič; signature Paulin Bitnar; an infant died Sep 9, 1911 (3.5 months); a mother change? (1909 »Mlut?« → 1911 »Plet?« — perhaps the SAME person)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1911,
    scan: 222,
    page: 197,
    whatSi: "krščena Neža [ime pod anotacijami] (3./4. 6., Juni glava) — oče Ivan Brinec? [~ Brine] ¾ zemnjak, mati Doroteja Pezdirec? [~ Podrinc/Podrtec]; h14 = 5. VPIS (1896, 1900, 1902, 1908 → 1911); VRZEL 3 LETI; babica PRAZNA (edina v 1911); botra Matija Brinec ¾ zemnj + Bara Adlešič = h24 babica r3 ISTA OSEBA CROSS-ROW!; podpis Paulin Bitnar; oče Brinec? = BRINEC familija signal (h24!); mati PEZDIREC signal; modri pripisi težko berljivi: »umrla dne 16.?11.?/22.11.? ... (dok. KO Gradec?, zap. št. 169)« + »Neža 18.01.1991?«",
    whatEn: "baptized Neža [the name under annotations] (Jun 3/4, the June heading) — father Ivan Brinec? [~ Brine], a three-quarter smallholder, mother Doroteja Pezdirec? [~ Podrinc/Podrtec]; h14 = the 5th ENTRY (1896, 1900, 1902, 1908 → 1911); a 3-YEAR GAP; THE MIDWIFE EMPTY (the only one in 1911); godfather Matija Brinec + godmother Bara Adlešič = the h24 midwife of r3 the SAME PERSON a CROSS-ROW!; signature Paulin Bitnar; the father Brinec? = the BRINEC family signal (h24!); the mother a PEZDIREC signal; blue notes hard to read: died Nov 16?/22? ... (file KO Gradec?, file no. 169) + Neža Jan 18, 1991?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "47",
    bookSignature: "04105",
    year: 1911,
    scan: 223,
    page: 198,
    whatSi: "krščen Janez (16./16. 7., Juli glava) — oče Janez Požek, bajtar, mati Katarina Veselič; h47 = 3. VPIS (1887, 1890 → 1911); **VRZEL 21 LET — NOV REKORD!** (prej 19 = h77 1909 + h28 1910); oče POŽEK bajtar = ISTA familija kot h77 (Jurij Požek bajtar 1890/1909!) — brata?; botra Marija Šimec + Ana Milek = r3 mati ISTA OSEBA CROSS-ROW!; babica Marija Meh; podpis Paulin Bitnar; modri pripisi: »umrl dne 18.1.1978 v Novem mestu (NT&K Novo mesto 1.1978, zap. št. 29)« + »poročen 14.6.1947« + »Gradec 27.2.1978«",
    whatEn: "baptized Janez (Jul 16/16, the July heading) — father Janez Požek, a cottager, mother Katarina Veselič; h47 = the 3rd ENTRY (1887, 1890 → 1911); **a 21-YEAR GAP — a NEW RECORD!** (the previous 19 = h77 1909 + h28 1910); the father POŽEK a cottager = the SAME family as h77 (Jurij Požek a cottager 1890/1909!) — brothers?; the godmother Marija Šimec + Ana Milek = the r3 mother the SAME PERSON a CROSS-ROW!; midwife Marija Meh; signature Paulin Bitnar; blue notes: died Jan 18, 1978 in Novo mesto (NT&K Novo mesto 1.1978, file no. 29) + married Jun 14, 1947 + Gradac Feb 27, 1978",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1911,
    scan: 223,
    page: 198,
    whatSi: "krščen Julij (+2/6.1912? — dojenček) (24./25. 8.) — oče Matija Strauš? [~ Straov] ¾ zemnjak, mati Marjeta Šimec; h72 = 7. VPIS (1888–1909); VRZEL 1 LETO; ISTA ZVEZA Strauš × Šimec kot 1909 (POVRAČNICA) — ŠTRAUS kontinuiteta SKLADNO!; mati Marjeta Šimec = Šimec familija (1909 menjava #3 ISTA); botra Mika? Jakofič? [~] + Barbara Šmuc? [~ Šmejc?]; babica Marija Meh; podpis Paulin Bitnar",
    whatEn: "baptized Julij (died Jun 2, 1912? — an infant) (Aug 24/25) — father Matija Strauš? [~ Straov], a three-quarter smallholder, mother Marjeta Šimec; h72 = the 7th ENTRY (1888–1909); a 1-YEAR GAP; the SAME COUPLE Strauš × Šimec as 1909 (the RETURNEE) — the ŠTRAUS continuity CONSISTENT!; the mother Marjeta Šimec = the Šimec family (1909 the change #3 the SAME); godparents Mika? Jakofič? [~] + Barbara Šmuc? [~]; midwife Marija Meh; signature Paulin Bitnar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "55",
    bookSignature: "04105",
    year: 1911,
    scan: 224,
    page: 199,
    whatSi: "krščen Matevž (3./4. 8., Avgust glava) — oče Matevž Kralj ¾ zemnjak, mati Barbara Škržan? [~ Šteran?]; h55 = 3. VPIS (1887, 1890 → 1911); **VRZEL 21 LET — REKORD IZENAČEN z r49 h47 (DVA 21-letna rekorda isto leto!)**; KRALJ familija NOVA v vzorcu (oče + botri ISTI PRIIMEK); vas Griblje jasna pod modro anotacijo (P104 lead »vas pokrita« POPRAVLJEN); botra Nikolaj Kralj + Ana Kralj; babica Marija Meh; podpis Paulin Bitnar; EMŠO mo 0308911500935 — SKLADNO — SIDRO (03.08.911, 10. števka 0 = moški); modri pripisi: »Žena, Kvalj? Ronja? umrla dne 31.1.1984 v Novem mestu (NKU Novo mesto 1.1984, št. 179, zap. št. 66, Simonič Nina 12.3.1984)« + »umrl dne 26.04.1986 v gmiljah? (NKU št. 1956, št. 151, zap. št. 2, Gradac 19.05.1986, Matičar: Obriž? dna?)« + »Gradac, 12/3-1984« + »poročen 19.2.1935?«",
    whatEn: "baptized Matevž (Aug 3/4, the August heading) — father Matevž Kralj, a three-quarter smallholder, mother Barbara Škržan? [~ Šteran?]; h55 = the 3rd ENTRY (1887, 1890 → 1911); **a 21-YEAR GAP — TIED with the r49 h47 record (TWO 21-year records in the same year!)**; the KRALJ family NEW to the sample (the father + the godparents the SAME SURNAME); the village Griblje clear under the blue annotation (the P104 lead »village covered« CORRECTED); godparents Nikolaj Kralj + Ana Kralj; midwife Marija Meh; signature Paulin Bitnar; personal ID 0308911500935 — CONSISTENT — an ANCHOR (Aug 3, 1911, the 10th digit 0 = male); blue notes: the wife, Kvalj? Ronja? died Jan 31, 1984 in Novo mesto (NKU Novo mesto 1.1984, no. 179, file no. 66, Simonič Nina Mar 12, 1984) + died Apr 26, 1986 in gmilje? (NKU no. 1956, no. 151, file no. 2, Gradac May 19, 1986, registrar: Obriž? dna?) + Gradac, Mar 12, 1984 + married Feb 19, 1935?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "3",
    bookSignature: "04105",
    year: 1911,
    scan: 225,
    page: 200,
    whatSi: "krščen Nikolaj (+25/4.1919 — dojenček) (1./2. 10., Oktobar glava) — oče Matija Papič ¾ zemnjak, mati Katarina Novak; GENETSKA REŠITEV vasi: napisano »Grišice« — genetsko GRIBLJE 3! (hiša 3 = h3 Papič hiša 1889/1902/1907; oče Papič) — 2. »Grišice« rešitev (cf. r37 h33)!; h3 = 4. VPIS; VRZEL 4 LETI; babica Katarina Novak — BABICA = MATI ISTA OSEBA! (cf. P103 r16); botra Nikolaj Novak + Ana Novak (ISTI PRIIMEK); podpis Jos. Rauq?; dojenček † +25/4.1919; PAPIČ 2 hiši v 1911 (h33 Martin + h3 Matija — brata?)",
    whatEn: "baptized Nikolaj (died Apr 25, 1919 — an infant) (Oct 1/2, the October heading) — father Matija Papič, a three-quarter smallholder, mother Katarina Novak; THE GENETIC SOLUTION OF THE VILLAGE: written »Grišice« — genetically GRIBLJE 3! (house 3 = the h3 Papič house 1889/1902/1907; the father Papič) — the 2nd »Grišice« solution (cf. r37 h33)!; h3 = the 4th ENTRY; a 4-YEAR GAP; the midwife Katarina Novak — THE MIDWIFE = THE MOTHER THE SAME PERSON! (cf. P103 r16); godparents Nikolaj Novak + Ana Novak (the SAME SURNAME); signature Jos. Rauq?; an infant died Apr 25, 1919; TWO Papič houses in 1911 (h33 Martin + h3 Matija — brothers?)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1911,
    scan: 225,
    page: 200,
    whatSi: "krščen Jurij (5./5. 10.) — oče Janez Trček ¾ zemnjak, mati Katarina Kure; h21 = 8. VPIS (1887–1910); ZAPORED — 2. leto!; MENJAVA OČETA Z ISTO MATI: 1910 »…mir« Požek × Katarina Kure → 1911 Janez Trček × ISTA Katarina Kure! (Požek 7 vpisov konec; cf. h1 1910 oče menjava Željko→Trome z ISTO mati Meh); botra Janez Brinec? [~] = h24 oče r3 CROSS-ROW! + Marija Šimec; babica Marjeta Meh; podpis Paulin Bitnar",
    whatEn: "baptized Jurij (Oct 5/5) — father Janez Trček, a three-quarter smallholder, mother Katarina Kure; h21 = the 8th ENTRY (1887–1910); CONSECUTIVE — the 2nd year!; A FATHER CHANGE WITH THE SAME MOTHER: 1910 »…mir« Požek × Katarina Kure → 1911 Janez Trček × the SAME Katarina Kure! (Požek's 7 entries ended; cf. h1 1910 the father change Željko→Trome with the SAME mother Meh); godfather Janez Brinec? [~] = the h24 father of r3 a CROSS-ROW! + Marija Šimec; midwife Marjeta Meh; signature Paulin Bitnar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "74",
    bookSignature: "04105",
    year: 1911,
    scan: 225,
    page: 200,
    whatSi: "krščen Janez (13./14. 10.) — oče Janez Kambič ¾ zemnjak, mati Marija Milek; h74 = 2. VPIS (1893 → 1911); **VRZEL 18 LET** (2. najdaljša v 1911); oče KAMBIČ (h74 nova familija signal); mati MARIJA MILEK = MILEK kontinuiteta; botra Matija Šimec + Katarina Požek = POŽEK signal (h47 r49!); babica Marija Meh; podpis Paulin Bitnar; EMŠO mo 1310911500879 — SKLADNO — SIDRO (13.10.911, 10. števka 0 = moški); VPIS PRENEŠEN 25.5.1999? [~] — Matičarka Šimonič Nina; modri pripisi: »žena umrla dne 04.08.1987 v gmiljah? (NKU NO št. 1987, št. 16, zap. št. 52, Metlika 10.08.1987)« + »umrl dne 02.05.1999 v Metliki (MOKNOK 1.1999, št. 21, zap. št. 40, Metlika 03.05.1999)«",
    whatEn: "baptized Janez (Oct 13/14) — father Janez Kambič, a three-quarter smallholder, mother Marija Milek; h74 = the 2nd ENTRY (1893 → 1911); **an 18-YEAR GAP** (the 2nd longest in 1911); the father KAMBIČ (an h74 new-family signal); the mother MARIJA MILEK = the MILEK continuity; godfather Matija Šimec + godmother Katarina Požek = the POŽEK signal (h47 r49!); midwife Marija Meh; signature Paulin Bitnar; personal ID 1310911500879 — CONSISTENT — an ANCHOR (Oct 13, 1911, the 10th digit 0 = male); THE ENTRY TRANSFERRED May 25, 1999? [~] — registrar Šimonič Nina; blue notes: the wife died Aug 4, 1987 in gmilje? (NKU NO no. 1987, no. 16, file no. 52, Metlika Aug 10, 1987) + died May 2, 1999 in Metlika (MOKNOK 1.1999, no. 21, file no. 40, Metlika May 3, 1999)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "49",
    bookSignature: "04105",
    year: 1911,
    scan: 225,
    page: 200,
    whatSi: "krščen Frančišek (+27/5.1913 — dojenček) (24./24. 11.) — oče Anton Brodarič ¾ zemnjak, mati Marija Milek; h49 = 6. VPIS (1899–1910); ZAPORED — 2. leto!; BRODARIČ kontinuiteta: 1910 r67 h49 Nikolaj Brodarič → 1911 Anton Brodarič (ISTA familija — oče menjava ali brat); botrinja Marjana Bohte = Bohte signal (1910 boter Jakop Bohte h49!); boter Jurij Podravec? [~]; babica Marija Meh; podpis Jos. Rauq?; dojenček † +27/5.1913; modri pripisi: »umrl/a dne 20.9.1987 v Črnomlju (NU KO Črnomelj 1.1987, št. 22, zap. št. 43)« + »umrla 1993 v Črnomlju (1.1993, št. 252, 6.01.1995)« + »poročena 5.2.1931« + »poročen 15.4.1935«",
    whatEn: "baptized Frančišek (died May 27, 1913 — an infant) (Nov 24/24) — father Anton Brodarič, a three-quarter smallholder, mother Marija Milek; h49 = the 6th ENTRY (1899–1910); CONSECUTIVE — the 2nd year!; the BRODARIČ continuity: 1910 r67 h49 Nikolaj Brodarič → 1911 Anton Brodarič (the SAME family — a father change or a brother); the godmother Marjana Bohte = the Bohte signal (1910 the godfather Jakop Bohte h49!); godfather Jurij Podravec? [~]; midwife Marija Meh; signature Jos. Rauq?; an infant died May 27, 1913; blue notes: died Sep 20, 1987 in Črnomelj (NU KO Črnomelj 1.1987, no. 22, file no. 43) + died 1993 in Črnomelj (1.1993, no. 252, Jan 6, 1995) + married Feb 5, 1931 + married Apr 15, 1935",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1911,
    scan: 225,
    page: 200,
    whatSi: "krščena Neža (28./29. 11.) — oče Jurij? Jakobič [~ — 1. branje »Janez«] ¾ zemnjak, mati Katarina Jakobič; h6 = 6. VPIS (1904, 1905, 1907, 1909, 1910 → 1911); **ZAPORED — 3. leto!** (1909/10/11); JAKOBIČ genetsko SKLADNO (h6 = Jakobič 1904/05); boter Jožef Željko = ŽELJKO signal (h1/h60!) + botrinja Marija Klepec = KLEPEC 4.× v 2 letih (1910 r32/r78/r83 → 1911 r74)!; babica Marija Meh; podpis Paulin Bitnar; EMŠO ž 2810911505907? [~ — mesec 11/10 na meji] (28.11.911, 10. števka 5 = ženska); modri pripisi: »umrl/a dne 20.3.1944 v 8-vojnci? (NU KO Novo mesto, št. 1995, zap. št. 13)« + »poročena 9.2.1947?« + »poročen 31.8.1935?«",
    whatEn: "baptized Neža (Nov 28/29) — father Jurij? Jakobič [~ — first reading »Janez«], a three-quarter smallholder, mother Katarina Jakobič; h6 = the 6th ENTRY (1904, 1905, 1907, 1909, 1910 → 1911); **CONSECUTIVE — the 3rd year!** (1909/10/11); the JAKOBIČ genetics CONSISTENT (h6 = Jakobič 1904/05); godfather Jožef Željko = the ŽELJKO signal (h1/h60!) + godmother Marija Klepec = KLEPEC the 4th time in 2 years (1910 r32/r78/r83 → 1911 r74)!; midwife Marija Meh; signature Paulin Bitnar; personal ID 2810911505907? [~ — the month 11/10 borderline] (Nov 28, 1911, the 10th digit 5 = female); blue notes: died Mar 20, 1944 in 8-vojnica? (NU KO Novo mesto, no. 1995, file no. 13) + married Feb 9, 1947? + married Aug 31, 1935?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1911,
    scan: 227,
    page: 201,
    whatSi: "krščena Marija (14./14. 11.) — oče Nikolaj Segina ¾ zemljak, mati Katarina Brinec; h30 = 13. VPIS (1890–1909); VRZEL 1 LETO; **SEGINA POVRAT — 1906 MENJAVA REŠENA**: 1906 h30 »Segina → Brinec« menjava → 1911 oče Nikolaj Segina × mati Katarina Brinec = KOMBINACIJA obeh familij (Brinčeva žena v Seginovi hiši!); botrinji Marija Milek (r69 mati ISTA?) + Katarina Hrižan = HRIŽAN signal; babica Marija Meh; podpis Jos. Rauq?; VPIS PRENEŠEN v matični register dne 25.11.2007 Matičarka [Bebjanek? ~]; modri pripisi: »umrl/a dne 15.12.1999 v Grintofcu? (dokt. KO št. 1.1997, št. 204, zap. st. 22)« + »poročena 14.6.1937« + »Šimenc 31.2.1935.Osilnica?«",
    whatEn: "baptized Marija (Nov 14/14) — father Nikolaj Segina, a three-quarter smallholder, mother Katarina Brinec; h30 = the 13th ENTRY (1890–1909); a 1-YEAR GAP; **THE SEGINA RETURN — the 1906 FAMILY CHANGE SOLVED**: 1906 h30 »Segina → Brinec« change → 1911 the father Nikolaj Segina × the mother Katarina Brinec = a COMBINATION of both families (a Brinec wife in the Segina house!); godmothers Marija Milek (the r69 mother the SAME?) + Katarina Hrižan = the HRIŽAN signal; midwife Marija Meh; signature Jos. Rauq?; THE ENTRY TRANSFERRED to the civil register Nov 25, 2007 by registrar [Bebjanek? ~]; blue notes: died Dec 15, 1999 in Grintovec? (file KO no. 1.1997, no. 204, file st. 22) + married Jun 14, 1937 + Šimenc Feb 31, 1935.A minor?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1911,
    scan: 227,
    page: 201,
    whatSi: "krščena Marija (+7/10.1914 — dojenček) (22./22. 11.) — oče Nikolaj Podravec? [~ Tecdrnec/Podrnec] ¾ zemnjak, mati Ana Žuran? [~]; h40 = 4. VPIS (1897, 1898, 1899 → 1911); **VRZEL 12 LET!**; oče PODRAVEC? = familija (h48 r32!); botra Matija Hrižan + Katarina Hrižan = HRIŽAN PAR; babica Marija Meh; podpis Paulin Bitnar; EMŠO ž 2311911505307 — 10. števka 5 = ženska SKLADNO; dan 23 vs register 22 — MOŽEN DATUMSKI POPRAVEK [~ dan]; dojenček † +7/10.1914; modri pripisi: »Alen? umrl/a dne 09.03.1983 v Zagrebu (1918 Vojvodina?, cerke 1982)« + »umrl/a dne 19.8.1975 v Kandijah?«",
    whatEn: "baptized Marija (died Oct 7, 1914 — an infant) (Nov 22/22) — father Nikolaj Podravec? [~ Tecdrnec/Podrnec], a three-quarter smallholder, mother Ana Žuran? [~]; h40 = the 4th ENTRY (1897, 1898, 1899 → 1911); **a 12-YEAR GAP!**; the father PODRAVEC? = the family (h48 r32!); godparents the HRIŽAN COUPLE; midwife Marija Meh; signature Paulin Bitnar; personal ID 2311911505307 — the 10th digit 5 = female CONSISTENT; the day 23 vs the register 22 — a POSSIBLE BIRTH-DATE CORRECTION [~ the day]; an infant died Oct 7, 1914; blue notes: died Mar 9, 1983 in Zagreb (1918 Vojvodina?, the church 1982) + died Aug 19, 1975 in Kandija?",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1911,
    scan: 227,
    page: 201,
    whatSi: "krščena Amalija (2./2. 12.) — oče Janez Gapič? [~ Papič?] ¾ zemnjak, mati Katarina Hrižan; h31 = 10. VPIS (1887–1900); **VRZEL 11 LET!**; mati Katarina Hrižan + botrinja Barbara Hrižan = HRIŽAN kampanja; oče Gapič?/Papič? kolizija — PAPIČ 3. hiša v 1911? (h33 Martin + h3 Matija + h31 Janez G/P?) — genetska dilema; boter Janez Jaklič? [~ »Jaklič Janez«]; babica Marija Meh; podpis Paulin Bitnar; VPIS PRENEŠEN v matični register 19.11.2007 Matičarka Belojaunik? [~ Belofanovič?]; modri pripisi: »umrla dne 19.8.1973 (MMK Ljubljana-center)« + »Gradec 31.12.1973«",
    whatEn: "baptized Amalija (Dec 2/2) — father Janez Gapič? [~ Papič?], a three-quarter smallholder, mother Katarina Hrižan; h31 = the 10th ENTRY (1887–1900); **an 11-YEAR GAP!**; the mother Katarina Hrižan + the godmother Barbara Hrižan = the HRIŽAN campaign; the father Gapič?/Papič? a collision — a 3rd Papič house in 1911? (h33 Martin + h3 Matija + h31 Janez G/P?) — a genetic dilemma; godfather Janez Jaklič? [~]; midwife Marija Meh; signature Paulin Bitnar; THE ENTRY TRANSFERRED to the civil register Nov 19, 2007 by registrar Belojaunik? [~ Belofanovič?]; blue notes: died Aug 19, 1973 (MMK Ljubljana-center) + Gradac Dec 31, 1973",
    status: "DOCUMENTED",
  },
  {
    houseNo: "70",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščen Alojzij (2./2. 1.) — oče Matija Brinec ¾ zemljak [~ 48?], mati Marija Grabrijan; h70 = 2. VPIS (1893 → 1912); **VRZEL 19 LET!**; **SELIJA h10 → h70**: 1909 h10 par (Matija Brinec × Marija Grabrijan — P106) zdaj v h70 — 2. selitev vzorca (cf. h30→h10 1909!); botra Janez Brinec + Ana Segina (»z ženo«); babica Marija Meh; podpis Jos. Rauq; EMŠO 0201912500174 — SKLADNO — SIDRO (2.1.1912; 10. števka 4 = moški) — P106 lead EMŠO 0101912500294 NAPAČEN (popravek forenzike 6–7×); poroki 8.5.1941; rdeči pripis: »umrl dne 23.8.1987 v Novem mestu (MKU NO, str. 222, zap. št. 477; 29.9.1987)« — 75 let",
    whatEn: "baptized Alojzij (Jan 2/2) — father Matija Brinec, a three-quarter smallholder [~ 48?], mother Marija Grabrijan; h70 = the 2nd ENTRY (1893 → 1912); **a 19-YEAR GAP!**; **A MOVE h10 → h70**: the 1909 h10 couple (Matija Brinec × Marija Grabrijan — P106) now in h70 — the 2nd move of the sample (cf. h30→h10 1909!); godparents Janez Brinec + Ana Segina (»with wife«); midwife Marija Meh; signature Jos. Rauq; personal ID 0201912500174 — CONSISTENT — an ANCHOR (Jan 2, 1912; the 10th digit 4 = male) — the P106 lead ID 0101912500294 WRONG (corrected by 6–7× forensics); married May 8, 1941; red note: died Aug 23, 1987 in Novo mesto (MKU NO, p. 222, file no. 477; Sep 29, 1987) — aged 75",
    status: "DOCUMENTED",
  },
  {
    houseNo: "59",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščen Janez (+16/6.1912 [~ 16/7] — dojenček) (5./5. 1.) — oče France Jaklič, bajtar in kovač (DVA poklica!), mati Ana Krambič; h59 = 3. VPIS (1889, 1899 → 1912); VRZEL 13 LET; botra Alojzij Novak + Barbara Krambič (botrinja = ISTI PRIIMEK kot mati — familija!); babica Marija Meh; podpis Paulin Bitnar; dojenček †",
    whatEn: "baptized Janez (died Jun 16, 1912 [~ Jul 16] — an infant) (Jan 5/5) — father France Jaklič, a cottager AND a blacksmith (TWO trades!), mother Ana Krambič; h59 = the 3rd ENTRY (1889, 1899 → 1912); a 13-YEAR GAP; godparents Alojzij Novak + Barbara Krambič (the godmother = the SAME SURNAME as the mother — the family!); midwife Marija Meh; signature Paulin Bitnar; an infant died",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščen Anton (+3.9.1912 [~] — dojenček) (10./10. 1.) — oče Marko Hrižan ¾ zemljak, mati Katarina Štraus; h36 = 8. VPIS (1894–1911); botra Jurij Pezdirec + Ana Pezdirec (PAR); babica Marija Meh; podpis Paulin Bitnar; dojenček †; HRIŽAN signal (oče) + ŠTRAUS mati cf. h72 (P106 ISTA ZVEZA)",
    whatEn: "baptized Anton (died Sep 3, 1912 [~] — an infant) (Jan 10/10) — father Marko Hrižan, a three-quarter smallholder, mother Katarina Štraus; h36 = the 8th ENTRY (1894–1911); godparents Jurij Pezdirec + Ana Pezdirec (a COUPLE); midwife Marija Meh; signature Paulin Bitnar; an infant died; the HRIŽAN signal (the father) + the ŠTRAUS mother cf. h72 (P106 the SAME COUPLE)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščena Neža (11./12. 1.) — oče Janez Kumprič ¾ zemljak, mati Marija Jakofčič; h11 = 4. VPIS (1890–1908); botra Janez Adlešič + Neza Adlešič (PAR); babica Marija Meh; podpis Paulin Bitnar; **† 18.2.2004 Griblje — 92 LET (najstarejši vpis 1912!)** (MKU MO Črnomelj, str. 44, zap. št. 14; 06.05.2004; Maribor); pripis »znaka: kam. delavka dna« [~]",
    whatEn: "baptized Neža (Jan 11/12) — father Janez Kumprič, a three-quarter smallholder, mother Marija Jakofčič; h11 = the 4th ENTRY (1890–1908); godparents Janez Adlešič + Neza Adlešič (a COUPLE); midwife Marija Meh; signature Paulin Bitnar; **died Feb 18, 2004 in Griblje — 92 YEARS (the oldest entry of 1912!)** (MKU MO Črnomelj, p. 44, file no. 14; May 6, 2004; Maribor); a note »znaka: kam. delavka dna« [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščen Anton (+8.4.1913 — dojenček) (16./16. 1.) — oče Miklavž Filar? [~ Šilar?] ¾ zemljak, mati Katarina Šlobučar; h45 = 5. VPIS (1896, 1897, 1900, 1904 → 1912); VRZEL 8 LET; botra Miklavž Segina + Katarina Hrižan; babica Marija Meh; podpis Jos. Rauq; **DVOJČKI r6/r7 (Anton + Jožefa) — ISTI starši + ISTA botra + isti dan!** (3. par 1912); dojenček †; Seginov boter (cf. P106 r80 h30 Segina povrat)",
    whatEn: "baptized Anton (died Apr 8, 1913 — an infant) (Jan 16/16) — father Miklavž Filar? [~ Šilar?], a three-quarter smallholder, mother Katarina Šlobučar; h45 = the 5th ENTRY (1896, 1897, 1900, 1904 → 1912); an 8-YEAR GAP; godparents Miklavž Segina + Katarina Hrižan; midwife Marija Meh; signature Jos. Rauq; **THE TWINS r6/r7 (Anton + Jožefa) — the SAME parents + the SAME godparents + the same day!** (the 3rd pair of 1912); an infant died; a Segina godfather (cf. P106 r80 h30 the Segina return)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščena Jožefa (+13.1914 [~]) (16./16. 1.) — oče Miklavž Filar? [~ Šilar?] ¾ zemljak, mati Katarina Šlobučar; h46 = 8. VPIS (1893–1910); **DVOJČKI r6/r7 — 2/2 (dva zaporedna VPISA v DVEH sosednjih hišah 45+46!)**; botra Miklavž Segina + Katarina Hrižan; babica Marija Meh; podpis Jos. Rauq; otrok †; modri pripis »62: matjaino teresijo...« [~]",
    whatEn: "baptized Jožefa (died 1914 [~]) (Jan 16/16) — father Miklavž Filar? [~ Šilar?], a three-quarter smallholder, mother Katarina Šlobučar; h46 = the 8th ENTRY (1893–1910); **THE TWINS r6/r7 — 2/2 (two consecutive ENTRIES in TWO NEIGHBOURING houses 45+46!)**; godparents Miklavž Segina + Katarina Hrižan; midwife Marija Meh; signature Jos. Rauq; a child died; the blue note »62: matjaino teresijo...« [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščen Anton (19./19. 1.) — oče Janez Jakofčič ¾ zemljak, mati Neza Jakljevič; h8 = 3. VPIS (1888, 1889 → 1912); **VRZEL 23 LET — NOV REKORD!** (prej 21: h47+h55 1911); botra Jakob Toller + Katarina Toller; babica Marija Meh; podpis Jos. Rauq; † 24.1942 [~] Griblje (k.1942, str. 109, zap. št. 9)",
    whatEn: "baptized Anton (Jan 19/19) — father Janez Jakofčič, a three-quarter smallholder, mother Neza Jakljevič; h8 = the 3rd ENTRY (1888, 1889 → 1912); **a 23-YEAR GAP — A NEW RECORD!** (the previous 21: h47+h55 1911); godparents Jakob Toller + Katarina Toller; midwife Marija Meh; signature Jos. Rauq; died 1942 [~] in Griblje (the book of 1942, p. 109, file no. 9)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "26",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščen Jožef († 26.11.1930 — 18 let) (3./4. 2.) — oče Anton Podlavrič? [~] ¾ zemljak, mati Katarina Meh; h26 = 5. VPIS (1887, 1889, 1896, 1906 → 1912); mati MEH = babica familija!; botra Miklavž Šelko? [~] + Ana Podbrec; babica Marija Meh; podpis Paulin Bitnar",
    whatEn: "baptized Jožef (died Nov 26, 1930 — aged 18) (Feb 3/4) — father Anton Podlavrič? [~], a three-quarter smallholder, mother Katarina Meh; h26 = the 5th ENTRY (1887, 1889, 1896, 1906 → 1912); the mother MEH = the midwife family!; godparents Miklavž Šelko? [~] + Ana Podbrec; midwife Marija Meh; signature Paulin Bitnar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1912,
    scan: 229,
    page: 202,
    whatSi: "krščen Bogomir (4./5. 2.) — oče France Kalan [poklic ?ulst vrsjc — neberljiv], mati Marija Verhovnik; h90 = 7. VPIS (1890–1910); KALAN = učiteljska familija (h90 1905–1910 Kalan Vincencij učitelj — P105!); **RAZVEZAL zakonsko zvezo dne 15.01.1953 v Ljubljani** (1. razveljavitev 1912) + zlato poroka pripis; botra Janez Podbrec + Katarina Podina? [~ Logira?]; babica Ana Marijeta? [~]; podpis Paulin Bitnar; beli trak: † 14.04.2003 (Matričarka Šimončič; Kalčič Klas)",
    whatEn: "baptized Bogomir (Feb 4/5) — father France Kalan [the trade ?ulst vrsjc — illegible], mother Marija Verhovnik; h90 = the 7th ENTRY (1890–1910); KALAN = the teacher family (h90 1905–1910 Kalan Vincencij the teacher — P105!); **HE DISSOLVED his marriage on Jan 15, 1953 in Ljubljana** (the 1st annulment of 1912) + a golden-wedding note; godparents Janez Podbrec + Katarina Podina? [~ Logira?]; midwife Ana Marijeta? [~]; signature Paulin Bitnar; the white strip: died Apr 14, 2003 (the registrar Šimončič; Kalčič Klas)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "71",
    bookSignature: "04105",
    year: 1912,
    scan: 230,
    page: 203,
    whatSi: "krščena Juli (+23.9.1912 — dojenček) (18./19. 2. [~]) — oče Anton Lovrec, zemljak, mati Barbara Hrižan; h71 = 3. VPIS (1890, 1894 → 1912); **VRZEL 18 LET**; botra Janez Capič? [~ Dapič?] + Katarina Capič? [~]; babica Marija Meh; podpis Jos. Rauq; dojenček †; datumi 18|19 [~ — 1. števke slabo vidne; kronologija Feb 8→13→18]",
    whatEn: "baptized Juli (died Sep 23, 1912 — an infant) (Feb 18/19 [~]) — father Anton Lovrec, a smallholder, mother Barbara Hrižan; h71 = the 3rd ENTRY (1890, 1894 → 1912); **an 18-YEAR GAP**; godparents Janez Capič? [~ Dapič?] + Katarina Capič? [~]; midwife Marija Meh; signature Jos. Rauq; an infant died; the dates 18|19 [~ — the leading 1s faint; the chronology Feb 8→13→18]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1912,
    scan: 230,
    page: 203,
    whatSi: "krščen Jakob (20./21. 3.) — oče Janez Dragoš ¾ zemljak, mati Nara Cvitkovič; h12 = 13. VPIS (1892–1909); botra Marija Štrucelj + Katarina Toller; babica Ana Adlešič; podpis Paulin Bitnar; poročen 15.5.1943 [~]; **† 14.9.1987 v Trupoli = TRIPOLI!** (MKU NO, str. 12, zap. št. 24; 14.10.1987) — eksotična smrt (delo v tujini?); DRAGOŠ × CVITKOVIČ cf. P104 h12 ISTA ZVEZA",
    whatEn: "baptized Jakob (Mar 20/21) — father Janez Dragoš, a three-quarter smallholder, mother Nara Cvitkovič; h12 = the 13th ENTRY (1892–1909); godparents Marija Štrucelj + Katarina Toller; midwife Ana Adlešič; signature Paulin Bitnar; married May 15, 1943 [~]; **died Sep 14, 1987 in Trupoli = TRIPOLI!** (MKU NO, p. 12, file no. 24; Oct 14, 1987) — an exotic death (work abroad?); DRAGOŠ × CVITKOVIČ cf. P104 h12 the SAME COUPLE",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04105",
    year: 1912,
    scan: 231,
    page: 204,
    whatSi: "krščena Barbara (2./3. 5.) — **ANOMALIJA A1: v koloni očeta ŽENSKO ime »Marija Tomec ¾ zemljak«** + mati kolona Marija Krambič = dvojna mati / nezakonska z napako duhovnika (1. primer vzorca!); h18 = 5. VPIS (1898, 1906, 1907, 1910 → 1912); botra Janez Muc + Ana Jakljič; babica Marija Meh; podpis Jos. Rauq; † 28.8.1980 Griblje (MKU, str. 17, zap. št. 5; Gradec 5.12.1980)",
    whatEn: "baptized Barbara (May 2/3) — **ANOMALY A1: the father column carries a WOMAN'S name »Marija Tomec, a three-quarter smallholder«** + the mother column Marija Krambič = a double mother / an out-of-wedlock birth with a priest's error (the 1st case of the sample!); h18 = the 5th ENTRY (1898, 1906, 1907, 1910 → 1912); godparents Janez Muc + Ana Jakljič; midwife Marija Meh; signature Jos. Rauq; died Aug 28, 1980 in Griblje (MKU, p. 17, file no. 5; Gradec Dec 5, 1980)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1912,
    scan: 231,
    page: 204,
    whatSi: "krščena Marija (11./12. 5.) — oče **Miko Alek ¾ zemljak — MLINAR** (potrjen 1913 r2 Kranjak 15: »Miko Alek mlinar« — P108 lead!), mati Ana Žunič; h22 = 6. VPIS (1899–1910); botra Jakob Bohle + Ana Požek; babica [PRAZNA] (2. v 1912); podpis Paulin Bitnar; EMŠO 1106912505630 — mesec 06 vs register 05 (Maj) — MOŽEN DATUMSKI POPRAVEK [~]; † 16.1.1983 Griblje (MKU štov. Griblje, št. 122, zap. št. 2; 31.1.1983); Bohle cf. h66 (P104) + Požek signal",
    whatEn: "baptized Marija (May 11/12) — father **Miko Alek, a three-quarter smallholder — A MILLER** (confirmed by 1913 r2 Kranjak 15: »Miko Alek mlinar« — the P108 lead!), mother Ana Žunič; h22 = the 6th ENTRY (1899–1910); godparents Jakob Bohle + Ana Požek; midwife [EMPTY] (the 2nd of 1912); signature Paulin Bitnar; personal ID 1106912505630 — the month 06 vs the register 05 (May) — a POSSIBLE BIRTH-DATE CORRECTION [~]; died Jan 16, 1983 in Griblje (MKU Griblje station, no. 122, file no. 2; Jan 31, 1983); Bohle cf. h66 (P104) + the Požek signal",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1912,
    scan: 231,
    page: 204,
    whatSi: "krščena Jožefa (+16.11.1937 — 25 let) (25./25. 5.) — oče Janez Brinec ¾ zemljak, mati Ana Alek; **h24 = 16. VPIS — NOV REKORD HIŠE!** (prej 15: 1887–1911; ZAPORED 2. leto 1911+1912!); botra Matija Alek + Marija Brinec (mati familija + očeva familija — kombinacija!); babica [branje nejasno]; podpis Paulin Bitnar",
    whatEn: "baptized Jožefa (died Nov 16, 1937 — aged 25) (May 25/25) — father Janez Brinec, a three-quarter smallholder, mother Ana Alek; **h24 = the 16th ENTRY — A NEW HOUSE RECORD!** (the previous 15: 1887–1911; CONSECUTIVE the 2nd year 1911+1912!); godparents Matija Alek + Marija Brinec (the mother's family + the father's family — a combination!); midwife [illegible reading]; signature Paulin Bitnar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "19",
    bookSignature: "04105",
    year: 1912,
    scan: 231,
    page: 204,
    whatSi: "krščena Ana (28./29. 5.) — oče Jožef Podbrec ¾ zemljak, mati Ana Hrižan; h19 = 3. VPIS (1901, 1906 → 1912); VRZEL 6 LET; botra Matija Alek + Katarina Hrižan (HRIŽAN kontinuiteta); babica Marija Meh; podpis Paulin Bitnar; EMŠO 2806912505946 — SKLADNO — SIDRO (28.6.1912; 10. števka 6 = ženska); maticar Vida Simončič 09.03.2001; † 21.1.1995 Črnomelj (MKU NO, str. 54, zap. št. 3)",
    whatEn: "baptized Ana (May 28/29) — father Jožef Podbrec, a three-quarter smallholder, mother Ana Hrižan; h19 = the 3rd ENTRY (1901, 1906 → 1912); a 6-YEAR GAP; godparents Matija Alek + Katarina Hrižan (the HRIŽAN continuity); midwife Marija Meh; signature Paulin Bitnar; personal ID 2806912505946 — CONSISTENT — an ANCHOR (Jun 28, 1912; the 10th digit 6 = female); registrar Vida Simončič Mar 9, 2001; died Jan 21, 1995 Črnomelj (MKU NO, p. 54, file no. 3)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1912,
    scan: 234,
    page: 206,
    whatSi: "krščena Amalija (28./28. 7.) — oče Jožef Podbrec? [~ Perdbrec?] ¾ zemljak, mati Katarina Beršaper? [~]; h48 = 6. VPIS (1897–1911; ZAPORED 2. leto!); hiša 48/43 [~ — 2 branja]; botra Joža Podbrec + Marija Brodarič; babica Marija Meh; podpis Paulin Bitnar; EMŠO 2807912505918 — SKLADNO — SIDRO (28.7.1912); poročena 5.3.1932; † 11.4.1995 (maticar Ana Všuonič 09.03.2001)",
    whatEn: "baptized Amalija (Jul 28/28) — father Jožef Podbrec? [~ Perdbrec?], a three-quarter smallholder, mother Katarina Beršaper? [~]; h48 = the 6th ENTRY (1897–1911; CONSECUTIVE the 2nd year!); the house 48/43 [~ — 2 readings]; godparents Joža Podbrec + Marija Brodarič; midwife Marija Meh; signature Paulin Bitnar; personal ID 2807912505918 — CONSISTENT — an ANCHOR (Jul 28, 1912); married Mar 5, 1932; died Apr 11, 1995 (registrar Ana Všuonič Mar 9, 2001)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "33",
    bookSignature: "04105",
    year: 1912,
    scan: 235,
    page: 207,
    whatSi: "krščena Terezija (5./5.? 10. [~]) — oče Martin Papič [piše se variabilno: Papič/Tapič/Caprič — cf. 1909/1911!] ¾ zemljak, mati Ana Tomc; h33 = 5. VPIS (1889, 1898, 1909, 1911 → 1912; ZAPORED 2. leto!); **GENETSKA VAS ×2: napisano »Grišice« — GENETSKO GRIBLJE 33** (cf. P106 r37; ISTI oče Martin + ISTA hiša 33 — 2. potrjena »Grišice«!); botra Peter Kralj + Ana Kralj; babica Marija Pletoj? [~]; podpis Paulin Bitnar; poročena 28.6.1950 (priča Jožefom, v Metliki); † 7.11.1985 Novo mesto (zap. št. 841)",
    whatEn: "baptized Terezija (Oct 5/5? [~]) — father Martin Papič [written variably: Papič/Tapič/Caprič — cf. 1909/1911!], a three-quarter smallholder, mother Ana Tomc; h33 = the 5th ENTRY (1889, 1898, 1909, 1911 → 1912; CONSECUTIVE the 2nd year!); **THE GENETIC VILLAGE ×2: written »Grišice« — GENETICALLY GRIBLJE 33** (cf. P106 r37; the SAME father Martin + the SAME house 33 — the 2nd confirmed »Grišice«!); godparents Peter Kralj + Ana Kralj; midwife Marija Pletoj? [~]; signature Paulin Bitnar; married Jun 28, 1950 (witnessed by the Jožefs, in Metlika); died Nov 7, 1985 Novo mesto (file no. 841)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "86",
    bookSignature: "04105",
    year: 1912,
    scan: 237,
    page: 208,
    whatSi: "krščena Alojzija (20./20. 10.) — oče Peter Brinec, bajtar, mati Ana Butala; **h86 = 1. VPIS — NOVA HIŠA VZORCA!** (prva po 1909: 0/1/0/0/0/0/0/0/1 — prelomsko leto!); celotna botra+babica = OČEVA familija (Brinec ×3!): Janez + Doroteja Brinec + Barbara Brinec; podpis Paulin Bitnar; EMŠO 2010912506419 [~] — SKLADNO — SIDRO (20.10.1912); modri pripis: sklenila zakonsko zvezo 25.11.1946, priimek Sprem, Koprivnica (poroka 1946!)",
    whatEn: "baptized Alojzija (Oct 20/20) — father Peter Brinec, a cottager, mother Ana Butala; **h86 = the 1st ENTRY — A NEW SAMPLE HOUSE!** (the first since 1909: 0/1/0/0/0/0/0/0/1 — a breaking year!); the entire godparents+midwife = the FATHER's family (Brinec ×3!): Janez + Doroteja Brinec + Barbara Brinec; signature Paulin Bitnar; personal ID 2010912506419 [~] — CONSISTENT — an ANCHOR (Oct 20, 1912); the blue note: married Nov 25, 1946, the surname Sprem, Koprivnica (a 1946 marriage!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1912,
    scan: 237,
    page: 208,
    whatSi: "krščen Mihael († 29.7.1930 — 17 let) (20./21. 11.) — oče Miklavž Brodarič ¾ zemljak, mati Sara Jevanov? [~ Juranč?]; h40 = 5. VPIS (1897, 1898, 1899, 1911 → 1912); botra Janez Želj + Ana Podbrec? [~]; babica Marija Jakofčič; podpis Jos. Rauq; **November glava skrita pod belim trakom r79** (maticar 1995)",
    whatEn: "baptized Mihael (died Jul 29, 1930 — aged 17) (Nov 20/21) — father Miklavž Brodarič, a three-quarter smallholder, mother Sara Jevanov? [~ Juranč?]; h40 = the 5th ENTRY (1897, 1898, 1899, 1911 → 1912); godparents Janez Želj + Ana Podbrec? [~]; midwife Marija Jakofčič; signature Jos. Rauq; **the November heading hidden under the white strip r79** (the registrar 1995)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1912,
    scan: 239,
    page: 209,
    whatSi: "krščen Anton (+18.1.1913 [~] — dojenček) (23./23. 12.) — oče Matija Štrucelj (»je ženit« — nezakonski signal [~]), mati Marija Meh; h5 = 6. VPIS (1891–1910); **MATI + BOTRINJA = MEH ×2** (Marija Meh + Bara Meh — familija! cf. P105 r83 mati+babica MEH); botra Janez Dragoš + Bara Meh (»sestra«?); babica Bara Adlešič; podpis Paulin Bitnar; dojenček †; ŠTRUCELJ × MEH cf. h5 1905/1910 (Štrucelj × Meh 5. skupaj — P105!); **glava 1913 INLINE str. 209 DNO** (s239/240 — pod r88!) — P108 lead: 1913 r1 = Cerkvišče 31? Marija (4./10. Januar, EMŠO 0401913505350; Januar 1913 IMA vpise na str. 209 dnu) — h5 r87 = ZADNJA Griblje vrstica 1912",
    whatEn: "baptized Anton (died Jan 18, 1913 [~] — an infant) (Dec 23/23) — father Matija Štrucelj (»je ženit« — an out-of-wedlock signal [~]), mother Marija Meh; h5 = the 6th ENTRY (1891–1910); **THE MOTHER + THE GODMOTHER = MEH ×2** (Marija Meh + Bara Meh — the family! cf. P105 r83 mother+midwife MEH); godparents Janez Dragoš + Bara Meh (»sister«?); midwife Bara Adlešič; signature Paulin Bitnar; an infant died; ŠTRUCELJ × MEH cf. h5 1905/1910 (Štrucelj × Meh the 5th together — P105!); **the 1913 heading INLINE at the bottom of p. 209** (s239/240 — below r88!) — the P108 lead: 1913 r1 = Cerkvišče 31? Marija (Jan 4/10, personal ID 0401913505350; January 1913 HAS entries at the bottom of p. 209) — h5 r87 = the LAST Griblje row of 1912",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1913,
    scan: 241,
    page: 210,
    whatSi: "krščena Vida (⚰ 16.8.1916 — umrla pri 3,5 letih) (13./13. 2.) — oče Janez Teprič? [~ Zupan? popravek forenzike 3×] ¼ zemljak, mati Štefancva Šrajgar? [~ KOLIZIJA z r9 — isti priimek matere]; h31 = 11. VPIS (1887–1911); VRZEL 2 LETI; **h31 ×2 v 1913 (r10 + r70) — NARE PRELOM — 1. ponovitev od P104!** + **DVE RAZLIČNI FAMILIJI v h31 isto leto** (r10 Teprič? × Šrajgar? vs r70 Černič × Počelf? — hišna delitev? selitev? cf. h31 Papič/Gapič kolizija P106); botra Anton Lozar + Barbara Lozar (½ zemljak); babica Ana Mavrenič; podpis Jos. Rauq; otrok †",
    whatEn: "baptized Vida (died Aug 16, 1916 — aged 3.5) (Feb 13/13) — father Janez Teprič? [~ Zupan? corrected by 3× forensics] quarter smallholder, mother Štefancva Šrajgar? [~ a COLLISION with r9 — the same mother surname]; h31 = the 11th ENTRY (1887–1911); a 2-YEAR GAP; **h31 ×2 in 1913 (r10 + r70) — the NARE BREAK — the 1st repeat since P104!** + **TWO DIFFERENT FAMILIES in h31 the same year** (r10 Teprič? × Šrajgar? vs r70 Černič × Počelf? — a house division? a move? cf. the h31 Papič/Gapič collision P106); godparents Anton Lozar + Barbara Lozar (half smallholder); midwife Ana Mavrenič; signature Jos. Rauq; the child died",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04105",
    year: 1913,
    scan: 241,
    page: 210,
    whatSi: "krščena Marija (⚰ 1.1.1917 — forenzika: faza-1 »+1.1.1913?« NAPAČNO, »Ⓗ 1. I. 1917« jasno) (16./16. 2.) — oče Arnold? Jakofčič? [~ Rakob? — 4× forenzika] ¼ zemljak, mati Klepec Terezija?; h9 = 3. VPIS (1896, 1900 → 1913); **VRZEL 13 LET — najdaljša 1913**; botra Janez Žunec? + Ana Šparatič? (½ zemljak); babica Marija Pleščič; podpis Paulin Bitnar; modra † marginalia »Umel 4.10.19..« [~ kolizija s sosednjo vrstico]",
    whatEn: "baptized Marija (died Jan 1, 1917 — forensics: the phase-1 »+Jan 1, 1913?« WRONG, »Ⓗ Jan 1, 1917« clear) (Feb 16/16) — father Arnold? Jakofčič? [~ Rakob? — 4× forensics] quarter smallholder, mother Klepec Terezija?; h9 = the 3rd ENTRY (1896, 1900 → 1913); **a 13-YEAR GAP — the longest of 1913**; godparents Janez Žunec? + Ana Šparatič? (half smallholder); midwife Marija Pleščič; signature Paulin Bitnar; a blue death marginalia »Umel 4.10.19..« [~ a collision with the neighbouring row]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "65",
    bookSignature: "04105",
    year: 1913,
    scan: 241,
    page: 210,
    whatSi: "krščen Jožef (22./23. 2.) — oče Matija Milek [~ Milfelt? — 3× forenzika] ¼ zemljak, mati Marija Pezdič? [~]; h65 = 11. VPIS (1887–1910; P105 popravek matičarja »št. 45« NAPAČEN!); VRZEL 3 LETA; **VRNJEN V SEZNAM: faza-1 surova transkripcija je r15 IZPUSTILA (navedla 17 vpisov) — forenzika s241-A POTRJUJE vas Griblje + hiša 65 + oče Milek SKLADNO s h65 MILEK kontinuiteto!** → 18 Griblje vpisov 1913; botra Peter Pondriice? + Valerijana Pezdič? (¼ zemljak; botrinja = ISTI PRIIMEK kot mati — familija!); babica Barbara Adlešič; podpis Paulin Bitnar; EMŠO marginalia 2502913505841? = kolizija z r16 (verjetno r16-ina)",
    whatEn: "baptized Jožef (Feb 22/23) — father Matija Milek [~ Milfelt? — 3× forensics] quarter smallholder, mother Marija Pezdič? [~]; h65 = the 11th ENTRY (1887–1910; the P105 registrar's correction »no. 45« WRONG!); a 3-YEAR GAP; **RESTORED TO THE LIST: the phase-1 raw transcription OMITTED r15 (listing 17 entries) — the s241-A forensics CONFIRM the village Griblje + house 65 + father Milek CONSISTENT with the h65 MILEK continuity!** → 18 Griblje entries 1913; godparents Peter Pondriice? + Valerijana Pezdič? (quarter smallholder; the godmother = the SAME SURNAME as the mother — the family!); midwife Barbara Adlešič; signature Paulin Bitnar; the ID marginalia 2502913505841? = a collision with r16 (probably r16's)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1913,
    scan: 243,
    page: 211,
    whatSi: "krščena Barbura (⚰ 7.11.1913 — dojenček †) (7./8. 3.) — oče Janez Jakofčič ¼ zemljak, mati Štefanija Jakofčič; h6 = 7. VPIS (1904–1911); VRZEL 2 LETI; botra Jožef Željko? + Marija Mehle? (½ zemljak); babica Marija Jakofčič (Jakofčič kampanja 1913!); podpis Jos. Rauq",
    whatEn: "baptized Barbura (died Nov 7, 1913 — an infant died) (Mar 7/8) — father Janez Jakofčič quarter smallholder, mother Štefanija Jakofčič; h6 = the 7th ENTRY (1904–1911); a 2-YEAR GAP; godparents Jožef Željko? + Marija Mehle? (half smallholder); midwife Marija Jakofčič (the Jakofčič campaign 1913!); signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04105",
    year: 1913,
    scan: 243,
    page: 211,
    whatSi: "krščena Marija (⚰ 7/6.19.. [~]) (29./29. 3.) — oče Janez Jakofčič? [~ Jakobič] ¼ zemljak, mati Neža Jakljevič?; h8 = 5. VPIS (1886, 1888, 1889, 1912 → 1913) — **ZAPORED 2. leto** (po P107 VRZEL 23 LET REKORD!); ISTA ZVEZA Janez Jakofčič × Neža Jakljevič kot 1912 — SKLADNO; botra Jakob Völler + Štefanija Völler (½ zemljak; ISTI boter Völler/Toller kot 1912 h8 — POVRAČNICA 2. leto!); babica Marija Jakofčič; podpis Paulin Bitnar",
    whatEn: "baptized Marija (died Jun 7, 19xx [~]) (Mar 29/29) — father Janez Jakofčič? [~ Jakobič] quarter smallholder, mother Neža Jakljevič?; h8 = the 5th ENTRY (1886, 1888, 1889, 1912 → 1913) — **CONSECUTIVE the 2nd year** (after the P107 23-YEAR GAP RECORD!); the SAME COUPLE Janez Jakofčič × Neža Jakljevič as 1912 — CONSISTENT; godparents Jakob Völler + Štefanija Völler (half smallholder; the SAME godfather Völler/Toller as 1912 h8 — the RETURNEE the 2nd year!); midwife Marija Jakofčič; signature Paulin Bitnar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "28",
    bookSignature: "04105",
    year: 1913,
    scan: 245,
    page: 212,
    whatSi: "krščen Anton (10./11. 4.) — oče Anton Lozar ¼ zemljak, mati Barbara Šrimar; h28 = 3. VPIS (1891, 1910 → 1913); VRZEL 3 LETA; **1910 NEZAKONSKA → 1913 OČE LOZAR** (očakovsko v 1910 brez — zdaj vpisan); botra Janez Zabič? + Štefanija Zabič? (½ zemljak); babica Marija Pleščič; podpis Jos. Rauq; EMŠO 1004913500031 — SKLADNO (10.4.1913; 11.–12. števka 03 = moški) — SIDRO; † 10.09.1985 Griblje — 72 let (MKU Griblje 8.1985, str. 129, zap. št. 2); poročen 7.2.19..",
    whatEn: "baptized Anton (Apr 10/11) — father Anton Lozar quarter smallholder, mother Barbara Šrimar; h28 = the 3rd ENTRY (1891, 1910 → 1913); a 3-YEAR GAP; **1910 OUT-OF-WEDLOCK → 1913 THE FATHER LOZAR** (the fatherhood absent in 1910 — now entered); godparents Janez Zabič? + Štefanija Zabič? (half smallholder); midwife Marija Pleščič; signature Jos. Rauq; personal ID 1004913500031 — CONSISTENT (Apr 10, 1913; the 11th–12th digits 03 = male) — an ANCHOR; died Sep 10, 1985 in Griblje — aged 72 (MKU Griblje 8.1985, p. 129, file no. 2); married Feb 7, 19xx",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1913,
    scan: 245,
    page: 212,
    whatSi: "krščen Anton (23./24. 4.) — oče Jožef Štrucelj ¼ zemljak (h44 SKLADNO!), mati Barbara Černe; h44 = 6. VPIS (1888, 1901, 1906, 1908, 1910 → 1913); VRZEL 3 LETA; **PAPIRNI VSTAVEK »Pozamanitev« čez vrstico** (Kosec Jakob pocigan? × Katarina Hudovirac ciganka — otrok Leopold — potujoča družina — unikat vzorca!; podpisa Štefanič Martin župnik + Kostlivšek? Franc kaplan); hiša »44 (98?)« pod vstavkom — 44 SKLADNO; botra delno pod vstavkom [faza-1: Janez Černe? + Marijeta Štraus?]; babica Marija Jakofčič; podpis Jos. Rauq; † 27.4.1994",
    whatEn: "baptized Anton (Apr 23/24) — father Jožef Štrucelj quarter smallholder (h44 CONSISTENT!), mother Barbara Černe; h44 = the 6th ENTRY (1888, 1901, 1906, 1908, 1910 → 1913); a 3-YEAR GAP; **A PAPER INSERT »Pozamanitev« across the row** (Kosec Jakob, a tinsmith? × Katarina Hudovirac, a Roma woman — the child Leopold — a travelling family — a UNIQUE of the sample!; signed by Štefanič Martin the dean + Kostlivšek? Franc the chaplain); house »44 (98?)« under the insert — 44 CONSISTENT; godparents partly under the insert [phase-1: Janez Černe? + Marijeta Štraus?]; midwife Marija Jakofčič; signature Jos. Rauq; died Apr 27, 1994",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04105",
    year: 1913,
    scan: 245,
    page: 212,
    whatSi: "krščen Stanislav (4./5. 5.) — oče Matija Štraus ¼ zemljak [prvo branje »Marija« NAPAČNO — popravek forenzike], mati Marjeta Šimec; h72 = 8. VPIS (1888–1911); VRZEL 2 LETI; **ZAPORED ISTA ZVEZA Strauš/Štraus × Šimec: 1909 + 1911 + 1913 (3. skupaj!)**; botra Mika? Jakofčič + Barbana Jakofčič; babica Marija Jakofčič; podpis Jos. Rauq; marginalia »24.11.1937 je prevzel v šlevišče?...«",
    whatEn: "baptized Stanislav (May 4/5) — father Matija Štraus quarter smallholder [the first reading »Marija« WRONG — corrected by forensics], mother Marjeta Šimec; h72 = the 8th ENTRY (1888–1911); a 2-YEAR GAP; **CONSECUTIVE the SAME COUPLE Strauš/Štraus × Šimec: 1909 + 1911 + 1913 (the 3rd together!)**; godparents Mika? Jakofčič + Barbana Jakofčič; midwife Marija Jakofčič; signature Jos. Rauq; a marginalia »Nov 24, 1937 he took up in the...«",
    status: "DOCUMENTED",
  },
  {
    houseNo: "59",
    bookSignature: "04105",
    year: 1913,
    scan: 251,
    page: 213,
    whatSi: "krščena Marija (⚰ 3/6.1913 — dojenček †) (12./12. 5.) — oče Janez Jaklič [nova?] ¼ zemljak, mati Ana Hrambič; h59 = 4. VPIS (1889, 1899, 1912 → 1913) — **ZAPORED 2. leto**; oče Janez cf. 1912 h59 France Jaklič (MENJAVA očeta France → Janez? ali isti — [~]); botra Alojzij Novak + Barbara Krambič? (botrinja = ISTA kot 1912 h59 — POVRAČNICA 2. leto!); babica Barbara Adlešič; podpis Paulin Bitnar; »Cer. poročen 6.10.1936«",
    whatEn: "baptized Marija (died Jun 3, 1913 — an infant died) (May 12/12) — father Janez Jaklič [nova?] quarter smallholder, mother Ana Hrambič; h59 = the 4th ENTRY (1889, 1899, 1912 → 1913) — **CONSECUTIVE the 2nd year**; the father Janez cf. 1912 h59 France Jaklič (a FATHER CHANGE France → Janez? or the same — [~]); godparents Alojzij Novak + Barbara Krambič? (the godmother = the SAME as 1912 h59 — the RETURNEE the 2nd year!); midwife Barbara Adlešič; signature Paulin Bitnar; »church-married Oct 6, 1936«",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1913,
    scan: 251,
    page: 213,
    whatSi: "krščen Anton (⚰ 9/9.1913 — dojenček †) (8./9. 6.) — oče Janez Krambič ¼ zemljak, mati Marija Milek? [~ Mehelf]; **h34 MENJAVA DRUŽINE**: 1910/11 Janez Brinec × Ana Milek → 1913 Janez Krambič × Marija Milek? — mati familija MILEK obstane!; h34 = 9. VPIS (1887–1910); VRZEL 3 LETA; botra Marija Volek? + Katarina Frus?; babica Barbara Adlešič; podpis Jos. Rauq",
    whatEn: "baptized Anton (died Sep 9, 1913 — an infant died) (Jun 8/9) — father Janez Krambič quarter smallholder, mother Marija Milek? [~ Mehelf]; **h34 A FAMILY CHANGE**: 1910/11 Janez Brinec × Ana Milek → 1913 Janez Krambič × Marija Milek? — the mother family MILEK persists!; h34 = the 9th ENTRY (1887–1910); a 3-YEAR GAP; godparents Marija Volek? + Katarina Frus?; midwife Barbara Adlešič; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1913,
    scan: 252,
    page: 214,
    whatSi: "krščena Ivana (22./23. 7.) — oče **Matija Jakofčič [REŠENO — faza-1 dvom »Marija→Matija?« POTRJEN 4× forenziko; cf. P107 r32 žensko-ime signal]** ¼? zemljak, mati Marija Jakofčič? [~]; h13 = 6. VPIS (1886, 1888, 1894, 1907, 1911 → 1913); VRZEL 2 LETI; Jakofčič kontinuiteta SKLADNO (1911 menjava #2 → Jakofič); **OČE + MATI + BOTRINJA + BABICA = JAKOFČIČ ×4** (celotna familija!); botra Jožef Željko? + Štefanija Jakofčič (½ zemljak); babica Marija Jakofčič; podpis Paulin Bitnar; +20.5.1946",
    whatEn: "baptized Ivana (Jul 22/23) — father **Matija Jakofčič [RESOLVED — the phase-1 doubt »Marija→Matija?« CONFIRMED by 4× forensics; cf. the P107 r32 female-name signal]** quarter? smallholder, mother Marija Jakofčič? [~]; h13 = the 6th ENTRY (1886, 1888, 1894, 1907, 1911 → 1913); a 2-YEAR GAP; the Jakofčič continuity CONSISTENT (the 1911 change #2 → Jakofič); **THE FATHER + THE MOTHER + THE GODMOTHER + THE MIDWIFE = JAKOFČIČ ×4** (the whole family!); godparents Jožef Željko? + Štefanija Jakofčič (half smallholder); midwife Marija Jakofčič; signature Paulin Bitnar; died May 20, 1946",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1913,
    scan: 253,
    page: 215,
    whatSi: "krščen Julij (⚰ 24/6 19.. [~]) (8./9. 8.) — oče Jožef Černič ¼ zemljak, mati Ana Počelf? [~]; **h31 = 12. VPIS — h31 ×2 v 1913 (r10 + r70) = NARE PRELOM (1. ponovitev od P104!)**; **DVE RAZLIČNI FAMILIJI v isti hiši isto leto** (r10 Teprič? × Šrajgar? + r70 Černič × Počelf? — hišna delitev/selitev? anomalijska dilema — obe vpisani); botra Janez Matič? + Štefanija Kovač? (½ zemljak); babica Marija Jakofčič; podpis Jos. Rauq; otrok/dojenček †",
    whatEn: "baptized Julij (died Jun 24, 19xx [~]) (Aug 8/9) — father Jožef Černič quarter smallholder, mother Ana Počelf? [~]; **h31 = the 12th ENTRY — h31 ×2 in 1913 (r10 + r70) = the NARE BREAK (the 1st repeat since P104!)**; **TWO DIFFERENT FAMILIES in the same house the same year** (r10 Teprič? × Šrajgar? + r70 Černič × Počelf? — a house division/move? an anomalous dilemma — both entered); godparents Janez Matič? + Štefanija Kovač? (half smallholder); midwife Marija Jakofčič; signature Jos. Rauq; the child/infant died",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1913,
    scan: 253,
    page: 215,
    whatSi: "krščena Angela (20./20. 8.) — oče Janez Hrižan ¼ zemljak, mati Katarina Hrucelj? [~ Štrucelj?]; h36 = 11. VPIS (1886–1912) — **ZAPORED 3. leto** (1911 + 1912 + 1913!); **HRIŽAN kontinuiteta SKLADNO** (oče Janez cf. P106 h36 HRIŽAN + P107 h36 Marko Hrižan); **SELIJA h36 → h86: P107 h36 par (Marko Hrižan × Katarina Štraus) zdaj v h86 (r75) — 3. selitev vzorca!**; botra Marija Pezdirec + Marijeta Štraus; babica Marija Jakofčič; podpis Paulin Bitnar; EMŠO 2008913505094 — SKLADNO (20.8.1913; 11.–12. števka 50 = ženska) — SIDRO; † 04.10.2004 Nova Gorica — 91 let (MKU MO NG 1.2004, str. 209; 26.12.2004)",
    whatEn: "baptized Angela (Aug 20/20) — father Janez Hrižan quarter smallholder, mother Katarina Hrucelj? [~ Štrucelj?]; h36 = the 11th ENTRY (1886–1912) — **CONSECUTIVE the 3rd year** (1911 + 1912 + 1913!); **the HRIŽAN continuity CONSISTENT** (the father Janez cf. P106 h36 HRIŽAN + P107 h36 Marko Hrižan); **A MOVE h36 → h86: the P107 h36 couple (Marko Hrižan × Katarina Štraus) now in h86 (r75) — the 3rd move of the sample!**; godparents Marija Pezdirec + Marijeta Štraus; midwife Marija Jakofčič; signature Paulin Bitnar; personal ID 2008913505094 — CONSISTENT (Aug 20, 1913; the 11th–12th digits 50 = female) — an ANCHOR; died Oct 4, 2004 in Nova Gorica — aged 91 (MKU MO NG 1.2004, p. 209; Dec 26, 2004)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "86",
    bookSignature: "04105",
    year: 1913,
    scan: 253,
    page: 215,
    whatSi: "krščen Janez (25./26. 8.) — oče Marko Hrižan ¼ zemljak [~ ¾ cf. P107 h36], mati Katarina Štraus; h86 = 2. VPIS (nova hiša 1912); **SELIJA h36 → h86** (P107 h36 par Marko Hrižan × Katarina Štraus — **3. selitev vzorca**: cf. h30→h10 1909 + h10→h70 1912!); botra Martin Gornik? + Marija Gornik?; babica Marija Pleščič; podpis Jos. Rauq; EMŠO 2508913505169 — SKLADNO (25.8.1913; 11.–12. števka 16 = moški) — SIDRO; † 21.03.1992 Črnomelj (MKU Črnomelj 1.1992, str. 98, zap. 119; 25.03.1992)",
    whatEn: "baptized Janez (Aug 25/26) — father Marko Hrižan quarter smallholder [~ ¾ cf. P107 h36], mother Katarina Štraus; h86 = the 2nd ENTRY (the new house of 1912); **A MOVE h36 → h86** (the P107 h36 couple Marko Hrižan × Katarina Štraus — **the 3rd move of the sample**: cf. h30→h10 1909 + h10→h70 1912!); godparents Martin Gornik? + Marija Gornik?; midwife Marija Pleščič; signature Jos. Rauq; personal ID 2508913505169 — CONSISTENT (Aug 25, 1913; the 11th–12th digits 16 = male) — an ANCHOR; died Mar 21, 1992 in Črnomelj (MKU Črnomelj 1.1992, p. 98, file no. 119; Mar 25, 1992)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "76",
    bookSignature: "04105",
    year: 1913,
    scan: 254,
    page: 216,
    whatSi: "krščena Vilhelmina (⚰ 16/9.1913 — dojenček †) (9./11. 9.) — oče Janez Kramec? [~ Kranec] šoždar? [~ poklic — redkost!], mati Alojzija Muc; **h76 = NOVA HIŠA VZORCA** (prvi vpis v vseh treh knjigah 04105+04894+04455!) — **2. leto ZAPORED z novo hišo** (h86 1912 → h76 1913: 0/1/0/0/0/0/0/0/1/1!); PT SKLADNO (hiša 76 v 1825 naboru PT); botra Jožif? Vranetič? (kovač) + Neža Vranetič? (njegova žena); babica Ana Mavrenič; podpis Jos. Rauq; mati MUC (velika župnijska familija cf. r26 + r64)",
    whatEn: "baptized Vilhelmina (died Sep 16, 1913 — an infant died) (Sep 9/11) — father Janez Kramec? [~ Kranec], a shoemaker? [~ a trade — a rarity!], mother Alojzija Muc; **h76 = A NEW HOUSE OF THE SAMPLE** (the first entry in all three books 04105+04894+04455!) — **the 2nd CONSECUTIVE year with a new house** (h86 1912 → h76 1913: 0/1/0/0/0/0/0/0/1/1!); the PT CONSISTENT (house 76 in the 1825 PT set); godparents Jožif? Vranetič? (a blacksmith) + Neža Vranetič? (his wife); midwife Ana Mavrenič; signature Jos. Rauq; the mother MUC (a large parish family cf. r26 + r64)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1913,
    scan: 254,
    page: 216,
    whatSi: "krščen Frančišek (28./29. 9.) — oče Anton Brodarič ¼ zemljak, mati Katarina Milek? [~ Mehelf]; h46 = 9. VPIS (1893–1912) — ZAPORED 2. leto (cf. 1912 h46 DVOJČKI); botra Nikolaj Željko? + Ana Pezdirec? (¼ zemljak); babica Marija Jakofčič; podpis **R. Ozlob? Polak, kap.** — NOVI PODPIS (3. duhovnik 1913; blok r82–r87 s254!); EMŠO 2809913500032 — SKLADNO (28.9.1913; 11.–12. števka 03 = moški) — SIDRO; † 03.12.1978 Slovenj Gradec — 83 let (MKU MO SG 8.1978, str. 52, zap. 509; 24.01.1979)",
    whatEn: "baptized Frančišek (Sep 28/29) — father Anton Brodarič quarter smallholder, mother Katarina Milek? [~ Mehelf]; h46 = the 9th ENTRY (1893–1912) — CONSECUTIVE the 2nd year (cf. the 1912 h46 TWINS); godparents Nikolaj Željko? + Ana Pezdirec? (quarter smallholder); midwife Marija Jakofčič; signature **R. Ozlob? Polak, chaplain** — A NEW SIGNATURE (the 3rd priest of 1913; the block r82–r87 s254!); personal ID 2809913500032 — CONSISTENT (Sep 28, 1913; the 11th–12th digits 03 = male) — an ANCHOR; died Dec 3, 1978 in Slovenj Gradec — aged 83 (MKU MO SG 8.1978, p. 52, file no. 509; Jan 24, 1979)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "60",
    bookSignature: "04105",
    year: 1913,
    scan: 254,
    page: 216,
    whatSi: "krščen Nikolaj (⚰ 29.12.1944 — umrl med 2. svetovno vojno, 44 let) (1./2. 10.) — oče Nikolaj Kalan? [~ Kalko?] ¼ zemljak, mati Marija Brodarič; h60 = 9. VPIS (1893–1910); VRZEL 3 LETA; **KALAN na h60** (cf. h90 Kalan učiteljska familija — 2. hiša Kalana v vzorcu!); botra Martin Pezdirec + Marija Klepec?; babica Marija Meh (edina Meh 1913 — padec z 12/20!); podpis Jos. Rauq",
    whatEn: "baptized Nikolaj (died Dec 29, 1944 — during WWII, aged 44) (Oct 1/2) — father Nikolaj Kalan? [~ Kalko?] quarter smallholder, mother Marija Brodarič; h60 = the 9th ENTRY (1893–1910); a 3-YEAR GAP; **KALAN at h60** (cf. h90 the Kalan teacher family — the 2nd Kalan house in the sample!); godparents Martin Pezdirec + Marija Klepec?; midwife Marija Meh (the only Meh of 1913 — a fall from 12/20!); signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "47",
    bookSignature: "04105",
    year: 1913,
    scan: 255,
    page: 217,
    whatSi: "krščena Marija († 30.01.1998 Griblje — 84 let; MKU HO Črnomelj 1998, str. 39, zap. 319?; 16.02.1998) (5./6. 11.) — oče Janez Timec? [~ Tomec] ¼ zemljak, mati Barbara Vlokuše? [~]; **h47 MENJAVA DRUŽINE** (1911 Požek bajtar → 1913 Timec?); h47 = 4. VPIS (1887, 1890, 1911 → 1913); VRZEL 2 LETI; botra Nikolaj Mek? + Ana Timec? (botrinja = ISTI PRIIMEK kot oče — familija!); babica Marija Pleščič; podpis Jos. Rauq; marginalia »cer. poroč. 26.4.1947 v Novem mestu«; EMŠO 0411913500028 — MOŽEN POPRAVEK (11.–12. števka 02 = moški vs Marija ženska — morda 0411913505028) — SIDRO [~]; **glava »1914« INLINE str. 218 DNO** (s256, pod r105!) — P109 lead: 1914 r1 = [vas] 17 Terezija 1./1., EMŠO 01019141505225 (VPIS PRENEŠEN 16.10.2002); 1914 r5 = Griblje 1?/4? Anton (+9/2.1915) [~] — h47 r95 = ZADNJA Griblje vrstica 1913",
    whatEn: "baptized Marija (died Jan 30, 1998 in Griblje — aged 84; MKU HO Črnomelj 1998, p. 39, file no. 319?; Feb 16, 1998) (Nov 5/6) — father Janez Timec? [~ Tomec] quarter smallholder, mother Barbara Vlokuše? [~]; **h47 A FAMILY CHANGE** (the 1911 Požek cottager → 1913 Timec?); h47 = the 4th ENTRY (1887, 1890, 1911 → 1913); a 2-YEAR GAP; godparents Nikolaj Mek? + Ana Timec? (the godmother = the SAME SURNAME as the father — the family!); midwife Marija Pleščič; signature Jos. Rauq; a marginalia »church-married Apr 26, 1947 in Novo mesto«; personal ID 0411913500028 — A POSSIBLE CORRECTION (the 11th–12th digits 02 = male vs Marija female — maybe 0411913505028) — an ANCHOR [~]; **the 1914 heading INLINE at the bottom of p. 218** (s256, below r105!) — the P109 lead: 1914 r1 = [village] 17 Terezija Jan 1/1, personal ID 01019141505225 (the entry transferred Oct 16, 2002); 1914 r5 = Griblje 1?/4? Anton (died Feb 9, 1915) [~] — h47 r95 = the LAST Griblje row of 1913",
    status: "DOCUMENTED",
  },
  {
    houseNo: "1",
    bookSignature: "04105",
    year: 1914,
    scan: 257,
    page: 218,
    whatSi: "krščena Ana (⚰ 9.2.1915 — dojenček, 3 tedne) (18./19. 1.) — oče [raztrgano — neberljivo; kmet?], mati Marija Mice? [~]; h1 = 8. VPIS (1888–1910); VRZEL 4 LETA; **faza-1 POPRAVEK: otrok ANA (ne »Anton«!) + hiša 1 (ne »1?/4?« — 4.5× jasno »1.«)**; botra Jožef Štrucel + Marija Klešec (½ zemlj.; boter = h44 familija!); babica Marija Pleščič? [~]; podpis **Polak (kap.)** — NOVI podpis v Gribljih 1914 (cf. P108 r87); otrok †",
    whatEn: "baptized Ana (died Feb 9, 1915 — an infant, 3 weeks) (Jan 18/19) — father [torn — illegible; a farmer?], mother Marija Mice? [~]; h1 = the 8th ENTRY (1888–1910); a 4-YEAR GAP; **the phase-1 CORRECTION: the child ANA (not »Anton«!) + house 1 (not »1?/4?« — 4.5× clearly »1.«)**; godparents Jožef Štrucel + Marija Klešec (half smallholder; the godfather = the h44 family!); midwife Marija Pleščič? [~]; signature **Polak (chaplain)** — a NEW signature among the Griblje rows of 1914 (cf. P108 r87); the infant died",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1914,
    scan: 259,
    page: 219,
    whatSi: "krščen Alojzij (20./21. 2.) — oče [raztrgano — »…inec« → verj. BRINEC, kmet], mati Doroteja Perdivec? [~]; h14 = 6. VPIS (1896–1911); **VRZEL 3 LETA (faza-1 »vrzel 18« POPRAVLJENO — h14 = 1896/1900/1902/1908/1911!)**; botra Peter Brinec + Ana Brinec (¼ zemlj.); babica Barbara Adlešič; podpis Jos. Rauq; mati PERDIVEC + botri BRINEC ×2 (sosedski blok)",
    whatEn: "baptized Alojzij (Feb 20/21) — father [torn — »…inec« → prob. BRINEC, a farmer], mother Doroteja Perdivec? [~]; h14 = the 6th ENTRY (1896–1911); **a 3-YEAR GAP (the phase-1 »gap 18« CORRECTED — h14 = 1896/1900/1902/1908/1911!)**; godparents Peter Brinec + Ana Brinec (quarter smallholder); midwife Barbara Adlešič; signature Jos. Rauq; the mother PERDIVEC + the godparents BRINEC ×2 (the neighbouring block)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1914,
    scan: 259,
    page: 219,
    whatSi: "krščena Marija (⚰ 26.3.1925 — umrla pri 11 letih) (3.? 3.) — oče [raztrgano — »…amšatro?« kmet?], mati Marjeta Perdivec? [~]; h53 = 5. VPIS (1891–1898); **VRZEL 16 LET — najdaljša 1914!** (rekord vzorca ostaja h8 23 let 1912); botra Jurij Perdivec + Marjeta Kranjc? [~]; babica Marija Jakofčič; podpis [nalepka r18 prekriva — verj. Jos. Rauq]; **PERDIVEC mati ×2 1914** (r13 Doroteja + r17 Marjeta — sestrski poroki v h14 + h53?); nalepka »umrla 16.05.2000 Nm« = r18 Ana (Primostek 10), NE r17 — faza-1 pripis POPRAVLJEN",
    whatEn: "baptized Marija (died Mar 26, 1925 — aged 11) (Mar 3.?) — father [torn — »…amšatro?« a farmer?], mother Marjeta Perdivec? [~]; h53 = the 5th ENTRY (1891–1898); **a 16-YEAR GAP — the longest of 1914!** (the sample record remains h8's 23 years of 1912); godparents Jurij Perdivec + Marjeta Kranjc? [~]; midwife Marija Jakofčič; signature [the r18 label covers it — prob. Jos. Rauq]; **the PERDIVEC mother ×2 in 1914** (r13 Doroteja + r17 Marjeta — sister marriages into h14 + h53?); the label »died May 16, 2000 Nm« = r18 Ana (Primostek 10), NOT r17 — the phase-1 attribution CORRECTED",
    status: "DOCUMENTED",
  },
  {
    houseNo: "11",
    bookSignature: "04105",
    year: 1914,
    scan: 261,
    page: 220,
    whatSi: "krščena Jožefa (⚰ 3.9.1914 — dojenček, 6 mesecev) (18./18. 3.) — oče [pod zavihkom strani], mati Marija Jakobčič; h11 = 7. VPIS (1886–1912); VRZEL 2 LETI; **faza-1 POPRAVEK: hiša 11 — VIDNA na OBEH dupih s260+s261 4.5× (faza-1 »pod zavihkom« ZAVRŽENO!)**; EMŠO 1803914505878 — SKLADNO (18.3.1914; 8.11.1982 Šimonič Nina) — SIDRO; botra Janez Adlešič + Ana Adlešič (½ zemlj.); babica Marija Jakobčič [~ — ISTO ime kot mati!]; podpis »Pf. Koziga?« [~]; otrok †",
    whatEn: "baptized Jožefa (died Sep 3, 1914 — an infant, 6 months) (Mar 18/18) — father [under the page corner], mother Marija Jakobčič; h11 = the 7th ENTRY (1886–1912); a 2-YEAR GAP; **the phase-1 CORRECTION: house 11 — VISIBLE on BOTH duplicates s260+s261 at 4.5× (the phase-1 »under the page corner« REJECTED!)**; personal ID 1803914505878 — CONSISTENT (Mar 18, 1914; Nov 8, 1982 Šimonič Nina) — an ANCHOR; godparents Janez Adlešič + Ana Adlešič (half smallholder); midwife Marija Jakobčič [~ — the SAME name as the mother!]; signature »Pf. Koziga?« [~]; the infant died",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1914,
    scan: 261,
    page: 220,
    whatSi: "krščena Barbara (por. 20.5.1933 [~]; ⚰ 11.04.2001 v Gribljah — 86 let; MKU MO Črnomelj 1.2001, zap.št.20; 11.05.2001) (1. 5., rojstva pod nalepko) — starši pod nalepkami [neberljivo]; h44 = 7. VPIS (1888–1913) — **ZAPORED 2. LETO** (1913 r35 + 1914 r28!); **ŠTRUCELJ kontinuiteta** (cf. P107/P108 h44 Štrucelj + botri Štrucel ×4 v 1914!); **hiša 44 POTRJENA 4.5× (»44«; faza-1 band-dvom »34« ZAVRŽEN)**; EMŠO 0405914500184 [~ — 04.05.1914; dvom 3004914500184 = 30.04. — SKLADNO s krsto 1.5.]; babica Barbara Adlešič? [~]; podpis [ghost — verj. Jos. Rauq]",
    whatEn: "baptized Barbara (married May 20, 1933 [~]; died Apr 11, 2001 in Griblje — aged 86; MKU MO Črnomelj 1.2001, file no. 20; May 11, 2001) (May 1, the birth date under the label) — the parents under the labels [illegible]; h44 = the 7th ENTRY (1888–1913) — **CONSECUTIVE the 2nd YEAR** (1913 r35 + 1914 r28!); **the ŠTRUCELJ continuity** (cf. P107/P108 h44 Štrucelj + the godparents Štrucel ×4 in 1914!); **house 44 CONFIRMED at 4.5× (»44«; the phase-1 band-doubt »34« REJECTED)**; personal ID 0405914500184 [~ — May 4, 1914; the doubt 3004914500184 = Apr 30 — CONSISTENT with the baptism May 1]; midwife Barbara Adlešič? [~]; signature [a ghost — prob. Jos. Rauq]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1914,
    scan: 261,
    page: 220,
    whatSi: "krščen Janez (4. 5., krsta pod nalepko; poročen 22.5.1939 [~]; žena Jožefa Štrucel? umrla 26.10.1982 Novo mesto — m.l.1982 št.292, kop.461) — **oče-kolona: Marija Štrucel (¼ zemljak) — ŽENSKO IME V OČETOVI KOLONI (1./3 primerov 1914 — nezakonski vzorec!)**, mati Marija Meh; h5 = 7. VPIS (1891–1912); VRZEL 2 LETI; **NOVA VRSTICA VZORCA — faza-1 je r29 IZPUSTILA (nalepka blok)!**; EMŠO 0405914505481 — SKLADNO (4.5.1914; 8.11.1982) — SIDRO; botra Janez Dragoš + Neža Jakobčič; babica Marija Jakofčič; podpis Jos. Rauq",
    whatEn: "baptized Janez (May 4, the baptism under the label; married May 22, 1939 [~]; the wife Jožefa Štrucel? died Oct 26, 1982 in Novo mesto — m.l.1982 no.292, grave 461) — **the father column: Marija Štrucel (quarter smallholder) — A WOMAN'S NAME IN THE FATHER COLUMN (the 1st of 3 cases of 1914 — the out-of-wedlock pattern!)**, mother Marija Meh; h5 = the 7th ENTRY (1891–1912); a 2-YEAR GAP; **A NEW ROW OF THE SAMPLE — the phase-1 OMITTED r29 (the label block)!**; personal ID 0405914505481 — CONSISTENT (May 4, 1914; Nov 8, 1982) — an ANCHOR; godparents Janez Dragoš + Neža Jakobčič; midwife Marija Jakofčič; signature Jos. Rauq",
    status: "DOCUMENTED",
  },
  {
    houseNo: "77",
    bookSignature: "04105",
    year: 1914,
    scan: 262,
    page: 221,
    whatSi: "krščen Anfons/Alfons? [~] (⚰ 1.9.1950 v Šempolju? št.63 [~]; matičar Janez Ravnik? [~]) (15./16. 6.) — oče Janez Božič? [~] — **ŠAHTAR (rudar! — edinstven poklic v Gribljih vzorca)**, mati Katarina Veselič [~]; h77 = 4. VPIS (1890–1909); VRZEL 5 LET; **faza-1 POPRAVEK: otrok Anfons/Alfons (ne »Anton«) + babica Marija Pleščič (ne Adlešič — R_r38 3× jasno!)**; botra Miklavž Mledeš? + Marija Šimec? [~]; babica Marija Pleščič; podpis Jos. Rauq; rudarski poklic = selitveni signal (cf. r58 vojni invalid Podrečje)",
    whatEn: "baptized Anfons/Alfons? [~] (died Sep 1, 1950 in Šempolje? no.63 [~]; the registrar Janez Ravnik? [~]) (Jun 15/16) — father Janez Božič? [~] — **A MINER (ŠAHTAR! — a unique trade among the Griblje of the sample)**, mother Katarina Veselič [~]; h77 = the 4th ENTRY (1890–1909); a 5-YEAR GAP; **the phase-1 CORRECTION: the child Anfons/Alfons (not »Anton«) + the midwife Marija Pleščič (not Adlešič — R_r38 3× clear!)**; godparents Miklavž Mledeš? + Marija Šimec? [~]; midwife Marija Pleščič; signature Jos. Rauq; the mining trade = a migration signal (cf. r58 the war invalid of Podrečje)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1914,
    scan: 262,
    page: 221,
    whatSi: "krščena Danica (poročena 20.?11.1946/47 v Gradcu [~ — ženin Ferdinand? Jurij?]; ⚰ 20.08.1991 Novo mesto — 76 let; MKU MO Nm; Metlika 25.11.1991) (30. 6./1. 7.) — oče Janez Papič? [~] (¼ zemlj.), mati Katarina Krixan/Kranjc? [~]; h21 = 9. VPIS (1887–1911; največ med 1914 hišami!); VRZEL 3 LETA; **faza-1 POPRAVEK: starši = Papič × Krixan (ne »Anton Lavca + Ana Tome« — to sta BOTRA!)**; botra **Anton Lozar + Barbara Lozar**; babica Marija Karevič? [~ trak]; podpis [trak — verj. Jos. Rauq]; EMŠO 3006914500518 — SKLADNO (30.6.1914; 8.11.1982) — SIDRO",
    whatEn: "baptized Danica (married Nov 20?, 1946/47 in Graz [~ — the groom Ferdinand? Jurij?]; died Aug 20, 1991 in Novo mesto — aged 76; MKU MO Nm; Metlika Nov 25, 1991) (Jun 30/Jul 1) — father Janez Papič? [~] (quarter smallholder), mother Katarina Krixan/Kranjc? [~]; h21 = the 9th ENTRY (1887–1911; the most among the 1914 houses!); a 3-YEAR GAP; **the phase-1 CORRECTION: the parents = Papič × Krixan (not »Anton Lavca + Ana Tome« — those are the GODPARENTS!)**; godparents **Anton Lozar + Barbara Lozar**; midwife Marija Karevič? [~ strip]; signature [strip — prob. Jos. Rauq]; personal ID 3006914500518 — CONSISTENT (Jun 30, 1914; Nov 8, 1982) — an ANCHOR",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1914,
    scan: 264,
    page: 222,
    whatSi: "krščena Ivanka (⚰ 7.7.1915? [~] — dojenček, ~1 leto) (4./9. 7.) — oče **Ernest Šušteršič — ljudski učitelj** [~], mati Marjeta Pečej? [~]; h90 = 8. VPIS (1890–1912); VRZEL 2 LETI; botra Jožef Štrucel + Barbara Štrucel (h44 familija — Štrucel mreža!); babica Marija Jakofčič; podpis Jos. Rauq; oče UČITELJ — h90 kmečka hiša z učiteljskim očetom 1914; otrok †",
    whatEn: "baptized Ivanka (died Jul 7, 1915? [~] — an infant, ~1 year old) (Jul 4/9) — father **Ernest Šušteršič — a people's teacher** [~], mother Marjeta Pečej? [~]; h90 = the 8th ENTRY (1890–1912); a 2-YEAR GAP; godparents Jožef Štrucel + Barbara Štrucel (the h44 family — the Štrucel network!); midwife Marija Jakofčič; signature Jos. Rauq; the father A TEACHER — h90 a farm house with a teacher father in 1914; the infant died",
    status: "DOCUMENTED",
  },
  {
    houseNo: "18",
    bookSignature: "04105",
    year: 1914,
    scan: 264,
    page: 222,
    whatSi: "krščena Barbara (por. 30.10.1938? [~]) (26. 8.; EMŠO 2108914500174 — SKLADNO 21.8.1914, 8.11.1982 — SIDRO) — oče Miklavž Zagina? [~] (¼ zemljak), mati **Katarina Brinec**; h18 = 6. VPIS (1898–1912); VRZEL 2 LETI; botra Matija Milec + Marjeta Križan? [~] (boter = h65 MILEK familija — vrnjen mreži!); babica Ana Mavrenič; podpis **Pavlin Bitnar**",
    whatEn: "baptized Barbara (married Oct 30, 1938? [~]) (Aug 26; personal ID 2108914500174 — CONSISTENT Aug 21, 1914, Nov 8, 1982 — an ANCHOR) — father Miklavž Zagina? [~] (quarter smallholder), mother **Katarina Brinec**; h18 = the 6th ENTRY (1898–1912); a 2-YEAR GAP; godparents Matija Milec + Marjeta Križan? [~] (the godfather = the h65 MILEK family — returned to the network!); midwife Ana Mavrenič; signature **Pavlin Bitnar**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1914,
    scan: 264,
    page: 222,
    whatSi: "krščena [ime pod trakom] (1.?/4.? 9.; EMŠO 0409914505296 [~]; ⚰ 26.06.1976 Novo mesto? [~]; poročena [~]) — oče Miklavž Jaklič? [~ skozi trak], mati Ana Špižac? [~]; h48 = 7. VPIS (1898–1912); VRZEL 2 LETI; **DVOM FAZE 1 REŠEN: vas = GRIBLJE (začetnica »G« jasna skozi prozoren trak 5×!), hiša 48** → **12. VPIS VZORCA**; **PT: h48 (s h44 + h53) v luknji 41–60 — dokazane številke!**; botra Janez Vidjan? + Ana Mlakar? [~]; babica Ana Mavrenič? [~]; podpis [trak — verj. Pavlin Bitnar]",
    whatEn: "baptized [the name under the strip] (Sep 1.?/4.?; personal ID 0409914505296 [~]; died Jun 26, 1976 in Novo mesto? [~]; married [~]) — father Miklavž Jaklič? [~ through the strip], mother Ana Špižac? [~]; h48 = the 7th ENTRY (1898–1912); a 2-YEAR GAP; **THE PHASE-1 DOUBT RESOLVED: the village = GRIBLJE (the initial »G« clear through the transparent strip at 5×!), house 48** → **the 12th ENTRY OF THE SAMPLE**; **the PT: h48 (with h44 + h53) in the 41–60 gap — proven numbers!**; godparents Janez Vidjan? + Ana Mlakar? [~]; midwife Ana Mavrenič? [~]; signature [strip — prob. Pavlin Bitnar]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "8",
    bookSignature: "04105",
    year: 1914,
    scan: 266,
    page: 223,
    whatSi: "krščena Jožefa (⚰ 31.7.1915 — dojenček, ~10 mesecev) (11./12. 9.) — oče Janez Jakobčič (½ zemljak), mati Neža Jakljevič; h8 = 6. VPIS (1886–1913) — **ZAPORED 2. LETO** (1913 + 1914 — po vrzeli 23 let 1889→1912!); ISTA ZVEZA Jakobčič × Jakljevič kot 1912/1913 — 3. skupaj SKLADNO; botra **Matija Štrucel + Katarina Potter** (¼; faza-1 »Hrovat« POPRAVLJENO!); babica Marija Jakofčič; podpis **Pavlin Bitnar**; otrok †; EMŠO 2210914505196 = **r63 Zemelj 20 (22./22. OKTOBER), NE r62 — faza-1 pripis POPRAVLJEN** (2210 = 22.10.1914 SKLADNO z r63!); **glava 1915 na VRHU str. 225 = s269 (NI INLINE na dnu str. 224 — ročno dopisan »1915.«!)** — P110 lead: 1915 r1 = Škrilje? 1 Janez 1./2. Januar; 1915 r8 = **GRIBLJE 88 Ivana** 20./22.? (P110 lead!); opomba na dnu str. 224: **»78 konec porodov l. 1914«** — h8 r62 = ZADNJA Griblje vrstica 1914",
    whatEn: "baptized Jožefa (died Jul 31, 1915 — an infant, ~10 months) (Sep 11/12) — father Janez Jakobčič (half smallholder), mother Neža Jakljevič; h8 = the 6th ENTRY (1886–1913) — **CONSECUTIVE the 2nd YEAR** (1913 + 1914 — after the 23-year gap 1889→1912!); the SAME COUPLE Jakobčič × Jakljevič as 1912/1913 — the 3rd together CONSISTENT; godparents **Matija Štrucel + Katarina Potter** (quarter; the phase-1 »Hrovat« CORRECTED!); midwife Marija Jakofčič; signature **Pavlin Bitnar**; the infant died; the personal ID 2210914505196 = **r63 Zemelj 20 (Oct 22/22), NOT r62 — the phase-1 attribution CORRECTED** (2210 = Oct 22, 1914 CONSISTENT with r63!); **the 1915 heading at the TOP of p. 225 = s269 (NOT INLINE at the bottom of p. 224 — manually added »1915.«!)** — the P110 lead: 1915 r1 = Škrilje? 1 Janez Jan 1/2; 1915 r8 = **GRIBLJE 88 Ivana** Jan 20/22.? (the P110 lead!); the note at the bottom of p. 224: **»78 konec porodov l. 1914«** — h8 r62 = the LAST Griblje row of 1914",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1915,
    scan: 269,
    page: 225,
    whatSi: "krščena Ivana († 20.2.1915 [~ — dojenček, ~1 mesec!]; marg. »+ 20/[II] 1915« — d1 4×) (20./22. 1.) — oče **Peter Brinec**, bajtar, roj. 28/9 1860 (por. 25.9.1892 | 12.96 [~]), mati **Ana roj. Butala** (22/12 1874; faza-1 »Buntala« POPRAVLJENO); h88 = 4. VPIS (1886, 1904, 1910 → 1915) — VRZEL 5 LET; **P109 lead POTRJEN (GRIBLJE 88 Ivana!)**; botra **Janez Brinec in žena njegova Doroteja Brinec** (½ zemlj.); babica Marija Jakofčič; podpis V. Valerijan Učak (svinčnik); glava 1915 ročno na VRHU str. 225 = s269",
    whatEn: "baptized Ivana (died Feb 20, 1915 [~ — an infant, ~1 month]; the marginal note »+ 20/[II] 1915« — d1 4×) (Jan 20/22) — father **Peter Brinec**, cottager, born Sep 28, 1860 (m. Sep 25, 1892 | Dec 1896 [~]), mother **Ana née Butala** (Dec 22, 1874; the phase-1 »Buntala« CORRECTED); h88 = the 4th ENTRY (1886, 1904, 1910 → 1915) — a 5-YEAR GAP; **the P109 lead CONFIRMED (GRIBLJE 88 Ivana!)**; godparents **Janez Brinec and his wife Doroteja Brinec** (half smallholder); midwife Marija Jakofčič; signature V. Valerijan Učak (pencil); the 1915 heading manually at the TOP of p. 225 = s269",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1915,
    scan: 270,
    page: 226,
    whatSi: "krščena Zora Jožefa († 25.7.1915 — dobenček, ~3,5 mesece; marg. »+ 25/7 15«) (6./7. 3.) — oče **Franc Rajhmer** [~], čuv.[aj]? [~], roj. 13/12 1882 [~], (por. 18.4.1908), mati **Ivana roj. Tadej** (13/8 86 [~]); h45 = 6. VPIS (1896–1912) — VRZEL 3 LETA; botra **Jurij Berdir? [~]** (½ zemlj.) + **Terezija Jakofčič**, ros. žena; babica Marija Jakofčič; podpis Učak [~]",
    whatEn: "baptized Zora Jožefa (died Jul 25, 1915 — an infant, ~3.5 months; the marginal note »+ 25/7 15«) (Mar 6/7) — father **Franc Rajhmer** [~], caretaker? [~], born Dec 13, 1882 [~], (m. Apr 18, 1908), mother **Ivana née Tadej** (Aug 13, 1886 [~]); h45 = the 6th ENTRY (1896–1912) — a 3-YEAR GAP; godparents **Jurij Berdir? [~]** (half smallholder) + **Terezija Jakofčič**, the ros. wife; midwife Marija Jakofčič; signature Učak [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "70",
    bookSignature: "04105",
    year: 1915,
    scan: 270,
    page: 226,
    whatSi: "krščena Barbara (16./17. 3.; EMŠO ž. **1603915505171** — 5× jasno, faza-1 »5505141« POPRAVLJENO) — oče **Matija Brinec**, ½ zemlj., roj. 15/7 1883 [~ — 4×; faza-1 »1888« POPRAVLJENO], mati **Marija (1877), roj. PEZDIREC**, r. 30/1? [~ — faza-1 »Perdivec« POPRAVLJENO (3.2×) — PEZDIREC mreža!]; h70 = 3. VPIS (1893, 1912 → 1915) — VRZEL 3 LETA; botra **Miko Šegina? [~]** (½ zemlj.) + **Ana Brinec**, ros. žena; babica **Barbara Adlešič**; podpis Kapl. Bitnar; marg.: mož umrl 4.1.1994 [~ — faza-1 »oče« ZAVRŽENO: nemogoče za očeta r. 1883] + umrla 23.6.2004 (MKU MO Novo mesto 1.2004, str. 220, zap. št. 312) + poročena 13.2.1939",
    whatEn: "baptized Barbara (Mar 16/17; the personal ID **1603915505171** — 5× clear, the phase-1 »5505141« CORRECTED) — father **Matija Brinec**, half smallholder, born Jul 15, 1883 [~ — 4×; the phase-1 »1888« CORRECTED], mother **Marija (1877), née PEZDIREC**, b. Jan 30? [~ — the phase-1 »Perdivec« CORRECTED (3.2×) — the PEZDIREC network!]; h70 = the 3rd ENTRY (1893, 1912 → 1915) — a 3-YEAR GAP; godparents **Miko Šegina? [~]** (half smallholder) + **Ana Brinec**, the ros. wife; midwife **Barbara Adlešič**; signature Kapl. Bitnar; the marginal notes: the husband died Jan 4, 1994 [~ — the phase-1 »father« REJECTED: impossible for a father born 1883] + she died Jun 23, 2004 (MKU MO Novo mesto 1.2004, p. 220, no. 312) + married Feb 13, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "78",
    bookSignature: "04105",
    year: 1915,
    scan: 272,
    page: 227,
    whatSi: "krščena Jožefa (‡ 10.9.1917 — d27 3.5× jasno; **P109 lead »1916« ZAVRŽENO!**) (22./23. 3.) — oče **Anton Ložar** [~ Ložar/Lozar], ½ zemlj., roj. 5/5 890 (por. 16.1.1912), mati **Barbara roj. Križan** (r. 20/6 1889); h78 = 3. VPIS (1887, 1888 → 1915); **VRZEL 27 LET = NOV REKORD vzorca!** (prej h53 16 let); botra **Janez Kambič** (½ zemlj.) + **Katar. Šapič**, ros. žena (faza-1 »Hatar.« = Katar.!); babica Marija Jakofčič; podpis Učak d.i. (svinčnik)",
    whatEn: "baptized Jožefa (died Sep 10, 1917 — d27 3.5× clear; **the P109 lead »1916« REJECTED!**) (Mar 22/23) — father **Anton Ložar** [~ Ložar/Lozar], half smallholder, born May 5, 1890 (m. Jan 16, 1912), mother **Barbara née Križan** (b. Jun 20, 1889); h78 = the 3rd ENTRY (1887, 1888 → 1915); **a 27-YEAR GAP = the NEW RECORD of the sample!** (previously h53 16 years); godparents **Janez Kambič** (half smallholder) + **Katar. Šapič**, the ros. wife (the phase-1 »Hatar.« = Katar.!); midwife Marija Jakofčič; signature Učak d.i. (pencil)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1915,
    scan: 277,
    page: 231,
    whatSi: "krščena Ana (18./19. 7.) — oče **Matija JAKOBČIČ** [~ — faza-1 »Jaklič/Jakličič« POPRAVLJENO (4× d29)], ½ zemljak, roj. 17.8. 1856 (star 59 ob krsti! [~]), mati **Marija roj. Jakofčič** (24.2.1877; por. 28.1.1910); h13 = 8. VPIS (1885–1913) — VRZEL 2 LETI; botra **Matija Perdivec** (½ zemlj.) + **Katarina Jakofčič**, ½ zemljaka žena; babica Marija Jakofčič; podpis V. Valerijan Učak",
    whatEn: "baptized Ana (Jul 18/19) — father **Matija JAKOBČIČ** [~ — the phase-1 »Jaklič/Jakličič« CORRECTED (4× d29)], half smallholder, born Aug 17, 1856 (aged 59 at the baptism! [~]), mother **Marija née Jakofčič** (Feb 24, 1877; m. Jan 28, 1910); h13 = the 8th ENTRY (1885–1913) — a 2-YEAR GAP; godparents **Matija Perdivec** (half smallholder) + **Katarina Jakofčič**, the half-smallholder's wife; midwife Marija Jakofčič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1915,
    scan: 280,
    page: 234,
    whatSi: "krščena Marija Ana († 23.6.1943 — 2. svetovna doba; marg. »+ 23. 6. 1943«) (26./28. 10.; trak čez vrstico, vendar berljivo 3×) — oče **Nikolaj Pezdirec**, posestnik ½ z., roj. 28.11. 1874 (por. 16.11. 1907), mati **Rosa roj. Tuvan** (r. 29.1. 1880); h40 = 6. VPIS (1897–1912) — VRZEL 3 LETA; botra **Matija Urh**, posest. + **Ana Pezdirec**, posest žena; babica Marija Jakofčič, n.zp.; podpis V. Valerijan Učak d.i.",
    whatEn: "baptized Marija Ana (died Jun 23, 1943 — the WWII era; the marginal note »+ 23. 6. 1943«) (Oct 26/28; a strip across the row, yet legible 3×) — father **Nikolaj Pezdirec**, landowner half, born Nov 28, 1874 (m. Nov 16, 1907), mother **Rosa née Tuvan** (b. Jan 29, 1880); h40 = the 6th ENTRY (1897–1912) — a 3-YEAR GAP; godparents **Matija Urh**, landowner + **Ana Pezdirec**, the landowner's wife; midwife Marija Jakofčič, n.zp.; signature V. Valerijan Učak d.i.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1915,
    scan: 280,
    page: 234,
    whatSi: "krščena Marija (2./3. 11.; EMŠO ž. **0211915505717** — 4× jasno) — oče **Matija Štravs**, posest ½ z., roj. 1.I. 1862 (por. 8.II. 1904), mati **Marjeta roj. Šimec** (r. 22.2. 1875); h32 = 11. VPIS (1889–1909 — največ med hišami 1915!) — VRZEL 6 LET; botra **Mihael Jakofčič**, posestnik? + **Barbara Štrucelj**, pos. žena (**ŠTRUCELJ mreža!**); babica Marija Jakofčič, nj.; podpis V. Valerijan Učak d.i.; marg.: umrla 31.1.1989 Novo mesto (MKU 1.1989, str. 112, zap. št. 66) + poročena 19.2.1939",
    whatEn: "baptized Marija (Nov 2/3; the personal ID **0211915505717** — 4× clear) — father **Matija Štravs**, landowner half, born Jan 1, 1862 (m. Feb 8, 1904), mother **Marjeta née Šimec** (b. Feb 22, 1875); h32 = the 11th ENTRY (1889–1909 — the most among the 1915 houses!) — a 6-YEAR GAP; godparents **Mihael Jakofčič**, landowner? + **Barbara Štrucelj**, the pos. wife (**the ŠTRUCELJ network!**); midwife Marija Jakofčič, nj.; signature V. Valerijan Učak d.i.; the marginal notes: she died Jan 31, 1989 Novo mesto (MKU 1.1989, p. 112, no. 66) + married Feb 19, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1915,
    scan: 281,
    page: 235,
    whatSi: "krščen Martin (8./8. 11.) — oče **Anton Brodarič**, posest. ½ zem., roj. 14/11-1859 (por. 7/11-1904), mati **Katarina roj. Milek** (1./8.-1876; **MILEK — cf. P108 h34/h65!**); h46 = 10. VPIS (1893–1913) — VRZEL 2 LETI; botra **Nikolaj Želejko? [~]**, posr. **župan** (2. župan-botra vzorca — cf. r40 Jakob Stipanič!) + **Ana Pezdirec**, posed žena; babica Marija Jakofčič, n.zp.; podpis Kapl. Bitnar; VELIKA modra marg.: poroki 19.1.1952 + 19.3.1961 (Karlovci) + **zakonska zveza RAZVELJAVLJENA s sodbo št. K 757/65-10 (2.12.1965, Karlovci — prvi razveljavljen zakon vzorca!)** + umrl 15.5.1992 Karlovci [~]",
    whatEn: "baptized Martin (Nov 8/8) — father **Anton Brodarič**, landowner half, born Nov 14, 1859 (m. Nov 7, 1904), mother **Katarina née Milek** (Aug 1, 1876; **MILEK — cf. P108 h34/h65!**); h46 = the 10th ENTRY (1893–1913) — a 2-YEAR GAP; godparents **Nikolaj Želejko? [~]**, posr. **mayor** (the 2nd mayor-godparent of the sample — cf. r40 Jakob Stipanič!) + **Ana Pezdirec**, the posed wife; midwife Marija Jakofčič, n.zp.; signature Kapl. Bitnar; a LARGE blue marginal note: marriages Jan 19, 1952 + Mar 19, 1961 (Karlovac) + **the marriage ANNULLED by the court no. K 757/65-10 (Dec 2, 1965, Karlovac — the first annulled marriage of the sample!)** + he died May 15, 1992 Karlovac [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04105",
    year: 1915,
    scan: 281,
    page: 235,
    whatSi: "krščena Neža († 23.12.1916 — dojenček; marg. »+ 23/12 1916«) (15./16. 11.) — oče **Oswald JAKOBČIČ** [~ — faza-1 »Jakobeč« POPRAVLJENO; cf. h13 Matija Jakobčič — familija Jakobčič v Gribljih!], posest ½ z., roj. 3. aug 1889 (star 26; por. 6.2.1911), mati **Terezija roj. Klepec** (r. 21.6. 1890; faza-1 »20.6« POPRAVLJENO); h9 = 4. VPIS (1896, 1900, 1913 → 1915) — VRZEL 2 LETI; botra **Jurij Klepec**, posest. + **Marija Žunič**, posest žena; babica **Marija Jakobčič**, neizp. (verj. očetova mati); podpis V. Valerijan Učak d.i.; ime OSWALD = nemško-modno (cf. r21 Vilhelm + r49 Emil Filip Leopold)",
    whatEn: "baptized Neža (died Dec 23, 1916 — an infant; the marginal note »+ 23/12 1916«) (Nov 15/16) — father **Oswald JAKOBČIČ** [~ — the phase-1 »Jakobeč« CORRECTED; cf. h13 Matija Jakobčič — the Jakobčič family in Griblje!], landowner half, born Aug 3, 1889 (aged 26; m. Feb 6, 1911), mother **Terezija née Klepec** (b. Jun 21, 1890; the phase-1 »Jun 20« CORRECTED); h9 = the 4th ENTRY (1896, 1900, 1913 → 1915) — a 2-YEAR GAP; godparents **Jurij Klepec**, landowner + **Marija Žunič**, the landowner's wife; midwife **Marija Jakobčič**, neizp. (probably the father's mother); signature V. Valerijan Učak d.i.; the name OSWALD = German-fashion (cf. r21 Vilhelm + r49 Emil Filip Leopold)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1915,
    scan: 282,
    page: 236,
    whatSi: "krščen Nikolaj (25./26. 11.; EMŠO ž. **2511915500090** — 4× jasno) — oče **Nikolaj Milek**, posest ½ z., roj. 13.11. 1869 (por. 12.2. 1900; **MILEK ×2 v 1915 — cf. h46 mati Milek!**), mati **Ana roj. Črnič** (2.8. 1875); h22 = 7. VPIS (1899–1912) — VRZEL 3 LETA; botra **Nikolaj Požek**, p. ½ z. + **Ana Črnič**, posest žena; babica Marija Jakofčič, neizž.; podpis Valerijan Učak d.i.; marg.: sklenil zakonsko zvezo 15.8.1945 Črnomelj (RNK 1.1945 zap. št. 84) + umrl 24.4.1992 Črnomelj [faza-1 »1932« POPRAVLJENO: nemogoče po poroki 1945]",
    whatEn: "baptized Nikolaj (Nov 25/26; the personal ID **2511915500090** — 4× clear) — father **Nikolaj Milek**, landowner half, born Nov 13, 1869 (m. Feb 12, 1900; **MILEK ×2 in 1915 — cf. h46 the mother Milek!**), mother **Ana née Črnič** (Aug 2, 1875); h22 = the 7th ENTRY (1899–1912) — a 3-YEAR GAP; godparents **Nikolaj Požek**, p. ½ z. + **Ana Črnič**, the landowner's wife; midwife Marija Jakofčič, neizž.; signature Valerijan Učak d.i.; the marginal notes: he married Aug 15, 1945 Črnomelj (RNK 1.1945 no. 84) + he died Apr 24, 1992 Črnomelj [the phase-1 »1932« CORRECTED: impossible after the 1945 marriage]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1915,
    scan: 282,
    page: 236,
    whatSi: "krščen Janez (18./18. 12.; EMŠO ž. **1812915500054** — 4× jasno) — oče **Jure Dragos**, posest ½ z., roj. 23.4.1888 (por. 21/4-1913; **DRAGOS — cf. P107 r47 + P109 r78 mrtvorojen Dragos × Bahorič!**), mati **Marjeta Pezdirc** (14.8.1891); h53 = 6. VPIS (1891–1914); **ZAPORED 2. LETO** (1914 r17!); botra **Matija Štravs**, posest. + **Katarina Pezdirc**, posest žena; babica Marija Jakofčič, neizpr.; podpis Kapl. Bitnar; marg.: poročen 5.3.1947 s Petjak Marijo? [~] + umrl 2.10.1958 (MKU NO Novo mesto 1.1958, str. 251, zap. št. 2345?) + umrla 5.12.1955 + **odločba (Ljubljana) 16.3.1948 postala pravnomočna 16.3.1948 — Gradac 4.6.1948 matičar, nam. [~ — vsebina dvom: posvojitev/rodovna pravica?]**",
    whatEn: "baptized Janez (Dec 18/18; the personal ID **1812915500054** — 4× clear) — father **Jure Dragos**, landowner half, born Apr 23, 1888 (m. Apr 21, 1913; **DRAGOS — cf. P107 r47 + P109 r78 the stillborn Dragos × Bahorič!**), mother **Marjeta Pezdirc** (Aug 14, 1891); h53 = the 6th ENTRY (1891–1914); **CONSECUTIVE the 2nd YEAR** (1914 r17!); godparents **Matija Štravs**, landowner + **Katarina Pezdirc**, the landowner's wife; midwife Marija Jakofčič, neizpr.; signature Kapl. Bitnar; the marginal notes: married Mar 5, 1947 to Petjak Marija? [~] + died Oct 2, 1958 (MKU NO Novo mesto 1.1958, p. 251, no. 2345?) + she died Dec 5, 1955 + **the decision (Ljubljana) of Mar 16, 1948 became final on Mar 16, 1948 — Gradac Jun 4, 1948 the deputy registrar [~ — the content unclear: adoption/ancestral right?]**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1916,
    scan: 285,
    page: 239,
    whatSi: "krščena Barbara († 26.8.1917 — dojenček ~17 mesecev; marg. »† 26.8.1917«) (27./28. 2.) — oče **Nikolaj Silak? [~ Bilak?]**, posest ½ ž., roj. 8.12.1877, mati **Katarina roj. Klobučar** (23.4.1877); h34 = 10. VPIS (1887–1913) — VRZEL 3 LETA; **1. GRIBLJE vrstica 1916!**; mesec glava »february«; botra **Matija Muh** (½ ž. posestnik) + **Katarina Hrižan** (posest žena); babica Bara Adlešič; podpis V. Valerijan Učak",
    whatEn: "baptized Barbara (died Aug 26, 1917 — an infant ~17 months; marg. »† 26.8.1917«) (Feb 27/28) — father **Nikolaj Silak? [~ Bilak?]**, half smallholder, born Dec 8, 1877, mother **Katarina née Klobučar** (Apr 23, 1877); h34 = the 10th ENTRY (1887–1913) — a 3-YEAR GAP; **the 1st GRIBLJE row of 1916!**; the month heading »february«; godparents **Matija Muh** + **Katarina Hrižan**; midwife Bara Adlešič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1916,
    scan: 286,
    page: 240,
    whatSi: "krščen Vincencij († ~3 leta; marg. »+ 8/9 1919« — vojna!) (28./29. 4.) — oče **Ivan Dragos? [~]**, posestnik ½ ž., roj. 5.7.1867, mati **Barbara roj. Grintkenič? [~]** (11.12.1871); h12 = 14. VPIS (1892–1912) — VRZEL 4 LETA; **2. GRIBLJE vrstica 1916!**; botra **Štefk Matija? [~]** + **Marija TOTER** (posest samska hči — mreža cf. P109 r62!); babica Bara Adlešič",
    whatEn: "baptized Vincencij (died ~3 years old; marg. »+ 8/9 1919« — the war!) (Apr 28/29) — father **Ivan Dragos? [~]**, half-estate farmer, born Jul 5, 1867, mother **Barbara née Grintkenič? [~]** (Dec 11, 1871); h12 = the 14th ENTRY (1892–1912) — a 4-YEAR GAP; **the 2nd GRIBLJE row of 1916!**; godparents **Štefk Matija? [~]** + **Marija TOTER** (the estate's unmarried daughter); midwife Bara Adlešič",
    status: "DOCUMENTED",
  },
  {
    houseNo: "82",
    bookSignature: "04105",
    year: 1916,
    scan: 287,
    page: 241,
    whatSi: "krščena Ana († ~3 leta; marg. »+ 8/9 1919« — ista † kot h12 r21!) (16./16. 5.; mesec glava »majnik« = pisarska idiosinkrazija za maj — NOVELA!) — oče **Peter Vrebec? [~]**, **TESARSKI MOJ.** (nov poklic v Gribljih!), roj. 16.8.1882, mati **Terezija roj. Muc** (12.10.1887); **h82 = 1. VPIS V VSEH TREH KNJIGAH = NOVA HIŠA vzorca!** (PT set jo že pokriva); **3. GRIBLJE vrstica 1916!**; prečrtan pisarjev false start v vas koloni; hiša 82 ZOOM 4× jasno (dvom 82/32 ZAVRŽENO); botra **Ožbald Jakofčič? [~]** + **Terezija Jakofčič**; babica Marija Jakofčič; podpis V. Valerijan Učak",
    whatEn: "baptized Ana (died ~3 years old; marg. »+ 8/9 1919« — the same † as h12 r21!) (May 16/16; the month heading »majnik« = the scribe's idiosyncrasy for May — a NOVELTY!) — father **Peter Vrebec? [~]**, a **CARPENTER MASTER** (a new trade in Griblje!), born Aug 16, 1882, mother **Terezija née Muc** (Oct 12, 1887); **h82 = the 1st ENTRY IN ALL THREE BOOKS = a NEW SAMPLE HOUSE!**; **the 3rd GRIBLJE row of 1916!**; a crossed-out scribe's false start in the village cell; house 82 ZOOM 4× clear; godparents **Ožbald Jakofčič? [~]** + **Terezija Jakofčič**; midwife Marija Jakofčič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1916,
    scan: 287,
    page: 241,
    whatSi: "krščen Anton (22./23. 5.; EMŠO ž. **2205916500023** — ZOOM 4.5× jasno → 22.5.1916 ✓) — oče **Janez Hrižan**, posest ½ ž., roj. 11.1.1861, mati **Katarina roj. Štincelj? [~]** (13.3.1874); h36 = 12. VPIS (1886–1913) — VRZEL 3 LETA; **4. GRIBLJE vrstica 1916!**; marg. »Umrl dne 19.12.**1983** v Gribljah, str. 126, 20/2-1984« (**faza-1 »1980« POPRAVLJENO!**) + »em poročen s Kambič? Katarino?« (2. poroka!); botra **Matija Pezdirc** (posestnik) + **Marjeta ŠTRAUS** (posest žena — cf. P107 h36 par!); babica Marija Jakofčič; podpis V. Valerijan Učak",
    whatEn: "baptized Anton (May 22/23; the personal ID **2205916500023** — ZOOM 4.5× clear → May 22, 1916 ✓) — father **Janez Hrižan**, half smallholder, born Jan 11, 1861, mother **Katarina née Štincelj? [~]** (Mar 13, 1874); h36 = the 12th ENTRY (1886–1913) — a 3-YEAR GAP; **the 4th GRIBLJE row of 1916!**; marg. »died Dec 19, **1983** in Griblje, p. 126, Feb 20, 1984« (**the phase-1 »1980« CORRECTED!**) + »remarried Katarina Kambič?« (a 2nd marriage!); godparents **Matija Pezdirc** + **Marjeta ŠTRAUS**; midwife Marija Jakofčič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1916,
    scan: 287,
    page: 241,
    whatSi: "krščena Neža († dojenček ~1 teden!; marg. »+ 9/7 1916«) (21./23. 6.) — oče **Peter Brinec**, **bajtar**, roj. 28.9.1860, mati **Ana roj. Butala** (22.12.1879); **h88 ZAPORED 2. LETO: 1915 Ivana + 1916 Neža — ISTA starša (Brinec × Butala) + ISTI botri (Janez + Doroteja Brinec) — familija Brinec ×3!**; h88 = 4. VPIS (1904, 1910, 1915 → 1916) — VRZEL 1 LETO; **5. GRIBLJE vrstica 1916!**; datumi 21./23. ZOOM 4× jasno; babica Marija Muc; podpis V. Valerijan Učak",
    whatEn: "baptized Neža (died an infant ~1 week old!; marg. »+ 9/7 1916«) (Jun 21/23) — father **Peter Brinec**, a **cottager**, born Sep 28, 1860, mother **Ana née Butala** (Dec 22, 1879); **h88 CONSECUTIVE 2nd YEAR: 1915 Ivana + 1916 Neža — the SAME parents (Brinec × Butala) + the SAME godparents (Janez + Doroteja Brinec) — the Brinec family ×3!**; h88 = the 4th ENTRY (1904, 1910, 1915 → 1916) — a 1-YEAR GAP; **the 5th GRIBLJE row of 1916!**; midwife Marija Muc; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "37",
    bookSignature: "04105",
    year: 1916,
    scan: 290,
    page: 244,
    whatSi: "**Marko MRTVOROJEN** (29. 12.; krsta kolona: **»krščena v sili in utero m.« = NUJNI KRST V MATERNICI — PRVI TAK SIGNAL V VZORCU!** ZOOM 4× — 3 vrstice) — oče **Marko Hubljan? [~]**, posestnik, roj. 30.7.1889, mati **Ivana roj. Hukan? [~]** (7.5.1893); **h37 = 3. VPIS (1895, 1897 → 1916) — VRZEL 19 LET = 2. najdaljša (po h78 27!) — in njen edini 1916 vpis je MRTVOROJEN!**; **6. GRIBLJE vrstica 1916!**; zap. št. 41 = zadnja (zaključna opomba »I številko 41 … v l. 1916«); botra/podpis PRAZNO; **DVOJNI MODEL r28+r29 (Krasinec 8 — 2 vrstici istega otroka!) vs. ENOVRSIČNI r41 = 2 protokola mrtvorojenih!**; babica Ana Marentič",
    whatEn: "**Marko STILLBORN** (Dec 29; the baptism column: **»baptized in emergency in utero matris« = an EMERGENCY IN-WOMB BAPTISM — the FIRST such signal in the sample!** ZOOM 4× — 3 lines) — father **Marko Hubljan? [~]**, farmer, born Jul 30, 1889, mother **Ivana née Hukan? [~]** (May 7, 1893); **h37 = the 3rd ENTRY (1895, 1897 → 1916) — a 19-YEAR GAP = the 2nd longest (after h78 27!) — and its only 1916 entry is STILLBORN!**; **the 6th GRIBLJE row of 1916!**; serial no. 41 = the last (the closing note »I številko 41 … in 1916«); godparents/signature EMPTY; **the DOUBLE model r28+r29 (Krasinec 8 — 2 rows for the same child!) vs. the SINGLE-ROW r41 = 2 stillbirth protocols!**; midwife Ana Marentič",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1917,
    scan: 291,
    page: 245,
    whatSi: "krščen Karol Feliks (4./6. 1.; mesec glava **»jamarija« = NOVA idiosinkrazija za januar** — cf. marecij/majnik!) — oče **Franc Rajmer? [~ Rajhner?]**, **CEVLJAR** (1. čevljar-oče vzorca!), roj. 3.12.1882, mati **Ivana roj. Tadej** (13.3.1886); h45 = 7. VPIS (1896–1915) — VRZEL 2 LETA; **1. GRIBLJE vrstica 1917!** (P111 lead POTRJEN!); botra **Ožbald Jakofčič** (1. od 3 vlog 1917!) + Katarina Pezdire; babica Marentič izpr. (brez imena); marg.: **»Zakonska zveza razvezana s pravomočno odločbo sodišča v Ljubljani št. 9.309/356« = RAZVEZANA ZVEZA 1956 (2. primer! cf. P110 A12 Karlovci) + ov. poročen 13.5.1946 z Anico? [~]** + umrl 05.06.1989 v Jesenicah (NKU NO Jesenice 1.1989, str. 236, zap. št. 221); podpis ornatni »C?dinus Šibar?« [~ = najverj. Paulinus Bitnar]",
    whatEn: "baptized Karol Feliks (Jan 4/6; the month heading **»jamarija« = a NEW idiosyncrasy for January** — cf. marecij/majnik!) — father **Franc Rajmer? [~ Rajhner?]**, a **SHOEMAKER** (the 1st shoemaker-father of the sample!), born Dec 3, 1882, mother **Ivana née Tadej** (Mar 13, 1886); h45 = the 7th ENTRY (1896–1915) — a 2-YEAR GAP; **the 1st GRIBLJE row of 1917!** (the P111 lead CONFIRMED!); godparents **Ožbald Jakofčič** (the 1st of his 3 roles in 1917!) + Katarina Pezdire; midwife Marentič izpr. (no first name); marg.: **»the marriage dissolved by a final court decision in Ljubljana no. 9.309/356« = a DISSOLVED UNION 1956 (the 2nd case! cf. P110 A12 Karlovci) + remarried May 13, 1946 to Ana? [~]** + died Jun 5, 1989 in Jesenice; signature ornate »C?dinus Šibar?« [~ = most likely Paulinus Bitnar]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "62",
    bookSignature: "04105",
    year: 1917,
    scan: 291,
    page: 245,
    whatSi: "krščena Marija (9./9. 1.) — oče **Janez Kure**, k.ž. posestnik, roj. 8.12.1884, mati **Marija roj. Požek** (13.6.1882; por. 26.11.1906); h62 = 4. VPIS (1887, 1891, 1907 → 1917) — **VRZEL 10 LET = najdaljša aktivna vrzel 1917!** (2. najdaljša vzorca za h78 27!); **2. GRIBLJE vrstica 1917!**; botra **Ivan Brinc posestnik GRIBLJE 10** (familija Brinec! cf. A19) + Ana Brinc; babica Katarina Uak? [~] nah. izpr.; marg. rdeče-svinčnik: **»‡ 18/1 1917« = umrla pri 9 dneh!**",
    whatEn: "baptized Marija (Jan 9/9) — father **Janez Kure**, smallholder landowner, born Dec 8, 1884, mother **Marija née Požek** (Jun 13, 1882; m. Nov 26, 1906); h62 = the 4th ENTRY (1887, 1891, 1907 → 1917) — **a 10-YEAR GAP = the longest active gap of 1917!** (the 2nd longest of the sample after h78 27!); **the 2nd GRIBLJE row of 1917!**; godparents **Ivan Brinc, landowner GRIBLJE 10** (the Brinec family! cf. A19) + Ana Brinc; midwife Katarina Uak? [~] nah. izpr.; red-pencil marg.: **»died Jan 18, 1917« = died aged 9 days!**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1917,
    scan: 293,
    page: 247,
    whatSi: "**MRTVOROJEN** (21. 3.; krsta »—«) — oče **Janez Brinec**, k.ž. posestnik, roj. 20.3.1862 (**star 55!**), mati **Dorotija Pezdire** r. 1.10.1881 (por. 25.10.1908); h14 = 7. VPIS (1896–1914) — VRZEL 3 LETA; **3. GRIBLJE vrstica 1917!**; **MRTVOROJENI PROTOCOL enovrstični (cf. P111 r41): botra/babica/podpis VSI »—« = nihče ne krsti mrtvorojenega; spola MOŠKEGA** — 1. od 3 protokolov 1917 (r14 + r38 + r40 v sili); familija Brinec (cf. A19)",
    whatEn: "**STILLBORN** (Mar 21; baptism »—«) — father **Janez Brinec**, smallholder landowner, born Mar 20, 1862 (**aged 55!**), mother **Dorotija Pezdire** b. Oct 1, 1881 (m. Oct 25, 1908); h14 = the 7th ENTRY (1896–1914) — a 3-YEAR GAP; **the 3rd GRIBLJE row of 1917!**; the SINGLE-ROW STILLBIRTH protocol (cf. P111 r41): godparents/midwife/signature ALL »—« = no one baptizes a stillborn; sex MALE — the 1st of 3 protocols of 1917 (r14 + r38 + r40 in-extremis); the Brinec family (cf. A19)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "31",
    bookSignature: "04105",
    year: 1917,
    scan: 293,
    page: 247,
    whatSi: "krščena Ana (12./13. 4.; EMŠO je: **1204917505096** → 12.4. ✓; 8. št. = 5 = »moška« šifra pri ženskem imenu — cf. A10!) — oče **Janez Papič**, **mali posebnik in kolar? [~ holar/Kolar — poklic ali priimek dvom!]**, roj. 6.9.1887, mati **Katarina roj. Križan** (20.1.1887; por. 20.1.1911); h31 = 10. VPIS (1887–1913) — VRZEL 4 LETA; **4. GRIBLJE vrstica 1917!**; botra **Miko Brodanič? [~ Brodnik?]** kmeč. posestnik + Bara Lozar; babica Marija Jakofčič neizpr.; marg.: **PEČAT »VPIS PRENEŠEN V MATIČNI REGISTER, dne 23.08.1966, Matičarka: Ivana Šimunič« = 1. od 4 prenosov 1917 (NOVELA — cf. A6!)** + poročena 24.11.1941 + živ. por. 24.5.1947 z [~ Kovačičevim?]; podpis Valerijan Učak ord. tout.",
    whatEn: "baptized Ana (Apr 12/13; the personal ID **1204917505096** → Apr 12 ✓; the 8th digit = 5 = a »male« code on a female name — cf. A10!) — father **Janez Papič**, a **smallholder and wheelwright? [~ holar/Kolar — a trade or a surname, unclear!]**, born Sep 6, 1887, mother **Katarina née Križan** (Jan 20, 1887; m. Jan 20, 1911); h31 = the 10th ENTRY (1887–1913) — a 4-YEAR GAP; **the 4th GRIBLJE row of 1917!**; godparents **Miko Brodanič? [~ Brodnik?]** + Bara Lozar; midwife Marija Jakofčič neizpr.; marg.: the STAMP »ENTRY TRANSFERRED TO THE CIVIL REGISTER, Aug 23, 1966, registrar Ivana Šimunič« = the 1st of 4 transfers of 1917 (a NOVELTY — cf. A6!) + married Nov 24, 1941; signature Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1917,
    scan: 295,
    page: 249,
    whatSi: "krščen Anton (28./29. 5.; mesec glava »majnik«; EMŠO je: **2805917500040** → 28.5. ✓ **ZOOM 5× — faza-1 »2803« POPRAVLJENO!**) — oče **Janez Brinec**, posestnik, roj. 22.11.1880, mati **Ana roj. Milek** (25.9.1889; por. 22.5.1905); h24 = 16. VPIS (1887–1912 — **največkrat vpisana gribljska hiša do 1917!**) — VRZEL 5 LET; **5. GRIBLJE vrstica 1917!**; **DVOJČEK #1 (a) — r26+r27: isti dan 28.5.1917 (EMŠO oba 2805917!), isti krstni dan 29.5., ISTI starši (identična celica), ISTI botri, ISTA babica — 7. par vzorca!**; botra Miko Šegina? [~ Segina] + Marija Brinec; babica Bara Adlešič neizpr.; podpis P. Valerijan Učak ord. taut.",
    whatEn: "baptized Anton (May 28/29; the month heading »majnik«; the personal ID **2805917500040** → May 28 ✓ **ZOOM 5× — the phase-1 »2803« CORRECTED!**) — father **Janez Brinec**, landowner, born Nov 22, 1880, mother **Ana née Milek** (Sep 25, 1889; m. May 22, 1905); h24 = the 16th ENTRY (1887–1912 — **the most-registered Griblje house up to 1917!**) — a 5-YEAR GAP; **the 5th GRIBLJE row of 1917!**; **TWIN BOY #1 (a) — r26+r27: the same day May 28, 1917 (both EMŠO 2805917!), the same baptism day, IDENTICAL parents, IDENTICAL godparents, IDENTICAL midwife — the 7th pair of the sample!**; godparents Miko Šegina? + Marija Brinec; midwife Bara Adlešič; signature P. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "24",
    bookSignature: "04105",
    year: 1917,
    scan: 295,
    page: 249,
    whatSi: "krščena Ivana (28./29. 5.; EMŠO je: **2805917505115** → 28.5. ✓ — **EDINA INTRA-LETNA PONOVITEV hiše 1917!**) — starši/botri/babica IDENTIČNO r26 (Janez Brinec × Ana Milek; Miko Šegina? + Marija Brinec; Bara Adlešič); **DVOJČICA #1 (b) — 8. par vzorca (4. leto z dvojčki: P108/P109/P110/P112!); NARE ostaja: vseh 11 hiš obstoječih**; podpis P. Valerijan Učak ord. taut.",
    whatEn: "baptized Ivana (May 28/29; the personal ID **2805917505115** → May 28 ✓ — **the ONLY intra-year house repeat of 1917!**) — parents/godparents/midwife IDENTICAL to r26 (Janez Brinec × Ana Milek; Miko Šegina? + Marija Brinec; Bara Adlešič); **TWIN GIRL #1 (b) — the 8th pair of the sample (the 4th year with twins: P108/P109/P110/P112!); NARE holds: all 11 houses pre-existing**; signature P. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1917,
    scan: 296,
    page: 250,
    whatSi: "krščen Julij (21./21. 7.) — oče **Anton Brodarič? [~ Brodarić/Brodanič?]**, posestnik, **roj. 14.11.1859 (STAR 57–58!)**, mati **Katarina Milek** roj. 1.8.1876 (por. 7.11.1904); h46 = 10. VPIS (1893–1915) — VRZEL 2 LETA; **7. GRIBLJE vrstica 1917!**; botra **Nikolaj Željko POSEST. IN ŽUPAN** (1. od 3 županov-botrov 1917! cf. A13) + Ana Pezdire; babica Marija Jakofčič neizpr.; marg.: **»+ 16.7.1928« = umrl pri 11 letih (1928!)**; podpis Valerijan Učak ord. tout.",
    whatEn: "baptized Julij (Jul 21/21) — father **Anton Brodarič? [~ Brodarić/Brodanič?]**, landowner, **born Nov 14, 1859 (AGED 57–58!)**, mother **Katarina Milek** b. Aug 1, 1876 (m. Nov 7, 1904); h46 = the 10th ENTRY (1893–1915) — a 2-YEAR GAP; **the 7th GRIBLJE row of 1917!**; godparents **Nikolaj Željko, LANDOWNER AND MAYOR** (the 1st of 3 mayor-godfathers of 1917! cf. A13) + Ana Pezdire; midwife Marija Jakofčič neizpr.; marg.: **»+ Jul 16, 1928« = died aged 11 (1928!)**; signature Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1917,
    scan: 296,
    page: 250,
    whatSi: "krščen Jakob (22./24. 7.; EMŠO je: **2207917500054** → 22.7. ✓ **ZOOM 5× — faza-1 »2204« POPRAVLJENO!**) — oče **PRAZNO (nezakonski!)**, mati **Mara Hudorovac CIGANKA (Romnja) — 1. EKSPlicitNA ETNIČNA OZNAČBA VZORCA!** (socialna zgodovina Bele krajine 1917; cf. A12); h5 = 8. VPIS (1891–1914) — VRZEL 3 LETA; **8. GRIBLJE vrstica 1917!**; botra »—« (BREZ boter = popolna socialna izolacija vpisa!); babica/podpis pokrito s trakom; marg.: poročen 24.11.1941 + domači poročen 8.5.1951 v [Gradacu? ~] + umrl 25.12.2004 v [Zemelju? ~] (NKU NO Metlika 1.2004; matičarka Vesna Šimunič [~])",
    whatEn: "baptized Jakob (Jul 22/24; the personal ID **2207917500054** → Jul 22 ✓ **ZOOM 5× — the phase-1 »2204« CORRECTED!**) — father EMPTY (illegitimate!), mother **Mara Hudorovac, a GYPSY WOMAN (Romnja) — the 1st EXPLICIT ETHNIC LABEL of the sample!** (the social history of Bela krajina 1917; cf. A12); h5 = the 8th ENTRY (1891–1914) — a 3-YEAR GAP; **the 8th GRIBLJE row of 1917!**; godparents »—« (NO godparents = the total social isolation of the entry!); midwife/signature covered by tape; marg.: married Nov 24, 1941 + married locally May 8, 1951 + died Dec 25, 2004",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1917,
    scan: 297,
    page: 251,
    whatSi: "krščena Katarina (1./2. 9.) — oče **Peter Brinc**, MALI POSESTNIK, **roj. 28.9.1860 (star 57!)**, mati **Katarina Bahorič** roj. 18.10.1888 (**por. 12.11.1916 — 1. otrok po 8 mesecih!**); **h88 ZAPORED 3. LETO!** (1915 P110 r8 + 1916 P111 r26 + 1917 = **1. trojno zaporedje hiše v vojnih letih!**); h88 = 5. VPIS (1904–1916); **9. GRIBLJE vrstica 1917!**; botra **Ožbald Jakofčič** (2. vloga 1917!) + Magda Bahorič; babica Marija Jakofčič; marg.: **»† 9.11.1918« = umrla pri 14 mesecih — TEDEN DO KONCA VOJNE!** (predaja 11.11.1918); podpis Valerijan Učak ord. teat",
    whatEn: "baptized Katarina (Sep 1/2) — father **Peter Brinc**, a SMALL landowner, **born Sep 28, 1860 (aged 57!)**, mother **Katarina Bahorič** b. Oct 18, 1888 (**m. Nov 12, 1916 — the 1st child 8 months after the wedding!**); **h88 CONSECUTIVE the 3rd YEAR!** (1915 P110 r8 + 1916 P111 r26 + 1917 = **the 1st triple consecutive run of a house in the war years!**); h88 = the 5th ENTRY (1904–1916); **the 9th GRIBLJE row of 1917!**; godparents **Ožbald Jakofčič** (his 2nd role of 1917!) + Magda Bahorič; midwife Marija Jakofčič; marg.: **»died Nov 9, 1918« = died aged 14 months — A WEEK BEFORE THE END OF THE WAR!** (the armistice Nov 11, 1918); signature Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "77",
    bookSignature: "04105",
    year: 1917,
    scan: 297,
    page: 251,
    whatSi: "krščena Katarina (12./13. 9.; EMŠO je: 1209917505071 [~] → 12.9. ✓) — oče **Jurij Sočik? [~ Socik/Sočih]**, mali posestnik, roj. 6.5.1883, mati **Katarina Veselič** roj. 12.4.1885 (por. 12.5.1907); h77 = 5. VPIS (1890–1914) — VRZEL 3 LETA; **10. GRIBLJE vrstica 1917!**; botra Matija Šimec posestnik + Ana Mlekh [~ Milek] posest. žena; babica Marija Jakofčič; marg.: **PEČAT »VPIS PRENEŠEN V MATIČNI REGISTER dne 14.11.2007« (2. pečat 1917!)** + Vročena? 26.11.1944 z Ambrož? Avguštinom [~] + mož umrl 10.08.1987 v Ljubljani (NKU NO Ljubljana-center 1987, str. 128, zap. št. 2276); podpis Valerijan Učak ord. tout.",
    whatEn: "baptized Katarina (Sep 12/13; the personal ID 1209917505071 [~] → Sep 12 ✓) — father **Jurij Sočik? [~ Socik/Sočih]**, small landowner, born May 6, 1883, mother **Katarina Veselič** b. Apr 12, 1885 (m. May 12, 1907); h77 = the 5th ENTRY (1890–1914) — a 3-YEAR GAP; **the 10th GRIBLJE row of 1917!**; godparents Matija Šimec + Ana Mlekh [~ Milek]; midwife Marija Jakofčič; marg.: the STAMP »ENTRY TRANSFERRED TO THE CIVIL REGISTER Nov 14, 2007« (the 2nd stamp of 1917!) + married Nov 26, 1944 to Ambrož? Avguštin? [~] + the husband died Aug 10, 1987 in Ljubljana; signature Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04105",
    year: 1917,
    scan: 298,
    page: 252,
    whatSi: "krščen Janez (24./25. 10.) — oče **Ožbald Jakobčič? [~ Jakofčič — ortografija variira!]**, posestnik, roj. 3.8.1889, mati **Terezija roj. Klepec** (21.6.1890; por. 6.2.1911); h9 = 5. VPIS (1896–1915) — VRZEL 2 LETA; **11. GRIBLJE vrstica 1917!**; **oče = ISTI OŽBALD JAKOFČIČ, ki je boter r1 + r41 — 3. vloga v enem letu (2× boter + 1× oče! cf. A20)**; botra Anton Marentič posestnik + Marija Žunič; babica Marija Jakobčič; podpis Valerijan Učak ord. tout.",
    whatEn: "baptized Janez (Oct 24/25) — father **Ožbald Jakobčič? [~ Jakofčič — the spelling varies!]**, landowner, born Aug 3, 1889, mother **Terezija née Klepec** (Jun 21, 1890; m. Feb 6, 1911); h9 = the 5th ENTRY (1896–1915) — a 2-YEAR GAP; **the 11th GRIBLJE row of 1917!**; **the father = the SAME OŽBALD JAKOFČIČ who is the godfather of r1 + r41 — his 3rd role in one year (2× godfather + 1× father! cf. A20)**; godparents Anton Marentič + Marija Žunič; midwife Marija Jakobčič; signature Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "37",
    bookSignature: "04105",
    year: 1917,
    scan: 298,
    page: 252,
    whatSi: "krščena Marija (8./9. 12.; EMŠO je: **0812917505459** → 8.12. ✓) — oče **Marko Stublar? [~ Stubljar]**, posestnik, roj. 30.5.1898 [popravki: prečrtano + pripis »30.« + »89→98«], mati **Ivana roj. Kukar** (7.5.1893; por. 27.2.1916); h37 = 5. VPIS (1895, 1897, **1916 MRTVOROJEN** → 1917) — **h37 NADALJUJE po P111 mrtvorojencu (vrzel 19 let zaključena!)**; **12. GRIBLJE vrstica 1917!**; botra Matija Šimec posestnik + Katarina Križan; babica Marija Piletič; marg.: **PEČAT »VPIS PRENEŠEN V MATIČNI REGISTER, dne 14.11.2007, matičarka [B~l~lončič? ~]« (3. pečat!) + ZAKONEC [Lipovec?] Jože umrl 26.3.1945 v [Zejcih? ~] = MOŽ † WWII! (cf. A21)** + Sklenila zakonsko zvezo 03.11.1940 z [Lipovec?] Jožefom (PPK Kočevje [~], rep. št. 25); podpis Valerijan Učak o.t.",
    whatEn: "baptized Marija (Dec 8/9; the personal ID **0812917505459** → Dec 8 ✓) — father **Marko Stublar? [~ Stubljar]**, landowner, born May 30, 1898 [corrections: crossed out + added »30.« + »89→98«], mother **Ivana née Kukar** (May 7, 1893; m. Feb 27, 1916); h37 = the 5th ENTRY (1895, 1897, **1916 STILLBORN** → 1917) — **h37 CONTINUES after the P111 stillbirth (the 19-year gap closed!)**; **the 12th GRIBLJE row of 1917!**; godparents Matija Šimec + Katarina Križan; midwife Marija Piletič; marg.: the STAMP »ENTRY TRANSFERRED TO THE CIVIL REGISTER Nov 14, 2007« (the 3rd stamp!) + the HUSBAND [Lipovec?] Jože died Mar 26, 1945 in [Zejcih? ~] = the HUSBAND † WWII! (cf. A21) + the marriage sealed Nov 3, 1940; signature Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "86",
    bookSignature: "04105",
    year: 1918,
    scan: 300,
    page: 254,
    whatSi: "krščena Marija (11./12. 1.) — oče **Marko Šuštar? [~ Šurhan?]**, posednik, roj. 3.8.1885, mati **Katarina Štravs** (13.9.1891; por. 11.7.1910); h86 = VPIS po **VRZELI 4 LET** (1912+1913 → 1918); **1. GRIBLJE vrstica 1918!**; botra Jožef Padric? [~] + Katarina Padric; babica Marija Piletič? [~]; marg.: † 16.9.1974 v Gribljah (MRD 1.1974, str. 100, zap. št. 3) + 21.9.1974; podpis Valerijan Učak",
    whatEn: "baptized Marija (Jan 11/12) — father **Marko Šuštar? [~ Šurhan?]**, landowner, born Aug 3, 1885, mother **Katarina Štravs** (Sep 13, 1891; m. Jul 11, 1910); h86 = an ENTRY after a **4-YEAR GAP** (1912+1913 → 1918); **the 1st GRIBLJE row of 1918!**; godparents Jožef Padric? [~] + Katarina Padric; midwife Marija Piletič? [~]; marg.: died Sep 16, 1974 in Griblje (MRD 1/1974, p. 100, ref. 3) + Sep 21, 1974; signature Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1918,
    scan: 303,
    page: 256,
    whatSi: "krščena Ivana (14. 5.; krsta pod marg) — oče **Nikolaj Štilak? [~]**, m.k. posednik, roj. 8.12.1877, mati **Katarina r. Klobučar** (23.7.1877; por. 17.10.1898); h34 = **11. VPIS** (1887–1916 → 1918; VRZEL 1 LETO); **3. GRIBLJE vrstica 1918!**; botra Matija Ulh? [~] + Katarina Kližan?; babica Bara Adlešič reizp.; **podpis Paulinus Bitnar (KAPLAN — jasno; cf. P112 r49/r53–r55!)**; marg (r16/r17 meja [~]): zaročena 4.5.1945 + 1. žena umrla 25.02.1967 Novo mesto",
    whatEn: "baptized Ivana (May 14; the baptism under marg) — father **Nikolaj Štilak? [~]**, small landowner, born Dec 8, 1877, mother **Katarina née Klobučar** (Jul 23, 1877; m. Oct 17, 1898); h34 = the **11th ENTRY** (1887–1916 → 1918; a 1-YEAR GAP); **the 3rd GRIBLJE row of 1918!**; godparents Matija Ulh? [~] + Katarina Kližan?; midwife Bara Adlešič; **signature Paulinus Bitnar (the CHAPLAIN — clear; cf. P112!)**; marg (r16/r17 boundary [~]): engaged May 4, 1945 + the 1st wife died Feb 25, 1967 Novo mesto",
    status: "DOCUMENTED",
  },
  {
    houseNo: "21",
    bookSignature: "04105",
    year: 1918,
    scan: 304,
    page: 257,
    whatSi: "krščen Alojzij (2./5. 7.) — **NEZAKONSKA (očetova celica PRAZNA!; stan = nezakonskega!)**, mati **Katarina Poček**, posedt. sam. hči (roj. 4.10.1893); h21 = **10. VPIS** (1887–1914 → 1918; **VRZEL 3 LETI**); **4. GRIBLJE vrstica 1918!**; **EMŠO je: 0707918500142 (= 07.07.1918) — DATUMSKI DVOM (rojstva 2.07; cf. P112 popravki!)**; marg † 23.1.1992 Ljubljana (MKU MO Ljubljana 1.1992, zap. št. 364); botra Miko Mihelčič? [~] + Majsta?/Agata? Jžek? [~]; **podpis Leopold Kolbezen, ŽUP. UPRAVITELJ — 1. podpis žup. upr. v vzorcu (med Učak r23 in Učak r25!)**",
    whatEn: "baptized Alojzij (Jul 2/5) — **ILLEGITIMATE (the father's cell EMPTY!; the status = illegitimate!)**, mother **Katarina Poček**, a landowner's unmarried daughter (born Oct 4, 1893); h21 = the **10th ENTRY** (1887–1914 → 1918; a **3-YEAR GAP**); **the 4th GRIBLJE row of 1918!**; **personal ID 0707918500142 (= Jul 7, 1918) — a DATE DOUBT (the birth Jul 2; cf. the P112 corrections!)**; marg died Jan 23, 1992 Ljubljana (MKU MO Ljubljana 1/1992, ref. 364); godparents Miko Mihelčič? [~] + Majsta?/Agata? Jžek? [~]; **signature Leopold Kolbezen, the PARISH ADMINISTRATOR — the 1st administrator signature in the sample (between Učak r23 and Učak r25!)**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1918,
    scan: 305,
    page: 258,
    whatSi: "krščen Nikolaj (9./10. 8.) — oče **Janez Dragoš? [~]**, posednik, roj. 23.11.1873, mati **Marjeta Legirke? [~]** (17.12.1894; por. 21.4.1913); h53 = **7. VPIS** (1891–1915 → 1918; **VRZEL 2 LETI**); **5. GRIBLJE vrstica 1918!**; marg † **18/3. 1919** (dojenček!); botra Štravs Matija + Ogriže? [~] Katarina; babica Mara Jakofčič reizp.? [~]; podpis Učak d.ž.; vrstica berljiva na OBEH dup skenih (s305 + s306)",
    whatEn: "baptized Nikolaj (Aug 9/10) — father **Janez Dragoš? [~]**, landowner, born Nov 23, 1873, mother **Marjeta Legirke? [~]** (Dec 17, 1894; m. Apr 21, 1913); h53 = the **7th ENTRY** (1891–1915 → 1918; a **2-YEAR GAP**); **the 5th GRIBLJE row of 1918!**; marg died **Mar 18, 1919** (an infant!); godparents Štravs Matija + Ogriže? [~] Katarina; midwife Mara Jakofčič [~]; signature Učak; the row legible on BOTH dup scans (s305 + s306)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1918,
    scan: 308,
    page: 260,
    whatSi: "krščen Anton (3./4. 10.; **EMŠO je: 0310918500439 → 3.10. ✓ SKLADNO — SIDRO**) — oče **Franc Rajmr? [~ Rajhner?]**, **ČEVLJAR** (2. čevljar-oče cf. P112 r1!), roj. 3.11.1882, mati **Ivana Tidič? [~]** (23.3.1885); h45 = **8. VPIS — ZAPORED 2. LETO (1917 Karol Feliks + 1918 Anton!)**; **6. GRIBLJE vrstica 1918!**; marg: poročila 21.6.1947 v **ZAGREBU** (sv. Marko? [~]) + † 3.4.1982 (MKU MO Ljubljana 1982, št. 1889; maticarka Ana Drušić? [~]); babica Marija Jakofčič reizp.; **podpis Jožef(o) Lopar, KAPLAN — 3. duhovnik 1918!**",
    whatEn: "baptized Anton (Oct 3/4; **personal ID 0310918500439 → Oct 3 ✓ CONSISTENT — an ANCHOR**) — father **Franc Rajmr? [~ Rajhner?]**, a **SHOEMAKER** (the 2nd shoemaker-father cf. P112 r1!), born Nov 3, 1882, mother **Ivana Tidič? [~]** (Mar 23, 1885); h45 = the **8th ENTRY — CONSECUTIVE the 2nd YEAR (1917 Karol Feliks + 1918 Anton!)**; **the 6th GRIBLJE row of 1918!**; marg: married Jun 21, 1947 in **ZAGREB** (St Mark? [~]) + died Apr 3, 1982 (MKU MO Ljubljana 1982, no. 1889; registrar Ana Drušić? [~]); midwife Marija Jakofčič; **signature Jožef(o) Lopar, the CHAPLAIN — the 3rd priest of 1918!**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "30",
    bookSignature: "04105",
    year: 1918,
    scan: 308,
    page: 260,
    whatSi: "krščen Franc (10./11. 10.; **EMŠO je: 1010918500188 → 10.10. ✓ SKLADNO — SIDRO**) — oče **Miko Šegina**, kmuč. posednik, roj. 22.11.1883, mati **Katarina Brinec** (30.9.1885? [~]; por. 12.5.1912); h30 = **13. VPIS — VRZEL 6 LET** (1911 → 1918; **najdaljša aktivna 1918!**); **7. GRIBLJE vrstica 1918!**; marg: zaročen 28.11.1953 v Metlikah [~] + zakonec Šegina? Ivan † 9.8.1975 Novo mesto (MRK 1.1975, str. 39, zap. 257; Gradec 25.9.1975 Valenčič Klara) + † 27.9.2000 Metlika (MKU MO Metlika 1.2000, str. 81, zap. 71); babica Marija Jakofčič reizp.; podpis Učak",
    whatEn: "baptized Franc (Oct 10/11; **personal ID 1010918500188 → Oct 10 ✓ CONSISTENT — an ANCHOR**) — father **Miko Šegina**, a smallholder, born Nov 22, 1883, mother **Katarina Brinec** (Sep 30, 1885? [~]; m. May 12, 1912); h30 = the **13th ENTRY — a 6-YEAR GAP** (1911 → 1918; **the longest active of 1918!**); **the 7th GRIBLJE row of 1918!**; marg: engaged Nov 28, 1953 in Metlika [~] + the spouse Šegina? Ivan died Aug 9, 1975 Novo mesto (MRK 1/1975, p. 39, ref. 257; Gradec Sep 25, 1975 Valenčič Klara) + died Sep 27, 2000 Metlika (MKU MO Metlika 1/2000, p. 81, ref. 71); midwife Marija Jakofčič; signature Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "14",
    bookSignature: "04105",
    year: 1918,
    scan: 308,
    page: 260,
    whatSi: "krščena Barbara (15./16. 10.) — oče **Janez Brinec**, kmuč. posednik, roj. 20.3.1884, mati **Terezija Bogdine? [~]** (1.10.1887; por. 25.10.1913); h14 = **9. VPIS — ZAPORED 2. LETO (1917 mrtvorojen + 1918!)**; **8. GRIBLJE vrstica 1918!**; marg † **19/6. 1920** (dojenčka!); botra Peter + Katarina Brinec (**BRINEC mreža: oče Janez + botra Peter/Katarina + h30 mati Katarina Brinec!**); babica Marija Jakofčič reizp.; podpis Učak d.ž.",
    whatEn: "baptized Barbara (Oct 15/16) — father **Janez Brinec**, a smallholder, born Mar 20, 1884, mother **Terezija Bogdine? [~]** (Oct 1, 1887; m. Oct 25, 1913); h14 = the **9th ENTRY — CONSECUTIVE the 2nd YEAR (the 1917 stillbirth + 1918!)**; **the 8th GRIBLJE row of 1918!**; marg died **Jun 19, 1920** (an infant girl!); godparents Peter + Katarina Brinec (**the BRINEC network: the father Janez + the godparents Peter/Katarina + the h30 mother Katarina Brinec!**); midwife Marija Jakofčič; signature Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "sub dioe.",
    bookSignature: "04105",
    year: 1918,
    scan: 309,
    page: 261,
    whatSi: "krščena Vilhelma (6./10. 11.) — **hišna celica = »sub dioe.« (pod drugo škofijo — brez številke; 4. tak vpis 1918 in 1. GRIBLJSKI — vsi 4 = ciganske/begunske družine!)** — oče **Jožef Brajdič, CIG.** (2. Brajdič 1918 — cf. r10 nemška sodba BRAJDIČ!), roj. 13.2.1875, mati **Marta r. Malovšič? [~]** (26.9.1876; por. 10.3.1910 v Štropicah? [~]); **9. GRIBLJE vrstica 1918 (zadnja)!**; EMŠO 2104191850345? [dvom branja — ≠ rojstva 6.11]; marg [Anthoineta?] 20.6.1950 Nova gorica (MKU MO NG 1.1950, str. 945, zap. 1088) + 14.5.1952; botra Marija Grabrijan? [~] iz Čebrovc 31?; babica — (črtica); podpis Učak ord. tent. žp.",
    whatEn: "baptized Vilhelma (Nov 6/10) — **the house cell = »sub dioe.« (under another diocese — no number; the 4th such entry of 1918 and the 1st GRIBLJE one — all 4 = Roma/refugee families!)** — father **Jožef Brajdič, a GYPSY** (the 2nd Brajdič of 1918 — cf. the r10 German ruling BRAJDIČ!), born Feb 13, 1875, mother **Marta née Malovšič? [~]** (Sep 26, 1876; m. Mar 10, 1910 in Štropice? [~]); **the 9th GRIBLJE row of 1918 (the last)!**; personal ID 2104191850345? [a reading doubt — ≠ the birth Nov 6]; marg [Anthoineta?] Jun 20, 1950 Nova gorica (MKU MO NG 1/1950, p. 945, ref. 1088) + May 14, 1952; godmother Marija Grabrijan? [~] from Čebrovc 31?; midwife — (a dash); signature Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "44",
    bookSignature: "04105",
    year: 1918,
    scan: 309,
    page: 261,
    whatSi: "krščena Terezija (10./11. 11.; rojstva dvom) — oče **Jožef Štucelj? [~]**, posednik, roj. 30.11.1882, mati **Barbara r. Tome** (18.10.1885; por. 27.2.1905); h44 = **9. VPIS** (1887–1914 → 1918; **VRZEL 3 LETI**); **9. GRIBLJE vrstica 1918!**; **EMŠO ×2: 0611918505155 (06.11 — ne skladno!) + 101191850503? (10.11 ✓) = 1. KOREKCIJSKI PAR (marg »Gradec, 10/11-1979«)!**; marg: zakonec Švagelj? Janez † 13.6.1979 Ljubljana (MKU Ljubljana 1.1979, str. 402, zap. 4379) + poročena 27.12.1946 + MKU MO 2.1985 str. 366, Metlika 12.3.1995 [~]; babica M. Zahorič? [~]; **podpis Jos. Lopar kapl.**",
    whatEn: "baptized Terezija (Nov 10/11; the birth a doubt) — father **Jožef Štucelj? [~]**, landowner, born Nov 30, 1882, mother **Barbara née Tome** (Oct 18, 1885; m. Feb 27, 1905); h44 = the **9th ENTRY** (1887–1914 → 1918; a **3-YEAR GAP**); **the 9th GRIBLJE row of 1918!**; **personal ID ×2: 0611918505155 (Nov 6 — inconsistent!) + 101191850503? (Nov 10 ✓) = the 1st CORRECTION PAIR (marg »Gradec, Nov 10/11-1979«)!**; marg: the spouse Švagelj? Janez died Jun 13, 1979 Ljubljana (MKU Ljubljana 1/1979, p. 402, ref. 4379) + married Dec 27, 1946 + MKU MO 2/1985 p. 366, Metlika Mar 12, 1995 [~]; midwife M. Zahorič? [~]; **signature Jos. Lopar kapl.**",
    status: "DOCUMENTED",
  },

  // ——— P114: krstna 1919 (04105, skeni 311–324 == str. 263–275; 79 vpisov = ZADNJE leto knjige;
  // 11 Griblje vrstic; NARE 10/11 + 1 NOVA hiša h81 — čisto leto se konča pri 4!; prilepeni dopis
  // ordinariata s325 (Jakob Košec 14.4.1917!) + bela listina = legitimizacijsko pismo Šponiček
  // (Fiume 1.8.1915) na s320/s321 dup-fotu; EMŠO ~34 žigov REKORD + l57 PRAZEN; 4 razveljavitve
  // REKORD; 5 duhovnikov REKORD; 19 VPIS PRENEŠEN REKORD; † 12 vključno l78 bombardiranje 1945
  // = ZADNJI VPIS; vitals 517→528; bloki 04105 491→502; kumulativ krstna linija 509 vpisov / 88 hiš / 34 let) ———
  {
    houseNo: "8",
    bookSignature: "04105",
    year: 1919,
    scan: 312,
    page: 264,
    whatSi: "krščena Ana (26./26. 3.; **EMŠO je: 2603919505488 → 26.3. ✓ SKLADNO — SIDRO**) — oče **Janez Jakofčič**, posednik, roj. 26.10.1889, mati **Ana r. Jakljevič** (2.5.1893); h8 = **7. VPIS — VRZEL 5 LET** (1914 → 1919); **1. GRIBLJE vrstica 1919 (P114 lead potrjen — glava »Anno 1919« ročna + tiskana)!**; pečat VPIS PRENEŠEN 7.11.2007 (Beljakovič) + marg »mož umrl 16.12.1971 v Gribljah (MKK Griblje 1.1971, str. 95, zap. 4)« + poročena 30.1.1939; botra Matija Štuvec? [~] + Katarina Totter? [~]; babica Marija Jakofčič; podpis Grgor Cerar župnik — 1. podpis župnika Cerarja v vzorcu!",
    whatEn: "baptized Ana (Mar 26/26; **personal ID 2603919505488 → Mar 26 ✓ CONSISTENT — an ANCHOR**) — father **Janez Jakofčič**, landowner, born Oct 26, 1889, mother **Ana née Jakljevič** (May 2, 1893); h8 = the **7th ENTRY — a 5-YEAR GAP** (1914 → 1919); **the 1st GRIBLJE row of 1919 (the P114 lead CONFIRMED — the »Anno 1919« hand header + print)!**; stamp VPIS PRENEŠEN Nov 7, 2007 (Beljakovič) + marg »the husband died Dec 16, 1971 in Griblje« + married Jan 30, 1939; godparents Matija Štuvec? [~] + Katarina Totter? [~]; midwife Marija Jakofčič; signature Grgor Cerar, the parish priest — his 1st signature in the sample!",
    status: "DOCUMENTED",
  },
  {
    houseNo: "47",
    bookSignature: "04105",
    year: 1919,
    scan: 313,
    page: 265,
    whatSi: "krščena Marija (6./6. 4.) — oče **Janez Šimec**, posednik, roj. 23.10.1886, mati **Barbara r. Hudorovac? [~ Hlobuar?]** (18.4.1887; por. 2/3 1908); h47 = **5. VPIS — VRZEL 6 LET** (1913 → 1919); **2. GRIBLJE vrstica 1919!**; pečat VPIS PRENEŠEN v OLR 26.08.2005 (Josipa Simonič) + marg »mož umrl 30.05.1986 Ljubljana (MKU 1986, str. 250, zap. 140)« + poročena 19.4.1952; botra Miko Filak? [~ Zilah?] + Marija Županič; babica Katarina Kapole? [~]; **DVOJNI PODPIS: Logar Jos. Kpol. + Grgor Cerar župnik (edini v vzorcu!)**",
    whatEn: "baptized Marija (Apr 6/6) — father **Janez Šimec**, landowner, born Oct 23, 1886, mother **Barbara née Hudorovac? [~]** (Apr 18, 1887; m. Mar 2, 1908); h47 = the **5th ENTRY — a 6-YEAR GAP** (1913 → 1919); **the 2nd GRIBLJE row of 1919!**; stamp VPIS PRENEŠEN Aug 26, 2005 + marg »the husband died May 30, 1986 Ljubljana« + married Apr 19, 1952; godparents Miko Filak? [~] + Marija Županič; midwife Katarina Kapole? [~]; **the DOUBLE SIGNATURE: Logar Jos. Kpol. + Grgor Cerar (the only one in the sample!)**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1919,
    scan: 315,
    page: 267,
    whatSi: "krščena Amalija (16./17. 5.; **EMŠO je: 1605919505381 → 16.5. ✓ SKLADNO**) — oče **Peter Brinc** (v vpisu »Briner«!), mali posednik, **roj. 28.9.1860 = najstarejši oče 1919 (59!)**, mati **Katarina r. Bohor** (18.10.1888); h88 = **6. VPIS** (1904–1917 → 1919); **3. GRIBLJE vrstica 1919!**; **NOVELA — marg »Priimek Brinec mi Brinc, ampak je pravilen Brinc« = uradna korekcija priimka (maticarka Šimonič Nina)!**; pečat VPIS PRENEŠEN 7.11.2007; botra Janez Brinc + Doroteja Brinc; babica Marija Jakofčič; podpis Cerar",
    whatEn: "baptized Amalija (May 16/17; **personal ID 1605919505381 → May 16 ✓ CONSISTENT**) — father **Peter Brinc** (written »Briner«!), a small landowner, **born Sep 28, 1860 = the oldest father of 1919 (59!)**, mother **Katarina née Bohor** (Oct 18, 1888); h88 = the **6th ENTRY** (1904–1917 → 1919); **the 3rd GRIBLJE row of 1919!**; **the NOVELA — marg »the surname Brinec mi Brinc, but the correct is Brinc« = the official surname correction (registrar Šimonič Nina)!**; stamp VPIS PRENEŠEN Nov 7, 2007; godparents Janez Brinc + Doroteja Brinc; midwife Marija Jakofčič; signature Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1919,
    scan: 315,
    page: 267,
    whatSi: "krščen Peter (28./29. 6.) — oče **Anton Brodarič**, posednik, roj. 14.4.1889? [~], mati **Katarina r. Milek? [~]** (9.2.1876? [~]); h46 = **12. VPIS — VRZEL 2 LETI** (1917 → 1919); **4. GRIBLJE vrstica 1919!**; marg † »+ 11/3? 1920« (dojenček); botra Miko Željko? [~] + Ana Perdivec; babica Marija Jakofčič; podpis Cerar; **labela »31« ×2 (ta + naslednja str. 268 = Cerkvišče 8 Anton) — edina številčenjska napaka vzorca 34 let!**",
    whatEn: "baptized Peter (Jun 28/29) — father **Anton Brodarič**, landowner, born Apr 14, 1889? [~], mother **Katarina née Milek? [~]** (Feb 9, 1876? [~]); h46 = the **12th ENTRY — a 2-YEAR GAP** (1917 → 1919); **the 4th GRIBLJE row of 1919!**; marg † »+ Mar 11? 1920« (an infant); godparents Miko Željko? [~] + Ana Perdivec; midwife Marija Jakofčič; signature Cerar; **the label »31« ×2 (this + the next p. 268 = Cerkvišče 8 Anton) — the only numbering error of the 34-year sample!**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "90",
    bookSignature: "04105",
    year: 1919,
    scan: 316,
    page: 268,
    whatSi: "krščena Stanislava (5./6. 7.) — oče **Šašteršič? [~]**, **UČITELJ** (1. učitelj-oče na Gribljih!), roj. 9.2.1883, mati **Marjeta r. Želef** (9.4.1889; por. 6/5 1913); h90 = **9. VPIS — VRZEL 5 LET** (1914 → 1919); **5. GRIBLJE vrstica 1919!**; marg »birman 17.5.1931« (poročni priimek — cf. l14 Birman!); botra Jožef Želef + Marija Jakofčič; babica Marija Jakofčič; podpis Cerar",
    whatEn: "baptized Stanislava (Jul 5/6) — father **Šašteršič? [~]**, a **TEACHER** (the 1st teacher-father on Griblje!), born Feb 9, 1883, mother **Marjeta née Želef** (Apr 9, 1889; m. May 6, 1913); h90 = the **9th ENTRY — a 5-YEAR GAP** (1914 → 1919); **the 5th GRIBLJE row of 1919!**; marg »birman May 17, 1931« (the married name — cf. l14 Birman!); godparents Jožef Želef + Marija Jakofčič; midwife Marija Jakofčič; signature Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "82",
    bookSignature: "04105",
    year: 1919,
    scan: 317,
    page: 269,
    whatSi: "krščen Peter (22./23. 8.) — oče **Peter Vreber? [~ Vecber?]**, **TESAR**, roj. 16.8.1882, mati **Terezija r. Mur? [~]** (4.10.1884; por. 7/3 1915); h82 = **2. VPIS — VRZEL 3 LETI** (1916 → 1919); **6. GRIBLJE vrstica 1919!**; marg † »+ 11.11.1934« (14 let!) + marg »se poročil 23.5.1943 s Elzo? Tominšek v Tuhinju« [~]; botra Ožbald Jakofčič + Terezija Jakofčič; babica Bara Galeir? [~ Adlešič?]; podpis Jos. Lopar/Logar Kpol.",
    whatEn: "baptized Peter (Aug 22/23) — father **Peter Vreber? [~]**, a **CARPENTER**, born Aug 16, 1882, mother **Terezija née Mur? [~]** (Oct 4, 1884; m. Mar 7, 1915); h82 = the **2nd ENTRY — a 3-YEAR GAP** (1916 → 1919); **the 6th GRIBLJE row of 1919!**; marg † »+ Nov 11, 1934« (aged 14!) + marg »married May 23, 1943 to Elza? Tominšek in Tuhinj« [~]; godparents Ožbald Jakofčič + Terezija Jakofčič; midwife Bara Galeir? [~]; signature Jos. Lopar/Logar Kpol.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04105",
    year: 1919,
    scan: 318,
    page: 270,
    whatSi: "krščena Vida (31. 8./1. 9.; **EMŠO je: 3108919505332? → 31.8. ✓ SKLADNO [~]**) — oče **Jurij Perdivec**, posednik, roj. 22.3.1873, mati **Katarina r. Hudovar? [~]** (18.10.1875; por. 17/6 1903); h48 = **8. VPIS — VRZEL 5 LET** (1914 → 1919); **7. GRIBLJE vrstica 1919!**; marg »Zakonska zveza razvezana ... v Beogradu št. J-1599/56 z dne 25.6.1954« + »se poročena 10.2.1948 s Bojančičem Svorodom? v Beogradu« + **»DRŽAVLJANKA Republike Slovenije« (UNŠ 1208-70/93, 29.01.1996 — Matičarka Šimonič Ana)!**; pečat VPIS PRENEŠEN 4.12.2007; botra Miko Brodarič + Bara Perdivec; babica Marija Jakofčič; podpis Cerar",
    whatEn: "baptized Vida (Aug 31/Sep 1; **personal ID 3108919505332? → Aug 31 ✓ CONSISTENT [~]**) — father **Jurij Perdivec**, landowner, born Mar 22, 1873, mother **Katarina née Hudovar? [~]** (Oct 18, 1875; m. Jun 17, 1903); h48 = the **8th ENTRY — a 5-YEAR GAP** (1914 → 1919); **the 7th GRIBLJE row of 1919!**; marg »the marriage dissolved ... in Belgrade no. J-1599/56 of Jun 25, 1954« + »married Feb 10, 1948 to Bojančič Svorod? in Belgrade« + **»A CITIZEN of the Republic of Slovenia« (UNŠ 1208-70/93, Jan 29, 1996 — registrar Šimonič Ana)!**; stamp VPIS PRENEŠEN Dec 4, 2007; godparents Miko Brodarič + Bara Perdivec; midwife Marija Jakofčič; signature Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1919,
    scan: 318,
    page: 270,
    whatSi: "krščen Julij (6./6. 9.) — oče **Matija Briner (= Brinc!)**, posednik, roj. 15.2.1883, mati **Marija r. Perdivec** (3.4.1877; por. 1905); h40 = **7. VPIS — VRZEL 4 LETI** (1915 → 1919); **8. GRIBLJE vrstica 1919!**; marg † »+ 6/3 1920« (dojenček); pečat 19.6.1982 Šimonič Nina; botra Janez Briner + Ana Briner (babica —); podpis Cerar; **BRINC/Briner mreža: h88 Amalija (l26) + h40 (l46) = 2 hiše iste familije (cf. marg »pravilen Brinc«)!**",
    whatEn: "baptized Julij (Sep 6/6) — father **Matija Briner (= Brinc!)**, landowner, born Feb 15, 1883, mother **Marija née Perdivec** (Apr 3, 1877; m. 1905); h40 = the **7th ENTRY — a 4-YEAR GAP** (1915 → 1919); **the 8th GRIBLJE row of 1919!**; marg † »+ Mar 6, 1920« (an infant); stamp Jun 19, 1982 Šimonič Nina; godparents Janez Briner + Ana Briner (midwife —); signature Cerar; **the BRINC/Briner network: h88 Amalija (l26) + h40 (l46) = 2 houses of the same family (cf. the marg »the correct Brinc«)!**",
    status: "DOCUMENTED",
  },
  {
    houseNo: "81",
    bookSignature: "04105",
    year: 1919,
    scan: 318,
    page: 270,
    whatSi: "krščena Karolina (9./10. 9.; **EMŠO je: 0909919505271 → 9.9. ✓ SKLADNO**) — oče **Janez Papič**, kolar, roj. 6.9.1889, mati **Katarina r. Herian** (2.2.1887; por. 30/1 1911); **h81 = NOVA HIŠA (1. vpis kadarkoli v registru 1886–1919 — edina nova 1919; NARE 10/11 — čisto leto se konča pri 4!)**; **9. GRIBLJE vrstica 1919!**; marg »mož umrl 03.04.1935 v Črnomlju« + »se poročila 18.4.1952 s Belim? Antonom v Ljubljani« + »umrla 27.02.2003 v Ljubljani na Zagrebu«; pečat VPIS PRENEŠEN 25.02.2003 (Jasna Simonič); botra Franc Dragoš + Barbara Logar vdova (babica —); podpis Cerar",
    whatEn: "baptized Karolina (Sep 9/10; **personal ID 0909919505271 → Sep 9 ✓ CONSISTENT**) — father **Janez Papič**, a wheelwright, born Sep 6, 1889, mother **Katarina née Herian** (Feb 2, 1887; m. Jan 30, 1911); **h81 = A NEW HOUSE (the 1st entry ever in the register 1886–1919 — the only new one of 1919; NARE 10/11 — the clean-year streak ends at 4!)**; **the 9th GRIBLJE row of 1919!**; marg »the husband died Apr 3, 1935 in Črnomelj« + »married Apr 18, 1952 to Beli? Anton in Ljubljana« + »died Feb 27, 2003 in Ljubljana-Zagreb«; stamp VPIS PRENEŠEN Feb 25, 2003 (Jasna Simonič); godparents Franc Dragoš + Barbara Logar the widow (midwife —); signature Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "6",
    bookSignature: "04105",
    year: 1919,
    scan: 323,
    page: 274,
    whatSi: "krščena Barbara (29./29. 11.) — oče **Jurij Jakofčič**, posednik, roj. 15.2.1879, mati **Katarina r. Jaklič** (14.2.1880; por. 6/2 1913); h6 = **8. VPIS — VRZEL 6 LET** (1913 → 1919); **10. GRIBLJE vrstica 1919!**; marg † »+ 28/4 1921« (dojenčica); botra Peter Perdivec + Barbara Perdivec; babica Marija Jakofčič; podpis Cerar",
    whatEn: "baptized Barbara (Nov 29/29) — father **Jurij Jakofčič**, landowner, born Feb 15, 1879, mother **Katarina née Jaklič** (Feb 14, 1880; m. Feb 6, 1913); h6 = the **8th ENTRY — a 6-YEAR GAP** (1913 → 1919); **the 10th GRIBLJE row of 1919!**; marg † »+ Apr 28, 1921« (an infant girl); godparents Peter Perdivec + Barbara Perdivec; midwife Marija Jakofčič; signature Cerar",
    status: "DOCUMENTED",
  },
  {
    houseNo: "5",
    bookSignature: "04105",
    year: 1919,
    scan: 324,
    page: 275,
    whatSi: "krščen Jožef (17.?/18. 12.; **EMŠO je: 191219500852 = 12-MESTNI (manjka števka!) → 19.12.? ≠ rojstva 17.? [DVOM — oboje]**) — oče **Matija Štuvec? [~ Štucec?]**, posednik, roj. 12.2.1873, mati **Marija r. Ureh? [~]** (14.8.1881; por. 1912?); h5 = **9. VPIS — VRZEL 2 LETI** (1917 → 1919); **11. GRIBLJE vrstica 1919 = ZADNJA GRIBLJSKA vrstica knjige 04105!**; pečat VPIS PRENEŠEN 06.02.2007 (Beljakovič) + marg »umrl(a) 11.08.1958 v Dončelah« [~]; botra Janez Dragoš + Neža Jakofčič; babica Marija Jakofčič; podpis Jos. Lopar/Logar Kpol.",
    whatEn: "baptized Jožef (Dec 17?/18; **the personal ID 191219500852 = 12-DIGIT (a digit missing!) → Dec 19? ≠ the birth 17? [a DOUBT — both]**); father **Matija Štuvec? [~]**, landowner, born Feb 12, 1873, mother **Marija née Ureh? [~]** (Aug 14, 1881; m. 1912?); h5 = the **9th ENTRY — a 2-YEAR GAP** (1917 → 1919); **the 11th GRIBLJE row of 1919 = the LAST GRIBLJE row of book 04105!**; stamp VPIS PRENEŠEN Feb 6, 2007 (Beljakovič) + marg »died Aug 11, 1958 in Dončele« [~]; godparents Janez Dragoš + Neža Jakofčič; midwife Marija Jakofčič; signature Jos. Lopar/Logar Kpol.",
    status: "DOCUMENTED",
  },
  // ——— P150 razširitev: POROČNA KNJIGA 04455 — polno leto 1921 (s182-dno
  // (№1–2) + s183–s187 == Pag. 180–185); 31 vpisov (№1–31) = 3. NAJVEČJE LETO
  // LINIJE (1919:40 → 1920:37 → 1921:31); 13 PON (41,9%) + 9 NED + 4 SRE +
  // 2 TOR + 3 PET + 0 SOB; vpisi z Griblji (9 poroke → 9 NOVIH BLOKOV!):
  // №4 h63×h70 INTRA · №8 h68×h36 INTRA · №10 h64 · №11 h64×h53 INTRA ·
  // №13 h59 · №20 h45×h92 INTRA (h92 NOVA!) · №22 h72×h44 INTRA (h72 NOVA!)
  // · №23 h10 · №27 h7 = 14 Griblje-števil; NOVELE: ★★★ 2 RAZVEZI-LISTINE (1. v
  // liniji! škof. ord. LJUBLJANA №16 št. 1442/21? + №18 št. 459/21!) +
  // ★★★ 1. HRVAŠKA (№28 Kaluka 41 (Hrv.) + potrdilo žup. Lipik/Lipnik!) +
  // ★★ 6 INTRA-HIŠE = REKORD (№6 Gradac 1 · №9 Krasinec 47 · №16 Grm 35 ·
  // №18 Krasinec 2 · №26 Gradac 78 · №31 Črnomelj 69!) + ★★ 4 POROKE ISTI
  // DAN 21.11. (№27–30) + ★★ ŽUPNIK-MENJAVA SREDI LETA (Cerar №1–24 → P.
  // Remigi JEREB №25–31, od 10.10.! — 1. opazovani prehod) + ★ POLETNA VRZEL
  // 113 DNI (19.6.→10.10. — najdaljša [~]) + BERKOVEC-TROJICA (№5/1921 + №5
  // + №6/1922 Lemelj 13, zadnja dva ISTI DAN!) + JAKOFČIČ ×5 v letu +
  // PERDIVEC ×8 omemb + MITENET ×3 + KURE ×6 + 5 MODRIH ANOTACIJ (†1976–81,
  // №8 + MATIČAR-PODPIS — 1.!) + 3 SAMOKOREKCIJE (№19-oče prečrtan · №20-
  // datum X→20. · №22-hišna 72) + 1. DATUM-NEOBSTOJI (№24 roj. 31. 6.!) +
  // NOVI POKLICI (sedlar · sodni sluga · pekar · orožniški tit. narednik ·
  // elektriciar? · revžarski pomočnik?) + 17-letna nevesta №31 + 52-letni
  // ženin №16 + 1. rojen-v-Metliki №20
  // Dokaz: research/issue17/parish-marriage-1921.json; verifikator:
  // scripts/p150_parish_marriage_1921.py --check (I1–I12).
  {
    houseNo: "63",
    bookSignature: "04455",
    year: 1921,
    scan: 183,
    page: 181,
    whatSi: "poroka (24. 1. 1921, vpis 4 — PONEDELJEK) — ženin Anton KRIŽAN, povstnika sin, 25 [r. 6. 3. 1895 ✓], GRIBLJE 63 (h63 = poročna 1911 №1 nevesta Catharina KRIŽAN prek 04105-filtra — 2. poročni dokaz h63; 1. v 04455!) × nevesta Marija GRABRIJAN, povstnika hiči, 20 (temno prepisano), r. 28. 2. 1900 ✓, GRIBLJE 70 (★ 1. korpusni dokaz h70-v-04455; h70 že v vzorci prek 04105); ★★★ INTRA-GRIBLJE h63 × h70; starši: Miko Križan × Katarina roj. PERDIVEC + †Marko Grabrijan × Marija roj. PERDIVEC = INTRA-STARŠI ×2 (obe mati roj. Perdivec — sestri? [~])!; priči Jure Grabrijan + Janez Papič? [~] kolar; KRIŽAN ×160-mreža (cf. P149 №27!)",
    whatEn: "marriage (Jan 24, 1921, entry 4 — MONDAY) — groom Anton KRIŽAN, a smallholder's son, 25 [b. Mar 6, 1895 ✓], GRIBLJE 63 (h63 = the 1911 №1 bride Catharina KRIŽAN via the 04105 filter — the 2nd marriage evidence of h63; the 1st in 04455!) × bride Marija GRABRIJAN, a smallholder's daughter, 20 (rewritten darker), b. Feb 28, 1900 ✓, GRIBLJE 70 (★ the 1st corpus evidence of h70 in 04455; h70 already in the sample via 04105); ★★★ an INTRA-GRIBLJE marriage h63 × h70; parents: Miko Križan × Katarina née PERDIVEC + †Marko Grabrijan × Marija née PERDIVEC = INTRA-PARENTS ×2 (both mothers born Perdivec — sisters? [~])!; witnesses Jure Grabrijan + Janez Papič? [~] a wheelwright; the KRIŽAN ×160 network (cf. P149 №27!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "68",
    bookSignature: "04455",
    year: 1921,
    scan: 183,
    page: 181,
    whatSi: "poroka (31. 1. 1921, vpis 8 — PONEDELJEK) — ženin Miko MITEK, povstnika sin, 23 [r. 29. 2. 1897 ✓ — 1. 29.-februarski rojstni datum linije?! [~]], GRIBLJE 68 (★ NOVA-dokaz: P149-lead '18' → ZOOM 68!; h68 = poročna 1914 №3/№4 — 2. poročni dokaz) × nevesta Katarina KRŽAN [~ Kružan], povstnika hiči, 23, r. 20. 9. 1898 ✓, GRIBLJE 36 (h36 = poročna 1920 №34!); ★★★ INTRA-GRIBLJE h68 × h36 + MITENET (cf. №12-mati + №20-nevesta!); margin MODRA ANOTACIJA 1979 + MATIČAR-PODPIS (1. v liniji!): 'Zakonca Mitek Katarina hiči umrla 26.5.1979 v Gribljah (mrk. l. 1979, str. 12, zop. 3), Gradac 4.6.1979 — matičar Šimec Šuso? [~]'",
    whatEn: "marriage (Jan 31, 1921, entry 8 — MONDAY) — groom Miko MITEK, a smallholder's son, 23 [b. Feb 29, 1897 ✓ — the 1st Feb-29 birth date of the line?! [~]], GRIBLJE 68 (★ NEW evidence: the P149 lead read '18' → the ZOOM shows 68!; h68 = the 1914 №3/№4 marriage — the 2nd marriage evidence) × bride Katarina KRŽAN [~ Kružan], a smallholder's daughter, 23, b. Sep 20, 1898 ✓, GRIBLJE 36 (h36 = the 1920 №34 marriage!); ★★★ an INTRA-GRIBLJE marriage h68 × h36 + the MITENET (cf. №12-mother + №20-bride!); a blue 1979 margin ANNOTATION + a REGISTRAR SIGNATURE (the 1st of the line!): 'the spouse Mitek Katarina died May 26, 1979 in Griblje (reg. 1979, p. 12, no. 3), Gradac Jun 4, 1979 — registrar Šimec Šuso? [~]'",
    status: "DOCUMENTED",
  },
  {
    houseNo: "64",
    bookSignature: "04455",
    year: 1921,
    scan: 184,
    page: 182,
    whatSi: "poroka (10. 4. 1921, vpis 10 — NEDELJA) — ženin Anton HARASINIČ, povstnik, '46 let' [r. 30. 5. 1875/1876-dvom — H10: račun 45/44!], ČERKVIŠČE 25 (lead-korekcija '33'→25!) × nevesta Marija JAKOFČIČ, povstnika hiči, 32, r. 27. 3. 1889 ✓, GRIBLJE 64 (h64 = poročna 1886 №12 Požek! 2. poročni dokaz); ★★★ BRAT+SESTRA ISTI DAN (№10-bride + №11-groom = sorojenci Janez Jakofčič × Marija Štabjar!) + JAKOFČIČ-NET (×149-mreža!); starši: †Miko Harasinič × Marija roj. PERDIVEC; priči Miko Kambič gostilničar + Peter Harasinič; 20-letna razlika",
    whatEn: "marriage (Apr 10, 1921, entry 10 — SUNDAY) — groom Anton HARASINIČ, a smallholder, '46 years' [b. May 30, 1875/1876-doubt — H10: the arithmetic gives 45/44!], ČERKVIŠČE 25 (the lead correction '33'→25!) × bride Marija JAKOFČIČ, a smallholder's daughter, 32, b. Mar 27, 1889 ✓, GRIBLJE 64 (h64 = the 1886 №12 Požek marriage! the 2nd marriage evidence); ★★★ A BROTHER+SISTER WED THE SAME DAY (№10-bride + №11-groom = the children of Janez Jakofčič × Marija Štabjar!) + the JAKOFČIČ network (the ×149 web!); parents: †Miko Harasinič × Marija née PERDIVEC; witnesses Miko Kambič an innkeeper + Peter Harasinič; a 20-year age gap",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04455",
    year: 1921,
    scan: 184,
    page: 182,
    whatSi: "poroka (10. 4. 1921, vpis 11 — NEDELJA) — ženin Matija JAKOFČIČ, povstnika sin ✓, 24 [r. 7. 7. 1896 ✓], GRIBLJE 64 (h64 = 2. dokaz ISTI DAN kot №10! — brat №10-neveste!) × nevesta Margareta DRAGOS roj. PERDIVEC (VDOVA [~]), povstnica, 29, r. 17. 8. 1891 ✓, GRIBLJE 53 (★ BLOK h53 — h53 = poročna 1890 v6 Perdinec! 2. poročni dokaz; P80_PT_GAP-hiša!); ★★★ INTRA-GRIBLJE h64 × h53 + PERDIVEC-mreža (nevesta roj. Perdivec + №10-mati roj. Perdivec + №11-tasta roj. Križan!); priči Peter Perdivec + Matija Jakofčič",
    whatEn: "marriage (Apr 10, 1921, entry 11 — SUNDAY) — groom Matija JAKOFČIČ, a smallholder's son ✓, 24 [b. Jul 7, 1896 ✓], GRIBLJE 64 (h64 = the 2nd evidence THE SAME DAY as №10! — the brother of the №10 bride!) × bride Margareta DRAGOS née PERDIVEC (a WIDOW [~]), a smallholder, 29, b. Aug 17, 1891 ✓, GRIBLJE 53 (★ the h53 BLOCK — h53 = the 1890 v6 Perdinec marriage! the 2nd marriage evidence; an P80_PT_GAP house!); ★★★ an INTRA-GRIBLJE marriage h64 × h53 + the PERDIVEC web (the bride born Perdivec + the №10 mother born Perdivec + the №11 grandmother born Križan!); witnesses Peter Perdivec + Matija Jakofčič",
    status: "DOCUMENTED",
  },
  {
    houseNo: "59",
    bookSignature: "04455",
    year: 1921,
    scan: 184,
    page: 182,
    whatSi: "poroka (13. 4. 1921, vpis 13 — SREDA) — ženin Michael JAKOFČIČ, povstnik ✓, 35 [r. 27. 3. 1885 ✓], ČERKVIŠČE 9 × nevesta Ana JAKLIČ roj. KAMBIČ (VDOVA!), povstnica, 40 (5 let STAREJŠA!), r. 2. 5. 1880 ✓, GRIBLJE 59 (★ BLOK h59 — h59 = P80_PT_GAP-hiša (poročna 1897-era); 1. poročni dokaz h59 v 04455!); ★★★ JAKOFČIČ 3. v 4 dneh (№10 + №11 + №13!) + VDOWA + tasta nem. BRUNER [~]; priči Peter Jakofčič + Janez Jaklič; 3. poroka 13. 4.",
    whatEn: "marriage (Apr 13, 1921, entry 13 — WEDNESDAY) — groom Michael JAKOFČIČ, a smallholder ✓, 35 [b. Mar 27, 1885 ✓], ČERKVIŠČE 9 × bride Ana JAKLIČ née KAMBIČ (a WIDOW!), a smallholder, 40 (5 years OLDER!), b. May 2, 1880 ✓, GRIBLJE 59 (★ the h59 BLOCK — an P80_PT_GAP house (the 1897-era marriage); the 1st marriage evidence of h59 in 04455!); ★★★ the 3rd JAKOFČIČ in 4 days (№10 + №11 + №13!) + a WIDOW + the German BRUNER grandmother [~]; witnesses Peter Jakofčič + Janez Jaklič; the 2nd wedding of Apr 13",
    status: "DOCUMENTED",
  },
  {
    houseNo: "92",
    bookSignature: "04455",
    year: 1921,
    scan: 185,
    page: 183,
    whatSi: "poroka (20. 5. 1921, vpis 20 — PETEK; datum-korekcija: prečrtano + X + »20.«!) — ženin Janez ŠTABGAR? [~ Štubgar], revžarski pomočnik? [~], 29 [račun 30-dvom], r. 24. 6. 1891 V METLIKI (1. rojen-izven-vas ženin!), GRIBLJE 45 × nevesta Marija MITEK, hiči povstnika, 25 [~26-dvom], r. 24. 7. 1895 ✓, GRIBLJE 92 (★★★ NOVA HIŠA — 1. korpusni dokaz h92 = 1. poročni dokaz NAJVIŠJE številke — nov maksimum po h87/P148!); ★★★ INTRA-GRIBLJE h45 × h92 + MITENET (№8-ženin Mitek h68 + №12-mati roj. Mitek!) + SAMOKOREKCIJA-datuma; priči Franc Rajmer? čevljar + Franc Vrana? sluga",
    whatEn: "marriage (May 20, 1921, entry 20 — FRIDAY; a date correction: struck out + an X + »20.«!) — groom Janez ŠTABGAR? [~ Štubgar], a 'revžar' assistant? [~], 29 [the arithmetic says 30 — a doubt], b. Jun 24, 1891 IN METLIKA (the 1st groom born outside the parish villages!), GRIBLJE 45 × bride Marija MITEK, a smallholder's daughter, 25 [~26-doubt], b. Jul 24, 1895 ✓, GRIBLJE 92 (★★★ A NEW HOUSE — the 1st corpus evidence of h92 = the 1st marriage evidence of the HIGHEST number — a new maximum after h87/P148!); ★★★ an INTRA-GRIBLJE marriage h45 × h92 + the MITENET (№8-groom Mitek h68 + №12-mother born Mitek!) + a date self-correction; witnesses Franc Rajmer? a shoemaker + Franc Vrana? a servant",
    status: "DOCUMENTED",
  },
  {
    houseNo: "72",
    bookSignature: "04455",
    year: 1921,
    scan: 186,
    page: 184,
    whatSi: "poroka (6. 6. 1921, vpis 22 — PONEDELJEK) — ženin Michael ŠTRAVS, sin povstnika ✓, 25 [r. 13. 9. 1895 ✓], GRIBLJE 72 (★★★ NOVA HIŠA — 1. korpusni dokaz h72!; številka 72-dopisana/popravljena — SAMOKOREKCIJA [~]; P149-lead '4a' → 72!) × nevesta Ana TOMC, hiči povstnika, 21, r. 30. 8. 1899 ✓ (+ opomba 'šlejfa'? [~]), GRIBLJE 44; ★★★ INTRA-GRIBLJE h72 × h44 + ŠTRAVS-net (1887-h71-Straus → 1921-h72-Štravs!) + JAKOFČIČ-mati (†Marija roj. Jakofčič — 5. pojav v letu!); oče-neveste Janez Tomc vihtar [rihtar ~] (cf. №12!); priči Miko Kure + Janez Klepec",
    whatEn: "marriage (Jun 6, 1921, entry 22 — MONDAY) — groom Michael ŠTRAVS, a smallholder's son ✓, 25 [b. Sep 13, 1895 ✓], GRIBLJE 72 (★★★ A NEW HOUSE — the 1st corpus evidence of h72!; the number 72-added/corrected — a SELF-CORRECTION [~]; the P149 lead read '4a' → 72!) × bride Ana TOMC, a smallholder's daughter, 21, b. Aug 30, 1899 ✓ (+ a note 'šlejfa'? [~]), GRIBLJE 44; ★★★ an INTRA-GRIBLJE marriage h72 × h44 + the ŠTRAVS web (1887-h71-Straus → 1921-h72-Štravs!) + a JAKOFČIČ mother (†Marija née Jakofčič — the 5th appearance of the year!); the bride's father Janez Tomc a vihtar [rihtar ~] (cf. №12!); witnesses Miko Kure + Janez Klepec",
    status: "DOCUMENTED",
  },
  {
    houseNo: "10",
    bookSignature: "04455",
    year: 1921,
    scan: 186,
    page: 184,
    whatSi: "poroka (6. 6. 1921, vpis 23 — PONEDELJEK) — ženin Miko BRINEC, sin povstnika, 25 [r. 8. 9. 1895 ✓], GRIBLJE 10 (h10 = poročna-era znana hiša — poročni dokaz 1921!) × nevesta Bara KLEPEC, hiči povstnika, 21, r. 19. 10. 1899 ✓, Krasinec 34; starši: Janez Brinec × Ana roj. KURE + Jurij Klepec × Marija roj. Tomc; priči Janez Kure + Anton Marenta?; KURE-mreža (cf. №16/№24/№25!); 3. poroka 6. 6. (№21–23 = ponedeljkov trojček!)",
    whatEn: "marriage (Jun 6, 1921, entry 23 — MONDAY) — groom Miko BRINEC, a smallholder's son, 25 [b. Sep 8, 1895 ✓], GRIBLJE 10 (h10 = a known house of the marriage era — the 1921 marriage evidence!) × bride Bara KLEPEC, a smallholder's daughter, 21, b. Oct 19, 1899 ✓, Krasinec 34; parents: Janez Brinec × Ana née KURE + Jurij Klepec × Marija née Tomc; witnesses Janez Kure + Anton Marenta?; the KURE web (cf. №16/№24/№25!); the 3rd wedding of Jun 6 (№21–23 = a Monday trio!)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "7",
    bookSignature: "04455",
    year: 1921,
    scan: 187,
    page: 185,
    whatSi: "poroka (21. 11. 1921, vpis 27 — PONEDELJEK) — ženin Jurij JAKLIČ, pavestniška sin ✓, 24 [r. 24. 4. 1897 ✓], BORŠT 47 (izven-župnijski — župn. Boršt!) × nevesta Marija FOTTER, pavest. hiči, 20 (NEDOLETNA!), r. 27. 7. 1901 ✓, GRIBLJE 7 (★ BLOK h7 — NAJNIŽJA Griblje-št. 1921; h7 že v vzorci prek 04105 — poročni dokaz 1921!; FOTTER = NOV PRIIMEK!); dokument: PISMENO DOVOLJENJE OČETA NEDOLETNE NEVESTE; priči Matija Štrucelj? + Miko Tasič? (rim. kat.); ★★★ 1. od 4 POROK 21. 11. + MODRA ANOTACIJA † 6. 11. 1977: 'Zakonec Jaklič Jurij umrl dne 6. 11. 77 v Gribljah (l. 1977, str. 107, zop. št. 5), Gradac 5. 12. [77/79?]' + 'matičar Šimec Šuso? [~]' (2. matičar-podpis!)",
    whatEn: "marriage (Nov 21, 1921, entry 27 — MONDAY) — groom Jurij JAKLIČ, a smallholder's son ✓, 24 [b. Apr 24, 1897 ✓], BORŠT 47 (out-of-parish — the parish of Boršt!) × bride Marija FOTTER, a smallholder's daughter, 20 (a MINOR!), b. Jul 27, 1901 ✓, GRIBLJE 7 (★ the h7 BLOCK — the LOWEST Griblje number of 1921; h7 already in the sample via 04105 — the 1921 marriage evidence!; FOTTER = a NEW SURNAME!); document: a WRITTEN CONSENT of the father of the underage bride; witnesses Matija Štrucelj? + Miko Tasič? (Roman Catholic); ★★★ the 1st of 4 WEDDINGS Nov 21 + a blue ANNOTATION † Nov 6, 1977: 'the husband Jaklič Jurij died Nov 6, 77 in Griblje (1977, p. 107, no. 5), Gradac Dec 5' + 'registrar Šimec Šuso? [~]' (the 2nd registrar signature!)",
    status: "DOCUMENTED",
  },
  // ——— P151: poročna knjiga 04455, leto 1922 = ZAKLJUČEK KNJIGE (s188–s190 ==
  // Pag. 186–188, 9.–11. potrditev Pag==sken−2!) — 37. leto poročne linije
  // (P115 = 1886 → … → P151 = 1922 = KONEC; naslovnica 'P 1873–1922'!). 13
  // vpisov (11 oštevilčenih №1–11 + 2 NEŠTEVILČENA = 3.+4. v liniji!) =
  // ★★★ SIBLING-SWAP #2 (№4+№5 — isti dan + isti priči + zamenjava
  // sorojencev Berkovec↔Brodarič!) + ★★★ 1. FRANCISKAN/'per delegationem'
  // duhovnik (P. Edvard Raustelar O.F.M. Brežje — Mala Paka-Hrvaška!) +
  // ★★★ 16 NOVIH PRIIMKOV = REKORD + ★★ 2. HRVAŠKA-referenca (Mala Paka 19,
  // župn. Lipnik-Hrv.!) + ★★ ZADNJI VPIS 27.8.1922 (№11) + ★★ 2 VDOVI +
  // 16-LETNICA ×2 (3.+4.!) + MLADOLETNOST-VAL (≥6/13!) + 5-LISTIN №8 +
  // NAJSTAREJŠI ŽENIN 67 LET (№10 Jurij Jakofčič-SENIOR — H: 1866/67!) +
  // INTRA-GRIBLJE h23×h68 (Brinec × Milek/Mlak-M-zmeda!) + SEGINA ×2 +
  // TESAR ×2 + BRODARIČ ×3 + ŽUPANIČ ×3 + BERKOVEC-TROJICA zaključena +
  // 5 NEZNANIH VAS [~] (Fučkovič · Jsenic · Šibrje · Čerhovice · Hrbiška
  // gora!) + P151-lead KOREKCIJE ×16
  // Dokaz: research/issue17/parish-marriage-1922.json; verifikator:
  // scripts/p151_parish_marriage_1922.py --check (I1–I12).
  {
    houseNo: "17",
    bookSignature: "04455",
    year: 1922,
    scan: 188,
    page: 186,
    whatSi: "poroka (23. 1. 1922, vpis 1 — PONEDELJEK) — ženin Jurij KRALJ, povestnik-tesar ✓ (svinčniški ✓!), 36 [r. 10. 7. 1885 ✓ — lead-faza-1 '10.2.1895' → ZOOM 1885, aritmetika ✓!], GRIBLJE 17 (★ 3. poročni dokaz h17 — 1892-№10 Johann Kralj 48 [1.] + 1909-№1 Maria Kralj 27 [2.] → 1922 Jurij [3.]; korpus-aritmetika: Johann-r.~1844 → sin-Jurij-r.1885 ✓!) × nevesta Ana SEGINA, povest. hči, starost NEZAPISANA (r. 22. 9. 1897 → 24), FUČKOVIČ 11. [~ NEZNANA VAS!]; ★ SEGINA ×2 v letu (cf. №11-ženin Janez Segina — 2 familije!) + TESAR ×2 (cf. №11 tesarski pomočnik!); starši: Janez Kralj vrtnar? [~ 'vrtlhar'] × Ana roj. Jakobovič? [~] + Daniel Segina povest. × Barbora roj. Frensič? [~]; priči Miko Filak? [~ 'Fiškar'] + Julij Belčič? tesar? [~]; duhovnik R. Remigi Jereb",
    whatEn: "marriage (Jan 23, 1922, entry 1 — MONDAY) — groom Jurij KRALJ, a smallholder-carpenter ✓ (a pencil check!), 36 [b. Jul 10, 1885 ✓ — the lead-faza-1 'Feb 10, 1895' → the ZOOM 1885, the arithmetic ✓!], GRIBLJE 17 (★ the 3rd marriage evidence of h17 — the 1892-№10 Johann Kralj 48 [1st] + the 1909-№1 Maria Kralj 27 [2nd] → 1922 Jurij [3rd]; the corpus-arithmetic: Johann-b.~1844 → the son-Jurij-b.1885 ✓!) × bride Ana SEGINA, a smallholder's daughter, the age NOT WRITTEN (b. Sep 22, 1897 → 24), FUČKOVIČ 11. [~ an UNKNOWN VILLAGE!]; ★ SEGINA ×2 in the year (cf. the №11 groom Janez Segina — 2 families!) + TESAR ×2 (cf. №11 the carpenter's assistant!); parents: Janez Kralj a gardener? [~] × Ana née Jakobovič? [~] + Daniel Segina × Barbora née Frensič? [~]; witnesses Miko Filak? [~] + Julij Belčič? a carpenter? [~]; priest R. Remigi Jereb",
    status: "DOCUMENTED",
  },
  {
    houseNo: "23",
    bookSignature: "04455",
    year: 1922,
    scan: 188,
    page: 186,
    whatSi: "poroka (6. 2. 1922, vpis 2 — PONEDELJEK) — ženin Marko BRINE, povest. sin ✓, 28 [r. 24. 4. 1893 ✓ — faza-1 '23 let' → ZOOM 28, aritmetika ✓!], GRIBLJE 23 (★ 3. poročni dokaz h23 = BRINEC-družina: 1887-v4 Maria [1.] + 1888-v2 Mathias [2.] → 1922 Marko [3.] — Marko = sin Mathiasa-1888-ženina? [~ aritmetika ✓]) × nevesta Loroteja? [~] MILEK, povest. hči, 20, r. 11. 10. 1901 ✓ (P150-lead '16-letna' → NEPRAVILNO — 20-letna!), GRIBLJE 68 (★ lead '69' → ZOOM 68!; 4. poročni dokaz h68: 1914-№3/№4-MLAKOVA + 1921-№8-Mitek → 1922 [4.] — M-5-družinska zmeda Milek/Mlak nadaljevana!); ★★★ INTRA-GRIBLJE h23 × h68!; starši: Matija Brine povestnik × Marija roj. Lehlič? [~ 'Zeblič'] + Matija Milek povest. × Katarina roj. POŽEK (cf. h21-Požek 1889!); priči Miko POŽEK povest. (nevestina-mati-priimek!) + Tomaž Lehlič? povest.; listine ×2: spričevalo sorodstva škof. ord. Ljubljana št. 428/22 + ženitčno dovoljenje okraj. sodišča Črnomelj št. 5877/21 (mladoletna-nevesta-vzorec!); duhovnik R. Remigi Jereb",
    whatEn: "marriage (Feb 6, 1922, entry 2 — MONDAY) — groom Marko BRINE, a smallholder's son ✓, 28 [b. Apr 24, 1893 ✓ — the faza-1 '23 years' → the ZOOM 28, the arithmetic ✓!], GRIBLJE 23 (★ the 3rd marriage evidence of h23 = the BRINEC family: the 1887-v4 Maria [1st] + the 1888-v2 Mathias [2nd] → 1922 Marko [3rd] — Marko = the son of Mathias the 1888 groom? [~ the arithmetic ✓]) × bride Loroteja? [~] MILEK, a smallholder's daughter, 20, b. Oct 11, 1901 ✓ (the P150-lead '16-year-old' → WRONG — she is 20!), GRIBLJE 68 (★ the lead '69' → the ZOOM 68!; the 4th marriage evidence of h68: the 1914-№3/№4-MLAKOVA + the 1921-№8-Mitek → 1922 [4th] — the M-5-family confusion Milek/Mlak continues!); ★★★ an INTRA-GRIBLJE marriage h23 × h68!; parents: Matija Brine × Marija née Lehlič? [~] + Matija Milek × Katarina née POŽEK (cf. the h21-Požek 1889!); witnesses Miko POŽEK (the bride's-mother-surname!) + Tomaž Lehlič?; documents ×2: the kinship certificate of the diocesan ordinariate Ljubljana no. 428/22 + the marital permission of the district court Črnomelj no. 5877/21 (the underage-bride pattern!); priest R. Remigi Jereb",
    status: "DOCUMENTED",
  },
  {
    houseNo: "48",
    bookSignature: "04455",
    year: 1922,
    scan: 189,
    page: 187,
    whatSi: "poroka (22. 5. 1922, vpis 8 — PONEDELJEK) — ženin Janez ŠUŠTARIČ (NOV PRIIMEK — REKORD-LETNA valova 16 novih!), povestnik, 31 [r. 20. 12. 1890 ✓], PRILOZJE 31 (lead '3' → ZOOM 31!) × nevesta Ana PEZDIRC, povest. hči, 16 (16-LETNICA #4 linije!), r. 27. 8. 1905 ✓ [~ 25.8.], GRIBLJE 48 (★ 2. poročni dokaz h48 po P148-№20!; PEZDIRC-mreža ×152!); starši: Jurij Šuštarič povestnik × Ana roj. JAKOFČIČ (mreža ×151!) + Jurij PEZDIRC povestnik × Katarina roj. Pezdirc? [~ — INTRA-STARŠI!]; priči Miko BERKOVEC povestnik (cf. №4+№5-Berkovec-TROJICA!) + Matija Šuštarič; ★★ 5 LISTIN (2. najbolj dokumentiran vpis linije po №12/1919!): spričevalo [sorodstva?] škof. ord. št. 494 · dekan. urad Šuhor? [~] št. 109 · okraj. glavar Trnovec? [~] št. 5238 · policijska uprava št. 18338 · PISMENO DOVOLJENJE OČETA MLADOLETNE NEVESTE; duhovnik R. Remigi Jereb",
    whatEn: "marriage (May 22, 1922, entry 8 — MONDAY) — groom Janez ŠUŠTARIČ (a NEW SURNAME — the record-year wave of 16 new ones!), a smallholder, 31 [b. Dec 20, 1890 ✓], PRILOZJE 31 (the lead '3' → the ZOOM 31!) × bride Ana PEZDIRC, a smallholder's daughter, 16 (the 16-year-old #4 of the line!), b. Aug 27, 1905 ✓ [~ Aug 25], GRIBLJE 48 (★ the 2nd marriage evidence of h48 after the P148-№20!; the PEZDIRC network ×152!); parents: Jurij Šuštarič × Ana née JAKOFČIČ (the network ×151!) + Jurij PEZDIRC × Katarina née Pezdirc? [~ — INTRA-PARENTS!]; witnesses Miko BERKOVEC (cf. the №4+№5 Berkovec-TRIO!) + Matija Šuštarič; ★★ 5 DOCUMENTS (the 2nd best-documented entry of the line after №12/1919!): the [kinship?] certificate of the diocesan ordinariate no. 494 · the deanery office Šuhor? [~] no. 109 · the district captain Trnovec? [~] no. 5238 · the police directorate no. 18338 · a WRITTEN CONSENT of the father of the underage bride; priest R. Remigi Jereb",
    status: "DOCUMENTED",
  },
];