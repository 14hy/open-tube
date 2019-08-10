from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from controlller.reply import extract_reply
app = Flask(__name__)
CORS(app)
app.config.from_pyfile("db.cfg")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db 연결
db = SQLAlchemy(app)

api = Api(app, version="1.0", title="OPEN TUBE", description="OPEN TUBE API")

api.add_namespace(extract_reply, path="/extract")

