#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P202 — build proof research/issue17/parish-death-1875-04106.json (recept P200/P201)."""
import json

E = json.load(open("/tmp/p202/entries_1875.json"))
entries = E["entries"]
tail_1874 = E["tail_1874"]
griblje = [e for e in entries if e["vas"] and "gribl" in e["vas"].lower()]

def g(zap):
    for e in griblje:
        if e["zap"] == zap:
            return e
    raise KeyError(zap)

mesi = {}
for e in entries:
    m = "December" if e["mesec"] in ("Dezember", "December") else e["mesec"]
    mesi[m] = mesi.get(m, 0) + 1

# otroci: jasni < 10 let (z11-2-Mes + z31-4½-Mon + z40-5-Tednov); z17/z18 = '24'-enota-[?]-leta/tednov-NEJASNA!
OTROŠKE_JASNE = ["11", "31", "40"]
OTROŠKE_MEJNE = ["17", "18"]  # '24 7/8' + '24' — enota-[?]!
otroci = [e for e in griblje if e["zap"] in OTROŠKE_JASNE]

proof = {
    "faza": "P202",
    "tema": "mrliška PREDZGODOVINA 04106, leto 1875 = 11. leto PREDZGODOVINSKE LINIJE (issue #18)",
    "knjiga": "Matricula-online.eu — Slovenia, Ljubljana, Podzemelj — 04106 (Sterb-Buch 1857–1885)",
    "okvir": {
        "leto_1875": "s127-z11–s134-z4 == Pag. 121–128 (pag == sken − 6!); 71 vpisov (z1–z71, ŠTEVJE-IZ-VRSTIC — ordinali-NEVIDNI-na-vseh-8-straneh! recept-s148-4.×!) / 10 Griblje / 10 hiš (★★★ 5-NOVIH: h11 + h35 + h45 + h59 + h72! + 5-že-videnih: h5-1875→1880/85-nazaj + h17 + h22 + h31 + h69!) / März-15-MAX + Juli-1-MIN!",
        "meja_1874_75": "★★★ s127 (pag 121): TAIL-10-NOV/DEZ-1874-nad (z1–z10: November-×5 + Dezember-×5! 2-GRIBLJE: r1-Katharina-Krič[?] + r4-Mathias-Miler[?]!) + ★★★ 'Jänner 1875'-GLAVA-V-Z11-DATUMSKI-CELICI (42.-POTRDITEV-invariante! glava-z-letom!) + restart + ★ z1-ULEDBA-vzorec (smrt-31.-Dez-1874 + pokop-2.-Jänner-1875 — pokop-v-novem-letu! Michael-Plam[?]-Certovišče-44J!)",
        "meja_1875_76": "s134 (P201-REUSE + TA-SEJA-1:1-MD5): TAIL-4-DEZ-1875-nad (z68–z71: 14/16 + 22/23 + 22/24 + 24/26!) + VELIKA-'1876 Jänner'-glava-V-SREDINI ('Jahr'-beseda!) — ★★★ POPOLNA-SOGLASJA-Z-P201 (z71-Kunić-h11-65J-Dez-24/26 = P201-lead-'z4-h11-KUNIĆ'!) — P201-lead-preliminarni-'×11'-s133 → FINAL-×10 (Oct-tail-z58-ločen!)",
        "konec_1875": "z71 = s134-r4 (Dez-24/26 — Catharina-KUNIĆ-h11-65J!) — leto-konča-z-DEZEMBERJEM (za-razliko-od-1876-konca-z-NOVEMBERJEM!)",
        "zaporedna": "ordinali-NEVIDNI-na-vseh-8-straneh (s127–s134 — 'starejši-format-brez-stolpca'!) → ŠTEVJE-IZ-VRSTIC-4.× (recept-s148!); zap-z1–z71 = REKONSTRUIRAN",
        "forma": "tiskane-glave-Sterb-Buch + ročni-meseci; ★★★ GLAVE-V-DATUMSKI-CELICAH-×6: 42.-POTRDITEV-s127-z11-'Jänner 1875' (z-letom!) + 43.-POTRDITEV-s128-z6-'März' + 44.-POTRDITEV-s133-z1-'1875' (KROP-eksplicitno! violetna-tinta!) + mesečne-podpore: Juli-s131-z6 + November-s133-z2 + Dezember-s133-z10!",
        "skeni": "s126–s134 (pag 120–128); s126 = 1874-kontekst; s134-md5-križna-validacija-ta-seja: svež == P201-disk-1:1 (b89f2492790337532e89833a46163f6c) — VERIGA-P197→P198→P199→P200→P201→P202-6.×!",
        "preštevanje": "vrstna-aritmetika 1+11+10+13+12+10+10+4 = 71 ✓ (s127:1-samo-z1!); meseci: Jänner-3 + Feber-3 ('Feber'-grafa!) + März-15-MAX + April-7 + Mai-6 + Juni-6 + Juli-1-MIN + August-6 + September-6 + October-4(+1-tail) + November-8 + Dezember-5 = 71 ✓!",
    },
    "statistika": {
        "vpisov_1875": 71,
        "griblje": len(griblje),
        "hise": sorted({str(e["hisna"]).rstrip(".").split()[0] for e in griblje}, key=lambda x: int(x)),
        "nove_hise": "h11 + h35 + h45 + h59 + h72 (5 NOVIH!) — h5/h17/h22/h31/h69-niti-RAZŠIRJENE-NAZAJ-v-1875!",
        "otrok_griblje": f"{len(otroci)}/10 jasna = 30% (+2-[?]-mejna: z17-'24 7/8' + z18-'24' — enota-leta/tednov-NEJASNA-×2! če-tednov → 50%!)",
        "march_peak": "März-15-MAX (21%-leta-v-1-mesecu! Griblje-×4-v-Märzu: z9 + z11 + z17 + z18!) + Juli-1-MIN (edini-mesec-z-1-vpisom-v-korpusu-1870s!)",
        "december": 5,
        "duhovniki": "★★★ KOGEJ-NIT-'provinciat'-RANK-1875 (Hogeyu/Kooci/Bogija-Coop.-×~10!) + DOVGAN-DOMINANTA-×23 (Dovgan-7 + Dorgai-6 + Dorgam-3 + franzy-Dorgan-3 + Lovšar-[Dovgan?]-4!) + HOZJAN-VARIANTE-×14 (Hoger-6 + Hozjan-5 + Hočevar-3 — ena-oseba-[?]!) + Jostinmaut-Rogelj-×6 + Jožef-Vogrin-×5",
    },
    "anomalije": [
        "★★★ MEJA-1874/75-s127: TAIL-10-NOV/DEZ-1874-nad + 'Jänner 1875'-glava-v-z11-celici (42.-POTRDITEV!) + z1-ULEDBA (31-Dez-1874-smrt → 2-Jän-1875-pokop!) — 1.-LETA-MEJA-z-10-tail-vrsticami-v-korpusu (P201-je-imel-×4!)",
        "★★★ KOGEJ-NIT-'provinciat'-RANK (z17-s129: 'provinciat Hogeyu Coop.' + z18: 'provinciat Kooci Coop.' — EKSPLICITNO-'Kooci'-grafia!) — KOGEJ-OBDOBJE-RAZŠIRJENO-NAZAJ-3.-× (1877-Jän→Mai → 1876-Feb→Nov → 1875-'provinciat'-rank!) + 'Feldkurat-Bogija-Corp.'-×5-grafia (z59 + 4-druge!)",
        "★★★ DOVGAN-DOMINANTA-1875-×23-izpisov (7-Dovgan + 6-Dorgai + 3-Dorgam + 3-franzy-Dorgan + 4-Lovšar-[Dovgan?]) — NAJVEČJA-DOVGAN-LETNICA-v-korpusu-doslej (cf. P201-×3 + P200-dominanta!)",
        "★★★ PEZDIR-GRAFIA-DUEL-#1-1875 (z9-s128-h59: 'Georg-Peglinc[?Bezdira?]' — KROP-'G-e-o-r-g-P-e-g/d-linc' — 'Peglinc'-vs-'Bezdira'-[?]!) — NIT-kontekst: PEZDINC-h53-1876/77 (P201-z22 + P200-z51) → h59-nov-PEZDIR-kandidat-[?]!",
        "★★★ KROP-FALSIFIKACIJA-VLM-#9 (z27-s130-h35: VLM-'Matthea-Klemencic-43J'-ŽENSKO-ime → KROP-'Miha-Nemanič-gründbm'-MOŠKO-ime-potrjeno! '14./16.-Griblje-35.-Miha-Nemanič'!)",
        "★★★ GEORG-HUSIČ-DUEL-s133 (z58-Gradac-37J-Okt-26/28 + z59-GRIBLJE-h69-27J-Nov-26/28 — ISTA-imena + ISTI-dnevi-26/28-mesec-dan-RAZLIČEN! 2-ločeni-vpisa-KROP-potrjena — [~]-dvojnost-dokumentirana! h69-Griblje → 1882/1884-nit-RAZŠIRJENA-NAZAJ!)",
        "★★★ BRAUŠ-NIT-1875-×2 (z11-h45: 'Sohn-der-Anna-Braußsche' + z40-h72: 'Sohn-des-Marcus-Brauše' — 2-matere/oca-BRAUŠ-v-1-letu! z40-KURRENT-2/3-DUEL-RAZREŠEN: h72-NE-h73!)",
        "★★★ '1875'-GLAVA-VIOLETNA-TINTA (z58-s133-z1-KROP — P201-lead-napoved-potrjena!) + 44.-POTRDITEV-invariante-KROP-eksplicitno!",
        "★ z17/z18-'24'-ENOTA-ZMEDA (z17-h31-Maria-Kambič-'24 7/8'-VLM-'24-tj.'-FALSIFICIRAN-KROP-'24 7/8' — enota-leta/tednov-NEJASNA + z18-h17-Anna-Kraus-'24'[?] + '¾ J.'-glif-v-imenskem-stolpcu — ure/leta-[?]!) — oba-März-21-smrt + pokop-23 — isti-datumi!",
        "★ ZIMSKI-KLASTER-GRIBLJE-MÄRZ-×4 (z9-40J-Asthma + z11-2-Mes + z17 + z18 — 4-od-10-Griblje-v-Märzu!)",
        "★ FRISEN-NIT-1875-×2 (z40-h72-'Frisen'[~] + z59-h69-'Frais-en/Schlagfluß'[?] — cf. P201-KERBICA-FRISEN-×2-1876!)",
        "★ Wassersucht-[?]-z11-h45 (dojenček-2-Mes — cf. h53-WASSERSUCHT-nit-1877/78!) + Juli-1-MIN (Juli-1875 = skoraj-mrtvi-mesec!)",
        "★ 'Feber'-GRAFA-×3 (s128-z4/z5/z6 — krajšana-forma-'Feber'-namesto-'Februar' — 1.-pojav-te-grafe-v-korpusu-[?]!)",
        "★ z18-'¾ J.'-glif-V-IMENSKEM-STOLPCU (starost-podatek-v-napačnem-stolpcu — pisarjeva-napaka-[?]!)",
    ],
    "duhovniki": {
        "KOGEJ-NIT-1875-PROVINCIAT": "provinciat-Hogeyu-Coop.-z17 + provinciat-Kooci-Coop.-z18 + Feldkurat-Bogija-Corp.-×5 (z59 + s133/s134!) — KOGEJ-OBDOBJE-NOW-1875→1877 (3-leta-neprekinjeno! rank-'provinciat' = nov-podatek!)",
        "DOVGAN-×23": "Dovgan/Dorgai/Dorgam/franzy-Dorgan/Lovšar-[Dovgan?] — NAJVEČJA-letnica (23-izpisov!) — cf. P200-dominanta-1877 + P201-×3-1876",
        "HOZJAN-VARIANTE-×14": "Ferdinand-Hoger-×6 + Ferdinand-Hozjan-×5 + Ferdinand-Hočevar-×3 (z71! — ena-oseba-3-grafe-[?]-ali-3-osebe-[?]!) — ★HOZJAN-'Capp.'-1876-RAZŠIRJENO-NAZAJ-v-1875-kot-'Coop.'!",
        "ROGELJ-×6": "Jostinmaut-[?]-Rogelj-Coop.-×6 (s127-z11-'Jožefin[?]-Rogelj'-prvi!) — ROGELJ-nit-nov-[?]",
        "VOGRIN-×5": "Jožef-Vogrin[?]-Coop.-×5 (z54-Griblje!)",
    },
    "hišne_kontinuitete": {
        "h11": "NOVA-hiša-1875 (z71-Catharina-KUNIĆ[~Kuniz?]-geb.-JAKOŠ-65J-vdova-Asthma-Dez-24/26!) — KUNIĆ/JAKOŠ-nit-1.-dokaz! (P201-lead-napoved-1:1!)",
        "h35": "NOVA-hiša-1875 (z27-Miha-NEMANIČ-43J-Typhus-Apr-14/16! KROP-FALSIFIKACIJA-VLM-#9!)",
        "h45": "NOVA-hiša-1875 (z11-Mathias-Riünzflißler[?Rinzbissler?]-2-Mes-sohn-der-Anna-Braußsche!) — BRAUŠ-mama!",
        "h59": "NOVA-hiša-1875 (z9-Georg-PEGLINC[?Bezdira?]-40J-Asthma-März-6/8!) — PEZDIR-GRAFIA-DUEL-#1!",
        "h72": "NOVA-hiša-1875 (z40-Joannes-BRAUŠ-5-Tednov-Juni-19/20! KURRENT-DUEL-RAZREŠEN-h72!)",
        "h5": "RAZŠIRJENA-NAZAJ (1875-z54-Joanes-ŠTUZEL[?Sturzel]-34J-¼-Gübler-Okt-2/4 → 1880 + 1885!) — 10-letna-nit!",
        "h17": "RAZŠIRJENA-NAZAJ (1875-z18-Anna-KRAUS-24[?]-März-21/23 → 1881 + 1884!)",
        "h22": "RAZŠIRJENA-NAZAJ (1875-z31-Maria-MIHEL[?]-4½-Mon-Mai-13/15 → 1880!)",
        "h31": "RAZŠIRJENA-NAZAJ (1875-z17-Maria-KAMBIČ-Kurpašnič[?]-24 7/8[?]-März-21/23 → 1881 + 1885!)",
        "h69": "RAZŠIRJENA-NAZAJ (1875-z59-Georg-HUSIC-27J-Nov-26/28 → 1882 + 1884!) — 9-letna-nit + GEORG-HUSIČ-DUEL!",
    },
    "forme": [
        "'Jänner 1875'-MEJA-GLAVA-V-Z11-CELICI-s127 (42.-POTRDITEV — glava-z-letom-v-celici-1.-×-od-1877-'18 77.'-odrezane!)",
        "'März'-glava-V-Z6-CELICI-s128 (43.-POTRDITEV!)",
        "'1875'-glava-V-Z1-CELICI-s133 (44.-POTRDITEV — KROP-eksplicitno! VIOLETNA-TINTA! November-blok-opener!)",
        "mesečne-glave-v-celicah-podpore: Juli-s131-z6 + November-s133-z2 + Dezember-s133-z10 (6-glav-v-celicah-skupaj-1875 = korpus-REKORD-×6!)",
        "'Feber'-krajšana-grafa-×3 (s128!)",
        "ordinali-NEVIDNI-×8 (s127–s134!) → ŠTEVJE-IZ-VRSTIC-4.×",
        "TAIL-10-NOV/DEZ-1874-s127 (NAJVEČJI-tail-v-korpusu! 2-Griblje!)",
        "TAIL-4-DEZ-1875-s134 (P201-1:1-konzistentno!)",
    ],
    "crossChecks": [
        "md5-križna-validacija: s134-svež == P201-disk-1:1 (b89f2492790337532e89833a46163f6c) — VERIGA-P197→…→P202-6.×!",
        "vrstna-aritmetika: 1+11+10+13+12+10+10+4 = 71 ✓ (z1–z71!)",
        "meseci-vsota: 3+3+15+7+6+6+1+6+6+4+8+5 = 71 ✓",
        "s134-tail-×4-P201-1:1: z68-14/16 + z69-22/23 + z70-22/24 + z71-24/26 == P201-'TAIL-4-DEZ-1875'-točno ✓ (datumi-vrstni-red-hiše!)",
        "z71-KUNIĆ-h11 == P201-lead-'z4-h11-Catharina-KUNIĆ[~Kuniz?]-geb.-Jakoš-65J-Asthma-24/26' — 1:1 ✓",
        "s133-glava-'1875'-violetna == P201-lead-napoved ✓ (KROP-ta-seja-potrjeno!)",
        "P201-lead-'s133-×11' → FINAL-×10 (Oct-tail-z58-ločen — 1.-popravek-preliminarnega-branja!)",
        "h69/h5/h17/h22/h31-niti-vs-04106-bloki-1879–1885 (h69-1882/84 + h5-1880/85 + h17-1881/84 + h22-1880 + h31-1881/85) ✓",
        "z40-h72-KURRENT-DUEL (h73-[?]-VLM-vs-h72-KROP-'Griblje 72.'-2/3-soglasje!) ✓",
        "z27-KROP-FALSIFIKACIJA-×2-branja ('Miha-Nemanič'-moško — VLM-'Matthea-Klemencic'-žensko-ZAVRŽENO!) ✓",
    ],
    "honesty": {
        "H1": "ordinali-NEVIDNI-×8 → zap-z1–z71 = REKONSTRUIRAN (ŠTEVJE-IZ-VRSTIC-4.× — brez-ločenih-konfirmacij!)",
        "H2": "z17-'24 7/8' + z18-'24'-ENOTA-NEJASNA (leta/tednov!) — otroška-umrljivost-30%-do-50%-obseg — dokazano-kot-[?]",
        "H3": "GEORG-HUSIČ-DUEL-z58/z59 (ista-imena + isti-dnevi-26/28!) — KROP-2-ločeni-vpisa, a-dvojnost-podvig-v-[~] (VLM-dupliciranje-mogoče!)",
        "H4": "z9-'Peglinc[?Bezdira?]'-PEZDIR-DUEL — [?] — grafia-ne-razrešena",
        "H5": "z11-'Riünzflißler[?Rinzbissler?]' — [?] — grafia-ne-razrešena",
        "H6": "z17-'Brüzframenghfak][?' + z18-'Blattronn[?Blatkronn' — bolezni-kriptični-[?]",
        "H7": "z18-'¾ J.'-glif-v-imeni-stolpcu — starost-v-napačnem-stolpcu-[?]",
        "H8": "duhovniki-grafije: Hogeyu/Kooci/Bogija = KOGEJ-substituendus (interpretacija — 'provinciat'-rank-zanesljiv!); Hoger/Hozjan/Hočevar = 1-ali-3-osebe-[?]",
        "H9": "s126 (1874-kontekst) ni-v-celoti-analiziran-ta-seja — P203-LEAD",
        "H10": "tail_1874-×10: 5-Nov + 5-Dez-1874 — imena-delno-[?] (Krič[?]/Miler[?]/Fazilič[?]/Zahlič[?]...) — P203-LEAD-dokumentiran-kot-surov",
        "H11": "Feber-'grafa-1.-pojav' — trditev-limited-na-04106-korpus (druge-knjige-ne-preverjene!)",
        "H12": "z59-'Frais-en/Schlagfluß[?]' — bolezen-[?] (FRISEN-nit-[~])",
        "H13": "meseci-per-vrstico = VLM-labeli + KROP-korekcije ('[prej-October]'-z58!) — vsota-71-je-robu-stabilna!",
        "H14": "otroška-umrljivost-klasifikacija: 3-jasni (< 1-leta) + 2-mejni-'24'[?]-zmeda — mejni-dokumentirani",
        "H15": "42./43.-invariantna-številčenje = rekonstruirano-zaporedje-glav-v-celicah (44.-KROP-eksplicitno-zanesljivo!)",
        "H16": "tail_1874-×10: dokumentirane-kot-P203-LEAD (ne-vplivajo-na-1875-števec!)",
    },
    "kaskada": {
        "vitals": "1375 → 1385 (+10-blokov-04106-1875!)",
        "04106": "156 → 166 (16×-1885 + 21×-1884 + 11×-1883 + 16×-1882 + 19×-1881 + 13×-1880 + 9×-1879 + 23×-1878 + 8×-1877 + 20×-1876 + 10×-1875!)",
        "04894": "520-NESPREMENJENO",
        "p80": "94-NESPREMENJENO",
        "korpus": "93-NESPREMENJEN",
        "pt_luknja": "18-REGENERIRANA (166/1385!)",
        "yearset": "+ 1875 (vse-04106-leta-zdaj-{1875,...,1885})",
        "qa": "qa-p202-blok (202. kontrola!) + kaskada-v-qa-p201-bloku",
    },
    "lead": {
        "P203": "mrliška 04106, leto 1874 (12/29!) — SIDRA: s127-TAIL-×10 (Nov-×5 + Dez-×5-1874! 2-GRIBLJE: r1-Katharina-Krič[?]-Griblje + r4-Mathias-Miler[?]-Griblje!) + s126-ŽE-FETCHAN-ta-seja (1874-kontekst!) → probe: s118–s127; 1874-začetek = išče-nazaj (≈71-90-vpisov-po-povprečju); krstna-04104 + poročna-04455-čakata!",
        "krstna": "04104-1871–1885-×200-skenov-čaka (vzporedno!)",
        "poročna": "04455-začetek-1873–1885-čaka",
    },
    "entries": entries,
    "tail_1874": tail_1874,
    "notes": [
        "P202-recept = P200/P201-recept (fetch-md5 + VLM + KROP + entries + insert + sanitize + verifier + runQA + deploy).",
        "md5-verige: P197→P198→P199→P200→P201→P202 (s134-svež == P201-disk-1:1 — 6.×!).",
        "Griblje-10/71 = 14.1% — NAJNIŽJI-Griblje-delež-od-1878 (23/89-1878? ne — 04106-1875-10/71 — cf. 1876-20/89-22.5% + 1877-8/60-13.3%!).",
        "5-NOVIH-hiš-v-1-letu (h11/h35/h45/h59/h72) = korpus-REKORD-1870s! (P201-1876-je-imel-19-hiš-ampak-večino-že-videnih!)",
    ],
}

out = "/home/z/my-project/research/issue17/parish-death-1875-04106.json"
json.dump(proof, open(out, "w"), ensure_ascii=False, indent=1)
print(f"OK → {out}")
print(f"entries: {len(entries)} | griblje: {len(griblje)} | otroci-jasni: {len(otroci)}/10 | hiše: {proof['statistika']['hise']}")
