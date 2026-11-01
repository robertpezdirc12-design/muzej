#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P177 — vstavi 1911 mrliški blok (13 Griblje-vpisov) v parish.ts + PIN-kaskada."""
import re

PARISH = "src/data/atlas/parish.ts"
QA = "src/lib/qa-parish.ts"

ANCHOR = '  // ——— P80 razširitev: POROČNA KNJIGA 04455 1873–1922 — okvir 1886 (skeni 61–65 == Pag. 60–64, vpisi 1–24; Pag. = sken − 1 v razponu 61–66) ———'

E = []


def e(house, scan, si, en):
    E.append(f'''  {{
    houseNo: "{house}",
    bookSignature: "04894",
    year: 1911,
    scan: {scan},
    page: {scan - 1},
    whatSi: "{si}",
    whatEn: "{en}",
    status: "DOCUMENTED",
  }},
''')


# h14 z13 — Ana BRINEC (s131)
e("14", 131,
  "umrla Ana BRINEC [★★ BRINEC-patroN-P173-vez (Marija-11-let-1908!) — 'Brinec' jasno @×2.2!], ¼ zemljiškova hči [~], 8 LET (26. 4., pokop 28. 4.) — Jetika; previden (1); Lausin Bitnar [~ #16]; ★★ h14 = 7. mrliški vpis (1896 + 1897-×2 + 1904 + 1907 + 1910 + 1911!) + ★★ BRINEC-×2-1911-h14 (z13-Ana-8-let + z48-Matija-4-let = brat+sestra?-PAR-7-mesecev-apart!) + Jetika-×3-1911 (z13 + z31 + z42!) + 1 + 4 hišna (14)",
  "died Ana BRINEC [★★ the BRINEC-godmother-P173-link (Marija-11-1908!) — 'Brinec' clear @×2.2!], a quarter-smallholder's daughter [~], 8 YEARS (Apr 26, buried Apr 28) — Jetika; previden (1); Lausin Bitnar [~ #16]; ★★ h14 = the 7th death entry (1896 + the 1897-×2 + 1904 + 1907 + 1910 + 1911!) + ★★ BRINEC-×2-1911-h14 (z13-Ana-8 + z48-Matija-4 = a brother+sister?-PAIR-7-months-apart!) + Jetika-×3-1911 + the 1 + 4 house number (14)")

# h14 z48 — Matija BRINEC (s134)
e("14", 134,
  "umrl Matija BRINEC [★★★ KROP-×3.0 — VLM-'Birčec'+panel-'Sofija'-ZAVRJENA: 'Brinec'-jasno + sin-stan = moško-ime!], ¼ zemljakov sin [~ 'Že gospodin sin' — ¼-G-SIMBOL-LEKSIKON], 4 LETA (9. 11., pokop 11. 11.) — Opeklina [★★★ 1.-TA-BOLEZEN-LINIJE = 3.-TRAUMA-SMRT (cf. 1908-'Z-VRCA-PADEL' + 1910-'Mrtvo najden'!)]; previden (.) [pika-dojenček-vzorec!]; Lausin Bitnar [~ #16]; ★★ h14 = 8. mrliški vpis = 2.-MESTO-LINIJE (cf. h35-10-REKORD + h46-8-isto-let0!) + ★★ BRINEC-×2-1911 + PUA-'Brinc'-0.8333-vez + 1 + 4 hišna (14)",
  "died Matija BRINEC [★★★ the CROP-×3.0 — the VLM-'Birčec'+panel-'Sofija'-REJECTED: 'Brinec'-clear + the son-status = a male name!], a quarter-smallholder's son [~], 4 YEARS (Nov 9, buried Nov 11) — Opeklina [★★★ the 1st SUCH-ILLNESS-of-the-line = the 3rd TRAUMA-DEATH (cf. 1908-'fell-from-a-cart' + 1910-'found dead'!)]; previden (.); Lausin Bitnar [~ #16]; ★★ h14 = the 8th death entry = the 2nd-PLACE-of-the-line (cf. h35-10-RECORD + h46-8-the-same-year!) + ★★ BRINEC-×2-1911 + the PUA-'Brinc'-0.8333-link + the 1 + 4 house number (14)")

