// P221 krop pass-4 — SEAM-DEFINITIVA: s198-top-zap-hi (prvi 3 ordinali!) + s197-twins-zap-hi
import sharp from 'sharp';
const TMP = '/tmp/p221';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
await crop('r4_s198_zap_top_hi', 198, 0.04, 0.32, 0.02, 0.14, 7.0);
await crop('r4_s197_zap_bot_hi', 197, 0.62, 0.99, 0.02, 0.14, 7.0);
