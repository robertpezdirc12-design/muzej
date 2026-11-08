#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P226 — dokaz parish-baptism-1880-04104.json (krstna PREDZGODOVINA 6/15!)."""
import json, os

TMP = "/tmp/p226"
E = json.load(open(f"{TMP}/entries_1880.json"))

grib = E["griblje_entries"]
okvir = E["okvir"]
st = okvir["stats"]

out = {
 "phase": "P226",
 "title": "Župnija Podzemelj — krstna knjiga 04104 (predzgodovina), polno leto 1880 = 6/15 (issue #18)",
 "type": "parish-baptism-prehistory",
 "status": "DOCUMENTED",
 "issuedAt": "2026-11-08",
 "source": {"book": "04104", "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
            "inventar": 200, "okvir": "s119–s135 (17 skenov; s129–s135-proba! s119–s128-probe-nazaj! s135-lead-ŽE-VLM-P225!)", "prenos": "2×-neodvisna-md5-17/17"},
 "method": "2×-neodvisna-prenosa-md5 + page-VLM-×5 (s129–s133) + VIZUALNO-arhivar-branje-×12 (s119–s128, s134, s135!) + krop-86 (zap-16 + pag-17 + meja-3 + mesec-stolpci-10 + Griblje-22 + posebni-13!) — triangulacija-page+VIZUALNO+krop+sandwich-chronologija",
 "frame": {"scanFrom": 119, "scanTo": 135, "pagKonvencija": "gola-svinčna-'sken−6'-17/17-SEKVENČNO (s119='113'/s120='114'/s121='115'/s122='116'/s123='117'/s124='118'/s125='119'/s126='120'/s127='121'/s128='122'/s129='123'-VLM-'129'-misread-9↔3-REŠEN!/s130='124'/s131='125'/s132='126'-VLM-VIZUALNO!/s133='127'-VLM-'124'-misread-4↔7-REŠEN!/s134='128'/s135='129'!) — brez-luknje-v-1880-oknu (SKUPNA-SERIJA-113–158-z-1881/1882/1883-okni!)", "year": 1880,
           "rowsTotal": 122, "break1879/80": "s119/s120 (TAIL-1879-z92–z96 + Schnörkel + 'Jahr 1879'-brez-vsotne + velike-cifre-'1/8/8/0'-P214-TIP + 'Jahr 1880'-glava + restart-z1-Jän-3-Dobravce-h11-Martin!)", "break1880/81": "s135/s136 (P225!)"},
 "okvir": {**okvir, "stats": st},
 "entries": grib,
 "stats": {**st, "griblje_22": "22-GRIBLJE / 20-hiš (h27-×2: z46+z54! + h24-×2: z65+z72! — DUELI-REŠENI-1:1!) — vs-25-TIE-rekord-P221/P224 + 21-P222 + 19-P223 + 17-P225! + PEZDIRC-×14-REKORD-LINJE!"},
 "anomalije": None,
 "crossLinks": None,
 "honesty": None,
 "nextSteps": [
   "P227-LEAD: krstna-04104, leto 1879 (7/15) — 96-vpisov-BONUS-ŽE-ŠTEVJE (s119-tail: z92–z96-Dez-17–30 + Schnörkel + 'Jahr 1879'-brez-vsotne!-incl.-z92-Griblje-h28 + z95-Griblje-h40-PEZDIRC-oče!) → MEJA-1878/79-pred-s119 → probe-s112–s119! (gola-pag-'sken−6'-pričakovana — s112='106'!)"
 ],
}
an_path = f"{TMP}/anomalije_1880.json"
if os.path.exists(an_path):
    out["anomalije"] = json.load(open(an_path))
    out["crossLinks"] = json.load(open(f"{TMP}/cross_1880.json"))
    out["honesty"] = json.load(open(f"{TMP}/honesty_1880.json"))
else:
    out.pop("anomalije"), out.pop("crossLinks"), out.pop("honesty")

os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(out, open("/home/z/my-project/research/issue17/parish-baptism-1880-04104.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: entries={len(out['entries'])} anomalije={len(out.get('anomalije') or [])} cross={len(out.get('crossLinks') or [])} honesty={len(out.get('honesty') or [])}")
