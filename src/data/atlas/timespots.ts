/**
 * AR TIME SPOTS v1 (issue #11) — časovne točke po vasi.
 *
 * Vsaka točka je portal v določen zgodovinski trenutek (koncept TimeLens):
 * fizična lokacija + letnica + kaj tu stoji v rekonstrukciji + viri.
 * Odklene se, ko obiskovalec stopi znotraj radija; globa povezava
 * `?casovni=<leto>&spot=<id>` (in QR koda nanjo) pa jo odpre od koderkoli.
 *
 * Koordinate so vzete IZKLJUČNO iz zapisov zbirke (exhibits.json, lat/lng) —
 * nobena točka ni izmišljena. Letnica ustreza obstoječi rekonstrukciji
 * časovnega stroja (1825 · ~1900 · danes), opisi pošteno ločujejo
 * REKONSTRUIRANO / OCENO / INTERPRETACIJO.
 *
 * Mlini (MVG-009) in letališče Otok (MVG-013) so IZVEN obsega 3D prizora
 * (~600 m okoli jedra) → prestavljeni v P1 (issue #11, komentar o izbiri).
 */

import type { GeoPoint } from "@/lib/geo";
import { distanceM } from "@/lib/geo";
import type { TimeYear } from "@/lib/time-machine-store";

export interface TimeSpot {
  /** kratek identifikator (URL, QR, shramba) */
  id: string;
  lat: number;
  lng: number;
  /** radij odklepanja v metrih (TimeLens vzorec — velik, odklep zgodaj) */
  radius: number;
  /** bližina, na kateri je scena »poravnana« (issue #14 — dinamični radij) */
  renderReadyM?: number;
  /** bližina visoke natančnosti — kompas-kalibracija smiselna (issue #14) */
  precisionM?: number;
  /** GeoTruth povezava (issue #14 — avdit zahteva sidro) */
  anchorId?: string;
  /** privzeta letnica časovnega stroja ob odklepu */
  year: TimeYear;
  titleSi: string;
  titleEn: string;
  /** kaj tu stoji v rekonstrukciji — kratko, pošteno */
  descSi: string;
  descEn: string;
  /** navedba vira (prikaz na kartici) */
  evidenceSi: string;
  evidenceEn: string;
  /** povezani zapis zbirke (MVG) */
  exhibitSlug: string;
  /** hiša iz registra 1825 (opcijsko — hišna zgodba) */
  houseNo?: string;
}

