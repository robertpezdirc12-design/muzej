# P12 — AR 3D vas: hišne številke (raziskava) + vas oživi (integracija)

Datum: 2026-10-08 (zvečer). Naročilo uporabnika: »nadaljuj z razvojem ar vasi 3d«.

## 1. Raziskava: hišne številke na listu A02 (IZID: NEGATIVEN, dokumentiran)

Motivacija: kartica stavbe v AR časovnem stroju je (do P12) obeleževala
»hišna številka na listu A02 še ni prebrana (TO_COLLECT)«. Cilj je bil
prebrati hišne številke ob stavbah in 156 3D podlatn povezati z Registrom
hiš 1825 (PT: ~80 lastnikov, hiše 1–98) in matičnimi knjigami.

### Kaj je bilo preizkušeno (metode + izidi)

1. **Vzorčni izrezi stavb (45 px roba, 6× povečava)** — VLM je »prebral«
   številke 1–11, a ponovitve so pokazale, da je bila zaporednost HALUCINACIJA
   (vprašanje je vodilo model).
2. **Slepi test (brez konteksta, 8× zoom, 3 ponovitve, 6 jedrnih stavb)** —
   5/6 stavb: NO_CHARS (dosledno); 1/6: »1935« (rdečkasto, sredina) — kasneje
   razloženo kot rdeči madež/parcelni ostanek.
3. **Barvna analiza skena (numpy)** — rdeče črnilo 0,95 % površine;
   domneva »rdeče polnilo = stanovanjske hiše«: 95–97 stavb z rdečim deležem
   > 0,25 ≈ število PT hiš (80–98) — STATISTIČNO ZANESLJIVO, a VLM preverba
   posameznih stavb je DIVERGIRALA (mešani izidi: »RDECE_POLNILO«,
   »NI_RDECE«, »RDECI_PIKI« pri istih vrednostih) → klasifikacija ni
   uporabljena kot podatkovna plast (poštenost > domneva).
4. **Povezane komponente rdečega (scipy.ndimage)** — 1217 komponent; 43
   »številka-podobnih« (15–250 px², 6–17 px višine) znotraj stavbnih bboxov;
   12 najbolj obetavnih prebranih pri 14×: **NEČITLJIVI** (razpad skena;
   en sam delni izid »3«, en »morda 2 ali 5« — nezadostno).
5. **Rdeče 4-mestne številke v parcelah** — te SO berljive (ob jedru:
   1009–1106; strnjena sekvenca 1044–1054 ob vzhodnem pasu; t1 ploščica
   okoli cerkve: 1010–1026). To so **PARCELNE** številke (rdeče črnilo,
   zapisane v odprtih parcelah; GLASNOST: VLM je eksplicitno potrdil
   »nobena ni neposredno znotraj stavbnih obrisov«).
6. **PT register — struktura razjasnjena** (VLM na strani 4 N083PT.pdf,
   prenesenega z VAČ): stolpci ~ Haus Nro. / lastnik / Stand/Wohnort
   (»W.«= Wohnort = hišna št. prebivališča lastnika — POTRJEN mostiček
   P5-c med PT in PUA številčenjem!) / vrsta (»Schißing/Apnind« = napačni
   brani kulture, številka za njimi je AREAL v klafrter) — torej PT NE
   vsebuje parcelnih številk, ki bi se neposredno videle na listu.
7. **PS register (Protokoll der Grund-Parzellen)** — prenesen (59 MB, 143
   strani, VAČ uodid 373415 docid 41780); struktura (PS-structure.json):
   Nro. des Blattes / **Nro. der Parzelle / Haus Nro.** / lastnik / raba /
   površina → **TO JE ZANESLJIV MOST PARCELA↔HIŠA**, a za pokritje ~156
   stavbnih parcel bi bilo treba prebrati ~50+ strani Kurrent rokopisa po
   ~14–20 vrstic/stran pri akutnem VLM rate-limitu (429 po ~10 hitrih
   klicih; 20–25 s presledki so nujni) → **TO_COLLECT** (ocena: 1–2 h
   VLM časa ob sproščeni kvoti).

