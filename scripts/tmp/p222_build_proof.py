#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P222 — dokaz parish-baptism-1884-04104.json (krstna PREDZGODOVINA 2/15!)."""
import json

TMP = "/tmp/p222"
E = json.load(open(f"{TMP}/entries_1884.json"))

grib = E["griblje_entries"]
okvir = E["okvir"]
st = okvir["stats"]

anomalije = [
 {"id": a["id"], "opis": a["opis"], "dokazi": a["dokazi"]} for a in [
 {"id":"meja-1883-84-s173","opis":"★★★ MEJA-1883/84 = s173 (61.-POTRDITEV-invariante!): z99-TAIL-1883 + VSOTNA-razpete-'1/8/8/4'-P214-TIP + rokopisna-'Jänner'-glava + RESTART-z1-NA-DAN-1.-1.-GRIBLJE-h34[~84-DUEL!] (PARALELA-P221-restart-z1-1885-NA-DAN-1.-1.-GRIBLJE-h21!) — 1883 = 99-vpisov (P223-LEAD!)","dokazi":["s173-page-VLM","s173_zap_hi3","arb_s173_meja-krop"]},
 {"id":"pisar-ostevilcenje-s175","opis":"★★★ PISARJEVA-OŠTEVILČEVSKA-NAPAKA-s175: zap-stolpec-piše-8–14 (3×-neodvisno!) ZA-9-VRSTIC (2-manjka! '8'-RAZPETA!) — VRSTNA-ARITMETIKA-REŠI: 15–23!","dokazi":["s175_zap_hi3-3×","s174_zap_hi3","s176_zap_hi3"]},
 {"id":"pisar-reorientacija-s177","opis":"★★★ PISARJEVA-REORIZENTACIJA-s177: izvirno-61–68 PREČRTANO-×8 → dopisano-31–38 (REVIZIJA-OŠTEVILČENJA!) + seam-z31-DUP-vs-32-X-open","dokazi":["s177_zap_hi","s177_zap_stolpec","s176_zap_hi3"]},
 {"id":"z84-duplikat-s183","opis":"★★★ z84-DUPLIKAT-ANOMALIJA: s182-vrsta8=84 (81-DUP→82→83→84-korekcije!) + s183-vrsta1=84-DUPLIKAT → pisar-2×-84! (zap-hi-2×-ČISTO + X-open-vs-85!) — PARALELA-s182-81-DUP!","dokazi":["s183_zap_hi-2×","s182_zap_hi","s184_zap_hi"]},
 {"id":"s184-prazna-vrstica-revizije","opis":"★★★ s184 = 93–102 + 1-PRAZNA-NEŠTEVILČENA-VRSTICA (med-99-in-100!) + REVIZIJSKE-POŠEVNICE-×10 — page-VLM-MIS-count-9!","dokazi":["s184_zap_hi","s184-page-VLM"]},
 {"id":"s179-top-korekcije","opis":"s179-TOP-KOREKCIJE-×2 (48[prečr]→49 + 51[prečr]→51!)","dokazi":["s179_zap_hi","s179_zap_stolpec"]},
 {"id":"s186-tail-x-precrte","opis":"★★★ TAIL-1884 = z111[prečrtan-X!]-Gradac + z112[prečrtan-X!]-GRIBLJE-h43-Mathias-†28.12.1887 + VSOTNA-'1/8/8/5' + RESTART-z1-1885 = 61.-POTRDITEV-invariante! (pass3-'29/30'-DAN-bleed-MISREAD-dokumentiran!)","dokazi":["s186_zap_stolpec","arb_s186_meja","s186_zap_hi3","P221-paralela"]},
 {"id":"vas-dueli-reseni","opis":"VAS-DUELI-REŠENI-krop-hi: z99-GRIBLJE-JASNO (vs-trak-'Podplanina'-ZAVRNJENA!) + z52-PRILOZJE-IZLOČEN (page-'Griblje'-MISREAD!) + z60-BORŠT-IZLOČEN (re-crop-bleed-dokumentiran!)","dokazi":["z99_s184_vas_hi","z52_s179_vas_hi","z60_s180_vas_hi"]},
 {"id":"krstni-pripisi-kriz-mrlisko-1884","opis":"★★★ POZNEJŠI-PRIPISI = KRIŽ-z-mrliško-04106: z70-'†29/10-1887' + z112-'†28/12-1887' + z19-'gest-3/5-884[?]' + z75-MMK-'1974' + z99-'6.2.1911' + z105-'Mrt/Poroč-1.10.1953'-X-open!","dokazi":["z70-krop","z112-krop","z75-re","z99-page","z105-trak+oc_hi"]},
 {"id":"mreze-1884","opis":"MREŽE: PEZDIRC-×4 (z69-mati + z95-mati+botra + z78-oče-grafija + z84dup-oče!) + KRIŽAN-×3 (z59-oče+botri-×2 + z84-botra + z105-mati!) + BRODARIČ-×5 (z78 + z84 + z84dup + z95 + z105!) + POŽEK-×2 (z61-mati + z65-botra?) + URIH (z61-oče-X-open!) + SIMEC (z51-mati!) + URH (z51-oče!) + MILEK (z105-botra!) + LAZAR (z93-oče!) + DRAGOŠ (z26-mati!) + DEBLIČ-×2 (z69-botra + z78-mati!) + JAKLIČ (z99!)","dokazi":["vsi-row-krops + traki"]},
 ]]

