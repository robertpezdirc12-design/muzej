// P206 krop-5 — CELOTNA s88 tabela (ordinala-stolpec do bolezni) 2×
import sharp from 'sharp';
const TMP = '/tmp/p206';
const meta = await sharp(`${TMP}/s88.jpg`).metadata();
const top = Math.round(0.13 * meta.height);
const width = Math.round(0.62 * meta.width);
const height = Math.round(0.87 * meta.height) - top;
await sharp(`${TMP}/s88.jpg`).extract({ left: Math.round(0.015*meta.width), top, width, height })
  .resize({ width: Math.min(Math.round(width * 2), 1800) }).png().toFile(`${TMP}/krop2/arb_s88_full_table.png`);
console.log('OK');
