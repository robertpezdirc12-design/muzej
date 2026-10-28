#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P124 — župnija Podzemelj: poročna knjiga 04455, polno leto 1895 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P123 = 1894): okvir POTRJEN —
skeni 94–96 == Pag. 93–95 (Pag. == sken − 1, 10. potrditev; velja v 61–96);
**16 vpisov** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 →
1892:15 → 1893:20 → 1894:15 → 1895:16; razpored 6+5+5); **VELIKA GLAVA
»Trauungs=Buch« + rokopisno »1895« POTRJENA na s94** (P124 lead!; 6. velika
glava linije: 1887 s66 + 1890 s77 + 1892 s84 + 1893 s87 + 1894 s91 + 1895 s94).
LANDSCAPE geometrija (2510/2511/2521×1800). Ob robu s96: tiskar »Laibach.
Druck u. Verlag v. Möttlig.«!

FAZA 2: **16/16 vpisov transkribiranih OBOJESTRANSKO** + 32 row-crops ×2
LANCZOS + 65 zoomov + 30+ mikro-zoomov 8×/10×/12× (zoom_124/124b/124c).

NOVELE: **★ 1. ČASTNIK linije** (v15 Herr Andreas Stal, OBERLEUTNANT [~],
Metlika 38, 40 × Francisca Logar, hči Offizierja [~], 18 — priča Josef Avanzo
k.k. HAUPTMANN + Garnisons-Propstei zū Metlika + mestna občina Metlika št:150)
+ **★ 1. hrvaški dokumenti** (v6 Gerdinovac — »in Croalien« [~] + smrtni list
dekanate v Lipniku [~] + Broj 485 občine Griblje) + **★ POPRAVEK STAROSTI
40→54** (v6 — vdovec!) + **★ DISPENS-REKORD ×4** (v7 №504 + v8 №613 + v12
Ž/L:4994 »Wittwenschaft« [~] PO poroki! + v16) + **★ 2. LANDSREGIERUNG
Laibach №181** (v8) + **★ »Möttling« = nemško ime METLIKE** (Bez. Ger. ×4) +
**★ HOMONIMA** (Marcus Perdinec v11 ≠ P123 v3 + Johann Starasinič v8 ≠ v14) +
**★ DVA PRIČA ISTO IME** (v4 Peter Jakofčič ×2 — vzorec P123 v5!) + **3+3+2
poroke na 3 dnevih** + ZUGELJ ×3 + MAYD ×2 + Großjährigkeits-Erklärung ×3 +
formula »in Ungarn … Närnk« [~] ×4 + Rauy-monopol 16/16 (»M.!« ×7).

Skripta scripts/p124_parish_marriage_1895.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
matricula-online.eu). Brez --live je popolnoma OFFLINE (I1–I10).

