// P221 krop pass-2 — seam-dueli + hi-zoom:
// SEAM-197/198 (94-duel!) + S199-ordinal-hi + S192-prazni-slot + S186-meja-hi (prečrtani-111/112 + VSOTNA!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// seam s197 (zadnji 2 vrstici: 93? 94?) + s198 (prve 2: 94/95?)
await crop('seam_s197_bot', 197, 0.70, 0.99, 0.02, 0.60, 3.2);
await crop('seam_s198_top', 198, 0.04, 0.38, 0.02, 0.60, 3.2);
// s199 ordinali-hi (triple-read: 102, 103, 103→104?)
await crop('s199_zap_hi', 199, 0.05, 0.72, 0.02, 0.14, 6.0);
// s192 prazni-slot (7. vrstica: idx 6)
const B192 = (0.975 - 0.165) / 8;
await crop('s192_slot7', 192, 0.165 + 6*B192 - 0.012, 0.165 + 7*B192 + 0.012, 0.02, 0.88, 3.0);
// s186 meja-hi (prečrtani-111/112 + VSOTNA + restart)
await crop('s186_meja_hi', 186, 0.05, 0.45, 0.02, 0.16, 5.5);
console.log('P221 krop pass-2: 5 izrezov');
