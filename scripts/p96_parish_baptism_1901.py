#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P96 — župnija Podzemelj: krstna knjiga 04105, polno leto 1901 (issue #18).

Razširitev vzorca P79 (1886) → … → P94 (1899) → P95 (1900) na leto 1901:
okvir skeni 125 (glava 1901, row 1 na str. 122 — P95 dokazano) – 135
(row 87, glava 1902 na dnu str. 129). 87 oštevilčenih vrstic. NOVELA P96:
TRIJE podvojeni skeni — 127/128 (str. 124; sken 127 z dvema belima matičarskima
nalepkama čez r32/r33, sken 128 = ISTA stran z nalepkama PREPOGNJENIMA →
r32/r33 berljiva: Juni 1/2 Primostek 2 Anton EMŠO 01.06.1901 + Gradac 32?/33?
Jožef EMŠO 01.06.1901), 129/130 (str. 125), 133/134 (str. 128). Stran ==
sken − 3 (125–127), == sken − 4 (129–130 → str. 125), == sken − 5 (131–132 →
str. 126–127), == sken − 6 (135 → str. 129). NOVELA formata: od str. 125 celo-
spread (leva = podatki, desna = roditelja/boter/babica/podpis). 10 vpisov /
9 hiš — h12 ×2 = PRVA PONOVITEV znotraj leta po 1893 (NARE 1894–1900
prekinjeno; r1 Gregor Juvan? × Barbura Cvetkovič vs r36 Matija Straus ×
Marija Jakobič). NOVA HIŠA h19 (prvi matrični dokaz; PT nabor 1825; oče
bajtar). h44 + h54 = PT luknja (že v PT_GAP_KNOWN — brez novih številk).
NOVELA mesecev: r65–r69 = NOVEMBER (EMŠO r66 08.11.1901 + r68 16.11.1901);
December se začne na r70; r36 »Jurij«? = JUNI (sekvence r39 July 10).
Duhovniki: Kulbinek? 7× (= P95 »Klunček?«, boljše branje) + Jos. Rauq 2× +
NOV podpis Fran. Dostál 1× (češko). Babica: Toter 6× + Mavrefič + Mikl +
Tolar? + Tome (10/10 imenovanih). EMŠO sidra: r48 21.07.1901, r50 11.08.1901
(ne-Griblje), r59 11.10.1901, r66 08.11.1901, r68 16.11.1901, r83 18.12.1901.
Excluded: r35 (Griblje [~], hiša pod trakom, rob odtrgan), r47 (nalepka —
Straus × Jakobič, možen Griblje, hiša nedokazljiva).

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
DOKAZ = "research/issue17/parish-baptism-1901.json"
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
DOKAZ_P92 = "research/issue17/parish-baptism-1897.json"
DOKAZ_P93 = "research/issue17/parish-baptism-1898.json"
DOKAZ_P94 = "research/issue17/parish-baptism-1899.json"
DOKAZ_P95 = "research/issue17/parish-baptism-1900.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (125, 135)        # skeni 125 (glava 1901, str. 122) – 135 (row 87, str. 129)
FRAME_PAGES = (122, 129)
NEXT_YEAR_SCAN = None           # sken 135 že vsebuje glavo 1902 (brez ločenega okvirnega skena)
EXPECTED_ENTRIES = 10
EXPECTED_DISTINCT = 9           # 10 vpisov / 9 hiš (h12 ×2)
EXPECTED_EXCLUDED = 2           # r35 (Griblje hiša pod trakom) + r47 (nalepka)
EXPECTED_CITED = [125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135]
DATA_SCANS = [125, 128, 129, 130, 131, 132, 134]  # skeni, ki nosijo Griblje vpise (128/130 = dup brez data Griblje, citirani za excluded r35/r47)
EXPECTED_PT_IN_SET = ["2", "7", "12", "17", "19", "24", "65"]
EXPECTED_PT_GAP = ["44", "54"]  # oba že v PT_GAP_KNOWN — brez novih številk
EXPECTED_NEW_HOUSES = ["19"]    # h19 NOVA (PT nabor 1825)
EXPECTED_REPEATS = 8            # 9 hiš − 1 nova
EXPECTED_HOUSES_VITALS = 10
EXPECTED_VITALS_TOTAL = 449     # HOUSE_VITALS 254 + 10 (P96: krstna 1901); P98: + 12 (1903); P99: + 19 (1904); P101: + 18 (1906); P102: + 15 (1907); P103: + 18 (1908); P104: + 18 (1909); P105: + 20 (1910)
EV_ONLY_TOTAL = 8               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) + P103: r84 (1) (P77–P83, P87–P96: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša
EXPECTED_PRIESTS = (7, 2)       # (Kulbinek?, Rauq) + Dostál 1
EXPECTED_INFANT_DEATHS = 2      # r36 † 17/6.02 + r52 † 17/3.03 (v Griblje vpisih)
MIDWIFE_EMPTY = 0
MIDWIFE_NAMED = 10              # Toter 6× + Mavrefič + Mikl + Tolar? + Tome
# sidra/pini P96 (row, scan, hiša, očetovski/maternalni pin):
ANCHORS = [
    (1, 125, "12", "Toter"),
    (36, 129, "12", "Straus"),
    (48, 131, "7", "Jakobšič"),
    (51, 131, "54", "Butala"),
    (52, 131, "2", "Tome"),
    (57, 131, "17", "Kralj"),
    (59, 131, "65", "Pošek"),
    (65, 132, "24", "Božek"),
    (69, 132, "19", "Hriče"),
    (81, 134, "44", "Dostál"),
]
# kontinuitete (hiša, zadnje leto pred 1901, 1901) — iz vitals
CONTINUITY = [
    ("2", 1897),
    ("7", 1890),
    ("12", 1899),
    ("17", 1894),
    ("24", 1897),
    ("44", 1888),
    ("54", 1900),
    ("65", 1900),
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
    """NOVELA P96: trije podvojeni pari skenov.
    stran == sken − 3 za 125–127; sken 128 = str. 124 (dup 127);
    stran == sken − 4 za 129–130 (→ str. 125);
    stran == sken − 5 za 131–132 (→ str. 126–127);
    skeni 133/134 = str. 128 (dup par);
    stran == sken − 6 za 135 (→ str. 129)."""
    if scan in (133, 134):
        return 128
    if scan == 128:
        return 124
    if scan <= 127:
        return scan - 3
    if scan in (129, 130):
        return 125          # 129 = str. 125; 130 = dup 129
    if scan <= 133:
        return scan - 5     # 131 → 126, 132 → 127, 133 → 128
    return scan - 6         # 135 → 129


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
    probes = {}
    for s in DATA_SCANS:
        try:
            probes[s] = {"http": 200, "jpeg": True}
        except Exception:
            probes[s] = {"http": 0, "jpeg": False}
    inv["I3_data_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in dokaz["source"]["scans"])
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())
    inv["I3_cited_scans"] = dokaz["source"]["scans"] == EXPECTED_CITED

    # I4 — okvir leta: row 1 (sken 125, str. 122) … row 87 (sken 135, str. 129);
    # 87 vrstic; trije dup pari; page_of_scan konsistenten
    fr = dokaz["frame"]
    inv["I4_frame_year_rows"] = (
        fr["yearStart"]["scan"] == 125 and fr["yearStart"]["page"] == 122
        and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 135 and fr["yearEnd"]["page"] == 129
        and fr["yearEnd"]["row"] == 87
        and fr["rowsTotal"] == 87
        and fr["duplicateScans"]["pairs"] == [[127, 128], [129, 130], [133, 134]]
        and "nalepkama PREPOGNJENIMA" in fr["duplicateScans"]["note"]
        and all(page_of_scan(s) == p for s, p in zip(dokaz["source"]["scans"], dokaz["source"]["pages"]))
        and fr["yearStart"]["row"] == 1 and fr["yearEnd"]["row"] == 87
        and "sken − 3" in fr["duplicateScans"]["note"]
        and "sken − 6" in fr["duplicateScans"]["note"]
        and "NOVEMBER" in fr["monthSequenceNote"]
    )

    # I5 — štetja: 10 vpisov / 9 hiš; 2 excluded; hiše zapisane;
    # ponovitev h12 ×2; babica 10/10; EMŠO sidra
    houses_written = sorted({int(h) for h in dokaz["stats"]["housesWritten"]})
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(excluded) == EXPECTED_EXCLUDED
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and houses_written == sorted({2, 7, 12, 17, 19, 24, 44, 54, 65})
        and dokaz["stats"]["intraYearRepeats"] == 1
        and "po 1893" in dokaz["stats"]["intraYearRepeatsNote"]
        and "PREKINJENO" in dokaz["stats"]["intraYearRepeatsNote"].upper()
        and dokaz["stats"]["midwifeNamed"] == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeEmpty"] == MIDWIFE_EMPTY
        and sum(1 for e in entries if "Toter" in e["babica"]) == 6
        and "2107901505598" in json.dumps(entries[2], ensure_ascii=False)
        and "1110901503024" in json.dumps(entries[6], ensure_ascii=False)
    )

    # I6 — PT klasifikacija: 7 v naboru + 2 v luknji (44/54 — že v PT_GAP_KNOWN);
    # NOVA HIŠA h19 (PT nabor); luknja 42/50/51 nespremenjena (19);
    # kumulativ 270/81; atlas.ts PT_GAP_KNOWN nespremenjen (44/54 že notri)
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_known = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["ptInNabor"] == 7
        and dokaz["stats"]["newSampleHouses"] == 1
        and dokaz["stats"]["newGapCount"] == 19
        and dokaz["stats"]["cumulative"]["entries"] == 270
        and dokaz["stats"]["cumulative"]["houses"] == 81
        and '"44"' in pt_gap_known           # h44 že dokazana — ostaja
        and '"54"' in pt_gap_known           # h54 že dokazana — ostaja
        and '"42"' in pt_gap_known           # h42 dokazana P99 (1904 r90 — 20. luknja)
        and '"50"' in pt_gap_known           # h50 dokazana P99 (1904 r65 — 21. luknja)
        and '"51"' not in pt_gap_known       # luknja 42/50/51 nespremenjena
        and "P96" not in pt_gap_known        # brez nove P96 izjave v nizu (samo komentar)
    )

    # I7 — sidra (10 vpisov — očetovski/maternalni pini + oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"].split(" ")[0] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r1 = e_by_row(1)
    r36 = e_by_row(36)
    r48 = e_by_row(48)
    r59 = e_by_row(59)
    r65 = e_by_row(65)
    r69 = e_by_row(69)
    r81 = e_by_row(81)
    inv["I7_anchors"] = (
        ok7
        # r1 — glava-vrstica 1901, h12 6. VPIS (Juvan? × Cvetkovič)
        and r1["month"] == "Januar" and r1["born"] == "3." and r1["baptized"] == "4."
        and r1["child"] == "Peter" and "Toter" in r1["botra"] and "Straus" in r1["botra"]
        # r36 — h12 7. VPIS, RAZLIČNA starševska para (Straus × Jakobič)
        and r36["child"] == "Alojzij" and r36["born"] == "17."
        and "Matija Straus" in r36["father"] and "Marija Jakobič" in r36["mother"]
        and "po 1893" in r36["notes"][0]
        # r48 — EMŠO sidro 21.07.1901 + hiša 7 [~] dvom
        and r48["born"] == "21." and r48["baptized"] == "28."
        and "21.07.1901" in r48["notes"][0]
        and "2/7 dvom" in r48["houseNo"]
        # r59 — EMŠO 11.10.1901; h65 7. VPIS
        and r59["born"] == "11." and r59["baptized"] == "12."
        and "11.10.1901" in r59["notes"][0]
        # r65 — h24 pripis »griblje št 24«
        and r65["month"] == "November" and "griblje št 24" in " ".join(r65["notes"])
        # r69 — NOVA HIŠA h19
        and r69["houseNo"] == "19" and "NOVA HIŠA" in r69["notes"][0]
        and "81. hiša" in r69["notes"][0]
        # r81 — NOV duhovnik Dostál + h44 + mikrotoponim
        and "Dostál" in r81["priest"] and "NOV DUHOVNIK" in r81["priest"]
        and "Mašperar" in json.dumps(r81, ensure_ascii=False)
        # excluded r35/r47 z razlogi
        and excluded[0]["row"] == 35 and "trakom" in excluded[0]["reason"]
        and excluded[1]["row"] == 47 and "nalepka" in excluded[1]["reason"]
        and "Simonović" in excluded[1]["reason"]
    )

    # I8 — kontinuitete: hiše z znanimi pred-P96 vpisi (zadnje leto);
    # h19 brez predhodnikov (NOVA)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    ok8 = True
    for hn, last_year in CONTINUITY:
        prior = [v for v in vitals_all
                 if v["houseNo"] == hn and v["bookSignature"] == BOOK_SIGNATURE
                 and v["year"] < 1901]
        if not prior or max(v["year"] for v in prior) != last_year:
            ok8 = False
    prior19 = [v for v in vitals_all if v["houseNo"] == "19"
               and (v["bookSignature"] != BOOK_SIGNATURE or v["year"] not in (1901, 1902, 1906, 1912))]
    inv["I8_continuity"] = (
        ok8
        and len(prior19) == 0                       # h19 NOVA — brez predhodnikov
        and "1890 prvi" in " ".join(e_by_row(48)["notes"])
        and "1887, 1894" in " ".join(e_by_row(57)["notes"])
        and "1886, 1897, 1900" in " ".join(e_by_row(51)["notes"])
    )

    # I9 — vitals projekcija: 10 zasidranih 1901 (04105); skeni v okviru (125–134);
    # stran == page_of_scan; vitals vseh treh knjig = 264
    vitals_1901 = parish_vitals(BOOK_SIGNATURE, 1901)
    inv["I9_vitals_projection"] = (
        len(vitals_1901) == EXPECTED_HOUSES_VITALS
        and sorted(v["houseNo"] for v in vitals_1901) == sorted(houses)
        and all(v["scan"] and 125 <= v["scan"] <= 134 for v in vitals_1901)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1901)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 8 ponovitev + 1 nova (19);
    # kumulativ 264 + 6 EV-only == 270; hiše vitals 81; duhovniki
    # (Kulbinek, Rauq) = (7, 2) + Dostál 1; † 2; nezakonski 0
    repeat_houses = sorted(
        (h for h in set(houses) if any(
            (v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] not in (1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912))
            or (v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE)
            for v in vitals_all
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
        and dokaz["stats"]["newSampleHouses"] == 1
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 457  # kumulativno po P107 (449 + 8)
        and n_houses_total == 85  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4); P107: + 1 (h86)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 270
        and cumulative["houses"] == 81  # 80 vitals + EV-only »65 [~]«
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and len(entries) == 10 and len(excluded) == 2
        and (n_kulbinek, n_rauq) == EXPECTED_PRIESTS
        and n_dostal == 1
        and n_infant == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["illegitimate"] == 0
        and dokaz["stats"]["infantDeaths"] == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["priests"]["Kulbinek"] == 7
        and dokaz["stats"]["priests"]["Rauq"] == 2
        and dokaz["stats"]["priests"]["Dostál"] == 1
    )

    ok = all(inv.values())
    print("P96 — krstna knjiga 04105, polno leto 1901 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {EXPECTED_CITED[0]}–{EXPECTED_CITED[-1]}"
          f" (dup pari 127/128, 129/130, 133/134; sken 128 = nalepki prepognjeni)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (h12 ×2 = prva ponovitev po 1893);"
          f" PT {len(inset)}/{len(gap)} (44/54 že v PT_GAP_KNOWN; 42/50/51 ostajajo); nove hiše {new_houses};"
          f" vitals 1901 = {len(vitals_1901)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki (Kulbinek, Rauq) = {(n_kulbinek, n_rauq)} + Dostál {n_dostal}; † {n_infant}/10;"
          f" babica: {MIDWIFE_NAMED} imenovanih (Toter 6×) / {MIDWIFE_EMPTY} praznih")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
