#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P86 — župnija Podzemelj: krstna knjiga 04105, polno leto 1891 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85
(1890) na leto 1891: okvir skeni 49–56 == strani 48–55 (stran == sken − 1;
leto se začne na str. 48 row 1 po 1890 rows 78–86; glava »Leto 1892« na str.
55 row 1) — vsi vpisi z Griblji. LE OKVIR — prejšnja leta imajo svoje skripte
p82/p83/p84/p85. Sidra: h72 Straus (oče ISTI kot P83 1888, mati menjana),
h30 Milek (popolna kontinuiteta z P85 dvojčki — isti starši + ista botra),
h61 Požek (oče ISTA OSEBA kot P82 sidro 1887, mati menjana Filak→Dragos),
h53 NOVA LUKNJA 41–60 (14. dokazana), h2 trojna kontinuiteta (ISTI starši
1887+1889+1891), h28 Požek (3. hiša familije 79→77→28), h31 Straus mati
(ISTA OSEBA 1887+1890+1891), h5 Torec (nova), r52 evidence-only (prekrita).

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
DOKAZ = "research/issue17/parish-baptism-1891.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (49, 56)          # skeni 49–56 == strani 48–55 (okvir leta 1891)
ENTRY_SCANS = (50, 54)          # Griblje vpisi: skeni 50–54 (str. 49–53)
FRAME_PAGES = (48, 55)
BREAK_1892 = {"scan": 56, "page": 55, "row": 1}
EXPECTED_ENTRIES = 10
EXPECTED_DISTINCT = 9           # imenovane hiše (1 evidence-only izključena)
ILLEGIBLE_ROWS = (52,)          # r52 — hiša + datumi prekriti z modrimi pripisi
EXPECTED_PT_IN_SET = {"2", "5", "28", "30", "31", "61", "62", "72"}
EXPECTED_PT_GAP = {"53"}
PT_GAP_NEW = ["53"]
EXPECTED_HOUSES_VITALS = 9      # 10 vpisov − 1 evidence-only (runtime projekcija)
EXPECTED_VITALS_TOTAL = 490     # HOUSE_VITALS 121 + 12 (p80 I7 pin); P87: + 12 (1892); P88: + 17 (1893); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900); P98: + 12 (1903); P99: + 19 (1904); P101: + 18 (1906); P102: + 15 (1907); P103: + 18 (1908); P104: + 18 (1909); P105: + 20 (1910)
EV_ONLY_TOTAL = 8               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) + P103: r84 (1)
# sidra/pins P86:
H72_ROW = {"row": 6, "scan": 50, "fatherPin": "Straus"}
H30_ROW = {"row": 21, "scan": 51, "fatherPin": "Milek"}
H61_ROW = {"row": 39, "scan": 52, "fatherPin": "Pošek"}
H53_ROW = {"row": 40, "scan": 52, "fatherPin": "Pozdirec"}
H2_ROW = {"row": 43, "scan": 53, "fatherPin": "Hlebec"}
H28_ROW = {"row": 56, "scan": 54, "fatherPin": "Požek"}
CONT_HOUSE = "30"               # kontinuiteta z P85 dvojčki (rows 51+52)


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


