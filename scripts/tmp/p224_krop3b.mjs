import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p224';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop3/${name}.png`);
  console.log('OK', name);
}
for (const p of [150, 151, 154, 155, 156, 158, 159, 160, 148, 149, 152, 153, 157]) await crop(`s${p}_hisna_strip2`, p, 0.14, 0.99, 0.185, 0.29, 6.0);
console.log('strip2: 13');
