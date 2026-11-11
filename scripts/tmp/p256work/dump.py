import json, sys, os

def load(f):
    raw = open(f).read().strip()
    if raw.startswith('```'):
        raw = raw.split('```')[1]
        if raw.startswith('json'): raw = raw[4:]
    try:
        return json.loads(raw), None
    except Exception as e:
        # poskusi popraviti: odstrani vrstico z 'Extra data'
        return None, raw

def dump(f, kind):
    d, raw = load(f)
    print(f"════ {os.path.basename(f)} ════")
    if d is None:
        print('  NAPAČEN-JSON:', (raw or '')[:250].replace('\n',' '))
        return
    for v in d.get('vrstice', []):
        if kind == 'G':
            print(f"  D:{v.get('datum')!r} V:{v.get('vas')!r} H:{v.get('hisa')} I:{v.get('ime')!r} S:{v.get('starost')} O:{str(v.get('opomba'))[:70]!r}")
        else:
            print(f"  V:{v.get('vas')!r} H:{v.get('hisa')} I:{v.get('ime')!r} S:{v.get('starost')} PR:{str(v.get('price'))[:55]!r}")
    print('  R:', (d.get('razlaga') or '')[:230])

for t in sys.argv[1:]:
    for g in ['G','B']:
        for h in ['T','B']:
            f = f'/tmp/p256/L/{t}_{g}{h}.json'
            if os.path.exists(f): dump(f, g)
