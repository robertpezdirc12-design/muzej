#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P94 — župnija Podzemelj: krstna knjiga 04105, polno leto 1899 (issue #18).

Razširitev vzorca P79 (1886) → … → P92 (1897) → P93 (1898) na leto 1899:
okvir skeni 109 (row 97) – 118 (row 104) == strani 106–115 (1899 r1 = Griblje
12 Marija na str. 106 — novo leto se začne z Griblji; 104 vrstic; stran ==
sken − 3 ZA CELO LETO — brez novih duplikatov; glava »1900.« na SREDINI
str. 115 = sken 118 row 105 — PRVIČ v vzorcu se novo leto NE začne na novi
strani; 1900 row 1 = Krasinec — prvič z drugo vasjo). 15 vpisov / 15 hiš —
NARE (6. leto) — PRVO LETO BREZ znotraj-letnih ponovitev (vsaka hiša 1×).
2 NOVI hiši: h22 (PT nabor 1825 — prvi matrični dokaz) + h49 (NOVA LUKNJA
ŠTEVILKA — 19. dokazana v 41–60; luknja zdaj 42/50/51). h60 TRDNI PIN
(4. vpis iste zveze Željko × Brodarič + 3. ista botra para Pendirec ×
Klepac; hišna pod modrim pripisom — kanalna + strukturna forenzika). h40
TRETJA družina v 3 letih (Berkopne 1897 → Brodarič 1898 [~] → Straus 1899)
+ STRAUS × SPUDIČ = potrditev poročnega lead-a 04455. MENJAVE: h1 Željko →
Segina (SEGINA VERIGA h70→h30→h1 — 3 hiše / 6 let), h30 4. družina (→
Županič), h34 2. družina (Šimec → Šilak), h57 oče Peter → Miha Pozdirec.
Duhovniki: Šturm 6× + Rauq 4× + Klun 2× (vrnitev) + 3 neberljivih. Dojenči-
jska umrljivost 3/15. r25 NEŠTET (matičar črno nadpisal kraj+hišno). babica
PRAZNA (14 vidnih + 1 poškodovan — 5. leto novele).

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
DOKAZ = "research/issue17/parish-baptism-1899.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
DOKAZ_P87 = "research/issue17/parish-baptism-1892.json"
DOKAZ_P88 = "research/issue17/parish-baptism-1893.json"
DOKAZ_P89 = "research/issue17/parish-baptism-1894.json"
DOKAZ_P90 = "research/issue17/parish-baptism-1895.json"
DOKAZ_P91 = "research/issue17/parish-baptism-1896.json"
DOKAZ_P92 = "research/issue17/parish-baptism-1897.json"
DOKAZ_P93 = "research/issue17/parish-baptism-1898.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (109, 118)        # skeni 109 (row 97) – 118 (row 104) == str. 106–115
FRAME_PAGES = (106, 115)
UNCITED_SCAN = 118              # sken 118 = str. 115 — samo okvir (prelom 1900), 0 Griblje vpisov 1899
BREAK_1900 = {"scan": 118, "page": 115, "row": 105}
EXPECTED_ENTRIES = 15
EXPECTED_DISTINCT = 15          # 15 vpisov / 15 hiš (NARE, brez ponovitev)
EXPECTED_EXCLUDED = 3           # r25 uničen + r27 Berkoviše + r93 Germ
EXPECTED_CITED = [109, 110, 111, 112, 113, 114, 115, 116, 117]
EXPECTED_PT_IN_SET = ["1", "12", "21", "22", "27", "30", "34", "40", "75"]  # 9 v PT naboru 1825
EXPECTED_PT_GAP = ["41", "46", "49", "57", "59", "60"]  # luknja 41–60 (49 NOVA)
PT_GAP_NEW = ["49"]             # h49 = NOVA luknja številka (19. dokazana)
EXPECTED_NEW_HOUSES = ["22", "49"]
EXPECTED_REPEATS = 13           # 15 hiš − 2 novi
EXPECTED_HOUSES_VITALS = 15
EXPECTED_VITALS_TOTAL = 288     # HOUSE_VITALS 223 + 15 (P94: krstna 1899); P95: + 16 (1900); P98: + 12 (1903)
EV_ONLY_TOTAL = 6               # P84: 2 + P85: 3 + P86: 1 (P77–P83, P87–P94: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša
EXPECTED_PRIESTS = (6, 4)       # (Šturm, Rauq) + Klun 2 + 3 neberljivih
EXPECTED_INFANT_DEATHS = 3      # r1 † 25/6.99 [~] + r26 † 2/[5-6].99 [~] + r94 † 24/6.00
# sidra/pini P94 (row, scan, hiša, očetovski/maternalni pin):
ANCHORS = [
    (1, 109, "12", "Dragar"),
    (6, 110, "46", "Brodarič"),
    (11, 110, "27", "Knekar"),
    (13, 110, "60", "Željko"),
    (15, 110, "59", "Simič"),
    (26, 111, "22", "Milek"),
    (33, 112, "41", "Kušič"),
    (37, 112, "21", "Požek"),
    (43, 113, "40", "Straus"),
    (61, 114, "1", "Segina"),
    (62, 114, "30", "Županič"),
    (71, 115, "75", "Jakobič"),
    (89, 116, "57", "Pozdirec"),
    (94, 117, "49", "Brodarič"),
    (100, 117, "34", "Šilak"),
]


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


