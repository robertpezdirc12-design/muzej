import sharp from 'sharp';
const TMP = '/tmp/p224';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1600) }).png().toFile(`${TMP}/krop3/${name}.png`);
  console.log('OK', name);
}
await crop('duel_z22_s150_cell2', 150, 0.545, 0.685, 0.02, 0.36, 6.5);
await crop('duel_z23_s150_cell2', 150, 0.645, 0.785, 0.02, 0.36, 6.5);
await crop('duel_z31_s151_cell2', 151, 0.55, 0.72, 0.02, 0.36, 6.5);
console.log('ok');
