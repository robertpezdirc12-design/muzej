// ISSUE #3 — raziskovalni in provenienčni model (strojno berljiv)
// Načelo: NIČ IZMIŠLJENEGA. Vsak podatek ima status, vir in — kjer obstaja —
// neposredno povezavo. Negativni rezultati ostanejo vidni.

import type { ResearchStatus } from "./sources";

// ——— 1. STANJE PREPISOV KURRENT ROKOPISOV (issue #3 #4) ——————————

export interface KurrentSeries {
  code: string;
  unitSi: string;
  unitEn: string;
  pages: number;
  pagesTranscribed: number;
  structuredEntries: number;
  status: ResearchStatus;
  noteSi: string;
  noteEn: string;
}

/** Prioriteta prepisa po issue #3: PR, PS, PUA, PZ, nato ostale serije. */
export const KURRENT_SERIES: KurrentSeries[] = [
  {
    code: "PR",
    unitSi: "Opis meje (Grenz-Beschreibung)",
    unitEn: "Boundary description",
    pages: 4,
    pagesTranscribed: 0,
    structuredEntries: 0,
    status: "TO_COLLECT",
    noteSi: "Nemški Kurrent, 4 strani. Prepis ima prednost po issue #3, a še ni izdelan.",
    noteEn: "German Kurrent, 4 pages. Transcription has priority per issue #3 but is not made yet.",
  },
  {
    code: "PS",
    unitSi: "Seznam zemljiških parcel",
    unitEn: "Register of land parcels",
    pages: 143,
    pagesTranscribed: 0,
    structuredEntries: 0,
    status: "TO_COLLECT",
    noteSi: "143 strani parcel po sekcijah I–V; 20 vrstic je v pripravljenem modelu, poln prepis še ni izdelan.",
    noteEn: "143 pages of parcels by sections I–V; 20 rows sit in a prepared model, the full transcription is not made yet.",
  },
  {
    code: "PUA",
    unitSi: "Abecedni seznam lastnikov",
    unitEn: "Alphabetical register of owners",
    pages: 49,
    pagesTranscribed: 2,
    structuredEntries: 21,
    status: "REVIEW",
    noteSi: "Prepisani strani A–B (21 lastnikov) za navzkrižno preverjanje s PT. Strani C–Ž (47) niso prepisane.",
    noteEn: "Pages A–B transcribed (21 owners) for cross-checking against PT. Pages C–Ž (47) are not transcribed.",
  },
  {
    code: "PZ",
    unitSi: "Katastrski cenilni elaborat",
    unitEn: "Cadastral valuation elaborate",
    pages: 71,
    pagesTranscribed: 0,
    structuredEntries: 0,
    status: "TO_COLLECT",
    noteSi: "71 strani ocen in razredov; prepis ni izdelan.",
    noteEn: "71 pages of valuations and classes; transcription not made yet.",
  },
  {
    code: "PT",
    unitSi: "Protokol stavbnih parcel",
    unitEn: "Protocol of building parcels",
    pages: 8,
    pagesTranscribed: 8,
    structuredEntries: 80,
    status: "REVIEW",
    noteSi: "80 stavbnih vrstic (hišne št. 1–98) prebranih s pomočjo strojnega branja; vsi vnosi status REVIEW, čakajo paleografski pregled.",
    noteEn: "80 building rows (house nos. 1–98) read with machine assistance; all entries carry REVIEW status, awaiting palaeographic review.",
  },
  {
    code: "PG",
    unitSi: "Indikacijska skica",
    unitEn: "Indication sketch",
    pages: 1,
    pagesTranscribed: 0,
    structuredEntries: 0,
    status: "TO_COLLECT",
    noteSi: "1 stran; vsebinski prepis ni izdelan.",
    noteEn: "1 page; content transcription not made yet.",
  },
  {
    code: "PV",
    unitSi: "Izkaz rabe zemljišč",
    unitEn: "Statement of land use",
    pages: 1,
    pagesTranscribed: 0,
    structuredEntries: 0,
    status: "TO_COLLECT",
    noteSi: "1 stran; vsebinski prepis ni izdelan.",
    noteEn: "1 page; content transcription not made yet.",
  },
];

// ——— 2. INVENTAR JAVNIH GEODETSKIH VIROV (issue #3 #3) ——————————

export interface GeodataSource {
  id: string;
  nameSi: string;
  nameEn: string;
  provider: string;
  kindSi: string;
  kindEn: string;
  url: string;
  /** ali pokriva območje Griblje */
  coversGriblje: boolean;
  coversNoteSi?: string;
  coversNoteEn?: string;
  licence: string;
  status: ResearchStatus;
  lastVerified: string;
}

