// P196: crop contested rows for focused VLM verification
import sharp from 'sharp';
import fs from 'fs';

const crops = [
  // [scan, name, x0frac, y0frac, x1frac, y1frac]
  ['s171', 'z72-tail', 0.02, 0.13, 0.66, 0.24],   // tail-1880 row (age 72 vs 92?)
  ['s171', 'z1',       0.02, 0.355, 0.66, 0.49],  // Movrin row (Jure/Ursula, 70/90?)
  ['s171', 'z2',       0.02, 0.465, 0.66, 0.575], // Reaf row (59J confirm)
  ['s171', 'z8',       0.02, 0.86, 0.66, 0.985],  // Toprič row (house 3/4, ½J/2J)
  ['s178', 'z69-z70',  0.02, 0.20, 0.66, 0.42],   // first two rows of s178
  ['s179', 'z81',      0.02, 0.20, 0.66, 0.34],   // first row of s179 (Svec/Ivec, 2J/6J)
  ['s179', 'z90',      0.02, 0.80, 0.66, 0.95],   // Köhler row (35J/45J)
];

fs.mkdirSync('/tmp/p196/crops', { recursive: true });

for (const [scan, name, x0, y0, x1, y1] of crops) {
  const meta = await sharp(`/tmp/p196/${scan}.jpg`).metadata();
  const left = Math.round(x0 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.min(Math.round((x1 - x0) * meta.width), meta.width - left);
  const height = Math.min(Math.round((y1 - y0) * meta.height), meta.height - top);
  const out = `/tmp/p196/crops/${scan}-${name}.png`;
  await sharp(`/tmp/p196/${scan}.jpg`)
    .extract({ left, top, width, height })
    .resize({ width: Math.round(width * 1.7) })
    .png()
    .toFile(out);
  console.log('OK', out, `${width}x${height}`);
}
