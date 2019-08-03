from sqlalchemy import Column, Integer, String, DateTime, Float
from api.common import *


class Table(Base):
    __tablename__ = 'reply'

    id = Column(Integer, primary_key=True)
    videoId = Column(String)
    comment = Column(String)
    userId = Column(String)
    addedTime = Column(DateTime)
    like = Column(Integer)
    dislike = Column(Integer)
    sentiment = Column(Float)

    def __init__(self, videoId, comment, userId, addedTime, like, dislike, sentiment):
        self.videoId = videoId
        self.comment = comment
        self.userId = userId
        self.addedTime = addedTime
        self.like = like
        self.dislike = dislike
        self.sentiment = sentiment

    # def __repr__(self):
    #     return
