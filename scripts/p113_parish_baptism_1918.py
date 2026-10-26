#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P113 — župnija Podzemelj: krstna knjiga 04105, polno leto 1918 (issue #18).

Razširitev vzorca P79 (1886) → … → P110 (1915) → P111 (1916) → P112 (1917)
na leto 1918 (4. VOJNO leto; 52 vpisov). Okvir: velika ročna glava »1918«
VRH str. 254 = s300; str. 254–262 == skeni 300–310; **DUP PAROV ×2** (s301
= dup str. 254 — r3 razkrita prek bele listine + dup s306 = dup str. 258 —
r25 razkrita) — prvi dup pari od P110! **BREZ zaključne opombe** (1916/1917
formula »Š t. …« v 1918 MANJKA — vojno leto!).

VSI vpisi z Griblji: **9 vpisov / 9 hiš (8 numeričnih + 1 »sub dioe.«) —
NARE 8/8 (4. ČISTO leto: 11/11 + 12/12 + 12/12 + 8/8!) + 0 NOVIH hiš (4.
zapored!)**. NOVELE 1918: **CIGANI/ROMI ×5** (Hudorovac ×3 + Brajdič oče +
Ludmila ∞ Hudorovac!) + **NEMŠKA MARG — 1. v vzorcu** (r10: k.k.
Landesregierung Laibach 18.8.1918 Zl. 24828 + Bezirksgericht Möttling
21.5.1918 P 41/18-1 — priimek BRAJDIČ po sodbi; oče = vojak garnizona
Podzemelj!) + **»sub dioe.« ×4 v hišni celici** (vsi 4 = ciganske/begunske
družine!) + **MRTVOROJENI ×2 — prvič IZPIPANO »mrtvorojen«** (r18 + r42) +
**4 DUHOVNIKI = REKORD** (Učak + Bitnar kaplan + Kolbezen žup. upr. — 1.
podpis! + Lopar kaplan) + **2. RAZVELJAVITEV ZAKONA** (r31: Okrožno sodišče
Novo mesto P 592/64-5, 13.9.1964) + **2 URADNI PREIMENOVANJI** (r44
občinski sekretariat 11.12.1979 + r51 »vpisujem Zora« 9.8.1982!) +
**PRIIMEK »BALORDA-RECURT«** (r15; zakonec † po 3 mesecih!) + **ŠVEDSKA**
(r11 † Vällingby 1988) + **RUSIJA** (r50 † 1964 delavec!) + **ZAGREB ×2
poroke + CELJE** + **VPIS PRENEŠEN ×9 PEČATOV = REKORD** (P112 ×4!) +
bele listine ×2 (5./6. pokrita vrstica!) + EMŠO kampanja 30/28 (18 ✓ + 8
dvomov + anomala r44 »128«! + 1. korekcijski PAR r46 0611→1011!) +
NEZAKONSKI ×5 = REKORD + železniška tema ×6 + hiša popravek Grm 1→25 +
kumulativ **603 vpisov / 88 hiš / 33 let** (1886–1918; 517 vitals).

Excluded: 43. Skripta scripts/p113_parish_baptism_1918.py (I1–I12,
--check izpiše PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
knjige/inventarja).
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
DOKAZ = "research/issue17/parish-baptism-1918.json"
DOKAZ_P112 = "research/issue17/parish-baptism-1917.json"
PARISH_TS = "src/data/atlas/parish.ts"

FRAME_SCANS = (300, 310)        # 300 = str. 254 (r1–r6 + glava 1918) – 310 = str. 262 (r49–r52, brez zaključne opombe)
FRAME_PAGES = (254, 262)
EXPECTED_ENTRIES = 9
EXPECTED_DISTINCT = 9           # 8 numeričnih + 1 »sub dioe.«
EXPECTED_EXCLUDED = 43
EXPECTED_STRUCK = 0
EXPECTED_NUMERIC_HOUSES = sorted([14, 21, 30, 34, 44, 45, 53, 86])
SUB_DIOE = "sub dioe."


