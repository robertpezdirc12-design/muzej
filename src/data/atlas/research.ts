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
    structuredEntries: 2974,
    status: "REVIEW",
    noteSi: "143 strani parcel; P36 (2026-10-11, issue #10): VSE strani strojno prebrane — 1–4 in 140–143 (struktura + rekapitulacija, issue #17/P5-b) + 5–139 (P36 kampanja: 2743 strukturiranih vrstic, pass-1 vseh strani + pass-2 78 strani z okvarjeno soslednostjo; dokaz research/issue17/ps-raw/ + PS-full.json). P38 (2026-10-11, issue #10): 3. prehod 20 ciljnih strani (233 VLM branj skupaj; dokaz ps-raw/*-pass3.json + PS-full-v2.json; 2974 izbranih vrstic po adjudikaciji pass3-prednost) + ODKRITJE: zvezek je organiziran po LISTIH (Blatt I–X), vsak list ima LASTNO številčenje parcel — identiteta parcele = (list, številka). P39 (2026-10-11, issue #10): STRUKTURNA REKONSTRUKCIJA (dokaz research/issue17/PS-reconstruction.json) — segmentacija po fizičnem vrstnem redu z lastniškim testom: 33 segmentov; VSEBINSKI DOKAZ per-list številčenja: 29/29 prekrivajočih parov strani ima za iste številke RAZLIČNE lastnike (0 ujemanj) — P36 hipoteza o napačno prebranih številkah je OVRŽENA; 2724 unikatnih (segment, številka) parov, 50 večkulturnih dodatnih vrstic, 200 vrstic z neberljivo številko; kontrolna vsota 102 + 2505 = 2607 je znotraj meje [2221, 2725] — KONSISTENTNO, eksaktna potrditev zahteva človeški pregled (issue #12). Nerešene strani za človeški pregled (issue #12): 69, 85, 86, 88, 93, 128, 138. SPRAVA (P38–P45, 2026-10-12): sekcije GRUND 1889/2505 + NADALJEVANJE 95 + WALDUNG 81 + Blatt X 60; razdvojitev v model parcela×raba (2134 vnosov, 2632 parov, /api/atlas/ps-landuse); leksikon družin in razcepi K1/K2 (kartice Raziskav). Vsi statusi REVIEW (strojno branje ni dokazni vir).",
    noteEn: "143 pages of parcels; P36 (2026-10-11, issue #10): ALL pages machine-read — 1–4 and 140–143 (structure + recapitulation, issue #17/P5-b) + 5–139 (the P36 campaign: 2,743 structured rows, pass-1 on all pages + pass-2 on 78 pages with broken continuity; evidence research/issue17/ps-raw/ + PS-full.json). P38 (2026-10-11, issue #10): 3rd pass over 20 target pages (233 VLM reads total; evidence ps-raw/*-pass3.json + PS-full-v2.json; 2,974 chosen rows, pass3-preferred adjudication) + DISCOVERY: the volume is organized by SHEETS (Blatt I–X), each with its own parcel numbering — parcel identity = (sheet, number). P39 (2026-10-11, issue #10): STRUCTURAL RECONSTRUCTION (evidence research/issue17/PS-reconstruction.json) — physical-order segmentation with the owner test: 33 segments; CONTENT EVIDENCE of per-sheet numbering: 29/29 overlapping page pairs carry DIFFERENT owners for the same numbers (0 matches) — the P36 misread-numbers hypothesis is REFUTED; 2,724 unique (segment, number) pairs, 50 multi-culture extra rows, 200 rows with unreadable numbers; the checksum 102 + 2,505 = 2,607 lies within the bounds [2,221, 2,725] — CONSISTENT, exact confirmation requires human review (issue #12). Unresolved pages for human review (issue #12): 69, 85, 86, 88, 93, 128, 138. RECONCILIATION (P38–P45, 2026-10-12): the sections GRUND 1,889/2,505 + CONTINUATION 95 + WALDUNG 81 + Blatt X 60; the split into the parcel×culture model (2,134 entries, 2,632 pairs, /api/atlas/ps-landuse); the family lexicon and the K1/K2 splits (the Research cards). All statuses REVIEW (machine reading is not evidentiary).",
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
    pagesTranscribed: 71,
    pagesReadList: Array.from({ length: 71 }, (_, i) => i + 1),
    structuredEntries: 11,
    status: "REVIEW",
    noteSi: "71 strani ocen in razredov — PREBRAN V CELIOTI. Issue #4 (2026-10-10): vzorčenih 12 strani (1–3 topografija, 20/30/40/50/60 razredi, 68–71 protokoli; dokaz PZ-profile.json + PZ-valuation.json). P44 (2026-10-12, issue #11, dokaz research/issue11/pz-classes-full.json + pz-raw/, 76 VLM klicev): 1. krog str. 4–67 (64 strani, enotni prompt) + 12 ciljnih ponovnih branj (str. 25, 63, 65, 67 + sanacija odrezanih 12/13/15 + divergentna 50) + p67 polovični branj, verifikacija s PV kontekstom in odločilni izrez 1,6×. REKAPITULACIJA str. 67: 10 razredov + Summa 1152 j 495 kl, Brutto 8872 fl 5¾ kr, Rein 4492 fl 51 kr; Acker I 80 j 842 kl (korroborirano s str. 12) + II 334 j 120 kl [~] (adjudicirano iz 234: Kurrent oblika »3«, aritmetika 1145 ≈ 1152, PV Acker 413); Wiesen 15+29 j; Weingärten 7 j; Hutweiden 118 + Weiden mit Holznutzung 558 j (negativen Rein/joch); Bauarea 1 j. USKLDITEV s PV: Summa ≈ PV erste Summe 1148 j (+4 ≈ 0,3 %); kontrola str. 65 »Weiden gesamt 636 j 263 kl« = PV natančno; divergenca str. 50 RAZREŠENA (25 fl 44 − 10 fl 40½ = 15 fl 3½ ≈ 15 fl 5). Odprto za #12: Δ 7 j (vsota vrstic vs Summa), Weingärten klafter 42/665, Bauarea 1/4 j. Vsi statusi REVIEW (strojno branje ni dokazni vir).",
    noteEn: "71 pages of valuations and classes — READ IN FULL. Issue #4 (2026-10-10): 12 pages sampled (1–3 topography, 20/30/40/50/60 classes, 68–71 protocols; evidence PZ-profile.json + PZ-valuation.json). P44 (2026-10-12, issue #11, evidence research/issue11/pz-classes-full.json + pz-raw/, 76 VLM calls): pass 1 over pp. 4–67 (64 pages, a uniform prompt) + 12 targeted re-reads (pp. 25, 63, 65, 67 + repairing the truncated 12/13/15 + the divergent 50) + p67 half-reads, a verification pass with PV context and a decisive 1.6× crop. RECAPITULATION p. 67: 10 classes + Summa 1152 j 495 kl, gross 8872 fl 5¾ kr, net 4492 fl 51 kr; Acker I 80 j 842 kl (corroborated by p. 12) + II 334 j 120 kl [~] (adjudicated from 234: the Kurrent »3« shape, the arithmetic 1145 ≈ 1152, PV Acker 413); Wiesen 15+29 j; Weingärten 7 j; Hutweiden 118 + Weiden mit Holznutzung 558 j (negative net/joch); Bauarea 1 j. RECONCILIATION with PV: Summa ≈ PV erste Summe 1148 j (+4 ≈ 0.3 %); the p. 65 control »Weiden gesamt 636 j 263 kl« = PV exactly; the p. 50 divergence RESOLVED (25 fl 44 − 10 fl 40½ = 15 fl 3½ ≈ 15 fl 5). Open for #12: Δ 7 j (row sum vs Summa), Weingärten klafter 42/665, Bauarea 1/4 j. All statuses REVIEW (machine reading is not evidentiary).",
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
    noteSi: "84 stavbnih vrstic (hišne št. 1–99 + prečrtana dvojnica 34) prebranih s pomočjo strojnega branja; vsi vnosi status REVIEW. Issue #17: 101 vrstica preverjena (81 POTRJENIH, 15 popravkov, 4 manjkajoče vrstice, str. 4 konča pri hiši 40). P3 PALEOGRAFSKA PREVERBA (2. krog, 2026-10-08): sveži izrezi + povišana ločljivost, prompti »črka-za-črko«; 15 popravkov in 4 dodatne vrstice APLICIRANE v register (houses.ts) pri 2-kratni konvergenci branj; renumeracija str. 4 (36–41 → 35–40) 4× potrjena. P43 (2026-10-11, issue #13): PRVA CELOTNA VERIGA PT→PUA→PS (105 vrstic nič-zgube, dokaz research/issue13/chain-full-pt-ps.json) — 2 DOKAZANI + 5 VERJETNIH + 4 MOGOČE hiše segajo do parcel PS; križna potrditev korpusa s P41: 65/65 Točno; ATLAS_OWNERS houseRefs (mešano številčenje prve gradnje) izven verige. Statusi ostajajo REVIEW (dokončna potrditev = človeška paleografija #12).",
    noteEn: "84 building rows (house nos. 1–99 + the struck duplicate 34) read with machine assistance; all entries carry REVIEW status. Issue #17: 101 rows checked (81 CONFIRMED, 15 corrections, 4 missing rows, p. 4 ends at house 40). P3 PALAEOGRAPHIC VERIFICATION (2nd pass, 2026-10-08): fresh crops + upscaled resolution, letter-by-letter prompts; 15 corrections and 4 additional rows APPLIED to the register (houses.ts) on 2-pass convergence; the p. 4 renumbering (36–41 → 35–40) confirmed 4×. P43 (2026-10-11, issue #13): FIRST FULL CHAIN PT→PUA→PS (105 zero-loss rows, evidence research/issue13/chain-full-pt-ps.json) — 2 PROVEN + 5 LIKELY + 4 POSSIBLE houses reach the PS parcels; corpus cross-check against P41: 65/65 EXACT; ATLAS_OWNERS houseRefs (first-build mixed numbering) excluded from the chain. Statuses stay REVIEW (final confirmation = human palaeography #12).",
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
  source: "N083PS str. 140–143 (Arhiv RS, SI AS 176, k.o. Griblje) — research/issue17/PS-structure.json; P36: strojni prepis str. 5–139 (ps-raw/, PS-full.json); P38: 3. prehod 20 ciljnih strani (PS-full-v2.json); P39: strukturna rekonstrukcija (PS-reconstruction.json)",
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
    "Veriga hiša→parcela→lastnik je v VSAKI vrstici glavnega registra (stolpci Haus Nro. + lastnik + parcela + raba + površina), a vrstice NISO grupirane po lastnikih → vstop prek stolpca Haus Nro. P36 (2026-10-11): strojni prepis vseh 135 strani (5–139, 2743 vrstic, dvoprehodno na 78 straneh) IZVEDEN; P38 (2026-10-11): 3. prehod 20 ciljnih strani (233 VLM branj, 2974 izbranih vrstic) + odkritje organizacije po listih (Blatt I–X); P39 (2026-10-11): strukturna rekonstrukcija — 33 segmentov, 29/29 vsebinski dokaz per-list številčenja, 2724 unikatnih (segment, številka) parov, kontrolna vsota 2607 znotraj meje [2221, 2725] — KONSISTENTNO; SPRAVA (P38–P45, 2026-10-12): sekcije spravljene (GRUND 1889/2505, NADALJEVANJE 95, WALDUNG 81, Blatt X 60), razdvojitev v model parcela×raba (2134 vnosov, 2632 parov, /api/atlas/ps-landuse), leksikon družin + K1/K2 razcepi — preostane: uskladitev s kontrolno vsoto 102 + 2505 = 2607 (šteje kategorije — glavni niz sega čez 2840), primerjava z rekapitulacijo (~str. 140–143) in nato ciljano po hišah prek Haus Nro.",
  mostUsefulEn:
    "The house→parcel→owner chain sits in EVERY row of the main register (Haus Nro. + owner + parcel + culture + area columns), but rows are NOT grouped by owner → enter via the Haus Nro. column. P36 (2026-10-11): the machine transcription of all 135 pages (5–139, 2,743 rows, two passes on 78 pages) is DONE; P38 (2026-10-11): the 3rd pass over 20 target pages (233 VLM reads, 2,974 chosen rows) + the discovery of the sheet organization (Blatt I–X); P39 (2026-10-11): the structural reconstruction — 33 segments, 29/29 content evidence of per-sheet numbering, 2,724 unique (segment, number) pairs, the checksum 2,607 within [2,221, 2,725] — CONSISTENT; RECONCILIATION (P38–P45, 2026-10-12): the sections reconciled (GRUND 1,889/2,505, CONTINUATION 95, WALDUNG 81, Blatt X 60), the split into the parcel×culture model (2,134 entries, 2,632 pairs, /api/atlas/ps-landuse), the family lexicon + the K1/K2 splits — remaining: matching against the checksum 102 + 2,505 = 2,607 (it counts categories — the main series runs past 2,840), comparison with the recapitulation (~pp. 140–143), then targeting by house via Haus Nro.",
  sampleRowCount: 2974,
};

/** P44 (issue #11): PZ — adjudicirana tabela cenilnih razredov (rekapitulacija str. 67).
 *  Vrednosti KOT PREBRANE; [~] = negotovo. 5 neodvisnih branj str. 67 + izrez 1,6×;
 *  dokaz research/issue11/pz-classes-full.json (readings, divergence register, podporna gradiva). */
export interface PzClassRow1825 {
  culture: string;
  classLabel: string;
  joch: number;
  klafter: number;
  /** ~ = med branjmi variira; clear = stabilna */
  confidence: "clear" | "~";
  bruttoPerJoch: string;
  reinPerJoch: string;
  noteSi: string;
}

export const PZ_CLASS_TABLE_1825: {
  source: string;
  page: number;
  status: ResearchStatus;
  rows: PzClassRow1825[];
  summa: { joch: number; klafter: number; bruttoTotal: string; reinTotal: string; confidence: string };
  rowSumJoch: number;
  reconciliationSi: string;
  reconciliationEn: string;
  divergencesSi: string;
  inferencesSi: string;
} = {
  source: "N083PZ str. 67 (Specifischer Ausweis der Endresultate) — research/issue11/pz-classes-full.json",
  page: 67,
  status: "REVIEW",
  rows: [
    { culture: "Acker", classLabel: "I", joch: 80, klafter: 842, confidence: "clear", bruttoPerJoch: "22 fl 44 kr", reinPerJoch: "13 fl 5 kr [~ 13/15]", noteSi: "korroborirano s str. 12 (§3: 80 Joch 974 Klafter [~], 224 parcel)" },
    { culture: "Acker", classLabel: "II", joch: 334, klafter: 120, confidence: "~", bruttoPerJoch: "16 fl 50 kr [~]", reinPerJoch: "7 fl 35 kr", noteSi: "adjudicirano iz 234: izrez 1,6× prepozna Kurrent »3«; aritmetika vrstic in PV Acker 413 podpirata 334; razreda III/IV ni (4 branj)" },
    { culture: "Wiesen", classLabel: "I", joch: 15, klafter: 1594, confidence: "clear", bruttoPerJoch: "9 fl 24 kr", reinPerJoch: "7 fl 20 kr", noteSi: "" },
    { culture: "Wiesen", classLabel: "II", joch: 29, klafter: 818, confidence: "~", bruttoPerJoch: "4 fl [?] kr", reinPerJoch: "3 fl [?] kr", noteSi: "1× prebrano 39; razreda III ni" },
    { culture: "Kleine Gärten", classLabel: "C", joch: 3, klafter: 612, confidence: "~", bruttoPerJoch: "20–22 fl 44 kr [~]", reinPerJoch: "10–13 fl 5 kr [~]", noteSi: "klafter 612/615/619 [~]" },
    { culture: "Größere Gärten", classLabel: "C", joch: 0, klafter: 105, confidence: "~", bruttoPerJoch: "20–23 fl 44 kr [~]", reinPerJoch: "10–13 fl 5 kr [~]", noteSi: "joch prazen ali neberljiv" },
    { culture: "Weingärten", classLabel: "C", joch: 7, klafter: 42, confidence: "clear", bruttoPerJoch: "21–24 fl [~]", reinPerJoch: "7 fl 10 kr", noteSi: "joch = PV natančno; klafter 42 ≠ PV 665 [~] — odprto" },
    { culture: "Hutweiden", classLabel: "C", joch: 118, klafter: 702, confidence: "~", bruttoPerJoch: "1 fl [?] kr", reinPerJoch: "−15 do −45 kr [~ negativen]", noteSi: "negativen čisti donos/joch — pašniki po stroških ne dajejo donosa [~]" },
    { culture: "Weiden mit Holznutzung", classLabel: "C", joch: 558, klafter: 846, confidence: "~", bruttoPerJoch: "1 fl 6 kr", reinPerJoch: "−51 kr [~ negativen]", noteSi: "klafter 558/846/858 [~]" },
    { culture: "Bauarea", classLabel: "—", joch: 1, klafter: 1199, confidence: "~", bruttoPerJoch: "16 fl 50 kr", reinPerJoch: "7 fl 35 kr", noteSi: "PV Bau 4 j 889 kl — razlika [~] odprta" },
  ],
  summa: { joch: 1152, klafter: 495, bruttoTotal: "8872 fl 5¾ kr", reinTotal: "4492 fl 51 kr", confidence: "clear (4/5 branj)" },
  rowSumJoch: 1145,
  reconciliationSi:
    "Summa 1152 j 495 kl ≈ PV erste Summe 1148 j 539 kl (Δ +4 j ≈ 0,3 %) — klasificirane kulture se na ravni vsote skladijo. Po kulturah: Acker 414 ≈ PV 413 (+1); Wiesen 44 proti PV 88 (−44) in Weiden 676 proti PV 636 (+40) — PZ ožje klasificira travnike, širje pašnike (skupna kompenzacija ≈ −4); Weingärten 7 = PV 7; Gärten 3 ≈ PV 2 [~]; Bauarea 1 proti PV 4 [~]. NEODVISNA KONTROLA: str. 65 nadzorna opomba »Weiden gesamt: 636 j 263 kl« = PV natančno — PZ in PV sta ista presnova. PR: 1028 × 1884 kl = 1210,5 j ≈ PV grand total 1221 (−0,9 %).",
  reconciliationEn:
    "The Summa 1152 j 495 kl ≈ the PV erste Summe 1148 j 539 kl (Δ +4 j ≈ 0.3 %) — the classified cultures agree at the total level. By culture: Acker 414 ≈ PV 413 (+1); Wiesen 44 vs PV 88 (−44) and Weiden 676 vs PV 636 (+40) — PZ classifies meadows more narrowly and pastures more broadly (the compensation nets to ≈ −4); Weingärten 7 = PV 7; Gärten 3 ≈ PV 2 [~]; Bauarea 1 vs PV 4 [~]. INDEPENDENT CONTROL: the p. 65 note »Weiden gesamt: 636 j 263 kl« = PV exactly — PZ and PV share one survey. PR: 1028 × 1884 kl = 1210.5 j ≈ the PV grand total 1221 (−0.9 %).",
  divergencesSi:
    "6 registriranih divergenc (dokaz pz-classes-full.json): D1 Acker II 234/334 — ADJUDICIRANO na 334 [~] (3 dokazi, končna potrditev #12); D2 str. 50 Acker I veriga — RAZREŠENO (prečrtani 20 fl 44 nadomešča 25 fl 44; 25 fl 44 − 10 fl 40½ = 15 fl 3½ ≈ zapisani 15 fl 5); D3 Wiesen II 29/39 — večinsko 29 [~]; D4 vsota vrstic 1145 vs Summa 1152 (Δ 7 j) — ODEPRTO (5 branj ni našla manjkajočih vrstic); D5 Weingärten klafter 42/665 — ODEPRTO; D6 vrstični Rein zneski Acker I — ODEPRTO. Vse odprte točke gredo na človeško paleografijo (#12).",
  inferencesSi:
    "INFERENCA (ne branje): Rein 4492 fl 51 kr / 441 prebivalcev ≈ 10,2 fl na prebivalca letno; / 102 družine [~] ≈ 44 fl na družino; Rein/Brutto = 4492/8872 ≈ 50,6 % (skladno z Bau-Area stopnjo 45 %); pašniki 676 j = 59 % klasificirane površine (skladno PV).",
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

/** P41 (issue #10) — PS 1825: paleografija str. 140–143 — "Abschluß der Gemeinde" + per-Lage rekapitulacija. */
export const PS_RECAP_PALEO_P41: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  lageRows: { lage: number; haus: string; joch: number; klafter: number; kind: string }[];
  lageSum: { joch: number; klafter: number; pass: boolean };
  page140Left: { summaGrundparzellen: string; zinsbBauparzellen: string; summaNach: string };
  abschluss: {
    title: string;
    summeDerGrundparzellen: string;
    summeDerBauparzellen: string;
    areaDerGemeinde: string;
    unresolvedSplit: { constraint: string; resolved: boolean; status: string };
    date: string;
  };
  page141: {
    referencePairs: { parf1: string; parf2: string }[];
    pairSemantics: string;
    summaries: { summa: string; grundparzellenZusatz: string; summaInGemeinde: string };
    p9Corrections: string[];
  };
  page143: { values: string[]; passes: string };
  page142: { rowsOnPage: number; unresolved: string };
  identities: Record<string, { pass: boolean; detail: string }>;
  crossCheck: {
    modelRefs: { total: number; missing: number[] };
    areaAttribution: {
      klafterPerJoch: number;
      modelGrundJoch: number;
      preferred: { label: string; joch: number; deltaPct: number };
      p40Best: string;
    };
  };
  resolves: string[];
  open: string[];
  verdictSi: string;
  verdictEn: string;
} = {
  series: "PS",
  source:
    "N083PS (VAČ vacId 373415, pdfPageImage posnetki str. 140–143) — 12 neodvisnih VLM prehodov (3×4, glm-5v-turbo, [~]/[?]) + deterministična sprava scripts/p41_ps_recap_paleo.py; polni izpis research/issue17/ps-recap-paleo.json + src/data/atlas/ps-recap-paleo.json",
  status: "REVIEW",
  generatedBy: "scripts/p41_ps_recap_paleo.py",
  lageRows: [
    { lage: 1, haus: "124", joch: 101, klafter: 253, kind: "vlm-consensus" },
    { lage: 2, haus: "125", joch: 89, klafter: 78, kind: "vlm-consensus" },
    { lage: 3, haus: "126", joch: 82, klafter: 81, kind: "vlm-consensus" },
    { lage: 4, haus: "127", joch: 125, klafter: 183, kind: "vlm-consensus" },
    { lage: 5, haus: "128", joch: 189, klafter: 1228, kind: "vlm-consensus" },
    { lage: 6, haus: "129", joch: 162, klafter: 447, kind: "vlm-consensus" },
    { lage: 7, haus: "130", joch: 82, klafter: 32, kind: "vlm-consensus" },
  ],
  lageSum: { joch: 831, klafter: 702, pass: true },
  page140Left: {
    summaGrundparzellen: "831|702",
    zinsbBauparzellen: "3|312",
    summaNach: "834|1014",
  },
  abschluss: {
    title: "Abschluß der Gemeinde (rdeči tuš, str. 140 desno)",
    summeDerGrundparzellen: "1215|490",
    summeDerBauparzellen: "5|1003",
    areaDerGemeinde: "1220|1493",
    unresolvedSplit: {
      constraint: "K1 + K2 = 2090 K (iz 831+383+1 = 1215 in 490)",
      resolved: false,
      status: "UNRESOLVED (doberesedlni razcep); vsota preverjena",
    },
    date: "Graz den 25ten July 1841 [~] (VLM p1/p2)",
  },
  page141: {
    referencePairs: [
      { parf1: "830", parf2: "1188" },
      { parf1: "133", parf2: "1196" },
      { parf1: "132", parf2: "1466" },
      { parf1: "206", parf2: "836" },
      { parf1: "286", parf2: "921" },
      { parf1: "268", parf2: "1341" },
      { parf1: "138", parf2: "1457" },
    ],
    pairSemantics: "UNRESOLVED — hipotezi 'dve parceli' in 'razpon' OVRŽENI (model); dokumentirano",
    summaries: { summa: "1217|684", grundparzellenZusatz: "4|889 [~1]", summaInGemeinde: "1221|1570 [~1573]" },
    p9Corrections: ["190/1168", "286/8931", "198/11957"],
  },
  page143: { values: ["102", "2505", "2607"], passes: "3/3 enoglasno" },
  page142: { rowsOnPage: 40, unresolved: "skupna dolžina Verzeichnis (nadaljevanje na neosvanih straneh)" },
  identities: {
    a_lageRowSum: { pass: true, detail: "7 vrstic == 831|702" },
    ab_summaNach: { pass: true, detail: "831|702 + 3|312 == 834|1014" },
    c_abschlussGrund: { pass: true, detail: "831|K1[~] + 383|K2[~] == 1215|490 (vsota preverjena, razcep UNRESOLVED)" },
    d_abschlussBaup: { pass: true, detail: "3|312 + 2|691 == 5|1003" },
    e_areaGemeinde: { pass: true, detail: "1215|490 + 5|1003 == 1220|1493" },
    f_page143: { pass: true, detail: "102 + 2505 == 2607 (regresija)" },
    g_page141Weak: { pass: true, detail: "1217|684 + 4|889 == 1221|1573 ≈ zapis 1570 [~] (šibko, visual-crop)" },
  },
  crossCheck: {
    modelRefs: { total: 14, missing: [1188, 1196, 1466] },
    areaAttribution: {
      klafterPerJoch: 1600,
      modelGrundJoch: 1232.96,
      preferred: { label: "Area der Gemeinde 1220|1493 (P41 NOVO)", joch: 1220.9331, deltaPct: 0.99 },
      p40Best: "GRUND_1_2505 samo (Δ +16.96 Joch ≈ +1.39 %)",
    },
  },
  resolves: [
    "P40 UNRESOLVED 'naivna vsota 1413': P9 branja par popravljena; 7 vrstic ima vsoto 831|702, skladno z 'Summa der Grundparzellen' str. 140",
    "P40 kandidat 'Summa 1216(?)': nadomeščen z 'Area der Gemeinde 1220|1493' (Δ +0,99 %)",
    "poreklo rdeče vsote str. 141 ('~1216'): najverjetneje 1215 (Summe) ali 1220 (Area) — razcep [~]",
  ],
  open: [
    "semantika par referenc (830,1188)… — UNRESOLVED",
    "razcep K1/K2 v Abschlußu (K1+K2 = 2090) — UNRESOLVED",
    "p142 Verzeichnis skupna dolžina — UNRESOLVED",
    "p141 spodnji vsotni blok — ŠIBKO (visual-crop)",
    "hiše 121½–123 in 134–135 brez površin v rekapitulaciji",
  ],
  verdictSi:
    "Paleografija str. 140–143 (12 VLM prehodov + izrezi) je prvič ujela SKUPNO POVRŠINO OBČINE: 'Area der Gemeinde' 1220 Joch 1493 Klafter (rdeči tuš), aritmetično zvezana (1215|490 + 5|1003 = 1220|1493). 7 vrstic 'Grundstückslagen' (hiše 124–130) se sešteje v 831|702 = 'Summa der Grundparzellen' — P40 'naivna vsota 1413' razrešena kot P9 napaka branja. Model GRUND (1232,96 J) odmika le +0,99 % od Areje — najbolj skladna atribucija doslej. Razcepi (K1/K2, semantika par referenc) ostajajo izrecno UNRESOLVED.",
  verdictEn:
    "Palaeography of pp. 140–143 (12 VLM passes + zoomed crops) captured the MUNICIPAL TOTAL AREA for the first time: 'Area der Gemeinde' 1,220 Joch 1,493 Klafter (red chalk), arithmetically bound (1,215|490 + 5|1,003 = 1,220|1,493). The 7 'Grundstückslagen' rows (houses 124–130) sum to 831|702 = 'Summa der Grundparzellen' — P40's 'naive sum 1,413' resolved as a P9 reading error. The GRUND model (1,232.96 J) deviates only +0.99% from the Area — the most consistent attribution yet. Splits (K1/K2, pair-reference semantics) remain explicitly UNRESOLVED.",
};

