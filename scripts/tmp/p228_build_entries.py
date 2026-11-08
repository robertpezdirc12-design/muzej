#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P228 — agregacija 16-GRIBLJE-vpisov leta 1878 (krstna PREDZGODOVINA 04104, 8/15!).
MEJA-1877/78 = s92/s93 (TAIL-1877-Dezember + glava-'Jahr 1877'-BREZ-VSOTNE/velikih-cifer-P225-TIP!
  + RESTART-z1-NA-DAN-[8↔9]-JÄNNER-Boginja-vas-h14-Margareth-TAUFE-DUEL-mesec-prečrtan!)
  = 67.-POTRDITEV-invariante (66.-P227!).
Ordinalna linija: z1–z94 (94-DISTINCT! vrstna-aritmetika 7+6+7+7+6+8+8+7+8+8+7+10+5 = 94 = P227-LEAD-'1878-=-94'-1:1!).
★★★ 16-GRIBLJE / 14-hiš (h11-×2: z28+z29! + h6y-×2: z46+z81!-identični-glifyi-64/69-DUEL-X-open!)
  — ★★★ PEZDIRC-×17-vrstic-REKORD (z46-DVOJNI! z81-DVOJNI!-grafija-continuum-8-let: ×4/×4/×6/×4/×9/×14/×12/×17!)
  + ★★★ DUHOVNIŠKA-TROJNA-IZMENJAVA ('…binant-Kroggj-coop[?]' ↔ 'Franz-Dovgan' ↔ 'Franz-Janičar-coop'!-3-podpisa!)
  + ★★★ z28-TODTGEBOREN-GRIBLJE (garble-'Nrbžgabumšt'≈'nichtlebendgeburt'!-botra+duhovnik-PRAZNA!)
  + ★★★ z65-NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!-×5-linije!)
  + ★★★ DVOJČKI-×2 (z17/z18-Krasinec-h43-bracket! + z87/z88-Bajukh-squiggle!)
  + ★★★ FOLIACIJA-'sken−5'-13/14 (87–99!-LUKNJA-'94'-NA-s99-TEMNA-'34'-ANOMALIA!) + s105-DUPLIKAT-SKEN (≡s104!)
  → 'sken−6'-od-s106-P227-konvencija-ARTEFAKT-DUPLIKATA-RAZLAGA-NAJDENA! + LEPLJENEC-1908 (Danijel-Barle!).
