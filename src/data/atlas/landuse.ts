// ATLAS 1825 — RABA TAL in ZASELKI (issue #7; cone zamaknjene po GEOTRUTH, issue #14)
// Vzorci rabe tal so izpeljani iz VLM analize katastrskih listov A01/A02 (2026-10-07)
// in GEOTRUTH afini (issue #14): listi zasidrani na uradni EŠD 2122 — translacija
// −0,005190 lat / −0,001889 lng glede na staro (krožno) georeferenco: reka Kolpa na vzhodnem robu listov, njivski mozaik
// zahodno/severno od vasi, poplavne loke med vasjo in reko, gozdni kompleks na jugu A02.
// Vse cone so približni pravokotniki — status RECONSTRUCTED, natančne meje parcel
// niso vektorsko preslikane (TO_COLLECT).
// Zgodovinska dejstva (Brezov gozd, Goranja lokva, Rudna peč, studi): Wikipedija — Griblje.

export type LandUseKind = "meadow" | "field" | "forest";

export interface LandUseZone {
  id: string;
  kind: LandUseKind;
  labelSi: string;
  labelEn: string;
  /** približen pravokotnik [N, W] → [S, E] (RECONSTRUCTED) */
  bounds: [[number, number], [number, number]];
  status: "RECONSTRUCTED";
  /** delež na listu po VLM analizi (x/y v %) */
  vlmHintSi: string;
  color: string;
  fillColor: string;
  noteSi: string;
  noteEn: string;
}

export const LANDUSE_ZONES: LandUseZone[] = [
  {
    id: "raba-loke",
    kind: "meadow",
    labelSi: "Poplavne loke ob Kolpi",
    labelEn: "Flood meadows along the Kolpa",
    bounds: [[45.5836, 15.2909], [45.5618, 15.2976]],
    status: "RECONSTRUCTED",
    vlmHintSi: "A01: svetlozelene travnine v jedru vasi (x 65–80, y 60–95) in otok ob reki (x 88–91); Kolpa na x 93–99",
    color: "#7d9b76",
    fillColor: "#9ec497",
    noteSi:
      "Kolpa je z naplavljanjem ustvarila rodovitne loke; reka del vode ponika in se pojavlja kot studenci. Cona je pas med jedrom vasi in reko — približno (±100–150 m).",
    noteEn:
      "The Kolpa created fertile meadows through flooding; part of its water sinks and re-emerges as springs. The zone is the strip between the village core and the river — approximate (±100–150 m).",
  },
  {
    id: "raba-njive",
    kind: "field",
    labelSi: "Njivski mozaik (Äcker)",
    labelEn: "Field mosaic (Äcker)",
    bounds: [[45.5836, 15.2681], [45.5700, 15.2861]],
    status: "RECONSTRUCTED",
    vlmHintSi: "A01: bež/rumenkasti mozaik dolgih ozkih parcel s parcelnimi št. (x 55–92, y 5–98), gost na severu (Maloška Pecina) in zahodu (na Lokaže)",
    color: "#c9a35a",
    fillColor: "#e3c887",
    noteSi:
      "Dominantna raba lista A01 (~70–75 %): dolge ozke parcele z rdečimi parcelnimi številkami okoli vasi, razen rečne strani. Vzporedne njivske črte (Gewan) so značilne za franciscejski kataster.",
    noteEn:
      "Dominant land use of sheet A01 (~70–75 %): long narrow parcels with red parcel numbers around the village, except the river side. Parallel field strips (Gewan) are typical of the Franciscean cadastre.",
  },
  {
    id: "raba-gozd",
    kind: "forest",
    labelSi: "Gozdni kompleks na jugu (A02)",
    labelEn: "Southern forest complex (A02)",
    bounds: [[45.5623, 15.2759], [45.5561, 15.2946]],
    status: "RECONSTRUCTED",
    vlmHintSi: "A02: šrafirana območja s simboli dreves v južnem delu (Pod Schattinger, Robar), manjši sestavi na zahodu",
    color: "#5d7a54",
    fillColor: "#79966b",
    noteSi:
      "Na listu A01 velikih gozdnih kompleksov ni — območje je pretežno kmetijsko; gozd se pojavi na južnem robu lista A02. Brezov gozd (izkrčen po 1848) na listih ni izrazito lociran — lega TO_COLLECT.",
    noteEn:
      "Sheet A01 shows no large forest complexes — the area is mostly agricultural; forest appears on the southern edge of sheet A02. The birch forest (cleared after 1848) is not distinctly located on the sheets — position TO_COLLECT.",
  },
];

/** Krajevne posebnosti rabe tal — dokumentirane, brez geometrije (TO_COLLECT) */
export interface LandUseEntity {
  id: string;
  labelSi: string;
  labelEn: string;
  descriptionSi: string;
  descriptionEn: string;
  status: "DOCUMENTED" | "TO_COLLECT";
  /** muzejski zapis */
  museumRef?: string;
}

