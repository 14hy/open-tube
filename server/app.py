from flask import Flask
from flask_cors import CORS
from api.api import api
from api.common import *

if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app)

    api.init_app(app)
    app.run(host=FLASK_CONFIG.host, port=FLASK_CONFIG.port, debug=FLASK_CONFIG.debug)
