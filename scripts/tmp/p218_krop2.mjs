// P218 krop pass-2 — s11 vsotna/'1859'-glava + z6-Griblje
import sharp from 'sharp';
const TMP = '/tmp/p218';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
await crop('arb_s11_vsota_glava', 11, 0.38, 0.68, 0.005, 0.62, 2.6);   // vsotna + '1859'-glava + z1–z3
await crop('z6_s11_grib2', 11, 0.73, 0.845, 0.005, 0.90, 2.8);          // z6-Griblje (1 vrstica nižje prej!)
console.log('P218 krop pass-2: 2 izreza');
