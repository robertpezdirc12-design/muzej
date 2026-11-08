#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P227 — dokaz parish-baptism-1879-04104.json (krstna PREDZGODOVINA 7/15!)."""
import json, os

TMP = "/tmp/p227"
E = json.load(open(f"{TMP}/entries_1879.json"))

grib = E["griblje_entries"]
okvir = E["okvir"]
st = E["stats"]

anomalije = [
 {"id": "meja-1878-79-s105-s106", "opis": "★★★ MEJA-1878/79 = s105/s106 (66.-POTRDITEV-invariante, 65.-P226!): s106 = TAIL-1878 (z90–z94-Dez-23–30-×5: z90-Cerkvišče + z91-Krivoglavce-†3.1.1932 + z92-Dobravie + z93-Krasinea-†9/879 + z94-Germ) + VSOTNA-RAZPETA-'1 8'+'79' (RAZPETA-ČEZ-OBE-STRANI!-'1 8'-leva + '79'-desna!) + glava-'Jahr 1878'-s-popravo-cifre (8-čez-X-open!) + RESTART-z1-NA-DAN-8./9.-JÄNNER-Kloster-h37-Maria-†19.7.1942-MODRI!-7.-restart-z1-NAJPONEJŠI-LINIJE (P221-1.1!-P222-1.1!-P223-4.1!-P224-2.1!-P225-1.1!-P226-3.1!)"},
 {"id": "restart-z1-najponejši", "opis": "★★★ RESTART-z1-NA-DAN-8./9.-JÄNNER-NAJPONEJŠI-v-liniji (rojen-8 + krsten-9!-prestavitev!) — z1 = Kloster-h37-Maria (oče-Jozef-Hočevar!-MODRI-'†-19.7.1942'!) + z2-NA-DAN-8/9-GRIBLJE-h31-Mathias!"},
 {"id": "vrstna-aritmetika-96", "opis": "★★★ 96-VPIISOV-DISTINCT — ŠTEVJE-IZ-VRSTIC-7.× (z1–z96; vrstna-aritmetika 2+8+7+7+6+6+7+8+8+9+8+7+8+5 = 96 = P226-LEAD-'1879-=-96-vpisov-BONUS'-1:1-INVARIANTA! — zap-stolpci-14/14-ČISTO!)"},
 {"id": "foliacija-sken-6-14-14", "opis": "★★★ FOLIACIJA-'sken−6'-14/14-SEKVENČNO-BREZ-LUKNJE (100–113!): s106='100'/s107='101'/s108='102'/s109='103'/s110='104'/s111='105'/s112='106'-LEAD-PREDICTION-POTRJENA!/s113='107'/s114='108'/s115='109'/s116='110'/s117='111'/s118='112'/s119='113'-P226! — SKUPNA-SERIJA-100–158 (1879+1880-P226+1881-P225+1882-P224+LUKNJA-'158'+1883-'sken−5'!)"},
 {"id": "dueli-his-MAX-krop", "opis": "★★★ HIŠNE-VIZUALNE-REŠITVE-DUELOV-×3-MAX-krop (12×-zoom!): z33-'49'-REŠEN ('4'-odprta-Kurrent-forma-NE-'1'-vs-referenca-'15'/'17'-ravni-1!) + z61-'22'-REŠEN (dva-ista-2-glifya!-z22-h22!) + z69-'17'-REŠEN ('17'-1+γ-7-JASNO!-z28-h17!) — 22-GRIBLJE / 19-hiš (h31-×2: z2+z91! + h22-×2: z22+z61! + h17-×2: z28+z69!)"},
 {"id": "dvojcki-zwillinge-x3", "opis": "★★★ DVOJČKI-ZWILLINGE-×3-REKORD-LINJE (vs-×1-P223 + ×1-P226!): z47/48-Dorothea+Margaretha (Krasinec-h43-August-29/29!) + z55/56-Katharina+Barbara (Krasinec-h32-August-14/14!-+MODRI-'†-7.11.1953'!) + z65/66-Martin+todtgeboren (Zemelj-h24-September-23!) — VSE-TRI-v-eni-vrstici-z-DVEMA-zap-številkama + pisarjeva-'Zwillinge'-vertikalna-anotacija + zavit-oklepaj!"},
 {"id": "todtgeboren-x3", "opis": "★★★ TODTGEBOREN-garble-×3 (Mißgeburt-TIP-P226-z76/z77-PARALELA!): z15 (Vranoviče-h21-März-9/—-oče-Markus-Kralj!-¼-Güblm-matec-Christina-Oberlin[?]) + z57 (Prilozye-h35-16/—-oče-Jane-Klepec[?]-matec-Margaretha-Berkšpec[?]) + z66 (Zemelj-h24-23/—-DVOJČEK-z65-Martin!-isti-starši-Nikolaus-Mue + Anna-Papič!) — garble-'…blyaborn'-≈-'todtgeboren' (MAX-krop-potrjeno-z57!) — krsten+botra+duhovnik-VSI-PRAZNI!"},
 {"id": "nezakonski-x2", "opis": "★★★ NEZAKONSKI-×2 (očetov-stolpec-PRAZEN!): z23-GRIBLJE-h24 (April-19/20!-matec-Anna-Filaš-Križan-garble-¼-K.Jokčon!-P226-z114-PARALELA!) + z86-Certoviše-h9 (November-10/10!-matec-Katharina-Jaklič!-botra-Peter-Gabrijan + Anna-Subler!)"},
 {"id": "modri-pripisi-x12", "opis": "★★★ MODRI-MATIČARSKI-PRIPISI-×12-REKORD-LINJE (vs-×9-P226!): ×7-Griblje (z13-'Umrla-dne-25.4.1949-Gospje-št.16'! + z21-'umrl-dne-30.12.1953-v-gostilni-št.3'! + z30-'umrla-19.9.1960-Griblje'! + z39-'Umrla-dne-10.5.1962-v-Gribljah-št.65'-DOLG-+'Dorothea'-dopisano! + z63-'†-7.5.1945-v-Partizanini-v-Podzemlji'! + z74-'umrla-dne-20.1.1939-v-Zemeljem-št.4'! + z91-'umrl-dne-15.11.1965-v-Permanontie-št.17'!) + ×5-ne-Griblje (z35-'Umrla-dne-22.6.1961-v-Zg.-Volčina'-DOLG-'Gradec-22.12.1975'-uradniški-podpis! + z41-Krasinec-'umrl-v-Ljubljani-1950'-X-open + z55-Krasinec-'†-7.11.1953-v-Horjulnem-št.92' + z64-Primostek-'umrla-dne-21.6.1955-v-Drčlrog-št.1' + z79-Begunja-vas-'Umel-dne-1.1969'-DOLG-'Gradec-dne-10.3.1969-duhovnik'!) — 1939–1969-razpon!"},
 {"id": "duhovniska-izmenjava", "opis": "★★★ DUHOVNIŠKA-IZMENJAVA-1879-'Franz/Franc-Janičar-coep' ↔ 'Franz-Dovgan'-ALTERNIRAJOČE-čez-celo-leto (X-open-po-VIZUALNO-branju!-podpisi-krop-×9!): Griblje-split-11/22 (Dovgan: z21/z23/z30/z33/z39/z49/z61/z63/z69/z78/z95! + Janičar: ostali!) — vs-1880-ČISTA-menjava-okoli-z106-P226! + z60-pripis-'B.Dog'-iniciale (Dovgan!) + PARALELA-P222/P223-'coep'-forma!"},
 {"id": "z60-pogojni-krst", "opis": "★★★ Z60-POGOJNI-KRST-1.-LINIJE (Vranoviče-h32-Daniel-August-23/23!-oče-Daniel-Sliva[?]-garble-matec-Ina-Pedire-PEZDIRC!): pripis-čez-gender-stolpce-'Richtiglubem[?]-…-sub-conditione-…-die-27.-Augusti-1879-B.Dog' (iniciale-Dovgan!) — kondicionalni-ritus-4-dnevi-po-krstu!"},
 {"id": "z32-imenski-popravek", "opis": "★★★ Z32-IMENSKI-POPRAVEK (Primostek-h9[✗!]-Anna-13/13!-oče-Josef-Muc-¼-Wörder-garble-matec-Katharina-Križan!): ime-'Anna'-→-prečrtano-'Johann'-→-'Anna'-ponovno-pod-popravkom! + ✗-X-križ-pred-hišno-številko-9! — P226-z100-'Alois→Alojzija'-PARALELA!-botra-'vľ'-kratica!"},
 {"id": "z76-datumski-pripis", "opis": "★★★ Z76-DATUMSKI-PRIPIS (Gradec-h4-Anna-September-15/15!-oče-Peter-Jranzeth-garble): pripis-pod-ime-'…-gebären-am-[21~26].-Decemb-1879'-X-open (dan-DUEL-21↔26!) — DECEMBERSKI-datum-pod-SEPTEMBER-vpiso! — Z49-'den-17.-Juli-1880-zuzschreiben'-P226-PARALELA-X-open (namen-otvorjen!)"},
 {"id": "hebamme-x4", "opis": "Z42-HEBAMME (Podzemelj-h7-Daniel-10/13-3-dnevi!-oče-Johann-Barle-matec-Johanna-Bernič!): 'Die-beistehende-Hebamme'-Maria-Rom-v-Hebamme-stolpcu! + Maria-Rom-še-×3 (z25-Gradec! + z46-Gradec! + z52-Gradec!-+z75-_podpis_) — NOTOCHRST-vzorec!"},
 {"id": "glave-s-popravami", "opis": "GLAVE-S-POPRAVAMI-CIFER-×2 (X-open): s106-'Jahr 1878'-8-s-popravo + s119-'Jahr 1879'-9-čez-7-(X-open-črkovno!-MAX-krop!) — pisar-2×-popravljal-letnice-glav!"},
]
cross = [
 {"id": "x-pezdirc-continuum", "opis": "PEZDIRC-grafija-continuum-7-let (P221-×4/P222-×4/P223-×6/P224-×4/P225-×9/P226-×14/P227-×12-vrstic!): z22-matec-Maria-Perdiče + z91-matec-Katharina-Pedirc + z95-oče-Johann-Pezdirc (in-Griblje!-incl.-'†-15.6.1941'!) + z23/z78-botra-X-open + ×7-ne-Griblje (z26-boter-Mark-Pedire! + z51-matec+botra-DVOJNI! + z58-oče-Peter-Pezdiče! + z60-matec-Ina-Pedire! + z67-matec+boter-DVOJNI! + z70-boter-Joh-Pedirc! + z82-botra-Maria-Poždire!)"},
 {"id": "x-milek-komplet", "opis": "MILEK-×6-vrstic (z20-matec! + z22-oče+boter-DVOJNI! + z49-matec! + z63-botra! + z78-oče! + z92-boter!) — KOMPLET-nit-6/6 (vs-P226-×4!)"},
 {"id": "x-jakofcic-5", "opis": "JAKOFČIČ-×5-in-Griblje (z21-oče! + z28-matec+botra-DVOJNI! + z44-botra-×2-DVOJNI! + z49-botra! + z85-boter!) + ×3-ne-G (z29-Certoviše-TRI-Jakofčič-v-vrstici!-oče-garble-Jakoše + botra-Georg + Barbara-Jakofčič!) — vs-P226-×10"},
 {"id": "x-simec-brodaric-komplet", "opis": "SIMEC-×3-KOMPLET (z20-oče! + z33-boter-Mike! + z85-botra-Anna!) + BRODARIČ-×3-KOMPLET (z2-matec-Maria! + z63-botra-Barbara! + z74-boter-Anton!) — obe-KOMPLET-niti (vs-P226-SIMEC-×3!-BRODARIČ-×4!)"},
 {"id": "x-klobucar-5", "opis": "KLOBUČAR-×5-X-open-heavy (z39-matec-Hlobuar + botra-Klobucar! + z49-oče-Martinus-Hlobučar! + z69-oče-Peter-Hlobučar! + z74-botra-Barb-Klobučar! + z78-botra-Anna-Klobučar! + z92-botra-Barbara-Hlobučar!) — P226-z10-Klebučar-nit-continuum!"},
 {"id": "x-hure-dragos", "opis": "HURE-×2 (z63-oče-Anton!-P226-z88-PARALELA! + z92-botra-Barbara-Hure-X-open!) + DRAGOŠ-×2-matec-garble-X-open (z61-Dragot! + z85-Dragot-Dragoš!)"},
 {"id": "x-križan-4", "opis": "KRIŽAN-×4-in-Griblje (z13-botra-Mathias + Dorothea-DVOJNI! + z23-matec-Anna-garble! + z44-matec-Maria! + z63-matec-Barbara!) — vs-×9-P226-REKORD"},
 {"id": "x-paradele", "opis": "Hišne-paralele: h68-P223-DVOJČKI-GRIBLJE! + h44-P226-z104! + h7-P226-z58-TOTER! + h62-P224! + h63-P226-neG! + h37-PARALELA-z1-Kloster! + h11-P226-restart-Dobravce! + h28-P226! + h24-P223! + h17-PARALELA-hiš-17-v-1880! + h22/h31/h17-×2-v-lastnem-letu!"},
 {"id": "x-notochrst", "opis": "rojen≠krsten-×9-vzorec (z2-8/9 + z21-13/14 + z23-19/20 + z28-10/13-3-dnevi! + z42-10/13-HEBAMME! + z61... — vs-1880-×2!) + HEBAMME-Maria-Rom-×4 (z25/z42/z46/z52-+z75!)"},
 {"id": "x-z1-z2-stran", "opis": "RESTART-STRAN-s106: z1-Kloster-h37-Maria-†19.7.1942-MODRI (oče-Jozef-Hočevar-Cajin + matec-Agnes-Pibl-garble!-botra-Mart-Frans + Catharina-Maucžl-garble-+Hebamme-Maria-Rom!) + z2-GRIBLJE-h31-Mathias — 2-vpisa-na-meji!"},
 {"id": "x-s119-tail", "opis": "TAIL-1879-s119 (P226-ŽE-VLM!): z92-GRIBLJE-h28-Anna (oče-Georg-Pižek-garble!-matec-Margareth-Hribar-garble!-botra-Mathias-Milek + Barbara-Hure-X-open!) + z93-Otok-h31 + z94-Gradec-h6 + z95-GRIBLJE-h40-Josef-PEZDIRC-'†-15.6.1941' (oče-Johann-Pezdirc-¼-Güblm!-matec-Anna-Jallopič-garble!-botra-Mathias-Duflič + Barbara-Hlobučar!-podpis-DOVGAN!) + z96-Dragoviě-h4 + Schnörkel + 'Jahr 1879'-BREZ-VSOTNE!"},
]
honesty = [
 {"id": "h-garble-očeta-MAX", "opis": "OČE-garble-MAX-X-open-×6 (z2-Melb/Neb! + z11-Melb/Nrb! + z30-Brime/Drime! + z61-Mareo-Sraus/Starasina! + z74-Mihal-Locar/Socar-Güntlor! + z91-Mike-Žuganič/Luganič!) — VIZUALNO-branje-honesty (Kurrent-stara-pisava!)"},
 {"id": "h-garble-matec-X-open", "opis": "MATEC-garble-X-open-×5 (z23-Anna-Filaš-Križan-¼-K.Jokčon! + z39-Agnes-Hlobuar! + z61-Kathar-Dragot! + z92-Margareth-Hribar! + z95-Anna-Jallopič!)"},
 {"id": "h-garble-botra", "opis": "BOTRA-garble-×8 (z2-Bradde/Brodde! + z11-Lepe/Lyce + Leškovič-Muger! + z21-Lummi-Gumi + Lešlra! + z23-Merk/Werh + Poždivc/Poždire! + z30-Pašič! + z61-Eluc-Dragoš + Leugel-Špacer-Hanek-MAX! + z69-Straus + Lusič! + z78-Pozdire/Podire + Klobučar!)"},
 {"id": "h-duhovniki-X-open", "opis": "DUHOVNIKI-X-open-podpis-razločba (Janičar-coep-vs-Dovgan!-Kurrent-ligature!-VIZUALNO-branje-14-strani!-krop-×9!)-brez-API-VLM (429!) — alternacija-opisana-kot-X-open-vzorec"},
 {"id": "h-z76-dan-DUEL", "opis": "z76-datumski-pripis-dan-DUEL-X-open (21↔26!-'gebären-am-…-Decemb-1879') + namen-X-open (datumski-popravek?-Z49-PARALELA!-ali-drugega-vpisa?!)"},
 {"id": "h-todtgeboren-garble", "opis": "todtgeboren-garble-X-open-črkovno (z15-'tolyabnumm' + z57-'turblyaborn'-MAX-krop! + z66-'turblyubonnin'-MAX-krop!) — ≈-'todtgeboren'-vzorec-3×-POTRJEN!-točna-črkovanja-X-open"},
 {"id": "h-429-API", "opis": "METODOLOŠKA-OPOMBA: API-VLM-429-rate-limit-za-celotno-fazo! → VIZUALNO-arhivar-branje-×14 (direktno-branje-skenov!) + MAX-krop-70 (12×-zoom!-dueli!-dvojčki!-todtgeboren!-meja!-glave!-podpisi!-z60/z32/z76!) — recept-P226-VIZUALNO-×12!"},
 {"id": "h-hisna-19-or-49", "opis": "z33-hiša-DUEL-19↔49-REŠEN-KOT-49 ('4'-odprta-forma!-vs-referenca-'1'-v-'15'/'17'!)-ampak-črkovno-X-open-opomba (manj-100%-kot-čisto-'22'/'17'-rešitvi!)"},
 {"id": "h-ozelt-hisna", "opis": "z80-Krasinec-hiša-DUEL-15↔45-NE-REŠEN (ne-Griblje!-izven-obsega-blokov!-X-open-v-dokazu)"},
 {"id": "h-z42-vas-garble", "opis": "z42-vas-'Podremej[?]'-X-open (Podzemelj-varianta?!) + z108-'Hrašt/Hrast'-X-open (z45!)"},
 {"id": "h-z15-krsten-prazen-typ", "opis": "z15-krsten-'—'-PRAZEN (todtgeboren!) — 1.-KRSTEN-PRAZEN-TIP-×3 (z15/z57/z66!) — P226-z110-PARALELA!"},
 {"id": "h-pag-konvencija", "opis": "pag-konvencija-'sken−6'-14/14-VIZUALNO (vsak-sken!) — brez-VLM-misreadov-te-leta (čisto-okno!)-LEAD-s112-'106'-PREDICTION-1:1!"},
]
lead = "P228-LEAD: krstna-04104, leto 1878 (8/15) — TAIL-ŽE-VLM (s106: z90–z94-Dez-23–30 + VSOTNA-'1/8/7/8'-ali-'1/8/7/9'-DUEL-X-open + glava-'Jahr 1878'-s-popravo!-incl.-z91-Krivoglavce-†3.1.1932!) → 1878 = 94-vpisov-pričakovano (z1–z94) → MEJA-1877/78-pred-s106 → probe-s99–s106! — gola-pag-'sken−6'-pričakovana-s99='93'!"

