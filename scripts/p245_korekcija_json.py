#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P245 — P244-KOREKCIJA JSON: restart-1879 = s26 (ne s27!), številčenje-v-margini, finis-1878."""
import json

P = '/home/z/my-project/research/issue17/parish-marriage-1879-04455.json'
d = json.load(open(P, encoding='utf-8'))

d['naslov'] = ('POROČNA PREDZGOVINA 04455, leto 1879 = 7/13 — s26–s35 (P245-KOREKCIJA: RESTART-1879 = s26-TOP-'
               'velika-letnica-v-datumu-vpisa-1-Fritz-×-Blasnik!-številčenje-v-LEVI-MARGINI! + GLAVA-ponovljena-'
               's27–s34-je-PONOVITEV-ne-restart! + FOLIACIJA-5/5→P243-DUEL-REŠEN!)')

d['vir']['skeni'] = ('s26–s35 (10 skenov md5-10/10! — vsi-glavni!-+ s25-tail-kontekst-1878-na-zalogi-md5!) — '
                     'P245-KOREKCIJA: s26-je-GLAVNI (restart!) ne-samo-tail-kontekst')

d['frame']['restart_varianta'] = (
    "P245-KOREKCIJA (popravlja-P244!): RESTART-1879 = s26-TOP — VELIKA-letnica-'1879'-kot-predpona-DATUMA-vpisa-1 "
    "('1879-Jänner-1.'-veliko!-NI-posebna-glava-nad-tabelo!-cf.-P238/P239-vzorec-velika-letnica-v-vpisu-1!) — "
    "vpis-1 = 1. Jänner 1879 — Wilhelm-Fritz-[~frih/Kritz-DUEL-Kurrent!]-Ökonom-Wolfsberg-41-v-Kärnthen-stanuje-"
    "LOKA-1 (34-l) × Anna-Blasnik-[~Blahnik-DUEL!]-Cerno-melj.-38 (43-l)-gostilničarjeva-hči! + vpis-2 = 12. Jänner — "
    "Anton-Krupljen-[~Krystan/Pristan-DUEL!]-k.k.-Postwärth-Cernomelj (37-l) × Elisabeth-[~Rubin/Krslin-DUEL!]-"
    "18-l-MLADOLETNICA-minderjährig-Einwilligung-starši! + vpis-3 = 26. Jänner — Georg-Krugel-[~Krigel/Krügel-DUEL!]-"
    "½-Gübler-Dobranič-18 (63-l) × Katharina-geb.-Klobučar-[~Hrab/Klepec-DUEL-verw.!]-Boršt-22 (44-l)-VDOVA! — "
    "ŠTEVILČENJE-v-LEVI-MARGINI (1-2-3-modro-sivo!-natisnjen-Lfd.-stolpec-NE-OBSTAJA-'Haus-Nr.'-je-med-Wohnort-in-imenom!) "
    "+ DUHOVNIK-Franz-DOVGAN-podpis-×3 (v1–v3!-kontinuum-od-1.-VPISA-1879!) — P244-napaka (restart-s27-TOP-+-'vpis-1-=-"
    "Klepec-29.-Jänner')-nastala: pass-1-s26-vrnil-PRAZNO (vrstic=0-glave=[ni]!)-+ pass-1-s27-številke-'niso-vidne'→"
    "P244-sklenil-restart-na-s27; GLAVA-'1879'-na-s27–s34-je-PONOVITEV-leto-na-vsakem-listu (P244-sama-NOVA-8.-VARIANTA!)-"
    "NE-restart-marker — Klepec-29.-Jänner = vpis-4 (NE-1!)")

