#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P251 — posodobitev README.md na stanje po P251 (predzgodovina 13/13 KOMPLETNA)."""
ROOT = "/home/z/my-project"
RD = f"{ROOT}/README.md"
src = open(RD, encoding="utf-8").read()
delo = 0

def rep(a, b, label=""):
    global src, delo
    n = src.count(a)
    src = src.replace(a, b)
    delo += n
    print(f"  [{n}] {a[:64]} → {b[:44]} {label}")

# ——— 1. TOC ———
rep("raziskovalna linija v fazah (P1–P250)", "raziskovalna linija v fazah (P1–P251)", "(TOC!)")
rep("#zadnje-stanje-raziskave-po-p250--2026-11-11", "#zadnje-stanje-raziskave-po-p251--2026-11-11", "(TOC-anchor!)")
rep("## Zadnje stanje raziskave (po P250 · 2026-11-11)", "## Zadnje stanje raziskave (po P251 · 2026-11-11)", "(naslov!)")

# ——— 2. povzetek: po P250 → po P251 + vstavi P251 fragment ———
rep("> **11. november 2026 · po P250 · ★★★ POROČNA PREDZGOVINA 04455 = 1874",
    "> **11. november 2026 · po P251 · ★★★★★ POROČNA PREDZGOVINA 04455 = 13/13 KOMPLETNA — ZAKLJUČEK PREDZGOVINE! (P251: 4 vpisov m18–m21 BREZ preskokov — 6. leto! / 2 POLNA DVOJNA = 50%-REKORD (h13×h62 + h22×h50!) / ★★★★★ KONČNA-POTRDITEV-KNIŽNEGA-ODPIRANJA (s1 = vezalo → s2 = 'Pag. 1' → prva-marginala-18 = m1–m17-leta-1873-v-predhodniku!) / ★★★★★ 4-DVIGI-V-1-LETU (h22-ZA-25-LET-2.-NAJVEČJI!-h62-ZA-20!-h13-ZA-9!-h50-ZA-6!) / ★★★★★ DOVGAN-continuum-PODALJŠAN-NA-13-LET (1873–1885!) / ★★★★★ PEZDIRC-13/13-LET-VSEH (Maria-PEGDIRE-h50-oče-Marcus!) / ★★★ MEJA-1873/74 = s2-MID/DNO = 13.-VARIANTA-1:1-RE! / FOLIACIJA-1/1 → SKUPAJ 29/29-V-ZAPOREDNIH-LETIH! / ★★★ m19-KLAGENFURT-MIGRANT-IBERER-1.-TE-VRSTE!-+ m21-VETRHVIŠČE-X-OPEN!) · tsc 0 · lint 0 · QA živo · ★★★ POROČNA PREDZGOVINA 04455 = 1874",
    "(povzetek-lead!)")

# ——— 3. tabela linij: pokritost + status ———
rep("| **leta 1885→1874 = 12/13** (P238:",
    "| **leta 1885→1873 = 13/13 KOMPLETNA — PREDZGOVINA ZAKLJUČENA!** (P238:", "(tabela-pokritost!)")
rep("FOLIACIJA-5/5-28/28!-DOVGAN-12-let!)",
    "FOLIACIJA-5/5-28/28!-DOVGAN-12-let! · P251-KONČNO: 4-vpisi-m18–m21-BREZ-preskokov-6.-leto!-2-POLNA-DVOJNA-50%-REKORD-h13×h62-h22×h50!-KNIŽNO-ODPIRANJE-marginala-18-m1–m17-v-predhodniku!-MEJA-s2-MID/DNO-13.-VARIANTA-RE!-4-DVIGI-h22-25-LET-h62-20!-DOVGAN-13-LET!-PEZDIRC-13/13-VSEH!-FOLIACIJA-1/1-29/29!)", "(tabela-P251!)")
rep("| 🔄 P238–P250 — LINIJA TEČE (1873 odprto) |",
    "| ✅ P238–P251 — PREDZGOVINA KOMPLETNA (13/13 · 1873–1885) |", "(tabela-status!)")

# ——— 4. korpus ———
rep("**Korpus (po P250):** **2008 vitalov**", "**Korpus (po P251):** **2012 vitalov**", "(korpus!)")
rep("265 poročnih blokov 04455 (1886–1922 + predzgodovina 1874–1885",
    "269 poročnih blokov 04455 (1886–1922 + predzgodovina 1873–1885", "(korpus-04455!)")