export const GEODATA_SOURCES: GeodataSource[] = [
  {
    id: "geo-dmr",
    nameSi: "Državni višinski model 1 m (DMR)",
    nameEn: "National digital elevation model 1 m (DMR)",
    provider: "ARSO (Agencija RS za okolje)",
    kindSi: "raster, višine (EPSG:3794)",
    kindEn: "raster, elevation (EPSG:3794)",
    url: "https://gis.arso.gov.si/arcgis/rest/services/Slovenija_DMR_D96TM/ImageServer",
    coversGriblje: true,
    coversNoteSi: "Preverjeno z vzorčenjem višin na območju Griblje (151–177 m).",
    coversNoteEn: "Verified by sampling elevations in the Griblje area (151–177 m).",
    licence: "javna storitev ARSO, brezplačno",
    status: "VERIFIED",
    lastVerified: "2026-10-07",
  },
  {
    id: "geo-dof",
    nameSi: "Ortofoto DOF (cikli 1990–2024)",
    nameEn: "Orthophoto DOF (cycles 1990–2024)",
    provider: "ARSO",
    kindSi: "raster, ortofoto (25–50 cm)",
    kindEn: "raster, orthophoto (25–50 cm)",
    url: "https://gis.arso.gov.si/arcgis/rest/services/DOF_D96TM_2022_2023_2024/MapServer",
    coversGriblje: true,
    coversNoteSi: "Celotna Slovenija; sloji po ciklih (2019, 2018–2021, 2022–2024 …).",
    coversNoteEn: "All of Slovenia; layers per cycle (2019, 2018–2021, 2022–2024 …).",
    licence: "javna storitev ARSO, brezplačno",
    status: "VERIFIED",
    lastVerified: "2026-10-07",
  },
  {
    id: "geo-lidar-hs",
    nameSi: "LiDAR senčenje (hillshade)",
    nameEn: "LiDAR hillshade",
    provider: "ARSO",
    kindSi: "WMTS raster (nivoji 0–16)",
    kindEn: "WMTS raster (levels 0–16)",
    url: "https://gis.arso.gov.si/arcgis/rest/services/Lidar_hillshade_D96TM/MapServer/WMTS/1.0.0/WMTSCapabilities.xml",
    coversGriblje: false,
    coversNoteSi:
      "Storitev pokriva Slovenijo, a LiDAR 2014–2015 za blok b_16 (Griblje, liste 519_46–526_52) ni bil sneman — 0 listov. Vzorčni bloki: b_11–15, b_21–26, b_31–37 (74 % države).",
    coversNoteEn:
      "The service covers Slovenia but the 2014–2015 LiDAR for block b_16 (Griblje, tiles 519_46–526_52) was not flown — 0 tiles. Scanned blocks: b_11–15, b_21–26, b_31–37 (74 % of the country).",
    licence: "javna storitev ARSO, brezplačno",
    status: "NOT_FOUND",
    lastVerified: "2026-10-07",
  },
  {
    id: "geo-clss",
    nameSi: "CLSS — ciklično lasersko skeniranje (2023+)",
    nameEn: "CLSS — cyclic laser scanning (2023+)",
    provider: "GURS + Flycom",
    kindSi: "3D portal: oblak točk GKOT, DMR, DSM, PAS",
    kindEn: "3D portal: GKOT point cloud, DMR, DSM, PAS",
    url: "https://clss.si",
    coversGriblje: true,
    coversNoteSi: "Slovenija je v celoti lasersko posneta v novem ciklu (pregledovalnik 3D podatkov).",
    coversNoteEn: "Slovenia is fully laser-scanned in the new cycle (3D data viewer).",
    licence: "javni dostop",
    status: "VERIFIED",
    lastVerified: "2026-10-07",
  },
  {
    id: "geo-gurs-eprostor",
    nameSi: "GURS e-prostor (JV/JGP ortofoto, kataster)",
    nameEn: "GURS e-prostor (JV/JGP orthophoto, cadastre)",
    provider: "GURS (Geodetska uprava RS)",
    kindSi: "spletni pregledovalniki + odprti podatki",
    kindEn: "web viewers + open data",
    url: "https://ipi.eprostor.gov.si/jv/",
    coversGriblje: true,
    coversNoteSi: "JV vključuje 3D pogled; JGP brezplačen izpis; kataster kn s slikovnim prikazom.",
    coversNoteEn: "JV includes a 3D view; JGP free download; cadastre kn with imagery display.",
    licence: "odprto, brez prijave (podatki GURS)",
    status: "VERIFIED",
    lastVerified: "2026-10-07",
  },
  {
    id: "geo-gurs-wms",
    nameSi: "GURS ortofoto WMS",
    nameEn: "GURS orthophoto WMS",
    provider: "GURS",
    kindSi: "WMS storitev",
    kindEn: "WMS service",
    url: "https://eprostor.gov.si/imps",
    coversGriblje: false,
    coversNoteSi:
      "Neposredni WMS endpoint ni potrjen: egp.gu.gov.si je upokojen (DNS), wms.eprostor.gov.si se ne razreša. Metapodatki INSPIRE so na eprostor.gov.si/imps.",
    coversNoteEn:
      "A direct WMS endpoint is not confirmed: egp.gu.gov.si is retired (DNS), wms.eprostor.gov.si does not resolve. INSPIRE metadata is at eprostor.gov.si/imps.",
    licence: "—",
    status: "NOT_FOUND",
    lastVerified: "2026-10-07",
  },
  {
    id: "geo-3dkd",
    nameSi: "3DKD — 3D stavbni kataster",
    nameEn: "3DKD — 3D building cadastre",
    provider: "GURS",
    kindSi: "3D stavbni podatki",
    kindEn: "3D building data",
    url: "https://ipi.eprostor.gov.si/jv/",
    coversGriblje: false,
    coversNoteSi:
      "Javni izdelek z imenom 3DKD ni najden. GURS javne 3D možnosti so JV 3D pogled in CLSS; 3D kataster/BIM je v razvoju. Alternativa za 3D stavbe: CLSS DSM.",
    coversNoteEn:
      "No public product named 3DKD was found. GURS public 3D options are the JV 3D view and CLSS; a 3D cadastre/BIM is in development. Alternative for 3D buildings: CLSS DSM.",
    licence: "—",
    status: "NOT_FOUND",
    lastVerified: "2026-10-07",
  },
  {
    id: "geo-osm",
    nameSi: "OpenStreetMap",
    nameEn: "OpenStreetMap",
    provider: "skupnost OSM",
    kindSi: "rastrske ploščice + vektorski podatki",
    kindEn: "raster tiles + vector data",
    url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    coversGriblje: true,
    licence: "ODbL (podatki), © prispevali OSM (obvezna atribucija)",
    status: "VERIFIED",
    lastVerified: "2026-10-07",
  },
];