out = {
 "phase": "P227",
 "title": "Župnija Podzemelj — krstna knjiga 04104 (predzgodovina), polno leto 1879 = 7/15 (issue #18)",
 "type": "parish-baptism-prehistory",
 "status": "DOCUMENTED",
 "issuedAt": "2026-11-09",
 "source": {"book": "04104", "url": "https://data.matricula-online.eu/sl/slovenia/ljubljana/podzemelj/04104/",
            "inventar": 200, "okvir": "s106–s119 (14 skenov; s112-proba! s105–s111-probe-nazaj! s106-MEJA! s119-tail-P226!)", "prenos": "2×-neodvisna-md5-15/15"},
 "method": "2×-neodvisna-prenosa-md5 + VIZUALNO-arhivar-branje-×14 (API-429-override!-s106–s119!) + krop-70 (dueli-MAX-×4 + dvojčki-×3 + todtgeboren-×3 + meja-×2 + glave-×2 + z60/z32/z76 + zap-×5 + meseci-×4 + podpisi-×9 + foliacija-×13 + Griblje-×21!) — triangulacija-VIZUALNO+MAX-krop+sandwich-chronologija",
 "frame": {"scanFrom": 106, "scanTo": 119, "pagKonvencija": "gola-svinčna-'sken−6'-14/14-SEKVENČNO (100–113!-s112='106'-LEAD-PREDICTION-POTRJENA!) — brez-luknje-v-1879-oknu (SKUPNA-SERIJA-100–158!)", "year": 1879,
           "rowsTotal": 96, "break1878/79": "s105/s106 (TAIL-1878-z90–z94 + VSOTNA-RAZPETA-'1 8'+'79'-čez-obe-strani! + glava-'Jahr 1878'-s-popravo + restart-z1-8./9.-JÄNNER-Kloster-h37-Maria-†19.7.1942!)", "break1879/80": "s119/s120 (P226!)"},
 "okvir": {**okvir, "stats": st},
 "entries": grib,
 "stats": {**st, "griblje_22": "22-GRIBLJE / 19-hiš (h31-×2 + h22-×2 + h17-×2-DUELI-REŠENI!) — PARALELA-22-P226! + PEZDIRC-×12 (2-DVOJNI!-continuum-7-let!) + DVOJČKI-ZWILLINGE-×3-REKORD ('Zwillinge'-anotacije!) + TODTGEBOREN-×3 + MODRI-×12-REKORD + DUHOVNIŠKA-IZMENJAVA!"},
 "anomalije": anomalije,
 "crossLinks": cross,
 "honesty": honesty,
 "nextSteps": [lead],
}
os.makedirs("/home/z/my-project/research/issue17", exist_ok=True)
json.dump(out, open("/home/z/my-project/research/issue17/parish-baptism-1879-04104.json", "w"), ensure_ascii=False, indent=1)
print(f"dokaz: entries={len(out['entries'])} anomalije={len(anomalije)} cross={len(cross)} honesty={len(honesty)}")
