import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const PROMPT = `Slika: ×5 povečana datumski celica poročne knjige 01738 (Podzemelj), Kurent-pisava. Prepiši NATANČNO vsak znak: letnica / dan / mesec / ditto. Kurent številke: 1=črt, 2=zanka, 3=flat-top, 4=odprt-krož, 5=spodnja-zanka, 6=odprta-zanka, 7=črt+s prečko, 8=dvojna-zanka, 9=zanka+rep, 0=krož. Pozor: 'den 4.' pomeni 'dne 4.'. NE ugibaj — nejasno OZNAČI [~]. Izhod SAMO JSON: {"zapis":"","dan":null,"mesec":"","leto":null,"razlaga":""}`;
for (const id of ['s4r2_dt2','s4r3_dt2','s4r4_dt2','s4r5_dt2','s5r4_dt2','s5r5_dt2']) {
  const out = `/tmp/p256/D/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); continue; }
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`/tmp/p256/D/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({ messages: [{ role: 'user', content }], temperature: 0.1, max_tokens: 600, thinking: { type: 'disabled' } });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      break;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,3000)); }
  }
  await new Promise(r=>setTimeout(r,800));
}
