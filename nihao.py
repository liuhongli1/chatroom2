#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# outhor:刘洪礼 time:2018/7/31
from time import sleep
def show_love(love_name,name,ck):
    words = love_name
    print(words,'做我女朋友好么？')
    letters_cmd=''
    for item in words.split():
        
        for y in range(12,-12,-1):
            lisst_X = []
            letters = ''
            for x in range(-30,30):
                expression = ((x*0.05)**2+(y*0.1)**2-1)\
                **3-(x*0.05)**2*(y*0.1)**3
                if expression <= 0:
                    letters +=item[(x-y)%len(item)]
                else:
                    letters +='*'
            letters_cmd += letters+'\n'
    textmsg = letters_cmd
    if words:
        cmd='##'+' '+words+" "+name+' '+textmsg
    else:
        cmd ='##'+' '+'anyone'+' '+name+' '+textmsg
    ck.send(cmd.encode('utf-8'))
    print(textmsg)
    # print('\n'.join(letterlist))
    # sleep(0.5)