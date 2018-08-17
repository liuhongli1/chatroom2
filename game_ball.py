from tkinter import *
import random
import threading
import time #调用时间函数让游戏有真实感
paddle_pos1=None

def My_game(rival_name,ck,first_into,name):
#将对手排的w位置实时发过来和击球时速度传入作为小球返回的速度的依据
    print(name)
    ck = ck
    first_into = first_into
    print(first_into)
    tk = Tk()
    tk.title("Game") 
    #给窗口命名
    tk.resizable(0,0)
    #窗口的大小不可调整，第一个参数表示长，0，0的意思是“窗口的大小在水平方向上和垂直方向上都不能改变”
    tk.wm_attributes("-topmost",1)
    #将画布的窗口始终放到所有其他窗口之前
    canvas = Canvas(tk,width=500, height=400,bg='purple', bd=0, highlightthickness=0)#后两个参数作用：确保画布之外没有边框，使得屏幕更美观
    canvas.pack()
    tk.update()#为动画做好初始化
    ball_id = canvas.create_oval(10, 10, 20, 20, fill='red')#（10,10）表示左上角x,y坐标，（25,25）表示右下角x,y坐标，填充色
    canvas.move(ball_id, 235,185)#将球移动到画布中心
    
    paddle_id = canvas.create_rectangle(0, 0, 100, 10, fill='green') 
     # （10,10）
    paddle_id1 = canvas.create_rectangle(0, 0, 100, 10, fill='green')
    # 创建对手的排
    canvas.move(paddle_id, 200, 390)  # 自己的排放在最下面中间
    canvas.move(paddle_id1, 200, 0)#将对手的排放在最上方
    
    paddle_x = 0
    paddle_x1=0
    pos = canvas.coords(ball_id)
    paddle_pos=canvas.coords(paddle_id)
    paddle_pos1=canvas.coords(paddle_id1)
    hit_bottom = False
    gama_cyclic = True
    game_order=True
    def turn_left(evt):#改变向左向右的方向
        nonlocal paddle_x
        if paddle_pos[0]<=0:
            paddle_x=0      
        else:
            paddle_x = -1
    def turn_right(evt):
        nonlocal paddle_x
        if paddle_pos[2]>=canvas.winfo_width():
            paddle_x=0
            
        else:
            paddle_x = 1
    def turn_top(evt):
        nonlocal paddle_x
        if paddle_x==0:
            pass
        elif paddle_x<0:
            paddle_x-=1
        else:
            paddle_x+=1
    def turn_buttom(evt):
        nonlocal paddle_x
        if paddle_x == 0:
            pass
        elif paddle_x<0:
            paddle_x+=1
        else:
            paddle_x-=1
    def send_go():
        nonlocal first_into
        nonlocal paddle_x
        nonlocal paddle_x1
        nonlocal ck
        nonlocal rival_name
        nonlocal hit_bottom
        nonlocal first_into
        nonlocal gama_cyclic
        def my_destroy():
            nonlocal first_into
            nonlocal first_into
            nonlocal paddle_x1
            nonlocal ck
            nonlocal rival_name
            nonlocal paddle_x
            nonlocal hit_bottom
            nonlocal gama_cyclic
            tk1.destroy()
            time.sleep(3)
            while hit_bottom ==False:
            
                # print('循环改变')
                cmd = "G#"+' '+str(paddle_x)+" "+rival_name
                ck.send(cmd.encode('utf-8'))
                # print('信息发送成功')
                cmd=ck.recv(1024).decode('utf-8')
                paddle_x1=int(cmd)
                # print('paddle_x=',paddle_x,"paddle_x1=",paddle_x1)
                # print("信息接受成功")
                tub=draw(ball_id,paddle_id,paddle_id1)
                tk.update_idletasks()
                tk.update()
                time.sleep(0.01)
            
        tk1=Tk()
        tk1.title("over")
        tk1.resizable(0,0)
        label=Label(tk1,text='确定后三秒游戏开始',fg='red',font='15')
        label.pack()
        buttom=Button(tk1,text='确定',bg='green',command=my_destroy)
        buttom.pack()
        tk1.mainloop()
    def button_fun():
        print("调用循环命令成功")
        while True:
            
            if gama_cyclic:
                break
            else:
                print("进入循环接受有洗命令")
                cmd_list=ck.recv(1204).decode('utf-8').split(' ')
                print(cmd_list)
                print("接受到游戏命令成功")
                if cmd_list[0]=="G$":
                    print("接受到球位置更改信息")
                    game_updata_fun(cmd_list)
                elif cmd_list[0]=="G@A":
                    print('接受到请求再来一次的请求')
                    game_agin_fun(cmd_list)
                elif cmd_list[0]=='G@Q':
                    print('接收到对方请求退出游戏的请求')
                    game_quit_fun(cmd_list)
                elif cmd_list[0]=="G@AR":
                    print("对方已经对你请求在来一次的请求 做出回复")
                    game_Areply_fun(cmd_list)
                elif cmd_list[0]=="G@QR":
                    print("对方已经对你请求退出游戏的请求 做出回复")
                    game_Qreply_fun(cmd_list)
                elif cmd_list[0]=="G@@":
                    print('可以退出游戏')
                    
    def game_Qreply_fun(cmd_list):
        nonlocal hit_bottom
        nonlocal gama_cyclic
        nonlocal ck
        nonlocal rival_name
        def quit_game_agin():
            nonlocal ck
            nonlocal rival_name
            cmd = "G@Q"+ " "+ rival_name
            ck.send(cmd.encode("utf-8"))
            tk6.destroy()
        def no_quit_game():
            tk6.destroy()
        def confirm_quit_game():
            nonlocal hit_bottom
            nonlocal gama_cyclic
            nonlocal ck
            nonlocal rival_name
            gama_cyclic = True
            cmd = "G@QR1"+' '+rival_name+' '+"OK"+" "+name
            ck.send(cmd.encode("utf-8"))
            tk6.destroy()
            time.sleep(2)
            tk.destroy()
        tk6=Tk()
        tk6.title("提示")
        tk6.resizable(0,0)
        labelC=Label(tk6)
        labelC.pack()
        if cmd_list[1]=="OK":
            labelC["text"]="对方同意您退出游戏"
            buttonC=Button(tk6,text="确定",command=confirm_quit_game)
            buttonC.pack()
        if cmd_list[1]=="NO":
            labelC["text"]="对方拒绝您退出游戏，是否继续退出"
            buttonC=Button(tk6,text="是",command=quit_game_agin)
            buttonC.pack()
            buttonC1=Button(tk6,text="否",command=no_quit_game)
            buttonC1.pack()

        tk6.mainloop()

    def game_Areply_fun(cmd_list):
        nonlocal ck 
        nonlocal hit_bottom
        nonlocal gama_cyclic
        nonlocal name
        nonlocal rival_name
        def into_game_agin():
            nonlocal hit_bottom
            nonlocal name
            nonlocal ck
            nonlocal gama_cyclic
            nonlocal rival_name
            cmd = "G@AR1"+' '+rival_name+' '+"OK"+" "+name
            ck.send(cmd.encode('utf-8'))
            hit_bottom = False
            gama_cyclic = True
            time.sleep(0.1)
            tk5.destroy()
            send_go()
        def nointo_game_agin():
            tk5.destroy()
        tk5=Tk()
        tk5.title("提示")
        labelA=Label(tk5)
        labelA.pack()
        buttom=Button(tk5,text='确定',bg='green')
        buttom.pack()

        if cmd_list[1]=="OK":
            labelA["text"]="对方接受请求，游戏即将进行"
            buttom["command"]=into_game_agin
        else:
            labelA["text"]="对方拒绝请求"
            buttom["command"]=nointo_game_agin
        tk5.mainloop()

    def game_quit_fun(cmd_list):
        nonlocal ck
        nonlocal rival_name
        nonlocal name
        nonlocal gama_cyclic
        def agree_quit():
            nonlocal ck
            nonlocal name
            nonlocal rival_name
            nonlocal gama_cyclic
            gama_cyclic = False
            cmd = "G@QR"+' '+rival_name+' '+"OK"+" "+name
            ck.send(cmd.encode("utf-8"))
            tk4.destroy()
            time.sleep(2)
            tk.destroy()
        def refuse_quit():
            nonlocal ck
            cmd = "G@QR"+' '+rival_name+" "+"NO"
            ck.send(cmd.encode("utf-8"))
            tk4.destroy()
        if cmd_list[1]=="first":
            tk4 = Tk()
            tk4.title("提示")
            tk4.resizable(0,0)
            labelQ=Label(tk4,text="对方想要退出游戏，是否同意")
            labelQ.pack()
            buttonG = Button(tk4,text="同意",command=agree_quit)
            buttonG.pack(side=LEFT)
            buttonG1 = Button(tk4,text="拒绝",command=refuse_quit)
            buttonG1.pack(side=LEFT)
            tk4.mainloop
        else:
            tk4 = Tk()
            tk4.title("提示")
            tk4.resizable(0,0)
            labelQ=Label(tk4,text="对方坚持退出，您必须同意")
            labelQ.pack()
            buttonG = Button(tk4,text="同意",command=agree_quit)
            buttonG.pack(side=LEFT)
            tk4.mainloop

    def game_agin_fun(cmd_list):
        nonlocal ck
        nonlocal rival_name
        nonlocal hit_bottom
        nonlocal gama_cyclic
        nonlocal name
        def agree_agin():
            nonlocal ck
            nonlocal hit_bottom
            nonlocal gama_cyclic
            nonlocal rival_name
            nonlocal name
            hit_bottom = False
            gama_cyclic=True
            cmd = "G@AR"+' '+rival_name+' '+"OK"+" "+name
            ck.send(cmd.encode('utf-8'))
            time.sleep(0.1)
            tk3.destroy()
            send_go()
        def refuse_agin():
            nonlocal ck
            cmd = "G@AR"+' '+rival_name+' '+"NO"
            ck.send(cmd.encode('utf-8'))
            tk3.destroy()
        tk3 = Tk()
        tk3.title("提示")
        tk3.resizable(0,0)
        label=Label(tk3,text="对方请求再来一局")
        label.pack()
        buttonG = Button(tk3,text="同意",command=agree_agin)
        buttonG.pack(side=LEFT)
        buttonG1 = Button(tk3,text="拒绝",command=refuse_agin)
        buttonG1.pack(side=LEFT)
        tk3.mainloop()
    def game_updata_fun(cmd_list):
        nonlocal ck
        nonlocal ball_y
        nonlocal ball_x
        ball_x,ball_y = int(cmd_list[1]),-int(cmd_list[2])

    def play_agin():
        nonlocal hit_bottom
        nonlocal paddle_x
        nonlocal ball_x
        nonlocal ball_y
        nonlocal ball_id
        nonlocal pos
        nonlocal paddle_pos
        nonlocal paddle_pos1
        nonlocal gama_cyclic
        def tk7destroy():
            tk7.destroy()
        if gama_cyclic:

            starts = [-3,-2,-1,1,2,3]
            random.shuffle(starts)

            ball_x = starts[0]
            ball_y = starts[0]
            cmd = "G$"+" "+rival_name+" "+str(ball_x)+" "+str(ball_y)
            ck.send(cmd.encode("utf-8"))
            time.sleep(0.01)
            
            cmd = "G@A"+" "+rival_name
            ck.send(cmd.encode("utf-8"))
            time.sleep(0.5)
            gama_cyclic = False
            button_fun()
        else:
            tk7=Tk()
            tk7.title("提示")
            labelC1=Label(tk7,text="您是赢者，把主动权给别人吧")
            labelC1.pack()
            buttomC=Button(tk7,text='确定',command=tk7destroy)
            buttomC.pack()
            tk7.mainloop()
    def send_quit():
        def tk7destroy():
            tk7.destroy()
        if gama_cyclic:
            cmd="G@Q"+" "+rival_name
            ck.send(cmd.encode("utf-8"))
        else:
            tk7=Tk()
            tk7.title("提示")
            labelC1=Label(tk7,text="您是赢者，把主动权给别人吧")
            labelC1.pack()
            buttomC=Button(tk7,text='确定',command=tk7destroy)
            buttomC.pack()
            tk7.mainloop()
    canvas.bind_all('<KeyPress-Left>', turn_left)
    canvas.bind_all('<KeyPress-Up>', turn_top)
    #按键时调用函数，< >内为 事件名字，让对象对操作有反应
    canvas.bind_all('<KeyPress-Down>', turn_buttom)
    canvas.bind_all('<KeyPress-Right>', turn_right)
    
    def draw(ball_id,paddle_id,paddle_id1):
        nonlocal hit_bottom
        nonlocal paddle_x
        nonlocal paddle_x1
        nonlocal ball_x
        nonlocal ball_y
        nonlocal pos
        nonlocal paddle_pos
        nonlocal paddle_pos1
        nonlocal gama_cyclic
        # print("ball_x=",ball_x,'ball_y=',ball_y)
        canvas.move(ball_id,ball_x,ball_y)
        canvas.move(paddle_id,paddle_x,0)
        canvas.move(paddle_id1,paddle_x1,0)
        pos = canvas.coords(ball_id)
        paddle_pos1=canvas.coords(paddle_id1)
        paddle_pos=canvas.coords(paddle_id)
        if paddle_pos[0]<0:
            paddle_x=0
            paddle_pos[0]=0
            paddle_pos[2]=100
            
        elif paddle_pos[2]>canvas.winfo_width():
            paddle_x=0
            paddle_pos[0]=canvas.winfo_width()-100
            paddle_pos[2]=canvas.winfo_width()
        else:
            paddle_pos=canvas.coords(paddle_id)
        if paddle_pos1[0]<0:
            paddle_x=0
            paddle_pos1[0]=0
            paddle_pos1[2]=100
            
        elif paddle_pos[2]>canvas.winfo_width():
            paddle_x=0
            paddle_pos1[0]=canvas.winfo_width()-100
            paddle_pos1[2]=canvas.winfo_width()
        else:
            paddle_pos=canvas.coords(paddle_id)
        def my_Destroy():
            
            tk1.destroy()
            
            print("输赢已经出来")
            button_fun()
        def my_destroy():
            nonlocal ball_id
            tk1.destroy()
            

        # print(pos[2],canvas.winfo_width(),pos[0])
        if (paddle_pos1[0]-10)<=pos[0]<=paddle_pos1[2] and 0<pos[1]<=10:
            ball_y = -ball_y

        elif pos[1] <= 0:
            x=250-pos[0]
            # hit_bottom ==False
            canvas.move(ball_id, x,195)
            gama_cyclic = False
            hit_bottom = True
            button2['text']="等待"
            button2["command"]=play_agin
            tk1=Tk()
            tk1.title("over")
            tk1.resizable(0,0)
            label=Label(tk1,text='你赢了,亲等待输家的请求',fg='red',font='15')
            label.pack()
            buttom=Button(tk1,text='确定',bg='green',command=my_Destroy)
            buttom.pack()
            tk1.mainloop()


        if (paddle_pos[0]-10)<=pos[0]<=paddle_pos[2] and 390<=pos[3]<400:
            ball_y = -ball_y
        elif pos[2] >= canvas.winfo_width() or pos[0] <= 0:
            ball_x = -ball_x
        elif pos[3] >= canvas.winfo_height():
            hit_bottom = True
            x=250-pos[0]
            # hit_bottom ==False
            canvas.move(ball_id, x,-195)
            button2["text"]="再来一局"
            button2["command"]=play_agin
            tk1=Tk()
            tk1.title("over")
            tk.resizable(0,0)
            label=Label(tk1,text='你输了，您将拥有主动权',fg='red',font='15')
            label.pack()
            buttom=Button(tk1,text='确定',bg='green',command=my_destroy)
            buttom.pack()
            tk1.mainloop()
            return 'Fail'
        
    frame = Frame(tk)
    frame.pack()
    # button1=Button(frame,text='准备',command=send_ready).pack(side=LEFT)

    button2=Button(frame,text='开始',command=send_go).pack(side=LEFT)
    # button3=Button(frame,text='再来一局',command=play_agin).pack(side=LEFT)
    buttom4=Button(frame,text='退出',command=send_quit).pack(side=LEFT)    
    if first_into :
    #     tk2=Tk()
    #     tk2.title("友情提示")
    #     label1=Label(tk2,text="您是邀请方，将由您发起开始",fg="green")
    #     label1.pack()
        starts = [-3,-2,-1,1,2,3]
        random.shuffle(starts)

        ball_x = starts[0]
        ball_y = starts[0]
        cmd = "G@"+" "+rival_name+" "+str(ball_x)+" "+str(ball_y)
        ck.send(cmd.encode("utf-8"))
        time.sleep(2)
        # tk2.destroy()
        # tk2.mainloop()
    else:
        # tk2=Tk()
        # tk2.title("友情提示")
        # label1=Label(tk2,text="您是被邀请方，由对方发起开始",fg="green")
        # label1.pack()
        # cmd = "G@"+" "+ball_x+" "+ball_y
        cmd_list=ck.recv(1024).decode('utf-8').split(' ')
        ball_x=int(cmd_list[1])
        ball_y=-int(cmd_list[2])
        time.sleep(2)
        # tk2.destroy()
        # tk2.mainloop()
        
   

    tk.mainloop()
    return True
if __name__ == '__main__':
    My_game()