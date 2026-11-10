// P248 pass-4: VLM na 11 dopolnilnih mikro-kropih
import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';

const DIR = '/home/z/p248tmp';
const OUT = `${DIR}/pass248`;

const prompts = {
  's12-r8-hisnaB2': `ULTRA-ZOOM (8×) HIŠNE ŠTEVILKE neveste vpisa-8 na s12 poročne knjige (stolpec 'Haus-Nr.' DESNO od natisnjenega 'Wohnort' stolpca, v vrstici z ženinom 'Gri. šte. 35 Mathias Hrižan'). Kandidati: "64" ALI "19" ALI "6x". FORENZIKA: Kurrent "6" = spodnja zaprta zanka z zgornjim lokom; "1" = RAVNA padajoča poteza BREZ zanke; "4" = zaprta zanka z navzkrižnim drogom ali odprt h; "9" = zaprta zgornja zanka z dolgim spuščnim repom. Prepiši znak za znak in razloži OBE črki. {"id":"s12-r8-hisnaB2","stevilka":"...","prva":"opis","druga":"opis","odgovor":"...","zanesljivost":"...","note":"..."}`,
  's12-r6-wohnort': `ULTRA-ZOOM (4×) Wohnorta ŽENINA vpisa-6 na s12 (vrstica '1876. Febr. 16.', ženin Mathias Mohlorič[~] 28-l). Kandidati: "Gradac 36" ALI "Drašiče 36" (+ morda pripis 'pf. Möbling/Metlika'?). Prepiši znak za znak. {"id":"s12-r6-wohnort","wohnort":"...","hisna":"...","pripis":"...","odgovor":"...","note":"..."}`,
  's12-r7-wohnort': `ULTRA-ZOOM (4×) Wohnortov vpisa-7 na s12: ženin "Dobranice 8" (Jakob Štefanič 25-l) + nevesta "Podzgemeľ 6" (Barbara Tome 40-l, pripis pod imenom!). Prepiši VSE znak za znak (tudi pripis!). {"id":"s12-r7-wohnort","zeninWohnort":"...","nevestaWohnort":"...","nevestaPripis":"...","note":"..."}`,
  's12-r7-befunde': `ULTRA-ZOOM (4×) Befunde vpisa-7 na s12: pričakovano 'Oewißliche/zweifache Dispens zum dritten Grad dd. 12. Febr. 876. und Dispens dd. 15. Febr. 876' (DISPENS 3.-krvno-sorodstveni-stopnji!). Prepiši znak za znak — kateri stopnji (dritter Grad?) in datumi? {"id":"s12-r7-befunde","befunde":"...","dispensStopnja":"...","datumi":"...","note":"..."}`,
  's11-r1-elternG': `ULTRA-ZOOM (4×) staršev ŽENINA vpisa-1 na s11 (oče: Matthias Krupanič[~Zupanič]-DUEL; mati: [Kath. Starasinić ~ Barbara née Lavrič]-DUEL). Prepiši VSE vrstice znak za znak. {"id":"s11-r1-elternG","ocee":"...","mati":"...","note":"..."}`,
  's11-r1-pricE': `ULTRA-ZOOM (4×) prič (Tauf- und Familien-Name + Stand) vpisa-1 na s11 — kandidat: "Nicolaus Bahorič/Bahovič × Nicolaus [?]" ALI prazno. Prepiši znak za znak. {"id":"s11-r1-pricE","price":"...","stand":"...","note":"..."}`,
  's11-tail-befunde': `ULTRA-ZOOM (4×) Befundov TAIL-VRSTE (vijolični vpis 1875) na s11: kandidati 'Copulations-Erlaubnis v. k.k. Bezirksamt + Gemeindezettel vom 3. VIII. 1875 + Einsegnung-datumi + 'Privat''. Prepiši VSE znak za znak (vijolično črnilo, delno bledeče). Posebej: kateri DATUMI so berljivi? {"id":"s11-tail-befunde","befunde":"...","datumi":"...","note":"..."}`,
  's13-r10-wohnort': `ULTRA-ZOOM (4×) Wohnortov vpisa-10 na s13 ('1876. Februar 23.'): ženin "Vinica 1"? (Johann Županič/Kupanič 23-l) + nevesta "Krasina 63-vs-43-DUEL" (Anna Bahovič 17-l). Prepiši VSE znak za znak. {"id":"s13-r10-wohnort","zeninWohnort":"...","nevestaWohnort":"...","hisnaDuel":"63|43|...","note":"..."}`,
  's13-r11-wohnort': `ULTRA-ZOOM (4×) Wohnortov vpisa-11 na s13 ('Feb. 27.'): ženin "Velika-Gorica/Lipnik-in-Kroatien 9" (Janko Mihelec 26-l) + nevesta "Adlešiči 16" (Barbara Novak 22-l). Prepiši VSE znak za znak. {"id":"s13-r11-wohnort","zeninWohnort":"...","nevestaWohnort":"...","note":"..."}`,
  's13-r12-wohnort': `ULTRA-ZOOM (4×) Wohnortov vpisa-12 na s13 ('Septemb. 17.'): ženin "Graz/Windberg-48" (Eduard Lingl 30-l + stan-pripis!) + nevesta "Graz/Blae 23" (Josepa 29-l + stan). Prepiši VSE znak za znak (vojaški/oficirski pripisi!). {"id":"s13-r12-wohnort","zeninWohnort":"...","zeninStan":"...","nevestaWohnort":"...","nevestaStan":"...","note":"..."}`,
  's13-r10-befunde': `ULTRA-ZOOM (4×) Befundov vpisa-10 na s13: pričakovano 'Aufgebot am 6. und 13. Febr. 1876 + Consens des Vormundschaftsgerichtes [MLADOLETNICA 17-l!] ertheilt am 15. Febr. 1876'. Prepiši znak za znak. {"id":"s13-r10-befunde","befunde":"...","aufgebot":"...","consens":"...","note":"..."}`,
};

const zai = await ZAI.create();

async function run(t) {
  const out = `${OUT}/p4-${t.id}.json`;
  if (fs.existsSync(out)) { console.log(`${t.id}: že obstaja`); return; }
  const b64 = fs.readFileSync(`${DIR}/krops4/${t.id}.jpg`).toString('base64');
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      console.log(`--- ${t.id} (poskus ${attempt}) ...`);
      const completion = await Promise.race([
        zai.chat.completions.createVision({
          messages: [{ role: 'user', content: [
            { type: 'text', text: prompts[t.id] },
            { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
          ]}],
          thinking: { type: 'disabled' }
        }),
        new Promise((_, rej) => setTimeout(() => rej(new Error('TIMEOUT 240s')), 240000))
      ]);
      const raw = completion.choices[0]?.message?.content ?? '';
      const s = raw.indexOf('{');
      const e = raw.lastIndexOf('}');
      if (s === -1 || e === -1) throw new Error('ni JSON');
      fs.writeFileSync(out, JSON.stringify(JSON.parse(raw.slice(s, e + 1)), null, 2));
      console.log(`${t.id}: OK`);
      return;
    } catch (err) {
      console.log(`${t.id}: poskus ${attempt} NAPAKA: ${err.message}`);
      await new Promise(r => setTimeout(r, 3000));
    }
  }
  console.log(`${t.id}: NEUSPEŠEN`);
}

for (const id of Object.keys(prompts)) await run({ id });
console.log('pass-4 KONČAN');
