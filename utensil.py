#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import MySQLdb,os,json

PATH = os.path.dirname(__file__)

def get_config():
    with open(os.path.join(PATH,'config.json')) as f:
          evn = json.loads(f.read())
    return evn

evn = get_config()

def connectdb(dbname = ""):
    return MySQLdb.Connection(host=evn["host"], user=evn["user"], passwd=evn["pas"],charset='utf8',db = dbname)