# h19 z42 — Marija VRŠIČ (s134)
e("19", 134,
  "umrla Marija VRŠIČ [~ VLM-'Vrše'], vdova viškarica [~ 'vrtnarica'], 68 LET (26. 9., pokop 28. 9.) — Jetika; previden (1); Lausin Bitnar [★★ PODW-KROP — 'Lamblin Pihnar'-VLM-ZAVRJEN!]; ★★★ h19-KOREKCIJA (KROP-trak — 'h14'-VLM-raw-ZAVRJENO — 4/9-KURRENT!) = 4. mrliški vpis (3-pred) + h19-vez (poročna-1907-v4-Nikolaus-Hranc = 1. poročni dokaz h19-P136!) + 1 + 9 hišna (19)",
  "died Marija VRŠIČ [~ the VLM-'Vrše'], a widowed vineyard-worker [~ 'vrtnarica'], 68 YEARS (Sep 26, buried Sep 28) — Jetika; previden (1); Lausin Bitnar [★★ the WIDE-SIGNATURE-CROP — the VLM-'Lamblin Pihnar'-REJECTED!]; ★★★ the h19-CORRECTION (the track-crop — the VLM-raw-'h14'-REJECTED — the 4/9-KURRENT!) = the 4th death entry + the h19-link (the marriage-1907-v4-Nikolaus-Hranc = the 1st marriage-proof of h19-P136!) + the 1 + 9 house number (19)")

# h20 z51 — Peter PEZDIREC (s134)
e("20", 134,
  "umrl Peter PEZDIREC [★★★ KROP-×3.0-ŠIROK — VLM-'Perdih'-ZAVRJEN ('Pezdirec'-z-DESCENDER-jasno — NE-Perdinec-×159-dominanten!)], vdovec in viškar [~ 'vdovec in žitnar'], 73 LET (8. 12., pokop 10. 12.) — Naduha; previden (1); Lausin Bitnar [~ #16]; ★★★ PEZDIREC-×4-1911 (z24-Podzemelj + z26-h42 + z27-h48 + z51-h20 = 1.-LETO-×4-PRIIMKA-LINIJE!) + h20 = 6. mrliški vpis + 2 + 0 hišna (20)",
  "died Peter PEZDIREC [★★★ the WIDE-CROP-×3.0 — the VLM-'Perdih'-REJECTED ('Pezdirec'-with-the-z-DESCENDER-clear — NOT-Perdinec-×159-dominant!)], a widower and vineyard-worker [~ 'vdovec in žitnar'], 73 YEARS (Dec 8, buried Dec 10) — Naduha; previden (1); Lausin Bitnar [~ #16]; ★★★ PEZDIREC-×4-1911 (z24-Podzemelj + z26-h42 + z27-h48 + z51-h20 = the 1st YEAR-×4-SURNAME-of-the-line!) + h20 = the 6th death entry + the 2 + 0 house number (20)")

# h24 z56 — Marjeta JURAJEVIČ (s135)
e("24", 135,
  "umrla Marjeta JURAJEVIČ [~ VLM-'Margareta Juračevič' — KROP: 'arjeta' + 'Jura-jevič'; JURAJEVČIČ-×5-poročna-vez!], vdova viškarica [~ 'odločena ženihovica'], 76 LET (23. 12., pokop 24. 12.) — Naduha; previden (1); Lausin Bitnar [~ #16]; ★ h24 = 7. mrliški vpis + NADUHA-×3-1911-decembrska-gnezdov (z51 + z55 + z56!) + 2 + 4 hišna (24)",
  "died Marjeta JURAJEVIČ [~ the VLM-'Margareta Juračevič' — the crop: 'arjeta' + 'Jura-jevič'; the JURAJEVČIČ-×5-marriage-link!], a widowed vineyard-worker [~ 'odločena ženihovica'], 76 YEARS (Dec 23, buried Dec 24) — Naduha; previden (1); Lausin Bitnar [~ #16]; ★ h24 = the 7th death entry + the NADUHA-×3-1911-December-nests + the 2 + 4 house number (24)")

# h31 z54 — Janez POŽEK (s135)
e("31", 135,
  "umrl Janez POŽEK [★★★ KROP-trak — VLM-'Fošelj'-ZAVRJEN ('Požek'-ž-CARON-jasno!); POŽEK-veriga (P85-h79/h77-bajtarji-vez!)], oženjen ¼ zemljak [~ KROP], 61 LET (19. 12., pokop 21. 12.) — Pljučnica; previden (1); Lausin Bitnar [~ #16]; ★ h31 = 7. mrliški vpis (cf. 1910-z38-Martin-PAPIČ! KRIŽAN→KRALJ→PAPIČ→POŽEK-hiša-priimki?) + 3 + 1 hišna (31)",
  "died Janez POŽEK [★★★ the track-crop — the VLM-'Fošelj'-REJECTED ('Požek'-with-the-ž-CARON-clear!); the POŽEK-chain (the P85-h79/h77-cottagers-link!)], a married quarter-smallholder [~ the crop], 61 YEARS (Dec 19, buried Dec 21) — Pljučnica; previden (1); Lausin Bitnar [~ #16]; ★ h31 = the 7th death entry (cf. 1910-z38-Martin-PAPIČ!) + the 3 + 1 house number (31)")

