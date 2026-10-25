#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P105 — župnija Podzemelj: krstna knjiga 04105, polno leto 1910 (issue #18).

Razširitev vzorca P79 (1886) → … → P102 (1907) → P103 (1908) → P104 (1909) na
leto 1910: glava »1910 / Januar« INLINE na str. 187 = sken 211 (pod vsoto
1909; s211/s212 SOSEDNJA — ni dup par); 1910 r1 = Cerkvišče 2 Anton, 3./4.
Januar (EMŠO 0301910500241) — P104 lead POTRJEN. Row 84 = str. 194 (sken 219;
glava »~1911~« INLINE; 1911 r1 = Begunja vas 14 Anton, 8./9. Januar — P106
lead; prva Griblje vrstica 1911 = r3 Griblje 34 Antonia, Janez Brinec × Ana
Milek — h34 TRETJE leto!). 84 oštevilčenih vrstic (1908 = 90, 1909 = 81).
NOVELA P105 — EN dup par: 216/217 = str. 192 (najmanj od P102; s217 za复核
r64–r67). Stran == sken − 24 (211–216) / DUP 217 == str. 192 / − 25 (218,
219). VSI vpisi z Griblji: 20 vpisov / 20 hiš — NARE 20/20 (po P104 prelomu
h34×2 spet brez intra-letnih ponovitev). 0 NOVIH hiš (6. leto z 0). PT 20/5
(42+44+46+49+60 v luknji 41–60). Kumulativ s P79–P104: 420 vpisov / 85 hiš /
25 let (1886–1910).

SIDRA: r3 h5 5. VPIS (Štrucelj × Meh 5. skupaj; EMŠO 0801910505931; ime
»?exa« neberljivo — P104 lead »Jožefa« NAPAČEN); r7 h88 2. VPIS (natrgan rob);
r10 h29 4. VPIS — VRZEL 15 LET + NEZAKONSKI (mati Barbara Milek sama = h29
familija); r18 h18 4. VPIS — POVRAT Šimec × Kambič + VPIS PRENEŠEN 23.06.2003
(EMŠO 0703910505638); r22 h44 5. VPIS (Štrucelj 3.× zapored; EMŠO
0403910500260 — datumski popravek rojstev 4.); r26 h34 8. VPIS — TRETJE leto
(Nikolaj Šulak? pod trakom; ISTI boter Segina 3.); r32 h60 9. VPIS (Nikolaj
Željko — branje »Kolehko«); r33 h90 6. VPIS — 2. Kalanov (učitelj; † 19.10);
r39 h21 7. VPIS (oče »…mir« = morda Kazimir — 1888 nezakonski POVRET?; mati
menjava Ana Šimec → Katarina Kure); r42 h35 7. VPIS (babica PRAZNA; † 26/6);
r47 h22 5. VPIS (Milek; EMŠO 2506910505074; boter Ivan Požek); r48 h91 6.
VPIS — OČE MENJAVA Janez→Matija Muc (mati Ana Kure ISTA 6×; † 18/9); r54 h46
7. VPIS (Brodarič genetsko; forenzika 46); r66 h65 10. VPIS (Matija Milek
10.×; popravek »št. 45« NAPAČEN; EMŠO 2809910500547 — datumski popravek 28.);
r67 h49 5. VPIS (Nikolaj Brodarič; VPIS PRENEŠEN 5.5.1957); r72 h28 2. VPIS —
VRZEL 19 LET (izenačen rekord z h77 1909!) + NEZAKONSKA (mati Marjeta Sodek?
samota; botrinja Marija Kalan učiteljeva žena = CROSS-ROW h90 r33!); r78 h6
5. VPIS (Jakobič 4.×; botrinja Marija Klepec 3.×; † 19/11 ISTI DAN); r79 h42
5. VPIS — GENETSKA REŠITEV (forenzika »16« NAPAČNA — h16 = Novak r84 kolizija;
Pezdirec × Jurajevič 2. leto); r83 h1 8. VPIS — OČE MENJAVA Željko→Trome
(podpis jasen P: »Paulin Bitnar«; poroka 17.2.1936 → † 14.3.1936!); r84 h16
9. VPIS (Alojzij Novak × Marija Frlah? = h60 1904 par; botra PRAZNA; † 11/12
ISTI DAN — zadnja vrstica!).

