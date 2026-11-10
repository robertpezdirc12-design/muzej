#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p241_bump — sanitizacija zastarelih agregatov za P241 (korpus 1951→1957, 04455 208→214, sidra 201→207 + 1882:1→7, dobe 175→181).
MERGE-vzorec P238-h13: 6 novih blokov 1882 (+ pre-stoječi P80-sidro h36 = 7. blok-leta!). Prekine BREZ pisanja, če katera številka ne ustreza.
"""
import sys

PATH = '/home/z/my-project/src/lib/qa-parish.ts'
with open(PATH, encoding='utf-8', newline='') as f:
    original = f.read()

Q = '"'
# vrstica b: veriga skupnih zneskov
B_OLD = ('HOUSE_VITALS ≠ 1951 (${HOUSE_VITALS.length} — P237: 1940; P238: + 7 blokov 04455-1885 '
         '− 1-duplikat-starega-P80-sidra-h13 = 1946; P239: + 3 bloka 04455-1884 = 1949; '
         'P240: + 2 bloka 04455-1883 (h13-RADOVIČ + h2-HLEBEC!) = 1951!)')
B_NEW = ('HOUSE_VITALS ≠ 1957 (${HOUSE_VITALS.length} — P237: 1940; P238: + 7 blokov 04455-1885 '
         '− 1-duplikat-starega-P80-sidra-h13 = 1946; P239: + 3 bloka 04455-1884 = 1949; '
         'P240: + 2 bloka 04455-1883 (h13-RADOVIČ + h2-HLEBEC!) = 1951; '
         'P241: + 6 novih blokov 04455-1882 (h35 + h38×h12 + h56 + h13×h52 + h8 + h1×h10!-h36 = MERGE-z-P80-sidrom!) = 1957!)')
# vrstica e: sidra year-guard 1882: 1 → 7
E_OLD = '  p80MarrAnchors.filter((h) => h.year === 1882).length !== 1 ||'
E_NEW = '  p80MarrAnchors.filter((h) => h.year === 1882).length !== 7 ||'
# vrstica d: dobe guard
D_OLD = 'dobe-bloki ≠ 175/7/26'
D_NEW = 'dobe-bloki ≠ 181/7/26'
D2_OLD = 'predvojna ≤1913 vključuje 5 pred-linijskih 1882+1883-P240×2+1884-P239+1885!'
D2_NEW = 'predvojna ≤1913 vključuje 11 pred-linijskih 1882-P241×7!+1883-P240×2+1884-P239+1885!'

REPLACEMENTS = [
    ('a  guard: HOUSE_VITALS.length !== 1951',
     'HOUSE_VITALS.length !== 1951',
     'HOUSE_VITALS.length !== 1957', 150),
    ('b  template: P237–P240 veriga + P241 dodatek',
     B_OLD, B_NEW, 1),
    ('c  p80Marr.length !== 208',
     'p80Marr.length !== 208',
     'p80Marr.length !== 214', 1),
    ('c2 p115Marr.length !== 208',
     'p115Marr.length !== 208',
     'p115Marr.length !== 214', 1),
    ('d  p80MarrAnchors.length !== 201 (2x)',
     'p80MarrAnchors.length !== 201',
     'p80MarrAnchors.length !== 207', 2),
    ('e  sidra year-guard: 1882: 1 → 7',
     E_OLD, E_NEW, 1),
    ('f  sidra message: 201 → 207 + 1882:7-P241!',
     'poročna sidra ≠ 201 (1882:1 · 1883:2-P240!',
     'poročna sidra ≠ 207 (1882:7-P241! · 1883:2-P240!', 1),
    ('g  p116Marr.length !== 208 (8x)',
     'p116Marr.length !== 208',
     'p116Marr.length !== 214', 8),
    ('h  filter-04455-length !== 208 (29x)',
     'bookSignature === ' + Q + '04455' + Q + ').length !== 208',
     'bookSignature === ' + Q + '04455' + Q + ').length !== 214', 29),
    ('i  p152Blocks.length !== 208',
     'p152Blocks.length !== 208',
     'p152Blocks.length !== 214', 1),
    ('j  message: bloki 04455 ≠ 208 (27x)',
     'bloki 04455 ≠ 208',
     'bloki 04455 ≠ 214', 27),
    ('j2 message: bloki-04455 ≠ 208 (2x)',
     'bloki-04455 ≠ 208',
     'bloki-04455 ≠ 214', 2),
    ('l  narrative: korpus: 1951/',
     'korpus: 1951/',
     'korpus: 1957/', 1),
    ('m  narrative: corpus: 1951/',
     'corpus: 1951/',
     'corpus: 1957/', 1),
    ('n  narrative: 288/1951 (2x)',
     '288/1951',
     '288/1957', 2),
    ('o  narrative: = 1951 blokov',
     '= 1951 blokov',
     '= 1957 blokov', 1),
    ('p  narrative: = 1951 blocks',
     '= 1951 blocks',
     '= 1957 blocks', 1),
    ('q  badge: vitals 1951 · 04104 288',
     'vitals 1951 · 04104 288',
     'vitals 1957 · 04104 288', 1),
    ('r  dobe: 175/7/26 → 181/7/26',
     D_OLD, D_NEW, 1),
    ('r2 dobe: 5 → 11 pred-linijskih',
     D2_OLD, D2_NEW, 1),
]

text = original
for label, old, new, expected in REPLACEMENTS:
    n = text.count(old)
    if n != expected:
        print(f'ABORT [{label}]: pričakovano {expected}, najdeno {n} × {old[:80]!r} — NIČ NE PISAN', file=sys.stderr)
        sys.exit(1)
    text = text.replace(old, new)
    print(f'  ok [{label}] {n}/{expected}')

leftover_guard = text.count('HOUSE_VITALS.length !== 1951')
leftover_208 = text.count('.length !== 208')
if leftover_guard or leftover_208:
    print(f'ABORT: ostanki — guard-1951={leftover_guard}, length-208={leftover_208}', file=sys.stderr)
    sys.exit(1)

with open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(text)
print('ZAPISANO:', PATH)