export const LANDUSE_ENTITIES: LandUseEntity[] = [
  {
    id: "raba-brezov-gozd",
    labelSi: "Brezov gozd",
    labelEn: "Birch forest (Brezov gozd)",
    descriptionSi:
      "Kmetje so po letu 1848 s pomočjo vprežne živine izkrčili brezov gozd; v brezju je nastal kal Goranja lokva, kjer so kopali glino za opeko. Natančna lega na katastrskih listih ni izrazita (TO_COLLECT).",
    descriptionEn:
      "After 1848 farmers cleared the birch forest with draft animals; in the birch grove the Goranja lokva pond was made, where clay for bricks was dug. Its exact position on the cadastral sheets is not distinct (TO_COLLECT).",
    status: "TO_COLLECT",
    museumRef: "MVG-024",
  },
  {
    id: "raba-goranja-lokva",
    labelSi: "Goranja lokva (kal)",
    labelEn: "Goranja lokva (pond)",
    descriptionSi:
      "Kal/lokev v nekdanjem brezju, kjer so kopali glino za opeko; tam so v času pomanjkanja vode tudi pasli živino. Lega: zahodno od Gribelj (ribnik, MVG-016) — natančen položaj lokev TO_COLLECT.",
    descriptionEn:
      "A pond in the former birch grove where clay for bricks was dug; livestock was grazed there in times of water scarcity. Position: west of Griblje (pond, MVG-016) — exact pond position TO_COLLECT.",
    status: "TO_COLLECT",
    museumRef: "MVG-050",
  },
  {
    id: "raba-rudna-pec",
    labelSi: "Rudna peč",
    labelEn: "Rudna peč (iron-ore rock)",
    descriptionSi:
      "Kraj zahodno/severno od vasi, kjer je v plasteh zemlje železova prst — krajevna geološka posebnost, ki se veže na prazgodovinsko in rimske najdbe železa v Beli krajini. Lega TO_COLLECT.",
    descriptionEn:
      "A place west/north of the village where iron-bearing soil lies in layers — a local geological peculiarity linked to prehistoric and Roman iron finds in Bela krajina. Position TO_COLLECT.",
    status: "TO_COLLECT",
  },
  {
    id: "raba-studenci",
    labelSi: "Studenci ob Kolpi",
    labelEn: "Springs along the Kolpa",
    descriptionSi:
      "Velik del vode Kolpe ponika in se ob reki pojavlja v obliki studencev »na vsakem koraku« — vir vode pred vodovodom. Točni studenci niso preslikani (TO_COLLECT).",
    descriptionEn:
      "Much of the Kolpa's water sinks and re-emerges along the river as springs »at every step« — the water source before piped water. Exact springs not mapped (TO_COLLECT).",
    status: "TO_COLLECT",
    museumRef: "MVG-067",
  },
];

/** Zaselki Gribelj — dokumentirana imena (Wikipedija + KS Griblje), razporeditev hiš TO_COLLECT */
export interface Hamlet {
  id: string;
  nameSi: string;
  nameEn: string;
  status: "DOCUMENTED" | "TO_COLLECT";
  noteSi: string;
  noteEn: string;
}

export const HAMLETS: Hamlet[] = [
  {
    id: "zaselek-dolnje",
    nameSi: "Dolnje Griblje",
    nameEn: "Lower Griblje (Dolnje)",
    status: "TO_COLLECT",
    noteSi: "Ime dokumentirano (Wikipedija, KS Griblje). Katere konskripcijske hišne št. (1825) spadajo k zaselku — ni znano; ocena domačinov je zaželena.",
    noteEn: "Name documented (Wikipedia, KS Griblje). Which conscription house numbers (1825) belong to the hamlet is unknown; local estimates welcome.",
  },
  {
    id: "zaselek-brinsko",
    nameSi: "Brinsko selo",
    nameEn: "Brinsko selo",
    status: "TO_COLLECT",
    noteSi: "Ime dokumentirano; muzej išče prvi pisni zapis imena Brinsko selo in natančne meje med zaselki.",
    noteEn: "Name documented; the museum is looking for the first written record of the name Brinsko selo and precise boundaries between hamlets.",
  },
  {
    id: "zaselek-srednje",
    nameSi: "Srednje Griblje",
    nameEn: "Middle Griblje (Srednje)",
    status: "TO_COLLECT",
    noteSi: "Ime dokumentirano (Wikipedija, KS Griblje). Razporeditev hišnih št. TO_COLLECT.",
    noteEn: "Name documented (Wikipedia, KS Griblje). House-number distribution TO_COLLECT.",
  },
  {
    id: "zaselek-gornje",
    nameSi: "Gornje Griblje",
    nameEn: "Upper Griblje (Gornje)",
    status: "TO_COLLECT",
    noteSi: "Ime dokumentirano (Wikipedija, KS Griblje). Razporeditev hišnih št. TO_COLLECT.",
    noteEn: "Name documented (Wikipedia, KS Griblje). House-number distribution TO_COLLECT.",
  },
];
