#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P111 — župnija Podzemelj: krstna knjiga 04105, polno leto 1916 (issue #18).

Razširitev vzorca P79 (1886) → … → P109 (1914) → P110 (1915) na leto 1916
(2. VOJNO leto; 41 vpisov — NAJNIŽE doslej! polovica 1915!). Okvir: glava
»1916« ročno INLINE sredi str. 237 = s283-B (P110 lead POTRJEN) + tiskana
glava »Leto 1916« na VRHU str. 238 = s284-A; 1916 r1 = Grišiče 3 Julija
9./11. Januar; **r28 + r29 = DVOJNI VPIS istega mrtvorojenega otroka**
(Krasinec 8: r28 »Mrtvorojena« brez krsta + r29 »Neža Cajnar« »krščena
v sili« = ISTA OSEBA — nov protokol!); **r41 = GRIBLJE 37 Marko
mrtvorojen + krsta kolona »krščena v sili in utero m.« = NUJNI KRST V
MATERNICI — PRVI V VZORCU!** (enovrstični model!); zaključna opomba
»I številko 41 zaključeno število porodov oz. krstov v l. 1916.« +
podpis O. Mučah? / ozd. leut? [~]. == strani 237–244 == skeni 283–290
(8 skenov; str. == sken − 46); **NIČ DUP PAROV — prvo leto od P106!**

VSI vpisi z Griblji: **6 vpisov / 6 hiš — NARE 6/6 (11. čisto leto!)** +
**1 NOVA hiša h82** (1. vpis v vseh treh knjigah! prekinjena 0-seriji
P109/P110) + h88 ZAPORED 2. leto (Brinec × Butala ×2!) + h36 ZAPORED
familija (Štraus botrinja cf. P107!) + **h37 VRZEL 19 LET** (2. najdaljša
po h78 27!) — in njen edini vpis je MRTVOROJEN. Kumulativ s P79–P110:
**539 vpisov / 88 hiš / 31 let** (1886–1916; 496 vitals).

NOVELE 1916: **2 protokola mrtvorojenih** (r28+r29 dvojni vpis vs. r41
enovrstični + in-utero krst!) + **r31 DVOJNA hiša 25/32 + DVOJNO ime
Alojzij Franc** (prva dvojna hiša!) + **ŽELEZNIŠKA TEMA ×3** (r31 Kok +
r37 Škravara/Župančič; poroka 11.6.1916 ISTO LETO!) + **mesec glavi
»marcij« (latinsko!) + »majnik« (idiosinkrazija!)** + nezakonska r35
(razglašena marg!) + vojna smrtnost otrok ~18/41 = **44% EKSTREMUM** +
podpisna uganka Učak/Bitnar/Muh 07/Mučah (možen 5. duhovnik) + EMŠO
kampanja 12 kandidatov (r12 + r23 ZOOM potrjena sidra).

