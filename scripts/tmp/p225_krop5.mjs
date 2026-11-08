// P225 krop pass-4 — hi-DUELI po P224-receptu (x0.30–0.62 vas+hišna-regija! 6×):
// z15_s138 (37-vs-34!) + z40_s141 (49-vs-19!) + z66_s144 (57-vs-37!) + z52_s143 (hi-51 + ime-Marta/Maria!)
import sharp from 'sharp';
const TMP = '/tmp/p224';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
await crop('r5_z15_s138_hisna_hi', 138, 0.150, 0.295, 0.38, 0.63, 8.0);  // vrsta-1: 37/34-DUEL!
await crop('r5_z40_s141_hisna_hi', 141, 0.618, 0.758, 0.38, 0.63, 8.0);  // vrsta-5: 49/19-DUEL!
await crop('r5_z52_s143_hisna_hi', 143, 0.256, 0.382, 0.38, 0.63, 8.0);  // vrsta-2: h51 + ime!
await crop('r5_z66_s144_hisna_hi', 144, 0.864, 0.999, 0.38, 0.63, 8.0);  // vrsta-8: 57/37-DUEL!
console.log('P225 krop pass-4b');
