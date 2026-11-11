#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P230 — verifikator KRSTNE PREDZGODOVINE 04104, leto 1876 = 10/15 (I1–I10 + --live)."""
import json, re, sys, urllib.request

ROOT = "/home/z/my-project"
results, ok = [], True

def check(ime, cond, detail=""):
    global ok
    results.append((ime, cond, detail))
    if not cond: ok = False
    print(f"[{'PASS' if cond else 'FAIL'}] {ime}" + (f" — {detail}" if detail else ""))

src = open(f"{ROOT}/src/data/atlas/parish.ts", encoding="utf-8").read()
bloki = re.findall(r'houseNo: "([^"]+)",\s*bookSignature: "04104",\s*year: 1876,', src)
check("I1 bloki 04104/1876-numeric == 14", len(bloki) == 14, f"najdeno {len(bloki)}")
pri = ["40", "39", "20", "16", "7", "15", "22", "53", "62", "25", "8", "55", "44", "31"]
check("I2 hiše-1876 (file-order, 14/14-DISTINCT-BREZ-DUPLIKATOV!)", bloki == pri and len(set(bloki)) == 14, ",".join(bloki) if bloki else "-")
skupaj = src.count('bookSignature: "04104"')
check("I3 vitals-1940 + 04104==288", "HOUSE_VITALS.length !== 1889" not in src and skupaj == 288, f"04104={skupaj}")

d = json.load(open(f"{ROOT}/research/issue17/parish-baptism-1876-04104.json", encoding="utf-8"))
grib = [e for e in d["entries"] if "grib" in str(e.get("vas", "")).lower()]
an = json.dumps(d["anomalije"], ensure_ascii=False)
check("I4 dokaz (14-griblje + MEJA-s64/s65-DVO-STRANSKA-69.-POTRDITEV + 100-DISTINCT + finis-KALLIGRAFIJA + pag-sken−5-15/15)",
      len(grib) == 14
      and "s64/s65-DVO-STRANSKA" in json.dumps(d["okvir"], ensure_ascii=False) and "69.-POTRDITEV" in an
      and "meja-1875-76-s64-s65-dvo-stranska" in an
      and "vpisov-100" in an
      and "foliacija-sken-5-15-15" in an
      and d["frame"]["rowsTotal"] == 100 and d["stats"]["griblje_vpisov"] == 14
      and "15/15-SEKVENČNO" in d["frame"]["pagKonvencija"] and "59–73" in d["frame"]["pagKonvencija"],
      f"entries={len(d['entries'])} griblje={len(grib)} anomalije={len(d['anomalije'])}")
check("I4b novosti (wolfgr-druzina-x3 + nezakonski-x6 + dvojcki-x4-novi-varianti + als-amtsvormund + zap-94-modra + retro-vpisi-x2 + duhovniki-7-7)",
      "wolfgr-anomalija-druzina-x3" in an and "nezakonski-x6-rekord" in an
      and "dvojcki-x4-novi-varianti" in an and "als-amtsvormund-betra-nota" in an
      and "zap-94-modra" in an and "retro-vpisi-x2" in an
      and "duhovniki-7-7-izenačen" in an)

qa = open(f"{ROOT}/src/lib/qa-parish.ts", encoding="utf-8").read()
st = qa.count("HOUSE_VITALS.length !== 2059")
check("I5 qa-p230 + števec-1940", "qa-p230-parish-baptism-1876-04104" in qa and st >= 142, f"1940-številcev={st}")

