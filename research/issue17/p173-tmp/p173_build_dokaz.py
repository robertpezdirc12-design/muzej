#!/usr/bin/env python3
"""P173 — build dokaz parish-death-1907.json iz VLM-base + forezika-korekcije."""
import json, os

VP = "/tmp/p173/vlm-page"
OUT = "/home/z/muzej/research/issue17/parish-death-1907.json"

# ——— korekcije (forezika ×3.0/×4.0 kompoziti + diag-vizualna) ———
# format: (scan, zap) -> dict polj za prepis
K = {
 (109, 1):  {"ime": "Anton BRODARIČ [★★★ P172-'BRINEC-PAR-vez'-KOREKCIJA — kompozit-×4-ista-glyph-forma-kot-z57-Nikolaj-Brodarič!]",
             "stan": "vdovec vrškar [~ 'vdovec-in-vrškar'; vrškarica-forma-potrjena-1906-z62!]",
             "bolezen": "Nadruka [~ VLM-'Naduha' — kompozit-K-jasno!]"},
 (109, 2):  {"ime": "Ana ŽELJKO [~ KURRENT-Ž/V-caron; P172-lead-'VELJKO'-alternativa]", "bolezen": "Kašel [~ VLM-'Kaicij']"},
 (109, 4):  {"ime": "Ana MUC [★★★ P172-lead-'MEC'-KOREKCIJA + VLM-'Hleu'-ZAVRJENA — kompozit-'Muc' + h91 = MUC-×-KURE-genetska (krstna-1895/1902/1904/1908)!]",
             "stan": "hovarčeva hiča [~ diag-'hovacova'; VLM-'hlapčeva-žena'-zmeda]"},
 (109, 5):  {"starost": "3 tednov [~ diag-'5'?]"},
 (109, 9):  {"ime": "Marija NOVAK [★★ VLM-'pri-Jovanek'-ZAVRJENA + P172-lead-'POVH'-ZAVRJENA — kompozit-'Marija, ry: Novak odova / po + Janezu Pezdircu'-jasno!]",
             "stan": "roj. Novak, vdova po Janezu PEZDIREC, ¼ zemljakinja"},
 (109, 11): {"ime": "Alojzij POČEK [~ KURRENT-P-bowl; VLM-'Pošek'; P172-lead-'DRIŠEK'-ZAVRJENA]", "bolezen": "Kašel [~ VLM-'Kaicij']"},
 (110, 13): {"ime": "Anton ŽELJKO [★★ VLM-'Veliko'-ZAVRJENA — kompozit-caron-Ž!]", "bolezen": "Kašel [~ VLM-'Maščef'-ZAVRJENA]"},
 (110, 18): {"ime": "Matija URH [★★★ VLM-'Udoh'-ZAVRJENA — kompozit-jasno!]",
             "opomba": "★★★ PISAR-DATUM-NAPAKA (smrt-'29.'-Februar-1907 = NE-PRESTOPNO-leto — 1.-v-liniji!; [~ rešitev-28.2])"},
 (111, 27): {"ime": "Marija ŠTRMEC [~ kompozit-'Štimec/Štrmec'-tr-zmeda]", "stan": "omožena ¼ zemljakinja [~ diag-'ovrozena']", "bolezen": "Pljučnica"},
 (111, 32): {"ime": "Marija ŽUNIČ [~ kompozit-Ž-caron; VLM-'Kumič'-ZAVRJENA]", "bolezen": "Kašel [~ diag-'Kasel'-jasno]"},
 (112, 36): {"ime": "Marija DRAGOŠ [~ kompozit-'Dragos'; cf.-Dragar?], omožena KAMBIČ [~ 'Škambič/Hambič']"},
 (112, 37): {"ime": "Matija ŠIMEC [~ VLM-'Simic']", "stan": "kmetijski hlapec",
             "bolezen": "od opeklin [★★ diag-'?led opeklin' — OPEKLINE — 3.-nesreča-v-liniji!]"},
 (112, 39): {"ime": "Matija MILEK [★★ VLM-'Mlek'-zmeda — kompozit-i + h65 = MILEK-hiša-1886-poročna!]", "stan": "oženjen ¼ zemljak [~ ½]", "bolezen": "Kašel"},
 (113, 53): {"ime": "Jurij TOŽEK [★★ diag-'Toček/Soček' — kompozit-ž-hook + P172-h58-TOŽEK!]", "stan": "oženjen ¼ zemljak"},
 (113, 55): {"ime": "Ana KRIŽE [★★ VLM-'Kroše'-ZAVRJENA — kompozit + P172-h19-Janez-KRIŽE!]", "stan": "samotka ¼ zemljaška hiča",
             "opomba": "★★ PISAR-DATUM-NAPAKA (pokop-'31.'-September = NE-OBSTOJA — 30-dni!; ×2-z-z56)"},
 (113, 56): {"ime": "Ana ŠIMEC, omožena TOŽEK [~ 'Toček/Poček']", "stan": "roj. Šimec, ¼ zemljakinja",
             "opomba": "★★ PISAR-DATUM-NAPAKA (pokop-'31.'-September-×2!)"},
 (113, 57): {"houseNo": "49 [★★ VLM-'40'-ZAVRJENA — kompozit-q-9-loop!]",
             "ime": "Nikolaj BRODARIČ [★★ kompozit-jasno — ISTA-forma-kot-z1!], ¼ zemljakov sin [~ ½]"},
 (113, 58): {"ime": "Matija BRINEC [★★★ VLM-'Ogrince'-ZAVRJENA — kompozit-jasno!]"},
 (113, 59): {"ime": "Katarina PEZDIREC [~], omožena KAMBIČ [~]", "smrt": "2.", "pokop": "4. [★★ VLM-'14.'-ZAVRJENA — kompozit-jasno!]",
             "stan": "roj. Pezdirec?, ¼ zemljakova žena"},
 (114, 63): {"ime": "Anton BRINEC [★★★ VLM-'Vrhnar'-ZAVRJENA — kompozit-jasno!]",
             "duhovnik": "Jos. LILEK župnik v. p. [~ — NOVI-DUHOVNIK!]"},
 (114, 65): {"duhovnik": "Greg. Cerar kap."},
}

