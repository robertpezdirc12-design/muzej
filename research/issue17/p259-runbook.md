# P259 — RUNBOOK — ★ KONČANO 12. 11. 2026 ~19:30 UTC — METODA: AGENT-VIZIJA (alternativa pri kvoti 0!)

**IZID: 36/36 vrstic + 3/3 pag + dueli REŠENI + integracija (6 blokov) + QA-253 + browser + commit — VSE BREZ VISION-KLICEV (kvota celi dan 0).**

- **Ključna ugotovitev:** Agent (Read-tool) prebere Kurrent-pisavo 1:1 pri povečanih izrezih — L+R-celotni-strani (1058-px, 1:1) so dovolj legibilne; stacki (2×-vertikalno) + zoomi (×3–5) + seq13-ravnila + dcol13-4× razrešijo dvoumnosti. VLM-alternative (chat /chat/completions + video-understand) delijo ISTO dnevno kvoto (429 — preverjeno z glavami) — agent-vizija edina neodvisna pot.
- **Datumski duel s13 (rob 9–14):** RAZREŠEN 4×-dcol — VSE PETICE (5. Febr ×7!) — datcol 1:1, census/pass1 NAPAČNA. Rob 15 = 9., rob 16–18 = 10.
- **Restart-duel s12_r7:** 22. Jän 1834 (ne 27.).
- **ŠIMIČ-h60-1:1:** Georg SCHIMIG 59 l (hint '39' napačen!) + mati Maria SHMIG — P258-kandidata h56/h49 dobila referenco.
- **h53×h24 (m8):** Johann PESDIRZ (ne Gosling!) hiša 53 (census '33' napačna!) × Maria BRING 24.
- **h68×h51 (m12):** hiša 68 (ne 58!) × 51.
- **Duhovnika:** 'Georg [~Kraphoniz?] Parochus' (župnik) vs 'Joseph [~Kepanyhigh?] Capell.' (kaplan).
- **Korpus:** 2059→2065 · 01738 47→53 · SIX 31→34 · bothEra 34→39 · 6 dvigov (h51-33/h28-32/h53-30/h68-27/h24-26/h60-24).
- **Umetnine:** blocks-p259.json + module-p259.txt + qa-p259-section.txt + ui-p259-data.json + parish-marriage-notranjost-1833n.json + parish-house-stories.json (regeneriran).
- **Push:** še vedno čaka na nov žeton (P258-token-mrtv 401). Commiti lokalni.

# P259 RUNBOOK — nadaljevanje ko se VLM-kvota (daily) povrne

## ★ POSODOBITEV 2026-11-12 10:55 UTC — ★★★ CHUNK.SH SAMOCELJENJE + SNAP (utrditev po današnji izgubi /tmp!)
- **Testirano na simuliranem brisanju /tmp** (mv + chunk BUDGET=3): 16 JSON korena + pilot + 118 JPG — **VSE BIT-IDENTIČNO**, 0 VLM klicev, izhod 0.
- **heal()**: če ob zagonu manjka hints.json / s11.jpg / duels/ → chunk.sh SAM obnovi JSON-e+skeni iz p259-work/ + regenerira vse izreze (PIL, brez VLM). Cron-valovi nato nadaljujejo brez posega.
- **snap()**: po vsakem uspelem branju (row/census/pass1/pag/duel) se JSON-i TAKOJ prepišejo v p259-work/ — novo branje ne more več izginiti z /tmp (danes ob 09:30 bi izgubili vse; zdaj tega ne more več usodno zadeti).
- ★ STRANSKI UČINEK (pričakovano, NI napaka): p259-work/ se med valovi polni z novimi JSON-i → `git status` kaže nove datoteke do integracije (KORAK 4/6 jih doda v commit).
- runbook KORAK 2 popravljen: p259_pass2.sh (ZASTARELO — samo vrstice!) → p259_chunk.sh (vse faze + samoceljenje).

