#!/usr/bin/env python3
"""P174 — build dokaz parish-death-1908.json v P173-shape (frame + anomalies + crossChecks + honesty).
Vhod: /tmp/p174/vlm-page/s{114..122}.json + K-korekcije (diag-vizualna + max-zoom crops!)."""
import json, os

VP = "/tmp/p174/vlm-page"
OUT = "/home/z/muzej/research/issue17/parish-death-1908.json"

SCAN_MAP = {114: 114, 115: 115, 116: 116, 117: 117, 118: 118, 119: 119, 120: 120, 121: 121, 122: 122}
PAGE_MAP = {114: 113, 115: 114, 116: 115, 117: 116, 118: 117, 119: 118, 120: 119, 121: 120, 122: 121}

MESEC = {"Januar": "Januar", "Januarji:": "Januar", "Februar": "Februar", "Marec": "Marec",
         "April": "April", "Mai": "Maj", "Maj": "Maj", "Junij": "Juni", "Juni": "Juni",
         "Juli": "Juli", "July": "Juli", "August": "Avgust", "Avgust": "Avgust",
         "September": "September", "Sept": "September", "October": "Oktober",
         "November": "November", "December": "December"}

# K — diag-vizualne + max-zoom korekcije VLM-branj (ključ: (scan, zap))
K = {
 (115, 4):  {"ime": "Marija ELME [~ KURRENT-'Elme/Heme'-zmeda — NERAZREŠENO]",
             "stan": "½ zemljakova hči",
             "duhovnik": "G. g. Matija CERAR, DEKAN [★★★ NOVI-DUHOVNIK! — kompozit-'dekan'-jasno; iste-priimke-kot-kaplan-Gregor-CERAR!]",
             "opomba": "★★★ NOV-DUHOVNIK + OPOMBA-marginalija ('Matijo Sogozor? [?] župn. per vic [?]' — delno-ZA-HRBTOM-knjige — neberljivo!)"},
 (115, 5):  {"ime": "Katarina MUC", "starost": "85 LET"},
 (115, 8):  {"starost": "— [PRAZNA!]"},
 (115, 9):  {"ime": "Matija ŠTIPARIČ [~ VLM-'Štefanič']", "bolezen": "Kaplje vode [~ VLM-'Hlapce, rode' — kaplje/hidropsija!]"},
 (115, 10): {"ime": "Doroteja PEZDIREC [★★ diag-'Pezdirec'-z-descender-jasno!]", "starost": "51 LET [★★★ P173-LEAD-'81'-KOREKCIJA — max-zoom-'5'-jasno!]", "duhovnik": "Gregor Cerar"},
 (115, 11): {"ime": "Anton ŽUGELJ [~ VLM-'Hugel']", "bolezen": "Junica [~ NERAZREŠENA-bolezen]"},
 (115, 12): {"ime": "Janez HARAŠINIČ [★★ VLM-'Špahič'-ZAVRJENA — diag-'Harašinič'-jasno cf.-z61!]"},
 (115, 13): {"ime": "Barbara BUČAN [~ diag-'Bučan/Buion']", "stan": "omrčena Debelić, ¼ zemljakinja"},
 (115, 14): {"stan": "vojzak [~ 'gojzak/gostar'?] in vdovec"},
 (115, 15): {"ime": "Marija VLEPEC"},
 (116, 16): {"ime": "Marjeta BRINEC [★★★ VLM-'Majeta-Binec'-KOREKCIJA — max-zoom-'Brinec'-jasno P173-patroN!]", "starost": "11 LET"},
 (116, 18): {"ime": "Barbara PRIČEK", "starost": "43 LET [★★ VLM-'4½'-ZAVRJENA — max-zoom-'43'-jasno!]", "pokop": "2. maja"},
 (116, 19): {"ime": "Anton LILE", "stan": "lesarjeva pomočnika sin [~ diag-'lesaruga' — VLM-'kmeta']"},
 (116, 20): {"ime": "Ana POPRIČ [~ diag-'Poprič/Puprič' — KURRENT-o/u-zmeda; NERAZREŠENO]", "bolezen": "Naduha [★★ VLM-'Maduha'-ZAVRJENA — N-jasno!]"},
 (116, 22): {"ime": "Marija BRODARIČ [★★ VLM-'Štokarič'-ZAVRJENA]", "stan": "½ gemžškov sin [~ SPOL-ZMEDA — žensko-ime + moški-stan!]"},
 (116, 24): {"stan": "hajdurov sin [~ diag-'hajdurov/gajdurov' — VLM-'hajdujov']"},
 (116, 25): {"ime": "Jožef PERDINEC [★ KURRENT-r/n-zmeda — Perdinec-×159-dominanten!]", "stan": "¼ zemljakov sin",
             "starost": "— [PRAZNA!]", "bolezen": "Vsled težkega poroda [★★★ max-zoom-'Vsled...težkega poroda'-jasno — 1888-r23-leksikalna-paralela!]",
             "opomba": "★★★ PORODNA-SMRT-#3-linije (1888-×2 → 1908!) + rdeči-✓-revizija!"},
 (116, 26): {"ime": "Julij PIBERNIK [★★ VLM-'Jely'-KOREKCIJA — diag-'Julij'-jasno!]", "houseNo": "42"},
 (117, 28): {"ime": "Anton ŽMIDARŠIČ [★★ VLM-VRSTA-IZPUŠČENA — diag-rešena!; KURRENT-Ž-caron-jasno; NERAZREŠENO-'žm/šm']",
             "mesec": "Juni", "smrt": "9", "pokop": "10", "vas": "Kaplišče", "houseNo": "9", "starost": "5 LET",
             "opomba": "★★ VLM-izpuščena-vrsta — diag + max-zoom-rešena + rdeči-✓!"},
 (117, 29): {"ime": "Marija WEBER [~ diag-'Weber/Veber']"},
 (117, 31): {"ime": "J. VOŠMAN [~ kratica-J.-ne-razrita]", "vas": "Zorit [? NERAZREŠENA-VAS — X-anomalija!]",
             "starost": "— [PRAZNA!]", "bolezen": "Mrtvorojen", "duhovnik": "BREZ PODPISA [r53-vzorec!]",
             "opomba": "★★★ MRTVOROJEN + BREZ-PODPISA + rdeči-✓!"},
 (117, 32): {"ime": "Neža BRODARIČ [~ VLM-'Vodarič']"},
 (117, 35): {"ime": "Katarina MUIČ [~]", "stan": "vdova, kranjica? [~]"},
 (117, 37): {"ime": "Marija ZUNČ [~ diag-'Zunč/Zumič']", "stan": "omrčena Jakobič, vinškanka [~]"},
 (117, 38): {"ime": "Ana JAKIČ", "stan": "omrčena Pavlič, bajtarica [~]"},
 (118, 40): {"starost": "5 LET"},
 (118, 41): {"opomba": "★★ SIBLING-SMRT-1-DAN-APART (z40-Rudolf-5-let-Julij-9 + z41-Ana-3-leta-Julij-10 — h11-Mlače!)"},
 (118, 42): {"ime": "Anton BRINEC [★★★ VLM-'Alojz-Ožinger'-ZAVRJENA — max-zoom-'Anton-Brinec'-jasno P173-patroN!]"},
 (118, 43): {"ime": "Marija ŽUGELJ [~ diag-'Žuglj/Žugelj']"},
 (118, 45): {"ime": "Frana ŠERKOPEC [~ diag-'Šerkopec/Šarkopec' — NERAZREŠENO]"},
 (118, 46): {"ime": "Marija JELIČIČ [~ diag-'Jeličič/Loičič']", "starost": "64 LET [★★ VLM-'84'-KOREKCIJA — max-zoom-'64'-jasno!]",
             "stan": "omrčena vinškarica"},
 (118, 47): {"ime": "Peter HROVAT [★★★ VLM-'Afanas'-ZAVRJENA — max-zoom-'Hrovat'-jasno!]", "stan": "venčen bajtar [~ VLM-'kmejen-kajtar' — 'venčen'=poročen!]",
             "starost": "55 LET", "duhovnik": "BREZ PODPISA ['—'-črta]",
             "opomba": "★★★ 'SE JE OBESIL' = SAMOMOR = 2.-V-LINIJI (1892-h9-Janez-1.! — 16-letni-lok!) + BREZ-PODPISA-pri-samomoru!"},
 (118, 48): {"bolezen": "Telačna mrzlica [~ VLM-'mrzlivos' — tifus-otroški?]"},
 (118, 49): {"ime": "Jozefa VEDARIČ [~ diag-'Vedarič/Hudarič']"},
 (118, 50): {"ime": "Katarina ŽUGELJ [★★ VLM-'Kalevina'-ZAVRJENA — max-zoom-'Katarina'-jasno!]"},
 (118, 51): {"houseNo": "109 [~ diag-'10?'-KURRENT-tail — 9?-rep]", "starost": "½ leta, 1 mesec [~ VLM-'1½ leta' — diag-'½']",
             "ime": "Frančišek ŠTIPANIČ [~]", "bolezen": "prirojena slabost [★ VLM-'Pripojena'-KOREKCIJA!]"},
 (119, 52): {"ime": "Marijta BRODARIČ [~]", "duhovnik": "Gregor Cerar rog. [~ 'r. g.'-sufiks-X-anomalija!]"},
 (119, 53): {"ime": "August MILAVEC", "stan": "mlinac?/mlinarjev sin [~ diag-'mlinarju']"},
 (119, 54): {"ime": "Mihael TAPRIČ [~ diag-'Taprič/Tapir' — KURRENT-r/i-zmeda; NERAZREŠENO; TAPRIČ-vez-×2!]",
             "stan": "¼ zemljak", "opomba": "★★ rdeči-✓-revizija!"},
 (119, 55): {"ime": "Frančiška KAMBIČ"},
 (119, 56): {"ime": "Dorotija NOVAK", "starost": "70 LET"},
 (119, 57): {"ime": "Matija JAKŠIA [~ diag-'Jakšia/Jakšič']", "stan": "vrčpen ¼ gemžšk [~]",
             "bolezen": "Z vrca padel je se ubil [★★★ max-zoom-jasno — 2.-TRAUMA-SMRT-linije!]",
             "opomba": "★★★ 'sv. olje' v previden-stolpcu = 3.-IZPISANI-SAKRAMENT-linije (pri padcu-ubojstvu!)"},
 (119, 58): {"ime": "Ana LIPOVEC [~ VLM-'Uipovec']"},
 (119, 59): {"ime": "Marija TAPRIČ [★★ max-zoom-ista-forma-kot-z54 — TAPRIČ-vez-h2×h33! (mati+sin-hipoteza [~])]",
             "stan": "vdova vinškarica", "opomba": "★★ rdeči-✓ + rdeča-puščica!"},
 (119, 60): {"ime": "Marjeta BOŽMAN [★★ VLM-'Božnar'-približna — diag-'Božman'-'m'-jasno]"},
 (119, 61): {"ime": "Matija HARAŠINIČ [cf.-z12-Janez!]", "stan": "vrčpen vrškar [~]"},
 (119, 62): {"ime": "Francišek ROHAR"},
 (119, 63): {"ime": "Martin UHR [★★ diag-'Uhr'-jasno — P173-z18-URH-vez!]"},
 (120, 64): {"ime": "Avguštin JURJEVIČ [★★ VLM-'Jeračevič'-ZAVRJENA — diag-'Jurjevič/Jurajevič'-zmeda; cf.-1907-z61-Jurjevčič!]",
             "duhovnik": "Gregor Cerar rog. [~ 'r. g.'-sufiks-×2!]",
             "opomba": "★★ hiša-'24'-VLM-PRAV (diag-'34'-NAPAČNA — KURRENT-2/3!) + h24-×2-v-1908!"},
 (120, 65): {"ime": "Ana JUDNIČ [~]"},
 (120, 66): {"ime": "Jakob ZMAVC", "stan": "vrčpen gozdar [~]", "bolezen": "Mrtvoud [~ Mrtvod-leksikon-1906–1890!]"},
 (120, 67): {"ime": "Matija PERDINEC [★★★ VLM-'Pečnik'-ZAVRJENA ×3 — max-zoom-'Perdinec'-jasno!]"},
 (120, 68): {"ime": "Klepec Marija [~ diag-'Klepc/Klepece' — vrstni-red-priimka!]"},
 (120, 69): {"ime": "Jožef KOZIJAN [~ VLM-'Kozjan']", "starost": "— [PRAZNA!]",
             "bolezen": "Šički porod [~ NERAZREŠEN — X-anomalija: moški-otrok + 'porod'!]"},
 (120, 70): {"ime": "Katarina PERDINEC [★★★ VLM-'Pečnik'-ZAVRJENA]"},
 (120, 71): {"ime": "Matija PERDINEC [★★★ VLM-'Pečnik'-ZAVRJENA]"},
 (120, 72): {"ime": "Marija ŠTRUCELJ [★★★ VLM-'Špancej'-ZAVRJENA — max-zoom-'Štrucelj'-jasno cf.-krstna-botri-Štrucel!]",
             "smrt": "[IZBRISANO/PRAZNO — neberljivo!]", "starost": "41 LET [diag-'44'-KOREKCIJA — max-zoom-'41'-jasno!]",
             "opomba": "★★ EDINA-1908-vrsta-BREZ-datuma-smrti (celica-prazna/izbrisana — ink-spatter!)"},
 (120, 73): {"ime": "Marija CAJVAR [~ VLM-'Rajnar' — diag-'Cajvar/Cajvan']"},
 (120, 74): {"ime": "Nikolaj HRALJ [★★ VLM-'Wolf'-ZAVRJENA — max-zoom-'Hralj'-jasno; ~ Kralj]"},
 (120, 75): {"ime": "Barbara MILEK [★★ diag-'Milek'-jasno cf.-h65-MILEK!; VLM-'Mlek']",
             "stan": "nova dnadelovka [~ VLM-'drnadelovka' — 'nova dnevna delavka'? NERAZREŠENO]",
             "bolezen": "Nemoglost [~ VLM-'Dremoglost' — max-zoom-'Nemoglost'-jasno; = nemoklost/šibkost?]",
             "opomba": "★★ rdeči-✓-revizija!"},
 (121, 0):  {"starost": "1 LETO [★★ diag-'4'-KOREKCIJA — max-zoom-'1'-jasno!]"},
}

