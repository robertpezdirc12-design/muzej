#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P248-restore: ponovna vstavitev P248-sekcije v parish.ts (po git-checkout revert-u)."""
F = "/home/z/my-project/src/data/atlas/parish.ts"
s = open(F, encoding="utf-8").read()
if "P248: POROČNA PREDZGOVINA" in s:
    print("ŽE vstavljeno — preskočim"); raise SystemExit

ANCHOR = '''    whatEn: "marriage Dec 28, 1877 [~'Desinc'-garble-DUEL!-OUT-OF-CHRONOLOGY-after-entry-17!-'d.-19-Jänner-1878'-annotation] (entry 16-corrected-from-15!, s18, margin-'15'-CROSSED-→-'16'-RE-NUMBERING!) — groom Nicholaus Terdić [~T/S-DUEL!], 51 y. [~29-DUEL!], 'Pfarrer-v.-Cernomelj' 13 [~X-OPEN!] × bride Katharina Allešič [~Ažetič-DUEL!], 40 y., GRIBLJE 69 (3×-reads-1:1!)-annotation-'widow-of/rel.-BRINC'!; + ★★★ BRIDE-BLOCK + ★★★ h69-firstYear-DVIG-1887→1877-BY-10-YEARS + ★ BRINC-NETWORK-proof-in-1877 (cf.-h24-1880-+ h21-1879!)",
    status: "DOCUMENTED" as const,
  },
  {'''

