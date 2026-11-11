#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P256 — patch p255_gen.py → p256_gen.py (5 blokov 1829)."""
src = open('scripts/tmp/p256_gen.py', encoding='utf-8').read()

def rep(old, new, label):
    global src
    assert old in src, f"MANJKA: {label}"
    src = src.replace(old, new, 1)
    print(f"OK: {label}")

# 1. docstring
rep('"""P255 — regenerator P254-modula parish-house-stories.ts + dokaza po 3 novih blokih 1828 (01738).\nKorpus 2023 → 2026; šest-knjižne 9 → 12 (h6/h22/h61!); bothEra-poročna 10 → 13; najdaljši razpon 66 → 96 (h6!).\nPo vzoru scripts/tmp/p254_gen.py + dokaz-emisija (research/issue17/parish-house-stories.json)."""',
    '"""P256 — regenerator P255-modula parish-house-stories.ts + dokaza po 5 novih blokih 1829 (01738).\nKorpus 2026 → 2031; šest-knjižne 12 → 16 (h5/h19/h32/h62!); bothEra-poročna 13 → 17; h20-span 1829–1919 = 90 (4.!).\nPo vzoru scripts/tmp/p255_gen.py + dokaz-emisija (research/issue17/parish-house-stories.json)."""',
    'docstring')

rep('assert len(entries) == 2026, f"expected 2026, got {len(entries)}"',
    'assert len(entries) == 2031, f"expected 2031, got {len(entries)}"', 'assert-2031')

rep('''    "01738": ("poročna-predhodnik", "marriage predecessor", "1828 + 1873",
              "h6/h22/h61 firstYear-1828! (h22 −41 = absolutni-rekord-dviga! · m13-polni-dvojni-61×22!)"),''',
    '''    "01738": ("poročna-predhodnik", "marriage predecessor", "1828 + 1829 + 1873",
              "P256: h62/h32/h5/h19 firstYear-1829! (h62 −35 = največji dvig P256! · m18-KRIŽAN-h62×h22 · h20-01738-span-1829+1873!)"),''',
    'bookmeta-01738')

