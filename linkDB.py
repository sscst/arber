#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import MySQLdb,os,json,warnings
from utensil import *

with open(os.path.join(PATH,'db.sql')) as db:
        text = db.read()
        conn = connectdb()
        cur = conn.cursor()
        command_lines = text.split(';')
        command_lines.pop()
	with warnings.catch_warnings():
            warnings.simplefilter("ignore")
	    for line in command_lines :
		    cur.execute(line + ';')
        conn.commit()
        cur.close()
        conn.close()
