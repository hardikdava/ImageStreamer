from sanic import Sanic, response

from image_streamer.vision import Vision

app = Sanic(name="ImageStreamer")

vision = Vision()


async def gen_frames(_response):
    while True:
        buffer = vision.read(encode=True)  # read the camera frame
        if buffer is None:
            continue
        frame = buffer.tobytes()
        data = b"".join(
            [b"--frame\r\nContent-Type: image/jpeg\r\n\r\n", frame, b"\r\n"]
        )
        await _response.send(data)


# async def video_feed(request):
#     response = await request.respond()
#     vision.start_capturing()
#     return ResponseStream(
#         gen_frames(response),
#         content_type='multipart/x-mixed-replace; boundary=frame'
#     )


@app.route("/video_feed")
async def camera_stream(request):
    _response = await request.respond()
    headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0",
        "Pragma": "no-cache",
        "Content-Type": "multipart/x-mixed-replace;boundary=--jpgboundary",
        "Connection": "close",
    }

    return await response.ResponseStream(
        gen_frames(_response),
        content_type="multipart/x-mixed-replace; boundary=frame",
        headers=headers,
    )
