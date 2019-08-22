from app import db
from models.download import Download
from flask_restplus import Resource, Model, fields, reqparse, inputs, Namespace
from src.download import download_url
from flask import jsonify
from src.download import _download

api_download = Namespace('download', description='영상 얼굴 인식 작업을 요청합니다.')


@api_download.route('/')
class Route(Resource):

    @api_download.doc(params={'vid': 'vid', 'uid': 'uid'})
    def get(self):
        """얼굴 영상 인식의 작업 상황을 확인
        :return: {'status': 'wait', 'processing', 'complete'}
        """
        parser = reqparse.RequestParser()
        parser.add_argument('vid', help='동영상 URL')
        parser.add_argument('uid', help='User ID')
        args = parser.parse_args(strict=True)
        vid = args['vid']
        uid = args['uid']

        try:
            q = Download.query.filter_by(vid=vid, uid=uid).first()
        except:
            db.session.remove()
            db.session.rollback()
            q = Download.query.filter_by(vid=vid, uid=uid).first()

        if q is not None:
            if q.status == 'processing':
                return {
                    'status': q.status
                }
            if q.status == 'downloading':
                return {
                    'status': 'wait'
                }
            if q.status == 'downloaded':
                _download(vid)
                return {
                    'status': 'processing'
                }
            if q.status == 'completed':
                return {
                    'status': 'complete',
                    'time_line': q.time_line
                }
        else:
            return {
                'status': 'error',
                'msg': f'requested {vid} with {uid} does not exists.'
            }

    @api_download.doc(params={'vid': 'vid', 'uid': 'uid'})
    def post(self):
        """새로운 얼굴 영상 인식 작업 추가
        """
        parser = reqparse.RequestParser()
        parser.add_argument('vid', help='동영상 URL')
        parser.add_argument('uid', help='User ID')
        args = parser.parse_args(strict=True)
        vid = args['vid']
        uid = args['uid']

        return jsonify(download_url(vid=vid, uid=uid))
