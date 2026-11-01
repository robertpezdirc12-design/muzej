#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P177 — build dokaz parish-death-1911.json (p174-vzorec).
Vhod: /tmp/p177/rows1911.json (58 vrstic) + K-korekcije (16 kropov lastne
vizije @×2.2/×3.0 + 6 kompozit-panelov VLM!).
K-KOREKCIJE-1911 (VLM-raw → diag/max-zoom):
  z14-hrušič: h34 + '2 maj' pokop + ŠILAK-vrnitev-[~]
  z24: vas 'Lodnemej'→PODZEMELJ (KROP!); 'vajtharica'→viškarica [~]
  z26: 'vajthar'→viškar [~]
  z27: 'Vidou'→Vida [~]
  z30: vas 'Griblje'→GRIŠIČE? (KROP! P131-precedent); '95 let'→35 LET
       (KROP + roj. 4.8.1876-forenzika!); roj. PLAT [~ Plut]; 'Rauq'→Jos. Pumf
       (PODW-KROP!)
  z31: '96 let'→26 LET (KROP + roj. 19.4.1884-forenzika!); 'Mavrič'→
       MAVREŠIČ [~]; +roj. PEZDIREC (KROP!); 'Pithar'→Bitnar (PODW-KROP!)
  z36: vas 'Griblje'→GRIŠIČE? (KROP!)
  z42: h14→h19 (KROP! 4/9-KURRENT!); 'Vrše'→Vršič [~]; 'vrtnarica'→viškarica [~]
  z46: 'Hladno klatran'→HLADNI KAŠELJ (KROP! 1.-TA-BOLEZEN!)
  z47: 'Nepomuk'→KUPANIČ (KROP! @×3.0!); 'sinjen vrhtar'→ženjen viškar [~];
       'Rupf'→Jos. Pumf [~]
  z48: 'Birčec'→BRINEC (KROP!); ime-'Sofija'→Matija (sin-stan!); 'Pihnar'→
       Bitnar [~]; previden '.'!
  z51: 'Perdih'→PEZDIREC (KROP! z-DESCENDER-leksikon!); 'žitnar'→viškar [~]
  z54: 'Fošelj'→POŽEK (KROP!); h31-POTRJENA (KROP!)
  z55: 'Vlobučar'→HLOBUČAR (KROP! H-prečka + P166-vez!); 'omslena ženihovica'→
       žena viškarica [~]
  z56: 'Margareta Juračevič'→Marjeta JURAJEVIČ [~]; 'ženihovica'→viškarica [~]
