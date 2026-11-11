import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const DIR = '/tmp/p256/D';

const HOUSE = `Slika: ×5 povečan izrez iz poročne knjige 01738 (Podzemelj), Kurent-pisava. VIDNI STA STOLPCA VAS in HIŠA (številka) — [plus sosednji stolpec v ozadju].
Prepiši NATANČNO, dobesedno, kar je zapisano v obeh stolpcih: ime vasi (kraja) in hišna številka. Kurent številke: 1=črt, 2=zanka, 3=flat-top, 4=odprt-krož, 5=spodnja-zanka, 6=odprta-zanka, 7=črt+s črto, 8=dvojna-zanka, 9=zanka+rep, 0=krož.
NE ugibaj — nejasno OZNAČI [~]. Če vidiš več številk/vpisov, prepiši vse.
Izhod SAMO JSON: {"vas":"","hisa":null,"vsebina":"","razlaga":""}`;

const DATE = `Slika: ×5 povečana datumski celica (stolpec 'Jahr, Monat und Tag der Trauung') poročne knjige 01738 (Podzemelj), Kurent-pisava.
Prepiši NATANČNO, dobesedno, kar je zapisano: letnica / dan / mesec / ditto-znaki. Kurent številke: 1=črt, 2=zanka, 3=flat-top, 4=odprt-krož, 5=spodnja-zanka, 6=odprta-zanka, 7=črt+s črto, 8=dvojna-zanka, 9=zanka+rep, 0=krož. Meseci: Jän(n), Febr, Mär(z), Apr, Mai, Jun(i), Jul(i), Aug, Sept/7br, Okt/8br, Nov/9br, Dez/Xbr. Ditto: '//', '=', 'dto', 'ejusd(em)'.
NE ugibaj — nejasno OZNAČI [~].
Izhod SAMO JSON: {"zapis":"","dan":null,"mesec":"","leto":null,"razlaga":""}`;

const MAP = { gh: HOUSE, bh: HOUSE, dt: DATE };
const files = fs.readdirSync(DIR).filter(f => f.endsWith('.jpg'));
for (const f of files) {
  const id = f.slice(0, -4);
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out)) { console.log(`${id}: skip`); continue; }
  const kind = id.split('_')[1];
  const prompt = MAP[kind] || DATE;
  const content = [{ type: 'text', text: prompt }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${f}`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({ messages: [{ role: 'user', content }], temperature: 0.1, max_tokens: 700, thinking: { type: 'disabled' } });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      break;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,50)}`); await new Promise(r2=>setTimeout(r2,3000)); }
  }
  await new Promise(r=>setTimeout(r,900));
}
