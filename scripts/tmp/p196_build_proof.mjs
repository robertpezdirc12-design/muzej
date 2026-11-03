// P196 v2: proof JSON builder — machine-extracted base + targeted overrides (robust)
import fs from 'fs';

const raw = JSON.parse(fs.readFileSync('/tmp/p196/entries_raw.json', 'utf8'));
// exclude the unreadable z[?] artifact row on s172 (kanon: 93 vpisov)
const base = raw.filter(e => e.zaporedna !== '[?]');

// —— spol map (z@skan → M/F) ——
const SPOL = { '1@s171':'M','2@s171':'F','3@s171':'F','4@s171':'F','5@s171':'M','6@s171':'M','7@s171':'F','8@s171':'M','8@s172':'F','9@s172':'F','10@s172':'F','11@s172':'F','12@s172':'M','13@s172':'F','14@s172':'M','15@s172':'F','16@s172':'M','17@s172':'F','18@s172':'M','19@s172':'M','20@s173':'M','21@s173':'F','22@s173':'F','23@s173':'F','24@s173':'M','25@s173':'F','26@s173':'F','27@s173':'M','28@s173':'F','29@s173':'M','30@s174':'F','31@s174':'F','32@s174':'M','33@s174':'F','34@s174':'F','35@s174':'F','36@s174':'M','37@s174':'M','38@s174':'F','39@s174':'F','40@s175':'M','41@s175':'F','42@s175':'M','43@s175':'F','44@s175':'M','45@s175':'M','46@s175':'F','47@s175':'F','48@s175':'F','49@s175':'M','50@s176':'M','51@s176':'F','52@s176':'M','53@s176':'F','54@s176':'M','55@s176':'F','56@s176':'F','57@s176':'F','58@s176':'M','59@s176':'F','60@s177':'F','61@s177':'M','62@s177':'F','63@s177':'F','64@s177':'F','65@s177':'F','66@s177':'F','67@s177':'M','68@s177':'F','69@s178':'M','70@s178':'F','71@s178':'F','72@s178':'F','73@s178':'F','74@s178':'F','75@s178':'F','76@s178':'F','77@s178':'M','78@s178':'M','79@s178':'F','80@s178':'M','81@s179':'F','82@s179':'F','83@s179':'F','84@s179':'F','85@s179':'F','86@s179':'F','87@s179':'M','88@s179':'F','89@s179':'F','90@s179':'M','91@s179':'F','92@s179':'F' };

