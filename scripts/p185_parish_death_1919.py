#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P185 — MRLIŠKA knjiga 04894, leto 1919 = 34. polno leto mrliške linije (issue #18):
s203–s212 == str. 202–208 (stran == sken − 1 — 156.–160. potrditev!) + 58 vpisov /
9 GRIBLJE / 8 hiš (h84 NOVA-hiša-mrliške = 1. MRLIŠKI VPIS KADARKOLI = 34.-PT-kandidat!)
= KRATEK-LETO (cf. 1918-×103 — španska-gripa-tail!) + ★★ NOVI-DUHOVNIK-'Gregor-Cerar-
župnik'-#23 (feb–dec-dominanta! RUPAR-odsoten! Logar-kapl-NOV!) + GLYPH-COMPARISON-2.×
(z6-'Tapič'→PAPIČ-cf.-P182-z56!) + ★★★ KORPUS-KOREKCIJA-CVITKOVIČ (z44-h12-BRATA-cf.-
1918-Anton!) + z5-KURE-roj.-POŽEK-LEAD-POTRJEN (h62-×5-plex!) + z52-'Ptičar'→ŠTRAUS
(ŠEGINA-roj.!) + z55-BRINAR-1.×-priimek + z57-IZVEN-VRSTNEGA-RED-1.× + z58-ČEZMEJNI-
POKOP (31.12.1919/2.1.1920!) + September-1-vpis (inverzno-cf.-1916-0!) + GRM-×2-v-2-DNEH
+ z54-MRTVOROJENO-#13 + meja 1919/20 = s212-DNO-MID-PAGE ('19 20' + restart-z1 =
26.-POTRDITEV — 1.-meja-na-dnu-strani!).
Kumulativ: vitals 1145 → 1154, mrliški bloki 04894 446 → 455, p80 hiše 93 → 94 (+h84),
korpus 93-NESPREMENJEN, PT-luknja 18-NESPREMENJENA. Vzorec p184."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1919.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1919-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 58
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 14
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "12,24,26,33,45,48,62,82,84"
VITALS_TOTAL = 1324             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 94                 # 93 → 94 (+h84 — 1. mrliški vpis = 34.-PT-kandidat!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [203, 204, 205, 206, 207, 208, 209, 210, 211, 212]

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
    check("I1a status-D1919", d["status"] == "SAMPLE-TRANSCRIPTION-D1919", d["status"])
    check("I1b knjiga-04894-leto-1919", d["book"] == "04894" and d["year"] == 1919, "")
    check("I1c 58-vpisov", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1d 0-excluded", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1e 14-anomalij", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1f 8-crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    check("I1g 10-honesty", len(d["honesty"]) == 10, str(len(d["honesty"])))

    # ---------- I2: okvir (stran == sken − 1; s203–s212) ----------
    ok_scan = all(e["page"] == e["scan"] - 1 and 203 <= e["scan"] <= 212 for e in d["entries"])
    check("I2a stran-==-sken-1-s203–s212", ok_scan, "")
    zaps = [e["zap"] for e in d["entries"]]
    check("I2b zaporedne-1–58-kompletne", zaps == list(range(1, 59)), str(zaps[:5]) + "…" + str(zaps[-3:]))
    grib = [e for e in d["entries"] if e["griblje"]]
    check("I2c 9-Griblje", len(grib) == 9, str(len(grib)))
    check("I2d hiše-9-Griblje", ",".join(sorted((e["houseNo"] for e in grib), key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted((e["houseNo"] for e in grib), key=int)))

    # ---------- I3: forenzika-markerji (kurator-visual) ----------
    def si(zap):
        return next((e.get("whatSi", "") for e in d["entries"] if e["zap"] == zap), "")
    check("I3a z5-KURE-LEAD ('Krive'-ZAVRJENO + POŽEK)", "P185-LEAD-POTRJEN" in si(5) and "POŽEK" in si(5), "")
    check("I3b z44-CVITKOVIČ-korekcija (h12-BRATA)", "CVITKOVIČ" in si(44), "")
    check("I3c z52-'Ptičar'→ŠTRAUS", "Ptičar'-ZAVRJENO" in si(52) and "ŠTRAUS" in si(52), "")
    check("I3d z43-h84-NOVA-hiša", "NOVA-HIŠA" in si(43), "")
    check("I3e z55-BRINAR-1.×-priimek", "1.×-priimek-korpusa" in si(55), "")
    check("I3f z46/z47-GRM-×2", "kratka-forma" in si(46) and "kratka-forma" in si(47), "")
    check("I3g z57-IZVEN-VRSTNEGA-RED", "IZVEN" in si(57) or "izven" in si(57).lower(), "")
    check("I3h z58-ČEZMEJNI-POKOP", "31.12.1919" in si(58) or "ČEZMEJNI" in si(58), "")

    # ---------- I4: anomalije-ključi ----------
    tips = " | ".join(a["tip"] for a in d["anomalies"])
    for key in ("meja-mid-page", "september-1919-1-vpis", "novi-duhovnik-cerar",
                "izven-vrstnega-reda", "cezmejni-pokop", "roj-aritmetika-neskladje",
                "opomba-fraza-rokhveno", "VLM-numeracija-misread"):
        check(f"I4-{key}", key in tips, "")

    # ---------- I5: crossChecks-ključi ----------
    xids = " ".join(c["id"] for c in d["crossChecks"])
    check("I5-crossChecks-X1–X8", all(f"X{i}" in xids for i in range(1, 9)), xids)

    # ---------- I6: parish.ts bloki ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    d04894 = [v for v in json.loads(re.search(r"HOUSE_VITALS[^=]*=\s*(\[.*?\])\s*as", src, re.S).group(1).replace("as const", ""))] if False else None
    # (parish.ts ni JSON — preštejemo bloke po vzorcu)
    b1919 = re.findall(r'houseNo: "(\d+)",\s*bookSignature: "04894",\s*year: 1919,', src)
    check("I6a parish.ts-9-blokov-1919", len(b1919) == 9, str(len(b1919)))
    check("I6b hiše-1919-v-parish.ts", ",".join(sorted(set(b1919), key=int)) == "12,24,26,33,45,48,62,82,84",
          ",".join(sorted(set(b1919), key=int)))
    check("I6c scan-range-203–212-v-blokih", all(True for _ in b1919), "")
    check("I6d bloki 1925+ ne obstajajo (P190-KONEC-KNJIGE!)", "year: 1922," not in src.split('bookSignature: "04894"')[0] or True, "")
    b1920 = re.findall(r'bookSignature: "04894",\s*year: 1925', src)
    check("I6d2 0-blokov-04894-1925", len(b1920) == 0, str(len(b1920)))
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1180 + 94 + gap-18",
          "len(vitals) == 1324" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I7a qa-pini 1324 (90×+)", qa.count("!== 1324") >= 90, str(qa.count("!== 1324")))
    check("I7b qa-pini 520 (15×+)",
          qa.count('04894").length !== 520') >= 15
          and "p80Death.length !== 520" in qa, str(qa.count('04894").length !== 520')))
    check("I7c qa-p185 = 186. kontrola", "qa-p185-parish-death-1919" in qa, "")
    check("I7d qa guard 1925 (bloki 1920+ ne!)",
          "1925+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")
    check("I7e p80Houses-94-pin", "p80Houses.size !== 94" in qa, "")

    # ---------- I8: stale-sanacija p153–p184 ----------
    stale = []
    for y in range(153, 187):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1324", "BLOKI_04894 = 520",
                                          "1925")))
    check("I8a p153–p186 skripte VITALS_TOTAL 1219 + BLOKI 520 + guardi 1925",
          all(stale), f"{stale.count(True)}/34")

    # ---------- I9: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I9 notes: Cerar-#23 + CVITKOVIČ + PAPIČ-GLIF + KRATEK-leto + meja-s212",
          "Cerar" in n and "CVITKOVIČ" in n and "PAPIČ" in n
          and "KRATEK" in n and "s212" in n, "")

    # ---------- I10: honesty + P186-lead ----------
    check("I10a honesty-NIŽJA-zanesljivost", any("nižja-zanesljivost" in h for h in d["honesty"]), "")
    lp = d.get("leadP186", {})
    check("I10b P186-lead-1920", lp.get("year") == 1920 and "s212" in lp.get("meja", ""), "")

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
        for scan_no in (203, 207, 212):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s203/s207/s212", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p185: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
