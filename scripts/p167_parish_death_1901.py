#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P167 — MRLIŠKA knjiga 04894, leto 1901 = 16. polno leto mrliške linije
(s80-dno re-potrditev meje 1900/01 + s81–s85 == str. 80–84; 55 vrstic /
10 Griblje-vpisov / 10 hiš — VSE RAZLIČNE! 3. leto brez hiša-×2!). (issue #18).
★★★ h28 = 1. MRLIŠKI VPIS KADARKOLI (25. PT-vezni dokaz IZVEN 41–60 —
cf. h11/h82-P165 + h81-P166!) + ★★★ h35 = 7. mrliški vpis = NOVI REKORD
linije (cf. h30-6!) + ★★★ KRIŽAN-×2-1901 (h36-Ana-76 + h35-Janez-63 = 2
hiši-2 spola-v-1-letu!) + ★★★ HLOBUČAR-×2-v-2-MESECIH-RAZREŠEN (Marija-h47-
DEC-1900 + Matija-h48-JAN-1901 = 17 DNI, sosednji hiši — P166-lead 100%!)
+ KUT'NEK-DOMINANTA-1901 (6× Jan–Mar!) + NOVI-DUHOVNIK-KANDIDAT #11 'Dostal'
[~] + meja 1901/02 = s85 ('1902.' VELIKA + DVOJNI podčrtaj = 5. STIL 9.
POTRDITEV — P166-lead POTRJEN!) + γ→7-lekcija 9.–10. potrditev (s81-'zap4'→7
+ s85-'zap65'→55!) + VLM-vas-0-napak (1. leto odkar P161!).
Kumulativ: vitals 894 → 904, mrliški bloki 04894 195 → 205, p80 hiše 89
NESPREMENJENE, korpus 93 NESPREMENJEN (h28 že v 04105!). Vzorec p166."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1901.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1901-notes.md"

EXPECTED_ENTRIES = 10
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "28,29,33,34,35,36,48,60,64,81"
VITALS_TOTAL = 921               # 894 + 10!
BLOKI_04894 = 222                # 195 + 10!
P80_HOUSES = 89                  # NESPREMENJENO (h28 že v 04105!)
KORPUS_HOUSES = 93               # NESPREMENJENO (h28 že v 04105!)
NEW_SCANS = [81, 82, 83, 84, 85]

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
    fr = d["frame"]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1901", d["status"])
    check("I1b 10 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1901 = 55 vrstic / 10 Griblje / 10 hiš (VSE RAZLIČNE!)",
          fr["vrstic"] == 55 and fr["griblje_vpisi"] == 10 and fr["hise"] == 10,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b ponovitve: BREZ hiša-×2 (3. leto! rast 13→7→8→13→8→10)",
          "BREZ hiša-×2" in fr["ponovitve"] and "13→7→8→13→8→10" in fr["rast"],
          fr["ponovitve"][:60])
    check("I2c hiše = 10 različnih (36,48,60,28,81,29,33,35,64,34)",
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 10 — 47.–52. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 80–85 (s80-reuse + s81–s85!)",
          all(e["scan"] in [80] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    e28 = next(e for e in ent if e["houseNo"] == "28")
    check("I5a h28-Marija-BRINEC (1. MRLIŠKI VPIS — 25. PT-vez! IZVEN 41–60!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e28["opomba"]
          and "25. PT-vezni dokaz" in e28["opomba"] and "IZVEN 41–60" in e28["opomba"], "")
    e35 = next(e for e in ent if e["houseNo"] == "35")
    check("I5b h35-Janez-KRIŽAN[~Kešran] (7. mrliški = NOVI REKORD!)",
          "7. mrliški vpis" in e35["opomba"] and "NOVI REKORD" in e35["opomba"]
          and "Kešran" in e35["ime"], "")
    e36 = next(e for e in ent if e["houseNo"] == "36")
    check("I5c h36-Ana-KRIŽAN (P167-lead-POTRJEN! KRIŽAN-×2-1901!)",
          "P167-lead-POTRJEN" in e36["ime"] and "KRIŽAN-×2-1901" in e36["opomba"], "")
    e48 = next(e for e in ent if e["houseNo"] == "48")
    check("I5d h48-Matija-HLOBUČAR (HLOBUČAR-×2-v-2-MESECIH-RAZREŠEN! P166-lead!)",
          "HLOBUČAR-×2-v-2-MESECIH-RAZREŠEN" in e48["opomba"] and "P166-lead" in e48["ime"], "")
    e81 = next(e for e in ent if e["houseNo"] == "81")
    check("I5e h81-Marija-Cindrič (2. leto ZAPORED — P166-nova!)",
          "2. mrliški vpis" in e81["opomba"] and "2. leto ZAPORED" in e81["opomba"], "")
    e29 = next(e for e in ent if e["houseNo"] == "29")
    check("I5f h29-Ana-MILEK (MILEK-leksikon — 4 hiše-10 vpisov!)",
          "MILEK-leksikon" in e29["ime"] and "MILEK-mreža" in e29["opomba"], "")
    e64 = next(e for e in ent if e["houseNo"] == "64")
    check("I5g h64-Janez-JAKOBČIČ (5. mrliški — hiša-×2-×2 + Voz-nesreča[~]!)",
          "5. mrliški vpis" in e64["opomba"] and "Voz" in e64["bolezen"], "")
    e34 = next(e for e in ent if e["houseNo"] == "34")
    check("I5h h34-Nikolaj-RAMPIČ[~Mramlič] (ZADNJA-1901 + meja-9.-POTRDITEV!)",
          "RAMPIČ" in e34["ime"] and "Mramlič" in e34["ime"] and "9. POTRDITEV" in e34["opomba"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 904", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 222", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1901 = [v for v in d04894 if v["year"] == 1901]
    check("I6c bloki 1901 = 10", len(d1901) == 10, str(len(d1901)))
    check("I6d bloki 1901: skeni 80–85 + stran == sken − 1",
          all(v["scan"] and 80 <= v["scan"] <= 85 and v["page"] == v["scan"] - 1 for v in d1901), "")
    check("I6d2 bloki 1903+ ne obstajajo (P169-lead!; P167-P168 = 1901+1902 sedaj v korpusu!)",
          all(v["year"] < 1903 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 921 + 90 + gap-18 (NESPREMENJENO!)",
          "len(vitals) == 921" in p80 and "len(houses) == 90" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — h28 že v 04105!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (18. potrditev — 3 konflikti [~]) ----------
    check("I7a zap50-IME-KONFLIKT 'Križan'vs'Kešran' → [~] (konzervativno!)",
          "Kešran" in e35["ime"] and "[~ Kešran" in e35["ime"], "")
    check("I7b zap55-IME-KONFLIKT 'Rampič'vs'Mramlič' → [~]",
          "RAMPIČ" in e34["ime"] and "Mramlič" in e34["ime"], "")
    check("I7c A2: VLM-vas-0-napak (1. leto odkar P161 — lekcija-'kompozit-vas'!)",
          any("VLM-vas-0-napak" in a["opis"] for a in d["anomalies"]), "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7d A3: KUT'NEK-DOMINANTA-1901 (6× Jan–Mar — cf. P166-Sep–Dec!)",
          "KUT'NEK-DOMINANTA-1901" in a3["opis"] and "6× Griblje" in a3["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7e A4: NOVI-DUHOVNIK-KANDIDAT #11 'Dostal' [~] (konflikt-ne-razrešen!)",
          "Dostal" in a4["opis"] and "#11" in a4["opis"], "")
    a8 = next(x for x in d["anomalies"] if x["id"] == "A8")
    check("I7f A8: γ→7-LEKCIJA 9.–10. potrditev (s81-'zap4'→7 + s85-'zap65'→55!)",
          "γ→7-LEKCIJA" in a8["opis"] and "s81" in a8["opis"] and "s85" in a8["opis"], "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1900/01 re-potrditev = s80 (5. STIL 8. POTRDITEV!)",
          "s80" in fr["meja_1900_01"] and "8. POTRDITEV" in fr["meja_1900_01"], "")
    check("I8b meja 1901/02 = s85 ('1902.' + DVOJNI podčrtaj = 9. POTRDITEV!)",
          "s85" in fr["meja_1901_02"] and "9. POTRDITEV" in fr["meja_1901_02"]
          and "DVOJNI podčrtaj" in fr["meja_1901_02"], "")
    check("I8c P168-lead v dokazu (1902 + s85-dno!)",
          "P168-lead" in d["nextSteps"] and "1902" in d["nextSteps"]["P168-lead"], "")
    e6 = next(x for x in d["excluded"] if x["id"] == "E6")
    check("I8d E6-1902-dno (zap1–10 + Pezdirec/Brinec?-zmeda!)",
          "zap1-Grem" in e6["opis2"] and "Pezdirec-56" in e6["opis2"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×10 (vs. 1900 = 1 ×8!)",
          prev.count("1") == 10, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Kut'nek ×6 + Rauq ×1 + Škurmelj ×2 + Dostal ×1 (Griblje-10!)",
          sum(1 for x in duh if "Kut'nek" in x) == 6
          and sum(1 for x in duh if "Rauq" in x) == 1
          and sum(1 for x in duh if "Škurmelj" in x) == 2
          and sum(1 for x in duh if x.startswith("Franc Dostal")) == 1, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Jan3·Feb1·Mar2·Apr1·Okt2·Dec1",
          meseci.get("Jan") == 3 and meseci.get("Feb") == 1 and meseci.get("Mar") == 2
          and meseci.get("Apr") == 1 and meseci.get("Okt") == 2 and meseci.get("Dec") == 1,
          str(meseci))
    check("I9d razpon 4 mesece → 76 let (h33 → h36!)",
          any("4 mesece" in e["starost"] for e in ent) and any("76 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if any(u in e["starost"] for u in ("mesecev", "mesec", "leta", " let"))
              and e["houseNo"] in ("60", "28", "81", "33")]
    check("I9e otroška smrt ×4 (h60-8-let + h28-4-let + h81-8-mes + h33-4-mes = 40%!)",
          len(otroci) == 4, str([e["houseNo"] for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p167 = 168. kontrola", "qa-p167-parish-death-1901" in qa, "")
    check("I10b qa-pini 921/222/90 (81×+15×+18×)",
          qa.count("!== 921") >= 80 and qa.count("!== 222") >= 15 and qa.count("p80Houses.size !== 90") >= 17,
          f"{qa.count('!== 921')}/{qa.count('!== 222')}/{qa.count('p80Houses.size !== 90')}")
    check("I10c qa guard 1903 (bloki 1903+ ne!)",
          "1903+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1903" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi p153–p166 → 1902 (13× qa)",
          qa.count("1903+-mrliški bloki že v korpusu") >= 13,
          f"{qa.count('1903+-mrliški bloki že v korpusu')}")

    # ---------- I11: honesty + notes ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (Križan-Kešran + Rampič-Mramlič + Dostal)",
          "[~]" in d["honesty"][1] and "Kešran" in d["honesty"][1]
          and "Mramlič" in d["honesty"][1], "")
    check("I11c rows-metoda-v3 (H3 — linije-v-projekciji-bug!)",
          "v3" in d["honesty"][2] and "linij" in d["honesty"][2], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: kompozit-forenzika + 18. okvir + P168-lead",
          "kompozit-forenzika" in notes and "P168-lead" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p166 skripte VITALS_TOTAL 904",
          all("VITALS_TOTAL = 921" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900))), "")
    check("I12b p80 PT_GAP_HOUSES komentar (P167: korpus-NESPREMENJEN!)",
          "+ 51 (mrliška 04894-1896" in p80, "")
    check("I12c stale-guardi p153–p166 → 1902 (VSE skripte!)",
          all("1903+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900))), "")
    check("I12d qa-parish.ts bloki 04894 = 222 (P167-kaskada!)",
          qa.count('04894").length !== 222') >= 15, str(qa.count('04894").length !== 222')))

    # ---------- I13 (--live): matricula dostopna ----------
    if live:
        try:
            st, body = http_get(BOOK_URL, timeout=30)
            urls = re.findall(r'"(/image/[A-Za-z0-9+/=%]+/)"', body.decode("utf-8", "replace"))
            check("I13 live knjiga 04894 (200 + inventar 256)",
                  st == 200 and len(urls) >= 256, f"{st}/{len(urls)}")
            import base64
            inv = []
            for m in re.finditer(r'"(/image/[A-Za-z0-9+/=%]+/)"', body.decode("utf-8", "replace")):
                s = m.group(1)[7:-1]
                try:
                    dd = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                    if dd.startswith("http"):
                        inv.append(dd)
                except Exception:
                    pass
            ok_scans = 0
            for sc in NEW_SCANS:
                try:
                    st2, data = http_get(inv[sc - 1], timeout=45)
                    if st2 == 200 and len(data) > 50000:
                        ok_scans += 1
                    time.sleep(1.0)
                except Exception:
                    pass
            check("I13b live citirani skeni 81–85 (5/5 JPEG 200)",
                  ok_scans == 5, f"{ok_scans}/5")
        except Exception as e:
            check("I13 live knjiga 04894", False, str(e))

    # ---------- izpis ----------
    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f" {'✓' if o else '✗'} {name}" + (f" [{det}]" if det and not o else ""))
    print(f"p167: {ok}/{len(results)} " + ("PASS" if ok == len(results) else "FAIL"))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
