from flask import Flask, Response, render_template

from image_streamer.vision import Vision

app = Flask(__name__, template_folder="../templates")

vision = Vision()


@app.route("/")
def index() -> str:
    return render_template("index.html")


def gen_frames():
    while True:
        buffer = vision.read(encode=True)  # read the camera frame
        if buffer is None:
            continue
        frame = buffer.tobytes()
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )  # concat frame one by one and show result


@app.route("/video_feed")
def video_feed():
    vision.start_capturing()
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
