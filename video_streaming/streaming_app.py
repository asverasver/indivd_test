import time

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('streaming_template.html')


def get_frame():
    """Video streaming generator function."""
    cap = cv2.VideoCapture('static/double_decker_video.mp4')

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            ret2, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.025)

    cap.release()


@app.route('/stream_video_file')
def stream_video_file():
    return Response(get_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
