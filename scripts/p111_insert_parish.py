#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P111 — vstavi 6 blokov 1916 v HOUSE_VITALS (parish.ts) pred zaključni '];'."""
import io

PATH = "src/data/atlas/parish.ts"

BLOCKS = r'''  {
    houseNo: "34",
    bookSignature: "04105",
    year: 1916,
    scan: 285,
    page: 239,
    whatSi: "krščena Barbara († 26.8.1917 — dojenček ~17 mesecev; marg. »† 26.8.1917«) (27./28. 2.) — oče **Nikolaj Silak? [~ Bilak?]**, posest ½ ž., roj. 8.12.1877, mati **Katarina roj. Klobučar** (23.4.1877); h34 = 10. VPIS (1887–1913) — VRZEL 3 LETA; **1. GRIBLJE vrstica 1916!**; mesec glava »february«; botra **Matija Muh** (½ ž. posestnik) + **Katarina Hrižan** (posest žena); babica Bara Adlešič; podpis V. Valerijan Učak",
    whatEn: "baptized Barbara (died Aug 26, 1917 — an infant ~17 months; marg. »† 26.8.1917«) (Feb 27/28) — father **Nikolaj Silak? [~ Bilak?]**, half smallholder, born Dec 8, 1877, mother **Katarina née Klobučar** (Apr 23, 1877); h34 = the 10th ENTRY (1887–1913) — a 3-YEAR GAP; **the 1st GRIBLJE row of 1916!**; the month heading »february«; godparents **Matija Muh** + **Katarina Hrižan**; midwife Bara Adlešič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "12",
    bookSignature: "04105",
    year: 1916,
    scan: 286,
    page: 240,
    whatSi: "krščen Vincencij († ~3 leta; marg. »+ 8/9 1919« — vojna!) (28./29. 4.) — oče **Ivan Dragos? [~]**, posestnik ½ ž., roj. 5.7.1867, mati **Barbara roj. Grintkenič? [~]** (11.12.1871); h12 = 14. VPIS (1892–1912) — VRZEL 4 LETA; **2. GRIBLJE vrstica 1916!**; botra **Štefk Matija? [~]** + **Marija TOTER** (posest samska hči — mreža cf. P109 r62!); babica Bara Adlešič",
    whatEn: "baptized Vincencij (died ~3 years old; marg. »+ 8/9 1919« — the war!) (Apr 28/29) — father **Ivan Dragos? [~]**, half-estate farmer, born Jul 5, 1867, mother **Barbara née Grintkenič? [~]** (Dec 11, 1871); h12 = the 14th ENTRY (1892–1912) — a 4-YEAR GAP; **the 2nd GRIBLJE row of 1916!**; godparents **Štefk Matija? [~]** + **Marija TOTER** (the estate's unmarried daughter); midwife Bara Adlešič",
    status: "DOCUMENTED",
  },
  {
    houseNo: "82",
    bookSignature: "04105",
    year: 1916,
    scan: 287,
    page: 241,
    whatSi: "krščena Ana († ~3 leta; marg. »+ 8/9 1919« — ista † kot h12 r21!) (16./16. 5.; mesec glava »majnik« = pisarska idiosinkrazija za maj — NOVELA!) — oče **Peter Vrebec? [~]**, **TESARSKI MOJ.** (nov poklic v Gribljih!), roj. 16.8.1882, mati **Terezija roj. Muc** (12.10.1887); **h82 = 1. VPIS V VSEH TREH KNJIGAH = NOVA HIŠA vzorca!** (PT set jo že pokriva); **3. GRIBLJE vrstica 1916!**; prečrtan pisarjev false start v vas koloni; hiša 82 ZOOM 4× jasno (dvom 82/32 ZAVRŽENO); botra **Ožbald Jakofčič? [~]** + **Terezija Jakofčič**; babica Marija Jakofčič; podpis V. Valerijan Učak",
    whatEn: "baptized Ana (died ~3 years old; marg. »+ 8/9 1919« — the same † as h12 r21!) (May 16/16; the month heading »majnik« = the scribe's idiosyncrasy for May — a NOVELTY!) — father **Peter Vrebec? [~]**, a **CARPENTER MASTER** (a new trade in Griblje!), born Aug 16, 1882, mother **Terezija née Muc** (Oct 12, 1887); **h82 = the 1st ENTRY IN ALL THREE BOOKS = a NEW SAMPLE HOUSE!**; **the 3rd GRIBLJE row of 1916!**; a crossed-out scribe's false start in the village cell; house 82 ZOOM 4× clear; godparents **Ožbald Jakofčič? [~]** + **Terezija Jakofčič**; midwife Marija Jakofčič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "36",
    bookSignature: "04105",
    year: 1916,
    scan: 287,
    page: 241,
    whatSi: "krščen Anton (22./23. 5.; EMŠO ž. **2205916500023** — ZOOM 4.5× jasno → 22.5.1916 ✓) — oče **Janez Hrižan**, posest ½ ž., roj. 11.1.1861, mati **Katarina roj. Štincelj? [~]** (13.3.1874); h36 = 12. VPIS (1886–1913) — VRZEL 3 LETA; **4. GRIBLJE vrstica 1916!**; marg. »Umrl dne 19.12.**1983** v Gribljah, str. 126, 20/2-1984« (**faza-1 »1980« POPRAVLJENO!**) + »em poročen s Kambič? Katarino?« (2. poroka!); botra **Matija Pezdirc** (posestnik) + **Marjeta ŠTRAUS** (posest žena — cf. P107 h36 par!); babica Marija Jakofčič; podpis V. Valerijan Učak",
    whatEn: "baptized Anton (May 22/23; the personal ID **2205916500023** — ZOOM 4.5× clear → May 22, 1916 ✓) — father **Janez Hrižan**, half smallholder, born Jan 11, 1861, mother **Katarina née Štincelj? [~]** (Mar 13, 1874); h36 = the 12th ENTRY (1886–1913) — a 3-YEAR GAP; **the 4th GRIBLJE row of 1916!**; marg. »died Dec 19, **1983** in Griblje, p. 126, Feb 20, 1984« (**the phase-1 »1980« CORRECTED!**) + »remarried Katarina Kambič?« (a 2nd marriage!); godparents **Matija Pezdirc** + **Marjeta ŠTRAUS**; midwife Marija Jakofčič; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "88",
    bookSignature: "04105",
    year: 1916,
    scan: 287,
    page: 241,
    whatSi: "krščena Neža († dojenček ~1 teden!; marg. »+ 9/7 1916«) (21./23. 6.) — oče **Peter Brinec**, **bajtar**, roj. 28.9.1860, mati **Ana roj. Butala** (22.12.1879); **h88 ZAPORED 2. LETO: 1915 Ivana + 1916 Neža — ISTA starša (Brinec × Butala) + ISTI botri (Janez + Doroteja Brinec) — familija Brinec ×3!**; h88 = 4. VPIS (1904, 1910, 1915 → 1916) — VRZEL 1 LETO; **5. GRIBLJE vrstica 1916!**; datumi 21./23. ZOOM 4× jasno; babica Marija Muc; podpis V. Valerijan Učak",
    whatEn: "baptized Neža (died an infant ~1 week old!; marg. »+ 9/7 1916«) (Jun 21/23) — father **Peter Brinec**, a **cottager**, born Sep 28, 1860, mother **Ana née Butala** (Dec 22, 1879); **h88 CONSECUTIVE 2nd YEAR: 1915 Ivana + 1916 Neža — the SAME parents (Brinec × Butala) + the SAME godparents (Janez + Doroteja Brinec) — the Brinec family ×3!**; h88 = the 4th ENTRY (1904, 1910, 1915 → 1916) — a 1-YEAR GAP; **the 5th GRIBLJE row of 1916!**; midwife Marija Muc; signature V. Valerijan Učak",
    status: "DOCUMENTED",
  },
  {
    houseNo: "37",
    bookSignature: "04105",
    year: 1916,
    scan: 290,
    page: 244,
    whatSi: "**Marko MRTVOROJEN** (29. 12.; krsta kolona: **»krščena v sili in utero m.« = NUJNI KRST V MATERNICI — PRVI TAK SIGNAL V VZORCU!** ZOOM 4× — 3 vrstice) — oče **Marko Hubljan? [~]**, posestnik, roj. 30.7.1889, mati **Ivana roj. Hukan? [~]** (7.5.1893); **h37 = 3. VPIS (1895, 1897 → 1916) — VRZEL 19 LET = 2. najdaljša (po h78 27!) — in njen edini 1916 vpis je MRTVOROJEN!**; **6. GRIBLJE vrstica 1916!**; zap. št. 41 = zadnja (zaključna opomba »I številko 41 … v l. 1916«); botra/podpis PRAZNO; **DVOJNI MODEL r28+r29 (Krasinec 8 — 2 vrstici istega otroka!) vs. ENOVRSIČNI r41 = 2 protokola mrtvorojenih!**; babica Ana Marentič",
    whatEn: "**Marko STILLBORN** (Dec 29; the baptism column: **»baptized in emergency in utero matris« = an EMERGENCY IN-WOMB BAPTISM — the FIRST such signal in the sample!** ZOOM 4× — 3 lines) — father **Marko Hubljan? [~]**, farmer, born Jul 30, 1889, mother **Ivana née Hukan? [~]** (May 7, 1893); **h37 = the 3rd ENTRY (1895, 1897 → 1916) — a 19-YEAR GAP = the 2nd longest (after h78 27!) — and its only 1916 entry is STILLBORN!**; **the 6th GRIBLJE row of 1916!**; serial no. 41 = the last (the closing note »I številko 41 … in 1916«); godparents/signature EMPTY; **the DOUBLE model r28+r29 (Krasinec 8 — 2 rows for the same child!) vs. the SINGLE-ROW r41 = 2 stillbirth protocols!**; midwife Ana Marentič",
    status: "DOCUMENTED",
  },
'''

src = io.open(PATH, encoding="utf-8").read()
idx = src.rstrip().rfind("];")
assert idx > 0, "zaključni ]; ni najden"
new = src[:idx] + BLOCKS + src[idx:]
io.open(PATH, "w", encoding="utf-8", newline="\n").write(new)
print("VSTAVLJENIH 6 blokov 1916 v", PATH)
