// P226 krop pass-3 — GRIBLJE-rows ŠIROKO (x1=0.98 — starševski/botrov stolpec!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p226';
const N = { 119: 5, 120: 8, 121: 9, 122: 9, 123: 8, 124: 7, 125: 9, 126: 7, 127: 6, 128: 7, 129: 8, 130: 7, 131: 8, 132: 8, 133: 7, 134: 7, 135: 7 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
const G = [
  [121, 1, 'w_z10'], [121, 2, 'w_z11'], [121, 5, 'w_z14'],
  [122, 8, 'w_z26'], [123, 4, 'w_z31'], [124, 0, 'w_z35'], [124, 1, 'w_z36'],
  [125, 4, 'w_z46'], [126, 0, 'w_z51'], [126, 3, 'w_z54'],
  [127, 0, 'w_z58'], [127, 3, 'w_z61'], [128, 1, 'w_z65'], [128, 5, 'w_z69'],
  [129, 1, 'w_z72'], [131, 2, 'w_z88'], [131, 3, 'w_z89'],
  [132, 1, 'w_z95'], [132, 5, 'w_z99'], [132, 7, 'w_z101'],
  [133, 2, 'w_z104'], [134, 5, 'w_z114'],
];
for (const [s, idx, name] of G) { const [a, b] = row(s, idx); await crop(name, s, a, b, 0.02, 0.985, 2.6); }
console.log('pass-3 DONE');
