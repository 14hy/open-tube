from app import db


class Download(db.Model):
    __tablename__ = 'download'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    vid = db.Column(db.String, nullable=False, unique=True)
    status = db.Column(db.Enum('failed', 'downloading', 'downloaded', 'processing', 'completed', name='download_type'),
                       nullable=False, default=False)
    file_path = db.Column(db.String, nullable=True)
    uid = db.Column(db.String, unique=False, nullable=False)
    time_line = db.Column(db.JSON(none_as_null=True), nullable=True, default=None)


if __name__ == "__main__":
    db.create_all()
    # db.drop_all()
