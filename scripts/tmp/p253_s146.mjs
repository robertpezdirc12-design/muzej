import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p253';
const zai = await ZAI.create();

const P1 = `Slika je ZADNJA content-stran poročne knjige Trauungs-Buch 01738 (Podzemelj, 1828–1873) — konec knjige. Knjiga se fizično konča s tem listom. Vprašanja:
1) Katere vrstice/tablične vrstice so FIZIČNO ZAPISANE (črnilo na tej strani) in katere so le PROSOJNI ODTIS z naslednje/prejšnje strani (bleščanje skozi papir)?
2) Prepiši VSE fizično zapisane vrstice: marginala, datum, ženin, nevesta (ime+priimek+vas+hiša).
3) Ali je to KONEC tabele (zadnji vpis leta 1873 v tej knjigi) in katera je številka ZADNJEGA vpisa?
Izhod SAMO JSON: {"fizicne_vrstice":[...],"prosojni_odtisi":"...","zadnji_vpis_st":"","razlaga":"..."}`;

const P2 = `Slika je pas ( trak) zadnje strani poročne knjige 01738 (1873, Kurrent). Prepiši FIZIČNO zapisano vrstico (marginala, datum, ženin+vas+hiša, nevesta+vas+hiša). Ignoriraj bleščanje oz. prosojne odtise z druge strani papirja.
Izhod SAMO JSON: {"marg":"","datum":"","zenin":"","nevesta":"","opomba":""}`;

async function ask(id, prompt, file) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: prompt }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(file).toString('base64')}` } });
  for (let a = 1; a <= 5; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1300, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      await new Promise(r2=>setTimeout(r2,9000));
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,12000)); }
  }
  console.log(`${id}: FAIL`);
}
await ask('s146_page', P1, `${DIR}/full/s146_Lpage.jpg`);
await ask('s146_b1', P2, `${DIR}/full/s146_b1.jpg`);
await ask('s146_b2', P2, `${DIR}/full/s146_b2.jpg`);
await ask('s146_b3', P2, `${DIR}/full/s146_b3.jpg`);
await ask('s146_b4', P2, `${DIR}/full/s146_b4.jpg`);
await ask('s146_b5', P2, `${DIR}/full/s146_b5.jpg`);
await ask('s146_b6', P2, `${DIR}/full/s146_b6.jpg`);
await ask('s146_b7', P2, `${DIR}/full/s146_b7.jpg`);
