#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P243 — sanacija zastarelih agregatov: 1966→1969 · 223→226 · sidra 216→219 (1880:3!) · dobe 190→193 (23/31-pred-linijskih!) + p85-izjeme-h24/h63/h53-1880 + qa-p243 vstavitev."""
import re, sys

ROOT = "/home/z/my-project"
QA = f"{ROOT}/src/lib/qa-parish.ts"
delo = 0

src = open(QA, encoding="utf-8").read()
orig = src

def rep(a, b, label=""):
    global src, delo
    n = src.count(a)
    src = src.replace(a, b)
    delo += n
    print(f"  [{n}] {a[:56]} → {b[:56]} {label}")

# ——— 1. HOUSE_VITALS 1966→1969 (152 gard + sporočila) ———
rep("HOUSE_VITALS.length !== 1966", "HOUSE_VITALS.length !== 1969")
rep("HOUSE_VITALS ≠ 1966", "HOUSE_VITALS ≠ 1969")

# ——— 2. bloki-04455 223→226 ———
rep("p80Marr.length !== 223", "p80Marr.length !== 226")
rep("p115Marr.length !== 223", "p115Marr.length !== 226")
rep("p116Marr.length !== 223", "p116Marr.length !== 226")
rep('HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 223', 'HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length !== 226')
rep("p152Blocks.length !== 223", "p152Blocks.length !== 226")
rep("bloki 04455 ≠ 223", "bloki 04455 ≠ 226")
rep("bloki-04455 ≠ 223", "bloki-04455 ≠ 226")
rep("poročni vpisi (04455) ≠ 223", "poročni vpisi (04455) ≠ 226")

# ——— 3. sidra 216→219 + 1880:3 gardo ———
rep("p80MarrAnchors.length !== 216", "p80MarrAnchors.length !== 219")
rep("poročna sidra ≠ 216 (1881:9-P242!", "poročna sidra ≠ 219 (1880:3-P243! · 1881:9-P242!")
rep("poročna sidra ≠ 216 (${p80MarrAnchors.length} — 207 + 9-novih-1881-P242!)", "poročna sidra ≠ 219 (${p80MarrAnchors.length} — 216 + 3-novih-1880-P243!)")
a = "  p80MarrAnchors.filter((h) => h.year === 1881).length !== 9 ||"
b = "  p80MarrAnchors.filter((h) => h.year === 1880).length !== 3 ||\n" + a
if a in src and "year === 1880" not in src.split(a)[0][-300:]:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +1880:3-letni-gard")

# ——— 4. sken-range garda 1880 (s35–s38) ———
a = 'if (p80MarrAnchors.some((h) => h.year === 1882 && ((h.scan ?? 0) < 45 || (h.scan ?? 0) > 50)))'
b = ('if (p80MarrAnchors.some((h) => h.year === 1880 && ((h.scan ?? 0) < 35 || (h.scan ?? 0) > 38)))\n'
     '  p80Errors.push(`poročna sidra 1880: skeni izven 35–38 (P243: s35–s38!-najdeno: ${p80MarrAnchors.filter((h) => h.year === 1880).map((h) => h.scan).join(",")})`);\n' + a)
if a in src and "skeni izven 35–38" not in src:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +sken-range-garda-1880-s35–s38")

# ——— 5. dobe 190→193 + pred-linijskih 20→23 / 28→31 ———
rep("p152Pre !== 190 || p152Wwi !== 7 || p152Boom !== 26", "p152Pre !== 193 || p152Wwi !== 7 || p152Boom !== 26")
rep("dobe-bloki ≠ 190/7/26", "dobe-bloki ≠ 193/7/26")
rep("predvojna ≤1913 = 190 blokov", "predvojna ≤1913 = 193 blokov")
rep("20 pred-linijskih 1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!", "23 pred-linijskih 1880-P243×3!+1881-P242×9!+1882-P241×7!+1883-P240×2+1884-P239+1885!")
rep("28 pred-linijskih (1881×9-P242!+1882×7-P241!+1883×2+1884×3+1885×7)", "31 pred-linijskih (1880×3-P243!+1881×9-P242!+1882×7-P241!+1883×2+1884×3+1885×7)")

# ——— 6. p85-izjeme-04455-1880-h24/h63/h53 (bloki-pred-prvencem!) ———
# 6a. skupina-hiš-1890 (h7/h30/h38/h41/h77/h90): ni h24/h63/h53 — preskoči
# 6b. h28/h53-skupina (izjeme-04455-1890/1913/1921-h53!): + 1880-h53
a = '!(v.bookSignature === "04455" && v.year === 1890 && hn === "53")'
b = '!(v.bookSignature === "04455" && v.year === 1880 && hn === "53") && ' + a
if a in src and "v.year === 1880 && hn === \"53\"" not in src:
    src = src.replace(a, b, 1); delo += 1; print("  [1] +izjema-04455-1880-h53 (h28/h53-skupina)")
# 6c. h63-skupina? najdi izjemo-04455-1911-h63 (P140)
n = src.count('!(v.bookSignature === "04455" && v.year === 1911 && hn === "63")')
if n:
    a = '!(v.bookSignature === "04455" && v.year === 1911 && hn === "63")'
    b = '!(v.bookSignature === "04455" && v.year === 1880 && hn === "63") && ' + a
    src = src.replace(a, b, 1); delo += 1; print(f"  [{n}] +izjema-04455-1880-h63")
