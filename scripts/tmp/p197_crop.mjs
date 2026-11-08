// P197: crop kontestiranih vrstic za fokusirano agent-oči forenziko
// (P196-KROP-metodologija: 1.7× zoom, frakcijske koordinate razprtja!)
import sharp from 'sharp';
import fs from 'fs';

const crops = [
  // [scan, name, x0frac, y0frac, x1frac, y1frac]
  ['s164', 'meja-split',      0.02, 0.28, 0.99, 0.62],  // z63-tail + '1880'-SPLIT-GUTTER + z1 Karavanič (obe polovici!)
  ['s164', 'griblje-z2-z4',   0.02, 0.55, 0.66, 0.74],  // z2 Huoe + z3 Krian + z4 Novak (Griblje h10/h8/h21)
  ['s165', 'glava-z8',        0.02, 0.09, 0.66, 0.24],  // leto-glava '1880 Feber' + z8 (1859→1880 forenzika!)
  ['s165', 'z10-kuncelj',     0.02, 0.28, 0.66, 0.42],  // z10 vas Griblje?-h5 Kuncelj 70J
  ['s166', 'z19-z22',         0.02, 0.12, 0.66, 0.44],  // z19 Timec-h39 + z22 Grabrian-h20 (Griblje)
  ['s168', 'z52-klobucar',    0.02, 0.74, 0.66, 0.94],  // z52 Klobučar-h47 (Griblje, zadnja vrstica)
  ['s169', 'griblje-z53-z57', 0.02, 0.13, 0.66, 0.62],  // z53 Mihelič + z55 Klepec + z56 Kere + z57 Pezdirc (glave 1880-August + September!)
  ['s169', 'bottom-z60-z62',  0.02, 0.66, 0.99, 0.97],  // z60 + z61 + z62-MANJKAJOČA (polna-širina = starost/bolezen!)
  ['s170', 'glava-z63',       0.02, 0.09, 0.99, 0.26],  // leto-glava '1880 Novobr' + z63 (1853→1880 forenzika!)
  ['s170', 'griblje-z65-z66', 0.02, 0.29, 0.66, 0.51],  // z65 Hukar-h27 + z66 Simec-h18 (Griblje)
];

fs.mkdirSync('/tmp/p197/crops', { recursive: true });

for (const [scan, name, x0, y0, x1, y1] of crops) {
  const meta = await sharp(`/tmp/p197/${scan}.jpg`).metadata();
  const left = Math.round(x0 * meta.width);
  const top = Math.round(y0 * meta.height);
  const width = Math.min(Math.round((x1 - x0) * meta.width), meta.width - left);
  const height = Math.min(Math.round((y1 - y0) * meta.height), meta.height - top);
  const out = `/tmp/p197/crops/${scan}-${name}.png`;
  await sharp(`/tmp/p197/${scan}.jpg`)
    .extract({ left, top, width, height })
    .resize({ width: Math.min(Math.round(width * 1.7), 1500) })
    .png()
    .toFile(out);
  console.log('OK', out, `${width}x${height}`);
}
