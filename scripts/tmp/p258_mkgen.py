#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — priprava p258_gen.py iz p257_gen.py (transformacija). """
import re

SRC = "scripts/tmp/p257_gen.py"
OUT = "scripts/tmp/p258_gen.py"

src = open(SRC, encoding="utf-8").read()

# 1) glava docstring
src = src.replace(
    '"""P257 — regenerator modula parish-house-stories.ts + dokaza po 11 novih blokih 1830/1831 (01738).\nKorpus 2032 → 2043; šest-knjižne 16 → 23 (+7: h1/h11/h26/h27/h33/h56/h65 — NAJVEČJI-SKOK!);\nbothEra-poročna 17 → 26; 10 dvigov (h54-37 = 2. največji vseh časov!); h50-93 (3. razpon).\nPo vzoru scripts/tmp/p256_gen.py + dokaz-emisija (research/issue17/parish-house-stories.json)."""',
    '"""P258 — regenerator modula parish-house-stories.ts + dokaza po 16 novih blokih 1831-konec/1832/1833 (01738).\nKorpus 2043 → 2059; šest-knjižne 23 → 31 (+8: h2/h8/h35/h36/h42/h46/h47/h48 — 2.-največji-skok!);\nbothEra-poročna 26 → 34 (+8!); 10 dvigov (h8-40 = 2. največji vseh časov!); h2-93 (izenači 3.-mesto).\nPo vzoru scripts/tmp/p257_gen.py + dokaz-emisija (research/issue17/parish-house-stories.json)."""',
)

# 2) števci
src = src.replace('assert len(entries) == 2043, f"expected 2043, got {len(entries)}"',
                  'assert len(entries) == 2059, f"expected 2059, got {len(entries)}"')

# 3) book_meta 01738
src = src.replace(
    '''    "01738": ("poročna-predhodnik", "marriage predecessor", "1828 + 1829 + 1830 + 1831 + 1873",
              "P257: 10 dvigov 1831 (h54-37 = 2. vseh časov!) + h22-3.-zaporedno-leto-1830! · m2-PESDIRZ-h50 (PEZDIRC-NIT-42-let!)"),''',
    '''    "01738": ("poročna-predhodnik", "marriage predecessor", "1828–1833 + 1873",
              "P258: 16 blokov 1831-konec/1832/1833 (h8-40 = 2. dvig vseh časov! + PEZDIRC-h50-3-vrstice + šest-knjižni-klub-23→31!) · m6-1833-Johann-PESDIRZ-h50!"),''',
)

# 4) tiers assertion
src = src.replace(
    "assert tiers[6] == 23 and tiers[5] == 41 and tiers[4] == 12 and tiers[3] == 8 and tiers[2] == 8 and tiers[1] == 8, dict(tiers)",
    "assert tiers[6] == 31 and tiers[5] == 33 and tiers[4] == 12 and tiers[3] == 8 and tiers[2] == 8 and tiers[1] == 8, dict(tiers)",
)

