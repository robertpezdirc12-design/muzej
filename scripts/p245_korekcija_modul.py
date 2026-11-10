#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P245 — P244-KOREKCIJA modul parish-marriage-early.ts."""
P = '/home/z/my-project/src/data/atlas/parish-marriage-early.ts'
s = open(P, encoding='utf-8').read()
n = 0

def rep(old, new, tag):
    global s, n
    if old not in s:
        raise SystemExit(f'NISDEM: {tag}\nOLD: {old[:120]}')
    if s.count(old) != 1:
        raise SystemExit(f'NEUNIKATNO ({s.count(old)}×): {tag}')
    s = s.replace(old, new)
    n += 1
    print(f'OK {tag}')

# 1) section header
rep("/** ——— P244: poročna predzgodovina 04455, leto 1879 = 7/13 (s27–s35; RESTART-s27-top velika-glava + GLAVA-PONOVLJENA-NA-VSAKEM-LISTU-NOVA-8.-MEJNA-VARIANTA! + FOLIACIJA-4/4→P243-DUEL-REŠEN!) — 33 VPISOV-BREZ-PRESKOKOV · 9-GRIBLJE-blokov (h16-×2-BLOKA!) ——— */",
    "/** ——— P244: poročna predzgovorina 04455, leto 1879 = 7/13 (s26–s35; P245-KOREKCIJA: RESTART = s26-TOP-velika-letnica-v-vpisu-1-Fritz-×-Blasnik + številčenje-v-LEVI-MARGINI + GLAVA-ponovljena-s27–s34-je-PONOVITEV! + FOLIACIJA-5/5→P243-DUEL-REŠEN!) — 33 VPISOV-BREZ-PRESKOKOV · 9-GRIBLJE-blokov (h16-×2-BLOKA!) ——— */",
    '1-header')

# 2) MEJA restart SI/EN
rep('  restartSi:\n    "restart-vpis-1 = 29. Jänner 1879 [~März-DUEL-2-branja!-pass-1+2+3-za-Jänner!] = s27-TOP (VELIKA-glava-\'1879\'-na-ZAČETKU-leve-polovice-PRED-vrstico-zap.-št.-1!-cf.-P241-4.-VARIANTA!) — ženin-Georg-Klepec-[~Klejec/Klobučar/Pegdirc-TRIPLE-DUEL-4-branja!]-½-Güblar-GRIBLJE-16-[~DUEL-Otok-1!] ×-Marie-Jurejevič-GRIBLJE-10-[~3-branja!]-+ MODRI-pripis-\'Civil-Beizag-präsent-...-Dechant-von-Admont-9.-Jänner-1879\'-NOV-ELEMENT-[~X-OPEN!]",',
    '  restartSi:\n    "P245-KOREKCIJA: restart-vpis-1 = 1. Jänner 1879 = s26-TOP (velika-letnica-\'1879\'-kot-predpona-datuma-vpisa-1-NI-posebna-glava!-cf.-P238/P239!) — ženin-Wilhelm-Fritz-[~frih/Kritz-DUEL!]-Ökonom-Wolfsberg-41-v-Kärnthen-stanuje-LOKA-1 (34-l) ×-Anna-Blasnik-[~Blahnik!]-Cerno-melj.-38 (43-l!) + v2-Krupljen-Cerno-12.-Jänner + v3-Krugel-DOBRANIČ-18-26.-Jänner (½-Gübler!-NI-blok!) — številčenje-v-LEVI-MARGINI-1–3 (modro-sivo!-Lfd.-stolpec-ne-obstaja!) + Franz-DOVGAN-podpis-×3! — P244-napaka: pass-1-s26-vrnil-PRAZNO-→-napačen-restart-s27; Klepec-29.-Jänner = vpis-4 (NE-1!)",',
    '2-restartSi')
