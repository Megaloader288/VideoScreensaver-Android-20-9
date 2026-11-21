import pathlib
d = pathlib.Path("app/src/main/java/systems/sieber/vscreensaver")

def rep(s, old, new):
    assert s.count(old) == 1, "not found: " + old[:60]
    return s.replace(old, new)

p = d / "VideoScreensaverView.java"
s = p.read_text()
a = s.index("        DisplayMetrics displayMetrics = new DisplayMetrics();\n        ((Activity) getContext())")
b = s.index("        mVideoView.setLayoutParams(layoutParams);")
nb = '''        int screenWidth = getWidth();
        int screenHeight = getHeight();
        if(screenWidth <= 0 || screenHeight <= 0) {
            DisplayMetrics dm = new DisplayMetrics();
            WindowManager wm = (WindowManager) getContext().getSystemService(Context.WINDOW_SERVICE);
            wm.getDefaultDisplay().getRealMetrics(dm);
            screenWidth = dm.widthPixels;
            screenHeight = dm.heightPixels;
        }
        int pivotPointX = 0;
        int pivotPointY = 0;
        float scaleY = 1.0f;
        float scaleX = 1.0f;
        ViewGroup.LayoutParams layoutParams = mVideoView.getLayoutParams();
        if(mSharedPref.getBoolean("video-stretch", true)) {
            float videoAspect = (float) videoWidth / videoHeight;
            float screenAspect = (float) screenWidth / screenHeight;
            if(screenAspect > videoAspect) {
                scaleY = (screenWidth / videoAspect) / screenHeight;
            } else {
                scaleX = (screenHeight * videoAspect) / screenWidth;
            }
            pivotPointX = screenWidth / 2;
            pivotPointY = screenHeight / 2;
            layoutParams.width = screenWidth;
            layoutParams.height = screenHeight;
        } else {
            float ratioWidth = (float) screenWidth / videoWidth;
            float ratioHeight = (float) screenHeight / videoHeight;
            float aspectRatio = (float) videoWidth / videoHeight;
            if(ratioWidth > ratioHeight) {
                layoutParams.width = (int) (screenHeight * aspectRatio);
                layoutParams.height = screenHeight;
            } else {
                layoutParams.width = screenWidth;
                layoutParams.height = (int) (screenWidth / aspectRatio);
            }
        }

'''
s = s[:a] + nb + s[b:]
s = s.replace("import android.app.Activity;\n", "", 1)
p.write_text(s)

p = d / "BaseSettingsActivity.java"
s = p.read_text()
s = rep(s, '"video-stretch", false)', '"video-stretch", true)')
p.write_text(s)

p = d / "FullscreenDream.java"
s = p.read_text()
s = rep(s, "import android.view.View;\n", "import android.view.View;\nimport android.view.Window;\nimport android.view.WindowManager;\n")
s = rep(s, "        setFullscreen(true);\n", "        setFullscreen(true);\n        extendWindowToFullDisplay();\n")
s = rep(s, "    private void initContentView() {", '''    private void extendWindowToFullDisplay() {
        Window window = getWindow();
        if(window == null) return;
        window.addFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            WindowManager.LayoutParams lp = window.getAttributes();
            lp.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            window.setAttributes(lp);
        }
    }

    private void initContentView() {''')
s = rep(s, "View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);", "View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);")
p.write_text(s)
print("fullscreen fix applied")
