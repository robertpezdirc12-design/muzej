import sharp from 'sharp';
const TMP = '/tmp/p213';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
await crop('z34_ime2_s42', 42, 0.335, 0.415, 0.24, 0.55, 4.5);
await crop('z85_hisa_s45', 45, 0.78, 0.88, 0.17, 0.28, 5.0);
await crop('z6_ime_s40', 40, 0.30, 0.38, 0.24, 0.55, 4.5);
await crop('z9_ime_s40', 40, 0.475, 0.555, 0.24, 0.55, 4.5);
