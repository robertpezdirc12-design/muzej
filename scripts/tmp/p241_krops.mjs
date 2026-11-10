// P241 kropi — poročna 04455, leto 1882 = 4/13 (s45–s50)
// pass-2: 10 polovic (s45–s49 L+D) · pass-3: 5 nodat-trakov (številčenje) · pass-3b: ultra-zoom bloki
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p241';
fs.mkdirSync(`${TMP}/krops`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`)
    .extract({ left: Math.round(x0 * meta.width), top: Math.round(y0 * meta.height), width: Math.round((x1 - x0) * meta.width), height: Math.round((y1 - y0) * meta.height) })
    .resize({ width: Math.min(Math.round((x1 - x0) * meta.width * sc), 1800) })
    .png().toFile(`${TMP}/krops/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrija: razprti-listi 2457–2469×1800; vrstice ytop 0.165, yb 0.975
const N = { 45: 4, 46: 4, 47: 4, 48: 5, 49: 6, 50: 6 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

// --- pass-2: polovice (L = ženini, D = neveste) ---
for (const s of [45, 46, 47, 48, 49]) {
  await crop(`s${s}_levo_cel`, s, 0.04, 0.99, 0.02, 0.505, 1.6);
  await crop(`s${s}_desno_cel`, s, 0.04, 0.99, 0.495, 0.99, 1.6);
}

// --- pass-3: nodat-trakovi (levo številčenje) ---
for (const s of [45, 46, 47, 48, 49]) await crop(`s${s}_nodat`, s, 0.14, 0.99, 0.02, 0.16, 3.0);

// --- pass-3b: ultra-zoom vrstice (Griblje + PEZDIRC + meja/restart) ---
const Z = [
  [45, 0, 'p01_s45_r1_grib35'],   // vpis 1 — Anna Cvet GRIBLJE 35 (nevesta) + RESTART!
  [45, 1, 'p02_s45_r2'],          // vpis 2 — Šikar/Rozman (datum-duel 23./8.?)
  [46, 3, 'p03_s46_r8_grib'],     // vpis 8 — Johan Pazeš h38 × Anna Dragos h12 (POLNI!)
  [47, 0, 'p04_s47_r9_pezdirc'],  // vpis 9 — Georg Pezdirc × Margaretha Pezdirc (OBA PEZDIRC!)
  [47, 0, 'p05_s47_r9_datum'],    // vpis 9 — datum 9./15.-duel
  [48, 0, 'p06_s48_r13_grib56'],  // vpis 13 — Katharina Brinc h56 (48 let!)
  [48, 2, 'p07_s48_r15_grib'],    // vpis 15 — Matthias Jakopič h13 × Maria Pezdirc h52 (POLNI!)
  [48, 3, 'p08_s48_r16_pezdirc'], // vpis 16 — Michael Pezdirc Prusi × Anna Jakopič h8!
  [49, 0, 'p09_s49_r18_pezdirc'], // vpis 18 — Anne Pezdirc Otok 1
  [49, 3, 'p10_s49_r21_pezdirc'], // vpis 21 — Anne Pezdirc Krupšiše
  [49, 5, 'p11_s49_r23_grib'],    // vpis 23 — Nicolaus Lesiro h1 × Katharina Škrce h10 (POLNI!)
  [45, 0, 'p12_s45_meja'],        // MEJA-1881/82: glava 1882 + restart-1 (zgornji pas)
];
for (const [sken, idx0, name] of Z) { const [y0, y1] = row(sken, idx0); await crop(name, sken, y0, y1, 0.02, 0.98, 2.2); }
// meja-krop: zgornjih 45% lista s45 (tail-1881? + glava 1882 + vpis 1)
await crop('p12_s45_meja_top', 45, 0.03, 0.52, 0.02, 0.62, 2.2);
console.log('KROPI KONČANI');
