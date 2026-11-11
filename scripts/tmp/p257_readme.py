#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P257 — README posodobitev (banner + korpus + tabela + Zadnje stanje + Odprto)."""
p = 'README.md'
s = open(p, encoding='utf-8').read()
applied = []

# 1) TOC
if '#zadnje-stanje-raziskave-po-p256--2026-11-11' in s:
    s = s.replace('- [Zadnje stanje raziskave](#zadnje-stanje-raziskave-po-p256--2026-11-11)',
                  '- [Zadnje stanje raziskave](#zadnje-stanje-raziskave-po-p257--2026-11-11)')
    applied.append('TOC')

# 2) banner pred P256
banner = (
    "> **11. november 2026 · po P257 · ★★★★★★ NOTRANJOST-01738: LETO 1830/1831 — 11 BLOKOV, 10 DVOGOV, ŠEST-KNJIŽNI-KLUB 16→23 (NAJVEČJI SKOK!)!** "
    "(1830: 8 vpisov (RESTART 12. Jänner + množični dan 17. Febr ×4 + METLIKA-140 + [~21.|26.] Juni + 30. Juni — druga polovica PRAZNA!) — "
    "edini korpusni vpis: m4 Anna MILEK, Griblje 22 = **3. ZAPOREDNO LETO nevest iz h22** (1828+1829+1830 — Miller ali Milek? [~X-OPEN]!) + BORŠT-20! · "
    "1831: **13 porok v 15 dneh** (26. 1.–9. 2.!) — ★★★★★★ **NIT PEZDIRC-h50: Georg PESDIRZ-h50-1831 s očetom MARCO PESDIRZ (črko-za-črko!) "
    "↔ Marcus PEGDIRE-h50-1873 (P251!) = ISTA DRUŽINA 42 LET (1831–1873!)** + m3/m13 nevesti [Pedierz?]/[Podierz?] — 4 vrstice družine! "
    "+ ★-ANOMALIJA-m7 ('ženin' MARIA Pödiz — žensko ime v ženinskem stolpcu — cf. MUZ-P255!) · "
    "★★★★★ **10 dvigov: h54 −37 = 2. NAJVEČJI VSEH ČASOV (za h22 −41!)** + h56 −36 · h27 −33 · h11 −32 · h1 −30 · h26 −28[~] · h33 −28[~] · h3 −27 · "
    "h50 −27 (span 93 = 3. mesto!) · **h65 −26 (BILA je prva hiša korpusa 1857!** — MILEK-h65-NIT 1831↔1874 = 43 let!) + KRIŽAN ×2 v m1 (ženin Peter h3 + mati neveste Dorothea!) · "
    "**šest-knjižni klub 16→23 (+7 — največji skok!) + bothEra-poročna 17→26** · korpus **2043** vitalov / 01738 = 31 · QA živo **251/251** · ~517/517 preverjanj!) · tsc 0 · lint 0 ·\n"
)
if banner.strip()[:60] not in s:
    s = s.replace('> **11. november 2026 · po P256 ·', banner + '> **11. november 2026 · po P256 ·', 1)
    applied.append('banner')

# 3) korpus-vrstica
i0 = s.find('**Korpus (po P256):**')
if i0 >= 0:
    i1 = s.find('\n\n', i0)
    old_k = s[i0:i1]
    new_k = (
        "**Korpus (po P257):** **2043 vitalov** · 502 krstna bloka 04105 (1887–1919) · **269 poročnih blokov 04455 (1886–1922 + predzgodovina 1873–1885 · P152 SINTEZA 592 vpisov)** · "
        "520 mrliških blokov 04894 (1886–1924) · **433 mrliških blokov 04106-predzgodovine (1857–1885 · 29 let, KONEC P220)** · "
        "**288 krstnih blokov 04104-predzgodovine (1871–1885 · 15 let, KONEC P235 + P236 sinteza: 1562 vpisov)** · "
        "**31 poročnih blokov 01738-predhodnika (1873-m1–m17 P253 + 1828 P255 + 1829 P256 + 1830/1831 P257 — korpus-prvi-vpis-1828!)** · "
        "**94 p80-hiš · 93 korpus hiš · P254: 100 hišnih oznak mreže (78 Griblje + 16 druga-vas + 6 neznan — 23 šest-knjiž-hiš po P257!)** — "
        "**P191: PT-luknja-18 ZAKLJUČENA analitično: 18/18 hiš (42–60 brez h41/h50) ima dokaze — 13/18 v vseh treh knjigah, najtanjša h51 (4 bloki, samo mrliška), pravih lukenj 0** — "
        "dokaz `research/issue17/pt-luknja-18-final.json` (po P257: vitals 2043 · 04455 269 = 74-predzgodovina + 195-linija-1:1 · "
        "01738 31 = 11-1873 + 3-1828 + 6-1829 + 1-1830 + 10-1831 (h3/h33/h50/h54/h56/h26/h27/h65/h1/h11!) · "
        "★★★★★ PEZDIRC-NIT-h50: Marco-Pesdirz-1831 ↔ Marcus-Pegdire-1873 = 42-let! · h65-firstYear-1857→1831 — BILA-prva-hiša-korpusa!) "
        "+ `research/issue17/parish-house-stories.json` (P257: 23-šest-knjižnih!)"
    )
    s = s[:i0] + new_k + s[i1:]
    applied.append('korpus')

