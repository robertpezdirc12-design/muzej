import glob,io
rem=[p for p in glob.glob("scripts/*.py") if "/home/z/my-project" in io.open(p,encoding="utf-8").read()]
print("preostali hardcoded:",rem)
