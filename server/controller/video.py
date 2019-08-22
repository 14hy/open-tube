from models.history import History
from flask_restplus import Resource, Model, fields, reqparse, inputs, Namespace
from src.thumbnail import *
from src.reply_gif import *
from multiprocessing import Process

api_video = Namespace('video', description='댓글 태그 gif와 썸네일을 요청합니다.')


@api_video.route('/reply_gif')
class Route(Resource):

    @api_video.doc(params={'vid': 'vid', 'uid': 'uid'})
    def get(self):
        """상태 확인 및 결과 받기"""

        parser = reqparse.RequestParser()
        parser.add_argument('vid', help='동영상 URL')
        parser.add_argument('uid', help='User ID')
        args = parser.parse_args(strict=True)
        vid = args['vid']
        uid = args['uid']

        v: Video = Video.query.filter_by(vid=vid, uid=uid).first()
        if v is None:

            return {
                'status': 'failed',
                'msg': f'requested {vid} with {uid} does not exists.'
            }

        elif v.status == 'complete':
            return {
                'status': 'complete',
                'reply_gif': v.reply_gif
            }

        else:
            return {'status': 'processing'}

    @api_video.doc(params={'vid': 'vid', 'uid': 'uid'})
    def post(self):
        """댓글의 태그에 해당하는 gif 작업 추가
        :return: {'status': 'wait', 'processing', 'complete'}
        {
            'time(sec)': {
                'reply': [ ],
                'gif_path': str
            }
            ..
        }
        """
        parser = reqparse.RequestParser()
        parser.add_argument('vid', help='동영상 URL')
        parser.add_argument('uid', help='User ID')
        args = parser.parse_args(strict=True)

        base_url = 'https://www.youtube.com/watch?v='
        vid = args['vid']
        uid = args['uid']

        h: History = History.query.filter_by(url=f'{base_url}{vid}', userId=uid).first()
        if h is None:
            return {
                'status': 'reply data in history is not ready'
            }

        else:
            d: Download = Download.query.filter_by(vid=vid, uid=uid).first()
            if d is None:
                print("downloading start")
                download_url(vid, uid)
                return {'status': 'wait'}

            elif d.status == 'failed':
                print("failed")
                return {'status': d.status}

            elif d.status == 'downloading':
                print("downloading")
                return {'status': 'wait'}

            else:
                v: Video = Video.query.filter_by(vid=vid, uid=uid).first()
                if v is None:
                    v = Video(vid=vid, uid=uid, status='wait')
                    db.session.add(v)
                    db.session.commit()

                    file_path = d.file_path
                    tags_dict = extract_tag_from_table(vid)
                    Process(target=tag_to_gif, kwargs={
                        'file_path': file_path,
                        'tags_dict': tags_dict,
                        'gif_path': f'/mnt/master/gifs',
                        'vid': vid,
                        'uid': uid
                    }).start()
                    return {
                        'status': 'processing'
                    }

                elif v.status == 'complete':
                    return {
                        'status': 'complete',
                        'reply_gif': v.reply_gif
                    }

                else:
                    return {'status': 'processing'}


@api_video.route('/thumbnail')
class Route(Resource):

    @api_video.doc(params={'vid': 'vid', 'uid': 'uid', 'height': '세로', 'width': '가로'})
    def get(self):
        """상태 확인 및 결과 받기"""

        parser = reqparse.RequestParser()
        parser.add_argument('vid', help='동영상 URL')
        parser.add_argument('uid', help='User ID')
        parser.add_argument('height', type=int, help='height')
        parser.add_argument('width', type=int, help='width')
        args = parser.parse_args(strict=True)
        vid = args['vid']
        uid = args['uid']
        height = args['height']
        width = args['width']

        v: Video = Video.query.filter_by(vid=vid, uid=uid).first()
        if v is None:
            return {
                'status': 'failed',
                'msg': f'requested {vid} with {uid} does not exists.'
            }

        try:
            path = v.thumbnails_path[f'{height}{width}']
            return {
                'status': 'complete',
                'thumbnail_path': path
            }

        except:
            return {
                'status': 'processing'
            }

    @api_video.doc(params={'vid': 'vid', 'uid': 'uid', 'height': '세로', 'width': '가로'})
    def post(self):
        """영상의 썸네일 작업을 추가"""
        parser = reqparse.RequestParser()
        parser.add_argument('vid', help='동영상 URL')
        parser.add_argument('uid', help='User ID')
        parser.add_argument('height', type=int, help='height')
        parser.add_argument('width', type=int, help='width')

        args = parser.parse_args(strict=True)
        vid = args['vid']
        uid = args['uid']
        height = args['height']
        width = args['width']

        v: Video = Video.query.filter_by(vid=vid, uid=uid).first()
        if v is None:
            v = Video(vid=vid, uid=uid, status='wait', thumbnails_path={})
            db.session.add(v)
            db.session.commit()
        elif v.thumbnails_path is None:
            v.status = 'processing'
            db.session.commit()
            Process(target=make_thumbnail, kwargs={"vid": vid, "uid": uid,
                                                   "save_path": f"/mnt/master/thumbnails",
                                                   "grid": (height, width)}).start()
            return {
                'status': v.status
            }

        try:
            path = v.thumbnails_path[f'{height}{width}']
            return {
                'status': 'complete',
                'thumbnail_path': path
            }

        except:
            return {
                'status': 'something is wrong. error'
            }
