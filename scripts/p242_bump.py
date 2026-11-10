#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P242 — sanacija zastarelih agregatov: 1957→1966 · 214→223 · 207→216 · 181→190 + qa-p242 vstavitev."""
import re, sys

ROOT = "/home/z/my-project"
QA = f"{ROOT}/src/lib/qa-parish.ts"
PT = f"{ROOT}/research/issue17/pt-luknja-18-final.json"
delo = 0

# ——— 1. qa-parish.ts ———
src = open(QA, encoding="utf-8").read()
orig = src

# 1a. HOUSE_VITALS 1957→1966 (garda + sporočila)
for a, b in [
    ("HOUSE_VITALS.length !== 1957", "HOUSE_VITALS.length !== 1966"),
    ("HOUSE_VITALS ≠ 1957", "HOUSE_VITALS ≠ 1966"),
]:
    n = src.count(a); src = src.replace(a, b); delo += n

# 1b. bloki-04455 214→223 (vse gard + sporočila)
for a, b in [
    ("p80Marr.length !== 214", "p80Marr.length !== 223"),
    ("p115Marr.length !== 214", "p115Marr.length !== 223"),
    ("p116Marr.length !== 214", "p116Marr.length !== 223"),
    ('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 214', 'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 223'),
    ("p152Blocks.length !== 214", "p152Blocks.length !== 223"),
    ("bloki 04455 ≠ 214", "bloki 04455 ≠ 223"),
    ("bloki-04455 ≠ 214", "bloki-04455 ≠ 223"),
    ("poročni vpisi (04455) ≠ 206", "poročni vpisi (04455) ≠ 223"),
]:
    n = src.count(a); src = src.replace(a, b); delo += n

# 1c. sidra 207→216 + 1881:9 gardo
n = src.count("p80MarrAnchors.length !== 207"); src = src.replace("p80MarrAnchors.length !== 207", "p80MarrAnchors.length !== 216"); delo += n
n = src.count("poročna sidra ≠ 207"); src = src.replace("poročna sidra ≠ 207", "poročna sidra ≠ 216"); delo += n
n = src.count('sidra ≠ 207 (1882:7-P241!'); src = src.replace('sidra ≠ 207 (1882:7-P241!', 'sidra ≠ 216 (1881:9-P242! · 1882:7-P241!'); delo += n
# p80 letni gardi: dodaj 1881 vrstico pred 1882
a = "  p80MarrAnchors.filter((h) => h.year === 1882).length !== 7 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1881).length !== 9 ||\n" + a
if a in src and "year === 1881" not in src.split(a)[0][-400:]:
    src = src.replace(a, b, 1); delo += 1
# p152 sidra-sporočilo
a = "poročna sidra ≠ 207 (${p80MarrAnchors.length} — 201 + 6-novih-1882-P241!)"
b = "poročna sidra ≠ 216 (${p80MarrAnchors.length} — 207 + 9-novih-1881-P242!)"
if a in src: src = src.replace(a, b); delo += 1

# 1d. p152 dobe 181→190 + pred-linijskih 19→28 + 11→20
for a, b in [
    ("p152Pre !== 181 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 190 || p152Wwi !== 7 || p152Boom !== 26"),
    ("dobe-bloki ≠ 181/7/26", "dobe-bloki ≠ 190/7/26"),
    ("19 pred-linijskih (1882×7-P241!+1883×2+1884×3+1885×7)", "28 pred-linijskih (1881×9-P242!+1882×7-P241!+1883×2+1884×3+1885×7)"),
    ("11 pred-linijskih 1882-P241×7!", "20 pred-linijskih 1881-P242×9!+1882-P241×7!"),
    ("predvojna ≤1913 = 181 blokov", "predvojna ≤1913 = 190 blokov"),
]:
    n = src.count(a); src = src.replace(a, b); delo += n

open(QA, "w", encoding="utf-8").write(src)
print(f"qa-parish.ts: {delo} zamenjav")

