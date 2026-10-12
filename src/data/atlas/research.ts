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
  /** dokazano prebrane strani (issue #4) — izpis iz surovih raziskav,
   *  ne pavšalni števec; dolžina == pagesTranscribed */
  pagesReadList?: number[];
  /** vzorčene strani znotraj nepresranih odsekov (PZ) — niso polne prepise */
  pagesSampledList?: number[];
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
    pagesTranscribed: 4,
    pagesReadList: [1, 2, 3, 4],
    structuredEntries: 10,
    status: "REVIEW",
    noteSi: "Prepisane vse 4 strani (issue #17, VLM 2026-10-08): naslovnica »Prod N° 218 / Grenz-Beschreibung der Gemeinde GRÜBLE«, splošne mere 1028 × 1884 klafter, točke meje št. 1–10 (prebrano na str. 2, nadaljevanje negotovo 10–20), sosedi (Kraljevina Hrvaška/Weidendorf stabilna, ostali [~]), zaključek »am 8ten April 1825«. 1028 × 1884 kl = 1210,5 jocha — se ujema s PV (<1 %). Strojni prepis = REVIEW.",
    noteEn: "All 4 pages transcribed (issue #17, VLM 2026-10-08): title page »Prod N° 218 / Grenz-Beschreibung der Gemeinde GRÜBLE«, overall dimensions 1028 × 1884 klafter, boundary points nos. 1–10 (read on p. 2, continuation uncertain 10–20), neighbours (Kingdom of Croatia/Weidendorf stable, others [~]), closing »am 8ten April 1825«. 1028 × 1884 kl = 1210.5 joch — matches PV (<1 %). Machine reading = REVIEW.",
  },
  {
    code: "PS",
    unitSi: "Seznam zemljiških parcel",
    unitEn: "Register of land parcels",
    pages: 143,
    pagesTranscribed: 143,
    pagesReadList: Array.from({ length: 143 }, (_, i) => i + 1),
    structuredEntries: 2743,
    status: "REVIEW",
    noteSi: "143 strani parcel; P36 (2026-10-11, issue #10): VSE strani strojno prebrane — 1–4 in 140–143 (struktura + rekapitulacija, issue #17/P5-b) + 5–139 (P36 kampanja: 2743 strukturiranih vrstic, pass-1 vseh strani + pass-2 78 strani z okvarjeno soslednostjo; dokaz research/issue17/ps-raw/ + PS-full.json). STRUKTURA: zvezek pomešan (strani niso v redu parcel — npr. str. 80–82 = parcele 1644–1700); več števčnih nizov — glavne parcele, Waldung (skupna gozdna, brez lastnikov), Schmiegärten (vrtovi), Blatt X (lastno številčenje 1–40); glavni niz sega čez 2840. Končna Summa (str. 143, rdeči tuš): 102 + 2505 = 2607 šteje KATEGORIJE, ne maksimum. PREOSTANE: 3. prehod ~15 dvoumnih strani, klasifikacija sekcij, razdvojitev večkulturnih vrstic (ista parcela več vrstic po kulturah), uskladitev s 2607 — issue #10 odprt. Vsi statusi REVIEW (strojno branje ni dokazni vir).",
    noteEn: "143 pages of parcels; P36 (2026-10-11, issue #10): ALL pages machine-read — 1–4 and 140–143 (structure + recapitulation, issue #17/P5-b) + 5–139 (the P36 campaign: 2,743 structured rows, pass-1 on all pages + pass-2 on 78 pages with broken continuity; evidence research/issue17/ps-raw/ + PS-full.json). STRUCTURE: the volume is shuffled (pages not in parcel order — e.g. pp. 80–82 = parcels 1644–1700); several numbering series — main parcels, Waldung (communal forest, ownerless), Schmiegärten (gardens), Blatt X (own 1–40 numbering); the main series runs past 2840. The final Summa (p. 143, red ink): 102 + 2,505 = 2,607 counts CATEGORIES, not a maximum. REMAINS: a 3rd pass over ~15 ambiguous pages, section classification, splitting multi-culture rows (the same parcel has several rows by culture), matching against 2,607 — issue #10 open. All statuses REVIEW (machine reading is not evidentiary).",
  },
  {
    code: "PUA",
    unitSi: "Abecedni seznam lastnikov",
    unitEn: "Alphabetical register of owners",
    pages: 49,
    pagesTranscribed: 49,
    pagesReadList: Array.from({ length: 49 }, (_, i) => i + 1),
    structuredEntries: 101,
    status: "REVIEW",
    noteSi: "Register prebran V CELIOTI — 49/49 strani, a v DVAH modelih (issue #4 pojasnilo, 2026-10-10): strani 1–2 (A–B, 21 lastnikov) iz prve gradnje so v lastniškem modelu ATLAS_OWNERS prek PT navzkrižij; strani 3–49 (101 vrstic) v PUA_CONTINUATION (issue #17: strani 3–10, 18 vnosov; P3: stran 11, 4 vnosi; P4: strani 12–34, 47 vnosov — priimki H–P vključno s Kirche H. Veith = cerkev sv. Vida; P5-b: strani 35–49, 32 vnosov, zap. št. 69–100 vključno s skupinskimi vnosi »Gemeinde Malfz Brandhof…« in »Uebersprungene Parzellen-Numern«). structuredEntries 101 = SAMO PUA_CONTINUATION (strani 3–49); strani A–B niso v PUA_CONTINUATION. KLJUČNA UGOTOVITEV P4: PUA in PT očitno uporabljata RAZLIČNO številčenje hiš [~] (PUA hiša 6 = Höflehner, PT hiša 6 = Tilel Miho); PUA ohranja št. v območju 41–60, kjer jih PT nima. Vse ostaja REVIEW (strojno branje ni dokazni vir); surovi izpisi v research/p3/pua-raw/ (38 strani) + research/issue17/PUA-more.json.",
    noteEn: "The register read IN FULL — 49/49 pages, but in TWO models (issue #4 clarification, 2026-10-10): pages 1–2 (A–B, 21 owners) from the first build live in the ATLAS_OWNERS owners model via PT cross-checks; pages 3–49 (101 rows) in PUA_CONTINUATION (issue #17: pp. 3–10, 18 entries; P3: p. 11, 4 entries; P4: pp. 12–34, 47 entries — surnames H–P including Kirche H. Veith = St. Vitus' church; P5-b: pp. 35–49, 32 entries, rows 69–100 including the group entries »Gemeinde Malfz Brandhof…« and »Uebersprungene Parzellen-Numern«). structuredEntries 101 = PUA_CONTINUATION ONLY (pp. 3–49); the A–B pages are not in PUA_CONTINUATION. KEY P4 FINDING: PUA and PT evidently use DIFFERENT house numbering [~] (PUA house 6 = Höflehner, PT house 6 = Tilel Miho); PUA keeps nos. in the 41–60 range where PT has none. Everything stays REVIEW (machine reading is not evidentiary); raw outputs in research/p3/pua-raw/ (38 pages) + research/issue17/PUA-more.json.",
  },
  {
    code: "PZ",
    unitSi: "Katastrski cenilni elaborat",
    unitEn: "Cadastral valuation elaborate",
    pages: 71,
    pagesTranscribed: 12,
    pagesReadList: [1, 2, 3, 20, 30, 40, 50, 60, 68, 69, 70, 71],
    structuredEntries: 10,
    status: "REVIEW",
    noteSi: "71 strani ocen in razredov. Vzorčeno 12 strani (issue #4, 2026-10-10, dokaz: research/issue17/PZ-profile.json + PZ-valuation.json pagesSampled=[20,30,40,50,60]): 1–3 (naslov, §§ topografija/meje/prebivalstvo), 20/30/40/50/60 (cenilni razredi kultur, nizka gotovost — 3 VLM branja se razhajajo), 68–71 (zaključni protokoli: Vorlage, Geprüft, Nachtrag hus Zins, »Gemacht den 28ten Juli 1825«). POPRAVEK issue #4: prejšnji števec 10 se ni ujemal z lastno opombo (12 strani) — dokazano stanje je 12. Vsebina: topografija §1 (2294 joch 516 klafter [~]), prebivalstvo §3 (441 prebivalcev — 222 m/219 ž; 72 hiš [~]; 102 družin [~]), cenilna veriga Roh-Ertrag → Cultur-Aufwand → Rein-Ertrag (Bau-Area: 16 fl 50½ kr → 7 fl 35 kr/joch, aritmetika potrjena). Tabele razredov v sredini (str. 4–67, razen vzorčenih) so NEPRESRANE — poln prepis 59 strani TO_COLLECT.",
    noteEn: "71 pages of valuations and classes. 12 pages sampled (issue #4, 2026-10-10, evidence: research/issue17/PZ-profile.json + PZ-valuation.json pagesSampled=[20,30,40,50,60]): 1–3 (title, §§ topography/boundaries/population), 20/30/40/50/60 (culture valuation classes, low confidence — 3 VLM readings disagree), 68–71 (closing protocols: Vorlage, Geprüft, Nachtrag hus Zins, »Gemacht den 28ten Juli 1825«). issue #4 CORRECTION: the previous count of 10 contradicted its own note (12 pages) — the evidenced state is 12. Content: topography §1 (2294 joch 516 klafter [~]), population §3 (441 inhabitants — 222 m/219 f; 72 houses [~]; 102 families [~]), the valuation chain Roh-Ertrag → Cultur-Aufwand → Rein-Ertrag (Bau-Area: 16 fl 50½ kr → 7 fl 35 kr/joch, arithmetic confirmed). The class tables in the middle (pp. 4–67, apart from the sampled ones) remain UNTRANSCRIBED — the full 59-page transcription TO_COLLECT.",
  },
  {
    code: "PT",
    unitSi: "Protokol stavbnih parcel",
    unitEn: "Protocol of building parcels",
    pages: 8,
    pagesTranscribed: 8,
    pagesReadList: [1, 2, 3, 4, 5, 6, 7, 8],
    structuredEntries: 84,
    status: "REVIEW",
    noteSi: "84 stavbnih vrstic (hišne št. 1–99 + prečrtana dvojnica 34) prebranih s pomočjo strojnega branja; vsi vnosi status REVIEW. Issue #17: 101 vrstica preverjena (81 POTRJENIH, 15 popravkov, 4 manjkajoče vrstice, str. 4 konča pri hiši 40). P3 PALEOGRAFSKA PREVERBA (2. krog, 2026-10-08): sveži izrezi + povišana ločljivost, prompti »črka-za-črko«; 15 popravkov in 4 dodatne vrstice APLICIRANE v register (houses.ts) pri 2-kratni konvergenci branj; renumeracija str. 4 (36–41 → 35–40) 4× potrjena; statusi ostajajo REVIEW (2. krog je še vedno strojno branje; dokončna potrditev = človeška paleografija).",
    noteEn: "84 building rows (house nos. 1–99 + the struck duplicate 34) read with machine assistance; all entries carry REVIEW status. Issue #17: 101 rows checked (81 CONFIRMED, 15 corrections, 4 missing rows, p. 4 ends at house 40). P3 PALAEOGRAPHIC VERIFICATION (2nd pass, 2026-10-08): fresh crops + upscaled resolution, letter-by-letter prompts; 15 corrections and 4 additional rows APPLIED to the register (houses.ts) on 2-pass convergence; the p. 4 renumbering (36–41 → 35–40) confirmed 4×; statuses stay REVIEW (the 2nd pass is still machine reading; final confirmation = human palaeography).",
  },
  {
    code: "PG",
    unitSi: "Indikacijska skica",
    unitEn: "Indication sketch",
    pages: 1,
    pagesTranscribed: 1,
    pagesReadList: [1],
    structuredEntries: 1,
    status: "REVIEW",
    noteSi: "Indikationsskizze prebrana (issue #17, VLM 2026-10-08): ročno risana skica z naslovom »Gemeinde Grüble« + veliko številko 83 (ujema se s signaturo N83), debel mejni mnogokotnik z rdeče oštevilčenimi točkami (~15–19), Kolpa modrikasta po vzhodnem robu z napisom »Königreich Croatien«, sosedi Weidendorf/Mallertschitsch/Pridbor[~]. Hišnih simbolov NI vidnih (negativen rezultat). Lestvica [~1 W. Zoll = 1000 klafter].",
    noteEn: "Indication sketch read (issue #17, VLM 2026-10-08): hand-drawn sketch titled »Gemeinde Grüble« + large number 83 (matches signature N83), thick boundary polygon with red-numbered points (~15–19), the Kolpa blue along the east edge inscribed »Königreich Croatien«, neighbours Weidendorf/Mallertschitsch/Pridbor[~]. NO house symbols visible (negative result). Scale [~1 W. inch = 1000 klafter].",
  },
  {
    code: "PV",
    unitSi: "Izkaz rabe zemljišč",
    unitEn: "Statement of land use",
    pages: 1,
    pagesTranscribed: 1,
    pagesReadList: [1],
    structuredEntries: 10,
    status: "REVIEW",
    noteSi: "Izkaz rabe tal PREBRAN v celoti (issue #17, VLM 2026-10-08, vsaka izpolnjena celica potrjena ≥2 klicoma): tiskan obrazec »AUSWEIS über die Benützungsart des Bodens«, Provinz Illyrien, [~Kreis Neustadtl], datum »den 10 Jenner 1825«. 10 izpolnjenih vrstic kultur (20 vrstic obrazca) + 2 vsoti: ganze Area 1148 j 539 kl + strnjena 73 j 1024 kl = skupaj 1221 [~1225] j 1513 [~1563] kl ≈ 703 ha (≈ sodobna k.o. Griblje 7,0 km²). Presenetljivo: vrstica Wälder (gozd) je PRAZNA — dominira 636 joch pašnikov. Aritmetika ±1 joch (dokumentirana odstopanja).",
    noteEn: "Statement of land use READ in full (issue #17, VLM 2026-10-08, every filled cell confirmed by ≥2 calls): printed form »AUSWEIS über die Benützungsart des Bodens«, Provinz Illyrien, [~Kreis Neustadtl], dated »den 10 Jenner 1825«. 10 filled culture rows (20 form rows) + 2 totals: ganze Area 1148 j 539 kl + compact 73 j 1024 kl = grand 1221 [~1225] j 1513 [~1563] kl ≈ 703 ha (≈ the modern k.o. Griblje 7.0 km²). Striking: the Wälder (forest) row is EMPTY — 636 joch of pasture dominate. Arithmetic ±1 joch (documented deviations).",
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
    id: "geo-ezkn",
    nameSi: "eZKN — georeferenčni zgodovinski kataster (GisKD/GeoHub)",
    nameEn: "eZKN — georeferenced historical cadastre (GisKD/GeoHub)",
    provider: "GURS + Arhiv RS",
    kindSi: "spletni georeferenčni pregledovalnik ZKN + indikacijski katastrski zemljevidi",
    kindEn: "online georeferenced ZKN viewer + indication cadastral maps",
    url: "https://geohub.gov.si/ghapp/ezkn/",
    coversGriblje: true,
    coversNoteSi:
      "POTRJENO 2026-10-08 (issue #17): javni pregledovalnik ZKN GURS + indikacijski zemljevidi franciscejskega/reambulančnega katastra ARS (JPG). Pod imenom »GeoZgodovina« portal ne obstaja — pravi vir je eZKN. Uradna javna georeferenca katastrskih map; ključ za prostorsko prekrivanje 1825↔danes.",
    coversNoteEn:
      "CONFIRMED 2026-10-08 (issue #17): a public GURS ZKN viewer + ARS indication maps of the Franciscean/reambulation cadastre (JPG). No portal named »GeoZgodovina« exists — the real source is eZKN. The official public georeference of cadastral maps; key for the 1825↔today spatial overlay.",
    licence: "javni dostop (GeoHub GURS)",
    status: "VERIFIED",
    lastVerified: "2026-10-08",
  },
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
    coversNoteSi:
      "Slovenija je v celoti lasersko posneta v novem ciklu (pregledovalnik 3D podatkov). Issue #17 (2026-10-08): cikel 2023–2025 — nadomesti LiDAR 2014–15, ki bloka b_16 (Griblje) ni zajemal; kvadrantni prenosi GKOT/DMR/DMP (.laz), nDMP/PAS (.tif); uradni globoki link za Griblje: clss.si/?center=522667||47571&srid=3794.",
    coversNoteEn:
      "Slovenia is fully laser-scanned in the new cycle (3D data viewer). Issue #17 (2026-10-08): cycle 2023–2025 — replaces the 2014–15 LiDAR which missed block b_16 (Griblje); quadrant downloads GKOT/DMR/DMP (.laz), nDMP/PAS (.tif); official deep link for Griblje: clss.si/?center=522667||47571&srid=3794.",
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
    "Primarni digitalni predmet (inventarna številka, datum, avtor, slika, pravni status) ne obstaja v zbirki in NI potrjen. Issue #17 (2026-10-08): za Griblje ni nobenega Gasparijevega predmeta; dokumentiran kandidat ZA BELO KRAJINO je slika »Belokranjska ohcet« (1924, olje/platno, hrani jo SEM — viri RTV SLO, Dnevnik, Družina, razstava SEM 2024, radio-odeon/preloka.si) — javne inventarne številke NI, v SEM digitalnih zbirkah ni. Status ostaja TO_COLLECT: iskanje primarnega predmeta/inventarne št. (SEM, Narodni muzej).",
  noteEn:
    "No primary digital object (inventory number, date, author, image, legal status) exists in the collection and none is confirmed. Issue #17 (2026-10-08): no Gaspari item for Griblje exists; the documented candidate FOR BELA KRAJINA is the painting »Belokranjska ohcet« (1924, oil/canvas, held by SEM — sources RTV SLO, Dnevnik, Družina, the 2024 SEM exhibition, radio-odeon/preloka.si) — no public inventory number, not in the SEM digital collections. Status remains TO_COLLECT: search for the primary object/inventory no. (SEM, National Museum).",
  lastVerified: "2026-10-08",
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
  /** javni zapis SEM (issue #17, verifikacija 2026-10-08) */
  publicRecord: {
    status: ResearchStatus;
    url: string;
    verifiedAt: string;
    findingSi: string;
    findingEn: string;
  };
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
  publicRecord: {
    status: "VERIFIED",
    url: "https://www.etno-muzej.si/sl/digitalne-zbirke/zbirka-starih-fotografij/f0000212",
    verifiedAt: "2026-10-08",
    findingSi:
      "Javni zapis SEM POTRJEN (HTTP 200): 'Enonadstropna hiša na pero, rojstna hiša dr. Nika Županiča', Zbirka starih fotografij, lokacija Griblje; slika javna (/files/oc/f0000212.jpg, 264 KB). Polji fotograf in datum sta v javnem zapisu PRAZNA — za metapodatke je treba pisati SEM (miha.spicek@etno-muzej.si). Domena evd.si (domnevna baza SEM) je naprodaj — NI baza SEM; pravi vir je etno-muzej.si.",
    findingEn:
      "The public SEM record CONFIRMED (HTTP 200): 'Enonadstropna hiša na pero, rojstna hiša dr. Nika Županiča', the Old Photographs Collection, location Griblje; image public (/files/oc/f0000212.jpg, 264 KB). The photographer and date fields are EMPTY in the public record — SEM must be contacted for metadata (miha.spicek@etno-muzej.si). The evd.si domain (assumed SEM database) is for sale — NOT a SEM database; the real source is etno-muzej.si.",
  },
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
    { stepSi: "SEM, digitalne zbirke — zapis F0000212", stepEn: "SEM, digital collections — record F0000212", status: "VERIFIED" },
    { stepSi: "javni zapis SEM (etno-muzej.si, URL potrjen 2026-10-08) + javna slika", stepEn: "public SEM record (etno-muzej.si, URL confirmed 2026-10-08) + public image", status: "VERIFIED" },
    { stepSi: "opis vsebine (hiša na pero, rojstna hiša Županiča)", stepEn: "content description (gallery house, Županič birth house)", status: "DOCUMENTED" },
    { stepSi: "fotograf / datum snemanja (polji v javnem zapisu prazni — pisati SEM)", stepEn: "photographer / shooting date (fields empty in the public record — write to SEM)", status: "TO_COLLECT" },
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
  periodOriginals: { title: string; sourceUrl: string; licence: string; verified?: string }[];
  bounds: { north: number; south: number; west: number; east: number };
  georeferencePath: {
    status: ResearchStatus;
    methodSi: string;
    methodEn: string;
  };
  /** Izvedena strojna georeferenca izvirnika 1812 (OCR → LSQ preslikava) — issue #17, P6 */
  georef?: {
    executedAt: string;
    method: string;
    controlPoints: number;
    residualsKm: { median: number; max: number };
    scaleMPerPx: { x: number; y: number };
    gribljePx: { x: number; y: number };
    uncertaintyKm: number;
    artifacts: string[];
    /** Koroboracija na drugem (neodvisnem) skenu istega lista — P7, 2026-10-08 */
    corroboration?: {
      secondScan: string;
      executedAt: string;
      method: string;
      registration: { inliers: number; matches: number; rmsPx: number; scaleRatio: number };
      controlPoints: number;
      fullWords: number;
      residualsKm: { median: number; medianFullWords: number; max: number };
      scaleMPerPx: { x: number; y: number };
      gribljePathA: { x: number; y: number };
      gribljePathB: { x: number; y: number };
      agreementPx: number;
      agreementKm: number;
      artifacts: string[];
    };
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
      title: "Provinces Illyriennes Servie et Bosnie 1812 (izvirnik 1812, Giraldon; javna last)",
      sourceUrl: "https://commons.wikimedia.org/wiki/File:Provinces_Illyriennes_Servie_et_Bosnie_1812.jpg",
      licence: "javna last (Public Domain)",
      verified: "POTRJENO 2026-10-08 (issue #17): datoteka obstaja, 8297 × 6080 px, vir = dlib ref. 6EZTJ9C0",
    },
    {
      title: "Provinces Illyriennes, Servie et Bosnie (Lapie/Malte-Brun/Chamouin/Giraldon; drugi sken istega lista, Internet Archive)",
      sourceUrl: "https://commons.wikimedia.org/wiki/File:Provinces_Illyriennes,_Servie_et_Bosnie._(IA_dr_provinces-illyriennes-servie-et-bosnie-2631039).jpg",
      licence: "javna last (Public Domain)",
      verified: "POTRJENO 2026-10-08 (P6, Commons API): 7636 × 5936 px, umetniki Malte-Brun/Lapie/Chamouin/Giraldon — NEODVISEN drugi sken istega graverja kot glavni vir; koroboracija izvirnika",
    },
    {
      title: "Zemljevid Ilirskih provinc iz leta 1812 (Gašperič, Orožen Adamič, Šumrada; ZRC SAZU 2012)",
      sourceUrl: "https://dlib.si/URN:NBN:SI:doc-F4NO0ZFV",
      licence: "ZRC SAZU (faksimile francoskega zemljevida 1812)",
      verified: "POTRJENO 2026-10-08 (issue #17) prek COBISS/WorldCat/giam.zrc-sazu.si (dlib s sandboxa timeout, URN obstaja)",
    },
  ],
  bounds: { north: 48.1, south: 41.4, west: 11.1, east: 24.4 },
  georeferencePath: {
    status: "REVIEW",
    methodSi:
      "Izvedeno 2026-10-08 (P6, brez AI-branja vsebine): obdobjeni izvirnik Giraldon 1812 (Commons 8297×6080 px, javna last) prenešen → OCR mestnih oznak (tesseract, 3–6× povečave izrezov) → 15 kontrolnih točk (Pest, Leoben, Ancona, Vidin, Semlin, Zvornik, Priština, Beograd, Sarajevo, Ragusa, Agram, Fiume, Laibach, Trst, Banya Luka) → najmanjša kvadratna preslikava px→WGS84 (afina IN kvadratna 2. reda; za Griblje se ujemata na ±2 px). Merilo ≈ 126×124 m/px (razmerje 1,024 — lista ni raztegnjena); residuali: mediana ≈ 10 km, max ≈ 25 km (Laibach — oznaka vzhodno od mesta). Griblje (45,568 N 15,290 E) → px (2499, 2286) ± ~10 km; dokazni izrez z označeno lego v zbirki (MVG-092). KOROBORACIJA P7 (2026-10-08): drugi, knjižni sken istega lista (Internet Archive 7636×5936) — ORB+RANSAC registracija obeh skenov (4030 inlierjev, RMS 3,9 px) + neodvisen 12-točkovni OCR geo-model drugega skena → obe poti za lego Gribelj se ujemata na 37 px = 5,6 km (znotraj ± 10 km negotovosti) — rezultat NI artefakt skeniranja. OMEJITVE [~]: kontrolne točke so centri OCR-anih NAPISOV, ne mestnih pik; mrežne stopinje niso bile strojno berljive (Parisov meridian nepotrjen); končna potrditev zahteva človeško paleografijo ali QGIS georeferenco. Polni strojno berljivi rezultat: research/georef-1812/georef-1812.json + reproducibilen skript fit-georef.py (1. sken) in fit-georef-second.py (2. sken, koroboracija).",
    methodEn:
      "Executed 2026-10-08 (P6, no AI content reading): the period original Giraldon 1812 (Commons 8297×6080 px, public domain) downloaded → OCR of city labels (tesseract, 3–6× upscaled crops) → 15 control points (Pest, Leoben, Ancona, Vidin, Semlin, Zvornik, Pristina, Belgrade, Sarajevo, Ragusa, Agram, Fiume, Laibach, Trieste, Banya Luka) → least-squares px→WGS84 mapping (affine AND 2nd-order quadratic; they agree on Griblje to ±2 px). Scale ≈ 126×124 m/px (ratio 1.024 — the sheet is not stretched); residuals: median ≈ 10 km, max ≈ 25 km (Laibach — label east of the city). Griblje (45.568 N 15.290 E) → px (2499, 2286) ± ~10 km; evidence crop with the marked position in the collection (MVG-092). CORROBORATION P7 (2026-10-08): a second, book scan of the same sheet (Internet Archive 7636×5936) — ORB+RANSAC registration of both scans (4030 inliers, RMS 3.9 px) + an independent 12-point OCR geo-model of the second scan → both paths for Griblje's position agree to 37 px = 5.6 km (within the ± 10 km uncertainty) — the result is NOT a scanning artifact. LIMITS [~]: control points are centres of OCR-read LABELS, not city dots; graticule degrees were not machine-readable (Paris meridian unconfirmed); final confirmation needs human paleography or QGIS georeferencing. Full machine-readable result: research/georef-1812/georef-1812.json + reproducible script fit-georef.py (scan 1) and fit-georef-second.py (scan 2, corroboration).",
  },
  georef: {
    executedAt: "2026-10-08",
    method: "OCR (tesseract eng) mestnih oznak → LSQ afina + kvadratna preslikava px→WGS84; primerjava modelov",
    controlPoints: 15,
    residualsKm: { median: 10.1, max: 25.0 },
    scaleMPerPx: { x: 126, y: 124 },
    gribljePx: { x: 2499, y: 2286 },
    uncertaintyKm: 10,
    artifacts: [
      "research/georef-1812/georef-1812.json",
      "research/georef-1812/fit-georef.py",
      "research/georef-1812/orig-1812.jpg",
      "research/georef-1812/griblje-okolis-1812-oznacen.jpg",
      "public/images/authentic/griblje-okolis-1812-900.jpg",
      "public/images/authentic/griblje-okolis-1812-600.jpg",
    ],
    corroboration: {
      secondScan: "Provinces Illyriennes, Servie et Bosnie (Lapie/Malte-Brun/Chamouin/Giraldon; Internet Archive, 7636×5936 px, javna last) — drugi, knjižni sken istega lista",
      executedAt: "2026-10-08",
      method: "ORB+RANSAC slikovna registracija obeh skenov → OCR 12 oznak 2. skena → neodvisen LSQ geo-model; primerjava poti A (model 1. skena + registracija) in poti B (model 2. skena) za lego Gribelj",
      registration: { inliers: 4030, matches: 4670, rmsPx: 3.9, scaleRatio: 1.005 },
      controlPoints: 12,
      fullWords: 5,
      residualsKm: { median: 9.7, medianFullWords: 6.2, max: 22.2 },
      scaleMPerPx: { x: 151, y: 152 },
      gribljePathA: { x: 2513, y: 2003 },
      gribljePathB: { x: 2489, y: 2032 },
      agreementPx: 37,
      agreementKm: 5.6,
      artifacts: [
        "research/georef-1812/georef-1812-second.json",
        "research/georef-1812/fit-georef-second.py",
        "research/georef-1812/orig-1812-second.jpg",
        "research/georef-1812/regis-orb.json",
        "research/georef-1812/scan2-labels.json",
      ],
    },
  },
  lastVerified: "2026-10-08",
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

