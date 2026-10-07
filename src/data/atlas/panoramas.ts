/**
 * HISTORICAL PANORAMA LAYER (issue #13 — P2 VISUAL REALISM).
 *
 * TimeLens vzorec: obiskovalec na lokaciji odklene TimeSpot in stopi v
 * »zgodovinski trenutek, v katerega pogleda« — ne v 3D maketo, ampak v
 * imerzivni 360° prizor. Ta datoteka je PODATKOVNI SLOJ te plasti:
 *
 *  · vsaka panorama je vezana na obstoječi TimeSpot (noben nov sistem);
 *  · equirectangular 360° slika (2:1) + določen headingDeg središča slike;
 *  · vsaka VIZUALNA TRDITEV ima svoj evidence status (Himera vzorec —
 *    visual realism ≠ historical certainty);
 *  · produkcija: zgodovinski viri → evidence zapis → scene brief →
 *    vizualizacija → 360 asset → metadata/provenance (TimeLens pipeline);
 *  · panorama ni fotografija in ni fotogrametrija: je INTERPRETACIJA,
 *    zgrajena NA DOCUMENTIRANIH legah (EŠD/kataster/struga Kolpe).
 *    Kar ni dokumentirano (fasade, ljudje, živali), v prizoru NI —
 *    in je v claims zabeleženo kot TO_COLLECT.
 *
 * Proceduralna 3D vas (village-scene) OSTANE kot podatkovni/fallback sloj.
 */

import type { TimeYear } from "@/lib/time-machine-store";

/** evidence status vizualne trditve (issue #13, točka 10) */
export type ClaimStatus =
  | "DOCUMENTED" // uradni/arhivski vir
  | "RECONSTRUCTED" // izpeljano iz virov (npr. kataster pod afinijo)
  | "ESTIMATE" // ocena
  | "INTERPRETATION" // poštena upodobitev brez neposrednega vira
  | "TO_COLLECT"; // podatka še ni — v prizoru GA NI

export interface PanoClaim {
  /** kaj je v prizoru (ali zakaj ga ni) */
  whatSi: string;
  whatEn: string;
  status: ClaimStatus;
  sourceSi: string;
  sourceEn: string;
}

export interface HistoricalPanorama {
  /** kratek identifikator (URL / API) */
  id: string;
  /** vez na obstoječi TimeSpot (TIME_SPOTS) */
  timeSpotId: string;
  year: TimeYear;
  /** equirectangular slika (2:1, JPEG, ~1440×720) */
  imageUrl: string;
  /** lahek predogled (~480×240, nalaga se prvi) */
  previewUrl: string | null;
  /** kompasna smer središča slike (u = 0,5) — začetni pogled je determinističen */
  headingDeg: number;
  titleSi: string;
  titleEn: string;
  /** poštena evidenca celotne panorame */
  evidenceSi: string;
  evidenceEn: string;
  /** skupni status vizualizacije */
  status: "RECONSTRUCTED" | "ESTIMATE" | "INTERPRETATION";
  /** trditve po elementih — povezava visual asset → claim → vir → status */
  claims: PanoClaim[];
  /** opis produkcije (TimeLens pipeline, pošteno) */
  methodSi: string;
  methodEn: string;
  /** viri (GeoTruth sourceId + MVG zapisi) */
  sources: string[];
  /** pripoved: statični MP3 obstaja v isti drop-in lokaciji kot TTS #12 */
  audioSiUrl: string;
  audioEnUrl: string;
}