rep('  restartEn:\n    "restart-entry-1 = Jan 29, 1879 [~März-DUEL!] = s27-TOP (the-BIG-heading-\'1879\'-BEFORE-entry-row-1!-cf.-P241-4th-VARIANT!) — groom-Georg-Klepec-[~TRIPLE-DUEL-4-readings!]-½-Güblar-GRIBLJE-16-[~DUEL-Otok-1!] ×-Marie-Jurejevič-GRIBLJE-10-[~3-readings!]-+ the-MARGIN-note-\'Civil-Beizag-präsent\'-NEW-element-[~X-OPEN!]",',
    '  restartEn:\n    "P245-CORRECTION: restart-entry-1 = Jan 1, 1879 = s26-TOP (the-BIG-year-\'1879\'-as-the-PREFIX-of-entry-1\'s-date-NOT-a-separate-heading!-cf.-P238/P239!) — groom-Wilhelm-Fritz-[~frih/Kritz-DUEL!]-Ökonom-Wolfsberg-41-in-Carinthia-lives-at-LOKA-1 (34-y) ×-Anna-Blasnik-[~Blahnik!]-Cerno-melj.-38 (43-y!) + v2-Krupljen-Cerno-Jan-12 + v3-Krugel-DOBRANIČ-18-Jan-26 (½-Gübler!-NOT-a-block!) — the-numbering-IN-THE-LEFT-MARGIN-1–3 (blue-grey!-no-printed-Lfd.-column!) + Franz-DOVGAN-×3-signatures! — the-P244-error: pass-1-on-s26-returned-EMPTY-→-the-restart-wrongly-placed-on-s27; Klepec-Jan-29 = entry-4 (NOT-1!)",',
    '3-restartEn')

# 3) MEJA boundary SI/EN
rep("  boundarySi:\n    \"meja-1878/79 = s26→s27 (tail-1878-Georg-Krugel-[~Krigel!]-½-Grubl-s26-DNO!-opomba-'dd.-12-Jänner-879'-priča-[~X-OPEN!]) · meja-1879/80 = s35-mid (33→restart-1–2-P243-1:1!) — GLAVA-'1879'-PONOVLJENA-NA-VSAKEM-RAZPRTEM-LISTU-s27–s34 (mrliški-vzorec-mej-60.–74.-POTRDILO-ČEZ-KNJIGE!) = NOVA-8.-MEJNA-VARIANTA!\",",
    "  boundarySi:\n    \"meja-1878/79 = s25→s26 (P245-KOREKCIJA!-tail-1878 = s25: margina-22–23-+ VELIKA-'finis-pro-anno-1878'-sredina-strani = 2.-instance-zaključne-oznake-cf.-P243-s38!-Krugel-s26-NI-tail-1878-ampak-vpis-3!) · meja-1879/80 = s35-mid (33→restart-1–2-P243-1:1!) — GLAVA-'1879'-PONOVLJENA-NA-VSAKEM-RAZPRTEM-LISTU-s27–s34 (mrliški-vzorec-mej-60.–74.-POTRDILO-ČEZ-KNJIGE!) = NOVA-8.-MEJNA-VARIANTA-vendar-PONOVITEV-ne-restart-marker (P244-napaka-popravljena!)\",",
    '4-boundarySi')
rep("  boundaryEn:\n    \"the-1878/79-boundary = s26→s27 (the-tail-1878-Krugel-[~]-s26-BOTTOM!-note-'dd.-12-Jänner-879'-witness-[~X-OPEN!]) · the-1879/80-boundary = s35-mid (P243-1:1!) — the-'1879'-heading-REPEATED-ON-EVERY-SPREAD-s27–s34 (the-death-register-boundary-pattern-CONFIRMED-ACROSS-BOOKS!) = the-NEW-8th-MEJNA-VARIANT!\",",
    "  boundaryEn:\n    \"the-1878/79-boundary = s25→s26 (P245-CORRECTION!-the-1878-tail = s25: margin-22–23-+-the-BIG-'finis-pro-anno-1878'-mid-page = the-2nd-instance-of-the-year-end-marker-cf.-P243-s38!-Krugel-on-s26-is-NOT-the-tail-but-entry-3!) · the-1879/80-boundary = s35-mid (P243-1:1!) — the-'1879'-heading-REPEATED-ON-EVERY-SPREAD-s27–s34 (the-death-register-boundary-pattern-CONFIRMED-ACROSS-BOOKS!) = the-NEW-8th-MEJNA-VARIANT-but-a-REPETITION-not-a-restart-marker (the-P244-error-corrected!)\",",
    '5-boundaryEn')

# 4) NUMBERING + comment
rep("/** Številčenje strani 1879 (s27 = 1–2 · s28 = 3–8 · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33) — 33-VPISOV-BREZ-PRESKOKOV (5.-leto-BREZ-kontrast-1881!). */",
    "/** Številčenje strani 1879 (P245-KOREKCIJA! s26 = 1–3 · s27 = 4–5 · s28 = 6–8 · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33) — 33-VPISOV-BREZ-PRESKOKOV (5.-leto-BREZ-kontrast-1881!-vsota-33-NESPREMENJENA!). */",
    '6-numcomment')