// ——— 9. RESEARCH GAP CLOSURE v2 (issue #17, 2026-10-08) ———————————————————
//
// ISSUE #17: zapolnjevanje raziskovalnih vrzeli Kurrent 1812–1853, hiše/parcele,
// primarni viri in ustna zgodovina. Vsa branja: VLM (glm-5v-turbo) na skenih
// N083 (PDF v download/atlas-1825/n83/, javno dostopni prek VAČ — OPSI zbirka
// "Digitalizirano arhivsko gradivo starih katastrov"). Surovi izpisi VLM klicev
// se hranijo v research/issue17/*.json (provenienca). Strojni prepisi so po
// definiciji REVIEW; negotova branja so označena [~], neberljiva [?].

export interface LandUseRow1825 {
  /** kultura, kot zapisano v viru (nemško) */
  cultureAsWritten: string;
  /** slovenski prevod */
  cultureSi: string;
  joch: number | null;
  klafter: number | null;
  /** [~] = negotovo branje števk */
  confidence: "clear" | "~" | "empty";
}

/** PV — Izkaz rabe tal 1825 (N083PV, 10. 1. 1825) — PREBRAN v celoti. */
export const PV_LAND_USE_1825: {
  source: string;
  titleAsWritten: string;
  dateAsWritten: string;
  status: ResearchStatus;
  rows: LandUseRow1825[];
  totals: {
    ersteSumme: { label: string; joch: number; klafter: number; confidence: string };
    zweiteSumme: { label: string; joch: number; klafter: number; confidence: string };
    grandTotal: { label: string; joch: number; klafter: number; confidence: string; hectares: number };
  };
  arithmeticCheckSi: string;
  anomalySi: string;
  anomalyEn: string;
} = {
  source: "N083PV (Arhiv RS, SI AS 176, k.o. Griblje) — research/issue17/PV.json",
  titleAsWritten: "AUSWEIS über die Benützungsart des Bodens für die Gemeinde Grüble (Provinz Illyrien, [~Kreis Neustadtl])",
  dateAsWritten: "den 10 Jenner 1825",
  status: "REVIEW",
  rows: [
    { cultureAsWritten: "Gemüse Gärten", cultureSi: "zelenjavnih vrtov", joch: 2, klafter: 123, confidence: "clear" },
    { cultureAsWritten: "Obst Gärten", cultureSi: "sadovnjakov", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Zier Gärten", cultureSi: "okrasnih vrtov", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Wein Gärten", cultureSi: "vinogradov", joch: 7, klafter: 665, confidence: "clear" },
    { cultureAsWritten: "Hopfen Gärten", cultureSi: "hmeljišč", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Wiesen", cultureSi: "travnikov", joch: 76, klafter: 1480, confidence: "clear" },
    { cultureAsWritten: "Wiesen mit Obstbäumen", cultureSi: "travnikov s sadjem", joch: 12, klafter: 328, confidence: "clear" },
    { cultureAsWritten: "Weiden", cultureSi: "pašnikov", joch: 636, klafter: 263, confidence: "clear" },
    { cultureAsWritten: "Sümpfe", cultureSi: "barja/močvirij", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Sümpfe mit Rohrwuchs", cultureSi: "barja s trstjem", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Aecker", cultureSi: "njiv", joch: 413, klafter: 870, confidence: "clear" },
    { cultureAsWritten: "Aecker mit Obstbäume", cultureSi: "njiv s sadjem", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Aecker mit Oelbäumen", cultureSi: "njiv z oljkami", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Aecker mit Weinreben", cultureSi: "njiv z vinsko trto", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Aecker mit Bäume und Weinreben", cultureSi: "njiv z drevjem in trto", joch: null, klafter: null, confidence: "empty" },
    { cultureAsWritten: "Oedungen", cultureSi: "neobdelanega", joch: 1, klafter: 476, confidence: "~" },
    { cultureAsWritten: "Flüsse oder Bäche", cultureSi: "rek/potokov", joch: 21, klafter: 142, confidence: "clear" },
    { cultureAsWritten: "Weg Parzellen", cultureSi: "poti", joch: 46, klafter: 1127, confidence: "clear" },
    { cultureAsWritten: "Bau Parzellen", cultureSi: "stavbnih parcel", joch: 4, klafter: 889, confidence: "clear" },
    { cultureAsWritten: "Wälder", cultureSi: "gozdov", joch: null, klafter: null, confidence: "empty" },
  ],
  totals: {
    ersteSumme: { label: "Ganze Area der Gemeinde (vsota obdelanega)", joch: 1148, klafter: 539, confidence: "clear (vrstice se seštejejo v 1148/529±)" },
    zweiteSumme: { label: "vsota strnjenih/voda/poti/stavbe", joch: 73, klafter: 1024, confidence: "clear (vrstice ~72/1036)" },
    grandTotal: { label: "Area der ganzen Gemeinde", joch: 1221, klafter: 1513, confidence: "clear (~1225/1563 v enem klicu)", hectares: 703 },
  },
  arithmeticCheckSi:
    "Vsota vrstic: 1148 j 529 kl (prva skupina, razlika 10 kv. kl) + ~72 j 1036 kl (druga, ~1 joch) → skupaj 1221 j 1565 kl [~1513–1563]. Odmiki 1 joch / 10–50 kv. kl — bodisi posamično napačno prebrana števka, bodisi pisarniška napaka leta 1825; vse odstopanje je dokumentirano v PV.json. Neodvisna kontrola: 1028 × 1884 kl (PR mere) = 1.936.752 kv. kl = 1210,5 jocha — odstopanje <1 % od skupne vsote 1221 j → obe številki sta skoraj zagotovo prebrani pravilno.",
  anomalySi:
    "ODK RITO: vrstica Wälder (gozd) je PRAZNA — izkaz rabe 1825 za k.o. Griblje ne registrira nobenega gozda; prevladujejo pašniki (636 j). NASPROTJE s katastrskim listom A02, ki na južnem robu kaže gozdní kompleks (glej landuse.ts raba-gozd). Možni razlogi (hipoteze, ne dejstva): (a) gozd na A02 pripada sosednji k.o. (meja lista ≠ meja občine), (b) gozd je bil odvezen/zajet v drugi vpis, (c) vrstica je ostala nepopolnjena po ukazu. Odprto vprašanje za paleografski pregled originala.",
  anomalyEn:
    "FINDING: the Wälder (forest) row is EMPTY — the 1825 land-use statement registers no forest for k.o. Griblje; pasture dominates (636 joch). CONTRAST with cadastral sheet A02 which shows a forest complex on its southern edge (see landuse.ts raba-gozd). Possible reasons (hypotheses, not facts): (a) the A02 forest belongs to the neighbouring k.o. (sheet edge ≠ municipality boundary), (b) the forest was carried in another entry, (c) the row was left unfilled by instruction. Open question for a palaeographic review of the original.",
};

/** PR — opis meje 1825 (N083PR, 8. 4. 1825) — prebrano, točke 1–10 jasno. */
export const PR_BOUNDARY_1825: {
  source: string;
  titleAsWritten: string;
  dateAsWritten: string;
  status: ResearchStatus;
  dimensions: { eastWestKlafter: number; northSouthKlafter: number; confidence: string };
  boundaryPoints: { no: number; nameAsWritten: string; lengthKlafter?: string; confidence: string }[];
  neighbours: { nameAsWritten: string; confidence: string }[];
  crossCheckSi: string;
} = {
  source: "N083PR (Arhiv RS, SI AS 176, k.o. Griblje) — research/issue17/PR.json",
  titleAsWritten: "Grenz-Beschreibung der Gemeinde „ GRÜBLE“ (Prod N° 218)",
  dateAsWritten: "am 8ten April 1825",
  status: "REVIEW",
  dimensions: { eastWestKlafter: 1028, northSouthKlafter: 1884, confidence: "1028 stabilno (5/5 klicev); 1884 [~1834] (3/5)" },
  boundaryPoints: [
    { no: 1, nameAsWritten: "[~Acker des Wölflaner …] — začetna točka", lengthKlafter: "60,6", confidence: "~" },
    { no: 2, nameAsWritten: "Hohenstie/Holensthe Busch", lengthKlafter: "838", confidence: "~" },
    { no: 3, nameAsWritten: "Liebstöhe/Liebstöckel", confidence: "~" },
    { no: 4, nameAsWritten: "Halb Dell", confidence: "~" },
    { no: 5, nameAsWritten: "Heusch (ob vodi)", confidence: "~" },
    { no: 6, nameAsWritten: "Krofing/Poleschitzi", confidence: "~" },
    { no: 7, nameAsWritten: "Rudini Pöltsch/Gastei Scheibe", lengthKlafter: "823", confidence: "~" },
    { no: 8, nameAsWritten: "[~Dorn …] Welthe Oel", lengthKlafter: "240", confidence: "~" },
    { no: 9, nameAsWritten: "Na öhering", confidence: "~" },
    { no: 10, nameAsWritten: "nadaljevanje s slovenskimi mikrotoponimi (Losa, Schimotschi Drani, Vetalachki, Skaize Hardanove, Na Dragi, Hali Grami, Studeni Potok …; dolžine 326/370/274/170/87/185/86/46,8/185/41 kl)", confidence: "~ štetje točk negotovo (10–20; PG skica nakazuje 15–19)" },
  ],
  neighbours: [
    { nameAsWritten: "Königreich Croaten (čez Kolpo, jug/vzhod)", confidence: "stabilno (3 klici + PG skica)" },
    { nameAsWritten: "Weidendorf (Vinji Vrh?)", confidence: "stabilno (PR + PG)" },
    { nameAsWritten: "Mallertschitsch (Maloš? — iz PG skice)", confidence: "~" },
    { nameAsWritten: "Pridbor[~] (Pridvorje?) — iz PG skice", confidence: "~" },
    { nameAsWritten: "Krasincz/Kremsig [~], Sribitsche/Stibischoche [~], Pervang/Travnik [~], Alloschütz/Adlerschütz [~]", confidence: "branja med klici nestabilna" },
  ],
  crossCheckSi:
    "1028 × 1884 kv. klafterjev = 1.936.752 kv. kl = 1210,5 jocha → odstopanje <1 % od PV skupne površine 1221 j → mere sta medsebojno potrjeni. Datum zaključka meje: 8. 4. 1825; izkaz rabe: 10. 1. 1825; cenilni elaborat: 28. 7. 1825 — dokumentirana kronologija nastanka N83 za Griblje.",
};

/** PS — rekapitulacija 1826 (N083PS, str. 143, rdeči tuš). */
export const PS_RECAP_1826: {
  source: string;
  status: ResearchStatus;
  summaBauplätze: number;
  summaGrundparzellen: number;
  zusammen: number;
  columns: string[];
  mostUsefulSi: string;
  mostUsefulEn: string;
  sampleRowCount: number;
} = {
  source: "N083PS str. 140–143 (Arhiv RS, SI AS 176, k.o. Griblje) — research/issue17/PS-structure.json; P36: str. 5–139 prebrane strojno (research/issue17/ps-raw/, PS-full.json)",
  status: "REVIEW",
  summaBauplätze: 102,
  summaGrundparzellen: 2505,
  zusammen: 2607,
  columns: [
    "Nro. des Blattes (katastralski list)",
    "Nro. der Parzelle",
    "Dominical/Rustical",
    "Haus Nro.",
    "Lastnik (Vor und Zuname)",
    "Stand",
    "Wohnort",
    "Kultur Gattung (raba)",
    "Joch / Quadrat-Klafter (površina)",
    "Classe (razred)",
    "Reiner jährl. Ertrag fl/kr (donos)",
    "Capital Werth fl/kr",
    "Anmerkung",
  ],
  mostUsefulSi:
    "Veriga hiša→parcela→lastnik je v VSAKI vrstici glavnega registra (stolpci Haus Nro. + lastnik + parcela + raba + površina), a vrstice NISO grupirane po lastnikih → vstop prek stolpca Haus Nro. P36 (2026-10-11): strojni prepis vseh 135 strani (5–139, 2743 vrstic, dvoprehodno na 78 straneh) IZVEDEN; P38 (2026-10-12): sekcije spravljene (GRUND 1889/2505, NADALJEVANJE 95, WALDUNG 81, Blatt X 60), P39 (2026-10-12): razdvojitev v model parcela×raba (2134 vnosov, 2632 parov, /api/atlas/ps-landuse) — preostane: 3. prehod dvoumnih strani, uskladitev s kontrolno vsoto 102 + 2505 = 2607 (šteje kategorije — glavni niz sega čez 2840), primerjava z rekapitulacijo (~str. 140–143) in nato ciljano po hišah prek Haus Nro.",
  mostUsefulEn:
    "The house→parcel→owner chain sits in EVERY row of the main register (Haus Nro. + owner + parcel + culture + area columns), but rows are NOT grouped by owner → enter via the Haus Nro. column. P36 (2026-10-11): the machine transcription of all 135 pages (5–139, 2,743 rows, two passes on 78 pages) is DONE; P38 (2026-10-12): sections reconciled (GRUND 1,889/2,505, CONTINUATION 95, WALDUNG 81, Blatt X 60); P39 (2026-10-12): split into the parcel×culture model (2,134 entries, 2,632 pairs, /api/atlas/ps-landuse) — remaining: a 3rd pass over ambiguous pages, matching against the checksum 102 + 2505 = 2,607 (it counts categories — the main series runs past 2840), comparison with the recapitulation (~pp. 140–143), then targeting by house via Haus Nro.",
  sampleRowCount: 2743,
};

/**
 * P38 (issue #10) — N083PS: deterministična sprava strojno prebranega protokola.
 * Izračunano s committed skriptom scripts/p38_ps_reconcile.py iz committed dokazov
 * research/issue17/ps-raw/ (213 VLM branj); polno poročilo: research/issue17/
 * ps-reconciliation.json. Vsi statusi ostajajo REVIEW (strojno branje ni dokazni vir).
 */
export const PS_RECONCILIATION_P38: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  readingRule: "pass1" | "pass2wins" | "union";
  sections: Record<
    string,
    { rows: number; distinctParcels: number; pages: number[] | null; range: [number, number] | null }
  >;
  splitting: {
    rowsBefore: number;
    rowsAfter: number;
    pass1RowsTotal: number;
    parcelCulturePairs: number;
    parcelsWithMultipleCultures: number;
    extraRowsFromMultiCulture: number;
  };
  coverage: {
    grundDistinct: number;
    grundMissing: number;
    grundCoveragePct: number;
    grundMissingRanges: string;
    nad2506Distinct: number;
    nad2506Range: [number, number] | null;
    waldungDistinct: number;
    waldungRange: [number, number] | null;
    blattXDistinct: number;
    blattXRange: [number, number] | null;
  };
  ocrLeadingDigitCandidates: { count: number; note: string };
  p36Baseline: { reproducedUnderPass2wins: boolean; note: string };
  sensitivity: Record<
    "pass1" | "pass2wins" | "union",
    { grundDistinct: number; grundMissing: number; nad2506Distinct: number; waldungDistinct: number; ocrCandidates: number }
  >;
  verdictSi: string;
  verdictEn: string;
  next: string[];
  negativeResults: string[];
} = {
  series: "PS",
  source:
    "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — sprava nad committed dokazi research/issue17/ps-raw/ (213 VLM branj, P36); polno poročilo research/issue17/ps-reconciliation.json",
  status: "REVIEW",
  generatedBy: "scripts/p38_ps_reconcile.py",
  readingRule: "pass2wins",
  sections: {
    GRUND_1_2505: {
      rows: 2490,
      distinctParcels: 1889,
      pages: Array.from({ length: 123 }, (_, i) => i + 5),
      range: [41, 2500],
    },
    NADALJEVANJE_2506: { rows: 100, distinctParcels: 95, pages: [128, 129, 130, 131, 132], range: [2507, 2840] },
    WALDUNG: { rows: 101, distinctParcels: 81, pages: [133, 134, 135, 136, 137], range: [2601, 2700] },
    BLATT_X: { rows: 60, distinctParcels: 60, pages: [138, 139], range: [1, 100] },
    NEBEREŽNA: { rows: 9, distinctParcels: 0, pages: null, range: null },
  },
  splitting: {
    rowsBefore: 2760,
    rowsAfter: 2127,
    pass1RowsTotal: 2743,
    parcelCulturePairs: 2118,
    parcelsWithMultipleCultures: 430,
    extraRowsFromMultiCulture: 633,
  },
  coverage: {
    grundDistinct: 1889,
    grundMissing: 616,
    grundCoveragePct: 75.4,
    grundMissingRanges:
      "1–40, 421–440, 561–563, 781–800, 1065, 1067, 1071–1072, 1075, 1181–1200, 1222–1233, 1301–1326, 1347–1440, 1461–1480, 1501–1600, 1621–1643, 1701–1800, 1841–1880, 1904, 1906, 2000, 2237, 2239–2240, 2281–2290, 2311–2340, 2361–2382, 2441–2460, 2501–2505",
    nad2506Distinct: 95,
    nad2506Range: [2507, 2840],
    waldungDistinct: 81,
    waldungRange: [2601, 2700],
    blattXDistinct: 60,
    blattXRange: [1, 100],
  },
  ocrLeadingDigitCandidates: {
    count: 0,
    note:
      "konzervativno pravilo (parcela < 100 zunaj Blatt X na strani, kjer so vse ostale parcele ≥ 100, ≥ 3 drugih) ni označilo NIČNEGA kandidata v nobeni od obeh neodvisnih bralnih sej — primer 161→61 iz P36 se v committed podatkih ni ohranil kot preostanek ali ga prehod 2 že razrešil",
  },
  p36Baseline: {
    reproducedUnderPass2wins: true,
    note:
      "P36 štetja se pod pravilom pass2wins + izločitvijo Blatt X REPRODUCIRAJO natanko: grundSeen 1889 = distinct GRUND_1_2505; over2505 176 = NADALJEVANJE_2506 (95) + WALDUNG (81); grundMissing 616 = 2505 − 1889; bauplatzeSeen 60 = distinct BLATT_X — razrešeno poreklo: Blatt X (str. 138–139, lastno številčenje 1–100) nosi register stavbnih mest (cilj 102)",
  },
  sensitivity: {
    pass1: { grundDistinct: 1820, grundMissing: 685, nad2506Distinct: 100, waldungDistinct: 81, ocrCandidates: 0 },
    pass2wins: { grundDistinct: 1889, grundMissing: 616, nad2506Distinct: 95, waldungDistinct: 81, ocrCandidates: 0 },
    union: { grundDistinct: 2018, grundMissing: 487, nad2506Distinct: 116, waldungDistinct: 81, ocrCandidates: 0 },
  },
  verdictSi:
    "DELNO USKLAJENO: glavni niz 1–2505 pokrit 1889/2505 (75,4 %); preostalih 616 parcel = strojno neodčitane/okvarjene vrstice in vloge Blatt X še niso spravljene; kontrolna vsota (102 + 2505 = 2607 kategorij) zahteva 3. prehod dvoumnih strani in primerjavo z rekapitulacijo 140–143. Blatt X (60/102 stavbnih mest) je zdaj razpoznan kot Bauplätze register.",
  verdictEn:
    "PARTIALLY RECONCILED: the main 1–2505 series is 75.4% covered (1,889/2,505); the remaining 616 parcels stem from unread/damaged rows and the Blatt X role is not yet reconciled; the checksum (102 + 2,505 = 2,607 categories) requires a third pass over ambiguous pages and comparison with the 140–143 recapitulation. Blatt X (60/102 building plots) is now recognised as the Bauplätze register.",
  next: [
    "3. prehod ~15 dvoumnih strani (audit §17, npr. str. 84, 138)",
    "razdvojitev večkulturnih vrstic v spravni model (štetja pripravljena; 430 parcel z več rabami)",
    "primerjava posameznih parcel z rekapitulacijo str. 140–143 (P5-b)",
    "človeška paleografska potrditev vseh strojnih branj",
  ],
  negativeResults: [
    "OCR kandidati za izgubo vodilne števke: 0 v obeh sejah — konzervativno pravilo ni označilo ničesar; zamenjave števk 3↔1 in 8↔5 ostajajo nedokazljive deterministično (lažni pozitivi)",
    "parcela 680 (str. 5) očitno okvarjena (hišna št. namesto parcele), pravilo je ne ujame — ostaja REVIEW brez samodejnega popravka",
    "večkulturne vrstice (430 parcel, +633 vrstic) še NISO razdvojene v aplikacijski model — samo štetja",
    "stran 129 (2831–2850) dokazuje, da nadaljevalni niz sega čez 2840 — skladno s P36 ugotovitvijo, da 2607 šteje kategorije, ne maksimum",
  ],
};

/**
 * P39 (issue #10) — N083PS: razdvojitev večkulturnih vrstic V SPRAVNI MODEL
 * (parcela × raba) + deterministična klasifikacija rab (pravilnik v1, brez AI).
 * Izračunano s committed skriptom scripts/p39_ps_landuse.py iz committed dokazov
 * research/issue17/ps-raw/ (213 VLM branj, P36) s P38 pravili; POLNI model
 * (2125 parcel + 9 NEBEREŽNA): research/issue17/ps-landuse.json (kanonski dokaz)
 * in identično kopijo src/data/atlas/ps-landuse.json za runtime; strojno berljivo
 * prek /api/atlas/ps-landuse. Vsi statusi ostajajo REVIEW.
 *
 * IZBOLJŠAVE ŠTETJA NASPROTI P38 (nove ugotovitve, P38 konstante ostanejo):
 *  - P38 »parcelCulturePairs« 2118 = vnosi po parcelah Z vsaj eno rabo; pravih
 *    vnosov po parcelah je 2125 (7 sirot brez rabe, 70 vrstic), model 2134.
 *  - pravih različnih parov parcela×raba je 2632; 49 vrstic ponovi rabo
 *    znotraj svoje parcele (ohranjene kot rows > 1, ne spletene).
 */
export const PS_LANDUSE_P39: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  readingRule: "pass1" | "pass2wins" | "union";
  totals: {
    rowsBefore: number;
    parcelEntries: number;
    parcelEntriesWithCulture: number;
    parcelEntriesEmptyCulture: number;
    emptyCultureRows: number;
    cultureRows: number;
    duplicateCultureRows: number;
    parcelCulturePairs: number;
    parcelsWithMultipleCultures: number;
    nebereznaRows: number;
    modelEntries: number;
  };
  sections: Record<string, { parcelEntries: number }>;
  cultureClasses: {
    rulebookVersion: string;
    classifiedPairs: number;
    classifiedPct: number;
    primaryCounts: Record<string, number>;
    multiClassPairs: number;
    unclassified: { count: number; distinctRaw: number };
  };
  topCulturesRaw: { raw: string; count: number }[];
  orphanParcelKeys: string[];
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "PS",
  source:
    "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — model nad committed dokazi research/issue17/ps-raw/ (213 VLM branj, P36); polni izpis research/issue17/ps-landuse.json + src/data/atlas/ps-landuse.json",
  status: "REVIEW",
  generatedBy: "scripts/p39_ps_landuse.py",
  readingRule: "pass2wins",
  totals: {
    rowsBefore: 2760,
    parcelEntries: 2125,
    parcelEntriesWithCulture: 2118,
    parcelEntriesEmptyCulture: 7,
    emptyCultureRows: 70,
    cultureRows: 2681,
    duplicateCultureRows: 49,
    parcelCulturePairs: 2632,
    parcelsWithMultipleCultures: 430,
    nebereznaRows: 9,
    modelEntries: 2134,
  },
  sections: {
    GRUND_1_2505: { parcelEntries: 1889 },
    NADALJEVANJE_2506: { parcelEntries: 95 },
    WALDUNG: { parcelEntries: 81 },
    BLATT_X: { parcelEntries: 60 },
  },
  cultureClasses: {
    rulebookVersion: "v1",
    classifiedPairs: 1896,
    classifiedPct: 72.0,
    primaryCounts: {
      NJIVA: 1049,
      TRAVNIK: 487,
      GOZD: 134,
      PASTVISCE: 54,
      STAVBNO: 52,
      VRT: 51,
      ALM: 23,
      NEROD: 22,
      OBCINA: 15,
      VINOGRAD: 8,
      CESTA: 1,
    },
    multiClassPairs: 156,
    unclassified: { count: 736, distinctRaw: 230 },
  },
  topCulturesRaw: [
    { raw: "Acker", count: 880 },
    { raw: "Wiese", count: 249 },
    { raw: "Wald", count: 126 },
    { raw: "Wiesen", count: 46 },
    { raw: "Acker und Wiese", count: 45 },
    { raw: "Ackerland", count: 39 },
    { raw: "Acker und Wiesen", count: 39 },
    { raw: "Alm", count: 25 },
    { raw: "Wiese und Acker", count: 20 },
    { raw: "Schüttmühle", count: 20 },
  ],
  orphanParcelKeys: ["GRUND_1_2505#115", "GRUND_1_2505#122", "GRUND_1_2505#483", "GRUND_1_2505#484", "GRUND_1_2505#488", "GRUND_1_2505#580", "GRUND_1_2505#2262"],
  verdictSi:
    "MODEL ZGRADJEN: 2760 vrstic → 2134 vnosi (2125 parcel + 9 NEBEREŽNA), zero-loss pokritost vrstic 2681 + 70 + 9 = 2760; 2632 parov parcela×raba, 430 parcel z več rabami, 49 podvojenih rab ohranjenih; klasifikacija rab (pravilnik v1, brez AI) pokrije 72,0 % parov (1896/2632: njiva 1049 ≫ travnik 487 ≫ gozd 134 …), preostalih 736 parov (230 surovih vrednosti) izrecno NEKLASIFICIRANO. Novosti nasproti P38: 7 sirot (parcela brez rabe) + 2632 pravih parov + 49 podvojenih rab. Surove vrednosti nedotaknjene, status REVIEW.",
  verdictEn:
    "MODEL BUILT: 2,760 rows → 2,134 entries (2,125 parcels + 9 NEBEREŽNA), zero-loss row accounting 2,681 + 70 + 9 = 2,760; 2,632 parcel×culture pairs, 430 multi-culture parcels, 49 duplicate cultures preserved; the culture rulebook (v1, no AI) classifies 72.0% of pairs (1,896/2,632: arable 1,049 ≫ meadow 487 ≫ forest 134 …), the remaining 736 pairs (230 raw values) are explicitly UNCLASSIFIED. New against P38: 7 orphan parcels + 2,632 true pairs + 49 duplicate cultures. Raw values untouched, status REVIEW.",
  next: [
    "3. prehod ~15 dvoumnih strani (audit §17) — tudi za 7 sirot in 9 NEBEREŽNA vrstic",
    "razširitev pravilnika rab v2 (lokalni termini: Lhut, Lohn, Ahn, Äfling …) ob paleografski potrditvi",
    "povezava modela z GEOTRUTH raba-tal conami (landuse.ts) — le kot kontekst, ne samodejna preslikava",
  ],
};

