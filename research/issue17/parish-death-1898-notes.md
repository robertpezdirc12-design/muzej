# P164 — MRLIŠKA KNJIGA 04894, LETO 1898 — notes (13. polno leto mrliške linije)

## METODA (deterministična reprodukcija)

- **Fetch 8/8**: s65–s72 (inventar-256 re-uporabljen iz /tmp/p163 — SANACIJA-ne-potrebna, artefakti zdržali celo sejo — prvič odkar P161!)
- **VLM 8/8, 0 FAIL**: 8 celostanskih branj (glm-5v-turbo, ≤2 foreground-po-vzorec — dejansko 5+3 v 2 serijah!)
- **rows-detekcija = NOVA LEKCIJA**: P162-zap-stolpec-recept NAPAKEN za te skene — skeni so DVOSTRANSKI razponi ('Mrtvaška knjiga.' čez pregib!) + ROTIRANI (pravila drsijo v x ±15px!) + zap-stolpec vsebuje NATISNJEN navpičen naslov 'Zaporedna štev.' (colfrac 0.69 — vezava vsebine!)
- **REŠITEV**: morfološka odstranitev črt (scipy binary_opening 81×1 + dilatacija 3×9) + ozka projekcija zap-številk (x 0.052–0.064 — LEVO od natisnjenega naslova!) + MERGE_GAP 55 → P163-s64-napaka-RAZREŠENA
- **8× diag-PNG agent-oči** (full-overlay vrstic) + **26 max-zoom izrezov** (22 targetiranih + 4 dopolnilni: podpisa-zap4/zap34 + zap5-bolezen + zap15-ime + zap39-ime)

## MAX-ZOOM > VLM — 15. POTRDITEV (9 popravkov)

1. s66-zap4: hišna-'32' → **52** (5 = raven-zgornji-dvig + spodnja-zanka — P163-lead-'h32' OVRJEN!)
2. s66-zap10: mesec-'Maj' → **Marcej** (5-glyph M-a-r-a-j — VLM-krnjša!)
3. s67-zap18: vas-'Krasinec' → **ŠKRILJE** (Š-k-r-i-l-j-e s caronom — ŽE v župnijskem naboru! P163-lead-'h2-Griblje' DELNO OVRJEN!)
4. s67-zap21: bolezen-'Hprnica[?]' → **Vodernica** (korpus-termin ×4!)
5. s69-zap46: bolezen-'Vaselj' → **Kašelj** (K-a-š-e-l-j jasno!)
6. s69-zap48: ime-'Mihel' → **MILEK** (M-i-l-e-k — korpus-leksikon: matika-1887 'geb. Milek'!)
7. s69-zap46: ime-'Žele' → **ŽELJKO** (Ž-e-l-j-k-o — cf. P92-1887-botra-Nikolaj-Željko-h1!)
8. s66-zap4/s68-zap34: duhovnik-'Jelen'/'Hennig' → **Fr. Škurmelj** (podpisa @×3.0 — VLM-duhovnik-stolpec NEZANESLJIV-1898!)
9. s66-zap5: bolezen-'Starost/Slabost' → **Mrtvorojen** (M-r-t-v-o-r-o-j-e-n jasno!)

## P162b-γ-LEKCIJA — 16.–17. POTRDITEV

- s65-zap2 (Jožef-Čopič/Tapič-Primostek-h1): starost '41' (VLM×2) / '77' (diag-eye) → **71** @×3.2 (γ-forma = 7!)
- s65-zap3 (Jožef-Jakša-Vranoviče-h26): starost '43' (VLM) / '93' (diag-eye) → **73** @×3.2 (γ = 7 + 3!)
- **LEKCIJA ponovno potrjena: VEDNO kalibriraj γ/±/zaprta-zanka na zap-stolpcu ISTEGA skena pred branjem starosti!**

## MEJA 1897/98 = 5. STIL 6. POTRDITEV + MEJA 1898/99 = 4. INLINE-POTRDITEV

- s65-dno: **»1898.« DVOJNO podčrtana** letnica na PRAZNI vrsti (@max-zoom: debela + tanka črta!) + zap1 **'3. Jan. 5.' — Jan-OKRAJŠAVA-INLINE** (1. okrajšava-varianta INLINE — cf. P155–157 + P161 + P163-INLINE!) + restart zap 58→1
- s70-top: **'1899.' ročno v smrti-celici zap1** (NAD Januarj — NI na prazni vrsti!) + Januarj-INLINE + restart zap 48→1 = **4. INLINE-potrditev** (cf. P161-s51 '— 1895. —' INLINE!)
- **P163-lead-'s71+?' OVRJEN**: s70 = ŽE 1899 (glava + zap 1–11); s69-dno = PRAZNE vrste brez markera!
- **2 VARIANTI stil-#5 v ISTEM letu** (s65-prazna-vrsta-podčrtana + s70-INLINE) — prvič!

## PEZDIREC-×4-v-1898 = REKORD mrliške (era 7. leto, rast 2→3→4!)

