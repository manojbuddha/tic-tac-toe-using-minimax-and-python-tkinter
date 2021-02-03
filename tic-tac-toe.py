# required # 100,100 ! 300,100 ! 500,100 ! 100,300  ! 300,300 ! 500,300 ! 100,500 ! 300,500 ! 500,500

from tkinter import *
# import tkinter as tk
import math
import random
import time

TURN = "X"
BOARD = []
MODE = ["Multiplayer","Single"]
WIN = False
SWAPTURN = True
player = "O"
opponent = "X"
score_x = 0
score_o = 0
score_draw = 0

def evaluate(board):

    for ind in range(0,3):

        if board[ind][0] == board[ind][1] == board[ind][2] :
            if board[ind][0] == opponent:
                return -10
            elif board[ind][0] == player:
                return 10

        elif board[0][ind] == board[1][ind] == board[2][ind]: 
            if board[0][ind] == opponent:
                return -10
            elif board[0][ind] == player:
                return 10

    if board[0][0]==board[1][1]  == board[2][2]:
            if board[1][1] == opponent:
                return -10
            elif board[1][1] == player:
                return 10
    if board[0][2]==board[1][1] ==board[2][0]:
            if board[1][1] == opponent:
                return -10
            elif board[1][1] == player:
                return 10


    return 0

def check_draw(board):
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == "NONE":
                return False
    return True
    
def minimax(board, is_max):

    score = evaluate(board)
    
    if score == 10:
        return score
    if score == -10:
        return score    

    if check_draw(board):
        return 0
    
    if is_max:
        best = -1000
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j]=="NONE":                
                    board[i][j] = player
                    best = max(best,minimax(board, not is_max))
                    
                    board[i][j] = "NONE"
        return best
        

    else:
        best = 1000
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j]=="NONE":        
                    board[i][j] = opponent
                    best = min(best,minimax(board, not is_max))
                    board[i][j] = "NONE"
        return best
    
    return best

def find_best_move(board):
    best = -1000
    best_move_location = []
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j]=="NONE":
                board[i][j] = player
                move_score = minimax(board,False)
                board[i][j] = "NONE"    
                # print(i,j,move_score,best)
                if move_score > best:                  
                    best_move_location = [i,j]
                    best = move_score

    return best_move_location

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
    global SWAPTURN
    game_canvas.delete("all")
    game_canvas.create_line(0,200,600,200,width=5, fill="yellow")
    game_canvas.create_line(0,400,600,400,width=5, fill="yellow")
    game_canvas.create_line(200,0,200,600,width=5, fill="yellow")
    game_canvas.create_line(400,0,400,600,width=5, fill="yellow")
    set_board()
    TURN = "X"    
    WIN = False
    turn_label.configure(text="Turn: "+TURN)
    if mode.get()=="Single":
        if SWAPTURN:
            TURN = "O" 
            load_rect = game_canvas.create_rectangle(150, 250, 450, 350, fill="yellow",width=2,stipple='gray50')
            load_text = game_canvas.create_text(300,300,text="Thinking...!!",font=('Pursia',25))  
            ai_turn()
            game_canvas.delete(load_rect)
            game_canvas.delete(load_text)
            SWAPTURN = not SWAPTURN
        else:
            SWAPTURN = not SWAPTURN

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

#Checks for win board after every move
def check_win():
    global score_x
    global score_o
    global score_draw
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
        if TURN == "X":
            score_x+=1
        if TURN == "O":
            score_o+=1            
        win_rect = game_canvas.create_rectangle(150, 250, 450, 350, fill="#ebb81e",width=2,stipple='gray75')
        game_canvas.create_text(300,300,text=TURN+" Wins!!",font=('Pursia',25))
        update_score()
        return

    if check_draw(BOARD):
        score_draw+=1
        win_rect = game_canvas.create_rectangle(150, 250, 450, 350, fill="#ebb81e",width=2,stipple='gray75')
        game_canvas.create_text(300,300,text="Draw!!",font=('Pursia',25))
        update_score()
        return

def ai_turn():
    global BOARD
    window.update()  
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
        # the below two lines are to place randomly
        # choice = random.choice(unraveled_board)
        # co_ord1 = co_ord[unraveled_board.index(choice)]
        co_ord1 = find_best_move(BOARD)
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
        if turn=="X":
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="red")
        else:
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="blue")  
        BOARD[co_ord1[0]][co_ord1[1]] = turn
        check_win()
        set_turn()          
        
def change_mode(*args):
    global mode
    mode.set(mode.get())
    print(mode.get())
    restart_game()

def on_canvas_click(event):
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
            return
        BOARD[l2][l1] = turn
        if turn=="X":
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="red")
        else:
            game_canvas.create_text(x,y,text=turn,font=('Pursia',80),fil="blue")
        check_win()
        set_turn()
        if mode.get() == "Single":
            ai_turn()
        turn_label.configure(text="Turn: "+TURN)          

def update_score():
    x_label.config(text = "X: "+str(score_x))
    o_label.config(text = "O: "+str(score_o))
    draw_label.config(text = "Draw: "+str(score_draw))


window = Tk()
window.title("tic-tac-toe")
window.geometry("600x690")
frame = Frame(window)
frame.pack()
mode = StringVar(frame)
mode.set("Single")
mode.trace("w", change_mode)
OptionMenu(frame, mode,*MODE).grid(row=0,column=0)
Button(frame,text="Restart game",command=restart_game).grid(row=0,column=1,padx=100,pady=5)
turn_label = Label(frame,text="Turn: "+"X")
turn_label.grid(row=0,column=2)
x_label = Label(frame,text = "X: "+str(score_x),font=80, fg="black")
x_label.grid(row=1,column=0)
o_label = Label(frame,text = "O: "+str(score_o),font=80, fg="black")
o_label.grid(row=1,column=1)
draw_label = Label(frame,text = "Draw: "+str(score_draw),font=80, fg="black")
draw_label.grid(row=1,column=2)

game_canvas = Canvas(window,width=600,height=600, bg='black')
game_canvas.pack()
set_board()
game_canvas.create_line(0,200,600,200,width=5, fill="yellow")
game_canvas.create_line(0,400,600,400,width=5, fill="yellow")
game_canvas.create_line(200,0,200,600,width=5, fill="yellow")
game_canvas.create_line(400,0,400,600,width=5, fill="yellow")
game_canvas.bind("<Button>", on_canvas_click)
window.resizable()  
window.mainloop()