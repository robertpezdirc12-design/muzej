// P208 krop — ord-stolpci ×3.5 (recept-P206) s75/s76/s80 + arb_s75_meja + z13-detail
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p208';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });

async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  const left = Math.round(x0 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.round((x1 - x0) * meta.width);
  const height = Math.max(30, Math.round(y1 * meta.height) - top);
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left, top, width, height })
    .resize({ width: Math.min(Math.round(width * sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
const YT = { a: 0.14, b: 0.97 };
// s75: 14-vrstic (4-tail + vsota + 9-new) → h=(0.83)/14
const h75 = (YT.b - YT.a) / 14;
await crop('ord_s75_full', 75, 0.12, 0.99, 0.02, 0.14, 3.5);
await crop('arb_s75_meja', 75, Math.max(0.02, YT.a + 2 * h75), Math.min(0.99, YT.a + 7 * h75), 0.02, 0.55, 2.2); // vsota + glava + z1–z2
await crop('arb_z13_s76r6', 76, YT.a + 4.6 * ((YT.b - YT.a) / 14), YT.a + 7.2 * ((YT.b - YT.a) / 14), 0.02, 0.75, 2.4); // z13-hišna!
await crop('ord_s80_full', 80, 0.12, 0.99, 0.02, 0.14, 3.5);
console.log('GOTOV');
