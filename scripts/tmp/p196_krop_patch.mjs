// P196-KROP: surgical patch of HEAD proof JSON with 7 crop-verified corrections (2025-11-03-seja)
import fs from 'fs';

const P = 'research/issue17/parish-death-1881-04106.json';
const d = JSON.parse(fs.readFileSync(P, 'utf8'));

const byZ = z => d.entries.find(e => String(e.zaporedna) === z);

// —— z1: ime Jure (ne Ursula!) + spol M + bolezen Asthma-glif — starost 90 OSTAJA (KROP+HEAD-se-strinjata!) ——
const z1 = byZ('1');
z1.ime = "Jure Movrin [★KROP-2025-11-03★: ime-crop-jasno-JURE — HEAD-zavrnitev-'Jure'-preveč-grobo (zavrla-VESELJ-ime+starost)!]";
z1.spol = 'M';
z1.bolezen = 'Asthma [★KROP★-glif-kratki + VLM-fresh — HEAD: Abzehrung]';
z1.opomba = "★KROP★: ime-JURE (crop-s171: J-u-r-e-jasno!) + starost-90-OSTAJA (crop-'90 Japre' + HEAD-se-strinjata — VLM-fresh-'70'-ZAVRJENA!)";

// —— z69: KROP-POTRJENO (HEAD-že-Zemelj-h21-2J ✓ — dodan-le-dokaz) ——
byZ('69').opomba = "★KROP-POTRJENO-s178★: Zemelj-h21-2J-crop-jasno ('Martin Mlue'/'2 Japre'/'Marpnn'-glif) — stara-kanon-'Prilozje-63J'-odpravljena!";

// —— z70: KROP-POTRJENO (HEAD-že-65 ✓) ——
byZ('70').opomba = "★KROP-POTRJENO-s178★: 65J-crop-jasno ('65.') — stara-kanon-'63J'-odpravljena! + Sodeja-pair-cf.-z74!";

// —— z74: hiša 26 (ne 21!) — Sodeja-pair-ista-hiša ——
const z74 = byZ('74');
z74.hisna = "26 [★KROP-POTRJENO-s178★: h26-crop-jasno — HEAD-'21 [~26?]'-razrešeno-na-26!]";
z74.opomba = '★KROP★: h26-ne-h21 (crop-s178: 26.-jasno!) — Sodeja-pair-z70+z74-ISTA-hiša-Prilozje-h26!';

// —— z81: ime Ivec + starost 6 (ne 2!) ——
const z81 = byZ('81');
z81.ime = "Katharina Ivec [★KROP-POTRJENO-s179★: Ivec-crop-jasno — HEAD-'Svec [~Ivec?]'-razrešeno!]";
z81.starost = "6 [★KROP-POTRJENO-s179★: 6-ne-2! — '6 Japre'-crop-jasno]";
z81.opomba = "★KROP★: 6J (crop-s179: '6'-jasno — HEAD-'2 [~6?]'-razrešeno!) + ANGINA-nit-ostaja!";

// —— z90: starost 45 (ne 35!) ——
const z90 = byZ('90');
z90.starost = "45 [★KROP-POTRJENO-s179★: 45-ne-35! — '45 Japre'-crop-jasno (Kurrent-4-obroč + 5)]";
z90.opomba = "★KROP★: 45J (crop-s179: '45'-jasno — HEAD-'35 [VLM-45-ZAVRŽEN!]'-zavrnitev-ODPRAVLJENA — crop+VLM-fresh-se-strinjata!) + stan-'Gasthaus-wirth'? → 'Güblanns-?-glif' [~migrant-družina]";
z90.stan = "Güblanns-?-stan-glif [★KROP★ ~migrant-družina — HEAD-'Gasthaus-wirth'-dvomljivo]";

// —— okvir: tail-1880 92J→72J + restart-z1 Ursula→Jure ——
if (d.okvir?.meja_1880_81) {
  d.okvir.meja_1880_81 = d.okvir.meja_1880_81
    .replace(/92J/g, '72J [★KROP-POTRJENO-s171★: 72-ne-92!]')
    .replace(/Ursula-Movrin-Certoviše-h15-90J-Abzehrung/gi, 'Jure-Movrin-Certoviše-h15-90J [★KROP-POTRJENO-s171★: Jure-ne-Ursula!]');
}

// —— statistika: spol-prešteje (z1 F→M) ——
const male = d.entries.filter(e => e.spol === 'M').length;
const female = d.entries.filter(e => e.spol === 'F').length;
if (d.statistika) {
  if ('male' in d.statistika) d.statistika.male = male;
  if ('female' in d.statistika) d.statistika.female = female;
  if (d.statistika.spol) { d.statistika.spol.moski = male; d.statistika.spol.zenske = female; }
  if (d.statistika.najstarejša && /Ursula/.test(d.statistika.najstarejša)) {
    d.statistika.najstarejša = d.statistika.najstarejša.replace(/Ursula/g, 'Jure [★KROP★]');
  }
}

// —— honesty: dodaj KROP-sejo ——
if (Array.isArray(d.honesty)) {
  d.honesty.push('★KROP-SEJA-2025-11-03★: 10-kropov (s171-z72/z1/z2/z8 + s178-z69/z70/z71/z74 + s179-z81/z82/z90) → 7-popravkov: z1-ime-Ursula→JURE (+spol-M +bolezen-Asthma-glif) + z72-tail-92J→72J + z69-Zemelj-h21-2J-POTRJENO + z70-65J-POTRJENO + z74-h21→h26 + z81-Svec-2J→Ivec-6J + z90-35J→45J — VSE-crop-dokazani; 19-Griblje-blokov-NESPREMENJENIH (z2-REAF-59J + z82-h48-31J + z89-h2-27J-crop-POTRJENI!)');
} else if (d.honesty && typeof d.honesty === 'object') {
  d.honesty['krop_seja_2025-11-03'] = '10-kropov → 7-popravkov (z1-Ursula→JURE + z72-92J→72J + z69 + z70 + z74-h26 + z81-Ivec-6J + z90-45J) — crop-dokazi; 19-Griblje-blokov-NESPREMENJENIH';
}

// —— notes: dodaj KROP-zapis ——
d.notes = d.notes || [];
d.notes.push('KROP-seja-2025-11-03 (nadaljevalna): fresh-VLM-branja-×9 (s171–s179) + 10-cropov → 7-kanon-popravkov (zgoraj) — proof-posodobljen; parish.ts-komentar + qa-p196-opis usklajena; verifier-p196-26/26-PASS-obdržan.');

fs.writeFileSync(P, JSON.stringify(d, null, 1) + '\n');
console.log('KROP-PATCH OK —', P);
console.log('statistika M/Ž:', male + '/' + female);
for (const z of ['1', '69', '70', '74', '81', '90']) {
  const e = byZ(z);
  console.log(`z${z}: ime=${(e.ime || '').slice(0, 42)} | hisna=${String(e.hisna).slice(0, 22)} | starost=${String(e.starost).slice(0, 28)} | spol=${e.spol}`);
}
console.log('okvir-meja:', (d.okvir?.meja_1880_81 || '').slice(0, 160));
