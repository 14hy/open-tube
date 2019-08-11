import psycopg2
import configparser
from sqlalchemy import create_engine
def config(filename='db2.cfg', section='postgresql'):
    # create a parser
    parser = configparser.ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
configs = configparser.ConfigParser()
configs.read("db2.cfg")
engine = create_engine(configs.get('flask', 'SQLALCHEMY_DATABASE_URI'), encoding='utf-8')
params = config()
conn = psycopg2.connect(**params)