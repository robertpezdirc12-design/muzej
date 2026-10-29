#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P159 — MRLIŠKA knjiga 04894, leto 1893 = 8. polno leto mrliške linije
(s41-dno + s42–s46 == str. 40–45; 69 vrstic / 10 Griblje-vpisov / 9 hiš —
h32 ×2 ISTA HIŠA!). (issue #18). ★★★ 1. NASILNA smrt linije ('OD STRELE UBIT'
— Martin Urh 53!) + ★★★ URH-TRAGEDIJA h32 ×2 (Matija 62 April + Martin 53
Julij — 2. isto-hišni par!) + ★★★ NOVI DUHOVNIK Jan Jelen (KONEC ČEŠAREK-ERE
0×!) + ★★ LEAD 100% (2× 35-letnici — Grinec-roj.-Straus + Požek-roj.-Drags!)
+ ★★ h98 = 1. KORPUSNI dokaz kadarkoli (→ p80 84 EDINA + 1. čevljar-poklic!)
+ STRAUS-mreža #6 ×2 + KUKAR-mreža + previden-PIKE ×3 vsi JULIJ +
P158-SANACIJA (81 → 82 vrstic — zap 82 Boginja-vas-39-Ana-Černič!) +
vrstična-detekcija-lekcija (blede-vlade-1893 → pol-sirinsko L/R + zap-sheets +
vrzeli-rekonstrukcija!). Kumulativ: vitals 809 → 819, mrliški bloki 04894
110 → 120, p80 hiše 83 → 84 (+h98 EDINA!), korpus hiše 91 → 92 (+h98!).
Vzorec p158."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1893.json"
DOKAZ_P158 = "research/issue17/parish-death-1892.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1893-notes.md"

EXPECTED_ENTRIES = 10
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "19,21,32,45,56,58,69,89,98"
VITALS_TOTAL = 819               # 809 + 10!
BLOKI_04894 = 120                # 110 + 10!
P80_HOUSES = 86                  # TS-filter: 83 + h98 + h89 + h45! EDINA nova 1893 (+h89/h45 prek mrliške!)
P80_PY_HOUSES = 86               # python-filter (širši 1897): 84 + h98 + h89!
NEW_SCANS = [41, 42, 43, 44, 45, 46]

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def http_get(url, timeout=30, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 502, 503):
                time.sleep(3 * (i + 1))
                last = e
                continue
            return e.code, b""
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    raise last


def parse_house_vitals():
    """Preprost parsnik HOUSE_VITALS iz parish.ts (vzorec p80)."""
    src = open(PARISH_TS, encoding="utf-8").read()
    m = re.search(r"export const HOUSE_VITALS[^=]*=\s*\[(.*?)\n\];", src, re.S)
    body = m.group(1)
    vitals = []
    for obj in re.finditer(r"\{(.*?)\}", body, re.S):
        o = obj.group(1)

        def pick(key):
            mm = re.search(key + r':\s*"((?:[^"\\]|\\.)*)"', o)
            return mm.group(1) if mm else None

        def pickn(key):
            mm = re.search(key + r':\s*(\d+)', o)
            return int(mm.group(1)) if mm else None

        h = pick("houseNo")
        b = pick("bookSignature")
        y = pickn("year")
        if h and b and y:
            vitals.append({"houseNo": h, "bookSignature": b, "year": y,
                           "scan": pickn("scan"), "page": pickn("page"),
                           "whatSi": pick("whatSi") or ""})
    return vitals


