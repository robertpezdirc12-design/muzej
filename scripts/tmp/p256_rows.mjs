import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p256/full';
const zai = await ZAI.create();

const ROWS = [];
for (const [tag, n] of [['s4', 9], ['s5', 8], ['s6', 11], ['s7', 13]])
  for (let i = 1; i <= n; i++) ROWS.push(`${tag}_r${i}`);

const PROMPT = `Slika je POVEČAN IZREZ (vodoravni trak) poročne knjige Trauungs-Buch 01738 (Podzemelj, 1829–1831, Kurrent-pisava, nemško). Trak obsega ENO vrstico vpisa (ali del dveh — loči po vodoravnih črtah!).
Stolpci leve strani: [Jahr,Monat,Tag der Trauung] [Wohn-ort] [Haus-Nr] [Taufname, Familien-Name, Stand ženina] [Religion] [Stan?] [Alter] [Zeuge1?] [Zeuge2?] | [Wohn-ort neveste] [Haus-Nr] [Taufname, Familien-Name, Stand neveste] [Religion] [Stan] [Alter] [Zeuge?] [Zeuge?]
Stolpci desne strani: [Eltern des Bräutigams: Taufname+Stand / Tauf+Fam.Name der Mutter] [Eltern der Braut] [Zeugen: Tauf- und Familien-Nahme + Stand] [Stand] [Urkunden] [Unterschrift des trauenden Priesters]
Prepiši vrstico (ali vrstici) po stolpcih — popolnoma dobesedno, vključno z okrajšavami. Oznči nejasna branja z [~]. Prekrižani/izbrisani deli: označi (prekrižano).
Izhod SAMO JSON: {"vrste":[{"datum":"","vasZenin":"","hisZenin":"","zenin":"","star":"", "letoZenin":0,"vasNevesta":"","hisNevesta":"","nevesta":"","starNevesta":0,"oceZenin":"","mataZenin":"","oceNevesta":"","mataNevesta":"","price":"","urkunde":"","duhovnik":"","xOpen":[]}],"razlaga":""}`;

async function run(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
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
for (const id of ROWS) { await run(id); await new Promise(r=>setTimeout(r,1200)); }
