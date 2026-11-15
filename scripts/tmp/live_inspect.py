import io,re
for p in ["scripts/p243_parish_marriage_1880_04455.py","scripts/p252_parish_synthesis_04455.py","scripts/p257_1830_1831.py"]:
    s=io.open(p,encoding="utf-8").read()
    print("="*20,p)
    for m in re.finditer(r'.*(3000|--live|urlopen|LIVE|/api/qa).*', s):
        print(m.group(0)[:160])
