import io
def rd(p): return io.open(p,encoding="utf-8").read()
def wr(p,s): io.open(p,"w",encoding="utf-8",newline="\n").write(s)

# p176
p="scripts/p176_parish_death_1910.py"; s=rd(p)
old='''          f"{qa.count(\'=== \\"04894\\" && v.year === 1910\')}")'''
assert old in s, "p176 anchor"
s=s.replace(old,'''          f"{n1910}")''')
s=s.replace('''    check("I10e P176-allow-listi (h7/h90 + h91 + h14 + h49 — 1910!)",
          qa.count(\'=== "04894" && v.year === 1910\') == 4,''',
'''    n1910 = qa.count(\'=== "04894" && v.year === 1910\')
    check("I10e P176-allow-listi (h7/h90 + h91 + h14 + h49 — 1910!)",
          n1910 == 4,''')
wr(p,s)

# p192, p199, p200
specs=[("scripts/p192_parish_death_1885_04106.py","n04106","04106"),
       ("scripts/p199_parish_death_1878_04106.py","n04894","04894"),
       ("scripts/p200_parish_death_1877_04106.py","n04894","04894")]
for p,var,sig in specs:
    s=rd(p)
    cnt=f"src.count('bookSignature: \"{sig}\"')"
    broken=f"f\"{sig}-bloki={{{cnt}}}\")" if sig=="04106" else f"f\"04894={{src.count('bookSignature: \\\"{sig}\\\"')}}\")"
    if sig=="04106":
        broken="f\"04106-bloki={src.count('bookSignature: \\\"04106\\\"')}\")"
    else:
        broken="f\"04894={src.count('bookSignature: \\\"04894\\\"')}\")"
    assert broken in s, (p, broken)
    label="04106-bloki" if sig=="04106" else "04894"
    s=s.replace(broken, f'f"{label}={{{var}}}")')
    # insert variable line before the check(
    anchor=f'check("I10 04894-still-520"' if sig=="04894" else 'check("I3 vitals-1940 + 04106==433"'
    assert anchor in s
    s=s.replace(anchor, f'{var} = src.count(\'bookSignature: "{sig}"\')\n'+anchor, 1)
    wr(p,s)
print("syntax fixed")