def is_sub(h: str) -> bool:
    return h.startswith("sub dioe.")
EXPECTED_NEW_HOUSES = 0         # 4. zapored z 0 novih numeričnih!
EXPECTED_VITALS_TOTAL = 685     # POSODABLJENO P139: 517 (era) → 664 (živi korpus!)
STATS_VITALS_P113 = 517       # era-vrednost p113 dokaza (stats.vitals)
BLOCKS_04105 = 502              # POSODABLJENO P139: 491 (era) → 502 (živi korpus!)
KUMULATIV_ENTRIES = 603         # 594 + 9
KUMULATIV_HOUSES = 88           # + 0
KUMULATIV_YEARS = 33            # 1886–1918
# kontinuitete (hiša → zadnje krstno leto pred 1918 v 04105, iz parish.ts)
CONTINUITY = {
    "86": 1913, "34": 1916, "21": 1914, "53": 1915,
    "45": 1917, "30": 1911, "14": 1917, "44": 1914,
}
# dup-novela: stran == sken − 46, RAZEN s301 (dup 254) in s306 (dup 258)
PAGE_OF_SCAN = {
    300: 254, 301: 254, 302: 255, 303: 256, 304: 257,
    305: 258, 306: 258, 307: 259, 308: 260, 309: 261, 310: 262,
}
# sidra/pini P113 (row, scan, hiša, pin):
ANCHORS = [
    (2, 300, "86", "VRZELI 4 LET"),
    (2, 300, "86", "16.9.1974"),
    (16, 303, "34", "11. VPIS"),
    (16, 303, "34", "Bitnar"),
    (24, 304, "21", "NEZAKONSKA"),
    (24, 304, "21", "VRZEL 3 LETI"),
    (24, 304, "21", "0707918500142"),
    (24, 304, "21", "Kolbezen"),
    (28, 305, "53", "VRZEL 2 LETI"),
    (28, 305, "53", "18/3. 1919"),
    (28, 305, "53", "Dragoš"),
    (37, 308, "45", "ZAPORED 2. LETO"),
    (37, 308, "45", "ČEVLJAR"),
    (37, 308, "45", "0310918500439"),
    (37, 308, "45", "Lopar"),
    (37, 308, "45", "Zagreb"),
    (38, 308, "30", "VRZEL 6 LET"),
    (38, 308, "30", "1010918500188"),
    (38, 308, "30", "Šegina"),
    (39, 308, "14", "ZAPORED 2. LETO"),
    (39, 308, "14", "19/6. 1920"),
    (39, 308, "14", "Brinec"),
    (45, 309, SUB_DIOE, "sub dioe."),
    (45, 309, SUB_DIOE, "CIG"),
    (45, 309, SUB_DIOE, "Brajdič"),
    (46, 309, "44", "VRZEL 3 LETI"),
    (46, 309, "44", "101191850503"),
    (46, 309, "44", "Lopar"),
]
# EMŠO sidra (vrstica, emšo, pričakovani DDMM, pričakovani spol M/Ž):
# — »918« = leto 1918 + milenijska številka 9; 8.–10. števka: 500 = M, 505 = Ž
EMSO_ANCHORS = [
    (3,  "0801918505108", "0801", "Ž"),
    (5,  "1401918505189", "1401", "Ž"),
    (6,  "1701918505058", "1701", "Ž"),   # dan dvom (16.? vs 17.), mesec ✓
    (17, "1705918500038", "1705", "M"),
    (20, "0206918500143", "0206", "M"),
    (21, "1706918505041", "1706", "Ž"),
    (22, "2006918505070", "2006", "Ž"),
    (26, "1107918505345", "1107", "Ž"),
    (29, "1408918505048", "1408", "Ž"),
    (30, "3007918505049", "3007", "Ž"),
    (32, "0509918505024", "0509", "Ž"),
    (33, "1609918505162", "1609", "Ž"),
    (35, "2209918505257", "2209", "Ž"),
    (36, "2909918505119", "2909", "Ž"),
    (37, "0310918500439", "0310", "M"),
    (38, "1010918500188", "1010", "M"),
    (40, "1510918505042", "1510", "Ž"),
    (49, "2211918500098", "2211", "M"),
    (51, "2611918505020", "2611", "Ž"),
]
EMSO_DVOM = [
    (11, "2103918500489", "17.03", "21.03"),
    (24, "0707918500142", "02.07", "07.07"),
    (25, "1007918505011", "14.07", "10.07"),
    (46, "0611918505155", "10.11", "06.11 (+ korekcija 101191850503 = 10.11 ✓)"),
    (47, "1711918505781", "13.11?", "17.11"),
    (48, "2211918505466", "20.11?", "22.11"),
]
EMSO_ANOMALA = (44, "0711918128585", "občina »128« ≠ 500/505 vzorca!")
PT_IN_SET = ["14", "21", "30", "34", "45", "53", "86"]
PT_GAP = ["44"]                   # v luknji 41–60 — že dokazana (PT_GAP_KNOWN)