// ——— 3. ŠOLSKI ARHIVSKI VIR 4118864 (issue #3 #5) ——————————

export interface SchoolArchiveUnit {
  vacId: string;
  vacUrl: string;
  signature: string;
  titleSi: string;
  titleEn: string;
  fundSi: string;
  archiveSi: string;
  years: string;
  contentSi: string;
  contentEn: string;
  accessSi: string;
  status: ResearchStatus;
  lastVerified: string;
}

export const SCHOOL_ARCHIVE: {
  museumRef: string;
  units: SchoolArchiveUnit[];
  chronicle: {
    status: ResearchStatus;
    whereSi: string;
    whereEn: string;
    noteSi: string;
    noteEn: string;
  };
} = {
  museumRef: "MVG-026",
  units: [
    {
      vacId: "4118864",
      vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=4118864",
      signature: "SI_ZAL_ČRN/0001/001/00012",
      titleSi: "Šolski list s prilogami: Državna osnovna šola Griblje",
      titleEn: "School file with annexes: State primary school Griblje",
      fundSi: "SI_ZAL_ČRN/0001 Okrajno glavarstvo Črnomelj (1861–1943), podserija 001 šolski listi",
      archiveSi: "Zgodovinski arhiv Ljubljana, Enota za Dolenjsko in Belo krajino Novo mesto (ZAL NME)",
      years: "1929–1941",
      contentSi:
        "Šolski list s prilogo: opis kraja, poročilo. Slovenski in srbohrvaški jezik, latinica in cirilica (tipkopis). 4 tehnične enote, ovoj 12. Kopija digitalizirana, datoteke v VAČ niso priključene — za digitalno kopijo je treba zaprositi ZAL NME.",
      contentEn:
        "School file with an annex: description of the place, a report. Slovenian and Serbo-Croatian, Latin and Cyrillic script (typewritten). 4 technical units, box 12. A digitised copy exists but no files are attached in VAČ — request ZAL NME for the digital copy.",
      accessSi: "javno dostopno (konec nedostopnosti 31. 12. 1941)",
      status: "DOCUMENTED",
      lastVerified: "2026-10-07",
    },
    {
      vacId: "747512",
      vacUrl: "https://vac.sjas.gov.si/vac/search/details?id=747512",
      signature: "SI_ZAL_NME/0234/003/096",
      titleSi: "Osnovna šola Črnomelj, podružnica Griblje",
      titleEn: "Primary school Črnomelj, branch school Griblje",
      fundSi: "SI_ZAL_NME/0234 Zavod RS za šolstvo OE Novo mesto, podserija 003 spisi šol",
      archiveSi: "Zgodovinski arhiv Ljubljana, Enota za Dolenjsko in Belo krajino Novo mesto (ZAL NME)",
      years: "1970–1982",
      contentSi:
        "Poročila o pregledu pouka in šole 1970–72, hospitacijska poročila 1974–75, poročilo o pedagoškem nadzoru 1982.",
      contentEn:
        "Reports on teaching and school inspections 1970–72, observation reports 1974–75, a pedagogical supervision report 1982.",
      accessSi: "javno dostopno",
      status: "DOCUMENTED",
      lastVerified: "2026-10-07",
    },
  ],
  chronicle: {
    status: "REVIEW",
    whereSi: "Najverjetneje pri podružnični šoli Griblje (OŠ Loka Črnomelj)",
    whereEn: "Most probably with the Griblje branch school (OŠ Loka Črnomelj)",
    noteSi:
      "Šola dejavno navaja šolsko kroniko (gradnja ~1888, prvo šolsko leto 1889/90, prvi učitelj Peter Kambič, 66 učiteljev v 100 letih). Trditev MVG-026, da je kronika v Slovenskem šolskem muzeju, NI bila potrjena — Slovenski šolski muzej izdaja revijo 'Šolska kronika', kar je verjeten vir zamenjave. Popravek statusa: REVIEW, dokler hranilnik ne potrdi.",
    noteEn:
      "The school actively cites the school chronicle (built ~1888, first school year 1889/90, first teacher Peter Kambič, 66 teachers over 100 years). The MVG-026 claim that the chronicle is kept in the Slovenian School Museum could NOT be verified — the Slovenian School Museum publishes the journal 'Šolska kronika', a likely source of confusion. Status correction: REVIEW until the keeper confirms.",
  },
};