/** P40 (issue #10) — PS 1825: rekapitulacija str. 140–143 vs spravni model (P5-b). */
export const PS_RECAP_P40: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  recapitulation: {
    page: number;
    summaBauplatze: number;
    summaGrundparzellen: number;
    zusammen: number;
    areaReadingPage141: { value: number; verbatim: string; uncertain: boolean };
  };
  crossCheck: {
    checksumIdentity: { pass: boolean };
    baselineIdentity: { grundSeen: number; grundMissing: number; recapGrundparzellen: number; pass: boolean };
    p38ControlSum: { value: number; recapZusammen: number; pass: boolean };
    bauplatzeRegister: { recap: number; blattXRows: number; gap: number; coveragePct: number };
  };
  areaDecomposition: {
    klafterPerJoch: number;
    bySection: Record<string, { rowsWithArea: number; rowsWithoutArea: number; joch: number; klafter: number; jochEquivalent: number }>;
    rowsWithArea: number;
    rowsWithoutArea: number;
  };
  recapAreaAttribution: {
    recapReading: number;
    candidates: { scope: string; jochEquivalent: number; deltaJoch: number; deltaPct: number; assessment: string }[];
    closest: string;
    resolution: string;
  };
  blattXOverlap: {
    pairsGrund: number;
    pairsBlattX: number;
    pairsOverlap: number;
    ownersGrund: number;
    ownersBlattX: number;
    ownersOverlap: number;
    distinctHausNrBlattX: number;
  };
  fragmentRows140_141: { page: number; verbatim: string[]; count: number; naiveJochSum: number; resolution: string };
  numericEcho: { hypothesis: string; maxParcelNadaljevanje: number; recapZusammen: number; refuted: boolean; verdict: string };
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "PS",
  source:
    "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — rekapitulacija str. 140–143 nad committed dokazi: PS-structure.json (P9), ps-reconciliation.json (P38), ps-landuse.json (P39); polni izpis research/issue17/ps-recap.json + src/data/atlas/ps-recap.json",
  status: "REVIEW",
  generatedBy: "scripts/p40_ps_recap.py",
  recapitulation: {
    page: 143,
    summaBauplatze: 102,
    summaGrundparzellen: 2505,
    zusammen: 2607,
    areaReadingPage141: { value: 1216, verbatim: "Summa 1216(?) Joch", uncertain: true },
  },
  crossCheck: {
    checksumIdentity: { pass: true },
    baselineIdentity: { grundSeen: 1889, grundMissing: 616, recapGrundparzellen: 2505, pass: true },
    p38ControlSum: { value: 2607, recapZusammen: 2607, pass: true },
    bauplatzeRegister: { recap: 102, blattXRows: 60, gap: 42, coveragePct: 58.8 },
  },
  areaDecomposition: {
    klafterPerJoch: 1600,
    bySection: {
      BLATT_X: { rowsWithArea: 40, rowsWithoutArea: 20, joch: 262, klafter: 29966, jochEquivalent: 280.7287 },
      GRUND_1_2505: { rowsWithArea: 2378, rowsWithoutArea: 7, joch: 404, klafter: 1326343, jochEquivalent: 1232.9644 },
      NADALJEVANJE_2506: { rowsWithArea: 96, rowsWithoutArea: 0, joch: 1, klafter: 19932, jochEquivalent: 13.4575 },
      WALDUNG: { rowsWithArea: 86, rowsWithoutArea: 5, joch: 8, klafter: 47412, jochEquivalent: 37.6325 },
    },
    rowsWithArea: 2600,
    rowsWithoutArea: 32,
  },
  recapAreaAttribution: {
    recapReading: 1216,
    candidates: [
      {
        scope: "GRUND_1_2505 samo (zemljiške parcele; stavbna mesta se štejejo po kosih)",
        jochEquivalent: 1232.9644,
        deltaJoch: 16.9644,
        deltaPct: 1.4,
        assessment: "NAJBOLJ SKLADEN — odmik 1,39 % je v redu negotovosti branja »1216(?)« + 32 vrstic brez površine; odločitev paleografska",
      },
      {
        scope: "GRUND + NADALJEVANJE + WALDUNG (brez Blatt X)",
        jochEquivalent: 1284.0544,
        deltaJoch: 68.0544,
        deltaPct: 5.6,
        assessment: "možen, če rekapitulacija šteje tudi nadaljevalne in gozdne parcele — odmik 5,6 %",
      },
      {
        scope: "celoten register z Blatt X (zgornja meja)",
        jochEquivalent: 1564.7831,
        deltaJoch: 348.7831,
        deltaPct: 28.68,
        assessment: "neskladen — zahteval bi podvajanje Blatt X površin, ki ga prekrivanje parov ne dokazuje; zavrnjen",
      },
    ],
    closest: "GRUND_1_2505 samo (Δ +16.96 Joch ≈ +1.39 %)",
    resolution: "OTVORENO — paleografska potrditev branj str. 140–143 (dvomljivo »1216(?)«)",
  },
  blattXOverlap: {
    pairsGrund: 2969,
    pairsBlattX: 59,
    pairsOverlap: 1,
    ownersGrund: 1083,
    ownersBlattX: 22,
    ownersOverlap: 1,
    distinctHausNrBlattX: 59,
  },
  fragmentRows140_141: {
    page: 141,
    verbatim: ["190/1168", "133/1196", "132/1466", "206/836", "286/8931(?)", "268/1341", "198/11957(?)"],
    count: 7,
    naiveJochSum: 1413,
    resolution: "UNRESOLVED — potrebna človeška paleografija (dva VLM branja se razhajata)",
  },
  numericEcho: {
    hypothesis: "max parcela NADALJEVANJE (2506+) == Zusammen rekapitulacije (2607)",
    maxParcelNadaljevanje: 2840,
    recapZusammen: 2607,
    refuted: true,
    verdict: "OVRGAN — max parcela v NADALJEVANJE je 2840, ne 2607; številčni eho ne obstaja (negativen izid, izrecno dokumentiran)",
  },
  verdictSi:
    "Rekapitulacija str. 143 (102 + 2505 = 2607, rdeči tuš) je natanko tista kontrolna vsota, ki jo sprava (P38) uporablja od začetka, in se ujema z osnovno črto P36/P38 (1889 + 616 = 2505). Površinsko se najbolj sklada z GRUND-only (1232,96 Joch; Δ +1,39 %). Blatt X nosi površine brez dokazanega podvajanja — celotna vsota registra je samo zgornja meja. Per-house vrstice 140–141 ostajajo UNRESOLVED.",
  verdictEn:
    "The page-143 recap (102 + 2,505 = 2,607, red chalk) is exactly the control sum the reconciliation (P38) has used all along and matches the P36/P38 baseline (1,889 + 616 = 2,505). Area-wise it best matches GRUND-only (1,232.96 Joch; Δ +1.39%). Blatt X carries areas with unproven duplication — the whole-register sum is only an upper bound. The per-house rows 140–141 remain UNRESOLVED.",
  next: [
    "človeška paleografska potrditev str. 140–143 (Summa 1216(?) Joch + 7 per-house vrstic)",
    "3. prehod ~15 dvoumnih strani (tudi za 7 sirot in 9 NEBEREŽNA vrstic)",
    "razširitev pravilnika rab v2 (Lhut, Lohn, Ahn, Äfling …) ob paleografski potrditvi",
  ],
};

