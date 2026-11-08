// P214 krop-2 — popravljena geometrija (kalibracija iz pass-1!):
// s36: row_i center = 0.206 + (i-1)*0.0493 → z12=row4: 0.354
// s37: row_i center = 0.2007 + (i-1)*0.0493 → z27=row4: 0.349, z33=row10: 0.644
// + TIGHT izrezi: z2-ime (KUNE-duel) + z2-bolezen (Gicht-duel) + z18-starost (65/68!) + z38-ime+datum
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p214';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// --- POPRAVLJENE full-row izreze ---
await crop('z12_s36_grib2', 36, 0.305, 0.405, 0.02, 0.88, 2.8);
await crop('z27_s37_grib2', 37, 0.30, 0.40, 0.02, 0.88, 2.8);
await crop('z33_s37_grib2', 37, 0.615, 0.71, 0.02, 0.88, 2.8);
// --- TIGHT izrezi (ultra-zoom za duele; širok-x-proba 0.25–0.75 = ime-cona?) ---
await crop('z2_ime_tight', 35, 0.55, 0.64, 0.25, 0.70, 4.5);
await crop('z2_bolezen_tight', 35, 0.55, 0.64, 0.60, 0.95, 4.5);
await crop('z18_starost_tight', 36, 0.605, 0.695, 0.60, 0.95, 4.5);
await crop('z38_ime_tight', 37, 0.865, 0.955, 0.25, 0.70, 4.5);
await crop('z38_datum_tight', 37, 0.865, 0.955, 0.02, 0.30, 4.5);
console.log('P214 krop pass-2: 8 izrezov');
