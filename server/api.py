from flask_restplus import Api
from api.v1.resources.reply import api as v1_reply
from api.common import *

api = Api(version=FLASK_CONFIG.version, title=FLASK_CONFIG.title, description=FLASK_CONFIG.description)

api.add_namespace(v1_reply)
