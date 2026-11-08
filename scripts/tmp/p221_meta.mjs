import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p221';
for (let i = 185; i <= 200; i++) {
  const f = `${TMP}/s${i}.jpg`;
  if (!fs.existsSync(f)) continue;
  const m = await sharp(f).metadata();
  console.log(`s${i}: ${m.width}x${m.height} ${m.width > m.height ? 'LANDSCAPE' : 'PORTRAIT'} ratio=${(m.width/m.height).toFixed(2)}`);
}
