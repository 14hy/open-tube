from models.history import History, db
from flask_restplus import Resource, reqparse, Namespace

api_history = Namespace('history', description='댓글 레포트 요청 API - (감성분석, 키워드, 욕설) 합니다.')


@api_history.route("/")
class Route(Resource):

    @api_history.doc(params={'userId': 'userId', 'url': 'url'})
    def get(self):
        """댓글 레포트 요청 확인 API

        :return: {'status': 0, 1, 2 or 'error'}
        0: 작업에 추가 되었고 스케쥴링 되었음
        1: 크롤링 및 분석 중
        2: 완료
        """
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=str)
        parser.add_argument('url', required=True, type=str)
        args = parser.parse_args(strict=True)

        url = args['url']
        userId = args['userId']

        history: History = History.query.filter_by(url=args['url'], userId=args['userId']).first()
        if history is None:
            return {
                'status': 'error',
                'msg': f'requested {url} with {userId} does not exists.'
            }

        return {
            'status': history.done
        }

    @api_history.doc('history', params={'userId': 'userId', 'keyword': 'keyword',
                                        'sentiment': 'sentiment', 'url': 'url', 'slang': 'slang'})
    def post(self):
        """새로운 댓글 분석 요청

        :return: {'status': 'success', 'unknown error'}
        """
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=str)
        parser.add_argument('keyword', required=True, type=bool)
        parser.add_argument('sentiment', required=True, type=bool)
        parser.add_argument('url', required=True, type=str)
        parser.add_argument('slang', required=True, type=bool)

        args = parser.parse_args(strict=True)

        try:
            history = History(userId=args['userId'], keyword=args['keyword'], sentiment=args['sentiment'],
                              url=args['url'], slang=args['slang'])
            db.session.add(history)
            db.session.commit()
            return {
                'status': 'success'
            }
        except:
            return {
                'status': 'unknown error'
            }