d['frame']['meja_1878_79'] = (
    "s25→s26 (P245-KOREKCIJA!-tail-1878 = s25: zap-št.-22–23-v-margini — 22-=-1878-Okt.-[24~27-DUEL!]-Martin-[~]-"
    "Mrivo-glavre-38-+ 23-=-Novem.-10.-Mathias-[~]-Gornji-Dovc.-67-+ ★★★ VELIKA-ROKOPISNA-OPOMBA-'finis-pro-anno-1878'-"
    "na-sredi-strani-POD-vrstama = ZAKLJUČNA-OZNAKA-LETA — 2.-instance-v-poročni-predzgovorini (cf.-P243-s38-'finis-/-"
    "s-1880'!-vzorec-PONOVLJEN-čez-leta!-P243-'1.-ta-vrsta'-→-1.-ODKRITA-v-P243-ampak-s25-zgodnejša-v-knjigi!) — "
    "Krugel-s26-dno-NI-tail-1878-ampak-vpis-3-1879-P245-KOREKCIJA!)")

d['frame']['numbering'] = (
    "s26 = 1–3-restart (P245-KOREKCIJA!-margini-1/2/3!) · s27 = 4–5 (margini-4/5!-Klepec-16-je-v4!) · s28 = 6–8 "
    "(3-vrstice!-margina-6-jasna-+ 7-poškodovana-trganje-papirja-aritmetično-vsiljena-6-[7]-8-+ 8-jasna!-v6-Wingler-"
    "Cerknobl-14-vojak-NE-Griblje-v7-Pezdirc-50-v8-Kunič[~]-Ustje-19!) · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · "
    "s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33-tail (P243-1:1!) — 33-VPISOV-BREZ-PRESKOKOV "
    "(5.-leto-zapored!-vsota-NESPREMENJENA: P244-s27+s28-8-vpisov-=-KOREKCIJA-s26+s27+s28-8-vpisov!)")

d['frame']['foliacija'] = (
    "s26-'Pag. 25.'-1:1 (P245-KOREKCIJA-nova!)-+ s27-'Pag. 26.'-1:1-+ s30-'Pag. 29'-1:1-+ s34-'Pag. 33'-1:1-+ "
    "s35-'Pag. 34.'-1:1 = FOLIACIJA-'Pag-=-sken−1'-5/5-1879! → P243-s38-'Pag. 34.'-X-OPEN-DUEL-REŠEN: pravilo-"
    "Pag==sken−1-OSTAJA (s38-branje-'34'-= MISREAD-'37'-0-vs-7-Kurrent-cf.-P162b!) + s31-'Pag. 36.'-[~MISREAD-'30'-"
    "0-vs-6-DUEL-podporjen!]")

d['stats']['entriesNote'] = (
    "s26-1–3-restart + s27-4–5 + s28-6–8 + s29-9–11 + s30-12–14 + s31-15–18 + s32-19–21 + s33-22–25 + s34-26–30 + "
    "s35-top-31–33 = 33 DISTINCT (BREZ preskokov!-P245-KOREKCIJA: distribucija-s26–s28-popravljena-vsota-33-NESPREMENJENA!)")

d['bloki'][0]['vpis'] = 4
d['bloki'][0]['opomba'] = ("P245-KOREKCIJA: vpis-4 (NE-1!-restart-je-v1-Fritz-s26!)-+ 'Civil-Beizag'-modri-pripis-"
                           "NOV-element!-+ Klepec-cf.-P94-h22-MILEK-×-KLEPEC-1899!")
d['bloki'][1]['vpis'] = 7
d['bloki'][1]['opomba'] = ("★★★ h50 = 1.-POROČNI-DOKAZ-V-PREDZGODOVINI (PT-luknja-hiša-P191!) + PEZDIRC-ženin-7.-leto! + "
                           "P245-KOREKCIJA: vpis-7 (NE-5!-margina-fizično-poškodovana-trganje-papirja-aritmetično-vsiljena-"
                           "6-[7]-8!) + v6-Wingler-Cerknobl-vojak-NE-Griblje!")

an = d['anomalie']
# [0] restart
an[0] = ("★★★ P245-KOREKCIJA: RESTART-1879 = s26-TOP — velika-letnica-v-datumu-vpisa-1 (1.-Jänner-Wilhelm-Fritz-LOKA-1-"
         "×-Anna-Blasnik-CERNO-38!-cf.-P238/P239-vzorec!) — P244-trdil-s27-TOP-z-Klepcem-kot-vpisom-1 (napaka: pass-1-s26-"
         "prazno-vrstic=0-+ številke-'niso-vidne'-na-s27!)-Klepec = vpis-4 (NE-1!)-podrobnosti-v-frame.restart_varianta")
