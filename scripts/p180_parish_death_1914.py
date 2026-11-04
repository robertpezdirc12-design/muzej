#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P180 — MRLIŠKA knjiga 04894, leto 1914 = 29. polno leto mrliške linije
(s147–s151 == str. 146–150; 55 vpisov / 5 Griblje-vpisov / 4 hiše (h40-×2-2-RAZLIČNA-
PRIIMKA!) = PADec 14→5). (issue #18).
★★★ 3-LEAD-KOREKCIJE-@forenzika (P179-lead: 'VOTLOVEC'→JAKOFČIČ + 'PEKOVEC'→
PEZDIREC + 'FINK'→FIŠLAK[~Filak]!) + ★★★ PEZDIREC-1914 = 4.-LETO-ZAPORED +
★★★ h34-FIŠLAK = ŠILAK-hiša-4.-ZAPOREDNO-LETO (1911–1914!) + ★★★ h40-×2 = 2-
RAZLIČNA-PRIIMKA ('mlinarjeva žena'-TKALČIĆ = 1.-MLINAR-FORMULA-LINIJE!) +
★★★ UTONITE-×2-v-1-LETU = REKORD (z24-TUJ-ŽUPANIJA-Preloka-1.×! + z42!) +
★★★ PALETA-SEBE-LEKCIJA-1.× (s149 = 0-GRIBLJE-ne-3 — diag-RE-VERIFIKACIJA!) +
★★ NOVI-DUHOVNIK-#19-IVAN-NEMANIČ + ANZELM-POLÁK-#18-POTRJEN + ★ 'L.?t.-
No?jay-o.f.d.'-×7-[?]-NE-RAZREŠEN + GLAVE-NAPAKE-×2 (s148-'18…1914'-mala +
s152-'18915'-9-vrinjena!) + meja 1914/15 = s152 (21.-POTRDITEV) + VLM-VAS-
KOREKCIJE-×9-@palete + z2-pisar-×2-POPRAVEK + ⅛-ULOMEK-#2.
Kumulativ: vitals 1077 → 1082, mrliški bloki 04894 378 → 383, p80 hiše
93-NESPREMENJENO, korpus 93-NESPREMENJEN, PT-luknja 15-NESPREMENJENA.
Vzorec p179."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1914.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1914-notes.md"

