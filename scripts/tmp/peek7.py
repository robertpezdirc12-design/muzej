import io
ls=io.open("scripts/p243_parish_marriage_1880_04455.py",encoding="utf-8").read().splitlines()
for i in range(76,100): print(i+1,ls[i][:120])