# 4. SIX_STORIES: nove 4 + posodobitve h20/h22
anchor73 = '    "73": ("★ TIHA-HIŠA'
add = (
    '    "5": ("MÜLLER-hiša: m10-1829 ženin Mathe MÜLLER (26 l, GRIBLJE 5 × [Šimek?]-h19 — POLNI-DVOJNI, P256!) — h5-firstYear-1859→1829 (DVIG 30!); 31 blokov 1829–1924 — h5-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!); MÜLLER-×2-družini-1829 (h5-hiša + h22-Millerji!).",\n'
    '          "The MÜLLER house: the m10-1829 groom Mathe MÜLLER (26, GRIBLJE 5 × the h19-bride — the FULL DOUBLE, P256!) — the h5-firstYear-1859→1829 (LIFT 30!); 31 blocks 1829–1924 — h5-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!); the MÜLLER-×2-families-of-1829 (the h5-house + the h22-Millers!)."),\n'
    '    "19": ("[ŠIMEK?]-hiša: m10-1829 nevesta Maria [ŠIMEK?~Knimek/Thimnik — 4-branja-DUEL!] (21 l, GRIBLJE 19 × Müller-h5, P256!) — oče Georg [Šimek?~\'Shimek\'-garble — ŠIMEC-marker-kand.!] + mati [Salva?] TILLAR! (TILLAR-NIT-1829!); h19-firstYear-1858→1829 (DVIG 29!) — h19-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!).",\n'
    '          "The [ŠIMEK?] house: the m10-1829 bride Maria [ŠIMEK?~4-reads-DUEL!] (21, GRIBLJE 19 × the Müller-h5, P256!) — the father Georg [Šimek?~garble] + the mother [Salva?] TILLAR! (the-1829-TILLAR-thread!); the h19-firstYear-1858→1829 (LIFT 29!) — h19-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!)."),\n'
    '    "32": ("[DEHLIČ?]-hiša: m2-1829 ženin Michael [DEHLIČ?~3-branja-DUEL] (28 l, GRIBLJE 32 [~DUEL-32|33!] × [Malešič?]-h20 — POLNI-DVOJNI, P256!) — MALEŠIČ×MALEŠIČ (mati-ženina + oče-neveste — KRVNO-SOROSTVO-KAND.!); h32-firstYear-1863→1829 (DVIG 34!) — h32-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!).",\n'
    '          "The [DEHLIČ?] house: the m2-1829 groom Michael [DEHLIČ?~3-reads-DUEL] (28, GRIBLJE 32 [~DUEL-32|33!] × the h20-bride — the FULL DOUBLE, P256!) — the MALEŠIČ×MALEŠIČ-kinship-cand.!; the h32-firstYear-1863→1829 (LIFT 34!) — h32-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!)."),\n'
    '    "62": ("★★★★★ KRIŽAN-HRIŽAN-hiša-44-LET: m18-1829 ŽENIN Matthe KRIŽAN (GRIBLJE 62 × Miller-h22 — POLNI-DVOJNI, P256!) + m18-1873 NEVESTA Maria HRIŽAN (h62 × Gabovšič-h13 — ŠIV-P253!) = ISTA-HIŠA-1829–1873!; oče Nikl. KRIŽAN + mati [TILLAR-garble — Barbara?|Dorothea?-DUEL!]; h62-firstYear-1864→1829 (DVIG 35 = največji P256!) — h62-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!); 29 blokov 1829–1908.",\n'
    '          "★★★★★ THE-KRIŽAN-HRIŽAN-HOUSE-44-YEARS: the m18-1829 GROOM Matthe KRIŽAN (GRIBLJE 62 × the Miller-h22 — the FULL DOUBLE, P256!) + the m18-1873 BRIDE Maria HRIŽAN (h62 × the Gabovšič-h13 — the-P253-SEAM!) = THE-SAME-HOUSE-1829–1873!; the father Nikl. KRIŽAN + the mother [TILLAR-garble — Barbara?|Dorothea?-DUEL!]; the h62-firstYear-1864→1829 (LIFT 35 = the-largest-of-P256!) — h62-ENTERS-THE-SIX-BOOKS-CLUB (12→16, P256!); 29 blocks 1829–1908."),\n'
)
rep(anchor73, add + anchor73, 'SIX-dodaj-4')

rep('"BORŠT-h20: z72/z73 DVOJČKI 1871 Georg + Catharina = 1. DVOJČKI KRSTNE LINIJE (P235!); 1869 Marko PEZDIRE †24 + 1859 [~Klara/Elena-Podire-garble]; 1919 Peter PEZDIRC poroka — PEZDIRC-nit čez 3 generacije (1859→1919 = 60 let!).",',
    '"BORŠT-h20: ★★★ P256: m2-1829 [MALEŠIČ?]-nevesta (Griblje 20 × [Dehlič?]-h32 — POLNI-DVOJNI!) = h20-ŽE-DRUGI-01738-blok (1829+1873-m7-P253!) — h20-firstYear-1859→1829 (DVIG 30!) + span-1829–1919 = 90-let (4.-najdaljši-za-h6-96/h22-93/h61-91!); z72/z73 DVOJČKI 1871 = 1. DVOJČKI KRSTNE LINIJE (P235!); PEZDIRC-nit čez 3 generacije (1859→1919 = 60 let!).",',
    'h20-zgodba-si')
rep('"The BORŠT h20: the z72/z73 TWINS 1871 Georg + Catharina = THE FIRST TWINS OF THE BAPTISM LINE (P235!); Marko PEZDIRE †24 in 1869 + the 1859 [~Klara/Elena-Podire garble]; Peter PEZDIRC marries 1919 — the PEZDIRC thread across 3 generations (1859→1919 = 60 years!)."),',
    '"The BORŠT h20: ★★★ P256: the m2-1829 bride (Griblje 20 × the h32-groom — the FULL DOUBLE!) = h20-SECOND-01738-block (1829+1873!) — the h20-firstYear-1859→1829 (LIFT 30!) + span-1829–1919 = 90-years (the-4th-longest!); the z72/z73 TWINS 1871 (P235!); the PEZDIRC thread 1859→1919 (60 years!)."),',
    'h20-zgodba-en')

