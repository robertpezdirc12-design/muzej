#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P188 — MRLIŠKA knjiga 04894, leto 1922 = 37. polno leto mrliške linije (issue #18):
s231 (z1–z6) + s232–s238 + s239-z49/z50 == str. 230–238 (stran == sken − 1 —
167.–188. potrditev!) + 50 vpisov / 14 GRIBLJE / 13 hiš (h14-×2!) + ★★★ Remigi-
JEREB-žup.-dominanta (~41 — #24-P187-'knj.uprav.'-kandidat-POTRJEN-kot-ŽUPNIK!
garble-×5-forma: 'Ferč/Ferelj/Jurec/Jeréb/Jos-Rauč-Ferch'-VSI-ZAVRŽENI!) + ★★
CERAR-'prošt-v-Metliki'-#23-COMEBACK-1.× + ★★ Ivan-NEMANJIČ-'žup.-v-pokojini-
v-Metliki'-#25-kandidat = METLIKA-×2-CROSSOVER! + ★★★ z36-UTOPITEV (NESREČA-2.-
leto-zapored cf. 1921-z8-padec-z-voza!) + ★★ z49-'padec-s-poda'-NESREČA + ★★★
MRTVOROJENO-×2-#15+#16 (z47-N.-BRINE-h14-PODPIS-PRAZEN-2.×-forma-cf.-1920-z1!
+ z11-N.-JAKOFČIČ!) + ★★★ h14-×2-BRINEC-v-1-LETU + ★★★ PERDIH-BOOM-×4-v-1-LETU
(z1-Marija + z22-Ivana + z28-Ana + z33-Matija-Gradac!) + ★★★ KOSTNI-KRI-×2-
CONTINUITETA-4.-LETO + ★★★ z10-VLAŠINEC + ★★★ z8-NOVGRADAC-'služkinja-iz-občine-
Zadale-na-Hrvatskem'-MIGRANTKA-DELAVKA-1.×-FORMA (1.×-priimek!) + ★★ z13-JARAJEVIČ-
'samska-DELAVNICA' + 'vžithar'-stan-×2-IDENTIČEN-glif-cf.-P187-MUSIČ + glava-s239-
'1922'-PREČRTANO+POPRAVLJENO-2.-leto-zapored! + MEJA 1922/23 = s239-MID ('19 23'
+ restart-z1 = 29.-POTRDITEV — 3.-leto-zapored-meja-na-dnu-strani! kurator-visual!).
Kumulativ: vitals 1180 → 1194, mrliški bloki 04894 481 → 495, p80 hiše 94-
NESPREMENJENO, korpus 93-NESPREMENJEN, PT-luknja 18-NESPREMENJENA. Vzorec p187."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1922.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1922-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 50
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 16
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "9,11,14,14,18,20,21,25,33,35,48,53,60,71"
VITALS_TOTAL = 1355             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 94                 # NESPREMENJENO
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [231, 232, 233, 234, 235, 236, 237, 238, 239]

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
            else:
                raise
        except Exception as e:
            last = e
            time.sleep(2)
    raise last