def probe_jpeg(url):
    st, b = http_get(url, UA)
    return {"http": st, "jpeg": bool(b) and b[:2] == b"\xff\xd8", "bytes": len(b) if b else 0}


def pt_house_set():
    d = json.load(open(PT_CHAIN, encoding="utf-8"))
    return {str(r["no"]).strip() for r in d["chain"] if r.get("kind") == "hiša"}


def parish_vitals(signature, year=None):
    src = open(PARISH_TS, encoding="utf-8").read()
    out = []
    pat = r"\{[^{}]*?bookSignature:\s*\"" + signature + r"\"[^{}]*?\}"
    for m in re.finditer(pat, src, re.S):
        block = m.group(0)
        g = lambda k: (re.search(rf'{k}:\s*"([^"]*)"', block) or re.search(rf"{k}:\s*(\d+)", block))  # noqa: E731
        hn = g("houseNo")
        yr = re.search(r"year:\s*(\d+)", block)
        sc = re.search(r"scan:\s*(\d+)", block)
        pg = re.search(r"page:\s*(\d+)", block)
        out.append({
            "houseNo": hn.group(1) if hn else None,
            "year": int(yr.group(1)) if yr else None,
            "scan": int(sc.group(1)) if sc else None,
            "page": int(pg.group(1)) if pg else None,
            "bookSignature": signature,
        })
    if year is not None:
        out = [v for v in out if v["year"] == year]
    return out


