import glob,io
bad=[]
for p in sorted(glob.glob("scripts/*.py")):
    s=io.open(p,encoding="utf-8").read()
    try: compile(s,p,"exec")
    except SyntaxError as e: bad.append((p,e.lineno,str(e)[:60]))
print("syntax errors:",len(bad))
for b in bad: print(b)
