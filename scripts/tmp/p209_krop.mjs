// P209 krop — ord_s69 + arb_s69_meja (invarianta-'1868' + vsota-4-delna!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p209';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  const left = Math.round(x0 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.round((x1 - x0) * meta.width);
  const height = Math.max(30, Math.round(y1 * meta.height) - top);
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left, top, width, height })
    .resize({ width: Math.min(Math.round(width * sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
// s69: 11-realnih (1-tail + vsota + 10-new?) → vizualno-~12-vrstic
await crop('ord_s69_full', 69, 0.12, 0.99, 0.02, 0.14, 3.5);
await crop('arb_s69_meja', 69, 0.02, 0.42, 0.02, 0.60, 2.2);
console.log('GOTOV');
