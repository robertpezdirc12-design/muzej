// P234 — branje ZAP-STRIPS + SUPER-zoomov (ground-truth zap-verige!).
import ZAI from 'file:///home/z/my-project/node_modules/z-ai-web-dev-sdk/dist/index.js';
import fs from 'fs';

const inst = await ZAI.create();
const DIR = '/tmp/p234/krops';

const TASKS = [
  { img: 'ZAP-STRIPS.png', out: 'zread-STRIPS.json', prompt: `To je 5-VERTIKALNIH-STRIPESIS (povečava ×3) ZAPorednih-številk iz KRSTNE matične knjige župnije Podzemelj (Kurrent-pisava, 1872–1873). Vsak strip = ZAPoredni-stolpec (najbolj-levo, ročno-zapisane-številke!) ENE STRANI tabele, od-zgoraj-navzdol (vse-vrstice-strani!).
STRIP-i: STRIP-s19 (9-vrstic!-pričakovano-1–9-ALI-51–59?!), STRIP-s25 (6-vrstic!-TAIL-leta!), STRIP-s26 (11-vrstic!-RESTART-na-1?-ALI-nadaljevanje?!), STRIP-s27 (10-vrstic!), STRIP-s28 (11-vrstic!).
★★★ CIFRE-KURRENT: '1' = ozka-črtica (lahko-s-serifom!-BREZ-zanke!-vs-'2'-ima-osnovo!), '3' = zrcalna-E, '4' = zanka, '5' = črta+zanka, '6' = zanka-gor, '7' = γ-s-prečko, '8' = dve-zanki, '9' = zanka+rep, '0' = oval.
★★★ ZNANE-KONTROLE: s28 = 11-vrstic-in-PRVA-vrstica-ima-MÄRZ (mesec-NI-v-stolpcu-ampak-poštevi-vrstice!); s31-iz-druge-slike (ne-vtem-shetu) = zadnja-številka-'51' (X-POTRJEN!).
ZA VSAK strip: preberi VSE zaporedne-številke-od-zgoraj-navzdol (tudi-če-so-nejasne!-najboljši-guess-s-[~]!-če-je-vrstica-BREZ-številke-napiši-null!).
Izhod: SAMO JSON: {"stripsi":[{"strip":"s19","stevilk":9,"zapi":["...","..."],"opomba":"..."}, ...]}` },
  { img: 'S28R1-SUPER.png', out: 'zread-S28R1.json', prompt: `To je SUPER-zoom (×4) PRVE-vrstice strani s28 krstne knjige Podzemelj (Kurrent-1873!). Viden: ZAPoredna-številka (skrajno-levo, ročno!) + mesec/dan + začetek-vasi + hišna-št.
ZNANO: ta-vrstica = 'März-3-Podzemelj-Mathildis' (P233-potrjeno!). VPRAŠANJE: katera-je-ZAPoredna-ŠTEVILKA?? Kandidati: '11' (P233-model!), '20' (P233-brano!), '22', '28' (P234-X-brano-visoko!).
★★★ KURRENT: '1' = ozka-črtica-s-serifom (BREZ-zanke!), '2' = osnova+zgornja-zanka, '8' = dve-zanki, '0' = oval-BREZ-repa. POZOR: popravki/prestriki-mogoči!
Izhod: SAMO JSON: {"zap":"...","zanesljivost":"visoko|srednje|nizko","analiza":"katera-cifra-kje (npr. 'prva-cifra-je-1-s-serifom', 'druga-cifra-je...')","mesec":"...","dan":"...","vas":"...","hisna":"..."}` },
  { img: 'S26R1-SUPER.png', out: 'zread-S26R1.json', prompt: `To je SUPER-zoom (×4) PRVE-vrstice strani s26 krstne knjige Podzemelj (Kurrent!). Viden: ZAPoredna-številka (skrajno-levo!) + mesec/dan + vas + hišna-št.
ZNANO: ta-vrstica = 'Jänner-3?-Gradac?-Anna' (brano!). VPRAŠANJE: (1) katera-je-ZAPoredna-ŠTEVILKA ('1'-restart?? '3'? drugo?), (2) kateri-MESEC (Jänner-z-J-zanko? Dezember-z-D? drug?), (3) dan?
★★★ KURRENT: '1' = ozka-črtica-s-serifom, '3' = zrcalna-E, 'J'-zanka-pri-Jänner, 'D'-pri-Dezember.
Izhod: SAMO JSON: {"zap":"...","zanesljivost":"visoko|srednje|nizko","mesec":"...","dan":"...","vas":"...","hisna":"...","otrok":"...","analiza":"..."}` },
];

for (const t of TASKS) {
  const outPath = `/tmp/p234/${t.out}`;
  if (fs.existsSync(outPath)) { console.log(`${t.img}: ŽE`); continue; }
  let done = false;
  for (let attempt = 1; attempt <= 4 && !done; attempt++) {
    try {
      const b64 = fs.readFileSync(`${DIR}/${t.img}`).toString('base64');
      const r = await Promise.race([
        inst.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: t.prompt },
            { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 240000))
      ]);
      const c = r?.choices?.[0]?.message?.content || '';
      const a = c.indexOf('{'), b = c.lastIndexOf('}');
      if (a < 0 || b < 0) throw new Error('ni JSON');
      const j = JSON.parse(c.slice(a, b + 1));
      fs.writeFileSync(outPath, JSON.stringify(j, null, 2));
      console.log(`${t.img}: OK`);
      console.log(JSON.stringify(j, null, 1).slice(0, 1600));
      done = true;
    } catch (e) {
      console.error(`${t.img}: poskus ${attempt} FAIL ${e.message.slice(0, 90)}`);
      if (/429|Too many/.test(e.message)) await new Promise(r2 => setTimeout(r2, 45000));
      else await new Promise(r2 => setTimeout(r2, 8000));
    }
  }
  if (!done) console.error(`${t.img}: KONČNO-FAIL`);
  await new Promise(r => setTimeout(r, 15000));
}
console.log('ZAP-STRIPS-READ-KONČANO');
