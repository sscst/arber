#!/usr/bin/env python  
# -*- coding: utf-8 -*- 

import urllib2,json

class token:
    def __init__(self,token_list):
        self.token_list = token_list
        self.cur_index = 0
        self.lenth = len(token_list)
        
    def return_new_token(self):
        wait = 0
        self.cur_index = ( self.cur_index + 1 ) % self.lenth
        if self.cur_index == 0 :
            url = "https://api.weibo.com/2/account/rate_limit_status.json?access_token="
            c = urllib2.urlopen(url+self.token_list[self.cur_index])
            result = json.loads(c.read())
            if result["remaining_user_hits"] == 0 :
                wait = result["reset_time_in_seconds"]
        new_token = {"wait":wait,"token":self.token_list[self.cur_index]}
        return new_token

    def get_token(self):
        return self.token_list[self.cur_index]




    
