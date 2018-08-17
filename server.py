#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# outhor:刘洪礼 time:2018/7/31
import tkinter
import socket, threading
from pymysql2 import *
from time import ctime
from baiduSearch import BaikeSearch


win = tkinter.Tk()  # 创建主窗口
win.title('模拟服务器')
win.geometry("400x400+200+20")
users = {}#用户字典临时存储正处于聊天室的用户
game_dict={}
Baik=None
def MyLogin(cList,ck):
    global users
    name = cList[1]
    password = cList[2]
    Order = login_fun(name,password)
    if Order ==0:
        users[name] = ck#解码并储存用户的信息
    #print(users)
        printStr = "" + name + "连接\n"#在连接显示框中显示是否连接成功
        text.insert(tkinter.INSERT, printStr)
        cmd1 = 'OK'
        tuble1= seek_anyone()
        num=len(tuble1)
        Str = ''
        for tp in tuble1:
            Str += ' '+tp[0]
        for tp in users:
            Str+=' '+tp
        print(users)
        for Ck in users:
            if Ck ==name:
                cmd = cmd1+Str+' '+str(num)
            else:
                cmd = cmd1+' '+name
            users[Ck].send(cmd.encode('utf-8'))
    else:
        ck.send(b'fial')
def MyRegister(cList,ck):
    name = cList[1]
    password = cList[2]
    Order = enter_fun(name,password)
    if Order == 'OK':
        ck.send(b'OK')
    else :
        ck.send('用户已经存在'.encode('utf-8'))
def MyMoreResv(cList,ck):
    global users
    rescName = cList[1]
    name = cList[2]
    sendInfo = cList[3]
    cmd = 'C'+' '+ctime().split(' ')[3]+name+'发来:'+sendInfo
    cmd1 = 'C'+' '+ctime().split(' ')[3]+'发给'+rescName+':'+sendInfo
    if rescName=='anyone':
        for user in users:
            if user ==name:
                print(user)
                users[user].send(cmd1.encode('utf-8'))
            else:
                users[user].send(cmd.encode('utf-8'))
    else:
        if rescName in game_dict:
            cmd='C'+' '+ctime().split(' ')[3]+':您要搜索的人在游戏中，请稍后'
            users[name].send(cmd.encode('utf-8'))
        elif rescName in users:
            users[rescName].send(cmd.encode('utf-8'))
            users[name].send(cmd1.encode('utf-8'))
        else:
            cmd='C'+' '+ctime().split(' ')[3]+':您搜索的人不在线'
            users[name].send(cmd.encode('utf-8'))
    save_info_fun(name,rescName,sendInfo)
def MyQuery(cList,ck):
    name = cList[1]
    rescName = cList[2]
    data = int(cList[3])
    cmd=''
    if name =='#':
        tuble =seek_fun(data)
        for tub in tuble:
            cmd += tub[1]+"在"+str(tub[4]).replace(' ','>')+'发给'+tub[2]+':'+tub[3]+'\n'
    elif name !='#' and rescName =='#':
        tuble =seek_name_fun(name,data)
        for tub in tuble:
            print(tub[1],type(tub[4]))
            cmd += tub[1]+"在"+str(tub[4]).replace(' ','>')+'发给'+tub[2]+':'+tub[3]+'\n'
    else:
        tuble = seek_rece_name_fun(name,rescName,data)
        for tub in tuble:
            cmd += tub[1]+"在"+str(tub[4]).replace(' ','>')+'发给'+tub[2]+':'+tub[3]+'\n'
    cmd1='R'+' '+cmd
    ck.send(cmd1.encode('utf-8'))
def Auoresponse(cList,ck):
    global users
    content = Baik.Search(cList[-1])
    cmd='S'+' '+content
    ck.send(cmd.encode('utf-8'))
