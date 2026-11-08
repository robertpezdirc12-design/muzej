import sharp from 'sharp';
const TMP = '/tmp/p227';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
// z76 (s116 zadnja vrstica) — pripis-pod-iménom
await crop('z76_datum2', 116, 0.78, 0.99, 0.24, 0.62, 5.0);
// z15 todtgeboren (s108 r4) — ime-stolpec MAX
await crop('todt_z15_MAX', 108, 0.60, 0.78, 0.24, 0.62, 5.5);
// z95 Griblje-h40 (s119 r3) — celotna + pripis-†15.6.1941
await crop('grib_z95_MAX', 119, 0.60, 0.84, 0.02, 0.99, 3.6);
// z1 restart (s106 r6) — MAX
await crop('z1_restart_MAX', 106, 0.78, 0.94, 0.02, 0.99, 3.4);
console.log('DONE');
