import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const DIR = '/tmp/p257';

const PROMPT = `Slika je CELA LEVA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), leto 1831, Kurrent-pisava, nemško. Stran vsebuje zaporedne vpise (vrstice) porok.
Naloga — ŠTETJE VRSTIC (census): preštej VSE vpise na strani in za VSAKEGA podaj:
1) zaporedno številko (1 = zgoraj),
2) DATUM vpisa (dan. mesec),
3) ime ŽENINA (le krstno ime, priimek okrajšaj) + njegovo hišno številko,
4) ime NEVESTE + njeno hišno številko.
Pazi: vrstice so lahko dvovrstične (pisanje čez dve mrežni vrstici) — štej VPIS, ne mrežno vrstico! Prazne mrežne vrstice ne štej.
Izhod SAMO JSON: {"stevilo":N,"rows":[{"r":1,"datum":"...","zenin":"ime+his","nevesta":"ime+his"}],"dvojvrsticne":[r,...],"opomba":"..."}`;

const PROMPT2 = `Slika je CELA DESNA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemelj), leto 1831 — stolpci: Eltern des Bräutigams | Eltern der Braut | Zeugen | [Stand] | Urkunden | Unterschrift. Leva stran (ista višina vrstic) ima vpise 1831.
Naloga: preštej VSE vpise (vrstice) na strani in za VSAKOGA podaj zaporedno št. + ime OČETA ŽENINA (iz stolpca Eltern des Bräutigams, le prva oseba).
Izhod SAMO JSON: {"stevilo":N,"rows":[{"r":1,"oceZenina":"..."}],"opomba":"..."}`;

async function one(id, file, prompt) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: prompt }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(file).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1400, thinking: { type: 'disabled' },
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
im = Image.open('/tmp/p257/s7.jpg')
im.crop((40, 250, 1030, 1480)).save('/tmp/p257/s7_LEFT.jpg', quality=92)
im.crop((1030, 250, 2040, 1480)).save('/tmp/p257/s7_RIGHT.jpg', quality=92)
im2 = Image.open('/tmp/p257/s6.jpg')
im2.crop((40, 250, 1030, 1480)).save('/tmp/p257/s6_LEFT.jpg', quality=92)
im2.crop((1030, 250, 2040, 1480)).save('/tmp/p257/s6_RIGHT.jpg', quality=92)
print('ok')
"`);
await one('census_s7L', '/tmp/p257/s7_LEFT.jpg', PROMPT);
await one('census_s7R', '/tmp/p257/s7_RIGHT.jpg', PROMPT2);

const PROMPT6 = `Slika je CELA LEVA STRAN razprtega lista poročne knjige Trauungs-Buch 01738 (Podzemel). Zgornje 3 vpisi so leto 1829 (1. März / 5. Juli / 25. November), nato RESTART z letnico 1830 (12. Jänner) in vpisi 1830 do 30. Juni; spodaj prazno.
Naloga — CENSUS: preštej VSE vpise na strani in za VSAKEGA podaj: zaporedno št., DATUM, ime ŽENINA + hišno številko, ime NEVESTE + hišno številko. Označi, kje je točno meja 1829/1830 (katere vpisi so 1829, kateri 1830) in ali je spodnja polovica (julij–december 1830) res PRAZNA.
Izhod SAMO JSON: {"stevilo":N,"restart_kje":"...","rows":[{"r":1,"datum":"...","zenin":"ime+his","nevesta":"ime+his"}],"spodaj_prazno":"...","opomba":"..."}`;
await one('census_s6L', '/tmp/p257/s6_LEFT.jpg', PROMPT6);
