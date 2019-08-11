from models.history import History2, db
from flask_restplus import Resource, Model, fields, reqparse, inputs, Namespace

api_history = Namespace('history')


@api_history.route("/")
class Route(Resource):

    @api_history.doc('history', params={'userId': 'userId', 'keyword': 'keyword',
                                        'sentiment': 'sentiment', 'url': 'url'})
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=str)
        parser.add_argument('keyword', required=True, type=bool)
        parser.add_argument('sentiment', required=True, type=bool)
        parser.add_argument('url', required=True, type=str)

        args = parser.parse_args(strict=True)

        history = History2(userId=args['userId'], keyword=args['keyword'], sentiment=args['sentiment'],
                           url=args['url'])
        db.session.add(history)
        db.session.commit()
        return 201

