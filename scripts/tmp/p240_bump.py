#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p240_bump — sanitizacija zastarelih agregatov za P240 (korpus 1949→1951, 04455 206→208, sidra 199→201).
Ciljane zamenjave samo; zgodovinske vrstice so zaščitene. Prekine BREZ pisanja, če katera številka ne ustreza.
"""
import sys

PATH = '/home/z/my-project/src/lib/qa-parish.ts'

with open(PATH, encoding='utf-8', newline='') as f:
    original = f.read()

Q = '"'
# vrstica r: stari/novi niz z notranjimi navedki (TS template literal)
R_OLD = ('bloki-04455 ≠ 206 (${HOUSE_VITALS.filter((h) => h.bookSignature === '
         + Q + '04455' + Q + ').length} — 203 + 3-leta-1884!)')
R_NEW = ('bloki-04455 ≠ 208 (${HOUSE_VITALS.filter((h) => h.bookSignature === '
         + Q + '04455' + Q + ').length} — 206 + 2-leta-1883!)')
# vrstica b: veriga skupnih zneskov
B_OLD = ('HOUSE_VITALS ≠ 1949 (${HOUSE_VITALS.length} — P237: 1940; P238: + 7 blokov 04455-1885 '
         '− 1-duplikat-starega-P80-sidra-h13 = 1946; P239: + 3 bloka 04455-1884 = 1949!)')
B_NEW = ('HOUSE_VITALS ≠ 1951 (${HOUSE_VITALS.length} — P237: 1940; P238: + 7 blokov 04455-1885 '
         '− 1-duplikat-starega-P80-sidra-h13 = 1946; P239: + 3 bloka 04455-1884 = 1949; '
         'P240: + 2 bloka 04455-1883 (h13-RADOVIČ + h2-HLEBEC!) = 1951!)')
# vrstica e: sidra year-guard vstavljanje
E_OLD = ('  p80MarrAnchors.filter((h) => h.year === 1882).length !== 1 ||\n'
         '  p80MarrAnchors.filter((h) => h.year === 1885).length !== 7 ||')
E_NEW = ('  p80MarrAnchors.filter((h) => h.year === 1882).length !== 1 ||\n'
         '  p80MarrAnchors.filter((h) => h.year === 1883).length !== 2 ||\n'
         '  p80MarrAnchors.filter((h) => h.year === 1885).length !== 7 ||')

REPLACEMENTS = [
    ('a  guard: HOUSE_VITALS.length !== 1949',
     'HOUSE_VITALS.length !== 1949',
     'HOUSE_VITALS.length !== 1951', 149),
    ('b  template: P237/P238/P239 veriga + P240 dodatek',
     B_OLD, B_NEW, 1),
    ('c  p80Marr.length !== 206',
     'p80Marr.length !== 206',
     'p80Marr.length !== 208', 1),
    ('c2 p115Marr.length !== 206',
     'p115Marr.length !== 206',
     'p115Marr.length !== 208', 1),
    ('d  p80MarrAnchors.length !== 199 (2x)',
     'p80MarrAnchors.length !== 199',
     'p80MarrAnchors.length !== 201', 2),
    ('e  sidra year-guard: + 1883:2 vrstica',
     E_OLD, E_NEW, 1),
    ('f  sidra message: 199 → 201 + 1883:2-P240!',
     'poročna sidra ≠ 199 (1882:1 · 1884:3-P239! · 1885:7',
     'poročna sidra ≠ 201 (1882:1 · 1883:2-P240! · 1884:3-P239! · 1885:7', 1),
    ('g  p116Marr.length !== 206 (8x)',
     'p116Marr.length !== 206',
     'p116Marr.length !== 208', 8),
    ('h  filter-04455-length !== 206 (28x)',
     'bookSignature === ' + Q + '04455' + Q + ').length !== 206',
     'bookSignature === ' + Q + '04455' + Q + ').length !== 208', 28),
    ('i  p152Blocks.length !== 206',
     'p152Blocks.length !== 206',
     'p152Blocks.length !== 208', 1),
    ('j  message: bloki 04455 ≠ 206 (27x)',
     'bloki 04455 ≠ 206',
     'bloki 04455 ≠ 208', 27),
    ('l  narrative: korpus: 1949/',
     'korpus: 1949/',
     'korpus: 1951/', 1),
    ('m  narrative: corpus: 1949/',
     'corpus: 1949/',
     'corpus: 1951/', 1),
    ('n  narrative: 288/1949 (2x)',
     '288/1949',
     '288/1951', 2),
    ('o  narrative: = 1949 blokov',
     '= 1949 blokov',
     '= 1951 blokov', 1),
    ('p  narrative: = 1949 blocks',
     '= 1949 blocks',
     '= 1951 blocks', 1),
    ('q  badge: vitals 1949 · 04104 288',
     'vitals 1949 · 04104 288',
     'vitals 1951 · 04104 288', 1),
    ('r  p239 narrative: 04455-206 → 208 (SI+EN zvezek)',
     R_OLD, R_NEW, 1),
]

text = original
for label, old, new, expected in REPLACEMENTS:
    n = text.count(old)
    if n != expected:
        print(f'ABORT [{label}]: pričakovano {expected}, najdeno {n} × {old[:80]!r} — NIČ NE PISAN', file=sys.stderr)
        sys.exit(1)
    text = text.replace(old, new)
    print(f'  ok [{label}] {n}/{expected}')

leftover_guard = text.count('HOUSE_VITALS.length !== 1949')
leftover_206 = text.count('.length !== 206')
if leftover_guard or leftover_206:
    print(f'ABORT: ostanki — guard-1949={leftover_guard}, length-206={leftover_206}', file=sys.stderr)
    sys.exit(1)

with open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(text)
print('ZAPISANO:', PATH)