# [1] glava
an[1] = an[1].replace(
    "= NOVA-8.-MEJNA-VARIANTA",
    "= NOVA-8.-MEJNA-VARIANTA (P245-KOREKCIJA: ponovitev-glave-NI-restart-marker!-P244-je-iz-nje-napačno-sklenil-"
    "restart-na-s27!)")
# [2] foliacija 4/4 → 5/5
an[2] = an[2].replace("4/4-1879", "5/5-1879").replace(
    "(s27-'Pag. 26' + s30-'Pag. 29' + s34-'Pag. 33' + s35-'Pag. 34'!-vsi-ul",
    "(s26-'Pag. 25' + s27-'Pag. 26' + s30-'Pag. 29' + s34-'Pag. 33' + s35-'Pag. 34'!-vsi-ul")
# [3] v5→v7
an[3] = an[3].replace("(v5-Mathias-Pezdirc", "(v7-Mathias-Pezdirc")
# [4] v1→v4
an[4] = an[4].replace("(v1-Klepec-+", "(v4-Klepec-+")
# [7] v5→v7
an[7] = an[7].replace("v5-ženin-Mathias-h50", "v7-ženin-Mathias-h50")
# [10] v1→v4 (Civil-Beizag na s27 pripada Klepecu)
an[10] = an[10].replace("★★ v1-'Civil-Beizag", "★★ v4-'Civil-Beizag", 1)
# NOVI vnosi
an.append("★★★ P245-KOREKCIJA-METODA: številčenje-1879-v-LEVI-MARGINI (modro-sivo-črnilo!-natisnjen-Lfd.-stolpec-NE-"
          "OBSTAJA-'Haus-Nr.'-je-med-Wohnort-in-imenom!) — dokazi: margina-2/3-s26-+ 4/5-s27-+ 6/8-s28-ultra-zoom-jasna-"
          "+ 7-poškodovana-trganje-papirja-aritmetično-vsiljena-6-[7]-8-+ 22/23-s25-1878!-P244-pass-1-s26-vrnil-prazno-"
          "PONOVLJENIH-6-VLM-pregledov-P245-+ 3-ultra-zooma")
an.append("★★★ FINIS-PRO-ANNO-1878 = s25-sredina-strani (velika-rokopisna-opomba-POD-vrstama-22–23!) = 2.-instance-"
          "zaključne-oznake-leta-v-poročni-predzgovorini (cf.-P243-s38-'finis-/-s-1880'-1.-ODKRITA!-vzorec-se-PONOVLJUJE-"
          "čez-leta-1878-in-1880!)-+ meja-1878/79-spremenjena-s26→s27-NA-s25→s26")
an.append("★★ KONTEKST-v1-v2-v3-v5-NI-bloki-pošteno: v1-Fritz-LOKA-1-(roj.-Wolfsberg-Kärnthen!)-+ v2-Krupljen-CERNO-"
          "melj.-+ v3-Krugel-DOBRANIČ-18-(½-Gübler-status-NI-hiša-Griblje!)-+ v5-Štefanik[~]-DOBRANE-8 — vsi-4-NI-"
          "kandidati-korpusa (GRIBLJAN-izvor/bivališče-pravilo-pošteno!)")
an.append("★★ DOVGAN-od-PRVEGA-VPISA-1879: Franz-Dovgan-podpis-×3-na-s26 (v1-2-3!-+ Befunde-v3-'Franz-Dovgan') = "
          "kontinuum-ZDAJ-OD-1.-VPISA-leta (P244-je-poznal-samo-s35-tail-podpis-14/9!-1879–1885-kontinuum-se-širi!)")

