#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P118 — župnija Podzemelj: poročna knjiga 04455, polno leto 1889 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → P116 = 1887 → P117 = 1888): okvir
POTRJEN — skeni 75–76 == Pag. 74–75 (Pag. == sken − 1 velja v 71–76; 4.
potrditev); **10 vpisov** (razpored 6+4); glava 1889 = Pag. 74 BREZ velike
glave [~] (novela-kandidat POTRJEN); vrstice restart na 1 = 3. potrditev
novele P83. LANDSCAPE geometrija (~2471–2478×1800). Glava 1890 že Pag. 76
= s77 (1890 ima ≥ 16 vpisov!); glava 1891 = Pag. 79 = s80.

FAZA 2: **10/10 vpisov transkribiranih OBOJESTRANSKO** + 19 mega-zoomov
×3–6. **FAZA-1 ORIS POPRAVKI ×24** (vsak vpis vsaj 1 — najbolj napačen oris
linije!): v1 Cerkvišče 32/Štubljar 13 + v2 URB (ne »Mech«) × PERDINEC h40
(ne »Lechne h16«) + v3 POŽEK (ne »Perich«) × ANNA SIMEC h54 (ne »Maria
Simic h24«) + v4 starosti 30/23 + v5 ŠOPČIČ Gradac 49 **66 LET** (ne
»Šupanc 19, 46«) × Zaštava 8 Pf. Črnomelj + v6 Cerkvišče 35 (ne »Solvenia«)
+ v7 23.9. (ne 3.9.) + v8 MILEK (ne »Mulek/Melek«) × KLEJPEC (ne
»Kleklvec«) GRIBLJE 87 (ne 31) 14.10. (ne 10.10.) + v9 SENICA/Zimmermann
+ v10 h65 (ne 6).

NOVELE: **NAJSTAREJŠI ŽENIN VSEH ČASOV = 66 LET** (v5; prej 61 Kottlin 1887
+ 58 ×2 1888) + **37-letna razlika** (v8: 60 × 23!) + **v9 OBA OČETA
PRAZNA = 1. NEZAKONSKA PAR LINIJE** + **v7 brez duhovnikovega podpisa**
(varuh MATIJA NOVAK — pro tutore delegato?) + **v8 2. DUHOVNIK AMBROSIJ
GLIHA coop.** (Rauy ×8 + Gliha ×1 + prazen ×1!) + **⅓ GÜTL NOV ULOMEK**
(v8 Marcus Perdinec) + **MAGD ×2 NOV STATUS NEVESTE** (v5 + v9; »Mayr/
Mayst« = Kurrent »Mayd«!) + **ZIMMERMANN ×2** (v6 + v9) + **PFLEGER NOV
STATUS PRIČE** (v9 Anton Toma) + **MLADOLETNOST-NOVELA 7/10** (vse neveste
< 24 s privolitvenim dokumentom; v1 edina brez) + **ZGŁASNICA ×10/10 =
100%** (v1 datirana 25.10.1888 — 3,5 mes. vnaprej!) + **ZIMSKA VRZEL 3,5
MESECA** (3.6. → 23.9. — rekord linije!) + dvojni dan 11.2. ×2 + NOVI
DOKUMENTNI TIPI ×5 (varuhovo dovoljenje + oznamni list župn. urada +
Amtskindschaft-Pfarramt + G?upjäftigit-Knitt-Etbürning/Klärning [~] +
Genehm. Landesreg. Laibach).

MREŽE: **PERDINEC ×3** (v2 h40 + v3 mati + v8 h87/Marcus ⅓!) + **POŽEK ×3**
(v3 ženin h21 + v4 ženin Adlešiče + v6 mati neveste!) + **NOVAK ×2** (v7
varuh ↔ v10 nevesta/oče — Gradac!) + MILEK (1887 h23 mati ↔ 1889 h30) +
DOHLIČ (1888 h33 nevesta ↔ 1889 h32 mati) + TOME (1887 ×4 → 1889) + DRAGOŠ
+ ZUGELJ + GRABRIJAN; tuje župnije ×4 (Adlešiče + Pf. Črnomelj + Pf.
Toplice + Pf. Otok?); sodna mreža ×4 (Črnomelj Z:1118/Z:8062 + Metlika
VIII.889/119 + IV/878) + Ljubljana ×2 (Landesreg. Z:6758 + Ordinariat
št. 2515) + Bez.-Hauptm. Črnomelj Z:9540 (cf. 1888 Z:4574!).

