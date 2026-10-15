// ATLAS 1825 — arhivski viri in registri
// Recovery: stari atlas podatkovni model (atlas-map-data-model-1825, knowledge-graph-1825,
// story-graph-1825, georef-1825, parcel-register-1825, cadastre-a01) v NOBENEM od
// recovery virov (bundle, arhivski repozitoriji, diski, Vercel deploymenti) ni bil najden.
// Nadomeščeno z DEJANSKIMI javnimi arhivskimi viri: Arhiv Republike Slovenije,
// fond SI AS 176 (Franciscejski kataster za Kranjsko), katastrska občina Griblje (N83).
// Fizični viri preverjeni 2026-10-07 prek VAČ (Virtualna arhivska čitalnica).

export type SourceType =
  | "cadastral-map"
  | "sketch"
  | "boundary-description"
  | "parcel-register"
  | "building-protocol"
  | "owner-register"
  | "land-use"
  | "valuation"
  | "heritage-register"
  | "archival-mention";

/** strojno berljiv status prenosa digitalne kopije (issue #3 #11) */
export type TransferStatus =
  | "TRANSFERRED" /** digitalna kopija v repozitoriju */
  | "TO_COLLECT" /** enota je digitalizirana, kopija še ni prenesena */
  | "NOT_DIGITIZED" /** enota obstaja, a ni digitalizirana */
  | "NOT_APPLICABLE";

/** strojno berljiv status georeference (issue #3 #11; issue #4: ločitev natančnosti)
 *  GEOREFERENCED = georeferenca z znano negotovostjo; od P50 ločuje kalibro prek
 *                  placement.precision (VALIDATED_GEOREF = točkovna sidra,
 *                  NEATLINE_* = afina na uradne kote celic eZKN);
 *  GRID_APPROX   = okvirna umestitev po sekcijski mreži 1:2880 (eZKN) — NI validirana
 *                  georeferenca (brez točkovnega sidra; ±200–400 m). */
export type GeorefStatus =
  | "GEOREFERENCED"
  | "GRID_APPROX"
  | "TO_COLLECT"
  | "NOT_APPLICABLE";

/** Prostorska umestitev grafičnega lista (issue #4) — ločuje dokazano stanje od
 *  približka. Podatek izhaja iz SHEET_GEOREFS (model.ts): A01/A02 imata afino
 *  s kontrolnimi točkami; A03–A05 imajo od P50 P46 neatline afine (meje = narisana
 *  neatline = uradna meja celice eZKN 1:2880; A03 = 2/4 strani detektirane). */
export interface SpatialPlacement {
  precision: "VALIDATED_GEOREF" | "GRID_APPROX" | "NEATLINE_GEOREFERENCED" | "NEATLINE_PARTIAL_GEOREFERENCED";
  methodSi: string;
  methodEn: string;
  /** št. kontrolnih točk / preveritev, ki podpirajo umestitev */
  controlPoints: number;
  accuracySi: string;
  accuracyEn: string;
  /** datum zadnje preveritve (YYYY-MM-DD) */
  lastChecked: string;
}

/** strojno berljivi statusi raziskave vsakega zgodovinskega podatka (issue #3 #13) */
export type ResearchStatus =
  | "VERIFIED"
  | "DOCUMENTED"
  | "REVIEW"
  | "RECONSTRUCTED"
  | "INFERRED"
  | "TO_COLLECT"
  | "NOT_FOUND"
  | "NOT_PUBLIC";

export interface AtlasSource {
  id: string;
  code: string;
  type: SourceType;
  titleSi: string;
  titleEn: string;
  /** oddaja v okviru N83 */
  unit?: string;
  vacId?: string;
  vacUrl?: string;
  /** datoteka v javni digitalni knjižnici (seja) */
  fileRef?: string;
  pages?: number;
  yearFrom?: number;
  yearTo?: number;
  fund: string;
  archive: string;
  licenceSi: string;
  licenceEn: string;
  thumb?: string;
  /** ali je list georeferenciran (validirana afina — issue #4 loči od okvirne umestitve) */
  georeferenced?: boolean;
  /** strojno berljiva statusa (issue #3) */
  transferStatus?: TransferStatus;
  georefStatus?: GeorefStatus;
  /** prostorska umestitev z natančnostjo (issue #4) */
  placement?: SpatialPlacement;
  /** koliko vsebinskih zapisov enote je strukturiranih v Atlasu */
  structuredEntries?: number;
  /** datum zadnje preveritve vira (YYYY-MM-DD) */
  lastVerified?: string;
  noteSi?: string;
  noteEn?: string;
}