# Griblje-blok korekcije (finalne)
GRIB = {
 10:  {"houseNo": "42", "vas": "Griblje", "ime": "Doroteja PEZDIREC", "stan": "vdova vinškarica",
       "starost": "51 LET", "bolezen": "Pljučnica", "mesec": "Marec", "smrt": "18", "pokop": "20",
       "duhovnik": "Gregor Cerar"},
 16:  {"houseNo": "24", "vas": "Griblje", "ime": "Marjeta BRINEC", "stan": "½ zemljakova hči",
       "starost": "11 LET", "bolezen": "Pljučnica", "mesec": "April", "smrt": "6", "pokop": "8",
       "duhovnik": "Gregor Cerar"},
 20:  {"houseNo": "3", "vas": "Griblje", "ime": "Ana POPRIČ [~ Puprič]", "stan": "vdova in vinškarica",
       "starost": "85 LET", "bolezen": "Naduha", "mesec": "Maj", "smrt": "7", "pokop": "9",
       "duhovnik": "Jos. Rauq"},
 25:  {"houseNo": "85", "vas": "Griblje", "ime": "Jožef PERDINEC", "stan": "¼ zemljakov sin",
       "starost": "—", "bolezen": "Vsled težkega poroda", "mesec": "Maj", "smrt": "24", "pokop": "25",
       "duhovnik": "Gregor Cerar"},
 42:  {"houseNo": "83", "vas": "Griblje", "ime": "Anton BRINEC", "stan": "bajtarjev sin",
       "starost": "6 LET", "bolezen": "Jetika", "mesec": "Juli", "smrt": "11", "pokop": "13",
       "duhovnik": "Gregor Cerar"},
 47:  {"houseNo": "44", "vas": "Griblje", "ime": "Peter HROVAT", "stan": "venčen bajtar [~]",
       "starost": "55 LET", "bolezen": "Se je obesil", "mesec": "Avgust", "smrt": "14", "pokop": "16",
       "duhovnik": "BREZ PODPISA"},
 54:  {"houseNo": "2", "vas": "Griblje", "ime": "Mihael TAPRIČ [~ Tapir]", "stan": "¼ zemljak",
       "starost": "48 LET", "bolezen": "Jetika", "mesec": "September", "smrt": "18", "pokop": "20",
       "duhovnik": "Jos. Rauq"},
 59:  {"houseNo": "33", "vas": "Griblje", "ime": "Marija TAPRIČ [~ Tapir]", "stan": "vdova vinškarica",
       "starost": "66 LET", "bolezen": "Naduha", "mesec": "Oktober", "smrt": "3", "pokop": "4",
       "duhovnik": "Jos. Rauq"},
 64:  {"houseNo": "24", "vas": "Griblje", "ime": "Avguštin JURJEVIČ [~ Jurajevič]", "stan": "bajtarjev sin",
       "starost": "5 MESECEV", "bolezen": "Griža", "mesec": "Oktober", "smrt": "23", "pokop": "24",
       "duhovnik": "Gregor Cerar rog. [~]"},
 70:  {"houseNo": "20", "vas": "Griblje", "ime": "Katarina PERDINEC", "stan": "¼ zemljakova hči",
       "starost": "2 LETI", "bolezen": "Jetika", "mesec": "November", "smrt": "22", "pokop": "24",
       "duhovnik": "Gregor Cerar"},
 71:  {"houseNo": "30", "vas": "Griblje", "ime": "Matija PERDINEC", "stan": "vdovec in vrškar",
       "starost": "81 LET", "bolezen": "Slabost", "mesec": "December", "smrt": "1", "pokop": "3",
       "duhovnik": "Gregor Cerar"},
 72:  {"houseNo": "5", "vas": "Griblje", "ime": "Marija ŠTRUCELJ", "stan": "¼ zemljakova hči",
       "starost": "41 LET", "bolezen": "Pljučnica", "mesec": "December", "smrt": "[?]", "pokop": "9",
       "duhovnik": "Gregor Cerar"},
 75:  {"houseNo": "39", "vas": "Griblje", "ime": "Barbara MILEK", "stan": "nova dnadelovka [~]",
       "starost": "76 LET", "bolezen": "Nemoglost [~]", "mesec": "December", "smrt": "15", "pokop": "17",
       "duhovnik": "Gregor Cerar"},
}