# 5) SIX_STORIES: posodobitve h22/h56/h61 + 8 novih pred zaklepajem }
src = src.replace(
    '''    "65": ("★★★★★ P257-MILEK-hiša: m10-1831-ŽENIN-Nicol-MILEK ('-ek'-1:1!-oče-Janez!, GRIBLJE 65 × [Prodsanzig?]-Podzemelj-2) — h65-firstYear-1857→1831 (DVIG 26!) — ★-h65-BILA-PRVA-HIŠA-KORPUSA-1857 (korpus-prvi-vpis-PRE-P255!) + MILEK-h65-NIT: 1831↔1874-P250 = 43-LET-družine!; 44 blokov = 2.-najglasnejša (za-h24-45!) + 14 v 04106 = REKORD-skupaj-s-h13; zdaj-ŠEST-knjižna-prek-P257!",
           "★★★★★ The P257-MILEK house: the m10-1831 GROOM Nicol MILEK (father-Janez!, GRIBLJE 65 × the Podzemelj-2-bride) — the h65-firstYear-1857→1831 (LIFT 26!) — ★-h65-WAS-THE-FIRST-HOUSE-OF-THE-CORPUS-1857 + THE-MILEK-THREAD: 1831↔1874 = A-43-YEAR-family!; 44 blocks = the-2nd-loudest (after h24-45!) + 14 in 04106 = the record-with-h13; now-SIX-book-via-P257!"),
}''',
    '''    "65": ("★★★★★ P257-MILEK-hiša: m10-1831-ŽENIN-Nicol-MILEK ('-ek'-1:1!-oče-Janez!, GRIBLJE 65 × [Prodsanzig?]-Podzemelj-2) — h65-firstYear-1857→1831 (DVIG 26!) — ★-h65-BILA-PRVA-HIŠA-KORPUSA-1857 (korpus-prvi-vpis-PRE-P255!) + MILEK-h65-NIT: 1831↔1874-P250 = 43-LET-družine!; 44 blokov = 2.-najglasnejša (za-h24-45!) + 14 v 04106 = REKORD-skupaj-s-h13; zdaj-ŠEST-knjižna-prek-P257!",
           "★★★★★ The P257-MILEK house: the m10-1831 GROOM Nicol MILEK (father-Janez!, GRIBLJE 65 × the Podzemelj-2-bride) — the h65-firstYear-1857→1831 (LIFT 26!) — ★-h65-WAS-THE-FIRST-HOUSE-OF-THE-CORPUS-1857 + THE-MILEK-THREAD: 1831↔1874 = A-43-YEAR-family!; 44 blocks = the-2nd-loudest (after h24-45!) + 14 in 04106 = the record-with-h13; now-SIX-book-via-P257!"),
    # ——— P258 NOVIH 8 šest-knjižnih (23→31!) ———
    "2": ("★★★★★ P258-hiša-DVAKRAT-V-ZAPOREDNIH-LETIH: 1831-NEVESTA-Anna-[~Kleberz=KLEBEC-kand.!] (24, GRIBLJE 2 × Johann-KLOBUČAR-h48 — POLNI-DVOJNI-24.-Avg!) + 1832-ŽENIN-Johann-[HLEBEC!] (21, oče-Johann-kmet!, GRIBLJE 2 × Anna-[~Petriz]-h42-[~Gríblje|Smrečje-DUEL] — POLNI-DVOJNI-[~]-29.-Febr-PRESTOPNI!) = ★-ISTA-HIŠA-2-LETI-ZAPORED-2-DRUGI-VLOGI (nevesta→ženin!) — h2-firstYear-1858→1831 (DVIG 27!) + ★★★★★-HLEBEC-NIT: 1832-h2 ↔ 1873-m11-h3-P253 (41-let!-sosednji-hiši!); 26 blokov 1831–1924 = 93 let (IZENAČI-h20/h22/h50!); zdaj-ŠEST-knjižna (23→31!)",
           "★★★★★ The P258 house TWICE-IN-CONSECUTIVE-YEARS: the 1831 BRIDE Anna [~Kleberz?] (GRIBLJE 2 × the KLOBUČAR-h48 — the FULL DOUBLE!) + the 1832 GROOM Johann [HLEBEC!] (GRIBLJE 2 × the h42-bride — the leap-day-FULL-DOUBLE-[~]!) = ★-THE-SAME-HOUSE-2-YEARS-2-DIFFERENT-ROLES (bride→groom!) — the h2-firstYear-1858→1831 (LIFT 27!) + ★★★★★ THE-HLEBEC-THREAD: 1832-h2 ↔ 1873-m11-h3 (41-years!); 26 blocks 1831–1924 = 93 years (ties-h20/h22/h50!); now-SIX-book (23→31!)"),
    "8": ("★★★★★ P258-hiša-DVIG-40 = 2.-NAJVEČJI-VSEH-ČASOV: 1831-NEVESTA-Catharina-[~Klofčič] (18, GRIBLJE 8 × Matthias-KLOBUČAR-h46 — POLNI-DVOJNI-24.-Avg!-KLOBUČAR-BRATJE-m19×m20-ISTI-DAN!) — h8-firstYear-1871→1831 (DVIG 40!-za-h22-41-P255!-pred-h46/h66-36!) + 26 blokov 1831–1919 = 88 let; zdaj-ŠEST-knjižna (23→31!)",
           "★★★★★ The P258 house — THE-LIFT-40 = THE-2ND-LARGEST-EVER: the 1831 BRIDE Catharina [~Klofčič] (18, GRIBLJE 8 × the KLOBUČAR-h46 — the FULL DOUBLE of Aug 24!-the-KLOBUČAR-brothers-same-day!) — the h8-firstYear-1871→1831 (LIFT 40!-after-h22-41-P255!) + 26 blocks 1831–1919 = 88 years; now-SIX-book (23→31!)"),
    "35": ("★★★★★ P258-hiša-DVE-DRUŽINI-V-ENEM-LETU: 1832-m8-NEVESTA-Anna-[~Štremuz] (21, GRIBLJE 35 × Johann-MILEK-h22 — POLNI-DVOJNI-15.-Febr!) + 1832-m17-NEVESTA-Catharina-[~FLACH] (17, oče-Peter!, GRIBLJE 35 × Nicol-KRIŽAN-h36 — POLNI-DVOJNI-29.-Febr-PRESTOPNI!) = ★-DVA-PAROV-IZ-h35-V-14-DNEH-ISTEGA-LETA (cf.-h28-×2-1873!) — h35-firstYear-1867→1832 (DVIG 35!) + ★-FLACH-×2-NIT (h35+h61!) + 29 blokov 1832–1922 = 90 let + HRIŽAN-družina-04894:15-REKORD; zdaj-ŠEST-knjižna (23→31!)",
            "★★★★★ The P258 house — TWO-FAMILIES-IN-ONE-YEAR: the m8-1832 BRIDE Anna [~Štremuz] (GRIBLJE 35 × the MILEK-h22 — the FULL DOUBLE!) + the m17-1832 BRIDE Catharina [~FLACH] (GRIBLJE 35 × the KRIŽAN-h36 — the leap-day-FULL-DOUBLE!) = ★-TWO-COUPLES-FROM-h35-IN-14-DAYS (cf.-h28-×2-1873!) — the h35-firstYear-1867→1832 (LIFT 35!) + ★-THE-FLACH-×2-THREAD (h35+h61!) + 29 blocks 1832–1922 = 90 years + the HRIŽAN-04894:15-RECORD; now-SIX-book (23→31!)"),
    "36": ("★★★ P258-KRIŽAN-hiša: 1832-ŽENIN-Nicol-KRIŽAN (20, oče-Matthias!, GRIBLJE 36 × Catharina-[~Flach]-h35 — POLNI-DVOJNI-29.-Febr-prestopni!) — ★★★★★-KRIŽAN-KONGLOMERAT: 1831-h3 + 1832-h36 + 1832-h66 + 1873-h63 = 4-GRIBLJE-HIŠE + HRIŽAN-h62-ŠIV = 5-hiš-istega-korena! — h36-firstYear-1857→1832 (DVIG 25!); 26 blokov 1832–1917 = 85 let; zdaj-ŠEST-knjižna (23→31!)",
            "★★★ The P258-KRIŽAN house: the 1832 GROOM Nicol KRIŽAN (20, father-Matthias!, GRIBLJE 36 × the h35-bride — the leap-day-FULL-DOUBLE!) — ★★★★★ THE-KRIŽAN-CONGLOMERATE: 1831-h3 + 1832-h36 + 1832-h66 + 1873-h63 = 4-GRIBLJE-HOUSES + the h62-seam = 5-houses-of-one-root! — the h36-firstYear-1857→1832 (LIFT 25!); 26 blocks 1832–1917 = 85 years; now-SIX-book (23→31!)"),
    "42": ("★★★ P258-hiša-[~village-DUEL]: 1832-NEVESTA-Anna-[~Petriz] (17, oče-Matthias-kmet!, [~GRIBLJE-2:1|Smrečje?-DUEL-VAS-X-OPEN!] 42 × Johann-[HLEBEC]-h2 — POLNI-DVOJNI-[~]-29.-Febr-PRESTOPNI!) — h42-firstYear-1861→1832 (DVIG 29-[~vas-DUEL-ostaja!]); 24 blokov 1832–1912 = 80 let; zdaj-ŠEST-knjižna-[~DUEL] (23→31!)",
            "★★★ The P258 house-[~village-DUEL]: the 1832 BRIDE Anna [~Petriz] (17, [~GRIBLJE-2:1|Smrečje?-DUEL] 42 × the [HLEBEC]-h2 — the leap-day-FULL-DOUBLE-[~]!) — the h42-firstYear-1861→1832 (LIFT 29-[~duel-remains!]); 24 blocks 1832–1912 = 80 years; now-SIX-book-[~] (23→31!)"),
    "46": ("★★★ P258-KLOBUČAR-hiša: 1831-ŽENIN-Matthias-KLOBUČAR (27, oče-Mathias!, GRIBLJE 46 × Catharina-[~Klofčič]-h8 — POLNI-DVOJNI-24.-Avg!) — ★-KLOBUČAR-BRATJE-m19×m20 (h46×h8-+-h48×h2-DVA-POLNA-DVOJNA-ISTEGA-DNE!-[~bratje-kand.]) — h46-firstYear-1867→1831 (DVIG 36 = 3.-mesto-TROJNO-h46/h56/h66!); 26 blokov 1831–1920 = 89 let; zdaj-ŠEST-knjižna (23→31!)",
            "★★★ The P258-KLOBUČAR house: the 1831 GROOM Matthias KLOBUČAR (27, father-Mathias!, GRIBLJE 46 × the h8-bride — the FULL DOUBLE of Aug 24!) — ★-THE-KLOBUČAR-BROTHERS-m19×m20 (TWO-FULL-DOUBLES-OF-THE-SAME-DAY!) — the h46-firstYear-1867→1831 (LIFT 36 = the-3rd-place-TRIPLE!); 26 blocks 1831–1920 = 89 years; now-SIX-book (23→31!)"),
    "47": ("★★★★★ P258-PEZDIRC-PRIČA-hiša: 1831-NEVESTA-Maria-KLOBUČAR (20, GRIBLJE 47 × Andreas-[~Mercina|Hribar|Luminanic?-3-variant-GARBLE]-ŠKRILJE-1 — 9.-Febr-d°-12.-poroka-dneva!) — ★★★★★-PRIČA-AND.-PEZDIRC (duel-'Pezdirc'-jasno!-[~Simon-zavrnjen]) = 5.-VRSTICA-Pesdirc-družine-1831 (ženin+nevesta+ANOMALIJA+nevesta+PRIČA!-vse-vrste!) — h47-firstYear-1862→1831 (DVIG 31!); 25 blokov 1831–1919 = 88 let; zdaj-ŠEST-knjižna (23→31!)",
            "★★★★★ The P258 PEZDIRC-WITNESS house: the 1831 BRIDE Maria KLOBUČAR (20, GRIBLJE 47 × Andreas-[~3-variant-GARBLE]-of-ŠKRILJE-1 — the Feb-9-d°-12th-wedding!) — ★★★★★ THE-WITNESS-AND.-PEZDIRC = the-5th-ROW-of-the-1831-Pesdirc-family (all-kinds!) — the h47-firstYear-1862→1831 (LIFT 31!); 25 blocks 1831–1919 = 88 years; now-SIX-book (23→31!)"),
    "48": ("★★★ P258-KLOBUČAR-2-hiša: 1831-ŽENIN-Johann-KLOBUČAR (29, GRIBLJE 48 × Anna-[~Kleberz]-h2 — POLNI-DVOJNI-24.-Avg-d°-ISTI-DAN-kot-m19!) — [~očeN-Vincenz-PARON?-BARON-m21-veza-kand.!] — h48-firstYear-1857→1831 (DVIG 26!); 26 blokov 1831–1922 = 91 let (IZENAČI-h11/h33!); zdaj-ŠEST-knjižna (23→31!)",
            "★★★ The P258-KLOBUČAR-2 house: the 1831 GROOM Johann KLOBUČAR (29, GRIBLJE 48 × the h2-bride — the FULL-DOUBLE-same-day-as-m19!) — [~the-father-Vincenz-BARON?-candidate!] — the h48-firstYear-1857→1831 (LIFT 26!); 26 blocks 1831–1922 = 91 years (ties-h11/h33!); now-SIX-book (23→31!)"),
}''',
)

