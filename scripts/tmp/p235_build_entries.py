#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P235 — agregacija 17-GRIBLJE-vpisov leta 1871 (krstna PREDZGODOVINA 04104, 15/15 — LINIJA KOMPLETNA!).
★★★ 108-VPISOV-ARITMETIČNI-MODEL (z1–z108!-1:1-SEKVENČNO-10/10-strani!): s3=1–8 (8!-z1-RESTART-13.-restart!-ODPRTJE-ZVEZKA!)
  → s4 = DUPLIKAT-s3 (fol-1-2×!-8-vrstic!-★★★ 1.-DUPLIKAT-KNJIGE-s3=s4-RESITEV-P234-UGE!) → s5=9–19 (11!-POST-DUPLIKAT-z9!)
  → s6=20–30 (11!) → s7=31–41 (11!-z37/z38-PREČRTANI!) → s8=42–52 (11!) → s9=53–64 (12!) → s10=65–74 (10!-z72/z73-DVOJČKI-ZWILLINGE!)
  → s11=75–86 (12!) → s12=87–96 (10!) → s13=97–108 (12!-TAIL-VERIGA-3/3!-z108-TAIL-Dez-31!) = ★★★ 108-DISTINCT-VPISOV
  (116-vrstic-−-8-DUPLIKAT = 108!) — vs-LEAD-'~90–110'-POTRJENO-1:1!
★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s1-vezava!-s2-naslovna-'Tauf-Buch.'!-arhivski-nalepek-'PODZEMELJ-R-1871-1885'-D2!-KNJIGA = 15-LET-LINIJA-1:1!)
★★★ 17-GRIBLJE / 16-hiš (h28-×2-DUEL-z81-vs-z83!-PARALELA-h30-×2-1872!-h37-×2-1873!-3.-leto-vzorec!)
★★★ PEZDIRC-×8 (z81-oče-'Peter-Pezdirc'-EKSPPLICITNO-X-POTRJEN!-+3×-Peter-Pezdirc-z34/z40/z81!-vs-×5-1872!-×8-1873!)
★★★ DUHOVNIKI-1871-EKSTRAHIRANI (1872-X-open-LEKCIJA-UPOŠTEVANA!): Weisel-Cap.-z1–z13 + Jakob?-z14–z19 + Dotto?-z20–z41
  + Feršlan-Pfr.-z42–z52 + Daniel-Wessely-cop.-z98!-(+z53–z64-'Daniel...'-X-open!) + Weisel/Wenzel/Wessely-GARBLE-continuum!