cross_checks = [
 {"tip":"meja-1883/84-re-križ","opis":"s173-VSOTNA + restart-z1 (arb_s173_meja + zap_hi3) — 61.-POTRDITEV-invariante (60.-P221!)","status":"POTRJENO"},
 {"tip":"112-vpisov-invarianta","opis":"vrstna-aritmetika = 112-DISTINCT (1–112!) = P221-'1884-=-112-vpisov'-1:1!","status":"POTRJENO"},
 {"tip":"z112-h43-†28.12.1887","opis":"→ 04106-1887-korpus-X-open (P153!)","status":"X-open-KRIŽ"},
 {"tip":"z70-†29.10.1887","opis":"→ 04106-1887-X-open","status":"X-open-KRIŽ"},
 {"tip":"PEZDIRC-mreža-1884","opis":"×4 → P221-×4-1885-PARALELA!","status":"DOKUMENTIRANO"},
 {"tip":"KRIŽAN-mreža-1884","opis":"×3 (z59-oče+botri + z84-botra + z105-mati!)","status":"DOKUMENTIRANO"},
 {"tip":"BRODARIČ-mreža-1884","opis":"×5!","status":"DOKUMENTIRANO"},
 {"tip":"MILEK-nit","opis":"z105-botra → P220/P218-h65!","status":"DOKUMENTIRANO"},
 {"tip":"LAZAR-nit","opis":"z93-oče → P220-z4-1857!","status":"DOKUMENTIRANO"},
 {"tip":"DRAGOŠ-nit","opis":"z26-mati → P193/P220!","status":"DOKUMENTIRANO"},
 {"tip":"POŽEK-nit","opis":"z61-mati + z65-botra? → P221-z14!","status":"DOKUMENTIRANO"},
]

honesty = [
 "z84dup = honesty-MAX-1884 (ordinal-DUPLIKAT + mesec-DUEL + dan-garble + hiša-DUEL + mati-TRI-garble!)",
 "z1-hiša-DUEL (34-vs-84! — '37'-3-reads-ZAVRNJENE-hi2!)",
 "z26-hiša-TRI-DUEL (33/58/38!) + oče-TRI-garble",
 "z21-mati-TRI-DUEL + oče-TRI-garble",
 "z110-oče-TRI-QUAD-garble (Martincič/Gratzy/Gostofar!)",
 "z65-NEZAKONIT-DUELI (oče + mati!)",
 "z51/z59-mesec-Juni/Juli-DUEL (chrono-rekonstrukcija!)",
 "z75-mesec-DVOJNI-MISREAD + hiša-DUEL (43/13!)",
 "z93-otrok-garble-DUEL",
 "z105-pripis-'Mrt/Poroč-1953'-X-open + oče-garble",
 "z52 + z60-IZLOČENI (vas-krop-hi!)",
 "s175-pisarjeva-napaka (vrstna-aritmetika-REŠI!)",
 "s177-reorizentacija (pisar-sam-popravil!)",
 "z84-DUPLIKAT-X-open-vs-85",
 "s184-prazna-vrstica + revizijske-poševnice-×10",
 "hišna-hi2-'ticks'-geometrija-dokumentirana",
 "krop-zamiki-pass1-dokumentirani (×5!)",
 "matec/botra-garble-[~] — brez-fabriciranja",
]

out = {
 "phase": "P222",
 "title": "Župnija Podzemelj — krstna knjiga 04104 (predzgodovina), polno leto 1884 = 2/15 (issue #18)",
 "type": "parish-baptism-prehistory",
 "status": "DOCUMENTED",
 "issuedAt": "2026-11-07",
 "source": {"book": "04104", "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
            "inventar": 200, "okvir": "s173–s186 (14 skenov; s170–s172 + s186-proba!)", "prenos": "2×-neodvisna-md5-17/17"},
 "method": "2×-neodvisna-prenosa-md5 + page-VLM-×17 + traki-56 + krop-43 + krop2-21 (hi-zoom!) + krop3-13 (zadnje-forenzike!) — triangulacija-page+trak+krop",
 "frame": {"scanFrom": 173, "scanTo": 186, "pagKonvencija": "sken+13 = folio-svinčnik (re-potrjeno-×3: s177='190'/s181='194'/s185='198'!)", "year": 1884,
           "rowsTotal": 112, "break1883/84": "s173 (VSOTNA + restart-z1!)", "break1884/85": "s186 (P221!)"},
 "okvir": {**okvir, "stats": st},
 "entries": grib,
 "stats": {**st, "griblje_21": "21-GRIBLJE / 20-hiš (h13-×2!) — vs-25-P221-1885 (rekord-ostaja!)"},
 "anomalije": anomalije,
 "crossLinks": cross_checks,
 "honesty": honesty,
 "nextSteps": [
   "P223-LEAD: krstna-04104, leto 1883 (3/15) — s171–s172-ŽE-proba (z83–z98: Griblje-×3-tail: z88-h25[?]-Katharina + z94-h11-Nikolaus + z96-h63-Ana + z97-h29-Barbara!) + z99-tail-s173-ŽE-VLM → MEJA-1882/83-pred-s171 → probe-s164–s171!"
 ],
}
import os
os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(out, open("/home/z/my-project/research/issue17/parish-baptism-1884-04104.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: entries={len(out['entries'])} anomalije={len(anomalije)} cross={len(cross_checks)} honesty={len(honesty)}")
