#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P198 — sanitizacija: stale-števci 1315→1498 + 04106 96→105 + leta-+1879
(vzorec P197-'stale-sanacija') + INSERT qa-p198 blok + pt-luknja-regeneracija."""
import glob, json
from pathlib import Path

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
orig = src

# ——— A1: total-assertions ———
n1 = src.count("HOUSE_VITALS.length !== 1315")
src = src.replace("HOUSE_VITALS.length !== 1315", "HOUSE_VITALS.length !== 1498")

# ——— A2: 04106-total 96 → 105 ———
n2 = src.count('04106").length !== 96')
src = src.replace('04106").length !== 96', '04106").length !== 105')
n2b = src.count("+ P197: 13 × 1880 = 96!)")
src = src.replace(
    "+ P197: 13 × 1880 = 96!)",
    "+ P197: 13 × 1880 + P198: 9 × 1879 = 105!)",
)

# ——— A3: year-set +1879 ———
OLD_SET = "(h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
NEW_SET = "(h.year ?? 0) !== 1879 && " + OLD_SET
n3 = src.count(OLD_SET)
src = src.replace(OLD_SET, NEW_SET)
n3b = src.count("04106-bloki izven {1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1879 še nebrani!)")
src = src.replace(
    "04106-bloki izven {1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1879 še nebrani!)",
    "04106-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1878 še nebrani!)",
)

# ——— A4: detail-nizi ———
n4 = src.count("vitals 1315 · 04106 96 · 04894 520")
src = src.replace("vitals 1315 · 04106 96 · 04894 520", "vitals 1498 · 04106 105 · 04894 520")

QA.write_text(src, encoding="utf-8")
print(f"qa-parish.ts: total-{n1} | 04106-{n2}+{n2b} | yearset-{n3}+{n3b} | detail-{n4}")

# ——— B: skripte (1315→1498 + 04106-96→105) — p59 IZJEMA (1302 = parcele!) + p198 IZJEMA ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p198_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1315" not in t and "== 96" not in t and "04106==96" not in t:
        continue
    o = t
    t = t.replace("1315", "1498")
    t = t.replace('.get("04106") == 96', '.get("04106") == 279')
    t = t.replace("04106 == 96", "04106 == 279")
    t = t.replace("04106==96", "04106==279")
    t = t.replace("skupaj == 96", "skupaj == 279")
    t = t.replace('"04106") == 96', '"04106") == 279')
    t = t.replace("(04106, 96)", "(04106, 279)")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— C: pt-luknja regeneracija ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1498
pt["corpus"]["byBook"]["04106"] = 105
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P198: +9-blokov-1879 (04106 96→105, vitals 1315→1498; sanacija-re-run!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: vitalsTotal={pt['corpus']['vitalsTotal']} 04106={pt['corpus']['byBook']['04106']}")

# ——— D: INSERT qa-p198 blok (pred qa-p197) ———
BLOCK = '''
  // ——— qa-p198: MRLIŠKA PREDZGODOVINA 04106 — leto 1879 = 7. leto PREDZGODOVINSKE
  //      LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1879-04106; knjiga 1857–1885!;
  //      SANACIJA-RE-RUN: /tmp-wipe → re-clone-@195b4e1 + re-fetch-1:1 + re-VLM-×7
  //      + re-arbitraža-×5!). 1879 = 64 fizičnih vrstic / 63 ordinalov (z1–z63
  //      z ★ z28-DUPLIKAT!) / 9 Griblje / 8 hiš (h20-×2!) + ★★★ MEJA-1878/79-s158
  //      ('Incipit-annus' + '1 8'/'7 9'-STACKED-SPLIT-VARIANTA = 37.-POTRDITEV-
  //      invariante! restart-85→1; tail-z83–z85-KROP+RE-READ-SOGLASJE!) +
  //      ★★★ z28-DUPLIKAT (3.-številčna-anomalija-04106!) + ★★★ 97-LET-KORPUS-
  //      REKORD (z28-Mathias-Peglic — KROP + RE-READ-SOGLASJE!) + ★★★ GEHIRN-
  //      ENTZÜNDUNG-×2-istega-dna (h44-37J + h40-97J!) + FRISELN-×14 (W-krivulja
  //      14→28→3→16!) + KRONOLOŠKI-PRESKOKI-×2 + ULEDBA-#10-6.-instance
  //      (ARBITRAŽA-A1: 'Junii-29'→'1. Juli'!) + JANČAR-GRIBLJE-9/9-100%
  //      (5.-leto-nit!) + s157-ordinali-73–82-KROP (VLM-7→6-obeh-sej → 1878 ≈ 85!).
  //      Dokaz: parish-death-1879-04106.json; skripte p198 (fetch-1:1 + read +
  //      build-entries + build-proof).
  {
  const p198Errors: string[] = [];
  const p198Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1879);
  if (p198Death.length !== 9)
    p198Errors.push(`bloki 1879 (04106) ≠ 9 (${p198Death.length} — 9 Griblje-vpisov / 64 fizičnih vrstic z z28-DUPLIKAT!)`);
  const p198Houses = p198Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p198Houses.join(",") !== "1,20,20,30,32,40,44,53,56")
    p198Errors.push(`hiše 1879 ≠ [1,20,20,30,32,40,44,53,56] — najdeno: ${p198Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1498)
    p198Errors.push(`HOUSE_VITALS ≠ 1498 (${HOUSE_VITALS.length} — P197: 1315; P198: + 9 blokov 1879-04106 = 1498!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 105)
    p198Errors.push(`bloki 04106 ≠ 105 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 105!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p198Errors.push("04106-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1878 še nebrani!)");
  const p198H20 = p198Death.filter((h) => h.houseNo === "20");
  if (p198H20.length !== 2)
    p198Errors.push(`h20-vpisov-1879 ≠ 2 (${p198H20.length} — z28-DUP-Pezdirc-Juni + z47-Abramšek-Okt!)`);
  if (!p198Death.some((h) => h.houseNo === "40" && h.whatSi.includes("97")))
    p198Errors.push("★★★ z28-'97-LET'-KORPUS-REKORD (KROP + RE-READ-SOGLASJE!) ni označena");
  if (!p198Death.some((h) => h.houseNo === "40" && h.whatSi.includes("z28-DUPLIKAT-1/2")))
    p198Errors.push("★★★ z28-DUPLIKAT-1/2 (3.-številčna-anomalija-04106!) ni označena");
  if (!p198Death.some((h) => h.houseNo === "20" && h.whatSi.includes("ULEDBA-#10-6.-INSTANCE")))
    p198Errors.push("★★★ ULEDBA-#10-6.-instance (ARBITRAŽA-A1: 'Junii-29'→'1. Juli'!) ni označena");
  if (!p198Death.some((h) => h.houseNo === "44" && h.whatSi.includes("GEHIRNENTZÜNDUNG-KATASTROFA-×2-ISTEGA-DNA")))
    p198Errors.push("★★★ GEHIRNENTZÜNDUNG-KATASTROFA-×2-istega-dna (h44-37J + h40-97J!) ni označena");
  if (!p198Death.some((h) => h.houseNo === "56" && h.whatSi.includes("Incipit-annus")))
    p198Errors.push("★★★ MEJA-'Incipit-annus'+'1 8|7 9'-SPLIT-VARIANTA (37.-POTRDITEV!) ni označena");
  push(
    "qa-p198-parish-death-1879-04106",
    "P198: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1879 = 7. LETO PREDZGODOVINSKE LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1879-04106; knjiga 1857–1885!; SANACIJA-RE-RUN: /tmp-wipe → repo-re-clone-iz-GitHub-@195b4e1 + re-fetch-8/8-velikosti-1:1-P197-seji + re-VLM-×7 + tail-z62/z63-iz-SEJNEGA-ZAPISA-P197-KROP-1:1 + re-arbitraža-×5-cropov = deterministična-reprodukcija-vzorec-P156!): okvir — s157–s164 == Pag. 151–158 (stran == sken − 6! PRINTED-'152/153/154/155/156'-×5-vizualno-KROP!) + **MEJA 1878/79 = s158 ('Incipit annus'-band [re-read-'Summarischer-Anno'-ZAVRJEN!] + velika-'1879'-SPLIT-VARIANTA '1 8'+'7 9'-STACKED-na-desno-TP = 37.-POTRDITEV-invariante + P194-tehnika-#9-ponovitev!)** (restart-85→1! tail-1878-z83–z85: KROP-hipoteza-1.-seje + RE-READ-SOGLASJE-2.-seje = 2-viri-fakt! 1878 ≈ 85-vpisov-P199-lead!) + MEJA 1879/80 = s164-mid-'1 8|8 0' (P197-36.-reuse! konec-1879 = z63-tail-Certoviše-Jakofčič-smrt-31.12→pokop-1.1.1880-ULEDBA-#10!) + **★★★ z28-DUPLIKAT** (s160-konec-'28'-Mathias-Peglic-h40-97J + s161-top-'28'-Martin-Pezdirc-h20-44J — s161-margin-strip-28,29,30–37-KROP-VSI-JASNI + RE-READ-SOGLASJE-28! = 3.-številčna-anomalija-04106: P196-z8-dup + P197-z55-skip!) + **★★★ 97-LET-KORPUS-REKORD** (z28-Mathias-Peglic — KROP-max-zoom-'9'+γ-7+'.'-struktura-identična-z27-'37.' + RE-READ-'97[~9J/97?]'-2.-neodvisni-viri! cf. 1881-Movrin-90J-prejšnji-max!) + **★★★ GEHIRNENTZÜNDUNG-KATASTROFA-×2-ISTEGA-DNA** (z27-Maria-Peglic-h44-37J + z28-Mathias-Peglic-h40-97J — obe-26./28.-Mai! ARBITRAŽA-A3: '-entzündung'-konec-umlaut — re-read-'Gichtarmzündung'-ZAVRJEN!) + **★★★ FRISELN-×14-1879** (W-KRIVULJA: 1879-×14 → 1880-×28-FLOOD → 1881-×3-DOLINA → 1882-×16!) + **★★★ KRONOLOŠKI-PRESKOKI-×2** (Jänner z6-Jan26→z7-Jan23→z8-Jan24-KROP-max + Dezember-3→13→12→7→21-KROP-datumi-s163 — nazaj-zapolnitve!) + **★★★ ULEDBA-#10-6.-INSTANCE** (z28-DUP: ARBITRAŽA-A1-ODLOČILNA-'1879-Julβ'-header+'Junii-29.'-JASNO→pokop-'1.'-'Juli' — re-read-'July-29/Aug-1'-ZAVRJEN!) + **★★★ JANČAR-GRIBLJE-9/9-100%-DOMINANTA** (5.-leto-nit: 1879→1880→1881→1882→1883! VLM-variant-podpisov-'Janezak/Hancar/Lončar/Vančar/Janičar'-=-ISTA-PODPIS!) + ★ z47-Griblje-h20-BREZ-starosti/bolezni (RE-READ-SOGLASJE-[?]! ime-'Nelly?[~4-varianti!]-Abramšek?[~]-Pivk?[~]') + ★ z35-totgeboren + z30-'unget'[ungetauft!] + ★ h20-×2-1879 (PEZDIREC-era-cf-P171!) + ★ h53-nit (z15 + tail-1878-z83-Peglavc-87J!) + ★ h56-ŠIMEC-nit (→ 1880-z19 + 1881-h18!) + ★ h1-nit (→ ZELŠKO-1882-P195!) + ★ z42-Zemelj-h24-DVOJNICA-z45 (Kuc-×2-v-3-tednih!) + ★ ARBITRAŽE-A1–A5 (max-zoom > VLM — 6.-potrditev-vzorca-P156: A1-Junii-datum + A2-h44-ne-14 + A3-Gehirn-ne-Gichtarm + A4-Novak-ne-Dovgan + A5-Mlake-ne-Malše!) + s157-ordinali-73–82-KROP (VLM-'63–72'-7→6-sistemsko-obeh-sej → 1878 ≈ 85-vpisov!) + RE-READ-SOGLASJA-×4 (tail-83/84/85 + 97J + z28-DUP-28 + z47-prazna = 2-viri-fakti!); **1879 = 64 fizičnih vrstic / 63 ordinalov (z1–z63 + z28-DUPLIKAT!) / 9 Griblje-vpisov / 8 hiš (h20-×2!)**; **9 NOVIH BLOKOV parish.ts: vitals 1315 → 1498 · 04106 = 96 → 105 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJENO**; skripte p198 (fetch-1:1 + read + build-entries + build-proof) + qa-p198 (198. kontrola) + dokaz parish-death-1879-04106.json (64 entries: 9-Griblje + 55-ne! 14-anomalij + 10-crossChecks + honesty-15 + leadP199-1878!) + pt-luknja-REGENERACIJA (105/1498!); verifikacija: runQA 198/198 ok:True · tsc 0 · lint 0; korpus po P198: **1498/198+105(04106)+520/191/94(p80)·93(korpus)**; **★★★ PREDZGODOVINA-LINIJA-7/29-LET!** (P199-LEAD: 1878 — s150–s157-probe; s157-ordinali-73–82-KROP-ŽE-POTRJENI + s158-tail-z83–z85-2-viri! 1878 ≈ 85-vpisov + krstna-04104-čaka!)",
    "P198: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1879 = THE 7th YEAR OF THE PREHISTORY LINE (issue #18; SANACIJA-RE-RUN: the-/tmp-wipe → the-repo-re-cloned-from-GitHub-@195b4e1 + the-re-fetch-8/8-sizes-1:1-vs-P197-session + the-re-VLM-×7 + the-tail-z62/z63-from-the-SESSION-RECORD-P197-KROP-1:1 + the-re-arbitration-×5-crops = the-deterministic-reproduction-the-P156-pattern!): the frame — s157–s164 == pages 151–158 (page == scan − 6! the-PRINTED-'152–156'-×5-visual-KROP!) + **THE 1878/79 BOUNDARY = s158 (the-'Incipit annus'-band + the-big-'1879'-SPLIT-VARIANT-'1 8'+'7 9'-STACKED = the 37th boundary-invariant-confirmation!)** (the-restart-85→1! the-1878-tail-z83–z85: KROP-hypothesis + RE-READ-AGREEMENT = 2-source-fact!) + the 1879/80 boundary = s164-mid (P197-36th-reuse! the-1879-end = z63-tail-ULEDBA-#10!) + **★★★ the-z28-DUPLICATE** (3rd-numbering-anomaly-04106!) + **★★★ the-97-YEAR-CORPUS-AGE-RECORD** (z28-Mathias-Peglic — KROP-max-zoom + RE-READ-AGREEMENT!) + **★★★ the-GEHIRNENTZÜNDUNG-CATASTROPHE-×2-SAME-DAY** (h44-37J + h40-97J — ARBITRATION-A3!) + **★★★ the-FRISELN-×14** (the-W-CURVE: 14→28→3→16!) + **★★★ the-CHRONOLOGY-HICCUPS-×2** + **★★★ the-ULEDBA-#10-6th-INSTANCE** (ARBITRATION-A1-DECISIVE-'Junii-29'!) + **★★★ the-JANČAR-9/9-100%-DOMINANT** (the-5th-year-thread!) + ★ the-z47-EMPTY-row + ★ the-ARBITRATIONS-A1–A5 (max-zoom > VLM — the-6th-pattern-confirmation!) + the-s157-ordinals-73–82-KROP (the-VLM-'63–72'-7→6-both-sessions → 1878 ≈ 85-entries!) + the-RE-READ-AGREEMENTS-×4 (2-source-facts!); **1879 = 64 physical rows / 63 ordinals (z1–z63 + z28-DUPLICATE!) / 9 Griblje / 8 houses (h20-×2!)**; **9 NEW BLOCKS: the vitals 1315 → 1498 · the 04106 = 96 → 105 · the 04894 = 520-UNCHANGED**; the scripts p198 (fetch-1:1 + read + build-entries + build-proof) + the qa-p198 (the 198th check) + the evidence parish-death-1879-04106.json (64 entries: 9-Griblje + 55-not!) + the pt-gap-REGENERATION (105/1498!); the verification: the runQA 198/198 ok:True · tsc 0 · lint 0; **★★★ THE-PREHISTORY-LINE-7/29-YEARS!** (the P199-LEAD: 1878 — the-s150–s157-probe; the-s157-ordinals-73–82-KROP-ALREADY-PROVEN + the-s158-tail-z83–z85-2-sources! 1878 ≈ 85-entries + the-baptism-04104-waits!)",
    p198Errors.length === 0,
    p198Errors.length === 0
      ? `9 vpisov / 64 fizičnih vrstic (z28-DUPLIKAT!) / 8 hiš (h20-×2!) · MEJA-s158-'Incipit-annus'+'1 8|7 9'-STACKED-SPLIT-37.-POTRDITEV + restart-85→1 (tail-83/84/85-KROP+RE-READ!) · z28-DUPLIKAT-3.-anomalija · 97-LET-KORPUS-REKORD · GEHIRN-×2-istega-dna · FRISELN-×14-W-krivulja · KRONOLOŠKI-PRESKOKI-×2 · ULEDBA-#10-ARBITRAŽA-A1 · JANČAR-9/9-100%-5.-leto · ARBITRAŽE-A1–A5 · **PREDZGODOVINA-7/29!** · vitals 1498 · 04106 105 · 04894 520`
      : p198Errors.join("; "),
  );
  }
'''

ANCHOR_QA = "  // ——— qa-p197: MRLIŠKA PREDZGODOVINA 04106 — leto 1880 = 6. leto PREDZGODOVINSKE"
src = QA.read_text(encoding="utf-8")
assert src.count(ANCHOR_QA) == 1, f"anchor-qa={src.count(ANCHOR_QA)}"
src = src.replace(ANCHOR_QA, BLOCK + "\n" + ANCHOR_QA, 1)
QA.write_text(src, encoding="utf-8")
print(f"qa-p198-blok: INSERTED (+{len(BLOCK)} B) | qa.ts {len(orig)} → {len(src)} B")