i0 = src.find("P230: krstna PREDZGODOVINA 04104, leto 1876")
seg = src[i0:] if i0 >= 0 else ""
check("I6a 100-DISTINCT + vrstna-aritmetika + zap-1:1-×6 + zap-94-MODRA", "100-VPISOV-DISTINCT" in seg and "vrstna-aritmetika" in seg and "7+7+7+8+9+8+8+7+8+8+7+7+8+1 = 100" in seg and "zap-stolpci-VIDNI-×6-strani-1:1" in seg and "zap-'94'-MODRA" in seg)
check("I6b FOLIACIJA-sken−5-15/15 + 3×-NARISE + SKUPNA-SERIJA-59–158", "15/15-SEKVENČNO" in seg and "3×-VIZUALNO-NARISE" in seg and "59–158" in seg)
check("I6c MEJA-s64/s65-DVO-STRANSKA + FINIS-ANNI-1875 + RESTART-z1-5./5.-JÄNNER + BREZ-INCIPIT + 69.-POTRDITEV", "MEJA-1875/76-s64/s65-DVO-STRANSKA" in seg and "finis-Anni-1875" in seg and "RESTART-z1-NA-DAN-5./5.-JÄNNER" in seg and "BREZ-INCIPIT" in seg and "69.-POTRDITEV-invariante" in seg and "10.-restart-z1" in seg)
check("I7a 14-GRIBLJE / 14-hiš-BREZ-DUPLIKATOV", "14-GRIBLJE / 14-hiš-BREZ-DUPLIKATOV" in seg and "h53" in seg and "h55" in seg and "h62" in seg and "h44" in seg and "h31" in seg)
check("I7b PEZDIRC-×18-REKORD + continuum-10-let + JAKOFČIČ-×8 + MILEK-×5 + BRODARIČ-×7", "PEZDIRC-×17-vrstic-TIE-REKORD-P228-continuum-10-let" in seg and "×4/×4/×6/×4/×9/×14/×12/×17/×11/×17" in seg and "JAKOFČIČ-×8" in seg and "MILEK-×5" in seg and "BRODARIČ-×7" in seg)
check("I7c DVOJČKI-×4-NOVI-VARIANTI + WOLFGR-DRUŽINA-×3 + NEZAKONSKI-×6", "DVOJČKI-×4-dogodki-REKORD-NOVI-VARIANTI" in seg and "2-SHARED-ROW" in seg and "zap-38-ISTI" in seg and "WOLFGR-ANOMALIJA-DRUŽINA-×3-NOVA" in seg and "'Wolfgrabiff[?]'" in seg and "NEZAKONSKI-×6-REKORD" in seg)
check("I7d als-Amtsvormund + RETRO-×2 + zap-94-MODRA + HEBAMME-×9", "'als-Amtsvormund'-botra-NOTA-NOVI-TIP" in seg and "RETRO-VPISI-×2" in seg and "zap-'94'-MODRA" in seg and "HEBAMME-Maria-Rom-×9" in seg)
check("I7e MODRI-×11-REKORD + CHICAGO + MMK + DUHOVNIKI-7/7 + HEBAMME", "MODRI-×11-linij-REKORD" in seg and "CHICAGO-1970" in seg and "MMK-Metlika-1962" in seg and "MMK-Novo-mesto-1963" in seg and "Griblje-split-7/7-POPOLNOM-IZENAČEN" in seg)
check("I8a meseci-Griblje (Jänner/Feber/Juni-×0!) + 1875-LEAD", "Jänner/Feber/Juni-×0" in seg and "M1+A2+Mai1+Juli2+A[?]1+S3+O1+N2+D1" in seg and "P231-LEAD" in qa and "1875" in qa)
check("I8b TAIL-1876-s78-r1 + zap-100-X-open", "TAIL-1876-s78-r1" in seg or "s78-r1-zap-'100'-X-open" in seg)
check("I9a qa-p230 (230. kontrola!)", "qa-p230" in qa and "230. kontrola" in qa)
pt = open(f"{ROOT}/research/issue17/pt-luknja-18-final.json", encoding="utf-8").read()
check("I9b pt-luknja-271/2043 + byBook-04104", '"vitalsTotal": 2059' in pt and '"04104": 288' in pt)

live = "--live" in sys.argv
if live or "--check" not in sys.argv:
    try:
        req = urllib.request.Request("https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            check("I10 LIVE matricula-04104 HTTP 200", r.status == 200, f"status={r.status}")
    except Exception as e:
        check("I10 LIVE matricula-04104", False, str(e)[:80])

print(f"\n{'VSI PASS' if ok else 'NEUSPEH!'} ({sum(1 for _, c, _ in results if c)}/{len(results)})")
sys.exit(0 if ok else 1)
