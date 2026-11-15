import io
ls=io.open("scripts/p176_parish_death_1910.py",encoding="utf-8").read().splitlines()
for i,l in enumerate(ls):
    if "I6a vitals" in l or "I6e p80-skripta" in l or "I6f korpus" in l or "I10b qa-parish" in l or "I10c qa-parish" in l or "I10d qa-parish" in l or "I11d ni-04894" in l:
        for j in range(i,min(len(ls),i+3)): print(j+1,ls[j][:150])
        print("-"*30)
