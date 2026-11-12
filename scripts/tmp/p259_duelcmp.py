#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P259 — DUEL-CMP: primerjava neodvisnih VLM validacij (duel-vals/) z integriranimi odgovori.
Izpis: verdikt tabela + status (POTRJENO / SPOR / NAPAKA)."""
import json
import re
import os

OUT = 'research/issue17/p259-work/duel-vals'

def load(name):
    p = os.path.join(OUT, f'{name}.json')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'^```json|```$', '', s, flags=re.M).strip()
    # najdi prvi { in zadnji }
    a, b = s.find('{'), s.rfind('}')
    return json.loads(s[a:b+1])

# ——— INTEGRIRANI ODGOVORI (parish.ts + module-p259.txt + datcol/pass1 sinteza) ———
INTEGRIRANO = {
  's11_dates': {'rows': {**{i: '6. Febr' for i in range(1, 9)}, **{i: '13. Febr' for i in range(9, 14)}}, 'leto': 1833},
  's11_r2_gosling': {'zenin': 'PESDIRZ (ne Gosling)', 'hisZenin': '53 (ne 33)', 'nevesta': 'BRING', 'hisNevesta': '24'},
  's12_dates': {'rows': {1: '19. Febr', 2: '19. d°', 3: '21. April', 4: '5. Mai', 5: '19. Oct (rob-25-prečrtan)',
                          6: '27. Nov (rob-1)', 7: '22. Jän', 8: 'd° (22.)', 9: '29. Jän', 10: '29. d°', 11: '29. d°', 12: '29. d°'},
                 'letoR1': 1833, 'letoR7': 1834},
  's12_r1_r2': {'r1': {'zenin': 'Hofferer|Hohenauer (eden od teh)', 'hisZenin': '13'},
                 'r2': {'datum': '19. d° Febr 1833 (ne 12. dito!)'}},
  's12_r7_restart': {'datum': '22. Jän 1834 (ne 27.)', 'leto': 1834},
  's13_r1_restart': {'datum': '5. Febr 1834 (ne 8.)', 'rob': 8},
  's13_dates': {'rows': {**{i: '5. Febr' for i in range(1, 8)}, 8: '9. Febr', 9: '10. Febr', 10: '10. d°', 11: '10. d°'},
                 'robovi': '1–7 → rob 8–14, 8 → rob 15, 9–11 → rob 16–18', 'leto': 1834},
  's13_r6_vrh': {'zenin': 'VRH (Marcus)', 'hisZenin': '68 (ne 58)', 'nevesta': 'HARAGHINIGH', 'hisNevesta': '51'},
  's13_r11_marentic': {'datum': '10. Febr (ne 17.)', 'nevesta': 'MARENTICH', 'hisNevesta': '24 ali 29', 'leto': 1834},
}

def norm(s):
    return re.sub(r'[^a-z0-9]', '', str(s).lower())

def verdict(name, v):
    intg = INTEGRIRANO[name]
    checks = []
    if name == 's11_r2_gosling':
        g = f"{v.get('zenin','')} {v.get('vasZenin','')}"
        checks.append(('ženin=PESDIRZ', 'pesdirz' in norm(g) or 'gospodirz' in norm(g), norm(g)[:60]))
        checks.append(('hiša-ženina=53', norm(v.get('hisZenin')) == '53', str(v.get('hisZenin'))))
        checks.append(('nevesta=BRING', 'bring' in norm(v.get('nevesta')), norm(v.get('nevesta'))[:60]))
        checks.append(('hiša-neveste=24', norm(v.get('hisNevesta')) == '24', str(v.get('hisNevesta'))))
    elif name in ('s13_r6_vrh',):
        g = f"{v.get('zenin','')} {v.get('vasZenin','')}"
        checks.append(('ženin=VRH-jedro', 'vrh' in norm(g) or 'vrb' in norm(g), norm(g)[:60]))
        checks.append(('hiša-ženina=68', norm(v.get('hisZenin')) == '68', str(v.get('hisZenin'))))
        checks.append(('nevesta-HARAGH-jedro', 'harag' in norm(v.get('nevesta')) or 'karaf' in norm(v.get('nevesta')) or 'haragh' in norm(v.get('nevesta')), norm(v.get('nevesta'))[:60]))
        checks.append(('hiša-neveste=51', norm(v.get('hisNevesta')) == '51', str(v.get('hisNevesta'))))
    elif name == 's13_r11_marentic':
        checks.append(('datum=10. Febr', '10' in str(v.get('datum', '')) and '17' not in str(v.get('datum', '')), str(v.get('datum'))))
        checks.append(('nevesta=MARENTI-jedro', 'marenti' in norm(v.get('nevesta')) or 'marcutei' in norm(v.get('nevesta')), norm(v.get('nevesta'))[:60]))
        hz = str(v.get('hisNevesta'))
        checks.append(('hiša-neveste=24|29', norm(hz) in ('24', '29'), hz))
        checks.append(('leto=1834', str(v.get('leto')) == '1834' or '1834' in str(v.get('datum', '')), f"{v.get('leto')}"))
    elif name in ('s12_r7_restart', 's13_r1_restart'):
        dt = str(v.get('datum', ''))
        want = intg['datum']
        day = want.split('.')[0]
        bad = want.split('ne ')[-1].rstrip(')').split('.')[0] if ' ne ' in want else None
        ok = norm(day) in norm(dt) and (bad is None or norm(bad) not in norm(dt))
        checks.append((f'datum={want}', ok, dt))
        checks.append(('leto=1834', str(v.get('leto')) == '1834' or '1834' in norm(dt), f"{v.get('leto')}"))
    elif name == 's12_r1_r2':
        r1, r2 = v.get('r1', {}), v.get('r2', {})
        checks.append(('r1-ženin=Hofferer|Hohenauer-jedro', any(x in norm(r1.get('zenin', '')) for x in ('hofferer', 'hohenauer', 'haunauer', 'hogenauer')), norm(r1.get('zenin', ''))[:60]))
        checks.append(('r1-hiša=13', norm(r1.get('hisZenin')) == '13', str(r1.get('hisZenin'))))
        d2 = str(r2.get('datum', ''))
        checks.append(('r2-datum=19. Febr (ne 12.)', '19' in norm(d2) and '12' not in norm(d2), d2))
    elif name == 's11_dates':
        rows = {int(r.get('r')): str(r.get('datum', '')) for r in v.get('rows', [])}
        want6 = [i for i, d in intg['rows'].items() if d == '6. Febr']
        want13 = [i for i, d in intg['rows'].items() if d == '13. Febr']
        ok6 = sum(1 for i in want6 if '6' in norm(rows.get(i, '')) and '13' not in norm(rows.get(i, '')))
        ok13 = sum(1 for i in want13 if '13' in norm(rows.get(i, '')) or 'dito' in str(rows.get(i, '')).lower())
        checks.append((f'6.-Febr-kaskada r1–r8 ({ok6}/8)', ok6 >= 7, str(ok6)))
        checks.append((f'13.-Febr r9–r13 ({ok13}/5)', ok13 >= 4, str(ok13)))
    elif name == 's12_dates':
        rows = {int(r.get('r')): f"{r.get('datum','')} {r.get('leto') or ''}" for r in v.get('rows', [])}
        pairs = [(1, '19'), (2, '19'), (3, '21'), (4, '5'), (5, '19'), (6, '27'), (7, '22'), (9, '29'), (10, '29'), (11, '29'), (12, '29')]
        oks = []
        for r, day in pairs:
            dt = norm(rows.get(r, ''))
            ok = day in dt and not (r == 2 and '12' in dt and '19' not in dt) and not (r == 5 and '10' in dt and '19' not in dt and '26' not in dt)
            oks.append(ok)
        n = sum(oks)
        checks.append((f'datumi r1–r12 ({n}/11)', n >= 9, str(n)))
        ok1833 = any('1833' in norm(rows.get(1, '')) for _ in [0])
        ok1834 = any('1834' in norm(rows.get(7, '')) for _ in [0])
        checks.append(('r1-leto=1833', ok1833, rows.get(1, '')[:50]))
        checks.append(('r7-leto=1834-RESTART', ok1834, rows.get(7, '')[:50]))
    elif name == 's13_dates':
        rows = {int(r.get('r')): f"{r.get('datum','')}|rob={r.get('rob')}" for r in v.get('rows', [])}
        five = sum(1 for i in range(1, 8) if '5' in norm(rows.get(i, '')) and '8' not in str(rows.get(i, '')).replace('1834', ''))
        nine = sum(1 for i in [8] if '9' in norm(rows.get(i, '')))
        ten = sum(1 for i in (9, 10, 11) if '10' in norm(rows.get(i, '')))
        checks.append((f'5.-Febr ×7 r1–r7 ({five}/7)', five >= 6, str(five)))
        checks.append(('9.-Febr r8', nine == 1, rows.get(8, '')[:40]))
        checks.append((f'10.-Febr ×3 r9–r11 ({ten}/3)', ten >= 2, str(ten)))
    return checks

names = ['s11_dates', 's12_dates', 's13_dates', 's11_r2_gosling', 's12_r1_r2', 's12_r7_restart', 's13_r1_restart', 's13_r6_vrh', 's13_r11_marentic']
total_ok, total_all = 0, 0
for n in names:
    try:
        v = load(n)
    except Exception as e:
        print(f'== {n}: PARSE-NAPAKA {e}')
        continue
    print(f'== {n}')
    for label, ok, detail in verdict(n, v):
        total_all += 1; total_ok += ok
        print(f'  {"✓" if ok else "✗"} {label} :: {detail[:70]}')
print(f'\nSKUPAJ: {total_ok}/{total_all} ok')