def page_of_scan(scan):
    """NOVELA P92: od skena 98 stran == sken − 3 — velja za vse citirane
    skene 1899 (109–117), brez novih duplikatov."""
    return scan - 3


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    inv = {}

    # I1 — knjiga dostopna + inventar 326
    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    # I3 — citirani skeni ⊆ okvir 109–117 + JPEG probe; sken 118 NI citiran
    # (samo okvir/prelom 1900 — 0 Griblje vpisov 1899)
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == EXPECTED_CITED and UNCITED_SCAN not in cited
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1899; stran == sken − 3 (novela P92 za celo leto);
    # brez duplikatov; prelom 1900 na SREDINI str. 115 (sken 118) row 105 →
    # restart 1; rowsTotal 104; 1899 row 1 = Griblje 12
    rows = [e["row"] for e in entries]
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1899 for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and all(FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and fr["yearStart"]["scan"] == 109 and fr["yearStart"]["page"] == 106 and fr["yearStart"]["row"] == 97
        and fr["yearEnd"]["scan"] == 118 and fr["yearEnd"]["page"] == 115 and fr["yearEnd"]["row"] == 104
        and fr["rowsTotal"] == 104
        and dokaz["source"]["duplicateScan"] is None
        and fr["nextYearBreak"]["scan"] == BREAK_1900["scan"]
        and fr["nextYearBreak"]["page"] == BREAK_1900["page"]
        and fr["nextYearBreak"]["row"] == BREAK_1900["row"]
        and fr["nextYearBreak"]["restartRow"] == 1
        and fr["nextYearBreak"]["year"] == 1900
        and "sken − 3" in fr["pageOfScan"]
        and "novela P83 potrjena 12. leto" in fr["nextYearBreak"]["note"]
        and "NA SREDINI strani 115" in fr["nextYearBreak"]["note"]
        and "Griblje 12" in fr["yearStart"]["note"]
    )

    # I5 — števec: 15 vpisov / 15 hiš; 0 neberljivih hiš; NARE brez ponovitev;
    # NOVELA babica 5. leto: vseh 15 PRAZNO (ali poškodovano z »—«);
    # 3 izključeni (uničen + Berkoviše + Germ)
    houses = [e["houseNo"] for e in entries]
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"].startswith("Griblje") for e in entries)
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and all(e["babica"].startswith("—") for e in entries)  # NOVELA babica 5. leto
        and len(excluded) == EXPECTED_EXCLUDED
        and "UNIČENA" in excluded[0]["reason"].upper()
        and "NEŠTET" in excluded[0]["reason"].upper()
        and "Berkoviše" in excluded[1]["reason"]
        and "Germ" in excluded[2]["reason"]
        and "Jožef" in json.dumps(excluded[0], ensure_ascii=False)
    )

    # I6 — PT klasifikacija: 9 v naboru + 6 v luknji; NOVA LUKNJA ŠTEVILKA 49
    # (19. dokazana); 2 NOVI hiši (22, 49); kumulativ 244/79; atlas.ts
    # PT_GAP_KNOWN mora vsebovati 49 (runtime projekcija)
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newGapCount"] == 19
        and dokaz["stats"]["cumulative"]["entries"] == 244
        and dokaz["stats"]["cumulative"]["houses"] == 79
        # atlas.ts PT_GAP_KNOWN mora vsebovati 49 (runtime projekcija)
        and '"49"' in re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", open(ATLAS_TS, encoding="utf-8").read()).group(0)
    )

    # I7 — sidra (15 vpisov — očetovski pini + oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    # posebne oznake:
    r1 = e_by_row(1)
    r13 = e_by_row(13)
    r26 = e_by_row(26)
    r37 = e_by_row(37)
    r43 = e_by_row(43)
    r61 = e_by_row(61)
    r62 = e_by_row(62)
    r89 = e_by_row(89)
    r94 = e_by_row(94)
    r100 = e_by_row(100)
    inv["I7_anchors"] = (
        ok7
        and "Griblje 12" in fr["yearStart"]["note"]
        and "TRDNI PIN" in json.dumps(r13["notes"], ensure_ascii=False)
        and "ISTA ZVEZA" in json.dumps(r13["notes"], ensure_ascii=False)
        and "Klepac" in r13["botra"] and "Pendirec" in r13["botra"]
        and "NOVA ŠTEVILKA" in json.dumps(r26["notes"], ensure_ascii=False)
        and "NOVA LUKNJA" in json.dumps(r94["notes"], ensure_ascii=False)
        and "19. dokazana" in json.dumps(r94["notes"], ensure_ascii=False)
        and "Brodarič" in r94["father"] and "Milek" in r94["mother"]
        and "Spudič" in r43["mother"] and "Straus" in r43["father"]
        and "bajtar" in r43["father"]
        and "04455" in json.dumps(r43["notes"], ensure_ascii=False)
        and "TRETJA DRUŽINA" in json.dumps(r43["notes"], ensure_ascii=False)
        and "MENJAVA" in json.dumps(r61["notes"], ensure_ascii=False)
        and "SEGINA VERIGA" in json.dumps(r61["notes"], ensure_ascii=False)
        and "Griblja" in r61["village"]
        and "4. DRUŽINA" in json.dumps(r62["notes"], ensure_ascii=False)
        and "ŽUPANIČ CLUSTER" in json.dumps(r62["notes"], ensure_ascii=False)
        and "OČE MENJAVA" in json.dumps(r89["notes"], ensure_ascii=False)
        and "Željko" in r89["botra"]
        and "2. DRUŽINA" in json.dumps(r100["notes"], ensure_ascii=False)
        and "Klobučar" in r100["mother"]
        and "Segina" in r100["botra"]
        and "Knekar" in r37["botra"]  # križni sklic: botra h21 = oče h27
        and "Knekar" in json.dumps(e_by_row(11)["father"])
        and "Cvitkovič" in e_by_row(1)["mother"]
        and "UNIČEN" in json.dumps(e_by_row(89), ensure_ascii=False).upper()
    )

    # I8 — čez-letne kontinuitete prek dokazov:
    # h60 (P88 1893 + P89 1894 + P92 1897 Željko × Brodarič → P94 4. vpis ISTA ZVEZA)
    # h41 (P85 1890 + P91 1893 + P90 1896 Kušič × Jakobič → P94 4. vpis)
    # h21 (P82 1887 Požek + P91 1893 Požek × Šimec → P94 2. vpis iste zveze)
    # h75 (P87 1892 + P89 1894 Jakobič × Stubljar → P94 3. vpis)
    # h46 (P91 1893 + P87 1895 + P90 1896 + P92 1897 Brodarič → P94 5. vpis, 4. varianta matere)
    # h27 (P82 1887 + P88 1890 + P87 1892 + P91 1893 → P94 6. vpis; oče 2. branje Knekar)
    # h34 (P82 1887 Šimec → P94 2. DRUŽINA Šilak)
    # h40 (P92 1897 Berkovec + P93 1898 Brodarič [~] → P94 3. DRUŽINA Straus × Spudič)
    # h1 (P83 1888 + P87 1892 + P90 1896 Željko × Kure → P94 MENJAVA Segina)
    # h30 (P85 1890 Milek + P86 1891 + P91 1893 Jakljevič + P91 1895 Šegina → P94 4. DRUŽINA Županič)
    # h57 (P83 1888 + P84 1889 + P89 1894 Peter Pezdirec → P94 OČE MENJAVA Miha)
    # h59 (P84 1889 Pezdirec → P94 2. vpis Simič × Kure)
    # h12 (P92 1897 Dragar → P94 mati MENJAVA Cvitkovič [~])
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p83 = json.load(open("research/issue17/parish-baptism-1888.json", encoding="utf-8"))
    p84 = json.load(open(DOKAZ_P84, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p88 = json.load(open(DOKAZ_P88, encoding="utf-8"))
    p89 = json.load(open(DOKAZ_P89, encoding="utf-8"))
    p90 = json.load(open(DOKAZ_P90, encoding="utf-8"))
    p91 = json.load(open(DOKAZ_P91, encoding="utf-8"))
    p92 = json.load(open(DOKAZ_P92, encoding="utf-8"))
    p93 = json.load(open(DOKAZ_P93, encoding="utf-8"))

    def hs(d, h):
        return [e for e in d["entries"] if str(e.get("houseNo")) == h]

    def blob(d, h):
        return json.dumps(hs(d, h), ensure_ascii=False)

    inv["I8_continuity"] = (
        len(hs(p88, "60")) >= 1 and "Željko" in blob(p88, "60") and "Brodarič" in blob(p88, "60")
        and len(hs(p89, "60")) >= 1 and len(hs(p92, "60")) >= 1
        and len(hs(p85, "41")) >= 1 and len(hs(p88, "41")) >= 1 and len(hs(p91, "41")) >= 1
        and len(hs(p82, "21")) >= 1 and len(hs(p88, "21")) >= 1 and "Šimec" in blob(p88, "21")
        and len(hs(p87, "75")) >= 1 and len(hs(p89, "75")) >= 1
        and len(hs(p88, "46")) >= 1 and len(hs(p90, "46")) >= 1 and len(hs(p92, "46")) >= 1
        and len(hs(p82, "27")) >= 1 and len(hs(p85, "27")) >= 1 and len(hs(p87, "27")) >= 1
        and "Klobučar" in blob(p88, "27")
        and len(hs(p82, "34")) >= 1 and "Šimec" in blob(p82, "34")
        and len(hs(p92, "40")) >= 1 and "Berkovec" in blob(p92, "40")
        and len(hs(p93, "40")) >= 1 and "Brodarič" in blob(p93, "40")
        and len(hs(p83, "1")) >= 1 and ("Željko" in blob(p83, "1") or "Zeljth" in blob(p83, "1")) and "Kure" in blob(p83, "1")
        and len(hs(p87, "1")) >= 1 and len(hs(p91, "1")) >= 1
        and len(hs(p85, "30")) >= 1 and "Milek" in blob(p85, "30")
        and len(hs(p86, "30")) >= 1  # 1891 Milek nadaljevanje
        and len(hs(p88, "30")) >= 1 and "Jakljevič" in blob(p88, "30")  # 1893 MENJAVA
        and len(hs(p90, "30")) >= 1 and "Šegina" in blob(p90, "30")  # 1895 MENJAVA
        and len(hs(p83, "57")) >= 1 and len(hs(p84, "57")) >= 1 and "Pezdirec" in blob(p84, "57")
        and len(hs(p84, "59")) >= 1
        and len(hs(p92, "12")) >= 1 and "Dragar" in blob(p92, "12")
        # popravki/izključitve:
        and "NEŠTET" in json.dumps(excluded[0], ensure_ascii=False).upper()
        and "matičar" in excluded[0]["reason"]
        # h49 NOVA LUKNJA (prvič v 41–60 za 49) + h22 NOVA (PT nabor)
        and "NOVA LUKNJA ŠTEVILKA" in json.dumps(r94["notes"], ensure_ascii=False)
        and "NOVA ŠTEVILKA" in json.dumps(r26["notes"], ensure_ascii=False)
    )

    # I9 — vitals projekcija: 15 zasidranih 1899 (04105); vsi skeni v okviru;
    # stran == sken − 3; vitals skupaj 254
    vitals_1899 = parish_vitals(BOOK_SIGNATURE, 1899)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    inv["I9_vitals_projection"] = (
        len(vitals_1899) == EXPECTED_HOUSES_VITALS
        and sorted(v["houseNo"] for v in vitals_1899) == sorted(houses)
        and all(v["scan"] and 109 <= v["scan"] <= 117 for v in vitals_1899)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1899)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 13 ponovitev + 2 novi
    # (22/49); kumulativ 254 + 6 EV-only == 260; hiše vitals 79; duhovniki
    # (Šturm, Rauq) = (6, 4) + Klun 2 + 3 neberljivih; dojenčijska umrljivost 3
    # klasifikacija v P94 vesolju — kasnejši bloki (1900 P95 + 1901 P96) NE
    # smejo spreminjati zgodovinske klasifikacije leta 1899 (filtri vesolja)
    vitals_pre1900 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1900, 1901, 1902))
    ]
    repeat_houses = sorted(
        (h for h in set(houses) if any(
            (v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1899)
            or (v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE)
            for v in vitals_pre1900
        )), key=int)
    new_houses = sorted(set(houses) - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    ev_only_houses = set()
    for fn in (DOKAZ_P84, DOKAZ_P85, DOKAZ_P86):
        d = json.load(open(fn, encoding="utf-8"))
        vit_h = {v["houseNo"] for v in vitals_all}
        for e in d["entries"]:
            hn = e.get("houseNo")
            if hn is not None and hn not in vit_h:
                ev_only_houses.add(hn)
    cumulative = dokaz["stats"]["cumulative"]
    n_sturm = sum(1 for e in entries if "Šturm" in e["priest"])
    n_rauq = sum(1 for e in entries if "Rauq" in e["priest"])
    n_klun = sum(1 for e in entries if "Klun" in e["priest"])
    n_infant = dokaz["stats"]["infantDeaths"]
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and new_houses == EXPECTED_NEW_HOUSES == dokaz["stats"]["newSampleHouses"]
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 294  # kumulativno po P98 (288 + 6)
        and n_houses_total == 80  # P94: 78; P95: + 1 (67)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 244
        and cumulative["houses"] == 79  # 78 vitals + 1 EV-only »65 [~]« (zamrznjeno P94)
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and len(entries) == 15 and len(excluded) == 3
        and (n_sturm, n_rauq) == EXPECTED_PRIESTS
        and n_klun == 2
        and n_infant == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["midwifeEmpty"] == 14
        and dokaz["stats"]["illegitimate"] == 0
        and dokaz["stats"]["priests"]["Klun"] == 2
    )

    ok = all(inv.values())
    print("P94 — krstna knjiga 04105, polno leto 1899 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited} (sken 118 = str. 115 samo okvir/prelom 1900 — ni citiran)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (NARE, brez ponovitev);"
          f" PT {len(inset)}/{len(gap)} (49 NOVA luknja); nove hiše {sorted(new_houses)};"
          f" vitals 1899 = {len(vitals_1899)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki (Šturm, Rauq) = {(n_sturm, n_rauq)} + Klun {n_klun}; † {n_infant}/15")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
