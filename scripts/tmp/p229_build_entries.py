#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P229 — agregacija 20-GRIBLJE-vpisov leta 1877 (krstna PREDZGODOVINA 04104, 9/15!).
MEJA-1876/77 = s78-ENE-STRANI (TAIL-1876-Dobravce-Dez-24/26 + glava-'Jahr 1876' + ★★★ 'Incipit-annus-Domini-1877'
  -VELIKA-KALLIGRAFIJA-ČEZ-SREDINO-STRANI-1.-INCIPIT-v-krstni-liniji! + glava-'Jahr 1877-Jänner' + RESTART-z1-NA-DAN-9./10.-JÄNNER-Zemelj-h20!)
  = 68.-POTRDITEV-invariante (67.-P228!).
★★★ LEAD-KOREKCIJA: '1877 = 91'-P228-LEAD-BILA-NAPAČNA (predpostavka-tail-'z86–z91'!) → REALNOST: 108-VPISOV (z1–z108!)
  — vrstna-aritmetika 5+7+8+9+7+8+9+7+8+8+7+6+7+6+6 = 108 + zap-stolpci-VIDNI-×6-strani-1:1 (s78:1–5!-s79:6–12!-s80:13–20!
  -s81:21–29!-s82:30–36!-s83:37–44!) = NOV-REKORD-POTRDITEV-zap-1:1! (LEAD-KOREKCIJA-9.×-linija-P228-'93'-NA-s98-PARALELA!)
★★★ 20-GRIBLJE / 18-hiš (h6-×2: z13+z56! + h14-×2: z67+z68-DVOJČKI-bracket-'Zwillings'-nota!)
  — ★★★ DVOJČKI-×4-REKORD-LINJE (z28/z29-Prilozje-h30! + z46/z47-Grem-h26! + z67/z68-GRIBLJE-h14! + z75/z76-Krasine-h18!-vs-×3-P227!)
  + ★★★ TODTGEBOREN-TIP-garble-×3 (z41-'Nurlygaburišt'! + z42-'Tuolynbuns'-hišna-PRAZNA! + z65-'Nurlygabuništ'-Kloster!-P228-z28-'Nrbžgabumšt'-PARALELA!)
  + ★★★ PEZDIRC-×11-vrstic-continuum-9-let (z8-DVOJNI-Griblje!-×7-Griblje + ×4-ne-Griblje!)
  + ★★★ November-31-DUEL-×2 (z89-GRIBLJE-h40! + z90-Dragoše!-Nov-31-NE-OBSTAJA-pisarjev-slip-za-Nov-30/Dec-1!)
  + ★★★ RETRO-VPISI-×2 (z97/z98-Nov-29/30-NA-STRANI-PO-Dec-28/29-s91!-nakadna-dopolnitev!)
  + ★★★ DUHOVNIŠKA-IZMENJAVA-1877 ('Ferdinand-Hoggin/Hoggja/Roggja-coop'-KURRENT-DUEL-podpis-DOMINANTA! ↔ 'Franz-Dovgan'-ALTERNIRAJÖČE!)
  + ★★★ z22-PREČRTANA-VRSTICA-GRIBLJE (veliki-X-črnilo-čez-ime+'legitimaha-že'+pripis! + oče-'Samuel-Štua'-PREČRTAN-swap!)
  + ★★★ z15-DATUMSKI-DUEL-Feb28→Mar1-GRIBLJE (rojen≠krsten-ČEZ-MESEC!-1877-NON-LEAP!) + MODRI-×9 (z8-MATCH-h37!-z27-TORONTO-KANADA!)
  + †-črnilo-×2-Griblje (z56-†30.4.19?0! + z94-†6.3.1945-P228-z87-†6.4.1945-PARALELA!).