def MyShowLove(cList,ck):
    global users
    rescName = cList[1]
    name = cList[2]
    sendInfo = cList[3]
    cmd = '##'+' '+ctime().split(' ')[3]+name+'发来:\n'+sendInfo
    cmd1 = '##'+' '+ctime().split(' ')[3]+'发给'+rescName+':\n'+sendInfo
    if rescName=='anyone':
        for user in users:
            if user ==name:
                users[user].send(cmd1.encode('utf-8'))
            else:
                users[user].send(cmd.encode('utf-8'))
    else:
        if rescName in game_dict:
            cmd='C'+' '+ctime().split(' ')[3]+':您要搜索的人在游戏中，请稍后'
            users[name].send(cmd.encode('utf-8'))
        elif rescName in users:
            print('示爱目标在线')
            users[rescName].send(cmd.encode('utf-8'))
            users[name].send(cmd1.encode('utf-8'))
        else:
            cmd='C'+' '+ctime().split(' ')[3]+':您搜索的人不在线'
            users[name].send(cmd.encode('utf-8'))
def MyGame(cList,ck):
    global users
    global game_dict
    quit_num=1
    if cList[0]=='GR':
        cmd = 'GR'+' '+cList[1]
        users[cList[2]].send(cmd.encode())
    elif cList[0]=="GA":
        cmd = "GA"+' '+cList[1]
        users[cList[2]].send(cmd.encode())
    elif cList[0]=='GI':
        cmd = 'GI'+' '+cList[1]
        users[cList[2]].send(cmd.encode())
    elif cList[0]=='GE':
        cmd = 'GE'+' '+cList[1]
        users[cList[2]].send(cmd.encode())
    elif cList[0]=='GE1':
        cmd = 'GE1'+' '+cList[1]
        users[cList[2]].send(cmd.encode())    
    elif cList[0]=="GOK":
        cmd = 'GOK'+' '+cList[1]
        users[cList[2]].send(cmd.encode())
        game_dict[cList[1]]=users[cList[1]]
        game_dict[cList[2]]=users[cList[2]]
        del users[cList[1]]
        del users[cList[2]]
    elif cList[0]=="G@":
        cmd = "G@"+" "+cList[2]+" "+cList[3]
        game_dict[cList[1]].send(cmd.encode("utf-8"))
    elif cList[0]=='G#':
        cmd = cList[1]
        game_dict[cList[2]].send(cmd.encode())
    elif cList[0]=='GQ':
        for a in users:
            print(a)
        cmd = 'GQ'+' '+cList[1]
        print(cList,"下面开始发送退出游戏")
        users[cList[2]].send(cmd.encode('utf-8'))
        print("发送退出游戏成功")
    elif cList[0]=='G$':
        cmd = "G$"+' '+cList[2]+' '+cList[3]
        game_dict[cList[1]].send(cmd.encode())
    elif cList[0]=="G@A":
        cmd = "G@A"
        game_dict[cList[1]].send(cmd.encode("utf-8"))
    elif cList[0]=="G@AR":
        if cList[2]=="OK":
            cmd = "G@AR"+" "+"OK"
            # cmd1 = "G@@"
            game_dict[cList[1]].send(cmd.encode('utf-8'))
            # game_dict[cList[3]].send(cmd1.encode("utf-8"))
        else:
            cmd = "G@AR"+" "+"NO"
            game_dict[cList[1]].send(cmd.encode('utf-8'))
    elif cList[0]=="G@AR1":
        game_dict[cList[3]].send("G@@".encode("utf-8"))
    elif cList[0]=="G@Q":
        if quit_num ==1:
            cmd="G@Q"+' '+"first"
            game_dict[cList[1]].send(cmd.encode("utf-8"))
        else:
            cmd="G@Q"+" "+"second"
            game_dict[cList[1]].send(cmd.encode("utf-8"))
    elif cList[0]=="G@QR":
        if cList[2]=="OK":
            cmd = "G@QR"+" "+"OK"
            cmd1 = "G@@"
            game_dict[cList[1]].send(cmd.encode('utf-8'))
            # game_dict[cList[3]].send(cmd1.encode("utf-8"))
        else:
            cmd = "G@QR"+" "+"NO"
            game_dict[cList[1]].send(cmd.encode('utf-8'))
    elif cList[0]=="G@QR1":
        cmd = "G@@"
        # game_dict[cList[3]].send("G@@".encode("utf-8"))
        users[cList[1]]=game_dict[cList[1]]
        users[cList[3]]=game_dict[cList[3]]
        del game_dict[cList[1]]
        del game_dict[cList[3]]