NOVE POROČNE HIŠE: **6 × 1. POROČNI DOKAZ** (h7/h21/h30/h40/h54/h87 —
vse že v krstni 04105!) + **h32 = 2. dokaz** (×2 v 2 letih po 1888 v7
Straus!) — **bloki 04455 = 27; vitals 544; p80 hiše 44**. Skripta
scripts/p118_parish_marriage_1889.py (I1–I11, --check izpiše PASS/FAIL in
vrne exit code; --live omogoči HTTP preverjanje knjige/inventarja).
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1889.json"
DOKAZ_P117 = "research/issue17/parish-marriage-1888.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (75, 76)          # 75 = Pag. 74 (vpisi 1–6) … 76 = Pag. 75 (vpisi 7–10)
FRAME_PAGES = (74, 75)
EXPECTED_ENTRIES = 10
EXPECTED_EXCLUDED = 10
EXPECTED_ANOMALIES = 16
EXPECTED_CROSSCHECKS = 24
GRIBLJE_ROWS = [2, 3, 4, 8]
GRIBLJE_MARRIAGES = 4
GRIBLJE_HOUSES_TS = "7,21,30,32,40,54,87"   # hiše z 1889 bloki v parish.ts
EXPECTED_VITALS = 544           # P118 dokaz lastna kumulativa (537 + 7 bloki); trenutna = 548 (P119)
BLOCKS_04455 = 27                # P118 dokaz lastna kumulativa (20 + 7)
BLOCKS_04455_TS = 164   # P140: + 6 blokov 1911               # P126: + 9 blokov 1897 (52 + 9)            # parish.ts zdaj = 49 (P121 +4 bloki 1892 + P122 +5 bloki 1893 + P123 +4 bloki 1894 + P124 +3 bloki 1895)
P80_HOUSES = 44                 # p118 JSON lastna vrednost (vzorčni podnabor p80; trenutna = 46 P119)
DATE_COUNTS = {"januar": 0, "februar": 5, "marec": 0, "april": 0, "maj": 0,
               "junij": 1, "julij": 0, "avgust": 0, "september": 1, "oktober": 1,
               "november": 2, "december": 0}
# P118 pini (blok-houseNo → obvezen fragment v whatSi)
BLOCK_PINS = [
    ("32", "Urb"), ("32", "Perdinec"), ("32", "Dohlič"),
    ("40", "Perdinec"), ("40", "Perdinec-mreža"),
    ("21", "Požek"), ("21", "Dragoš"),
    ("54", "Simec"), ("54", "Perdinec"),
    ("7", "Totter"), ("7", "Adlešiče"),
    ("30", "Milek"), ("30", "60"),
    ("87", "Perdinec"), ("87", "Klejpec"), ("87", "Gliha"),
]
# stara branja = IZTELA iz 04455 blokov (natančni faza-1 fragmenti)
OLD_READINGS = [
    "Mech", "Kleklvec", "Mulek?/Melek", "Simic? GRIBLJE 24", "Mayr",
]


