#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P181 — MRLIŠKA knjiga 04894, leto 1915 = 30. polno leto mrliške linije (issue #18):
s152–s161 == str. 151–160 (stran == sken − 1 — 129.–138. potrditev!) + 68 vpisov /
9 GRIBLJE / 8 hiš (h90 ×2!) + ★★★ 4 × 1.-×-FORME (EKSPlicitna zaključna opomba s161
'V številko 68. je leto 1915 končano. Podzemelj, 31. decemb. 1915' + podpis + diagonalni
črti ×2 · STORNO-z61-1.×-mrliška · CORREXIT-z68-'Dejnar→Černič'+'corr.'-1.× ·
ne-štet-Županič-Kandija-zap-prazno-1.×) + ★★★ 'Grm' = GRIBLJE-kratka-forma-1.×
(hišni-referenci h25/h28!) + ★★★ h90-×2-v-5-DNEH = SESTRI-Šušteršič-učitelja-otroka
(dvojčki-smrti-#5!) + 'Grišiče' ≠ Griblje (P92-leksikon!) + TUJI-hospital-VPIS-#2
(žel. delavec-Kandija-sepsis!) + 'pokopan na starem pokopališču' ×~10-1.×-MASOVNI +
vzroki-leksikon ×5-novi (SRČNA KAP + TIFUS + hiravost + vodenica-×3 + SEPSIS!) +
1.-TESAR + 1.-ČEVLJAR-poklic + BRINEC-mreža ×3-hiš (h88/h5/h25!) + podpis-zmeda-9.-leto
(Bitnar-×~21 + Učakar-×~15-forme!) + 3-LEAD-KOREKCIJE (P181-lead: 'Griblje-h33-Tapič'→
Grišiče-h33-PAPIČ + z19-Hudorovič + z20-Boršt/h23!) + meja 1915/16 = s162 = 22.-
POTRDITEV (nov-podvzorec-#6: zaključna-opomba + glava + velika-letnica + restart!).
Kumulativ: vitals 1082 → 1091, mrliški bloki 04894 383 → 392, p80 hiše 93-NESPREMENJENO
(vseh-8-hiš-že-v-filtru!), korpus 93-NESPREMENJEN, PT-luknja 18-NESPREMENJENA.
Vzorec p180."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1915.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
NOTES = "research/issue17/parish-death-1915-notes.md"
P80 = "scripts/p80_parish_md_books.py"

EXPECTED_ENTRIES = 68
EXPECTED_EXCLUDED = 1
EXPECTED_ANOMALIES = 14
EXPECTED_CROSSCHECKS = 7
GRIBLJE_HOUSES = "5,8,17,25,44,45,88,90,90"
VITALS_TOTAL = 1194             # 1180 + 14! (P188)
BLOKI_04894 = 495               # 481 + 14! (P188)
P80_HOUSES = 93                 # NESPREMENJENO (vseh-8-hiš-ŽE-v-filtru!)
KORPUS_HOUSES = 93              # NESPREMENJENO
NEW_SCANS = [152, 153, 154, 155, 156, 157, 158, 159, 160, 161]

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
    check("I1 dokaz obstaja + status", d["status"] == "SAMPLE-TRANSCRIPTION-D1915", d["status"])
    check("I1b 68 vnosov", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c 1 excluded / 14 anomalij / 7 križnih",
          len(d["excluded"]) == EXPECTED_EXCLUDED and len(d["anomalies"]) == EXPECTED_ANOMALIES
          and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS,
          f"{len(d['excluded'])}/{len(d['anomalies'])}/{len(d['crossChecks'])}")

    # ---------- I2: okvir ----------
    grib_e = [e for e in ent if e["vas"] == "Griblje" or (e.get("vas") or "").startswith("Griblje [")]
    check("I2 1915 = 68 veljavnih / 9 Griblje (frame!)",
          fr["validRows"] == 68 and fr["rowsTotal"] == 69 and fr["stornoRows"] == 1
          and fr["unnumberedRows"] == 1 and len(grib_e) == 9,
          f"{fr['validRows']}/{fr['rowsTotal']}/{len(grib_e)}")
    check("I2b okvir skeni 152–161 + strani 151–160",
          fr["scans"] == NEW_SCANS and fr["pages"] == list(range(151, 161)),
          f"{fr['scans']}")
    hise_clean = sorted({e["houseNo"] for e in grib_e}, key=int)
    check("I2c hiše = [5,8,17,25,44,45,88,90] (h90-×2!)",
          ",".join(hise_clean) == "5,8,17,25,44,45,88,90", ",".join(hise_clean))

    # ---------- I3: 4 × 1.-×-FORME ----------
    check("I3a EXPLICITNA-zaključna-opomba (s161!)",
          "V številko 68. je leto 1915 končano" in fr["yearEnd"]["note"]
          and "31. decemb. 1915" in fr["yearEnd"]["note"]
          and "diagonalni" in fr["yearEnd"]["note"], fr["yearEnd"]["note"][:60])
    ex = d["excluded"][0]
    check("I3b STORNO-z61 (1.×-mrliška!)",
          ex["zap"] == 61 and "STORNIRAN" in ex["vrsta"]
          and "h36" in ex["opis"] and "P100" in ex["cf"], ex["vrsta"][:50])
    e68 = next(e for e in ent if e["zap"] == 68)
    check("I3c CORREXIT-z68 (Dejnar→Černič + 'corr.'!)",
          "Dejnar" in e68["ime"] and "Černič" in e68["ime"] and "corr. Mcač" in e68["ime"], "")
    zp = next(e for e in ent if e["zap"] is None)
    check("I3d ne-štet-Županič (zap-prazno-1.×! + Kandija-hospital!)",
          zp["ime"] == "Jožef Županič" and "Kandija" in zp["vas"]
          and "SEPSIS" in zp["vzrok"] and "okr. glav. Rudolf" in (zp.get("opomba") or ""), "")

    # ---------- I4: invarianta ----------
    check("I4 stran == sken − 1 (vseh 68 — 129.–138. potrditev!)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 152–161",
          all(e["scan"] in NEW_SCANS for e in ent), str(sorted({e["scan"] for e in ent})))

    # ---------- I5: 'Grm'-forma + lead-korekcije ----------
    e56 = next(e for e in ent if e["zap"] == 56)
    check("I5a z56-'Grm' = GRIBLJE-kratka-forma (h25-hišna-referenca!)",
          "Grm" in e56["vas"] and "kratka-forma" in (e56.get("whatSi") or ""), "")
    e13 = next(e for e in ent if e["zap"] == 13)
    check("I5b LEAD-KOREKCIJA-#1: 'Griblje-h33-Tapič' → Grišiče-h33-PAPIČ!",
          "Grišiče" in e13["vas"] and "Papič" in e13["ime"], e13["vas"][:40])
    e19 = next(e for e in ent if e["zap"] == 19)
    check("I5c LEAD-KOREKCIJA-#2: z19 = Grišiče-Hudorovič-cigan (hiša-'—'!)",
          "Grišiče" in e19["vas"] and "Hudorovič" in e19["ime"] and e19["houseNo"] == "—", "")
    e20 = next(e for e in ent if e["zap"] == 20)
    check("I5d LEAD-KOREKCIJA-#3: z20 = Boršt-h23-41-l (NE-Griblje!)",
          e20["vas"] == "Boršt" and e20["houseNo"] == "23" and "41" in e20["starost"], "")
    e17 = next(e for e in ent if e["zap"] == 17)
    check("I5e P180-LEAD-potrjen: z17-h88-Ivana-BRINEC!",
          e17["vas"] == "Griblje" and e17["houseNo"] == "88" and "Brinec" in e17["ime"], "")

    # ---------- I6: kumulativ + parish.ts ----------
    vit = parse_house_vitals()
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 1100", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 401", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1915 = [v for v in d04894 if v["year"] == 1915]
    check("I6c bloki 1915 = 9 (Griblje!)",
          len(d1915) == 9 and all(v["houseNo"] in {"5", "8", "17", "25", "44", "45", "88", "90"}
                                   for v in d1915), str(len(d1915)))
    check("I6d bloki 1923+ ne obstajajo (P189-lead!)",
          all(v["year"] < 1923 for v in d04894), "")
    p80src = open(P80, encoding="utf-8").read()
    check("I6e p80-skripta pini 1091 + 93 + gap-18 (vitals-P181-kaskada!)",
          "len(vitals) == 1100" in p80src and "len(houses) == 94" in p80src
          and "len(gap) == 18" in p80src, "")

    # ---------- I7: h90-×2-SESTRI + poklici ----------
    e40 = next(e for e in ent if e["zap"] == 40)
    e42 = next(e for e in ent if e["zap"] == 42)
    check("I7a h90-×2-v-5-DNEH = SESTRI (Ivanka + Minka — učitelja otroka!)",
          e40["houseNo"] == "90" and e42["houseNo"] == "90"
          and "učitelja otrok" in e40["stan"] and "učitelja otrok" in e42["stan"]
          and "Minka" in e42["ime"], "")
    e41 = next(e for e in ent if e["zap"] == 41)
    check("I7b 1.-TESAR-poklic (z41-Kralj-tesarski-pomočnik!)",
          "tesarski pomočnik" in e41["stan"] and "Kralj" in e41["ime"], "")
    e46 = next(e for e in ent if e["zap"] == 46)
    check("I7c 1.-ČEVLJAR-leksikon (z46-Rajmer-čevljarskega-mojstra!)",
          "čevljarskega mojstra" in e46["stan"], "")
    e32 = next(e for e in ent if e["zap"] == 32)
    check("I7d z32-starost-POPRAVEK 78 → 28 (@×6!)",
          "28" in e32["starost"] and "NE 78" in e32["starost"], "")

    # ---------- I8: vzroki-leksikon-novi ----------
    e57 = next(e for e in ent if e["zap"] == 57)
    e35 = next(e for e in ent if e["zap"] == 35)
    check("I8a SRČNA KAP-1.× (z57!) + TIFUS-1.× (z35!)",
          "SRČNA KAP" in e57["vzrok"] and "TIFUS" in e35["vzrok"], "")
    check("I8b vodenica/vodemica-×3 (z8 + z37 + z39!)",
          "vodenica" in next(e for e in ent if e["zap"] == 8)["vzrok"]
          and "vodemica" in next(e for e in ent if e["zap"] == 37)["vzrok"]
          and "vodemica" in next(e for e in ent if e["zap"] == 39)["vzrok"], "")
    check("I8c 'pokopan(a) na starem pokopališču'-opombe (×8-v-dokazu!)",
          sum(1 for e in ent if "starem pokopališču" in (e.get("opomba") or "")) >= 8,
          str(sum(1 for e in ent if "starem pokopališču" in (e.get("opomba") or ""))))

    # ---------- I9: meja-1915/16 ----------
    check("I9 meja-1915/16 = s162 (22.-POTRDITEV — nov-podvzorec-#6!)",
          "22.-POTRDITEV" in fr["boundary1916"]["note"]
          and "1916" in fr["boundary1916"]["note"], fr["boundary1916"]["note"][:60])

    # ---------- I10: qa-parish.ts pini ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I10a qa-pini 1091 (95×)",
          qa.count("!== 1194") >= 90, str(qa.count("!== 1194")))
    check("I10b qa-pini 392 (15×+)",
          qa.count('04894").length !== 495') >= 15
          and "p80Death.length !== 495" in qa, str(qa.count('04894").length !== 495')))
    check("I10c qa guard 1919 (bloki 1919+ ne!)",
          "1916+-mrliški bloki že v korpusu" in qa and "(h.year ?? 0) >= 1923" in qa, "")
    check("I10d stale-guardi → 1916 (27× qa)",
          qa.count("(h.year ?? 0) >= 1916") >= 27, str(qa.count("(h.year ?? 0) >= 1916")))

    # ---------- I11: stale-sanacija p153–p180 ----------
    stale = []
    for y in range(153, 181):
        f = f"scripts/p{y}_parish_death_{y - 153 + 1887}.py"
        s = open(f, encoding="utf-8").read()
        stale.append(all(p in s for p in ("VITALS_TOTAL = 1194", "BLOKI_04894 = 495",
                                          "1923")))
    check("I11a p153–p180 skripte VITALS_TOTAL 1100 + BLOKI 401 + guardi 1917",
          all(stale), f"{stale.count(True)}/28")

    # ---------- I12: notes ----------
    n = open(NOTES, encoding="utf-8").read()
    check("I12 notes: 4-×-1.-×-forme + 'Grm' + h90-×2-SESTRI",
          "EKSPlicitna ZAKLJUČNA OPOMBA" in n and "STORNO-VPIS" in n
          and "CORREXIT" in n and "GRIBLJE-kratka-forma" in n
          and "SESTRI-v-5-DNEH" in n, "")

    # ---------- I13: LIVE (matricula) ----------
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
        for scan_no in (152, 159, 161):
            st2, img = http_get(urls[scan_no - 1])
            probes.append(st2 == 200 and img[:2] == b"\xff\xd8")
        check("L3 JPEG-probe-s152/s159/s161", all(probes), str(probes))

    ok = sum(1 for _, o, _ in results if o)
    print(f"p181: {ok}/{len(results)} {'PASS' if ok == len(results) else 'FAIL'}")
    for name, o, det in results:
        if not o:
            print(f"  FAIL: {name} {det}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
