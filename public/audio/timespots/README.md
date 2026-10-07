# TTS pripovedi časovnih točk (issue #12)

Komponenta `ar-time-machine.tsx` ob pritisku »Poslušaj« najprej poskusi
naložiti statično datoteko po shemi:

    /audio/timespots/<id točke>-si.mp3   (slovenščina)
    /audio/timespots/<id točke>-en.mp3   (angleščina)

ID-ji: `cerkev`, `jedro`, `kolpa`, `ribnik`, `gornje`, `meja`.
Besedilo = naslov + opis točke (`src/data/atlas/timespots.ts`).

Če datoteke ni (404), se samodejno uporabi brskalnikov
`speechSynthesis` (zastonj, brez odvisnosti od plačljivih storitev) —
to je trenutni primarni mehanizem, ker razpoložljivi oblačni TTS
glasovi ne izgovarjajo slovenščine muzejsko kvalitetno.

## Kako dodati posnetke (priporočeno naslednji korak)

1. Posnemi človeški glas (domačin!) po besedilu iz timespots.ts.
2. Shrani MP3 (~96–128 kbps, mono) pod zgoraj imenovanimi imeni.
3. Brez spremembe kode — prvi poskus HEAD bo uspel in predvajal datoteko.

Service worker jih ob obisku predpomni (stale-while-revalidate).
