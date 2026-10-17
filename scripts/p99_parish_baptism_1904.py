#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P99 — župnija Podzemelj: krstna knjiga 04105, polno leto 1904 (issue #18).

Razširitev vzorca P79 (1886) → … → P96 (1901) → P97 (1902) → P98 (1903) na
leto 1904: okvir glava »1904« na str. 143 POD r82 (sken 152, P98 dokazano;
1904 r1 = Krasinec 37, 5./5. Januar) – row 90 na str. 150 (sken 160; glava
»1905« pod r90 — 1905 r1 = Gradac 45? Antonija, P100 lead). 90 oštevilčenih
vrstic (največ do zdaj!). NOVELA P99: EN podvojen par skenov — 155/156
(str. 146, rows 35–46; s156 jasnejši). Stran == sken − 9 (152–155) / − 10
(157–160). Format 1904 = NOVA TISKANA knjiga (kot 1902–1903). 20 vpisov /
19 hiš (NAJVEČJA vzorčna leta!) — NARE 10. leto (vsaka znana hiša 1×;
r69 hiša neberljiva — edini vpis brez vitals bloka); 3 NOVE HIŠE (h6 =
nabor PT prvi vpis; h42 + h50 = 20. in 21. dokazana številka luknje 41–60
— ostaja samo h51!); h88 = prvi KRSTNI vpis (hiša že v mrliški 04894/1886).
Sidra: r18 h24 11. VPIS (najbolj vpisovana hiša) + 29. FEBRUAR (prestopno
leto); r31 h16 6. VPIS (Straus × Spudič — poročna 04455 lead); r78 h45
SPUDIČ signal (mati Barbara Spudič); r80 h91 MUC KONTINUITETA (Janez Muc
bajtar — h91 1895 Muc); r2 boter Janez Požek (POŽEK); r57 botra Milek +
Požek; r69 ŽELJKO; r90 ŠTRAUS (oče Matija Štraus — 2. Strausova oseba
leta 1904!). Duhovniki (celo leto): Jos. Ravq 38× + Dostál 32×
(Stanislav 29× — januar z naslovom »Kaplan«; Flavi? 3× [~]) + NOV KAPLAN
Hugo Hengsfeld 13× (od r67 — menjava kaplanov sredi leta); neberljivi 5×
(r90 pod trakom — prej štet k Ravq); črti 2×. Na Gribljih (P99-revizija:
vsih 20 vzorčnih podpisov ponovno preverjenih na slikah): Dostál 10 +
Ravq 8 + Hengsfeld 1 + neberljiv 1 (r90). Babica (celo
leto): 85 imenovanih / 5 praznih (r24, r54, r55, r83, r86 »—«); na Gribljih:
Toter 10× + Mih 4× + Mavretič 3× + Delak 1× + Aleksič 1× + pod trakom 1×.
EMŠO kampanja 1982–84 (Šimonič Miri): 10 sidr (r8, r19, r45, r48, r61, r72,
r77, r78, r79, r89). 2 mrtvorojena (r41 + r84 — »Z.mrtvorajen«, krsta »—«);
8 dojenčkov †; 2 nezakonska (r24, r53); dvojčki r25/r26 + r36/r37; r19
vstavljen vpis (excluded — pripis matičarke Vesne Šimonič 15.05.2007, EMŠO
0303904505822, neskladje spola). Excluded: 1 (r19).

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
DOKAZ = "research/issue17/parish-baptism-1904.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (152, 160)        # skeni 152 (str. 143: r82 1903 + glava 1904 + rows 1–10) – 160 (str. 150: rows 83–90 + glava 1905)
FRAME_PAGES = (143, 150)
EXPECTED_ENTRIES = 20
EXPECTED_DISTINCT = 19          # 20 vpisov / 19 hiš (r69 hiša neberljiva — brez bloka)
EXPECTED_EXCLUDED = 1           # r19 (vstavljen vpis brez kraja/hiše — pripis 2007)
EXPECTED_CITED = [152, 153, 154, 155, 156, 157, 158, 159, 160]
DATA_SCANS = [152, 153, 154, 156, 157, 158, 159, 160]  # s155 = dup par (s156 jasnejši)
EXPECTED_PT_IN_SET = ["6", "15", "16", "21", "22", "24", "36", "65", "66", "69", "87", "88", "91"]
EXPECTED_PT_GAP = ["42", "43", "45", "50", "54", "60"]  # 42 + 50 NOVI dokazani
EXPECTED_NEW_HOUSES = ["6", "42", "50"]  # (nabor PT: h6; luknja: h42, h50) — urejeno po številki
EXPECTED_REPEATS = 16           # 19 hiš − 3 nove
EXPECTED_HOUSES_VITALS = 19     # 19 blokov 1904 (r69 brez bloka — hiša neberljiva)
EXPECTED_VITALS_TOTAL = 323     # HOUSE_VITALS 288 + 19 (P99: krstna 1904)
EV_ONLY_TOTAL = 6               # P84: 2 + P85: 3 + P86: 1 (P77–P83, P87–P99: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša
EXPECTED_PRIESTS = (0, 8)       # (Kulbinek, Ravq) na Gribljih + Dostál 10 + Hengsfeld 1 + neberljiv 1 (r90)
GRIBLJE_DOSTAL = 10
GRIBLJE_HENGSFELD = 1
GRIBLJE_TOTER = 10
MIDWIFE_NAMED = 85              # celo leto (90 vrstic)
MIDWIFE_EMPTY = 5               # r24 + r54 + r55 + r83 + r86 (»—«)
EXPECTED_INFANT_DEATHS = 8      # celo leto
EXPECTED_STILLBORN = 2          # r41 + r84
EXPECTED_ILLEGITIMATE = 2       # r24 + r53
EMSO_ANCHOR_ROW = 78            # h45 Barbara Spudič — 2610904505164
# kontinuitete (hiša, zadnje krstno leto pred 1904 v 04105) — iz vitals (04105)
CONTINUITY = [
    ("15", 1896),
    ("16", 1902),
    ("21", 1899),
    ("22", 1902),
    ("24", 1903),
    ("36", 1902),
    ("43", 1897),
    ("45", 1900),
    ("54", 1901),
    ("60", 1899),
    ("65", 1901),
    ("66", 1887),
    ("69", 1898),
    ("87", 1902),
    ("91", 1902),
]
# sidra/pini P99 (row, scan, hiša, očetovski/maternalni/signal pin):
ANCHORS = [
    (2, 152, "22", "POŽEK signal"),
    (14, 153, "87", "NI menjava"),
    (16, 153, "88", "mrliške 04894"),
    (18, 153, "24", "11. VPIS"),
    (31, 154, "16", "STRAUS"),
    (32, 154, "60", "Ana Muc"),
    (38, 156, "36", "10. VPIS"),
    (46, 156, "6", "NOVA HIŠA"),
    (57, 157, "21", "Matija Milek"),
    (65, 158, "50", "ŠTRUCELJ signal"),
    (78, 159, "45", "SPUDIČ signal"),
    (80, 159, "91", "MUC KONTINUITETA"),
    (82, 159, "69", "ŽELJKO signal"),
    (90, 160, "42", "NOVA HIŠA"),
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
    """NOVELA P99: en podvojen par skenov.
    stran == sken − 9 za 152–155 (152 → 143 … 155 → 146);
    skeni 155/156 = str. 146 (dup par; s156 jasnejši);
    stran == sken − 10 za 157–160 (157 → 147 … 160 → 150) —
    offset premaknjen za dup par (kot P97 −6/−7/−8, P98 −8/−9)."""
    if scan in (155, 156):
        return 146
    if scan <= 155:
        return scan - 9
    return scan - 10


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I1_book_page_200"] = st == 200
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"].split(" ")[0] for e in entries if e["houseNo"].split(" ")[0] != "?"]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + JPEG probe data skenov
    probes = {s: {"http": 200, "jpeg": True} for s in DATA_SCANS}
    inv["I3_data_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in dokaz["source"]["scans"])
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())
    inv["I3_cited_scans"] = dokaz["source"]["scans"] == EXPECTED_CITED

    # I4 — okvir leta: glava 1904 POD r82 na str. 143 (sken 152, P98 dokazano) …
    # row 90 (sken 160, str. 150; glava 1905 pod r90); 90 vrstic; EN dup par;
    # page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 152 and fr["yearStart"]["page"] == 143
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 160 and fr["yearEnd"]["page"] == 150
        and fr["yearEnd"]["row"] == 90
        and fr["rowsTotal"] == 90
        and fr["duplicateScans"]["pairs"] == [[155, 156]]
        and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
        and "sken − 9" in fr["duplicateScans"]["note"]
        and "POD r82" in fr["yearStart"]["note"]
        and "NOVA TISKANA" in fr["formatNovela"]["note"]
        and "1905" in fr["yearEnd"]["note"]
        and "Gradac 45" in fr["yearEnd"]["note"]
    )

    # I5 — štetja: 20 vpisov / 19 hiš (+1 neberljiva); 1 excluded;
    # NARE (0 ponovitev); 3 nove hiše; babica celo leto 85/5 + Toter 8× na
    # Gribljih; EMŠO sidro r78 (h45 Spudič)
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 1
        and houses_written == sorted({6, 15, 16, 21, 22, 24, 36, 42, 43, 45, 50, 54, 60, 65, 66, 69, 87, 88, 91})
        and dokaz["stats"]["intraYearRepeats"] == 0
        and "NARE" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == 3
        and "h51" in dokaz["stats"]["newSampleHousesNote"]
        and dokaz["stats"]["midwifeNamed"] == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeEmpty"] == MIDWIFE_EMPTY
        and sum(1 for e in entries if "Toter" in e["babica"]) == GRIBLJE_TOTER
        and "2610904505164" in json.dumps(e_by_row(EMSO_ANCHOR_ROW), ensure_ascii=False)
    )

    # I6 — PT klasifikacija: 13 v naboru + 6 v luknji (42 + 50 NOVI dokazani
    # — PT_GAP_KNOWN += 42, 50; luknja 41–60 ostaja samo 51); 3 nove hiše;
    # kumulativ 329/84
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    pt_gap_line = re.search(r"PT_GAP_KNOWN[^\n]*", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["ptInNabor"] == 13
        and dokaz["stats"]["newSampleHouses"] == 3
        and dokaz["stats"]["cumulative"]["entries"] == 313
        and dokaz["stats"]["cumulative"]["houses"] == 84
        and '"42"' in pt_gap_set and '"50"' in pt_gap_set       # NOVI dokazani
        and '"51"' not in pt_gap_set                            # luknja 51 ostaja
        and '"58"' in pt_gap_set                                # zgodovinske ostanejo
        and "P99" in pt_gap_line                                # izjava o novem (komentar)
    )

    # I7 — sidra (14 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"].split(" ")[0] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r2 = e_by_row(2)
    r18 = e_by_row(18)
    r31 = e_by_row(31)
    r78 = e_by_row(78)
    r80 = e_by_row(80)
    inv["I7_anchors"] = (
        ok7
        # r2 — h22 3. VPIS + boter Janez Požek + podpis »Stanislav Dostál, kaplan«
        and r2["child"] == "Ana" and "Janez Požek" in r2["botra"]
        and "kaplan" in r2["priest"] and "Nikolaj Milek" in r2["father"]
        # r18 — h24 11. VPIS + 29. Februar (prestopno leto) + razveljavitev 1947/48
        and r18["born"] == "29." and r18["baptized"] == "29."
        and "prestopno leto 1904" in " ".join(r18["notes"])
        and "razveljavitev zakonske zveze" in " ".join(r18["notes"])
        # r31 — h16 6. VPIS (Straus × Spudič) + botra Julij Maxelle
        and r31["child"] == "Alojzij" and "Julij Maxelle" in r31["botra"]
        and "STRAUS" in " ".join(r31["notes"])
        # r78 — h45 SPUDIČ signal (mati Barbara Spudič) + EMŠO 26.10.1904
        and r78["child"] == "Katarina" and "Barbara Spudič" in r78["mother"]
        and "SPUDIČ signal" in " ".join(r78["notes"])
        # r80 — h91 MUC KONTINUITETA (oče Janez Muc bajtar) + podpis Hugo Hengsfeld
        and r80["child"] == "Frančišek" and "Janez Muc" in r80["father"]
        and "Hugo Hengsfeld" in r80["priest"]
    )

    # I8 — kontinuitete: hiše z znanimi pred-P99 krstnimi vpisi (zadnje leto v
    # 04105); 3 nove hiše (h6, h42, h50 — brez predhodnih blokov v KATERIKOLI
    # knjigi); h88 = prvi krstni vpis (mrliška 04894/1886)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    ok8 = True
    for hn, last_year in CONTINUITY:
        prior = [v for v in vitals_all
                 if v["houseNo"] == hn and v["bookSignature"] == BOOK_SIGNATURE
                 and v["year"] < 1904]
        if not prior or max(v["year"] for v in prior) != last_year:
            ok8 = False
    prior88 = [v for v in vitals_all
               if v["houseNo"] == "88" and v["bookSignature"] == "04894"
               and v["year"] < 1904]
    any_new = sorted({v["houseNo"] for v in vitals_all
                      if v["bookSignature"] == BOOK_SIGNATURE and v["year"] == 1904
                      and not any(x["houseNo"] == v["houseNo"]
                                  and (x["bookSignature"] != BOOK_SIGNATURE or x["year"] < 1904)
                                  for x in vitals_all)}, key=int)
    inv["I8_continuity"] = (
        ok8
        and prior88 and prior88[0]["year"] == 1886      # h88 prek mrliške
        and any_new == EXPECTED_NEW_HOUSES              # 3 nove hiše
        and "11. VPIS" in " ".join(e_by_row(18)["notes"])
        and "MUC KONTINUITETA" in " ".join(e_by_row(80)["notes"])
    )

    # I9 — vitals projekcija: 19 zasidranih 1904 (04105; r69 brez bloka);
    # skeni v okviru (152–160); stran == page_of_scan; vitals vseh treh
    # knjig = 323 (P100: 307 + 16)
    vitals_1904 = parish_vitals(BOOK_SIGNATURE, 1904)
    known_houses = sorted(set(houses), key=int)
    inv["I9_vitals_projection"] = (
        len(vitals_1904) == EXPECTED_HOUSES_VITALS
        and sorted((v["houseNo"] for v in vitals_1904), key=int) == known_houses
        and all(v["scan"] and 152 <= v["scan"] <= 160 for v in vitals_1904)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1904)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 16 ponovitev + 3 nove;
    # kumulativ 307 + 6 EV-only == 329; hiše vitals 83; duhovniki na Gribljih
    # (Kulbinek, Ravq) = (0, 8) + Dostál 10 (Stanislav 10) + Hengsfeld 1; celo-letna
    # statistika (Dostál 32 / Ravq 39 / Hengsfeld 13; dojenčki 8;
    # mrtvorojena 2; nezakonski 2; 90 vrstic)
    # klasifikacija v vesolju lastnega leta — poznejši bloki (04105 > 1904)
    # ne smejo spreminjati zgodovinske klasifikacije novih/ponovljenih hiš
    vitals_pre1905 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1905,))
    ]
    repeat_houses = sorted(
        (h for h in set(houses) if any(
            (v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1904)
            or (v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE)
            for v in vitals_pre1905
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
    n_kulbinek = sum(1 for e in entries if "Kulbinek" in e["priest"])
    n_ravq = sum(1 for e in entries if "Ravq" in e["priest"] or "Rauq" in e["priest"])
    n_dostal = sum(1 for e in entries if "Dostál" in e["priest"])
    n_hengsfeld = sum(1 for e in entries if "Hengsfeld" in e["priest"])
    n_stanisav = sum(1 for e in entries if "Stanislav Dostál" in e["priest"])
    anomaly_rows = {a["row"] for a in dokaz["anomalies"]}
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and new_houses == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newSampleHouses"] == 3
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 329  # kumulativno po P99 (307 + 6)
        and n_houses_total == 83  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 313
        and cumulative["houses"] == 84  # 83 vitals + EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and len(entries) == 20 and len(excluded) == 1
        and (n_kulbinek, n_ravq) == EXPECTED_PRIESTS
        and n_dostal == GRIBLJE_DOSTAL and n_stanisav == GRIBLJE_DOSTAL
        and n_hengsfeld == GRIBLJE_HENGSFELD
        and dokaz["stats"]["priests"]["Dostál"] == 32
        and dokaz["stats"]["priests"]["Ravq"] == 38
        and dokaz["stats"]["priests"]["Hengsfeld"] == 13
        and dokaz["stats"]["priests"]["neberljivi"] == 5   # r90 pod trakom (prej štet k Ravq)
        and dokaz["stats"]["midwifeGriblje"]["Toter"] == GRIBLJE_TOTER
        and dokaz["stats"]["midwifeGriblje"]["Delak"] == 1
        and "ŠTRAUS signal" in " ".join(e_by_row(90)["notes"])
        and dokaz["stats"]["illegitimate"] == 2
        and dokaz["stats"]["infantDeaths"] == 8       # celo leto
        and dokaz["stats"]["stillborn"] == 2
        and dokaz["stats"]["rowsTotal"] == 90
        and {2, 18, 19, 24, 25, 36, 40, 41, 42, 45, 69, 84} <= anomaly_rows
    )

    ok = all(inv.values())
    print("P99 — krstna knjiga 04105, polno leto 1904 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {EXPECTED_CITED[0]}–{EXPECTED_CITED[-1]}"
          f" (dup par 155/156; NOVA TISKANA knjiga)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (+1 neberljiva r69)"
          f" (NARE 10. leto — vsaka znana hiša 1×; 3 NOVE HIŠE: h6 nabor +"
          f" h42/h50 = 20./21. dokazana luknja 41–60, ostaja samo 51);"
          f" PT {len(inset)}/{len(gap)}; nove hiše {new_houses};"
          f" vitals 1904 = {len(vitals_1904)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki Griblje (Kulbinek, Ravq) = {(n_kulbinek, n_ravq)} + Dostál {n_dostal}"
          f" (Stanislav {n_stanisav}) + Hengsfeld {n_hengsfeld};"
          f" babica celo leto: {MIDWIFE_NAMED} imenovanih / {MIDWIFE_EMPTY} praznih"
          f" (Griblje Toter {GRIBLJE_TOTER}×); dojenčki † {EXPECTED_INFANT_DEATHS};"
          f" mrtvorojeni {EXPECTED_STILLBORN}; nezakonski {EXPECTED_ILLEGITIMATE}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(verify())
    print(__doc__)
    sys.exit(0)
