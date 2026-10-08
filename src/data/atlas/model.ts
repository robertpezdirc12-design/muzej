// ATLAS 1825 — lastniki (navzkrižno preverjeni med PT in PUA) + georeferenca + model

export interface AtlasOwner {
  id: string;
  /** prepis iz vira (Kurrent, REVIEW) */
  nameAsWritten: string;
  /** sodobna približna različica */
  modernGuess?: string;
  /** hiše iz PT (parc. sklici) */
  houseRefs: string[];
  /** potrditev iz PUA (abecedni seznam) */
  puaRef?: string;
  status: "REVIEW" | "DOCUMENTED";
}

export const ATLAS_OWNERS: AtlasOwner[] = [
  { id: "lastnik-bring-weygandt", nameAsWritten: "Bring. Weygandt Bauern von Grüblen [PT rokopis: Brinig — Magnus/Malfa/Miklo ~]", modernGuess: "Bring/Brinig", houseRefs: ["24", "31", "32", "35", "37", "38", "40"], puaRef: "PUA str. 4, črka B; issue #17: PUA str. 4 vrstica 3 = Bring Michael/Migan Bauern hiesig, Haus 24 [~] — navzkrižna potrditev hiše 24; P3: renumeracija str. 4 (36→35, 38→37, 39→38, 41→40 — hiša 41 ne obstaja); PT brania Brinig Magnus/Malfa/Miklo [~]", status: "REVIEW" },
  { id: "lastnik-bring-math", nameAsWritten: "Bring. Math. Bauern von Grüblen", modernGuess: "Bring", houseRefs: ["25"], puaRef: "PUA str. 4, črka B; issue #17: PUA str. 4 vrstica 4 = Bring Miß/Martin Bauern hiesig, Haus 25 [~] — navzkrižna potrditev", status: "REVIEW" },
  { id: "lastnik-veith", nameAsWritten: "Veith (H., St.?) [~]", modernGuess: "Veith", houseRefs: ["1", "2"], puaRef: "P3 paleografija: hiša 1 = Veith (H.) [~] 3× (prej Peth) — navzkrižje s PUA str. 3 (Dragosche [~], glej lastnik-adlolschitz)", status: "REVIEW" },
  { id: "lastnik-simec", nameAsWritten: "Schimek / Šimec", modernGuess: "Šimec", houseRefs: ["3", "4", "63", "64", "66"], status: "REVIEW" },
  { id: "lastnik-lebing", nameAsWritten: "Lebing/Lebring Mädl. [~]", modernGuess: "Lebing?", houseRefs: ["7", "8"], puaRef: "P3 paleografija (2 kroga): L-priimek + Mädl. konvergirata — prej brano Leskovec Matija (hiša 8) in Lebring/Leudig Martin (hiša 7)", status: "REVIEW" },
  { id: "lastnik-bödig", nameAsWritten: "Bödig mündl. [~]", modernGuess: "Bödig?", houseRefs: ["7½", "8½"], puaRef: "P3 paleografija (2 kroga): 2× Bödig mündl. — prej brano Podlesy Marija (7½) / Leskovec Matija (8½)", status: "REVIEW" },
  { id: "lastnik-hrovat", nameAsWritten: "Hrovat Jhan", modernGuess: "Hrvat", houseRefs: ["18", "15"], status: "REVIEW" },
  { id: "lastnik-krisan", nameAsWritten: "Krišan Gregor", houseRefs: ["29", "30"], status: "REVIEW" },
  { id: "lastnik-milleg", nameAsWritten: "Milleg Hans (Jan) [~]", modernGuess: "Milleg", houseRefs: ["34", "36"], puaRef: "P3: renumeracija (37→36); stara 35 = prečrtana dvojnica 34 (Milleg) — Jan = Hans, ista oseba; prej [34, 35, 37]", status: "REVIEW" },
  { id: "lastnik-glan", nameAsWritten: "Glan (Georg, Matthäus, Simonz)", houseRefs: ["—"], puaRef: "PUA str. 4–5", status: "REVIEW" },
  { id: "lastnik-greg", nameAsWritten: "Greg/Grög (Michael, Ulrich)", houseRefs: ["—"], status: "REVIEW" },
  { id: "lastnik-filak", nameAsWritten: "Filak (Peter, Mihel)", houseRefs: ["69", "70", "71"], puaRef: "PUA str. 9–10, črka F — Fillah (Michael, Maria, Jetter, Miho) v hišah 16/34/36/61 [~]: ista družina, hišne št. divergentne s PT [~]", status: "REVIEW" },
  { id: "lastnik-dikobutar", nameAsWritten: "Dikobutar (Rupre, Mihelo, Mihlo, Marko)", houseRefs: ["68", "72", "77", "78", "80"], status: "REVIEW" },
  { id: "lastnik-peutinger", nameAsWritten: "Peutinger (Jhan, Mihel)", houseRefs: ["61", "65", "73"], status: "REVIEW" },
  { id: "lastnik-drulak", nameAsWritten: "Drulak (Jhan, Peter)", houseRefs: ["74", "75"], status: "REVIEW" },
  { id: "lastnik-stenopfs", nameAsWritten: "Strauß Georg [~]", modernGuess: "Strauß", houseRefs: ["76", "79"], puaRef: "P3 paleografija: 2× Strauß Georg (prej Stenopfs); hiša 79 vrstica rdeče prečrtana (možen duplikat 76)", status: "REVIEW" },
  { id: "lastnik-groy", nameAsWritten: "Strauß Georg [Groy] [~]", modernGuess: "Strauß/Groy", houseRefs: ["81", "82", "83", "84", "92"], puaRef: "P3 paleografija: 2× Strauß + ime Georg (ne Hanž); Groy kot drugi zapis v rokopisu; Feidig (92) v 2. krogu ni ponovno bran — ostaja [~]", status: "REVIEW" },
  { id: "lastnik-ihmeyer", nameAsWritten: "Ihmeyer (Manko, Georg?) [~]", modernGuess: "Ihmeyer?", houseRefs: ["96"], puaRef: "P3 paleografija: 2× Ihmeyer (prej Groy Khunz na hiši 96); hiša 90: tri divergentna brania — glej lastnik-kuncelj", status: "REVIEW" },
  { id: "lastnik-heurisch", nameAsWritten: "Heurisch Marko", houseRefs: ["87", "89", "91"], status: "REVIEW" },
  { id: "lastnik-kuncelj", nameAsWritten: "hiša 90: brania divergirajo [?]", houseRefs: ["90"], puaRef: "P3: 1. krog Kavalar/Bumiller Marlo [~], 2. krog Ihmeyer Georg [~] — priimek Kuncelj se ne potrdi; vrstica ostaja ILLEGIBLE (stari očrt v houses.ts kot opomba)", status: "REVIEW" },
  { id: "lastnik-schmerz", nameAsWritten: "Schmerz Marko", houseRefs: ["95", "97"], status: "REVIEW" },
  { id: "lastnik-adlolschitz", nameAsWritten: "Adlolschitz, Wulff Ludwig (von)", houseRefs: ["1"], puaRef: "PUA str. 3, črka A — Dragosche", status: "REVIEW" },
  { id: "lastnik-ludvig", nameAsWritten: "Ludvig Gregor", houseRefs: ["23"], status: "REVIEW" },
  { id: "lastnik-zollnerd", nameAsWritten: "k.k. Zollamt (ärarial) [~] — institucija", houseRefs: ["98"], puaRef: "P3: 2× institucionalno branje (A. A. Zollamt + ärarial + »Hauptmagazin von 1826«) — carinska postaja/skladišče, ne priimek Zollnerd", status: "REVIEW" },
  { id: "lastnik-stettner", nameAsWritten: "Stettner [~] (prečrtana vrstica 71½)", houseRefs: ["71½"], puaRef: "P3: prečrtana polovična vrstica na str. 6 — dokumentirana, neštet priimni vnos", status: "REVIEW" },
  { id: "lastnik-hufschmied", nameAsWritten: "Hufschmied [~] (rdeči vpis, prečrtana 76½)", houseRefs: ["76½"], puaRef: "P3: beseda Hufschmied (podkovar) v rdečem čnilu na prečrtani vrstici — poklic ali priimek, neštet vnos", status: "REVIEW" },
];