# h34 z14 — Katarina HRUŠIČ (s131)
e("34", 131,
  "umrla Katarina HRUŠIČ [★★ K-A-panel-'H-s-prečko'; ★ P176-lead-'ŠILAK-vrnitev' — roj.-Šilak?-hipoteza (h34-klaster-Šilak/Čilak/Čišlak/Žilak + FILAK!)], vdova [~ 'vdovka'], 88 LET (30. 4., pokop 2. 5.) — Slabost; previden (1); Jos. Pumf [~ Punc-zmeda-6.-leto]; ★★ h34 = 7. mrliški vpis (1898-Filak + 1899-Čilak + 1901-Rampič + 1904-Čišlak + 1909-ŠILAK-DVOJČKI-×2 + 1911!) + ★ 88-let = NAJSTAREJŠA-1911 + pokop-2.-MAJA (2-dni-po-smrti!) + 3 + 4 hišna (34)",
  "died Katarina HRUŠIČ [★★ the K-A-panel-'H-with-the-crossbar'; ★ the P176-lead-'ŠILAK-return' — a born-Šilak?-hypothesis (the h34-cluster-Šilak/Čilak/Čišlak/Žilak + FILAK!)], a widow [~ 'vdovka'], 88 YEARS (Apr 30, buried May 2) — Slabost; previden (1); Jos. Pumf [~ the Punc-confusion-6th-year]; ★★ h34 = the 7th death entry (1898-Filak + 1899-Čilak + 1901-Rampič + 1904-Čišlak + the 1909-ŠILAK-TWINS-×2 + 1911!) + ★ the 88-years = the OLDEST-1911 + the burial-May-2 + the 3 + 4 house number (34)")

# h41 z46 — Neža HROVAT (s134)
e("41", 134,
  "umrla Neža HROVAT [★★ cf. P174-z47-Peter-HROVAT-'Afanas'-ZAVRJENA-vez!], ¼ zemljičeva hči [~ 'Že gospodinjska hiši' — ¼-G-SIMBOL-LEKSIKON], 12 LET (11. 10., pokop 13. 10.) — Hladni kašelj [★★★ KROP — VLM-'Hladno klatran'-ZAVRJENO = 1.-TA-BOLEZEN-LINIJE!]; previden (1); Lausin Bitnar [~ #16]; ★ h41 = 4. mrliški vpis + HLADNI-KAŠELJ = 1.-NOVA-BOLEZEN-1911 (2.-nova-z-OPEKLINO-z48 — 2-novi-v-1-letu!) + 4 + 1 hišna (41)",
  "died Neža HROVAT [★★ cf. the P174-z47-Peter-HROVAT-'Afanas'-REJECTED-link!], a quarter-smallholder's daughter [~ the ¼-G-SYMBOL-LEXICON], 12 YEARS (Oct 11, buried Oct 13) — Hladni kašelj [★★★ the CROP — the VLM-'Hladno klatran'-REJECTED = the 1st SUCH-ILLNESS-of-the-line!]; previden (1); Lausin Bitnar [~ #16]; ★ h41 = the 4th death entry + the COLD-COUGH = the 1st NEW-ILLNESS-1911 (the 2nd-with-OPEKLINA-z48 — 2-new-in-1-year!) + the 4 + 1 house number (41)")

# h42 z26 — Janez PEZDIREC (s132)
e("42", 132,
  "umrl Janez PEZDIREC [★★ z-DESCENDER-leksikon-P174/P175 — 'Pexdipec'-VLM], samotni viškar [~ 'samotni vajthar'/'samostni vinthar' — KROP], 53 LET (13. 7., pokop 15. 7.) — Slabost; previden (1); Lausin Bitnar [~ #16]; ★★ h42 = 6. mrliški vpis + PEZDIREC-×4-1911! + 4 + 2 hišna (42)",
  "died Janez PEZDIREC [★★ the z-DESCENDER-lexicon-P174/P175 — the VLM-'Pexdipec'], a single vineyard-worker [~ 'samotni vajthar' — the crop], 53 YEARS (Jul 13, buried Jul 15) — Slabost; previden (1); Lausin Bitnar [~ #16]; ★★ h42 = the 6th death entry + PEZDIREC-×4-1911! + the 4 + 2 house number (42)")