# 5b) posodobitve obstoječih zgodb h22/h56/h61 — append P258-note v storySi/En
src = src.replace(
    '''"22": ("REKORD-DVIGA-41-LET: m13-1828-nevesta-Catra-[~Miller-garble-'Križan'-kand.!]-GRIBLJE-22 × Miko-TILLAR-h61 = POLNI-DVOJNI (P255!) — h22-firstYear-1869→1828 = ABSOLUTNI-REKORD-DVIGA-MATRIČNE-LINIJE; P256: m18-1829-nevesta-Maria-MILLER (h22 × KRIŽAN-h62!); ★★★★★ P257: m4-1830-NEVESTA-Anna-MILEK (oče-Joh.-Milek!) = ★-3-ZAPOREDNA-LETA-NEVEST-IZ-h22 (1828+1829+1830 — edino-3-letno-zaporedje-v-01738!) — [~X-OPEN: Miller-ali-Milek-družina? + h65-Milek-1831-vezava-kand.!]; 35 blokov 1828–1921 = 93 let!",''',
    '''"22": ("REKORD-DVIGA-41-LET: m13-1828-nevesta-Catra-[~Miller-garble-'Križan'-kand.!]-GRIBLJE-22 × Miko-TILLAR-h61 = POLNI-DVOJNI (P255!) — h22-firstYear-1869→1828 = ABSOLUTNI-REKORD-DVIGA-MATRIČNE-LINIJE; P256: m18-1829-nevesta-Maria-MILLER (h22 × KRIŽAN-h62!); ★★★★★ P257: m4-1830-NEVESTA-Anna-MILEK (oče-Joh.-Milek!); ★★★★★★ P258: m8-1832-ŽENIN-Johann-MILEK (oče-Johann!-duel-'k'-ne-'ch'!) = ★★★-MILEK-DOMNEVA-POTRJENA (1830-Anna-+-1832-Johann = brat-sesta-ISTA-družina!) — h22-4-BLOKI-V-5-LETIH (1828+1829+1830+1832!-1831-edina-luknja!) — [~X-OPEN: Miller-garble-1828/1829-verjetno-ista!]; 36 blokov 1828–1921 = 93 let!",''',
)
src = src.replace(
    '"THE-41-YEAR-LIFT-RECORD: the m13-1828 bride Catra-GRIBLJE-22 × Miko-TILLAR-h61 = the FULL DOUBLE (P255!) — the h22-firstYear-1869→1828 = the ABSOLUTE-LIFT-RECORD; P256: the m18-1829 bride Maria MILLER (h22 × the KRIŽAN-h62!); ★★★★★ P257: the m4-1830 BRIDE Anna MILEK (father Joh. Milek!) = THREE-CONSECUTIVE-YEARS-OF-BRIDES-FROM-h22 (1828+1829+1830 — the only 3-year run in 01738!) — [~X-OPEN: Miller-or-Milek + the h65-1831-link-cand.!]; 35 blocks 1828–1921 = 93 years!"',
    '"THE-41-YEAR-LIFT-RECORD: the m13-1828 bride Catra (P255!) — the ABSOLUTE-LIFT-RECORD; P256: the m18-1829 bride Maria MILLER; ★★★★★ P257: the m4-1830 BRIDE Anna MILEK; ★★★★★★ P258: the m8-1832 GROOM Johann MILEK (father Johann!-the-letter-k!) = ★★★ THE-MILEK-HYPOTHESIS-CONFIRMED (brother-and-sister!) — h22-4-BLOCKS-IN-5-YEARS (1828+1829+1830+1832!-1831-the-only-gap!) — [~the-1828/1829-Miller-garble-likely-the-same!]; 36 blocks 1828–1921 = 93 years!"',
)
src = src.replace(
    '''"56": ("P257-hiša: m3-1831-ŽENIN-Math.-[Kiniz?~Schimiz/Štimic—3-branja] (32, GRIBLJE 56 × [Pedierz?]-Podzemelj-3 — pol-dvojni!) — h56-firstYear-1867→1831 (DVIG 36 — 3.-največji-vseh-časov!); 14 blokov 1831–1908 = 77 let; mati-[Klepz?]-KLEPEC-nit-kand. (continuum-1828/1829!)",''',
    '''"56": ("P257-hiša: m3-1831-ŽENIN-Math.-[Kiniz?~Schimiz/Štimic—3-branja] (32, GRIBLJE 56 × [Pedierz?]-Podzemelj-3) — ★★★★ P258: m23-1832-ŽENIN-Peter-[~SIMIG=ŠIMIČ?|Himiz?—3-variant-DUEL-vsi-'-imiz'!] (36, oče-Nicol-[~Šimič!]!, GRIBLJE 56 × Anna-[~Filach]-h61 — POLNI-DVOJNI-28.-Nov!) = 2.-družina-h56-01738 (1831+1832!) + [~ŠIMIČ-kand.-nit-h49-1833!] — h56-firstYear-1867→1831 (DVIG 36 — 3.-največji-trojno-h46/h56/h66!); 15 blokov 1831–1908 = 77 let; mati-[Klepz?]-KLEPEC-nit-kand. (continuum-1828/1829!)",''',
)
src = src.replace(
    '"The P257 house: the m3-1831 GROOM Math. [Kiniz?~DUEL] (32, GRIBLJE 56 × the Podzemelj-3-bride — a half-double!) — the h56-firstYear-1867→1831 (LIFT 36 — the-3rd-largest!); 14 blocks 1831–1908 = 77 years; the-[Klepz?]-KLEPEC-thread"',
    '"The P257 house: the m3-1831 GROOM Math. [Kiniz?~DUEL] — ★★★★ P258: the m23-1832 GROOM Peter [~ŠIMIČ?] (36, father Nicol!, GRIBLJE 56 × the [Filach]-h61 — the FULL DOUBLE!) = the-2nd-family-of-h56 + [~the-ŠIMIČ-h49-1833-thread!] — the h56-firstYear-1867→1831 (LIFT 36 — the-triple-3rd!); 15 blocks 1831–1908 = 77 years; the-[Klepz?]-KLEPEC-thread"',
)
src = src.replace(
    '''"61": ("TILLAR-hiša: m13-1828-ženin-Miko-TILLAR-½-Gütl-GRIBLJE-61 × nevesta-h22 = POLNI-DVOJNI (P255!) — TILLAR-NIT-×2 (m2-1828-mati-Anna-Tillar-Boršt-13!); h61-firstYear-1862→1828 (DVIG 34!); 3-poroke-04455 (1879-29 + …) + 04105-×4 + 04894-×6 = 17 blokov 1828–1919 = 91 let.",''',
    '''"61": ("TILLAR-hiša: m13-1828-ženin-Miko-TILLAR-½-Gütl-GRIBLJE-61 × nevesta-h22 = POLNI-DVOJNI (P255!) — TILLAR-NIT-×2 (m2-1828-mati-Anna-Tillar-Boršt-13!); ★★★★ P258: m23-1832-NEVESTA-Anna-[~FILACH=FLACH?] (22, oče-Nicol!, GRIBLJE 61 × Peter-[~Šimič]-h56 — POLNI-DVOJNI-28.-Nov!) = 3.-blok-01738 + ★-TILLAR→FILACH-ZAMENJAVA-DRUŽIN-h61 ([~X-OPEN: prodana-kmetija?]) + FLACH-×2-nit (h35!); h61-firstYear-1862→1828 (DVIG 34!); 18 blokov 1828–1919 = 91 let.",''',
)
src = src.replace(
    '"The TILLAR house: the m13-1828 groom Miko-TILLAR-½-Gütl-GRIBLJE-61 × the h22-bride = the FULL DOUBLE (P255!) — the TILLAR-thread-×2 (the m2-1828 mother Anna Tillar of Boršt 13!); the h61-firstYear-1862→1828 (LIFT 34!); 17 blocks 1828–1919 = 91 years."',
    '"The TILLAR house: the m13-1828 groom Miko-TILLAR × the h22-bride = the FULL DOUBLE (P255!) — the TILLAR-thread-×2; ★★★★ P258: the m23-1832 BRIDE Anna [~FILACH] (father Nicol!, GRIBLJE 61 × the [Šimič]-h56 — the FULL DOUBLE!) = the-3rd-01738-block + ★-THE-TILLAR→FILACH-FAMILY-CHANGE ([~X-OPEN]) + the-FLACH-×2-thread (h35!); the h61-firstYear-1862→1828 (LIFT 34!); 18 blocks 1828–1919 = 91 years."',
)

