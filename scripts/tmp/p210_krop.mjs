// P210 krop — arb_s61_glava (invarianta-'1867'!) + ord_s61
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p210';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
await crop('ord_s61_full', 61, 0.12, 0.99, 0.02, 0.14, 3.5);
await crop('arb_s61_glava', 61, 0.02, 0.34, 0.02, 0.62, 2.2);
console.log('GOTOV');
