#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P232 — INSERT qa-p232 + sanitizacija (1870→1887, 04104=218→237, yearset-04104-{1874..1885}, pt-luknja)."""
from pathlib import Path
import glob, json, re

ROOT = Path("/home/z/my-project")
QA = ROOT / "src/lib/qa-parish.ts"
src = QA.read_text(encoding="utf-8")
ANCHOR = "  // ——— qa-p231: KRSTNA PREDZGODOVINA 04104 — leto 1875 = 11/15"
assert src.count(ANCHOR) == 1 and "qa-p232-parish-baptism-1874-04104" not in src

BLOCK = '''
  // ——— qa-p232: KRSTNA PREDZGODOVINA 04104 — leto 1874 = 12/15
  //      (P231: 1875 = 11/15!). 1874 = 92 vpisov (z1–z92!-P231-LEAD-'~92'-1:1-POTRJENO!-aritmetika 7+8+9+11+9+9+9+9+8+8+5 = 92!-1874-sklenjen-z92!) /
  //      19-GRIBLJE / 18-hiš (h40-×2-DUEL-z51-vs-z82!-RAZLIČNI-družini!) + ★★★ MEJA-1873/74-s37-SREDI-PAGI-'Initium-anni-Domini-1874'-KALLIGRAFIJA-NOVA-VARIANTA
  //      (1.-INITIUM-v-liniji!-TAIL-1873-zap-28[~98-X-open!]-Dez-28/29-Kloster! + RESTART-z1-1./1.-JÄNNER-krst-4.!-TIE-najzgodnejši-P221/P222!-12.-restart!)
  //      = 71.-POTRDITEV + ★★★ 'sken−3'-SEKVENČNO-s36–s47 (33–44!-12/12!-BREZ-duplikatov!) + ★★★ zap-POZICIJSKA-ARITMETIKA-4/4-POTRJENA (z73=zap-73!-z76!-z81!-z82!) +
  //      ★★★ PEZDIRC-×7-PORAST (vs-×5-P231!-+Zgajdire-hipoteza-→×8!) + ★★★ MILEK-×7-REKORD-PORAST + ★★★ BREZ-PRAZNIH-MESECEV-1.-LINIJI + ★★★ TRI-duhovnika-NOVI-×2.
  //      Dokaz: parish-baptism-1874-04104.json; skripte p232.
  {
  const p232Errors: string[] = [];
  const p232Bapt = HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && h.year === 1874);
  if (p232Bapt.length !== 19)
    p232Errors.push(`bloki 1874 (04104) ≠ 19 (${p232Bapt.length} — 19 Griblje-vpisov / 18-hiš-h40-DUEL! / 92-vpisov!)`);
  if (HOUSE_VITALS.length !== 1887)
    p232Errors.push(`HOUSE_VITALS ≠ 1887 (${HOUSE_VITALS.length} — P231: 1870; P232: + 19 blokov 1874-04104 = 1887!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 237)
    p232Errors.push(`bloki 04104 ≠ 237 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P231: 218; P232: + 19 × 1874 = 237!)`);
  if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)
    p232Errors.push("04104-bloki izven {1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885} (predzgodovina-12/15: 1874–1885-do-P233!)");
  if (!p232Bapt.some((h) => h.whatSi.includes("71.-POTRDITEV")))
    p232Errors.push("★★★ MEJA-1873/74-s37-SREDI-PAGI-'Initium-anni-Domini-1874'-KALLIGRAFIJA (TAIL-1873! + RESTART-z1-1./1.!-12.-restart!) ni označena");
  if (p232Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length < 7)
    p232Errors.push(`★★★ PEZDIRC-×7-Griblje ni dosežen (${p232Bapt.filter((h) => h.whatSi.includes("PEZDIRC")).length}/7!)`);
  if (!p232Bapt.some((h) => h.whatSi.includes("PEZDIRC-matec-nit")))
    p232Errors.push("★★★ PEZDIRC-matec-nit (z24-h48-X-potrjen!) ni označena");
  if (!p232Bapt.some((h) => h.whatSi.includes("PEZDIRC-oče-nit")))
    p232Errors.push("★★★ PEZDIRC-oče-nit (z82-h40-X-potrjen!) ni označena");
  if (!p232Bapt.some((h) => h.whatSi.includes("PEZDIRC-boter-nit")))
    p232Errors.push("★★★ PEZDIRC-boter-nit (z65/z91-X-potrjen!) ni označena");
  if (p232Bapt.filter((h) => h.whatSi.includes("MILEK")).length < 7)
    p232Errors.push(`★★★ MILEK-×7-REKORD ni dosežen (${p232Bapt.filter((h) => h.whatSi.includes("MILEK")).length}/7!)`);
  if (p232Bapt.filter((h) => h.whatSi.includes("HRIŽAN")).length < 5)
    p232Errors.push(`★★★ HRIŽAN-×5 ni dosežen (${p232Bapt.filter((h) => h.whatSi.includes("HRIŽAN")).length}/5!)`);
  if (!p232Bapt.some((h) => h.whatSi.includes("HRIŽAN-oče+matec-DVOJNI")))
    p232Errors.push("★★★ HRIŽAN-oče+matec-DVOJNI-nit (z81-h3-Peter+Dorothea!) ni označena");
  if (!p232Bapt.some((h) => h.whatSi.includes("HERBAVEC-×3-DVOJNI")))
    p232Errors.push("★★★ HERBAVEC-×3-DVOJNI-nit (z23-h30-oče+boter+botra!) ni označena");
  if (!p232Bapt.some((h) => h.whatSi.includes("LEGDIRE-oče-nit")))
    p232Errors.push("★★★ LEGDIRE-oče-nit (z76-h32!) ni označena");
  if (!p232Bapt.some((h) => h.whatSi.includes("zap-73-VIDEN-1:1")))
    p232Errors.push("★★★ zap-POZICIJSKA-ARITMETIKA-1:1 (z73=zap-73!) ni označena");
  if (!p232Bapt.some((h) => h.whatSi.includes("h9-NOVA-hiša")))
    p232Errors.push("★★★ h9-NOVA-hiša (z63!) ni označena");
  if (!p232Bapt.some((h) => h.whatSi.includes("TAIL-1874-GRIBLJE")))
    p232Errors.push("★★★ TAIL-1874-GRIBLJE (z90/z91-P231-1:1-KRIŽ!) ni označena");
  if (p232Bapt.filter((h) => h.whatSi.includes("MODRI")).length < 4)
    p232Errors.push(`★★★ MODRI-×4-Griblje ni dosežen (${p232Bapt.filter((h) => h.whatSi.includes("MODRI")).length}/4!)`);
  if (new Set(p232Bapt.map((h) => h.houseNo)).size !== 18)
    p232Errors.push(`★★★ 18-hiš-DISTINCT (h40-×2-DUEL!) ni izpolnjeno (najdeno ${new Set(p232Bapt.map((h) => h.houseNo)).size})`);
  push(
    "qa-p232-parish-baptism-1874-04104",
    "P232: ŽUPNIJA PODZEMELJ — KRSTNA PREDZGODOVINA 04104, LETO 1874 = 12/15 (issue #18): okvir — s37–s47 (11 skenov; s37-SREDI-PAGI-MEJA-'Initium'!-TAIL-1873-r1! + s38–s44-1874!-s45–s47-TAIL-1874-P231-predizkop!-DESCENDING-probe-P231-LEAD-s36–s45!-2×-neodvisna-md5-12/12!) + **★★★ FOLIACIJA-'sken−3'-SEKVENČNO-s36–s47 (33–44!-12/12-visoko!-s37='34'-s44='41'-s45='42'-s47='44'!-formula-CONTINUES-iz-P231-s45–s60!-BREZ-duplikatov-v-oknu!-2-DUPLIKATA-še-vedno-pred-s36-neznana-lokacija-s1–s35!)** + **★★★ MEJA-1873/74 = s37-SREDI-PAGI + 'Initium-anni-Domini-1874'-VELIKA-KALLIGRAFIJA-NOVA-VARIANTA-1.-INITIUM-kalligrafija-v-liniji (vs-'finis-Anni-1875'-P230-s64!-vs-BREZ-kalligrafije-P231-s47!-4.-mejna-varianta-zaporedoma: P229-ENO-STRANSKA!-P230-DVO-STRANSKA!-P231-SREDI-PAGI!-P232-SREDI-PAGI-z-INITIUM!): s37-r1 = TAIL-1873 (zap-28[~98/lokalni-restart-X-open!-vs-s36-zap-94-NOV!]-Dez-28/29-Kloster-h69-Amalia-oče-Ignaz-Lobonik[~Osmidžan!]-'Franz-Dovgan'-podpis!) → 'Initium-anni-Domini-1874'-KALLIGRAFIJA-ČEZ-VRSTO (X-potrjen!) → s37-r2 = RESTART-z1-NA-DAN-1./1.-JÄNNER (krst-4.!-Gradac-h31-Maria-oče-Martin-Malešič-½G!-babica-nota!-TIE-najzgodnejši-P221-1.1!-P222-1.1!-12.-restart-z1-linije!-'glava-v-vrstici-2'-'Jahr-1874'!-podpis-'Albin-Schringer/Schwinger-Coop.'-NOVI-DUHOVNIK!) = 71.-POTRDITEV-invariante (70.-P231!) | s47-SREDI-PAGI-MEJA-1874/75-P231!** + **★★★ 92-VPISOV (z1–z92!-P231-LEAD-'1874-vpisov-pričakovano-~92'-1:1-POTRJENO!-aritmetika 7+8+9+11+9+9+9+9+8+8+5 = 92!-1874-sklenjen-z92!) + zap-stolpec-VIDEN-s37 (z1–z7-restart!-z2-GRIBLJE-VIDEN!)-in-s45/s46 (zap-72–87!-P231-križ!-★★★ POZICIJSKA-ARITMETIKA-4/4-POTRJENA: z73=zap-73!-z76=zap-76!-z81=zap-81!-z82=zap-82!)-NEZAPISAN-s38–s44 (starša-forma-vs-P231-s47–s63-PARALELA!)** + **★★★ 19-GRIBLJE / 18-hiš (h40-×2-DUEL-z51-'40[~10]'-Zgajdire?-družina!-vs-z82-'40[~4]'-PEZDIRC-družina!-RAZLIČNI!-obe-X-potrjeni!-vs-P231-h48-×2-PARALELA!): z2-h12-DRAGOŠ-oče-JAKOFČIČ-zakonca-botra-DVOJNI!-matec-DUEL-3-way-X-open!-NOVI-duhovnik-'Albin-Schwinger-Coop.'! + z8-h46-MILEK-×2-matec+botra-DVOJNI!-HLOBUČAR-oče-X-★★★-3-way-ločitev!-stan-DUEL-½/¾G! + z10-h45-MILEK-boter!-BRIME-oče-garble!-MARKOVIN-matec-garble!-hisna-45/25-DUEL-X-★★★-REŠEN-'45'! + z20-h44-STRAUČIČ-oče+boter-DVOJNI!-KLOBUČAR-matec+botra-DVOJNI!-MESEC-MÄRZ-X2-potrjen!-'Lužana'-nota! + z21-h18-SIMEC-oče!-JANAPIČ/ZUNIČ-DUEL!-MODRI-†3.2.1933! + z23-h30-HERBAVEC-×3-oče+boter+botra-VSE-ISTI!-vas-DUEL-REŠEN-X2! + z24-h48-KOBLAR-oče-X-★★★-3-way!-PEZDIRC-matec-X-★★★!-h48-continuum! + z27-h39-JARREC-oče-X-★★★-NE-Simec!-MESEC-JUNI-X-open (VLM-neberljiv!-kronologija!-vs-full-'August'-NAPAČEN!)! + z51-h40-ZGAJDIRE-oče-X-★★★-PEZDIRC-hipoteza!-vas-DUEL-×2/×1-GRIBLJE-majoriteta!-MILEK-botra!-BRODARIČ-boter! + z57-h60-FELK-oče!-HRIŽAN-matec-X!-PILAK-botra-garble!-s43-GLAVA-'1871'-VLM-MISREAD (kronologija-✓)! + z58-h49-BRODARIČ-oče!-PEZDIRC-×2-matec+botra-X-★★★!-DEBLIČ-botra!-'Fabijan-Kragelj[?]-Cap'-NOVI-duhovnik-X-open! + z63-h9-NOVA-hiša!-JAŠKOFČIČ-oče+matec-DVOJNI!-KELHO-boter-P231-'Kelčho'-PARALELA!-DRAGOŠ-botra! + z65-h13-PEZDIRC-boter-X-★★★!-HRIŽAN-matec!-MODRI-'preseljen[?]-19.3.1882'! + z73-h66-HRIŽAN-oče-X-★★★-4-way-DUEL-rešen!-MODRI-†22.10.1930-P231-križ!-zap-73-VIDEN-1:1!-'MILCH'-matec-garble-X-open!-LEGDIRE-boter!-66/64-DUEL-X-rešen! + z76-h32-LEGDIRE-oče-KOMPLET!-TROJNI-hisna-DUEL-32/52/62-X-★★★-REŠEN-'32'!-zap-76-VIDEN-1:1!-NOVAK/VORALT-DUEL! + z81-h3-HRIŽAN-oče+matec-DVOJNI-Peter+Dorothea!-zap-81-VIDEN-1:1!-KUMPAR+LAH-botra-garble! + z82-h40-PEZDIRC-oče-X-★★★!-MODRI-'†29.11.1947[?]-vs-P231-1944[?]'-DUEL!-zap-82-VIDEN-1:1!-JAKOFČIČ/PAHOVIČ-matec-DUEL!-HLOBUČAR-botra (z8-PARALELA)!-DEBLIČ-botra-continuum! + z90-h22-TAIL-MILEK-oče+boter-DVOJNI!-PEZDIRC-matec!-BRODARIČ-botra!-hisna-22/42-DUEL-X-★★★-REŠEN-'22'! + z91-h65-TAIL-MILEK-oče!-PEZDIRC-boter-X-★★★-REŠEN!-HARASINIČ-matec!-ime-DUEL-Maria/Franziska-X-REŠEN!-PUTLAR/TURK-botra-garble!** + **★★★ PEZDIRC-×7-GRIBLJE-PORAST (vs-×5-P231!-+z51-'Zgajdire'-hipoteza-→×8!-X-★★★-POTRJENI-×5!-grafija-continuum-Pezdirc/Pezdire!)** + MILEK-×7-REKORD-PORAST (vs-×4!) + HRIŽAN-×5 + KLOBUČAR/HLOBUČAR-×4 + JAKOFČIČ-×4 + BRODARIČ-×3-KOMPLET + DEBLIČ-×2-continuum + LEGDIRE-×2-KOMPLET + STRAUČIČ-×2-DVOJNI + HERBAVEC-×3-DVOJNI + DRAGOŠ-×2 + SIMEC-×1 + KOBLAR-×1-X + HARASINIČ-×1 + **★★★ NEZAKONSKI-×0-GRIBLJE-1.-LINIJI (vs-×2-P231!-vs-×6-P230-REKORD!)** + **★★★ MODRI-×4-Griblje (†3.2.1933[?]!-'preseljen[?]-19.3.1882'!-†22.10.1930!-†29.11.1947[?]!-razpon-1882–1947!-+CHICAGO-1949-ne-G-P231-kontrola-1:1!)** + **★★★ BREZ-PRAZNIH-MESECEV-1.-LINIJI (J1+F2+M2+A2+Juni1+Aug1+S3+O1+N4+D2 = 19!-vs-P231-2-prazne!-vs-P230-3!-vs-P229-2!)** + **★★★ TRI-DUHOVNIKA-1874-IZMENJAVA ('Albin-Schringer/Schwinger-Coop.'-NOVI-s37-restart!-'Franz-Dovgan'-continuum!-'Fabijan-Kragelj[?]-Cap.'-NOVI-X-open-KURRENT-garble!-vs-1875-DOVGAN/HOGGIA-2-duhovnika!-TAIL-1873-'Franz-Dovgan'!)** + babica-nota-z1-Gradac + TAIL-1873-zap-28[~98]-X-open + rdeči-tički-continuum + **19 NOVIH BLOKOV parish.ts: vitals 1870 → 1887 · 04104 = 218 → 237 · 04105/04106/04894/04455-NESPREMENJENI**; skripte p232 (fetch-2×-md5-12/12 + celostanska-branja-×12 (s36–s47!) + probe-glave/foliacije/prve-vrstice/dna-Q1–Q4 + vrstični-krops-×11-sheetov + ločilni-krops-X1–X3 (×36!)) + qa-p232 (232. kontrola!) + dokaz parish-baptism-1874-04104.json (92-vpisov: 19-Griblje + 73-druge! anomalije/crossChecks/honesty!) + pt-luknja-237/1887; **★★★ KRSTNA-PREDZGODOVINA-LINIJA-12/15-LET!** (P233-LEAD: 1873 — MEJA-1873/74-ŽE-NAJDENA-s37-SREDI-PAGI-'Initium'!-TAIL-1873-s37-r1-ŽE-VLM-×1-vrstica-zap-28[~98]! → MEJA-1872/73-pred-s36 → probe-s28–s36-DESCENDING!-'sken−3'-pričakovana-s35='32'! (s36='33'!-s30='27'!)-POZOR: 2-DUPLIKATA-še-vedno-neznana-lokacija-s1–s35!-1873-vpisov-pričakovano-~95 (zap-94-s36-r7-Nov-25-+Dez-28-tail!)-'Initium-anni-Domini-1873'-kalligrafija-LAHKO-se-ponovi!)",
    "P232: THE PARISH OF PODZEMELJ — THE BAPTISM-REGISTER-PREHISTORY 04104, THE YEAR 1874 = 12/15 (issue #18): the-frame — s37–s47 (11 scans; 2×-INDEPENDENT-md5-12/12!) + **★★★ THE-FOLIATION-'scan−3'-SEQUENTIAL-s36–s47 (33–44!-12/12!-THE-FORMULA-CONTINUES!-NO-DUPLICATES!-2-DUPLICATES-still-before-s36-unknown-location-s1–s35!)** + **★★★ THE-1873/74-BOUNDARY = s37-MID-PAGE + 'Initium-anni-Domini-1874'-THE-GREAT-CALLIGRAPHY-THE-NEW-VARIANT-THE-1ST-INITIUM-CALLIGRAPHY-IN-THE-LINE (the-TAIL-1873-zap-28!-Dez-28/29-Kloster! + the-RESTART-z1-1./1.-JÄNNER-the-krst-4.!-the-TIE-the-earliest-P221/P222!-the-12th-restart!-the-NEW-priest-'Albin-Schwinger-Coop.'!) = the-71st-CONFIRMATION (70th-P231!)-4-THE-BOUNDARY-VARIANT-IN-A-ROW!** + **★★★ 92-ENTRIES (z1–z92!-the-P231-LEAD-'~92'-1:1-CONFIRMED!) + the-ZAP-POSITIONAL-ARITHMETIC-4/4-CONFIRMED (z73=zap-73!-z76!-z81!-z82!)** + **★★★ 19-GRIBLJE / 18-houses (h40-×2-DUEL!)** + **★★★ THE-PEZDIRC-×7-GRIBLJE-GROWTH (vs-×5-P231!-+the-Zgajdire-hypothesis-→×8!-X-★★★-CONFIRMED-×5!)** + MILEK-×7-THE-RECORD-GROWTH + HRIŽAN-×5 + JAKOFČIČ-×4 + **★★★ THE-ILLEGITIMATE-×0-GRIBLJE-THE-1ST-IN-THE-LINE** + **★★★ THE-BLUE-ANNOTATIONS-×4-GRIBLJE-† (1882–1947!)** + **★★★ NO-EMPTY-MONTHS-THE-1ST-IN-THE-LINE** + **★★★ THE-THREE-PRIESTS-1874-THE-ALTERNATION (the-'Albin-Schwinger-Coop'-NEW!-the-'Franz-Dovgan'-continuum!-the-'Fabijan-Kragelj[?]-Cap'-NEW-X-open!)** + **19 NEW BLOCKS: the vitals 1870 → 1887 · the 04104 = 218 → 237**; the scripts p232 + qa-p232 (the 232nd check!) + the evidence parish-baptism-1874-04104.json (92-entries: 19-Griblje + 73-others!) + the pt-gap-237/1887; **★★★ THE-BAPTISM-PREHISTORY-LINE-12/15-YEARS!** (the P233-LEAD: 1873 — the-boundary-ALREADY-FOUND-s37-MID-PAGE-'Initium'! → the-TAIL-1873-×1-row! → probe-s28–s36-DESCENDING!)",
    p232Errors.length === 0,
    p232Errors.length === 0
      ? `19 vpisov / 92-vpisov (z1–z92!-LEAD-~92-1:1!-z100-ni!-1874-sklenjen-z92!) / 18-hiš-h40-DUEL · MEJA-1873/74-s37-SREDI-PAGI-'Initium-anni-Domini-1874'-KALLIGRAFIJA-NOVA-VARIANTA-71.-POTRDITEV (TAIL-1873-zap-28!-RESTART-z1-1./1.!-12.-restart!-'Albin-Schwinger'-NOVI!) · 'sken−3'-33–44-SEKVENČNO · zap-ARITMETIKA-4/4 (z73/z76/z81/z82!) · PEZDIRC-×7-PORAST · MILEK-×7-REKORD · HRIŽAN-×5 · NEZ-×0-1.-LINIJI · MODRI-×4 · BREZ-PRAZNIH-MESECEV-1.-LINIJI · TRI-duhovnika-NOVI-×2 · **LINIJA-12/15!** · vitals 1887 · 04104 237`
      : p232Errors.join("; "),
  );
  }

'''
src = src.replace(ANCHOR, BLOCK + ANCHOR, 1)
src = src.replace("HOUSE_VITALS.length !== 1870", "HOUSE_VITALS.length !== 1887")
# P231-block 04104-total: 218 → 237 (zdaj vključuje 1874!)
src = src.replace('if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 218)',
                  'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length !== 237)')
