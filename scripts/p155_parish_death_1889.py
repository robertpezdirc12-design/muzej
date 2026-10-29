#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P155 — MRLIŠKA knjiga 04894, leto 1889 = 4. polno leto mrliške linije
= NAJNIŽE leto (s21-dno + s22–s24 == str. 20–23; 36 vrstic / 8 Griblje-vpisov
= povratek na dno po rekordnem 1888 ×2.2!). (issue #18). ★★★ 92-letni REKORD
linije (r27 h55 Peter Šimec kolar — prej 80!) + ★★★ 2 krstna↔mrliška vezi
dojenčkov (h69 Janez 16 dni ← krst 1./2. 4. + h65 Barbara 13 dni ← krst
23. 11. — SKLAD NA DAN!) + ★★ h83 sib-swap (†Barbara 31.10. → krst Barbara
nov.!) + ★★ P154-LEAD-POPRAVEK starost 67 → 49 (marker-9 forenzika! VLM bere
9 kot 7!) + ★ ¼ ure (izenačen najkrajši!) + meja 1890 = INLINE (3. stil!).
Kumulativ: vitals 754 → 762, mrliški bloki 04894 55 → 63, p80 hiše 79 (0 novih
— h30/h48/h55 = 1. MRLIŠKI vpisi!). Vzorec p154."""
import json
import re
import sys
import time
import urllib.request
import urllib.error

DOKAZ = "research/issue17/parish-death-1889.json"
DOKAZ_P154 = "research/issue17/parish-death-1888.json"
BOOK_URL = "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04894/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; muzej-qa/1.0)"}
QA_TS = "src/lib/qa-parish.ts"
PARISH_TS = "src/data/atlas/parish.ts"
README = "README.md"
NOTES = "research/issue17/parish-death-1889-notes.md"

EXPECTED_ENTRIES = 8             # 1 P154-lead (popravljen!) + 7 novih
EXPECTED_EXCLUDED = 10           # skupine vrstic izven Gribelj + marker + 1890-okvir
EXPECTED_ANOMALIES = 8
EXPECTED_CROSSCHECKS = 10
GRIBLJE_HOUSES = "5,30,48,53,55,65,69,83"
VITALS_TOTAL = 809               # POSODABLJENO P158: 792 + 17!
BLOKI_04894 = 110                # POSODABLJENO P158: 93 + 17!
P80_HOUSES = 79                  # NESPREMENJENO (0 novih!)
NEW_SCANS = [21, 22, 23, 24]

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
    check("I1 dokaz obstaja + status", d.get("status") == "SAMPLE-TRANSCRIPTION-D1889", d.get("status", ""))
    check("I1b št. vpisov = 8", len(ent) == EXPECTED_ENTRIES, str(len(ent)))
    check("I1c izključene skupine = 10",
          len(d["excluded"]) == EXPECTED_EXCLUDED, str(len(d["excluded"])))
    check("I1d anomalije ×8 + križne ×10 + iskrenost ×10", (
        len(d["anomalies"]) == EXPECTED_ANOMALIES
        and len(d["crossChecks"]) == EXPECTED_CROSSCHECKS
        and len(d["honesty"]) == 10),
        f"anom {len(d['anomalies'])} cross {len(d['crossChecks'])} hon {len(d['honesty'])}")

    # ---------- I2: vrste, hiše, meseci ----------
    rows = [e["row"] for e in ent]
    check("I2 vrste naraščajoče (4,11,17,27,28,30,32,33)",
          rows == sorted(rows) and rows[0] == 4 and rows[-1] == 33, str(rows))
    houses = sorted((e["houseNo"] for e in ent), key=int)
    check("I2b hišni multizbroj = 8 različnih",
          ",".join(houses) == GRIBLJE_HOUSES, f"{len(set(houses))} različnih")
    months = {}
    for e in ent:
        months[e["mesec"]] = months.get(e["mesec"], 0) + 1
    check("I2c meseci (Jan 1 · Apr 1 · Jun 1 · Okt 2 · Nov 1 · Dec 2)",
          months == {"Januarj": 1, "April": 1, "Junij": 1, "Oktober": 2,
                     "November": 1, "December": 2}, str(months))

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
            check("I3c citirani skeni 4/4 JPEG 200", probes_ok, " ".join(det))

    # ---------- I4: preslikava stran == sken − 1 ----------
    check("I4 stran == sken − 1 (vseh 8)",
          all(e["page"] == e["scan"] - 1 for e in ent),
          str(sorted({(e["scan"], e["page"]) for e in ent})))
    check("I4b skeni v naboru 21+22+23+24",
          sorted({e["scan"] for e in ent}) == NEW_SCANS, "")

    # ---------- I5: hiše ----------
    vit = parse_house_vitals()
    uniq = sorted({e["houseNo"] for e in ent}, key=lambda x: float(x))
    check("I5 8 različnih hiš", len(uniq) == 8, ",".join(uniq))
    # h30/h48/h55 = 1. mrliški vpis (prej nič v 04894!)
    for h in ("30", "48", "55"):
        prej = [v for v in vit if v["bookSignature"] == "04894"
                and v["houseNo"] == h and (v["year"] or 0) < 1889]
        check(f"I5b h{h} = 1. mrliški vpis (prej 0 v 04894)", len(prej) == 0,
              f"prej {len(prej)}")

    # ---------- I6: parish.ts ----------
    d1889 = [v for v in vit if v["bookSignature"] == "04894" and v["year"] == 1889]
    d04894 = [v for v in vit if v["bookSignature"] == "04894"]
    check("I6a vitals 777 (P156)", len(vit) == VITALS_TOTAL, str(len(vit)))
    check("I6b mrliški bloki 04894 = 110 (P158)", len(d04894) == BLOKI_04894, str(len(d04894)))
    check("I6c bloki 1889 = 8", len(d1889) == 8, str(len(d1889)))
    check("I6d bloki 1889: skeni 21–24 + stran == sken − 1",
          all(v["scan"] and 21 <= v["scan"] <= 24 and v["page"] == v["scan"] - 1 for v in d1889), "")
    check("I6d2 bloki 1893+ ne obstajajo (P159-lead!; P158 = 1892 v korpusu!)",
          not [v for v in vit if v["bookSignature"] == "04894" and (v["year"] or 0) >= 1893], "")
    p80_script = open("scripts/p80_parish_md_books.py", encoding="utf-8").read()
    check("I6f p80-skripta pini 809 + 84", "len(vitals) == 809" in p80_script and "len(houses) == 84" in p80_script, "")
    # celotni korpus = 90 številskih hiš (p80-filtriranih 79 — tega preverja qa-p80!)
    houses_all = {v["houseNo"] for v in vit if v["houseNo"] and v["houseNo"].isdigit()}
    check("I6g korpus = 91 hiš (P158: +h80 EDINA — 1. korpusni dokaz!)",
          len(houses_all) == 91, str(len(houses_all)))

    # ---------- I7: max-zoom forenzika ----------
    r4 = next((e for e in ent if e["row"] == 4), None)
    check("I7a r4 = 49 let (P154-lead 67 POPRAVLJEN!)",
          bool(r4) and "49 let" in r4["whatSi"] and "67" in r4["whatSi"]
          and "P154-LEAD-POPRAVEK" in r4["whatSi"], "")
    r27 = next((e for e in ent if e["row"] == 27), None)
    check("I7b r27 = 92 let REKORD + h55 (DVE 5-formi!)",
          bool(r27) and "92 LET" in r27["whatSi"] and "REKORD LINIJE" in r27["whatSi"]
          and r27["houseNo"] == "55", "")
    r28 = next((e for e in ent if e["row"] == 28), None)
    check("I7c r28 = ¼ ure (izenačen rekord!) + sib-swap",
          bool(r28) and "¼ URE" in r28["whatSi"] and "SIB-SWAP" in r28["whatSi"], "")
    r32 = next((e for e in ent if e["row"] == 32), None)
    check("I7d r32 h65 (ne 68! začetna napaka) + krstna-vez",
          bool(r32) and r32["houseNo"] == "65" and "'68' NAPAČNA" in r32["whatSi"]
          and "KRSTNA↔MRLIŠKA VEZ #2" in r32["whatSi"], "")
    r33 = next((e for e in ent if e["row"] == 33), None)
    check("I7e r33 h48 = 1. mrliški vpis + ZADNJI 1889",
          bool(r33) and "1. MRLIŠKI vpis h48" in r33["whatSi"]
          and "ZADNJI gribeljski vpis 1889" in r33["whatSi"], "")

    # ---------- I8: P154-kontinuiteta ----------
    p154 = json.load(open(DOKAZ_P154))
    lead = next((e for e in ent if e["row"] == 4 and e["houseNo"] == "53"), None)
    check("I8a P154-lead r4 h53 potrjen + popravljen (67→49)",
          bool(lead) and lead["whatSi"].startswith("umrla Ana Perdihec"), "")
    p154_last = [e for e in p154["entries"] if e["row"] == 102]
    check("I8b P154 zadnji 1888 (r102 h3) se nadaljuje z 1889-r1 (s21-dno)",
          bool(p154_last) and lead["scan"] == 21, "s21-dno == P154-s21!")
    check("I8c P154-marker-9 = P155-starost-referenca (H-A1)",
          any("9 z dolgim repom" in str(x) for x in [p154["frame"]["boundaries"].get("1888→1889", "")]), "")

    # ---------- I9: krstna-vezi + sib-swap ----------
    x1 = next((x for x in d["crossChecks"] if x["id"] == "X1"), None)
    check("I9a X1 krstna↔mrliška h69 Janez (16 dni, SKLAD NA DAN!)",
          bool(x1) and "ISTI OTROK" in x1["detail"], "")
    r11 = next((e for e in ent if e["row"] == 11), None)
    check("I9b r11 h69 Janez Brinec 16 DNI + VEZ #1 v whatSi",
          bool(r11) and "16 DNI" in r11["whatSi"] and "KRSTNA↔MRLIŠKA VEZ #1" in r11["whatSi"], "")
    x2 = next((x for x in d["crossChecks"] if x["id"] == "X2"), None)
    check("I9c X2 krstna↔mrliška h65 Barbara (13 dni, SKLAD NA DAN!)",
          bool(x2) and "ISTA OTROK" in x2["detail"], "")
    x3 = next((x for x in d["crossChecks"] if x["id"] == "X3"), None)
    check("I9d X3 h83 sib-swap (†31.10. → krst nov.!)",
          bool(x3) and "sib-swap" in x3["name"] and "imenska naslednica" in x3["detail"], "")

    # ---------- I10: podpisi + vzroki + rekordi ----------
    signed = [e for e in ent if e.get("duhovnik")]
    check("I10a podpisi 5/8 (Andrej Glibe polni ×1 + Antn. ×1 + Romey ×3; BREZ ×3)",
          len(signed) == 5
          and sum(1 for e in signed if "Andrej Glibe" in e["duhovnik"]) == 1
          and sum(1 for e in signed if "Antn. Glibe" in e["duhovnik"]) == 1
          and sum(1 for e in signed if "Romey" in e["duhovnik"]) == 3,
          str([(e["row"], e["duhovnik"]) for e in signed]))
    r27 = next((e for e in ent if e["row"] == 27), None)
    check("I10b vzrok Vodenica ×2 (r27 + r30) + KOLAR (2. linije!)",
          sum(1 for e in ent if "Vodenica" in e["bolezen"]) == 2
          and "KOLAR" in r27["whatSi"], "")
    ages = [e["starost"] for e in ent]
    check("I10c razpon 13 dni → 92 let (REKORD!)",
          "92 let" in ages and "16 dni" in ages and "13 dni" in ages, str(ages))
    check("I10d 'sv. olje' = 2. izpisani sakrament linije (r4)",
          "sv. olje" in r4["whatSi"] and "2. izpisani sakrament" in r4["whatSi"], "")

    # ---------- I11: meja 1890 + lead-1890 + glave ----------
    b = d["frame"]["boundaries"]
    check("I11 meja 1889/1890 = INLINE »1890.« (3. stil!)",
          "INLINE »1890.«" in b.get("1889→1890", ""), "")
    check("I11b lead-1890 = h90 učitelj (P156!)",
          "učitelj" in b.get("lead-1890", "") and "h90" in b.get("lead-1890", ""), "")
    check("I11c glave s22–s24 izpisane (frame.glave)",
          "Leto 1889" in d["frame"].get("glave", ""), "")

    # ---------- I12: qa + README + notes ----------
    qa = open(QA_TS, encoding="utf-8").read()
    check("I12 qa-p155 obstaja", "qa-p155-parish-death-1889" in qa, "")
    check("I12b qa-p154 guard 1891 (posodobljeno)", "1892+-mrliški bloki že v korpusu" in qa, "")
    readme = open(README, encoding="utf-8").read()
    check("I12c README P155", "P155" in readme and "1889" in readme, "")
    notes = open(NOTES, encoding="utf-8").read()
    check("I12d notes obstajajo (marker-9 referenca)",
          "marker-9" in notes and "SKLAD NA DAN" in notes, "")

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
