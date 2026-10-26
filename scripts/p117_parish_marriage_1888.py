#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P117 — župnija Podzemelj: poročna knjiga 04455, polno leto 1888 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → P116 = 1887): okvir POTRJEN —
skeni 71–74 == Pag. 70–73 (Pag. == sken − 1 velja v 66–76; 3. potrditev);
**20 vpisov** (razpored 7+3+6+4); glava 1889 = Pag. 74 = s75 BREZ velike
glave [~] (novela-kandidat). GEOMETRIJA LANDSCAPE (2500×1800): levi list =
Braütigam+Brant, desni = Eltern/Befände/Befunden/kathol. Pfarrer.

FAZA 2: **20/20 vpisov transkribiranih OBOJESTRANSKO** + mega-zoom serija
(~25 izrezov ×4–6). **FAZA-1 POPRAVKI ×11**: v1 Zajčji vrh/Pf. Toplice +
Ana HRASOVEC (ne »Krajovce«) + v2 MATHIAS (ne »Michael«) Brinec + v3
MRAVINEC?/POŽEK?/58! + v4 KNURE?/Škrilje? + v5 MARENTIČ?/STAJNIĆ? + v6
~~März~~→APRIL 30 + Johan FILAK? (ne »Šoltar«) + v7 Mathias STRAUS (ne
»Kravce«) × Maria JAKOŠ? + v8 JAKLIČ? (ne »Josejc«) + v9 17.6. (ne »9.6.«)
+ v10 ČRNOMELJ 63/18.7./Perie?/Lasič + v12 GRIBLJE 64 (P82 »26« REŠEN!)
+ v13 MARTIN Zugelj/JAKŠA? + v14 MURN 58/SUSTEK/Gradac 12? + v15
VRBANEK?/Bubnjarci-Pf. ŽAKANJE/Zemelj? 17 + v16 SAJHNER?/Sayhnec? + v17
KOŠIR?/POVŠE 17/Gradac 85+Verden? + v18 TASIČ? (ne »Javnič«!)/HARASIMIČ?
+ v19 JAKLIČ? (ne »Javkič«)/Zemelj? 25 + v20 KOHAMIČ?/Cerkvišče 22/28.

NOVELE: **DUHOVNIK JOS. RAUY PROVISOR ×20/20** (nov status linije) +
**v9 = NAJBOGATEJŠI BEFUNDEN** (6 dokumentov: RGBl 153 + DISPENS 3. kl.
12.6. Z: 1109 + Bez.-Hauptm. 14.6. Z: 4574 + Ordin. Laibach 17.6. № 1143
+ mündliche Einwilligung = poroka isti dan!) + **SESTRI CERNIČ** (v6+v16,
isti starši, obe h42) + **BRATA BRINEC h23** (1887 v4 Maria + 1888 v2
Mathias, isti starši) + **STRAUS-VEJA h32** (oče MARCUS × Katharina
Dragoševič?) + **KOTTLIN-PRIČA** (v17 = 1887 v21 ženin — 1. cross-link!)
+ **PEGDIREC ×9+** (v12 mati Anna + priča Peter = P115 v5 ŽENIN!) +
**PLUT ×3 / JAKLIČ ×4 / FILAK ×4 / KAMBIČ ×4 / HRIŽAN ×3 / DRAGOŠ ×3** +
**TAUF-NOVELA ×3** (v10 48-letnik + v14 Ana Sustek 43 + v15 Vrbanek) +
**2× 58-LETNI ŽENIN** (v3+v14) + **NEVESTA 17** (v17) + **4 TUJE ŽUPNIJE**
(Toplice? ×2, Adlešiče, Semič, **Žakanje** ~45 km!) + mesto **ČRNOMELJ**
(v10) + Borovnica ×2 + Rudolfswert + **NOVI DOKUMENTNI TIPI ×6** (mrtvaški
list Semič + Communalzettel Gradac + Nedelovna svjedodžba proglašenstva +
virna izjava sodnije Metlika/polnoletnost + §102 + Wehrmannsschein?) +
**mati ženina PRAZNA** (v14, pika) + statusi-neznank ×6 (novela-kandidat).

