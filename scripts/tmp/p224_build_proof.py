#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P224 — dokaz parish-baptism-1882-04104.json (krstna PREDZGODOVINA 4/15!)."""
import json, os

TMP = "/tmp/p224"
E = json.load(open(f"{TMP}/entries_1882.json"))

grib = E["griblje_entries"]
okvir = E["okvir"]
st = okvir["stats"]

out = {
 "phase": "P224",
 "title": "Župnija Podzemelj — krstna knjiga 04104 (predzgodovina), polno leto 1882 = 4/15 (issue #18)",
 "type": "parish-baptism-prehistory",
 "status": "DOCUMENTED",
 "issuedAt": "2026-11-07",
 "source": {"book": "04104", "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
            "inventar": 200, "okvir": "s147–s161 (15 skenov; s145–s146-proba! s159–s161-lead-ŽE-VLM-P223!)", "prenos": "2×-neodvisna-md5-17/17"},
 "method": "2×-neodvisna-prenosa-md5 + page-VLM-×17 + krop-51 (zap-15 + pag-6 + meja-2 + mesec-stolpci-3 + Griblje-25!) + krop2-34 (re-krops-7 + hi-zoomi-23 + posebni-4!) + krop3-15 (stripi + re-krops + foliacija-spoj!) + duel-celice-×11-VIZUALNO — triangulacija-page+krop+strip+VIZUALNO",
 "frame": {"scanFrom": 147, "scanTo": 161, "pagKonvencija": "gola-svinčna-'sken−6' (1882-okno-9-vizualnih: s148='142'/s153='147'/s157='151'/s159='153'/s160='154'/s161='155'/s162='156'/s163='157'!) + ★LUKNJA-'158' (skok-s163→s164!) — TRI-serije!", "year": 1882,
           "rowsTotal": 106, "break1881/82": "s147/s148 (finis + Anni-'1 8 8 1.'-razpeta + Jahr-1882-glava + restart-z1-Jän-2!)", "break1882/83": "s161 (P223!)"},
 "okvir": {**okvir, "stats": st},
 "entries": grib,
 "stats": {**st, "griblje_25": "25-GRIBLJE / 23-hiš (h13-×2: z89+z99! h68-×2: z105+z106-DVOJČKI!) = TIE-REKORD-P221 (1885!) — vs-21-P222 + 19-P223!"},
 "anomalije": [{"id": a["id"], "opis": a["opis"], "dokazi": a["dokazi"]} for a in E.get("_anomalije", [])] if E.get("_anomalije") else None,
 "crossLinks": None,
 "honesty": None,
 "nextSteps": [
   "P225-LEAD: krstna-04104, leto 1881 (5/15) — TAIL-1881-ŽE-VLM (s147: z83–z89-Dez-8–21 + finis + Anni-'1 8 8 1.'-razpeta!) → MEJA-1880/81-pred-s147 → probe-s141–s147! (gola-pag-'sken−6'-pričakovana!)"
 ],
}
# anomalije/cross/honesty iz build_entries (priložene kot ločene datoteke)
an_path = f"{TMP}/anomalije_1882.json"
if os.path.exists(an_path):
    out["anomalije"] = json.load(open(an_path))
    out["crossLinks"] = json.load(open(f"{TMP}/cross_1882.json"))
    out["honesty"] = json.load(open(f"{TMP}/honesty_1882.json"))
else:
    out.pop("anomalije"), out.pop("crossLinks"), out.pop("honesty")

os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(out, open("/home/z/my-project/research/issue17/parish-baptism-1882-04104.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: entries={len(out['entries'])} anomalije={len(out.get('anomalije') or [])} cross={len(out.get('crossLinks') or [])} honesty={len(out.get('honesty') or [])}")
