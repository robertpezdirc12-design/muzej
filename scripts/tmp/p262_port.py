import glob,io
hits=[p for p in glob.glob("scripts/*.py") if "/home/z/my-project" in io.open(p,encoding="utf-8",errors="ignore").read()]
print(len(hits),"files"); print("\n".join(hits[:12]))
