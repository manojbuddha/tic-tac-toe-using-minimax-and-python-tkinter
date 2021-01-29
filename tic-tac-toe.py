# required # 100,100 ! 300,100 ! 500,100 ! 100,300  ! 300,300 ! 500,300 ! 100,500 ! 300,500 ! 500,500

from tkinter import *
import tkinter as tk
import math
import random

TURN = "X"
BOARD = []
WIN = False

def minimax():
    
    pass

def findbestmove():
    
    pass

#Sets board array to none
def set_board():
    global BOARD
    BOARD=[]    
    for _ in range(0,3):
        row=[]
        for _ in range(0,3):
            row.append("NONE")
        BOARD.append(row)

#restarts game
def restart_game(): 
    global WIN
    global TURN
    game_canvas.delete("all")
    game_canvas.create_line(0,200,600,200,width=5)
    game_canvas.create_line(0,400,600,400,width=5)
    game_canvas.create_line(200,0,200,600,width=5)
    game_canvas.create_line(400,0,400,600,width=5)
    set_board()
    TURN = "X"    
    WIN = False


#gets the turn
def get_turn():
    global TURN
    return TURN

#toogles player turn from X and O
def set_turn():
    global TURN
    if TURN == "X":
        TURN = "O"
    else:
        TURN = "X"

def set_win():
    pass

#Checks for win board after every move
def check_win():
    
    global WIN
    for ind in range(0,3):
        if ind==0:
            mul=1
        elif ind==1:
            mul=3
        elif ind==2:
            mul=5        
        if BOARD[ind][0] == BOARD[ind][1] == BOARD[ind][2] == TURN :
            game_canvas.create_line(50,(mul)*100,550,(mul)*100,width=5,fill="green")
            WIN=True
        elif BOARD[0][ind] == BOARD[1][ind] == BOARD[2][ind] == TURN : 
            game_canvas.create_line((mul)*100,50,(mul)*100,550,width=5,fill="green")            
            WIN=True
    if BOARD[0][0]==BOARD[1][1]==BOARD[2][2]==TURN or BOARD[0][2]==BOARD[1][1]==BOARD[2][0]==TURN:
            if BOARD[0][0]==BOARD[1][1]==BOARD[2][2]==TURN:
                game_canvas.create_line(50,50,550,550,width=5,fil="green")            
            elif BOARD[0][2]==BOARD[1][1]==BOARD[2][0]==TURN:
                game_canvas.create_line(50,550,550,50,width=5,fill="green")                            
            WIN=True        
    if WIN==True:
        win_rect = game_canvas.create_rectangle(100, 200, 500, 400, fill="green",width=2,stipple='gray75')
        game_canvas.create_text(300,300,text=TURN+" Wins!!",font=('Pursia',50))
        return
    drawcheck = 0
    for row in BOARD:
        for cell in row:
            if drawcheck>=1:
                return
            if cell=='NONE':
                drawcheck+=1
    if drawcheck == 0:
        win_rect = game_canvas.create_rectangle(100, 200, 500, 400, fill="green",width=2,stipple='gray75')
        game_canvas.create_text(300,300,text="Draw!!",font=('Pursia',50))

def ai_turn():
    global BOARD
    #game_canvas.create_line(0,0,600,600,width=5)
    if not WIN:
        count = 0
        unraveled_board = []
        co_ord = []
        for i in range(0,3):
            for j in range(0,3):
                if BOARD[i][j] == 'NONE':
                    co_ord.append([i,j])
                    unraveled_board.append(count)
                count+=1
        if len(unraveled_board) == 0:
            return
        choice = random.choice(unraveled_board)
        co_ord1 = co_ord[unraveled_board.index(choice)]
        loc=[]
        for i in range(0,len(co_ord1)):
    
            if co_ord1[i] == 0:
                loc.append(100)
            if co_ord1[i] == 1:
                loc.append(300)
            if co_ord1[i] == 2:
                loc.append(500)    
        turn = get_turn()            
        x=loc[1]
        y=loc[0]    
        print(x,y)
        if turn=="X":
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="red")
        else:
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="blue")  
        BOARD[co_ord1[0]][co_ord1[1]] = turn
        check_win()
        set_turn()          
        
        print(choice)
        print(co_ord)
        print(unraveled_board)
        print(BOARD)
        

def onObjectClick(event):
    if not WIN:
        global BOARD
        if event.x > 0 and event.x <200:
            x=100
        if event.y > 0 and event.y <200:
            y=100
        if event.x > 200 and event.x <400:
            x=300
        if event.y > 200 and event.y <400:
            y=300
        if event.x > 400 and event.x <600:
            x=500
        if event.y > 400 and event.y <600:
            y=500        
    
        turn = get_turn()
        if x==100:
            l1=0
        if x==300:
            l1=1
        if x==500:
            l1=2           
        if y==100:
            l2=0
        if y==300:
            l2=1
        if y==500:
            l2=2   
        if BOARD[l2][l1]!='NONE':
            print("turn rejected")
            return
        BOARD[l2][l1] = turn
        print(BOARD)
        print(x,y)
        if turn=="X":
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="red")
        else:
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="blue")
        check_win()
        set_turn()
        ai_turn()
        
                
        

window = Tk()
window.title("tic-tac-toe")
window.geometry("600x650")
game_canvas = Canvas(window,width=600,height=600, bg='white')
game_canvas.pack()
set_board()
Button(window,text="Restart game",command=restart_game).pack()
game_canvas.create_line(0,200,600,200,width=5)
game_canvas.create_line(0,400,600,400,width=5)
game_canvas.create_line(200,0,200,600,width=5)
game_canvas.create_line(400,0,400,600,width=5)
game_canvas.bind("<Button>", onObjectClick)
window.resizable(False,False)  
window.mainloop()