# P130 — poročna knjiga 04455, polno leto 1901 (s114–s116 == Pag. 113–115)

## FAZA 0 — PONOVNA REKONSTRUKCIJA OKOLJA (po environment-resetu)
- `/home/z/muzej` (izgubljen) → klon GitHub-mirror `robertpezdirc12-design/muzej` @ **14b47f5** (Task 105-b; nov žeton ghp_l614 POTRJEN — 401-blokada rešena)
- `/home/z/.p126tmp` (izgubljen) → **inventory.txt** (192 URL-jev) rekonstruiran iz matricula `MatriculaDocView` konfiguracije (`/image/<base64>` → hosted-images.matricula-online.eu/SI-LNSA/…/P Podzemelj 1873-1922-NNN.jpg)
- `fetch130.py` (recept fetch128: UA + backoff + JPEG-magika) → s114–s117 (4× OK, 1. poskus)
- `crop_rows130.py` (recept P128/P129: L 0–1250 + R 1300–W, 2× LANCZOS; y-meje vizualno) → 18 obrezkov + ~25 pod-zoomov (4–8×)
- GitLab žetona (gl_api.py + .bak) OBA MRTVA (401/403) — mirror zaostanek 3 commiti (P128+P129+P130); akcija lastnika: PAT rotacija

## FAZA 1 — OKVIR (potrjen)
- **s114 = Pag. 113**: rokopisna glava **»1901.«** (podčrtana) + **v1–4**
- **s115 = Pag. 114**: **v5–9**
- **s116 = Pag. 115**: **v10–11** + rokopisna glava **»1902.«** (dvopodčrtana!) + v1–3/1902 — **P131 LEAD** (KOREKCIJA: P129-lead je pričakoval veliko tiskano glavo na s117!)
- **s117 = Pag. 116**: v4–6/1902 (brez glave — nadaljevanje); ⚠ tiskani stolpčni glavi na vseh straneh standardni
- **Pag. == sken − 1 = 16. potrditev** (velja 61–115)
- **1901 = 11 vpisov obojestransko** (min: 1886:7 → 1900:8 → 1899:9 → **1901:11**)
- Datumi: Jan 28 · Feb 4 · **Febr 11 ×6 (v3–v8!!)** · Jul 29 · Nov 4 · Nov 11
- ⚠ P130-lead korekcije ×4: Jänner 18→**28** · Otok 14→**34** · Kurjan?→**KRIŽAN** · Pačaj?→**PALČIČ**

## FAZA 1 — VPISI (11)
| v | datum | ženin (hiša, starost) | nevesta (hiša, starost) | duhovnik |
|---|---|---|---|---|
| 1 | 28.1. | Joseph **Križan** (Otok **34**, 23, ½ küblastofsju? [~]) | Barbara **Palčič** (Otok 21, 23, ½ Küblwirthschaft? [~]) | Rauy |
| 2 | 4.2. | Georg Rožman? (Borit? 19 [~], 31, ½ z gübler) | Anna Cvetič? (Hast? 11 [~], 24, z güblastof?-hči? [~]) | Rauy |
| 3 | 11.2. | Mathias Marasinič? (Krasinec **23**, 28, **½ gbl. Sohn**) | Barbara Žimec? (Grišiče? 35 [~], 22, **½ gbl. Tochter**) | Rauy |
| 4 | 11.2. | Peter Kambič (Krasinec **19**, **21**, ½ gübler) | Maria Jurajevič? (Otok 11, **18**, ½ gbl. Tochter) | Rauy |
| 5 | 11.2. | Franz Simonič (Gradac 20, 24, ½ gbl. Sohn) | Maria Jakša? (Gradac **77**, 21, Küblwirthschafts-tochter? [~]) | Rauy |
| 6 | 11.2. | Georg Jakobčič? (Cerkvišče? 26 [~], **34**, ½ gübler) | Barbara Štubljar? (Cerkvišče 1, **34**, ½ gbl. Tochter) | Rauy |
| 7 | 11.2. | Conrad Bartle (Metlika 38, 25, [?] ✓) | Engelbetha Prevec (Primostek 1, **18**, **¾ gbl. Tochter**!) | Rauy |
| 8 | 11.2. | Martin Štefanič (Podzemelj 6, 23, ½ gbl. Sohn) | **Anna Muc** (Primostek 4, 23, ½ gbl. Tochter) | Rauy |
| 9 | 29.7. | Mathias Marentič? (Gradac 11, **36**, ¼ gübler) | Maria Žumič? (Zastava 10, **30**, ½ gbl. Tochter) | Rauy |
| 10 | 4.11. | Johann Skerbavec? (Gradac 63, 24, ½ güblar?-štofa? [~]) | Anna Zučna? (Dobraviče? 15 [~], 19, z güblarštof-hči? [~]) | Rauy |
| 11 | 11.11. | Anton Gibelič? (Gradac 53, 23, z güblarštofa? [~]) | **Maria Muc** (Vranoviče **8**, 21, ½ güblastofa? [~]) | Rauy |