export const PANORAMAS: HistoricalPanorama[] = [
  {
    id: "pano-cerkev-1825",
    timeSpotId: "cerkev",
    year: 1825,
    imageUrl: "/panoramas/cerkev-1825.jpg",
    previewUrl: "/panoramas/cerkev-1825-preview.jpg",
    /* središče slike po rollu = vas 1825 (azimut ≈ 35°); cerkev v prizoru na
       u≈0,23 ≈ azimut 298° — približno (stališče je griček Ob cerkvi) */
    headingDeg: 35,
    titleSi: "S cerkvenega grička — Griblje 1825",
    titleEn: "From the church hill — Griblje 1825",
    evidenceSi:
      "EŠD 2122 (uradna lokacija cerkve) · kataster list A02 (SI AS 176, GEOTRUTH afina, issue #14) · MVG-002 · MVG-003 · MVG-001",
    evidenceEn:
      "EŠD 2122 (official church location) · cadastre sheet A02 (SI AS 176, GEOTRUTH affine, issue #14) · MVG-002 · MVG-003 · MVG-001",
    status: "INTERPRETATION",
    claims: [
      {
        whatSi: "Cerkev sv. Vida z zvonikom na pokopališkem gričku (opazovalno stališče)",
        whatEn: "St. Vitus' church with its bell tower on the cemetery hill (the viewpoint)",
        status: "DOCUMENTED",
        sourceSi: "EŠD 2122 · MVG-002/MVG-003 (prva omemba 1526 — 500-letnica 2026)",
        sourceEn: "EŠD 2122 · MVG-002/MVG-003 (first mentioned 1526 — 500th anniversary 2026)",
      },
      {
        whatSi: "Vas ~156 stavb v dveh sklopih severno/severovzhodno od cerkve",
        whatEn: "The village of ~156 buildings in two clusters N/NE of the church",
        status: "RECONSTRUCTED",
        sourceSi: "Franciscejski kataster 1825, list A02 (SI AS 176), GEOTRUTH afina (issue #14)",
        sourceEn: "1825 Franciscean cadastre, sheet A02 (SI AS 176), GEOTRUTH affine (issue #14)",
      },
      {
        whatSi: "Lesene hiše z strmimi dvokapnicami (skodle/slama)",
        whatEn: "Timber houses with steep gabled roofs (shingles/thatch)",
        status: "INTERPRETATION",
        sourceSi: "vrstna Belokranjska ljudska arhitektura; material po stavbah NI zapisan v katastru",
        sourceEn: "Bela krajina vernacular architecture type; per-building materials are NOT recorded in the cadastre",
      },
      {
        whatSi: "Kolpa — sijaj vode v prizoru (georeferencirana struga)",
        whatEn: "The Kolpa — water glinting in the scene (georeferenced channel)",
        status: "RECONSTRUCTED",
        sourceSi: "georeferencirana struga Kolpe + cone rabe tal (VLM analiza lista A02). POŠTENO: smer vode V SLIKI je kompasno približna — struga je dokumentirana, njena smer v vizualizaciji pa je interpretacija postavitve",
        sourceEn: "georeferenced Kolpa channel + land-use zones (VLM analysis of sheet A02). HONESTLY: the water's direction IN THE IMAGE is compass-approximate — the channel is documented, its direction in the visualisation is a placement interpretation",
      },
      {
        whatSi: "Ljudje, živina, vozovi — v prizoru jih NI",
        whatEn: "People, livestock, carts — NOT in the scene",
        status: "TO_COLLECT",
        sourceSi: "Register hiš 1825 pozna 80 lastnikov, matrike 1669–1947 — vendar ni etnografske dokumentacije oblačil/delavnosti v muzejskih virih; izmišljevanje NE",
        sourceEn: "the 1825 house register knows 80 owners, parish books 1669–1947 — but no ethnographic documentation of clothing/activity in the museum's sources; inventing them is NOT honest",
      },
      {
        whatSi: "Jutranja svetloba, zgodnjejesenski letni čas",
        whatEn: "Morning light, early-autumn season",
        status: "INTERPRETATION",
        sourceSi: "atmosferska izbira produkcije — letni čas 1825 ni dokumentiran",
        sourceEn: "production atmosphere choice — the season of 1825 is not documented",
      },
    ],
    methodSi:
      "TimeLens pipeline: zgodovinski viri (EŠD 2122, kataster A02, struga Kolpe) → evidence zapis → scene brief (lege SO dokumentirane) → vizualizacija equirectangular 360° → post-proces (horizontalni roll — šiv v monotonem pasu, navpična kalibracija horizonta 0,45→0,50, preklopni šiv 120 px, JPEG) → asset + metadata. POŠTENO: slika je INTERPRETACIJA postavitve, ne fotografija; lege so dokumentirane, izgled je vrstno-rekonstrukcijski, smeri posameznih prvin v sliki so kompasno približne.",
    methodEn:
      "TimeLens pipeline: historical sources (EŠD 2122, cadastre A02, Kolpa channel) → evidence record → scene brief (positions ARE documented) → equirectangular 360° visualisation → post-processing (horizontal roll — seam in a uniform strip, vertical horizon calibration 0.45→0.50, 120 px cross-fade seam, JPEG) → asset + metadata. HONESTLY: the image is an INTERPRETATION of the layout, not a photograph; positions are documented, appearance is a type-reconstruction, individual feature directions in the image are compass-approximate.",
    sources: ["src-esd2122", "src-a02-sheet", "src-geotruth-fix", "MVG-001", "MVG-002", "MVG-003"],
    audioSiUrl: "/audio/timespots/cerkev-si.mp3",
    audioEnUrl: "/audio/timespots/cerkev-en.mp3",
  },
  {
    id: "pano-jedro-1825",
    timeSpotId: "jedro",
    year: 1825,
    imageUrl: "/panoramas/jedro-1825.jpg",
    previewUrl: "/panoramas/jedro-1825-preview.jpg",
    /* središče slike po rollu ≈ azimut 267° (W — travniki); cerkev v prizoru
       na u≈0,37 = azimut 220° (dokumentirana smer jedro→cerkev) */
    headingDeg: 267,
    titleSi: "Sred vasi — Griblje 1825",
    titleEn: "Middle of the village — Griblje 1825",
    evidenceSi:
      "Kataster list A02 (SI AS 176, GEOTRUTH afina, issue #14) · Register hiš 1825 (80 lastnikov) · MVG-001 · MVG-002 (cerkev)",
    evidenceEn:
      "Cadastre sheet A02 (SI AS 176, GEOTRUTH affine, issue #14) · 1825 house register (80 owners) · MVG-001 · MVG-002 (church)",
    status: "INTERPRETATION",
    claims: [
      {
        whatSi: "Vas 1825 okoli tebe — dva sklopa, ~156 stavb, vasi podobna ulica",
        whatEn: "The 1825 village around you — two clusters, ~156 buildings, a lane-like street",
        status: "RECONSTRUCTED",
        sourceSi: "Franciscejski kataster 1825, list A02 (SI AS 176), GEOTRUTH afina (issue #14)",
        sourceEn: "1825 Franciscean cadastre, sheet A02 (SI AS 176), GEOTRUTH affine (issue #14)",
      },
      {
        whatSi: "Cerkev sv. Vida z zvonikom na gričku proti jugozahodu",
        whatEn: "St. Vitus' church with its bell tower on the hill to the SW",
        status: "DOCUMENTED",
        sourceSi: "EŠD 2122 · MVG-002 · prvič omenjena 1526",
        sourceEn: "EŠD 2122 · MVG-002 · first mentioned 1526",
      },
      {
        whatSi: "Kolpa — sijaj vode v prizoru (desno od cerkve)",
        whatEn: "The Kolpa — water glinting in the scene (right of the church)",
        status: "RECONSTRUCTED",
        sourceSi: "georeferencirana struga Kolpe (issue #14). POŠTENO: smer vode V SLIKI je kompasno približna, georeferencirana struga leži vzhodno — smer v vizualizaciji je interpretacija",
        sourceEn: "georeferenced Kolpa channel (issue #14). HONESTLY: the water's direction IN THE IMAGE is compass-approximate, the georeferenced channel lies east — the direction in the visualisation is an interpretation",
      },
      {
        whatSi: "Njive/travniki okoli jedra, gozdni rob zahodno",
        whatEn: "Fields/meadows around the core, forest edge to the west",
        status: "RECONSTRUCTED",
        sourceSi: "cone rabe tal (VLM analiza lista A02)",
        sourceEn: "land-use zones (VLM analysis of sheet A02)",
      },
      {
        whatSi: "Lesene hiše, skodlaste strehe, zemeljska pot",
        whatEn: "Timber houses, shingled roofs, earthen lane",
        status: "INTERPRETATION",
        sourceSi: "vrstna Belokranjska arhitektura; materiali in cesta niso po-stavbo dokumentirani",
        sourceEn: "Bela krajina vernacular type; materials and the lane are not documented per-building",
      },
      {
        whatSi: "Meščani/stanovalci — v prizoru jih NI (80 lastnikov je v registru, oblačil ni v virih)",
        whatEn: "Residents — NOT in the scene (80 owners are in the register, clothing is not in the sources)",
        status: "TO_COLLECT",
        sourceSi: "Register hiš 1825 · matrike Podzemelj — etnografski vir še ni v zbirki",
        sourceEn: "1825 house register · Podzemelj parish books — an ethnographic source is not yet in the collection",
      },
    ],
    methodSi:
      "TimeLens pipeline: kataster (lege) → evidence → scene brief → vizualizacija 360° → post-proces (roll 0,15 — šiv v monotonem pasu, kalibracija horizonta 0,38→0,50, preklopni šiv, JPEG). Cerkev v prizoru stoji na dokumentirani smeri (azimut 220°); gostota jedra je rekonstruirana; izgled stavb je vrstna interpretacija.",
    methodEn:
      "TimeLens pipeline: cadastre (positions) → evidence → scene brief → 360° visualisation → post-processing (roll 0.15 — seam in a uniform strip, horizon calibration 0.38→0.50, cross-fade seam, JPEG). The church in the scene stands at its documented direction (bearing 220°); the core density is reconstructed; building appearance is a type interpretation.",
    sources: ["src-a02-sheet", "src-geotruth-fix", "src-esd2122", "MVG-001", "MVG-002"],
    audioSiUrl: "/audio/timespots/jedro-si.mp3",
    audioEnUrl: "/audio/timespots/jedro-en.mp3",
  },
  {
    id: "pano-kolpa-1825",
    timeSpotId: "kolpa",
    year: 1825,
    imageUrl: "/panoramas/kolpa-1825.jpg",
    previewUrl: "/panoramas/kolpa-1825-preview.jpg",
    /* središče slike po rollu ≈ azimut 71° (E — čez reko, HR breg); vas v
       prizoru na u≈0,15 = azimut 305° (dokumentirana smer kolpa→jedro) */
    headingDeg: 71,
    titleSi: "Ob Kolpi — Griblje 1825",
    titleEn: "By the Kolpa — Griblje 1825",
    evidenceSi:
      "Georeferencirana struga Kolpe (OSM/issue #14, sidro CORROBORATED) · cone rabe tal (A02) · MVG-006 · MVG-092 (carinarnica — BEZ geometrije)",
    evidenceEn:
      "Georeferenced Kolpa channel (OSM/issue #14, CORROBORATED anchor) · land-use zones (A02) · MVG-006 · MVG-092 (customs post — WITHOUT geometry)",
    status: "INTERPRETATION",
    claims: [
      {
        whatSi: "Kolpa — reka, ki je vasi dala življenje (struga georeferencirana)",
        whatEn: "The Kolpa — the river that gave the village life (channel georeferenced)",
        status: "DOCUMENTED",
        sourceSi: "OSM struga + sidro anchor-kolpa (CORROBORATED, ±25 m) · MVG-006",
        sourceEn: "OSM channel + anchor-kolpa (CORROBORATED, ±25 m) · MVG-006",
      },
      {
        whatSi: "Vas v daljavi proti severozahodu",
        whatEn: "The village in the distance to the NW",
        status: "RECONSTRUCTED",
        sourceSi: "kataster A02 + GEOTRUTH afina — ~350 m od struge",
        sourceEn: "cadastre A02 + GEOTRUTH affine — ~350 m from the channel",
      },
      {
        whatSi: "Travniki ob reki, gozd na hrbtnih bregovih",
        whatEn: "Meadows by the river, forest on the far banks",
        status: "RECONSTRUCTED",
        sourceSi: "cone rabe tal (VLM analiza lista A02)",
        sourceEn: "land-use zones (VLM analysis of sheet A02)",
      },
      {
        whatSi: "Utrta pot ob bregu (v prizoru)",
        whatEn: "A trodden path along the bank (in the scene)",
        status: "INTERPRETATION",
        sourceSi: "pot ob Kolpi do mlinov je zgodovinsko verjetna, a NI dokumentirana na tem odseku — upodobljena kot interpretacija",
        sourceEn: "a path along the Kolpa towards the mills is historically plausible, but NOT documented on this stretch — shown as an interpretation",
      },
      {
        whatSi: "Napoleonova carinarnica 1809–1813 — v prizoru je NI",
        whatEn: "Napoleon's customs post 1809–1813 — NOT in the scene",
        status: "TO_COLLECT",
        sourceSi: "MVG-092: zgodovinski zapis BREZ geometrije in BREZ opisa izgleda — izmišljevanje fasade bi bilo neresnično; zgodba ostaja na kartici točke",
        sourceEn: "MVG-092: a historical record WITHOUT geometry and WITHOUT an appearance description — inventing a facade would be dishonest; the story stays on the spot card",
      },
      {
        whatSi: "Čolni, mlini, ribiči — v prizoru jih NI (mlin so 2+ km dolvodno, MVG-009)",
        whatEn: "Boats, mills, fishermen — NOT in the scene (the mills are 2+ km downstream, MVG-009)",
        status: "TO_COLLECT",
        sourceSi: "MVG-009 (mlini: Dol, Radenci, Pobrežje, Krasinec — oddaljeni od te točke)",
        sourceEn: "MVG-009 (mills: Dol, Radenci, Pobrežje, Krasinec — distant from this spot)",
      },
    ],
    methodSi:
      "TimeLens pipeline: struga (dokumentirana) → evidence → scene brief → vizualizacija 360° → post-proces (roll 0,25 — šiv v odprtem travniku, kalibracija horizonta 0,25→0,50, preklopni šiv, JPEG). POŠTENO: carinarnice NI v prizoru, ker zapis (MVG-092) ne nosi ne geometrije ne izgleda — praznina ostaja vidna, ne zapolnjena z izmišljeno fasado.",
    methodEn:
      "TimeLens pipeline: channel (documented) → evidence → scene brief → 360° visualisation → post-processing (roll 0.25 — seam in open meadow, horizon calibration 0.25→0.50, cross-fade seam, JPEG). HONESTLY: the customs post is NOT in the scene, because the record (MVG-092) carries neither geometry nor appearance — the gap stays visible, not filled with an invented facade.",
    sources: ["src-osm", "src-esd10094", "src-a02-sheet", "MVG-006", "MVG-092", "MVG-009"],
    audioSiUrl: "/audio/timespots/kolpa-si.mp3",
    audioEnUrl: "/audio/timespots/kolpa-en.mp3",
  },
];

