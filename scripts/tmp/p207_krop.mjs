// P207 krop — ORDINALNI-STOLPCI cele s82/s83/s84-top (×3.5, recept-P206!) + glava-s81 + dno-s80
import sharp from 'sharp';
const TMP = '/tmp/p207';
const metaW = {};

async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = metaW[sken] ||= await sharp(`${TMP}/s${sken}.jpg`).metadata();
  const left = Math.round(x0 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.round((x1 - x0) * meta.width);
  const height = Math.max(30, Math.round(y1 * meta.height) - top);
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left, top, width, height })
    .resize({ width: Math.min(Math.round(width * sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
import fs from 'fs';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
await crop('ord_s82_full', 82, 0.12, 0.99, 0.02, 0.14, 3.5);
await crop('ord_s83_full', 83, 0.12, 0.99, 0.02, 0.14, 3.5);
await crop('ord_s84_full', 84, 0.12, 0.99, 0.02, 0.14, 3.5);
await crop('arb_s81_glava', 81, 0.02, 0.30, 0.02, 0.60, 2.2);   // '1870'-velika-letnica + z1–z2
await crop('arb_s80_dno',   80, 0.75, 0.995, 0.02, 0.60, 2.2);  // valovita-črta + konec-letnika
console.log('GOTOV');
