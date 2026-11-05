// P206 krop-2.krog — arbitr: s88-r13 (DUP-31?), s87-r13 (110J?), s86-z1-celica ('1871.'-invarianta), s88-r12
import sharp from 'sharp';
import fs from 'fs';

const TMP = '/tmp/p206';
const YT = { a: 0.14, b: 0.97 };
const n_map = { 86: 12, 87: 13, 88: 13 };

fs.mkdirSync(`${TMP}/krop2`, { recursive: true });

// [ime, sken, r0, r1, x0, x1, scale]
const JOBS = [
  ['arb_s88r13_wide',   88, 12.5, 14.6, 0.00, 0.95, 2.2],  // r13 = 31[?]-zadnja-vrsta-s88 — ŠIROK!
  ['arb_s88r12_wide',   88, 11.3, 13.4, 0.00, 0.95, 2.2],  // r12 = 30-Krasinec-kontekst
  ['arb_s87r13_wide',   87, 12.5, 14.4, 0.00, 0.95, 2.2],  // r13 = 17-Grible-13-'110J[?]' — starost-stolpec!
  ['arb_s86_z1_cell',   86, 8.7, 10.6, 0.03, 0.42, 2.6],   // z1 (restart-1) — DATUMSKI-STOLPEC-'1871.'-invarianta!
  ['arb_s86_z3_z4',     86, 10.5, 12.6, 0.03, 0.42, 2.6],  // z3/z4-datumske-celice-kontekst
  ['arb_s87_z5_cell',   87, 4.6, 6.4, 0.03, 0.42, 2.6],    // z5-Plut-Jänner-celica
];

for (const [name, sken, r0, r1, x0, x1, sc] of JOBS) {
  const n = n_map[sken];
  const h = (YT.b - YT.a) / n;
  const y0 = Math.max(0.0, YT.a + (r0 - 1) * h);
  const y1 = Math.min(0.999, YT.a + (r1 - 1) * h);
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  const left = Math.round(x0 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.round((x1 - x0) * meta.width);
  const height = Math.max(30, Math.round(y1 * meta.height) - top);
  const out = `${TMP}/krop2/${name}.png`;
  await sharp(`${TMP}/s${sken}.jpg`)
    .extract({ left, top, width, height })
    .resize({ width: Math.min(Math.round(width * sc), 1800) })
    .png()
    .toFile(out);
  console.log('OK', name, `y=${y0.toFixed(3)}–${y1.toFixed(3)}`);
}
console.log('KROG-2 GOTOV');
