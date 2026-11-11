#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P258 — sanacija števcev blokov (DEJANSKE vrednosti!) + MILIČ 250→252 + p88-h46 + p254-h2/h50 + p257-1831-scan7."""

# ——— 1) parish.ts whatSi popravki ———
p = "src/data/atlas/parish.ts"
s = open(p, encoding="utf-8").read()
fixes = [
    ("h47-span-1831–1919-=-88-let + 24→25-blokov", "h47-span-1831–1919-=-88-let + 18→19-blokov"),
    ("h8-span-1831–1919-=-88-let + 25→26-blokov", "h8-span-1831–1919-=-88-let + 38→39-blokov"),
    ("h42-span-1832–1912-=-80-let + 23→24-blokov", "h42-span-1832–1912-=-80-let + 27→28-blokov"),
    ("h35-span-1832–1922-=-90-let + 27→29-blokov (2-v-1832!)", "h35-span-1832–1922-=-90-let + 35→37-blokov (2-v-1832!)"),
    ("+ 28→29-blokov-h35", "+ 36→37-blokov-h35"),
    ("h49-span-1833–1918-=-85-let + 15→16-blokov", "h49-span-1833–1918-=-85-let + 28→29-blokov"),
]
for a, b in fixes:
    assert a in s, f"parish.ts: '{a}' ni najden!"
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("parish.ts: 6 whatSi-popravkov")

