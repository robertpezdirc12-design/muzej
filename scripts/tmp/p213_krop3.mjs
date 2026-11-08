// P213 krop-3 — z18-re-crop (row2 = y0.23–0.33; rows-start ~0.17!)
import sharp from 'sharp';
const TMP = '/tmp/p213';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
await crop('z18_s41_grib2', 41, 0.23, 0.33, 0.02, 0.88, 2.8);
