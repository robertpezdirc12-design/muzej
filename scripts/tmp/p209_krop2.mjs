import sharp from 'sharp';
const TMP = '/tmp/p209';
// s69: 12-vizualnih (tail-103 + vsota + z1–z10)
const h = (0.97 - 0.14) / 12;
const y0 = 0.14 + 2.3 * h, y1 = 0.14 + 4.6 * h;
const meta = await sharp(`${TMP}/s69.jpg`).metadata();
await sharp(`${TMP}/s69.jpg`).extract({ left: Math.round(0.03*meta.width), top: Math.round(y0*meta.height), width: Math.round(0.35*meta.width), height: Math.round((y1-y0)*meta.height) })
  .resize({ width: 1400 }).png().toFile(`${TMP}/krop-grib/arb_s69_z1cell.png`);
console.log('OK');
