// P227 krop — KROP-dokazi (krstna 04104, leto 1879 = 7/15!):
// DUELI hiš: z33 (19↔49!), z61 (22↔72!), z69 (17↔19!) + Griblje-vrstice ×21
// DVOJČKI-vrstice: z47/48 (Krasinec-h43!), z55/56 (Krasinec-h32!), z65/66 (Zemelj-h24!)
// TODTGEBOREN-garble: z15, z57, z66 + z60-sub-conditione + z32-imenski-popravek + z76-datum-anomalija
// MEJA: s106-vsotna-'1/8/7/9' + restart-z1 + 'Jahr 1878'-glava-patch
// FOLIACIJA + ZAP-STOLPCI (ordinalna-linija z1–z96!)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p227';
fs.mkdirSync(`${TMP}/krop-grib`, { recursive: true });
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0.toFixed(3)}-${y1.toFixed(3)} x${x0}-${x1}`);
}
// geometrije: razprti-listi; ytop 0.165; B = (0.975−0.165)/n-fizičnih-vrstic
const N = { 106: 8, 107: 8, 108: 7, 109: 7, 110: 6, 111: 6, 112: 7, 113: 7, 114: 7, 115: 8, 116: 8, 117: 7, 118: 8, 119: 5 };
const YT = 0.165, YB = 0.975;
function row(sken, idx0) { const B = (YB - YT) / N[sken]; const y0 = YT + idx0 * B; return [y0 - 0.012, y0 + B + 0.012]; }

const args = process.argv.slice(2);
const ONLY = args.length ? args : null;
async function maybe(name, fn) { if (ONLY && !ONLY.includes(name)) return; await fn(); }

// --- FOLIACIJA (gola-svinčna-'sken−6'!) ---
for (const p of [106,107,108,109,110,111,112,113,114,115,116,117,118]) await maybe(`arb_s${p}_pag`, () => crop(`arb_s${p}_pag`, p, 0.02, 0.17, 0.02, 0.42, 3.2));

// --- MEJA s106 (VSOTNA-razpeta-'1/8/7/9' + restart-z1 + glava-patch!) ---
await maybe('arb_s106_meja', () => crop('arb_s106_meja', 106, 0.02, 0.99, 0.02, 0.62, 2.6));
await maybe('arb_s106_vsotna', () => crop('arb_s106_vsotna', 106, 0.60, 0.80, 0.02, 0.62, 3.4));

// --- Griblje-vrstice (21!) — celotna-vrstica (levo-identifikacija + desno-starši-botri) ---
const GRIB = [ [106, 6], [108, 0], [108, 2], [109, 2], [109, 3], [109, 4], [109, 5], [110, 3], [110, 5], [111, 2], [113, 0], [113, 5], [115, 1], [115, 3], [116, 0], [116, 6], [117, 1], [118, 1], [118, 7], [119, 0], [119, 3] ];
for (let i = 0; i < GRIB.length; i++) {
  const [p, idx] = GRIB[i];
  await maybe(`g${i}_s${p}_r${idx}`, () => { const [y0, y1] = row(p, idx); return crop(`g${i}_s${p}_r${idx}`, p, y0, y1, 0.02, 0.99, 3.6); });
}

// --- DUELI-hiš (celica!) ---
await maybe('duel_z33_hisna', () => { const [y0, y1] = row(111, 2); return crop('duel_z33_hisna', 111, y0, y1, 0.20, 0.30, 7.0); });
await maybe('duel_z61_hisna', () => { const [y0, y1] = row(115, 1); return crop('duel_z61_hisna', 115, y0, y1, 0.20, 0.30, 7.0); });
await maybe('duel_z69_hisna', () => { const [y0, y1] = row(116, 0); return crop('duel_z69_hisna', 116, y0, y1, 0.20, 0.30, 7.0); });

// --- DVOJČKI-vrstice (ime-stolpec + zap!) ---
await maybe('dvojcki_z47z48', () => { const [y0, y1] = row(113, 3); return crop('dvojcki_z47z48', 113, y0, y1, 0.02, 0.45, 4.2); });
await maybe('dvojcki_z55z56', () => { const [y0, y1] = row(114, 3); return crop('dvojcki_z55z56', 114, y0, y1, 0.02, 0.45, 4.2); });
await maybe('dvojcki_z65z66', () => { const [y0, y1] = row(115, 5); return crop('dvojcki_z65z66', 115, y0, y1, 0.02, 0.45, 4.2); });

// --- TODTGEBOREN-garble (ime-stolpec!) ---
await maybe('todt_z15', () => { const [y0, y1] = row(108, 4); return crop('todt_z15', 108, y0, y1, 0.20, 0.50, 5.0); });
await maybe('todt_z57', () => { const [y0, y1] = row(114, 4); return crop('todt_z57', 114, y0, y1, 0.20, 0.50, 5.0); });

// --- z60-POGOJNI-KRST (pripis!) + z32-imenski-popravek + z76-datum-anomalija ---
await maybe('z60_subcond', () => { const [y0, y1] = row(115, 0); return crop('z60_subcond', 115, y0, y1, 0.02, 0.99, 3.8); });
await maybe('z32_imepopravek', () => { const [y0, y1] = row(111, 1); return crop('z32_imepopravek', 111, y0, y1, 0.02, 0.50, 4.6); });
await maybe('z76_datum', () => { const [y0, y1] = row(116, 7); return crop('z76_datum', 116, y0, y1, 0.02, 0.50, 4.6); });

// --- ZAP-STOLPCI (ordinalna-linija!) — vzorčni + kritični ---
for (const p of [106, 112, 113, 114, 115]) await maybe(`s${p}_zap_stolpec`, () => crop(`s${p}_zap_stolpec`, p, 0.05, 0.99, 0.02, 0.115, 5.0));

// --- MESEC-STOLPCI (chronologija!) ---
for (const p of [109, 112, 115, 118]) await maybe(`s${p}_mesec_stolpec`, () => crop(`s${p}_mesec_stolpec`, p, 0.10, 0.99, 0.02, 0.42, 4.0));

// --- PODPISI (duhovnik-izmenjava! vzorci) ---
const SIG = [ [107, 1, 'z4_dovgan'], [107, 2, 'z5_dovgan'], [108, 5, 'z16_dovgan'], [112, 0, 'z37_dovgan'], [112, 2, 'z39_dovgan'], [119, 3, 'z95_dovgan'], [107, 0, 'z3_janicar'], [112, 1, 'z38_janicar'], [119, 0, 'z92_janicar'] ];
for (const [p, idx, name] of SIG) await maybe(`sig_${name}`, () => { const [y0, y1] = row(p, idx); return crop(`sig_${name}`, p, y0, y1, 0.80, 1.0, 5.5); });

console.log('KROPI KONČANI');
