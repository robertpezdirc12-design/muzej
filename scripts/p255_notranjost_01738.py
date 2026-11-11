#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P255 — verifikator NOTRANJOSTI-01738: ZAČETEK = leto 1828 (I1–I10 + --live).
Korpus 2023 → 2026 (+3 bloki 1828: h6-m6 + h61/h22-m13 polni dvojni!);
korpus-prvi-vpis 1857 → 1828; šest-knjižne 9 → 12; dokaz parish-marriage-notranjost-1828.json."""
import json
import re
import sys
import base64
import hashlib
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

# ——— I1: 3 bloki 1828/01738 (h6 + h61 + h22 — file-order!) ———
bloki1828 = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "01738",\s*year: 1828,', src)
check("I1 bloki-01738/1828 == [6,61,22] (m6 + m13-polni-dvojni!)", bloki1828 == ["6", "61", "22"], ",".join(bloki1828))
check("I1b m13 = dva bloka s3 (scan: 3-×2!)", src.count('bookSignature: "01738",\n    year: 1828,\n    scan: 3,') == 2, "-")

# ——— I2: korpus 2026 + 01738 == 14 + korpus-prvi-vpis 1828 ———
vseh = re.findall(r'bookSignature: "01738"', src)
skupaj = len(re.findall(r'bookSignature: "', src))
leta = [int(y) for y in re.findall(r'bookSignature: "[^"]+",\s*year: (\d+)', src)]
check("I2 vitals == 2059 + 01738 == 47 + korpus-prvi-vpis == 1828",
      "HOUSE_VITALS.length !== 2059" not in src and len(vseh) == 47 and skupaj == 2059 and min(leta) == 1828,
      f"01738={len(vseh)} skupaj={skupaj} min-leto={min(leta)}")

# ——— I3: modul PREDHODNIK_1828_* (10 izvozov) ———
exports = ["PREDHODNIK_1828_BLOCKS", "PREDHODNIK_1828_HOUSES", "PREDHODNIK_1828_TOTAL",
           "PREDHODNIK_1828_STEVILCENIH", "PREDHODNIK_1828_NESTEVILCENIH", "PREDHODNIK_1828_BLOCKI",
           "PREDHODNIK_1828_ODPIRANJE", "PREDHODNIK_1828_NESTEVILCENE", "PREDHODNIK_1828_NITI",
           "PREDHODNIK_1828_KORPUS"]
manjka = [e for e in exports if f"export const {e}" not in early]
check("I3 modul parish-marriage-early P255-sekcija (10 izvozov)", not manjka, f"manjka: {manjka}" if manjka else "×10")
check("I3b števci 16/13/3/3 + korpus 2026/14",
      "PREDHODNIK_1828_TOTAL = 16" in early and "PREDHODNIK_1828_STEVILCENIH = 13" in early
      and "PREDHODNIK_1828_NESTEVILCENIH = 3" in early and "PREDHODNIK_1828_BLOCKI = 3" in early
      and "vitalsTotal: 2026" in early and "byBook01738: 14" in early, "-")  # P256: 1828-snapshot ostaja!

# ——— I4: zgodbe — naslovnica + množični-dan-×7 + MUZ-duplikat + niti ———
seg = early[early.find("P255: NOTRANJOST"):]
check("I4 ODPIRANJE: NASLOVNICA + RESTART-KNJIGE-z-1 + 6.-Feber-×7",
      "NASLOVNICA" in seg and "RESTART-KNJIGE-z-1" in seg and "6. Feber ×7" in seg
      and "m1 = 20. Jänner 1828" in seg, "-")
check("I4b NEŠTEVILČENE: MUZ-vrstica + DUPLIKAT-m9 + krvno-sorstvo + svinčnik-✓",
      "DUPLIKAT-m9-kand" in seg and "krvno-sorstvo-MUZ×MUZ" in seg
      and "'Gel. Disp. halb extra'" in seg and "svinčnik-'✓'" in seg, "-")
check("I4c NITI: MUZ-×4 + TILLAR-×2 + STARA-×2 + KRIŽAN-oče + BROD-IN-CROATIA",
      "MUZ-×4" in seg and "TILLAR-×2" in seg and "STARA-×2" in seg
      and "KRIŽAN-oče-m13" in seg and "BROD-IN-CROATIA" in seg, "-")

# ——— I5: dvigi-firstYear v blokih (32/41/34) ———
check("I5 dvigi: h6-32 + h22-41-ABSOLUTNI-REKORD + h61-34",
      "DVIG-ZA-32-LET" in src and "DVIG-ZA-41-LET = ABSOLUTNI-REKORD-DVIGA-MATRIČNE-LINIJE" in src
      and "DVIG-ZA-34-LET" in src and "prej-h43-34-P250" in src, "-")

# ——— I6: hišne zgodbe regenerirane (12 šest-knjižnih + h6-96 + bothEra 13) ———
check("I6 stories: SIX-×31 + h6-36-bl-96-let + bothEraPorocna-34 + blocks-2043",
      stories.count('houseNo: "') >= 31 and 'blocks: 2059,' in stories
      and "bothEraPorocna: 34" in stories and 'houseNo: "6", kind: "griblje", blocks: 36, books: 6' in stories
      and "firstYear: 1828" in stories and "longestSpan: 96" in stories
      and "longestSpanHouses: [\"6\"]" in stories
      and stories.count('export const HOUSE_STORY_SIX') == 1
      and len(re.findall(r'houseNo: "\d+", blocks: \d+, years: "1828–\d+"', stories)) == 3, "-")  # P256: 1828-šest-knjižne ostanejo 3!
pt = json.load(open(f"{ROOT}/research/issue17/parish-house-stories.json", encoding="utf-8"))
check("I6b dokaz-stories: 100-hiš + tiers-six-31 + stories-31 (P258!)",
      len(pt.get("houses", [])) == 100 and pt["structure"]["tiers"]["six"] == 31
      and len(pt["sixBookHouses"]["stories"]) == 31, "-")

# ——— I7: qa-p255 (249.) + živa kontrola ———
check("I7 qa-p255-notranjost kontrola obstaja + korpus-prvi-vpis-živo",
      '"qa-p255-parish-marriage-notranjost-01738-1828"' in qa
      and "korpus-prvi-vpis ≠ 1828" in qa and "HOUSE_VITALS ≠ 2043" in qa, "-")

# ——— I8: UI Notranjost01738Zacetek (komponenta + render + uvozi) ———
check("I8 UI Notranjost01738Zacetek (komponenta + render + uvozi-×10)",
      "function Notranjost01738Zacetek" in ui and "<Notranjost01738Zacetek />" in ui
      and "PREDHODNIK_1828_ODPIRANJE" in ui and "PREDHODNIK_1828_KORPUS" in ui, "-")

# ——— I9: dokaz-notranjost-1828.json (16 vrstic + šiv-struktura) ———
ev = json.load(open(f"{ROOT}/research/issue17/parish-marriage-notranjost-1828.json", encoding="utf-8"))
check("I9 dokaz: 16-vrstic + 13-številčenih + 3-neštevilčenih + 3-bloki + niti",
      len(ev.get("entries", [])) == 16 and ev["struktura"]["stevilcenih"] == 13
      and ev["struktura"]["nestevilcenih"] == 3 and ev["struktura"]["bloki"] == 3
      and ev["korpusUcinek"]["sestKnjiznih"] == "9 → 12 (h6/h22/h61!)"
      and ev["korpusUcinek"]["najdaljsiRazpon"] == "66 → 96 (h6 = 1828–1924!)", "-")

# ——— I10: LIVE Matricula-01738 + pt-luknja-2026 ———
pt2 = json.load(open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8"))
check("I9b pt-luknja-2059/20438:31",
      pt2.get("vitalsTotal") == 2059 and pt2.get("corpus", {}).get("byBook", {}).get("01738") == 47, "-")
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