scan_map = {"s109": 109, "s110": 110, "s111": 111, "s112": 112, "s113": 113, "s114": 114}
page_map = {109: 108, 110: 109, 111: 110, 112: 111, 113: 112, 114: 113}
griblje = {"Griblje", "Griblje [~]", "griblje"}

entries, g_count = [], 0
for s in ["s109", "s110", "s111", "s112", "s113", "s114"]:
    d = json.load(open(f"{VP}/{s}.json"))
    scan = scan_map[s]
    for v in d.get("vrstice", []):
        zap_raw = str(v.get("zaporedna", "")).strip()
        if not zap_raw.isdigit():
            continue  # prazna vrstica / 1908-vrstice-brez-zap
        zap = int(zap_raw)
        if scan == 114 and zap <= 3:
            continue  # 1908-restart-vrstice = P174-lead (excluded)
        row = {
            "row": len(entries) + 1, "zap": zap, "scan": scan, "page": page_map[scan],
            "bookSignature": "04894", "year": 1907,
            "mesec": v.get("mesec"), "smrt": v.get("smrt"), "pokop": v.get("pokop"),
            "vas": v.get("vas"), "houseNo": str(v.get("hisna") or "").rstrip('.') or "?",
            "ime": v.get("ime"), "stan": v.get("stan"), "starost": v.get("starost"),
            "bolezen": v.get("bolezen"), "previden": v.get("previden"),
            "duhovnik": v.get("duhovnik"), "opomba": v.get("opomba"),
        }
        if (scan, zap) in K:
            row.update(K[(scan, zap)])
        if row["vas"] and "griblje" in str(row["vas"]).lower():
            g_count += 1
            row["griblje"] = True
        entries.append(row)

# ——— meja 1908-vrstice (s114 z1–3) = EXCLUDED (P174-lead) ———
d114 = json.load(open(f"{VP}/s114.json"))
p174_lead = []
for v in d114.get("vrstice", []):
    z = str(v.get("zaporedna", "")).strip()
    if z in ("1", "2", "3"):
        p174_lead.append(v)

