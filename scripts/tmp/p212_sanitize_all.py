#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P212 — INSERT qa-p212 + sanitizacija (1544→1557, 325→338, yearset +1865) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p211: MRLIŠKA PREDZGODOVINA 04106 — leto 1866 = 20. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p212-parish-death-1865-04106" not in src
BLOCK = '''
  // ——— qa-p212: MRLIŠKA PREDZGODOVINA 04106 — leto 1865 = 21. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1865 = 66 vpisov (ordinali-1–66 ČISTO — 6.-leto-
  //      zapored!) / 13 Griblje / 12 hiš (h37-×2-HUSIČ-klaster!) + ★★★ MEJA-
  //      1864/65-s46 (tail-1864-NATAČNO-4-KROP + ULEDBA-#11-z91-30.Dez→1.Jän +
  //      '1865'-VELIKA-LETVICA-50.-POTRDITEV!) + z74-duel-REŠEN (Kurrent-4/1!)
  //      + ANOMALIJA-pokop-pred-smrtjo-z13 (pisar-mota!) + HUSIČ-h37-klaster
  //      (mati-27J + otrok-2-mes!) + 2×-Maria-Križan-v-1-tednu + BRINC-×2 +
  //      POŽEK-h67-nit + PEZDIRC-h14-kontinuiteta-tail + otroška-umrljivost-31%!
  //      Dokaz: parish-death-1865-04106.json; skripte p212.
  {
  const p212Errors: string[] = [];
  const p212Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1865);
  if (p212Death.length !== 13)
    p212Errors.push(`bloki 1865 (04106) ≠ 13 (${p212Death.length} — 13 Griblje-vpisov / 66 vpisov vrstno-štetje!)`);
  const p212Houses = p212Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p212Houses.join(",") !== "3,14,18,19,23,28,32,37,37,50,67,68,70")
    p212Errors.push(`hiše 1865 neujemane — najdeno: ${p212Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1557)
    p212Errors.push(`HOUSE_VITALS ≠ 1557 (${HOUSE_VITALS.length} — P211: 1544; P212: + 13 blokov 1865-04106 = 1557!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 338)
    p212Errors.push(`bloki 04106 ≠ 338 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P212: 13 × 1865 + P211: 13 × 1866 + P210: 20 × 1867 + P209: 13 × 1868 + P208: 14 × 1869 + P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 338!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1865 && (h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p212Errors.push("04106-bloki izven {1865, ..., 1885} (predzgodovina: 1857–1865 še nebrani!)");
  if (!p212Death.some((h) => h.houseNo === "37" && h.whatSi.includes("HUSIČ-h37-klaster-#1")))
    p212Errors.push("★★★ HUSIČ-h37-klaster-z13 (mati-27-J-Schwindsucht + otrok-z18!) ni označen");
  if (!p212Death.some((h) => h.houseNo === "14" && h.whatSi.includes("PEZDIRC-h14-KONTINUITETA")))
    p212Errors.push("★★★ PEZDIRC-h14-KONTINUITETA-z66-tail (Maria-66-J → z41-1866-Mathias!) ni označena");
  if (!p212Death.some((h) => h.houseNo === "3" && h.whatSi.includes("PRVI-VPIS-1865-restart")))
    p212Errors.push("★★★ z1-PRVI-VPIS-1865-restart (Maria-Križan-h3-81-J!) ni označen");
  if (!p212Death.some((h) => h.houseNo === "67" && h.whatSi.includes("POŽEK-nit-#2")))
    p212Errors.push("★★★ POŽEK-nit-#2-z36 (Mathias-h67 — cf. h58-P211/P192!) ni označena");
  push(
    "qa-p212-parish-death-1865-04106",
    "P212: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1865 = 21. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s046–s051 == Pag. 41–46 (pag = sken−5; 2×-neodvisna-prenosa-md5-9/9 + križ-s50-vs-P211-disk-1:1!) + **★★★ MEJA-1864/65 = s46 (tail-1864-z88–z91-NATAČNO-4-vrstice-KROP! + z91-ULEDBA-#11-10.INSTANCE-30.Dez-1864→1.Jänner-1865-pokop! + dvojna-ločilna-črta + restart-'Jänner'-'1865'-VELIKA-LETVICA-KROP-50.-POTRDITEV-invariante!)** + **★★★ z74_s45_zap-DUEL-REŠEN** (s45-zaporedne-74/75/76-KROP: '4-ima-ZANKO-1-je-ozka-črtica'-KURRENT-CIFRA-ANALIZA! → 1864-kontekst-veriga-60→91-ČISTO-ZVEZNA — VLM-'71/72/73'-FALSIFICIRAN!) + **★★★ 66-VPIISOV-ŠTEVJE-IZ-VRSTIC-14.×** (ordinali-1–66-ČISTO — 6.-LETO-ZAPORED-BREZ-luknje/dupa! vrstna-aritmetika 7+14+14+14+15+2 + meseci J8+F6+M7+A10+M6+J2+J6+A4+S3+O4+N7+D3!) + **★★★ z13-ANOMALIJA-PISAR-MOTA** (pokop-17.-vpisan-PRED-smrt-18.-KROP-POTRJENO-v-zapisu — 'morda-smrt-17./pokop-18.'!) + **★★★ HUSIČ-h37-KLASTER** (z13-mati-Anna-27-J-Schwindsucht-umrla-18.2 + z18-otrok-Anna-2-mes-umrla-11.3 — '½-Güblerswirt' + '-Kind'-suffix-ISTE-hiše! mati+dojenček-v-3-tednih!) + **★★★ 2×-MARIA-KRIŽAN-v-1-tednu** (z88-tail-Otok-h20-48-J-12.Dez + z1-restart-GRIBLJE-h3-81-J-16.Jan!) + **★★★ BRINC-×2-v-2-hišah** (z9-Anna-h23-60-J + z20-Jernej-h28-28-J!) + **★★★ POŽEK-nit-#2-z36** (Mathias-h67-36-J — cf. P211-z90-h58 + P192-h58! h67-NOVA!) + **★★★ PEZDIRC-h14-KONTINUITETA-tail-z66** (Maria-66-J → z41-1866-Mathias-unehelich-h14! VLM-h11-duel-rešen-KROP-h14!) + ★★★ KRIŽAN-h3-nit (z1 → 1867-h3-Papic-×3!) + ★ z11-KROP-4-KOREKCIJE (h50-NI-80 + Redovi-NI-Podgoršek + ½-Gübler-Kind + Wassersucht!) + ★ z8-URIH-grafia (KROP-'Urih,-ne-Urik'!) + ★ z9-starost-DUEL (KROP-60-vs-VLM-56!) + otroška-umrljivost-31%-4/13 (NIŽJA-kot-1866-77% — cholera-prelivala-v-1866?); **1865 = 66 vpisov (z1–z66) / 13 Griblje-vpisov / 12 hiš (h37-×2!)**; **13 NOVIH BLOKOV parish.ts: vitals 1544 → 1557 · 04106 = 325 → 338 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p212 (fetch-2×-md5-9/9 + read-×9 + krop-×16 + build-entries + build-proof) + qa-p212 (212. kontrola!) + dokaz parish-death-1865-04106.json (66 entries: 13-Griblje + 53-druge!) + pt-luknja-338/1557; **★★★ PREDZGODOVINA-LINIJA-21/29-LET!** (P213-LEAD: 1864 — s42–s46-tail-ŽE-VLM+delno-KROP (zap-31–91-ZVEZNA; z74-duel-REŠEN!) → probe-s039–s042!)",
    "P212: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1865 = THE 21st YEAR (issue #18): the-frame + **★★★ THE-1864/65-BOUNDARY = s46 (the-1864-TAIL-EXACTLY-4-ROWS-KROP! + the-z91-ULEDBA-#11-10th-INSTANCE-30-Dec-1864→1-Jan-1865! + the-double-line + the-restart-'1865'-BIG-YEAR-KROP-the-50th-CONFIRMATION!)** + **★★★ THE-z74-DUEL-SOLVED** (the-s45-74/75/76-KROP: the-'4-has-a-LOOP-1-is-a-slash'-KURRENT-DIGIT-ANALYSIS! → the-1864-context-chain-60→91-CLEAN — the-VLM-'71/72/73'-FALSIFIED!) + **★★★ THE-66-ENTRIES-COUNT-FROM-ROWS-14.×** (ordinals-1–66-CLEAN — the-6th-CONSECUTIVE-CLEAN-YEAR!) + **★★★ THE-z13-SCRIBAL-ERROR** (the-burial-17-WRITTEN-BEFORE-the-death-18-KROP-CONFIRMED!) + **★★★ THE-HUSIČ-h37-CLUSTER** (the-mother-27-y + the-child-2-mo-3-weeks-apart! the-'½-Güblerswirt' + '-Kind'-suffix!) + **★★★ 2×-MARIA-KRIŽAN-IN-1-WEEK** + **★★★ BRINC-×2-in-2-houses** + **★★★ POŽEK-thread-#2-h67** + **★★★ PEZDIRC-h14-CONTINUITY-tail** + child-mortality-31%; **1865 = 66 entries / 13 Griblje / 12 houses (h37-×2!)**; **13 NEW BLOCKS: the vitals 1544 → 1557 · the 04106 = 325 → 338**; the scripts p212 + the qa-p212 (the 212th check!) + the evidence parish-death-1865-04106.json (66 entries!) + the pt-gap-338/1557; **★★★ THE-PREHISTORY-LINE-21/29-YEARS!** (the P213-LEAD: 1864 — the-s42–s46-tail-ALREADY-READ → the-probe-s039–s042!)",
    p212Errors.length === 0,
    p212Errors.length === 0
      ? `13 vpisov / 66 vrstic (števje-iz-vrstic-14.×! ordinali-1–66-ČISTO-6.-leto!) / 12 hiš (h37-×2-HUSIČ-klaster!) · MEJA-s46-tail-1864-KROP-4-vrstice + ULEDBA-#11 + restart-'1865'-50.-POTRDITEV · z74-duel-REŠEN-KURRENT-4/1 · ANOMALIJA-z13-pisar-mota · HUSIČ-h37-klaster-mati+otrok · 2×-Maria-Križan · BRINC-×2 · POŽEK-h67 · PEZDIRC-h14-tail · otroška-31% · **PREDZGODOVINA-21/29!** · vitals 1557 · 04106 338 · 04894 520`
      : p212Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1544", "HOUSE_VITALS.length !== 1557")
src = src.replace('04106").length !== 325', '04106").length !== 338')
OLD_SET = "(h.year ?? 0) !== 1866 && (h.year ?? 0) !== 1867 && (h.year ?? 0) !== 1868 && (h.year ?? 0) !== 1869 && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1865 && " + OLD_SET)
src = src.replace("04106-bloki izven {1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1866 še nebrani!)",
                  "04106-bloki izven {1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1865 še nebrani!)")
src = src.replace("vitals 1544 · 04106 325 · 04894 520", "vitals 1557 · 04106 338 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1557')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_", "p208_", "p210_", "p211_", "p212_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1544" not in t and "== 325" not in t: continue
    o = t
    t = t.replace("1544", "1557").replace('.get("04106") == 325', '.get("04106") == 338').replace("04106 == 325", "04106 == 338").replace("04106==325", "04106==338").replace("skupaj == 325", "skupaj == 338").replace('"04106") == 325', '"04106") == 338').replace("(04106, 325)", "(04106, 338)").replace("== 325,", "== 338,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-9][0-9]_parish*.py")):
    if "p212" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("04106 == 325", "04106 == 338"), ("04106==325", "04106==338"),
                 ('04106": 325', '04106": 338'), ("skupaj == 325", "skupaj == 338"),
                 ('"04106") == 325', '"04106") == 338'), ("(04106, 325)", "(04106, 338)"),
                 ('byBook"]["04106"] == 325', 'byBook"]["04106"] == 338'),
                 ('["04106"] == 325', '["04106"] == 338'),
                 ("vitals == 1544", "vitals == 1557"), ("vitalsTotal == 1544", "vitalsTotal == 1557"),
                 ('vitalsTotal"] == 1544', 'vitalsTotal"] == 1557'),
                 ('"vitalsTotal": 1544', '"vitalsTotal": 1557'),
                 ('\\"vitalsTotal\\": 1544', '\\"vitalsTotal\\": 1557'),
                 ('!== 1544"', '!== 1557"'),
                 ("1544-številcev", "1557-številcev"),
                 ("vitals-števec-1544", "vitals-števec-1557"), ("vitals-1544", "vitals-1557")]:
        t = t.replace(a, b)
    t = re.sub(r'set\(izven\) == \{"1866"', 'set(izven) == {"1865", "1866"', t)
    t = t.replace('",".join(leta) == "1866,1867', '",".join(leta) == "1865,1866,1867')
    t = t.replace('join(leta) == "1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1557
pt["corpus"]["byBook"]["04106"] = 338
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P212: +13-blokov-1865 (04106 325→338, vitals 1544→1557, ordinali-1–66-ČISTO-6.leto + MEJA-'1865'-50.-POTRDITEV + z74-duel-REŠEN + ULEDBA-#11 + ANOMALIJA-pisar-mota-z13 + HUSIČ-h37-klaster!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
