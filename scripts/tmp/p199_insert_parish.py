#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P199 — vstavi 23-GRIBLJE-blokov (04106, leto 1878) v parish.ts
PRED P198-sekcijo (newest-first vzorec). 23 vpisov / 22 hiš (h30-×2!)."""
from pathlib import Path

TS = Path("/home/z/muzej/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P198: mrliška PREDZGODOVINA 04106, leto 1879"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1878," not in src, "1878-bloki-že-obstajajo?!"

BLOCKS = [
    # (hišna, sken, zap, whatSi, whatEn)
    ("18", 149, 1,
     "umrla Theresia INNEC? [~Innec/Konec-re-read — priimek-[?]!], '¼ Gütlersgattin?' [~stan-glif], 41 LET (5. 1., pokop 7. 1.) — Pljučnica? [~Auszehrung-re-read-varianca!]; previden (1); substituendus Kogoj/Kogej 'Corp.' (KROP-'Hoggaj'-grafia!); + ★★★ 1.-GRIBLJE-VPIS-1878 + ★★★ MEJA-1877/78 = s149: '18 78.'-SPLIT-VARIANTA-v-TA-celici (KROP-max-γ-7 — VLM-'1848'-4/7-ZAVRJEN!) = 38.-POTRDITEV-invariante + restart-1 + ★ h18-nit (1877-tail-s148-z4-Katharina-h18[?]! cf. 1881-h18-TIMEC-P196!) + [z1]",
     "died Theresia INNEC? [~Innec/Konec-re-read — surname-[?]!], '¼ Gütlersgattin?' [~the-glyph], 41 YEARS (Jan 5, buried Jan 7) — Pljučnica? [~Auszehrung-re-read-variant!]; previden (1); substituendus Kogoj/Kogej 'Corp.' (KROP-'Hoggaj'-grafia!); + ★★★ the-1st-GRIBLJE-ENTRY-1878 + ★★★ the-1877/78-BOUNDARY = s149: the-'18 78.'-SPLIT-VARIANT-inside-THIS-date-cell (KROP-max-γ-7 — VLM-'1848'-4/7-REJECTED!) = the-38th-INVARIANT-CONFIRMATION + restart-1 + ★ the-h18-thread (1877-tail-s148-z4-Katharina-h18[?]! cf. 1881-h18-TIMEC-P196!) + [z1]"),
    ("30", 149, 4,
     "umrl Mathias PEZDIRC [KROP-jasno!], 'sohn des Joh. u. Valburdua?/Mathias u. Theodita? Güttler' [~stan-partial], 6 LET [~KROP-'6 Jfr.'-grafia] (19. 1., pokop 20. 1. — KROP-z4-datum!) — Brustsucht? [~KROP-'Brunn?fuffun'-neberljivo]; previden (1); substituendus Kogoj/Kogej 'Corp.'; + ★★★ PEZDIRC-NIT-1878-#1 (h30-×2-1878: → z62-Markus-'Pezdir(e)'! cf. 1879-z58-Križan-h30 + PEZDIREC-era-P171!) + [z4]",
     "died Mathias PEZDIRC [KROP-CLEAR!], 'sohn des...' [~stan-partial], 6 YEARS [~KROP-'6 Jfr.'-grafia] (Jan 19, buried Jan 20 — KROP-z4-date!) — Brustsucht? [~KROP-unreadable]; previden (1); substituendus Kogoj/Kogej 'Corp.'; + ★★★ the-PEZDIRC-THREAD-1878-#1 (h30-×2-1878: → z62-Markus-'Pezdir(e)'! cf. 1879-z58-Križan-h30 + the-PEZDIREC-era-P171!) + [z4]"),
    ("10", 149, 9,
     "umrl Marcus KURE [~Hure-KROP-grafia], 47 LET (21. 2., pokop 23. 2.) — Asthma (KROP-jasno!); previden (1); substituendus Kogoj/Kogej 'Corp.'; + ★ h10-nit (cf. 1880-h10-×2: Huore-Jan + Kere-Sept-P197!) + zadnja-GRIBLJE-s149 + [z9]",
     "died Marcus KURE [~Hure-KROP-grafia], 47 YEARS (Feb 21, buried Feb 23) — Asthma (KROP-CLEAR!); previden (1); substituendus Kogoj/Kogej 'Corp.'; + ★ the-h10-thread (cf. 1880-h10-×2-P197!) + the-last-GRIBLJE-on-s149 + [z9]"),
    ("48", 150, 14,
     "umrl Johann KLOBUČAR, '¼ Gütler' (KROP-ime-crop-JASNO!), 35½ LET (KROP-'35½ J.' ✓) (11. 3., pokop 13. 3.) — Abzehrung (KROP ✓); previden (1); substituendus Kogej 'Corp.' (KROP-podpis-'Hogeju'!); + ★★★ KLOBUČAR-NIT-1878-h48 (cf. 1880-KLOBUČAR-h47-nit-P197 → 1884-veriga-P193!) + [z14]",
     "died Johann KLOBUČAR, '¼ Gütler' (KROP-name-crop-CLEAR!), 35½ YEARS (KROP-'35½ J.' ✓) (März 11, buried März 13) — Abzehrung (KROP ✓); previden (1); substituendus Kogej 'Corp.' (KROP-signature-'Hogeju'!); + ★★★ the-KLOBUČAR-THREAD-1878-h48 (cf. 1880-KLOBUČAR-h47-P197 → the-1884-chain-P193!) + [z14]"),
    ("66", 152, 31,
     "umrla Maria HRIZAN [~Križan! — VLM-'Horvat'-ZAVRJEN-KROP-ime-crop!], 'nepol. ½ J. — [Točken?] f: Johann u. Cath.' [~stan-partial], 8 LET (KROP-'8 J.' ✓) (7. 4., pokop 9. 4.) — Frisen (KROP-'Fraisan'-grafia ✓); previden (1); substituendus Kogeju 'coop.' (KROP-podpis! — VLM-'Fortin-aus-Kogelnik-Corp.'-ZAVRJEN!); + ★ HRIZAN/KRIŽAN-grafija-nit-1878-#1 (→ z70-Anna-Hrizan-h15! cf. 1879-z58-Križan!) + FRISELN-×10-1878 + [z31]",
     "died Maria HRIZAN [~Križan! — VLM-'Horvat'-REJECTED-KROP-name-crop!], 'nepol. ½ J. — [Točken?] f: Johann u. Cath.' [~stan-partial], 8 YEARS (KROP-'8 J.' ✓) (Apr 7, buried Apr 9) — Frisen (KROP-'Fraisan'-grafia ✓); previden (1); substituendus Kogeju 'coop.' (KROP-signature! — VLM-'Fortin-aus-Kogelnik-Corp.'-REJECTED!); + ★ the-HRIZAN/KRIŽAN-grafia-thread-1878-#1 (→ z70-Anna-Hrizan-h15! cf. 1879-z58-Križan!) + FRISELN-×10-1878 + [z31]"),
    ("55", 152, 32,
     "umrla Maria SIMEC, 'nepol. [¼/½?] J. — Točkan[?]' [~stan-partial], 1½ LET (KROP-stolpec-'1½ J.'-AVTORITATIVNO!) (9. 4., pokop 10. 4.) — Brustentzündung (KROP ✓); previden (1); substituendus Kogeju 'coop.' (KROP!); + ★ ŠIMEC-NIT-1878-#1 (→ z44-h38-Maria-Simec-87J-isti-mesec-čas! cf. 1879-z5-Peter-Šimec-h56 + 1881-h18-TIMEC!) + [z32]",
     "died Maria SIMEC, 'nepol. [¼/½?] J. — Točkan[?]' [~stan-partial], 1½ YEARS (KROP-column-'1½ J.'-AUTHORITATIVE!) (Apr 9, buried Apr 10) — Brustentzündung (KROP ✓); previden (1); substituendus Kogeju 'coop.' (KROP!); + ★ the-ŠIMEC-THREAD-1878-#1 (→ z44-h38-Maria-Simec-87J-same-month! cf. 1879-z5-Peter-Šimec-h56 + 1881-h18-TIMEC!) + [z32]"),
    ("9", 153, 34,
     "umrl Nicolaus JAKOFČIČ, 'nepol. ½ J. Sohn f: Johann u. Maria' (KROP-ime-crop! — VLM-'Natalia'-ZAVRJEN!), 2½ LET [~KROP-stolpec-'2½J.'-avtoritativno] (18. 4., pokop 20. 4.) — Friesen (KROP ✓); previden (1); Franz Dovgan (KROP-podpis!); + ★★★ JAKOFČIČ-nit-1878 (cf. z48-Georg-Jakofčič-isti-sken-okno + 1879-tail-z63-Nicol-Jakofčič!) + glava-'1878.'+'Aprìlis'-top (KROP — VLM-'1875'-5/7-ZAVRJEN!) + [z34]",
     "died Nicolaus JAKOFČIČ, 'nepol. ½ J. Sohn f: Johann u. Maria' (KROP-name-crop! — VLM-'Natalia'-REJECTED!), 2½ YEARS [~KROP-column-authoritative] (Apr 18, buried Apr 20) — Friesen (KROP ✓); previden (1); Franz Dovgan (KROP-signature!); + ★★★ the-JAKOFČIČ-thread-1878 (cf. z48-Georg-Jakofčič + 1879-tail-z63!) + the-'1878.'+'Aprìlis'-head-top (KROP — VLM-'1875'-5/7-REJECTED!) + [z34]"),
    ("3", 153, 38,
     "umrla M[ar]___ Ana P. [?KURRENT-raw-'NrtffyabhanfAna P.' — kripto-ime!], 'Wwe./v. Math. Brinec[?]; ¼ G.[?]-nota' [~stan-glif], 54 LET (KROP-'54 J.' ✓✓) (21. 4., pokop 23. 4.) — Asthma (KROP ✓✓); previden (1); Franz Dovgan (KROP!); + ★ BRINC/PRINC-nit-1878 (cf. P197-ŠIMEC/TIMEC-dvojnica-vzorec!) + Griblje-Asthma-×3-1878 (z9/z38/z73!) + [z38]",
     "died M[ar]___ Ana P. [?KURRENT-raw-'NrtffyabhanfAna P.' — crypto-name!], 'Wwe./v. Math. Brinec[?]; ¼ G.[?]-nota' [~the-glyph], 54 YEARS (KROP-'54 J.' ✓✓) (Apr 21, buried Apr 23) — Asthma (KROP ✓✓); previden (1); Franz Dovgan (KROP!); + ★ the-BRINC/PRINC-thread-1878 (cf. P197-ŠIMEC/TIMEC-twin-pattern!) + Griblje-Asthma-×3-1878 (z9/z38/z73!) + [z38]"),
    ("54", 153, 39,
     "umrla Anna P[ar/g]___rb? [?KURRENT; VLM-'Maria[?]'-nerazrešeno!], '¼ G.'-nota [~], ★ STAROST-NI-VPISANA — tilda-'~' (KROP-desni-ALL-crop!) (23. 4., pokop 26. 4.) — Abzehrung (KROP — VLM-'Tizanica[?]'-ZAVRJEN!); previden (1); substituendus Kogeju 'coop.' (KROP!); + ★★★ 2.-PRAZNA-STAROST-04106 (cf. 1879-z47-Nelly?-h20-pusta-vrstica!) + [z39]",
     "died Anna P[ar/g]___rb? [?KURRENT; VLM-'Maria[?]'-unresolved!], '¼ G.'-nota [~], ★ AGE-NOT-ENTERED — the-tilde-'~' (KROP-desni-ALL-crop!) (Apr 23, buried Apr 26) — Abzehrung (KROP — VLM-'Tizanica[?]'-REJECTED!); previden (1); substituendus Kogeju 'coop.' (KROP!); + ★★★ the-2nd-EMPTY-AGE-04106 (cf. 1879-z47-Nelly?-h20-empty-row!) + [z39]"),
    ("16", 153, 41,
     "umrl Johann JILAK [~Ilak/Jelak], 'Sohn f: Jacob u. Mathia' (KROP!), 2 LETI (KROP-'2 J.' ✓) (1. 5., pokop 2. 5. — glava-'Mai'!) — Marbmil (KROP ✓); previden (1); substituendus Kogeju 'coop.' (KROP!); + ★ h16-DVOJNA-IDENTIFIKACIJA-1878 (cf. z28-'Begunja-vas-pri-Gribljah'-h16-Ludmila-Horvat-isti-sken-okno!) + [z41]",
     "died Johann JILAK [~Ilak/Jelak], 'Sohn f: Jacob u. Mathia' (KROP!), 2 YEARS (KROP-'2 J.' ✓) (Mai 1, buried Mai 2 — the-'Mai'-head!) — Marbmil (KROP ✓); previden (1); substituendus Kogeju 'coop.' (KROP!); + ★ the-h16-DUAL-IDENTIFICATION-1878 (cf. z28-'Begunja-vas-pri-Gribljah'-h16-same-window!) + [z41]"),
    ("40", 153, 42,
     "umrl Johann POZDRIN? [~PEZDIRC-grafija? — VLM-'Pozdrin[?]'], 3 LETA (KROP-'3 J.' ✓) (2. 5., pokop 4. 5.) — Brustentzündung (KROP ✓); previden (1); Franz Dovgan (KROP!); + ★★★ h40-NIT-1878 (→ 1879-z28-Mathias-Peglic-97J-★★★ KORPUS-REKORD — h40-v-2-letih!) + PEZDIR/PEGLIC-grafija-nit-1878-#2 + [z42]",
     "died Johann POZDRIN? [~PEZDIRC-grafija? — VLM-'Pozdrin[?]'], 3 YEARS (KROP-'3 J.' ✓) (Mai 2, buried Mai 4) — Brustentzündung (KROP ✓); previden (1); Franz Dovgan (KROP!); + ★★★ the-h40-THREAD-1878 (→ 1879-z28-Mathias-Peglic-97J-★★★ CORPUS-RECORD — h40-in-2-years!) + the-PEZDIR/PEGLIC-grafia-thread-1878-#2 + [z42]"),
    ("47", 153, 43,
     "umrl Johann HROVAT (KROP ✓), 56 LET (KROP-'56 J.' ✓) (3. 5., pokop 4. 5.) — Lungenentzündung (KROP ✓); previden (1); Franz Dovgan (KROP!); + ★ h47-nov-dokaz-1878 (h47 = KLOBUČAR-nit-hiša-P197-1880 → 1884-veriga — h47/h48-sosednji-Klobučar-čas!) + [z43]",
     "died Johann HROVAT (KROP ✓), 56 YEARS (KROP-'56 J.' ✓) (Mai 3, buried Mai 4) — Lungenentzündung (KROP ✓); previden (1); Franz Dovgan (KROP!); + ★ h47-new-proof-1878 (h47 = the-KLOBUČAR-thread-house-P197-1880 → 1884-chain — h47/h48-adjacent-Klobučar-time!) + [z43]"),
    ("38", 154, 44,
     "umrla Maria SIMEC, 'nepol. Gütlers-tochter f: Georg u. Anna' (KROP-ime-crop!), 87 LET (KROP-'87 J.' ✓✓ — desni-ALL-crop!) (5. 5., pokop 6. 5.) — Lungenentzündung [~ + 2.-vrstica-'-irny?'[?]-nerazrešena; VLM-'Altersmarbmil'-ZAVRJEN!]; previden (1); Franz Dovgan (KROP-podpis!); + ★★★ GRIBLJE-87-LET-#1-1878 (×2-z-tail-z83-Peglavc! cf. 1879-korpus-rekord-97J!) + ★ ŠIMEC-NIT-×2-1878 (z32-h55-isti-mesec!) + [z44]",
     "died Maria SIMEC, 'nepol. Gütlers-tochter f: Georg u. Anna' (KROP-name-crop!), 87 YEARS (KROP-'87 J.' ✓✓ — the-ALL-crop!) (Mai 5, buried Mai 6) — Lungenentzündung [~ + 2nd-line-'-irny?'[?]-unresolved; VLM-'Altersmarbmil'-REJECTED!]; previden (1); Franz Dovgan (KROP-signature!); + ★★★ GRIBLJE-87-YEARS-#1-1878 (×2-with-tail-z83-Peglavc! cf. 1879-corpus-record-97J!) + ★ the-ŠIMEC-THREAD-×2-1878 (z32-h55-same-month!) + [z44]"),
    ("1", 154, 46,
     "umrla Anna ZELKO (KROP-ime-crop!), '¼ Gütlerswirth[?]' [~stan-glif], 34 LET (KROP-'34 J.' ✓✓) (6. 5., pokop 7. 5.) — In Entbindung (KROP-2-vrstici! VLM-'In kindbett gestor'-SEMANTIČNO-SOGLASJE — porodna-smrt!); previden (1); Franz Dovgan (KROP!); + ★★★ ZELIHA-NIT-h1-×3-v-2-LETIH (→ 1879-z6-Anna-Zeliha-74J + z10-Anna-Zeliho-¾J! cf. ZELŠKO-h1-×2-1882!) + [z46]",
     "died Anna ZELKO (KROP-name-crop!), '¼ Gütlerswirth[?]' [~the-glyph], 34 YEARS (KROP-'34 J.' ✓✓) (Mai 6, buried Mai 7) — In Entbindung (KROP-2-lines! VLM-'In kindbett gestor'-SEMANTIC-AGREEMENT — a-childbirth-death!); previden (1); Franz Dovgan (KROP!); + ★★★ the-ZELIHA-THREAD-h1-×3-in-2-YEARS (→ 1879-z6-Anna-Zeliha-74J + z10-Anna-Zeliho-¾J! cf. ZELŠKO-h1-×2-1882!) + [z46]"),
    ("14", 155, 55,
     "umrla Barbara VEZDIRZ? [~PEZDIR-grafija! — VLM-'Pegelj[?]'-ZAVRJEN], 'nepol. Gutfrau[?]' [~stan-glif], 10 MESECEV (KROP ✓) (26. 6., pokop 28. 6.) — Krastelj (KROP-'Chrzfa'-grafia[~]); previden (1); Franz Jančar coop [~partial-KROP]; + ★ PEZDIR-GRAFIJA-NIT-1878-#3 (→ z60-h20 + z62-h30!) + glava-'1878.'+'Juni'-v-z54-celici (KROP!) + [z55]",
     "died Barbara VEZDIRZ? [~PEZDIR-grafia! — VLM-'Pegelj[?]'-REJECTED], 'nepol. Gutfrau[?]' [~the-glyph], 10 MONTHS (KROP ✓) (June 26, buried June 28) — Krastelj (KROP-'Chrzfa'-grafia[~]); previden (1); Franz Jančar coop [~partial-KROP]; + ★ the-PEZDIR-GRAFIA-THREAD-1878-#3 (→ z60-h20 + z62-h30!) + the-'1878.'+'Juni'-head-in-z54-cell (KROP!) + [z55]"),
    ("33", 155, 56,
     "umrl Johann DEBEVC [~Debevec/Debliv-KROP], 'nepol. Sohn [+½G?-nota]', 37 LET [~KROP-'3[7] J.' — 7-v-cut; VLM-soglasje!] (29. 6., pokop 1. 7.) — Abzehrung (KROP ✓); previden (1); Franz Jančar coop (KROP-podpis-JASNO!) — ★★★ JANČAR-NA-GRIBLJU-1878-#1 + ★★★ ULEDBA-#10-7.-INSTANCE (smrt-'29'-Juni → pokop-'1.'-'Juli'-header-v-vrstici — KROP-levi-strip! cf. 1879-z28-DUP + z63!) + [z56]",
     "died Johann DEBEVC [~Debevec/Debliv-KROP], 'nepol. Sohn [+½G?-nota]', 37 YEARS [~KROP-'3[7] J.' — 7-cut; VLM-agrees!] (June 29, buried July 1) — Abzehrung (KROP ✓); previden (1); Franz Jančar coop (KROP-signature-CLEAR!) — ★★★ JANČAR-ON-GRIBLJE-1878-#1 + ★★★ the-FINDING-#10-7th-INSTANCE (death-'29'-June → burial-'1.'-'Juli'-head-in-row — KROP-left-strip! cf. 1879-z28-DUP + z63!) + [z56]"),
    ("20", 155, 60,
     "umrla Katharina VEZDIRZ? [~PEZDIR-grafija! — VLM-'Pegelj[?]'-ZAVRJEN], 10 MESECEV (KROP-'10 Monate' ✓✓ — re-aligned!) (12. 8., pokop 14. 8. — glava-'August'!) — Masern (KROP ✓✓); previden (1); Franz Jančar coop (KROP-JASNO!) — ★★★ JANČAR-NA-GRIBLJU-1878-#2 + ★★★ h20-PEZDIRC-era-1878 (→ 1879-×2: z28-DUP-Pezdirc + z47-Nelly?-cf-P171!) + ★★★ MASERN-×2-ADJACENT-1/2 (z61-naslednja!) + [z60]",
     "died Katharina VEZDIRZ? [~PEZDIR-grafia! — VLM-'Pegelj[?]'-REJECTED], 10 MONTHS (KROP-'10 Monate' ✓✓ — re-aligned!) (Aug 12, buried Aug 14 — the-'August'-head!) — Masern (KROP ✓✓); previden (1); Franz Jančar coop (KROP-CLEAR!) — ★★★ JANČAR-ON-GRIBLJE-1878-#2 + ★★★ h20-the-PEZDIRC-era-1878 (→ 1879-×2: z28-DUP-Pezdirc + z47-Nelly?-cf-P171!) + ★★★ MASERN-×2-ADJACENT-1/2 (z61-next!) + [z60]"),
    ("30", 155, 62,
     "umrl Markus PEZDIR(E)? [?PEZDIR-grafija! — VLM-'Pegelj[?]'-ZAVRJEN], 35 LET [~KROP-3/5-zmeda-'55?'; VLM-soglasje] (16. 8., pokop 18. 8.) — Cholik (KROP ✓); previden (1); Franz Dovgan (KROP!); + ★★★ h30-×2-1878-2/2 (z4-Mathias-Pezdirc-Jänner!) + PEZDIR-GRAFIJA-NIT-#5 + [z62]",
     "died Markus PEZDIR(E)? [?PEZDIR-grafia! — VLM-'Pegelj[?]'-REJECTED], 35 YEARS [~KROP-3/5-confusion-'55?'; VLM-agrees] (Aug 16, buried Aug 18) — Cholik (KROP ✓); previden (1); Franz Dovgan (KROP!); + ★★★ h30-×2-1878-2/2 (z4-Mathias-Pezdirc-January!) + the-PEZDIR-GRAFIA-THREAD-#5 + [z62]"),
    ("15", 156, 70,
     "umrla Anna HRIZAN [~Križan! — VLM-'Muc'-ZAVRJEN-KROP-ime-crop!], 'nepol. ¼ J.[?]' [~stan-glif], 5 LET (KROP-'5 J.' ✓) (23. 10., pokop 25. 10.) — Fraisen (KROP ✓); previden (1); Franz Jančar coop (KROP-JASNO!) — ★★★ JANČAR-NA-GRIBLJU-1878-#3 + ★ HRIZAN/KRIŽAN-grafija-nit-#2 (z31-Maria-h66!) + [z70]",
     "died Anna HRIZAN [~Križan! — VLM-'Muc'-REJECTED-KROP-name-crop!], 'nepol. ¼ J.[?]' [~the-glyph], 5 YEARS (KROP-'5 J.' ✓) (Oct 23, buried Oct 25) — Fraisen (KROP ✓); previden (1); Franz Jančar coop (KROP-CLEAR!) — ★★★ JANČAR-ON-GRIBLJE-1878-#3 + ★ the-HRIZAN/KRIŽAN-grafia-thread-#2 (z31-Maria-h66!) + [z70]"),
    ("37", 157, 73,
     "umrl Johann PERHAR? [~Kosler?-re-read — priimek-[?]!], 41 LET (KROP-'41 J.' ✓) (1. 11., pokop 2. 11.) — Asthma (KROP ✓✓); previden (1); Franz Jančar coop (KROP-podpis!) — ★★★ JANČAR-NA-GRIBLJU-1878-#4 + 1.-GRIBLJE-s157 + glava-'1878.'+'Nov.'-top (KROP — 2-seji!) + ordinali-73–82-KROP-×2-seji (VLM-'63–72'-7→6-3.×!) + Griblje-Asthma-×3-1878-3/3 + [z73]",
     "died Johann PERHAR? [~Kosler?-re-read — surname-[?]!], 41 YEARS (KROP-'41 J.' ✓) (Nov 1, buried Nov 2) — Asthma (KROP ✓✓); previden (1); Franz Jančar coop (KROP-signature!) — ★★★ JANČAR-ON-GRIBLJE-1878-#4 + the-1st-GRIBLJE-on-s157 + the-'1878.'+'Nov.'-head-top (KROP — 2-reads!) + ordinals-73–82-KROP-×2-reads (VLM-'63–72'-7→6-3rd-time!) + Griblje-Asthma-×3-1878-3/3 + [z73]"),
    ("44", 157, 77,
     "umrl Mathias PECOLAR? [?PEZDIR/Peglic-grafija — VLM-'Pecolar[?]'], 44 LET (KROP-'44 Jahre' ✓✓) (8. 11., pokop 10. 11.) — Zagfuß? [?KROP-'Zagfus/Zapfus'-neberljivo; VLM-'Hustend[?]'-ZAVRJEN]; previden (1); Franz Jančar coop (KROP!) — ★★★ JANČAR-NA-GRIBLJU-1878-#5 + ★★★ h44-NIT-1878 (→ 1879-z27-Maria-Peglic-37J-GEHIRNENTZÜNDUNG-katastrofa-tik-pred-rekordom!) + PEZDIR/PEGLIC-grafija-#6 + [z77]",
     "died Mathias PECOLAR? [?PEZDIR/Peglic-grafia — VLM-'Pecolar[?]'], 44 YEARS (KROP-'44 Jahre' ✓✓) (Nov 8, buried Nov 10) — Zagfuß? [?KROP-unreadable; VLM-'Hustend[?]'-REJECTED]; previden (1); Franz Jančar coop (KROP!) — ★★★ JANČAR-ON-GRIBLJE-1878-#5 + ★★★ the-h44-THREAD-1878 (→ 1879-z27-Maria-Peglic-37J-GEHIRNENTZÜNDUNG-catastrophe-just-before-the-record!) + the-PEZDIR/PEGLIC-grafia-#6 + [z77]"),
    ("57", 157, 80,
     "umrla Maria LOGAR, 'nepol. Gütlersfrau' (KROP-ime-crop-JASNO!), 17 LET (KROP-'17 J.'-γ-7-jasno! — VLM-'17?/37?'-REŠENO!) (15. 11., pokop 16. 11.) — Gehirnentzündung [~KROP-'G___ntzündung'-grafia]; previden (1); Franz Dovgan (KROP!); + ★★★ GEHIRNENTZÜNDUNG-NIT-1878-#3 (→ 1879-×2-istega-dna-z27/z28-Peglic-katastrofa = NIT-×5-1878/79!) + ★ h57-nov-dokaz + hišna-KROP-'57'-γ-7 (VLM-'51[?]'-'ZAVRJEN!) + [z80]",
     "died Maria LOGAR, 'nepol. Gütlersfrau' (KROP-name-crop-CLEAR!), 17 YEARS (KROP-'17 J.'-γ-7-clear! — VLM-'17?/37?'-RESOLVED!) (Nov 15, buried Nov 16) — Gehirnentzündung [~KROP-'G___ntzündung'-grafia]; previden (1); Franz Dovgan (KROP!); + ★★★ the-GEHIRNENTZÜNDUNG-THREAD-1878-#3 (→ 1879-×2-same-day-z27/z28-Peglic-catastrophe = the-THREAD-×5-1878/79!) + ★ h57-new-proof + house-KROP-'57'-γ-7 (VLM-'51[?]'-REJECTED!) + [z80]"),
    ("53", 158, 83,
     "umrl Mathias PEGLAVC? [~Marthe-re-read; P198-KROP-crop-'Mathias'-jasno! — priimek-[?]!], 87 LET [~17-re-read; P198-KROP-crop-'87 J.'-jasno!] (1. 11., pokop 2. 11.) — Wassersucht[?]; previden (1); Franz Jančar coop (TA-SEJA-KROP-podpis-'Franz Jančar coop'-JASNO!) — ★★★ JANČAR-NA-GRIBLJU-1878-#6 + ★★★ GRIBLJE-87-LET-#2-1878 (z44-Simec!) + 1878-TAIL-1/3 (ordinali-83–85: P198-KROP + RE-READ-SOGLASJE-2-viri!) + ★ h53-nit (→ 1879-z15-Peter-Bežek?-½J!) + MEJA-'Incipit-annus'+'1 8|7 9'-SPLIT-TIK-POD (P198-37.-potrditev-reuse!) + [z83]",
     "died Mathias PEGLAVC? [~Marthe-re-read; P198-KROP-crop-'Mathias'-CLEAR! — surname-[?]!], 87 YEARS [~17-re-read; P198-KROP-crop-'87 J.'-CLEAR!] (Nov 1, buried Nov 2) — Wassersucht[?]; previden (1); Franz Jančar coop (THIS-SESSION-KROP-signature-'Franz Jančar coop'-CLEAR!) — ★★★ JANČAR-ON-GRIBLJE-1878-#6 + ★★★ GRIBLJE-87-YEARS-#2-1878 (z44-Simec!) + the-1878-TAIL-1/3 (ordinals-83–85: P198-KROP + RE-READ-AGREEMENT-2-sources!) + ★ the-h53-thread (→ 1879-z15-Peter-Bežek?-½J!) + the-'Incipit-annus'+'1 8|7 9'-SPLIT-JUST-BELOW (the-P198-37th-confirmation-reuse!) + [z83]"),
]

lines = []
lines.append("  // ——— P199: mrliška PREDZGODOVINA 04106, leto 1878 = 8. leto PREDZGODOVINSKE LINIJE (s148–s158 == Pag. 142–152, z1–z85 = 85 vpisov == P197-'restart-85→1' + P198-'1878 ≈ 85'-EXAKT!; pag == sken − 6, md5-križna-validacija-verige-P197→P198→P199!) — 23 GRIBLJE-blokov / 22 hiš (h30-×2!) ———")
lines.append("  // ★★★ MEJA 1877/78 = s149 ('18 78.'-SPLIT-VARIANTA-v-z1-datuma-celici = 38.-POTRDITEV-invariante! restart-1; s148-1877-tail-z-ORDINALI-NEVIDNIMI — P200-lead!) + MEJA 1878/79 = s158-mid (P198-37.-reuse! konec-1878 = z85-tail) + ★ ORDINALNO-ČISTO-LETO (85/85 — kontrast-3-anomalijam-1879/80/81!; s156-z72-KROP-γ-7 — VLM-'62'-7→6-3.×!) + ★★★ DUHOVNIKI-TRANZICIJA-V-REALNEM-ČASU: Dovgan-dominanta + Kogej-subst.-coop-na-Griblju-×8 (Jänner–April; VLM-'Fortin-aus-Kogelnik'-ZAVRJEN-KROP!) → Jančar-coop-od-junija (Griblje-×6!) = ★★★ JANČAR-NIT-1878→1883 = 6-LET (P198-'5-let'-razširjena!) + ★★★ 'Ukolk'[?]-NEZNANA-VAS-×5 (cf. P195-'Wolk'-1882!) + ★★★ MASERN-×2-ADJACENT (z60+z61 — KROP-identična-grafia; VLM-'Fraisen'-ZAVRJEN!) + FRISELN+MASERN-×12 (W-krivulja-5-točkovna: 12→14→28→3→16!) + ★★★ PEZDIR/PEZDIRC-GRAFIJA-NIT-×6 (z4-h30 + z42-h40 + z55-h14 + z60-h20 + z62-h30 + z77-h44 — 1-LETO-PRED-P198-katastrofo!) + ZELIHA-NIT-h1-×3-v-2-letih (z46!) + ŠIMEC-NIT-×2-1878 (z32-h55 + z44-h38-87J!) + KLOBUČAR-NIT-h48 (z14!) + ULEDBA-#10-7.-instance (z56: 29-Juni→1-Juli!) + GEHIRNENTZÜNDUNG-×3-1878 (z80-h57-17J!) = NIT-×5-1878/79 + VLM-leto-misread-×3-KROP ('1848'/'1858'/'1875'→'1878'!) + PRINTED-146–150-×5-vizualno + 2×-87-LET-GRIBLJE (z44-Simec + z83-Peglavc-P198-KROP!) + dokaz research/issue17/parish-death-1878-04106.json (85-entries: 23-Griblje! 13-anomalij + 10-crossChecks + honesty-16 + lead-P200-1877!) + skripte: p199_fetch.py + p199_read_page.mjs + p199_crop.py + p199_build_entries.py + p199_build_proof.py ———")
for hisna, sken, zap, wsi, wen in BLOCKS:
    lines.append("  {")
    lines.append(f'    houseNo: "{hisna}",')
    lines.append('    bookSignature: "04106",')
    lines.append("    year: 1878,")
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
print("year-1878-blokov:", out.count("year: 1878,"))