// ——— GEOREFERENCA (GEOTRUTH, issue #14, 2026-10-08) ——————————————————
// Listi A01/A02 so zasidrani na uradni EŠD 2122 (Register nepremične kulturne
// dediščine, GisKD): cerkev sv. Vida na listu A02 (px 1995,577) ↔ uradni poligon
// 45,567610 N 15,290311 E. Struga Kolpe na listu (desni krak, VLM x 2765–2890)
// se pod to afino ujema s sodobno strugo 6–30 m — pod staro (krožno) afino je
// odstopala 80–130 m. Vsi izpeljani podatki so bili translirani za
// −0,005190 lat / −0,001889 lng (≈ −147 m E / +578 m J).

export interface SheetGeoref {
  id: string;
  sheet: string;
  imageUrl: string;
  /** [severni, zahodni], [južni, vzhodni] — GEOTRUTH (EŠD 2122) afina */
  bounds: [[number, number], [number, number]];
  pixels: { width: number; height: number };
  scaleMPerPixel: number;
  status: "CORROBORATED" | "RECONSTRUCTED" | "REVIEW";
  methodSi: string;
  methodEn: string;
  controlPoints: { fromSi: string; a01x?: number; a01y?: number; modernLat: number; modernLng: number; noteSi?: string }[];
  accuracySi: string;
  accuracyEn: string;
}

