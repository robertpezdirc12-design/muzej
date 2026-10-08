# P5 — Navzkrižna analiza PUA ↔ PT + W-most + PUA zaključek (2026-10-08)

Nadaljevanje po P4 (isti dan), po naročilu uporabnika (»odlicno nadaljuj«).
Odprtih ostaja PUA strani 35–49 (priimki P–Ž), blokiranih na VLM 429 rate-limit
(limit na ravni računa, vztraja > 3 h od ~08:12).

## Kaj je narejeno (P5-a: deterministična analiza)

**`scripts/pua-pt-cross.py`** — navzkrižna primerjava brez AI klicev
(Levenshtein podobnost normaliziranih priimkov, prag 0,72 = ujemanje /
0,50 = verjetno; ponovljivo, bere `research.ts` + `houses.ts`):

- 69 vnosov PUA (str. 3–34) ↔ 84 hišnih vrstic PT (21 parcelnih ločeno)
- **0/64 neposrednih ujemanj** priimka pri isti hišni št. (51 divergenc < 0,50)
- 8 priimkov obstaja v OBEH registrih (Bring, Hlebety, Kriš(t)an, Milleg …)
  — a na RAZLIČNIH hišnih številkah
- PUA: 38 PT št. pokritih; 12 PUA št. brez PT vpisa (11 v bloku 41–60 = str. 5 PT);
  PUA št. se končajo pri ~69, PT pri 98
- PUA vsebuje tudi nesosednje lastnike (Deschitz, Dragosche, Waldendorf,
  Leusthal) in institucije (cerkev sv. Vida, komenda, baron Gradatz)

**Sklep (hipoteza [~]):** PUA je abecedni indeks lastnikov PARCEL z lastno hišno
referenco, ki ni enaka konskripcijskemu številčenju PT → seriji primerjaj po
imenih, ne po številkah. Oba vira sta strojna branjla [~] — 0/64 je lahko tudi
sistemska napaka VLM pri stolpcu hišnih št.; končna presoja: človeška paleografija
+ arhivsko vprašanje ARS (konskripcijska št. vs. Steuerhausnummer).

## Kaj je narejeno (P5-c: W-most PT ↔ PUA, isti dan)

**`scripts/pua-pt-wbridge.py`** — nadaljevanje P5-a: odkritje, da 43 vrstic PT
(hiše 21–40 str. 4, vinogradniške parcele 41–60 str. 5, hiša 76½) nosi
**45 sklicev »W.<štev>«** — hipoteza [~]: W = hišna št. lastnika v PUA
številčenju → MOST med obema sistemoma številčenja.

- 26 različnih W; 22 ima PUA protistrani, 4 (32, 64, 65, 68) jo še nimajo
- **15/22 (68 %) ujemanj ≥ 0,50** po križno-žetonjski podobnosti vseh imenskih
  žetonov (proti izhodišču P5-a: 0/64): 6 MATCH (W.2 Hlebetz↔Hlebety 0,86;
  W.24/W.25 Brinig↔Bring 0,83; W.29 Milleg↔Millej 0,83; W.21 Jožef↔Jožeg 0,80;
  W.1 Mufa↔Wufa 0,75 — M↔W zamenjava značilna za Kurrent), 9 PARTIAL, 7 MISMATCH
- Šumenje pošteno dokumentirano: W.47 = prečrtana PT vrstica, W.62 = dvojni PUA
  vpis (Kosirhan Mäda + Georg Juttner), PT str. 6+ W-stolpca ne nosi
- **4 preverljive napovedi za strani 35–49** (P5-b): PUA h32 (Greg/Piberig
  Ulrich), h64 (Varbutek Mufa / Jörg Georg), h65 (Bring Marko / Glan Simonz),
  h68 (Malt Ulrich) — če se ob branju potrdijo, se zaupanje v most dvigne

## Artefakti
- `pua-pt-cross.json` — polni izpis (obsodbe po vnosih, pokritosti, priimki)
- `pua-pt-wbridge.json` — polni W-most (join po številkah, verdikti, napovedi)
- `src/data/atlas/research.ts` — PUA_PT_CROSS + PUA_PT_WBRIDGE
- `museum-research.tsx` — kartici P5 in P5-c (zavihek vrzeli)
- `qa.ts` — testa `qa-p5-pua-pt-cross` + `qa-p5-pua-pt-wbridge`
- `/api/provenance` → `research.p5.puaPtCross` + `research.p5.puaPtWbridge`

## Kaj čaka (P5-b)
- PUA strani 35–49: `bun scripts/pua-probe-read.mjs` (sonda čaka na dvig limita,
  nato prebere manjkajoče strani) → `python3 scripts/pua-parse.py` →
  `python3 scripts/pua-gen-ts.py` → integracija + ponovni zagon OBEH analize
  (P5-a in P5-c) + preverba napovedi h32/h64/h65/h68
- VLM 429 rate-limit: vztraja še ob 11:30 (2 novi sondi); tekstovni LLM prav tako
