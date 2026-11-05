#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P207 — INSERT qa-p207 + sanitizacija (1472→1484, 253→265, yearset +1870) + verifier-patch + pt-luknja + krstne-izjeme."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p206: MRLIŠKA PREDZGODOVINA 04106 — leto 1871 = 15. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p207-parish-death-1870-04106" not in src
BLOCK = '''
  // ——— qa-p207: MRLIŠKA PREDZGODOVINA 04106 — leto 1870 = 16. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1870 = 70 vpisov (ordinali-1–70 ČISTO — brez-luknje/
  //      dupa, edinstveno!) / 12 Griblje / 12 hiš-vsi-različni + ★★★ MEJA-1869/70
  //      s80→s81 (valovita-črta + velika-'1870'-×2-KROP!) + MEJA-1870/71-s86
  //      (P206-soglasje!) + h1-GOSPODAR-Jessernigg + POŽEK-h28-NIT-2.-leto.
  //      Dokaz: parish-death-1870-04106.json; skripte p207.
  {
  const p207Errors: string[] = [];
  const p207Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1870);
  if (p207Death.length !== 12)
    p207Errors.push(`bloki 1870 (04106) ≠ 12 (${p207Death.length} — 12 Griblje-vpisov / 70 vpisov vrstno-štetje!)`);
  const p207Houses = p207Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p207Houses.join(",") !== "1,4,20,22,28,32,40,46,48,51,52,68")
    p207Errors.push(`hiše 1870 neujemane — najdeno: ${p207Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1484)
    p207Errors.push(`HOUSE_VITALS ≠ 1484 (${HOUSE_VITALS.length} — P206: 1472; P207: + 12 blokov 1870-04106 = 1484!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 265)
    p207Errors.push(`bloki 04106 ≠ 265 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P207: 12 × 1870 + P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 265!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1870 && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p207Errors.push("04106-bloki izven {1870, ..., 1885} (predzgodovina: 1857–1869 še nebrani!)");
  if (!p207Death.some((h) => h.houseNo === "1" && h.whatSi.includes("Jessernigg")))
    p207Errors.push("★★★ h1-GOSPODAR-'Jessernigg'-z28 (65J — cf. P84-krstne-h1!) ni označena");
  if (!p207Death.some((h) => h.houseNo === "28" && h.whatSi.includes("POŽEK-h28-NIT-2.-LETO")))
    p207Errors.push("★★★ POŽEK-h28-NIT-2.-LETO (z51-Johann-1-mes → 1871-z50-Georg!) ni označena");
  if (!p207Death.some((h) => h.houseNo === "52" && h.whatSi.includes("MRTVOROJEN")))
    p207Errors.push("★★★ MRTVOROJEN-Knavs-h52 (z42 — July —/23!) ni označena");
  push(
    "qa-p207-parish-death-1870-04106",
    "P207: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1870 = 16. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s81–s86 == Pag. 76–81 (pag = sken−5; md5-križna-veriga-P197→…→P207-11.×: s84+s85+s86-sveži == P206-disk-1:1!) + **★★★ MEJA-1869/70 = s80→s81 (s80-KONEC-LETOVNIKA-1869 — 'VALOVITA-ČRTA'-KROP-DA! + '1869'-VLM-misread-'1849'-falsificirana! → s81-VELIKA-LETVICA-'1870'-×2-KROP-POTRJENA + RESTART-1! s78/s79/s80-1869-kontekst-zap-38–76!)** + **★★★ MEJA-1870/71 = s86 (tail-×7-zap-64–70 + 'vsota'-'1|8' + restart-'Jänner'-1871 — P206-soglasje-1:1!)** + **★★★ 70-VPIISOV-ŠTEVJE-IZ-VRSTIC-9.×** (ordinali-1–70-ČISTO-BREZ-luknje/dupa — edinstveno-v-04106-predzgodovini! ord-stolpci-×3.5-recept-P206: s83-'25–37'-(celostanska-zamik-−2! 36/37-TUKAJ — NI-luknje!)-+ s84-'38–50' + vrstna-aritmetika 11+13+13+13+13+7 + meseci J3+F6+M9+A11-MAX+M6+J4+J2+A5+S7+O6+N4+D5!) + **★★★ h1-GOSPODAR-'Jessernigg'-z28** (Karolina-65J-Wassersucht!) + **★★★ POŽEK-h28-NIT-2.-LETO** (z51-Johann-Požek-1-mes-Sept-1870 → 1871-z50-Georg-5¾J-Sept!) + MRTVOROJEN-z42-Knavs-h52 + ime-DUELI-×3 (z39-Pezić/Pezdire + z60-'Janos-Millié'-vs-'Janez-Milič' + z63-'Peter-Afrik'-vs-'Adriih'!) + Urih-nit (z49-h68 → 1871-z20-Arik[~Urih]-h33!); **1870 = 70 vpisov (z1–z70) / 12 Griblje-vpisov / 12 hiš-vsi-RAZLIČNI**; **12 NOVIH BLOKOV parish.ts: vitals 1472 → 1484 · 04106 = 253 → 265 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p207 (fetch-md5 + read + ord-stolpci + build-entries + build-proof) + qa-p207 (207. kontrola!) + dokaz parish-death-1870-04106.json (70 entries: 12-Griblje + 58-druge!) + pt-luknja-REGENERACIJA (265/1484!); **★★★ PREDZGODOVINA-LINIJA-16/29-LET!** (P208-LEAD: 1869 — s80-KONEC-LETOVNIKA-'valovita-črta'-ŽE-VLM-PREBRANA (zap-65–76!) + s78/s79-ŽE-FETCHAN+VLM (zap-38–64!) → probe-s071–s080!)",
    "P207: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1870 = THE 16th YEAR (issue #18): the-frame + **★★★ THE-1869/70-BOUNDARY = s80→s81 (s80-THE-END-OF-THE-1869-VOLUME — the-'WAVY-LINE'-KROP-YES! + the-'1869'-VLM-misread-'1849'-FALSIFIED! → s81-the-BIG-'1870'-YEAR-DIGIT-×2-KROP-CONFIRMED + RESTART-1!)** + **★★★ THE-1870/71-BOUNDARY = s86 (P206-agreement-1:1!)** + **★★★ THE-70-ENTRIES-COUNT-FROM-ROWS-9.×** (ordinals-1–70-CLEAN-no-gap-no-dup — unique-in-the-04106-prehistory! the-ordinal-columns-×3.5-P206-recipe: s83-'25–37'-+ s84-'38–50'!) + **★★★ the-h1-GENTLEMAN-'Jessernigg'-z28** + **★★★ the-POŽEK-h28-THREAD-2nd-YEAR** + the-STILLBORN-z42 + ime-DUELS-×3 + the-Urih-thread; **1870 = 70 entries / 12 Griblje / 12 houses-ALL-DIFFERENT**; **12 NEW BLOCKS: the vitals 1472 → 1484 · the 04106 = 253 → 265**; the scripts p207 + the qa-p207 (the 207th check!) + the evidence parish-death-1870-04106.json (70 entries!) + the pt-gap-REGENERATION (265/1484!); **★★★ THE-PREHISTORY-LINE-16/29-YEARS!** (the P208-LEAD: 1869 — the-s80-END-OF-VOLUME-ALREADY-READ → the-probe-s071–s080!)",
    p207Errors.length === 0,
    p207Errors.length === 0
      ? `12 vpisov / 70 vrstic (števje-iz-vrstic-9.×! ordinali-1–70-ČISTO!) / 12 hiš-vsi-različni · MEJA-s80-'valovita-črta'→s81-'1870'-velika-letnica-×2-KROP · MEJA-s86-P206-soglasje · h1-GOSPODAR-Jessernigg · POŽEK-h28-NIT-2.-leto · MRTVOROJEN-z42 · ime-DUELI-×3 · **PREDZGODOVINA-16/29!** · vitals 1484 · 04106 265 · 04894 520`
      : p207Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1472", "HOUSE_VITALS.length !== 1484")
src = src.replace('04106").length !== 253', '04106").length !== 265')
OLD_SET = "(h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1870 && " + OLD_SET)
src = src.replace("04106-bloki izven {1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1870 še nebrani!)",
                  "04106-bloki izven {1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1869 še nebrani!)")
src = src.replace("vitals 1472 · 04106 253 · 04894 520", "vitals 1484 · 04106 265 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1484')}")

# krstne-izjeme: 1870-doda-h28 → P86-izjema (h28 že od P206-p86-patch-ma-1871; dodaj 1870)
m86 = src.count('&& !(v.bookSignature === "04106" && v.year === 1871 && hn === "28")')
if m86:
    src = src.replace('&& !(v.bookSignature === "04106" && v.year === 1871 && hn === "28")',
                      '&& !(v.bookSignature === "04106" && v.year === 1871 && hn === "28") && !(v.bookSignature === "04106" && v.year === 1870 && hn === "28")')
    QA.write_text(src, encoding="utf-8")
    print(f"p86-izjema-h28-1870-dodana ({m86})")
# P85-h38?-1870-NI-h38. P90-h20?-preveri-runQA.
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_", "p207_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1472" not in t and "== 253" not in t: continue
    o = t
    t = t.replace("1472", "1484").replace('.get("04106") == 253', '.get("04106") == 265').replace("04106 == 253", "04106 == 265").replace("04106==253", "04106==265").replace("skupaj == 253", "skupaj == 265").replace('"04106") == 253', '"04106") == 265').replace("(04106, 253)", "(04106, 265)").replace("== 253,", "== 265,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p20[01234567]_parish*.py")):
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace("04106 == 253", "04106 == 265").replace("04106==253", "04106==265").replace('04106": 253', '04106": 265').replace("skupaj == 253", "skupaj == 265").replace('"04106") == 253', '"04106") == 265').replace("(04106, 253)", "(04106, 265)").replace('byBook"]["04106"] == 253', 'byBook"]["04106"] == 265')
    t = t.replace("vitals == 1472", "vitals == 1484").replace("vitalsTotal == 1472", "vitalsTotal == 1484").replace('vitalsTotal"] == 1472', 'vitalsTotal"] == 1484').replace('!== 1472"', '!== 1484"').replace("1472-številcev", "1484-številcev").replace("vitals-števec-1472", "vitals-števec-1484").replace("vitals-1472", "vitals-1484")
    t = t.replace('"vitalsTotal": 1472', '"vitalsTotal": 1484')
    t = re.sub(r'set\(izven\) == \{"1871"', 'set(izven) == {"1870", "1871"', t)
    t = t.replace('",".join(leta) == "1871,1872', '",".join(leta) == "1870,1871,1872')
    t = t.replace('join(leta) == "1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1484
pt["corpus"]["byBook"]["04106"] = 265
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P207: +12-blokov-1870 (04106 253→265, vitals 1472→1484, ordinali-1–70-ČISTO + h1-Jessernigg + POŽEK-h28-2.leto!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
