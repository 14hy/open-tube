import pandas as pd
from flask_restplus import Resource, Namespace, fields, reqparse, inputs
from flask import jsonify
from ..app import app, db, extract_reply
from ..helper import __extract_save_reply

@extract_reply.route("/<youtube_id>")
class ExtractReply(Resource):
    def get(self,youtube_id):
        cmd= "youtube"
        