# 6) glave komentarjev TS
src = src.replace('A("// P254+P255+P256+P257: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (regenerirano P257: +11 blokov 1830/1831!; 2026-11-11)")',
                  'A("// P254+P255+P256+P257+P258: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (regenerirano P258: +16 blokov 1831-konec/1832/1833!; 2026-11-11)")')
src = src.replace('A("// SINTEZNA FAZA: agregacija celotnega korpusa HOUSE_VITALS (2043 vitalov) po hišah čez VSEH 6 knjig:")',
                  'A("// SINTEZNA FAZA: agregacija celotnega korpusa HOUSE_VITALS (2059 vitalov) po hišah čez VSEH 6 knjig:")')
src = src.replace('A("// 01738 (poročna-predhodnik 1828 + 1829 + 1830 + 1831 + 1873 — P257: +11 blokov!) + 04104 (krstna-predzgodovina 1871–1885)")',
                  'A("// 01738 (poročna-predhodnik 1828–1833 + 1873 — P258: +16 blokov!) + 04104 (krstna-predzgodovina 1871–1885)")')
src = src.replace('A("// ★★★★★ P257: 23 ŠEST-KNJIŽ-HIŠ (P254-9 → P255-12 → P256-16 → P257-23 — NAJVEČJI-SKOK!):")',
                  'A("// ★★★★★ P258: 31 ŠEST-KNJIŽ-HIŠ (P254-9 → P255-12 → P256-16 → P257-23 → P258-31 — 2.-NAJVEČJI-SKOK!):")')
