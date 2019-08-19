import pandas as pd
from flask_restplus import Resource, Namespace
from flask import jsonify, make_response
from app import db

api_reply = Namespace('api_reply', description='감성분성 및 키워드 분석')


@api_reply.route("/<youtube_url>")
class ExtractReply(Resource):
    @api_reply.doc('reply')
    def get(self, youtube_url):
        youtube_key = youtube_url.split("?v=")[-1]
        youtube_key = youtube_key.split("&")[0]
        table = youtube_key.lower()
        sql = f'select * from "{table}"'
        raw_reply_df = pd.read_sql(sql, db.engine)
        test = raw_reply_df.to_dict(orient="records")
        return make_response(jsonify(test))
