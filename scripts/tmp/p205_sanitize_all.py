#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P205 — INSERT qa-p205 + sanitizacija (1444→1461, 225→242, yearset +1872) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p204: MRLIŠKA PREDZGODOVINA 04106 — leto 1873 = 13. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p205-parish-death-1872-04106" not in src
BLOCK = '''
  // ——— qa-p205: MRLIŠKA PREDZGODOVINA 04106 — leto 1872 = 14. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1872 = 114 vpisov (z1–z114, ŠTEVJE-IZ-VRSTIC-7.×!)
  //      / 17 Griblje / 14 hiš + ★★★ MEJA-1871/72-s92 (1871-tail-×3 + 'vsota'-
  //      vrsica-1.×-v-korpusu + 'Jänner'-glava + restart!) + ★★★ 'finis'-s101-
  //      1.× + ★★★ CHOLERA-1872-NASTOP (z78-Jegliče-83J!) + KROP-KOREKCIJE-×5
  //      + h11-NIT-4.-LETO + h44/h62/h6-×2 + PEZDIR-grafia-#11.
  //      Dokaz: parish-death-1872-04106.json; skripte p205.
  {
  const p205Errors: string[] = [];
  const p205Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1872);
  if (p205Death.length !== 17)
    p205Errors.push(`bloki 1872 (04106) ≠ 17 (${p205Death.length} — 17 Griblje-vpisov / 114 vpisov vrstno-štetje!)`);
  const p205Houses = p205Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p205Houses.join(",") !== "1,5,6,6,7,8,11,20,37,38,42,44,44,50,62,62,66")
    p205Errors.push(`hiše 1872 neujemane — najdeno: ${p205Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1461)
    p205Errors.push(`HOUSE_VITALS ≠ 1461 (${HOUSE_VITALS.length} — P204: 1444; P205: + 17 blokov 1872-04106 = 1461!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 242)
    p205Errors.push(`bloki 04106 ≠ 242 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 242!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p205Errors.push("04106-bloki izven {1872, ..., 1885} (predzgodovina: 1857–1871 še nebrani!)");
  if (!p205Death.some((h) => h.houseNo === "42" && h.whatSi.includes("CHOLERA-1872-NASTOP")))
    p205Errors.push("★★★ CHOLERA-1872-NASTOP (z78-Jegliče-83J-Sept — epidemija-1873-začne-tukaj!) ni označena");
  if (!p205Death.some((h) => h.houseNo === "11" && h.whatSi.includes("h11-NIT-4.-LETO")))
    p205Errors.push("★★★ h11-NIT-4.-LETO-1872 (z23-2mes → 1873-63J → 1874-16dni → 1875-KUNIĆ!) ni označena");
  if (!p205Death.some((h) => h.houseNo === "28" && h.whatSi.includes("KROP-KOREKCIJA-ime")))
    p205Errors.push("★★★ KROP-KOREKCIJA ('Žunec'→'PRIMEJ'-2-DNI-Brechruhr!) ni označena");
  if (!p205Death.some((h) => h.houseNo === "38" && h.whatSi.includes("Prilozje-in-Griblje")))
    p205Errors.push("★★★ h38/24-'Prilozje-in-Griblje'-DVOJNA (P204-tail-1:1!) ni označena");
  push(
    "qa-p205-parish-death-1872-04106",
    "P205: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1872 = 14. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s92–s101 == Pag. 87–96 (pag = sken−5; md5-križna-veriga-P197→…→P205-9.×: s100+s101-sveža == P204-disk-1:1!) + **★★★ MEJA-1871/72 = s92 (1871-TAIL-×3-vrste-71–73! + 'VSOTA'-VRSTICA-1.-×-V-KORPUSU ('1-|-8'-VLM-misread-[?'73'?]!) + 'Jänner.'-GLAVA + RESTART-1–9! — VLM-'1877/78'-LETO-HALUCINACIJA-FALSIFICIRANA!)** + **★★★ MEJA-1872/73 = s102 (P204-REUSE-1:1-MD5: '1873.'-glava-v-z1-celici + 'Incipit annus Domini' — POPOLNA-SOGLASJA!)** + **★★★ 'FINIS'-S101-1.×-V-KORPUSU** (Dez-1872-zaključek!) + **★★★ CHOLERA-1872-NASTOP** (z78-Jegliče-83J-Sept — epidemija-1873-začne-tukaj!) + **★★★ 114-VPIISOV-ŠTEVJE-IZ-VRSTIC-7.×** (ordinali-partial-vidni: s101-'102–110'-jasno; vrstna-aritmetika 9+11+13+12+11+11+14+13+12+9 + meseci J21-MAX+F1-MIN+M3+A15+M13+J4+J5+A9+S12+O6+N6+D10!) + **★★★ KROP-KOREKCIJE-×5 (z28-'Žunec'→'PRIMEJ'-otrok-2-DNI! + z35-'Zaupšek'→'Jakofitsch' + z65-'Pegdirec'→'LEGAT' + z78-'Dejak'→'JEGLIČE'-83J + z16-'Vrižan'→'KRIŽAN'-66J!)** + h11-NIT-4.-LETO-1872 (z23-otrok-2mes → 1873-z177-63J → P203-16dni → P202-KUNIĆ-1875 — NEPREKINJENO-4-leta!) + h44-×2-1872 (z26-Bakorić + z28-Primej-2-DNI-v-7-dneh!) + h62-×2 (z85-NEPOZNAN-Dutzbandl + z86-Anna-KHURE!) + h6-×2-v-10-dneh (z35-Jakofitsch-1J + z67-Jakofčič-8Mon!) + PEZDIR-grafia-#11-1872 (z13-'Pecdiac/Kerdise/Perdise'-h50!) + hisna-DUELI-×3 (z43-37/38 + z74-7/3 + z89-8/9/5!) + z111-h38/24-'Prilozje-in-Griblje'-DVOJNA (P204-tail-1:1!) + otroška-umrljivost-47%-8/17-jasna; **1872 = 114 vpisov (z1–z114) / 17 Griblje-vpisov / 14 hiš**; **17 NOVIH BLOKOV parish.ts: vitals 1444 → 1461 · 04106 = 225 → 242 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p205 (fetch-md5 + read + crop + build-entries + merge + build-proof) + qa-p205 (205. kontrola!) + dokaz parish-death-1872-04106.json (114 entries: 17-Griblje + 97-druge! 13-anomalij + 8-crossChecks + honesty-8 + leadP206-1871!) + pt-luknja-REGENERACIJA (242/1461!); **★★★ PREDZGODOVINA-LINIJA-14/29-LET!** (P206-LEAD: 1871 — s92-TAIL-×3-ŽE-VLM-PREBRANA (vrste-71–73 + 'vsota') → probe-s084–s092!)",
    "P205: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1872 = THE 14th YEAR (issue #18): the-frame + **★★★ THE-1871/72-BOUNDARY = s92 (the-1871-TAIL-×3 + the-'VSOTA'-ROW-1st-×-IN-THE-CORPUS + the-'Jänner'-HEAD + RESTART-1–9! — VLM-'1877/78'-YEAR-HALLUCINATION-FALSIFIED!)** + **★★★ THE-1872/73-BOUNDARY = s102 (P204-REUSE-1:1-MD5 — FULL-AGREEMENTS!)** + **★★★ 'FINIS'-S101-1st-×-IN-THE-CORPUS** + **★★★ the-CHOLERA-1872-ONSET** + **★★★ THE-114-ENTRIES-COUNT-FROM-ROWS-7.×** + **★★★ KROP-CORRECTIONS-×5** + the-h11-THREAD-4th-YEAR + h44-×2 + h62-×2 + h6-×2-in-10-DAYS + the-PEZDIR-grafia-#11 + house-DUELS-×3 + the-z111-dual-locality + the-child-mortality-47%; **1872 = 114 entries / 17 Griblje / 14 houses**; **17 NEW BLOCKS: the vitals 1444 → 1461 · the 04106 = 225 → 242**; the scripts p205 + the qa-p205 (the 205th check!) + the evidence parish-death-1872-04106.json (114 entries!) + the pt-gap-REGENERATION (242/1461!); **★★★ THE-PREHISTORY-LINE-14/29-YEARS!** (the P206-LEAD: 1871 — the-s92-TAIL-×3-ALREADY-READ → the-probe-s084–s092!)",
    p205Errors.length === 0,
    p205Errors.length === 0
      ? `17 vpisov / 114 vrstic (števje-iz-vrstic-7.×!) / 14 hiš (×3-×2!) · MEJA-s92-'vsota'-vrsica-1.× + restart-'Jänner'-1872 · 'finis'-s101-1.× · CHOLERA-1872-NASTOP (z78-83J!) · KROP-KOREKCIJE-×5 · h11-NIT-4.-leto · PEZDIR-grafia-#11 · otroška-47% · **PREDZGODOVINA-14/29!** · vitals 1461 · 04106 242 · 04894 520`
      : p205Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1444", "HOUSE_VITALS.length !== 1461")
src = src.replace('04106").length !== 225', '04106").length !== 242')
OLD_SET = "(h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1872 && " + OLD_SET)
src = src.replace("04106-bloki izven {1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1872 še nebrani!)",
                  "04106-bloki izven {1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1871 še nebrani!)")
src = src.replace("vitals 1444 · 04106 225 · 04894 520", "vitals 1461 · 04106 242 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1461')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1444" not in t and "== 225" not in t: continue
    o = t
    t = t.replace("1444", "1461").replace('.get("04106") == 225', '.get("04106") == 242').replace("04106 == 225", "04106 == 242").replace("04106==225", "04106==242").replace("skupaj == 225", "skupaj == 242").replace('"04106") == 225', '"04106") == 242').replace("(04106, 225)", "(04106, 242)").replace("== 225,", "== 242,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p20[01234]_parish*.py")):
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace("04106 == 225", "04106 == 242").replace("04106==225", "04106==242").replace('04106": 225', '04106": 242').replace("skupaj == 225", "skupaj == 242").replace('"04106") == 225', '"04106") == 242').replace("(04106, 225)", "(04106, 242)").replace('byBook"]["04106"] == 225', 'byBook"]["04106"] == 242')
    t = t.replace("vitals == 1444", "vitals == 1461").replace("vitalsTotal == 1444", "vitalsTotal == 1461").replace('vitalsTotal"] == 1444', 'vitalsTotal"] == 1461').replace('!== 1444"', '!== 1461"').replace("1444-številcev", "1461-številcev").replace("vitals-števec-1444", "vitals-števec-1461").replace("vitals-1444", "vitals-1461")
    t = re.sub(r'set\(izven\) == \{"1873"', 'set(izven) == {"1872", "1873"', t)
    t = t.replace('",".join(leta) == "1873,1874', '",".join(leta) == "1872,1873,1874')
    t = t.replace('join(leta) == "1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1461
pt["corpus"]["byBook"]["04106"] = 242
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P205: +17-blokov-1872 (04106 225→242, vitals 1444→1461, 'vsota'-1.× + 'finis'-1.× + CHOLERA-nastop!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
