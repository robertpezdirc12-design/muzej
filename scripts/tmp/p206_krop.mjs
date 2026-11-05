// P206: KROP — 11 Griblje-vrstic 1871 + 7 forenzičnih probe (LUK-18 / DUP-31 / restart-glava-s86 / s85-'1876'-glava)
// recept P196–P205: frakcijske koordinate, kontekst ±1.2 vrstice, sharp 1.7×
import sharp from 'sharp';
import fs from 'fs';

const TMP = '/tmp/p206';

// vizualne-vrstice-per-sken (glava ~0.10–0.14; dno ~0.97) — s86: 7-tail+vsota+4-new=12; s92: 3+vsota+9=13
const YT = { a: 0.14, b: 0.97 };
const n_vrst_map = { 84: 13, 85: 13, 86: 12, 87: 13, 88: 13, 89: 14, 90: 14, 91: 12, 92: 13 };

fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });

// (ime, sken, od-vrste, do-vrste) — 1-based vizualne-vrstice; glava-vzorec za zone
const JOBS = [
  // —— forenzične probe
  ['probe_s87bottom_r12_13', 87, 11.6, 14.2],   // zap-16–17 + rob — vidi-li-se '18'?
  ['probe_s88top_r0_2',      88, 0.02, 2.8],    // glava + zap-18[?]/19/20 — LUK-18!
  ['probe_s88r13_zap31',     88, 12.4, 14.2],   // DUP-31-#1 (zadnja-vrsta s88)
  ['probe_s89r1_zap31',      89, 0.02, 2.8],    // DUP-31-#2 (prva-vrsta s89)
  ['probe_s86_restart',      86, 6.3, 12.9],    // tail-end + vsota + 'Jänner'-glava + zap-1–4 — INVARIANTA!
  ['probe_s85_head',         85, 0.02, 2.8],    // '1876'-glava-misread? + r1-zap51
  ['probe_s92_tail3',        92, 0.02, 4.2],    // zap-71–73 + vsota — soglasje-s-P205!
  // —— Griblje-vrste (11)
  ['grib_z5_s87r5_h11',   87, 4.5, 6.5],
  ['grib_z7_s87r7_h29',   87, 6.5, 8.5],
  ['grib_z13_s87r13_h38', 87, 12.4, 14.2],
  ['grib_z21_s88r3_h33',  88, 2.4, 4.4],
  ['grib_z30_s88r12_h66', 88, 11.4, 13.4],
  ['grib_z32_s89r2_h72',  89, 1.5, 3.5],
  ['grib_z50_s90r6_h28',  90, 5.5, 7.5],
  ['grib_z61_s91r1_h65',  91, 0.02, 2.6],
  ['grib_z62_s91r2_h2',   91, 1.4, 3.4],
  ['grib_z67_s91r7_h8',   91, 6.4, 8.4],
];

for (const [name, sken, r0, r1] of JOBS) {
  const n = n_vrst_map[sken] ?? 13;
  const h = (YT.b - YT.a) / n;
  const y0 = Math.max(0.0, YT.a + (r0 - 1) * h);
  const y1 = Math.min(0.998, YT.a + (r1 - 1) * h);
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  const top = Math.round(y0 * meta.height);
  const width = Math.round(0.78 * meta.width);
  const height = Math.max(40, Math.round(y1 * meta.height) - top);
  const out = `${TMP}/krop-grib/${name}.png`;
  await sharp(`${TMP}/s${sken}.jpg`)
    .extract({ left: 0, top, width, height })
    .resize({ width: Math.min(Math.round(width * 1.7), 1600) })
    .png()
    .toFile(out);
  console.log('OK', name, `y=${y0.toFixed(3)}–${y1.toFixed(3)}`);
}
console.log(`SKUPAJ: ${JOBS.length} kropov`);
