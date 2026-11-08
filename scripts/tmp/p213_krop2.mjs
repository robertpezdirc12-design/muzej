// P213 krop-2 — s41-SHIFT-SANACIJA (VLM +1-shift razkrit: margin-N = fresh-row(N-16)!):
// z18 (row2, y0.17–0.27) + z27 (row11, y0.72–0.82) + z30 (row14, y0.90–0.99) + z18-hisna-duel
// + glave s39 ('1863'-tail) + s40 ('1864' = 51.-POTRDITEV-invariante!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p213';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
await crop('z18_s41_grib', 41, 0.17, 0.27, 0.02, 0.88, 2.8);
await crop('z27_s41_grib', 41, 0.72, 0.82, 0.02, 0.88, 2.8);
await crop('z30_s41_grib2', 41, 0.90, 0.99, 0.02, 0.88, 2.8);
await crop('z18_hisa_s41', 41, 0.11, 0.27, 0.68, 0.92, 3.2);
await crop('arb_s39_glava', 39, 0.02, 0.14, 0.02, 0.65, 2.4);
await crop('arb_s40_glava', 40, 0.02, 0.14, 0.02, 0.65, 2.4);
console.log('GOTOV — 6 dodatnih');
