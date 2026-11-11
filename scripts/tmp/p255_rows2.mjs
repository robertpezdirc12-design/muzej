import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p255';
const zai = await ZAI.create();

const PROMPT = `Slika je ENA CELA VRSTICA (razprti list, širina = 2 strani) poročne knjige Trauungs-Buch 01738 (Podzemelj, ZAČETEK knjige, leto 1828, Kurrent-pisava, natisnjena tabularna glava zgoraj ALI čista vrstica). LEVA polovica = datum, ženin (Wohn-ort vas + hiša, ime, Stand, starost) in nevesta (isto). DESNA polovica = starši ženina (Eltern des Bräutigams: oče + mati), starši neveste, priče (Zeugen), Urkunden (dispense/soglasja), podpis duhovnika (navpičen na skrajnem desnem robu — lahko je odrezan).
PREPIŠI znak-za-znakom VSAKOLIKO vidno polje te vrstice. Leto = 1828. Stand lahko je: Bauer, ½ Bauer, ¼ Gütl, ½ Gütl, lediger, Inmann,=inw..
Izhod SAMO JSON: {"marg":"","datum":"","zenin":{"vas_hisa":"","ime":"","status":"","starost":""},"nevesta":{"vas_hisa":"","ime":"","starost":""},"starsi_zenin":{"oce":"","mati":""},"starsi_nevesta":{"oce":"","mati":""},"price":"","urkunde":"","duhovnik":"","opombe":""}`;

async function run(tag) {
  const out = `${DIR}/fullb_${tag}.json`;
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
const tags = ['s2_r1','s2_r2','s2_r3','s2_r4','s2_r5','s2_r6','s2_r7','s2_r8','s2_r9','s3_r1','s3_r2','s3_r3','s3_r4','s3_r5','s3_r6','s3_r7'];
for (const t of tags) await run(t);
