#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P122 — župnija Podzemelj: poročna knjiga 04455, polno leto 1893 (issue #18).

Nadaljevanje poročne linije (P115 = 1886 → … → P121 = 1892): okvir POTRJEN —
skeni 87–90 == Pag. 86–89 (Pag. == sken − 1, 8. potrditev; velja v 61–91);
**20 vpisov** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 →
1892:15 → 1893:20 = 2. največje leto linije!; razpored 6+5+5+4); **VELIKA
GLAVA »Traunungs=Buch« + rokopisno »1893« POTRJENA na s87** (P122 lead!;
cikel velike glave: 1887 s66 + 1890 s77 + 1892 s84 + 1893 s87; 1891 brez =
izjema). LANDSCAPE geometrija (~2512–2524×1800; s91 = Pag. 90 = glava 1894
+ v1–6/1894 = P123 lead).

FAZA 2: **20/20 vpisov transkribiranih OBOJESTRANSKO** + 40 row-crops ×2
LANCZOS + ~40 mikro-zoomov ×3–6 (crop_rows_122.py, z*_*.png).
NOVELE: **DRUBEL-GRIBLJE poroke ×2** (v15 h69×h62 + v16 h58×h74) + v10
nevesta **GRIBLJE 26 NOVA HIŠA** (P122 lead popravka 26 NE 36!) = 3 poroke /
5 hiš — **7 POROK NA ISTI DAN 6.2. = REKORD VSEH ČASOV LINIJE** (prej 4 —
P121 22.2.!) + **BRAT-SESTRA PERDINEC DVOZAKON ISTI DAN** (v4 ženin + v6
nevesta — ISTI starša Georg Perdinec × Cathar. Klepec! = 3. tak primer) +
**★ RENOVACIJA ZAKONA 8.9.1898** (v8 — latinski blok: dispensacija 3. st.
transversa ab Antonio Jos. Jeglič [~ — cf. bodoči škof ljubljanski!] +
renovacija consensus Podzemelj 8.9.1898, priči Franc Maur Cooperatore +
Martin Skala — NOV DOKUMENT-TIP LINIJE) + **★ 2. DUHOVNIK LINIJE Michael
KLEMENČIČ Coop. ×2** (v10+v11, 30.4. — konec Rauy-monopola od P117; Rauy
vseeno ×18) + **★ 1. DOKUMENT OBČINE GRIBLJE** v poročni liniji (v15) +
občina Tribuče NOVA (v20) + »GJUPNIJSKI urad« (hrvaška oblika!) ×3 (v9/v10/
v20 Adlešiči) + **★ VOJSKA**: nadvarstveno dovoljenje voj. okrožja RUDOLFOVO
(Rudolfswerth = Novo mesto!) za mladoletno nevesto + proxy-zastopstvo (v12,
v imenu Franca Marentiča priča Martin Novacič!) + v17 rod. pf. Smihelj b.
Rudolfswerth (~50 km — najdaljši lok 1893) + **★ DISPENSACIJA 3. KAN.
STOPNJE №1661** (v16 — Ordinariat Laibach 17.7.1893, 6 dni pred poroko;
starša neveste Mathias Kambič × Catharina BRINEC — OBA MATERI BRINC!) +
**★ INHABER = NOV STATUS** (v19 Michael Murn — imetnik!) + 2 status-neznanki
(v17 »Kronft« + v4 »K?ña's=tochter«) + **deleži ¼/½ ×32 oseb** (vsi vpisi!)
+ anomala »1« namesto ulomka (v5 nevesta + njen oče) + **rekordi starosti**:
ženin 58 (v13 Kambič!) + nevesta 17 (v5 Marentič — TIED rekord mladosti z
P121 v1!) + mladoletnost 12/40 (ABGB-24, dokumenti 100% skladni, 7. leto!)
+ **Laipšl ×8 (3. leto mreže!)** + KAMBIČ ×5 = najmočnejši priimek + BRINC
×5 + PEZDIREC-cluster ×6 (3 pisave!) + MUC ×2 + KURE ×3 + SKALA ×2 (isti
mož priča 1893 IN renovaciji 1898!) + zimska koncentracija jan+feb 8/20.

GRIBLJE: 3 poroke / 5 poročnih blokov (h26 v10 nevesta NOVA + h69 v15 ženin
2. dokaz po 1887 + h62 v15 nevesta NOVA + h58 v16 ženin 1. DOKAZ SPLOH! +
h74 v16 nevesta NOVA — krstna 1893+1911 ISTO LETO v obeh knjigah!) —
**bloki 04455 = 46 (P122: 42 + P123: 4); vitals 563; p80 hiše 44 po P122 (+h26/h58/h62 NOVE;
h69/h74 že prek 1887 poročne/mrliške 1886!) → 47 po P123 (+h9/h27/h42)**.
Skripta scripts/p122_parish_marriage_1893.py (I1–I11, --check izpiše
PASS/FAIL in vrne exit code; --live omogoči HTTP preverjanje
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
DOKAZ = "research/issue17/parish-marriage-1893.json"
DOKAZ_P121 = "research/issue17/parish-marriage-1892.json"
PARISH_TS = "src/data/atlas/parish.ts"
QA_TS = "src/lib/qa-parish.ts"

FRAME_SCANS = (87, 88, 89, 90)  # 87 = Pag. 86 (velika glava 1893 + v1–6) · 88 = Pag. 87 (v7–11) · 89 = Pag. 88 (v12–16) · 90 = Pag. 89 (v17–20)
FRAME_PAGES = (86, 87, 88, 89)
EXPECTED_ENTRIES = 20
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 8
EXPECTED_CROSSCHECKS = 20
GRIBLJE_ROWS = [10, 15, 16]
GRIBLJE_MARRIAGES = 3
GRIBLJE_HOUSES = [26, 58, 62, 69, 74]
GRIBLJE_HOUSES_TS = "26,58,62,69,74"  # hiše z 1893 bloki v parish.ts (v10 h26 + v15 h69/h62 + v16 h58/h74)
EXPECTED_VITALS = 559                 # P122 dokaz lastna kumulativa (554 + 5 blokov)
BLOCKS_04455 = 42                     # 37 (P121) + 5 novih blokov 1893 (P122)
BLOCKS_04455_TS = 94              # P126: + 9 blokov 1897 (61) + P127: + 9 blokov 1898 (70)
P80_HOUSES = 44                       # POPRAVEK (P123 sinhronizacija): 41 → 44 (+h26/h58/h62 NOVE v vzorcu; h69/h74 že prek 1887/mrliške!)
DATE_COUNTS = {"januar": 1, "februar": 7, "marec": 0, "april": 3, "maj": 2,   # april = v9 23.4. + v10 + v11 (30.4. ×2); avgust = v18 + v19
               "junij": 2, "julij": 2, "avgust": 2, "september": 0, "oktober": 0,
               "november": 1, "december": 0}
# P122 pini (blok-houseNo → obvezen fragment v whatSi; cf. qa-p122)
BLOCK_PINS = [
    ("26", "NOVA HIŠA"), ("26", "KRALJ"), ("26", "KLEMENČIČ"), ("26", "GJUPNIJSKEGA"), ("26", "Fučkovec"),
    ("69", "DRUBEL-GRIBLJE"), ("69", "h62"), ("69", "KURE"), ("69", "2. poročni dokaz h69"), ("69", "ADLEŠIČ"),
    ("62", "NOVA hiša"), ("62", "KURE"), ("62", "KRIŽAN"), ("62", "drubel"),
    ("58", "POŽEK"), ("58", "DRUBEL-GRIBLJE"), ("58", "h74"), ("58", "1661"), ("58", "BRINEC"),
    ("74", "NOVA hiša"), ("74", "KAMBIČ"), ("74", "BRINEC"), ("74", "1661"),
]
OLD_READINGS = []


def http_get(url, headers=None, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except Exception:  # noqa: BLE001
            import time
            time.sleep(2 + i * 2)
            last = sys.exc_info()[1]
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
    check("I1c excluded=0", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1d anomalije=8", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1e crossChecks=20", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    bad = [e["row"] for e in d["entries"] if not e.get("parentsGroom") or not e.get("parentsBride")]
    check("I1f obojestransko (20/20)", not bad, str(bad) if bad else "vse ✓")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 skeni 87–90", tuple(fr.get("scans", ())) == FRAME_SCANS, str(fr.get("scans")))
    check("I2b strani 86–89", tuple(fr.get("pages", ())) == FRAME_PAGES, str(fr.get("pages")))
    check("I2c Pag. == sken − 1 (8. potrditev)", "sken − 1" in fr.get("pagRule", ""), fr.get("pagRule", "")[:60])
    check("I2d velika glava 1893 na s87 (P122 lead POTRJEN)",
          "s87" in fr.get("bigHeader", "") and "1893" in fr.get("bigHeader", ""),
          fr.get("bigHeader", "")[:70])
    rows_f = fr.get("rows", {})
    check("I2e vrstice s87/s88/s89/s90", all(k in rows_f for k in ("s87", "s88", "s89", "s90")), str(list(rows_f.keys())))
    rows = [e["row"] for e in d["entries"]]
    check("I2f vrstice 1–20 zapored", rows == list(range(1, 21)), str(rows))
    sc = [e["scan"] for e in d["entries"]]
    check("I2g skeni znotraj 87–90", all(87 <= s <= 90 for s in sc), str(sorted(set(sc))))
    per = {87: 6, 88: 5, 89: 5, 90: 4}
    raz = {}
    for e in d["entries"]:
        raz[e["scan"]] = raz.get(e["scan"], 0) + 1
    check("I2h razpored 6+5+5+4", raz == per, str(raz))
    lead = d.get("lead", {})
    check("I2i P123 lead (poročna 1894, s91)", "P123" in lead.get("next", "") and "1894" in lead.get("next", "")
          and "s91" in lead.get("frame", ""), f'{lead.get("next", "")} | {lead.get("frame", "")[:40]}')

    # ---------- I3: ključni vpisi ----------
    grows = [e["row"] for e in d["entries"] if e.get("griblje")]
    check("I3 Griblje vrstice = [10,15,16]", grows == GRIBLJE_ROWS, str(grows))
    check("I3-0 Griblje porok = 3 (5 hiš!)", d["stats"].get("gribljeMarriages") == GRIBLJE_MARRIAGES,
          str(d["stats"].get("gribljeMarriages")))
    check("I3a Griblje hiše = [26,58,62,69,74]", d["stats"].get("gribljeHouses") == GRIBLJE_HOUSES,
          str(d["stats"].get("gribljeHouses")))
    e4 = d["entries"][3]
    e6 = d["entries"][5]
    check("I3b v4+v6 BRAT-SESTRA DVOZAKON isti dan (Perdinec, ista starša!)",
          e4["date"] == e6["date"] == "6.2.1893"
          and "Perdinec" in e4["groom"]["name"] and "Perdinec" in e6["bride"]["name"]
          and "Georg Perdinec" in e4["parentsGroom"] and "Georg Perdinec" in e6["parentsBride"],
          f'{e4["groom"]["name"]} + {e6["bride"]["name"]}, {e4["date"]}')
    e5 = d["entries"][4]
    check("I3c v5 nevesta 17 (TIED rekord mladosti!) + »1« ulomek-anomala",
          e5["bride"]["age"] == 17 and "1 Griblers" in e5["bride"].get("stand", ""),
          f'{e5["bride"]["name"]} {e5["bride"]["age"]}; {e5["bride"].get("stand", "")}')
    e8 = d["entries"][7]
    check("I3d v8 RENOVACIJA ZAKONA 8.9.1898 (latinski blok + Jeglič + dispensacija 3. st.!)",
          "1898" in e8["urkunden"] and "dispensatione" in e8["urkunden"] and "Jeglič" in e8["urkunden"],
          e8["urkunden"][:70])
    e10 = d["entries"][9]
    check("I3e v10 = h26 NOVA HIŠA (nevesta Brinec 37) + 2. DUHOVNIK KLEMENČIČ + gjupnijski urad",
          e10["bride"]["houseNo"] == 26 and "Brinec" in e10["bride"]["name"]
          and "Klemenčič" in e10.get("priest", "") and "gjupnijskega" in e10["urkunden"],
          f'{e10["bride"]["name"]} h26; {e10.get("priest", "")}')
    e13 = d["entries"][12]
    check("I3f v13 ženin 58 = NAJSTAREJŠI 1893 + Gübler ü-forma",
          e13["groom"]["age"] == 58 and "Gübler" in e13["groom"].get("stand", ""),
          f'{e13["groom"]["name"]} {e13["groom"]["age"]}; {e13["groom"].get("stand", "")}')
    e15 = d["entries"][14]
    check("I3g v15 = h69 × h62 DRUBEL #1 + 1. dokument občine GRIBLJE (11/6. št: 1!)",
          e15["groom"]["houseNo"] == 69 and e15["bride"]["houseNo"] == 62
          and "Kure" in e15["bride"]["name"] and "GRIBLJE" in e15["urkunden"] and "št: 1" in e15["urkunden"],
          f'{e15["groom"]["name"]} h69 × {e15["bride"]["name"]} h62')
    e16 = d["entries"][15]
    check("I3h v16 = h58 × h74 DRUBEL #2 + DISPENS №1661 (3. st., oba materi BRINC!)",
          e16["groom"]["houseNo"] == 58 and e16["bride"]["houseNo"] == 74
          and "1661" in e16["urkunden"] and "Brinec" in e16["parentsBride"],
          f'{e16["groom"]["name"]} h58 × {e16["bride"]["name"]} h74; {e16["urkunden"][:40]}')
    e12 = d["entries"][11]
    check("I3i v12 VOJSKA Rudolfovo + proxy-zastopstvo (Marentič→Novacič)",
          "Rudolfovo" in json.dumps(e12, ensure_ascii=False)
          and "Novacič" in json.dumps(e12, ensure_ascii=False)
          and "Marentič" in json.dumps(e12, ensure_ascii=False),
          e12["urkunden"][:60])
    e17 = d["entries"][16]
    check("I3j v17 status-neznanka »Kronft« + rod. pf. Smihelj b. Rudolfswerth (~50 km)",
          "Kronft" in e17["groom"].get("stand", "") and "Rudolfswerth" in json.dumps(e17, ensure_ascii=False),
          f'{e17["groom"]["name"]}; {e17["groom"].get("stand", "")}')
    e19 = d["entries"][18]
    check("I3k v19 INHABER = NOV STATUS linije (Michael Murn)",
          "Inhaber" in e19["groom"].get("stand", ""), f'{e19["groom"]["name"]}; {e19["groom"].get("stand", "")}')
    feb6 = [e["row"] for e in d["entries"] if e["date"].startswith("6.2.")]
    jun12 = [e["row"] for e in d["entries"] if e["date"].startswith("12.6.")]
    apr30 = [e["row"] for e in d["entries"] if e["date"].startswith("30.4.")]
    check("I3l REKORD dneva 6.2. = [2,3,4,5,6,7,8] (7 porok!) + 12.6. = [14,15] + 30.4. = [10,11]",
          feb6 == [2, 3, 4, 5, 6, 7, 8] and jun12 == [14, 15] and apr30 == [10, 11], f'{feb6} + {jun12} + {apr30}')
    laipsl_rows = [e["row"] for e in d["entries"]
                   if "Laip" in json.dumps(e, ensure_ascii=False)]
    check("I3m Laipšl-mreža ×8 (v12 + v17 + v19 — 3. leto!)",
          len(laipsl_rows) >= 3
          and "Laipflers=tochft" in d["entries"][11]["bride"].get("stand", "")
          and "Laipflers=tochf" in d["entries"][16]["bride"].get("stand", "")
          and "Laipflerin" in d["entries"][18]["bride"].get("stand", ""),
          f'vrstice {laipsl_rows}')
    e20 = d["entries"][19]
    check("I3n v20 občina Tribuče NOVA + mladoletni ženin 23 (popravek 25→23!)",
          "tribuče" in e20["urkunden"].lower() and e20["groom"]["age"] == 23,   # case-insensitive (v JSON: TRIBUČE)
          f'{e20["groom"]["name"]} {e20["groom"]["age"]}; {e20["urkunden"][:50]}')

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
    check("I4 meseči (vsota 20; jan+feb 8 = 40 % zimska koncentracija!)",
          not bad_m and sum(mc.values()) == 20, str(bad_m or sum(mc.values())))
    aug29 = [e["row"] for e in d["entries"] if e["date"].startswith("29.8.")]
    check("I4b v19 = 29.8. (dispens PO poroki 13/9! — A7)", aug29 == [19], str(aug29))
    check("I4c v15 zglednica občine Griblje 11/6. št: 1 + v16 dispens 17.7.1893 №: 1661",
          "11/6. 1893" in e15["urkunden"] and ("17.7.1893" in e16["urkunden"] or "17/7" in e16["urkunden"]
          or "17.7." in e16["urkunden"] or "17. Juli 1893" in e16["urkunden"]),   # v16 JSON: »delto 17. Juli 1893 №: 1661«
          "v15/v16 urkunden")

    # ---------- I5: stats ključne številke ----------
    st = d["stats"]
    pr = st.get("priests", {})
    check("I5 duhovniki: Rauy ×18 + KLEMENČIČ ×2 (2. duhovnik linije — konec monopola!)",
          pr.get("Jos. Rauy") == 18 and pr.get("Michael Klemenčič (Coop.)") == 2 and len(pr) == 2, str(pr))
    check("I5b vitals=559 (554 + 5 P122)", st.get("vitals") == EXPECTED_VITALS, str(st.get("vitals")))
    check("I5c bloki 04455=42", st.get("blocks04455") == BLOCKS_04455, str(st.get("blocks04455")))
    check("I5d p80 hiše=44 (POPRAVEK: +h26/h58/h62 NOVE — h69/h74 že!)", st.get("p80Houses") == P80_HOUSES,
          str(st.get("p80Houses")))
    ag = st.get("ageGrooms", {})
    ab = st.get("ageBrides", {})
    check("I5e ženin max=58 (v13!) + min=22", ag.get("max") == 58 and ag.get("min") == 22, str(ag))
    check("I5f nevesta max=37 + min=17 (v5 TIED rekord!)", ab.get("max") == 37 and ab.get("min") == 17, str(ab))
    check("I5g mladoletne neveste=8 + ženini=4 (12/40, ABGB-24 7. leto!)",
          st.get("underageBrides") == 8 and st.get("underageGrooms") == 4,
          f'{st.get("underageBrides")}/{st.get("underageGrooms")}')
    check("I5h dispensacije=2 (v8 renovacija + v16 №1661)", st.get("dispensations") == 2,
          str(st.get("dispensations")))
    fd = st.get("foreignDocuments", {})
    check("I5i tuji dokumenti: Ordinariat ×1 + BezHauptm ×4 + Möttling ×3 + Rudolfovo ×1 + pf ×3",
          fd.get("Ordinariat-Laibach") == 1 and fd.get("BezHauptm-Črnomelj") == 4
          and fd.get("BezGer-Möttling") == 3 and fd.get("Rudolfovo-vojno-okrožje") == 1
          and fd.get("pf-StMichael") == 1 and fd.get("pf-Metlika") == 1 and fd.get("pf-Stopiče") == 1,
          str(fd))

    # ---------- I6: anomalije A1–A8 ----------
    ids = [a["id"] for a in d["anomalies"]]
    check("I6 anomalije A1–A8", ids == [f"A{i}" for i in range(1, 9)], str(ids))
    a1 = next((a for a in d["anomalies"] if a["id"] == "A1"), {})
    check("I6b A1 = BRAT-SESTRA-DVOZAKON (v4+v6 Perdinec)", a1.get("type") == "BRAT-SESTRA-DVOZAKON" and "v4" in a1.get("text", ""),
          a1.get("text", "")[:60])
    a2 = next((a for a in d["anomalies"] if a["id"] == "A2"), {})
    check("I6c A2 = RENOVACIJA-ZAKONA-1898 (v8, Jeglič)", a2.get("type") == "RENOVACIJA-ZAKONA-1898" and "1898" in a2.get("text", ""),
          a2.get("text", "")[:60])
    a4 = next((a for a in d["anomalies"] if a["id"] == "A4"), {})
    check("I6d A4 = STATUS-»1«-ULOMEK (v5)", a4.get("type") == "STATUS-»1«-ULOMEK" and "1" in a4.get("text", ""),
          a4.get("text", "")[:60])
    a8 = next((a for a in d["anomalies"] if a["id"] == "A8"), {})
    check("I6e A8 = MLADOLETEN-ŽENIN-POPPAVKA (v20 25→23)", a8.get("type") == "MLADOLETEN-ŽENIN-POPPAVKA" and "23" in a8.get("text", ""),
          a8.get("text", "")[:60])

    # ---------- I7: crossChecks ----------
    cc_ids = [c.get("id") for c in d["crossChecks"]]
    check("I7 crossChecks C1–C20", cc_ids == [f"C{i}" for i in range(1, 21)], str(cc_ids[-3:]))
    c1 = next((c for c in d["crossChecks"] if c.get("id") == "C1"), {})
    check("I7b C1 = DRUBEL-GRIBLJE ×2 + h26 = 3 poroke / 5 hiš", c1.get("type") == "DRUBEL-GRIBLJE" and "h69" in c1.get("text", ""),
          c1.get("text", "")[:60])
    c15 = next((c for c in d["crossChecks"] if c.get("id") == "C15"), {})
    check("I7c C15 6.2. ×7 = REKORD VSEH ČASOV", "×7" in c15.get("text", ""), c15.get("text", "")[:60])
    c12 = next((c for c in d["crossChecks"] if c.get("id") == "C12"), {})
    check("I7d C12 LAIPŠL ×8 (3. leto mreže)", "×8" in c12.get("text", ""), c12.get("text", "")[:60])
    c19 = next((c for c in d["crossChecks"] if c.get("id") == "C19"), {})
    check("I7e C19 DUHOVNIKI: Rauy ×18 + Klemenčič ×2", "×18" in c19.get("text", "") and "KLEMENČIČ" in c19.get("text", ""),
          c19.get("text", "")[:60])
    c13 = next((c for c in d["crossChecks"] if c.get("id") == "C13"), {})
    check("I7f C13 SKALA ×2 (priča 1893 IN renovacije 1898!)", "SKALA" in c13.get("type", ""), c13.get("text", "")[:60])
    # P121 dokaz ostaja nespremenjen (regresijska zaščita — lastna kumulativa)
    try:
        d121 = json.load(open(DOKAZ_P121))
        check("I7g P121 dokaz stats vitals=554 + bloki=37",
              d121["stats"].get("vitals") == 554 and d121["stats"].get("blocks04455") == 37,
              f'v{d121["stats"].get("vitals")} b{d121["stats"].get("blocks04455")}')
    except Exception as e:  # noqa: BLE001
        check("I7g P121 dokaz branje", False, str(e))

    # ---------- I8: parish.ts bloki 04455 ----------
    ts = open(PARISH_TS).read()
    blocks_m = re.findall(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*(\d{4}),\s*scan:\s*(\d+)', ts)
    check("I8 bloki 04455 = 94 (P121 +5, P122 +5, P123 +4 + P124 +3 + P125 +3 + P126 +9 + P127 +9 + P128 +6! + P129 +2 + P131 +4 + P132 +12!)", len(blocks_m) == BLOCKS_04455_TS, str(len(blocks_m)))
    h1893 = sorted((h for h, y, _ in blocks_m if y == "1893"), key=int)
    check("I8b hiše 1893 = [26,58,62,69,74]", ",".join(h1893) == GRIBLJE_HOUSES_TS, ",".join(h1893))
    h1892 = sorted((h for h, y, _ in blocks_m if y == "1892"), key=int)
    check("I8c hiše 1892 nespremenjene", ",".join(h1892) == "17,30,36,60", ",".join(h1892))
    h1891 = sorted((h for h, y, _ in blocks_m if y == "1891"), key=int)
    check("I8d hiše 1891 nespremenjene", ",".join(h1891) == "20,87", ",".join(h1891))
    h1890 = sorted((h for h, y, _ in blocks_m if y == "1890"), key=int)
    check("I8e hiše 1890 nespremenjene", ",".join(h1890) == "10,53,61,91", ",".join(h1890))
    h1889 = sorted((h for h, y, _ in blocks_m if y == "1889"), key=int)
    check("I8f hiše 1889 nespremenjene", ",".join(h1889) == "7,21,30,32,40,54,87", ",".join(h1889))
    h1888 = sorted((h for h, y, _ in blocks_m if y == "1888"), key=int)
    check("I8g hiše 1888 nespremenjene", ",".join(h1888) == "23,32,33,64", ",".join(h1888))
    h1887 = sorted((h for h, y, _ in blocks_m if y == "1887"), key=int)
    check("I8h hiše 1887 nespremenjene", ",".join(h1887) == "3,10,15,23,37,69,71", ",".join(h1887))
    h1886 = sorted((h for h, y, _ in blocks_m if y == "1886"), key=int)
    check("I8i hiše 1886 nespremenjene", ",".join(h1886) == "16,25,31,56,60,65,71", ",".join(h1886))
    # pini novih brani (1893 bloki)
    missing = []
    for hn, pin in BLOCK_PINS:
        found = False
        for m in re.finditer(r'\{\s*houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1893,\s*scan:\s*(\d+),\s*page:\s*(\d+),\s*whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S):
            if m.group(1) == hn and pin.lower() in m.group(4).lower():
                found = True
                break
        if not found:
            missing.append((hn, pin))
    check("I8j pini P122 (23)", not missing, str(missing) if missing else "vse ✓")
    # oznake dokazov 1893
    check("I8k h26 = NOVA HIŠA + KLEMENČIČ (2. duhovnik linije)",
          any(m.group(1) == "26" and "NOVA HIŠA" in m.group(2) and "KLEMENČIČ" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1893,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8l h69 = 2. poročni dokaz (po 1887!) + h62 + DRUBEL #1",
          any(m.group(1) == "69" and "2. poročni dokaz h69" in m.group(2) and "DRUBEL" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1893,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8m h58 = 1. POROČNI DOKAZ SPLOH! + h74 NOVA + DRUBEL #2 + dispens №1661",
          any(m.group(1) == "58" and "1. POROČNI DOKAZ h58" in m.group(2) and "h74" in m.group(2)
              and "DRUBEL" in m.group(2) and "1661" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1893,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))
    check("I8n h74 = NOVA hiša + krstna 1893+1911 (isto leto v obeh knjigah!)",
          any(m.group(1) == "74" and "NOVA hiša" in m.group(2) and "1893 + 1911" in m.group(2)
              for m in re.finditer(r'houseNo:\s*"([^"]*)",\s*bookSignature:\s*"04455",\s*year:\s*1893,[^}]*?whatSi:\s*"((?:[^"\\]|\\.)*)"', ts, re.S)))

    # ---------- I9: qa-parish ----------
    qa = open(QA_TS).read()
    check("I9 qa-p122", '"qa-p122-parish-marriage-1893"' in qa)
    check("I9b p80 bloki 78", "poročni vpisi (04455) ≠ 93" in qa)
    check("I9c p80 sidra 71 (1898×9 · 1899×6 · 1900×2!)", "poročna sidra ≠ 87" in qa)
    check("I9d p80 hiše 58 (qa kumulativa — …; P127: +6 NOVIH!)", "različnih hiš (vse tri knjige) ≠ 59" in qa)
    # vitals 559 regresijska zaščita v qa-p122
    check("I9e vitals 595 zaščita (P128)", "HOUSE_VITALS.length !== 611" in qa[qa.index("const p122Marr"):] if "const p122Marr" in qa else False)
    check("I9f stari 537/544/548/550/554/559 iztekla",
          "HOUSE_VITALS.length !== 537" not in qa and "HOUSE_VITALS.length !== 544" not in qa
          and "HOUSE_VITALS.length !== 548" not in qa and "HOUSE_VITALS.length !== 550" not in qa
          and "HOUSE_VITALS.length !== 554" not in qa and "HOUSE_VITALS.length !== 559" not in qa)

    # ---------- I10: README + notes ----------
    rd = open("README.md").read()
    check("I10 README po P122", "P122" in rd and ("124/124" in rd or "po P123" in rd))
    nt = open("research/issue17/parish-marriage-1893-notes.md").read()
    check("I10b notes faza 2 + DRUBEL", "FAZA 2" in nt and "DRUBEL-GRIBLJE" in nt.upper())

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
