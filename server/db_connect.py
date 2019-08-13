import psycopg2
from sqlalchemy import create_engine
import os

POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

engine = create_engine(f'postgresql://opentube:{POSTGRES_PASSWORD}@101.101.164.71:32352/opentube', encoding='utf-8')
conn = psycopg2.connect(host='101.101.167.71', port=32352, user='opentube', database='opentube')
