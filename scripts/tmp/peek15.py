import io,re
for p in ["p192_parish_death_1885_04106.py","p193_parish_death_1884_04106.py","p194_parish_death_1883_04106.py","p195_parish_death_1882_04106.py","p196_parish_death_1881_04106.py","p197_parish_death_1880_04106.py","p198_parish_death_1879_04106.py","p199_parish_death_1878_04106.py"]:
    s=io.open("scripts/"+p,encoding="utf-8").read()
    print(p, re.findall(r'.*\bst\b *=.*',s)[:3])
