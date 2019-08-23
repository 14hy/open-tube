from app import db


class Video(db.Model):
    __tablename__ = 'video'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    vid = db.Column(db.String, nullable=False)
    uid = db.Column(db.String, unique=False, nullable=False)
    status = db.Column(db.Enum('wait', 'processing', 'complete', name='video_type'),
                       nullable=False, default=False)
    reply_gif = db.Column(db.JSON(none_as_null=True), nullable=True, unique=False)
    thumbnails_path = db.Column(db.JSON(none_as_null=True), unique=False, nullable=True)
    

if __name__ == "__main__":
    db.create_all()
    # db.drop_all()