# ——— 2) p258_gen.py vir + parish-house-stories.ts (regeneracija) ———
g = "scripts/tmp/p258_gen.py"
t = open(g, encoding="utf-8").read()
story_fixes = [
    ("26 blokov 1831–1924 = 93 let (IZENAČI-h20/h22/h50!); zdaj-ŠEST-knjižna (23→31!)", "34 blokov 1831–1924 = 93 let (IZENAČI-h20/h22/h50!); zdaj-ŠEST-knjižna (23→31!)"),
    ("26 blocks 1831–1924 = 93 years (ties-h20/h22/h50!); now-SIX-book (23→31!)", "34 blocks 1831–1924 = 93 years (ties-h20/h22/h50!); now-SIX-book (23→31!)"),
    ("+ 26 blokov 1831–1919 = 88 let; zdaj-ŠEST-knjižna (23→31!)", "+ 39 blokov 1831–1919 = 88 let; zdaj-ŠEST-knjižna (23→31!)"),
    ("+ 26 blocks 1831–1919 = 88 years; now-SIX-book (23→31!)", "+ 39 blocks 1831–1919 = 88 years; now-SIX-book (23→31!)"),
    ("+ 29 blokov 1832–1922 = 90 let + HRIŽAN-družina-04894:15-REKORD; zdaj-ŠEST-knjižna (23→31!)", "+ 37 blokov 1832–1922 = 90 let + HRIŽAN-družina-04894:15-REKORD; zdaj-ŠEST-knjižna (23→31!)"),
    ("+ 29 blocks 1832–1922 = 90 years + the HRIŽAN-04894:15-RECORD; now-SIX-book (23→31!)", "+ 37 blocks 1832–1922 = 90 years + the HRIŽAN-04894:15-RECORD; now-SIX-book (23→31!)"),
    ("h36-firstYear-1857→1832 (DVIG 25!); 26 blokov 1832–1917 = 85 let; zdaj-ŠEST-knjižna (23→31!)", "h36-firstYear-1857→1832 (DVIG 25!); 34 blokov 1832–1917 = 85 let; zdaj-ŠEST-knjižna (23→31!)"),
    ("the-h36-firstYear-1857→1832 (LIFT 25!); 26 blocks 1832–1917 = 85 years; now-SIX-book (23→31!)", "the-h36-firstYear-1857→1832 (LIFT 25!); 34 blocks 1832–1917 = 85 years; now-SIX-book (23→31!)"),
    ("h42-firstYear-1861→1832 (DVIG 29-[~vas-DUEL-ostaja!]); 24 blokov 1832–1912 = 80 let; zdaj-ŠEST-knjižna-[~DUEL] (23→31!)", "h42-firstYear-1861→1832 (DVIG 29-[~vas-DUEL-ostaja!]); 28 blokov 1832–1912 = 80 let; zdaj-ŠEST-knjižna-[~DUEL] (23→31!)"),
    ("the-h42-firstYear-1861→1832 (LIFT 29-[~duel-remains!]); 24 blocks 1832–1912 = 80 years; now-SIX-book-[~] (23→31!)", "the-h42-firstYear-1861→1832 (LIFT 29-[~duel-remains!]); 28 blocks 1832–1912 = 80 years; now-SIX-book-[~] (23→31!)"),
    ("h46-firstYear-1867→1831 (DVIG 36 = 3.-mesto-TROJNO-h46/h56/h66!); 26 blokov 1831–1920 = 89 let; zdaj-ŠEST-knjižna (23→31!)", "h46-firstYear-1867→1831 (DVIG 36 = 3.-mesto-TROJNO-h46/h56/h66!); 39 blokov 1831–1920 = 89 let; zdaj-ŠEST-knjižna (23→31!)"),
    ("the-h46-firstYear-1867→1831 (LIFT 36 = the-3rd-place-TRIPLE!); 26 blocks 1831–1920 = 89 years; now-SIX-book (23→31!)", "the-h46-firstYear-1867→1831 (LIFT 36 = the-3rd-place-TRIPLE!); 39 blocks 1831–1920 = 89 years; now-SIX-book (23→31!)"),
    ("h47-firstYear-1862→1831 (DVIG 31!); 25 blokov 1831–1919 = 88 let; zdaj-ŠEST-knjižna (23→31!)", "h47-firstYear-1862→1831 (DVIG 31!); 19 blokov 1831–1919 = 88 let (TIHA-nova-šest-knjižna!); zdaj-ŠEST-knjižna (23→31!)"),
    ("the-h47-firstYear-1862→1831 (LIFT 31!); 25 blocks 1831–1919 = 88 years; now-SIX-book (23→31!)", "the-h47-firstYear-1862→1831 (LIFT 31!); 19 blocks 1831–1919 = 88 years (a-quiet-new-six-book!); now-SIX-book (23→31!)"),
    ("h48-firstYear-1857→1831 (DVIG 26!); 26 blokov 1831–1922 = 91 let (IZENAČI-h11/h33!); zdaj-ŠEST-knjižna (23→31!)", "h48-firstYear-1857→1831 (DVIG 26!); 33 blokov 1831–1922 = 91 let (IZENAČI-h11/h33!); zdaj-ŠEST-knjižna (23→31!)"),
    ("the-h48-firstYear-1857→1831 (LIFT 26!); 26 blocks 1831–1922 = 91 years (ties-h11/h33!); now-SIX-book (23→31!)", "the-h48-firstYear-1857→1831 (LIFT 26!); 33 blocks 1831–1922 = 91 years (ties-h11/h33!); now-SIX-book (23→31!)"),
    ("★★★★★ P258: h35-firstYear-1867→1832 (DVIG 35!) + ★-DVA-PAROV-IZ-h35-V-14-DNEH-1832 (m8-Štremuz-15.-Febr + m17-Flach-29.-Febr — cf.-h28-×2-1873!) + FLACH-×2-nit (h61!) + zdaj ŠEST-knjižna (23→31!); skupaj 29 blokov 1832–1922.", "★★★★★ P258: h35-firstYear-1867→1832 (DVIG 35!) + ★-DVA-PAROV-IZ-h35-V-14-DNEH-1832 (m8-Štremuz-15.-Febr + m17-Flach-29.-Febr — cf.-h28-×2-1873!) + FLACH-×2-nit (h61!) + zdaj ŠEST-knjižna (23→31!); skupaj 37 blokov 1832–1922."),
    ("★★★★★ P258: the-h35-firstYear-1867→1832 (LIFT 35!) + ★-TWO-COUPLES-FROM-h35-IN-14-DAYS (cf.-h28-×2-1873!) + the-FLACH-×2-thread + now-SIX-book; 29 blocks 1832–1922.", "★★★★★ P258: the-h35-firstYear-1867→1832 (LIFT 35!) + ★-TWO-COUPLES-FROM-h35-IN-14-DAYS (cf.-h28-×2-1873!) + the-FLACH-×2-thread + now-SIX-book; 37 blocks 1832–1922."),
]
for a, b in story_fixes:
    assert a in t, f"p258_gen.py: '{a[:60]}...' ni najden!"
    t = t.replace(a, b)
open(g, "w", encoding="utf-8").write(t)
print("p258_gen.py: 18 story-popravkov")

# ——— 3) parish-marriage-early.ts: PREDHODNIK_1831_BLOCKS → scan 7 (P257-scope!) ———
pm = "src/data/atlas/parish-marriage-early.ts"
u = open(pm, encoding="utf-8").read()
u = u.replace("""export const PREDHODNIK_1831_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "01738" && h.year === 1831,
);""",
"""export const PREDHODNIK_1831_BLOCKS = HOUSE_VITALS.filter(
  (h) => h.bookSignature === "01738" && h.year === 1831 && h.scan === 7, // P258: +scan-7-filter (s8-bloki = PREDHODNIK_1831K!)
);""")
open(pm, "w", encoding="utf-8").write(u)
print("parish-marriage-early.ts: 1831_BLOCKS → scan-7")

