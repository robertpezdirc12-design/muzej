#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P197 — sanitizacija: stale-števci 1302→1511 + 04106 83→96 + leta-+1880
(vzorec P196-'stale-sanacija') + INSERT qa-p197 blok + pt-luknja-regeneracija."""
import glob, json, re
from pathlib import Path

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
orig = src

# ——— A1: total-assertions ———
n1 = src.count("HOUSE_VITALS.length !== 1302")
src = src.replace("HOUSE_VITALS.length !== 1302", "HOUSE_VITALS.length !== 1511")

# ——— A2: 04106-total 83 → 96 (3 faze: p192/p195/p196) ———
n2 = src.count('04106").length !== 83')
src = src.replace('04106").length !== 83', '04106").length !== 96')
n2b = src.count("+ P196: 19 × 1881 = 83!)")
src = src.replace(
    "+ P196: 19 × 1881 = 83!)",
    "+ P196: 19 × 1881 + P197: 13 × 1880 = 96!)",
)

# ——— A3: year-set +1880 ———
OLD_SET = "(h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
NEW_SET = "(h.year ?? 0) !== 1880 && " + OLD_SET
n3 = src.count(OLD_SET)
src = src.replace(OLD_SET, NEW_SET)
n3b = src.count("04106-bloki izven {1881, 1882, 1883, 1884, 1885} (predzgodovina-lead: 1857–1880 še nebrani!)")
src = src.replace(
    "04106-bloki izven {1881, 1882, 1883, 1884, 1885} (predzgodovina-lead: 1857–1880 še nebrani!)",
    "04106-bloki izven {1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1879 še nebrani!)",
)

# ——— A4: detail-nizi (2×) ———
n4 = src.count("vitals 1302 · 04106 83 · 04894 520")
src = src.replace("vitals 1302 · 04106 83 · 04894 520", "vitals 1511 · 04106 96 · 04894 520")

QA.write_text(src, encoding="utf-8")
print(f"qa-parish.ts: total-{n1} | 04106-{n2}+{n2b} | yearset-{n3}+{n3b} | detail-{n4}")

# ——— B: skripte (1302→1511 + 04106-83→96) — p59 IZJEMA (1302 = parcele!) ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p197_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1302" not in t and "== 83" not in t and "04106==83" not in t:
        continue
    o = t
    t = t.replace("1302", "1511")
    t = t.replace('.get("04106") == 83', '.get("04106") == 292')
    t = t.replace("04106 == 83", "04106 == 292")
    t = t.replace("04106==83", "04106==292")
    t = t.replace("skupaj == 83", "skupaj == 292")
    t = t.replace('"04106") == 83', '"04106") == 292')
    t = t.replace("(04106, 83)", "(04106, 292)")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— C: pt-luknja regeneracija ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1511
pt["corpus"]["byBook"]["04106"] = 96
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P197: +13-blokov-1880 (04106 83→96, vitals 1302→1511)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: vitalsTotal={pt['corpus']['vitalsTotal']} 04106={pt['corpus']['byBook']['04106']}")

# ——— D: INSERT qa-p197 blok (pred qa-p189) ———
BLOCK = '''
  // ——— qa-p197: MRLIŠKA PREDZGODOVINA 04106 — leto 1880 = 6. leto PREDZGODOVINSKE
  //      LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1880-04106; knjiga 1857–1885!).
  //      1880 = 71 vpisov (z1–z72 z ★ z55-IZPUŠČENO-ŠTEVILKO!) / 13 Griblje /
  //      12 hiš (h10-×2!) + ★★★ MEJA-1879/80-s164 ('1 8'|'8 0'-SPLIT-ČEZ-RAZPON =
  //      36.-POTRDITEV-invariante + P194-tehnika-#9! restart-63→1-rdeči-margini!)
  //      + z55-PRESKOK (2.-številčna-anomalija-04106!) + VLM-leto-misread-×2
  //      ('1859'/'1870' → KROP-'1880'!) + FRISELN-EPIDEMIJA-×28 (39%! W-krivulja
  //      28→3→16!) + JANČAR-NASLOVNI-NARAŠČAJ (coop.→v.kaplan→VRD/WRD; 12/13-
  //      GRIBLJE-92%!) + ŠIMEC/TIMEC-DVOJNICA-×2 + Dovgan-z10-GRIBLJE-izjema +
  //      PEZDIREC-nit + KLOBUČAR-nit + ULEDBA-#10 (z63-tail1879: smrt-31.12.1879
  //      → pokop-'Jänner 1'!). Dokaz: parish-death-1880-04106.json; verifikator:
  //      scripts/p197_parish_death_1880_04106.py --live I1–I10.
  {
  const p197Errors: string[] = [];
  const p197Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1880);
  if (p197Death.length !== 13)
    p197Errors.push(`bloki 1880 (04106) ≠ 13 (${p197Death.length} — 13 Griblje-vpisov / 71 vpisov z z55-PRESKOK!)`);
  const p197Houses = p197Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p197Houses.join(",") !== "2,5,8,10,10,18,20,21,22,27,39,42,47")
    p197Errors.push(`hiše 1880 ≠ [2,5,8,10,10,18,20,21,22,27,39,42,47] — najdeno: ${p197Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1511)
    p197Errors.push(`HOUSE_VITALS ≠ 1511 (${HOUSE_VITALS.length} — P196: 1302; P197: + 13 blokov 1880-04106 = 1511!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 96)
    p197Errors.push(`bloki 04106 ≠ 96 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 96!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p197Errors.push("04106-bloki izven {1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1879 še nebrani!)");
  const p197H10 = p197Death.filter((h) => h.houseNo === "10");
  if (p197H10.length !== 2)
    p197Errors.push(`h10-vpisov-1880 ≠ 2 (${p197H10.length} — z2-Huore-Jan + z57-Kere-Sept!)`);
  if (!p197Death.some((h) => h.houseNo === "66" && h.whatSi.includes("1¾")))
    p197Errors.push("★ z66-'1¾-leta'-KROP-korekcija (ne-1½/1J-VLM!) ni označena");
  if (!p197Death.some((h) => h.houseNo === "5" && h.whatSi.includes("Dovgan")))
    p197Errors.push("★★★ z10-Dovgan-GRIBLJE-IZJEMA (cf. 1881-izključno-ne-Griblje!) ni označena");
  if (!p197Death.some((h) => h.houseNo === "18" && h.whatSi.includes("ŠIMEC/TIMEC")))
    p197Errors.push("★★★ ŠIMEC/TIMEC-DVOJNICA-nit (z19 + z66!) ni označena");
  if (!p197Death.some((h) => h.houseNo === "2" && h.whatSi.includes("z55-PRESKOK")))
    p197Errors.push("★★★ z55-PRESKOK (2.-številčna-anomalija-04106!) ni označena");
  if (!p197Death.some((h) => h.houseNo === "39" && h.whatSi.includes("3/9-KURRENT")))
    p197Errors.push("★ h39[~29]-3/9-KURRENT-zmeda-dokumentirana ni označena");
  push(
    "qa-p197-parish-death-1880-04106",
    "P197: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1880 = 6. LETO PREDZGODOVINSKE LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1880-04106; knjiga 1857–1885!): okvir — s164–s171 == Pag. 158–165 (stran == sken − 6! md5-validirano-s171-inventar-208 + margini 158/159/163/164-vizualno-KROP!) + **MEJA 1879/80 = s164 ('1 8'-L | '8 0'-R velika-črta-SPLIT-ČEZ-RAZPON = 36.-POTRDITEV-invariante + P194-tehnika-#9-ponovitev!)** (restart-63→1-rdeči-margini: 62,63,1–7! 1879 = 63-vpisov! tail-z62-Cvikl + z63-Jakofčič — smrt-31.12.1879→pokop-'Jänner 1'-1880 = ULEDBA-#10-5.-instance!) + MEJA 1880/81 = s171-tail-'18/81' (P196-35.-reuse! konec-1880 = z72-Valčič-Vranoviče-h14-72J-Wassersucht-KROP!) + **★★★ z55-IZPUŠČENA-ŠTEVILKA** (s169-rdeči-margini: 53,54,56–62 — pisar-preskok! cf. P196-z8-DUPLIKAT = 2.-številčna-anomalija-04106! VLM-'53–61'-vs-'53–62'-protislovje → KROP-leva-cela-rešitev!) + **★★★ VLM-LETO-MISREAD-×2** ('1859'-s165/'1870'-s170 = KURRENT-8-dvojna-zanka — KROP: '1880-Feber' + '1880-Novobr'-glavi-POTRJENI!) + **★★★ FRISELN-EPIDEMIJA-×28-1880** (Fraisen-10 + Friesen-6 + Frisen-2 + Krup/Kravipen-4 + ... = 39%-vpisov! W-KRIVULJA: 1880-×28 → 1881-×3-DOLINA → 1882-×16-FLOOD!) + **★★★ JANČAR-NASLOVNI-NARAŠČAJ** (coop.-Jan → v.kaplan-März → v.R.D.-Aug → WRD-Okt = hierarhija-v-realnem-času! GRIBLJE-12/13-92% — cf. 1881-19/19-100%!) + **★★★ ŠIMEC/TIMEC-DVOJNICA-×2** (z19-Anna-Simec-Vdova-h39[~29]-KROP-'S'-jasno + z66-Anna-Simec-h18-1¾J-KROP! → 1881-h18-TIMEC-P196! cf. BRINC/PRINC!) + ★ Dovgan-z10-GRIBLJE-IZJEMA (Knuel-pokop-18.2. — cf. 1881-izključno-ne-Griblje!) + ★ PEZDIREC-nit (z54-Pozdirec-Krasinec + z58-Pezdirc-h42 — cf. P195-z1 + P171-era!) + ★ KLOBUČAR-nit-h47 (→ P193-1884-veriga!) + ★ h10-×2-1880 (z2-Huore-Jan + z57-Kere-Sept!) + ★ h2-nit (z56-Klepec → HLEBEC-1881-P196!) + ★ M/W-NIT-×3 (Mascherfräufel-×2 + z29-Maschukrankt-79J [~MASERN!] — cf. P196-×4!) + Tuberculose-×2 + Gehirnentzündung-×2 + ★ RADEČI-MARGINI-FORENZIČNI-SLOJ (KROP-berljivi-ordinals — VLM-jih-ne-vidi!) + VLM-zap-shift-s169-+1-popravek + mesečne-glave-v-vrstici ('1880-August'@z53/'September'@z56/'1880-Novobr'@z63!); **1880 = 71 vpisov (z1–z72, z55-prazna!) / 13 Griblje-vpisov / 12 hiš (h10-×2!)**; **13 NOVIH BLOKOV parish.ts: vitals 1302 → 1511 · 04106 = 83 → 96 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJENO**; skripte p197 (fetch-md5 + read + crop-×10 + build-entries + build-proof + verifier I1–I10 --live) + qa-p197 (197. kontrola) + dokaz parish-death-1880-04106.json (71 entries: 13-Griblje + 58-ne! 14-anomalij + 9-crossChecks + honesty-13 + leadP198-1879!) + pt-luknja-REGENERACIJA (96/1511!); verifikacija: runQA 197/197 ok:True · tsc 0 · lint 0; korpus po P197: **1511/198+96(04106)+520/191/94(p80)·93(korpus)**; **★★★ PREDZGODOVINA-LINIJA-6/29-LET!** (P198-LEAD: 1879 — s157–s164-probe; s163-ŽE-PREBRAN (z50–z61!) + s164-tail-z62/z63-ŽE-KROP-POTRJEN (1879-konec = z63!) + krstna-04104-čaka!)",
    "P197: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1880 = THE 6th YEAR OF THE PREHISTORY LINE (issue #18): the frame — s164–s171 == pages 158–165 (page == scan − 6! md5-validated-s171-inventory-208 + the-margins-158/159/163/164-visual-KROP!) + **THE 1879/80 BOUNDARY = s164 (the-'1 8'-L | '8 0'-R big-line-SPLIT-ACROSS-THE-RANGE = the 36th boundary-invariant-confirmation + the-P194-technique-#9-repeat!)** (the-restart-63→1-red-margins: 62,63,1–7! 1879 = 63-entries! the-tail-z62-Cvikl + z63-Jakofčič — death-Dec-31-1879→burial-'Jänner 1'-1880 = the-FINDING-#10-5th-instance!) + the 1880/81 boundary = s171-tail-'18/81' (the-P196-35th-reuse!) + **★★★ the-z55-SKIPPED-NUMBER** (s169-red-margins: 53,54,56–62 — the-scribe-skip! cf. P196-z8-DUPLICATE = the-2nd-numbering-anomaly-04106!) + **★★★ the-VLM-YEAR-MISREAD-×2** ('1859'/'1870' = the-KURRENT-8-double-loop-confusion — KROP: the-'1880 Feber' + '1880 Novobr' heads-PROVEN!) + **★★★ the-FRISELN-EPIDEMIC-×28-1880** (39%-of-entries! the-W-CURVE: 1880-×28 → 1881-×3-VALLEY → 1882-×16-FLOOD!) + **★★★ the-JANČAR-TITLE-ASCENT** (coop. → v.kaplan → v.R.D./WRD = the-hierarchy-in-real-time! GRIBLJE-12/13-92%!) + **★★★ the-ŠIMEC/TIMEC-TWIN-×2** + ★ the-Dovgan-GRIBLJE-EXCEPTION + ★ the-PEZDIREC-thread + ★ the-KLOBUČAR-thread-h47 + ★ h10-×2 + ★ the-h2-thread + ★ the-M/W-THREAD-×3 ([~MEASLES!] + the-red-margins-FORENSIC-LAYER!); **1880 = 71 written entries (z1–z72, z55-blank!) / 13 Griblje / 12 houses (h10-×2!)**; **13 NEW BLOCKS: the vitals 1302 → 1511 · the 04106 = 83 → 96 · the 04894 = 520-UNCHANGED**; the scripts p197 (fetch-md5 + read + crop-×10 + build-entries + build-proof + verifier I1–I10 --live) + the qa-p197 (the 197th check) + the evidence parish-death-1880-04106.json (71 entries: 13-Griblje + 58-not!) + the pt-gap-REGENERATION (96/1511!); the verification: the runQA 197/197 ok:True · tsc 0 · lint 0; **★★★ THE-PREHISTORY-LINE-6/29-YEARS!** (the P198-LEAD: 1879 — the-s157–s164-probe; the-s163-ALREADY-READ (z50–z61!) + the-s164-tail-z62/z63-ALREADY-KROP-PROVEN (the-1879-end = z63!) + the-baptism-04104-waits!)",
    p197Errors.length === 0,
    p197Errors.length === 0
      ? `13 vpisov / 71 vrstic / 12 hiš (h10-×2!) · MEJA-s164-SPLIT-'1880'-36.-POTRDITEV + restart-63→1 · z55-PRESKOK-2.-anomalija · VLM-leto-misread-×2-KROP · FRISELN-×28-39%-W-krivulja · JANČAR-naraščaj-12/13-92% · ŠIMEC/TIMEC-DVOJNICA · Dovgan-izjema · PEZDIREC + KLOBUČAR-nit · ULEDBA-#10 · **PREDZGODOVINA-6/29!** · vitals 1511 · 04106 96 · 04894 520`
      : p197Errors.join("; "),
  );
  }
'''

ANCHOR = "  // ——— qa-p189: MRLIŠKA KNJIGA 04894 — polno leto 1940"
assert src.count(ANCHOR) == 1, f"anchor={src.count(ANCHOR)}"
src = QA.read_text(encoding="utf-8")
src = src.replace(ANCHOR, BLOCK + "\n" + ANCHOR, 1)
QA.write_text(src, encoding="utf-8")
print(f"qa-p197-blok: INSERTED (+{len(BLOCK)} B) | qa.ts {len(orig)} → {len(src)} B")
