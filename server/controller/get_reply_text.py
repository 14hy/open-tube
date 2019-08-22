import pandas as pd
from flask_restplus import Resource, Namespace
from flask import jsonify
from app import db

api_reply = Namespace('api_reply', description='분석된 댓글 테이블 긁어오기')


@api_reply.route("/<vid>")
class ExtractReply(Resource):
    
    @api_reply.doc('reply')
    def get(self, vid):
        table = vid.lower()
        sql = f'select * from "{table}"'
        raw_reply_df = pd.read_sql(sql, db.engine)
        test = raw_reply_df.to_dict(orient="records")
        return jsonify(test)