def MyExit(cList,ck):
    global users
    name = cList[1]
    del users[name]
    cmd = 'E'+' '+ctime().split(' ')[3]+':'+name+'离开聊天室'
    for user in users:
        users[user].send(cmd.encode('utf-8'))
    printStr = "" + name + "退出聊天室\n"#在连接显示框中显示是否连接成功
    text.insert(tkinter.INSERT, printStr)
    if users:
        pass
    else:
        Baik.Close()
def run(ck, ca):
    while True:     
        cmd = ck.recv(4096).decode('utf-8')#接受客户端发送的信息以1k作为单位这里接受到的信息为byte类型
        cList = cmd.split(' ')
        if cList[0] == "L":#调用登录函数
            MyLogin(cList,ck)
        elif cList[0]=='R':#调用注册函数
            MyRegister(cList,ck)
        elif cList[0]=='#':#调用回复信息函数
            MyMoreResv(cList,ck)
        elif cList[0]=='##':
            MyShowLove(cList,ck)
        elif cList[0]=='Q':#调用查询记录函数
            MyQuery(cList,ck)
        elif cList[0]=='S':#前方高能机器回复
            Auoresponse(cList,ck)
        elif cList[0] =='E':#处理客人退出
            MyExit(cList,ck)
        elif 'G' in cList[0]:
            if cList[0][0] =='G':
                MyGame(cList,ck)
def start():
    global Baik
    if users:
        pass
    else:
        Baik = BaikeSearch()

    ipStr = eip.get()#从输入端中获取ip
    portStr = eport.get()#从输入端中获取端口，注意端口取得时候不能被占用（可以取8080，9876，等）
    portStr = int(portStr)
    print(ipStr,portStr)
    print(type(ipStr),type(portStr))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4或ipv6，和相关协议的
    server.bind((ipStr,portStr))#绑定ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
    #2:bind()的参数是一个元组的形式
    server.listen(10)#设置监听，和设置连接的最大的数量
    printStr = "服务器启动成功\n"#，是否连接成功
    text.insert(tkinter.INSERT, printStr)#显示在信息窗口中
    while True:#这里用死循环是因为模拟的服务器要一直运行
        ck, ca = server.accept()#接受所连接的客户端的信息
        # 其中ca是ip和端口号组成的元组，ck有关客户端的信息
        t = threading.Thread(target=run, args=(ck, ca))#每连接一个客户端就开启一个线程
        #其中Thread函数中的传入函数的参数也是以元组的形式
        t.start()#开启线程
def startSever():
    s = threading.Thread(target=start)#启用一个线程开启服务器
    s.start()#开启线程
    # s.join()

#下面是关于界面的操作
labelIp = tkinter.Label(win, text='ip').grid(row=0, column=0)
labelPort = tkinter.Label(win, text='port').grid(row=1, column=0)
eip = tkinter.Variable()
eport = tkinter.Variable()
entryIp = tkinter.Entry(win, textvariable=eip).grid(row=0, column=1)
entryPort = tkinter.Entry(win, textvariable=eport).grid(row=1, column=1)
button = tkinter.Button(win, text="启动", command=startSever).grid(row=2, column=0)
text = tkinter.Text(win, height=20, width=30)
labeltext = tkinter.Label(win, text='连接消息').grid(row=3, column=0)
text.grid(row=3, column=1)
win.mainloop()