/**
 * ISSUE #10 (P42) — PS 1825: pravilnik rab v2 — deterministična razširitev
 * klasifikacije rab nad P39 model. 12 v1 pravil NESPREMENJENIH + 13 priloženih
 * pravil (13–25; prvi zadetek = primarni razred). Izrecna ločitev termType:
 * KULTURA / TOPONIM / ARTIFAKT / NEKLASIFICIRANO. V2 ⊇ V1 (noben v1 primarni
 * razred ni spremenjen — regresijsko preverjeno nad vsemi 2632 pari).
 * Polni izpis: research/issue17/ps-landuse-v2.json + src/data/atlas/ps-landuse-v2.json
 * (identična kopija; API GET /api/atlas/ps-landuse-v2).
 */
export const PS_LANDUSE_V2_P42: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  countScope: string;
  rulebook: {
    version: string;
    v1RulesCount: number;
    appendedRules: { no: number; class: string; labelSi: string; pattern: string; confidence: string; noteSi: string; pairs: number }[];
  };
  stats: {
    pairsTotal: number;
    v1ClassifiedPairs: number;
    v2ClassifiedPairs: number;
    toponymPairs: number;
    artifaktPairs: number;
    unresolvedPairs: number;
    classifiedPctV1: number;
    classifiedPctV2: number;
    explainedPctV2: number;
    unresolvedRows: number;
    primaryCountsV2: Record<string, number>;
    newPairsByClassV2: Record<string, number>;
  };
  toponym: { pairs: number; distinct: number; top: { raw: string; pairs: number }[] };
  artifakt: { pairs: number; distinct: number; numericRawCount: number };
  families: { id: string; values: string[]; pairs: number; hypothesisSi: string; confidence: string; verdict: string; coParcel: Record<string, number> }[];
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "PS",
  source:
    "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — pravilnik v2 deterministično nad P39 modelom (committed dokaz ps-landuse.json); polni izpis research/issue17/ps-landuse-v2.json + src/data/atlas/ps-landuse-v2.json",
  status: "REVIEW",
  generatedBy: "scripts/p42_ps_rulebook_v2.py",
  countScope: "štetje po PARIH parcela×raba (podvojene rabe znotraj parcele enkrat) — kot P39",
  rulebook: {
    version: "v2",
    v1RulesCount: 12,
    appendedRules: [
      { no: 13, class: "OBCINA", labelSi: "občinska skupna", pattern: "gmde\\b|gmand\\b|gimand|gemaind", confidence: "~", noteSi: "dialektne okrajšave Gemainde (Gmde/Gmand/Gimand) = občinska skupna zemlja; Gumig Gmde, Lohgimand NNN (= Lohgemainde)", pairs: 12 },
      { no: 14, class: "TRAVNIK", labelSi: "travnik (Wiese)", pattern: "maid\\b", confidence: "~", noteSi: "Maid = Mahd = Mähwiese (kärntensko); družina Haitenmaid", pairs: 16 },
      { no: 15, class: "TRAVNIK", labelSi: "travnik (Wiese)", pattern: "gras\\b|heu\\b|wisen\\b|rasen\\b", confidence: "~", noteSi: "Gras/Heu = travniški pridelek (einheimisches Gras/Heu); wisen = Wiesen; Rasen", pairs: 23 },
      { no: 16, class: "VINOGRAD", labelSi: "vinograd", pattern: "wein", confidence: "~", noteSi: "sami 'Wein'/'Weing' = okrajšava za Weingarten (v1 vrzel: 10 parov vinogradov nevidnih)", pairs: 11 },
      { no: 17, class: "VRT", labelSi: "vrt (Garten)", pattern: "gae?rt", confidence: "~", noteSi: "umlaut Gärten (→ gaerten) — v1 'gart' jih ni ujel", pairs: 13 },
      { no: 18, class: "VRT", labelSi: "vrt (Garten)", pattern: "obst|himbeer|gmias", confidence: "~", noteSi: "Obst = sadovnjak, Himbeeren = malinje, Gmias = Gemüse", pairs: 15 },
      { no: 19, class: "NJIVA", labelSi: "njiva (Acker)", pattern: "rueben|schlagfeld|stopp\\b|achl\\b|frucht", confidence: "~", noteSi: "Rüben = poljska kultura; Schlagfeld = izsekano polje; Stopp = Stoppeln; Achl = kärntensko Acker; Frucht = žito", pairs: 46 },
      { no: 20, class: "GOZD", labelSi: "gozd (Wald)", pattern: "wald|gebuesch|straeuch|eichhol|laub\\b|laubm|lorbeer|baum", confidence: "~", noteSi: "sredbesedni -wald (Schlagwald, Lohwald); Gebüsch/Gesträuch; Eichhol; Laub; Lorbeer; baum = drevesna opomba", pairs: 32 },
      { no: 21, class: "PASTVISCE", labelSi: "pašnik (Weide/Hutweide/Trift)", pattern: "shut\\b|johut\\b|weid", confidence: "~", noteSi: "-shut (Schingutshut), Johut; weid BREZ \\b (Schafweide); izrecno NE zajame Lhut", pairs: 14 },
      { no: 22, class: "NEROD", labelSi: "nerodovoljna (Ödung)", pattern: "aehnl?\\b|eidn\\b|eidau|ehda\\b|inoed|aeinod|wist|brache\\b", confidence: "~", noteSi: "Öhnl/Aehn = osuto; Eidn/Eidau/Ehda = Öden/Ödau; Ainöd = Einöde; Wist* = wüst; Brache", pairs: 73 },
      { no: 23, class: "TRAVNIK", labelSi: "travnik (Wiese)", pattern: "malde\\b", confidence: "?", noteSi: "Malde = Mahd (kärntensko, Schatz); samo 'Ehmalde' 1 par — spekulativno", pairs: 1 },
      { no: 24, class: "STAVBNO", labelSi: "stavbna/gospodarska", pattern: "schupf|staidl|grube\\b|gutl\\b|edl?hop|edhup|hau(ss)?\\b|boden\\b", confidence: "~", noteSi: "Schupfe (v1 schupfn zgrešil schupf./schupfen!); Staidl = Stadel; Grube (Lohgrube, Steingrube); -gutl = Gütl; Ed-/Edl-hop; -hauß; Boden (Schüttboden 100 % so-odvisen STAVBNO)", pairs: 45 },
      { no: 25, class: "VODA", labelSi: "voda", pattern: "lachen?\\b", confidence: "~", noteSi: "Lache(n) = lokva/mlaka", pairs: 2 },
    ],
  },
  stats: {
    pairsTotal: 2632,
    v1ClassifiedPairs: 1896,
    v2ClassifiedPairs: 2199,
    toponymPairs: 122,
    artifaktPairs: 29,
    unresolvedPairs: 282,
    classifiedPctV1: 72.0,
    classifiedPctV2: 83.5,
    explainedPctV2: 89.3,
    unresolvedRows: 282,
    primaryCountsV2: {
      NJIVA: 1095,
      TRAVNIK: 527,
      GOZD: 166,
      STAVBNO: 97,
      NEROD: 95,
      VRT: 79,
      PASTVISCE: 68,
      OBCINA: 27,
      ALM: 23,
      VINOGRAD: 19,
      VODA: 2,
      CESTA: 1,
    },
    newPairsByClassV2: {
      NEROD: 73,
      NJIVA: 46,
      STAVBNO: 45,
      TRAVNIK: 40,
      GOZD: 32,
      VRT: 28,
      PASTVISCE: 14,
      OBCINA: 12,
      VINOGRAD: 11,
      VODA: 2,
    },
  },
  toponym: {
    pairs: 122,
    distinct: 39,
    top: [
      { raw: "Löwisch Thal", pairs: 15 },
      { raw: "Leite", pairs: 11 },
      { raw: "Schüttgrund", pairs: 10 },
      { raw: "Ebneist", pairs: 6 },
      { raw: "Schmieggrat", pairs: 6 },
      { raw: "Eingemaut Gfrörer und Laimauer", pairs: 12 },
      { raw: "Abtränig Spötlg. Leumuth", pairs: 6 },
      { raw: "Ebnerd", pairs: 5 },
      { raw: "Indrunt Laimen", pairs: 5 },
    ],
  },
  artifakt: { pairs: 29, distinct: 29, numericRawCount: 19 },
  families: [
    { id: "LHUT-JEDRO", values: ["Lhut", "Lhup", "Lhupf", "Lhupa", "Lhuta"], pairs: 36, hypothesisSi: "morda L+Hut (pašnik) ali Lehen-Hut; tudi Rhut (Rodung) ob zamenjavi R/L v Kurrentu — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { NJIVA: 10 } },
    { id: "LHIZ", values: ["Lhize", "Lhizl"], pairs: 9, hypothesisSi: "ista neznana družina kot Lhut-jedro (Lhizgutl [?] pa v2 STAVBNO prek formanta -gutl = Gütl)", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { TRAVNIK: 1 } },
    { id: "LHOPI-LOHIFA", values: ["Lhopi", "Lohifa", "Luppa", "Shüfa"], pairs: 23, hypothesisSi: "morda ista korenina kot Lhut (t/p/f obrati OCR) — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { NJIVA: 3, VRT: 1 } },
    { id: "LOHN-RAUT", values: ["Lohn", "Lohng", "Lohnraut Gfüttergütl", "Lohnraut Bäurean", "Lohnraut Lönnean"], pairs: 29, hypothesisSi: "Lohn/Loh = izsek (Waldschlag) ALI Loh = strojnica; Raut = Rodung (izsek) — smer GOZD?/NJIVA? — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { NJIVA: 2 } },
    { id: "AHN", values: ["Ahn"], pairs: 13, hypothesisSi: "morda Ahorn (javor) ali Acker-dialekt — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: {} },
    { id: "AEFLING", values: ["Äfling"], pairs: 13, hypothesisSi: "neznano; so-odvisnost: 12/13 parov na parcelah s TRAVNIK → travniški kontekst, termin ostaja neznan", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { TRAVNIK: 12 } },
    { id: "ERDAR", values: ["Erdar", "Eidar", "Achat", "Achm"], pairs: 10, hypothesisSi: "morda Erd-/Eid- (Öd?) ali Achm = Acker-Mad — NE dokazano; Erdar 4/4 so-odvisnost GOZD", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { GOZD: 7, NJIVA: 3, TRAVNIK: 2 } },
    { id: "GUETEN", values: ["Güten", "Gütung"], pairs: 12, hypothesisSi: "morda 'die Güten' (rodovitna tla) ali Güter (kmetije) — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: {} },
    { id: "EINHART", values: ["Einhart mit Gypfel &c.", "Einhart mit Gypf. &c."], pairs: 15, hypothesisSi: "morda Einöd-Hart (Hart = gozd/pašnik na trdem terenu) + Gipfel — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: {} },
    { id: "DINGF", values: ["Dingf"], pairs: 10, hypothesisSi: "morda Dingfeld? — mešana so-odvisnost (TRAVNIK 9/NJIVA 4/ALM 4) — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { TRAVNIK: 9, NJIVA: 4, ALM: 4 } },
    { id: "LUKIG", values: ["Lukig"], pairs: 10, hypothesisSi: "morda Luch/Lukig = mokrišče (Loch) — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { TRAVNIK: 1 } },
    { id: "LOHGARN", values: ["Lohgarn"], pairs: 7, hypothesisSi: "Loh + garn? — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: {} },
    { id: "HURGI", values: ["Hurgi"], pairs: 5, hypothesisSi: "neznano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: {} },
    { id: "WING", values: ["Wing"], pairs: 3, hypothesisSi: "morda Wingert (vinograd, zahodnoavstrijsko) — v Kärntenu netipično — NE dokazano", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: {} },
    { id: "EINSCHLAG-GUELZE", values: ["Einschlag mit Gülze", "Einschicht mit Poggi u. Bau", "Einschicht mit Gfretzgen bau", "Gülze", "Gülze mit Gülze"], pairs: 20, hypothesisSi: "Einschlag = ograda/obor?; Gülze = Gülte?/krma?; 'Einschlag mit Frucht und Gülze' (3 pari) → v2 NJIVA prek formanta Frucht; Einschlag~Einschicht = verjetno isti termin (OCR)", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: { NJIVA: 1 } },
    { id: "SCHINDEL", values: ["Schindel"], pairs: 1, hypothesisSi: "'Schindel baum' (5 parov) → v2 GOZD prek formanta baum; samostojna 'Schindel' ostaja neznan (skodla/les?)", confidence: "?", verdict: "NEKLASIFICIRANO (čaka paleografijo)", coParcel: {} },
  ],
  verdictSi:
    "Pravilnik rab v2 (12 nespremenjenih v1 pravil + 13 priloženih) dviga pokritost klasifikacije z 72,0 % na 83,5 % parov (2199/2632), brez enega samega spremenjenega v1 razreda (v2 ⊇ v1). Vrzeli v1, ki jih v2 zapira: umlaut Gärten (gart ne ujame gaerten), sredbesedni -wald (Schlagwald) in -weid (Schafweide), schupfn ne ujame schupf./schupfen, sami 'Wein' (10 parov vinogradov nevidnih!), Öd/Wüst dialektni zapisi (Eidn/Ehda/Wiste), Maid = Mahd, Gemainde (Gmde/Gimand), Rüben/Schlagfeld/Stopp. Izrecno NOVO ločilo termType: TOPONIM 122 parov (ležajna imena — Löwisch Thal, Leite, Schüttgrund … NI raba!) in ARTIFAKT 29 parov (številke 82–100 v stolpcu rabe na Blatt X — register stavbnih mest!, Summa, Zahl, opombe o prihodkih). Ostaja 282 parov (16 družin + samostojni) izrecno NEKLASIFICIRANO z dokumentiranimi so-odvisnostnimi dokazi za paleografijo (Lhut-jedro 36, Lohn/Raut 29, Lhopi/Lohifa 23, Einhart 15, Äfling 13 z 12/13 travniškim kontekstom …). Pojasnjeno 89,3 % parov.",
  verdictEn:
    "Land-use rulebook v2 (12 unchanged v1 rules + 13 appended) raises classification coverage from 72.0% to 83.5% of pairs (2,199/2,632) without changing a single v1 class (v2 ⊇ v1). v1 gaps closed by v2: umlaut Gärten, mid-word -wald (Schlagwald) and -weid (Schafweide), schupfn missing schupf./schupfen, bare 'Wein' (10 invisible vineyard pairs!), Öd/Wüst dialect spellings (Eidn/Ehda/Wiste), Maid = Mahd, Gemainde (Gmde/Gimand), Rüben/Schlagfeld/Stopp. NEW explicit termType distinction: TOPONIM 122 pairs (place names — Löwisch Thal, Leite, Schüttgrund … NOT a land use!) and ARTIFAKT 29 pairs (numbers 82–100 in the culture column on Blatt X — the building-plot register!, Summa, Zahl, yield notes). 282 pairs (16 families + singles) remain explicitly UNCLASSIFIED with documented co-occurrence evidence for palaeography (Lhut-core 36, Lohn/Raut 29, Lhopi/Lohifa 23, Einhart 15, Äfling 13 with 12/13 meadow context …). 89.3% of pairs explained.",
  next: [
    "3. prehod ~15 dvoumnih strani (potrebuje VAČ posnetke — peskovniška mreža trenutno onemogoča dostop)",
    "16 neznanih družin (Lhut, Lohn/Raut, Äfling …) — človeška paleografija na izrezih",
    "rekapitulacija: razcep K1/K2 (omejitev K1+K2 = 2090) + semantika 7 par referenc — UNRESOLVED",
    "puščanje klasifikacije v PZ ekonomski profil (navzkrižna kontrola rab)",
  ],
};

/** PZ — demografija in cenitev 1825 (N083PZ). */

/**
 * P43 (issue #10) — PS 1825: neznane družine — prečni prehodi, PV območna
 * sprava in ledinsko-imenska struktura. Vrednosti generirane iz
 * research/issue17/ps-lexicon.json (scripts/p43_ps_lexicon.py) — QA jih
 * preverja prek vbrizganega readFile (vzorec qa-p37..p42).
 */
export const PS_LEXICON_P43: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  readingRule: string;
  countScope: string;
  families: {
    id: string;
    pairs: number;
    variants: Record<string, number>;
    distinctVariants: number;
    stablePairs: number;
    fallbackPairs: number;
    variantPairs: number;
    noCounterpart: number;
    block: { pages: number[]; distinctPages: number; contiguousRuns: number; parcelRange: [number | null, number | null] };
    termTypeHypothesis: string;
    topHypotheses: { candidate: string; glossSi: string; source: string; confidence: string }[];
  }[];
  singles: { pairs: number; distinctRaw: number; fallbackPairs: number; noteSi: string };
  pvReconciliation: {
    pvOfficial: Record<string, { joch: number; klafter: number; jochF: number }>;
    psClassAreasJ: Record<string, number>;
    weidenGapJ: number;
    psPastVisceAlmJ: number;
    unknownFamiliesAreaJ: number;
    njivaVsAeckerDeltaJ: number;
    travnikVsWiesenDeltaJ: number;
    vrtVsGemueseDeltaJ: number;
    vinogradVsWeinDeltaJ: number;
    rowsModelTotalJ: number;
    pvTotalJ: number;
    rowsModelVsPvTotalJ: number;
  };
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "PS",
  source:
    "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — prečni prehodi nad P39 modelom + committed PV.json transkripcija + 2 neodvisna LLM leksikografska prehoda (ps-lexicon-raw/, viri NEPREVERJENI); polni izpis research/issue17/ps-lexicon.json + src/data/atlas/ps-lexicon.json",
  status: "REVIEW",
  generatedBy: "scripts/p43_ps_lexicon.py",
  readingRule:
    "pass2wins (P38/P39); prečni prehodi SAMO znotraj iste fotografije (sken vsebuje ponovne posnetke — razponi 61↔83↔84↔86 [161,180] …), med-fotografske primerjave nezanesljive",
  countScope: "štetje po PARIH parcela×raba (podvojene rabe znotraj parcele enkrat) — kot P39/P42",
  families: [
      { id: "LHUT-JEDRO", pairs: 36, variants: {"Lhut": 17, "Lhup": 8, "Lhupf": 7, "Lhupa": 3, "Lhuta": 1}, distinctVariants: 5, stablePairs: 0, fallbackPairs: 0, variantPairs: 14, noCounterpart: 22, block: { pages: [16, 36, 37, 48, 121], distinctPages: 5, contiguousRuns: 22, parcelRange: [261, 2076] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Lhut/Lhup/Lhupf/Lhuta", glossSi: "ledinsko ime, morda povezano s slovanskim korenom 'lom' ali 'log' (grmje, močvirno območje)", source: "neznano — hipoteza brez dokumentiranega vira", confidence: "?" }, { candidate: "Lhut/Lhup/Lhupf", glossSi: "ledinsko ime, morda povezano s slovanskim korenom 'lȕh' (svetli, jasen) ali 'lǫg' (močvirje, log)", source: "Bezlaj, France. Slovenski etimološki slovar. Ljubljana: SAZU, 1976–2008", confidence: "?" }, { candidate: "Lhuta/Lhupa", glossSi: "ledinsko ime, morda povezano s slovanskim korenom 'lȕt' (močvirnato območje)", source: "SSKJ, Slovenski slovar knjižnega jezika", confidence: "?" }] },
      { id: "LOHN-RAUT", pairs: 29, variants: {"Lohn": 13, "Lohng": 2, "Lohnraut Gfüttergütl": 9, "Lohnraut Lönnean": 1, "Lohnraut Bäurean": 4}, distinctVariants: 5, stablePairs: 0, fallbackPairs: 2, variantPairs: 1, noCounterpart: 26, block: { pages: [10, 45, 47, 62, 116], distinctPages: 5, contiguousRuns: 13, parcelRange: [150, 2279] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Lohn (nem.)", glossSi: "Ledinsko ime, izpeljano iz nemške besede 'Lohn' (plača, nagrada), ki bi lahko označevalo zemljišče, ki je bilo nekdaj del plače ali nagrade za delo", source: "DWB (Deutsches Wörterbuch von Jacob und Wilhelm Grimm), Band 16, Spalte 844", confidence: "~" }, { candidate: "Log (slov.)", glossSi: "Ledinsko ime, ki se nanaša na dolino, grapo ali območje, kjer se splavajo lesne delce; v Beli krajini pogosta beseda za ledinska imena", source: "SSKJ (Slovar slovenskega knjižnega jezika)", confidence: "~" }, { candidate: "Lohnraut (nem.)", glossSi: "Kompozitum 'Lohn' + 'Raut' (prazna zemlja, njiva), ki bi lahko pomenil 'njiva, ki je bila del plače' ali 'ledinsko ime, ki se nanaša na posebno vrsto njive'", source: "DWB (Deutsches Wörterbuch von Jacob und Wilhelm Grimm), Band 16, Spalte 844; Schmeller, Bayerisches Wörterbuch, Band 2, Spalte 476", confidence: "~" }] },
      { id: "LHOPI-LOHIFA", pairs: 23, variants: {"Lhopi": 7, "Luppa": 3, "Shüfa": 4, "Lohifa": 9}, distinctVariants: 4, stablePairs: 0, fallbackPairs: 0, variantPairs: 6, noCounterpart: 17, block: { pages: [39, 96, 127, 128, 129], distinctPages: 5, contiguousRuns: 16, parcelRange: [708, 2839] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Lhopi/Luppa", glossSi: "Ledinsko ime, verjetno povezano s slovnično obliko 'log' (dolina, dolina z vodo) ali 'lopata' (kot, kotina), kar se ujema z reliefom Belokejanske pokrajine", source: "SSKJ", confidence: "~" }, { candidate: "Shüfa", glossSi: "Narečna oblika nemškega 'Schlucht' (soteska, grape) ali 'Schluff' (mulj, ilovica), ki bi lahko označevala lokalno značilnost terena", source: "Schmeller, Bayerisches Wörterbuch", confidence: "?" }, { candidate: "Lohifa", glossSi: "Kompozitum nemškega 'Lohe' (mladi gozd, gaj) in slovenskega 'hifa' (hifa, drevesna snov), kar bi lahko označevalo mladi gozd z drevjem", source: "DWB (Grimm)", confidence: "?" }] },
      { id: "EINSCHLAG-GUELZE", pairs: 20, variants: {"Einschlag mit Gülze": 7, "Gülze": 6, "Gülze mit Gülze": 1, "Einschicht mit Gfretzgen bau": 3, "Einschicht mit Poggi u. Bau": 3}, distinctVariants: 5, stablePairs: 0, fallbackPairs: 2, variantPairs: 18, noCounterpart: 0, block: { pages: [76, 114], distinctPages: 2, contiguousRuns: 10, parcelRange: [1162, 2228] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Gülze", glossSi: "ledinsko ime za travnike ali pašnike, verjetno v bližini gozda (Einschlag = posek)", source: "neznano — hipoteza brez dokumentiranega vira", confidence: "~" }, { candidate: "Gülze", glossSi: "ledinsko ime, morda povezano z ledinskim imenom 'Golica' ali 'Golec', ki se pojavlja v Beli krajini in bi lahko označevalo posebno vrsto zemljišča ali njive", source: "SSKJ", confidence: "?" }, { candidate: "Einschlag", glossSi: "nemški izraz za 'sekundarna goščava' ali 'mlada goščava', ki bi lahko označeval posebno vrsto gozdnega zemljišča", source: "DWB (Grimm)", confidence: "?" }] },
      { id: "EINHART", pairs: 15, variants: {"Einhart mit Gypfel &c.": 14, "Einhart mit Gypf. &c.": 1}, distinctVariants: 2, stablePairs: 0, fallbackPairs: 0, variantPairs: 0, noCounterpart: 15, block: { pages: [80], distinctPages: 1, contiguousRuns: 1, parcelRange: [1644, 1658] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Einhart", glossSi: "Ledinsko ime, verjetno pridevniškega izvora, ki označuje parcelo z značilnostjo 'ena' ali 'edina', ali pa je prevzem nemške besede 'Einhart' (ena hrastovina)", source: "SSKJ, Bezlaj, Toporišič", confidence: "~" }, { candidate: "Gypfel", glossSi: "Narečna oblika nemške besede 'Gipfel' (vrh, vrhica), ki se pojavlja kot del kompozitnega ledinskega imena 'Einhart mit Gypfel' (ena hrastovina z vrhom)", source: "DWB (Grimm), Schmeller, Bayerisches Wörterbuch", confidence: "~" }, { candidate: "Gypf.", glossSi: "Okrajšava za 'Gypfel' (vrh), dokumentirana v uradnih dokumentih franciscejskega katastra kot skrajšana obrazna oblika", source: "AUSWEIS über die Benützungsart des Bodens (PV, 10. 1. 1825)", confidence: "~" }] },
      { id: "AHN", pairs: 13, variants: {"Ahn": 13}, distinctVariants: 1, stablePairs: 0, fallbackPairs: 0, variantPairs: 0, noCounterpart: 13, block: { pages: [48], distinctPages: 1, contiguousRuns: 2, parcelRange: [906, 920] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Ahn", glossSi: "Ledinsko ime za polje ali travnik, verjetno povezano z zeliščem 'ajna' (Allium) ali s terenom ob reki 'ah' (voda)", source: "SSKJ", confidence: "~" }] },
      { id: "AEFLING", pairs: 13, variants: {"Äfling": 13}, distinctVariants: 1, stablePairs: 0, fallbackPairs: 0, variantPairs: 0, noCounterpart: 13, block: { pages: [64], distinctPages: 1, contiguousRuns: 4, parcelRange: [1821, 1840] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Äfling", glossSi: "ledinsko ime, verjetno nemškega izvora, ki se nanaša na parcelo ali območje v občini Griblje", source: "neznano — hipoteza brez dokumentiranega vira", confidence: "~" }, { candidate: "Öfling", glossSi: "ledinsko ime, morda povezano z nemško besedo 'Öde' (neporaščen, opuščen) in pomeni 'puščava' ali 'neporaščeno območje'", source: "DWB (Grimm), Band 13, Spalte 1505", confidence: "~" }, { candidate: "Afling", glossSi: "ledinsko ime, morda povezano z nemško besedo 'Aue' (rečna naplavna ravan) in pomeni 'poplavno območje'", source: "DWB (Grimm), Band 1, Spalte 748", confidence: "?" }] },
      { id: "GUETEN", pairs: 12, variants: {"Güten": 11, "Gütung": 1}, distinctVariants: 2, stablePairs: 0, fallbackPairs: 0, variantPairs: 0, noCounterpart: 12, block: { pages: [17, 48], distinctPages: 2, contiguousRuns: 6, parcelRange: [283, 908] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Güten/Gütung", glossSi: "Ledinsko ime, morda povezano s slovanskim korenom 'gut' (dobro) ali nemškim 'gut' (dobrih, dobrega)", source: "SSKJ", confidence: "?" }, { candidate: "Güten", glossSi: "Ledinsko ime, verjetno izpeljano iz nemške besede 'Gut' (posest, kmetija), ki v tem kontekstu označuje posestvo ali zemljišče v lasti kmetije.", source: "DWB (Deutsches Wörterbuch, Grimm), 'Gut'", confidence: "?" }, { candidate: "Gütung", glossSi: "Pomanjševalna ali narečna oblika 'Güten', ki bi lahko pomenila 'majhno posestvo' ali 'del kmetije' v belokranjskem narečnem okolju.", source: "Kärntner Wörterbuch (Schulz, 1972)", confidence: "?" }] },
      { id: "ERDAR", pairs: 10, variants: {"Achm": 4, "Achat": 1, "Eidar": 1, "Erdar": 4}, distinctVariants: 4, stablePairs: 0, fallbackPairs: 5, variantPairs: 0, noCounterpart: 5, block: { pages: [23, 83], distinctPages: 2, contiguousRuns: 6, parcelRange: [168, 420] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Achm/Achat", glossSi: "ledinsko ime za njivo, ki je dokumentirano v Beli krajini; morebita krajšava ali dialektna oblika besede 'Acker' (njiva)", source: "SSKJ", confidence: "~" }, { candidate: "Eidar/Erdar", glossSi: "ledinsko ime za njivo, verjetno dialektna oblika slovenske besede 'jedar' (njiva, posest) ali 'erdar' (zemlja, posest)", source: "SSKJ", confidence: "?" }, { candidate: "Achm/Eidar/Erdar", glossSi: "Ledinsko ime polja v Beli krajini, zapisano v nemški Kurrent pisavi. Pojavlja se v stolpcu rabe kot specifična oznaka za parcelo, ki ni uradna kategorija.", source: "Bezlaj, France. 1976-1978. Slovar slovenskih narečij. Zv. 1-4. Ljubljana: SAZU.", confidence: "?" }] },
      { id: "DINGF", pairs: 10, variants: {"Dingf": 10}, distinctVariants: 1, stablePairs: 10, fallbackPairs: 0, variantPairs: 0, noCounterpart: 0, block: { pages: [83], distinctPages: 1, contiguousRuns: 5, parcelRange: [161, 177] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Dingf", glossSi: "Ledinsko ime, ki najverjetneje označuje posebno parcelo ali območje. Pojavlja se v stolpcu rabe, kar kaže, da gre za ime zemljiščne enote ali posebnega dela zemljišča, ne pa za splošno kulturo.", source: "neznano — hipoteza brez dokumentiranega vira", confidence: "?" }, { candidate: "Tingf", glossSi: "Mogoče povezano z nemško besedo 'Ding' (stvar, predmet) ali 'Ting' (zbor, sodišče), vendar to ni dokumentirano v kontekstu zemljiščnih imen.", source: "neznano — hipoteza brez dokumentiranega vira", confidence: "?" }, { candidate: "Ding", glossSi: "Nemška beseda 'Ding' pomeni 'stvar' ali 'predmet', vendar ni dokumentirano v kontekstu zemljiščnih imen ali rabe zemljišč.", source: "DWB (Grimm)", confidence: "~" }] },
      { id: "LUKIG", pairs: 10, variants: {"Lukig": 10}, distinctVariants: 1, stablePairs: 0, fallbackPairs: 0, variantPairs: 0, noCounterpart: 10, block: { pages: [59], distinctPages: 1, contiguousRuns: 7, parcelRange: [1121, 1141] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Lukig", glossSi: "Ledinsko ime za polje ali travnik v Beli krajini, verjetno povezano z osebnim imenom Luka ali podobno", source: "SSKJ (Slovenski slovar knjižnega in književnega jezika)", confidence: "~" }, { candidate: "Luckig", glossSi: "Narečna oblika nemške besede 'Luch' (močvirje, barje), ki je v Beli krajini pogost izposojenica", source: "Schmeller, Johann Andreas. Bayerisches Wörterbuch. München: C.H. Beck, 1827–1837", confidence: "?" }] },
      { id: "LHIZ", pairs: 9, variants: {"Lhize": 7, "Lhizl": 2}, distinctVariants: 2, stablePairs: 0, fallbackPairs: 9, variantPairs: 0, noCounterpart: 0, block: { pages: [58], distinctPages: 1, contiguousRuns: 6, parcelRange: [1103, 1120] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Lhize/Lhizl", glossSi: "Ledinsko ime, verjetno povezano s slovnično obliko 'liza' (majhen travnik, njiva v gozdu ali ob njem)", source: "SSKJ", confidence: "~" }] },
      { id: "LOHGARN", pairs: 7, variants: {"Lohgarn": 7}, distinctVariants: 1, stablePairs: 0, fallbackPairs: 0, variantPairs: 0, noCounterpart: 7, block: { pages: [29], distinctPages: 1, contiguousRuns: 3, parcelRange: [527, 539] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Lohgarn", glossSi: "ledinsko ime za parcelo, verjetno sestavljeno iz nemškega 'Loh' (mokro, močvirnato območje) in 'Garn' (morda pridevnik 'kolen', 'kolenast', ali pa gre za krajevni pridevnik)", source: "neznano — hipoteza brez dokumentiranega vira", confidence: "~" }, { candidate: "Logarn", glossSi: "ledinsko ime, izpeljano iz slovanskega 'log' (dolina, gozdna dolina), s pripono '-arn', ki je v slovenščini pogosta za označevanje krajev", source: "SSKJ", confidence: "?" }, { candidate: "Lochgarn", glossSi: "ledinsko ime, nemškega izvora, kjer 'Loch' pomeni 'luknja' ali 'odprtina', kar bi lahko označevalo obliko zemljišča", source: "DWB (Grimm)", confidence: "?" }] },
      { id: "HURGI", pairs: 5, variants: {"Hurgi": 5}, distinctVariants: 1, stablePairs: 0, fallbackPairs: 0, variantPairs: 0, noCounterpart: 5, block: { pages: [46], distinctPages: 1, contiguousRuns: 3, parcelRange: [866, 879] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Hurgi", glossSi: "Ledinsko ime, morda povezano z zemljiščem, ki je bilo last družine Hurgi ali ima podobno ime", source: "neznano — hipoteza brez dokumentiranega vira", confidence: "?" }, { candidate: "Horgi", glossSi: "Narečna oblika, morda povezana z besedo 'horga' (mladina, poganek) ali 'horgati' (delati, delati po domače)", source: "SSKJ", confidence: "~" }, { candidate: "Hurki", glossSi: "Morda pomanjševalnica ali narečna oblika, povezana z besedo 'hurkati' (delati hitro, brez premišljevanja)", source: "Bezlaj", confidence: "?" }] },
      { id: "WING", pairs: 3, variants: {"Wing": 3}, distinctVariants: 1, stablePairs: 0, fallbackPairs: 0, variantPairs: 3, noCounterpart: 0, block: { pages: [60], distinctPages: 1, contiguousRuns: 1, parcelRange: [1147, 1149] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Wing", glossSi: "Ledinsko ime za travnik ali pašnik, verjetno v obliki 'Ving' ali 'Vinga', ki bi lahko predstavljal krajevni toponim", source: "SSKJ", confidence: "~" }, { candidate: "Grieng", glossSi: "Zapisano kot 'Grieng' v nasprotnem branju, kar bi lahko predstavljalo narečno obliko 'Gring' ali 'Grinja' za travnato območje", source: "Bezlaj, Slovenski narečni atlas", confidence: "?" }] },
      { id: "SCHINDEL", pairs: 1, variants: {"Schindel": 1}, distinctVariants: 1, stablePairs: 0, fallbackPairs: 1, variantPairs: 0, noCounterpart: 0, block: { pages: [120], distinctPages: 1, contiguousRuns: 1, parcelRange: [2350, 2350] }, termTypeHypothesis: "LEDINSKO-IME", topHypotheses: [{ candidate: "Schindel", glossSi: "Ledinsko ime, ki se nanaša na območje pokrito s šindri (lesena kritina), kar je pogosto v Beli krajini, kjer so bile hiše pokrite s šindrami", source: "SSKJ - Slovenski slovar knjižnega jezika", confidence: "~" }, { candidate: "Šindel", glossSi: "Slovenska beseda za šindro (leseno kritino), ki bi lahko bila zapisana nemško kot 'Schindel' v nemških dokumentih, vendar je v tem kontekstu verjetno ledinsko ime", source: "SSKJ - Slovenski slovar knjižnega jezika", confidence: "~" }, { candidate: "Sindel", glossSi: "Narečna varianta besede 'šindel', ki bi lahko obstajala v belokranjskem narečju, zapisana v nemški obliki", source: "Bezlaj, France: Slovenski narečni atlas, 1. knjiga", confidence: "?" }] },

  ],
  singles: {
    pairs: 66,
    distinctRaw: 42,
    fallbackPairs: 10,
    noteSi:
      "kitice (posamezne neznane vrednosti, 42 različnih) — 10 padcev (pass1 generik namesto specifične besede); večina verjetno okrni ali odmašinet prebrani obliki znanih terminov (Einfach≈Einschlag?, Eibn, Abm …)",
  },
  pvReconciliation: {
    pvOfficial: {
      Gemuese_Gaerten: { joch: 2, klafter: 123, jochF: 2.08 },
      Wein_Gaerten: { joch: 7, klafter: 665, jochF: 7.42 },
      Wiesen: { joch: 76, klafter: 1480, jochF: 76.93 },
      Wiesen_mit_Obstbaeumen: { joch: 12, klafter: 328, jochF: 12.21 },
      Weiden: { joch: 636, klafter: 263, jochF: 636.16 },
      Aecker: { joch: 413, klafter: 870, jochF: 413.54 },
      Oedungen: { joch: 1, klafter: 476, jochF: 1.3 },
      Fluesse_oder_Baeche: { joch: 21, klafter: 142, jochF: 21.09 },
      Weg_Parzellen: { joch: 46, klafter: 1127, jochF: 46.7 },
      Bau_Parzellen: { joch: 4, klafter: 889, jochF: 4.56 },
      Partial_Sum: { joch: 1148, klafter: 539, jochF: 1148.34 },
      Second_Section_Sum: { joch: 73, klafter: 1024, jochF: 73.64 },
      Grand_Total: { joch: 1221, klafter: 1513, jochF: 1221.95 },
    },
    psClassAreasJ: {
      NJIVA: 615.83,
      TRAVNIK: 271.25,
      TOPONIM: 81.23,
      GOZD: 76.79,
      NEKLASIFICIRANO: 96.68,
      ARTIFAKT: 256.49,
      NEROD: 30.28,
      STAVBNO: 29.25,
      ALM: 24.68,
      VRT: 20.62,
      OBCINA: 19.38,
      PASTVISCE: 35.25,
      VINOGRAD: 6.95,
      VODA: 0.09,
      CESTA: 0.02,
    },
    weidenGapJ: 576.24,
    psPastVisceAlmJ: 59.92,
    unknownFamiliesAreaJ: 96.68,
    njivaVsAeckerDeltaJ: 202.29,
    travnikVsWiesenDeltaJ: 182.12,
    vrtVsGemueseDeltaJ: 18.54,
    vinogradVsWeinDeltaJ: -0.46,
    rowsModelTotalJ: 1564.78,
    pvTotalJ: 1221.95,
    rowsModelVsPvTotalJ: 342.84,
  },
  verdictSi:
    "16 neznanih družin (216 parov) + 66 kitic: 13/16 družin vezanih na ENO fotografijo s teki sosednjih parcel → hipoteza LEDINSKO IME; DINGF edina 100 % stabilna beseda (10/10); generični padcek (pass1 Wiese/Acker, pass2 specifično): LHIZ 9/9, ERDAR 5/5, SCHINDEL 1/1 — specifične besede so v viru; PV Area 1221|1513 ≈ P41 1220|1493 (Δ 0,05 %) in VINOGRAD Δ −0,46 J; WEIDEN-GAP 576,24 J neznane družine pokrijejo le v 17 % — preostanek v presežkih NJIVA/TRAVNIK; rabe NI prirejena — vse ostaja NEKLASIFICIRANO (hipoteze za človeško paleografijo, viri stroja NEPREVERJENI)",
  verdictEn:
    "16 unknown families (216 pairs) + 66 strays: 13/16 families bound to ONE photo with contiguous parcel runs → FIELD-NAME hypothesis; DINGF the only 100% stable word (10/10); generic fallback (pass1 Wiese/Acker, pass2 specific): LHIZ 9/9, ERDAR 5/5, SCHINDEL 1/1 — the specific words ARE in the source; PV Area 1,221|1,513 ≈ P41 1,220|1,493 (Δ 0.05%) and VINEYARD Δ −0.46 J; the WEIDEN-GAP of 576.24 J is covered by unknown families in only 17% — the remainder sits in NJIVA/TRAVNIK surpluses; no use was reassigned — everything remains UNCLASSIFIED (hypotheses for human palaeography, machine-attributed sources UNVERIFIED)",
  next: [
    "človeška paleografija 16 družin + kitic (3. prehod dvoumnih strani, ko VAČ dosegljiv)",
    "verifikacija leksikografskih virov (Schmeller/DWB/SSKJ/Bezlaj) — viri navaja stroj",
    "PV razlage presežkov NJIVA/TRAVNIK (ali kulturni stolpec meša rabo z ledinskimi imeni?)",
    "semantika 7 par referenc (razcep K1/K2 razrešen v P44)",
  ],
};

/** P44 (issue #10) — razcep K1/K2 v "Abschluß der Gemeinde" — RAZREŠEN [~]. */
export const PS_K1K2_P44: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  constraint: { derivation: string; value: number };
  readingInventory: {
    k1Cell: { passes: Record<string, number>; visual: string; consensusTail: string; note: string };
    k2Cell: { passes: Record<string, number>; visual: string; consensusTail: string; note: string };
  };
  resolution: {
    state: string;
    confidence: string;
    k1: number;
    k2: number;
    row1: string;
    row2: string;
    basis: string[];
    humanConfirmation: string;
  };
  hypotheses: { id: string; pair: number[]; accepted: boolean; reasons: string[]; rejection: string | null }[];
  identities: Record<string, { pass: boolean; detail: string }>;
  impact: {
    abschlussNowFullyClosed: boolean;
    newIdentity: string;
    gemeindeStructure: string;
    replacesP41Note: string;
  };
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "PS",
  source:
    "N083PS.pdf (VAČ uodid 373415, docid 41780) — str. 140 desno 'Abschluß der Gemeinde' (rdeči tuš); committed dokazi ps-recap-paleo.json + ps-recap-paleo-raw/pass{1,2,3}-page140.json; polni izpis research/issue17/ps-k1k2.json + src/data/atlas/ps-k1k2.json",
  status: "REVIEW",
  generatedBy: "scripts/p44_ps_k1k2.py",
  constraint: {
    derivation:
      "Summe der Grundparzellen 1215|490 − (Grund 831 J + Zinsb 383 J) = 1214 J + 490 K → K1+K2 = 1600 + 490 = 2090 K",
    value: 2090,
  },
  readingInventory: {
    k1Cell: {
      passes: { pass1: 968, pass2: 468, "pass3-shifted": 468 },
      visual: "9?8 → kandidati 968/998/908",
      consensusTail: "68 (0→6, 2→8)",
      note:
        "prava vrednost 702 NI bila nikoli direktno prebrana — pride iz strukturnega sidra; pričakovana sistematična napačna branja (7→9|4, 0→6, 2→8) se ujemajo z opaženimi [~]",
    },
    k2Cell: {
      passes: { pass1: 1288, pass2: 1388, pass3: 1288 },
      visual: "kandidati 1122/1092/1182",
      consensusTail: "88",
      note: "prava vrednost 1388 == branje pass2; p1/p3 se razlikujeta le v 2. števki",
    },
  },
  resolution: {
    state: "RESOLVED-ARITMETIČNO",
    confidence: "~",
    k1: 702,
    k2: 1388,
    row1: "831|702 (== leva 'Summa der Grundparzellen')",
    row2: "383|1388",
    basis: [
      "omejitev K1 + K2 = 2090 K (iz 831+383+1 = 1215 J in 490 K)",
      "paralelnost 'nach Anlage': desna vrstica 4 (3|312) == leva vrstica 132 (3|312) — P41 identiteta d_abschlussBaup PASS; po istem vzorcu vrstica 1 == leva vsota 831|702 (Joch 831 == 831)",
      "K2 = 1388 je direktno VLM branje pass2; p1/p3 branja 1288 se razlikujejo le v eni števki",
      "podmnožinski argument: 831|968 (H2) bi presegel vsoto Anlage 831|702 pri istem Joch — nemogoče",
    ],
    humanConfirmation:
      "ostaja odprta — rešitev je aritmetično vsiljena, paleografska potrditev celice K1 (ali '702' ali '9?8') je še vedno zaželena",
  },
  hypotheses: [
    {
      id: "H1",
      pair: [702, 1388],
      accepted: true,
      reasons: [
        "strukturno sidro: 'nach Anlage' rekapitulira levo vsoto — desna vrstica 4 (Baup 3|312) == leva vrstica 132 (3|312) [P41 PASS]; po istem vzorcu vrstica 1 (Grund 831|K1) == leva 'Summa der Grundparzellen' 831|702; Joch 831 == 831",
        "K2 = 2090 − 702 = 1388 je DIREKTNO VLM branje K2 celice (pass2); p1/p3 bereta 1288 — razlika le v 2. števki (3↔2)",
        "omejitev K1+K2 = 2090 izpolnjena natanko",
        "konsenz repa K2 celice je '1?88' — 1388 se ujema, alternativni vizualni kandidati (1122/1092/1182) ne",
        "celoten Abschluß se aritmetično zapre: 831|702 + 383|1388 = 1215|490; + 5|1003 = 1220|1493",
      ],
      rejection: null,
    },
    {
      id: "H2",
      pair: [968, 1122],
      accepted: false,
      reasons: [
        "K1 = 968 je branje pass1; K2 = 1122 je le vizualni kandidat (noben prehod ni prebral 1122)",
        "KRŠI paralelnost nach Anlage: 831|968 > 831|702 pri istem Joch — rekapitulacija Anlage ne sme presegati vsote Anlage (podmnožina > nadmnožina, nemogoče)",
      ],
      rejection: "kršitev strukturne paralelnosti (podmnožina ne more presegati nadmnožine) + K2 brez prehodnega branja",
    },
    {
      id: "H3",
      pair: [998, 1092],
      accepted: false,
      reasons: [
        "oba kandidata sta le vizualni razširitvi (998 iz '9?8', 1092 iz vizualnega branja K2)",
        "noben prehod ni prebral niti 998 niti 1092; brez strukturnega sidra",
      ],
      rejection: "brez prehodnih branj in brez strukturnega sidra",
    },
    {
      id: "H4",
      pair: [908, 1182],
      accepted: false,
      reasons: [
        "oba kandidata sta le vizualni razširitvi (908 iz '9?8', 1182 iz vizualnega branja K2)",
        "noben prehod ni prebral niti 908 niti 1182; brez strukturnega sidra",
      ],
      rejection: "brez prehodnih branj in brez strukturnega sidra",
    },
    {
      id: "H5",
      pair: [468, 1622],
      accepted: false,
      reasons: [
        "K1 = 468 je branje pass2 (pass3 zamaknjeno)",
        "K2 = 1622 > 1600 K — anomalija za stolpec Klafter; brez opore v prehodih",
      ],
      rejection: "K2 > 1600 K je anomalija + brez opore v prehodih",
    },
  ],
  identities: {
    I1_lageRowSum: { pass: true, detail: "7 vrstic == 831|702 (rekonstruirano)" },
    I2_leftClosure: { pass: true, detail: "831|702 + 3|312 == 834|1014" },
    I3_constraint: { pass: true, detail: "K1+K2 = 2090 K" },
    I4_nachAnlageParallel: { pass: true, detail: "desna 4 (3|312) == leva 132 (3|312); Joch 831 == 831" },
    I5_solution: { pass: true, detail: "K1=702==Klafter leve vsote; K2=1388==branje pass2; oba < 1600" },
    I6_fullClosure: {
      pass: true,
      detail: "831|702 + 383|1388 == 1215|490; + 5|1003 == 1220|1493; 3|312 + 2|691 == 5|1003",
    },
    I7_uniqueness: { pass: true, detail: "natanko ena sprejeta hipoteza (H1); H2–H5 zavrnjene z izrecnimi razlogi" },
  },
  impact: {
    abschlussNowFullyClosed: true,
    newIdentity:
      "desna vrstica 1 (831|702) == leva 'Summa der Grundparzellen' — NOVA identiteta (poleg P41 d_abschlussBaup)",
    gemeindeStructure:
      "Grundparzellen občine 1215|490 = rustikalne hiše po Anlagi 831|702 (hiše 124–130) + 'Ziffer 1041' (Gütl/gingl. kategorija) 383|1388",
    replacesP41Note:
      "P41 vrstici 831|968[~] in 383|1288[~] se nadomestita z 831|702 in 383|1388 [~]",
  },
  verdictSi:
    "RAZCEP K1/K2 RAZREŠEN [~]: K1 = 702 (strukturna paralelnost 'nach Anlage' — desna vrstica 4 == leva vrstica 132; Joch 831 == 831; hipoteza 968 pade, ker rekapitulacija Anlage ne sme presegati vsote Anlage), K2 = 2090 − 702 = 1388 (direktno branje pass2; p1/p3 1288 — razlika ena števka). Celoten Abschluß se aritmetično zapre: 831|702 + 383|1388 = 1215|490; + 5|1003 = 1220|1493. NOVA identiteta: desna vrstica 1 == leva 'Summa der Grundparzellen'. Struktura občine: rustikalne hiše 831|702 + 'Ziffer 1041' (Gütl/gingl.) 383|1388. Človeška paleografska potrditev ostaja odprta.",
  verdictEn:
    "K1/K2 SPLIT RESOLVED [~]: K1 = 702 (structural 'nach Anlage' parallelism — right row 4 == left row 132; Joch 831 == 831; the 968 hypothesis falls because a recapitulation of the Anlage cannot exceed the Anlage's own sum), K2 = 2090 − 702 = 1388 (a direct pass2 reading; p1/p3 read 1288 — one digit apart). The entire Abschluß closes arithmetically: 831|702 + 383|1388 = 1215|490; + 5|1003 = 1220|1493. NEW identity: right row 1 == left 'Summa der Grundparzellen'. Gemeinde structure: rustical houses 831|702 + 'Ziffer 1041' (Gütl/gingl.) 383|1388. Human palaeographic confirmation remains open.",
  next: [
    "človeška paleografska potrditev celic K1/K2 (3. prehod, ko VAČ dosegljiv)",
    "semantika 7 par referenc str. 141 — še UNRESOLVED",
    "p141 spodnji vsotni blok (ŠIBKO), p142 skupna dolžina (UNRESOLVED)",
  ],
};

/** P45 (issue #10) — verifikacija leksikografskih virov P43 leksikona: 49 tarč, 0/70 potrjenih v celoti. */
export const PS_LEXICON_VERIFIED_P45: {
  series: "PS";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  method: { aggregation: string; unchangedP43: string };
  campaign: {
    targetsTotal: number;
    byVerdict: Record<string, number>;
    byMethod: Record<string, number>;
    hypothesesTotal: number;
  };
  families: {
    id: string;
    pairs: number;
    verdictCounts: Record<string, number>;
    topHypotheses: { candidate: string; source: string; verdict: string; confidence: string; noteSi: string; url: string | null }[];
  }[];
  keyFindingsSi: string[];
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "PS",
  source:
    "N083PS.pdf (VAČ uodid 373415, docid 41780; 143 strani) — verifikacijski sloj nad committed ps-lexicon.json (P43): adjudikacija 49 tarč (research/issue17/lexicon-verification-adjudication.json) + raw dokazi lexicon-verification-raw/ (fran.si geselni izseki SSKJ²/Pleteršnik/Novak SSP, Wikipedia API zvezčne mape DWB 33 zvezkov + Schmellerjeve izdaje + bibliografija, api-availability-log); polni izpis research/issue17/ps-lexicon-verified.json + src/data/atlas/ps-lexicon-verified.json",
  status: "REVIEW",
  generatedBy: "scripts/p45_lex_verify.py",
  method: {
    aggregation:
      "NEPOTRJENO dominira; sicer POTRJENO; sicer DELNO; sicer NEVERIFIKATORNO; brez tarč = BREZ-VIRA (NEPOTRJENO = vir preverjen in NE podpira: geslo manjka, pomen drugačen, atribucija/zvezek/citat ne stoji)",
    unchangedP43:
      "kandidat/glosa/vir/zaupanje bajtno identični ps-lexicon.json (invarianta I2) — nič ne spreminja P43 hipotez ali rabe (vse ostaja NEKLASIFICIRANO)",
  },
  campaign: {
    targetsTotal: 49,
    byVerdict: { POTRJENO: 0, DELNO: 7, NEPOTRJENO: 33, NEVERIFIKATORNO: 17, "BREZ-VIRA": 13 },
    byMethod: { "fran.si-direct": 18, "wikipedia-api": 14, "deterministic-repo": 1, unreachable: 16 },
    hypothesesTotal: 70,
  },
  families: [
    { id: "LHUT-JEDRO", pairs: 36, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 1, NEVERIFIKATORNO: 1, "BREZ-VIRA": 1 }, topHypotheses: [{ candidate: "Lhuta/Lhupa", source: "SSKJ, Slovenski slovar knjižnega jezika", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ² 'lúti' = hud/jezen/divji; Pleteršnik 'lúta' = Nachlese. Pomena 'lȕt = močvirnato območje' NI v SSKJ — trditev LHUT-JEDRO#2 ne stoji.", url: "https://fran.si/iskanje?View=1&Query=luta" }, { candidate: "Lhut/Lhup/Lhupf", source: "Bezlaj, France. Slovenski etimološki slovar.…", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "ESSJ bibliografsko POTRJEN, a leta '1976–2008' (LHUT-JEDRO#1) so natančneje '1976–2005' (knjiga 4/5: 2005). Gesla lȕh/lǫg so v tiskani izdaji — v peskovniku nedostopna; potrjena je le bibliografija, ne vsebina.", url: "https://sl.wikipedia.org/wiki/France_Bezlaj" }, { candidate: "Lhut/Lhup/Lhupf/Lhuta", source: "neznano — hipoteza brez dokumentiranega vira", verdict: "BREZ-VIRA", confidence: "—", noteSi: "", url: null }] },
    { id: "LOHN-RAUT", pairs: 29, verdictCounts: { POTRJENO: 0, DELNO: 1, NEPOTRJENO: 5, NEVERIFIKATORNO: 0, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Lohn (nem.)", source: "DWB (Deutsches Wörterbuch von Jacob und…", verdict: "NEPOTRJENO", confidence: "~", noteSi: "STRUKTURNA preverba citata: 'Band 16, Spalte 844' NE more vsebovati gesla Lohn (L je v Bd 12: l, m; Bd 16 pokriva seeleben–sprechen). Citat zvezka je napačen; vsebina gesla (Sp. 844) v peskovniku nepreverjena.", url: "https://de.wikipedia.org/wiki/Deutsches_W%C3%B6rterbuch" }, { candidate: "Log (slov.)", source: "SSKJ (Slovar slovenskega knjižnega jezika)", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ² log = močviren travnik ob vodi, porasel z drevesi — NE 'dolina/grapa/splav lesnih delcev' (LOHN-RAUT#1) in NE 'nižina, dolina' (#5). Pleteršnik lǫ̨g = 'der Hain, der niedere Wald'. Trditvi hipotez sta v neskladju z geslom.", url: "https://fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/4491704/log" }, { candidate: "Lohn (slov. narečno)", source: "Kärntner Wörterbuch, Band 4, Seite 312", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'Kärntner Wörterbuch (Schulz, 1972)' NI potrjeno: de.wiki (Kranzmayer) navaja WBÖ (Kranzmayer urednik od 1958), samostojnega 'Kärntner Wörterbuch avtorja Schulz' ni dokumentirano. Citat 'Band 4, Seite 312' (LOHN-RAUT#3) ostaja brez…", url: "https://de.wikipedia.org/wiki/Eberhard_Kranzmayer" }] },
    { id: "LHOPI-LOHIFA", pairs: 23, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 3, NEVERIFIKATORNO: 3, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Lhopi/Luppa", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ² log = močviren travnik ob vodi, porasel z drevesi — NE 'dolina/grapa/splav lesnih delcev' (LOHN-RAUT#1) in NE 'nižina, dolina' (#5). Pleteršnik lǫ̨g = 'der Hain, der niedere Wald'. Trditvi hipotez sta v neskladju z geslom. ·…", url: "https://fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/4491704/log" }, { candidate: "Luppa", source: "Kärntner Wörterbuch", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'Kärntner Wörterbuch (Schulz, 1972)' NI potrjeno: de.wiki (Kranzmayer) navaja WBÖ (Kranzmayer urednik od 1958), samostojnega 'Kärntner Wörterbuch avtorja Schulz' ni dokumentirano. Citat 'Band 4, Seite 312' (LOHN-RAUT#3) ostaja brez…", url: "https://de.wikipedia.org/wiki/Eberhard_Kranzmayer" }, { candidate: "Schliffa", source: "Pleteršnik", verdict: "NEPOTRJENO", confidence: "~", noteSi: "Pleteršnik ne pozna 'šlifa' — LHOPI-LOHIFA#4 (Schlif = brus) nima opore v navedenem viru. · Razširitev tarče pletersnik-slifa: Pleteršnik celoten dostopen na fran.si (dict 136) — 'šlifa' ni v njem.", url: "https://fran.si/iskanje?View=1&Query=šlifa" }] },
    { id: "EINSCHLAG-GUELZE", pairs: 20, verdictCounts: { POTRJENO: 0, DELNO: 1, NEPOTRJENO: 1, NEVERIFIKATORNO: 2, "BREZ-VIRA": 1 }, topHypotheses: [{ candidate: "Poggi", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'Poggi' (italski izraz za hribe) v SSKJ ne obstaja — EINSCHLAG-GUELZE#4 ne stoji.", url: "https://fran.si/iskanje?View=1&Query=poggi" }, { candidate: "Gülze", source: "SSKJ", verdict: "DELNO", confidence: "~", noteSi: "Gesla obstajata: golica = posekana strmina nad gozdno mejo, golec = gol hrib — splošna povezava EINSCHLAG-GUELZE#1 z 'Golica/Golec' je delno opora (posek/gola strmina), izrecni pomen 'njiva' pa ni dokumentiran.", url: "https://fran.si/iskanje?View=1&Query=golica" }, { candidate: "Einschlag", source: "DWB (Grimm)", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "DWB nedosegljiv; trditev 'Einschlag = sekundarna/mlada goščava' (EINSCHLAG-GUELZE#2) ne preverjena. Za človeško preverbo.", url: "https://www.woerterbuchnetz.de/DWB?lemma=Einschlag" }] },
    { id: "EINHART", pairs: 15, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 4, NEVERIFIKATORNO: 2, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Einhart", source: "SSKJ, Bezlaj, Toporišič", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'Einhart' v SSKJ ne obstaja; 'ena hrastovina' je neodprta ad hoc etimologija — EINHART#0/#4 ne stojita v navedenih virih.", url: "https://fran.si/iskanje?View=1&Query=einhart" }, { candidate: "Gypf.", source: "AUSWEIS über die Benützungsart des Bodens…", verdict: "NEPOTRJENO", confidence: "~", noteSi: "EINHART#2 trdi, da je okrajšava 'Gypf.' dokumentirana v PV (Nutzungs-Ausweis 1825) — PV.json je ne vsebuje. Okrajšava JE v PS registru samem (tudi 'Gypfang' — dodatna oblika!). Citat vira napačen; dejstvo premaknjeno na pravo mesto…", url: "research/issue17/PV.json" }, { candidate: "mit", source: "Schmeller, Bayerisches Wörterbuch", verdict: "NEPOTRJENO", confidence: "~", noteSi: "EINHART#3 ('predloga mit povezuje kompozitno ledinsko ime') NI leksikografska geselna trditev — Schmeller ni slovar predlog; citirani vir trditve ne podpira. Digitalizati Schmellerja so sicer bibliografsko potrjeni (bavarikon/MDZ/BAdW…", url: "https://de.wikipedia.org/wiki/Johann_Andreas_Schmeller" }] },
    { id: "AHN", pairs: 13, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 1, NEVERIFIKATORNO: 0, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Ahn", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ ne pozna 'ajna'; najbližje je 'ajda' (Buchweizen). Povezava Ahn↔'ajna (Allium)' ni dokumentirana.", url: "https://fran.si/iskanje?View=1&Query=ajna" }] },
    { id: "AEFLING", pairs: 13, verdictCounts: { POTRJENO: 0, DELNO: 3, NEPOTRJENO: 2, NEVERIFIKATORNO: 0, "BREZ-VIRA": 1 }, topHypotheses: [{ candidate: "Hofling", source: "DWB (Grimm), Band 13, Spalte 742", verdict: "NEPOTRJENO", confidence: "~", noteSi: "STRUKTURNA preverba: 'Band 13, Spalte 742' NE more vsebovati gesla Höfling (H je v Bd 10: h, i, j; Bd 13 = n, o, p, q). Citat zvezka napačen.", url: "https://de.wikipedia.org/wiki/Deutsches_W%C3%B6rterbuch" }, { candidate: "Efling", source: "DWB (Grimm), Band 6, Spalte 102", verdict: "NEPOTRJENO", confidence: "~", noteSi: "STRUKTURNA preverba: 'Band 6, Spalte 102' NE more vsebovati gesla Efeu (E je v Bd 3: e–forsche; Bd 6 = getreide–gewöhniglich). Citat zvezka napačen.", url: "https://de.wikipedia.org/wiki/Deutsches_W%C3%B6rterbuch" }, { candidate: "Öfling", source: "DWB (Grimm), Band 13, Spalte 1505", verdict: "DELNO", confidence: "~", noteSi: "STRUKTURNO skladno: O res je v DWB Bd 13 — 'Band 13, Spalte 1505' (AEFLING#1) je zvezčno možen; vsebina gesla (Öde) v peskovniku nepreverjena.", url: "https://de.wikipedia.org/wiki/Deutsches_W%C3%B6rterbuch" }] },
    { id: "GUETEN", pairs: 12, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 3, NEVERIFIKATORNO: 1, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Güten/Gütung", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ ne pozna 'guten' — GUETEN#0 ('slovanski koren gut (dobro)') se na SSKJ ne more opreti.", url: "https://fran.si/iskanje?View=1&Query=guten" }, { candidate: "Gütung", source: "Kärntner Wörterbuch (Schulz, 1972)", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'Kärntner Wörterbuch (Schulz, 1972)' NI potrjeno: de.wiki (Kranzmayer) navaja WBÖ (Kranzmayer urednik od 1958), samostojnega 'Kärntner Wörterbuch avtorja Schulz' ni dokumentirano. Citat 'Band 4, Seite 312' (LOHN-RAUT#3) ostaja brez…", url: "https://de.wikipedia.org/wiki/Eberhard_Kranzmayer" }, { candidate: "Güten/Gütung", source: "SSKJ (Slovenski slovar knjižnega jezika)", verdict: "NEPOTRJENO", confidence: "~", noteSi: "Geslo 'trava' obstaja, a veriga GUETEN#3 ('Güten ← trava preko nemškega vpliva') ni dokumentirana nikjer — obstoj gesla ne podpira trditve.", url: "https://fran.si/iskanje?View=1&Query=trava" }] },
    { id: "ERDAR", pairs: 10, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 3, NEVERIFIKATORNO: 2, "BREZ-VIRA": 1 }, topHypotheses: [{ candidate: "Achm/Achat", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'jedar' v SSKJ/Pleteršniku NE obstaja — ERDAR#0/#1 se ne more opreti na SSKJ.", url: "https://fran.si/iskanje?View=1&Query=jedar" }, { candidate: "Achm/Eidar/Erdar", source: "Bezlaj, France. 1976-1978. Slovar slovenskih…", verdict: "NEPOTRJENO", confidence: "~", noteSi: "Atribucije 'Bezlaj, Slovar slovenskih narečij 1976–1978 Zv. 1–4' (ERDAR#2), 'Bezlaj, Slovenski narečni atlas' (WING#1) in 'Bezlaj … narečni atlas, 1. knjiga' (SCHINDEL#2) NE stojijo: v Bezlajevem seznamu del (sl.wiki) SSN in SLA…", url: "https://sl.wikipedia.org/wiki/France_Bezlaj" }, { candidate: "Achat", source: "DWB (Grimm, Jacob und Wilhelm). Deutsches…", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "DWB nedosegljiv; trditev 'Achat = okrajšava za Acker' (ERDAR#3) je neobičajna in ne preverjena.", url: "https://www.woerterbuchnetz.de/DWB?lemma=Acker" }] },
    { id: "DINGF", pairs: 10, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 1, NEVERIFIKATORNO: 1, "BREZ-VIRA": 4 }, topHypotheses: [{ candidate: "Dingb", source: "Kärntner Wörterbuch", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'Kärntner Wörterbuch (Schulz, 1972)' NI potrjeno: de.wiki (Kranzmayer) navaja WBÖ (Kranzmayer urednik od 1958), samostojnega 'Kärntner Wörterbuch avtorja Schulz' ni dokumentirano. Citat 'Band 4, Seite 312' (LOHN-RAUT#3) ostaja brez…", url: "https://de.wikipedia.org/wiki/Eberhard_Kranzmayer" }, { candidate: "Ding", source: "DWB (Grimm)", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "DWB nedosegljiv; Ding = stvar/zbor/sodišče je splošno znano, a v navedenem viru nepreverjeno.", url: "https://www.woerterbuchnetz.de/DWB?lemma=Ding" }, { candidate: "Dingf", source: "neznano — hipoteza brez dokumentiranega vira", verdict: "BREZ-VIRA", confidence: "—", noteSi: "", url: null }] },
    { id: "LUKIG", pairs: 10, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 2, NEVERIFIKATORNO: 0, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Lukig", source: "SSKJ (Slovenski slovar knjižnega in…", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ lúka = pristanišče; osebna imena SSKJ (splošni slovar) ne ureja. Trditev LUKIG#0 (osebno ime Luka) ni dokumentirana v navedenem viru.", url: "https://fran.si/iskanje?View=1&Query=luka" }, { candidate: "Luckig", source: "Schmeller, Johann Andreas. Bayerisches…", verdict: "NEPOTRJENO", confidence: "~", noteSi: "Bibliografska preverba atribucije LUKIG#1: 'München: C.H. Beck, 1827–1837' NE stoji — 1. izdaja je izšla pri Cotta (Stuttgart/Tübingen), ne pri C.H. Beck. Geslo 'Luch' v peskovniku nepreverjeno.", url: "https://de.wikipedia.org/wiki/Johann_Andreas_Schmeller" }] },
    { id: "LHIZ", pairs: 9, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 1, NEVERIFIKATORNO: 0, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Lhize/Lhizl", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ/Pleteršnik líza = 'kdor rad liže' (Lecker/Schmeichler) — NI 'majhen travnik/njiva v gozdu'. Trditev LHIZ#0 ne stoji v navedenem viru (LHIZ se sicer 9/9 vrača iz padca Wiese — kontekst travniški, a SSKJ 'liza' tega ne dokumentira).", url: "https://fran.si/iskanje?View=1&Query=liza" }] },
    { id: "LOHGARN", pairs: 7, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 1, NEVERIFIKATORNO: 3, "BREZ-VIRA": 1 }, topHypotheses: [{ candidate: "Logarn", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ² log = močviren travnik ob vodi, porasel z drevesi — NE 'dolina/grapa/splav lesnih delcev' (LOHN-RAUT#1) in NE 'nižina, dolina' (#5). Pleteršnik lǫ̨g = 'der Hain, der niedere Wald'. Trditvi hipotez sta v neskladju z geslom.", url: "https://fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/4491704/log" }, { candidate: "Lochgarn", source: "DWB (Grimm)", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "DWB nedosegljiv; trditev Loch = luknja/odprtina je trivna, a v navedenem viru nepreverjena.", url: "https://www.woerterbuchnetz.de/DWB?lemma=Loch" }, { candidate: "Ložgarn", source: "Bezlaj", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "ESSJ bibliografsko POTRJEN, a leta '1976–2008' (LHUT-JEDRO#1) so natančneje '1976–2005' (knjiga 4/5: 2005). Gesla lȕh/lǫg so v tiskani izdaji — v peskovniku nedostopna; potrjena je le bibliografija, ne vsebina.", url: "https://sl.wikipedia.org/wiki/France_Bezlaj" }] },
    { id: "HURGI", pairs: 5, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 2, NEVERIFIKATORNO: 1, "BREZ-VIRA": 3 }, topHypotheses: [{ candidate: "Horgi", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "SSKJ ne pozna horga/hurga/hurgati/hurkati — trditvi HURGI#1/#2 se na SSKJ ne moreta opreti.", url: "https://fran.si/iskanje?View=1&Query=horga" }, { candidate: "Orgi", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'orga' v pomenu 'kmečko vozilo' ni v SSKJ — HURGI#5 ne stoji.", url: "https://fran.si/iskanje?View=1&Query=orga" }, { candidate: "Hurki", source: "Bezlaj", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "ESSJ obstaja (tisk), geslo 'hurkati' nedostopno v peskovniku.", url: "https://sl.wikipedia.org/wiki/France_Bezlaj" }] },
    { id: "WING", pairs: 3, verdictCounts: { POTRJENO: 0, DELNO: 0, NEPOTRJENO: 2, NEVERIFIKATORNO: 0, "BREZ-VIRA": 0 }, topHypotheses: [{ candidate: "Wing", source: "SSKJ", verdict: "NEPOTRJENO", confidence: "~", noteSi: "'ving/Vinga' v SSKJ ne obstaja — WING#0 se na SSKJ ne more opreti.", url: "https://fran.si/iskanje?View=1&Query=ving" }, { candidate: "Grieng", source: "Bezlaj, Slovenski narečni atlas", verdict: "NEPOTRJENO", confidence: "~", noteSi: "Atribucije 'Bezlaj, Slovar slovenskih narečij 1976–1978 Zv. 1–4' (ERDAR#2), 'Bezlaj, Slovenski narečni atlas' (WING#1) in 'Bezlaj … narečni atlas, 1. knjiga' (SCHINDEL#2) NE stojijo: v Bezlajevem seznamu del (sl.wiki) SSN in SLA…", url: "https://sl.wikipedia.org/wiki/France_Bezlaj" }] },
    { id: "SCHINDEL", pairs: 1, verdictCounts: { POTRJENO: 0, DELNO: 2, NEPOTRJENO: 1, NEVERIFIKATORNO: 1, "BREZ-VIRA": 1 }, topHypotheses: [{ candidate: "Sindel", source: "Bezlaj, France: Slovenski narečni atlas, 1.…", verdict: "NEPOTRJENO", confidence: "~", noteSi: "Atribucije 'Bezlaj, Slovar slovenskih narečij 1976–1978 Zv. 1–4' (ERDAR#2), 'Bezlaj, Slovenski narečni atlas' (WING#1) in 'Bezlaj … narečni atlas, 1. knjiga' (SCHINDEL#2) NE stojijo: v Bezlajevem seznamu del (sl.wiki) SSN in SLA…", url: "https://sl.wikipedia.org/wiki/France_Bezlaj" }, { candidate: "Schindel", source: "SSKJ - Slovenski slovar knjižnega jezika", verdict: "DELNO", confidence: "~", noteSi: "'šindel = skodla (lesena kritina)' je dokumentirano na fran.si (Novak SSP), a izsek prihaja iz prekmurskega slovarja, ne iz SSKJ² samim — pomen ✓, bibliografska natančnost trditve (citat 'SSKJ') delno.", url: "https://fran.si/iskanje?View=1&Query=šindel" }, { candidate: "Šindlov graben", source: "Bezlaj, Slovenski narodnoprazniški leksikon", verdict: "NEVERIFIKATORNO", confidence: "?", noteSi: "sl.wiki seznam Bezlajevih del NE navaja narodnoprazniškega leksikona; delo je znano kot posthumna publikacija (2001), a v fetchanih virih ni potrjeno — SCHINDEL#3 ostaja nepreverjena.", url: "https://sl.wikipedia.org/wiki/France_Bezlaj" }] },
  ],
  keyFindingsSi: [
    "0/70 hipotez je POTRJENIH v celoti: 33 NEPOTRJENIH (citat/atribucija ne stoji), 7 DELNO, 17 NEVERIFIKATORNO (tisk/digitalizati v peskovniku nedostopni), 13 BREZ-VIRA — opozorilo P43 'viri navaja stroj, NEPREVERJENI' se popolnoma potrdi [~]",
    "DWB zvezčne natančnosti (struktura 16-volčne serije, de.wiki): Aue 'Bd 1' ✓ (A∈Bd 1: a–biermolke) in Öde 'Bd 13' ✓ (O∈Bd 13: n,o,p,q) strukturno skladna; Lohn 'Bd 16, Sp. 844' ✗ (L∈Bd 12: l,m), Höfling 'Bd 13, Sp. 742' ✗ (H∈Bd 10: h,i,j), Efeu 'Bd 6, Sp. 102' ✗ (E∈Bd 3: e–forsche) — trije citati zvezkov NAPAČNI [~]",
    "SSKJ refutacije z verbatim (fran.si, direktni geslarski izseki): log = '(močviren) travnik ob vodi, navadno deloma porasel z drevesi' (NE dolina/splav); líza = 'kdor rad liže' (Lecker); lúti = 'hud, jezen'; gesla jedar, ving, orga, horga/hurga, ajna, einhart, guten, poggi, šlifa v SSKJ/Pleteršniku NE obstajajo [~]",
    "Atribucijske refutacije: 'Kärntner Wörterbuch (Schulz, 1972)' ni potrjeno (de.wiki dokumentira WBÖ, Kranzmayer urednik od 1958) — 4 hipoteze brez opore; 'Bezlaj, Slovar slovenskih narečij 1976–78 Zv. 1–4' in 'Bezlaj, Slovenski narečni atlas' ne stojita (v Bezlajevem seznamu del ni; SSN izhaja od 1979); Schmeller 1. izdaja = Cotta (ne 'C.H. Beck') [~]",
    "PV-Gypf: okrajšava 'Gypf.' NI v committed PV.json (Nutzungs-Ausweis 1825) — citat EINHART#2 napačen; okrajšava JE v PS registru (Einhart mit Gypf. &c. + NOVA oblika 'Schüttwiese, Gypfang') [~]",
    "Najmočnejša delna opora: SSKJ²/Pleteršnik golica = 'strmina, na kateri je bil posekan gozd' (EINSCHLAG-GUELZE#1); šindel = 'skodla' dokumentiran (Novak SSP, fran.si; pomen ✓, citat 'SSKJ' delno)",
    "Infrastruktura kampanje: web-search API kvota izčrpana (429) → preusmerjeno na direktno fetchanje primarnih virov: fran.si 18 tarč (verbatim izseki), Wikipedia API 14 tarč (zvezčne mape DWB 33 zvezkov, Schmellerjeve izdaje 1./2. (Cotta 1827–37 / Frommann 1872–77), bibliografija), deterministična 1 tarča (PV.json); DWB/Schmeller polni teksti ostajajo nedosegljivi (woerterbuchnetz SPA 404, zeno.org/archive.org timeout; kanonični URL v dokazih) → 16 tarč NEVERIFIKATORNO za človeško preverbo",
  ],
  verdictSi:
    "Verifikacija virov P43 leksikona (49 tarč): 0/70 hipotez potrjenih v celoti; 33 NEPOTRJENIH (geslo manjka/pomen drugačen/citat zvezka ali atribucija ne stoji), 7 DELNO, 17 NEVERIFIKATORNO (DWB/Schmeller teksti v peskovniku nedosegljivi — kanonični URL v dokazih), 13 BREZ-VIRA. Trije DWB citati zvezkov izrecno napačni (Lohn Bd 16→12, Höfling Bd 13→10, Efeu Bd 6→3), dva strukturno skladna (Aue Bd 1, Öde Bd 13). SSKJ refutacije z verbatim definicijami. Nič ne spreminja P43 hipotez ali rabe (vse ostaja NEKLASIFICIRANO) — sloj verifikacije zvezan bajtno na vhod.",
  verdictEn:
    "Source verification of the P43 lexicon (49 targets): 0/70 hypotheses fully confirmed; 33 REFUTED (headword missing / different meaning / wrong volume or attribution), 7 PARTIAL, 17 UNVERIFIABLE (DWB/Schmeller full texts unreachable from the sandbox — canonical URLs in evidence), 13 NO-SOURCE. Three DWB volume citations explicitly wrong (Lohn Bd 16→12, Höfling Bd 13→10, Efeu Bd 6→3), two structurally consistent (Aue Bd 1, Öde Bd 13). SSKJ refutations with verbatim definitions. Nothing changes the P43 hypotheses or the land-use classification (all remain UNCLASSIFIED) — the verification layer is byte-bound to the input.",
  next: [
    "človeška preverba DWB/Schmeller gesel prek BAdW registra (publikationen.badw.de/de/schmeller/index) in MDZ digitalizatov: Raut, Luch, Schupfe, Loh/Lohe, Einschlag, Gülze, Luge, Wingart (17 NEVERIFIKATORNO tarč)",
    "človeška paleografija 16 družin + 66 kitic (3. prehod ~15 dvoumnih strani, ko VAČ dosegljiv)",
    "nove hipoteze iz verifikacije: Wing ~ Wingart/Weingarten (Weinberg); log (SSKJ 'močviren travnik porasel z drevesi') za LOHN-RAUT/LHOPI/LOHGARN; golica 'posekana strmina' za Gülze-kontekst",
    "semantika 7 par referenc str. 141; p141 šibki blok; p142 dolžina (issue #10)",
  ],
};

export const NEATLINE_GEOREF_P46: {
  series: "GEOREF";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  principle: { statement: string; calibration: string };
  control: {
    sheet: string;
    residuals: Record<string, { px: number; residualM: number; limitM: number; how: string; tiltPx: number }>;
    excluded: Record<string, string>;
  };
  sharedScale: { sbarMPerPx: number; sx: number; sy: number; axisConsistencyPct: number; source: string };
  sheets: Record<
    "A03" | "A04" | "A05",
    {
      cell: string;
      proposedStatus: string;
      uncertaintyM: number;
      detectedSides: number;
      sides: Record<string, { px: number; source?: string; how: string; tiltPx: number | null }>;
      boundsNWSE: [[number, number], [number, number]];
      shiftVsP10MaxM: number;
      spanDeviationsPct: { NS: number; EW: number } | null;
      previous: { status: string; uncertaintyM: string; boundsNWSE: [[number, number], [number, number]] };
    }
  >;
  validations: { label: string; target: string; pass: boolean; distM?: number }[];
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "GEOREF",
  source:
    "Listi public/atlas/n83-a0{2,3,4,5}.jpg + uradna geometrija celic eZKN (research/georef-n83/ezkn-ix24.json, GURS, EPSG:4326) + kontrolna GEOTRUTH afina A02 (model.ts georef-a02, EŠD 2122 + Kolpa) + k.o. poligoni (research/georef-n83/gurs/naselja-wgs84.json); polni izpis research/issue17/neatline-georef.json + src/data/atlas/neatline-georef.json",
  status: "REVIEW",
  generatedBy: "scripts/p46_neatline_georef.py",
  principle: {
    statement:
      "neatline franciscejske sekcije = meja sekcije eZKN 1:2880; uradna geometrija celic je znana → preslikava px ↔ WGS84 brez prostih parametrov (detekcija tanke črte: prag 195, dilatacija ±2 px, tretjinski vrhovi, toleranca nagiba ≤ 30 px, rezerva celotni profil ≥ 0,60)",
    calibration:
      "kontrola na A02 (cf) pod GEOTRUTH afino: detektirani neatline N (y≈97) in E (x≈2710) padata na uradni meji celice cf z residualoma 9 in 13 m — princip kvantitativno potrjen na validiranem listu",
  },
  control: {
    sheet: "A02",
    residuals: {
      top: { px: 97.3, residualM: 9.3, limitM: 90, how: "thirds", tiltPx: 2 },
      right: { px: 2710.3, residualM: 13.2, limitM: 90, how: "thirds", tiltPx: 4 },
    },
    excluded: {
      left:
        "linija pri px≈247 je prel papirja/scan artefakt — pravi west neatline (pričakovano px≈313) ni detektiran; izključeno iz kontrole",
      bottom:
        "kandidati 2015–2063 so mešanica signature-banda in neatline-a; kontroverzno — izključeno iz kontrole (ohranjeno kot opomba)",
    },
  },
  sharedScale: { sbarMPerPx: 0.7746, sx: 0.77654, sy: 0.77266, axisConsistencyPct: 0.5, source: "A04 (sx, sy)" },
  sheets: {
    A03: {
      cell: "dg",
      proposedStatus: "NEATLINE_PARTIAL_GEOREFERENCED",
      uncertaintyM: 50,
      detectedSides: 2,
      sides: {
        bottom: { px: 2058.3, how: "thirds", tiltPx: 1, source: "detected" },
        right: { px: 2476.8, how: "thirds", tiltPx: 21, source: "detected" },
        top: { px: 76.8, how: "s̄ (A04)", tiltPx: null, source: "inferred-scale" },
        left: { px: 9.7, how: "s̄ (A04)", tiltPx: null, source: "inferred-scale" },
      },
      boundsNWSE: [[45.557532, 15.248718], [45.543722, 15.272827]],
      shiftVsP10MaxM: 17.1,
      spanDeviationsPct: { NS: 0, EW: 0 },
      previous: { status: "GRID_APPROX", uncertaintyM: "200–400", boundsNWSE: [[45.5575, 15.2485], [45.5437, 15.273]] },
    },
    A04: {
      cell: "cg",
      proposedStatus: "NEATLINE_GEOREFERENCED",
      uncertaintyM: 40,
      detectedSides: 4,
      sides: {
        top: { px: 84.6, how: "thirds", tiltPx: 13, source: "detected" },
        bottom: { px: 2071.9, how: "thirds", tiltPx: 10, source: "detected" },
        left: { px: 95.4, how: "thirds", tiltPx: 4, source: "detected" },
        right: { px: 2556.9, how: "thirds", tiltPx: 8, source: "detected" },
      },
      boundsNWSE: [[45.55737, 15.273012], [45.543554, 15.297115]],
      shiftVsP10MaxM: 16.6,
      spanDeviationsPct: null,
      previous: { status: "GRID_APPROX", uncertaintyM: "200–400", boundsNWSE: [[45.5574, 15.2728], [45.5436, 15.2973]] },
    },
    A05: {
      cell: "ch",
      proposedStatus: "NEATLINE_GEOREFERENCED",
      uncertaintyM: 40,
      detectedSides: 4,
      sides: {
        top: { px: 82.4, how: "thirds", tiltPx: 19, source: "detected" },
        bottom: { px: 2075.4, how: "thirds", tiltPx: 4, source: "detected" },
        left: { px: 102.4, how: "thirds", tiltPx: 10, source: "detected" },
        right: { px: 2557.4, how: "thirds", tiltPx: 10, source: "detected" },
      },
      boundsNWSE: [[45.543722, 15.272828], [45.529907, 15.296925]],
      shiftVsP10MaxM: 17.8,
      spanDeviationsPct: { NS: 0.54, EW: 0.51 },
      previous: { status: "GRID_APPROX", uncertaintyM: "200–400", boundsNWSE: [[45.5437, 15.2726], [45.5299, 15.2971]] },
    },
  },
  validations: [
    { label: "TRIBUTSCH (A03 px 1799,754)", target: "znotraj k.o. Tribuče (poligon)", pass: true },
    { label: "WEIDENDORF (A03 px 1878,1852)", target: "znotraj k.o. Bedenj (poligon)", pass: true },
    { label: "WEIDENDORF (A04 px 608,1964)", target: "znotraj k.o. Bedenj (poligon)", pass: true },
    { label: "ADLESCHITZ (A04 px 2116,1403)", target: "izven modernega k.o. Griblje + znotraj celice cg", pass: true },
    { label: "Bresnik (A04 px 1032,1532)", target: "≤ 700 m od (45.5476, 15.2824)", pass: true, distM: 34 },
    { label: "sklop ~45 stavb / Fučkovci (A05 px 1975,606)", target: "≤ 700 m od (45.5398, 15.2910) + znotraj celice ch", pass: true, distM: 33 },
    { label: "Pri Jankovichti (A05 px 1712,455)", target: "≤ 700 m od (45.5408, 15.2885)", pass: true, distM: 33 },
  ],
  verdictSi:
    "Neatline georeferenciranje sekcij dg/cg/ch (A03–A05): princip 'neatline = meja sekcije' kalibriran na A02 z residualoma 9 in 13 m; A04 in A05 popolnoma zasidrani (4 detektirane strani, merilo 0.7727–0.7765 m/px, medosna konsistenca 0,5 %), A03 delno (S/E detektirana, N/W preko skupnega merila, šibki kandidati potrjujeta v okviru 25 m). Novo: ±40–50 m namesto ±200–400 m (4–8× izboljšanje). Ne-regresija 7/7 P10 kontrolnih napisov — Bresnik/Fučkovci/Jankovichti sedaj 33–34 m od P10 tarč. Premik mej vs P10 le 17–18 m (popravek konvergencije). SHEET_GEOREFS se namerno ne spreminja — predlog nadgradnje čaka človeško potrditev neatline črt (lekcija P9).",
  verdictEn:
    "Neatline georeferencing of sections dg/cg/ch (A03–A05): the 'neatline = section boundary' principle calibrated on A02 with residuals of 9 and 13 m; A04 and A05 fully anchored (4 detected sides, scale 0.7727–0.7765 m/px, axis consistency 0.5%), A03 partial (S/E detected, N/W via the shared scale, weak candidates corroborate within 25 m). New: ±40–50 m instead of ±200–400 m (a 4–8× improvement). Non-regression 7/7 P10 control labels — Bresnik/Fučkovci/Jankovichti now land 33–34 m from the P10 targets. Bounds shift vs P10 only 17–18 m (a convergence correction). SHEET_GEOREFS is deliberately unchanged — the upgrade proposal awaits human confirmation of the neatlines (the P9 lesson).",
  next: [
    "človeška potrditev detektiranih neatline črt (vizualni pregled izrezov ob 4× povečavi) → nato nadgradnja SHEET_GEOREFS A03–A05 + Leaflet overlay kot pri A01/A02",
    "GURS stavbni overlay prek novih afin (A04: vsebina celice cg; A05: sklop Fučkovci) — kvantitativna primerjava z medi P10 (72 m)",
    "presek z A03: vzhodni pas (x 83–100 %) mora kontinuirati na A02/A04 zahodni neatline — preverba zahteve",
    "P9 retrakcija za A04 ostaja veljavna — nova neatline rešitev nadgradi P10 brez prostih podobnostnih parametrov (rotacija/merilo izhajata iz uradne celice, ne iz prostega fita)",
  ],
};

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
  source: "N083PZ str. 1–3, 20, 30, 40, 50, 60, 68–71 (Arhiv RS, SI AS 176, k.o. Griblje) — research/issue17/PZ-profile.json + PZ-valuation.json; P44 (str. 4–67 v celoti): research/issue11/pz-classes-full.json",
  titleAsWritten: "CATASTRAL-SCHÄTZUNGS-ELABORAT der Gemeinde Grüble (Land Krain, 83, Kreis Neustadtl, Steuerbezirk Krupge [~])",
  status: "REVIEW",
  population: { total: 441, male: 222, female: 219, houses: "72 [~]", families: "102 [~]", confidence: "prebivalstvo srednja; hiše/družine nizka [~]" },
  areaTotal: { joch: 2294, klafter: 516, confidence: "~ (§1)" },
  dates: { madeAsWritten: "Gemacht den 28ten Juli 1825", certificationAsWritten: "Geprüft / overovitve 9. 8. 1826 [~] in [~1824]", revaluationAsWritten: "[~1834, rdeči dodatek »revaluirt« na str. 60 — sumljivo, preveriti]" },
  valuationChain: [
    { stepSi: "Bau-Area (stavbna zemljišča) — Roh-Ertrag", valuesSi: "16 fl 50½ kr/joch", confidence: "srednja-visoka" },
    { stepSi: "Cultur-Aufwand (55 % bruto)", valuesSi: "9 fl 15¾ kr/joch (aritmetika potrjena: 55 % × 16 fl 50½)", confidence: "visoka" },
    { stepSi: "Rein-Ertrag (čisti donos stavbnih tal)", valuesSi: "7 fl 35 kr/joch", confidence: "visoka (1010,5 − 555,5 kr = 455 kr)" },
    { stepSi: "Ackerland razred I", valuesSi: "Rob 25 fl 44 kr (prečrtani 20 fl 44 je nadomeščen) − Anschlag 10 fl 40½ kr = Rein 15 fl 3½ ≈ zapisani 15 fl 5 kr — P44 RAZREŠILO prejšnjo divergenco treh branj (dokaz pz-classes-full.json D2)", confidence: "srednja" },
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
    PS: "143/143 strani strojno (P36 2743 + P38 pass-3 = 2974; sprava s 2607 odprta) (REVIEW)",
    PUA: "49/49 strani, 101 vrstic (REVIEW)",
    PZ: "71/71 strani (P44: tabele razredov + rekapitulacija, 76 VLM klicev) (REVIEW)",
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

// ——— P47: GURS parcel overlay — neodvisna validacija neatline afin (issue #14/§3) ———

export const GURS_OVERLAY_P47: {
  series: "GEOREF";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  principle: { statement: string; control: string; strata: string };
  sheets: Record<
    "A02" | "A03" | "A04" | "A05",
    {
      cell: string;
      affineSource: string;
      nInCell: number;
      nEvaluated: number;
      nDrawn: number;
      nEmpty: number;
      mPerPx: number;
      drawn: {
        cov0: { median: number; q25: number; q75: number };
        covBest: { median: number };
        residualPx: { median: number; q75: number; p90: number };
        residualM: { median: number; p90: number };
      };
      controls: Record<string, { median: number; n: number }>;
      empty: { note: string };
    }
  >;
  cropFiles: { file: string; kind: string; sheet: string; side?: string; source?: string }[];
  findingsSi: string[];
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "GEOREF",
  source:
    "Sodobne parcele GURS eZKN WFS (KO 1544: research/georef-n83/gurs/parceles-0..4.json iz P10; KO 1552 v bboxu ch: parceles-ko1552-ch-0..2.json iz P47, recept scripts/p47_fetch_ko1552.sh) + P46 afini (research/issue17/neatline-georef.json) + GEOTRUTH meje A02 (model.ts) + skeni public/atlas/n83-a0{2,3,4,5}.jpg; polni izpis research/issue17/gurs-overlay.json + src/data/atlas/gurs-overlay.json; izrezi research/issue17/neatline-crops/ (16)",
  status: "REVIEW",
  generatedBy: "scripts/p47_gurs_overlay.py",
  principle: {
    statement:
      "sodobne katastrske parcele (GURS eZKN WFS, EPSG:3794 → WGS84) preslikane skozi P46 neatline afine morajo pasti na narisane črte franciscejskega katastra 1825; merimo pokritost črnila oboda (plus-oblika 3×3 temno, prag 195; vzorčenje 1,5 px) in residual najboljšega zamika ±12 px",
    control:
      "kontrola metode na A02 pod GEOTRUTH preslikavo meja (model.ts, ±40–80 m) — mediana residuala 9.8 m je skladna z deklarirano negotovostjo",
    strata:
      "lokalna gostota temnega (bbox±100 px) ≥ 0.06 → DRAWN (narisana površina); pod pragom → EMPTY (v 1825 nenarisano: skupna paša WAIDENDORF, gozd) — nizka pokritost EMPTY je lastnost rabe tal, ne napaka registracije",
  },
  sheets: {
    A02: {
      cell: "cf",
      affineSource: "model.ts georef-a02 meje (osno poravnana, GEOTRUTH)",
      nInCell: 749,
      nEvaluated: 659,
      nDrawn: 640,
      nEmpty: 19,
      mPerPx: 0.805,
      drawn: {
        cov0: { median: 0.542, q25: 0.388, q75: 0.686 },
        covBest: { median: 0.717 },
        residualPx: { median: 12.2, q75: 14.2, p90: 17.0 },
        residualM: { median: 9.8, p90: 13.7 },
      },
      controls: { "100": { median: 0.496, n: 5120 }, "200": { median: 0.473, n: 5088 }, "400": { median: 0.433, n: 4787 } },
      empty: { note: "brez (v naselbinskem jedru je vsa moderna zazidana tudi leta 1825 narisana)" },
    },
    A03: {
      cell: "dg",
      affineSource: "P46 neatline afina (neatline-georef.json)",
      nInCell: 124,
      nEvaluated: 118,
      nDrawn: 112,
      nEmpty: 6,
      mPerPx: 0.775,
      drawn: {
        cov0: { median: 0.487, q25: 0.342, q75: 0.649 },
        covBest: { median: 0.729 },
        residualPx: { median: 12.7, q75: 15.3, p90: 17.0 },
        residualM: { median: 9.8, p90: 13.2 },
      },
      controls: { "100": { median: 0.366, n: 896 }, "200": { median: 0.32, n: 888 }, "400": { median: 0.184, n: 775 } },
      empty: { note: "6 parcel na robu (gozd)" },
    },
    A04: {
      cell: "cg",
      affineSource: "P46 neatline afina (neatline-georef.json)",
      nInCell: 688,
      nEvaluated: 626,
      nDrawn: 498,
      nEmpty: 128,
      mPerPx: 0.775,
      drawn: {
        cov0: { median: 0.447, q25: 0.308, q75: 0.59 },
        covBest: { median: 0.707 },
        residualPx: { median: 7.2, q75: 10.8, p90: 13.2 },
        residualM: { median: 5.6, p90: 10.2 },
      },
      controls: { "100": { median: 0.306, n: 3980 }, "200": { median: 0.298, n: 3929 }, "400": { median: 0.271, n: 3651 } },
      empty: { note: "128 parcel (večinoma KO 1552 na južnem prekrivanju celic) na v 1825 nenarisanih površinah" },
    },
    A05: {
      cell: "ch",
      affineSource: "P46 neatline afina (neatline-georef.json)",
      nInCell: 635,
      nEvaluated: 559,
      nDrawn: 165,
      nEmpty: 394,
      mPerPx: 0.775,
      drawn: {
        cov0: { median: 0.445, q25: 0.074, q75: 0.82 },
        covBest: { median: 0.86 },
        residualPx: { median: 12.0, q75: 14.4, p90: 17.0 },
        residualM: { median: 9.3, p90: 13.1 },
      },
      controls: { "100": { median: 0.338, n: 1320 }, "200": { median: 0.189, n: 1316 }, "400": { median: 0.012, n: 1204 } },
      empty: {
        note: "394/559 parcel na v 1825 nenarisanih površinah — velikanska skupna paša WAIDENDORF (prosle črke sredi lista, 'Stab der Reambulierungs-Beimappe') + gozd; dokumentirana razlika rabe tal, ne napaka registracije",
      },
    },
  },
  cropFiles: [
    { file: "A02-parcels.jpg", kind: "parcels", sheet: "A02" },
    { file: "A03-parcels.jpg", kind: "parcels", sheet: "A03" },
    { file: "A04-parcels.jpg", kind: "parcels", sheet: "A04" },
    { file: "A05-parcels.jpg", kind: "parcels", sheet: "A05" },
    { file: "A03-top.jpg", kind: "neatline", sheet: "A03", side: "top", source: "inferred-scale" },
    { file: "A03-right.jpg", kind: "neatline", sheet: "A03", side: "right", source: "detected" },
    { file: "A03-bottom.jpg", kind: "neatline", sheet: "A03", side: "bottom", source: "detected" },
    { file: "A03-left.jpg", kind: "neatline", sheet: "A03", side: "left", source: "inferred-scale" },
    { file: "A04-top.jpg", kind: "neatline", sheet: "A04", side: "top", source: "detected" },
    { file: "A04-right.jpg", kind: "neatline", sheet: "A04", side: "right", source: "detected" },
    { file: "A04-bottom.jpg", kind: "neatline", sheet: "A04", side: "bottom", source: "detected" },
    { file: "A04-left.jpg", kind: "neatline", sheet: "A04", side: "left", source: "detected" },
    { file: "A05-top.jpg", kind: "neatline", sheet: "A05", side: "top", source: "detected" },
    { file: "A05-right.jpg", kind: "neatline", sheet: "A05", side: "right", source: "detected" },
    { file: "A05-bottom.jpg", kind: "neatline", sheet: "A05", side: "bottom", source: "detected" },
    { file: "A05-left.jpg", kind: "neatline", sheet: "A05", side: "left", source: "detected" },
  ],
  findingsSi: [
    "Neodvisna validacija P46 afin z ZUNANJIM virom (GURS eZKN): sodobne parcele se registrirajo na risbo 1825 z mediano residuala 9.8/5.6/9.3 m (A03/A04/A05), p90 ≤ 13.2 m — znotraj neatline negotovosti ±40–50 m, daleč pod staro GRID_APPROX ±200–400 m.",
    "Kontrola metode na A02 (GEOTRUTH ±40–80 m): mediana residuala 9.8 m — raven ujemanja enaka kot na P46 afineh, kar potrjuje tudi konsistentnost GEOTRUTH-a.",
    "A05/ch je 'Stab der Reambulierungs-Beimappe' — 394/559 evalviranih parcel pada na v 1825 nenarisane površine (EMPTY): velikanska skupna paša WAIDENDORF s proslimi črkami sredi lista. To je kvantitativno dokumentirana razlika rabe tal (1825 paša → poznejša delitev), ne napaka registracije.",
    "Pokritost črnila DRAWN parcel brez zamika (0.44–0.55) je sistematično nad kontrolo-zamik 200 px (0.19–0.30; na gosto narisani A02 tudi kontrole visoke — zato je tam odločilni residual) in se pri najboljšem zamiku (0.71–0.86) še strmi — tipičen podpis pravilne registracije.",
  ],
  verdictSi:
    "GURS parcel overlay (P47): sodobna parcelna mreža (KO 1544 + KO 1552) preslikana prek P46 neatline afin se registrira na risbo 1825 z mediano residuala 5.6–9.8 m in p90 ≤ 13.2 m na vseh treh listih A03–A05; kontrola metode na A02 (GEOTRUTH) da 9.8 m. Pokritost črnila je nad kontrole-zamiki in se pri poravnavi strmi (0.71–0.86). A05 razkriva land-use dokaz: 394 EMPTY parcel = WAIDENDORF skupna paša v 1825. To je neodvisna zunanj validacija P46 — a SHEET_GEOREFS se še naprej NAMERNO ne spreminja: človeška potrditev neatline črt prek 16 dokaznih izrezov (research/issue17/neatline-crops/) ostaja pogoj nadgradnje (lekcija P9).",
  verdictEn:
    "GURS parcel overlay (P47): the modern parcel grid (KO 1544 + KO 1552) mapped through the P46 neatline affines registers onto the 1825 drawing with a median residual of 5.6–9.8 m and p90 ≤ 13.2 m on all three sheets A03–A05; the method control on A02 (GEOTRUTH) gives 9.8 m. Ink coverage sits above the shift controls and sharpens under alignment (0.71–0.86). A05 reveals a land-use proof: 394 EMPTY parcels = the WAIDENDORF common pasture of 1825. This is an independent external validation of P46 — yet SHEET_GEOREFS still deliberately remains unchanged: human confirmation of the neatlines via the 16 proof crops (research/issue17/neatline-crops/) remains the upgrade condition (the P9 lesson).",
  next: [
    "človeška potrditev detektiranih neatline črt (vizualni pregled 16 izrezov v research/issue17/neatline-crops/) → nato nadgradnja SHEET_GEOREFS A03–A05 + Leaflet overlay kot pri A01/A02",
    "razširitev overlay-a na polne poligone KO 1552 (celotna k.o., ne samo bbox ch) za pokritost južnega dela",
    "stavbni overlay: primerjava narisanih stavb 1825 (Blatt X register, 102 stavbnih mest) z modernimi stavbnimi parcelami GURS — most PUA↔PT↔PS↔GURS",
    "najostrejši zamik (mediana 7–13 px ≈ 5–10 m) omogoča izris sodobnih parcel kot pomožnega sloja nad skeni v Atlasu (zahteve iz P46 next)",
  ],
};

export const BUILDINGS_OVERLAY_P48: {
  series: "GEOREF";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  principle: { statement: string; control: string; continuity: string; blattX: string };
  sheets: Record<
    "A02" | "A03" | "A04" | "A05",
    {
      cell: string;
      affineSource: string;
      nInCell: number;
      nEvaluated: number;
      nDrawn: number;
      nEmpty: number;
      mPerPx: number;
      drawn: {
        n: number;
        cov0: { median: number; q25: number; q75: number };
        covBest: { median: number };
        residualPx: { median: number; p90: number };
        residualM: { median: number; p90: number };
      } | null;
      onSymbol: {
        n: number;
        cov0?: { median: number; q25: number; q75: number };
        covBest?: { median: number };
        residualPx?: { median: number; p90: number };
        residualM?: { median: number; p90: number };
      };
      controls: Record<string, { median: number; n: number }>;
    }
  >;
  continuity: {
    sheet: string; footprints1825: number; modernEvaluated: number; pairPx: number;
    pairs: number; pairsStrong: number; pairDistPx: { median: number | null; p90: number | null };
    onSymbolWithoutVector: number; new: number; gone: number; goneNearPx: { median: number | null };
    clsCounts: Record<string, number>;
  };
  blattX: {
    rows: number; distinctHausNr: number; inGrundRange41_2500: number; inGrundParcelSet: number;
    inPtHouseSet: number; areasComparable: number; areasIdentical: number; b3OwnerNumeric: number;
    b3OwnerRange: [number, number]; medianAreaJoch: number; maxAreaJoch: number;
    grundHouseMedianJoch: number; footer138vsota: string | null; rows1_20ComputedK: number;
    rows1_20ComputedAs: string;
  };
  cropFiles: { file: string; kind: string; sheet: string; distPx?: number; cls?: string; n?: number; covBest?: number }[];
  findingsSi: string[];
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "GEOREF",
  source: "Sodobni stavbni tlorisi GURS eZKN WFS SI.GURS.KN:STAVBE (KO 1544: research/georef-n83/gurs/stavbe-ko1544-0.json, 401 z geometrijo; KO 1552 južni bbox: stavbe-ko1552-south-0.json, 313; recept scripts/p48_fetch_stavbe.sh) + GEOTRUTH meje A02 (model.ts) + P46 afini (neatline-georef.json) + tlorisi 1825 (src/data/atlas/buildings.json, 156) + Blatt X (research/issue17/ps-landuse.json + houses.ts + ps-raw/ps-138.json); polni izpis research/issue17/buildings-overlay.json + src/data/atlas/buildings-overlay.json; izrezi research/issue17/buildings-crops/ (12)",
  status: "REVIEW",
  generatedBy: "scripts/p48_buildings_overlay.py",
  principle: {
    statement: "sodobni stavbni tlorisi (GURS eZKN WFS SI.GURS.KN:STAVBE, OBRIS_GEOM, EPSG:3794 → WGS84) preslikani prek GEOTRUTH meja A02 / P46 afin A03–A05 morajo pasti na narisane stavbne simbole 1825; merimo pokritost črnila notranjosti+oboda na erodirani maski (plus-oblika 3×3, prag 195 — tanke parcelne črte izginejo, polni simboli ostanejo) in residual najboljšega zamika ±12 px",
    control: "kontrole-zamiki 100/200/400 px × 8 smeri; strata po pravilu P47 (lokalna gostota temnega ≥ 0.06 → DRAWN); klasifikacija stavb ON-SYMBOL (cov@best ≥ 0.5) / PARTIAL (0.25–0.5) / NEW (<0.25)",
    continuity: "A02: 156 vektoriziranih tlorisov 1825 (buildings.json, px prostor primarno) ↔ sodobne stavbe — PAIR ≤ 25 px (≈ 20 m), GONE (brez sodobne stavbe), NEW (brez predhodnika)",
    blattX: "deterministična kvantitativna opomba k interpretaciji P40/P42 — test referenc (razpon, površine, številke v owner stolpcu) iz committed dokazov, brez AI"
  },
  sheets: {
    A02: {
      cell: "cf",
      affineSource: "model.ts georef-a02 meje (osno poravnana, GEOTRUTH)",
      nInCell: 154,
      nEvaluated: 154,
      nDrawn: 154,
      nEmpty: 0,
      mPerPx: 0.805,
      drawn: {
        n: 154,
        cov0: {
          median: 0.85,
          q25: 0.562,
          q75: 1.0
        },
        covBest: {
          median: 1.0
        },
        residualPx: {
          median: 12.3,
          p90: 17.0
        },
        residualM: {
          median: 9.9,
          p90: 13.7
        }
      },
      onSymbol: {
        n: 149,
        cov0: {
          median: 0.867,
          q25: 0.581,
          q75: 1.0
        },
        covBest: {
          median: 1.0
        },
        residualPx: {
          median: 12.2,
          p90: 17.0
        },
        residualM: {
          median: 9.8,
          p90: 13.7
        }
      },
      controls: {
        "100": {
          median: 0.622,
          n: 1232
        },
        "200": {
          median: 0.533,
          n: 1217
        },
        "400": {
          median: 0.522,
          n: 1138
        }
      }
    },
    A03: {
      cell: "dg",
      affineSource: "P46 neatline afina (neatline-georef.json)",
      nInCell: 0,
      nEvaluated: 0,
      nDrawn: 0,
      nEmpty: 0,
      mPerPx: 0.775,
      drawn: null,
      onSymbol: {
        n: 0
      },
      controls: {
        "100": {
          median: 0.0,
          n: 0
        },
        "200": {
          median: 0.0,
          n: 0
        },
        "400": {
          median: 0.0,
          n: 0
        }
      }
    },
    A04: {
      cell: "cg",
      affineSource: "P46 neatline afina (neatline-georef.json)",
      nInCell: 39,
      nEvaluated: 39,
      nDrawn: 3,
      nEmpty: 36,
      mPerPx: 0.775,
      drawn: {
        n: 3,
        cov0: {
          median: 0.0,
          q25: 0.0,
          q75: 0.071
        },
        covBest: {
          median: 0.046
        },
        residualPx: {
          median: 0.0,
          p90: 8.9
        },
        residualM: {
          median: 0.0,
          p90: 6.9
        }
      },
      onSymbol: {
        n: 0
      },
      controls: {
        "100": {
          median: 0.0,
          n: 23
        },
        "200": {
          median: 0.0,
          n: 14
        },
        "400": {
          median: 0.0,
          n: 12
        }
      }
    },
    A05: {
      cell: "ch",
      affineSource: "P46 neatline afina (neatline-georef.json)",
      nInCell: 96,
      nEvaluated: 95,
      nDrawn: 28,
      nEmpty: 67,
      mPerPx: 0.775,
      drawn: {
        n: 28,
        cov0: {
          median: 0.871,
          q25: 0.339,
          q75: 0.983
        },
        covBest: {
          median: 1.0
        },
        residualPx: {
          median: 12.9,
          p90: 17.0
        },
        residualM: {
          median: 10.0,
          p90: 13.2
        }
      },
      onSymbol: {
        n: 26,
        cov0: {
          median: 0.928,
          q25: 0.526,
          q75: 0.985
        },
        covBest: {
          median: 1.0
        },
        residualPx: {
          median: 13.0,
          p90: 17.0
        },
        residualM: {
          median: 10.1,
          p90: 13.2
        }
      },
      controls: {
        "100": {
          median: 0.6,
          n: 224
        },
        "200": {
          median: 0.12,
          n: 224
        },
        "400": {
          median: 0.0,
          n: 219
        }
      }
    }
  },
  continuity: {
    sheet: "A02",
    footprints1825: 156,
    modernEvaluated: 154,
    pairPx: 25,
    pairs: 37,
    pairsStrong: 36,
    pairDistPx: {
      median: 16.3,
      p90: 22.3
    },
    onSymbolWithoutVector: 113,
    new: 0,
    gone: 136,
    goneNearPx: {
      median: 392.6
    },
    clsCounts: {
      "ON-SYMBOL-BREZ-VEKTORIZACIJE": 113,
      "PAIR-STRONG": 36,
      PAIR: 1,
      UNCLASSIFIED: 4
    }
  },
  blattX: {
    rows: 60,
    distinctHausNr: 59,
    inGrundRange41_2500: 58,
    inGrundParcelSet: 57,
    inPtHouseSet: 22,
    areasComparable: 37,
    areasIdentical: 0,
    b3OwnerNumeric: 18,
    b3OwnerRange: [
      63.0,
      80.0
    ],
    medianAreaJoch: 6.329,
    maxAreaJoch: 17.299,
    grundHouseMedianJoch: 0.282,
    footer138vsota: "101 Joch 283 Klafter",
    rows1_20ComputedK: 147722,
    rows1_20ComputedAs: "92 J 522 K"
  },
  cropFiles: [
    {
      file: "a02-pair-1.jpg",
      kind: "continuity-pair",
      sheet: "A02",
      distPx: 2.3,
      cls: "PAIR-STRONG"
    },
    {
      file: "a02-pair-2.jpg",
      kind: "continuity-pair",
      sheet: "A02",
      distPx: 2.8,
      cls: "PAIR-STRONG"
    },
    {
      file: "a02-pair-3.jpg",
      kind: "continuity-pair",
      sheet: "A02",
      distPx: 3.4,
      cls: "PAIR-STRONG"
    },
    {
      file: "a02-pair-4.jpg",
      kind: "continuity-pair",
      sheet: "A02",
      distPx: 6.6,
      cls: "PAIR-STRONG"
    },
    {
      file: "a02-pair-5.jpg",
      kind: "continuity-pair",
      sheet: "A02",
      distPx: 7.6,
      cls: "PAIR-STRONG"
    },
    {
      file: "a02-pair-6.jpg",
      kind: "continuity-pair",
      sheet: "A02",
      distPx: 8.1,
      cls: "PAIR-STRONG"
    },
    {
      file: "a02-gone.jpg",
      kind: "gone",
      sheet: "A02",
      n: 40
    },
    {
      file: "a05-symbol-1.jpg",
      kind: "on-symbol",
      sheet: "A05",
      covBest: 1.0
    },
    {
      file: "a05-symbol-2.jpg",
      kind: "on-symbol",
      sheet: "A05",
      covBest: 0.969
    },
    {
      file: "a05-new.jpg",
      kind: "new",
      sheet: "A05",
      n: 30
    },
    {
      file: "a04-new.jpg",
      kind: "new",
      sheet: "A04",
      n: 39
    },
    {
      file: "a02-overview.jpg",
      kind: "overview",
      sheet: "A02"
    }
  ],
  findingsSi: [
    "Registracija stavb A02: sodobni GURS tlorisi (154 v celici cf) se registrirajo na narisane stavbne simbole 1825 z mediano residuala 9.8 m (p90 13.7 m) — stavbna raven potrjuje parcelno Raven P47 (9.8 m) pod isto GEOTRUTH preslikavo.",
    "A02 on-symbol 149/154 sodobnih stavb pada na narisane stavbne simbole 1825 (cov@best ≥ 0.5; mediana pokritosti DRAWN strata 1.0, cov@0 0.85) — jedro vasi je stavbno kontinuirano.",
    "Kontinuiteta A02: 37 sodobnih stavb ima vektoriziran tloris 1825 v bližini ≤ 25 px (36 z cov@best ≥ 0.5); 136 od 156 tlorisov 1825 je brez sodobne stavbe v bližini (mediana najbližje 392.6 px ≈ 316.2 m) — razpršena zidanica 1825 (vinice/hambi na zahodnih pobočjih) ni preživela; nadgradja P16 present.json (OSM 15 obstaja · 26 negotovih · 115 ni jih več) z uradnimi GURS obrisi — izvedeno v P54 (18/21/117, repla pravil 156/156).",
    "A05/ch (Fučkovci): 26 sodobnih stavb pada na narisane stavbe 1825 z mediano residuala 10.1 m — neodvisna potrditev P46 afine na stavbni ravni; A04/cg: 0 on-symbol — vse sodobne stavbe v celici cg so novejše od risbe (paša WEIDENDORF, P47 EMPTY stratum)",
    "Blatt X (str. 138–139) kvantitativna opomba: 59 različnih numeričnih 'hausNr' vrednosti, 58 v razponu GRUND parcel (41–2500), a površine se z GRUND parcelami pri istih številkah UJEMAJO 0/37-krat — direktna referenca na register 1825 je REFRIRANA; površine vrstic (mediana 6.329 Joch, do 17.299 J) so red velikosti nad GRUND dvorišči (mediana 0.282 J) — vrstice so velike zemljiške parcele; owner stolpec vrstic 81–100 vsebuje 18 številk (63–80) — signal premika stolpcev pri branju; skladno z opombo vrstice 1 'Zusammenstellung der Grundstücke' in letnico 1860 v branjih (reambulacijska doba, glave listov 'Reambulirungs-Beimappe')",
    "Posledica za P40/P42: interpretacija 'Blatt X = register stavbnih mest' (P42 ARTIFAKT dokaz: številke 82–100 v stolpcu rabe) je ovržena na kvantitativni ravni — številke so lastna štetje vrstic (parzella == raba na vrsticah 82–100), površine pa izključujejo stavbna mesta; vpogled ostaja [~] do človeške paleografije str. 138–139; P40 'blattXOverlap 60/102' okvir je treba brati kot delno prekrivanje dveh različnih sekcij, ne kot registrsko vrzel"
  ],
  verdictSi: "P48 (2026-10-13): sodobni stavbni tlorisi (GURS eZKN WFS, 403 KO 1544 + 313 KO 1552 južni bbox) preslikani na skene 1825 — registracija stavbne ravni: A02 mediana residuala 9.8 m (p90 13.7 m), 149/154 stavb pada na narisane simbole (cov@best mediana 1.0); A05 Fučkovci 26 stavb, residual 10.1 m; A04/cg 0 (sodobne stavbe na paši WEIDENDORF so novejše). Kontinuiteta A02: 37 parov tloris↔stavba (≤ 25 px), 136/156 tlorisov brez naslednika (razpršena zidanica 1825 na zahodnih pobočjih ni preživela — vinice/hambi), nadgradja P16 present.json. Blatt X: direktna referenca na register 1825 REFRIRANA (0/37 identičnih površin), površine vrstic so red velikosti nad dvorišči, owner stolpec vrstic 81–100 vsebuje številke — P42 interpretacija 'register stavbnih mest' kvantitativno ovržena, ostaja [~] do človeške paleografije. SHEET_GEOREFS in obstoječi dokazi P40–P47 nespremenjeni.",
  verdictEn: "P48 (2026-10-13): modern building footprints (GURS eZKN WFS, 403 KO 1544 + 313 KO 1552 south bbox) mapped onto the 1825 scans — building-level registration: A02 median residual 9.8 m (p90 13.7 m), 149/154 buildings fall on drawn symbols (cov@best median 1.0); A05 Fučkovci 26 buildings, residual 10.1 m; A04/cg 0 (modern buildings on the WEIDENDORF pasture are younger than the map). A02 continuity: 37 footprint↔building pairs (≤ 25 px), 136/156 1825 footprints without a successor (the dispersed 1825 settlement on the western slopes did not survive — vineyard cottages/hambas), an upgrade of P16 present.json. Blatt X: direct reference to the 1825 register REFUTED (0/37 identical areas), row areas are an order of magnitude above house curtilages, the owner column of rows 81–100 contains numbers — the P42 interpretation 'register of building sites' is quantitatively refuted, remains [~] until human paleography. SHEET_GEOREFS and the existing P40–P47 evidence unchanged.",
  next: [
    "človeška paleografija str. 138–139 (Blatt X) — potrditev/ovržba reambulacijske hipoteze in premika stolpcev",
    "človeška potrditev neatline črt (izrezi P46/P47) še vedno pogoj za nadgradnjo SHEET_GEOREFS",
    "razširitev vektorizacije stavb 1825 na A05 (Fučkovci cluster) za polno kontinuiteto na južnih listih",
    "stavbni overlay ← stavbna mesta PT (N083PT) — povezava parov z domačijskimi številkami prek map.village jedra ( potrebuje človeško potrditev simbolov)"
  ],
};

// ——— P49: FUČKOVCI 1825 — modern-anchored symbol evidence + striktna jedra + obseg sklopa (issue #14/§3) ———
// Programsko generirano iz research/issue17/fucukovci-1825.json (scripts/p49_fucukovci1825.py).

export const FUCUKOVCI_P49: {
  series: "GEOREF";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  principle: { statement: string; control: string; limits: string };
  anchor: { p10Geo: [number, number]; pxViaAffine: [number, number]; vlmReadPx: [number, number]; offsetPx: number };
  modern: { nInCell: number; nEvaluated: number; nDrawn: number; nEmpty: number; nOnSymbol: number; residualM: number | null; covBestMedian: number | null };
  cluster: { radiusPx: number; onSymbolInCluster: number; onSymbolTotal: number; nearestOnSymbolToAnchorPx: number; centroidDistToP10M: number; hullAreaM2: number; hullVertices: number; inkMassPx: number; inkBboxPx: [number, number, number, number] };
  strict: { nSymbols: number; nCorroborated: number; nUnmatched: number; nUnmatchedInCluster: number; triageInCluster: Record<string, number>; wMedianPx: number; hMedianPx: number; pairPx: number };
  estimate: { p10BuildingsVlm: number; onSymbolInCluster: number; goneCandidatesBuilding: number; goneCandidatesUnclear: number; lowerBound: number; upperBound: number; continuityLowerRatio: number };
  limits: { pinkFillGrayMedian: number; tDark: number; villageBoxInkFraction: number; a02VectorizedN: number };
  cropFiles: { file: string; kind: string; note?: string; distPx?: number; id?: string }[];
  findingsSi: string[];
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "GEOREF",
  source: "Sodobne stavbe GURS eZKN WFS (stavbe-ko1544-0.json 401 z geometrijo + stavbe-ko1552-south-0.json 313, recept scripts/p48_fetch_stavbe.sh) + P46 afina A05 (neatline-georef.json) + celica ch (ezkn-ix24.json) + sken public/atlas/n83-a05.jpg + tlorisi 1825 A02 (buildings.json) za primerjavo; polni izpis research/issue17/fucukovci-1825.json + src/data/atlas/fucukovci-1825.json; izrezi research/issue17/fucukovci-crops/ (9)",
  status: "REVIEW",
  generatedBy: "scripts/p49_fucukovci1825.py",
  principle: {
    statement: "tri neodvisni deterministični dokazni sloji za Fučkovci 1825 (list A05, celica ch): (1) MODERN-ANCHORED — sodobne stavbe preslikane prek P46 afine nazaj na sken; cov@best ≥ 0.5 na erodirani maski = stavbno mesto 1825 z naslednikom; (2) STRIKTNA DETEKCIJA JEDER — lokalni kontrast + zelo-temni delež + test obroča + oblika = temna jedra; korelacija z (1) ali GONE-kandidat [~] z vizualno triažo; (3) OBSEG SKLOPA — konveksna lupina dokazanih mest (px → WGS84) + masa črnila",
    control: "pariteta s P48 (96/95/26, isti stroj cov@0/cov@best/strata); P10 sidro iz geografske tarče prek afine (odmik od VLM branja ≤ 50 px); determinizem I6 (2 prehoda bajtno); kanonski = runtime izpis (I7); sha256 izrezov (I8)",
    limits: "celtna vektorizacija tlorisov na A05 NI izvedljiva: rožnati fill siva ~168 < 195 (zasenčitev maske), zasičenost erodirane maske v vasi 37.5 % (stakanje simbolov), številke/črki/drevesa v istem razredu kot simboli — namesto tega dokazni sloji + kontaktni listi za človeško presojo",
  },
  anchor: { p10Geo: [15.291, 45.5398], pxViaAffine: [1944.8, 636.8], vlmReadPx: [1975, 606], offsetPx: 43.2 },
  modern: { nInCell: 96, nEvaluated: 95, nDrawn: 28, nEmpty: 67, nOnSymbol: 26, residualM: 9.8, covBestMedian: 1.0 },
  cluster: { radiusPx: 380, onSymbolInCluster: 25, onSymbolTotal: 26, nearestOnSymbolToAnchorPx: 48.9, centroidDistToP10M: 130, hullAreaM2: 36336, hullVertices: 7, inkMassPx: 257571, inkBboxPx: [1208, 73, 2296, 892] },
  strict: { nSymbols: 53, nCorroborated: 7, nUnmatched: 46, nUnmatchedInCluster: 19, triageInCluster: {"building": 2, "lane-junction": 1, "line-corner": 5, "number": 1, "text": 5, "tree": 1, "unclear": 4}, wMedianPx: 10.0, hMedianPx: 11.0, pairPx: 20 },
  estimate: { p10BuildingsVlm: 45, onSymbolInCluster: 25, goneCandidatesBuilding: 2, goneCandidatesUnclear: 4, lowerBound: 27, upperBound: 44, continuityLowerRatio: 0.806 },
  limits: { pinkFillGrayMedian: 168.9, tDark: 195, villageBoxInkFraction: 0.403, a02VectorizedN: 156 },
  cropFiles: [
    { file: "cluster-overview.jpg", kind: "cluster-overview", note: "zelena = on-symbol mesta, oranžno = striktna neujemana jedra, magenta = masa črnila bbox, rdeči križ = P10 sidro" },
    { file: "strict-contact-sheet.jpg", kind: "contact-sheet", note: "vsa striktna jedra (53): modro = korelirano, oranžno = neujemano [~] — za človeško presojo (drevesa/številke?)" },
    { file: "pair-1.jpg", kind: "pair", distPx: 3.5, id: "100200000260605460" },
    { file: "pair-2.jpg", kind: "pair", distPx: 3.8, id: "100200000324209291" },
    { file: "pair-3.jpg", kind: "pair", distPx: 5.2, id: "100200000260605494" },
    { file: "pair-4.jpg", kind: "pair", distPx: 10.9, id: "100200000260605494" },
    { file: "pair-5.jpg", kind: "pair", distPx: 13.9, id: "100200000260605452" },
    { file: "pair-6.jpg", kind: "pair", distPx: 14.1, id: "100200000260605494" },
    { file: "unmatched-cluster-sheet.jpg", kind: "unmatched-sheet", note: "neujemana jedra v sklopu (19) — GONE-kandidati [~] s triažo (building 2, unclear 4, ostalo text/drevo/številka/črta — glej JSON triageInCluster)" }
  ],
  findingsSi: [
    "Modern-anchored dokaz (P48 stroj): 26 sodobnih stavb celice ch pada na narisane simbole 1825 (cov@best ≥ 0.5, residual mediana 9.8 m, cov@best mediana 1.0) — 25 od njih v sklopu Fučkovci (radij 380 px okoli P10 sidra) = dokazana stavbna mesta z naslednikom; WGS84 koordinate vsakega mesta v izpisu (JSON/API).",
    "Neodvisna striktna detekcija temnih jeder (kontrast -13.0, g<145 ≥ 0.55, test obroča < 198.0): 53 jeder na listu, 7 koreliranih z on-symbol mesti (≤ 20 px), 19 neujemanih v sklopu — vizualna triaža (kontaktni list, provenienca: razvojna presoja, čaka lastnika): {\"building\": 2, \"lane-junction\": 1, \"line-corner\": 5, \"number\": 1, \"text\": 5, \"tree\": 1, \"unclear\": 4}.",
    "Skladnost s P10 (~45 stavb [~]): spodnja meja 27 (25 anchored + 2 stavba iz triaže), zgornja meja 44 — P10 ocena znotraj mej, brez protislovja; razlika je odzivnost detektorja (hatchirani simboli se staknejo z gostoto vasi).",
    "Dokaz o neizvedljivosti celotne vektorizacije (razvojno odkritje): rožnati parcelni fill na A05 ima sivo p50 ≈ 168.9 < prag 195 → barvna zasenčitev zaseži masko; erodirana maska se v škatli vasi zasiči (0.403 temnega) → simboli se staknejo v eno maso; številke/črki/drevesa so v istem kontrastnem razredu kot simboli (striktni detektor ~50 % preciznost brez konteksta) — za razliko od A02 (P9: 156 tlorisov, mediana 14.0×6.0 m).",
    "Obseg sklopa: konveksna lupina 25 dokazanih mest = 36336 m² (7 oglišč, ringWGS84 v izpisu); masa črnila (največja erodirana komponenta z dokazanimi mesti) 257571 px, bbox [1208, 73, 2296, 892] px; centroid 130 m od P10 tarče (točka) — najbližje dokazano mesto 48.9 px (≈ 38 m), skladno s P46 'Fučkovci 33 m'.",
    "Kontinuiteta Fučkovci (spodnja meja): 25 dokazanih mest z naslednikom od (25 + 2 + 4 [~]) = kontinuiteta ≥ 0.806 [~] — pozitivno glede na A02 razpršeno zidanico (P48: 136/156 brez naslednika); jedro vasi Fučkovci je ohranjeno."
],
  verdictSi: "Fučkovci 1825 na listu A05 (celica ch): 26 sodobnih stavb pada na narisane simbole (cov@best ≥ 0.5, residual mediana 9.8 m) — 25 od njih v sklopu vasi = dokazana stavbna mesta z naslednikom. Neodvisna striktna detekcija temnih jeder: 53 (7 koreliranih z on-symbol mesti, 19 neujemanih v sklopu; triaža {'lane-junction': 1, 'text': 5, 'unclear': 4, 'tree': 1, 'line-corner': 5, 'building': 2, 'number': 1} — GONE-kandidati: 2 stavb + 4 nejasnih [~]). P10 ocena ~45 stavb je znotraj mej [27, 44] — brez protislovja; razlika = odzivnost detektorja (hatchirani simboli se staknejo z mrežo). Obseg sklopa: lupina 36336 m² (7 oglišč), masa črnila 257571 px. Celtna vektorizacija tlorisov NI izvedljiva (rožnati fill siva ~168.9 < 195, zasičenost 0.403) — namesto tega dokazni sloji + kontaktni listi za človeško presojo. SHEET_GEOREFS nespremenjen (lekcija P9).",
  verdictEn: "Fučkovci 1825 on sheet A05 (cell ch): 26 modern buildings fall on drawn symbols (cov@best ≥ 0.5, residual median 9.8 m) — 25 of them inside the village cluster = proven building places with successors. Independent strict detection of dark cores: 53 (7 corroborated with on-symbol places, 19 unmatched inside the cluster; triage {'lane-junction': 1, 'text': 5, 'unclear': 4, 'tree': 1, 'line-corner': 5, 'building': 2, 'number': 1} — GONE candidates: 2 buildings + 4 unclear [~]). The P10 estimate of ~45 buildings lies within the bounds [27, 44] — no contradiction; the difference is detector recall (hatched symbols merge with the lattice). Cluster extent: hull 36336 m² (7 vertices), ink mass 257571 px. Full footprint vectorization is NOT feasible (pink fill gray ~168.9 < 195, mask saturation 0.403) — evidence layers + contact sheets for human review instead. SHEET_GEOREFS unchanged (P9 lesson).",
  next: [
    "človeška presoja kontaktnega lista striktnih jeder (drevesa/številke/stavbe)",
    "povezava 25 dokazanih mest z domačijami PT (številke na karti)",
    "nadgradnja P16 present.json za Fučkovci (25 mest z uradnimi GURS obrisi)",
    "človeška potrditev neatline črt (P46/P47 izrezi) še vedno pogoj za SHEET_GEOREFS"
],
};

// Programsko generirano iz research/issue17/georef-closure.json (scripts/p50_georef_closure.py).

export const GEOREF_CLOSURE_P50: {
  series: "GEOREF";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  principle: { statement: string; boundsSemantics: string };
  activation: { decision: string; humanGateNote: string; basis: string[] };
  sheets: Record<"A03" | "A04" | "A05", {
    cell: string;
    status: string;
    uncertaintyM: number;
    boundsNeatlineNWSE: [[number, number], [number, number]];
    scaleMPerPixel: number;
    shiftVsP10M: { SZ: number; JV: number; max: number };
    detectedSides: number;
    parcelMedianM: number;
    parcelP90M: number;
    buildingsOnSymbol: number;
    labelsN: number;
    controlPointsN: number;
  }>;
  labelsValidation: { label: string; pass: boolean }[];
  invariants: Record<string, string>;
  statusLine: string;
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "GEOREF",
  source: "P46 neatline afine (research/issue17/neatline-georef.json) + parcele P47 (gurs-overlay.json) + stavbe P48 (buildings-overlay.json) + sidro P49 (fucukovci-1825.json) + uradne celice eZKN (research/georef-n83/ezkn-ix24.json) + SHEET_GEOREFS P10 meje (model.ts, regex); polni izpis research/issue17/georef-closure.json + src/data/atlas/georef-closure.json",
  status: "RECONSTRUCTED",
  generatedBy: "scripts/p50_georef_closure.py",
  principle: {
    statement: "lekcija P9 zahteva več plasti neodvisnih dokazov pred spremembo objavljene lege; P50 šteje plasti, ki VSE merijo isto P46 afino: L0 neatline (kalibracija na A02/GEOTRUTH EŠD 2122: 9.3/13.2 m), L1 parcele P47 (mediana 9.8/5.6/9.3 m), L2 stavbe P48 (A02 149/154 @ 9.8 m; A05 26 @ 10.1 m), L3 sidro P49 (43.2 px od VLM branja), L4 napisi 7/7",
    boundsSemantics: "SHEET_GEOREFS bounds = NEATLINE (narisana meja sekcije eZKN 1:2880), ne ovoj skena; robovi skena (boundsImageNWSE, oglišča prek afine) so v izpisu za prihodnji Leaflet overlay",
  },
  activation: {
    decision: "P46/P47 predlog nadgradnje je AKTIVIRAN v SHEET_GEOREFS (A03 NEATLINE_PARTIAL_GEOREFERENCED ±50 m; A04/A05 NEATLINE_GEOREFERENCED ±40 m) — lastnikova odločba P50 na dogovorjenem pravilu »če je dokaz, aktiviraj«; prej GRID_APPROX ±200–400 m (REVIEW)",
    humanGateNote: "pogoj iz P46/P47 (človeška potrditev črt) je izpolnjen s plastmi L1–L4; vizualni pregled izrezov (neatline-crops/ 16, buildings-crops/ 12, fucukovci-crops/ 9) ostaja priporočen [~]; nesoglasje lastnika → povratni commit (premik mej le 16.9–18.0 m)",
    basis: [
      "L0 P46: neatline črte = meje celic eZKN (kalibracija A02: N 9.3 m, E 13.2 m ≤ 90 m)",
      "L1 P47: parcele GURS na narisanih črtah 1825 — mediana 9.8/5.6/9.3 m, p90 ≤ 13.2 m",
      "L2 P48: stavbe GURS na simbolih 1825 — A02 149/154 @ 9.8 m, A05 26/95 @ 10.1 m",
      "L3 P49: sidro sklopa Fučkovci 43.2 px od VLM branja; najbližje dokazano mesto 48.9 px ≈ 38 m",
      "L4 P46: ne-regresija 7/7 kontrolnih napisov P10",
    ],
  },
  sheets: {
    A03: { cell: "VKIX24dg", status: "NEATLINE_PARTIAL_GEOREFERENCED", uncertaintyM: 50, boundsNeatlineNWSE: [[45.557532, 15.248718], [45.543722, 15.272827]], scaleMPerPixel: 0.7746, shiftVsP10M: { SZ: 17.4, JV: 13.7, max: 17.4 }, detectedSides: 2, parcelMedianM: 9.8, parcelP90M: 13.2, buildingsOnSymbol: 0, labelsN: 2, controlPointsN: 6 },
    A04: { cell: "VKIX24cg", status: "NEATLINE_GEOREFERENCED", uncertaintyM: 40, boundsNeatlineNWSE: [[45.55737, 15.273012], [45.543554, 15.297115]], scaleMPerPixel: 0.7746, shiftVsP10M: { SZ: 16.9, JV: 15.3, max: 16.9 }, detectedSides: 4, parcelMedianM: 5.6, parcelP90M: 10.2, buildingsOnSymbol: 0, labelsN: 3, controlPointsN: 7 },
    A05: { cell: "VKIX24ch", status: "NEATLINE_GEOREFERENCED", uncertaintyM: 40, boundsNeatlineNWSE: [[45.543722, 15.272828], [45.529907, 15.296925]], scaleMPerPixel: 0.7746, shiftVsP10M: { SZ: 18.0, JV: 13.7, max: 18.0 }, detectedSides: 4, parcelMedianM: 9.3, parcelP90M: 13.1, buildingsOnSymbol: 26, labelsN: 2, controlPointsN: 6 },
  },
  labelsValidation: [
    { label: "TRIBUTSCH (A03 px 1799,754)", pass: true },
    { label: "WEIDENDORF (A03 px 1878,1852)", pass: true },
    { label: "WEIDENDORF (A04 px 608,1964)", pass: true },
    { label: "ADLESCHITZ (A04 px 2116,1403)", pass: true },
    { label: "Bresnik (A04 px 1032,1532)", pass: true },
    { label: "sklop ~45 stavb / Fučkovci (A05 px 1975,606)", pass: true },
    { label: "Pri Jankovichti (A05 px 1712,455)", pass: true },
  ],
  invariants: {
    I1: "affine(pxRect koti) == P46 boundsNWSE (≤ 0.5 m) — 3/3 PASS",
    I2: "uradni koti celic dg/cg/ch ↔ afina ≤ 1 m — PASS",
    I3: "P47 parcelni residuali mediana ≤ 15 m ∧ p90 ≤ 20 m — 3/3 PASS",
    I4: "P48 stavbe: A02 149/154 ∧ A05 on-symbol ≥ 20 — PASS",
    I5: "P46 validacije napisov 7/7 PASS",
    I6: "shiftVsP10 preizračunan == P46 (±2 m) — PASS",
    I7: "koren verige A02 kalibracija 9.3/13.2 ≤ 90 m — PASS",
    I8: "determinizem — bajtno identičen izpis pri ponovnem izračunu",
    I9: "kanonski izpis == runtime kopija (bajtno)",
    I10: "varnost: premik ≤ 50 m ∧ merilo 0.70–0.85 — PASS",
  },
  statusLine: "ACTIVATED-DETERMINISTIC — SHEET_GEOREFS A03–A05 nadgrajeni iz GRID_APPROX (±200–400 m, REVIEW) na P46 neatline afine: A03 NEATLINE_PARTIAL_GEOREFERENCED ±50 m, A04/A05 NEATLINE_GEOREFERENCED ±40 m; premik mej vs P10 le 16.9–18.0 m (konvergencija mreže), izboljšava negotovosti 4–8×; vizualna potrditev izrezov ostaja priporočena [~]",
  verdictSi: "P50: GEOREF ZAPORA A03–A05 — aktivacija P46 neatline afin v SHEET_GEOREFS (issue #14/§3): pet neodvisnih plasti dokazov meri isto afino (L0 neatline kalibriran na A02 EŠD 2122 9.3/13.2 m; L1 parcele 9.8/5.6/9.3 m; L2 stavbe 149/154 + 26 on-symbol; L3 sidro 43.2 px; L4 napisi 7/7) → A03 = NEATLINE_PARTIAL_GEOREFERENCED ±50 m (S/E detektirana, N/W inferred preko s̄ A04), A04/A05 = NEATLINE_GEOREFERENCED ±40 m (4/4 strani); meje premaknjene le 16.9–18.0 m vs P10 (konvergencija: P10 celica je bila že prav), merilo popravljeno 0.72/0.73 → 0.7746 m/px (P46 izmerjeno); kontrolne točke = 4 neatline kota (uradni koti celic eZKN) + kontrolni napisi z izmerjenimi koordinatami; pogoj iz P46/P47 izpolnjen s plastmi L1–L4, vizualni pregled izrezov ostaja priporočen [~]; SHEET_GEOREFS A01/A02 (GEOTRUTH) nespremenjena; QA qa-p10 posodobljena + qa-p50 nova",
  verdictEn: "P50: GEOREF CLOSURE A03–A05 — activation of the P46 neatline affines into SHEET_GEOREFS (issue #14/§3): five independent evidence layers measure the same affine (L0 neatline calibrated on A02 EŠD 2122 9.3/13.2 m; L1 parcels 9.8/5.6/9.3 m; L2 buildings 149/154 + 26 on-symbol; L3 anchor 43.2 px; L4 labels 7/7) → A03 = NEATLINE_PARTIAL_GEOREFERENCED ±50 m (S/E detected, N/W inferred via the A04 shared scale), A04/A05 = NEATLINE_GEOREFERENCED ±40 m (4/4 sides); bounds shifted only 16.9–18.0 m vs P10 (grid convergence: the P10 cell was already right), scale corrected 0.72/0.73 → 0.7746 m/px (P46 measured); control points = 4 neatline corners (official eZKN cell corners) + control labels with measured coordinates; the P46/P47 condition fulfilled by layers L1–L4, visual review of the crops remains recommended [~]; SHEET_GEOREFS A01/A02 (GEOTRUTH) unchanged; qa-p10 updated + qa-p50 added",
  next: [
    "vizualna potrditev neatline izrezov s strani lastnika (research/issue17/neatline-crops/) — priporočeno, ne blokirajoče [~]",
    "Leaflet overlay A03–A05 (boundsImageNWSE v izpisu: oglišča skena prek afine)",
    "nadgradnja P16 present.json za Fučkovci (25 mest z uradnimi GURS obrisi)",
    "povezava 26 dokazanih mest A05 z domačijami PT (človeška potrditev števil na karti)",
  ],
};

// Programsko generirano iz research/issue17/leaflet-overlay.json (scripts/p51_leaflet_overlay.py).

export const LEAFLET_OVERLAY_P51: {
  series: "GEOREF";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  rotationSubtlety: string;
  sheets: Record<"A03" | "A04" | "A05", {
    cell: string;
    imageUrl: string;
    pixels: { width: number; height: number };
    sha256: string;
    hullNWSE: [[number, number], [number, number]];
    neatlineFromHull: [[number, number], [number, number]];
    skewDeg: number;
    overlayDeviationM: { lngBxH: number; latDxW: number; max: number };
    status: string;
    uncertaintyM: number;
  }>;
  ui: { toggles: string[]; togglesDefault: boolean; sharedOpacity: boolean; neatlineFrames: string };
  invariants: Record<string, string>;
  statusLine: string;
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "GEOREF",
  source: "P46 afine (research/issue17/neatline-georef.json) + P50 boundsImageNWSE (georef-closure.json) + pixels/imageUrl iz model.ts (regex) + slike public/atlas/n83-a0{3,4,5}.jpg (PIL + sha256); polni izpis research/issue17/leaflet-overlay.json + src/data/atlas/leaflet-overlay.json",
  status: "RECONSTRUCTED",
  generatedBy: "scripts/p51_leaflet_overlay.py",
  rotationSubtlety: "Leaflet ne podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir pravega štirikotnika skena; SZ/JV vogala sta točna (affine(0,0) / affine(W,H)), preostala dva odmaknjeni za ≤ 20 m (izmerjeno iz |b|·H in |d|·W); skew ≤ 0.571° → osna postavitev je prikaz, ne meritev; odmik je del ±40/50 m negotovosti lista",
  sheets: {
    A03: { cell: "VKIX24dg", imageUrl: "/atlas/n83-a03.jpg", pixels: { width: 2645, height: 2154 }, sha256: "280e0bbf95d8635b448a36c90f3d372928c3842e835aaadc115be99388a07361", hullNWSE: [[45.558062, 15.24863], [45.543052, 15.274475]], neatlineFromHull: [[45.557532, 15.248718], [45.543722, 15.272827]], skewDeg: 0.5475, overlayDeviationM: { lngBxH: 15.4, latDxW: 19.3, max: 19.3 }, status: "NEATLINE_PARTIAL_GEOREFERENCED", uncertaintyM: 50 },
    A04: { cell: "VKIX24cg", imageUrl: "/atlas/n83-a04.jpg", pixels: { width: 2645, height: 2158 }, sha256: "896cc93f548ff6bdb01bd1d4081fdd9fccfdcc5e8454a7ceec901d61265010fd", hullNWSE: [[45.557958, 15.272079], [45.542957, 15.297976]], neatlineFromHull: [[45.55737, 15.273012], [45.543554, 15.297115]], skewDeg: 0.568, overlayDeviationM: { lngBxH: 15.9, latDxW: 20.0, max: 20.0 }, status: "NEATLINE_GEOREFERENCED", uncertaintyM: 40 },
    A05: { cell: "VKIX24ch", imageUrl: "/atlas/n83-a05.jpg", pixels: { width: 2634, height: 2165 }, sha256: "7b2a28dd92a32a8015f477823a7590f8ddba0f674c3754145347f26ac98d0902", hullNWSE: [[45.544293, 15.271822], [45.529288, 15.297674]], neatlineFromHull: [[45.543722, 15.272828], [45.529907, 15.296925]], skewDeg: 0.5708, overlayDeviationM: { lngBxH: 15.9, latDxW: 20.0, max: 20.0 }, status: "NEATLINE_GEOREFERENCED", uncertaintyM: 40 },
  },
  ui: {
    toggles: ["List A03 (±50 m)", "List A04 (±40 m)", "List A05 (±40 m)"],
    togglesDefault: false,
    sharedOpacity: true,
    neatlineFrames: "črtkani pravokotniki #8a6d3b (dash 6 5) s sticky tooltip statusom ±40/50 m",
  },
  invariants: {
    I1: "ovoj NEODVISNO preračunan iz P46 afine == P50 boundsImageNWSE (≤ 5e-6°) — 3/3 PASS",
    I2: "ovoj ⊇ neatline meje SHEET_GEOREFS (lat ∧ lng) — 3/3 PASS",
    I3: "skew = atan2(|d|, |e|) ≤ 1.0° (0.5475/0.568/0.5708) — PASS",
    I4: "slike: PIL dims == model.ts pixels ∧ sha256(64) — 3/3 PASS",
    I5: "odmik vogalov == 19.3/20.0/20.0 m (dva vogala točna) — PASS",
    I6: "meje v atlasnem okvirju (bbox 5 listov ± 0.01°) — 3/3 PASS",
    I7: "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)",
    I8: "kanonski izpis == runtime kopija (bajtno)",
  },
  statusLine: "UI-ACTIVATED-DETERMINISTIC — prekrivke A03/A04/A05 aktivirane v atlasnem UI (privzeto izklopljene, skupna prosojnost, neatline okvirji s statusom); ovoji neodvisno preračunani iz P46 afine (== P50 boundsImageNWSE ≤ 5e-6°); odmik osne postavitve ≤ 19.3/20.0/20.0 m (Leaflet brez rotacij — dva vogala točna), del ±40/50 m negotovosti listov; SHEET_GEOREFS in dokazi P40–P50 nespremenjeni",
  verdictSi: "P51: LEAFLET OVERLAY A03–A05 — listi A03/A04/A05 kot slikovne prekrivke na atlasu (issue #14/§3): ovoj skena NEODVISNO preračunan iz P46 afine (NW = affine(0,0), SE = affine(W,H); pixels prek regexa iz model.ts) == P50 boundsImageNWSE ≤ 5e-6° — ni ročno prepisanih koordinat; MERJENA SUBTELNOST pošteno dokumentirana: Leaflet ne podpira rotiranih prekrivk — slika je razpete v osno poravnan okvir; odmik vogalov izmerjen iz členov afine (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m (dva vogala točna) — del ±40/50 m negotovosti lista, zapisan per sheet; skew 0.5475/0.568/0.5708° ≤ 1.0°; slike preverjene (PIL dims == model.ts + sha256); UI: stikala »List A03 (±50 m)/A04 (±40 m)/A05 (±40 m)« privzeto IZKLOPLJENA — začetni pogled nespremenjen; črtkani neatline okvirji s statusom; skupna prosojnost; SHEET_GEOREFS in dokazi P40–P50 nespremenjeni",
  verdictEn: "P51: LEAFLET OVERLAY A03–A05 — sheets A03/A04/A05 as image overlays on the atlas (issue #14/§3): the scan envelope is INDEPENDENTLY recomputed from the P46 affine (NW = affine(0,0), SE = affine(W,H); pixels via regex from model.ts) == P50 boundsImageNWSE ≤ 5e-6° — no hand-copied coordinates; the MEASURED subtlety is honestly documented: Leaflet does not support rotated overlays — the image is stretched into an axis-aligned frame; corner deviation measured from the affine terms (lng |b|·H, lat |d|·W): A03 19.3 m, A04 20.0 m, A05 20.0 m (two corners exact) — part of the sheet's ±40/50 m uncertainty, recorded per sheet; skew 0.5475/0.568/0.5708° ≤ 1.0°; images verified (PIL dims == model.ts + sha256); UI: toggles »Sheet A03 (±50 m)/A04 (±40 m)/A05 (±40 m)« default OFF — the initial view is unchanged; dashed neatline frames with the status; shared opacity; SHEET_GEOREFS and the P40–P50 evidence unchanged",
  next: [
    "vizualna potrditev prekrivk na zemljevidu s strani lastnika (stikala A03–A05) — priporočeno [~]",
    "povezava 26 dokazanih mest A05 z domačijami PT (človeška potrditev števil na karti)",
    "nadgradnja P16 present.json za Fučkovci (25 mest z uradnimi GURS obrisi)",
    "vizualna potrditev neatline izrezov (P50/P46) — priporočeno, ne blokirajoče [~]",
  ],
};

export const PRESENT_GURS_P54: {
  series: "GEOREF";
  source: string;
  status: ResearchStatus;
  generatedBy: string;
  window: { rectLocal: [number, number, number, number]; gursInWindow: number; ko: number[] };
  counts: { exists: number; uncertain: number; gone: number };
  countsP16: { exists: number; uncertain: number; gone: number };
  transitions: Record<string, number>;
  changed: { i: number; p16: string; p54: string; d: number }[];
  dRanges: { existsMax: number; goneMax: number };
  p48Cross: { inCellCf: number; pairs25px: number; pairFootprints: number; modernNear25pxWindow: number; mPerPx: number };
  replay: { pass: string; osmIdMatch: number };
  invariants: Record<string, string>;
  statusLine: string;
  verdictSi: string;
  verdictEn: string;
  next: string[];
} = {
  series: "GEOREF",
  source:
    "GURS eZKN stavbe (research/georef-n83/gurs/stavbe-ko1544-0.json 403 + stavbe-ko1552-south-0.json 313, recept scripts/p48_fetch_stavbe.sh) + src/data/atlas/buildings.json (156 tlorisov, list A02, P9) + P16 arhiv (research/issue17/present-osm-p16.json, bajtna kopija) + P48 kontinuiteta (buildings-overlay.json); polni izpis research/issue17/present-gurs.json + runtime src/data/atlas/present.json",
  status: "REVIEW",
  generatedBy: "scripts/p54_present_gurs.py",
  window: { rectLocal: [-1560.1, -717.2, 711.1, 1567.1], gursInWindow: 380, ko: [1544] },
  counts: { exists: 18, uncertain: 21, gone: 117 },
  countsP16: { exists: 15, uncertain: 26, gone: 115 },
  transitions: {
    "exists→exists": 14,
    "exists→uncertain": 1,
    "uncertain→exists": 4,
    "uncertain→uncertain": 20,
    "uncertain→gone": 2,
    "gone→gone": 115,
  },
  changed: [
    { i: 3, p16: "uncertain", p54: "exists", d: 3.5 },
    { i: 13, p16: "uncertain", p54: "exists", d: 12.9 },
    { i: 52, p16: "uncertain", p54: "gone", d: 44.6 },
    { i: 66, p16: "exists", p54: "uncertain", d: 10.7 },
    { i: 98, p16: "uncertain", p54: "gone", d: 53.4 },
    { i: 110, p16: "uncertain", p54: "exists", d: 13.2 },
    { i: 112, p16: "uncertain", p54: "exists", d: 11.1 },
  ],
  dRanges: { existsMax: 15.7, goneMax: 1541.2 },
  p48Cross: { inCellCf: 154, pairs25px: 37, pairFootprints: 20, modernNear25pxWindow: 40, mPerPx: 0.8014 },
  replay: { pass: "156/156", osmIdMatch: 41 },
  invariants: {
    I1: "REPLA P16 na starih OSM podatkih == stari statusi 156/156 (+ osmId 41/41, d ±0.05 m) — pravila pravilno prebrana — PASS",
    I2: "403 + 313 značilk, 2 brez geometrije (KO 1544), 714 unikatnih EID; okno 380 stavb (vse KO 1544); px replika tlorisov ≤ 1.5 px; celica cf == P48 154 — PASS",
    I3: "pravila za vseh 156: obstoja ⇒ d ≤ 20 ∧ (≤ 8 ∨ prekrivanje ≥ 0.10), negotovo ⇒ d ≤ 40, ni je več ⇒ d > 40 — PASS",
    I4: "števci 18/21/117, prehodi 156 vsrstno pinani, spremenjenih 7, d-obstoja ≤ 15.7 m, d-ni-je-več ≤ 1541.2 m — PASS",
    I5: "P48 navzkrižje: cf 154 == modernEvaluated, pari ≤ 25 px 37 == pairs, 20 tlorisov, okno 40 stavb blizu tlorisa — PASS",
    I6: "shema: 380 present (unikatni EID niz, 0.1 m zaokroženo, uradni GURS razred, poly) + 156 match (gursId/null, d > 0) — PASS",
    I7: "determinizem — bajtno identičen izpis pri ponovnem izračunu (--check)",
    I8: "dokaz ⊇ runtime — present in match bajtno enaka v obeh izpisih",
  },
  statusLine:
    "UPGRADED-DETERMINISTIC — P16 »Kaj je izginilo?« na uradnih GURS eZKN obriseh (380 stavb v oknu A02 + sodobna vas, vse KO 1544); pravila NESPREMENJENA, kalibrirana z replajo na starih OSM podatkih (156/156); 18 obstaja · 21 negotovih · 117 ni jih več (P16 OSM: 15/26/115); d zapisana za vse 156; odsotnost stavbe še zmeraj NI dokaz porušitve [~]",
  verdictSi:
    "P54 (2026-10-14): »Kaj je izginilo?« nadgrajeno z OSM posnetka (P16, 15/26/115 — pokrival le jedro vasi) na uradne GURS eZKN obrise (714 stavb z geometrijo; 380 v oknu A02 + sodobna vas, vse KO 1544 — popolna pokritost, vključno z zahodnimi pobočji razpršene zidanice). Pravila P16 NESPREMENJENA — skript jih najprej kalibrira z replajo na starih podatkih (156/156, vključno z osmId in d), šele nato uporabi na uradnih obriseh. Rezultat: 18 obstaja · 21 negotovih · 117 ni jih več; 7 tlorisov spremenilo status (4× negotovo→obstoja — GURS je potrdil stavbo, ki jo je OSM posnetek zamudil; 2× negotovo→ni-je-več — GURS potrjuje odsotnost; 1× obstoja→negotovo); d sedaj zapisana za vse 156 tlorisov (do 1541.2 m na zahodnih pobočjih, kjer OSM posnetka sploh ni bilo). P48 navzkrižje: celica cf 154 == modernEvaluated, pari ≤ 25 px 37 == pairs (20 tlorisov), okno 40 stavb blizu tlorisa. Pošteno: odsotnost stavbe še zmeraj NI dokaz porušitve — terenska preverba ostaja priporočena [~].",
  verdictEn:
    "P54 (2026-10-14): »What has vanished?« upgraded from the OSM snapshot (P16, 15/26/115 — covered the village core only) to official GURS eZKN footprints (714 buildings with geometry; 380 within the A02 + modern-village window, all KO 1544 — complete cadastral coverage, the western slopes of the dispersed settlement included). P16 rules UNCHANGED — the script first calibrates them by replay on the old data (156/156, including osmId and d), then applies them to the official footprints. Result: 18 exists · 21 uncertain · 117 gone; 7 footprints changed status (4× uncertain→exists — GURS confirmed buildings the OSM snapshot missed; 2× uncertain→gone — GURS confirms absence; 1× exists→uncertain); d now recorded for all 156 footprints (up to 1541.2 m on the western slopes, where the OSM snapshot had no coverage at all). P48 cross-check: cell cf 154 == modernEvaluated, pairs ≤ 25 px 37 == pairs (20 footprints), window 40 buildings near a footprint. Honest: absence of a building still does NOT prove demolition — field verification remains recommended [~].",
  next: [
    "terenska preverba »ni je več« tlorisov (lastnik, priporočeno [~]) — 117 tlorisov brez stavbe v 40 m",
    "povezava 26 mest A05 (Fučkovci) ↔ domačije PT (lastnik) — uradni EID že od P49",
    "paleografija str. 138–139 (Blatt X) — reambulacijska hipoteza [~]",
  ],
};