# ——— 2. qa-p242 blok (pred qa-p241) ———
qa242 = '''  // ——— qa-p242: POROČNA PREDZGOVINA 04455 — leto 1881 = 5/13 (P242) ———
  {
    const p242Errors: string[] = [];
    if (HOUSE_VITALS.length !== 1966) p242Errors.push(`HOUSE_VITALS ≠ 1966 (${HOUSE_VITALS.length} — 9-novih-1881!)`);
    if (MARRIAGE_1881_GRIBLJE !== 9) p242Errors.push(`Griblje-poroke-1881 ≠ 9 (${MARRIAGE_1881_GRIBLJE})`);
    const p242Pri = ["27", "4", "28", "8", "42", "27", "41", "52", "16"];
    if (JSON.stringify(MARRIAGE_1881_HOUSES) !== JSON.stringify(p242Pri)) p242Errors.push(`hiše-1881 ≠ [27,4,28,8,42,27,41,52,16] (${MARRIAGE_1881_HOUSES.join(",")})`);
    if (MARRIAGE_1881_TOTAL !== 25) p242Errors.push("vpisi-1881 ≠ 25 (1–26-z-1-PRESKOKOM-12!-kontrast-1882-26-BREZ!)");
    if (MARRIAGE_1881_ZAP_SKIPPED !== 12) p242Errors.push(`zap-skipped-1881 ≠ 12 (${MARRIAGE_1881_ZAP_SKIPPED} — s41(11)→s42(13)!-[X-OPEN-DUEL-ali-16!])`);
    if (MARRIAGE_1881_XOPEN.length !== 2) p242Errors.push(`X-OPEN-dueli-1881 ≠ 2 (${MARRIAGE_1881_XOPEN.length})`);
    if (MARRIAGE_1881_VILLAGE_DUELS.length !== 4) p242Errors.push(`vas-dueli-1881 ≠ 4 (${MARRIAGE_1881_VILLAGE_DUELS.length})`);
    if (!MARRIAGE_1881_BLOCKS.some((h) => h.whatSi.includes("h52-FIRSTYEAR-DVIG-1882→1881"))) p242Errors.push("h52-FIRSTYEAR-DVIG-ni-označen (v17-Petrič!-P241-ZA-5-LET→ZA-6-LET!)");
    if (!MARRIAGE_1881_BLOCKS.some((h) => h.whatSi.includes("RESTART-1881-s39-letnica-v-stolpcu-NAD-vrstico-1-NOVA-5.-MEJNA-VARIANTA"))) p242Errors.push("restart-s39-letnica-v-stolpcu-ni-označena (NOVA-5.-mejna-varianta!)");
    if (!MARRIAGE_1881_BLOCKS.some((h) => h.whatSi.includes("PEZDIRC-ŽENIN-04455-1881-CONTINUUM"))) p242Errors.push("v14-PEZDIRC-ženi n-continuum-ni-označen (Georg-h42!)");
    if (!MARRIAGE_1881_BLOCKS.some((h) => h.whatSi.includes("TAPIČ↔ŠILAR-KRIŽ"))) p242Errors.push("v23-TAPIČ↔ŠILAR-križ-ni-označen (starši-neveste-Anna-geb.-TAPIČ!)");
    if (!MARRIAGE_1881_BLOCKS.some((h) => h.whatSi.includes("POLNI-GRIBLJE-BLOK ×2"))) p242Errors.push("POLNI-GRIBLJE-BLOK-×2-ni-označen (h28×h8 · h42×h27 · h41×h52!)");
    if (!MARRIAGE_1881_BLOCKS.some((h) => h.whatSi.includes("h27-×2-BLOKA-V-1-LETU-PRVIČ"))) p242Errors.push("h27-×2-bloka-ni-označena (v4-ženi n-+ v14-nevesta!)");
    // neodvisni PEZDIRC-križ 1881: korpus-bloki z PEZDIRC-v-whatSi = 1 (v14-Georg!)
    const p242Pez = MARRIAGE_1881_BLOCKS.filter((h) => /PEZDIRC/i.test(h.whatSi));
    if (p242Pez.length !== 1) p242Errors.push(`PEZDIRC-bloki-1881 ≠ 1 (${p242Pez.map((h) => h.houseNo).join(",")} — v14-Georg!-s40-v7-starši-izven-Griblje-blokov!)`);
    // neodvisni križ 1881: PRAZEN (iskreno!) — noben MILEK/MILIČ-vpis-v-1881 (v14-Hrizom-[~Križan]-NI-MILEK!)
    const p242Križ = MARRIAGE_1881_BLOCKS.filter((h) => MILIC_FAMILY_RE.test(h.whatSi));
    if (p242Križ.length !== 0)
      p242Errors.push(`križ-bloki-1881 ≠ [] (${p242Križ.map((h) => h.houseNo).join(",")} — nobenega-MILEK/MILIČ-v-1881-iskreno!-v14-'Hrizom'-NI-MILEK!)`);
    if (MILIC_FAMILY_TOTAL !== 237) p242Errors.push(`MILIČ-family-total ≠ 237 (${MILIC_FAMILY_TOTAL} — 1881-brez-novih-križev!)`);
    if (HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 223)
      p242Errors.push(`bloki-04455 ≠ 223 (${HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length} — 214 + 9-novih-leta-1881!)`);
    push(
      "qa-p242-parish-marriage-early-04455-1881",
      "P242: ŽUPNIJA PODZEMELJ — POROČNA PREDZGOVINA 04455, LETO 1881 = 5/13 (issue #18): s39–s44 (6 razprti-listov == Pag. 38–43; 25-vpisov-leta-1881-ŠTEVJE-IZ-ZAP-STOLPCA-1–11 + 13–26-z-1-PRESKOKOM-12!-s41(11)→s42(13)!-[X-OPEN-DUEL: ali-s42=12–15-preskok-16!]-5.-številčenjska-anomalija-linije-cf.-1885-vpis-3-P238!) · RESTART-1881 = s39-top (letnica-'1881'-v-DATUMSKEM-STOLPCU-NAD-VRSTICO-zap.-št.-1!-vpis-1 = 16.-Jänner!-NOVA-5.-MEJNA-VARIANTA-skromna!-cf.-1882-VELIKA-GLAVA-+ 1883-razporejena-+ 1884/1885-vrhnja!) · MEJA-1880/81 = s38→s39 (tail-1880-pričakovan-na-s38-P243!-[X-OPEN!]) · MEJA-1881/82 = s44→s45-glava (P241-1:1!-tail-1881 = vpis-26-20.-Dez!) · številčenje s39=1–4 · s40=5–7 · s41=8–11 · s42=13–16 (PRESKOK-12!) · s43=17–20 · s44=21–26 — 9-GRIBLJE-blokov [27,4,28,8,42,27,41,52,16] (3-POLNA ×2!-h27-×2-bloka-v-1-letu-PRVIČ!) · ★★★★★ h52-FIRSTYEAR-DVIG-1882→1881 (v17-Anna-Petrič-24.-Okt-uz-B-'jasno-5-nad-2'-1:1!-P241-ZA-5-LET→ZA-6-LET!-h52-9→10-blokov!) · ★★★★ PEZDIRC-ženi n-v14-Georg-h42 (črka-za-črko-1:1!-×-Anna-geb.-Hrizom-[~Križan]-h27-POLNI ×2!-continuum-5.-leto!) · ★★★ TAPIČ↔ŠILAR-križ-v23 (starši-neveste-Anna-geb.-TAPIČ!) + BRINC-continuum-v13-Peter-h28 × Katharina-Horvasinič-h8-POLNI ×2! · foliacija-'Pag-=-sken−1'-3/3-s39/s43/s44 (s39-'Pag. 38'-NEDVOUMNO-uz-C!) · duhovnik-Franz-Dovgan-DORGON-variante-+ v23-DUEL-[Dovgan:Jemiar/Janžar!]-[~X-OPEN!]. Dokaz: parish-marriage-1881-04455.json; skripte p242.",
      "P242: THE PARISH OF PODZEMELJ — THE MARRIAGE-REGISTER-PREHISTORY 04455, THE YEAR 1881 = 5/13 (issue #18): s39–s44 (6 spreads == Pag. 38–43; 25 entries of 1881 counted-from-the-number-column-1–11-+-13–26-with-1-SKIP-12!-s41(11)→s42(13)!-[X-OPEN-DUEL: or-s42=12–15-skip-16!]-the-5th-numbering-anomaly-of-the-line-cf.-the-1885-entry-3-P238!) · THE-1881-RESTART = s39-top (the-year-'1881'-in-the-DATE-COLUMN-ABOVE-row-1!-entry-1 = Jan-16!-a-NEW-5th-BOUNDARY-VARIANT-modest!) · the-1880/81-boundary = s38→s39 (the-1880-tail-expected-on-s38-P243!-[X-OPEN!]) · the-1881/82-boundary = s44→s45-heading (the-P241-1:1!-the-1881-tail = entry-26-Dec-20!) · numbering s39=1–4 · s40=5–7 · s41=8–11 · s42=13–16 (the-SKIP-12!) · s43=17–20 · s44=21–26 — 9-GRIBLJE-blocks [27,4,28,8,42,27,41,52,16] (3-FULL ×2!-the-h27-×2-blocks-in-1-year-FOR-THE-FIRST-TIME!) · ★★★★★ the-h52-FIRSTYEAR-RAISE-1882→1881 (the-v17-Anna-Petrič-Oct-24-the-uz-B-'clearly-5-above-2'-1:1!-the-P241-BY-5-YEARS→BY-6-YEARS!-the-h52-9→10-blocks!) · ★★★★ the-PEZDIRC-groom-v14-Georg-h42 (letter-by-letter-1:1!-×-Anna-geb.-Hrizom-[~Križan]-h27-FULL ×2!-the-continuum-5th-year!) · ★★★ the-TAPIČ↔ŠILAR-cross-v23 (the-bride's-parents-Anna-geb.-TAPIČ!) + the-BRINC-continuum-v13-Peter-h28 × Katharina-Horvasinič-h8-FULL ×2! · the-foliation-'Pag-=-sken−1'-3/3-s39/s43/s44 (the-s39-'Pag. 38'-UNAMBIGUOUS-uz-C!) · the-priest-Franz-Dovgan-DORGON-variants-+ the-v23-DUEL-[Dovgan:Jemiar/Janžar!]-[~X-OPEN!]. Evidence: parish-marriage-1881-04455.json; scripts p242.",
      p242Errors.length === 0,
      p242Errors.length === 0
        ? `poročna-1881: 25-vpisov/z-1-PRESKOKOM-12!-5.-številčenjska-anomalija! · 9-Griblje-blokov-[27,4,28,8,42,27,41,52,16]-3-POLNA ×2!-h27-×2-bloka-PRVIČ! · ★★★★★ h52-firstYear-DVIG-1882→1881 (P241-ZA-5-LET→ZA-6-LET!) · ★★★★ PEZDIRC-ženi n-v14-Georg-h42 × Anna-Hrizom-h27 (continuum-5.-leto!) · ★★★ TAPIČ↔ŠILAR-križ-v23! · BRINC-v13-Peter-h28 × Katharina-h8-POLNI ×2! · restart-s39-letnica-v-stolpcu-NOVA-5.-mejna-varianta! · meja-1881/82-P241-IZPOLNJENA-1:1! · foliacija-'Pag-=-sken−1'-3/3! · MILIČ-križ-×237-nespremenjen (nobenega-v-1881!)`
        : p242Errors.join("; "),
    );
  }

  // ——— qa-p241: POROČNA PREDZGOVINA 04455 — leto 1882 = 4/13 (P241) ———'''

