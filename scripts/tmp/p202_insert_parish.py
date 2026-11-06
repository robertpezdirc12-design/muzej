#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 — vstavi 10-GRIBLJE-blokov (04106, leto 1875) v parish.ts PRED P201-sekcijo
(newest-first vzorec). 10 vpisov / 10 hiš (5 NOVIH: h11/h35/h45/h59/h72!)."""
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P201: mrliška PREDZGODOVINA 04106, leto 1876"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1875," not in src, "1875-bloki-že-obstajajo?!"

KOGEJ = "KOGEJ-NIT-'provinciat'-RANK-1875 (Hogeyu/Kooci/Bogija-Coop.-grafia!)"
KOGEJ_EN = "the-KOGEJ-THREAD-'provinciat'-RANK-1875 (Hogeyu/Kooci/Bogija-Coop.-the-graphia!)"

BLOCKS = [
    ("59", 128, 9,
     "umrl Georg PEGLINC[?BEZDIRA?] [★★★ PEZDIR-GRAFIA-DUEL-#1-1875! KROP-'Griblje 59. Georg-P-e-g/d-linc' — 'Peglinc'-vs-'Bezdira'-[?] — NIT-kontekst: PEZDINC-h53-1876/77 → h59-nov-PEZDIR-kandidat-[?]!], 'gmüth[?]'-stan-glif, 40 LET (März 6., pokop 8.) — Asthma; previden (1); [~]-Coop. (KOGEJ-grafia!); + ★★★ h59-NOVA-hiša (1.-dokaz-kadarkoli!) + ZIMSKI-KLASTER-März-×4 (z9/z11/z17/z18!) + [z9]",
     "died Georg PEGLINC[?BEZDIRA?] [★★★ the-PEZDIR-GRAFIA-DUEL-#1-1875! KROP-'Griblje 59. Georg-P-e-g/d-linc' — [?]-the-THREAD-context: PEZDINC-h53-1876/77 → h59-the-new-PEZDIR-candidate-[?]!], 'gmüth[?]'-the-glyph, 40 YEARS (März 6, buried 8) — Asthma; previden (1); [~]-Coop. (the-KOGEJ-graphia!); + ★★★ h59-NEW-HOUSE (the-1st-proof-ever!) + the-WINTER-CLUSTER-März-×4 (z9/z11/z17/z18!) + [z9]"),
    ("45", 128, 11,
     "umrl Mathias RIÜNZFLIßLER[?RINZBIßLER?] [grafia-[?]! KROP-'Griblje 45. Mathias'-jasno!], 'Sohn-der-Anna-Braußsche, ½ J. vne. Auszüglerin'[~], 2 MESECE (März 8., pokop 9.) — Wassersucht[?] (cf. h53-WASSERSUCHT-nit-1877/78!); previden (1); [~]-Coop. (KOGEJ-grafia!); + ★★★ h45-NOVA-hiša (1.-dokaz-kadarkoli!) + BRAUŠ-mama (→ z40-h72-Marcus-Brauše — BRAUŠ-NIT-×2-1875!) + otrok-jasen + [z11]",
     "died Mathias RIÜNZFLIßLER[?RINZBIßLER?] [the-graphia-[?]! KROP-'Griblje 45. Mathias'-clear!], 'the-son-of-Anna-Braußsche, ½ J. vne. Auszüglerin'[~], 2 MONTHS (März 8, buried 9) — Wassersucht[?] (cf. the-h53-WASSERSUCHT-THREAD-1877/78!); previden (1); [~]-Coop. (the-KOGEJ-graphia!); + ★★★ h45-NEW-HOUSE (the-1st-proof-ever!) + the-BRAUŠ-mother (→ z40-h72-Marcus-Brauše — the-BRAUŠ-THREAD-×2-1875!) + the-clear-child + [z11]"),
    ("31", 129, 17,
     "umrla Maria KAMBIČ, Kurpašnič[?] [KROP-'Griblje 31.'-jasno!], '¼ Gribl. Taglöhnerin'-stan-glif, 24⅞ [★ KROP-'24 7/8' — VLM-'24 tj.'-FALSIFICIRAN! enota-leta/tednov-NEJASNA-[?] — MEJNI-OTROK-[?]!] (März 21., pokop 23.) — 'Brüzframenghfak][?kriptično]'; previden (1); provinciat Hogeyu Coop. (★★★ " + KOGEJ + "); + ★★★ h31-nit-RAZŠIRJENA-NAZAJ (→ 1881 + 1885!) + ZIMSKI-KLASTER-März + isti-datumi-kot-z18 (21./23.!) + [z17]",
     "died Maria KAMBIČ, Kurpašnič[?] [KROP-'Griblje 31.'-clear!], '¼ Gribl. Taglöhnerin'-the-glyph, 24⅞ [★ KROP-'24 7/8' — VLM-'24 tj.'-REJECTED! the-unit-years/weeks-UNCLEAR-[?] — the-borderline-child-[?]!] (März 21, buried 23) — 'Brüzframenghfak][?cryptic]'; previden (1); provinciat Hogeyu Coop. (★★★ " + KOGEJ_EN + "); + ★★★ the-h31-THREAD-EXTENDED-BACK (→ 1881 + 1885!) + the-WINTER-CLUSTER-März + the-same-dates-as-z18 (21./23.!) + [z17]"),
    ("17", 129, 18,
     "umrla Anna KRAUS, ansl. hči Josusa/Južefa Krausa [KROP-'Griblje 17.'-jasno!], 'nep.l. hči ... ½ j.'[~], 24 [★ enota-[?]-leta/tednov-NEJASNA! + '¾ J.'-glif-V-IMENSKEM-STOLPCU — pisarjeva-napaka-[?]!] (März 21., pokop 23.) — 'Blattronn[?Blatkronn-kriptično]'; previden (1); provinciat Kooci Coop. (★★★ EKSPLICITNO-'Kooci'-grafia = " + KOGEJ + "); + ★★★ h17-nit-RAZŠIRJENA-NAZAJ (→ 1881 + 1884!) + isti-datumi-kot-z17 + [z18]",
     "died Anna KRAUS, ansl. the-daughter-of-Josus/Južef-Kraus [KROP-'Griblje 17.'-clear!], 'nep.l. daughter ... ½ j.'[~], 24 [★ the-unit-[?]-years/weeks-UNCLEAR! + the-'¾ J.'-glyph-IN-THE-NAME-COLUMN — the-scribe-error-[?]!] (März 21, buried 23) — 'Blattronn[?Blatkronn-cryptic]'; previden (1); provinciat Kooci Coop. (★★★ the-EXPLICIT-'Kooci'-graphia = " + KOGEJ_EN + "); + ★★★ the-h17-THREAD-EXTENDED-BACK (→ 1881 + 1884!) + the-same-dates-as-z17 + [z18]"),
    ("35", 130, 27,
     "umrl Miha NEMANIČ [★★★ KROP-FALSIFIKACIJA-VLM-#9! VLM-'Matthea-Klemencic-43J'-ŽENSKO-ime → KROP-'14./16.-Griblje-35.-Miha-Nemanič, gründbm'-MOŠKO-ime-potrjeno!], 'gründbm[?Güntblom-kriptično]', 43 [J.] (April 14., pokop 16.) — Typhus; previden-drei[?]; Franz Dovgan (DOVGAN-dominanta!); + ★★★ h35-NOVA-hiša (1.-dokaz-kadarkoli!) + [z27]",
     "died Miha NEMANIČ [★★★ the-KROP-FALSIFICATION-VLM-#9! VLM-'Matthea-Klemencic-43J'-the-FEMALE-name → KROP-'14./16.-Griblje-35.-Miha-Nemanič, gründbm'-the-MALE-name-confirmed!], 'gründbm[?Güntblom-cryptic]', 43 [J.] (April 14, buried 16) — Typhus; previden-drei[?]; Franz Dovgan (the-DOVGAN-dominance!); + ★★★ h35-NEW-HOUSE (the-1st-proof-ever!) + [z27]"),
    ("22", 130, 31,
     "umrla Maria MIHEL[?] [grafia-[?]], 'rspł. Hufb.'[~], 4½ MESECEV (Mai 13., pokop 15.) — Krämpfe; previden (1); Ferdinand Hoger, Coop. (HOZJAN-variante!); + ★ h22-nit-RAZŠIRJENA-NAZAJ (→ 1880!) + otrok-jasen + [z31]",
     "died Maria MIHEL[?] [the-graphia-[?]], 'rspł. Hufb.'[~], 4½ MONTHS (Mai 13, buried 15) — Krämpfe; previden (1); Ferdinand Hoger, Coop. (the-HOZJAN-variant!); + ★ the-h22-THREAD-EXTENDED-BACK (→ 1880!) + the-clear-child + [z31]"),
    ("72", 131, 40,
     "umrl Joannes, ansl. sin Marcusa BRAUŠA [★★★ KROP-'Griblje 72.'-KURRENT-DUEL-RAZREŠEN: h72-NE-h73! 2/3-soglasje!], 'Kitfl. [?]', 5 TEDNOV (Juni 19., pokop 20.) — Frisen[~] (FRISEN-NIT-1/2!); previden (1); Ferdinand Hozjan Coop. (HOZJAN-'Coop.'-1875 — P201-'Capp.'-1876-RAZŠIRJENO-NAZAJ!); + ★★★ h72-NOVA-hiša (1.-dokaz-kadarkoli!) + BRAUŠ-oče (→ z11-h45-Anna-Braußsche — NIT-×2!) + otrok-jasen + [z40]",
     "died Joannes, ansl. the-son-of-Marcus-BRAUŠ [★★★ KROP-'Griblje 72.'-the-KURRENT-DUEL-RESOLVED: h72-NOT-h73! 2/3-agreement!], 'Kitfl. [?]', 5 WEEKS (Juni 19, buried 20) — Frisen[~] (the-FRISEN-THREAD-1/2!); previden (1); Ferdinand Hozjan Coop. (HOZJAN-'Coop.'-1875 — the-P201-'Capp.'-1876-EXTENDED-BACK!); + ★★★ h72-NEW-HOUSE (the-1st-proof-ever!) + the-BRAUŠ-father (→ z11-h45-Anna-Braußsche — the-THREAD-×2!) + the-clear-child + [z40]"),
    ("5", 132, 54,
     "umrl Joanes ŠTUZEL[?STURZEL] [grafia-dvom! KROP-'Griblje 5.'-jasno!], '¼ Gübler'-stan-glif, 34 LET (October 2., pokop 4.) — Rückfalls-Krankheit[?]; previden (1); Jožef Vogrin[?] Coop.; + ★★★ h5-nit-RAZŠIRJENA-NAZAJ (1875 → 1880 + 1885 — 10-LETNA-NIT!) + oktobrski-Griblje-vpis + [z54]",
     "died Joanes ŠTUZEL[?STURZEL] [the-graphia-doubt! KROP-'Griblje 5.'-clear!], '¼ Gübler'-the-glyph, 34 YEARS (October 2, buried 4) — Rückfalls-Krankheit[?]; previden (1); Jožef Vogrin[?] Coop.; + ★★★ the-h5-THREAD-EXTENDED-BACK (1875 → 1880 + 1885 — the-10-YEAR-THREAD!) + the-October-Griblje-entry + [z54]"),
    ("69", 133, 59,
     "umrl Georg HUSIC [★★★ GEORG-HUSIČ-DUEL-s133: z58-Gradac-37J-Okt-26/28 + z59-GRIBLJE-27J-Nov-26/28 — ISTA-imena + ISTI-dnevi-RAZLIČEN-mesec — 2-ločeni-vpisa-KROP + [~]-dvojnost-dokumentirana!], 'kath. Befs. [Bauer?]', 27 LET (November 26., pokop 28. — glava-'November'-v-z2-celici!) — Fraisen/Schlagfluß[?] (FRISEN-NIT-2/2!); previden (1); Feldkurat Bogija, Corp. (KOGEJ-grafia!); + ★★★ h69-nit-RAZŠIRJENA-NAZAJ (→ 1882 + 1884 — 9-LETNA-NIT!) + '1875'-glava-V-Z1-CELICI-s133 = 44.-POTRDITEV-invariante (VIOLETNA-TINTA!) + [z59]",
     "died Georg HUSIC [★★★ the-GEORG-HUSIČ-DUEL-s133: z58-Gradac-37J-Oct-26/28 + z59-GRIBLJE-27J-Nov-26/28 — the-SAME-names + the-SAME-days-different-month — 2-separate-entries-KROP + [~]-the-duality-documented!], 'kath. Befs. [Bauer?]', 27 YEARS (November 26, buried 28 — the-'November'-header-in-the-z2-cell!) — Fraisen/Schlagfluß[?] (the-FRISEN-THREAD-2/2!); previden (1); Feldkurat Bogija, Corp. (the-KOGEJ-graphia!); + ★★★ the-h69-THREAD-EXTENDED-BACK (→ 1882 + 1884 — the-9-YEAR-THREAD!) + the-'1875'-header-IN-THE-Z1-CELL-s133 = the-44th-CONFIRMATION-invariant (VIOLET-INK!) + [z59]"),
    ("11", 134, 71,
     "umrla Catharina KUNIĆ[~Kuniz?] geb. JAKOŠ, vne. Podžemljanova[~] [★★★ P201-lead-NAPVED-1:1-POTRJENA ('z4-h11-KUNIĆ-65J-Dez-24/26')!], 'Witwe[~ Alstglaubin?]', 65 J. (December 24., pokop 26. — ZADNJA-GRIBLJE-1875!) — Asthma; previden (1); Ferdinand Hočevar Coop. (HOZJAN-variante!); + ★★★ h11-NOVA-hiša (1.-dokaz-kadarkoli!) + KUNIĆ/JAKOŠ-NIT-1.-dokaz + P201-tail-×4-1:1 (z68–z71 == 14/16 + 22/23 + 22/24 + 24/26!) + [z71]",
     "died Catharina KUNIĆ[~Kuniz?] née JAKOŠ, vne. Podžemljanova[~] [★★★ the-P201-lead-PREDICTION-1:1-CONFIRMED ('z4-h11-KUNIĆ-65J-Dez-24/26')!], 'Witwe[~ Alstglaubin?]', 65 Y. (December 24, buried 26 — the-LAST-GRIBLJE-1875!) — Asthma; previden (1); Ferdinand Hočevar Coop. (the-HOZJAN-variant!); + ★★★ h11-NEW-HOUSE (the-1st-proof-ever!) + the-KUNIĆ/JAKOŠ-THREAD-1st-proof + the-P201-tail-×4-1:1 (z68–z71 == 14/16 + 22/23 + 22/24 + 24/26!) + [z71]"),
]

lines = []
lines.append("  // ——— P202: mrliška PREDZGODOVINA 04106, leto 1875 = 11. leto PREDZGODOVINSKE LINIJE (s127-z11–s134-z4 == Pag. 121–128, z1–z71 = 71 vpisov — vrstna-aritmetika 1+11+10+13+12+10+10+4 + meseci J3+F3+M15-MAX+A7+M6+J6+J1-MIN+A6+S6+O4+N8+D5; pag == sken − 6, md5-križna-ta-seja: s134-svež == P201-disk-1:1 — veriga-P197→…→P202-6.×!) — 10 GRIBLJE-blokov / 10 hiš (★★★ 5-NOVIH: h11/h35/h45/h59/h72!) ———")
lines.append("  // ★★★ MEJA 1874/75 = s127: TAIL-10-NOV/DEZ-1874-nad (2-Griblje: Krič[?] + Miler[?]!) + 'Jänner 1875'-glava-V-Z11-CELICI (42.-POTRDITEV! z-letom!) + z1-ULEDBA (31-Dez-1874-smrt → 2-Jän-1875-pokop!) + ★★★ MEJA 1875/76 = s134 (P201-REUSE-1:1-MD5: TAIL-4-DEZ-1875-nad + VELIKA-'1876 Jänner'-glava!) + ★★★ GLAVE-V-CELICAH-×6-korpus-REKORD: 42.-Jänner-s127-z11 + 43.-März-s128-z6 + 44.-'1875'-s133-z1 (KROP-eksplicitno — VIOLETNA-TINTA!) + Juli-s131-z6 + November-s133-z2 + Dezember-s133-z10! + ★★★ KOGEJ-OBDOBJE-3.-RAZŠIRITEV-NAZAJ ('provinciat'-RANK-1875: Hogeyu/Kooci/Bogija-Coop. — 1875→1876→1877-neprekinjeno!) + ★★★ DOVGAN-DOMINANTA-×23 (NAJVEČJA-letnica!) + HOZJAN-VARIANTE-×14 (Hoger/Hozjan/Hočevar!) + ★★★ 5-NOVIH-HIŠ-REKORD + PEZDIR-GRAFIA-DUEL-#1 (z9-'Peglinc[?Bezdira?]'-h59!) + KROP-FALSIFIKACIJA-VLM-#9 (z27-'Miha-Nemanič'-moško-NE-'Matthea-Klemencic'!) + GEORG-HUSIČ-DUEL-s133 (Gradac-37J + Griblje-27J — isti-dnevi!) + BRAUŠ-NIT-×2 (z11-mama + z40-oče!) + h72-KURRENT-DUEL-RAZREŠEN (h72-NE-h73!) + '24'-ENOTA-ZMEDA-×2 (z17/z18 — leta/tednov-[?]!) + 'Feber'-GRAFA-×3 + FRISEN-×2 + otroška-umrljivost-30%-3/10-jasna (+2-[?]-mejna!) + niti-RAZŠIRJENE-NAZAJ: h5-10-let + h69-9-let + h17/h22/h31 + dokaz research/issue17/parish-death-1875-04106.json (71-entries: 10-Griblje + 61-druge! 14-anomalij + 10-crossChecks + honesty-16 + tail-1874-×10-P203-lead!) + skripte: p202_fetch.py + p202_read_page.mjs + p202_crop.py + p202_build_entries.py + p202_build_proof.py ———")
for hisna, sken, zap, wsi, wen in BLOCKS:
    lines.append("  {")
    lines.append(f'    houseNo: "{hisna}",')
    lines.append('    bookSignature: "04106",')
    lines.append("    year: 1875,")
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
print("year-1875-blokov:", out.count("year: 1875,"))
