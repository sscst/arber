#!/usr/bin/env python  
# -*- coding: utf-8 -*- 

import sys,time,urllib,urllib2,json
from utensil import process_weibo

reload(sys)
sys.setdefaultencoding('utf-8')

class weibo_take:
    def __init__(self,_list,name,conn,cur):
        self.token = _list
        self.name = name
        self.index = 0
        self.conn = conn
        self.cur = cur

    def return_new_token(self):
        wait = 0
        self.index = ( self.index + 1 ) % len(self.token)
        token = self.token[self.index]
        if self.index == 0 :
            url = "https://api.weibo.com/2/account/rate_limit_status.json?access_token="
            result = json.loads(urllib2.urlopen(url+token).read())
            if result["remaining_user_hits"] == 0 :
                wait = result["reset_time_in_seconds"]
        new_token = {"wait":wait,"token":token}
        return new_token

    def req(self,page):
        while True:
            parm = {"access_token":self.token[self.index],
                    "count":"100",
                    "page":page,
                    "screen_name":self.name,
                    }
            url = "https://api.weibo.com/2/statuses/user_timeline.json"
            try :
                result = urllib2.urlopen(url+"?"+urllib.urlencode(parm))
            except urllib2.HTTPError :
                new_token = self.return_new_token()
                if not new_token["wait"] == 0 :
                    time.sleep(new_token["wait"] + 10)
                continue
            break
        return json.loads(result.read())

    def get_weibo(self):
        page = 1
        self.cur.execute('SET NAMES utf8')
        while True :
            weibo_data = self.req(page)
            if not weibo_data["statuses"]:
                break
            info = process_weibo(weibo_data,self.name)
            page += 1
            self.cur.executemany("INSERT INTO context VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",info)
        self.conn.commit()
