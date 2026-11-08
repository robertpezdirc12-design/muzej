// P221 krop pass-6 — s198 row-5 (z98?) — potencialna-pregrešena-GRIBLJE-vrstica! + kalibracija 9-vrstic
import sharp from 'sharp';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `y${y0.toFixed(3)}-${y1.toFixed(3)}`);
}
const B = (0.975 - 0.165) / 9;  // 9 vrstic (z94-z102)
for (let i = 3; i <= 5; i++) {
  const y0 = 0.165 + i*B, y1 = y0 + B;
  await crop(`r6_s198_row${i+1}`, 198, y0-0.012, y1+0.012, 0.02, 0.88, 3.0);
}
