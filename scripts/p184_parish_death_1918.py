#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P184 — MRLIŠKA knjiga 04894, leto 1918 = 33. polno leto mrliške linije (issue #18):
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
Vzorec p183."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1918.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1918-lead.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 103
EXPECTED_EXCLUDED = 3
EXPECTED_ANOMALIES = 16
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "2,6,6,10,12,16,19,22,22,22,26,27,27,30,35,37,46,49,53,53,53,58,58,62,74,88,92"
VITALS_TOTAL = 1347             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 93                 # NESPREMENJENO (vseh-8-hiš-ŽE-v-filtru!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,201,202]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1918", d["status"])
    check("I1b 103 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 4 excluded / 15 anomalij / 8 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    grib_e = [e for e in ent if e["griblje"]]
    check("I2 1918 = 102 veljavnih + 1-storno / 27-Griblje-REKORD (frame!)",
          fr["validRows"] == 102 and fr["rowsTotal"] == 103 and fr["stornoRows"] == 1
          and fr["unnumberedRows"] == 0 and len(grib_e) == 27,
          f"{fr['validRows']}/{fr['rowsTotal']}/{len(grib_e)}")
    check("I2b okvir skeni 184–202 (s199/s200-INSERTI-izpuščeni!)",
          fr["scans"] == NEW_SCANS, f"{fr['scans']}")
    hise_clean = sorted({e["houseNo"] for e in grib_e}, key=int)
    check("I2c hiše = [2,6,10,12,16,19,22,26,27,30,35,37,46,49,53,58,62,74,88,92]",
          ",".join(hise_clean) == "2,6,10,12,16,19,22,26,27,30,35,37,46,49,53,58,62,74,88,92", ",".join(hise_clean))

    # ---------- I3: P184-forme ----------
    e34 = next(e for e in ent if e["zap"] == 34)
    check("I3a STORNO-#2-z34 (datumi-popravljeni-nato-prečrtani!)",
          "STORNO" in (e34.get("whatSi") or "") or e34["danSmrti"].startswith("9. [prečrtano"), "")
    spanka = sum(1 for e in ent if "špan" in (e["vzrok"] or "").lower())
    check("I3b ŠPANSKA-GRIPA-×~40 (val-okt–dec!)",
          spanka >= 35, str(spanka))
    check("I3c 'Španska-bolezen'-FULL-FORM-1.×!",
          any("ŠPANSKA BOLEZEN" in (e["vzrok"] or "") for e in ent), "")
    check("I3d s199-ADMIN-'Spremnica'-'starem-pokopališču'-RAZREŠITEV!",
          "s199-ADMIN" in (d["frame"]["skeni"]) and any("starem-pokopališču" in a["opis"] for a in d["anomalies"]), "")
    e50 = next(e for e in ent if e["zap"] == 50)
    check("I3e RUPAR-kapl.-nov-duhovnik-#22 (z50-1.-podpis!)",
          "Rupar" in e50["duhovnik"], e50["duhovnik"][:50])

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 71 — 139.–149. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 162–172",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: P184-lead-korekcije ----------
    e13 = next(e for e in ent if e["zap"] == 13)
    check("I5a LEAD-z13: 'Griblje-h21-Mlivc'→Žemelj-MUC (EXCLUDED!)",
          e13["griblje"] is False and "Žemelj" in e13["vas"], e13["vas"])
    e36 = next(e for e in ent if e["zap"] == 36)
    check("I5b LEAD-z36: 'Tuše'→KURE (korpus-h62!)",
          "Kure" in e36["ime"] and e36["houseNo"] == "62", e36["ime"])
    e65 = next(e for e in ent if e["zap"] == 65)
    check("I5c LEAD-z65: 'Elna-Vegina'→ŠEGINA!",
          "Šegina" in e65["ime"] and e65["houseNo"] == "30", "")
    e75 = next(e for e in ent if e["zap"] == 75)
    check("I5d LEAD-z75: 'vdova'→ZAKONSKI-OTROK (h88!)",
          "OTROK" in e75["stan"].upper() and e75["houseNo"] == "88", e75["stan"][:50])
    e94 = next(e for e in ent if e["zap"] == 94)
    e96 = next(e for e in ent if e["zap"] == 96)
    check("I5e LEAD-z94/z96: 'Tožek/Toček'→POŽEK-×2!",
          "Požek" in e94["ime"] and "Požek" in e96["ime"], "")
    e6 = next(e for e in ent if e["zap"] == 6)
    check("I5f P184-LEAD-potrjen: z6-h49-Štravs-Barbara-82!",
          e6["vas"] == "Griblje" and e6["houseNo"] == "49" and "Štravs" in e6["ime"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1100", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 401", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1918 = [v for v in d04894 if v["year"] == 1918]
    check("I6c bloki 1918 = 27 (Griblje-REKORD-LINIJE!)",
          len(d1918) == 27 and all(v["houseNo"] in {"2", "6", "10", "12", "16", "19", "22", "26", "27", "30", "35", "37", "46", "49", "53", "58", "62", "74", "88", "92"}
                                   for v in d1918), str(len(d1918)))
    check("I6d bloki 1925+ ne obstajajo (P190-KONEC-KNJIGE!)",
          all(v["year"] < 1925 for v in d04894), "")
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1118 + 93 + gap-18 (vitals-P183-kaskada!)",
          "len(vitals) == 1347" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: DVOJNI-TRAGEDIJI + POŽEK + begunci ----------
    e71 = next(e for e in ent if e["zap"] == 71)
    e79 = next(e for e in ent if e["zap"] == 79)
    check("I7a h6-×2-BRATA-ISTA-STARŠI-v-3-DNEH (#10!)",
          e71["houseNo"] == "6" and e79["houseNo"] == "6"
          and "Jakof" in e71["ime"] and "Jakob" in e79["ime"], "")
    e82 = next(e for e in ent if e["zap"] == 82)
    e96 = next(e for e in ent if e["zap"] == 96)
    check("I7b h58-×2-MATER+HČER-v-13-DNEH (#11! POŽEK/KAMBIČ)",
          e82["houseNo"] == "58" and e96["houseNo"] == "58"
          and "KAMBI" in e82["stan"].upper() and "KAMBI" in e96["ime"].upper(), "")
    pozek = sum(1 for e in ent if e["griblje"] and "Požek" in (e["ime"] or ""))
    check("I7c POŽEK-družina-×5-1918 (z80/z82/z85/z91/z94/z96!)",
          pozek >= 5, str(pozek))
    begunci = sum(1 for e in ent if "begun" in (e["stan"] or "").lower())
    check("I7d BEGUNCI-×11-1918-MASOVNI (WWI-val!)",
          begunci >= 6, str(begunci))

    # ---------- I8: meja-1916/17 + glave ----------
    check("I8 meja-1918/19 = s203-'Anno-1919'-restart (25.-POTRDITEV!)",
          "s203" in fr["meja1918_19"] and "25.-POTRDITEV" in fr["meja1918_19"],
          fr["meja1918_19"][:60])
    check("I8b s199/s200-INSERTI-paginacijska-anomalija-A12!",
          any("paginacija" in a["tip"] for a in d["anomalies"]), "")

    # ---------- I9: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I9a qa-pini 1347 (90×+)", qa.count("!== 1347") >= 90, str(qa.count("!== 1347")))
    check("I9b qa-pini 401 (15×+)",
          qa.count('04894").length !== 520') >= 15
          and "p80Death.length !== 520" in qa, str(qa.count('04894").length !== 520')))
    check("I9c qa-p184 = 185. kontrola", "qa-p184-parish-death-1918" in qa, "")
    check("I9d qa guard 1919 (bloki 1919+ ne!)",
          "1925+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1925" in qa, "")

    # ---------- I10: stale-sanacija p153–p181 ----------
    stale = []
    for y in range(153, 187):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1347", "BLOKI_04894 = 520",
                                          "1925")))
    check("I10a p153–p184 skripte VITALS_TOTAL 1219 + BLOKI 520 + guardi 1925",
          all(stale), f"{stale.count(True)}/34")

    # ---------- I11: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I11 notes: ŠPANSKA-GRIPA + RUPAR + starem-pokopališču + REKORD",
          "ŠPANSKA-GRIPA" in n and "RUPAR" in n
          and "starem-pokopališču" in n and "REKORD" in n, "")

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
        for scan_no in (184, 192, 202):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s184/s192/s202", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p184: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
