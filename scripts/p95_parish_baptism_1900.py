#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P95 — župnija Podzemelj: krstna knjiga 04105, polno leto 1900 (issue #18).

Razširitev vzorca P79 (1886) → … → P93 (1898) → P94 (1899) na leto 1900:
okvir skeni 118 (row 105 na str. 115 — SREDINA strani, P94 dokazano) – 124
(row 77) == strani 115–121 (stran == sken − 3, novela P92; sken 125 = str.
122 = glava 1901). 77 oštevilčenih vrstic. STRUKTURA: sken 121 = DVA
podatkovna panela (r33–44 + r45–56), sken 122 = DVA starševska panela;
vrstice 51–56 FIZIČNO RAZTRGANE (podatki izgubljeni, starši znani). 16
vpisov / 16 hiš — NARE (7. leto) — 2. leto brez znotraj-letnih ponovitev.
NOVA HIŠA h67 (prvi matrični dokaz; PT nabor 1825 — 61–99 blok; Straus
gumbar). scoping POPRAVKI: r5→r3, r8→r6 (margini str. 115 raztrgani — 8
vrstic, BREZ anomalije), r27→r28…r30→r31 (scoping izpustil r27 Otok 8);
4 izpuščene vrstice najdene (r45 h16, r46 h58, r59 h31, r63 h25); scopingov
r49 »Griblje 51 NOVA LUKNJA« = NAPAČEN (Primostek 5) — luknja 42/50/51
nespremenjena. NOVELA babica: stolpec PRVIČ izpolnjen (Fottre 7× + Hrižan +
Mavrenfič + Grabrijan; 1886–99 prazen). Duhovniki: Šturm 0× (PRVIČ!), Rauq
9× + Perg? 4× + Klunček? 2×. h1 ŽELJKO VRNITEV (Jurij = boter 1888 → oče
1900); h31 6. pin Papič × Straus; h45 3. pin Straus × Spudič (04455);
h90 4. pin Vetročnik × Schmelzer (Leopoldina po materi); h23 4. pin Brinec ×
Dehlič (1893 »Debič?« rešeno); h14 Janez Brinec (reši 1896); h58 NOVA ŽENA
Kranbič; h32 Meh (Kurrent U/M dvom). EMŠO konflikt r30 (vrstica »40 jun« vs
EMŠO 24.05.1900). Dojenčijska umrljivost 5/16.

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
DOKAZ = "research/issue17/parish-baptism-1900.json"
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
PARISH_TS = "src/data/atlas/parish.ts"
ATLAS_TS = "src/lib/atlas.ts"
PT_CHAIN = "research/issue13/chain-full-pt-ps.json"