Izhod: /tmp/p235/entries_1871.json"""
import json

TMP = "/tmp/p235"

GRIBLJE = [
 {"z":"z13","sken":5,"pag":"2 [konv.-sken−3]","mesec":"Februar","rojen":"12 [~13-DUEL-X-open!]","krsten":"13","vas":"Griblje","hisna":"24 [~]",
  "otrok":"Katharina","spol":"ženski",
  "ocec":"Matthias Kambič [~KAMBIČ-garble!], ¼ Griblje",
  "matec":"Katharina Brine [~BRINE-continuum-z16!-'Brina'-PARALELA-P234-z99!]",
  "botra":"Matthias Stuhler [~ŠUBLER-garble-PARALELA-P234-z99!] + Bara Brohar [~BRODARIČ-garble!] + rči [?]",
  "_opomba":"★★★ 1.-GRIBLJE-1871 = z13 (Februar!-Jänner-×0-GRIBLJE!-vs-1872-1.-vpis-leta-GRIBLJE-z1!-VZOREC-PREKINJEN!) + BRINE-matec-nit (1/2!-z16!) + BRODARIČ-botra-garble (PARALELA-z77/z80/z95!) + ŠUBLER-garble-continuum + duhovnik-Weisel-Cap. (z1–z13-OBDOBJE!) + rojen-12/13-DUEL-X-open + h24 (PARALELA-1872-z47-h24-PRINC!-×2-v-2-letih!) + zap-13-pozicijsko (s5=9–19!-X-'13'-LAMIM-nota!) + pag-sken−3"},
 {"z":"z16","sken":5,"pag":"2 [konv.-sken−3]","mesec":"Februar","rojen":"21","krsten":"21","vas":"Griblje","hisna":"23 [~]",
  "otrok":"Joanes","spol":"moški",
  "ocec":"Matthias Brine [~BRINE-★★★!-'Brine'-2/2-KOMPLET-z13!], ½ Griblje",
  "matec":"Maria Mihelik [~MILIČ-MILEK?-X-★★★-HIPOTEZA!-'Mihelik'-garble-continuum-MILEK/MILIČ/MIHELIČ!]",
  "botra":"Marko Habai [~garble-'Haba'-DUEL-X-open!] + Maria Uhl [~garble!] + car. [?]",
  "_opomba":"★★★ BRINE-oče-nit (2/2-KOMPLET-z13-matec!) + ★★★ MILIČ-MATEC-'Mihelik'-hipoteza (1/5-MILIČ-nit-linije!-MILEK?-X-open-PARALELA-P234-'Milhoeluc'-z92!) + h23 (NOVA-hiša-linije!) + duhovnik-JAKOB?-zamenjava (z14–z19!-★★★ DUHOVNIŠKA-MEJA-z13/z14-X-open!) + zap-16-pozicijsko + pag-sken−3"},
 {"z":"z18","sken":5,"pag":"2 [konv.-sken−3]","mesec":"Februar","rojen":"25","krsten":"25","vas":"Griblje","hisna":"60",
  "otrok":"Anna","spol":"ženski",
  "ocec":"Georg Schelko [~garble-X-open-'Šelko/Chelko'?], ¼ Griblje",
  "matec":"Catharina Križan [~HRIŽAN-1/9!-'Križan'-garble-continuum!]",
  "botra":"Janez Filak [~garble!] + Margareth Perz [~PERZ-garble!-'Parez'?] + Dire [?]",
  "_opomba":"HRIŽAN-matec-nit (1/9-oseb-1871!-Križan-garble-continuum!) + h60 (PARALELA-1874-z57-h60-FELK!-×2-v-3-letih-RAZLIČNI-družini!) + oče-garble-SCHELKO + botra-garble-×3 + zap-18-pozicijsko + pag-sken−3"},
 {"z":"z25","sken":6,"pag":"3 [konv.-sken−3]","mesec":"März","rojen":"19","krsten":"19","vas":"Griblje","hisna":"5",
  "otrok":"Joseph","spol":"moški",
  "ocec":"Veljan [?] Cvetanec [~CVETANEC-garble-X-open!-'Veljan'-ime-garble!], ½ Göblar",
  "matec":"Maria Klarančič [~KLAR-garble-X-open-'Klarančič/planšič'?-PARALELA-z34-'Klar'!]",
  "botra":"Mathias Logelf [~garble-X-open-'Loger/Luget'?] + Margareta Duttor [~DUTAR-garble!]",
  "_opomba":"★★★ vrstica-ZELO-BLEDA (celost-'slabo-berljiva'!-X-open-×4-polja!) + h5 (NOVA-hiša!) + oče-garble-CVETANEC + matec-garble-KLARANČIČ (KLAR-nit-PARALELA-z34!) + botra-garble-×2 + duhovnik-DOTTO.-EKSPPLICITEN-PODPIS (z20–z41-obdobje!) + zap-25-pozicijsko (s6=20–30!) + pag-sken−3"},
 {"z":"z34","sken":7,"pag":"4 [konv.-sken−3]","mesec":"April","rojen":"18","krsten":"18","vas":"Griblje","hisna":"46",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Marko Klar [?] Juniar [~KLAR-★★★-garble-'Klar/Juniar'-DUEL-X-open!-'planšič'?], ¼ Gribljar",
  "matec":"Katharina Vrblik [~garble-X-open!]",
  "botra":"Peter Pezdirc [~PEZDIRC-X-★★★-EKSPPLICITNO-'Pezdirc'-1/8!-boter!], Neža Struček [~STRUCELJ-garble!] + Jurka [?]",
  "_opomba":"★★★ PEZDIRC-boter-nit-'Peter-Pezdirc' (1/8!-EKSPPLICITNO!-PARALELA-z40/z81-PETER-×3-linije!) + KLAR-oče-garble (PARALELA-z25-matec!) + STRUČELJ-botra-garble-continuum (z92-botra-'Strucelj'!) + h46 (NOVA-hiša!) + duhovnik-idem (continuum-DOTTO?-X-open!) + zap-34-pozicijsko (s7=31–41!) + pag-sken−3"},
 {"z":"z35","sken":7,"pag":"4 [konv.-sken−3]","mesec":"April","rojen":"19","krsten":"19","vas":"Griblje","hisna":"4",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Nicolaus Tomc [~TOMC-garble!-'Toma/Tome'-continuum!], ¼ Gribljar",
  "matec":"Barbara Hermesa [~garble-X-open-'Hermes/Hermašič'?]",
  "botra":"Mathia Toma [~TOMC-2/2!-'Toma'-garble!] + Neža Suričij [~garble-X-open!] + Gribljarji [?]",
  "_opomba":"★★★ †-pripis-'geboren-30.4.1885[?]-+17.6.1939[?]' (X-open-ceLOT-NEBERLJIV!-'geboren'-ANOMALIJA-1871-dete!-poroka?-ALBO-'gehoret'?-★★★ MODRI/RDEČI-pripis-kontekst!) + TOMC-DVOJNI-oče+botra-nit (1/2+2/2-KOMPLET!) + h4 (NOVA-hiša!) + oče-garble-HERMESA + zap-35-X-pozicijsko + pag-sken−3"},
 {"z":"z44","sken":8,"pag":"5 [konv.-sken−3]","mesec":"Mai","rojen":"8","krsten":"9","vas":"Griblje","hisna":"69",
  "otrok":"Mathias","spol":"moški",
  "ocec":"Johann Husič [~HUSIČ-garble-'Flušič'-PARALELA-P234-z61!], ¼ Gübler",
  "matec":"Bara (Barbara) Tribijanovič [~TRIBIJANOVIČ-garble-X-open!]",
  "botra":"Janez Brince [~BRINE-garble-3rd!-'Brince'!] + Anna Petrič [~PETRIČ-garble!] + Ps. [?]",
  "_opomba":"★★★ h69-CONTINUUM (z44-1871!-+ z97-1872!-+ z55-1873!-h69-×3-v-3-letih-★★★ RAZLIČNI-družini-HUSIČ/BORIN!-vs-h40-PEZDIRC-continuum-ISTI!) + rojen≠krsten-8/9 + BRINE-botra-garble (3rd-Brine-vrstica-1871!-z13/z16/z44!) + oče-garble-HUSIČ (PARALELA-P234-z61-'Flušič'!) + matec-garble-TRIBIJANOVIČ + h69 + zap-44-pozicijsko (s8=42–52!) + duhovnik-FERŠLAN-Pfr.-obdobje (z42–z52!) + pag-sken−3"},
 {"z":"z46","sken":8,"pag":"5 [konv.-sken−3]","mesec":"Mai","rojen":"11","krsten":"11","vas":"Griblje","hisna":"12",
  "otrok":"Peter","spol":"moški",
  "ocec":"Joannes Dragoš [~DRAGOŠ-★★★-EKSPPLICITNO!-'Dragoš'-1/6!], ½ Gübler",
  "matec":"Anna Dragoš [~DRAGOŠ-2/6-★★★-DVOJNI-oče+matec-ISTI-priimek!-'kmečka-paralela'-X-open!]",
  "botra":"Peter Jakofčič [~JAKOFČIČ-1/7!], Katharina Jakofčič [~JAKOFČIČ-2/7!-★★★ DVOJNI-boter+botra!] + Laura [?]",
  "_opomba":"★★★ DRAGOŠ-DVOJNI-oče+matec-nit (1/6+2/6!-Griblje-h12!-vs-1872-×3-KOMPLET-PARALELA!-★★★ h12-CONTINUUM-z59-1872-PEZDIRC-'Pegdic'-×2-v-2-letih-RAZLIČNI-družini!) + ★★★ JAKOFČIČ-DVOJNI-boter+botra-nit (1/7+2/7!-+z14/z15/z43/z87!-JAKOFČIČ-REKORD-linije!) + duhovnik-D.-FERŠLAN-Pfr.-EKSPPLICITEN (z42–z52-OBDOBJE!-★★★ 2.-duhovnik-ekspliciten!) + h12 (PARALELA-P233-z94-h41/11!-+h12-1872!) + zap-46-pozicijsko + pag-sken−3"},
 {"z":"z69","sken":10,"pag":"7 [konv.-sken−3]","mesec":"Juli","rojen":"25","krsten":"25","vas":"Griblje","hisna":"1",
  "otrok":"Johann","spol":"moški",
  "ocec":"Nicolaus Zeller [~ZELLER-garble-X-open-'Zellko'?], ¼ Gübler",
  "matec":"Anna Sakofčič [~JAKOFČIČ-3/7-X-★★★-GARBLE-'Sakofčič'-K-S-zmeda!-S-for-J!]",
  "botra":"Peter Sakofčič [~JAKOFČIČ-4/7-garble!] + Catharina Sakofčič [~JAKOFČIČ-5/7-garble!-★★★ SAKOFČIČ-×3-DVOJNI-TROJNI-block!]",
  "_opomba":"★★★ SAKOFČIČ-×3-TROJNI-block (matec+boter+botra-VSE-'Sakofčič'!-★★★ JAKOFČIČ-garble-continuum-'S'-for-'J'-KURRENT!-vs-×5-eksplicitni-1871!) + h1 (PARALELA-1873-z47-h1-JAKOFČIČ-zakonca!-×2-v-2-letih!) + oče-garble-ZELLER + duhovnik-jo.[?]-neberljiv + zap-69-pozicijsko (s10=65–74!-DVOJČKI-stran!) + pag-sken−3"},
 {"z":"z80","sken":11,"pag":"8 [konv.-sken−3]","mesec":"September","rojen":"15","krsten":"15","vas":"Griblje [celost-'Grible'-garble!]","hisna":"48",
  "otrok":"Mathias","spol":"moški",
  "ocec":"Joanes Klobučar [~KLOBUČAR-★★★-EKSPPLICITNO-oče!-'Klobučar'-1/5!-X-POTRJEN-zoom!], ¼ Griblje",
  "matec":"Bara PožJure [~PEZDIRC?-hipoteza-X-★★★-OPEN-'Pez-Jure'-garble!-'Požek-Jure'?-DUEL-X-open!] (Pez Jure)",
  "botra":"Ant. Brodarič [~BRODARIČ-2/5!] + Agn. Stručež [~STRUČELJ-garble-2nd!]",
  "_opomba":"★★★ KLOBUČAR-oče-nit-EKSPPLICITEN (1/5!-X-'Joanes-Klobučar-in-Griblace'-zoom-POTRJEN!-vs-×2-1872!) + ★★★ matec-'Pez-Jure'-PEZDIRC?-hipoteza-X-OPEN (DUEL-'Požek-Jure'-garble!-PEZDIRC-×8-kontekst!-★★★ ne-ločiteljivo-1:1!) + BRODARIČ-boter-nit (2/5!-z77!) + STRUČELJ-botra (2nd!) + h48 (NOVA-hiša!) + zap-80-X-pozicijsko (s11=75–86!-X-'80'-zoom-POTRJEN!) + duhovnik-neberljivi-paraf (s11!) + pag-sken−3"},
 {"z":"z81","sken":11,"pag":"8 [konv.-sken−3]","mesec":"September","rojen":"19","krsten":"19","vas":"Griblje [celost-'Grible'!]","hisna":"28 [~20-DUEL-X-open!]",
  "otrok":"Joanes","spol":"moški",
  "ocec":"Peter Pezdirc [~PEZDIRC-X-★★★-EKSPPLICITNO-'Peter-Pezdirc-in-Griblach'-X-ZOOM-POTRJEN-2/8!-OČE!-'Peter'-×3-linije-z34/z40/z81!], ¼ Griblje",
  "matec":"Katarina Dehlič [~DEBLIČ?-garble-X-★★★-OPEN-'Dehlič'-'Deblič'/'Deblin'-P234-z61-continuum!-'Delič'?-DUEL!]",
  "botra":"Mathe Milič [~MILIČ-2/5!-'Mate'-continuum-z83!] + Katar. Klobučar [~KLOBUČAR-2/5!]",
  "_opomba":"★★★ PEZDIRC-oče-EKSPPLICITEN-'Peter-Pezdirc' (2/8!-X-ZOOM-'Peter-Pezdirc-in-Griblach'-1:1-POTRJEN!-★★★ h28-PETER-PEZDIRC-družina-1871!-vs-1873-'Peter-Ležir'-h40!-vs-1874-'Peter-Pezdirc'-h40!-PETER-PEZDIRC-continuum-linije!) + ★★★ hisna-28/20-DUEL-X-open (celost-'28'-vs-X-'20'!-KURRENT-2/8-zmeda!-h28-×2-DELO-DUEL-z81-vs-z83!-X-open!) + ★★★ DEBLIČ?-matec-garble-'Dehlič' (X-open-continuum-P234-'Deblin'!) + MILIČ-botra-nit (2/5!-z83-ISTI-botra-h28-DUEL-PAIR!) + KLOBUČAR-botra-nit (2/5!-z80-oče!) + h28 + zap-81-X-pozicijsko (X-'81'-'1'-črtica-zoom!) + pag-sken−3"},
 {"z":"z83","sken":11,"pag":"8 [konv.-sken−3]","mesec":"September","rojen":"25","krsten":"25","vas":"Griblje [celost-'Grible'!]","hisna":"28",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Georg Požek [~POŽEK-garble-★★★!-'Požek'-EKSPPLICITEN-matec-'PožJure'-z80-hipoteza-1:1-CONTINUUM!-'Požek'-P223-continuum!], ¼ Griblje",
  "matec":"Anna Kuhar [~KUHAR-garble-'Kuhor'?-PARALELA-1872-z82-'Kuhar'?-X-open!]",
  "botra":"Mate Milič [~MILIČ-3/5!-ISTI-botra-kot-z81!-'Mathe/Mate'-DUEL!] + Mave Krlžan [~HRIŽAN-2/9-garble-'Krlžan/Križan'-X-open!]",
  "_opomba":"★★★ h28-×2-DELO-DUEL (z81-Pezdirc-družina!-vs-z83-Požek-družina!-★★★ RAZLIČNI-družini-PARALELA-h30-×2-1872!-h37-×2-1873!-3.-LETO-VZOREC!-+ X-hisna-z81-20/28!) + ★★★ POŽEK-oče-nit (matec-z80-'PožJure'-continuum-1:1-hipoteza-'Požek-Jure'-OJAČANA!) + MILIČ-botra-nit (3/5!-2×-ISTI-botra-z81/z83-h28-pair!) + HRIŽAN-botra-garble (2/9!) + KUHAR-matec-garble + zap-83-pozicijsko + pag-sken−3"},
 {"z":"z91","sken":12,"pag":"9 [konv.-sken−3]","mesec":"October","rojen":"18","krsten":"— [PRAZNO-X-★★★-totgeboren?-ALBO-nepisan!-X-open!]","vas":"Griblje","hisna":"65",
  "otrok":"Wolfgang [?]/Anton [?] (nečitljivo)","spol":"moški",
  "ocec":"Mathias Milič [~MILIČ-4/5!-'Milič'-oče!-MILEK?-hipoteza-continuum!], ½ Griblcev",
  "matec":"Margar. Klobučan [~KLOBUČAR-3/5-garble-'Klobučan'-continuum!]",
  "botra":"— [PRAZNO!]",
  "_opomba":"★★★ KRSTEN-PRAZNO-'—' (X-★★★-X-open: totgeboren?-ALBO-krst-nepisan?-ALBO-mrtvorojen!-celost-'mrtev/predčasno'-hipoteza!-vs-totgeboren-z30-DRAGOŠE!-★★★ 2.-BREZ-KRSTA-vrstica-1871!) + ★★★ BREZ-BOTER + BREZ-PODPISA (edinstveno-linije!) + MILIČ-oče-nit (4/5!-z96!) + KLOBUČAN-matec-garble (3/5!) + h65 (NOVA-hiša!) + zap-91-pozicijsko (s12=87–96!) + pag-sken−3"},
 {"z":"z92","sken":12,"pag":"9 [konv.-sken−3]","mesec":"October","rojen":"20","krsten":"20","vas":"Griblje","hisna":"72",
  "otrok":"Nicolaus","spol":"moški",
  "ocec":"Marcus Straus [~STRAUS-garble-'Straus/Stras'-continuum-P234-z90-'Straus'?-X-open!], ¼ Gübler",
  "matec":"Katharina Dragaš [~DRAGOŠ-3/6-garble-'Dragaš'!-DRAGOŠ-continuum!]",
  "botra":"Mathias Strucelj [~STRUČELJ-3rd!-'Sennan[?]'-nota!] + Maria Dragoš [~DRAGOŠ-4/6!-'Maria-Drags'!]",
  "_opomba":"★★★ skupni-PODPIS-med-vrsticama-92/93-'Wilhelm-Wenzel[?]-Coop.' (X-★★★!-WEISEL/WENZEL/WESSELY-garble-continuum!-★★★ isti-kaplan-kot-z1–z13-LAHKO!-X-open-★★★!) + DRAGOŠ-matec+botra-nit (3/6+4/6!-z46-DVOJNI!) + STRUČELJ-botra-nit (3rd!-z34-z80!) + oče-garble-STRAUS + h72 (NOVA-hiša!) + zap-92-pozicijsko + pag-sken−3"},
 {"z":"z96","sken":12,"pag":"9 [konv.-sken−3]","mesec":"November","rojen":"15","krsten":"15","vas":"Griblje","hisna":"26 [?]",
  "otrok":"Johann","spol":"moški",
  "ocec":"Johann Milič [~MILIČ-5/5-KOMPLET!-'Milič'-oče!-MILEK?-hipoteza-continuum-z91!], ¼ Griblcev",
  "matec":"Maria Trničan [~garble-X-open-'Frižan'?-DUEL-X-open!-'Trnikar'?]",
  "botra":"Marko Tiček [~garble-X-open!] + Mare Stuler [~ŠTLER-garble-'Stuhler'-continuum-z13!]",
  "_opomba":"★★★ MILIČ-oče-nit-KOMPLET (5/5!-z16-matec-'Mihelik'-hipoteza!-z81/z83-boter!-z91-oče!-z96-oče!-★★★ MILIČ-×5-oseb-1871-REKORD-linije!-MILEK?-X-open-continuum-P234-'Milhoeluc'!) + matec-garble-TRNIČAN (DUEL-'Frižan'-X-open!) + botra-garble-ŠTLER (continuum!) + h26 [?] (NOVA-hiša!-X-neberljiv!) + duhovnik-Jo.-garble + zap-96-pozicijsko + pag-sken−3"},
 {"z":"z98","sken":13,"pag":"10 [konv.-sken−3]","mesec":"November","rojen":"25","krsten":"25","vas":"Griblje","hisna":"6",
  "otrok":"Maria","spol":"ženski",
  "ocec":"Matthias Sakotovič [~JAKOFČIČ-6/7-X-★★★-GARBLE-'Sakotovič/Sakafvič'-K-S-zmeda-continuum-z69!], ¼ Griblje",
  "matec":"Anna Želko [~ŽELKO-garble-X-open-'Železko'?-PARALELA-1872-z61-'Husič'?-X-open!]",
  "botra":"Janez Žinič [~garble-X-open!] + Anna Dragoš [~DRAGOŠ-5/6-X-'Anna-Dragos'-hipoteza!]",
  "_opomba":"★★★ TAIL-VERIGA-z98 (X-★★★-'98'-1:1-POTRJEN!-s13-r2!-GRIBLJE-v-TAIL!) + JAKOFČIČ-garble-'Sakotovič'-oče (6/7!-SAK-garble-continuum-z69-×3!) + DRAGOŠ-botra-nit (5/6!-X-open-hipoteza!) + h6 (PARALELA-1872-z63-h6/61-PEZDIRC-×2!-×2-v-2-letih!) + duhovnik-DANIEL-WESSELY-cop.-EKSPPLICITEN (★★★ 3.-ekspliciten-duhovnik!-WEISEL/WESSELY-garble-X-open-ista-oseba?!) + h6 + zap-98-X-pozicijsko (s13=97–108!) + pag-sken−3"},
 {"z":"z103","sken":13,"pag":"10 [konv.-sken−3]","mesec":"Dezember","rojen":"22","krsten":"22","vas":"Griblje","hisna":"10",
  "otrok":"Barbara","spol":"ženski",
  "ocec":"Simon Kuke [~KUKE-garble-X-open-'Kukar'?-'Kukej'-botra-continuum!], ¼ Griblje",
  "matec":"Anna Skala [~ŠKALA-garble-continuum-'Skala'-PARALELA-z79!-'Skallič'-z89?]",
  "botra":"Janez Tabrič [~garble-X-open-'Grabrian'-PARALELA-z14-'Grabrian'!] + Magdalena Kukej [~KUKE-2/2-KOMPLET-'Kukej'-garble!]",
  "_opomba":"★★★ TAIL-1871 = z108 (z103 = pred-tail-GRIBLJE!-s13-r7!-Dez-22!) + KUKE-DVOJNI-oče+botra-nit (1/2+2/2-KOMPLET!-'Kuke/Kukej'-garble!) + ŠKALA-matec-garble-continuum + botra-garble-TABRIČ (PARALELA-z14-'Grabrian'-garble-continuum!) + h10 (NOVA-hiša!) + duhovnik-'Po (ista-roka)'-garble (continuum-z98-Wessely?-X-open!) + zap-103-pozicijsko + pag-sken−3"},
]
assert len(GRIBLJE) == 17

OKVIR = {
 "window": "s3–s13 (11 skenov-ODPRTJE-KNJIGE!-s1-vezava-0-vrstic!-s2-naslovna-'Tauf-Buch.'-0-vrstic!-arhivski-nalepek-'PODZEMELJ-R-1871-1885'!-s3–s13-'Jahr 1871'-11/11-glave!-s14-ŽE-1872-z1-P234!-11-skenov-DESCENDING-probe-P234-LEAD-nadgrajeno-s9–s13→s3–s13!)",
 "prenos": "2×-neodvisna-md5-14/14 (s1–s14-fresh-fetch!-inventar-200!)",
 "foliacija": "★★★ 'sken−3'-KOMPLETNA-FORMULA-KNJIGE-s3–s14 (s3='1'!-s4='1'-★★★ DUPLIKAT!-s5='2'-s6='3'-s7='4'-s8='5'-s9='6'-s10='7'-s11='8'-s12='9'-s13='10'!-s14='11'-P234!-★★★ 12/12-visoko+srednje!-SKOK-NA-DUPLIKATU-s4→s5-'1'→'2'-PARALELA-s29→s30-'25'→'27'-P234!-2-DUPLIKATA-KNJIGE: s3=s4-fol-1-★★★-RESITEV + s28=s29-fol-25-P234!)",
 "mejaStart": "★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s2/s3!-EDINSTVENO-LINIJE!): s1 = vezava/marmorirana-platnica (0-vrstic!) + s2 = tiskana-naslovna-'Tauf-Buch.'-fraktura (0-vrstic!-+ ARHIVSKI-NALEPEK-'PODZEMELJ-R-1871-1885'-★★★-1:1-15-LET-LINIJA-KNJIGA!) + s3-r1 = z1-RESTART-Jänner-3-KRASINEC-h27-Joanes-Zupanič (★★★ 13.-restart-z1-linije!-1.-vpis-leta = KRASINEC-NOT-GRIBLJE!-vs-1872-GRIBLJE-z1!-VZOREC-1.-VPISA-PREKINJEN!-X-'1'-kontrola!)",
 "mejaKonec": "★★★ MEJA-1871/72 = s13/s14-PAGE-BOUNDARY (P234-POTRJENA-1:1!-re-use!): s13-TAIL = z108-Dez-31-Otok-h31-Maria (TAIL-VERIGA-'97–108'-3/3-X-potrjena!-12-vrstic!-zaključni-vlakanci-+ rdeča-valovita-črta!-BREZ-'finis-Anni-1871'-kalligrafije-Q4-5/5-negativno!-1871-končan-plain-PARALELA-1872!) + s14-r1 = z1-Jänner-5-GRIBLJE-h11 (restart-12.-restart-P234-SUPER!)",
 "rowsTotal": 108,
 "aritmetika": "★★★ 108-VPISOV-ARITMETIČNI-MODEL (z1–z108!-SEKVENČNO-1:1-10/10-strani-celost-branja-POPOLNO!): s3=1–8 (8!-z1-RESTART-13.!-ODPRTJE!) + [s4=DUPLIKAT-s3-fol-1-8-vrstic!] + s5=9–19 (11!-z9-POST-DUPLIKAT-X!) + s6=20–30 (11!-z25!) + s7=31–41 (11!-z34/z35!-z37/z38-PREČRTANI!) + s8=42–52 (11!-z44/z46!) + s9=53–64 (12!-probe-zap-35!-celost-1:1!) + s10=65–74 (10!-z69!-z72/z73-DVOJČKI-ZWILLINGE!) + s11=75–86 (12!-z80/z81/z83-X!) + s12=87–96 (10!-z91/z92/z96!) + s13=97–108 (12!-z98/z103!-TAIL-VERIGA-3/3!) = ★★★ 116-vrstic-total − 8-DUPLIKAT-s4 = 108-DISTINCT-VPISOV (z1–z108!) — vs-LEAD-'~90–110'-POTRJENO-1:1 (108!-★★★ celost-zap-branja-1–108-SEKVENČNO-BREZ-NAPAK-1:1!)",
 "meseci": "F3(z13-z16-z18!)+M1(z25!)+A2(z34-z35!)+Mai2(z44-z46!)+J3-1(z69!-Juli!)+Sep3(z80-z81-z83!)+O2(z91-z92!)+N2(z96-z98!)+D1(z103!) = 17-Griblje (★★★ JÄNNER-×0-+ JUNI-×0-GRIBLJE-2-PRAZNA-MESECA-1871!-vs-1872-1-prazen-Sep!-vs-1873-4-prazni!-vs-1874-BREZ!)",
 "duhovniki": "★★★ DUHOVNIKI-1871-EKSTRAHIRANI-1:1 (1872-X-open-LEKCIJA-UPOŠTEVANA!-ločilni-R-zoom!): Wilhelm-Weisel-'D.H.-Cap.'-z1–z13 (s3-s5!-'M.R.-Cap.'-garble!) + Jakob?-z14–z19 ('Jakbe'-garble!-DUHOVNIŠKA-MEJA-z13/z14!) + Dotto.-z20–z41 ('Dotto.'-ekspliciten-z25!-idem-z34/z35-continuum!) + D.-Feršlan-'Pfr.'-z42–z52 (ekspliciten-z46!) + Daniel?-z53–z64 ('le-dva-jasnejša-Daniel'-s9!-X-open!) + neberljivi-paraf-s11 (z75–z86!) + Wilhelm-Wenzel?-Coop.-z92/93 (skupni-podpis!-garble-continuum!) + Jo.-z96 + Daniel-Wessely-'cop.'-z98 (ekspliciten!-★★★ WEISEL/WENZEL/WESSELY-garble-continuum-ista-oseba?-X-open-★★★!) + 'Po-ista-roka'-z103 — ★★★ ≥4-eksplicitna-imena (Weisel + Dotto + Feršlan + Wessely!) + Jakob?-garble = PENT?-X-open (vs-1872-X-open!-vs-1873-PENT!)",
}

stats = {
 "griblje_vpisov": 17,
 "griblje_his": 16,
 "dup": "h28-×2-DUEL (z81-'28[~20-DUEL]'-Peter-Pezdirc-družina! + z83-'28'-Georg-Požek-družina!-★★★ RAZLIČNI-družini!-X-hisna-z81-20/28!-3.-LETO-VZOREC: h30-×2-1872!-h37-×2-1873!)",
 "pezdirc": "★★★ ×8-1871 (vs-×5-1872!-×8-1873!-X-★★★-z81-oče-'Peter-Pezdirc'-EKSPPLICITNO-X-ZOOM-POTRJEN!): z32-matec-'Maria-Pezdirc'-Kapljišče + z32-botra-'Švure-Pezdirc'[?] + z34-boter-'Peter-Pezdirc'-h46 + z40-boter-'Peter-Pezdirc'-h16 + z81-oče-'Peter-Pezdirc'-h28-X-★★★-POTRJEN + z84-matec-'Maria-Petdirc' + z84-boter-'Mioha-Petdirc' + z88-boter-'Peter-Seždirič'[?]-garble + z80-matec-'Pez-Jure'-hipoteza-X-open — grafija-continuum: Pezdirc/Petdirc/Pevdire/Seždirič/Pez-Jure — ★★★ 'Peter'-×3-PEZDIRC-linije (z34-z40-z81!-vs-'Peter-Ležir/Perdisek'-1873/74!)",
 "milič": "★★★ ×5-oseb-MILIČ-nit-REKORD (MILEK?-hipoteza-X-open-continuum-P234-'Milhoeluc'!): z16-matec-'Maria-Mihelik'? + z81-boter-'Mathe-Milič' + z83-boter-'Mate-Milič'-2×-ISTI-botra-h28-pair! + z91-oče-'Mathias-Milič'-h65 + z96-oče-'Johann-Milič'-h26 — grafo-continuum: Mihelik/Milič/MILEK?/MIHELIČ!-vs-×1-1872!",
 "klobučar": "★★★ ×5-KOMPLET-ish (z80-oče-'Joanes-Klobučar'-X-POTRJEN! + z81-botra-'Katar.-Klobučar' + z91-matec-'Margar.-Klobučan' + z95-matec-'Anna-Klobučan' + (z44?no) — 'Klobučan'-garble-continuum!-vs-×2-1872!-vs-×1-1873!)",
 "jakofčič": "★★★ ×7-eksplicitni + ×4-SAKOFČIČ-garble = ×11-ish-REKORD-LINIJE (z14-oče-Peter + z14-botra-Bara + z15-oče-Georg + z15-matec-Anna + z43-oče-Nikolaus + z46-boter+botra-Peter+Katharina-DVOJNI + z87-boter-Michael[?] + SAKOFČIČ-×3-TROJNI-z69 (Anna+Peter+Catharina!) + z98-oče-'Sakotovič' — grafo-continuum: Jakofčič/Sakofčič/Sakotovič-'S'-for-'J'!-vs-×5-1873!-vs-×2-1872!)",
 "dragoš": "★★★ ×6-oseb (z46-oče-Joannes! + z46-matec-Anna!-★★★ DVOJNI-oče+matec-ISTI-priimek-Griblje-h12! + z87-oče-Nicolaus-Dragoše + z92-matec-'Dragaš' + z92-botra-'Maria-Dragoš' + z95-oče-Matija-Dragoše + z98-botra-'Anna-Dragos'[?]-hipoteza — vs-×3-KOMPLET-1872/1873!)",
 "hrižan": "★★★ ×9-oseb-REKORD (z9-boter-'Peter-Križan'-Otok + z12-oče-'Peter-Križan'-½-Griblje-Otok-h20 + z18-matec-'Catharina-Križan'-h60 + z54-matec-'Katharina-Križanič' + z54-boter-'Johann-Križan' + z83-botra-'Mave-Krlžan'[?] + z101-botra-'Niko-Kricžan' + z108-botra-'Niko-Kricžan'-2×-ISTI! — grafo-continuum-Križan/Križanič/Krlžan/Kricžan!-vs-×5-1872!)",
 "brodarič": "★★★ ×5 (z7-matec-'Katarina-Brodarič'-s3! + z77-boter-'Miko-Brodarič' + z80-boter-'Ant.-Brodarič' + z95-boter-'Anton-Brodarič' + z13-botra-'Bara-Brohar'-garble! — vs-×2-1872!-vs-×6-1873!)",
 "modri": "★★★ ×3-arhivski-pripisi-1871 (z20-'umrl-20.12.1957-v-Dolnji...'-★★★ 1957-NAJNOVEJŠI-DATUM-LINIJE!-vijolični! + z57-'smrt-1940'-modri + z68-'smrt-1953'-modri-črnilni!-vs-×4-1872!-razpon-1940–1957!) + †-pripisa-z32/z35 (rdeči-črnilni!-z35-'geboren-1885?-+1939?-X-open-ceLOT-neberljiv!)",
 "nezakonski": "★ ×1 (z29-oče-PRAZNO!-Gradac-h49-April-1/2-Anna-matec-Katharina-Beznik!-PARALELA-×1-1873!-vs-×0-1872!)",
 "posebne": "★★★ 108-VPISOV-ARITMETIČNI-MODEL-1:1 (116-−-8-DUPLIKAT!-SEKVENČNO-10/10!-TAIL-VERIGA-3/3!) + ★★★ MEJA-1870/71 = ZAČETEK-KNJIGE (s1-vezava!-s2-naslovna!-nalepek-'PODZEMELJ-R-1871-1885'!-KNJIGA = 15-LET-LINIJA-1:1!) + ★★★ DUPLIKAT-s3 = s4-RESITEV (P234-'1-DUPLIKAT-s1–s13'-UGE-REŠENA!-fol-1-2×!-2.-DUPLIKAT-KNJIGE-za-s28=s29!-SKOK-s4→s5!) + ★★★ 13.-RESTART-z1-NA-s3-r1 (ODPRTJE-ZVEZKA!-1.-vpis-leta = KRASINEC-NOT-GRIBLJE!-VZOREC-PREKINJEN!) + ★★★ z72/z73-DVOJČKI-'Zwillinge'-pripis-X-POTRJEN (Boršt-h20!-Georg+Catharina!-1.-DVOJČKI-linije!) + ★★★ z37/z38-PREČRTANI-DVOJNI (Krasinec-h12!-Harasinič!-April-22!-vijugasta-črta!-mrtvorojeni-dvojčki?-X-open!-vs-P234-1-prečrtana-kopija!) + z30-TOTGEBOREN (Dragoše!-krsten-'—'!) + z91-KRSTEN-PRAZNO-'—'-BREZ-botra-BREZ-podpisa (Griblje-h65!-MILIČ!-X-open!) + ★★★ DUHOVNIKI-1871-EKSTRAHIRANI (Weisel/Dotto/Feršlan/Wessely-4-eksplicitnih!-WEISEL/WENZEL/WESSELY-garble!) + ★★★ 2-PRAZNA-MESECA-GRIBLJE (Jänner + Juni!) + PEZDIRC-×8-'Peter'-×3 + MILIČ-×5-REKORD + JAKOFČIČ-×11-ish-REKORD (SAKOFČIČ-garble!) + HRIŽAN-×9-REKORD + KLOBUČAR-×5 + BRODARIČ-×5 + DRAGOŠ-×6-DVOJNI-z46 + MODRI-×3-1957! + NEZ-×1 + h28-×2-DUEL-3.-LETO + h69-×3-continuum + h12-continuum-DRAGOŠ→PEZDIRC + rdeči-tički-continuum-'Lamim'-noty",
}

out = {"leto": 1871, "griblje_entries": GRIBLJE, "okvir": OKVIR, "stats": stats}
json.dump(out, open(f"{TMP}/entries_1871.json", "w"), ensure_ascii=False, indent=1)
print(f"entries_1871.json: {len(GRIBLJE)}-Griblje-vpisov / 108-DISTINCT-VPISOV / 16-hiš (h28-×2-DUEL)")
