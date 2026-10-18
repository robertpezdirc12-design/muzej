#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P88 — župnija Podzemelj: krstna knjiga 04105, polno leto 1893 (issue #18).

Razširitev vzorca P79 (1886) → P82 (1887) → P83 (1888) → P84 (1889) → P85
(1890) → P86 (1891) → P87 (1892) na leto 1893: okvir skeni 63–70 == strani
62–69 (glava »1893~« na str. 62 po 1892 row 82; velike cifre »1894« na str.
69 po row 83) — vsi vpisi z Griblji. LE OKVIR — prejšnja leta imajo svoje
skripte p82–p87. Sidra: h72 Strauš (SIDRO 3. VPIS — oče ISTI 3×: 1888+1891
+1893), h65 Milek (oče ISTI 3×: 1887+1889+1893), h27 DVOJČICI (Antonija +
Ivana, pripis »dvojčice«; oče Stukar/Stubhar [~]), h21 Šimec NAZAJ (mati
Ana Šimec + botra Janez Šimec; oče Požek ISTI 1887+1893, mati MENJANA),
h24 ISTA zveza Brinec × Jakobec 1887+1893 (5. vpis), h30 menjava
gospodinjstva (Milek → Jakljevič), h41 ISTA zveza 1890+1893, h15 ISTA
zveza 1887+1893, h60 NOVA (Željko 2. hiša), h91 NOVA (botra Željko + Kure).

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
DOKAZ = "research/issue17/parish-baptism-1893.json"
DOKAZ_P82 = "research/issue17/parish-baptism-1887.json"
DOKAZ_P83 = "research/issue17/parish-baptism-1888.json"
DOKAZ_P84 = "research/issue17/parish-baptism-1889.json"
DOKAZ_P85 = "research/issue17/parish-baptism-1890.json"
DOKAZ_P86 = "research/issue17/parish-baptism-1891.json"
DOKAZ_P87 = "research/issue17/parish-baptism-1892.json"
PARISH_TS = "src/data/atlas/parish.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (63, 70)          # skeni 63–70 == strani 62–69 (okvir leta 1893)
FRAME_PAGES = (62, 69)
BREAK_1894 = {"scan": 70, "page": 69}
EXPECTED_ENTRIES = 17
EXPECTED_DISTINCT = 16          # 17 vpisov / 16 hiš (h27 dvojčici)
ILLEGIBLE_ROWS = ()             # 1893 brez evidence-only
EXPECTED_PT_IN_SET = {"15", "21", "23", "24", "25", "27", "30", "32", "65", "70", "72", "74", "91"}
EXPECTED_PT_GAP = {"41", "46", "60"}
PT_GAP_NEW = ["46"]             # 46 NOVA — 15. dokazana; 41/60 že znana
EXPECTED_NEW_HOUSES = ["23", "46", "70", "91"]
EXPECTED_REPEATS = 12
EXPECTED_HOUSES_VITALS = 17     # 17 vpisov, vsi zasidrani (runtime projekcija)
EXPECTED_VITALS_TOTAL = 374     # HOUSE_VITALS 133 + 17 (p80 I7 pin); P89: + 14 (1894); P90: + 15 (1895); P91: + 14 (1896); P92: + 19 (1897); P93: + 12 (1898); P94: + 15 (1899); P95: + 16 (1900); P98: + 12 (1903); P99: + 19 (1904); P101: + 18 (1906); P102: + 15 (1907); P103: + 18 (1908)
EV_ONLY_TOTAL = 8               # P84: 2 + P85: 3 + P86: 1 + P102: r4 (1) + P103: r84 (1) (P87/P88: 0)
# sidra/pins P88:
H72_ROW = {"row": 46, "scan": 66, "fatherPin": "Strauš"}
H65_ROW = {"row": 15, "scan": 64, "fatherPin": "Milek"}
H27_ROW = {"row": 33, "scan": 65, "fatherPin": "Stukar"}
H21_ROW = {"row": 62, "scan": 68, "fatherPin": "Požek"}
H24_ROW = {"row": 56, "scan": 67, "fatherPin": "Brinec"}
H30_ROW = {"row": 50, "scan": 67, "fatherPin": "Jakljevič"}
H41_ROW = {"row": 22, "scan": 64, "fatherPin": "Hušič"}
H15_ROW = {"row": 39, "scan": 66, "fatherPin": "Jaklič"}
H60_ROW = {"row": 1, "scan": 63, "fatherPin": "Željko"}
H91_ROW = {"row": 31, "scan": 65, "fatherPin": "Novak"}


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

    # I3 — citirani skeni ⊆ okvir 63–70 + JPEG probe (sken 70 = str. 69:
    # prelom 1894; vpisi na skenih 63, 64, 65, 66, 67, 68)
    cited = sorted({e["scan"] for e in entries})
    inv["I3_cited_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and cited == [63, 64, 65, 66, 67, 68]
    probes = {s: probe_jpeg(urls[s - 1]) for s in cited} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())

    # I4 — okvir: vsi vpisi 1893, skeni 63–69, stran == sken − 1; prelom 1894
    rows = [e["row"] for e in entries]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1893 for e in entries)
        and all(e["scan"] - 1 == e["page"] for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and dokaz["frame"]["break1894"]["scan"] == BREAK_1894["scan"]
        and dokaz["frame"]["break1894"]["page"] == BREAK_1894["page"]
        and dokaz["frame"]["rowsTotal"] == 83
    )

    # I5 — števec: 17 vpisov / 16 hiš (h27 dvojčici) / 0 neberljivih
    ev_only = [e for e in entries if e["row"] in ILLEGIBLE_ROWS]
    named = [e for e in entries if e["row"] not in ILLEGIBLE_ROWS]
    houses = {e["houseNo"] for e in named}
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"] == "Griblje" for e in entries)
        and len(houses) == EXPECTED_DISTINCT
        and len(ev_only) == 0
        and dokaz["stats"]["housesIllegible"] == 0
        and sum(1 for e in entries if e["houseNo"] == "27") == 2
        and "dvojčice" in json.dumps([e["notes"] for e in entries if e["row"] in (33, 34)], ensure_ascii=False)
    )

    # I6 — PT klasifikacija: 13 v naboru + 3 v luknji (46 NOVA — 15. dokazana;
    # 41 že dokazana P85; 60 že dokazana P80 poroka); nove hiše 23/46/60/70/91
    pts = pt_house_set()
    inset = sorted((h for h in houses if h in pts), key=int)
    gap = sorted((h for h in houses if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGapNew"] == PT_GAP_NEW
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
    )

    # I7 — sidra (h72 Strauš SIDRO 3. VPIS; h65 Milek 3×; h27 dvojčici;
    # h21 Šimec nazaj + mati menjana; h24 ISTA zveza; h30 menjava;
    # h41 ISTA zveza; h15 ISTA zveza; h60 NOVA Željko 2. hiša; h91 NOVA)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    h72 = e_by_row(H72_ROW["row"])
    h65 = e_by_row(H65_ROW["row"])
    h27 = e_by_row(H27_ROW["row"])
    h21 = e_by_row(H21_ROW["row"])
    h24 = e_by_row(H24_ROW["row"])
    h30 = e_by_row(H30_ROW["row"])
    h41 = e_by_row(H41_ROW["row"])
    h15 = e_by_row(H15_ROW["row"])
    h60 = e_by_row(H60_ROW["row"])
    h91 = e_by_row(H91_ROW["row"])
    inv["I7_anchors"] = (
        h72["houseNo"] == "72"
        and H72_ROW["fatherPin"] in h72["father"]
        and "3. VPIS" in json.dumps(h72["notes"], ensure_ascii=False)
        and h65["houseNo"] == "65"
        and H65_ROW["fatherPin"] in h65["father"]
        and "3×" in json.dumps(h65["notes"], ensure_ascii=False)
        and h27["houseNo"] == "27"
        and H27_ROW["fatherPin"] in h27["father"]
        and "DVOJČICA" in json.dumps(h27["notes"], ensure_ascii=False)
        and h21["houseNo"] == "21"
        and H21_ROW["fatherPin"] in h21["father"]
        and "Šimec" in h21["mother"]
        and "MENJANA" in json.dumps(h21["notes"], ensure_ascii=False)
        and h24["houseNo"] == "24"
        and H24_ROW["fatherPin"] in h24["father"]
        and "ISTA ZVEZA" in json.dumps(h24["notes"], ensure_ascii=False)
        and h30["houseNo"] == "30"
        and H30_ROW["fatherPin"] in h30["father"]
        and "MENJAVA GOSPODINJSTVA" in json.dumps(h30["notes"], ensure_ascii=False)
        and h41["houseNo"] == "41"
        and H41_ROW["fatherPin"] in h41["father"]
        and "ISTA ZVEZA" in json.dumps(h41["notes"], ensure_ascii=False)
        and h15["houseNo"] == "15"
        and H15_ROW["fatherPin"] in h15["father"]
        and "ISTA ZVEZA" in json.dumps(h15["notes"], ensure_ascii=False)
        and h60["houseNo"] == "60"
        and H60_ROW["fatherPin"] in h60["father"]
        and "2. HIŠA" in json.dumps(h60["notes"], ensure_ascii=False)
        and h91["houseNo"] == "91"
        and H91_ROW["fatherPin"] in h91["father"]
        and "Željko" in h91["botra"]
    )

    # I8 — čez-letne kontinuitete prek dokazov: h72 (P83 1888 + P86 1891 —
    # oče Strauš vsi trije); h65 (P82 1887 + P84 1889 — oče Milek vsi trije);
    # h27 (P82 1887 Kukar × Klobučar); h15 (P82 1887 Jakšič × Brinec); h21
    # (P82 1887 Požek × Brinec); h41 (P85 1890 Hrušič × Jakobčič); h30
    # (P85 1890 Milek); h24 (P87 1892 Jurajevič — izmenjava); h32 (P87 1892
    # Urh × Pegdirec + botra Hrižan/Strauš); h1 (P83 1888 Zeljth × Kure)
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p84 = json.load(open(DOKAZ_P84, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p86 = json.load(open(DOKAZ_P86, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p83_h72 = [e for e in p83["entries"] if e.get("houseNo") == "72"]
    p86_h72 = [e for e in p86["entries"] if e.get("houseNo") == "72"]
    p82_h65 = [e for e in p82["entries"] if e.get("houseNo") == "65"]
    p84_h65 = [e for e in p84["entries"] if e.get("houseNo") == "65"]
    p82_h27 = [e for e in p82["entries"] if e.get("houseNo") == "27"]
    p82_h15 = [e for e in p82["entries"] if e.get("houseNo") == "15"]
    p82_h21 = [e for e in p82["entries"] if e.get("houseNo") == "21"]
    p85_h41 = [e for e in p85["entries"] if e.get("houseNo") == "41"]
    p85_h30 = [e for e in p85["entries"] if e.get("houseNo") == "30"]
    p87_h32 = [e for e in p87["entries"] if e.get("houseNo") == "32"]
    p87_h24 = [e for e in p87["entries"] if e.get("houseNo") == "24"]
    p83_h1 = [e for e in p83["entries"] if e.get("houseNo") == "1"]
    inv["I8_crossyear_continuity"] = (
        len(p83_h72) == 1
        and ("Strauš" in p83_h72[0]["father"] or "Straus" in p83_h72[0]["father"])
        and len(p86_h72) == 1
        and "Straus" in p86_h72[0]["father"]
        and "Strauš" in h72["father"]
        and len(p82_h65) == 1
        and "Milek" in p82_h65[0]["father"]
        and len(p84_h65) == 1
        and "Milek" in p84_h65[0]["father"]
        and "Milek" in h65["father"]
        and len(p82_h27) == 1
        and "Kukar" in p82_h27[0]["father"]
        and "Klobučar" in p82_h27[0]["mother"]
        and "Klobučar" in h27["mother"]
        and len(p82_h15) == 1
        and "Jakšič" in p82_h15[0]["father"]
        and "Brinec" in p82_h15[0]["mother"]
        and "Brinec" in h15["mother"]
        and len(p82_h21) == 1
        and "Požek" in p82_h21[0]["father"]
        and "Brinec" in p82_h21[0]["mother"]
        and "Požek" in h21["father"]
        and "Šimec" in h21["mother"]
        and len(p85_h41) == 2
        and any("Hrušič" in e["father"] for e in p85_h41)
        and "Hušič" in h41["father"]
        and "Jakobič" in h41["mother"]
        and len(p85_h30) == 2
        and all("Milek" in e["father"] for e in p85_h30)
        and "Jakljevič" in h30["father"]
        and len(p87_h32) == 1
        and "Urh" in p87_h32[0]["father"]
        and "Pegdirec" in p87_h32[0]["mother"]
        and "Pegdirec" in next(e for e in entries if e["row"] == 69)["mother"]
        and "Hrižan" in next(e for e in entries if e["row"] == 69)["botra"]
        and len(p87_h24) == 1
        and "Jurajevič" in p87_h24[0]["father"]
        and "Brinec" in h24["father"]
        and len(p83_h1) == 1
        and "Zeljth" in p83_h1[0]["father"]
        and "Željko" in h60["father"]
        and "Željko" in h91["botra"]
    )

    # I9 — runtime projekcija: HOUSE_VITALS 1893 == 17 zasidranih (sk. 63–69,
    # page == sken−1); skupaj 150; brez »Hraus« v aktivnih whatSi poljih
    vitals_1893 = parish_vitals(BOOK_SIGNATURE, 1893)
    hv_houses = sorted((v["houseNo"] for v in vitals_1893), key=int)
    src = open(PARISH_TS, encoding="utf-8").read()
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    active_hraus = [
        w for w in re.findall(r"whatSi:\s*\"([^\"]+)\"", src)
        if "Hraus" in w and "re-read" not in w and "prej" not in w
    ]
    inv["I9_runtime_projection"] = (
        len(vitals_1893) == EXPECTED_HOUSES_VITALS
        and sorted(set(hv_houses), key=int) == sorted(houses, key=int)
        and all(v["scan"] and 63 <= v["scan"] <= 69 and v["page"] == v["scan"] - 1
                for v in vitals_1893)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
        and not active_hraus
    )

    # I10 — statistika dokaza == neodvisen preracun: 12 ponovitev + 4 novi
    # (23, 46, 70, 91; h60 ponovitev čez knjige — poroka 04455 1886); sampleTotal
    # po konvenciji verige P82–P87; klasifikacija v P88 vesolju — brez P89
    # razširitve (1894 blokov ne more spreminjati zgodovinske klasifikacije
    # leta 1893 — h23 je 1894 ponovitev, toda za P88 dokaz ostaja nova)
    vitals_pre89 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] in (1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908))
    ]
    repeat_houses = [h for h in houses if any(
        v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1893
        or v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE
        for v in vitals_pre89
    )]
    new_houses = sorted(houses - set(repeat_houses), key=int)
    n_entries_total = len(vitals_all)
    n_houses_total = len({v["houseNo"] for v in vitals_all})
    p85_ev_named = [e["houseNo"] for e in p85["entries"]
                    if e.get("houseNo") is not None and e.get("row") in (31, 75, 77)]
    inv["I10_stats_independent"] = (
        len(repeat_houses) == dokaz["stats"]["repeatHouses"] == EXPECTED_REPEATS
        and new_houses == dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 382  # kumulativno po P103 (374 + 8)
        and n_houses_total == 84  # P98: 80 vitals; P99: + 3 (h6, h42, h50); P100: + 0 (1905 brez novih); P101: + 1 (h4)
        and p85_ev_named == ["65 [~]"]
        and dokaz["stats"]["sampleTotal"] == "156 vpisov / 65 hiš čez tri knjige (04105 + 04894 + 04455) in osem let (1886/1887/1888/1889/1890/1891/1892/1893)"
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
    )

    ok = all(inv.values())
    print("P88 — krstna knjiga 04105, polno leto 1893 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {cited}")
    print(f"vpisi {len(entries)} / hiše {len(houses)} + {len(ev_only)} neberljive;"
          f" PT {len(inset)}/{len(gap)}; vitals 1893 = {len(vitals_1893)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
