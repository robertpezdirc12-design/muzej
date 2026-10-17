#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P93 — župnija Podzemelj: krstna knjiga 04105, polno leto 1898 (issue #18).

Razširitev vzorca P79 (1886) → … → P91 (1896) → P92 (1897) na leto 1898:
okvir skeni 101–109 == strani 98–106 (glava »1898.« na str. 98 po 1897 row
85; leto 1898 ima 96 vrstic; prelom 1899 na str. 106 = sken 109 row 97 —
oznake ponastavljene, novela P83 potrjena 11. leto; 1899 row 1 = Griblje 12
Marija — novo leto se začne z Griblji). NOVELA P92 potrjena: stran == sken − 3
ZA CELO LETO (brez novih duplikatov; sken 105 = str. 102 brez Griblje vrstic,
ni citiran). 12 vpisov / 12 hiš — NARE (5. leto po P87/P89/P91/P92); 3 NOVE
hiše (18, 48, 89); h48 = NOVA LUKNJA ŠTEVILKA (18. dokazana v 41–60); h52
prvi TRDNI pin (1887 [~] po trojni korekciji). VRNITEV h63 — oče Nikolaj
Hrižan ISTI 6× (P92 »konec serije« popravljen). DVE MENJAVI + SELITEV: h69
Brinec → Straus; h33 Brinec → Dehlič (stari Brinec botra); Berkopne h40 →
h48; Brodarič h46 → h40 [~]. ŠOLSKA HIŠA h90: tretji učitelj (Kopitar →
Vetročnik × Schmelzer; botr učitelj Vrhovec). Duhovniki: Rauq 8× + Šturm 3×
+ 1 neberljiv; Klun (11× 1897) izgine. NOVELA babica 4. leto (12/12 PRAZNO).
KURRENT FORENZIKA: r5 »Griblje 39?« → jasno GRIŠINIČE 33 (izključena); r76
»Griblje?« → jasno ŠRIGLJE? (izključena); r72 »40?« → jasno 48 (6x — dvojna
zanka = 8); r63 »56?« → jasno 36 (5x); r22 69 + r30 89 (Kurrent 9 z repom);
r20 LEVI DEL UNIČEN (desni: Jurij Straus × Marija Jakofin — neštet).

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
DOKAZ = "research/issue17/parish-baptism-1898.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
DOKAZ_P87 = "research/issue17/parish-baptism-1892.json"
DOKAZ_P91 = "research/issue17/parish-baptism-1896.json"
DOKAZ_P92 = "research/issue17/parish-baptism-1897.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (101, 109)        # skeni 101–109 == strani 98–106 (okvir leta 1898)
FRAME_PAGES = (98, 106)
UNCITED_SCAN = 105              # sken 105 = str. 102 — 0 Griblje vrstic, ni citiran
BREAK_1899 = {"scan": 109, "page": 106, "row": 97}
EXPECTED_ENTRIES = 12
EXPECTED_DISTINCT = 12          # 12 vpisov / 12 hiš (NARE)
EXPECTED_EXCLUDED = 3           # r5 Grišiniče + r20 uničen + r76 Šriglje
EXPECTED_CITED = [102, 103, 104, 106, 107, 108, 109]  # 101 (r5 izključena) + 105 brez Griblje — ni citirana
EXPECTED_PT_IN_SET = ["18", "32", "33", "36", "40", "63", "69", "89", "90"]  # 18/89 = hiše 1825 v PT verigi
EXPECTED_PT_GAP = ["48", "52", "53"]  # luknja 41–60 (52/53 priori + 48 NOVA)
PT_GAP_NEW = ["48"]             # h48 = NOVA luknja številka (18. dokazana)
EXPECTED_NEW_HOUSES = ["18", "48", "89"]
EXPECTED_REPEATS = 9            # 12 hiš − 3 nove
EXPECTED_HOUSES_VITALS = 12
EXPECTED_VITALS_TOTAL = 276     # HOUSE_VITALS 211 + 12 (P93: krstna 1898); P94: + 15 (1899); P95: + 16 (1900)
EV_ONLY_TOTAL = 6               # P84: 2 + P85: 3 + P86: 1 (P77–P83, P87–P93: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša (None × 4)
EXPECTED_PRIESTS = (8, 3)       # (Rauq, Šturm) + 1 neberljiv (r42); Klun izgine
EXPECTED_INFANT_DEATHS = 1      # r78 † 6/6.1900 (r37 [~] možna — neštet)
# sidra/pini P93 (row, scan, hiša, očetovski pin):
ANCHORS = [
    (14, 102, "40", "Brodarič"),
    (22, 103, "69", "Straus"),
    (30, 103, "89", "Željko"),
    (37, 104, "18", "Šimec"),
    (42, 104, "32", "Urk"),
    (63, 106, "36", "Hrigar"),
    (71, 107, "33", "Dehlič"),
    (72, 107, "48", "Berkopne"),
    (78, 107, "63", "Hrižan"),
    (79, 107, "52", "Podrinc"),
    (89, 108, "53", "Podrinc"),
    (96, 109, "90", "Vetročnik"),
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
    """NOVELA P92 potrjena: od skena 98 stran == sken − 3 (artefakt podvojenega
    skena 97) — velja za VSE citirane skene 1898 (101–109), brez novih
    duplikatov."""
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

    # I3 — citirani skeni ⊆ okvir 101–109 + JPEG probe; sken 105 NI citiran
    # (0 Griblje vrstic — pregledan)
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == EXPECTED_CITED and UNCITED_SCAN not in cited
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1898; stran == sken − 3 (novela P92 za celo leto);
    # brez duplikatov; prelom 1899 na str. 106 (sken 109) row 97 → restart 1;
    # rowsTotal 96; 1899 row 1 = Griblje 12
    rows = [e["row"] for e in entries]
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1898 for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and all(FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and fr["yearStart"]["scan"] == 101 and fr["yearStart"]["page"] == 98 and fr["yearStart"]["row"] == 86
        and fr["yearEnd"]["scan"] == 109 and fr["yearEnd"]["page"] == 106 and fr["yearEnd"]["row"] == 96
        and fr["rowsTotal"] == 96
        and dokaz["source"]["duplicateScan"] is None
        and fr["nextYearBreak"]["scan"] == BREAK_1899["scan"]
        and fr["nextYearBreak"]["page"] == BREAK_1899["page"]
        and fr["nextYearBreak"]["row"] == BREAK_1899["row"]
        and fr["nextYearBreak"]["restartRow"] == 1
        and fr["nextYearBreak"]["year"] == 1899
        and "sken − 3" in fr["pageOfScan"]
        and "novela P83 potrjena 11. leto" in fr["nextYearBreak"]["note"]
        and "Griblje 12" in fr["nextYearBreak"]["note"]
    )

    # I5 — števec: 12 vpisov / 12 hiš; 0 neberljivih; NOVELA babica 4. leto:
    # vseh 12 PRAZNO; 3 izključeni (Grišiniče + uničen + Šriglje)
    houses = [e["houseNo"] for e in entries]
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and all(e["babica"] == "—" for e in entries)  # NOVELA babica 4. leto
        and len(excluded) == EXPECTED_EXCLUDED
        and excluded[0]["village"].startswith("Grišiniče")
        and excluded[1]["village"].startswith("(levi del uničen)")
        and excluded[2]["village"].startswith("Šriglje")
        and excluded[1]["houseNo"] is None
        and "Jurij Straus" in excluded[1]["reason"]
    )

    # I6 — PT klasifikacija: 11 v naboru + 1 v luknji; NOVA LUKNJA ŠTEVILKA
    # 48 (18. dokazana); 3 NOVE hiše (18, 48, 89); kumulativ 229/77
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newGapCount"] == 18
        and dokaz["stats"]["cumulative"]["entries"] == 229
        and dokaz["stats"]["cumulative"]["houses"] == 77
        # atlas.ts PT_GAP_KNOWN mora vsebovati 48 (runtime projekcija)
        and '"48"' in re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", open(ATLAS_TS, encoding="utf-8").read()).group(0)
    )

    # I7 — sidra (12 vpisov — očetovski pini + oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    # posebne oznake:
    h69 = e_by_row(22)
    h89 = e_by_row(30)
    h18 = e_by_row(37)
    h48 = e_by_row(72)
    h63 = e_by_row(78)
    h52 = e_by_row(79)
    h53 = e_by_row(89)
    h90 = e_by_row(96)
    h33 = e_by_row(71)
    inv["I7_anchors"] = (
        ok7
        and "MENJAVA" in json.dumps(h69["notes"], ensure_ascii=False)
        and "Brinec" in json.dumps(h69["notes"], ensure_ascii=False)
        and "NOVA ŠTEVILKA" in json.dumps(h89["notes"], ensure_ascii=False)
        and "NOVA ŠTEVILKA" in json.dumps(h18["notes"], ensure_ascii=False)
        and "NOVA ŠTEVILKA" in json.dumps(h48["notes"], ensure_ascii=False)
        and "SELITEV" in json.dumps(h48["notes"], ensure_ascii=False)
        and "Klobučar" in h48["mother"]
        and "6×" in json.dumps(h63["notes"], ensure_ascii=False)
        and "VRNITEV" in json.dumps(h63["notes"], ensure_ascii=False)
        and "1900" in json.dumps(h63["notes"], ensure_ascii=False)
        and "TRDNI PIN" in json.dumps(h52["notes"], ensure_ascii=False)
        and "ISTA ZVEZA" in json.dumps(h53["notes"], ensure_ascii=False)
        and "Kure" in h53["botra"]
        and "UČITELJ" in h90["father"]
        and "Schmelzer" in h90["mother"]
        and "Brinec" in h33["botra"]  # stari h33 oče zdaj botra
    )

    # I8 — čez-letne kontinuitete prek dokazov:
    # h63 (P87 + P91 Nikolaj Hrižan → P93 VRNITEV — oče ISTI 6×)
    # h69 (P84/P85 Brinec → P93 MENJAVA Straus)
    # h33 (P84 Brinec → P93 MENJAVA Dehlič; stari Brinec botra)
    # h53 (P86 + P91 Pendirec/Pozdirec × Hrižan → P93 4. VPIS ISTA ZVEZA)
    # h36 (P89 + P91 Križan × Straucelj → P93 3. VPIS ISTA ZVEZA)
    # h32 (P87 Urh → P93 Urk varianta)
    # h40 (P92 Berkovec → P93 MENJAVA Brodarič)
    # h52 (P82 nezakonski → P93 prvi TRDNI pin)
    # h90 (P85 Kopitar učitelj → P93 NOVI učitelj Vetročnik)
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p84 = json.load(open(DOKAZ_P84, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p91 = json.load(open(DOKAZ_P91, encoding="utf-8"))
    p92 = json.load(open(DOKAZ_P92, encoding="utf-8"))

    def hs(d, h):
        return [e for e in d["entries"] if e.get("houseNo") == h]

    p91_h63 = hs(p91, "63")
    p87_h63 = hs(p87, "63")
    p84_h69 = hs(p84, "69")
    p84_h33 = hs(p84, "33")
    p86_h53 = hs(p86, "53")
    p91_h53 = hs(p91, "53")
    p91_h36 = hs(p91, "36")
    p87_h32 = hs(p87, "32")
    p92_h40 = hs(p92, "40")
    p82_h52 = hs(p82, "52")
    p85_h90 = hs(p85, "90")

    def blob(d, h):
        return json.dumps(hs(d, h), ensure_ascii=False)

    inv["I8_continuity"] = (
        len(p91_h63) >= 1 and "Hrižan" in blob(p91, "63")
        and len(p87_h63) >= 1
        # popravki forenzike v dokazu:
        and "GRIŠINIČE" in json.dumps(excluded[0], ensure_ascii=False).upper()
        and "ŠRIGLJE" in json.dumps(excluded[2], ensure_ascii=False).upper()
        and "UNIČEN" in json.dumps(excluded[1], ensure_ascii=False).upper()
        # h72 hišna št. 48 = 6x forenzika (dvojna zanka = 8, ne 0)
        and "jasno 48 (ne 40" in json.dumps(h48["notes"], ensure_ascii=False)
        # h63 vrnitev: oče isti 6×
        and "Nikolaj Hrižan" in h63["father"]
    )

    # I9 — vitals projekcija: 12 zasidranih 1898 (04105); vsi skeni v okviru;
    # stran == sken − 3; vitals skupaj 223
    vitals_1898 = parish_vitals(BOOK_SIGNATURE, 1898)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    inv["I9_vitals_projection"] = (
        len(vitals_1898) == EXPECTED_HOUSES_VITALS
        and sorted(v["houseNo"] for v in vitals_1898) == sorted(houses)
        and all(v["scan"] and 101 <= v["scan"] <= 109 for v in vitals_1898)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1898)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 9 ponovitev + 3 nove
    # (18/48/89); kumulativ 223 + 6 EV-only == 229; hiše vitals 76; duhovniki
    # (Rauq, Šturm) = (8, 3) + 1 neberljiv; dojenčijska umrljivost 1
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1898
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_all
    )]
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
    n_rauq = sum(1 for e in entries if "Rauq" in e["priest"])
    n_sturm = sum(1 for e in entries if "Šturm" in e["priest"])
    n_infant = dokaz["stats"]["infantDeaths"]
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and new_houses == EXPECTED_NEW_HOUSES == dokaz["stats"]["newSampleHouses"]
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 282  # kumulativno po P95 (254 + 6)
        and n_houses_total == 80  # P94: 78; P95: + 1 (67)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 229
        and cumulative["houses"] == 77  # 76 vitals + 1 EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and len(entries) == 12 and len(excluded) == 3
        and (n_rauq, n_sturm) == EXPECTED_PRIESTS
        and n_infant == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["midwifeEmpty"] == 12
        and dokaz["stats"]["illegitimate"] == 0
    )

    ok = all(inv.values())
    print("P93 — krstna knjiga 04105, polno leto 1898 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited} (sken 105 = str. 102 brez Griblje — ni citiran)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (NARE);"
          f" PT {len(inset)}/{len(gap)} (48 NOVA luknja); nove hiše {sorted(new_houses)};"
          f" vitals 1898 = {len(vitals_1898)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki (Rauq, Šturm) = {(n_rauq, n_sturm)}; † {n_infant}/12")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
