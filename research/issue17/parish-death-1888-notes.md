# P154 — MRLIŠKA knjiga 04894, leto 1888 (delovne opombe)

Datum: 28. 10. 2026 · metoda: 9× celostansko + 116× VLM + 15× max-zoom + AI-vizualna forenzika

## Potek dela

1. **Prenos skenov** s14–s22 (inventar 256 ✓; s13–s17 že iz /tmp/p153) → `/tmp/p154/`.
2. **Celostanski VLM prehodi** (s13–s22, glm-5v-turbo, thinking-off) — ozadnji proces je umrl po s13;
   ključne strani prebrane ročno (half-res pogledi).
3. **SPOR MARKERJA**: celostanski VLM je s13-marker prebral »1 8 8 9«; P153 je zapisal »1 8 8 8«.
   → 3-segmentna max-zoom forenzika + AI-vizualni pregled cifrov: vse tri »8« = dve zaprti zanki,
   brez repa → **1888 POTRJEN** (anomalija A1 v dokazu).
4. **Kalibracija vrstic**: uniformna mreža NE deluje (dvovrstična imena!) → vizualna kalibracija
   po ser. številkah na vsakem skenu (s14: r6≈312 … r18≈1585; s21 posebej: 6+marker+6) +
   široki prekrivajoči trakovi (±75/+95 px) — vrstica vedno znotraj traku, identifikacija po ser. št.
5. **VLM pass-1** (58 trakov, 429 rate-limit → retry-ponovitev 58/58) + **pass-2 ciljirani**
   (ser. št. v pozivu). Primerjava pass-1/pass-2/celostansko → 15× max-zoom celic + AI-oke.
6. **AI-vizualna forenzika** (ključne celice): h83 (8+dvohrba 3 ≠ 68/88!), h25 (5-forma = s59-'35';
   6 ima visok ovinek), marker-1889 desna stran (9 z dolgim repom!), glave s14–s17 (»Leto 18ſſ..«),
   r102 vzrok (»Starost« ≠ 'Karast/Slabost'), r89 vzrok (»Difteritis in slabost — v sih Kruščen [?]«).

## Ključna spoznanja

- **29 Griblje-vpisov / 102 vrstic = rekord linije** (13 → 13 → 29; ×2.2).
- **2 porodni smrti** (r6 h72 'Na porodu' 3 dni po hči; r23 h83 'Vsled těžkega poroda') — 1. porodna
  umrljivost linije; h72 = mati + novorojenček v 4 dneh.
- **Željko/Želičo ×4 otroci** (h1 ×2 + h60 ×2 — sestri 'Strgjatinka' v 6 dneh).
- **h61 Požek ×3** (+ h21 Marija 38 = Požek ×5 v letu).
- **h83 + h47 = NOVI p80-hiši** (77 → 79); h25 [~ Kurrent 5/6].
- **'Starost' kot vzrok** (r102, 80 let — 1. primer) + '1 URO' (r89) + nerazrešena
  'Strgjatinka' ×3 / 'Vrhjatinka' / 'Kruščen'.
- **Podpisi-kolaps**: 9/29 (Glibe coop. ×6 + Romey ×2 + Andrej ×1) — proti 1887 vse-podpisano.
- **Glave s14–s21 izpisane** (»Leto 18ſſ..«) — nasprotje s P153 s13-PRAZNO.

## Pin-kaskada

- vitals 725 → **754** (68× `HOUSE_VITALS.length !== 725` → 754 + sporočila)
- 04894 bloki 26 → **55** (qa-p80 vrstica 109 + qa-p153)
- p80 hiše 77 → **79** (+h47/h83; qa ×2 + p80-skripta houses 78 → 80, gap 14 → 15)
- qa-p153: 1888-odsotnost → **1889+-odsotnost + 1888=29**; kumulativ-detail posodobljen
- qa-p85/p86 NOVA-hiša-stražarja: + 04894-1888 izjeme (h7/h41/h53)
- p80-skripta: `len(vitals) == 754`; p153-skripta: VITALS/BLOKI/P80-HOUSES + I5b/I6e/I6f/I10b

## Verifikacija

- p154 **37/37 PASS** · p153 --check **39/39** · p80 --check **PASS**
- runQA **155/155 ok:True** · tsc **0** · lint **0**

## P155-lead

Mrliška 1889: s21-restart r1–6 (Januar–Februar; **Griblje 53 Ana Perdihec, 67, Mertvod [~], 25.1.**)
+ s22+ (r7 h35 Mar 1 izven-Griblje; r11 h60; r17 h30 Marija Milek 66!).