# 4) tabela-vrstica 01738
old_row = '| Poročna PREDHODNIK 01738 | Matricula Online | **leto 1873 = m1–m17 (29. 1.–25. 5.) + ŠIV-MED-KNJIGAMA!**'
if old_row in s:
    i0 = s.find(old_row)
    i1 = s.find('\n', i0)
    new_row = (
        "| Poročna PREDHODNIK 01738 | Matricula Online | **leta 1873 + 1828 + 1829 + 1830/1831 (notranjost!) + ŠIV-MED-KNJIGAMA!** "
        "(P253 s140–s147 + P255 s1–s3 + P256 s4–s7 + P257 s6-r4–r11 + s7 — 31 blokov Griblje · "
        "★★★★★ PEZDIRC-NIT-h50: Marco-Pesdirz-1831 ↔ Marcus-Pegdire-1873 = 42-let! · KRIŽAN-h62-ŽENIN-1829 + HRIŽAN-h62-NEVESTA-1873 = ISTA hiša 44 let! · "
        "1831 = 13 porok v 15 dneh!) | ✅ P253 + P255 + P256 + P257 — NOTRANJOST 1828–1831 + ŠIV |"
    )
    s = s[:i0] + new_row + s[i1:]
    applied.append('tabela')

# 5) Zadnje stanje: naslov + nov vnos
s = s.replace('## Zadnje stanje raziskave (po P256 · 2026-11-11)', '## Zadnje stanje raziskave (po P257 · 2026-11-11)')
p257_entry = (
    "- **P257 (NOTRANJOST-01738: LETO 1830/1831!) ZAKLJUČENA** — P256-lead-①-naravna-pot: s6-r4–r11 (1830) + s7 (1831) = Pag. 9/11 "
    "(foliacija-'Pag-=-2·sken−3'-potrjena-×7!) — md5-dvojno (skupaj-4.-prenos-s-P256!) + **census-L/R-dvakrat-13/13-neodvisno!** + "
    "vrstični-trakovi-×21 + duel-valovi-×3-14-mikro-celic — **1830 (8-vpisov):** RESTART-12. Jänner + MNOŽIČNI-DAN-17. Febr-×4 (vzorec-3.-leto!) + "
    "METLIKA-140 (Möttling-1.-omemba!-[~140|110|40]) + [~21.|26.]-Juni-DUEL + 30. Juni + **1830-II-polovica-PRAZNA** (census-1:1!) + "
    "m2-Tschall-RECOVERED (manjkajoča-iz-pass-1!) + **m4-Anna-MILEK-GRIBLJE-22** (edini-korpusni-vpis!-3.-ZAPOREDNO-LETO-1828+1829+1830!-"
    "[~X-OPEN: Miller-ali-Milek?]) + m7-BORŠT-20 (2.-Boršt-hiša!) — **1831 (13-vpisov-V-15-DNEH!):** 26. Jän + 1. Febr + 9. Febr + d°-×10 + "
    "**m7-★-ANOMALIJA-VRSTICA ('ženin'-MARIA-Pödiz — ŽENSKO-IME-V-ŽENINSKEM-STOLPCU!-cf.-MUZ-P255!)** — "
    "**★★★★★★ NIT-PEZDIRC-h50 (NAJVEČJA-GENEALOŠKA-NIT-VSEH-FAZ!): Georg-PESDIRZ-h50-1831-s-očetom-MARCO-PESDIRZ "
    "(w2-črko-za-črko-'Pesdirz'!-duel-oče-1:1!) ↔ Marcus-PEGDIRE-h50-1873-P251-m20 = ISTA-DRUŽINA-42-LET (1831–1873!-ista-hiša-ista-imena!)** + "
    "m3/m13-nevesti-[Pedierz?]/[Podierz?] — 4-vrstice-družine! — **★★★★★ 11-BLOKOV-10-DVIGOV:** h54-37 (2.-VSEH-ČASOV-za-h22-41!) + h56-36 + h27-33 + "
    "h11-32 + h1-30 + h26-28[~26|20] + h33-28[~33|39] + h3-27 + h50-27 (span-93-3.!-POSTANE-pet-knjižna!) + **h65-26 (BILA-PRVA-HIŠA-KORPUSA-1857!**-"
    "MILEK-h65-NIT-1831↔1874-=-43-let!) + h22-3.-zaporedno-leto — **★★★★★ ŠEST-KNJIŽNI-KLUB-16→23 (+7 — NAJVEČJI-SKOK!) + bothEra-17→26 (+9)** + "
    "NITI: KRIŽAN-×2-m1 (ženin-h3-+-mati-Dorothea!) + MILEK-h65 + STARE-m5 + MUZ-oče-m12 + KAMBIC-m12-[13|15|18|20]-4-variant! + KLEPEC-[Klepz?]-m3 + "
    "[~Malezigk?-MALEŠIČ-kand.] — korpus-2032→**2043** · 01738-20→**31** — hišne-zgodbe-REGENERIRANE (p257_gen.py: SIX-×23 + tierji-23/41/12 + "
    "h1/h11/h26/h27/h33/h56/h65-nove-zgodbе!) — modul-PREDHODNIK_1830/1831-×16-izvozov + UI-Notranjost01738Leto1830_1831 + "
    "dokaza parish-marriage-notranjost-1830.json + -1831.json + skripta p257 (I1–I10) + qa-p257 (**251. kontrola!**) + "
    "**SANACIJA-NESREČE-2 (pisalne-skripte-baterije!)** + stari-števci-2032→2043-×157 — verifikacija: p257-24/24-s-LIVE (inventar-147-1:1!) + "
    "**BATERIJA-26/26-verifikatorjev-VSI-PASS (~517-preverjanj!)** + runQA-**251/251** + tsc-0 + lint-0 + browser-OK "
    "(P257-kartica-VIDNA-12/12-TRUE + 0-console-errors + mobilni-390-BREZ-prelivanja + footer-naravno!) — "
    "**P258+: ① meja-1831/32 (s8!) · ② paleografska-potrditev (Pesdirz-Podierz-Peterž + Ianigl-Muniz-Kranigh!) · ③ hišne-zgodbe-podrobneje — po uporabnikovi odločitvi**\n"
)
if '## P257 (NOTRANJOST-01738: LETO 1830/1831' not in s:
    s = s.replace('## Zadnje stanje raziskave (po P257 · 2026-11-11)\n',
                  '## Zadnje stanje raziskave (po P257 · 2026-11-11)\n' + p257_entry, 1)
    applied.append('zadnje-stanje')

