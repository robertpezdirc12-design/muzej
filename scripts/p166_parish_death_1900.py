#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P166 — MRLIŠKA knjiga 04894, leto 1900 = 15. polno leto mrliške linije
(s75-dno re-potrditev meje 1899/1900 + s76–s80 == str. 75–79; 61 vrstic /
8 Griblje-vpisov / 8 hiš — VSE RAZLIČNE! 2. leto brez hiša-×2!). (issue #18).
★★★ h81 = 1. MRLIŠKI VPIS KADARKOLI (24. PT-vezni dokaz IZVEN 41–60 —
hišna-'81'-glif-dokaz: Kurrent-2 = odprta-zgornja-zanka, ta = zaprta → 8;
VLM-'21'-Papič ZAVRJENO!) + ★★★ NOVI DUHOVNIK #10: J.R. Kut'nek (1. podpis
s79-zap49 21. 9. 1900!; dominanta Sep–Dec 12×; Perz-era Jan–Avg 30× = 49%!)
+ ★★★ URH-h32-SAGA #2 (1893-Martin-OD-STRELE → 1900-Marija-vdova — VLM-
'Matija-Ulh' ZAVRJEN!) + ★★★ ŠTRAUS-h45-×3-v-7-letih (VLM-'Ulhar' + lead-
'Štavar' OBOJE ZAVRJENA!) + ★★★ HLOBUČAR-×2-v-2-mesecih (Marija-h47-Dec +
Matija-h48-Jan-1901 = P167-lead!) + ★★★ POROČNA-cross-h49 (DVA-dojenčka-
Marija-v-3-mesecih?! [~]) + MAX-ZOOM > VLM 17. potrditev = 10 popravkov
(5× A2-vas-napak = NOVI REKORD!) + meja 1900/01 = s80 (5. STIL 8. POTRDITEV
— P165-lead-'s79+?' OVRJEN!) + 3× pokop-'1901'-letnica (1. primer linije!).
Kumulativ: vitals 886 → 894, mrliški bloki 04894 187 → 195, p80 hiše 88 → 89
(+h81 EDINA NOVA — 1. mrliški-vpis!), korpus 93 NESPREMENJEN (h81 že v 04105!). Vzorec p165 (vključno stale-guardi!)."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1900.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1900-notes.md"

