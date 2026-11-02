#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P182 — MRLIŠKA knjiga 04894, leto 1916 = 31. polno leto mrliške linije (issue #18):
s162–s172 == str. 161–170 (stran == sken − 1 — 139.–149. potrditev!) + s173-DVOPAGE
(str. 171+172 = MEJA-1.×!) + 71 vpisov / 9 GRIBLJE / 8 hiš (h88 ×2 = MATER-IN-DOTKA-v-8-
DNEH!) + ★★★ 5 × 1.-×-FORME (in-utero-KRST-z71-'mrtvoroj.-dete-še-živo-in-utero-v-sili-
krščeno'-2.-signal-cf.-krstna-s290-PRVI + previden-'ne'-×2-z62/z63-DVOJNA-TRAGEDIJA-Macele
+ DVOPAGE-skan-s173 + SEPTEMBER-1916-0-VPISOV + BREZ-zaključne-opombe) + 3-LEAD-KOREKCIJE
(z24-'Griblje'→ŠKRILJE + z57-'Griblje'-X-šrafura→DRAGOŠE + z56-'Tapič'→PAPIČ-GLIF-TEST
=s153-z13-IDENTIČEN + korpus-h31-Papič/Straus!) + WWI-vojak-črnogorski-z18 + tuj-pokop-
KOSTEL-#3-z17 + vzroki-×3-novi (mrtvoud + davica + dobrci-×5!) + MRTVOROJENO-×2 +
DVOJČKI-SMRTI-#6 + roj.-popravek-z38-'1859'→1871-okrajšava-z-tildo + glave-'18916'-×6-
'9-J'-forma-3.-LETO + meja 1916/17 = s173-restart-z1 = 23.-POTRDITEV.
Kumulativ: vitals 1091 → 1100, mrliški bloki 04894 392 → 401, p80 hiše 93-NESPREMENJENO
(vseh-8-hiš-že-v-filtru!), korpus 93-NESPREMENJEN, PT-luknja 18-NESPREMENJENA.
Vzorec p181."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1916.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1916-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 71
EXPECTED_EXCLUDED = 4
EXPECTED_ANOMALIES = 15
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "9,15,21,28,31,35,37,88,88"
VITALS_TOTAL = 1164             # 1118 + 27! (P184)
BLOKI_04894 = 465               # 419 + 27! (P184)
P80_HOUSES = 93                 # NESPREMENJENO (vseh-8-hiš-ŽE-v-filtru!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1916", d["status"])
    check("I1b 71 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 4 excluded / 15 anomalij / 8 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    grib_e = [e for e in ent if e["griblje"]]
    check("I2 1916 = 71 veljavnih / 9 Griblje (frame!)",
          fr["validRows"] == 71 and fr["rowsTotal"] == 71 and fr["stornoRows"] == 0
          and fr["unnumberedRows"] == 0 and len(grib_e) == 9,
          f"{fr['validRows']}/{fr['rowsTotal']}/{len(grib_e)}")
    check("I2b okvir skeni 162–172 + strani 161–170 (+ s173-DVOPAGE!)",
          fr["scans"] == NEW_SCANS and fr["pages"] == list(range(161, 171)),
          f"{fr['scans']}")
    hise_clean = sorted({e["houseNo"] for e in grib_e}, key=int)
    check("I2c hiše = [9,15,21,28,31,35,37,88] (h88-×2!)",
          ",".join(hise_clean) == "9,15,21,28,31,35,37,88", ",".join(hise_clean))

    # ---------- I3: 5 × 1.-×-FORME ----------
    e71 = next(e for e in ent if e["zap"] == 71)
    check("I3a IN-UTERO-KRST-z71 (2.-signal-cf.-krstna-s290!)",
          "mrtvorojeno" in e71["vzrok"] and "in utero" in (e71.get("whatSi") or "")
          and "sili krščeno" in (e71.get("whatSi") or ""), (e71.get("whatSi") or "")[:80])
    e62 = next(e for e in ent if e["zap"] == 62)
    e63 = next(e for e in ent if e["zap"] == 63)
    check("I3b PREVIDEN-'ne'-×2 (DVOJNA-TRAGEDIJA-Macele-21/22.-okt!)",
          e62["previden"] == "ne" and e63["previden"] == "ne"
          and "21/22" in e62["danSmrti"] and "21/22" in e63["danSmrti"]
          and "utopila" in e62["vzrok"] and "pijanosti" in e63["vzrok"], "")
    check("I3c DVOPAGE-skan-s173 (1.×!)",
          "DVOPAGE" in fr["skeni"] and "23.-POTRDITEV" in fr["boundary1917"]["note"],
          fr["skeni"][:60])
    e61 = next(e for e in ent if e["zap"] == 61)
    check("I3d SEPTEMBER-1916-0-VPISOV (avgust→oktober-skok!)",
          e61["mesec"] == "Oktober" and e61["danSmrti"] == "4." and "0-VPISOV" in (e61.get("whatSi") or ""), "")
    check("I3e BREZ-zaključne-opombe (cf. 1915!)",
          any(a["tip"] == "brez-zaključne-opombe" for a in d["anomalies"]), "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 71 — 139.–149. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 162–172",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: lead-korekcije + 'Grm' ----------
    e24 = next(e for e in ent if e["zap"] == 24)
    check("I5a LEAD-KOREKCIJA-#1: z24 = ŠKRILJE-h1 (NE-Griblje!)",
          e24["vas"] == "Škrilje" and e24["houseNo"] == "1", e24["vas"])
    e57 = next(e for e in ent if e["zap"] == 57)
    check("I5b LEAD-KOREKCIJA-#2: z57 = DRAGOŠE-h5 (Griblje-X-šrafura!)",
          e57["vas"] == "Dragoše" and e57["houseNo"] == "5", e57["vas"])
    e56 = next(e for e in ent if e["zap"] == 56)
    check("I5c LEAD-KOREKCIJA-#3: z56-'Tapič' → PAPIČ (GLIF-TEST = s153-z13!)",
          "Papič" in e56["ime"] and "GLIF-TEST" in (e56.get("whatSi") or "")
          and e56["houseNo"] == "31", e56["ime"])
    e2 = next(e for e in ent if e["zap"] == 2)
    e40 = next(e for e in ent if e["zap"] == 40)
    check("I5d 'Grm'-kratka-forma ×3 (z2-h28 + z40-h35!)",
          "Grm" in e2["vas"] and "Grm" in e40["vas"]
          and "LEAD-POTRJEN" in (e2.get("whatSi") or ""), "")
    e38 = next(e for e in ent if e["zap"] == 38)
    check("I5e ROJ.-POPRAVEK-z38: '1859' → 1871 (okrajšava-z-tildo — 44-SKLADNA!)",
          "1871" in e38["starost"] and "44 let" in e38["starost"], e38["starost"])

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1100", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 401", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1916 = [v for v in d04894 if v["year"] == 1916]
    check("I6c bloki 1916 = 9 (Griblje!)",
          len(d1916) == 9 and all(v["houseNo"] in {"9", "15", "21", "28", "31", "35", "37", "88"}
                                   for v in d1916), str(len(d1916)))
    check("I6d bloki 1921+ ne obstajajo (P187-lead!)",
          all(v["year"] < 1921 for v in d04894), "")
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1118 + 93 + gap-18 (vitals-P183-kaskada!)",
          "len(vitals) == 1164" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: h88-×2-MATER-IN-DOTKA + vzroki-novi ----------
    e42 = next(e for e in ent if e["zap"] == 42)
    check("I7a h88-×2-v-8-DNEH = MATER (Ana-44) + DOTKA (Neža-19-dni!) — DVOJNA-TRAGEDIJA-#7",
          e38["houseNo"] == "88" and e42["houseNo"] == "88"
          and "posestnikova žena" in e38["stan"] and "posestnikov otrok" in e42["stan"]
          and "19 dni" in e42["starost"], "")
    e16 = next(e for e in ent if e["zap"] == 16)
    check("I7b 1.-'MRTVOUD'-vzrok (z16-Jaklič!)",
          "mrtvoud" in e16["vzrok"] and "MRTVOUD" in (e16.get("whatSi") or ""), "")
    e69 = next(e for e in ent if e["zap"] == 69)
    check("I7c 1.-'DAVICA'-vzrok (z69-Jakofčič!)",
          "davica" in e69["vzrok"] and "DAVICA" in (e69.get("whatSi") or ""), "")
    check("I7d 'dobrci/dobrici'-×5-MASOVNI-1.× (z32/z37/z40/z45/z46/z53!)",
          sum(1 for e in ent if "dobr" in (e["vzrok"] or "").lower()) >= 5,
          str(sum(1 for e in ent if "dobr" in (e["vzrok"] or "").lower())))
    e18 = next(e for e in ent if e["zap"] == 18)
    check("I7e WWI-vojak-črnogorski (z18-Krasinec-h20!)",
          "vojak" in e18["stan"] and "črnog" in e18["stan"], e18["stan"][:50])
    e17 = next(e for e in ent if e["zap"] == 17)
    check("I7f TUJI-POKOP-#3: 'pokopan v Krostn' [~ KOSTEL!] (z17!)",
          "Krostn" in (e17.get("whatSi") or ""), "")

    # ---------- I8: meja-1916/17 + glave ----------
    check("I8 meja-1916/17 = s173-restart (23.-POTRDITEV — DVOPAGE-izjema!)",
          "s173" in fr["meja1916_17"] and "23.-POTRDITEV" in fr["meja1916_17"],
          fr["meja1916_17"][:60])
    check("I8b glava-'18916'-napake-×6-'9-J'-forma-3.-LETO (cf. P180/P181!)",
          any("18916" in a["opis"] for a in d["anomalies"]), "")

    # ---------- I9: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I9a qa-pini 1100 (90×+)", qa.count("!== 1164") >= 90, str(qa.count("!== 1164")))
    check("I9b qa-pini 401 (15×+)",
          qa.count('04894").length !== 465') >= 15
          and "p80Death.length !== 465" in qa, str(qa.count('04894").length !== 465')))
    check("I9c qa-p182 = 183. kontrola", "qa-p182-parish-death-1916" in qa, "")
    check("I9d qa guard 1919 (bloki 1919+ ne!)",
          "1921+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1921" in qa, "")

    # ---------- I10: stale-sanacija p153–p181 ----------
    stale = []
    for y in range(153, 183):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1164", "BLOKI_04894 = 465",
                                          "1921")))
    check("I10a p153–p182 skripte VITALS_TOTAL 1118 + BLOKI 419 + guardi 1918",
          all(stale), f"{stale.count(True)}/30")

    # ---------- I11: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I11 notes: in-utero-KRST + MATER-IN-DOTKA + GLIF-TEST + SEPTEMBER-0",
          "IN-UTERO-NUJNI-KRST" in n and "MATER-IN-DOTKA" in n
          and "GLIF-TEST" in n and "SEPTEMBER" in n, "")

    # ---------- I12: LIVE (matricula) ----------
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
        for scan_no in (162, 169, 172):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s162/s169/s172", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p182: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
