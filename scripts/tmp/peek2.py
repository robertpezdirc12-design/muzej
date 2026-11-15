import io,re
for p in ["scripts/p252_parish_synthesis_04455.py","scripts/p243_parish_marriage_1880_04455.py","scripts/p257_1830_1831.py","scripts/p244_parish_marriage_1879_04455.py"]:
    ls=io.open(p,encoding="utf-8").read().splitlines()
    print("="*15,p)
    for i,l in enumerate(ls):
        if "api/qa" in l or "localhost:3000" in l:
            for j in range(max(0,i-8),min(len(ls),i+12)): print(j+1,ls[j])
            print("-"*40); break