Uporaba: python3 scripts/p124_parish_marriage_1895.py [--live]
"""
import json
import re
import sys
import urllib.request

BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04455/"
BOOK_SIGNATURE = "04455"
EXPECTED_IMAGES = 192
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
DOKAZ = "research/issue17/parish-marriage-1895.json"
DOKAZ_P123 = "research/issue17/parish-marriage-1894.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"
FRAME_SCANS = (94, 95, 96)  # 94 = Pag. 93 (velika glava 1895 + v1–6) · 95 = Pag. 94 (v7–11) · 96 = Pag. 95 (v12–16)
FRAME_PAGES = (93, 94, 95)
EXPECTED_ENTRIES = 16
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 8
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [10, 11, 13]
GRIBLJE_MARRIAGES = 3
GRIBLJE_HOUSES = [16, 27, 52]
GRIBLJE_HOUSES_TS = "16,27,52"  # numerični vrstni-red (h16+h27 s95, h52 s96)
EXPECTED_VITALS = 566                 # P124 dokaz lastna kumulativa (563 + 3 blokov); trenutna = 569 (P125)
BLOCKS_04455 = 49                      # dokaz stats (46 + 3); trenutna = 61 (P126)
BLOCKS_04455_TS = 171   # POSODABLJENO P144: 164 (P142-era) → 168 (P143: +4 — ZAMUDA SANIRANA!) → 169 (P144: +1 h82!)   # P140: + 6 blokov 1911
P80_HOUSES = 48                       # POPRAVEK: 47 → 48 (+h52 NOVA v vzorcu; h16 že v mrliškem)
DATE_COUNTS = {"januar": 0, "februar": 8, "marec": 0, "april": 0, "maj": 5,
               "junij": 2, "julij": 0, "avgust": 0, "september": 1,
               "oktober": 0, "november": 0, "december": 0}
# P124 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p124)
BLOCK_PINS = [
    ("16", "NOVA HIŠA"),
    ("16", "BRODARIČ"),
    ("27", "3. poročni dokaz"),
    ("27", "HOMONIM"),
    ("27", "ZUGELJ"),
    ("52", "NOVA HIŠA"),
    ("52", "PERDINEC"),
    ("52", "JAKOBIČ"),
]


def http_get(url, headers=None, tries=3):
    req = urllib.request.Request(url, headers=headers or UA)
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    return 0, str(last).encode()


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
    check("I1b entries=16", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=0", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1d anomalije=8", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=20", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (16/16)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 skeni 94–96", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2b strani 93–95", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    check("I2c Pag. == sken − 1 (10. potrditev)", "sken − 1" in fr.get("pagRule", ""), fr.get("pagRule", "")[:60])
    check("I2d velika glava 1895 na s94 (P124 lead POTRJEN)",
          "s94" in fr.get("bigHeader", "") and "1895" in fr.get("bigHeader", ""),
          fr.get("bigHeader", "")[:70])
    rows_f = fr.get("rows", {})
    check("I2e vrstice s94/s95/s96", all(k in rows_f for k in ("s94", "s95", "s96")), str(list(rows_f.keys())))
    rows = [e["row"] for e in d["entries"]]
    check("I2f vrstice 1–16 zapored", rows == list(range(1, 17)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 94–96", all(94 <= s <= 96 for s in sc), str(sorted(set(sc))))
    per = {94: 6, 95: 5, 96: 5}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 6+5+5", raz == per, str(raz))
    lead = d.get("lead", {})
    check("I2i P125 lead (poročna 1896, s97)", "P125" in lead.get("next", "") and "1896" in lead.get("next", "")
          and "s97" in lead.get("frame", ""), f'{lead.get("next", "")} | {lead.get("frame", "")[:40]}')

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [10,11,13]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 3 (3 bloki!)", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3a Griblje hiše = [16,27,52]", d["stats"].get("gribljeHouses") == GRIBLJE_HOUSES,
          str(d["stats"].get("gribljeHouses")))
    e6 = d["entries"][5]
    check("I3b v6 POPRAVEK 40→54 + vdovec (smrtni list) + Croalien + Broj 485",
          e6["groom"]["age"] == 54 and "Croalien" in e6["groom"]["village"]
          and "Smrtni list" in e6["urkunden"] and "Broj 485" in e6["urkunden"],
          f'v6 starost {e6["groom"]["age"]}; {e6["urkunden"][:50]}')
    e15 = d["entries"][14]
    check("I3c v15 VOJSKA-ČASTNIK: Oberleutnant + k.k. Hauptmann priča + Garnison i. Propstei + mestna občina št:150",
          "Oberleutnant" in e15["groom"]["stand"] and "Hauptmann" in json.dumps(e15["witnesses"], ensure_ascii=False)
          and "Garnison i. Propstei" in e15["urkunden"] and "150" in e15["urkunden"],
          f'{e15["groom"]["name"]}: {e15["groom"]["stand"]}')
    e8 = d["entries"][7]
    check("I3d v8 2. LANDSREGIERUNG №181 (6.2.1895) + dispens №613 2. st. svarstva",
          "Landesregierung" in e8["urkunden"] and "181" in e8["urkunden"] and "613" in e8["urkunden"],
          e8["urkunden"][:70])
    e7 = d["entries"][6]
    check("I3e v7 DISPENS 3. st. krvno №504 (Ordinariat Laibach 13.2.)",
          "504" in e7["urkunden"] and "3ten Grade" in e7["urkunden"] and "Blutsverwandtschaft" in e7["urkunden"],
          e7["urkunden"][:70])
    e12 = d["entries"][11]
    check("I3f v12 WITTWENSCHAFT-dispens Ž4994 (Bez. Gft Črnomelj — PO poroki!)",
          "4994" in e12["urkunden"] and "Wittwenschaft" in e12["urkunden"] and "Črnomelj" in e12["urkunden"],
          e12["urkunden"][40:110])
    e11 = d["entries"][10]
    check("I3g v11 HOMONIM Marcus Perdinec (f. Marcus — ≠ P123 v3 f. Michaël) + h27 + Zugelj",
          e11["groom"]["houseNo"] == 27 and e11["parentsGroom"].startswith("Marcus Perdinec")
          and "Zugelj" in e11["bride"]["name"] and e11["groom"]["age"] == 34,
          f'{e11["groom"]["name"]} h27; starši: {e11["parentsGroom"][:40]}')
    e10 = d["entries"][9]
    check("I3h v10 NOVA HIŠA h16 (Anton Brodarič) + občina Griblje №1",
          e10["groom"]["houseNo"] == 16 and "Brodarič" in e10["groom"]["name"] and "Griblje" in e10["urkunden"],
          f'{e10["groom"]["name"]} h16 × {e10["bride"]["name"]}')
    e13 = d["entries"][12]
    check("I3i v13 NOVA HIŠA h52 (Mathias Perdinec f. Johann — 2. veja!) + občina Griblje št:3",
          e13["groom"]["houseNo"] == 52 and e13["parentsGroom"].startswith("Johann Perdinec")
          and "Griblje" in e13["urkunden"],
          f'{e13["groom"]["name"]} h52 × {e13["bride"]["name"]}')
    e4 = d["entries"][3]
    check("I3j v4 DVA PRIČA ISTO IME Peter Jakofčič ×2 + MAYD nevesta",
          e4["witnesses"] == ["Peter Jakofčič", "Peter Jakofčič (} ½ gbl)"]
          and "Mayd" in e4["bride"]["stand"],
          f'priče: {e4["witnesses"]}; {e4["bride"]["name"]}')
    e3 = d["entries"][2]
    check("I3k v3 MLADOLETNA nevesta 17 (najmlajša!) + Müllers Knecht + občina Adlešiči",
          e3["bride"]["age"] == 17 and "Knecht" in e3["groom"]["name"] and "Adlešič" in e3["urkunden"],
          f'{e3["groom"]["name"]} × {e3["bride"]["name"]} 17')
    e16 = d["entries"][15]
    check("I3l v16 4. DISPENS (3.[u2.?] lineae collateralis) + Kloster [~] + JAKŠA obe mati",
          "lineae collateralis" in e16["urkunden"] and "Kloster" in e16["bride"]["village"]
          and "Jakša" in e16["parentsGroom"] and "Jakša" in e16["parentsBride"],
          f'{e16["groom"]["name"]} × {e16["bride"]["name"]}')
    e9 = d["entries"][8]
    check("I3m v9 dokument za OBA partnerja (Bräutigam und Braut — edini!) + Zumrič",
          "Bräutigam und" in e9["urkunden"] and "Zumrič" in json.dumps(e9, ensure_ascii=False),
          f'{e9["groom"]["name"]} × {e9["bride"]["name"]}')
    e2 = d["entries"][1]
    check("I3n v2 Großjährigkeits-Priznanje (Bez. Ger. Möttling 19/1.)",
          "Großjährigkeits" in e2["urkunden"] and "Möttling" in e2["urkunden"],
          e2["urkunden"][:80])
    e14 = d["entries"][13]
    check("I3o v14 2. Johann Starasinič (f. Michaël — HOMONIM v8!) + Großjährigkeits-Erklärung 21/5.",
          "Starasinič" in e14["groom"]["name"] and e14["parentsGroom"].startswith("Michaël Starasinič")
          and "Großjährigkeits" in e14["urkunden"],
          f'{e14["groom"]["name"]} (oče Michaël) × {e14["bride"]["name"]}')
    same1 = [e["row"] for e in d["entries"] if e["date"].startswith("11.2.")]
    same2 = [e["row"] for e in d["entries"] if e["date"].startswith("19.5.")]
    same3 = [e["row"] for e in d["entries"] if e["date"].startswith("26.5.")]
    check("I3p trojni dnevi 11.2. = [1,2,3] + 19.5. = [9,10,11] + 26.5. = [12,13]",
          same1 == [1, 2, 3] and same2 == [9, 10, 11] and same3 == [12, 13],
          f'{same1} + {same2} + {same3}')
    un = sum(1 for e in d["entries"] if "in Ungarn" in e["urkunden"] or "in Un" in e["urkunden"])
    check("I3q formula »in Ungarn« ×5 (v1/v3/v5/v13 + v15 varianta)", un == 5, f'x{un}')
    mo = sum(1 for e in d["entries"] if "Möttling" in e["urkunden"])
    check("I3r Bez. Ger. Möttling ×4 (= nemško ime Metlike!)", mo == 4, f'x{mo}')
    zug = sum(1 for e in d["entries"] if "Zugelj" in json.dumps(e, ensure_ascii=False))
    check("I3s ZUGELJ ×2 vpisa / 4 osebe (v8 geb. + v11 nevesta + 2 očeta)", zug >= 2, f'x{zug}')

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
    check("I4 meseči (vsota 16; februar 8 = zimska koncentracija!)",
          not bad_m and sum(mc.values()) == 16, str(bad_m or sum(mc.values())))
    check("I4b v15 mestna občina Metlika št: 150 (2. mestna občina linije!)",
          "150" in e15["urkunden"] and "mestne občine Metlika" in e15["urkunden"],
          e15["urkunden"][:60])
    check("I4c v12 dispens datiran PO poroki (26.5. -> 5/6.) — vzorec P123 Ž8667",
          "5/6." in e12["urkunden"] or "8/6." in e12["urkunden"], "v12 urkunden")

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki: Rauy ×16/16 (3. leto zapored monopol!)",
          pr.get("Jos. Rauy") == 16 and len(pr) == 1, str(pr))
    check("I5b vitals=566 (563 + 3 P124; trenutna 569 P125)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5c bloki 04455=49 (trenutna 52 P125)", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5d p80 hiše=48 (+h52 NOVA; h16 že v mrliškem!)", st.get("p80Houses") == P80_HOUSES,
          str(st.get("p80Houses")))
    ag = st.get("ageGrooms", {})
    ab = st.get("ageBrides", {})
    check("I5e ženin max=54 (v6 POPRAVLJEN!) + min=23", ag.get("max") == 54 and ag.get("min") == 23, str(ag))
    check("I5f nevesta max=37 (v6) + min=17 (v3 MLADOLETNA!)", ab.get("max") == 37 and ab.get("min") == 17, str(ab))
    check("I5g mladoletne neveste=8 + ženini=1 (9/30, ABGB-24)",
          st.get("underageBrides") == 8 and st.get("underageGrooms") == 1,
          f'{st.get("underageBrides")}/{st.get("underageGrooms")}')
    check("I5h dispensacije=4 (REKORD linije! v7/v8/v12/v16)", st.get("dispensations") == 4,
          str(st.get("dispensations")))
    fd = st.get("foreignDocuments", {})
    check("I5i tuji dokumenti: Möttling ×4 + Ordinariat ×2 + Landesreg. + Črnomelj + mestna-Metlika + Garnisons-Propstei + občine (Podzemelj ×5/Gradac ×4/Adlešiči ×2/Griblje ×4)",
          fd.get("BezGer-Möttling") == 4 and fd.get("Ordinariat-Laibach") == 2
          and fd.get("Landesregierung-Laibach") == 1 and fd.get("BezGer-Črnomelj") == 1
          and fd.get("mestna-občina-Metlika") == 1 and fd.get("Garnisons-Propstei-Metlika") == 1
          and fd.get("občina-Podzemelj") == 5 and fd.get("občina-Gradac") == 4
          and fd.get("občina-Adlešiči") == 2 and fd.get("občina-Griblje") == 4,
          str(fd))

    # ---------- I6: anomalije A1–A8 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A8", ids == [f"A{i}" for i in range(1, 9)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I6b A1 = VOJSKA-ČASTNIK (Oberleutnant + Hauptmann)", a1.get("type") == "VOJSKA-CASTNIK"
          and "OBERLEUTNANT" in a1.get("text", ""), a1.get("text", "")[:60])
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6c A2 = HRVAŠKA-VLOGA (Croalien + Broj 485)", a2.get("type") == "HRVAŠKA-VLOGA"
          and "485" in a2.get("text", ""), a2.get("text", "")[:60])
    a4 = next((a for a in d["anomalies"] if a["id"] == "A4"), {})
    check("I6d A4 = DISPENS-REKORD ×4", a4.get("type") == "DISPENS-REKORD" and "504" in a4.get("text", "")
          and "613" in a4.get("text", "") and "4994" in a4.get("text", ""), a4.get("text", "")[:60])
    a6 = next((a for a in d["anomalies"] if a["id"] == "A6"), {})
    check("I6e A6 = HOMONIMI (Perdinec + Starasinič)", a6.get("type") == "HOMONIMI"
          and "PERDINEC" in a6.get("text", "") and "STARASINIČ" in a6.get("text", ""), a6.get("text", "")[:60])
    a7 = next((a for a in d["anomalies"] if a["id"] == "A7"), {})
    check("I6f A7 = DVOJNI-PRIČA (Jakofčič ×2)", a7.get("type") == "DVOJNI-PRIČA"
          and "Jakofčič" in a7.get("text", ""), a7.get("text", "")[:60])

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C20", cc_ids == [f"C{i}" for i in range(1, 21)], str(cc_ids[-3:]))
    c1 = next((c for c in d["crossChecks"] if c.get("id") == "C1"), {})
    check("I7b C1 = GRIBLJE-POROKE ×3 (h16+h27+h52)", c1.get("type") == "GRIBLJE-POROKE" and "h52" in c1.get("text", ""),
          c1.get("text", "")[:60])
    c2 = next((c for c in d["crossChecks"] if c.get("id") == "C2"), {})
    check("I7c C2 POROKE-NA-ISTI-DAN 3+3+2", "8 od 16" in c2.get("text", ""), c2.get("text", "")[:60])
    c8 = next((c for c in d["crossChecks"] if c.get("id") == "C8"), {})
    check("I7d C8 MÖTTLING=METLIKA (4 dokumentov)", "4 dokumentov" in c8.get("text", "")
          and "METLIK" in c8.get("text", ""),
          c8.get("text", "")[:60])
    c10 = next((c for c in d["crossChecks"] if c.get("id") == "C10"), {})
    check("I7e C10 OBČINA-GRIBLJE ×4 (Broj 485 + №1 + št:2 + št:3)", "×4" in c10.get("text", "")
          and "485" in c10.get("text", ""), c10.get("text", "")[:60])
    c16 = next((c for c in d["crossChecks"] if c.get("id") == "C16"), {})
    check("I7f C16 RAUY-MONOPOL 16/16 (3. leto)", "16/16" in c16.get("text", ""), c16.get("text", "")[:60])
    c20 = next((c for c in d["crossChecks"] if c.get("id") == "C20"), {})
    check("I7g C20 status-neznanki ×15+", "×15+" in c20.get("text", ""), c20.get("text", "")[:60])
    # P123 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d123 = json.load(open(DOKAZ_P123))
        check("I7h P123 dokaz stats vitals=563 + bloki=46",
              d123["stats"].get("vitals") == 563 and d123["stats"].get("blocks04455") == 46,
              f'v{d123["stats"].get("vitals")} b{d123["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7h P123 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P123 46 + P124 3 + P125 3 + P126 9 + P127 9 + P129 +2 + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1895 = sorted((h for h, y, _ in blocks_m if y == "1895"), key=int)
    check("I8b hiše 1895 = [14,16,24,27,52] (P125 +h14/h24!)", ",".join(h1895) == "14,16,24,27,52", ",".join(h1895))
    h1894 = sorted((h for h, y, _ in blocks_m if y == "1894"), key=int)
    check("I8c hiše 1894 nespremenjene", ",".join(h1894) == "9,11,27,42", ",".join(h1894))
    h1893 = sorted((h for h, y, _ in blocks_m if y == "1893"), key=int)
    check("I8d hiše 1893 nespremenjene", ",".join(h1893) == "26,58,62,69,74", ",".join(h1893))
    h1892 = sorted((h for h, y, _ in blocks_m if y == "1892"), key=int)
    check("I8e hiše 1892 nespremenjene", ",".join(h1892) == "17,30,36,60", ",".join(h1892))
    h1891 = sorted((h for h, y, _ in blocks_m if y == "1891"), key=int)
    check("I8f hiše 1891 nespremenjene", ",".join(h1891) == "20,87", ",".join(h1891))
    h1890 = sorted((h for h, y, _ in blocks_m if y == "1890"), key=int)
    check("I8g hiše 1890 nespremenjene", ",".join(h1890) == "10,53,61,91", ",".join(h1890))
    h1889 = sorted((h for h, y, _ in blocks_m if y == "1889"), key=int)
    check("I8h hiše 1889 nespremenjene", ",".join(h1889) == "7,21,30,32,40,54,87", ",".join(h1889))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8i hiše 1888 nespremenjene", ",".join(h1888) == "23,32,33,64", ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8j hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8k hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1895 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1895,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8l pini P124 (8)", not missing, str(missing) if missing else "vse ✓")
    # oznake dokazov 1895
    check("I8m h16/h52 = NOVA HIŠA + h27 = 3. poročni dokaz + HOMONIM",
          any(m.group(1) == "27" and "3. poročni dokaz" in m.group(2) and "HOMONIM" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1895,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)),
          "h27 pin")

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p124", '"qa-p124-parish-marriage-1895"' in qa)
    check("I9b p80 bloki 78", "poročni vpisi (04455) ≠ 158" in qa)
    check("I9[cd] p80 sidra 72 (1895×5 + 1896×1 + 1897×9 + 1898×9 · 1899×6 · 1900×2!)", "poročna sidra ≠ 164" in qa)
    check("I9d p80 hiše 58 (qa kumulativa — …; P127: +6 NOVIH!)", "različnih hiš (vse tri knjige) ≠ 70" in qa)
    check("I9e PT luknja 12 (+h52/h46/h48)", "PT luknja ≠ 13 hiš" in qa)
    # vitals 569 regresijska zaščita v qa-p124
    check("I9f vitals 637 zaščita (P128)", "HOUSE_VITALS.length !== 714" in qa[qa.index("const p124Marr"):] if "const p124Marr" in qa else False)
    check("I9g stari 537/544/548/550/554/559/563 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa and "HOUSE_VITALS.length !== 550" not in qa
          and "HOUSE_VITALS.length !== 554" not in qa and "HOUSE_VITALS.length !== 559" not in qa
          and "HOUSE_VITALS.length !== 563" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P124", "P124" in rd and ("126/126" in rd or "po P124" in rd))
    nt = open("research/issue17/parish-marriage-1895-notes.md").read()
    check("I10b notes faza 2 + ČASTNIK", "FAZA 2" in nt and "ČASTNIK" in nt)

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