rep("cf.-P251-m20-MILEK-'Griblje-[22~26]-DUEL'-1873; 5-porok-04455 (1879–1919) + 33 blokov 1828–1921 = 93 let!\",",
    "cf.-P251-m20-MILEK-'Griblje-[22~26]-DUEL'-1873; ★★★★★ P256: m18-1829-nevesta-Maria-MILLER (h22 × KRIŽAN-h62 — POLNI-DVOJNI!) = 2-LETNI-ZAPORED-MILLERjevih-nevest-na-h22 (1828-Catra-[Miller-garble] + 1829-Maria-MILLER — oče-Josc.-Miller!); 5-porok-04455 (1879–1919) + 34 blokov 1828–1921 = 93 let!\",",
    'h22-zgodba-si')
rep('cf.-the-P251-m20-MILEK-\'Griblje-[22~26]-DUEL\'-1873; 5 marriages 04455 (1879–1919) + 33 blocks 1828–1921 = 93 years!"),',
    'cf.-the-P251-m20-MILEK-\'Griblje-[22~26]-DUEL\'-1873; ★★★★★ P256: the m18-1829 bride Maria MILLER (h22 × the KRIŽAN-h62 — the FULL DOUBLE!) = TWO-CONSECUTIVE-YEARS-OF-MILLER-BRIDES-ON-h22 (1828-Catra-[Miller-garble] + 1829-Maria-MILLER!); 5 marriages 04455 (1879–1919) + 34 blocks 1828–1921 = 93 years!"),',
    'h22-zgodba-en')

rep('assert tiers[6] == 12 and tiers[5] == 50 and tiers[4] == 14 and tiers[3] == 8 and tiers[2] == 8 and tiers[1] == 8, dict(tiers)',
    'assert tiers[6] == 16 and tiers[5] == 46 and tiers[4] == 14 and tiers[3] == 8 and tiers[2] == 8 and tiers[1] == 8, dict(tiers)',
    'tiers-16/46')

rep('A("// P254+P255: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (regenerirano P255: +3 bloki 1828/01738!; 2026-11-11)")',
    'A("// P254+P255+P256: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (regenerirano P256: +5 blokov 1829/01738!; 2026-11-11)")',
    'ts-glava-1')
rep('A("// SINTEZNA FAZA: agregacija celotnega korpusa HOUSE_VITALS (2026 vitalov) po hišah čez VSEH 6 knjig:")',
    'A("// SINTEZNA FAZA: agregacija celotnega korpusa HOUSE_VITALS (2031 vitalov) po hišah čez VSEH 6 knjig:")',
    'ts-glava-2')
rep('A("// 01738 (poročna-predhodnik 1828 + 1873 — P255: +3 bloki 1828!) + 04104 (krstna-predzgodovina 1871–1885)")',
    'A("// 01738 (poročna-predhodnik 1828 + 1829 + 1873 — P256: +5 blokov 1829!) + 04104 (krstna-predzgodovina 1871–1885)")',
    'ts-glava-3')
rep('A("// ★★★★★ P255-VELIKI-PRELOM: KORPUS-PRVI-VPIS-1857→1828 (h6/h22/h61!) — ★★★ 12 ŠEST-KNJIŽ-HIŠ (P254-9 → P255-12!:")',
    'A("// ★★★★★ P255-VELIKI-PRELOM: KORPUS-PRVI-VPIS-1857→1828 (h6/h22/h61!) — ★★★★★ P256: 16 ŠEST-KNJIŽ-HIŠ (P254-9 → P255-12 → P256-16!:")',
    'ts-glava-4')