INSERT = ANCHOR.replace("  },\n  {", """  },
  // ——— P248: POROČNA PREDZGOVINA 04455, leto 1876 = 10/13 — (s11–s14; md5-7/7-s8–s14!-s14-3×-neodvisen-1:1!-Read-očesa-NAJPREJ-×7-P244-LEKCIJA!-+ VLM-pass-1-×4 + pass-2-ultra-×12 + pass-3-mikro-×24 + pass-4-×11 + letterform-forenzika-'f'/'O'/'8-vs-2'/'š-háček'/'6-vs-4'!); ★★★ RESTART-1876 = s11-VRSTA-2 (druga-vrsta!-marginalna-'1'-FIZIČNO-1:1!-vpis-1 = 'de.-fbruar-9'-BREZ-letnice!-mesec-mikro-forenzika-'f'-ena-zanka+spodnja-zanka-NI-J!-vpis-1 = h31-Krupanič-[~Zupanič-DUEL!]-34-l-×-h44-PEGDIRE-20-l-INTRA-DVOJNI!-zettel-'woher-Güblje-dd.-8.-Februar-1876'-1:1!-sreda-ritem-9/16/23!) + ★★★ TAIL-1875 = s11-top-VPIS-8-VIOLET-NAKNADNI-VPIS (marginalna-'8'-fizično-ENA-številka!-vijolično-črnilo!-podpis-KAPLAN-Daniel-Perschek-[~Fošbek!]-≠-DOVGAN!-datum-'1875'+'3.'-mesec-MAREC~AUGUST-DUEL-zettel-'3.-VIII'-podpora-August!-opomba-'Privat'!-→-NAPAVED-P249-preskok-8!-NAKNADNO-DOPISAN-ČEZ-MEJO!) = 10.-MEJNA-VARIANTA (meja-NA-ISTI-STRANI-+ naknadni-vmes-+ restart-brez-letnice-+ INLINE-od-2.-lista-s12-m6-'1876.-Febr.-16.'-+ s13-m10-'1876.-Februar-23.'-+ s14-m14-'1876.-Novembris-15.'!) · MEJA-1875/76 = s10→s11 (tail-1875-REGULARNO = s10-vpis-17-'Juli-20'!-margine-13–17!) · MEJA-1876/77 = s14→s15 (P247-1:1!-finis-1876-3.-instance-re-verifikacija-1:1!) · 15-VPISOV-BREZ-PRESKOKOV-7.-LETO (s11-1–5 · s12-6–9-margina-'8'-'2'-glif-RAZREŠEN!-s13-10–13 · s14-14–15!) · ★★★★★ FOLIACIJA-'Pag-=-sken−1'-4/4-1876 (s11-'Pag. 10'-+ s12-'Pag. 11'-pass-1-'4'-MISREAD-KOREKCIJA!-+ s13-'Pag. 12'-+ s14-'Pag. 13'!) = 19/19-V-ZAPOREDNIH-LETIH-5.-LETO! — 6-GRIBLJE-blokov-6-DVIGOV-V-1-LETU-REKORD (h44-ZA-23-LET-NOV-ABSOLUTNI-REKORD!-h30-ZA-13!-h64-ZA-12!-h31-ZA-10!-h35-ZA-6!-h41-ZA-5!): h31-v1-ŽENIN-INTRA-×-h44 + h44-v1-NEVESTA-REKORD-DVIG!-+ h35-v8-ŽENIN-INTRA-×-h64-P229-z79-'Mathias-Hrižan'-PARALELA!-+ h64-v8-NEVESTA-NOVA-04455!-+ h41-v13-NEVESTA-'Leinmannstochter'!-+ h30-v14-NEVESTA-'Leinmannstochter'! + ★★★★★ PEZDIRC/PEGDIRE-×9-omemb-V-1-LETU-REKORD (×4-BLOKOV!-'Leinmannstochter'-×2!-2×-Georg-Pegdire-oče!-PEGDIRE-LEINWEBER-DRUŽINA-kandidat!) + INTRA-DVOJNI-×2-+ IZMENA-VLOG-×2-(v3/v4-Pasič↔Movrin!-v6/v7-Štefanič-Dobranice-8!-cf.-P241!) + DISPENS-3.-GRAD-1:1-v7-(dd.-12.-+15.-Febr.-dve!-25-vs-40!) + MLADOLETNICA-×2-(v10-17-l-Vormund-Consens!-v13-'PRO-DIE-MINDERJ.-BRAUT'!) + v14-TYPHUS-+ k.k.-Bez.Gericht-Metlika! + DOVGAN-CONTINUUM-10-LET (1876–1885!-začenja-z-restartom!-kaplan-Perschek-zadnji-1875!) ———
  {
    houseNo: "31",
    bookSignature: "04455",
    year: 1876,
    scan: 11,
    page: 10,
    whatSi: "poroka 9. Februar 1876 [~letnica-MANJKA-v-datumu-INLINE-vzorec-prekinjen-na-restartu!-mesec-mikro-forenzika-'f'-1:1!] (vpis 1 = RESTART-1876, s11-VRSTA-2, margina-'1'-FIZIČNO!) — ženin Nicolaus Krupanič [~Zupanič/Grupanič-K-DUEL-3-branja!-pripis-'ž-Gültner/Wirth'[~X-OPEN!]-cf.-P247-v6-Županič-DUEL-paralela!], 34 let, GRIBLJE 31 ('Gri. šte. 31'-strip-1:1!) × nevesta Katharina Pegdire [~Pozdire-DUEL!], 20 let, GRIBLJE 44 ('Gri. šte. 44'-1:1!); starši ženina: Matthias Krupanič × Katharina roj. Lavrič [~'Lavričin'-DUEL!-X-OPEN]; starši neveste: Georg [Starasinič~Pegdire-DUEL!] × Maria [Bohorič~Starasinič-DUEL!-X-OPEN] + pripis-Nicolaus-Bahorič[~]; priče: Nicolaus Bahorič [~Bahovič!] × Nicolaus [?]; duhovnik Georg Dovgan; Befunde: 'Communalzettel/Gemeinezettel von Gemeinde woher Güblje dd. 8. Februar 1876' (mikro-1:1!-permit-dan-pred-poroko!); + ★★★ ŽENIN-BLOK-INTRA-DVOJNI (h31×h44!-RESTART-že-v-vpisu-1!) + ★★★ h31-firstYear-04455-DVIG-1886→1876-ZA-10-LET (cf.-h53-DVIG-P243!-h10-h69-P247!) + ŽUPANIČ-veja-h31-kontinuiteta (cf.-P247-'cf.-h31-1876-ŽUPANIČ'-napoved-IZPOLNJENA!)",
    whatEn: "marriage Feb 9, 1876 [~year-MISSING-in-date!-month-mikro-forensics-'f'-1:1!] (entry 1 = RESTART-1876, s11-ROW-2, margin-'1'-PHYSICALLY!) — groom Nicolaus Krupanič [~3-way-DUEL!], 34 y., GRIBLJE 31 (1:1!) × bride Katharina Pegdire [~DUEL!], 20 y., GRIBLJE 44 (1:1!); groom's parents: Matthias Krupanič × Katharina née Lavrič [~X-OPEN]; bride's parents: Georg [DUEL!] × Maria [DUEL!-X-OPEN]; witnesses: Nicolaus Bahorič[~] × Nicolaus [?]; priest Georg Dovgan; Befunde: 'Communalzettel von Gemeinde woher Güblje dd. 8. Februar 1876' (mikro-1:1!); + ★★★ GROOM-BLOCK-INTRA-DOUBLE (h31×h44!-RESTART-already-in-entry-1!) + ★★★ h31-firstYear-DVIG-1886→1876-BY-10-YEARS!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "44",
    bookSignature: "04455",
    year: 1876,
    scan: 11,
    page: 10,
    whatSi: "poroka 9. Februar 1876 (vpis 1, s11, margina-'1') — NEVESTA Katharina Pegdire [~Pozdire-DUEL!], 20 let, GRIBLJE 44 ('Gri. šte. 44'-strip-1:1!) × ženin Nicolaus Krupanič GRIBLJE 31; + ★★★★★ NEVESTA-BLOK-INTRA-DVOJNI + ★★★★★ h44-firstYear-04455-DVIG-1899→1876-ZA-23-LET = NOV-ABSOLUTNI-REKORD-DVIG-LINIJE (prejšnji-rekord-h53-10-let-P243!-h10-h69-10-let-P247!-h44-04455-leta-do-zdaj: 1899/1903/1905/1908/1912!) + PEZDIRC-×1-od-×9-v-1-letu (cf.-h44-korpus-PEZDIRC-veja!)",
    whatEn: "marriage Feb 9, 1876 (entry 1, s11) — BRIDE Katharina Pegdire [~DUEL!], 20 y., GRIBLJE 44 (1:1!) × groom Nicolaus Krupanič GRIBLJE 31; + ★★★★★ BRIDE-BLOCK-INTRA-DOUBLE + ★★★★★ h44-firstYear-DVIG-1899→1876-BY-23-YEARS = THE-NEW-ABSOLUTE-RECORD-OF-THE-LINE (the-previous-record-h53-10-years-P243!) + PEZDIRC-×1-of-×9-in-1-year!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "35",
    bookSignature: "04455",
    year: 1876,
    scan: 12,
    page: 11,
    whatSi: "poroka 16. Februar 1876 [~] (vpis 8, s12, margina-'8'-FIZIČNO-1:1-dvojni-lok!-'2'-glif-full-page-MISREAD-RAZREŠEN!) — ženin Mathias Hrižan [~Križan-H-forma-DUEL-P246-K-vs-H-lekcija!], 22 let [~20-DUEL-mikro-2:1!], Inwohner [~Leinann-DUEL-X-OPEN!], GRIBLJE 35 ('Gri. šte. 35'-mikro-visoka-zanesljivost!) × nevesta Anna Požeh [~Pozeh!], 19 let, GRIBLJE 64 ('Gri. šte. 64'-mikro-forenzika-6=spodnja-zanka-+'4'=h-droga-75%!-NOVA-HIŠA-V-04455!); starši ženina: Nicolaus Hrižan 'vulgo-Khrižem' [~Krasch-garble!] × Maria roj. [Gilah~Pozeh-DUEL-X-OPEN!]; starši neveste: Mathias POŽEH (mikro-1:1-ime-continuum!) × Maria roj. PEGDIRE (mikro-1:1-PEZDIRC!-p2-swap-X-OPEN!); priče: Georg [Simer~Hrižen-DUEL!] × Martin Krasovec [~]; duhovnik Georg Dovgan; Befunde: 'Gemeinezettel-Griblje-dd.-15.-Februar-1876'-+ Dispens-dd.-15.-Febr.-876-+ VOJAŠKA-omemba-'zum-k.k.-[enota]'-[X-OPEN!]-+ Črnomelj-robno!; + ★★★ ŽENIN-BLOK-INTRA-DVOJNI (h35×h64!) + ★★★ h35-firstYear-04455-DVIG-1882→1876-ZA-6-LET + ★★★ h35-PARALELA-1:1: 'Mathias-Hrižan'-h35 == P229-z79-krst-04104-'Mathias-Hrižan'-h35 (ISTO-IME+ISTO-HIŠA!-oče-sin-ISTO-IME-kandidat-X-OPEN!-cf.-P231-z111-Kelcho-veriga!) + HRIŽAN-h35-veja-2.-leto-zapored-cf.-P246-v17-nevesta-1878!",
    whatEn: "marriage Feb 16, 1876 [~] (entry 8, s12, margin-'8'-PHYSICALLY-1:1!-'2'-glyph-MISREAD-RESOLVED!) — groom Mathias Hrižan [~H-forma-DUEL!], 22 y. [~20-DUEL-mikro-2:1!], GRIBLJE 35 (mikro-high!) × bride Anna Požeh, 19 y., GRIBLJE 64 (mikro-forensics-6=lower-loop-+'4'=h-stem-75%!-NEW-HOUSE-IN-04455!); groom's parents: Nicolaus Hrižan 'vulgo-Khrižem'[~] × Maria née [Gilah~Pozeh-DUEL-X-OPEN!]; bride's parents: Mathias POŽEH (mikro-1:1!) × Maria née PEGDIRE (mikro-1:1-PEZDIRC!); witnesses: Georg [DUEL!] × Martin Krasovec[~]; priest Georg Dovgan; Befunde: zettel-Griblje-dd.-15.-Feb-1876-+ Dispens-+ MILITARY-mention-'zum-k.k.-[unit]'-[X-OPEN!] + Črnomelj!; + ★★★ GROOM-BLOCK-INTRA-DOUBLE (h35×h64!) + ★★★ h35-firstYear-DVIG-1882→1876-BY-6-YEARS + ★★★ h35-PARALLEL-1:1: 'Mathias-Hrižan'-h35 == the-baptism-P229-z79-'Mathias-Hrižan'-h35 (SAME-NAME+SAME-HOUSE!)",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "64",
    bookSignature: "04455",
    year: 1876,
    scan: 12,
    page: 11,
    whatSi: "poroka 16. Februar 1876 (vpis 8, s12, margina-'8') — NEVESTA Anna Požeh, 19 let, GRIBLJE 64 ('Gri. šte. 64'-mikro-forenzika-75%!-'19'-mislotted-mikro-ZAVRŽEN-lokacijska-napaka!) × ženin Mathias Hrižan GRIBLJE 35; starši: Mathias POŽEH × Maria roj. PEGDIRE!; + ★★★★★ NEVESTA-BLOK-INTRA-DVOJNI-NOVA-HIŠA-V-04455-KORPUSU + ★★★★★ h64-firstYear-04455-DVIG-1888→1876-ZA-12-LET (h64-04455-leta-do-zdaj: 1888/1921!) + POŽEH-veja-h64-korpus-kontinuiteta (cf.-P244-v31-Požeh-h77-MILEK-križ!-P246-v7-Anna-MILEK-h65!) + PEZDIRC-mati-dokaz!",
    whatEn: "marriage Feb 16, 1876 (entry 8, s12) — BRIDE Anna Požeh, 19 y., GRIBLJE 64 (mikro-forensics-75%!-the-'19'-mislotted-mikro-REJECTED-location-error!) × groom Mathias Hrižan GRIBLJE 35; parents: Mathias POŽEH × Maria née PEGDIRE!; + ★★★★★ BRIDE-BLOCK-INTRA-DOUBLE-THE-NEW-HOUSE-IN-THE-04455-CORPUS + ★★★★★ h64-firstYear-DVIG-1888→1876-BY-12-YEARS + the-POŽEH-branch-h64-continuity + the-PEZDIRC-mother-proof!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "41",
    bookSignature: "04455",
    year: 1876,
    scan: 13,
    page: 12,
    whatSi: "poroka 22. Oktober 1876 [★★★ datum-DUEL-pass-1-'October-22'-+mikro-forenzika-'O'-poudarjen-2:1-vs-'Sept-17'-očesa!-zettel-'dd.-16.-7ber'-(September)-5-tednov-prej-X-OPEN!] (vpis 13, s13, margina-'13') — ženin Nicolaus Simec, 22 let, 'Wsch 22' [~Wuchel-p2-DUEL!-'55'-PREČRTAN!-popravek-'z-Griblje'[~X-OPEN!]-NI-blok-pošteno!] × nevesta Maria PEGDIRE 'Leinmannstochter' (Leinweber-hči!), 20 let, GRIBLJE 41 ('Gri. šte. 41'-2×-branja-1:1!); starši neveste: Georg PEGDIRE-Bauer (3×-branja!-cf.-v9-ISTO-IME-oče!-2-ženi-kandidat-X-OPEN!) × Anna roj. BRINC (BRINC-MREŽA-5.-leto!); priče: Peter Mrh × Johann Mrh (2×-1:1!); duhovnik Georg Dovgan [pass-1-'Franc-Grgas'-MISREAD-KOREKCIJA-mikro-6×-1:1!]; Befunde: 'Gemeinezettel-zum-Gemeinderathe-Griblje-dd.-16.-[7~8]ber-876' (POPRAVEK-'ber'!)-+ Consens-vom-Landg.-Črnomelj-+'PRO-DIE-MINDERJ.-BRAUT'-MLADOLETNICA-izrecno!; + ★★★ NEVESTA-BLOK-'Leinmannstochter' + ★★★ h41-firstYear-04455-DVIG-1881→1876-ZA-5-LET + PEZDIRC-×2-(nevesta+oče!)-+ BRINC-družinska-vez (cf.-h24-1880!-h21-1879!-h69-1877-opomba!)",
    whatEn: "marriage Oct 22, 1876 [★★★ date-DUEL-2:1-vs-'Sept-17'!-zettel-'16.-7ber'-(Sep)-5-weeks-earlier-X-OPEN!] (entry 13, s13, margin-'13') — groom Nicolaus Simec, 22 y., 'Wsch 22' [~'55'-CROSSED!-correction-'z-Griblje'[~X-OPEN!]-NOT-a-block-fairly!] × bride Maria PEGDIRE 'Leinmannstochter' (linen-weaver's-daughter!), 20 y., GRIBLJE 41 (2×-reads-1:1!); bride's parents: Georg PEGDIRE (3×-reads!) × Anna née BRINC (the-BRINC-network-5th-year!); witnesses: Peter Mrh × Johann Mrh (2×-1:1!); priest Georg Dovgan [pass-1-'Franc-Grgas'-MISREAD-CORRECTED-mikro-6×-1:1!]; Befunde: zettel-Griblje-dd.-16.-[7~8]ber-876-+ Consens-vom-Landg.-Črnomelj-+'PRO-DIE-MINDERJ.-BRAUT'-MINOR-explicit!; + ★★★ BRIDE-BLOCK-'Leinmannstochter' + ★★★ h41-firstYear-DVIG-1881→1876-BY-5-YEARS + PEZDIRC-×2-+ the-BRINC-family-link!",
    status: "DOCUMENTED" as const,
  },
  {
    houseNo: "30",
    bookSignature: "04455",
    year: 1876,
    scan: 14,
    page: 13,
    whatSi: "poroka 15. Novembris 1876 ('Novem-ber-15'-margins-krop-1:1-očesa-'vor'-MISREAD-KOREKCIJA!-letnica-INLINE!) (vpis 14, s14, margina-'14'-P247-tail-kontekst-ZDAJ-blok!) — ženin Johann Jurgovič [~Jurgpovič/Jerejovič-DUEL!], 20 let, Mali Lipoglav 18 [pass-1+pass-4-2×-neodvisno-1:1-'Lipoglav'-struktura!-Wilsput-hint-ZAVRŽEN!-X-OPEN-kraj!] × nevesta Anna PEGDIRE 'Leinmannstochter' (Leinweber-hči!), 20 let, GRIBLJE 30 ('Griblje 30'-mikro-8×-visoka-+P247-tail-2×-neodvisno!); starši ženina: Michael Gurgpovič 'yat.-Pergbohte' [~geb.-garble-X-OPEN!] × Maria roj. Bertke [~]; starši neveste: Markus [Margon~Morzan~Berghoper-TRIPLE-DUEL!-X-OPEN] × Mathiewa roj. PEGDIRE (3×-branja!-PEZDIRC-mati!-cf.-h63-1880-Magdalena-hči-Marka-P243-PARALELA-Marek~Markus!); duhovnik Georg Dovgan [pass-1-'Dorgun'-garble!]; Befunde: 'Gemeinezettel-woher-Gemeinde-Amt-Griblje-dd.-11.-9br-(Novembris!)-1876'-+ TYPHUS-'da-fraglich-dt-Typh'-omemba!-+ zdravniški-30.-August-1876-[~X-OPEN!]-+ Consens-k.k.-Bez.Gericht-Metlika-'Mötthling'-garble-dd.-18.-9br-1876!; + ★★★ NEVESTA-BLOK-'Leinmannstochter' (P247-tail-kontekst-PROMOCIJA-v-blok!-PEZDIRC-napoved-IZPOLNJENA!) + ★★★ h30-firstYear-04455-DVIG-1889→1876-ZA-13-LET + PEZDIRC-×2-(nevesta+mati!)-+ TYPHUS+k.k.-sodišče-vzorec-(cf.-BRINC-1877-h69!)",
    whatEn: "marriage Nov 15, 1876 (entry 14, s14, margin-'14'-the-P247-tail-context-NOW-a-block!) — groom Johann Jurgovič [~DUEL!], 20 y., Mali Lipoglav 18 [2×-independent-1:1!-X-OPEN-village!] × bride Anna PEGDIRE 'Leinmannstochter', 20 y., GRIBLJE 30 (mikro-8×-high-+P247-tail-2×-independent!); groom's parents: Michael Gurgpovič 'yat.-Pergbohte'[~] × Maria née Bertke[~]; bride's parents: Markus [TRIPLE-DUEL!-X-OPEN] × Mathiewa née PEGDIRE (3×-reads!-the-PEZDIRC-mother!-cf.-h63-1880-P243-PARALLEL!); priest Georg Dovgan; Befunde: zettel-Griblje-dd.-11.-9br-(Novembris!)-1876-+ TYPHUS-mention!-+ medical-+ the-Consens-k.k.-Bez.Gericht-Metlika-dd.-18.-9br-1876!; + ★★★ BRIDE-BLOCK-'Leinmannstochter' (the-P247-tail-context-PROMOTION-to-a-block!-the-PEZDIRC-forecast-FULFILLED!) + ★★★ h30-firstYear-DVIG-1889→1876-BY-13-YEARS + PEZDIRC-×2-+ TYPHUS+the-court-pattern!",
    status: "DOCUMENTED" as const,
  },
  {""")

assert s.count(ANCHOR) == 1, f"anchor najden {s.count(ANCHOR)}×"
s = s.replace(ANCHOR, INSERT)
open(F, "w", encoding="utf-8").write(s)
print("parish.ts: P248-sekcija ponovno vstavljena")