NOVE GRIBLJE HIŠE: h33 (v2) + h32 Straus (v7) — NOVE; h23-1888 (Brinec
brata) + h64-1888 (2. dokaz po P115) — ponovitve; **bloki 04455 = 20;
vitals 544**. Skripta scripts/p117_parish_marriage_1888.py (I1–I11, --check
izpiše PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
knjige/inventarja).
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1888.json"
DOKAZ_P116 = "research/issue17/parish-marriage-1887.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (71, 74)          # 71 = Pag. 70 (vpisi 1–7) … 74 = Pag. 73 (vpisi 17–20)
FRAME_PAGES = (70, 73)
EXPECTED_ENTRIES = 20
EXPECTED_EXCLUDED = 10
EXPECTED_ANOMALIES = 16
EXPECTED_CROSSCHECKS = 26
GRIBLJE_ROWS = [2, 3, 7, 12]
GRIBLJE_MARRIAGES = 4
GRIBLJE_HOUSES_TS = "23,32,33,64"   # hiše z 1888 bloki v parish.ts
EXPECTED_VITALS = 537           # P117 dokaz lastna kumulativa (533 + 4 bloki); trenutna = 544 (P118)
BLOCKS_04455 = 20                # P117 dokaz lastna kumulativa
BLOCKS_04455_TS = 164   # P140: + 6 blokov 1911               # P126: + 9 blokov 1897 (52 + 9)            # parish.ts zdaj = 49 (P121 +4 bloki 1892 + P122 +5 bloki 1893 + P123 +4 bloki 1894 + P124 +3 bloki 1895)
DATE_COUNTS = {"januar": 2, "februar": 3, "marec": 0, "april": 1, "maj": 2,
               "junij": 1, "julij": 1, "avgust": 2, "september": 1, "oktober": 2,
               "november": 5, "december": 0}
