# parish-baptism-1918 — zapiski (P113; krstna 04105, leto 1918)

## FAZA 1 (fetch + forenzika) — Task 86
- **MATRICULA FETCH**: matscan.py protokol (AES-256-ECB+MD5+csrf, ključ »pG58&Qj$?.d=(<.[v!kJkm_XNbsa6e.f«) — **fetch s300–s312 (13 skenov) → /tmp/p113** (s311/s312 = str. 263/264 = 1919 glava + P114 lead!).
- **STRUKTURA LETO 1918**: velika ročna glava »1918« VRH str. 254 = s300; str. 254–262 == skeni 300–310 (11 skenov; str. == sken − 46 **RAZEN dup parov**); **DUP PAROV ×2 — prvi od P110!**:
  - **s301 = dup str. 254** — bela listina čez r3 delno dvignjena → r3 razkrita (Gradac, Antonija, 8./12. 1., EMŠO 0801918505108 = 08.01.1918 ✓; gosta legitimacijska marg: deželna vlada Ljubljana 25.2.1920 št. 3898 [~] + 1949 + poročena 9.8.1945 Ljubljani + 1976 podpis »Cergar?« [~]).
  - **s306 = dup str. 258** — r25 razkrita (Gradac 80?/20, Ivana, 14. 7., EMŠO 1007918505011 — DVOM 10.07 vs rojstva 14.07); bela listina na VRHU str. 258 = 2 smrtna zapisa (†16/17.4.1973 Ljubljana + †1.10.2004 Kranj, maticarka Vesna Simonič) + žig »PODZEMLJ 1918/25«? [~].
- **CROP KORPUS** (170+ izrezov): 60 n-zoomov + 26 z + 32 f + 21 x + 5 sig + 13 stan-bandov (860–1160 px! — levostranski stolpci Vera/Spola/Stan segajo do x≈1060) + 25 novih ciljanih (t/u/v/w/x30–x33/y/z3x/q).
- **POZOR — prejšnji n-series bug**: n16_r18/n60_r18B/n21_r23r24/n29_r34/n30_r35r36 = ČRNI (crop izven meja skena) — nadomeščeni s svežimi cropi (w01–w04, z31–z34).

## FAZA 2 (transkripcija + evidence + verifier + qa) — Task 86
- **52 vrstic r1–r52** (6 strani × 6 + 4); **BREZ zaključne opombe** (formula 1916/1917 manjka — vojno leto; str. 262 se konča z r52 + prazne vrstice; f17/f18 = dno prazno).
- **entries = 9 Griblje vpisov** (r2 h86, r16 h34, r24 h21, r28 h53, r37 h45, r38 h30, r39 h14, r45 »sub dioe.«, r46 h44); **excluded = 43** (vsi izven Gribljih); **NARE 8/8 — 4. čisto leto!** (86←1913, 34←1916, 21←1914, 53←1915, 45←1917 ZAPORED, 30←1911 VRZEL 6 LET, 14←1917 ZAPORED, 44←1914); PT 7/1 (h44 v luknji 41–60).
- **20 anomalij** (A1–A20): CIGANI ×5 + NEMŠKA MARG (Brajdič, garnizona Podzemelj!) + sub dioe. ×4 + mrtvorojena izpipana ×2 + 4 duhovniki (Učak + Bitnar + **Kolbezen žup. upr.** + Lopar) + 2. razveljavitev (Novo mesto P 592/64-5, 13.9.1964) + 2 preimenovanji (r44 1979 občinski sekretariat + r51 »vpisujem Zora« 1982) + Balorda-Recurt († po 3 mesecih!) + Švedska (Vällingby 1988) + Rusija (1964 delavec) + Zagreb ×2 + VPIS PRENEŠEN ×9 = REKORD + NEZAKONSKI ×5 = REKORD + EMŠO 30/28 (18✓ + 8 dvomov + anomala r44 »128« + 1. korekcijski PAR r46 0611→1011) + železniška ×6 + hiša Grm 1→25 + † 17.3%.
- **evidence**: research/issue17/parish-baptism-1918.json (9 entries + 43 excluded + 20 anomalij + 30 crossChecks + kontinuitete + p114Lead).
- **verifier**: scripts/p113_parish_baptism_1918.py — I1–I13, **16/16 PASS** (živo: knjiga 200 + inventar 326 + skeni 13 prisotnih; --check offline 14/14).
- **parish.ts**: +9 blokov 1918 (h86/h34/h21/h53/h45/h30/h14/»sub dioe.«/h44); vitals 508 → **517**; bloki 04105 482 → **491**.
- **qa-p113**: 114. kontrola (9 vpisov / 9 hiš NARE 8/8 + 1 sub dioe. + 0 intra-repeats + dup-novela s301/s306 + 0 novih + 30 pinov + 4 duhovniki + nezakonska r24 + regresije h88-KONEC/h24-pavza/h45-čevljar-2. leto/h14-zaporedje); **runQA 114/114** (obnova allow-list: P85 h30 + 1918, P86 h53 + 1918, P91 h45/h14 + 1918; Lopar živ threshold 2/9 Griblje).
- **README**: P113 bullet ZAKLJUČEN + »Zadnje stanje (po P113)« + QA 114/114 (p79–p113 = 35 skript).

## P114 LEAD (krstna 1919 — ZADNJE leto knjige!)
- **glava 1919 = velika ročna (»Avstrija 1919«? [~]) + tiskana »Leto 1919« VRH str. 263 = s311** (s311/s312 že lokalno!); str. 263–264.
- **1919 r1 = Krasinec 3 Anton** (1./2. Januar; EMŠO 0101191850191? [~ — vzorec »195«?! P114 naloga: milenijska številka 1919 = »0«? — 010119**500**191 bi bila 01.01.1950! preveriti 5×]; marg zarocen 21.4.1956 + žena † 17.11.2002; PEČAT vpis prenešen 5.2.2006).
- r2 = Cerkvišče 35 Jožef (13./13. Januar; EMŠO 130319500623?; † 10.7.1984 Novo mesto, Gradac 17.1.1985 maticarka Ana Drušić?); r3 = Vranoviči 30 Anton (14./15. Januar; +16/6 1949); r4 = Grišiče 33 Alojzij (16./18. Januar; porocen 5.6.1948); r5 = **Krasnoglavice 29 Ana** (5./8. Februar; PEČAT vpis prenešen 21.11.2003 Metlika; EMŠO 050219500525; † 20.9.1935) — **NOVA vas »Krasnoglavice«!**; r6 = Grišiče 5 Stanislav (22./23. Februar; † 1994 Ljubljana).
- fetch s313+ potreben (/tmp/p114); **konec knjige 04105 = konec krstne linije 1886–1919!**
