import glob,io,re
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
changed=[]
for p in sorted(glob.glob("scripts/p1[0-9][0-9]*.py")):
    s=rd(p); orig=s
    def repl(m):
        inner=m.group(1)
        if "encoding" in inner: return m.group(0)
        if re.search(r"['\"]([rwa]b|b[rwa]?)['\"]", inner): return m.group(0)
        return f"open({inner}, encoding=\"utf-8\")"
    s=re.sub(r'\bopen\(([^()]*)\)', repl, s)
    if s!=orig:
        wr(p,s); changed.append(p)
print(len(changed)); print("\n".join(changed[:20]))
