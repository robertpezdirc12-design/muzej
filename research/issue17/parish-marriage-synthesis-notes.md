# P152 — SINTEZA poročne linije 04455 (1886–1922) = kuratorsko zaprtje knjige

Datum: 28. 10. 2026 · tip: SYNTHESIS-M04455 · status: COMPLETE
Vir: 37 letnih dokazov `parish-marriage-1886..1922.json` (P115–P151) + runtime-korpus `parish.ts`
Metoda: MERI — **NI novih paleografskih branj, NI novih skenov** (kompilacija + preracun!)

## 1. Zaključek linije

Poročna knjiga 04455 je po P151 (leto 1922, naslovnica »Podzemelj P 1873–1922«) **KOMPLETNO
prebrana**: 37/37 let (1886–1922) v 37 zaporednih fazah (P115 → P151). Korpus: **714 vitalov ·
197 blokov 04455 · 190 poročnih sidra · 77 gribeljskih hiš** (p80-vzorec) · PT-luknja 13.
Od teh 197 blokov sta **2 pred-linijska** (1882 + 1885 — korpusni bonus iz sidranskih faz),
195 pa pripada 37-letni liniji. Dve leti imata **0 blokov**: 1901 (P130) in 1918 (P147).

## 2. Demografski lok (sinteza po dobah)

| doba | leta | # | vpisi | avg/leto | bloki |
|---|---|---|---|---|---|
| predvojna | 1886–1913 | 28 | 442 | 15,79 | 162 |
| prva svetovna | 1914–1918 | 5 | 29 | **5,80** | 7 |
| povojni boom | 1919–1922 | 4 | 121 | **30,25** | 26 |

- **WWI-kolaps**: 1914:7 → 1915:6 → 1916:4 → 1917:8 → 1918:4 (dvojni dno 1916 + 1918;
  avg 5,8 = 37 % predvojne ravni). Vojni žig: Feldsuperiorat Graz št. 2531, sanitetni vojaki,
  orožniški naredniki, vojaška dvolistina №3/1918.
- **Povojni boom**: 1919:**40** (rekord linije) + 1920:37 + 1921:31 = tri največja leta ZAPORED
  (nadomestne poroke); 1922:13 — leto se **prekine 27.8.1922** (konec knjige!). Polnih-let
  sredstvo 1919–1921 = 36,0.
- **Vrzel Griblja**: bloki == 0 v 1901 in 1918; povratek 1919 z **10 bloki = največji
  enoletni priliv** linije.

## 3. Ekstremi in vzorci

- **Ekstremi vpisov**: max 40 (1919) · min 4 (1916 + 1918) · skupaj **592** vpisov
  (avg 16,0/leto).
- **Osebni ekstremi**: najstarejši ženin 67 let (Jurij Jakofčič-senior, 1922 №10, H-dvom
  1866/67-razlika-11!) · najmlajša nevesta 16 let (1920 №8 Zunič; 1922 dve 16-letnici) ·
  mladoletnost-val v WWI/boom (očetova dovoljenja, okrajno-sodiščna dovoljenja).
- **Sibling-swap** dogodki: 1920 №2/№3 (Škala↔Berkoper) + 1922 №4/№5 (Berkovec↔Brodarič —
  isti dan + isti priči + ista starša!).
- **Družinske mreže** (do P151): KRIŽAN ×160 · PEZDIRC ×152 · JAKOFČIČ ×151 · ŽELJKO ×148 ·
  KAMBIČ ×56 · ŽUPANIČ ×36 · KRALJ ×34 · GRABRIJAN ×27.
- **Novi priimki**: rekord P151 = 16 novih v enem letu (po ~6 P150).
- **Migracijski robovi**: 1. ameriško-rojena oseba (1918 №2 Gregorič) · 2 hrvaški referenci
  (1921 Kaluka-nevesta Lipik/Lipnik + 1922 Mala Paka-ženin) · učiteljski par poročen v
  **Ljubljani** (1920 Vode × Štefanc — 2. vpis brez številke!).
- **Institucionalni lok** (duhovniki): Jos. Rauy (P79-era) → Miklavčič → **Cerar-dominanta**
  (~1907–1921) → **P. Remigi Jereb** (od 10.10.1921 — 1. opazovani prehod!) → **P. Edvard
  Raustelar O.F.M. Brežje** (1922 — 1. frančiškan + 'per delegationem').
- **Kalendarna** (44 zabeleženih vpisov kasnejših faz): PONEDELJEK 21 (48 %!) = 1. dan
  porok · NEDELJA 13 · SREDA 4 · PETEK 3 (1. PETEK 14.5.1920!) · TOREK 2 · ČETRTEK 1 ·
  **SOBOTA 0/44**. Za 548/592 vpisov dan NI zabeležen (zgodnje faze).
- **Postne/poletne vrzeli** vsako leto; najdaljša poletna 113 dni (1921).

## 4. Metrična legenda (POMEMBNO!)

| metrika | vrednost | pomen |
|---|---|---|
| evidenceEntries | **592** | vpisi prebrani na polnih straneh (vsi, ne samo Griblje) |
| blocks (parish.ts) | **195** (linija) + 2 (pred-linija) = **197** | vpisi z gribeljsko HIŠNO ŠT. (ženin/nevesta/priča/starši) |
| stats.gribljeMarriages | 127 | zgodnja metrika: poroke OSEB iz Griblje-vasi |

Razlika 195 − 127 ≈ 68 = bloki iz prič/staršev/sorojencev z gribeljskimi hišnimi številkami.
Stats-ključi se spreminjajo po fazah (`gribljeMarriages` → `gribljeBlocks`/`gribljeBlocksNew`
→ `gribljeEntries`) — **razlika je metrična, ne napaka!** Dokumentirana v honesty sinteze.

## 5. Znane pomanjkljivosti (honesty)

1. P152 NI novih branj — nižja raven dokazovanja kot letne faze (kompilacija).
2. 1906 intra-datotečno neskladje: `stats.gribljeBlocks=6` vs `gribljeBlocksNew=5` vs
   kumulativ `bloki04455 115→120 (+5)` — **avtoritativno 5** (parish.ts potrjuje); stari
   dokaz NI popravljen (P152 ne revidira zgodovine).
3. dayOfWeek pokriva samo 44/592 vpisov.
4. Era-meje so kuratorske konvencije, ne arhivske.
5. avg-boom 30,25 vključuje delno 1922 (do 27.8.).

## 6. Odprta vprašanja → naslednja faza

- **Nova knjiga?** mrliška **04456/04894** (okvir 1886, P80 vzorec) ALI krstna
  **04105-nadaljevanje** (čez 1919 — knjiga se konča 1919!) — **odločitev uporabnika**.
- Človeška paleografska potrditev VLM prepisov (issue #12) — odprta za vseh 592 vpisov.
- Metrična sprava zgodnjih faz — nizka prioriteta (razlika dokumentirana).

---
Dokaz: `research/issue17/parish-marriage-synthesis.json` · verifikator:
`scripts/p152_parish_marriage_synthesis.py --check --live` (I1–I12) ·
runtime-kontrola: `qa-p152-parish-marriage-synthesis` (153. test) v `src/lib/qa-parish.ts`.
