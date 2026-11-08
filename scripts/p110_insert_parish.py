#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P110 — vstavi 11 blokov 1915 v HOUSE_VITALS (parish.ts) pred zaključni '];'."""
import io

PATH = "src/data/atlas/parish.ts"

BLOCKS = r'''  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1915,
    scan: 269,
    page: 225,
    whatSi: "krščena Ivana († 20.2.1915 [~ — dojenček, ~1 mesec!]; marg. »+ 20/[II] 1915« — d1 4×) (20./22. 1.) — oče **Peter Brinec**, bajtar, roj. 28/9 1860 (por. 25.9.1892 | 12.96 [~]), mati **Ana roj. Butala** (22/12 1874; faza-1 »Buntala« POPRAVLJENO); h88 = 4. VPIS (1886, 1904, 1910 → 1915) — VRZEL 5 LET; **P109 lead POTRJEN (GRIBLJE 88 Ivana!)**; botra **Janez Brinec in žena njegova Doroteja Brinec** (½ zemlj.); babica Marija Jakofčič; podpis V. Valerijan Učak (svinčnik); glava 1915 ročno na VRHU str. 225 = s269",
    whatEn: "baptized Ivana (died Feb 20, 1915 [~ — an infant, ~1 month]; the marginal note »+ 20/[II] 1915« — d1 4×) (Jan 20/22) — father **Peter Brinec**, cottager, born Sep 28, 1860 (m. Sep 25, 1892 | Dec 1896 [~]), mother **Ana née Butala** (Dec 22, 1874; the phase-1 »Buntala« CORRECTED); h88 = the 4th ENTRY (1886, 1904, 1910 → 1915) — a 5-YEAR GAP; **the P109 lead CONFIRMED (GRIBLJE 88 Ivana!)**; godparents **Janez Brinec and his wife Doroteja Brinec** (half smallholder); midwife Marija Jakofčič; signature V. Valerijan Učak (pencil); the 1915 heading manually at the TOP of p. 225 = s269",
    status: "DOCUMENTED",
  },
  {
    houseNo: "45",
    bookSignature: "04105",
    year: 1915,
    scan: 270,
    page: 226,
    whatSi: "krščena Zora Jožefa († 25.7.1915 — dobenček, ~3,5 mesece; marg. »+ 25/7 15«) (6./7. 3.) — oče **Franc Rajhmer** [~], čuv.[aj]? [~], roj. 13/12 1882 [~], (por. 18.4.1908), mati **Ivana roj. Tadej** (13/8 86 [~]); h45 = 6. VPIS (1896–1912) — VRZEL 3 LETA; botra **Jurij Berdir? [~]** (½ zemlj.) + **Terezija Jakofčič**, ros. žena; babica Marija Jakofčič; podpis Učak [~]",
    whatEn: "baptized Zora Jožefa (died Jul 25, 1915 — an infant, ~3.5 months; the marginal note »+ 25/7 15«) (Mar 6/7) — father **Franc Rajhmer** [~], caretaker? [~], born Dec 13, 1882 [~], (m. Apr 18, 1908), mother **Ivana née Tadej** (Aug 13, 1886 [~]); h45 = the 6th ENTRY (1896–1912) — a 3-YEAR GAP; godparents **Jurij Berdir? [~]** (half smallholder) + **Terezija Jakofčič**, the ros. wife; midwife Marija Jakofčič; signature Učak [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "70",
    bookSignature: "04105",
    year: 1915,
    scan: 270,
    page: 226,
    whatSi: "krščena Barbara (16./17. 3.; EMŠO ž. **1603915505171** — 5× jasno, faza-1 »5505141« POPRAVLJENO) — oče **Matija Brinec**, ½ zemlj., roj. 15/7 1883 [~ — 4×; faza-1 »1888« POPRAVLJENO], mati **Marija (1877), roj. PEZDIREC**, r. 30/1? [~ — faza-1 »Perdivec« POPRAVLJENO (3.2×) — PEZDIREC mreža!]; h70 = 3. VPIS (1893, 1912 → 1915) — VRZEL 3 LETA; botra **Miko Šegina? [~]** (½ zemlj.) + **Ana Brinec**, ros. žena; babica **Barbara Adlešič**; podpis Kapl. Bitnar; marg.: mož umrl 4.1.1994 [~ — faza-1 »oče« ZAVRŽENO: nemogoče za očeta r. 1883] + umrla 23.6.2004 (MKU MO Novo mesto 1.2004, str. 220, zap. št. 312) + poročena 13.2.1939",
    whatEn: "baptized Barbara (Mar 16/17; the personal ID **1603915505171** — 5× clear, the phase-1 »5505141« CORRECTED) — father **Matija Brinec**, half smallholder, born Jul 15, 1883 [~ — 4×; the phase-1 »1888« CORRECTED], mother **Marija (1877), née PEZDIREC**, b. Jan 30? [~ — the phase-1 »Perdivec« CORRECTED (3.2×) — the PEZDIREC network!]; h70 = the 3rd ENTRY (1893, 1912 → 1915) — a 3-YEAR GAP; godparents **Miko Šegina? [~]** (half smallholder) + **Ana Brinec**, the ros. wife; midwife **Barbara Adlešič**; signature Kapl. Bitnar; the marginal notes: the husband died Jan 4, 1994 [~ — the phase-1 »father« REJECTED: impossible for a father born 1883] + she died Jun 23, 2004 (MKU MO Novo mesto 1.2004, p. 220, no. 312) + married Feb 13, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "78",
    bookSignature: "04105",
    year: 1915,
    scan: 272,
    page: 227,
    whatSi: "krščena Jožefa (‡ 10.9.1917 — d27 3.5× jasno; **P109 lead »1916« ZAVRŽENO!**) (22./23. 3.) — oče **Anton Ložar** [~ Ložar/Lozar], ½ zemlj., roj. 5/5 890 (por. 16.1.1912), mati **Barbara roj. Križan** (r. 20/6 1889); h78 = 3. VPIS (1887, 1888 → 1915); **VRZEL 27 LET = NOV REKORD vzorca!** (prej h53 16 let); botra **Janez Kambič** (½ zemlj.) + **Katar. Šapič**, ros. žena (faza-1 »Hatar.« = Katar.!); babica Marija Jakofčič; podpis Učak d.i. (svinčnik)",
    whatEn: "baptized Jožefa (died Sep 10, 1917 — d27 3.5× clear; **the P109 lead »1916« REJECTED!**) (Mar 22/23) — father **Anton Ložar** [~ Ložar/Lozar], half smallholder, born May 5, 1890 (m. Jan 16, 1912), mother **Barbara née Križan** (b. Jun 20, 1889); h78 = the 3rd ENTRY (1887, 1888 → 1915); **a 27-YEAR GAP = the NEW RECORD of the sample!** (previously h53 16 years); godparents **Janez Kambič** (half smallholder) + **Katar. Šapič**, the ros. wife (the phase-1 »Hatar.« = Katar.!); midwife Marija Jakofčič; signature Učak d.i. (pencil)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "13",
    bookSignature: "04105",
    year: 1915,
    scan: 277,
    page: 231,
    whatSi: "krščena Ana (18./19. 7.) — oče **Matija JAKOBČIČ** [~ — faza-1 »Jaklič/Jakličič« POPRAVLJENO (4× d29)], ½ zemljak, roj. 17.8. 1856 (star 59 ob krsti! [~]), mati **Marija roj. Jakofčič** (24.2.1877; por. 28.1.1910); h13 = 8. VPIS (1885–1913) — VRZEL 2 LETI; botra **Matija Perdivec** (½ zemlj.) + **Katarina Jakofčič**, ½ zemljaka žena; babica Marija Jakofčič; podpis V. Valerijan Učak",
    whatEn: "baptized Ana (Jul 18/19) — father **Matija JAKOBČIČ** [~ — the phase-1 »Jaklič/Jakličič« CORRECTED (4× d29)], half smallholder, born Aug 17, 1856 (aged 59 at the baptism! [~]), mother **Marija née Jakofčič** (Feb 24, 1877; m. Jan 28, 1910); h13 = the 8th ENTRY (1885–1913) — a 2-YEAR GAP; godparents **Matija Perdivec** (half smallholder) + **Katarina Jakofčič**, the half-smallholder's wife; midwife Marija Jakofčič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "40",
    bookSignature: "04105",
    year: 1915,
    scan: 280,
    page: 234,
    whatSi: "krščena Marija Ana († 23.6.1943 — 2. svetovna doba; marg. »+ 23. 6. 1943«) (26./28. 10.; trak čez vrstico, vendar berljivo 3×) — oče **Nikolaj Pezdirec**, posestnik ½ z., roj. 28.11. 1874 (por. 16.11. 1907), mati **Rosa roj. Tuvan** (r. 29.1. 1880); h40 = 6. VPIS (1897–1912) — VRZEL 3 LETA; botra **Matija Urh**, posest. + **Ana Pezdirec**, posest žena; babica Marija Jakofčič, n.zp.; podpis V. Valerijan Učak d.i.",
    whatEn: "baptized Marija Ana (died Jun 23, 1943 — the WWII era; the marginal note »+ 23. 6. 1943«) (Oct 26/28; a strip across the row, yet legible 3×) — father **Nikolaj Pezdirec**, landowner half, born Nov 28, 1874 (m. Nov 16, 1907), mother **Rosa née Tuvan** (b. Jan 29, 1880); h40 = the 6th ENTRY (1897–1912) — a 3-YEAR GAP; godparents **Matija Urh**, landowner + **Ana Pezdirec**, the landowner's wife; midwife Marija Jakofčič, n.zp.; signature V. Valerijan Učak d.i.",
    status: "DOCUMENTED",
  },
  {
    houseNo: "32",
    bookSignature: "04105",
    year: 1915,
    scan: 280,
    page: 234,
    whatSi: "krščena Marija (2./3. 11.; EMŠO ž. **0211915505717** — 4× jasno) — oče **Matija Štravs**, posest ½ z., roj. 1.I. 1862 (por. 8.II. 1904), mati **Marjeta roj. Šimec** (r. 22.2. 1875); h32 = 11. VPIS (1889–1909 — največ med hišami 1915!) — VRZEL 6 LET; botra **Mihael Jakofčič**, posestnik? + **Barbara Štrucelj**, pos. žena (**ŠTRUCELJ mreža!**); babica Marija Jakofčič, nj.; podpis V. Valerijan Učak d.i.; marg.: umrla 31.1.1989 Novo mesto (MKU 1.1989, str. 112, zap. št. 66) + poročena 19.2.1939",
    whatEn: "baptized Marija (Nov 2/3; the personal ID **0211915505717** — 4× clear) — father **Matija Štravs**, landowner half, born Jan 1, 1862 (m. Feb 8, 1904), mother **Marjeta née Šimec** (b. Feb 22, 1875); h32 = the 11th ENTRY (1889–1909 — the most among the 1915 houses!) — a 6-YEAR GAP; godparents **Mihael Jakofčič**, landowner? + **Barbara Štrucelj**, the pos. wife (**the ŠTRUCELJ network!**); midwife Marija Jakofčič, nj.; signature V. Valerijan Učak d.i.; the marginal notes: she died Jan 31, 1989 Novo mesto (MKU 1.1989, p. 112, no. 66) + married Feb 19, 1939",
    status: "DOCUMENTED",
  },
  {
    houseNo: "46",
    bookSignature: "04105",
    year: 1915,
    scan: 281,
    page: 235,
    whatSi: "krščen Martin (8./8. 11.) — oče **Anton Brodarič**, posest. ½ zem., roj. 14/11-1859 (por. 7/11-1904), mati **Katarina roj. Milek** (1./8.-1876; **MILEK — cf. P108 h34/h65!**); h46 = 10. VPIS (1893–1913) — VRZEL 2 LETI; botra **Nikolaj Želejko? [~]**, posr. **župan** (2. župan-botra vzorca — cf. r40 Jakob Stipanič!) + **Ana Pezdirec**, posed žena; babica Marija Jakofčič, n.zp.; podpis Kapl. Bitnar; VELIKA modra marg.: poroki 19.1.1952 + 19.3.1961 (Karlovci) + **zakonska zveza RAZVELJAVLJENA s sodbo št. K 757/65-10 (2.12.1965, Karlovci — prvi razveljavljen zakon vzorca!)** + umrl 15.5.1992 Karlovci [~]",
    whatEn: "baptized Martin (Nov 8/8) — father **Anton Brodarič**, landowner half, born Nov 14, 1859 (m. Nov 7, 1904), mother **Katarina née Milek** (Aug 1, 1876; **MILEK — cf. P108 h34/h65!**); h46 = the 10th ENTRY (1893–1913) — a 2-YEAR GAP; godparents **Nikolaj Želejko? [~]**, posr. **mayor** (the 2nd mayor-godparent of the sample — cf. r40 Jakob Stipanič!) + **Ana Pezdirec**, the posed wife; midwife Marija Jakofčič, n.zp.; signature Kapl. Bitnar; a LARGE blue marginal note: marriages Jan 19, 1952 + Mar 19, 1961 (Karlovac) + **the marriage ANNULLED by the court no. K 757/65-10 (Dec 2, 1965, Karlovac — the first annulled marriage of the sample!)** + he died May 15, 1992 Karlovac [~]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "9",
    bookSignature: "04105",
    year: 1915,
    scan: 281,
    page: 235,
    whatSi: "krščena Neža († 23.12.1916 — dojenček; marg. »+ 23/12 1916«) (15./16. 11.) — oče **Oswald JAKOBČIČ** [~ — faza-1 »Jakobeč« POPRAVLJENO; cf. h13 Matija Jakobčič — familija Jakobčič v Gribljih!], posest ½ z., roj. 3. aug 1889 (star 26; por. 6.2.1911), mati **Terezija roj. Klepec** (r. 21.6. 1890; faza-1 »20.6« POPRAVLJENO); h9 = 4. VPIS (1896, 1900, 1913 → 1915) — VRZEL 2 LETI; botra **Jurij Klepec**, posest. + **Marija Žunič**, posest žena; babica **Marija Jakobčič**, neizp. (verj. očetova mati); podpis V. Valerijan Učak d.i.; ime OSWALD = nemško-modno (cf. r21 Vilhelm + r49 Emil Filip Leopold)",
    whatEn: "baptized Neža (died Dec 23, 1916 — an infant; the marginal note »+ 23/12 1916«) (Nov 15/16) — father **Oswald JAKOBČIČ** [~ — the phase-1 »Jakobeč« CORRECTED; cf. h13 Matija Jakobčič — the Jakobčič family in Griblje!], landowner half, born Aug 3, 1889 (aged 26; m. Feb 6, 1911), mother **Terezija née Klepec** (b. Jun 21, 1890; the phase-1 »Jun 20« CORRECTED); h9 = the 4th ENTRY (1896, 1900, 1913 → 1915) — a 2-YEAR GAP; godparents **Jurij Klepec**, landowner + **Marija Žunič**, the landowner's wife; midwife **Marija Jakobčič**, neizp. (probably the father's mother); signature V. Valerijan Učak d.i.; the name OSWALD = German-fashion (cf. r21 Vilhelm + r49 Emil Filip Leopold)",
    status: "DOCUMENTED",
  },
  {
    houseNo: "22",
    bookSignature: "04105",
    year: 1915,
    scan: 282,
    page: 236,
    whatSi: "krščen Nikolaj (25./26. 11.; EMŠO ž. **2511915500090** — 4× jasno) — oče **Nikolaj Milek**, posest ½ z., roj. 13.11. 1869 (por. 12.2. 1900; **MILEK ×2 v 1915 — cf. h46 mati Milek!**), mati **Ana roj. Črnič** (2.8. 1875); h22 = 7. VPIS (1899–1912) — VRZEL 3 LETA; botra **Nikolaj Požek**, p. ½ z. + **Ana Črnič**, posest žena; babica Marija Jakofčič, neizž.; podpis Valerijan Učak d.i.; marg.: sklenil zakonsko zvezo 15.8.1945 Črnomelj (RNK 1.1945 zap. št. 84) + umrl 24.4.1992 Črnomelj [faza-1 »1932« POPRAVLJENO: nemogoče po poroki 1945]",
    whatEn: "baptized Nikolaj (Nov 25/26; the personal ID **2511915500090** — 4× clear) — father **Nikolaj Milek**, landowner half, born Nov 13, 1869 (m. Feb 12, 1900; **MILEK ×2 in 1915 — cf. h46 the mother Milek!**), mother **Ana née Črnič** (Aug 2, 1875); h22 = the 7th ENTRY (1899–1912) — a 3-YEAR GAP; godparents **Nikolaj Požek**, p. ½ z. + **Ana Črnič**, the landowner's wife; midwife Marija Jakofčič, neizž.; signature Valerijan Učak d.i.; the marginal notes: he married Aug 15, 1945 Črnomelj (RNK 1.1945 no. 84) + he died Apr 24, 1992 Črnomelj [the phase-1 »1932« CORRECTED: impossible after the 1945 marriage]",
    status: "DOCUMENTED",
  },
  {
    houseNo: "53",
    bookSignature: "04105",
    year: 1915,
    scan: 282,
    page: 236,
    whatSi: "krščen Janez (18./18. 12.; EMŠO ž. **1812915500054** — 4× jasno) — oče **Jure Dragos**, posest ½ z., roj. 23.4.1888 (por. 21/4-1913; **DRAGOS — cf. P107 r47 + P109 r78 mrtvorojen Dragos × Bahorič!**), mati **Marjeta Pezdirc** (14.8.1891); h53 = 6. VPIS (1891–1914); **ZAPORED 2. LETO** (1914 r17!); botra **Matija Štravs**, posest. + **Katarina Pezdirc**, posest žena; babica Marija Jakofčič, neizpr.; podpis Kapl. Bitnar; marg.: poročen 5.3.1947 s Petjak Marijo? [~] + umrl 2.10.1958 (MKU NO Novo mesto 1.1958, str. 251, zap. št. 2345?) + umrla 5.12.1955 + **odločba (Ljubljana) 16.3.1948 postala pravnomočna 16.3.1948 — Gradac 4.6.1948 matičar, nam. [~ — vsebina dvom: posvojitev/rodovna pravica?]**",
    whatEn: "baptized Janez (Dec 18/18; the personal ID **1812915500054** — 4× clear) — father **Jure Dragos**, landowner half, born Apr 23, 1888 (m. Apr 21, 1913; **DRAGOS — cf. P107 r47 + P109 r78 the stillborn Dragos × Bahorič!**), mother **Marjeta Pezdirc** (Aug 14, 1891); h53 = the 6th ENTRY (1891–1914); **CONSECUTIVE the 2nd YEAR** (1914 r17!); godparents **Matija Štravs**, landowner + **Katarina Pezdirc**, the landowner's wife; midwife Marija Jakofčič, neizpr.; signature Kapl. Bitnar; the marginal notes: married Mar 5, 1947 to Petjak Marija? [~] + died Oct 2, 1958 (MKU NO Novo mesto 1.1958, p. 251, no. 2345?) + she died Dec 5, 1955 + **the decision (Ljubljana) of Mar 16, 1948 became final on Mar 16, 1948 — Gradac Jun 4, 1948 the deputy registrar [~ — the content unclear: adoption/ancestral right?]**",
    status: "DOCUMENTED",
  },
'''

with io.open(PATH, encoding="utf-8") as f:
    src = f.read()

marker = "    status: \"DOCUMENTED\",\n  },\n];"
idx = src.rfind(marker)
assert idx != -1, "marker not found"
insert_at = idx + len("    status: \"DOCUMENTED\",\n  },\n")
new_src = src[:insert_at] + BLOCKS + src[insert_at:]
with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(new_src)
print("vstavljeno OK; blokov 1915 = 11")