src = src.replace('A("// 3, 5, 6, 10, 11, 12, 16, 18, 19, 20, 22, 26, 27, 28, 32, 33, 56, 61, 62, 63, 65, 73, 1!")',
                  'A("// 1, 2, 3, 5, 6, 8, 10, 11, 12, 16, 18, 19, 20, 22, 26, 27, 28, 32, 33, 35, 36, 42, 46, 47, 48, 56, 61, 62, 63, 65, 73 — +8: h2/h8/h35/h36/h42/h46/h47/h48 (P258!)")')
src = src.replace('A("// ★★★★★ P257-10-DVIGOV: h54-37 (2.-vseh-časov!) + h56-36 + h27-33 + h11-32 + h1-30 + h26-28[~] + h33-28[~] + h3-27 + h50-27 (PEZDIRC-NIT-42-let!) + h65-26 (bila-prva-hiša-1857!) + h22-3.-zaporedno-leto-1830!")',
                  'A("// ★★★★★ P258-10-DVIGOV: h8-40 (2.-vseh-časov-za-h22-41!) + h46-36 + h66-36 (3.-mesto-TROJNO-s-h56!) + h35-35 + h47-31 + h42-29[~] + h2-27 + h48-26 + h36-25 + h49-25 + h22-4.-blok-v-5-letih (1828/29/30/32!)")')
