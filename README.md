# indivd_test

This is a web service that streams a video file as an MJPEG stream.

The service has a REST interface and takes a video file name as arequired parameter (`--video="video.mp4"` or `-v="video.mp4"`), when itstarted from terminal. If the parameter is not provided, or the filespecified cannot be opened (it does not exist, the app does not havesufficient permissions, etc.), an error image is shown.Also, to show the video with an appropriate speed, a framerateparameter can be passed (`--framerate=10` or `-f=10`). It has the defaultvalue of 30 frames per second, and limited to `MIN_FRAMERATE <= framerate <= MAX_FRAMERATE`.

To remove any pauses between frames, simply comment the line with the sleep function call:
```python
# sleep(pause_between_frames)
```
Typical usage example:
```bash
% python streaming_app.py --video="double_decker_video.mp4"
```
or
```bash
% python streaming_app.py -v="double_decker_video.mp4"
```
Typical usage example with the framerate parameter specified:
```bash
% python streaming_app.py --video="double_decker_video.mp4" --framerate=10
```
To see the streaming, open https://127.0.0.1:5000/ in a browser that supports MJPEG playback.
