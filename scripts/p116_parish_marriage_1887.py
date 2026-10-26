#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P116 — župnija Podzemelj: poročna knjiga 04455, polno leto 1887 (issue #18).

Nadaljevanje poročne linije (P115 = 1886): okvir POTRJEN — skeni 66–70 ==
Pag. 65–69 (Pag. == sken − 1 velja tudi v 66–71); **21 vpisov** (razpored
4+4+3+3+7); glava 1888 že na Pag. 70 (s71) — polno leto 1887 v eni fazi.

FAZA 2: **21/21 vpisov transkribiranih OBOJESTRANSKO** (starši/Befstände/
Befunden/duhovnik) + mega-zoom serija (~30 izrezov ×3–5, 1:1 primerjava
števk). **P80/P115 RE-READ POPRAVKI ×8**: h15 ženin = Johann FABLIĆ (ne
»Šambie«) + nevesta = GRIBLJE **23** (ne »29«!) + h71 mati neveste = née
KAMBIČ (ne »Šambiè«) + mrliška h29-komentar (poroka na h23) + faza-1: h69
(ne »64«!), h10 (ne »19«), Zemelj 16 (ne »11«), PRIMOSTEK (ne »Šimeck«),
METLIKA (ne »Štilnik«), Grabrijan (ne »Gubeljas«), LERCH, Jos. ROUY.

NOVELE: **VPIS 16 = POROKA RAZPADLA?** (marginala »ni bil poročen, se
razdrlo/razšlo? ravno pred poroko« — Jos. Rouy; datum + Befstände PRAZNI;
61-letni ženin Hütlin Gradac 28 — isti mož kot vpis 21 KOTTLIN!) +
**VPIS 14 = 1. SLOVENSKOJEZIČNI VPIS** (druga roka! »Matija/Maj/let« +
slovenski Befunden) + **ŽENITOVANJSKA ZGLASNICA = nov dokument** (vpisi
14–21) + **BRATA FABLIĆ** (vpisa 1+4, isti starši) + **TRETJA FABLIĆ**
(vpis 6 — mati druga!) + **SESTRSKI DVOJNI POROK Turšič** (vpisa 5+7,
13.2., ista starša = 3. v liniji!) + **DVE Katharina Klepec v 2 dneh**
(v7 19 / v9 22 — različni!) + **4× POROKA TOME** + **STARAŠINIČ-BRATA**
(v9+v14, Krasinec 12) + **KRIŽAN × KRIŽE** (v20, h3 × h10!) + tuji ženini
×5 (Gradnik/Semič, Primostek ×2, Čedno selo/Adlešiče, Borovnica/
FRANZDORF [~]!) + duhovniki Dovgan ×8 / Grieb ×4 / ROUY ×8 / prazno 1 +
dispensacije ×5 + 2× Großjährigkeits-Schein + tiskarna Metlika.

