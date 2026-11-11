#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P250-OBNOVA: pt-luknja + I9c-križne-popravke + p237-Python-literáli + README + worklog."""
import json, glob, re

# ——— 1. pt-luknja ———
p = 'research/issue17/pt-luknja-18-final.json'
d = json.load(open(p, encoding='utf-8'))
d['vitalsTotal'] = 2008
c = d['corpus']
c['vitalsTotal'] = 2008
c['byBook']['04455'] = 265
if 'P250' not in c.get('housesNote', ''):
    c['housesNote'] = c.get('housesNote', '') + ' | P250: +11-blokov-1874 (04455 254→265, vitals 1997→2008!)'
for h in d['gapHouses']:
    if h['houseNo'] == '42':
        h['blocksTotal'] = 16
        h['byBook']['04455'] = 3
        h['firstYear'] = 1874
        h['years'] = sorted(set(h['years'] + [1874]))
        h['p250Note'] = ("P250: s7-m32-PROMOCIJA-tail-kontekst→BLOK (NAPAVED-IZPOLNJENA!-cf.-P248-h30!) — "
                         "nevesta-Maria-PEGDIRC-GRIBLJE 42-(P249-mikro-6×-1:1!)-18.-November-1874-ženin-Nicolaus-Marasinič "
                         "= h42-PARALELA-1:1-z-Georg-Pegdirc-1879-P244-v21-ISTA-HIŠA-ISTA-PRIIMEK (PEZDIRC-družina-na-h42-2-dokaza-5-let-narazen!) "
                         "— h42-04455-firstYear-1879→1874-ZA-5-LET!-bloki-15→16 (04455-2→3!)")
        h['p249Note'] = h.get('p249Note', '') + ' [P250-IZPOLNJENO!]'
    if h['houseNo'] == '43':
        h['blocksTotal'] = 10
        h['byBook']['04455'] = 2
        h['firstYear'] = 1874
        h['years'] = sorted(set(h['years'] + [1874]))
        h['p250Note'] = ("P250: m25-s6-NEVESTA-Marina-[~Martin]-BRULA-GRIBLJE 43-14.-Juni-1874-'Gribje-43'-ultra-8×-1:1 "
                         "(Kurrent-'4'-odprti-vrh-NE-'93'/'33'!) = H43-BRULA-PARALELA-1:1-z-Katharina-BRULA-1878-P246-v5-bride-KONTEKST-ISTA-HIŠA-ISTA-PRIIMEK "
                         "(P249-h42-vzorec-2.-instance!) — h43-04455-firstYear-1908→1874-DVIG-ZA-34-LET-NOV-ABSOLUTNI-REKORD-DVIGA!-bloki-9→10 (04455-1→2!)")
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('pt-luknja-obnovljena')

# ——— 2. I9c-križne-popravke-v-vseh-starih-verifikatorjih ———
for f in sorted(glob.glob('scripts/p2*_parish_*.py')) + ['scripts/p237_parish_forensics.py']:
    src = open(f, encoding='utf-8').read()
    o = src
    src = src.replace('"1997" in open', '"2008" in open')
    src = re.sub(r'(and ")254(" in open\(f"\{ROOT\}/scripts/p23[6-9])', r'\g<1>265\g<2>', src)
    src = re.sub(r'(and ")254(" in open\(f"\{ROOT\}/scripts/p24[0-9])', r'\g<1>265\g<2>', src)
    if src != o:
        open(f, 'w', encoding='utf-8').write(src)
        print(f'I9c: {f.split("/")[-1]}')

# ——— 3. p237-Python-literáli ———
f = 'scripts/p237_parish_forensics.py'
src = open(f, encoding='utf-8').read()
src = src.replace('[53,78,20,36,54] · skupaj 241', '[53,78,20,36,56] · skupaj 243')
src = src.replace('skupaj == 241', 'skupaj == 243')
src = src.replace('== 241)', '== 243)')
src = src.replace('{"04104": 53, "04105": 78, "04106": 20, "04894": 36, "04455": 54} and milic_skupaj == 243',
                  '{"04104": 53, "04105": 78, "04106": 20, "04894": 36, "04455": 56} and milic_skupaj == 243')
src = src.replace('{total:42, family:36, others:6}', '{total:43, family:37, others:6}')
src = src.replace('len(h65) == 42 and len(h65_druzina) == 36', 'len(h65) == 43 and len(h65_druzina) == 37')
src = src.replace('len(mathias) == 22 and leta_mathias[0] == 1871', 'len(mathias) == 23 and leta_mathias[0] == 1871')
src = src.replace('== 22 blokov', '== 23 blokov').replace('n == 22', 'n == 23')
src = src.replace("'\"]53,78,20,36,54[\"' in qa", "']53,78,20,36,56[' in qa")
src = src.replace('"53,78,20,36,54" in qa', '"53,78,20,36,56" in qa')
src = src.replace("'\"53,78,20,36,54\"' in qa", "'\"53,78,20,36,56\"' in qa")
src = src.replace('živi preverja 241/53-78-20-36-54/22/42-36-6', 'živi preverja 243/53-78-20-36-56/23/43-37-6')
src = src.replace('živi preverja 243/53-78-20-36-54/22/42-36-6', 'živi preverja 243/53-78-20-36-56/23/43-37-6')
src = src.replace('P248: +1-v9!', 'P248-+1-v9!-P250-+2-1874!')
open(f, 'w', encoding='utf-8').write(src)
print('p237-literáli-obnovljeni')

# ——— 4. p249-I8b (h42-15→16 + vejica) ———
f = 'scripts/p249_parish_marriage_1875_04455.py'
src = open(f, encoding='utf-8').read()
src = src.replace('h42["blocksTotal"] == 15 and "p249Note" in h42', 'h42["blocksTotal"] == 16 and "p249Note" in h42')
src = src.replace('check("I8b h42-p249Note (tail-kandidat!-bloki-nespremenjeni-15!)",',
                  'check("I8b h42-p249Note (tail-kandidat-PROMOCIJA-P250!-bloki-16!)",')
open(f, 'w', encoding='utf-8').write(src)
print('p249-I8b-obnovljen')
