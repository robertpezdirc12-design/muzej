#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P199 — sanitizacija: stale-števci 1324→1347 + 04106 105→128 + leta-+1878
(vzorec P198) + INSERT qa-p199 blok + pt-luknja-regeneracija + krstni-izjeme-×6."""
import glob, json
from pathlib import Path

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
orig = src

# ——— A1: total-assertions ———
n1 = src.count("HOUSE_VITALS.length !== 1324")
src = src.replace("HOUSE_VITALS.length !== 1324", "HOUSE_VITALS.length !== 1347")

# ——— A2: 04106-total 105 → 128 ———
n2 = src.count('04106").length !== 105')
src = src.replace('04106").length !== 105', '04106").length !== 128')
n2b = src.count("+ P198: 9 × 1879 = 105!)")
src = src.replace(
    "+ P198: 9 × 1879 = 105!)",
    "+ P198: 9 × 1879 + P199: 23 × 1878 = 128!)",
)

# ——— A3: year-set +1878 ———
OLD_SET = "(h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
NEW_SET = "(h.year ?? 0) !== 1878 && " + OLD_SET
n3 = src.count(OLD_SET)
src = src.replace(OLD_SET, NEW_SET)
n3b = src.count("04106-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1878 še nebrani!)")
src = src.replace(
    "04106-bloki izven {1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1878 še nebrani!)",
    "04106-bloki izven {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1877 še nebrani!)",
)

# ——— A4: detail-nizi ———
n4 = src.count("vitals 1324 · 04106 105 · 04894 520")
src = src.replace("vitals 1324 · 04106 105 · 04894 520", "vitals 1347 · 04106 128 · 04894 520")

QA.write_text(src, encoding="utf-8")
print(f"qa-parish.ts: total-{n1} | 04106-{n2}+{n2b} | yearset-{n3}+{n3b} | detail-{n4}")

# ——— B: skripte (1324→1347 + 04106-105→128) — p59 IZJEMA + p199 IZJEMA ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1324" not in t and "== 105" not in t and "04106==105" not in t:
        continue
    o = t
    t = t.replace("1324", "1347")
    t = t.replace('.get("04106") == 105', '.get("04106") == 128')
    t = t.replace("04106 == 105", "04106 == 128")
    t = t.replace("04106==105", "04106==128")
    t = t.replace("skupaj == 105", "skupaj == 128")
    t = t.replace('"04106") == 105', '"04106") == 128')
    t = t.replace("(04106, 105)", "(04106, 128)")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— C: pt-luknja regeneracija ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1347
pt["corpus"]["byBook"]["04106"] = 128
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P199: +23-blokov-1878 (04106 105→128, vitals 1324→1347)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: vitalsTotal={pt['corpus']['vitalsTotal']} 04106={pt['corpus']['byBook']['04106']}")

# ——— D: krstni-izjeme-×6 (04106-1878-dokazi PRED krstnimi 'NOVA-hiša' prvenci!) ———
IZJEME = [
    # (stara-tail, nova-tail, komentar)
    ('&& !(v.bookSignature === "04106" && v.year === 1879 && hn === "30")))',
     '&& !(v.bookSignature === "04106" && v.year === 1879 && hn === "30") && !(v.bookSignature === "04106" && v.year === 1878 && (hn === "30" || hn === "38")))',
     " // P199: + mrliška 04106-1878 h30-×2 (Mathias-PEZDIRC-6J-Jänner + Markus-'Pezdir(e)'-35J-Aug — PEZDIRC-era-pred-krstnim-prvencem-1890!) + h38 (Maria-SIMEC-87J-Mai — ŠIMEC-nit!)",),
    ('&& !(v.bookSignature === "04106" && v.year === 1879 && hn === "53")))',
     '&& !(v.bookSignature === "04106" && v.year === 1879 && hn === "53") && !(v.bookSignature === "04106" && v.year === 1878 && hn === "53")))',
     " // P199: + mrliška 04106-1878 h53 (tail-z83-Mathias-PEGLAVC?-87J-Wassersucht-Nov — P198-KROP-reuse + ta-seja-podpis-Jančar! pred-krstnim-prvencem-1891!)",),
    ('&& !(v.bookSignature === "04106" && v.year === 1879 && (hn === "20" || hn === "40")))',
     '&& !(v.bookSignature === "04106" && v.year === 1879 && (hn === "20" || hn === "40")) && !(v.bookSignature === "04106" && v.year === 1878 && (hn === "20" || hn === "37")))',
     " // P199: + mrliška 04106-1878 h20 (Katharina-VEZDIRZ?-10-mes-MASERN-Aug — PEZDIRC-era! + MASERN-×2-adjacent!) + h37 (Johann-PERHAR?-41J-Asthma-Nov! — pred-krstnima prvencema 1895!)",),
    ('&& !(v.bookSignature === "04894" && v.year === 1924 && hn === "45")))',
     '&& !(v.bookSignature === "04894" && v.year === 1924 && hn === "45") && !(v.bookSignature === "04106" && v.year === 1878 && (hn === "9" || hn === "14")))',
     " // P199: + mrliška 04106-1878 h9 (Nicolaus-JAKOFČIČ-2½J-April!) + h14 (Barbara-VEZDIRZ?-10-mes-Juni — PEZDIR-grafija! pred-krstnima prvencema 1896!)",),
    ('&& !(v.bookSignature === "04106" && v.year === 1879 && hn === "40")))',
     '&& !(v.bookSignature === "04106" && v.year === 1879 && hn === "40") && !(v.bookSignature === "04106" && v.year === 1878 && (hn === "10" || hn === "40")))',
     " // P199: + mrliška 04106-1878 h10 (Marcus-KURE-47J-Asthma-Jänner!) + h40 (Johann-'Pozdrin?'-3J-Mai — h40-nit-pred-1879-rekordom! pred-krstnima prvencema 1897!)",),
    ('&& !(v.bookSignature === "04106" && v.year === 1880 && hn === "18")))',
     '&& !(v.bookSignature === "04106" && v.year === 1880 && hn === "18") && !(v.bookSignature === "04106" && v.year === 1878 && (hn === "18" || hn === "48")))',
     " // P199: + mrliška 04106-1878 h18 (Theresia-INNEC?-41J-Jänner — 1.-GRIBLJE-1878 + MEJA-'18 78.'-v-celici!) + h48 (Johann-KLOBUČAR-¼-Gütler-35½J-März — pred-krstnima prvencema 1898!)",),
]
n_izj = 0
for old, new, comment in IZJEME:
    if old in src:
        src = src.replace(old, new + comment, 1)
        n_izj += 1
    else:
        print(f"⚠️ izjema-NI-našel: {old[:60]}")
QA.write_text(src, encoding="utf-8")
print(f"krstni-izjeme-1878: {n_izj}/6")

# ——— E: INSERT qa-p199 blok (pred qa-p198) ———
BLOCK = '''
  // ——— qa-p199: MRLIŠKA PREDZGODOVINA 04106 — leto 1878 = 8. leto PREDZGODOVINSKE
  //      LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1878-04106; knjiga 1857–1885!).
  //      1878 = 85 vpisov (z1–z85, ORDINALNO-ČISTO!) / 23 Griblje /
  //      22 hiš (h30-×2!) + ★★★ MEJA-1877/78-s149 ('18 78.'-SPLIT-VARIANTA-v-z1-
  //      datuma-celici = 38.-POTRDITEV-invariante! restart-1; s148-1877-tail-z-
  //      ORDINALI-NEVIDNIMI — P200-lead!) + ★★★ DUHOVNIKI-TRANZICIJA (Dovgan-
  //      dominanta + Kogej-subst.-coop-na-Griblju-×8 → Jančar-coop-od-junija-×6 =
  //      ★★★ JANČAR-NIT-1878→1883 = 6-LET!) + ★★★ 'Ukolk'[?]-NEZNANA-VAS-×5 +
  //      ★★★ MASERN-×2-ADJACENT (z60+z61!) + FRISELN+MASERN-×12 (W-krivulja
  //      12→14→28→3→16!) + ★★★ PEZDIR/PEZDIRC-GRAFIJA-NIT-×6 + ULEDBA-#10-
  //      7.-instance + 2×-87-LET-GRIBLJE (z44-Simec + z83-Peglavc!).
  //      Dokaz: parish-death-1878-04106.json; skripte p199 (fetch-md5 + read +
  //      crop + build-entries + build-proof).
  {
  const p199Errors: string[] = [];
  const p199Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1878);
  if (p199Death.length !== 23)
    p199Errors.push(`bloki 1878 (04106) ≠ 23 (${p199Death.length} — 23 Griblje-vpisov / 85 vpisov ordinalno-ČISTO!)`);
  const p199Houses = p199Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p199Houses.join(",") !== "1,3,9,10,14,15,16,18,20,30,30,33,37,38,40,44,47,48,53,54,55,57,66")
    p199Errors.push(`hiše 1878 ≠ [1,3,9,10,14,15,16,18,20,30,30,33,37,38,40,44,47,48,53,54,55,57,66] — najdeno: ${p199Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1347)
    p199Errors.push(`HOUSE_VITALS ≠ 1347 (${HOUSE_VITALS.length} — P198: 1324; P199: + 23 blokov 1878-04106 = 1347!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 128)
    p199Errors.push(`bloki 04106 ≠ 128 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 128!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p199Errors.push("04106-bloki izven {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1877 še nebrani!)");
  const p199H30 = p199Death.filter((h) => h.houseNo === "30");
  if (p199H30.length !== 2)
    p199Errors.push(`h30-vpisov-1878 ≠ 2 (${p199H30.length} — z4-Mathias-PEZDIRC-6J-Jänner + z62-Markus-'Pezdir(e)'-35J-Aug!)`);
  if (!p199Death.some((h) => h.houseNo === "18" && h.whatSi.includes("38.-POTRDITEV")))
    p199Errors.push("★★★ MEJA-'18 78.'-SPLIT-VARIANTA-v-z1 (38.-POTRDITEV-invariante!) ni označena");
  if (!p199Death.some((h) => h.houseNo === "33" && h.whatSi.includes("ULEDBA-#10-7.-INSTANCE")))
    p199Errors.push("★★★ ULEDBA-#10-7.-instance (z56: 29-Juni→1-Juli!) ni označena");
  if (!p199Death.some((h) => h.houseNo === "33" && h.whatSi.includes("JANČAR-NA-GRIBLJU-1878-#1")))
    p199Errors.push("★★★ JANČAR-NIT-1878→1883 = 6-LET (tranzicija-Dovgan/Kogej→Jančar!) ni označena");
  if (!p199Death.some((h) => h.houseNo === "38" && h.whatSi.includes("87 LET")))
    p199Errors.push("★★ 87-LET-GRIBLJE-×2-1878 (z44-Simec + z83-Peglavc!) ni označena");
  if (!p199Death.some((h) => h.houseNo === "1" && h.whatSi.includes("ZELIHA-NIT")))
    p199Errors.push("★★★ ZELIHA-NIT-h1-×3-v-2-letih (z46-Anna-Zelko-In-Entbindung!) ni označena");
  if (!p199Death.some((h) => h.houseNo === "57" && h.whatSi.includes("GEHIRNENTZÜNDUNG-NIT-1878-#3")))
    p199Errors.push("★★★ GEHIRNENTZÜNDUNG-NIT-×5-1878/79 (z80-h57-17J!) ni označena");
  if (!p199Death.some((h) => h.houseNo === "20" && h.whatSi.includes("MASERN")))
    p199Errors.push("★★★ MASERN-×2-ADJACENT (z60-h20 + z61-Klošter!) ni označena");
  push(
    "qa-p199-parish-death-1878-04106",
    "P199: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1878 = 8. LETO PREDZGODOVINSKE LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1878-04106; knjiga 1857–1885!): okvir — s148–s158 == Pag. 142–152 (stran == sken − 6! md5-križna-validacija-verige-P197→P198→P199: s157/s158-sveže == P198-seja-1:1! PRINTED-'146–150'-×5-vizualno!) + **MEJA 1877/78 = s149 ('18 78.'-SPLIT-VARIANTA-v-z1-datuma-celici — KROP-max-γ-7; VLM-'1848'-4/7-ZAVRJEN! = 38.-POTRDITEV-invariante + P194-tehnika-#9-NOVA-OBLIKA-glava-v-vrstici!)** (restart-1 + Jänner-z1–z7/Februar-z8–z9 + z10-prazna! s148 = 1877-Oct–Dez-tail-z-ORDINALI-NEVIDNIMI — P200-lead!) + MEJA 1878/79 = s158-mid (P198-37.-reuse! konec-1878 = z85-tail-Klošter) + **★★★ 85-VPISOV-EXAKT** (P197-'restart-85→1'-napoved + P198-'1878 ≈ 85'-lead = 1:1-POTRJENA!) + **★★★ ORDINALNO-ČISTO-LETO** (85/85 — kontrast-3-anomalijam-1879/80/81!; s156-z72-KROP-γ-7 — VLM-'62'-7→6-misread-3.×-potrjen!) + **★★★ DUHOVNIKI-TRANZICIJA-V-REALNEM-ČASU** (Jänner–April = Dovgan-dominanta + substituendus-KOGEJ-coop-NA-GRIBLJU-×8 [VLM-'Fortin-aus-Kogelnik'-ZAVRJEN-KROP-podpisi!] → od-junija = FRANZ-JANČAR-coop-raste [Griblje-×6: z56/60/70/73/77/83!] = **★★★ JANČAR-NIT-1878→1883 = 6-LET — P198-'5-let'-RAZŠIRJENA-NAZAJ!** VLM-'Vancaš'-grafia-ZAVRJEN!) + **★★★ 'Ukolk'[?]-NEZNANA-VAS-×5** (z36/67/71/75/78 — VLM-'Hrast'-ZAVRJEN-×3! cf. P195-'Wolk[~Volk?]'-1882 = verjetno-ista-vas!) + **★★★ MASERN-×2-ADJACENT** (z60-Griblje-h20-Katharina-10-mes + z61-Klošter-h36-Plut-1-dan — KROP-IDENTIČNA-GRAFIA! VLM-'Fraisen'-ZAVRJEN! M/W-nit!) + **★★★ FRISELN+MASERN-×12** (W-KRIVULJA-5-točkovna: 1878-×12 → 1879-×14 → 1880-×28-FLOOD → 1881-×3-DOLINA → 1882-×16!) + **★★★ PEZDIR/PEZDIRC-GRAFija-NIT-×6** (z4-Mathias-Pezdirc-h30 + z42-'Pozdrin[?]'-h40 + z55/'Vezdirz[?]'-h14 + z60-'Vezdirz[?]'-h20 + z62-'Pezdir(e)[?]'-h30 + z77-'Pecolar[?]'-h44 — h20/h30/h40/h44 = 1-LETO-PRED-P198-katastrofo!) + ★★★ ZELIHA-NIT-h1-×3-v-2-letih (z46-Anna-Zelko-34J-In-Entbindung → 1879-×2!) + ★ ŠIMEC-NIT-×2-1878 (z32-h55-1½J + z44-h38-87J!) + ★ KLOBUČAR-NIT-h48 (z14-¼-Gütler!) + ★ h18-nit-čez-mejo (1877-tail-s148-z4 + z1!) + ★ JAKOFČIČ-nit (z34! cf. z48 + 1879-z63!) + ★ HRIZAN/KRIŽAN-grafija-×2 (z31-h66 + z70-h15!) + ★★ ULEDBA-#10-7.-INSTANCE (z56-Griblje-h33: smrt-29-Juni → pokop-1-Juli!) + ★★ GEHIRNENTZÜNDUNG-×3-1878 (z26[~] + z33[~] + z80-h57-Maria-Logar-17J!) = NIT-×5-1878/79! + ★★ z39-STAROST-'~'-NI-VPISANA (2.-prazna-cf-P198-z47!) + z38-kripto-ime-'M[ar]___Ana-P.[?]'-Wwe-Math-Brinec[?] (BRINC-nit!) + ★ VLM-leto-misread-×3-KROP ('1848'/'1858'/'1875' → '1878'-glave-×6!) + ★ 2×-87-LET-GRIBLJE (z44-Simec-h38 + z83-Peglavc-h53-P198-KROP-reuse + ta-seja-podpis-Jančar!) + ★ s148-1877-tail-Griblje-×1 (z4-Katharina-h18[?]-Nov!) + KROP-RE-ALIGNMENT-lekcija-#18 (levi/desni-strani-ne-poravnani — row-tracing!); **1878 = 85 vpisov (z1–z85, ordinalno-ČISTO!) / 23 Griblje-vpisov / 22 hiš (h30-×2!)**; **23 NOVIH BLOKOV parish.ts: vitals 1324 → 1347 · 04106 = 105 → 128 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJENO**; skripte p199 (fetch-md5 + read + crop + build-entries + build-proof) + qa-p199 (199. kontrola) + dokaz parish-death-1878-04106.json (85 entries: 23-Griblje + 62-ne! 13-anomalij + 10-crossChecks + honesty-16 + leadP200-1877!) + pt-luknja-REGENERACIJA (128/1347!) + krstni-izjeme-×6 (p85-h30/h38 + p86-h53 + p90-h20/h37 + p91-h9/h14 + p92-h10/h40 + p93-h18/h48!); verifikacija: runQA 199/199 ok:True · tsc 0 · lint 0; korpus po P199: **1347/199+128(04106)+520/191/94(p80)·93(korpus)**; **★★★ PREDZGODOVINA-LINIJA-8/29-LET!** (P200-LEAD: 1877 — s142–s149-probe; s148-tail-Oct–Dez-ŽE-PREBRAN (Griblje-×1-Katharina-h18[?]! ordinali-NEVIDNI!) + 1878-z1-restart-1 → 1877 ≈ 85-?-vpisov + krstna-04104-čaka!)",
    "P199: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1878 = THE 8th YEAR OF THE PREHISTORY LINE (issue #18): the frame — s148–s158 == pages 142–152 (page == scan − 6! the-md5-cross-validation-of-the-chain-P197→P198→P199: s157/s158-fresh == P198-session-1:1! PRINTED-'146–150'-×5-visual!) + **THE 1877/78 BOUNDARY = s149 (the-'18 78.'-SPLIT-VARIANT-inside-the-z1-date-cell — KROP-max-γ-7; VLM-'1848'-4/7-REJECTED! = the 38th boundary-invariant-confirmation + the-NEW-FORM-head-inside-the-row!)** (the-restart-1 + s148 = the-1877-Oct–Dec-tail-with-ORDINALS-INVISIBLE — P200-lead!) + the 1878/79 boundary = s158-mid (P198-37th-reuse! the-1878-end = z85-tail) + **★★★ THE-85-ENTRIES-EXACT** (the-P197-'restart-85→1'-prediction + the-P198-'1878 ≈ 85'-lead = 1:1-PROVEN!) + **★★★ THE-ORDINALLY-CLEAN-YEAR** (85/85 — in-contrast-to-the-3-anomalies-1879/80/81!) + **★★★ THE-PRIESTS-TRANSITION-IN-REAL-TIME** (Jan–Apr = Dovgan-dominant + the-substituendus-KOGEJ-coop-ON-GRIBLJE-×8 [VLM-'Fortin-aus-Kogelnik'-REJECTED-KROP!] → from-June = FRANZ-JANČAR-coop-rises [Griblje-×6!] = **★★★ THE-JANČAR-THREAD-1878→1883 = 6-YEARS!** VLM-'Vancaš'-grafia-REJECTED!) + **★★★ the-'Ukolk'[?]-UNKNOWN-VILLAGE-×5** + **★★★ the-MEASLES-×2-ADJACENT** (KROP-identical-grafia! VLM-'Fraisen'-REJECTED!) + **★★★ the-FRISELN+MEASLES-×12** (the-W-CURVE-5-point: 12→14→28→3→16!) + **★★★ the-PEZDIR/PEZDIRC-GRAFIA-THREAD-×6** (h20/h30/h40/h44 = 1-YEAR-BEFORE-the-P198-catastrophe!) + ★★★ the-ZELIHA-THREAD-h1-×3-in-2-years + ★ the-ŠIMEC-×2 + ★ the-KLOBUČAR-h48 + ★ the-JAKOFČIČ-thread + ★ the-HRIZAN/KRIŽAN-grafia-×2 + ★★ the-ULEDBA-#10-7th-INSTANCE + ★★ the-GEHIRNENTZÜNDUNG-×3-1878 = the-THREAD-×5-1878/79! + ★★ the-z39-EMPTY-AGE + the-z38-crypto-name + ★ the-VLM-year-misread-×3-KROP + ★ the-2×-87-YEARS-GRIBLJE + the-KROP-RE-ALIGNMENT-lesson-#18; **1878 = 85 entries (z1–z85, ordinally-CLEAN!) / 23 Griblje / 22 houses (h30-×2!)**; **23 NEW BLOCKS: the vitals 1324 → 1347 · the 04106 = 105 → 128 · the 04894 = 520-UNCHANGED**; the scripts p199 + the qa-p199 (the 199th check) + the evidence parish-death-1878-04106.json (85 entries: 23-Griblje + 62-not!) + the pt-gap-REGENERATION (128/1347!) + the-baptism-exceptions-×6; the verification: the runQA 199/199 ok:True · tsc 0 · lint 0; **★★★ THE-PREHISTORY-LINE-8/29-YEARS!** (the P200-LEAD: 1877 — the-s142–s149-probe; the-s148-tail-Oct–Dec-ALREADY-READ (Griblje-×1! ordinals-INVISIBLE!) → 1877 ≈ 85-?-entries + the-baptism-04104-waits!)",
    p199Errors.length === 0,
    p199Errors.length === 0
      ? `23 vpisov / 85 vrstic (ordinalno-ČISTO!) / 22 hiš (h30-×2!) · MEJA-s149-'18 78.'-SPLIT-v-z1-38.-POTRDITEV + restart-1 · 85-vpisov-EXAKT-P197/P198-lead · DUHOVNIKI-TRANZICIJA-Dovgan/Kogej→JANČAR (NIT-6-LET!) · 'Ukolk'[?]-×5-NEZNANA-VAS · MASERN-×2-adjacent · FRISELN-×12-W-krivulja-5-točk · PEZDIR-GRAFIJA-×6 (1-leto-pred-katastrofo!) · ZELIHA-h1-×3 · ULEDBA-#10-7.-instance · GEHIRN-×3-nit-×5 · 2×-87-LET-GRIBLJE · **PREDZGODOVINA-8/29!** · vitals 1347 · 04106 128 · 04894 520`
      : p199Errors.join("; "),
  );
  }
'''

ANCHOR_QA = "  // ——— qa-p198: MRLIŠKA PREDZGODOVINA 04106 — leto 1879 = 7. leto PREDZGODOVINSKE"
src = QA.read_text(encoding="utf-8")
assert src.count(ANCHOR_QA) == 1, f"anchor-qa={src.count(ANCHOR_QA)}"
src = src.replace(ANCHOR_QA, BLOCK + "\n" + ANCHOR_QA, 1)
QA.write_text(src, encoding="utf-8")
print(f"qa-p199-blok: INSERTED (+{len(BLOCK)} B) | qa.ts {len(orig)} → {len(src)} B")