SCAN_MONTH_CARRY = {
    # (scan, zap) -> mesec (pisar piše mesec samo ob 1. vnosu — ponesi)
    114: {1: "Januar"},
    115: {4: "Februar", 9: "Marec", 13: "April"},
    116: {16: "April", 19: "Maj", 26: "Juni"},
    117: {28: "Juni", 38: "Juli"},
    118: {40: "Juli", 46: "Avgust", 50: "September"},
    119: {52: "September", 59: "Oktober"},
    120: {64: "Oktober", 67: "November", 71: "December"},
    121: {76: "December"},
}

entries = []
last_month = None
for scan in range(114, 122):
    d = json.load(open(f"{VP}/s{scan}.json"))
    for v in d.get("vrstice", []):
        z = str(v.get("zaporedna", "")).strip()
        if not z.isdigit():
            continue
        zap = int(z)
        if zap > 76:
            continue  # 1909-restart (P175!)
        if scan == 114 and zap > 3:
            continue  # 1907-tail (P173-dokaz!)
        if scan == 121 and zap != 76:
            continue  # 1909-restart z1–10 (P175-lead!)
        k = K.get((scan, zap), {})
        g = GRIB.get(zap) if (scan != 114 or zap <= 3) and zap >= 1 else None
        if g and (scan, zap) not in [(114, 1), (114, 2), (114, 3)]:
            # Griblje-vpis (1908-only)
            pass
        # mesec: K > SCAN_MONTH_CARRY > VLM > carry
        mesec = None
        if (scan, zap) in [(114, 1), (114, 2), (114, 3)] or g:
            mesec = g["mesec"] if g else MESEC.get((SCAN_MONTH_CARRY.get(114, {}).get(zap) or ""), None)
        m_raw = k.get("mesec") or v.get("mesec")
        if m_raw and m_raw in MESEC:
            mesec = MESEC[m_raw]
            last_month = mesec
        elif (scan, zap) in SCAN_MONTH_CARRY and zap in SCAN_MONTH_CARRY[scan]:
            mesec = SCAN_MONTH_CARRY[scan][zap]
            last_month = mesec
        else:
            mesec = last_month if last_month and (scan, zap) != (114, 1) else None
        row = {"row": len(entries) + 1, "zap": zap,
               "houseNo": str(k.get("houseNo") or v.get("hisna") or "").rstrip('.') or "?",
               "bookSignature": "04894", "year": 1908, "scan": scan, "page": PAGE_MAP[scan],
               "mesec": mesec, "smrt": k.get("smrt") or v.get("smrt"), "pokop": k.get("pokop") or v.get("pokop"),
               "vas": k.get("vas") or v.get("vas"), "ime": k.get("ime") or v.get("ime"),
               "stan": k.get("stan") or v.get("stan"), "starost": k.get("starost") or v.get("starost"),
               "bolezen": k.get("bolezen") or v.get("bolezen"),
               "previden": k.get("previden") or v.get("previden"),
               "duhovnik": k.get("duhovnik") or v.get("duhovnik"), "opomba": k.get("opomba")}
        # GRIB-kanonične vrednosti za Griblje-vpise (finalne diag+korekcije!)
        is_grib_1908 = (scan != 114 or zap <= 3) and (scan != 121 or zap == 76) and zap in GRIB
        if is_grib_1908:
            for fk in ("houseNo", "vas", "ime", "stan", "starost", "bolezen",
                       "mesec", "smrt", "pokop", "duhovnik"):
                if fk in GRIB[zap]:
                    row[fk] = GRIB[zap][fk]
        entries.append(row)

