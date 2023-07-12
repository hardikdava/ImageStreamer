import os.path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from image_streamer.vision import Vision

app = FastAPI()

vision = Vision()
template_directory = os.path.join(os.getcwd(), "image_streamer", "templates")
templates = Jinja2Templates(directory=template_directory)


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
):
    return templates.TemplateResponse("index.html", context={"request": request})


def gen_frames():
    while True:
        buffer = vision.read(encode=True)  # read the camera frame
        if buffer is None:
            continue
        frame = buffer.tobytes()
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )  # concat frame one by one and show result


@app.get("/video_feed")
def video_feed():
    vision.start_capturing()
    return StreamingResponse(
        gen_frames(), media_type="multipart/x-mixed-replace;boundary=frame"
    )
