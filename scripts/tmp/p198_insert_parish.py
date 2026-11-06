#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P198 — vstavi 9-GRIBLJE-blokov (04106, leto 1879) v parish.ts
PRED P197-sekcijo (newest-first vzorec; SANACIJA-RE-RUN: repo-re-clone-@195b4e1
→ P198-bloki-bili-izgubljeni-z-wipe → re-insert-iz-sejnih-dokazov!)."""
from pathlib import Path

TS = Path("/home/z/my-project/muzej-backup/src/data/atlas/parish.ts")
src = TS.read_text(encoding="utf-8")

ANCHOR = "  // ——— P197: mrliška PREDZGODOVINA 04106, leto 1880"
assert src.count(ANCHOR) == 1, f"anchor-count={src.count(ANCHOR)}"
assert "year: 1879," not in src, "1879-bloki-že-obstajajo?!"

BLOCKS = [
    # (hišna, sken, zap, whatSi, whatEn)
    ("56", 158, 5,
     "umrl Peter ŠIMEC [~Simec-obeh-VLM-branj — kanon-ŠIMEC-nit!], '½ G.' [~Götlaner-stan-glif], 82 LET [~88-re-read; KROP-crop-'82'-jasno!] (22. 1., pokop 24. 1.) — Asthma; previden (1); Franz Jančar 'coop.'; + ★★★ 1.-GRIBLJE-VPIS-1879 + ★ ŠIMEC-nit (→ 1880-z19-Anna-Simec-h39-P197 + 1881-h18-TIMEC-P196!) + MEJA-'Incipit-annus'+velika-'1 8|7 9'-SPLIT-nad (37.-POTRDITEV-invariante — KROP!) + [z5]",
     "died Peter ŠIMEC [~Simec-both-VLM-reads — canonical-ŠIMEC-thread!], a '½ G.' [~Götlaner-the-glyph], 82 YEARS [~88-re-read; KROP-crop-'82'-CLEAR!] (Jan 22, buried Jan 24) — Asthma; previden (1); Franz Jančar 'coop.'; + ★★★ the-1st-GRIBLJE-ENTRY-1879 + ★ the-ŠIMEC-thread (→ 1880-z19 + 1881-h18-TIMEC-P196!) + the-'Incipit-annus'+big-'1 8|7 9'-SPLIT-above (the-37th-INVARIANT-CONFIRMATION — KROP!) + [z5]"),
    ("1", 158, 6,
     "umrla Anna ZELIHA [~Zeliho-obeh-branj!], 'apf. ¼ Göttlanerstochter' [~stan-glif-KROP!], 74 LET [~¾-J-re-read; KROP-crop-'74 J.'-jasno!] (26. 1., pokop 27. 1.) — Fraisen (SOGLASJE-obeh-branj + KROP-max!); previden (1); Franz Jančar 'coop.'; + ★ h1-nit (→ ZELŠKO-h1-×2-1882-P195!) + zadnja-GRIBLJE-s158 + kronološki-preskok-naslednja-vrstica (z7-Jan23!) + [z6]",
     "died Anna ZELIHA [~Zeliho-both-reads!], 'apf. ¼ Göttlanerstochter' [~the-glyph-KROP!], 74 YEARS [~¾-J-re-read; KROP-crop-'74 J.'-CLEAR!] (Jan 26, buried Jan 27) — Fraisen (BOTH-READS-AGREE + KROP-max!); previden (1); Franz Jančar 'coop.'; + ★ the-h1-thread (→ ZELŠKO-h1-×2-1882-P195!) + the-last-GRIBLJE-on-s158 + the-chronology-hiccup-next-row (z7-Jan23!) + [z6]"),
    ("53", 159, 15,
     "umrl Peter BEŽEK? [~Grčevac/Razlava-re-read — priimek-NERAZREŠEN [?]!], 'spół. ½ Gribl. Krist. Spn.' [~stan-glif], ½ LETA (SOGLASJE-obeh-branj: '½ J.'!) (6. 3., pokop 7. 3.) — Krämpfe? [~Farnism-neberljivo]; previden (1); Franz Jančar 'coop.'; + ★ h53-nit (→ tail-1878-z83-Mathias-Peglavc-87J-Wassersucht-tik-prej!) + FRISELN-×14-1879 + [z15]",
     "died Peter BEŽEK? [~Grčevac/Razlava-re-read — surname-UNRESOLVED [?]!], 'spół. ½ Gribl. Krist. Spn.' [~the-glyph], ½ YEAR (BOTH-READS-AGREE: '½ J.'!) (März 6, buried März 7) — Krämpfe? [~Farnism-unreadable]; previden (1); Franz Jančar 'coop.'; + ★ the-h53-thread (→ tail-1878-z83-Mathias-Peglavc-87J-Wassersucht-just-before!) + FRISELN-×14-1879 + [z15]"),
    ("44", 160, 27,
     "umrla Maria PEGLIC? [~Pegelj-1.VLM/~Pezdirc-re-read — priimek-[~]!], 'apf. ½ G.-Kostgängerin?' [~Kostbn-stan-glif], 37 LET (26. 5., pokop 28. 5.) — Gehirnentzündung (ARBITRAŽA-A3: konec-'-entzündung'-umlaut — re-read-'Gichtarmzündung'-ZAVRJEN!); previden (1); Franz Jančar 'coop.'; + ★★★ GEHIRNENTZÜNDUNG-KATASTROFA-×2-ISTEGA-DNA (h40-z28-97J!) + h44-nov-dokaz (ARBITRAŽA-A2-'44.'-dva-4-glifa — re-read-'14'-ZAVRJEN!) + [z27]",
     "died Maria PEGLIC? [~Pegelj-1st-VLM/~Pezdirc-re-read — surname-[~]!], 'apf. ½ G.-Kostgängerin?' [~Kostbn-the-glyph], 37 YEARS (Mai 26, buried Mai 28) — Gehirnentzündung (ARBITRATION-A3: the-'-entzündung'-ending-with-umlaut — the-re-read-'Gichtarmzündung'-REJECTED!); previden (1); Franz Jančar 'coop.'; + ★★★ the-GEHIRNENTZÜNDUNG-CATASTROPHE-×2-SAME-DAY (h40-z28-97J!) + h44-new-proof (ARBITRATION-A2-'44.'-two-4-glyphs — the-re-read-'14'-REJECTED!) + [z27]"),
    ("40", 160, 28,
     "umrl Mathias PEGLIC? [~Pezdirc-re-read — priimek-[~]!], 97 LET ★★★ KORPUS-REKORD-STAROSTI (KROP-max-zoom-'9'+γ-7+'.'-struktura-identična-z27-'37.' + RE-READ-SOGLASJE-'97[~9J/97?]'-2.-neodvisni-viri!) (26. 5., pokop 28. 5.) — Gehirnentzündung (KROP-fragment-'-ntzü-'+umlaut + ARBITRAŽA-A3!); previden (1); Franz Jančar 'coop.'; + ★★★ z28-DUPLIKAT-1/2 (rdeči-margin-'28'-s160-konec + RE-READ-SOGLASJE-28! cf. P196-z8-DUPLIKAT!) + ★★★ istega-dna-kot-z27-h44 (h40+h44-sosednji = žarišče?) + [z28]",
     "died Mathias PEGLIC? [~Pezdirc-re-read — surname-[~]!], 97 YEARS ★★★ CORPUS-AGE-RECORD (KROP-max-zoom-'9'+γ-7+'.'-structure-identical-to-z27-'37.' + the-RE-READ-AGREEMENT-'97[~9J/97?]'-2nd-independent-source!) (Mai 26, buried Mai 28) — Gehirnentzündung (KROP-fragment + ARBITRATION-A3!); previden (1); Franz Jančar 'coop.'; + ★★★ z28-DUPLICATE-1/2 (the-red-margin-'28'-at-s160-end + the-RE-READ-AGREEMENT-28! cf. P196-z8-DUPLICATE!) + ★★★ same-day-as-z27-h44 (h40+h44-adjacent = hotspot?) + [z28]"),
    ("20", 161, "28-DUP",
     "umrl Martin PEZDIRC [~Martinus-Pegdirič-obeh-branj!], '½ G.-Unterzüngler?' [~Unterzinglon-1./~Gutsingler-re-read-stan-glif], 44 LET (SOGLASJE-obeh-branj!) (29. 6., pokop 1. 7.) — Abmattsschwäche? [~Abzehrungsschwäche-1./~Abzehrungsfriesen-re-read!]; previden (1); Franz Jančar 'coop.'; + ★★★ z28-DUPLIKAT-2/2 (s161-top-'28' — margin-strip-28,29,30–37-KROP-VSI-JASNI + RE-READ-SOGLASJE! 63-ordinalov/64-vrstic!) + ★★★ ULEDBA-#10-6.-INSTANCE (ARBITRAŽA-A1-ODLOČILNA: '1879-Julβ'-header + 'Junii-29.'-JASNO → pokop-'1.'-'Juli' — re-read-'July-29/Aug-1'-ZAVRJEN!) + ★ h20-×2-1879 (→ z47-Okt! cf. PEZDIREC-era-h20-P171!) + [z28-dup]",
     "died Martin PEZDIRC [~Martinus-Pegdirič-both-reads!], '½ G.-Unterzüngler?' [~Unterzinglon-1st/~Gutsingler-re-read-the-glyph], 44 YEARS (BOTH-READS-AGREE!) (June 29, buried July 1) — Abmattsschwäche? [~variants-documented!]; previden (1); Franz Jančar 'coop.'; + ★★★ z28-DUPLICATE-2/2 (s161-top-'28' — margin-strip-28–37-KROP-ALL-CLEAR + RE-READ-AGREEMENT! 63-ordinals/64-rows!) + ★★★ ULEDBA-#10-6th-INSTANCE (ARBITRATION-A1-DECISIVE: the-'1879-Julβ'-header + 'Junii-29.'-CLEAR → burial-'1.'-'Juli' — the-re-read-'July-29/Aug-1'-REJECTED!) + ★ h20-×2-1879 (→ z47-Okt! cf. PEZDIREC-era-h20-P171!) + [z28-dup]"),
    ("20", 162, 47,
     "umrla Nelly? [~Molly-1./~Marija-1.VLM/~Marthy-re-read — 4-ime-varianti-NERAZREŠENE!] ABRAMŠEK? [~abramſkon-1./~Abram-re-read] — PIVK? [2.-vrstica-1.; ~Elend-re-read!], BREZ-starosti/bolezni (RE-READ-SOGLASJE-[?]! — mrtvorojen?/nedokončan-vpis!) (6. 10., pokop 7. 10.) — —; —; Franz Jančar 'coop.'; + ★★★ h20-×2-1879-2/2 (z28-DUP-Pezdirc-Juni!) + ★ redka-pusta-vrstica-GRIBLJE (cf. z35-totgeboren-Prilozje!) + [z47]",
     "died Nelly? [~Molly-1st/~Marija-1st-VLM/~Marthy-re-read — 4-name-variants-UNRESOLVED!] ABRAMŠEK? [~abramſkon-1st/~Abram-re-read] — PIVK? [2nd-line-1st; ~Elend-re-read!], NO-age/disease (the-RE-READ-AGREEMENT-[?]! — stillbirth?/unfinished-entry!) (Oct 6, buried Oct 7) — —; —; Franz Jančar 'coop.'; + ★★★ h20-×2-1879-2/2 (z28-DUP-Pezdirc-June!) + ★ a-rare-empty-GRIBLJE-row (cf. z35-totgeboren-Prilozje!) + [z47]"),
    ("30", 163, 58,
     "umrla Martha KRIŽAN, '½ hči/dekla? [~½-Grefin-Altna-P197-branja]' [~stan-glif], 60 LET (RE-READ-SOGLASJE-×2-branji: vas+ime+starost!) (13. 12., pokop 15. 12. — KROP-datumi-jasna!) — Gelbsucht (SOGLASJE!); previden (1); Franz Jančar 'co.op'; + ★ december-nazaj-zapolnitev (z59-12.-naslednja!) + h30-nov-dokaz + [z58]",
     "died Martha KRIŽAN, '½ hči/dekla? [~½-Grefin-Altna-the-P197-reading]' [~the-glyph], 60 YEARS (the-RE-READ-AGREEMENT-×2-reads: vas+name+age!) (Dec 13, buried Dec 15 — KROP-dates-CLEAR!) — Gelbsucht (AGREEMENT!); previden (1); Franz Jančar 'co.op'; + ★ december-backfill (z59-12.-next!) + h30-new-proof + [z58]"),
    ("32", 163, 59,
     "umrla Maria KRAUS, 'hči ½ Griblar dekica? [~½-Grefin-služkinja-P197]' [~stan-glif], ½ LETA [~] (RE-READ-SOGLASJE!) (12. 12., pokop 13. 12. — KROP!) — Griža? [~Geviža-P197]/Fraisen-P197; previden (1); Franz Jančar 'co.op'; + ★ december-kronološki-preskok-2/3 (13→12→7 — KROP-datumi!) + h32-nov-dokaz + FRISELN-×14 + [z59]",
     "died Maria KRAUS, 'hči ½ Griblar dekica? [~½-Grefin-služkinja-P197]' [~the-glyph], ½ YEAR [~] (the-RE-READ-AGREEMENT!) (Dec 12, buried Dec 13 — KROP!) — Griža? [~Geviža-P197]/Fraisen-P197; previden (1); Franz Jančar 'co.op'; + ★ december-chronology-hiccup-2/3 (13→12→7 — KROP-dates!) + h32-new-proof + FRISELN-×14 + [z59]"),
]

lines = []
lines.append("  // ——— P198: mrliška PREDZGODOVINA 04106, leto 1879 = 7. leto PREDZGODOVINSKE LINIJE (s157–s164 == Pag. 151–158, z1–z63 + ★ z28-DUPLIKAT = 64 fizičnih vrstic / 63 ordinalov == P197-'63-vpisov'-EXAKT!; pag == sken − 6, re-fetch-1:1-P197-seji (sanacija!) + PRINTED-152–156-×5-vizualno!) — 9 GRIBLJE-blokov / 8 hiš (h20-×2!) ———")
lines.append("  // ★★★ SANACIJA-RE-RUN: /tmp-wipe → repo-re-clone-iz-GitHub-@195b4e1 → re-fetch-8/8 (velikosti-1:1!) + re-VLM-×7 + tail-z62/z63-iz-SEJNEGA-ZAPISA + re-arbitraža-×5 (deterministična-reprodukcija — vzorec-P156!) + ★★★ MEJA 1878/79 = s158 ('Incipit annus'-band + velika-'1879'-SPLIT-VARIANTA '1 8'+'7 9'-stacked = 37.-POTRDITEV-invariante! restart-85→1; tail-1878 = z83–z85: KROP-hipoteza + RE-READ-SOGLASJE = 2-viri!) + MEJA 1879/80 = s164-mid-'1 8|8 0' (P197-36.-reuse! konec-1879 = z63-tail) + ★★★ z28-DUPLIKAT (Peglic-h40-97J + Pezdirc-h20-44J oba-'28' — s161-margin-strip-28–37-KROP + RE-READ-SOGLASJE! = 3.-številčna-anomalija-04106!) + ★★★ 97-LET-KORPUS-REKORD (z28-Mathias-Peglic — KROP-max-zoom + RE-READ-SOGLASJE!) + ★★★ GEHIRNENTZÜNDUNG-×2-istega-dna (z27-h44-37J + z28-h40-97J — ARBITRAŽA-A3!) + FRISELN-×14 (W-krivulja: 1879-×14 → 1880-×28 → 1881-×3 → 1882-×16!) + KRONOLOŠKI-PRESKOKI-×2 (Jänner z6→z7/z8 + Dezember 3→13→12→7→21 — KROP!) + ULEDBA-#10-6.-instance (z28-DUP: ARBITRAŽA-A1-'Junii-29'→pokop-'1. Juli'!) + JANČAR-GRIBLJE-9/9-100%-DOMINANTA (5.-leto-nit!) + s157-ordinali-73–82-KROP (VLM-'63–72'-7→6-obeh-sej → 1878 ≈ 85-vpisov-P199-lead!) + ARBITRAŽE-A1–A5 (max-zoom > VLM — 6.-potrditev-vzorca!) + dokaz research/issue17/parish-death-1879-04106.json (64-entries: 9-Griblje! 14-anomalij + 10-crossChecks + honesty-15 + lead-P199-1878!) + skripte: p198_fetch.py + p198_read_page.mjs + p198_build_entries.py + p198_build_proof.py ———")
for hisna, sken, zap, wsi, wen in BLOCKS:
    lines.append("  {")
    lines.append(f'    houseNo: "{hisna}",')
    lines.append('    bookSignature: "04106",')
    lines.append("    year: 1879,")
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
print("year-1879-blokov:", out.count("year: 1879,"))