rep('  "s27 = 1–2 (restart!) · s28 = 3–8 (6-vrstic-pass-1-samo-3-videl-krop-stolp-3×!-v3-Wingler-Cerknobl-vojak!-v5-Pezdirc-50!-v6-Luniri-Vranovice!) · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33-tail (P243!)";',
    '  "s26 = 1–3 (P245-KOREKCIJA-restart!-margini-1/2/3!) · s27 = 4–5 (margini-4/5!-Klepec-je-v4!) · s28 = 6–8 (3-vrstice!-6-jasna-+ 7-poškodovana-trganje-papirja-aritmetično-6-[7]-8-+ 8-jasna!-v6-Wingler-NE-Griblje-v7-Pezdirc-50-v8-Kunič[~]) · s29 = 9–11 · s30 = 12–14 · s31 = 15–18 · s32 = 19–21 · s33 = 22–25 · s34 = 26–30 · s35-top = 31–33-tail (P243!)";',
    '7-numbering')

# 5) FOLIACIJA 4/4→5/5
rep("/** ★★★★★ FOLIACIJA-1879-'Pag = sken−1'-4/4 (s27-'Pag. 26' + s30-'Pag. 29' + s34-'Pag. 33' + s35-'Pag. 34'!-vsi-ultra-zoom-1:1!) → P243-s38-'Pag. 34.'-X-OPEN-DUEL-REŠEN: pravilo-Pag==sken−1-OSTAJA (s38-branje-'34'-= MISREAD-'37'-0-vs-7-Kurrent-cf.-P162b!) — s31-'Pag. 36.'-[~MISREAD-'30'-0-vs-6-DUEL-podporjen!]. */",
    "/** ★★★★★ FOLIACIJA-1879-'Pag = sken−1'-5/5 (s26-'Pag. 25' + s27-'Pag. 26' + s30-'Pag. 29' + s34-'Pag. 33' + s35-'Pag. 34'!-vsi-ultra-zoom-1:1!-s26-P245-KOREKCIJA-nova!) → P243-s38-'Pag. 34.'-X-OPEN-DUEL-REŠEN: pravilo-Pag==sken−1-OSTAJA (s38-branje-'34'-= MISREAD-'37'-0-vs-7-Kurrent-cf.-P162b!) — s31-'Pag. 36.'-[~MISREAD-'30'-0-vs-6-DUEL-podporjen!]. */",
    '8-folcomment')
rep('  "s27-\'Pag. 26\'-1:1-+ s30-\'Pag. 29\'-1:1-+ s34-\'Pag. 33\'-1:1-+ s35-\'Pag. 34\'-1:1 = 4/4-1879!-→ P243-X-OPEN-DUEL-REŠEN',
    '  "s26-\'Pag. 25\'-1:1-+ s27-\'Pag. 26\'-1:1-+ s30-\'Pag. 29\'-1:1-+ s34-\'Pag. 33\'-1:1-+ s35-\'Pag. 34\'-1:1 = 5/5-1879!-→ P243-X-OPEN-DUEL-REŠEN',
    '9-folstr')

# 6) H50 vpis-5→7
rep('  "vpis-5-Mathias-Pezdirc-GRIBLJE-50-×-Maria-Škuncelj-44-5.-Februar-1879 = h50-1.-POROČNI-DOKAZ-V-PREDZGODOVINI',
    '  "P245-KOREKCIJA: vpis-7-Mathias-Pezdirc-GRIBLJE-50-×-Maria-Škuncelj-44-5.-Februar-1879 (NE-vpis-5!-margina-fizično-poškodovana-trganje-papirja-aritmetično-vsiljena-6-[7]-8!) = h50-1.-POROČNI-DOKAZ-V-PREDZGODOVINI',
    '10-h50')

# 7) H16 v1→v4
rep('  "h16 = ×2-BLOKA-V-1879 (v1-ženin-Georg-Klepec-[~TRIPLE-DUEL!]-29.-Jänner-+ v25-ženin-Matthius-Tomc-4.-Mai!)',
    '  "h16 = ×2-BLOKA-V-1879 (P245-KOREKCIJA: v4-ženin-Georg-Klepec-[~TRIPLE-DUEL!]-29.-Jänner-NE-vpis-1!-restart-je-v1-Fritz-s26!-+ v25-ženin-Matthius-Tomc-4.-Mai!)',
    '11-h16')

# 8) PEZDIRC v5→v7
rep('  "PEZDIRC-CONTINUUM-×131→04455-v-7.-LETU-predzgodovine: v5-ženin-Mathias-Pezdirc-h50-1:1-krop!',
    '  "PEZDIRC-CONTINUUM-×131→04455-v-7.-LETU-predzgodovine: P245-KOREKCIJA-v7-ženin-Mathias-Pezdirc-h50-1:1-krop! (NE-v5!)',
    '12-pezdirc')

