#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P112 — župnija Podzemelj: krstna knjiga 04105, polno leto 1917 (issue #18).

Razširitev vzorca P79 (1886) → … → P110 (1915) → P111 (1916) na leto 1917
(3. VOJNO leto; 55 vpisov — ODBOJKA od 41! +34%). Okvir: glava »1917«
tiskana VRH str. 245 = s291-A (+ velika ročna »1917«); 1917 r1 = GRIBLJE
45 Karol Feliks (P111 lead POTRJEN — razvezana zveza 1956!); **55 vpisov
r1–r55 čez str. 245–253 == s291–s299 (9 skenov; str. == sken − 46)**;
zaključna opomba **»Š t. 55 je zaključno število porodov oziroma krstov
v l. 1917«** + podpis O. M. Učak? ord. tout. [~]. **NIČ DUP PAROV — 2.
leto zapored!**

VSI vpisi z Griblji: **12 vpisov / 11 hiš — NARE 12/12 (12. čisto leto!)
+ 0 NOVIH hiš (3. zapored!)** + h24 ×2 = **DVOJČKA r26+r27** (Anton +
Ivana, isti dan 28.5.1917, EMŠO oba 2805917 ✓ ZOOM 5×!) + **h88 ZAPORED
3. LETO** (1915+1916+1917 — 1. trojno zaporedje!) + h37 nadaljuje po
1916 mrtvorojencu + **h62 VRZEL 10 LET** (najdaljša aktivna 1917).
NOVELE 1917: **glava »jamarija«** (nova idiosinkrazija!) + »marecij« ×2
+ »majnik« (ponovitve) + mesec popravek september→oktober (r45) +
**MRTVOROJENI/V-SILI ×3** (r14 + r38 + r40 z IME PRAZNO + babica
»tudi krstila«!) + **RAZGLAŠENI ×3 = REKORD** (r30/r50/r55 — »kot član
K.B.g. [~] ni preživel« 15.5.1946!) + **BEGUNCI Renče št. 296 na
Goriškem** (r54 — Soška fronta, 1. begunski protokol!) + **POSTHUMNO
rojstvo** (r39 — oče † 13.5.1917, 3 mesece pred rojstvom!) + **VPIS
PRENEŠEN ×4 pečati** (r18 1966 + r36 MRB 2005 + r43/r52 2007 — NOVELA!)
+ **hiša »čuvaj meča 34«** (r7 — železniška čuvajnica!) + železniška
tema ×5 + ŽUPAN botri ×3 + **Mara Hudorovac CIGANKA** (r37 — 1.
eksplicitna etnična označba!) + EMŠO kampanja 21 (datumski ✓ 21/21 po
2 POPRAVKIH 2805/2207!; spolna šifra M=500/F=505 anomalija!) + oče 58
let (r29 Bohte 1859!) + mož † 26.3.1945 WWII (r52!) + cross-ref »glej
strani 264« (r20 → P114 lead!). Kumulativ s P79–P111:
**594 vpisov / 88 hiš / 32 let** (1886–1917; 508 vitals).