## ★ POSODOBITEV 2026-11-12 09:42 UTC — ★★★ /tmp/p259 IZGUBLJEN (restart peskovnika!) + OBNOVLJEN 1:1
- Med ~09:25 in 09:35 UTC je peskovnik ZAGNAL NA NOVO → **/tmp/p259 v celoti pobrisan** (rows/loop.log/pag/duels-json vsega ni bilo več).
- **Obnova po postopku vrst. 116 (točno po predpisu!)** — stanje po obnovi **IDENTIČNO pred-izgubi**:
  - JSON-i + skeni s11/s12/s13 vrnjeni iz `research/issue17/p259-work/` (md5 skenov 1:1: b56f04a5/ed62d632/8afbec80 ✓; pilot s11_r1 md5 b5223ba5 ✓).
  - Izrezi regenerirani (deterministično, PIL, BREZ VLM): rows.py (36 full + 36 dates + L×12 + R×6 + census-LEFT/RIGHT×6) + hdrdates.py (hdr×3 + dates_full×3 + dates_grid×3) + duelcrops.py (kompoziti ×10 — md5 VSI OK proti repo-varnostni kopiji!).
  - **Števke: rows=1/36 · census=6/6 · pass1=3/3 · pag=0/3 · duels=0/10** — ostali VLM-work nespremenjen: 35 vrstic + 3 pag + 10 dvobojev.
  - hints.json = 35 ključev (brez s11_r1 — pravilno: pilot je prebran, _one.mjs ga preskoči pred namigom).
- ★★ **PUSH-POPRAVEK:** predhodne seje so commitale BREZ pusha — bilo je **13 zadržanih commitov** (dbdd14c … f25b127). Zdaj pushano vse.
- Cron-valovi (10:45 / 13:15 / 16:15 UTC) + watch-r5 (22:30 UTC) NEPRESNEJENI — epohe preverjene (1794480300 = 12. 11. 10:45 UTC točno!).

## ★ POSODOBITEV 2026-11-12 09:05 UTC — ★★ SANACIJA uigen.py + koledarska popravka (pred-poletna kontrola!)
- **★★★ uigen.py JE IMEL SINTAKSNO NAPAKO** (f-string `}})}}}` — en `}` preveč; py-commit-claim
  P259-PRIPRAVE je bil napačen!) + **NEURAVNOVEŠEN JSX izpis** (68:64 — dvojni zaviti oklepaji
  namesto template-literal po P258-vzoru!). SANIRANO: timeline_jsx prepisana kot NAVADEN niz
  z @@zamenjavami@@ (ne f-string!) — zdaj: py-compile OK + oklepaji 52:52 + **bun-build 5-modulov
  OK** (funkcionalni test s sintetičnimi podatki!) + dry-run exit-2 z navodili + intro/labeli
  iz DATA-JSON (introSi/introEn/label1833n/label1834!) + esc() zaščita.
- **★ KOLEDARSKA NAPAKA ODSTRANJENA:** 'pepelna sreda 1834 = 5. 2.' je NAPAČNO — Gauss:
  Velika noč 1834 = 30. 3. → pepelna sreda = **12. 2. 1834** (in 1833: 20. 2.!). Popravljeni
  p259_duels.mjs (oba poziva — s13_dates sedaj izrecno sprašuje R3–R7!) + p259-facts.json
  (2 polji) + uigen.py. Koledar za [5.|8.]-Febr NE odloča — odločajo SAMO ČRKE.
- Zgodovinsko-dosledno: poroke 1833 (6.+13. 2.) in 1834 (do 10. 2.) so VSE predpostne — vzorec
  'množične-poroke-pred-postom' se nadaljuje (1828-6.2. ×7! → 1834).

## ★ POSODOBITEV 2026-11-12 08:35 UTC — PRE-RECONCILE DOKONČAN (KORAK-3 pospešitev!)
- **Nova analiza: `research/issue17/p259-work/prereconcile.txt`** (326 vrstic — KORAK 3 začni TAM!)
  = konsenz/konflikt tabela vseh 36 vrstic iz pass1+census L/R+datcol+hints (generator: scripts/tmp/p259_prereconcile.py).