Excluded: 35. Skripta scripts/p111_parish_baptism_1916.py (I1–I12,
--check izpiše PASS/FAIL in vrne exit code).
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
DOKAZ = "research/issue17/parish-baptism-1916.json"
DOKAZ_P110 = "research/issue17/parish-baptism-1915.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (283, 290)        # 283 = str. 237 (r1–r3 + glava 1916 inline) – 290 = str. 244 (r38–r41 + zaključna opomba)
FRAME_PAGES = (237, 244)
EXPECTED_ENTRIES = 6
EXPECTED_DISTINCT = 6           # NARE 6/6 — 11. čisto leto!
EXPECTED_EXCLUDED = 35
EXPECTED_STRUCK = 0
EXPECTED_HOUSES = sorted([12, 34, 36, 37, 82, 88])
EXPECTED_VITALS_HOUSES = EXPECTED_HOUSES
EXPECTED_PT_IN_SET = ["12", "34", "36", "37", "82", "88"]
EXPECTED_PT_GAP = []            # vseh 6 v PT naboru!
EXPECTED_NEW_HOUSES = 1         # h82!
EXPECTED_NEW_HOUSE_NOS = ["82"]
EXPECTED_VITALS_TOTAL = 496     # 490 + 6 (P111)
BLOCKS_04105 = 470              # 464 + 6
KUMULATIV_ENTRIES = 539         # 498 + 41
KUMULATIV_HOUSES = 88           # + 1 (h82)
KUMULATIV_YEARS = 31            # 1886–1916
# kontinuitete (hiša → zadnje krstno leto pred 1916 v 04105, iz parish.ts)
CONTINUITY = {
    "12": 1912, "34": 1913, "36": 1913, "37": 1897, "88": 1915,
}
# sidra/pini P111 (row, scan, hiša, pin):
ANCHORS = [
    (10, 285, "34", "1. GRIBLJE"),
    (10, 285, "34", "Učak"),
    (10, 285, "34", "26.8.1917"),
    (21, 286, "12", "2. GRIBLJE"),
    (21, 286, "12", "Toter"),
    (22, 287, "82", "3. GRIBLJE"),
    (22, 287, "82", "NOVA HIŠA"),
    (22, 287, "82", "majnik"),
    (22, 287, "82", "TESARSKI"),
    (23, 287, "36", "4. GRIBLJE"),
    (23, 287, "36", "2205916500023"),
    (23, 287, "36", "1983"),
    (23, 287, "36", "ŠTRAUS"),
    (26, 287, "88", "5. GRIBLJE"),
    (26, 287, "88", "ZAPORED 2. LETO"),
    (26, 287, "88", "Butala"),
    (41, 290, "37", "6. GRIBLJE"),
    (41, 290, "37", "in utero"),
    (41, 290, "37", "VRZEL 19 LET"),
    (41, 290, "37", "MRTVOROJEN"),
]
EMSO_ANCHOR_ROWS = {
    23: "2205916500023",
}
GRIBLJE_UCak = 4                # jasni podpisi Učak ≥4 (r10/r22/r23/r26; r21 dvom!)
GRIBLJE_JAKOFCIC = 2            # babica Jakofčič ×2 (r22/r23)
DEAD_CHILDREN_NOTE_MIN = 3      # r10 + r21 + r22 + r26 + r41 — †/‡/mrtvorojen ≥3


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


def parish_vitals_04105():
    src = open(PARISH_TS, encoding="utf-8").read()
    blocks = re.findall(r"\{[^{}]*?bookSignature:\s*\"" + BOOK_SIGNATURE + r"\"[^{}]*?\}", src, re.S)
    out = []
    for b in blocks:
        hn = re.search(r'houseNo:\s*"([^"]*)"', b)
        yr = re.search(r"year:\s*(\d+)", b)
        out.append({"houseNo": hn.group(1) if hn else None,
                    "year": int(yr.group(1)) if yr else None})
    return out