# 9) DOVGAN
rep('  "DOVGAN-CONTINUUM-PODALJŠAN-NA-7-LET (1879–1885!): s35-tail-D-podpis-\'Copulatus-sum-Griblje-d.-14/9-1879.-Dopgan\'-1:1!-+ v16-duhovnik-\'Franc-[~Pasthic/Dovgan-DUEL!]\'-+ s27-v1-modri-pripis-\'Anton-Franz-von-Dovgan-Dechant\'-omenjen-[~X-OPEN-kaj-točno!]";',
    '  "DOVGAN-CONTINUUM-PODALJŠAN-NA-7-LET (1879–1885!-P245-KOREKCIJA-se-širi-OD-PRVEGA-VPISA!): Franz-Dovgan-podpis-×3-NA-s26 (v1-2-3!-januar-1879!-+ Befunde-v3-\'Franz-Dovgan\')-+ s35-tail-D-podpis-\'Copulatus-sum-Griblje-d.-14/9-1879.-Dopgan\'-1:1!-+ v16-duhovnik-\'Franc-[~Pasthic/Dovgan-DUEL!]\'-+ s27-v4-modri-pripis-\'Anton-Franz-von-Dovgan-Dechant\'-omenjen-[~X-OPEN-kaj-točno!]";',
    '13-dovgan')

# 10) DUELS v1→v4
rep('/** Datum-dueli 1879 (v1-\'29.-Jänner-vs-März\'-2:1!-+ v15/v16/v17-\'19.\'-3-poroke-isti-dan-kandidat-[~X-OPEN!]-+ v24-\'23-vs-24\'-Feb-[~]-+ v20/v21-\'19.\'-[~]). */',
    "/** Datum-dueli 1879 (P245-KOREKCIJA: Klepec-je-v4!-v1-Fritz-1.-Jänner-BREZ-duela!-+ v15/v16/v17-'19.'-3-poroke-isti-dan-kandidat-[~X-OPEN!]-+ v24-'23-vs-24'-Feb-[~]-+ v20/v21-'19.'-[~]). */",
    '14-duelcomment')
rep('  "v1-datum »29. Jänner vs 29. März« 2:1-za-Jänner [~] (pass-1+2+3-Jänner!-pass-4-\'März\'-\'Jänner\'-oboje-v-branju!)"',
    '  "P245-KOREKCIJA-v4-datum »29. Jänner vs 29. März« 2:1-za-Jänner [~] (pass-1+2+3-Jänner!-pass-4-\'März\'-\'Jänner\'-oboje-v-branju!-NE-vpis-1!-v1-Fritz-1.-Jänner-brez-duela!)"',
    '15-duel0')

