#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P163 — MRLIŠKA knjiga 04894, leto 1897 = 12. polno leto mrliške linije
(s60-dno restart zap1–2 + s61–s65 == str. 59–64; 58 vrstic / 13 Griblje-vpisov /
10 hiš — h2 ×2 + h14 ×2 + h53 ×2 = 3 PONOVITVE!).
(issue #18).
★★★ URH-TRILOGIJA dokaz #3 (h51-Ana-Urh-roj.-Novosel-61 — P162-lead 100%!)
+ ★★★ PEZDIREC-×3-v-1897 (h42-Jurij + h87-Matija + h53-Barbara — KURRENT-z-
zanke @max-zoom ×3 — era 6. leto!) + ★★★ HLEBEC-h2-×2-DRAMA (mati-Ana-33-Maj +
sin-Peter-1-mes-Junij = 2 smrti v 6 TEDNEH!) + ★★★ h54 = 1. mrliški vpis
kadarkoli (19. PT-luknja-dokaz!) + meja 1897/98 = 5. STIL 5. POTRDITEV
(»1898.« DVOJNI podčrtaj s65 + Jan-INLINE + restart — P162-lead-'s67' OVRJEN!)
+ MAX-ZOOM > VLM 14. potrditev (10 popravkov!) + VLM-MISS-Griblje ×3 s63
(diag-agent-oči!) + 2× VLM-A2-vas-napaka ponovno (Giriče + Prilozje!)
+ r53-#11 (N.-Jakofčič) + NOVI DUHOVNIK #8-kandidat Maginarič[~].
Kumulativ: vitals 853 → 866, mrliški bloki 04894 154 → 167, p80 hiše 88
NESPREMENJENE (h54 že v vzorci prek 04105!), p80-skripta-houses 88 → 89
(+h54!), korpus 93 NESPREMENJEN. Vzorec p162."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1897.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1897-notes.md"

EXPECTED_ENTRIES = 13
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "2,14,15,16,26,42,51,53,54,87"
VITALS_TOTAL = 950               # 853 + 13!
BLOKI_04894 = 251                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 88                  # NESPREMENJENO (h54 že v vzorci prek 04105!)
P80_SCRIPT_HOUSES = 88           # NESPREMENJENO (h34/h52 IZVEN p80-filtra — P164!)
KORPUS_HOUSES = 93               # NESPREMENJENO (h54 že!)
NEW_SCANS = [61, 62, 63, 64, 65]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1897", d["status"])
    check("I1b 13 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1897 = 58 vrstic / 13 Griblje / 10 hiš",
          fr["vrstic"] == 58 and fr["griblje_vpisi"] == 13 and fr["hise"] == 10,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b 3 ponovitve (h2 ×2 + h14 ×2 + h53 ×2!)",
          "h2 ×2" in fr["ponovitve"] and "h14 ×2" in fr["ponovitve"]
          and "h53 ×2" in fr["ponovitve"], fr["ponovitve"])
    check("I2c hiše = 10 različnih (14,15,16,2,26,42,51,53,54,87)",
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 13 — 26.–32. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 61–65 (s61/s62/s63/s64/s65!)",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    e51 = next(e for e in ent if e["houseNo"] == "51")
    check("I5a h51-Ana-URH-roj.-NOVOSEL (URH-TRILOGIJA #3 — P162-lead 100%!)",
          "URH" in e51["ime"] and "NOVOSEL" in e51["rojena"] and "61" in e51["starost"], "")
    pez = [e for e in ent if "PEZDIR" in e["ime"]]
    check("I5b PEZDIREC-×3-v-1897 (h42-Jurij + h87-Matija + h53-Barbara!)",
          len(pez) == 3 and {e["houseNo"] for e in pez} == {"42", "87", "53"},
          str([(e["houseNo"], e["ime"][:30]) for e in pez]))
    h2 = [e for e in ent if e["houseNo"] == "2"]
    check("I5c HLEBEC-h2-×2 (Ana-33-Maj + Peter-1-mes-Junij — 2 smrti v 6 TEDNEH!)",
          len(h2) == 2 and all("HLEBEC" in e["ime"] for e in h2),
          str([(e["ime"][:20], e["mesec"]) for e in h2]))
    e54 = next(e for e in ent if e["houseNo"] == "54")
    check("I5d h54-ŠIMEC (1. mrliški vpis kadarkoli — 19. PT-luknja!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e54["opomba"] and "19. PT-luknja-dokaz" in e54["opomba"], "")
    h53 = [e for e in ent if e["houseNo"] == "53"]
    check("I5e h53-×2 (Ana-Brinec-gostarjeva-hči + Barbara-Pezdirec — 2 priimka 1 hiša!)",
          len(h53) == 2 and "BRINEC" in h53[0]["ime"] and "PEZDIREC" in h53[1]["ime"],
          str([e["ime"][:25] for e in h53]))

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 866", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 239 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1897 = [v for v in d04894 if v["year"] == 1897]
    check("I6c bloki 1897 = 13", len(d1897) == 13, str(len(d1897)))
    check("I6d bloki 1897: skeni 61–65 + stran == sken − 1",
          all(v["scan"] and 61 <= v["scan"] <= 65 and v["page"] == v["scan"] - 1 for v in d1897), "")
    check("I6d2 bloki 1905+ ne obstajajo (P168-lead!; P163-P167 = 1897–1901 sedaj v korpusu!)",
          all(v["year"] < 1905 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 950 + 91 + gap-18 (P170-kaskada!)",
          "len(vitals) == 950" in p80 and "len(houses) == 91" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — h54 že v vzorci!)", len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))
    p80s = {v["houseNo"] for v in d04894}
    check("I6h p80-skripta-houses 89 (88 + h54!)",
          "54" in p80s, f"h54 v 04894: {'54' in p80s}")

    # ---------- I7: max-zoom forenzika (14. potrditev — 10 popravkov) ----------
    check("I7a h51 'Mlh'→URH (VLM ZAVRJEN — U-r-h jasno!)",
          "VLM-'Mlh' ZAVRJEN" in e51["ime"], "")
    e2 = next(e for e in ent if e["houseNo"] == "2" and "Ana" in e["ime"])
    check("I7b h2 'Vrobeč'→HLEBEC + γ-3-'33' (obe cifri isti glyph!)",
          "VLM-'Vrobeč' ZAVRJEN" in e2["ime"] and "33" in e2["starost"] and "γ-3-REŠEN" in e2["starost"], "")
    e42 = next(e for e in ent if e["houseNo"] == "42")
    check("I7c h42-Jurij-PEZDIRC ('Perdivec'→z-zanke + lead-Jurij!)",
          "PEZDIRC" in e42["ime"] and "Jurij" in e42["ime"]
          and "POTRJEN: JURIJ" in e42["opomba"], "")
    e87 = next(e for e in ent if e["houseNo"] == "87")
    check("I7d h87-Matija-PEZDIREC ('Perdinec'→z-zanke + 'Marlo'→Matija!)",
          "PEZDIREC" in e87["ime"] and "Matija" in e87["ime"], "")
    e53b = next(e for e in ent if e["houseNo"] == "53" and "Barbara" in e["ime"])
    check("I7e h53-Barbara-PEZDIREC ('Padriec'→z-zanke + hišna-'83'→53!)",
          "PEZDIREC" in e53b["ime"] and "83'→53" in e53b["opomba"], "")
    e26 = next(e for e in ent if e["houseNo"] == "26")
    check("I7f h26-Janez-BRINEC pokop-17.-julij (γ-7-prečka > VLM-'14'!)",
          "17. julij" in e26["pokop"] and "VLM-'14' ZAVRJEN" in e26["pokop"], "")
    e16 = next(e for e in ent if e["houseNo"] == "2" and "Peter" in e["ime"])
    check("I7g h2-Peter pokop-9.-junij (VLM-'6' ZAVRJEN — zanka-zgoraj+descender!)",
          "9." in e16["pokop"] and "VLM-'6' ZAVRJEN" in e16["pokop"], "")
    e14j = next(e for e in ent if e["houseNo"] == "14" and "Janez" in e["ime"])
    check("I7h h14-Janez-BERTOPIO[?] ('Botek' ZAVRJEN — 8-glyph!)",
          "BERTOPIO" in e14j["ime"] and "VLM-'Botek' ZAVRJEN" in e14j["ime"], "")
    vlm_miss = [e for e in ent if "VLM-MISS-Griblje" in e["opomba"]]
    check("I7i VLM-MISS-Griblje ×3 (s63 — diag-agent-oči RAZKRILA!)",
          len(vlm_miss) == 3, str([e["houseNo"] for e in vlm_miss]))

    # ---------- I8: meje + lead ----------
    check("I8a meja 1896/97 = s60 (5. STIL 4. POTRDITEV — P162!)",
          "s60" in fr["meja_1896_97"] and "TROJNO podčrtana" in fr["meja_1896_97"], "")
    check("I8b meja 1897/98 = 5. STIL 5. POTRDITEV (»1898.« DVOJNI podčrtaj s65 + Jan-INLINE + restart!)",
          "s65" in fr["meja_1897_98"] and "DVOJNO podčrtana" in fr["meja_1897_98"]
          and "INLINE" in fr["meja_1897_98"], "")
    check("I8c P162-lead-'s67' OVRJEN (s66/s67/s68 = že 1898!)",
          "OVRJEN" in fr["meja_1897_98"], "")
    check("I8d P164-lead v dokazu (1898 + PEZDIREC-era-7.-leto!)",
          "P164" in d["nextSteps"][0] and "PEZDIREC" in d["nextSteps"][0], "")
    e8 = next(x for x in d["excluded"] if x["id"] == "E8")
    check("I8e E8-1898-Griblje-lead ×5 (h32 + h30 + h64 + h2 + h34!)",
          "Griblje-lead ×5" in e8["opis"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×9 + pika ×4",
          prev.count("1") == 9 and prev.count("pika") == 4, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Škurmelj ×5 + Rauq ×8",
          sum(1 for x in duh if "Škurmelj" in x) == 5 and sum(1 for x in duh if "Rauq" in x) == 8, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Feb1·Mar1·Maj1·Jun2·Jul2·Avg3·Sep1·Okt1·Nov1 · 2× MESEC-0 (Jan0 + Dec0!)",
          meseci.get("Feb") == 1 and meseci.get("Mar") == 1 and meseci.get("Maj") == 1
          and meseci.get("Jun") == 2 and meseci.get("Jul") == 2 and meseci.get("Avg") == 3
          and meseci.get("Sep") == 1 and meseci.get("Okt") == 1 and meseci.get("Nov") == 1
          and "Jan" not in meseci and "Dec" not in meseci, str(meseci))
    check("I9d razpon 1 mesec → 61 let (h2-Peter → h51-Ana!)",
          any("1 mesec" in e["starost"] for e in ent) and any("61 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if any(u in e["starost"] for u in ("mesecev", "mesec", "tednov"))
              or e["starost"].startswith("2 leta")]
    check("I9e otroška umrljivost 54 % (≤3 leta ×7/13: h2-Peter/h87/h53-Ana/h15/h16/h53-Barb/h14-Jožef!)",
          len(otroci) == 7, f"{len(otroci)}: {sorted(e['houseNo'] for e in otroci)}")

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p163 = 164. kontrola", "qa-p163-parish-death-1897" in qa, "")
    check("I10b qa-pini 950/251/91 (P170-kaskada!)",
          qa.count("!== 950") >= 60 and qa.count("!== 251") >= 12 and qa.count("p80Houses.size !== 91") >= 12,
          f"{qa.count('!== 950')}/{qa.count('!== 251')}/{qa.count('p80Houses.size !== 91')}")
    check("I10c qa guard 1901 (bloki 1901+ ne!)",
          "1905+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1905" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO — h54 že v doc-list!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi p153–p162 → 1898 (11× qa)",
          qa.count("1905+-mrliški bloki že v korpusu") >= 11, str(qa.count("1905+-mrliški bloki že v korpusu")))

    # ---------- I11: honesty + notes + README ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (PEZDIRC + PEZDIREC + HLEBEC + DRINEC + ŠTRUNCELJ + BERTOPIO[?])",
          "[~]" in d["honesty"][1] and "BERTOPIO" in d["honesty"][1], "")
    check("I11c SANACIJA-ne-potrebna (H3 — artefakti zdržali!)",
          "SANACIJA-ne-potrebna" in d["honesty"][2], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: 14. POTRDITEV (10 popravkov) + VLM-MISS ×3",
          "MAX-ZOOM > VLM — 14. POTRDITEV (10 popravkov)" in notes and "VLM-MISS ×3" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p163 skripte VITALS_TOTAL 873",
          all("VITALS_TOTAL = 950" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896))), "")
    check("I12b p80 PT_GAP_HOUSES vsebuje 54 (19. luknja-dokaz)",
          '"54"' in p80, "")
    check("I12c stale-guardi p153–p161 → 1898 (VSE skripte!)",
          all("1905+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894))), "")
    check("I12d P80_PT_GAP qa/skripta usklajena (doc-15 = skripta-18 [h54 ŽE v setu!] + h54 v obeh!)",
          '"54"' in qa and '"54"' in p80, "")

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
            inv = sorted(set(inv))
            ok7 = 0
            for s in NEW_SCANS:
                st2, data = http_get(inv[s - 1], timeout=60)
                if st2 == 200 and len(data) > 50000:
                    ok7 += 1
                time.sleep(1.0)
            check("I13b live skeni 61–65 (5× >50KB)", ok7 == 5, f"{ok7}/5")
        except Exception as e:
            check("I13 live knjiga 04894", False, str(e))

    ok = sum(1 for _, o, _ in results if o)
    print(f"\np163: {ok}/{len(results)}", "PASS" if ok == len(results) else "FAIL")
    for name, o, detail in results:
        mark = "✓" if o else "✗"
        print(f" {mark} {name}" + (f" — {detail}" if detail and not o else ""))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