# h43 z47 — Nikolaj KUPANIČ (s134)
e("43", 134,
  "umrl Nikolaj KUPANIČ [★★★ KROP-×3.0 — VLM-'Nikolaj Nepomuk'-ZAVRJEN ('[K]upanič'-jasno — NI sv.-Janez-Nepomuk!) — NOV-PRIIMEK? [~ X-open]], ženjen viškar [~ 'sinjen vrhtar'], 69 LET (15. 10., pokop 17. 10.) — Vodenica [lexikon-vez: 1888-h7 + 1890-h16 + 1902-'Vodernica' + 1910!]; previden (1); Jos. Pumf [~ 'Rupf' — P/R-KURRENT]; ★ h43 = 4. mrliški vpis + 4 + 3 hišna (43)",
  "died Nikolaj KUPANIČ [★★★ the CROP-×3.0 — the VLM-'Nikolaj Nepomuk'-REJECTED ('[K]upanič'-clear — NOT-st.-Janez-Nepomuk!) — a NEW-SURNAME? [~ X-open]], a married vineyard-worker [~ 'sinjen vrhtar'], 69 YEARS (Oct 15, buried Oct 17) — Vodenica [the lexicon-link: 1888-h7 + 1890-h16 + 1902-'Vodernica' + 1910!]; previden (1); Jos. Pumf [~ 'Rupf' — the P/R-KURRENT]; ★ h43 = the 4th death entry + the 4 + 3 house number (43)")

# h46 z55 — Katarina HLOBUČAR (s135)
e("46", 135,
  "umrla Katarina HLOBUČAR [★★ KROP-×3.0 — VLM-'Vlobučar': H-prečka-jasna + P166-HLOBUČAR-vez (Marija-h47-1900 + Matija-h48-1901!); H/V-KURRENT-lekcija-2.-potrditev (cf. KAMBIČ-'Vambič'-P176!)], žena viškarica [~ 'omslena ženihovica'], 66 LET (22. 12., pokop 23. 12.) — Naduha; previden (1); Lausin Bitnar [~ #16]; ★★ h46 = 8. MRLIŠKI VPIS = 2.-MESTO-LINIJE (cf. h35-10-REKORD + h14-8-isto-let0!) + HLOBUČAR-×3-vez + 4 + 6 hišna (46)",
  "died Katarina HLOBUČAR [★★ the CROP-×3.0 — the VLM-'Vlobučar': the H-crossbar-clear + the P166-HLOBUČAR-link (Marija-h47-1900 + Matija-h48-1901!); the H/V-KURRENT-lesson-2nd-confirmation (cf. KAMBIČ-'Vambič'-P176!)], a vineyard-worker's wife [~ 'omslena ženihovica'], 66 YEARS (Dec 22, buried Dec 23) — Naduha; previden (1); Lausin Bitnar [~ #16]; ★★ h46 = the 8th DEATH ENTRY = the 2nd-PLACE-of-the-line (cf. h35-10-RECORD + h14-8-the-same-year!) + the HLOBUČAR-×3-link + the 4 + 6 house number (46)")

# h48 z27 — Vida PEZDIREC (s132)
e("48", 132,
  "umrla Vida PEZDIREC [~ VLM-'Vidou' — žensko-stan-čez-branju!], ¼ zemljakova hči, 3 MESECE (16. 7., pokop 17. 7.) — Božjast; previden (.); Lausin Bitnar [~ #16]; ★ h48 = 5. mrliški vpis + PEZDIREC-×4-1911 + otroška-smrt-×3-1911 = 23% (z13-8-let + z27-3-mes + z48-4-let!) + 4 + 8 hišna (48)",
  "died Vida PEZDIREC [~ the VLM-'Vidou' — the female-status-across-readings!], a quarter-smallholder's daughter, 3 MONTHS (Jul 16, buried Jul 17) — Božjast; previden (.); Lausin Bitnar [~ #16]; ★ h48 = the 5th death entry + PEZDIREC-×4-1911 + the child-deaths-×3-1911 = 23%! + the 4 + 8 house number (48)")

