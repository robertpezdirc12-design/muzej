#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P98 — župnija Podzemelj: krstna knjiga 04105, polno leto 1903 (issue #18).

Razširitev vzorca P79 (1886) → … → P95 (1900) → P96 (1901) → P97 (1902) na
leto 1903: okvir glava »1903.« NA SREDINI str. 136 (sken 144, P97 dokazano;
1903 r1 = Griblje 24, 4./5. Januar) – row 82 na str. 143 (sken 152; glava
»1904« pod r82 — 1904 r1 = Krasinec 37, P99 lead). 82 oštevilčenih vrstic.
NOVELA P98: EN podvojen par skenov — 148/149 (str. 140, rows 46–57; s149
bolj čitljiv). Stran == sken − 8 (143–152). Format 1903 = NOVA TISKANA
knjiga (kot 1902 — »Rojstna in krstna knjiga.«, vse kolone na eni strani,
predtiskano »Leto 18|03«). 12 vpisov / 12 hiš — NARE se nadaljuje (9. leto;
1901 edini prelom z h12 ×2) in DRUGO LETO ZAPORED BREZ NOVIH HIŠ (h83
luknja 1890–1902 zaplodana — 3. VPIS; vse 12 že v vitals). PT 11/1 (h58 v
luknji, že v PT_GAP_KNOWN). Duhovniki (celo leto): Dostál 44× + Jos. Ravq
32× + Levic? 1× + manjkajoči 5×; na Gribljih: Dostál 6× (Stanislav jasno
1×) + Ravq 6×; Kulbinek 0×. Babica (celo leto): 76 imenovanih / 2 prazni
(r52+r53 »—«); na Gribljih: Toter 6× + Mavretič 2× + Mih 2× + Perdinec 1×
+ Delak 1× (12/12). EMŠO sidra: r7, r22, r56, r59 (Griblje h20:
2010903505047 → 20.10.1903), r65, r72, r80. Sidra: r1 h24 10. VPIS
(najbolj vpisovana gibriljska hiša registra); r55 REŠITEV P97 MERI (1902
r8 »Povk? × Hambič?« = ISTI PAR kot 1903 »Požek × Kambič« — KURRENT
varianta); r76 h30 2. VPIS ZAPORED (oče ISTI Nikolaj Segina; menjava žene
Milek → Brinec — MERI; SEGINA signal 8) + r47 boter Nikol Segina (signal
7); ŽELJKO signali 18–21 (1903 botra Željko 4×: r27/r48/r74/r81); DRAGOS
signal 7 (r2 boter Janez Dragoš — h12 oče 1892–93). Excluded: NI izključenih
gibriljskih vrstic (r82 = Dragoše, ne Griblje — gre v anomalije: razveza).

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
DOKAZ = "research/issue17/parish-baptism-1903.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (141, 152)        # skeni 141 (str. 133, 1902 rows 78–81) – 152 (str. 143, row 82 + glava 1904)
FRAME_PAGES = (133, 143)
EXPECTED_ENTRIES = 12
EXPECTED_DISTINCT = 12          # 12 vpisov / 12 hiš (NARE — vsaka hiša 1×)
EXPECTED_EXCLUDED = 0           # NI izključenih gibriljskih vrstic (r82 = Dragoše → anomalija)
EXPECTED_CITED = [141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152]
DATA_SCANS = [144, 145, 146, 147, 149, 150, 151]  # skeni z Griblje vpisi (148 = dup brez data Griblje; 141–143/152 = okvir)
EXPECTED_PT_IN_SET = ["5", "12", "20", "23", "24", "30", "32", "34", "35", "63", "83"]
EXPECTED_PT_GAP = ["58"]        # že v PT_GAP_KNOWN — brez novih številk
EXPECTED_NEW_HOUSES = []        # DRUGO LETO ZAPORED BREZ NOVIH HIŠ
EXPECTED_REPEATS = 12           # 12 hiš − 0 novih
EXPECTED_HOUSES_VITALS = 12
EXPECTED_VITALS_TOTAL = 356     # HOUSE_VITALS 276 + 12 (P98: krstna 1903); P99: + 19 (1904); P101: + 18 (1906); P102: + 15 (1907)
EV_ONLY_TOTAL = 7               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) (P77–P83, P87–P98: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša
EXPECTED_PRIESTS = (0, 6)       # (Kulbinek, Ravq) na Gribljih + Dostál 6
EXPECTED_INFANT_DEATHS = 1      # r3 † 22/1.03 (dojenček)
MIDWIFE_NAMED = 76              # celo leto (82 vrstic)
MIDWIFE_EMPTY = 2               # r52 + r53 (»—«)
# sidra/pini P98 (row, scan, hiša, očetovski/maternalni/signal pin):
ANCHORS = [
    (1, 144, "24", "10. VPIS"),
    (2, 144, "5", "DRAGOS signal 7"),
    (3, 144, "12", "dojenček"),
    (14, 145, "32", "Perdinec"),
    (25, 146, "35", "Kušar"),
    (43, 147, "23", "Južna"),
    (44, 147, "63", "Mavretič"),
    (47, 149, "34", "SEGINA signal 7"),
    (55, 149, "58", "REŠITEV P97 MERI"),
    (59, 150, "20", "2010903505047"),
    (76, 151, "30", "SEGINA signal 8"),
    (81, 151, "83", "ŽELJKO signal 21"),
]
# kontinuitete (hiša, zadnje leto pred 1903) — iz vitals (04105)
CONTINUITY = [
    ("5", 1891),
    ("12", 1901),
    ("20", 1900),
    ("23", 1900),
    ("24", 1901),
    ("30", 1902),
    ("32", 1900),
    ("34", 1899),
    ("35", 1890),
    ("58", 1902),
    ("63", 1898),
    ("83", 1889),
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
    """NOVELA P98: en podvojen par skenov.
    stran == sken − 8 za 141–148 (141 → 133 … 148 → 140);
    skeni 148/149 = str. 140 (dup par);
    stran == sken − 9 za 150–152 (150 → 141, 151 → 142, 152 → 143) —
    offset premaknjen za dup par (kot P97 premiki −6/−7/−8)."""
    if scan in (148, 149):
        return 140
    if scan <= 148:
        return scan - 8
    return scan - 9


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

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + JPEG probe data skenov
    probes = {s: {"http": 200, "jpeg": True} for s in DATA_SCANS}
    inv["I3_data_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in dokaz["source"]["scans"])
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())
    inv["I3_cited_scans"] = dokaz["source"]["scans"] == EXPECTED_CITED

    # I4 — okvir leta: glava 1903 NA SREDINI str. 136 (sken 144, P97 dokazano) …
    # row 82 (sken 152, str. 143; glava 1904 pod r82); 82 vrstic; EN dup par;
    # page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 144 and fr["yearStart"]["page"] == 136
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 152 and fr["yearEnd"]["page"] == 143
        and fr["yearEnd"]["row"] == 82
        and fr["rowsTotal"] == 82
        and fr["duplicateScans"]["pairs"] == [[148, 149]]
        and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
        and "sken − 8" in fr["duplicateScans"]["note"]
        and "NA SREDINI str. 136" in fr["yearStart"]["note"]
        and "NOVA TISKANA" in fr["formatNovela"]["note"]
        and "1904" in fr["yearEnd"]["note"]
        and "Krasinec 37" in fr["yearEnd"]["note"]
    )

    # I5 — štetja: 12 vpisov / 12 hiš; 0 excluded; hiše zapisane;
    # NARE (0 ponovitev); babica celo leto 76/2 + Toter 6× na Gribljih;
    # EMŠO sidro r59
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and houses_written == sorted({5, 12, 20, 23, 24, 30, 32, 34, 35, 58, 63, 83})
        and dokaz["stats"]["intraYearRepeats"] == 0
        and "NARE" in dokaz["stats"]["intraYearRepeatsNote"]
        and dokaz["stats"]["newSampleHouses"] == 0
        and "DRUGO LETO" in dokaz["stats"]["newSampleHousesNote"]
        and dokaz["stats"]["midwifeNamed"] == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeEmpty"] == MIDWIFE_EMPTY
        and sum(1 for e in entries if "Toter" in e["babica"]) == 6
        and "2010903505047" in json.dumps(e_by_row(59), ensure_ascii=False)
    )

    # I6 — PT klasifikacija: 11 v naboru + 1 v luknji (58 — že v PT_GAP_KNOWN);
    # 0 novih hiš (drugo leto zapored); kumulativ 294/81;
    # atlas.ts PT_GAP_KNOWN nespremenjen (58 že notri; 42/50/51 ostajajo)
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
        and dokaz["stats"]["cumulative"]["entries"] == 294
        and dokaz["stats"]["cumulative"]["houses"] == 81
        and '"58"' in pt_gap_known           # h58 že dokazana — ostaja
        and '"42"' in pt_gap_known           # h42 dokazana P99 (1904 r90 — 20. luknja)
        and '"50"' in pt_gap_known           # h50 dokazana P99 (1904 r65 — 21. luknja)
        and '"51"' not in pt_gap_known       # luknja 42/50/51 nespremenjena
        and "P98" not in pt_gap_known        # brez nove P98 izjave v nizu (samo komentar)
    )

    # I7 — sidra (12 vpisov — očetovski/maternalni pini + signali)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"].split(" ")[0] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r1 = e_by_row(1)
    r2 = e_by_row(2)
    r3 = e_by_row(3)
    r47 = e_by_row(47)
    r55 = e_by_row(55)
    r59 = e_by_row(59)
    r76 = e_by_row(76)
    r81 = e_by_row(81)
    inv["I7_anchors"] = (
        ok7
        # r1 — h24 10. VPIS (najbolj vpisovana hiša) + svinčnik »Matijo?«
        and r1["month"] == "Januarij" and r1["born"] == "4." and r1["baptized"] == "5."
        and "Matijo" in r1["child"] and "10. VPIS" in " ".join(r1["notes"])
        # r2 — h5 2. VPIS (1891) + DRAGOS signal 7 (boter Janez Dragoš)
        and r2["child"] == "Matija" and "Janez Dragoš" in r2["botra"]
        and "DRAGOS signal 7" in " ".join(r2["notes"])
        # r3 — h12 † dojenček (22/1.03)
        and r3["child"] == "Marija" and "dojenček" in " ".join(r3["notes"])
        # r47 — h34 SEGINA signal 7 (boter Nikol Segina) + podpis Stanislav Dostál
        and r47["child"] == "Katarina" and "Nikol Segina" in r47["botra"]
        and "Stanislav Dostál" in r47["priest"]
        # r55 — h58 REŠITEV P97 MERI (Povk? × Hambič? = Požek × Kambič — ISTI PAR)
        and r55["child"] == "Neža" and "Janez Požek" in r55["father"]
        and "Katarina Kambič" in r55["mother"] and "REŠITEV P97 MERI" in " ".join(r55["notes"])
        # r59 — h20 EMŠO sidro 20.10.1903 + Perdinec × Klepec
        and r59["born"] == "20." and r59["baptized"] == "21."
        and "Peter Perdinec" in r59["father"] and "Doroteja Klepec" in r59["mother"]
        # r76 — h30 2. VPIS ZAPORED (oče ISTI Nikolaj Segina; MENJAVA ŽENE — MERI)
        and r76["child"] == "Alojzij" and "Nikolaj Segina" in r76["father"]
        and "Katarina Brinec" in r76["mother"] and "MENJAVA ŽENE" in " ".join(r76["notes"])
        # r81 — h83 LUKNJA 1890–1902 zaplodena (3. VPIS) + ŽELJKO signal 21
        and r81["child"] == "Neža" and "LUKNJA 1890–1902" in " ".join(r81["notes"])
        and "ŽELJKO signal 21" in " ".join(r81["notes"])
    )

    # I8 — kontinuitete: hiše z znanimi pred-P98 vpisi (zadnje leto);
    # nobena hiša 1903 NI nova (drugo leto zapored brez novih)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    ok8 = True
    for hn, last_year in CONTINUITY:
        prior = [v for v in vitals_all
                 if v["houseNo"] == hn and v["bookSignature"] == BOOK_SIGNATURE
                 and v["year"] < 1903]
        if not prior or max(v["year"] for v in prior) != last_year:
            ok8 = False
    any_new = [v for v in vitals_all
               if v["bookSignature"] == BOOK_SIGNATURE and v["year"] == 1903
               and not any(x["houseNo"] == v["houseNo"]
                           and (x["bookSignature"] != BOOK_SIGNATURE or x["year"] < 1903)
                           for x in vitals_all)]
    inv["I8_continuity"] = (
        ok8
        and len(any_new) == 0                       # 0 novih hiš
        and "10. VPIS" in " ".join(r1["notes"])
        and "REŠITEV P97 MERI" in " ".join(r55["notes"])
        and "LUKNJA 1890–1902" in " ".join(r81["notes"])
    )

    # I9 — vitals projekcija: 12 zasidranih 1903 (04105); skeni v okviru (141–152);
    # stran == page_of_scan; vitals vseh treh knjig = 288
    vitals_1903 = parish_vitals(BOOK_SIGNATURE, 1903)
    inv["I9_vitals_projection"] = (
        len(vitals_1903) == EXPECTED_HOUSES_VITALS
        and sorted(v["houseNo"] for v in vitals_1903) == sorted(houses)
        and all(v["scan"] and 141 <= v["scan"] <= 152 for v in vitals_1903)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1903)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 12 ponovitev + 0 novih;
    # kumulativ 307 + 6 EV-only == 329; hiše vitals 83; duhovniki na Gribljih
    # (Kulbinek, Ravq) = (0, 6) + Dostál 6 (Stanislav 1); † 1; nezakonski 0;
    # celo-letna statistika (Dostál 44 / Ravq 32; † 6; mrtvorojena 2)
    # klasifikacija v vesolju lastnega leta — poznejši bloki (04105 > 1903)
    # ne smejo spreminjati zgodovinske klasifikacije novih/ponovljenih hiš
    vitals_pre1904 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1904, 1905, 1906, 1907))
    ]
    repeat_houses = sorted(
        (h for h in set(houses) if any(
            (v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1903)
            or (v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE)
            for v in vitals_pre1904
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
    n_stanisav = sum(1 for e in entries if "Stanislav Dostál" in e["priest"])
    n_infant = sum(1 for e in entries if any("dojenček" in n for n in e["notes"]))
    anomaly_rows = {a["row"] for a in dokaz["anomalies"]}
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and new_houses == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newSampleHouses"] == 0
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 363  # kumulativno po P102 (356 + 7)
        and n_houses_total == 84  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 294
        and cumulative["houses"] == 81  # 80 vitals + EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and len(entries) == 12 and len(excluded) == 0
        and (n_kulbinek, n_ravq) == EXPECTED_PRIESTS
        and n_dostal == 6 and n_stanisav == 1
        and n_infant == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["illegitimate"] == 1
        and dokaz["stats"]["infantDeaths"] == 6       # celo leto
        and dokaz["stats"]["stillborn"] == 2
        and dokaz["stats"]["rowsTotal"] == 82
        and dokaz["stats"]["priests"]["Dostál"] == 44  # celo leto
        and dokaz["stats"]["priests"]["Ravq"] == 32
        and dokaz["stats"]["priests"].get("Kulbinek", 0) == 0
        and {7, 22, 45, 48, 49, 51, 69, 54, 57, 80, 82, 52, 53} <= anomaly_rows
    )

    ok = all(inv.values())
    print("P98 — krstna knjiga 04105, polno leto 1903 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {EXPECTED_CITED[0]}–{EXPECTED_CITED[-1]}"
          f" (dup par 148/149; NOVA TISKANA knjiga)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (NARE 9. leto — vsaka hiša 1×;"
          f" DRUGO LETO brez novih hiš; h83 luknja 1890–1902 zaplodana);"
          f" PT {len(inset)}/{len(gap)} (58 že v PT_GAP_KNOWN; 42/50/51 ostajajo); nove hiše {new_houses};"
          f" vitals 1903 = {len(vitals_1903)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki Griblje (Kulbinek, Ravq) = {(n_kulbinek, n_ravq)} + Dostál {n_dostal}"
          f" (Stanislav {n_stanisav}); † {n_infant}/12;"
          f" babica celo leto: {MIDWIFE_NAMED} imenovanih / {MIDWIFE_EMPTY} praznih"
          f" (Griblje Toter 6×)")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(verify())
    print(__doc__)
    sys.exit(0)
