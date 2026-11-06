#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P197 — vstavi 13-GRIBLJE-blokov (04106, leto 1880) v parish.ts
PRED P196-sekcijo (newest-first vzorec: P196-pred-P195!)."""
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P196: mrliška PREDZGODOVINA 04106, leto 1881"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1880," not in src, "1880-bloki-že-obstajajo?!"

BLOCKS = [
    # (hišna, sken, zap, whatSi, whatEn)
    ("10", 164, 2,
     "umrla Anna HUORE [~Huoe/Thure-VLM], '¼ Götblwirthaftöngn' [~stan-glif], 50 LET (3. 1., pokop 5. 1.) — Asthma; previden (1); Franz Jančar 'coop.'; + ★★★ 1. GRIBLJE-VPIS-1880 (z1 = Krasinec-Karavanič!) + ★ h10-×2-1880 (z57-Kere-Sept!) + restart-63→1-tik-nad (rdeči-margini-KROP!) + [z2]",
     "died Anna HUORE [~Huoe/Thure-the-VLM], a '¼ Götblwirthaftöngn' [~the-glyph], 50 YEARS (Jan 3, buried Jan 5) — Asthma; previden (1); Franz Jančar 'coop.'; + ★★★ the-1st-GRIBLJE-ENTRY-1880 (z1 = Krasinec-Karavanič!) + ★ h10-×2-1880 (z57-Kere-Sept!) + the-restart-63→1-just-above (the-red-margins-KROP!) + [z2]"),
    ("8", 164, 3,
     "umrl Mich. KRIAN [~Kovian-VLM], 'Kinderstöfn' [~stan-glif], otrok, 2 LETA (6. 1., pokop 8. 1.) — Fraisen; previden (1); Franz Jančar 'coop.'; + ★ h8-nit (→ BRINC-1881-P196-z51!) + FRISELN-EPIDEMIJA-×28-1880 + [z3]",
     "died Mich. KRIAN [~Kovian-the-VLM], a 'Kinderstöfn' [~the-glyph], a child, 2 YEARS (Jan 6, buried Jan 8) — Fraisen; previden (1); Franz Jančar 'coop.'; + ★ the-h8-thread (→ BRINC-1881-P196-z51!) + the-FRISELN-EPIDEMIC-×28-1880 + [z3]"),
    ("21", 164, 4,
     "umrl Mathias NOVAK, '⅔-J.' [~½-stan-glif], 42 LET (10. 1., pokop 12. 1.) — Gehirnentzündung [~Gaßfranzüßt-VLM]; previden (1); Franz Jančar 'coop.'; + ★ h21-HOT-SPOT (→ 1881-×2-P196: Ožolt + Pögl + KROP-Zemelj-h21-s178!) + [z4]",
     "died Mathias NOVAK, a '⅔-J.' [~½-the-glyph], 42 YEARS (Jan 10, buried Jan 12) — Gehirnentzündung [~Gaßfranzüßt-the-VLM]; previden (1); Franz Jančar 'coop.'; + ★ the-h21-HOT-SPOT (→ 1881-×2-P196: Ožolt + Pögl + KROP-Zemelj-h21-s178!) + [z4]"),
    ("5", 165, 10,
     "umrla Katharina KNUEL [~Kuncelj-VLM — KROP: vas-'Griblje.'-JASNO, VLM-'Krive'-ZAVRJEN!], 'Abldbarmin ¼ gütshirtl.' [~stan-glif], 70 LET (16. 2., pokop 18. 2.) — Asthma; previden (1); Franz DOVGAN; + ★★★ Dovgan-GRIBLJE-IZJEMA-1880 (cf. 1881-izključno-ne-Griblje = vloga-vmes!) + h5-nov-dokaz + leto-glava-'1880-Feber'-nad (KROP: VLM-'1859'-ZAVRJEN!) + [z10]",
     "died Katharina KNUEL [~Kuncelj-the-VLM — KROP: the-vas-'Griblje.'-CLEAR, the-VLM-'Krive'-REJECTED!], an 'Abldbarmin ¼ gütshirtl.' [~the-glyph], 70 YEARS (Feb 16, buried Feb 18) — Asthma; previden (1); Franz DOVGAN; + ★★★ the-Dovgan-GRIBLJE-EXCEPTION-1880 (cf. 1881-exclusively-non-Griblje = an-in-between-role!) + h5-new-proof + the-'1880-Feber'-head-above (KROP: the-VLM-'1859'-REJECTED!) + [z10]"),
    ("39", 166, 19,
     "umrla Anna SIMEC [~Timec-VLM — KROP: 'S'-začetnica-jasna!], Vdova, 'koniriš(?)' [~stan-glif], 63 LET (26. 3., pokop 29. 3.) — Asthma; previden (1); Franc Jančar 'v. kaplan' (NASLOVNI-NARAŠČAJ: coop.-Jan → kaplan-März → VRD-Aug!); + ★★★ ŠIMEC/TIMEC-DVOJNICA-nit (→ z66-h18 + 1881-h18-TIMEC-P196!) + h39[~29]-3/9-KURRENT-zmeda-dokumentirana + [z19]",
     "died Anna SIMEC [~Timec-the-VLM — KROP: the-'S'-initial-CLEAR!], a widow, 'koniriš(?)' [~the-glyph], 63 YEARS (März 26, buried März 29) — Asthma; previden (1); Franc Jančar 'v. kaplan' (the-TITLE-ASCENT: coop.-Jan → kaplan-März → VRD-Aug!) + ★★★ the-ŠIMEC/TIMEC-TWIN-thread (→ z66-h18 + 1881-h18-TIMEC-P196!) + the-h39[~29]-3/9-KURRENT-confusion-documented + [z19]"),
    ("20", 166, 22,
     "umrl Fabian GRABRIAN [~Grabrijan], 'Sohn der Anna Grabrian vorehelich' [~stan], otrok, 3½ [~¾] LETA (3. 4., pokop 5. 4.) — Fraisen; previden (1); Franc Jančar 'v. kaplan'; + FRISELN-EPIDEMIJA-×28 (39%-vpisov!) + h20 (cf. P171-PEZDIREC-h20-04894!) + [z22]",
     "died Fabian GRABRIAN [~Grabrijan], 'the-son-of Anna Grabrian, illegitimate' [~the-status], a child, 3½ [~¾] YEARS (April 3, buried April 5) — Fraisen; previden (1); Franc Jančar 'v. kaplan'; + the-FRISELN-EPIDEMIC-×28 (39%-of-entries!) + h20 (cf. P171-PEZDIREC-h20-04894!) + [z22]"),
    ("47", 168, 52,
     "umrl Johann KLOBUČAR [~], 'Kindsmagd' [~stan-glif], otrok, 11 MESECEV (25. 8., pokop 27. 8.) — Frisen; previden (1); Franz Jančar 'v.R.D. Priester'; + ★ KLOBUČAR-priimek-nit (→ P193-1884-h44-veriga: Hlebučar-1883→Klobučar!) + h47-KROP-'47.'-JASNO + [z52]",
     "died Johann KLOBUČAR [~], a 'Kindsmagd' [~the-glyph], a child, 11 MONTHS (Aug 25, buried Aug 27) — Frisen; previden (1); Franz Jančar 'v.R.D. Priester'; + ★ the-KLOBUČAR-surname-thread (→ P193-1884-h44-chain: Hlebučar-1883→Klobučar!) + h47-KROP-'47.'-CLEAR + [z52]"),
    ("22", 169, 53,
     "umrl Georg MIHELIČ [~Mihel], 'apl. ¼ G.Bef.' [~stan], 17 LET (29. 8., pokop 31. 8.) — Krup [Frawsen-glifa]; previden (1); Franc Jančar 'Janežal'-glifa-'v.r.d.'; + '1880-August'-MESEC-GLAVA-V-VRSTICI (forma-dokaz!) + h22-nov-dokaz + [z53]",
     "died Georg MIHELIČ [~Mihel], 'apl. ¼ G.Bef.' [~the-status], 17 YEARS (Aug 29, buried Aug 31) — Krup [the-Frawsen-glyph]; previden (1); Franc Jančar the-'Janežal'-glyph-'v.r.d.'; + the-'1880-August'-MONTH-HEAD-IN-ROW (the-forma-proof!) + h22-new-proof + [z53]"),
    ("2", 169, 56,
     "umrla Ana KLEPEC, 'legit. Idochter' [~stan-glif], otrok, 4 MESECEV (3. 9., pokop 5. 9.) — Fraisen; previden (1); Franc Jančar 'v.r.d. Pastor'; + ★ h2-nit (→ HLEBEC-1881-P196-z89 → HLEBČAR-h48-DVOJNICA!) + ★★★ z55-PRESKOK-tik-pred (s169-rdeči-margini: 53,54,56..62 = 2.-številčna-anomalija-04106!) + 'September'-glava-v-vrstici + [z56]",
     "died Ana KLEPEC, a 'legit. Idochter' [~the-glyph], a child, 4 MONTHS (Sept 3, buried Sept 5) — Fraisen; previden (1); Franc Jančar 'v.r.d. Pastor'; + ★ the-h2-thread (→ HLEBEC-1881-P196-z89 → HLEBČAR-h48-TWIN!) + ★★★ the-z55-SKIP-just-before (s169-red-margins: 53,54,56..62 = the-2nd-numbering-anomaly-04106!) + the-'September'-head-in-row + [z56]"),
    ("10", 169, 57,
     "umrl Nicolaus (Miklavž) KERE [~], '¼ Fürstkind' [~stan-glif], otrok, 3 TEDNOV [~] (13. 9., pokop 17. 9.) — Kraisha [?Auszehrung-glif]; previden (1); Franc Jančar 'v.r.d. Priester'; + ★ h10-×2-1880 (z2-Huore-Jan!) + VLM-zap-shift-+1-popravljen (55-preskok!) + [z57]",
     "died Nicolaus (Miklavž) KERE [~], a '¼ Fürstkind' [~the-glyph], a child, 3 WEEKS [~] (Sept 13, buried Sept 17) — Kraisha [?Auszehrung-glyph]; previden (1); Franc Jančar 'v.r.d. Priester'; + ★ h10-×2-1880 (z2-Huore-Jan!) + the-VLM-zap-shift-+1-corrected (the-55-skip!) + [z57]"),
    ("42", 169, 58,
     "umrla Ana PEZDIRC [~Pozdirec], '¼ Götblück Kind' [~stan-glif], otrok, 2 MESECEV (15. 9., pokop 17. 9.) — Fraisen; previden (1); Franc Jančar 'v.r.d. Priest.'; + ★ PEZDIREC-nit (→ P195-1882-z1-Pozdire + P171-era-h20-04894!) + FRISELN-EPIDEMIJA + [z58]",
     "died Ana PEZDIRC [~Pozdirec], a '¼ Götblück Kind' [~the-glyph], a child, 2 MONTHS (Sept 15, buried Sept 17) — Fraisen; previden (1); Franc Jančar 'v.r.d. Priest.'; + ★ the-PEZDIREC-thread (→ P195-1882-z1-Pozdire + the-P171-era-h20-04894!) + the-FRISELN-EPIDEMIC + [z58]"),
    ("27", 170, 65,
     "umrl Jakob HUKAR, '¼ Gärtlser' [~Gärtner-stan-glif], 70 LET (9. 11., pokop 11. 11.) — Altersschwäche; previden (1); Fran Jančar 'WRD Priester'; + h27-nov-dokaz + leto-glava-'1880-Novobr'-nad (KROP: VLM-'1839'-ZAVRJEN!) + [z65]",
     "died Jakob HUKAR, a '¼ Gärtlser' [~Gärtner-the-glyph], 70 YEARS (Nov 9, buried Nov 11) — Altersschwäche; previden (1); Fran Jančar 'WRD Priester'; + h27-new-proof + the-'1880-Novobr'-head-above (KROP: the-VLM-'1839'-REJECTED!) + [z65]"),
    ("18", 170, 66,
     "umrla Anna SIMEC [~Simec], 'Kindsmagd' [~stan-glif], otrok, 1¾ LETA (KROP-POTRJENO: 1¾-ne-1½/1J-VLM!) (20. 11., pokop 21. 11.) — Fraisen; previden (1); Fran Jančar 'WRD Priester'; + ★★★ ŠIMEC/TIMEC-DVOJNICA-2/2 (z19-h39 + ta!) + h18 (→ 1881-TIMEC-P196!) + [z66]",
     "died Anna SIMEC [~Simec], a 'Kindsmagd' [~the-glyph], a child, 1¾ YEARS (KROP-PROVEN: 1¾-not-1½/1J-the-VLM!) (Nov 20, buried Nov 21) — Fraisen; previden (1); Fran Jančar 'WRD Priester'; + ★★★ the-ŠIMEC/TIMEC-TWIN-2/2 (z19-h39 + this-one!) + h18 (→ 1881-TIMEC-P196!) + [z66]"),
]

lines = []
lines.append("  // ——— P197: mrliška PREDZGODOVINA 04106, leto 1880 = 6. leto PREDZGODOVINSKE LINIJE (s164–s171 == Pag. 158–165, z1–z72 = 71 vpisanih vrstic z ★ z55-IZPUŠČENO-ŠTEVILKO!; pag == sken − 6, md5+vizualno-validirano! margini 158/159/163/164-KROP!) — 13 GRIBLJE-blokov / 12 hiš (h10-×2!) ———")
lines.append("  // ★★★ MEJA 1879/80 = s164 ('1 8'-L | '8 0'-R SPLIT-ČEZ-RAZPON = 36.-POTRDITEV-invariante + P194-tehnika-#9! restart-63→1-rdeči-margini: 62,63,1–7! 1879 = 63-vpisov!) + MEJA 1880/81 = s171-tail-'18/81' (P196-35.-reuse! konec-1880 = z72-Valčič-Vranoviče-h14-72J-Wassersucht-KROP!) + ★★★ z55-PRESKOK (s169-rdeči-margini: 53,54,56–62 — pisar-skip! cf. P196-z8-DUPLIKAT!) + ★★★ VLM-LETO-MISREAD-×2 ('1859'-s165/'1839'-s170 = KURRENT-8-zmeda — KROP: '1880 Feber' + '1880 Novobr'!) + FRISELN-EPIDEMIJA-×28 (39%! W-krivulja: 1880-×28 → 1881-×3 → 1882-×16!) + JANČAR-NASLOVNI-NARAŠČAJ (coop.→v.kaplan→VRD/WRD-Priester; GRIBLJE-12/13-92%!) + ŠIMEC/TIMEC-DVOJNICA-×2 + Dovgan-z10-GRIBLJE-IZJEMA + PEZDIREC-nit + KLOBUČAR-nit + MESEC-SREMBE-ULEDBA-#10 (z63-tail1879: smrt-31.12.→pokop-'Jänner 1'!) + dokaz research/issue17/parish-death-1880-04106.json (71-entries: 13-Griblje! 14-anomalij + 9-crossChecks + honesty-13 + lead-P198-1879!) + skripte: p197_fetch.py (md5!) + p197_read_page.mjs + p197_crop.mjs (10-cropov!) + p197_build_entries.py + p197_build_proof.py ———")
for hisna, sken, zap, wsi, wen in BLOCKS:
    lines.append("  {")
    lines.append(f'    houseNo: "{hisna}",')
    lines.append('    bookSignature: "04106",')
    lines.append("    year: 1880,")
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
print("year-1880-blokov:", out.count("year: 1880,"))