- ★★ NOVO ODKRITO — **s13 datumski SPOR (sistematičen!)**: datcol pravi rob8–14 = 5. Febr ×7,
  censusL+pass1 pa rob9 = 9. Febr + rob10–14 = 10. Febr ×5 (2:1 proti datcol!).
  facts.json '5febr1834 ×7'-claim VISI na tem → dvoboj s13_dates MORA razrešiti pred bloki!
- s11 datumi = KONSENZ (6. Febr ×8 + 13. Febr ×5 — samo notacija 'd°'); KRIŽAN-×2-starši s12_r6;
  pass1_s13 foliacija-zmeda (trdi Pag. 19/20 — vsebina veljavna, foliacija ne);
  censusR_s13 v slovenskih imenih (Kržišnik/Kavčič/Zupanc — strip arbitrirà).

## ★ POSODOBITEV 2026-11-12 08:00 UTC — RAZDEDUPLIKACIJA SPOROČILCEV + PREVERJENO STANJE
- Kvota ob 07:59 UTC še vedno 0 (429). Zadnji 429-umik v loop.log: 06:14 UTC.
- **CRON razdedupliran:** watch-r2/r3/r4 (podvojeni z valovi 1–3!) IZBRISANI. Aktiven niz:
  **val-1 10:45 UTC · val-2 13:15 UTC · val-3 16:15 UTC** (samo branje: chunk.sh ×3–4) +
  **watch-r5 22:30 UTC** (= 06:30 SH 13. 11. — polna rolling-24h obnova 22:21! → KORAKI 2–6 do konca).
- Preverjeno: /tmp/p259+duels ×10 kompozitov + dates ×36 + L/R trakovi ✓ · rows=1/36 · census=6/6 · pass1=3/3 · pag=0/3 · git čisto · dev-server OK.
- Ostali VLM-work: 35 vrstic + 3 pag + 10 dvobojev = ~48 klicev (+ retryji).