rep('A("// 3, 6, 10, 12, 16, 18, 20, 22, 28, 61, 63, 73) + bothEra-poročna 10→13 + najdaljši-razpon-66→96 (h6!).")',
    'A("// 3, 5, 6, 10, 12, 16, 18, 19, 20, 22, 28, 32, 61, 62, 63, 73!) + bothEra-poročna 10→13→17 + razponi: h6-96/h22-93/h61-91/h20-90 (4.-mesto-P256!) + h62-1829 (KRIŽAN-ŽENIN-44-let-pred-HRIŽAN-ŠIV!)")',
    'ts-glava-5')
rep('A("// regenerator: scripts/tmp/p255_gen.py (po vzoru p254_gen.py).")',
    'A("// regenerator: scripts/tmp/p256_gen.py (po vzoru p255_gen.py).")',
    'ts-glava-6')

rep('A("/** ★★★ 12 ŠEST-KNJIŽ-HIŠ (P255!) — blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste). */")',
    'A("/** ★★★★★ 16 ŠEST-KNJIŽ-HIŠ (P256!) — blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste). */")',
    'six-komentar')
rep('A("/** Pokritje po številu knjig: 12/50/14/8/8/8 = 100 (P255: 9/53 → 12/50!). */")',
    'A("/** Pokritje po številu knjig: 16/46/14/8/8/8 = 100 (P256: 12/50 → 16/46!). */")',
    'tiers-komentar')

rep('A("  blocks: 2026,")', 'A("  blocks: 2031,")', 'blocks-2031')
rep('A("  bothEraPorocna: 13,")', 'A("  bothEraPorocna: 17,")', 'bothEra-17')
rep("A('  deathsGap: \"25\",')\nA(\"} as const;\")",
    "A('  deathsGap: \"25\",')\nA('  p256Dvigi: \"h62/h32/h5/h20/h19 = 35/34/30/30/29 (1829!)\",')\nA(\"} as const;\")",
    'totals-p256')

rep('"h6 dokumentirana 1828→1924 (96 let!) — m6-1828-v-predhodniku × 04894-1924-mrliška; sledita h22 (93: 1828–1921) in h61 (91: 1828–1919) — obe čez polni-dvojni-m13! Stari-rekord-66 (h2/h13/h50/h60/h64, 1857/58→1923/24) ostaja za štiri-knjižnimi.",',
    '"h6 dokumentirana 1828→1924 (96 let!) — m6-1828-v-predhodniku × 04894-1924-mrliška; sledita h22 (93: 1828–1921) in h61 (91: 1828–1919) — ★★★ P256: h20 zdaj 4. z 90 leti (1829–1919 — m2-1829-malešič + 1919-PEZDIRC!) + h62 pridobi 1829 (KRIŽAN-ženin — 44 let pred HRIŽAN-ŠIV-1873!); stari-rekord-66 (h2/h13/h50/h60/h64) ostaja za štiri-knjižnimi.",',
    'razponi-si')
rep('"The h6 documented 1828→1924 (96 years!) — the m6-1828-in-the-predecessor × the 04894-1924-death; then h22 (93: 1828–1921) and h61 (91: 1828–1919) — both via the m13 full-double! The old record 66 (h2/h13/h50/h60/h64) remains for the four-book houses."),',
    '"The h6 documented 1828→1924 (96 years!) — then h22 (93) and h61 (91) — ★★★ P256: h20 now 4th with 90 years (1829–1919!) + h62 gains 1829 (the KRIŽAN groom — 44 years before the HRIŽAN-SEAM-1873!); the old record 66 remains for the four-book houses."),',
    'razponi-en')

