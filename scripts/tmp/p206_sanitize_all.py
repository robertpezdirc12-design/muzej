#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P206 — INSERT qa-p206 + sanitizacija (1461→1472, 242→253, yearset +1871) + verifier-patch + pt-luknja."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p205: MRLIŠKA PREDZGODOVINA 04106 — leto 1872 = 14. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p206-parish-death-1871-04106" not in src
BLOCK = '''
  // ——— qa-p206: MRLIŠKA PREDZGODOVINA 04106 — leto 1871 = 15. leto PREDZGODOVINSKE
  //      LINIJE (issue #18). 1871 = 73 vpisov (ordinali-1–73: LUK-18-pisarski-
  //      preskok + DUP-19-×2-s88!, ŠTEVJE-IZ-VRSTIC-8.×!) / 11 Griblje / 11 hiš
  //      (vsi-različni!) + ★★★ MEJA-1870/71-s86 (1870-tail-×7 + 'vsota'-'1|8'-2.×
  //      + 'Jänner'-glava + restart!) + ★★★ MEJA-1871/72-s92 ('December-1871'-
  //      glava-KROP-1:1-P205!) + ★★★ h11-NIT-5.-LETO (z5-Plut-13J!) + ime-DUEL-z17
  //      + stan-'Ablasser'-z29 + KROP-SOGLASJE-z50-5¾J.
  //      Dokaz: parish-death-1871-04106.json; skripte p206.
  {
  const p206Errors: string[] = [];
  const p206Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1871);
  if (p206Death.length !== 11)
    p206Errors.push(`bloki 1871 (04106) ≠ 11 (${p206Death.length} — 11 Griblje-vpisov / 73 vpisov vrstno-štetje!)`);
  const p206Houses = p206Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p206Houses.join(",") !== "2,8,11,13,28,29,33,38,65,66,72")
    p206Errors.push(`hiše 1871 neujemane — najdeno: ${p206Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1472)
    p206Errors.push(`HOUSE_VITALS ≠ 1472 (${HOUSE_VITALS.length} — P205: 1461; P206: + 11 blokov 1871-04106 = 1472!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 253)
    p206Errors.push(`bloki 04106 ≠ 253 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P206: 11 × 1871 + P205: 17 × 1872 + P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 253!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1871 && (h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p206Errors.push("04106-bloki izven {1871, ..., 1885} (predzgodovina: 1857–1870 še nebrani!)");
  if (!p206Death.some((h) => h.houseNo === "11" && h.whatSi.includes("h11-NIT-5.-LETO-1871")))
    p206Errors.push("★★★ h11-NIT-5.-LETO-1871 (z5-Plut-13J → 1872-z23 → 1873-63J → 1874-16dni → 1875-KUNIĆ!) ni označena");
  if (!p206Death.some((h) => h.houseNo === "13" && h.whatSi.includes("ime-DUEL")))
    p206Errors.push("★★★ ime-DUEL-z17 (VLM-'Maria-Jančarič' vs KROP-'Anton-Grüblner-Tonis'!) ni označena");
  if (!p206Death.some((h) => h.houseNo === "66" && h.whatSi.includes("Ablasser")))
    p206Errors.push("★★★ stan-'Ablasser'-z29 (odpustitelj — 1.×-v-korpusu!) ni označena");
  if (!p206Death.some((h) => h.houseNo === "28" && h.whatSi.includes("KROP-POPOLNO-SOGLASJE")))
    p206Errors.push("★★★ KROP-POPOLNO-SOGLASJE-z50 (5¾-J!) ni označena");
  push(
    "qa-p206-parish-death-1871-04106",
    "P206: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1871 = 15. LETO PREDZGODOVINSKE LINIJE (issue #18): okvir — s86–s92 == Pag. 81–87 (pag = sken−5; md5-križna-veriga-P197→…→P206-10.×: s92-sveža == P205-disk-1:1!) + **★★★ MEJA-1870/71 = s86 (1870-TAIL-×7-zap-64–70 + 'VSOTA'-'1|8'-2.×-V-KORPUSU + 'Jänner'-glava + RESTART! — s84/s85-1870-kontekst + '1876'-glava-MISREAD-falsificirana!)** + **★★★ MEJA-1871/72 = s92 ('December-1871'-glava-KROP-1:1-s-P205-soglasje!)** + **★★★ 73-VPIISOV-ŠTEVJE-IZ-VRSTIC-8.×** (ordinali-1–73: LUK-18-pisarski-preskok (s87-zap-17→s88-zap-19! — vzorec-P204-luknje!) + DUP-19-×2-s88 (r1-Drugoše-Kumin + r2-Primostek-Klavec! — vzorec-P204-dupkatov!) + ord-stolpec-cele-s88-×3.5-branje '19,19,20,21,…,30' + vrstna-aritmetika 4+13+13+14+14+12+3 + meseci J6+F6+M5+A10+M4+J2+J3+A11-MAX+S7+O8+N3+D8!) + **★★★ h11-NIT-5.-LETO-1871** (z5-Josef-Plut-13J-Gehirnentzündung → 1872-z23-otrok-2mes → 1873-z177-63J → 1874-16dni → 1875-KUNIĆ — NEPREKINJENO-5-let!) + **★★★ ime-DUEL-z17** (VLM-'Maria-Jančarič-110J[?]' vs KROP-'Anton-Grüblner-Tonis'!) + **★★★ stan-'ABlasser'-z29** (odpustitelj — 1.×-v-korpusu!) + **★★★ KROP-POPOLNO-SOGLASJE-z50** (5¾-J vs '5let[~5½]'; '¼-Griblerjev-sohn'!) + ordinala-DUEL-z20 (Arik-vs-Urih; hišna-33-vs-62/65!) + KROP-y-drift-LEKCIJA-#22 (ob-mesečnih-glavah-izrezi-zadenejo-sosednje-vrste — celostanska-osnova-za-pozicije!); **1871 = 73 vpisov (z1–z73) / 11 Griblje-vpisov / 11 hiš-vsi-RAZLIČNI**; **11 NOVIH BLOKOV parish.ts: vitals 1461 → 1472 · 04106 = 242 → 253 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p206 (fetch-md5 + read + krop-×3-kroga + build-entries + merge + build-proof) + qa-p206 (206. kontrola!) + dokaz parish-death-1871-04106.json (73 entries: 11-Griblje + 62-druge!) + pt-luknja-REGENERACIJA (253/1472!); **★★★ PREDZGODOVINA-LINIJA-15/29-LET!** (P207-LEAD: 1870 — s86-TAIL-×7-zap-64–70-ŽE-VLM-PREBRANA (Dec-1870 + 'vsota') → probe-s078–s086!)",
    "P206: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1871 = THE 15th YEAR (issue #18): the-frame + **★★★ THE-1870/71-BOUNDARY = s86 (the-1870-TAIL-×7 + the-'VSOTA'-'1|8'-2nd-×-IN-THE-CORPUS + the-'Jänner'-HEAD + RESTART!)** + **★★★ THE-1871/72-BOUNDARY = s92 ('December-1871'-head-KROP-1:1-with-P205!)** + **★★★ THE-73-ENTRIES-COUNT-FROM-ROWS-8.×** (ordinals-1–73: the-LUK-18-scribe-skip + the-DUP-19-×2 + the-ordinal-column-full-s88-×3.5-reading '19,19,20,21,…,30'!) + **★★★ the-h11-THREAD-5th-YEAR-1871** + **★★★ the-ime-DUEL-z17** + **★★★ the-stan-'ABlasser'-z29** + **★★★ KROP-FULL-AGREEMENT-z50** + the-ordinal-DUEL-z20 + the-KROP-y-drift-LESSON-#22; **1871 = 73 entries / 11 Griblje / 11 houses-ALL-DIFFERENT**; **11 NEW BLOCKS: the vitals 1461 → 1472 · the 04106 = 242 → 253**; the scripts p206 + the qa-p206 (the 206th check!) + the evidence parish-death-1871-04106.json (73 entries!) + the pt-gap-REGENERATION (253/1472!); **★★★ THE-PREHISTORY-LINE-15/29-YEARS!** (the P207-LEAD: 1870 — the-s86-TAIL-×7-ALREADY-READ → the-probe-s078–s086!)",
    p206Errors.length === 0,
    p206Errors.length === 0
      ? `11 vpisov / 73 vrstic (števje-iz-vrstic-8.×! LUK-18 + DUP-19!) / 11 hiš-vsi-različni · MEJA-s86-'vsota'-'1|8'-2.× + restart-'Jänner'-1871 · 'December-1871'-glava-KROP · h11-NIT-5.-leto (z5-Plut-13J!) · ime-DUEL-z17 · stan-'Ablasser'-z29 · KROP-SOGLASJE-z50-5¾J · otroška-18%-2/11 · **PREDZGODOVINA-15/29!** · vitals 1472 · 04106 253 · 04894 520`
      : p206Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1461", "HOUSE_VITALS.length !== 1472")
src = src.replace('04106").length !== 242', '04106").length !== 253')
OLD_SET = "(h.year ?? 0) !== 1872 && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1871 && " + OLD_SET)
src = src.replace("04106-bloki izven {1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1871 še nebrani!)",
                  "04106-bloki izven {1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1870 še nebrani!)")
src = src.replace("vitals 1461 · 04106 242 · 04894 520", "vitals 1472 · 04106 253 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: {src.count('HOUSE_VITALS.length !== 1472')}")

files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_", "p205_", "p206_")
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1461" not in t and "== 242" not in t: continue
    o = t
    t = t.replace("1461", "1472").replace('.get("04106") == 242', '.get("04106") == 253').replace("04106 == 242", "04106 == 253").replace("04106==242", "04106==253").replace("skupaj == 242", "skupaj == 253").replace('"04106") == 242', '"04106") == 253').replace("(04106, 242)", "(04106, 253)").replace("== 242,", "== 253,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p20[012345]_parish*.py")):
    t = f.read_text(encoding="utf-8"); o = t
    t = t.replace("04106 == 242", "04106 == 253").replace("04106==242", "04106==253").replace('04106": 242', '04106": 253').replace("skupaj == 242", "skupaj == 253").replace('"04106") == 242', '"04106") == 253').replace("(04106, 242)", "(04106, 253)").replace('byBook"]["04106"] == 242', 'byBook"]["04106"] == 253')
    t = t.replace("vitals == 1461", "vitals == 1472").replace("vitalsTotal == 1461", "vitalsTotal == 1472").replace('vitalsTotal"] == 1461', 'vitalsTotal"] == 1472').replace('!== 1461"', '!== 1472"').replace("1461-številcev", "1472-številcev").replace("vitals-števec-1461", "vitals-števec-1472").replace("vitals-1461", "vitals-1472")
    t = re.sub(r'set\(izven\) == \{"1872"', 'set(izven) == {"1871", "1872"', t)
    t = t.replace('",".join(leta) == "1872,1873', '",".join(leta) == "1871,1872,1873')
    t = t.replace('join(leta) == "1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1472
pt["corpus"]["byBook"]["04106"] = 253
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P206: +11-blokov-1871 (04106 242→253, vitals 1461→1472, LUK-18 + DUP-19 + h11-nit-5.leto + 'Ablasser'!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