Izhod: /tmp/p229/entries_1877.json"""
import json

TMP = "/tmp/p229"

GRIBLJE = [
 {"z":"z8","sken":79,"pag":"74 [konv.-sken−5]","mesec":"Jänner","rojen":"30","krsten":"31","vas":"Griblje","hisna":"37",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Mathias Pezdire [~PEZDIRC!], ½ Ġünšlcn[?]-garble",
  "matec":"Dorothea z.b. Jakofčič [~JAKOFČIČ!]",
  "botra":"Johann Milek [~MILEK!] + Anna Pezdire [~PEZDIRC!]",
  "_opomba":"★★★ PEZDIRC-DVOJNI-vrstica (oče+botra!-1/7-Griblje!-continuum-9-let!) + MILEK-boter-nit + ★★★ MODRI-MATIČARSKI-PRIPIS-'umrla-dne-21.4.1961-v-gribljskih-št.-37-vrnica'-MATCH-h37! + podpis-'Ferdinant-Roggja-coop'-KURRENT-DUEL + Jänner-30/31 (rojen≠krsten!)"},
 {"z":"z13","sken":80,"pag":"75 [konv.-sken−5]","mesec":"Februar","rojen":"24","krsten":"24","vas":"Griblje","hisna":"6",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Mathias Jakofčič [~JAKOFČIČ!], ¼ Ġübl",
  "matec":"Anna z.b. Ceglko[?]-garble",
  "botra":"Georg Ceglko[?]-garble + Katharina Lunic[?]-garble",
  "_opomba":"★★★ JAKOFČIČ-oče-nit (1/7!) + ★★★ MODRI-dolg-'Umrła-dne-27.-januarija-1963-v-Gribljah'+'o. 23/1.1910'! + h6 (z56-×2!) + podpis-Franz-DOVGAN"},
 {"z":"z15","sken":80,"pag":"75 [konv.-sken−5]","mesec":"März","rojen":"28-Feb [Feb-28-ČEZ-MESEC!→Mar-1]","krsten":"1","vas":"Griblje","hisna":"13",
  "otrok":"Josef","spol":"moški",
  "ocec":"Mathias Jakofčič [~JAKOFČIČ!], ½ Ġ",
  "matec":"Maria z.b. Hrižan [~HRIŽAN!]",
  "botra":"Mathias Hambič [~HAMBIČ!] + Anna Pezdire [~PEZDIRC!]",
  "_opomba":"★★★ JAKOFČIČ-oče-nit (2/7!) + PEZDIRC-boter-nit (2/7!) + HRIŽAN-matec-nit + ★★★ DATUMSKI-DUEL-Feb28→Mar1 (rojen≠krsten-ČEZ-MESEC!-1877-NON-LEAP!-potrjeno-krop!) + HAMBIČ-boter + podpis-Ferdinant-Hoggin-coop"},
 {"z":"z22","sken":81,"pag":"76 [konv.-sken−5]","mesec":"März","rojen":"23","krsten":"23","vas":"Griblje","hisna":"36",
  "otrok":"Maria-PREČRTANA-VELIKI-X-ČRNILO!","spol":"ženski",
  "ocec":"Samuel Štua[?]-garble-PREČRTAN-črnilo-swap-X-open!",
  "matec":"Anna z.b. Simec [~SIMEC!]-'Simec-Leizige-ji-Ġüblerskojte[?]'-garble",
  "botra":"Mathias Worh[?]-Wroth[?]-garble + Barbara Brodarič [~BRODARIČ!]",
  "_opomba":"★★★ PREČRTANA-VRSTICA-GRIBLJE (veliki-X-črnilo-čez-IME+'legitimaha-že'+pripis!-1.-v-GRIBLJI!) + ★★★ OČE-PREČRTAN-SWAP (črnilo-'Samuel-Štua'-X-open!) + SIMEC-matec-nit + BRODARIČ-boter-nit + ★★★ MODRI-'Umrła-dne-20.I-1912-v-Podgoricah[?]'-X-open + podpis-'Ferdinant-Roggja-coop'-DUEL"},
 {"z":"z25","sken":81,"pag":"76 [konv.-sken−5]","mesec":"März","rojen":"29","krsten":"30","vas":"Griblje","hisna":"65",
  "otrok":"Mathias","spol":"moški",
  "ocec":"Mathias Milek [~MILEK!], ½ Ġübl",
  "matec":"Cathar. z.b. Skarazimič[?]-garble",
  "botra":"Peter Pezdire [~PEZDIRC!] + Anna Kušter[?]-Kunker[?]-garble",
  "_opomba":"★★★ MILEK-oče-nit (2/5!) + PEZDIRC-boter-nit (3/7!) + rojen≠krsten-29/30 + podpis-Franz-DOVGAN + h65"},
 {"z":"z34","sken":82,"pag":"77 [konv.-sken−5]","mesec":"April","rojen":"30","krsten":"30","vas":"Griblje","hisna":"74",
  "otrok":"Johann","spol":"moški",
  "ocec":"Mathias Hambič [~HAMBIČ!], ½ Ġütler",
  "matec":"Catharina Brinc [~BRINC!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Maria Milek [~MILEK!]",
  "_opomba":"★★★ HAMBIČ-oče-nit (P228-z87/88-PARALELA!) + BRODARIČ-boter-nit (2/6!) + MILEK-boter-nit (3/5!) + BRINC-matec (z67/68-PARALELA!) + podpis-'Ferdinant-Hoggja-coop'-KURRENT-DUEL + h74"},
 {"z":"z56","sken":85,"pag":"80 [konv.-sken−5]","mesec":"Juli","rojen":"23","krsten":"24","vas":"Griblje","hisna":"6",
  "otrok":"Katharina","spol":"ženski",
  "ocec":"Martin Hlobučar [~KLOBUČAR!], ½ Ġüblan",
  "matec":"Kathar. z.b. Milek [~MILEK!]",
  "botra":"Johann Jakofčič [~JAKOFČIČ!] + Agnes Šrucelj[?]-garble",
  "_opomba":"★★★ KLOBUČAR-oče-nit (1/4!) + MILEK-matec-nit (4/5!) + JAKOFČIČ-boter-nit + ★★★ črnilo-pripis-'Umrła-dne-30.4.19?0-v-Gribljah'-X-open-1940/1950! + rojen≠krsten-23/24 + podpis-Franz-DOVGAN + h6-×2 (z13!)"},
 {"z":"z61","sken":86,"pag":"81 [konv.-sken−5]","mesec":"August","rojen":"15","krsten":"15","vas":"Griblje","hisna":"7",
  "otrok":"Johann","spol":"moški",
  "ocec":"Andreas Kerbler[?]-garble, ½ Ġ",
  "matec":"Marg. Štrunc[?]-Štruclj[?]-garble",
  "botra":"Georg Simec [~SIMEC!] + Maria Štrucelj[?]-garble",
  "_opomba":"★★★ SIMEC-boter-nit (2/3!) + podpis-Franz-DOVGAN + h7 (P228-izjema-h7-nit-continuum-11-let!) + August-blok"},
 {"z":"z67","sken":86,"pag":"81 [konv.-sken−5]","mesec":"August","rojen":"31 [Aug-31→Sep-1!]","krsten":"1","vas":"Griblje","hisna":"14",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Michael Pezdure [~PEZDIRC!], ¼ Ġübler",
  "matec":"Anna Brinc [~BRINC!]",
  "botra":"Mathias Jakofčič [~JAKOFČIČ!] + Catharina Hambič [~HAMBIČ!]",
  "_opomba":"★★★ DVOJČKI-×1-GRIBLJE (z67/z68-h14-bracket-'Zwillings'-vertikalna-nota-potrjena-krop!-7.-dvojčki-linija!-P223-GRIBLJE-h68-P226-h20-P227-×3-P228-×2-PARALELA!) + ★★★ PEZDIRC-oče-nit (4/7!) + BRINC-matec (z34-PARALELA!) + JAKOFČIČ+HAMBIČ-botra + rojen≠krsten-31/1 + podpis-Ferdinand-Hoggin-coop"},
 {"z":"z68","sken":86,"pag":"81 [konv.-sken−5]","mesec":"August","rojen":"31 [Aug-31→Sep-1!]","krsten":"1","vas":"Griblje","hisna":"14",
  "otrok":"Margaretha","spol":"ženski",
  "ocec":"Michael Pezdure [~PEZDIRC!], ¼ Ġübler (isti!)",
  "matec":"Anna Brinc [~BRINC!] (ista!)",
  "botra":"Mathias Jakofčič + Catharina Hambič (isti!)",
  "_opomba":"★★★ DVOJČKI-×1-GRIBLJE (z67-zaverižani!-isti-starši+isti-botra-1:1-krop!) + ★★★ PEZDIRC-oče-nit (5/7!) + h14-×2 (z67!) + rojen≠krsten-31/1"},
 {"z":"z77","sken":88,"pag":"83 [konv.-sken−5]","mesec":"October","rojen":"5","krsten":"6","vas":"Griblje","hisna":"2",
  "otrok":"Johann","spol":"moški",
  "ocec":"Peter Sellebec[?]-garble, ¼ Ġ",
  "matec":"Maria Jakofčič [~JAKOFČIČ!]",
  "botra":"Mathias Tunič[?]-garble + Barbara Hlobučar [~KLOBUČAR!]",
  "_opomba":"★★★ JAKOFČIČ-matec-nit (3/7!) + KLOBUČAR-boter-nit (2/4!) + rojen≠krsten-5/6 + podpis-Franz-DOVGAN + h2 + Oktobar-blok"},
 {"z":"z79","sken":88,"pag":"83 [konv.-sken−5]","mesec":"October","rojen":"11","krsten":"11","vas":"Griblje","hisna":"35",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Mathias Hrižan [~HRIŽAN!], ¼ Ġ",
  "matec":"Anna Cegdin[?]-Ceglik[?]-garble",
  "botra":"Mathias Urih[?]-garble + Maria Ceglinc[?]-garble",
  "_opomba":"★★★ HRIŽAN-oče-nit (2/5!) + podpis-Franz-DOVGAN + h35 (z101-h34-RAZLIČNI!)"},
 {"z":"z84","sken":89,"pag":"84 [konv.-sken−5]","mesec":"November","rojen":"22","krsten":"23","vas":"Griblje","hisna":"20",
  "otrok":"Catharina","spol":"ženski",
  "ocec":"Peter Pezdire [~PEZDIRC!], ½ Ġütter",
  "matec":"Catharina Deblič [~DEBLIČ!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Catharina Milek [~MILEK!]",
  "_opomba":"★★★ PEZDIRC-oče-nit (6/7!) + DEBLIČ-matec-nit + BRODARIČ-boter-nit (3/6!) + MILEK-boter-nit (5/5!) + rojen≠krsten-22/23 + podpis-Ferdinant-Hoggin-coop + November-blok + h20"},
 {"z":"z85","sken":89,"pag":"84 [konv.-sken−5]","mesec":"November","rojen":"23","krsten":"24","vas":"Griblje","hisna":"9",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Johann Jakofčič [~JAKOFČIČ!], ½ Ġütl",
  "matec":"Maria rođ. Jakofčič [~JAKOFČIČ!]",
  "botra":"Nicolaus Šuštile[?]-garble + Anna Dragoš [~DRAGOŠ!]",
  "_opomba":"★★★ JAKOFČIČ-DVOJNI-vrstica (oče+matec!-4/7!) + ★★★ DRAGOŠ-boter-nit (1/1!-P228-×4-KOMPLET-PARALELA!) + rojen≠krsten-23/24 + podpis-Ferdinant-Hoggin-coop + h9"},
 {"z":"z89","sken":89,"pag":"84 [konv.-sken−5]","mesec":"November","rojen":"31-x [Nov-31-NE-OBSTAJA!→Dec-1-DUEL!]","krsten":"1","vas":"Griblje","hisna":"40",
  "otrok":"Johann","spol":"moški",
  "ocec":"Johann Pezdič[?]-Pezdire[?]-garble-X-open [~PEZDIRC!], ½ Ġ",
  "matec":"Anna z.b. Jakofčič [~JAKOFČIČ!]",
  "botra":"Mathias Deblič [~DEBLIČ!] + Barbara Hlobučar [~KLOBUČAR!]",
  "_opomba":"★★★ November-31-DUEL-×1-GRIBLJE (Nov-31-NE-OBSTAJA-pisarjev-slip-za-Nov-30/Dec-1!-z90-Dragoše-PARALELA-×2!) + ★★★ PEZDIRC-oče-nit-X-open (7/7!) + JAKOFČIČ-matec-nit (5/7!) + DEBLIČ+KLOBUČAR-botra + rojen≠krsten-31/1 + podpis-Ferdinant-Hoggin-coop + h40"},
 {"z":"z94","sken":90,"pag":"85 [konv.-sken−5]","mesec":"Dezember","rojen":"18","krsten":"18","vas":"Griblje","hisna":"49 [DUEL-49/40-X-open!]",
  "otrok":"Katharina","spol":"ženski",
  "ocec":"Anton Brodarič [~BRODARIČ!], ½ Ġ",
  "matec":"Barbara Cigotič[?]-garble",
  "botra":"Peter Ceglinc[?]-Cegdin[?]-garble + Ana Husič [~HUSIČ!]",
  "_opomba":"★★★ BRODARIČ-oče-nit (4/6!) + ★★★ črnilo-pripis-'† 6.3.1945'-s-križem (P228-z87-'†6.4.1945'-PARALELA!-mar/apr-1945-continuum!) + HUSIČ-botra (z106-matec-PARALELA!) + h49-DUEL (49/40-Kurrent!-X-open) + podpis-Ferdinant-Hoggin-coop + Dezember-blok"},
 {"z":"z95","sken":90,"pag":"85 [konv.-sken−5]","mesec":"Dezember","rojen":"27","krsten":"27","vas":"Griblje","hisna":"78",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Michael Levac[?]-'Lezar'[?]-garble-X-open",
  "matec":"Barbara Skarasič [~SKARASIČ!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Barbara Hlobučar [~KLOBUČAR!]",
  "_opomba":"★★★ BRODARIČ-boter-nit (5/6!) + KLOBUČAR-boter-nit (3/4!) + oče-garble-MAX-X-open + podpis-Ferdinant-Hoggin-coop + h78"},
 {"z":"z99","sken":91,"pag":"86 [konv.-sken−5]","mesec":"Dezember","rojen":"3","krsten":"3","vas":"Griblje","hisna":"3",
  "otrok":"Johann","spol":"moški",
  "ocec":"Peter Hrižan [~HRIŽAN!], ½ Ġ",
  "matec":"Dorothea z.b. Hrižan [~HRIŽAN!]",
  "botra":"Georg Simec [~SIMEC!] + Maria Štumbi[?]-Štumi[?]-garble",
  "_opomba":"★★★ HRIŽAN-DVOJNI-vrstica (oče+matec!-3/5!) + ★★★ SIMEC-boter-nit (3/3-KOMPLET!) + podpis-Franz-DOVGAN + h3 (z98-Goriče-h33-RAZLIČNI!)"},
 {"z":"z101","sken":91,"pag":"86 [konv.-sken−5]","mesec":"Dezember","rojen":"8","krsten":"8","vas":"Griblje","hisna":"34 [DUEL-34/84/94-X-open!]",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Johann Skalaš[?]-'fielah'[?]-garble-X-open, ½ Ġvišt[?]",
  "matec":"Anna z.b. Deblič [~DEBLIČ!]",
  "botra":"Georg Žeflko[?]-Zeflho[?]-garble + Maria Šravič[?]-garble",
  "_opomba":"★★★ DEBLIČ-matec-nit (2/4!) + oče-garble-MAX-X-open + botra-garble-×2-MAX + h34-DUEL (34/84/94-Kurrent!-najverjetneje-34-ista-grafija-kot-z2/z11-Krasine-h34!-X-open) + podpis-Ferdinant-Hoggin-coop"},
 {"z":"z106","sken":92,"pag":"87 [konv.-sken−5]","mesec":"Dezember","rojen":"18","krsten":"18","vas":"Griblje","hisna":"33",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Mathias Deblič [~DEBLIČ!], ½ Ġüble",
  "matec":"Maria Husič [~HUSIČ!]",
  "botra":"Anton Brodarič [~BRODARIČ!] + Anna Pezdire [~PEZDIRC!]",
  "_opomba":"★★★ DEBLIČ-oče-nit (3/4!) + HUSIČ-matec-nit + BRODARIČ-boter-nit (6/6-KOMPLET!) + PEZDIRC-boter-nit (P228-TAIL-ŽE-VLM-s92-1:1-KRIŽ!) + podpis-Ferdinant-Hoggin-coop + h33 (P228-'h33-P227-TAIL-z89-1877-GRIBLJE!')"},
]
assert len(GRIBLJE) == 20

OKVIR = {
 "window": "s78–s92 (15 skenov; s85–s92-proba-P228-LEAD! s78–s84-probe-nazaj! s78-MEJA-ENE-STRANI! s92-tail-P228!)",
 "prenos": "2×-neodvisna-md5-15/15 (s78–s92!-s92-kopija-iz-P228-md5-1:1!)",
 "foliacija": "gola-svinčna-'sken−5'-15/15-SEKVENČNO (s78='73'/s79='74'/s80='75'/s81='76'/s82='77'/s83='78'/s84='79'/s85='80'-LEAD-PREDIKCIJA-POTRJENA!/s86='81'/s87='82'/s88='83'/s89='84'/s90='85'/s91='86'/s92='87'-P228!) — SKUPNA-SERIJA-73–158-continuum!",
 "mejaStart": "s78-ENE-STRANI-MEJA (TAIL-1876-r1-Dobravce-Martin-Dez-24/26-h16-Hržnić[?]/Rus! + glava-'Jahr 1876'! + ★★★ 'Incipit-annus-Domini-1877'-VELIKA-KALLIGRAFIJA-ČEZ-SREDINO-STRANI-1.-INCIPIT-v-krstni-liniji! + glava-'Jahr 1877-Jänner' + RESTART-z1-NA-DAN-9./10.-JÄNNER-Zemelj-h20-Catharina-Škatab[?]/Jurejčič[?]-DUEL!-9.-restart-z1-linija!-P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!-P227-8./9.!-P228-[8↔9]-DUEL!-P229-9./10.!)",
 "mejaKonec": "s92/s93 (P228!-TAIL-1877-z103–z108-Dezember-11–30 + glava-'Jahr 1877'-s92 + RESTART-z1-1878-[8↔9]-JÄNNER!)",
 "rowsTotal": 108,
 "aritmetika": "5+7+8+9+7+8+9+7+8+8+7+6+7+6+6 = 108 = REALNOST (P228-LEAD-'1877-=-91'-NAPAČNA!-predpostavka-tail-'z86–z91'!) — zap-stolpci-VIDNI-×6-strani-1:1 (s78:1–5!-s79:6–12!-s80:13–20!-s81:21–29!-s82:30–36!-s83:37–44!) = NOV-REKORD-POTRDITEV-zap-1:1! — LEAD-KOREKCIJA-9.×-linija (P228-'93'-NA-s98-PARALELA!)",
 "meseci": "J1+F3+M2+A1+Juli1+A3+O2+N3+D5 = 20-Griblje (Juni/Sep-×0!-2-prazne!)",
 "duhovniki": "DVOJNA-IZMENJAVA-1877-'Ferdinand-Hoggin/Hoggja/Roggja-coop'-KURRENT-DUEL-podpis (isti-duhovnik-3-grafični-varianti-X-open!-DOMINANTA-~×30!) ↔ 'Franz-Dovgan' (~×20!-ALTERNIRAJÖČE-čez-celo-leto!) — Griblje-split-HOGGIN-×13/DOVGAN-×7!",
}

stats = {
 "griblje_vpisov": 20,
 "griblje_his": 18,
 "dup": "h6-×2 (z13+z56!-Feb-24-vs-Juli-23!-RAZLIČNI-starši-JAKOFČIČ-vs-KLOBUČAR!) + h14-×2 (z67+z68-DVOJČKI!-isti-starši-1:1!) — vs-P228-h11-×2/h64-×2",
 "pezdirc": "×11-vrstic-continuum-9-let (×4/×4/×6/×4/×9/×14/×12/×17/×11!): Griblje-×7-vrstic (z8-oče-Mathias-Pezdire+botra-Anna-Pezdire-DVOJNI! + z15-boter-Anna-Pezdire! + z25-boter-Peter-Pezdire! + z67/z68-oče-Michael-Pezdure-×2! + z84-oče-Peter-Pezdire! + z89-oče-Pezdič-X-open! + z106-boter-Anna-Pezdire!) + ne-Griblje-×4 (z16-matec-Maria-Pezdire-Krasine! + z18-matec-Maria-Pezdire-Kaplišče! + z23-boter-Maria-Pezdir-Krasine! + z24-matec-Anna-Pezdire-Vranoviče!)",
 "jakofčič": "×11-linij (Griblje: z13-oče! + z15-oče! + z67/z68-boter-Mathias-×2! + z77-matec-Maria! + z85-oče+matec-DVOJNI! + z89-matec! + ne-G: z1-matec-Catharina-Jurejčič/Jakofčič-DUEL! + z31-oče+botra-×2-TRIJNI-Certovišče! + z43-boter-Georg! + z58-boter-Nicolaus!)",
 "milek": "×5 (z8-boter-Johann-Griblje! + z25-oče-Mathias-Griblje! + z34-boter-Maria-Griblje! + z56-matec-Kathar.-Griblje! + z84-boter-Catharina-Griblje!-vse-Griblje!)",
 "deblič": "×4 (z84-matec-Catharina! + z89-boter-Mathias! + z101-matec-Anna! + z106-oče-Mathias!)",
 "brodarič": "×6 (z22-boter-Barbara! + z34-boter-Anton! + z84-boter-Anton! + z94-oče-Anton! + z95-boter-Anton! + z106-boter-Anton!-6/6-Griblje-KOMPLET!)",
 "klobučar": "×4 (z56-oče-Martin-Hlobučar! + z77-boter-Barbara! + z89-boter-Barbara! + z95-boter-Barbara!)",
 "hrižan": "×5 (z15-matec-Maria! + z79-oče-Mathias! + z99-oče+matec-DVOJNI! + ne-G: z38-oče-Johann-Otok! + z9-matec-Catharina-Primostek!)",
 "simec": "×3 (z22-matec-Anna! + z61-boter-Georg! + z99-boter-Georg!-KOMPLET-nit!)",
 "dragoš": "×1 (z85-boter-Anna!-P228-×4-KOMPLET-continuum!)",
 "hure": "×2-neG (z18-oče-Johann-Kaplišče! + z63-boter-Nicolaus-Primostek!-P227/P228-PARALELA!)",
 "hambič": "×4 (z15-boter-Mathias! + z34-oče-Mathias! + z67/z68-boter-Catharina-×2! + z9-matec-Margaretha-Primostek!)",
 "dvojcki": "★★★ ×4-REKORD-LINJE (vs-×3-P227!-×2-P228!): z28/z29-Prilozje-h30-Georg+Marcus-April-9/9-bracket! + z46/z47-Grem-h26-Joannes+Anna-Juni-27/27-bracket-mesec-'Juni'-Kurrent-'Nai/Mai'-DUEL! + z67/z68-GRIBLJE-h14-Barbara+Margaretha-Aug-31/Sep-1-bracket-'Zwillings'-vertikalna-nota! + z75/z76-Krasine-h18-Michael+Martin-Sep-21/22-bracket-†11.3.1939-ink-čez-Michael!",
 "todtgeboren": "★★★ TODTGEBOREN-TIP-garble-×3-REKORD (vs-×1-P228!): z41-Krasine-h11-IME-'Nurlygaburišt'[?]-garble-MAX (botra+duhovnik-PRAZNA!) + z42-Podzemelj-HIŠNA-PRAZNA-IME-'Tuolynbuns'[?]-garble-MAX (mati-X + botra/duhovnik-PRAZNA!) + z65-Kloster-h43-IME-'Nurlygabuništ'[?]-garble-MAX (botra+duhovnik+hebamme-VSI-PRAZNI!) — P228-z28-'Nrbžgabumšt'-1:1-GARBLE-DRUŽINA!",
 "nezakonski": "★★★ ×4-linije (očetov-stolpec-PRAZEN!-vs-×5-P228!): z38-Krasine-h46 (Mai-8/9!-oče-dash-PRAZEN!-matec-Anna-Malešič!) + z43-Certovišče-h14 (Juni-16/17!-oče-PRAZEN!-matec-Barbara-Skarčinič!) + z44-Vranoviče-h20-X-open (Juni-23/24!-samo-matec-Agnes-Hönig!) + z?-Krasine-h46-'al-46'-popravek-nad-hišno!",
 "modri": "★★★ ×9+-linije: z8-'umrla-21.4.1961-gribljskih-št.37'-MATCH-h37! + z13-dolg-'†27.1.1963-Gribljah'+'o.23/1.1910'! + z22-'†20.I.1912-Podgoricah[?]'! + z27-'†15.marja-1959-Novem-mestu-TORONTO-KANADA'-matičar! + z28-'Amor-Anžan-Lav.'-modra-vertikala! + z40-dolg-'†6.12.1960-Gradacu'-MMK! + z43-'†23.12.1953-Letrjači[?]-št.20'-DUEL-1943/1953! + z18-dolg-Kaplišče-MMK-Otok-1964! + tail-z87-'†6.4.1945'-P228!",
 "cnilo_pripisi": "★★★ črnilo-×2-Griblje (z56-'†30.4.19?0'! + z94-'†6.3.1945'-s-križem!) + ★★★ z22-PREČRTANA-VELIKI-X-ČRNILO (ime+'legitimaha-že'+pripis!) + ★★★ OČE-PREČRTAN-SWAP-z22! + ne-G: z2-'†3.1.1931'-Krasine! + z3-'Jannen-an-15.2.1897'+'†19.4.1940'-Škrile! + z32-'†'-vertikalno-čez-IME-Krasine! + z85-'copulatus-in-Zagreb-a-parocho-St.-Blasii-25.6.1916'-Gradac! + z97-'†19/3-1919'-Dragoše! + z79-'†22.2.1937'-Primostek! + z74-'†11.3.1939'-vertikalno-Krasine! + z94-tail-'†6.4.1945'-P228!",
 "posebne": "★★★ November-31-DUEL-×2 (z89-GRIBLJE-h40! + z90-Dragoše-h1!-Nov-31-NE-OBSTAJA-pisarjev-slip-za-Nov-30/Dec-1!-×2-ZAPOREDOMA!) + ★★★ RETRO-VPISI-×2 (z97-z98-Nov-29/30-NA-STRANI-s91-PO-s90-Dec-28/29!-nakadna-dopolnitev-chronologije!-Dragoše-Joannes-†19/3-1919 + Goriče-Nicolaus!) + ★★★ z15-DATUMSKI-DUEL-Feb28→Mar1-GRIBLJE (rojen≠krsten-ČEZ-MESEC!-1877-NON-LEAP!) + 'Incipit-annus-Domini-1877'-KALLIGRAFIJA + HEBAMME-Maria-Rom/Born-×7 (z39/z40/z43/z45/z48/z63/z65-Gradac-Podzemelj-continuum!) + rojen≠krsten-Griblje-×10 (z8-30/31! + z15-28/1! + z25-29/30! + z56-23/24! + z67/z68-31/1-×2! + z77-5/6! + z84-22/23! + z85-23/24! + z89-31/1!) + RED-tički-✓-margin (arhivske!) + z38-'al-46'-popravek-nad-hišno-X-open",
}

out = {"leto": 1877, "griblje_entries": GRIBLJE, "okvir": OKVIR, "stats": stats}
json.dump(out, open(f"{TMP}/entries_1877.json", "w"), ensure_ascii=False, indent=1)
print(f"entries_1877.json: {len(GRIBLJE)}-Griblje-vpisov / 108-DISTINCT / 18-hiš")
