import fs from 'fs';
import ZAI from 'z-ai-web-dev-sdk';
const zai = await ZAI.create();
const PROMPT = `Slika: ZGORNJI DEL LEVE STRANI razprtega lista poročne knjige 01738 (Podzemelj, leto 1829), Kurent-pisava, ×3 povečava.
Najprej OPISI POSTAVITEV: katere stolpce vidiš (natisnjena glava + rokopis), od leve proti desni (približno v frakcijah širine).
Nato PREPIŠI VSE VRSTICE tabele (zgoraj dol). Za vsako vrstico podaj:
- datum (natanko prepisan: letnica/dan/mesec ali ditto)
- vas/hiša ženina (naslednji stolpci)
- ime ženina (prve besede)
- ostalo, kar je razločno
Nejasno OZNAČI [~]. Ne ugibaj. Izhod SAMO JSON:
{"postavitev":"","vrstice":[{"datum":"","vasZenin":"","hisZenin":"","zenin":"","ostalo":""}],"razlaga":""}`;
const content = [{ type: 'text', text: PROMPT }];
content.push({ type: 'image_url', image_url: { url: `data:image/jpeg;base64,${fs.readFileSync('/tmp/p256/probe/s4_topL.jpg').toString('base64')}` } });
const r = await zai.chat.completions.createVision({ messages: [{ role: 'user', content }], temperature: 0.1, max_tokens: 2500, thinking: { type: 'disabled' } });
fs.writeFileSync('/tmp/p256/probe/s4_topL.json', r.choices[0].message.content || '');
console.log(r.choices[0].message.content?.slice(0, 300));
