import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p255';
const zai = await ZAI.create();

const PROMPT = `Slika je ENA CELA VRSTICA (razprti list, širina = 2 strani) poročne knjige Trauungs-Buch 01738 (Podzemelj, ZAČETEK knjige, leto 1828, Kurrent-pisava, natisnjena tabularna glava). LEVA polovica = začetni stolpci (marginalna št., datum Trauung, ženin: Wohn-ort [VAS + hišna št.], Aufnahme [ime + Stand — Bauer/½ gzeit/lediger...], starost, nevesta: isto), DESNA polovica = nadaljevalni stolpci (starši oče+mati za oba, priče [Zeugen], Urkunden [dispense/soglasja], podpis duhovnika).
PREPIŠI znak-za-znakom VSAKOLIKO vidno polje te vrstice. Pazi Kurrent: 'Jänner'=Januar, '½ gzeit'=half-farmer, 'g.'=guzil/gospod. Leto je 1828 (ali morda 1829 če je to zadnja vrstica). Duhovnik 1828 NI Dovgan — prepiši podpis kakor je.
Izhod SAMO JSON: {"marg":"","datum":"","zenin":{"vas_hisa":"","ime":"","status":"","starost":""},"nevesta":{"vas_hisa":"","ime":"","status":"","starost":""},"starsi_zenin":{"oce":"","mati":""},"starsi_nevesta":{"oce":"","mati":""},"price":"","urkunde":"","duhovnik":"","opombe":""}`;

async function run(tag) {
  const out = `${DIR}/full_${tag}.json`;
  if (fs.existsSync(out)) { console.log(`${tag}: skip`); return; }
  const f = `${DIR}/full/${tag}.jpg`;
  const content = [{ type: 'text', text: PROMPT }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(f).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1400, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${tag}: OK`);
      return;
    } catch (e) { console.log(`${tag}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${tag}: FAIL`);
}
const tags = ['s2_m1','s2_m2','s2_m3','s2_m4','s2_m5','s2_m6','s2_m7','s2_m8','s3_m1','s3_m2','s3_m3','s3_m4','s3_m5','s3_m6','s3_m7'];
for (const t of tags) await run(t);