src = src.replace('A("// Razponi: h6-96/h62-95/h50+h20+h22-93/h11+h33-91/h26-90 — bothEra-poročna 17→26. Dokaz: research/issue17/parish-house-stories.json; verifikator: scripts/p254_house_stories.py --check; regenerator: scripts/tmp/p257_gen.py.")',
                  'A("// Razponi: h6-96/h62-95/h2+h50+h20+h22-93/h11+h33+h48+h61-91/h26+h35-90 — bothEra-poročna 26→34 (+8!). Dokaz: research/issue17/parish-house-stories.json; verifikator: scripts/p254_house_stories.py --check; regenerator: scripts/tmp/p258_gen.py.")')

# 7) komentarji strukture SIX/TIERS/TOTALS
src = src.replace('A("/** ★★★★★ 23 ŠEST-KNJIŽ-HIŠ (P257!) — blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste). */")',
                  'A("/** ★★★★★ 31 ŠEST-KNJIŽ-HIŠ (P258!) — blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste). */")')
src = src.replace('A("/** Pokritje po številu knjig: 23/41/12/8/8/8 = 100 (P257: 16/46 → 23/41!). */")',
                  'A("/** Pokritje po številu knjig: 31/33/12/8/8/8 = 100 (P258: 23/41 → 31/33 — 2.-največji-skok!). */")')

