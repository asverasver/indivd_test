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
import argparse
import sys
from time import sleep
from flask import Flask, render_template, Response
import cv2

DEFAULT_FRAMERATE = 30
MIN_FRAMERATE = 1
MAX_FRAMERATE = 120
ERROR_MESSAGE_IMAGE = 'static/playback_error.png'
NO_VIDEO_PATH_ERROR_MESSAGE = 'Error: video path is not provided.'\
                              'The application cannot be started'

app = Flask(__name__)


@app.route('/')
def index():
    """Returns the main page of the service, with embedded MJPEG translation."""
    return render_template('streaming_template.html')


def get_error_image_as_bytes() -> bytes:
    """Generates a bytes representation of the error message image."""
    with open(ERROR_MESSAGE_IMAGE, "rb") as image:
        error_image_as_bytes = bytearray(image.read())

    return error_image_as_bytes


def get_frame_as_bytes(video_file_path: str,
                       framerate: int = DEFAULT_FRAMERATE) -> bytes:
    """Generates a JPEG from the video file frames.

    Args:
      video_file_path: A path to the video file.
      framerate: Defines the timeout between frames (1/framerate).
                  Limited to MIN_FRAMERATE <= frame_rate <= MAX_FRAMERATE.

    Yields:
      Bytes representation of the next video frame as an JPEG, or of an error message image.
    """
    if not framerate or not (MIN_FRAMERATE <= framerate <= MAX_FRAMERATE):
        framerate = DEFAULT_FRAMERATE

    pause_between_frames = 1 / framerate

    capture = cv2.VideoCapture(video_file_path)

    # FIXME: does not return a proper image to the web page
    if not capture.isOpened():
        error_image_as_bytes = get_error_image_as_bytes()
        return (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + error_image_as_bytes + b'\r\n')

    while capture.isOpened():
        capture_return_code, frame = capture.read()
        if capture_return_code:
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            sleep(pause_between_frames)

    capture.release()


@app.route('/stream_video_file')
def stream_video_file():
    """Returns a response containing JPEG frames from the video."""
    video_file_path = app.config.get('video')
    framerate = app.config.get('framerate', DEFAULT_FRAMERATE)

    return Response(get_frame_as_bytes(video_file_path, framerate),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    """Here we parse args and start the service, if everything is OK"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', '-v', help='Path to the video file to be streamed')
    parser.add_argument('--framerate', '-f', help='Framerate for the video stream')
    args = parser.parse_args()

    if args.video:
        app.config['video'] = args.video
    else:
        print(NO_VIDEO_PATH_ERROR_MESSAGE)
        sys.exit(1)

    if args.framerate:
        app.config['framerate'] = args.framerate

    app.run(ssl_context=('cert.pem', 'key.pem'))
