import exhibitsRaw from "@/data/museum/exhibits.json";
import eventsRaw from "@/data/museum/events.json";
import metaRaw from "@/data/museum/meta.json";
import extraRaw from "@/data/museum/extra.json";

/* ─────────────────────────  TIPI  ───────────────────────── */

export type EvidenceCode =
  | "DOCUMENTED"
  | "CORROBORATED"
  | "TESTIMONY"
  | "TRADITION"
  | "UNVERIFIED"
  | "TO_COLLECT";

export type CategoryCode =
  | "kraj"
  | "sege"
  | "vojna"
  | "gospodarstvo"
  | "narava"
  | "kolpa";

export interface MuseumSource {
  id: string;
  sourceKey: string;
  nameSi: string | null;
  nameEn: string | null;
  sourceType: string | null;
  license: string | null;
  url: string | null;
  noteSi: string | null;
  noteEn: string | null;
  creator: string | null;
  licenseUrl: string | null;
  attribution: string | null;
  restrictions: string | null;
}

export interface Exhibit {
  id: string;
  slug: string;
  museumNo: string;
  category: CategoryCode;
  titleSi: string;
  titleEn: string;
  periodSi: string;
  periodEn: string;
  summarySi: string;
  summaryEn: string;
  storySi: string;
  storyEn: string;
  evidenceStatus: EvidenceCode;
  image: string | null;
  imageCredit: string | null;
  model3dUrl: string | null;
  model3dCredit: string | null;
  yearFrom: number | null;
  yearTo: number | null;
  lat: number | null;
  lng: number | null;
  coordsApprox: boolean;
  featured: boolean;
  sortOrder: number;
  sources: MuseumSource[];
}

export interface MuseumEvent {
  id: string;
  titleSi: string;
  titleEn: string;
  descriptionSi: string;
  descriptionEn: string;
  startsAt: string;
  locationSi: string | null;
  locationEn: string | null;
  eventType: string | null;
  isExternal: boolean;
  externalUrl: string | null;
}

export interface LifeStation {
  year: string;
  stage: string;
  description: string;
  evidence: string | null;
  sourceUrl: string | null;
  sourceName: string | null;
}

export interface Claim {
  text: string;
  evidence: string | null;
  confidence: string | null;
  sourceUrl: string | null;
  sourceName: string | null;
}

export interface RelatedEntry {
  slug: string;
  museumNo: string;
  title: string;
  reasons: string[];
}

export interface WalkInfo {
  name: string;
  station: number | null;
  total: number | null;
  note: string | null;
  next: string | null;
}

export interface ExhibitExtra {
  slug: string;
  lifeStations: LifeStation[];
  claims: Claim[];
  related: RelatedEntry[];
  walk: WalkInfo | null;
}

interface StoryRecord {
  kind: string;
  title: { sl?: string; en?: string } | string;
  text: { sl?: string; en?: string } | string;
  /** meta.json: attribution je dvojezični objekt { sl, en } */
  attribution: { sl?: string; en?: string } | string | null;
  evidenceStatus: string;
}

/* ─────────────────────────  PODATKI  ───────────────────────── */

export const exhibits: Exhibit[] = (
  exhibitsRaw as { count: number; exhibits: Exhibit[] }
).exhibits;

export const events: MuseumEvent[] = (
  eventsRaw as { count: number; events: MuseumEvent[] }
).events;

const meta = metaRaw as {
  museum: Record<string, unknown>;
  counts: Record<string, number>;
  evidenceScale: { code: EvidenceCode; labelSi: string; labelEn: string }[];
  stories: StoryRecord[];
};

export const museumInfo = meta.museum;
export const counts = meta.counts;
export const evidenceScale = meta.evidenceScale;
export const stories = meta.stories;

const extraMap = extraRaw as Record<string, ExhibitExtra>;
export function getExtra(slug: string): ExhibitExtra | null {
  const e = extraMap[slug];
  if (!e) return null;
  return e;
}

export function getExhibit(slug: string): Exhibit | undefined {
  return exhibits.find((e) => e.slug === slug);
}

export function exhibitsByMuseumNo(): Exhibit[] {
  return [...exhibits].sort((a, b) =>
    a.museumNo.localeCompare(b.museumNo, "sl"),
  );
}

/* ─────────────────────────  SLOVARJI  ───────────────────────── */

export const CATEGORY_LABELS: Record<CategoryCode, { si: string; en: string; icon: string }> = {
  kraj: { si: "Kraji", en: "Places", icon: "MapPin" },
  sege: { si: "Šege in tradicija", en: "Customs & traditions", icon: "Sparkles" },
  vojna: { si: "Vojna in meja", en: "War & border", icon: "Shield" },
  gospodarstvo: { si: "Delo in obrt", en: "Work & crafts", icon: "Wheat" },
  narava: { si: "Narava", en: "Nature", icon: "Leaf" },
  kolpa: { si: "Kolpa", en: "The Kolpa", icon: "Waves" },
};