export const TIME_SPOTS: TimeSpot[] = [
  {
    id: "cerkev",
    lat: 45.56761,
    lng: 15.290311,
    radius: 50,
    renderReadyM: 25,
    precisionM: 10,
    anchorId: "anchor-cerkev",
    year: 1825,
    titleSi: "Cerkev sv. Vida",
    titleEn: "St. Vitus' church",
    descSi:
      "Stojiš pred cerkvijo na pokopališkem gričku južno od jedra, prvič omenjeno 1526. V rekonstrukciji 1825 stoji njen 3D model na uradni lokaciji EŠD 2122 — z zvonikom. Letos obeležujemo 500 let od prve omembe.",
    descEn:
      "You stand before the church on its cemetery hill south of the core, first mentioned in 1526. In the 1825 reconstruction its 3D model stands at the official EŠD 2122 location — with its bell tower. This year marks 500 years since the first mention.",
    evidenceSi: "EŠD 2122 (Register nepremične kulturne dediščine, uradni vir) · MVG-002 · MVG-003 · kataster, list A02 (SI AS 176)",
    evidenceEn: "EŠD 2122 (Register of Immovable Cultural Heritage, official source) · MVG-002 · MVG-003 · cadastre, sheet A02 (SI AS 176)",
    exhibitSlug: "sveti-vid",
  },
  {
    id: "jedro",
    lat: 45.57092,
    lng: 15.29435,
    radius: 60,
    renderReadyM: 30,
    anchorId: "anchor-jedro-1825",
    year: 1825,
    titleSi: "Jedro vasi 1825 — Grüble",
    titleEn: "Village core 1825 — Grüble",
    descSi:
      "Sredi vasi 1825: 156 katastrskih stavb stoji okoli tebe, jedro z dvema sklopoma ob cerkvi. Tapni hišo — pove ti tloris in postavi vprašanje, kdo je v njej živel: Register hiš 1825 ima 80 lastnikov, matične knjige pa 1669–1947. Današnje jedro je ~400 m severno — vas je zrasla proti severu.",
    descEn:
      "In the middle of the 1825 village: 156 cadastre buildings around you, the core in two clusters by the church. Tap a house — it shows its footprint and asks who lived there: the 1825 house register holds 80 owners, the parish books span 1669–1947. Today's core lies ~400 m north — the village grew northward.",
    evidenceSi: "MVG-001 · kataster list A02 (SI AS 176, GEOTRUTH afina, issue #14) · Register hiš 1825 · matrike Podzemelj",
    evidenceEn: "MVG-001 · cadastre sheet A02 (SI AS 176, GEOTRUTH affine, issue #14) · 1825 house register · Podzemelj parish books",
    exhibitSlug: "griblje-vas",
    houseNo: "61",
  },
  {
    id: "kolpa",
    lat: 45.5688,
    lng: 15.2988,
    radius: 60,
    anchorId: "anchor-kolpa",
    year: 1825,
    titleSi: "Kolpa — življenje ob reki",
    titleEn: "Kolpa — life on the river",
    descSi:
      "Ob reki, ki je vasi dala življenje. 1809–1813 je tu delovala Napoleonova carinarnica (Ilirske province); struga Kolpe je v rekonstrukciji georeferencirana.",
    descEn:
      "By the river that gave the village life. In 1809–1813 Napoleon's customs post operated here (Illyrian Provinces); the Kolpa riverbed is georeferenced in the reconstruction.",
    evidenceSi: "MVG-006 · MVG-092 (carinarnica 1809–1813) · georeferencirana struga (sidro 15,2994 E)",
    evidenceEn: "MVG-006 · MVG-092 (customs post 1809–1813) · georeferenced riverbed (anchor 15.2994 E)",
    exhibitSlug: "kolpa-reka",
  },
  {
    id: "ribnik",
    lat: 45.5735,
    lng: 15.294,
    radius: 45,
    anchorId: "anchor-ribnik",
    year: 1900,
    titleSi: "Vaški ribnik",
    titleEn: "The village pond",
    descSi:
      "Kraj, kjer je vas hranila vodo za živino. Ribi sam v prizoru ni — vidiš jedro vasi ~1900: OCENO zgoščevanja po delitvi domačij (35 novih stavb).",
    descEn:
      "The place where the village kept water for livestock. The pond itself is not in the scene — you see the village core ~1900: an ESTIMATE of densification after farm divisions (35 new buildings).",
    evidenceSi: "MVG-016 · ~1900 = OCENA (metodologija periode)",
    evidenceEn: "MVG-016 · ~1900 = ESTIMATE (period methodology)",
    exhibitSlug: "ribnik",
  },
  {
    id: "gornje",
    lat: 45.571396,
    lng: 15.292355,
    radius: 50,
    renderReadyM: 25,
    anchorId: "anchor-spomenik",
    year: 1825,
    titleSi: "Zgornji konec vasi — spomenik in zaselki",
    titleEn: "Upper end of the village — memorial and hamlets",
    descSi:
      "Severni rob vasi 1825 (vas je pozneje zrasla še severneje). Zaselki Dolnje, Srednje in Gornje Griblje so zapisani že 1526. Tu, pred osnovno šolo, stoji spomenik padlim vaščanom (1961) — uradna lokacija EŠD 19326. Preklopi na »danes« in primerjaj.",
    descEn:
      "The north end of the 1825 village (it later grew further north). The hamlets of Dolnje, Srednje and Gornje Griblje are recorded as early as 1526. Here, in front of the primary school, stands the memorial to the fallen villagers (1961) — the official EŠD 19326 location. Switch to “today” and compare.",
    evidenceSi: "EŠD 19326 (spomenik pred osnovno šolo, uradni vir) · MVG-029 · MVG-049 (zaselki 1526)",
    evidenceEn: "EŠD 19326 (memorial in front of the primary school, official source) · MVG-029 · MVG-049 (hamlets 1526)",
    exhibitSlug: "spomenik-padlim",
  },
  {
    id: "meja",
    lat: 45.5675,
    lng: 15.2995,
    radius: 50,
    anchorId: "anchor-meja",
    year: 2026,
    titleSi: "Meja ob Kolpi — danes in duhovi",
    titleEn: "Border on the Kolpa — today and ghosts",
    descSi:
      "Stojiš na meji, ki je tu od 1991. Vklopi »danes«: žični duhovi hiš 1825 razmejujejo, kje je stala vas — pogovor med preteklostjo in sedanjostjo.",
    descEn:
      "You stand on the border, here since 1991. Switch to “today”: the wireframe ghosts of the 1825 houses trace where the village stood — a dialogue between past and present.",
    evidenceSi: "MVG-015 (meja 1991) · »danes« = interpretacija (žični obris 1825)",
    evidenceEn: "MVG-015 (border 1991) · “today” = interpretation (1825 wireframe outline)",
    exhibitSlug: "meja-1991",
  },
];

/** privzeti dinamični radiji, če točka ne določa svojih (issue #14, točka 10):
 *  unlock = radij odklepa (TimeLens — odklep zgodaj), renderReady = bližina,
 *  na kateri je scena »poravnana«, precision = visoka natančnost. */
export const SPOT_RADIUS_DEFAULTS = {
  unlock: 50,
  renderReady: 25,
  precision: 10,
} as const;

/** URL parameter letnice za globo povezavo/QR (skladen s parseYearParam). */
export function spotYearParam(year: TimeYear): string {
  return year === 2026 ? "danes" : year === 1900 ? "1900" : "1825";
}

/** privzeti radij »scene poravnana«, če točka ne določa svojega */
export const SPOT_RENDER_READY = SPOT_RADIUS_DEFAULTS.renderReady;
/** privzeti radij visoke natančnosti */
export const SPOT_PRECISION = SPOT_RADIUS_DEFAULTS.precision;

/** Globa povezava točke — izhodišče QR kod. */
export function spotDeepLink(spot: TimeSpot): string {
  return `https://griblje-museum.vercel.app/?casovni=${spotYearParam(spot.year)}&spot=${spot.id}`;
}

/** Točka po id (null, če ne poznamo). */
export function getSpotById(id: string | null | undefined): TimeSpot | null {
  if (!id) return null;
  return TIME_SPOTS.find((s) => s.id === id) ?? null;
}

/** Najbližja točka od položaja uporabnika (+ razdalja v metrih). */
export function findNearestSpot(p: GeoPoint): { spot: TimeSpot; dist: number } {
  let best = TIME_SPOTS[0];
  let bestD = distanceM(p, best);
  for (const s of TIME_SPOTS.slice(1)) {
    const d = distanceM(p, s);
    if (d < bestD) {
      best = s;
      bestD = d;
    }
  }
  return { spot: best, dist: bestD };
}
