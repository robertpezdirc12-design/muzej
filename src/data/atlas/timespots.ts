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
 * Mlini (MVG-009) in letališče Otok (MVG-013) sta bila v v1 IZVEN obsega
 * 3D prizora → prestavljena v P1. P1 (issue #12) ju dodaja skupaj s
 * Cerkviščem (MVG-040) kot ODDALJENE TOČKE z lastno vsebino (Knossos
 * vzorec — segmentirano nalaganje: lastna lahka proceduralna scena ali
 * story kartica, namesto praznega pogleda na vas 2–10 km stran):
 *  · mlini      — proceduralna scena vodnega mlina (tip, ne konkretn mlin);
 *  · otok       — story kartica z dogodki 1944–45 (brez 3D: spomenik je fizičen);
 *  · cerkvišče  — tri cerkvice kot duhovi (1408) + kapelica 1994.
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
  /** lastna proceduralna mini-scena (issue #12 — oddaljene točke,
      namesto praznega pogleda na oddaljeno vas) */
  miniScene?: "mlini" | "cerkvisce";
  /** dogodki za story kartico (issue #12 — Otok: story-only) */
  events?: SpotEvent[];
}

/** dogodek na story kartici točke (issue #12 — Otok 1944–45) */
export interface SpotEvent {
  /** oznaka časa (leto ali datum) */
  whenSi: string;
  whenEn: string;
  textSi: string;
  textEn: string;
}