# 6d. h24-skupina? najdi izjemo-04455-1896-h24 (P125)
n = src.count('v.bookSignature === "04455" && v.year === 1896 && hn === "24"')
if n:
    a = 'v.bookSignature === "04455" && v.year === 1896 && hn === "24"'
    b = 'v.bookSignature === "04455" && (v.year === 1896 || v.year === 1880) && hn === "24"'
    src = src.replace(a, b, 1); delo += 1; print(f"  [{n}] +izjema-04455-1880-h24 (ob 1896)")

# ——— 7. qa-p243 vstavitev (pred qa-p242 blok) ———
P243_QA = '''
// ——— qa-p243: poročna predzgodovina 04455 — leto 1880 = 6/13 (P243, 243. kontrola) ———
// vir: s35–s38 (Matricula hosted-images; restart-1880 = s35-DNO NOVA-7.-MEJNA-VARIANTA!; finis-s38!)
// meri ŽIVO iz korpusa (HOUSE_VITALS 1:1) — neodvisno od parish-marriage-early modula!
{
  const p243Blocks = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1880);
  const p243Errors: string[] = [];
  if (p243Blocks.length !== 3)
    p243Errors.push(`Griblje poroke 1880 ≠ 3 (${p243Blocks.length} — P243: h24-BRINE-s36 + h63-KRIŽAN×Pegdirec-s37 + h53-PERDIRC-[~Pegdirc!]-TAIL-s38!)`);
  const p243Houses = p243Blocks.map((h) => h.houseNo).join(",");
  if (p243Houses !== "24,63,53")
    p243Errors.push(`hiše-1880 ≠ [24,63,53] (najdeno: ${p243Houses} — vrstni-red-blokov-vrstica!)`);
  const p243Scans = p243Blocks.map((h) => h.scan).join(",");
  if (p243Scans !== "36,37,38")
    p243Errors.push(`skeni-1880 ≠ [36,37,38] (najdeno: ${p243Scans} — s36-vpis-4 · s37-vpis-14 · s38-vpis-20-TAIL!)`);
  if (p243Blocks.some((h) => (h.page ?? 0) !== (h.scan ?? 0) - 1))
    p243Errors.push("Pag==sken−1-pag-1880 (s36→35 · s37→36 · s38→37!-s38-'Pag. 34'-branje-[~X-OPEN-DUEL-ostaja-v-foliaciji!])");
  if (p243Blocks.every((h) => h.status !== "DOCUMENTED"))
    p243Errors.push("status-1880-bloki");
  if (p243Errors.length)
    qa.push({ id: "qa-p243-parish-marriage-early-04455-1880", ok: false, detail: `P243 poročna-predzgodovina-1880: ${p243Errors.join(" · ")}` });
  else
    qa.push({ id: "qa-p243-parish-marriage-early-04455-1880", ok: true, detail: `P243 poročna-predzgodovina-1880 ŽIVO: 20 vpisov (s35-dno-restart-1–2 + s36-3–8 + s37-9–14 + s38-15–20-tail-BREZ-preskokov!) · 3 Griblje bloka [24,63,53] (h24-BRINE-1:1! · h63-KRIŽAN-continuum-cf.-mrliška-1884! · h53-PERDIRC-[~Pegdirc!]-TAIL-+ Gaveldzettel-margine!) · RESTART-1880 = s35-DNO (31-32-33→1-2!-NOVA-7.-MEJNA-VARIANTA + letnica-v-datumskem-stolpcu-vrste-3-s36!) · MEJA-1880/81 = s38→s39 (finis/s-1880! + s39-top-'1881'-P242-2×-1:1!) · h53-firstYear-1890→1880-DVIG-ZA-10-LET! · PEZDIRC-continuum-×3-reads · GRIBLJAN-izvor-×2 · Dovgan/Dovžan-continuum-6-let! · FOLIACIJA-s38-'Pag. 34'-[~X-OPEN-DUEL-vs-37!]` });
}
'''
anchor = "// ——— qa-p242: poročna predzgodovina 04455 — leto 1881 = 5/13"
if anchor in src and "qa-p243-parish-marriage-early-04455-1880" not in src:
    src = src.replace(anchor, P243_QA + anchor, 1)
    delo += 1
    print("  [1] +qa-p243-blok-vstavljen")

open(QA, "w", encoding="utf-8").write(src)
print(f"qa-parish.ts: {delo} zamenjav")

# ——— 8. pt-luknja-18-final.json ———
import json
PT = f"{ROOT}/research/issue17/pt-luknja-18-final.json"
pt = json.load(open(PT, encoding="utf-8"))
pt["vitalsTotal"] = 1969
pt["corpus"]["vitalsTotal"] = 1969
pt["corpus"]["byBook"]["04455"] = 226
for h in pt.get("gapHouses", []):
    if h.get("houseNo") == "53":
        h["blocksTotal"] = h.get("blocksTotal", 21) + 1
        if "byBook" in h and "04455" in h["byBook"]:
            h["byBook"]["04455"] = h["byBook"]["04455"] + 1
        h["firstYear"] = 1880
        h["p243Note"] = "P243: poročna-04455-1880-vpis-20-TAIL-Peter-PERDIRC-[~Pegdirc-DUEL!]-GRIBLJE-53 (s38!) — h53-firstYear-04455-1890→1880-DVIG-ZA-10-LET + margine-'Gaveldzettel-der-Gemeinde-Griblje-vom-21.-November-1880'-očetova-privolitev! (cf.-04105-h53-firstYear-1887 — poročna-OUTRUNA-ZA-7-LET!)"
json.dump(pt, open(PT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("pt-luknja: vitalsTotal=1969 · 04455=226 · h53-posodobljen (firstYear-1880 + p243Note!)")
