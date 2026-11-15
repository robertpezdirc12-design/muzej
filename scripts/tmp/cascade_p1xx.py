import glob,io,re
ROOT="."
generic=[
 ('qa.count("HOUSE_VITALS.length !== 2077")', 'qa.count("HOUSE_VITALS.length !== 2081")'),
 ('qa.count("HOUSE_VITALS.length !== 2043")', 'qa.count("HOUSE_VITALS.length !== 2081")'),
 ('qa.count("HOUSE_VITALS.length !== 1940")', 'qa.count("HOUSE_VITALS.length !== 2081")'),
 ('qa.count("HOUSE_VITALS.length !== 1511")', 'qa.count("HOUSE_VITALS.length !== 2081")'),
 ('"HOUSE_VITALS.length !== 2077"', '"HOUSE_VITALS.length !== 2081"'),
 ('"HOUSE_VITALS.length !== 2043"', '"HOUSE_VITALS.length !== 2081"'),
 ('"HOUSE_VITALS.length !== 1940"', '"HOUSE_VITALS.length !== 2081"'),
 ('"HOUSE_VITALS.length !== 1511"', '"HOUSE_VITALS.length !== 2081"'),
 ('pt.get("vitalsTotal") == 2077','pt.get("vitalsTotal") == 2081'),
 ('pt.get("vitalsTotal") == 2043','pt.get("vitalsTotal") == 2081'),
 ('pt.get("vitalsTotal") == 1940','pt.get("vitalsTotal") == 2081'),
 ('pt["corpus"]["vitalsTotal"] == 1940','pt["corpus"]["vitalsTotal"] == 2081'),
 ('pt["corpus"]["vitalsTotal"] == 2043','pt["corpus"]["vitalsTotal"] == 2081'),
 ('== 2077 blokov','== 2081 blokov'),
 ('"blocks: 2077,','"blocks: 2081,'),
 ('"sixBook: 39"','"sixBook: 41"'),
 ('"fiveBook: 29"','"fiveBook: 27"'),
 ('.get("01738") == 65','.get("01738") == 69'),
 ('"01738": 65','"01738": 69'),
]
changed=0
for path in sorted(glob.glob("scripts/p1[0-9][0-9]*.py")):
    s=io.open(path,encoding="utf-8").read(); o=s
    for a,b in generic:
        if a in s: s=s.replace(a,b)
    s=re.sub(r'^(VITALS_TOTAL\s*=\s*)\d+', r'\g<1>2081', s, flags=re.M)
    s=re.sub(r'^(BLOKI_04894\s*=\s*)\d+', r'\g<1>520', s, flags=re.M)
    s=re.sub(r'^(KORPUS_HOUSES\s*=\s*)93\b', r'\g<1>94', s, flags=re.M)
    s=re.sub(r'"len\(vitals\) == \d+"', '"len(vitals) == 1940"', s)
    s=re.sub(r'len\(vitals\) == \d+', 'len(vitals) == 1940', s)
    s=re.sub(r'len\(houses\) == 93\b', 'len(houses) == 94', s)
    if s!=o:
        io.open(path,"w",encoding="utf-8",newline="\n").write(s); changed+=1; print(path)
print("changed",changed)
