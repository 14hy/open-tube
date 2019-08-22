#-*- coding:utf-8 -*-
from multiprocessing import Pool # Pool import하기
import datetime
from db_connect import conn, engine
from helper import get_table_data,extract_save_reply,make_table
class test:
    
    def sentiment(self,youtube_url):
        cur = conn.cursor()
        extract_save_reply(youtube_url)
        make_table(youtube_url)
        sql=f"update history set done=1 where url='{youtube_url}'"
        cur.execute(sql)
        conn.commit()

    def serving_sentiment(self,youtube_url):
        get_table_data(youtube_url,'sentiment')

    def slang(self,youtube_url):
        cur = conn.cursor()
        extract_save_reply(youtube_url)
        make_table(youtube_url)
        sql=f"update history set done=1 where url='{youtube_url}'"
        cur.execute(sql)
        conn.commit()

    def serving_slang(self,youtube_url):
        get_table_data(youtube_url,'slang')

    def execute(self,num):
        cur = conn.cursor()
        sql = 'select url from history where done=0 and sentiment=true'
        cur.execute(sql)
        data = cur.fetchall()
        sen_data = [i[0] for i in data]
        sql2 = 'select url from history where done=0 and slang=true'
        cur.execute(sql2)
        data2 = cur.fetchall()
        slang_data = [i[0] for i in data2]
#        pool = Pool(processes=num) # 4개의 프로세스를 사용합니다.
#        pool.map(self.sentiment,sen_data)# get_contetn 함수를 넣어줍시다.
#        pool.map(self.slang,slang_data)# get_contetn 함수를 넣어줍시다.
#        print('start')
#        exit()
        for url in sen_data:
            self.sentiment(url)
            self.serving_sentiment(url)
        for url in slang_data:
            self.slang(url)
            self.serving_slang(url)


if __name__ =="__main__":
    e= test()
    result = e.execute(8)
