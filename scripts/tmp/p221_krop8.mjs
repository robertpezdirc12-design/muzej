// P221 krop pass-8 — s198 DNO (vse vrstice y0.63-1.0, celotna širina) + s198 ordinali-zgornji-del
import sharp from 'sharp';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `y${y0.toFixed(3)}-${y1.toFixed(3)}`);
}
await crop('r8_s198_dno', 198, 0.63, 1.0, 0.02, 0.88, 3.4);
await crop('r8_s198_zgornji', 198, 0.14, 0.66, 0.02, 0.88, 3.0);
