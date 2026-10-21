# P124 — poročna knjiga 04455, polno leto 1895 (issue #18)

**Skripta:** `scripts/p124_parish_marriage_1895.py` (I1–I11, `--check` = PASS/FAIL + exit code; `--live` = HTTP preverjanje Matricule)
**Dokaz:** `research/issue17/parish-marriage-1895.json`
**Skeni:** 94–96 == **Pag. 93–95** (Pag. == sken − 1, **10. potrditev**; velja v 61–96) — prenešeni v `/home/z/.p123tmp/` (LANDSCAPE 2510–2521×1800)

## FAZA 1 — okvir (POTRJEN)
- **VELIKA GLAVA »Trauungs=Buch« + rokopisno »1895« na s94** (zoom hdr1895; cikel velike glave: 1887 s66 + 1890 s77 + 1892 s84 + 1893 s87 + 1894 s91 + **1895 s94**).
- **16 vpisov** (1886:7 → 1887:21 → 1888:20 → 1889:10 → 1890:16 → 1891:18 → 1892:15 → 1893:20 → 1894:15 → **1895:16**; razpored **6+5+5**):
  - s94 = Pag. 93: v1–v6 · s95 = Pag. 94: v7–v11 · s96 = Pag. 95: v12–v16
- Meje vrstic: s94 po geometriji s91 (isti tiskani formular); s95/s96 re-kalibrirane z datum-zoomi (v8 = visoka vrstica 490–985; v13 = kratka 575–700; v16 = 1330–1780).
- Ob robu s96: tiskar »Laibach. Druck u. Verlag v. Möttlig.« (navpično).

## FAZA 2 — transkripcija (16/16 OBOJESTRANSKO)
32 row-crops (L/R ×2 LANCZOS) + 65 zoomov (`zoom_124.py`, `zoom_124b.py`) + 30+ 8×/10×/12× mikro-zoomov (`zoom_124c.py` + ročni popravki). Datumne celice vseh 16 vrstic prebrane v 4× zoomu (kronologija brez izjem).

## NOVELE
- **★ VOJSKA — 1. ČASTNIK linije (v15):** ženin **Herr Andreas Stal, OBERLEUTNANT [~]**, Metlika 38, 40, × **Francisca Logar, hči Offizierja [~]**, Metlika 65, **18**; priča **Josef Avanzo, k.k. HAUPTMANN** + Richard Megušar [~], k.k. podučitelj [~]; Befunde: zglašnica **mestne občine Metlika** št: 150 + **Garnisons-Propstei zū Metlika** 17.6.1895 + latinsko »testes delegata co[mm]andi« [~]. (P123 je odkril vojak Inf.-Reg. №267 — P124 korak naprej: častnik + vojaška kuracija!)
- **★ 1. HRVAŠKI dokumenti linije (v6):** ženin **Peter Gerdinovac**, Krasinec 1 — »zi Pämbig nach Kalchs **in Croalien**« [~]; smrtni list dekanate v Lipniku [~] od 16/2. 95 + »svjedovbe« [~] + proglasnica občine Griblje **Broj 485** (hrvaško »Broj«!).
- **★ POPRAVEK STAROSTI 40→54 (v6):** prečrtana 40, popravljena **54** — vdovec (smrtni list 1. žene!); 2. primer popravka v liniji (P122 v5 »1«).
- **★ DISPENS-REKORD ×4:** v7 №504 (3. stopnja krvnega sorodstva, Ordinariat Laibach 13.2.) + v8 №613 (2. stopnja svarstva, Ordinariat 22.2.) + v12 **Ž/L: 4994** (»Wittwenschaft« [~] — anomalija: oba ledig!; Bez. Gft Črnomelj 5/6. — ~2 tedna PO poroki) + v16 (3. [u 2.? ~] lineae collateralis).
- **★ 2. LANDSREGIERUNG linije (v8):** Beglaubigung k.k. Landesregierung Laibach **№: 181** od 6.2.1895 (cf. P123 v11 Ž8667 9/9.1894!).
- **★ »Möttling« = nemško ime METLIKA:** k.k. Bez. Ger. **Möttling** ×4 (v2/v8/v9/v14) — lingvistična identifikacija kraja; istoimenski tiskar v Laibachu.
- **★ HOMONIMI ×2 para:** **Marcus Perdinec** (v11: f. Marcus, 34, ½ Griblar × Catharina Zugelj ≠ P123 v3: f. Michaël, 33, ¼ Gribler × Margareth Perdinec — isto hiša 27!) + **Johann Starasinič** (v8: f. Johann, 24, Krasinec 32 ≠ v14: f. Michaël, 32, Krasinec 51).
- **★ DVA PRIČA ISTO IME (v4):** Peter Jakofčič ×2 (} ½ gbl) — vzorec P123 v5 (dva Peter Perdinec Valur/Pofn).
- **★ 3 POROKE 11.2. + 3 POROKE 19.5. + 2 POROKI 26.5.** = 8 od 16 vpisov v treh dnevih (11.2. = 2. največ za rekordom P122 — 7 porok 6.2.1893!).
- **GRIBLJE: 3 poroke / 3 hiše** — v10 **h16 NOVA** (Anton Brodarič × Anna Harasinič — oče in mati isti priimek!) + v11 h27 **3. poročni dokaz** (Marcus Perdinec homonim!) + v13 **h52 NOVA — v PT-luknji 41–60!** (Mathias Perdinec × Anna Jakobič) → parish.ts +3 bloka → **bloki 04455 = 49; vitals 563 → 566; p80 hiše 47 → 48; PT luknja 9 → 10 (+h52)**.
- **ZUGELJ ×3:** v8 nevesta »geb. Zugelj« (oče Mathias ½ Griblar) + v11 nevesta Catharina (oče Michaël ¼ Griblar) — cf. P123 v14.
- **MAYD ×2:** v4 Catharina Čermelj »Mayd« + v6 Anna Černič »Priš [~] Magd« — P118 Rosetta → P123 v5 → P124.
- **Großjährigkeits-Erklärung ×3** (v2, v14, v8 [~]): mladoletne neveste 17 (v3!), 20, 23.
- **formula »in Ungarn ward obigen šti. Närnk« ×4** (v1/v3/v5/v13, [~]) — morda neveste na služenju v Ogrski (Mayd-kontekst); »Närnk« [~] neslovljeno.
- **KRALJ ×6 + MARENTIČ ×5 + JAKŠA ×5 + PERDINEC 5. leto.**
- duhovnik **Jos. Rauy 16/16** (podpis »M.!« ×7) — 3. leto zapored monopol.
- status-neznanki [~] ×15+ (Otljuka, Krivo glavce, Fučkovci, Dragoše, Kloster, Njofan, Gjofan, Aleffon, Žugffan, Priš, beylöffers tauffnn, Brsitzon Jamstki, …) — POŠTENOST disciplina.

## Verifikacije
- `python3 scripts/p124_parish_marriage_1895.py --check` → I1–I10 PASS (brez omrežja); `--live` = I11 (Matricula HTTP).
- Regresije: p114–p123 veriga + p80/p81/p83 + `/api/qa` 124 → **125/125** (qa-p124 = 125. kontrola).
