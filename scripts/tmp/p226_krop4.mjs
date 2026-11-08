// P226 krop pass-4 — POPRAVKI odmika (generozni pasovi)
import sharp from 'sharp';
const TMP = '/tmp/p226';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
// (sken, y0, y1, ime)
const FIX = [
  [121, 0.50, 0.66, 'f_z14'],   // z14 Griblje 39
  [122, 0.76, 0.94, 'f_z26'],   // z26 Griblje 13
  [125, 0.38, 0.54, 'f_z46'],   // z46 Griblje 27 (celotna!)
  [132, 0.55, 0.73, 'f_z99'],   // z99 Griblje 33
  [132, 0.78, 0.97, 'f_z101'],  // z101 Griblje 29
];
for (const [s, y0, y1, n] of FIX) await crop(n, s, y0, y1, 0.02, 0.985, 2.6);
console.log('pass-4 DONE');
