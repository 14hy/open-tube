from flask_restplus import Resource, Namespace

api = Namespace(name='v1/service', description='service')


@api.route('/')
class Service(Resource):
    @api.doc('Service', params={'params': 'param message'})
    def get(self, params):
        return 'Service Message, param: {}'.format(params)
