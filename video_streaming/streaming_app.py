#!/usr/bin/python3
"""This is a web service that streams a video file as an MJPEG stream

The service has a REST interface and takes a video file name as a
required parameter, when in started from terminal. If the parameter
is not provided, or the file specified cannot be opened (it does not
exist, the app does not have sufficient permissions, etc.), an error
image is shown.
Also, to show the video with an appropriate speed, a framerate
parameter can be passed. It has default value of 30 frames per second,
and

  Typical usage example:

  !!! add a terminal example

  Typical usage example with the framerate parameter specified:

  !!! add a terminal example

  To see the streaming, open https://127.0.0.1:5000/ in a browser that
  supports MJPEG playback.
"""

from time import sleep
from flask import Flask, render_template, Response
import cv2


DEFAULT_FRAME_RATE = 30
ERROR_MESSAGE_IMAGE = 'static/playback_error.png'

app = Flask(__name__)


@app.route('/')
def index():
    """Returns the main page of the service, with embedded MJPEG translation."""
    return render_template('streaming_template.html')


def get_frame(video_file_path: str,
              frame_rate: int = DEFAULT_FRAME_RATE) -> bytes:
    """Generates a JPEG from the video file frames.

    Args:
      video_file_path: A path to the video file.
      frame_rate: Defines the timeout between frames (1/frame_rate).
                  Limited to 1 <= frame_rate <= 120.

    Yields:
      Next video frame as a JPEG, or an error message image.
    """

    cap = cv2.VideoCapture(video_file_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            ret2, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            sleep(0.025)

    cap.release()


@app.route('/stream_video_file')
def stream_video_file():
    """Returns a response containing JPEG frames from the video."""
    return Response(get_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
