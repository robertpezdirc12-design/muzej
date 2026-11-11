import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const DIR = '/tmp/p257/full';
const zai = await ZAI.create();

// Kontekst po vrsticah (iz P256-predbranj + P257-pass-1) — za potrditve/korekcije.
const HINTS = {
  s6_r4: "1830 m1: 12. Jänner 1830 — Marcus [Vipavc?/Vißnyak/Vizgar/Vipauz] (vas Krajnog?/Kriesing?, hiša 34?, starost 43?) × Catharina [Aurnig?/Truniž/Schurig] (Kaplja vas? 7, 35). RESTART-1830 vrstica!",
  s6_r5: "1830: 17. Febr — Martin [Tschall?/Taschall?] (Gurila?/Mronš? 8) × Catharina [Stephanitsch?] (Dobrnič? 8).",
  s6_r6: "1830: 17. Febr — Math. [Koging?/Koynig?] (Dobrnik?/Dobraiz? 17/14?) × Maria [Angel?] (Dobrnič? 23).",
  s6_r7: "1830: 17. Febr — Georg [Megorin?/Moosin?] (Zerkinjef?/Zarkwishe? 15) × Anna [Milek??] (Griblje?? 22??) — NEVESTA-IZ-GRIBLJE-22?! (hiša Millerjevih nevest 1828/1829!) — PREVIDNO preberi vas+hišo neveste!",
  s6_r8: "1830: 17. Febr — Georg [Kaphing?/Knaphaiz?] (Kringlace?/Krioglauz? 27/29) × Anna [Tong?] (Pamaets? 11).",
  s6_r9: "1830: 18.? (März?) — Mart./Carl [Kosalth?/Hoftett?] (Möttling?, hiša [140|10|110?]-DUEL!) × Maria [Kaphing?] (Kringlace? 29).",
  s6_r10: "1830: 21.? (Jun?) — Mart. [Shunigh?] (Vastaniz? 10) × ? — morda TA VRSTICA ali prazna; preveri tudi 30. Juni!",
  s6_r11: "1830: 30. Juni — Johann [TaNofznigh?/Sebastianig?] (Zarkwishe?/Zerkinjef? 7) × Anna [Lenough?] (Zarblinge? 16). ZADNJI-VPIS-1830?",
  s7_r1: "1831 m1: 26. Jänner 1831 — Peter [Križan?/Krieghan] (Griblje/Grüble, hiša 3) × Anna [Pehligh?/Doblič?] (Griblje/Grüble?, hiša 33?). PREVIDNO: hiša ženina in hiša neveste (3 in 33?)!",
  s7_r2: "1831: 1. Febr — Georg [Podierz?/Pesdirz?] (Griblje/Grübln, hiša 50) × Anna [Leoporz?/Lebartz?] (Griblje?/Güibbln?, hiša 54?). PREVIDNO: priimek ženina (Podierz ali Pesdirz — Pesdirc?!) in hiši (50/54?)!",
  s7_r3: "1831: 9. Febr — Math. [Kiniz?/Schimiz?] (Griblje/Grübln, hiša 56) × Maria [Podierz?/Pesdirz?] (Podzemelj/Podsemel, hiša 3). PREVIDNO: priimka (Schimiz ali Kiniz; Podierz ali Pesdirz) in hiši (56/3?)!",
  s7_r4: "1831: 9. Febr d° — Nicol [Tomz?] (Podzemelj/Podsemel, hiša 17?) × Barbara [Sitej?/Saie?] (Otok, hiša 1).",
  s7_r5: "1831: 9. Febr d° — Peter [Haren?/Hare?] (Kruschnz?/Krasching?/Kaproic?, hiša 24) × Maria [Nikol?] (Podzemelj/Podsemel, hiša 11).",
  s7_r6: "1831: 9. Febr d° — Peter [Podierz?/Pesdirz?] (Kaplja vas/Kapln?, hiša 4) × Anna [Turejef?] (Otok, hiša 17). PREVIDNO: priimek ženina (Podierz/Pesdirz — 3. omemba!) in vas (Kapln?)!",
  s7_r7: "1831: 9. Febr d° — [Maria Podierz??] (Griblje/Grübln, hiša 26/20-DUEL?) × Anna [Maley?/Malež?] (Griblje/Grübln, hiša 27). ANOMALIJA: žensko ime v stolpcu ženina — preveri (vdova? pisarska napaka? premik vrstic?)!",
  s7_r8: "1831: 9. Febr d° — Mich. [Zajner?/Zajec?] (Otok, hiša 3) × Maria [Zuitica?] (Prioel/Priol?, hiša 2).",
  s7_r9: "1831: 9. Febr d° — Johann [Nowig?/Skvic?/Novak?] (Gradac/Gradaz, hiša 5) × Catharina [Kreiel?] (Podierz??/Podsemel?, hiša 17). PREVIDNO: priimek/vas neveste (Podierz = priimek ali vas Podsemelj?)!",
  s7_r10: "1831: 9. Febr d° — Nicol [Milek?/Milic?] (Griblje/Grübln, hiša 65) × Margaretha [Podlanzigh?/Prodsanzig?] (Podzemelj/Podsemel, hiša 2). PREVIDNO: priimek ženina (Milek ali Milic) in hiša 65!",
  s7_r11: "1831: 9. Febr d° — Anton [Galonz?/Dal?] (Otok, hiša 22) × Cath. [Muffich?] (Kruschinz?, hiša 14).",
  s7_r12: "1831: 9. Febr d° — Nicol [Kambicz?/Hambis?] (Podlog?, hiša 13/15-DUEL?) × Maria [Mag.?] (Tomel?, hiša 17).",
  s7_r13: "1831: 9. Febr d° — Math. [Muniz?/Ianigl?] (Griblje/Grübln, hiša 1) × Catharina [Podierz?/Pesdirz?] (Griblje/Grübln, hiša 11). PREVIDNO: priimka (Muniz=MUZ?/Ianigl; Podierz/Pesdirz — 6. omemba!) in hiši (1/11?)!",
};

