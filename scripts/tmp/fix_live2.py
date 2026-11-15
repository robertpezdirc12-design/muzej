import glob,io,re
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)
changed=[]
for p in [x for x in glob.glob("scripts/*.py") if "localhost:3000" in io.open(x,encoding="utf-8").read()]:
    s=rd(p); orig=s
    if "BASE_URL" not in s:
        m=re.search(r'^ROOT = .*\n', s, re.M)
        if not m:
            m=re.search(r'^(?:import [^\n]*\n)+', s, re.M)
        assert m, p
        s = s[:m.end()] + 'BASE_URL = os.environ.get("MUZEJ_URL", "http://localhost:3000")\n' + s[m.end():]
    s = s.replace('f"{ROOT.replace(\'/home/z/my-project\', \'http://localhost:3000\')}/api/qa"', 'f"{BASE_URL}/api/qa"')
    s = s.replace('"http://localhost:3000/api/qa"', 'f"{BASE_URL}/api/qa"')
    s = s.replace('if live or "--check" not in sys.argv:', 'if live:')
    pat = re.compile(r'(# ——— I10: QA-živo ———\n)(.*?)(?=\n# ———|\Z)', re.S)
    m = pat.search(s)
    if m and 'if live:' not in m.group(2):
        body = m.group(2).rstrip("\n")
        indented = "\n".join(("    "+l if l.strip() else l) for l in body.split("\n"))
        new = m.group(1) + 'if live:\n' + indented + '\nelse:\n    print("[SKIP] I10 QA-živo — zazeni z --live ali MUZEJ_URL")\n'
        s = s[:m.start()] + new + s[m.end():]
    if s!=orig:
        wr(p,s); changed.append(p)
print("changed",len(changed)); print("\n".join(changed))
