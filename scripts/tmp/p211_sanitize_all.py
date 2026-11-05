#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P211 — INSERT qa-p211 + sanitizacija (1531→1544, 312→325, yearset +1866) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p210: MRLIŠKA PREDZGODOVINA 04106 — leto 1867 = 19. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p211-parish-death-1866-04106" not in src
BLOCK = '''
  // ——— qa-p211: MRLIŠKA PREDZGODOVINA 04106 — leto 1866 = 20. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1866 = 104 vpisov (ordinali-1–104 ČISTO — 5.-leto-
  //      zapored!) / 13 Griblje / 12 hiš (h34-×2-FILAK!) + ★★★ DOUBLE-SCAN-4.×
  //      (s53==s54-SKIP!) + MEJA-1865/66-s51 (tail-1865-KROP + prečrtana-67 +
  //      restart-'1866'-VELIKA-LETVICA-49.-POTRDITEV!) + DVOJČKA-z34/z35 +
  //      ULEDBA-#10-z58 (29-JUNI→1-JULI!) + HUESTIČ-h41-kontinuiteta-z22 +
  //      PEZDIRC-h14/h53 + POŽEK-h58 + otroška-umrljivost-77%!
  //      Dokaz: parish-death-1866-04106.json; skripte p211.
  {
  const p211Errors: string[] = [];
  const p211Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1866);
  if (p211Death.length !== 13)
    p211Errors.push(`bloki 1866 (04106) ≠ 13 (${p211Death.length} — 13 Griblje-vpisov / 104 vpisov vrstno-štetje!)`);
  const p211Houses = p211Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p211Houses.join(",") !== "1,3,13,14,19,34,34,37,41,47,48,53,58")
    p211Errors.push(`hiše 1866 neujemane — najdeno: ${p211Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1544)
    p211Errors.push(`HOUSE_VITALS ≠ 1544 (${HOUSE_VITALS.length} — P210: 1531; P211: + 13 blokov 1866-04106 = 1544!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 325)
    p211Errors.push(`bloki 04106 ≠ 325 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 325!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p211Errors.push("04106-bloki izven {1866, ..., 1885} (predzgodovina: 1857–1866 še nebrani!)");
  if (!p211Death.some((h) => h.houseNo === "41" && h.whatSi.includes("HUESTIČ-h41-KONTINUITETA")))
    p211Errors.push("★★★ HUESTIČ-h41-KONTINUITETA-z22 (Maria-Hušić[~Huestič]-¼-güblerštofa → 1903!) ni označena");
  if (!p211Death.some((h) => h.houseNo === "14" && h.whatSi.includes("PEZDIRC-h14-KONTINUITETA")))
    p211Errors.push("★★★ PEZDIRC-h14-KONTINUITETA-z41 (Mathias — z66-tail-1865!) ni označena");
  if (!p211Death.some((h) => h.houseNo === "58" && h.whatSi.includes("TOTGEBORENES-v.-Mark.-POŽEK")))
    p211Errors.push("★★★ TOTGEBORENES-POŽEK-h58-z90 (2-OSEBI-FALSIFICIRAN-KROP!) ni označena");
  if (!p211Death.some((h) => h.houseNo === "1" && h.whatSi.includes("ULEDBA-#10-9.INSTANCE")))
    p211Errors.push("★★★ ULEDBA-#10-9.INSTANCE-z58 (29-JUNI→1-JULI!) ni označena");
  if (!p211Death.some((h) => h.houseNo === "34" && h.whatSi.includes("FILAK-×2-#1")))
    p211Errors.push("★★★ h34-FILAK-×2 (z48 + z80!) ni označena");
  push(
    "qa-p211-parish-death-1866-04106",
    "P211: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1866 = 20. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s051–s060 == Pag. 46–55 (pag = sken−5; SANDBOX-RESET-REGENERACIJA: 2×-neodvisna-prenosa-md5-11/11 + vsebinska-križ-s60↔P210-tail-zap-95–104-10/10!) + **★★★ DOUBLE-SCAN-4.× = s53==s54 (md5-različna-450719B/470425B — vsebina-1:1-po-imenih-13/13!) → s54-SKIP (cf. P204-s103==s104!)** + **★★★ MEJA-1865/66 = s51 (tail-1865-z65/z66-KROP: z66-Griblje-h14-Maria-Pezdirc-66J! + PREČRTANA-PRAZNA-VRSTA-67-Schlangenlinien-SKIP + restart-'Jänner'-'1866'-VELIKA-LETVICA-KROP-49.-POTRDITEV-invariante!)** + **★★★ 104-VPIISOV-ŠTEVJE-IZ-VRSTIC-13.×** (ordinali-1–104-ČISTO — 5.-LETO-ZAPORED-BREZ-luknje/dupa! vrstna-aritmetika 8+12+13+12+13+13+11+12+10 + meseci J8+F5+M10+A12+M10+J13-MAX+J9+A7+S7+O7+N11+D4!) + **★★★ DVOJČKA-MRTVOROJENA-z34/z35** ('Totgeborenes-Kind-v.-Josef-Žunič'-×2-Vranoviče-h19-April! — VLM-halucinaciji-FALSIFICIRANI!) + **★★★ ULEDBA-#10-9.INSTANCE-z58** (29-JUNI→1-JULI-pokop-KROP-'Juli-1'-ČISTO!) + **★★★ HUESTIČ-h41-KONTINUITETA-z22** (Maria-Hušić[~Huestič/Kusić?]-22-J-¼-güblerštofa → 1903-Maria-HUESTIČ-GRIBLJE-41-37-let-globoko! + hiša-DUEL-11-vs-41-rešen-izrezom!) + **★★★ PEZDIRC-niti-z41-h14 (+z66-tail!) + z98-h53** ('Missgeborenes-Kind-d.-Janez-Pezdirc' — P210-tail-'Anton'-FALSIFICIRANA!) + **★★★ POŽEK-h58-z90** ('Totgeborenes-Kind-v.-Mark.-Požek' — 2-OSEBI-HIPOTEZA-FALSIFICIRANA-KROP-4.2×!) + ★★★ otroška-umrljivost-77%-10/13-GRIBLJE + h34-FILAK-×2 + KLOBUČAR-×2-v-4-dneh + ½/¼-GÜBLER-leksikon; **1866 = 104 vpisov (z1–z104) / 13 Griblje-vpisov / 12 hiš (h34-×2!)**; **13 NOVIH BLOKOV parish.ts: vitals 1531 → 1544 · 04106 = 312 → 325 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p211 (fetch-2×-md5 + read + krop-×11 + build-entries + build-proof) + qa-p211 (211. kontrola!) + dokaz parish-death-1866-04106.json (104 entries: 13-Griblje + 91-druge!) + pt-luknja-REGENERACIJA (325/1544!); **★★★ PREDZGODOVINA-LINIJA-20/29-LET!** (P212-LEAD: 1865 — s50-ŽE-FETCHAN+VLM (zap-50–64: 15-vrstic!) + s51-TAIL-z65/z66-ŽE-KROP (Griblje-h14-Maria-Pezdirc!) → probe-s042–s050!)",
    "P211: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1866 = THE 20th YEAR (issue #18): the-frame + **★★★ THE-DOUBLE-SCAN-4.× = s53==s54 (SKIP!)** + **★★★ THE-1865/66-BOUNDARY = s51 (the-1865-TAIL-KROP + the-CROSSED-OUT-EMPTY-ROW-67 + the-restart-'1866'-BIG-YEAR-KROP-the-49th-CONFIRMATION!)** + **★★★ THE-104-ENTRIES-COUNT-FROM-ROWS-13.×** (ordinals-1–104-CLEAN — the-5th-CONSECUTIVE-CLEAN-YEAR!) + **★★★ THE-TWIN-STILLBORNS-z34/z35** + **★★★ the-ULEDBA-#10-9th-INSTANCE-z58** (29-JUNI→1-JULI!) + **★★★ the-HUESTIČ-h41-CONTINUITY-z22** (→ 1903-Maria-HUESTIČ-37-years-deep!) + **★★★ the-PEZDIRC-threads-z41-h14 + z98-h53** ('Missgeborenes-Kind-d.-Janez-Pezdirc' — the-'Anton'-FALSIFIED!) + **★★★ POŽEK-h58-z90** (the-2-PERSONS-HYPOTHESIS-FALSIFIED-KROP-4.2×!) + child-mortality-77%; **1866 = 104 entries / 13 Griblje / 12 houses (h34-×2!)**; **13 NEW BLOCKS: the vitals 1531 → 1544 · the 04106 = 312 → 325**; the scripts p211 + the qa-p211 (the 211th check!) + the evidence parish-death-1866-04106.json (104 entries!) + the pt-gap-REGENERATION (325/1544!); **★★★ THE-PREHISTORY-LINE-20/29-YEARS!** (the P212-LEAD: 1865 — the-s50-ALREADY-READ + the-s51-TAIL-ALREADY-KROP → the-probe-s042–s050!)",
    p211Errors.length === 0,
    p211Errors.length === 0
      ? `13 vpisov / 104 vrstic (števje-iz-vrstic-13.×! ordinali-1–104-ČISTO-5.-leto!) / 12 hiš (h34-×2-FILAK!) · DOUBLE-SCAN-4.×-s53==s54-SKIP · MEJA-s51-tail-1865-KROP + prečrtana-67 + restart-'1866'-49.-POTRDITEV · DVOJČKA-z34/z35 · ULEDBA-#10-z58-JULI · HUESTIČ-h41-z22 · PEZDIRC-h14/h53 · POŽEK-h58 · otroška-77% · **PREDZGODOVINA-20/29!** · vitals 1544 · 04106 325 · 04894 520`
      : p211Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1531", "HOUSE_VITALS.length !== 1544")
src = src.replace('04106").length !== 312', '04106").length !== 325')
OLD_SET = "(h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1866 && " + OLD_SET)
src = src.replace("04106-bloki izven {1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1867 še nebrani!)",
                  "04106-bloki izven {1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1866 še nebrani!)")
src = src.replace("vitals 1531 · 04106 312 · 04894 520", "vitals 1544 · 04106 325 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1544')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1531" not in t and "== 312" not in t: continue
    o = t
    t = t.replace("1531", "1544").replace('.get("04106") == 312', '.get("04106") == 325').replace("04106 == 312", "04106 == 325").replace("04106==312", "04106==325").replace("skupaj == 312", "skupaj == 325").replace('"04106") == 312', '"04106") == 325').replace("(04106, 312)", "(04106, 325)").replace("== 312,", "== 325,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 312", "04106 == 325"), ("04106==312", "04106==325"),
                 ('04106": 312', '04106": 325'), ("skupaj == 312", "skupaj == 325"),
                 ('"04106") == 312', '"04106") == 325'), ("(04106, 312)", "(04106, 325)"),
                 ('byBook"]["04106"] == 312', 'byBook"]["04106"] == 325'),
                 ('["04106"] == 312', '["04106"] == 325'),
                 ("vitals == 1531", "vitals == 1544"), ("vitalsTotal == 1531", "vitalsTotal == 1544"),
                 ('vitalsTotal"] == 1531', 'vitalsTotal"] == 1544'),
                 ('"vitalsTotal": 1531', '"vitalsTotal": 1544'),
                 ('\\"vitalsTotal\\": 1531', '\\"vitalsTotal\\": 1544'),
                 ('!== 1531"', '!== 1544"'),
                 ("1531-številcev", "1544-številcev"),
                 ("vitals-števec-1531", "vitals-števec-1544"), ("vitals-1531", "vitals-1544")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1867"', 'set(izven) == {"1866", "1867"', t)
    t = t.replace('",".join(leta) == "1867,1868', '",".join(leta) == "1866,1867,1868')
    t = t.replace('join(leta) == "1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1544
pt["corpus"]["byBook"]["04106"] = 325
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P211: +13-blokov-1866 (04106 312→325, vitals 1531→1544, ordinali-1–104-ČISTO-5.leto + DOUBLE-SCAN-4.× + DVOJČKA + ULEDBA-#10 + HUESTIČ-h41-kontinuiteta!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
