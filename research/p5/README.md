# P5 — Navzkrižna analiza PUA ↔ PT + PUA zaključek (2026-10-08)

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

## Artefakti
- `pua-pt-cross.json` — polni izpis (obsodbe po vnosih, pokritosti, priimki)
- `src/data/atlas/research.ts` — PUA_PT_CROSS (sklep, omejitve, naslednji koraki)
- `museum-research.tsx` — kartica P5 (zavihek vrzeli)
- `qa.ts` — test `qa-p5-pua-pt-cross`
- `/api/provenance` → `research.p5.puaPtCross`

## Kaj čaka (P5-b)
- PUA strani 35–49: `bun scripts/pua-probe-read.mjs` (sonda čaka na dvig limita,
  nato prebere manjkajoče strani) → `python3 scripts/pua-parse.py` →
  `python3 scripts/pua-gen-ts.py` → integracija + ponovni zagon analize
- VLM 429 rate-limit: aktiven > 3 h (testirano 09:56–10:18, 18 sond, vse 429;
  tekstovni LLM prav tako 429 — isti limit)