src = src.replace('p231Errors.push(`bloki 04104 ≠ 218 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875 = 218!)`)',
                  'p231Errors.push(`bloki 04104 ≠ 237 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04104").length} — P221: 25 × 1885; P222: + 21 × 1884; P223: + 19 × 1883; P224: + 25 × 1882; P225: + 17 × 1881; P226: + 22 × 1880; P227: + 22 × 1879; P228: + 16 × 1878; P229: + 20 × 1877; P230: + 14 × 1876; P231: + 17 × 1875; P232: + 19 × 1874 = 237!)`)')
# yearset-04104: {1875..1885} → {1874,...,1885} (v P231-, P230-, P229-, P228-, P227-, P226-, P225-blokih!)
old_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
new_yearset = 'if (HOUSE_VITALS.filter((h) => h.bookSignature === "04104" && (h.year ?? 0) !== 1874 && (h.year ?? 0) !== 1875 && (h.year ?? 0) !== 1876 && (h.year ?? 0) !== 1877 && (h.year ?? 0) !== 1878 && (h.year ?? 0) !== 1879 && (h.year ?? 0) !== 1880 && (h.year ?? 0) !== 1881 && (h.year ?? 0) !== 1882 && (h.year ?? 0) !== 1883 && (h.year ?? 0) !== 1884 && (h.year ?? 0) !== 1885).length > 0)'
n_y = src.count(old_yearset)
src = src.replace(old_yearset, new_yearset)
for ph in ("p231Errors", "p230Errors", "p229Errors", "p228Errors", "p227Errors", "p226Errors", "p225Errors"):
    src = src.replace(f'{ph}.push("04104-bloki izven {{1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-11/15: 1875–1885-do-P232!)");',
                      f'{ph}.push("04104-bloki izven {{1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885}} (predzgodovina-12/15: 1874–1885-do-P233!)");')
