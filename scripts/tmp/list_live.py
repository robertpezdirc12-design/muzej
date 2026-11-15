import glob,io
fs=[p for p in glob.glob("scripts/*.py") if "localhost:3000" in io.open(p,encoding="utf-8").read()]
print(len(fs)); print("\n".join(fs))
