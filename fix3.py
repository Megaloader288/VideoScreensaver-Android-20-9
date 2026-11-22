import pathlib

def rep(s, old, new, count=1):
    assert s.count(old) == count, "not found %d times: %s" % (count, old[:60])
    return s.replace(old, new)

J = pathlib.Path("app/src/main/java/systems/sieber/vscreensaver")

# --- build.gradle: add ExoPlayer, minSdk 21 (required by media3)
p = pathlib.Path("app/build.gradle")
s = p.read_text()
s = rep(s, "minSdkVersion 17\n", "minSdkVersion 21\n")
s = rep(s, "    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'\n",
        "    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'\n    implementation 'androidx.media3:media3-exoplayer:1.3.1'\n")
p.write_text(s)

# --- VideoScreensaverView: gapless single-video loop with ExoPlayer
p = J / "VideoScreensaverView.java"
s = p.read_text()
s = rep(s, "import android.media.MediaPlayer;\n",
        "import android.media.MediaPlayer;\nimport androidx.media3.common.MediaItem;\nimport androidx.media3.common.PlaybackException;\nimport androidx.media3.common.Player;\nimport androidx.media3.exoplayer.ExoPlayer;\n")
s = rep(s, "    MediaPlayer mMediaPlayer = new MediaPlayer();\n",
        "    MediaPlayer mMediaPlayer = new MediaPlayer();\n    ExoPlayer mExo = null;\n")
s = rep(s, "                mMediaPlayer.setDisplay(holder);\n",
        "                if(mExo == null) mMediaPlayer.setDisplay(holder);\n", 2)
s = rep(s, "        mp.setLooping(mVideoUris.size() == 1",
        "        if(startGapless(mp, vol)) return;\n        mp.setLooping(mVideoUris.size() == 1")
s = rep(s, "    public void start() {\n        mVideoUris = getVideoUris(mSharedPref);\n",
        "    public void start() {\n        releaseGapless();\n        mVideoUris = getVideoUris(mSharedPref);\n")
p.write_text(s)

# --- stop calls: also stop ExoPlayer
for name, n in (("MainActivity.java", 1), ("FullscreenDream.java", 2)):
    p = J / name
    s = p.read_text()
    s = rep(s, "mScreensaverView.mMediaPlayer.stop();", "mScreensaverView.stopPlayback();", n)
    p.write_text(s)
print("gapless player patch applied")