QA.write_text(src, encoding="utf-8")
print(f"qa-parish: 1887×{src.count('HOUSE_VITALS.length !== 1887')} · qa-p232×{src.count('qa-p232-parish-baptism-1874-04104')} · yearset-patched-{n_y}")

# --- skripte + verifierji patch (1870→1887, 218→237) ---
files = sorted(set(glob.glob(str(ROOT / "scripts/**/*.py"), recursive=True) + glob.glob(str(ROOT / "scripts/**/*.mjs"), recursive=True)))
skip = ("p232_",)
patched = 0
for f in files:
    if any(s2 in f for s2 in skip): continue
    t = Path(f).read_text(encoding="utf-8")
    if "1870" not in t: continue
    o = t
    t = t.replace("1870", "1887")
    if t != o:
        Path(f).write_text(t, encoding="utf-8"); patched += 1
print(f"skripte-patched: {patched}")

vpatched = 0
for f in sorted(ROOT.glob("scripts/p19*.py")) + sorted(ROOT.glob("scripts/p2[0-2][0-9]_parish*.py")):
    if "p232" in f.name: continue
    t = f.read_text(encoding="utf-8"); o = t
    for a, b in [("vitals == 1870", "vitals == 1887"), ("vitalsTotal == 1870", "vitalsTotal == 1887"),
                 ('vitalsTotal"] == 1870', 'vitalsTotal"] == 1887'),
                 ('"vitalsTotal": 1870', '"vitalsTotal": 1887'),
                 ('\\"vitalsTotal\\": 1870', '\\"vitalsTotal\\": 1887'),
                 ('!== 1870"', '!== 1887"'),
                 ("1870-številcev", "1887-številcev"),
                 ("vitals-števec-1870", "vitals-števec-1887"), ("vitals-1870", "vitals-1887")]:
        t = t.replace(a, b)
    # 04104-total 218 → 237 v verifierjih p221–p231
    t = t.replace("== 218", "== 237")
    if t != o:
        f.write_text(t, encoding="utf-8"); vpatched += 1
