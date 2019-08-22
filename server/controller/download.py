from app import db
from models.download import Download
from flask_restplus import Resource, Model, fields, reqparse, inputs, Namespace
from src.download import download_url
from flask import jsonify

api_download = Namespace('download', description='동영상 다운로드 작업을 추가합니다.')


@api_download.route('/')
class Route(Resource):

    @api_download.doc(params={'vid': 'vid', 'uid': 'uid'})
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('vid', help='동영상 URL')
        parser.add_argument('uid', help='User ID')

        args = parser.parse_args(strict=True)

        return jsonify(download_url(vid=args['vid'], uid=args['uid']))
