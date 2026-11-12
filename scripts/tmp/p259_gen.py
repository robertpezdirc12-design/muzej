#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — regenerator modula parish-house-stories.ts + dokaza po novih blokih 1833-nadaljevanje/1834 (01738, s11–s13).
Korpus 2059 → EXPECTED_TOTAL (izpolni po integraciji!); šest-knjižne 31 → EXPECTED_SIX (kandidati: h24/h28/h53/h60…!);
bothEra-poročna 34 → EXPECTED_BOTHP; dvigi h24-26/h28-32/h51-33?/h53-30?/h58-25?/h60-24?/h68-27? (P259!).
Po vzoru scripts/tmp/p258_gen.py + dokaz-emisija (research/issue17/parish-house-stories.json).
★★★ P259-PREDLOGA: pred zagonom izpolni CONFIG-spodaj (števke iz blocks-p259.json) + SIX_STORIES-candidate! ★★★"""
import json
import re
import sys
from collections import defaultdict

# ——— P259-CONFIG (izpolni po integraciji — vrednosti iz blocks-p259.json / reconcile!) ———
EXPECTED_TOTAL = 2065   # 2059 + 6-P259
EXPECTED_TIERS = {6: 34, 5: 34, 4: 8, 3: 8, 2: 8, 1: 8}  # P259: 5 hiš 5→6-knjig
EXPECTED_SIX = 34      # 31 + 5 (h24/h53/h60/h68/h51)
EXPECTED_BOTH_P = 39   # 34 + 5

SRC = "src/data/atlas/parish.ts"
OUT_TS = "src/data/atlas/parish-house-stories.ts"
OUT_JSON = "research/issue17/parish-house-stories.json"

src = open(SRC, encoding="utf-8").read()
m = re.search(r'export const HOUSE_VITALS: HouseVital\[\] = \[(.*?)\n\];', src, re.S)
body = m.group(1)
pat = re.compile(r'houseNo:\s*"([^"]+)",\s*bookSignature:\s*"([^"]+)",\s*year:\s*(\d+)')
entries = pat.findall(body)
if EXPECTED_TOTAL == 0:
    print(f"P259-CONFIG: izpolni EXPECTED_TOTAL = {len(entries)} (dejansko št. vitalov) in ponovno zaženi!")
    sys.exit(2)
assert len(entries) == EXPECTED_TOTAL, f"expected {EXPECTED_TOTAL}, got {len(entries)}"

houses = defaultdict(lambda: defaultdict(list))
for h, b, y in entries:
    houses[h][b].append(int(y))

BOOKS = ["01738", "04104", "04105", "04455", "04106", "04894"]
book_meta = {
    "01738": ("poročna-predhodnik", "marriage predecessor", "1828–1834 + 1873",
              "P259: bloki 1833-nadaljevanje/1834 (s11–s13 — 13-porok-6.-Febr-1833-NOVI-REKORD + robno-številčenje-čez-mejo-leta + 5.-restart-1834!) · P258: 16 blokov 1831/32/33 (h8-40 = 2. dvig!) · P253: šiv-1873!"),
    "04104": ("krstna-predzgodovina", "baptism prehistory", "1871–1885", "h6 · h40 · h[?] (8 blokov vsak)"),
    "04105": ("krstna-linija", "baptism line", "1887–1919", "h24 (18 blokov!)"),
    "04455": ("poročna-linija + predzgodovina", "marriage line + prehistory", "1873–1922", "h27 SEGINA (8 blokov)"),
    "04106": ("mrliška-predzgodovina", "death prehistory", "1857–1885", "h13 · h65 (14 blokov vsak)"),
    "04894": ("mrliška-linija", "death line", "1886–1924", "h35 HRIŽAN (15 blokov!)"),
}


def kind_of(h):
    if h.isdigit():
        return "griblje" if 1 <= int(h) <= 78 else "druga-vas"
    return "neznano"


griblje = sorted([h for h in houses if kind_of(h) == "griblje"], key=int)
drugavas = sorted([h for h in houses if kind_of(h) == "druga-vas"], key=int)
neznano = ["13 [~]", "17 [~]", "32 [~]", "29 [~X-OPEN]", "[?]", "sub dioe."]
order = griblje + drugavas + neznano
assert set(order) == set(houses.keys()), sorted(set(order) ^ set(houses.keys()))

def entry(h):
    d = houses[h]
    tot = sum(len(v) for v in d.values())
    yrs = sorted(y for v in d.values() for y in v)
    per = ", ".join(f'{{ sig: "{b}", n: {len(d[b])} }}' for b in BOOKS if b in d)
    return (f'  {{ houseNo: "{h}", kind: "{kind_of(h)}", blocks: {tot}, books: {len(d)}, '
            f'perBook: [{per}], firstYear: {yrs[0]}, lastYear: {yrs[-1]}, span: {yrs[-1]-yrs[0]} }},')

six = sorted([h for h, d in houses.items() if len(d) == 6], key=lambda x: int(x) if x.isdigit() else 999)
if EXPECTED_SIX == 0:
    print(f"P259-CONFIG: izpolni EXPECTED_SIX = {len(six)} + SIX_STORIES-draft za: {six} in ponovno zaženi!")
    sys.exit(2)
assert len(six) == EXPECTED_SIX
tiers = defaultdict(int)
for h, d in houses.items():
    tiers[len(d)] += 1
tiers_sum = sum(tiers[k] for k in range(1, 7))
assert tiers_sum == len(houses) == 100
if not EXPECTED_TIERS:
    print(f"P259-CONFIG: izpolni EXPECTED_TIERS = {6: 34, 5: 34, 4: 8, 3: 8, 2: 8, 1: 8} (dejansko tierje) in ponovno zaženi!")
    sys.exit(2)
assert all(tiers[k] == v for k, v in EXPECTED_TIERS.items()), f"expected {EXPECTED_TIERS}, got {dict(tiers)}"

bk = sum(1 for h, d in houses.items() if "04104" in d and "04105" in d)
bm_ = sum(1 for h, d in houses.items() if "04106" in d and "04894" in d)
bp = sum(1 for h, d in houses.items() if "01738" in d and "04455" in d)
if EXPECTED_BOTH_P == 0:
    print(f"P259-CONFIG: izpolni EXPECTED_BOTH_P = {bp} (bothEra-poročna) in ponovno zaženi!")
    sys.exit(2)
assert bp == EXPECTED_BOTH_P, f"bothEra-poročna: expected {EXPECTED_BOTH_P}, got {bp}"
spans = sorted(((max(max(v) for v in d.values()) - min(min(v) for v in d.values()), h)
                for h, d in houses.items()), reverse=True)
best_span, best_house = spans[0]
assert (best_span, best_house) == (96, "6"), spans[:6]
assert spans[1][0] == 95 and spans[1][1] == "62", spans[:6]

SIX_STORIES = {
    "3": ("HRIŽAN/KRIŽAN-hiša: ★★★★★ P257: m1-1831-ŽENIN-Peter-KRIŽAN (GRIBLJE 3 × [Dehligl?]-h33 — POLNI-DVOJNI!) + ★-mati-neveste-Dorothea-KRIŽAN = KRIŽAN-×2-V-ENI-VRSTICI! — h3-firstYear-1858→1831 (DVIG 27!) + 24 blokov 1831–1917 = 86 let; Peter-Hrižan krstni oče 1872–1881 (4 krsti) + †1888 Peter Križar/Križan 80 let; 1864 Georg DRAGOŠ †70 (najstarejša omemba); m11-HLEBEC-1873 (P253!); 1907 PEZDIREC-poroka.",
          "The HRIŽAN/KRIŽAN house: ★★★★★ P257: the m1-1831 GROOM Peter KRIŽAN (GRIBLJE 3 — the FULL DOUBLE!) + the bride's mother Dorothea KRIŽAN = KRIŽAN-TWICE-IN-ONE-ROW! — the h3-firstYear-1858→1831 (LIFT 27!) + 24 blocks 1831–1917 = 86 years; Peter Hrižan the baptismal father 1872–1881 + Peter Križan †1888 aged 80; Georg DRAGOŠ †70 in 1864 (the oldest mention); the m11-HLEBEC-1873 (P253!); a PEZDIREC marriage 1907."),
    "6": ("NAJDALJŠA-HIŠA-KORPUSA (96 let!): m6-1828-nevesta-Maria-[Jan/Spin]-GRIBLJE-6 × ženin-Jure-STARA = PRVI-GRIBLJE-VPIS-PREDHODNIKA-01738 (P255 — korpus 1857→1828!); h6-firstYear-1860→1828 (DVIG 32!); 04104-trospec (8) + 04106 (6) + 04455 (5 porok!) + 04105 (8) + 04894 (8) = 36 blokov 1828–1924 čez VSEH 6 knjig!",
          "THE-LONGEST-SPAN-HOUSE-OF-THE-CORPUS (96 years!): the m6-1828 bride Maria-GRIBLJE-6 × groom Jure-STARA = the FIRST Griblje entry of the 01738 predecessor (P255 — the corpus 1857→1828!); the h6-firstYear-1860→1828 (LIFT 32!); 36 blocks 1828–1924 across ALL 6 books!"),
    "10": ("MUC-hiša: m6-1873 poroka neveste Muc — KOLBEZEN h16 × MUC h10 polni dvojni (P253!); KRAUE-h10 52-letna nevesta 1874 = NAJSTAREJŠA PREDZGODOVINE (P250!); 11 mrliških blokov 04106 (1857–1885) — med najglobljimi smrtnimi zgodovinami.",
           "The MUC house: the m6-1873 marriage of a Muc bride — KOLBEZEN h16 × MUC h10 the full double (P253!); the 52-year-old bride of 1874 = THE OLDEST OF THE PREHISTORY (P250!); 11 death blocks 04106 (1857–1885) — among the deepest death histories."),
    "12": ("DRAGOŠ-50-LET: 1869 Michael Dragos †27 → 1871 Joannes Dragoš krstni oče (z46!) → 1919 Franc DRAGOS poroka + Vincencij DRAGOS † — ISTA DRUŽINA 1869–1919! + PEZDIRC-continuum (z59-1872, P235!); 14 blokov v 04105 = 2.-največ v knjigi.",
           "The DRAGOŠ 50 YEARS: 1869 Michael Dragos †27 → 1871 Joannes Dragoš the baptismal father (z46!) → 1919 Franc DRAGOS marries + Vincencij DRAGOS † — THE SAME FAMILY 1869–1919! + the PEZDIRC continuum (z59-1872, P235!); 14 blocks in 04105 = the 2nd most of the book."),
    "16": ("KOLBEZEN-hiša: m6-1873 ženin Georg KOLBEZEN (h16 × h10 polni dvojni, P253!); 1918 Ana FILAK roj. NEMANIČ †75 (poročena 1879!); 1924 Alojzy NOVAK †27. 9. — zadnja leta mrliške linije (04894 se konča 31. 12. 1924, P190!).",
           "The KOLBEZEN house: the m6-1873 groom Georg KOLBEZEN (h16 × h10 the full double, P253!); Ana FILAK née NEMANIČ †75 in 1918 (married 1879!); Alojzy NOVAK †Sep 27 1924 — the final years of the death line (04894 ends Dec 31 1924, P190!)."),
    "18": ("ŠIMEC-hiša (P246-h18-ŠIMEC-1:1!): 1863 Georg Simic †53; 1878 dve INTRA-poroki v 1 letu (h18 × h65, P246!); 1921 Karolina PEZDIRC †1,3 (zadnji PEZDIRC-blok hiše); 36 blokov = najglasnejša šest-knjižna hiša (skupaj z h6!).",
           "The ŠIMEC house (P246-h18-ŠIMEC-1:1!): Georg Simic †53 in 1863; two INTRA-marriages in one year 1878 (h18 × h65, P246!); Karolina PEZDIRC †1.3 in 1921 (the house's last PEZDIRC block); 36 blocks = the loudest six-book house (together with h6!)."),
    "20": ("BORŠT-h20: ★★★ P256: m2-1829 [MALEŠIČ?]-nevesta (Griblje 20 × [Dehlič?]-h32 — POLNI-DVOJNI!) = h20-ŽE-DRUGI-01738-blok (1829+1873-m7-P253!) — h20-firstYear-1859→1829 (DVIG 30!) + span-1829–1922 = 93-let (IZENAČI-h22 — delita-2.-3.-mesto!); z72/z73 DVOJČKI 1871 = 1. DVOJČKI KRSTNE LINIJE (P235!); PEZDIRC-nit čez 3 generacije (1859→1919 = 60 let!).",
           "The BORŠT h20: ★★★ P256: the m2-1829 bride (Griblje 20 × the h32-groom — the FULL DOUBLE!) = h20-SECOND-01738-block (1829+1873!) — the h20-firstYear-1859→1829 (LIFT 30!) + span-1829–1922 = 93-years (ties-h22!); the z72/z73 TWINS 1871 (P235!); the PEZDIRC thread 1859→1919 (60 years!)."),
    "22": ("REKORD-DVIGA-41-LET: m13-1828-nevesta-Catra-[~Miller-garble-'Križan'-kand.!]-GRIBLJE-22 × Miko-TILLAR-h61 = POLNI-DVOJNI (P255!) — h22-firstYear-1869→1828 = ABSOLUTNI-REKORD-DVIGA-MATRIČNE-LINIJE; P256: m18-1829-nevesta-Maria-MILLER (h22 × KRIŽAN-h62!); ★★★★★ P257: m4-1830-NEVESTA-Anna-MILEK (oče-Joh.-Milek!); ★★★★★★ P258: m8-1832-ŽENIN-Johann-MILEK (oče-Johann!-duel-'k'-ne-'ch'!) = ★★★-MILEK-DOMNEVA-POTRJENA (1830-Anna-+-1832-Johann = brat-sesta-ISTA-družina!) — h22-4-BLOKI-V-5-LETIH (1828+1829+1830+1832!-1831-edina-luknja!) — [~X-OPEN: Miller-garble-1828/1829-verjetno-ista!]; 36 blokov 1828–1921 = 93 let!",
           "THE-41-YEAR-LIFT-RECORD: the m13-1828 bride Catra (P255!) — the ABSOLUTE-LIFT-RECORD; P256: the m18-1829 bride Maria MILLER; ★★★★★ P257: the m4-1830 BRIDE Anna MILEK; ★★★★★★ P258: the m8-1832 GROOM Johann MILEK (father Johann!-the-letter-k!) = ★★★ THE-MILEK-HYPOTHESIS-CONFIRMED (brother-and-sister!) — h22-4-BLOCKS-IN-5-YEARS (1828+1829+1830+1832!-1831-the-only-gap!) — [~the-1828/1829-Miller-garble-likely-the-same!]; 36 blocks 1828–1921 = 93 years!"),
    "28": ("DVE-DRUŽINI-HIŠA — edina z ×2 blokoma v 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) krstni (P235-h28-dve-družini!); 1916/1917 Ana + Anton PEZDIREC — poročena 30. 1. 1861, Anton †78 let = 56-LETNA ZAKONSKA ZVEZA!",
           "THE TWO-FAMILY HOUSE — the only one with ×2 blocks in 01738 (P253: m2-MAVRIN + m4-TOMC!): 1871 Pezdirc (z81) + Požek (z83) baptisms (P235-h28-two-families!); 1916/1917 Ana + Anton PEZDIREC — married Jan 30 1861, Anton †78 = A 56-YEAR MARRIAGE!"),
    "61": ("TILLAR-hiša: m13-1828-ženin-Miko-TILLAR-½-Gütl-GRIBLJE-61 × nevesta-h22 = POLNI-DVOJNI (P255!) — TILLAR-NIT-×2 (m2-1828-mati-Anna-Tillar-Boršt-13!); ★★★★ P258: m23-1832-NEVESTA-Anna-[~FILACH=FLACH?] (22, oče-Nicol!, GRIBLJE 61 × Peter-[~Šimič]-h56 — POLNI-DVOJNI-28.-Nov!) = 3.-blok-01738 + ★-TILLAR→FILACH-ZAMENJAVA-DRUŽIN-h61 ([~X-OPEN: prodana-kmetija?]) + FLACH-×2-nit (h35!); h61-firstYear-1862→1828 (DVIG 34!); 18 blokov 1828–1919 = 91 let.",
           "The TILLAR house: the m13-1828 groom Miko-TILLAR × the h22-bride = the FULL DOUBLE (P255!) — the TILLAR-thread-×2; ★★★★ P258: the m23-1832 BRIDE Anna [~FILACH] (father Nicol!, GRIBLJE 61 × the [Šimič]-h56 — the FULL DOUBLE!) = the-3rd-01738-block + ★-THE-TILLAR→FILACH-FAMILY-CHANGE ([~X-OPEN]) + the-FLACH-×2-thread (h35!); the h61-firstYear-1862→1828 (LIFT 34!); 18 blocks 1828–1919 = 91 years."),
    "63": ("KRIŽAN-HIŠA (korpus-uradno: 'h63 = KRIŽAN-hiša'!): Križan/Hrižan-continuum 1862–1921 (9+ blokov); m1-KURE-29. 1. 1873 = PRVI VPIS PREDHODNIKA (P253-RESTART-1!); tri poroke Križan 1911/1912/1921; PEZDIRC-mati ×4 (1881–1896).",
           "THE KRIŽAN HOUSE (officially in the corpus: 'h63 = KRIŽAN-hiša'!): the Križan/Hrižan continuum 1862–1921 (9+ blocks); the m1-KURE-Jan 29 1873 = THE FIRST ENTRY OF THE PREDECESSOR (the P253 RESTART-1!); three Križan marriages 1911/1912/1921; the PEZDIRC mother ×4 (1881–1896)."),
    "5": ("MÜLLER-hiša: m10-1829 ženin Mathe MÜLLER (26 l, GRIBLJE 5 × [Šimek?]-h19 — POLNI-DVOJNI, P256!) — h5-firstYear-1859→1829 (DVIG 30!); 31 blokov 1829–1924 — h5-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (12→16, P256!); MÜLLER-×2-družini-1829 (h5-hiša + h22-Millerji!).",
          "The MÜLLER house: the m10-1829 groom Mathe MÜLLER (26, GRIBLJE 5 × the h19-bride — the FULL DOUBLE, P256!) — the h5-firstYear-1859→1829 (LIFT 30!); 31 blocks 1829–1924 — h5-ENTERS-THE-SIX-BOOKS-CLUB (P256!); the MÜLLER-×2-families-of-1829 (the h5-house + the h22-Millers!)."),
    "19": ("[ŠIMEK?]-hiša: m10-1829 nevesta Maria [ŠIMEK?~Knimek/Thimnik — 4-branja-DUEL!] (21 l, GRIBLJE 19 × Müller-h5, P256!) — oče Georg [Šimek?~'Shimek'-garble — ŠIMEC-marker-kand.!] + mati [Salva?] TILLAR! (TILLAR-NIT-1829!); h19-firstYear-1858→1829 (DVIG 29!) — h19-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (P256!).",
          "The [ŠIMEK?] house: the m10-1829 bride Maria [ŠIMEK?~4-reads-DUEL!] (21, GRIBLJE 19 × the Müller-h5, P256!) — the father Georg [Šimek?~garble] + the mother [Salva?] TILLAR! (the-1829-TILLAR-thread!); the h19-firstYear-1858→1829 (LIFT 29!) — h19-ENTERS-THE-SIX-BOOKS-CLUB (P256!)."),
    "32": ("[DEHLIČ?]-hiša: m2-1829 ženin Michael [DEHLIČ?~3-branja-DUEL] (28 l, GRIBLJE 32 [~DUEL-32|33!] × [Malešič?]-h20 — POLNI-DVOJNI, P256!) — MALEŠIČ×MALEŠIČ (mati-ženina + oče-neveste — KRVNO-SOROSTVO-KAND.!); h32-firstYear-1863→1829 (DVIG 34!) — h32-VSTOPA-V-ŠEST-KNJIŽNI-KLUB (P256!).",
          "The [DEHLIČ?] house: the m2-1829 groom Michael [DEHLIČ?~3-reads-DUEL] (28, GRIBLJE 32 [~DUEL-32|33!] × the h20-bride — the FULL DOUBLE, P256!) — the MALEŠIČ×MALEŠIČ-kinship-cand.!; the h32-firstYear-1863→1829 (LIFT 34!) — h32-ENTERS-THE-SIX-BOOKS-CLUB (P256!)."),
    "62": ("★★★★★ KRIŽAN-HRIŽAN-hiša-44-LET: m18-1829 ŽENIN Matthe KRIŽAN (GRIBLJE 62 × Miller-h22 — POLNI-DVOJNI, P256!) + m18-1873 NEVESTA Maria HRIŽAN (h62 × Gabovšič-h13 — ŠIV-P253!) = ISTA-HIŠA-1829–1873!; h62-firstYear-1864→1829 (DVIG 35 = največji P256!); 29 blokov 1829–1924 = 95 let (2.-najdaljši-za-h6-96!)",
          "★★★★★ THE-KRIŽAN-HRIŽAN-HOUSE-44-YEARS: the m18-1829 GROOM Matthe KRIŽAN (GRIBLJE 62 × the Miller-h22 — the FULL DOUBLE, P256!) + the m18-1873 BRIDE Maria HRIŽAN (h62 × the Gabovšič-h13 — the-P253-SEAM!) = THE-SAME-HOUSE-1829–1873!; the h62-firstYear-1864→1829 (LIFT 35 = the-largest-of-P256!); 29 blocks 1829–1924 = 95 years (the-2nd-longest-after-h6-96!)"),
    "73": ("★ TIHA-HIŠA — samo 9 blokov v 6 knjigah (1–2 na knjigo, najtišja šest-knjižna — naslednja h61 ima 17!): m12-KUPAMIČ-1873 s pisarjevim popravkom '13'→'73' (P253!); Županič/Lupanič/Lepančič-garble-continuum 1869–1921; PEZDIRC-mati ×4 (Pezdire/Pegdire/Pozdirec/Pegdirec — 4 grafije!).",
           "★ THE QUIET HOUSE — only 9 blocks in 6 books (1–2 per book, the quietest six-book house — the next, h61, has 17!): the m12-KUPAMIČ-1873 with the scribe's correction '13'→'73' (P253!); the Županič/Lupanič/Lepančič garble continuum 1869–1921; the PEZDIRC mother ×4 (four spellings!)."),
    # ——— P257 NOVIH 7 šest-knjižnih (16→23!) ———
    "1": ("★★★ P257-hiša: m13-1831-ŽENIN-Math.-[Ianigl?~Muniz/Kranigh — 3-variant-GARBLE!] (ledina, GRIBLJE 1 × [Podierz?]-h11 — POLNI-DVOJNI!) — h1-firstYear-1861→1831 (DVIG 30!); 42 blokov 1831–1914 = 83 let (11 v 04106!); [~Muniz?-MUZ-kand. (1828-Semelj-nit!)]; h1 = ena-najstarejših-hiš-Griblja-številka-1!",
          "★★★ The P257 house: the m13-1831 GROOM Math. [Ianigl?~3-variant-GARBLE!] (GRIBLJE 1 × the h11-bride — the FULL DOUBLE!) — the h1-firstYear-1861→1831 (LIFT 30!); 42 blocks 1831–1914 = 83 years (11 in 04106!); [~Muniz?-a-MUZ-cand.!]; h1 = the lowest Griblje house-number!"),
    "11": ("★★★ P257-hiša: m13-1831-NEVESTA-Catharina-[Podierz?~Pesdirz!—DUEL-'Pesdirz-ali-Podierz'] (ledina, GRIBLJE 11 × [Ianigl?]-h1 — POLNI-DVOJNI!) — h11-firstYear-1863→1831 (DVIG 32!); 31 blokov 1831–1922 = 91 let (IZENAČI-h33!-4.-5.-mesto); Pesdirz/Podierz-nit-1831-×4-vrstice (m2/m3/m7/m13!); 04104-prazna (4-knjige→5-01738-P257!→6?)",
           "★★★ The P257 house: the m13-1831 BRIDE Catharina [Podierz?~Pesdirz!] (GRIBLJE 11 × the h1-groom — the FULL DOUBLE!) — the h11-firstYear-1863→1831 (LIFT 32!); 31 blocks 1831–1922 = 91 years (ties-h33!); the-Pesdirz-thread-1831-×4-rows (m2/m3/m7/m13!)"),
    "26": ("★★★ P257-ANOMALIJA-hiša: m7-1831-'ženin'-MARIA-Pödiz? [~Pesdirz?~Podierz?—ŽENSKO-IME-V-ŽENINSKEM-STOLPCU!] ([~26|20-DUEL-w3-'26'-4:2], GRIBLJE 26 × [Maly?]-h27 — POLNI-DVOJNI-ANOMALIJA!) — h26-firstYear-1859→1831 (DVIG 28-[~]); 27 blokov 1831–1921 = 90 let (5.-mesto!); očeN-Georg-[Pödiz?]-istim-imenom-kot-m2-ženin!",
           "★★★ The P257 ANOMALY house: the m7-1831-'groom'-MARIA-Pödiz? [~DUEL — A-FEMALE-NAME-IN-THE-GROOM'S-COLUMN!] (GRIBLJE 26 [~26|20] × the h27-bride — the ANOMALY-FULL-DOUBLE!) — the h26-firstYear-1859→1831 (LIFT 28-[~]); 27 blocks 1831–1921 = 90 years (5th!)"),
    "27": ("★★★ P257-hiša: m7-1831-NEVESTA-Anna-[Maly?~Malež] (GRIBLJE 27 × ANOMALIJA-Maria-h26 — POLNI-DVOJNI!) — h27-firstYear-1864→1831 (DVIG 33 — 4.-največji-vseh-časov!); 30 blokov 1831–1918 = 87 let; h27 = SEGINA-rekord-poročne-04455 (8-blokov!)+031?-ne — zdaj-ŠEST-knjižna-prek-P257!",
           "★★★ The P257 house: the m7-1831 BRIDE Anna [Maly?] (GRIBLJE 27 × the-Maria-h26-ANOMALY — the FULL DOUBLE!) — the h27-firstYear-1864→1831 (LIFT 33 — the-4th-largest!); 30 blocks 1831–1918 = 87 years; h27 = the-04455-marriage-record-SEGINA (8 blocks!) — now-SIX-book-via-P257!"),
    "33": ("★★★ P257-hiša: m1-1831-NEVESTA-Anna-[Dehligl?~Pehligh/Dölker—3-branja + očeN-Mario-Doblioz-DVOJMA!] (GRIBLJE 33 [~33|39-w3-'33'-3:2] × KRIŽAN-h3 — POLNI-DVOJNI!) — h33-firstYear-1859→1831 (DVIG 28-[~]); 31 blokov 1831–1922 = 91 let (IZENAČI-h11!); mati-Dorothea-KRIŽAN!",
           "★★★ The P257 house: the m1-1831 BRIDE Anna [Dehligl?~3-reads + the father's-surname-DVOJMA!] (GRIBLJE 33 [~33|39] × the-KRIŽAN-h3 — the FULL DOUBLE!) — the h33-firstYear-1859→1831 (LIFT 28-[~]); 31 blocks 1831–1922 = 91 years (ties-h11!); the mother Dorothea KRIŽAN!"),
    "56": ("P257-hiša: m3-1831-ŽENIN-Math.-[Kiniz?~Schimiz/Štimic—3-branja] (32, GRIBLJE 56 × [Pedierz?]-Podzemelj-3) — ★★★★ P258: m23-1832-ŽENIN-Peter-[~SIMIG=ŠIMIČ?|Himiz?—3-variant-DUEL-vsi-'-imiz'!] (36, oče-Nicol-[~Šimič!]!, GRIBLJE 56 × Anna-[~Filach]-h61 — POLNI-DVOJNI-28.-Nov!) = 2.-družina-h56-01738 (1831+1832!) + [~ŠIMIČ-kand.-nit-h49-1833!] — h56-firstYear-1867→1831 (DVIG 36 — 3.-največji-trojno-h46/h56/h66!); 15 blokov 1831–1908 = 77 let; mati-[Klepz?]-KLEPEC-nit-kand. (continuum-1828/1829!)",
           "The P257 house: the m3-1831 GROOM Math. [Kiniz?~DUEL] — ★★★★ P258: the m23-1832 GROOM Peter [~ŠIMIČ?] (36, father Nicol!, GRIBLJE 56 × the [Filach]-h61 — the FULL DOUBLE!) = the-2nd-family-of-h56 + [~the-ŠIMIČ-h49-1833-thread!] — the h56-firstYear-1867→1831 (LIFT 36 — the-triple-3rd!); 15 blocks 1831–1908 = 77 years; the-[Klepz?]-KLEPEC-thread"),
    "65": ("★★★★★ P257-MILEK-hiša: m10-1831-ŽENIN-Nicol-MILEK ('-ek'-1:1!-oče-Janez!, GRIBLJE 65 × [Prodsanzig?]-Podzemelj-2) — h65-firstYear-1857→1831 (DVIG 26!) — ★-h65-BILA-PRVA-HIŠA-KORPUSA-1857 (korpus-prvi-vpis-PRE-P255!) + MILEK-h65-NIT: 1831↔1874-P250 = 43-LET-družine!; 44 blokov = 2.-najglasnejša (za-h24-45!) + 14 v 04106 = REKORD-skupaj-s-h13; zdaj-ŠEST-knjižna-prek-P257!",
           "★★★★★ The P257-MILEK house: the m10-1831 GROOM Nicol MILEK (father-Janez!, GRIBLJE 65 × the Podzemelj-2-bride) — the h65-firstYear-1857→1831 (LIFT 26!) — ★-h65-WAS-THE-FIRST-HOUSE-OF-THE-CORPUS-1857 + THE-MILEK-THREAD: 1831↔1874 = A-43-YEAR-family!; 44 blocks = the-2nd-loudest (after h24-45!) + 14 in 04106 = the record-with-h13; now-SIX-book-via-P257!"),
    # ——— P258 NOVIH 8 šest-knjižnih (23→31!) ———
    "2": ("★★★★★ P258-hiša-DVAKRAT-V-ZAPOREDNIH-LETIH: 1831-NEVESTA-Anna-[~Kleberz=KLEBEC-kand.!] (24, GRIBLJE 2 × Johann-KLOBUČAR-h48 — POLNI-DVOJNI-24.-Avg!) + 1832-ŽENIN-Johann-[HLEBEC!] (21, oče-Johann-kmet!, GRIBLJE 2 × Anna-[~Petriz]-h42-[~Gríblje|Smrečje-DUEL] — POLNI-DVOJNI-[~]-29.-Febr-PRESTOPNI!) = ★-ISTA-HIŠA-2-LETI-ZAPORED-2-DRUGI-VLOGI (nevesta→ženin!) — h2-firstYear-1858→1831 (DVIG 27!) + ★★★★★-HLEBEC-NIT: 1832-h2 ↔ 1873-m11-h3-P253 (41-let!-sosednji-hiši!); 34 blokov 1831–1924 = 93 let (IZENAČI-h20/h22/h50!); zdaj-ŠEST-knjižna (23→31!)",
           "★★★★★ The P258 house TWICE-IN-CONSECUTIVE-YEARS: the 1831 BRIDE Anna [~Kleberz?] (GRIBLJE 2 × the KLOBUČAR-h48 — the FULL DOUBLE!) + the 1832 GROOM Johann [HLEBEC!] (GRIBLJE 2 × the h42-bride — the leap-day-FULL-DOUBLE-[~]!) = ★-THE-SAME-HOUSE-2-YEARS-2-DIFFERENT-ROLES (bride→groom!) — the h2-firstYear-1858→1831 (LIFT 27!) + ★★★★★ THE-HLEBEC-THREAD: 1832-h2 ↔ 1873-m11-h3 (41-years!); 34 blocks 1831–1924 = 93 years (ties-h20/h22/h50!); now-SIX-book (23→31!)"),
    "8": ("★★★★★ P258-hiša-DVIG-40 = 2.-NAJVEČJI-VSEH-ČASOV: 1831-NEVESTA-Catharina-[~Klofčič] (18, GRIBLJE 8 × Matthias-KLOBUČAR-h46 — POLNI-DVOJNI-24.-Avg!-KLOBUČAR-BRATJE-m19×m20-ISTI-DAN!) — h8-firstYear-1871→1831 (DVIG 40!-za-h22-41-P255!-pred-h46/h66-36!) + 39 blokov 1831–1919 = 88 let; zdaj-ŠEST-knjižna (23→31!)",
           "★★★★★ The P258 house — THE-LIFT-40 = THE-2ND-LARGEST-EVER: the 1831 BRIDE Catharina [~Klofčič] (18, GRIBLJE 8 × the KLOBUČAR-h46 — the FULL DOUBLE of Aug 24!-the-KLOBUČAR-brothers-same-day!) — the h8-firstYear-1871→1831 (LIFT 40!-after-h22-41-P255!) + 39 blocks 1831–1919 = 88 years; now-SIX-book (23→31!)"),
    "35": ("★★★★★ P258-hiša-DVE-DRUŽINI-V-ENEM-LETU: 1832-m8-NEVESTA-Anna-[~Štremuz] (21, GRIBLJE 35 × Johann-MILEK-h22 — POLNI-DVOJNI-15.-Febr!) + 1832-m17-NEVESTA-Catharina-[~FLACH] (17, oče-Peter!, GRIBLJE 35 × Nicol-KRIŽAN-h36 — POLNI-DVOJNI-29.-Febr-PRESTOPNI!) = ★-DVA-PAROV-IZ-h35-V-14-DNEH-ISTEGA-LETA (cf.-h28-×2-1873!) — h35-firstYear-1867→1832 (DVIG 35!) + ★-FLACH-×2-NIT (h35+h61!) + 37 blokov 1832–1922 = 90 let + HRIŽAN-družina-04894:15-REKORD; zdaj-ŠEST-knjižna (23→31!)",
            "★★★★★ The P258 house — TWO-FAMILIES-IN-ONE-YEAR: the m8-1832 BRIDE Anna [~Štremuz] (GRIBLJE 35 × the MILEK-h22 — the FULL DOUBLE!) + the m17-1832 BRIDE Catharina [~FLACH] (GRIBLJE 35 × the KRIŽAN-h36 — the leap-day-FULL-DOUBLE!) = ★-TWO-COUPLES-FROM-h35-IN-14-DAYS (cf.-h28-×2-1873!) — the h35-firstYear-1867→1832 (LIFT 35!) + ★-THE-FLACH-×2-THREAD (h35+h61!) + 37 blocks 1832–1922 = 90 years + the HRIŽAN-04894:15-RECORD; now-SIX-book (23→31!)"),
    "36": ("★★★ P258-KRIŽAN-hiša: 1832-ŽENIN-Nicol-KRIŽAN (20, oče-Matthias!, GRIBLJE 36 × Catharina-[~Flach]-h35 — POLNI-DVOJNI-29.-Febr-prestopni!) — ★★★★★-KRIŽAN-KONGLOMERAT: 1831-h3 + 1832-h36 + 1832-h66 + 1873-h63 = 4-GRIBLJE-HIŠE + HRIŽAN-h62-ŠIV = 5-hiš-istega-korena! — h36-firstYear-1857→1832 (DVIG 25!); 34 blokov 1832–1917 = 85 let; zdaj-ŠEST-knjižna (23→31!)",
            "★★★ The P258-KRIŽAN house: the 1832 GROOM Nicol KRIŽAN (20, father-Matthias!, GRIBLJE 36 × the h35-bride — the leap-day-FULL-DOUBLE!) — ★★★★★ THE-KRIŽAN-CONGLOMERATE: 1831-h3 + 1832-h36 + 1832-h66 + 1873-h63 = 4-GRIBLJE-HOUSES + the h62-seam = 5-houses-of-one-root! — the h36-firstYear-1857→1832 (LIFT 25!); 34 blocks 1832–1917 = 85 years; now-SIX-book (23→31!)"),
    "42": ("★★★ P258-hiša-[~village-DUEL]: 1832-NEVESTA-Anna-[~Petriz] (17, oče-Matthias-kmet!, [~GRIBLJE-2:1|Smrečje?-DUEL-VAS-X-OPEN!] 42 × Johann-[HLEBEC]-h2 — POLNI-DVOJNI-[~]-29.-Febr-PRESTOPNI!) — h42-firstYear-1861→1832 (DVIG 29-[~vas-DUEL-ostaja!]); 28 blokov 1832–1912 = 80 let; zdaj-ŠEST-knjižna-[~DUEL] (23→31!)",
            "★★★ The P258 house-[~village-DUEL]: the 1832 BRIDE Anna [~Petriz] (17, [~GRIBLJE-2:1|Smrečje?-DUEL] 42 × the [HLEBEC]-h2 — the leap-day-FULL-DOUBLE-[~]!) — the h42-firstYear-1861→1832 (LIFT 29-[~duel-remains!]); 28 blocks 1832–1912 = 80 years; now-SIX-book-[~] (23→31!)"),
    "46": ("★★★ P258-KLOBUČAR-hiša: 1831-ŽENIN-Matthias-KLOBUČAR (27, oče-Mathias!, GRIBLJE 46 × Catharina-[~Klofčič]-h8 — POLNI-DVOJNI-24.-Avg!) — ★-KLOBUČAR-BRATJE-m19×m20 (h46×h8-+-h48×h2-DVA-POLNA-DVOJNA-ISTEGA-DNE!-[~bratje-kand.]) — h46-firstYear-1867→1831 (DVIG 36 = 3.-mesto-TROJNO-h46/h56/h66!); 39 blokov 1831–1920 = 89 let; zdaj-ŠEST-knjižna (23→31!)",
            "★★★ The P258-KLOBUČAR house: the 1831 GROOM Matthias KLOBUČAR (27, father-Mathias!, GRIBLJE 46 × the h8-bride — the FULL DOUBLE of Aug 24!) — ★-THE-KLOBUČAR-BROTHERS-m19×m20 (TWO-FULL-DOUBLES-OF-THE-SAME-DAY!) — the h46-firstYear-1867→1831 (LIFT 36 = the-3rd-place-TRIPLE!); 39 blocks 1831–1920 = 89 years; now-SIX-book (23→31!)"),
    "47": ("★★★★★ P258-PEZDIRC-PRIČA-hiša: 1831-NEVESTA-Maria-KLOBUČAR (20, GRIBLJE 47 × Andreas-[~Mercina|Hribar|Luminanic?-3-variant-GARBLE]-ŠKRILJE-1 — 9.-Febr-d°-12.-poroka-dneva!) — ★★★★★-PRIČA-AND.-PEZDIRC (duel-'Pezdirc'-jasno!-[~Simon-zavrnjen]) = 5.-VRSTICA-Pesdirc-družine-1831 (ženin+nevesta+ANOMALIJA+nevesta+PRIČA!-vse-vrste!) — h47-firstYear-1862→1831 (DVIG 31!); 19 blokov 1831–1919 = 88 let (TIHA-nova-šest-knjižna!); zdaj-ŠEST-knjižna (23→31!)",
            "★★★★★ The P258 PEZDIRC-WITNESS house: the 1831 BRIDE Maria KLOBUČAR (20, GRIBLJE 47 × Andreas-[~3-variant-GARBLE]-of-ŠKRILJE-1 — the Feb-9-d°-12th-wedding!) — ★★★★★ THE-WITNESS-AND.-PEZDIRC = the-5th-ROW-of-the-1831-Pesdirc-family (all-kinds!) — the h47-firstYear-1862→1831 (LIFT 31!); 19 blocks 1831–1919 = 88 years (a-quiet-new-six-book!); now-SIX-book (23→31!)"),
    # ——— P259 KANDIDATI (DRAFT — potrdi/prilagodi po VLM-branjih + reconcile!) ———
    "24": ("★★★★★ P259-Najglasnejša-hiša-KORPUSA-KONČNO-ŠEST-KNJIŽNA: m?-1833-nevesta-Maria-[~BRING|BRINC]-GRIBLJE-24 × [~Gosling|Pesdirz]-h53|h33 (6.-Febr-d°-kaskada!) = PRVI-01738-blok-najglasnejše-hiše (45-blokov!) — h24-firstYear-1859→1833 (DVIG 26!) + polni-cikel-VSEH-6-knjig; [~DUEL: Bring|Brinc + h24-potrditev!]",
           "★★★★★ P259-THE-LOUDEST-HOUSE-FINALLY-SIX-BOOK: the 1833 bride Maria [~BRING|BRINC] of GRIBLJE 24 (the Feb-6-cascade!) = the FIRST-01738-block-of-the-corpus'-loudest-house (45 blocks!) — the h24-firstYear-1859→1833 (LIFT 26!) + the full-6-book-cycle; [~DUEL!]"),
    "28": ("DVE-DRUŽINI-HIŠA — edina z ×2 blokoma v 01738 (P253: m2-MAVRIN + m4-TOMC!) — ★★★ P259: +3.-blok-1833 (Georg-[~BRING]-h28?) — h28-firstYear-1865→1833 (DVIG 32!) + 1871-Pezdirc/Požek-krsti (P235!); 1916/1917 Ana + Anton PEZDIREC — 56-LETNA ZAKONSKA ZVEZA!",
           "THE TWO-FAMILY HOUSE — ★★★ P259: +the-3rd-1833-block ([~BRING]-h28!) — the h28-firstYear-1865→1833 (LIFT 32!); the 1871 Pezdirc/Požek baptisms (P235!); Ana + Anton PEZDIREC — A 56-YEAR MARRIAGE!"),    "53": ("P259-hiša [~KANDIDAT — h33|h53-DUEL-ženina-s11_r2!]: m?-1833-ženin-[~Gosling|Pesdirz|Gutting]-GRIBLJE-53 × Maria-[~Bring]-h24 (6.-Febr-1833!) — h53-firstYear-1863→1833 (DVIG 30?) + šest-knjižna?; [~ČE-h33-name: 2.-01738-blok-1831+1833-BREZ-dviga (firstYear-že-1831)!]",
           "The P259 house [~THE-h33|h53-DUEL]: the 1833 groom [~Gosling|Pesdirz] of GRIBLJE 53 (Feb-6-1833!) — the h53-firstYear-1863→1833 (LIFT 30?); [~IF-h33-instead: no-lift!]"),    "60": ("P259-ŠIMIČ-hiša [~KANDIDAT]: m?-Oct-1833-ženin-Georg-[~SCHMIG=ŠIMIČ?]-GRIBLJE-60 × Katharina-[~Kresling|Kosting]-h21 — ★-ŠIMIČ-nit-3-vrstice-3-hiše (1832-Peter-h56-oče-Nicol-Šimič + 1833-Maria-h49!) — h60-firstYear-1857→1833 (DVIG 24?) + šest-knjižna?; [~DUEL: Schmig|Amiz + h60-potrditev!]",
           "The P259 ŠIMIČ house [~CANDIDATE]: the Oct-1833 groom Georg [~ŠIMIČ] of GRIBLJE 60 — ★-the-ŠIMIČ-thread-3-rows (1832-h56 + 1833-h49!) — the h60-firstYear-1857→1833 (LIFT 24?); [~DUEL!]"),    "48": ("★★★ P258-KLOBUČAR-2-hiša: 1831-ŽENIN-Johann-KLOBUČAR (29, GRIBLJE 48 × Anna-[~Kleberz]-h2 — POLNI-DVOJNI-24.-Avg-d°-ISTI-DAN-kot-m19!) — [~očeN-Vincenz-PARON?-BARON-m21-veza-kand.!] — h48-firstYear-1857→1831 (DVIG 26!); 33 blokov 1831–1922 = 91 let (IZENAČI-h11/h33!); zdaj-ŠEST-knjižna (23→31!)",
            "★★★ The P258-KLOBUČAR-2 house: the 1831 GROOM Johann KLOBUČAR (29, GRIBLJE 48 × the h2-bride — the FULL-DOUBLE-same-day-as-m19!) — [~the-father-Vincenz-BARON?-candidate!] — the h48-firstYear-1857→1831 (LIFT 26!); 33 blocks 1831–1922 = 91 years (ties-h11/h33!); now-SIX-book (23→31!)"),
}

lines = []
A = lines.append
A("// P254+P255+P256+P257+P258+P259: HIŠNE ZGODBE GLOBJE — mreže hiš čez 6 knjig (regenerirano P259: +bloki 1833-nadaljevanje/1834 s11–s13!; 2026-11-12)")
A(f"// SINTEZNA FAZA: agregacija celotnega korpusa HOUSE_VITALS ({EXPECTED_TOTAL} vitalov) po hišah čez VSEH 6 knjig:")
A("// 01738 (poročna-predhodnik 1828–1834 + 1873 — P259: +bloki 1833k/1834!) + 04104 (krstna-predzgodovina 1871–1885)")
A("// + 04105 (krstna-linija 1887–1919) + 04455 (poročna 1873–1922) + 04106 (mrliška-predzgodovina 1857–1885)")
A("// + 04894 (mrliška-linija 1886–1924). 100 hišnih oznak = 78 Griblje (1–78) + 16 druga-vas (79–98) + 6 neznanek.")
A(f"// ★★★★★ P259: {EXPECTED_SIX} ŠEST-KNJIŽ-HIŠ (P254-9 → P255-12 → P256-16 → P257-23 → P258-31 → P259-{EXPECTED_SIX}!):")
missing = [h for h in six if h not in SIX_STORIES]
extra = [h for h in SIX_STORIES if h not in six]
assert not missing and not extra, f"SIX_STORIES: manjka {missing}, odveč {extra}"
A("// " + ", ".join(six) + " — P259-dodane so v SIX_STORIES označene s P259-komentarjem!")
A("// ★★★★★ P259-DVIGI (izpolni po integraciji!): h24-26/h28-32/h51-33?/h53-30?/h58-25?/h60-24?/h68-27? — glej p259Dvigi-spodaj!")
A("// ★★★★★ P258-10-DVIGOV: h8-40 (2.-vseh-časov!) + h46/h66-36 + h35-35 + h47-31 + h42-29[~] + h2-27 + h48-26 + h36-25 + h49-25 + h22-4.-blok-v-5-letih")
A(f"// Razponi: h6-96/h62-95/h2+h50+h20+h22-93 — bothEra-poročna 34→{EXPECTED_BOTH_P} (P259!). Dokaz: research/issue17/parish-house-stories.json; verifikator: scripts/p254_house_stories.py --check; regenerator: scripts/tmp/p259_gen.py.")
A("")
A("export interface HouseStory {")
A("  houseNo: string;")
A('  kind: "griblje" | "druga-vas" | "neznano";')
A("  /** skupno število vitalnih blokov hiše v korpusu */")
A("  blocks: number;")
A("  /** število različnih knjig s hišnim blokom (1–6) */")
A("  books: number;")
A("  perBook: { sig: string; n: number }[];")
A("  firstYear: number;")
A("  lastYear: number;")
A("  span: number;")
A("}")
A("")
A("export interface HouseStoryBookMeta {")
A("  sig: string;")
A("  roleSi: string;")
A("  roleEn: string;")
A("  years: string;")
A("  blocks: number;")
A("  houses: number;")
A("  recordSi: string;")
A("}")
A("")
A("export const HOUSE_STORY_BOOKS: HouseStoryBookMeta[] = [")
for b in BOOKS:
    roleSi, roleEn, years, rec = book_meta[b]
    n_blocks = sum(len(v) for d in houses.values() for bb, v in d.items() if bb == b)
    n_houses = sum(1 for d in houses.values() if b in d)
    A(f'  {{ sig: "{b}", roleSi: "{roleSi}", roleEn: "{roleEn}", years: "{years}", blocks: {n_blocks}, houses: {n_houses}, recordSi: "{rec}" }},')
A("];")
A("")
A("/** Vseh 100 hišnih oznak korpusa — Griblje (1–78) številsko, druga-vas (79–98), nato neznanke. */")
A("export const HOUSE_STORIES: HouseStory[] = [")
for h in order:
    A(entry(h))
A("];")
A("")
A("export function houseStoryByNo(no: string): HouseStory | undefined {")
A("  return HOUSE_STORIES.find((h) => h.houseNo === no);")
A("}")
A("")
A("export interface HouseStorySix {")
A("  houseNo: string;")
A("  blocks: number;")
A("  years: string;")
A("  storySi: string;")
A("  storyEn: string;")
A("}")
A("")
A("/** ★★★★★ 31 ŠEST-KNJIŽ-HIŠ (P258!) — blok v VSEH 6 knjigah = polni življenjski cikel (obe eri × vse 3 vrste). */")
A("export const HOUSE_STORY_SIX: HouseStorySix[] = [")
for h in six:
    d = houses[h]
    yrs = sorted(y for v in d.values() for y in v)
    tot = sum(len(v) for v in d.values())
    si, en = SIX_STORIES[h]
    si = si.replace('"', "'")
    en = en.replace('"', "'")
    A(f'  {{ houseNo: "{h}", blocks: {tot}, years: "{yrs[0]}–{yrs[-1]}", storySi: "{si}", storyEn: "{en}" }},')
A("];")
A("")
A("export interface HouseStoryTier {")
A("  books: number;")
A("  houses: number;")
A("  labelSi: string;")
A("}")
A("")
A(f"/* Pokritje po številu knjig: {tiers[6]}/{tiers[5]}/{tiers[4]}/{tiers[3]}/{tiers[2]}/{tiers[1]} = 100 (P259!). */")
A("export const HOUSE_STORY_TIERS: HouseStoryTier[] = [")
labels = {6: "šešt-knjižne (polni cikel!)", 5: "pet-knjižne", 4: "štiri-knjižne", 3: "tri-knjižne", 2: "dvo-knjižne", 1: "eno-knjižne"}
for k in [6, 5, 4, 3, 2, 1]:
    A(f'  {{ books: {k}, houses: {tiers[k]}, labelSi: "{labels[k]}" }},')
A("];")
A("")
A("export const HOUSE_STORY_TOTALS = {")
A("  houses: 100,")
A("  griblje: 78,")
A("  drugaVas: 16,")
A("  neznano: 6,")
A(f"  blocks: {EXPECTED_TOTAL},")
A(f"  sixBook: {tiers[6]},")
A(f"  fiveBook: {tiers[5]},")
A(f"  fourBook: {tiers[4]},")
A("  bothEraKrstna: 69,")
A("  bothEraMrliska: 75,")
A(f"  bothEraPorocna: {EXPECTED_BOTH_P},")
A('  loudest: "24",')
A("  loudestBlocks: 45,")
A('  quietest6: "73",')
A("  quietest6Blocks: 9,")
A("  longestSpan: 96,")
A('  longestSpanHouses: ["6"],')
A('  deathsGap: "25",')
A('  p256Dvigi: "h62/h32/h5/h20/h19 = 35/34/30/30/29 (1829!)",')
A('  p257Dvigi: "h54/h56/h27/h11/h1/h26/h33/h3/h50/h65 = 37/36/33/32/30/28/28/27/27/26 (1831!) + h22-3-leto-1830!",')
A('  p258Dvigi: "h8/h46/h66/h35/h47/h42/h2/h48/h36/h49 = 40/36/36/35/31/29/27/26/25/25 (1831/32/33!) + h22-4-bloki-v-5-letih + h35-×2-družini!",')
A('  p259Dvigi: "h51-33/h28-32/h53-30/h68-27/h24-26/h60-24 (1833k/1834!-h58-ZAVRŽEN-s13_r6-hiša-68-POTRJENA!)",')
A("} as const;")
A("")
A("export interface HouseStoryNotable {")
A("  id: string;")
A("  titleSi: string;")
A("  titleEn: string;")
A("  bodySi: string;")
A("  bodyEn: string;")
A("}")
A("")
A("/** Osamelci, rekordi in vrzeli mreže — 7 zgodb (P257-posodobljene). */")
A("export const HOUSE_STORY_NOTABLES: HouseStoryNotable[] = [")
notables = [
    ("najglasnejsa", "h24 = najglasnejša hiša korpusa",
     "The h24 = the loudest house of the corpus",
     "45 blokov (1859–1920) — 18 v 04105 = REKORD KRSTNE LINIJE; a samo 5 knjig: 01738 je nima (niti 1873 niti 1828–1831 — P255/P257!). 8 blokov tudi v 04104.",
     "45 blocks (1859–1920) — 18 in 04105 = THE BAPTISM LINE RECORD; but only 5 books: 01738 lacks it (neither 1873 nor 1828–1831 — P255/P257!). Also 8 blocks in 04104."),
    ("h65", "h65 = 44 blokov (P257! +1), rekord mrliške predzgodovine",
     "The h65 = 44 blocks (P257! +1), the death-prehistory record",
     "★★★★★ P257: h65-BILA-PRVA-HIŠA-KORPUSA-1857 — zdaj-firstYear-1831 (DVIG 26!) + MILEK-NIT-1831↔1874 = 43-let!; 44 blokov (1831–1914); 14 v 04106 = REKORD skupaj s h13; MILEK-družina (P218/P220/P224/P246 + P257 = 5 virov!); zdaj ŠEST-knjižna (16→23!)",
     "★★★★★ P257: h65-WAS-THE-FIRST-HOUSE-1857 — now-firstYear-1831 (LIFT 26!) + THE-MILEK-THREAD-1831↔1874 = 43 years!; 44 blocks (1831–1914); 14 in 04106 = THE RECORD with h13; the MILEK family (5 sources!); now SIX-book (16→23!)"),
    ("h35", "h35 = rekord mrliške linije 04894 + DVE DRUŽINI 1832 (P258!)",
     "The h35 = the death-line 04894 record + TWO FAMILIES of 1832 (P258!)",
     "15 blokov v 04894 (1886–1924) = NAJVEČ V ENI KNJIGI med vsemi hišami; HRIŽAN-družina (P229!). ★★★★★ P258: h35-firstYear-1867→1832 (DVIG 35!) + ★-DVA-PAROV-IZ-h35-V-14-DNEH-1832 (m8-Štremuz-15.-Febr + m17-Flach-29.-Febr — cf.-h28-×2-1873!) + FLACH-×2-nit (h61!) + zdaj ŠEST-knjižna (23→31!); skupaj 37 blokov 1832–1922.",
     "15 blocks in 04894 (1886–1924) = THE MOST IN ONE BOOK of all houses; the HRIŽAN family (P229!). ★★★★★ P258: the-h35-firstYear-1867→1832 (LIFT 35!) + ★-TWO-COUPLES-FROM-h35-IN-14-DAYS (cf.-h28-×2-1873!) + the-FLACH-×2-thread + now-SIX-book; 37 blocks 1832–1922."),
    ("h27", "h27 = rekord poročne knjige 04455 — zdaj šest-knjižna (P257!)",
     "The h27 = the 04455 marriage record — now six-book (P257!)",
     "★★★ P257: m7-1831-NEVESTA-Anna-[Maly?] (Griblje 27!) — h27-firstYear-1864→1831 (DVIG 33 — 4.!) + 30 blokov 1831–1918; 8 blokov v 04455 = REKORD POROČNE (SEGINA-hiša: 1875 + 1881 + 1882 + 1884 + …); Jacob-63-l-×-Anna-HRIŽAN-1875 (P250).",
     "★★★ P257: the m7-1831 BRIDE Anna [Maly?] (Griblje 27!) — the h27-firstYear-1864→1831 (LIFT 33!) + 30 blocks 1831–1918; 8 blocks in 04455 = THE MARRIAGE RECORD (the SEGINA house); Jacob-63-y-o × Anna HRIŽAN 1875 (P250)."),
    ("smrtna-vrzeli", "h25 = SMRTNA VRZEL 29 let + P258: h66/h49 = POROČNI VRZELI (BREZ 04455!)",
     "The h25 = A 29-YEAR DEATH GAP + P258: h66/h49 = MARRIAGE GAPS (WITHOUT 04455!)",
     "5 knjig a BREZ 04106: noben mrliški zapis 1857–1885 (29 let!) kljub krstnim blokom 1876 + 1883 ×2 in poroki v 01738 (m3-kandidat, P253!). Šele 04894 prinese 7 blokov (1888–1923) — mrežna luknja, ne stvarna. ★★★ P258: h66 (KRIŽAN-h66-1832!) in h49 (Maria-[Himiz]-1833!) = 5 knjig BREZ 04455 — poročni vrzeli! (h49 tudi BREZ 04104 ne — 04104+04105+04106+04894+01738!)",
     "5 books but WITHOUT 04106: no death record 1857–1885 (29 years!) despite the baptisms 1876 + 1883 ×2. ★★★ P258: h66 (the-KRIŽAN-house-1832!) and h49 (the-1833-bride!) = 5 books WITHOUT 04455 — marriage gaps!"),
    ("razponi-96", "P255: h6 = 96-letni razpon (ostaja rekord!)",
     "P255: the h6 = a 96-year span (the standing record!)",
     "h6 dokumentirana 1828→1924 (96 let!); sledita h62 (95: 1829–1924) in ★★★ P257/P258: h50/h20/h22/h2 (93: ★-h2-1831–1924-NOVO-P258-izenači-trojno!) + h11/h33/h48/h61 (91: ★-h48+h61-P258!) + h26/h35 (90: ★-h35-1832–1922-P258!) + h27 (87) + h46 (89-P258!); stari-rekord-66 (h2/h13/h50/h60/h64) ostaja za štiri-knjižnimi.",
     "The h6 documented 1828→1924 (96 years!); then h62 (95) and ★★★ P257: h50/h20/h22 (93 — h50's new 3rd place!) + h11/h33 (91!) + h26 (90!) + h27 (87); the old record 66 remains for the four-book houses."),
    ("skrita-hisa", "h[?] = skrita hiša brez številke",
     "The h[?] = the hidden house without a number",
     "10 blokov 1857–1885 (8 v 04104 + 2 v 04106) z izpraznjeno hišno celico — edina hiša korpusa brez številke; P235/P220 X-OPEN. V kasnejših knjigah izgine (razrešena številka?).",
     "10 blocks 1857–1885 (8 in 04104 + 2 in 04106) with an emptied house cell — the only corpus house without a number; P235/P220 X-OPEN. It vanishes in the later books (a resolved number?)."),
]
for nid, tsi, ten, bsi, ben in notables:
    bsi = bsi.replace('"', "'")
    ben = ben.replace('"', "'")
    A(f'  {{ id: "{nid}", titleSi: "{tsi}", titleEn: "{ten}", bodySi: "{bsi}", bodyEn: "{ben}" }},')
A("];")

open(OUT_TS, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"OK TS: {OUT_TS}: {len(lines)} lines, {len(order)} houses, six={len(six)}")

# ——— dokaz JSON ———
def house_json(h):
    d = houses[h]
    yrs = sorted(y for v in d.values() for y in v)
    return {
        "houseNo": h, "kind": kind_of(h),
        "blocks": sum(len(v) for v in d.values()), "books": len(d),
        "perBook": {b: len(d[b]) for b in BOOKS if b in d},
        "firstYear": yrs[0], "lastYear": yrs[-1], "span": yrs[-1] - yrs[0],
    }

five_missing = {h: [b for b in BOOKS if b not in houses[h]]
                for h, d in houses.items() if len(d) == 5}
h24 = houses["24"]
h24_tot = sum(len(v) for v in h24.values())
h24_yrs = sorted(y for v in h24.values() for y in v)
h65 = houses["65"]
h35 = houses["35"]
h27 = houses["27"]
records = {
    "loudest": {"house": "24", "blocks": h24_tot, "years": f"{h24_yrs[0]}–{h24_yrs[-1]}", "note": "04105:18 = rekord krstne linije"},
    "secondLoudest": {"house": "65", "blocks": sum(len(v) for v in h65.values()), "note": "04106:14 = rekord mrliške predzgodovine (skupaj h13); MILEK-družina — P257: +1831 (+44 blokov!)"},
    "deathLineRecord": {"house": "35", "blocks04894": len(h35["04894"]), "note": "HRIŽAN-družina (P229!)"},
    "marriageRecord": {"house": "27", "blocks04455": len(h27["04455"]), "note": "SEGINA-hiša — 1875+1881+1882+1884+… — P257: h27-postala-šest-knjižna!"},
    "baptismPrehistoryRecord": {"houses": ["6", "40", "[?]"], "blocks04104": len(houses["6"]["04104"]), "note": "trospec — h[?] = skrita hiša brez številke!"},
    "longestSpan": {"years": best_span, "houses": [best_house], "note": "P255: h6-1828→1924 (96!); P257: h50-93-NOVO-3.-mesto + h11/h33-91 + h26-90"},
    "firstYearLiftsP258": {"h8": 40, "h46": 36, "h66": 36, "h35": 35, "h47": 31, "h42": 29, "h2": 27, "h48": 26, "h36": 25, "h49": 25,
                           "note": "P258: 10 dvigov (h8 −40 = 2. največji vseh časov za h22-41-P255!); h46/h56/h66 = 3.-mesto-TROJNO!; h22-BREZ-dviga-ampak-4.-BLOK-V-5-LETIH (1828/29/30/32!); h35-×2-DVE-DRUŽINI-1832!; h42-[~village-DUEL]"},
    "firstYearLiftsP257": {"h54": 37, "h56": 36, "h27": 33, "h11": 32, "h1": 30, "h26": 28, "h33": 28, "h3": 27, "h50": 27, "h65": 26,
                           "note": "P257: 10 dvigov (h54 −37 = 2. največji vseh časov za h22-41-P255!); h22-BREZ-dviga-ampak-3.-ZAPOREDNO-LETO-1830!; h65-bila-prva-hiša-korpusa-1857!"},
    "firstYearLiftsP256": {"h62": 35, "h32": 34, "h5": 30, "h20": 30, "h19": 29, "note": "P256: 5 dvigov (h62 −35 = največji P256)"},
    "firstYearLiftsP255": {"h6": 32, "h22": 41, "h61": 34, "note": "h22 −41 = absolutni rekord dviga matrične linije (prej h43 −34, P250!)"},
}
anomalies = {
    "deathsGap": "h25: 5 knjig BREZ 04106 — noben mrliški zapis 1857–1885 (29 let!) kljub krstnim 1876+1883×2 — mrežna luknja",
    "hiddenHouse": "h[?]: 10 blokov 1857–1885 (04104:8 + 04106:2) brez hišne številke — P235/P220-X-OPEN",
    "m7anomalija": "P257: m7-1831-'ženin'-MARIA-Pödiz — ŽENSKO-IME-V-ŽENINSKEM-STOLPCU (cf.-MUZ-vrstica-P255!) — h26-[~26|20]-DUEL",
    "bothEraCoverage": {"krstna": bk, "mrlishka": bm_, "porocna": bp,
                        "note": f"P258: poročna obe-eri 26→34 (+8 — h47/h46/h8/h48/h2/h35/h36/h42-dodane!-h66/h49-BREZ-04455-poročne-vrzeli!)"},
    "p258vrzeli": "h66 + h49 = 5 knjig BREZ 04455 (poročni vrzeli!); h50 = 5 knjig BREZ 04104!",
    "m2anomalija1832": "P258: m2-1832-'ženin'-MARIA-VIPAVC — ŽENSKO-IME-V-ŽENINSKEM-STOLPCU (duel-črko-za-črko-'M-a-r-i-a'!-2.-za-P257-m7!) + m3-[~Marino-MOŠKI-DUEL]",
}
book_json = []
for b in BOOKS:
    roleSi, roleEn, years, rec = book_meta[b]
    book_json.append({
        "sig": b, "role": roleSi, "years": years,
        "blocks": sum(len(v) for d in houses.values() for bb, v in d.items() if bb == b),
        "houses": sum(1 for d in houses.values() if b in d),
    })
stories_json = {h: {"si": SIX_STORIES[h][0], "en": SIX_STORIES[h][1]} for h in six}
dokaz = {
    "phase": "P254+P255+P256+P257+P258+P259 (regenerirano P259)",
    "title": "Hišne zgodbe globje — mreže hiš čez 6 knjig (+P259: bloki 1833-nadaljevanje/1834 s11–s13!)",
    "date": "2026-11-12",
    "type": "sinteza-agregacija",
    "lead": "P252-lead-② + P253 + P255–P258 + P259-1833k/1834 (korpus-leta-1828–1834+1873!)",
    "source": {"corpus": "src/data/atlas/parish.ts HOUSE_VITALS", "vitalsTotal": EXPECTED_TOTAL, "books": 6,
               "bookSigs": BOOKS,
               "method": "agregacija vseh vitalnih blokov po hišni oznaki — 1:1 z runtime (qa-p254 živa rekalkulacija!)"},
    "structure": {
        "housesTotal": 100, "griblje": 78, "drugaVas": 16, "neznano": 6,
        "neznanoOznake": ["13 [~]", "17 [~]", "32 [~]", "29 [~X-OPEN]", "[?]", "sub dioe."],
        "tiers": {"six": tiers[6], "five": tiers[5], "four": tiers[4], "three": tiers[3], "two": tiers[2], "one": tiers[1]},
        "tiersSum": tiers_sum,
    },
    "sixBookHouses": {
        "houses": six, "count": len(six),
        "note": "blok v VSEH 6 knjigah = polni življenjski cikel — P254: 9 → P255: 12 → P256: 16 → P257: 23 (h1/h11/h26/h27/h33/h56/h65 vstopajo prek 1831!)",
        "stories": stories_json,
    },
    "missingBookAnalysis": {"fiveBookMissing": five_missing,
                            "note": "P257: pet-knjižne 46→41 (h1/h11/h26/h27/h33/h56/h65-izstopajo-v-šest-knjižne; h50/h54-vstopajo-iz-štiri-knjižnih!)"},
    "records": records,
    "anomalies": anomalies,
    "bookMeta": book_json,
    "houses": [house_json(h) for h in order],
    "korpusUcinek": {
        "vitalsTotal": 2043,
        "p255": "+3 bloki 1828 — šest-knjižne 9→12, razpon 66→96 (h6)",
        "p256": "+5 blokov 1829 — šest-knjižne 12→16, bothEra-poročna 13→17, dvigi 35/34/30/30/29",
        "p257": "+11 blokov 1830/1831 (1×h22-1830 + 10×1831!) — šest-knjižne 16→23 (NAJVEČJI-SKOK!), bothEra-poročna 17→26, dvigi h54-37 (2. vseh časov!)/h56-36/h27-33/h11-32/h1-30/h26-28[~]/h33-28[~]/h3-27/h50-27 (PEZDIRC-NIT-42-let!)/h65-26 (bila-prva-hiša-1857!), h22-3.-zaporedno-leto-1830, h50-span-93 (3. mesto!)",
        "p259": "+N blokov 1833-nadaljevanje/1834 (s11–s13 — izpolni po integraciji!) — šest-knjižne 31→?, bothEra-poročna 34→?, dvigi h24-26?/h28-32?/h51-33?/h53-30?/h58-25?/h60-24?/h68-27?, 13-porok-6.-Febr-1833-NOVI-REKORD-korpusa, robno-številčenje-čez-mejo-leta (rob-1–18!), 5.-restart-1834!",
        "newModule": "src/data/atlas/parish-house-stories.ts (regeneriran p257_gen.py)",
        "ui": "HouseStoriesP254 v ParishTab (Matrike) + Notranjost01738Leto1829 (P256) + P257-kartice",
        "qa": "qa-p254 (živa rekalkulacija!) + qa-p255/256 + qa-p257 (251. kontrola!)",
        "verifier": "scripts/p254_house_stories.py --check + scripts/p256_1829.py + scripts/p257_1830_1831.py (I1–I10 + --live!)",
    },
}
json.dump(dokaz, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK JSON: {OUT_JSON}: houses={len(dokaz['houses'])}, six={len(six)}")
print("tiers:", {k: tiers[k] for k in range(6, 0, -1)}, "| bothEra:", bk, bm_, bp, "| span:", best_span, best_house)
