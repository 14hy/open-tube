from flask_restplus import Api, Resource
from api.v1.index import api as v1_index
from api.v1.service.index import api as v1_service
from api.common import *

api = Api(version=CONFIG['version'], title=CONFIG['title'], description=CONFIG['description'])

api.add_namespace(v1_index)
api.add_namespace(v1_service)