# 8) TOTALS
src = src.replace('A("  blocks: 2043,")', 'A("  blocks: 2059,")')
src = src.replace('A("  bothEraPorocna: 26,")', 'A("  bothEraPorocna: 34,")')
src = src.replace('A(\'  p257Dvigi: "h54/h56/h27/h11/h1/h26/h33/h3/h50/h65 = 37/36/33/32/30/28/28/27/27/26 (1831!) + h22-3-leto-1830!",\')',
                  'A(\'  p257Dvigi: "h54/h56/h27/h11/h1/h26/h33/h3/h50/h65 = 37/36/33/32/30/28/28/27/27/26 (1831!) + h22-3-leto-1830!",\')\nA(\'  p258Dvigi: "h8/h46/h66/h35/h47/h42/h2/h48/h36/h49 = 40/36/36/35/31/29/27/26/25/25 (1831/32/33!) + h22-4-bloki-v-5-letih + h35-×2-družini!",\')')

# 9) notables: h35 posodobitev + razponi + vrzeli
src = src.replace(
    '''    ("h35", "h35 = rekord mrliške linije 04894",
     "The h35 = the death-line 04894 record",
     "15 blokov v 04894 (1886–1924) = NAJVEČ V ENI KNJIGI med vsemi hišami; HRIŽAN-družina (P229!). Skupaj 24 blokov 1857–1922.",
     "15 blocks in 04894 (1886–1924) = THE MOST IN ONE BOOK of all houses; the HRIŽAN family (P229!). Altogether 24 blocks 1857–1922."),''',
    '''    ("h35", "h35 = rekord mrliške linije 04894 + DVE DRUŽINI 1832 (P258!)",
     "The h35 = the death-line 04894 record + TWO FAMILIES of 1832 (P258!)",
     "15 blokov v 04894 (1886–1924) = NAJVEČ V ENI KNJIGI med vsemi hišami; HRIŽAN-družina (P229!). ★★★★★ P258: h35-firstYear-1867→1832 (DVIG 35!) + ★-DVA-PAROV-IZ-h35-V-14-DNEH-1832 (m8-Štremuz-15.-Febr + m17-Flach-29.-Febr — cf.-h28-×2-1873!) + FLACH-×2-nit (h61!) + zdaj ŠEST-knjižna (23→31!); skupaj 29 blokov 1832–1922.",
     "15 blocks in 04894 (1886–1924) = THE MOST IN ONE BOOK of all houses; the HRIŽAN family (P229!). ★★★★★ P258: the-h35-firstYear-1867→1832 (LIFT 35!) + ★-TWO-COUPLES-FROM-h35-IN-14-DAYS (cf.-h28-×2-1873!) + the-FLACH-×2-thread + now-SIX-book; 29 blocks 1832–1922."),''',
)
src = src.replace(
    '''    ("smrtna-vrzeli", "h25 = SMRTNA VRZEL 29 let",
     "The h25 = A 29-YEAR DEATH GAP",
     "5 knjig a BREZ 04106: noben mrliški zapis 1857–1885 (29 let!) kljub krstnim blokom 1876 + 1883 ×2 in poroki v 01738 (m3-kandidat, P253!). Šele 04894 prinese 7 blokov (1888–1923) — mrežna luknja, ne stvarna.",
     "5 books but WITHOUT 04106: no death record 1857–1885 (29 years!) despite the baptism blocks 1876 + 1883 ×2 and a marriage in 01738 (the m3 candidate, P253!). Only 04894 brings 7 blocks (1888–1923) — a network hole, not a real one."),''',
    '''    ("smrtna-vrzeli", "h25 = SMRTNA VRZEL 29 let + P258: h66/h49 = POROČNI VRZELI (BREZ 04455!)",
     "The h25 = A 29-YEAR DEATH GAP + P258: h66/h49 = MARRIAGE GAPS (WITHOUT 04455!)",
     "5 knjig a BREZ 04106: noben mrliški zapis 1857–1885 (29 let!) kljub krstnim blokom 1876 + 1883 ×2 in poroki v 01738 (m3-kandidat, P253!). Šele 04894 prinese 7 blokov (1888–1923) — mrežna luknja, ne stvarna. ★★★ P258: h66 (KRIŽAN-h66-1832!) in h49 (Maria-[Himiz]-1833!) = 5 knjig BREZ 04455 — poročni vrzeli! (h49 tudi BREZ 04104 ne — 04104+04105+04106+04894+01738!)",
     "5 books but WITHOUT 04106: no death record 1857–1885 (29 years!) despite the baptisms 1876 + 1883 ×2. ★★★ P258: h66 (the-KRIŽAN-house-1832!) and h49 (the-1833-bride!) = 5 books WITHOUT 04455 — marriage gaps!"),''',
)
src = src.replace(
    '''h6 dokumentirana 1828→1924 (96 let!); sledita h62 (95: 1829–1924) in ★★★ P257: h50/h20/h22 (93: h50-1831–1924-NOVO-3.-mesto-izenači-h20/h22!) + h11/h33 (91: 1831–1922!) + h26 (90: 1831–1921!) + h27 (87); stari-rekord-66 (h2/h13/h50/h60/h64) ostaja za štiri-knjižnimi.''',
    '''h6 dokumentirana 1828→1924 (96 let!); sledita h62 (95: 1829–1924) in ★★★ P257/P258: h50/h20/h22/h2 (93: ★-h2-1831–1924-NOVO-P258-izenači-trojno!) + h11/h33/h48/h61 (91: ★-h48+h61-P258!) + h26/h35 (90: ★-h35-1832–1922-P258!) + h27 (87) + h46 (89-P258!); stari-rekord-66 (h2/h13/h50/h60/h64) ostaja za štiri-knjižnimi.''',
)

