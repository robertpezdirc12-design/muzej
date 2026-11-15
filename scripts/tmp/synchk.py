import glob,py_compile,os
bad=[]
for p in sorted(glob.glob("scripts/**/*.py",recursive=True)):
    try: py_compile.compile(p, cfile=os.devnull, doraise=True)
    except Exception as e: bad.append((p,str(e).splitlines()[-1][:80]))
print("syntax errors:",len(bad))
for b in bad: print(b)
