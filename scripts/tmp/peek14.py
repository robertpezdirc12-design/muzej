import io,re
for p in ["p192_parish_death_1885_04106.py","p193_parish_death_1884_04106.py","p194_parish_death_1883_04106.py","p195_parish_death_1882_04106.py","p196_parish_death_1881_04106.py","p197_parish_death_1880_04106.py","p198_parish_death_1879_04106.py","p199_parish_death_1878_04106.py"]:
    ls=io.open("scripts/"+p,encoding="utf-8").read().splitlines()
    print("="*10,p)
    for i,l in enumerate(ls):
        if "I5 qa-" in l or "I9b pt-luknja" in l or "I9 pt-luknja" in l:
            for j in range(i,min(len(ls),i+3)): print("   ",j+1,ls[j][:150])
