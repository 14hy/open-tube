import pandas as pd
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from flask import jsonify
from ..helper import __extract_save_reply

extract_reply = Namespace("extract")
@extract_reply.route("/<youtube_id>")
class ExtractReply(Resource):
    def get(self, youtube_id):
        __extract_save_reply(youtube_id)
        reply_df = pd.DataFrame()
        raw_reply_df = pd.read_scv(f"./csv/{youtube_id}.csv")
        reply_df['id'] = youtube_id
        reply_df['reply_text'] = raw_reply_df['reply_text'].dropna()
        print(reply_df)
        return 200

        
