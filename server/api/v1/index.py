from flask_restplus import Resource, Namespace

api = Namespace(name='v1', description='version-1')


@api.route('/')
class Index(Resource):
    @api.doc('Index', params={'params': 'param message'})
    def get(self, params):
        return 'Index Message, param: {}'.format(params)
