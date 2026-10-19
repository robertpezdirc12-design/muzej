#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P92 — župnija Podzemelj: krstna knjiga 04105, polno leto 1897 (issue #18).

Razširitev vzorca P79 (1886) → … → P90 (1895) → P91 (1896) na leto 1897:
okvir skeni 93–101 == strani 91–98 (glava »Leto 1897« na str. 91 po 1896 row
94; leto 1897 ima 85 vrstic; prelom 1898 na str. 98 = sken 101 po row 85 —
oznake ponastavljene, novela P83 potrjena 10. leto).
NOVELA P92 — PODVOJEN SKEN 97 (duplikat s96 = str. 94; 2. znani duplikat po
skenu 73): NOVELA P89 (stran == sken − 2) velja samo do skena 96; od skena 98
stran == sken − 3 — premik offseta je artefakt podvojenega skena, NE nove
številčenja. 19 vpisov / 18 hiš — NARE (4. leto po P87/P89/P91); h31 2 vpisa
v enem letu; 3 NOVE hiše (10, 40, 43); h43 = NOVA LUKNJA ŠTEVILKA (17.
dokazana v 41–60); h54 2. dokaz + h60 4. dokaz + h45/h46 luknji. PRVI
NEZAKONSKI vpis od P90 (r31 sama mati Pozdirec). NOVELA babica 3. leto (19/19
PRAZNO). Dojenčijska umrljivost 7/19 — najvišje doslej. Duhovniki: Šuvar
izgine; Klun 11× + Rauq 8× (mešano leto). KURRENT FORENZIKA 6 popravkov
(h23/h24 dve hiši, Grisice≠Griblje, Otok≠Griblje, h16≠10, row 59/62/64, h45
mati Spudič — POPRAVEK P91 prebira »Doroteja?«).

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
DOKAZ = "research/issue17/parish-baptism-1897.json"
DOKAZ_P77 = "research/issue17/parish-sample-transcription.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
DOKAZ_P87 = "research/issue17/parish-baptism-1892.json"
DOKAZ_P88 = "research/issue17/parish-baptism-1893.json"
DOKAZ_P89 = "research/issue17/parish-baptism-1894.json"
DOKAZ_P90 = "research/issue17/parish-baptism-1895.json"
DOKAZ_P91 = "research/issue17/parish-baptism-1896.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (93, 101)         # skeni 93–101 == strani 91–98 (okvir leta 1897)
FRAME_PAGES = (91, 98)
DUP_SCAN = 97                   # sken 97 = podvojen (duplikat s96) — NI citiran
BREAK_1898 = {"scan": 101, "page": 98, "row": 86}
EXPECTED_ENTRIES = 19
EXPECTED_DISTINCT = 18          # 19 vpisov / 18 hiš (h31 ×2)
EXPECTED_INTRA_REPEATS = 1      # h31 (r51 + r64)
EXPECTED_CITED = [93, 94, 95, 96, 98, 99, 100, 101]  # sken 97 podvojen ni citiran
EXPECTED_PT_IN_SET = ["2", "10", "12", "16", "20", "23", "24", "31", "32", "37", "40", "61", "65"]
EXPECTED_PT_GAP = ["43", "45", "46", "54", "60"]
PT_GAP_NEW = ["43"]             # h43 = NOVA luknja številka (17. dokazana)
EXPECTED_NEW_HOUSES = ["10", "40", "43"]
EXPECTED_REPEATS = 15           # 18 hiš − 3 nove (z notranjo ponovitvijo h31)
EXPECTED_HOUSES_VITALS = 19
EXPECTED_VITALS_TOTAL = 467     # HOUSE_VITALS 211 + 12 (P93: krstna 1898); h61 sidro = P79-era placeholder ZDRUŽEN, ne dupliran; P94: + 15 (1899); P95: + 16 (1900); P98: + 12 (1903); P99: + 19 (1904); P101: + 18 (1906); P102: + 15 (1907); P103: + 18 (1908); P104: + 18 (1909); P105: + 20 (1910)
EV_ONLY_TOTAL = 8               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) + P103: r84 (1) (P77–P83, P87–P92: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša (None × 4)
EXPECTED_PRIESTS = (11, 8)      # (Klun, Rauq) — mešano leto; Šuvar izgine
EXPECTED_INFANT_DEATHS = 7
# sidra/pini P92 (row, scan, očetovski pin, oznaka):
ANCHORS = [
    (8, 93, "12", "Dragar", "h12"),
    (12, 94, "32", "Perdune", "h32"),
    (15, 94, "10", "Brinec", "h10 NOVA"),
    (21, 94, "24", "Brinec", "h24 (ne 23!)"),
    (25, 95, "37", "Pendirec", "h37"),
    (26, 95, "54", "Brinec", "h54 LUKNJA"),
    (28, 95, "60", "Željko", "h60 LUKNJA"),
    (29, 95, "2", "Vhebec", "h2"),
    (31, 95, "43", "Pozdirec", "h43 NOVA LUKNJA + SAMA MATI"),
    (38, 96, "23", "Brinec", "h23 (ne 24!)"),
    (41, 96, "46", "Brodarič", "h46 4. VPIS"),
    (51, 98, "31", "Sapič", "h31 vpis 1"),
    (52, 98, "16", "Jaklič", "h16 (ne 10!)"),
    (59, 99, "40", "Berkovec", "h40 NOVA"),
    (62, 99, "20", "Pendirec", "h20"),
    (64, 99, "31", "Straus", "h31 vpis 2"),
    (79, 100, "61", "Muc", "h61"),
    (80, 100, "65", "Mihek", "h65"),
    (84, 101, "45", "Straus", "h45 2. VPIS ISTA ZVEZA"),
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
        except Exception:  # noqa: BLE001
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
    """NOVELA P89 (sken − 2) velja do skena 96; sken 97 = podvojen; od skena
    98 stran == sken − 3 (artefakt duplikata — NOVELA P92)."""
    if scan <= 96:
        return scan - 2
    return scan - 3


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = [e for e in dokaz["entries"] if e["village"] == "Griblje"]
    excluded = [e for e in dokaz["entries"] if e["village"] != "Griblje"]
    inv = {}

    # I1 — knjiga dostopna + inventar 326
    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    # I3 — citirani skeni ⊆ okvir 93–101 + JPEG probe; sken 97 NI citiran
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == EXPECTED_CITED and DUP_SCAN not in cited
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1897; stran: sken − 2 (≤96) / sken − 3 (≥98);
    # sken 97 podvojen; prelom 1898 na str. 98 (sken 101) row 86; rowsTotal 85
    rows = [e["row"] for e in entries]
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1897 for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and all(FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1] for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in excluded)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and fr["yearStart"]["scan"] == 93 and fr["yearStart"]["page"] == 91 and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 101 and fr["yearEnd"]["page"] == 98 and fr["yearEnd"]["row"] == 85
        and fr["rowsTotal"] == 85
        and fr["duplicateScan"]["scan"] == 97 and fr["duplicateScan"]["duplicateOf"] == 96
        and "NI citiran" in fr["duplicateScan"]["note"]
        and fr["nextYearBreak"]["scan"] == BREAK_1898["scan"]
        and fr["nextYearBreak"]["page"] == BREAK_1898["page"]
        and fr["nextYearBreak"]["row"] == BREAK_1898["row"]
        and "artefakt" in fr["pageOfScan"]
    )

    # I5 — števec: 19 vpisov / 18 hiš; h31 2 vpisa; 0 neberljivih;
    # NOVELA babica 3. leto: vseh 19 PRAZNO; 1 izključen (Grisice) z neg. oznako
    houses = [e["houseNo"] for e in entries]
    intra = dokaz["stats"]["intraYearRepeats"]
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and len(set(houses)) == EXPECTED_DISTINCT
        and len(intra) == EXPECTED_INTRA_REPEATS
        and intra[0]["houseNo"] == "31" and intra[0]["rows"] == [51, 64]
        and dokaz["stats"]["housesIllegible"] == 0
        and all(e["babica"] and "prazen" in e["babica"] for e in entries)  # NOVELA babica 3. leto
        and len(excluded) == 1 and excluded[0]["village"] == "Grisice"
        and any("IZKLJUČEN" in n for n in excluded[0]["notes"])
    )

    # I6 — PT klasifikacija: 13 v naboru + 5 v luknjah; NOVA LUKNJA ŠTEVILKA
    # 43 (17. dokazana); 3 NOVE hiše (10, 40, 43)
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["cumulative"]["entries"] == 217
        and dokaz["stats"]["cumulative"]["houses"] == 74
        # atlas.ts PT_GAP_KNOWN mora vsebovati 43 (runtime projekcija)
        and '"43"' in re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", open(ATLAS_TS, encoding="utf-8").read()).group(0)
    )

    # I7 — sidra (19 vpisov — očetovski pini + kontinuitetne oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    ok7 = True
    for row, scan, hn, pin, label in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    # posebne oznake:
    h43 = e_by_row(31)
    h45 = e_by_row(84)
    h46 = e_by_row(41)
    h31a, h31b = e_by_row(51), e_by_row(64)
    inv["I7_anchors"] = (
        ok7
        and "NOVA LUKNJA ŠTEVILKA" in json.dumps(h43["notes"], ensure_ascii=False)
        and "SAMA MATI" in json.dumps(h43["mother"], ensure_ascii=False)
        and "OČE PRAZEN" in h43["father"]
        and "2. VPIS ISTA ZVEZA" in json.dumps(h45["notes"], ensure_ascii=False)
        and h45["mother"].startswith("Barbara Spudič")
        and "3. varianta matere" in json.dumps(h46["mother"], ensure_ascii=False)
        and "Sapič" in h31a["father"] and "Straus" in h31b["father"]
        and "Željko" in e_by_row(79)["botra"] and "Kure" in e_by_row(79)["botra"]
    )

    # I8 — čez-letne kontinuitete prek dokazov:
    # h45 (P91 1896 Straus bajtar → P92 ISTA zveza 2. VPIS; POPRAVEK Spudič)
    # h46 (P88 + P90 + P91 Brodarič → P92 4. VPIS)
    # h31 (P89 Fapič? × Straus + P91 Pendirec? × Žugelj? → P92 2 vpisa)
    # h60 (P87 + P89 + P91 Željko? → P92 4. dokaz luknje)
    # h61 (P86 + P87 → P92 5. pin); h65 (P87 + P89 + P90 + P91 → P92 5. pin)
    # h2 (P83–P86 → P92 5. pin); h24 (P87 menjave → P92)
    # h23/h24 FORENZIKA: r21 = 24, r38 = 23 (5x izreza)
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p88 = json.load(open(DOKAZ_P88, encoding="utf-8"))
    p89 = json.load(open(DOKAZ_P89, encoding="utf-8"))
    p90 = json.load(open(DOKAZ_P90, encoding="utf-8"))
    p91 = json.load(open(DOKAZ_P91, encoding="utf-8"))

    def hs(d, h):
        return [e for e in d["entries"] if e.get("houseNo") == h]

    p91_h45 = hs(p91, "45")
    p88_h46 = hs(p88, "46")
    p90_h46 = hs(p90, "46")
    p91_h46 = hs(p91, "46")
    p89_h31 = hs(p89, "31")
    p91_h31 = hs(p91, "31")
    p82_h2 = hs(p82, "2")
    p87_h61 = hs(p87, "61")
    p87_h24 = hs(p87, "24")
    inv["I8_continuity"] = (
        len(p91_h45) == 1 and "Straus" in p91_h45[0]["father"]
        and "Doroteja" in p91_h45[0]["mother"]  # P91 prebir — P92 ga popravlja
        and len(p88_h46) >= 1 and len(p90_h46) >= 1 and len(p91_h46) >= 1
        and all("Brodarič" in e["father"] for e in p88_h46 + p90_h46 + p91_h46)
        and len(p89_h31) >= 1 and "Straus" in p89_h31[0].get("mother", "")
        and len(p91_h31) >= 1
        and len(p82_h2) >= 1
        and len(p87_h61) >= 1
        and len(p87_h24) >= 1
        # popravki forenzike v dokazu:
        and "dve različni Brinec hiši" in json.dumps([e_by_row(21)["notes"], e_by_row(38)["notes"]], ensure_ascii=False)
    )

    # I9 — vitals projekcija: 19 zasidranih 1897 (04105); vsi skeni v okviru;
    # stran == page_of_scan; vitals skupaj 212; hiše vitals 73
    vitals_1897 = parish_vitals(BOOK_SIGNATURE, 1897)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    inv["I9_vitals_projection"] = (
        len(vitals_1897) == EXPECTED_HOUSES_VITALS
        and sorted((int(v["houseNo"]) for v in vitals_1897))
        == sorted(int(h) for h in houses)  # multiset (h31 ×2)
        and all(v["scan"] and 93 <= v["scan"] <= 101 for v in vitals_1897)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1897)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 15 ponovitev + 3 nove
    # (10/40/43); kumulativ 212 + 6 EV-only == 218; hiše vitals 73; duhovniki
    # (Klun, Rauq) = (11, 8); dojenčijska umrljivost 7
    # klasifikacija v P92 vesolju — poznejši bloki (1898) ne smejo spreminjati
    # zgodovinske klasifikacije leta 1897 (h40: 1898 MENJAVA — Brodarič)
    vitals_pre98 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913))
    ]
    repeat_houses = sorted(
        (h for h in set(houses) if any(
            (v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1897)
            or (v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE)
            for v in vitals_pre98
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
    n_klun = sum(1 for e in entries if "Klun" in e["priest"])
    n_rauq = sum(1 for e in entries if "Rauq" in e["priest"])
    n_infant = len(dokaz["stats"]["infantDeaths"])
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and dokaz["stats"].get("repeatHousesNote", EXPECTED_REPEATS) == EXPECTED_REPEATS
        and new_houses == EXPECTED_NEW_HOUSES == dokaz["stats"]["newSampleHouses"]
        and len(intra) == EXPECTED_INTRA_REPEATS
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 475  # kumulativno po P108 (467 + 8)
        and n_houses_total == 85  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4); P107: + 1 (h86)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 217
        and cumulative["houses"] == 74  # 73 vitals + 1 EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and len(dokaz["entries"]) == 20  # 19 Griblje + 1 izključen (Grisice)
        and (n_klun, n_rauq) == EXPECTED_PRIESTS
        and n_infant == EXPECTED_INFANT_DEATHS
    )

    ok = all(inv.values())
    print("P92 — krstna knjiga 04105, polno leto 1897 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited} (sken 97 = podvojen str. 94 — ni citiran)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (NARE; h31 ×2);"
          f" PT {len(inset)}/{len(gap)} (43 NOVA luknja); nove hiše {sorted(new_houses)};"
          f" vitals 1897 = {len(vitals_1897)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki (Klun, Rauq) = {(n_klun, n_rauq)}; † {n_infant}/19")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
