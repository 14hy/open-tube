from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
import os

app = Flask(__name__)
CORS(app)
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{POSTGRES_PASSWORD}@210.89.189.25:5432'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db 연결
db = SQLAlchemy(app)

api = Api(app, version="1.0", title="OPEN TUBE", description="OPEN TUBE API")

from controller.history import api_history
from controller.download import api_download
from controller.get_reply_text import api_reply
from controller.get_reply_keywords import api_keywords
from controller.video import api_video

api.add_namespace(api_history)
api.add_namespace(api_download)
api.add_namespace(api_reply)
api.add_namespace(api_keywords)
api.add_namespace(api_video)
