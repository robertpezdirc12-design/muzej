import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const DIR = '/tmp/p259/full';

const COLS = `Stolpci LEVE strani razprtega lista: [Jahr/Monat/Tag der Trauung] [Wohnort ŽENINA] [Haus-Nr] [Taufname+Familien-Name+Stand ŽENINA] [Alter] | DESNE strani: [Eltern des Bräutigams] [Eltern der Braut] [Zeugen] [Urkunden] [Unterschrift des trauenden Priesters]`;

const HINTS = {
  s11_r1: "1833 Pag. 19 vrh (6. Febr 1833 — 7. poroka tega dne, kaskada se nadaljuje iz Pag. 17!): trije viri: (a) 'Nikolaus Gus? Lindart Dobroviz 13 × Catharina Haushony Dobroviz 14' (b) 'Nicolaus Rup Dobroviz 13 × Catharina Krischoviz Dobroviz 14' (c) oče ženina po desni strani: 'Nic. Angel Lindart', mati 'Maria Gertschpig'; nevestini starši: 'Martin Kerschnik? / Barbara Angel'. VPRAŠANJE: priimek ženina (Gus? Rup? Angel?) + njegova VAS (Lindart ali Dobroviz=Dobravlje?) + hiša (13?) + priimek neveste (Haushony? Krischoviz?) + njena vas/hiša (Dobroviz 14?).",
  s11_r2: "1833 Pag. 19 (6. Febr d°): POZOR — prejšnja stran (Pag. 17) se je končala z 'Johann PESDIRZ Griblje 50 × Maria [Himiz] Griblje 49'! Ta vrstica: (a) 'Joh. Gosling/Goslig? Lindart Griblje 53 × Maria Bring/Brinc Griblje 24' (b) 'Johann Pesdirz? Griblje 33 × Maria Brung Griblje 24' (c) oče: 'Johann Gutting? / Maria Poshel'. VPRAŠANJE: ALI je priimek ženina res PESDIRZ (druga poroka Pesdirz v 2 dneh?!) ali Gosling/Gostinč? Hiša: 33? 53? 50? Priimek neveste: Bring/Brinc/Brung? Hiša 24? Preberi ČRKO ZA ČRKO.",
  s11_r9: "1833 Pag. 19 (13. Febr — prva vrstica po 6.-Febr-kaskadi): (a) 'Georg Haushfinigl? Krajng 32 × Catharina Kurra/Kurre Germ 29' (b) 'Georg Arahrinigel? Kosting 22 × Catharina Kurre Gern 29' (c) oče: 'Peter Harschping? Lindart / Maria Horsang? Lindartin'. VPRAŠANJE: priimek ženina (Haušpinc? Harschpich?) + vas (Kranjc? Kostanjevica?) + hiša (32? 22?) + vas neveste (Gern? Germ?) + hiša (29?).",
};

const PROMPT = (id) => `Slika je POVEČAN IZREZ (vodoravni trak, širina celega razprtega lista) poročne knjige Trauungs-Buch 01738 (Podzemelj, Kurrent-pisava, nemško). Trak obsega ENO vrstico vpisa (lahko tudi del sosednje — loči po vsebinski celovitosti!).
KONTEKST: ${HINTS[id]}
${COLS}
Naloga: prepiši DOBESEDNO po stolpcih. Hišne številke so MAJHNE — previdno! Nejasna mesta označi z [~]. Če je trak prazen ali vsebuje dve vrstici, povej.
Izhod SAMO JSON: {"id":"${id}","vrstica":"polna/opis","datum":"","leto":0,"vasZenin":"","hisZenin":0,"zenin":"","standZenin":"","starZenin":0,"letoZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","standNevesta":"","starNevesta":0,"letoNevesta":0,"oceZenin":"","mataZenin":"","oceNevesta":"","mataNevesta":"","price":"","urkunde":"","duhovnik":"","xOpen":[],"razlaga":""}`;

async function run(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.error(`${id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT(id) }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 6; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1500, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.error(`${id}: OK`);
      return;
    } catch (e) {
      console.error(`${id}: a${a} ${String(e).slice(0,60)}`);
      await new Promise(r2 => setTimeout(r2, 4000 * a)); // eksponentni zamik
    }
  }
  console.error(`${id}: FAIL`);
}
for (const id of Object.keys(HINTS)) {
  try { await run(id); } catch (e) { console.error(`outer ${id}: ${String(e).slice(0,80)}`); }
  await new Promise(r => setTimeout(r, 2500));
}
console.error('PILOT DONE');
