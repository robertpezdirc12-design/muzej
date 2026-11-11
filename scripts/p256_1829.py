#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P256 — verifikator NOTRANJOSTI-01738: NADALJEVANJE = leto 1829 (I1–I10 + --live).
Korpus 2026 → 2032 (+6 blokov 1829: h32/h20-m2 + h5/h19-m10 + h62/h22-m18!);
šest-knjižne 12 → 16; bothEra-poročna 13 → 17; dokaz parish-marriage-notranjost-1829.json."""
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

# ——— I1: 6 blokov 1829/01738 (h32 + h20 + h5 + h19 + h62 + h22 — file-order!) ———
bloki1829 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1829,', src)
check("I1 bloki-01738/1829 == [32,20,5,19,62,22] (m2+m10+m18 — 3 polni dvojni!)",
      bloki1829 == ["32", "20", "5", "19", "62", "22"], ",".join(bloki1829))
check("I1b m2/m10/m18 = pari z istim scanom (4/5/6)",
      src.count('bookSignature: "01738",\n    year: 1829,\n    scan: 4,') == 2
      and src.count('bookSignature: "01738",\n    year: 1829,\n    scan: 5,') == 2
      and src.count('bookSignature: "01738",\n    year: 1829,\n    scan: 6,') == 2, "-")
check("I1c foliacija: Pag. 5/7/9 (2·sken−3)",
      'page: 5,' in src and 'page: 7,' in src and 'page: 9,' in src, "-")

# ——— I2: korpus 2032 + 01738 == 20 + korpus-prvi-vpis 1828 (ostaja!) ———
vseh = re.findall(r'bookSignature: "01738"', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta = [int(y) for y in re.findall(r'bookSignature: "[^"]+",\s*year: (\d+)', src)]
check("I2 vitals == 2043 + 01738 == 31 + korpus-prvi-vpis == 1828",
      "HOUSE_VITALS.length !== 2043" not in src and len(vseh) == 31 and skupaj == 2043 and min(leta) == 1828,
      f"01738={len(vseh)} skupaj={skupaj} min-leto={min(leta)}")

# ——— I3: modul PREDHODNIK_1829_* (9 izvozov) ———
exports = ["PREDHODNIK_1829_BLOCKS", "PREDHODNIK_1829_HOUSES", "PREDHODNIK_1829_TOTAL",
           "PREDHODNIK_1829_BLOCKI", "PREDHODNIK_1829_STRUNA", "PREDHODNIK_1829_KRAJI",
           "PREDHODNIK_1829_NITI", "PREDHODNIK_1829_RESTART1830", "PREDHODNIK_1829_KORPUS"]
manjka = [e for e in exports if f"export const {e}" not in early]
check("I3 modul parish-marriage-early P256-sekcija (9 izvozov)", not manjka, f"manjka: {manjka}" if manjka else "×9")
check("I3b števci 20/6 + korpus 2032/20 + h22dvojni",
      "PREDHODNIK_1829_TOTAL = 20" in early and "PREDHODNIK_1829_BLOCKI = 6" in early
      and "vitalsTotal: 2032" in early and "byBook01738: 20" in early
      and "h22dvojni:" in early and "2-letni-zapored-Millerjevih-nevest" in early, "-")

# ——— I4: STRUNA + KRAJI + RESTART ———
seg = early[early.find("P256: NOTRANJOST"):]
check("I4 STRUNA: MNOŽIČNI-DAN-4.×4 + RESTART-1830 + foliacija-2·sken−3",
      "MNOŽIČNI-DAN-den-4.-Febr-×4" in seg and "RESTART-1830 na s6-r4" in seg
      and "2·sken−3" in seg and "letnica-'1829'-NAD-vrstico" in seg, "-")
check("I4b KRAJI: 1.-BORŠT + 1.-KAPLJA-VAS + KRAMARIČ×JURJEVIČ-križ",
      "BORŠT-m16-h18" in seg and "KAPLJA-VAS-m17-h7" in seg
      and "KRIŽNO" in seg and "13-garble-VASI-X-OPEN" in seg, "-")
check("I4c RESTART1830: 12. Jänner + PRAZNA-polovica + s7-1831",
      "12. Jänner 1830" in seg and "PRAZNA" in seg and "s7 = 1831" in seg, "-")

# ——— I5: dvigi-firstYear v blokih (35/34/30/30/29) ———
check("I5 dvigi: h62-35-NAJVEČJI + h32-34-DUEL + h5/h20-30 + h19-29 + h22-2.-blok",
      "DVIG-ZA-35-LET" in src and "DVIG-ZA-34-LET" in src
      and src.count("DVIG-ZA-30-LET") >= 2 and "DVIG-ZA-29-LET" in src
      and "2-letni-zapored-Millerjevih-nevest" in src, "-")
check("I5b KRIŽAN-1829 + HRIŽAN-1873-ŠIV = ISTA-HIŠA-44-LET",
      "KRIŽAN-h62-ŽENIN-1829 + HRIŽAN-h62-NEVESTA-1873-ŠIV" in src
      and "THE-SAME-HOUSE-44-YEARS" in src, "-")

# ——— I6: hišne zgodbe regenerirane (16 šest-knjižnih + h62-95 + bothEra 17) ———
check("I6 stories: SIX-×23 + blocks-2043 + bothEraPorocna-26 + tierji-23/41",
      stories.count('houseNo: "') >= 23 and 'blocks: 2043,' in stories
      and "bothEraPorocna: 26" in stories and "sixBook: 23" in stories
      and "fiveBook: 41" in stories and "firstYear: 1829" in stories
      and "longestSpan: 96" in stories and 'longestSpanHouses: ["6"]' in stories
      and len(re.findall(r'houseNo: "\d+", blocks: \d+, years: "1829–\d+"', stories)) == 5, "-")
h62m = re.search(r'houseNo: "62", kind: "griblje", blocks: 29, books: 6.*?firstYear: 1829, lastYear: 1924, span: 95', stories)
check("I6b h62-story: 29-blokov-1829–1924-span-95 (2.-najdaljši!)",
      bool(h62m), "-" if h62m else "h62-ni-tako")
h20m = re.search(r'houseNo: "20", kind: "griblje", blocks: 35, books: 6.*?firstYear: 1829, lastYear: 1922, span: 93', stories)
check("I6c h20-story: 35-blokov-1829–1922-span-93 (izenači-h22!)",
      bool(h20m), "-" if h20m else "h20-ni-tako")
pt = json.load(open(f"{ROOT}/research/issue17/parish-house-stories.json", encoding="utf-8"))
check("I6d dokaz-stories: 100-hiš + tiers-six-23 + stories-23 + bothEra-26 (P257!)",
      len(pt.get("houses", [])) == 100 and pt["structure"]["tiers"]["six"] == 23
      and len(pt["sixBookHouses"]["stories"]) == 23
      and pt["records"]["firstYearLiftsP256"]["h62"] == 35, "-")

# ——— I7: qa-p256 (250.) + živa kontrola ———
check("I7 qa-p256-notranjost kontrola obstaja + korpus-prvi-vpis-živo",
      '"qa-p256-parish-marriage-notranjost-01738-1829"' in qa
      and "korpus-prvi-vpis ≠ 1828" in qa and "HOUSE_VITALS.length !== 2043" in qa, "-")

# ——— I8: UI Notranjost01738Leto1829 (komponenta + render + uvozi) ———
check("I8 UI Notranjost01738Leto1829 (komponenta + render + uvozi-×9)",
      "function Notranjost01738Leto1829" in ui and "<Notranjost01738Leto1829 />" in ui
      and "PREDHODNIK_1829_STRUNA" in ui and "PREDHODNIK_1829_KORPUS" in ui
      and "16 šest-knjižnih hiš" in ui, "-")

# ——— I9: dokaz-notranjost-1829.json (20 vrstic + restart1830 + niti) ———
ev = json.load(open(f"{ROOT}/research/issue17/parish-marriage-notranjost-1829.json", encoding="utf-8"))
check("I9 dokaz: 20-vrstic + 6-blokov + restart1830 + niti-1829",
      len(ev.get("entries", [])) == 20 and ev["korpusUcinek"]["noviBloki"] == 6
      and ev["korpusUcinek"]["vitals"] == "2026 → 2032"
      and ev["restart1830"]["datum"] == "12. Jänner 1830"
      and "TILLAR" in ev["niti1829"] and "MALEŠIČ" in ev["niti1829"]
      and "PEZDIRC-kand" in ev["niti1829"]
      and ev["p257+"]["1831"].startswith("s7 (26. Jän 1831"), "-")

# ——— I10: LIVE Matricula-01738 + pt-luknja-2032 ———
pt2 = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I10b pt-luknja-2043/20438:31",
      pt2.get("vitalsTotal") == 2043 and pt2.get("corpus", {}).get("byBook", {}).get("01738") == 31, "-")
live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request(
            "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/01738/",
            headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8", "ignore")
            urls = []
            for m in re.finditer(r'"(/image/[A-Za-z0-9+/=]+/)"', body):
                s = m.group(1)[7:-1]
                try:
                    d = base64.b64decode(s + "=" * (-len(s) % 4)).decode("utf-8")
                    if d.startswith("http"):
                        urls.append(d)
                except Exception:
                    pass
            check("I10 LIVE matricula-01738 HTTP 200 + inventar-147-URL-1:1",
                  r.status == 200 and len(urls) == 147, f"status={r.status} urls={len(urls)}")
    except Exception as e:
        check("I10 LIVE matricula-01738", False, str(e)[:80])

print()
print(f"REZULTAT: {OK} PASS / {FAIL} FAIL" + (" — VSI PASS!" if FAIL == 0 else " — POPRAVI!"))
sys.exit(1 if FAIL else 0)