Izhod: /tmp/p228/entries_1878.json"""
import json

TMP = "/tmp/p228"

GRIBLJE = [
 {"z":"z23","sken":96,"pag":"91 [konv.-sken−5]","mesec":"April","rojen":"4","krsten":"4","vas":"Griblje","hisna":"73",
  "otrok":"Georg","spol":"moški",
  "ocec":"Nicolaus Županič[?]-garble, ½ Gübl",
  "matec":"Cathar. z.b. Pezdire [~PEZDIRC!]",
  "botra":"Nicolaus Starasinič + Margareth Županič",
  "_opomba":"★★★ PEZDIRC-matec-nit (1/6-Griblje!-continuum-8-let!) + ★★★ črnilo-pripis-'por. 18/11 1920 v Kuniva[?]-† 12.5.1939' (ročno-črnilo!) + podpis-Franz-DOVGAN + h73 (z31-h43-RAZLIČNI-Kurrent-7/4!)"},
 {"z":"z24","sken":96,"pag":"91 [konv.-sken−5]","mesec":"April","rojen":"4","krsten":"5","vas":"Griblje","hisna":"19",
  "otrok":"Anton","spol":"moški",
  "ocec":"Johann Hriže[?]-garble, ½ güblo[?]",
  "matec":"Maria Sodec",
  "botra":"Peter Klebec + Catharina Jakofeč",
  "_opomba":"★★★ podpis-TRETJI-DUHOVNIK-'…binant-Kroggj[?]-coop'-garble (1/16-Griblje!-trojna-izmenjava!) + rojen≠krsten-4/5 + h19"},
 {"z":"z27","sken":96,"pag":"91 [konv.-sken−5]","mesec":"April","rojen":"25","krsten":"25","vas":"Griblje","hisna":"29",
  "otrok":"Johann","spol":"moški",
  "ocec":"Peter Milek [~MILEK!], ¼ Ġ.",
  "matec":"Anna j. Hrižan",
  "botra":"Johann Pajk[?]-garble + Barbava Adlesič[?]-garble",
  "_opomba":"★★★ MILEK-oče-nit (1/2-1878!) + podpis-Franz-DOVGAN + h29"},
 {"z":"z28","sken":97,"pag":"92 [konv.-sken−5]","mesec":"April","rojen":"25","krsten":"25","vas":"Griblje","hisna":"11",
  "otrok":"IME-GARBLE-'Nrbžgabumšt'[?] ≈ 'nichtlebendgeburt'[?]-X-open","spol":"X-open",
  "ocec":"Mathias Drmelič[?]-garble, ¼ Ġ.",
  "matec":"Agnes z.b. Hlobuvar[?]-garble",
  "botra":"BOTRA-PRAZNA [—!]",
  "_opomba":"★★★ TODTGEBOREN-GRIBLJE (garble-'Nrbžgabumšt'≈'nichtlebendgeburt'/'Notgeburt'-X-open!-P227-todtgeboren-×3-PARALELA!-1.-v-GRIBLJI!) + botra+duhovnik-VSI-PRAZNI! + h11 (z29-×2!) + MAX-krop-potrjeno"},
 {"z":"z29","sken":97,"pag":"92 [konv.-sken−5]","mesec":"April","rojen":"26","krsten":"26","vas":"Griblje","hisna":"11 [DUEL-×2-JASNO!]",
  "otrok":"Joannes","spol":"moški",
  "ocec":"Mathias Lunič[?]-Tumie[?]-garble, ½ Gübl",
  "matec":"Barbara z.b. Dragos [~DRAGOŠ!]",
  "botra":"Mathias Jakofeč + Anna Simec [~SIMEC!]",
  "_opomba":"★★★ DRAGOŠ-matec-nit (1/3!) + SIMEC-botra-nit (1/2!) + h11-×2 (z28!-DUEL-REŠEN-1:1-VIZUALNO!) + podpis-Franz-DOVGAN"},
 {"z":"z30","sken":97,"pag":"92 [konv.-sken−5]","mesec":"April","rojen":"28","krsten":"29","vas":"Griblje","hisna":"1",
  "otrok":"Anna","spol":"ženski",
  "ocec":"Nicolaus Beltho[?]-garble, ¼ Gübl",
  "matec":"Anna z.b. Jakofeč",
  "botra":"Johann Jakofeč + Agnes Jakofeč [~JAKOFČIČ-×2-vrstica!]",
  "_opomba":"★★★ JAKOFČIČ-DVOJNI-botra-nit (×2-v-vrstici!) + rojen≠krsten-28/29 + podpis-Franz-DOVGAN + h1"},
 {"z":"z31","sken":97,"pag":"92 [konv.-sken−5]","mesec":"Mai","rojen":"1","krsten":"1","vas":"Griblje","hisna":"43",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Johann Vludži[?]-garble, ½ gübl",
  "matec":"Maria z.b. Brula[?]-garble",
  "botra":"Marcus Skala[?]-garble + Catharina Hlobučič[?]-garble",
  "_opomba":"★★★ MODRI-MATIČARSKI-PRIPIS-'umrla dne 18.6.1955 v gvi števil 43'-MATCH-h43! + h43 (z23-h73-RAZLIČNI!) + Mai-blok-start + podpis-Franz-DOVGAN"},
 {"z":"z45","sken":99,"pag":"94 [konv.-sken−5]","mesec":"Juli","rojen":"9","krsten":"9","vas":"Griblje","hisna":"55",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Nicolaus Simec [~SIMEC!], ¼ Gübler",
  "matec":"Maria Pezdire [~PEZDIRC!]",
  "botra":"Marko Kraus[?]-garble + Ana Kukar[?]-garble",
  "_opomba":"★★★ SIMEC-oče-nit (2/2-KOMPLET!) + ★★★ PEZDIRC-matec-nit (2/6!) + podpis-Franz-JANIČAR-coop (1/3-Griblje!) + h55 (z56-h53-RAZLIČNI!) + Juli-blok"},
 {"z":"z46","sken":99,"pag":"94 [konv.-sken−5]","mesec":"Juli","rojen":"30-x [Juni-30-PREČRTAN!→Juli-1]","krsten":"1","vas":"Griblje","hisna":"64 [DUEL-64/69-X-open-identični-glifyi-z81!]",
  "otrok":"Margarebh","spol":"ženski",
  "ocec":"Nicolaus Terdič[?]-Perdič[?]-garble [~PEZDIRC-grafija-X-open!], ¼ Ġ.",
  "matec":"Karth. z.b. Adlesič[?]-garble",
  "botra":"Johann Pezdire [~PEZDIRC!] + Katharina Krambič[?]-garble",
  "_opomba":"★★★ PEZDIRC-DVOJNI-vrstica (oče-X-open + boter!-2/6!) + ★★★ DATUMSKA-KOREKCIJA ('Juni 30'-prečrtan → 'Juli 1'!-Z49-P226-PARALELA!) + h64-×2-DUEL (z81-identični-glifyi!-64/69-X-open!) + podpis-Franz-DOVGAN"},
 {"z":"z52","sken":100,"pag":"95 [konv.-sken−5]","mesec":"September","rojen":"9","krsten":"9","vas":"Griblje","hisna":"18 [celica-'8'-+'1'-slabo-MODRI-'št-18'-NAMIG!]",
  "otrok":"Catharina","spol":"ženski",
  "ocec":"Johann Jakofeč[?]-Šovar[?]-garble",
  "matec":"Maria Uhr",
  "botra":"Jre Dragot[?] [~DRAGOŠ-X-open!] + Cathar. Hlobucar[?] [~KLOBUČAR-X-open!]",
  "_opomba":"★★★ MODRI-MATIČARSKI-PRIPIS-'Umrila dne 18.3.1959 v Gribljah št 18 (MMK gradec l. 1959, št 115 (kop. št 7)'!-MATCH-h18! + DRAGOŠ-boter-X-open (2/3!) + KLOBUČAR-boter-X-open + podpis-Franz-JANIČAR-coop (2/3!) + September-blok"},
 {"z":"z53","sken":100,"pag":"95 [konv.-sken−5]","mesec":"September","rojen":"11","krsten":"11","vas":"Griblje","hisna":"48",
  "otrok":"Anna","spol":"ženski",
  "ocec":"Johann Hlobunür[?]-garble, ¼ Ġ.",
  "matec":"Barbara z.b. Pezdrič [~PEZDIRC!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Agnes Smucel[?]-garble",
  "_opomba":"★★★ PEZDIRC-matec-nit (3/6!) + BRODARIČ-boter-nit (1/3!) + podpis-Franz-DOVGAN + h48"},
 {"z":"z56","sken":100,"pag":"95 [konv.-sken−5]","mesec":"August","rojen":"19","krsten":"20","vas":"Griblje","hisna":"53",
  "otrok":"Petrus","spol":"moški",
  "ocec":"Johann Pezdire [~PEZDIRC!], ½ gübl",
  "matec":"Anna z.b. Terdič[?]-Perdič[?]-garble [~PEZDIRC-grafija-X-open!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Anna Dragos [~DRAGOŠ!]",
  "_opomba":"★★★ PEZDIRC-matec-garble-X-open (oče+matec!-4/6!) + BRODARIČ-boter (2/3!) + DRAGOŠ-boter (3/3-KOMPLET!) + rojen≠krsten-19/20 + podpis-Franz-DOVGAN + h53 (z45-h55-RAZLIČNI!) + August-blok"},
 {"z":"z64","sken":101,"pag":"96 [konv.-sken−5]","mesec":"September","rojen":"28","krsten":"29","vas":"Griblje","hisna":"77",
  "otrok":"Michail","spol":"moški",
  "ocec":"Johann Tuttler[?]-garble, Göntlon[?]-garble",
  "matec":"Kath. z.b. Hrižan",
  "botra":"Anton Hure [~HURE!] + Margareth Tuttler[?]-garble",
  "_opomba":"★★★ HURE-boter-nit (1/1!-P227-z63-oče-PARALELA!) + ★★★ črnilo-pripis-dolg-'poročen 27/9 974[?] v Mamorških vas[?] N.N. 17.3.972[?]'-garble + rojen≠krsten-28/29 + podpis-Franz-DOVGAN + h77"},
 {"z":"z65","sken":102,"pag":"97 [konv.-sken−5]","mesec":"October","rojen":"3","krsten":"3","vas":"Griblje","hisna":"6",
  "otrok":"Johann","spol":"moški",
  "ocec":"OČETOV-STOLPEC-PRAZEN [NEZAKONSKI!]",
  "matec":"Maria Jakofeč[?], Lnišfhnurgi[?]-garble",
  "botra":"Mathias Murla[?]-Merla[?]-garble + Catharina Piglher[?]-garble",
  "_opomba":"★★★ NEZAKONSKI-GRIBLJE (očetov-stolpec-PRAZEN!-P227-z23-PARALELA!-×5-linije!) + ★★★ črnilo-pripis-'um 16 Novr 880[?]-gestorben[?]'-X-open + podpis-Franz-DOVGAN + h6 + Oktobar-blok"},
 {"z":"z69","sken":102,"pag":"97 [konv.-sken−5]","mesec":"October","rojen":"23","krsten":"23","vas":"Griblje","hisna":"38",
  "otrok":"Johann","spol":"moški",
  "ocec":"Georg Simec [~SIMEC!], Göntlon[?]-garble",
  "matec":"Anna z.b. Hrižan",
  "botra":"Gotlob Tokar[?]-garble + Anna Dragos [~DRAGOŠ!]",
  "_opomba":"★★★ SIMEC-oče-nit (2/2!) + DRAGOŠ-botra-KOMPLET (3/3!) + ★★★ črnilo-pripis-'† 31.10.1931 v Anwaru[?]-naslednju v Reading[?]' + podpis-Franz-DOVGAN + h38"},
 {"z":"z81","sken":104,"pag":"99 [konv.-sken−5]","mesec":"December","rojen":"2","krsten":"2","vas":"Griblje","hisna":"64 [DUEL-64/69-X-open-identični-glifyi-z46!]",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Mathias Jakofeč [~JAKOFČIČ!]",
  "matec":"Maria Pezdire [~PEZDIRC!]",
  "botra":"Georg Pezdire [~PEZDIRC!] + Kath. Novak",
  "_opomba":"★★★ PEZDIRC-DVOJNI-vrstica (matec+boter!-5/6!-JAKOFČIČ-oče!) + h64-×2-DUEL (z46-identični-glifyi!-64/69-X-open!) + podpis-Franz-JANIČAR-coop (3/3!) + Dezember-blok + s105-DUPLIKAT-SKEN-istega-lista!"},
]
assert len(GRIBLJE) == 16

OKVIR = {
 "window": "s92–s106 (15 skenov; s99–s106-proba-P227-LEAD! s92–s98-probe-nazaj! s92-MEJA! s105-DUPLIKAT! s106-tail-P227!)",
 "prenos": "2×-neodvisna-md5-15/15 (s92–s106!)",
 "foliacija": "gola-svinčna-'sken−5'-13/14-SEKVENČNO (s92='87'/s93='88'/s94='89'/s95='90'/s96='91'/s97='92'/s98='93'/s99-TEMNA-'34'-ANOMALIA-LUKNJA-'94'!/s100='95'/s101='96'/s102='97'/s103='98'/s104='99') + s105='99'-DUPLIKAT-SKEN (≡s104-1:1!-LEPLJENEC-1908!) → s106='100'-'sken−6'-P227-konvencija = ARTEFAKT-DUPLIKATA-s105-RAZLAGA-NAJDENA! (SKUPNA-SERIJA-87–158!)",
 "mejaStart": "s92/s93 (TAIL-1877-Dezember-z86–z91 + glava-'Jahr 1877'-BREZ-VSOTNE/velikih-cifer-P225-TIP! + RESTART-z1-NA-DAN-[8↔9]-JÄNNER-DUEL-Geburt-'9'/Taufe-'8'-OBRNJENO-X-open!-Boginja-vas-h14-Margareth-MODRI-dolg-†6.12.1959!-mesec-'Jänner'-PREČRTAN!-8.-restart-z1!)",
 "mejaKonec": "s105/s106 (P227!-TAIL-1878-z90–z94 + VSOTNA-RAZPETA-'1 8'+'79'='1879'-velika-letnica! + RESTART-z1-1879!)",
 "rowsTotal": 94,
 "aritmetika": "7+6+7+7+6+8+8+7+8+8+7+10+5 = 94 = P227-LEAD-'1878 = 94-vpisov-pričakovano'-1:1-INVARIANTA! (zap-stolpci-15/15-ČISTO-brez-duplikatov!)",
 "meseci": "A6+Mai1+Aug1+Juli2+S3+O2+D1 = 16-Griblje (Jänner/Feber/März-×0!-3-prazne!)",
 "duhovniki": "TROJNA-IZMENJAVA-'…binant-Kroggj[?]-coop' ↔ 'Franz-Dovgan' ↔ 'Franz-Janičar-coop' (3-podpisa!-vs-×2-1879/1880!-Kroggj-z1–z26-alternacija-z-Dovganom!-Janičar-vstopi-z35!-Griblje-split-DOVGAN-×10/JANIČAR-×3/KROGGJ-×1/PRAZNA-×1!)",
}

stats = {
 "griblje_vpisov": 16,
 "griblje_his": 14,
 "dup": "h11-×2 (z28+z29!-s97-1:1-VIZUALNO!) + h64-×2 (z46+z81!-identični-glifyi-64/69-DUEL-X-open!) — vs-h43-×2/h33-×2-ni (z23-h73!-z31-h43!-z45-h55!-z56-h53!-RAZLIČNI!)",
 "pezdirc": "×17-vrstic-NOV-REKORD-LINJE (vs-×14-P226-×12-P227!): Griblje-×6-vrstic (z23-matec! + z45-matec! + z46-oče-Terdič-X-open+boter-Johann-DVOJNI! + z53-matec-Pezdrič! + z56-oče+matec-garble! + z81-matec+boter-Georg-DVOJNI!) + ne-Griblje-×11 (z2/z3/z4-matec-×3-ZAPOREDOMA-RESTART-stran! + z7-boter + z22/z25-oče + z44-boter + z60-boter + z70-oče + z84-boter + z89-oče!) — grafija-continuum-8-let: ×4/×4/×6/×4/×9/×14/×12/×17!",
 "milek": "×2 (z27-oče-Griblje! + …)",
 "simec": "×3 (z29-botra-Anna-Griblje! + z45-oče-Griblje! + z69-oče-Griblje!)",
 "dragoš": "×3 (z29-matec-garble! + z52-botra-Jre-Dragot-X-open! + z56-botra-Anna! + z69-botra!-×4-vrstic!)",
 "jakofčič": "×5+-vrstic (z30-botra-×2-DVOJNI! + z52-oče-garble + z64? + z81-oče! + z24-botra-Catharina + …)",
 "klobučar": "×1-X-open (z52-botra-Cathar.-Hlobucar!)",
 "brodarič": "×2 (z53-boter-Anton! + z56-boter-Anton!)",
 "hure": "×1 (z64-boter-Anton!-P227-z63-oče-PARALELA!)",
 "križan": "×2 (z44-matec-Barbara-neG! + matec-Hrižan-variants?)",
 "dvojcki": "★★★ ×2 (z17/z18-Krasinec-h43-Febrar-28/März-1-zavit-oklepaj-bracket-P223-PARALELA! + z87/z88-Bajukh-Primostek/Gerag[?]-h12-December-17/17-squiggle-mark-+Agnes-Bajukh-PREČRTANA-v-botrah!-vas-popravki!) — vs-×3-P227-REKORD",
 "todtgeboren": "★★★ z28-GRIBLJE-TODTGEBOREN (garble-'Nrbžgabumšt'≈'nichtlebendgeburt'/'Notgeburt'-X-open!-MAX-krop!-botra+duhovnik-VSI-PRAZNI!-1.-v-GRIBLJI!-P227-×3-PARALELA!)",
 "nezakonski": "★★★ ×5-REKORD-LINJE (očetov-stolpec-PRAZEN!): z9-Dobravce-h13 (Jänner-25/26!-Dovgan!) + z13?-Gradaz-h68 (Februar-2/3!) + z36?-Krasine-h23 (Mai-21!) + z63?-Krasine-h9 (Sept-22!) + z65-GRIBLJE-h6 (October-3/3!-P227-z23-PARALELA!) — X-open-za-z13/z36/z63 (MAX-krop!)",
 "modri": "★★★ ×12+-REKORD-LINJE (MODRI-pripisi!): z1-dolg-'†6.12.1959-Pančiči[?]-MMK-1959'! + z2-dolg-'†29.12.1960-Gradac[?]-MMK-1960-kop.19/9-908'! + z11-'†9.9.1978'! + z20-'†30.8.1949'! + z22-'†30.IV.1948-godine-pri-Begunjah'! + z31-GRIBLJE-'†18.6.1955-št-43'-MATCH! + z37-'†10.7.1963-Gradac-št-38'! + z38-'†10.7.1967-Auflišši-Matica-Preg-št-43'! + z39-'†27.8.1961'! + z42-'†1.8.1955-št-31/34'! + z51-'†18.3.1959-Gribljah-št-18'-MATCH-h18! + z83-'†21.4.1954-št-66'! — 1948–1978-razpon!-×2-MATCH-hišam (z31-h43!-z52-h18!)",
 "cnilo_pripisi": "★★★ ČRNILO-pripisi-×4-Griblje (ročno-črnilo!): z23-'por. 18/11 1920-† 12.5.1939'! + z64-'poročen-27/9-974[?]-dolg'! + z65-'um-16-Novr-880[?]'! + z69-'† 31.10.1931-Anwaru[?]-Reading[?]'! + ne-G: z51-'†17.6.1935'! + z82-'am-16-Jänr-879[?]'! + z58-'†27.4.1966'! + z60-'†8.3.1972-+✠-margina'! + z75-'✠-4/y-1884'! + z72-'†-9/1-878[?]'! + z86-'†-5.4.1935'! + z91-'†-3.1.1932'-P227-TAIL! + z93-'+8/879'-P227-TAIL!",
 "popravki": "★★★ POPRAVKI-×5: z87-VAS-POPRAVEK ('Nicolaus'-✗✗-DOVEMA-KRIŽEMA→'Primostek'!-pisarjev-slip-otrokovo-ime-v-vas-stolpcu!) + z88-vas-'Gerag[?]'-X-open (✗-v-sredini!) + z46-DATUMSKA-KOREKCIJA ('Juni-30'-prečrtan→'Juli-1'!) + z1-MESEC-PREČRTAN ('Jänner'-ponovljen-čez-prečrtano!) + z4-OČE-POPRAVEK ('Georg-gm[?]fič'-PREČRTAN→'Nicolaus-Uhr'!)",
 "posebne": "z1-RESTART-DATUMSKI-DUEL (Geburt-'9'/Taufe-'8'-OBRNJENI-glifyi-X-open!-P227-8./9.-PARALELA!) + s105-LEPLJENEC-1908 (Danijel-Barle-rojen-19/1-1879-v-Podzemlju-+Marijo-Župan-15/5-1908-poročen-Župni-urad-Svinče[?]-25/5-1908-OVALNI-PEČAT-+podpis-'Ant.-Peterlin[?]'!-lepljen-ČEZ-z82–z85!) + HEBAMME-Maria-Rom/Born-×8 (z10/z19/z34/z35/z37/z40/z68/z72!-continuum!) + rojen≠krsten-Griblje-×5 (z24-4/5! + z30-28/29! + z46-30/1! + z56-19/20! + z64-28/29!) + ✠-veliki-križ-margina (z60!) + zap-r1-'34-42'-STRAY-s99 (temna-'34'+svetla-'42'!)",
}

out = {"leto": 1878, "griblje_entries": GRIBLJE, "okvir": OKVIR, "stats": stats}
json.dump(out, open(f"{TMP}/entries_1878.json", "w"), ensure_ascii=False, indent=1)
print(f"entries_1878.json: {len(GRIBLJE)}-Griblje-vpisov")