### Zaključek raziskave

- Hišne številke **NA stavbah lista A02 niso zapisane** (slepi testi +
   analiza madežev) — ugotovitev je DOKUMENTIRANA (ne več TO_COLLECT za
   same številke).
- List nosi rdeče PARCELNE številke; most do hišnih št. vodi le prek PS
   (143 str.) — odprto za prihodnjo sejo ob višji kvoti.
- Vsi statusi ostajajo REVIEW (strojno branje ni dokazni vir).

## 2. Integracija: AR 3D vas oživi (P12)

- `src/lib/village3d.ts`: TREES (1666: 1586 v gozdnih conah + 80 razpršenih
  na lokah; mulberry32 seed 1225 — deterministično; izogib ≥ 7 m od stavb),
  TREE_STATS, SMOKE_CHIMNEYS (8: vsaka 3. jedrna stavba 7–18 m), HOUSENO_FINDING
  (si+en dokumentirana ugotovitev), PERIODS[1825] nota dopolnjena.
- `src/components/museum/village-scene.ts`: drevesa = 3 InstancedMesh
  (debla valj + listave krošnje ikozaeder z barvnimi razlikami + iglavci
  stožec); dim = 8 dimnikov × 6 Sprite oblakov (canvas radialni gradient),
  cikel 6,5 s, dvig 7–13 m, mehak vhod/izhod; viden le 1825/~1900 (ne
  »danes«, ne mini-scena); skrit tudi v mini načinu; **nov privzeti orbit
  pogled s severa** (vas v ospredju, Kolpa desno, Brezov gozd za njim —
  prejšnji pogled z JV je gozd puščal ZA kamero); razhroščevalni vez
  window.__vscene (E2E).
- `src/components/museum/village-viewer.tsx`: **kartica stavbe v 3D
  pregledu (orbit)** — tap na stavbo: vrsta/ocene, tloris, razdalja, status
  2026 (🟢🟡🔴 + najbližja današnja), jedro/cerkev, P12 nota, povezava na
  Atlas; legenda: drevesa + dim (interpretacija); besedilo nalaganja
  posodobljeno.
- `src/components/museum/ar-time-machine.tsx`: kartica AR — »Kdo je tu
  živel?« nadgrajena z dokumentirano P12 ugotovitvijo (namesto TO_COLLECT).
- `src/lib/qa.ts`: +qa-p12-village-life (23. test): drevesa ≥ 1200,
  koordinate veljavne, 8 dimnikov z realnimi višinami, HOUSENO_FINDING si+en,
  podroben detail.
- `public/sw.js`: v18 → v19.

## 3. E2E preverba (agent-browser, dev)

- 3D vas: canvas 790×520 izrisan; drevesa POTRJENA s pikselno analizo po
  zoomu (277.227 zelenih pik = 43 % okvirja); v privzetem pogledu majhna
  a prisotna (1175 pik).
- Dim: časovna diferenca dveh posnetkov (1,6 s) → 164 spremenjenih pik,
  VSE znotraj canvasa nad jedrom (x 278–526, y 234–355) = animirani dim;
  `smokeGroup.visible`: 1825/1900 = true, 2026 = false ✓; wireframe duhovi
  2026 ✓.
- Tap na hišo (65 %, 40 % okvirja → stavba 24 m): kartica »Stavba ~1825 —
  kataster«, tloris, P12 nota ✓; radijo letnic 1825/~1900/danes ✓.
- Konzola: 0 napak.

## 4. Artefakti

- `/tmp` (session): hn-test/, hn-tiles/, dblob/, blind-*, dec-*, b111/b74,
  pt-01..08 (N083PT.pdf render), N083PS.pdf (143 str., 59 MB — večji deli
  v /tmp, niso commitani; PS je javno dostopen prek VAČ metode v
  research/p3/README.md).
- research/p12/README.md (ta datoteka).
