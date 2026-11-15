import io
p="worklog.md"
s=io.open(p,encoding="utf-8").read()
entry = """
## P262-START — NOTRANJOST-01738: 1837-NADALJEVANJE (s18 = Pag. 33/34 [~predvideno]) — 7 VPISOV (v6–v12) + DVA POROČNA DNEVA (4× 1. 2. 1837 + 3× 6. 2. 1837) + KRIŽAN-NIT-4.-BLOK — 2026-11-15

**Izvedba P262-lead-①** (P261-lead: s18 = Pag. 33+, REZERVA-md5 `1bb45fb3` že na disku). Branje s18 (498726 B, 2173×1500, MD5 **1bb45fb32482e5a0b46287c0d034ec7f** ✓ = P261-REZERVA 1:1), metoda-**AGENT-VIZIJA** (0 VLM klicev, 21 izrezov v `research/issue17/p262-work/`).

- **POPRAVEK METODE — ZAMIK IZREZOV:** prva serija `row6_L…row12_R` je bila **zamaknjena za 1 vrstico** (pasovi ujeti na meji). Rešitev: detekcija horizontalnih črt (profil tinte, x 400–2050) → **meje y = 285/432/578/724/870/1016/1162/1308/1462** (višina vrstice 146 px) → nova serija `r06L/R…r13L/R` (2×) + stolpec datumov 4× + `r06L_big` 4× + `z6_date` 8×.
- **POPRAVEK BRANJA DATUMA:** v6 je bilo najprej prebrano `6ten Februar` → **`1ten / Februar`** (4× zoom stolpca datumov + 4× r06L). S tem je kronologija **zaporedna**: **v6–v9 = 1. februar 1837** (`1ten dto`) + **v10–v12 = 6. februar 1837** (`6ten dto`). → **DVA POROČNA DNEVA** (4 + 3 poroke), vzorec kot P260 (27. februar ×5).
- **v13 = PRAZNA** → stran se zaključi z vrstico 12 (7 vpisov, ne 8).
- **7 VPISOV:** v6 Georg KRISCHAN 25 Krafing-25 (pripis `auf d. Grüblau`) × Anna KRISCHAN 27 Grüble-36 (Johann × Dorothea Krischan | Mathias × Dorothea Vrli) · v7 Peter Hufigh? 24 Kerkvippe-11 × Anna Bullog? 26 Grüble-5 (Mathias × Dorothea Hlebeg? | Mathias × Maria **Stampahar**) · v8 Johann KRISCHAN 30 **Grüble-63** × Anna Tilach? **18** Grüble-31 (**MLADOLETNA**) (Georg × Dorothea Krischan | Mathias × Anna Hofsig?) · v9 Mathias Bilighighk? 20 Gerssigh?-31 × Maria Jassha? 20 Vranovig-14 (Jacob × **Maria Novak** | Joseph × **Maria Horvath**) · v10 Martin POPISH 33 Gerssigh?-33 × Maria **Kral** 24 Grüble-17 (Marcus × Anna Brausfule | Stanislaus × Catharina Zulmingh?) · v11 Georg Sugel? 29 **Olok-2** × Maria **Vipauz** 27 Krafing-22 (Nicolaus × Catharina Marontigh? | Georg × Maria Safporigh?) · v12 Martin SIMONIGH 24 **Gradaz-20** × Agnes Jassha? 28 Vranovig-6 (Joseph × Maria Krischan | Stephan × Maria Nikelezhig?).
- **★★★★★ KRIŽAN-NIT = 4. BLOK h63:** v8 ženin Johann Krischan h63 (P253 m1 1873 + P260 m7 1836 + P261 m3 1837 + **P262 m8 1837**) — najdaljša hišna nit serije (1836→1880 = 44 let).
- **★★★★ VIPAUZ-NIT 1830→1837:** v11 nevesta Maria **Vipauz** (+ oče Georg + priča Marcus) ↔ P257 m1 1830 `[Vipavc?~Vipauz/Wipenz]`.
- **★★★ NOVE PONOVITVE:** `Jassha` ×2 (v9 Maria, v12 Agnes — verjetno 2 družini) + `Popish` ×3 (v10 ženin + oče + priča) + `Simonigh` ×3 (v12) + `Sugel` ×2 (v11) + `Horopigh`/`Gregorigh`/`Nikelezhig` (priče/očetje — `~-ič` kandidati).
- **KRAJI (7):** `Grüble` h5/h17/h31/h36/h63 + `Grüblau` = **varianta Grüble (= GRIBLJE!)** · `Krafing` h22/h25 [X-OPEN, cf. P257/P258 'Krajing'-garble] · `Kerkvippe` h11 [X-OPEN] · `Gerssigh` h31/h33 [X-OPEN] · `Olok` h2 (potrjeno P261) · `Gradaz` h20 (potrjeno P260/P261 — 2. hiša GRADAC!) · `Vranovig` h6/h14 [X-OPEN, nova vas v seriji?].
- **LISTINE:** 6/7 `ohne Aufgebot` (ista logika kot P261) + **v12 `Verkündigsschein` Pfarr Möttling (= METLIKA!) `dto 5. Feb. 1837`** = **1:1 dokaz čez-župnijskega lista** (nevesta iz Vranovičev!) + **v8 `Mit beider Eltern Einwilligung`** = **PRVO soglasje leta 1837** in se 1:1 ujema z mladoletnostjo neveste (18 let!) + v7 listina datirana `29. Juni/Jäner? 1837` **DUEL-X-OPEN** (post-datirana?).
- **DUHOVNIKI:** **Coop. Gregor Dolinijhigk [~Dolinšič]** (v6–v9, 4× — IDEM s P261 `Dolinšh[ek?]ff`!) + **župnik Georg … Pfarrer** (v10 — refined P261 `Georg [~Kraphovi(g/ž)?]`!) + v7/v11/v12 podpisi nečitljivi [X-OPEN].
- **X-OPEN-KRONOLOGIJA:** s18 (1./6. 2. 1837) je **pred** zadnjim vpisom s17 (P261 m5 = `1. Juni? d°` X-OPEN) → hipotezi: (a) napačno prebran datum na s17 (Jun ↔ Jän), (b) knjiga polnjena izven kronološkega reda.
- **ARTEFAKTI:** `research/issue17/p262-facts.json` (7 vpisov, bloki, niti, kraji, korpusUcinek 2077→2084/65→72, metodaDokaz, X-OPEN) + `research/issue17/p262-work/transcript.md` + 21 izrezov + 11 skript `scripts/tmp/p262_*.py`.
- **STANJE:** START-commit **1c64134** — **PUSHAN na GitHub** (`ab944b5..1c64134 HEAD -> main` ✓). Integracija v `parish.ts` / `marriage-early.ts` / `house-stories` / `qa-parish` / verifier / UI še **NI** izvedena (P262-INTEGRACIJA = naslednji korak; odprto vprašanje: ali bloki za 5 hiš v Grüble (h5/h17/h31/h36/h63) ali 7 blokov po vrstici — P261 je štel po hiši, ne po vrstici).
- deploy: GitHub-origin (push ✓ 1c64134) + GitLab-mirror-workflow + Vercel-avtomatsko.
"""
if not s.endswith("\n"): s += "\n"
s += entry
io.open(p,"w",encoding="utf-8",newline="\n").write(s)
print("ok", len(entry))
