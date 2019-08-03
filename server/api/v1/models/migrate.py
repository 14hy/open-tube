from api.v1.models.reply import *


def drop_all():
    Base.metadata.drop_all(engine)


def create_all():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    drop_all()
    create_all()
