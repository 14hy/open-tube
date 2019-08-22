from app import db
from models.video import Video
from models.history import History
from flask_restplus import Resource, Model, fields, reqparse, inputs, Namespace
from flask import jsonify
from src.thumbnail import *
from src.reply_gif import *
from multiprocessing import Process

api_video = Namespace('video', description='댓글 태그 gif 및 썸네일을 위한 API')


@api_video.route('/reply_gif')
class Route(Resource):

    @api_video.doc(params={'vid': 'vid', 'uid': 'uid'})
    def post(self):
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
    def post(self):
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
            v = Video(vid=vid, uid=uid, status='wait')
            db.session.add(v)
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
                'status': v.status
            }

        return {'status': 'error'}
