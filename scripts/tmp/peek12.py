import io
ls=io.open("scripts/p176_parish_death_1910.py",encoding="utf-8").read().splitlines()
for i in range(0,40): print(i+1,ls[i][:140])