- h52-Marija-½-hči-11-mes-Januar + h30-Doroteja-žena-59-Marec + h64-Ana-roj.-PEZDIREC-63-April + Boršt-h23-Janez-½-sin-34-Maj
- PEZDIREC-mreža čez knjige: poročna-1886-Nikolaj-PEZDIRC-h16 + mrliška 1896-×2 + 1897-×3 + 1898-×4
- 1899-lead: s70-zap10-h20-Marija-Pezdirec + s70-zap7-Krasinec-h3-Jožef[~] = **era 8. leto!**

## h64-×2-DRAMA (3. par linije!)

- Ana-VERBIČAR-roj.-PEZDIREC-63-April + Matija-VERBIČAR-58-Okt = 2 smrti ISTA HIŠA v ~6 MESECIH (verjetno PAR [~])
- cf. 1895-h46-2-DNI (Brodarič-mati+sin) + 1896-h51-12-DNI (Urh-mati+sin) + 1898-h64-6-MESECEV (Verbičar-par [~])

## 2× 1. MRLIŠKI VPIS KADARKOLI

- **h52** (Marija-Pezdirec) = **20. PT-luknja-dokaz** — h52 ŽE v P80_PT_GAP-doc-list prek poročne-1895-Mathias-Perdinec (P124)!
- **h34** (Ana-Filak) = 21. dokaz — h34 IZVEN 41–60-luknje (ne gre v PT_GAP-set)!
- 0 novih hiš v korpusu-93 — **4. leto zasičanja** (h51-P162 = zadnja nova!)

## SKEN-GEOMETRIJA (nova lekcija za rows-detekcijo)

- 04894-skeni 65–72 = **dvostranski razponi** (leva stran: zap+mesec+vas+ime; desna: vere+starost+bolezen+podpis)
- ROTACIJA: pravila drsijo v x (~15px čez višino) → fiksni x-band neuporaben (P163-s64-napaka: 1 'vrstica' = celotna višina!)
- natisnjen navpičen naslov 'Zaporedna štev.' v zap-stolpcu (colfrac 0.69) → vezava vsebine
- REŠITEV: scipy-binary_opening-81×1 (navpične črte) + dilatacija ±4px + ozka-projekcija-x-0.052–0.064 + MERGE_GAP-55
- diag-PNG-agent-oči = pogoj (VLM-MISS-Griblje = 0-leta — P163-×3-lekcija vgrajena v VLM-prompt!)

## DEMOGRAFIJA 1898 (DNO linije!)

- 48 vpisov / 7 Gribljev / 6 hiš (h64 ×2) — najnižje odkar 1889-8!
- rast: 13→13→29→8→15→15→17→10→6→12→16→13→**7**
- meseci: Jan4·Feb1·Mar8·Apr3·Maj10·Jun2·Jul3·Avg2·Sep3·Okt5·Nov2·Dec5 = 48 (1. leto z VSEMI 12 meseci odkar 1890 — brez MESEC-0!)
- otroška umrljivost 46 % (≤6-let ×22/48) + razpon 11 mesecev → 73 let
- 2× mrtvorojen-BREZ-podpisa (zap39-N.-Plut + zap41-N.-Jože — r53-vzorec #12–#13!)
- previden: 1 ×7/7 Gribljev (1897: 1 ×9 + pika ×4)
- duhovniki (diag-leksikon): Fr.-Škurmelj-dominanca + Jos.-Rauq (VLM-stolpec 'Jelen'/'Hennig' ZAVRJENA)

## KUMULATIV po P164

- vitals 866 → **873** (+7) · mrliški bloki 04894 167 → **174** (+7) · bloki 1898 = 7
- p80 hiše **88 NESPREMENJENE** (h34/h52 IZVEN p80-filtra — filter = 1886 ∪ 1897 ∪ sidri!)
- p80-skripta: 873/88/gap-18 · korpus **93 NESPREMENJEN**
- P80_PT_GAP doc-list 15 NESPREMENJEN (h52 že v setu prek P124; h34 izven nabora!)
- qa-p164 = 165. kontrola · stale-guardi → 1899 (11× qa + 9 skript) · VITALS_TOTAL-cascade p153–p163 → 873

## P165-LEAD: mrliška 1899

- s70: glava 'Leto 1899' + '1899.'-INLINE-zap1 (Januarj 1./5.-Otok-11-Nikolaj-Jurcavič-68!) + zap 1–11 [Griblje ×1: zap10-h20-Marija-Pezdirec — PEZDIREC-era-8.!]
- s71: zap 12–23 [Griblje ×5! — VLM-agregat] · s72: zap 24–35 [Griblje ×2: h32-Marija-Mulek? + h24-Matija-Štrinec? — VLM-s72-meseci-KAOS (Januarj@24?) ANOMALIJA!]
- NOVI DUHOVNIK #9-kandidat: **Franc-Števan-coop** (s70-zap2/3/7/8/10/11!)
- meja 1899/1900 [~ s75+?]
