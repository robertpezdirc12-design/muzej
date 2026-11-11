import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const DIR = '/tmp/p256/L';

const PGROOM = `Slika: del tabele poročne knjige 01738 (Podzemelj), Kurent-pisava, ×3 povečava. Vidni stolpci: DATUM (Jahr/Monat/Tag — letnica napisana enkrat, mesec enkrat, nato ditto: 'und 4.'='den 4.', '//', 'dto', 'ejusd.'), VAS ženina, HIŠA ženina (številka), IME ženina (ime+priimek+stand/poklic), nato številski stolpči (stan/starost).
Prepiši ZGORAJ DOL vsako vrstico tabele, ki vsebuje vpis. Za vsako:
- datum (danes prepisano — dobesedno, npr. '1829 / 18 Jän', 'und 4.', '17', '(prazna)')
- vas ženina, hiša ženina (številka!), ime ženina (ime + priimek + pripis)
- starost ženina (številka v stolpcu Alter, če vidna)
Nejasno OZNAČI [~]. NE ugibaj imen. Prazne vrstice izpusti.
Izhod SAMO JSON: {"vrstice":[{"datum":"","vas":"","hisa":null,"ime":"","starost":null,"opomba":""}],"razlaga":""}`;

const PBRIDE = `Slika: desni del LEVE strani razprtega lista poročne knjige 01738 (Podzemelj), Kurent-pisava, ×3. Stolpci tu: (konec ženinovih številskih stolpcev), VAS neveste, HIŠA neveste, IME neveste (ime+priimek+stand), številski (stan/starost neveste), lahko priče.
Prepiši ZGORAJ DOL vsako vrstico z vpisom. Za vsako: vas neveste, hiša neveste (številka), ime neveste, starost neveste (številka), morebitne priče.
Nejasno OZNAČI [~]. NE ugibaj. Izhod SAMO JSON: {"vrstice":[{"vas":"","hisa":null,"ime":"","starost":null,"price":"","opomba":""}],"razlaga":""}`;

const JOBS = [];
for (const t of ['s4','s5','s6','s7']) {
  for (const h of ['T','B']) {
    JOBS.push({ id: `${t}_G${h}`, prompt: PGROOM });
    JOBS.push({ id: `${t}_B${h}`, prompt: PBRIDE });
  }
}

async function run(j) {
  const out = `${DIR}/${j.id}.json`;
  if (fs.existsSync(out)) { console.log(`${j.id}: skip`); return; }
  const content = [{ type: 'text', text: j.prompt }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${j.id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({ messages: [{ role: 'user', content }], temperature: 0.1, max_tokens: 2200, thinking: { type: 'disabled' } });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${j.id}: OK`);
      return;
    } catch (e) { console.log(`${j.id}: a${a} ${String(e).slice(0,60)}`); await new Promise(r2=>setTimeout(r2,3500)); }
  }
  console.log(`${j.id}: FAIL`);
}
for (const j of JOBS) { await run(j); await new Promise(r=>setTimeout(r,1200)); }