# 10) dokaz JSON polja
src = src.replace('"phase": "P254+P255+P256+P257 (regenerirano P257)",', '"phase": "P254+P255+P256+P257+P258 (regenerirano P258)",')
src = src.replace('"title": "Hišne zgodbe globje — mreže hiš čez 6 knjig (+P257: 11 blokov 1830/1831!)",', '"title": "Hišne zgodbe globje — mreže hiš čez 6 knjig (+P258: 16 blokov 1831-konec/1832/1833!)",')
src = src.replace('"lead": "P252-lead-② + P253-korpus + P255-1828 + P256-1829 + P257-1830/1831 (korpus-1857→1828→1829→1830/31!)",', '"lead": "P252-lead-② + P253 + P255–P257 + P258-meja-1831/32/33 (korpus-leta-1828–1833+1873!)",')
src = src.replace('"source": {"corpus": "src/data/atlas/parish.ts HOUSE_VITALS", "vitalsTotal": 2043,', '"source": {"corpus": "src/data/atlas/parish.ts HOUSE_VITALS", "vitalsTotal": 2059,')
src = src.replace('"method": "agregacija vseh 2043 vitalnih blokov po hišni oznaki — 1:1 z runtime (qa-p254 živa rekalkulacija!)"', '"method": "agregacija vseh 2059 vitalnih blokov po hišni oznaki — 1:1 z runtime (qa-p254 živa rekalkulacija!)"')
src = src.replace('''    "firstYearLiftsP257": {"h54": 37, "h56": 36, "h27": 33, "h11": 32, "h1": 30, "h26": 28, "h33": 28, "h3": 27, "h50": 27, "h65": 26,
                           "note": "P257: 10 dvigov (h54 −37 = 2. največji vseh časov za h22-41-P255!); h22-BREZ-dviga-ampak-3.-ZAPOREDNO-LETO-1830!; h65-bila-prva-hiša-korpusa-1857!"},''',
    '''    "firstYearLiftsP258": {"h8": 40, "h46": 36, "h66": 36, "h35": 35, "h47": 31, "h42": 29, "h2": 27, "h48": 26, "h36": 25, "h49": 25,
                           "note": "P258: 10 dvigov (h8 −40 = 2. največji vseh časov za h22-41-P255!); h46/h56/h66 = 3.-mesto-TROJNO!; h22-BREZ-dviga-ampak-4.-BLOK-V-5-LETIH (1828/29/30/32!); h35-×2-DVE-DRUŽINI-1832!; h42-[~village-DUEL]"},
    "firstYearLiftsP257": {"h54": 37, "h56": 36, "h27": 33, "h11": 32, "h1": 30, "h26": 28, "h33": 28, "h3": 27, "h50": 27, "h65": 26,
                           "note": "P257: 10 dvigov (h54 −37 = 2. največji vseh časov za h22-41-P255!); h22-BREZ-dviga-ampak-3.-ZAPOREDNO-LETO-1830!; h65-bila-prva-hiša-korpusa-1857!"},''')
src = src.replace('''    "bothEraCoverage": {"krstna": bk, "mrlishka": bm_, "porocna": bp,
                        "note": f"P257: poročna obe-eri 17→26 (+9 — vse-10-hiš-1831-imajo-04455-poročne!)"},''',
    '''    "bothEraCoverage": {"krstna": bk, "mrlishka": bm_, "porocna": bp,
                        "note": f"P258: poročna obe-eri 26→34 (+8 — h47/h46/h8/h48/h2/h35/h36/h42-dodane!-h66/h49-BREZ-04455-poročne-vrzeli!)"},
    "p258vrzeli": "h66 + h49 = 5 knjig BREZ 04455 (poročni vrzeli!); h50 = 5 knjig BREZ 04104!",
    "m2anomalija1832": "P258: m2-1832-'ženin'-MARIA-VIPAVC — ŽENSKO-IME-V-ŽENINSKEM-STOLPCU (duel-črko-za-črko-'M-a-r-i-a'!-2.-za-P257-m7!) + m3-[~Marino-MOŠKI-DUEL]",''')

open(OUT, "w", encoding="utf-8").write(src)
print("napisan", OUT, len(src), "znakov")
