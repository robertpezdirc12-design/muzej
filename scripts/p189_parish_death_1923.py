#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P189 — MRLIŠKA knjiga 04894, leto 1923 = 38. polno leto mrliške linije (issue #18):
s239-bot (z1–z4) + s240–s246 + s247-z53–z58 == str. 238–246 (stran == sken − 1 —
167.–194. potrditev!) + 58 vpisov / 11 GRIBLJE / 10 hiš (h17-×2!) + ★★★ DUHOVNIKI-
×3-v-1-LETU: Remigi-JEREB-žup.-dominanta-~44-2.-leto (garble-×7-VSI-ZAVRŽENI!) +
★★ Matija-TOMC-'et-deleg.'-×2 = NOVI-DUHOVNIK-#26-kandidat ('et-delegatus'-1.×!)
+ ★★ Jožef-OTT[~Rott]-'kaplan'-×~7 = NOVI-DUHOVNIK-#27-kandidat (KAPLAN-1.×-od-
P186-Logar!) = 2-NOVA-DUHOVNIKA-v-1-LETU! + ★★★ z36+z37-PLUT-DVOJČKI-SMRTI
(Klošter-h41-roj.-26.6.1923-ISTI-DAN-'1-dan' = 2.×-linije-cf.-1890-h30!) + ★★★
KOSTNI-KRI/HRK-×8-CONTINUITETA-5.-LETO (vse-ne-Griblje!) + ★★★ z21-BRINEC-h14-
3.-LETO-ZAPORED ('Srenc-Kap.'-SRČNA-KAP-1.×-VZROK-FORMA-22-let-tragedija!) +
★★★ HVALA/HRAJ-1.×-priimek-korpusa-×2-v-1-LETU (z8-Ivan + z51-Ana-h17-×2-isti-
glif-forenzika!) + ŽELJKO-h60-×2 + PLUT-h25-×2-ZAPORED (posestniška-PAR-†!) +
z30-ŽELEZNIČAR-stan-1.× + z58-'vžitharica'-1.× + z57-HLEBEC-h2-cf.-P163! +
z2-'Črnomelj'→Vranoviče + z32-TRIPLE-korekcija (Griblje→Ceroviše-Marjeta-
GRUBRIJAN!) + MEJA 1923/24 = s247-END (restart-z1-Jan-1924 = 30.-POTRDITEV!) +
s248-1924-START = ZADNJE-LETO-KNJIGE (256-skenov-do-1924 → linija-39/39!).
Kumulativ: vitals 1194 → 1205, mrliški bloki 04894 495 → 506, p80 hiše 94-
NESPREMENJENO, korpus 93-NESPREMENJEN, PT-luknja 18-NESPREMENJENA. Vzorec p188."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1923.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1923-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 58
EXPECTED_EXCLUDED = 0
EXPECTED_ANOMALIES = 16
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "2,13,14,17,17,25,44,60,64,71,78"
VITALS_TOTAL = 1283             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 94                 # NESPREMENJENO
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [239, 240, 241, 242, 243, 244, 245, 246, 247]

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
    check("I1a status-D1923", d["status"] == "SAMPLE-TRANSCRIPTION-D1923", d["status"])
    check("I1b knjiga-04894-leto-1923", d["book"] == "04894" and d["year"] == 1923, "")
    check("I1c 58-vpisov", len(d["entries"]) == EXPECTED_ENTRIES, str(len(d["entries"])))
    check("I1d 0-excluded", len(d.get("excluded", [])) == EXPECTED_EXCLUDED, str(len(d.get("excluded", []))))
    check("I1e 16-anomalij", len(d["anomalies"]) == EXPECTED_ANOMALIES, str(len(d["anomalies"])))
    check("I1f 8-crossChecks", len(d["crossChecks"]) == EXPECTED_CROSSCHECKS, str(len(d["crossChecks"])))
    check("I1g 11-honesty", len(d["honesty"]) == 11, str(len(d["honesty"])))

    # ---------- I2: okvir (stran == sken − 1; s239–s247; z1–z58) ----------
    ok_scan = all(e["page"] == e["scan"] - 1 and 239 <= e["scan"] <= 247 for e in d["entries"])
    check("I2a stran-==-sken-1-s239–s247", ok_scan, "")
    zaps = [e["zap"] for e in d["entries"]]
    check("I2b zaporedne-1–58-kompletne", zaps == list(range(1, 59)), str(zaps[:5]) + "…" + str(zaps[-3:]))
    grib = [e for e in d["entries"] if e["griblje"]]
    check("I2c 11-Griblje", len(grib) == 11, str(len(grib)))
    check("I2d hiše-11-Griblje", ",".join(sorted((e["houseNo"] for e in grib), key=int)) == GRIBLJE_HOUSES,
          ",".join(sorted((e["houseNo"] for e in grib), key=int)))

    # ---------- I3: forenzika-markerji (kurator-visual) ----------
    def si(zap):
        e = next((e for e in d["entries"] if e["zap"] == zap), {})
        return (e.get("whatSi", "") + " " + e.get("ime", "") + " " + e.get("duhovnik", ""))
    check("I3a z1-ANNE-posestniški-otrok-h64", "ANNE" in si(1) and "Pivac" in si(1), "")
    check("I3b z8-HRAJ-1.×-priimek", "1.×-priimek-korpusa-kandidat" in si(8), "")
    check("I3c z9-'Traponščak'→DRAGOS", "'Traponščak'-ZAVRŽEN" in si(9), "")
    check("I3d z12-ŽELJKO-×2-ZAPORED", "ŽELJKO-h60-×2-ZAPORED" in si(12), "")
    check("I3e z13-'Jakopič'→JAKOFČIČ", "'Jakopič'-ZAVRŽEN" in si(13), "")
    check("I3f z21-SRČNA-KAP-1.×-BRINEC-h14", "SRČNA-KAP-1.×-VZROK-FORMA" in si(21) and "BRINEC-h14-3.-LETO-ZAPORED" in si(21), "")
    check("I3g z31-PLUT-h25-×2-ZAPORED", "PLUT-h25-×2-ZAPORED" in si(31), "")
    check("I3h z51-HRAJ-×2-h17-POPOLNO", "HVALA/HRAJ-×2-v-1-LETU" in si(51), "")
    check("I3i z57-HLEBEC-h2-ZADNJA", "HLEBEC-h2" in si(57) and "ZADNJA-1923-GRIBLJE" in si(57), "")

    # ---------- I4: anomalije-ključi ----------
    tips = " | ".join(a["tip"] for a in d["anomalies"])
    for key in ("plut-dvojcki-smrti", "kostni-kri-continuiteta-5-leto", "brinec-h14-3-leto-zapored",
                "srcna-kap-1x", "duhovniki-3-novi-2", "zeleznicar-stan-1x",
                "vzitharica-1x", "hvala-hraj-1x-x2", "z32-triple-korekcija",
                "meja-s247-end-30", "glava-s248-1924"):
        check(f"I4-{key}", key in tips, "")

    # ---------- I5: crossChecks-ključi ----------
    xids = " ".join(c["id"] for c in d["crossChecks"])
    check("I5-crossChecks-X1–X8", all(f"X{i}" in xids for i in range(1, 9)), xids)

    # ---------- I6: parish.ts bloki ----------
    src = open(PARISH_TS, encoding="utf-8").read()
    b1923 = re.findall(r'houseNo: "(\d+)",\s*bookSignature: "04894",\s*year: 1923,', src)
    check("I6a parish.ts-11-blokov-1923", len(b1923) == 11, str(len(b1923)))
    check("I6b hiše-1923-v-parish.ts", ",".join(sorted(b1923, key=int)) == "2,13,14,17,17,25,44,60,64,71,78",
          ",".join(sorted(b1923, key=int)))
    b1924 = re.findall(r'bookSignature: "04894",\s*year: 1925', src)
    check("I6d 0-blokov-04894-1925 (P190-KONEC-KNJIGE!)", len(b1924) == 0, str(len(b1924)))
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1205 + 94 + gap-18",
          "len(vitals) == 1283" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I7a qa-pini 1283 (90×+)", qa.count("!== 1283") >= 90, str(qa.count("!== 1283")))
    check("I7b qa-pini 520 (15×+)",
          qa.count('04894").length !== 520') >= 15
          and "p80Death.length !== 520" in qa, str(qa.count('04894").length !== 520')))
    check("I7c qa-p189 = 190. kontrola", "qa-p189-parish-death-1923" in qa, "")
    check("I7d qa guard 1925 (bloki 1923+ ne!)",
          "1925+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")
    check("I7e p80Houses-94-pin", "p80Houses.size !== 94" in qa, "")

    # ---------- I8: stale-sanacija p153–p188 ----------
    stale = []
    for y in range(153, 190):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1283", "BLOKI_04894 = 520",
                                          "1925")))
    check("I8a p153–p188 skripte VITALS_TOTAL 1219 + BLOKI 520 + guardi 1925",
          all(stale), f"{stale.count(True)}/37")

    # ---------- I9: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I9 notes: TOMC-et-deleg + OTT-kaplan + PLUT-dvojčki + s247-meja",
          "TOMC" in n and "OTT" in n and "DVOJČKI" in n and "s247" in n, "")

    # ---------- I10: honesty + P189-lead ----------
    check("I10a honesty-nižja-zanesljivost", any("nižja-zanesljivost" in h for h in d["honesty"]), "")
    lp = d.get("leadP190", {})
    check("I10b P190-lead-1924", lp.get("year") == 1924 and "s247" in lp.get("meja", ""), "")

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
        for scan_no in (239, 243, 247):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s239/s243/s247", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p189: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
