import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();
const PROMPT = `Slika je CELA VRSTICA (razprti list, širina = 2 strani) poročne knjige Trauungs-Buch 01738 (Podzemelj, leto 1873, Kurrent-pisava). LEVA polovica = začetni stolpci (marginalna št., datum Copulati, ženin ime+status+starost+vas+hiša, nevesta isto), DESNA polovica = nadaljevalni stolpci (starši oče+mati za oba, priče, Urkunden, podpis duhovnika).
PREPIŠI znak-za-znakom VSAKOLIKO vidno polje te vrstice. Pazi Kurrent: 'b'≠'2', 'Jänner'='Januar', 'Mai'≠'März', '873'='1873'. Duhovnik = župnik Franz Dovgan (zapisan Dergan/Dorgan).
Izhod SAMO JSON: {"marg":"","datum":"","zenin":{"ime":"","status":"","starost":"","vas":"","hisa":""},"nevesta":{"ime":"","status":"","starost":"","vas":"","hisa":""},"starsi_zenin":{"oce":"","mati":""},"starsi_nevesta":{"oce":"","mati":""},"price":"","urkunde":"","duhovnik":"","opombe":""}`;
async function run(tag) {
  const out = `${DIR}/full_${tag}.json`;
  if (fs.existsSync(out)) { console.log(`${tag}: skip`); return; }
  const f = `${DIR}/full/${tag.replace('full_','')}.jpg`;
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(f).toString('base64')}` } });
  for (let a = 1; a <= 6; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1400, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${tag}: OK`);
      await new Promise(r2=>setTimeout(r2,12000));
      return;
    } catch (e) { console.log(`${tag}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,15000)); }
  }
  console.log(`${tag}: FAIL`);
}
for (const t of ['s144_m5','s144_m6','s144_m7','s144_m8','s144_m9']) await run(t);
