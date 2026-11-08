#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P223 — dokaz parish-baptism-1883-04104.json (krstna PREDZGODOVINA 3/15!)."""
import json, os

TMP = "/tmp/p223"
E = json.load(open(f"{TMP}/entries_1883.json"))

grib = E["griblje_entries"]
okvir = E["okvir"]
st = okvir["stats"]

anomalije = [
 {"id": a["id"], "opis": a["opis"], "dokazi": a["dokazi"]} for a in [
 {"id":"meja-1882-83-s161","opis":"★★★ MEJA-1882/83 = s161 (62.-POTRDITEV-invariante!): TAIL-1882-z104–z106 (Dezember-31-×3! + z105+z106 = DVOJČKI-GRIBLJE-h68-ZWILLINGE-bracket! — P224-LEAD!) + 'Initium-annos-Domini' + VSOTNA-razpeta-'1 8 8 3.' + RESTART-z1-NA-DAN-4.-1.-JÄNNER-Gradac!","dokazi":["s161-page-VLM","s161_zap_stolpec","arb_s161_meja","s161-mesec-hi"]},
 {"id":"mesec-carry-over-vzorec","opis":"★★★ MESEC-CARRY-OVER-VZOREC (NOVO!): labela-samo-na-prvi-vrstici-bloka (z1-'Jänner' + z2–z6-PRAZNI — page-'Feber'-sklepanje-ZAVRNJENO!) — 12-mesečnih-blokov-popolna-kronologija (Jän-z1–z9 4–31 · Feb-z10–z19 1–28-neprestupno! · Mär-z20–z30 · Apr-z31–z40 · Mai-z41–z48 · Jun-z49–z56 · Jul-z57–z63 · Aug-z64–z70 · Sep-z71–z74 · Okt-z75–z87 · Nov-z88–z91 · Dez-z92–z99!)","dokazi":["s161-mesec-hi","s162/s163-dnevi","chrono-aritmetika"]},
 {"id":"marz-label-misread-korekcija","opis":"★★★ MÄRZ-LABEL-MISREAD-KOREKCIJA: z24-'Mai'-page → hi-VIZUALNO-'März' — April-sandwich-anomalija-RAZREŠENA! z25/z28-GRIBLJE-MÄRZ!","dokazi":["z24_s164_label_hi","s164-mesec-col","s166_mesec_col"]},
 {"id":"dvojni-foliacijski-seriji","opis":"★★★ DVOJNI-FOLIACIJSKI-SERIJI (NOVO-ODKRITJE!): gola-svinčna-'sken−5' (1883-okno: s165='160'/s169='164'/s173='168'! s161='155[~156?]') VS-'Pag.'-natisnjena-'sken+13' (1884-okno: s177='190'/s181='194'/s185='198'-re-potrjeno!) — menjava-tiskane-forme-okoli-s174/175 + P222-'s173=186'-KOREKCIJA ('168'-6/8-transpozicija!)","dokazi":["arb_s165/s169/s173_pag + hi","recheck_s177/s181/s185_pag"]},
 {"id":"z99-tail-izlocen","opis":"★★★ z99-TAIL-1883-IZLOČEN: vas-hi-'Obrijuh.'-hisna-'17.' — NI-Griblje! (P222-'OBržuh/Obrije[?]'-potrjeno!)","dokazi":["z99_s173_vas_hi"]},
 {"id":"hisni-dueli-reseni","opis":"HIŠNI-DUELI-REŠENI (5): z43-'42'-preliv-iz-'1942'-ZAVRNJEN (17!) + z59-'1965'-KOREKCIJA ('Mrt.-1985'!) + z61-'70'-ZAVRNJENO (90!) + z76-'51'-KOREKCIJA (56!) + z78-'sy'-ZAVRNJEN (37!) + z96-'18'-ZAVRNJENA (63!) + h25-×2 (18-hiš!)","dokazi":["hi2/hi3-vizualni-kropi"]},
 {"id":"pripisi-kriz-mmk-1883","opis":"★★★ POZNEJŠI-PRIPISI-MMK-ERA (8-GRIBLJE!): z5-'umrla-18.12.1962' + z22-'umrla-6.1.1940-90-let' + z32-'umrla-18.[?].1957'-KOREKCIJA + z43-'poročen-3/2.1919'+'H-30.8.1942' + z52-'umrl-2.9.1965[X]' + z58-'umrla-8.10.[1959/1960]' + z59-'Mrt.-10.7.1985-št.57'-KOREKCIJA + z94-'Cop.-1910-Pilteburg[?]'-X-open!","dokazi":["8-pripisnih-kropov"]},
 {"id":"mreze-1883","opis":"MREŽE: PEZDIRC-grafija-×6 (z7+z32+z52-×2+z76+z96-×2!) + BRODARIČ-×4 + DRAGOŠ-×2 + SIMEC-×3 + KRIŽAN-×2 + STRUCELJ-×2 + LESKO-×3 + MIHELČ-MILEK-×2 + HLEBEC + KLOBUČAR + ZUPANIČ-×2 + Kure-×2!","dokazi":["krops + hi + page"]},
 ]]

