#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P200 — vstavi 8-GRIBLJE-blokov (04106, leto 1877) v parish.ts
PRED P199-sekcijo (newest-first vzorec). 8 vpisov / 8 hiš (vse-enkrat!)."""
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P199: mrliška PREDZGODOVINA 04106, leto 1878"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1877," not in src, "1877-bloki-že-obstajajo?!"

BLOCKS = [
    ("42", 145, 24,
     "umrla Catharina PESTOTNIK (KROP-'Catharina P...'-jasno!), '¼ Güblner[?]' [~stan-glif = ¼-Gütler], 53½ LET (KROP-'53 2/4 J'-frakcija ✓✓) (29. 4., pokop 1. 5. — ★★★ ULEDBA-#10-8.-INSTANCE: smrt-29-April → pokop-1-Mai-čez-mesečno-mejo! cf. P199-×7!) — Asthma (KROP-jasno!); previden (1); substituendus Hoggai[s] 'Coop.' (KROP-podpis = KOGEJ-subst.-grafia-P199-identična!); + ★★★ 1.-GRIBLJE-vpis-1877 (z22–z23-Zemelj-nad!) + glava-'1877.'-ZAPISANA-V-Z22-DATUMSKI-CELICI-nad (KROP = 39.-POTRDITEV-invariante 'glava-v-z1-celici-letnega-odseka' — VLM-'tail'-zastavica-NAPAČNI-ALARM!) + ★ KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ (1877-Mai! P199-'1878-Jänner–April'!) + [z24]",
     "died Catharina PESTOTNIK (KROP-name-clear!), '¼ Güblner[?]' [~the-glyph = ¼-Gütler], 53½ YEARS (KROP-'53 2/4 J'-fraction ✓✓) (Apr 29, buried Mai 1 — ★★★ the-FINDING-#10-8th-INSTANCE: death-Apr-29 → burial-Mai-1-across-the-month-boundary! cf. P199-×7!) — Asthma (KROP-clear!); previden (1); substituendus Hoggai[s] 'Coop.' (KROP-signature = the-KOGEJ-subst.-grafia-P199-identical!); + ★★★ the-1st-GRIBLJE-entry-1877 + the-'1877.'-head-WRITTEN-INSIDE-THE-Z22-DATE-CELL-above (KROP = the-39th-INVARIANT-CONFIRMATION — the-VLM-'tail'-flag-FALSE-ALARM!) + ★ the-KOGEJ-PERIOD-EXTENDED-BACK (1877-Mai!) + [z24]"),
    ("18", 145, 26,
     "umrla Barbara SINIEC [★ŠIMEC-GRAFIA! — VLM-soglasje; cf. 1878-z32/z44-Simec + 1881-h18-TIMEC!], '¼ G. s[p]elinq: daughter' [~KROP = ¼-Gütler's-hči!], 8½ LET (KROP-'8½ J.' ✓) (8. 5., pokop 9. 5.) — Abzehrung (KROP-'Anbzoforning'-grafia-jasno!); previden (~); substituendus Hoggai[s] 'Coop.' (KROP!); + ★★★ h18-ŠIMEC-NIT-1877 (→ 1878-z1-Theresia-INNEC?-h18 + 1881-h18-TIMEC — INNEC/SIMEC/TIMEC-GRAFIA-DVOJNIČKA-3-LETNA-NA-h18!) + ★ KOGEJ-subst.-2/2-1877-Griblje + [z26]",
     "died Barbara SINIEC [★the-ŠIMEC-GRAFIA! — VLM-agrees; cf. 1878-z32/z44-Simec + 1881-h18-TIMEC!], '¼ G. s[p]elinq: daughter' [~KROP = ¼-Gütler's-daughter!], 8½ YEARS (KROP-'8½ J.' ✓) (Mai 8, buried Mai 9) — Abzehrung (KROP-'Anbzoforning'-grafia-clear!); previden (~); substituendus Hoggai[s] 'Coop.' (KROP!); + ★★★ the-h18-ŠIMEC-THREAD-1877 (→ 1878-z1-Theresia-INNEC?-h18 + 1881-h18-TIMEC — the-INNEC/SIMEC/TIMEC-GRAFIA-TWIN-3-YEAR-on-h18!) + ★ KOGEJ-subst.-2/2-1877-Griblje + [z26]"),
    ("8", 146, 39,
     "umrla Catharina JAKOFČIČ (KROP ✓ — VLM-soglasje!), 'nepol. Tochter des Gübln[er]s: Johann und Anna, ¼ G.' [KROP-2-vrstici!], 9½ MESECEV (KROP-'9½ Mon.' ✓) (2. 8., pokop 4. 8. — 'August'-glava-v-vrstici!) — Hirnfall (KROP-jasno!); previden (~); Franz Dovgan (KROP-podpis-dvojna-črta!); + ★ h8-NOV-dokaz-1877 (v-1878-BREZ-h8-vpisov!) + ★★★ JAKOFČIČ-×2-1877 (→ z52-Anna-h6!) + ★ VLM-v5/v6-DRIFT-popravek (VLM-je-vrste-premaknil — real-v6 = TA! 'Certoviše-h8-Anna-Jakofčič-¼güblnwitwe'-nad = druga-vrsta!) + [z39]",
     "died Catharina JAKOFČIČ (KROP ✓ — VLM-agrees!), 'nepol. Tochter des Gübln[er]s: Johann und Anna, ¼ G.' [KROP-2-lines!], 9½ MONTHS (KROP-'9½ Mon.' ✓) (Aug 2, buried Aug 4 — the-'August'-head-in-row!) — Hirnfall (KROP-clear!); previden (~); Franz Dovgan (KROP-double-line-signature!); + ★ the-h8-NEW-proof-1877 (in-1878-NO-h8-entries!) + ★★★ the-JAKOFČIČ-×2-1877 (→ z52-Anna-h6!) + ★ the-VLM-v5/v6-DRIFT-correction + [z39]"),
    ("62", 147, 48,
     "umrla Barbara HURE [~KURE-grafia! VLM-'Hurie'-varianta — cf. 1878-z9-Marcus-Kure[~Hure]-h10!], 'Erbin des Anton, ¼ G.' [~KROP-'lrb Anton... ¼ J.'-grafia], 3¼ LETI [KROP-'3¼'-frakcija — VLM-'3½'-ZAVRJEN-γ-frakcija! — 2.-3½→3¼-POPRAVEK-ta-seja!] (1. 10., pokop 3. 10. — 'October'-glava-v-z48-celici-KROP!) — 'Br[a]stfbrand'[?KROP-neberljivo-fraza; VLM-'Brennfieber'-ZAVRJEN]; previden (~); Franz Dovgan (KROP-podpis-velik!); + ★★★ 'Br[a]stfbrand'-KLASTER-1/3 (z48+z49+z52-zaporedoma-OKTOBER!) + ★ h62-nov-dokaz (1878-BREZ-h62!) + ★★★ GRIBLJE-OTROK-UMRL-×4-1877 (z39-9½mes + z48-3¼J + z51-1J + z52-3¾J = 50%-otroška-umrljivost-Griblje-1877!) + [z48]",
     "died Barbara HURE [~the-KURE-grafia! VLM-'Hurie'-variant — cf. 1878-z9-Marcus-Kure[~Hure]!], 'Erbin des Anton, ¼ G.' [~KROP-grafia], 3¼ YEARS [KROP-'3¼'-fraction — VLM-'3½'-REJECTED-γ-fraction!] (Oct 1, buried Oct 3 — the-'October'-head-in-z48-cell-KROP!) — 'Br[a]stfbrand'[?KROP-unreadable; VLM-'Brennfieber'-REJECTED]; previden (~); Franz Dovgan (KROP-big-signature!); + ★★★ the-'Br[a]stfbrand'-CLUSTER-1/3 (z48+z49+z52-consecutive-OKTOBER!) + ★ the-h62-new-proof + ★★★ GRIBLJE-CHILD-DEATHS-×4-1877 (50%-child-mortality!) + [z48]"),
    ("57", 147, 49,
     "umrl Johann LOZAR (KROP-jasno!), 'des Michael, Gütler' [~KROP-'Sed Michael...'-grafia = Sohn/Erbe?], 2 LETI (KROP-'2 J.' ✓) (4. 10., pokop 5. 10.) — 'Br[a]stfbrand'[?isti-word-kot-z48!]; previden (~); Franz Dovgan (KROP-podpisan!); + ★★★ h57-NIT-1877 (→ 1878-z80-Maria-LOGAR-h57-17J-GEHIRNENTZÜNDUNG! — h57-2-leta-zaporedoma-2-smrti!) + ★ 'Br[a]stfbrand'-KLASTER-2/3 + ordinal-'5'-viden-v-datumskem-stolpcu-pod (KROP — z49-burial-'5'!) + [z49]",
     "died Johann LOZAR (KROP-clear!), 'des Michael, Gütler' [~KROP = Sohn/Erbe?], 2 YEARS (KROP-'2 J.' ✓) (Oct 4, buried Oct 5) — 'Br[a]stfbrand'[?same-word-as-z48!]; previden (~); Franz Dovgan (KROP!); + ★★★ the-h57-THREAD-1877 (→ 1878-z80-Maria-LOGAR-h57-GEHIRNENTZÜNDUNG! — h57-two-deaths-in-two-years!) + ★ the-'Br[a]stfbrand'-CLUSTER-2/3 + [z49]"),
    ("53", 147, 51,
     "umrla Maria PEZDINC [★★★ PEZDINC-GRAFIA-NIT-#7! KROP-'Pezdinc'-jasno — VLM-'Perdinc'-t/d-zmeda-ZAVRJEN! — veriga: 1878-×6-'Vezdirz/Pozdrin/Pezdir(e)/Pecolar' → 1879-katastrofa-h40/h44!], 'nepol. Tochter des Johann und [der] Anna, ½ G.' [KROP-2-vrstici!], 1 LETO (KROP-'1 Jahr' ✓) (15. 10., pokop 16. 10.) — Wasserfriesl (KROP-jasno! VLM-soglasje — 'friesl'-grafia = ★FRISELN-nit!); previden (~); Franz Dovgan (KROP-podpis-dvojna!); + ★★★ h53-NIT-1877 (→ 1878-z83-Mathias-PEGLAVC-h53-87J! — h53-2-smrti-v-2-letih!) + ordinal-'5|16'-KROP-datum + [z51]",
     "died Maria PEZDINC [★★★ the-PEZDINC-GRAFIA-THREAD-#7! KROP-clear — VLM-'Perdinc'-REJECTED! — the-chain: 1878-×6 → 1879-catastrophe!], 'nepol. Tochter des Johann und [der] Anna, ½ G.' [KROP-2-lines!], 1 YEAR (KROP-'1 Jahr' ✓) (Oct 15, buried Oct 16) — Wasserfriesl (KROP-clear! VLM-agrees — the-'friesl'-grafia = ★the-FRISELN-thread!); previden (~); Franz Dovgan (KROP-double!); + ★★★ the-h53-THREAD-1877 (→ 1878-z83-PEGLAVC-87J!) + [z51]"),
    ("6", 147, 52,
     "umrla Anna JAKOFČIČ (KROP — VLM-'Jakopič'-ZAVRJEN! — ★JAKOFČIČ-×2-1877-2/2!), 'nepol. Tochter des Mathias und [der] Anna, ¼ G.' [KROP!], 3¾ LETI (KROP-'3¾'-frakcija-jasno!) (17. 10., pokop 18. 10.) — 'Br[a]stfbrand'[?isti-word-klaster-3/3!]; previden (~); Franz Dovgan (KROP!); + ★ h6-REŠENO ('6'-samo — VLM-'h6[~46?]'-dvom-razrešen!) + ★ h6-nov-dokaz (1878-BREZ-h6!) + ★★★ 'Br[a]stfbrand'-KLASTER-3/3 + ZADNJA-GRIBLJE-s147 + [z52]",
     "died Anna JAKOFČIČ (KROP — VLM-'Jakopič'-REJECTED! — ★the-JAKOFČIČ-×2-1877-2/2!), 'nepol. Tochter des Mathias und [der] Anna, ¼ G.' [KROP!], 3¾ YEARS (KROP-'3¾'-fraction-clear!) (Oct 17, buried Oct 18) — 'Br[a]stfbrand'[?same-word-cluster-3/3!]; previden (~); Franz Dovgan (KROP!); + ★ the-h6-RESOLVED ('6'-only!) + ★ the-h6-new-proof + ★★★ the-'Br[a]stfbrand'-CLUSTER-3/3 + the-last-GRIBLJE-on-s147 + [z52]"),
    ("12", 148, 56,
     "umrla Katharina DRAGOŠ [KROP-'Dragoš'-š-čarec; VLM-'Dragos'-soglasje], 'lbb.'[?KROP-abb-neberljivo], 21 LET [KROP-'21'-2/7-KURRENT-zmeda-'71'; VLM-'21'-soglasje → 21!] (1. 11., pokop 3. 11.) — 'Alt___sfr____'[?KROP-neberljivo; VLM-'Albrandstbrünst[~]'-nesoglasje-2-kandidata]; previden (1); Franz Dovgan (KROP-podpis-dvojni-flourish!); + ★★★ h12-DEFINITIVNO (KROP-'12'-10×-JASNO — ★★★ P199-'h18[?]'-POPREVEK! — h18-nit-referenca-v-P199-z1-bloku-OSLABLJENA-na-'samo-1878-Innec!') + P199-REUSE-tail_1877-1:1 (md5-križna-validacija-ta-seja: s148-svež == P199-disk-1:1!) + ★ ZADNJA-GRIBLJE-1877 + [z56]",
     "died Katharina DRAGOŠ [KROP-š-glyph; VLM-agrees], 'lbb.'[?KROP-abb-unreadable], 21 YEARS [KROP-'21'-the-2/7-KURRENT-confusion-'71'; VLM-'21'-agrees → 21!] (Nov 1, buried Nov 3) — 'Alt___sfr____'[?KROP-unreadable; VLM-'Albrandstbrünst[~]'-2-candidates]; previden (1); Franz Dovgan (KROP-double-flourish-signature!); + ★★★ the-h12-DEFINITIVE (KROP-'12'-10×-CLEAR — ★★★ the-P199-'h18[?]'-CORRECTION!) + the-P199-REUSE-tail_1877-1:1 (the-md5-cross-validation: s148-fresh == P199-disk-1:1!) + ★ the-LAST-GRIBLJE-1877 + [z56]"),
]

lines = []
lines.append("  // ——— P200: mrliška PREDZGODOVINA 04106, leto 1877 = 9. leto PREDZGODOVINSKE LINIJE (s142–s148 == Pag. 136–142, z1–z60 = 60 vpisov — vrstna-aritmetika 11+10+12+10+9+8 + datum-veriga-continuous!; pag == sken − 6, md5-križna-ta-seja: s148/s149-sveže == P199-disk-1:1 — veriga-P197→P198→P199→P200-4.×!) — 8 GRIBLJE-blokov / 8 hiš ———")
lines.append("  // ★★★ MEJA 1876/77 = s143-top: '18 77.'-glava-ODREZANA-off-scan (scan-edge!) — restart-evidenca: s142-Dez-1876-nad + Jänner-pod + z1-pokop-'1.'; ★★★ 39.-POTRDITEV-invariante = s145-'1877.'-glava-ZAPISANA-V-Z22-DATUMSKI-CELICI (mid-year-glava-vrsta — VLM-'tail'-NAPAČNI-ALARM!) + MEJA 1877/78 = s149 (P199-38.-reuse!) + konec-1877 = z60 (s148-v8: Dez 21.) + ★ ORDINALI-NEVIDNI-na-vseh-6-straneh (forma-brez-stolpca/scan-edge) → ŠTEVJE-IZ-VRSTIC (recept-s148-2.×!) — P199-'1877 ≈ 85-?'-FALSIFICIRANA (60!) + ★★★ 'HRIBLE'[?='Hrib'?]-NOVA-LOKALNOST-×3 (z3/z6/z7-Tomc-klaster-h2/h2/h1 — 1.-pojav-v-korpusu! G-glyph-duel-3.×-POZITIVEN: ≠Gradac-G + ≠s145-Griblje-G + ≠z4-'Gribl[j]ar'-G-vsi-descender-G! cf. 'Ukolk'[?]-1878!) + ★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ (substituendus-Hoggai-Coop-1877-Jänner→Mai: z2/z8/z9/z11 + Griblje-z24/z26! P199-'1878-Jänner–April'-RAZŠIRJENA!) + Franz-DOVGAN-dominanta (Griblje-×6!) + NO-Jančar-1877 (★★★ JANČAR-NIT-1878→1883-SPREMENJENA!) + ★★★ PEZDINC-GRAFIA-#7 (z51-h53!) + ★★★ 'Br[a]stfbrand'[?]-KLASTER-×3-OKTOBER (z48/z49/z52-zaporedoma!) + ★★★ GRIBLJE-OTROŠKA-UMRLJIVOST-50%-1877 (4/8-otroci!) + ★★★ ULEDBA-#10-8.-INSTANCE (z24: 29-April→1-Mai!) + ★★★ h12-DEFINITIVNO (P199-'h18[?]'-POPREVEK!) + h18-ŠIMEC-NIT-1877 (z26-Siniec! INNEC/SIMEC/TIMEC-3-LETNA!) + h53/h57/h44(1876-tail!)-NITI + MASERN-z6-'Hrib'-h2 + FRAISEN-z3 + Wasserfriesl-z51 (FRISELN-nit-kontekst!) + VLM-KROP-korekcije-×7 (frakcije-3½→3¼-×2 + h18→h12 + 'Kreuzsteing'→'Abzehrung' + VLM-v5/v6-DRIFT + 'Jakopič'→'Jakofčič' + h6[~46?]→h6!) + dokaz research/issue17/parish-death-1877-04106.json (60-entries: 8-Griblje + 3-'Hrib'[?] + tail-1876-×3-GRIBLJE-P201-lead! 13-anomalij + 10-crossChecks + honesty-16 + lead-P201-1876!) + skripte: p200_fetch.py + p200_read_page.mjs + p200_crop.py + p200_build_entries.py + p200_build_proof.py ———")
for hisna, sken, zap, wsi, wen in BLOCKS:
    lines.append("  {")
    lines.append(f'    houseNo: "{hisna}",')
    lines.append('    bookSignature: "04106",')
    lines.append("    year: 1877,")
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
print("year-1877-blokov:", out.count("year: 1877,"))