src = open(QA, encoding="utf-8").read()
a = "  // ——— qa-p241: POROČNA PREDZGOVINA 04455 — leto 1882 = 4/13 (P241) ———"
assert a in src, "qa-p241-marker-ni-najden!"
src = src.replace(a, qa242, 1)
open(QA, "w", encoding="utf-8").write(src)
print("qa-p242 blok vstavljen")

# ——— 3. pt-luknja-18-final.json — h52 + vsota ———
import json
pt = json.load(open(PT, encoding="utf-8"))
h52 = [x for x in pt["gapHouses"] if x["houseNo"] == "52"][0]
h52["blocksTotal"] = 10
h52["byBook"] = {**h52.get("byBook", {"04455": 2}), "04455": 3}
h52["firstYear"] = 1881
h52.pop("p241Note", None)
h52["p242Note"] = "P242: poročna-1881-v17-Anna-Petrič-GRIBLJE-52-24.-Okt-uz-B-1:1! — h52-firstYear-DVIG-1882→1881-ZA-1-LETO!-P241-ZA-5-LET→ZA-6-LET!-9→10-blokov!"
json.dump(pt, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"pt-luknja: h52-posodobljen (10-blokov/firstYear-1881/byBook-04455=3/p242Note!) · vitalsTotal={pt.get('vitalsTotal')}")
if pt.get("vitalsTotal") != 1966:
    pt["vitalsTotal"] = 1966
    json.dump(pt, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("vitalsTotal 1957→1966 popravljen")