// —— overrides: kanon-19-Griblje-blokov + KROP-2025-11-03 + dokumentirane-zavrnitve ——
const OV = {
  // ——— 19 GRIBLJE-kanon (parish.ts-bloki — NESPREMENJENI, KROP-potrjeni) ———
  'z2@s171': { hisna:'17', ime:'Margaretha REAF [~Reaß?; KROP-potrjeno: ne-Kralj!]', stan:"'Brig-zy-honn'-glif [~; KROP/VLM: Obžigobarica-forma]", starost:'59 let [KROP-POTRJENO: ne-39/56!]', bolezen:'Lungenentzündung-glif', duhovnik:'Franz Jančar v.R.C. Pfarrer', add:'1.-GRIBLJE-vpis-1881 (po-MEJI!)' },
  'z8@s172': { hisna:'4', ime:"Anna BRINE [~Brinc? — 'Božinec'-ZAVRŽEN!]", stan:"'Alt-bannsin'-glif [~]", starost:'63 let', bolezen:'Maffpüffl-glif [★★★ M/W-nit-1/4!]', duhovnik:'Franz Jančar', add:'z8-DUPLIKAT-2/2! BRINC/PRINC-dvojnica-cf.-z51!' },
  'z15@s172': { hisna:"56 [KANON: 'h36'-ZAVRŽEN!]", ime:'Maria ŠIMEC [VLM: Finc]', stan:"'Aul-wirtin'-glif [~]", starost:'56 let [VLM: 55?]', bolezen:'Asthma', duhovnik:'Franz Jančar', add:'ŠIMEC-MREŽA-h56 (→h54-×2+h55-1882-P195)!' },
  'z29@s173': { hisna:'37 [VLM: h35]', ime:'Matthias HLINAR jun. [~Hliunar-glif; VLM: Hričič]', stan:"'nachl.-Defron'-glif [~]", starost:'1 leto', bolezen:'Frisern [★★★ FRISELN-1/3!; VLM: Krastelj]', duhovnik:'Franz Jančar v.H.O. Priester', add:'h37-KATASTROFA-1/2-v-2-dneh (z30-NASLEDNJI-DAN)! h37=DAVICA-1883-P194-z70-nit!' },
  'z30@s174': { hisna:'37 [VLM: h27]', ime:'Anna HUDIČ [VLM: Husič]', stan:"'Interša'-glif [~]", starost:'31 let', bolezen:'an der Lähmung [~paraliza!; VLM: Gehirnentzündung]', duhovnik:'Franz Jančar v.R.C. Pfarrer', add:"h37-KATASTROFA-2/2! '1881'-glava+'April'-VIZUALNO (s174-top)!" },
  'z33@s174': { hisna:'18', ime:'Ana TIMEC [VLM: Time]', stan:'⅔-Güblanns-wittbe-glif [~; VLM: hčerka-Žiklenda]', starost:'33 let [VLM: 23?]', bolezen:'[Schlafsucht? ~Sl-ff-glif; VLM: Slabost]', duhovnik:'Franz Jančar', smrt:'9. [~4?]', pokop:'10./11.', add:'datum-VLM/crop-razkol (9-vs-4!) [~]' },
  'z35@s174': { hisna:'44 [VLM: h24]', ime:'Katharina HAMBIČ [~Hamzić?; VLM: Kambič]', stan:"'Lind-wirtin'-glif [~; VLM: Vavtova-wilb]", starost:'35 let', bolezen:'[Schlachon? ~glif]', duhovnik:'Franz Jančar v.R.C. Pfarrer', add:'h44=HLEBUČAR-veriga (1883-P194-z73→Klobučar-1884→BRINEC-1901)!' },
  'z47@s175': { hisna:'21', ime:'Barbara OŽOLT [~Ožbolt?; VLM: Dorgeh/Doreth]', stan:'⅔-Güblanns-wittbe-glif [~grahovlina?]', starost:'50 let', bolezen:'Asthma [VLM: Verkohrung-glif?]', duhovnik:'Franz Jančar', add:'h21-×2-1881 (z78-Pögl-november)! ASTHMA-nit!' },
  'z51@s176': { hisna:'8 [VLM: h3]', ime:'Barbara BRINC [~Princ?; VLM: Prime]', stan:'⅔-Güblanns-wirthin-glif [~; VLM: ¼-Gärtlerstochter]', starost:'8 MESECEV', bolezen:'[Krämpfe? ~Brüpe-glif — FRISELN-sorodna!]', duhovnik:'Franz Jančar', add:'BRINC/PRINC-DVOJNICA-1/2 (z86-h26-61J-december — babica-vnuček? [~])! h8=JAKOFČIČ-1882-nit!' },
  'z54@s176': { hisna:"66 [KANON: 'h6e'-ZAVRŽEN!; VLM: h62]", ime:'Matthias KRIŽAN [~Hrižan? — V/K-glif]', stan:"'Magzinjter'-glif [~ — ista-kot-z1-Movrin!; VLM: Meiereibesitzer]", starost:'¾ let [GLIF; VLM: 77?]', bolezen:'Blasensucht-glif [~Blasp-fucht; VLM: Magenkrebs]', duhovnik:'Franz Jančar', add:'h66=NOVA-GRIBLJE-hiša-1881! KRIŽAN-nit (cf.-1920-P186)!' },
  'z60@s177': { hisna:'78 [VLM: h48]', ime:'Anna LOŽAR', stan:'Gärtners-tochter-glif [~; VLM: Gänslers-Aufwartin]', starost:'1 leto [~]', bolezen:'Maspenn-glif [★★★ M/W-nit-2/4!; VLM: Marbmil]', duhovnik:'Franz Jančar v.R.C. Priester', add:"h78=LOZAR-NIT-1.člen (P195: Legan→Funkl→Lozar→LOZAR-1883)! '1881'-glava-VIZUALNO (s177-top)!" },
  'z77@s178': { hisna:'31', ime:'Josef KMECL [VLM: Kraulič]', stan:'⅔-Gült.-glif [~gütl.bes; VLM: ½-Griblj.]', starost:'6¼ let [GLIF ~ne-6½!; VLM: 64?]', bolezen:'[Schlarme? ~glif; VLM: Asthma]', duhovnik:'Franz Jančar v.R.C. Priester', add:'h31-GRIBLJE! KMECL-nit-cf.?' },
  'z78@s178': { hisna:'21', ime:'Johann PÖGL [~Pögek?; VLM: Pegel]', stan:'Lanns-Kind-glif [~; VLM: konovod]', starost:'— [starost-BLEDE/odsek; VLM: 1-Jafr]', bolezen:'Entzündung-glif [~Binözfpfiung; VLM: Kindsgefälle]', duhovnik:'Franz Jančar v.H.C. Priester', add:'h21-×2-1881 (z47-Ožolt-julij)!' },
  'z79@s178': { hisna:'60', ime:'Katharina TOMINC [VLM: Tomasevnič]', stan:'Müllers-wittwe-glif [~mlinarjeva-vdova; VLM: delavka-hlapica]', starost:'71 let', bolezen:'Altersschwäche-glif [~Abz-glif]', duhovnik:'Franz Jančar v.H.C. Priester', add:'h60=TOMINC-hiša (cf.-P195-h60-nit)! MÜHLZÜGLER-ženska-forma-nit!' },
  'z80@s178': { hisna:'13', ime:'Michael JANOPIRČ [~Janopitsch?; VLM: Juhničič]', stan:'⅔-Gültler-sohn-glif [~; VLM: ½-gribljanski-syn]', starost:'19 let [~Jafr]', bolezen:'Entzündung-glif [VLM: Kindsgefälle]', duhovnik:'Franz Jančar v.H.C. Priester', pokop:"1. ['Dezember'-IZPISAN!]", add:'★★★ ULEDBA-#10: MESEC-SPREMEMBA-V-VRSTICI (Nov-29→pokop-Dezember-1)! h13=JAKOFČIČ-1882-nit!' },
  'z82@s179': { hisna:'48', ime:'Maria HLEBČAR [~Hlebec?; KROP/VLM: Hlobučar — cf.-Klobučar-veriga!]', stan:'⅔-Güblanns-wirthin?-glif [~]', starost:'31 let [KROP-POTRJENO: ne-34!]', bolezen:'Brünnow-glif [~Bräune? — DAVICA-sorodna!; VLM: Brünnen]', duhovnik:'Franz Jančar v.R.C. Priester', add:'HLEBEC-DVOJNICA-1/2 (z89-h2-27J-2-tedna-kasneje)!' },
  'z85@s179': { hisna:'65 [~]', ime:'Margaretha MILEK [VLM: Mihelič/Mileli]', stan:"'Anzüglannsin'-glif [~; VLM: delavka/starosta]", starost:'71 let [GLIF ~ne-91!; VLM: 74?]', bolezen:'Altersschwäche [dolgi-ſ-ligatura!; VLM: Abzehrung]', duhovnik:'Franz Jančar v.H.C. Priester', add:'h65=MILEK-NIT (cf.-h65-1882-P195 + z46-Zemelj)! NAJSTAREJŠA-december [~]' },
  'z86@s179': { hisna:'26 [~]', ime:'Barbara PRINC [VLM: Perne]', stan:'(Lanič?-nadpis [~]) Lanns-wirtin-glif [~; VLM: izgrbelska-toča]', starost:'61 let', bolezen:'Asthma', duhovnik:'Franz Jančar', add:'BRINC/PRINC-DVOJNICA-2/2 (z51-h8-8-MESECEV-avgust)!' },
  'z89@s179': { hisna:'2', ime:'Maria HLEBEC [VLM: Heleec/Helec/Kvelec]', stan:'⅔-Gribljanns-tochter-glif [~; VLM: grbelska-pastirica]', starost:'27 let [KROP-POTRJENO!]', bolezen:'Lungenentzündung', duhovnik:'Franz Jančar v.H.C. Priester', add:'HLEBEC-DVOJNICA-2/2! h2-GRIBLJE = ZADNJI-GRIBLJE-vpis-1881!' },
  // ——— KROP-popravki + dokumentirane-zavrnitve (ne-Griblje) ———
  'z1@s171': { ime:'Jure Movrin [KROP: ne-Ursula!]', hisna:'15', starost:'90 let [KROP: ne-70!]', add:'RESTART-z1! KROP-POTRJENO-s171 (ime+starost)' },
  'z8@s171': { hisna:'3 [KROP-vizualno]', ime:'Janez Toprič [~; VLM: Paprič/Popit]', starost:'½ Jahr [KROP-POTRJENO: ne-2-leti!]', add:'z8-DUPLIKAT-1/2! (s172-z8-Brine-2.-vpis-isto-številko — 5.×-linija!)' },
  'z9@s172': { vas:'Prilozje', hisna:"30 [KANON: 'Griblje-h30'-ZAVRŽEN!]", add:'VLM-zavrnitev: vas-Griblje→PRILOZJE (kanon)!' },
  'z18@s172': { mesec:'Feber/März', pokop:'25. [März?]', add:'cf.-ULEDBA-#10: mesec-sprememba-v-vrstici (Feb-24→März-25?) [~]' },
  'z68@s177': { mesec:'Oktober', smrt:'30.', pokop:'1. [November]', add:'cf.-ULEDBA-#10: Okt-30→Nov-1-mesec-sprememba-v-vrstici [~]!' },
  'z69@s178': { vas:'Zemelj', hisna:'21 [KROP-POTRJENO]', ime:'Martin Mlue [~Mehle?]', starost:'2 leti [GLIF-KROP: ne-63!]', bolezen:'Maspenn-glif [★★★ M/W-nit-3/4!]', add:'KROP-POTRJENO-s178: vas-Zemelj-h21 (ne-Prilozje!) + 2J (ne-63!)' },
  'z70@s178': { starost:'65 let [GLIF-KROP: ne-63!]', bolezen:'Marbm-glif [★★★ M/W-nit-4/4!]', add:'KROP-POTRJENO-s178: 65J (ne-63!) + Sodeja-pair-cf.-z74!' },
  'z71@s178': { hisna:'32-ex-41 [~28-ex-41? — COMPOUND-glif!]', add:"COMPOUND-hiša-glif (cf.-Dobravce-'39-ex-13'-1882-P195)!" },
  'z73@s178': { smrt:'31.', pokop:'2. [November]', add:'cf.-ULEDBA-#10: Okt-31→Nov-2 [~]!' },
  'z74@s178': { hisna:'26 [KROP-POTRJENO: ne-h21!]', add:'KROP-POTRJENO-s178: h26 (ne-h21)! Sodeja-pair-z70+z74-ISTA-hiša!' },
  'z81@s179': { ime:'Katharina Ivec [~Svec/Jvec? — KROP]', starost:'6 let [GLIF-KROP: ne-2!]', bolezen:'Angina [★★★ 1.×-PREDZGODOVINE — latinsko-modro-črnilo!]', add:'KROP-POTRJENO-s179: 6J (ne-2)! ANGINA-nit-cf.-DAVICA-×2-1882!' },
  'z90@s179': { starost:'45 let [GLIF-KROP: ne-35!]', bolezen:'Tuberculose [★★★ 1.×-LATINSKA-forma!]', duhovnik:'Jozef Dovgan? [~Franz-Dovgan-forma?]', add:'KROP-POTRJENO-s179: 45J (ne-35)! cf.-honesty-z43-Lungentuberculose [~]' },
};

