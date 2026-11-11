import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const DIR = '/tmp/p258';

const L8 = `Slika je CELA LEVA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Kurrent-pisava, nemško. Stran = Pag. 13, NADALJEVANJE leta 1831 (leta 1831 začetek: 26. Jänner + 1./9. Febr je na prejšnji strani Pag. 11).
Naloga — ŠTETJE VRSTIC (census): preštej VSE vpise na strani in za VSAKEGA podaj:
1) zaporedno številko (1 = zgoraj),
2) DATUM vpisa (dan. mesec — pozorno: prva vrstica je lahko 'd°' oz. nadaljevanje 9. Febr iz prejšnje strani!),
3) ime ŽENINA (krstno ime + priimek) + njegovo VAS in hišno številko,
4) ime NEVESTE + njeno VAS in hišno številko.
Pazi: vrstice so lahko dvovrstične — štej VPIS, ne mrežno vrstico! Prazne mrežne vrstice ne štej. Označi tudi letnico v glavi stolpca datuma.
Izhod SAMO JSON: {"stevilo":N,"leta_glava":"...","rows":[{"r":1,"datum":"...","zenin":"ime vas hisa","nevesta":"ime vas hisa"}],"opomba":"..."}`;

const R8 = `Slika je CELA DESNA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Pag. 14 — stolpci: Eltern des Bräutigams | Eltern der Braut | Zeugen | Urkunden | Unterschrift. Leva stran (ista višina vrstic) ima NADALJEVANJE vpisov leta 1831 (~11 vrstic, 9. Febr/14. Febr/6. Juni/24. Aug/Nov).
Naloga: preštej VSE vpise (vrstice) na strani in za VSAKOGA podaj zaporedno št. + ime OČETA ŽENINA (iz stolpca Eltern des Bräutigams, prva oseba) + pričo, če berljiv.
Izhod SAMO JSON: {"stevilo":N,"rows":[{"r":1,"oceZenina":"...","prica":"..."}],"opomba":"..."}`;

const L9 = `Slika je CELA LEVA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Kurrent-pisava, nemško. Stran = Pag. 15, RESTART letnice 1832 v glavi (prvi vpis 18. Jänner 1832).
Naloga — ŠTETJE VRSTIC (census): preštej VSE vpise na strani in za VSAKEGA podaj:
1) zaporedno številko (1 = zgoraj),
2) DATUM vpisa (dan. mesec; 'd°'/'tt°' = isti dan kot prejšnji),
3) ime ŽENINA + njegovo VAS in hišno številko,
4) ime NEVESTE + njeno VAS in hišno številko.
Pazi: vrstice so lahko dvovrstične — štej VPIS, ne mrežno vrstico! Prazne ne štej. Označi letnico v glavi in ali je kje RESTART letnice. Pozorno preberi Griblje/Grüble-hiše (22, 35, ...).
Izhod SAMO JSON: {"stevilo":N,"leta_glava":"...","restart_kje":"...","rows":[{"r":1,"datum":"...","zenin":"ime vas hisa","nevesta":"ime vas hisa"}],"opomba":"..."}`;

const R9 = `Slika je CELA DESNA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Pag. 16 — stolpci: Eltern des Bräutigams | Eltern der Braut | Zeugen | Urkunden | Unterschrift. Leva stran (ista višina vrstic) ima vpise leta 1832 (~15 vrstic: 18. Jän ×3 + 25. + 29. Jän + 15. Febr ×4 + 22. + 29. Febr ×5).
Naloga: preštej VSE vpise (vrstice) na strani in za VSAKOGA podaj zaporedno št. + ime OČETA ŽENINA + pričo, če berljiv.
Izhod SAMO JSON: {"stevilo":N,"rows":[{"r":1,"oceZenina":"...","prica":"..."}],"opomba":"..."}`;

const L10 = `Slika je CELA LEVA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Kurrent-pisava, nemško. Stran = Pag. 17, NADALJEVANJE leta 1832 (zgornje vrstice: 29. Febr 1832 + 5. März + 28. Mai + 20. Juni + 28. Nov), nato RESTART letnice 1833 (~5./6. Febr 1833) v spodnjem delu.
Naloga — ŠTETJE VRSTIC (census): preštej VSE vpise na strani in za VSAKEGA podaj:
1) zaporedno številko (1 = zgoraj),
2) DATUM vpisa (dan. mesec),
3) ime ŽENINA + njegovo VAS in hišno številko,
4) ime NEVESTE + njeno VAS in hišno številko.
Označi TOČNO, kje je meja 1832/1833 (katera vrstica je prva 1833 in kje piše letnica). Pazi: dvovrstični vpisi — štej VPIS, ne mrežno vrstico!
Izhod SAMO JSON: {"stevilo":N,"restart_kje":"...","rows":[{"r":1,"datum":"...","zenin":"ime vas hisa","nevesta":"ime vas hisa"}],"opomba":"..."}`;

const R10 = `Slika je CELA DESNA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), Pag. 18 — stolpci: Eltern des Bräutigams | Eltern der Braut | Zeugen | Urkunden | Unterschrift. Leva stran (ista višina vrstic) ima zgornje vpise 1832 (~8) + spodnje 1833 (~6).
Naloga: preštej VSE vpise (vrstice) na strani in za VSAKOGA podaj zaporedno št. + ime OČETA ŽENINA + pričo, če berljiv.
Izhod SAMO JSON: {"stevilo":N,"rows":[{"r":1,"oceZenina":"...","prica":"..."}],"opomba":"..."}`;

async function one(id, file, prompt) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: prompt }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(file).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1600, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
const { execSync } = await import('child_process');
execSync(`python3 -c "
from PIL import Image
for s, w in [(8, 2113), (9, 2100), (10, 2113)]:
    im = Image.open(f'/tmp/p258/s{s}.jpg')
    im.crop((40, 250, 1040, 1480)).save(f'/tmp/p258/s{s}_LEFT.jpg', quality=92)
    im.crop((1040, 250, w - 30, 1480)).save(f'/tmp/p258/s{s}_RIGHT.jpg', quality=92)
print('ok')
"`);
await one('census_s8L', `${DIR}/s8_LEFT.jpg`, L8);
await one('census_s8R', `${DIR}/s8_RIGHT.jpg`, R8);
await one('census_s9L', `${DIR}/s9_LEFT.jpg`, L9);
await one('census_s9R', `${DIR}/s9_RIGHT.jpg`, R9);
await one('census_s10L', `${DIR}/s10_LEFT.jpg`, L10);
await one('census_s10R', `${DIR}/s10_RIGHT.jpg`, R10);
