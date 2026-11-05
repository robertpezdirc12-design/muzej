// P206 krop-6 — ORDINALNI-STOLPEC cele s88 (x-0.02–0.14, ×3.5)
import sharp from 'sharp';
const TMP = '/tmp/p206';
const meta = await sharp(`${TMP}/s88.jpg`).metadata();
const top = Math.round(0.12 * meta.height);
const width = Math.round(0.14 * meta.width);
const height = Math.round(0.99 * meta.height) - top;
await sharp(`${TMP}/s88.jpg`).extract({ left: Math.round(0.02*meta.width), top, width, height })
  .resize({ width: Math.min(Math.round(width * 3.5), 1400) }).png().toFile(`${TMP}/krop2/ord_s88_full_column.png`);
console.log('OK');