export const ATLAS_SOURCES: AtlasSource[] = [
  {
    id: "src-a01",
    code: "N083A01",
    type: "cadastral-map",
    titleSi: "Katastrski list A01 — občina Grüble",
    titleEn: "Cadastral sheet A01 — municipality of Grüble",
    unit: "list A01",
    vacId: "227666",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227666",
    fileRef: "IIIF: /vac/iiif/raster/f919e72f-862b-3300-a8e8-4b20d7fed9e9",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/a01-thumb.jpg",
    georeferenced: true,
    transferStatus: "TRANSFERRED",
    georefStatus: "GEOREFERENCED",
    placement: {
      precision: "VALIDATED_GEOREF",
      methodSi: "GEOTRUTH afina (issue #14): sidri »jedro vasi« (cerkev+ pokopališče, 34 m od EŠD 2122) in severna skupina hiš; struga Kolpe kot neodvisna E–Z kontrola.",
      methodEn: "GEOTRUTH affine (issue #14): the anchors »village core« (church + churchyard, 34 m from EŠD 2122) and the northern house cluster; the Kolpa channel as an independent E–W control.",
      controlPoints: 3,
      accuracySi: "±60–100 m na območju vasi (struga potrjena 6–30 m)",
      accuracyEn: "±60–100 m over the village area (the channel confirmed at 6–30 m)",
      lastChecked: "2026-10-08",
    },
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "Grafični list katastrske občine Griblje (Grüble). Reka Kolpa kot vzhodna meja, naselbina v jugovzhodnem delu. Sken 2826 × 2273 px. Digitalna kopija prenesena iz VAČ IIIF; meje parcel še niso vektorsko izrisane (TO_COLLECT).",
    noteEn:
      "Graphical sheet of the Griblje (Grüble) cadastral municipality. The Kolpa river as eastern boundary, settlement in the south-east. Scan 2826 × 2273 px. Digital copy transferred from VAČ IIIF; parcel boundaries not yet vectorised (TO_COLLECT).",
  },
  {
    id: "src-a02",
    code: "N083A02",
    type: "cadastral-map",
    titleSi: "Katastrski list A02 — občina Grüble, vas s cerkvijo sv. Vidom",
    titleEn: "Cadastral sheet A02 — Grüble with St. Vitus church",
    unit: "list A02",
    vacId: "227668",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227668",
    fileRef: "IIIF: /vac/iiif/raster/fb69b6eb-c538-3249-8f1e-28d804f3d698",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/a02-thumb.jpg",
    georeferenced: true,
    transferStatus: "TRANSFERRED",
    georefStatus: "GEOREFERENCED",
    placement: {
      precision: "VALIDATED_GEOREF",
      methodSi: "GEOTRUTH afina (issue #14), CORROBORATED: cerkev sv. Vida na listu ↔ uradni poligon EŠD 2122 (GisKD) + stavba OSM 284847361 (≤ 8 m); struga Kolpe se ujema 6–30 m. Iz tega lista je vektoriziranih 156 stavbnih tlorisov — izvor 3D vasi.",
      methodEn: "GEOTRUTH affine (issue #14), CORROBORATED: St. Vitus' church on the sheet ↔ the official EŠD 2122 polygon (GisKD) + OSM building 284847361 (≤ 8 m); the Kolpa channel matches at 6–30 m. The 156 building footprints were vectorised from THIS sheet — the origin of the 3D village.",
      controlPoints: 2,
      accuracySi: "±40–80 m na območju vasi (najbolje zasidran list serije)",
      accuracyEn: "±40–80 m over the village area (the best-anchored sheet of the series)",
      lastChecked: "2026-10-08",
    },
    structuredEntries: 156,
    lastVerified: "2026-10-07",
    noteSi:
      "List z jedrom vasi in cerkvijo St. Veith (sv. Vid, oznaka K, stavba z apsido). Sken 3010 × 2158 px. Iz lista je vektoriziranih 156 stavbnih objektov (RECONSTRUCTED). OPOMBA (issue #4): vektorizacija zajema GEOMETRIJO stavb, ne pa dokazanih povezav s hišnimi številkami — lista ne nosi berljivih hišnih št. ob vseh objektih; te izhajajo iz PT/PUA registrov (156 geometrij ≥ 84 hiš = ni 1:1 povezave). P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — neodvisna validacija neatline afine z zunanjim virom: sodobne parcele (GURS eZKN WFS, EPSG:3794 → WGS84) preslikane prek P46 afine pasti na narisane črte 1825; mediana residuala 9.8 m (p90 13.7 m; 640 DRAWN parcel; kontrola metode pod GEOTRUTH mejami — residual skladen z ±40–80 m), pokritost črnila cov@0 0.542 nad kontrolo-zamik 200 px (0.473) in se pri najboljšem zamiku strmi (0.717); SHEET_GEOREFS ostaja nespremenjen do človeške potrditve črt (lekcija P9; izrezi research/issue17/neatline-crops/); strojno berljivo /api/atlas/gurs-overlay (invarianti I1–I7, dokaz research/issue17/gurs-overlay.json). P48 (2026-10-13, issue #14, deterministic — scripts/p48_buildings_overlay.py): STAVBNI OVERLAY — sodobni stavbni tlorisi (GURS eZKN WFS SI.GURS.KN:STAVBE, OBRIS_GEOM; recept scripts/p48_fetch_stavbe.sh) preslikani prek GEOTRUTH mej na sken morajo pasti na narisane stavbne simbole 1825: 154 stavb v celici cf, 149 on-symbol (cov@best mediana 1.0, DRAWN cov@0 0.85), mediana residuala 9.9 m (p90 13.7 m) — stavbna raven potrjuje parcelno raven P47 (9.8 m); kontinuiteta: 37 parov z vektoriziranimi tlorisi (≤ 25 px, 36 strong), 136/156 tlorisov 1825 brez naslednika (razpršena zidanica — vinice/hambi na zahodnih pobočjih ni preživela); nadgradja P16 present.json (OSM 15/26/115); izrezi research/issue17/buildings-crops/; strojno berljivo /api/atlas/buildings-overlay (invarianti I1–I8, dokaz research/issue17/buildings-overlay.json). P54 (2026-10-14, issue #12 nadgradnja, deterministic — scripts/p54_present_gurs.py): PRESENT.JSON NA URADNIH OBRISIH — »Kaj je izginilo?« nadgrajeno z OSM posnetka (15/26/115, pokrival le jedro) na uradne GURS eZKN obrise (380 stavb v oknu A02 + sodobna vas, vse KO 1544); pravila P16 nespremenjena, kalibrirana z replajo na starih podatkih (156/156); rezultat 18/21/117, 7 tlorisov spremenilo status; d zapisana za vse 156 (do 1541.2 m na zahodnih pobočjih); dokaz research/issue17/present-gurs.json + arhiv P16 research/issue17/present-osm-p16.json. ",
    noteEn:
      "Sheet with the village core and St. Veith church (marked K, apsidal building). Scan 3010 × 2158 px. 156 building objects vectorised from the sheet (RECONSTRUCTED). NOTE (issue #4): the vectorisation captures the buildings' GEOMETRY, not proven links to house numbers — the sheet does not carry readable house numbers by every object; those come from the PT/PUA registers (156 geometries ≥ 84 houses = no 1:1 link). P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — an independent validation of the neatline affine with an external source: modern parcels (GURS eZKN WFS, EPSG:3794 → WGS84) mapped through the P46 affine fall on the drawn 1825 lines; median residual 9.8 m (p90 13.7 m; 640 DRAWN parcels; the method control under the GEOTRUTH bounds — residual consistent with ±40–80 m), ink coverage cov@0 0.542 above the 200-px shift control (0.473) and sharpening under best alignment (0.717); SHEET_GEOREFS remains unchanged until human confirmation of the lines (the P9 lesson; crops in research/issue17/neatline-crops/); machine-readable /api/atlas/gurs-overlay (invariants I1–I7, evidence research/issue17/gurs-overlay.json). P48 (2026-10-13, issue #14, deterministic — scripts/p48_buildings_overlay.py): BUILDING OVERLAY — modern building footprints (GURS eZKN WFS SI.GURS.KN:STAVBE, OBRIS_GEOM; receipt scripts/p48_fetch_stavbe.sh) mapped via the GEOTRUTH bounds onto the scan must fall on the drawn 1825 building symbols: 154 buildings in cell cf, 149 on-symbol (cov@best median 1.0, DRAWN cov@0 0.85), median residual 9.9 m (p90 13.7 m) — the building level confirms the parcel level of P47 (9.8 m); continuity: 37 pairs with vectorized footprints (≤ 25 px, 36 strong), 136/156 1825 footprints without a successor (the dispersed settlement — vineyard cottages/hambas on the western slopes did not survive); an upgrade of P16 present.json (OSM 15/26/115); crops in research/issue17/buildings-crops/; machine-readable /api/atlas/buildings-overlay (invariants I1–I8, evidence research/issue17/buildings-overlay.json). P54 (2026-10-14, issue #12 upgrade, deterministic — scripts/p54_present_gurs.py): PRESENT.JSON ON OFFICIAL FOOTPRINTS — »What has vanished?« upgraded from the OSM snapshot (15/26/115, core only) to official GURS eZKN footprints (380 buildings within the A02 + modern-village window, all KO 1544); P16 rules unchanged, calibrated by replay on the old data (156/156); result 18/21/117, 7 footprints changed status; d recorded for all 156 (up to 1541.2 m on the western slopes); evidence research/issue17/present-gurs.json + the P16 archive research/issue17/present-osm-p16.json. ",
  },
  {
    id: "src-a03",
    code: "N083A03",
    type: "cadastral-map",
    titleSi: "Katastrski list A03 — občina Grüble, vzhodni predeli z razpršenimi zaselki",
    titleEn: "Cadastral sheet A03 — municipality of Grüble, eastern dispersed hamlets",
    unit: "list A03",
    vacId: "227670",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227670",
    fileRef: "IIIF: /vac/iiif/raster (uodid 227670)",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/n83-a03-thumb.jpg",
    georeferenced: true,
    transferStatus: "TRANSFERRED",
    georefStatus: "GEOREFERENCED",
    placement: {
      precision: "NEATLINE_PARTIAL_GEOREFERENCED",
      methodSi: "P50 (2026-10-14): P46 neatline afina AKTIVIRANA (celica dg) — meje = narisana neatline = uradna meja celice VKIX24dg (eZKN 1:2880); S/E strani detektirane, N/W inferred preko s̄ = 0.7746 m/px; 5 neodvisnih plasti dokazov (neatline kalibracija A02 9,3/13,2 m; parcele P47 mediana 9,8 m; stavbe P48 kontrola; sidro P49; napisi 7/7). Prej P10 GRID_APPROX ±200–400 m.",
      methodEn: "P50 (2026-10-14): the P46 neatline affine ACTIVATED (cell dg) — bounds = the drawn neatline = the official boundary of cell VKIX24dg (eZKN 1:2880); S/E sides detected, N/W inferred via s̄ = 0.7746 m/px; 5 independent evidence layers (neatline calibration A02 9.3/13.2 m; parcels P47 median 9.8 m; buildings P48 control; anchor P49; labels 7/7). Previously P10 GRID_APPROX ±200–400 m.",
      controlPoints: 6,
      accuracySi: "±50 m (NEATLINE_PARTIAL; premik vs P10 17,4 m). Prej ±200–400 m.",
      accuracyEn: "±50 m (NEATLINE_PARTIAL; shift vs P10 17.4 m). Previously ±200–400 m.",
      lastChecked: "2026-10-14",
    },
    structuredEntries: 0,
    lastVerified: "2026-10-08",
    noteSi:
      "GEOREFERENCA (P10, 2026-10-08): okvirna oznaka lista »O.IX24dg« = sekcijska celica eZKN mreže (GURS) VKIX24dg z uradno geometrijo → list = JUŽNOZAHODNA celica (45,5437–45,5575 N, 15,2485–15,2730 E); risana vsebina = le vzhodni pas = zahodni rob k.o. Griblje (meja s k.o. Tribuče/Bedenj); validacije: TRIBUTSCH → k.o. Tribuče ✓, WEIDENDORF → k.o. Bedenj ✓, »Borli« ≈ istoimensko območje na ZKN »GRIBLJE 4« (eZKN) ✓ (raziskava: research/georef-n83/ P10; ±200–400 m). List z razpršeno poselitvijo na vzhodnem delu k.o. in z obmejnimi predeli sosednjih občin. Digitalna kopija prenesena iz VAČ IIIF (2645 × 2154 px); georeferenca še ni izračunana — poskus P8 (2026-10-08, deterministično): zasidranje na reko Kolpo (ekstrakcija pasu med bregovnimi črtami + primerjava z moderno strugo iz OpenTopoMap) je na validaciji A02 izkazalo NEDELOVITNOST — Kolpa je tu premalo vijugasta za določitev smeri sever–jug in merila (napaka cerkve 0,9–1,6 km); raziskovalna pot v research/georef-n83/ (dokumentirana negativna ugotovitev; potreben VAČ metapodatek ali točkovno sidro). P9 (2026-10-08, VLM ploščični sken): na listu NI reke; naselbinska veriga (~41 stavb) poteka NAVPIČNO ob vzhodnem robu (x ≈ 87–91 %) — skladno z nadaljevanjem vzdolžnega pasu vasi Griblje (Dolnje Griblje?) proti jugu na zemljepisni dolžini vasi [~]; razpršen napis TRIBUTSCH = ozemlje k.o. Tribuče (45,545/15,243); WEIDENDORF (Bedenj) v spodnjem delu. List je približno sever-gor (veriga teče S–J) — nasprotje A04 (+31°) [~]. P45 (2026-10-11, validacija porazdelitve stavb — neodvisna kampanja): veriga 30 zaznanih rdečih simbolov (x 86–93 %) pod celično preslikavo pade na sodobno verigo 51 stavb (GURS) z mediano 89 m — celična umestitev kvantitativno POTRJENA (pošteno ±150–250 m; prosti/omejeni fitovi zavrnjeni; dokaz research/georef-n83/p45-sheet-fits.json). P46 (2026-10-12, issue #14, deterministic — scripts/p46_neatline_georef.py): NEATLINE SIDRO — narisana neatline lista = meja sekcije eZKN 1:2880; detektirani S (y 2058.3, pokritost 1.0, tilt 1 px) in E (x 2476.8, tilt 21 px); N/W implicitno preko skupnega merila s̄ = 0.7746 m/px (iz A04: sx 0.77654 / sy 0.77266, medosna konsistenca 0,5 %); princip kalibriran na A02 (residuala 9.3/13.2 m pod GEOTRUTH afino); nova meja [45.557532, 15.248718]–[45.543722, 15.272827] (premik vs celica le 17 m — konvergencija); ne-regresija 7/7 P10 napisov (TRIBUTSCH v k.o. Tribuče ✓, WEIDENDORF v k.o. Bedenj ✓ — poligonska validacija nad naselja-wgs84.json); PREDLOG: NEATLINE_PARTIAL_GEOREFERENCED ±50 m (iz ±200–400 m) — SHEET_GEOREFS ostaja nespremenjen do človeške potrditve detektiranih črt (lekcija P9); strojno berljivo /api/atlas/neatline-georef (invarianti I1–I7, dokaz research/issue17/neatline-georef.json). P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — neodvisna validacija neatline afine z zunanjim virom: sodobne parcele (GURS eZKN WFS, EPSG:3794 → WGS84) preslikane prek P46 afine pasti na narisane črte 1825; mediana residuala 9.8 m (p90 13.2 m; 112 DRAWN parcel), pokritost črnila cov@0 0.487 nad kontrolo-zamik 200 px (0.32) in se pri najboljšem zamiku strmi (0.729); SHEET_GEOREFS ostaja nespremenjen do človeške potrditve črt (lekcija P9; izrezi research/issue17/neatline-crops/); strojno berljivo /api/atlas/gurs-overlay (invarianti I1–I7, dokaz research/issue17/gurs-overlay.json). AKTIVACIJA P50 (2026-10-14, issue #14/§3, deterministic — scripts/p50_georef_closure.py): GEOREF ZAPORA — P46 predlog nadgradnje je AKTIVIRAN v SHEET_GEOREFS: meje = P46 neatline [45.557532, 15.248718]–[45.543722, 15.272827] (premik 17,4 m), merilo 0,7746 m/px, georefStatus GEOREFERENCED / placement NEATLINE_PARTIAL_GEOREFERENCED ±50 m; odločba na 5 neodvisnih plasti (L0 kalibracija A02 9,3/13,2 m; L1 parcele ta list mediana 9,8 m; L2 stavbe kontrola A02 149/154; L3 sidro P49; L4 napisi 7/7); pogoj iz P46/P47 izpolnjen s plastmi L1–L4, vizualni pregled izrezov priporočen [~]; strojno berljivo /api/atlas/georef-closure (invarianti I1–I10). P51 (2026-10-14, issue #14/§3, deterministic — scripts/p51_leaflet_overlay.py): LEAFLET OVERLAY — list A03 kot slikovna prekrivka na atlasnem zemljevidu (stikalo »List A03 (±50 m)«, privzeto IZKLOPLJENO): ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0), SE = affine(2645,2154)) == P50 boundsImageNWSE [45.558062, 15.24863]–[45.543052, 15.274475] (≤ 5e-6°) — ni ročno prepisanih koordinat; MERJENA SUBTELNOST: Leaflet ne podpira rotiranih prekrivk — slika razpete v osno poravnan okvir, odmik vogalov ≤ 19,3 m (dva vogala točna), skew 0.5475° ≤ 1.0° — del ±50 m negotovosti lista; ob prekrivki črtkani neatline okvir s statusom; skupna prosojnost z A01/A02; strojno berljivo /api/atlas/leaflet-overlay (invarianti I1–I8).",
    noteEn:
      "GEOREFERENCE (P10, 2026-10-08): the sheet's frame code »O.IX24dg« = the eZKN grid cell (GURS) VKIX24dg with official geometry → the sheet = the SOUTHWESTERN cell (45.5437–45.5575 N, 15.2485–15.2730 E); the drawn content = the eastern strip only = the western edge of c.m. Griblje (the border with c.m. Tribuče/Bedenj); validations: TRIBUTSCH → c.m. Tribuče ✓, WEIDENDORF → c.m. Bedenj ✓, »Borli« ≈ the same-named area on the ZKN sheet »GRIBLJE 4« (eZKN) ✓ (research: research/georef-n83/ P10; ±200–400 m). Sheet with dispersed settlement in the eastern part of the cadastral municipality and boundary areas with neighbouring municipalities. Digital copy transferred from VAČ IIIF (2645 × 2154 px); georeference not yet computed — the P8 attempt (2026-10-08, deterministic): anchoring on the Kolpa river (bank-to-bank band extraction + comparison with the modern channel from OpenTopoMap) proved UNWORKABLE in A02 validation — the Kolpa meanders too weakly here to pin the north–south direction and scale (church error 0.9–1.6 km); research path in research/georef-n83/ (a documented negative finding; VAČ metadata or a point anchor needed). P9 (2026-10-08, VLM tile scan): NO river on the sheet; the settlement chain (~41 buildings) runs VERTICALLY along the east edge (x ≈ 87–91 %) — consistent with the southern continuation of the elongated Griblje village ribbon (Dolnje Griblje?) at the village's longitude [~]; the spread label TRIBUTSCH = the territory of c.m. Tribuče (45.545/15.243); WEIDENDORF (Bedenj) in the lower part. The sheet is roughly north-up (the chain runs N–S) — in contrast to A04 (+31°) [~]. P45 (2026-10-11, building-distribution validation — an independent campaign): the chain of 30 detected red symbols (x 86–93 %) under the cell mapping lands on the modern chain of 51 buildings (GURS) at a median of 89 m — the cell placement quantitatively CONFIRMED (honestly ±150–250 m; the free/constrained fits rejected; evidence research/georef-n83/p45-sheet-fits.json). P46 (2026-10-12, issue #14, deterministic — scripts/p46_neatline_georef.py): NEATLINE ANCHOR — the sheet's drawn neatline = the eZKN 1:2880 section boundary; detected S (y 2058.3, coverage 1.0, tilt 1 px) and E (x 2476.8, tilt 21 px); N/W inferred via the shared scale s̄ = 0.7746 m/px (from A04: sx 0.77654 / sy 0.77266, axis consistency 0.5%); the principle calibrated on A02 (residuals 9.3/13.2 m under the GEOTRUTH affine); new bounds [45.557532, 15.248718]–[45.543722, 15.272827] (shift vs the cell only 17 m — grid convergence); non-regression 7/7 P10 labels (TRIBUTSCH in c.m. Tribuče ✓, WEIDENDORF in c.m. Bedenj ✓ — polygon validation over naselja-wgs84.json); PROPOSAL: NEATLINE_PARTIAL_GEOREFERENCED ±50 m (from ±200–400 m) — SHEET_GEOREFS unchanged until human confirmation of the detected lines (the P9 lesson); machine-readable /api/atlas/neatline-georef (invariants I1–I7, evidence research/issue17/neatline-georef.json). P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — an independent validation of the neatline affine with an external source: modern parcels (GURS eZKN WFS, EPSG:3794 → WGS84) mapped through the P46 affine fall on the drawn 1825 lines; median residual 9.8 m (p90 13.2 m; 112 DRAWN parcels), ink coverage cov@0 0.487 above the 200-px shift control (0.32) and sharpening under best alignment (0.729); SHEET_GEOREFS remains unchanged until human confirmation of the lines (the P9 lesson; crops in research/issue17/neatline-crops/); machine-readable /api/atlas/gurs-overlay (invariants I1–I7, evidence research/issue17/gurs-overlay.json). P50 ACTIVATION (2026-10-14, issue #14/§3, deterministic — scripts/p50_georef_closure.py): GEOREF CLOSURE — the P46 upgrade proposal is ACTIVATED in SHEET_GEOREFS: bounds = the P46 neatline [45.557532, 15.248718]–[45.543722, 15.272827] (shift 17.4 m), scale 0.7746 m/px, georefStatus GEOREFERENCED / placement NEATLINE_PARTIAL_GEOREFERENCED ±50 m; the decision on 5 independent layers (L0 A02 calibration 9.3/13.2 m; L1 parcels this sheet median 9.8 m; L2 buildings control A02 149/154; L3 anchor P49; L4 labels 7/7); the P46/P47 condition fulfilled by layers L1–L4, visual review of the crops recommended [~]; machine-readable /api/atlas/georef-closure (invariants I1–I10). P51 (2026-10-14, issue #14/§3, deterministic — scripts/p51_leaflet_overlay.py): LEAFLET OVERLAY — sheet A03 as an image overlay on the atlas map (toggle »Sheet A03 (±50 m)«, default OFF): the scan envelope INDEPENDENTLY recomputed from the P46 affine (NW = affine(0,0), SE = affine(2645,2154)) == P50 boundsImageNWSE [45.558062, 15.24863]–[45.543052, 15.274475] (≤ 5e-6°) — no hand-copied coordinates; MEASURED SUBTLETY: Leaflet does not support rotated overlays — the image is stretched into an axis-aligned frame, corner deviation ≤ 19.3 m (two corners exact), skew 0.5475° ≤ 1.0° — part of the sheet's ±50 m uncertainty; a dashed neatline frame with the status accompanies the overlay; shared opacity with A01/A02; machine-readable /api/atlas/leaflet-overlay (invariants I1–I8).",
  },
  {
    id: "src-a04",
    code: "N083A04",
    type: "cadastral-map",
    titleSi: "Katastrski list A04 — občina Grüble, južni del občine (celica cg)",
    titleEn: "Cadastral sheet A04 — municipality of Grüble, southern part (cell cg)",
    unit: "list A04",
    vacId: "227671",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227671",
    fileRef: "IIIF: /vac/iiif/raster (uodid 227671)",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/n83-a04-thumb.jpg",
    georeferenced: true,
    transferStatus: "TRANSFERRED",
    georefStatus: "GEOREFERENCED",
    placement: {
      precision: "NEATLINE_GEOREFERENCED",
      methodSi: "P50 (2026-10-14): P46 neatline afina AKTIVIRANA (celica cg) — meje = narisana neatline = uradna meja celice VKIX24cg (eZKN 1:2880); vse 4 strani detektirane, merilo sx 0.77654 / sy 0.77266, afina 4 vogalov RMS ≤ 30 m; 5 plasti dokazov (kalibracija A02; parcele P47 mediana 5,6 m — najboljša v seriji; stavbe P48 kontrola; sidro P49; napisi 7/7). Prej P10 GRID_APPROX ±200–400 m (sam popravek P9 636 m ostaja dokumentiran).",
      methodEn: "P50 (2026-10-14): the P46 neatline affine ACTIVATED (cell cg) — bounds = the drawn neatline = the official boundary of cell VKIX24cg (eZKN 1:2880); all 4 sides detected, scale sx 0.77654 / sy 0.77266, 4-corner affine RMS ≤ 30 m; 5 evidence layers (A02 calibration; parcels P47 median 5.6 m — the best of the series; buildings P48 control; anchor P49; labels 7/7). Previously P10 GRID_APPROX ±200–400 m (the P9 636 m correction remains documented).",
      controlPoints: 7,
      accuracySi: "±40 m (NEATLINE; premik vs P10 16,9 m). Prej ±200–400 m.",
      accuracyEn: "±40 m (NEATLINE; shift vs P10 16.9 m). Previously ±200–400 m.",
      lastChecked: "2026-10-14",
    },
    structuredEntries: 0,
    lastVerified: "2026-10-08",
    noteSi:
      "POPRAVEK P10 (2026-10-08): okvirna oznaka lista »O.IX24cg« (trikratno prebrana) = celica eZKN mreže VKIX24cg (45,5436–45,5574 N, 15,2728–15,2973 E) — območje DIREKTNO JUŽNO od A02, NE ovin Kolpe pri Adlešiči! P9 georeferenca (rot +30,9°, ovin 45,522–45,538) ZAVRŽENA: stavbna validacija 636 m mediane odmika (statistična izključitev), P9 kontrole nedisterminativne, P9 »reka« = verjetno dolina/cesta (Kolpa teče ~1,2 km vzhodno od celice, IZVEN lista). Nova lega: sever-gor, celica cg + robovi; validacije WEIDENDORF→k.o. Bedenj ✓, ADLESCHITZ→k.o. Adlešiči ✓, razpored ≈ ZKN »GRIBLJE 4« ✓ (±200–400 m; raziskava: research/georef-n83/ P10). Prejšnji zapis: list z dolino Kolpe in ovinom reke pri Adlešičih — edini list serije s komaj zasidrljivim odsekom struge. Digitalna kopija prenesena iz VAČ IIIF (2645 × 2158 px). GEOREFERENCA (P9, 2026-10-08, ob dvigu VLM kvote): 10 točk struge (VLM vodenje po ploščicah) → podobnostni fit proti validirani moderni centerline Kolpe: rotacija +30,9°, merilo 0,55 m/px, mediana 10 m; neodvisna kontrola 23 m; napisi ADLESCHITZ/WEIDENDORF (Bedenj)/TRIBUTSCH (Tribuče) skladni s k.o. sosedi. Status RECONSTRUCTED [~]: zasidran vzdolž reke (±100–150 m), vogali odvisni od dvoumnosti merila 0,45–0,74 (±250–470 m); list rotiran +31° v ovojnici bounds (raziskava: research/georef-n83/). Prejšnji poskus P8 (ravna struga pri Gribljah) negativen — ovin pri Adlešičih je razrešil zadrego. P45 (2026-10-11, validacija porazdelitve stavb — neodvisna kampanja): 170 simbolov po celem listu pod celično preslikavo doseže mediano 69,7 m do sodobnih stavb — umestitev POPRAVEK P10 kvantitativno POTRJENA (pošteno ±100–200 m; omejeni fit zavrnjen — premaknil bi oznake s k.o.-validiranih mest; dokaz research/georef-n83/p45-sheet-fits.json). P46 (2026-10-12, issue #14, deterministic — scripts/p46_neatline_georef.py): NEATLINE SIDRO — vse 4 strani detektirane (top 84.6 tilt 13, bottom 2071.9 tilt 10, left 95.4 tilt 4, right 2556.9 tilt 8); merilo sx 0.77654 / sy 0.77266 m/px (medosna konsistenca 0,5 %) + afina 4 vogalov na uradne kote celice cg (RMS 0,1 m); nova meja [45.55737, 15.273012]–[45.543554, 15.297115] (premik 17 m); ne-regresija: WEIDENDORF v k.o. Bedenj ✓ (poligon), ADLESCHITZ izven modernega k.o. Griblje ✓, Bresnik 34 m od P10 tarče; PREDLOG: NEATLINE_GEOREFERENCED ±40 m (iz ±200–400 m) — SHEET_GEOREFS nespremenjen do človeške potrditve črt (lekcija P9); strojno berljivo /api/atlas/neatline-georef. P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — neodvisna validacija neatline afine z zunanjim virom: sodobne parcele (GURS eZKN WFS, EPSG:3794 → WGS84) preslikane prek P46 afine pasti na narisane črte 1825; mediana residuala 5.6 m (p90 10.2 m; 498 DRAWN parcel; 128 EMPTY parcel (južno prekrivanje KO 1552) na v 1825 nenarisanih površinah), pokritost črnila cov@0 0.447 nad kontrolo-zamik 200 px (0.298) in se pri najboljšem zamiku strmi (0.707); SHEET_GEOREFS ostaja nespremenjen do človeške potrditve črt (lekcija P9; izrezi research/issue17/neatline-crops/); strojno berljivo /api/atlas/gurs-overlay (invarianti I1–I7, dokaz research/issue17/gurs-overlay.json). AKTIVACIJA P50 (2026-10-14, issue #14/§3, deterministic — scripts/p50_georef_closure.py): GEOREF ZAPORA — P46 predlog nadgradnje je AKTIVIRAN v SHEET_GEOREFS: meje = P46 neatline [45.55737, 15.273012]–[45.543554, 15.297115] (premik 16,9 m), merilo 0,7746 m/px (izmerjeno sx 0.77654 / sy 0.77266), georefStatus GEOREFERENCED / placement NEATLINE_GEOREFERENCED ±40 m (vse 4 strani detektirane); parcele P47 mediana 5,6 m — najboljša v seriji; pogoj iz P46/P47 izpolnjen s plastmi L1–L4, vizualni pregled izrezov priporočen [~]; strojno berljivo /api/atlas/georef-closure (invarianti I1–I10). P51 (2026-10-14, issue #14/§3, deterministic — scripts/p51_leaflet_overlay.py): LEAFLET OVERLAY — list A04 kot slikovna prekrivka na atlasnem zemljevidu (stikalo »List A04 (±40 m)«, privzeto IZKLOPLJENO): ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0), SE = affine(2645,2158)) == P50 boundsImageNWSE [45.557958, 15.272079]–[45.542957, 15.297976] (≤ 5e-6°) — ni ročno prepisanih koordinat; MERJENA SUBTELNOST: Leaflet ne podpira rotiranih prekrivk — slika razpete v osno poravnan okvir, odmik vogalov ≤ 20,0 m (dva vogala točna), skew 0.568° ≤ 1.0° — del ±40 m negotovosti lista; ob prekrivki črtkani neatline okvir s statusom; skupna prosojnost z A01/A02; strojno berljivo /api/atlas/leaflet-overlay (invarianti I1–I8).",
    noteEn:
      "P10 CORRECTION (2026-10-08): the sheet's frame code »O.IX24cg« (read three times) = the eZKN grid cell VKIX24cg (45.5436–45.5574 N, 15.2728–15.2973 E) — the area DIRECTLY SOUTH of A02, NOT the Kolpa bend by Adlešiči! The P9 georeference (rot +30.9°, the bend at 45.522–45.538) RETRACTED: the building validation shows a 636 m median offset (statistically excluded), P9's checks were non-discriminating, P9's »river« = probably a valley/road (the Kolpa flows ~1.2 km east of the cell, OUTSIDE the sheet). New position: north-up, cell cg + margins; validations WEIDENDORF→c.m. Bedenj ✓, ADLESCHITZ→c.m. Adlešiči ✓, the layout ≈ the ZKN sheet »GRIBLJE 4« ✓ (±200–400 m; research: research/georef-n83/ P10). Previous record: sheet with the Kolpa valley and the river bend by Adlešiči — the only sheet of the series with an anchorable channel stretch. Digital copy transferred from VAČ IIIF (2645 × 2158 px). GEOREFERENCE (P9, 2026-10-08, after the VLM quota was lifted): 10 channel points (VLM tile-guided) → similarity fit against the validated modern Kolpa centerline: rotation +30.9°, scale 0.55 m/px, median 10 m; independent check 23 m; the ADLESCHITZ/WEIDENDORF (Bedenj)/TRIBUTSCH (Tribuče) labels consistent with the neighbouring municipalities. Status RECONSTRUCTED [~]: anchored along the river (±100–150 m), the corners depend on the scale ambiguity 0.45–0.74 (±250–470 m); the sheet is rotated +31° inside the bounds envelope (research: research/georef-n83/). The earlier P8 attempt (straight channel at Griblje) was negative — the Adlešiči bend resolved the impasse. P45 (2026-10-11, building-distribution validation — an independent campaign): 170 symbols across the whole sheet under the cell mapping reach a median of 69.7 m to modern buildings — the P10 CORRECTION placement quantitatively CONFIRMED (honestly ±100–200 m; the constrained fit rejected — it would move the labels off their c.m.-validated positions; evidence research/georef-n83/p45-sheet-fits.json). P46 (2026-10-12, issue #14, deterministic — scripts/p46_neatline_georef.py): NEATLINE ANCHOR — all 4 sides detected (top 84.6 tilt 13, bottom 2071.9 tilt 10, left 95.4 tilt 4, right 2556.9 tilt 8); scale sx 0.77654 / sy 0.77266 m/px (axis consistency 0.5%) + a 4-corner affine onto the official cg cell corners (RMS 0.1 m); new bounds [45.55737, 15.273012]–[45.543554, 15.297115] (shift 17 m); non-regression: WEIDENDORF inside c.m. Bedenj ✓ (polygon), ADLESCHITZ outside the modern c.m. Griblje ✓, Bresnik 34 m from the P10 target; PROPOSAL: NEATLINE_GEOREFERENCED ±40 m (from ±200–400 m) — SHEET_GEOREFS unchanged until human confirmation of the lines (the P9 lesson); machine-readable /api/atlas/neatline-georef. P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — an independent validation of the neatline affine with an external source: modern parcels (GURS eZKN WFS, EPSG:3794 → WGS84) mapped through the P46 affine fall on the drawn 1825 lines; median residual 5.6 m (p90 10.2 m; 498 DRAWN parcels; 128 EMPTY parcels (the southern KO 1552 overlap) on surfaces not drawn in 1825), ink coverage cov@0 0.447 above the 200-px shift control (0.298) and sharpening under best alignment (0.707); SHEET_GEOREFS remains unchanged until human confirmation of the lines (the P9 lesson; crops in research/issue17/neatline-crops/); machine-readable /api/atlas/gurs-overlay (invariants I1–I7, evidence research/issue17/gurs-overlay.json). P50 ACTIVATION (2026-10-14, issue #14/§3, deterministic — scripts/p50_georef_closure.py): GEOREF CLOSURE — the P46 upgrade proposal is ACTIVATED in SHEET_GEOREFS: bounds = the P46 neatline [45.55737, 15.273012]–[45.543554, 15.297115] (shift 16.9 m), scale 0.7746 m/px (measured sx 0.77654 / sy 0.77266), georefStatus GEOREFERENCED / placement NEATLINE_GEOREFERENCED ±40 m (all 4 sides detected); parcels P47 median 5.6 m — the best of the series; the P46/P47 condition fulfilled by layers L1–L4, visual review of the crops recommended [~]; machine-readable /api/atlas/georef-closure (invariants I1–I10). P51 (2026-10-14, issue #14/§3, deterministic — scripts/p51_leaflet_overlay.py): LEAFLET OVERLAY — sheet A04 as an image overlay on the atlas map (toggle »Sheet A04 (±40 m)«, default OFF): the scan envelope INDEPENDENTLY recomputed from the P46 affine (NW = affine(0,0), SE = affine(2645,2158)) == P50 boundsImageNWSE [45.557958, 15.272079]–[45.542957, 15.297976] (≤ 5e-6°) — no hand-copied coordinates; MEASURED SUBTLETY: Leaflet does not support rotated overlays — the image is stretched into an axis-aligned frame, corner deviation ≤ 20.0 m (two corners exact), skew 0.568° ≤ 1.0° — part of the sheet's ±40 m uncertainty; a dashed neatline frame with the status accompanies the overlay; shared opacity with A01/A02; machine-readable /api/atlas/leaflet-overlay (invariants I1–I8).",
  },
  {
    id: "src-a05",
    code: "N083A05",
    type: "cadastral-map",
    titleSi: "Katastrski list A05 — občina Grüble, južni predeli s poselitvijo",
    titleEn: "Cadastral sheet A05 — municipality of Grüble, southern settled outskirts",
    unit: "list A05",
    vacId: "227673",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227673",
    fileRef: "IIIF: /vac/iiif/raster (uodid 227673)",
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    thumb: "/atlas/n83-a05-thumb.jpg",
    georeferenced: true,
    transferStatus: "TRANSFERRED",
    georefStatus: "GEOREFERENCED",
    placement: {
      precision: "NEATLINE_GEOREFERENCED",
      methodSi: "P50 (2026-10-14): P46 neatline afina AKTIVIRANA (celica ch) — meje = narisana neatline = uradna meja celice VKIX24ch (eZKN 1:2880); vse 4 strani detektirane, 4-vogalna afina; stavbna potrditev P48 26 on-symbol @ 10,1 m + sidro P49 (43,2 px od VLM branja); parcele P47 mediana 9,3 m; napisi 7/7. Prej P10 GRID_APPROX ±200–400 m.",
      methodEn: "P50 (2026-10-14): the P46 neatline affine ACTIVATED (cell ch) — bounds = the drawn neatline = the official boundary of cell VKIX24ch (eZKN 1:2880); all 4 sides detected, the 4-corner affine; building-level confirmation P48 26 on-symbol @ 10.1 m + the P49 anchor (43.2 px from the VLM read); parcels P47 median 9.3 m; labels 7/7. Previously P10 GRID_APPROX ±200–400 m.",
      controlPoints: 6,
      accuracySi: "±40 m (NEATLINE; premik vs P10 18,0 m). Prej ±200–400 m. Hišne št. na listu so znotraj tedanje k.o. Griblje (ozemlje pozneje odvzeto).",
      accuracyEn: "±40 m (NEATLINE; shift vs P10 18.0 m). Previously ±200–400 m. The house numbers on the sheet are within the then c.m. Griblje (territory later detached).",
      lastChecked: "2026-10-14",
    },
    structuredEntries: 0,
    lastVerified: "2026-10-08",
    noteSi:
      "GEOREFERENCA (P10, 2026-10-08): okvirna oznaka lista »O.IX24ch« = sekcijska celica eZKN mreže VKIX24ch (45,5299–45,5437 N, 15,2726–15,2971 E) — skrajni JUG 1825 k.o. Griblje (današnja k.o. Adlešiči — meja se je pozneje premaknila!); sklop ~45 stavb pri (75 %, 28 %) → območje Fučkovcev/Dragošev [~]; validacije: ADLESC/Vedalschitz → k.o. Adlešiči ✓, »Pri Jankovichti« → naselje Jankoviči ✓ (raziskava: research/georef-n83/ P10; ±200–400 m). List z gručasto poselitvijo (rdeči nalič stavb in dvorišč) na vzhodnem delu in obmejnimi napisi sosednjih občin. Digitalna kopija prenesena iz VAČ IIIF (2634 × 2165 px); georeferenca še ni izračunana — poskus P8 (2026-10-08) prek reke Kolpe: negativna ugotovitev (see research/georef-n83/); reka na listu morda ni vidna (južna meja k.o. ni ob Kolpi). P9 (2026-10-08, VLM ploščični sken): potrjeno — reke NI; en velik naselbinski sklop (~45 stavb) pri (75 %, 28 %) s hišnimi številkami (npr. N°9) in vrstnimi imeni (Pri Janhovičih, Na Dvagi Žoleg, Šiže Vardianove [~]) — verjetno južni konec vzdolžnega pasu vasi Griblje (zaselki: Dolnje Griblje / Brinsko selo?) [~]; razpršene črke A D L E S C… zgoraj desno in napis [Vedalschitz ~] = ozemlje sosednje k.o. Adlešiči; glava lista nosi »V« (5. list serije, skladen z A03 = »III«). Simboli stavb nakazujejo merilo ~0,66 m/px [~] (primerjava z A02). P45 (2026-10-11, validacija porazdelitve stavb — neodvisna kampanja): sklop ~30 simbolov (x 52–86 %) pod celično preslikavo pade na sodobne stavbe z mediano 27 m (60 % znotraj 30 m); omejeni fit neodvisno potrdi lego z odmikom 64 m — umestitev kvantitativno POTRJENA (dokaz research/georef-n83/p45-sheet-fits.json; zamenjana s P46–P50 neatline georeferenco). P46 (2026-10-12, issue #14, deterministic — scripts/p46_neatline_georef.py): NEATLINE SIDRO — vse 4 strani detektirane (top 82.4 tilt 19, bottom 2075.4 tilt 4, left 102.4 tilt 10, right 2557.4 tilt 10); 4-vogalna afina na uradne kote celice ch; nova meja [45.543722, 15.272828]–[45.529907, 15.296925] (premik 18 m); ne-regresija: sklop ~45 stavb (Fučkovci) 33 m od P10 tarče, Pri Jankovichti 33 m — oba znotraj celice; PREDLOG: NEATLINE_GEOREFERENCED ±40 m (iz ±200–400 m) — SHEET_GEOREFS nespremenjen do človeške potrditve črt (lekcija P9); strojno berljivo /api/atlas/neatline-georef. P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — neodvisna validacija neatline afine z zunanjim virom: sodobne parcele (GURS eZKN WFS, EPSG:3794 → WGS84) preslikane prek P46 afine pasti na narisane črte 1825; mediana residuala 9.3 m (p90 13.1 m; 165 DRAWN parcel; 394/559 parcel EMPTY = skupna paša WAIDENDORF v 1825 (land-use dokaz, ne napaka registracije)), pokritost črnila cov@0 0.445 nad kontrolo-zamik 200 px (0.189) in se pri najboljšem zamiku strmi (0.86); SHEET_GEOREFS ostaja nespremenjen do človeške potrditve črt (lekcija P9; izrezi research/issue17/neatline-crops/); strojno berljivo /api/atlas/gurs-overlay (invarianti I1–I7, dokaz research/issue17/gurs-overlay.json). P48 (2026-10-13, issue #14, deterministic — scripts/p48_buildings_overlay.py): STAVBNI OVERLAY — sodobni stavbni tlorisi preslikani prek P46 afine: 95 stavb v celici ch, 26 on-symbol (mediana residuala 10.1 m) — neodvisna potrditev afine na stavbni ravni; sklop Fučkovci se registrira tudi stavbeno; strojno berljivo /api/atlas/buildings-overlay (dokaz research/issue17/buildings-overlay.json). P49 (2026-10-13, issue #14, deterministic — scripts/p49_fucukovci1825.py): FUČKOVCI 1825 — TRI neodvisna dokazna sloja: (1) modern-anchored: 26 sodobnih stavb pada na narisane simbole (residual mediana 9.8 m), 25 v sklopu vasi = dokazana stavbna mesta z naslednikom (WGS84 v izpisu); (2) striktna detekcija temnih jeder: 53 (7 koreliranih, 19 neujemanih v sklopu — triaža: 2 stavbe + 4 nejasni = GONE-kandidati [~], ostalo text/črta/drevo/številka); (3) obseg sklopa: lupina 36 336 m² + masa črnila 257 571 px; ocena stavb [27, 44] — P10 ~45 znotraj mej, brez protislovja; DOKAZ o neizvedljivosti celotne vektorizacije (rožnati fill siva ~169 < 195, zasičenost maske 40.3 %); kontinuiteta ≥ 0.806 [~]; izrezi research/issue17/fucukovci-crops/; strojno berljivo /api/atlas/fucukovci-1825 (invarianti I1–I8, dokaz research/issue17/fucukovci-1825.json). AKTIVACIJA P50 (2026-10-14, issue #14/§3, deterministic — scripts/p50_georef_closure.py): GEOREF ZAPORA — P46 predlog nadgradnje je AKTIVIRAN v SHEET_GEOREFS: meje = P46 neatline [45.543722, 15.272828]–[45.529907, 15.296925] (premik 18,0 m), merilo 0,7746 m/px, georefStatus GEOREFERENCED / placement NEATLINE_GEOREFERENCED ±40 m (vse 4 strani detektirane); stavbna potrditev P48 26 @ 10,1 m + sidro P49 43,2 px; pogoj iz P46/P47 izpolnjen s plastmi L1–L4, vizualni pregled izrezov priporočen [~]; strojno berljivo /api/atlas/georef-closure (invarianti I1–I10). P51 (2026-10-14, issue #14/§3, deterministic — scripts/p51_leaflet_overlay.py): LEAFLET OVERLAY — list A05 kot slikovna prekrivka na atlasnem zemljevidu (stikalo »List A05 (±40 m)«, privzeto IZKLOPLJENO): ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0), SE = affine(2634,2165)) == P50 boundsImageNWSE [45.544293, 15.271822]–[45.529288, 15.297674] (≤ 5e-6°) — ni ročno prepisanih koordinat; MERJENA SUBTELNOST: Leaflet ne podpira rotiranih prekrivk — slika razpete v osno poravnan okvir, odmik vogalov ≤ 20,0 m (dva vogala točna), skew 0.5708° ≤ 1.0° — del ±40 m negotovosti lista; ob prekrivki črtkani neatline okvir s statusom; skupna prosojnost z A01/A02; strojno berljivo /api/atlas/leaflet-overlay (invarianti I1–I8).",
    noteEn:
      "GEOREFERENCE (P10, 2026-10-08): the sheet's frame code »O.IX24ch« = the eZKN grid cell VKIX24ch (45.5299–45.5437 N, 15.2726–15.2971 E) — the far SOUTH of the 1825 c.m. Griblje (today's c.m. Adlešiči — the boundary was later redrawn!); the cluster of ~45 buildings at (75 %, 28 %) → the Fučkovci/Dragoši area [~]; validations: ADLESC/Vedalschitz → c.m. Adlešiči ✓, »Pri Jankovichti« → the settlement of Jankoviči ✓ (research: research/georef-n83/ P10; ±200–400 m). Sheet with a clustered settlement (red tint of buildings and farmyards) in the eastern part and boundary labels of neighbouring municipalities. Digital copy transferred from VAČ IIIF (2634 × 2165 px); georeference not yet computed — the P8 river-anchoring attempt (2026-10-08) had a negative outcome (see research/georef-n83/); the river may not appear on this sheet at all (the southern k.o. boundary is not on the Kolpa). P9 (2026-10-08, VLM tile scan): confirmed — NO river; one large settlement cluster (~45 buildings) at (75 %, 28 %) with house numbers (e.g. N°9) and field names (Pri Janhovičih, Na Dvagi Žoleg, Šiže Vardianove [~]) — probably the southern end of the elongated Griblje village ribbon (hamlets: Dolnje Griblje / Brinsko selo?) [~]; the spread letters A D L E S C… at the top right and the label [Vedalschitz ~] = the territory of the neighbouring c.m. Adlešiči; the sheet header carries »V« (5th sheet of the series, consistent with A03 = »III«). The building symbols suggest a scale of ~0.66 m/px [~] (comparison with A02). P45 (2026-10-11, building-distribution validation — an independent campaign): a cluster of ~30 symbols (x 52–86 %) under the cell mapping lands on modern buildings at a median of 27 m (60 % within 30 m); the constrained fit independently confirms the position with a 64 m offset — the placement quantitatively CONFIRMED (evidence research/georef-n83/p45-sheet-fits.json; superseded by the P46–P50 neatline georeference). P46 (2026-10-12, issue #14, deterministic — scripts/p46_neatline_georef.py): NEATLINE ANCHOR — all 4 sides detected (top 82.4 tilt 19, bottom 2075.4 tilt 4, left 102.4 tilt 10, right 2557.4 tilt 10); a 4-corner affine onto the official ch cell corners; new bounds [45.543722, 15.272828]–[45.529907, 15.296925] (shift 18 m); non-regression: the ~45-building cluster (Fučkovci) 33 m from the P10 target, Pri Jankovichti 33 m — both inside the cell; PROPOSAL: NEATLINE_GEOREFERENCED ±40 m (from ±200–400 m) — SHEET_GEOREFS unchanged until human confirmation of the lines (the P9 lesson); machine-readable /api/atlas/neatline-georef. P47 (2026-10-13, issue #14, deterministic — scripts/p47_gurs_overlay.py): GURS PARCEL OVERLAY — an independent validation of the neatline affine with an external source: modern parcels (GURS eZKN WFS, EPSG:3794 → WGS84) mapped through the P46 affine fall on the drawn 1825 lines; median residual 9.3 m (p90 13.1 m; 165 DRAWN parcels; 394/559 parcels EMPTY = the 1825 WAIDENDORF common pasture (a land-use proof, not a registration error)), ink coverage cov@0 0.445 above the 200-px shift control (0.189) and sharpening under best alignment (0.86); SHEET_GEOREFS remains unchanged until human confirmation of the lines (the P9 lesson; crops in research/issue17/neatline-crops/); machine-readable /api/atlas/gurs-overlay (invariants I1–I7, evidence research/issue17/gurs-overlay.json). P48 (2026-10-13, issue #14, deterministic — scripts/p48_buildings_overlay.py): BUILDING OVERLAY — modern building footprints mapped via the P46 affine: 95 buildings in cell ch, 26 on-symbol (median residual 10.1 m) — an independent confirmation of the affine at the building level; the Fučkovci cluster registers at the building level too; machine-readable /api/atlas/buildings-overlay (evidence research/issue17/buildings-overlay.json). P49 (2026-10-13, issue #14, deterministic — scripts/p49_fucukovci1825.py): FUČKOVCI 1825 — THREE independent evidence layers: (1) modern-anchored: 26 modern buildings fall on drawn symbols (residual median 9.8 m), 25 inside the village cluster = proven building places with successors (WGS84 in the evidence file); (2) strict dark-core detection: 53 cores (7 corroborated, 19 unmatched inside the cluster — triage: 2 buildings + 4 unclear = GONE candidates [~], rest text/line/tree/number); (3) cluster extent: hull 36 336 m² + ink mass 257 571 px; building-count estimate [27, 44] — the P10 ~45 lies within the bounds, no contradiction; PROOF that full footprint vectorization is not feasible (pink fill gray ~169 < 195, mask saturation 40.3 %); continuity ≥ 0.806 [~]; crops in research/issue17/fucukovci-crops/; machine-readable /api/atlas/fucukovci-1825 (invariants I1–I8, evidence research/issue17/fucukovci-1825.json). P50 ACTIVATION (2026-10-14, issue #14/§3, deterministic — scripts/p50_georef_closure.py): GEOREF CLOSURE — the P46 upgrade proposal is ACTIVATED in SHEET_GEOREFS: bounds = the P46 neatline [45.543722, 15.272828]–[45.529907, 15.296925] (shift 18.0 m), scale 0.7746 m/px, georefStatus GEOREFERENCED / placement NEATLINE_GEOREFERENCED ±40 m (all 4 sides detected); building-level confirmation P48 26 @ 10.1 m + the P49 anchor 43.2 px; the P46/P47 condition fulfilled by layers L1–L4, visual review of the crops recommended [~]; machine-readable /api/atlas/georef-closure (invariants I1–I10). P51 (2026-10-14, issue #14/§3, deterministic — scripts/p51_leaflet_overlay.py): LEAFLET OVERLAY — sheet A05 as an image overlay on the atlas map (toggle »Sheet A05 (±40 m)«, default OFF): the scan envelope INDEPENDENTLY recomputed from the P46 affine (NW = affine(0,0), SE = affine(2634,2165)) == P50 boundsImageNWSE [45.544293, 15.271822]–[45.529288, 15.297674] (≤ 5e-6°) — no hand-copied coordinates; MEASURED SUBTLETY: Leaflet does not support rotated overlays — the image is stretched into an axis-aligned frame, corner deviation ≤ 20.0 m (two corners exact), skew 0.5708° ≤ 1.0° — part of the sheet's ±40 m uncertainty; a dashed neatline frame with the status accompanies the overlay; shared opacity with A01/A02; machine-readable /api/atlas/leaflet-overlay (invariants I1–I8).",
  },
  {
    id: "src-pg",
    code: "N083PG",
    type: "sketch",
    titleSi: "Indikacijska skica",
    titleEn: "Indication sketch",
    unit: "Skica",
    vacId: "373413",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373413",
    fileRef: "N083PG.pdf (1 stran)",
    pages: 1,
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pg-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 1,
    lastVerified: "2026-10-07",
    noteSi:
      "Indikacijska skica prebrana (issue #17, VLM 2026-10-08, strojno branje = REVIEW): ročno risana skica z naslovom »Gemeinde Grüble« + veliko številko 83 (ujema se s signaturo N83), debel mejni mnogokotnik z rdeče oštevilčenimi točkami (~15–19), Kolpa modrikasta po vzhodnem robu z napisom »Königreich Croatien«, sosedi Weidendorf/Mallertschitsch/Pridbor [~]. NEGATIVEN REZULTAT: hišnih simbolov NI vidnih — skica za hišno-parcelno verigo ni uporabna. Lestvica [~1 W. Zoll = 1000 klafter].",
    noteEn:
      "Indication sketch read (issue #17, VLM 2026-10-08, machine reading = REVIEW): hand-drawn sketch titled »Gemeinde Grüble« + the large number 83 (matching the N83 signature), a thick boundary polygon with red-numbered points (~15–19), the Kolpa blue along the east edge inscribed »Königreich Croatien«, neighbours Weidendorf/Mallertschitsch/Pridbor [~]. NEGATIVE RESULT: NO house symbols visible — the sketch is not usable for the house–parcel chain. Scale [~1 W. inch = 1000 klafter].",
  },
  {
    id: "src-pr",
    code: "N083PR",
    type: "boundary-description",
    titleSi: "Opis meje — Grenz-Beschreibung der Gemeinde „GRÜBLE“",
    titleEn: "Boundary description of the municipality of “GRÜBLE”",
    unit: "Opis meje",
    vacId: "373414",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373414",
    fileRef: "N083PR.pdf (4 strani)",
    pages: 4,
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pr-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 10,
    lastVerified: "2026-10-08",
    noteSi:
      "Opis meje v nemščini (Kurrent) — prebrane VSE 4 strani (issue #17, VLM 2026-10-08, strojno branje = REVIEW; surovi izpis research/issue17/PR.json): naslovnica »Prod N° 218 / Grenz-Beschreibung der Gemeinde GRÜBLE«, splošne mere 1028 × 1884 klafter, točke meje št. 1–10 (prebrano na str. 2, nadaljevanje negotovo 10–20), sosedi (Kraljevina Hrvaška/Weidendorf stabilna, ostali [~]), zaključek »am 8ten April 1825«. 1028 × 1884 kl = 1210,5 jocha — se ujema s PV (<1 %).",
    noteEn:
      "Boundary description in German (Kurrent) — all 4 pages read (issue #17, VLM 2026-10-08, machine reading = REVIEW; raw output research/issue17/PR.json): title page »Prod N° 218 / Grenz-Beschreibung der Gemeinde GRÜBLE«, overall dimensions 1028 × 1884 klafter, boundary points nos. 1–10 (read on p. 2, continuation uncertain 10–20), neighbours (Kingdom of Croatia/Weidendorf stable, others [~]), closing »am 8ten April 1825«. 1028 × 1884 kl = 1210.5 joch — matches PV (<1 %).",
  },
  {
    id: "src-ps",
    code: "N083PS",
    type: "parcel-register",
    titleSi: "Seznam zemljiških parcel",
    titleEn: "Register of land parcels",
    unit: "Seznam zemljiških parcel",
    vacId: "373415",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373415",
    fileRef: "N083PS.pdf (143 strani)",
    pages: 143,
    yearFrom: 1824,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-ps-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 2974,
    lastVerified: "2026-10-12",
    noteSi:
      "143 strani zemljiških parcel po sekcijah. P36 (2026-10-11, issue #10): STROJNI PREPIS VSEH 135 strani (5–139) — 2743 strukturiranih vrstic; dokaz research/issue17/ps-raw/ + spravno poročilo PS-full.json. P38 (2026-10-11, issue #10): 3. PREHOD — eliminacijska analiza (prekrivanja z različno vsebino 0/20 + fizična sosledja) je določila 20 ciljnih strani; 20 novih VLM branj (skupaj 233) z izboljšanim pozivom na sosledje številk; dokaz ps-raw/*-pass3.json + PS-full-v2.json (2974 izbranih vrstic, adjudikacija pass3-prednost). KLJUČNO STRUKTURNO ODKRITJE P38: zvezek je organiziran po LISTIH (Blatt I, II, IIb, III, IV, V, VII, IX, X) — vsak list nosi LASTNO številčenje parcel; ista številka na različnih listih je DRUGA parcela (razlaga nemogočih prekrivanj iz P36); skupna gozdna zemlja (Waldung, brez lastnikov) je med listi; kontrolna vsota 102 + 2505 = 2607 je vsota (list, številka) parov čez vse liste, ne maksimum enega niza. Primer: str. 24 strukturno potrjena kot 421-440 (p1/p2 sta skupaj napačno brala 401-420 — sistematna zamenjava 2↔4; dokaz korelacije napak med prehodoma). NERESENE strani za človeški pregled (issue #12): 69, 85, 86, 88, 93, 128, 138 (tri medsebojno različna branja). P39 (2026-10-11, issue #10): STRUKTURNA REKONSTRUKCIJA (dokaz research/issue17/PS-reconstruction.json) — segmentacija po fizičnem vrstnem redu z lastniškim testom: 33 segmentov; VSEBINSKI DOKAZ per-list številčenja: 29/29 prekrivajočih parov strani ima za iste številke RAZLIČNE lastnike (0 ujemanj) — P36 hipoteza o napačno prebranih številkah je OVRŽENA; 2724 unikatnih (segment, številka) parov, 50 večkulturnih dodatnih vrstic, 200 vrstic z neberljivo številko; kontrolna vsota 102 + 2505 = 2607 je znotraj meje [2221, 2725] — KONSISTENTNO; eksaktna potrditev in razvrstitev preostanka (nerešene strani, morebitni fantomski obsegi) zahtevata človeški pregled (issue #12); SPRAVA (P38–P45, 2026-10-12): sekcije GRUND 1889/2505 + NADALJEVANJE 95 + WALDUNG 81 + Blatt X 60 = bauplatzeSeen P36; razdvojitev v model parcela×raba (2134 vnosov, 2632 parov, /api/atlas/ps-landuse); leksikon družin (P43), razcepi K1/K2 (P44) in leksikografska verifikacija (P45) — kartice Raziskav; uskladitev s kontrolno vsoto 2607 ostaja izrecno odprta. P55 (2026-10-14, issue #13): protokol prvič GEOLOCIRAN — 1110 vrstic (40.2 %) povezanih s sodobnimi parcelami KO 1544 po ohranjeni številki; vztrajnost oštevilčenja 1825→2026 dokazana (površine median 3.6984 ≈ 1 Wiener QK 3.59665 m², Δ +2.83 %; prostorska soslednost zaporednih številk 51.8 m vs naključno 1436.9 m — 27.8×); odkritje sekcije »Furkofze« (Fučkovci, 2 vrstici, parceli 2159/2160, Van Wawech Mihó); per-parcelno zaupanje STRONG/MEDIUM/WEAK, identifikacija posamezne parcele [~]. P56 (2026-10-13, issue #13): TOPOLOGIJA REGISTRA — register NI homogen: S1 glavni register (str. 5–127, per-Blatt), S2 spremembni register (str. 128–137, št. 2507–2840, anmerkung dodatki — »einf. Vermessung vom Jahr 1805«, »Grundsteuerkataster 1841«, vzdrževan do 1934: 584 označenih vrstic, pik 1841 s 83 vrsticami na 44 straneh), S3 zapadek »Zusammenstellung der Grundstücke« (str. 138–139, LASTNO oštevilčenje 1–100) — 43 S3 vrstic je bilo lažno povezanih v P55 (median razmerja površin 0.0892 ≪ 3.7188 — ~42× odmik; pass2/pass3 razhajanje [1..40] vs [421..440]) — sanitiran join 1110 → 1067 vrstic, 800 → 774 base; per-Blatt dvoumnost kvantificirana (515 base na več straneh, 512 vrstic dvoumnih [~], brez prerazporeditev); sodobna praznina 2507–2607 (0 parcel) dokumentirana. P57 (2026-10-13, issue #13): ZAČETEK REGISTRA PREBRAN — strani 3–4 (številke 1–40, Blatt I), ki jih P38/P56 izbora nista vključili, prebrane s ŠTIRIMI plastmi (polna ×3, kolone Haus Nro. ×3, izrezi površin ×3, tarčne celice 6× za 10 spornih) in deterministično adjudicirane; veriga Blatt I 1–60 zaprta; join obnovi 26/26 izgubljenih base P56 (25 s pari površin, median 3.7594 ≈ 1 QK 3.59665, Δ +4.53 %; soslednost 81.2 m vs kontrola 263 m); 14 številk upokojenih (brez sodobne naslednice). P58 (2026-10-14, issue #13): SANACIJA PRODUKCIJE (v2) — 43 lažnih S3 povezav odstranjenih iz runtime-a (nabor bajtno enak P56 seznamu) in 26 Blatt I vrstic dodanih iz P57 (vseh 26 lostBases) → 1093 vrstic / 800 števil; pozicije per base → soslednost in S1/S2 zaupanje bajtno enaka v1 (590/51.8/27.8×; 174/759/160); površinski median čist 3.7709 (Δ +4.85 % — v1 3.6984 je bil umetno snizan); serije BI/S1/S2 + per-Blatt dvoumnost 211 base / 495 vrstic [~]; v1 dokaz arhiviran; vsi statusi REVIEW (strojno branje ni dokazni vir). P59 (2026-10-14, issue #13): GLAVE LISTOV PREBRANE — stolpec 'Nro. des Blattes' prvič zanesljivo (levi izrez 135 strani × 2 prehoda + 32 arbitraž-oči; stari blatt stolpec potrjeno šumen — p12 ditto prebrano kot 20× 'I'): Blatt I = parcele 1–800 (str. 3–40, prehodna cona 721–800 s popravki I→II [~]), Blatt II se začne pri 801 (str. 43–92, p72 = III vmes, cona 1100–1640 prepletena z lokalnimi sekcijami); per-Blatt ločitev 211 dvoumnih base MERJENA (P62 polna pokritost 135/135): 110 čez ≥2 Blatta, 17 ruleCandidate (edina instanca v pasu razmerij [0.8, 1.25]); join v2 nespremenjen. P60 (2026-10-14, issue #13): PER-BLATT ATRIBUCIJA IZVEDENA — 17 ruleCandidate base dobi instanco v pasu [0.8, 1.25] kot attributedBlatt (II 12 · I 1 · III 4; 23 vrstic; npr. 163 → Blatt II @ 0.9813 — 4 kulture na 61/83/84/86 — vs Blatt I @ 7.0 @ p11); soslednost-kontrola 21/23 (671/934 [~] — prečrtane vrstice); pas-strani (36, 49, 61, 83–87, 94, 99) = 100 % več-stranskih base (Kultur-Tabellen re-listing [~]); unit-semantics: pas ujema modo B (ratio ≈ 1, n=62), ne modo A (≈ 3.59665 = 1 QK → m², n=226) — absolutna korespondenca ODPRTA, atribucija = relativa [~]; join v2 nespremanjen. P61 (2026-10-14, issue #13): UNIT-SEMANTICS MERJENA — moda B karakterizirana s permutacijsko kontrolo na GURS parcelah KO 1544 (2117 parcel, deterministične FNV-1a točke, radija 50/100 m, pas ±25 %): moda A real @50 0.9248 vs perm 0.1637 (ujeta = prava parcela), moda B real @50 0.2903 vs perm 0.1774 → prava parcela (QK×3.6) ni tik zraven → H1 napačni številčni join ZAVRŽEN kot glavni mehanizem; delna površina neuporabna (samo 2 base z ≥2 B vrsticami); moda B = dosledna drugačna registracijska konvencija (številka ≈ m²; 62 vrstic, 42 strani, Blatt II 32 · IV 15 · III 9 · I 5 (P62: null 5 → IV +4, II +1); bloki 3/9) — identiteta enote ODPRTA [~]; pas pravilo P59/P60 = moda B — atribucija relativa smiselna; join v2 nespremanjen. P63 (2026-10-14, issue #13): ZAKLJUČNE STRANI (138–139) PALEOGRAFSKO ZAKLJUČENE — 3 neodvisni prehodi (VLM 2× + agent-oči 4×–5×, 2-od-3 konsenz, 42 flagov [~]): p139 = Blatt IIb (pod-list NOV v strukturi) s parcelami 41–60 (duplikat Blatt I številk) + lastninske kolone (Haus Nº rdeče, 'Vor und Zuname' = številke 62–80 — ne imena; konskripcija/Einlage? [~]) + desna kultura rekapitulacija 81–100 / Classe 101–120; KOREKCIJA: prejšnja očesna razlaga 'Nro. des Hauses.' = očesna napaka (glava je 'Nro. des Blattes.') — P58 open #6 ZAPRT; p138 = izbrisana leva tabela (bledi ostanki 'T. 191'[~] @ r14) + 'Zusammenstellung der Grundstücke' (Wiese 1–20, Classe 21–40) desna;  P64 (2026-10-14, issue #13): RAZŠIRITEV PER-BLATT ATRIBUCIJE — 110 čez-Blatt base atribucija z merjeno hierarhijo pravil: R1 pas [0.8, 1.25] (P60, 17, bajtno) · R2a area-dominanca ≥ 0.75 (53: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b ena-Blatt-s-površino (1: 1605) → 71/110 atributiranih (Blatt II 42 · III 15 · I 5 · IV 5 · V 4); 39 split (delež 0.5–0.75) z alternativami po deležih — kandidati za lastniško odločitev o per-Blatt SPLIT joinu; R1↔R2 soglasje 15/17 (2 divergence: 930, 671 [~]); občutljivost praga 0.75: 24 @ ≥0.9 … 69 @ ≥0.6 (od 92 z izmerjeno površino); join v2 nespremanjen. P65 (2026-10-14, issue #13): POLNA PER-BLATT ATRIBUCIJA — 101 single-Blatt več-stranskih base atributiranih (vse vrstice na straneh istega Blatta — trivialno, R3-single: I 3 · II 26 · III 14 · IV 58; 205 vrstic) → pokritost več-stranskih base POPOLNA 211/211 (110 čez-Blatt iz P64 bajtno + 101), skupaj 172 atributiranih (Blatt II 68 · IV 63 · III 29 · I 8 · V 4) + 39 split z alternativami (lastniška odločitev o SPLIT joinu); polna pokritost registra: 800 base = 589 single-page (implicitno prek strani: I 145 · I·II 10 · II 183 · III 28 · IV 205 · V 18) + 211 multi-page; 0 vrstic brez atribucije; join v2 nespremanjen. P66 (2026-10-14, issue #13): SPLIT DECISION PACK — 39 split base odločitveni paket za per-Blatt SPLIT joina (P64 #8; NE odloča namesto lastnika — MERI in DOKAZUJE dejstva, deterministično): 39 × 2 deleža, 93 vrstic (25 × 2 + 13 × 3 + 1 × 4); pari Blattov I·II 7 · II·III 21 · II·IV 2 · IV·V 9 (sosednji 37, skok 2: 1603/1604 — isti kulturi na obeh Blattih); lastniki per Blatt DISJUNKTNI 39/39 (2–3 edinstvenih: 25/13/1) → močan dokaz, da je ista številka pod različnima Blattoma 2 RAZLIČNI realni parceli; dominantni deleži [0.50,0.60) 23 · [0.60,0.70) 11 · [0.70,0.75) 5; kulture 92 z razčlenitvijo per Blatt; GEO 39/39: vse vrstice base nosijo ENAKO geometrijo joina v2 (na nivoju številke — SPLIT bi zahteval 2 geometriji); areaSuspect 0; sosledje split del 82/93 (flag 11 — 5 base: 646, 661, 1821, 2141, 2143); P65 polja 39× bajtno; join v2 nespremanjen; odločitev LASTNIKA P67 (2026-10-14, issue #13): FORENZIČNI PAKET ANOMALIJ — (A) skok II·IV (1603/1604) = artifakt DVOJNE Kurrent zamenjave: p78 (Blatt II, Wüstung 'Pod Grabino') prave 1501–1520 (strip 2× bajtno; vrstice 5–14 rdeče prečrtane; kontinuiteta 1461–1480→1481–1500→1501–1520; karta: 1461–1500 ima 12 poligonov / 1121–1200 PRAZNO) → v2 1603–1605 napaka 5→6, prave 1503/1504/1505; p93 (Blatt IV) prave 1901–1920 (strip 2× r11–20 bajtno; karta: blok 1901–1907 ima TOČNO 7 poligonov = prečrtani blok; P38 pass1 9→0, pass2 9→6) → prave 1903/1904/1905; p87 (Blatt II) prave 1681–1700 (pass2 + oči; pass1 661–680 = izguba vodilne 1 + 8→6; strip 161–180 = odrezane vodilne) → 11 v2 vrstic napačno (+1020) z LAŽNO geometrijo (== p36 koordinate); posledica: 1603/1604/1605/661/671 = lažne fuzije — skok II·IV izgine, čez-Blatt primeri 661/671 razpadeta, p93 (IV) × p98 (III) = isti obseg 1901–1920; renumerifikacija 17 preslikav, 0 kolizij = P68; projekcija base 802, multi 208; (B) 5 sosledje flagov = artefakt obsega joina — manjkajoči sosedje obstajajo v registru (P38 z imeni), brez poligonov v karti; 1820/2140 na prejšnjih straneh; 11/11 razloženih; (C) 671 razrešena (ni divergencia — II instanca = 1691), 930 [~] z merjenim dokazom; (D) univerzalna disjunktnost lastnikov per Blatt 110/110 čez-Blatt base — ista številka pod različnima Blattoma = 2 RAZLIČNI parceli; v2 nespremanjen; renumerifikacija = P68 IZVEDENA. P68 (2026-10-14, issue #13): V3 SANACIJA ŠTEVILČENJA IZVEDENA — mehanski izvod P67 specifikacije (deterministično, brez AI ob delovanju): 17 preslikav (p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700 +1020; 0 kolizij; parzella ostaja originalno branje — sanacija le na join ključu) + re-join po P55 metodi: 14 vrstic izpada (base brez PF poligona — kartni priči P67), p93 3× re-claim na 1903/1904/1905 (poligoni JZ; 1903/1905 delita poziciji s p98 instancami III); v3: 1079 vrstic / 798 base / 199 multi-page / 98 cross-Blatt (blattDist I·II 31 · II·III 46 · III·IV 3 · IV·V 18); fuzija 1903 = III×2+IV×1 (delež 0.7081), 1905 R2b, 1904 ratio 6.8052 izven pasu; površine median 3.8512 (Δ +7.08 %), soslednost 590/51.8/28.3×; odmiki od P67 aproksimacije (802/208/107) dokumentirani [~]; veriga re-run P59–P66 s posodobljenimi pini; v2 arhiviran; SPLIT join = lastniška odločitev (P69) P69 (2026-10-15, issue #13): SISTEMSKI PREGLED P38 pass1 slojev cone p73–93 + p99 — očesna forenzika (4× široki izrezi x=0..430 + 7×–8× zoomi + kontinuiteta + karta + P56 annRecords zamiki + Blatt stolpec + hišne številke + površinska razmerja): stari sloji = sistematski digitalni artefakti (p74 1121–40=1421–40 4→1, p76 1161–81=1461–80, p77 1181–1200=1481–1500, p79 1821–42=1521–40 5→8, p80/p81 16xx=15xx 5→6, p82 1681–1700=1581–1600 — pass1 pravilen, join vzel p2, 16 vrstic izgubljenih, p88 721–740=601–620 +120, p89/p90 19xx=9xx fantom-1, p92 990–1008=981–1000 +9, p99 921–40=1921–40 −1000 zrcalno); 77 renum preslikav (0 kolizij) + 98 rejoin kandidatov = spec P70; 5 lokalnih sekcij (p83/p84/p86 161–180, p85 641–660, p88 601–620; 56 vrstic) = dokazane lažne fuzije (hiše p85 r641 Hi16 vs p35 Hi68; Σ ratio 161=235.65×) — exclude/per-Blatt = lastniška odločitev; p89/p99 zrcalni primer (Blatt stolpec razrešuje); join v3 nespremanjen. P70 (2026-10-15, issue #13): IZVEDBA P69 SPECIFIKACIJE (v4) — mehanski izvod, deterministično, brez AI ob delovanju: 77 renum preslikav (bajtno po P69; konec lažnih fuzij: p74 1121–1140→1421–1440 4→1, p76 1161–1180→1461–1480, p79 182x→152x 5→8, p80/p81 16xx→15xx 5→6, p89/p90 19xx→9xx fantom-1, p92 +9, p99 92x→192x) + 95 rejoin vrstic iz starih P38 slojev (sloji po P69; P55 normalizacija; 3 kandidati p80 1541–1543 brez vira [~]) + 29 izpada (brez poligonov); 33 fuzij isti-Blatt (dva bloka registra 921–1000: p49–52 + p89–92; SPLIT = LASTNIKA); v4: 1145 vrstic / 878 base / 215 multi / 79 cross; area median 3.8843 (Δ +8.0 %); soslednost 654/52.0/27.6×; 56 sekijskih vrstic nespremenjenih (exclude/per-Blatt = lastniška odločitev); veriga P59–P67 --check PASS; v3 arhiviran P71 (2026-10-15, issue #13): KOREKCIJE v4 — (C1) 56 sekijskih vrstic (p83–86, p88) EXCLUDE iz joina (P69 sectionClass bajtno; dokazane lažne fuzije na Blatt I poligone — Σ ratio 161 = 235.65×, lastniško prekrivanje s p11 = 0; LASTNIŠKA odločitev: opcija exclude; per-Blatt instance = odprta točka; vrstice ostanejo v registru brez geometrije; 0 poligonov ostane praznih) + (C2) P93 REVERZIJA — P68 renum 160x→190x OVRŽEN: notranja glifna forenzika (r9 = 1609 / r19 = 1619 — gotova 9 z repom ≠ srednja 6, isti pisar; kontrole p98 '1916' = 9 in 6 v istem številu, p92 981–983 verificirane 9) + annRecords anotatorja (1601–1619: 'Durch Theilung im 1824', '1870. 8-1117') + pageMap P56 + P38 pass2 — 15 vrstic base := parzella, PF ujemanja 1603/1604/1605 (prej prazni poligoni dobili prve vrstice), 12 izpadlih (base brez PF poligona); PF 1901–1920 brez lažnih dvojnih zahtevkov p93 (ostane p98 III), PF 1904/1906 izpadla iz base seta; v5: 1077 vrstic / 879 base / 184 multi-page / 48 cross-Blatt; površine median 3.9052 (Δ +8.58 %, kontrola 4.2304); soslednost 652/51.8 m/25.5×; nespremenjene vrstice bajtno == v4 (1041 + 33 group-derived); forenzični izrezi research/issue17/p93-forensics/ (7 PNG, 8–12×); skripta scripts/p71_ps_v5_sections_p93.py --check PASS (pini v4/P69/P59/P56/PARCELS); veriga P59–P67 PASS, P69 zamrznjen (v3 dokaz), P70 dokaz bajtno (runtime nasledstvo v5 deklarirano). P72 (2026-10-15, issue #13): DVOJNOSTI REGISTRA — 135 ISTI-BLATT DUAL BASE odločitveni paket za isti-Blatt SPLIT joina (P70 »SPLIT = LASTNIKA« razširjen na cel register; razširitev P66 cross-Blatt vzorca; deterministično, brez AI ob delovanju; NE odloča namesto lastnika — MERI in DOKAZUJE; v5 join nespremanjen): 135 base z vrsticami na ≥ 2 straneh ISTEGA Blatta ima med straneh DISJUNKTNE lastnike (274 vrstice; 2 tri-zapisni + 2 nearDual 2080/2081), stranski pari delijo iste številčne razpone po P56 pageMap (p23/p24 = 401–420 obe, p51/p91 = 961–980 obe, p103/p118 = 2001–2020 obe …) z odmiki po blokih konsistentnimi (40 × 44 · 15 × 49 · 5 × 29 · 1 × 13) = DVOJNI ZAPIS iste serije v dveh blokih registra; hišne številke RAZLIČNE 130/135; Σ areaQK blok A 128 125 / blok B 145 057 QK; P70 33 kolizij = PODMNOŽICA + 11 starih p51×p91 (v2 era) + 91 dozdaj neopaženih; opcija A (drop drugi-blok vrstic po C1 vzorcu): 137 izpada, 0 base brez vrstic, rows 939, multi 50, cross 48 nespr.; opcija B zahteva georef Blattnih kart [~]; opcija C neodločljiva (pageMap razponi prekrivajo); odločitev LASTNIKA; dokaz research/issue17/ps-dual-occurrence-pack.json + runtime src/data/atlas/ps-dual-occurrence-pack.json",
    noteEn:
      "143 pages of land parcels by sections. P36 (2026-10-11, issue #10): machine transcription of ALL 135 pages (5–139) — 2,743 structured rows; evidence research/issue17/ps-raw/ + the reconciliation report PS-full.json. P38 (2026-10-11, issue #10): 3rd PASS — elimination analysis (overlaps with different content 0/20 + physical adjacency) identified 20 target pages; 20 new VLM reads (233 total) with an improved continuity-aware prompt; evidence ps-raw/*-pass3.json + PS-full-v2.json (2,974 chosen rows, pass3-preferred adjudication). KEY STRUCTURAL DISCOVERY (P38): the volume is organized by SHEETS (Blatt I, II, IIb, III, IV, V, VII, IX, X) — each sheet carries its OWN parcel numbering; the same number on different sheets is a DIFFERENT parcel (explains the impossible overlaps from P36); the checksum 102 + 2,505 = 2,607 is the sum of (sheet, number) pairs across all sheets, not a single-series maximum. Example: p. 24 structurally confirmed as 421-440 (p1/p2 both misread 401-420 — a systematic 2↔4 swap; proof of correlated errors across passes). UNRESOLVED pages for human review (issue #12): 69, 85, 86, 88, 93, 128, 138 (three mutually different readings). P39 (2026-10-11, issue #10): STRUCTURAL RECONSTRUCTION (evidence research/issue17/PS-reconstruction.json) — physical-order segmentation with the owner test: 33 segments; CONTENT EVIDENCE of per-sheet numbering: 29/29 overlapping page pairs carry DIFFERENT owners for the same numbers (0 matches) — the P36 misread-numbers hypothesis is REFUTED; 2,724 unique (segment, number) pairs, 50 multi-culture extra rows, 200 rows with unreadable numbers; the checksum 102 + 2,505 = 2,607 lies within the bounds [2,221, 2,725] — CONSISTENT; exact confirmation and residual triage (unresolved pages, possible phantom ranges) require human review (issue #12); RECONCILIATION (P38–P45, 2026-10-12): the sections GRUND 1,889/2,505 + CONTINUATION 95 + WALDUNG 81 + Blatt X 60 = P36 bauplatzeSeen; the split into the parcel×culture model (2,134 entries, 2,632 pairs, /api/atlas/ps-landuse); the family lexicon (P43), the K1/K2 splits (P44) and the lexicographic verification (P45) — the Research cards; the reconciliation against the checksum 2,607 remains explicitly open. P55 (2026-10-14, issue #13): the protocol GEOLOCATED for the first time — 1,110 rows (40.2 %) linked to modern parcels of c.m. 1544 by the persisted number; the 1825→2026 numbering persistence proven (areas median 3.6984 ≈ 1 Wiener QK 3.59665 m², Δ +2.83 %; spatial adjacency of consecutive numbers 51.8 m vs shuffled 1,436.9 m — 27.8×); discovery of the »Furkofze« section (Fučkovci, 2 rows, parcels 2159/2160, Van Wawech Mihó); per-parcel confidence STRONG/MEDIUM/WEAK, per-parcel identification [~]. P56 (2026-10-13, issue #13): REGISTER TOPOLOGY — the register is NOT homogeneous: S1 main register (pp. 5–127, per-sheet), S2 changes register (pp. 128–137, nos. 2507–2840, annotated additions — »einf. Vermessung vom Jahr 1805«, »Grundsteuerkataster 1841«, maintained until 1934: 584 annotated rows, peak 1841 with 83 rows on 44 pages), S3 appendix »Zusammenstellung der Grundstücke« (pp. 138–139, OWN numbering 1–100) — 43 S3 rows were falsely linked in P55 (median area ratio 0.0892 ≪ 3.7188 — ~42× off; pass2/pass3 disagreement [1..40] vs [421..440]) — sanitized join 1,110 → 1,067 rows, 800 → 774 bases; per-sheet ambiguity quantified (515 bases on multiple pages, 512 rows ambiguous [~], no reassignments); the modern void 2507–2607 (0 parcels) documented. P57 (2026-10-13, issue #13): the REGISTER OPENING READ — pp. 3–4 (numbers 1–40, Blatt I), omitted by the P38/P56 selections, read in FOUR layers (full ×3, Haus Nro. columns ×3, area crops ×3, targeted 6× cells for 10 disputed) and deterministically adjudicated; the Blatt I chain 1–60 closed; the join restores 26/26 lostBases of P56 (25 with area pairs, median 3.7594 ≈ 1 QK 3.59665, Δ +4.53 %; adjacency 81.2 m vs control 263 m); 14 numbers retired (no modern successor). P58 (2026-10-14, issue #13): PRODUCTION SANITIZATION (v2) — 43 false S3 links removed from the runtime (the set byte-identical to the P56 list) and 26 Blatt I rows added from P57 (all 26 lostBases) → 1,093 rows / 800 numbers; per-base positions → adjacency and S1/S2 confidence byte-identical to v1 (590/51.8/27.8×; 174/759/160); clean area median 3.7709 (Δ +4.85 % — the v1 3.6984 was artificially lowered); series BI/S1/S2 + per-sheet ambiguity 211 bases / 495 rows [~]; the v1 evidence archived; all statuses REVIEW (machine reading is not evidentiary). P59 (2026-10-14, issue #13): LEAF HEADERS READ — the 'Nro. des Blattes' column read reliably for the first time (left-strip crops of 135 pages × 2 passes + 32 agent-eye arbitrations; the old blatt column confirmed noisy — p12 ditto read as 20× 'I'): Blatt I = parcels 1–800 (pp. 3–40, transition zone 721–800 with I→II corrections [~]), Blatt II starts at 801 (pp. 43–92, p72 = III in between, the 1100–1640 zone interleaved with local sections); the per-Blatt disambiguation of the 211 ambiguous bases MEASURED: 110 span ≥2 Blaetter, 17 ruleCandidates (P62 full coverage 135/135) (exactly one instance within the ratio band [0.8, 1.25]); the v2 join unchanged. P60 (2026-10-14, issue #13): PER-BLATT ATTRIBUTION EXECUTED — the 17 ruleCandidate bases get their in-band [0.8, 1.25] instance as the attributedBlatt (II 12 · I 1 · III 4; 23 rows; e.g. 163 → Blatt II @ 0.9813 — 4 cultures on 61/83/84/86 — vs Blatt I @ 7.0 @ p11); adjacency control 21/23 (671/934 [~] — crossed-out rows); the attribute pages (36, 49, 61, 83-87, 94, 99) carry 100% multi-page bases (Kultur-Tabellen re-listing [~]); unit semantics: the band matches mode B (ratio ~ 1, n=62), not mode A (~ 3.59665 = 1 QK to m2, n=226) — the absolute correspondence OPEN, the attribution = relative [~]; the v2 join unchanged. P61 (2026-10-14, issue #13): UNIT-SEMANTICS MEASURED — mode B characterized with a permutation control on the GURS parcels KO 1544 (2,117 parcels, deterministic FNV-1a points, 50/100 m, ±25 %): mode A real @50 0.9248 vs perm 0.1637 (the join = the true parcel), mode B real @50 0.2903 vs perm 0.1774 → the true parcel (QK×3.6) is not next door → the H1 wrong-number join REJECTED as the main mechanism; partial surface unusable (only 2 bases with ≥2 B rows); mode B = a consistent alternative registration convention (number ≈ m2; 62 rows, 42 pages, Blatt II 32 · IV 15 · III 9 · I 5 (P62: null 5 → IV +4, II +1); blocks 3/9) — unit identity OPEN [~]; the P59/P60 band rule = mode B — the relative attribution is sound; the v2 join unchanged. P63 (2026-10-14, issue #13): TAIL PAGES (138-139) COMPLETED PALEOGRAPHICALLY — 3 independent passes (VLM 2x + agent eyes 4x-5x, 2-of-3 consensus, 42 flags [~]): p139 = Blatt IIb (a sub-leaf NEW to the structure) with parcels 41-60 (duplicate Blatt I numbers) + owner columns (red Haus Nº, 'Vor und Zuname' = numbers 62-80 — not names; conscription/Einlage? [~]) + the right-page culture recap 81-100 / Classe 101-120; CORRECTION: the earlier 'Nro. des Hauses.' reading was an eye error (the header is 'Nro. des Blattes.') — P58 open #6 CLOSED; p138 = an erased left table (faint remains 'T. 191'[~] @ r14) + 'Zusammenstellung der Grundstuecke' (Wiese 1-20, Classe 21-40) right;  P64 (2026-10-14, issue #13): PER-BLATT ATTRIBUTION EXTENDED — all 110 cross-Blatt bases attributed with a measured rule hierarchy: R1 band [0.8, 1.25] (P60, 17, byte-identical) · R2a area dominance >= 0.75 (53: II 29 · III 11 · IV 5 · I 4 · V 4) · R2b single-Blatt-with-area (1: 1605) -> 71/110 attributed (Blatt II 42 · III 15 · I 5 · IV 5 · V 4); 39 splits (share 0.5-0.75) with per-share alternatives — candidates for the owner decision on the per-Blatt SPLIT join; R1-vs-R2 agreement 15/17 (2 divergences: 930, 671 [~]); threshold sensitivity 0.75: 24 @ >=0.9 … 69 @ >=0.6 (of 92 with measured area); the v2 join unchanged. P65 (2026-10-14, issue #13): FULL PER-BLATT ATTRIBUTION — the 101 single-Blatt multi-page bases attributed (all rows on pages of the same Blatt — trivial, R3-single: I 3 · II 26 · III 14 · IV 58; 205 rows) -> multi-page coverage COMPLETE 211/211 (110 cross-Blatt from P64 byte-identical + 101), 172 attributed in total (Blatt II 68 · IV 63 · III 29 · I 8 · V 4) + 39 splits with alternatives (owner decision on the SPLIT join); full register coverage: 800 bases = 589 single-page (implicit via the page: I 145 · I·II 10 · II 183 · III 28 · IV 205 · V 18) + 211 multi-page; 0 rows without attribution; the v2 join unchanged. P66 (2026-10-14, issue #13): SPLIT DECISION PACK — the decision pack for the per-Blatt SPLIT join over the 39 split bases (P64 #8; it does NOT decide on behalf of the owner — it MEASURES and PROVES the facts, deterministic): 39 × 2 shares, 93 rows (25 × 2 + 13 × 3 + 1 × 4); Blatt pairs I·II 7 · II·III 21 · II·IV 2 · IV·V 9 (adjacent 37, skips 2: 1603/1604 — same cultures on both Blatts); owners per Blatt DISJOINT 39/39 (2–3 unique: 25/13/1) -> strong evidence that the same number under different Blatts is 2 DIFFERENT real parcels; dominant shares [0.50,0.60) 23 · [0.60,0.70) 11 · [0.70,0.75) 5; cultures 92 with the per-Blatt partition; GEO 39/39: all rows of a base carry the SAME join-v2 geometry (at the number level — a SPLIT would require 2 geometries); areaSuspect 0; adjacency split part 82/93 (11 flags — 5 bases: 646, 661, 1821, 2141, 2143); the P65 fields byte-identical 39×; the v2 join unchanged; the decision belongs to the OWNER P67 (2026-10-14, issue #13): ANOMALY FORENSICS PACK — (A) the II·IV skip (1603/1604) = a double Kurrent substitution artifact: p78 (Blatt II, Wuestung 'Pod Grabino') true 1501–1520 (strip 2 passes byte-exact; rows 5–14 red-crossed; continuity 1461–1480→1481–1500→1501–1520; map: 1461–1500 has 12 polygons / 1121–1200 EMPTY) → v2 1603–1605 error 5→6, true 1503/1504/1505; p93 (Blatt IV) true 1901–1920 (strip 2 passes r11–20 byte-exact; map: block 1901–1907 has EXACTLY 7 polygons = the crossed block; P38 pass1 9→0, pass2 9→6) → true 1903/1904/1905; p87 (Blatt II) true 1681–1700 (pass2 + eyes; pass1 661–680 = lost leading 1 + 8→6; strip 161–180 = clipped leading digits) → 11 v2 rows wrong (+1020) with FALSE geometry (== p36 coordinates); consequence: 1603/1604/1605/661/671 = false fusions — the II·IV skip dissolves, the cross-Blatt pairs 661/671 collapse, p93 (IV) × p98 (III) = the same range 1901–1920; renumbering 17 mappings, 0 collisions = P68; projection bases 802, multi 208; (B) the 5 adjacency flags = a join-scope artifact — the missing neighbours exist in the register (P38 with names), without map polygons; 1820/2140 on the previous pages; 11/11 explained; (C) 671 resolved (not a divergence — the II instance = 1691), 930 [~] with measured evidence; (D) universal owner disjointness per Blatt 110/110 cross-Blatt bases — the same number under different Blatts = 2 DIFFERENT parcels; the v2 join unchanged; the renumbering = P68 REALIZED. P68 (2026-10-14, issue #13): THE v3 RENUMBERING SANITATION REALIZED — a mechanical derivation of the P67 specification (deterministic, no AI at runtime): 17 mappings (p78 160x→150x, p93 160x→190x, p87 661–680→1681–1700 +1020; 0 collisions; parzella keeps the original reading — the sanitation touches only the join key) + re-join by the P55 method: 14 rows dropped (base without a PF polygon — the P67 map witnesses), p93 3× re-claim on 1903/1904/1905 (south-west polygons; 1903/1905 share positions with the p98 III instances); v3: 1,079 rows / 798 bases / 199 multi-page / 98 cross-Blatt (blattDist I·II 31 · II·III 46 · III·IV 3 · IV·V 18); fusion 1903 = III×2+IV×1 (share 0.7081), 1905 R2b, 1904 ratio 6.8052 out of band; areas median 3.8512 (Δ +7.08 %), adjacency 590/51.8/28.3×; deviations from the P67 approximation (802/208/107) documented [~]; the re-run chain P59–P66 with updated pins; v2 archived; SPLIT join = owner decision (P69) P69 (2026-10-15, issue #13): THE SYSTEMATIC REVIEW OF THE P38 pass1 LAYERS, zone p73–93 + p99 — ocular forensics (4× wide crops x=0..430 + 7×–8× zooms + continuity + the map + P56 annRecords offsets + the Blatt column + house numbers + area ratios): the old layers = systematic digital artifacts (p74 1121–40=1421–40 4→1, p76 1161–81=1461–80, p77 1181–1200=1481–1500, p79 1821–42=1521–40 5→8, p80/p81 16xx=15xx 5→6, p82 1681–1700=1581–1600 — pass1 correct, the join took p2, 16 rows lost, p88 721–740=601–620 +120, p89/p90 19xx=9xx phantom-1, p92 990–1008=981–1000 +9, p99 921–40=1921–40 −1000 mirror); 77 renumber mappings (0 collisions) + 98 re-join candidates = the P70 spec; 5 local sections (p83/p84/p86 161–180, p85 641–660, p88 601–620; 56 rows) = proven false fusions (houses p85 r641 H16 vs p35 H68; Σ ratio 161=235.65×) — exclude/per-Blatt = the owner decision; the p89/p99 mirror case (the Blatt column resolves it); the v3 join unchanged. P70 (2026-10-15, issue #13): THE P69 SPECIFICATION REALIZED (v4) — a mechanical derivation, deterministic, no AI at runtime: 77 renumber mappings (byte-equal to P69; end of the false fusions: p74 1121–1140→1421–1440 4→1, p76 1161–1180→1461–1480, p79 182x→152x 5→8, p80/p81 16xx→15xx 5→6, p89/p90 19xx→9xx phantom-1, p92 +9, p99 92x→192x) + 95 rows re-joined from the old P38 layers (layers per P69; P55 normalization; 3 candidates p80 1541–1543 without a source [~]) + 29 dropped (no polygons); 33 same-Blatt fusions (the register holds 921–1000 in two blocks: p49–52 + p89–92; SPLIT = the OWNER's); v4: 1145 rows / 878 bases / 215 multi / 79 cross; area median 3.8843 (Δ +8.0 %); adjacency 654/52.0/27.6×; 56 section rows unchanged (exclude/per-Blatt = the owner's decision); the P59–P67 chain --check PASS; v3 archived P71 (2026-10-15, issue #13): THE v4 CORRECTIONS — (C1) 56 section rows (p83–86, p88) EXCLUDED from the join (P69 sectionClass byte-equal; proven false fusions onto Blatt I polygons — Σ ratio 161 = 235.65×, owner overlap with p11 = 0; the OWNER's decision: the exclude option; per-Blatt instances = open; the rows stay in the register without geometry; 0 polygons left empty) + (C2) THE P93 REVERSION — the P68 renum 160x→190x REFUTED: the within-page glyph forensics (r9 = 1609 / r19 = 1619 — the certain 9 with a descender ≠ the middle 6, same scribe; controls p98 '1916' = 9 and 6 in the same number, p92 981–983 verified 9s) + the annotator's annRecords (1601–1619: 'Durch Theilung im 1824', '1870. 8-1117') + the P56 pageMap + P38 pass2 — 15 rows base := parzella, PF matches 1603/1604/1605 (previously empty polygons got their first rows), 12 dropped (base without a PF polygon); PF 1901–1920 free of p93's false double claims (p98 III remains), PF 1904/1906 dropped from the base set; v5: 1,077 rows / 879 bases / 184 multi-page / 48 cross-Blatt; areas median 3.9052 (Δ +8.58 %, control 4.2304); adjacency 652/51.8 m/25.5×; unchanged rows byte-identical to v4 (1,041 + 33 group-derived); the forensic crops research/issue17/p93-forensics/ (7 PNG, 8–12×); the script scripts/p71_ps_v5_sections_p93.py --check PASS (pins v4/P69/P59/P56/PARCELS); the chain P59–P67 PASS, P69 frozen (the v3 proof), P70 proof byte-equal (the runtime succession v5 declared). P72 (2026-10-15, issue #13): REGISTER DUAL OCCURRENCES — 135 SAME-BLATT DUAL BASES, the decision pack for the same-Blatt SPLIT join (P70 \"SPLIT = OWNER\" extended to the whole register; extending the P66 cross-Blatt pattern; deterministic, no AI at runtime; does NOT decide on behalf of the owner — MEASURES and PROVES; the v5 join unchanged): 135 bases with rows on ≥ 2 pages of the SAME Blatt have DISJOINT owners across those pages (274 rows; 2 triples + 2 near-duals 2080/2081), page pairs share the same number ranges per the P56 pageMap (p23/p24 = 401–420 both, p51/p91 = 961–980 both, p103/p118 = 2001–2020 both …) with consistent per-block gaps (40 × 44 · 15 × 49 · 5 × 29 · 1 × 13) = DUAL ENTRY of the same series in two register blocks; house numbers DIFFERENT 130/135; Σ areaQK block A 128 125 / block B 145 057 QK; the P70 33 collisions are a SUBSET + 11 old p51×p91 (v2 era) + 91 previously unnoticed; option A (drop second-block rows per the C1 pattern): 137 dropped, 0 bases left empty, rows 939, multi 50, cross 48 unchanged; option B requires georeferenced Blatt sheets [~]; option C undecidable (pageMap ranges overlap); the decision belongs to the OWNER; evidence research/issue17/ps-dual-occurrence-pack.json + runtime src/data/atlas/ps-dual-occurrence-pack.json",
  },
  {
    id: "src-pt",
    code: "N083PT",
    type: "building-protocol",
    titleSi: "Protokol stavbnih parcel — Protocoll der Bau Parcellen der Gemeinde „GRÜBLE“",
    titleEn: "Protocol of building parcels of the municipality of “GRÜBLE”",
    unit: "Seznam stavbnih parcel",
    vacId: "373416",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373416",
    fileRef: "N083PT.pdf (8 strani)",
    pages: 8,
    yearFrom: 1825,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pt-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 84,
    lastVerified: "2026-10-11",
    noteSi:
      "Glavni vir hišnega registra ~1825: hišne številke 1–99 z lastniki in parcelnimi sklici. Issue #17: pregled 101 vrstice (81 potrjenih, 15 popravkov, 4 manjkajoče). P3 paleografska preverba (2. krog, 2026-10-08): popravki APLICIRANI — 84 stavbnih vrstic (renumeracija str. 4: hiše 35–40, prečrtana dvojnica 34, hiša 41 ne obstaja; lastniki Veith/Lebing/Bödig/Brinig/Strauß/Ihmeyer/Zollamt; dodane vrstice 7/71½/76½/99). P43 (2026-10-11, issue #13): PRVA CELOTA VERIGA PT→PUA→PS sestavljena (kompozicija W-mostu P5-c + verige P41, dokaz research/issue13/chain-full-pt-ps.json, 105 vrstic nič-zgube): od 84 hiš 2 DOKAZANI (Milleg Hans W.29) + 5 VERJETNIH (Štunidat/Hlebetz/Brinig) + 4 MOGOČE, 6 hiš s priimkovno korroboracijo čez W; križna potrditev korpusa izbranih PS branj s P41: 65/65 Točno; PT-stranski houseRefs v ATLAS_OWNERS (mešano številčenje prve gradnje) izrecno izven verige. Statusi ostajajo REVIEW (strojno branje; dokončna potrditev = človeška paleografija #12).",
    noteEn:
      "Primary source of the ~1825 house register: house numbers 1–99 with owners and parcel references. Issue #17: review of 101 rows (81 confirmed, 15 corrections, 4 missing). P3 palaeographic verification (2nd pass, 2026-10-08): corrections APPLIED — 84 building rows (the p. 4 renumbering: houses 35–40, the struck duplicate 34, house 41 does not exist; owners Veith/Lebing/Bödig/Brinig/Strauß/Ihmeyer/Zollamt; added rows 7/71½/76½/99). P43 (2026-10-11, issue #13): FIRST FULL CHAIN PT→PUA→PS assembled (composition of the P5-c W-bridge + the P41 chain, evidence research/issue13/chain-full-pt-ps.json, 105 zero-loss rows): of 84 houses 2 PROVEN (Milleg Hans W.29) + 5 LIKELY (Štunidat/Hlebetz/Brinig) + 4 POSSIBLE, 6 houses with surname corroboration across W; corpus cross-check of the selected PS readings against P41: 65/65 EXACT; the PT-side houseRefs in ATLAS_OWNERS (first-build mixed numbering) explicitly excluded from the chain. Statuses stay REVIEW (machine reading; final confirmation = human palaeography #12).",
  },
  {
    id: "src-pua",
    code: "N083PUA",
    type: "owner-register",
    titleSi: "Abecedni seznam lastnikov zemljišč",
    titleEn: "Alphabetical register of land owners",
    unit: "Abecedni seznam lastnikov zemljišč",
    vacId: "373417",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373417",
    fileRef: "N083PUA.pdf (49 strani)",
    pages: 49,
    yearFrom: 1825,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pua-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 101,
    lastVerified: "2026-10-08",
    noteSi:
      "Lastniki po abecedi s hišnimi številkami in parcelami po sekcijah I–V. DEJANSKO STANJE (issue #4, 2026-10-10): register prebran V CELIOTI — 49/49 strani. Strani A–B (21 lastnikov) iz prve gradnje so v lastniškem modelu (ATLAS_OWNERS prek PT navzkrižij); strani 3–49 (101 vrstic) v PUA_CONTINUATION (research/issue17/PUA-more.json + P3 str. 11 + P4 str. 12–34 + P5-b str. 35–49; surovi izpisi research/p3/pua-raw/, 38 datotek). KLJUČNA UGOTOVITEV P4: PUA in PT uporabljata RAZLIČNO številčenje hiš [~] (PUA hiša 6 = Höflehner, PT hiša 6 = Tilel Miho) — povezave po sami hišni št. NISO dovoljene. NAPAKA POPRAVLJENA (issue #4): prejšnja opomba je navajala »43 vnosov na 11/49 strani, strani 12–49 TO_COLLECT« — stanje po P3, pred branjem P4/P5-b. Vsi statusi REVIEW (strojno branje ni dokazni vir).",
    noteEn:
      "Owners alphabetically with house numbers and parcels by sections I–V. ACTUAL STATE (issue #4, 2026-10-10): the register read IN FULL — 49/49 pages. Pages A–B (21 owners) from the first build live in the owners model (ATLAS_OWNERS via PT cross-checks); pages 3–49 (101 rows) in PUA_CONTINUATION (research/issue17/PUA-more.json + P3 p. 11 + P4 pp. 12–34 + P5-b pp. 35–49; raw outputs research/p3/pua-raw/, 38 files). KEY P4 FINDING: PUA and PT use DIFFERENT house numbering [~] (PUA house 6 = Höflehner, PT house 6 = Tilel Miho) — links by house number alone are NOT allowed. CORRECTED (issue #4): the previous note claimed »43 entries over 11/49 pages, pages 12–49 TO_COLLECT« — the state after P3, before the P4/P5-b reading. All statuses REVIEW (machine reading is not evidentiary).",
  },
  {
    id: "src-pv",
    code: "N083PV",
    type: "land-use",
    titleSi: "Izkaz rabe zemljišč",
    titleEn: "Statement of land use",
    unit: "Izkaz rabe zemljišč",
    vacId: "373418",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373418",
    fileRef: "N083PV.pdf (1 stran)",
    pages: 1,
    yearFrom: 1825,
    yearTo: 1825,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pv-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 10,
    lastVerified: "2026-10-08",
    noteSi:
      "Izkaz rabe tal PREBRAN v celoti (issue #17, VLM 2026-10-08, vsaka izpolnjena celica potrjena ≥2 klicoma; surovi izpis research/issue17/PV.json): tiskan obrazec »AUSWEIS über die Benützungsart des Bodens«, Provinz Illyrien, [~Kreis Neustadtl], datum »den 10 Jenner 1825«. 10 izpolnjenih vrstic kultur (20 vrstic obrazca) + 2 vsoti: ganze Area 1148 j 539 kl + strnjena 73 j 1024 kl = skupaj 1221 [~1225] j 1513 [~1563] kl ≈ 703 ha (≈ sodobna k.o. Griblje 7,0 km²). Presenetljivo: vrstica Wälder (gozd) je PRAZNA — dominira 636 joch pašnikov. Aritmetika ±1 joch (dokumentirana odstopanja). OPOMBA (issue #4): 71-stranski cenilni elaborat pripada PZ, ne tej enoti (prejšnja zmeda opomb odpravljena).",
    noteEn:
      "Statement of land use READ in full (issue #17, VLM 2026-10-08, every filled cell confirmed by ≥2 calls; raw output research/issue17/PV.json): printed form »AUSWEIS über die Benützungsart des Bodens«, Provinz Illyrien, [~Kreis Neustadtl], dated »den 10 Jenner 1825«. 10 filled culture rows (20 form rows) + 2 totals: ganze Area 1148 j 539 kl + compact 73 j 1024 kl = grand 1221 [~1225] j 1513 [~1563] kl ≈ 703 ha (≈ the modern k.o. Griblje 7.0 km²). Striking: the Wälder (forest) row is EMPTY — 636 joch of pasture dominate. Arithmetic ±1 joch (documented deviations). NOTE (issue #4): the 71-page valuation elaborate belongs to PZ, not to this unit (the earlier note mix-up resolved).",
  },
  {
    id: "src-pz",
    code: "N083PZ",
    type: "valuation",
    titleSi: "Katastrski cenilni elaborat",
    titleEn: "Cadastral valuation elaborate",
    unit: "Katastrski cenilni elaborat",
    vacId: "373419",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=373419",
    fileRef: "N083PZ.pdf (71 strani)",
    pages: 71,
    yearFrom: 1825,
    yearTo: 1830,
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    thumb: "/atlas/n83-pz-thumb.jpg",
    transferStatus: "TRANSFERRED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 11,
    lastVerified: "2026-10-12",
    noteSi:
      "Cenilni elaborat 71 strani. DEJANSKO STANJE (P44, issue #11, 2026-10-12, dokaz: research/issue11/pz-classes-full.json + pz-raw/, 76 VLM klicev): PREBRAN V CELIOTI — 71/71 strani (12 vzorčenih issue #4 + 64 strani P44: 1. krog str. 4–67 + 12 ciljnih ponovnih branj). REKAPITULACIJA (str. 67, Specifischer Ausweis der Endresultate): 10 vrstic razredov + Summa 1152 j 495 kl; Brutto 8872 fl 5¾ kr; Rein 4492 fl 51 kr. Ključne vrednosti: Acker I 80 j 842 kl (korroborirano s str. 12: 80 j 974 kl [~]) + II 334 j 120 kl [~] (adjudicirano: izrez 1,6× prepona Kurrent »3«, aritmetika vrstic 1145 ≈ Summa 1152 in PV Acker 413); Wiesen I/II 15+29 j; Weingärten 7 j (= PV); Hutweiden 118 + Weiden mit Holznutzung 558 j (negativen Rein-Ertrag/joch); Bauarea 1 j. USKLDITEV s PV: Summa 1152 j ≈ PV erste Summe 1148 j (+4 ≈ 0,3 %); str. 65 nadzorna opomba »Weiden gesamt 636 j 263 kl« = PV NATANČNO. Zgodovinska divergenca str. 50 (Acker I) RAZREŠENA: Rob 25 fl 44 kr (prečrtani 20 fl 44 nadomešča) − Anschlag 10 fl 40½ = Rein 15 fl 3½ ≈ zapisani 15 fl 5 kr. Odprto (za paleografijo #12): Δ 7 j med vsoto vrstic in Summo, Weingärten klaftri 42/665, Bauarea 1/4 j. Vsi statusi REVIEW (strojno branje ni dokazni vir).",
    noteEn:
      "Valuation elaborate, 71 pages. ACTUAL STATE (P44, issue #11, 2026-10-12, evidence: research/issue11/pz-classes-full.json + pz-raw/, 76 VLM calls): READ IN FULL — 71/71 pages (12 sampled by issue #4 + 64 pages by P44: pass 1 over pp. 4–67 + 12 targeted re-reads). RECAPITULATION (p. 67, Specifischer Ausweis der Endresultate): 10 class rows + Summa 1152 j 495 kl; gross 8872 fl 5¾ kr; net 4492 fl 51 kr. Key values: Acker I 80 j 842 kl (corroborated by p. 12: 80 j 974 kl [~]) + II 334 j 120 kl [~] (adjudicated: the 1.6× crop reads the Kurrent »3«, the row arithmetic 1145 ≈ Summa 1152 and PV Acker 413 agree); Wiesen I/II 15+29 j; Weingärten 7 j (= PV); Hutweiden 118 + Weiden mit Holznutzung 558 j (negative net yield/joch); Bauarea 1 j. RECONCILIATION with PV: Summa 1152 j ≈ PV erste Summe 1148 j (+4 ≈ 0.3 %); the p. 65 control note »Weiden gesamt: 636 j 263 kl« = PV EXACTLY. The historical p. 50 divergence (Acker I) RESOLVED: gross 25 fl 44 kr (the struck-through 20 fl 44 is superseded) − assessment 10 fl 40½ = net 15 fl 3½ ≈ the written 15 fl 5 kr. Open (for palaeography #12): a Δ of 7 j between the row sum and the Summa, the Weingärten klafter 42/665, Bauarea 1/4 j. All statuses REVIEW (machine reading is not evidentiary).",
  },
  // Zunanji registri in poznejši viri — jasno ločeni od N83
  {
    id: "src-as749",
    code: "SI AS 749/3/8/12",
    type: "archival-mention",
    titleSi:
      "Izpisek zemljiških parcel iz katastrskih davčnih vpisnikov za davčne občine Vinji Vrh, Kot, Griblje, Kaltersberg, Loka, Petrova vas in Krasinec v gospostvih Krupa in Pobrežje za namene zemljiške odveze",
    titleEn:
      "Extract of land parcels from the cadastral tax registers for the tax municipalities of Vinji Vrh, Kot, Griblje, Kaltersberg, Loka, Petrova vas and Krasinec in the lordships of Krupa and Pobrežje for the purposes of land release",
    vacId: "4971617",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=4971617",
    yearFrom: 1851,
    yearTo: 1853,
    fund: "SI AS 749 Gospostva Krupa, Pobrežje in Pusti Gradac (1587–1901)",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (konec nedostopnosti 31. 12. 1900)",
    licenceEn: "publicly accessible (closure ended 31 Dec 1900)",
    transferStatus: "NOT_DIGITIZED",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "Potrjena enota v VAČ (2 zvezka, nemški Kurrent, prejšnja signatura fasc. 58). Enota je javno dostopna, a NI digitalizirana — vpogled le v čitalnici Arhiva RS. Vir za kasnejšo plast 1851–1853 in povezavo parcel skozi čas; digitalizacija je predlagan naslednji korak (TO_COLLECT).",
    noteEn:
      "Confirmed unit in VAČ (2 volumes, German Kurrent, previous signature fasc. 58). Publicly accessible but NOT digitized — consultation in the Arhiv RS reading room only. Source for the later 1851–1853 layer and parcel links through time; digitisation is the proposed next step (TO_COLLECT).",
  },
  {
    id: "src-as1138",
    code: "SI AS 1138/I/1204",
    type: "archival-mention",
    titleSi: "Katastrska občina Griblje — katastrski načrt (katastrski okraj Črnomelj, 1952)",
    titleEn: "Cadastral municipality Griblje — cadastral plan (Črnomelj district, 1952)",
    vacUrl: "https://vac.sjas.gov.si/vac/search/fieldSearch",
    yearFrom: 1952,
    yearTo: 1952,
    fund: "SI AS 1138",
    archive: "Arhiv Republike Slovenije",
    licenceSi: "javno dostopno (VAČ)",
    licenceEn: "publicly accessible (VAČ)",
    transferStatus: "TO_COLLECT",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 0,
    lastVerified: "2026-10-07",
    noteSi:
      "Povojni reambulirani katastrski načrt — pripravljen kot kasnejša plast za primerjavo 1825 → 1952 → danes. Natančna VAČ enota še ni identificirana (iskanje fieldSearch, TO_COLLECT).",
    noteEn:
      "Post-war reambulated cadastral plan — prepared as a later layer for the 1825 → 1952 → today comparison. The exact VAČ unit is not identified yet (fieldSearch lookup, TO_COLLECT).",
  },
  {
    id: "src-esd",
    code: "GISKD/EŠD",
    type: "heritage-register",
    titleSi: "Register nepremične kulturne dediščine (EŠD)",
    titleEn: "Register of immovable cultural heritage (EŠD)",
    vacUrl: "https://giskd.gov.si/egk",
    fund: "GISKD — Geografski informacijski sistem kulturne dediščine",
    archive: "Ministrstvo za kulturo RS",
    licenceSi: "javni register",
    licenceEn: "public register",
    transferStatus: "NOT_APPLICABLE",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 5,
    lastVerified: "2026-10-07",
    noteSi:
      "Identificirane enote za območje Griblje (uradno preverjene 2026-10-07 prek iskalnika EID): EŠD 2122 (Griblje — cerkev sv. Vida, spomenik lokalnega pomena), EŠD 19324 (Cerkvišče — spomenik NOB) in EŠD 19326 (Griblje — spomenik NOB, registrirana dediščina), EŠD 11118 (Podzemelj — arheološko najdišče Kučar, občina Metlika, spomenik lokalnega pomena) ter EŠD 10094 (Griblje — arheološko najdišče ob Kolpi, registrirana dediščina). Kučar (11118) in najdišče ob Kolpi (10094) sta dve ločeni enoti. Ločen sodoben uraden sloj.",
    noteEn:
      "Units identified for the Griblje area (officially verified 2026-10-07 via the EID search): EŠD 2122 (Griblje — Church of St. Vitus, local heritage monument), EŠD 19324 (Cerkvišče — WWII memorial) and EŠD 19326 (Griblje — WWII memorial, registered heritage), EŠD 11118 (Podzemelj — Kučar archaeological site, Municipality of Metlika, local heritage monument) and EŠD 10094 (Griblje — archaeological site by the Kolpa, registered heritage). Kučar (11118) and the Kolpa site (10094) are two separate units. A separate modern official layer.",
  },
  {
    id: "src-vac-n83",
    code: "SI AS 176/N/N83",
    type: "archival-mention",
    titleSi: "VAČ — arhivska enota N83 Griblje, k.o. (potrditev identitete listov)",
    titleEn: "VAČ — archival unit N83 Griblje, c.m. (sheet identity confirmation)",
    unit: "celotna enota grafičnega gradiva",
    vacId: "227663",
    vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=227663",
    fund: "SI AS 176 Franciscejski kataster za Kranjsko (1823–1869) → N Novomeška kresija → N83 Griblje, k.o.",
    archive: "Arhiv Republike Slovenije (prek VAČ — Virtualne arhivske čitalnice)",
    licenceSi: "javno dostopno, dovoljenje ni potrebno (VAČ)",
    licenceEn: "publicly accessible, no permission required (VAČ)",
    transferStatus: "NOT_APPLICABLE",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 0,
    lastVerified: "2026-10-08",
    noteSi:
      "P10 (2026-10-08): uradna arhivska potrditev identitete listov — k.o. Griblje = št. 83 (prejšnja signatura N083A, zgodovinsko ime Grüble); enota vsebuje NATANČNO 5 listov (N083A01–A05 = naši A01–A05) + spisovno gradivo; podrejena raven »grafični«. IDENTITETA NEODVISNO POTRJENA: baza križnih korelacij med VAČ predogledi (zajeti s strani) in našimi skeni — diagonala (A03↔A03 0,53; A04↔A04 0,44; A05↔A05 0,51) dokazuje skladno številčenje. VAČ nudi tudi tok JPG (fileStream, docid 9) — polne ločljivosti za javnost prek registracije (celotne slike zahtevajo prijavo; predogledi 520×418).",
    noteEn:
      "P10 (2026-10-08): the official archive confirmation of the sheets' identity — c.m. Griblje = no. 83 (former signature N083A, historical name Grüble); the unit contains EXACTLY 5 sheets (N083A01–A05 = our A01–A05) + written records; sub-level »grafični«. IDENTITY INDEPENDENTLY CONFIRMED: a cross-correlation matrix between VAČ previews (captured on site) and our scans — a clear diagonal (A03↔A03 0.53; A04↔A04 0.44; A05↔A05 0.51) proves the numbering is consistent. VAČ also offers a JPG stream (fileStream, docid 9) — full resolution publicly via registration (complete images require a login; previews 520×418).",
  },
  {
    id: "src-gurs-wfs",
    code: "GURS WFS (ipi.eprostor.gov.si)",
    type: "archival-mention",
    titleSi: "GURS WFS — uradni sloji k.o., parcel in naselij (CORROBORATING)",
    titleEn: "GURS WFS — official layers of c.m.s, parcels and settlements (CORROBORATING)",
    vacUrl: "https://ipi.eprostor.gov.si/wfs-si-gurs-kn/wfs?request=GetCapabilities",
    fund: "Kataster nepremičnin / Register prostorskih enot (javni spletni servisi GURS)",
    archive: "Geodetska uprava Republike Slovenije",
    licenceSi: "javni dostop, CC BY 4.0 (pogoji GURS)",
    licenceEn: "public access, CC BY 4.0 (GURS terms)",
    transferStatus: "NOT_APPLICABLE",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 0,
    lastVerified: "2026-10-08",
    noteSi:
      "P10 (2026-10-08): odkriti javni WFS končne točke GURS: wfs-si-gurs-kn (KATASTRSKE_OBCINE, PARCELE, GRADBENE_PARCELE…) in wfs-si-gurs-rpe (NASELJA, OBČINE…), EPSG:3794 (D96/TM). Preneseno: POLIGON k.o. GRIBLJE (SIFKO 1544, 550 oglišč; 15,2665–15,3009 E, 45,5442–45,5859 N), 2117 parcel k.o. 1544 (od tega ~660 stavbnih <800 m²), 2432 parcel k.o. Adlešiči (1552) v ciljnem okviru, poligoni 8 naselij (Griblje, Krasinec, Cerkvišče, Dragoši, Fučkovci, Jankoviči, Bedenj, Tribuče) + 10 k.o. regije. UPORABA: (1) sodobna stavbna sidra za validacijo georeferenc listov (P10); (2) uradna meja k.o. kot referenčni okvir; (3) kartni seznam naselij za identifikacije (Pri Jankovichti → Jankoviči ✓). Artefakti: research/georef-n83/gurs/.",
    noteEn:
      "P10 (2026-10-08): public GURS WFS endpoints discovered: wfs-si-gurs-kn (KATASTRSKE_OBCINE, PARCELE, GRADBENE_PARCELE…) and wfs-si-gurs-rpe (NASELJA, OBČINE…), EPSG:3794 (D96/TM). Downloaded: the c.m. GRIBLJE polygon (SIFKO 1544, 550 vertices; 15.2665–15.3009 E, 45.5442–45.5859 N), 2117 parcels of c.m. 1544 (of which ~660 building parcels <800 m²), 2432 parcels of c.m. Adlešiči (1552) in the target frame, polygons of 8 settlements (Griblje, Krasinec, Cerkvišče, Dragoši, Fučkovci, Jankoviči, Bedenj, Tribuče) + 10 regional c.m.s. USE: (1) modern building anchors for sheet-georeference validation (P10); (2) the official c.m. boundary as a reference frame; (3) the settlement gazetteer for identifications (Pri Jankovichti → Jankoviči ✓). Artefacts: research/georef-n83/gurs/.",
  },
  {
    id: "src-ezkn",
    code: "eZKN (geohub.gov.si)",
    type: "archival-mention",
    titleSi: "eZKN — pregledovalnik arhivskih načrtov GURS/ARS (SEKCIJSKA MREŽA 1:2880)",
    titleEn: "eZKN — the GURS/ARS archive plan viewer (the 1:2880 SECTION GRID)",
    vacUrl: "https://geohub.gov.si/ghapp/ezkn/index.html",
    fund: "eZKN 1.0 (2018) — ZKN GURS + indikacijski načrti franciscejskega/reambulančnega katastra ARS",
    archive: "Geodetska uprava RS + Arhiv RS",
    licenceSi: "javni dostop (JPG/DjVu); ARS gradivo v nižji ločljivosti",
    licenceEn: "public access (JPG/DjVu); ARS material in lower resolution",
    transferStatus: "NOT_APPLICABLE",
    georefStatus: "NOT_APPLICABLE",
    structuredEntries: 0,
    lastVerified: "2026-10-08",
    noteSi:
      "P10 (2026-10-08) — KLJUČNA RAZKRITJA: (1) SEKCIJSKA MREŽA 1:2880 z URADNO geometrijo (sloj GURS/EZKN_LISTI/8000): celice ~1,9×1,5 km, kodirane IX24+2 črki (stolpci a–d, vrstice e–i); OKVIRJENE OZNAKE NAŠIH LISTOV SO KODI CELIC: A02=»O.IX24cƒ«→celica cf (središče se NATANČNO ujema s središčem vsebine A02!), A03=»O.IX24dg«→celica dg, A04=»O.IX24cg«→celica cg (POPRAVEK P9!), A05=»O.IX24ch«→celica ch. (2) ZAPIS N83-1544 (Stanje 20 — Franciscejski kataster ARS): POVEZAVAJPG = VAČ fileStream (uodid 227663, docid 9), IME = »SI AS 176/N/N83«, koordinatni sistem »Schockell, Gellert in Krim«. (3) JAVNE DJVU/JPG slike ZKN listov (GRIBLJE 1/2/4/K 2–3, ~1970–2005, 300 dpi; prek /gurs/ezknpodatki/) — preneseni in dekodirani (libdjvulibre) za primerjavo vsebin. Zavrnjeno: Mapire/Arcanum (403 s sandboxa).",
    noteEn:
      "P10 (2026-10-08) — KEY DISCOVERIES: (1) the 1:2880 SECTION GRID with OFFICIAL geometry (layer GURS/EZKN_LISTI/8000): cells ~1.9×1.5 km, coded IX24+2 letters (columns a–d, rows e–i); OUR SHEETS' FRAME CODES ARE CELL CODES: A02=»O.IX24cƒ«→cell cf (the centre matches A02's content centre EXACTLY!), A03=»O.IX24dg«→cell dg, A04=»O.IX24cg«→cell cg (the P9 CORRECTION!), A05=»O.IX24ch«→cell ch. (2) The record N83-1544 (State 20 — Franciscean cadastre ARS): POVEZAVAJPG = the VAČ fileStream (uodid 227663, docid 9), IME = »SI AS 176/N/N83«, coordinate system »Schockell, Gellert and Krim«. (3) PUBLIC DjVu/JPG images of ZKN sheets (GRIBLJE 1/2/4/K 2–3, ~1970–2005, 300 dpi; via /gurs/ezknpodatki/) — downloaded and decoded (libdjvulibre) for content comparison. Rejected: Mapire/Arcanum (403 from the sandbox).",
  },
];