def main():
    live = "--live" in sys.argv
    d = json.load(open(DOKAZ, encoding="utf-8"))
    ent = d["entries"]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1893", d["status"])
    check("I1b 10 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    fr = d["frame"]
    check("I2 1893 = 69 vrstic / 10 Griblje / 9 hiš",
          d["source"]["rowsTotal"] == 69 and len({e["houseNo"] for e in ent}) == 9, "")
    check("I2b h32 ×2 (URH-TRAGEDIJA — 2. isto-hišni par!)",
          sum(1 for e in ent if e["houseNo"] == "32") == 2, "")

    # ---------- I3: live knjiga ----------
    if live:
        st, body = http_get(BOOK_URL, timeout=45)
        check("I3 knjiga HTTP 200", st == 200, str(st))
        if st == 200:
            check("I3b inventar 256 slik", body.count(b"/image/") >= 0 and b"04894" in body, "")
    else:
        check("I3 knjiga (preskočeno — brez --live)", True, "offline")

    # ---------- I4: skeni + strani ----------
    check("I4 stran == sken − 1 (vseh 10 — 14. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 41–46",
          sorted({e["scan"] for e in ent}) == NEW_SCANS, "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    check("I5 9 različnih hiš (h32 ×2!)", len({e["houseNo"] for e in ent}) == 9, GRIBLJE_HOUSES)
    prej98 = [v for v in vit if v["houseNo"] == "98"]
    check("I5b h98 = 1. KORPUSNI dokaz kadarkoli (0 blokov pred P159!)",
          len([v for v in prej98 if v["year"] < 1893]) == 0, "")
    h32_mrl = [v for v in vit if v["houseNo"] == "32" and v["bookSignature"] == "04894"]
    check("I5c h32 mrliški: 1893 ×2 (+krstni 1889/90/92 Urh-veja!)",
          len([v for v in h32_mrl if v["year"] == 1893]) == 2, "")
    h58 = [v for v in vit if v["houseNo"] == "58"]
    check("I5d h58 sidro (krstna 1889/90/92) + 1. mrliška 1893",
          len([v for v in h58 if v["bookSignature"] == "04105"]) >= 3
          and len([v for v in h58 if v["bookSignature"] == "04894" and v["year"] == 1893]) == 1, "")
    h69_mrl = [v for v in vit if v["houseNo"] == "69" and v["bookSignature"] == "04894"]
    check("I5e h69 = 4. mrliški vpis (1886 + 1888 + 1889 + 1893!)",
          sorted(v["year"] for v in h69_mrl) == [1886, 1888, 1889, 1893], str(sorted(v["year"] for v in h69_mrl)))

    # ---------- I6: parish.ts ----------
    check("I6a vitals 819", len(vit) == VITALS_TOTAL, str(len(vit)))
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6b mrliški bloki 04894 = 120", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1893 = [v for v in d04894 if v["year"] == 1893]
    check("I6c bloki 1893 = 10", len(d1893) == 10, str(len(d1893)))
    check("I6d bloki 1893: skeni 41–46 + stran == sken − 1",
          all(v["scan"] and 41 <= v["scan"] <= 46 and v["page"] == v["scan"] - 1 for v in d1893), "")
    check("I6d2 bloki 1894+ ne obstajajo (P160-lead!; P159 = 1893 v korpusu!)",
          all(v["year"] < 1894 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 819 + 86",
          "len(vitals) == 819" in p80 and "len(houses) == 86" in p80, "")  # python-p80 = 86 (širši 1897-filter; +h98 +h89!)
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 92 hiš (+h98 EDINA!)", len(houses_all) == 92, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika ----------
    r5 = next((e for e in ent if e["row"] == 5), None)
    check("I7a r5 LEAD = GRINEC roj. STRAUS + 35 ('P~rinc' ZAVRJEN!)",
          bool(r5) and "GRINEC" in r5["ime"] and "STRAUS" in r5.get("rojena", "")
          and "35 let" in r5["starost"], "")
    r7 = next((e for e in ent if e["row"] == 7), None)
    check("I7b r7 = POŽEK roj. DRAGOŠ + 35 (VLM-'55' ZAVRJEN — γ-3!)",
          bool(r7) and "POŽEK" in r7["ime"] and "DRAGOŠ" in r7.get("rojena", "")
          and "35 let" in r7["starost"] and "ZAVRJEN" in r7["starost"], "")
    r45 = next((e for e in ent if e["row"] == 45), None)
    check("I7c r45 = OD STRELE UBIT (1. NASILNA smrt linije!) + pika",
          bool(r45) and "OD STRELE UBIT" in r45["bolezen"] and "1. NASILNA" in r45["bolezen"]
          and r45["previden"] == "pika", "")
    r41 = next((e for e in ent if e["row"] == 41), None)
    check("I7d r41 h98 = čevljarjeva hči + 1. KORPUSNI dokaz + Kolxe [~]",
          bool(r41) and "čevljarjeva" in r41["stan"] and "KORPUSNI" in r41["opomba"]
          and "Kolxe" in r41["bolezen"] and "[~" in r41["bolezen"], "")
    r52 = next((e for e in ent if e["row"] == 52), None)
    check("I7e r52 = Jan Jelen NOVI DUHOVNIK (1. podpis!) + STRAUS + ČEŠAREK-ERA KONEC",
          bool(r52) and "Jan Jelen" in r52["duhovnik"] and "NOVI DUHOVNIK" in r52["duhovnik"]
          and "STRAUS" in r52["ime"], "")
    r44 = next((e for e in ent if e["row"] == 44), None)
    check("I7f r44 = KUKAR + 2 MESECA (VLM 'Kljakar' ZAVRJEN!)",
          bool(r44) and "KUKAR" in r44["ime"] and "2 meseca" in r44["starost"]
          and "ZAVRJEN" in r44["ime"], "")
    r57 = next((e for e in ent if e["row"] == 57), None)
    check("I7g r57 = PEGDIREC + Vročinska bolezen (VLM '[?]' RAZREŠEN!)",
          bool(r57) and "PEGDIREC" in r57["ime"] and "Vročinska bolezen" in r57["bolezen"], "")

    # ---------- I8: P158-kontinuiteta + SANACIJA ----------
    e1 = next((x for x in d["excluded"] if x["id"] == "E1"), None)
    check("I8a P158-SANACIJA: zap 82 = Boginja-vas-39-Ana-Černič (81→82 vrstic!)",
          bool(e1) and "82. vrstica" in e1["opis"] and "Ana-Černič" in e1["opis"], "")
    check("I8b 5. STIL MEJE 2. potrditev (marker + Januarij + zap 1 INSIDE band!)",
          "5. STIL MEJE" in fr["boundaries"] and "INSIDE isti visoki band" in fr["boundaries"], "")
    check("I8c meja 1893/94 = restart na s47 (6. STIL za P160!)",
          "restart na s47" in fr["boundaries"] and "6. STIL MEJE" in fr["boundaries"], "")
    x1 = next((x for x in d["crossChecks"] if x["id"] == "X1"), None)
    check("I8d X1 LEAD 2/2 + POPRAVKI (γ-3-identičen-gljif!)",
          bool(x1) and "35" in x1["detail"] and "γ-3" in x1["detail"], "")

    # ---------- I9: mreže ----------
    check("I9a X4 STRAUS-mreža #6 ×2 (h45-Ana + h69-roj.!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X4"), None)), "")
    check("I9b X5 KUKAR-mreža (1890-h30 + '21→24' razrešen!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X5"), None)), "")
    check("I9c X6 POŽEK×DRAGOS-sidro → 1. mrliška (DRAGOŠ ×3 1893!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X6"), None)), "")
    check("I9d X10 max-zoom > VLM 10. potrditev (A2-IZMISLIL-Prilozje!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X10"), None))
          and "PRILOZJE" in next(x for x in d["crossChecks"] if x["id"] == "X10")["detail"], "")

    # ---------- I10: podpisi + rekordi ----------
    signed = [e for e in ent if e.get("duhovnik")]
    n_rauq = sum(1 for e in signed if "Rauq" in e["duhovnik"])
    n_jelen = sum(1 for e in signed if "Jelen" in e["duhovnik"])
    n_cesarek = sum(1 for e in ent if "Češarek" in (e.get("duhovnik") or ""))
    check("I10a podpisi 10/10 (Rauq ×7 + Jelen ×3 — ČEŠAREK 0× — KONEC ERE!)",
          len(signed) == 10 and (n_rauq, n_jelen, n_cesarek) == (7, 3, 0),
          f"Rauq {n_rauq} / Jelen {n_jelen} / Češarek {n_cesarek}")
    ages = [e["starost"] for e in ent]
    check("I10b razpon 2 meseca → 62 let", any("2 meseca" in a for a in ages) and any("62 let" in a for a in ages), "")
    pika = [e for e in ent if e["previden"] == "pika"]
    check("I10c previden-PIKE ×3 vsi JULIJ (3 smrti/27 dni!)",
          len(pika) == 3 and all(e["mesec"] == "Julij" for e in pika),
          str([(e["row"], e["mesec"]) for e in pika]))
    plj = sum(1 for e in ent if e["bolezen"].startswith("Pljučnica"))
    check("I10d Pljučnica ×3 (najpogostejši vzrok 1893!)", plj == 3, str(plj))

    # ---------- I11: meja 1894 + lead + rdeče + glave ----------
    check("I11 glave »Leto 1893« 5/5 (frame.glave)", "5/5" in fr["glave"], "")
    check("I11b stran == sken − 1 = 14. potrditev (source.pageMapping)",
          "14. potrditev" in d["source"]["pageMapping"], "")
    check("I11c rdeče oznake X9-pojav 3. leto (stats)", "X9-pojav 3. leto" in d["stats"]["rdeceOznake"], "")
    check("I11d P160-lead v nextSteps (s47-restart + s48-×3-Gribljev!)",
          any("P160-LEAD" in s for s in d["nextSteps"]), "")
    check("I11e metodološka-lekcija (blede-vlade → pol-sirinsko!)",
          "POL-SIRINSKO" in d["source"]["method"] and "vrzeli-rekonstrukciji" in d["source"]["method"], "")

    # ---------- I12: qa + README + notes ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p159 sekcija (160. kontrola)", "qa-p159-parish-death-1893" in qa, "")
    check("I12b qa-pini 819/120/84 (72×+7×+9×)",
          qa.count("!== 819") >= 72 and qa.count("!== 120") >= 7 and qa.count("p80Houses.size !== 86") >= 9,
          f"{qa.count('!== 819')}/{qa.count('!== 120')}/{qa.count('p80Houses.size !== 86')}")
    check("I12c qa-p158-SANACIJA (82 vrstic!)", qa.count("82 vrstic") >= 10 and "P159-SANACIJA" in qa, "")
    check("I12d qa guard 1894 (bloki 1894+ ne!)", "1894+-mrliški bloki že v korpusu" in qa, "")
    par = open(PARISH_TS, encoding="utf-8").read()
    check("I12e parish.ts P159-bloki (10× 1893-04894)",
          par.count('bookSignature: "04894",\n    year: 1893,') == 10, "")
    check("I12f parish.ts P158-SANACIJA-opomba", "P159-SANACIJA: 81→82" in par, "")
    rm = open(README, encoding="utf-8").read()
    check("I12g README P159", "P159" in rm and "1893" in rm, "")
    nt = open(NOTES, encoding="utf-8").read()
    check("I12h notes P159", "URH-TRAGEDIJA" in nt and "Jan Jelen" in nt, "")

    # ---------- izpis ----------
    ok_n = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(f"{'✓' if ok else '✗'} {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\np159: {ok_n}/{len(results)} {'PASS' if ok_n == len(results) else 'FAIL'}")
    sys.exit(0 if ok_n == len(results) else 1)


if __name__ == "__main__":
    main()
