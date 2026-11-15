import io
ls=io.open(r"scripts/p200_parish_death_1877_04106.py",encoding="utf-8").read().splitlines()
for i,l in enumerate(ls):
    if "04894=" in l or "bookSignature: \\\"04894\\\"" in l or "src.count(" in l:
        print(i+1,l)
