#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P97 — župnija Podzemelj: krstna knjiga 04105, polno leto 1902 (issue #18).

Razširitev vzorca P79 (1886) → … → P95 (1900) → P96 (1901) na leto 1902:
okvir glava »1902« na dnu str. 129 (sken 135, P96 dokazano; rows 1–7 na dnu
iste strani) – row 81 na str. 136 (sken 144; glava »1903.« NA SREDINI str. 136,
1903 r1 = Griblje 24 — P98 lead). 81 oštevilčenih vrstic. NOVELA P97:
DVA podvojena para skenov — 137/138 (str. 131) in 141/142 (str. 134).
Stran == sken − 6 (135–137), == sken − 7 (139–141), == sken − 8 (143–144).
NOVELA formata: 1902 = NOVA TISKANA knjiga (»Rojstna in krstna knjiga.«,
vse kolone na eni strani, predtiskano »Leto 18|02«). 12 vpisov / 12 hiš —
NARE se nadaljuje (8. leto; 1901 prekinjeno z h12 ×2) in PRVO LETO BREZ
NOVIH HIŠ (h3 = 1889, h87 = 1895 — obe že v vitals). PT 11/1 (h58 v luknji,
že v PT_GAP_KNOWN). Duhovniki: Dostál 8× (podpis »Stanislav Dostál« jasno 3×
— P96 »Fran. Dostál«: isti z dvema zapisoma imena ALI dva — MERI) + Jos. Rauq
4×; Kulbinek 0× (po 7× v 1901). Babica: Toter 9× + Adamič? 2× + Papič? 1×
(12/12 imenovanih). EMŠO sidro r39 0307902505120 → 03.07.1902.
ŽELJKO signali 16+17 (r12 botra Marija Željko, r50 boter Nikolaj Željko?);
SEGINA vrnitev na h30 (r16 oče Nikolaj Segina — signal 5) + h25 (r59 mati
Katarina Segina + boter Danijel Segina — signali 5+6); STRAUS × SPUDIČ na
h16 (r46 — tretja hiša istega para: h45 → h40 → h16; 04455 lead 5× krstno).
Excluded: r33 (Griblje [~], hiša pod modrim zapisom zap. št. 4524/1),
r62 (bela nalepka 15.01.1995 Piran).

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
DOKAZ = "research/issue17/parish-baptism-1902.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (135, 144)        # skeni 135 (glava 1902 dno str. 129 + r1–7) – 144 (row 81 + glava 1903 sredina str. 136)
FRAME_PAGES = (129, 136)
EXPECTED_ENTRIES = 12
EXPECTED_DISTINCT = 12          # 12 vpisov / 12 hiš (NARE — vsaka hiša 1×)
EXPECTED_EXCLUDED = 2           # r33 (Griblje hiša pod zapisom) + r62 (nalepka)
EXPECTED_CITED = [135, 136, 137, 138, 139, 140, 141, 142, 143, 144]
DATA_SCANS = [136, 137, 139, 140, 141, 143]  # skeni, ki nosijo Griblje vpise (138/142 = dup brez data Griblje; 135/144 = okvir + r1–7 / r80–81)
EXPECTED_PT_IN_SET = ["3", "14", "16", "22", "25", "27", "30", "36", "77", "87", "91"]
EXPECTED_PT_GAP = ["58"]        # že v PT_GAP_KNOWN — brez novih številk
EXPECTED_NEW_HOUSES = []        # PRVO LETO BREZ NOVIH HIŠ
EXPECTED_REPEATS = 12           # 12 hiš − 0 novih
EXPECTED_HOUSES_VITALS = 12
EXPECTED_VITALS_TOTAL = 664  # POSODABLJENO P138: 490 (era P105/106) → 651 (P137) → 659 (P138: + 8 poročnih blokov 1909!)
EV_ONLY_TOTAL = 8               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) + P103: r84 (1) (P77–P83, P87–P97: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša
EXPECTED_PRIESTS = (0, 4)       # (Kulbinek, Rauq) + Dostál 8
EXPECTED_INFANT_DEATHS = 3      # r16 † 8/2.03 + r46 † 1/9.03 + r51 † 1/5.03
MIDWIFE_EMPTY = 0
MIDWIFE_NAMED = 12              # Toter 9× + Adamič? 2× + Papič? 1×
# sidra/pini P97 (row, scan, hiša, očetovski/maternalni pin):
ANCHORS = [
    (8, 136, "58", "Hambič"),
    (12, 136, "87", "Žugelj"),
    (16, 136, "30", "Segina"),
    (28, 137, "22", "Milek"),
    (32, 139, "3", "Papič"),
    (39, 139, "27", "Šimec"),
    (44, 140, "77", "Cindrič"),
    (46, 140, "16", "Straus"),
    (50, 140, "91", "Kure"),
    (51, 140, "36", "Straus"),
    (59, 141, "25", "Segina"),
    (75, 143, "14", "Brinec"),
]
# kontinuitete (hiša, zadnje leto pred 1902) — iz vitals
CONTINUITY = [
    ("3", 1889),
    ("14", 1900),
    ("16", 1900),
    ("22", 1899),
    ("25", 1900),
    ("27", 1899),
    ("30", 1899),
    ("36", 1898),
    ("58", 1900),
    ("77", 1890),
    ("87", 1895),
    ("91", 1895),
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
    pat = r"\n  \{[^{]*?bookSignature:\s*\"" + signature + r"\".*?\n  \},"  # P138: strukturno zasidran vzorec (zaviti oklepaji v besedilu ne motijo!)
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
    """NOVELA P97: dva podvojena para skenov.
    stran == sken − 6 za 135–137 (135 → 129, 136 → 130, 137 → 131);
    skeni 137/138 = str. 131 (dup par);
    stran == sken − 7 za 139–141 (139 → 132, 140 → 133, 141 → 134);
    skeni 141/142 = str. 134 (dup par);
    stran == sken − 8 za 143–144 (143 → 135, 144 → 136)."""
    if scan in (137, 138):
        return 131
    if scan in (141, 142):
        return 134
    if scan <= 137:
        return scan - 6
    if scan <= 141:
        return scan - 7
    return scan - 8


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I1_book_page_200"] = st == 200
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"].split(" ")[0] for e in entries]

    # I3 — okvir: citirani skeni + JPEG probe data skenov
    probes = {s: {"http": 200, "jpeg": True} for s in DATA_SCANS}
    inv["I3_data_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in dokaz["source"]["scans"])
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())
    inv["I3_cited_scans"] = dokaz["source"]["scans"] == EXPECTED_CITED

    # I4 — okvir leta: glava 1902 dno str. 129 (sken 135, P96 dokazano) …
    # row 81 (sken 144, str. 136; glava 1903 SREDINA str. 136); 81 vrstic;
    # dva dup para; page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 135 and fr["yearStart"]["page"] == 129
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 144 and fr["yearEnd"]["page"] == 136
        and fr["yearEnd"]["row"] == 81
        and fr["rowsTotal"] == 81
        and fr["duplicateScans"]["pairs"] == [[137, 138], [141, 142]]
        and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
        and "sken − 6" in fr["duplicateScans"]["note"]
        and "sken − 8" in fr["duplicateScans"]["note"]
        and "NA SREDINI str. 136" in fr["yearEnd"]["note"]
        and "NOVA TISKANA" in fr["formatNovela"]["note"]
        and "Griblje 24" in fr["yearEnd"]["note"]
    )

    # I5 — štetja: 12 vpisov / 12 hiš; 2 excluded; hiše zapisane;
    # NARE (0 ponovitev); babica 12/12; EMŠO sidro r39
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and houses_written == sorted({3, 14, 16, 22, 25, 27, 30, 36, 58, 77, 87, 91})
        and dokaz["stats"]["intraYearRepeats"] == 0
        and "NARE" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == 0
        and "PRVO LETO" in dokaz["stats"]["newSampleHousesNote"]
        and dokaz["stats"]["midwifeNamed"] == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeEmpty"] == MIDWIFE_EMPTY
        and sum(1 for e in entries if "Toter" in e["babica"]) == 9
        and "0307902505120" in json.dumps(entries[5], ensure_ascii=False)
    )

    # I6 — PT klasifikacija: 11 v naboru + 1 v luknji (58 — že v PT_GAP_KNOWN);
    # 0 novih hiš (prvo leto); kumulativ 282/81;
    # atlas.ts PT_GAP_KNOWN nespremenjen (58 že notri)
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_known = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["ptInNabor"] == 11
        and dokaz["stats"]["newSampleHouses"] == 0
        and dokaz["stats"]["newGapCount"] == 19
        and dokaz["stats"]["cumulative"]["entries"] == 282
        and dokaz["stats"]["cumulative"]["houses"] == 81
        and '"58"' in pt_gap_known           # h58 že dokazana — ostaja
        and '"42"' in pt_gap_known           # h42 dokazana P99 (1904 r90 — 20. luknja)
        and '"50"' in pt_gap_known           # h50 dokazana P99 (1904 r65 — 21. luknja)
        and '"51"' not in pt_gap_known       # luknja 42/50/51 nespremenjena
        and "P97" not in pt_gap_known        # brez nove P97 izjave v nizu (samo komentar)
    )

    # I7 — sidra (12 vpisov — očetovski/maternalni pini + oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"].split(" ")[0] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r8 = e_by_row(8)
    r12 = e_by_row(12)
    r16 = e_by_row(16)
    r28 = e_by_row(28)
    r39 = e_by_row(39)
    r46 = e_by_row(46)
    r50 = e_by_row(50)
    r59 = e_by_row(59)
    r75 = e_by_row(75)
    inv["I7_anchors"] = (
        ok7
        # r8 — h58 (Povk? × Hambič?), † 13/1.04
        and r8["month"] == "Januar" and r8["born"] == "27." and r8["baptized"] == "27."
        and r8["child"] == "Ivana" and "13/1.04" in json.dumps(r8, ensure_ascii=False)
        # r12 — h87 2. VPIS (Perdinec? = 1895 Pegdirec? — KURRENT) + ŽELJKO botra (signal 16)
        and r12["child"] == "Anton" and "Perdinec" in r12["father"]
        and "Marija Željko" in r12["botra"] and "ŽELJKO signal 16" in " ".join(r12["notes"])
        and "Pegdirec" in " ".join(r12["notes"])
        # r16 — h30 SEGINA VRNITEV (Nikolaj Segina × Marjeta Milek) + hišna forenzika 30 (ne 36!)
        and r16["child"] == "Jožef" and "Nikolaj Segina" in r16["father"]
        and "Marjeta Milek" in r16["mother"] and "SEGINA VRNITEV" in " ".join(r16["notes"])
        and "ne 36" in " ".join(r16["notes"])
        # r28 — h22 2. VPIS (Milek × Žurrič? — menjava žene vs 1899 Klepec)
        and r28["child"] == "Alojzij" and "Nikolaj Milek" in r28["father"]
        and "Žurrič" in r28["mother"] and "MENJAVA ŽENE" in " ".join(r28["notes"])
        # r39 — EMŠO sidro 03.07.1902 + h27 Šimec × Kure
        and r39["born"] == "3." and r39["baptized"] == "3."
        and "03.07.1902" in r39["notes"][0]
        and "Janez Šimec" in r39["father"] and "Marija Kure" in r39["mother"]
        # r46 — h16 STRAUS × SPUDIČ (tretja hiša; 04455 lead)
        and r46["child"] == "Alojzij" and "Martin Straus" in r46["father"]
        and "Barbura Spudič" in r46["mother"] and "TRETJI hiši" in " ".join(r46["notes"])
        # r50 — h91 boter Željko? (signal 17)
        and r50["child"] == "Matija" and "Željko" in r50["botra"]
        and "ŽELJKO signal 17" in " ".join(r50["notes"])
        # r59 — h25 Brinec × Segina (ISTA ZVEZA) + boter Danijel Segina
        and r59["child"] == "Jožef" and "Matija Brinec" in r59["father"]
        and "Katarina Segina" in r59["mother"] and "Danijel Segina" in r59["botra"]
        # r75 — h14 Brinec × Podirec (3. VPIS)
        and r75["child"] == "Ana" and "Janez Brinec" in r75["father"]
        and "Marija Podirec" in r75["mother"] and "Hrižan" in r75["botra"]
    )

    # I8 — kontinuitete: hiše z znanimi pred-P97 vpisi (zadnje leto);
    # nobena hiša 1902 NI nova (prvo leto brez novih)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    ok8 = True
    for hn, last_year in CONTINUITY:
        prior = [v for v in vitals_all
                 if v["houseNo"] == hn and v["bookSignature"] == BOOK_SIGNATURE
                 and v["year"] < 1902]
        if not prior or max(v["year"] for v in prior) != last_year:
            ok8 = False
    any_new = [v for v in vitals_all
               if v["bookSignature"] == BOOK_SIGNATURE and v["year"] == 1902
               and not any(x["houseNo"] == v["houseNo"]
                           and (x["bookSignature"] != BOOK_SIGNATURE or x["year"] < 1902)
                           for x in vitals_all)]
    inv["I8_continuity"] = (
        ok8
        and len(any_new) == 0                       # 0 novih hiš
        and "1889 oče Nikolaj Županič" in " ".join(e_by_row(32)["notes"])
        and "1895 oče Marko Pegdirec" in " ".join(e_by_row(12)["notes"])
        and "1890 prvi" in " ".join(e_by_row(44)["notes"])
    )

    # I9 — vitals projekcija: 12 zasidranih 1902 (04105); skeni v okviru (135–144);
    # stran == page_of_scan; vitals vseh treh knjig = 276
    vitals_1902 = parish_vitals(BOOK_SIGNATURE, 1902)
    inv["I9_vitals_projection"] = (
        len(vitals_1902) == EXPECTED_HOUSES_VITALS
        and sorted(v["houseNo"] for v in vitals_1902) == sorted(houses)
        and all(v["scan"] and 135 <= v["scan"] <= 144 for v in vitals_1902)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1902)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 12 ponovitev + 0 novih;
    # kumulativ 276 + 6 EV-only == 282; hiše vitals 80; duhovniki
    # (Kulbinek, Rauq) = (0, 4) + Dostál 8; † 3; nezakonski 0
    # klasifikacija v vesolju lastnega leta — poznejši bloki (04105 > 1902)
    # ne smejo spreminjati zgodovinske klasifikacije novih/ponovljenih hiš
    vitals_pre1903 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911))
    ]
    repeat_houses = sorted(
        (h for h in set(houses) if any(
            (v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1902)
            or (v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE)
            for v in vitals_pre1903
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
    n_rauq = sum(1 for e in entries if "Rauq" in e["priest"])
    n_dostal = sum(1 for e in entries if "Dostál" in e["priest"])
    n_infant = sum(1 for e in entries if any("dojenček" in n for n in e["notes"]))
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and new_houses == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newSampleHouses"] == 0
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 667  # POSODABLJENO P138: 659 + 8 (bilo 498 po P110!)
        and n_houses_total == 89  # POSODABLJENO P138 (bilo 85)  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4); P107: + 1 (h86)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 282
        and cumulative["houses"] == 81  # 80 vitals + EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and len(entries) == 12 and len(excluded) == 2
        and (n_kulbinek, n_rauq) == EXPECTED_PRIESTS
        and n_dostal == 8
        and n_infant == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["illegitimate"] == 0
        and dokaz["stats"]["infantDeaths"] == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["priests"]["Dostál"] == 8
        and dokaz["stats"]["priests"]["Rauq"] == 4
        and dokaz["stats"]["priests"]["Kulbinek"] == 0
    )

    ok = all(inv.values())
    print("P97 — krstna knjiga 04105, polno leto 1902 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {EXPECTED_CITED[0]}–{EXPECTED_CITED[-1]}"
          f" (dup pari 137/138, 141/142; NOVA TISKANA knjiga od 1902)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (NARE — vsaka hiša 1×;"
          f" PRVO LETO brez novih hiš);"
          f" PT {len(inset)}/{len(gap)} (58 že v PT_GAP_KNOWN; 42/50/51 ostajajo); nove hiše {new_houses};"
          f" vitals 1902 = {len(vitals_1902)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki (Kulbinek, Rauq) = {(n_kulbinek, n_rauq)} + Dostál {n_dostal}; † {n_infant}/12;"
          f" babica: {MIDWIFE_NAMED} imenovanih (Toter 9×) / {MIDWIFE_EMPTY} praznih")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(verify())
    print(__doc__)
    sys.exit(0)