export const EVIDENCE_LABELS: Record<EvidenceCode, { si: string; en: string; descSi: string; descEn: string }> = {
  DOCUMENTED: {
    si: "dokumentirano",
    en: "documented",
    descSi: "Trditev sloni na arhivskem ali objavljenem dokumentiranem viru.",
    descEn: "The claim rests on an archival or published documented source.",
  },
  CORROBORATED: {
    si: "preverjeno",
    en: "corroborated",
    descSi: "Trditev potrjujejo vsaj dva neodvisna vira.",
    descEn: "The claim is confirmed by at least two independent sources.",
  },
  TESTIMONY: {
    si: "pričevanje",
    en: "testimony",
    descSi: "Trditev temelji na ustnem pričevanjo domačinov.",
    descEn: "The claim is based on oral testimony of locals.",
  },
  TRADITION: {
    si: "tradicija",
    en: "tradition",
    descSi: "Trditev nosi živa tradicija, virov pa še nismo potrdili.",
    descEn: "The claim is carried by living tradition; sources not yet confirmed.",
  },
  UNVERIFIED: {
    si: "nepreverjeno",
    en: "unverified",
    descSi: "Trditev še čaka preverjanje.",
    descEn: "The claim is still awaiting verification.",
  },
  TO_COLLECT: {
    si: "v zbiranju",
    en: "to collect",
    descSi: "Podatke še zbiramo — morda jih imate vi.",
    descEn: "We are still collecting data — perhaps you have it.",
  },
};

export function storyText(story: StoryRecord, lang: "si" | "en"): string {
  if (typeof story.text === "string") return story.text;
  return story.text[lang] ?? story.text.sl ?? "";
}

export function storyTitle(story: StoryRecord, lang: "si" | "en"): string {
  if (typeof story.title === "string") return story.title;
  return story.title[lang] ?? story.title.sl ?? "";
}

export function storyAttribution(
  story: StoryRecord,
  lang: "si" | "en",
): string | null {
  if (story.attribution == null) return null;
  if (typeof story.attribution === "string") return story.attribution;
  return story.attribution[lang] ?? story.attribution.sl ?? null;
}

/* ─────────────────────────  ISKANJE  ───────────────────────── */

/**
 * Zloži diakritike (č→c, š→s, ž→z, à→a …) — zadetki tudi, ko uporabnik tipka
 * brez šumnikov ("sokcev" najde "Šokčev", "zunici" najde "Žuniči").
 */
function foldDiacritics(s: string): string {
  return s
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/đ/g, "d");
}

/** Iskalni kop zapisa: številka, naziva, povzetka, obdobja, polno kuratorsko besedilo, viri, letnice. */
function searchHay(e: Exhibit): string {
  const parts: string[] = [
    e.museumNo,
    e.titleSi,
    e.titleEn,
    e.summarySi,
    e.summaryEn,
    e.periodSi,
    e.periodEn,
    e.storySi,
    e.storyEn,
    e.yearFrom != null ? String(e.yearFrom) : "",
    e.yearTo != null ? String(e.yearTo) : "",
    ...(e.sources ?? []).flatMap((s) => [s.nameSi ?? "", s.nameEn ?? ""]),
  ];
  return foldDiacritics(parts.join(" "));
}

/** Vnaprej zložen iskalni indeks (redko, enkrat ob zagonu — brez dela ob vsakem pritisku tipke). */
const SEARCH_INDEX: { exhibit: Exhibit; hay: string }[] =
  exhibitsByMuseumNo().map((e) => ({ exhibit: e, hay: searchHay(e) }));

export function filterExhibits(
  query: string,
  category: CategoryCode | "all",
  evidence: EvidenceCode | "all",
  featuredOnly: boolean,
): Exhibit[] {
  const q = foldDiacritics(query.trim());
  return SEARCH_INDEX.filter(({ exhibit: e, hay }) => {
    if (featuredOnly && !e.featured) return false;
    if (category !== "all" && e.category !== category) return false;
    if (evidence !== "all" && e.evidenceStatus !== evidence) return false;
    if (q && !hay.includes(q)) return false;
    return true;
  }).map(({ exhibit }) => exhibit);
}

export const STATS = {
  exhibits: exhibits.length,
  sources: counts.sources ?? 589,
  categories: Object.keys(CATEGORY_LABELS).length,
  /** prva pisna omemba vasi Griblje — zapis MVG-001 */
  firstYear:
    exhibits.find((e) => e.slug === "griblje-vas")?.yearFrom ?? 1468,
  images: exhibits.filter((e) => e.image).length,
  bilingual: true as const,
};
