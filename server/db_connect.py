import psycopg2
from sqlalchemy import create_engine
import os

POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

engine = create_engine(f'postgres://postgres:{POSTGRES_PASSWORD}@210.89.189.25:5432', encoding='utf-8')
conn = psycopg2.connect(host='210.89.189.25', port=5432, user='postgres', database='postgres',
                        password=POSTGRES_PASSWORD)
