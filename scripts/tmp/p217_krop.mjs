// P217 krop — KROP-dokazi (leto 1860 = 26/29!):
// MEJA-dokaz (1): s20 restart-glava '1860'-vs-VLM-'1800'-MISREAD!
// GRIBLJE-VRSTICE (5): s20 z7/z13 + s21 z23/z24 + s22 z27 (full-row!)
// TAIL-1859-GRIBLJE-PEZDIRC (2): s17 z73-'Pardire[~Pezdirceva?]' + s18 z91-'Andreas-Pesdire-99J[?]'
// ZAP-DOKAZI (2): s22-r1-margin ('23'-vs-'27'-chain!) + s18-tens-duel ('80–91'-vs-'90–101'!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p217';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// --- MEJA-dokaz s20 (restart-glava + z1; 13 vrst; band≈0.065) ---
await crop('arb_s20_glava', 20, 0.06, 0.21, 0.02, 0.60, 3.0);
// --- GRIBLJE full-row izrezi ---
await crop('z7_s20_grib', 20, 0.49, 0.60, 0.02, 0.88, 2.8);
await crop('z13_s20_grib', 20, 0.885, 0.985, 0.02, 0.88, 2.8);
await crop('z23_s21_grib', 21, 0.69, 0.80, 0.02, 0.88, 2.8);
await crop('z24_s21_grib', 21, 0.755, 0.865, 0.02, 0.88, 2.8);
await crop('z27_s22_grib', 22, 0.105, 0.215, 0.02, 0.88, 2.8);
// --- TAIL-1859-GRIBLJE (PEZDIRC-dokaz!) ---
await crop('z73_s17_grib', 17, 0.46, 0.57, 0.02, 0.88, 2.8);
await crop('z91_s18_grib', 18, 0.175, 0.285, 0.02, 0.88, 2.8);
// --- ZAP-DOKAZI ---
await crop('s22_zap_stolpec', 22, 0.10, 0.60, 0.02, 0.115, 5.0);
await crop('s18_zap_stolpec', 18, 0.10, 0.95, 0.02, 0.115, 5.0);
// --- PAS-izrezi ---
await crop('z7_s20_pas', 20, 0.47, 0.60, 0.55, 0.95, 3.2);
await crop('z13_s20_pas', 20, 0.87, 0.985, 0.55, 0.95, 3.2);
await crop('z23_s21_pas', 21, 0.67, 0.80, 0.55, 0.95, 3.2);
await crop('z24_s21_pas', 21, 0.74, 0.865, 0.55, 0.95, 3.2);
await crop('z27_s22_pas', 22, 0.09, 0.215, 0.55, 0.95, 3.2);
console.log('P217 krop pass-1: 15 izrezov');
