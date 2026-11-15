import glob,io,re
pat=re.compile(r'.*(VITALS_TOTAL|BLOKI_04894|KORPUS_HOUSES)\s*=\s*\d+.*')
from collections import Counter
c=Counter()
for p in glob.glob("scripts/p1[0-9][0-9]*.py"):
    s=io.open(p,encoding="utf-8").read()
    for m in pat.findall(s):
        pass
    for l in s.splitlines():
        if re.match(r'\s*(VITALS_TOTAL|BLOKI_04894|KORPUS_HOUSES)\s*=\s*\d+',l):
            c[re.match(r'\s*(\w+)\s*=\s*(\d+)',l).group(1)]+=1
print(c)
# sample I6a vitals lines
n=0
for p in sorted(glob.glob("scripts/p1[0-9][0-9]*.py")):
    s=io.open(p,encoding="utf-8").read()
    for l in s.splitlines():
        if re.search(r'(vitals|vit)\D{0,8}==\s*\d{3,4}',l) and "2081" not in l and "2043" not in l:
            print(p.split("\\")[-1],"|",l.strip()[:120]); n+=1
            if n>12: break
    if n>12: break