## ★ POSODOBITEV 2026-11-12 07:30 UTC — VSI MEHANIZMI PRIPRAVLJENI (ne-VLM delo KONČANO!)
- **Duel-kompoziti ×10 ŽE GENERIRANI:** /tmp/p259/duels/*.jpg (backup: research/issue17/p259-work/duels/!) —
  3 datumski (s11/s12/s13_dates = VSE vrstice) + 7 imenskih (s11_r2_gosling ★GOSLING|PESDIRZ-h53|33+BRING|BRINC-h24 ·
  s12_r1_r2 ★19.|12.-Febr+HOFFERER · s12_r5_schmig ★ŠIMIČ-h60+19.|10.|26.-Oct · s12_r7_restart ★22.|27.-Jän-1834 ·
  s13_r1_restart ★5.|8.-Febr · s13_r6_vrh ★VRH-h58|68+h51 · s13_r11_marentic ★10.|17.-Febr+MARENTIČ-24|29).
  Generator: scripts/tmp/p259_duelcrops.py (GEOM po p258-s8/s9-kalibraciji!).
- **p259_duels.mjs** (10 jobov, skip-logika, argument = posamezen job-id!) — DODAN v p259_chunk.sh kot FAZA 5
  (samodejno ŽENE ko so rows=36/36!). Zagon: `bun scripts/tmp/p259_duels.mjs [id]` (brez id-ja = vsi).
- **p259_gen.py** (hišne zgodbe): CONFIG-na-vrhu (EXPECTED_TOTAL/TIERS/SIX/BOTH_P = 0 → izpiše dejanske vrednosti
  in konča z exit-2! Izpolni po integraciji). SIX_STORIES: 31-starih + 7-DRAFT-kandidatov (h24/h28/h51/h53/h58/h60/h68
  — potrdi/prilagodi po reconcile!). POZOR: h24-igra-vlogo-v-notables (najglasnejša-postaja-šest-knjižna!).
- **p259_oldverifier_update.py**: CONFIG-DRIVEN — bere scripts/tmp/p259-config.json
  {total, byBook01738, sixList, bothEraPorocna, p94exceptions:[{year,house,note}], housesNote} →
  qa-parish.ts (HOUSE_VITALS ×N + SIX-lista ×2 + tiers + bothEra ×2 + byBook ×4 + p94-izjeme) + pt-luknja-kirurško!
- **p259_docs.py**: CONFIG-DRIVEN — bere scripts/tmp/p259-docs.json
  {worklogEntry, banner, bullet, tabelaRow, korpusNote, odprtoNew, evidenceNote, total, byBook01738, sixCount, bothEra}
  → worklog.md + README.md (ankri = P258-besedila, stabilni!).
- KORAK-2-konec je zdaj: rows=36/36 **IN** census=6/6 **IN** pass1=3/3 **IN** pag=3/3 **IN** duels=10/10
  (chunk.sh poroča vse pet števk!). Po KORAKU-2+ izbriši preostale cron-sprožilče (cron list → delete).

## Kontekst (samozadostno)
Projekt: Podzemelj matrice (Next.js, /home/z/my-project). Faza P259 = NOTRANJOST poročne knjige 01738:
**1833-nadaljevanje + 1834-začetek (s11–s13 = Pag. 19/21/23).** Vsa priprava je ŽE opravljena:

- Skrani s11/s12/s13: /tmp/p259/s11.jpg (md5 b56f04a5…), s12.jpg (ed62d632…), s13.jpg (8afbec80…) — md5-dvojno 1:1 ✓
- pass-1 + census-L/R + ygrid + datcol + 1 pilot-vrstica (s11_r1) ŽE PREBRANI: /tmp/p259/pass1_s*.json, census_*.json, ygrid_s*.json, datcol_s*.json, full/s11_r1.json ✓
- Struktura POTRJENA: s11 = 13 vrstic (6. Febr ×8 + 13. Febr ×5 = m7–m19); s12 = 12 vrstic (1833-konec m20–m25 + 1834-restart m1–m6, robno-številčenje 1–7!); s13 = 11 vrstic (1834 m7–m17, rob 8–18!). Skupaj 36 vpisov, 35 vrstic ŠE NI prebranih (s11_r2 … s13_r11).
- ★ 13 porok na 6. 2. 1833 = NOVI REKORD korpusa; 1833 = 25 vpisov (največje leto); rob-štetenje čez mejo leta; 5. restart (1834).
- Kvota: x-ratelimit-user-daily (0 = izčrpana 22:21 UTC 11. 11.; 10-min limit 30!). Rolling-24h → vrača se postopoma od ~10:45 UTC 12. 11.

## KORAK 1 — preveri kvoto (en klic)
```bash
cd /home/z/my-project && bun run /tmp/p259_raw.mjs 2>&1 | rg 'STATUS|daily-remaining'
```
- Če `daily-remaining: 0` → NE DELAJ NIČ VLM (vsak klic tudi zavrnjen porabi kvoto!). Odgovori kratko in počakaj naslednji sprožilec.
- Če `daily-remaining` > 0 → NADALJUJ s KORAKOM 2.

## KORAK 2 — preberi vrstice (35) + vse ostale faze — SAMO prek chunk.sh!
```bash
cd /home/z/my-project && bash scripts/tmp/p259_chunk.sh 540   # ponavljaj dokler ne konča; ~32 s/zahtevo (varčno < 30/10min!)
```
Ponavljaj `bash scripts/tmp/p259_chunk.sh 540` dokler `ls /tmp/p259/full/s1*_r*.json | wc -l` ne da **36** IN pag=3/3 IN duels=10/10.
Chunk samodejno teče skozi faze: rows → census → pass1 → pag → duels (ko je rows=36/36); skip-logika + SAMOCELJENJE (heal) + snap()-varnostna kopija vsakega branja v p259-work/.
NE uporabljaj p259_pass2.sh (zastarelo — samo vrstice, brez ostalih faz)!
Namigi za vsako vrstico so v /tmp/p259/hints.json (bere jih scripts/tmp/p259_one.mjs).

## KORAK 3 — uskladitvena tabela
```bash
cd /home/z/my-project && python3 scripts/tmp/p259_reconcile.py > /tmp/p259/reconcile.txt 2>&1; less /tmp/p259/reconcile.txt
```
Preuči konsenze; določi DUELE (samo tam kjer 3 viri ne soglašajo — prihrani kvoto!):
- DATUMSKI: s12_r1 [19.|12.]-Febr · s12_r5 [19.|10.|26.]-Oct · s12_r7 [22.|27.]-Jän-1834 · s13_r1 [5.|8.]-Febr-1834 · s13_r11 [10.|17.]-Febr
- IMENSKI/hišni: s11_r2 ženin (Pesdirz? Gosling? Gutting? h33|h53?) + nevesta (Bring/Brinc h24?) · s13_r6 ženin (h58|h68? Vrh?) + nevesta (h51?)
Duele naredi po vzoru P258: scripts/tmp/p258_duelcrops.py (celice ×3 zoom kompoziti) + p258_duels.mjs.

## KORAK 4 — integracija (mehanizmi so pripravljeni!)
1. Bloki → research/issue17/blocks-p259.json (vzorec: glej scripts/tmp/p259_insert.py + P258-bloke v parish.ts ~vrstica 14331–14491!) → `python3 scripts/tmp/p259_insert.py`
2. Modul → scripts/tmp/module-p259.txt (PREDHODNIK_1833N_*/1834_*/259_NITI/KRAJI/KORPUS po vzoru P258-sekcije vrst. 1269–1347!) → `python3 scripts/tmp/p259_module.py`
3. Hišne zgodbe → prilagodi scripts/tmp/p258_gen.py → p259_gen.py (števci: 2059→N, tierji, SIX 31→S, bothEra 34→B; NOVE zgodbe za h24/h28/h51/h53/h58/h60/h68 po potrebi + posodobljene obstoječe!)
4. Dokaz → research/issue17/parish-marriage-notranjost-1833.json (po vzoru -1832.json; vir/struktura/leta/niti/kraji/korpusUcinek/xOpen/p260!)
5. UI → scripts/tmp/ui-p259-data.json (e1833n/e1834/korpus_card/niti_card/kraji_card/imports) → `python3 scripts/tmp/p259_uigen.py && python3 scripts/tmp/p259_ui.py`
6. QA → scripts/tmp/qa-p259-section.txt + qa-p259-imports.txt → `python3 scripts/tmp/p259_qa.py`
7. pt-luknja-18-final.json: kirurško vitalsTotal/byBook-01738 (vzorec p258_sanacija2.py!)
8. Stari verifikatorji → scripts/tmp/p259_oldverifier_update.py (vzorec p258_oldverifier_update.py: 2059→N, 47→M, SIX-31→S, bothEra-34→B, QA-252→253+, leta-1828–1833→1828–1834!)