// ——— 4. GASPARI — stopnja dokazljivosti (issue #3 #6) ——————————

export const GASPARI_RESEARCH: {
  personSi: string;
  personEn: string;
  status: ResearchStatus;
  mentionSi: string;
  mentionEn: string;
  primaryObject: null;
  noteSi: string;
  noteEn: string;
  lastVerified: string;
} = {
  personSi: "Maksim Gaspari (1883–1980), slikar",
  personEn: "Maksim Gaspari (1883–1980), painter",
  status: "TO_COLLECT",
  mentionSi:
    "V zbirki je omenjen izključno sekundarno: v zapisu MVG-010 (Niko Županič) kot soavtor najstarejših upodobitev vasi in njenih ljudi skupaj z Ivanom Vavpotičem.",
  mentionEn:
    "Mentioned in the collection only secondarily: in record MVG-010 (Niko Županič) as co-author of the oldest depictions of the village and its people together with Ivan Vavpotič.",
  primaryObject: null,
  noteSi:
    "Primarni digitalni predmet (inventarna številka, datum, avtor, slika, pravni status) ne obstaja v zbirki in NI potrjen. Predmet se ne sme označiti kot potrjen brez primarnega dokaza — iskanje v SEM in drugih zbirkah je naslednji korak (TO_COLLECT).",
  noteEn:
    "No primary digital object (inventory number, date, author, image, legal status) exists in the collection and none is confirmed. The object must not be marked as confirmed without primary evidence — searching SEM and other collections is the next step (TO_COLLECT).",
  lastVerified: "2026-10-07",
};

// ——— 5. F0000212 — popolna provenienčna pot (issue #3 #7) ——————————

