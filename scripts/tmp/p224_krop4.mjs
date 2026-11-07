import sharp from 'sharp';
const TMP = '/tmp/p224';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1600) }).png().toFile(`${TMP}/krop3/${name}.png`);
  console.log('OK', name);
}
// tesni-hišni-celici (x0.185–0.29!) + del-vsa-za-kontekst
await crop('duel_z90_s159_cell', 159, 0.395, 0.515, 0.02, 0.30, 7.0);
await crop('duel_z91_s159_cell', 159, 0.495, 0.615, 0.02, 0.30, 7.0);
await crop('duel_z92_s159_cell', 159, 0.595, 0.715, 0.02, 0.30, 7.0);
await crop('duel_z54_s154_cell', 154, 0.605, 0.745, 0.02, 0.30, 7.0);
await crop('duel_z58_s155_cell', 155, 0.145, 0.285, 0.02, 0.30, 7.0);
await crop('duel_z31_s151_cell', 151, 0.53, 0.75, 0.02, 0.30, 6.0);
await crop('duel_z22_s150_cell', 150, 0.555, 0.685, 0.02, 0.30, 7.0);
await crop('duel_z23_s150_cell', 150, 0.655, 0.785, 0.02, 0.30, 7.0);
console.log('duel-celic: 8');
