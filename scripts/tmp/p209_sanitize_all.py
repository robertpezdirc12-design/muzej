#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P209 — INSERT qa-p209 + sanitizacija (1557→1511, 279→292, yearset +1868) + verifier-patch + pt-luknja + krstne-izjeme."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p208: MRLIŠKA PREDZGODOVINA 04106 — leto 1869 = 17. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p209-parish-death-1868-04106" not in src
BLOCK = '''
  // ——— qa-p209: MRLIŠKA PREDZGODOVINA 04106 — leto 1868 = 18. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1868 = 80 vpisov (ordinali-1–80 ČISTO — 3.-leto-
  //      zapored!) / 13 Griblje / 11 hiš (h54-×2 + h13-×2) + ★★★ MEJA-1867/68-s69
  //      (tail-×1-ULEDBA + 'vsota'-4-DELNA-'1|8|6|8'-1.×! + restart-'1.-Jänner-1868'!)
  //      + 'nožgodanujeleg'-ANOMALIA-z61 + z77/z78-2-smrti-v-1-dnevu.
  //      Dokaz: parish-death-1868-04106.json; skripte p209.
  {
  const p209Errors: string[] = [];
  const p209Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1868);
  if (p209Death.length !== 13)
    p209Errors.push(`bloki 1868 (04106) ≠ 13 (${p209Death.length} — 13 Griblje-vpisov / 80 vpisov vrstno-štetje!)`);
  const p209Houses = p209Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p209Houses.join(",") !== "10,13,13,15,26,36,41,50,54,54,65,66,35")
    p209Errors.push(`hiše 1868 neujemane — najdeno: ${p209Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1511)
    p209Errors.push(`HOUSE_VITALS ≠ 1511 (${HOUSE_VITALS.length} — P208: 1557; P209: + 13 blokov 1868-04106 = 1511!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 292)
    p209Errors.push(`bloki 04106 ≠ 292 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 292!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p209Errors.push("04106-bloki izven {1868, ..., 1885} (predzgodovina: 1857–1867 še nebrani!)");
  if (!p209Death.some((h) => h.houseNo === "15" && h.whatSi.includes("nožgodanujeleg")))
    p209Errors.push("★★★ h15-'nožgodanujeleg'-ANOMALIA-z61 (edina-popolnoma-NEBERLJIVA!) ni označena");
  if (!p209Death.some((h) => h.houseNo === "13" && h.whatSi.includes("JAKOFČIČ-×2")))
    p209Errors.push("★★★ h13-JAKOFČIČ-×2-1868 (z66-Anna + z80-Agnes!) ni označena");
  if (!p209Death.some((h) => h.houseNo === "41" && h.whatSi.includes("HROVAT-nit")))
    p209Errors.push("★★★ h41-HROVAT-nit-z77 (P208-tail-soglasje!) ni označena");
  if (!p209Death.some((h) => h.houseNo === "35" && h.whatSi.includes("2-smrti-v-ISTEM-dnevu")))
    p209Errors.push("★★★ z77/z78-'2-smrti-v-ISTEM-dnevu' (Dec-13./15!) ni označena");
  push(
    "qa-p209-parish-death-1868-04106",
    "P209: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1868 = 18. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s69–s75 == Pag. 64–70 (pag = sken−5; md5-križna-veriga-P197→…→P209-13.×: s71+s72+s73+s74-sveži == P208-disk-1:1!) + **★★★ MEJA-1867/68 = s69 (1867-TAIL-×1-zap-103-Primostek-15-Lutblan-80J-ULEDBA-31.Dez→1.Jän + 'VSOTA'-4-DELNA-'1|8|6|8'-NOVA-FORMA-1.×-V-KORPUSU + RESTART-'1.-Jänner-1868'! s64–s68-1867-kontekst-zap-36–102!)** + **★★★ 80-VPIISOV-ŠTEVJE-IZ-VRSTIC-11.×** (ordinali-1–80-ČISTO — 3.-LETO-ZAPORED-BREZ-luknje/dupa! ord-stolpec-s69-'1–10'-×3.5 + s75-'77–80'-(P208-soglasje!) + vrstna-aritmetika 10+13+13+13+14+13+4 + meseci J13-MAX+F6+M4+A10+M5+J2+J5+A10+S4+O7+N4+D8!) + **★★★ h15-'nožgodanujeleg'-ANOMALIA-z61** (ime-neberljivo + starost-'—' — edina-popolnoma-NEBERLJIVA-vrsta-1868!) + **★★★ z77/z78-'2-smrti-v-ISTEM-dnevu'** (Dec-13./15-h41-Hrovat-46J + h35-Hrovćan-57J!) + h13-JAKOFČIČ-×2 (z66-Anna-63J + z80-Agnes-19J-Posledice[~Brandfleck?]!) + h54-×2 (z32-Timic + z35-Lopare!) + ULEDBA-vzorec-×2 (z56-Aug/Sep-31→1 + tail-103!); **1868 = 80 vpisov (z1–z80) / 13 Griblje-vpisov / 11 hiš (h54-×2 + h13-×2!)**; **13 NOVIH BLOKOV parish.ts: vitals 1557 → 1511 · 04106 = 279 → 292 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p209 (fetch-md5 + read + ord-stolpec + arb-meja + z1-celica + build-entries + build-proof) + qa-p209 (209. kontrola!) + dokaz parish-death-1868-04106.json (80 entries: 13-Griblje + 67-druge!) + pt-luknja-REGENERACIJA (292/1511!); **★★★ PREDZGODOVINA-LINIJA-18/29-LET!** (P210-LEAD: 1867 — s69-TAIL-×1-ŽE-VLM-PREBRANA (zap-103-Primostek-15-Lutblan-80J-ULEDBA!) + s64–s68-ŽE-FETCHAN+VLM (zap-36–102!) → probe-s057–s069!)",
    "P209: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1868 = THE 18th YEAR (issue #18): the-frame + **★★★ THE-1867/68-BOUNDARY = s69 (the-1867-TAIL-×1-ULEDBA + the-'VSOTA'-4-PART-'1|8|6|8'-NEW-FORM-1st-×-IN-THE-CORPUS + RESTART-'1.-Jänner-1868'!)** + **★★★ THE-80-ENTRIES-COUNT-FROM-ROWS-11.×** (ordinals-1–80-CLEAN — the-3rd-CONSECUTIVE-CLEAN-YEAR!) + **★★★ the-h15-'nožgodanujeleg'-ANOMALY-z61** + **★★★ z77/z78-'2-DEATHS-ON-THE-SAME-DAY'** + h13-JAKOFČIČ-×2 + h54-×2 + the-ULEDBA-pattern-×2; **1868 = 80 entries / 13 Griblje / 11 houses**; **13 NEW BLOCKS: the vitals 1557 → 1511 · the 04106 = 279 → 292**; the scripts p209 + the qa-p209 (the 209th check!) + the evidence parish-death-1868-04106.json (80 entries!) + the pt-gap-REGENERATION (292/1511!); **★★★ THE-PREHISTORY-LINE-18/29-YEARS!** (the P210-LEAD: 1867 — the-s69-TAIL-×1-ALREADY-READ → the-probe-s057–s069!)",
    p209Errors.length === 0,
    p209Errors.length === 0
      ? `13 vpisov / 80 vrstic (števje-iz-vrstic-11.×! ordinali-1–80-ČISTO!) / 11 hiš (×2-×2!) · MEJA-s69-'vsota'-4-DELNA-'1|8|6|8'-1.× + restart-'1.-Jänner-1868' · 'nožgodanujeleg'-ANOMALIA-z61 · 2-smrti-v-1-dnevu-z77/z78 · h13-×2-h54-×2 · ULEDBA-×2 · **PREDZGODOVINA-18/29!** · vitals 1511 · 04106 292 · 04894 520`
      : p209Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1557", "HOUSE_VITALS.length !== 1511")
src = src.replace('04106").length !== 279', '04106").length !== 292')
OLD_SET = "(h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1868 && " + OLD_SET)
src = src.replace("04106-bloki izven {1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1868 še nebrani!)",
                  "04106-bloki izven {1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1867 še nebrani!)")
src = src.replace("vitals 1557 · 04106 279 · 04894 520", "vitals 1511 · 04106 292 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1511')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p209_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1557" not in t and "== 279" not in t: continue
    o = t
    t = t.replace("1557", "1511").replace('.get("04106") == 338', '.get("04106") == 292').replace("04106 == 338", "04106 == 292").replace("04106==338", "04106==292").replace("skupaj == 338", "skupaj == 292").replace('"04106") == 338', '"04106") == 292').replace("(04106, 338)", "(04106, 292)").replace("== 338,", "== 292,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0123456789]_parish*.py")):
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace("04106 == 338", "04106 == 292").replace("04106==338", "04106==292").replace('04106": 279', '04106": 292').replace("skupaj == 338", "skupaj == 292").replace('"04106") == 338', '"04106") == 292').replace("(04106, 338)", "(04106, 292)").replace('byBook"]["04106"] == 279', 'byBook"]["04106"] == 292')
    t = t.replace("vitals == 1557", "vitals == 1511").replace("vitalsTotal == 1557", "vitalsTotal == 1511").replace('vitalsTotal"] == 1557', 'vitalsTotal"] == 1511').replace('!== 1557"', '!== 1511"').replace("1557-številcev", "1511-številcev").replace("vitals-števec-1557", "vitals-števec-1511").replace("vitals-1557", "vitals-1511")
    t = t.replace('"vitalsTotal": 1557', '"vitalsTotal": 1511')
    t = re.sub(r'set\(izven\) == \{"1869"', 'set(izven) == {"1868", "1869"', t)
    t = t.replace('",".join(leta) == "1869,1870', '",".join(leta) == "1868,1869,1870')
    t = t.replace('join(leta) == "1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1511
pt["corpus"]["byBook"]["04106"] = 292
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P209: +13-blokov-1868 (04106 279→292, vitals 1557→1511, ordinali-1–80-ČISTO-3.leto + 'nožgodanujeleg'-ANOMALIA + 2-smrti-v-1-dnevu!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
