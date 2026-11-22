import pathlib

p = pathlib.Path("app/src/main/java/systems/sieber/vscreensaver/VideoScreensaverView.java")
s = p.read_text()
methods = '''    private boolean startGapless(final MediaPlayer mp, float vol) {
        if(mVideoUris == null || mVideoUris.size() != 1) return false;
        if(!mSharedPref.getBoolean("video-loop", true)) return false;
        try {
            releaseGapless();
            final ExoPlayer exo = new ExoPlayer.Builder(getContext()).build();
            mExo = exo;
            exo.setVolume(vol);
            exo.setRepeatMode(Player.REPEAT_MODE_ONE);
            exo.setVideoSurfaceView(mVideoView);
            exo.addListener(new Player.Listener() {
                @Override
                public void onPlayerError(PlaybackException error) {
                    Log.e("ExoPlayer", "falling back to MediaPlayer", error);
                    post(new Runnable() {
                        @Override
                        public void run() {
                            releaseGapless();
                            try {
                                mp.setDisplay(mVideoView.getHolder());
                                mp.setLooping(true);
                                mp.start();
                            } catch(Exception e) {
                                e.printStackTrace();
                            }
                        }
                    });
                }
            });
            exo.setMediaItem(MediaItem.fromUri(Uri.parse(mVideoUris.get(0))));
            exo.prepare();
            exo.play();
            return true;
        } catch(Throwable t) {
            Log.e("ExoPlayer", "gapless start failed", t);
            releaseGapless();
            return false;
        }
    }

    void releaseGapless() {
        if(mExo != null) {
            try { mExo.release(); } catch(Exception ignored) {}
            mExo = null;
        }
    }

    void stopPlayback() {
        try { mMediaPlayer.stop(); } catch(Exception ignored) {}
        releaseGapless();
    }

'''
old = "    static ArrayList<String> getVideoUris("
assert s.count(old) == 1, "getVideoUris not found"
p.write_text(s.replace(old, methods + old))
print("gapless methods added")
