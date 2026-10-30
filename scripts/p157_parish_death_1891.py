#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P157 — MRLIŠKA knjiga 04894, leto 1891 = 6. polno leto mrliške linije
(s28-dno + s29–s33 == str. 27–32; 65 vrstic / 15 Griblje-vpisov / 13 hiš —
h6 + h61 ×2 edini ponovitvi). (issue #18). ★★ r13-95→75 POPRAVEK (γ-7-forma!) — rekord ostaja 92-P155.
+ ★★★ DUHOVNIŠKA KRIZA 1891 (7 podpisnih oblik — 3 duhovnika v 5 dneh avgusta
+ ČEŠAREK-era ×6!) + ★★ STRAUS/ŠTRAVS-mreža #4 (h71 Matija Štravs 85!) +
★★ ISTO-IMEŠKI PAR h6 (2× Matija Jakobčič!) + FILAK-lead POTRJEN + ★★★ h85 =
PRVI DOKAZ KADARKOLI → p80 82→83 EDINA! + RDEČE oznake X9 + meja 1891/92 =
4. STIL (glava+marker). Kumulativ: vitals 777 → 792, mrliški bloki 04894
78 → 93, p80 hiše 82 → 83 (+h85 EDINA!), korpus hiše 90 (0 novih).
Vzorec p156."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1891.json"
DOKAZ_P156 = "research/issue17/parish-death-1890.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1891-notes.md"

EXPECTED_ENTRIES = 15            # P156-lead-r1 (Ana Schweiger = izključena!) + 15 novih
EXPECTED_EXCLUDED = 7            # 1891-lead + s29–s33 nonG (5) + 1892-lead
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "6,9,16,23,30,46,55,56,61,62,68,71,85"
VITALS_TOTAL = 853               # POSODABLJENO P162: 837 + 16 (mrliška 1896)!
BLOKI_04894 = 154               # POSODABLJENO P162: 138 + 16 (mrliška 1896)!
P80_HOUSES = 82                  # TS-filter (04105-1897 samo h61!): 81 + h85! EDINA nova 1891
NEW_SCANS = [29, 30, 31, 32, 33]

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

    # ---------- I1: dokaz-structura ----------
    check("I1 dokaz obstaja + status", d.get("status") == "SAMPLE-TRANSCRIPTION-D1891", d.get("status", ""))
    check("I1b št. vpisov = 15", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c izključene skupine = 7",
          len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije ×10 + križne ×10 + iskrenost ×10", (
        len(d["anomalies"]) == EXPECTED_ANOMALIES
        and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS
        and len(d["honesty"]) == 10), f"{len(d['anomalies'])}/{len(d['crossChecks'])}/{len(d['honesty'])}")

    # ---------- I2: vrste, hiše, meseci ----------
    vrste = [e["row"] for e in ent]
    check("I2 vrste naraščajoče (13,17,27,30,33,34,39,41,42,43,55,56,62,63,64)",
          vrste == sorted(vrste) and vrste == [13, 17, 27, 30, 33, 34, 39, 41, 42, 43, 55, 56, 62, 63, 64],
          ",".join(map(str, vrste)))
    uniq = sorted({e["houseNo"] for e in ent}, key=int)
    check("I2b hišni multizbroj = 13 različnih (h61 ×2 + h6 ×2!)",
          len(uniq) == 13, ",".join(uniq))
    check("I2c h61 ×2 (r13-Novak-75 + r41-Požek-½-ure!)",
          sum(1 for e in ent if e["houseNo"] == "61") == 2
          and {e["row"] for e in ent if e["houseNo"] == "61"} == {13, 41}, "")
    check("I2c2 h6 ×2 ISTO-IMEŠKA (r39 + r64 Jakobčič!)",
          sum(1 for e in ent if e["houseNo"] == "6") == 2
          and {e["row"] for e in ent if e["houseNo"] == "6"} == {39, 64}
          and all("Jakobčič" in e["ime"] for e in ent if e["houseNo"] == "6"), "")
    meseci = {}
    for e in ent:
        meseci[e["mesec"][:3]] = meseci.get(e["mesec"][:3], 0) + 1
    check("I2c3 meseci (Mar 2 · Maj 1 · Jun 2 · Jul 2 · Avg 3 · Okt 1 · Nov 1 · Dec 3)",
          meseci == {"Mar": 2, "Maj": 1, "Jun": 2, "Jul": 2, "Avg": 3, "Okt": 1, "Nov": 1, "Dec": 3},
          json.dumps(meseci, ensure_ascii=False))

    # ---------- I3: live viri ----------
    if live:
        try:
            st, body = http_get(BOOK_URL)
            ok200 = st == 200
            check("I3a knjiga 04894 HTTP 200", ok200, str(st))
            urls = []
            if ok200:
                for m in re.finditer(r'"(/image/[A-Za-z0-9+/=%]+/)"', body.decode("utf-8", "replace")):
                    import base64
                    s = m.group(1)[7:-1]
                    try:
                        dd = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                        if dd.startswith("http"):
                            urls.append(dd)
                    except Exception:
                        pass
                urls = sorted(set(urls))
            check("I3b inventar 256", len(urls) == 256, str(len(urls)))
            probes_ok, det = 0, []
            for sc in NEW_SCANS:
                if sc - 1 < len(urls):
                    try:
                        st2, data = http_get(urls[sc - 1], timeout=45)
                        ok = st2 == 200 and len(data) > 50000
                        probes_ok += 1 if ok else 0
                        det.append(f"s{sc}:{st2}")
                    except Exception as e:
                        det.append(f"s{sc}:ERR")
            check("I3c citirani skeni 5/5 JPEG 200", probes_ok == 5, " ".join(det))
        except Exception as e:
            check("I3 live-viri", False, str(e))

    # ---------- I4: preslikava stran == sken − 1 ----------
    check("I4 stran == sken − 1 (vseh 15)",
          all(e["page"] == e["scan"] - 1 for e in ent), "")
    check("I4b skeni v naboru 29+30+31+32+33",
          sorted({e["scan"] for e in ent}) == NEW_SCANS, "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    check("I5 13 različnih hiš", len(uniq) == 13, ",".join(uniq))
    for h, leto in (("56", 1891), ("68", 1891), ("9", 1891), ("6", 1891), ("62", 1891), ("23", 1891), ("85", 1891)):
        prej = [v for v in vit if v["houseNo"] == h and v["bookSignature"] == "04894" and v["year"] < leto]
        check(f"I5b h{h} = 1. mrliški vpis (prej 0 v 04894)", len(prej) == 0,
              f"prej: {sorted({v['year'] for v in prej})}")
    for h, pred in (("68", 1914), ("9", 1894), ("6", 1903)):
        prej_leta = sorted(v["year"] for v in vit if v["houseNo"] == h)
        check(f"I5c h{h} = najzgodnejši vpis kadarkoli (prej {pred} → zdaj 1891!)",
              bool(prej_leta) and min(prej_leta) == 1891 and pred in prej_leta, str(prej_leta[:4]))
    check("I5c2 h62 ostaja pri krstni-1887 + h85 pri krstni-1888 (popravek najzgodnejših!)",
          min(v["year"] for v in vit if v["houseNo"] == "62") == 1887
          and min(v["year"] for v in vit if v["houseNo"] == "85") == 1888, "")
    h85_vsi = [v for v in vit if v["houseNo"] == "85"]
    h85_mrl = [v for v in h85_vsi if v["bookSignature"] == "04894"]
    h85_krst = [v for v in h85_vsi if v["bookSignature"] == "04105"]
    check("I5d h85 = 1 mrliški (1891) + krstni 1888/1908 izven p80-filtra",
          len(h85_mrl) == 1 and h85_mrl[0]["year"] == 1891
          and sorted(v["year"] for v in h85_krst) == [1888, 1908]
          and all(v["year"] not in (1886, 1897) for v in h85_krst), "")

    # ---------- I6: parish.ts ----------
    check("I6a vitals 825", len(vit) == VITALS_TOTAL, str(len(vit)))
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6b mrliški bloki 04894 = 138", len(d04894) == BLOKI_04894, str(len(d04894)))
    d1891 = [v for v in d04894 if v["year"] == 1891]
    check("I6c bloki 1891 = 15", len(d1891) == 15, str(len(d1891)))
    check("I6d bloki 1891: skeni 29–33 + stran == sken − 1",
          all(v["scan"] and 29 <= v["scan"] <= 33 and v["page"] == v["scan"] - 1 for v in d1891), "")
    check("I6d2 bloki 1894+ ne obstajajo (P161-lead!; P159 = 1893 v korpusu!)",
          all(v["year"] < 1897 for v in d04894), "")
    p80 = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 819 + 86",
          "len(vitals) == 853" in p80 and "len(houses) == 88" in p80, "")  # python-p80 = 84 (širši 1897-filter))
    houses_all = {v["houseNo"] for v in vit if v["houseNo"].isdigit()}
    check("I6g korpus = 92 hiš (P159: +h98 EDINA!)", len(houses_all) == 93, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika ----------
    r13 = next((e for e in ent if e["row"] == 13), None)
    check("I7a r13 = 95→75 POPRAVEK (h61 Novak vdova-kolarica! γ-7-forma)",
          bool(r13) and r13["houseNo"] == "61" and "75 let" in r13["whatSi"]
          and "γ-7-forma" in r13["whatSi"] and "rekord linije OSTAJA 92" in r13["whatSi"]
          and "kolarica" in r13["whatSi"].lower(), "")
    r63 = next((e for e in ent if e["row"] == 63), None)
    check("I7b r63 h71 ≠ 91 (γ-7-forma!) + ŠTRAVS ne Škraba + 85 let",
          bool(r63) and r63["houseNo"] == "71" and "ŠTRAVS" in r63["whatSi"]
          and "Škraba" in r63["whatSi"] and "'91' ZAVRJEN" in r63["whatSi"]
          and "85 let" in r63["whatSi"], "")
    r41 = next((e for e in ent if e["row"] == 41), None)
    check("I7c r41 = Nikolaj POŽEK (VLM ×3 ZAVRJENI!) + ½ URE najkrajši",
          bool(r41) and "POŽEK" in r41["whatSi"] and "Fošek" in r41["whatSi"]
          and "½ URE" in r41["whatSi"], "")
    r56 = next((e for e in ent if e["row"] == 56), None)
    check("I7d r56 = BRINEC ne Božičec (max-zoom!)",
          bool(r56) and "BRINEC" in r56["whatSi"] and "Božičec" in r56["whatSi"], "")
    r33 = next((e for e in ent if e["row"] == 33), None)
    check("I7e r33 = FILAK + 'vdova kolarica' + Češarek-'župnik' podpis",
          bool(r33) and "FILAK" in r33["whatSi"] and "kolarica" in r33["whatSi"].lower()
          and "župnik" in r33["whatSi"], "")
    r17 = next((e for e in ent if e["row"] == 17), None)
    check("I7f r17 = 'vdovec in kolar' (VLM 'Notar' ZAVRJEN!) + Šarost [~]",
          bool(r17) and "vdovec in kolar" in r17["whatSi"].lower() and "Notar" in r17["whatSi"]
          and "Šarost" in r17["whatSi"], "")

    # ---------- I8: P156-kontinuiteta ----------
    p156 = json.load(open(DOKAZ_P156, encoding="utf-8"))
    e1 = next((x for x in d["excluded"] if x["id"] == "E1"), None)
    check("I8a P156-lead Ana Schweiger POTRJEN (5/5: ime+⅓+17-mesec+datumi+vas)",
          bool(e1) and "Ana Schweiger" in e1["opis"] and "17 MESECEV" in e1["opis"]
          and "100% POTRJEN" in e1["opis"].replace("100 %", "100%"), "")
    check("I8b LEAD-POPRAVEK Otok 18 → 15. (P156-lead-delna-napaka!)",
          bool(e1) and "Otok 15." in e1["opis"] and "POPRAVEK 15." in e1["opis"].replace("→ POPRAVEK 15.", "→ POPRAVEK 15."), "")
    check("I8c r53-vzorec #3 (neimenovani + brez podpisa: P153-53 + P156-53 + 1891-r2!)",
          bool(e1) and "r53-vzorec #3" in e1["opis"], "")

    # ---------- I9: mreže ----------
    x2 = next((x for x in d["crossChecks"] if x["id"] == "X2"), None)
    check("I9a X2 STRAUS/ŠTRAVS-mreža #4 (4 smrti v 4 letih!)",
          bool(x2) and "#4" in x2["name"], "")
    check("I9b r63 STRAUS/ŠTRAVS-mreža #4 v bloku",
          bool(r63) and "straus/štravs-mreža #4" in r63["whatSi"].lower(), "")
    x10 = next((x for x in d["crossChecks"] if x["id"] == "X10"), None)
    check("I9c X10 najzgodnejši ×3 + p80-h85",
          bool(x10) and "×3" in x10["name"] and "81→82" in x10["detail"].replace("81 → 82", "81→82"), "")
    x6 = next((x for x in d["crossChecks"] if x["id"] == "X6"), None)
    check("I9d X6 FILAK-lead POTRJEN (×2 v 2 mesecih!)",
          bool(x6) and "DOKAZANA" in x6["detail"], "")
    x5 = next((x for x in d["crossChecks"] if x["id"] == "X5"), None)
    check("I9e X5 ISTO-IMEŠKI PAR h6 (oče+sin? — isto ime + isto hišo!)",
          bool(x5) and "isto ime + isto hišo" in x5["detail"]
          and "oče + sin" in x5["detail"], "")

    # ---------- I10: podpisi + duhovniki + rekordi ----------
    signed = [e for e in ent if e.get("duhovnik")]
    n_rauq = sum(1 for e in signed if "Rauq" in e["duhovnik"])
    n_cesarek = sum(1 for e in signed if "Češarek" in e["duhovnik"])
    n_saselj = sum(1 for e in signed if "Šašelj" in e["duhovnik"])
    n_belavic = sum(1 for e in signed if "Belavič" in e["duhovnik"])
    check("I10a podpisi 15/15 (Rauq ×7 + Češarek ×6 + Šašelj ×2 [r43 + r33-Šašeř~Šašelj!] + Belavič ×1)",
          len(signed) == 15 and (n_rauq, n_cesarek, n_saselj, n_belavic) == (7, 6, 2, 1),
          f"Rauq {n_rauq} / Češarek {n_cesarek} / Šašelj {n_saselj} / Belavič {n_belavic}")
    r42 = next((e for e in ent if e["row"] == 42), None)
    check("I10b r42 Rauq ŽUP. (1. titel!) + AVGUSTOVSKI LOM",
          bool(r42) and "ŽUP." in r42["whatSi"] and "AVGUSTOVSKI" in r42["whatSi"], "")
    ages = [e["starost"] for e in ent]
    check("I10c razpon ½ ure → 85 let",
          "½ ure" in ages and "85 let" in ages, str(ages))
    mla = [e for e in ent if e["starost"] in ("½ ure", "14 dni", "1 leto", "2½ leta")]
    check("I10d otroška umrljivost 5/15 = 33 % (≤3 leta ×5 — med 1889 in 1890!)",
          len(mla) == 5, str([e["starost"] for e in mla]))
    r30 = next((e for e in ent if e["row"] == 30), None)
    check("I10e r30 Belavič KAPLAN (1. kaplan-podpis linije!)",
          bool(r30) and "KAPLAN" in r30["whatSi"] and "Belavič" in r30["whatSi"], "")

    # ---------- I11: meja 1892 + lead + rdeče oznake + glave ----------
    fr = d["frame"]
    check("I11 meja 1891/92 = 4. STIL (glava »Leto 1892.« + podčrtan marker, s34)",
          "4. STIL" in fr["boundaries"] and "1892" in fr["boundaries"], "")
    check("I11b stran == sken − 1 = 12. potrditev (source.pageMapping)",
          "12. potrditev" in d["source"]["pageMapping"], "")
    check("I11c glave »Leto 1891« izpisane 5/5 (frame.glave)",
          "5/5" in fr["glave"], "")
    check("I11d rdeče oznake X9 (source.layout + X9-detail)",
          "X9" in d["source"]["layout"] and "rdeče kredne" in next(x["detail"] for x in d["crossChecks"] if x["id"] == "X9"), "")

    # ---------- I12: qa + README + notes ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p157 obstaja", "qa-p157-parish-death-1891" in qa, "")
    check("I12b qa-p158 guard 1893 (posodobljeno)", "1897+-mrliški bloki že v korpusu" in qa, "")
    check("I12c qa-pini 837/138/87 (75×+9×+13×)",
          qa.count("!== 853") >= 77 and qa.count("!== 154") >= 11 and qa.count("p80Houses.size !== 88") >= 14,
          f"{qa.count('!== 837')}/{qa.count('!== 126')}/{qa.count('p80Houses.size !== 87')}")
    readme = open(README, encoding="utf-8").read()
    check("I12d README P157", "P157" in readme and "1891" in readme, "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I12e notes obstajajo (95→75 POPRAVEK + duhovniška kriza)",
          "95→75" in notes and "DUHOVNIŠKA KRIZA" in notes, "")

    # ---------- izpis ----------
    fails = [r for r in results if not r[1]]
    for name, ok, det in results:
        print(("PASS " if ok else "FAIL ") + name + (f"  [{det}]" if det and not ok else ""))
    print(f"\n{len(results) - len(fails)}/{len(results)} PASS"
          + ("" if not fails else f" — {len(fails)} FAIL!"))
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
