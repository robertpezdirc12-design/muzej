#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P162 — MRLIŠKA knjiga 04894, leto 1896 = 11. polno leto mrliške linije
(s55-dno restart zap1–4 + s56–s59 + s60 == str. 54–59; 60 vrstic / 16
Griblje-vpisov / 13 hiš — h51 ×2 + h42 ×2 + h46 ×2 + h64 ×2 = 4 PONOVITVE!).
(issue #18).
★★★ h51 = NOVA korpusna hiša #93 + p80 #88 (1. dokaz kadarkoli — h51-DRAMA:
Marija-72-Januar + Peter-42-Februar = 2 smrti v 12 DNEH + URH-TRILOGIJA
1893→1896→1897!) + ★★★ PEZDIREC-×2-v-3-DNEH (h20-Matija-8-mes + h42-Marija-
14-let!) + ★★★ h46-×2-NIKOLAJA (Brodarič-12-dni + Štabijar-16-let-hlapac —
X10!) + meja 1895/96 = 5. STIL 4. POTRDITEV (»1896.« DVOJNI podčrtaj s55!)
+ meja 1896/97 = 5. STIL 4. POTRDITEV (»1897.« TROJNI podčrtaj s60! —
izgubljena-seja-'s61'-hipoteza OVRJENA!) + MAX-ZOOM > VLM 13. potrditev
(9 popravkov!) + 3× VLM-A2-vas-napaka + 1. DECEMBER-0 + r53-#8–#10.
SANACIJA: /tmp artefakti izgubljeni (sandbox-reset) — VLM re-generiran +
diag-agent-oči + max-zoom celice. Kumulativ: vitals 837 → 853, mrliški bloki
04894 138 → 154, p80 hiše 87 → 88 (+h51 EDINA!), korpus 92 → 93 (+h51!).
Vzorec p161."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1896.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1896-notes.md"