# 11) NOVI izvozi: MARRIAGE_1879_KOREKCIJA + MARGINA + FINIS + KONTEKST (pred MARRIAGE_1879_KORPUS)
anchor = '/** Vse-nove-1879-meritve-v-obliki-za-QA (skupaj-04455: 226→235'
novi = '''/** ★★★★★ P245-KOREKCIJA: P244-napaka-RAZKRITA-in-POPRAVLJENA — restart-1879 = s26 (ne s27!): 3-januarskih-vpisov-na-s26 (v1-Fritz-×-Blasnik!-v2-Krupljen!-v3-Krugel!-Krugel-NI-tail-1878!)-številčenje-v-LEVI-MARGINI (Lfd.-stolpec-ne-obstaja!)-Klepec-je-v4-Pezdirc-je-v7-vsota-33-NESESPEMLJENA! */
export const MARRIAGE_1879_KOREKCIJA = {
  razkritje:
    "RESTART-1879 = s26 (ne s27!): 3-vpisa-januarja-1879-na-s26 (v1-Wilhelm-Fritz-LOKA-1-×-Anna-Blasnik-CERNO-38 · v2-Anton-Krupljen-CERNO-· v3-Georg-Krugel-DOBRANIČ-18-×-Katharina-Klobučar[~])-številčenje-v-levi-margini-1–3",
  vzrokNapake:
    "P244-pass-1-na-s26-vrnil-PRAZNO (vrstic=0-glave=[ni]!) → s26-obdelan-kot-'tail-kontekst'-brez-vpisov; s27-velika-glava-'1879'-napačno-tumačena-kot-restart-marker (glava-je-PONOVLJENA-na-vsakem-listu-P244-sama!); marginalne-številke-niso-bile-preverjene-fizično",
  dokazi: [
    "6-VLM-pregledov-živega-vira (margine-s25/s26/s27/s28 + s26-polna-stran + glava-stolpcev!)",
    "ultra-zoom: s26-'1'-cvak + s28-'6'-jasno + s28-'8'-jasno + s28-'7'-trganje-papirja-aritmetika-6-[7]-8",
    "s25-margina-22/23-+-velika-opomba-'finis-pro-anno-1878'",
    "foliacija-s26-'Pag. 25.'-1:1-→-pravilo-Pag==sken−1-5/5",
    "duhovnik-Franz-DOVGAN-×3-podpisa-na-s26 (v1–v3!)",
  ],
  nespremenjeno: [
    "33-vpisov-skupaj-BREZ-preskokov-5.-leto!",
    "9-Griblje-blokov-h16-h50-h61-h21-h32-h13-h42-h17-h16",
    "korpus-235-04455-·-1978-vitalov-·-228-sidra-·-202-dobe",
    "v9–v33-vse-vpisne-številke",
    "meja-1879/80-s35-mid-P243",
  ],
} as const;

/** ★★★ ŠTEVILČENJE-v-LEVI-MARGINI (nov-element-table-formata!): natisnjen-Lfd.-stolpec-NE-OBSTAJA ('Haus-Nr.'-je-med-Wohnort-in-imenom!) — letne-zaporedne-številke-pisane-v-levi-margini-modro-sivim-črnilom (s26-1/2/3 + s27-4/5 + s28-6/[7]/8 + s25-1878-22/23!) — pričakovano-tudi-za-ostala-leta-predzgodovine (kontrola-pri-P246!). */
export const MARGINA_1879_STEVILCENJE =
  "natisnjen-Lfd.-stolpec-ne-obstaja ('Haus-Nr.'-med-Wohnort-in-Tauname!)-letne-številke-v-LEVI-MARGINI-modro-sivo (1–3-s26-+ 4–5-s27-+ 6–8-s28-+ 22–23-s25!) — s28-'7'-fizično-poškodovana-trganje-papirja-aritmetično-vsiljena-6-[7]-8!";

/** ★★★ FINIS-PRO-ANNO-1878 = s25 (2.-instance-zaključne-oznake-leta-v-poročni-predzgovorini!-cf.-P243-s38-'finis-/-s-1880'-1.-ODKRITA!-vzorec-se-ponavlja-čez-leta!). */
export const FINIS_1878_S25 =
  "s25-sredina-strani-POD-vrstama-22–23: velika-rokopisna-opomba-'finis-pro-anno-1878' = zaključna-oznaka-leta-2.-instance (P243-'1.-ta-vrsta'-drži-kot-1.-ODKRITA-ampak-s25-zgodnejša-v-knjigi!)-meja-1878/79-=-s25→s26!";

/** ★★ KONTEKST-vpis-1–5-1879-NI-bloki-pošteno (izven-Griblje!): v1-Fritz-LOKA-1 + v2-Krupljen-CERNO + v3-Krugel-DOBRANIČ-18 + v5-Štefanik[~]-DOBRANE-8. */
export const MARRIAGE_1879_KONTEKST = [
  "v1-1.-Jänner-Wilhelm-Fritz-[~frih/Kritz!]-Ökonom-Wolfsberg-41-Kärnthen-stanuje-LOKA-1-34-l-×-Anna-Blasnik-[~Blahnik!]-Cerno-38-43-l-gostilničarjeva-hči-NI-blok (izven-Griblje!)",
  "v2-12.-Jänner-Anton-Krupljen-[~Krystan/Pristan!]-k.k.-Postwärth-Cernomelj-37-l-×-Elisabeth-[~Rubin/Krslin!]-18-l-MLADOLETNICA-minderjährig-Einwilligung-starši-NI-blok",
  "v3-26.-Jänner-Georg-Krugel-[~Krigel/Krügel!]-½-Gübler-DOBRANIČ-18-63-l-×-Katharina-geb.-Klobučar-[~Hrab/Klepec-DUEL-verw.!]-Boršt-22-44-l-VDOVA-NI-blok (½-Gübler-STATUS-ni-hiša-Griblje!)-P244-ga-je-štel-kot-'tail-1878'-NAPAČNO!",
  "v5-2.[~10.?]-Februar-Georg-Štefanik[~]-½-Gübler-DOBRANE-8-NI-blok-[~X-OPEN-datum-duel!]",
] as const;

'''
rep(anchor, novi + anchor, '16-novi-izvozi')

open(P, 'w', encoding='utf-8').write(s)
print(f'\nMODUL KOREKCIJA OK: {n} sprememb')
