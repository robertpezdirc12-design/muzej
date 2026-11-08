import sharp from 'sharp';
const TMP = '/tmp/p227';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
// s119: tabela z92–z96 ≈ y0.16–0.65; 5 vrstic B≈0.097
await crop('s119_z92_fix', 119, 0.155, 0.27, 0.02, 0.99, 3.6);
await crop('s119_z95_fix', 119, 0.44, 0.56, 0.02, 0.99, 3.6);
await crop('s119_glava_jahr1879', 119, 0.055, 0.155, 0.02, 0.40, 4.5);
await crop('s119_schnoerkel', 119, 0.62, 0.90, 0.02, 0.99, 2.4);
console.log('DONE');
