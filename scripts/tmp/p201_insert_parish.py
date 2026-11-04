#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P201 — vstavi 20-GRIBLJE-blokov (04106, leto 1876) v parish.ts PRED P200-sekcijo
(newest-first vzorec). 20 vpisov / 19 hiš (h46-×2!)."""
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P200: mrliška PREDZGODOVINA 04106, leto 1877"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1876," not in src, "1876-bloki-že-obstajajo?!"

K = "Joannes/Jošefin Hogeja/Hogeš 'Coop.' (KROP-grafija = KOGEJ-substituendus — ★★★ KOGEJ-OBDOBJE-NOW-1876!)"
KE = "Joannes/Jošefin Hogeja/Hogeš 'Coop.' (KROP-graphia = the-KOGEJ-substituendus — ★★★ the-KOGEJ-PERIOD-NOW-1876!)"

BLOCKS = [
    ("7", 135, 10,
     "umrl Michael LUŠTANIČ [~], 'Lustbär'[?stan-glif], 65 LET (Februar 15., pokop 17.) — 'Brustkrampf'[?]; previden (1); " + K + "; + ★ 1.-GRIBLJE-vpis-1876 (s134-z5–z10 = 6-Jänner-vrstic-nad!) + [~datum-zmeda-z3/z4-Feb] + [z10]",
     "died Michael LUŠTANIČ [~], 'Lustbär'[?the-glyph], 65 YEARS (Feb 15, buried 17) — 'Brustkrampf'[?]; previden (1); " + KE + "; + ★ the-1st-GRIBLJE-entry-1876 (s134-z5–z10 = 6-Jänner-rows-above!) + [z10]"),
    ("41", 135, 12,
     "umrla Maria STUBLAR, vdova-[?]Hrovič[~], 56 LET (Februar 18., pokop 20.) — Asthma; previden (1); " + K + "; + ★ STUBL-h nit (→ z85-h75-Joannes-STUBLER-Nov-1876 + cf. 1878-nit!) + [z12]",
     "died Maria STUBLAR, widow-[?]Hrovič[~], 56 YEARS (Feb 18, buried 20) — Asthma; previden (1); " + KE + "; + ★ the-STUBL-thread (→ z85-h75-Joannes-STUBLER-Nov-1876!) + [z12]"),
    ("53", 136, 22,
     "umrla Maria PERDIRE [★★★ PEZDINC-GRAFIA-NIT-#8! KROP-'P-e-r-d-i-r-e'-črka-za-črko ≈ PEZDIR — VLM-'Perdiue/Perdiu'-t/d-zmeda-ZAVRJEN! veriga: 1877-z51-'Pezdinc' + 1878-×6-'Vezdirz/Pozdrin/Pecolar' → 1879-katastrofa!], 'Auszüglerin' [KROP-'Einzüglerin'], 62 LET [~62-J.] (März 29., pokop 30. — ★KROP-monotoničnost: 'April-29'-VLM-NEGRE-proti-z6-April-12!) — Lungenentzündung; previden (1); Ferdinand Hoggin 'Corp.' (KOGEJ-grafia!); + ★★★ h53-NIT-1876/77-×2: babica-Maria-62J-März-1876 + dojenček-Maria-1J-Okt-1877 (P200-z51)! h53 = PEZDIR-gospodinjstvo! + [z22]",
     "died Maria PERDIRE [★★★ the-PEZDINC-GRAFIA-THREAD-#8! KROP-'P-e-r-d-i-r-e'-letter-by-letter ≈ PEZDIR — VLM-'Perdiue/Perdiu'-REJECTED! the-chain: 1877-z51 + 1878-×6 → 1879-catastrophe!], 'Auszüglerin' [KROP], 62 YEARS [~] (März 29, buried 30 — ★the-KROP-monotonicity: 'April-29'-VLM-REJECTED-vs-z6-April-12!) — Lungenentzündung; previden (1); Ferdinand Hoggin 'Corp.' (the-KOGEJ-graphia!); + ★★★ the-h53-NIT-1876/77-×2: the-62J-grandmother-März-1876 + the-1J-infant-Okt-1877 (P200-z51)! h53 = the-PEZDIR-household! + [z22]"),
    ("46", 136, 24,
     "umrla Anna KLOBUČAR [~Klobucar-grafia], 'Matr.[?]Aufs.'[~], 2½ LET [~½-Jahre?-VLM-zmeda!] (April 12., pokop 13.) — 'Marbmil'[~Marasmus]; previden (1); Franz Dorgan [★★★ DOVGAN-1/3-1876!]; + ★ KLOBUČAR-nit-1876 (→ P199-'KLOBUČAR-h48'-1878!) + h46-1/2-1876 (→ z35-Mathias!) + [z24]",
     "died Anna KLOBUČAR [~the-Klobucar-graphia], 'Matr.[?]Aufs.'[~], 2½ YEARS [~½-Jahre?-VLM-confusion!] (Apr 12, buried 13) — 'Marbmil'[~Marasmus]; previden (1); Franz Dorgan [★★★ the-DOVGAN-1/3-1876!]; + ★ the-KLOBUČAR-thread-1876 (→ P199-'KLOBUČAR-h48'-1878!) + the-h46-1/2-1876 (→ z35-Mathias!) + [z24]"),
    ("23", 136, 26,
     "umrl Johann BONIE [~Borie-grafia-zmeda], 'Indiv.[?in-Ehe]Sohn'[~Baſe?], 5 LET (April 14., pokop 15.) — 'Husten such.'[?]; previden (1); Franz Dorgan [DOVGAN-2/3!]; + h23[~28?]-dvom-hišne-št.-dokumentiran + [z26]",
     "died Johann BONIE [~the-Borie-grafia-confusion], 'Indiv.[?in-Ehe]Sohn'[~], 5 YEARS (Apr 14, buried 15) — 'Husten such.'[?]; previden (1); Franz Dorgan [the-DOVGAN-2/3!]; + the-h23[~28?]-house-number-doubt-documented + [z26]"),
    ("34", 136, 30,
     "umrla Margaretha SILAK, 'neblige[?]½-Gribl.-Auszor'[~Auszügler-Tochter?], 9 LETE (Mai 14., pokop 15.) — Durchfall; previden (1); Ferdinand Hoggin 'Corp.' (KOGEJ!); + ★ SILAK-grafia (cf. z86-Pilah[~Spilak?] + 1877-z26-SINIEC-ŠIMEC-nit-kontekst!) + ZADNJA-GRIBLJE-s136 + [z30]",
     "died Margaretha SILAK, 'neblige[?]½-Gribl.-Auszor'[~Auszügler-daughter?], 9 YEARS (Mai 14, buried 15) — Durchfall; previden (1); Ferdinand Hoggin 'Corp.' (the-KOGEJ!); + ★ the-SILAK-graphia (cf. z86-Pilah[~Spilak?] + the-1877-SINIEC-context!) + the-last-GRIBLJE-on-s136 + [z30]"),
    ("70", 137, 32,
     "umrla Katharina [~KOLAR?], 'eheliche Tochter des Mathias [~Bezdive?Kögel?]'[~], 6½ LET (Mai 17., pokop 18.) — ★★★ MASERNFRIESEL (MASERN-nit-1876: cf. P199-×2-1878 + P200-z6-'Hrib'-h2!); previden (~); " + K + "; + h70[~]-dvom + [z32]",
     "died Katharina [~KOLAR?], 'eheliche Tochter des Mathias [?]'[~], 6½ YEARS (Mai 17, buried 18) — ★★★ MASERNFRIESEL (the-MASERN-thread-1876: cf. P199-×2-1878 + P200-z6!); previden (~); " + KE + "; + the-h70[~]-doubt + [z32]"),
    ("26", 137, 33,
     "umrl Peter BRINC, 'Gänßler'[?gans-drozd-grafia!], 36 LET (Mai 19., pokop 19. — ★pokop-isti-dan-smrti!) — Lungenentzündung; previden (1); " + K + "; + h26-nov-dokaz + [z33]",
     "died Peter BRINC, 'Gänßler'[?the-thrush-graphia!], 36 YEARS (Mai 19, buried 19 — ★the-burial-same-day-as-death!) — Lungenentzündung; previden (1); " + KE + "; + the-h26-new-proof + [z33]"),
    ("46", 137, 35,
     "umrl Mathias HLOBINAR [~Hlobučar?-grafia-zmeda — cf. z24-KLOBUČAR-h46!], '[~Hlobczen?]'-stan-glif, 72 LET (Mai 27., pokop 29.) — Asthma; previden (1); " + K + "; + ★★★ h46-×2-v-2-MESECIH-1876 (z24-Anna-Klobučar-April + z35-Mathias-Mai!) + [z35]",
     "died Mathias HLOBINAR [~Hlobučar?-the-graphia-confusion — cf. z24-KLOBUČAR-h46!], '[~Hlobczen?]'-the-glyph, 72 YEARS (Mai 27, buried 29) — Asthma; previden (1); " + KE + "; + ★★★ the-h46-×2-IN-2-MONTHS-1876 (z24-April + z35-Mai!) + [z35]"),
    ("12", 137, 36,
     "umrl Anton DRAGOŠ [★★★ KROP-'So des Joanes Dragoš' — sin-JOANESA-DRAGOŠA! VLM-'unehelich?'-ZAVRŽEN!], 'ehelicher Sohn des Joannes Dragoš' [KROP!], ¼ LETO [★★★ KROP-'¼ J.' — VLM-'2½ J.'-ZAVRJEN!] (Mai 28., pokop 29.) — Gehirnfieber; previden (~); " + K + "; + ★★★ DRAGOŠ-h12-NIT-1876/77 (z36-Anton-¼J-1876 → 1877-z56-Katharina-21J-h12! Joannes-Drigoš-otoka-×2!) + opora-DRAGOŠ-na-h12-pred-krstnim-prvencem-1892! + [z36]",
     "died Anton DRAGOŠ [★★★ KROP-'So des Joanes Dragoš' — the-son-of-JOANNES-DRAGOŠ! VLM-'unehelich?'-REJECTED!], 'ehelicher Sohn des Joannes Dragoš' [KROP!], ¼ YEAR [★★★ KROP-'¼ J.' — VLM-'2½ J.'-REJECTED!] (Mai 28, buried 29) — Gehirnfieber; previden (~); " + KE + "; + ★★★ the-DRAGOŠ-h12-THREAD-1876/77 (z36-Anton-¼J-1876 → 1877-z56-Katharina-21J! ×2-children-of-Joannes!) + the-support-for-DRAGOŠ-on-h12-before-the-1892-baptism! + [z36]"),
    ("49", 137, 40,
     "umrl Peter [BRODARIČ], 'ehelicher Sohn des Anton Brodarič ½ J.'[~grafia], 6 LET (Juni 18., pokop 20.) — Gehirnfieber; previden (~); " + K + "; + ★ Gehirnfieber-×2-klaster (z36 + z40-s137!) + [z40]",
     "died Peter [BRODARIČ], 'ehelicher Sohn des Anton Brodarič ½ J.'[~], 6 YEARS (Juni 18, buried 20) — Gehirnfieber; previden (~); " + KE + "; + ★ the-Gehirnfieber-×2-cluster (z36 + z40-on-s137!) + [z40]"),
    ("20", 138, 41,
     "umrl Mathias KERBICA, 'rufol.[?]Pajer-vda.-Peter-Kerbica'[~stan-zmeda], 2 MESECE (Juni 23., pokop 25.) — ★ FRISEN (FRISEN-nit-1/2!); previden (1); fortd. Jos. HOZJAN 'Capp.' (★★★ HOZJAN-Cappellan-1/2 — nov-duhovnik!); + KERBICA-družina-1/2 + [z41]",
     "died Mathias KERBICA, 'rufol.[?]Pajer-widow-Peter-Kerbica'[~], 2 MONTHS (Juni 23, buried 25) — ★ FRISEN (the-FRISEN-thread-1/2!); previden (1); fortd. Jos. HOZJAN 'Capp.' (★★★ the-HOZJAN-Cappellan-1/2 — the-new-priest!); + the-KERBICA-family-1/2 + [z41]"),
    ("64", 138, 43,
     "umrla Catharina KERBICA, vdova-Mathias-Kerbica ['rufol. Haušl. vda.'~], 1 LETO (Juni 28., pokop 29.) — ★ FRISEN (FRISEN-nit-2/2 — ★★★ ×2-v-6-DNEH-h20+h64!); previden (~); fortd. Jos. HOZJAN 'Capp.' (HOZJAN-2/2!); + KERBICA-družina-2/2 + [z43]",
     "died Catharina KERBICA, the-widow-of-Mathias-Kerbica ['rufol. Haušl. vda.'~], 1 YEAR (Juni 28, buried 29) — ★ FRISEN (the-FRISEN-thread-2/2 — ★★★ ×2-IN-6-DAYS-h20+h64!); previden (~); fortd. Jos. HOZJAN 'Capp.' (the-HOZJAN-2/2!); + the-KERBICA-family-2/2 + [z43]"),
    ("55", 139, 59,
     "umrl [?] dojenček, hči-[?]Magd.-Agnes-MARZIN [~Marin — KROP-s139_spodaj: '(Noth-)gemein(?) hči Magd. Agnes Marzin, dojenček'!], starost-[?] (August 25., pokop 26.) — 'Zo falge'[?kriptično — Noth-tauf[?]!]; previden (1); Justiniant Roggia 'Cœp.'[~grafia — nov-duhovnik-[?]!]; + ★★★ s139-TABELA-KONČA-PREK (9-vrstic + prazen-prostor — KROP!) + kriptičen-vpis-[?] + [z59]",
     "died [?] the-infant, the-daughter-of-[?]Magd.-Agnes-MARZIN [~Marin — the-KROP: '(Noth-)gemein(?) daughter-of-Magd.-Agnes-Marzin, the-infant'!], age-[?] (Aug 25, buried 26) — 'Zo falge'[?cryptic — Noth-tauf[?]!]; previden (1); Justiniant Roggia 'Cœp.'[~ — the-new-priest-[?]!]; + ★★★ the-s139-TABLE-ENDS-EARLY (9-rows + the-empty-space — KROP!) + the-cryptic-entry-[?] + [z59]"),
    ("52", 140, 66,
     "umrla Bartharina[~] PERŽHIR [~grafia], 'ehel. Toch.'[~], 27 LET (September 17., pokop 18.) — Wassersucht[~]; previden (1); Franz Dorgan [★★★ DOVGAN-3/3-1876!]; + h52-nov-dokaz + [z66]",
     "died Bartharina[~] PERŽHIR [~the-graphia], 'ehel. Toch.'[~], 27 YEARS (Sept 17, buried 18) — Wassersucht[~]; previden (1); Franz Dorgan [★★★ the-DOVGAN-3/3-1876!]; + the-h52-new-proof + [z66]"),
    ("18", 141, 78,
     "umrla Maria ŠIMEC [★★★ h18-ŠIMEC-NIT-3.-LETO! KROP-'Maria Simec, Mädchen'-jasno — VLM-'Zupančič?/Zimec?'-nesoglasje → NIT: 1876-Simec + 1877-Siniec + 1878-Innec? + 1881-TIMEC = 4-IMENA-4-LETI-NA-h18!], 'Mädchen' [KROP], 72¾ LET [★★★ KROP-'72 3/4'-soglasje-2/3 — KROP-2.-'74'-in-VLM-'72 2/5'-nesklajeni — [~]!] (October 25., pokop 27.) — Asthma; previden (1); Jožef Kogej 'coop.'[~ — edini-eksplicitni-'Kogej'-podpis-1876!]; + [z78]",
     "died Maria ŠIMEC [★★★ the-h18-ŠIMEC-THREAD-3rd-YEAR! KROP-'Maria Simec, Mädchen'-clear — VLM-'Zupančič?/Zimec?'-confusion → the-THREAD: 1876-Simec + 1877-Siniec + 1878-Innec? + 1881-TIMEC = 4-NAMES-4-YEARS-ON-h18!], 'Mädchen' [KROP], 72¾ YEARS [★★★ KROP-'72 3/4'-agreement-2/3 — [~]!] (Oct 25, buried 27) — Asthma; previden (1); Jožef Kogej 'coop.'[~ — the-only-explicit-'Kogej'-signature-1876!]; + [z78]"),
    ("8", 141, 79,
     "umrla Anna JAKOFČIČ [KROP — 'Jakopič'-VLM-varianta], stan-[?('½-let?-Wwe.-Wirt?'~zmeda)], 27½ LET [★★★ KROP-'27 1/2'-soglasje-2/3 — KROP-2.-'½ leta'-nesklajen — [~]!] (October 26., pokop 28. — ZADNJA-GRIBLJE-s141!) — Hirnhautentzündung [★★★ KROP — VLM-'Brustbekfinbar?'-ZAVRJEN!]; previden (1); Franz Dvorjan[~Dorgan?]; + ★ h8-JAKOFČIČ-NIT-1876/77 (→ 1877-z39-Catharina-JAKOFČIČ-9½mes-h8!) + [z79]",
     "died Anna JAKOFČIČ [KROP — the-'Jakopič'-VLM-variant], stan-[?], 27½ YEARS [★★★ KROP-agreement-2/3 — [~]!] (Oct 26, buried 28 — the-LAST-GRIBLJE-on-s141!) — Hirnhautentzündung [★★★ KROP — VLM-'Brustbekfinbar?'-REJECTED!]; previden (1); Franz Dvorjan[~Dorgan?]; + ★ the-h8-JAKOFČIČ-THREAD-1876/77 (→ 1877-z39-Catharina-9½-months-h8!) + [z79]"),
    ("44", 142, 83,
     "umrla Barbara ARNUETZ[?] [★★★ PRIMEK-NESOGLASJE-×3: 'Kavčič[?]'(VLM)/'Arnuetz[?]'(KROP-'legitimirana-hči-Antona')/'Struselj[?]'(KROP-2.) — [?]!], 24 URE [~starost-stolpec-izven-kropa!] (NOVEMBER 24., pokop 25. — ★★★ Dez→Nov-POPREVEK: VLM-'Dezember'-FALSIFICIRAN-kroz-KROP-'N-o-v-e-m-b-e-r.'!) — 'Vesperstmörfer'[?]; previden (~); 'subinuant Hogyi coop.' (KOGEJ-subst.!); + ★★★ s142-KRONOLOŠKA-NAPAKA-PISARJA (Nov-24-zapisan-PRED-Nov-12 — KROP-×2-potrjeno — 1.-pojav-v-korpusu!) + ★ h44-NIT (→ 1878-z77 + 1879-katastrofa!) + [z83]",
     "died Barbara ARNUETZ[?] [★★★ the-SURNAME-DISAGREEMENT-×3: 'Kavčič[?]'(VLM)/'Arnuetz[?]'(KROP)/'Struselj[?]'(KROP-2.) — [?]!], 24 HOURS [~] (NOVEMBER 24, buried 25 — ★★★ the-Dec→Nov-CORRECTION: the-VLM-'Dezember'-FALSIFIED-by-the-KROP-'N-o-v-e-m-b-e-r.'!) — 'Vesperstmörfer'[?]; previden (~); 'subinuant Hogyi coop.' (the-KOGEJ-subst.!); + ★★★ the-s142-CHRONOLOGICAL-SCRIBE-ERROR (Nov-24-written-BEFORE-Nov-12 — KROP-×2-confirmed — the-1st-in-the-corpus!) + ★ the-h44-THREAD (→ 1878-z77 + 1879-catastrophe!) + [z83]"),
    ("75", 142, 85,
     "umrl Joannes STUBLER, 'Schneider' [krojač!], 50⅔ LET (NOVEMBER 14., pokop 16. — Dez→Nov-POPREVEK!) — Asthma; previden (1); 'subinuant Hogyi coop.' (KOGEJ-subst.!); + ★ STUBL-nit (→ z12-s135-Maria-'Stublar'-Feb!) + [z85]",
     "died Joannes STUBLER, 'Schneider' [the-tailor!], 50⅔ YEARS (NOVEMBER 14, buried 16 — the-Dec→Nov-CORRECTION!) — Asthma; previden (1); 'subinuant Hogyi coop.' (the-KOGEJ-subst.!); + ★ the-STUBL-thread (→ z12-s135-Maria-'Stublar'-Feb!) + [z85]"),
    ("16", 142, 86,
     "umrla Anna PILAH [~SPILAK?-grafia-dvom — cf. z30-SILAK!], 'apost.Kath.[~] d. seel. Mathias und Anna' [starša-†!], 3¾ LET ('3 2/4 Jahre'!) (NOVEMBER 17., pokop 18. — Dez→Nov-POPREVEK!) — Hirnentzündung; previden (~); 'subinuant Hogyi coop.' (KOGEJ-subst.!); + ★ h16-NIT (→ P199-1878-z41!) + [z86]",
     "died Anna PILAH [~SPILAK?-the-graphia-doubt — cf. z30-SILAK!], 'apost.Kath.[~] d. seel. Mathias und Anna' [the-†-parents!], 3¾ YEARS ('3 2/4 Jahre'!) (NOVEMBER 17, buried 18 — the-Dec→Nov-CORRECTION!) — Hirnentzündung; previden (~); 'subinuant Hogyi coop.' (the-KOGEJ-subst.!); + ★ the-h16-THREAD (→ P199-1878-z41!) + [z86]"),
]

lines = []
lines.append("  // ——— P201: mrliška PREDZGODOVINA 04106, leto 1876 = 10. leto PREDZGODOVINSKE LINIJE (s134–s142 == Pag. 128–136, z1–z89 = 89 vpisov — vrstna-aritmetika 6+12+12+10+10+9+10+10+10 + meseci J6+F9+M6+A6+M10+J7+J5+A10+S16+O4+N10; pag == sken − 6, md5-križna-ta-seja: s142-svež == P200-disk-1:1 — veriga-P197→P198→P199→P200→P201-5.×!) — 20 GRIBLJE-blokov / 19 hiš (h46-×2!) ———")
lines.append("  // ★★★ MEJA 1875/76 = s134: TAIL-4-DEZ-1875-nad + VELIKA-'1876 Jänner'-GLAVA-V-SREDINI ('Jahr'-beseda!) + restart-Jänner-2.-pod (ordinali-NEVIDNI!) + ★★★ MEJA 1876/77 = s143-'18 77.'-ODREZANA (P200-reuse + TA-SEJA-RE-VERIFIKACIJA: smrt-1./pokop-8. + 'todt geboren' + restart-1 → P200-60-NETAKNJENA!) + ★★★ DECEMBER-1876 = 0-VPIISOV (Nov-30→Jän-1-31-dnevna-vrzel!) + ★★★ 40.-in-41.-POTRDITEV-invariante (s136-'1876.'-v-z1-celici-März + s142-'1876.'-v-z1-celici-NOVEMBER!) + ★★★ NOVEMBER-FALSIFIKACIJA (s142-'Dezember'-VLM-×2-KROP-FALSIFICIRAN — 'N-o-v-e-m-b-e-r.'-črka-za-črko! P200-lead-'Dez-tail'-POPREVEK!) + ★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-V-1876 (Hogeja/Hoggin/Hogyi-Coop-×9-Feb→Nov + eksplicitni-'Jožef-Kogej-coop.'-z78!) + DOVGAN-×3 + HOZJAN-Capp.-×2 + ROGGIA-×1 + ★★★ PEZDINC-GRAFIA-#8 (z22-'Perdire'-h53 — h53-NIT-×2: babica-62J + dojenček-1J!) + ★★★ DRAGOŠ-h12-NIT (z36-Anton-¼J-sin-Joanesa! → 1877-z56!) + ★★★ ŠIMEC-h18-NIT-3.-LETO (z78-'Simec' — 4-imena-4-leti!) + h46-×2-v-2-mesecih + h8-JAKOFČIČ-nit + FRISEN-×2-6-dneh (Kerbica-h20/h64!) + MASERN-z32 + KLOBUČAR-z24 + 24-URE-z83 (h44-NESOGLASJE-×3-ime!) + KRONOLOŠKA-NAPAKA-PISARJA (Nov-24-pred-Nov-12!) + otroška-umrljivost-55%-11/20 + dokaz research/issue17/parish-death-1876-04106.json (89-entries: 20-Griblje + 69-druge! 16-anomalij + 10-crossChecks + honesty-16 + tail-1875-×4-P202-lead!) + skripte: p201_fetch.py + p201_read_page.mjs + p201_crop.py + p201_build_entries.py + p201_build_proof.py ———")
for hisna, sken, zap, wsi, wen in BLOCKS:
    lines.append("  {")
    lines.append(f'    houseNo: "{hisna}",')
    lines.append('    bookSignature: "04106",')
    lines.append("    year: 1876,")
    lines.append(f"    scan: {sken},")
    lines.append(f"    page: {sken - 6},")
    lines.append(f'    whatSi: "{wsi}",')
    lines.append(f'    whatEn: "{wen}",')
    lines.append('    status: "DOCUMENTED",')
    lines.append("  },")
section = "\n".join(lines) + "\n"

out = src.replace(ANCHOR, section + ANCHOR, 1)
TS.write_text(out, encoding="utf-8")
print(f"OK — vstavljenih {len(BLOCKS)} blokov; TS {len(src)} → {len(out)} bajtov")
print("year-1876-blokov:", out.count("year: 1876,"))