## FAZA 2 — MIKRO-REŠITVE (zoomi 4–8×)
- **MASA 11. FEBRUAR 1901 = 6 POROK** (v3–v8) — vsi šestje zoom-potrjeni »Febr 11« (dates_s114_34 + dates_s115_58); P130-lead napaka »19« pri v4 = HIŠNA ŠT., ne dan!
- **RAUY 11/11 = 100%** — novi ABSOLUTNI rekord dominance (P129 8/8; P128 Novak 5/9); v1–v11 vsi en podpis »Jos. Rauy R!«
- **v5 nevesta hiša = Gradac 77** (8× zoom: dva jasna sedmica; ne 44!)
- **v5 nevesta starost = 21** (ne 24); **v10 starosti = 24/19** (ne 34/24); **v11 ženin = 23**
- **v1 starosti = 23/23** — končnica »J.« = **Jahre** (ne ulomek ½!)
- **Rosetta EKSPlicitno ×2** (v3): »½ gbl. Sohn« + »½ gbl. Tochter« == 1891 »½ Griblers. Sohn« rosetta — kratke forme leto 1901 DOLGE [~ küblastofsju/Küblwirthschaft] izpodrivajo
- **v8 dispens št: 236** (22.1.1901) + robni **»potestate delegata«**; v1 dispens **Anverwantschaft** (afinost!) ddo 15/1.1901 **No 138** [~]
- **v7 robni zapis**: »Janko Bartle, arhivar in pro-tokolist [nad]škof.? pisarne v Za[g]reba?« — zagrebški arhivist-priča! + Weißstand **Theodulair? Lejihař, c. k. poštni asistent**
- **v9 zglasnica** »od dne 29/?. 1901 štev: 45« — MESEC neberljiv [~] (poroka 29.7.)
- **v2 Schmiedmeister == v10 Schmiedmeister** — ISTI Anton Palčič? Weißstand ×2 v letu!

## NOVELE (povzetek; podrobnosti v JSON)
1. **★ 6 POROK NA 11.2.1901** = 2. največji dan linije (rekord 1893: 7 — 6.2., P122!); 3× več od P129-rekordnega dneva; od 1894 NOVI REKORD
2. **★ RAUY 11/11 = 100%** — absolutni rekord; karierna linija Rauy 1886–1901 ≈ 49/55 [~]
3. **★ 0 OMEMB GRIBLJE** — 1. leto linije 1886–1901 (16 let) popolnoma brez Griblje; ASIMETRIJA s krstno 1901 (P96: vsi vpisi Griblje!)
4. **★ ¾ griblar 2. dokaz** — v7 oče Ignac Prevec + hči Engelbetha (Primostek 1) == P128 v7 Žugelj vzorec
5. **★ 1. DISPENS AFINOSTI** — v1 Anverwandtschaft (2. dum? No 138 Laibach 15/1.); v8 consanguinitas 4. kolena št 236 (cf. P128 v7 № 2319)
6. **★ POLNOLETNOST ZA ŽENINA** — v4 (21!; Metlika IV 218/89 + 9.6.1900 b 41/98 + deželna vlada št 1786) + v11 (OBA: ženin 23 + nevesta 21)
7. **★ MUC ×3** — v8 nevesta Anna + v11 nevesta Maria + Weißstand Johan Muc == P128 v3 PRIČA (h10 1890 ženin!) — triple-vloga
8. **★ Vranoviče 8** = 6. hiša vasi (1898 h4+h2; 1899 h9+h27+h28) — K/V-korekcija faza-1 potrjena
9. **★ 1. ČINOVNIKI/OBRTNIKI kot priče** — c.k. poštni asistent + zagrebški nadškofijski arhivar (robni zapis!) + Schmiedmeister ×2
10. **★ nove vasi** — Primostek ×2 · Cerkvišče ×2 · Zastava · Dobraviče? · Borit? · Hast? · Grišiče? [~] (+ Metlika 7. dokaz)
11. **★ Krasinec 3 hiše** — 18 (P129) + 19 + 23 (1901)
12. **mreže 1901** — Muc ×3 · Jurajevič ×3 · Palčič ×3 (v1 nevesta + v2+v10 Weißstand!) · Križan ×2 · Žimec ×2 · Jakša ×2 · Novačič ×2 · Perdinec ×2 · Novak ×2 · Klepec ×2 · Kambič ×2 (oče+Weißstand) · Marentič ×2 + čez-faza: Jakljevič (1898→1901) · Štrucelj (1900→1901) · Simonič (1893+1900→1901) · Hočevar (1898→1901)
13. **starosti** — najstarejši ženin 36 (v9), nevesta 34 (v6 — 2. linije po 68!); par 34×34 (v6); 8 nevest > 24-j prag? [~] — mj.-dokumenti 7/11

## P131 LEAD (korekcija)
- **glava »1902.« ŽE na s116** (dvopodčrtana) + v1–3/1902 tam; s117 = v4–v6 brez glave
- **v2/1902: »[G]pbyke? 5« × »Griblje 31«** = možna 2. DRUBEL-GRIBLJE poroka [~]!
- **v4/1902 (s117): Griblje 30 × Griblje 24** = DRUBEL-GRIBLJE poroka potrjena na prvi pogled!
- min 6 vpisov (s116–s117); skeni 117–120 že v .p126tmp