export const F0000212_PROVENANCE: {
  id: string;
  holder: string;
  classificationSi: string;
  classificationEn: string;
  descriptionSi: string;
  descriptionEn: string;
  creator: null;
  date: null;
  rightsSi: string;
  rightsEn: string;
  museumRef: string;
  houseLink: {
    houseNo: string;
    parcel: string;
    status: ResearchStatus;
    noteSi: string;
    noteEn: string;
  };
  chain: { stepSi: string; stepEn: string; status: ResearchStatus }[];
  lastVerified: string;
} = {
  id: "F0000212",
  holder: "Slovenski etnografski muzej (SEM), digitalne zbirke",
  classificationSi: "hiša (klassifikacija SEM)",
  classificationEn: "house (SEM classification)",
  descriptionSi:
    "Enonadstropna hiša na pero, rojstna hiša dr. Nika Županiča. Belokranjska hiša z leseno galerijo na dvoriščni strani, pred njo človek na klopci in sveže razžagani hlodi.",
  descriptionEn:
    "A one-storey house with a gallery, the birth house of Dr. Niko Županič. A Bela krajina house with a wooden gallery on the courtyard side, a person on a bench in front and freshly sawn logs.",
  creator: null,
  date: null,
  rightsSi: "SEM digitalne zbirke — 'navedi vir'; reproduciranje zahteva soglasje SEM",
  rightsEn: "SEM digital collections — 'cite the source'; reproduction requires SEM consent",
  museumRef: "MVG-010",
  houseLink: {
    houseNo: "73",
    parcel: "942/4",
    status: "REVIEW",
    noteSi:
      "Hipoteza iz starih konceptov: hiša št. 73 (PT str. 6, lastnik Peutinger Mihel — prepis negotov) in parcela 942/4. Povezava ni potrjena s primarnim virom — SEM fotografija ni geometric locirana, hišna številka na njej ni razvidna.",
    noteEn:
      "Hypothesis from old concepts: house no. 73 (PT p. 6, owner Peutinger Mihel — uncertain reading) and parcel 942/4. The link is not confirmed by a primary source — the SEM photograph is not geolocated and no house number is visible on it.",
  },
  chain: [
    { stepSi: "SEM, digitalne zbirke — zapis F0000212", stepEn: "SEM, digital collections — record F0000212", status: "DOCUMENTED" },
    { stepSi: "opis vsebine (hiša na pero, rojstna hiša Županiča)", stepEn: "content description (gallery house, Županič birth house)", status: "DOCUMENTED" },
    { stepSi: "fotograf / datum snemanja", stepEn: "photographer / shooting date", status: "TO_COLLECT" },
    { stepSi: "identifikacija hiše → hišna št. 73 (PT 1825)", stepEn: "house identification → house no. 73 (PT 1825)", status: "REVIEW" },
    { stepSi: "parcela 942/4 → kataster 1825 (PS)", stepEn: "parcel 942/4 → 1825 cadastre (PS)", status: "TO_COLLECT" },
    { stepSi: "današnja lokacija hiše (ali stoji še?)", stepEn: "today's location of the house (still standing?)", status: "TO_COLLECT" },
  ],
  lastVerified: "2026-10-07",
};

// ——— 6. ZEMLJEVID 1812 — dokumentiran vir + pot do georeference (issue #3 #1) —

export const MAP_1812: {
  imageRef: string;
  museumRef: string;
  actualSource: {
    author: string;
    year: number;
    source: string;
    sourceUrl: string;
    licence: string;
    isPeriodOriginal: false;
    noteSi: string;
    noteEn: string;
  };
  periodOriginals: { title: string; sourceUrl: string; licence: string }[];
  bounds: { north: number; south: number; west: number; east: number };
  georeferencePath: {
    status: ResearchStatus;
    methodSi: string;
    methodEn: string;
  };
  lastVerified: string;
} = {
  imageRef: "/images/authentic/ilirske-province-1812.jpg",
  museumRef: "MVG-092",
  actualSource: {
    author: "TRAJAN 117",
    year: 2018,
    source: "Wikimedia Commons — File: Illyrian Provinces (1812).svg",
    sourceUrl: "https://commons.wikimedia.org/wiki/File:Illyrian_Provinces_(1812).svg",
    licence: "CC BY-SA 3.0 (obvezna atribucija avtorja)",
    isPeriodOriginal: false,
    noteSi:
      "Sodoben (2018) vektor zemljevid Ilirskih provinc — politični pregled, ne projekcijski list iz 1812. Atribucija je v zapisu MVG-092 (imageCredit).",
    noteEn:
      "A modern (2018) vector map of the Illyrian Provinces — a political overview, not an 1812 projection sheet. Attribution is in record MVG-092 (imageCredit).",
  },
  periodOriginals: [
    {
      title: "Provinces Illyriennes Servie et Bosnie 1812 (izvirnik 1812)",
      sourceUrl: "https://commons.wikimedia.org/wiki/File:Provinces_Illyriennes_Servie_et_Bosnie_1812.jpg",
      licence: "javna last (Public Domain)",
    },
    {
      title: "Carte des Provinces Illyriennes (Lapie/Tardieu, Internet Archive)",
      sourceUrl: "https://commons.wikimedia.org/",
      licence: "javna last (Public Domain)",
    },
  ],
  bounds: { north: 46.7, south: 42.4, west: 13.3, east: 19.3 },
  georeferencePath: {
    status: "TO_COLLECT",
    methodSi:
      "Pot do georeferenciranega sloja: (1) pridobi obdobjeni izvirnik z Wikimedie (javna last); (2) afina transformacija na kontrolne točke (enaka metoda kot N83 A01/A02 — Dunaj/Trst/Zagreb/rečne meje); (3) seznam sloj v Atlasu za obdobje 1809–1813. Današnji vir je politični pregled brez projekcije in zato za georeferenco neuporaben.",
    methodEn:
      "Path to a georeferenced layer: (1) acquire a period original from Wikimedia (public domain); (2) an affine transformation on control points (same method as N83 A01/A02 — Vienna/Trieste/Zagreb/river boundaries); (3) add the layer to the Atlas for the 1809–1813 period. The current source is a political overview without projection and is therefore unusable for georeferencing.",
  },
  lastVerified: "2026-10-07",
};

