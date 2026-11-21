import pathlib
p = pathlib.Path("app/src/main/res/layout/activity_main.xml")
s = p.read_text()
old = '    android:fitsSystemWindows="true"\n'
assert s.count(old) == 1, "fitsSystemWindows line not found"
p.write_text(s.replace(old, ""))
print("gray frame fix applied")
