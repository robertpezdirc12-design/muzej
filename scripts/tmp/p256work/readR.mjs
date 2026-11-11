import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const PROMPT = `Slika: DESNA STRAN razprtega lista poročne knjige 01738 (Podzemelj, 1829/1830), Kurent-pisava, ×1.8. Stolpci: [Eltern des Bräutigams: oče + mati (roj. priimek)] [Eltern der Braut: oče + mati] [Zeugen/priče] [Urkunden] [Unterschrift des trauenden Priesters].
Prepiši ZGORAJ DOL vsako vrstico: starši ženina, starši neveste, priče, urkunde, duhovnik (podpis). Nejasno OZNAČI [~]. NE ugibaj.
Izhod SAMO JSON: {"vrstice":[{"oceZenina":"","mataZenina":"","oceNeveste":"","mataNeveste":"","price":"","urkunde":"","duhovnik":""}],"razlaga":""}`;
for (const id of ['s4_R1','s5_R1','s6_R1']) {
  const out = `/tmp/p256/R/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); continue; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`/tmp/p256/R/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({ messages: [{ role: 'user', content }], temperature: 0.1, max_tokens: 2400, thinking: { type: 'disabled' } });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      break;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,3000)); }
  }
  await new Promise(r=>setTimeout(r,800));
}