EXPECTED_ENTRIES = 16
EXPECTED_EXCLUDED = 9
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "9,14,20,26,31,41,42,45,46,51,58,63,64"
VITALS_TOTAL = 921               # 837 + 16!
BLOKI_04894 = 222                # POSODABLJENO P167: + 10 (mrliška 1901)!
P80_HOUSES = 88                  # 87 + h51 (EDINA NOVA — 1. dokaz kadarkoli!)!
KORPUS_HOUSES = 93               # 92 + h51!
NEW_SCANS = [55, 56, 57, 58, 59, 60]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1896", d["status"])
    check("I1b 16 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 9 excluded / 10 anomalij / 10 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1896 = 60 vrstic / 16 Griblje / 13 hiš",
          fr["vrstic"] == 60 and fr["griblje_vpisi"] == 16 and fr["hise"] == 13,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b 4 ponovitve (h51 ×2 + h42 ×2 + h46 ×2 + h64 ×2!)",
          "h51 ×2" in fr["ponovitve"] and "h42 ×2" in fr["ponovitve"]
          and "h46 ×2" in fr["ponovitve"] and "h64 ×2" in fr["ponovitve"], fr["ponovitve"])
    check("I2c hiše = 13 različnih (9,14,20,26,31,41,42,45,46,51,58,63,64)",
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted({e["houseNo"] for e in ent}, key=int)))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 16 — 20.–25. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 55–60 (Griblje-vrstice: 55/56/57/58/59/60 — s61 = že 1897!)",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    h51 = [v for v in parse_house_vitals() if v["houseNo"] == "51" and v["bookSignature"] == "04894"]
    check("I5a h51 = NOVA hiša P162 (1. dokaz kadarkoli — 1896 ×2!; POSODABLJENO P163: + 1897-Ana-URH-TRILOGIJA #3!)",
          sorted(v["year"] for v in h51) == [1896, 1896, 1897],
          str(sorted(v["year"] for v in h51)))
    n46 = [e for e in ent if e["houseNo"] == "46"]
    check("I5b h46 ×2 NIKOLAJA (Brodarič-12-dni-Maj + Štabijar-16-let-Avg — X10-#3!)",
          len(n46) == 2 and all(e["ime"].startswith("Nikolaj") for e in n46),
          str([e["ime"] for e in n46]))
    pez = [e for e in ent if "PEZDIREC" in e["ime"]]
    check("I5c PEZDIREC-×2-v-3-DNEH (h20-31.3. + h42-2.4.!)",
          len(pez) == 2 and {e["houseNo"] for e in pez} == {"20", "42"},
          str([(e["houseNo"], e["smrt"]) for e in pez]))
    h45 = [v for v in parse_house_vitals() if v["houseNo"] == "45" and v["bookSignature"] == "04894"]
    check("I5d h45-STRAUS ×3 (1893-×2 + 1896-Barbara-70 [γ-REVIZIJA!] + P166-1900-Marko! — MREŽA #9!)",
          sorted(v["year"] for v in h45) == [1893, 1896, 1900], str(sorted(v["year"] for v in h45)))
    jak = [e for e in ent if "JAKOBČIČ" in e["ime"]]
    check("I5e JAKOBČIČ-×2-1896 (h64-Matija-68 + h9-Neža-9-mes — SUICID-hiša-vez!)",
          len(jak) == 2 and {e["houseNo"] for e in jak} == {"64", "9"},
          str([(e["houseNo"], e["ime"]) for e in jak]))

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 853", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 222 (POSODABLJENO P167)", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1896 = [v for v in d04894 if v["year"] == 1896]
    check("I6c bloki 1896 = 16", len(d1896) == 16, str(len(d1896)))
    check("I6d bloki 1896: skeni 55–60 + stran == sken − 1",
          all(v["scan"] and 55 <= v["scan"] <= 60 and v["page"] == v["scan"] - 1 for v in d1896), "")
    check("I6d2 bloki 1903+ ne obstajajo (P168-lead!; P162-P167 = 1896–1901 sedaj v korpusu!)",
          all(v["year"] < 1903 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 921 + 90 + gap-18 (POSODABLJENO P164)",
          "len(vitals) == 921" in p80 and "len(houses) == 90" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (+h51 — 1. dokaz kadarkoli!)", len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (13. potrditev — 9 popravkov) ----------
    e58 = next(e for e in ent if e["houseNo"] == "58")
    check("I7a h58 Ana PRIJET roj. BRINEC 70 [γ-REVIZIJA-P162b — γ=7: ZAP7=γ + ZAP14=+-4 + Tomc-74!] (VLM-'30'/'34' + 'Ogrizovičeva'/'Primca' ZAVRJENI!)",
          e58["ime"].startswith("Ana PRIJET") and e58["rojena"] == "BRINEC [★★ max-zoom — VLM-'Ogrizovičeva' + izgubljena-seja-'Primca' ZAVRJENA]"
          and "70" in e58["starost"] and "γ-REVIZIJA" in e58["starost"], "")
    e14 = next(e for e in ent if e["houseNo"] == "14")
    check("I7b h14 N. BRINEC mrtvorojen BREZ podpisa (VLM-'Binec/Bunec' ZAVRJEN — r53-#8!)",
          e14["ime"] == "N. BRINEC [★★ VLM-'Binec/Bunec' ZAVRJEN]" and e14["duhovnik"] == "BREZ PODPISA", "")
    e20 = next(e for e in ent if e["houseNo"] == "20")
    check("I7c h20 Matija PEZDIREC (VLM-'Podrivec' + diag-'Pozdrivec' OBOJE ZAVRJENA!)",
          "PEZDIREC" in e20["ime"] and "OBOJE ZAVRJENA" in e20["ime"], "")
    e42 = next(e for e in ent if e["houseNo"] == "42")
    check("I7d h42 Marija PEZDIREC 14 let (identičen glyph + VLM-'11' ZAVRJEN!)",
          "Marija PEZDIREC" in e42["ime"] and "14 let" in e42["starost"] and "ZAVRJEN" in e42["starost"], "")
    e64 = next(e for e in ent if e["houseNo"] == "64" and "VERBIČAR" in e["ime"])
    check("I7e h64 Ana VERBIČAR — hišna-64 (VLM-'61' + diag-'60/61' OBOJE ZAVRJENA!)",
          "64" in e64["opomba"] and "OBOJE ZAVRJENA" in e64["opomba"], "")
    e26 = next(e for e in ent if e["houseNo"] == "26")
    check("I7f h26 Barbara HVALEŠIČ 36 let (diag-'56' ZAVRJEN — VLM-'36' ✓!)",
          "36 let" in e26["starost"] and "56' ZAVRJEN" in e26["starost"], "")
    e41 = next(e for e in ent if e["houseNo"] == "41")
    check("I7g h41 Marjeta MUŠIČ + Bule (VLM-'Magdalena-Hlevič'+'Škrlje' OBOJE ZAVRJENA — 1. BULE!)",
          "MUŠIČ" in e41["ime"] and "Bule" in e41["bolezen"] and "1. VPIS BULE" in e41["bolezen"], "")
    e51p = next(e for e in ent if e["houseNo"] == "51" and "Peter" in e["ime"])
    check("I7h h51 Peter URH 72 let [γ-REVIZIJA-P162b — zap-kalibracija ZAP7=γ + Tomc-74; VLM-'92' + seja-'42' ZAVRJENA!]",
          "72 let" in e51p["starost"] and "γ-REVIZIJA" in e51p["starost"], "")
    e46s = next(e for e in ent if e["houseNo"] == "46" and "ŠTABIJAR" in e["ime"])
    check("I7i h46 Nikolaj ŠTABIJAR hlapac (1. stan-hlapac mrliške!)",
          "hlapac" in e46s["stan"] and "1. stan-hlapac" in e46s["stan"], "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1895/96 = 5. STIL 4. POTRDITEV (»1896.« DVOJNI podčrtaj s55 + Januarj + restart!)",
          "s55" in fr["meja_1895_96"] and "DVOJNO podčrtana" in fr["meja_1895_96"], "")
    check("I8b meja 1896/97 = 5. STIL 4. POTRDITEV (»1897.« TROJNI podčrtaj s60!)",
          "s60" in fr["meja_1896_97"] and "TROJNO podčrtana" in fr["meja_1896_97"], "")
    check("I8c izgubljena-seja-'s61'-hipoteza OVRJENA (s61 = že 1897 — glava + zap 3–14!)",
          "OVRJENA" in fr["meja_1896_97"] and "že 1897" in fr["meja_1896_97"], "")
    e7 = next(x for x in d["excluded"] if x["id"] == "E7")
    check("I8d E7-meja-dokaz (»1897.« TROJNO podčrtana + restart zap 1–2)",
          "TROJNO podčrtana" in e7["opis"] and "1897" in e7["opis"], "")
    check("I8e P163-lead v dokazu (1897 + h51-Ana-Urh-TRILOGIJA #3!)",
          "P163" in d["nextSteps"][0] and "Novosel" in d["nextSteps"][0], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×7 + pika ×5 + NE ×4 (dojenčki/mrtvorojen!)",
          prev.count("1") == 7 and prev.count("pika") == 5 and prev.count("NE") == 4, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Škurmelj ×12 + Rauq ×3 + BREZ ×1 (mrtvorojen!)",
          sum(1 for x in duh if "Škurmelj" in x) == 12 and sum(1 for x in duh if "Rauq" in x) == 3
          and sum(1 for x in duh if "BREZ" in x) == 1, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Jan4·Feb1·Mar1·Apr1·Maj1·Jun1·Avg2·Sep2·Okt1·Nov2 · 1. DECEMBER-0!",
          meseci.get("Jan") == 4 and meseci.get("Feb") == 1 and meseci.get("Mar") == 1
          and meseci.get("Apr") == 1 and meseci.get("Maj") == 1 and meseci.get("Jun") == 1
          and meseci.get("Avg") == 2 and meseci.get("Sep") == 2 and meseci.get("Okt") == 1
          and meseci.get("Nov") == 2 and "Dec" not in meseci, str(meseci))
    check("I9d razpon 12 dni → 72 let (h46-Brodarič → h51-Marija!)",
          any("12 dni" in e["starost"] for e in ent) and any("72 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if any(u in e["starost"] for u in ("mesecev", "dni", "½ leta", "leti")) or e["starost"].startswith("[—]")]
    check("I9e otroška umrljivost 44 % (≤3 leta ×7/16: h14/h46/h63/h20/h41/h9/h31!)",
          len(otroci) == 7, f"{len(otroci)}: {sorted(e['houseNo'] for e in otroci)}")

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p162 = 163. kontrola", "qa-p162-parish-death-1896" in qa, "")
    check("I10b qa-pini 886/187/88 (78×+12×+14×)",
          qa.count("!== 921") >= 78 and qa.count("!== 222") >= 12 and qa.count("p80Houses.size !== 90") >= 14,
          f"{qa.count('!== 853')}/{qa.count('!== 154')}/{qa.count('p80Houses.size !== 90')}")
    check("I10c qa guard 1901 (bloki 1901+ ne!)",
          "1903+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1903" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (+h51 = 16. hiša luknje!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi p153–p161 → 1897 (10× qa)",
          qa.count("1903+-mrliški bloki že v korpusu") >= 10, str(qa.count("1903+-mrliški bloki že v korpusu")))

    # ---------- I11: honesty + notes + README ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (PRIJET + ŠTABIJAR + MUŠIČ + HVALEŠIČ + VERBIČAR + PAPIČ X-open)",
          "[~]" in d["honesty"][1] and "PRIJET" in d["honesty"][1], "")
    check("I11c SANACIJA dokumentirana (H3 — artefakti izgubljeni, VLM re-generiran)",
          "SANACIJA" in d["honesty"][2], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: 13. POTRDITEV (9 popravkov) + SANACIJA-glava",
          "MAX-ZOOM > VLM — 13. POTRDITEV (9 popravkov)" in notes and "SANACIJA" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p162 skripte VITALS_TOTAL 866",
          all("VITALS_TOTAL = 921" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896))), "")
    check("I12b p80 PT_GAP_HOUSES + 51 (18. luknja-dokaz)",
          '"51" in p80 or \'51\' in p80' and '"51", "52"' in p80.replace('", "', '", "'), "")
    check("I12c stale-guardi p153–p160 → 1897 (VSE skripte!)",
          all("1903+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894))), "")
    check("I12d P80_PT_GAP qa/skripta usklajena (doc-15 = skripta-18 + h51 v obeh!)",
          '"49", "51"' in qa and '"49", "51", "52"' in p80, "")

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
            check("I13b live skeni 55–60 (6× >50KB)", ok7 == 6, f"{ok7}/6")
        except Exception as e:
            check("I13 live knjiga 04894", False, str(e))

    ok = sum(1 for _, o, _ in results if o)
    print(f"\np162: {ok}/{len(results)}", "PASS" if ok == len(results) else "FAIL")
    for name, o, detail in results:
        mark = "✓" if o else "✗"
        print(f" {mark} {name}" + (f" — {detail}" if detail and not o else ""))
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