export const SHEET_GEOREFS: SheetGeoref[] = [
  {
    id: "georef-a01",
    sheet: "A01",
    imageUrl: "/atlas/n83-a01.jpg",
    bounds: [
      [45.58361, 15.26031],
      [45.56141, 15.29971],
    ],
    pixels: { width: 2826, height: 2273 },
    scaleMPerPixel: 1.09,
    status: "RECONSTRUCTED",
    methodSi:
      "GEOTRUTH afina (issue #14): staro sidro A01 »jedro vasi« (px 2091,1773) se po popravku izkaže za cerkev+ pokopališče (34 m od EŠD 2122), »severna skupina« (px 2063,1477) pa za severni rob vasi 1825. Translacija lista: −0,005190 lat / −0,001889 lng. Struga Kolpa ostaja neodvisen vir E–Z kontrole (OSM ploščice).",
    methodEn:
      "GEOTRUTH affine (issue #14): the old A01 anchor »village core« (px 2091,1773) re-identifies, after the correction, as the church + churchyard (34 m from EŠD 2122); the »northern cluster« (px 2063,1477) is the north end of the 1825 village. Sheet translation: −0.005190 lat / −0.001889 lng. The Kolpa channel remains an independent E–W control (OSM tiles).",
    controlPoints: [
      { fromSi: "cerkev sv. Vida / »jedro« (A01 px 2091, 1773)", a01x: 2091, a01y: 1773, modernLat: 45.56761, modernLng: 15.290311, noteSi: "EŠD 2122 (uradni vir) — prej razlagano kot jedro vasi, krožna georeferenca" },
      { fromSi: "severna skupina hiš (A01 px 2063, 1477)", a01x: 2063, a01y: 1477, modernLat: 45.57022, modernLng: 15.290913, noteSi: "severni rob vasi 1825 po GEOTRUTH afini" },
      { fromSi: "reka Kolpa pri vasi (A01 px 2580, 1773)", a01x: 2580, a01y: 1773, modernLat: 45.56761, modernLng: 15.2994, noteSi: "izsledek struge iz OSM ploščic (neodvisen vir E–Z)" },
    ],
    accuracySi:
      "Ocena natančnosti ±60–100 m na območju vasi (struga potrjena 6–30 m, translacija ena za oba lista). Kotni odmik lokalne katastrske projekcije ni odstranjen (ocena ≤ 2,5°).",
    accuracyEn:
      "Estimated accuracy ±60–100 m over the village area (the river channel confirmed at 6–30 m, one shared translation for both sheets). The angular offset of the local cadastral projection was not removed (estimated ≤ 2.5°).",
  },
  {
    id: "georef-a02",
    sheet: "A02",
    imageUrl: "/atlas/n83-a02.jpg",
    bounds: [
      [45.571808, 15.26979],
      [45.556118, 15.300746],
    ],
    pixels: { width: 3010, height: 2158 },
    scaleMPerPixel: 0.79,
    status: "CORROBORATED",
    methodSi:
      "GEOTRUTH afina (issue #14): cerkev sv. Vida na listu (px 1995,577 — apsida, križ, pokopališki obrobl) ↔ uradni poligon EŠD 2122 (45,567610 N 15,290311 E, GisKD MK_EVRD/3602, STANJE_POD 07-10-2026); stavba OSM 284847361 znotraj poligona (≤ 8 m). Struga Kolpe na listu (desni krak, VLM x 2765–2890 pri y 100–1400) se s sodobno strugo ujeme 6–30 m. Stara afina je bila KROŽNA — cerkev je bila lastna kontrolna točka s predpostavljeno koordinato 45,5728/15,2922.",
    methodEn:
      "GEOTRUTH affine (issue #14): St. Vitus' church on the sheet (px 1995,577 — apse, cross, churchyard) ↔ the official EŠD 2122 polygon (45.567610 N 15.290311 E, GisKD MK_EVRD/3602, status 07-10-2026); the OSM building 284847361 lies inside the polygon (≤ 8 m). The Kolpa channel on the sheet (right branch, VLM x 2765–2890 at y 100–1400) matches the modern channel at 6–30 m. The old affine was CIRCULAR — the church was its own control point with an assumed coordinate 45.5728/15.2922.",
    controlPoints: [
      { fromSi: "cerkev sv. Vida (A02 px 1995, 577)", a01x: 1995, a01y: 577, modernLat: 45.56761, modernLng: 15.290311, noteSi: "EŠD 2122 — uradni register (GisKD) + OSM way 284847361 + pokopališče 284847363" },
      { fromSi: "reka Kolpa ob cerkvi (A02 px 2695, 577 — desni krak x≈2827)", a01x: 2695, a01y: 577, modernLat: 45.56761, modernLng: 15.29866, noteSi: "sodobna struga pri latitudi cerkve (OSM); na listu narisana pri x≈2827, ujemanje 6–30 m" },
    ],
    accuracySi:
      "Ocena natančnosti ±40–80 m na območju vasi. Skala lista ~0,79 m/px. Prisotnost OSM stavb (15 obstoječih od 156 po novi shemi) dodatno podpira afino.",
    accuracyEn:
      "Estimated accuracy ±40–80 m over the village area. Sheet scale ~0.79 m/px. The OSM building presence (15 of 156 matching under the new scheme) further supports the affine.",
  },
  {
    id: "georef-a03",
    sheet: "A03",
    imageUrl: "/atlas/n83-a03.jpg",
    bounds: [
      [45.5575, 15.2485],
      [45.5437, 15.273],
    ],
    pixels: { width: 2645, height: 2154 },
    scaleMPerPixel: 0.72,
    status: "REVIEW",
    methodSi:
      "P10 (2026-10-08): arhivska oznaka v okvirju lista »O.IX24dg« (Kurrent, nepomaknjeno VLM branje iz P9) = SEKCIJA katastrske mreže eZKN (GURS): celica VKIX24dg z URADNO geometrijo (45,5437–45,5575 N, 15,2485–15,2730 E; D96/TM). List ≈ celica + robovi (princip potrjen na A02: središče vsebine A02 = središče celice VKIX24cf NATANČNO). Risana vsebina A03 = le vzhodni pas (x 83–100 %) = zahodni rob k.o. Griblje ob meji s k.o. Tribuče/Bedenj — ostalo lista je prazno (ozemlje sosednjih k.o., narisano na njihovih listih). VALIDACIJE: razpršeni napis E-H-C-S-T-U-B-I-R-T = TRIBUTSCH (68 %, 35 %) pade v k.o. Tribuče ✓; WEIDENDORF (71 %, 86 %) pade v k.o. Bedenj ✓ (Bedenj = Weidendorf, Wikipedija); napis »Borli«/»Berli« ≈ istoimensko območje na ZKN »GRIBLJE 4« (eZKN) ✓. P5-b hiše na pasu ≈ kmetije zahodnega roba (porabe: 1825→2026 se vzorec spremeni).",
    methodEn:
      "P10 (2026-10-08): the archive code in the sheet frame »O.IX24dg« (Kurrent, unprompted VLM read from P9) = the SECTION of the eZKN cadastral grid (GURS): cell VKIX24dg with OFFICIAL geometry (45.5437–45.5575 N, 15.2485–15.2730 E; D96/TM). Sheet ≈ cell + margins (the principle validated on A02: the centre of A02's content = the centre of cell VKIX24cf EXACTLY). The drawn content of A03 = only the eastern strip (x 83–100 %) = the western edge of c.m. Griblje along the Tribuče/Bedenj border — the rest of the sheet is blank (the neighbours' territory, drawn on their own sheets). VALIDATIONS: the scattered letters E-H-C-S-T-U-B-I-R-T = TRIBUTSCH (68 %, 35 %) falls inside c.m. Tribuče ✓; WEIDENDORF (71 %, 86 %) falls inside c.m. Bedenj ✓ (Bedenj = Weidendorf, Wikipedia); the label »Borli«/»Berli« ≈ the same-named area on the ZKN sheet »GRIBLJE 4« (eZKN) ✓.",
    controlPoints: [
      { fromSi: "celica VKIX24dg (eZKN/GURS, uradna geometrija mreže 1:2880)", a01x: 1322, a01y: 1077, modernLat: 45.5506, modernLng: 15.2608, noteSi: "središče celice ≈ središče lista; k.o. Griblje zaseda le vzhodni pas (15,269–15,273)" },
      { fromSi: "razpršeni napis TRIBUTSCH (A03 px ≈ 68 %, 35 %)", a01x: 1799, a01y: 754, modernLat: 45.5527, modernLng: 15.2652, noteSi: "ime k.o. Tribuče, pisano po njenem ozemlju — pod celico pade v k.o. Tribuče ✓" },
      { fromSi: "napis WEIDENDORF (A03 px ≈ 71 %, 86 %)", a01x: 1878, a01y: 1852, modernLat: 45.5456, modernLng: 15.2659, noteSi: "ime k.o. Bedenj (Weidendorf) — pade v k.o. Bedenj ✓" },
    ],
    accuracySi:
      "Ocena ±200–400 m (preslikava list↔celica po principu iz A02; stavbna validacija šibka — 200 let sprememb). K.o. Griblje na listu = le vzhodni pas; zahodni del lista = ozemlje k.o. Tribuče in Bedenj (prazno). Merilo ~0,72 m/px (isti papirni format 1:2880 kot A02).",
    accuracyEn:
      "Estimated ±200–400 m (the sheet↔cell mapping by the principle validated on A02; the building validation is weak — 200 years of change). C.m. Griblje on the sheet = the eastern strip only; the western part of the sheet = the territory of c.m. Tribuče and Bedenj (blank). Scale ~0.72 m/px (the same 1:2880 paper format as A02).",
  },
  {
    id: "georef-a04",
    sheet: "A04",
    imageUrl: "/atlas/n83-a04.jpg",
    bounds: [
      [45.5574, 15.2728],
      [45.5436, 15.2973],
    ],
    pixels: { width: 2645, height: 2158 },
    scaleMPerPixel: 0.72,
    status: "REVIEW",
    methodSi:
      "P10 POPRAVEK (2026-10-08): arhivska oznaka v okvirju lista »O.IX24cg« (trikratno VLM branje: P9 nepomaknjeno + 2× ciljno) = SEKCIJA eZKN mreže: celica VKIX24cg (45,5436–45,5574 N, 15,2728–15,2973 E) — območje DIREKTNO JUŽNO od A02/celice cf, NE ovin Kolpe pri Adlešiči! P9-georeferenca (rot +30,9°, s 0,55, ovin 45,522–45,538) je bila ZAVRŽENA: (1) stavbna validacija — 222 zaznanih simbolov A04 na P9-legi ima mediano odmik 636 m od sodobnih stavb (celica cg: 72 m) — P9 lega statistično izključena; (2) P9 »neodvisne« kontrole (ADLESCHITZ v k.o. Adlešiči, WEIDENDORF ob k.o. Bedenj) so NEDISKRIMINATIVNE — obe območji ležita v istih k.o.; (3) P9 sled »reke« (10 točk, širina 180 px ≈ 130 m pri 0,72) je najverjetneje dolina/cesta, ne Kolpa (Kolpa je ~1,2 km vzhodno od vzhodnega roba celice cg, IZVEN lista); P9 prileganje oblike ovinka = zavedljiv lokalni optimum proste podobnostne preslikave. SEDAJ: list A04 = celica cg + robovi (sever-gor, kot A02 — razmerje stranic lista 1,23 ≈ celice 1,25 ✓); vsebina = južni del k.o. Griblje + meje s.k. Tribuče (Z), Bedenj (JZ), Adlešiči (V). VALIDACIJE: WEIDENDORF (spodaj levo) = k.o. Bedenj ✓; ADLESCHITZ (desno) = k.o. Adlešiči ✓; razporeditev se ujema z ZKN listom »GRIBLJE 4« (eZKN, isto območje: Tribuče sredina-levo, Bednji spodaj-levo) ✓; Bresnik (1032,1532) → (45,5476; 15,2824) ≈ območje Brinskega sela [~].",
    methodEn:
      "P10 CORRECTION (2026-10-08): the archive code in the sheet frame »O.IX24cg« (three VLM reads: P9 unprompted + 2 targeted) = the eZKN grid SECTION: cell VKIX24cg (45.5436–45.5574 N, 15.2728–15.2973 E) — the area DIRECTLY SOUTH of A02/cell cf, NOT the Kolpa bend by Adlešiči! The P9 georeference (rot +30.9°, s 0.55, the bend at 45.522–45.538) was RETRACTED: (1) building validation — 222 detected A04 symbols at the P9 position have a median offset of 636 m from modern buildings (cell cg: 72 m) — the P9 position is statistically excluded; (2) P9's »independent« checks (ADLESCHITZ inside c.m. Adlešiči, WEIDENDORF at c.m. Bedenj) are NON-DISCRIMINATING — both candidate areas lie in the same c.m.s; (3) P9's »river« trace (10 points, width 180 px ≈ 130 m at 0.72) is most likely a valley/road, not the Kolpa (the Kolpa lies ~1.2 km east of cell cg's eastern edge, OUTSIDE the sheet); P9's bend-shape fit = a seductive local optimum of the free similarity transform. NOW: sheet A04 = cell cg + margins (north-up, like A02 — the sheet aspect 1.23 ≈ the cell's 1.25 ✓); the content = the southern part of c.m. Griblje + the borders with c.m. Tribuče (W), Bedenj (SW), Adlešiči (E). VALIDATIONS: WEIDENDORF (bottom left) = c.m. Bedenj ✓; ADLESCHITZ (right) = c.m. Adlešiči ✓; the layout matches the ZKN sheet »GRIBLJE 4« (eZKN, the same area: Tribuče middle-left, Bednji bottom-left) ✓.",
    controlPoints: [
      { fromSi: "celica VKIX24cg (eZKN/GURS, uradna geometrija mreže 1:2880)", a01x: 1322, a01y: 1079, modernLat: 45.5505, modernLng: 15.2851, noteSi: "središče celice = središče lista (princip A02↔cf)" },
      { fromSi: "napis WEIDENDORF = Bedenj (A04 px ≈ 608,1964 → spodaj levo)", a01x: 608, a01y: 1964, modernLat: 45.5457, modernLng: 15.2784, noteSi: "k.o. Bedenj (Weidendorf) — jugozahodni sosed celice ✓" },
      { fromSi: "napis ADLESCHITZ (A04 px ≈ 2116,1403 → desno)", a01x: 2116, a01y: 1403, modernLat: 45.5485, modernLng: 15.2924, noteSi: "k.o. Adlešiči — vzhodni sosed celice ✓" },
    ],
    accuracySi:
      "Ocena ±200–400 m (preslikava list↔celica; dvoumnost robov lista). Popravek P9: prejšnja objavljena lega (ovin Kolpe, ±100 m vzdolž reke) je NAPAČNA za ~2,5 km — razlogi dokumentirani v methodSi. Kolpa NI na listu A04 (teče ~120 m vzhodno od vzhodnega roba celice cg).",
    accuracyEn:
      "Estimated ±200–400 m (the sheet↔cell mapping; the sheet-margin ambiguity). P9 correction: the previously published position (the Kolpa bend, ±100 m along the river) is WRONG by ~2.5 km — the reasons documented in methodSi. The Kolpa is NOT on sheet A04 (it flows ~120 m east of cell cg's eastern edge).",
  },
  {
    id: "georef-a05",
    sheet: "A05",
    imageUrl: "/atlas/n83-a05.jpg",
    bounds: [
      [45.5437, 15.2726],
      [45.5299, 15.2971],
    ],
    pixels: { width: 2634, height: 2165 },
    scaleMPerPixel: 0.73,
    status: "REVIEW",
    methodSi:
      "P10 (2026-10-08): arhivska oznaka v okvirju lista »O.IX24ch« (nepomaknjeno VLM branje iz P9) = SEKCIJA eZKN mreže: celica VKIX24ch (45,5299–45,5437 N, 15,2726–15,2971 E) — skrajni JUG 1825 k.o. Griblje (današnja k.o. Adlešiči; ozemlje je bilo pozneje odvzeto k.o. Griblje!). Risana vsebina = sklop ~45 stavb s hišnimi št. v ZGORNJI DESNI polovici (75 %, 28 %) → (45,5398; 15,291) = območje Fučkovcev/severnega roba Dragošev [~]; ostalo lista = prazno (k.o. Adlešiči). VALIDACIJE: razpršene črke A-D-L-E-S-C + [Vedalschitz ~] = k.o. Adlešiči ✓ (ime pisano po njenem ozemlju); vrstno ime »Pri Jankovichti« (65 %, 21 %) → (45,5408; 15,2885) = današnje naselje Jankoviči ✓ (45,523–45,545; 15,273–15,293); »Na Prago Poljé«, »Štize Vardianove«, »N°8 Na Svetoschki Schloß« = Flurnamen istega območja; neodvisen multivalentni fit sklopa (A05 px → sodobne stavbne parcele GURS) je izbral Fučkovce kot najboljšega kandidata med 6-imi (score 0,914, vendar nediskriminativen — nič-test 0,84).",
    methodEn:
      "P10 (2026-10-08): the archive code in the sheet frame »O.IX24ch« (unprompted VLM read from P9) = the eZKN grid SECTION: cell VKIX24ch (45.5299–45.5437 N, 15.2726–15.2971 E) — the far SOUTH of the 1825 c.m. Griblje (today's c.m. Adlešiči; the territory was later detached from c.m. Griblje!). The drawn content = a cluster of ~45 buildings with house numbers in the UPPER RIGHT half (75 %, 28 %) → (45.5398; 15.291) = the Fučkovci / north-Dragoši area [~]; the rest of the sheet is blank (c.m. Adlešiči). VALIDATIONS: the scattered letters A-D-L-E-S-C + [Vedalschitz ~] = c.m. Adlešiči ✓ (the name written across its own territory); the field name »Pri Jankovichti« (65 %, 21 %) → (45.5408; 15.2885) = today's settlement of Jankoviči ✓ (45.523–45.545; 15.273–15.293); »Na Prago Poljé«, »Štize Vardianove«, »N°8 Na Svetoschki Schloß« = field names of the same area; an independent multi-candidate fit of the cluster (A05 px → modern GURS building parcels) selected Fučkovci as the best of 6 candidates (score 0.914, but non-discriminating — the null test 0.84).",
    controlPoints: [
      { fromSi: "celica VKIX24ch (eZKN/GURS, uradna geometrija mreže 1:2880)", a01x: 1317, a01y: 1082, modernLat: 45.5368, modernLng: 15.2849, noteSi: "središče celice = središče lista; k.o. Griblje zaseda le zgornjo desno polovico" },
      { fromSi: "sklop ~45 stavb s hišnimi št. (A05 px ≈ 75 %, 28 %)", a01x: 1975, a01y: 606, modernLat: 45.5398, modernLng: 15.291, noteSi: "Fučkovci / severni rob Dragošev [~] — k.o. Griblje 1825 sega do sem!" },
      { fromSi: "vrstno ime »Pri Jankovichti« (A05 px ≈ 65 %, 21 %)", a01x: 1712, a01y: 455, modernLat: 45.5408, modernLng: 15.2885, noteSi: "današnje naselje Jankoviči ✓" },
    ],
    accuracySi:
      "Ocena ±200–400 m. List pokriva skrajni jug 1825 k.o. Griblje (45,530–45,5437) — ozemlje, ki ga današnja k.o. Griblje (do 45,5442) NE vsebuje več: meji k.o. sta se pozneje premaknili. Hišne št. na listu (npr. N°8) so številke znotraj tedanje k.o. Griblje.",
    accuracyEn:
      "Estimated ±200–400 m. The sheet covers the far south of the 1825 c.m. Griblje (45.530–45.5437) — territory that today's c.m. Griblje (down to 45.5442) no longer contains: the c.m. boundaries were later redrawn. The house numbers on the sheet (e.g. N°8) are numbers within the then c.m. Griblje.",
  },
];

