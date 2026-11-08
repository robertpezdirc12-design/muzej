#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P225 — dokaz parish-baptism-1881-04104.json (krstna PREDZGODOVINA 5/15!)."""
import json, os

TMP = "/tmp/p224"
E = json.load(open(f"{TMP}/entries_1881.json"))

grib = E["griblje_entries"]
okvir = E["okvir"]
st = okvir["stats"]

out = {
 "phase": "P225",
 "title": "Župnija Podzemelj — krstna knjiga 04104 (predzgodovina), polno leto 1881 = 5/15 (issue #18)",
 "type": "parish-baptism-prehistory",
 "status": "DOCUMENTED",
 "issuedAt": "2026-11-07",
 "source": {"book": "04104", "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
            "inventar": 200, "okvir": "s135–s147 (13 skenov; s138–s144-proba! s145–s147-lead-ŽE-VLM-P224! s134–s137-probe-nazaj!)", "prenos": "2×-neodvisna-md5-14/14"},
 "method": "2×-neodvisna-prenosa-md5 + page-VLM-×11 (s134–s144-novi + s145–s147-lead!) + krop-47 (zap-12 + pag-13 + meja-2 + mesec-stolpci-3 + Griblje-17!) + krop2-13 (wide-re-krops-6 + foliacija-5 + glava/finis-2!) + krop3-4 + krop4/5-8 (hi-dueli!) — triangulacija-page+krop+VIZUALNO+sandwich-invarianta",
 "frame": {"scanFrom": 135, "scanTo": 147, "pagKonvencija": "gola-svinčna-'sken−6'-13/13-SEKVENČNO (s135='129'/s136='130'/s137='131'/s138='132'/s139='133'/s140='134'/s141='135'/s142='136'/s143='137'-sandwich!/s144='138'/s145='139'-sandwich!/s146='140'/s147='141'!) — brez-luknje-v-1881-oknu (LUKNJA-'158'-ostaja-v-1882-oknu-s163/s164!)", "year": 1881,
           "rowsTotal": 89, "break1880/81": "s135/s136 (Finis + 'Jahr 18 80.'-brez-vsotne + 'Jahr 1881.'-glava + restart-z1-Jän-1-GRIBLJE-h55-Agnes!)", "break1881/82": "s147/s148 (P224!)"},
 "okvir": {**okvir, "stats": st},
 "entries": grib,
 "stats": {**st, "griblje_17": "17-GRIBLJE / 17-hiš-VSE-DISTINCT (brez-duplikatov!) — vs-25-TIE-rekord-P221/P224 + 21-P222 + 19-P223! + PEZDIRC-×9-rekord-leta!"},
 "anomalije": None,
 "crossLinks": None,
 "honesty": None,
 "nextSteps": [
   "P226-LEAD: krstna-04104, leto 1880 (6/15) — TAIL-1880-ŽE-VLM (s135: z116–z122-Dez-5–30 + Finis + 'Jahr 18 80.'-brez-vsotne!) → 1880 = 122-vpisov → MEJA-1879/80-pred-s135 → probe-s129–s135! (gola-pag-'sken−6'-pričakovana — s129='123'!)"
 ],
}
an_path = f"{TMP}/anomalije_1881.json"
if os.path.exists(an_path):
    out["anomalije"] = json.load(open(an_path))
    out["crossLinks"] = json.load(open(f"{TMP}/cross_1881.json"))
    out["honesty"] = json.load(open(f"{TMP}/honesty_1881.json"))
else:
    out.pop("anomalije"), out.pop("crossLinks"), out.pop("honesty")

os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(out, open("/home/z/my-project/research/issue17/parish-baptism-1881-04104.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: entries={len(out['entries'])} anomalije={len(out.get('anomalije') or [])} cross={len(out.get('crossLinks') or [])} honesty={len(out.get('honesty') or [])}")
