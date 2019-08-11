import pandas as pd
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from flask import jsonify, make_response
import json
import sys
sys.path.append("..")
from models.response import ExtractReply
from helper import extract_save_reply
extract_reply = ExtractReply.api
@extract_reply.marshal_with(ExtractReply.user)
@extract_reply.route("/<youtube_id>")
class ExtractReply(Resource):
    def get(self, youtube_id):
        flag = extract_save_reply(youtube_id)
        if(flag):
            reply_df = pd.DataFrame()
            raw_reply_df = pd.read_csv(f"./csv/{youtube_id}.csv")
            reply_df['reply_text'] = raw_reply_df['text'].dropna()
            reply_df['id'] = youtube_id
            print(reply_df)
            test = reply_df.to_dict(orient="records")
            return make_response(jsonify(test))
        else:
            return 0
        

        
