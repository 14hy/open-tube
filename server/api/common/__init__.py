from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import config

DATABASE_CONFIG = config.DATABASE
FLASK_CONFIG = config.FLASK

engine = create_engine(DATABASE_CONFIG.uri, echo=True)
Base = declarative_base()