// ——— LOKACIJSKE entitete (LOCATION sloj) ——————————

export interface AtlasLocation {
  id: string;
  kind: "vas" | "cerkev" | "reka" | "pot" | "meja";
  titleSi: string;
  titleEn: string;
  lat?: number;
  lng?: number;
  status: "VERIFIED" | "DOCUMENTED" | "APPROXIMATE";
  sourceId: string;
  museumRef?: string;
  noteSi?: string;
}

export const ATLAS_LOCATIONS: AtlasLocation[] = [
  {
    id: "loc-griblje",
    kind: "vas",
    titleSi: "Griblje (Grüble) — jedro vasi ~1825",
    titleEn: "Griblje (Grüble) — village core ~1825",
    lat: 45.57092,
    lng: 15.29435,
    status: "VERIFIED",
    sourceId: "src-a02",
    museumRef: "MVG-001",
    noteSi: "Razpotegnjeno jedro z dvema sklopoma hiš na listu A02 (GEOTRUTH afina, issue #14); 156 vektoriziranih objektov (status RECONSTRUCTED). Današnje jedro (OSM place node 45,5725/15,2926) je ~370 m severno — vas je zrasla proti severu.",
  },
  {
    id: "loc-cerkev",
    kind: "cerkev",
    titleSi: "Cerkev sv. Vida (St. Veith) ~1825",
    titleEn: "St. Vitus church (St. Veith) ~1825",
    lat: 45.56761,
    lng: 15.290311,
    status: "VERIFIED",
    sourceId: "src-a02",
    museumRef: "MVG-002",
    noteSi: "Stavba z apsido, križem in pokopališkim obroblom na listu A02 (px 1995,577). EŠD 2122: »na pokopališču, na gričku južno od vasi«. Uradni vir (GisKD) + OSM (way 284847361) — koordinata VERIFIED (issue #14, konflikt 595 m razrešen). Pripravljena za 3D/AR (GLB model MVG-002, realno merilo 13 m).",
  },
  {
    id: "loc-kolpa",
    kind: "reka",
    titleSi: "Reka Kolpa — vzhodna meja občine ~1825",
    titleEn: "The Kolpa river — eastern municipality boundary ~1825",
    status: "VERIFIED",
    sourceId: "src-a01",
    noteSi: "Na obeh listih označena kot meja proti CROATIEN / KÖNIGREICH CROATIEN; struga se v glavnem ujema s sodobno.",
  },
  {
    id: "loc-meja",
    kind: "meja",
    titleSi: "Meja katastrske občine (k.o. št. 83)",
    titleEn: "Boundary of the cadastral municipality (c.m. no. 83)",
    status: "DOCUMENTED",
    sourceId: "src-pr",
    noteSi: "Grenz-Beschreibung der Gemeinde „GRÜBLE“ — opis meje v N083PR (4 strani, Kurrent, še ni prebran v celoti).",
  },
];

// ——— Stavbe — vektorizacija iz lista A02 (RECONSTRUCTED) ————

export interface VectorBuilding {
  lat: number;
  lng: number;
  w: number;
  h: number;
  px: [number, number];
}

import buildingsJson from "./buildings.json";
export const VECTOR_BUILDINGS = buildingsJson as VectorBuilding[];
