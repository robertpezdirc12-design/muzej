#!/usr/bin/env python3
"""P173 — build dokaz parish-death-1907.json v P172-shape (frame-dict + anomalies-{id,opis})."""
import json

VP = "/tmp/p173/vlm-page"
OUT = "/home/z/muzej/research/issue17/parish-death-1907.json"

K = {
 (109, 1):  {"ime": "Anton BRODARIČ [★★★ P172-'BRINEC-PAR-vez'-KOREKCIJA — kompozit-×4-ista-glyph-forma-kot-z57-Nikolaj-Brodarič!]",
             "stan": "vdovec vrškar [~ 'vdovec-in-vrškar'; vrškarica-forma-potrjena-1906-z62!]",
             "bolezen": "Nadruka [~ VLM-'Naduha' — kompozit-K-jasno!]",
             "starost": "66 LET", "duhovnik": "St. Florijana FLORJANČIČ cap. [#14?]"},
 (109, 2):  {"ime": "Ana ŽELJKO [~ KURRENT-Ž/V-caron; P172-lead-'VELJKO'-alternativa]", "bolezen": "Kašel [~ VLM-'Kaicij']",
             "starost": "6 LET", "duhovnik": "St. Florijana FLORJANČIČ cap. [#14?]"},
 (109, 4):  {"ime": "Ana MUC [★★★ P172-lead-'MEC'-KOREKCIJA + VLM-'Hleu'-ZAVRJENA — kompozit-'Muc' + h91 = MUC-×-KURE-genetska!]",
             "stan": "hovarčeva hiča [~ diag-'hovacova'; VLM-'hlapčeva-žena'-zmeda]",
             "starost": "16 LET", "duhovnik": "St. Florijana FLORJANČIČ cap. [#14?]"},
 (109, 5):  {"starost": "3 TEDNOV [~ diag-'5'?]", "duhovnik": "St. Florijana FLORJANČIČ cap. [#14?]"},
 (109, 9):  {"ime": "Marija NOVAK [★★ VLM-'pri-Jovanek'-ZAVRJENA + P172-lead-'POVH'-ZAVRJENA — kompozit-jasno!]",
             "stan": "roj. Novak, vdova po Janezu PEZDIREC, ¼ zemljakinja", "starost": "69 LET"},
 (109, 11): {"ime": "Alojzij POČEK [~ KURRENT-P-bowl; VLM-'Pošek'; P172-lead-'DRIŠEK'-ZAVRJENA]", "bolezen": "Kašel [~ VLM-'Kaicij']", "starost": "6 MESECEV"},
 (110, 13): {"ime": "Anton ŽELJKO [★★ VLM-'Veliko'-ZAVRJENA — kompozit-caron-Ž!]", "bolezen": "Kašel [~ VLM-'Maščef'-ZAVRJENA]", "starost": "4 MESECE"},
 (110, 18): {"ime": "Matija URH [★★★ VLM-'Udoh'-ZAVRJENA — kompozit-jasno!]", "starost": "16 LET",
             "opomba": "★★★ PISAR-DATUM-NAPAKA-1/3 (smrt-'29.'-Februar-1907 = NE-PRESTOPNO-leto — 1.-v-liniji!; [~ rešitev-28.2])"},
 (111, 27): {"ime": "Marija ŠTRMEC [~ kompozit-'Štimec/Štrmec'-tr-zmeda]", "stan": "omožena ¼ zemljakinja [~ diag-'ovrozena']", "bolezen": "Pljučnica", "starost": "39 LET"},
 (111, 32): {"ime": "Marija ŽUNIČ [~ kompozit-Ž-caron; VLM-'Kumič'-ZAVRJENA]", "bolezen": "Kašel [~ diag-'Kasel'-jasno]", "starost": "2 LETI"},
 (112, 36): {"ime": "Marija DRAGOŠ [~ kompozit-'Dragos'; cf.-Dragar?], omožena KAMBIČ [~ 'Škambič/Hambič']", "starost": "22 LET"},
 (112, 37): {"ime": "Matija ŠIMEC [~ VLM-'Simic']", "stan": "kmetijski hlapec", "starost": "24 LET",
             "bolezen": "od opeklin [★★ diag-'?led opeklin' — OPEKLINE — 3.-nesreča-v-liniji!]"},
 (112, 39): {"ime": "Matija MILEK [★★ VLM-'Mlek'-zmeda — kompozit-i + h65 = MILEK-hiša-1886!]", "stan": "oženjen ¼ zemljak [~ ½]", "bolezen": "Kašel", "starost": "65 LET"},
 (113, 53): {"ime": "Jurij TOŽEK [★★ diag-'Toček/Soček' — kompozit-ž-hook + P172-h58-TOŽEK!]", "stan": "oženjen ¼ zemljak", "starost": "62 LET", "duhovnik": "Gregor CERAR kaplan [1.-mrliški-podpis-CERAR!]"},
 (113, 55): {"ime": "Ana KRIŽE [★★ VLM-'Kroše'-ZAVRJENA — kompozit + P172-h19-Janez-KRIŽE!]", "stan": "samotka ¼ zemljaška hiča", "starost": "24 LET", "duhovnik": "Gregor CERAR kapl.",
             "opomba": "★★ PISAR-DATUM-NAPAKA-2/3 (pokop-'31.'-September = NE-OBSTOJA — 30-dni!; ×2-z-z56)"},
 (113, 56): {"ime": "Ana ŠIMEC, omožena TOŽEK [~ 'Toček/Poček']", "stan": "roj. Šimec, ¼ zemljakinja", "starost": "42 LET", "duhovnik": "Gregor CERAR kap.",
             "opomba": "★★ PISAR-DATUM-NAPAKA-3/3 (pokop-'31.'-September-×2-BATCH!)"},
 (113, 57): {"houseNo": "49", "ime": "Nikolaj BRODARIČ [★★ kompozit-jasno — ISTA-forma-kot-z1!; VLM-'Brodarvič']", "starost": "18 DNI", "duhovnik": "Gregor CERAR kap.",
             "opomba": "★★ VLM-'h40'-ZAVRJENA — kompozit-q-9-loop-'49'!; ★★★ NIKOLAJ-BRODARIČ-ime-vez (1899-krstna-h49-starši-Nikolaj-×-Marjeta-Milek!)"},
 (113, 58): {"ime": "Matija BRINEC [★★★ VLM-'Ogrince'-ZAVRJENA — kompozit-jasno!]", "starost": "2 LETI", "duhovnik": "Gregor CERAR kap."},
 (113, 59): {"ime": "Katarina PEZDIREC [~], omožena KAMBIČ [~]", "smrt": "2.", "pokop": "4. [★★ VLM-'14.'-ZAVRJENA!]",
             "stan": "roj. Pezdirec?, ¼ zemljakova žena"},
 (114, 63): {"ime": "Anton BRINEC [★★★ VLM-'Vrhnar'-ZAVRJENA — kompozit-jasno!]", "starost": "4 DNI",
             "duhovnik": "Jos. LILEK župnik v. p. [~ — NOVI-DUHOVNIK!]",
             "opomba": "★★★ h10 = 1. MRLIŠKI VPIS KADARKOLI = 31.-PT-vez-kandidat (04894-h10-pred-1907-pRAZNO!)"},
 (114, 65): {"duhovnik": "Greg. Cerar kap.", "starost": "11 DNI",
             "opomba": "★★★ h10-×2-v-1-letu-2.-del (6-DNI-APART-po-z63!) + BRINEC-×3-v-1907!"},
}
# dodaj h75 (1.-vpis!) opombo
K[(112, 37)]["opomba"] = "★★★ h75 = 1. MRLIŠKI VPIS KADARKOLI = 30.-PT-vez-kandidat (04894-h75-pred-1907-pRAZNO!)"

