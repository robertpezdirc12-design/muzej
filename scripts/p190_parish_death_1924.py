#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P190 — MRLIŠKA knjiga 04894, leto 1924 = 39. polno leto = ZADNJE-LETO-KNJIGE
(mrliška-linija-39/39-KONEC! issue #18): s248–s254 + s255-z45/z46 == str. 247–254
(stran == sken − 1 — 167.–202. potrditev!) + 46 vpisov / 14 GRIBLJE / 13 hiš
(h55-×2! + h50-NOVA-mrliška!) + ★★★ z10-Jožef-ŽELJKO-16-l-SUICID-OBESITEV-#3-
LINIJE ('duševna-slabost-(se-sam-obesil)'-cf.-1892 + 1908!) + ★★★ z25-'J.-
JAKOFČIČ-moškega-spola'-h6-MRTVOROJEN-#17-korpusa (PODPIS-PRAZEN-3.×-FORMA!) +
★★★ z5-Matija-PERDIRC-h50 = NOVA-HIŠA-MRLIŠKA (1.-vpis-kadarkoli = 35.-PT-
kandidat! h50-ŽE-v-p80!) + ★★★ z40-Martin-MUHAR-1.×-priimek-'delavec-samski'-
stan-1.×-FORMA (h55-×2!) + BRINEC-mreža-4.-leto (3-hiše-v-1-letu!) + OTT-kaplan-
DOMINANTA-~26 + JEREB-POVRAT-×3 + z45-'Boginja-vas'-korekcija + s253-zap-duplikat
'32' + s256-VEZ-halucinacija-ZAVRŽENA + KONEC-KNJIGE (z46-Marija-Jaklič-†-31.12.
1924 = ZADNJI-VPIS-KNJIGE-04894!). Kumulativ: vitals 1205 → 1219, mrliški bloki
04894 506 → 520 = KONEC-KNJIGE, p80 hiše 94-NESPREMENJENO, korpus 93-NESPREMENJEN,
PT-luknja 18-NESPREMENJENA. Vzorec p189."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1924.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1924-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 46
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 16
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "2,6,16,43,45,50,53,55,55,62,68,69,70,88"
VITALS_TOTAL = 1219             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 94                 # NESPREMENJENO
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [248, 249, 250, 251, 252, 253, 254, 255]

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
    check("I1a status-D1924", d["status"] == "SAMPLE-TRANSCRIPTION-D1924", d["status"])
    check("I1b knjiga-04894-leto-1924", d["book"] == "04894" and d["year"] == 1924, "")
    check("I1c 46-vpisov", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1d 0-excluded", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1e 16-anomalij", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1f 8-crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    check("I1g 11-honesty", len(d["honesty"]) == 11, str(len(d["honesty"])))

    # ---------- I2: okvir (stran == sken − 1; s248–s255; z1–z46) ----------
    ok_scan = all(e["page"] == e["scan"] - 1 and 248 <= e["scan"] <= 255 for e in d["entries"])
    check("I2a stran-==-sken-1-s248–s255", ok_scan, "")
    zaps = [e["zap"] for e in d["entries"]]
    check("I2b zaporedne-1–46-kompletne", zaps == list(range(1, 47)), str(zaps[:5]) + "…" + str(zaps[-3:]))
    grib = [e for e in d["entries"] if e["griblje"]]
    check("I2c 14-Griblje", len(grib) == 14, str(len(grib)))
    check("I2d hiše-14-Griblje", ",".join(sorted((e["houseNo"] for e in grib), key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted((e["houseNo"] for e in grib), key=int)))

    # ---------- I3: forenzika-markerji (kurator-visual) ----------
    def si(zap):
        e = next((e for e in d["entries"] if e["zap"] == zap), {})
        return (e.get("whatSi", "") + " " + e.get("ime", "") + " " + e.get("duhovnik", ""))
    check("I3a z5-h50-NOVA-mrliška-PERDIRC", "NOVA-HIŠA-MRLIŠKA" in si(5) and "PERDIRC" in si(5), "")
    check("I3b z10-SUICID-OBESITEV-#3", "SUICID-OBESITEV-#3-LINIJE" in si(10) and "ŽELJKO" in si(10), "")
    check("I3c z14-LASIČ-83-let", "NAJSTAREJŠI-1924" in si(14), "")
    check("I3d z25-MRTVOROJEN-#17-PODPIS-PRAZEN", "#17-korpusa" in si(25) and "PODPIS-PRAZEN" in si(25), "")
    check("I3e z23-'Galkovič'→JAKOFČIČ", "'Galkovič'-ZAVRŽEN" in si(23), "")
    check("I3f z29-DRAGOS-samska-delavka", "DRAGOS" in si(29) and "samska-delavka" in si(29), "")
    check("I3g z32-BRINEC-5.-leto-3-hiše", "BRINEC-mreža-5.-leto" in si(32), "")
    check("I3h z40-MUHAR-1.×-priimek", "1.×-priimek-korpusa-kandidat" in si(40) and "delavec" in si(40).lower(), "")
    check("I3i z42-BRINEC-h2-ZADNJA", "ZADNJA-1924-GRIBLJE-VRSTA" in si(42), "")

    # ---------- I4: anomalije-ključi ----------
    tips = " | ".join(a["tip"] for a in d["anomalies"])
    for key in ("suicid-obesitev-3-linije", "mrtvorojen-17-korpusa", "h50-nova-mrliška-1x",
                "h55-x2-v-1-letu", "muhar-1x-priimek", "brinec-mreza-5-leto",
                "duhovnik-jereb-povrat", "ott-kaplan-dominanta", "s253-zap-duplikat",
                "s256-vez-halucinacija", "zadnji-vpis-knjige", "z45-boginja-vas-korekcija"):
        check(f"I4-{key}", key in tips, "")

    # ---------- I5: crossChecks-ključi ----------
    xids = " ".join(c["id"] for c in d["crossChecks"])
    check("I5-crossChecks-X1–X8", all(f"X{i}" in xids for i in range(1, 9)), xids)

    # ---------- I6: parish.ts bloki ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    b1924 = re.findall(r'houseNo: "(\d+)",\s*bookSignature: "04894",\s*year: 1924,', src)
    check("I6a parish.ts-14-blokov-1924", len(b1924) == 14, str(len(b1924)))
    check("I6b hiše-1924-v-parish.ts", ",".join(sorted(b1924, key=int)) == "2,6,16,43,45,50,53,55,55,62,68,69,70,88",
          ",".join(sorted(b1924, key=int)))
    b1925 = re.findall(r'bookSignature: "04894",\s*year: 1925', src)
    check("I6d 0-blokov-04894-1925 (KNJIGA-KONČANA!)", len(b1925) == 0, str(len(b1925)))
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1219 + 94 + gap-18",
          "len(vitals) == 1219" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I7a qa-pini 1219 (90×+)", qa.count("!== 1219") >= 90, str(qa.count("!== 1219")))
    check("I7b qa-pini 520 (15×+)",
          qa.count('04894").length !== 520') >= 15
          and "p80Death.length !== 520" in qa, str(qa.count('04894").length !== 520')))
    check("I7c qa-p191 = 191. kontrola", "qa-p191-parish-death-1924" in qa, "")
    check("I7d qa guard 1925 (KNJIGA-KONČANA!)",
          "1925+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")
    check("I7e p80Houses-94-pin", "p80Houses.size !== 94" in qa, "")

    # ---------- I8: stale-sanacija p153–p189 ----------
    stale = []
    for y in range(153, 190):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1219", "BLOKI_04894 = 520",
                                          "1925")))
    check("I8a p153–p189 skripte VITALS_TOTAL 1219 + BLOKI 520 + guardi 1925",
          all(stale), f"{stale.count(True)}/37")

    # ---------- I9: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I9 notes: SUICID-OBESITEV + h50-NOVA + KONEC-KNJIGE + s256-vez",
          "SUICID" in n and "h50" in n and "KONEC" in n and "s256" in n, "")

    # ---------- I10: honesty + leadP190_end ----------
    check("I10a honesty-nižja-zanesljivost", any("nižja-zanesljivost" in h for h in d["honesty"]), "")
    lp = d.get("leadP190_end", {})
    check("I10b linija-39/39-KONEC", "39/39" in lp.get("line", ""), lp.get("line", ""))

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
        for scan_no in (248, 252, 255, 256):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s248/s252/s255/s256", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p190: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