/** EŠD enote — sodoben uradni register dediščine (issue #3 #8: ločene, uradno dokumentirane) */
export interface HeritageUnit {
  esd: number;
  titleSi: string;
  titleEn: string;
  /** uradni naziv iz registra (EID) */
  officialNameSi?: string;
  officialNameEn?: string;
  /** vrsta enote npr. stavbe / arheološka najdišča / spominski objekti in kraji */
  unitTypeSi?: string;
  unitTypeEn?: string;
  /** status varstva npr. spomenik lokalnega pomena / registrirana dediščina */
  protectionSi?: string;
  protectionEn?: string;
  municipality?: string;
  registerUrl?: string;
  lat?: number;
  lng?: number;
  museumRef?: string;
  /** razlika med uradnim registrom in muzejevo interpretacijo */
  deltaSi?: string;
  deltaEn?: string;
  lastVerified?: string;
}

export const HERITAGE_UNITS: HeritageUnit[] = [
  {
    esd: 2122,
    titleSi: "Griblje — cerkev sv. Vida",
    titleEn: "Griblje — Church of St. Vitus",
    officialNameSi: "Griblje - Cerkev sv. Vida",
    unitTypeSi: "stavbe (podružnična cerkev)",
    unitTypeEn: "buildings (filial church)",
    protectionSi: "spomenik lokalnega pomena",
    protectionEn: "local heritage monument",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=2122",
    lat: 45.56761,
    lng: 15.290311,
    museumRef: "MVG-002",
    deltaSi: "GEOTRUTH (issue #14, 2026-10-08): uradni poligon EŠD 2122 (GisKD, MK_EVRD/3602) — centroid 45,567610 N 15,290311 E, »na pokopališču, na gričku južno od vasi«. Stara koordinata 45,5728/15,2922 (krožna georeferenca) je odstopala 595 m — razrešeno v korist uradnega vira. OSM way 284847361 potrjuje (≤ 8 m).",
    lastVerified: "2026-10-08",
  },
  {
    esd: 10094,
    titleSi: "Griblje — arheološko najdišče ob Kolpi",
    titleEn: "Griblje — archaeological site by the Kolpa",
    officialNameSi: "Griblje - Arheološko najdišče ob Kolpi",
    unitTypeSi: "arheološka najdišča",
    unitTypeEn: "archaeological sites",
    protectionSi: "registrirana dediščina",
    protectionEn: "registered heritage",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=10094",
    lastVerified: "2026-10-07",
    deltaSi:
      "Sinonimi registra: Kohane, Požekov vrt, Krasinec - Vrh. Datiranje: mlajši neolitik do zgodnje rimske doba (naselbine, gomila, ravno grobišče). Vodnik ZVKD Novo mesto, usmeritve 2008. Ni mešan z EŠD 11118 (Kučar, Podzemelj) — dve ločeni enoti. Register ne objavlja koordinat v besedilu; lokacija bo dodana, ko bo pridobljena geometrija iz GISKD (TO_COLLECT).",
  },
  {
    esd: 11118,
    titleSi: "Podzemelj — arheološko najdišče Kučar",
    titleEn: "Podzemelj — Kučar archaeological site",
    officialNameSi: "Podzemelj - Arheološko najdišče Kučar",
    unitTypeSi: "arheološka najdišča",
    unitTypeEn: "archaeological sites",
    protectionSi: "spomenik lokalnega pomena",
    protectionEn: "local heritage monument",
    municipality: "Metlika",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=11118",
    lastVerified: "2026-10-07",
    deltaSi:
      "Občina je Metlika (ne Črnomelj). Železnodobno gradišče in zgodnjekrščansko središče z dvema cerkvama in krstilnico. Muzej v prejšnjih zapisih kraj ni navedel — popravek iz uradnega registra 2026-10-07.",
  },
  {
    esd: 19324,
    titleSi: "Cerkvišče — spomenik NOB",
    titleEn: "Cerkvišče — WWII memorial",
    officialNameSi: "Cerkvišče - Spomenik NOB",
    unitTypeSi: "spominski objekti in kraji",
    unitTypeEn: "memorial monuments and sites",
    protectionSi: "spomenik lokalnega pomena",
    protectionEn: "local heritage monument",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=19324",
    lastVerified: "2026-10-07",
    deltaSi: "Postavljen 1960, avtor Janez Savinšek. Vsebina: štirje partizani, ki so septembra 1941 napadli italijansko patruljo. Register ne objavlja koordinat v besedilu (TO_COLLECT).",
  },
  {
    esd: 19326,
    titleSi: "Griblje — spomenik NOB",
    titleEn: "Griblje — WWII memorial",
    officialNameSi: "Griblje - Spomenik NOB",
    unitTypeSi: "spominski objekti in kraji",
    unitTypeEn: "memorial monuments and sites",
    protectionSi: "registrirana dediščina",
    protectionEn: "registered heritage",
    municipality: "Črnomelj",
    registerUrl: "http://www.eheritage.si/apl/real.aspx?id=19326",
    lastVerified: "2026-10-07",
    deltaSi: "Steber z imeni 11 padlih borcev in dveh žrtev 2. svetovne vojne, postavljen 1961. Register ne objavlja koordinat v besedilu (TO_COLLECT).",
  },
];

