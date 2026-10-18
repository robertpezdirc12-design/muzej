#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P103 — župnija Podzemelj: krstna knjiga 04105, polno leto 1908 (issue #18).

Razširitev vzorca P79 (1886) → … → P100 (1905) → P101 (1906) → P102 (1907) na
leto 1908: okvir glava »Leto 18 1908« na str. 173 = skeni 189/190 (dup par;
1908 r1 = Krasinec 38(?) August, 1./1. Januar — P102 lead POTRJEN; hiša
forenzika 38 vs lead 58) – row 90 na str. 180 (sken 199; glava »1909« INLINE
na r91 = isti sken; 1909 r1 = Dobraviče 26 Anton, 7./7. Januar — P104 lead).
90 oštevilčenih vrstic. NOVELA P103 — TRIJE novi dup pari: 189/190 = str. 173
+ 193/194 = str. 176 + 197/198 = str. 179 (vsi trije z berljivimi
dopolnitvami: r6 na 190, r47 na 194, r79 na 198). Stran == sken − 16 (189) /
− 17 (190–193) / − 18 (194–197) / − 19 (198–199). VSI vpisi z Griblji: 19
vpisov / 18 hiš + 1 neberljiva (r84 — POSTRGAN rob str. 179, papir fizično
manjka na obojih dup skenih; pričevanje-samo brez vitals bloka) — NARE 18/18
(po 1907 prelomu h10 ×2 spet brez intra-letne ponovitve). 0 NOVIH hiš (4. leto
z 0: 1905 0/1906 1/1907 0/1908 0 — VSE 18 hiš že zasidrane). PT 12/6 (44+46+49
+52+56+60 v luknji 41–60 — ponovitve; luknja ostaja samo h51). Kumulativ s
P79–P102: 382 vpisov / 85 hiš / DVAINDVAJSET+ENO let (1886–1908).
Sidra: r16 h14 4. VPIS ISTA familija (BRINEC; botra = babica ISTA Barbara
Adlešič ×2!); r22 h60 8. VPIS ISTA ZVEZA (Željko × Brodarič — 5. OTROK;
PRESTOPNI 29. 2.!); r23 h24 13. VPIS (najbolj vpisovana; NOV DUHOVNIK Jos.
Dami!); r27 h16 8. VPIS (NOVAK bajtar POVRAT cf. 1900; CROSS-ROW boter Janez
Muc kovač = r31 h91 oče!); r31 h91 5. VPIS ISTA (Muc bajtar × Ana Kure; EMŠO
2204908500557 sidro; pripisno neskladje poroke); r41 h85 2. VPIS — NUJNI KRST
(»v sili krščen?«; botra + podpis PRAZNA; VRZEL 20 LET; dojenček † 29.5.1908);
r46 h52 3. VPIS — ISTA ZVEZA čez 10 LET (Podrinc/Pendirec ≈ Pezdirec +
Jakobič ≈ Jakobčič); r47 h44 5. VPIS (Štrucelj ISTA oče cf. 1906; botrinja
Doroteja = r69 mati CROSS-ROW; forenzika na dup skenu 194); r55 h23 7. VPIS —
ISTA ZVEZA čez 8 LET (Brinec? × Marija Dehlič — MATI ISTA kot 1900; celica
RAZTRGANA); r57 h65 9. VPIS — MILEK 1887–1908 (boter Peter Pezdirec ISTA kot
1887 — 21 LET!); r65 h46 6. VPIS (ISTA OČE Anton Brodarič cf. 1893–99 — VRZEL
9 LET; EMŠO 0310908500848); r66 h30 11. VPIS — SEGINA POVRAT (mati Katarina
Brinec ISTA kot 1903; EMŠO 0410908500444); r68 h49 4. VPIS ISTA (Brodarič;
EMŠO 0810908505763; boter Jurij Pezdirec 1./3); r69 h56 3. VPIS — VRZEL 20
LET (NOVA družina Jerčinovič? × Štrucelj; boter Jurij Pezdirec 2./3); r70 h36
11. VPIS — KRIŽAN POVRAT (ISTA zveza cf. 1894–1902; boter Matija Štraus); r79
h90 5. VPIS — TRETJA UČITELJSKA DRUŽINA (Kopitar → Vetročnik → Kalan!; EMŠO
— brez; boter Jurij Pezdirec 3./3); r88 h11 5. VPIS ISTA familija (Žumič;
babica Vötter VRNITEV; EMŠO 2612908500224); r90 h10 4. VPIS — BRINEC ISTA
(mati menjava Ana Klepec? → Ana Kure; ISTI boter par kot 1907 r85; EMŠO
2812908500042; ZADNJA vrstica 1908).
DUHOVNIKI NOVELA (na Gribljih 18 berljivih + r84): Gregor Cerar 12 + NOV
DUHOVNIK Jos. Dami 1 (r23; 2. podpis v letu = r18) + Jos. Ravq 4 (r65/r68/
r79/r84) + PRAZEN 1 (r41 NUJNI KRST); na 1909 r1 »P. Gregor Cerar coop.« (NE
na Gribljih). BABICA NOVELA: 18/18 imenovanih — Muc 6 + Adlešič 8 (Barbara 7
+ Marija 1) + Meh 2 + Vötter 1 (VRNITEV po 1907 0×!) + Mavrenič 1 + Mehrič?
1; MIH 0× (2. leto zapored). EMŠO kampanja: 6 sidr na Gribljih — VSI SKLADNI.
Anomalije: r41 nujni krst; r84 postrgan rob; r89 pod trakom (B-stran Matija
Muc × Marija Gregorič); r55 raztrgana očetova celica; CROSS-ROW ×3; žig
»FRIEDMANN« str. 179; prestopni 29. 2. 1908 (r22); kraj forenzika r28
Prilozje? + r42 Škrilje + r59 Štriglje? + r74 Prilozje 25. Excluded: 7.

