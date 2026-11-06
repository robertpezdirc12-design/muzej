// P221 krop pass-9 — s198 z101-zona kirurško
import sharp from 'sharp';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `y${y0.toFixed(3)}-${y1.toFixed(3)}`);
}
await crop('r9_s198_z101a', 198, 0.795, 0.885, 0.02, 0.60, 4.5);
await crop('r9_s198_z101b', 198, 0.885, 0.975, 0.02, 0.60, 4.5);