// —— blok-z-ključi (19 Griblje-blokov-v-parish.ts) ——
const BLOK = new Set(['2@s171','8@s172','15@s172','29@s173','30@s174','33@s174','35@s174','47@s175','51@s176','54@s176','60@s177','77@s178','78@s178','79@s178','80@s178','82@s179','85@s179','86@s179','89@s179']);

const pagOf = s => parseInt(s.slice(1), 10) - 6;
// normalize keys: lookup key has NO 'z' prefix (raw zaporedna), OV/BLOK defined with 'z'
const OVn = Object.fromEntries(Object.entries(OV).map(([k, v]) => [k.replace(/^z/, ''), v]));
const BLOKn = new Set([...BLOK].map(k => k.replace(/^z/, '')));
const entries = base.map(e => {
  const key = `${e.zaporedna}@${e.skan}`;
  const ov = OVn[key] || {};
  const out = {
    skan: e.skan,
    pag: pagOf(e.skan),
    zaporedna: e.zaporedna,
    mesec: ov.mesec ?? e.mesec,
    smrt: ov.smrt ?? e.smrt,
    pokop: ov.pokop ?? e.pokop,
    vas: ov.vas ?? e.vas,
    hisna: ov.hisna ?? e.hisna,
    ime: ov.ime ?? e.ime,
    stan: ov.stan ?? e.stan,
    starost: ov.starost ?? e.starost,
    bolezen: ov.bolezen ?? e.bolezen,
    previden: '1',
    duhovnik: ov.duhovnik ?? e.duhovnik,
    spol: SPOL[key] ?? '?',
    griblje: String(ov.vas ?? e.vas).startsWith('Griblje'),
    blok_v_parish: BLOKn.has(key),
    leto: 1881,
    opomba: [ov.add, e.opomba].filter(Boolean).join(' | ') || null,
  };
  return out;
});

