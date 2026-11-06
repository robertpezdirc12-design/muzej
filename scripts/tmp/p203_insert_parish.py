#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P203 — vstavi 21-GRIBLJE-blokov (04106, leto 1874) v parish.ts PRED P202-sekcijo."""
from pathlib import Path

TS = Path("/home/z/my-project/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P202: mrliška PREDZGODOVINA 04106, leto 1875"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1874," not in src, "1874-bloki-že-obstajajo?!"

B = [
    ("11", 119, 2, "umrla Katharina LUNIČ[?], 'ledinske-hči[?]', 16 DNI (Jänner 9., pokop 11.) — Frisen[?]; + ★★★ h11-KUNIĆ-hiša-NIT (→ 1875-z71-KUNIĆ-65J — ime-Katharina-×2!) + 1.-GRIBLJE-1874-samo-2-vrstici-pod-'18 74. Jänner'-glavo! + [z2]",
     "died Katharina LUNIČ[?], 16 DAYS (Jän 9, buried 11) — Frisen[?]; + ★★★ the-h11-KUNIĆ-house-THREAD (→ 1875-z71 — the-name-Katharina-×2!) + the-1st-GRIBLJE-1874-just-2-rows-below-the-'18 74. Jänner'-head! + [z2]"),
    ("24", 120, 6, "umrla Maria BRIME, 'ofd.'[?], 9 LET [~] (Feber 21., pokop 23. — KROP-VLM-'20'-misread!) — bolezen-[?]; + ★ BRIME-1/2-×2-v-5-TEDNIH (→ z13-h28-62J!) + otrok + [z6]",
     "died Maria BRIME, 9 YEARS [~] (Feb 21, buried 23 — KROP-the-VLM-'20'-misread!) — [?]; + ★ the-BRIME-1/2-×2-IN-5-WEEKS (→ z13-h28!) + the-child + [z6]"),
    ("28", 120, 13, "umrla Maria BRIME, 'nšl./praD. ofd.'[?], 62 LET (März 28., pokop 29.) — [?]; + ★★★ BRIME-2/2 (→ z6-h24-9J — 2-MARIJE-2-HIŠI-v-5-TEDNIH!) + [z13]",
     "died Maria BRIME, 62 YEARS (März 28, buried 29) — [?]; + ★★★ the-BRIME-2/2 (→ z6-h24-9J — 2-MARIAS-2-HOUSES-IN-5-WEEKS!) + [z13]"),
    ("69", 121, 15, "umrl Mathias BRINC, ½ LETO (April 9., pokop 11.) — [?]; + ★★★ h69-1/2-1874 (→ z51-BRUNE-Nov! → P202-h69-HUSIC-1875!) + otrok + [z15]",
     "died Mathias BRINC, ½ YEAR (Apr 9, buried 11) — [?]; + ★★★ the-h69-1/2-1874 (→ z51-BRUNE! → P202-h69-HUSIC-1875!) + the-child + [z15]"),
    ("55", 121, 23, "umrl Michael GUREJEŠIČ[?], 60 J. (April 30., pokop Mai-1. — ULEDBA-vzorec!) — [?]; + h55-nov-dokaz + [z23]",
     "died Michael GUREJEŠIČ[?], 60 Y. (Apr 30, buried Mai-1 — the-ULEDBA-pattern!) — [?]; + the-h55-new-proof + [z23]"),
    ("64", 122, 37, "umrla Milo VEBČAR[?Vabčar?], 8½ (TEDNOV?[~]) (Mai 25., pokop 27.) — [?]; + ★ h64-1/2-1874 (→ z75-JAVORNIK-Sept! cf. P201-h64-Kerbica-1876!) + otrok-[?] + [z37]",
     "died Milo VEBČAR[?], 8½ (WEEKS?[~]) (Mai 25, buried 27) — [?]; + ★ the-h64-1/2-1874 (→ z75! cf. P201-h64!) + the-child-[?] + [z37]"),
    ("72", 122, 39, "MRTVOROJEN otrok [★★★ Todtgeborenes!] des-[★★★ OČET-NESOGLASJE: 'Marcus-KRAJNC[?]'-VLM-vs-'Anton-JANEC[?]'-KROP-glif-za-glifom-[?]!] (Mai 26., pokop 27.) — mrtvorojen; + ★★★ h72-1/2-1874 (→ z71-MALENŠIČ-Sept! → P202-z40-BRAUŠ-1875!) + [z39]",
     "STILLBORN the-child [★★★ Todtgeborenes!] of-[★★★ the-FATHER-DISAGREEMENT: 'Marcus-KRAJNC[?]'-VLM-vs-'Anton-JANEC[?]'-KROP-[?]!] (Mai 26, buried 27) — stillborn; + ★★★ the-h72-1/2-1874 (→ z71! → P202-z40-BRAUŠ!) + [z39]"),
    ("86", 122, 40, "umrl Johann [?], 1½ J. (Mai 27., pokop 29.) — [?]; + ★ h86[?]-dvom-hišne-št. + otrok + [z40]",
     "died Johann [?], 1½ Y. (Mai 27, buried 29) — [?]; + ★ the-h86[?]-house-number-doubt + the-child + [z40]"),
    ("39", 124, 46, "umrl Mathias TILAK[?Silak], '½-Gabrielsova[?]-stan', 1 LETO (Juni 3., pokop 4.) — Halborn [★★★ KROP-slika-'Griblje-39.'-'Mathias-Tilak-½-Gabrielsova'! s123==s124-DVOSCAN-KROP-×2-soglasje! h39-NE-h34!]; + ★★★ h39-NOVA-hiša + Halborn-bolezen + otrok + [z46]",
     "died Mathias TILAK[?Silak], '½-Gabrielsova[?]', 1 YEAR (Juni 3, buried 4) — Halborn [★★★ the-KROP-image-'39.'! the-s123==s124-DOUBLE-SCAN-KROP-×2-agreement! h39-NOT-h34!]; + ★★★ h39-NEW-HOUSE + the-Halborn + the-child + [z46]"),
    ("69", 124, 51, "umrl Joannes BRUNE [★★★ KROP-'Griblje-69.-Joannes-Brune'-jasno!], 69 [★★★ KROP-'6g-jasno-69'-vs-VLM-'56¾-J'-NESOGLASJE-[~]!] (Juni 28., pokop 30. — KROP-datumi-VLM-'23'-misread!) — '¾-Ziblav'[?kriptično-'bolehal-¾-leta']; + ★★★ h69-2/2-1874 (→ z15-BRINC-April!) + [z51]",
     "died Joannes BRUNE [★★★ KROP-clear!], 69 [★★★ the-KROP-'69'-vs-VLM-'56¾-J'-DISAGREEMENT-[~]!] (Juni 28, buried 30 — KROP-the-VLM-'23'-misread!) — '¾-Ziblav'[?]; + ★★★ the-h69-2/2-1874 (→ z15-BRINC!) + [z51]"),
    ("21", 125, 61, "umrl Johann SABLER[?], 19 LET (September 12., pokop 13.) — [?]; ★★★ priimek-PREČRTAN-KORIGIRAN ('Hauš[?]-prečrtan' — KROP+VLM-soglasje!); previden-1; + ★ h21-nov-dokaz + [z61]",
     "died Johann SABLER[?], 19 YEARS (Sept 12, buried 13) — [?]; ★★★ the-surname-STRUCK-THROUGH-CORRECTED ('Hauš[?]' — KROP+VLM-agreement!); previden-1; + ★ the-h21-new-proof + [z61]"),
    ("48", 125, 64, "umrla Maria HRASTROVIČ[?], 27 LET (September 16., pokop 17.) — [?]; + ★ h48-nov-dokaz (cf. P199-h48-KLOBUČAR-1878!) + [z64]",
     "died Maria HRASTROVIČ[?], 27 YEARS (Sept 16, buried 17) — [?]; + ★ the-h48-new-proof (cf. P199-h48!) + [z64]"),
    ("6", 125, 67, "umrl Johann JABLOVIČ[?], 25 LET (September 24., pokop 26.) — [?]; + ★★★ h6-P200-NIT-RAZŠIRJENA-NAZAJ (1874 → 1877!) + [z67]",
     "died Johann JABLOVIČ[?], 25 YEARS (Sept 24, buried 26) — [?]; + ★★★ the-h6-P200-THREAD-EXTENDED-BACK (1874 → 1877!) + [z67]"),
    ("33", 125, 69, "umrla Katharina KRIŽAN [★★★ KROP-'33.'-glif-za-glifom-'ne-5-ne-8-ne-9' — h83-VLM-POPRAVEK→h33! VLM-'Valbarina[?]'-→KROP-'Katharina'!], 60 LET (September 25., pokop 27.) — Wassersucht; previden-1; provisorium KOGEJ [★★★ 'p.-undenard-Kogej'-PODPIS-1874! KOGEJ-NIT-4.-LETO!]; + ★★★ h33-NOVA-hiša + KOGEJ-'provisorium'-RANK-1874 + [z69]",
     "died Katharina KRIŽAN [★★★ KROP-'33.'-letter-by-letter — the-h83-VLM-CORRECTED→h33!], 60 YEARS (Sept 25, buried 27) — Wassersucht; previden-1; provisorium KOGEJ [★★★ the-'Kogej'-SIGNATURE-1874! the-KOGEJ-THREAD-4th-YEAR!]; + ★★★ h33-NEW-HOUSE + the-KOGEJ-'provisorium'-RANK + [z69]"),
    ("72", 125, 71, "umrla Maria MALENŠIČ[?], 72 LET (September 28., pokop 29.) — [?]; + ★★★ h72-2/2-1874 (→ z39-MRTVOROJEN-Mai! h72-NIT-×2-v-4-mesecih!) + [z71]",
     "died Maria MALENŠIČ[?], 72 YEARS (Sept 28, buried 29) — [?]; + ★★★ the-h72-2/2-1874 (→ z39-STILLBORN-Mai! ×2-IN-4-MONTHS!) + [z71]"),
    ("36", 126, 74, "umrla Katharina GOLOB, 'dbšl.-umrl.-Kužñar[?]', 43 LET [~] (September 12., pokop 14.) — [?]; + ★ h36[~]-dvom-hišne-št. + [z74]",
     "died Katharina GOLOB, the-widow-of-the-late-Kužñar[?], 43 YEARS [~] (Sept 12, buried 14) — [?]; + ★ the-h36[~]-doubt + [z74]"),
    ("64", 126, 75, "umrl Johann JAVORNIK[?], 'npšl. R.'[?], 62 LET [~] (September 16., pokop 18.) — [?]; + ★★★ h64-2/2-1874 (→ z37-VEBČAR-Mai!) + [z75]",
     "died Johann JAVORNIK[?], 62 YEARS [~] (Sept 16, buried 18) — [?]; + ★★★ the-h64-2/2-1874 (→ z37!) + [z75]"),
    ("38", 126, 77, "umrla Maria KAMBIČ[?], 'dbšl.'[?], 72 LET [~] (Oktober 10., pokop 12.) — [?]; + ★ h38[~]-dvom + KAMBIČ-nit (cf. P202-z17-h31!) + [z77]",
     "died Maria KAMBIČ[?], 72 YEARS [~] (Oct 10, buried 12) — [?]; + ★ the-h38[~]-doubt + the-KAMBIČ-thread (cf. P202-z17!) + [z77]"),
    ("57", 126, 81, "umrl Michael LOGAR, 'kolonist[?]', 1 LETO [~] (November 10., pokop 12.) — Gichtern; previden-1; c.-fr.-Franc DOUGAN [DOVGAN-nit!]; + ★★★ h57-P200-NIT-RAZŠIRJENA-NAZAJ (1874 → 1877 — 3-LETA!) + KROP-'57.'-NE-h8! + ★ MODRA-TINTA-'12'-annotacija-kasneje (anomalija!) + otrok + [z81]",
     "died Michael LOGAR, 'colonist[?]', 1 YEAR [~] (Nov 10, buried 12) — Gichtern; previden-1; c.-fr.-Franc DOUGAN [the-DOVGAN-thread!]; + ★★★ the-h57-P200-THREAD-EXTENDED-BACK (1874 → 1877!) + KROP-'57.'-NOT-h8! + ★ the-BLUE-INK-'12'-later-annotation (anomaly!) + the-child + [z81]"),
    ("19", 127, 85, "umrla Catharina KRIČ[?], 'nšl.'[?], 76 LET (November 24., pokop 26.) — 'Alb-Halsbräune'[?]; previden-1; provisorium-Bogija-Corp. [KOGEJ-grafia!]; + ★★★ h19-NOVA-hiša (KROP-slika-'19.'! P202-tail-None→POPRAVEK!) + starostinka + [z85]",
     "died Catharina KRIČ[?], 76 YEARS (Nov 24, buried 26) — [?]; previden-1; provisorium-Bogija-Corp. [the-KOGEJ-graphia!]; + ★★★ h19-NEW-HOUSE (the-KROP-image! the-P202-tail-None→CORRECTED!) + the-elderly + [z85]"),
    ("29", 127, 88, "umrl Mathias MILER[?Milek], 'Abb.'[?opat/vdovec-grafia], 71 LET (November 28., pokop 30.) — 'Alb-Halsbräune'[?]; previden-1; provisorium-Hoggin-Corp. [KOGEJ-grafia!]; + ★★★ h29-NOVA-hiša (KROP-slika-'29.'! P202-tail-None→POPRAVEK!) + [z88]",
     "died Mathias MILER[?Milek], 'Abb.'[?], 71 YEARS (Nov 28, buried 30) — [?]; previden-1; provisorium-Hoggin-Corp. [the-KOGEJ-graphia!]; + ★★★ h29-NEW-HOUSE (the-KROP-image! the-P202-tail-None→CORRECTED!) + [z88]"),
]

lines = []
lines.append("  // ——— P203: mrliška PREDZGODOVINA 04106, leto 1874 = 12. leto PREDZGODOVINSKE LINIJE (s119-glava–s127-z10 == Pag. 114–121, z1–z94 = 94 vpisov — vrstna-aritmetika 3+11+16+15+14+13+12+10 (s123-DUPLIKAT-IZPUŠČEN!) + meseci J4+F5+M4+A10+M19+J11+J5+A1+S17+O3+N11+D4; preslikava-pag-LEKCIJA-#21: s118–s122 = sken−5, s124+ = sken−6 (natisnjene-št.-strani-×7: 113/116/117/118-×2/119/120/121!), md5-križna-ta-seja: s127+s126-sveža == P202-disk-1:1 — veriga-P197→…→P203-7.×!) — 21 GRIBLJE-blokov / 18 hiš (h64-×2 + h69-×2 + h72-×2!) ———")
lines.append("  // ★★★ MEJA 1873/74 = s119: TAIL-10-DEZ-1873-nad (margine-201–212! 3-Griblje!) + VELIKA-'18 74. Jänner'-GLAVA (split! NO-'Incipit-annus-Domini'-VLM-halucinacija-FALSIFICIRANA!) + ★★★ MEJA 1874/75 = s127 (P202-REUSE-1:1: TAIL-10-NOV/DEZ-1874 + hišni-POPRAVKI-Krič-h19 + Miler-h29!) + ★★★ VLM-FALSIFIKACIJE-×3-KROP-REŠENE (s125-'Jänner'-×13→SEPTEMBER-'9.'-numerično! + s122-'1877'→'1874.'-glif-za-glifom! + 'Incipit'-halucinacija!) + ★★★ 45.-in-46.-POTRDITEV-invariante (s122-z1-'1874.'-Mai-celica + s125-z1-'1874.'-September-celica!) + ★★★ LEKCIJA-#21-DOUBLE-SCAN-2.× (s123==s124 = pag-118-×2 — natisnjena-'118'-na-obeh + hamming-15 + KROP-r1/r2-1:1-Tilak/Gradec-75!) + ★★★ KROP-POPRAVKI-hišnih-št.-×5 (h33-ne-h83-KRIŽAN! + h57-ne-h8-LOGAR! + h39-ne-h34-TILAK! + h19-KRIČ! + h29-MILER!) + ★★★ KOGEJ-'provisorium'-PODPIS-1874 (z69-'p.-undenard-Kogej'! NIT-4.-LETO-1874→1877!) + DOVGAN-nit (Dougan/Dovgan-×6!) + BRIME-×2-v-5-tednih (h24/h28-2-MARIJE!) + MRTVOROJEN-z39-h72 (oče-[?]Krajnc-vs-Janec!) + BRUNE-z51-starost-NESOGLASJE (KROP-69-vs-VLM-56¾!) + h11-LUNIČ-16-dni (KUNIĆ-hiša-1-leto-pred!) + h6/h57-NITI-RAZŠIRJENE-NAZAJ (→1877!) + h72-×2-v-4-mesecih + h64-×2 + h69-×2 + Sabler-priimek-PREČRTAN + modra-tinta-'12'-annotacija + otroška-umrljivost-33%-7/21-jasna + dokaz research/issue17/parish-death-1874-04106.json (94-entries: 21-Griblje + 73-druge! 14-anomalij + 10-crossChecks + honesty-16 + tail-1873-×10-P204-lead!) + skripte: p203_fetch.py + p203_read_page.mjs + p203_crop.py + p203_build_entries.py + p203_build_proof.py ———")
for hisna, sken, zap, wsi, wen in B:
    lines.append("  {")
    lines.append(f'    houseNo: "{hisna}",')
    lines.append('    bookSignature: "04106",')
    lines.append("    year: 1874,")
    lines.append(f"    scan: {sken},")
    lines.append(f"    page: {sken - 5 if sken <= 123 else sken - 6},")
    lines.append(f'    whatSi: "{wsi}",')
    lines.append(f'    whatEn: "{wen}",')
    lines.append('    status: "DOCUMENTED",')
    lines.append("  },")
section = "\n".join(lines) + "\n"
out = src.replace(ANCHOR, section + ANCHOR, 1)
TS.write_text(out, encoding="utf-8")
print(f"OK — vstavljenih {len(B)} blokov; year-1874-blokov: {out.count('year: 1874,')}")
