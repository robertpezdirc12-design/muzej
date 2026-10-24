#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P104 — župnija Podzemelj: krstna knjiga 04105, polno leto 1909 (issue #18).

Razširitev vzorca P79 (1886) → … → P101 (1906) → P102 (1907) → P103 (1908) na
leto 1909: glava »1909 / Januarij« INLINE na str. 180 = skeni 199/200 (dup par;
P103 ocava »sken 200 = str. 181« POPRAVLJENA — s200 = str. 180, r89 1908 pod
belim trakom berljiv SAMO na s200!) – row 81 na str. 187 (sken 211; glava
»1910« INLINE; 1910 r1 = Cerkvišče 2 Anton, 3./4. Januar — P105 lead; prva
Griblje vrstica 1910 = r3 Griblje 5 Jožefa, Matija Štrucelj × Marija Meh).
81 oštevilčenih vrstic (najkrajše leto v vzorcu; 1908 = 90). NOVELA P104 —
PET dup parov: 199/200 = str. 180 + 202/203 = str. 182 + 204/205 = str. 183
+ 207/208 = str. 185 + 209/210 = str. 186 (največ v enem letu doslej).
Stran == sken − 19 (199/200) / − 20 (201, 202) / − 21 (203–205) / − 22 (206,
207) / − 23 (208–210) / − 24 (211). VSI vpisi z Griblji: 18 vpisov / 17 hiš
(h34 ×2 = DVOJČKI Matija+Nikolaj, oba dojenčka umrla — NARE PRELOM, 1.
intra-letna ponovitev po 1908 NARE 18/18). 0 NOVIH hiš (5. leto z 0; vse 17
hiš že zasidrane; h42/h48/h54 = ponovitve v luknji 41–60). PT 14/3.
Kumulativ s P79–P103: 400 vpisov / 85 hiš / 24 let (1886–1909).
Sidra: r6 h77 3. VPIS — POŽEK POVRAT po 19 LETIH (1890 → 1902 Cindrič → 1909
ISTI Jurij Požek bajtar!); r9 h10 6. VPIS — SELITEV h30→h10 (Matija Brinec ×
Marija Grabrijan = ISTA ZVEZA kot h30 1906; trije Brincovi možje zapored
1907/08/09; EMŠO 3001909500735); r17 h42 4. VPIS — ISTA ZVEZA 1905 vrne
(Jurij Pezdirec × Katarina Jurajevič); r20+r21 h34 DVOJČKI (ISTA botra
Segina+Šuštar; r20 † 18/4.09 ISTI DAN!, r21 † 3/10.09); r28 h72 6. VPIS —
STRAUŠ POVRAČNICA po 14 LETIH (h42↔h72 ŠTRAUS↔PEZDIREC KARUSELJA; EMŠO
020609500254); r30 h33 3. VPIS — »Vpis prenesen v mrliški register« + EMŠO
0306095050335 (MENJAVA #3 Papič?; VRZEL 11 LET); r32 h63 9. VPIS — mati
»Katarina Križan, samka ½ zemljaka« (MOŽEN NEZAKONSKI); r35 h54 6. VPIS —
Šimec × Kure? nova družina (boter Ivan Požek!); r37 h1 7. VPIS ISTA ZVEZA
(Jurij Željko × Barbara Kure = 1900+1905; † 5.5.1925); r40 h6 4. VPIS —
HIŠNA CELICA POKRITA, hiša GENETSKO (ISTA ZVEZA 1904/05 + botrinja Marija
Klepec; EMŠO 120809505944 [~]); r44 h24 14. VPIS ZAPORED (najbolj
vpisovana; PONESREČI UMRLA 1965 pri božjani s šolskim kolektivom!; EMŠO
26079095?5231 [~]); r57 h30 12. VPIS — 7. DRUŽINA (Martinovič? kovač ×
Šimec); r58 h12 12. VPIS — Drgoš × Cvitkovič nova zveza (VÖTTER DVOJNO);
r60 h35 6. VPIS — MATI BREZ PRIIMKA (samo »Ana«!); r61 h32 10. VPIS — ISTA
ZVEZA Meh × Pezdirec (podpis-kolono prevzame maticarka Paulin Bitenc!); r64
h48 4. VPIS — EMŠO 1910909505186 = KRSTNI datum (rojstvo 18.10 — ANOMALIJA);
r72 h66 4. VPIS (Bohte × Križan; forenzika 66 ne 22/72; EMŠO 051090505628 [~]).
DUHOVNIKI: Gregor Cerar 10 (vključno r30 »coop.«) + Jos. Rauq 6 (r40–r64) +
2 podpisa maticarke Paulin Bitenc v koloni Podpis (r61/r72 — NOVELA: od r61
dalje maticarka podpisuje ob smrtnih pripisih 1950s–60s). BABICA NOVELA:
18/18 imenovanih — MEH 12/18 DOMINANTA + Adlešič 1 + Štraus 1 + Mavrenič 1 +
Uri? 1 + Novak 1 + Vötter 1. EMŠO kampanja: 6+1 sidr (r64 datum=krsta!).
Anomalije: r5 »Decembar 16./16.« POD glavo 1909 (kronološka kršitev); r91 =
aprilski vpis 1908 nad glavo; h42↔h72 karusela; POŽEK 19 let; selitev
h30→h10; dvojčki z obema smrtma; mati samka (r32); mati brez priimka (r60);
EMŠO=krsta (r64); maticarka v podpis-koloni; ponesreči umrla (r44); 2
razveljavitvi zakona (r73 Krško + r76); TRGOGRAD pripis (r19); »Vpis
prenesen v mrliški register« (r30) + »vzet v matični register 2000s« (r65
Vranovče); Podzemelj vpis (r63); mejni vpis r81 (31.12.1909/1.1.1910);
kraj »Gornej?« ×4. Excluded: 22.

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
DOKAZ = "research/issue17/parish-baptism-1909.json"
DOKAZ_P103 = "research/issue17/parish-baptism-1908.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (199, 211)        # skeni 199/200 (str. 180: glava 1909 + rows 1–5) – 211 (str. 187: rows 78–81 + glava 1910)
FRAME_PAGES = (180, 187)
DATA_SCANS = [199, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211]
EXPECTED_CITED = [199, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211]
EXPECTED_PAGES = [180, 181, 182, 182, 183, 183, 184, 185, 185, 186, 186, 187]
EXPECTED_ENTRIES = 18
EXPECTED_DISTINCT = 17          # 17 hiš (h34 ×2 dvojčka)
EXPECTED_EXCLUDED = 22
EXPECTED_HOUSES = sorted([1, 6, 10, 12, 24, 30, 32, 33, 34, 35, 42, 48, 54, 63, 66, 72, 77])
EXPECTED_VITALS_HOUSES = sorted([1, 6, 10, 12, 24, 30, 32, 33, 34, 34, 35, 42, 48, 54, 63, 66, 72, 77])
EXPECTED_PT_IN_SET = ["1", "6", "10", "12", "24", "30", "32", "33", "34", "35", "63", "66", "72", "77"]
EXPECTED_PT_GAP = ["42", "48", "54"]  # ponovitve v luknji 41–60 (h42/h48/h54 že dokazane)
EXPECTED_REPEATS = 1            # NARE PRELOM — h34 ×2 (dvojčka)
EXPECTED_NEW_HOUSES = 0         # 5. leto z 0 novih
EXPECTED_VITALS_TOTAL = 659     # 412 + 17 (P106)  # POSODABLJENO P138: 490 (era P106) → 651 (P137) → 659 (P138: + 8 poročnih blokov 1909!)
BLOCKS_04105 = 502              # 386 + 17 (P106)  # POSODABLJENO P138: 441 (era P106) → 502 (krstna knjiga zrasla P107–P114!)
KUMULATIV_ENTRIES = 400         # 382 + 18
KUMULATIV_HOUSES = 85
KUMULATIV_YEARS = 24            # 1886–1909
# kontinuitete (hiša → zadnje krstno leto pred 1909 v 04105, iz parish.ts)
CONTINUITY = {
    "1": 1905, "6": 1907, "10": 1908, "12": 1907, "24": 1908, "30": 1908,
    "32": 1903, "33": 1898, "34": 1906, "35": 1906, "42": 1906, "48": 1907,
    "54": 1904, "63": 1903, "66": 1905, "72": 1895, "77": 1902,
}
# sidra/pini P104 (row, scan, hiša, pin):
ANCHORS = [
    (6, 201, "77", "Požek"),
    (6, 201, "77", "POVRAT po 19 LETIH"),
    (9, 201, "10", "Brinec"),
    (9, 201, "10", "6. VPIS"),
    (17, 201, "42", "Pezdirec"),
    (17, 201, "42", "4. VPIS"),
    (20, 202, "34", "DVOJČEK 1/2"),
    (20, 202, "34", "Segina"),
    (21, 202, "34", "DVOJČEK 2/2"),
    (21, 202, "34", "Šuštar"),
    (28, 203, "72", "Straus"),
    (28, 203, "72", "POVRAČNICA"),
    (30, 204, "33", "PRENESEN"),
    (30, 204, "33", "3. VPIS"),
    (32, 205, "63", "samka"),
    (32, 205, "63", "9. VPIS"),
    (35, 205, "54", "Šimec"),
    (35, 205, "54", "6. VPIS"),
    (37, 205, "1", "Željko"),
    (37, 205, "1", "7. VPIS"),
    (40, 205, "6", "GENETSKO"),
    (40, 205, "6", "4. VPIS"),
    (44, 206, "24", "14. VPIS"),
    (44, 206, "24", "PONESREČI"),
    (57, 207, "30", "Martinovič"),
    (57, 207, "30", "12. VPIS"),
    (58, 207, "12", "Drgoš"),
    (58, 207, "12", "VÖTTER DVOJNO"),
    (60, 208, "35", "Pezdirec"),
    (60, 208, "35", "PRIIMKA"),
    (61, 208, "32", "Meh"),
    (61, 208, "32", "Bitenc"),
    (64, 208, "48", "KRSTNI datum"),
    (64, 208, "48", "Brodarič"),
    (72, 210, "66", "Bohte"),
    (72, 210, "66", "Križan"),
]
EMSO_ANCHOR_ROWS = {
    9: "3001909500735",
    28: "020609500254",
    30: "0306095050335",
    40: "120809505944",
    44: "26079095?5231",
    64: "1910909505186",
    72: "051090505628",
}
GRIBLJE_MEH = 12                # NOVELA: MEH 12/18 DOMINANTA
GRIBLJE_VOTTER = 1              # r58 Marjeta Vötter (+ botrinja Katarina Vötter = DVOJNO)
GRIBLJE_CERAR = 10              # vključno r30 coop.
GRIBLJE_RAVQ = 6                # r40/r44/r57/r58/r60/r64
GRIBLJE_BITENC = 2              # r61/r72 — maticarka v podpis-koloni (NOVELA)
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
    """NOVELA P104: PET dup parov. 199/200 = str. 180 (dup; s200 = str. 180,
    P103 ocava popravljena); 201 = 181; 202/203 = 182; 204/205 = 183;
    206 = 184; 207/208 = 185; 209/210 = 186; 211 = 187. Glava 1910 = INLINE
    str. 187 (sken 211)."""
    if scan in (199, 200):
        return 180
    if scan == 201:
        return 181
    if scan in (202, 203):
        return 182
    if scan in (204, 205):
        return 183
    if scan == 206:
        return 184
    if scan in (207, 208):
        return 185
    if scan in (209, 210):
        return 186
    if scan == 211:
        return 187
    return scan - 24


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p103 = json.load(open(DOKAZ_P103, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h.isdigit()]

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

    # I4 — okvir leta: glava 1909 INLINE na str. 180 = skeni 199/200 (dup par;
    # P103 ocava s200 popravljena) … row 81 (sken 211, str. 187); glava 1910
    # INLINE; 81 vrstic; PET dup parov; page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 199 and fr["yearStart"]["page"] == 180
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 211 and fr["yearEnd"]["page"] == 187
        and fr["yearEnd"]["row"] == 81
        and fr["rowsTotal"] == 81
        and fr["duplicateScans"]["count"] == 5
        and {(p["scans"][0], p["scans"][1], p["page"]) for p in fr["duplicateScans"]["pairs"]}
        == {(199, 200, 180), (202, 203, 182), (204, 205, 183), (207, 208, 185), (209, 210, 186)}
    ) and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
    inv["I4_glava_notes"] = (
        "POTRJEN" in fr["yearStart"]["note"]
        and "1909" in fr["yearStart"]["note"]
        and "popravljen" in fr["yearStart"]["note"].lower()
        and "P105 lead" in fr["glava1910"]["note"]
        and "Štrucelj" in fr["glava1910"]["note"]
    )

    # I5 — štetja: 18 vpisov / 17 hiš (h34 ×2); 22 excluded; NARE PRELOM
    # (1 ponovitev — dvojčka); 0 novih hiš; babica 18/18 + Meh 12 + Vötter 1;
    # EMŠO sidra r9/r28/r30/r40/r44/r64/r72
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses_numeric)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and houses_written == EXPECTED_HOUSES
        and dokaz["stats"]["intraYearRepeats"] == EXPECTED_REPEATS
        and "NARE PRELOM" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["babica"]["griblje"].startswith("18/18")
        and sum(1 for e in entries if "Vötter" in e["babica"]) == GRIBLJE_VOTTER
        and sum(1 for e in entries if "Meh" in e["babica"]) == GRIBLJE_MEH
        and sum(1 for e in entries if "Meh" in e["babica"]) == 12
        and all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
                for row, EMSO in EMSO_ANCHOR_ROWS.items())
    )

    # I6 — PT klasifikacija: 14 v naboru + 3 v luknji (42+48+54 = ponovitve
    # že dokazanih); 0 novih hiš; PT_GAP_KNOWN nespremenjen (ostaja samo 51
    # nedokazana v 41–60); kumulativ 400/85/24
    pts = pt_house_set()
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["pt"]["inNabor"] == 14
        and dokaz["stats"]["pt"]["inGap"] == 3
        and dokaz["stats"]["pt"]["inGapHouses"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == 0
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"42"' in pt_gap_set and '"48"' in pt_gap_set and '"54"' in pt_gap_set
    )

    # I7 — sidra (36 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r6 = e_by_row(6)
    r9 = e_by_row(9)
    r20 = e_by_row(20)
    r21 = e_by_row(21)
    r28 = e_by_row(28)
    r30 = e_by_row(30)
    r32 = e_by_row(32)
    r40 = e_by_row(40)
    r44 = e_by_row(44)
    r60 = e_by_row(60)
    r61 = e_by_row(61)
    r64 = e_by_row(64)
    r72 = e_by_row(72)
    inv["I7_anchors"] = (
        ok7
        # r6 — h77 POŽEK POVRAT po 19 letih
        and r6["child"] == "Alojzij" and "Jurij Požek" in r6["father"]
        and "bajtar" in r6["father"] and "19 LETIH" in " ".join(r6["notes"])
        # r9 — h10 selitev h30→h10 + EMŠO sidro
        and r9["child"] == "Anton" and "Matija Brinec" in r9["father"]
        and "Marija Grabrijan" in r9["mother"] and "h30→h10" in " ".join(r9["notes"])
        # r20+r21 — h34 dvojčka, ISTA botra, obe smrti
        and r20["child"] == "Matija" and r21["child"] == "Nikolaj"
        and "DVOJČEK 1/2" in " ".join(r20["notes"]) and "DVOJČEK 2/2" in " ".join(r21["notes"])
        and "Segina" in r20["botra"] and "Šuštar" in r20["botra"]
        and "18/4. 09" in " ".join(r20["notes"]) and "3/4. 10" in " ".join(r21["notes"])
        # r28 — h72 Strauš POVRAČNICA + KARUSELJA
        and r28["child"] == "Danijel" and "Straus" in r28["father"]
        and "KARUSELJA" in " ".join(r28["notes"]) and "14 LETIH" in " ".join(r28["notes"])
        # r30 — h33 vpis prenesen + MENJAVA #3
        and r30["child"] == "Katarina" and "Papič" in r30["father"]
        and "PRENESEN" in " ".join(r30["notes"])
        and "MENJAVA DRUŽINE #3" in " ".join(r30["notes"])
        # r32 — h63 mati samka (možen nezakonski)
        and r32["child"] == "Jožefa" and "samka" in r32["mother"]
        and "nezakonski" in " ".join(r32["notes"])
        # r40 — h6 genetsko (celica pokrita)
        and r40["child"] == "Ana" and "GENETSKO" in r40["houseNo"] + " ".join(r40["notes"])
        and "Jakobič" in r40["father"] and "Marija Klepec" in r40["botra"]
        # r44 — h24 14. VPIS + ponesreči umrla
        and r44["child"] == "Ana" and "14. VPIS" in " ".join(r44["notes"])
        and "PONESREČI" in " ".join(r44["notes"]) and "šolskim kolektivom" in " ".join(r44["notes"])
        # r60 — h35 mati brez priimka
        and r60["child"] == "Jožef" and "PRIIMEK NEZAPISAN" in r60["mother"]
        and "Pezdirec" in r60["father"]
        # r61 — h32 ISTA ZVEZA + maticarka Bitenc
        and r61["child"] == "Jožefa" and "Matija Meh" in r61["father"]
        and "Marjeta Pezdirec" in r61["mother"] and "Bitenc" in r61["priest"]
        # r64 — h48 EMŠO = krstni datum anomalija
        and r64["child"] == "Jožefa" and "Jurij Pezdirec" in r64["father"]
        and "KRSTNI datum" in " ".join(r64["notes"])
        # r72 — h66 forenzika 66 + Bohte × Križan
        and r72["child"] == "Marija" and "Jakob Bohte" in r72["father"]
        and "Katarina Križan" in r72["mother"] and "DVE ŠESTERKI" in " ".join(r72["notes"])
    )

    # I8 — kontinuitete: vsaka hiša ima pravilen zadnji prior-leto v parish.ts
    vitals = parish_vitals_04105()
    prior = {}
    for v in vitals:
        h, y = v["houseNo"], v["year"]
        if h in CONTINUITY and y is not None and y < 1909:
            if h not in prior or y > prior[h]:
                prior[h] = y
    inv["I8_continuity"] = all(prior.get(h) == y for h, y in CONTINUITY.items())

    # I9 — vitals projekcija: 04105 blokov 366 (348 + 18); 1909 bloki == 18;
    # SKUPNI HOUSE_VITALS (vse 3 knjige) == 429
    blocks_1909 = [v for v in vitals if v["year"] == 1909]
    all_src = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"bookSignature:\s*\"(04105|04894|04455)\"", all_src))  # P138: metoda bookSignature-štetja (stara {}-regex preskakovala bloke z zavitimi oklepaji!)
    inv["I9_vitals_projection"] = (
        len(vitals) == BLOCKS_04105
        and len(blocks_1909) == EXPECTED_ENTRIES
        and sorted(int(v["houseNo"]) for v in blocks_1909) == EXPECTED_VITALS_HOUSES
        and total_blocks == EXPECTED_VITALS_TOTAL
    )

    # I10 — neodvisen preracun: vsi village == Griblje; sken→stran konsistenten
    # z vnosnim scan/page; P103 kumulativ == 382/85 (veriga)
    ok10 = all(e["village"] == "Griblje" for e in entries)
    ok10 = ok10 and all(
        e["page"] == page_of_scan(e["scan"]) for e in entries)
    ok10 = ok10 and all(
        any(e["scan"] == s for s in dokaz["source"]["scans"]) for e in entries)
    cum_p103 = dokaz_p103["stats"]["cumulative"]
    ok10 = ok10 and cum_p103["entries"] == 382 and cum_p103["houses"] == 85
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
