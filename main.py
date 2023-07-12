
from image_streamer.flask.flask_app import app as FlaskApp
from image_streamer.fastapi.fastapi_app import app as FastapiApp
# from image_streamer.sanic.sanic_app import app as SanicApp
import uvicorn
from image_streamer.tornado.tornado_app import TornadoApp
import tornado

if __name__ == "__main__":

    # uvicorn.run(app=FastapiApp)
    # FlaskApp.run(debug=True)
    # bind server on 8080 port
    app = TornadoApp()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()