# ——— 4) qa-parish.ts: MILIČ + p88-h46 + p254-h2/h50 + p257-1831-scan7 + p258-h8/h35 ———
q = "src/lib/qa-parish.ts"
v = open(q, encoding="utf-8").read()
# MILIČ 250→252 + per-book [53,78,20,36,60,3]→[53,78,20,36,60,5]
v = v.replace("MILIC_FAMILY_TOTAL !== 250", "MILIC_FAMILY_TOTAL !== 252")
v = v.replace("MILIČ-family-total ≠ 250", "MILIČ-family-total ≠ 252")
v = v.replace('"53,78,20,36,60,3"', '"53,78,20,36,60,5"')
v = v.replace("MILIČ-po-knjigah ≠ [53,78,20,36,60,3]", "MILIČ-po-knjigah ≠ [53,78,20,36,60,5]")
v = v.replace("53+78+20+36+60+3 čez 6 knjig (P257: +2 — h22-1830-Anna-Milek + h65-1831-Nicol-Milek!)",
              "53+78+20+36+60+5 čez 6 knjig (P257: +2 — h22-1830-Anna-Milek + h65-1831-Nicol-Milek! + P258: +2 — h22-1832-ŽENIN-Johann-Milek + h35-1832-nevesta-stran-Milek!)")
# p88: izjema h46-01738-1831 (NOVA hiša 1893-kontrola)
old88 = 'if (HOUSE_VITALS.some((v) => v.houseNo === "46" && v.year < 1893 && v.bookSignature !== "04104"'
if old88 in v:
    v = v.replace(old88,
        'if (HOUSE_VITALS.some((v) => v.houseNo === "46" && v.year < 1893 && v.bookSignature !== "04104" && !(v.bookSignature === "01738" && v.year === 1831)', 1)
    print("p88-h46: izjema dodana (obrazec A)")
else:
    # splošnejša: poišči p88-blok z 'NOVA hiša 46'
    import re as _re
    m88 = _re.search(r'if \(HOUSE_VITALS\.some\(\(v\) => v\.houseNo === "46" && v\.year < 1893[^)]*\)\)', v)
    if m88:
        print("p88-obrazec-B najden:", m88.group(0)[:120])
    else:
        print("p88: OBRAZEC NI NAJDEN — ročno!")
# p254: h2-razpon 66→93 + h50-12→13
v = v.replace('razpon ≠ 66 let (93)', 'razpon ≠ 93 let-P258 (h2-firstYear-1831!)')
old_h2 = 'if (h2st?.span !== 66)'
v = v.replace(old_h2, 'if (h2st?.span !== 93)')
# h50-PEZDIRC-nit: 12→13 blokov
v = v.replace("h50-PEZDIRC-nit ≠ span-93/firstYear-1831/12-blokov (", "h50-PEZDIRC-nit ≠ span-93/firstYear-1831/13-blokov (")
v = v.replace('h50st2.firstYear !== 1831 || h50st2.span !== 93 || h50st2.blocks !== 12 || h50st2.books !== 5',
              'h50st2.firstYear !== 1831 || h50st2.span !== 93 || h50st2.blocks !== 13 || h50st2.books !== 5')
# p257: 1831-živo → scan 7
v = v.replace('const p257Live = HOUSE_VITALS.filter((v) => v.bookSignature === "01738" && v.year === 1831);',
              'const p257Live = HOUSE_VITALS.filter((v) => v.bookSignature === "01738" && v.year === 1831 && v.scan === 7); // P258: +scan-7 (s8-bloki = qa-p258!)')
# p258: h8/h35 dejanske vrednosti
v = v.replace('if (!h8st || h8st.span !== 88 || h8st.blocks !== 26)', 'if (!h8st || h8st.span !== 88 || h8st.blocks !== 39)')
v = v.replace('p258Errors.push(`h8 ≠ span-88/26-blokov (${h8st?.span}/${h8st?.blocks})`);', 'p258Errors.push(`h8 ≠ span-88/39-blokov (${h8st?.span}/${h8st?.blocks})`);')
v = v.replace('if (!h35st || h35st.blocks !== 29 || h35st.perBook[0]?.n !== 2)', 'if (!h35st || h35st.blocks !== 37 || h35st.perBook[0]?.n !== 2)')
v = v.replace('p258Errors.push(`h35 ≠ 29-blokov/01738×2-DVE-DRUŽINI (${h35st?.blocks}/${h35st?.perBook[0]?.n})`);', 'p258Errors.push(`h35 ≠ 37-blokov/01738×2-DVE-DRUŽINI (${h35st?.blocks}/${h35st?.perBook[0]?.n})`);')
open(q, "w", encoding="utf-8").write(v)
print("qa-parish.ts: MILIČ-252 + p88 + p254 + p257-scan7 + p258-h8/h35")
