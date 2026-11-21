import pathlib

p = pathlib.Path("app/src/main/res/layout/activity_main.xml")
s = p.read_text()
old = '    android:fitsSystemWindows="true"\n'
assert s.count(old) == 1, "fitsSystemWindows line not found"
p.write_text(s.replace(old, ""))

p = pathlib.Path("app/src/main/java/systems/sieber/vscreensaver/VideoScreensaverView.java")
s = p.read_text()
old = 'if(mSharedPref.getBoolean("video-stretch", true)) {'
assert s.count(old) == 1, "stretch line not found"
p.write_text(s.replace(old, "if(false) {"))
print("gray frame fix and fit mode applied")