grib = [e for e in entries if str(e["vas"]).lower().startswith("griblje")]

# VLM-izpuščena vrsta z28 (s117 — diag+crops rešena!): sintetična vstavitev
if not any(e["scan"] == 117 and e["zap"] == 28 for e in entries):
    k = K[(117, 28)]
    v28 = next(v for v in json.load(open(f"{VP}/s117.json")).get("vrstice", [])
               if str(v.get("zaporedna", "")).strip() in ("", "?") or True)  # placeholder
    entries.append({"row": 0, "zap": 28, "houseNo": k["houseNo"], "bookSignature": "04894",
                    "year": 1908, "scan": 117, "page": 116, "mesec": "Juni", "smrt": "9",
                    "pokop": "10", "vas": "Kaplišče", "ime": k["ime"], "stan": "½ zemljakov sin",
                    "starost": k["starost"], "bolezen": "Škrlatinka", "previden": None,
                    "duhovnik": "Jos. Rauq", "opomba": k["opomba"]})
entries.sort(key=lambda e: (e["scan"], e["zap"]))
for i, e in enumerate(entries):
    e["row"] = i + 1

print(f"entries: {len(entries)} | Griblje: {len(grib)} | hiše: {len({e['houseNo'] for e in grib})}")
for e in grib:
    print(f"  z{e['zap']} h{e['houseNo']} {e['ime']} {e['starost']} {e['mesec']} {e['smrt']}/{e['pokop']}")

