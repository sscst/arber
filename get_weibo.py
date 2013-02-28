#!/usr/bin/env python  
# -*- coding: utf-8 -*- 

import urllib2,urllib,json
from utensil import *

def get_standard_time(time_str):
    month_code = {"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}
    month = time_str[4:7]
    day = time_str[8:10]
    time = time_str[11:19]
    year = time_str[26:]
    return year + '-' + month_code[month] + '-' + day + " " + time

def request(name,index,max_id):
    parm = {"access_token":evn["token"],
            "count":"100",
            "page":index,
            "screen_name":name,
            "max_id":max_id}
    url = "https://api.weibo.com/2/statuses/user_timeline.json"
    result = urllib2.urlopen(url+"?"+urllib.urlencode(parm))
    return json.loads(result.read())

def get_weibo(name,max_id=0):
    index = 1
    conn = connectdb('arber')
    cur = conn.cursor()
    cur.execute('SET NAMES utf8')
    while True :
        try :
            weibo_data = request(name,index,max_id)
        except urllib2.HTTPError :
            print "token request limit,please change it"
            cur.close()
            conn.close()
            return False
        if not weibo_data["statuses"]:
            break
        info = ()
        for weibo in weibo_data["statuses"] :
            pic = "no picture"
            hot = weibo["reposts_count"] + weibo["comments_count"] + weibo["attitudes_count"]
            if weibo.has_key("retweeted_status"):
                retweeted_text = "貌似原微博已经被删除了"
                if not weibo["retweeted_status"].has_key("deleted"):
                    retweeted_text = weibo["retweeted_status"]["user"]["screen_name"] + " : " + weibo["retweeted_status"]["text"]
                if weibo["retweeted_status"].has_key("thumbnail_pic"):
                    pic = "小图 : " + weibo["retweeted_status"]["thumbnail_pic"] + '\n'
                    pic += "大图 ：" + weibo["retweeted_status"]["bmiddle_pic"] + '\n'
                sina_info = ((weibo["id"],weibo["text"],get_standard_time(weibo["created_at"]),pic,1,retweeted_text,name,'root',hot),)
            else :
                if weibo.has_key("thumbnail_pic"):
                    pic = "小图 : " + weibo["thumbnail_pic"] + '\n'
                    pic += "大图 ：" + weibo["bmiddle_pic"] + '\n'
                sina_info = ((weibo["id"],weibo["text"],get_standard_time(weibo["created_at"]),pic,0,"no retweeted",name,'root',hot),)
            info += sina_info
        index += 1
        cur.executemany("INSERT INTO context VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",info)
        conn.commit()
    cur.close()
    conn.close()
    return True
