import time

import tornado.httpserver
import tornado.ioloop
import tornado.process
import tornado.web

from image_streamer.vision import Vision

vision = Vision()


class StreamHandler(tornado.web.RequestHandler):
    async def get(self):
        vision.start_capturing()
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header(
            "Cache-Control",
            "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0",
        )
        self.set_header("Pragma", "no-cache")
        self.set_header(
            "Content-Type", "multipart/x-mixed-replace;boundary=--jpgboundary"
        )
        self.set_header("Connection", "close")

        self.served_image_timestamp = time.time()
        while True:
            # Generating images for mjpeg stream and wraps them into http resp
            encoded_frame = vision.read(encode=True)
            if encoded_frame is None:
                continue
            frame = encoded_frame.tobytes()

            self.write("--jpgboundary\n")
            self.write("Content-type: image/jpeg\r\n")
            self.write(f"Content-length: {len(frame)}\r\n\r\n")
            self.write(frame)
            await self.flush()


def TornadoApp():
    # add handlers
    return tornado.web.Application(
        [
            (r"/video_feed", StreamHandler),
        ],
    )
