#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P165 — MRLIŠKA knjiga 04894, leto 1899 = 14. polno leto mrliške linije
(s70-top re-potrditev meje 1898/99 + s70–s74 == str. 69–73; 61 vrstic /
13 Griblje-vpisov / 13 hiš — VSE RAZLIČNE! 1. leto brez hiša-×2 odkar 1889!).
(issue #18).
★★★ 2× 1. MRLIŠKI VPIS KADARKOLI (h11 = 22. PT-vez + h82 = 23.!) +
★★★ MILEK-×3-v-1899 (h22-78 + h65-3 + h82-5-mes; h22 = MILEK-×3-hiša!) +
★★★ meseci-KAOS-anomalija P164-lead RAZREŠENA (s72 = Junij/Julij/Avgust —
VLM-'Januarj/februarj/apr' = Kurrent-Jun/Jul-zmeda; kronologija 61/61!) +
★★★ NOVI DUHOVNIK #9: Jos. Perz coop. (12× s73–s74; P164-lead-'Franc-Števan'
NE POTRJEN — s72-'Jos. Vamp' = Jos. Rauq!) + ★★ suicid + SODNA PREISKAVA
(zap29-'se ustrelil'-'sodnijsko pregledan'-previden-PRAZEN!) + 2× mrtvorojen-
BREZ-podpisa (r53-#14+#15!) + X-vzrok 'Ustarélost [?]' ×2 + MAX-ZOOM > VLM
16. potrditev (12 popravkov!) + γ-lekcija 18.–19. (zap13-'91'→22 = ʒ vs
zap17-'91' = zaprta-zanka — ISTE VLM-branja, RAZLIČNI glyphi!) + meja 1899/1900
= s75 ('1900' VELIKA + VEČKRATNI podčrtaj + Januarj + restart = 5. STIL
7. POTRDITEV — P164-lead-'s75+?' POTRJEN!).
Kumulativ: vitals 873 → 886, mrliški bloki 04894 174 → 187, p80 hiše 88
NESPREMENJENE (vseh 13 št. že v korpusu!), korpus 93 NESPREMENJEN.
Vzorec p164 (vključno stale-guardi!)."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1899.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1899-notes.md"

EXPECTED_ENTRIES = 13
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "8,11,12,20,22,24,33,34,60,65,72,82,91"
VITALS_TOTAL = 904               # 873 + 13!
BLOKI_04894 = 205                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 88                  # NESPREMENJENO (vseh 13 št. že v korpusu!)
KORPUS_HOUSES = 93               # NESPREMENJENO
NEW_SCANS = [70, 71, 72, 73, 74]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1899", d["status"])
    check("I1b 13 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1899 = 61 vrstic / 13 Griblje / 13 hiš (VSE RAZLIČNE!)",
          fr["vrstic"] == 61 and fr["griblje_vpisi"] == 13 and fr["hise"] == 13,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b ponovitve: BREZ hiša-×2 + MILEK-×3 + PEZDIREC-×3",
          "BREZ hiša-×2" in fr["ponovitve"] and "MILEK-×3" in fr["ponovitve"]
          and "PEZDIREC-×3" in fr["ponovitve"], fr["ponovitve"][:80])
    check("I2c hiše = 13 različnih (8,11,12,20,22,24,33,34,60,65,72,82,91)",
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 13 — 35.–40. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 70–74 (s70/s71/s72/s73/s74!)",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    e22 = next(e for e in ent if e["houseNo"] == "22")
    check("I5a h22-Marija-MILEK (MILEK-×3-hiša! + '91'→22 + 'Mitek' ZAVRJEN!)",
          "MILEK" in e22["ime"] and "MILEK-×3-hiša" in e22["opomba"]
          and "'91'→22" in e22["opomba"], "")
    e82 = next(e for e in ent if e["houseNo"] == "82")
    check("I5b h82-Marija-Milek (1. MRLIŠKI VPIS — 23. PT-vez! + '32'→82!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e82["opomba"]
          and "23. PT-vezni dokaz" in e82["opomba"] and "'32'→82" in e82["opomba"], "")
    e11 = next(e for e in ent if e["houseNo"] == "11")
    check("I5c h11-Ana-Žumič (1. MRLIŠKI VPIS — 22. PT-vez! IZVEN 41–60!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e11["opomba"]
          and "22. PT-vezni dokaz" in e11["opomba"], "")
    e72 = next(e for e in ent if e["houseNo"] == "72")
    check("I5d h72-Barbara-Hravs ('32'→72 @max-zoom — γ-7!)",
          "'32'→72" in e72["opomba"], "")
    e91 = next(e for e in ent if e["houseNo"] == "91")
    check("I5e h91-Janez-Muc (hišna-'91' POTRJENA — zaprta-zanka-9!)",
          "PIKSELSKO POTRJENA" in e91["opomba"] and "Božjast" in e91["bolezen"], "")
    e34 = next(e for e in ent if e["houseNo"] == "34")
    check("I5f h34-Marija-Čilak (NOVI DUHOVNIK #9 Perz! + Ustarélost-X!)",
          "NOVI DUHOVNIK #9" in e34["duhovnik"] and "Ustarélost" in e34["bolezen"], "")
    e24 = next(e for e in ent if e["houseNo"] == "24")
    check("I5g h24-Matija-Štrinec (Prehlajenje-3.-pojav + KAOS-RAZREŠITEV-zap24!)",
          "Prehlajenje" in e24["bolezen"], "")
    milek = [e for e in ent if "Milek" in e["ime"] or "MILEK" in e["ime"]]
    check("I5h MILEK-×3-v-1899 (h22 + h65 + h82!)",
          len(milek) == 3 and {e["houseNo"] for e in milek} == {"22", "65", "82"},
          str([(e["houseNo"], e["ime"][:24]) for e in milek]))

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 894", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 205 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1899 = [v for v in d04894 if v["year"] == 1899]
    check("I6c bloki 1899 = 13", len(d1899) == 13, str(len(d1899)))
    check("I6d bloki 1899: skeni 70–74 + stran == sken − 1",
          all(v["scan"] and 70 <= v["scan"] <= 74 and v["page"] == v["scan"] - 1 for v in d1899), "")
    check("I6d2 bloki 1902+ ne obstajajo (P168-lead!; P165-P167 = 1899+1900+1901 sedaj v korpusu!)",
          all(v["year"] < 1902 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 886 + 88 + gap-18 (NESPREMENJENO!)",
          "len(vitals) == 904" in p80 and "len(houses) == 89" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — vseh 13 št. že v vzorci!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (16. potrditev — 12 popravkov) ----------
    check("I7a h22 hišna-'91'→22 (ʒ-forma — γ-lekcija 18.!)",
          "'91'→22" in e22["opomba"], "")
    check("I7b h82 hišna-'32'→82 (8 = DVOJNA-zanka!)",
          "'32'→82" in e82["opomba"], "")
    check("I7c h72 hišna-'32'→72 (γ-7 — 19. potrditev!)",
          "'32'→72" in e72["opomba"], "")
    check("I7d h82 mesec 'Januarj'→Junij (KAOS-RAZREŠITEV!)",
          "VLM-'Januarj' ZAVRJEN" in e82["mesec"], "")
    check("I7e h22 'Brehlajerje'→Prehlajenje + 'Hannig'→Škurmelj",
          "VLM-'Brehlajerje' ZAVRJEN" in e22["bolezen"]
          and "Hannig" in e22["duhovnik"] and "ZAVRJEN" in e22["duhovnik"], "")
    check("I7f h82 'Mulek'→Milek + h22 'Mitek'→MILEK",
          "VLM-'Mulek' ZAVRJEN" in e82["ime"] and "VLM-'Mitek'" in e22["ime"], "")
    check("I7g A3: meseci-KAOS RAZREŠEN (Junij/Julij/Avgust — kronologija 61/61!)",
          "KAOS" in next(x for x in d["anomalies"] if x["id"] == "A3")["opis"], "")
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7h A1: 12 popravkov (16. potrditev MAX-ZOOM > VLM!)",
          "12 popravkov" in a1["opis"] and "'32'→72" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7i A2: s73-zap40 'Griblje'→PRILOZJE (4. leto!)",
          "PRILOZJE" in a2["opis"], "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1899/1900 = s75 ('1900' VELIKA + VEČKRATNI podčrtaj = 5. STIL 7. POTRDITEV!)",
          "s75" in fr["meja_1899_1900"] and "VEČKRATNI podčrtaj" in fr["meja_1899_1900"]
          and "7. POTRDITEV" in fr["meja_1899_1900"], "")
    check("I8b P164-lead-'s75+?' POTRJEN (meja-1899/1900 v frame!)",
          "P164-lead" in fr["meja_1899_1900"], "")
    check("I8c P166-lead v dokazu (1900 + URH-h32-SAGA!)",
          "P166" in d["nextSteps"][0] and "URH" in d["nextSteps"][0], "")
    e8 = next(x for x in d["excluded"] if x["id"] == "E8")
    check("I8d E8-mrtvorojena ×2 (r53-#14+#15!)",
          "r53-vzorec #14+#15" in e8["opis"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×13 (vs. 1898 = 1 ×7!)",
          prev.count("1") == 13, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Škurmelj ×8 + Perz ×4 + Rauq ×1 (NOVI #9!)",
          sum(1 for x in duh if "Škurmelj" in x) == 8
          and sum(1 for x in duh if "Perz" in x) == 4
          and sum(1 for x in duh if "Rauq" in x) == 1, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Mar2·Apr2·Maj2·Jun1·Avg1·Okt3·Nov1·Dec1",
          meseci.get("Mar") == 2 and meseci.get("Apr") == 2 and meseci.get("Maj") == 2
          and meseci.get("Jun") == 1 and meseci.get("Avg") == 1 and meseci.get("Okt") == 3
          and meseci.get("Nov") == 1 and meseci.get("Dec") == 1, str(meseci))
    check("I9d razpon 5 mesecev → 78 let (h82 → h22!)",
          any("5 mesecev" in e["starost"] for e in ent) and any("78 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if any(u in e["starost"] for u in ("mesecev", "mesec", "leta"))
              and e["houseNo"] in ("82", "91", "65")]
    check("I9e otroška smrt ×3 (h82-5-mes + h91-3-let + h65-3-let!)",
          len(otroci) == 3, str([e["houseNo"] for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p165 = 166. kontrola", "qa-p165-parish-death-1899" in qa, "")
    check("I10b qa-pini 894/195/88 (78×+12×+14×)",
          qa.count("!== 904") >= 78 and qa.count("!== 205") >= 12 and qa.count("p80Houses.size !== 89") >= 14,
          f"{qa.count('!== 904')}/{qa.count('!== 205')}/{qa.count('p80Houses.size !== 89')}")
    check("I10c qa guard 1901 (bloki 1901+ ne!)",
          "1902+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1902" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO — h51 zadnji!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi p153–p165 → 1901 (12× qa)",
          qa.count("1902+-mrliški bloki že v korpusu") >= 11, str(qa.count("1902+-mrliški bloki že v korpusu")))

    # ---------- I11: honesty + notes + README ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (Muc + Jakobič + Štrinec + Hravs)",
          "[~]" in d["honesty"][1] and "Muc" in d["honesty"][1], "")
    check("I11c rows-mapa-zamaknjena (H3 — 3× re-kalibracija!)",
          "ZAMAKNJENA" in d["honesty"][2], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: 16. POTRDITEV (12 popravkov) + γ-lekcija 18.–19.",
          "MAX-ZOOM > VLM — 16. POTRDITEV (12 popravkov)" in notes and "18.–19. POTRDITEV" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p165 skripte VITALS_TOTAL 894",
          all("VITALS_TOTAL = 904" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898))), "")
    check("I12b p80 PT_GAP_HOUSES komentar (P165: korpus-NESPREMENJEN!)",
          "+ 51 (mrliška 04894-1896" in p80, "")
    check("I12c stale-guardi p153–p165 → 1901 (VSE skripte!)",
          all("1902+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (162, 1896), (163, 1897), (164, 1898))), "")
    check("I12d qa-parish.ts bloki 04894 = 187 (P165-kaskada!)",
          qa.count("04894\").length !== 205") >= 12, str(qa.count("04894\").length !== 205")))

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
            check("I13b live citirani skeni 70–74 (5/5 JPEG 200)",
                  ok_scans == 5, f"{ok_scans}/5")
        except Exception as e:
            check("I13 live knjiga 04894", False, str(e))

    # ---------- izpis ----------
    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f" {'✓' if o else '✗'} {name}" + (f" [{det}]" if det and not o else ""))
    print(f"p165: {ok}/{len(results)} " + ("PASS" if ok == len(results) else "FAIL"))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
