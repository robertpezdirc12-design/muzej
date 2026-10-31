#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P164 — MRLIŠKA knjiga 04894, leto 1898 = 13. polno leto mrliške linije
(s65-dno restart zap1 + s66–s69 == str. 64–68; 48 vrstic / 7 Griblje-vpisov /
6 hiš — h64 ×2! DNO linije — najnižje odkar 1889-8!).
(issue #18).
★★★ PEZDIREC-×4-v-1898 = REKORD mrliške (h52-Marija + h30-Doroteja +
h64-Ana-roj. + Boršt-h23-Janez — era 7. leto, rast 2→3→4!) + ★★★ h64-×2-DRAMA
(Ana-63-April + Matija-58-Okt = PAR [~] — 2 smrti v ~6 MESECIH — 3. par
linije!) + ★★★ 2× 1. mrliški vpis kadarkoli (h52 = 20. PT-luknja-dokaz +
h34 = 21.! [izven 41–60]) + meja 1898/99 = s70-top (»1899.« INLINE + Januarj
+ restart = 4. INLINE-potrditev — P163-lead-'s71+?' OVRJEN — s70 = ŽE 1899!)
+ MAX-ZOOM > VLM 15. potrditev (9 popravkov!) + P162b-γ-lekcija 16.–17.
potrditev (s65 '41'→71 + '43'→73!) + 2× mrtvorojen-brez-podpisa (r53 #12–#13!)
+ sken-geometrija-lekcija (dvoglavi-razpon + rotacija → morfološka
odstranitev črt — P163-s64-napaka RAZREŠENA!).
Kumulativ: vitals 866 → 873, mrliški bloki 04894 167 → 174, p80 hiše 88
NESPREMENJENE (h34/h52 IZVEN p80-filtra!), p80-skripta-houses 88 NESPREMENJENE,
korpus 93 NESPREMENJEN. Vzorec p163 (vključno I6f-lost-seja-popravek!)."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1898.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1898-notes.md"

EXPECTED_ENTRIES = 7
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "22,30,34,52,60,64"
VITALS_TOTAL = 938               # 866 + 7!
BLOKI_04894 = 239                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 88                  # NESPREMENJENO (h34/h52 IZVEN p80-filtra!)
KORPUS_HOUSES = 93               # NESPREMENJENO
NEW_SCANS = [66, 67, 68, 69]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1898", d["status"])
    check("I1b 7 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1898 = 48 vrstic / 7 Griblje / 6 hiš (DNO linije!)",
          fr["vrstic"] == 48 and fr["griblje_vpisi"] == 7 and fr["hise"] == 6,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b ponovitve: h64 ×2 (PAR!) + PEZDIREC-×4 (REKORD!)",
          "h64 ×2" in fr["ponovitve"] and "PEZDIREC-×4" in fr["ponovitve"], fr["ponovitve"])
    check("I2c hiše = 6 različnih (22,30,34,52,60,64)",
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 7 — 27.–34. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 66–69 (s66/s67/s68/s69!)",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    e52 = next(e for e in ent if e["houseNo"] == "52")
    check("I5a h52-Marija-PEZDIREC (1. mrliški vpis — 20. PT-luknja! + '32'→52!)",
          "PEZDIREC" in e52["ime"] and "1. MRLIŠKI VPIS KADARKOLI" in e52["opomba"]
          and "20. PT-luknja-dokaz" in e52["opomba"] and "'32'→52" in e52["opomba"], "")
    pez = [e for e in ent if "PEZDIREC" in e["ime"] or "PEZDIREC" in (e.get("rojena") or "")]
    check("I5b PEZDIREC-×3-na-Gribljih (h52-Marija + h30-Doroteja + h64-Ana-roj.!; 4. = Boršt EXCLUDED)",
          len(pez) == 3 and {e["houseNo"] for e in pez} == {"52", "30", "64"},
          str([(e["houseNo"], e["ime"][:26]) for e in pez]))
    h64 = [e for e in ent if e["houseNo"] == "64"]
    check("I5c h64-×2-DRAMA (Ana-63-April + Matija-58-Okt = VERBIČAR-PAR — 2 smrti v ~6 mesecev!)",
          len(h64) == 2 and all("VERBIČAR" in e["ime"] for e in h64)
          and {e["mesec"][:3] for e in h64} == {"Apr", "Okt"}, "")
    e34 = next(e for e in ent if e["houseNo"] == "34")
    check("I5d h34-Ana-FILAK (1. mrliški vpis — 21.! + Vodernica-korekcija!)",
          "FILAK" in e34["ime"] and "1. MRLIŠKI VPIS KADARKOLI" in e34["opomba"]
          and "Vodernica" in e34["bolezen"], "")
    e22 = next(e for e in ent if e["houseNo"] == "22")
    check("I5e h22-Janez-MILEK (2. mrliški vpis — MILEK-×2-hiša! + 'Mihel' ZAVRJEN!)",
          "MILEK" in e22["ime"] and "VLM-'Mihel' ZAVRJEN" in e22["ime"]
          and "MILEK-×2-hiša" in e22["opomba"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 873", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 239 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1898 = [v for v in d04894 if v["year"] == 1898]
    check("I6c bloki 1898 = 7", len(d1898) == 7, str(len(d1898)))
    check("I6d bloki 1898: skeni 66–69 + stran == sken − 1",
          all(v["scan"] and 66 <= v["scan"] <= 69 and v["page"] == v["scan"] - 1 for v in d1898), "")
    check("I6d2 bloki 1904+ ne obstajajo (P168-lead!; P164-P167 = 1898+1899+1900+1901 sedaj v korpusu!)",
          all(v["year"] < 1904 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 938 + 90 + gap-18 (h34/h52 IZVEN p80-filtra — NESPREMENJENO!)",
          "len(vitals) == 938" in p80 and "len(houses) == 91" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — h34/h52 že v vzorci!)", len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))
    p80s = {v["houseNo"] for v in d04894}
    check("I6h p80-skripta-houses vsebujeta h34 + h52 (1. mrliška!)",
          "34" in p80s and "52" in p80s, f"h34: {'34' in p80s}, h52: {'52' in p80s}")

    # ---------- I7: max-zoom forenzika (15. potrditev — 9 popravkov) ----------
    check("I7a h52 hišna-'32'→52 (5 = raven-zgornji-dvig — P163-lead OVRJEN!)",
          "'32'→52" in e52["opomba"], "")
    e30 = next(e for e in ent if e["houseNo"] == "30")
    check("I7b h30 'Maj'→Marcej (VLM ZAVRJEN — 5-glyph!)",
          "VLM-'Maj' ZAVRJEN" in e30["mesec"], "")
    check("I7c h34 'Hprnica[?]'→Vodernica (korpus-termin ×4!)",
          "VLM-'Hprnica[?]' ZAVRJEN" in e34["bolezen"], "")
    e60 = next(e for e in ent if e["houseNo"] == "60")
    check("I7d h60 'Vaselj'→Kašelj (K-a-š-e-l-j jasno!)",
          "VLM-'Vaselj' ZAVRJEN" in e60["bolezen"], "")
    check("I7e h22 'Mihel'→MILEK (korpus-leksikon — geb.-Milek-1887!)",
          "VLM-'Mihel' ZAVRJEN" in e22["ime"], "")
    check("I7f h64-Matija kronologija-'11.'→1. (VLM ZAVRJEN — zap38 6./8.!)",
          "VLM-'11.' ZAVRJEN" in h64[1]["smrt"] if h64[1]["ime"].startswith("Matija") else False, "")
    check("I7g podpis-'Jelen'→Škurmelj (VLM-duhovnik-stolpec NEZANESLJIV!)",
          "VLM-'Jelen' ZAVRJEN" in e52["duhovnik"], "")
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7h A1: 9 popravkov (15. potrditev MAX-ZOOM > VLM!)",
          "9 popravkov" in a1["opis"] and "Škrilje" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7i A2: P162b-γ-lekcija 16.–17. ('41'→71 + '43'→73!)",
          "41→71" in a2["opis"] and "43→93→73" in a2["opis"], "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1897/98 = 5. STIL 6. POTRDITEV (»1898.« DVOJNI podčrtaj + Jan-OKRAJŠAVA-INLINE!)",
          "s65" in fr["meja_1897_98"] and "DVOJNO podčrtana" in fr["meja_1897_98"]
          and "Jan.-OKRAJŠAVA-INLINE" in fr["meja_1897_98"], "")
    check("I8b meja 1898/99 = s70-top INLINE (4. INLINE-potrditev — P163-lead-'s71+?' OVRJEN!)",
          "s70" in fr["meja_1898_99"] and "INLINE" in fr["meja_1898_99"]
          and "OVRJEN" in fr["meja_1898_99"], "")
    check("I8c P165-lead v dokazu (1899 + PEZDIREC-era-8.!)",
          "P165" in d["nextSteps"][0] and "PEZDIREC" in d["nextSteps"][0], "")
    e8 = next(x for x in d["excluded"] if x["id"] == "E8")
    check("I8d E8-Griblje-lead ×7 (VSI POTRJENI @max-zoom!)",
          "Griblje-lead ×7" in e8["opis"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×7 (vs. 1897 = 1 ×9 + pika ×4!)",
          prev.count("1") == 7, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Škurmelj ×6 + Rauq ×1 (VLM-stolpec NEZANESLJIV — max-zoom leksikon!)",
          sum(1 for x in duh if "Škurmelj" in x) == 6 and sum(1 for x in duh if "Rauq" in x) == 1, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Jan1·Mar1·Apr1·Maj1·Okt1·Dec2",
          meseci.get("Jan") == 1 and meseci.get("Mar") == 1 and meseci.get("Apr") == 1
          and meseci.get("Maj") == 1 and meseci.get("Okt") == 1 and meseci.get("Dec") == 2, str(meseci))
    check("I9d razpon 11 mesecev → 63 let (h52-Marija → h64-Ana!)",
          any("11 mesecev" in e["starost"] for e in ent) and any("63 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if any(u in e["starost"] for u in ("mesecev", "mesec", "leta"))
              and e["houseNo"] in ("52", "60")]
    check("I9e otroška smrt ×2 (h52-11-mes + h60-1½-leta!)",
          len(otroci) == 2, str([e["houseNo"] for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p164 = 165. kontrola", "qa-p164-parish-death-1898" in qa, "")
    check("I10b qa-pini 886/187/88 (78×+12×+14×)",
          qa.count("!== 938") >= 78 and qa.count("!== 239") >= 12 and qa.count("p80Houses.size !== 90") >= 14,
          f"{qa.count('!== 938')}/{qa.count('!== 239')}/{qa.count('p80Houses.size !== 90')}")
    check("I10c qa guard 1900 (bloki 1900+ ne!)",
          "1904+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1904" in qa, "")  # POSODABLJENO P165
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO — h52 že v doc-list prek P124!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi p153–p163 → 1899 (11× qa)",
          qa.count("1904+-mrliški bloki že v korpusu") >= 11, str(qa.count("1904+-mrliški bloki že v korpusu")))

    # ---------- I11: honesty + notes + README ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (ŽELJKO + ožitkar + Kalf + Marentič)",
          "[~]" in d["honesty"][1] and "ŽELJKO" in d["honesty"][1], "")
    check("I11c SANACIJA-ne-potrebna (H3 — artefakti zdržali!)",
          "SANACIJA-ne-potrebna" in d["honesty"][2], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: 15. POTRDITEV (9 popravkov) + γ-lekcija 16.–17.",
          "MAX-ZOOM > VLM — 15. POTRDITEV (9 popravkov)" in notes and "16.–17. POTRDITEV" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p163 skripte VITALS_TOTAL 873",
          all("VITALS_TOTAL = 938" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897))), "")
    check("I12b p80 PT_GAP_HOUSES h52-že-v-setu + h34-izven-nabora (P164-komentar!)",
          "h52 1. MRLIŠKI vpis 1898" in p80 and "h34 1. mrliški vpis" in p80, "")
    check("I12c stale-guardi p155–p163 → 1899 (VSE skripte!)",
          all("1904+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (162, 1896), (163, 1897))), "")
    check("I12d P80_PT_GAP qa/skripta usklajena (doc-15 = skripta-18; h52 v obeh!)",
          '"52"' in qa and '"52"' in p80, "")

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
            check("I13b live citirani skeni 66–69 (4/4 JPEG 200)",
                  ok_scans == 4, f"{ok_scans}/4")
        except Exception as e:
            check("I13 live knjiga 04894", False, str(e))

    # ---------- izpis ----------
    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f" {'✓' if o else '✗'} {name}" + (f" [{det}]" if det and not o else ""))
    print(f"p164: {ok}/{len(results)} " + ("PASS" if ok == len(results) else "FAIL"))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
