#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P110 — župnija Podzemelj: krstna knjiga 04105, polno leto 1915 (issue #18).

Razširitev vzorca P79 (1886) → … → P108 (1913) → P109 (1914) na leto 1915
(2. VOJNO leto; 81 vpisov — višje od 1914 = 78!). Okvir: glava »1915« ročno
na VRHU str. 225 = s269 (P109 lead POTRJEN); 1915 r1 = Škrilje 1 Janez
1./2. Januar; **r81 = rojstvo 30.12.1915 / krsta 4.1.1916 — čez mejo leta**
(EMŠO 3012915505170); **glava 1916 ročno »1916.« INLINE v ločilni starševski
celici str. 237 = s283** (zrcali tiskani »Leto« header) + tiskana glava
»Leto 1916« = vrh str. 238 = s284. == tiskane strani 225–237 == skeni
269–283 (15 skenov; 2 dup para: 270/271 + 273/274 — s271 DUP RAZKRIVA r13
Boršt 22, s270 pokrit z nalepko!).

**OFFSET PORAVNAVA str. 237 (5 celic = 5 vrstic + s284-B kontrola)** —
P111 lead POPRAVLJEN: 1916 r1 ← Matija Šapič × Katarina Novak (ne Copri!).

VSI vpisi z Griblji: **11 vpisov / 11 hiš — NARE 11/11 (10. čisto leto!)** +
**0 NOVIH hiš (2. leto zapored!)** + h53 ZAPORED 2. leto (1914+1915) +
**h78 VRZEL 27 LET = NOV REKORD vzorca!** (prej h53 16). Kumulativ s
P79–P109: **498 vpisov / 87 hiš / 30 let** (1886–1915; 490 vitals).

Sidra: r8 **GRIBLJE 88 Ivana** (P109 lead POTRJEN; starši Peter Brinec bajt.
× Ana **Butala** POPRAVLJENO; † 20.2.1915 [~]) + r16 **Griblje 70 Barbara**
(EMŠO 1603915505171 POPRAVLJENO; mati **PEZDIREC** POPRAVLJENO; oče 1883
POPRAVLJENO; marg. »mož umrl 1994« POPRAVLJENO) + r17 **Griblje 78 Jožefa**
(‡ 10.9.1917 — P109 lead 1916 ZAVRŽENO; **VRZEL 27 LET = REKORD!**) +
r48 **Griblje 13 Ana** (oče Matija **JAKOBČIČ** POPRAVLJENO; star 59!) +
r67 **Griblje 32 Marija** (EMŠO 0211915505717; botra Barbara **ŠTRUCELJ**;
11. VPIS!) + r69 **Griblje 46 Martin** (mati **MILEK**; **zakon
RAZVELJAVLJEN** sodba K 757/65-10 Karlovci 2.12.1965!) + r72 **Griblje 9
Neža** (oče **Oswald Jakobčič** POPRAVLJENO) + r74 **Griblje 22 Nikolaj**
(EMŠO 2511915500090; **MILEK ×2**; umrl 24.4.**1992** POPRAVLJENO) +
r78 **Griblje 53 Janez** (EMŠO 1812915500054; **DRAGOS**; ZAPORED!).

NOVELE 1915: **2 para dvojčkov** (r37/38 Boršt 23: oče ‡ Mihael Perdivec
† 28.3.1915 = MAREC — 2 meseca PRED rojstvom! roj. 22.11.1873 v OBEH
celicah — kolizija REŠENA; r46/47 Krasinec 18: **LATINSKE URE rojstva
»½ 7h ante meridiem« + »7h a.m.« — PRVE v vzorcu!**; oba dvojčka † 1915!)
+ **3 marginalije očetovstva** (r34 Janez Križan 4.2.1918 — **ISTI Križan =
oče r41!** + r43 Jožef Željko 15.8.1918 — poroka 6.1.1918 + r53 Josip
Jager 18.4.1917 — poroka ISTI DAN!) + **5 nezakonskih** (r34/r43/r53/r73/
r79) + **r49 PROTESTANT** (»evang. reform.«!) + **2 očeta † 1915** (r30
Daniel Jakša + r37/38 Perdivec) + **r40 RAZGLAŠEN ZA MRTVEGA** (oče
Ludovik Schweiger Kamnossek + botra Jakob Stipanič ŽUPAN!) + **NOVI KRAJI:
GRM (»Gm« ×3 — POTRJENO iz matičnega območja!) + BOGINJA vas** (register
»Božinja vas« ×2) + **NARE PRELOM Boginja vas 15 ×2** (r56 + r70 — 3.!) +
**UREJENOST PO KRSTI** (r12 krsta 3.3. = r11; prečrtan »April« = false
start!) + EMŠO kampanja ~38 = NAJVEČJA doslej.

