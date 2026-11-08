// P225 krop pass-3 — hi-DUELI (z15-37/34! z40-19/49! z66-37/57!) + ime-DUEL (z52-Marta/Maria!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p224';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)}`);
}
const N = { 138: 7, 141: 7, 143: 8, 144: 8 };
const YT = 0.165, YB = 0.975;
function rowBand(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.010, Math.min(0.999, y0 + B + 0.014)]; }
// z15 = vrsta 1 (idx0 0); z40 = vrsta 5 (idx0 4); z52 = vrsta 2 (idx0 1); z66 = vrsta 8 (idx0 7)
{ const [a,b] = rowBand(138, 0); await crop('r3_z15_s138_hi', 138, a, b, 0.16, 0.26, 9.0); }
{ const [a,b] = rowBand(141, 4); await crop('r3_z40_s141_hi', 141, a, b, 0.16, 0.26, 9.0); }
{ const [a,b] = rowBand(143, 1); await crop('r3_z52_s143_ime', 143, a, b, 0.26, 0.42, 7.0); }
{ const [a,b] = rowBand(144, 7); await crop('r3_z66_s144_hi', 144, a, b, 0.16, 0.26, 9.0); }
console.log('P225 krop pass-3: 4 izrezi');
