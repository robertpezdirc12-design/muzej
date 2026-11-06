#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P201 — build proof research/issue17/parish-death-1876-04106.json (recept P200)."""
import json

E = json.load(open("/tmp/p201/entries_1876.json"))
entries = E["entries"]
tail_1875 = E["tail_1875"]
griblje = [e for e in entries if e["vas"] and "gribl" in e["vas"].lower()]

def g(zap):
    for e in griblje:
        if e["zap"] == zap:
            return e
    raise KeyError(zap)

mesi = {}
for e in entries:
    mesi[e["mesec"]] = mesi.get(e["mesec"], 0) + 1

OTROŠKE = ["24", "26", "30", "32", "36", "40", "41", "43", "59", "83", "86"]  # zap-ji-otrok (ročno-verificirano — '36 J.'-odrasli-IZKLJUČEN!)
otroci = [e for e in griblje if e["zap"] in OTROŠKE]

proof = {
    "faza": "P201",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1876 = 10. leto PREDZGODOVINSKE LINIJE (issue #18)",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1876": "s134-z5–s142-z10 == Pag. 128–136 (pag == sken − 6!); 89 vpisov (z1–z89, ŠTEVJE-IZ-VRSTIC — ordinali-NEVIDNI-×9!) / 20 Griblje / 19 hiš (h46-×2!); DECEMBER-1876 = 0-vpisov!",
        "meja_1875_76": "★★★ s134 (pag 128): TAIL-4-DEZ-1875-nad (z1–z4: Dez-14/16 + 22/23 + 22/24 + 24/26!) + VELIKA-'1876 Jänner'-GLAVA-V-SREDINI-STRANI (KROP: ročno-veliko-'1876 Jänner' + velika-beseda-'Jahr'-desno — drugačna-fraza-kot-1877-'18 77.'-ODREZANA!) + RESTART-Jänner-2.-pod (z5: Krasinec-30-Peter-1½-Mon.!) — ordinali-NEVIDNI-tudi-tu!",
        "meja_1876_77": "s143 (P200-reuse + TA-SEJA-RE-VERIFIKACIJA): '18 77.'-glava-ODREZANA-off-scan — P200-z1 = Jänner-1877-STOI (KROP-ta-seja: smrt-'1.'/pokop-'8.' + 'todt geboren zu Podžemelj'-opomba + restart-1 + Jänner-pod-z2!) → P200-60-vpisov-NETAKNJENA + DECEMBER-1876 = 0!",
        "konec_1876": "z89 = s142-v10 (Nov-29-smrt/pokop-'31.'[=Dez-1!] — Georg-Mur-Primostek-4-5½J!) — leto-konča-z-NOVEMBERJEM (brez-December-bloka!)",
        "zaporedna": "ordinali-NEVIDNI-na-vseh-9-straneh (VLM-×9: 'stolpec-ne-obstaja'/'brez-zaporednih'/'starejši-format'!) → ŠTEVJE-IZ-VRSTIC (recept-s148-2.× → 3.×!); zap-z1–z89 = REKONSTRUIRAN",
        "forma": "tiskane-glave-Sterb-Buch + ročni-meseci; '1876.'-glave-V-DATUMSKI-CELICI: s136-z1 (März! = 40.-POTRDITEV-invariante!) + s142-z1 (November! = 41.-POTRDITEV!) + s134-velika-'1876-Jänner' (MEJA-fraza!)",
        "skeni": "s133–s142 (pag 127–136); s142-md5-križna-validacija-ta-seja: svež == P200-disk-1:1 (b80a1ad1b969) — VERIGA-P197→P198→P199→P200→P201-5.×!; s133 = 1875-kontekst (Nov–Dez-1875-×11 — P202-lead!)",
        "preštevanje": "vrstna-aritmetika 6+12+12+10+10+9+10+10+10 = 89 ✓; meseci: Jänner-6 + Februar-9 + März-6 + April-6 + Mai-9(+1-Mai/Juni) + Juni-7 + Juli-5 + August-10 + September-16 + October-4 + November-10 = 89 ✓ + DECEMBER-0!",
    },
    "statistika": {
        "vpisov_1876": 89,
        "griblje": len(griblje),
        "hise": sorted({str(e["hisna"]).rstrip(".").split()[0] for e in griblje}, key=lambda x: int(x)),
        "otrok_griblje": f"{len(otroci)}/20 = {round(100*len(otroci)/20)}%",
        "december": 0,
        "november": 10,
        "duhovniki": "Hogeja/Hoggin/Hogyi-Coop.-×9 (KOGEJ-NIT-1876!) + Franz-Dorgan-[DOVGAN]-×3 + fortd.-Jos.-Hozjan-Capp.-×2 + Justiniant-Roggia-Cœp.[?]-×1",
    },
    "anomalije": [
        "★★★ NOVEMBER-FALSIFIKACIJA: s142-mesec = NOVEMBER (KROP: 'N-o-v-e-m-b-e-r.'-ročno-pod-'1876.'-glavo-v-z1 — črka-za-črko!) — VLM-page-'Dezember'-×2-FALSIFICIRANA! P200-lead-'Dez-1876-tail'-POPREVEK (×3-Griblje-OSTAJAJO-kot-November-vpisi!)",
        "★★★ DECEMBER-1876 = 0-VPIISOV: Nov-30-pokop-'31.'[=Dez-1!] → Jänner-1-1877 (P200-z1-'todt geboren'!) = 31-DNEVNA-BREZ-SMRTI-VRZEL — redka-zerost-v-korpusu (~10-vpisov/mesec-povprečje!)",
        "★★★ MEJA-1875/76-s134: velika-'1876 Jänner'-glava-V-SREDINI + 'Jahr'-beseda + tail-4-Dez-1875-nad + restart-Jänner-2.-pod — ordinali-NEVIDNI!",
        "★★★ s143-z1-RE-VERIFIKACIJA (P200): z1 = Jänner-1877-STOI — KROP-ta-seja: smrt-'1.'/pokop-'8.'-soglasje-P200 + 'todt geboren zu Podžemelj' + restart-1 + Jänner@z2 — P200-60-vpisov-POTRJENA (ne-59!)",
        "★★★ KOGEJ-OBDOBJE-RAZŠIRJENO-V-1876: Hogeja/Hoggin/Hogyi-'Coop.'-×9 (z10/z12-s135-Feb + z22/z30-s136 + z32/z33/z35/z36/z40-s137 + z78-s141-Okt + z83/z85/z86-s142-Nov-'subinuant Hogyi coop.') — P200-'1877-Jänner→Mai'-RAZŠIRJENA-NA-CELO-1876! + Franz-Dorgan-[DOVGAN]-×3 (z24/z26-s136-Apr + z66-s140-Sept + z79-s141-Okt!) + fortd.-Jos.-HOZJAN-Capp.-×2 (z41/z43-s138-Juni!) + Justiniant-Roggia-Cœp.[?]-×1 (z59-s139-Aug!)",
        "★★★ PEZDINC-GRAFIA-#8 (z22-s136-z4): Maria-'Perdire'-h53 — KROP-'P-e-r-d-i-r-e'-črka-za-črko ≈ PEZDIR (VLM-'Perdiue/Perdiu'-t/d-zmeda!) — ★★★ h53-NIT-1876/77-×2: babica-Maria-62J-Auszüglerin-März-29/30-1876-Lungenentzündung + dojenček-Maria-1J-Okt-15/16-1877-Wasserfriesl (P200-z51)! h53 = PEZDIR-gospodinjstvo!",
        "★★★ DRAGOŠ-h12-NIT-1876 (z36-s137-z6): Anton, sin-Joanes-DRAGOŠA (KROP-'So des Joanes Dragoš'!) — h12-¼J [KROP-'¼ J.' — VLM-'2½ J.'-ZAVRJEN!] Mai-28/29-Gehirnfieber — → 1877-z56-Katharina-DRAGOŠ-h12 (P200)! h12-DRAGOŠ-×2-v-2-letih ( Joannes-Drigoš-otoka!) — +opora-DRAGOŠ-na-h12-pred-krstnim-prvencem-1892!",
        "★★★ ŠIMEC-h18-NIT-3.-LETO (z78-s141-z9): Maria-'Simec'-Mädchen (KROP!) — VLM-'Zupančič?/Zimec?'-nesoglasje → ŠIMEC-nit: 1876-Simec-h18-72¾J + 1877-Siniec-h18-8½J + 1878-Innec?-h18 + 1881-TIMEC-h18 = 4-IMENA-4-LETI-NA-h18! [starost-KROP-nesoglasje: '72 3/4'-vs-'74' — [~]]",
        "★ h44-PRIMEK-NESOGLASJE-×3 (z83-s142-z4): 'Kavčič[?]' (VLM-page) / 'Arnuetz[?]' (KROP-'legitimirana-hči-Antona') / 'Struselj[?]' (KROP-2.) — VLM-nesoglasje-×3 → [?]! 24-URE-dojenček-Nov-24/25 (Dez→Nov-POPREVEK!)",
        "★ s142-KRONOLOŠKA-NAPAKA-PISARJA: z4-Nov-24/25-ZAPISAN-PRED-z5-Nov-12/13 (KROP-potrjeno-ob-2.-branjih!) — vpis-izven-kronološkega-reda (1.-pojav-v-korpusu!)",
        "★ '31.'-POKOP-NE-OBSTAJA-V-NOVEMBERJU (z88/z89: Nov-30-smrt + pokop-'31.' = DEZ-1-čez-mejo! ULEDBA-#10-9.-INSTANCE-vzorec!)",
        "★ KERBICA-×2-FRISEN (z41-h20-Mathias-2-Mes + z43-h64-Catharina-vda.-Mathias-Kerbica-1J — s138-Juni! FRISEN-nit + h20/h64-družina-×2-v-6-dneh!)",
        "★ MASERNFRIESEL-z32 (h70-Katharina-6½J-s137-Mai — MASERN-nit-1876: cf. P199-×2-1878 + P200-z6-'Hrib'-h2!) + KLOBUČAR-z24-h46 (→ P199-'KLOBUČAR-h48'-1878-nit!) + GANSSLER-z33-Brinc-h26 + HOZJAN-Capp.-×2-s138",
        "★ s139-TABELA-KONČA-PREK (9-vrstic + prazen-prostor-na-dnu — KROP! pisarjeva-izbira) + z59-Griblje-55-dojenček-hči-Magd.-Agnes-Marzin[?] — kriptičen-vpis (Noth-tauf[?]!)",
        "★★★ GRIBLJE-OTROŠKA-UMRLJIVOST-55%-1876 (11/20: z24-2½J + z26-5J + z30-9J + z32-6½J + z36-¼J + z40-6J + z41-2Mes + z43-1J + z59-dojenček + z83-24-URE + z86-3¾J! cf. 1877-50%)",
        "★ VLM-KROP-korekcije-×8 (NOVEMBER-s142! + März-29-s136-z4-monotoničnost! + ¼J-z36! + Dragoš-z36! + Šimec-z78! + Jakofčič-z79-Hirnhaut! + Arnuetz-z83! + Marzin-z59!)",
    ],
    "duhovniki": {
        "KOGEJ-NIT-1876": "Hogeja/Hoggin/Hogyi-'Coop.'-×9 (Feb→Nov!) — substituendus-grafia (cf. P200-'Hoggai[s]-Coop'-1877! KOGEJ-OBDOBJE-NOW-1876-Feb→1877-Mai-čez-2-leti!)",
        "DOVGAN-×3": "Franz-Dorgan-[DOVGAN]: z24/z26-s136-April + z66-s140-September + z79-s141-October — cf. P200-DOVGAN-dominanta-1877 (Griblje-×6)!",
        "HOZJAN-×2": "fortd.-Jos.-Hozjan-Capp.-z41/z43-s138-Juni (Cappellan! — nov-duhovnik-v-korpusu-1876!)",
        "ROGGIA-×1": "Justiniant-Roggia-Cœp.[?]-z59-s139-August [~grafia]",
    },
    "hišne_kontinuitete": {
        "h53": "×2-1876/77 (Maria-'Perdire'-62J-März-1876 + Maria-'Pezdinc'-1J-Okt-1877 — PEZDIR-gospodinjstvo! babica+dojenček!)",
        "h12": "×2-1876/77 (Anton-sin-Joanes-DRAGOŠA-¼J-Mai-1876 + Katharina-DRAGOŠ-21J-Nov-1877 — DRAGOŠ-otoka!)",
        "h18": "×4-1876/77/78/81 (Maria-'Simec'-72¾J-Okt-1876 + Barbara-'Siniec'-8½J-Mai-1877 + Theresia-'Innec?'-1878 + TIMEC-1881 — ŠIMEC-nit!)",
        "h46": "×2-1876 (z24-Anna-KLOBUČAR-2½J-April + z35-Mathias-'Hlobinar'[~Hlobučar?]-72J-Mai!)",
        "h8": "×2-1876/77 (Anna-Jakofčič-27½J-Okt-1876 + Catharina-JAKOFČIČ-9½mes-Aug-1877 — JAKOFČIČ-nit!)",
        "h44": "×3-nit (Nov-24/25-1876-24-URE-dojenček + 1878-z77 + 1879-katastrofa!)",
        "h75": "×2-1876 (z85-Joannes-STUBLER-50⅔J-Nov + s135-z12-Maria-'Stublar'-Hrovič-56J-Feb? [različni-Stubl-?])",
        "h16": "×2 (z86-Anna-Pilah[~Spilak?]-3¾J-Nov-1876 + P199-1878-z41-nit!)",
    },
    "forme": [
        "VELIKA-'1876 Jänner'-MEJA-GLAVA-s134 (ročno-veliko + 'Jahr'-beseda — drugačna-fraza-kot-1877-'18 77.'-ODREZANA-in-kot-1878-'18 78.'-SPLIT-v-z1!)",
        "'1876.'-glava-V-Z1-DATUMSKI-CELICI-s136 (März-blok-opener! = 40.-POTRDITEV-invariante 'glava-v-z1-celici-letnega-odseka'!)",
        "'1876.'-glava-V-Z1-DATUMSKI-CELICI-s142 (November-blok-opener! = 41.-POTRDITEV! — ta-glava-je-bila-P200-lead-'Dezember'-temelj — zdaj-NOVEMBER!)",
        "mesečne-glave-v-vrsticah: 'Jänner'@z5-s134 + 'Februar'@z7-s135 + 'März'@?-s135/s136 + 'April'@?-s136 + 'Mai'@?-s136/s137 + 'Juni'@?-s137/s138 + 'Juli'@?-s138 + 'August'@?-s138/s139 + 'September'@?-s139/s140/s141 + 'October'@z7-s141 + 'November'@z1-s142 (KROP!) + DEZEMBER-NI-ZAPISAN (0-vpisov!)",
        "ordinali-NEVIDNI-×9 (s134–s142 — 'starejši-format-brez-stolpca'!) → ŠTEVJE-IZ-VRSTIC-3.× (za-1877-s142–s147-in-P199-tail!)",
        "TAIL-4-DEZ-1875-s134-nad-glavo (z1–z4: 14/16 + 22/23 + 22/24 + 24/26 — 1-GRIBLJE: z4-h11-Catharina-KUNIĆ[~Kuniz?]-geb.-Jakoš-65J-Asthma!) — P202-LEAD!",
    ],
    "crossChecks": [
        "md5-križna-validacija: s142-svež == P200-disk-1:1 (b80a1ad1b969) — VERIGA-P197→P198→P199→P200→P201-5.×!",
        "vrstna-aritmetika: 6+12+12+10+10+9+10+10+10 = 89 ✓ (z1–z89!)",
        "meseci-vsota: 6+9+6+6+9(+1)+7+5+10+16+4+10 = 89 ✓ + DEZEMBER-0 ✓",
        "s143-z1-RE-VERIFIKACIJA: smrt-1./pokop-8.-soglasje-P200-KROP + 'todt geboren' + restart-1 → P200-60-NETAKNJENA + December-1876-0 ✓",
        "monotoničnost-s136: z4-März-29/30 (KROP!) — 'April-29'-(VLM)-NEGRE-proti-z6-April-12 → KROP-März-POTRJEN ✓",
        "h53/h12/h18-NITI-križno-vs-P200-dokaz (Pezdinc-z51 + Dragoš-z56 + Siniec-z26) ✓",
        "duhovniki-1876-soglasje: KOGEJ-subst.-×9-čez-9-mesecev (Feb→Nov-kontinuiteta!) ✓",
        "s142-glava-KROP-×3 (N-o-v-e-m-b-e-r-črka-za-črko + '1876.'-nad + dnevi-3/6 + 15/16-soglasja!) ✓",
        "s134-glava-KROP ('1876 Jänner' + 'Jahr'-beseda + tail-2-vrstice-v-kropu-od-4) ✓",
        "s141-z9/z10-dnevi-25/27 + 26/28-soglasje-×3 (VLM-page + KROP-z89 + KROP-levo) ✓",
    ],
    "honesty": {
        "H1": "ordinali-NEVIDNI-×9 → zap-z1–z89 = REKONSTRUIRAN (ŠTEVJE-IZ-VRSTIC — brez-ločenih-konfirmacij!)",
        "H2": "s141-z9-starost-NESOGLASJE: KROP-'72 3/4'-vs-KROP-2.-'74'-vs-VLM-'72 2/5' → '72 3/4 J [~]' (2-od-3-soglasje-o-72!)",
        "H3": "s141-z10-starost-NESOGLASJE: KROP-'27 1/2'-vs-KROP-2.-'½ leta' → '27 1/2 J [~]' (dnevi-26/28-soglasje-×3!)",
        "H4": "h44-PRIMEK-NESOGLASJE-×3: Kavčič[?]/Arnuetz[?]/Struselj[?] → dokumentirano-kot-[?] (ime-Barbara-soglasje-×3!)",
        "H5": "s135-z3/z4-datum-zmeda (Feb-16-vs-Feb-15-ne-monotono) — [~VLM-nestabilnost]",
        "H6": "z59-s139-Griblje-55: kriptičen-vpis ('Nastgainüschb.[?]-Mrenz[?]' + KROP-'dojenček-hči-Magd.-Agnes-Marzin[?]' + Noth-tauf[?]) — [?]!",
        "H7": "DECEMBER-1876-0: temelji-na-s142-NOVEMBER-KROP + s143-z1-Jänner-re-verifikaciji — močna-kompozitna-evidenca, a-mesec-s143-z1-je-FIZIČNO-ODREZAN (ni-mogoče-100%-prebrati!)",
        "H8": "s142-z4-kronološka-napaka-pisarja (Nov-24-pred-Nov-12) — potrjena-×2-KROP, ni-VLM-artefakt",
        "H9": "duhovniški-podpisi: 'Hogeja/Hoggin/Hogyi'-grafia-variante = ista-oseba (substituendus-KOGEJ-vzorec-iz-P200) — interpretacija!",
        "H10": "z83-'24 Stunden'-starost: VLM-page-'[~]' + KROP-ne-celoti (starost-stolpec-izven-kropa) — [~]",
        "H11": "h23-'[~ 28?]'-s136-z8 + h55-'[~ 35?]'-s139-z9 + h70-'[~]'-s137-z2 — hišne-št.[?] — dvomi-dokumentirani",
        "H12": "s133 (1875-kontekst) ni-v-celosti-analiziran-ta-seja (samo-tail-vrste-s134!) — P202-LEAD",
        "H13": "meseci-per-vrstico = VLM-labeli (mesec-glave-ponekod-chybí → row-label-zmeda — vsota-89-je-robu-stabilna!)",
        "H14": "otroška-umrljivost-11/20-klasifikacija: starost-<10-let (24-UR-do-9J) — mejni-primeri-dokumentirani",
        "H15": "bolezni-[?]: 'Vesperstmörfer[?]'-z83 + 'Zo falge[?]'-z59 + 'Husten-such.[?]' — neberljive-[?]",
        "H16": "tail_1875-×4: dokumentirane-kot-P202-LEAD (ne-vplivajo-na-1876-števec!)",
    },
    "kaskada": {
        "vitals": "1355 → 1375 (+20-blokov-04106-1876!)",
        "04106": "136 → 156 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882 + 19×-1881 + 13×-1880 + 9×-1879 + 23×-1878 + 8×-1877 + 20×-1876!)",
        "04894": "520-NESPREMENJENO",
        "p80": "94-NESPREMENJENO",
        "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-REGENERIRANA (156/1375!)",
        "yearset": "+ 1876 (vse-04106-leta-zdaj-{1876,...,1885})",
        "izjeme": "h53/h12/h18-krstni-izjeme-RAZŠIRJENE-na-1876 (PEZDIRE + DRAGOŠ + ŠIMEC-1876-dokazi!)",
        "qa": "qa-p201-blok (201. kontrola!) + kaskada-v-qa-p199/p200-blokih",
    },
    "lead": {
        "P202": "mrliška 04106, leto 1875 (11/29!) — SIDRA: s134-TAIL-×4 (Dez-1875: z1-Primostek-21-Mathias-MUC-34J-14/16 + z2-Dobravce-3-Anton-PAPIZ[?]-44J-22/23 + z3-Krivoglavce-30-Martin-HÜGELJ[?]-18-dni-22/24 + z4-GRIBLJE-11-Catharina-KUNIĆ[~Kuniz?]-geb.-Jakoš-65J-Asthma-24/26!) + s133-ŽE-PREBRAN-ta-seja (Nov–Dez-1875-×11: '1875'-glava-violetna-z1 + November@z3 + Dezember@z11!) → probe: s126–s134; 1875-začetek = išče-nazaj (≈89-?-vpisov-po-povprečju); krstna-04104 + poročna-04455-čakata!",
        "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
        "poročna": "04455-začetek-1873–1885-čaka",
    },
    "entries": entries,
    "tail_1875": tail_1875,
    "notes": [
        "P201-recept = P200-recept (fetch-md5 + VLM + KROP + entries + insert + sanitize + verifier + runQA + deploy).",
        "md5-verige: P197→P198→P199→P200→P201 (s142-svež == P200-disk-1:1 — 5.×!).",
        "VLM-page-s142-'Dezember' = FALSIFICIRAN (KROP-'November.') — lekcija-#19: mesec-glava-MORA-bit-KROP-preverjena-ob-vsakih-'tail'-trditvah!",
        "P200-lead-'Dez-1876-×10-Griblje-×3' → POPRAVEK: November-×10-Griblje-×3 (vpisi-isti, mesec-popravljen!).",
    ],
}

out = "/home/z/my-project/muzej-backup/research/issue17/parish-death-1876-04106.json"
json.dump(proof, open(out, "w"), ensure_ascii=False, indent=1)
print(f"OK → {out}")
print(f"entries: {len(entries)} | griblje: {len(griblje)} | otroci: {len(otroci)}/20 | hiše: {proof['statistika']['hise']}")