# h57 z31 — Marija MAVREŠIČ (s133)
e("57", 133,
  "umrla Marija MAVREŠIČ [★★★ KROP-×3.0 — VLM-'Mavrič'-ZAVRJEN (n/š-KURRENT; cf. z11-s131-Marjeta-MAVREŠIČ-ISTA-LETO!), roj. PEZDIREC [★★★ KROP — z-DESCENDER-jasno!]], žena ½ zemljakinja [~ 'omrčena'], 26 LET [★★★ KROP — VLM-'96'-ZAVRJEN! roj. 19. 4. 1884-marginalija → 1911−1884 = 26-SKLADNO!] (18. 3., pokop 20. 3.) — Jetika; previden (1); Lausin Bitnar [★★ PODW-KROP — 'LamblPithar'-VLM-ZAVRJEN!]; ★★★ MAX-ZOOM-FORENZIKA-3.-leto (95→35-z30 + 96→26-z31 — cf. P173-'81'→51 + P174-'84'→64 + P176-'86'→66!) + h57 = 5. mrliški vpis + roj.-PEZDIREC = 5.-kontakt-mreže-1911! + 5 + 7 hišna (57)",
  "died Marija MAVREŠIČ [★★★ the CROP-×3.0 — the VLM-'Mavrič'-REJECTED (the n/š-KURRENT; cf. z11-s131-Marjeta-MAVREŠIČ-the-SAME-year!), born PEZDIREC [★★★ the CROP — the z-DESCENDER-clear!]], a half-smallholder's wife [~ 'omrčena'], 26 YEARS [★★★ the CROP — the VLM-'96'-REJECTED! born Apr 19, 1884-margin → 1911−1884 = 26-CONSISTENT!] (Mar 18, buried Mar 20) — Jetika; previden (1); Lausin Bitnar [★★ the WIDE-SIGNATURE-CROP — the VLM-'LamblPithar'-REJECTED!]; ★★★ the MAX-ZOOM-FORENSICS-3rd-year (95→35-z30 + 96→26-z31!) + h57 = the 5th death entry + the born-PEZDIREC = the 5th-contact-of-the-1911-network! + the 5 + 7 house number (57)")


def main():
    src = open(PARISH, encoding="utf-8").read()
    assert "year: 1911" not in src.split('P80 razširitev')[0].split('04894')[-1] or True
    # varnost: 1911-04894 blok še ne obstaja
    assert len(re.findall(r'bookSignature: "04894",\n    year: 1911', src)) == 0, "1911 blok že obstaja!"
    block = (
        "\n  // ——— P177 razširitev: MRLIŠKA KNJIGA 04894 — leto 1911 (skeni 130–136; 58 vpisov / 13 Griblje / 12 hiš;"
        " h14-×2-BRINEC; meja 1911/12 = s135-INSIDE; dokaz: research/issue17/parish-death-1911.json) ———\n"
        + "".join(E)
    )
    assert ANCHOR in src, "sidro-ni-najdeno!"
    src = src.replace(ANCHOR, block + ANCHOR, 1)
    open(PARISH, "w", encoding="utf-8").write(src)
    n = len(re.findall(r'bookSignature: "04894",\n    year: 1911', src))
    print(f"parish.ts: 04894-1911 blokov = {n}")

    # ---- qa-parish.ts PIN-kaskada ----
    qa = open(QA, encoding="utf-8").read()
    a = qa.count("!== 1032")
    qa = qa.replace("!== 1032", "!== 1045")
    b = qa.count("!== 333")
    qa = qa.replace("!== 333", "!== 346")
    g = qa.count("(h.year ?? 0) >= 1911")
    qa = qa.replace("(h.year ?? 0) >= 1911", "(h.year ?? 0) >= 1912")
    c = qa.count("P176: + 12 blokov 1910 = 333!")
    qa = qa.replace("P176: + 12 blokov 1910 = 333!", "P176: + 12 blokov 1910 + P177: + 13 blokov 1911 = 346!")
    open(QA, "w", encoding="utf-8").write(qa)
    print(f"qa-parish.ts: 1032→1045 ({a}), 333→346 ({b}), guardi>=1912 ({g}), p80Death-sporočilo ({c})")

    # ---- skripte kaskada ----
    import glob
    v = s = 0
    for f in glob.glob("scripts/p1[5-7][0-9]_parish_death_*.py"):
        t = open(f, encoding="utf-8").read()
        t2 = t.replace("VITALS_TOTAL = 1032", "VITALS_TOTAL = 1045")
        t2 = t2.replace("BLOKI_04894 = 333", "BLOKI_04894 = 346")
        if t2 != t:
            open(f, "w", encoding="utf-8").write(t2)
            v += t.count("VITALS_TOTAL = 1032")
            s += t.count("BLOKI_04894 = 333")
    print(f"skripte: VITALS_TOTAL {v}, BLOKI {s}")


if __name__ == "__main__":
    main()
