import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();

// 1) PAGINACIJA: zgornji rob vsakega skena — katera 'Pag.' številka (svinčnik) je na LEVI in DESNI strani?
const PAG = `Slika je ZGORNJI ROB (pas 130 px, povečan ×2) skena razprtega lista (dve strani) poročne knjige Trauungs-Buch 01738.
Na sredini je tiskana glava; ZGORAJ LEVO nad levo stranjo in ZGORAJ (ob sredini/desno) nad desno stranjo so lahko SVINČNIKOVE foliacijske številke (ročno zapisane, npr. '19', '20', '21'...).
Previdno preberi VSE številke/pisma, ki jih vidiš na zgornjem robu, in njihov približen položaj (levo/sredina/desno). Ne ugibaj — če ni številke, reci 'ni'.
Izhod SAMO JSON: {"levo":"","sredina":"","desno":"","opis":""}`;

// 2) DATUMSKI-STOLPEC: zaporedje datumov po vrsticah
const DAT = (pag) => `Slika je DATUMSKI STOLPEC (x≈60–240, polna višina, povečan ×4) strani ${pag} poročne knjige 01738 (Kurrent).
Prepiši ZAPOREDJE datumov OD ZGORAJ DOL: za vsako vrstico z vpisom podaj dan + mesec (nemško: Febr, März, April, Mai, Juni, Juli, Aug(ust), 7ber/9ber/8ber, Oct, Nov, Dec, Jänner...). 'd°' ali dito = isti datum kot prejšnja vrstica. Letnice (1833/1834) so zapisane občasno — prepiši kje.
Izhod SAMO JSON: {"rows":[{"r":1,"datum":"","leto":null}],"razlaga":""}`;

async function ask(id, prompt, file) {
  const out = `/tmp/p259/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 30) { console.log(`${id}: skip`); return JSON.parse(fs.readFileSync(out, 'utf-8')); }
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
      return r.choices[0].message.content;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,60)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}

for (const s of [11, 12, 13]) {
  await ask(`pag_s${s}`, PAG, `/tmp/p259/hdr_s${s}.jpg`);
  await ask(`datcol_s${s}`, DAT(`s${s} (nepoznana Pag. — pričakovano Pag. ${2*s-3}/${2*s-2})`), `/tmp/p259/dates_full_s${s}.jpg`);
  await new Promise(r => setTimeout(r, 1200));
}