dokaz = {
 "status": "SAMPLE-TRANSCRIPTION-D1907",
 "generated": "P173",
 "phase": "P173 — mrliška 1907 (22. polno leto mrliške linije)",
 "source": "matricula-online.eu 04894, skeni 109–114 (s109-reuse-P172-meja + s110–s114)",
 "frame": "s109 (zap1–11; P172-meja-lead) + s110 (12–23) + s111 (24–35) + s112 (36–47) + s113 (48–59) + s114 (60–67; meja-1908 = velika-'1908'-podčrtana + Januarij + restart 67→1 = 6. STIL 15. POTRDITEV — P172-lead-'[~ s113+?]'-KOREKCIJA-→-s114!)",
 "entries": entries,
 "excluded": [{"reason": "s114-zap1–3 = leto-1908 (velika-'1908' + restart) = P174-LEAD", "rows": p174_lead}],
 "anomalies": [
  "★★★ PISAR-DATUM-NAPAKE-×3 = 1.-TIPO-v-liniji (NE-MOŽNI-datumi!): z18-'29.-Februar-1907' (NE-PRESTOPNO-leto!) + z55-'31.-September' + z56-'31.-September' (September-ima-30-dni-×2!)",
  "★★★ 5-GLAVE-NAPAKE = REKORD-IZENAČEN-3.× (P170-5 + P172-5 + P173-5!): s109-'181907' + s111-'181904'-NAPAČNO-LETO-NOV-VZOREC! + s112-'18'-NEKOMPLETNA-2.-v-liniji + s113-'181907.' + s114-'181907'",
  "★★★ 20-GRIBLJE = NOV-REKORD-LINIJE (rast 17→16→16→10→20!)",
  "★★★ P172-'BRINEC-PAR-vez'-KOREKCIJA: 1907-z1 = Anton-BRODARIČ (NE-BRINEC!) — h49-vez-ostaja (2-zaporedna-Januarja-66-let-vdova/vdovec — priimka-RAZLIČNA!)",
  "★★ h75 + h10 = 2-NOVI-MRLIŠKI-HIŠI (1.-MRLIŠKI-VPIS-KADARKOLI-×2 = 30./31.-PT-vezni-kandidat!)",
  "★★ h49-×2 + h10-×2-v-1-letu (PADEC-vzorec-4.-leto: 1904-h18 + 1905-h18/h27 + 1906-h58 + 1907-h49/h10!)",
  "★★ h65 = 8.-vpis = IZENAČUJE-REKORDISTKO-h58 (8×-1906!)",
  "★★ VLM-korekcije-imen-×13: 'Hleu'→MUC + 'pri-Jovanek/POVH'→roj.-NOVAK + 'Veliko'→ŽELJKO + 'h40'→h49 + 'Ogrince'→BRINEC + 'Vrhnar'→BRINEC + 'Udoh'→URH + 'Kroše'→KRIŽE + 'Mlek'→MILEK + 'Šimec'→ŠTRMEC[~] + 'Kumič'→ŽUNIČ[~] + 'Pošek'→POČEK[~] + 'Drišek'→POČEK[~]",
  "★★ VLM-bolezen-korekcije-×4: 'Maščef'/'Kaicij'/'Kasek'/'Kaikel'→KAŠEL (z2/z11/z13/z32/z39!)",
  "★★ NOVI-DUHOVNIK-Jos.-LILEK-'župnik-v.p.' (×4-5-podpisov — 0-pred-1907-v-parish.ts!) + Martin-Nemaniš-×1 + Guido-KRUSCH-layman-signature-×1 (z42-'za-župnika'+Krusch+rola[?]-anomalija!) + Gregor-CERAR-kaplan-DOMINANTA-×~14 (znan-iz-krstne-1908+ — 1.-mrliški-podpisi!)",
  "★ Mrtvorojenec-×1 (s111-z35-Otok-h10 — BREZ-podpisa!) + DVOJČKI-Krasinec-h18-×2-1-dan (z44-Martin + z45-Majeta-Čupanič[~VLM-'Češarič']!)",
  "★ ŠIMEC-×2-v-1-letu-Griblje (z37-h75-Matija-roj. + z56-h21-roj.Šimec!) + ŽELJKO-vez-h1+h60 + BRINEC-×3-v-1907 (z58/z63/z65!)",
 ],
 "crossChecks": [
  "stran == sken − 1 (s109–s114 == str. 108–113 — 82.–87. potrditev!)",
  "zap-sekvenca-1–67-BREZ-predorov (s109:1–11 → s110:12–23 → s111:24–35 → s112:36–47 → s113:48–59 → s114:60–67)",
  "meja-1907/08 = s114 (restart 67→1 — VIZUALNO-diag + velika-'1908'-podčrtana!)",
  "duhovniki-1907: Florjančič-cap-Jan + Stan.-Dostál-×1 + Jos.-Rauq-×~30 + Nemaniš-×1 + Krusch-×1 + Gregor-CERAR-kap-DOMINANTA + Jos.-LILEK-župnik-v.p.-×4-5",
  "hiše-1907-Griblje: 49-×2 + 1 + 91 + 87 + 52 + 31 + 60 + 32 + 14 + 11 + 74 + 75 + 65 + 28 + 19 + 21 + 25 + 10-×2 = 18-hiš",
 ],
 "honesty": [
  "s109/s110 = P172-ženda-skeni (diag-iz-/tmp/p172) — VLM-page-branja-iz-P172-seje",
  "rows-v3-detekcija-FAIL-na-vseh-skenih (P172-vzorec) → fiksni-diag-grid-330–1950/135px + Read-oči",
  "s109-pasovi-drift (start-420/step-150-meritve-po-MERITEV-ime-traku!)",
  "z5-starost-'3-tednov'-[~5?]-ne-rešena-do-konca (digit-odrezan)",
  "z57-frakcija-¼/½-[~] + z39/z53-frakcija-¼/½-[~]",
 ],
 "nextSteps": "P174-LEAD: 1908 (s114-zap1–3 ŽE-prebrani: z1-Dobravice-h25-Martin-Plut-vrškar-in-vdovec + z2-Gradac-h47-Frano-Schweiger + z3-Krivoglavce-h29-Janez-Muc = 0-GRIBLJE-v-zap1–3! + s115-zap4–15: z10-GRIBLJE-h42-Doroteja-PEZDIREC-81-let-Jan! + s116-zap16–27: z16-GRIBLJE-h24-Majeta-Binec-11-let + z20-GRIBLJE-h3-Ana-Papič-85 + z25-GRIBLJE-h85-Jožef-Perdinec = 4-GRIBLJE-ŽE-vidnih!; meja 1908/09 [~ s119+?])",
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(dokaz, open(OUT, "w"), ensure_ascii=False, indent=1)
g = [e for e in entries if e.get("griblje")]
print(f"dokaz: {len(entries)} entries, {len(g)} GRIBLJE")
print("GRIBLJE-hip:", [(e['zap'], e['houseNo'], e['ime'][:24]) for e in g])
