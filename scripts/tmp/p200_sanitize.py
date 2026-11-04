#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P200 — sanitizacija: stale-števci 1347→1355 + 04106 128→136 + leta-+1877
(vzorec P199) + krstni-izjeme-×3 (h53/h12-DRAGOŠ!/h18) + INSERT qa-p200 blok +
pt-luknja-regeneracija."""
import glob, json
from pathlib import Path

ROOT = Path("/home/z/muzej")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
orig = src

# ——— A1: total-assertions ———
n1 = src.count("HOUSE_VITALS.length !== 1347")
src = src.replace("HOUSE_VITALS.length !== 1347", "HOUSE_VITALS.length !== 1355")

# ——— A2: 04106-total 128 → 136 ———
n2 = src.count('04106").length !== 128')
src = src.replace('04106").length !== 128', '04106").length !== 136')
n2b = src.count("+ P199: 23 × 1878 = 128!)")
src = src.replace(
    "+ P199: 23 × 1878 = 128!)",
    "+ P199: 23 × 1878 + P200: 8 × 1877 = 136!)",
)

# ——— A3: year-set +1877 ———
OLD_SET = "(h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
NEW_SET = "(h.year ?? 0) !== 1877 && " + OLD_SET
n3 = src.count(OLD_SET)
src = src.replace(OLD_SET, NEW_SET)
OLD_ERR = "04106-bloki izven {1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1877 še nebrani!)"
NEW_ERR = "04106-bloki izven {1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1876 še nebrani!)"
n3b = src.count(OLD_ERR)
src = src.replace(OLD_ERR, NEW_ERR)

# ——— A4: detail-nizi ———
n4 = src.count("vitals 1347 · 04106 128 · 04894 520")
src = src.replace("vitals 1347 · 04106 128 · 04894 520", "vitals 1355 · 04106 136 · 04894 520")

QA.write_text(src, encoding="utf-8")
print(f"qa-parish.ts: total-{n1} | 04106-{n2}+{n2b} | yearset-{n3}+{n3b} | detail-{n4}")

# ——— B: skripte (1347→1355 + 04106-128→136) — p59/p199/p200-IZJEME ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True)
                   + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1347" not in t and "== 128" not in t and "04106==128" not in t:
        continue
    o = t
    t = t.replace("1347", "1355")
    t = t.replace('.get("04106") == 128', '.get("04106") == 136')
    t = t.replace("04106 == 128", "04106 == 136")
    t = t.replace("04106==128", "04106==136")
    t = t.replace("skupaj == 128", "skupaj == 136")
    t = t.replace('"04106") == 128', '"04106") == 136')
    t = t.replace("(04106, 128)", "(04106, 136)")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— C: pt-luknja regeneracija ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1355
pt["corpus"]["byBook"]["04106"] = 136
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P200: +8-blokov-1877 (04106 128→136, vitals 1347→1355)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: vitalsTotal={pt['corpus']['vitalsTotal']} 04106={pt['corpus']['byBook']['04106']}")

# ——— D: krstni-izjeme-×3 (04106-1877-dokazi PRED krstnimi 'NOVA-hiša' prvenci!) ———
IZJEME = [
    ('&& !(v.bookSignature === "04106" && v.year === 1878 && hn === "53")))',
     '&& !(v.bookSignature === "04106" && v.year === 1878 && hn === "53") && !(v.bookSignature === "04106" && v.year === 1877 && hn === "53")))',
     " // P200: + mrliška 04106-1877 h53 (z51-Maria-PEZDINC-1J-Wasserfriesl-Okt — ★★★ PEZDINC-GRAFIA-#7! 14-let-pred-krstnim-prvencem-1891!)",),
    ('&& !(v.bookSignature === "04106" && v.year === 1882 && hn === "73")))',
     '&& !(v.bookSignature === "04106" && v.year === 1882 && hn === "73") && !(v.bookSignature === "04106" && v.year === 1877 && hn === "12")))',
     " // P200: + mrliška 04106-1877 h12 (z56-Katharina-DRAGOŠ-21J-Nov — ★★★ DRAGOŠ-NA-h12-15-LET-PRED-KRSTNIM-PRVENCEM-1892! P199-'h18[?]'-POPREVEK!)",),
    ('&& !(v.bookSignature === "04106" && v.year === 1878 && (hn === "18" || hn === "48"))))',
     '&& !(v.bookSignature === "04106" && v.year === 1878 && (hn === "18" || hn === "48")) && !(v.bookSignature === "04106" && v.year === 1877 && hn === "18")))',
     " // P200: + mrliška 04106-1877 h18 (z26-Barbara-SINIEC[ŠIMEC!]-8½J-Mai — ★h18-ŠIMEC-NIT-1877! INNEC/SIMEC/TIMEC-3-LETNA! 19-let-pred-prvencem-1896!)",),
]
n_izj = 0
for old, new, comment in IZJEME:
    if old in src:
        src = src.replace(old, new + comment, 1)
        n_izj += 1
    else:
        print(f"⚠️ izjema-NI-našel: {old[:60]}")
QA.write_text(src, encoding="utf-8")
print(f"krstni-izjeme-1877: {n_izj}/3")

# ——— E: INSERT qa-p200 blok (pred qa-p199) ———
BLOCK = '''
  // ——— qa-p200: MRLIŠKA PREDZGODOVINA 04106 — leto 1877 = 9. leto PREDZGODOVINSKE
  //      LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1877-04106; knjiga 1857–1885!).
  //      1877 = 60 vpisov (z1–z60, ŠTEVJE-IZ-VRSTIC — ordinali-NEVIDNI-×6!) /
  //      8 Griblje / 8 hiš + ★★★ MEJA-1876/77-s143 ('18 77.'-glava-ODREZANA-
  //      off-scan! restart-evidenca: Dez-1876-nad + Jänner-pod!) + ★★★ 39.-POTRDI-
  //      TEV-invariante (s145-'1877.'-glava-V-Z22-DATUMSKI-CELICI! VLM-'tail'-
  //      NAPAČNI-ALARM!) + ★★★ 'HRIBLE'[?='Hrib'?]-NOVA-LOKALNOST-×3 (Tomc-
  //      klaster — G-glyph-duel-3.×-POZITIVEN! 1.-pojav-v-korpusu!) + ★★★
  //      KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ (1877-Jänner→Mai!) + ★★★ PEZDINC-
  //      GRAFIA-#7 (z51-h53!) + ★★★ 'Br[a]stfbrand'[?]-KLASTER-×3 + ★★★
  //      ULEDBA-#10-8.-instance (z24: 29-April→1-Mai!) + ★★★ h12-DEFINITIVNO
  //      (P199-'h18[?]'-POPREVEK — z56-DRAGOŠ!).
  //      Dokaz: parish-death-1877-04106.json; skripte p200 (fetch-md5 + read +
  //      crop + build-entries + build-proof).
  {
  const p200Errors: string[] = [];
  const p200Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1877);
  if (p200Death.length !== 8)
    p200Errors.push(`bloki 1877 (04106) ≠ 8 (${p200Death.length} — 8 Griblje-vpisov / 60 vpisov vrstno-štetje!)`);
  const p200Houses = p200Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p200Houses.join(",") !== "6,8,12,18,42,53,57,62")
    p200Errors.push(`hiše 1877 ≠ [6,8,12,18,42,53,57,62] — najdeno: ${p200Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1355)
    p200Errors.push(`HOUSE_VITALS ≠ 1355 (${HOUSE_VITALS.length} — P199: 1347; P200: + 8 blokov 1877-04106 = 1355!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 136)
    p200Errors.push(`bloki 04106 ≠ 136 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 136!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p200Errors.push("04106-bloki izven {1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1876 še nebrani!)");
  if (!p200Death.some((h) => h.houseNo === "42" && h.whatSi.includes("ULEDBA-#10-8.-INSTANCE")))
    p200Errors.push("★★★ ULEDBA-#10-8.-instance (z24: 29-April→1-Mai!) ni označena");
  if (!p200Death.some((h) => h.houseNo === "12" && h.whatSi.includes("P199-'h18[?]'-POPREVEK")))
    p200Errors.push("★★★ h12-DEFINITIVNO (P199-'h18[?]'-POPREVEK — z56-DRAGOŠ!) ni označena");
  if (!p200Death.some((h) => h.houseNo === "53" && h.whatSi.includes("PEZDINC-GRAFIA-NIT-#7")))
    p200Errors.push("★★★ PEZDINC-GRAFIA-NIT-#7 (z51-Maria-Pezdinc-h53!) ni označena");
  if (!p200Death.some((h) => h.houseNo === "18" && h.whatSi.includes("ŠIMEC-GRAFIA")))
    p200Errors.push("★★★ h18-ŠIMEC-NIT-1877 (z26-Siniec — INNEC/SIMEC/TIMEC-3-LETNA!) ni označena");
  if (!p200Death.some((h) => h.houseNo === "62" && h.whatSi.includes("Br[a]stfbrand'-KLASTER-1/3")))
    p200Errors.push("★★★ 'Br[a]stfbrand'[?]-KLASTER-×3-OKTOBER (z48/z49/z52!) ni označena");
  if (!p200Death.some((h) => h.houseNo === "57" && h.whatSi.includes("h57-NIT-1877")))
    p200Errors.push("★★★ h57-NIT-1877 (z49-Lozar → 1878-z80-Logar-GEHIRN!) ni označena");
  push(
    "qa-p200-parish-death-1877-04106",
    "P200: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1877 = 9. LETO PREDZGODOVINSKE LINIJE (issue #18; SAMPLE-TRANSCRIPTION-D1877-04106; knjiga 1857–1885!): okvir — s142–s148 == Pag. 136–142 (stran == sken − 6! md5-križna-validacija-verige-P197→P198→P199→P200: s148/s149-sveže == P199-disk-1:1 — 4.×!) + **MEJA 1876/77 = s143-top ('18 77.'-glava-ODREZANA-off-scan — scan-edge! restart-evidenca: s142-Dez-1876-nad + s143-Jänner-pod + z1-pokop-'1.' + nemška-opomba-'...in Podzemelj zu begraben'!)** + **★★★ 39.-POTRDITEV-invariante = s145-'1877.'-glava-ZAPISANA-V-Z22-DATUMSKI-CELICI** (mid-year-glava-vrsta — 'prečrtan'-izgled = prepis-nad-mesecem; VLM-'tail'-zastavica-NAPAČNI-ALARM!) + MEJA 1877/78 = s149 (P199-38.-reuse! konec-1877 = z60 = s148-v8-Dez 21.) + **★★★ 60-VPIISOV — ŠTEVJE-IZ-VRSTIC** (ordinali-NEVIDNI-na-vseh-6-straneh — forma-BREZ-stolpca/scan-edge! vrstna-aritmetika 11+10+12+10+9+8 + datum-veriga-continuous Jän1→Mär1→März5→März28→Juni26→Sept28→Okt18→Dez21!; **P199-'1877 ≈ 85-?'-ocena-FALSIFICIRANA!**) + **★★★ 'HRIBLE'[?='Hrib'?]-NOVA-LOKALNOST-×3** (z3/z6/z7-Tomc-klaster-h2/h2/h1 — 1.-pojav-v-korpusu! G-glyph-duel-3.×-POZITIVEN: ≠Gradac-G + ≠s145-Griblje-G + ≠z4-'Gribl[j]ar'-G-vsi-descender-G — z3-inicial-BREZ-descenderja! cf. 'Ukolk'[?]-1878 = 2.-neznana-vas-v-2-letih!) + **★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ** (substituendus-Hoggai[s]-Coop-1877-Jänner→Mai: z2/z8/z9/z11-s143 + Griblje-z24/z26! — P199-'1878-Jänner–April'-RAZŠIRJENA!) + Franz-DOVGAN-dominanta-1877 (Griblje-×6: z39/z48/z49/z51/z52/z56 + Tomc-×3!) + NO-Jančar-1877 (**★★★ JANČAR-NIT-1878→1883-SPREMENJENA-NE-RAZŠIRJENA!**) + **★★★ PEZDINC-GRAFIA-#7** (z51-Maria-Pezdinc-h53 → 1878-×6 → 1879-katastrofa-h40/h44!) + **★★★ 'Br[a]stfbrand'[?]-KLASTER-×3-OKTOBER** (z48-h62 + z49-h57 + z52-h6-zaporedoma! VLM-'Brennfieber'-nesoglasja) + **★★★ GRIBLJE-OTROŠKA-UMRLJIVOST-50%-1877** (4/8: z39-9½mes + z48-3¼J + z51-1J + z52-3¾J!) + **★★★ ULEDBA-#10-8.-INSTANCE** (z24: smrt-29-April → pokop-1-Mai!) + **★★★ h12-DEFINITIVNO** (z56-Katharina-DRAGOŠ-h12 — KROP-'12'-10×-jasno — **P199-'h18[?]'-POPREVEK!** — DRAGOŠ-NA-h12-15-LET-PRED-KRSTNIM-PRVENCEM-1892!) + ★ h18-ŠIMEC-NIT-1877 (z26-Siniec → 1878-Innec? + 1881-TIMEC = INNEC/SIMEC/TIMEC-3-LETNA-NA-h18!) + ★ h53-NIT (z51-Pezdinc → 1878-z83-Peglavc-87J!) + ★ h57-NIT (z49-Lozar → 1878-z80-Logar-GEHIRN!) + ★ h44-TAIL-1876 (s142-z4-Barbara-Kavčič-24-URE-Dez! → 1878-z77 + 1879-katastrofa!) + ★ h16-TAIL-1876 (Spilak?[?] → 1878-z41!) + ★ h75-TAIL-1876 (Stubler!) + ★ MASERN-z6-'Hrib'-h2 + FRAISEN-z3-'Hrib' (FRISEN-nit-do-1877!) + Wasserfriesl-z51 + tail-1876-Griblje-×3-P201-lead! + ★ VLM-KROP-korekcije-×7 (frakcije-3½→3¼-×2! + h18→h12! + 'Kreuzsteing'→'Abzehrung' + VLM-v5/v6-DRIFT + 'Jakopič'→'Jakofčič' + h6[~46?]→h6!); **1877 = 60 vpisov (z1–z60) / 8 Griblje-vpisov / 8 hiš** + 3-'Hrible'[?]-Tomc-NE-Griblje (dokumentirane!); **8 NOVIH BLOKOV parish.ts: vitals 1347 → 1355 · 04106 = 128 → 136 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJENO**; skripte p200 (fetch-md5 + read + crop + build-entries + build-proof) + qa-p200 (200. kontrola!) + dokaz parish-death-1877-04106.json (60 entries: 8-Griblje + 3-'Hrib'[?] + 49-druge! 13-anomalij + 10-crossChecks + honesty-16 + tail_1876-×3-GRIBLJE + leadP201-1876!) + pt-luknja-REGENERACIJA (136/1355!) + krstni-izjeme-×3 (h53-PEZDINC + h12-DRAGOŠ + h18-ŠIMEC!); verifikacija: runQA 200/200 ok:True · tsc 0 · lint 0; korpus po P200: **1355/200+136(04106)+520/191/94(p80)·93(korpus)**; **★★★ PREDZGODOVINA-LINIJA-9/29-LET!** (P201-LEAD: 1876 — s134–s142-probe; s142-Dez-tail-ŽE-PREBRAN-ta-seja (Griblje-×3: z4-h44-24-URE-Vesperstbrand[?]-KAVČIČ + z6-h75-Stubler + z7-h16-Spilak[?]!) + '1876.'-glava-v-z1-s142! + 1876 ≈ 60-85-?-vpisov + krstna-04104-čaka!)",
    "P200: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1877 = THE 9th YEAR OF THE PREHISTORY LINE (issue #18): the frame — s142–s148 == pages 136–142 (page == scan − 6! the-md5-cross-validation-of-the-chain-P197→P198→P199→P200: s148/s149-fresh == P199-disk-1:1 — the-4th-time!) + **THE 1876/77 BOUNDARY = s143-top (the-'18 77.'-head-CUT-OFF-SCAN — the-scan-edge! the-restart-evidence: s142-Dec-1876-above + s143-January-below + z1-burial-'1.' + the-German-note-'...in Podzemelj zu begraben'!)** + **★★★ THE-39th-INVARIANT-CONFIRMATION = the-s145-'1877.'-head-WRITTEN-INSIDE-THE-Z22-DATE-CELL** (the-mid-year-head-row — the-'struck-through'-look = the-overwrite-over-the-month; the-VLM-'tail'-flag-FALSE-ALARM!) + the 1877/78 boundary = s149 (the-P199-38th-reuse! the-1877-end = z60 = s148-v8-Dec 21.) + **★★★ THE-60-ENTRIES — THE-COUNT-FROM-ROWS** (the-ordinals-INVISIBLE-on-all-6-pages — the-form-WITHOUT-the-column/scan-edge! the-row-arithmetic 11+10+12+10+9+8 + the-continuous-date-chain!; **the-P199-'1877 ≈ 85-?'-estimate-FALSIFIED!**) + **★★★ the-'HRIBLE'[?='Hrib'?]-NEW-LOCALITY-×3** (the-Tomc-cluster-h2/h2/h1 — the-1st-appearance-in-the-corpus! the-G-glyph-duel-3×-POSITIVE!) + **★★★ the-KOGEJ-PERIOD-EXTENDED-BACK** (1877-January→Mai! — the-P199-'1878-Jan–Apr'-EXTENDED!) + the-Franz-DOVGAN-dominance (Griblje-×6!) + NO-Jančar-1877 (**★★★ the-JANČAR-THREAD-1878→1883-CHANGED-NOT-EXTENDED!**) + **★★★ the-PEZDINC-GRAFIA-#7** + **★★★ the-'Br[a]stfbrand'[?]-CLUSTER-×3-OKTOBER** + **★★★ the-GRIBLJE-CHILD-MORTALITY-50%-1877** + **★★★ the-ULEDBA-#10-8th-INSTANCE** (z24: death-Apr-29 → burial-Mai-1!) + **★★★ the-h12-DEFINITIVE** (the-P199-'h18[?]'-CORRECTION — the-DRAGOŠ-on-h12-15-YEARS-BEFORE-the-1892-baptism-first!) + ★ the-h18-ŠIMEC-THREAD-1877 (the-INNEC/SIMEC/TIMEC-3-YEAR-on-h18!) + ★ the-h53/h57-NITs + ★ the-h44-TAIL-1876 (24-HOURS!) + the-tail-1876-GRIBLJE-×3-P201-lead! + ★ the-VLM-KROP-corrections-×7; **1877 = 60 entries / 8 Griblje / 8 houses** + 3-'Hrible'[?]-Tomc-NOT-Griblje; **8 NEW BLOCKS: the vitals 1347 → 1355 · the 04106 = 128 → 136 · the 04894 = 520-UNCHANGED**; the scripts p200 + the qa-p200 (the 200th check!) + the evidence parish-death-1877-04106.json (60 entries!) + the pt-gap-REGENERATION (136/1355!) + the-baptism-exceptions-×3; the verification: the runQA 200/200 ok:True · tsc 0 · lint 0; **★★★ THE-PREHISTORY-LINE-9/29-YEARS!** (the P201-LEAD: 1876 — the-s134–s142-probe; the-s142-Dec-tail-ALREADY-READ-this-session (Griblje-×3: h44-24-HOURS-Vesperstbrand[?]-Kavčič + h75-Stubler + h16-Spilak[?]!) + the-'1876.'-head-in-z1-s142! + 1876 ≈ 60-85-?-entries + the-baptism-04104-waits!)",
    p200Errors.length === 0,
    p200Errors.length === 0
      ? `8 vpisov / 60 vrstic (števje-iz-vrstic!) / 8 hiš · MEJA-s143-'18 77.'-ODREZANA-off-scan + 39.-POTRDITEV-s145-glava-v-z22-celici · 60-vpisov (≈85-FALSIFICIRANA) · 'HRIBLE'[?]-×3-NOVA-LOKALNOST-G-glyph-duel · KOGEJ-razširjen-nazaj-1877 · PEZDINC-#7 · 'Br[a]stfbrand'-×3 · ULEDBA-#10-8.-instance · h12-POPREVEK-DRAGOŠ · h18-ŠIMEC-nit · otroška-umrljivost-50% · **PREDZGODOVINA-9/29!** · vitals 1355 · 04106 136 · 04894 520`
      : p200Errors.join("; "),
  );
  }
'''

ANCHOR_QA = "  // ——— qa-p199: MRLIŠKA PREDZGODOVINA 04106 — leto 1878 = 8. leto PREDZGODOVINSKE"
src = QA.read_text(encoding="utf-8")
assert src.count(ANCHOR_QA) == 1, f"anchor-qa={src.count(ANCHOR_QA)}"
src = src.replace(ANCHOR_QA, BLOCK + "\n" + ANCHOR_QA, 1)
QA.write_text(src, encoding="utf-8")
print(f"qa-p200-blok: INSERTED (+{len(BLOCK)} B) | qa.ts {len(orig)} → {len(src)} B")
