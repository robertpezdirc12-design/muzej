// P221 krop pass-7 — s198 vrstice 7-9 (z100/z101/z102) + s198 row1-3 kalibracija
import sharp from 'sharp';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `y${y0.toFixed(3)}-${y1.toFixed(3)}`);
}
const B = (0.975 - 0.165) / 9;
for (const [i, nm] of [[0, 'r7_s198_row1'], [1, 'r7_s198_row2'], [2, 'r7_s198_row3'], [6, 'r7_s198_row7'], [7, 'r7_s198_row8'], [8, 'r7_s198_row9']]) {
  const y0 = 0.165 + i*B, y1 = y0 + B;
  await crop(nm, 198, y0-0.012, y1+0.012, 0.02, 0.88, 3.0);
}
