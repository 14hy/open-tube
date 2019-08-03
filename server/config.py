import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class FLASK(object):
    version = '190729'
    title = 'OPEN-TUBE server'
    description = '강태욱/이민혁/전가빈/전현민'
    host = '0.0.0.0'
    port = '5000'
    debug = True


class DATABASE(object):
    # DB://user:password@host:port/dbName
    uri = 'postgres://admin:admin@localhost:32352/postgresdb'