// —— statistika ——
const griblje = entries.filter(e => e.griblje);
const cleanH = e => String(e.hisna).split(' ')[0];
const gHise = [...new Set(griblje.map(cleanH))].sort((a, b) => +a - +b);
const gCount = griblje.reduce((m, e) => { const h = cleanH(e); m[h] = (m[h] || 0) + 1; return m; }, {});
const gHiseX2 = Object.entries(gCount).filter(([, n]) => n > 1).map(([h, n]) => `h${h}-×${n}`);
const male = entries.filter(e => e.spol === 'M').length;
const female = entries.filter(e => e.spol === 'F').length;
const meseci = entries.reduce((m, e) => { const k = (e.mesec || '?').split(/[\s/(]/)[0]; m[k] = (m[k] || 0) + 1; return m; }, {});

const proof = {
  faza: 'P196',
  tema: 'mrliška PREDZGODOVINA 04106 — leto 1881 (5. leto predzgodovinske linije)',
  knjiga: '04106 (matricula-online.eu — Sterb-Buch, nemška tiskana forma)',
  okvir: {
    leto_1881: 'z1 = Jure Movrin, Certoviše h15, 90J, Jänner 3./5. (s171; KROP-POTRJENO: ime-Jure-ne-Ursula + 90J-ne-70!)',
    meja_1880_81: "s171 (velika-rokopisna-'18'|'81'-oznaka-SPLIT-ČEZ-RAZPON: '1'+'8'-L / '8'+'1'-R = 35.-POTRDITEV-invariante + P194-tehnika-#9-ponovitev! tail-1880 = z72-Jože-Valčič-Vranoviče-h14-72J [KROP: ne-92!]-Wassersucht + restart-z1)",
    meja_1881_82: "s180-top (ŽE-P195: '1882.'-glava + Jänner + Anno-Domini + restart-z1 = 34.-potrditev!)",
    konec_1881: 's179-z92-December-29/31 (Krasinec-h24-Marija-Staravinič-6J-Abzehrung)',
    zaporedna: 'z1–z92 (92 vpisanih vrstic) + z8-DUPLIKAT (s171-z8-Geršiče-Toprič-½J-Dovgan ≠ s172-z8-Griblje-Brine-63J-Jančar) = 93 vpisov! (5.×-duplikat-linija: cf.-1921-s218 + 1904-s253 + 1885-z4 + 1882-z33)',
    forma: "nemška-tiskana-'Sterb-Buch'-skroz (slovenska-šele-1885-s205/s206-P192!)",
    skeni: 's171–s179 (9 skenov; Pag. 165–173 = sken − 6!)',
    preštevanje: 'pag == sken − 6: s171-165 ✓ + s172-166 ✓ + s173-167 ✓ + s174-168 ✓ + s175-169 ✓ + s176-170 ✓ + s177-171 ✓ + s178-172 ✓ + s179-173 ✓ (9.-17.-potrditev-preslikave!)',
  },
  statistika: {
    vpisane_vrstice: entries.length,
    zaporedna_obseg: 'z1–z92 + z8-dup = 93',
    griblje_vpisov: griblje.length,
    griblje_hise: gHise,
    griblje_hise_x2: gHiseX2,
    najstarejša: 'z1-h15-Certoviše-Jure-Movrin-90-let (Asthma) [KROP-POTRJENO!]',
    najmlajša: 'z8-s171-Geršiče-Toprič-½-Jahr [KROP-POTRJENO!] + z51-h8-BRINC-8-mesecev + z44-Gradac-6-dni [~]',
    male,
    female,
    meseci,
  },
  anomalije: {
    z8_duplikat: '5.×-duplikat-številčenja-linija (s171-z8-Toprič-½J ≠ s172-z8-Brine-63J — cf.-1921-s218 + 1904-s253 + 1885-z4 + 1882-z33!)',
    uledba_10: "MESEC-SPREMEMBA-V-VRSTICI: z80 (Nov-29→pokop-'Dezember-1'-IZPISAN!) + cf.-z68 (Okt-30→Nov-1) + z73 (Okt-31→Nov-2) + z18 (Feb-24→März-25?) [~] — NOVA-FORENZIČNA-ULEDBA-#10!",
    h37_katastrofa: '×2-V-2-DNEH: z29-Hlinar-jun-1J-Apr-18/19 + z30-Hudič-31J-Apr-19/21 (cf.-h1-ZELŠKO-×2-1882 + h1-DAVICA-1885-P192!)',
    brinc_princ: 'DVOJNICA-×2: z51-h8-dojenček-8-MESECEV + z86-h26-61J (babica-vnuček?-hipoteza [~])',
    hlebec_dvojnica: '×2: z82-h48-Hlebčar-31J + z89-h2-Hlebec-27J (2-tedna-kasneje — cf.-h44-HLEBUČAR-veriga!)',
    sodeja_pair: 'z70-Maria + z74-Anna-Sodeja = ISTA-hiša-Prilozje-h26 [KROP-POTRJENO-z74!]',
    migrantni_glifi: '⅔-Güblanns-...-glif-×10+ (s171-z8 + z33 + z47 + z51 + z69 + z70 + z71 + z72 + z74 + z75 + z82 + z89...) — Gribljančani-po-vazah!',
    compound_hisa: "z71-Gradac-'32-ex-41'-glif [~28?] (cf.-Dobravce-'39-ex-13'-1882-P195!)",
    precrtani: 'z21-Šilak (prečrtan!) + z87-Tajnič (prečrtan-in-popravljen!)',
    friseln: '×3-kanon (z29-h37 + z34-Prilozje-17J + z84-Dobravce-1J) + širša-družina-novi-VLM (z14 + z52 + z32-Fraisen + Krämpfe-glifi [~])',
    mw_nit: '×4-GLIFA-forenzika: z8-h4-Maffpüffl + z60-h78-Maspenn + z69-Zemelj-Maspenn + z70-Prilozje-Marbm [~Masern-pustl? — KROP-potrjene-vrednosti!]',
    angina: 'z81-Gradac-h32-Ivec-6J-ANGINA (1.×-predzgodovine — latinsko-modro-črnilo!)',
    tuberculose: 'z90-Gradac-h1-Köhler-45J-TUBERCULOSE (1.×-LATINSKA-forma!) + z43-Lungentuberculose [~nemška-forma-honesty!]',
    starost_nejasne: 'z78-Pögl-BLEDE + z88-Perdiš-"1-leto-pri-otroku"-nemogoče [?] + z54-¾ [~77?] + z77-6¼ [~64?]',
  },
  duhovniki: {
    jančar_dominanta: 'Franz-JANČAR-19/19-GRIBLJE = 100% (3.-leto-zapored: 1881-×19/19 → 1882-~25+/59 → 1883-dominanta!) + ~40-vseh-vpisov',
    dovgan: "Franz-DOVGAN-×~15-IZKLJUČNO-ne-Griblje (Prilozje/Krasinec/Zemelj/Dobravce/Hrast/Gradac...) + z90-'Jozef-Dovgan?' [~ — 2.-Dovgan-kandidat? cf.-Jakob-Dovgan-1882-#31!]",
    forme: "'Prieſter'-Kurrent-ligatura-ULEDBA (dolgi-ſ+in) + VLM-'Janežič/Gorgan'-forme [~Jančar/Dovgan-misreads]",
  },
  hišne_kontinuitete: {
    h2: 'HLEBEC-z89 (zadnji-Griblje-1881!)',
    h4: 'BRINE-z8-s172 [z8-DUPLIKAT!] — → BRINC-1884-P193?',
    h8: 'BRINC-z51 — → JAKOFČIČ-1882-P195!',
    h13: 'JANOPIRČ-z80 — → JAKOFČIČ-1882-P195 + Kusič-1885-P192!',
    h17: 'REAF-z2 (1.-Griblje-vpis-1881)',
    h18: 'TIMEC-z33',
    h21: 'OŽOLT-z47 + PÖGL-z78 (×2!)',
    h26: 'PRINC-z86 (+ Sodeja-pair-z70/z74-ne-Griblje-cf.)',
    h31: 'KMECL-z77',
    h37: 'HLINAR-z29 + HUDIČ-z30 (KATASTROFA!) — → DAVICA-1883-P194-z70-nit!',
    h44: 'HAMBIČ-z35 — → HLEBUČAR-1883-P194-z73 → Klobučar-1884 → BRINEC-1901!',
    h48: 'HLEBČAR-z82 — cf.-Klobučar-veriga!',
    h56: 'ŠIMEC-z15 — → ŠIMEC-MREŽA-h54-×2+h55-1882-P195!',
    h60: 'TOMINC-z79 — cf.-P195-h60-nit!',
    h65: 'MILEK-z85 — → h65-1882-P195!',
    h66: 'KRIŽAN-z54 (NOVA-GRIBLJE-hiša-1881!) — cf.-1920-KRIŽAN-P186!',
    h78: 'LOŽAR-z60 — → LOZAR-1883 (P195-nit: Legan→Funkl→Lozar!)',
  },
  forme: {
    glave: "natisnjena-'Sterb-Buch.'-glava (s179-vizualno!) + ročne-letnice-prek-glave (s174-'1881' + s177-'1881') + meseci-nad-vrsticami (s175-Juni/Juli + z68-Oktober-nad-vrstico!)",
    jezik: 'nemščina-skroz (Jänner/Feber/März/April/Mai/Juni/Juli/August/September/October/November/December)',
  },
  crossChecks: {
    pag_preslikava: '9/9-skenov: pag == sken − 6 ✓✓',
    z_nadaljevanje: 'z1→z92-neprekinjeno (razen-pričakovani-z8-dup) ✓',
    z8_duplikat: '2-različna-vpisa-z-isto-številko ✓ (5.×-linija)',
    griblje_bloki: '19-proof-Griblje-vpisov == 19-parish.ts-blokov ✓',
    meja_35: "MEJA-1880/81-s171-split-'18'|'81' = 35.-POTRDITEV-invariante ✓",
    meja_34: 'MEJA-1881/82-s180-top = 34.-potrditev (P195-naveza) ✓',
    krop_verifikacija: '10-kropov-s171/s178/s179 — 19-Griblje-blokov-NESPREMENJENIH + 7-komentar-popravkov (z1 + z72-tail + z69 + z70 + z74 + z81 + z90) ✓',
  },
  honesty: {
    krop_popravki_komentarja: '×7 (2025-11-03): z1-Ursula→JURE (90J-ostaja!) + z72-tail-92J→72J + z69-Prilozje-63J→Zemelj-h21-2J + z70-63J→65J + z74-h21→h26 + z81-Svec-2J→Ivec-6J + z90-35J→45J — VSE-z-KROP-VLM-dokazi!',
    vlm_razkoli: 'starost-z54 (¾-vs-77) + z77 (6¼-vs-64) + z33 (33-vs-23) + z85 (71-vs-74) + ime-z2 (REAF-kanon-vs-Kralj-VLM) + ime-z47 (OŽOLT-kanon-vs-Dorgeh-VLM) — kanon+KROP-prednost!',
    's172_z[?]_vrstica': 'VLM-izpisal-1-neberljivo-vrstico-na-s172 (brez-podatkov) — po-kanonu-93-vpisov + z19→z20-kontinuiteti = artefakt/glava-meseca [~izključena]',
    friseln_taksonomija: "kanon-FRISELN-×3 (strog-'Frisern'-glif) vs novi-VLM-širša-družina (z14 + z52-Friesen + z32-Fraisen + Krämpfe-glifi) — taksonomija-ne-rešena [~]",
    tuberculose_forme: 'z90-latinska-Tuberculose (kanon-1.×!) vs z43-nemška-Lungentuberculose [~] — forme-razkol',
    letnica_glave_s175_s176: "VLM-branje-'1887'-v-glavi-s175/s176 = NAPAČNA-branja-glave (z-teka-40→59-potrjuje-1881!) [~VLM-quirk]",
    s178_guess: "VLM-'[~1870-71]'-leto-guess-s178 = napačen (z-teka-69–80-nadaljuje-1881!)",
    nezrešeni_glifi: "stan-glifi-×20+ ('Magzinjter'/'Alt-bannsin'/'Anzüglannsin'/Maymurs-tochter...) + z90-priest-'Jozef-Dovgan?' [~] — ostajajo-odprti",
    previden: "'1'-v-Versehen-stolpcu-vseh-vpisov [~interpretacija-stolpca-nejasna — cf.-p1882-'/']",
  },
  kaskada: {
    naprej: 'P195-1882 (s180–s186, z1–z59) → P194-1883 → P193-1884 → P192-1885',
    nizi: 'FRISELN ×3-1881 → ×16-1882-FLOOD (epidemija-rast!) + M/W-nit-×4-1881 [~Masern?] + ANGINA-z81 → ×2-1882 + DAVICA-h37-nit → 1883-z70 + MILEK-h65 → 1882-h65 + LOZAR-h78 → 1883-LOZAR + ŠIMEC-h56 → 1882-h54/h55 + KRIŽAN-h66 → 1920-P186 + PEZDIRC-z75/z88 → 1882-\'Pozdire\'-×3',
  },
  lead: {
    p197: "1880 (nazaj-v-času!): tail-1880 = z72-s171-top (Jože-Valčič-Vranoviče-h14-72J [KROP]-Wassersucht-December-9/10) + '1880'-glava-natisnjena-s171 — 1880-se-konča-s-z72 → pričakovano-~72-vpisov; MEJA-1879/80 = NEZNANA [pred-s171-iskanje]; skeni-pričakovani: s1xx–s171 (Pag-do-164); dokaz: s171-glava-'des-Codes-1880' + tail-z72 ✓",
  },
  entries,
  notes: [
    '93 vpisov = 9 VLM-branj (s171–s179, celostansko-prompt-P195-metodologija) + 10 krop-verifikacij (s171-z72/z1/z2/z8 + s178-z69/z70-z71/z74 + s179-z81/z82/z90) + kanon-19-Griblje-blokov (parish.ts).',
    'z8-DUPLIKAT = 5. instanca fenomena (cf.-1921-s218 + 1904-s253 + 1885-z4 + 1882-z33) — 93-vpisov-ob-z1–z92-obsegu.',
    "MEJA-1880/81-'18'|'81'-SPLIT-ČEZ-RAZPON = 35.-potrditev-preslikave-invariante (tehnika-#9-iz-P194).",
    "ULEDBA-#10 (mesec-sprememba-v-vrstici): z80-glavni-dokaz ('Dezember-1'-izpisan-v-pokopnem-stolpcu) + 3-cf.-vrstice [~].",
    'KROP-seja-2025-11-03: 7-popravkov-starega-kanon-komentarja — VSE-dokazane-z-cropi; 19-Griblje-blokov-NESPREMENJENIH.',
  ],
};

const out = 'research/issue17/parish-death-1881-04106.json';
fs.writeFileSync(out, JSON.stringify(proof, null, 1) + '\n');
console.log('WROTE', out);
console.log('entries:', entries.length, '| griblje:', griblje.length, '| unikatne-hiše:', gHise.length, '| M:', male, 'Ž:', female);
console.log('griblje hiše:', gHise.join(','));
console.log('hiše-×2+:', gHiseX2.join(' | '));
console.log('meseci:', JSON.stringify(meseci));
const spoliNeznani = entries.filter(e => e.spol === '?').map(e => 'z' + e.zaporedna + '@' + e.skan);
if (spoliNeznani.length) console.log('SPOL-?:', spoliNeznani.join(','));