# P117 pini (blok-houseNo → obvezen fragment v whatSi)
BLOCK_PINS = [
    ("23", "1888"), ("23", "BRINEC"), ("23", "brata"),
    ("32", "Straus"), ("32", "NOVA"), ("32", "Marcus"),
    ("33", "Dehlič"), ("33", "NOVA"),
    ("64", "1888"), ("64", "Marhiščar"), ("64", "Pegdirec"),
]
# stara branja = IZTELA iz 04455 blokov (natančni stari fragmenti)
OLD_READINGS = [
    "Michael BRINE", "GRIBLJE 26 [~]", "»Kokljicev", "Krasec?",
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
    check("I1b entries=20", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=10", len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije=16", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=26", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (20/20)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 entries=20", fr.get("entriesTotal") == EXPECTED_ENTRIES, str(fr.get("entriesTotal")))
    check("I2b skeni 71–74", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2c strani 70–73", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    rows = [e["row"] for e in d["entries"]]
    check("I2d vrstice 1–20 zapored", rows == list(range(1, 21)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2e skeni znotraj 71–74", all(71 <= s <= 74 for s in sc), str(sorted(set(sc))))
    per = {71: 7, 72: 3, 73: 6, 74: 4}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2f razpored 7+3+6+4", raz == per, str(raz))

    # ---------- I3: Griblje vpisi + nove hiše ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [2,3,7,12]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 4", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3b hiš omenjenih = 5", d["stats"].get("gribljeHousesMentioned") == 5,
          str(d["stats"].get("gribljeHousesMentioned")))
    e2 = d["entries"][1]
    check("I3c vpis 2 = h23 × h33 (BRATA BRINEC!)",
          e2["groom"]["houseNo"] == 23 and e2["bride"]["houseNo"] == 33
          and "Mathias" in e2["groom"]["name"] and "Michael" not in e2["groom"]["name"],
          f'{e2["groom"]["name"]} h23 × {e2["bride"]["name"]} h33')
    e7 = d["entries"][6]
    check("I3d vpis 7 = h32 Straus (NE Kravce!)", e7["groom"]["houseNo"] == 32
          and "Straus" in e7["groom"]["name"] and "Marcus" in e7["parentsGroom"],
          f'{e7["groom"]["name"]} h32; {e7["parentsGroom"][:40]}')
    e12 = d["entries"][11]
    check("I3e vpis 12 = h64 (NE 26! P82 rešen)", e12["groom"]["houseNo"] == 64
          and "PEGDIREC" in e12["parentsGroom"].upper(),
          f'h{e12["groom"]["houseNo"]}; {e12["parentsGroom"][:40]}')
    e9 = d["entries"][8]
    check("I3f vpis 9 = najbogatejši Befunden (RGBl+dispens)",
          "153" in e9["urkunden"] and "1109" in e9["urkunden"] and "1143" in e9["urkunden"],
          e9["urkunden"][:60])
    e11 = d["entries"][10]
    check("I3g vpis 11 = mrtvaški list (vdova 24)",
          "MRTVAŠKI LIST" in e11["urkunden"].upper() and "VDOVA" in e11["bride"]["status"].upper(),
          e11["urkunden"][:60])
    e17 = d["entries"][16]
    check("I3h vpis 17 = Kottlin priča + Borovnica",
          "KOTTLIN" in str(e17.get("witnesses", [])).upper() and "Borovnica" in e17["urkunden"],
          str(e17.get("witnesses", []))[:60])
    e6 = d["entries"][5]
    check("I3i vpis 6 = prekrižan ~~März~~ → 30.4.1888",
          "30.4.1888" in e6["date"] and "März" in e6["date"],
          e6["date"])
    e18 = d["entries"][17]
    check("I3j vpis 18 = Tasič (NE Javnič!)",
          e18["groom"]["name"].lower().startswith("nicolaus tasič"),
          e18["groom"]["name"])

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
    check("I4 meseči (vsota 20)", not bad_m and sum(mc.values()) == 20, str(bad_m or sum(mc.values())))
    feb6 = [e["row"] for e in d["entries"] if e["date"].startswith("6.2.")]
    check("I4b dvojni dan 6.2. = [4,5]", feb6 == [4, 5], str(feb6))
    nov12 = [e["row"] for e in d["entries"] if e["date"].startswith("12.11.")]
    check("I4c dvojni dan 12.11. = [16,17]", nov12 == [16, 17], str(nov12))
    nov19 = [e["row"] for e in d["entries"] if e["date"].startswith("19.11.")]
    check("I4d dvojni dan 19.11. = [18,19]", nov19 == [18, 19], str(nov19))

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovnik RauyProvisor ×20", pr.get("RauyProvisor") == 20, str(pr))
    check("I5b dispensacije=1", st.get("dispensations") == 1, str(st.get("dispensations")))
    check("I5c vitals=537 (P117 lastna kumulativa; trenutna 544)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5d bloki 04455=20 (P117 lastna; parish.ts 27)", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5e novi bloki=4", st.get("newBlocks") == 4, str(st.get("newBlocks")))
    check("I5f najstarejši ženin=58 (×2)", st.get("oldestGroom") == 58, str(st.get("oldestGroom")))
    check("I5g najmlajša nevesta=17", st.get("youngestBride") == 17, str(st.get("youngestBride")))
    check("I5h vdova-nevesta=1", st.get("widowsBride") == 1, str(st.get("widowsBride")))

    # ---------- I6: anomalije A1–A16 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A16", ids == [f"A{i}" for i in range(1, 17)], str(ids))
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6b A2 = najbogatejši Befunden", "NAJBOGATEJŠI" in a2.get("summary", "").upper())
    a7 = next((a for a in d["anomalies"] if a["id"] == "A7"), {})
    check("I6c A7 = sestri Cernič", "CERNIČ" in a7.get("summary", "").upper())
    a8 = next((a for a in d["anomalies"] if a["id"] == "A8"), {})
    check("I6d A8 = brata Brinec", "BRINEC" in a8.get("summary", "").upper())
    a13 = next((a for a in d["anomalies"] if a["id"] == "A13"), {})
    check("I6e A13 = Kottlin priča", "KOTTLIN" in a13.get("summary", "").upper())
    a6 = next((a for a in d["anomalies"] if a["id"] == "A6"), {})
    check("I6f A6 = Rauy provisor ×20", "PROVISOR" in a6.get("summary", "").upper())

    # ---------- I7: crossChecks ----------
    cc_ok = [c for c in d["crossChecks"] if c["verdict"].startswith("✓")]
    check("I7 crossChecks ✓ ≥ 24", len(cc_ok) >= 24, f"{len(cc_ok)}/{len(d['crossChecks'])}")
    cc16 = next((c for c in d["crossChecks"] if c.get("id") == "CC16"), {})
    check("I7b CC16 = Kottlin cross-link", "Kottlin" in cc16.get("verdict", "") and "priča" in cc16.get("verdict", ""))
    cc26 = next((c for c in d["crossChecks"] if c.get("id") == "CC26"), {})
    check("I7c CC26 = P118 lead 1889", "P118" in cc26.get("verdict", "") and "1889" in cc26.get("verdict", ""))
    # P116 dokaz ostaja nespremenjen (regresijska zaščita)
    try:
        d116 = json.load(open(DOKAZ_P116))
        check("I7d P116 dokaz stats vitals=533", d116["stats"].get("vitals") == 533,
              str(d116["stats"].get("vitals")))
    except Exception as e:  # noqa: BLE001
        check("I7d P116 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P121 +4, P122 +5, P123 +4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6! + P129 +2 + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8b hiše 1888 = [23,32,33,64]", ",".join(h1888) == GRIBLJE_HOUSES_TS, ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8c hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8d hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1888 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1888,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8e pini P117 (11)", not missing, str(missing) if missing else "vse ✓")
    whatsis = [m.group(1) for m in re.finditer(r'bookSignature:\s*"04455",\s*year:\s*\d{4},\s*scan:\s*\d+,\s*page:\s*\d+,\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)]
    stale = [o for o in OLD_READINGS if any(o in w for w in whatsis)]
    check("I8f stara branja iztekla", not stale, str(stale) if stale else "vse ✓")

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p117", '"qa-p117-parish-marriage-1888"' in qa)
    check("I9b qa-p116 bloki 78", "poročni bloki (04455) ≠ 142" in qa)
    check("I9c p80 bloki 78", "poročni vpisi (04455) ≠ 158" in qa)
    # vitals 544 regresijska zaščita v qa-p117
    check("I9d vitals 637 zaščita (P128)", "HOUSE_VITALS.length !== 681" in qa[qa.index("const p117Marr"):] if "const p117Marr" in qa else False)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P117", "P117" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1888-notes.md").read()
    check("I10b notes faza 2", "FAZA 2" in nt and "BRINEC" in nt.upper())

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