## KORAK 5 — verifikacija
```bash
cd /home/z/my-project && bunx tsc --noEmit && bun run lint && bun scripts/tmp/run-qa.ts   # pričakovano 253/253+ (252 + qa-p259)
```
+ verifikatorji baterija (po vzoru p258_verifier_cascade.py — VARNI FILTER: brez bump/fix/restore/docs skriptov!)
+ browser-verifikacija: agent-browser → Matrike-tab → P259-kartica + mobile 390×844 + footer + 0-console-errors (screenshota scripts/tmp/p259_card.png + p259_mobile.png!)

## KORAK 6 — zaključek
- worklog.md: vnos P259 (po vzoru P258-vnosa, vrstica ~8255+)
- README.md: banner + kazalo + tabela + korpus + Zadnje-stanje + Odprto-P260 (vzorec p258_docs.py)
- git add + commit (sporočilo po vzoru P258-commit c95df6f!) + push (origin main; žeton v skladišču besedila zgodovine)
- ★⚠ PUSH-TOKEN MRTEV (12. 11. ~11:05 UTC): ghp_-žeton iz zgodovine vrne **401 Bad credentials** (veljal je še 09:45 UTC!). Ni gh-CLI/netrc/credential-store nadomestkov. POSLEDICA: KORAK 6 push ČAKA na nov žeton od uporabnika (Settings → Developer settings → Personal access tokens → klasika ghp_ z repo-pravicami). VSE OSTALO (branja/integracija/QA/browser/worklog/README) poteka normalno — commiti ostanejo lokalni (varni: /home/z/my-project preživi /tmp-wipe); en sam push kasneje sinhronizira vse.

