#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P208 — INSERT qa-p208 + sanitizacija (1484→1498, 265→279, yearset +1869) + verifier-patch + pt-luknja + krstne-izjeme."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p207: MRLIŠKA PREDZGODOVINA 04106 — leto 1870 = 16. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p208-parish-death-1869-04106" not in src
BLOCK = '''
  // ——— qa-p208: MRLIŠKA PREDZGODOVINA 04106 — leto 1869 = 17. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1869 = 76 vpisov (ordinali-1–76 ČISTO — 2.-leto-
  //      zapored!) / 14 Griblje / 13–14 hiš (h22-×2 + h65-×2 + 1-[?]) + ★★★
  //      MEJA-1868/69-s75 (tail-×4 + 'vsota'-'1|8'-3.× + '1869'-glava-KROP-47.!)
  //      + ULEDBA-z1 + POŽEK-h28-NIT-3.-leto + DRAGOS-h12-nit.
  //      Dokaz: parish-death-1869-04106.json; skripte p208.
  {
  const p208Errors: string[] = [];
  const p208Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1869);
  if (p208Death.length !== 14)
    p208Errors.push(`bloki 1869 (04106) ≠ 14 (${p208Death.length} — 14 Griblje-vpisov / 76 vpisov vrstno-štetje!)`);
  const p208Houses = p208Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p208Houses.join(",") !== "12,13,20,22,22,28,47,49,65,65,70,72,73,?")
    p208Errors.push(`hiše 1869 neujemane — najdeno: ${p208Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1498)
    p208Errors.push(`HOUSE_VITALS ≠ 1498 (${HOUSE_VITALS.length} — P207: 1484; P208: + 14 blokov 1869-04106 = 1498!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 279)
    p208Errors.push(`bloki 04106 ≠ 279 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 279!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p208Errors.push("04106-bloki izven {1869, ..., 1885} (predzgodovina: 1857–1868 še nebrani!)");
  if (!p208Death.some((h) => h.houseNo === "1" || (h.houseNo === "22" && h.whatSi.includes("ULEDBA-NOVO-LETO"))))
    p208Errors.push("★★★ ULEDBA-NOVO-LETO-z1 (Jänner-1./2.-Milik-h22!) ni označena");
  if (!p208Death.some((h) => h.houseNo === "28" && h.whatSi.includes("POŽEK-NIT-3.-LETO")))
    p208Errors.push("★★★ h28-POŽEK-NIT-3.-LETO (z60-Ana-Pižek → 1870-Johann → 1871-Georg!) ni označena");
  if (!p208Death.some((h) => h.houseNo === "12" && h.whatSi.includes("DRAGOS-nit")))
    p208Errors.push("★★★ h12-DRAGOS-nit (→ 1877-DRAGOŠ-ISTE-HIŠE!) ni označena");
  if (!p208Death.some((h) => h.houseNo === "65" && h.whatSi.includes("Noßgabianstho")))
    p208Errors.push("★★★ 'Noßgabianstho-Kind'-z74 (h65-×2-#2 — dajalec-obroka!) ni označena");
  push(
    "qa-p208-parish-death-1869-04106",
    "P208: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1869 = 17. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s75–s80 == Pag. 70–75 (pag = sken−5; md5-križna-veriga-P197→…→P208-12.×: s78+s79+s80-sveži == P207-disk-1:1!) + **★★★ MEJA-1868/69 = s75 (1868-TAIL-×4-zap-77–80 + 'VSOTA'-'1|8'-3.×-V-KORPUSU-1:1-FORMA! + '1869-Jänner'-GLAVA-KROP-47.-POTRDITEV-invariante + RESTART-1–9! s71–s74-1868-kontekst-zap-24–76!)** + **KONEC-1869-s80-'VALOVITA-ČRTA' (P207-potrjeno!)** + **★★★ 76-VPIISOV-ŠTEVJE-IZ-VRSTIC-10.×** (ordinali-1–76-ČISTO-BREZ-luknje/dupa — 2.-LETO-ZAPORED-ČISTO! ord-stolpci-×3.5: s75-'77,78,79,80→1–9' + s80-'65–76' + vrstna-aritmetika 9+14+14+13+14+12 + meseci J7+F6+M5+A5+M3+J7+J5+1+1+A4+S10-MAX+O8+N7+D7!) + **★★★ ULEDBA-NOVO-LETO-z1** (Ana-Milik-Jänner-1./2. — vzorec-3.×!) + **★★★ h28-POŽEK-NIT-3.-LETO** (z60-Ana-Pižek-5-mes-Oct → 1870-z51-Johann → 1871-z50-Georg — NEPREKINJENO-3-LETA!) + **★★★ h12-DRAGOS-nit** (Michael-27J — → 1877-P200-DRAGOŠ-h12-ISTE-HIŠE-8-let!) + h65-×2 ('Noßgabianstho-Kind'-z74-dajalec-obroka! + Georg-Brine-z31) + h22-×2 (Milik-z1 + Miller-z33!) + PEZDIR-grafia-×3 (z40-z61-+kontekst!) + h13-JAKOFČIČ-nit (z17 → 1868-tail-z80-Agnes!); **1869 = 76 vpisov (z1–z76) / 14 Griblje-vpisov / 13–14 hiš (h22-×2 + h65-×2 + 1-[?]-neberljiva!)**; **14 NOVIH BLOKOV parish.ts: vitals 1484 → 1498 · 04106 = 265 → 279 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p208 (fetch-md5 + read + ord-stolpci + arb-meja + build-entries + build-proof) + qa-p208 (208. kontrola!) + dokaz parish-death-1869-04106.json (76 entries: 14-Griblje + 62-druge!) + pt-luknja-REGENERACIJA (279/1498!); **★★★ PREDZGODOVINA-LINIJA-17/29-LET!** (P209-LEAD: 1868 — s75-TAIL-×4-ŽE-VLM-PREBRANA (zap-77–80: Hrovat-41 + Hrovćan-35 + Tome-15 + Jakofčič-13!) + s71–s74-ŽE-FETCHAN+VLM (zap-24–76!) → probe-s064–s075!)",
    "P208: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1869 = THE 17th YEAR (issue #18): the-frame + **★★★ THE-1868/69-BOUNDARY = s75 (the-1868-TAIL-×4 + the-'VSOTA'-'1|8'-3rd-×-1:1-FORM! + the-'1869-Jänner'-HEAD-KROP-47th-CONFIRMATION + RESTART!)** + **THE-END-OF-1869-s80-'WAVY-LINE' (P207-confirmed!)** + **★★★ THE-76-ENTRIES-COUNT-FROM-ROWS-10.×** (ordinals-1–76-CLEAN — the-2nd-CONSECUTIVE-CLEAN-YEAR!) + **★★★ the-ULEDBA-NEW-YEAR-z1** + **★★★ the-h28-POŽEK-THREAD-3rd-YEAR** + **★★★ the-h12-DRAGOS-thread** + h65-×2-'Noßgabianstho' + h22-×2 + PEZDIR-grafia-×3 + the-h13-JAKOFČIČ-thread; **1869 = 76 entries / 14 Griblje / 13–14 houses**; **14 NEW BLOCKS: the vitals 1484 → 1498 · the 04106 = 265 → 279**; the scripts p208 + the qa-p208 (the 208th check!) + the evidence parish-death-1869-04106.json (76 entries!) + the pt-gap-REGENERATION (279/1498!); **★★★ THE-PREHISTORY-LINE-17/29-YEARS!** (the P209-LEAD: 1868 — the-s75-TAIL-×4-ALREADY-READ → the-probe-s064–s075!)",
    p208Errors.length === 0,
    p208Errors.length === 0
      ? `14 vpisov / 76 vrstic (števje-iz-vrstic-10.×! ordinali-1–76-ČISTO!) / 13–14 hiš (×2-×2-+[?]) · MEJA-s75-'vsota'-'1|8'-3.× + '1869'-glava-KROP-47. · ULEDBA-z1 · POŽEK-h28-3.-leto · DRAGOS-h12 · 'Noßgabianstho'-z74 · PEZDIR-×3 · **PREDZGODOVINA-17/29!** · vitals 1498 · 04106 279 · 04894 520`
      : p208Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1484", "HOUSE_VITALS.length !== 1498")
src = src.replace('04106").length !== 265', '04106").length !== 279')
OLD_SET = "(h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1869 && " + OLD_SET)
src = src.replace("04106-bloki izven {1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1869 še nebrani!)",
                  "04106-bloki izven {1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1868 še nebrani!)")
src = src.replace("vitals 1484 · 04106 265 · 04894 520", "vitals 1498 · 04106 279 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1498')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1484" not in t and "== 265" not in t: continue
    o = t
    t = t.replace("1484", "1498").replace('.get("04106") == 292', '.get("04106") == 279').replace("04106 == 292", "04106 == 279").replace("04106==292", "04106==279").replace("skupaj == 292", "skupaj == 279").replace('"04106") == 292', '"04106") == 279').replace("(04106, 292)", "(04106, 279)").replace("== 292,", "== 279,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p20[012345678]_parish*.py")):
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace("04106 == 292", "04106 == 279").replace("04106==292", "04106==279").replace('04106": 265', '04106": 279').replace("skupaj == 292", "skupaj == 279").replace('"04106") == 292', '"04106") == 279').replace("(04106, 292)", "(04106, 279)").replace('byBook"]["04106"] == 265', 'byBook"]["04106"] == 279')
    t = t.replace("vitals == 1484", "vitals == 1498").replace("vitalsTotal == 1484", "vitalsTotal == 1498").replace('vitalsTotal"] == 1484', 'vitalsTotal"] == 1498').replace('!== 1484"', '!== 1498"').replace("1484-številcev", "1498-številcev").replace("vitals-števec-1484", "vitals-števec-1498").replace("vitals-1484", "vitals-1498")
    t = t.replace('"vitalsTotal": 1484', '"vitalsTotal": 1498')
    t = re.sub(r'set\(izven\) == \{"1870"', 'set(izven) == {"1869", "1870"', t)
    t = t.replace('",".join(leta) == "1870,1871', '",".join(leta) == "1869,1870,1871')
    t = t.replace('join(leta) == "1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1498
pt["corpus"]["byBook"]["04106"] = 279
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P208: +14-blokov-1869 (04106 265→279, vitals 1484→1498, ordinali-1–76-ČISTO-2.leto + ULEDBA-z1 + POŽEK-h28-3.leto + 'Noßgabianstho'!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