rep("(po P250: vitals 2008 · 04455 265 · h42/h43-firstYear-1874!)",
    "(po P251: vitals 2012 · 04455 269 · h13/h22/h50/h62-firstYear-1873!)", "(pt-luknja-note!)")

# ——— 5. odprto ① ———
rep("① **poročna 04455 predzgodovina 1873 = 1/13 odprtih let (ZADNJE!)**",
    "① ~~poročna 04455 predzgodovina 1873–1885~~ — **ZAKLJUČENA (P251): 13/13 let!**", "(odprto-①!)")
rep("— zadnja odprta matrična linija; ② P251+ možnosti po worklogu: leto-1873 (13/13 — ZAKLJUČEK-predzgodovine!) · predhodnik-knjige-04455 · hišne-zgodbe-globlje — **ZAKLJUČENE LINIJE:",
    "— zadnja odprta matrična linija ZAKLJUČENA; naslednje možnosti (po izbiri uporabnika, P252+): **SINTEZA-PREDZGOVINE** (cf.-P236-krstna-15/15-sinteza!-mreže-hiš/PEZDIRC-13/13/DOVGAN-13-let/folijacija-29/29!) · hišne-zgodbe-globlje · predhodnik-knjige-04455 (m1–m17-leta-1873-v-predhodniku!) — **ZAKLJUČENE LINIJE:", "(odprto-možnosti!)")

# ——— 6. dokazi ———
rep("vsaka faza P0–P236 ima dokaz", "vsaka faza P0–P251 ima dokaz", "(dokazi!)")

# ——— 7. Zadnje stanje: vstavi P251 bullet na vrh ———
anchor = "## Zadnje stanje raziskave (po P251 · 2026-11-11)\n"
bullet = "- **P251 (POROČNA PREDZGOVINA 04455, leto 1873 = 13/13 KONČNO — ZAKLJUČEK PREDZGOVINE!) ZAKLJUČENA** — s1–s2 (+ s3-križna-meja; md5-2×-neodvisen-prenos-1:1!-Read-očesa-NAJPREJ-×2-P244-LEKCIJA!-VLM-pass-1-×2 + solo-×12 + očesi-deciser-×6 + letterform-referenca-m20-'22'!-kronologija-Juni<Aug<Nov!): **4 vpisov m18–m21 BREZ preskokov (6. leto!-NODAT-×0!)** · ★★★★★ **KONČNA-POTRDITEV-KNIŽNEGA-ODPIRANJA** (s1 = vezalo-knjige → s2 = 'Pag. 1' = prva-tabelarna-stran → **prva-marginala-18** = m1–m17-leta-1873-v-predhodniku-knjige!) · **2 POLNA DVOJNA = 50%-REKORD** (m18: h13-Gabovšič-42 × h62-Hrižan-32!-m20: h22-Milek-39-Innmann × h50-Pegdire-26!) · ★★★★★ **4-DVIGI** (h22-ZA-25-LET-2.-NAJVEČJI!-h62-ZA-20-LET!-h13-ZA-9!-h50-ZA-6!) · ★★★★★ **DOVGAN-13-LET (1873–1885!)** + **PEZDIRC-13/13-LET-VSEH** (Maria-PEGDIRE!) · ★★★ MEJA-1873/74 = s2-MID/DNO = 13.-VARIANTA-1:1-RE! · FOLIACIJA-1/1 → 29/29-8.-LETO! · m19-KLAGENFURT-IBERER-1.-TE-VRSTE [X-OPEN!] · korpus **2012/269** · sidra-262-1873:4! · dobe-236-66-pred-linijskih! · MILIČ-247! · verifier-21/21-s-LIVE + stari-verifikatorji-13/13-311-preverjanj! · tsc-0-lint-0-browser-OK!\n"
i = src.find(anchor)
assert i >= 0, "anchor Zadnje stanje ne najden!"
src = src[:i + len(anchor)] + bullet + src[i + len(anchor):]
delo += 1
print("  [1] P251-bullet na vrh Zadnje stanje")

open(RD, "w", encoding="utf-8").write(src)
print(f"\nSKUPAJ: {delo} sprememb")