# 6) Odprto: dodaj P257 med verige + zamenjaj P257+ z P258+
old_vega = '; nadaljevanje P255: **NOTRANJOST-1829 PREBRANA (P256!)** (20-vpisov + RESTART-1830 + 6-blokov/5-dvigov + KRIŽAN-h62-1829 = ISTA-hiša-kot-HRIŽAN-ŠIV-1873 + šest-knjižne-12→16 + h62-95/h20-93/h5-90!);'
new_vega = old_vega[:-1] + '; nadaljevanje P257: **NOTRANJOST-1830/1831 PREBRANA (P257!)** (8+13-vpisov + 11-blokov/10-dvigov + PEZDIRC-NIT-h50-42-let! + šest-knjižne-16→23 + bothEra-17→26!);'
if old_vega in s:
    s = s.replace(old_vega, new_vega, 1)
    applied.append('odprto-veriga')

old_p258 = 'naslednje možnosti (po izbiri uporabnika, P257+): **notranjost-1830/1831** (s6-r4–r11-1830 + s7-1831: 26. Jän + Grüble-3/50/56/65/1 — 6-korpusnih-hiš!) · **paleografska-potrditev** (issue #12: 13-garble-VASI + MALEŠIČ-×5 + ŠIMEK-×4 + m10-trojni-datum + 32|33/20|00-duela!) · **hišne-zgodbe-podrobneje** (posamezne hiše kot samostojne strani!)'
new_p258 = ('naslednje možnosti (po izbiri uporabnika, P258+): **meja-1831/32 (s8!)** (ali se notranjost nadaljuje v 1832+ — novih Grüble hiš? finis?) · '
            '**paleografska-potrditev** (issue #12: Pesdirz-Podierz-Peterž-DVOJMA + Ianigl-Muniz-Kranigh-3-variant + m12-hiša-[13|15|18|20]-4-variant + '
            'Salophig-Gerdschigh + 13-garble-VASI-1830!) · **hišne-zgodbe-podrobneje** (posamezne hiše kot samostojne strani!)')
if old_p258 in s:
    s = s.replace(old_p258, new_p258, 1)
    applied.append('odprto-p258')

open(p, 'w', encoding='utf-8').write(s)
print('README:', applied)