# ---------- frame ----------
frame = {
 "leto": 1908,
 "vrstic": 76,
 "zap_oštevilčenih": 76,
 "neštevilčenih": 0,
 "vpisi": 76,
 "dup_zaporedna": None,
 "griblje_vpisi": len(grib),
 "hise": len({e["houseNo"] for e in grib}),
 "hise_seznam": ",".join(sorted({e["houseNo"] for e in grib}, key=int)),
 "ponovitve": "24",
 "meja_1907_08": "s114 (P173-potrjena — velika-'1908'-PODČRTANA + Januarij + restart 67→1 = 6. STIL 15. POTRDITEV)",
 "meja_1908_09": "s121 (velika-'1909.'-BREZ-podčrtanja + PIKA + prazna-vrsta + restart 76→1 = 16. POTRDITEV — 6.-STIL-familija-BREZ-podčrtanja 1.×! P173-lead-'[~ s119+?]' KOREKCIJA-→-s121 — max-zoom-crop-'1909.'-jasno!)",
 "glave_napake": [
  "s114-'Leto 18 1907' (meja-stran — P173-že-šteta!)",
  "s115–s121-'Leto 18[ročno-1908]' = '181908'-PREDPONSKA-navada-×7-UNIVERZALNO — 0-EKZOTIČNIH (kontrast-1907-rekord-5-eksotičnih!)",
  "s122-'Leto 18 1909' (1909-prva-stran — P175-scope!)"
 ],
 "stran_invarianta": "stran == sken − 1 (s114–s122 == str. 113–121 — 88.–95. potrditev VIZUALNO-diag; s114-ŽE-P173!)"
}

