// P221 krop pass-5 — s198 LEVI-TRAK (ordinali+datumi: koliko vrstic? prvi ordinal?) + s197 levi-trak
import sharp from 'sharp';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
await crop('r5_s198_levo', 198, 0.03, 0.99, 0.02, 0.24, 4.0);
await crop('r5_s197_levo', 197, 0.03, 0.99, 0.02, 0.24, 4.0);