def main():
    live = "--live" in sys.argv

    # ---------- I1: dokaz-JSON ----------
    d = json.load(open(DOKAZ, encoding="utf-8"))
    check("I1a status-D1922", d["status"] == "SAMPLE-TRANSCRIPTION-D1922", d["status"])
    check("I1b knjiga-04894-leto-1922", d["book"] == "04894" and d["year"] == 1922, "")
    check("I1c 50-vpisov", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1d 0-excluded", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1e 16-anomalij", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1f 8-crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    check("I1g 11-honesty", len(d["honesty"]) == 11, str(len(d["honesty"])))

    # ---------- I2: okvir (stran == sken − 1; s231–s239; z1–z50) ----------
    ok_scan = all(e["page"] == e["scan"] - 1 and 231 <= e["scan"] <= 239 for e in d["entries"])
    check("I2a stran-==-sken-1-s231–s239", ok_scan, "")
    zaps = [e["zap"] for e in d["entries"]]
    check("I2b zaporedne-1–50-kompletne", zaps == list(range(1, 51)), str(zaps[:5]) + "…" + str(zaps[-3:]))
    grib = [e for e in d["entries"] if e["griblje"]]
    check("I2c 14-Griblje", len(grib) == 14, str(len(grib)))
    check("I2d hiše-14-Griblje", ",".join(sorted((e["houseNo"] for e in grib), key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted((e["houseNo"] for e in grib), key=int)))

    # ---------- I3: forenzika-markerji (kurator-visual) ----------
    def si(zap):
        e = next((e for e in d["entries"] if e["zap"] == zap), {})
        return (e.get("whatSi", "") + " " + e.get("ime", "") + " " + e.get("duhovnik", ""))
    check("I3a z1-PERDIH-BOOM-h20", "PERDIH-BOOM" in si(1) and "Papežare" in si(1), "")
    check("I3b z3-PLUT-lead-potrjen", "PLUT" in si(3), "")
    check("I3c z4-KOSTNI-KRI-4.-leto", "Kostni kri" in si(4), "")
    check("I3d z8-NOVGRADAC-MIGRANTKA", "MIGRANTKA-DELAVKA-1.×-FORMA" in si(8), "")
    check("I3e z13-JARAJEVIČ-DELAVNICA", "DELAVNICA" in si(13), "")
    check("I3f z22-'Uršula-Pezdirc'-ZAVRŽENO", "Uršula-Pezdirc'-ZAVRŽENO" in si(22), "")
    check("I3g z31-'Jakopec'-ZAVRŽENO", "'Jakopec'-ZAVRŽENO" in si(31), "")
    check("I3h z36-UTOPITEV-2.-leto", "UTOPITEV — NESREČA-2.-LETO-ZAPORED" in si(36), "")
    check("I3i z47-MRTVOROJEN-#15-PODPIS-PRAZEN", "#15-korpusa" in si(47) and "PODPIS-PRAZEN" in si(47), "")
    check("I3j z50-BRINEC-ZADNJA-1922", "ZADNJA-1922-VRSTA" in si(50), "")

    # ---------- I4: anomalije-ključi ----------
    tips = " | ".join(a["tip"] for a in d["anomalies"])
    for key in ("utopitev-nesreca-2-leto", "mrtvorojen-15-korpusa", "h14-x2-brinec",
                "perdih-boom-x4", "vlasinec-z10", "novgradac-migrantka-1x",
                "cerar-prost-comeback", "metlika-crossover", "vzithar-stan-x2",
                "glava-precrano-popravljeno"):
        check(f"I4-{key}", key in tips, "")

    # ---------- I5: crossChecks-ključi ----------
    xids = " ".join(c["id"] for c in d["crossChecks"])
    check("I5-crossChecks-X1–X8", all(f"X{i}" in xids for i in range(1, 9)), xids)

    # ---------- I6: parish.ts bloki ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    b1922 = re.findall(r'houseNo: "(\d+)",\s*bookSignature: "04894",\s*year: 1922,', src)
    check("I6a parish.ts-14-blokov-1922", len(b1922) == 14, str(len(b1922)))
    check("I6b hiše-1922-v-parish.ts", ",".join(sorted(b1922, key=int)) == "9,11,14,14,18,20,21,25,33,35,48,53,60,71",
          ",".join(sorted(b1922, key=int)))
    b1923 = re.findall(r'bookSignature: "04894",\s*year: 1925', src)
    check("I6d 0-blokov-04894-1925 (P190-KONEC-KNJIGE!)", len(b1923) == 0, str(len(b1923)))
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1194 + 94 + gap-18",
          "len(vitals) == 1355" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I7a qa-pini 1355 (90×+)", qa.count("!== 1355") >= 90, str(qa.count("!== 1355")))
    check("I7b qa-pini 520 (15×+)",
          qa.count('04894").length !== 520') >= 15
          and "p80Death.length !== 520" in qa, str(qa.count('04894").length !== 520')))
    check("I7c qa-p188 = 189. kontrola", "qa-p188-parish-death-1922" in qa, "")
    check("I7d qa guard 1925 (bloki 1922+ ne!)",
          "1925+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")
    check("I7e p80Houses-94-pin", "p80Houses.size !== 94" in qa, "")

    # ---------- I8: stale-sanacija p153–p187 ----------
    stale = []
    for y in range(153, 189):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1355", "BLOKI_04894 = 520",
                                          "1925")))
    check("I8a p153–p187 skripte VITALS_TOTAL 1219 + BLOKI 520 + guardi 1925",
          all(stale), f"{stale.count(True)}/36")

    # ---------- I9: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I9 notes: JEREB-#24-POTRJEN + CERAR-COMEBACK + NEMANJIČ + s239-meja",
          "JEREB" in n and "NEMANJIČ" in n and "COMEBACK" in n and "s239" in n, "")

    # ---------- I10: honesty + P188-lead ----------
    check("I10a honesty-nižja-zanesljivost", any("nižja-zanesljivost" in h for h in d["honesty"]), "")
    lp = d.get("leadP189", {})
    check("I10b P189-lead-1923", lp.get("year") == 1923 and "s239" in lp.get("meja", ""), "")

    # ---------- I11: LIVE (matricula) ----------
    if live:
        st, body = http_get(BOOK_URL)
        check("L1 matricula-04894-stran-200", st == 200, str(st))
        import base64 as _b64
        urls = []
        for mm in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', body.decode("utf-8", "replace")):
            seg = mm.group(1)[7:-1]
            try:
                dec = _b64.b64decode(seg + "=" * (-len(seg) % 4)).decode("utf-8")
                if dec.startswith("http"):
                    urls.append(dec)
            except Exception:
                pass
        urls = list(dict.fromkeys(urls))
        check("L2 inventar-256", len(urls) == 256, str(len(urls)))
        probes = []
        for scan_no in (231, 235, 239):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s231/s235/s239", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p188: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
