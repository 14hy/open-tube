from app import db
from datetime import datetime


class History(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String)
    url = db.Column(db.String)
    keyword = db.Column(db.Boolean)
    sentiment = db.Column(db.Boolean)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Integer, default=0)