// ——— 7. NESNOVNA DEDIŠČINA / USTNA ZGODOVINA (issue #3 #14) ——————————

export interface OralInterview {
  id: string;
  narratorSi: string;
  narratorEn: string;
  /** enoten zapis YYYY-MM-DD */
  date: string;
  locationSi: string;
  locationEn: string;
  interviewerSi: string;
  interviewerEn: string;
  /** soglasje za uporabo posnetka/prepisa */
  consent: { given: boolean; scopeSi: string; scopeEn: string };
  media: { audio: string | null; video: string | null };
  /** prepis z datumom in različico */
  transcript: { textSi: string; textEn: string; version: string } | null;
  relatedMuseumRefs: string[];
  rightsSi: string;
  rightsEn: string;
  status: ResearchStatus;
}

/** PRAZNO — brez izmišljene vsebine. Model čaka prve posnete intervjuje. */
export const ORAL_INTERVIEWS: OralInterview[] = [];

export interface OralTopic {
  id: string;
  topicSi: string;
  topicEn: string;
  fromOldResearchSi: string;
  fromOldResearchEn: string;
  status: ResearchStatus;
}

export const ORAL_TOPICS: OralTopic[] = [
  {
    id: "oral-pasuljada",
    topicSi: "Pasuljada",
    topicEn: "The bean feast (pasuljada)",
    fromOldResearchSi: "Izpostavljena v stari raziskavi kot tema za pričevanja domačinov.",
    fromOldResearchEn: "Highlighted in the old research as a topic for villagers' testimonies.",
    status: "TO_COLLECT",
  },
  {
    id: "oral-tamburasi",
    topicSi: "Tamburaši",
    topicEn: "Tamburica players",
    fromOldResearchSi: "Izpostavljena v stari raziskavi; povezava z MVG-026 (učiteljica Amalija Uršič je vasi prinesla tamburo).",
    fromOldResearchEn: "Highlighted in the old research; link to MVG-026 (teacher Amalija Uršič brought the tambura to the village).",
    status: "TO_COLLECT",
  },
  {
    id: "oral-dogodki",
    topicSi: "Lokalni dogodki",
    topicEn: "Local events",
    fromOldResearchSi: "Izpostavljena v stari raziskavi kot tema za ustno zgodovino.",
    fromOldResearchEn: "Highlighted in the old research as an oral-history topic.",
    status: "TO_COLLECT",
  },
  {
    id: "oral-sola",
    topicSi: "Šolski spomini",
    topicEn: "School memories",
    fromOldResearchSi: "Izpostavljena v stari raziskavi; povezava z MVG-026 in šolskim arhivom ZAL NME (4118864, 747512).",
    fromOldResearchEn: "Highlighted in the old research; link to MVG-026 and the ZAL NME school archive (4118864, 747512).",
    status: "TO_COLLECT",
  },
  {
    id: "oral-pricevanja",
    topicSi: "Pričevanja domačinov",
    topicEn: "Villagers' testimonies",
    fromOldResearchSi: "Izpostavljena v stari raziskavi kot splošna tema.",
    fromOldResearchEn: "Highlighted in the old research as a general topic.",
    status: "TO_COLLECT",
  },
];

// ——— 8. PRENOS IZ ARHIVA markec-group/muzej-arhiv (issue #16) ——————————

/**
 * ISSUE #16 — revizija prenosa iz arhiviranega repozitorija.
 *
 * Programatska primerjava (2026-10-07) je ugotovila: NOV repozitorij je
 * striktni nadnabor arhiva. Arhiv vsebuje star podatkovni model
 * (exhibits/extra/meta/events, 101 slik, 3D model cerkve) — vse to je v
 * novem repu enako ali izboljšano. Celoten ATLAS 1825 / Kurrent sloj v
 * arhivu NI OBSTOJAL (niti v enem od 27 commitov) — vse Kurrent raziskave
 * so nastale izključno v novem repozitoriju.
 *
 * Metoda primerjave (dejavstva, ne ugibanja): klon + unshallow (27
 * commitov), MD5 kontrolne vsote vseh 106 datotek public/, polje-po-polju
 * diff JSON zapisov (po museumNo), primerjava množic 589 virov, pregled
 * vseh 211 datotek, ki so kdarkoli obstajale v zgodovini arhiva.
 */
export interface ArchiveTransferRow {
  /** področje primerjave */
  areaSi: string;
  areaEn: string;
  /** dejansko stanje v arhivu (številke iz datotek) */
  archiveSi: string;
  archiveEn: string;
  /** dejansko stanje v novem muzeju */
  currentSi: string;
  currentEn: string;
  /** izvedena akcija */
  actionSi: string;
  actionEn: string;
  /** število prenesenih vnosov (issue #16: 0 = že prisotno) */
  transferred: number;
}

