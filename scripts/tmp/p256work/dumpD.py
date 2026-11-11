import json, os
for f in sorted(os.listdir('/tmp/p256/D')):
    if not f.endswith('.json'): continue
    raw = open('/tmp/p256/D/'+f).read().strip()
    if raw.startswith('```'):
        raw = raw.split('```')[1]
        if raw.startswith('json'): raw = raw[4:]
    print(f"══ {f[:-5]} ══")
    try:
        d = json.loads(raw)
        if 'hisa' in d:
            print(f"  vas={d.get('vas')!r} hisa={d.get('hisa')} vsebina={d.get('vsebina')!r}")
            print(f"  razlaga: {(d.get('razlaga') or '')[:180]}")
        else:
            print(f"  zapis={d.get('zapis')!r} dan={d.get('dan')} mesec={d.get('mesec')!r} leto={d.get('leto')}")
            print(f"  razlaga: {(d.get('razlaga') or '')[:180]}")
    except Exception as e:
        print('  ERR', raw[:200])
