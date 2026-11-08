import sharp from 'sharp';
const TMP = '/tmp/p224';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1600) }).png().toFile(`${TMP}/krop3/${name}.png`);
  console.log('OK', name);
}
await crop('duel_z89_s159_cell2', 159, 0.24, 0.36, 0.02, 0.30, 7.0);
await crop('duel_z90_s159_cell2', 159, 0.34, 0.46, 0.02, 0.30, 7.0);
await crop('duel_z99_s160_cell2', 160, 0.40, 0.53, 0.02, 0.30, 7.0);
console.log('ok');
