import glob,io
fs=[p for p in glob.glob("scripts/*.py") if "localhost:3000" in io.open(p,encoding="utf-8").read()]
bad=[p for p in fs if "BASE_URL" not in io.open(p,encoding="utf-8").read()]
print("files",len(fs),"brez BASE_URL:",bad)
