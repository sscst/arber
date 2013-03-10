#!/usr/bin/env python  
# -*- coding: utf-8 -*- 

from weiboBee import connect_db
from sina_token import sina_token
from sina_weibo import weibo_take
import time,warnings,threading

def run(name):
    conn,cur = connect_db()
    sina = weibo_take(sina_token,name,conn,cur)
    cur.execute("SELECT COUNT(*) FROM mession WHERE target_name = '%s' and status = '1'" % name)
    count = cur.fetchall()
    if count[0][0] == 0L :
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sina.get_weibo()
    cur.execute("UPDATE mession SET status='1' WHERE target_name='%s'"%name)
    conn.commit()
    cur.close()
    conn.close()

def ADaemon():
    threads = []
    while True :
        conn,cur = connect_db()
        cur.execute("SELECT target_name FROM mession WHERE status = '0'")
        names = cur.fetchall()
        cur.execute("UPDATE mession SET status='2' WHERE status = '0'")
        conn.commit()
        cur.close()
        conn.close()
        for name in names:
            threads.append(threading.Thread(target=run, args=(name[0],)))
            threads[-1].start()
        time.sleep(30)

ADaemon()