export const ARCHIVE_TRANSFER_ROWS: ArchiveTransferRow[] = [
  {
    areaSi: "Raziskovalni zapisi (exhibits.json)",
    areaEn: "Research records (exhibits.json)",
    archiveSi: "113 zapisov",
    archiveEn: "113 records",
    currentSi: "113 istih zapisov (isti museumNo/slug); 3 zapisi z GeoTruth popravkom koordinat (MVG-002, -003, -029 → uradni EŠD 2122)",
    currentEn: "113 identical records (same museumNo/slug); 3 with GeoTruth coordinate corrections (MVG-002, -003, -029 → official EŠD 2122)",
    actionSi: "0 prenosov — novi repo je natančnejši (koordinate arhiva so stare, napačne ~500–790 m)",
    actionEn: "0 transfers — the new repo is more accurate (archive coordinates are old, ~500–790 m off)",
    transferred: 0,
  },
  {
    areaSi: "Viri",
    areaEn: "Sources",
    archiveSi: "589 virov",
    archiveEn: "589 sources",
    currentSi: "589 istih virov (identična množica ID-jev)",
    currentEn: "589 identical sources (identical ID set)",
    actionSi: "0 prenosov — brez razlike",
    actionEn: "0 transfers — no difference",
    transferred: 0,
  },
  {
    areaSi: "Kurrent: PT (protokol stavbnih parcel)",
    areaEn: "Kurrent: PT (building parcels protocol)",
    archiveSi: "serija v arhivu NI obstajala (0 datotek, 0 commitov)",
    archiveEn: "series never existed in the archive (0 files, 0 commits)",
    currentSi: "8/8 strani, 80 stavbnih vrstic, status REVIEW",
    currentEn: "8/8 pages, 80 building rows, REVIEW status",
    actionSi: "0 prenosov — prepis je izključno delo novega repa; pregled ni potreben",
    actionEn: "0 transfers — the transcription is exclusively the new repo's work; no re-reading needed",
    transferred: 0,
  },
  {
    areaSi: "Kurrent: PUA (abecedni seznam lastnikov)",
    areaEn: "Kurrent: PUA (alphabetical owners register)",
    archiveSi: "serija v arhivu NI obstajala",
    archiveEn: "series never existed in the archive",
    currentSi: "2 strani (A–B), 21 lastnikov, status REVIEW",
    currentEn: "2 pages (A–B), 21 owners, REVIEW status",
    actionSi: "0 prenosov — v arhivu ni bilo dodatnih lastnikov",
    actionEn: "0 transfers — no additional owners existed in the archive",
    transferred: 0,
  },
  {
    areaSi: "Kurrent: PS (seznam zemljiških parcel)",
    areaEn: "Kurrent: PS (land parcels register)",
    archiveSi: "serija v arhivu NI obstajala",
    archiveEn: "series never existed in the archive",
    currentSi: "20 vrstic v pripravljenem modelu; poln 143-stranski prepis TO_COLLECT",
    currentEn: "20 rows in a prepared model; the full 143-page transcription is TO_COLLECT",
    actionSi: "0 prenosov — arhiv ni vseboval parcelnih vzorcev",
    actionEn: "0 transfers — the archive contained no parcel samples",
    transferred: 0,
  },
  {
    areaSi: "Kurrent: PR, PZ, PG, PV",
    areaEn: "Kurrent: PR, PZ, PG, PV",
    archiveSi: "serije v arhivu NI obstajale",
    archiveEn: "series never existed in the archive",
    currentSi: "model + status TO_COLLECT (prepis ni izdelan)",
    currentEn: "model + TO_COLLECT status (transcription not made)",
    actionSi: "0 prenosov — ni bilo česa prenesti",
    actionEn: "0 transfers — nothing to transfer",
    transferred: 0,
  },
  {
    areaSi: "Hiše / parcele / Atlas 1825",
    areaEn: "Houses / parcels / Atlas 1825",
    archiveSi: "atlas v arhivu NI obstajal (src/data/atlas/ ni v nobenem commitu)",
    archiveEn: "atlas never existed in the archive (src/data/atlas/ in no commit)",
    currentSi: "Atlas 1825: sources (N083*), houses (80), research, geotruth, reconciliation, coverage",
    currentEn: "Atlas 1825: sources (N083*), houses (80), research, geotruth, reconciliation, coverage",
    actionSi: "0 prenosov — celoten atlas je nastal v novem repu",
    actionEn: "0 transfers — the entire atlas originated in the new repo",
    transferred: 0,
  },
  {
    areaSi: "Dogodki (events.json)",
    areaEn: "Events (events.json)",
    archiveSi: "9 dogodkov",
    archiveEn: "9 events",
    currentSi: "11 dogodkov (2 dodana v novem repu — 500-letnice 2026)",
    currentEn: "11 events (2 added in the new repo — 2026 anniversaries)",
    actionSi: "0 prenosov — novi repo je nadnabor",
    actionEn: "0 transfers — the new repo is a superset",
    transferred: 0,
  },
  {
    areaSi: "Slike in 3D modeli (public/)",
    areaEn: "Images and 3D models (public/)",
    archiveSi: "106 datotek (101 slik + cerkev-sv-vida.glb + logotip + …)",
    archiveEn: "106 files (101 images + cerkev-sv-vida.glb + logo + …)",
    currentSi: "vseh 106 prisotnih z IDENTIČNIMI kontrolnimi vsotami (MD5) + 41 novih (atlas/qr/panorame/audio)",
    currentEn: "all 106 present with IDENTICAL checksums (MD5) + 41 new ones (atlas/qr/panoramas/audio)",
    actionSi: "0 prenosov — nobena datoteka ne manjka",
    actionEn: "0 transfers — no file is missing",
    transferred: 0,
  },
  {
    areaSi: "extra.json (postaje življenja, trditve, sorodni, sprehod)",
    areaEn: "extra.json (life stations, claims, related, walks)",
    archiveSi: "identična vsebina",
    archiveEn: "identical content",
    currentSi: "identična vsebina",
    currentEn: "identical content",
    actionSi: "0 prenosov — datoteki sta enaki",
    actionEn: "0 transfers — the files are equal",
    transferred: 0,
  },
];