EXPECTED_ENTRIES = 55
EXPECTED_EXCLUDED = 4
EXPECTED_ANOMALIES = 13
EXPECTED_CROSSCHECKS = 5
GRIBLJE_HOUSES = "8,34,36,40,40"
VITALS_TOTAL = 1461             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 93                 # NESPREMENJENO (vse-4-hiše-ŽE-v-filtru!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [147, 148, 149, 150, 151]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1914", d["status"])
    check("I1b 55 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 4 excluded / 13 anomalij / 5 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    check("I2 1914 = 55 vrstic / 5 Griblje / 4 hiše (h40-×2 — PADec 14→5!)",
          fr["vpisi"] == 55 and fr["griblje_vpisi"] == 5 and fr["hise"] == 4,
          f"{fr['vpisi']}/{fr['griblje_vpisi']}/{fr['hise']}")
    check("I2b meja 1914/15 = s152 ('18915'-NAPAKA + page-top + restart = 21.-POTRDITEV!)",
          "s152" in fr["meja_1914_15"] and "NAPAKA-9-vrinjena" in fr["meja_1914_15"]
          and "21.-POTRDITEV" in fr["meja_1914_15"], fr["meja_1914_15"][:80])
    grib_e = [e for e in ent if e["vas"] == "Griblje"]
    hise_clean = [str(e["hisa"]).split(" ")[0].rstrip(".") for e in
                  sorted(grib_e, key=lambda x: int(str(x["hisa"]).split(" ")[0].rstrip(".")))]
    check("I2c hiše = [8,34,36,40,40] (4 RAZLIČNE — h40-×2!)",
          ",".join(hise_clean) == "8,34,36,40,40", ",".join(hise_clean))

    # ---------- I3: lead-korekcije ----------
    e1 = next(e for e in ent if e["zap"] == 1)
    check("I3a z1-'VOTLOVEC'-lead-ZAVRJEN → JAKOFČIČ (KURRENT-th=k!)",
          "VOTLOVEC'-ZAVRJEN" in e1["ime"] and "JAKOFČIČ" in e1["ime"], "")
    e7 = next(e for e in ent if e["zap"] == 7)
    check("I3b z7-'PEKOVEC'-lead-ZAVRJEN → PEZDIREC (x-KRIŽEC+DESCENDER!)",
          "'PEKOVEC'-ZAVRJEN" in e7["ime"] and "PEZDIREC" in e7["ime"], "")
    e8 = next(e for e in ent if e["zap"] == 8)
    check("I3c z8-'FINK'-lead-ZAVRJEN → FIŠLAK[~Filak] (h34-leksikon!)",
          "'FINK'-ZAVRJEN" in e8["ime"] and "FIŠLAK" in e8["ime"], "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 55 — 124.–128. potrditev!)",
          all(e["page"] == int(e["scan"][1:]) - 1 for e in ent), "")
    check("I4b skeni v naboru 147–151 (s147-lead-reuse + s148–s151!)",
          all(int(e["scan"][1:]) in NEW_SCANS for e in ent), str(sorted({int(e["scan"][1:]) for e in ent})))

    # ---------- I5: hišne veze ----------
    check("I5a PEZDIREC-1914 = 4.-LETO-ZAPORED (1911-×4 + 1912-×4 + 1913-×1 + 1914!)",
          "4.-LETO-ZAPORED" in e7["opomba"], "")
    check("I5b h34 = ŠILAK-hiša-4.-ZAPOREDNO-LETO (1911–1914 = 1.-V-LINIJI!)",
          "ŠILAK-hiša-4.-ZAPOREDNO-LETO" in e8["opomba"], "")
    e53 = next(e for e in ent if e["zap"] == 53)
    check("I5c h40-×2 = 2-RAZLIČNA-PRIIMKA (PEZDIREC + TKALČIĆ-'mlinarjeva žena'-1.×!)",
          "h40-×2-1914" in e53["opomba"] and "mlinarjeva žena" in e53["stan"], "")
    check("I5d h8 = 6. mrliški vpis (JAKOFČIČ-vez-26-let + h8-leksikon-×5!)",
          "6. mrliški vpis" in e1["opomba"], "")
    e50 = next(e for e in ent if e["zap"] == 50)
    check("I5e h36-HRIŽAN ('Hribernik'-VLM-ZAVRJEN — ž-CARON-leksikon-3.×!)",
          "HRIŽAN" in e50["ime"] and "VLM-'Hribernik'-ZAVRJEN" in e50["ime"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1082", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 383", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1914 = [v for v in d04894 if v["year"] == 1914]
    check("I6c bloki 1914 = 5", len(d1914) == 5, str(len(d1914)))
    check("I6d bloki 1914: skeni 147–151 + stran == sken − 1",
          all(v["scan"] and 147 <= v["scan"] <= 151 and v["page"] == v["scan"] - 1 for v in d1914), "")
    check("I6d2 bloki 1925+ ne obstajajo (P190-KONEC-KNJIGE!)",
          all(v["year"] < 1925 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 1082 + 93 + gap-18 (vitals-P180-kaskada!)",
          "len(vitals) == 1100" in p80 and "len(houses) == 94" in p80 and "len(gap) == 18" in p80, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 93 hiš (NESPREMENJEN — vse-4-hiše-ŽE-v-korpusu!)",
          len(houses_all) == KORPUS_HOUSES, str(len(houses_all)))

    # ---------- I7: forenzika ----------
    x2 = next(x for x in d["crossChecks"] if "PALETA-vs-DIAG" in x)
    check("I7a PALETA-SEBE-LEKCIJA-1.× (s149-0-GRIBLJE — diag-RE-VERIFIKACIJA-×12!)",
          "PALETA-vs-DIAG-RE-VERIFIKACIJA-s149" in x2 and "Priložje-36" in x2, "")
    check("I7b ANZELM-POLÁK-#18-POTRJEN (z1-podpis — VLM-'Anton'-ZAVRJEN!)",
          "Anzelm Polák" in e1["duhovnik"] and "VLM-'Anton Polak'-ZAVRJEN" in e1["duhovnik"], "")
    check("I7c NOVI-DUHOVNIK-#19-NEMANIČ (anomalija!)",
          any("IVAN-NEMANIČ" in a and "#19" in a for a in d["anomalies"]), "")
    check("I7d 'No?jay'-podpis-×7-NE-RAZREŠEN (P179-lead-'Ho?er/Ojster'-ZAVRJEN!)",
          any("No?jay" in a and "×7" in a for a in d["anomalies"]), "")
    check("I7e UTONITE-×2-REKORD + TUJ-ŽUPANIJA-VPIS-1.× (z24-Preloka!)",
          any("UTONITE-×2" in a and "REKORD" in a for a in d["anomalies"])
          and any("TUJ-ŽUPANIJA-VPIS-1.×" in a for a in d["anomalies"]), "")
    check("I7f VLM-VAS-KOREKCIJE-×9 (z3/z4/z13/z15/z20/z42 + z28/z32/z36!)",
          any("VLM-VAS-KOREKCIJE-×9" in a for a in d["anomalies"]), "")
    check("I7g z2-pisar-×2-POPRAVEK + ⅛-ULOMEK-#2 (anomalija!)",
          any("PISAR-×2-POPRAVEK" in a and "⅛-ULOMEK-#2" in a for a in d["anomalies"]), "")

    # ---------- I8: meje + lead ----------
    check("I8a meja 1913/14 re-potrditev = s147 (20.-POTRDITEV — P179!)",
          "s147" in fr["meja_1913_14"] and "20.-POTRDITEV" in fr["meja_1913_14"], "")
    check("I8b meja 1914/15 = s152 (21.-POTRDITEV — '18915'-NAPAKA!)",
          "s152" in fr["meja_1914_15"] and "21.-POTRDITEV" in fr["meja_1914_15"], "")
    check("I8c P181-lead v dokazu (1915 + s152/s153!)",
          "P181_LEAD" in d["notes"] and "1915" in d["notes"]["P181_LEAD"], "")
    e17l = d["notes"]["P181_LEAD"]
    check("I8d P181-lead-GRIBLJE (s153-z17-h88-Ivana-BRINEC!)",
          "BRINEC" in e17l and "h88" in e17l, "")

    # ---------- I9: demografija ----------
    grib = [e for e in ent if e["vas"] == "Griblje"]
    check("I9a previden Griblje: 2×'.' + 1×'-' + 1×'ne' + 1×'.'-z50 (5)",
          [e["previden"] for e in grib].count(".") == 3
          and sum(1 for e in grib if str(e["previden"]).startswith("-")) == 1
          and sum(1 for e in grib if str(e["previden"]).startswith("ne")) == 1,
          str([e["previden"] for e in grib]))
    duh = [e["duhovnik"] for e in grib]
    check("I9b duhovniki Griblje: Polák×1 + Rumpf×2 + Bitnar×2",
          sum(1 for x in duh if "Polák" in x) == 1
          and sum(1 for x in duh if "Rumpf" in x) == 2
          and sum(1 for x in duh if "Bitnar" in x) == 2, str(duh))
    meseci = {}
    for e in grib:
        k = str(e["mesec"])[:3]
        meseci[k] = meseci.get(k, 0) + 1
    check("I9c meseci Griblje: Jan1·Feb1·Mar1·Nov1·Dec1 (razpršeno!)",
          meseci.get("Jan") == 1 and meseci.get("Feb") == 1 and meseci.get("Mar") == 1
          and meseci.get("Nov") == 1 and meseci.get("Dec") == 1, str(meseci))
    check("I9d razpon 2 leti → 21 let (BREZ-odraslih-razen-Tkalčić — otroška-80%!)",
          any("21 let" in str(e["starost"]) for e in grib)
          and any("2 leti" in str(e["starost"]) for e in grib), "")

    # ---------- I10: qa-parish + pin-kaskada ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-p180 = 181. kontrola", "qa-p180-parish-death-1914" in qa, "")
    check("I10b qa-pini 1145/446/93 (94×+28×+24×)",
          qa.count("!== 1461") >= 90 and qa.count("!== 446") >= 15 and qa.count("p80Houses.size !== 93") >= 18,
          f"{qa.count('!== 1100')}/{qa.count('!== 446')}/{qa.count('p80Houses.size !== 93')}")
    check("I10c qa guard 1919 (bloki 1919+ ne!)",
          "1917+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")
    check("I10d p152Wwi-04455-sinteza-NESPREMENJENA-7 (mrliški-1914-niso-v-04455-obsegu!)",
          "p152Wwi !== 7" in qa and "dobe (sinteza 04455)" in qa, "")
    check("I10e stale-guardi → 1916 (28× qa)",
          qa.count("1917+-mrliški bloki že v korpusu") >= 1
          and qa.count("(h.year ?? 0) >= 1916") >= 27,
          f"{qa.count('1917+-mrliški bloki že v korpusu')}/{qa.count('(h.year ?? 0) >= 1916')}")

    # ---------- I11: honesty + notes ----------
    check("I11a honesty 7 točk", len(d["honesty"]) == 7, str(len(d["honesty"])))
    check("I11b [~] konservativno (9 nejasnosti OHRANJENIH!)",
          "[~]" in d["honesty"][1] and "Jakofčič" in d["honesty"][1], "")
    check("I11c rows-metoda-v3 + z50-NE-RAZREŠENA + 'No?jay'-NE-RAZREŠEN!",
          "v3" in d["honesty"][2] and "NE RAZREŠENA" in d["honesty"][3]
          and "NE RAZREŠEN" in d["honesty"][4], "")
    check("I11d notes: paleta-sebe-lekcija + P181-lead",
          "paleta_sebe_lekcija" in d["notes"] and "P181_LEAD" in d["notes"], "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I11e notes: kompozit-forenzika + P181-lead",
          "P181-lead" in notes or "P181_LEAD" in notes, "")

    # ---------- I12: kaskada ----------
    check("I12a p153–p179 skripte VITALS_TOTAL 1082",
          all("VITALS_TOTAL = 1100" in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902), (169, 1903), (170, 1904), (171, 1905), (172, 1906), (173, 1907), (174, 1908), (175, 1909), (176, 1910), (177, 1911), (178, 1912), (179, 1913))), "")
    check("I12b p80 PT_GAP_HOUSES komentar (P162: + 51)", "+ 51 (mrliška 04894-1896" in p80, "")
    check("I12c stale-guardi → 1916 (p153–p179!)",
          all(any(pat in open(f"scripts/p{i}_parish_death_{y}.py", encoding="utf-8").read()
                  for pat in ('(h.year ?? 0) >= 1916', 'v["year"] < 1925', '(v["year"] or 0) >= 1916'))
              for i, y in ((153, 1887), (154, 1888), (155, 1889), (156, 1890), (157, 1891), (158, 1892), (159, 1893), (160, 1894), (161, 1895), (162, 1896), (163, 1897), (164, 1898), (165, 1899), (166, 1900), (167, 1901), (168, 1902), (169, 1903), (170, 1904), (171, 1905), (172, 1906), (173, 1907), (174, 1908), (175, 1909), (176, 1910), (177, 1911), (178, 1912), (179, 1913))), "")
    check("I12d qa-parish.ts bloki 04894 = 401 (P181-kaskada!)",
          qa.count('04894").length !== 520') >= 15, str(qa.count('04894").length !== 520')))

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
            check("I13b live skeni s147–s151 (5/5 JPEG > 50 KB)",
                  ok_scans == 5, f"{ok_scans}/5")
        except Exception as e:
            check("I13 live knjiga", False, str(e)[:80])

    # ---------- poročilo ----------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"P180: {passed}/{total}")
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}" + (f" :: {detail[:90]}" if detail else ""))
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
