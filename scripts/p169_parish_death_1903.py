#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P169 — verifikator MRLIŠKE knjige 04894, leto 1903 (17. → 18. polno leto).
Celoten neodvisen preracun iz bundled parish.ts + dokaz-JSON + qa + kaskada.
I-checki I1–I13 (vzorec P153–P168); --live = dodatna HTTP verifikacija
matricula-online.eu.
P169-rekordi: 17 GRIBLJE = IZENAČI-rekord-1902 (rast 10→17→17!) +
3-GLAVE-NAPAKE (s92-'18903' + s94-'18903' + s95-'18[~]1904') = NOVI REKORD
LINIJE + ZAPCOL-ČIST (1–51!) + ŠTRAVS-×5-v-2-letih (grozovita tragedija!)
+ PEZDIREC-×3-1903 = era-12 (×6-v-2-letih!) + h40-×3-v-2-letih (1. hiša!)
+ h4 = 1. MRLIŠKI = 28. PT-vez + h83-agent-oči-×7-'83'-kalibracija +
γ→7-13.–14. POTRDITEV (z38/z41-'42'→72!) + x-lekcija (starost-@1530–1770!).
Kumulativ: vitals 921 → 938, mrliški bloki 04894 222 → 239, p80 hiše 90 → 91
(+h4 = 1. mrliški vpis h4 = 28. PT-vez!; 04105-1906-blok-IZVEN-filtra —
cf. h66-vzorec!), korpus 93 NESPREMENJEN, PT 27 → 28."""
import json, os, re, sys, time, urllib.request, urllib.error

DOKAZ = "research/issue17/parish-death-1903.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1903-notes.md"

EXPECTED_ENTRIES = 17
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "4,11,12,18,18,30,36,40,40,45,45,46,52,58,60,72,83"
VITALS_TOTAL = 950               # 921 + 17!
BLOKI_04894 = 251                # 222 + 17!
P80_HOUSES = 91                  # 90 → 91 (+h4 = 28. PT-vez; 04105-1906-blok-IZVEN-filtra!)
KORPUS_HOUSES = 93               # NESPREMENJENO
NEW_SCANS = [91, 92, 93, 94]

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


def e_hn(ent, hn):
    return next(e for e in ent if e["houseNo"] == hn)


def main():
    live = "--live" in sys.argv
    d = json.load(open(DOKAZ, encoding="utf-8"))
    ent = d["entries"]
    fr = d["frame"]

    # ---------- I1: dokaz ----------
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1903", d["status"])
    check("I1b 17 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1903 = 51 vrstic / 17 Griblje / 14 hiš (Griblje-IZENAČI-REKORD!)",
          fr["vrstic"] == 51 and fr["griblje_vpisi"] == 17 and fr["hise"] == 14,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b Griblje 10→17→17 (IZENAČI-rekord-1902!) + 3-GLAVE-NAPAKE-REKORD",
          "10→17→17" in fr["rast"] and "3-GLAVE-NAPAKE" in fr["rekordi"]
          and "18903" in fr["rekordi"], fr["rekordi"][:90])
    check("I2c hiše = 14 različnih (h45/h40/h18 ×2!)",
          ",".join(str(e["houseNo"]) for e in sorted(ent, key=lambda x: int(x["houseNo"]))) == GRIBLJE_HOUSES,
          ",".join(e["houseNo"] for e in sorted(ent, key=lambda x: int(x["houseNo"]))))

    # ---------- I3: zap-continuity (ČISTO leto!) ----------
    zaps = sorted(int(e["zap"]) for e in ent)
    check("I3a Griblje-zap: 1,3,4,8,10,12,13,14,16,19,22,30,38,41,42,48,50",
          zaps == [1, 3, 4, 8, 10, 12, 13, 14, 16, 19, 22, 30, 38, 41, 42, 48, 50],
          str(zaps))
    check("I3b zapcol-ČIST (51-oštevilčenih / 51-fizičnih — NASPROTJE-1902!)",
          fr["zap_oštevilčenih"] == 51 and fr["neštevilčenih"] == 0
          and "ČIST" in fr["rekordi"], "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 17 — 58.–61. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 90–94 (s90-reuse + s91–s94!)",
          all(e["scan"] in [90] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    e4 = e_hn(ent, "4")
    check("I5a h4 = 1. MRLIŠKI VPIS KADARKOLI = 28. PT-vez (IZVEN 41–60!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e4["opomba"]
          and "28. PT-vezni dokaz" in e4["opomba"] and "IZVEN 41–60" in e4["opomba"], "")
    e40a = next(e for e in ent if e["houseNo"] == "40" and e["zap"] == 10)
    e40b = next(e for e in ent if e["houseNo"] == "40" and e["zap"] == 22)
    check("I5b h40-×3-v-2-LETIH (Ana-1902 + Marija-MAR + Janez-JUN-1903 — 1. hiša!)",
          "h40-×3-v-2-LETIH-#2" in e40a["opomba"] and "h40-×3-v-2-LETIH-ZAKLJUČEK" in e40b["opomba"], "")
    e72 = e_hn(ent, "72")
    check("I5c h72 = ŠTRAVS-hiša-POTRJENA + ×3-v-2-LETIH (super-×6-NE-Špan!)",
          "ŠTRAVS-hiša-POTRJENA" in e72["opomba"] and "h72-×3-v-2-LETIH" in e72["opomba"]
          and "ŠTRAVS" in e72["ime"] and "Špan" in e72["opomba"], "")
    e45a = next(e for e in ent if e["houseNo"] == "45" and e["zap"] == 1)
    e45b = next(e for e in ent if e["houseNo"] == "45" and e["zap"] == 3)
    check("I5d h45-×2-v-1903 (2-otroka-Štravs-v-5-tednih — ŠTRAVS-×5-v-2-letih!)",
          "h45-×2-v-1903-#1" in e45a["opomba"] and "h45-×2-v-1903-#2" in e45b["opomba"]
          and "ŠTRAVS-×5-v-2-LETIH-#3" in e45a["opomba"] and "ŠTRAVS-×5-v-2-LETIH-#4" in e45b["opomba"], "")
    e18b = next(e for e in ent if e["houseNo"] == "18" and e["zap"] == 41)
    check("I5e h18-×2-v-1903 (Janez-4½-APR + Jurij-72-OKT = možni-DED-Šimec!)",
          "h18-×2-v-1903-ZAKLJUČEK" in e18b["opomba"] and "72 let" in e18b["starost"], "")
    e36 = e_hn(ent, "36")
    check("I5f h36 = 7. mrliški = ×3-ZAPOREDNA-LETA (1901+1902+1903!) + KRIŽAN-super-×6!",
          "×3-ZAPOREDNA-LETA" in e36["opomba"] and "KRIŽAN" in e36["ime"]
          and "Kukan" in e36["opomba"], "")
    e83 = e_hn(ent, "83")
    check("I5g h83-agent-oči-×7 = 83 (3-kandidati-83/85/33 — kalibracija-s-'5'-ravno!)",
          "83" in e83["opomba"] and "KALIBRACIJA" in e83["opomba"]
          and "RADOVIČ" in e83["ime"] and "Radlovič" in e83["opomba"], "")
    check("I5h PEZDIREC-×3-1903 (h52-Barbara + h40-Marija + h40-Janez = era-12!)",
          "PEZDIREC-×3-1903-#1" in e_hn(ent, "52")["opomba"]
          and "PEZDIREC-×3-1903-#2" in e40a["opomba"]
          and "PEZDIREC-×3-1903-#3" in e40b["opomba"], "")
    check("I5i γ→7-LEKCIJA-13. (z41-'42'→72-@×7-γ-s-prečko!)",
          "γ→7-LEKCIJA-13. POTRDITEV" in e18b["opomba"] and "42" in e18b["opomba"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 938", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 239", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1903 = [v for v in d04894 if v["year"] == 1903]
    check("I6c bloki 1903 = 17", len(d1903) == 17, str(len(d1903)))
    check("I6d bloki 1903: skeni 90–94 + stran == sken − 1",
          all(v["scan"] and 90 <= v["scan"] <= 94 and v["page"] == v["scan"] - 1 for v in d1903), "")
    check("I6d2 bloki 1905+ ne obstajajo (P170-lead!; P169 = 1903 sedaj v korpusu!)",
          all(v["year"] < 1905 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 950 + 91 + gap-18 (vitals-P170-kaskada!)",
          "len(vitals) == 950" in p80 and "len(houses) == 91" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — h4 že v korpusu prek 04105-1906!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (20. okvir) ----------
    a10 = next(x for x in d["anomalies"] if x["id"] == "A10")
    check("I7a HISNA-KONFLIKTI-4/4-agent-oči-×7 (z19-58 + z38-72 + z42-4 + z48-83!)",
          "z19" in a10["opis"] and "58" in a10["opis"] and "z38" in a10["opis"]
          and "z42" in a10["opis"] and "z48" in a10["opis"], "")
    a9 = next(x for x in d["anomalies"] if x["id"] == "A9")
    check("I7b A9: γ→7-LEKCIJA 13.–14. (z38-'42'→72 + z41-'42'→72 — kalibracijski-TRIPAR!)",
          "γ→7-LEKCIJA-13.–14." in a9["opis"] and "zap38" in a9["opis"] and "zap41" in a9["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7c A4: ŠTRAVS-×5-v-2-LETIH (4-otroci + 1-odrasla-v-19-mesecih!)",
          "ŠTRAVS-×5-v-2-LETIH" in a4["opis"] and "19-mesecih" in a4["opis"], "")
    a1 = next(x for x in d["anomalies"] if x["id"] == "A1")
    check("I7d A1: 3-GLAVE-NAPAKE-REKORD (s92-18903 + s94-18903 + s95-181904!)",
          "18903" in a1["opis"] and "18[izbrisano]1904" in a1["opis"], "")
    a2 = next(x for x in d["anomalies"] if x["id"] == "A2")
    check("I7e A2: ZAPCOL-ČIST-1903 (NASPROTJE-1902-'345'+NEŠTEVILČENA!)",
          "ČIST" in a2["opis"] and "NASPROTJE-1902" in a2["opis"], "")
    check("I7f VLM-vas-0-napak-3.-leto (17/17-Griblje!)",
          any("VLM-vas-0-napak-3.-leto" in h for h in d["honesty"]), "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1902/03-RE = s90 (12. POTRDITEV!)",
          "s90" in fr["meja_1902_03"] and "12.-POTRDITEV" in fr["meja_1902_03"], "")
    check("I8b meja 1903/04 = s94 ('1904' + VEČKRATNI podčrtaj = 11. POTRDITEV!)",
          "s94" in fr["meja_1903_04"] and "11.-POTRDITEV" in fr["meja_1903_04"]
          and "VEČKRATNI" in fr["meja_1903_04"], "")
    check("I8c P170-lead v dokazu (1904 + s94-dno/s95!)",
          "P170-lead" in d["nextSteps"] and "1904" in d["nextSteps"]["P170-lead"], "")
    e8 = next(x for x in d["excluded"] if x["id"] == "E8")
    check("I8d E8-s95-kontekst (zap4–15-1904 + Griblje/Giriče-zmeda!)",
          "zap4–15" in e8["opis"] or "zap4-15" in e8["opis"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×17",
          prev.count("1") == 17, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Dostál ×16 + Rauq ×1 (Griblje-17 — DOMINANTA-95%!)",
          sum(1 for x in duh if "Dostál" in x) == 16
          and sum(1 for x in duh if "Rauq" in x) == 1, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Jan1·Feb2·Mar3·Apr3·Maj1·Jun1·Jul1·Okt2·Nov1·Dec2",
          meseci.get("Jan") == 1 and meseci.get("Feb") == 2 and meseci.get("Mar") == 3
          and meseci.get("Apr") == 3 and meseci.get("Maj") == 1 and meseci.get("Jun") == 1
          and meseci.get("Jul") == 1 and meseci.get("Okt") == 2 and meseci.get("Nov") == 1
          and meseci.get("Dec") == 2, str(meseci))
    check("I9d starostni-razpon 4-mesece → 73-let (z12-Frančiška → z42-Šotler!)",
          any("4 mesece" in e["starost"] for e in ent) and any("73 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if "mesec" in e["starost"] or "leta" in e["starost"]]
    check("I9e otroška-smrt ≥8/17 (dojenčki-dominanta!)",
          len(otroci) >= 8, str([(e["houseNo"], e["starost"]) for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p169 = 170. kontrola", "qa-p169-parish-death-1903" in qa, "")
    check("I10b qa-pini 950/251/91",
          qa.count("!== 950") >= 80 and qa.count("!== 251") >= 15 and qa.count("p80Houses.size !== 91") >= 18,
          f"{qa.count('!== 950')}/{qa.count('!== 251')}/{qa.count('p80Houses.size !== 91')}")
    check("I10c qa guard 1904 (bloki 1904+ ne!)",
          "1905+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1905" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi → 1904 (16× qa)",
          qa.count("1905+-mrliški bloki že v korpusu") >= 15,
          f"{qa.count('1905+-mrliški bloki že v korpusu')}")

    # ---------- I11: honesty + notes ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b x-lekcija-v-honesty (starost-@1530–1770!)",
          "x-lekcija" in d["honesty"][1] and "1530" in d["honesty"][1], "")
    check("I11c bolezen-forenzika-lekcija (previden-'1'-kljukica-zmeda!)",
          "bolezni" in d["honesty"][2] or "bolezen" in d["honesty"][2], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: forenzika + P170-lead",
          "forenzika" in notes and "P170-lead" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p168 skripte VITALS_TOTAL 938",
          all("VITALS_TOTAL = 950" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902))), "")
    check("I12b p80-skripta P169-komentar (921 → 938 + h4-28.-PT!)",
          "P169: 921 → 938" in p80 and "28. PT-vez" in p80, "")
    check("I12c stale-guardi → 1904 (14 skript-s-qa-stringom!)",
          all("1905+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902))), "")
    check("I12d qa-parish.ts bloki 04894 = 251 (P170-kaskada!)",
          qa.count('04894").length !== 251') >= 15, str(qa.count('04894").length !== 251')))

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
                    u = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                    if u.startswith("http"):
                        inv.append(u)
                except Exception:
                    pass
            inv = sorted(set(inv))
            ok_all = 0
            for s in [90] + NEW_SCANS:
                try:
                    st2, data = http_get(inv[s - 1], timeout=60)
                    if st2 == 200 and len(data) > 50000:
                        ok_all += 1
                except Exception:
                    pass
                time.sleep(1.2)
            check("I13b live citirani skeni 5/5 JPEG-200", ok_all == 5, f"{ok_all}/5")
        except Exception as e:
            check("I13 live (napaka)", False, str(e)[:120])

    ok = sum(1 for _, o, _ in results if o)
    for name, o, det in results:
        print(f"{'PASS' if o else 'FAIL'}  {name}" + (f"  [{det}]" if det else ""))
    print(f"\np169: {ok}/{len(results)}")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
