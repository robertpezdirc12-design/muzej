# Glas muzeja — govorne skripte (P15)

Glas muzeja so SKRIPTE. Vsaka časovna točka ima napisano govorno
skripto (slovenščina + angleščina) v `src/data/atlas/narrations.ts`,
izpeljano izključno iz muzejskih podatkov (naslov, opis, dokaz) —
nobeno zgodovinsko dejstvo ni dodano ali izmišljeno.

Predvajalnik je DETERMINISTIČEN in BREZ AI modelov:

  · brskalnikova vgrajena speechSynthesis (zastonj, lokalno),
  · nobenih omrežnih klicev ob predvajanju,
  · nobenih plačljivih TTS storitev v oblaku, nobenih API ključev.

Enak mehanizem poganja vse tri glasove muzeja (AR časovni stroj,
vodeni sprehod, AR kamera) prek skupnega modula `src/lib/narrator.ts`.
Med predvajanjem se na kartici pokaže tudi transkript skripte
(dostopnost za gluhe in naglušne obiskovalce).

Kvaliteta glasu je odvisna od glasov, ki jih ima naprava obiskovalca
 nameščenih — to je cena brezplačnega, zasebnega in determinističnega
 pristopa, ki ga muzej sprejema zavestno.

## Kdaj bi radi človeški posnetek?

Ta mapa ostaja pripravljena za morebitne posnetke DOMAČEGA GLASU
 (človeški posnetek ni AI model — načelo »brez AI« ostaja):

1. Posnemi človeški glas po besedilu skripte iz `narrations.ts`.
2. Shrani MP3 (~96–128 kbps, mono) kot `<id točke>-si.mp3` oz. `-en.mp3`.
3. V `ar-time-machine.tsx` ponovno dodaj vejo predvajanja datoteke
   (vzorec: HEAD preverba + `new Audio(url)`; gl. git zgodovino P14).

Prej tu obljubljena samodejna MP3 veja (HEAD 404 → fallback TTS) je
bila odstranjena: datoteke nikoli niso obstajale, vsak klik pa je
nalagal naporečen 404. Zdaj je skripta edini vir resnice govora.