DUHOVNIKI: **Učak ~59 DOMINANTA + Kapl. Bitnar ~21** (r1 podpis svinčnik
REŠEN). BABICA: **PILETIČ ~40/81 DOMINANTA — vrnitev!** (Jakofčič 9/11
Griblje; r72 Marija Jakobčič!). † 1915–1918 ~25% od 81 (VOJNA!).

Excluded: 70. Skripta scripts/p110_parish_baptism_1915.py (I1–I12, --check
izpiše PASS/FAIL in vrne exit code).
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
DOKAZ = "research/issue17/parish-baptism-1915.json"
DOKAZ_P109 = "research/issue17/parish-baptism-1914.json"
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (269, 283)        # 269 = str. 225 (glava 1915 ročno + r1–r9) – 283 = str. 237 (r80–r81 + glava 1916 + 1916 r1–r3)
FRAME_PAGES = (225, 237)
EXPECTED_ENTRIES = 11
EXPECTED_DISTINCT = 11          # NARE 11/11 — 10. čisto leto!
EXPECTED_EXCLUDED = 70
EXPECTED_STRUCK = 0
EXPECTED_HOUSES = sorted([9, 13, 22, 32, 40, 45, 46, 53, 70, 78, 88])
EXPECTED_VITALS_HOUSES = EXPECTED_HOUSES
EXPECTED_PT_IN_SET = ["9", "13", "22", "32", "40", "70", "78", "88"]
EXPECTED_PT_GAP = ["45", "46", "53"]  # v luknji 41–60 — vse tri dokazane v PT_GAP_KNOWN!
EXPECTED_NEW_HOUSES = 0         # 2. leto zapored!
EXPECTED_VITALS_TOTAL = 659  # POSODABLJENO P138: 490 (era) → 659 (P138!)
BLOCKS_04105 = 464              # 453 + 11
KUMULATIV_ENTRIES = 498         # 487 + 11
KUMULATIV_HOUSES = 87           # + 0
KUMULATIV_YEARS = 30            # 1886–1915
# kontinuitete (hiša → zadnje krstno leto pred 1915 v 04105, iz parish.ts)
CONTINUITY = {
    "9": 1913, "13": 1913, "22": 1912, "32": 1909, "40": 1912,
    "45": 1912, "46": 1913, "53": 1914, "70": 1912, "78": 1888, "88": 1910,
}
# sidra/pini P110 (row, scan, hiša, pin):
ANCHORS = [
    (8, 269, "88", "P109 lead POTRJEN"),
    (8, 269, "88", "Butala"),
    (8, 269, "88", "POPRAVLJENO"),
    (15, 270, "45", "Rajhmer"),
    (15, 270, "45", "25.7.1915"),
    (16, 270, "70", "1603915505171"),
    (16, 270, "70", "PEZDIREC"),
    (16, 270, "70", "POPRAVLJENO"),
    (17, 272, "78", "VRZEL 27 LET"),
    (17, 272, "78", "NOV REKORD"),
    (17, 272, "78", "1917"),
    (48, 277, "13", "JAKOBČIČ"),
    (48, 277, "13", "POPRAVLJENO"),
    (66, 280, "40", "23.6.1943"),
    (66, 280, "40", "Tuvan"),
    (67, 280, "32", "0211915505717"),
    (67, 280, "32", "ŠTRUCELJ"),
    (67, 280, "32", "11. VPIS"),
    (69, 281, "46", "MILEK"),
    (69, 281, "46", "RAZVELJAVLJENA"),
    (69, 281, "46", "župan"),
    (72, 281, "9", "Oswald JAKOBČIČ"),
    (72, 281, "9", "POPRAVLJENO"),
    (74, 282, "22", "2511915500090"),
    (74, 282, "22", "MILEK ×2"),
    (78, 282, "53", "1812915500054"),
    (78, 282, "53", "ZAPORED 2. LETO"),
    (78, 282, "53", "DRAGOS"),
]
EMSO_ANCHOR_ROWS = {
    16: "1603915505171",
    67: "0211915505717",
    74: "2511915500090",
    78: "1812915500054",
}
GRIBLJE_JAKOFCIC = 9            # 9/11 babica Marija Jakofčič (r72 = Marija Jakobčič!)
GRIBLJE_UCak = 8                # jasni podpisi Učak ≥8
GRIBLJE_BITNAR = 2              # jasni podpisi Bitnar ≥2 (r16/r69/r78)
GRIBLJE_DOJENCKI_UMRLI = 5      # r8 + r15 + r17 (1917) + r72 (1916) + r66 (1943) marginalia †


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
    """P110: 2 dup para (270/271=226, 273/274=228); ostali enojni."""
    return {269: 225, 270: 226, 271: 226, 272: 227, 273: 228, 274: 228,
            275: 229, 276: 230, 277: 231, 278: 232, 279: 233, 280: 234,
            281: 235, 282: 236, 283: 237}.get(scan)