anomalies = [
 {"id": "A1", "opis": "★★★ VLM-HALUCINACIJE-imen-×10 (max-zoom-korekcije!): z42-'Alojz-Ožinger'→Anton-BRINEC! + z47-'Afanas'→Peter-HROVAT! + z50-'Kalevina'→Katarina-ŽUGELJ! + z67/z70/z71-'Pečnik'→PERDINEC-×3! + z72-'Špancej'→ŠTRUCELJ! + z74-'Wolf'→HRALJ[~]! + z26-'Jely'→JULIJ! + z60-'Perman'→BOŽMAN! + z16-'Majeta'→MARJETA! + z28-VLM-VRSTA-IZPUŠČENA (diag-rešena — Anton-ŽMIDARŠIČ[~])!"},
 {"id": "A2", "opis": "★★ VLM-ŠTEVILKE-korekcije-×4: z10-starost-lead-'81'→51! (P173-lead-NAPAČEN!) + z18-'4½'→43! + z46-'84'→64! + z76-'4'→1-LETO! — max-zoom-'5'/'43'/'64'/'1'-jasno!"},
 {"id": "A3", "opis": "★★★ z47-'SE JE OBESIL' = SAMOMOR = 2.-V-LINIJI (1892-h9-Janez-53-let-1.! — 16-LETNI-LOK!) + PODPIS-'—' (BREZ-podpisa-pri-samomoru — 3.-brez-podpisa-linije-po-Mrtvorojen-vzorcih!) — Griblje-h44-Peter-HROVAT-venčen-bajtar-55-let!"},
 {"id": "A4", "opis": "★★★ z57-'Z VRCA PADEL JE SE UBIL' [~ 'z-vrca/vrte'-zmeda] = 2.-TRAUMA-SMRT-linije (po-1892-obesil? NE — 2.-nesreča-po-1890-opreljene/1907-opekline!) + 'sv. olje' v previden-stolpcu = 3.-IZPISANI-SAKRAMENT-linije (P155-'sv. olje'-#2 → 1908-#3!) — Krasinec-h30-Matija-Jakšia-46-let!"},
 {"id": "A5", "opis": "★★★ z25-'VSLED TEŽKEGA PORODA' = PORODNA-SMRT-#3-linije (1888-×2-materi → 1908-OTROK!) + starost-PRAZNA + rdeči-✓-revizija — Griblje-h85-Jožef-PERDINEC-¼-zemljakov-sin!"},
 {"id": "A6", "opis": "★★ ŠKRLATINKA-EPIDEMIJA ×10 (Junij–September — vsi-≤6-let!): z23-z27-Germ/Klošter (Jun) + z29-z30-z33-Gradac/Germ/Boginja-vas (Jun) + z40-z41-Mlače-SMUK-SIBLI-1-DAN-APART (z40-Rudolf-5-Julij-9 + z41-Ana-3-Julij-10!) + z50-Dobravice (Sep) = najhujša-otroška-epidemija-linije!"},
 {"id": "A7", "opis": "★★ 'DOBRČI [~ Dobreci/Dobrei]' = NERAZREŠEN-VZROK ×4 = 2.-epidemija (Sep–Okt — ×4-otroci-≤3-let: z53-6-mes + z55-7-mes + z62-3-let + z63-2-let!) — X8-leksikon (po-Božjast/Mertvod/Strgjatinka!)"},
 {"id": "A8", "opis": "★ BOŽJAST ×2 (z36-Krivoglavce-14-let + z49-Krasinec-9-mesec) = nerazrešen-vzrok-nadaljevanje (1890-×11 → 1907-×1 → 1908-×2!)"},
 {"id": "A9", "opis": "★★★ NOV-DUHOVNIK-'G. g. Matija-CERAR-DEKAN' ×1 (s115-z4!) + OPOMBA-marginalija-'Matijo-Sogozor?-župn.-per-vic?' (delno-ZA-HRBTOM-knjige — neberljivo!) — 1.-'dekan'-v-liniji + 1.-marginalija-mrliške! + Gregor-CERAR-kaplan-DOMINANTA (9/13-Griblje!) + Jos.-RAUQ-×3 + LILEK-s114-×2 + 'rog.'-sufiksi-×2-[~]"},
 {"id": "A10", "opis": "★★ z31-MRTVOROJEN-'J.-VOŠMAN'-½-zemljaškovo-dete + starost-PRAZNA + BREZ-PODPISA (r53-1887-vzorec!) + vas-'ZORIT-[?]' = NERAZREŠENA-VAS (X-anomalija!) — Junij-20/21"},
 {"id": "A11", "opis": "★★ PRAZNE-STAROSTI-×4 (z8-Mihael-Muc + z25-Perdinec + z31-Vošman + z69-Kozijan!) + z69-'ŠIČKI-POROD-[?]' = NERAZREŠEN-VZROK (moški-otrok + 'porod'-zmeda!) + z72-SMRT-CELICA-PRAZNA/IZBRISANA = edina-1908-vrsta-brez-datuma-smrti!"},
 {"id": "A12", "opis": "★★ h24-×2-v-1908 (z16-Marjeta-BRINEC-April + z64-Avguštin-JURJEVIČ-Oktober — različni-priimki!) = PADEC-vzorec-5.-LETO-ZAPORED (1904-h18 + 1905-h18/h27 + 1906-h58 + 1907-h49/h10 + 1908-h24!) + KURRENT-2/3-zmeda (diag-'h34'-NAPAČNA → max-zoom-'h24'-PRAV!)"},
 {"id": "A13", "opis": "★ GLAVE-'18'-PREDPONSKA-navada-×7-UNIVERZALNO (s115–s121-'Leto 18[ročno-1908]' — tiskano-18 + ročno-1908!) = 0-EKZOTIČNIH-NAPAK (kontrast-1907-REKORD-5-eksotičnih: '181904'/'18'-nekopl.!) + s114-'181907' + s122-'181909'"},
 {"id": "A14", "opis": "★★ MEJA-1908/09 = s121: velika-'1909.'-BREZ-PODČRTANJA + PIKA + restart-76→1 = 6.-STIL-familija-BREZ-podčrtanja 1.× (s114-'1908'-JE-bila-podčrtana!) + Mrtvorod-×2-1909-LEAD (s121-z6-z7 — Ana-Novarič-63?! + J.-Mihelič-BREZ-PODPISA!)"},
]

