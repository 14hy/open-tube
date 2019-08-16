from flask_restplus import Namespace, fields


class ExtractReply:
    api = Namespace('Extract', description='extract and save reply')
    user = api.model('data', {
        'id': fields.String(required=True, description='reply'),
        'text': fields.String(required=True, description='reply')
    })