/** panorama po id (null, če je ne poznamo). */
export function getPanoramaById(id: string | null | undefined): HistoricalPanorama | null {
  if (!id) return null;
  return PANORAMAS.find((p) => p.id === id) ?? null;
}

/** panorame za TimeSpot (po letu, zadnja zmaga) — prva je privzeta. */
export function getPanoramaForSpot(
  spotId: string | null | undefined,
  year?: TimeYear,
): HistoricalPanorama | null {
  if (!spotId) return null;
  const list = PANORAMAS.filter((p) => p.timeSpotId === spotId);
  if (list.length === 0) return null;
  if (year == null) return list[0];
  return list.find((p) => p.year === year) ?? list[0];
}

/** ima TimeSpot hero panoramo? (za [DOŽIVI 360°] gumb) */
export function spotHasPanorama(spotId: string): boolean {
  return PANORAMAS.some((p) => p.timeSpotId === spotId);
}

/**
 * Globa povezava panorame — isti vzorec kot spotDeepLink, z &pano=1
 * (obisk na lokaciji → QR → TimeSpot → Doživi 360°).
 */
export function panoramaDeepLink(p: HistoricalPanorama): string {
  const yearParam = p.year === 2026 ? "danes" : p.year === 1900 ? "1900" : "1825";
  return `https://griblje-museum.vercel.app/?casovni=${yearParam}&spot=${p.timeSpotId}&pano=1`;
}
