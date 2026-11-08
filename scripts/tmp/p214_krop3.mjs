// P214 krop-3 — TIGHT izrezi z VIZUALNO-kalibriranimi pasovi (s37/s36/s35/s39 templat: 
// hisna-col x0.21–0.235, ime x0.235–0.39, datum x0.02–0.16, Alter x0.51–0.58, bolezen x0.55–0.72,
// Anmerkung x0.88–1.0; vrstični centri: s35 z2≈0.60/vsota≈0.505; s36 z12≈0.355; s37 z27≈0.355/z38≈0.94; s39 z64≈0.69/vsota≈0.755)
import sharp from 'sharp';
import fs from 'fs';
const TMP = '/tmp/p214';
async function crop(name, sken, y0, y1, x0, x1, sc) {
  const meta = await sharp(`${TMP}/s${sken}.jpg`).metadata();
  await sharp(`${TMP}/s${sken}.jpg`).extract({ left: Math.round(x0*meta.width), top: Math.round(y0*meta.height), width: Math.round((x1-x0)*meta.width), height: Math.max(30, Math.round((y1-y0)*meta.height)) })
    .resize({ width: Math.min(Math.round((x1-x0)*meta.width*sc), 1800) }).png().toFile(`${TMP}/krop-grib/${name}.png`);
  console.log('OK', name, `s${sken} y${y0}-${y1} x${x0}-${x1}`);
}
// --- KRITIČNO: z27-hisna DUEL (11-vs-21-vs-31!) @6× ---
await crop('z27_hisna_tight', 37, 0.325, 0.385, 0.19, 0.26, 6.0);
await crop('z27_ime_tight2', 37, 0.325, 0.385, 0.22, 0.40, 5.0);
// --- z38: ime-2-vrstično (infans Rosalia v. Joh. Broz...) + Alter + bolezen ---
await crop('z38_ime_tight2', 37, 0.895, 0.978, 0.22, 0.40, 5.0);
await crop('z38_alter_tight', 37, 0.895, 0.978, 0.50, 0.60, 6.0);
await crop('z38_bolezen_tight', 37, 0.895, 0.978, 0.55, 0.74, 5.0);
// --- z12: bolezen-2-vrstično (desna stran!) + ime+stan + Anmerkung ---
await crop('z12_ime_stan_tight', 36, 0.318, 0.392, 0.22, 0.40, 5.0);
await crop('z12_bolezen_tight', 36, 0.318, 0.392, 0.54, 0.74, 5.0);
await crop('z12_opomba_tight', 36, 0.318, 0.392, 0.86, 1.0, 6.0);
// --- z2: ime-final (Kune!) + bolezen-final (desna!) ---
await crop('z2_ime_tight2', 35, 0.565, 0.635, 0.22, 0.40, 5.0);
await crop('z2_bolezen_tight2', 35, 0.565, 0.635, 0.54, 0.74, 5.0);
// --- VSOTNA = LETNICA-MARKER dokazi (2 instance!) ---
await crop('s35_vsota_tight', 35, 0.475, 0.545, 0.02, 0.50, 3.5);
await crop('s35_vsota_desno', 35, 0.475, 0.545, 0.50, 0.90, 3.5);
await crop('s39_vsota_tight', 39, 0.725, 0.795, 0.02, 0.50, 3.5);
await crop('s39_vsota_desno', 39, 0.725, 0.795, 0.50, 0.90, 3.5);
// --- z64 ULEDBA: eksplicitni-LETNICI (31.Dec 1863 | 2.Jän 1864!) @6× ---
await crop('z64_datumi_tight', 39, 0.655, 0.725, 0.02, 0.16, 6.0);
console.log('P214 krop pass-3: 14 izrezov');