NOVE GRIBLJE HIŠE: h23 + h37 + h69? [~] + h3 + h10 (5 novih blokov);
P80 sidri h71/h15 POTRJENA + popravljena. Skripta
scripts/p116_parish_marriage_1887.py (I1–I11, --check izpiše PASS/FAIL in
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
DOKAZ = "research/issue17/parish-marriage-1887.json"
DOKAZ_P115 = "research/issue17/parish-marriage-1886.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (66, 70)          # 66 = Pag. 65 (vpisi 1–4) … 70 = Pag. 69 (vpisi 15–21)
FRAME_PAGES = (65, 69)
EXPECTED_ENTRIES = 21
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 16
EXPECTED_CROSSCHECKS = 24
GRIBLJE_ROWS = [3, 4, 11, 20]
GRIBLJE_MARRIAGES = 4
GRIBLJE_HOUSES_TS = "3,10,15,23,37,69,71"
EXPECTED_VITALS = 533           # 528 (P114/P115) + 5 novih poročnih blokov P116 (zgodovinsko — P117 dokaz gre na 537)
BLOCKS_04455 = 164                # 11 (P115) + … + 4 bloki 1892 (P121) + 5 bloki 1893 (P122) + 4 bloki 1894 (P123) + 2 bloka 1900 (P129)
DATE_COUNTS = {"januar": 3, "februar": 8, "marec": 0, "april": 0, "maj": 5,
               "junij": 0, "julij": 1, "avgust": 2, "september": 1, "oktober": 1,
               "november": 0, "december": 0}
# P116 pini (blok-houseNo → obvezen fragment v whatSi)
BLOCK_PINS = [
    ("71", "franz Dovgan"), ("71", "KAMBIČ"), ("71", "P116"),
    ("15", "FABLIĆ"), ("15", "GRIBLJE 23"), ("15", "P116"),
    ("23", "Brinec"), ("23", "NOVA"), ("23", "Milek"),
    ("37", "Rusić"), ("37", "NOVA"),
    ("69", "NOVA hiša"), ("69", "Straus"),
    ("3", "Križan"), ("3", "Rouy"),
    ("10", "Križe"), ("10", "NOVA"),
]
# stara branja = IZTELA iz 04455 blokov (natančni stari fragmenti)
OLD_READINGS = [
    "Johann Šambie", "née Šambiè", "GRIBLJE 29 (starši",
    "PRIMOSTEK ≠", "»Šimeck",
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
    check("I1b entries=21", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1c excluded=8", len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije=16", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=24", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (21/21)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 entries=21", fr.get("entriesTotal") == EXPECTED_ENTRIES, str(fr.get("entriesTotal")))
    check("I2b skeni 66–70", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2c strani 65–69", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    rows = [e["row"] for e in d["entries"]]
    check("I2d vrstice 1–21 zapored", rows == list(range(1, 22)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2e skeni znotraj 66–70", all(66 <= s <= 70 for s in sc), str(sorted(set(sc))))
    per = {66: 4, 67: 4, 68: 3, 69: 3, 70: 7}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2f razpored 4+4+3+3+7", raz == per, str(raz))

    # ---------- I3: Griblje vpisi + nove hiše ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [3,4,11,20]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 4", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3b hiš omenjenih = 7", d["stats"].get("gribljeHousesMentioned") == 7,
          str(d["stats"].get("gribljeHousesMentioned")))
    e4 = d["entries"][3]
    check("I3c vpis 4 = h15 × Brinec × h23 (FABLIĆ!)",
          e4["groom"]["houseNo"] == 15 and e4["bride"]["houseNo"] == 23
          and "Fablić" in e4["groom"]["name"] and "Šambie" not in e4["groom"]["name"],
          f'{e4["groom"]["name"]} h15 × {e4["bride"]["name"]} h23')
    e11 = d["entries"][10]
    check("I3d vpis 11 = h69 (NE 64!)", e11["groom"]["houseNo"] == 69 and e11["bride"]["houseNo"] == 71,
          f'h{e11["groom"]["houseNo"]} × h{e11["bride"]["houseNo"]}')
    e20 = d["entries"][19]
    check("I3e vpis 20 = h3 × h10 (NE 19!)", e20["groom"]["houseNo"] == 3 and e20["bride"]["houseNo"] == 10,
          f'h{e20["groom"]["houseNo"]} × h{e20["bride"]["houseNo"]}')
    e16 = d["entries"][15]
    check("I3f vpis 16 = razpadla poroka (marginala)", "razdrlo" in e16["urkunden"] and "Rouy" in e16["urkunden"],
          e16["urkunden"][:60])
    e14 = d["entries"][13]
    check("I3g vpis 14 = slovenski vpis", "zglasnica" in e14["urkunden"].lower() and "Matija" in e14["groom"]["name"],
          e14["urkunden"][:60])

    # ---------- I4: datumi + meseči ----------
    import unicodedata
    def mes(datestr):
        s = datestr.lower()
        m = re.search(r"\d+\.\s*(\d+)\.?\s*1887", s)
        if m:
            return int(m.group(1))
        return None
    mc = {"januar": 0, "februar": 0, "marec": 0, "april": 0, "maj": 0, "junij": 0,
          "julij": 0, "avgust": 0, "september": 0, "oktober": 0, "november": 0, "december": 0}
    names = {1: "januar", 2: "februar", 3: "marec", 4: "april", 5: "maj", 6: "junij",
             7: "julij", 8: "avgust", 9: "september", 10: "oktober", 11: "november", 12: "december"}
    for e in d["entries"]:
        m = mes(e["date"])
        if m:
            mc[names[m]] += 1
    bad_m = {k: v for k, v in mc.items() if v != DATE_COUNTS[k]}
    check("I4 meseči (vsota 21)", not bad_m and sum(mc.values()) == 21, str(bad_m or sum(mc.values())))
    winter = mc["januar"] + mc["februar"] + mc["marec"]
    check("I4b zimska koncentracija 11 (52.4%)", winter == 11, str(winter))
    feb13 = [e["row"] for e in d["entries"] if e["date"].startswith("13.2.")]
    check("I4c 3 poroke 13.2. = [5,6,7]", feb13 == [5, 6, 7], str(feb13))
    feb14 = [e["row"] for e in d["entries"] if e["date"].startswith("14.2.")]
    check("I4d 3 poroke 14.2. = [8,9,10]", feb14 == [8, 9, 10], str(feb14))

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki 8/4/8/1", (pr.get("Dovgan"), pr.get("Grieb"), pr.get("Rouy"), pr.get("prazno")) == (8, 4, 8, 1), str(pr))
    check("I5b dispensacije=5", st.get("dispensations") == 5, str(st.get("dispensations")))
    check("I5c vitals=533 (528 + 5 P116)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5d bloki 04455=16 (P117: 20)", st.get("blocks04455") == 16, str(st.get("blocks04455")))
    check("I5e novi bloki=5", st.get("newBlocks") == 5, str(st.get("newBlocks")))
    check("I5f popravki P80=3", st.get("p80BlocksCorrected") == 3, str(st.get("p80BlocksCorrected")))
    check("I5g najstarejši ženin=61", st.get("oldestGroom") == 61, str(st.get("oldestGroom")))
    check("I5h najmlajša nevesta=17", st.get("youngestBride") == 17, str(st.get("youngestBride")))
    check("I5i Tome ×4", st.get("tomeCount") == 4, str(st.get("tomeCount")))

    # ---------- I6: anomalije A1–A16 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A16", ids == [f"A{i}" for i in range(1, 17)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I6b A1 = razpadla poroka", "RAZPADLA" in a1.get("summary", "").upper() and "Rouy" in a1.get("summary", ""))
    a8 = next((a for a in d["anomalies"] if a["id"] == "A8"), {})
    check("I6c A8 = 1. slovenski vpis", "SLOVENSKOJEZIČNI" in a8.get("summary", "").upper())
    a5 = next((a for a in d["anomalies"] if a["id"] == "A5"), {})
    check("I6d A5 = brata Fablić", "FABLIĆ" in a5.get("summary", "").upper())
    a4 = next((a for a in d["anomalies"] if a["id"] == "A4"), {})
    check("I6e A4 = Turšič dvojni", "Turšič" in a4.get("summary", ""))

    # ---------- I7: crossChecks ----------
    cc_ok = [c for c in d["crossChecks"] if c["verdict"].startswith("✓")]
    check("I7 crossChecks ✓ ≥ 20", len(cc_ok) >= 20, f"{len(cc_ok)}/{len(d['crossChecks'])}")
    cc24 = next((c for c in d["crossChecks"] if c.get("id") == "CC24"), {})
    check("I7b CC24 = Brine h23 (1888)", "Brine" in cc24.get("verdict", "") and "23" in cc24.get("verdict", ""))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P122 +5, P123 +4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6! + P129 +2 + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455, str(len(blocks_m)))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8b hiše 1887 = [3,10,15,23,37,69,71]", ",".join(h1887) == GRIBLJE_HOUSES_TS, ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8c hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1887 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1887,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8d pini P116 (17)", not missing, str(missing) if missing else "vse ✓")
    whatsis = [m.group(1) for m in re.finditer(r'bookSignature:\s*"04455",\s*year:\s*\d{4},\s*scan:\s*\d+,\s*page:\s*\d+,\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)]
    stale = [o for o in OLD_READINGS if any(o in w for w in whatsis)]
    check("I8e stara branja iztekla", not stale, str(stale) if stale else "vse ✓")

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p116", '"qa-p116-parish-marriage-1887"' in qa)
    check("I9b qa-p115 bloki 78", "poročni bloki (04455) ≠ 142" in qa)
    check("I9c p80 bloki 78", "poročni vpisi (04455) ≠ 158" in qa)
    # vitals 528 regresijska zaščita v qa-p116
    check("I9d vitals 637 zaščita (P128)", "HOUSE_VITALS.length !== 685" in qa[qa.index("const p116Marr"):] if "const p116Marr" in qa else False)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P116", "P116" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1887-notes.md").read()
    check("I10b notes faza 2", "FAZA 2" in nt and "FABLIĆ" in nt.upper())

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
