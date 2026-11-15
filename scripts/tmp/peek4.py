import io
for p,ln in [("scripts/p176_parish_death_1910.py",303),("scripts/p192_parish_death_1885_04106.py",37),("scripts/p199_parish_death_1878_04106.py",94),("scripts/p200_parish_death_1877_04106.py",89)]:
    ls=io.open(p,encoding="utf-8").read().splitlines()
    print("="*10,p)
    for i in range(ln-2,min(len(ls),ln+1)): print(i+1,ls[i])