d['metoda'] = (
    "10-skenov-s26–s35-md5-10/10 (viewer-HTML→192-URL-trailing-slash-fix!) + VLM-pass-1-×8 (s27–s34-polni-prepisi!) + "
    "pass-2-×18-kropov (glave-+ stolpci-+ bloki-+ tail!) + pass-4-ultra-zoom-4×-5-kropov (s27-v1-L/D + s29-L-vse + "
    "s31-v16 + s32-v20!) + reconciliacija-1:1-z-P243-tail (s35-top-31–33!) — P245-KOREKCIJA: 6-VLM-pregledov-živega-vira "
    "(margine-s25/s26/s27/s28 + s26-polna-stran + glava-stolpcev!) + 3-ultra-zooma-margine (s26-'1'-cvak + s28-'6'-jasno + "
    "s28-'8'-jasno!-7-poškodovano-trganje-papirja-aritmetično!) + moja-lastna-očesa-Read-pregledi-4-striptov — P244-napaka-"
    "RAZKRITA: pass-1-s26-vrnil-prazno (vrstic=0!)-in-P244-je-sklenil-restart-na-s27-brez-fizične-berljivosti-števil")

d['lead'] = ("P246+: leto-1878-=-8/13 (s24-nazaj-tail-1878 = s25-22–23-'finis-pro-anno-1878'-že-1:1-P245-KOREKCIJA!-"
             "s26-'1879'-restart-že-1:1!) ali-knjižno-odpiranje-1873-s1")

d['korekcija'] = {
    "faza": "P245",
    "razkritje": ("RESTART-1879 = s26 (ne s27!): 3-vpisa-januarja-1879-na-s26 (v1-Fritz-LOKA-1-×-Blasnik-CERNO-38 · "
                  "v2-Krupljen-CERNO-· v3-Krugel-DOBRANIČ-18)-številčenje-v-levi-margini-1–3"),
    "vzrok-napake": ("P244-pass-1-na-s26-vrnil-prazno (vrstic=0-glave=[ni]-meja='') → s26-obdelan-kot-'tail-kontekst'-"
                     "brez-vpisov; s27-velika-glava-'1879'-napačno-tumačena-kot-restart-marker (glava-je-ponovljena-na-"
                     "vsakem-listu!); marginalne-številke-niso-bile-preverjene-fizično"),
    "dokazi": [
        "6-VLM-pregledov (margine-s25/s26/s27/s28 + s26-polna-stran + glava-stolpcev)",
        "ultra-zoom: s26-'1'-cvak + s28-'6'-jasno + s28-'8'-jasno + s28-'7'-trganje-papirja-aritmetika-6-[7]-8",
        "s25-margina-22/23-+-velika-opomba-'finis-pro-anno-1878'",
        "foliacija-s26-'Pag. 25.'-1:1-→-pravilo-Pag==sken−1-5/5",
        "duhovnik-Franz-DOVGAN-×3-podpisa-na-s26 (v1–v3!)",
    ],
    "spremembe": [
        "restart_varianta: s27-TOP→s26-TOP (+ vpis-1-=-Fritz)",
        "meja_1878_79: s26→s27-postane-s25→s26",
        "bloki: Klepec-vpis-1→4-+-Pezdirc-vpis-5→7",
        "distribucija: s27-1–2-+-s28-3–8→s26-1–3-+-s27-4–5-+-s28-6–8",
        "foliacija: 4/4→5/5-(-s26)",
        "novi-kontekstni-vpisi-v1-v2-v3-v5-NI-bloki-pošteno",
        "DOVGAN-kontinuum-od-v1-(-×3-podpisa-s26)",
        "FINIS-1878-s25-=-2.-instance-vzorca",
    ],
    "nespremenjeno": [
        "33-vpisov-skupaj-BREZ-preskokov",
        "9-Griblje-blokov-h16-h50-h61-h21-h32-h13-h42-h17-h16",
        "korpus-235-04455-·-1978-vitalov-·-228-sidra-·-202-dobe",
        "v9–v33-vse-številke-NESESPRJENE",
        "meja-1879/80-s35-mid-P243",
    ],
}

json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('JSON korekcija OK:', P)
print('naslov:', d['naslov'][:100])
print('bloki-vpis:', [b['vpis'] for b in d['bloki']])
print('anomalie:', len(an))