/** oddaljene točke (issue #12): ločene v UI, lastna vsebina */
export const DISTANT_SPOT_IDS = ["mlini", "otok", "cerkvisce"] as const;

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

  /* ── P1 (issue #12): oddaljene točke z lastno vsebino ── */

  {
    id: "mlini",
    lat: 45.5315,
    lng: 15.3119,
    radius: 60,
    anchorId: "anchor-mlini",
    year: 1825,
    miniScene: "mlini",
    titleSi: "Mlini ob Kolpi",
    titleEn: "Mills on the Kolpa",
    descSi:
      "Ob Kolpi so mlini mleli žito bližnjih vasi stoletja — urbarji jih navajajo v Dolu, Radencih, Pobrežju in Krasincu. Pred tabo stoji proceduralna scena vodnega mlina: hiša, kolo, jez in toča. POŠTENO: to je rekonstrukcija VRSTE mlina (žimaln — vodoravno kolo znotraj), ne konkretnega mlina; koordinata zapisa je reprezentativna točka mlinarskega območja. Preklopi na »danes« — mlin postane duh: večina jih je propadla, Pobrežje je med ohranjenimi.",
    descEn:
      "Along the Kolpa mills ground the grain of nearby villages for centuries — the urbars list them at Dol, Radenci, Pobrežje and Krasinec. Before you stands a procedural water-mill scene: the house, the wheel, the weir and the millstream. HONESTLY: this is a reconstruction of the mill TYPE (žimaln — a horizontal wheel inside), not of a particular mill; the record coordinate is a representative point of the milling stretch. Switch to “today” — the mill turns into a ghost: most have decayed, Pobrežje among the preserved.",
    evidenceSi:
      "MVG-009 · Radio Odeon (urbarji) · Krajinski park Kolpa · scena = INTERPRETACIJA vrste (proceduralna) — terenska preverba čaka",
    evidenceEn:
      "MVG-009 · Radio Odeon (urbars) · Kolpa Landscape Park · the scene = an INTERPRETATION of the type (procedural) — field check pending",
    exhibitSlug: "mlini-na-kolpi",
  },
  {
    id: "otok",
    lat: 45.665,
    lng: 15.323,
    radius: 90,
    anchorId: "anchor-otok",
    year: 2026,
    titleSi: "Partizansko letališče Otok 1944–45",
    titleEn: "The Otok partisan airfield 1944–45",
    descSi:
      "Na travniku ob vasi Otok pri Metliki (~10 km severno od Gribelj) so partizani spomladi 1944 uredili letališče za zavezniška letala. Letala so pristajala ob zatemnitvi, travnik so označili z lučmi. Do konca vojne so od tu odpeljali 1473 ranjencev v zavezniške bolnišnice v južni Italiji — danes dogodek varuje spominski Douglas C-47 Dakota. Točka je story-only: travnik je pred tabo, spomenik stoji fizično — 3D tu ničesar ne dodajamo.",
    descEn:
      "On a meadow by the village of Otok near Metlika (~10 km north of Griblje) the Partisans laid out an airfield for Allied aircraft in the spring of 1944. The planes landed at blackout, the meadow marked with lanterns. By the end of the war 1,473 wounded were flown from here to Allied hospitals in southern Italy — today a Douglas C-47 Dakota stands guard over the memory. This spot is story-only: the meadow lies before you, the monument stands in the physical world — we add no 3D here.",
    evidenceSi:
      "MVG-013 · RTV Slovenija · Wikipedija (Otok, Metlika) · Wikimedia Commons (dokumentarna fotografija 1944) · koordinata je groba — terenska preverba čaka",
    evidenceEn:
      "MVG-013 · RTV Slovenia · Wikipedia (Otok, Metlika) · Wikimedia Commons (documentary photo 1944) · the coordinate is coarse — field check pending",
    exhibitSlug: "letalisce-otok-1944",
    events: [
      {
        whenSi: "pomlad 1944",
        whenEn: "spring 1944",
        textSi:
          "Partizani uredijo letališče na travniku ob Kolpi — v tajnosti, v velikosti za zavezniška transportna letala.",
        textEn:
          "The Partisans lay out the airfield on a meadow by the Kolpa — in secret, sized for Allied transport aircraft.",
      },
      {
        whenSi: "17. september 1944",
        whenEn: "17 September 1944",
        textSi:
          "Prvo zavezniško pristajanje — pet letali. Ranjenci iz gozdnih bolnišnic prvič letijo proti miru.",
        textEn:
          "The first Allied landing — five aircraft. The wounded of the forest hospitals fly towards peace for the first time.",
      },
      {
        whenSi: "1944 → 1945",
        whenEn: "1944 → 1945",
        textSi:
          "Zračni most: 1473 ranjencev prepeljanih v južno Italijo; rešenih tudi 87 britanskih letalcev, večinoma sestreljenih pilotov.",
        textEn:
          "The air bridge: 1,473 wounded carried to southern Italy; 87 British airmen rescued too, mostly downed pilots.",
      },
      {
        whenSi: "danes",
        whenEn: "today",
        textSi:
          "Spominski Douglas C-47 Dakota stoji pri Otoku; vsako leto vojaki prehodijo spominsko pot Vranov let (Ožbalt → Otok).",
        textEn:
          "The memorial Douglas C-47 Dakota stands at Otok; each year soldiers walk the Vranov let memorial trail (Ožbalt → Otok).",
      },
    ],
  },
  {
    id: "cerkvisce",
    lat: 45.5759667,
    lng: 15.2643167,
    radius: 55,
    anchorId: "anchor-cerkvisce",
    year: 2026,
    miniScene: "cerkvisce",
    titleSi: "Cerkvišče — tri cerkvice, ki jih ni več",
    titleEn: "Cerkvišče — the three churches that are no more",
    descSi:
      "Ime vasi je arheologija sama: tu so stale tri cerkvice, Turki pa so jih ob vpadih (od ~1408) porušili in zažgali. Pred tabo utripajo trije rdeči duhovi — za dve domnevno vaščani še vedo, kje sta stali, za tretjo ne ve nihče; postavitev je INTERPRETACIJA. Ob njih stoji bela kapelica iz leta 1994 — edini kamen, ki danes nosi spomin. Zaselk pripada isti krajevni skupnosti kot Griblje.",
    descEn:
      "The village's name is an archaeology in itself: three churches stood here, and the Turks pulled them down and burned them during the incursions (from ~1408). Before you three red ghosts pulse — for two the villagers still believe they know where they stood, of the third no one knows; the placement is an INTERPRETATION. Beside them stands the white chapel of 1994 — the only stone that still carries the memory. The hamlet belongs to the same local community as Griblje.",
    evidenceSi:
      "MVG-040 · Wikipedija (Cerkvišče) · Občina Črnomelj (KS Griblje = obe naselji) · sidro OSM place node · duhovi = interpretacija (lega tretje neznana)",
    evidenceEn:
      "MVG-040 · Wikipedia (Cerkvišče) · Municipality of Črnomelj (the Griblje LC = both settlements) · OSM place-node anchor · the ghosts are an interpretation (the third position unknown)",
    exhibitSlug: "cerkvisce",
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

/** Je točka oddaljena (izven vasi — lastna vsebina, issue #12)? */
export function isDistantSpot(spot: TimeSpot): boolean {
  return (DISTANT_SPOT_IDS as readonly string[]).includes(spot.id);
}

/** razdalja točke od jedra vasi (m) — za ločitev oddaljenih v UI */
export function spotDistanceFromVillage(spot: TimeSpot): number {
  return distanceM(spot, { lat: 45.5725, lng: 15.2926 });
}