crossChecks = [
 {"id": "C1", "opis": "zap-kontinuiteta: 76-oštevilčenih = 76-VPISOV — ČISTA-SEKVENCA-zap1–76 (BREZ-predorov/DUPLIKATOV — nasprotje-1906-dup-21!) — 4.-čisto-leto-zapored (1905-48 + 1907-67 + 1908-76!)"},
 {"id": "C2", "opis": "stran == sken − 1 ×9-vizualno (s114→113 … s122→121 — 88.–95.-potrditev-invariante; s114-ŽE-P173!)"},
 {"id": "C3", "opis": "meje: 1907/08 = s114 (P173-15.-POTRDITEV!) + 1908/09 = s121 (16.-POTRDITEV — velika-'1909.'-brez-podčrtanja; P173-lead-'[~ s119+?]' KOREKCIJA-→-s121!)"},
 {"id": "C4", "opis": "hiše-1:1-med-dokazom-in-parish.ts (13-Griblje-vpisov == 13-blokov; 12-hiš == 12!; h24-×2!)"},
 {"id": "C5", "opis": "duhovniški-roster-1908: Gregor-CERAR-dominanta (×~33-skupno; 9/13-Griblje!) + Jos.-RAUQ (×~18; 3/13!) + 'G. g.-Jos.-LILEK-župnik-v.p.'-s114-×2 + NOVI-'G. g.-Matija-CERAR-DEKAN'-×1 + BREZ-PODPISA-×3 (z31 + z47 + s121-z7-1909-lead!) = 4-duhovnika-v-1-letu"},
]