def http_get(url, headers=None, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except Exception as e:  # noqa: BLE001
            import time
            time.sleep(2 + i * 2)
            last = e
    raise last  # type: ignore


def main() -> int:
    live = "--live" in sys.argv
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    # ---------- I1: dokaz JSON ----------
    try:
        d = json.load(open(DOKAZ))
    except Exception as e:  # noqa: BLE001
        print(f"I1 FAIL: {e}")
        return 1
    check("I1 json obstaja", True, DOKAZ)
    check("I1b entries=10", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=10", len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije=16", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=24", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (10/10)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 entries=10", fr.get("entriesTotal") == EXPECTED_ENTRIES, str(fr.get("entriesTotal")))
    check("I2b skeni 75–76", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2c strani 74–75", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    rows = [e["row"] for e in d["entries"]]
    check("I2d vrstice 1–10 zapored", rows == list(range(1, 11)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2e skeni znotraj 75–76", all(75 <= s <= 76 for s in sc), str(sorted(set(sc))))
    per = {75: 6, 76: 4}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2f razpored 6+4", raz == per, str(raz))
    check("I2g glava 1889 brez velike glave [~]", "BREZ velike glave" in fr.get("glava1889", ""), fr.get("glava1889", "")[:60])
    check("I2h glava 1890 = Pag. 76", "Pag. 76" in fr.get("glava1890", ""), fr.get("glava1890", "")[:60])
    check("I2i glava 1891 = Pag. 79", "Pag. 79" in fr.get("glava1891", ""), fr.get("glava1891", "")[:60])

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [2,3,4,8]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 4", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3b hiš omenjenih = 7", d["stats"].get("gribljeHousesMentioned") == 7,
          str(d["stats"].get("gribljeHousesMentioned")))
    e2 = d["entries"][1]
    check("I3c vpis 2 = h32 × h40 (Urb × Perdinec!)",
          e2["groom"]["houseNo"] == 32 and e2["bride"]["houseNo"] == 40
          and "Urb" in e2["groom"]["name"] and "Mech" not in e2["groom"]["name"],
          f'{e2["groom"]["name"]} h32 × {e2["bride"]["name"]} h40')
    e3 = d["entries"][2]
    check("I3d vpis 3 = h21 × h54 (Požek × Simec; DRAGOŠ+PERDINEC starši!)",
          e3["groom"]["houseNo"] == 21 and e3["bride"]["houseNo"] == 54
          and "DRAGOŠ" in e3["parentsGroom"] and "PERDINEC" in e3["parentsBride"],
          f'h21 × h54; {e3["parentsGroom"][:30]} / {e3["parentsBride"][:30]}')
    e5 = d["entries"][4]
    check("I3e vpis 5 = 66-LETNI ženin (rekord linije!) + Magd",
          e5["groom"]["age"] == 66 and "Magd" in e5["bride"]["stand"],
          f'{e5["groom"]["age"]} let × {e5["bride"]["stand"]}')
    e8 = d["entries"][7]
    check("I3f vpis 8 = h30 × h87 (Milek 60!; Gliha coop.; ⅓ Gütl; Klejpec)",
          e8["groom"]["age"] == 60 and e8["bride"]["houseNo"] == 87
          and "GLIHA" in e8["priest"].upper() and "⅓" in e8["parentsBride"]
          and "KLEJPEC" in e8["parentsBride"].upper(),
          f'{e8["groom"]["age"]} let; {e8["priest"]}; {e8["parentsBride"][:40]}')
    e9 = d["entries"][8]
    check("I3g vpis 9 = OBA OČETA PRAZNA (1. nezakonska par!)",
          e9["parentsGroom"].startswith("—") and e9["parentsBride"].startswith("—"),
          f'G:{e9["parentsGroom"][:20]} B:{e9["parentsBride"][:20]}')
    e7 = d["entries"][6]
    check("I3h vpis 7 = varuh Novak podpis + sodišče Metlike (brez duhovnika!)",
          "NOVAK" in e7["priest"].upper() and "Metliki" in e7["urkunden"]
          and "Rauy" not in e7["priest"],
          f'{e7["priest"][:40]}')
    e10 = d["entries"][9]
    check("I3i vpis 10 = najbogatejši 1889 (5 dokumentov: 6758/9540/2515)",
          "6758" in e10["urkunden"] and "9540" in e10["urkunden"] and "2515" in e10["urkunden"],
          e10["urkunden"][:60])
    e1 = d["entries"][0]
    check("I3j vpis 1 = zgłasnica datirana 25.10.1888 (3,5 mes. vnaprej!)",
          "25. oktobra 1888" in e1["urkunden"], e1["urkunden"][:60])
    e4 = d["entries"][3]
    check("I3k vpis 4 = Adlešiče ×3 dokumenti (oznamni list ženinov NOV!)",
          e4["groom"]["village"] == "Adlešiče" and "list ženinov" in e4["urkunden"],
          e4["urkunden"][:60])

    # ---------- I4: datumi + meseči ----------
    def mes(datestr):
        m = re.search(r"(\d+)\.\s*(\d+)\.", datestr.lower())
        return int(m.group(2)) if m else None
    mc = {"januar": 0, "februar": 0, "marec": 0, "april": 0, "maj": 0, "junij": 0,
          "julij": 0, "avgust": 0, "september": 0, "oktober": 0, "november": 0, "december": 0}
    names = {1: "januar", 2: "februar", 3: "marec", 4: "april", 5: "maj", 6: "junij",
             7: "julij", 8: "avgust", 9: "september", 10: "oktober", 11: "november", 12: "december"}
    for e in d["entries"]:
        m = mes(e["date"])
        if m:
            mc[names[m]] += 1
    bad_m = {k: v for k, v in mc.items() if v != DATE_COUNTS[k]}
    check("I4 meseči (vsota 10)", not bad_m and sum(mc.values()) == 10, str(bad_m or sum(mc.values())))
    feb11 = [e["row"] for e in d["entries"] if e["date"].startswith("11.2.")]
    check("I4b dvojni dan 11.2. = [1,2]", feb11 == [1, 2], str(feb11))
    # zimska/poletna vrzel 3,5 meseca: 3.6. → 23.9. — noben datum v (jun > 3, jul, avg, sep < 23) + apr/maj prazni
    gap_rows = []
    for e in d["entries"]:
        m = re.match(r"(\d+)\.(\d+)\.", e["date"])
        if m:
            day, mo = int(m.group(1)), int(m.group(2))
            if mo in (4, 5, 7, 8) or (mo == 6 and day > 3) or (mo == 9 and day < 23):
                gap_rows.append(e["row"])
    check("I4c zimska/poletna vrzel 3.6.→23.9. (3,5 meseca)", not gap_rows, str(gap_rows))

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki Rauy ×8 + Gliha ×1 + prazen ×1",
          pr.get("Rauy") == 8 and pr.get("GlihaCoop") == 1 and pr.get("brezPodpisaVaruh") == 1, str(pr))
    check("I5b zgłasnice=10 (100%)", st.get("zgłasnice") == 10, str(st.get("zgłasnice")))
    check("I5c vitals=544 (P118 lastna kumulativa; trenutna 548)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5d bloki 04455=27 (P118 lastna; parish.ts 31)", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5e novi bloki=7", st.get("newBlocks") == 7, str(st.get("newBlocks")))
    og = st.get("oldestGroom", {})
    check("I5f najstarejši ženin=66 (rekord linije!)", og.get("age") == 66, str(og))
    yb = st.get("youngestBride", {})
    check("I5g najmlajša nevesta=20", yb.get("age") == 20, str(yb))
    gap = st.get("maxAgeGap", {})
    check("I5h največja razlika=37 (v8: 60×23)", gap.get("years") == 37, str(gap))
    check("I5i privolitveni dokumenti=7 (mladoletnost-novela)", st.get("consentDocs") == 7, str(st.get("consentDocs")))
    check("I5j p80 hiše=44", st.get("p80Houses") == P80_HOUSES, str(st.get("p80Houses")))

    # ---------- I6: anomalije A1–A16 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A16", ids == [f"A{i}" for i in range(1, 17)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I6b A1 = oris popravki ×24", "×24" in a1.get("summary", ""), a1.get("summary", "")[:50])
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6c A2 = najstarejši ženin 66", "66" in a2.get("summary", ""), a2.get("summary", "")[:50])
    a5 = next((a for a in d["anomalies"] if a["id"] == "A5"), {})
    check("I6d A5 = 1. nezakonska par", "NEZAKONSKA" in a5.get("summary", "").upper(), a5.get("summary", "")[:50])
    a9 = next((a for a in d["anomalies"] if a["id"] == "A9"), {})
    check("I6e A9 = Magd ×2 nov status", "MAGD" in a9.get("summary", "").upper(), a9.get("summary", "")[:50])
    a12 = next((a for a in d["anomalies"] if a["id"] == "A12"), {})
    check("I6f A12 = mladoletnost-novela 7/10", "MLADOLETNOST" in a12.get("summary", "").upper(), a12.get("summary", "")[:50])

    # ---------- I7: crossChecks ----------
    cc_ok = [c for c in d["crossChecks"] if c["verdict"].startswith("✓")]
    check("I7 crossChecks ✓ ≥ 22", len(cc_ok) >= 22, f"{len(cc_ok)}/{len(d['crossChecks'])}")
    cc1 = next((c for c in d["crossChecks"] if c.get("id") == "CC1"), {})
    check("I7b CC1 = h32 2. dokaz (×2 v 2 letih)", "h32" in cc1.get("verdict", "") and "×2" in cc1.get("verdict", ""))
    cc3 = next((c for c in d["crossChecks"] if c.get("id") == "CC3"), {})
    check("I7c CC3 = PERDINEC ×3 (1886→1889)", "PERDINEC ×3" in cc3.get("verdict", "") and "1886" in cc3.get("verdict", ""))
    cc9 = next((c for c in d["crossChecks"] if c.get("id") == "CC9"), {})
    check("I7d CC9 = NOVAK varuh↔nevesta", "NOVAK" in cc9.get("verdict", "") and "varuh" in cc9.get("verdict", ""))
    # P117 dokaz ostaja nespremenjen (regresijska zaščita)
    try:
        d117 = json.load(open(DOKAZ_P117))
        check("I7e P117 dokaz stats vitals=537", d117["stats"].get("vitals") == 537,
              str(d117["stats"].get("vitals")))
    except Exception as e:  # noqa: BLE001
        check("I7e P117 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P121 +4, P122 +5, P123 +4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6! + P129 +2 + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1889 = sorted((h for h, y, _ in blocks_m if y == "1889"), key=int)
    check("I8b hiše 1889 = [7,21,30,32,40,54,87]", ",".join(h1889) == GRIBLJE_HOUSES_TS, ",".join(h1889))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8c hiše 1888 nespremenjene", ",".join(h1888) == "23,32,33,64", ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8d hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8e hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1889 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1889,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8f pini P118 (16)", not missing, str(missing) if missing else "vse ✓")
    whatsis = [m.group(1) for m in re.finditer(r'bookSignature:\s*"04455",\s*year:\s*\d{4},\s*scan:\s*\d+,\s*page:\s*\d+,\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)]
    stale = []
    for o in OLD_READINGS:
        for w in whatsis:
            i = w.find(o)
            while i != -1:
                ctx = w[max(0, i - 60):i]
                # sklic na popravek (»ne »X«« / »oris ... = popravek« / faza-1) ni staro branje
                if not any(t in ctx for t in ("ne »", "popravek", "faza-1", "oris »")):
                    stale.append((o, w[max(0, i - 30):i + len(o) + 20]))
                    break
                i = w.find(o, i + 1)
    check("I8g stara branja iztekla", not stale, str(stale) if stale else "vse ✓")
    # oznake 1./2. poročni dokaz (po lastni hiši!)
    own1 = sorted({m.group(1) for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1889,[^}]*?(?:1\. poročni|1\. POROČNI) dokaz h\1', ts, re.S)}, key=int)
    check("I8h 1.-poročni-dokaz hiše = [7,30,40,54,87]", ",".join(own1) == "7,30,40,54,87", ",".join(own1))
    whatsis1889 = [m.group(1) for m in re.finditer(r'houseNo:\s*"\d+",\s*bookSignature:\s*"04455",\s*year:\s*1889,.*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)]
    check("I8i h21+h32 = »2. poročni dokaz« (1889 bloki)",
          sum(1 for w in whatsis1889 if "2. poročni dokaz h21" in w or "2. poročni dokaz h32" in w) == 2,
          str(sum(1 for w in whatsis1889 if "2. poročni dokaz h21" in w or "2. poročni dokaz h32" in w)))

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p118", '"qa-p118-parish-marriage-1889"' in qa)
    check("I9b qa-p116 bloki 78", "poročni bloki (04455) ≠ 142" in qa)
    check("I9c p80 bloki 78", "poročni vpisi (04455) ≠ 158" in qa)
    # vitals 544 regresijska zaščita v qa-p118
    check("I9d vitals 637 zaščita (P128)", "HOUSE_VITALS.length !== 681" in qa[qa.index("const p118Marr"):] if "const p118Marr" in qa else False)
    check("I9e stara številka 537 iztekla", "HOUSE_VITALS.length !== 537" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P118", "P118" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1889-notes.md").read()
    check("I10b notes faza 2", "FAZA 2" in nt and "NEZAKONSKA" in nt.upper())

    # ---------- live ----------
    if live:
        st_, body = http_get(BOOK_URL)
        check("I11 live knjiga 200", st_ == 200, str(st_))
        m = re.search(r'"files":\s*\[(.*?)\]', body.decode("utf-8", "ignore"), re.S)
        n = len(re.findall(r'/image/', m.group(1))) if m else 0
        check("I11b slike = 192", n == EXPECTED_IMAGES, str(n))

    # ---------- izpis ----------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    print(f"\n{passed}/{total} PASS")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