/** PZ — demografija in cenitev 1825 (N083PZ). */
export const PZ_ECONOMY_1825: {
  source: string;
  titleAsWritten: string;
  status: ResearchStatus;
  population: { total: number; male: number; female: number; houses: string; families: string; confidence: string };
  areaTotal: { joch: number; klafter: number; confidence: string };
  dates: { madeAsWritten: string; certificationAsWritten: string; revaluationAsWritten: string };
  valuationChain: { stepSi: string; valuesSi: string; confidence: string }[];
  economicProfileSi: string;
  economicProfileEn: string;
} = {
  source: "N083PZ str. 1–3, 20, 30, 40, 50, 60, 68–71 (Arhiv RS, SI AS 176, k.o. Griblje) — research/issue17/PZ-profile.json + PZ-valuation.json",
  titleAsWritten: "CATASTRAL-SCHÄTZUNGS-ELABORAT der Gemeinde Grüble (Land Krain, 83, Kreis Neustadtl, Steuerbezirk Krupge [~])",
  status: "REVIEW",
  population: { total: 441, male: 222, female: 219, houses: "72 [~]", families: "102 [~]", confidence: "prebivalstvo srednja; hiše/družine nizka [~]" },
  areaTotal: { joch: 2294, klafter: 516, confidence: "~ (§1)" },
  dates: { madeAsWritten: "Gemacht den 28ten Juli 1825", certificationAsWritten: "Geprüft / overovitve 9. 8. 1826 [~] in [~1824]", revaluationAsWritten: "[~1834, rdeči dodatek »revaluirt« na str. 60 — sumljivo, preveriti]" },
  valuationChain: [
    { stepSi: "Bau-Area (stavbna zemljišča) — Roh-Ertrag", valuesSi: "16 fl 50½ kr/joch", confidence: "srednja-visoka" },
    { stepSi: "Cultur-Aufwand (55 % bruto)", valuesSi: "9 fl 15¾ kr/joch (aritmetika potrjena: 55 % × 16 fl 50½)", confidence: "visoka" },
    { stepSi: "Rein-Ertrag (čisti donos stavbnih tal)", valuesSi: "7 fl 35 kr/joch", confidence: "visoka (1010,5 − 555,5 kr = 455 kr)" },
    { stepSi: "Ackerland razred I [~]", valuesSi: "Rob 20–25 fl 44 kr; Rein 12–15 fl 5 kr — 3 klice se RAZHAJAJO", confidence: "nizka" },
    { stepSi: "Wiesen razred I/II", valuesSi: "Heu 14/8 centnerjev, Grumet 6 (pridelek, ne fl)", confidence: "srednja" },
    { stepSi: "Weingärten [~C]", valuesSi: "Most 12 n.ö. Eimer/joch (pridelek)", confidence: "nizka" },
  ],
  economicProfileSi:
    "BRANJA: 441 prebivalcev (222 m/219 ž) v 72 hišah [~] / 102 družinah [~]; 2294 joch 516 kl [~] skupnega območja; donos stavbnih tal 7 fl 35 kr/joch; zaključek 28. 7. 1825. NAVKRIŽNO (PV): pašniki 636 j ≫ njive 413 j ≫ travniki 88 j ≫ vinogradi 7 j, gozd 0 — skromna rodovitnost. INFERENCA (ne branje): ~5,2 jocha/prebivalca (~19 joch/družino); 102 družini v 72 hišah [~] kažejo na večdružinska gospodinjstva; mešano poljedelstvo-živinorejo samozadostnega tipa z majhno tržno sivato; čisti donos ≈ 45 % bruto (stopnja iz Bau-Area).",
  economicProfileEn:
    "READINGS: 441 inhabitants (222 m/219 f) in 72 houses [~] / 102 families [~]; 2294 joch 516 klafter [~] total area; building land net yield 7 fl 35 kr/joch; closed 28 Jul 1825. CROSS-REF (PV): pasture 636 j ≫ fields 413 j ≫ meadows 88 j ≫ vineyards 7 j, forest 0 — modest fertility. INFERENCE (not a reading): ~5.2 joch per inhabitant (~19 joch per family); 102 families in 72 houses [~] points to multi-family households; a mixed subsistence crop-livestock economy with a small market surplus; net yield ≈ 45 % of gross (rate from the Bau-Area chain).",
};

/** PUA — nadaljevanje po straneh A–B (issue #17): strani 3–10, 17 vrstic. */
export interface PuaOwnerRow {
  page: number;
  row: number;
  nameAsWritten: string;
  houseNos: string[];
  sections: string;
  confidence: string;
}

