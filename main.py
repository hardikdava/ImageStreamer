
from image_streamer.flask.flask_app import app as FlaskApp
from image_streamer.fastapi.fastapi_app import app as FastapiApp
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app=FastapiApp)
    # FlaskApp.run(debug=True)


