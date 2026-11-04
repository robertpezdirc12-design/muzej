#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P183 — MRLIŠKA knjiga 04894, leto 1917 = 32. polno leto mrliške linije (issue #18):
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
Vzorec p182."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1917.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1917-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 72
EXPECTED_EXCLUDED = 1
EXPECTED_ANOMALIES = 17
EXPECTED_CROSSCHECKS = 8
GRIBLJE_HOUSES = "2,3,3,5,9,14,20,21,26,28,34,36,41,53,54,62,77,78"
VITALS_TOTAL = 1355             # 1205 + 14! (P190 = KONEC-KNJIGE!)
BLOKI_04894 = 520               # 506 + 14! (P190 = KONEC-KNJIGE!)
P80_HOUSES = 93                 # NESPREMENJENO (vseh-8-hiš-ŽE-v-filtru!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1917", d["status"])
    check("I1b 72 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 4 excluded / 15 anomalij / 8 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    grib_e = [e for e in ent if e["griblje"]]
    check("I2 1917 = 72 veljavnih / 18 Griblje-REKORD (frame!)",
          fr["validRows"] == 72 and fr["rowsTotal"] == 72 and fr["stornoRows"] == 0
          and fr["unnumberedRows"] == 0 and len(grib_e) == 18,
          f"{fr['validRows']}/{fr['rowsTotal']}/{len(grib_e)}")
    check("I2b okvir skeni 173–183 + strani 172–182 (s173-DVOPAGE + scan−2-paginacija!)",
          fr["scans"] == NEW_SCANS and fr["pages"] == list(range(172, 183)),
          f"{fr['scans']}")
    hise_clean = sorted({e["houseNo"] for e in grib_e}, key=int)
    check("I2c hiše = [2,3,5,9,14,20,21,26,28,34,36,41,53,54,62,77,78] (h3-×2-PAR!)",
          ",".join(hise_clean) == "2,3,5,9,14,20,21,26,28,34,36,41,53,54,62,77,78", ",".join(hise_clean))

    # ---------- I3: P183-forme ----------
    e22 = next(e for e in ent if e["zap"] == 22)
    check("I3a MRTVOROJENO-z22-smrt=pokop-ISTI-DAN (h14!)",
          "mrtvoroj" in e22["ime"].lower() and e22["danSmrti"] == "21." and e22["danPokopa"] == "21."
          and "ISTI-DAN" in (e22.get("whatSi") or ""), "")
    e51 = next(e for e in ent if e["zap"] == 51)
    e52 = next(e for e in ent if e["zap"] == 52)
    check("I3b 'na-porodu'-z51 + MATER+OTROK-ISTI-DAN (z51/z52 — #9!)",
          "porodu" in e51["vzrok"] and e51["danSmrti"] == e52["danSmrti"], "")
    e66 = next(e for e in ent if e["zap"] == 66)
    e71 = next(e for e in ent if e["zap"] == 71)
    check("I3c BEGUNCI-×2 (z66-Tolmina + z71-Vojsike!)",
          "BEGUNKA" in e66["stan"] and "Tolmin" in e66["stan"]
          and "BEGUNEC" in e71["stan"] and "Vojsic" in e71["stan"], "")
    e42 = next(e for e in ent if e["zap"] == 42)
    check("I3d vojak-služba-številka-z42 (1.×!)",
          "VOJAK" in e42["stan"] and "6 l." in e42["starost"], e42["stan"][:60])
    check("I3e BREZ-storno/BREZ-ne-štet (1917-čisto!)",
          fr["stornoRows"] == 0 and fr["unnumberedRows"] == 0, "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 71 — 139.–149. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 162–172",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: P183-lead-korekcije ----------
    e1 = next(e for e in ent if e["zap"] == 1)
    check("I5a LEAD-RAZREŠEN-z1: roj. '1843'→1913!",
          "1913" in e1["starost"] and "LEAD-RAZREŠEN" in (e1.get("whatSi") or ""), e1["starost"])
    e7 = next(e for e in ent if e["zap"] == 7)
    check("I5b LEAD-KOREKCIJA-z7: 'Griblje'→GRIŠIČE-h49 (EXCLUDED!)",
          e7["griblje"] is False and "Grišiče" in e7["vas"], e7["vas"])
    e11 = next(e for e in ent if e["zap"] == 11)
    check("I5c LEAD-KOREKCIJA-z11: 'Tožek'→POŽEK-h77-roj.-KRIŽAN!",
          "Požek" in e11["ime"] and e11["houseNo"] == "77" and "Križan" in e11["ime"], "")
    e24 = next(e for e in ent if e["zap"] == 24)
    check("I5d LEAD-KOREKCIJA-z24: 'Tožek'→POŽEK-h21 (korpus-×3!)",
          "Požek" in e24["ime"] and e24["houseNo"] == "21", "")
    e28 = next(e for e in ent if e["zap"] == 28)
    check("I5e LEAD-RAZREŠEN-×3-z28: KRALJ + OŽENJEN + 73-let!",
          "Kralj" in e28["ime"] and "73 let" in e28["starost"]
          and "oženjen 30.IV.1893" in e28["stan"], "")
    e46 = next(e for e in ent if e["zap"] == 46)
    e72 = next(e for e in ent if e["zap"] == 72)
    check("I5f 'Grm'-kratka-forma-×5 (z46-h36 + z72-h28!)",
          "Grm" in e46["vas"] and "Grm" in e72["vas"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1100", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 401", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1917 = [v for v in d04894 if v["year"] == 1917]
    check("I6c bloki 1917 = 18 (Griblje-REKORD!)",
          len(d1917) == 18 and all(v["houseNo"] in {"2", "3", "5", "9", "14", "20", "21", "26", "28", "34", "36", "41", "53", "54", "62", "77", "78"}
                                   for v in d1917), str(len(d1917)))
    check("I6d bloki 1925+ ne obstajajo (P190-KONEC-KNJIGE!)",
          all(v["year"] < 1925 for v in d04894), "")
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1118 + 93 + gap-18 (vitals-P183-kaskada!)",
          "len(vitals) == 1355" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: h78 + PAR-KRIŽAN + vzroki ----------
    e58 = next(e for e in ent if e["zap"] == 58)
    check("I7a h78-1.-MRLIŠKI-VPIS-KADARKOLI + ANGINA-1.× (z58!)",
          e58["houseNo"] == "78" and "angina" in e58["vzrok"]
          and "MRLIŠKI-VPIS-KADARKOLI" in (e58.get("whatSi") or ""), "")
    e34 = next(e for e in ent if e["zap"] == 34)
    e61 = next(e for e in ent if e["zap"] == 61)
    check("I7b PAR-KRIŽAN-h3-×2-v-6-MESECIH (DVOJNA-TRAGEDIJA-#8!)",
          e34["houseNo"] == "3" and e61["houseNo"] == "3"
          and "Križan" in e34["ime"] and "Križan" in e61["ime"], "")
    check("I7c okrajšave-z-tildo-×13-VSE-SKLADNE (starosti-Griblje!)",
          sum(1 for e in grib_e if "=1" in (e["starost"] or "") or "=18" in (e["starost"] or "")
              or "=184" in (e["starost"] or "") or "=185" in (e["starost"] or "")
              or "=186" in (e["starost"] or "") or "=183" in (e["starost"] or "")
              or "=191" in (e["starost"] or "")) >= 10,
          str(sum(1 for e in grib_e if "=" in (e["starost"] or ""))))
    e18 = next(e for e in ent if e["zap"] == 18)
    check("I7d WWI-begunci+vojaki-masovni (z66/z71 + z42/z58/z60/z70!)",
          sum(1 for e in ent if "BEGUN" in (e["stan"] or "")) >= 2
          and sum(1 for e in ent if "voj" in (e["stan"] or "")) >= 2, "")

    # ---------- I8: meja-1916/17 + glave ----------
    check("I8 meja-1917/18 = s184-restart (24.-POTRDITEV + begunci-nadaljevanje!)",
          "s184" in fr["meja1917_18"] and "24.-POTRDITEV" in fr["meja1917_18"],
          fr["meja1917_18"][:60])
    check("I8b paginacijski-prelom-'162b'-insert-A9 (1.×-knjige!)",
          any("162b" in a["opis"] for a in d["anomalies"]), "")

    # ---------- I9: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I9a qa-pini 1355 (90×+)", qa.count("!== 1355") >= 90, str(qa.count("!== 1355")))
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
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1355", "BLOKI_04894 = 520",
                                          "1925")))
    check("I10a p153–p184 skripte VITALS_TOTAL 1219 + BLOKI 520 + guardi 1925",
          all(stale), f"{stale.count(True)}/34")

    # ---------- I11: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I11 notes: IZENAČI-REKORD + PAGINACIJSKI-PRELOM + BEGUNCI + h78",
          "IZENAČI-REKORD-1912" in n and "PAGINACIJSKI-PRELOM" in n
          and "BEGUNCI" in n and "MRLIŠKI-VPIS-KADARKOLI" in n, "")

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
        for scan_no in (173, 180, 183):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s173/s180/s183", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p183: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
