# P259 — VLM-DUEL-VALIDACIJA (2026-11-12, kvota obnovljena 496 → porabljeno 11)

## Metoda
Nevtralni VLM klici (BREZ pričakovanih odgovorov v pozivu) na 10 duel-kompozitov iz
`p259-work/duels/` → `p259-work/duel-vals/*.json`, primerjava z integriranimi odgovori
(`p259_duelcmp.py`). Nato tiebreak: sveži ×6/×10 izrezi (`p259-work/tiebreak/`) + 2 nevtralna
VLM klica + agent-vizija (Read) z DIGIT-SHAPE referencami iz ISTEGA skena (r1/r3/r7 = znane '2').

## Rezultati — 9/10 duelov POTRJENO, 1 POPRAVEK, 1 dvom razrešen

| duel | verdikt | dokaz |
|---|---|---|
| s11_dates (6.×8 + 13.×5) | ✓ POTRJENO | duelval 7/8 + 4/5; datcol/pass1/agent-vizija 1:1 |
| s11_r2_gosling (PESDIRZ h53, BRING h24) | ✓ POTRJENO | duelval: 'pesdirz' 1:1, h53 1:1, h24 1:1, 'brinz'≈BRING (Kurrent z/g) |
| s12_dates r7 (22. Jän RESTART) | ✓ POTRJENO | duelval 1:1 '22. Jän. 1834' + rob-'2.' ✓ |
| s12_dates r9–r12 (29. Jän ×4) | ✓ POTRJENO | duelval 4/4 + robovne št. 4/5/6/7 ✓ |
| s13_dates r1–r7 (5. Febr ×7) | ✓ POTRJENO | duelval r1–r6 '5.' + r7 dito; datcol 1:1; agent-vizija |
| s13_r1 (5. Febr, rob 8) | ✓ POTRJENO | duelval '5. Feb.' + rob '8' + imena-garble ujemanje |
| s13_r6_vrh (VRH h68, h51) | ✓ POTRJENO | census_L13 'Marcus Vrh, Griblje 68' 1:1 (neodvisen vir pred duelom!) + agent-vizija; hint-'58' ZAVRŽEN 2:0 |
| s13_r11_marentic (10. Febr, Dobravlje 29) | ✓ POTRJENO | duelval '10. Hornung' + 'MARENTICH' + **h29** 1:1 (+ census_L13 'Dobravič 29'!) — h29 je bil xOpen → ZDAJ potrjen |
| s12_r5 (SCHMIG h60, 19. Oct) | ✓ POTRJENO (2. potrditev) | prvi VLM-presek (a48dc27) + tiebreak ×10: digit '9' = zaprt lok + rep POD črto, ≠ '2' flat-base (r1/r3/r7 reference); census '19.'; datcol '10.'/pass1 '26.' = misread |
| **s12 r1–r2 datum** | ✗→POPRAVEK 19.→**12. Febr ×2** | r1 polni zapis '12. Feb. 1833.' + r2 '12. att°' (×6 agent-vizija, digit '2' flat-base = r3/r7 reference); 4 izvora: census '12. Febr. 1833' + pass1 '12. Feb' + duelval '12. Feb' + urkunda-celica '...12. Febr 1833'; datcol '19.' = MISREAD 1:4 |

## Ključne ugotovitve
1. **m20/m21 = 12. Febr 1833 ×2** (ne 19.!) — ANOMALIJA razložena: 12. Febr pride ZA s11-tail
   13. Febr ×5 → dopisani zamik (urkunda-celica omenja licence '2. Febr + 12. Febr 1833' — zaporedje dokazil).
2. **m24 = 19. Oct 1833 POTRJEN** — '9' ima podpis rep pod črto, '2' (r1/r3/r7) nima; rob-'25.' =
   svinčnik, opuščeno zaporedno številčenje pred restartom rob-1 (27. Nov).
3. **s13_r6 hiša 68** zdaj 2 neodvisna vira (census + agent-vizija) — hint '58' definitivno zavrnjen.
4. **s13_r11 nevesta-hiša 29** (Dobravlje) — prej xOpen, zdaj VLM + census 1:1.
5. datcol-odkloni (r1 '19.', r5 '10.') so bili sistematski misreads pri dvomljivih Kurrent številkah —
   digital-shape analiza na ×10 je odločilna metoda (najti referenčne števke v ISTEM skenu!).

## Kvota
11 VLM klicov (9 duel-val + 2 tiebreak) + 4 agent-vizija Read (brez kvote). Ostalo ~485.

## Spremembe v korpusu
- `src/data/atlas/parish.ts` (P259 header): m20/m21 19.→12. Febr ×2 + evidence; m24 19.-Oct POTRJEN note.
- `src/data/atlas/parish-marriage-early.ts` (STRUKTURA si+en): isto.
- `scripts/tmp/module-p259.txt`: isto.
- `p259-work/s12_r1.json`: datum 12. Feb 1833 + razlaga-validacija.
- QA po popravku: 253/253 (brez spremembe števca — popravki so v komentar-tekstih, ne v števcih).
