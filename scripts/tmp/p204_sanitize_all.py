#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P204 — INSERT qa-p204 blok + sanitizacija (1406→1444, 187→225, yearset +1873) +
verifier-patch (p19x–p203) + pt-luknja + skripte-kaskada."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/muzej")

# ——— A: qa-p204 INSERT ———
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p203: MRLIŠKA PREDZGODOVINA 04106 — leto 1874 = 12. leto PREDZGODOVINSKE"
assert src.count(ANCHOR) == 1 and "qa-p204-parish-death-1873-04106" not in src
BLOCK = '''
  // ——— qa-p204: MRLIŠKA PREDZGODOVINA 04106 — leto 1873 = 13. leto PREDZGODOVINSKE
  //      LINIJE — ★★★ KOLERA-LETO (cholera epidermica!) (issue #18). 1873 =
  //      212 vpisov (z1–z212, ŠTEVJE-IZ-VRSTIC-6.× — NAJVEČJE-leto-korpusa!)
  //      / 38 Griblje / 30 hiš (REKORD!) + ★★★ MEJA-1872/73-s102 ('1873.'-glava-
  //      v-z1-celici = 41.-POTRDITEV + 'Incipit annus Domini'!) + ★★★ MEJA-1873/74-
  //      s119 (TAIL-9-DEZ-1873-ordinala-204–212 + 'December 1873'-glava-v-z204-
  //      celici = 43.-POTRDITEV!) + ★★★ DOUBLE-SCAN-3.× (s103==s104 = pag-98-×2!)
  //      + ★★★ pisarski-ORDINAL-DUPKATI-×4 (24/37/61/153!) + LUKNJE-×5 (67 +
  //      141–144!) + GLAVE-V-CELICAH-×6-REKORD + KROP-KOREKCIJE-×7 (z71-NI-GRIBLJE!
  //      + z76-spol + z112-5¾J + z115-Brime + z30-ime!).
  //      Dokaz: parish-death-1873-04106.json; skripte p204.
  {
  const p204Errors: string[] = [];
  const p204Death = HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && h.year === 1873);
  if (p204Death.length !== 38)
    p204Errors.push(`bloki 1873 (04106) ≠ 38 (${p204Death.length} — 38 Griblje-vpisov / 212 vpisov vrstno-štetje!)`);
  const p204Houses = p204Death.map((h) => h.houseNo).sort((a, b) => Number(a) - Number(b));
  if (p204Houses.join(",") !== "2,5,7,8,10,10,11,13,13,16,22,24,24,27,28,28,30,30,33,33,34,35,37,40,41,43,43,44,49,51,55,57,58,60,63,65,65,94")
    p204Errors.push(`hiše 1873 neujemane — najdeno: ${p204Houses.join(",")}`);
  if (HOUSE_VITALS.length !== 1444)
    p204Errors.push(`HOUSE_VITALS ≠ 1444 (${HOUSE_VITALS.length} — P203: 1406; P204: + 38 blokov 1873-04106 = 1444!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length !== 225)
    p204Errors.push(`bloki 04106 ≠ 225 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04106").length} — P204: 38 × 1873 + P203: 21 × 1874 + P202: 10 × 1875 + P201: 20 × 1876 + P200: 8 × 1877 + P199: 23 × 1878 + P198: 9 × 1879 + P197: 13 × 1880 + P192: 16 × 1885 + P193: 21 × 1884 + P194: 11 × 1883 + P195: 16 × 1882 + P196: 19 × 1881 = 225!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04106" && (h.year ?? 0) !== 1873 && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p204Errors.push("04106-bloki izven {1873, ..., 1885} (predzgodovina: 1857–1872 še nebrani!)");
  if (!p204Death.some((h) => h.houseNo === "2" && h.whatSi.includes("41.-POTRDITEV")))
    p204Errors.push("★★★ '1873.'-GLAVA-V-Z1-CELICI (41.-POTRDITEV-invariante + 'Incipit annus Domini'!) ni označena");
  if (!p204Death.some((h) => h.houseNo === "16" && h.whatSi.includes("43.-POTRDITEV")))
    p204Errors.push("★★★ 'December 1873'-GLAVA-V-Z204-CELICI (43.-POTRDITEV + ULEDBA!) ni označena");
  if (!p204Death.some((h) => h.houseNo === "58" && h.whatSi.includes("Griblje-DVOJNOST")))
    p204Errors.push("★★★ h58-Griblje-DVOJNOST ('Krasinec-mimo-Griblje'-Marcus-Dozeth-MOŠKI!) ni označena");
  if (!p204Death.some((h) => h.houseNo === "11" && h.whatSi.includes("LUNIČ-h11-NIT-3.-LETO")))
    p204Errors.push("★★★ LUNIČ-h11-NIT-3.-LETO (z177-63J → 1874-16dni → 1875-65J!) ni označena");
  if (!p204Death.some((h) => h.houseNo === "65" && h.whatSi.includes("h65-×2-KLASTER")))
    p204Errors.push("★★★ h65-×2-KLASTER (z8-dvojni-ime + z9-Küllik-32½J-Kindbett!) ni označena");
  if (!p204Death.some((h) => h.houseNo === "24" && h.whatSi.includes("BRIME-NIT")))
    p204Errors.push("★★★ BRIME-h24-NIT (z115-5J[~51?] → P203-z6-9J-1874!) ni označena");
  push(
    "qa-p204-parish-death-1873-04106",
    "P204: ŽUPNIJA PODZEMELJ — MRLIŠKA PREDZGODOVINA 04106, LETO 1873 = 13. LETO PREDZGODOVINSKE LINIJE — ★★★ KOLERA-LETO (cholera epidermica!) (issue #18): okvir — s102–s118 + s119-tail-9 == Pag. 97–114 (pag = sken−5, LEKCIJA-#21; md5-križna-veriga-P197→…→P204-8.×: s118+s119-sveža == P203-disk-1:1 + s110/s111-2. krog!) + **★★★ MEJA-1872/73 = s102 ('1873.'-GLAVA-V-Z1-DATUMSKI-CELICI = 41.-POTRDITEV-invariante + 'Incipit annus Domini'-ročno-glava + restart-1–12; s101-'finis'-zaključek-1872!)** + **★★★ MEJA-1873/74 = s119 (TAIL-9-DEZ-1873-ordinala-204–212-KROP! 4-Griblje! + 'December 1873'-GLAVA-V-Z204-CELICI = 43.-POTRDITEV + '1874. Jänner Incipit annus Domini'-meja-glava + restart-1–4!)** + **★★★ DOUBLE-SCAN-3.×: s103==s104 = pag-98-×2 (md5-RAZLIČNA-vsebina-1:1-KROP-ordinali-13–18-×2-jasno! — lekcija-#21-2.×-P203-s123==s124!)** + **★★★ PISARSKI-ORDINAL-DUPKATI-×4-ob-mejah-strani (24: s104-z24≠s105-r1 + 37: s105-end≠s106-r1-'1873. Jüni'-glava! + 61: s107-end≠s108-r1-'August'-glava! + 153: s114-end≠s115-r1-'October'-glava!) + LUKNJE-×5 (67-s108-'68'-vijolično + 141–144-s114-skok-137–140→145–153!) → neto-−1 (211/212-Kurent-koncu!)** + **★★★ VLM-ORDINAL-OFF-BY-N-×3-KROP-MARGINALA-FORENZIKA-REŠENE (s113-'128–140'→124–136 + s114-'133–145'→137–153 + s119-'201–209'→204–212!)** + **★★★ 212-VPIISOV-ŠTEVJE-IZ-VRSTIC-6.× — NAJVEČJE-leto-korpusa (2.3×-sredina! KOLERA-epidemia!)** (vrstna-aritmetika 12+12+14+12+13+13+13+13+12+12+13+13+12+12+13+14+9 + meseci J8+F9+M7+A13+M1+J6+J8+A73-MAX-KOLERA+S41+O13+N12+D9!) + **★★★ GLAVE-V-DATUMSKI-CELICAH-×6-REKORD-ta-seja (41.-s102-'1873.'-Jänner + s105-'1873.'-Feber/März-prečrtan + s106-'1873. Jüni'-DUPKAT-celica + s108-'August'-DUPKAT-celica + s115-'1873.'-October-DUPKAT-celica + 43.-s119-'December 1873'!)** + **★★★ KROP-KOREKCIJE-×7 (z71-'Griblje-37-Maria-Hrušič'-VLM-FALSIFIKACIJA→Gradoc-43-Škipanić-NI-GRIBLJE! + z76-'Mariana-Pojkl'→'Marcus-Dozeth-apl.-Ružar'-MOŠKI-Griblje-DVOJNOST-h58! + z112-'55J'→'5¾-J' + z115-'Brune'→'Brime' + z30-'Mariund'→'Marcus-Jakofčič' + z177-h[?]→h11-LUNIČ + z140-'9J'→'1-[?]')** + LUNIČ-h11-NIT-3.-LETO (z177-63J-Cholera → P203-h11-16dni → P202-h11-KUNIĆ!) + h65-×2-KLASTER (z8-dvojni-ime-vrstica 'Jurbya-baumann+Mathias-Milthin' + z9-Küllik-½-Gäblerin-32½J-Kindbett!) + BRIME-h24-NIT (z115-Sept → P203-z6-Feber-1874!) + PEZDIRC-×2-1873 (z55-Georg-h41 + z63-Katharina-h40!) + HRIZAN-grafia-×2 (z49 + z80!) + h13-×2-otroška + h28-×2-v-3-dneh + h30-×2 + h43-×2 + h10-×2 + ULEDBA-×3-konec-1873 (z211-h16-Brume-31-Dez→1-Jän + z212-Gradec + P203-z1-Podiner!) + otroška-umrljivost-26%-10/38-jasna; **1873 = 212 vpisov (z1–z212) / 38 Griblje-vpisov / 30 hiš-REKORD**; **38 NOVIH BLOKOV parish.ts: vitals 1406 → 1444 · 04106 = 187 → 225 · 04894 = 520-NESPREMENJENO · p80 94-NESPREMENJENO · korpus 93-NESPREMENJEN**; skripte p204 (fetch-md5-2-kroga + read + crop + build-entries + merge + build-proof) + qa-p204 (204. kontrola!) + dokaz parish-death-1873-04106.json (212 entries: 38-Griblje + 174-druge! 14-anomalij + 11-crossChecks + honesty-9 + leadP205-1872!) + pt-luknja-REGENERACIJA (225/1444!); **★★★ PREDZGODOVINA-LINIJA-13/29-LET!** (P205-LEAD: 1872 — s101-TAIL-×9-DEZ-1872-ŽE-VLM-PREBRANA ('finis'!) + s100-ŽE-FETCHAN+VLM → probe-s092–s101!)",
    "P204: THE PARISH OF PODZEMELJ — THE DEATH-REGISTER-PREHISTORY 04106, THE YEAR 1873 = THE 13th YEAR — ★★★ THE-CHOLERA-YEAR (issue #18): the-frame + **★★★ THE-1872/73-BOUNDARY = s102 (the-'1873.'-HEAD-IN-THE-Z1-DATE-CELL = the-41st-INVARIANT-CONFIRMATION + 'Incipit annus Domini' + restart-1–12!)** + **★★★ THE-1873/74-BOUNDARY = s119 (the-TAIL-9-DEZ-1873-ordinals-204–212-KROP! + the-'December 1873'-HEAD-IN-THE-Z204-CELL = the-43rd-INVARIANT + the-'1874. Jänner Incipit annus Domini'-boundary-head!)** + **★★★ the-DOUBLE-SCAN-3.×: s103==s104 = page-98-×2!** + **★★★ the-SCRIBAL-ORDINAL-DUPLICATES-×4-at-page-borders (24/37/61/153!) + GAPS-×5 (67 + 141–144!) → neto-−1** + **★★★ VLM-ORDINAL-OFF-BY-N-×3-KROP-MARGIN-FORENSICS-RESOLVED** + **★★★ THE-212-ENTRIES-COUNT-FROM-ROWS-6.× — THE-BIGGEST-YEAR (the-CHOLERA-epidemic!)** + **★★★ THE-HEADS-IN-THE-DATE-CELLS-×6-RECORD** + **★★★ KROP-CORRECTIONS-×7 (z71-NOT-GRIBLJE! + z76-GENDER + z112-age + z115-name + z30-name!)** + the-LUNIČ-h11-THREAD-3rd-YEAR + the-h65-×2-CLUSTER + the-BRIME-h24-THREAD + PEZDIRC-×2 + the-ULEDBA-×3-at-1873-end + the-child-mortality-26%; **1873 = 212 entries / 38 Griblje / 30 houses-RECORD**; **38 NEW BLOCKS: the vitals 1406 → 1444 · the 04106 = 187 → 225**; the scripts p204 + the qa-p204 (the 204th check!) + the evidence parish-death-1873-04106.json (212 entries!) + the pt-gap-REGENERATION (225/1444!); **★★★ THE-PREHISTORY-LINE-13/29-YEARS!** (the P205-LEAD: 1872 — the-s101-TAIL-×9-DEZ-1872-ALREADY-READ ('finis'!) + the-s100-ALREADY-FETCHED+VLM → the-probe-s092–s101!)",
    p204Errors.length === 0,
    p204Errors.length === 0
      ? `38 vpisov / 212 vrstic (števje-iz-vrstic-6.×!) / 30 hiš (REKORD!) · KOLERA-LETO-1873 (A73+S41!) · MEJA-s102-'1873.'-celici (41.-POTRDITEV) + s119-'December 1873'-celici (43.-POTRDITEV) · DOUBLE-SCAN-3.×-s103==s104 · ORDINAL-DUPKATI-×4 + LUKNJE-×5 · VLM-OFF-BY-N-×3-KROP-REŠENE · GLAVE-V-CELICAH-×6-REKORD · KROP-KOREKCIJE-×7 (z71-NI-GRIBLJE!) · LUNIČ-h11-NIT-3.-leto · h65-×2 · ULEDBA-×3 · otroška-26% · **PREDZGODOVINA-13/29!** · vitals 1444 · 04106 225 · 04894 520`
      : p204Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)

# ——— B: SANITIZACIJA 1406→1444 + 187→225 + yearset +1873 ———
src = src.replace("HOUSE_VITALS.length !== 1406", "HOUSE_VITALS.length !== 1444")
src = src.replace('04106").length !== 187', '04106").length !== 225')
OLD_SET = "(h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885"
src = src.replace(OLD_SET, "(h.year ?? 0) !== 1873 && " + OLD_SET)
src = src.replace("04106-bloki izven {1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1873 še nebrani!)",
                  "04106-bloki izven {1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina: 1857–1872 še nebrani!)")
src = src.replace("vitals 1406 · 04106 187 · 04894 520", "vitals 1444 · 04106 225 · 04894 520")
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: total-{src.count('HOUSE_VITALS.length !== 1444')} | 04106-{src.count('04106\").length !== 225')}")

# ——— C: skripte-kaskada (skip p59/p199–p204) ———
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p59_ps_blatt_headers", "p199_", "p200_", "p201_", "p202_", "p203_", "p204_")
patched = 0
for f in files:
    if any(s in f for s in skip):
        continue
    t = Path(f).read_text(encoding="utf-8")
    if "1406" not in t and "== 187" not in t:
        continue
    o = t
    t = t.replace("1406", "1444").replace('.get("04106") == 187', '.get("04106") == 225').replace("04106 == 187", "04106 == 225").replace("04106==187", "04106==225").replace("skupaj == 187", "skupaj == 225").replace('"04106") == 187', '"04106") == 225').replace("(04106, 187)", "(04106, 225)").replace("== 187,", "== 225,")
    if t != o:
        Path(f).write_text(t, encoding="utf-8")
        patched += 1
print(f"skripte-patched: {patched}")

# ——— D: verifier-patch p19x–p203 ———
vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p20[0123]_parish*.py")):
    t = f.read_text(encoding="utf-8")
    o = t
    t = t.replace("04106 == 187", "04106 == 225").replace("04106==187", "04106==225").replace('04106": 187', '04106": 225').replace("skupaj == 187", "skupaj == 225").replace('"04106") == 187', '"04106") == 225').replace("(04106, 187)", "(04106, 225)").replace('byBook"]["04106"] == 187', 'byBook"]["04106"] == 225')
    t = t.replace("vitals == 1406", "vitals == 1444").replace("vitalsTotal == 1406", "vitalsTotal == 1444").replace('vitalsTotal"] == 1406', 'vitalsTotal"] == 1444').replace('!== 1406"', '!== 1444"').replace("1406-številcev", "1444-številcev").replace("vitals-števec-1406", "vitals-števec-1444").replace("vitals-1406", "vitals-1444")
    t = re.sub(r'set\(izven\) == \{"1874"', 'set(izven) == {"1873", "1874"', t)
    t = t.replace('",".join(leta) == "1874,1875', '",".join(leta) == "1873,1874,1875')
    t = t.replace('join(leta) == "1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"',
                  'join(leta) == "1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885"')
    if t != o:
        f.write_text(t, encoding="utf-8")
        vpatched += 1
print(f"verifierji-patched: {vpatched}")

# ——— E: pt-luknja ———
ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1444
pt["corpus"]["byBook"]["04106"] = 225
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P204: +38-blokov-1873-KOLERA (04106 187→225, vitals 1406→1444, DOUBLE-SCAN-s103==s104 + ordinal-dupkati-×4/luknje-×5!)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04106']}")