Invarianta I1–I10; --check izpiše PASS/FAIL in vrne exit code.
"""
import json
import re
import sys
import base64
import urllib.request
import urllib.error

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04105/"
BOOK_SIGNATURE = "04105"
EXPECTED_IMAGES = 326
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-baptism-1908.json"
DOKAZ_P102 = "research/issue17/parish-baptism-1907.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (189, 199)        # skeni 189/190 (str. 173: glava 1908 + rows 1–12) – 199 (str. 180: rows 85–90 + glava 1909)
FRAME_PAGES = (173, 180)
DATA_SCANS = [189, 191, 192, 193, 195, 196, 197, 199]
EXPECTED_CITED = [189, 191, 192, 193, 195, 196, 197, 199]
EXPECTED_PAGES = [173, 174, 175, 176, 177, 178, 179, 180]
EXPECTED_ENTRIES = 19
EXPECTED_DISTINCT = 18          # 18 berljivih hiš (+1 neberljiva r84)
EXPECTED_EXCLUDED = 7           # r1 Krasinec, r28 Prilozje?, r42 Škrilje, r44 mrtvorojen, r59 Štriglje?, r74 Prilozje 25, r89 trak
EXPECTED_HOUSES = sorted({10, 11, 14, 16, 23, 24, 30, 36, 44, 46, 49, 52, 56, 60, 65, 85, 90, 91})
EXPECTED_VITALS_HOUSES = sorted([10, 11, 14, 16, 23, 24, 30, 36, 44, 46, 49, 52, 56, 60, 65, 85, 90, 91])
EXPECTED_PT_IN_SET = ["10", "11", "14", "16", "23", "24", "30", "36", "65", "85", "90", "91"]
EXPECTED_PT_GAP = ["44", "46", "49", "52", "56", "60"]  # ponovitve že dokazanih — luknja 41–60 ostaja samo h51
EXPECTED_REPEATS = 0            # NARE 18/18 — po 1907 prelomu spet brez ponovitev
EXPECTED_NEW_HOUSES = 0         # 4. leto z 0 novih (1905 0 / 1906 1 / 1907 0 / 1908 0)
EXPECTED_VITALS_TOTAL = 374     # HOUSE_VITALS 356 + 18 (P103: krstna 1908; r84 neberljiva brez bloka)
BLOCKS_04105 = 348              # 330 + 18
KUMULATIV_ENTRIES = 382         # 363 + 19
KUMULATIV_HOUSES = 85
KUMULATIV_YEARS = 23            # 1886–1908
# kontinuitete (hiša → zadnje krstno leto pred 1908 v 04105, iz parish.ts)
CONTINUITY = {
    "10": 1907, "11": 1907, "14": 1902, "16": 1906, "23": 1905, "24": 1906,
    "30": 1906, "36": 1904, "44": 1906, "46": 1899, "49": 1907, "52": 1898,
    "56": 1888, "60": 1906, "65": 1904, "85": 1888, "90": 1900, "91": 1904,
}
# sidra/pini P103 (row, scan, hiša, pin):
ANCHORS = [
    (16, 191, "14", "Brinec"),
    (16, 191, "14", "4. VPIS"),
    (22, 191, "60", "Željko"),
    (22, 191, "60", "8. VPIS"),
    (23, 191, "24", "13. VPIS"),
    (23, 191, "24", "Dami"),
    (27, 192, "16", "Novak"),
    (27, 192, "16", "8. VPIS"),
    (31, 192, "91", "Muc"),
    (31, 192, "91", "5. VPIS"),
    (41, 193, "85", "NUJNI KRST"),
    (41, 193, "85", "VRZEL 20 LET"),
    (46, 193, "52", "Pezdirec"),
    (46, 193, "52", "3. VPIS"),
    (47, 193, "44", "Štrucelj"),
    (47, 193, "44", "5. VPIS"),
    (55, 195, "23", "Dehlič"),
    (55, 195, "23", "7. VPIS"),
    (57, 195, "65", "Milek"),
    (57, 195, "65", "9. VPIS"),
    (65, 196, "46", "Brodarič"),
    (65, 196, "46", "6. VPIS"),
    (66, 196, "30", "Segina"),
    (66, 196, "30", "SEGINA POVRAT"),
    (68, 196, "49", "Brodarič"),
    (68, 196, "49", "4. VPIS"),
    (69, 196, "56", "Štrucelj"),
    (69, 196, "56", "VRZEL 20 LET"),
    (70, 196, "36", "Križan"),
    (70, 196, "36", "KRIŽAN POVRAT"),
    (79, 197, "90", "Kalan"),
    (79, 197, "90", "TRETJA UČITELJSKA"),
    (88, 199, "11", "Žumič"),
    (88, 199, "11", "Vötter"),
    (90, 199, "10", "Brinec"),
    (90, 199, "10", "4. VPIS"),
]
EMSO_ANCHOR_ROWS = {
    31: "2204908500557",
    65: "0310908500848",
    66: "0410908500444",
    68: "0810908505763",
    88: "2612908500224",
    90: "2812908500042",
}
GRIBLJE_MIH = 0                 # NOVELA: MIH 0× — 2. leto zapored
GRIBLJE_VOTTER = 1              # NOVELA: Vötter VRNITEV (1907 0×) — r88 Marjeta
GRIBLJE_CERAR = 12              # vključno r90
GRIBLJE_RAVQ = 4                # r65/r68/r79/r84
GRIBLJE_DAMI = 2                # r23 (Griblje) + r18 (Otok — v opombah)
GRIBLJE_EMPTY_PRIEST = 1        # r41 NUJNI KRST
MIDWIFE_NAMED = 18              # na Gribljih 18/18 (berljivih)
MIDWIFE_EMPTY = 0


def http_get(url, headers, tries=4):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read() if hasattr(e, "read") else b""
        except Exception as e:  # noqa: BLE001
            last = e
    raise last  # type: ignore


def decode_inventory(html):
    urls = []
    for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
        s = m.group(1)[7:-1]
        try:
            d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
            if d.startswith("http"):
                urls.append(d)
        except Exception:
            pass
    return sorted(set(urls))


def pt_house_set():
    d = json.load(open(PT_CHAIN, encoding="utf-8"))
    return {str(r["no"]).strip() for r in d["chain"] if r.get("kind") == "hiša"}


def parish_vitals_04105():
    src = open(PARISH_TS, encoding="utf-8").read()
    blocks = re.findall(r"\{[^{}]*?bookSignature:\s*\"" + BOOK_SIGNATURE + r"\"[^{}]*?\}", src, re.S)
    out = []
    for b in blocks:
        hn = re.search(r'houseNo:\s*"([^"]*)"', b)
        yr = re.search(r"year:\s*(\d+)", b)
        out.append({"houseNo": hn.group(1) if hn else None,
                    "year": int(yr.group(1)) if yr else None})
    return out


def page_of_scan(scan):
    """NOVELA P103: TRIJE novi dup pari (+ 178/179, 180/181, 183/184 že P101/P102).
    skeni 189/190 = str. 173 (dup par); 191 = str. 174; 192 = str. 175;
    193/194 = str. 176 (dup par); 195 = str. 177; 196 = str. 178;
    197/198 = str. 179 (dup par); 199 = str. 180. Glava 1909 = INLINE r91."""
    if scan in (189, 190):
        return 173
    if scan == 191:
        return 174
    if scan == 192:
        return 175
    if scan in (193, 194):
        return 176
    if scan == 195:
        return 177
    if scan == 196:
        return 178
    if scan in (197, 198):
        return 179
    if scan == 199:
        return 180
    return scan - 19


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p102 = json.load(open(DOKAZ_P102, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h != "?"]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + JPEG probe data skenov
    inv["I3_data_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in dokaz["source"]["scans"])
    probes = {}
    for s in DATA_SCANS:
        if s <= len(urls):
            try:
                st2, img = http_get(urls[s - 1], UA)
                probes[s] = st2 == 200 and img[:2] == b"\xff\xd8"
            except Exception:  # noqa: BLE001
                probes[s] = False
    inv["I3_jpeg_probes"] = all(probes.get(s, False) for s in DATA_SCANS)
    inv["I3_cited_scans"] = dokaz["source"]["scans"] == EXPECTED_CITED

    # I4 — okvir leta: glava 1908 na str. 173 = skeni 189/190 (dup par;
    # P102 dokazano) … row 90 (sken 199, str. 180); glava 1909 INLINE r91 =
    # isti sken; 90 vrstic; TRI dup pari; page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 189 and fr["yearStart"]["page"] == 173
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 199 and fr["yearEnd"]["page"] == 180
        and fr["yearEnd"]["row"] == 90
        and fr["rowsTotal"] == 90
        and fr["duplicateScans"]["count"] == 3
        and {(p["scans"][0], p["scans"][1], p["page"]) for p in fr["duplicateScans"]["pairs"]}
        == {(189, 190, 173), (193, 194, 176), (197, 198, 179)}
    ) and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
    inv["I4_glava_notes"] = (
        "POTRJEN" in fr["yearStart"]["note"]
        and "1909" in fr["yearEnd"]["note"]
        and fr["duplicateScans"]["count"] == 3
        and "P104 lead" in fr["glava1909"]["note"]
    )

    # I5 — štetja: 19 vpisov / 18 hiš + 1 neberljiva; 7 excluded; NARE 18/18
    # (0 ponovitev); 0 novih hiš; babica 18/18 + Vötter 1 + Mih 0;
    # EMŠO sidri r31/r65/r66/r68/r88/r90
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses_numeric)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 1
        and houses_written == EXPECTED_HOUSES
        and dokaz["stats"]["intraYearRepeats"] == EXPECTED_REPEATS
        and "NARE 18/18" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["babica"]["griblje"].startswith("18/18")
        and sum(1 for e in entries if "Vötter" in e["babica"]) == GRIBLJE_VOTTER
        and sum(1 for e in entries if "Mih" in e["babica"]) == GRIBLJE_MIH
        and sum(1 for e in entries if "Muc" in e["babica"]) == 6
        and all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
                for row, EMSO in EMSO_ANCHOR_ROWS.items())
    )

    # I6 — PT klasifikacija: 12 v naboru + 6 v luknji (44+46+49+52+56+60 =
    # ponovitve); 0 novih hiš; PT_GAP_KNOWN nespremenjen (ostaja samo 51);
    # kumulativ 382/85/23
    pts = pt_house_set()
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["pt"]["inNabor"] == 12
        and dokaz["stats"]["pt"]["inGap"] == 6
        and dokaz["stats"]["pt"]["inGapHouses"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == 0
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"60"' in pt_gap_set and '"52"' in pt_gap_set       # ponovitve že dokazanih
    )

    # I7 — sidra (36 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r16 = e_by_row(16)
    r31 = e_by_row(31)
    r41 = e_by_row(41)
    r55 = e_by_row(55)
    r57 = e_by_row(57)
    r66 = e_by_row(66)
    r79 = e_by_row(79)
    r84 = e_by_row(84)
    r90 = e_by_row(90)
    inv["I7_anchors"] = (
        ok7
        # r16 — h14 Brinec + botra = babica ISTA Barbara Adlešič
        and r16["child"] == "Marija" and "Janez Brinec" in r16["father"]
        and "Adlešič" in r16["botra"] and "Adlešič" in r16["babica"]
        # r31 — h91 Muc × Kure 5. VPIS + EMŠO sidro + neskladje poroke
        and r31["child"] == "Jožef" and "Janez Muc" in r31["father"]
        and "Ana Kure" in r31["mother"] and "neskladje" in " ".join(r31["notes"])
        # r41 — h85 NUJNI KRST (botra + podpis prazna) + VRZEL 20 LET
        and r41["child"] == "Jožef" and "Pezdirec" in r41["father"]
        and "NUJNI KRST" in r41["botra"] and "NUJNI KRST" in r41["priest"]
        and "20 LET" in " ".join(r41["notes"])
        and "29/5.08" in " ".join(r41["notes"])
        # r55 — h23 raztrgana celica + ISTA mati Dehlič
        and r55["child"] == "Amalija" and "RAZTRGANA" in r55["father"]
        and "Dehlič" in r55["mother"] and "MATI ISTA" in " ".join(r55["notes"])
        # r57 — h65 Milek + boter Peter Pezdirec 21 LET
        and r57["child"] == "Marija" and "Matija Milek" in r57["father"]
        and "Peter Pezdirec" in r57["botra"] and "21 LET" in " ".join(r57["notes"])
        # r66 — h30 SEGINA POVRAT + mati ISTA 1903
        and r66["child"] == "Leopold" and "Nikolaj Segina" in r66["father"]
        and "Katarina Brinec" in r66["mother"]
        and "SEGINA POVRAT" in " ".join(r66["notes"])
        and "ISTA kot 1903" in " ".join(r66["notes"])
        # r79 — h90 TRETJA učiteljska (Kalan uč.) + Jurij Pezdirec 3./3
        and r79["child"] == "Frančišek" and "Kalan" in r79["father"]
        and "učitelj" in r79["father"] and "TRETJA UČITELJSKA" in " ".join(r79["notes"])
        and "3. pojavitev" in " ".join(r79["notes"])
        # r84 — neberljiva (postrgan rob) + KURE mati
        and r84["houseNo"] == "?" and "NEBERLJIVO" in " ".join(r84["notes"])
        and "Katarina Kure" in r84["mother"]
        # r90 — h10 Brinec + ISTI boter par kot 1907 (Muc + Kure)
        and r90["child"] == "Matija" and "Janez Brinec" in r90["father"]
        and "Ana Kure" in r90["mother"] and "Janez Muc" in r90["botra"]
        and "ISTI BOTER PAR" in " ".join(r90["notes"])
    )

    # I8 — kontinuitete: vsaka hiša ima pravilen zadnji prior-leto v parish.ts
    vitals = parish_vitals_04105()
    prior = {}
    for v in vitals:
        h, y = v["houseNo"], v["year"]
        if h in CONTINUITY and y is not None and y < 1908:
            if h not in prior or y > prior[h]:
                prior[h] = y
    inv["I8_continuity"] = all(prior.get(h) == y for h, y in CONTINUITY.items())

    # I9 — vitals projekcija: 04105 blokov 348 (330 + 18); 1908 bloki == 18
    # (19 vpisov − 1 neberljiva); SKUPNI HOUSE_VITALS (vse 3 knjige) == 374
    blocks_1908 = [v for v in vitals if v["year"] == 1908]
    all_src = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"\{[^{}]*?bookSignature:\s*\"(04105|04894|04455)\"[^{}]*?\}", all_src, re.S))
    inv["I9_vitals_projection"] = (
        len(vitals) == BLOCKS_04105
        and len(blocks_1908) == EXPECTED_ENTRIES - 1
        and sorted(int(v["houseNo"]) for v in blocks_1908) == EXPECTED_VITALS_HOUSES
        and total_blocks == EXPECTED_VITALS_TOTAL
    )

    # I10 — neodvisen preracun: vsi village == Griblje; sken→stran konsistenten
    # z vnosnim scan/page; P102 kumulativ == 363/85 (veriga)
    ok10 = all(e["village"] == "Griblje" for e in entries)
    ok10 = ok10 and all(
        e["page"] == page_of_scan(e["scan"]) for e in entries)
    ok10 = ok10 and all(
        any(e["scan"] == s for s in dokaz["source"]["scans"]) for e in entries)
    cum_p102 = dokaz_p102["stats"]["cumulative"]
    ok10 = ok10 and cum_p102["entries"] == 363 and cum_p102["houses"] == 85
    inv["I10_independent_recalc"] = ok10

    return inv


def main():
    inv = verify()
    failed = [k for k, v in inv.items() if not v]
    for k, v in inv.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    if failed:
        print(f"\n{len(failed)} FAILED: {', '.join(failed)}")
        sys.exit(1)
    print("\nALL INVARIANTS PASS (I1–I10)")


if __name__ == "__main__":
    main()