rep('"longestSpan": {"years": best_span, "houses": [best_house], "note": "P255: h6 = 1828 (m6-01738!) → 1924 — stari rekord 66 (h2/h13/h50/h60/h64) presežen!"},',
    '"longestSpan": {"years": best_span, "houses": [best_house], "note": "P255: h6-1828→1924; P256: h20-90 (4.) + h62-pridobi-1829!"},\n    "firstYearLiftsP256": {"h62": 35, "h32": 34, "h5": 30, "h20": 30, "h19": 29, "note": "P256: 5 dvigov (h62 −35 = največji P256; h22 −41 ostaja absolutni rekord P255!)"},',
    'records-lifts')
rep('f"P255: poročna obe-eri 10→13 (h6/h22/h61 poročita v OBEH poročnih knjigah — 1828-predhodnik + 04455!)"},',
    'f"P256: poročna obe-eri 13→17 (h5/h19/h32/h62 poročita v OBEH — 1829 + 04455!)"},',
    'bothEra-note')
rep('"phase": "P254+P255 (regenerirano P255)",', '"phase": "P254+P255+P256 (regenerirano P256)",', 'json-faza')
rep('"title": "Hišne zgodbe globje — mreže hiš čez 6 knjig (+P255: 3 bloki 1828/01738!)",',
    '"title": "Hišne zgodbe globje — mreže hiš čez 6 knjig (+P256: 5 blokov 1829/01738!)",', 'json-naslov')
rep('"lead": "P252-lead-② + P253-korpus + P255-notranjost-01738-1828 (korpus-1857→1828!)",',
    '"lead": "P252-lead-② + P253-korpus + P255-notranjost-1828 + P256-notranjost-1829 (korpus-1857→1828→1829!)",', 'json-lead')
rep('"source": {"corpus": "src/data/atlas/parish.ts HOUSE_VITALS", "vitalsTotal": 2026, "books": 6,',
    '"source": {"corpus": "src/data/atlas/parish.ts HOUSE_VITALS", "vitalsTotal": 2031, "books": 6,', 'json-vir')
rep('"method": "agregacija vseh 2026 vitalnih blokov po hišni oznaki — 1:1 z runtime (qa-p254 živa rekalkulacija!)"},',
    '"method": "agregacija vseh 2031 vitalnih blokov po hišni oznaki — 1:1 z runtime (qa-p254 živa rekalkulacija!)"},', 'json-metoda')
rep('"note": "blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste) — P255: 9→12 (h6/h22/h61 vstopajo prek m6/m13-1828!)",',
    '"note": "blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste) — P255: 9→12 + P256: 12→16 (h5/h19/h32/h62 vstopajo prek m2/m10/m18-1829!)",', 'json-six-note')
rep('"note": "P255: 52-od-53-pet-knjižnih-prej-manjkalo-SAMO-01738 — h6/h22/h61-izstopajo (odprt-v-1828!)"},',
    '"note": "P256: pet-knjižne 50→46 — h5/h19/h32/h62-izstopajo (odprto-v-1829!); preostalih-46-čaka-01738-1830/1831+"},', 'json-missing-note')
rep('"vitalsTotal": 2026,\n        "p255": "+3 bloki 1828 (h6-m6 + h61/h22-m13 polni-dvojni!) — šest-knjižne 9→12, bothEra-poročna 10→13, najdaljši-razpon 66→96 (h6)",',
    '"vitalsTotal": 2031,\n        "p255": "+3 bloki 1828 — šest-knjižne 9→12, razpon 66→96 (h6)",\n        "p256": "+5 blokov 1829 (h32/h20-m2 + h5/h19-m10 + h62-m18!) — šest-knjižne 12→16, bothEra-poročna 13→17, dvigi 35/34/30/30/29 (h62/h32/h5/h20/h19!), h20-span-90!",', 'json-ucinek')
rep('"verifier": "scripts/p254_house_stories.py --check + scripts/p255_notranjost_01738.py (I1–I10)",',
    '"verifier": "scripts/p254_house_stories.py --check + scripts/p256_1829.py (I1–I10 + --live!)",', 'json-verifier')

open('scripts/tmp/p256_gen.py', 'w', encoding='utf-8').write(src)
print("p256_gen.py POPRAVLJEN")
