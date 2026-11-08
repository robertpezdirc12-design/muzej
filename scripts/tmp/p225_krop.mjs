// P225 krop pass-1 — KROP-dokazi (krstna 04104, leto 1881 = 5/15!):
// ZAP-STOLPCI (12): s136–s147 (restart-z1-GRIBLJE-h55! + 1881-z1–z89 + tail-Dez-8–21 + finis!)
// FOLIACIJA (13): s135–s147 (gola-svinčna-'sken−6' — s135='129'! s136='130'! s147='141'-pričakovana!)
// MEJA (2): arb_s135_finis (tail-1880-z116–z122 + 'finis' + glava-'Jahr 18 80.'!) + arb_s136_meja (glava-'Jahr 1881.' + restart-z1!)
// MESEC-STOLPCI (3): s136 (Jän→Feber-z6!) + s137 (Feb→Mär-z11→Apr-z14!) + s147 (Dez-tail-8–21!)
// GRIBLJE-VRSTICE (17): vse-Griblje-1881!
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p224';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-vrstic (page-VLM-števec!)
const N = { 135: 7, 136: 7, 137: 7, 138: 7, 139: 7, 140: 7, 141: 7, 142: 8, 143: 8, 144: 8, 145: 8, 146: 8, 147: 7 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- ZAP-stolpci (ordinalna-linija!) ---
for (const p of Object.keys(N)) { if (+p >= 136) await crop(`s${p}_zap_stolpec`, +p, 0.05, 0.99, 0.02, 0.115, 5.0); }

// --- FOLIACIJA + glave (gola-svinčna-'sken−6'!) ---
for (const p of [135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147]) await crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2);

// --- MEJA (1880/81!) ---
await crop('arb_s135_finis', 135, 0.04, 0.99, 0.02, 0.62, 2.6);  // tail-1880-z116–z122 + 'finis' + glava-'Jahr 18 80.'
await crop('arb_s136_meja', 136, 0.02, 0.60, 0.02, 0.62, 2.8);   // glava-'Jahr 1881.' + restart-z1-Jän-1-GRIBLJE-h55!

// --- MESEC-STOLPCI (chronologija!) ---
await crop('s136_mesec_stolpec', 136, 0.10, 0.99, 0.09, 0.42, 4.0);  // z1–z7: Jän-1–24 + Feber-11-×2!
await crop('s137_mesec_stolpec', 137, 0.10, 0.99, 0.09, 0.42, 4.0);  // z8–z14: Feb-23/24 + Mär-1/2/16 + Apr-31(März!)
await crop('s147_mesec_stolpec', 147, 0.10, 0.99, 0.09, 0.42, 4.0);  // z83–z89: Dez-tail-8–21!

// --- GRIBLJE full-rows (page-VLM-vrsta-indeksi, 1-based → idx0 = vrsta−1) ---
const G = [
  [136, 0, 'z01_s136_grib'],   // Agnes h55 — RESTART-z1-GRIBLJE-Jän-1!
  [138, 0, 'z15_s138_grib'],   // Matthias h37[~]
  [139, 6, 'z28_s139_grib'],   // Dorothea h3
  [140, 1, 'z30_s140_grib'],   // Georg h38
  [141, 4, 'z40_s141_grib'],   // Georg h49
  [141, 6, 'z42_s141_grib'],   // Anna h20
  [142, 0, 'z43_s142_grib'],   // Maria h17
  [142, 2, 'z45_s142_grib'],   // Anna h8[~]
  [142, 5, 'z48_s142_grib'],   // JustynAnna?/Justina h62
  [143, 1, 'z52_s143_grib'],   // Marta h51
  [143, 4, 'z55_s143_grib'],   // Maria h63
  [143, 6, 'z57_s143_grib'],   // Dorothea h14
  [144, 7, 'z66_s144_grib'],   // Nikolaus h57
  [145, 4, 'z71_s145_grib'],   // Catharina h24[~] — Okt-30!
  [146, 0, 'z75_s146_grib'],   // Johann h6 — oče-Jakofčič!
  [146, 3, 'z78_s146_grib'],   // Anna h22[~] — oče-MILEK!
  [146, 6, 'z81_s146_grib'],   // Maria h42[~] — oče-Perdijc-PEZDIRC!
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await crop(name, s, a, b, 0.02, 0.88, 2.8); }

console.log('P225 krop pass-1: ' + (12 + 13 + 2 + 3 + 17) + ' izrezov');