"""
import json

IN = "/tmp/p177/rows1911.json"
OUT = "/home/z/muzej/research/issue17/parish-death-1911.json"

SCAN = {"s130": 130, "s131": 131, "s132": 132, "s133": 133, "s134": 134, "s135": 135}

MESEC_REK = {
    (1, 1): "Januar", (1, 2): "Januar", (1, 3): "Januar", (1, 4): "Januar", (1, 5): "Januar",
    (6, 6): "Marec", (7, 9): "Marec", (10, 13): "April", (14, 14): "April",
    (15, 15): "Maj", (16, 17): "Maj",
    (18, 19): "Maj", (20, 20): "Junij", (21, 29): "Julij",
    (30, 33): "Avgust", (34, 41): "September",
    (42, 42): "September", (43, 47): "Oktober", (48, 53): "December-nadalj? -> Novemb/Dec",  # fix below
    (54, 56): "December", (57, 58): "December",
}

# ročna meja: z48 = Novemb. 9 (raw), z51 = December 8 (raw) → z49/z50 = November
def mesec_for(zap, raw):
    zap = int(zap)
    if zap <= 5:
        return "Januar"
    if 6 <= zap <= 9:
        return "Marec"
    if zap == 10 or zap == 11 or zap == 12 or zap == 13 or zap == 14:
        return "April"
    if 15 <= zap <= 19:
        return "Maj"
    if zap == 20:
        return "Junij"
    if 21 <= zap <= 29:
        return "Julij"
    if 30 <= zap <= 33:
        return "Avgust"
    if 34 <= zap <= 42:
        return "September"
    if 43 <= zap <= 47:
        return "Oktober"
    if 48 <= zap <= 50:
        return "November"
    return "December"


K = {
    13: {"ime": "Ana BRINEC [★★ K-A-panel + raw — 'Brinec' jasno; BRINEC-patroN-P173-vez!]",
         "stan": "¼ zemljiškova hči [~ '1/4 zemlješkova' — ¼-ULOMEK-LEKSIKON]",
         "duhovnik": "Lausin Bitnar [~ #16 — 'Lamlin Bitmar'-VLM]",
         "opomba": "★★ h14 = 7. mrliški vpis (1896 + 1897-×2 + 1904 + 1907 + 1910 + 1911-z13!) + BRINEC-h14-vez (poročna-1908-v17-'Dorothea-PEZDIREC-h14' + z48-Matija-BRINEC-ISTO-LET0!)"},
    14: {"ime": "Katarina HRUŠIČ [~ K-A-panel-'H-s-prečko'; ★★ P176-lead-'ŠILAK-vrnitev' — roj.-Šilak?-hipoteza: h34-klaster-Šilak/Čilak/Čišlak/Žilak!]",
         "stan": "vdova [~ 'vdovka'-raw]",
         "duhovnik": "Jos. Pumf [~ #? — Punc-zmeda-6.-leto]",
         "opomba": "★★ h34 = 7. mrliški vpis (1898-Filak + 1899-Čilak + 1901-Rampič + 1904-Čišlak + 1909-ŠILAK-DVOJČKI-×2 + 1911!) + pokop 2. MAJA (smrt 30. aprila!)"},
    26: {"ime": "Janez PEZDIREC [★★ z-DESCENDER-leksikon-P174/P175 — 'Pexdipec'-VLM]",
         "stan": "samotni viškar [~ 'samotni vajthar'/'samostni vinthar' — KROP-cel-z26]",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★ h42 = 6. mrliški vpis + PEZDIREC-×4-1911 (z24-Podzemelj + z26 + z27 + z51!)"},
    27: {"ime": "Vida PEZDIREC [~ 'Vidou'-VLM; K-A-'Vidov'-×2-beri — žensko-stan!",
         "stan": "¼ zemljakova hči",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★ h48 = 5. mrliški vpis + PEZDIREC-×4-1911! + 3.-OTROŠKA-SMRT-1911 (23%)"},
    31: {"ime": "Marija MAVREŠIČ [★★★ KROP-cel-z31 — 'Mavrič'-VLM-ZAVRJEN (n/š-KURRENT); cf. z11-s131-Marjeta-MAVREŠIČ-ISTA-LETO!], roj. PEZDIREC [★★★ KROP — 'Pezdirec'-jasno-z-DESCENDER!]",
         "stan": "žena ½ zemljakinja [~ 'omrčena ½ zemljačinja' — KROP-'žena'!]",
         "starost": "26 LET [★★★ KROP-cel-z31-starost — '96'-VLM-ZAVRJEN! roj. 19. 4. 1884 (KROP-marginalija!) → 1911−1884 = 26-SKLADNO!]",
         "duhovnik": "Lausin Bitnar [★★★ PODW-KROP — 'LamblPithar'-VLM-ZAVRJEN!]",
         "opomba": "★★★ MAX-ZOOM-FORENZIKA-1911 (3. leto: 95→35-z30 + 96→26-z31!) + h57 = 5. mrliški vpis + roj.-PEZDIREC = PEZDIREC-mreža-5.-kontakt-1911!"},
    42: {"ime": "Marija VRŠIČ [~ 'Vrše'-VLM-trak]",
         "stan": "vdova viškarica [~ 'vdova vrtnarica'/'vdova viškarica' — KROP-trak]",
         "duhovnik": "Lausin Bitnar [★★ PODW-KROP — 'Lamblin Pihnar'-VLM-ZAVRJEN!]",
         "opomba": "★★★ h19 (KROP-trak — '14'-VLM-raw-ZAVRJENO — 4/9-KURRENT!) = 4. mrliški vpis (3-pred: poročna-1907 + krsti?) + h19-vez (poročna-1907-v4-Nikolaus-Hranc!)"},
    46: {"ime": "Neža HROVAT [★★ cf. P174-z47-Peter-HROVAT-'Afanas'-ZAVRJENA-vez!]",
         "stan": "¼ zemljičeva hči [~ 'Že gospodinjska hiši'-VLM — ¼-G-SIMBOL-LEKSIKON]",
         "starost": "12 LET",
         "bolezen": "Hladni kašelj [★★★ KROP-cel-z46 — 'Hladno klatran'-VLM-ZAVRJENO = 1.-TA-BOLEZEN-LINIJE!]",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★ HLADNI-KAŠELJ = 1.-TA-BOLEZEN-1911 + h41 = 4. mrliški vpis"},
    47: {"ime": "Nikolaj KUPANIČ [★★★ KROP-cel-z47 — 'Nepomuk'-VLM-ZAVRJEN @×3.0 ('upanič'-jasno!); NI sv.-Janez-Nepomuk!",
         "stan": "ženjen viškar [~ 'sinjen vrhtar'-VLM]",
         "duhovnik": "Jos. Pumf [~ 'Jos. Rupf' — P/R-KURRENT-zmeda]",
         "opomba": "★★ NIKOLAJ-KUPANIČ = NOV-PRIIMEK-LINIJE? [~ X-open] + h43 = 4. mrliški vpis + Vodenica-leksikon (1888-h7 + 1890-h16 + 1902 + 1910-Čišlak-'Vodernica'!)"},
    48: {"ime": "Matija BRINEC [★★★ KROP-cel-z48 — 'Birčec'/'Sofija'-VLM-ZAVRJENA ('Brinec'-jasno + sin-stan = moško-ime!)]",
         "stan": "¼ zemljakov sin [~ 'Že gospodin sin'-VLM; K-C-'¼ gemljatov'-potrditev!]",
         "starost": "4 LETA",
         "bolezen": "Opeklina [★★ KROP-cel-z48-bolezen — '[~]eklina'-jasno!]",
         "previden": ".",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★★ OPEKLINA = 1.-TA-BOLEZEN-LINIJE = 3.-TRAUMA-SMRT (cf. 1908-'Z-VRCA-PADEL' + 1910-'Mrtvo najden'!) + ★★ h14-×2-1911 = BRAT-SESTRA-PAR? (z13-Ana-8-let + z48-Matija-4-let — BRINEC-×2-ISTA-HIŠA!) + previden-pika (dojenček-vzorec!)"},
    51: {"ime": "Peter PEZDIREC [★★★ KROP-cel-z51 — 'Perdih'-VLM-ZAVRJEN ('Pezdirec'-z-DESCENDER-jasno — NE Perdinec-×159!)]",
         "stan": "vdovec in viškar [~ 'vdovec in žitnar'/'rdovec in vžiglavka' — KROP]",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★★ PEZDIREC-×4-1911 (z24-Podzemelj-h10 + z26-h42 + z27-h48 + z51-h20!) = 1.-LETO-×4-PRIIMKA + h20 = 6. mrliški vpis"},
    54: {"ime": "Janez POŽEK [★★★ KROP-trak — 'Fošelj'-VLM-ZAVRJEN ('Požek'-ž-CARON-jasno!); POŽEK-veriga-P85-vez (h79/h77-bajtarji!)]",
         "stan": "oženjen ¼ zemljak [~ 'oženjen ¼ gemljak' — KROP]",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★ h31 = 7. mrliški vpis (cf. 1910-z38-Martin-PAPIČ-h31! KRIŽAN→KRALJ→PAPIČ→POŽEK-hiša-4-priimka?)"},
    55: {"ime": "Katarina HLOBUČAR [★★ KROP-cel-z55 — 'Vlobučar'-VLM: H-prečka-@×3.0 + P166-HLOBUČAR-vez (Marija-h47-1900 + Matija-h48-1901!); H/V-KURRENT-lekcija-2.-potrditev (cf. KAMBIČ-'Vambič'!)]",
         "stan": "žena viškarica [~ 'omslena ženihovica' — KROP]",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★ h46 = 8. MRLIŠKI VPIS (2. MESTO-linije — cf. h35-10-REKORD + h14-8-isto-let0!) + HLOBUČAR-×3-vez"},
    56: {"ime": "Marjeta JURAJEVIČ [~ 'Margareta Juračevič'-VLM — KROP: 'arjeta' + 'Jura-jevič'; JURAJEVČIČ-×5-poročna-vez!]",
         "stan": "vdova viškarica [~ 'odločena ženihovica' — KROP]",
         "duhovnik": "Lausin Bitnar [~ #16]",
         "opomba": "★★ h24 = 7. mrliški vpis + Naduhba-×3-1911 (z51 + z55 + z56 — decembrska-gnezdov!?)"},
}

GRIB_ZAPS = {13, 14, 26, 27, 31, 42, 46, 47, 48, 51, 54, 55, 56}
VAS_FIX = {24: "Podzemelj", 30: "Grišiče?", 36: "Grišiče?"}
HISA_FIX = {42: "19"}
STAROST_FIX = {31: "26 LET [★★★ KROP! roj. 19. 8. 1884 — 1-dan-pred-27.-ROJSTNIM-DNOM!]", 30: "35 LET [★★★ KROP! roj. 4. 8. 1876]"}
IME_FIX = {
    24: "Ana PEZDIREC [★★ z-DESCENDER-leksikon]",
    30: "Marija TAPRIČ [~ 'Taparič'], roj. PLAT [~ 'Plut' — KROP!]",
    36: "Marija TAPRIČ [~ 'Taparič']",
}
DUH_FIX = {14: "Jos. Pumf [~ 'Punc-zmeda'-6.-leto]", 24: "Jos. Pumf [~ 'Pung']", 30: "Jos. Pumf [★★ PODW-KROP — 'Rauq'-VLM-ZAVRJEN!]", 47: "Jos. Pumf [~ 'Rupf']"}
BOLEZEN_FIX = {30: "Vnetje krvi [~ 'Vmetje'-KROP-robov]"}
POKOP_FIX = {14: "2. maja", 5: "2. februarja [1912 — pokop-33-dni-po-smrti!]", 58: "2. januarja 1912 [EKSPPLICITNO-'1912'!]"}


def main():
    rows = json.load(open(IN, encoding="utf-8"))
    entries = []
    grib_n = 0
    for i, r in enumerate(rows, 1):
        zap = int(str(r["zap"]).rstrip("."))
        tag = r["scan_tag"]
        scan = SCAN[tag]
        vas = r.get("vas") or ""
        ime = r.get("ime") or ""
        hisa = r.get("hisa") or r.get("hisna") or ""
        starost = r.get("starost") or ""
        bolezen = r.get("bolezen") or ""
        previden = r.get("previden") or ""
        duh = r.get("duhovnik") or ""
        pokop = r.get("pokop") or ""
        is_grib = zap in GRIB_ZAPS and "Griblje" in vas
        k = K.get(zap, {})
        e = {
            "row": i,
            "zap": zap,
            "houseNo": str(k.get("houseNo", HISA_FIX.get(zap, hisa))),
            "bookSignature": "04894",
            "year": 1911,
            "scan": scan,
            "page": scan - 1,
            "mesec": mesec_for(zap, r.get("mesec")),
            "smrt": str(r.get("smrt") or "").rstrip("."),
            "pokop": POKOP_FIX.get(zap, str(pokop).rstrip(".")),
            "vas": VAS_FIX.get(zap, vas),
            "ime": IME_FIX.get(zap, k.get("ime", ime)),
            "stan": k.get("stan", r.get("stan") or ""),
            "starost": STAROST_FIX.get(zap, k.get("starost", starost)),
            "bolezen": BOLEZEN_FIX.get(zap, k.get("bolezen", bolezen)),
            "previden": k.get("previden", previden),
            "duhovnik": DUH_FIX.get(zap, k.get("duhovnik", duh)),
            "opomba": k.get("opomba", "ne-Griblje; VLM-raw"),
        }
        if zap == 4:
            e["opomba"] = "★★★ MRTVOROJENEC + BREZ-PODPISA ('—' + KROP-trak-k10: 'J. Škal [~ Škaf] / ¼ zemljaka dete' + rdeči-✓!) — 2.-MRTVOROJENEC-LINIJE (cf. 1908-r53!) + z3-1912-DRUGI-v-2-MESECIH (diag-s135!)"
        if is_grib:
            grib_n += 1
            if not k:
                e["opomba"] = "Griblje; VLM-raw (brez-dodatne-forenzike)"
        entries.append(e)

    grib = [e for e in entries if e["vas"].startswith("Griblje")]
    hise = sorted({e["houseNo"] for e in grib}, key=int)

    dokaz = {
        "status": "SAMPLE-TRANSCRIPTION-D1911",
        "generated": "2025-11-01",
        "phase": "P177",
        "source": "matricula-online.eu 04894 (Podzemelj, mrliška 1886–1924), skeni 130–136",
        "frame": {
            "leto": 1911,
            "vpisi": 58,
            "zap_oštevilčenih": 58,
            "neštevilčenih": 0,
            "griblje_vpisi": len(grib),
            "hise": len(hise),
            "ponovitve": f"h14-×2 (z13-Ana-8-let + z48-Matija-4-let BRINEC = brat+sestra?-PAR!) — 8. leto zapored hiša-×2 (1904→1911); rast {len(hise)}",
            "skeni": "s130-dno (z1–5) + s131 (z6–17) + s132 (z18–29) + s133 (z30–41) + s134 (z42–53) + s135 (z54–58); novi: s133–s136",
            "griblje_hise": ",".join(hise),
            "meja_1910_11": "s130-INSIDE — P176-potrditev-re-potrjena ('~1911~' VELIKA v praznem bandu-k6 + restart z49–54→z1 = 8. STIL mid-scan-band — diag-s130-spodaj!)",
            "meja_1911_12": "s135-INSIDE ('1912' VELIKA v praznem bandu-k5 + restart z58→z1 + Bitnar-podpis-v-meja-bandu = 2. POTRDITEV STILA-8! P176-lead-'[?]' REŠEN!)",
            "rast": "10→12→16→12→13",
        },
        "entries": entries,
        "excluded": [
            {"id": "X1", "opis": "z24-ana-PEZDIREC = PODZEMELJ h10 (KROP-trak — 'Lodnemej'-VLM-raw ZAVRJEN!) — ne-Griblje; PEZDIREC-vez vendar izven Griblje-frama (P176-lead-'×3'-KOREKCIJA → ×2-v-Griblju!)"},
            {"id": "X2", "opis": "z30-marija-TAPRIČ = GRIŠIČE? h33 (KROP-vas — 'Griblje'-VLM-raw ZAVRJEN!; cf. P131-'Grišiče? 35'-X-open + z10-s131-'Gipšiče'-TAPRIČ-vez!) — ne-Griblje; ★ 35 LET (KROP — '95'-ZAVRJEN! roj. 4.8.1876-forenzika) + roj. PLAT [~ Plut]"},
            {"id": "X3", "opis": "z36-marija-TAPRIČ = GRIŠIČE? h33 (KROP-vas!) — ne-Griblje; TAPRIČ-×2-h33-v-4-mesecih (z30-avg-35-let + z36-sep-5-mes = babica+vnučka?-hipoteza [~])"},
        ],
        "anomalies": [
            {"id": "A1", "opis": "★★★ z31-'96 let' → 26 LET (KROP @×3.0 — '2-6'-jasno + roj. 19. 8. 1884-marginalija → 26-let-364-dni = 1-DAN-PRED-27.-ROJSTNIM-DNOM-SKLADNO!) — 3.-STAROST-KOREKCIJA-V-ZAPORU (cf. P173-'81'→51 + P174-'84'→64 + P176-z9-'86'→66!)"},
            {"id": "A2", "opis": "★★★ z30-'95 let' → 35 LET (KROP — '3-5' + roj. 4. 8. 1876 → 35-let-12-dni-skladno!) — ne-Griblje ampak št.-forenzika-linije"},
            {"id": "A3", "opis": "★★★ z47-'Nikolaj Nepomuk' → Nikolaj KUPANIČ (KROP @×3.0 — '[K]upanič'-jasno! NI sv.-Nepomuk!) — NOV-PRIIMEK? [~ X-open]"},
            {"id": "A4", "opis": "★★ z48-'Matija Birčec' → Matija BRINEC (KROP — 'Brinec'-jasno; K-D-panel-'Sofija'-ZAVRJENA — sin-stan!) — BRINEC-×2-h14-1911"},
            {"id": "A5", "opis": "★★ z54-'Janez Fošelj' → Janez POŽEK (KROP — 'Požek'-ž-caron!) — POŽEK-veriga (P85-h79/h77-bajtarji-vez!)"},
            {"id": "A6", "opis": "★★★ z51-'Peter Perdih' → Peter PEZDIREC (KROP — z-DESCENDER-leksikon!) → PEZDIREC-×4-1911 (z24+z26+z27+z51 = 1.-LETO-×4!) + z31-roj.-Pezdirec = 5.-kontakt!"},
            {"id": "A7", "opis": "★★ z42-h14 → h19 (KROP — '19'-jasno, 4/9-KURRENT!) — h14-×2 rešeno (z13+z48), h19 = 4. mrliški"},
            {"id": "A8", "opis": "★★★ VAS-KOREKCIJE-×3: z24-'Lodnemej'→PODZEMELJ + z30/z36-'Griblje'→GRIŠIČE? (KROP-×3!) → GRIBLJE-13 (ne-16!) — P176-lead-'5-GRIBLJE-ŽE-vidnih' = 2-realnih (z13+z14) + 3-zavrnjenih!"},
            {"id": "A9", "opis": "★★ z55-'Vlobučar' → HLOBUČAR (KROP — H-prečka @×3.0; P166-vez-×3!) — H/V-KURRENT-lekcija-2.-potrditev"},
            {"id": "A10", "opis": "★★ z46-'Hladno klatran' → HLADNI KAŠELJ (KROP) = 1.-TA-BOLEZEN-LINIJE + z48-OPEKLINA = 1.-TA-BOLEZEN = 3.-TRAUMA-SMRT (1908-vrca + 1910-mrtvo-najden!) — 2-NOVI-BOLEZNI-V-1-LETU!"},
            {"id": "A11", "opis": "★★ meja-1911/12 = s135-INSIDE ('1912'-VELIKA-v-bandu-k5 + restart + Bitnar-podpis!) = 2.-POTRDITEV-STILA-8 (s130-vzorec) — P176-lead-'[?]' REŠEN; z58-pokop-'2-jan-1912'-EKSPPLICITNO = 3.-MEJNI-DOKAZ!"},
            {"id": "A12", "opis": "★ DUHOVNIKI-1911: Bitnar-×12-GNOMINANTA (3.-leto! cf. 1910-×~26) + Pumf-×1 (z14!) — PODW-KROPI-×3 (z30-'Rauq'→Pumf + z31-'Pithar'→Bitnar + z42-'Pihnar'→Bitnar = VLM-varianta-ZMEDA-RAZREŠENA!)"},
        ],
        "crossChecks": [
            {"id": "C1", "opis": "zap-kontinuiteta: 58-oštevilčenih == 58-VPISOV — ČISTA-SEKVENCA-z1–58 (7.-ČISTO-LETO! 0-predorov/0-duplikatov/0-neštevilčenih! cf. 1910-54)"},
            {"id": "C2", "opis": "stran == sken − 1 (106.–111. potrditev!): s131→130 + s132→131 + s133→132 (VLM-glava!) + s134→133 (VLM-glava!) + s135→134 (K-E-'191'-misread-[~]) + s136→135 (VLM-glava!) — 6/6 novih + 3 re-use (s130–s132)"},
            {"id": "C3", "opis": "h14-×2-BRINEC-veriga: z13-Ana-8-let (april) + z48-Matija-4-let (november, OPEKLINA) = brat+sestra?-PAR-2-meseci-apart + BRINEC-patroN-P173 + babica-P84/P85 + PUA-'Brinc'-0.8333!"},
            {"id": "C4", "opis": "PEZDIREC-1911-×5-kontaktov: z24-ana-Podzemelj + z26-janez-h42 + z27-vida-h48 + z31-roj.-Pezdirec-h57 + z51-peter-h20 — vsi-4-VAŠE! (Podzemelj + Griblje-×3) — 8.-leto-PEZDIREC-dominante!"},
            {"id": "C5", "opis": "meje-duplikat-STIL-8: s130 (~1911~) + s135 (1912) = 2-ZAPOREDNA-mid-scan-band-restarta — vzorec-stabilen-3.-leto (s126 + s130 + s135!)"},
        ],
        "honesty": [
            "band-recept: 330+135×k-100%-VELJAVEN-za-s131–s136; s130-ODSTOPANJE-+1 (meja-band-porine-1911-vrstice: k7=z1…k11=z5!) — diag-rešeno; zato trak-z4-k9 = z3-napačna-vrstica (popravljeno-k10!)",
            "[~] konservativno: MAVREŠIČ-vs-'Mavrič' (n/š-KURRENT) + JURAJEVIČ-vs-'Juračevič' + Marjeta-vs-'Margareta' + 'samotni viškar' + HLOBUČAR-H-prečka + z14-ŠILAK-vrnitev-hipoteza + KUPANIČ-nov-priimek",
            "VLM-panel-limite: panel-branja-je-brala-STOLPCE-NAPAČNO (starost = hišna, bolezen = stan, ime = vas!) — kompenzirano z 16-lastnimi-vizijami-kropov (@×2.2/×3.0); paneli-VREDNI-samo-skupaj-z-diag!",
            "z31-rojena-'1884'-vs-VLM-'1894': KROP-pokazuje-'1884' + 26-let-skladnost → 1884 [~]; z30-'1876'-100%-jasna",
            "z57-h20-vs-'h29'-diag (Primostek, ne-Griblje — VLM-raw-'h20'-obdržano [~ 4/9]); ne-Griblje-vrstice-VLM-raw-brez-dodatne-forenzike (p176-vzorec!)",
            "Grišiče-h33-vs-P131-'Grišiče?35': hiša-RAZLIKA (33-vs-35) — X-open-OBOJE [~]; vas-NI-v-PT-naboru-dokazano",
            "s135-K-E-glava-'Stran 191' = '134'-VLM-misread [~] — stran==sken−1-obdržano (vzorec-51-skenov!)",
        ],
        "nextSteps": {
            "P178-lead": "mrliška 1912 (s135-dno-z1–6 ŽE-prebrani + s136-z7–18 ŽE-prebrani: 2-GRIBLJE-ŽE-vidnih — 1912-z1-jožef-PEČNIK?-h87 [K-C-'Pechnik'-vs-diag-'Pačdivec'-zmeda!] + 1912-z10-barbara-ŠTRAVS-h11! + 1912-z3-MRTVOROJENEC-×2-v-2-MESECIH (Dobravice-h7 — cf. 1911-z4!); meja-1912/13 [~ s140+?])",
            "fetch": "s137–s141 + VLM-branje (≤2-skena/serijo-foreground)",
            "forezika": "PEČNIK-vs-'Pačdivec' + ŠTRAVS-h11-vez (STRAUS-mreža-#5? cf. 1888-h72!) + Maroutič-h45-vs-h15 + Mlinar-h47-vs-h27",
            "kaskada": "vitals 1045 → +n · bloki 346 → +n · guardi-1912 · PT-29 (0-novih-1911!)",
        },
    }

    # validacija
    assert len(entries) == 58, len(entries)
    assert len(grib) == 13, len(grib)
    assert len(hise) == 12, hise
    assert all(e["page"] == e["scan"] - 1 for e in entries)
    json.dump(dokaz, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"dokaz: {OUT}")
    print(f"vpisov={len(entries)} griblje={len(grib)} hiš={len(hise)} ({','.join(hise)})")
    grb = [e for e in grib if e['houseNo'] == '14']
    print(f"h14-×2: {[e['zap'] for e in grb]}")


if __name__ == "__main__":
    main()