EXPECTED_ENTRIES = 8
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "23,32,45,47,49,63,65,81"
VITALS_TOTAL = 950               # 886 + 8!
BLOKI_04894 = 251                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 89                  # 88 + h81 EDINA NOVA (1. mrliški — 24. PT-vez; cf. P162-h51!)
KORPUS_HOUSES = 93               # NESPREMENJENO (h81 že v 04105!)
NEW_SCANS = [76, 77, 78, 79, 80]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1900", d["status"])
    check("I1b 8 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1900 = 61 vrstic / 8 Griblje / 8 hiš (VSE RAZLIČNE!)",
          fr["vrstic"] == 61 and fr["griblje_vpisi"] == 8 and fr["hise"] == 8,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b ponovitve: BREZ hiša-×2 (2. leto! rast 13→7→8)",
          "BREZ hiša-×2" in fr["ponovitve"] and "13→7→8" in fr["rast"],
          fr["ponovitve"][:60])
    check("I2c hiše = 8 različnih (23,32,45,47,49,63,65,81)",
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 8 — 41.–46. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 75–80 (s75/s76/s77/s78/s79/s80!)",
          all(e["scan"] in [75] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    e81 = next(e for e in ent if e["houseNo"] == "81")
    check("I5a h81-Barbara-Povšek (1. MRLIŠKI VPIS — 24. PT-vez! IZVEN 41–60!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e81["opomba"]
          and "24. PT-vezni dokaz" in e81["opomba"] and "IZVEN 41–60" in e81["opomba"], "")
    e32 = next(e for e in ent if e["houseNo"] == "32")
    check("I5b h32-Marija-URH (URH-h32-SAGA #2! VLM-'Matija' ZAVRJEN!)",
          "URH-h32-SAGA" in e32["opomba"] and "VLM-'Matija" in e32["ime"], "")
    e45 = next(e for e in ent if e["houseNo"] == "45")
    check("I5c h45-Marko-ŠTRAUS (STRAUS-MREŽA #9 — ×3-v-7-letih!)",
          "ŠTRAUS" in e45["ime"] and "STRAUS-MREŽA #9" in e45["opomba"]
          and "3 vpisi v 7 letih" in e45["opomba"], "")
    e47 = next(e for e in ent if e["houseNo"] == "47")
    check("I5d h47-Marija-HLOBUČAR (HLOBUČAR-×2-v-2-MESECIH! P167-lead!)",
          "HLOBUČAR-×2-v-2-MESECIH" in e47["opomba"] and "P167-lead" in e47["opomba"], "")
    e49 = next(e for e in ent if e["houseNo"] == "49")
    check("I5e h49-Marija-Brodarič (POROČNA-cross-04105-1899! DVA-dojenčka?!)",
          "POROČNA-cross-04105-1899" in e49["opomba"] and "DVA-dojenčka" in e49["opomba"], "")
    e23 = next(e for e in ent if e["houseNo"] == "23")
    check("I5f h23-Peter-BRINEC (BRINEC-mreža! h23 = 3. mrliški!)",
          "BRINEC-mreža" in e23["ime"] and "3. mrliški vpis" in e23["opomba"], "")
    e63 = next(e for e in ent if e["houseNo"] == "63")
    check("I5g h63-Jožef-KRIŽAN (KRIŽAN-mreža! h63 = 2. mrliški!)",
          "KRIŽAN" in e63["ime"] and "KRIŽAN-mreža" in e63["opomba"], "")
    e65 = next(e for e in ent if e["houseNo"] == "65")
    check("I5h h65-Marija-Mihelj (5. mrliški vpis — hiša-×2-v-2-letih!)",
          "5. mrliški vpis" in e65["opomba"] and "hiša-×2-v-2-LETIH" in e65["opomba"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 894", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 239 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1900 = [v for v in d04894 if v["year"] == 1900]
    check("I6c bloki 1900 = 8", len(d1900) == 8, str(len(d1900)))
    check("I6d bloki 1900: skeni 75–80 + stran == sken − 1",
          all(v["scan"] and 75 <= v["scan"] <= 80 and v["page"] == v["scan"] - 1 for v in d1900), "")
    check("I6d2 bloki 1905+ ne obstajajo (P169-lead!; P166-P168 = 1900+1901+1902 sedaj v korpusu!)",
          all(v["year"] < 1905 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 950 + 91 + gap-18 (P170-kaskada!)",
          "len(vitals) == 950" in p80 and "len(houses) == 91" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — h81 že v 04105!; p80-ločeno!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (17. potrditev — 10 popravkov) ----------
    check("I7a h81 hišna-'81'-glif-dokaz (Kurrent-2-odprta vs zaprta-zanka!)",
          "ODPRTA-zgornja-zanka" in e81["opomba"] and "ZAPRTA" in e81["opomba"]
          and "VLM-'21'" in e81["opomba"], "")
    check("I7b h32 'Matija-Ulh'→Marija-URH (VLM ZAVRJEN!)",
          "VLM-'Matija" in e32["ime"] and "ZAVRJEN" in e32["ime"], "")
    check("I7c h45 'Ulhar'/'Štavar'→ŠTRAUS (OBOJE ZAVRJENA!)",
          "VLM-'Ulhar'" in e45["ime"] and "Štavar" in e45["ime"], "")
    check("I7d h47 'Vilbucar'→HLOBUČAR (VLM ZAVRJEN!)",
          "VLM-'Vilbucar' ZAVRJEN" in e47["ime"], "")
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7e A1: 10 popravkov (17. potrditev MAX-ZOOM > VLM!)",
          "10 popravkov" in a1["opis"] and "ŠTRAUS" in a1["opis"] and "HLOBUČAR" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7f A2: 5× A2-vas-napak = REKORD (Giriče/Otok/Cerkviše/Krivoglave/Klošter!)",
          "Giriče" in a2["opis"] and "Otok" in a2["opis"] and "Cerkviše" in a2["opis"]
          and "Krivoglave" in a2["opis"] and "NOVI REKORD" in a2["opis"], "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7g A3: NOVI DUHOVNIK #10 Kut'nek (VLM-'Klevinek'+'Kuhinek' = ISTA-ROKA!)",
          "Kut'nek" in a3["opis"] and "Klevinek" in a3["opis"] and "Kuhinek" in a3["opis"], "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1899/1900 re-potrditev = s75 (5. STIL 7. POTRDITEV!)",
          "s75" in fr["meja_1899_1900"] and "VEČKRATNI podčrtaj" in fr["meja_1899_1900"]
          and "7. POTRDITEV" in fr["meja_1899_1900"], "")
    check("I8b meja 1900/01 = s80 ('1901' VELIKA + podčrtaj = 5. STIL 8. POTRDITEV!)",
          "s80" in fr["meja_1900_01"] and "8. POTRDITEV" in fr["meja_1900_01"]
          and "P165-lead-'s79+?' OVRJEN" in fr["meja_1900_01"], "")
    check("I8c P167-lead v dokazu (1901 + HLOBUČAR-×2!)",
          "P167-lead" in d["nextSteps"] and "HLOBUČAR" in d["nextSteps"]["P167-lead"], "")
    e8 = next(x for x in d["excluded"] if x["id"] == "E8")
    check("I8d E8-1900-rep (zap57–61 + '2 jan 1901'!)",
          "zap57" in e8["opis"] and "2 jan 1901" in e8["opis2"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×8 (vs. 1899 = 1 ×13!)",
          prev.count("1") == 8, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Perz ×4 + Rauq ×2 + Kut'nek ×2 (Griblje-8!)",
          sum(1 for x in duh if "Perz" in x) == 4
          and sum(1 for x in duh if "Rauq" in x) == 2
          and sum(1 for x in duh if "Kut'nek" in x) == 2, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Jan1·Feb3·Jun2·Sep1·Dec1 (MAJ-0!)",
          meseci.get("Jan") == 1 and meseci.get("Feb") == 3 and meseci.get("Jun") == 2
          and meseci.get("Sep") == 1 and meseci.get("Dec") == 1, str(meseci))
    check("I9d razpon 3 mesece → 75 let (h49 → h45!)",
          any("3 mesece" in e["starost"] for e in ent) and any("75 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if any(u in e["starost"] for u in ("mesecev", "mesec", "tednov", "leta"))
              and e["houseNo"] in ("49", "63", "65", "23")]
    check("I9e otroška smrt ×4 (h49-3-mes + h63-1½ + h65-7-ted + h23-3-let!)",
          len(otroci) == 4, str([e["houseNo"] for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p166 = 167. kontrola", "qa-p166-parish-death-1900" in qa, "")
    check("I10b qa-pini 894/195/88 (80×+15×+14×)",
          qa.count("!== 950") >= 80 and qa.count("!== 251") >= 15 and qa.count("p80Houses.size !== 91") >= 14,
          f"{qa.count('!== 950')}/{qa.count('!== 251')}/{qa.count('p80Houses.size !== 91')}")
    check("I10c qa guard 1903 (bloki 1903+ ne!)",
          "1905+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1905" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO — h49/h51!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi p153–p166 → 1901/1902 (13+1× qa)",
          qa.count("1905+-mrliški bloki že v korpusu") >= 13
          and qa.count("1905+-mrliški bloki že v korpusu") >= 1,
          f"{qa.count('1905+-mrliški bloki že v korpusu')}+{qa.count('1905+-mrliški bloki že v korpusu')}")

    # ---------- I11: honesty + notes + README ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (Štraus + Povšek + KRIŽAN + Kut'nek)",
          "[~]" in d["honesty"][1] and "Štraus" in d["honesty"][1], "")
    check("I11c rows-mapa-zamaknjena (H3 — s79-zap50-FIX!)",
          "zamaknjena" in d["honesty"][2], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: 17. POTRDITEV (10 popravkov) + 5× A2 = REKORD",
          "17. POTRDITEV MAX-ZOOM > VLM (10 popravkov" in notes and "REKORD" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p165 skripte VITALS_TOTAL 894",
          all("VITALS_TOTAL = 950" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899))), "")
    check("I12b p80 PT_GAP_HOUSES komentar (P166: korpus-NESPREMENJEN!)",
          "+ 51 (mrliška 04894-1896" in p80, "")
    check("I12c stale-guardi p153–p165 → 1901 (VSE skripte!)",
          all("1905+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (162, 1896), (163, 1897), (164, 1898), (165, 1899))), "")
    check("I12d qa-parish.ts bloki 04894 = 195 (P166-kaskada!)",
          qa.count('04894").length !== 251') >= 13, str(qa.count('04894").length !== 251')))

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
            check("I13b live citirani skeni 76–80 (5/5 JPEG 200)",
                  ok_scans == 5, f"{ok_scans}/5")
        except Exception as e:
            check("I13 live knjiga 04894", False, str(e))

    # ---------- izpis ----------
    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f" {'✓' if o else '✗'} {name}" + (f" [{det}]" if det and not o else ""))
    print(f"p166: {ok}/{len(results)} " + ("PASS" if ok == len(results) else "FAIL"))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