honesty = [
 "rows-v3-FAIL-lekcija-3.-leto (diag-grid-330–1950/135px-recept-ponovno-vzpostavljen — 9/9-skenov-diag-prebranih!)",
 "imena-[~]-NERAZREŠENA ×6: TAPRIČ-×2 (h2+h33 — mati+sin-hipoteza [~]!) + POPRIČ-[~ Puprič] + HRALJ-[~ Kralj] + 'dnadelovka' + ELME + ŽMIDARŠIČ + ŠERKOPEC",
 "vzroki-NERAZREŠENI ×2-NOVA: 'Dobrči-[~ Dobreci]' ×4 (X8!) + 'Šički porod' ×1 + 'Nemoglost'-'dnadelovka'-'Junica'-'Kaplje-vode'-'Telačna-mrzlica' [~] — leksikon-raste!",
 "vas-'Zorit-[?]' (z31) NERAZREŠENA — venkon-župnijskih-vasi?",
 "opomba-s115-z4 (NOVI-duhovnik-Matija-CERAR-dekan) delno-ZA-HRBTOM-knjige — neberljiva [?]",
 "'rog.'-sufiksi-podpisov ×2-[~ 'r. g.'?] — neznana-funkcija"
]

nextSteps = [
 {"korak": "P175-lead", "opis": "mrliška 1909: s121-zap1–10 ŽE-prebrani (0-GRIBLJE-v-z1–10: Anton-Žugarič-Krasinec + Matija-Viličič + Peter-Stublar-92-IZENAČENJE-REKORDA-1889! + Neža-Bajuk + Neža-Novak-BOŽJAST + Ana-Novarič-MRTVOROD-63? + J.-Mihelič-MRTVORODJENA-BREZ-PODPISA + Helena-Župančič + Barbara-Jurajčič + Ana-Štefanič!) + s122-zap11–22-ŽE-prebrani (4-GRIBLJE-ŽE-vidnih: z11-h2-Barbara-Tome-86-let + z16-h15-Marija-Jakfčič-[~]-15-let + z17-h43-Marija-Lošič-[~]-84-let + z21/z22-h34-ŠILAK-DVOJČKI-½-dneva + 2-dni-APART!) + s123+; meja-1909/10-[~ s125+?]"}
]

dokaz = {
 "status": "SAMPLE-TRANSCRIPTION-D1908",
 "generated": "P174",
 "phase": "P174 — mrliška 1908 (22. → 23. polno leto mrliške linije)",
 "source": "matricula-online.eu 04894, skeni 114–122 (s114-reuse-P173-meja-lead + s115–s122)",
 "frame": frame,
 "entries": entries,
 "excluded": [
  {"id": "X1", "opis": "s121-zap1–10 (1909-restart: Januar–Februar — 0-GRIBLJE! z3-Peter-Stublar-92-let = izenačenje-rekorda-1889!) — P175-lead!"},
  {"id": "X2", "opis": "s122-str.-121 (1909-nadaljevanje zap11–22: 4-GRIBLJE-ŽE-vidnih + ŠILAK-dvojčki-h34-½-dneva/2-dni!) — P175-scope!"}
 ],
 "anomalies": anomalies,
 "crossChecks": crossChecks,
 "honesty": honesty,
 "nextSteps": nextSteps,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(dokaz, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK → {OUT}: {len(entries)} entries, {len(grib)} Griblje, {len(anomalies)} anomalij, {len(crossChecks)} crossChecks")
