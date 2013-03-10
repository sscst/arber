#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
from utensil import *
from utensil_function import *
from token import token
from token_list import token_list
import threading 


token_container = token(token_list) 
lock = threading.Lock() 
restart(token_container,lock)
print '''        欢迎来到微博备份工具！ 
        'a'后跟微博昵称，可进行微博备份
	'working'可查询正在工作的昵称
	'finish'可查询已经完成的昵称
	'down'后跟微博昵称，可将数据从数据库中导成txt文件，文件将会存放在result文件夹,后面可以跟 'top' + 数字，表示导出热度最大的N条微博
     '''
while True :
    o = raw_input("your choice : ")
    if o[0] == 'a':
        name = [x for x in o.split(' ') if x]
        if check_screen_name(name[1],token_container):
            thread = MyThread(name[1],token_container,lock)
            thread.setDaemon(True)
            thread.start()
        else :
            print "好像没有这个昵称哦，看看你有没有弄错？"
    elif o == 'working':
        show('0')
    elif o == 'finish':
        show('1')
    elif o[0:4] == 'down':
        num = -1
        order = [x for x in o.split(' ') if x]
        if len(order) == 4 and order[2] == 'top' and order[3].isdigit() :
            num = int(order[3])
        elif not len(order) == 2 :
            print "错误操作"
            continue
        if check_finish_name(order[1]):
            get_context(order[1],num)
        else :
            print "这个昵称不在完成序列中哦，你可以去a他们，或者看看昵称是不是弄错了"
        
