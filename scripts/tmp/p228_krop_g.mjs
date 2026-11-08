// P228 krop — celotna serija: 16-GRIBLJE-vrstic + DUELI + DVOJČKI + garble + RESTART + podpisi + zap + foliacija
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p228';
fs.mkdirSync(`${TMP}/krop-g`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-g/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
const N = { 92: 6, 93: 7, 94: 6, 95: 7, 96: 7, 97: 6, 98: 8, 99: 8, 100: 7, 101: 8, 102: 8, 103: 7, 104: 10 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.010, y0 + B + 0.010]; }

const args = process.argv.slice(2);
const ONLY = args.length ? args : null;
async function maybe(name, fn) { if (ONLY && !ONLY.includes(name)) return; await fn(); }

// --- 16 GRIBLJE-vrstic (celotna vrstica: levo-identifikacija + desno-starši/botri) ---
const GRIB = [
  ['z23', 96, 2], ['z24', 96, 3], ['z27', 96, 6],
  ['z28', 97, 0], ['z29', 97, 1], ['z30', 97, 2], ['z31', 97, 3],
  ['z45', 99, 3], ['z46', 99, 4],
  ['z52', 100, 2], ['z53', 100, 3], ['z56', 100, 6],
  ['z64', 101, 7],
  ['z65', 102, 0], ['z69', 102, 4],
  ['z81', 104, 1],
];
for (const [z, p, idx] of GRIB) await maybe(`g_${z}`, () => { const [y0, y1] = row(p, idx); return crop(`g_${z}`, p, y0, y1, 0.02, 0.99, 3.4); });

// --- DUELI-hiš (celica!) — h33 (z45/z56), h43 (z23/z31), h11 (z28/z29), h64 (z46/z81) ---
await maybe('duel_z45_h33', () => { const [y0, y1] = row(99, 3); return crop('duel_z45_h33', 99, y0, y1, 0.185, 0.29, 7.0); });
await maybe('duel_z56_h33', () => { const [y0, y1] = row(100, 6); return crop('duel_z56_h33', 100, y0, y1, 0.185, 0.29, 7.0); });
await maybe('duel_z23_h43', () => { const [y0, y1] = row(96, 2); return crop('duel_z23_h43', 96, y0, y1, 0.185, 0.29, 7.0); });
await maybe('duel_z31_h43', () => { const [y0, y1] = row(97, 3); return crop('duel_z31_h43', 97, y0, y1, 0.185, 0.29, 7.0); });
await maybe('duel_z28_h11', () => { const [y0, y1] = row(97, 0); return crop('duel_z28_h11', 97, y0, y1, 0.185, 0.29, 7.0); });
await maybe('duel_z29_h11', () => { const [y0, y1] = row(97, 1); return crop('duel_z29_h11', 97, y0, y1, 0.185, 0.29, 7.0); });
await maybe('duel_z46_h64', () => { const [y0, y1] = row(99, 4); return crop('duel_z46_h64', 99, y0, y1, 0.185, 0.29, 7.0); });
await maybe('duel_z81_h64', () => { const [y0, y1] = row(104, 1); return crop('duel_z81_h64', 104, y0, y1, 0.185, 0.29, 7.0); });

// --- SPECIALNE: z28-garble-nichtlebendgeburt (ime!) ---
await maybe('garble_z28_ime', () => { const [y0, y1] = row(97, 0); return crop('garble_z28_ime', 97, y0, y1, 0.29, 0.62, 6.0); });
// z87/z88-DVOJČKI-kandidat (2-vrstici + vas-popravek!)
await maybe('dvojcki_z87z88', () => { const [y0, y1] = row(104, 7); const [, y2] = row(104, 8); return crop('dvojcki_z87z88', 104, y0 - 0.005, y2 + 0.005, 0.02, 0.62, 4.0); });
// z46-datum-korekcija (Juni 30 → Juli 1) + MODRI
await maybe('z46_datum', () => { const [y0, y1] = row(99, 4); return crop('z46_datum', 99, y0, y1, 0.02, 0.35, 5.0); });
// NEZAKONSKI-kandidati: z9 (s94 r1), z13 (s94 r5), z36 (s98 r2), z63 (s101 r6)
await maybe('nez_z9', () => { const [y0, y1] = row(94, 1); return crop('nez_z9', 94, y0, y1, 0.02, 0.99, 3.4); });
await maybe('nez_z13', () => { const [y0, y1] = row(94, 5); return crop('nez_z13', 94, y0, y1, 0.02, 0.99, 3.4); });
await maybe('nez_z36', () => { const [y0, y1] = row(98, 2); return crop('nez_z36', 98, y0, y1, 0.02, 0.99, 3.4); });
await maybe('nez_z63', () => { const [y0, y1] = row(101, 6); return crop('nez_z63', 101, y0, y1, 0.02, 0.99, 3.4); });
// z60-✠-margina + †8.3.1972
await maybe('z60_kriz', () => { const [y0, y1] = row(101, 5); return crop('z60_kriz', 101, y0 - 0.03, y1 + 0.03, 0.02, 0.45, 4.2); });
// s105-LEPLJENEC (dokument!)
await maybe('s105_lepljenec', () => crop('s105_lepljenec', 105, 0.32, 0.68, 0.05, 0.55, 3.0));

// --- RESTART-z1 (s93 r0 — mega: mesec+dan+vas+hisna) ---
await maybe('restart_z1', () => { const [y0, y1] = row(93, 0); return crop('restart_z1', 93, y0 - 0.045, y1 + 0.02, 0.02, 0.55, 4.4); });

// --- ZAP-STOLPCI (ordinalna-linija: s93-restart + s104-10-vrstic + s99-'34-42') ---
for (const [p, tag] of [[93, 'restart'], [104, 'z80-89'], [99, 'z42-49'], [106, 'tail']]) await maybe(`zap_s${p}`, () => crop(`zap_s${p}`, p, 0.10, 0.99, 0.02, 0.115, 4.6));

// --- PODPISI (alternacija! Griblje-vrstice + vzorci) ---
const SIG = [
  ['z23_dovgan', 96, 2], ['z31_dovgan', 97, 3], ['z30_dovgan', 97, 2],
  ['z45_janicar', 99, 3], ['z46_janicar', 99, 4], ['z52_janicar', 100, 2],
  ['z56_dovgan', 100, 6], ['z64_dovgan', 101, 7], ['z65_dovgan', 102, 0],
  ['z69_dovgan', 102, 4], ['z81_janicar', 104, 1], ['z24_krop', 96, 3], ['z27_krop', 96, 6],
  ['z28_sig', 97, 0], ['z29_dovgan', 97, 1], ['z53_janicar', 100, 3],
];
for (const [nm, p, idx] of SIG) await maybe(`sig_${nm}`, () => { const [y0, y1] = row(p, idx); return crop(`sig_${nm}`, p, y0, y1, 0.86, 1.0, 5.5); });

// --- FOLIACIJA s96 (manjkajoča) + TEMNA-'34/94'-s99-MEGA ---
await maybe('fol_s96', () => crop('fol_s96', 96, 0.01, 0.13, 0.03, 0.22, 7.0));
await maybe('fol_s99_mega', () => crop('fol_s99_mega', 99, 0.01, 0.10, 0.04, 0.18, 10.0));

console.log('KROPI KONČANI');