cross_checks = [
 {"tip":"meja-1882/83-re-križ","opis":"s161-VSOTNA-'1 8 8 3.'-+ restart-z1 (arb_s161_meja + zap_stolpec + mesec-hi!) — 62.-POTRDITEV-invariante (61.-P222!)","status":"POTRJENO"},
 {"tip":"99-vpisov-invarianta","opis":"vrstna-aritmetika-13-skenov = 99-DISTINCT (z1–z99!) = P222-LEAD-1:1!","status":"POTRJENO"},
 {"tip":"dvojcki-griblje-h68-1882","opis":"z105/z106-'Zwillinge'-bracket-TAIL-1882 → P224-LEAD (1882 = 4/15!) — PARALELA-P219/P221-DVOJČKI!","status":"P224-LEAD"},
 {"tip":"PEZDIRC-grafija-×6","opis":"z7-oče + z32-mati + z52-oče+mati + z76-botra + z96-mati+botra → P221/P222-×4-PARALELE!","status":"DOKUMENTIRANO"},
 {"tip":"DRAGOŠ-×2","opis":"z25-botra + z94-mati → P193/P220/z26-1884!","status":"DOKUMENTIRANO"},
 {"tip":"SIMEC-×3","opis":"z22-oče + z17-botra + z43-botra → P221-SIMIC-×2!","status":"DOKUMENTIRANO"},
 {"tip":"BRODARIČ-×4","opis":"z7 + z22 + z28-botre → P222-×5!","status":"DOKUMENTIRANO"},
 {"tip":"MILEK-MIHELČ-×2","opis":"z59 + z88-botri → P218/P220-h65!","status":"DOKUMENTIRANO"},
 {"tip":"KRIŽAN-×2","opis":"z97-mati+botra → P222-mreza!","status":"DOKUMENTIRANO"},
 {"tip":"pag-dvojni-seriji","opis":"→ P224-LEAD (1882-okno = gola-serija!) + P222-GLAVA-korekcijska-opomba","status":"NOVO-DOKUMENTIRANO"},
]

honesty = [
 "z76-ime-TRI-garble + oče-garble-DUEL (Dorher/Baraga!)",
 "z61-garble-gostota (×4-garbles!)",
 "z28-hisna-'35'-X-open + oče-garble (Ostirc/Stepec!)",
 "z52-hisna-'55-vs-65'-DUEL + pripis-dodelitev-X-open",
 "z5-matec-garble-DUEL (Mihelovic/Hublvar!)",
 "z59-oče-DUEL (Brinc/Bovha!)",
 "z17-pripis-garble-X-open",
 "z58-pripis-garble-X-open ([1959/1960]!)",
 "z94-oče-garble (Hugel/Šumec/Hunic!)",
 "s161-pag-'155-vs-156'-X-open",
 "z99-'Obrijuh'-vas-X-open (IZLOČEN!)",
 "mesec-carry-over-page-sklepanja-KOREKCIJE (z5/z7/z25/z28!)",
 "pag-hi-geo-zamiki-dokumentirani (s161/s163/s169/s171!)",
 "matec/botra-[~]-garble — brez-fabriciranja",
 "z43-'42'-preliv-artefakt-dokumentiran",
]

out = {
 "phase": "P223",
 "title": "Župnija Podzemelj — krstna knjiga 04104 (predzgodovina), polno leto 1883 = 3/15 (issue #18)",
 "type": "parish-baptism-prehistory",
 "status": "DOCUMENTED",
 "issuedAt": "2026-11-07",
 "source": {"book": "04104", "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
            "inventar": 200, "okvir": "s161–s173 (13 skenov; s159–s160-proba! s164–s173-lead!)", "prenos": "2×-neodvisna-md5-15/15"},
 "method": "2×-neodvisna-prenosa-md5 + page-VLM-×15 + krop-40 (zap-15 + pag-4 + meja-1 + Griblje-20!) + krop2-hi-×20 + hi3-re-krops-×6 + VIZUALNE-verifikacije-×12 — triangulacija-page+krop+hi+VIZUALNO",
 "frame": {"scanFrom": 161, "scanTo": 173, "pagKonvencija": "gola-svinčna-'sken−5' (s165='160'/s169='164'/s173='168'-VIZUALNO!) — DVOJNI-SERIJI-odkritje!", "year": 1883,
           "rowsTotal": 99, "break1882/83": "s161 (VSOTNA + restart-z1!)", "break1883/84": "s173 (P222!)"},
 "okvir": {**okvir, "stats": st},
 "entries": grib,
 "stats": {**st, "griblje_19": "19-GRIBLJE / 18-hiš (h25-×2: z32+z88!) — vs-21-P222 (rekord-25-P221-ostaja!)"},
 "anomalije": anomalije,
 "crossLinks": cross_checks,
 "honesty": honesty,
 "nextSteps": [
   "P224-LEAD: krstna-04104, leto 1882 (4/15) — TAIL-ŽE-VLM (s159–s161: z88–z106 + DVOJČKI-GRIBLJE-h68-ZWILLINGE-z105/z106!) → MEJA-1881/82-pred-s159 → probe-s153–s159! (gola-pag-serija-'sken−5'-pričakovana!)"
 ],
}
os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(out, open("/home/z/my-project/research/issue17/parish-baptism-1883-04104.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: entries={len(out['entries'])} anomalije={len(anomalije)} cross={len(cross_checks)} honesty={len(honesty)}")