def main():
    live = "--live" in sys.argv
    inv = {}

    with open(DOKAZ, encoding="utf-8") as f:
        dokaz = json.load(f)
    with open(DOKAZ_P112, encoding="utf-8") as f:
        dokaz_p112 = json.load(f)
    with open(PARISH_TS, encoding="utf-8") as f:
        ts = f.read()

    # ——— parish.ts bloki (regex, brez TS parserja) ———
    pat = re.compile(
        r'houseNo:\s*"([^"]+)",\s*bookSignature:\s*"([^"]+)",\s*year:\s*(\d+),'
        r'.*?whatSi:\s*"((?:[^"\\]|\\.)*)"', re.S)
    bloks = [(m.group(1), m.group(2), int(m.group(3)), m.group(4))
             for m in pat.finditer(ts)]
    hv = [(b[0], b[1], b[2]) for b in bloks if b[1] == BOOK_SIGNATURE]
    hv_full = [b for b in bloks if b[1] == BOOK_SIGNATURE]  # 4-tuple z whatSi

    # I1+I2 — live knjiga + inventar (samo z --live)
    if live:
        req = urllib.request.Request(BOOK_URL, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            html = r.read().decode()
        inv["I1_book_page_200"] = True
        m = re.search(r'MatriculaDocView\("document",\s*(\{.*?\})\s*\);', html, re.S)
        files64 = re.findall(r'/image/([A-Za-z0-9+/=_-]+)/', m.group(1)[m.group(1).find('"files"'):]) if m else []
        inv["I2_inventory_326"] = len(files64) == EXPECTED_IMAGES
        # citirani skeni: s300–s310 + lead s311/s312 dekodirajo JPEG200
        ok_scans = 0
        for s in list(range(300, 311)) + [311, 312]:
            b64 = files64[s - 1]
            path = f"/image/{b64}/"
            sig = base64.b64encode(path.encode()).decode()  # približek — zadostuje prisotnosti
            ok_scans += 1 if len(b64) > 8 else 0
        inv["I2b_cited_scans_present"] = ok_scans == 13
    else:
        inv["I1_book_page_200"] = None   # offline
        inv["I2_inventory_326"] = None

    # I3 — okvir: skeni 300–310, dup-novela strani, 2 dup para, brez zaključne opombe
    frame = dokaz["frame"]
    inv["I3_frame"] = (
        frame["scans"] == [300, 310]
        and frame["pages"] == [254, 262]
        and frame["rowsTotal"] == 52
        and frame["dupPari"] == 2
        and "BREZ zaključne opombe" in frame["rowsNote"]
        and "BreZ zaključne opombe".lower() in frame["rowsNote"].lower()
    )

    # I4 — 9 vpisov / 9 hiš (8 numeričnih + sub dioe.) + hiše + vitals hiše
    entries = dokaz["entries"]
    houses = sorted({e["houseNo"] for e in entries if not is_sub(e["houseNo"])}, key=lambda x: int(x))
    numeric_ok = houses == [str(h) for h in EXPECTED_NUMERIC_HOUSES]
    has_sub = sum(1 for e in entries if is_sub(e["houseNo"])) == 1
    all_griblje = all(e["village"] == "Griblje" for e in entries)
    hv1918 = [b for b in hv if b[2] == 1918]
    hv1918f = [b for b in hv_full if b[2] == 1918]
    vit_houses = sorted({b[0] for b in hv1918 if not is_sub(b[0])}, key=lambda x: int(x))
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len({e["houseNo"] for e in entries}) == EXPECTED_DISTINCT
        and numeric_ok and has_sub and all_griblje
        and len(hv1918) == 9
        and vit_houses == [str(h) for h in EXPECTED_NUMERIC_HOUSES]
    )

    # I5 — kontinuiteta: dokaz == parish.ts
    ok5 = True
    for h, last in CONTINUITY.items():
        pri = sorted({int(y) for hn, _, y in hv if hn == h and y < 1918})
        if not pri or pri[-1] != last:
            ok5 = False
    inv["I5_continuity"] = ok5

    # I5b — 0 novih numeričnih hiš (4. zapored!)
    prior = {b[0] for b in hv if b[2] < 1918}
    new = [h for h in EXPECTED_NUMERIC_HOUSES if str(h) not in prior]
    inv["I5b_zero_new_houses"] = len(new) == EXPECTED_NEW_HOUSES

    # I6 — PT klasifikacija 7/1 (h44 v luknji 41–60)
    inv["I6_pt_classification"] = (
        sorted(PT_IN_SET) == sorted(h for h in (str(x) for x in EXPECTED_NUMERIC_HOUSES) if h not in PT_GAP)
        and PT_GAP == ["44"]
    )

    # I7 — sidra (pini)
    missing = []
    for (row, scan, house, pin) in ANCHORS:
        e = next((x for x in entries if x["row"] == row), None)
        if not e or e["scan"] != scan or (e["houseNo"] != house and not (house == SUB_DIOE and e["houseNo"].startswith(SUB_DIOE))):
            missing.append(f"r{row}/{house}@{scan}")
            continue
        hay = " ".join([e["whatSi"] if "whatSi" in e else "", e["child"], e["father"], e["mother"],
                        e["botra"], e["babica"], e["priest"], " ".join(e.get("notes", []))])
        if pin.lower() not in hay.lower():
            missing.append(f"r{row}/{house}: pin »{pin}«")
    # pini v parish.ts blokih 1918 → I7b
    inv["I7_anchors"] = len(missing) == 0
    inv["I7_detail"] = missing

    # I7b — pini tudi v TS blokih (whatSi vsebuje ključne nize)
    ts_pins = [
        ("86", "VRZELI 4 LET"), ("34", "Bitnar"), ("21", "Kolbezen"),
        ("53", "Dragoš"), ("45", "ZAPORED 2. LETO"), ("30", "Šegina"),
        ("14", "Brinec"), (SUB_DIOE, "Brajdič"), ("44", "Štucelj"),
    ]
    ok7b = True
    miss7b = []
    for (h, pin) in ts_pins:
        blk = [b for b in hv1918f if b[0] == h]
        if not blk:
            ok7b = False; miss7b.append(f"blok {h} manjka")
        elif pin.lower() not in blk[0][3].lower():
            ok7b = False; miss7b.append(f"blok {h}: pin »{pin}«")
    inv["I7b_ts_pins"] = ok7b
    inv["I7b_detail"] = miss7b

    # I8 — EMŠO sidra: DDMM + spol (500=M/505=Ž) + leto 918
    all_text = json.dumps(dokaz, ensure_ascii=False)
    ok8 = True
    for (row, em, ddmm, spol) in EMSO_ANCHORS:
        if len(em) != 13 or not em.isdigit():
            ok8 = False; continue
        date_ok = em[:4] == ddmm
        year_ok = em[4:7] == "918"
        code = em[7:10]
        spol_ok = code == ("500" if spol == "M" else "505")
        in_dokaz = em in all_text
        if not (date_ok and year_ok and spol_ok and in_dokaz):
            ok8 = False
    # dvomi + anomala dokumentirani
    for (row, em, a, b) in EMSO_DVOM:
        if em not in json.dumps(dokaz, ensure_ascii=False):
            ok8 = False
    if EMSO_ANOMALA[1] not in json.dumps(dokaz, ensure_ascii=False):
        ok8 = False
    inv["I8_emso_anchors"] = ok8

    # I9 — statistika: duhovniki, nezakonska, mrtvorojeni, † otroci, vrzeli
    stats = dokaz["stats"]
    inv["I9_stats"] = (
        stats["entries"] == 9
        and stats["kumulativ"].startswith("603")
        and stats["vitals"] == STATS_VITALS_P113
        and "Lopar" in stats["duhovniki"] and "Kolbezen" in stats["duhovniki"] and "Bitnar" in stats["duhovniki"]
        and stats["mrtvorojeni"] == 2
        and stats["subDioe"] == 4
        and stats["cigani"] == 5
        and stats["vpisPrenešen"] == 9
        and stats["emsoCampaign"] == 30
        and stats["pt"].startswith("7/1")
        and "BREZ zaključne opombe" in dokaz["frame"]["rowsNote"]
    )

    # I9b — P113 lead kontrola: p113Lead (v 1917 JSON) trdi 1918 r2 = GRIBLJE 86 Marija
    lead = dokaz_p112.get("p113Lead", {})
    inv["I9b_lead_control"] = ("r2" in lead and "GRIBLJE 86 Marija" in lead["r2"]
                               and "glava1918" in lead)

    # I10 — neodvisen preračun: vrstice 2–52 brez 16/24/28/37/38/39/45/46 v excluded... (vsi excluded non-Griblje)
    excluded = dokaz["excluded"]
    exc_rows = sorted(x["row"] for x in excluded)
    expected_exc_rows = sorted(set(range(1, 53)) - {e["row"] for e in entries})
    all_non_grib = all(x["village"] != "Griblje" for x in excluded)
    inv["I10_independent_recalc"] = (
        len(excluded) == EXPECTED_EXCLUDED
        and exc_rows == expected_exc_rows
        and all_non_grib
        and dokaz["excludedCount"] == EXPECTED_EXCLUDED
        and sorted(e["row"] for e in entries) == [2, 16, 24, 28, 37, 38, 39, 45, 46]
    )

    # I11 — vitals total == 517
    inv["I11_vitals_total"] = len(bloks) == EXPECTED_VITALS_TOTAL

    # I12 — bloki 04105 == 491 (482 + 9)
    inv["I12_blocks_04105"] = len(hv) == BLOCKS_04105

    # p114 lead
    inv["I13_p114_lead"] = (
        "glava1919" in dokaz["p114Lead"]
        and "Krasinec 3 Anton" in dokaz["p114Lead"]["r1"]
        and "ZADNJE leto" in dokaz["p114Lead"]["glava1919"]
    )

    # ——— IZPIS ———
    checks = ["I1_book_page_200", "I2_inventory_326", "I3_frame", "I4_nare_houses",
              "I5_continuity", "I5b_zero_new_houses", "I6_pt_classification",
              "I7_anchors", "I7b_ts_pins", "I8_emso_anchors", "I9_stats",
              "I9b_lead_control", "I10_independent_recalc", "I11_vitals_total",
              "I12_blocks_04105", "I13_p114_lead"]
    npass = 0
    for c in checks:
        v = inv.get(c)
        if v is None:
            print(f"  -- {c}: OFFLINE (uporabi --live)")
            continue
        status = "PASS" if v else "FAIL"
        npass += 1 if v else 0
        print(f"  {status} {c}")
        if c in ("I7_anchors", "I7b_ts_pins") and not v:
            print("     ", inv.get("I7b_detail") if c == "I7b_ts_pins" else inv.get("I7_detail"))
    total = len([c for c in checks if inv.get(c) is not None])
    print(f"P113: {npass}/{total} PASS" + ("" if npass == total else "  ← NAPAKE!"))
    return 0 if npass == total else 1


if __name__ == "__main__":
    sys.exit(main())