def verify():
    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    entries = dokaz["entries"]
    inv = {}

    # I1 — knjiga dostopna + inventar 326
    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    # I3 — citirani skeni ⊆ okvir 49–56 + JPEG probe (sken 49 = str. 48: 1891
    # rows 1–3 brez Gribljev; sken 56 = str. 55: glava 1892 — citiran kot prelom)
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == list(range(ENTRY_SCANS[0], ENTRY_SCANS[1] + 1))
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1891, skeni 50–54, stran == sken − 1; prelom 1892
    rows = [e["row"] for e in entries]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1891 for e in entries)
        and all(e["scan"] - 1 == e["page"] for e in entries)
        and all(ENTRY_SCANS[0] <= e["scan"] <= ENTRY_SCANS[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and dokaz["frame"]["break1892"]["scan"] == BREAK_1892["scan"]
        and dokaz["frame"]["break1892"]["page"] == BREAK_1892["page"]
        and dokaz["frame"]["rowsTotal"] == 75
    )

    # I5 — števec: 10 vpisov / 9 hiš + 1 neberljiva (r52, evidence-only)
    ev_only = [e for e in entries if e["row"] in ILLEGIBLE_ROWS]
    named = [e for e in entries if e["row"] not in ILLEGIBLE_ROWS]
    houses = {e["houseNo"] for e in named}
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and all(e["houseNo"] is None for e in ev_only)
        and len(houses) == EXPECTED_DISTINCT
        and len(ev_only) == len(ILLEGIBLE_ROWS)
        and {e["row"] for e in ev_only} == set(ILLEGIBLE_ROWS)
    )

    # I6 — PT klasifikacija: 8 v naboru + 1 v luknji (53 NOVA — 14. dokazana)
    pts = pt_house_set()
    inset = sorted((h for h in houses if h in pts), key=int)
    gap = sorted((h for h in houses if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
        and dokaz["stats"]["newSampleHouses"] == ["28", "53"]
    )

    # I7 — sidra (h72 Straus = P83 1888; h30 Milek = P85 1890 kontinuiteta;
    # h61 Pošek/Požek = P82 sidro 1887 + menjava matere; h53 luknja + forenzika;
    # h2 Hlebec trojna kontinuiteta; h28 Požek 3. hiša familije)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    h72 = e_by_row(H72_ROW["row"])
    h30 = e_by_row(H30_ROW["row"])
    h61 = e_by_row(H61_ROW["row"])
    h53 = e_by_row(H53_ROW["row"])
    h2 = e_by_row(H2_ROW["row"])
    h28 = e_by_row(H28_ROW["row"])
    inv["I7_anchors"] = (
        h72["houseNo"] == "72"
        and H72_ROW["fatherPin"] in h72["father"]
        and "P83" in json.dumps(h72["notes"], ensure_ascii=False)
        and h30["houseNo"] == "30"
        and H30_ROW["fatherPin"] in h30["father"]
        and "P85" in json.dumps(h30["notes"], ensure_ascii=False)
        and h61["houseNo"] == "61"
        and H61_ROW["fatherPin"] in h61["father"]
        and "P82" in json.dumps(h61["notes"], ensure_ascii=False)
        and h53["houseNo"] == "53"
        and H53_ROW["fatherPin"] in h53["father"]
        and "LUKNJA" in json.dumps(h53["notes"], ensure_ascii=False)
        and h2["houseNo"] == "2"
        and H2_ROW["fatherPin"] in h2["father"]
        and "P82" in json.dumps(h2["notes"], ensure_ascii=False)
        and h28["houseNo"] == "28"
        and H28_ROW["fatherPin"] in h28["father"]
        and "P85" in json.dumps(h28["notes"], ensure_ascii=False)
    )

    # I8 — čez-letne kontinuitete: h30 (P85 dvojčka — isti oče + ista botra);
    # h2 (P82 — isti oče); h61 (P82 — očetov priimek Požek v obeh + mati
    # menjana); h72 (P83 — Strauš/Straus v obeh)
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p85_h30 = [e for e in p85["entries"] if e.get("houseNo") == CONT_HOUSE]
    p82_h2 = [e for e in p82["entries"] if e.get("houseNo") == "2"]
    p82_h61 = [e for e in p82["entries"] if e.get("houseNo") == "61"]
    p83_h72 = [e for e in p83["entries"] if e.get("houseNo") == "72"]
    inv["I8_crossyear_continuity"] = (
        len(p85_h30) == 2
        and all("Janez Milek" in e["father"] for e in p85_h30)
        and "Janez Milek" in h30["father"]
        and all("Matija Milek" in e["botra"] for e in p85_h30)
        and "Matija Milek" in h30["botra"]
        and len(p82_h2) == 1
        and "Peter Hlebec" in p82_h2[0]["father"]
        and "Peter Hlebec" in h2["father"]
        and len(p82_h61) == 1
        and "Požek" in p82_h61[0]["father"]
        and "Filath" in p82_h61[0]["mother"]
        and "Pošek" in h61["father"]
        and "Dragos" in h61["mother"]
        and "Filak" not in h61["mother"]
        and len(p83_h72) == 1
        and ("Strauš" in p83_h72[0]["father"] or "Straus" in p83_h72[0]["father"])
        and "Straus" in h72["father"]
    )

    # I9 — runtime projekcija: HOUSE_VITALS 1891 == 9 zasidranih (sk. 50–54,
    # page == sken−1); skupaj 121; h53 natanko 1 blok 1891; brez »Hraus« v
    # aktivnih whatSi poljih (re-read pripombe dovoljene — vzorec I9 p84/p85)
    vitals_1891 = parish_vitals(BOOK_SIGNATURE, 1891)
    hv_houses = sorted((v["houseNo"] for v in vitals_1891), key=int)
    src = open(PARISH_TS, encoding="utf-8").read()
    blocks_53 = re.findall(r"\{[^{}]*?houseNo:\s*\"53\"[^{}]*?\}", src, re.S)
    blocks_53_1891 = [b for b in blocks_53 if "year: 1891" in b]
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    active_hraus = [
        w for w in re.findall(r"whatSi:\s*\"([^\"]+)\"", src)
        if "Hraus" in w and "re-read" not in w and "prej" not in w
    ]
    inv["I9_runtime_projection"] = (
        len(vitals_1891) == EXPECTED_HOUSES_VITALS
        and sorted(set(hv_houses), key=int) == sorted(houses, key=int)
        and all(v["scan"] and 50 <= v["scan"] <= 54 and v["page"] == v["scan"] - 1
                for v in vitals_1891)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
        and len(blocks_53_1891) == 1
        and "Pozdirec" in blocks_53_1891[0]
        and not active_hraus
    )

    # I10 — statistika dokaza == neodvisen preracun: 7 ponovitev (h5 ČEZ
    # KNJIGE — mrliška 04894 1886; h61 1887+1897; h62 1887) + 2 novi (28, 53);
    # sampleTotal po konvenciji verige P82–P85 (zasidrani + evidence-only);
    # klasifikacija v P86 vesolju — brez P87/P88/P89 razširitev (1892/1893/1894
    # blokov ne morejo spreminjati zgodovinske klasifikacije leta 1891 — h53
    # je 1894 ponovitev, toda za P86 dokaz ostaja nova)
    vitals_pre87 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911))
    ]
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1891
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_pre87
    )]
    new_houses = sorted(houses - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    # edina imenovana evidence-only hiša v verigi: P85 r31/75/77 »65 [~]«
    p85_ev_named = [e["houseNo"] for e in p85["entries"]
                    if e.get("houseNo") is not None and e.get("row") in (31, 75, 77)]
    inv["I10_stats_independent"] = (
        len(repeat_houses) == dokaz["stats"]["repeatHouses"] == 7
        and new_houses == dokaz["stats"]["newSampleHouses"]
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 498  # kumulativno po P110 (490 + 8)
        and n_houses_total == 85  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4); P107: + 1 (h86)
        and p85_ev_named == ["65 [~]"]
        and dokaz["stats"]["sampleTotal"] == "127 vpisov / 58 hiš čez tri knjige (04105 + 04894 + 04455) in šest let (1886/1887/1888/1889/1890/1891)"
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 1
    )

    ok = all(inv.values())
    print("P86 — krstna knjiga 04105, polno leto 1891 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited}")
    vitals_all_n = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    print(f"vpisi {len(entries)} / hiše {len(houses)} + {len(ev_only)} neberljive;"
          f" PT {len(inset)}/{len(gap)}; vitals 1891 = {len(vitals_1891)};"
          f" vitals vseh treh knjig = {len(vitals_all_n)} (pričakovano {EXPECTED_VITALS_TOTAL})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
