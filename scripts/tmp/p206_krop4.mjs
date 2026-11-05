// P206 krop-4 — s88-r9..r13 ŠIROK (ordinala+datumi+vas+ime) — arbitr-13-vrstic
import sharp from 'sharp';
const TMP = '/tmp/p206';
const YT = { a: 0.14, b: 0.97 }; const n = 13; const h = (YT.b - YT.a) / n;
const y0 = Math.max(0.0, YT.a + (9 - 1) * h);
const y1 = Math.min(0.999, YT.a + (14.4 - 1) * h);
const meta = await sharp(`${TMP}/s88.jpg`).metadata();
const top = Math.round(y0 * meta.height);
const width = Math.round(0.88 * meta.width);
const height = Math.max(30, Math.round(y1 * meta.height) - top);
await sharp(`${TMP}/s88.jpg`).extract({ left: Math.round(0.01*meta.width), top, width, height })
  .resize({ width: Math.min(Math.round(width * 2), 1800) }).png().toFile(`${TMP}/krop2/arb_s88_r9_r13_wide.png`);
console.log('OK y=', y0.toFixed(3), y1.toFixed(3));