## KLJUČNE ŽIVE ŠTEVKE (pred-P259)
Korpus: HOUSE_VITALS 2059 · byBook-01738 47 (leta 1828–1833+1873!) · SIX-klub 31 (tierji 31/35/10/8/8/8) · bothEra-poročna 34 · MILIČ 252 · QA 252/252.
Kandidatni Griblje-bloki P259: h24 (s11_r2 nevesta Bring/Brinc? — dvig 26 + ŠEST-knjižna!) · h33|h53 (s11_r2 ženin?) · h60 (s12_r5 Šimič?) · h28 (s12_r6 — dvig 32! ŠIV-hiša!) · h58|h68 (s13_r6 Vrh?) · h51 (s13_r6 — dvig 33?).
Vsi kandidati + firstYear-dvigi: research/issue17/p259-facts.json!

## NADZORNI podatki
- Vsi prebrani artefakti so zavarovani v research/issue17/p259-work/ (pass1/census/ygrid/datcol/hints/s11_r1 + skrani s11–s13 + dueli-JPG!). snap() med tekom dodaja tudi vsa nova branja. Če /tmp/p259 manjka: **SAMO poženi `bash scripts/tmp/p259_chunk.sh 540`** — heal() sam obnovi vse iz p259-work/ + regenerira izreze (ročni postopek iz prejšnje različice ostaja kot rezerva).
- Sprožilci: 06:15 · 10:45 · 13:15 · 16:15 · 22:30 UTC (cron). Po uspešnem zaključku KORAKA 2+ NE potrebuješ več ostalih sprožilcev (odstrani jih: cron list → delete).
- Kvota-glava: x-ratelimit-user-daily-remaining (10-min limit 30 — chunk.sh 32s ritem = varno).

## ——— VAL-FIN (2026-11-12 18:20 UTC) — VLM-DUEL-VALIDACIJA + POPRAVEK m20/m21 ———
- KVOTA OBNOVLJENA 496 → izvedena **neodvisna validacija vseh 9 preostalih duelov** (11 VLM klicov + 4 agent-vizija Read ×6/×10).
- **9/10 POTRJENO**: s11-dates, s11_r2-PESDIRZ-h53/BRING-h24, s12_r7-RESTART-22.-Jän, s13-dates-5.-Febr-×7, s13_r1, **s13_r6-VRH-h68** (2. neodvisen vir: census_L13!), **s13_r11-MARENTIČ-Dobravlje-29** (iz xOpen → 1:1), s12_r5-SCHMIG-19.-Oct (2. potrditev: digit-'9'-descender-≠-'2'-referenca-r1/r3/r7!).
- **1 POPRAVEK**: m20/m21 datum **19. → 12. Febr 1833 ×2** — r1 polni zapis '12. Feb. 1833.' + r2 '12. att°' (×6 agent-vizija, digit-shapes); 4 izvora (census+pass1+duelval+urkunda-celica-'12. Febr'); datcol-'19.' = misread 1:4. ANOMALIJA: 12. AFTER s11-tail 13. Febr = dopisani zamik (licence '2. + 12. Febr').
- Metoda-novina: **DIGIT-SHAPE reference iz istega skena** (znane števe r3 '21.' / r7 '22.' kot primer za dvomljivo '2|3|9') — odločilno pri ×10 zoomu.
- Popravljeni: parish.ts-header + STRUKTURA-si/en (parish-marriage-early.ts) + module-p259.txt + s12_r1.json; + VALIDACIJA.md + tiebreak/ + duel-vals/ backupi v repo.
- QA po popravku: **253/253** · tsc-0 · lint-CISTO · browser re-verifikacija (render OK, 0 console-errors, footer-na-dnu, mobile-390-brez-preliva, iskanje dela).
- Push: **28aa5cf** (nov žeton deluje — KORAK 6 dokončno zaprt).
