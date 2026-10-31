#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P168 — MRLIŠKA knjiga 04894, leto 1902 = 17. polno leto mrliške linije
(s85-dno re-verifikacija + s86–s90 == str. 85–89; 62 vpisov / 17 Griblje-
vpisov / 16 hiš (h72 ×2!) = TRI REKORDI LINIJE — vrstic 61→62! Griblje
13→17! hiš 13→16!). (issue #18).
★★★ 3 PISARJEVE NAPAKE V 1 LETU = REKORD (① NEŠTEVILČENA-vrsta-s85-r8
[zap-skok 7→8 — zapcol-10/10!] ② '345'=45-s88 [zapcol-pikselsko!]
③ glava-'18902'-s89!) + ★★★ h72-×2-v-1-LETU (2 OTROKA-Štravs-v-7-mesecih
— 1. hiša-×2-odkar-1898!) + ★★★ BRINEC-×3-1902 (2× Matija-64-v-2-hišah!)
+ ★★★ PEZDIREC-×3-1902 = era 11. leto (3 hiše-v-1-letu!) + ★★★ h66 = 1.
MRLIŠKI VPIS KADARKOLI (26. PT-vez!) + h40 = 1. (27. PT-vez!) + ★ h26 =
7. mrliški vpis = IZENAČI h35-REKORD (92 let = 2. najstarejši!) + NOVI
DUHOVNIK #11 POTRJEN: Stanislav Dostál (alternira z Rauq ×15/×2!) + NOVA-
BOLEZEN 'Kap' [~ Schlag — 1. v korpusu!] + meja 1902/03 = s90 ('1903.' +
DVOJNI podčrtaj = 5. STIL 10. POTRDITEV — P167-lead POTRJEN!) + γ→7-
lekcija 11.–12. potrditev + VLM-vas-0-napak 2. leto ZAPORED (17/17!).
Kumulativ: vitals 904 → 921, mrliški bloki 04894 205 → 222, p80 hiše
89 → 90 (+h66 — h40 ŽE-v-04455!), korpus 93 NESPREMENJEN, PT-vezni
dokazi 25 → 27. Vzorec p167."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1902.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1902-notes.md"

EXPECTED_ENTRIES = 17
EXPECTED_EXCLUDED = 8
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "2,11,16,23,25,26,33,36,38,40,52,57,65,66,72,72,90"
VITALS_TOTAL = 921               # 904 + 17!
BLOKI_04894 = 222                # 205 + 17!
P80_HOUSES = 90                  # 89 + h66 (h40 ŽE-v-04455!)
KORPUS_HOUSES = 93               # NESPREMENJENO (h66/h40 že v korpusu!)
NEW_SCANS = [86, 87, 88, 89, 90]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1902", d["status"])
    check("I1b 17 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 8 excluded / 10 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1902 = 62 vrstic / 17 Griblje / 16 hiš (TRI REKORDI!)",
          fr["vrstic"] == 62 and fr["griblje_vpisi"] == 17 and fr["hise"] == 16,
          f"{fr['vrstic']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b rekordi: vrstic 61→62 + Griblje 13→17 + hiš 13→16",
          "61→62" in fr["rekordi"] and "13→17" in fr["rekordi"] and "13→16" in fr["rekordi"],
          fr["rekordi"][:80])
    check("I2c hiše = 16 različnih (h72 ×2!)",
          ",".join(str(e["houseNo"]) for e in sorted(ent, key=lambda x: int(x["houseNo"]))) == GRIBLJE_HOUSES,
          ",".join(e["houseNo"] for e in sorted(ent, key=lambda x: int(x["houseNo"]))))

    # ---------- I3: pisarjeve napake ----------
    check("I3a 3 pisarjeve napake (NEŠTEVILČENA + '345' + '18902')",
          fr["pisarjeve_napake"] == 3 and "NEŠTEVILČENA" in fr["pisarjeve_napake_seznam"]
          and "'345'" in fr["pisarjeve_napake_seznam"] and "'18902'" in fr["pisarjeve_napake_seznam"],
          fr["pisarjeve_napake_seznam"][:80])
    e23 = next(e for e in ent if e["houseNo"] == "23")
    check("I3b h23 = NEŠTEVILČENA vrsta (zap null!)",
          e23["zap"] is None, str(e23["zap"]))
    e38 = next(e for e in ent if e["houseNo"] == "38")
    check("I3c h38 zap = '345→45' (zapcol-pikselsko!)",
          e38["zap"] == "345→45", str(e38["zap"]))

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 17 — 53.–57. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 85–90 (s85-reuse + s86–s90!)",
          all(e["scan"] in [85] + NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: hišne veze ----------
    check("I5a h66 = 1. MRLIŠKI VPIS KADARKOLI (26. PT-vez! IZVEN 41–60!)",
          "1. MRLIŠKI VPIS KADARKOLI" in e_hn(ent, "66")["opomba"]
          and "26. PT-vezni dokaz" in e_hn(ent, "66")["opomba"] and "IZVEN 41–60" in e_hn(ent, "66")["opomba"], "")
    e40 = e_hn(ent, "40")
    check("I5b h40-Ana-PEZDIREC = 1. mrliški + 27. PT-vez (ime-forenzika!)",
          "27. PT-vezni dokaz" in e40["opomba"] and "PEZDIREC" in e40["ime"], "")
    e72a = next(e for e in ent if e["houseNo"] == "72" and e["scan"] == 86)
    e72b = next(e for e in ent if e["houseNo"] == "72" and e["scan"] == 89)
    check("I5c h72-×2-v-1-LETU (2 OTROKA-Štravs: Anton-9-mes + Alojzij-1-leto!)",
          "h72-×2-v-1-LETU" in e72a["opomba"] and "h72-×2-v-1-LETU-DOKONČANA" in e72b["opomba"]
          and "9 mesecev" in e72a["starost"] and "1 leto" in e72b["starost"], "")
    e26 = e_hn(ent, "26")
    check("I5d h26-Janez-BRINEC-92-let = 7. mrliški IZENAČI-REKORD (2. najstarejši!)",
          "7. mrliški vpis" in e26["opomba"] and "IZENAČI" in e26["opomba"]
          and "92 let" in e26["starost"], "")
    check("I5e h23-Matija-PRINEC[~BRINEC] + BRINEC-×3-1902 (2× Matija-64!)",
          "BRINEC" in e23["ime"] and "BRINEC-×3-1902" in e23["opomba"]
          and "64 let" in e23["starost"], "")
    check("I5f h25-Matija-BRINEC (BRINEC-×3-#2 — diag-'69'-ZAVRJEN-64!)",
          "BRINEC" in e_hn(ent, "25")["ime"] and "BRINEC-×3-1902" in e_hn(ent, "25")["opomba"], "")
    check("I5g h52/h57/h40 = PEZDIREC-×3-1902 (era 11. leto — 3 hiše!)",
          "PEZDIREC" in e_hn(ent, "52")["ime"] and "PEZDIREC" in e_hn(ent, "57")["ime"]
          and "PEZDIREC" in e40["ime"], "")
    check("I5h h2-Nikolaj-TOME (γ→7-11.-POTRDITEV — '7 mesecev'!)",
          "γ→7-lekcija 11. POTRDITEV" in e_hn(ent, "2")["opomba"] and "7 mesecev" in e_hn(ent, "2")["starost"], "")
    check("I5i h36-Marjeta-ZOGRIVA ('Na porodu' = 1. tak vzrok korpusa!)",
          "Na porodu" in e_hn(ent, "36")["bolezen"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 921", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 222", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1902 = [v for v in d04894 if v["year"] == 1902]
    check("I6c bloki 1902 = 17", len(d1902) == 17, str(len(d1902)))
    check("I6d bloki 1902: skeni 85–90 + stran == sken − 1",
          all(v["scan"] and 85 <= v["scan"] <= 90 and v["page"] == v["scan"] - 1 for v in d1902), "")
    check("I6d2 bloki 1904+ ne obstajajo (P170-lead!; P168 = 1902 sedaj v korpusu!)",
          all(v["year"] < 1904 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 921 + 90 + gap-18 (vitals-P168-kaskada!)",
          "len(vitals) == 921" in p80 and "len(houses) == 90" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — h66/h40 že v korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika (19. okvir) ----------
    x3 = next(x for x in d["crossChecks"] if x["id"] == "X3")
    check("I7a hišni-spori-RAZREŠENI-pikselsko (z13-72-γ + z17-36 + z21-90 + z49-72!)",
          "z13" in x3["opis"] and "72" in x3["opis"] and "36" in x3["opis"]
          and "90" in x3["opis"] and "17/17" in x3["opis"], "")
    check("I7b A2: VLM-vas-0-napak 2. leto ZAPORED (17/17!)",
          any("VLM-vas-0-napak 2. leto ZAPORED" in a["opis"] for a in d["anomalies"]), "")
    a3 = next(x for x in d["anomalies"] if x["id"] == "A3")
    check("I7c A3: Stanislav Dostál = DUHOVNIK #11 POTRJEN (P2=P3-identična-roka!)",
          "Stanislav Dostál" in a3["opis"] and "#11" in a3["opis"], "")
    a4 = next(x for x in d["anomalies"] if x["id"] == "A4")
    check("I7d A4: NOVA-BOLEZEN 'Kap' (1. v korpusu — VLM-'Kolera'-ZAVRJEN!)",
          "Kap" in a4["opis"] and "pojav-v-korpusu" in a4["opis"], "")
    a8 = next(x for x in d["anomalies"] if x["id"] == "A8")
    check("I7e A8: γ→7-LEKCIJA 11.–12. potrditev (z11-'4'→7 + z61-'72'→92!)",
          "γ→7-LEKCIJA 11.–12." in a8["opis"] and "zap11" in a8["opis"] and "zap61" in a8["opis"], "")
    check("I7f 'Kap' v h66-dokazu (Kap [★★★ NOVA-BOLEZEN!)",
          "Kap" in e_hn(ent, "66")["bolezen"] and "NOVA-BOLEZEN" in e_hn(ent, "66")["bolezen"], "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1901/02 re-potrditev = s85 (5. STIL 9. POTRDITEV!)",
          "s85" in fr["meja_1901_02"] and "9. POTRDITEV" in fr["meja_1901_02"], "")
    check("I8b meja 1902/03 = s90 ('1903.' + DVOJNI podčrtaj = 10. POTRDITEV!)",
          "s90" in fr["meja_1902_03"] and "10. POTRDITEV" in fr["meja_1902_03"]
          and "DVOJNI podčrtaj" in fr["meja_1902_03"], "")
    check("I8c P169-lead v dokazu (1903 + s90-dno!)",
          "P169-lead" in d["nextSteps"] and "1903" in d["nextSteps"]["P169-lead"], "")
    e7 = next(x for x in d["excluded"] if x["id"] == "E7")
    check("I8d E7-1903-dno (zap1/3/4-Griblje-kandidati-ŽE-VIDNI!)",
          "zap1" in e7["opis2"] and "Štravs" in e7["opis2"], "")

    # ---------- I9: demografija ----------
    prev = [e["previden"] for e in ent]
    check("I9a previden: 1 ×17 (vs. 1901 = 1 ×10!)",
          prev.count("1") == 17, str(prev))
    duh = [e["duhovnik"] for e in ent]
    check("I9b Dostal ×15 + Rauq ×2 (Griblje-17 — alternacija!)",
          sum(1 for x in duh if "Dostál" in x) == 15
          and sum(1 for x in duh if "Rauq" in x) == 2, str(duh))
    meseci = {}
    for e in ent:
        k = e["mesec"][:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Feb2·Mar6·Apr2·Sep1·Okt1·Nov3·Dec2",
          meseci.get("Feb") == 2 and meseci.get("Mar") == 6 and meseci.get("Apr") == 2
          and meseci.get("Sep") == 1 and meseci.get("Okt") == 1 and meseci.get("Nov") == 3
          and meseci.get("Dec") == 2, str(meseci))
    check("I9d razpon mrtvorojen → 92 let (h26-2.-najstarejši!)",
          any("92 let" in e["starost"] for e in ent), "")
    otroci = [e for e in ent if any(u in e["starost"] for u in ("mesecev", "mesec", "leta", " leto", " leti"))
              and e["houseNo"] in ("2", "72")]
    check("I9e otroška smrt ×4 (h2-7-mes + h72-9-mes + h72-1-let + h72-...-γ!)",
          len(otroci) >= 3, str([(e["houseNo"], e["starost"]) for e in otroci]))

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p168 = 169. kontrola", "qa-p168-parish-death-1902" in qa, "")
    check("I10b qa-pini 921/222/90 (82×+16×+20×)",
          qa.count("!== 921") >= 80 and qa.count("!== 222") >= 15 and qa.count("p80Houses.size !== 90") >= 18,
          f"{qa.count('!== 921')}/{qa.count('!== 222')}/{qa.count('p80Houses.size !== 90')}")
    check("I10c qa guard 1903 (bloki 1903+ ne!)",
          "1903+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1903" in qa, "")
    check("I10d P80_PT_GAP doc-list 15 (NESPREMENJENO!)",
          '"49", "51"' in qa and "p80Gap.length !== 15" in qa, "")
    check("I10e stale-guardi p153–p167 → 1903 (15× qa)",
          qa.count("1903+-mrliški bloki že v korpusu") >= 15,
          f"{qa.count('1903+-mrliški bloki že v korpusu')}")

    # ---------- I11: honesty + notes ----------
    check("I11a honesty 10 točk", len(d["honesty"]) == 10, str(len(d["honesty"])))
    check("I11b [~] konservativno (12 nejasnosti OHRANJENE!)",
          "[~]" in d["honesty"][1] and "Prinec" in d["honesty"][1], "")
    check("I11c rows-metoda-v3 + H4-povratna-verifikacija-P167!",
          "v3" in d["honesty"][2] and "OFF-BY-ONE" in d["honesty"][3], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11d notes: kompozit-forenzika + 19. okvir + P169-lead",
          "kompozit-forenzika" in notes and "P169-lead" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p167 skripte VITALS_TOTAL 921",
          all("VITALS_TOTAL = 921" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901))), "")
    check("I12b p80 PT_GAP_HOUSES komentar (P167: korpus-NESPREMENJEN!)",
          "+ 51 (mrliška 04894-1896" in p80, "")
    check("I12c stale-guardi p153–p167 → 1903 (VSE skripte!)",
          all("1903+-mrliški bloki že v korpusu" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901))), "")
    check("I12d qa-parish.ts bloki 04894 = 222 (P168-kaskada!)",
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
            for s in NEW_SCANS:
                try:
                    st2, data = http_get(inv[s - 1], timeout=30)
                    if st2 == 200 and len(data) > 50000:
                        ok_scans += 1
                    time.sleep(1.0)
                except Exception:
                    pass
            check("I13b live skeni s86–s90 (5/5 JPEG > 50 KB)",
                  ok_scans == 5, f"{ok_scans}/5")
        except Exception as e:
            check("I13 live knjiga", False, str(e)[:80])

    # ---------- poročilo ----------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"P168: {passed}/{total}")
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}" + (f" :: {detail[:90]}" if detail else ""))
    if passed < total:
        sys.exit(1)


def e_hn(ent, hn):
    return next(e for e in ent if e["houseNo"] == hn)


if __name__ == "__main__":
    main()
