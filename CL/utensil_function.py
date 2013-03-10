#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import os,json,threading,time,MySQLdb,sys
from utensil import *
from get_weibo import *
import urllib2,warnings


reload(sys)
sys.setdefaultencoding('utf-8')

class restart_thread(threading.Thread):
    def __init__(self,name,max_id,token,lock):
        threading.Thread.__init__(self)
        self.name = name
        self.max_id = max_id
        self.token_container = token
        self.lock = lock
    def run(self):
        conn = connectdb('arber')
        cur = conn.cursor()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if get_weibo(self.name,self.token_container,self.lock,self.max_id):
                cur.execute("UPDATE mession SET status='1' WHERE target_name='%s'"%self.name)
                conn.commit()
        cur.close()
        conn.close()

def restart(token_container,lock):
    conn = connectdb('arber')
    cur = conn.cursor()
    cur.execute("SELECT target_name FROM mession WHERE status='0'")
    result = cur.fetchall()
    for name in result:
        cur.execute("SELECT min(id) FROM context WHERE target_name = '%s'" % name[0])
        max_id = cur.fetchall()
        if max_id[0][0] :
            new_start = restart_thread(name[0],max_id[0][0]-1,token_container,lock)
            new_start.setDaemon(True)
            new_start.start()

class MyThread(threading.Thread):
    def __init__(self,name,token,lock):
        threading.Thread.__init__(self)
        self.name = name
        self.token_container = token
        self.lock = lock
    def run(self):
        conn = connectdb('arber')
        cur = conn.cursor()
        cur.execute("INSERT INTO mession VALUES('%s','%s','0')"%('root',self.name))
        conn.commit()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if get_weibo(self.name,self.token_container,self.lock) :
                cur.execute("UPDATE mession SET status='1' WHERE target_name='%s'"%self.name)
                conn.commit()
        cur.close()
        conn.close()

def show(type):
    conn = connectdb('arber')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mession WHERE user_name = 'root' and status = '%s'"%type)
    result = cur.fetchall()
    for mission in result:
        print mission[1]

def get_context(name,num):
    conn = connectdb('arber')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    sql = "SELECT * FROM context WHERE target_name='%s'" % name
    if not num == -1 :
        sql = "SELECT * FROM context WHERE target_name='%s' ORDER BY hot DESC LIMIT %d" % (name,num) 
    cur.execute(sql)
    context = cur.fetchall()
    file = open(os.path.join(os.path.join(PATH,'result'),name + '.txt'),'w')
    file.close()
    for con in context :
        file = open(os.path.join(os.path.join(PATH,'result'),name + '.txt'),'a')
        text = '\n' + con[2].strftime("%Y-%m-%d %H:%M:%S")+'\n'+con[1]+'\n'
        if con[4] == 1 :
            text += con[5] + '\n'
        if not con[3] == 'no picture':
            text += con[3] 
        text += ("热度 : " + str(con[8]) + '\n')
        file.write(text)
        file.close()
    print name + " document is ready."

def check_screen_name(name,token_container):
    parm = {"access_token":token_container.get_token(),
            "screen_name":name}
    url = "https://api.weibo.com/2/users/show.json?" + urllib.urlencode(parm)
    try :
        result = json.loads(urllib2.urlopen(url).read())
    except urllib2.HTTPError :
        print "token request limit, please wait"
        return False
    return True

def check_finish_name(name):
    conn = connectdb('arber')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    cur.execute("SELECT * FROM mession WHERE target_name='%s' and status='1'"%name)
    result = cur.fetchall()
    if not result:
        return False
    return True
    