def page_of_scan(scan):
    """P111: NI dup parov — str. == sken − 46 strogo linearno."""
    return {283: 237, 284: 238, 285: 239, 286: 240, 287: 241,
            288: 242, 289: 243, 290: 244}.get(scan)


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p110 = json.load(open(DOKAZ_P110, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + stran==sken−46 + 0 dup parov + glava 1916
    # inline + r28/r29 dvojni vpis + r41 in-utero + zaključna opomba 41
    cited = sorted({e["scan"] for e in entries})
    inv["I3_frame"] = (
        cited == sorted(set(cited)) and set(cited) <= set(range(283, 291))
        and all(page_of_scan(s) == p for s, p in ((e["scan"], e["page"]) for e in entries))
        and dokaz["frame"]["rowsTotal"] == 41
        and dokaz["frame"]["rowsStruck"] == 0
        and dokaz["frame"]["dupPari"] == []
        and dokaz["frame"]["scans"] == list(FRAME_SCANS)
        and dokaz["frame"]["pages"] == list(FRAME_PAGES)
        and "NIČ DUP PAROV" in dokaz["frame"]["dupPariNote"]
        and "INLINE" in dokaz["frame"]["rowsNote"]
        and "DVOJNI VPIS" in dokaz["frame"]["rowsNote"]
        and "in utero" in dokaz["frame"]["rowsNote"]
        and "I številko 41" in dokaz["frame"]["rowsNote"]
        and dokaz["p112Lead"]["glava1917"].startswith("ročno »917«")
    )

    # I4 — 6 vpisov / 6 hiš (NARE 6/6!) + hiše + vitals hiše
    hv = parish_vitals_04105()
    hv1916 = [b for b in hv if b["year"] == 1916]
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and sorted(int(h) for h in set(houses)) == EXPECTED_HOUSES
        and sorted(int(b["houseNo"]) for b in hv1916 if b["houseNo"]) == EXPECTED_VITALS_HOUSES
    )

    # I5 — kontinuiteta: CONTINUITY iz dokaza se sklada s parish.ts
    ok5 = True
    for hn, last_year in CONTINUITY.items():
        ys = [b["year"] for b in hv if b["houseNo"] == hn and b["year"] < 1916]
        if not ys or max(ys) != last_year:
            ok5 = False
    inv["I5_continuity"] = ok5

    # I5b — 1 nova hiša h82: SAMO h82 nima zgodnejših vpisov; ostale imajo
    have_earlier = {hn for hn in set(houses)
                    if any(b["houseNo"] == hn and b["year"] < 1916 for b in hv)}
    inv["I5b_one_new_house"] = (
        have_earlier == {"12", "34", "36", "37", "88"}
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newHouseNos"] == EXPECTED_NEW_HOUSE_NOS
    )

    # I6 — PT klasifikacija: 6/6 v naboru; 0 gap; kumulativ 539/88/31
    pts = pt_house_set()
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == EXPECTED_PT_GAP
        and dokaz["stats"]["pt"] == "6/0 (vseh 6 hiš v PT naboru; PT_GAP_KNOWN ne potreben!)"
        and dokaz["stats"]["newHouseNos"] == EXPECTED_NEW_HOUSE_NOS
        and dokaz["stats"]["cumulative"] == "539 vpisov / 88 hiš / 31 let (1886–1916)"
        and dokaz["stats"]["vitals"] == EXPECTED_VITALS_TOTAL
    )

    # I7 — sidra (20 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False).lower()
        if not (e["houseNo"] == hn and e["scan"] == scan and pin.lower() in blob):
            ok7 = False
    r10 = e_by_row(10)
    r22 = e_by_row(22)
    r23 = e_by_row(23)
    r26 = e_by_row(26)
    r41 = e_by_row(41)
    inv["I7_anchors"] = (
        ok7
        # r10 — 1. Griblje + Učak + † 26.8.1917
        and "Učak" in r10["priest"] and "26.8.1917" in json.dumps(r10, ensure_ascii=False)
        # r22 — NOVA HIŠA h82 + majnik + tesarski moj.
        and "NOVA HIŠA" in json.dumps(r22, ensure_ascii=False)
        and "majnik" in r22["month"] and "tesarski" in json.dumps(r22, ensure_ascii=False).lower()
        # r23 — EMŠO + umrl 1983 POPRAVLJENO + ŠTRAUS botrinja
        and "2205916500023" in json.dumps(r23, ensure_ascii=False)
        and "1983" in json.dumps(r23, ensure_ascii=False)
        and "POPRAVLJENO" in json.dumps(r23, ensure_ascii=False)
        and "štraus" in r23["botra"].lower()
        # r26 — ZAPORED 2. LETO + Butala
        and "zapored 2. leto" in json.dumps(r26, ensure_ascii=False).lower()
        and "Butala" in r26["mother"]
        # r41 — mrtvorojen + in utero + VRZEL 19 LET
        and "mrtvorojen" in r41["child"].lower() and "in utero" in r41["baptized"]
        and any("VRZEL 19 LET" in n for n in r41["notes"])
    )

    # I8 — EMŠO sidro (r23 = 2205916500023, ZOOM 4.5×)
    ok8 = all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
              for row, EMSO in EMSO_ANCHOR_ROWS.items())
    inv["I8_emso_anchors"] = ok8

    # I9 — statistika: Učak ≥5, Jakofčič ×2, † otroci ≥3, vrzeli ≥1 (h37 19!),
    # dup 0, excluded 35, struck 0, anomalij ≥14, vitals hiš 6
    bab = [e["babica"] or "" for e in entries]
    inv["I9_stats"] = (
        sum(1 for e in entries if "Učak" in (e["priest"] or "")) >= GRIBLJE_UCak
        and sum(1 for b in bab if "Jakofčič" in b) == GRIBLJE_JAKOFCIC
        and sum(1 for e in entries if any(("†" in n or "‡" in n or "MRTVOROJEN" in n) for n in e["notes"])) >= DEAD_CHILDREN_NOTE_MIN
        and sum(1 for e in entries if any("VRZEL" in n and "LET" in n for n in e["notes"])) >= 2
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["intraYearRepeats"] == 0
        and dokaz["excludedCount"] == EXPECTED_EXCLUDED
        and dokaz["frame"]["rowsStruck"] == EXPECTED_STRUCK
        and len(dokaz["anomalies"]) >= 14
        and "44%" in dokaz["stats"]["deadInfants"]
    )

    # I9b — P110 lead kontrola: p111Lead trdi 1916 r1 = Grišiče 3 Julija
    # → P111 POTRJUJE (village/hiša/ime) + botra Kočevar NE POTRJENA +
    # P111 p112Lead pripravljen (1917 r1 = Griblje 45)
    ex1 = next(x for x in excluded if x["row"] == 1)
    inv["I9b_lead_control"] = (
        dokaz_p110["p111Lead"]["r1"].startswith("Grišiče 3")
        and ex1["village"] == "Grišiče" and ex1["houseNo"] == "3"
        and ex1["child"] == "Julija"
        and "NE POTRJEN" in ex1["reason"]
        and dokaz["p112Lead"]["r1"].startswith("GRIBLJE 45")
        and "razvezana" in dokaz["p112Lead"]["r1"]
    )

    # I10 — neodvisen preračun: vsi village == Griblje; sken→stran; vrstice
    ok10 = all(e["village"] == "Griblje" for e in entries)
    for e in entries:
        if page_of_scan(e["scan"]) != e["page"]:
            ok10 = False
    rows = sorted(e["row"] for e in entries)
    ok10 = ok10 and rows == sorted(rows) and len(rows) == len(set(rows))
    # r28+r29 dvojni vpis: r29 v excluded z »krščena v sili« + isti houseNo
    ex28 = next(x for x in excluded if x["row"] == 28)
    ex29 = next(x for x in excluded if x["row"] == 29)
    ok10 = ok10 and ex28["houseNo"] == "8" and ex29["houseNo"] == "8" \
        and "krščena v sili" in ex29["reason"]
    inv["I10_independent_recalc"] = ok10

    # vitals skupaj 496 (490 + 6; vse tri knjige 04105+04894+04455)
    src_all = open(PARISH_TS, encoding="utf-8").read()
    total_blocks = len(re.findall(r"\{[^{}]*?bookSignature:\s*\"(04105|04894|04455)\"[^{}]*?\}", src_all, re.S))
    inv["I11_vitals_total"] = total_blocks == EXPECTED_VITALS_TOTAL
    inv["I12_blocks_04105"] = len(hv) == BLOCKS_04105

    passed = sum(1 for v in inv.values() if v)
    total = len(inv)
    for k, v in inv.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    print(f"--- {passed}/{total} PASS")
    return 0 if passed == total else 1


def main():
    if "--check" in sys.argv:
        sys.exit(verify())
    print(__doc__)


if __name__ == "__main__":
    main()
