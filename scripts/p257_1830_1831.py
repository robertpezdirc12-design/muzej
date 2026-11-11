#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — verifikator NOTRANJOSTI-01738: LETO 1830/1831 (I1–I10 + --live).
Korpus 2032 → 2043 (+11 blokov: 1×1830-h22 + 10×1831!); šest-knjižne 16 → 23; bothEra 17 → 26;
10 dvigov (h54-37 = 2. vseh časov!); PEZDIRC-NIT-h50-42-let; ANOMALIJA-m7-Maria-Pödiz.
Dokaza: parish-marriage-notranjost-1830.json + parish-marriage-notranjost-1831.json."""
import json
import re
import sys
import base64
import urllib.request

ROOT = "/home/z/my-project"
OK = 0
FAIL = 0


def check(name, ok, msg=""):
    global OK, FAIL
    if ok:
        OK += 1
        print(f"[PASS] {name}" + (f" — {msg}" if msg else ""))
    else:
        FAIL += 1
        print(f"[FAIL] {name}" + (f" — {msg}" if msg else ""))


src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
early = open(f"{ROOT}/src/data/atlas/parish-marriage-early.ts", encoding="utf-8").read()
stories = open(f"{ROOT}/src/data/atlas/parish-house-stories.ts", encoding="utf-8").read()
qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
ui = open(f"{ROOT}/src/components/museum/museum-atlas.tsx", encoding="utf-8").read()

# ——— I1: 11 blokov 1830/1831/01738 (h22-1830 + h3/h33/h50/h54/h56/h26/h27/h65/h1/h11-1831 — file-order!) ———
bloki1830 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1830,', src)
check("I1 bloki-01738/1830 == [22] (m4-Anna-Milek!)",
      bloki1830 == ["22"], ",".join(bloki1830))
bloki1831 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1831,', src)
check("I1b bloki-01738/1831 == [3,33,50,54,56,26,27,65,1,11] (5-POLNIH-DVOJNIH!)",
      bloki1831 == ["3", "33", "50", "54", "56", "26", "27", "65", "1", "11"], ",".join(bloki1831))
check("I1c foliacija: Pag. 9/11 (2·sken−3 ×7)",
      'page: 9,' in src and 'page: 11,' in src, "-")

# ——— I2: korpus 2043 + 01738 == 31 + korpus-prvi-vpis == 1828 (ostaja!) ———
vseh = re.findall(r'bookSignature: "01738"', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta = [int(y) for y in re.findall(r'bookSignature: "[^"]+",\s*year: (\d+)', src)]
check("I2 vitals == 2043 + 01738 == 31 + korpus-prvi-vpis == 1828",
      "HOUSE_VITALS.length !== 2043" not in src and len(vseh) == 31 and skupaj == 2043 and min(leta) == 1828,
      f"01738={len(vseh)} skupaj={skupaj} min-leto={min(leta)}")

# ——— I3: modul PREDHODNIK_1830_* (8) + PREDHODNIK_1831_* (6) + PREDHODNIK_257_KORPUS ———
exports1830 = ["PREDHODNIK_1830_BLOCKS", "PREDHODNIK_1830_HOUSES", "PREDHODNIK_1830_TOTAL",
               "PREDHODNIK_1830_BLOCKI", "PREDHODNIK_1830_STRUNA", "PREDHODNIK_1830_VPISI",
               "PREDHODNIK_1830_KORPUS"]
exports1831 = ["PREDHODNIK_1831_BLOCKS", "PREDHODNIK_1831_HOUSES", "PREDHODNIK_1831_TOTAL",
               "PREDHODNIK_1831_BLOCKI", "PREDHODNIK_1831_STRUNA", "PREDHODNIK_1831_NITI",
               "PREDHODNIK_1831_KRAJI", "PREDHODNIK_257_KORPUS"]
manjka = [e for e in exports1830 + exports1831 if f"export const {e}" not in early]
check("I3 modul parish-marriage-early P257-sekcija (8+8 izvozov)", not manjka, f"manjka: {manjka}" if manjka else "×16")
check("I3b števci 8/1 + 13/10 + korpus 2043/31",
      "PREDHODNIK_1830_TOTAL = 8" in early and "PREDHODNIK_1830_BLOCKI = 1" in early
      and "PREDHODNIK_1831_TOTAL = 13" in early and "PREDHODNIK_1831_BLOCKI = 10" in early
      and "vitalsTotal: 2043" in early and "byBook01738: 31" in early, "-")

# ——— I4: STRUNA + NITI + KRAJI + VPISI ———
seg = early[early.find("P257: NOTRANJOST"):]
check("I4 STRUNA-1830: množični-dan-17.2.×4 + PRAZNA + METLIKA-140 + RESTART-12.1.",
      "17. Febr-×4-MNOŽIČNI-DAN" in seg and "II-POLONICA-PRAZNA" in seg
      and "METLIKA-140" in seg and "12. Jänner 1830" in seg, "-")
check("I4b STRUNA-1831: 13-POROK-V-15-DNEH + ANOMALIJA-VRSTICA + d°-×10",
      "13-POROK-V-15-DNEH" in seg and "ANOMALIJA-VRSTICA" in seg and "d°-×10" in seg, "-")
check("I4c NITI-1831: PEZDIRC-NIT-h50 + 42-LET + MARCO-PESDIRZ + KRIŽAN×2 + MILEK-h65 + MUZ + KAMBIC",
      "PEZDIRC-NIT-h50" in seg and "ISTA-DRUŽINA-42-LET" in seg and "MARCO-PESDIRZ" in seg
      and "KRIŽAN-×2-v-m1" in seg and "MILEK-h65" in seg and "MUZ-oče-m12" in seg and "KAMBIC" in seg, "-")
check("I4d KRAJI-1831: 10-GRIBLJE-hiš-v-1-letu + VPISI-1830: Anna-MILEK + BORŠT-20",
      "10-GRIBLJE-HIŠ-V-1-LETU" in seg and "Anna-MILEK-GRIBLJE-22" in seg and "BORŠT-20" in seg, "-")

# ——— I5: dvigi-firstYear v blokih + PEZDIRC-NIT ———
check("I5 dvigi: h54-37 (2.-VSEH-ČASOV!) + h56-36 + h27-33 + h11-32 + h1-30 + h26/h33-28 + h3/h50-27 + h65-26",
      "DVIG-ZA-37-LET" in src and "DVIG-ZA-36-LET" in src and "DVIG-ZA-33-LET" in src
      and "DVIG-ZA-32-LET" in src and "DVIG-ZA-30-LET" in src and src.count("DVIG-ZA-28-LET") >= 2
      and src.count("DVIG-ZA-27-LET") >= 2 and "DVIG-ZA-26-LET" in src, "-")
check("I5b PEZDIRC-NIT-h50-42-let (Marco-Pesdirz-1831 ↔ Marcus-Pegdire-1873!) + KRIŽAN-×2",
      "ISTA-DRUŽINA-42-LET" in src and "MARCO PESDIRZ" in src
      and "KRIŽAN-×2-V-ENI-VRSTICI" in src and "Dorothea KRIŽAN" in src, "-")
check("I5c ANOMALIJA-m7 + h22-3-zaporedno-leto (Miller/Milek-DVOJMA!)",
      "ŽENSKO-IME-V-ŽENINSKEM-STOLPCU" in src and "3-ZAPOREDNA-LETA-NEVEST-IZ-h22" in src
      and "TRI-LETA-V-ZAPOREDJU" in src and "Miller-ali-Milek" in src, "-")
check("I5d h65-BILA-PRVA-HIŠA-KORPUSA-1857 + MILEK-h65-NIT-43-let",
      "h65-BILA-PRVA-HIŠA-KORPUSA-1857" in src and "43-LET-družinska-continuiteta" in src, "-")

# ——— I6: hišne zgodbe regenerirane (SIX-23 + bothEra-26 + h50-span-93!) ———
check("I6 stories: SIX-×23 + blocks-2043 + bothEraPorocna-26 + tierji-23/41",
      stories.count('houseNo: "') >= 23 and 'blocks: 2043,' in stories
      and "bothEraPorocna: 26" in stories and "sixBook: 23" in stories
      and "fiveBook: 41" in stories and "longestSpan: 96" in stories
      and 'longestSpanHouses: ["6"]' in stories
      and len(re.findall(r'firstYear: 1831, lastYear', stories)) == 10, "-")
h50m = re.search(r'houseNo: "50", kind: "griblje", blocks: 12, books: 5.*?firstYear: 1831, lastYear: 1924, span: 93', stories)
check("I6b h50-story: 12-blokov-1831–1924-span-93 (3.-mesto!)",
      bool(h50m), "-" if h50m else "h50-ni-tako")
h65m = re.search(r'houseNo: "65", kind: "griblje", blocks: 44, books: 6.*?firstYear: 1831, lastYear: 1914, span: 83', stories)
check("I6c h65-story: 44-blokov-1831–1914-span-83 (2.-najglasnejša!)",
      bool(h65m), "-" if h65m else "h65-ni-tako")
pt = json.load(open(f"{ROOT}/research/issue17/parish-house-stories.json", encoding="utf-8"))
check("I6d dokaz-stories: 100-hiš + tiers-six-23 + stories-23 + P257-lifts",
      len(pt.get("houses", [])) == 100 and pt["structure"]["tiers"]["six"] == 23
      and len(pt["sixBookHouses"]["stories"]) == 23
      and pt["records"]["firstYearLiftsP257"]["h54"] == 37, "-")

# ——— I7: qa-p257 (251.) + živa kontrola ———
check("I7 qa-p257-notranjost kontrola obstaja + korpus-prvi-vpis-živo",
      '"qa-p257-parish-marriage-notranjost-01738-1830-1831"' in qa
      and "korpus-prvi-vpis ≠ 1828" in qa and "HOUSE_VITALS.length !== 2043" in qa, "-")

# ——— I8: dokaza JSON (1830: 8 + 1831: 13) ———
d30 = json.load(open(f"{ROOT}/research/issue17/parish-marriage-notranjost-1830.json", encoding="utf-8"))
d31 = json.load(open(f"{ROOT}/research/issue17/parish-marriage-notranjost-1831.json", encoding="utf-8"))
check("I8 dokaz-1830 (8-entries + md5-s6 + METLIKA + BORŠT-20)",
      len(d30["entries"]) == 8 and "593ac8c7" in d30["vir"]["md5"]
      and d30["entries"][3]["nevesta"] == "Anna MILEK"
      and "BORŠT" in d30["entries"][6]["vas_neveste"] and "METLIKA" in json.dumps(d30["korpusUcinek"]), "-")
check("I8b dokaz-1831 (13-entries + md5-s7 + PESDIRZ-m2 + ANOMALIJA-m7 + dvigi-10)",
      len(d31["entries"]) == 13 and "d19294a6" in d31["vir"]["md5"]
      and "PESDIRZ" in d31["entries"][1]["zenin"] and "MARCO PESDIRZ" in d31["entries"][1]["starši_zenin"]
      and "ŽENSKO-IME-V-ŽENINSKEM-STOLPCU" in d31["entries"][6]["zenin"]
      and len(d31["korpusUcinek"]["dvigi"]) == 10, "-")

# ——— I9: UI Notranjost01738Leto1830_1831 (komponenta + render + uvozi ×16) ———
check("I9 UI-Notranjost01738Leto1830_1831 (komponenta + render + uvozi)",
      "function Notranjost01738Leto1830_1831" in ui and "<Notranjost01738Leto1830_1831 />" in ui
      and "PREDHODNIK_1830_STRUNA" in ui and "PREDHODNIK_257_KORPUS" in ui
      and "PREDHODNIK_1831_NITI" in ui, "-")
check("I9b HouseStoriesP254-regresija (obe-eri-26-tekst)",
      "poročita v OBEH" in ui or "bothEra" in ui or "šest-knjiž" in ui, "-")

# ——— I10: pt-luknja + LIVE ———
pt2 = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I10 pt-luknja-2043/01738:31 (P257!)",
      pt2.get("vitalsTotal") == 2043 and pt2.get("corpus", {}).get("byBook", {}).get("01738") == 31
      and pt2.get("corpus", {}).get("byBook", {}).get("04455") == 269, "-")

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    # LIVE: matrica-HTTP + inventar + /api/qa
    try:
        req = urllib.request.Request(
            "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/",
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=60) as r:
            html = r.read().decode("utf-8", "ignore")
        urls = []
        for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', html):
            s = m.group(1)[7:-1]
            try:
                d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                if d.startswith("http"):
                    urls.append(d)
            except Exception:
                pass
        check("I10b LIVE-matricula-01738-HTTP-200 + inventar-147-1:1 + s6/s7-URL",
              r.status == 200 and len(set(urls)) == 147 and len(urls) >= 6 and len(urls) >= 7,
              f"status={r.status} inventar={len(set(urls))}")
    except Exception as e:
        check("I10b LIVE-matricula", False, str(e)[:80])
    try:
        r = urllib.request.Request("http://localhost:3000/api/qa")
        with urllib.request.urlopen(r, timeout=60) as resp:
            qa_data = json.load(resp)
        p257 = [q for q in qa_data.get("tests", []) if q.get("id", "").startswith("qa-p257")]
        check("I10c LIVE-/api/qa 251/251 ok:True (+qa-p257-id!)",
              qa_data.get("ok") is True and qa_data.get("passed") == 251 and qa_data.get("failed") == 0
              and len(p257) == 1 and p257[0].get("pass") is True,
              f"passed={qa_data.get('passed')} p257={len(p257)}")
    except Exception as e:
        check("I10c LIVE-/api/qa", False, str(e)[:80])

print()
if FAIL == 0:
    print(f"VSI PASS ({OK}/{OK})")
    sys.exit(0)
print(f"REZULTAT: {OK} PASS / {FAIL} FAIL — POPRAVI!")
sys.exit(1)