const PROMPT = (id) => `Slika je POVEČAN IZREZ (vodoravni trak, širina cele strani) poročne knjige Trauungs-Buch 01738 (Podzemelj, Kurrent-pisava, nemško). Trak obsega ENO vrstico vpisa (lahko tudi del sosednje — loči po vsebinski celovitosti!).
KONTEKST: ${HINTS[id]}
Stolpci LEVE strani razprtega lista (Pag. lihi): [Jahr/Monat/Tag der Trauung] [Wohnort] [Haus-Nr] [Taufname+Familien-Name+Stand ŽENINA] [Alter?] | [Wohnort] [Haus-Nr] [Taufname+Familien-Name+Stand NEVESTE] [Alter?]
Stolpci DESNE strani razprtega lista: [Eltern des Bräutigams] [Eltern der Braut] [Zeugen] [Urkunden] [Unterschrift des trauenden Priesters]
Naloga: prepiši DOBESEDNO po stolpcih. Hišne številke so MAJHNE — previdno! Nejasna mesta označi z [~]. Če je trak prazen ali vsebuje dve vrstici, povej.
Izhod SAMO JSON: {"id":"${id}","vrstica":"polna/opis","datum":"","leto":0,"vasZenin":"","hisZenin":0,"zenin":"","standZenin":"","starZenin":0,"letoZenin":0,"vasNevesta":"","hisNevesta":0,"nevesta":"","standNevesta":"","starNevesta":0,"letoNevesta":0,"oceZenin":"","mataZenin":"","oceNevesta":"","mataNevesta":"","price":"","urkunde":"","duhovnik":"","xOpen":[],"razlaga":""}`;

const ROWS = [];
for (let i = 4; i <= 11; i++) ROWS.push(`s6_r${i}`);
for (let i = 1; i <= 13; i++) ROWS.push(`s7_r${i}`);

async function run(id) {
  const out = `${DIR}/${id}.json`;
  if (fs.existsSync(out) && fs.statSync(out).size > 40) { console.log(`${id}: skip`); return; }
  const content = [{ type: 'text', text: PROMPT(id) }];
  content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync(`${DIR}/${id}.jpg`).toString('base64')}` } });
  for (let a = 1; a <= 4; a++) {
    try {
      const r = await zai.chat.completions.createVision({
        messages: [{ role: 'user', content }],
        temperature: 0.1, max_tokens: 1500, thinking: { type: 'disabled' },
      });
      fs.writeFileSync(out, r.choices[0].message.content || '');
      console.log(`${id}: OK`);
      return;
    } catch (e) { console.log(`${id}: a${a} ${String(e).slice(0,70)}`); await new Promise(r2=>setTimeout(r2,2500)); }
  }
  console.log(`${id}: FAIL`);
}
for (const id of ROWS) { await run(id); await new Promise(r=>setTimeout(r,1000)); }