/** Namerno NE preneseno iz arhiva (dokumentirane odločitve). */
export interface ArchiveNonTransfer {
  path: string;
  reasonSi: string;
  reasonEn: string;
}

export const ARCHIVE_NON_TRANSFERS: ArchiveNonTransfer[] = [
  {
    path: "download/README.md",
    reasonSi: "Vsebina: »Here are all the generated files.« — mapo generiranih (neraziskovalnih) datotek je arhiv sam izločil prek .vercelignore; ni raziskovalna vsebina.",
    reasonEn: "Content: “Here are all the generated files.” — the folder of generated (non-research) files was itself excluded via .vercelignore; not research content.",
  },
  {
    path: ".gitlab-ci.yml",
    reasonSi: "CI konfiguracija, namerno odstranjena v novem repu (GitLab CI brez potrjene kartice ni mogel poganjati jobov; primarna pot je Vercel integracija). Infrastruktura, ne vsebina.",
    reasonEn: "CI configuration, deliberately removed in the new repo (GitLab CI without a confirmed card could not run jobs; the Vercel integration is the primary path). Infrastructure, not content.",
  },
];

/** Skupni revizijski zapis issue #16 (strojno berljiv). */
export const ARCHIVE_TRANSFER_AUDIT = {
  issue: 16,
  comparedAt: "2026-10-07",
  archiveRepo: {
    path: "markec-group/muzej-arhiv",
    gitlabProjectId: 87313405,
    archived: true,
    headSha: "f519bd95ddec43a699ffa4373b5a75fef0eacead",
    commits: 27,
    /** vseh datotek, ki so kdarkoli obstajale v zgodovini */
    filesEverInHistory: 211,
    srcFiles: 78,
    publicFiles: 106,
  },
  canonicalRepo: {
    path: "robert.pezdirc12/muzej",
    headShaAtComparison: "19a6b7cfb56abae0a45b35264df2a33b5c181869",
  },
  methodSi:
    "Klon arhiva + unshallow (27 commitov); MD5 kontrolne vsote vseh datotek public/; polje-po-polju diff exhibits/extra/meta/events po museumNo; primerjava množic virov; pregled vseh 211 datotek zgodovine; iskanje Kurrent/N083/PUA po celotni zgodovini (0 zadetkov).",
  methodEn:
    "Archive clone + unshallow (27 commits); MD5 checksums of all public/ files; field-by-field diff of exhibits/extra/meta/events by museumNo; source-set comparison; review of all 211 files in history; Kurrent/N083/PUA search across the whole history (0 hits).",
  verdictSi:
    "Novi muzej je striktni nadnabor arhiva: 0 manjkajočih raziskav, 0 manjkajočih virov, 0 manjkajočih datotek z vsebino. Kurrent/Atlas sloj v arhivu nikoli ni obstajal — prenos ni bil potreben in NIČ ni bilo podvojeno.",
  verdictEn:
    "The new museum is a strict superset of the archive: 0 missing research, 0 missing sources, 0 missing content files. The Kurrent/Atlas layer never existed in the archive — no transfer was needed and NOTHING was duplicated.",
  totalTransferredEntries: 0,
};
