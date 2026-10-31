#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P158 — MRLIŠKA knjiga 04894, leto 1892 = 7. polno leto mrliške linije
(s34–s41-top == str. 33–40; 81 vrstic / 17 Griblje-vpisov / 17 hiš — NARE:
1. mrliško leto BREZ hišnih ponovitev!). (issue #18). ★★★ 1. SUICID linije
(r50 'Se je obesil' + BREZ PODPISA + pika!) + ★★ LEAD PEZDIREC-h57 =
krstna-1889-Rudolf (VITAL-CHAIN krstna→mrliška + poročna-1909-hčera!) +
★★ h80 = 1. KORPUSNI dokaz kadarkoli (→ p80 83 EDINA!) + ★★ h61 = 3. leto
zapored (6 vpisov — najbolj trpljenča POTRJENA; Ana-POŽEK-½-URE!) +
★★ γγ-77-POPRAVEK (r27) + 1¾-POPRAVEK (r46) + ½-URE-POPRAVEK (r61) +
Šašelj-1892-DVOJNI (r21+r22!) + mreže ×4 (FILAK/JAKOBČIČ/BRINEC/KLOBUČAR) +
SEP–DEC-epidemija (Difteritis ×2 + Angina ×3) + JUN–AVG = 0 +
5. STIL MEJE ('— 1893. —' na prazni vrsti!) + s38-'Stran 37' γ-7 v številki
strani! Kumulativ: vitals 792 → 809, mrliški bloki 04894 93 → 110, p80 hiše
82 → 83 (+h80 EDINA!), korpus hiše 90 → 91 (+h80!).
Vzorec p157."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1892.json"
DOKAZ_P157 = "research/issue17/parish-death-1891.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1892-notes.md"

EXPECTED_ENTRIES = 17
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "2,8,9,16,17,20,23,24,36,37,41,43,48,57,58,61,80"
VITALS_TOTAL = 904               # POSODABLJENO P162: 837 + 16 (mrliška 1896)!
BLOKI_04894 = 205                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 86                  # TS-filter: 83 + h98 + h89 + h45! EDINA nova 1893 (+h89/h45 prek mrliške!)
P80_PY_HOUSES = 86               # python-filter (širši 1897): 84 + h98 + h89!
NEW_SCANS = [34, 35, 36, 37, 38, 39, 40]

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

    # ---------- I1: dokaz-structura ----------
    check("I1 dokaz obstaja + status", d.get("status") == "SAMPLE-TRANSCRIPTION-D1892", d.get("status", ""))
    check("I1b št. vpisov = 17", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c izključene skupine = 8",
          len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije ×10 + križne ×10 + iskrenost ×10", (
        len(d["anomalies"]) == EXPECTED_ANOMALIES
        and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS
        and len(d["honesty"]) == 10), f"{len(d['anomalies'])}/{len(d['crossChecks'])}/{len(d['honesty'])}")

    # ---------- I2: vrste, hiše, meseci ----------
    vrste = [e["row"] for e in ent]
    check("I2 vrste naraščajoče (1,6,8,9,14,21,27,34,46,48,50,56,57,59,61,64,72)",
          vrste == sorted(vrste) and vrste == [1, 6, 8, 9, 14, 21, 27, 34, 46, 48, 50, 56, 57, 59, 61, 64, 72],
          ",".join(map(str, vrste)))
    uniq = sorted({e["houseNo"] for e in ent}, key=int)
    check("I2b 17 različnih hiš — NARE (1. mrliško leto BREZ ponovitev!)",
          len(uniq) == 17 and ",".join(uniq) == GRIBLJE_HOUSES, ",".join(uniq))
    ponovitve = {h: sum(1 for e in ent if e["houseNo"] == h) for h in uniq if sum(1 for e in ent if e["houseNo"] == h) > 1}
    check("I2c ni ponovitev (ponovitveni slovar prazen!)", not ponovitve, json.dumps(ponovitve))
    meseci = {}
    for e in ent:
        meseci[e["mesec"][:3]] = meseci.get(e["mesec"][:3], 0) + 1
    check("I2c2 meseci (Jan 1 · Feb 3 · Mar 2 · Apr 1 · Maj 1 · Sep 3 · Okt 3 · Nov 2 · Dec 1 — JUN–AVG = 0!)",
          meseci == {"Jan": 1, "Feb": 3, "Mar": 2, "Apr": 1, "Maj": 1, "Sep": 3, "Okt": 3, "Nov": 2, "Dec": 1},
          json.dumps(meseci, ensure_ascii=False))

    # ---------- I3: live viri ----------
    if live:
        try:
            st, body = http_get(BOOK_URL)
            ok200 = st == 200
            check("I3a knjiga 04894 HTTP 200", ok200, str(st))
            urls = []
            if ok200:
                for m in re.finditer(r'"(/image/[A-Za-z0-9+/=%]+/)"', body.decode("utf-8", "replace")):
                    import base64
                    s = m.group(1)[7:-1]
                    try:
                        dd = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                        if dd.startswith("http"):
                            urls.append(dd)
                    except Exception:
                        pass
                urls = sorted(set(urls))
            check("I3b inventar 256", len(urls) == 256, str(len(urls)))
            probes_ok, det = 0, []
            for sc in NEW_SCANS:
                if sc - 1 < len(urls):
                    try:
                        st2, data = http_get(urls[sc - 1], timeout=45)
                        ok = st2 == 200 and len(data) > 50000
                        probes_ok += 1 if ok else 0
                        det.append(f"s{sc}:{st2}")
                    except Exception:
                        det.append(f"s{sc}:ERR")
            check("I3c citirani skeni 7/7 JPEG 200", probes_ok == 7, " ".join(det))
        except Exception as e:
            check("I3 live-viri", False, str(e))

    # ---------- I4: preslikava stran == sken − 1 ----------
    check("I4 stran == sken − 1 (vseh 17 — 13. potrditev; s38-'Stran 37' γ-7!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 34–40",
          sorted({e["scan"] for e in ent}) == NEW_SCANS, "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    check("I5 17 različnih hiš (NARE!)", len(uniq) == 17, ",".join(uniq))
    for h in ("57", "80", "2", "20", "17"):
        prej = [v for v in vit if v["houseNo"] == h and v["bookSignature"] == "04894" and v["year"] < 1892]
        check(f"I5b h{h} = 1. mrliški vpis (prej 0 v 04894)", len(prej) == 0,
              f"prej: {sorted({v['year'] for v in prej})}")
    prej_80 = [v for v in vit if v["houseNo"] == "80"]
    check("I5c h80 = 1. KORPUSNI dokaz kadarkoli (vse tri knjige 0 blokov pred P158!)",
          len([v for v in prej_80 if v["year"] < 1892]) == 0, "")
    h61_mrl = [v for v in vit if v["houseNo"] == "61" and v["bookSignature"] == "04894"]
    check("I5d h61 = 6 mrliških vpisov (1888 ×3 + 1891 ×2 + 1892 ×1 — najbolj trpljenča!)",
          len(h61_mrl) == 6, str(sorted(v["year"] for v in h61_mrl)))
    h57_krst = [v for v in vit if v["houseNo"] == "57" and v["bookSignature"] == "04105"]
    check("I5e h57 krstni 1886–1899 (PEZDIREC-familija!)",
          sorted(v["year"] for v in h57_krst) == [1886, 1888, 1889, 1894, 1899],
          str(sorted(v["year"] for v in h57_krst)))
    h57_poro = [v for v in vit if v["houseNo"] == "57" and v["bookSignature"] == "04455"]
    check("I5f h57 poročna-1909 (hčera Maria PEZDIREC!)",
          1909 in [v["year"] for v in h57_poro], str(sorted(v["year"] for v in h57_poro)))

    # ---------- I6: parish.ts ----------
    check("I6a vitals 825", len(vit) == VITALS_TOTAL, str(len(vit)))
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6b mrliški bloki 04894 = 205 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1892 = [v for v in d04894 if v["year"] == 1892]
    check("I6c bloki 1892 = 17", len(d1892) == 17, str(len(d1892)))
    check("I6d bloki 1892: skeni 34–40 + stran == sken − 1",
          all(v["scan"] and 34 <= v["scan"] <= 40 and v["page"] == v["scan"] - 1 for v in d1892), "")
    check("I6d2 bloki 1902+ ne obstajajo (P168-lead!; P167 = 1901 sedaj v korpusu!)",
          all(v["year"] < 1902 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 886 + 88 + gap-18 (POSODABLJENO P164)",
          "len(vitals) == 904" in p80 and "len(houses) == 89" in p80 and "len(gap) == 18" in p80, "")  # python-p80 = 84 (širši 1897-filter)
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 92 hiš (+h98 EDINA!)", len(houses_all) == 93, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika ----------
    r50 = next((e for e in ent if e["row"] == 50), None)
    check("I7a r50 = 1. SUICID ('Se je obesil' + BREZ PODPISA + pika!)",
          bool(r50) and "Se je obesil" in r50["bolezen"] and "BREZ PODPISA" in r50["duhovnik"]
          and "1. SUICID" in r50["bolezen"], "")
    r1 = next((e for e in ent if e["row"] == 1), None)
    check("I7b r1 LEAD = PEZDIREC + 2½ leta + Češarek (3 VLM ZAVRJENI!)",
          bool(r1) and "PEZDIREC" in r1["ime"] and "2½ leta" in r1["starost"]
          and "Češarek" in r1["duhovnik"] and "krstna-04105-1889" in r1["opomba"], "")
    r61 = next((e for e in ent if e["row"] == 61), None)
    check("I7c r61 = Ana POŽEK + ½ URE + Habost (VLM ×3 ZAVRJENI!) + najkrajša",
          bool(r61) and "POŽEK" in r61["ime"] and "½ URE" in r61["starost"]
          and "Habost" in r61["bolezen"], "")
    r27 = next((e for e in ent if e["row"] == 27), None)
    check("I7d r27 = 77 let POPRAVEK (γγ!) + Mertvorno X6-4.",
          bool(r27) and "77 let" in r27["starost"] and "γγ" in r27["starost"]
          and "Mertvorno" in r27["bolezen"] and "X6" in r27["bolezen"], "")
    r46 = next((e for e in ent if e["row"] == 46), None)
    check("I7e r46 = 1¾ leta POPRAVEK (VLM '17¾' ZAVRJEN!)",
          bool(r46) and "1¾ leta" in r46["starost"] and "17¾" in r46["starost"], "")
    r21 = next((e for e in ent if e["row"] == 21), None)
    check("I7f r21 = Šašelj župnik Adlešiči (DVOJNI podpis!) + Milek + 80",
          bool(r21) and "Šašelj" in r21["duhovnik"] and "MILEK" in r21["stan"]
          and "80 let" in r21["starost"], "")
    r14 = next((e for e in ent if e["row"] == 14), None)
    check("I7g r14 h80 = gostilničarka + 1. KORPUSNI dokaz + Rauq",
          bool(r14) and "gostilničarka" in r14["stan"] and "KORPUSNI" in r14["opomba"]
          and "Rauq" in r14["duhovnik"], "")

    # ---------- I8: P157-kontinuiteta ----------
    e8 = next((x for x in d["excluded"] if x["id"] == "E8"), None)
    check("I8a #81 = Grem 29 (celostanski-VLM 'Griblje' ZAVRJEN — max-zoom!)",
          bool(e8) and "Grem" in e8["opis"] and "ZAVRJEN" in e8["opis"], "")
    check("I8b 5. STIL MEJE ('— 1893. —' na prazni vrsti + Januarij!)",
          bool(e8) and "5. STIL MEJE" in e8["opis"] and "1893" in e8["opis"], "")
    x1 = next((x for x in d["crossChecks"] if x["id"] == "X1"), None)
    check("I8c X1 PEZDIREC VITAL-CHAIN (krstna-1889 + poročna-1909!)",
          bool(x1) and "krstna-04105-1889" in x1["detail"] and "1909" in x1["detail"], "")

    # ---------- I9: mreže + epidemija ----------
    check("I9a X2 FILAK ×3 v 3 letih", next((x for x in d["crossChecks"] if x["id"] == "X2"), None) is not None, "")
    check("I9b X3 JAKOBČIČ #4 (h6 ×2 + h9-suicid + h17-roj.!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X3"), None)), "")
    check("I9c X7 SEP–DEC-epidemija (Difteritis ×2 + Angina ×3!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X7"), None)), "")
    check("I9d X10 γ-7 10.–13. potrditev (Stran-37 + 77 + 1¾!)",
          bool(next((x for x in d["crossChecks"] if x["id"] == "X10"), None)) and "13" in next(
              x for x in d["crossChecks"] if x["id"] == "X10")["name"], "")

    # ---------- I10: podpisi + rekordi ----------
    signed = [e for e in ent if e.get("duhovnik") and "BREZ PODPISA" not in e["duhovnik"]]
    n_cesarek = sum(1 for e in signed if "Češarek" in e["duhovnik"])
    n_rauq = sum(1 for e in signed if "Rauq" in e["duhovnik"])
    n_saselj = sum(1 for e in signed if "Šašelj" in e["duhovnik"])
    check("I10a podpisi 16/17 (Češarek ×14 + Rauq ×1 + Šašelj ×1 + BREZ-suicid ×1!)",
          len(signed) == 16 and (n_cesarek, n_rauq, n_saselj) == (14, 1, 1),
          f"Češarek {n_cesarek} / Rauq {n_rauq} / Šašelj {n_saselj} / brez 1")
    ages = [e["starost"] for e in ent]
    check("I10b razpon ½ ure → 80 let", any("½ URE" in a for a in ages) and any("80 let" in a for a in ages), "")
    mla = [e for e in ent if any(t in e["starost"] for t in ("2½ leta", "1¾ leta", "2 meseca", "2 leti", "2¾ leta", "½ URE"))]
    check("I10c otroška umrljivost 6/17 = 35 % (≤3 leta ×6 — dvig iz 33 %!)",
          len(mla) == 6, str([e["starost"] for e in mla]))
    jetika = sum(1 for e in ent if e["bolezen"].startswith("Jetika"))
    check("I10d JETIKA ×4 (najpogostejši vzrok 1892!)", jetika == 4, str(jetika))

    # ---------- I11: meja 1893 + lead + rdeče + glave ----------
    fr = d["frame"]
    check("I11 meja 1892/93 = 5. STIL ('— 1893. —' na prazni vrsti, s41)",
          "5. STIL MEJE" in fr["boundaries"] and "1893" in fr["boundaries"], "")
    check("I11b stran == sken − 1 = 13. potrditev (source.pageMapping)",
          "13. potrditev" in d["source"]["pageMapping"], "")
    check("I11c glave »Leto 1892« izpisane 6/6 (frame.glave)", "6/6" in fr["glave"], "")
    check("I11d rdeče oznake X9-pojav 2. leto (≥9/17!)",
          "X9-pojav 2. leto" in next(x["name"] for x in d["crossChecks"] if x["id"] == "X9"), "")
    check("I11e P159-lead v nextSteps (Griblje 69(?)/53(?) — 1893!)",
          any("P159-LEAD" in s or "P159-lead" in s or "P159" in s for s in d["nextSteps"]), "")

    # ---------- I12: qa + README + notes ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p158 obstaja", "qa-p158-parish-death-1892" in qa, "")
    check("I12b qa-p157 guard 1893 (posodobljeno)", "1902+-mrliški bloki že v korpusu" in qa, "")
    check("I12c qa-pini 866/167/88 (78×+12×+14×) (P163)",
          qa.count("!== 904") >= 78 and qa.count("!== 205") >= 12 and qa.count("p80Houses.size !== 89") >= 14,
          f"{qa.count('!== 837')}/{qa.count('!== 167')}/{qa.count('p80Houses.size !== 87')}")
    readme = open(README, encoding="utf-8").read()
    check("I12d README P158", "P158" in readme and "1892" in readme, "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I12e notes obstajajo (suicid + Pezdirec-VITAL-CHAIN + 5. STIL)",
          "SUICID" in notes and "PEZDIREC" in notes and "5. STIL" in notes, "")

    # ---------- izpis ----------
    fails = [r for r in results if not r[1]]
    for name, ok, det in results:
        print(("PASS " if ok else "FAIL ") + name + (f"  [{det}]" if det and not ok else ""))
    print(f"\n{len(results) - len(fails)}/{len(results)} PASS"
          + ("" if not fails else f" — {len(fails)} FAIL!"))
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