DUHOVNIKI/PODPISI: »Laulin/Paulin Bitnar« 13 (ISTA ROKA kot P104 maticarka
»Paulin Bitenc« — NOVELA dilema kaplan/maticarka; r83 jasni P = ista oseba
piše P/L) + »Jos. Rauq« 7 (nadaljevanje 1909). BABICA: 19/20 imenovanih —
MEH 15/20 DOMINANTA (r83 mati+babica MEH ×2!) + Ana Mavrenič 1 + Barbara
Adlešič 1 + Marjeta Toter 1 + 1 prazna (r42). EMŠO kampanja: 5 sidr VSI
SKLADNI (2× datumski popravki iz EMŠO). Anomalije: 2 nezakonska (r10, r72);
2 prazni botri (r42 babica, r84 botra); 5 dojenčkov † (2× ISTI DAN); OČE
MENJAVA h1 + h91; MATI MENJAVA h21 + h35; genetski popravki h42/h65/h34/h60;
VPIS PRENEŠEN ×3; napačen popravek matičarja (r66). Excluded: 61.

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
DOKAZ = "research/issue17/parish-baptism-1910.json"
DOKAZ_P104 = "research/issue17/parish-baptism-1909.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (211, 219)        # sken 211 (str. 187: glava 1910 + rows 1–7) – 219 (str. 194: rows 80–84 + glava 1911)
FRAME_PAGES = (187, 194)
DATA_SCANS = [211, 212, 213, 214, 215, 216, 217, 218, 219]
EXPECTED_CITED = [211, 212, 213, 214, 215, 216, 217, 218, 219]
EXPECTED_PAGES = [187, 188, 189, 190, 191, 192, 192, 193, 194]
EXPECTED_ENTRIES = 20
EXPECTED_DISTINCT = 20          # NARE 20/20
EXPECTED_EXCLUDED = 61
EXPECTED_HOUSES = sorted([1, 5, 6, 16, 18, 21, 22, 28, 29, 34, 35, 42, 44, 46, 49, 60, 65, 88, 90, 91])
EXPECTED_VITALS_HOUSES = sorted([1, 5, 6, 16, 18, 21, 22, 28, 29, 34, 35, 42, 44, 46, 49, 60, 65, 88, 90, 91])
EXPECTED_PT_IN_SET = ["1", "5", "6", "16", "18", "21", "22", "28", "29", "34", "35", "65", "88", "90", "91"]
EXPECTED_PT_GAP = ["42", "44", "46", "49", "60"]  # ponovitve v luknji 41–60
EXPECTED_REPEATS = 0            # NARE 20/20
EXPECTED_NEW_HOUSES = 0         # 6. leto z 0 novih
EXPECTED_VITALS_TOTAL = 670  # POSODABLJENO P138: 490 (era) → 659 (P138!)
BLOCKS_04105 = 502              # POSODABLJENO P139: 464 (era) → 502 (živi korpus!)
KUMULATIV_ENTRIES = 420         # 400 + 20
KUMULATIV_HOUSES = 85
KUMULATIV_YEARS = 25            # 1886–1910
# kontinuitete (hiša → zadnje krstno leto pred 1910 v 04105, iz parish.ts)
CONTINUITY = {
    "1": 1909, "5": 1907, "6": 1909, "16": 1908, "18": 1907, "21": 1906,
    "22": 1905, "28": 1891, "29": 1895, "34": 1909, "35": 1909, "42": 1909,
    "44": 1908, "46": 1908, "49": 1908, "60": 1908, "65": 1908, "88": 1904,
    "90": 1908, "91": 1908,
}
# sidra/pini P105 (row, scan, hiša, pin):
ANCHORS = [
    (3, 211, "5", "5. VPIS"),
    (3, 211, "5", "Štrucelj"),
    (10, 212, "29", "NEZAKONSKI"),
    (10, 212, "29", "4. VPIS"),
    (18, 212, "18", "PRENEŠEN"),
    (18, 212, "18", "Kambič"),
    (22, 213, "44", "5. VPIS"),
    (22, 213, "44", "Štrucelj"),
    (26, 213, "34", "Segina"),
    (26, 213, "34", "Šulak"),
    (32, 214, "60", "Željko"),
    (32, 214, "60", "9. VPIS"),
    (33, 214, "90", "Kalan"),
    (33, 214, "90", "učitelj"),
    (39, 214, "21", "Požek"),
    (39, 214, "21", "7. VPIS"),
    (42, 214, "35", "7. VPIS"),
    (42, 214, "35", "PRAZNO"),
    (47, 215, "22", "Milek"),
    (47, 215, "22", "5. VPIS"),
    (48, 215, "91", "Muc"),
    (48, 215, "91", "6. VPIS"),
    (54, 215, "46", "Brodarič"),
    (66, 216, "65", "Milek"),
    (66, 216, "65", "10. VPIS"),
    (67, 216, "49", "Brodarič"),
    (67, 216, "49", "5. VPIS"),
    (72, 218, "28", "NEZAKONSKA"),
    (72, 218, "28", "Kalan"),
    (78, 218, "6", "Jakobič"),
    (78, 218, "6", "5. VPIS"),
    (79, 218, "42", "GENETSKA REŠITEV"),
    (79, 218, "42", "Pezdirec"),
    (83, 219, "1", "Trome"),
    (83, 219, "1", "8. VPIS"),
    (84, 219, "16", "Novak"),
    (84, 219, "16", "PRAZNO"),
]
EMSO_ANCHOR_ROWS = {
    3: "0801910505931",
    18: "0703910505638",
    22: "0403910500260",
    47: "2506910505074",
    66: "2809910500547",
}
GRIBLJE_MEH = 16                # 15 × Marija Meh + 1 × Ana Meh (r83 mati+babica MEH ×2!)
GRIBLJE_KLEPEC_BOTRINA = 3      # r32 + r78 + r83 Marija Klepec
GRIBLJE_BITNAR = 13             # Laulin/Paulin Bitnar (NOVELA — ISTA roka kot P104 maticarka)
GRIBLJE_RAUQ = 7                # Jos. Rauq (nadaljevanje 1909)
GRIBLJE_NEZAKONSKI = 2          # r10 + r72
GRIBLJE_BOTRA_PRAZNA = 2        # r42 babica + r84 botra
GRIBLJE_DOJENCKI_UMRLI = 5      # r33/r42/r48/r78/r84
MIDWIFE_NAMED = 19              # na Gribljih 19/20 (r42 prazna)


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
    """P105: EN dup par. 211 = 187; 212 = 188; 213 = 189; 214 = 190;
    215 = 191; 216/217 = 192 (dup); 218 = 193; 219 = 194. Glava 1911 =
    INLINE str. 194 (sken 219)."""
    if scan == 211:
        return 187
    if scan == 212:
        return 188
    if scan == 213:
        return 189
    if scan == 214:
        return 190
    if scan == 215:
        return 191
    if scan in (216, 217):
        return 192
    if scan == 218:
        return 193
    if scan == 219:
        return 194
    return scan - 25


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p104 = json.load(open(DOKAZ_P104, encoding="utf-8"))
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

    # I4 — okvir leta: glava 1910 INLINE na str. 187 = sken 211 … row 84
    # (sken 219, str. 194); glava 1911 INLINE; 84 vrstic; EN dup par
    # (216/217 = str. 192); page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 211 and fr["yearStart"]["page"] == 187
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 219 and fr["yearEnd"]["page"] == 194
        and fr["yearEnd"]["row"] == 84
        and fr["rowsTotal"] == 84
        and fr["duplicateScans"]["count"] == 1
        and {(p["scans"][0], p["scans"][1], p["page"]) for p in fr["duplicateScans"]["pairs"]}
        == {(216, 217, 192)}
    ) and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
    inv["I4_glava_notes"] = (
        "POTRJEN" in fr["yearStart"]["note"]
        and "1910" in fr["yearStart"]["note"]
        and "P106 lead" in fr["glava1911"]["note"]
        and "Brinec" in fr["glava1911"]["note"]
    )

    # I5 — štetja: 20 vpisov / 20 hiš (NARE 20/20); 61 excluded; 0 novih
    # hiš; babica 19/20 + Meh 16 substring + Klepec botrinja 3; EMŠO sidra
    # r3/r18/r22/r47/r66; nezakonski 2; botra prazna 2; dojenčki † 5
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
        and "NARE 20/20" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["babica"]["griblje"].startswith("19/20")
        and sum(1 for e in entries if "Meh" in e["babica"]) == GRIBLJE_MEH
        and sum(1 for e in entries if "Klepec" in e["botra"]) == GRIBLJE_KLEPEC_BOTRINA
        and sum(1 for e in entries if "PRAZNO" in e["father"]) == 2
        and sum(1 for e in entries if "PRAZNO" in e["botra"]) == 1
        and sum(1 for e in entries if "PRAZNO" in e["babica"]) == 1
        and sum(1 for e in entries if "Bitnar" in e["priest"]) == GRIBLJE_BITNAR
        and sum(1 for e in entries if "Rauq" in e["priest"]) == GRIBLJE_RAUQ
        and sum(1 for e in entries if "DOJENČEK" in json.dumps(e, ensure_ascii=False)
                or "dojenček" in json.dumps(e, ensure_ascii=False)) >= 2
        and all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
                for row, EMSO in EMSO_ANCHOR_ROWS.items())
    )

    # I6 — PT klasifikacija: 15 v naboru + 5 v luknji (42+44+46+49+60);
    # 0 novih hiš; PT_GAP_KNOWN nespremenjen (ostaja samo 51 nedokazana v
    # 41–60); kumulativ 420/85/25
    pts = pt_house_set()
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["pt"]["inNabor"] == 15
        and dokaz["stats"]["pt"]["inGap"] == 5
        and dokaz["stats"]["pt"]["inGapHouses"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == 0
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"42"' in pt_gap_set and '"44"' in pt_gap_set and '"46"' in pt_gap_set
        and '"49"' in pt_gap_set and '"60"' in pt_gap_set
    )

    # I7 — sidra (37 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r3 = e_by_row(3)
    r10 = e_by_row(10)
    r18 = e_by_row(18)
    r26 = e_by_row(26)
    r32 = e_by_row(32)
    r39 = e_by_row(39)
    r48 = e_by_row(48)
    r66 = e_by_row(66)
    r72 = e_by_row(72)
    r79 = e_by_row(79)
    r83 = e_by_row(83)
    r84 = e_by_row(84)
    inv["I7_anchors"] = (
        ok7
        # r3 — h5 5. VPIS, ime neberljivo, P104 lead napačen
        and "neberljivo" in r3["child"] and "Jožefa" in json.dumps(r3, ensure_ascii=False)
        and "NAPAČNA ugiba" in json.dumps(r3, ensure_ascii=False)
        and "Matija Štrucelj" in r3["father"] and "Marija Meh" in r3["mother"]
        # r10 — h29 NEZAKONSKI + vrzel 15 let + Milek genetika
        and r10["father"].startswith("[PRAZNO") and "sama" in r10["mother"]
        and "15 LET" in " ".join(r10["notes"]) and "Milekova familija" in " ".join(r10["notes"])
        # r18 — h18 POVRAT + VPIS PRENEŠEN
        and r18["child"] == "Neža" and "POVRAT" in " ".join(r18["notes"])
        and "23.06.2003" in " ".join(r18["notes"])
        and "Matija Šimec" in r18["father"] and "Marija Kambič" in r18["mother"]
        # r26 — h34 TRETJE leto + Segina 3. + genetika Šulak
        and r26["child"] == "Jožef" and "Šulak" in r26["father"]
        and "TRETJE leto" in " ".join(r26["notes"])
        and "Nikolaj Segina" in r26["botra"] and "3. skupaj" in " ".join(r26["notes"])
        # r32 — h60 genetika Željko (»Kolehko«)
        and "Željko" in r32["father"] and "Kolehko" in r32["father"]
        and "Brodarič" in r32["mother"] and "9. VPIS" in " ".join(r32["notes"])
        # r39 — h21 Požek + oče »…mir« (Kazimir hipoteza)
        and "Požek" in r39["father"] and "Kazimir" in r39["father"]
        and "Katarina Kure" in r39["mother"] and "MATI MENJANA" in r39["mother"]
        # r48 — h91 OČE MENJAVA Janez→Matija Muc
        and "Matija Muc" in r48["father"] and "OČE MENJAVA" in r48["father"]
        and "Ana Kure" in r48["mother"] and "ISTA 6×" in " ".join(r48["notes"])
        # r66 — h65 10. VPIS + popravek 45 napačen
        and "Matija Milek" in r66["father"] and "10. VPIS" in " ".join(r66["notes"])
        and "NAPAČEN" in " ".join(r66["notes"]) and "št. 45" in " ".join(r66["notes"])
        # r72 — h28 NEZAKONSKA + vrzel 19 let + Kalan CROSS-ROW
        and r72["father"].startswith("[PRAZNO") and "samota" in r72["mother"]
        and "19 LET" in " ".join(r72["notes"])
        and "Kalan" in r72["botra"] and "CROSS-ROW" in r72["botra"] + " ".join(r72["notes"])
        # r79 — h42 GENETSKO (forenzika 16 napačna)
        and r79["houseNo"] == "42" and "GENETSKA REŠITEV" in r79["houseNo"] + " ".join(r79["notes"])
        and "Jurij Pezdirec" in r79["father"] and "Katarina Jurajevič" in r79["mother"]
        # r83 — h1 OČE MENJAVA + Paulin Bitnar (jasni P)
        and "Trome" in r83["father"] and "OČE MENJAVA" in r83["father"]
        and "Paulin Bitnar" in r83["priest"]
        and "Ana Meh" in r83["babica"] and "MEH ×2" in r83["babica"]
        # r84 — h16 botra PRAZNA + ISTI DAN + Novak genetika
        and r84["child"] == "Ana" and "PRAZNO" in r84["botra"]
        and "ISTI DAN" in " ".join(r84["notes"]) and "Frlah" in r84["mother"]
        and "h60 1904" in " ".join(r84["notes"])
    )

    # I8 — kontinuitete: vsaka hiša ima pravilen zadnji prior-leto v parish.ts
    vitals = parish_vitals_04105()
    prior = {}
    for v in vitals:
        h, y = v["houseNo"], v["year"]
        if h in CONTINUITY and y is not None and y < 1910:
            if h not in prior or y > prior[h]:
                prior[h] = y
    inv["I8_continuity"] = all(prior.get(h) == y for h, y in CONTINUITY.items())

    # I9 — vitals projekcija: 04105 blokov 386 (366 + 20); 1910 bloki == 20;
    # SKUPNI HOUSE_VITALS (vse 3 knjige) == 429
    blocks_1910 = [v for v in vitals if v["year"] == 1910]
    all_src = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"bookSignature:\s*\"(04105|04894|04455)\"", all_src))  # P138: bookSignature-štetje
    inv["I9_vitals_projection"] = (
        len(vitals) == BLOCKS_04105
        and len(blocks_1910) == EXPECTED_ENTRIES
        and sorted(int(v["houseNo"]) for v in blocks_1910) == EXPECTED_VITALS_HOUSES
        and total_blocks == EXPECTED_VITALS_TOTAL
    )

    # I10 — neodvisen preracun: vsi village == Griblje; sken→stran
    # konsistenten z vnosnim scan/page; P104 kumulativ == 400/85 (veriga)
    ok10 = all(e["village"] == "Griblje" for e in entries)
    ok10 = ok10 and all(
        e["page"] == page_of_scan(e["scan"]) for e in entries)
    ok10 = ok10 and all(
        any(e["scan"] == s for s in dokaz["source"]["scans"]) for e in entries)
    cum_p104 = dokaz_p104["stats"]["cumulative"]
    ok10 = ok10 and cum_p104["entries"] == 400 and cum_p104["houses"] == 85
    inv["I10_independent_recalc"] = ok10

    return inv


def main():
    inv = verify()
    fails = [k for k, v in inv.items() if not v]
    for k in sorted(inv):
        print(f"{k}: {'PASS' if inv[k] else 'FAIL'}")
    if fails:
        print(f"\nP105 --check: {len(inv) - len(fails)}/{len(inv)} PASS, {len(fails)} FAIL")
        sys.exit(1)
    print(f"\nP105 --check: {len(inv)}/{len(inv)} PASS")


if __name__ == "__main__":
    main()
