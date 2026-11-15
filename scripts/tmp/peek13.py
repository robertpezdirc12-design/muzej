import io,re
s=io.open("scripts/p176_parish_death_1910.py",encoding="utf-8").read()
for m in re.finditer(r'.*p80.*',s):
    print(m.group(0)[:130])
