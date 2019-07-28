from flask import Flask
from api import api
from api.common import *

if __name__ == "__main__":
    app = Flask(__name__)

    api.init_app(app)
    app.run(host=CONFIG['host'], port=CONFIG['port'], debug=CONFIG['debug'])
