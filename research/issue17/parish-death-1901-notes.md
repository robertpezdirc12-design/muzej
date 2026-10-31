# P167 — MRLIŠKA knjiga 04894, leto 1901 (16. polno leto mrliške linije)

## Metoda
- **FETCH**: s81–s85 (5/5 ✓, 604–628 KB) + s80-reuse (P166) → /tmp/p167
- **VLM celostansko**: 5/5 ✓ 0 FAIL (glm-5v-turbo; serije ≤2 foreground — P158-lekcija!)
  - s81: 12 vrstic, Griblje ×4 · s82: 12 ×1 · s83: 12 ×0 · s84: 12 ×2 · s85: 12 ×1 (1901) + 1902-dno
- **ROWS — tri-metoda-lekcija**:
  - v1 (COV=0.010 zap-projekcija COM): 9–12 vrstic/sken — **BUG: linije-v-projekciji** (opening (81,1) odstrani navpične, horizontalne ostanejo → COM = mešano!)
  - v2 (linije-opening-1×30 + celice): linije-vrzeli @ rotiranih skenih
  - v3 (**končna**): linije-1×30 + interpolacija (3 prehoda, n=2, gap>1.6×med) + cifre-BREZ-linij (clean & ~dilate(hlines)) + preslikava cifra→celica (cifra @ vrh celice!)
  - **NASLOV-'Zaporedna štev.'-ostanek** @s82/s84/s85 y~230–240 = false-cifra → izključen z yc<330 (P162-TOP_ZONE-lekcija!)
  - **rows_final**: roko-potrjen dict (P166-vzor): s80 (P166-reuse) + 5×12 + s85 (55+meja+1902:1–10)
- **diag-PNG agent-oči**: 5/5 ✓ — 12/12 črt na vrsticah (s81/s82/s83/s84/s85!)
- **zapcol rezine** (×2.5, 3 segmente/sken): pikselska potrditev cifr — '55' @s85 (VLM-'65' = 5/6-zmeda!), '7/8/9' @s81-seg0 (VLM-'4' = γ→7!)
- **kompozit-forenzika**: 6 kompozitov (42 izrezov: 10 Griblje-trakov ×2.2 + 5 mejnih + 27 celic ×3.0) × 1 VLM-klic = **ekonomija-7×** (vzor P162-primerjava-cifer!)

## 18. POTRDITEV okvira (stran == sken − 1)
s80=79 … s85=84 (47.–52. potrditev) — s85-dno = **meja 1901/02**:
'1902.' VELIKA + DVOJNI podčrtaj na PRAZNI vrsti + Januarj-INLINE + restart zap 1
= **5. STIL MEJE 9. POTRDITEV** (P166-lead-'[~ s85+?]' POTRJEN!)

## Rezultat: 1901 = 55 vrstic / 10 Griblje / 10 hiš (vse različne!)
- rast vrstic: 61→55 (pad) · rast Griblje: 8→10
- hiše: 36, 48, 60, 28, 81, 29, 33, 35, 64, 34
- **h28 = 1. MRLIŠKI VPIS KADARKOLI = 25. PT-vezni dokaz** (IZVEN 41–60!)
- **h35 = 7. mrliški vpis = NOVI REKORD linije** (cf. h30-6-P164!)
- h81 = 2. leto ZAPORED (1900 + 1901) · h36/h60/h64 = 5. vpis · h48-3. · h29-4. · h33-3. · h34-3.

## Drame in mreže
- **★★★ KRIŽAN-×2-1901**: h36-Ana-76-vdova (Jan) + h35-Janez-63-vdovec (Okt) = 2 hiši-2 spola-v-1-LETU!
- **★★★ HLOBUČAR-×2-v-2-MESECIH-RAZREŠEN**: Marija-h47-30.12.1900 (P166) + Matija-h48-16.1.1901 (P167) = **17 dni** na sosednjih hišah — P166-lead 100%!
- **MILEK-mreža**: h22/h65/h82 + h29-1901 = 4 hiše-10 vpisov
- **BRINEC-mreža-#6**: h28-1901-Marija-4-let
- **PAPIČ-mreža**: h33-1901-Martin-4-mes
- **JAKOBČIČ-mreža**: h64-1901-Janez-42 — bolezen 'Voz' [~ pade-zadušil = NESREČA-kandidat]
- **h64** = 5. vpis (1896-×2 + 1898-×2 + 1901 = hiša-×2-v-2-letih-×2!)

## Duhovniki 1901
- **KUT'NEK-DOMINANTA** (6× Griblje-Jan–Mar; cf. P166-Sep–Dec-12×) → Rauq (Apr) → Škurmelj[~Dostal] (Okt) → **'Dostal' = NOVI-KANDIDAT #11 [~]** (Dec + meja-K-'Laur. Dostál' — podpisi-K-'Češarek' = KONFLIKT-ne-razrešen!)

## MAX-ZOOM forenzika — 18. potrditev (3 ne-razrešeni konflikti → [~])
- zap50: 'Križan' (kompozit-ime-×3.0) vs 'Kešran' (griblje-B) → **[~]** — K-r-glif-nejasen
- zap55: 'Rampič' (griblje-B) vs 'Mramlič' (meja-K) → **[~]** — R/M-glif
- zap15-duhovnik: 'Kukljaš' vs 'Kut'nek' → **[~]**
- VLM-vas-0-napak (10/10 Griblje @kompozit-vas-hisna!) — 1. leto BREZ A2-vas-napake odkar P161!
- γ→7 lekcija: 9.–10. potrditev (s81-'zap4'→7 + s85-'zap65'→55)!

## Demografija Griblje-1901
- starosti: 76, 65, 8, 4, 8-mes, 54, 4-mes, 63, 42, 19 — otroška umrljivost 40% (4/10)
- bolezni: Božjast-×3, Jetika-×2, Marbmil[~], Živce[?], Prehlajenje[~], Voz[~], Pljučnica
- meseci: Jan3 · Feb1 · Mar2 · Apr1 · Okt2 · Dec1 = 10
- razpon: 4 mesece (h33) → 76 let (h36)

## P168-lead
mrliška 1902: s85-dno-restart zap1–10 ŽE prebrani (VLM-s85!) + s86 (zap11–22?) + s87+; meja 1902/03 [~ s90+?]
