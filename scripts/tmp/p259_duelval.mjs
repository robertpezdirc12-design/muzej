// P259 — DUEL-VAL: neodvisna VLM validacija 9 preostalih duelov (s12_r5 že VLM-potrjen 2:1).
// Nevtralni pozivi (BREZ pričakovanih odgovorov) — primerjava z integriranim kasneje (p259_duelcmp.mjs).
// Izhodi: research/issue17/p259-work/duel-vals/<name>.json (repo — preživi /tmp wipe).
import fs from 'fs';
import path from 'path';
import ZAI from 'z-ai-web-dev-sdk';

const SRC = '/home/z/my-project/research/issue17/p259-work/duels';
const OUT = '/home/z/my-project/research/issue17/p259-work/duel-vals';
fs.mkdirSync(OUT, { recursive: true });

const COLS = `Kontekst: poročna knjiga Trauungs-Buch 01738 (Podzemelj/Gradiče, Kurrent-pisava, nemško, ~1833/34). Kompozit je navpični sklad povečanih izrezov; vsak izrez ima nad sabo BEL OZNAKOVNI TRAK z oznako band-a. Oznake so vprašanja alternativ — NISO odgovori: prepiši SAMO dobesedno tisto, kar vidiš v rokopisu.`;

const DUELS = [
  {
    name: 's11_dates',
    ask: `Sklad 13 izrezov = DATUMSKI STOLPEC vrstic 1–13 strani Pag. 19. Za VSAK band (VRSTICA 1 … VRSTICA 13) prepiši zapisani datum DOBESEDNO: dan + mesec + letnica (če je zapisana); opazi tudi d°/dito/preskočene vrstice in česar koli prečrtanega v robu. Izhod SAMO JSON: {"name":"s11_dates","rows":[{"r":1,"datum":"","leto":null,"opomba":""}, ... 13 vrstic],"razlaga":""}`,
  },
  {
    name: 's12_dates',
    ask: `Sklad 12 izrezov = DATUMSKI STOLPEC vrstic 1–12 strani Pag. 21 (konec 1833 + zelo začetek 1834, RESTART letnice). Za VSAK band (VRSTICA 1 … VRSTICA 12) prepiši zapisani datum DOBESEDNO: dan + mesec + letnica; pazi na d°/dito, prazne celice, PREČRTANE številke v robu in robovne številke (1., 2., …). Izhod SAMO JSON: {"name":"s12_dates","rows":[{"r":1,"datum":"","leto":null,"opomba":""}, ... 12 vrstic],"razlaga":""}`,
  },
  {
    name: 's13_dates',
    ask: `Sklad 11 izrezov = DATUMSKI STOLPEC vrstic 1–11 strani Pag. 23 (leto 1834, z robovnimi številkami 8–18). Za VSAK band (VRSTICA 1 … VRSTICA 11) prepiši zapisani datum DOBESEDNO: dan + mesec + letnica; zapiši TUDI robovno številko, če je vidna; pazi na d°/dito in sistematične vzorce (isti dan večkrat zapored). Izhod SAMO JSON: {"name":"s13_dates","rows":[{"r":1,"datum":"","leto":1834,"rob":null,"opomba":""}, ... 11 vrstic],"razlaga":""}`,
  },
  {
    name: 's11_r2_gosling',
    ask: `Sklad 4 izrezov = VRSTICA 2 strani Pag. 19: (1) ŽENIN-IME, (2) ŽENIN-VAS+HIŠNA ŠT., (3) NEVESTA-IME, (4) NEVESTA-VAS+HIŠNA ŠT. Prepiši vsak band DOBESEDNO črko za črko (Kurrent!); hišno številko preberi ZA ŠTEVILKO (pazi 3/5, 0/9). Izhod SAMO JSON: {"name":"s11_r2_gosling","zenin":"","vasZenin":"","hisZenin":0,"nevesta":"","vasNevesta":"","hisNevesta":0,"razlaga":""}`,
  },
  {
    name: 's12_r1_r2',
    ask: `Sklad 6 izrezov strani Pag. 21: VRSTICA 1 (žENIN-IME, žENIN-VAS+HIŠA, NEVESTA-IME, NEVESTA-VAS+HIŠA) + VRSTICA 2 (DATUM, ŽENIN-IME). Prepiši vsak band DOBESEDNO (Kurrent, črko za črko; datum = dan+mesec+letnica; hiša = številko za številko!). Izhod SAMO JSON: {"name":"s12_r1_r2","r1":{"zenin":"","vasZenin":"","hisZenin":0,"nevesta":"","vasNevesta":"","hisNevesta":0},"r2":{"datum":"","zenin":""},"razlaga":""}`,
  },
  {
    name: 's12_r7_restart',
    ask: `Sklad 5 izrezov = VRSTICA 7 strani Pag. 21: (1) DATUM, (2) ŽENIN-IME, (3) ŽENIN-VAS+HIŠA, (4) NEVESTA-IME, (5) NEVESTA-VAS+HIŠA. Prepiši DOBESEDNO; DATUM = dan + mesec + LETNICA (pazi — začetek novega leta!; prepiši tudi robovno številko, če je vidna). Izhod SAMO JSON: {"name":"s12_r7_restart","datum":"","leto":null,"rob":null,"zenin":"","vasZenin":"","hisZenin":0,"nevesta":"","vasNevesta":"","hisNevesta":0,"razlaga":""}`,
  },
  {
    name: 's13_r1_restart',
    ask: `Sklad 5 izrezov = VRSTICA 1 strani Pag. 23: (1) DATUM, (2) ŽENIN-IME, (3) ŽENIN-VAS+HIŠA, (4) NEVESTA-IME, (5) NEVESTA-VAS+HIŠA. Prepiši DOBESEDNO; DATUM = dan + mesec + letnica (pazi na d°/robovno številko). Izhod SAMO JSON: {"name":"s13_r1_restart","datum":"","leto":null,"rob":null,"zenin":"","vasZenin":"","hisZenin":0,"nevesta":"","vasNevesta":"","hisNevesta":0,"razlaga":""}`,
  },
  {
    name: 's13_r6_vrh',
    ask: `Sklad 4 izrezov = VRSTICA 6 strani Pag. 23: (1) ŽENIN-IME, (2) ŽENIN-VAS+HIŠNA ŠT., (3) NEVESTA-IME, (4) NEVESTA-VAS+HIŠNA ŠT. Prepiši DOBESEDNO črko za črko; HIŠNO ŠTEVILKO ZA ŠTEVILKO (pazi 5/6, 0/8 v Kurrentu!). Izhod SAMO JSON: {"name":"s13_r6_vrh","zenin":"","vasZenin":"","hisZenin":0,"nevesta":"","vasNevesta":"","hisNevesta":0,"razlaga":""}`,
  },
  {
    name: 's13_r11_marentic',
    ask: `Sklad 5 izrezov = VRSTICA 11 (ZADNJA) strani Pag. 23: (1) DATUM, (2) ŽENIN-IME, (3) ŽENIN-VAS+HIŠA, (4) NEVESTA-IME, (5) NEVESTA-VAS+HIŠA. Prepiši DOBESEDNO; DATUM = dan+mesec+letnica; hišno številko ZA ŠTEVILKO. Izhod SAMO JSON: {"name":"s13_r11_marentic","datum":"","leto":null,"rob":null,"zenin":"","vasZenin":"","hisZenin":0,"nevesta":"","vasNevesta":"","hisNevesta":0,"razlaga":""}`,
  },
];