export const PUA_CONTINUATION: {
  source: string;
  status: ResearchStatus;
  pagesRead: number[];
  rows: PuaOwnerRow[];
  divergences: string[];
  noteSi: string;
} = {
  source: "N083PUA str. 3–49 (Arhiv RS, SI AS 176, k.o. Griblje) — research/issue17/PUA-more.json + P3 str. 11 + P4 str. 12–34 + P5-b str. 35–49 (research/p3/pua-12plus-parsed.json, 38 strani, 1 VLM klic/stran; P5-b prebrano 2026-10-08 ob dvigu kvote)",
  status: "REVIEW",
  pagesRead: [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
  rows: [
    { page: 3, row: 1, nameAsWritten: "Hölloschitsch Wufa Luina hau Dragosche [~]", houseNos: ["1"], sections: "II: 821–1084; IV: 1850–2410", confidence: "~ (alternativa prejšnjega branja: Adlolschitz Wulff Ludwig von)" },
    { page: 3, row: 2, nameAsWritten: "Bringz Wufa Luina hau Grüble [~]", houseNos: ["20 ali 23"], sections: "I–V (številne parcele; opomba B. K. 35)", confidence: "~" },
    { page: 3, row: 0, nameAsWritten: "Baron Abfalterer [~] (institucija)", houseNos: [], sections: "I: 72", confidence: "~" },
    { page: 4, row: 3, nameAsWritten: "Bring Migan/Michael Bauern hiesig Grübln [~]", houseNos: ["24"], sections: "I: 479–751; II: 1166–1644; III–IV: 1808–2168 (opomba B. A. 25)", confidence: "~" },
    { page: 4, row: 4, nameAsWritten: "Bring Miß/Martin Bauern hiesig Grübln [~]", houseNos: ["25"], sections: "I: 478–800; III: 1807–1951; IV: 2161–2168 (opomba B. P. 29)", confidence: "~" },
    { page: 5, row: 5, nameAsWritten: "Bring Johann Bräun [~] houlg.", houseNos: ["26"], sections: "—", confidence: "~" },
    { page: 5, row: 6, nameAsWritten: "Bring Mäda/Manda [~] (Magdalena) Brünn [~]", houseNos: ["28"], sections: "—", confidence: "~" },
    { page: 6, row: 7, nameAsWritten: "Brulla Mako/Matho Bünnhaußgübl [~] (alternative: Brinig, Brinc)", houseNos: ["43"], sections: "I: 78–243", confidence: "~" },
    { page: 6, row: 8, nameAsWritten: "Bring Manda Brinahug [~]", houseNos: ["63"], sections: "—", confidence: "~" },
    { page: 6, row: 9, nameAsWritten: "Commenda Vachernebel [~] (institucija — komenda)", houseNos: ["0"], sections: "—", confidence: "~" },
    { page: 7, row: 10, nameAsWritten: "Decklitsch Matthäus Bürger hiesig [~]", houseNos: ["33"], sections: "—", confidence: "~" },
    { page: 7, row: 11, nameAsWritten: "Dragosch Johann Bürger hiesig, Gemeinde Deschitz [~]", houseNos: ["3"], sections: "—", confidence: "~" },
    { page: 8, row: 12, nameAsWritten: "Dragosch Mavroslawitsch hiesig Dragosche, Gemeinde Molestitch [~]", houseNos: ["4"], sections: "—", confidence: "~" },
    { page: 8, row: 13, nameAsWritten: "Dragosch Georglawitsch zu Dragosche [~]", houseNos: ["5"], sections: "—", confidence: "~" },
    { page: 9, row: 14, nameAsWritten: "Fillah Michael Mühldörfler haußgübl [~]", houseNos: ["16"], sections: "—", confidence: "~" },
    { page: 9, row: 15, nameAsWritten: "Fillah Maria [~]", houseNos: ["34"], sections: "—", confidence: "~" },
    { page: 10, row: 16, nameAsWritten: "Fillah Jetter [~]", houseNos: ["36"], sections: "—", confidence: "~" },
    { page: 10, row: 17, nameAsWritten: "Fillah Miho [~]", houseNos: ["61"], sections: "I: 8–220; III: 745–1238; II: 814–1861", confidence: "~" },
    { page: 11, row: 18, nameAsWritten: "Hlebety Johann, Bauer hiesig zu Grüble [~]", houseNos: ["2"], sections: "II: 886–1789 (33 parcel); IV: 2089–2408; b.P. 26", confidence: "~ (PT: Hlebetz Jan hiša 26 — divergentna hišna št.)" },
    { page: 11, row: 19, nameAsWritten: "Huditsch Musto, Häusler hiesig [~]", houseNos: ["14"], sections: "I: 104–430 (18); II: 1150–2130 (10); V: 2476–2579; b.P. 87/89/91", confidence: "~" },
    { page: 11, row: 20, nameAsWritten: "Husitsch Baron von Gradatz [~] (plemiška/institucionalna lastnina)", houseNos: [], sections: "III: 746, 777", confidence: "~" },
    { page: 11, row: 21, nameAsWritten: "Hutweiz Johann, Bauer zu Waldendorf [~] (lastnik iz sosednje vasi)", houseNos: ["8"], sections: "IV: 2178", confidence: "~" },
     { page: 12, row: 22, nameAsWritten: "Höflehner Johann [~]", houseNos: ["6"], sections: "I: 47.; II: 841–1743 (28); IV: 2222–2592 (8); b.P. im III.", confidence: "~ (PT hiša 6: Tilel Miho)" },
    { page: 12, row: 23, nameAsWritten: "Höflehner Mathäus [~]", houseNos: ["8"], sections: "I: 503, 507, 511, 519, 817.; II: 819–1716 (13); IV: 2283–2427 (7) + 2228[?]; b.P. 11. 12. 10.", confidence: "~ (PT hiša 8: Lebing/Lebring Mädl. [~])" },
    { page: 13, row: 24, nameAsWritten: "Jakobstitzsch Johann [~]", houseNos: ["9"], sections: "II: 1077.", confidence: "~ (PT hiša 9: Stalhutstetisch Miho)" },
    { page: 13, row: 25, nameAsWritten: "Jakobstitzsch Nicolauß [~]", houseNos: ["13"], sections: "I: 803, 814, 815, 816, 785; II: 843–1742 (22); IV: 2292, 2411, 2425, 2380; V: 2530; b.P. D. P. 9. 10.", confidence: "~ (PT hiša 13: Stalhutstetisch Ruard)" },
    { page: 14, row: 26, nameAsWritten: "Jankovitsche Muffl bauernhow Zerguische [~]", houseNos: ["7"], sections: "V: 2810, 2811", confidence: "~ (PT hiša 7: Lebing/Lebring Mädl. [~])" },
    { page: 14, row: 27, nameAsWritten: "Jankowitsche Juran bauernhow Zerguische [~]", houseNos: ["26"], sections: "V: 2873, 2874, 2878, 2879", confidence: "~ (PT hiša 26: Hlebetz Jan)" },
    { page: 15, row: 28, nameAsWritten: "Janko vitnik [~]", houseNos: ["21"], sections: "V: 221, 2518", confidence: "~ (PT hiša 21: Šture Majzel)" },
    { page: 15, row: 29, nameAsWritten: "Janko vity [~]", houseNos: ["3"], sections: "IV: 2440, 2459, 2460", confidence: "~ (PT hiša 3: Šimec Jakob)" },
    { page: 16, row: 30, nameAsWritten: "Kristan Mäusel buaß hulgäßl [~]", houseNos: ["3"], sections: "I: 489.; II: 858–1769 (44); IV: 1792.1812.; V: 2216.; b.P. b.P. 19, 20.", confidence: "~ (PT hiša 3: Šimec Jakob)" },
    { page: 16, row: 31, nameAsWritten: "Lure Mäusel buaß hulgäßl [~]", houseNos: ["10"], sections: "II: 858–1708 (14); IV: 2211–2428 (17); b.P. b.P. 21.22.", confidence: "~ (PT hiša 10: Stalhutstetisch Miho)" },
    { page: 17, row: 32, nameAsWritten: "Loral Miko bauers hof Gsübln [~]", houseNos: ["15"], sections: "II: 779–1968 (10); III: 1797, 1798, 1799, 1800; IV: 2078–2362 (19)", confidence: "~ (PT hiša 15: Stalhutstetisch Jhan (Hrovatic Jhan))" },
    { page: 17, row: 33, nameAsWritten: "Loral Thoma bauers hof Gsübln [~]", houseNos: ["17"], sections: "II: 780–1790 (19); IV: 2031–2366 (15); V: 2671, 2572", confidence: "~ (PT hiša 17: Stalhutsch Marko)" },
    { page: 18, row: 34, nameAsWritten: "Krischan Mandschurischka / Griblje [~]", houseNos: ["31"], sections: "I: 102–601 (9); II: 1290, 1391, 1492, 1593, 2019, 1462; III: 1866; IV: 1806, 1807, 1858, 1985?, 2118, 2128; b.P. 30.", confidence: "~ (PT hiša 31: Bring Marko)" },
    { page: 18, row: 35, nameAsWritten: "Krischan Malfs Leurschkau / Griblje [~]", houseNos: ["36"], sections: "I: 135–422 (26) + 154h, 177h; II: 1182, 1287, 1286, 1294, 1312; IV: 1967, 2100; V: 2474, 2478, 2523, 2528; b.P. 86. 88.", confidence: "~ (PT hiša 36: Milleg Hans [~])" },
    { page: 19, row: 36, nameAsWritten: "Krischan Patta Buirshofgäubla [~]", houseNos: ["37"], sections: "I: 126–431 (29) + 174½; II: 1153.1195.1321.1460.; IV: 1968.1978.; V: 2192.2473.2479.3824.; b.P. 85.", confidence: "~ (PT hiša 37: Brinig Malfa [~])" },
    { page: 19, row: 37, nameAsWritten: "Krischan Halfa Buirshofgäubla [~]", houseNos: ["57"], sections: "I: 225.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 20, row: 38, nameAsWritten: "Kosirhan Mäda Bauer zu Griblje [~]", houseNos: ["62"], sections: "I: 4–349 (14) + 340 343; II: 441–1642 (21) + 1217 1357; III: 1876.1860.; IV: 2038–2254 (14) + 2145 2152; b.P. b. 9. 52.", confidence: "~ (PT hiša 62: Lappanig Miho)" },
    { page: 20, row: 39, nameAsWritten: "Schloßthaler Jätten Bauer zu Gribljen [~]", houseNos: ["46"], sections: "I: 162.; II: 1022.1104.1107.1110.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 21, row: 40, nameAsWritten: "Nikolaus Grönig bauer und Gailb. [~]", houseNos: ["63"], sections: "I: 2–391 (14) + k; II: 744. 760. 764. 776.; III: 788–1299 (10); IV: 1275–1940 (8); V: 1844. 1845.; b.P. 2029. 2040. 2041. 2070. 2079. 2082. 2091. 2107. 2107. 2108. 2109. 2110. 2119. 2146. 2187. 2259", confidence: "~ (PT hiša 63: Šimec Ripane)" },
    { page: 21, row: 41, nameAsWritten: "Nikolaus Grönig bauer und Gailb. [~]", houseNos: ["66"], sections: "I: 10–686 (8); II: 751. 762. 764.; III: 1006–1304 (9) + [?]41; IV: 1423. 1455. 1948.; V: 1862. 1875!; III.IV: 1956; b.P. 1977. 1980. 2000.", confidence: "~ (PT hiša 66: Šimec Jhan)" },
    { page: 22, row: 42, nameAsWritten: "Matthäus Wundsch [~]", houseNos: ["47"], sections: "I: 86–615 (21); II: 1100–1511 (14); IV: 1808, 1976, 2000, 2126; V: 2431, 2494, 2495, 2503; b.P. 72, 71, 78, 80", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 22, row: 43, nameAsWritten: "Kristan Matjaž Bučar [~]", houseNos: ["69"], sections: "II: 859–1776 (27); IV: 2220–2879 (11)", confidence: "~ (PT hiša 69: Filak Peter)" },
    { page: 22, row: 44, nameAsWritten: "Kirche H. Veith [~]", houseNos: ["0"], sections: "—; b.P. Lq. i2.", confidence: "~ (institucija)" },
    { page: 23, row: 45, nameAsWritten: "Hlobutschar Georg baur hiesig geb. [~]", houseNos: ["48"], sections: "I: 94–604 (20); II: 1206–1578 (9); III: 1883, 1899, 1902; IV: 3002, 3159; V: 2490, 2499", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 23, row: 46, nameAsWritten: "Kleppetz Georg büuerl hiesig Gemeinde: Hie Leusthal [~]", houseNos: ["2"], sections: "IV: 2294, 2309, 2351, 2976, 3077, 3086, zum Theil 1829", confidence: "~ (PT hiša 2: Veith (St.?) [~])" },
    { page: 24, row: 47, nameAsWritten: "Lukentitz Matho [~]", houseNos: ["7"], sections: "I: 49, 203, 611, 615, 790, 618.; II: 939–1712 (22); IV: 2281, 2298, 2412, 2422, 2580, 2581.; b.P. b.P. in", confidence: "~ (PT hiša 7: Lebing/Lebring Mädl. [~])" },
    { page: 24, row: 48, nameAsWritten: "Lukentitz Wolf [~]", houseNos: ["12"], sections: "II: 832–1805 (14); III: 1791, 1787.; IV: 2295, 2018, 2420.", confidence: "~ (PT hiša 12: Stalhutstetisch Marko)" },
    { page: 25, row: 49, nameAsWritten: "Rappar Nicolaus bau Gsöbln [~]", houseNos: ["54"], sections: "I: 24–418 (13); II: 770–1610 (14); III: 1913, 1924; IV: 2006–2076 (8); V: 2084–2815 (11); b.P. 62. 67.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 25, row: 50, nameAsWritten: "Millea Johann bau Gsöbln [~]", houseNos: ["22"], sections: "I: 107–680 (7); II: 1093–1646 (12); III: 1882, 1904, 1964, 1965; b.P. 9. 96", confidence: "~ (PT hiša 22: Šture Majzel)" },
    { page: 26, row: 51, nameAsWritten: "Mallestitak [~]", houseNos: ["27"], sections: "I: 468–718 (20); II: 1002.1011.1023.1106.1147.; IV: 2106–2169 (8); V: 1944.1990.; III/IV: 1810.1870.1920.; b.P. D. P. 40.", confidence: "~ (PT hiša 27: Jožef Miko)" },
    { page: 26, row: 52, nameAsWritten: "Millej [~]", houseNos: ["29"], sections: "I: 15–801 (16); II: 1221.1228.1402.1408.1421.1422.; b.P. D. P. 04 24", confidence: "~ (PT hiša 29: Krišan Gregor)" },
    { page: 27, row: 53, nameAsWritten: "Noah Mandl bauer zu Griblje [~]", houseNos: ["4"], sections: "I: 50, 256, 809, 881, 789; II: 808–1837 (31); IV: 2219–2377 (8); V: 2461", confidence: "~ (PT hiša 4: Šimec Matija)" },
    { page: 27, row: 54, nameAsWritten: "Georg Grangl bauer zu Griblje [~]", houseNos: ["11"], sections: "I: 62; II: 765; III: 857–1715 (16); IV: 2216–2360 (11); b.P. 22", confidence: "~ (PT hiša 11: Stalhutstetisch Marko)" },
    { page: 28, row: 55, nameAsWritten: "Poldiŕg Mufa/buͤrſn/zu Gribla [~]", houseNos: ["14"], sections: "I: 24.42.124.123.; II: 996–1889 (11); IV: 2034–2286 (8); b.P. b.P.7.8.", confidence: "~ (PT hiša 14: Stalhutstetisch Jhan (Ivan))" },
    { page: 28, row: 56, nameAsWritten: "Polcig Michael buͤrſn/zu/gribla [~]", houseNos: ["20"], sections: "I: 735:; II: 1115–1187 (17); IV: 1998.2010.", confidence: "~ (PT hiša 20: Krištan/Kraihan Mäfa [~])" },
    { page: 29, row: 57, nameAsWritten: "Jožeg Muhč Bauer houlgübl [~]", houseNos: ["21"], sections: "I: 732.70h.; II: 119–1118 (23); IV: 1979.999; III/IV: 9581", confidence: "~ (PT hiša 21: Šture Majzel)" },
    { page: 29, row: 58, nameAsWritten: "Peterig Muhč Bauer houlgäble [~]", houseNos: ["40"], sections: "I: 161–728 (27) + 177c; II: 1114–1486 (13); III: 1830–1901 (9); IV: 1978.1995.2013; V: 2006.2534; III/IV: 1957.1962.1883.18951; b.P. 93.94", confidence: "~ (PT hiša 40: Brinig Malfa [~])" },
    { page: 30, row: 59, nameAsWritten: "Georg Leiner [~]", houseNos: ["41"], sections: "I: 39–729 (29); II: 1026–1489 (18); III: 1838, 1841, 1848, 1854; IV: 1973, 1988, 1994, 2019; V: 2804; III-IV: 1959; b.P. J.P. 92.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 30, row: 60, nameAsWritten: "Matthäus Leiner [~]", houseNos: ["42"], sections: "I: 37–618 (17) + [~], [~]72; II: 1098–1808 (11); III: 1232; IV: [~]aib [~]i[~]; III.1: 1869, 1960, 1992", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 31, row: 61, nameAsWritten: "Georg Rußa Bauer zu Griblje [~]", houseNos: ["60"], sections: "I: 20–749 (22); II: 806–1556 (11); III: 1821, 1822; IV: 2001–2371 (15); V: 2481–2659 (8); b.P. 73", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 31, row: 62, nameAsWritten: "Georg Juttner Bauer zu Griblje [~]", houseNos: ["62"], sections: "I: 853, 870; II: 1101; IV: 2197; V: 2500–2693 (7)", confidence: "~ (PT hiša 62: Lappanig Miho)" },
    { page: 32, row: 63, nameAsWritten: "Peter Jhan Buidl / Buidlgübln [~]", houseNos: ["53"], sections: "I: 25–1117 (12); II: 782–1365 (14) + 1340[?]; IV: 2004–2400 (14); V: 2509, 2564, 2603, 2616; b.P. A. P. bi. 65.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 32, row: 64, nameAsWritten: "Joseph Gnoy Buida / Buidlgübln [~]", houseNos: ["67"], sections: "I: 480–702 (13); II: 1224, 1228; III: 1871, 1909, 1935, 1937, 1938, 1939; IV: 1963, 2009, 2108; V: 2612, 2641; b.P. B. P. 41.", confidence: "~ (PT hiša 67: Lappanig Miho)" },
    { page: 33, row: 65, nameAsWritten: "Pasticz Georg Bauernholds gemuth [~]", houseNos: ["4"], sections: "V: 206. 810.", confidence: "~ (PT hiša 4: Šimec Matija)" },
    { page: 33, row: 66, nameAsWritten: "Pacharistche Michl bauernholds gemüth [~]", houseNos: ["6"], sections: "V: 292.", confidence: "~ (PT hiša 6: Tilel Miho)" },
    { page: 34, row: 67, nameAsWritten: "Prodoritche Miho Bauernholds Gremium [~]", houseNos: ["7"], sections: "V: 2569. 2570. 2565. 2556.", confidence: "~ (PT hiša 7: Lebing/Lebring Mädl. [~])" },
    { page: 34, row: 68, nameAsWritten: "Pfister Blaž Bauernholds Güble [~]", houseNos: ["59"], sections: "—", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 35, row: 69, nameAsWritten: "Gemeinde Malfz Brandhofgässl [~]", houseNos: ["1"], sections: "II: 888–1613 (19); 1621.1622.1625'.1682.1698.1702. 1758.1771.1772.; III: 1758.1789.; IV: 2247.2272.2005;; b.P. B.P. eh. 28.", confidence: "~ (PT hiša 1: Veith (H.) [~])" },
    { page: 35, row: 70, nameAsWritten: "Gemeinde Malfz Brandhof Smibuche [~]", houseNos: ["31"], sections: "V: 2537.", confidence: "~ (PT hiša 31: Bring Marko)" },
    { page: 36, row: 71, nameAsWritten: "Starašinutsh Gura Leurakau Zgorsche [~]", houseNos: ["17"], sections: "V: 2571, 2572", confidence: "~ (PT hiša 17: Stalhutsch Marko)" },
    { page: 36, row: 72, nameAsWritten: "Strutz Jh. Bauernhof Grüble [~]", houseNos: ["3"], sections: "II: 940–1740 (26); IV: 2218–2401 (15)", confidence: "~ (PT hiša 3: Šimec Jakob)" },
    { page: 36, row: 73, nameAsWritten: "Hansitsch Jürgen Bäurin von Wiedendorf [~]", houseNos: ["3"], sections: "IV: 2175; b.P. D.p. 15, 16, 18", confidence: "~ (PT hiša 3: Šimec Jakob)" },
    { page: 37, row: 74, nameAsWritten: "Schimcz [~] Gutta Bauernhofgütl", houseNos: ["18"], sections: "II: 776. 776.; III: 796–1677 (25); IV: 2044–2599 (9); b.P. 119h", confidence: "~ (PT hiša 18: Hrovat Jhan)" },
    { page: 37, row: 75, nameAsWritten: "Schimcz Maffa Bauernhofgütl [~]", houseNos: ["19"], sections: "II: 801–1678 (11); III: 1783. 1789. 1784. 1785.; IV: 2186. 2271. 2532.", confidence: "~ (PT hiša 19: Krudelen Matija)" },
    { page: 38, row: 76, nameAsWritten: "Stübler Muffl Bauer zu Griblje [~]", houseNos: ["30"], sections: "I: 427–622 (21); II: 1091–1409 (8); III: 1880.1882.1883.1919.1943; IV: 1952; V: 1991–2209 (13); b.P. B.P. 114.", confidence: "~ (PT hiša 30: Krišan Gregor)" },
    { page: 38, row: 77, nameAsWritten: "Schimer Georg Bauer zu Griblje [~]", houseNos: ["38"], sections: "I: 160–591 (9); II: 1158–1384 (11); III: 1850.1852; IV: 1966.1976.1997.2011.2119.2129; b.P. B.P. 96.", confidence: "~ (PT hiša 38: Brinig Malfa [~])" },
    { page: 39, row: 78, nameAsWritten: "Schimey Maro baua haußgäbla [~]", houseNos: ["29"], sections: "I: 102–609 (8); II: 1166–1825 (12); III: 1851, 1863, 1864, 1876; IV: 1974, 1996, 2012, 2030; I.II: 1162; b.P. 95. 97.", confidence: "~ (PT hiša 29: Krišan Gregor)" },
    { page: 39, row: 79, nameAsWritten: "Strauß Georg baua haußgübla [~]", houseNos: ["45"], sections: "I: 88–596 (33); II: 798–1802 (24); III: 1886, 1897, 1903, 1925, 1926; IV: 1984–2285 (8); V: 2815; III.IV: 1958; b.P. 76. 79. 81, 82. 83. 84.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 40, row: 80, nameAsWritten: "Schimetz Michael Baunthofgäbln [~]", houseNos: [], sections: "I: 26–857 (12); II: 774; III: 787–1099 (9); IV: 1963; V: 2008–2870 (14); III.IV: 1229,1254,1326,1382,1541,1566,1648; b.P. b. P. 63.", confidence: "~" },
    { page: 40, row: 81, nameAsWritten: "Schimetz Hanß Baunthofgübln [~]", houseNos: ["55"], sections: "I: 60–422 (21); II: 507–2051 (24); III: 1818,1825,1828,1829; IV: 2031–2358 (25) + 2409[?]; V: 2442–2546 (8); III.IV: 1786; b.P. b. P. bo. 64. 66.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 41, row: 82, nameAsWritten: "Schumetz Juttan [~]", houseNos: ["56"], sections: "I: 45–423 (17); II: 797–1650 (22); III: 1823, 1906; IV: 1989–2548 (27); b.P. B. P. 59.", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 41, row: 83, nameAsWritten: "Stepanitsch Jakob Laurentzhow Gütte [~]", houseNos: ["58"], sections: "II: 1854", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 41, row: 84, nameAsWritten: "Schimey Stoffe Lorenz how Gribatsche [~]", houseNos: ["31"], sections: "V: 2801", confidence: "~ (PT hiša 31: Bring Marko)" },
    { page: 42, row: 85, nameAsWritten: "Schello Georg Bauer/b zu Gribla [~]", houseNos: ["60"], sections: "I: 10–873 (7) + 811/2; II: 794, 1234; III: 1250, 1265, 1280, 1496, 1522, 1481; V: 2487, 2489, 2689, 2554, 2833, 2836; b.P. b. P. 50, 51, 55;", confidence: "~ (PT: 42–60 brez hišnih št. (renumeracija P3))" },
    { page: 42, row: 86, nameAsWritten: "Strauß Niklo Bauer/b zu Gribla [~]", houseNos: ["71"], sections: "—", confidence: "~ (PT hiša 71: Filak Mihel)" },
    { page: 43, row: 87, nameAsWritten: "Strauß Mariz' baur/kaufgäbl [~]", houseNos: ["72"], sections: "—", confidence: "~ (PT hiša 72: Dikobutar Mihelo)" },
    { page: 43, row: 88, nameAsWritten: "Urlich Georg baur/kauf/gübln [~]", houseNos: ["32"], sections: "I: 55–650 (11); II: 756.1235.; III: 800–1815 (17); IV: 2063–2581 (8); b.P. D I. 54. 57. 58.", confidence: "~ (PT hiša 32: Bring Marko)" },
    { page: 44, row: 89, nameAsWritten: "Ulrich Pitter Bauer zu Gribla [~]", houseNos: ["31"], sections: "I: 27–750 (14); II: 805–1646 (18); III: 1795,1796.; IV: 2000–2187 (17) + 2385½; V: 2499–2270 (10); b.P. 774. 775.", confidence: "~ (PT hiša 31: Bring Marko)" },
    { page: 44, row: 90, nameAsWritten: "Ulrich Mida Bauer zu Gribla [~]", houseNos: ["68"], sections: "I: 56–575 (10) + iii; II: 786.,; III: 799–1777 (17); IV: 2064,2241,2242,2496,2552.; b.P. 516.", confidence: "~ (PT hiša 68: Dikobutar Rupre)" },
    { page: 44, row: 91, nameAsWritten: "Uebersprungene Parzellen=Numern. [~]", houseNos: [], sections: "I: 1–887 (13); IV: 2268.", confidence: "~" },
    { page: 44, row: 92, nameAsWritten: "Waisenkinder [~] von Weixelbaum", houseNos: ["6"], sections: "—; b.P. 216", confidence: "~ (PT hiša 6: Tilel Miho)" },
    { page: 45, row: 93, nameAsWritten: "Verbitzcher Mathä bau[er]haußgütl [~]", houseNos: ["64"], sections: "I: 2–264 (7); II: 1000–1779 (16); III: 939–1848 (9); IV: 1800,1983; b.P. b. p. 50.", confidence: "~ (PT hiša 64: Šimec Jhan)" },
    { page: 45, row: 94, nameAsWritten: "Wardian Mathä bau[er]haußgütlein [~]", houseNos: ["1"], sections: "I: Gemeinde Ackerstück; V: 2148–8577 (14)", confidence: "~ (PT hiša 1: Veith (H.) [~])" },
    { page: 46, row: 95, nameAsWritten: "Waschitzste M. mit Braut von Weidendorf [~]", houseNos: ["6"], sections: "IV: 2176, 2461, 2462", confidence: "~ (PT hiša 6: Tilel Miho)" },
    { page: 46, row: 96, nameAsWritten: "Wentschitsch M. Pfgl. Baur. b. Weidendorf [~]", houseNos: ["7"], sections: "V: 2157, 2457", confidence: "~ (PT hiša 7: Lebing/Lebring Mädl. [~])" },
    { page: 47, row: 97, nameAsWritten: "Zollamt S. L. Aversarial in Gribla [~]", houseNos: ["70"], sections: "III: 767; b.P. B. P. 98.", confidence: "~ (PT hiša 70: Filak Peter)" },
    { page: 48, row: 98, nameAsWritten: "Wge mit der Gemeinde Gribla [~]", houseNos: [], sections: "I: 2688. 2689.; II: 2690–2699 (10); III: 2596–2607 (10); IV: 2601.; V: 2608–2631 (24); b.P. 2636. 2637. 2638. 2639. 2640. 2641. 2642. 2643. 2644. 2645. 2646. 2647. 2648. 2649. 2650. 2651.", confidence: "~" },
    { page: 48, row: 99, nameAsWritten: " [~]", houseNos: [], sections: "I: 2652–2687 (36)", confidence: "~" },
    { page: 49, row: 100, nameAsWritten: "J. Lipovšek zu Griblje [~]", houseNos: [], sections: "—; b.P. 2700", confidence: "~" },
  ],
  divergences: [
    "PUA hiša 24 (Bring Michael [~]) UJEMA se z model.ts lastnik-bring-weygandt (houseRefs vsebuje 24) — navzkrižna potrditev",
    "PUA hiša 25 (Bring Martin [~]) UJEMA se z model.ts lastnik-bring-math (houseRefs 25) — navzkrižna potrditev",
    "PUA hiše 3–5 = Dragosch [~]; PT strojno branje pa Šimec/Šimec/Knavc — divergenca dveh strojnih branj [~]",
    "PUA Fillah v hišah 16/34/36/61; PT Filak v hišah 69–71 — ista družina [~], divergentne hišne št.",
    "Institucionalna lastnika brez hišnih št. (Baron Abfalterer, Commenda Vachernebel) — nov tip lastništva, ki ga PT register ne zajame",
    "P3 str. 11: Hlebety Johann Haus 2 [~] — PT beri Hlebetz Jan hiša 26 [~] — ista družina, divergentni hišne št. [~]",
    "P3 str. 11: Husitsch Baron von Gradatz — plemiška/institucionalna lastnina (sek. III: 746, 777); Hutweiz Johann zu Waldendorf Haus 8 — lastnik iz sosednje vasi Waldendorf",
    "P4 str. 22 v. 44: Kirche H. Veith [~] — CERKEV SV. VIDA kot institucionalna lastnica (brez hišne št.) — pomembna indikacija za PT hiši 1–2 »Veith (H./St.?)« [~]: začetnica H. = Heilig(er) Veith?",
    "P4: hišne št. PUA (22–68) se NE ujemajo s PT lastniki po številkah (npr. PUA hiša 6 Höflehner vs PT hiša 6 Tilel Miho) — potrjena hipoteza, da PUA in PT uporabljata RAZLIČNO številčenje hiš [~]; primerjava po imenih, ne po št.",
    "P4: PUA ohranja hišne št. v območju 41–60 (Leiner 41/42, Schloßthaler 46, Wundsch 47, Hlobutschar 48, Rappar 54, Krischan Halfa 57, Pfister 59, Rußa 60) — kjer PT register po P3 renumeraciji št. nima (blok brez št. + preskok na 61) [~]",
    "P4 str. 16–19: Krischan Mandschurischka (31), Krischan Malfs (36), Krischan Patta (37), Krischan Halfa (57) [~] — priimek K–M [~], vzporeden s PT Brinig/Milleg branjami istih vrstic [~]",
    "P4 str. 14: Jankowitsche Juran [~] hiša 26 — ime Juran/Janez konvergira s PT Hlebetz Jan hiša 26 [~] (ista hišna št. po naključju ali isti lastnik, divergentna branj)",
    "P4 str. 25–26: Rappar/Millea/Mallestitak/Millej [~] — novi priimki, ki v PT niso potrjeni (Millea ≈ Milleg [~]?)",
    "P5-b: hiša 60 ima DVA PUA lastnika (Rußa #61 str. 31 in Schello #85 str. 42) — W.60 se ujema s Schellom (MATCH 1,0) [~]",
    "P5-b: W.65 (Bring Marko / Glan Simonz) nima PUA protistrani na str. 35–49 — vrzel v registru ali bralna zmota [~]",
    "P5-b: napoved h68 POTRJENA (Ulrich Mida, MATCH 1,0); h32 delno v prid (Urlich Georg, 0,67); h64 zavrnjena (Verbitzcher, 0,46) [~]",
  ],
  noteSi:
    "Register ni strogo abeceden po sodobnih črkah — vsebuje hišna imena (zu Dragosche) in patronimike (Mavroslawitsch). P4 (2026-10-08): strani 12–34 prebrane (23 strani, 47 vnosov, 1 VLM klic/stran, zap. št. 22–68). P5-b (2026-10-08): strani 35–49 prebrane (15 strani, 32 vnosov, zap. št. 69–100) — REGISTER CEL (38 strojno branih strani, 101 vnosov) — vse ostaja REVIEW, strojno branje ni dokazni vir. PUA in PT očitno številčita hiše različno (zgodovinska ugotovitev [~]). UGOTOVITVE P5-b: hiša 60 ima DVA PUA lastnika (Rußa #61 str. 31 in Schello #85 str. 42) [~]; skupinski vnosi (Gemeinde Malfz Brandhofgässl #69, Uebersprungene Parzellen-Numern #91, Wge mit der Gemeinde Gribla #98) + vrstica #99 brez imena — konec registra vsebuje konsolidirane/preskočene parc. št. Imena velikih družin stabilna med ponovljenimi klici; hišne št. negotove [~]. Surovi VLM izpisi: research/p3/pua-raw/.",
};

/** P5 — navzkrižna analiza PUA ↔ PT (deterministična, brez AI; 2026-10-08). */
export const PUA_PT_CROSS: {
  date: string;
  method: string;
  status: ResearchStatus;
  artifact: string;
  counts: {
    puaEntries: number;
    ptHouseRows: number;
    ptParcelRows: number;
    withReadableHouseNo: number;
    directSurnameMatch: number;
    divergent: number;
    weakMatch: number;
    ptNumbersCovered: number;
    ptNumbersWithoutPua: number;
    puaHouseNosWithoutPt: number;
    surnamesInBothRegisters: number;
  };
  surnameOverlaps: { puaSurname: string; ptSurname: string; puaHouses: string; noteSi: string }[];
  findingSi: string;
  findingEn: string;
  caveatsSi: string;
  caveatsEn: string;
  nextStepSi: string;
  nextStepEn: string;
} = {
  date: "2026-10-08",
  method: "Deterministična navzkrižna primerjava (skript scripts/pua-pt-cross.py, Levenshtein podobnost normaliziranih priimkov, prag ujemanja 0,72 / verjetno 0,50) — brez AI klicev; po P5-b: 101 vnosov PUA (str. 3–49, register CEL); opomba: 84 hišnih vrstic PT = 83 edinstvenih št. (št. 34 je prečrtana dvojnica — 2 vrstici, 1 številka)",
  status: "REVIEW",
  artifact: "research/p5/pua-pt-cross.json",
  counts: {
    puaEntries: 101,
    ptHouseRows: 84,
    ptParcelRows: 21,
    withReadableHouseNo: 91,
    directSurnameMatch: 0,
    divergent: 72,
    weakMatch: 3,
    ptNumbersCovered: 48,
    ptNumbersWithoutPua: 35,
    puaHouseNosWithoutPt: 16,
    surnamesInBothRegisters: 11,
  },
  surnameOverlaps: [
    { puaSurname: "Bring / Bringz", ptSurname: "Bring/Brinig", puaHouses: "24, 25, 26, 28, 63, (20/23)", noteSi: "v PT na 31, 32, 35, 37, 38, 40 — ista družina, RAZLIČNE hišne št." },
    { puaSurname: "Hlebety", ptSurname: "Hlebetz", puaHouses: "2", noteSi: "v PT na 26 — ista družina, različna št." },
    { puaSurname: "Kristan / Krischan", ptSurname: "Krišan/Krištan", puaHouses: "3, 31, 36, 37, 57, 69", noteSi: "v PT na 29, 30 (Gregor) — vzporedna branja istih vrstic [~]" },
    { puaSurname: "Millea / Millej", ptSurname: "Milleg", puaHouses: "22, 29", noteSi: "v PT na 34, 36 — ista družina, različne št." },
    { puaSurname: "Jožeg (ime)", ptSurname: "Jožef Miko (ime)", puaHouses: "21", noteSi: "ujemanje imen, ne priimkov — šum, ne štejemo kot družino" },
    { puaSurname: "Strauß", ptSurname: "Strauß", puaHouses: "45, 71, 72", noteSi: "P5-b: nova družina v obeh registrih (PUA str. 39/42–43)" },
    { puaSurname: "Schimetz / Schumetz [~]", ptSurname: "Schmerz [~]", puaHouses: "55, 56", noteSi: "P5-b: verjetno ista družina, divergentna branja S-ch [~]" },
  ],
  findingSi:
    "KVANTIFICIRANA UGOTOVITEV (posodobljeno po P5-b — register CEL): pri 91 vnosih PUA z berljivo hišno št. NI NOGA neposrednega ujemanja priimka z lastnikom iste hišne št. v PT (0/91; 72 divergenc s podobnostjo < 0,50). Priimki, ki obstajajo v obeh registrih (Bring, Hlebety, Kriš(t)an, Milleg, Strauß, Schimetz/Schumetz [~] — skupaj 11), nastopajo na RAZLIČNIH hišnih številkah. PUA vsebuje tudi lastnike iz sosednjih vasi (Deschitz, Dragosche, Waldendorf, Leusthal) in institucije (cerkev sv. Vida, komenda, baron Gradatz), ki jih PT register hiš ne zajame; PUA hišne št. se končajo pri ~69, PT pa pri 98. Sklep (hipoteza, [~]): PUA je abecedni indeks lastnikov PARCEL z lastno hišno referenco, ki ni enaka konskripcijski številčenju hiš v PT — primerjava med serijama je možna le po imenih, ne po številkah.",
  findingEn:
    "QUANTIFIED FINDING (updated after P5-b — register COMPLETE): across 91 PUA entries with a readable house number there is NOT A SINGLE direct surname match with the owner of the same house number in PT (0/91; 72 divergences below 0.50 similarity). Surnames present in both registers (Bring, Hlebety, Kriš(t)an, Milleg, Strauß, Schimetz/Schumetz [~] — 11 in total) occur at DIFFERENT house numbers. PUA also lists owners from neighbouring villages (Deschitz, Dragosche, Waldendorf, Leusthal) and institutions (the church of St. Vitus, a commandery, Baron Gradatz) that the PT house register does not capture; PUA house numbers end at ~69, PT at 98. Conclusion (hypothesis, [~]): PUA is an alphabetical index of PARCEL owners with its own house reference that does not equal the PT conscription numbering — the two series can only be compared by names, not by numbers.",
  caveatsSi:
    "OBA vira sta strojna (VLM) branja z [~] negotovostjo — priimki in hišne št. so lahko napačno prebrani (npr. VLM je hišne št. že večkrat normaliziral po zaporedju). Analiza je deterministična (ponovljiva: python3 scripts/pua-pt-cross.py), a njene vhodne podatke je treba pred končno presojo potrditi s človeško paleografijo. Ujemanje 0/91 (posodobljeno po P5-b) je lahko tudi posledica sistemske napake VLM pri stolpcu hišnih št.",
  caveatsEn:
    "BOTH sources are machine (VLM) readings with [~] uncertainty — surnames and house numbers may be misread (the VLM has already had to normalise house numbers by sequence several times). The analysis itself is deterministic (reproducible: python3 scripts/pua-pt-cross.py), but its inputs must be confirmed by human palaeography before a final verdict. The 0/91 result (updated after P5-b) could also stem from a systematic VLM error in the house-number column.",
  nextStepSi:
    "Naslednji koraki: (1) OPRAVLJENO (P5-b): strani 35–49 prebrane (32 novih vnosov) in analiza ponovno zagnana — rezultat zgoraj (0/91, 11 skupnih priimkov); (2) človeška paleografska preverba stolpca hišnih št. na vzorcu 10 vnosov; (3) arhivsko vprašanje za ARS: ali PUA »Haus« pomeni konskripcijsko št. hiše ali št. davčnega gnezda (Steuerhausnummer)?",
  nextStepEn:
    "Next steps: (1) DONE (P5-b): pages 35–49 read (32 new entries) and the analysis re-run — result above (0/91, 11 shared surnames); (2) human palaeographic verification of the house-number column on a sample of 10 entries; (3) archival question for ARS: does the PUA »Haus« mean the conscription house number or the tax-nest number (Steuerhausnummer)?",
};

/** P5-c: W-MOST — sklici »W.<štev>« v PT ⟷ PUA hišno številčenje (deterministično, 2026-10-08). */
export const PUA_PT_WBRIDGE: {
  date: string;
  method: string;
  status: ResearchStatus;
  artifact: string;
  counts: {
    ptRowsWithW: number;
    wRefsTotal: number;
    wDistinct: number;
    wWithPua: number;
    wNoPua: number;
    match: number;
    partial: number;
    mismatch: number;
    puaNumsNoW: number;
  };
  hypothesisSi: string;
  hypothesisEn: string;
  findingSi: string;
  findingEn: string;
  bestMatches: { w: string; sim: string; pair: string; ptOwners: string; puaNames: string }[];
  predictions: { house: string; expectedOwners: string; resolved: string }[];
  caveatsSi: string;
  caveatsEn: string;
} = {
  date: "2026-10-08",
  method:
    "Deterministični W-most (skript scripts/pua-pt-wbridge.py, brez AI klicev): 43 vrstic PT (hiše 21–40 str. 4, parcele 41–60 str. 5, hiša 76½) nosi 45 sklicev »W.<štev>« (različnih 26) — zjoinanih s PUA hišnimi št. (PUA_CONTINUATION, 101 vnosov po P5-b); primerjava VSIH imenskih žetonov (križno-žetonjsko, Levenshtein 0,72/0,50 — enaka pragova kot P5-a, ß→ss normalizacija). Izhod: research/p5/pua-pt-wbridge.json.",
  status: "REVIEW",
  artifact: "research/p5/pua-pt-wbridge.json",
  counts: {
    ptRowsWithW: 43,
    wRefsTotal: 45,
    wDistinct: 26,
    wWithPua: 25,
    wNoPua: 1,
    match: 8,
    partial: 10,
    mismatch: 7,
    puaNumsNoW: 39,
  },
  hypothesisSi:
    "HIPOTEZA [~]: sklic »W.<štev>« v PT (Protokoll stavbnih parcel — tudi pri vinogradniških parcelah 41–60 na str. 5) je hišna številka lastnika v PUA številčenju (Grundsteuerkataster), torej MOST med obema različnima številčenjema iz ugotovitve P5-a.",
  hypothesisEn:
    "HYPOTHESIS [~]: the »W.<n>« reference in PT (the building-parcel protocol — also on vineyard parcels 41–60 on p. 5) is the owner's house number in the PUA (cadastre) numbering — i.e. the BRIDGE between the two differing numbering systems found by P5-a.",
  findingSi:
    "UGOTOVITEV (posodobljeno po P5-b — register CEL): pri 25 W-sklicih z PUA protistrani se 18 (72 %) ujema z žetonsko podobnostjo ≥ 0,50 (8 MATCH ≥ 0,72: W.2 Hlebetz↔Hlebety 0,86; W.24/W.25 Brinig↔Bring 0,83; W.29 Milleg↔Millej 0,83; W.21 Jožef↔Jožeg 0,80; W.1 Mufa↔Wufa 0,75 — zamenjava M/W značilna za Kurrent; NOVA po P5-b: W.60 Schello↔Schello 1,0 — Joger/Georg isti mož [~]; W.68 Ulrich↔Ulrich 1,0 — napoved h68 POTRJENA) — proti P5-a izhodišču 0/91 po istih številkah. Most je podprt, a šumosten: 7 MISMATCH (W.26, 27, 31, 47, 61, 62, 64) vključuje prečrtano PT vrstico (W.47 Hufschmied), dvojni PUA vpis za isto št. (W.62: Kosirhan Mäda IN Georg Juttner — notranja nestabilnost PUA številčenja) in verjetne VLM bralne zmote. KOMPONENTA PT str. 6+ (hiše 61–80) sklicev W ne nosi — W-stolpec je berljiv le na str. 4–5. RAZREŠITEV NAPOVEDI (P5-b, strani 35–49): h32 DELNO V PRID — PUA p43 v88 »Urlich Georg« (hiša 32), komponenti Georg+Ulrich ujemata s PT »Greg/Piberig Ulrich« (sim 0,67 ulrich↔urlich, vrstni red zamenjan [~]); h68 POTRJENA — PUA p44 v90 »Ulrich Mida« (hiša 68), ulrich↔ulrich 1,0 MATCH; h64 ZAVRNJENA — PUA p45 v93 »Verbitzcher Mathä« (hiša 64), varbutek↔verbitzcher 0,46 — a fonetska bližina ohranja dvom [~]; h65 NEREŠENA — noben PUA vnos na str. 35–49 nima hišne št. 65 (vrzel v registru ali bralna zmota [~]). Skupaj: 2/4 napovedi v prid (1 MATCH + 1 delna), 1 zavrnjena, 1 nerešena — zaupanje v most se je dvignilo, a ne dokončno.",
  findingEn:
    "FINDING (updated after P5-b — register COMPLETE): of 25 W-references with a PUA counterpart, 18 (72 %) agree at token similarity ≥ 0.50 (8 MATCH ≥ 0.72: W.2 Hlebetz↔Hlebety 0.86; W.24/W.25 Brinig↔Bring 0.83; W.29 Milleg↔Millej 0.83; W.21 Jožef↔Jožeg 0.80; W.1 Mufa↔Wufa 0.75 — an M/W swap typical of Kurrent script; NEW after P5-b: W.60 Schello↔Schello 1.0 — Joger/Georg the same man [~]; W.68 Ulrich↔Ulrich 1.0 — prediction h68 CONFIRMED) — against the P5-a baseline of 0/91 at the same numbers. The bridge is supported but noisy: 7 MISMATCHes (W.26, 27, 31, 47, 61, 62, 64) include a struck-through PT row (W.47 Hufschmied), a double PUA entry for the same number (W.62: Kosirhan Mäda AND Georg Juttner — internal instability of PUA numbering) and likely VLM misreads. The PT component on p. 6+ (houses 61–80) carries no W references — the W column is legible only on pp. 4–5. PREDICTION RESOLUTION (P5-b, pages 35–49): h32 PARTIALLY SUPPORTED — PUA p43 e88 »Urlich Georg« (house 32), the Georg+Ulrich components match PT »Greg/Piberig Ulrich« (sim 0.67 ulrich↔urlich, order swapped [~]); h68 CONFIRMED — PUA p44 e90 »Ulrich Mida« (house 68), ulrich↔ulrich 1.0 MATCH; h64 REJECTED — PUA p45 e93 »Verbitzcher Mathä« (house 64), varbutek↔verbitzcher 0.46 — though phonetic proximity keeps a residual doubt [~]; h65 UNRESOLVED — no PUA entry on pages 35–49 carries house no. 65 (a gap in the register or a misread [~]). Overall: 2/4 predictions supported (1 MATCH + 1 partial), 1 rejected, 1 unresolved — confidence in the bridge has risen, though not definitively.",
  bestMatches: [
    { w: "W.68", sim: "1,0", pair: "ulrich ↔ ulrich", ptOwners: "Malt Ulrich (parc. 56, W.68)", puaNames: "Ulrich Mida Bauer zu Gribla (p44 v90, h68) — napoved P5-b POTRJENA" },
    { w: "W.60", sim: "1,0", pair: "schello ↔ schello", ptOwners: "Joger Schello (parc. 50, 51, 55 — W.60)", puaNames: "Schello Georg Bauer/b zu Gribla (p42 v85, h60) + Georg Rußa (p31 v61) — hiša 60 ima dva PUA lastnika [~]" },
    { w: "W.2", sim: "0,86", pair: "hlebetz ↔ hlebety", ptOwners: "Hlebetz Jan (hiša 26, W.2 · Schißing 245)", puaNames: "Hlebety Johann, Bauer hiesig zu Grüble (p11 v18, h2)" },
    { w: "W.24", sim: "0,83", pair: "brinig ↔ bring", ptOwners: "Brinig Magnus (hiša 35, W.24 · Schißing 54/64)", puaNames: "Bring Migan/Michael Bauern hiesig Grübln (p4 v3, h24)" },
    { w: "W.25", sim: "0,83", pair: "brinig ↔ bring", ptOwners: "Brinig Miklo (hiša 39, W.25 · Schißing 39)", puaNames: "Bring Miß/Martin Bauern hiesig Grübln (p4 v4, h25)" },
    { w: "W.29", sim: "0,83", pair: "milleg ↔ millej", ptOwners: "Milleg Hans (hiša 34, W.29 · Schißing 46 / Walle 8)", puaNames: "Millej (p26 v52, h29)" },
    { w: "W.21", sim: "0,80", pair: "jozef ↔ jozeg", ptOwners: "Jožef Miko (hiša 27, W.21 · Schißing 88)", puaNames: "Jožeg Muhč Bauer houlgübl (p29 v57, h21)" },
    { w: "W.1", sim: "0,75", pair: "mufa ↔ wufa", ptOwners: "Štunidat Mufa (hiši 24/25, W.1 · Apnind 28 / Schißing 89)", puaNames: "Hölloschitsch Wufa Luina hau Dragosche (p3 v1, h1) — ista oseba, dve strojni brani (M↔W)" },
  ],
  predictions: [
    { house: "PUA h32", expectedOwners: "Greg Ulrich / Piberig Ulrich (PT: parc. 54, 57, 58 — W.32) — RAZREŠENO P5-b: PUA p43 v88 »Urlich Georg« (h32), PARTIAL 0,67 v prid [~]", resolved: "DELNO V PRID" },
    { house: "PUA h64", expectedOwners: "Varbutek Mufa (hiša 33, W.64 · Schißing 67) / Jörg Georg (parc. 41, W.64) — RAZREŠENO P5-b: PUA p45 v93 »Verbitzcher Mathä« (h64), MISMATCH 0,46 [~]", resolved: "ZAVRNJENO" },
    { house: "PUA h65", expectedOwners: "Bring Marko (hiša 32, W.65 · Schißing 90) / Glan Simonz (parc. 60, W.65) — RAZREŠENO P5-b: NOBEN PUA vnos s h65 na str. 35–49 (vrzel [~])", resolved: "NEREŠENO" },
    { house: "PUA h68", expectedOwners: "Malt Ulrich (parc. 56, W.68) — RAZREŠENO P5-b: PUA p44 v90 »Ulrich Mida« (h68), MATCH 1,0", resolved: "POTRJENO" },
  ],
  caveatsSi:
    "Vsa vhodna branja so strojna (VLM, status REVIEW) — W.47 je prečrtana PT vrstica (primerjava brez pomena), W.62 ima dva različna PUA lastnika (branje št. ali časovni zamik), križno-žetonjska primerjava lahko ujame tudi ime↔ime (ne priimek↔priimek), kar navidezno poveča podobnost. Analiza je deterministična in ponovljiva (python3 scripts/pua-pt-wbridge.py). Strani 35–49 so prebrane (P5-b) in napovedi razrešene: h68 POTRJENA (MATCH 1,0), h32 delno v prid (PARTIAL 0,67), h64 zavrnjena (0,46 — fonetska bližina [~]), h65 brez protistrani (vrzel [~]). Hipoteza W = PUA številčenje ostaja [~] do paleografske potrditve — vendar se je po razrešitvi 2/4 napovedi zaupanje v most dvignilo.",
  caveatsEn:
    "All input readings are machine-based (VLM, status REVIEW) — W.47 is a struck-through PT row (comparison meaningless), W.62 has two different PUA owners (number misread or temporal shift), and the cross-token comparison may match given-name↔given-name (not surname↔surname), inflating similarity. The analysis is deterministic and reproducible (python3 scripts/pua-pt-wbridge.py). Pages 35–49 have been read (P5-b) and the predictions resolved: h68 CONFIRMED (MATCH 1.0), h32 partially supported (PARTIAL 0.67), h64 rejected (0.46 — phonetic proximity [~]), h65 without counterpart (a register gap [~]). The W = PUA-numbering hypothesis remains [~] until palaeographic confirmation — though with 2/4 predictions resolved in its favour, confidence in the bridge has risen.",
};

/** PT — strokovni pregled obstoječega registra (issue #17, 2026-10-08). */
export const PT_REVIEW_2026: {
  source: string;
  status: ResearchStatus;
  reviewedRows: number;
  summary: { confirmed: number; corrections: number; additionalRows: number; repoOnly: number; illegible: number };
  structuralFindingSi: string;
  structuralFindingEn: string;
  corrections: { houseNo: string; repoOwner: string; vlmReading: string; confidence: string }[];
  additionalRows: { houseNo: string; note: string }[];
  decisionSi: string;
  decisionEn: string;
} = {
  source: "N083PT str. 1–8 proti src/data/atlas/houses.ts (101 vrstic registra + 4 dodatne rokopisne) — research/issue17/PT-review.json",
  status: "REVIEW",
  reviewedRows: 105,
  summary: { confirmed: 81, corrections: 15, additionalRows: 4, repoOnly: 0, illegible: 5 },
  structuralFindingSi:
    "STRUKTURNA (visoka zaupanja, 3× zoom-verificirano): vrstice registra za hiše 36–41 so zamaknjene za +1 — rokopis ima prečrtan dvojni vpis »34«, stran se konča pri hiši 40 (str. 5 se začne s 41, druga »41« ni mogoča). Register hiša »41« (Bring Mufa, W.23/Wiese 6) v rokopisu ustreza hiši 40. Popravek hišnih št. 36→35 … 41→40 čaka paleografski potrditev; VSEBINA vrstic (parcelni sklici) se potrjeno ujema.",
  structuralFindingEn:
    "STRUCTURAL (high confidence, 3× zoom-verified): register rows for houses 36–41 are shifted by +1 — the manuscript carries a struck duplicate »34«, the page ends at house 40 (p. 5 starts at 41, a second »41« is impossible). The register's house »41« (Bring Mufa, W.23/Wiese 6) corresponds to manuscript house 40. Renumbering 36→35 … 41→40 awaits palaeographic confirmation; the row CONTENT (parcel refs) matches.",
  corrections: [
    { houseNo: "1", repoOwner: "Peth (H.)", vlmReading: "H. Veith [~] (enako hiši 2)", confidence: "srednja — 2 klica" },
    { houseNo: "36 (repo)", vlmReading: "Bring Majzel — zamik št., glej strukturno ugotovitev", repoOwner: "Bring Majzel (hiša 36)", confidence: "visoka" },
    { houseNo: "39 (repo 40)", repoOwner: "Tonig Miko", vlmReading: "Brinig/Bring Misko [~]", confidence: "srednja — 3 klici (parcele W.25·Schißing 39 se natanko ujemajo)" },
    { houseNo: "76, 79", repoOwner: "Stenopfs Georg", vlmReading: "Strauß [~] Georg", confidence: "srednja — 3 klici (W45, površini 20/100 točni)" },
    { houseNo: "81–84", repoOwner: "Groy Hanž", vlmReading: "Strauß Georg [~] (priimek IN ime se razlikujeta)", confidence: "nizka — 2 klica" },
    { houseNo: "96", repoOwner: "Groy Khunz", vlmReading: "Sh-… [~] Georg", confidence: "nizka" },
    { houseNo: "98", repoOwner: "Zollnerd A. M.", vlmReading: "institucija: Zollamt [~] + ärarial [~]; opomba »verzahlt zum Hauptmagazin v[on] 1826« [~]", confidence: "srednja" },
  ],
  additionalRows: [
    { houseNo: "7 (brez ½)", note: "Lebring Mäfa/Leudig Martin [~], Nº 14, 84 kv. kl — vrstica v rokopisu, ki je ni v registru" },
    { houseNo: "71½", note: "PREČRTANO (rdeče); lastnik nestabilen [~]; 87/187 [~]" },
    { houseNo: "76½", note: "PREČRTANO (rdeče); Hufschmied [~]/Cholatschar Markus [~], W.47, 14 — vsebina se prekriva z repo hišo 77 (možen zamik 77/78)" },
    { houseNo: "99", note: "oštevilčena vrstica s PRAZNO lastniško celico — verjetno zaključna/vrsta vsote strani, ne hiša" },
  ],
  decisionSi:
    "ODLOČITEV (issue #17): register ATLAS_HOUSES je ostal nespremenjen do paleografske preverbe. P3 (2026-10-08, 2. krog VLM, črka-za-črko): popravki z 2-kratno konvergenco so APLICIRANI (15 lastniških popravkov, renumeracija str. 4 36–41→35–40, 4 dodane vrstice 7/71½/76½/99); statusi ostajajo REVIEW — dokončna potrditev je človeška paleografija. Neodvisna potrditev vsebine: vsota PT »…14/889« se natanko ujema s PV »Bau Parzellen 4 J 889 Kl«.",
  decisionEn:
    "DECISION (issue #17): the ATLAS_HOUSES register remained unchanged until palaeographic verification. P3 (2026-10-08, 2nd VLM pass, letter-by-letter): corrections with 2-pass convergence APPLIED (15 owner corrections, the p. 4 renumbering 36–41→35–40, 4 added rows 7/71½/76½/99); statuses stay REVIEW — final confirmation is human palaeography. Independent content validation: the PT total »…14/889« matches PV »Bau Parzellen 4 J 889 Kl« exactly.",
};

/** P3 — PALEOGRAFSKA PREVERBA PT, 2. KROG (2026-10-08): apliciranje popravkov registra. */
export const PT_PALEOGRAPHY_P3: {
  date: string;
  methodSi: string;
  methodEn: string;
  vlmCalls: number;
  pass2Rows: { houseNo: string; before: string; pass1: string; pass2: string; verdict: string }[];
  appliedSi: string;
  appliedEn: string;
  integritySi: string;
  integrityEn: string;
} = {
  date: "2026-10-08",
  methodSi:
    "2. krog VLM branja PT po priporočilu 17-z: SVEŽI izrezi (pasovi 1,4–1,8× povečave, različen okvir od 1. kroga), vloga »paleograf specialist za avstrijsko Kurent pisavo 1820ih«, prompti za analizo ČRKA ZA ČRKO (začetnica, končnica, ligature) + alternativna branja z zaupanjem. Popravek se aplicira SAMO, če se 1. in 2. krog konvergirata (istim priimkom ali strukturno lastnostjo).",
  methodEn:
    "2nd pass VLM reading of PT per the 17-z recommendation: FRESH crops (1.4–1.8× bands, framing different from pass 1), the role of a »palaeographer specialising in Austrian Kurrent script of the 1820s«, letter-by-letter prompts (initial letter, ending, ligatures) + alternative readings with confidence. A correction is applied ONLY where pass 1 and pass 2 converge (same surname or structural property).",
  vlmCalls: 9,
  pass2Rows: [
    { houseNo: "1", before: "Peth (H.)", pass1: "St. Veith / H. Veith [~] (2 branji)", pass2: "Veith (H.) — V ne P, končnica -th [črka-za-črko]", verdict: "POPRAVEK APLICIRAN (3× konvergenca)" },
    { houseNo: "7", before: "— (vrstica manjkala)", pass1: "Lebring Mäfa / Leudig Martin [~]", pass2: "Lebing Mädl. [~]", verdict: "DODANA VRSTICA (L-priimek + Mädl. 2×)" },
    { houseNo: "7½", before: "Podlesy Marija", pass1: "Lebring mäusg / Bödig mündl. [~]", pass2: "Bödig mündl. [~]", verdict: "POPRAVEK APLICIRAN (Bödig 2×)" },
    { houseNo: "8", before: "Leskovec Matija", pass1: "Lebring Mäfa / Leudig Martin [~]", pass2: "Lebing Mädl. [~]", verdict: "POPRAVEK APLICIRAN" },
    { houseNo: "8½", before: "Leskovec Matija", pass1: "[?] mäusg / Bödig mündl. [~]", pass2: "Bödig mündl. [~]", verdict: "POPRAVEK APLICIRAN" },
    { houseNo: "20", before: "Vičak Matija", pass1: "Kruišter Mäfa / Christan Muffn [~]", pass2: "Kraihan/Krischan Mäfa/Mädl [~] (K, ne V)", verdict: "POPRAVEK APLICIRAN (K 2×; točna oblika odprta)" },
    { houseNo: "34", before: "Milleg Stane", pass1: "Milleg Hanne [~]", pass2: "Milleg/Hanne — prva 34 [~]", verdict: "IME POSODOBLJENO (Hans)" },
    { houseNo: "34 (dvojnica)", before: "Milleg Stane (št. 35)", pass1: "prečrtan dvojni 34 [3× zoom]", pass2: "PREČRTAN DVOJNI 34, Milleg Hanne — zadnja št. str. 4 je 40 [4×]", verdict: "RENUMERACIJA APLICIRANA (35→34-dvojnica)" },
    { houseNo: "35–40", before: "št. 36–41 (Bring Majzel/Milleg Jan/Bring Mufa×2/Tonig Miko/Bring Mufa)", pass1: "Brinig Migurl / Milley Han / Brinig Malga ×3 / Brinig Misko", pass2: "Brinig Magnus / Milleg Hans / Brinig Malfa ×3 / Brinig Miklo (Niklo?)", verdict: "RENUMERACIJA + POPRAVKI APLICIRANI (Brinig 2×, stran se konča s 40)" },
    { houseNo: "71½", before: "— (vrstica manjkala)", pass1: "prečrtana [~]", pass2: "Stettner [~], prečrtana", verdict: "DODANA VRSTICA (prečrtana)" },
    { houseNo: "76", before: "Stenopfs Georg", pass1: "Strauß Georg [~]", pass2: "Strauß Georg (ali Gregor) [~]", verdict: "POPRAVEK APLICIRAN (Strauß 2×)" },
    { houseNo: "76½", before: "— (vrstica manjkala)", pass1: "Hufschmied [~] prečrtana", pass2: "Hufschmied, RDEČE črnilo, prečrtana", verdict: "DODANA VRSTICA (rdeči vpis)" },
    { houseNo: "79", before: "Stenopfs Georg", pass1: "Strauß Georg [~], prečrtana", pass2: "Strauß Georg, vrstica rdeče prečrtana", verdict: "POPRAVEK APLICIRAN + PREČRTANOST DOKUMENTIRANA" },
    { houseNo: "81–84", before: "Groy Hanž ×4", pass1: "Strauß Georg [~] ×4", pass2: "Strauß Georg [Groy] [~] — ime Georg, ne Hanž; Abgerissen/Hof gültfällig", verdict: "POPRAVEK APLICIRAN (Strauß 2×, Groy kot drugi zapis)" },
    { houseNo: "90", before: "Kuncelj Miha", pass1: "Kavalar [~Milo] / Bumiller Marlo [~]", pass2: "Ihmeyer Georg [~]", verdict: "OSTAJA ILLEGIBLE (3 divergentna branja — priimek Kuncelj se ne potrdi)" },
    { houseNo: "96", before: "Groy Khunz", pass1: "Shimerz / Ihmeyer Georg [~]", pass2: "Ihmeyer Manko/Mankl [~]", verdict: "POPRAVEK APLICIRAN (Ihmeyer 2×)" },
    { houseNo: "98", before: "Zollnerd A. M.", pass1: "Zollamt [~] + ärarial [~] + Hauptmagazin 1826 [~]", pass2: "A. A. Zollamt + ärarial + »Hauptmagazin von 1826«", verdict: "POPRAVEK APLICIRAN (institucija 2×; 1826, ne 1860)" },
    { houseNo: "99", before: "— (vrstica manjkala)", pass1: "oštevilčena, PRAZNA lastniška celica", pass2: "prazna vrstica 99 [2×]", verdict: "DODANA VRSTICA (prazna, zaključek strani)" },
  ],
  appliedSi:
    "APLICIRANO v houses.ts: (1) renumeracija str. 4 — prečrtana dvojnica 34 je zdaj lastna vrstica »34 (prečrtana dvojnica)«, hiše 35–40 prestavljene iz 36–41, hiša 41 NE obstaja več (str. 5 se začne s parcelo 41); (2) 15 lastniških popravkov z 2-kratno konvergenco (Veith 1, Lebing 7/8, Bödig 7½/8½, K-priimek 20, Brinig 35–40, Strauß 76/79/81–84, Ihmeyer 96, Zollamt 98); (3) 4 dodane vrstice (7, 71½ Stettner, 76½ Hufschmied, 99 prazna). Register: 105 vrstic (84 hišnih + 21 parcelnih). Vsi statusi ostajajo REVIEW.",
  appliedEn:
    "APPLIED in houses.ts: (1) the p. 4 renumbering — the struck duplicate 34 is now its own row »34 (struck duplicate)«, houses 35–40 shifted from 36–41, house 41 NO LONGER exists (p. 5 starts with parcel 41); (2) 15 owner corrections on 2-pass convergence (Veith 1, Lebing 7/8, Bödig 7½/8½, K-surname 20, Brinig 35–40, Strauß 76/79/81–84, Ihmeyer 96, Zollamt 98); (3) 4 added rows (7, 71½ Stettner, 76½ Hufschmied, 99 empty). Register: 105 rows (84 house + 21 parcel). All statuses stay REVIEW.",
  integritySi:
    "Nadzor nič-zgube: 101 starih vrstic je še vedno 101 (prečrtana dvojnica 34 ostaja kot vrstica, ne brisanje) + 4 nove = 105. Vsebina (parcelni sklici W./Schißing/Apnind) se ni spremenila — samo hišne št. in lastniki. Vsota str. 8 (889 kl) ostaja neodvisna kontrola. PUA str. 11 (4 vnosi, črka H) dodana v PUA_CONTINUATION.",
  integrityEn:
    "Zero-loss control: the 101 original rows remain 101 (the struck duplicate 34 stays as a row, not a deletion) + 4 new = 105. The content (parcel references W./Schißing/Apnind) is unchanged — only house numbers and owners. The p. 8 total (889 kl) remains an independent check. PUA p. 11 (4 entries, letter H) added in PUA_CONTINUATION.",
};

/** USTNA ZGODOVINA — raziskovalni protokol (issue #17 #6; intervjuji ostanejo prazni). */
export const ORAL_HISTORY_PROTOCOL: {
  version: string;
  status: ResearchStatus;
  scopeSi: string;
  scopeEn: string;
  stages: { no: number; nameSi: string; nameEn: string; descSi: string; descEn: string }[];
  requiredFields: string[];
  consentSi: string;
  consentEn: string;
  rightsSi: string;
  rightsEn: string;
  rulesSi: string[];
  rulesEn: string[];
} = {
  version: "1.0 (issue #17)",
  status: "TO_COLLECT",
  scopeSi:
    "Tematski okvir iz obstoječega modela (ORAL_TOPICS): Pasuljada, tamburaši, lokalni dogodki, šolski spomini, pričevanja domačinov — povezani na muzejske zapise (MVG-026 šola, MVG-026 tambura, dogodki 1526–2026).",
  scopeEn:
    "Thematic frame from the existing model (ORAL_TOPICS): the bean feast, tamburica players, local events, school memories, villagers' testimonies — linked to museum records (MVG-026 school, MVG-026 tambura, events 1526–2026).",
  stages: [
    { no: 1, nameSi: "Priprava", nameEn: "Preparation", descSi: "Identifikacija pripovedovalcev (imenski seznam domačinov, šolski spomini, rodbine iz PT/PUA 1825); kontakt prek krajevne skupnosti Griblje / OŠ Loka Črnomelj; seznam vprašanj po temah.", descEn: "Identify narrators (named villagers, school memories, PT/PUA 1825 families); contact via the Griblje local community / OŠ Loka Črnomelj; question lists per topic." },
    { no: 2, nameSi: "Snemanje", nameEn: "Recording", descSi: "Audio (minimalno) ali video; GPS lega; datum; trajanje; oprema: diktafon + rezervna mikrofonacija; soglasje PODPISANO pred snemanjem.", descEn: "Audio (minimum) or video; GPS position; date; duration; equipment: recorder + backup microphone; consent SIGNED before recording." },
    { no: 3, nameSi: "Obdelava", nameEn: "Processing", descSi: "Prepis (transkript) z datumom in različico; časovni žigi na tematske skoke; anonimizacija tretjih oseb po potrebi; jezikovna različica (narečje ohranjeno, standardni slovenski prevod).", descEn: "Transcript with date and version; timestamps at topic jumps; third-party anonymisation where needed; language variant (dialect preserved, standard Slovenian rendering)." },
    { no: 4, nameSi: "Vpis v zbirko", nameEn: "Ingest", descSi: "Polnjenje OralInterview modela (narrator, date, location, interviewer, consent, media, transcript, relatedMuseumRefs, rights, status); povezava na MVG zapise; avdio shranjen v /audio z imenom mvg-oral-<id>.", descEn: "Fill the OralInterview model (narrator, date, location, interviewer, consent, media, transcript, relatedMuseumRefs, rights, status); link to MVG records; audio stored in /audio as mvg-oral-<id>." },
  ],
  requiredFields: [
    "id (mvg-oral-NNN)",
    "narratorSi/En (ime ali anonimizirano)",
    "date (YYYY-MM-DD)",
    "locationSi/En",
    "interviewerSi/En",
    "consent { given, scopeSi/En } — obvezno podpisano soglasje",
    "media { audio, video } — pot do datoteke",
    "transcript { textSi, textEn, version } — ob popisanem intervjuju",
    "relatedMuseumRefs [] — povezave na MVG zapise",
    "rightsSi/En — licence in omejitve uporabe",
    "status — VERIFIED/DOCUMENTED/REVIEW po Zakonu o varstvu osebnih podatkov",
  ],
  consentSi:
    "Soglasje (obrazec): pripovedovalec potrdi (1) snemanje, (2) hrambo posnetka v muzejski zbirki, (3) objavo prepisa/sposnetka na spletu (neobvezno), (4) trajanje in obseg (časovno neomejeno / do preklica). Poseben dogovor za ranljive osebe in osebne podatke tretjih.",
  consentEn:
    "Consent (form): the narrator confirms (1) the recording, (2) storage in the museum collection, (3) online publication of the transcript/recording (optional), (4) duration and scope (unlimited / until revoked). Special handling for vulnerable persons and third-party personal data.",
  rightsSi: "Avtorske pravice pripovedovalca (ustna dela); muzej pridobi neizključno pravico uporabe z atribucijo; posnetki in prepisi se objavljajo le s soglasjem; ZVOP-1 (varstvo osebnih podatkov) upoštevan.",
  rightsEn: "Copyright remains with the narrator (oral works); the museum gains a non-exclusive right of use with attribution; recordings and transcripts are published only with consent; personal-data protection (ZVOP-1) observed.",
  rulesSi: [
    "NE izmišljuj intervjujev — ORAL_INTERVIEWS ostane prazen, dokler ni posnetega posnetka.",
    "Vsak vnos zahteva podpisano soglasje (fizični ali digitalni podpis).",
    "Prepis ohranja narečje; standardna slovenščina v ločenem polju.",
    "Status VERIFIED samo za preverjene identitete/datume; sicer REVIEW.",
    "Vsak intervju povežemo na muzejski zapis (relatedMuseumRefs) — brez povezave ni vnosa.",
  ],
  rulesEn: [
    "Do NOT invent interviews — ORAL_INTERVIEWS stays empty until a recording exists.",
    "Every entry requires a signed consent (physical or digital signature).",
    "The transcript preserves the dialect; standard Slovenian in a separate field.",
    "VERIFIED only for verified identities/dates; otherwise REVIEW.",
    "Every interview links to a museum record (relatedMuseumRefs) — no link, no entry.",
  ],
};

/** WEB VERIFIKACIJE (issue #17 #2 #4 #5 #7 #8) — 2026-10-08. */
export interface WebVerification {
  target: string;
  status: ResearchStatus;
  url: string;
  findingSi: string;
}

export const WEB_VERIFICATIONS: WebVerification[] = [
  {
    target: "SEM F0000212 — javni zapis",
    status: "VERIFIED",
    url: "https://www.etno-muzej.si/sl/digitalne-zbirke/zbirka-starih-fotografij/f0000212",
    findingSi: "HTTP 200: »Enonadstropna hiša na pero, rojstna hiša dr. Nika Županiča«, Zbirka starih fotografij, Griblje; slika javna. Fotograf/datum v zapisu PRAZNA — pisati SEM. (evd.si = domena naprodaj, NE baza SEM.)",
  },
  {
    target: "Gaspari — primarni predmet za Belo krajino",
    status: "DOCUMENTED",
    url: "https://www.etno-muzej.si",
    findingSi: "Za Griblje: nič. Dokumentiran kandidat: »Belokranjska ohcet« (1924, olje/platno, hrani SEM — RTV SLO/Dnevnik/Družina/razstava SEM 2024). Javne inventarne št. NI → ostaja TO_COLLECT.",
  },
  {
    target: "SI AS 749/3/8/12 (1851–1853) — VAČ",
    status: "VERIFIED",
    url: "https://vac.sjas.gov.si/vac/search/details?id=4971617",
    findingSi: "VAČ zapis potrjen (curl -k zaradi SSL): izpisek za davčne občine Vinji Vrh, Kot, Griblje, Kaltersberg, Loka, Petrova vas, Krasinec (serija /3/8 Zemljiška odveza). Javno dostopno, NI digitalizirano — vpogled v čitalnici ARS. Pregledana celotna serija /3/8 (17 enot): edina Griblje-enota je /3/8/12. www.e-ars.si: DNS mrtev.",
  },
  {
    target: "EŠD 2122 / 11118 / 10094 — Register nepremične kulturne dediščine",
    status: "VERIFIED",
    url: "https://geohub.gov.si/ghapp/giskd/?&find=2122",
    findingSi: "EŠD 2122 = Griblje — cerkev sv. Vida (spomenik lokalnega pomena; GisKD find=2122 deluje). EŠD 10094 = Griblje — najdišče ob Kolpi (registrirana, neolitik–rima). EŠD 11118 = Podzemelj-Kučar (občina Metlika) — NI Griblje; podatek v repu JE ŽE PRAVILEN (sources.ts razlikuje 11118 od 10094). Uradni javni vir: podatki.gov.si (CKAN, Register nepremične kulturne dediščine, CSV, zadnja posodobitev 2023-05-04).",
  },
  {
    target: "Šolski arhiv VAČ 4118864 + 747512",
    status: "VERIFIED",
    url: "https://vac.sjas.gov.si/vac/search/details?id=4118864",
    findingSi: "4118864: SI_ZAL_ČRN/0001/001/00012, Državna osnovna šola Griblje 1929–1941 — POTRJENO, DIGITALIZIRANO, javno. 747512: SI_ZAL_NME/0234/003/096, OŠ Črnomelj podružnica Griblje 1970–1982 — potrjeno, javno. Šolska kronika Griblje: javnega dokaza o hranilniku NI (ostaja REVIEW — verjetno pri OŠ Loka Črnomelj).",
  },
  {
    target: "1812 — izvirniki zemljevida",
    status: "VERIFIED",
    url: "https://commons.wikimedia.org/wiki/File:Provinces_Illyriennes_Servie_et_Bosnie_1812.jpg",
    findingSi: "Commons: datoteka obstaja (1812, Giraldon, javna last, 8297 × 6080 px). dlib URN:NBN:SI:doc-F4NO0ZFV (ZRC SAZU 2012) potrjen prek COBISS/WorldCat (dlib s sandboxa timeout). Georeferenca IZVEDENA (P6, 2026-10-08): OCR → LSQ afina/kvadratna, Griblje px (2499,2286) ± 10 km [~] REVIEW; koroborirana na drugem skenu istega lista (P7: IA 7636×5936, sporazumenje 5,6 km).",
  },
  {
    target: "matice.si — katastrski skeni",
    status: "NOT_FOUND",
    url: "https://matice.si",
    findingSi: "DNS se ne razreši; iskalniki takega vira ne poznajo. Skeni franciscejskega katastra za Griblje ostajajo na VAČ (N083, javno) — to je potrjena pot.",
  },
  {
    target: "eZKN — georeferenčiran zgodovinski kataster (GisKD/GeoHub)",
    status: "VERIFIED",
    url: "https://geohub.gov.si/ghapp/ezkn/",
    findingSi: "Javni georeferenciran pregledovalnik ZKN GURS + indikacijski katastrski zemljevidi franciscejskega/reambulančnega katastra ARS (JPG nižje ločljivosti; ime »GeoZgodovina« pod tem imenom NE obstaja — pravi vir je eZKN). Uradna javna georeferenca katastrskih map — ključ za prostorsko prekrivanje 1825↔danes.",
  },
  {
    target: "N083 — javna dostopnost skenov (OPSI)",
    status: "VERIFIED",
    url: "https://vac.sjas.gov.si/vac/search/details?id=373414",
    findingSi: "Celoten SI AS 176/N83 Griblje (grafični listi A01–A05 z »Digitalni posnetek« + spisovne enote PG/PR/PS/PT/PUA/PV/PZ) je javno dostopen v VAČ — OPSI zbirka »Digitalizirano arhivsko gradivo starih katastrov«. Tehnična pot javna; visoke resolucije v čitalnici ARS.",
  },
  {
    target: "CLSS — 3D LiDAR (novi cikel 2023–2025)",
    status: "VERIFIED",
    url: "https://clss.si/?center=522667||47571&srid=3794&scale=2000&pitch=45&z=1200",
    findingSi: "HTTP 200; 2D+3D pregledovalnik, cikel 2023–2025 (nadomesti LiDAR 2014–15, ki bloka b_16 ni zajemal); kvadrantni prenos GKOT/DMR/DMP (.laz) + nDMP/PAS (.tif); uradni globoki link za Griblje (center=522667||47571, EPSG:3794).",
  },
  {
    target: "OSM — dejanski podatki za Griblje",
    status: "VERIFIED",
    url: "https://api.openstreetmap.org/api/0.6/map?bbox=15.275,45.555,15.305,45.582",
    findingSi: "Direkten OSM API (Overpass blokiran s sandboxa — zamenjana pot, dokumentirano): 449 stavbnih way v k.o. bbox (~301 v jedru vasi; 55 z hišnimi št. — 37 različnih št. 23–85, ulici Griblje/Dragoši); cerkev Sv. Vid 45,56768/15,29039 (~12 m od EŠD 2122); vas node 45,57246/15,29257, population 356, wikidata Q2531566, name:de Grüble. Primanjkljaj: OSM nima hišnih št. kot zanesljivega ključa za hiše 1825; šole NI v OSM.",
  },
  {
    target: "ARSO DOF/DMR storitvi",
    status: "VERIFIED",
    url: "https://gis.arso.gov.si/arcgis/rest/services/DOF_D96TM_2022_2023_2024/MapServer",
    findingSi: "DOF 2022–2024: 200, DOF_25 = 25 cm, 17 LOD, EPSG:3794 (dokazano z izvozom 300 m pri cerkvi). DMR ImageServer: 200, 1 m F32, izvoz na cerkvi (D96TM x=522.667 y=47.571) deluje.",
  },
];

/** MATRIKA issue #17 — pred/zares (vse številke iz datotek). */
export interface Issue17MatrixRow {
  areaSi: string;
  areaEn: string;
  beforeSi: string;
  afterSi: string;
  delta: string;
}

export const ISSUE17_MATRIX: Issue17MatrixRow[] = [
  { areaSi: "PT", areaEn: "PT (building protocol)", beforeSi: "80 vrstic, REVIEW", afterSi: "101 vrstic registra + pregled: 81/105 verdiktov potrjenih, 15 popravkov [~], 4 prečrtane vrstice, strukturni zamik 36–41", delta: "+pregled (register nespremenjen)" },
  { areaSi: "PUA", areaEn: "PUA (owners register)", beforeSi: "2 strani / 21 lastnikov", afterSi: "10 strani / 39 vnosov (18 novih: Bring, Dragosch, Fillah, Brulla, Decklitsch, Abfalterer, Commenda)", delta: "+8 strani, +18 vnosov" },
  { areaSi: "PS", areaEn: "PS (parcel register)", beforeSi: "0 prebranih (20 vrstic model)", afterSi: "struktura + rekapitulacija: 102 stavbna mesta / 2505 parcel / 2607 skupaj; 12 vzorčnih vrstic", delta: "+9 strani, +12 vrstic, + kontrolna vsota" },
  { areaSi: "PR", areaEn: "PR (boundary description)", beforeSi: "0 (TO_COLLECT)", afterSi: "4/4 strani: mere 1028×1884 kl, točke 1–10 [~], sosedi, 8. 4. 1825", delta: "+4 strani (celota)" },
  { areaSi: "PZ", areaEn: "PZ (valuation elaborate)", beforeSi: "0 (TO_COLLECT)", afterSi: "10 vzorčenih strani: 441 prebivalcev, 2294 joch, cenilna veriga (Bau-Area 7 fl 35 kr/joch), 28. 7. 1825", delta: "+10 strani, +ekonomski profil" },
  { areaSi: "PG", areaEn: "PG (indication sketch)", beforeSi: "0 (TO_COLLECT)", afterSi: "1/1: skica z mejo, Kolpo, ~15–19 točk, sosedi; hiše niso videti (negativno)", delta: "+1 stran" },
  { areaSi: "PV", areaEn: "PV (land use)", beforeSi: "0 (TO_COLLECT)", afterSi: "1/1 v celoti: 10 izpolnjenih kultur (20 vrstic), skupaj 1221 j ≈ 703 ha, gozd PRAZEN (anomalija)", delta: "+1 stran, +10 vrstic" },
  { areaSi: "1812", areaEn: "1812 map", beforeSi: "dokumentirano, georeferenca TO_COLLECT", afterSi: "izvedena strojna georeferenca [~] REVIEW: 15 OCR kontrolnih točk, afina+kvadratna (soglasje ±2 px), merilo 126×124 m/px, Griblje px (2499,2286) ± 10 km; izrez v zbirki MVG-092; P7 koroboracija na 2. skenu (IA): registracija ORB+RANSAC (RMS 3,9 px) + neodvisen 12-točkovni model → sporazumenje 5,6 km", delta: "georeferenca izvedena [~] + koroborirana" },
  { areaSi: "1851–53", areaEn: "1851–53 (SI AS 749)", beforeSi: "odprto (VAČ 4971617, NOT_DIGITIZED)", afterSi: "enota potrjena + edina Griblje-enota v seriji /3/8 (17 enot pregledanih); ni digitalizirana", delta: "status pošteno DOCUMENTED" },
  { areaSi: "F0000212", areaEn: "F0000212 (SEM photo)", beforeSi: "delna provenanca (TO_COLLECT)", afterSi: "javni zapis VERIFIED (URL + slika); fotograf/datum: polji prazni — pisati SEM (TO_COLLECT)", delta: "+VERIFIED vir" },
  { areaSi: "Gaspari", areaEn: "Gaspari", beforeSi: "sekundarna omemba", afterSi: "za Griblje nič; dokumentiran kandidat za Belo krajino (Belokranjska ohcet 1924, SEM) brez inventarne št.", delta: "ostaja TO_COLLECT" },
  { areaSi: "šola", areaEn: "school", beforeSi: "2 enoti DOCUMENTED", afterSi: "obe enoti VAČ POTRJENI (4118864 celo digitalizirana!); kronika: hranilnik javno neznan (REVIEW)", delta: "+potrditev" },
  { areaSi: "ustna zgodovina", areaEn: "oral history", beforeSi: "prazen model", afterSi: "protokol v1.0 (4 faze, 11 obveznih polj, soglasje, pravice, 5 pravil); intervjuji ostajajo PRAZNI", delta: "+protokol, +0 intervjujev" },
  { areaSi: "arheologija/EŠD", areaEn: "archaeology/EŠD", beforeSi: "2122/11118/10094 v virih", afterSi: "EŠD potrjeni v uradnem registru (GisKD find=2122 deluje); 11118=Podzemelj (podatek v repu ŽE PRAVILEN)", delta: "+uradni URL-ji" },
  { areaSi: "javni geodata", areaEn: "public geodata", beforeSi: "8 virov, 3 VERIFIED", afterSi: "+eZKN (georef. kataster ARS), CLSS cikel 2023–25 z globokim linkom, OSM dejanski podatki (449 stavb), ARSO izvozi dokazani; LiDAR 2014-15 b_16 ostaja NOT_FOUND", delta: "+4 virov/dokazov" },
];

/** Skupni revizijski zapis issue #17 (strojno berljiv). */
export const ISSUE17_AUDIT = {
  issue: 17,
  closedAt: "2026-10-08",
  methodSi:
    "VLM branje skenov N083 (PDF→PNG, pdftoppm 200–300 dpi; skeni javno dostopni prek VAČ); vsako pomembno številko ≥2 neodvisna klica; cross-check PT↔PUA↔PS↔PV↔PR (mere, vsote, Bau-Parzellen 889 kl); web verifikacije virov (curl HTTP + iskanje); OSM podatki prek direktnega API. Surovi izpisi: research/issue17/*.json.",
  methodEn:
    "VLM reading of the N083 scans (PDF→PNG, pdftoppm 200–300 dpi; scans publicly accessible via VAČ); every key number read ≥2 independent calls; cross-checks PT↔PUA↔PS↔PV↔PR (dimensions, totals, Bau-Parzellen 889 kl); web verifications of sources (curl HTTP + search); OSM data via the direct API. Raw outputs: research/issue17/*.json.",
  vlmCallsTotal: 145,
  seriesRead: {
    PR: "4/4 strani (REVIEW)",
    PG: "1/1 stran (REVIEW)",
    PV: "1/1 stran, 10 izpolnjenih vrstic od 20 (REVIEW)",
    PS: "9 strani vzorčeno + rekapitulacija 102/2505/2607 (REVIEW)",
    PUA: "10/49 strani, 38 vrstic (REVIEW)",
    PZ: "10 strani vzorčeno, ekonomski profil (REVIEW)",
    PT: "8/8 pregledano proti registru: 81/101 potrjeno, 15 popravkov (REVIEW)",
  },
  stillOpenSi:
    "ODPRTO (pošteno): PUA strani 11–49; PS poln prepis (kontrola 2607); PZ sredina (str. 4–67 — cenilni razredi kultur); paleografska potrditev Vseh strojnih branj; georeferenca 1812; digitalizacija SI AS 749; metapodatki F0000212 (SEM); Gasparijeva inventarna št.; hranilnik šolske kronike; prvi posneti intervjuji.",
  stillOpenEn:
    "STILL OPEN (honest): PUA pages 11–49; full PS transcription (checksum 2607); PZ middle (pp. 4–67 — culture class values); palaeographic confirmation of ALL machine readings; 1812 georeference; SI AS 749 digitisation; F0000212 metadata (SEM); Gaspari inventory no.; school chronicle keeper; first recorded interviews.",
  principleSi:
    "Skladno s pravili issue #17: nič od #16 ni podvojeno; Atlas ni bil na novo izdelan; PT 1–98 NI prepisan ponovno (samo pregledan); REVIEW→VERIFIED SAMO s primarnim dokazom (javni zapis SEM, VAČ, GisKD, Commons); AI ni dokazni vir — VLM branja ostajajo REVIEW z označenimi negotovostmi [~]; negativni rezultati ostajajo vidni.",
  principleEn:
    "Per the issue #17 rules: nothing from #16 duplicated; the Atlas was not rebuilt; PT 1–98 NOT re-transcribed (only reviewed); REVIEW→VERIFIED ONLY with primary evidence (public SEM record, VAČ, GisKD, Commons); AI is not an evidentiary source — VLM readings stay REVIEW with marked uncertainties [~]; negative results remain visible.",
};
