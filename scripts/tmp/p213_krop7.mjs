import sharp from 'sharp';
const TMP = '/tmp/p213';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
await crop('z18_hisa2_s41', 41, 0.22, 0.30, 0.17, 0.28, 5.0);
await crop('z85_ime_s45', 45, 0.78, 0.88, 0.24, 0.55, 4.0);
await crop('z44_ime_s42', 42, 0.90, 0.99, 0.24, 0.60, 4.0);
await crop('z44_hisa_s42', 42, 0.90, 0.99, 0.17, 0.28, 5.0);
await crop('z61_s44_re', 44, 0.21, 0.31, 0.02, 0.88, 2.8);
