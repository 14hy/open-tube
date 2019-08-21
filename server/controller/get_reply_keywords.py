import pandas as pd
from flask_restplus import Resource, Namespace
from flask import jsonify
from app import db
from src.keyword import get_cnt_words

api_keywords = Namespace('api_keywords', description='키워드 분석')


@api_keywords.route("/<vid>")
class ExtractReply(Resource):
    @api_keywords.doc('api_keywords')
    def get(self, vid):
        table = vid.lower()
        sql = f'select * from "{table}"'
        conn = db.session.connection()
        result = conn.execute(f'select * from {vid.lower()}')
        conn.close()
        keywords = get_cnt_words(result)
        return keywords
