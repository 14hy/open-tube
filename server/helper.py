# -*- coding: utf-8 -*-
## help function들을 모은 집합입니다
import subprocess
import pandas as pd
import sys
from db_connect import conn


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
    __cmd = f"./run_cralwer.sh {youtube_url} {youtube_key}"
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
    reply_df = pd.read_json(f"json/{youtube_key}.json")
    reply_df.to_sql(youtube_key, con, if_exists='replace')
    # insert data


# def get_table_data(table, func):
#     #데이터 가져오기
#     #func 실행시키기
    

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("input function argument")
        exit
    func_name = sys.argv[1]
    youtube_url = sys.argv[2]
    globals()[func_name](youtube_url)
    # func_name(youtube_url)





