#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P156 — MRLIŠKA knjiga 04894, leto 1890 = 5. polno leto mrliške linije
(s24-dno + s25–s28 == str. 23–27; 55 vrstic / 15 Griblje-vpisov / 14 hiš —
vrnitev med 1889-dnom in 1888-rekordom). (issue #18). ★★★ 1. STAN 'učitelj'
mrliške + ★★★ UČITELJSKA ZAMENJAVA 1890 POTRJENA PREK SMRTI (r8 h90 Klambič-
učitelj † 26./28.1. ↔ krstna-1890-h90 Kopitar-učitelj 16./17.11. — P155-lead-
hipoteza DOKAZANA!) + ★★★ 1. izpisani 'Mrtvorojeno' (r53 h35 N. Križan — smrt
= pokop ISTI DAN, 'dete' neutersko, brez podpisa — LEKSIKONSKA REFERENCA, ampak
Mertvod-odrasli ×3 ≠ enostavna enačba!) + ★ 1. poklic 'mizarjeva žena' (r32 h7)
+ ★★ 1. 'Prezgodnji porod' (r10 h37, 2 URI) + ★★ h30 dojenčki ×2 v 5 dneh
+ ★★ STRAUS-mreža ×3 + ★ NOV duhovnik Šašelj-Adlešiči + meja 1890/91 = »1891«
inline na s28 (2 SKENA PREJ kot P155-lead-napoved!). Kumulativ: vitals 762 → 777,
mrliški bloki 04894 63 → 78, p80 hiše 80 → 82 (+h90 EDINA!), korpus hiše 90
(0 novih). Vzorec p155."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1890.json"
DOKAZ_P155 = "research/issue17/parish-death-1889.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1890-notes.md"

EXPECTED_ENTRIES = 15            # 1 P155-lead (Klambič!) + 14 novih
EXPECTED_EXCLUDED = 8            # skupine vrstic izven Gribelj + 1891-lead + 1889 + s29
EXPECTED_ANOMALIES = 10
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "7,18,26,27,30,32,35,37,38,42,58,71,90,91"
VITALS_TOTAL = 894               # POSODABLJENO P162: 837 + 16 (mrliška 1896)!
BLOKI_04894 = 195                # POSODABLJENO P164: + 7 (mrliška 1898)!
P80_HOUSES = 82                  # 81 + h90! (EDINA nova p80-hiša 1890!)
NEW_SCANS = [24, 25, 26, 27, 28]

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
        vitals.append({
            "houseNo": pick("houseNo"),
            "bookSignature": pick("bookSignature"),
            "year": pickn("year"),
            "scan": pickn("scan"),
            "page": pickn("page"),
            "whatSi": pick("whatSi") or "",
        })
    return vitals


def main():
    live = "--live" in sys.argv
    d = json.load(open(DOKAZ, encoding="utf-8"))
    ent = d["entries"]

    # ---------- I1: dokaz-structura ----------
    check("I1 dokaz obstaja + status", d.get("status") == "SAMPLE-TRANSCRIPTION-D1890", d.get("status", ""))
    check("I1b št. vpisov = 15", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c izključene skupine = 8",
          len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije ×10 + križne ×10 + iskrenost ×10", (
        len(d["anomalies"]) == EXPECTED_ANOMALIES
        and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS
        and len(d["honesty"]) == 10),
        f"anom {len(d['anomalies'])} cross {len(d['crossChecks'])} hon {len(d['honesty'])}")

    # ---------- I2: vrste, hiše, meseci ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste naraščajoče (8,10,17,18,23,28,29,32,34,35,43,51,53,54,55)",
          rows == sorted(rows) and rows[0] == 8 and rows[-1] == 55, str(rows))
    houses = sorted(set(e["houseNo"] for e in ent), key=int)
    check("I2b hišni multizbroj = 14 različnih (h30 ×2!)",
          ",".join(houses) == GRIBLJE_HOUSES, f"{len(houses)} različnih")
    check("I2c h30 = EDINA hiša z 2 vpisoma",
          sum(1 for e in ent if e["houseNo"] == "30") == 2
          and all(sum(1 for e in ent if e["houseNo"] == h) == 1
                  for h in houses if h != "30"), "")
    months = {}
    for e in ent:
        months[e["mesec"]] = months.get(e["mesec"], 0) + 1
    check("I2c2 meseci (Jan 1 · Feb 3 · Maj 1 · Jun 2 · Jul 1 · Avg 2 · Okt 1 · Dec 4)",
          months == {"Januarj": 1, "Februarj": 3, "Maj": 1, "Junij": 2, "Julij": 1,
                     "Avgust": 2, "Oktober": 1, "December": 4}, str(months))

    # ---------- I3: live viri ----------
    if live:
        st, body = http_get(BOOK_URL)
        ok200 = st == 200
        check("I3a knjiga 04894 HTTP 200", ok200, str(st))
        if ok200:
            html = body.decode("utf-8", "replace")
            inv = re.findall(r'"(/image/[A-Za-z0-9+/=%]+/)"', html)
            urls = set()
            for s in inv:
                import base64
                try:
                    u = base64.b64decode(s[7:-1] + "=" * (-len(s[7:-1]) % 4)).decode()
                    if u.startswith("http"):
                        urls.add(u)
                except Exception:
                    pass
            check("I3b inventar 256", len(urls) == 256, str(len(urls)))
            probes_ok = True
            det = []
            for n in NEW_SCANS:
                try:
                    st2, b2 = http_get(sorted(urls)[n - 1], timeout=60)
                    ok = st2 == 200 and b2[:2] == b"\xff\xd8"
                    probes_ok = probes_ok and ok
                    det.append(f"s{n}:{st2}")
                except Exception:
                    probes_ok = False
                    det.append(f"s{n}:ERR")
            check("I3c citirani skeni 5/5 JPEG 200", probes_ok, " ".join(det))

    # ---------- I4: preslikava stran == sken − 1 ----------
    check("I4 stran == sken − 1 (vseh 15)",
          all(e["page"] == e["scan"] - 1 for e in ent),
          str(sorted({(e["scan"], e["page"]) for e in ent})))
    check("I4b skeni v naboru 24+25+26+27+28",
          sorted({e["scan"] for e in ent}) == NEW_SCANS, "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    uniq = sorted(set(e["houseNo"] for e in ent), key=int)
    check("I5 14 različnih hiš", len(uniq) == 14, ",".join(uniq))
    # 7 hiš = 1. mrliški vpis (prej 0 v 04894! — h7 je imel 1888!)
    for h in ("27", "32", "37", "38", "42", "90", "91"):
        prej = [v for v in vit if v["bookSignature"] == "04894"
                and v["houseNo"] == h and (v["year"] or 0) < 1890]
        check(f"I5b h{h} = 1. mrliški vpis (prej 0 v 04894)", len(prej) == 0,
              f"prej {len(prej)}")
    # 2 hiši = najzgodnejši vpis kadarkoli (mrliška 1890 prekaša poročno!)
    for h, prej_leto in (("18", 1896), ("42", 1894)):
        starejsi = [v for v in vit if v["houseNo"] == h and (v["year"] or 0) < 1890]
        check(f"I5c h{h} = najzgodnejši vpis kadarkoli (prej {prej_leto})",
              len(starejsi) == 0, f"prej-1890: {len(starejsi)}")

    # ---------- I6: parish.ts ----------
    d1890 = [v for v in vit if v["bookSignature"] == "04894" and v["year"] == 1890]
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 777", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 174 (POSODABLJENO P164)", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1890 = 15", len(d1890) == 15, str(len(d1890)))
    check("I6d bloki 1890: skeni 24–28 + stran == sken − 1",
          all(v["scan"] and 24 <= v["scan"] <= 28 and v["page"] == v["scan"] - 1 for v in d1890), "")
    check("I6d2 bloki 1900+ ne obstajajo (P166-lead!; P165 = 1899 sedaj v korpusu!)",
          not [v for v in vit if v["bookSignature"] == "04894" and (v["year"] or 0) >= 1901], "")
    p80_script = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 886 + 88 + gap-18 (POSODABLJENO P164)",
          "len(vitals) == 894" in p80_script and "len(houses) == 89" in p80_script and "len(gap) == 18" in p80_script, "")
    houses_all = {v["houseNo"] for v in vit if v["houseNo"] and v["houseNo"].isdigit()}
    check("I6g korpus = 92 hiš (P159: +h98 EDINA!)", len(houses_all) == 93, str(len(houses_all)))
    # h90 = EDINA nova p80-hiša (krstni dokazi izven filtra!)
    h90_04105 = [v for v in vit if v["houseNo"] == "90" and v["bookSignature"] == "04105"]
    check("I6h h90: krstni dokazi 1890–1919 (izven p80-filtra!) + 1 mrliški",
          len(h90_04105) >= 6 and len([v for v in vit if v["houseNo"] == "90" and v["bookSignature"] == "04894"]) == 1, "")

    # ---------- I7: max-zoom forenzika ----------
    r8 = next((e for e in ent if e["row"] == 8), None)
    check("I7a r8 = učiteljska-zamenjava (LEAD!)",
          bool(r8) and r8["houseNo"] == "90" and "UČITELJ" in r8["whatSi"]
          and "UČITELJSKA ZAMENJAVA" in r8["whatSi"] and "POTRJENA PREK SMRTI" in r8["whatSi"], "")
    r53 = next((e for e in ent if e["row"] == 53), None)
    check("I7b r53 = Mrtvorojeno izpisano + isti dan + dete + brez podpisa",
          bool(r53) and "Mrtvorojeno" in r53["whatSi"] and "19./19." in r53["whatSi"]
          and "DETE" in r53["whatSi"] and "BREZ PODPISA" in r53["whatSi"]
          and r53["duhovnik"] is None, "")
    r32 = next((e for e in ent if e["row"] == 32), None)
    check("I7c r32 = mizarjeva žena (1. poklic!) + previden",
          bool(r32) and "MIZARJEVA ŽENA" in r32["whatSi"] and r32["houseNo"] == "7", "")
    r10 = next((e for e in ent if e["row"] == 10), None)
    check("I7d r10 = 2 URI + Prezgodnji porod (1.! najkrajši 1890!)",
          bool(r10) and "2 URI" in r10["whatSi"] and "Prezgodnji porod" in r10["whatSi"], "")
    r35 = next((e for e in ent if e["row"] == 35), None)
    r54 = next((e for e in ent if e["row"] == 54), None)
    check("I7e referenčni-par 38/58 (ISTA STRAN!)",
          bool(r35) and bool(r54) and "(ne 58!" in r35["whatSi"]
          and "'58'" in r54["whatSi"] and r35["scan"] == 27 and r54["scan"] == 28, "")
    r43 = next((e for e in ent if e["row"] == 43), None)
    check("I7f r43 h71 ≠ 72 (γ-7-forma; nasprotje P154-lead-h72!)",
          bool(r43) and r43["houseNo"] == "71" and "ne 72" in r43["whatSi"].lower(), "")

    # ---------- I8: P155-kontinuiteta ----------
    p155 = json.load(open(DOKAZ_P155))
    check("I8a P155-lead r8 h90 potrjen (Klambič-učitelj)",
          bool(r8) and r8["whatSi"].startswith("umrl g. Peter Klambič"), "")
    p155_last = [e for e in p155["entries"] if e["row"] == 33]
    check("I8b P155 zadnji 1889 (r33 h48) se nadaljuje z 1890-r8 (s24-dno)",
          bool(p155_last) and r8["scan"] == 24, "s24-dno == P155-s24!")
    check("I8c P155-lead-napoved meje 'pred s32' → dejansko s28 (A9!)",
          "s28" in d["frame"]["boundaries"].get("1890→1891", ""), "")

    # ---------- I9: mreže ----------
    x1 = next((x for x in d["crossChecks"] if x["id"] == "X1"), None)
    check("I9a X1 učiteljska-zamenjava (SMRT → KRST!)",
          bool(x1) and "DOKAZANA" in x1["detail"], "")
    r18 = next((e for e in ent if e["row"] == 18), None)
    check("I9b r18 h42 Straus-mreža #2 (1888-h72 + 1890-h42 + 1890-h71!)",
          bool(r18) and "STRAUS-MREŽA #2" in r18["whatSi"], "")
    x3 = next((x for x in d["crossChecks"] if x["id"] == "X3"), None)
    check("I9c X3 h30-dvojčki-smrti (3 dni + 9 dni = 5 dni razpona!)",
          bool(x3) and "5 DNI" in x3["detail"], "")
    r28 = next((e for e in ent if e["row"] == 28), None)
    r29 = next((e for e in ent if e["row"] == 29), None)
    check("I9d r28+r29 h30 Milek dojenčka (Slabost, junij)",
          bool(r28) and bool(r29) and r28["houseNo"] == "30" and r29["houseNo"] == "30"
          and "3 DNI" in r28["whatSi"] and "9 DNI" in r29["whatSi"], "")
    x6 = next((x for x in d["crossChecks"] if x["id"] == "X6"), None)
    check("I9e X6 Mertvod-leksikon ODRT (odrasli ×3 ≠ stillborn!)",
          bool(x6) and ("NERAZREŠEN" in x6["detail"] or "odprt" in x6["detail"].lower()), "")

    # ---------- I10: podpisi + duhovniki + rekordi ----------
    signed = [e for e in ent if e.get("duhovnik")]
    check("I10a podpisi 14/15 (Rauq ×12 + Šašelj ×2; BREZ ×1 r53)",
          len(signed) == 14
          and sum(1 for e in signed if "Rauq" in e["duhovnik"]) == 12
          and sum(1 for e in signed if "Šašelj" in e["duhovnik"]) == 2, "")
    r23 = next((e for e in ent if e["row"] == 23), None)
    check("I10b r23 ŠAŠELJ-Adlešiči (1. zunanji duhovnik linije!)",
          bool(r23) and "ŠAŠELJ" in r23["whatSi"] and "ADLEŠIČIH" in r23["whatSi"], "")
    ages = [e["starost"] for e in ent]
    check("I10c razpon 2 uri → 53 let (najkrajši r10; najstarejši r34)",
          "2 uri" in ages and "53 let" in ages, str(ages))
    # otroška umrljivost ≤ 3 leta + mrtvorojen = 11/15 = 73 %
    def mla(e):
        s = e["starost"]
        if s == "— (celica črtica)":  # r53 mrtvorojen — šteje kot otroška smrt
            return True
        if "uri" in s or "dni" in s or "mesecev" in s:
            return True
        if s.startswith(("1½", "2 leti", "2¾", "3 leta")):
            return True
        return False
    check("I10d otroška umrljivost 11/15 = 73 % (≤3 leta ×10 + mrtvorojen ×1 — najhujše leto linije!)",
          sum(1 for e in ent if mla(e)) == 11, str([e["starost"] for e in ent if mla(e)]))

    # ---------- I11: meja 1891 + lead-1891 + glave ----------
    b = d["frame"]["boundaries"]
    check("I11 meja 1890/1891 = »1891« inline na s28 (2 skena prej kot napoved!)",
          "s28" in b.get("1890→1891", "") and "1891" in b.get("1890→1891", ""), "")
    check("I11b lead-1891 = Ana Schweiger Vranoviče 11 (P157!)",
          "Schweiger" in b.get("lead-1891", "") and "Vranoviče 11" in b.get("lead-1891", ""), "")
    check("I11c glave »Leto 1890.« izpisane 4/4 (frame.glave)",
          "1890" in d["frame"].get("glave", "") and "4/4" in d["frame"].get("glave", ""), "")

    # ---------- I12: qa + README + notes ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p156 obstaja", "qa-p156-parish-death-1890" in qa, "")
    check("I12b qa-p155 guard 1895 (posodobljeno P160)", "1901+-mrliški bloki že v korpusu" in qa, "")
    readme = open(README, encoding="utf-8").read()
    check("I12c README P156", "P156" in readme and "1890" in readme, "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I12d notes obstajajo (učiteljska-zamenjava + Mrtvorojeno)",
          "učiteljska zamenjava" in notes and "Mrtvorojeno" in notes, "")

    # ---------- izpis ----------
    fails = [r for r in results if not r[1]]
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}" + (f" — {detail}" if detail and not ok else ""))
    print(f"\nSKUPAJ: {len(results) - len(fails)}/{len(results)} PASS")
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