FRAME_SCANS = (118, 124)        # skeni 118 (row 105 na str. 115) – 124 (row 77) == str. 115–121
FRAME_PAGES = (115, 121)
NEXT_YEAR_SCAN = 125            # sken 125 = str. 122 = glava 1901 (samo okvir)
EXPECTED_ENTRIES = 16
EXPECTED_DISTINCT = 16          # 16 vpisov / 16 hiš (NARE, brez ponovitev — 2. leto)
EXPECTED_EXCLUDED = 4           # r15 Okljuka + r49 napačen lead + r50 vas raztrgana + r51–56 raztrgane
EXPECTED_CITED = [118, 119, 120, 121, 122, 123, 124]  # 122 = starši r45/r46 (citiran brez data vpisov)
DATA_SCANS = [118, 119, 120, 121, 123, 124]
EXPECTED_PT_IN_SET = ["1", "9", "10", "14", "16", "20", "23", "25", "31", "32", "65", "67", "90"]
EXPECTED_PT_GAP = ["45", "54", "58"]  # 41–60 luknja (vsi trije že dokazani prej — ni novih številk)
EXPECTED_NEW_HOUSES = ["67"]    # h67 NOVA (PT nabor 1825); h51 NE (scoping r49 zavrnjen)
EXPECTED_REPEATS = 15           # 16 hiš − 1 nova
EXPECTED_HOUSES_VITALS = 16
EXPECTED_VITALS_TOTAL = 264     # HOUSE_VITALS 238 + 16 (P95: krstna 1900)
EV_ONLY_TOTAL = 6               # P84: 2 + P85: 3 + P86: 1 (P77–P83, P87–P95: 0)
EV_ONLY_HOUSE_STRINGS = {"65 [~]"}  # P85 — edina imenovana EV-only hiša
EXPECTED_PRIESTS = (0, 9)       # (Šturm, Rauq) + Perg 4 + Klunček 2 + 1 neberljiv
EXPECTED_INFANT_DEATHS = 5      # r3 † 1907 + r23 † 2/6.00 + r45 † 7/11.02 + r46 † 8/5.03 + r69 † 9/2.03
MIDWIFE_EMPTY = 6               # »—« (r3, r6, r10, r19, r23, r30)
MIDWIFE_NAMED = 8               # NOVELA: prvič izpolnjeno (Fottre 7× + Hrižan 1×)
# sidra/pini P95 (row, scan, hiša, očetovski/maternalni pin):
ANCHORS = [
    (3, 118, "1", "Željko"),
    (6, 118, "67", "Straus"),
    (10, 119, "10", "Grabrijan"),
    (19, 119, "32", "Meh"),
    (23, 120, "65", "Milek"),
    (28, 120, "20", "Pendirec"),
    (29, 120, "14", "Brinec"),
    (30, 120, "90", "Vetročnik"),
    (31, 120, "23", "Brinec"),
    (34, 121, "9", "Muc"),
    (43, 121, "54", "RAZTRGANO"),
    (45, 121, "16", "Novak"),
    (46, 121, "58", "Požek"),
    (59, 123, "31", "Papič"),
    (63, 123, "25", "Brinec"),
    (69, 124, "45", "Straus"),
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
    """NOVELA P92: od skena 98 stran == sken − 3 — velja za vse citirane
    skene 1900 (118–124), brez novih duplikatov."""
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

    # I3 — citirani skeni ⊆ okvir 118–124 + JPEG probe; sken 125 NI citiran
    # (glava 1901 — samo okvir); sken 122 citiran za starše r45/r46
    cited = sorted({e["scan"] for e in entries})
    inv["I3_data_scans_in_frame"] = all(
        FRAME_SCANS[0] <= s <= FRAME_SCANS[1] for s in cited
    ) and set(cited) <= set(DATA_SCANS)
    probes = {s: probe_jpeg(urls[s - 1]) for s in EXPECTED_CITED} if urls else {}
    inv["I3_jpeg_probes"] = all(p["http"] == 200 and p["jpeg"] for p in probes.values())
    inv["I3_cited_scans"] = dokaz["source"]["citedScans"] == EXPECTED_CITED

    # I4 — okvir: vsi vpisi 1900; stran == sken − 3 (novela P92 za celo leto);
    # brez duplikatov; 1900 r1 na SREDINI str. 115 (sken 118 pageRow 105,
    # P94 dokazano); rowsTotal 77; 1900 row 1 = Krasinec; sken 121 = 2 data
    # panela + sken 122 = 2 parents panela; r51–56 raztrgane
    rows = [e["row"] for e in entries]
    fr = dokaz["frame"]
    spread = fr["spreadStructure"]["scans"]
    inv["I4_frame_year_rows"] = (
        all(e["year"] == 1900 for e in entries)
        and all(e["page"] == page_of_scan(e["scan"]) for e in entries)
        and all(FRAME_SCANS[0] <= e["scan"] <= FRAME_SCANS[1] for e in entries)
        and all(FRAME_PAGES[0] <= e["page"] <= FRAME_PAGES[1] for e in entries)
        and rows == sorted(rows)
        and len(set(rows)) == len(rows)
        and fr["yearStart"]["scan"] == 118 and fr["yearStart"]["page"] == 115
        and fr["yearStart"]["pageRow"] == 105 and fr["yearStart"]["row"] == 1
        and fr["yearEnd"]["scan"] == 124 and fr["yearEnd"]["page"] == 121 and fr["yearEnd"]["row"] == 77
        and fr["rowsTotal"] == 77
        and dokaz["source"]["duplicateScan"] is None
        and "sredini str. 115" in fr["yearStart"]["note"]
        and "Krasinec" in fr["yearStart"]["note"]
        and "Božanja vas 15" in fr["yearEnd"]["note"]
        and "sken − 3" in fr["pageOfScan"]
        and spread["121"].count("r33") == 1 and spread["121"].count("r45–r56") == 1
        and "podatki r45–r56" in spread["121"]
        and "starši r33–r44" in spread["122"] and "starši r45–r56" in spread["122"]
        and "RAZTRGANE" in spread["121"]
        and fr["numbering"]["note"].count("BREZ ANOMALIJE") == 1
        and "ZAVRŽENA" in fr["numbering"]["note"]
        and next(e for e in entries if e["row"] == 3)["scan"] == 118
        and next(e for e in entries if e["row"] == 45)["scan"] == 121
        and next(e for e in entries if e["row"] == 46)["scan"] == 121
    )

    # I5 — števec: 16 vpisov / 16 hiš; 0 neberljivih hiš; NARE brez ponovitev
    # (2. leto); NOVELA babica: stolpec prvič izpolnjen (8 imenovanih + 6 praznih
    # + 2 neberljivih); 4 izključeni (Okljuka + napačen r49 + r50 + r51–56);
    # h51 NE dokazana (scoping r49 zavrnjen)
    houses = [e["houseNo"] for e in entries]
    bab_named = sum(1 for e in entries if not e["babica"].startswith("—") and "RAZTRGANO" not in e["babica"] and "neberljivo" not in e["babica"])
    bab_empty = sum(1 for e in entries if e["babica"].startswith("—"))
    inv["I5_counts"] = (
        len(entries) == EXPECTED_ENTRIES
        and all(e["village"].startswith("Griblje") for e in entries)
        and len(set(houses)) == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and dokaz["stats"]["intraYearRepeats"] == 0
        and bab_empty == MIDWIFE_EMPTY
        and bab_named == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeNamed"] == MIDWIFE_NAMED
        and dokaz["stats"]["midwifeEmpty"] == MIDWIFE_EMPTY
        and len(excluded) == EXPECTED_EXCLUDED
        and "NE GRIBLJE" in excluded[0]["reason"]
        and "Okljuka" in excluded[0]["reason"]
        and "NE GRIBLJE" in excluded[1]["reason"]
        and "Primostek 5" in excluded[1]["reason"]
        and "NAPAČEN" in excluded[1]["reason"]
        and "h51 NE dokazana" in excluded[1]["notes"]
        and "RAZTRGANI" in excluded[2]["reason"]
        and "Šegina" in excluded[2]["reason"]
        and "51–56" in str(excluded[3]["row"])
        and "NEBERLJIVI" in excluded[3]["reason"].upper()
        and "Katarina Hrižan" in excluded[3]["notes"]
    )

    # I6 — PT klasifikacija: 13 v naboru + 3 v luknji (45/54/58 — vsi že dokazani);
    # h58 NI v PT verigi (PT_GAP_KNOWN že vsebuje 58); NOVA HIŠA h67 (PT nabor);
    # h51 NE (luknja 42/50/51 nespremenjena, 19); kumulativ 260/80;
    # atlas.ts PT_GAP_KNOWN brez 51 (nespremenjen)
    pts = pt_house_set()
    inset = sorted((h for h in set(houses) if h in pts), key=int)
    gap = sorted((h for h in set(houses) if h not in pts), key=int)
    atlas_src = open(ATLAS_TS, encoding="utf-8").read()
    pt_gap_known = re.search(r"PT_GAP_KNOWN = new Set\(\[[^\]]*\]\)", atlas_src).group(0)
    inv["I6_pt_classification"] = (
        inset == sorted(EXPECTED_PT_IN_SET, key=int)
        and gap == sorted(EXPECTED_PT_GAP, key=int)
        and dokaz["stats"]["ptGap"] == EXPECTED_PT_GAP
        and dokaz["stats"]["ptInNabor"] == 13
        and dokaz["stats"]["newSampleHouses"] == 1
        and dokaz["stats"]["newGapCount"] == 19
        and dokaz["stats"]["cumulative"]["entries"] == 260
        and dokaz["stats"]["cumulative"]["houses"] == 80
        and '"49"' in pt_gap_known          # obstoječe luknje ostanejo
        and '"51"' not in pt_gap_known      # h51 NE dokazana — NE sme biti dodana
        and '"42"' not in pt_gap_known and '"50"' not in pt_gap_known
    )

    # I7 — sidra (16 vpisov — očetovski pini + oznake)
    def e_by_row(row):
        return next(e for e in entries if e["row"] == row)

    ok7 = True
    for row, scan, hn, pin in ANCHORS:
        e = e_by_row(row)
        blob = json.dumps(e, ensure_ascii=False)
        if not (e["houseNo"] == hn and e["scan"] == scan and pin in blob):
            ok7 = False
    r3 = e_by_row(3)
    r6 = e_by_row(6)
    r19 = e_by_row(19)
    r28 = e_by_row(28)
    r29 = e_by_row(29)
    r30 = e_by_row(30)
    r31 = e_by_row(31)
    r34 = e_by_row(34)
    r43 = e_by_row(43)
    r45 = e_by_row(45)
    r46 = e_by_row(46)
    r59 = e_by_row(59)
    r63 = e_by_row(63)
    r69 = e_by_row(69)
    inv["I7_anchors"] = (
        ok7
        # r3 — ŽELJKO VRNITEV (h1)
        and "ŽELJKO VRNITEV" in json.dumps(r3["notes"], ensure_ascii=False)
        and "BOTER h1 1888" in json.dumps(r3["notes"], ensure_ascii=False)
        and "Kure" in r3["mother"]
        # r6 — NOVA HIŠA h67 (Straus gumbar)
        and "NOVA HIŠA" in json.dumps(r6["notes"], ensure_ascii=False)
        and "prvi matrični dokaz" in json.dumps(r6["notes"], ensure_ascii=False)
        and "Jakopič" in r6["mother"]
        and "1002900505074" in json.dumps(r6["notes"], ensure_ascii=False)
        # r19 — Meh/Urh + prečrtana mati + raztrgani dnevi
        and "KURRENT U/M" in json.dumps(r19["notes"], ensure_ascii=False)
        and "PREČRTANO" in r19["mother"].upper()
        and "[raztrgano]" in r19["born"]
        and "Straus" in r19["botra"]
        # r28 — Pendirec × Klepec 3. pin + Terin
        and "2. VPIS ISTA ZVEZA" in json.dumps(r28["notes"], ensure_ascii=False)
        and "Klepec" in r28["mother"]
        # r29 — Janez Brinec reši 1896 (P91 MERI dvom)
        and "REŠUJE P91" in json.dumps(r29["notes"], ensure_ascii=False)
        # r30 — šolska hiša, Vetročnik × Schmelzer, EMŠO konflikt
        and "UČITELJ" in r30["father"]
        and "Schmelzer" in r30["mother"]
        and "KONFLIKT DATUMA" in json.dumps(r30["notes"], ensure_ascii=False)
        and "2405900505109" in json.dumps(r30["notes"], ensure_ascii=False)
        and "po materi Leopoldi" in json.dumps(r30["notes"], ensure_ascii=False)
        # r31 — Brinec × Dehlič 4. pin (1893 rešeno)
        and "Brinec × Dehlič" in json.dumps(r31["notes"], ensure_ascii=False)
        and "4. PIN ISTA ZVEZA" in json.dumps(r31["notes"], ensure_ascii=False)
        and "Dehlič" in r31["mother"]
        # r34 — Muc × Kure, svinčnik
        and "MENJAVA" in json.dumps(r34["notes"], ensure_ascii=False)
        and "Štumer" in json.dumps(r34["notes"], ensure_ascii=False)
        # r43 — starši raztrgani
        and "RAZTRGANO" in r43["father"] and "RAZTRGANO" in r43["mother"]
        # r45/r46 — izpuščeni s strani scopinga
        and "IZPUSTIL" in json.dumps(r45["notes"], ensure_ascii=False)
        and "IZPUSTIL" in json.dumps(r46["notes"], ensure_ascii=False)
        and "Šilak" in r45["mother"]
        and "Kranbič" in r46["mother"] and "NOVA ŽENA" in r46["mother"]
        # r59 — Papič × Straus 6. pin
        and "6. PIN ISTA ZVEZA" in json.dumps(r59["notes"], ensure_ascii=False)
        and "Straus" in r59["mother"]
        # r63 — Brinec × Segina + babica Hrižan
        and "Segina" in r63["mother"] and "Šegina" in r63["botra"]
        and "Hrižan" in r63["babica"]
        # r69 — Straus × Spudič 3. pin + 04455
        and "Spudič" in r69["mother"] and "Straus" in r69["father"]
        and "04455" in json.dumps(r69["notes"], ensure_ascii=False)
        and "3. PIN ISTA ZVEZA" in json.dumps(r69["notes"], ensure_ascii=False)
    )

    # I8 — čez-letne kontinuitete prek dokazov:
    # h1 (P83 1888/92/96 Željko × Kure + P94 1899 Segina → P95 VRNITEV Željko)
    # h31 (P82 1887 + P85 1890 + P89 1894 + P92 1897 Papič × Straus → P95 6. pin)
    # h45 (P91 1896 + P92 1897 Straus × Spudič → P95 3. pin)
    # h90 (P85 1890 + P87 1892 Kopitar + P93 1898 Vetročnik × Schmelzer → P95 4. pin ista družina)
    # h23 (P88 1893/94 + P92 1897 Brinec → P95 4. pin; Debič→Dehlič)
    # h20 (P90 1895 + P92 1897 Pendirec × Klepec → P95 3. pin)
    # h58 (P81 1889 + P82 1890/92 + P90 1895 Požek → P95 5. pin + nova žena)
    # h32 (P84 1889 Urh + P85 1890 + P87 1892 + P88 1893 Meh/Mrh + P92 1897 + P93 1898 → P95 8. pin Meh)
    # h65 (P82 1887 + P84 1889 + P88 1893 + P90 1895 + P92 1897 Milek → P95 6. pin)
    # h14 (P91 1896 Janez Brinec MERI dvom »ali drug?« → P95 forenzika REŠUJE)
    # h67 NOVA (ni priorja); h9 (P91 1896 Jakobič? → P95 MENJAVA Muc × Kure)
    p82 = json.load(open(DOKAZ_P82, encoding="utf-8"))
    p83 = json.load(open(DOKAZ_P83, encoding="utf-8"))
    p84 = json.load(open(DOKAZ_P84, encoding="utf-8"))
    p85 = json.load(open(DOKAZ_P85, encoding="utf-8"))
    p87 = json.load(open(DOKAZ_P87, encoding="utf-8"))
    p88 = json.load(open(DOKAZ_P88, encoding="utf-8"))
    p89 = json.load(open(DOKAZ_P89, encoding="utf-8"))
    p90 = json.load(open(DOKAZ_P90, encoding="utf-8"))
    p91 = json.load(open(DOKAZ_P91, encoding="utf-8"))
    p92 = json.load(open(DOKAZ_P92, encoding="utf-8"))
    p93 = json.load(open(DOKAZ_P93, encoding="utf-8"))
    p94 = json.load(open(DOKAZ_P94, encoding="utf-8"))

    def hs(d, h):
        return [e for e in d["entries"] if str(e.get("houseNo")) == h]

    def blob(d, h):
        return json.dumps(hs(d, h), ensure_ascii=False)

    inv["I8_continuity"] = (
        # h1: 1888/92/96 Željko × Kure → 1899 Segina → 1900 Željko (vrnitev)
        len(hs(p83, "1")) >= 1 and ("Željko" in blob(p83, "1") or "Zeljth" in blob(p83, "1")) and "Kure" in blob(p83, "1")
        and len(hs(p87, "1")) >= 1 and len(hs(p91, "1")) >= 1
        and len(hs(p94, "1")) >= 1 and "Segina" in blob(p94, "1")
        and len(hs(p83, "1")) >= 1 and "Jurij Zeljth" in blob(p83, "1")  # boter 1888
        # h31: Papič × Straus 1887+1890+1894+1897 → 1900 (6. pin)
        and len(hs(p82, "31")) >= 1 and "Papič" in blob(p82, "31") and "Straus" in blob(p82, "31")
        and len(hs(p85, "31")) >= 1 and len(hs(p89, "31")) >= 1 and len(hs(p92, "31")) >= 1
        # h45: Straus × Spudič 1896+1897 → 1900 (3. pin)
        and len(hs(p91, "45")) >= 1 and "Straus" in blob(p91, "45")
        and len(hs(p92, "45")) >= 1 and "Spudič" in blob(p92, "45")
        # h90: Kopitar 1890/92 → Vetročnik × Schmelzer 1898+1900
        and len(hs(p85, "90")) >= 1 and "Kopitar" in blob(p85, "90")
        and len(hs(p93, "90")) >= 1 and "Vetročnik" in blob(p93, "90") and "Schmelzer" in blob(p93, "90")
        # h23: Brinec 1893/94/97 → 1900; Debič → Dehlič
        and len(hs(p88, "23")) >= 1 and "Brinec" in blob(p88, "23") and "Debič" in blob(p88, "23")
        and len(hs(p92, "23")) >= 1
        # h20: Pendirec × Klepec 1897 → 1900
        and len(hs(p92, "20")) >= 1 and "Pendirec" in blob(p92, "20") and "Klepec" in blob(p92, "20")
        # h58: Požek 1889/1890/92/95 → 1900; Dragoš → Kranbič
        and len(hs(p84, "58")) >= 1 and "Požek" in blob(p84, "58") and "Dragoš" in blob(p84, "58")
        and len(hs(p90, "58")) >= 1 and "Dragoš" in blob(p90, "58")
        # h32: Urh/Meh 1889–1898 → 1900 Meh
        and len(hs(p84, "32")) >= 1 and "Urh" in blob(p84, "32")
        and len(hs(p88, "32")) >= 1 and "Meh" in blob(p88, "32")
        and len(hs(p93, "32")) >= 1
        # h65: Milek 1887–1897 → 1900
        and len(hs(p82, "65")) >= 1 and "Milek" in blob(p82, "65")
        and len(hs(p92, "65")) >= 1
        # h14: 1896 Janez Brinec MERI dvom → 1900 forenzika rešuje
        and len(hs(p91, "14")) >= 1 and "Brinec" in blob(p91, "14")
        # h9: 1896 Jakobič? → 1900 MENJAVA Muc × Kure
        and len(hs(p91, "9")) >= 1 and "Jakobič" in blob(p91, "9")
        # h67: NOVA — brez priorja v vseh dokazih
        and all(len(hs(d, "67")) == 0 for d in (p82, p83, p84, p85, p87, p88, p89, p90, p91, p92, p93, p94))
        # scoping r49 zavrnjen: h51 NE v P95 entries
        and all(str(e.get("houseNo")) != "51" for e in entries)
    )

    # I9 — vitals projekcija: 16 zasidranih 1900 (04105); vsi skeni v okviru;
    # stran == sken − 3; vitals skupaj 254
    vitals_1900 = parish_vitals(BOOK_SIGNATURE, 1900)
    vitals_all = sum((parish_vitals(s) for s in ("04105", "04894", "04455")), [])
    inv["I9_vitals_projection"] = (
        len(vitals_1900) == EXPECTED_HOUSES_VITALS
        and sorted(v["houseNo"] for v in vitals_1900) == sorted(houses)
        and all(v["scan"] and 118 <= v["scan"] <= 124 for v in vitals_1900)
        and all(v["page"] == page_of_scan(v["scan"]) for v in vitals_1900)
        and len(vitals_all) == EXPECTED_VITALS_TOTAL
    )

    # I10 — statistika dokaza == neodvisen preracun: 15 ponovitev + 1 nova (67);
    # kumulativ 254 + 6 EV-only == 260; hiše vitals 79; duhovniki (Šturm, Rauq)
    # = (0, 9) + Perg 4 + Klunček 2 + 1 neberljiv; † 5; nezakonski 0
    # klasifikacija v P95 vesolju — kasnejši blok (1901 P96) NE sme spreminjati
    # zgodovinske klasifikacije leta 1900 (filtri vesolja)
    vitals_pre1901 = [
        v for v in vitals_all
        if not (v["bookSignature"] == BOOK_SIGNATURE and v["year"] == 1901)
    ]
    repeat_houses = sorted(
        (h for h in set(houses) if any(
            (v["houseNo"] == h and v["bookSignature"] == BOOK_SIGNATURE and v["year"] != 1900)
            or (v["houseNo"] == h and v["bookSignature"] != BOOK_SIGNATURE)
            for v in vitals_pre1901
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
    n_sturm = sum(1 for e in entries if "Šturm" in e["priest"])
    n_rauq = sum(1 for e in entries if "Rauq" in e["priest"])
    n_perg = sum(1 for e in entries if "Perg" in e["priest"])
    n_kluncek = sum(1 for e in entries if "Klunček" in e["priest"])
    n_infant = sum(1 for e in entries if any("†" in n for n in e["notes"]))
    inv["I10_stats_independent"] = (
        len(repeat_houses) == EXPECTED_REPEATS
        and new_houses == EXPECTED_NEW_HOUSES
        and dokaz["stats"]["newSampleHouses"] == 1
        and n_entries_total == EXPECTED_VITALS_TOTAL
        and n_entries_total + EV_ONLY_TOTAL == 270  # kumulativno po P95 (254 + 6)
        and n_houses_total == 80  # P94: 78; P95: + 1 (67)
        and ev_only_houses == EV_ONLY_HOUSE_STRINGS
        and cumulative["entries"] == 260
        and cumulative["houses"] == 80  # 79 vitals + 1 EV-only »65 [~]« (zamrznjeno P95)
        and dokaz["stats"]["entries"] == EXPECTED_ENTRIES
        and dokaz["stats"]["distinctHouses"] == EXPECTED_DISTINCT
        and dokaz["stats"]["housesIllegible"] == 0
        and len(entries) == 16 and len(excluded) == 4
        and (n_sturm, n_rauq) == EXPECTED_PRIESTS
        and n_perg == 4 and n_kluncek == 2
        and n_infant == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["illegitimate"] == 0
        and dokaz["stats"]["infantDeaths"] == EXPECTED_INFANT_DEATHS
        and dokaz["stats"]["priests"]["Šturm"] == 0
        and dokaz["stats"]["priests"]["Rauq"] == 9
    )

    ok = all(inv.values())
    print("P95 — krstna knjiga 04105, polno leto 1900 (issue #18)")
    for k, v in inv.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"invarianti: {ok}")
    print(f"knjiga {BOOK_SIGNATURE}: slike {len(urls)} (pričakovano {EXPECTED_IMAGES});"
          f" citirani skeni {EXPECTED_CITED} (sken 122 = starševska stran; sken 125 = glava 1901, ni citiran)")
    print(f"vpisi {len(entries)} / hiše {len(set(houses))} (NARE, brez ponovitev);"
          f" PT {len(inset)}/{len(gap)} (45/54/58 že dokazani; 42/50/51 ostajajo); nove hiše {new_houses};"
          f" vitals 1900 = {len(vitals_1900)};"
          f" vitals vseh treh knjig = {len(vitals_all)} (pričakovano {EXPECTED_VITALS_TOTAL});"
          f" hiše vitals = {n_houses_total}; kumulativ {n_entries_total + EV_ONLY_TOTAL}"
          f" vpisov / {n_houses_total + len(ev_only_houses)} hiš;"
          f" duhovniki (Šturm, Rauq) = {(n_sturm, n_rauq)} + Perg {n_perg} + Klunček {n_kluncek}; † {n_infant}/16;"
          f" babica: {bab_named} imenovanih (NOVELA) / {bab_empty} praznih")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(verify())