print(f"verifierji-patched: {vpatched}")

# p191 EXPECTED_CORPUS: 04104 218 → 237
p191 = ROOT / "scripts/p191_pt_luknja_final.py"
t = p191.read_text(encoding="utf-8"); o = t
t = t.replace('"04104": 218}', '"04104": 237}')
t = t.replace("# POSODABLJENO P231: + krstna-04104 = 218 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230 + 17×1875-P231!)",
              "# POSODABLJENO P232: + krstna-04104 = 237 (25×1885-P221 + 21×1884-P222 + 19×1883-P223 + 25×1882-P224 + 17×1881-P225 + 22×1880-P226 + 22×1879-P227 + 16×1878-P228 + 20×1877-P229 + 14×1876-P230 + 17×1875-P231 + 19×1874-P232!)")
if t != o: p191.write_text(t, encoding="utf-8"); print("p191-EXPECTED_CORPUS-patched (237)")

ptp = ROOT / "research/issue17/pt-luknja-18-final.json"
pt = json.loads(ptp.read_text(encoding="utf-8"))
pt["corpus"]["vitalsTotal"] = 1887
pt["corpus"]["byBook"]["04104"] = 237
pt["corpus"]["housesNote"] = (pt["corpus"].get("housesNote") or "") + " | P232: +19-blokov-1874-krstna-04104-12/15 (vitals 1870→1887; 04104 218→237; 92-vpisov z1–z92-LEAD-~92-1:1-POTRJENO + MEJA-1873/74-s37-SREDI-PAGI-'Initium-anni-Domini-1874'-KALLIGRAFIJA-NOVA-VARIANTA-1.-INITIUM-v-liniji-71.-POTRDITEV (TAIL-1873-zap-28! + RESTART-z1-1./1.!-12.-restart!-'Albin-Schwinger'-NOVI-duhovnik!) + 'sken−3'-33–44-SEKVENČNO-BREZ-duplikatov + zap-ARITMETIKA-4/4-POTRJENA (z73/z76/z81/z82!) + 19-GRIBLJE/18-hiš-h40-DUEL + PEZDIRC-×7-PORAST + MILEK-×7-REKORD + NEZ-×0-1.-LINIJI + MODRI-×4 + BREZ-PRAZNIH-MESECEV-1.-LINIJI + TRI-duhovnika-NOVI-×2 → P233-LEAD-1873)"
ptp.write_text(json.dumps(pt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"pt-luknja: {pt['corpus']['vitalsTotal']}/{pt['corpus']['byBook']['04104']}")
