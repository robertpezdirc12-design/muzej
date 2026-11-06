// P221 krop pass-10 — s199 TOP (z102-zona: nad-France-vrstica!)
import sharp from 'sharp';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `y${y0.toFixed(3)}-${y1.toFixed(3)}`);
}
await crop('r10_s199_top', 199, 0.12, 0.42, 0.02, 0.88, 3.2);