/** Negativni rezultati — del raziskovalne provenience */
export interface NegativeResult {
  id: string;
  whatSi: string;
  whatEn: string;
  status: "NOT_FOUND" | "NOT_PUBLIC" | "REVIEW" | "TO_COLLECT";
  detailSi: string;
  detailEn: string;
}

export const NEGATIVE_RESULTS: NegativeResult[] = [
  {
    id: "neg-atlas-model",
    whatSi: "Star Atlas 1825 podatkovni model (atlas-map-data-model-1825, knowledge-graph-1825, story-graph-1825, georef-1825, parcel-register-1825, cadastre-a01)",
    whatEn: "The old Atlas 1825 data model (atlas-map-data-model-1825, knowledge-graph-1825, story-graph-1825, georef-1825, parcel-register-1825, cadastre-a01)",
    status: "NOT_FOUND",
    detailSi:
      "Preiskani: git bundle muzej-backup-20261007, arhivski repozitoriji (markec-group/muzej-arhiv ne obstaja več), lokalni diski, vsi Vercel deploymenti (28). Datoteke niso bile obnovljive — Atlas je znova zgrajen neposredno iz primarnega arhivskega vira SI AS 176/N/N83.",
    detailEn:
      "Searched: the muzej-backup-20261007 git bundle, archive repositories (markec-group/muzej-arhiv no longer exists), local disks, all Vercel deployments (28). The files were not recoverable — the Atlas was rebuilt directly from the primary archival source SI AS 176/N/N83.",
  },
  {
    id: "neg-kurrent",
    whatSi: "Popoln prepis Kurrent rokopisov (vseh 7 spisovnih enot N83)",
    whatEn: "Complete transcription of the Kurrent manuscripts (all 7 written units of N83)",
    status: "REVIEW",
    detailSi:
      "Vsi prepisi v Atlasu so pomožni strojni očrti rokopisa in zahtevajo paleografsko potrditev. Stanje po issue #17 + P5-b, usklajeno z issue #4 (2026-10-10, podrobnosti v research.ts KURRENT_SERIES + inventar /api/atlas): PR 4/4 strani, PG 1/1, PV 1/1 (10 kultur), PS 143/143 strani strojno (P36: 2743 vrstic + P38 pass-3: 2974; sprava s kontrolno vsoto 102+2505=2607 izrecno odprta), PUA 49/49 strani (strani A–B v lastniškem modelu + 101 vrstic strani 3–49 v PUA_CONTINUATION — CEL register), PZ 71/71 strani (P44: tabele razredov + rekapitulacija str. 67, dokaz pz-classes-full.json), PT 8/8 pregledan (101 izvornih vrstic: 81 potrjenih + 15 popravkov + 5 neberljivih; +4 dodane vrstice P3). Vsi statusi REVIEW; paleografska potrditev čaka (issue #12).",
    detailEn:
      "All transcriptions in the Atlas are machine-assisted readings requiring palaeographic confirmation. Status after issue #17 + P5-b, reconciled by issue #4 (2026-10-10, detail in research.ts KURRENT_SERIES + the /api/atlas inventory): PR 4/4 pages, PG 1/1, PV 1/1 (10 cultures), PS 8 pages (structure 1–4 + recapitulation 140–143) + the checksum 102+2505=2607, PUA 49/49 pages (pages A–B in the owners model + 101 rows of pages 3–49 in PUA_CONTINUATION — the COMPLETE register), PZ 12 pages sampled (1–3, 20/30/40/50/60, 68–71; evidence PZ-valuation.json pagesSampled), PT 8/8 reviewed (101 source rows: 81 confirmed + 15 corrections + 5 illegible; +4 rows added by P3). The full PS (135 pages 5–139) and PZ (59 pages 4–67) transcription remains TO_COLLECT; all statuses REVIEW.",
  },
  {
    id: "neg-1812",
    whatSi: "Napoleonov zemljevid ~1812 za območje Griblje",
    whatEn: "Napoleonic map ~1812 for the Griblje area",
    status: "TO_COLLECT",
    detailSi:
      "Slika v zbirki (MVG-092) je sodoben vektorski zemljevid Ilirskih provinc (TRAJAN 117, Wikimedia Commons, 2018, CC BY-SA 3.0) — ne izvirnik iz 1812. Ugotovitev 2026-10-07: javnodostopni obdobjeni izvirniki obstajajo na Wikimedii (npr. 'Provinces Illyriennes Servie et Bosnie 1812', javna last) — pridobitev izvirnika in afina georeferenca sta pripravljena naslednja koraka (TO_COLLECT, metoda enaka A01/A02). Prostorski sloj za 1812 v Atlasu še ni vzpostavljen; obdobje zajeta z MVG-092.",
    detailEn:
      "The collection image (MVG-092) is a modern vector map of the Illyrian Provinces (TRAJAN 117, Wikimedia Commons, 2018, CC BY-SA 3.0) — not an 1812 original. Finding of 2026-10-07: public-domain period originals exist on Wikimedia (e.g. 'Provinces Illyriennes Servie et Bosnie 1812') — acquiring the original and an affine georeference are prepared next steps (TO_COLLECT, method identical to A01/A02). No spatial 1812 layer in the Atlas yet; the period is covered by MVG-092.",
  },
  {
    id: "neg-georef-vector",
    whatSi: "Vektorizacija parcel iz listov A01/A02",
    whatEn: "Vectorization of parcels from sheets A01/A02",
    status: "TO_COLLECT",
    detailSi:
      "Listi sta georeferencirani (slikovno prekrivanje), parcelne meje pa še niso vektorsko izrisane. Samo zazidana pozicija je avtomatsko vektorizirana (156 objektov, status RECONSTRUCTED).",
    detailEn:
      "The sheets are georeferenced (image overlay) but parcel boundaries are not yet vectorised. Only built structures were auto-vectorised (156 objects, RECONSTRUCTED status).",
  },
  {
    id: "neg-sem",
    whatSi: "Digitalna kopija fotografije SEM F0000212 (domnevna rojstna hiša Nika Županiča)",
    whatEn: "Digital copy of the SEM F0000212 photograph (presumed birth house of Niko Županič)",
    status: "NOT_FOUND",
    detailSi:
      "Fotografija je dokumentirana v zbirki SEM (opis: enonadstropna hiša na pero, rojstna hiša dr. Nika Županiča), a digitalna kopija ni v muzejski zbirki (113 zapisov). Provenienca je vzpostavljena v research.ts (F0000212_PROVENANCE): vir SEM digitalne zbirke, pravice 'navedi vir', fotograf/datum ni znan (TO_COLLECT). Povezava hiša 73 / parcela 942/4 ↔ MVG-010 ostaja REVIEW, dokler primarni vir ne potrdi.",
    detailEn:
      "The photograph is documented in the SEM collection (description: one-storey house with a gallery, birth house of Dr. Niko Županič) but a digital copy is not in the museum collection (113 records). Provenance is established in research.ts (F0000212_PROVENANCE): source SEM digital collections, rights 'cite the source', photographer/date unknown (TO_COLLECT). The link house 73 / parcel 942/4 ↔ MVG-010 stays REVIEW until a primary source confirms it.",
  },
  {
    id: "neg-houses-geo",
    whatSi: "Natančne lokacije hiš 1–98 na sodobnem zemljevidu",
    whatEn: "Precise positions of houses 1–98 on the modern map",
    status: "TO_COLLECT",
    detailSi:
      "Hišne številke so na listih A01/A02 zapisane ob stavbah, vendar razdelava številk na listu za posamezno hišo še ni izvedena. Hiše imajo sklic na območje vasi (APPROXIMATE), ne na točko.",
    detailEn:
      "House numbers are written next to buildings on sheets A01/A02, but mapping individual numbers to buildings has not been done yet. Houses reference the village area (APPROXIMATE), not a point.",
  },
  {
    id: "neg-walk-station-32",
    whatSi: "Postaja 32 vodenga sprehoda »Vas in njeni ljudje«",
    whatEn: "Station 32 of the guided walk “The village and its people”",
    status: "NOT_FOUND",
    detailSi:
      "Preiskani VSI razpoložljivi viri (2026-10-07): (1) trenutni extra.json — postaje 1–31, 33–35; (2) izvirni repo pred incidentom (git bundle muzej-backup-20261007, VSEH 25 commitov od 2d9ac9b do 4896f35) — postaja 32 v nobeni različici ni nikoli obstajala; (3) vir podatkov = scrape izvirnega spletišča (zadnji delujoči Vercel deployment 2026-10-06 11:32) — vrzel izhaja že iz izvirnika; (4) surove scrape datoteke (download/) niso ohranjene. Sklep: postaja 32 v izvirniku ni bila objavljena ali je bila izpuščena pred objavo. Po pravilu issueja #4 vsebine NE izmišljujemo — vrzel je vidno označena v sprehodu (mesto 32) in v QA (zaporedje 1–35 z eksplicitnim NOT_FOUND).",
    detailEn:
      "All available sources searched (2026-10-07): (1) current extra.json — stations 1–31, 33–35; (2) the pre-incident original repo (git bundle muzej-backup-20261007, ALL 25 commits from 2d9ac9b to 4896f35) — station 32 never existed in any version; (3) the data source = a scrape of the original website (last working Vercel deployment 2026-10-06 11:32) — the gap originates in the original itself; (4) raw scrape files (download/) are not preserved. Conclusion: station 32 was never published in the original, or was dropped before publication. Per issue #4 no content is invented — the gap is visibly marked in the walk (slot 32) and in QA (sequence 1–35 with an explicit NOT_FOUND).",
  },
  {
    id: "neg-matice",
    whatSi: "matice.si — domnevni portal katastrskih skenov",
    whatEn: "matice.si — an assumed portal of cadastral scans",
    status: "NOT_FOUND",
    detailSi:
      "Iskano 2026-10-08 (issue #17): DNS domene matice.si se ne razreši; spletni iskalniki takega vira ne poznajo (poizvedbe 'matice.si Črnomelj', 'matice.si kataster Griblje'). SKLEP: vir ne obstaja (ali je ugasnjen). Skeni franciscejskega katastra za Griblje ostajajo na VAČ (N083, javno) — to je potrjena pot.",
    detailEn:
      "Searched 2026-10-08 (issue #17): the matice.si DNS does not resolve; search engines do not know such a source (queries 'matice.si Črnomelj', 'matice.si kataster Griblje'). CONCLUSION: the source does not exist (or is defunct). The Griblje Franciscean cadastre scans remain on VAČ (N083, public) — that is the confirmed path.",
  },
  {
    id: "neg-e-ars",
    whatSi: "www.e-ars.si — domnevni portal digitaliziranih enot Arhiva RS",
    whatEn: "www.e-ars.si — an assumed portal of digitised Arhiv RS units",
    status: "NOT_FOUND",
    detailSi:
      "Iskano 2026-10-08 (issue #17): DNS www.e-ars.si je mrtev. Celoten SI AS 176/N83 Griblje pa JE javno dostopen v VAČ (OPSI zbirka 'Digitalizirano arhivsko gradivo starih katastrov') — digitalizacija ARS torej obstaja, dostopna je prek VAČ, ne prek ločenega portala e-ars.si.",
    detailEn:
      "Searched 2026-10-08 (issue #17): the www.e-ars.si DNS is dead. The whole SI AS 176/N83 Griblje IS however publicly accessible via VAČ (the OPSI collection 'Digitalised archival material of the old cadastres') — the ARS digitisation exists, reachable through VAČ, not through a separate e-ars.si portal.",
  },
  {
    id: "neg-pz-recap",
    whatSi: "PZ — Rekapitulacija kultur/razredov na koncu elaborata",
    whatEn: "PZ — a recapitulation of cultures/classes at the end of the elaborate",
    status: "NOT_FOUND",
    detailSi:
      "Iskano 2026-10-08 (issue #17): vzorčene končne strani PZ 68–71 vsebujejo IZKLJUČNO administrativne protokole (Vorlage, Geprüft, Nachtrag s 'hus Zins' seznamom, zaključek 'Gemacht den 28ten Juli 1825') — kulturna rekapitulacija NI tam. Cenilne tabele po kulturah in razredih so v sredini (str. ~4–67; vzorčene str. 20/30/40/50/60). Naslednji korak: ciljano branje str. 4–67.",
    detailEn:
      "Searched 2026-10-08 (issue #17): the sampled end pages PZ 68–71 contain ONLY administrative protocols (Vorlage, Geprüft, a Nachtrag with the 'hus Zins' list, the closing 'Gemacht den 28ten Juli 1825') — no culture recapitulation is there. The valuation tables by culture and class sit in the middle (pp. ~4–67; sampled pp. 20/30/40/50/60). Next step: a targeted read of pp. 4–67.",
  },
  {
    id: "neg-oral-interviews",
    whatSi: "Posneti intervjuji ustne zgodovine",
    whatEn: "Recorded oral-history interviews",
    status: "TO_COLLECT",
    detailSi:
      "Iskano 2026-10-08 (issue #17): javno dostopnih posnetih pričevanj domačinov Gribelj NI (teme obstajajo: Pasuljada, tamburaši, dogodki, šola). Pripravljen je raziskovalni protokol v1.0 (research.ts ORAL_HISTORY_PROTOCOL: 4 faze, soglasje, pravice, 5 pravil). ORAL_INTERVIEWS ostane prazen — ne izmišljujemo intervjujev; prvi snemalni korak je na živi strani.",
    detailEn:
      "Searched 2026-10-08 (issue #17): no publicly accessible recorded testimonies of Griblje villagers exist (the topics do: the bean feast, tamburica players, events, school). A research protocol v1.0 is prepared (research.ts ORAL_HISTORY_PROTOCOL: 4 stages, consent, rights, 5 rules). ORAL_INTERVIEWS stays empty — no interviews are invented; the first recording step is on the live side.",
  },
];
