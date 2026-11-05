// P206 krop-3.krog — ORDINALNI-STOLPEC-ZOOM s88-r11..r13 (x-levo, 3×) — arbitr 30-vs-31
import sharp from 'sharp';
import fs from 'fs';

const TMP = '/tmp/p206';
const YT = { a: 0.14, b: 0.97 };
const n = 13; // s88
const h = (YT.b - YT.a) / n;

const JOBS = [
  ['ord_s88_r11_r13', 11.2, 14.6],  // r11..r13 ordinalni-stolpec + vas-stolpec
  ['ord_s88_r12_r13', 12.2, 14.6],  // r12..r13 tesneje
];

for (const [name, r0, r1] of JOBS) {
  const y0 = Math.max(0.0, YT.a + (r0 - 1) * h);
  const y1 = Math.min(0.999, YT.a + (r1 - 1) * h);
  const meta = await sharp(`${TMP}/s88.jpg`).metadata();
  const left = Math.round(0.02 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.round(0.30 * meta.width) - left;
  const height = Math.max(30, Math.round(y1 * meta.height) - top);
  const out = `${TMP}/krop2/${name}.png`;
  await sharp(`${TMP}/s88.jpg`)
    .extract({ left, top, width, height })
    .resize({ width: Math.min(Math.round(width * 3), 1800) })
    .png()
    .toFile(out);
  console.log('OK', name, `y=${y0.toFixed(3)}–${y1.toFixed(3)}`);
}
console.log('KROG-3 GOTOV');