Excluded: 43. Skripta scripts/p112_parish_baptism_1917.py (I1–I12+I5b,
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
DOKAZ = "research/issue17/parish-baptism-1917.json"
DOKAZ_P111 = "research/issue17/parish-baptism-1916.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (291, 299)        # 291 = str. 245 (r1–r6 + glava 1917) – 299 = str. 253 (r53–r55 + zaključna opomba)
FRAME_PAGES = (245, 253)
EXPECTED_ENTRIES = 12
EXPECTED_DISTINCT = 11          # NARE 12/12 — h24 ×2 (dvojčka)!
EXPECTED_EXCLUDED = 43
EXPECTED_STRUCK = 0
EXPECTED_HOUSES = sorted([5, 9, 14, 24, 31, 37, 45, 46, 62, 77, 88])
EXPECTED_VITALS_HOUSES = EXPECTED_HOUSES
EXPECTED_PT_IN_SET = [5, 9, 14, 24, 31, 37, 62, 77, 88]
EXPECTED_PT_GAP = ["45", "46"]    # v luknji 41–60 — obe dokazani v PT_GAP_KNOWN (cf. P110 h45+h46+h53)!
EXPECTED_NEW_HOUSES = 0         # 3. zapored z 0 novih!
EXPECTED_NEW_HOUSE_NOS = []
EXPECTED_VITALS_TOTAL = 508     # 496 + 12 (P112)
BLOCKS_04105 = 482              # 470 + 12
KUMULATIV_ENTRIES = 594         # 539 + 55
KUMULATIV_HOUSES = 88           # + 0
KUMULATIV_YEARS = 32            # 1886–1917
# kontinuitete (hiša → zadnje krstno leto pred 1917 v 04105, iz parish.ts)
CONTINUITY = {
    "45": 1915, "62": 1907, "14": 1914, "31": 1913, "24": 1912,
    "46": 1915, "5": 1914, "88": 1916, "77": 1914, "9": 1915, "37": 1916,
}
# sidra/pini P112 (row, scan, hiša, pin):
ANCHORS = [
    (1, 291, "45", "1. GRIBLJE"),
    (1, 291, "45", "jamarija"),
    (1, 291, "45", "razvezana"),
    (3, 291, "62", "2. GRIBLJE"),
    (3, 291, "62", "VRZEL 10 LET"),
    (3, 291, "62", "18/1 1917"),
    (14, 293, "14", "3. GRIBLJE"),
    (14, 293, "14", "MRTVOROJEN"),
    (18, 293, "31", "4. GRIBLJE"),
    (18, 293, "31", "VPIS PRENEŠEN"),
    (18, 293, "31", "23.08.1966"),
    (26, 295, "24", "5. GRIBLJE"),
    (26, 295, "24", "DVOJČEK"),
    (26, 295, "24", "2805917500040"),
    (27, 295, "24", "6. GRIBLJE"),
    (27, 295, "24", "DVOJČICA"),
    (27, 295, "24", "2805917505115"),
    (35, 296, "46", "7. GRIBLJE"),
    (35, 296, "46", "16.7.1928"),
    (35, 296, "46", "1859"),
    (37, 296, "5", "8. GRIBLJE"),
    (37, 296, "5", "CIGANKA"),
    (37, 296, "5", "2207917500054"),
    (41, 297, "88", "9. GRIBLJE"),
    (41, 297, "88", "ZAPORED 3. LETO"),
    (41, 297, "88", "9.11.1918"),
    (43, 297, "77", "10. GRIBLJE"),
    (43, 297, "77", "VPIS PRENEŠEN"),
    (48, 298, "9", "11. GRIBLJE"),
    (48, 298, "9", "Ožbald"),
    (52, 298, "37", "12. GRIBLJE"),
    (52, 298, "37", "VPIS PRENEŠEN"),
    (52, 298, "37", "0812917505459"),
]
EMSO_ANCHOR_ROWS = {
    26: "2805917500040", 27: "2805917505115",
    37: "2207917500054", 52: "0812917505459",
}
GRIBLJE_UCak = 6                # jasni podpisi Učak ≥6 (r18/r26/r27/r35/r41/r43/r48/r52)
GRIBLJE_JAKOFCIC = 4            # babica Jakofčič ×4 (r18/r35/r41/r43; r48 = Jakobčič ort. var.)
DEAD_CHILDREN_NOTE_MIN = 3      # r3 ‡ + r14 MRTVOROJEN + r41 †


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
    """P112: NI dup parov — str. == sken − 46 strogo linearno."""
    return {291: 245, 292: 246, 293: 247, 294: 248,
            295: 249, 296: 250, 297: 251, 298: 252, 299: 253}.get(scan)


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p111 = json.load(open(DOKAZ_P111, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + stran==sken−46 + 0 dup parov + glava
    # 1917 + r14/r38/r40 protokoli + zaključna opomba 55
    cited = sorted({e["scan"] for e in entries})
    inv["I3_frame"] = (
        cited == sorted(set(cited)) and set(cited) <= set(range(291, 300))
        and all(page_of_scan(s) == p for s, p in ((e["scan"], e["page"]) for e in entries))
        and dokaz["frame"]["rowsTotal"] == 55
        and dokaz["frame"]["rowsStruck"] == 0
        and dokaz["frame"]["dupPari"] in (0, [])
        and dokaz["frame"]["scans"] == list(FRAME_SCANS)
        and dokaz["frame"]["pages"] == list(FRAME_PAGES)
        and "NIČ prekoračitve" in dokaz["frame"]["rowsNote"]
        and "Š t. 55" in dokaz["frame"]["rowsNote"]
        and dokaz["p113Lead"]["glava1918"].startswith("ročno zapisana **1918**")
        and "POKRITO" in dokaz["p113Lead"]["r3"]
    )

    # I4 — 12 vpisov / 11 hiš (NARE 12/12; h24 ×2!) + hiše + vitals hiše
    hv = parish_vitals_04105()
    hv1917 = [b for b in hv if b["year"] == 1917]
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and sorted(int(h) for h in set(houses)) == EXPECTED_HOUSES
        and sorted({int(b["houseNo"]) for b in hv1917 if b["houseNo"]}) == EXPECTED_VITALS_HOUSES
        and len(hv1917) == EXPECTED_ENTRIES   # 12 blokov (h24 ×2!)
    )

    # I5 — kontinuiteta: CONTINUITY iz dokaza se sklada s parish.ts
    ok5 = True
    for hn, last_year in CONTINUITY.items():
        ys = [b["year"] for b in hv if b["houseNo"] == hn and b["year"] < 1917]
        if not ys or max(ys) != last_year:
            ok5 = False
    inv["I5_continuity"] = ok5

    # I5b — 0 novih hiš (3. zapored!): vseh 11 ima zgodnejše vpise
    have_earlier = {hn for hn in set(houses)
                    if any(b["houseNo"] == hn and b["year"] < 1917 for b in hv)}
    inv["I5b_zero_new_houses"] = (
        have_earlier == set(houses)
        and dokaz["stats"]["newSampleHouses"] == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newHouseNos"] == EXPECTED_NEW_HOUSE_NOS
    )

    # I6 — PT klasifikacija: 9/11 v naboru; gap = [45, 46] (luknja 41–60,
    # PT_GAP_KNOWN!) ; kumulativ 594/88/32
    pts = pt_house_set()
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    inset = sorted((int(h) for h in set(houses) if h in pts))
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET)
        and gap == EXPECTED_PT_GAP
        and "45" in pt_gap_set and "46" in pt_gap_set
        and dokaz["stats"]["pt"] == "9/2 (h45 + h46 v luknji 41–60 — obe dokazani v PT_GAP_KNOWN!)"
        and dokaz["stats"]["cumulative"] == "594 vpisov / 88 hiš / 32 let (1886–1917)"
        and dokaz["stats"]["vitals"] == EXPECTED_VITALS_TOTAL
    )

    # I7 — sidra (33 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False).lower()
        if not (e["houseNo"] == hn and e["scan"] == scan and pin.lower() in blob):
            ok7 = False
    r1 = e_by_row(1)
    r26 = e_by_row(26)
    r27 = e_by_row(27)
    r37 = e_by_row(37)
    r41 = e_by_row(41)
    r54ex = next(x for x in excluded if x["row"] == 54)
    r54why = r54ex.get("reason") or r54ex.get("why", "")
    inv["I7_anchors"] = (
        ok7
        # r1 — 1. Griblje + jamarija + razvezana zveza 1956
        and "jamarija" in r1["month"] and "1956" in json.dumps(r1, ensure_ascii=False)
        # r26/r27 — DVOJČKA h24 (isti EMŠO datum!)
        and "DVOJČEK" in json.dumps(r26, ensure_ascii=False)
        and "DVOJČICA" in json.dumps(r27, ensure_ascii=False)
        # r37 — CIGANKA (1. etnična označba!)
        and "ciganka" in json.dumps(r37, ensure_ascii=False).lower()
        and "Hudorovac" in r37["mother"]
        # r41 — ZAPORED 3. LETO + † 9.11.1918
        and "zapored 3. leto" in json.dumps(r41, ensure_ascii=False).lower()
        # r54 excluded — begunec iz Renče
        and "begunec" in r54why.lower() and "Renč" in r54why
    )

    # I8 — EMŠO sidra (4 ZOOM-verified + popravki 2805/2207)
    ok8 = all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
              for row, EMSO in EMSO_ANCHOR_ROWS.items())
    inv["I8_emso_anchors"] = ok8

    # I9 — statistika: Učak ≥6, Jakofčič ×3, † otroci ≥3, vrzeli ≥2,
    # dup 0, excluded 43, struck 0, anomalij ≥14, deadInfants 23.6%
    bab = [e["babica"] or "" for e in entries]
    inv["I9_stats"] = (
        sum(1 for e in entries if "Učak" in (e["priest"] or "")) >= GRIBLJE_UCak
        and sum(1 for b in bab if "Jakofčič" in b) == GRIBLJE_JAKOFCIC
        and sum(1 for e in entries if any(("†" in n or "‡" in n or "MRTVOROJEN" in n) for n in e["notes"])) >= DEAD_CHILDREN_NOTE_MIN
        and sum(1 for e in entries if any("VRZEL" in n and "LET" in n for n in e["notes"])) >= 2
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and len(dokaz["stats"]["intraYearRepeats"]) == 1
        and "24" in dokaz["stats"]["intraYearRepeats"][0]
        and dokaz["excludedCount"] == EXPECTED_EXCLUDED
        and dokaz["frame"]["rowsStruck"] == EXPECTED_STRUCK
        and len(dokaz["anomalies"]) >= 14
        and "23.6%" in dokaz["stats"]["deadInfants"]
    )

    # I9b — P111 lead kontrola: p112Lead trdi 1917 r1 = GRIBLJE 45
    # Karol Feliks (razvezana 1956) → P112 POTRJUJE + P112 p113Lead
    # pripravljen (1918 glava s300 + r1 Boršt 49)
    ex1 = next(x for x in excluded if x["row"] == 2)
    inv["I9b_lead_control"] = (
        dokaz_p111["p112Lead"]["r1"].startswith("GRIBLJE 45")
        and dokaz_p111["p112Lead"]["r1"].startswith("GRIBLJE 45")
        and entries[0]["village"] == "Griblje" and entries[0]["houseNo"] == "45"
        and entries[0]["child"] == "Karol Feliks"
        and "1956" in json.dumps(entries[0], ensure_ascii=False)
        and dokaz["p113Lead"]["r1"].startswith("BORŠT 49")
        and "Karlovci" in dokaz["p113Lead"]["r1"]
    )

    # I10 — neodvisen preračun: vsi village == Griblje; sken→stran; vrstice
    ok10 = all(e["village"] == "Griblje" for e in entries)
    for e in entries:
        if page_of_scan(e["scan"]) != e["page"]:
            ok10 = False
    rows = sorted(e["row"] for e in entries)
    ok10 = ok10 and rows == sorted(rows) and len(rows) == len(set(rows))
    # 2 dvojčka para: r24/r25 (Otok 14) + r26/r27 (Griblje 24) v excluded/entries
    ex24 = next(x for x in excluded if x["row"] == 24)
    ex25 = next(x for x in excluded if x["row"] == 25)
    why24 = ex24.get("reason") or ex24.get("why", "")
    why25 = ex25.get("reason") or ex25.get("why", "")
    ok10 = ok10 and ex24["houseNo"] == "14" and ex25["houseNo"] == "14" \
        and "DVOJČEK" in why24 and "DVOJČEK" in why25
    inv["I10_independent_recalc"] = ok10

    # vitals skupaj 508 (496 + 12; vse tri knjige 04105+04894+04455)
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
