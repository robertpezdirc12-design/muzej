#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P101 — župnija Podzemelj: krstna knjiga 04105, polno leto 1906 (issue #18).

Razširitev vzorca P79 (1886) → … → P98 (1903) → P99 (1904) → P100 (1905) na
leto 1906: okvir glava »1906« na str. 158 = sken 170/171 (dup par, P100
dokazano; 1906 r1 = »Gorn?« 34 Jožef, 1./1. Januar — P100 lead POTRJEN) –
row 87 na str. 165 (skeni 178/179; glava »1907« POD r87; 1907 r1 = Dobravice
27 Ivanka, podpis Anton Dostál — P102 lead). 87 oštevilčenih vrstic. NOVELA
P101 — EN podvojen par skenov v okviru leta: 178/179 = str. 165 (rows 85–87).
Stran == sken − 13 (172–178) / − 14 (180+); dup par 170/171 = str. 158.
Format = spread (levo data, desno Roditelja/Botra/Babica; kot 1905).
VSI vpisi z Griblji: 18 vpisov / 18 hiš — NARE ponovno (vsaka hiša 1×; po
1905 prelomu h12 ×2 spet brez intra-letne ponovitve). 1 NOVA HIŠA: h4 (85.
vitals; po dveh letih 1904+1905 brez novih; h4 JE v PT naboru). PT 14/4
(42+44+49+60 v luknji 41–60 — vsi ponovitve že dokazanih; ostaja samo h51).
Kumulativ s P79–P100: 347 vpisov / 85 hiš / ENAINDVajset let (1886–1906).
Sidra: r8 h16 7. VPIS NOVA DRUŽINA Jakofčič + † 16.2.1944 (2. svetovna
vojna); r16 h49 2. VPIS + EMŠO sidro + BRODARIČ↔ŽELJKO izmena (r16 boter
Željko + r19 boter Brodarič); r18 h34 5. VPIS — MENJAVA DRUŽINE 2× (Šimec
1887 → Šilak/Šulak 1899–1905 → Šimec 1906 — POVRAT, druga žena Kere);
r19 h60 7. VPIS — PAR Željko × Brodarič POVRAT (5. otrok istega para; botrinja
Marija Klepec 3.×); r35 h19 2. VPIS — NEZAKONSKI (očetova kolona prazna,
mati Ana Kovač [~] samostojna); r40 h44 3. VPIS — ŠTRUCELJ + HRIŽAN signali;
r43 h30 10. VPIS — MENJAVA Segina → Brinec; r48 h21 6. VPIS — POŽEK signal
(oče Janez Požek = h58 oče 1903+1905!); r51 h4 NOVA HIŠA — HRIŽAN oče +
ŠTRUCELJ mati + ŠTRAUS boter + EMŠO sidro; r52 h18 2. VPIS — VRZEL 8 LET;
r54 h20 5. VPIS — ISTA DRUŽINA Perdinec/Pozdirec × Klepec; r56 h42 3. VPIS
ZAPORED (Pezdirec × Jurajevič/Jurasovič — ista družina 2. leto); r62 h24 12.
VPIS — ŠE VEDNO najbolj vpisovana hiša registra (povrat Brincove hiše) +
EMŠO sidro; r66 h69 9. VPIS — isti oče Janez Željko bajtar; r71 h26 4. VPIS
— VRZEL 10 LET + ŠEGINA signal (oče = h30 oče 1902/1903) + HRIŽAN boter;
r79 h27 8. VPIS — HRIŽAN botrinja (Katarina = h34 botrinja 1903) + PEZDIREC
oče; r85 h35 5. VPIS — HRIŽAN ×2 (mati + botrinja) + PEZDIREC oče; r86 h15
6. VPIS — ŠTRAUS signal (Matija Štraus: lead 04455 na 4. hiši h45→h40→h16→
h15, VENDAR mati Marjeta Simec — 2. Štrausov par [MERI]) + ŠTRUCELJ boter.
DUHOVNIKI NOVELA (celo leto 87): Jos. Rauq 39 + NOV KAPLAN J. R. Kulbinek
(o.t.cap.) 20 — prvi podpis r38 = 12.5.1906 + Hugo Hengsfeld 17 (samo
Januar–April) + NOV coop. P. Kazimir Škrabec 7 (r76–r79 + r85–r87) + Dostál
1 (dualni podpis r30!) + prazni 4 (mrtvorojeni); na Gribljih 18/18: Rauq 7 +
Kulbinek 6 + Škrabec 3 + Hengsfeld 2. BABICA NOVELA: TOTER 0× — PRVIČ v
vzorcu (1886–1906)!; Marjeta Vötter 5× na Gribljih (zapisi Sotter 1889 →
Toter 1901–05 → Vötter 1906 — ista Marjeta? [MERI]); na Gribljih 18/18:
Mih (+Mihelič[~]) 10 + Vötter 5 + Adlešič 1 + Burek[~] 1 + Dragoš 1; celo
leto 83 imenovanih / 1 prazna (r34) / 3 neberljive (r10 trak, r11+r12
nalepka). EMŠO kampanja: 3 sidra na Gribljih (r16, r51, r62 — vsi skladni).
Anomalije: 4 mrtvorojeni (r21/r22/r26/r29, podpisi prazni); dualni podpis
r30 (Hengsfeld + Dostál); ciganka mati r31 (Dobravice — Hudorovac pattern);
nezakonski r35; dvojni modri pripis r51 (umrl 1994 + umrla 2004); izblidla
podpis r71; dvojčka r81/r82 (Krasinec 18); 5 dojenčkov † na Gribljih
(svinčniki r48/r52/r54/r66/r79); kraj forenzika: r39 = Otok 20 (NI Griblje
— prvo branje revidirano!), r73 = Prilozje 25, r87 = Grm 25. Excluded: 10.

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
DOKAZ = "research/issue17/parish-baptism-1906.json"
DOKAZ_P100 = "research/issue17/parish-baptism-1905.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (170, 179)        # skeni 170/171 (str. 158: glava 1906 + rows 1–12) – 178/179 (str. 165: rows 85–87 + glava 1907)
FRAME_PAGES = (158, 165)
DATA_SCANS = [170, 172, 173, 174, 175, 176, 177, 178]
EXPECTED_CITED = [170, 172, 173, 174, 175, 176, 177, 178]
EXPECTED_PAGES = [158, 159, 160, 161, 162, 163, 164, 165]
EXPECTED_ENTRIES = 18
EXPECTED_DISTINCT = 18          # 18 vpisov / 18 hiš — NARE ponovno
EXPECTED_EXCLUDED = 10          # r11+r12 nalepka, r21/r22/r26/r29 mrtvorojeni, r31 ciganka, r39 Otok, r73 Prilozje, r87 Grm
EXPECTED_HOUSES = sorted({4, 15, 16, 18, 19, 20, 21, 24, 26, 27, 30, 34, 35, 42, 44, 49, 60, 69})
EXPECTED_PT_IN_SET = ["4", "15", "16", "18", "19", "20", "21", "24", "26", "27", "30", "34", "35", "69"]
EXPECTED_PT_GAP = ["42", "44", "49", "60"]  # ponovitve že dokazanih (42 P99, 44 1888/1901, 49 P92, 60 P84)
EXPECTED_REPEATS = 0            # NARE ponovno — 0 intra-letnih ponovitev
EXPECTED_NEW_HOUSES = 1         # h4 (85. hiša v vitals; 1. nova po dveh letih 0+0)
EXPECTED_VITALS_TOTAL = 681     # HOUSE_VITALS 323 + 18 (P101: krstna 1906)  # POSODABLJENO P138: 490 (era P106) → 651 (P137) → 659 (P138: + 8 poročnih blokov 1909!)
BLOCKS_04105 = 502              # 297 + 18  # POSODABLJENO P138: 441 (era P106) → 502 (krstna knjiga zrasla P107–P114!)
KUMULATIV_ENTRIES = 347         # 329 + 18
KUMULATIV_HOUSES = 85
KUMULATIV_YEARS = 21            # 1886–1906
# kontinuitete (hiša → zadnje krstno leto pred 1906 v 04105, iz parish.ts)
CONTINUITY = {
    "4": None, "15": 1904, "16": 1904, "18": 1898, "19": 1901, "20": 1903,
    "21": 1904, "24": 1904, "26": 1896, "27": 1902, "30": 1903, "34": 1905,
    "35": 1903, "42": 1905, "44": 1901, "49": 1899, "60": 1904, "69": 1904,
}
# sidra/pini P101 (row, scan, hiša, pin):
ANCHORS = [
    (8, 170, "16", "2. svetovna vojna"),
    (8, 170, "16", "7. VPIS"),
    (16, 172, "49", "Brodarič"),
    (16, 172, "49", "EMŠO"),
    (19, 172, "60", "ŽELJKO"),
    (35, 173, "19", "NEZAKONSKI"),
    (40, 174, "44", "Štrucelj"),
    (43, 174, "30", "Brinec"),
    (48, 174, "21", "Požek"),
    (51, 175, "4", "NOVA HIŠA"),
    (52, 175, "18", "VRZEL 8 LET"),
    (54, 175, "20", "Pezdirec"),
    (56, 175, "42", "3. VPIS ZAPORED"),
    (62, 176, "24", "12. VPIS"),
    (66, 176, "69", "Željko"),
    (71, 176, "26", "ŠEGINA"),
    (79, 177, "27", "HRIŽAN"),
    (85, 178, "35", "HRIŽAN"),
    (86, 178, "15", "ŠTRAUS"),
    (86, 178, "15", "Štrucel"),
]
EMSO_ANCHOR_ROWS = {
    16: "2102906500234",
    51: "3107906505454",
    62: "0609906500161",
}
GRIBLJE_TOTER = 0               # NOVELA: TOTER 0× — prvič v vzorcu!
GRIBLJE_MIH = 10                # Mih (+Mihelič[~])
GRIBLJE_VOTTER = 5              # NOVELA: Vötter 5×
MIDWIFE_NAMED = 83              # celo leto (87 vrstic)
MIDWIFE_EMPTY = 1               # r34 (»—«)


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
    """NOVELA P101: EN podvojen par v okviru leta (+ en 170/171 = 1906 glava).
    skeni 170/171 = str. 158 (dup par); stran == sken − 13 (172–178);
    skeni 178/179 = str. 165 (dup par); stran == sken − 14 (180+)."""
    if scan in (170, 171):
        return 158
    if scan in (178, 179):
        return 165
    if scan <= 178:
        return scan - 13
    return scan - 14


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p100 = json.load(open(DOKAZ_P100, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]

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

    # I4 — okvir leta: glava 1906 na str. 158 = sken 170/171 (P100 dokazano)
    # … row 87 (skeni 178/179, str. 165); glava 1907 POD r87; 87 vrstic;
    # DVA dup para; page_of_scan konsistenten
    fr = dokaz["frame"]
    dup_pairs = {("170,171", 158), ("178,179", 165)}
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 170 and fr["yearStart"]["page"] == 158
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 178 and fr["yearEnd"]["page"] == 165
        and fr["yearEnd"]["row"] == 87
        and fr["rowsTotal"] == 87
        and fr["duplicateScans"]["count"] == 2
        and {(p["scans"][0], p["scans"][1], p["page"]) for p in fr["duplicateScans"]["pairs"]}
        == {(170, 171, 158), (178, 179, 165)}
        and len(dup_pairs) == 2
    ) and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
    inv["I4_glava_notes"] = (
        "P100 lead POTRJEN" in fr["yearStart"]["note"]
        and "1907" in fr["yearEnd"]["note"]
        and fr["duplicateScans"]["count"] == 2
    )

    # I5 — štetja: 18 vpisov / 18 hiš; 10 excluded; NARE ponovno (0 ponovitev);
    # 1 nova hiša (h4); babica celo leto 83/1 + Toter 0× + Mih 10 + Vötter 5
    # na Gribljih; EMŠO sidri r16/r51/r62
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and houses_written == EXPECTED_HOUSES
        and dokaz["stats"]["intraYearRepeats"] == EXPECTED_REPEATS
        and "NARE" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["midwifeNamed"] == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeEmpty"] == MIDWIFE_EMPTY
        and sum(1 for e in entries if "Toter" in e["babica"]) == GRIBLJE_TOTER
        and sum(1 for e in entries if "Mih" in e["babica"]) == GRIBLJE_MIH
        and sum(1 for e in entries if "Vötter" in e["babica"]) == GRIBLJE_VOTTER
        and all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
                for row, EMSO in EMSO_ANCHOR_ROWS.items())
    )

    # I6 — PT klasifikacija: 14 v naboru + 4 v luknji (42/44/49/60 = ponovitve);
    # 1 nova hiša (h4, v naboru); PT_GAP_KNOWN nespremenjen (ostaja samo 51);
    # kumulativ 347/85/21
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["ptInNabor"] == 14
        and dokaz["stats"]["newSampleHouses"] == 1
        and dokaz["stats"]["cumulative"]["entries"] == KUMULATIV_ENTRIES
        and dokaz["stats"]["cumulative"]["houses"] == KUMULATIV_HOUSES
        and dokaz["stats"]["cumulative"]["years"] == KUMULATIV_YEARS
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"42"' in pt_gap_set and '"44"' in pt_gap_set       # ponovitve že dokazanih
        and '"49"' in pt_gap_set and '"60"' in pt_gap_set
    )

    # I7 — sidra (20 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r8 = e_by_row(8)
    r19 = e_by_row(19)
    r51 = e_by_row(51)
    r62 = e_by_row(62)
    r86 = e_by_row(86)
    inv["I7_anchors"] = (
        ok7
        # r8 — h16 7. VPIS nova družina Jakofčič + † 1944
        and r8["child"] == "Leopold" and "Jakofčič" in r8["father"]
        and "1944" in " ".join(r8["notes"])
        # r19 — h60 par Željko × Brodarič povrat (5. otrok)
        and r19["child"] == "Jožefa" and "Nikolaj Željko" in r19["father"]
        and "Marija Brodarič" in r19["mother"] and "5. OTROK" in " ".join(r19["notes"])
        # r51 — h4 NOVA HIŠA + Hrižan oče + Štrucel mati + Štraus boter + EMŠO
        and r51["child"] == "Ana" and "Janez Hrižan" in r51["father"]
        and "Štrucel" in r51["mother"] and "Štraus" in r51["botra"]
        and "3107906505454" in " ".join(r51["notes"])
        # r62 — h24 12. VPIS najbolj vpisovana
        and r62["child"] == "Janez" and "Janez Brinec" in r62["father"]
        and "najbolj vpisovana" in " ".join(r62["notes"])
        # r86 — h15 ŠTRAUS × Simec (2. Štrausov par)
        and r86["child"] == "Francišek" and "Matija Štraus" in r86["father"]
        and "Marjeta Simec" in r86["mother"] and "2. Štrausov par" in " ".join(r86["notes"])
    )

    # I8 — kontinuitete: vsaka hiša ima pravilen zadnji prior-leto v parish.ts
    vitals = parish_vitals_04105()
    prior = {}
    for v in vitals:
        h, y = v["houseNo"], v["year"]
        if h in CONTINUITY and y is not None and y < 1906:
            if h not in prior or y > prior[h]:
                prior[h] = y
    inv["I8_continuity"] = all(prior.get(h) == y for h, y in CONTINUITY.items())

    # I9 — vitals projekcija: 04105 blokov 315 (297 + 18); 1906 bloki == 18;
    # SKUPNI HOUSE_VITALS (vse 3 knjige) == 341 (323 + 18)
    blocks_1906 = [v for v in vitals if v["year"] == 1906]
    all_src = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"bookSignature:\s*\"(04105|04894|04455)\"", all_src))  # P138: metoda bookSignature-štetja (stara {}-regex preskakovala bloke z zavitimi oklepaji!)
    inv["I9_vitals_projection"] = (
        len(vitals) == BLOCKS_04105
        and len(blocks_1906) == EXPECTED_ENTRIES
        and sorted(int(v["houseNo"]) for v in blocks_1906) == EXPECTED_HOUSES
        and total_blocks == EXPECTED_VITALS_TOTAL
    )

    # I10 — neodvisen preracun: vsi village == Griblje; sken→stran konsistenten
    # z vnosnim scan/page; P100 kumulativ == 329/84 (veriga)
    ok10 = all(e["village"] == "Griblje" for e in entries)
    ok10 = ok10 and all(
        e["page"] == page_of_scan(e["scan"]) for e in entries)
    ok10 = ok10 and all(
        any(e["scan"] == s for s in dokaz["source"]["scans"]) for e in entries)
    cum_p100 = dokaz_p100["stats"]["cumulative"]
    ok10 = ok10 and cum_p100["entries"] == 329 and cum_p100["houses"] == 84
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
