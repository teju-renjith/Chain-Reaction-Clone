import pygame
from pygame.locals import *
import math
pygame.font.init()
import sys

Height=600
width=500
height=500
white=(255,255,255)
black=(0,0,0)
red=(255,76,62)
green=(138,255,33)
win=pygame.display.set_mode((width,Height))
pygame.display.set_caption("Chain Reaction 2 Player")

grid_count = [[0 for i in range(5)] for j in range(5)]
grid_color = [['nil' for i in range(5)] for j in range(5)]
presentplayer='r' 
total_red=0
total_green=0
winner='X'

corner=[[0,0],[4,0],[0,4],[4,4]]
edges=[]
for X in range(1,4):
    edges.append([X,0])
    edges.append([X,4])
for Y in range(1,4):
    edges.append([0,Y])
    edges.append([4,Y])

def draw_win():
    win.fill(black)

    if presentplayer=='r':
        color=red
    else:
        color=green

    for i in range(0,6):
        line_h=pygame.Rect(0,i*100-2.5,width,5)
        line_v=pygame.Rect(i*100-2.5,0,5,height)
        pygame.draw.rect(win,color,line_h)
        pygame.draw.rect(win,color,line_v)
        pygame.display.update()

    text=pygame.font.SysFont("calibri",60)
    op=text.render("CHAIN REACTION",1,white)
    win.blit(op,(250-op.get_width()/2,height+50-op.get_height()/2))
    pygame.display.update()

def draw_coloured_lines():
    if presentplayer=='r':
        color=red
    else:
        color=green
    for i in range(0,6):
        line_h=pygame.Rect(0,i*100-2.5,width,5)
        line_v=pygame.Rect(i*100-2.5,0,5,height)
        pygame.draw.rect(win,color,line_h)
        pygame.draw.rect(win,color,line_v)
        pygame.display.update()

def put_one(x,y,color):
    global grid_count,presentplayer,grid_color,total_green,total_red
    blacksq=pygame.Rect(x*100+3,y*100+3,90,90)
    pygame.draw.rect(win,black,blacksq)
    rad=20
    cwid=20
    pygame.draw.circle(win, color, (x*100+50,y*100+50), 20, 20)
    grid_count[x][y]=1
    grid_color[x][y]=presentplayer
    
    pygame.display.update()

def put_two(x,y,color):
    global grid_count,presentplayer,grid_color,total_green,total_red
    blacksq=pygame.Rect(x*100+3,y*100+3,90,90)
    pygame.draw.rect(win,black,blacksq)
    rad=20
    cwid=20
    pygame.draw.circle(win, color, (x*100+50-20,y*100+50), 20, 20)
    pygame.draw.circle(win, color, (x*100+50+20,y*100+50), 20, 20)
    grid_count[x][y]=2
    grid_color[x][y]=presentplayer
    
    pygame.display.update()

def put_three(x,y,color):
    global grid_count,presentplayer,grid_color,total_green,total_red
    blacksq=pygame.Rect(x*100+3,y*100+3,90,90)
    pygame.draw.rect(win,black,blacksq)
    rad=20
    cwid=20
    pygame.draw.circle(win, color, (x*100+50,y*100+50 - 2*rad/math.sqrt(3)), 20, 20)
    pygame.draw.circle(win, color, (x*100+50+20,y*100+50+rad/math.sqrt(3)), 20, 20)
    pygame.draw.circle(win, color, (x*100+50-20,y*100+50+rad/math.sqrt(3)), 20, 20)
    grid_count[x][y]=3
    grid_color[x][y]=presentplayer
    
    pygame.display.update()  

recursion_count=0
def bomb(x,y,color):
    global grid_count,presentplayer,grid_color,total_green,total_red,winner,recursion_count

    recursion_count+=1
    if recursion_count>25:
        return

    blacksq=pygame.Rect(x*100+3,y*100+3,90,90)
    pygame.draw.rect(win,black,blacksq)

    clr=grid_color[x][y]
    if clr=='r':
        total_red-=grid_count[x][y]
    else:
        total_green-=grid_count[x][y]

    grid_count[x][y]=0
    grid_color[x][y]='nil'

    if x>0:
        putitem(x-1,y,color,1)
        
    if x<4:
        putitem(x+1,y,color,1)
        
    if y>0:
        putitem(x,y-1,color,1)
        
    if y<4:
        putitem(x,y+1,color,1)
    
    if total_green==0:
        winner="RED"
        return
    if total_red==0:
        winner="GREEN"
        return


def putitem2(x,y,color):
    global grid_count,presentplayer,grid_color,corner,edges,total_green,total_red
    count=grid_count[x][y]
    clr=grid_color[x][y]
    
    if count==0:
            put_one(x,y,color)
            if color==red:
                total_red+=1
            else:
                total_green+=1

    elif count==1:
        if [x,y] not in corner:
            put_two(x,y,color)

            if clr!='nil' and clr!=presentplayer:
                if color==red:
                    total_red+=2
                    total_green-=count
                else:
                    total_green+=2
                    total_red-=count
            else:
                if color==red:
                    total_red+=1
                else:
                    total_green+=1
                
        else:
            bomb(x,y,color)
            
    elif count==2:
        if [x,y] not in edges:
            put_three(x,y,color)

            if clr!='nil' and clr!=presentplayer:
                if color==red:
                    total_red+=3
                    total_green-=count
                else:
                    total_green+=3
                    total_red-=count
            else:
                if color==red:
                    total_red+=1
                else:
                    total_green+=1

        else:
            bomb(x,y,color)
    else:
        bomb(x,y,color)

def putitem(x,y,color,mode):   #if mode is 0,,,normal else bombed one
    global presentplayer,grid_color,flag

    clr=grid_color[x][y]
   
    if mode ==0:
        if clr == presentplayer or clr == 'nil':
            putitem2(x,y,color)
        else:
            flag=1
    elif mode==1:
        putitem2(x,y,color)

flag=0     
def click():
    global grid_count,presentplayer,grid_color,flag,recursion_count
    x,y=pygame.mouse.get_pos()   #imagine like graph NOT matrix : x ---> and y downwards....doesnt matter
    x=x//100
    y=y//100
    
    if presentplayer=='r':
        color=red
    else:
        color=green

    recursion_count=0
    putitem(x,y,color,0)
    
    if flag==0 and winner=='X':
        if presentplayer=='r':
            presentplayer='g'
        else:
            presentplayer='r'
        draw_coloured_lines()
    else:
        flag=0                                    # this means we clicked on existing or diff colored item like red player clicked on green ball
    
def restart():
    global grid_color,grid_count,presentplayer,total_red,total_green,winner
    grid_count = [[0 for i in range(5)] for j in range(5)]
    grid_color = [['nil' for i in range(5)] for j in range(5)]
    presentplayer='r' 
    total_red=0
    total_green=0
    winner='X'
    draw_win()

def gameover():
    global winner
    blackrect=pygame.Rect(0,505,500,100)
    pygame.draw.rect(win,black,blackrect)
    text=pygame.font.SysFont("calibri",60)
    wintext=text.render(winner+" WON",1,white)
    win.blit(wintext,(250-wintext.get_width()/2,height+50-wintext.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)
    restart()
   
def main():
    run=True
    clock=pygame.time.Clock()
    clock.tick(60)
    draw_win()
    while run:
        for event in pygame.event.get():
            if winner!='X':
                gameover()
            if event.type==pygame.QUIT:
                run=False
            if event.type==MOUSEBUTTONDOWN:
                click()
            
    pygame.quit()

if __name__=='__main__':
    main()