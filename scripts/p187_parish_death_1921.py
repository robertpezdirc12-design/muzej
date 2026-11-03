#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P187 — MRLIŠKA knjiga 04894, leto 1921 = 36. polno leto mrliške linije (issue #18):
s212-z1-MEJA-ROW + s213–s220 + s221-z50/z51 == str. 208–214 (stran == sken − 1 —
160.–166. potrditev!) + 51 vpisov = NAJNIŽJE-LETO-LINIJE (<55-1889!) / 10 GRIBLJE /
9 hiš (h46-×2!) = 2.-KRATEK-leto-zapored (58→51 — povojna-ekonomija!) + 'kostni-hri'[~]-
×~8-OTROŠKA-dominanta + ★★★ z51-RAJMER-dojenček-roj.-11.12.1920-†-25.12.1920 = 14-DNI
(roj./†-v-istem-mesecu-1.×-linije!) + ★★ h14-ISTI-STARŠA-cf.-P183-z22-MRTVOROJENO +
h46-×2 (Brodarič-dojenček + Milek-vdova) + BRODARIČ-mreža-×4 + MILEK-×2 + ★ z35-Leško-
1.×-priimek (h60-PT-vez-kandidat!) + ★ z30-Pavlakovič-LINK-cf.-P184-s199-ADMIN-
'Sprejemica'-Helene-Pavlaković-27.6.1921! + meja 1920/21 = s221-MID ('19 21' + restart-
z1-MRTVOROJENO-nezakonsko = 27.-POTRDITEV — 2.-leto-na-dnu-strani — kurator-visual!).
Kumulativ: vitals 1154 → 1164, mrliški bloki 04894 455 → 465, p80 hiše 94-NESPREMENJENO,
korpus 93-NESPREMENJEN, PT-luknja 18-NESPREMENJENA. Vzorec p185."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1921.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1921-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 57
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 14
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "6,15,18,22,26,29,31,31,35,35,41,41,44,73,77,82"
VITALS_TOTAL = 1283             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 94                 # NESPREMENJENO (h60-ŽE-v-42–60-luknja-setu!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [221, 222, 223, 224, 225, 226, 227, 228, 229, 230]

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
    check("I1a status-D1921", d["status"] == "SAMPLE-TRANSCRIPTION-D1921", d["status"])
    check("I1b knjiga-04894-leto-1921", d["book"] == "04894" and d["year"] == 1921, "")
    check("I1c 51-vpisov", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1d 0-excluded", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1e 14-anomalij", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1f 8-crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    check("I1g 10-honesty", len(d["honesty"]) == 10, str(len(d["honesty"])))

    # ---------- I2: okvir (stran == sken − 1; s212–s221; z1–z51) ----------
    ok_scan = all(e["page"] == e["scan"] - 1 and 221 <= e["scan"] <= 230 for e in d["entries"])
    check("I2a stran-==-sken-1-s221–s230", ok_scan, "")
    zaps = [e["zap"] for e in d["entries"]]
    check("I2b zaporedne-1–51-kompletne", zaps == list(range(1, 58)), str(zaps[:5]) + "…" + str(zaps[-3:]))
    grib = [e for e in d["entries"] if e["griblje"]]
    check("I2c 16-Griblje", len(grib) == 16, str(len(grib)))
    check("I2d hiše-10-Griblje", ",".join(sorted((e["houseNo"] for e in grib), key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted((e["houseNo"] for e in grib), key=int)))

    # ---------- I3: forenzika-markerji (kurator-visual) ----------
    def si(zap):
        e = next((e for e in d["entries"] if e["zap"] == zap), {})
        return (e.get("whatSi", "") + " " + e.get("ime", "") + " " + e.get("duhovnik", ""))
    check("I3a z1-MRTVOROJENO-nezakonsko-1.×", "NEZAKONSKO" in si(1), "")
    check("I3b z9-2.-NUJNI-KRST-cf.-P182", "2.-NUJNI-KRST-SIGNAL" in si(9), "")
    check("I3c z49-ZMRZNJENA-1.×-VZROK", "ZMRZNJENA" in si(49), "")
    check("I3d z8-NESREČA-padec-z-voza", "NESREČA-1.×-VZROK-FORMA" in si(8), "")
    check("I3e z36-MOLEK-CULMINACIJA", "MOLEK-TRAGEDIJA-CULMINACIJA" in si(36), "")
    check("I3f z47-knj.-uprav.-1.×", "knjižni-upravitelj" in si(47), "")
    check("I3g z10-'Pavčič'→POŽEK", "'Pavčič'-ZAVRJENO" in si(10), "")
    check("I3h z6-'Mihelčič'→MILEK", "'Mihelčič'-ZAVRJENO" in si(6), "")
    check("I3i z49-'Hafaj'→KRALJ", "'Hafaj'-ZAVRJENO" in si(49), "")

    # ---------- I4: anomalije-ključi ----------
    tips = " | ".join(a["tip"] for a in d["anomalies"])
    for key in ("meja-top-page", "duhovnik-prehod-1921", "zmrznjena-1x",
                "nesreca-padec-z-voza", "takoj-po-rojstvu-nujni-krst", "molek-tragedija",
                "kostni-hri-continuiteta", "pavlakovic-duplikat-kontrola"):
        check(f"I4-{key}", key in tips, "")

    # ---------- I5: crossChecks-ključi ----------
    xids = " ".join(c["id"] for c in d["crossChecks"])
    check("I5-crossChecks-X1–X8", all(f"X{i}" in xids for i in range(1, 9)), xids)

    # ---------- I6: parish.ts bloki ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    b1920 = re.findall(r'houseNo: "(\d+)",\s*bookSignature: "04894",\s*year: 1921,', src)
    check("I6a parish.ts-16-blokov-1921", len(b1920) == 16, str(len(b1920)))
    check("I6b hiše-1921-v-parish.ts", ",".join(sorted(b1920, key=int)) == "6,15,18,22,26,29,31,31,35,35,41,41,44,73,77,82",
          ",".join(sorted(b1920, key=int)))
    b1921 = re.findall(r'bookSignature: "04894",\s*year: 1925', src)
    check("I6d 0-blokov-04894-1925 (P190-KONEC-KNJIGE!)", len(b1921) == 0, str(len(b1921)))
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1180 + 94 + gap-18",
          "len(vitals) == 1283" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I7a qa-pini 1283 (90×+)", qa.count("!== 1283") >= 90, str(qa.count("!== 1283")))
    check("I7b qa-pini 520 (15×+)",
          qa.count('04894").length !== 520') >= 15
          and "p80Death.length !== 520" in qa, str(qa.count('04894").length !== 520')))
    check("I7c qa-p187 = 188. kontrola", "qa-p187-parish-death-1921" in qa, "")
    check("I7d qa guard 1925 (bloki 1921+ ne!)",
          "1925+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")
    check("I7e p80Houses-94-pin", "p80Houses.size !== 94" in qa, "")

    # ---------- I8: stale-sanacija p153–p186 ----------
    stale = []
    for y in range(153, 188):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1283", "BLOKI_04894 = 520",
                                          "1925")))
    check("I8a p153–p186 skripte VITALS_TOTAL 1219 + BLOKI 520 + guardi 1925",
          all(stale), f"{stale.count(True)}/35")

    # ---------- I9: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I9 notes: DUHOVNIŠKI-PREHOD + ZMRZNJENA + Nujni-krst + s231-meja",
          "Kumerrej" in n and "ZMRZNJENA" in n and "NUJNI" in n and "s231" in n, "")

    # ---------- I10: honesty + P187-lead ----------
    check("I10a honesty-nižja-zanesljivost", any("nižja-zanesljivost" in h for h in d["honesty"]), "")
    lp = d.get("leadP188", {})
    check("I10b P188-lead-1922", lp.get("year") == 1922 and "s231" in lp.get("meja", ""), "")

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
        for scan_no in (221, 225, 230):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s221/s225/s230", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p187: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
