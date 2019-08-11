# -*- coding: utf-8 -*-
## help function들을 모은 집합입니다
import subprocess
import pandas as pd
import sys
from db_connect import conn, engine
# from tensorflow.src.SentimentAnalysisKR import SentimentAnalysisKR
from src import keyword
def exist_test(table):
    cur = conn.cursor()
    query = f"SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' and table_name={table}"
    cur.execute(query)
    result = cur.fetchone()
    if(result == None):
        return 0
    elif(result[0] == 1):
        return 1
    else:
        return 0

def extract_save_reply(youtube_url):
    youtube_key = youtube_url.split("?v=")[-1]
    youtube_key = youtube_key.split("&")[0]
    youtube_key = youtube_key.lower()
    __cmd = f"./run_crawler.sh {youtube_url} {youtube_key}"
    print(__cmd)
    try:
        subprocess.call(__cmd, shell=True)
        subprocess.call(f"mv {youtube_key}.json json/", shell=True)
        return 1
    except Exception as e:
        print(e)
        return 0


def make_table(youtube_url):
    youtube_key = youtube_url.split("?v=")[-1]
    youtube_key = youtube_key.split("&")[0]
    youtube_key = youtube_key.lower()
    reply_df = pd.read_json(f"json/{youtube_key}.json")
    reply_df.to_sql(youtube_key, engine, if_exists='replace')
    # insert data


def get_table_data(table, func_name):
    table = table.lower()
    if(func_name == "sentiment"):
        cur = conn.cursor()
        query = f"SELECT root FROM {table}"
        cur.execute(query)
        result = cur.fetchall()
        result = [row[0] for row in result]
        temp = SentimentAnalysisKR.score(result)
        print(temp)
    elif(func_name == "keyword"):
        cur = conn.cursor()
        query = f"SELECT root FROM {table}"
        cur.execute(query)
        result = cur.fetchall()
        result = [row[0] for row in result]
        temp = get_cnt_words(result)
        print(temp)
        

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("input function argument")
        exit
    if (len(sys.argv) ==3):
        func_name = sys.argv[1]
        youtube_url = sys.argv[2]
        globals()[func_name](youtube_url)
    elif(len(sys.argv)>3):
        func_name = sys.argv[1]
        table_name = sys.argv[2]
        func_name2 = sys.argv[3]
        globals()[func_name](table_name,func_name2)
    # func_name(youtube_url)






