import sharp from 'sharp';
const TMP = '/tmp/p227';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name);
}
const N = { 111: 6, 116: 8, 115: 8, 106: 8 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.01, y0 + B + 0.01]; }
// z33 (s111 r2) — samo hišna celica, MAX-zoom
let [y0, y1] = row(111, 2);
await crop('duel2_z33_MAX', 111, y0, y1, 0.215, 0.285, 12.0);
// z69 (s116 r0) — hišna celica MAX
[y0, y1] = row(116, 0);
await crop('duel2_z69_MAX', 116, y0, y1, 0.215, 0.285, 12.0);
// referenca: z28 h17 (s110 r3) — hišna celica MAX (znana-17)
const N2 = { 110: 6 };
[y0, y1] = (() => { const B = (YB - YT) / N2[110]; const yy = YT + 3 * B; return [yy - 0.01, yy + B + 0.01]; })();
await crop('ref_z28_h17', 110, y0, y1, 0.215, 0.285, 12.0);
// referenca: z61 '22' (s115 r1) MAX
[y0, y1] = row(115, 1);
await crop('ref_z61_22', 115, y0, y1, 0.215, 0.285, 12.0);
console.log('DONE');