scan_map = {"s109": 109, "s110": 110, "s111": 111, "s112": 112, "s113": 113, "s114": 114}
page_map = {109: 108, 110: 109, 111: 110, 112: 111, 113: 112, 114: 113}

MESEC_CANON = {"Januar": "Januar", "Februar": "Februar", "Marec": "Marec", "März": "Marec",
               "April": "April", "Mai": "Maj", "Maj": "Maj", "Juni": "Juni", "Juni.": "Juni",
               "Juli": "Juli", "July": "Juli", "August": "Avgust", "Avgust": "Avgust",
               "September": "September", "Sept": "September", "October": "Oktober",
               "November": "November", "December": "December"}

entries, p174_lead = [], []
last_mesec = None
for s in ["s109", "s110", "s111", "s112", "s113", "s114"]:
    d = json.load(open(f"{VP}/{s}.json"))
    scan = scan_map[s]
    for v in d.get("vrstice", []):
        z = str(v.get("zaporedna", "")).strip()
        if not z.isdigit():
            continue
        zap = int(z)
        if scan == 114 and zap <= 3:
            p174_lead.append({"zap": zap, "vas": v.get("vas"), "houseNo": str(v.get("hisna") or ""),
                              "ime": v.get("ime"), "starost": v.get("starost")})
            continue
        row = {"row": len(entries) + 1, "zap": zap, "houseNo": str(v.get("hisna") or "").rstrip('.') or "?",
               "bookSignature": "04894", "year": 1907, "scan": scan, "page": page_map[scan],
               "mesec": None, "smrt": v.get("smrt"), "pokop": v.get("pokop"),
               "vas": v.get("vas"), "ime": v.get("ime"), "stan": v.get("stan"),
               "starost": v.get("starost"), "bolezen": v.get("bolezen"),
               "previden": v.get("previden"), "duhovnik": v.get("duhovnik"), "opomba": v.get("opomba")}
        m_raw = v.get("mesec")
        if m_raw:
            m_key = str(m_raw).strip().rstrip('.')
            for k, canon in MESEC_CANON.items():
                if m_key.lower().startswith(k.lower()):
                    last_mesec = canon
                    break
        row["mesec"] = last_mesec
        if (scan, zap) in K:
            row.update(K[(scan, zap)])
        entries.append(row)

