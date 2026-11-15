import io
s=io.open("scripts/p250_parish_marriage_1874_04455.py",encoding="utf-8").read()
i=s.find("/api/qa")
print(s[max(0,i-400):i+200])