def verify():
    inv = {}

    st, body = http_get(BOOK_URL, UA)
    inv["I1_book_page_200"] = st == 200
    urls = decode_inventory(body.decode("utf-8", "replace")) if st == 200 else []
    inv["I2_inventory_326"] = len(urls) == EXPECTED_IMAGES

    dokaz = json.load(open(DOKAZ, encoding="utf-8"))
    dokaz_p109 = json.load(open(DOKAZ_P109, encoding="utf-8"))
    entries = dokaz["entries"]
    excluded = dokaz["excluded"]
    houses = [e["houseNo"] for e in entries]
    houses_numeric = [h for h in houses if h.isdigit()]

    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    # I3 — okvir: citirani skeni + stran==sken + 2 dup para + glava 1916 inline + r81 čez mejo
    cited = sorted({e["scan"] for e in entries})
    inv["I3_frame"] = (
        cited == sorted(set(cited)) and set(cited) <= set(range(269, 284))
        and all(page_of_scan(s) == p for s, p in ((e["scan"], e["page"]) for e in entries))
        and dokaz["frame"]["rowsTotal"] == 81
        and dokaz["frame"]["rowsStruck"] == 0
        and len(dokaz["frame"]["dupPari"]) == 2
        and dokaz["frame"]["dupPari"] == [[270, 271], [273, 274]]
        and dokaz["frame"]["scans"] == [269, 283]
        and dokaz["frame"]["pages"] == [225, 237]
        and "1916" in dokaz["frame"]["rowsNote"]
        and "4. januar 1916" in json.dumps(next(x for x in excluded if x["row"] == 81), ensure_ascii=False)
    )

    # I4 — 11 vpisov / 11 hiš (NARE 11/11!) + hiše + vitals hiše
    hv = parish_vitals_04105()
    hv1915 = [b for b in hv if b["year"] == 1915]
    inv["I4_nare_houses"] = (
        len(entries) == EXPECTED_ENTRIES
        and len(set(houses)) == EXPECTED_DISTINCT
        and sorted(int(h) for h in set(houses_numeric)) == EXPECTED_HOUSES
        and sorted(int(b["houseNo"]) for b in hv1915 if b["houseNo"]) == EXPECTED_VITALS_HOUSES
    )

    # I5 — kontinuiteta: CONTINUITY iz dokaza se sklada s parish.ts
    ok5 = True
    for hn, last_year in CONTINUITY.items():
        ys = [b["year"] for b in hv if b["houseNo"] == hn and b["year"] < 1915]
        if not ys or max(ys) != last_year:
            ok5 = False
    inv["I5_continuity"] = ok5

    # I5b — 0 novih hiš: vsaka 1915 hiša ima zgodnejše vpise v 04105 + h78 vrzel 27
    ok5b = all(
        any(b["houseNo"] == hn and b["year"] < 1915 for b in hv)
        for hn in set(houses_numeric)
    )
    inv["I5b_no_new_houses"] = ok5b and dokaz["stats"]["newSampleHouses"] == 0

    # I6 — PT klasifikacija: 11/11 v naboru; 0 novih; kumulativ 498/87/30
    pts = pt_house_set()
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_set = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inset = sorted((h for h in set(houses_numeric) if h in pts), key=int)
    gap = sorted((h for h in set(houses_numeric) if h not in pts), key=int)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == EXPECTED_PT_GAP
        and dokaz["stats"]["pt"] == "8/3 (h45 + h46 + h53 v luknji 41–60 — vse tri dokazane v PT_GAP_KNOWN!)"
        and all(f'"{x}"' in pt_gap_set for x in ("45", "46", "53"))
        and dokaz["stats"]["newHouseNos"] == []
        and dokaz["stats"]["cumulative"] == "498 vpisov / 87 hiš / 30 let (1886–1915)"
        and dokaz["stats"]["vitals"] == EXPECTED_VITALS_TOTAL
    )

    # I7 — sidra (28 pinov na Gribljih)
    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r8 = e_by_row(8)
    r16 = e_by_row(16)
    r17 = e_by_row(17)
    r48 = e_by_row(48)
    r69 = e_by_row(69)
    r74 = e_by_row(74)
    r78 = e_by_row(78)
    inv["I7_anchors"] = (
        ok7
        # r8 — P109 lead POTRJEN + Butala POPRAVLJENO + † 20.2.1915
        and "P109 lead POTRJEN" in json.dumps(r8, ensure_ascii=False)
        and "Butala" in r8["mother"] and "20.2.1915" in json.dumps(r8, ensure_ascii=False)
        # r16 — mati PEZDIREC (ne Perdivec!) + EMŠO 5505171 + oče 1883 + mož 1994
        and "roj. PEZDIREC" in r16["mother"] and "»Perdivec« POPRAVLJENO" in r16["mother"]
        and "1603915505171" in json.dumps(r16, ensure_ascii=False)
        and "1883" in r16["father"]
        # r17 — ‡ 1917 (lead 1916 ZAVRŽENO) + VRZEL 27 LET
        and "1917" in json.dumps(r17, ensure_ascii=False) and "VRZEL 27 LET" in " ".join(r17["notes"])
        # r48 — oče JAKOBČIČ (ne Jaklič!)
        and "Matija JAKOBČIČ" in r48["father"] and "»Jaklič/Jakličič« POPRAVLJENO" in r48["father"]
        # r69 — mati MILEK + zakon RAZVELJAVLJEN + boter župan
        and "Milek" in r69["mother"] and "RAZVELJAVLJENA" in json.dumps(r69, ensure_ascii=False)
        and "župan" in r69["botra"]
        # r74 — umrl 24.4.1992 (POPRAVLJENO iz 1932) + MILEK ×2
        and "1992" in json.dumps(r74, ensure_ascii=False) and "MILEK ×2" in json.dumps(r74, ensure_ascii=False)
        # r78 — DRAGOS + ZAPORED 2. LETO
        and "DRAGOS" in json.dumps(r78, ensure_ascii=False) and "ZAPORED 2. LETO" in json.dumps(r78, ensure_ascii=False)
    )

    # I8 — EMŠO sidra (4 SKLADNA: r16/r67/r74/r78)
    ok8 = all(EMSO in json.dumps(e_by_row(row), ensure_ascii=False)
              for row, EMSO in EMSO_ANCHOR_ROWS.items())
    inv["I8_emso_anchors"] = ok8

    # I9 — statistika: babica Jakofčič 9/11, Učak ≥8, Bitnar ≥2,
    # dojenčki/otrok † ≥5, vrzeli, dup 2, excluded 70, struck 0
    bab = [e["babica"] or "" for e in entries]
    inv["I9_stats"] = (
        sum(1 for b in bab if "Jakofčič" in b) == GRIBLJE_JAKOFCIC
        and sum(1 for e in entries if "Učak" in (e["priest"] or "")) >= GRIBLJE_UCak
        and sum(1 for e in entries if "Bitnar" in (e["priest"] or "")) >= GRIBLJE_BITNAR
        and sum(1 for e in entries if any("†" in n or "‡" in n or "1916" in n or "1917" in n for n in e["notes"])) >= GRIBLJE_DOJENCKI_UMRLI
        and sum(1 for e in entries if any("VRZEL" in n and "LET" in n for n in e["notes"])) >= 9
        and dokaz["stats"]["babica"].startswith("PILETIČ")
        and dokaz["stats"]["entries"] == 11
        and dokaz["stats"]["distinctHouses"] == 11
        and dokaz["stats"]["intraYearRepeats"] == 0
        and dokaz["excludedCount"] == EXPECTED_EXCLUDED
        and dokaz["frame"]["rowsStruck"] == EXPECTED_STRUCK
        and len(dokaz["anomalies"]) >= 18
    )

    # I9b — P109 lead popravek: P109 p110Lead trdi r17 †10.9.1916 → P110 dokaz
    # r17 ‡ 1917 (ZAVRŽENO) + r8 GRIBLJE 88 Ivana POTRJEN + OFFSET poravnava (P111 lead)
    inv["I9b_lead_correction"] = (
        dokaz_p109["p110Lead"]["r17"].startswith("Griblje 78? Jožef")
        and "1916" in dokaz_p109["p110Lead"]["r17"]
        and "1917" in json.dumps(r17, ensure_ascii=False)
        and r8["houseNo"] == "88" and r8["child"] == "Ivana"
        and dokaz["p111Lead"]["r1"].startswith("Grišiče 3")
        and "Šapič" in dokaz["p111Lead"]["r1"]
        and "OFFSET" in json.dumps(next(x for x in excluded if x["row"] == 81), ensure_ascii=False).upper()
    )

    # I10 — neodvisen preračun: vsi village == Griblje; sken→stran; vrstice
    ok10 = all(e["village"] == "Griblje" for e in entries)
    for e in entries:
        if page_of_scan(e["scan"]) != e["page"]:
            ok10 = False
    rows = sorted(e["row"] for e in entries)
    ok10 = ok10 and rows == sorted(rows) and len(rows) == len(set(rows))
    inv["I10_independent_recalc"] = ok10

    # vitals skupaj 490 (479 + 11; vse tri knjige 04105+04894+04455)
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