grb = [e for e in entries if str(e["vas"]).lower().startswith("griblje")]
hise = sorted({e["houseNo"] for e in grb}, key=int)
ponovitve = [h for h in hise if sum(1 for e in grb if e["houseNo"] == h) > 1]

dokaz = {
 "status": "SAMPLE-TRANSCRIPTION-D1907",
 "generated": "P173",
 "phase": "P173 — mrliška 1907 (21. → 22. polno leto mrliške linije)",
 "source": "matricula-online.eu 04894, skeni 109–114 (s109-reuse-P172-meja-lead + s110–s114)",
 "frame": {
  "leto": 1907, "vrstic": 67, "zap_oštevilčenih": 67, "neštevilčenih": 0, "vpisi": 67,
  "dup_zaporedna": None, "griblje_vpisi": len(grb), "hise": len(hise),
  "hise_seznam": ",".join(hise), "ponovitve": ",".join(ponovitve),
  "meja_1906_07": "s109 (P172-potrjena — velika-'1907.' + restart 55→1 + glava-'181907' — 14. POTRDITEV!)",
  "meja_1907_08": "s114 (velika-'1908'-PODČRTANA + Januarij + restart 67→1 = 6. STIL 15. POTRDITEV — VIZUALNO-diag! P172-lead-'[~ s113+?]'-KOREKCIJA-→-s114!)",
  "glave_napake": ["s109-'181907'", "s111-'181904'-NAPAČNO-LETO-NOV-VZOREC-(4-za-7!)",
                   "s112-'18'-NEKOMPLETNA-2.-v-liniji", "s113-'181907.'", "s114-'181907'"],
  "stran_invarianta": "stran == sken − 1 (s109–s114 == str. 108–113 — 82.–87. potrditev VIZUALNO!)",
 },
 "entries": entries,
 "excluded": [
  {"id": "X1", "opis": "s114-zap1–3 = 1908-vrstice (restart-pod-velika-'1908'!): z1-Dobravice-h25-Martin-Plut-vrškar-in-vdovec + z2-Gradac-h47-Frano-Schweiger + z3-Krivoglavce-h29-Janez-Muc = 0-GRIBLJE-v-zap1–3!"},
  {"id": "X2", "opis": "s115 (zap4–15) + s116 (zap16–27) = 1908-nadaljevanje (P174-lead!): z10-GRIBLJE-h42-Doroteja-PEZDIREC-81 + z16-GRIBLJE-h24-Majeta-Binec-11 + z20-GRIBLJE-h3-Ana-Papič-85 + z25-GRIBLJE-h85-Jožef-Perdinec = 4-GRIBLJE-ŽE-vidnih!"},
 ],
 "anomalies": [
  {"id": "A1", "opis": "★★★ 3 PISAR-DATUM-NAPAKE = 1.-TIPO-V-LINIJI (NE-MOŽNI-datumi!): z18-'29.-Februar-1907' (NE-PRESTOPNO-leto — 29.2.1907-NE-OBSTOJA!) + z55-'31.-September' + z56-'31.-September' (September-ima-30-dni-×2 = pisar-BATCH-koledar-napake!)"},
  {"id": "A2", "opis": "★★★ 5 GLAVE-NAPAKE = REKORD-IZENAČEN-3.× (P170-5 + P172-5 + P173-5!): s109-'181907' + s111-'181904'-NAPAČNO-LETO-NOV-VZOREC-(4-za-7!) + s112-'18'-NEKOMPLETNA-2.-v-liniji + s113-'181907.' + s114-'181907'"},
  {"id": "A3", "opis": "★★★ 20-GRIBLJE = NOV-REKORD-LINIJE (rast 17→16→16→10→20!) / 18-hiš (h49-×2 + h10-×2-v-1-letu = PADEC-vzorec-4.-leto!)"},
  {"id": "A4", "opis": "★★★ P172-'BRINEC-PAR-vez'-KOREKCIJA: 1907-z1 = Anton-BRODARIČ (NE-BRINEC! kompozit-×4-ista-glyph-forma-kot-z57!) — h49-vez-ostaja (2-zaporedna-Januarja-66-let-vdova/vdovec — priimka-RAZLIČNA!)"},
  {"id": "A5", "opis": "★★ h75 + h10 = 2-NOVI-MRLIŠKI-HIŠI (1.-MRLIŠKI-VPIS-KADARKOLI-×2 = 30./31.-PT-vez-kandidata!) + h65 = 8.-vpis-IZENAČUJE-REKORDISTKO-h58 (8×-1906!)"},
  {"id": "A6", "opis": "★★ NOVI-DUHOVNIK-Jos.-LILEK-'župnik-v.p.' (×4-5-podpisov — 0-pred-1907-v-parish.ts!) + Martin-NEMANIŠ-×1 + Guido-KRUSCH-layman-signature-×1 (z42-'za-župnika'+Krusch+rola[?]-ANOMALIJA!) + Gregor-CERAR-kaplan-DOMINANTA-×~14 (znan-iz-krstne-1908+ — 1.-mrliški-podpisi!)"},
  {"id": "A7", "opis": "★★ VLM-HALUCINACIJE-imen-×13: 'Hleu'→MUC! + 'pri-Jovanek'/'POVH'→roj.-NOVAK! + 'Veliko'→ŽELJKO! + 'h40'→h49! + 'Ogrince'→BRINEC! + 'Vrhnar'→BRINEC! + 'Udoh'→URH! + 'Kroše'→KRIŽE! + 'Mlek'→MILEK! + 'Šimec'→ŠTRMEC[~] + 'Kumič'→ŽUNIČ[~] + 'Pošek/Drišek'→POČEK[~] + 'Veljko'→ŽELJKO[~]"},
  {"id": "A8", "opis": "★★ VLM-korekcije-boleznih-×4: 'Maščef'→KAŠEL (z13!) + 'Kaicij'→KAŠEL (z2/z11!) + 'Kasek'→KAŠEL (z39!) + 'Kaikel'→KAŠEL (z32-diag-jasno!)"},
  {"id": "A9", "opis": "★ Mrtvorojenec-×1 (s111-z35-Otok-h10 — BREZ-podpisa!) + DVOJČKI-Krasinec-h18-×2-1-dan (z44-Martin + z45-Majeta-Čupanič[~VLM-'Češarič']!) + z42-podpis-'za-župnika'+Guido-Krusch+rola[?]"},
  {"id": "A10", "opis": "★ GENETSKE-VEZE: h91 = MUC-×-KURE (krstna-1895/1902/1904/1908 — z4-MUC!) + h60 = ŽELJKO-×-Brodarič (krstna-1888–1906!) + h52 = PEZDIREC (krstna-1898/1908 — vdova-po-Janezu-Pezdircu!) + h65 = MILEK-1886-poročna! + h14 = BRINEC-krstna-1908! + h49-BRODARIČ-mreža (1899-Nikolaj-×-Marjeta-Milek + 1900-Marija!)"},
  {"id": "A11", "opis": "★ ŠIMEC-roj.-×2-v-1-letu (z37-h75-Matija + z56-h21-roj.-Šimec!) + ŽELJKO-vez-h1+h60 (z2-Ana + z13-Anton!) + BRINEC-×3-v-1907 (z58-h25 + z63/z65-h10!)"},
  {"id": "A12", "opis": "★ URH-vez-×4-v-2-letih (1905-h32-Marija-83 + 1906-h57-Matija-78 + 1907-z18-h32-Matija-16 + 1907-z20-Otok-h8-Barbara-66!)"},
 ],
 "crossChecks": [
  {"id": "C1", "opis": "ZAP-KONTINUITETA: zap1–11 (s109) + 12–23 (s110) + 24–35 (s111) + 36–47 (s112) + 48–59 (s113) + 60–67 (s114) = 67-oštevilčenih = 67-VPISOV (ČISTA-SEKVENCA-BREZ-predorov — nasprotje-1906-DUP-21!)"},
  {"id": "C2", "opis": "STRAN == SKEN − 1: s109–s114 == str. 108–113 (82.–87. potrditev — VIZUALNO-diag!)"},
  {"id": "C3", "opis": "MEJA-1907/08 = s114: velika-'1908'-PODČRTANA + Januarij + restart 67→1 (6. STIL 15. POTRDITEV — P172-lead-'[~ s113+?]'-KOREKCIJA!)"},
  {"id": "C4", "opis": "DUHOVNIKI-1907: Florjančič-cap-Jan + Stan.-Dostál-×1 + Jos.-Rauq-×~30 + Nemaniš-×1 + Krusch-×1 + Gregor-CERAR-kap-DOMINANTA-×~14 + Jos.-LILEK-župnik-v.p.-×4-5 = 7-podpisovcev!"},
  {"id": "C5", "opis": "HIŠE-1907-GRIBLJE: 49-×2 + 1 + 91 + 87 + 52 + 31 + 60 + 32 + 14 + 11 + 74 + 75 + 65 + 28 + 19 + 21 + 25 + 10-×2 = 18-različnih (h75/h10 = 1.-vpis-kadarkoli!)"},
 ],
 "honesty": [
  "honesty-1: s109/s110 = P172-že-skeni (diag-iz-/tmp/p172-reuse) — VLM-page-branja-iz-P172-seje",
  "honesty-2: rows-v3-detekcija-FAIL-na-vseh-8-skenih (P172-vzorec) → fiksni-diag-grid-330–1950/135px + Read-oči",
  "honesty-3: s109-pasovi-drift (start-420/step-150-meritve-po-MERITEV-ime-traku; +1-pas-zmeda-rešena!)",
  "honesty-4: z5-starost-'3-tednov'-[~5?]-ne-rešena-do-konca (digit-odrezan-v-cropu)",
  "honesty-5: frakcije-¼/½-[~]-nezanesljive (z39/z53/z57 — KURRENT-frakcija-glyph)",
  "honesty-6: VLM-s110-'meja'-opomba-zmedena ('vnosi-12–14-še-1906'-NAPAKA — zap-sekvenca-dokazuje-1907!)",
 ],
 "nextSteps": {
  "P174-lead": "mrliška 1908: s114-zap1–3 ŽE-prebrani (0-GRIBLJE!) + s115-zap4–15 (z10-GRIBLJE-h42-Doroteja-PEZDIREC-81-let-Jan = h42-PEZDIREC-nadaljevanje!) + s116-zap16–27 (z16-GRIBLJE-h24-Majeta-Binec-11-let + z20-GRIBLJE-h3-Ana-Papič-85 + z25-GRIBLJE-h85-Jožef-Perdinec = 4-GRIBLJE-ŽE-vidnih!); meja 1908/09 [~ s119+?]",
  "p174_lead_rows": p174_lead,
 },
}

json.dump(dokaz, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"dokaz: {len(entries)} entries, {len(grb)} GRIBLJE, {len(hise)} hiš, ponovitve={ponovitve}")
