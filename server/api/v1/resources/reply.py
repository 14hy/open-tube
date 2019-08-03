from api.common import engine
from sqlalchemy.orm import sessionmaker
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from flask import jsonify
from api.v1.models.reply import Table
from api.utils import *

Session = sessionmaker(bind=engine)
sess = Session()
name = 'reply'

api = Namespace('v1/{}'.format(name), description='{} endpoint'.format(name))

model = api.model(name, {
    'id': fields.Integer(),
    'videoId': fields.String(),
    'comment': fields.String(),
    'userId': fields.String(),
    'addedTime': fields.DateTime(),
    'like': fields.Integer(min=0),
    'dislike': fields.Integer(min=0),
    'sentiment': fields.Float(min=0),
})


@api.marshal_with(model)
@api.route('/')
class Route(Resource):

    @api.doc('get {}'.format(name))
    def get(self):
        query = sess.query(Table).all()

        return jsonify(pop__sa_instance_state(query))

    @api.marshal_with(model, as_list=True)
    @api.doc('post {}'.format(name), params={'videoId': 'videoId', 'comment': 'comment',
                                             'userId': 'userId', 'addedTime': 'addedTime',
                                             'like': 'like', 'dislike': 'dislike', 'sentiment': 'sentiment'})
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('videoId', required=True, type=str)
        parser.add_argument('comment', required=True, type=str)
        parser.add_argument('userId', required=True, type=str)
        parser.add_argument('addedTime', required=True, type=inputs.date_from_iso8601)
        parser.add_argument('like', required=True, type=int)
        parser.add_argument('dislike', required=True, type=int)
        parser.add_argument('sentiment', required=True, type=float)

        args = parser.parse_args(strict=True)

        reply = Table(args['videoId'], args['comment'], args['userId'], args['addedTime'],
                      args['like'], args['dislike'], args['sentiment'])

        sess.add(reply)
        sess.commit()

        return args.__dict__, 201

    @api.doc('patch {}'.format(name))
    def patch(self):
        return ''


@api.marshal_with(model)
@api.route('/<int:id>')
class Route(Resource):

    @api.doc('get id {}'.format(name))
    def get(self, id):
        query = sess.query(Table).filter(Table.id == id).all()
        return jsonify(pop__sa_instance_state(query)), 201

    @api.doc('delete {}'.format(name))
    def delete(self, id):
        query = sess.query(Table).filter(Table.id == id).delete()
        return query, 201