const zai = await ZAI.create();
const only = process.argv[2] || null;

for (const d of DUELS) {
  if (only && d.name !== only) continue;
  const outF = path.join(OUT, `${d.name}.json`);
  if (fs.existsSync(outF) && fs.statSync(outF).size > 60) { console.log(`${d.name}: ze-veljavno (preskok)`); continue; }
  const img = path.join(SRC, `${d.name}.jpg`);
  if (!fs.existsSync(img)) { console.error(`${d.name}: MANJKA slika ${img}`); continue; }
  const content = [
    { type: 'text', text: `${COLS}\n\n${d.ask}` },
    { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(img).toString('base64')}` } },
  ];
  try {
    const r = await zai.chat.completions.createVision({
      messages: [{ role: 'user', content }],
      temperature: 0.1, max_tokens: 2200, thinking: { type: 'disabled' },
    });
    const c = (r.choices[0].message.content || '').trim();
    if (c.length < 40) { console.error(`${d.name}: prekratko (${c.length})`); continue; }
    fs.writeFileSync(outF, c);
    console.log(`${d.name}: OK (${c.length} znakov)`);
    await new Promise((res) => setTimeout(res, 3500)); // QPS 2 varno
  } catch (e) {
    console.error(`${d.name}: NAPAKA ${String(e).slice(0, 200)}`);
  }
}
console.log('DUEL-VAL DONE');
