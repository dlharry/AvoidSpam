# This is a game made by Hanmin Liu
# Run in resolution of 1280x720
# Use <Up><Down><Left><Right> to move the player around under the goal of reach the yellow block
from tkinter import *
from tkinter import messagebox
import random
import time
import os

if(os.path.exists("./data.txt")==False):
    initial_data = open("data.txt","w")
    initial_data.write("nobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0")
    initial_data.close()
if(os.path.exists("./leaderboard.txt")==False):
    initial_leaderboard = open("leaderboard.txt","x")
    initial_leaderboard.write("nobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0\nnobody 0")
    initial_leaderboard.close()

BACKGROUND = "black"
GOAL = "yellow"
PAUSE = "white"
PAUSE_TITLE = "black"
GAMEOVER_TITLE = "red"
WIN_TITLE = "yellow"
LEADERBOARD_NAME = "blue"
PLAYER = "blue"
SETTING_BG = "white"


levelNumber = 0

window = Tk()
window.geometry("1280x720")
window.title("Avoid Spike")
spikeImage = PhotoImage(file="spike.png")
window.spikeImage = spikeImage

width = 1280
height = 720
name = "nobody"
cheatcode = "qwer"
checkCheat = [0,0,0,0]
countCheat = 0

upKey = "<Up>"
downKey = "<Down>"
leftKey = "<Left>"
rightKey = "<Right>"
bossKey = "b"

cheatactive = False
gameOver = False
win = False
spikePos = []
playerPos = [width-50, height-50, width-10, height-10]
goalPos = [width/2, height/2, width/2+50, height/2+50]
overSummon = False

canvas = Canvas(window, width=width, height=height, bg=BACKGROUND)
pausemenu = Canvas(window, width=200, height=400, bg=PAUSE)

boss_image = PhotoImage(file="bosscome.png")
window.boss_image=boss_image

bosscome = False

def checkCheat(event):
    global countCheat,cheatactive
    if(event.keysym == cheatcode[countCheat]):
        countCheat += 1
    if countCheat >= len(cheatcode):
        print("cheatactive")
        cheatactive = True

def bosswitch(event):
    global bosscome
    if(bosscome == False):
        bosscome = True
        global canvas
        canvas.delete("all")
        canvas.create_image(0,0, image=window.boss_image, anchor="nw")
    else:
        bosscome = False
        menu()
canvas.bind(bossKey, bosswitch)
canvas.focus_set()

canvas.bind("<Key>", checkCheat)

def save():
    f = open("data.txt")
    temp_str = f.read()
    temp = temp_str.split("\n")
    have = False
    for i in range(len(temp)):
        x = temp[i].split(" ")
        if x[0] == name:
            x[1] = str(levelNumber)
            have = True
    g = open("data.txt", "w")
    if(have == False):
        g.write(temp_str)
        g.write(name+" "+str(levelNumber)+"\n")
    else:
        g.write(temp_str)
    g.close()
    f.close()
    if(gameOver == False):
        messagebox.showinfo(title="info", message="the game successfully saved")

def left(event):
    canvas.move(player,-speed,0)
    #print("left")
def right(event):
    canvas.move(player,speed,0)
    #print("right")
def up(event):
    canvas.move(player,0,-speed)
    #print("up")
def down(event):
    canvas.move(player,0,speed)
    #print("down")

def put_spike():
    global playerPos
    #print(playerPos)
    x = random.randint(0, width)
    y = random.randint(0, height)
    if(overlap([x,y,x+20,y+20],playerPos)):
        print("not puttin")
        return False
    spikePos.append([x,y,x+20,y+20])
    canvas.create_image(x,y,image=window.spikeImage)
    return True

def resume():
    global pausemenu
    global canvas
    pausemenu.destroy()
    canvas.focus_set()

def pause():
    global pausemenu
    pausemenu = Canvas(window, width=200, height=400, bg=PAUSE)
    pausemenu.place(x=width/2,y=50, anchor="n")
    pausemenu.focus_set()
    pausemenu.create_text(100,10,fill=PAUSE_TITLE,font="Times 20 bold",text="Paused",anchor="n")
    Button(pausemenu,text="Resume",command=resume).place(x=100, y=40, anchor="n")

def backmenu():
    global pausemenu,canvas
    pausemenu.destroy()
    canvas.focus_set()
    if(gameOver == False):
        save()
    menu()

def nextlevel():
    global pausemenu, canvas
    pausemenu.destroy()
    canvas.focus_set()
    next()

def gameoverMenu():

    print("over menu summoned")
    global overSummon
    overSummon = True
    # Get the leaderboard from the file
    leaderboard_in = open("leaderboard.txt", "r")
    boardData_str = leaderboard_in.read()
    boardData_str = boardData_str.split("\n")
    boardData = []
    for tmp in boardData_str:
        tmp = tmp.split(" ")
        if(len(tmp)==2):
            print(tmp)
            boardData.append([tmp[0],int(tmp[1])])
    # print("boardData read in as")
    # print(boardData)
    # Update the leaderboard
    for i in range(len(boardData)):
        # print("comparing")
        # print(boardData[i][1])
        if(boardData[i][1] <= levelNumber ):
            boardData.insert(i,[name,levelNumber])
            break
    # print("updated as")
    # print(boardData)
    # Store the leaderboard in a list
    leaderboard_out = open("leaderboard.txt","w")
    for i in range(len(boardData)):
        leaderboard_out.write(boardData[i][0]+" "+str(boardData[i][1])+"\n")
    leaderboard_in.close()
    leaderboard_out.close()

    # Show the leaderboard
    global pausemenu
    pausemenu = Canvas(window, width=200, height=400, bg=PAUSE)
    pausemenu.place(x=width/2,y=50, anchor="n")
    pausemenu.focus_set()
    pausemenu.create_text(100,10,fill=GAMEOVER_TITLE,font="Times 20 bold",text="Oh no",anchor="n")
    for i in range(5):
        pausemenu.create_text(100, i*20+50, fill=LEADERBOARD_NAME, font="Times 10 bold",text=str(i+1)+". "+boardData[i][0]+" : "+str(boardData[i][1]), anchor = "n")

    Button(pausemenu,text="Back to main",command=backmenu).place(x=100, y=250, anchor="n")

def gamewinMenu():
    global pausemenu, menu
    pausemenu = Canvas(window, width=200, height=400, bg=PAUSE)
    pausemenu.place(x=width/2,y=50, anchor="n")
    pausemenu.focus_set()
    pausemenu.create_text(100,10,fill=WIN_TITLE,font="Times 20 bold",text="Congradulation",anchor="n")
    Button(pausemenu,text="Save and Back to main",command=backmenu).place(x=100, y=40, anchor="n")
    Button(pausemenu,text="Next Level",command=nextlevel).place(x=100, y=80, anchor="n")

def overlap(a, b):
    #print("comparing",a,b)
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False

def gameloop():
    global canvas, playerPos
    playerPos = canvas.coords(player)
    #print(playerPos)
    #print(spikePos)
    global win, gameOver
    if(overlap(goalPos, playerPos) and win == False):
        win = True
        gamewinMenu()
    for i in spikePos:
        if(overlap(i,playerPos) and cheatactive==False ):
            print("game is over")
            gameOver = True

    if(gameOver == False):
        window.after(90, gameloop)
    else:
        if(overSummon == False):
            gameoverMenu()

def level():
    # draw the map
    global canvas,spikePos
    canvas.delete("all")
    spikePos.clear()
    canvas.create_text(400,2,fill="red",font="Times 20 italic bold",text="Level "+str(levelNumber),anchor="n")
    canvas.create_rectangle(goalPos[0], goalPos[1], goalPos[2], goalPos[3], fill=GOAL)
    n = 10
    while(n > 0):
        if(put_spike()):
            #print("putting")
            n -= 1
    global pauseButton
    pauseButton = Button(
    canvas,
    text="pause",
    command=pause)
    pauseButton.place(x=width-80,y=5)
    global player
    player = canvas.create_rectangle(playerPos[0], playerPos[1], playerPos[2], playerPos[3], fill=PLAYER)
    canvas.focus_set()
    gameloop()

def start():
    global gameOver,win,overSummon
    gameOver = win = overSummon = False
    global speed, levelNumber
    levelNumber = 0
    speed = levelNumber + 3
    levelNumber += 1
    global playerPos
    playerPos = [width-50, height-50, width-10, height-10]
    global canvas
    canvas.bind(leftKey,left)
    canvas.bind(rightKey,right)
    canvas.bind(upKey,up)
    canvas.bind(downKey,down)
    canvas.focus_set()
    level()

def load():
    global name
    if(name == "nobody"):
        messagebox.showinfo("Confused","You are nobody, please enter a name")
        return
    global gameOver,win,overSummon
    gameOver = win = overSummon = False
    global speed, levelNumber

    # Load levelNum from data.txt
    f = open("data.txt", "r")
    tmp = f.read()
    print("data origin input")
    print(tmp)
    tmp = tmp.split("\n")
    found = False
    for i in range(len(tmp)):
        gamedata = tmp[i].split(" ")
        #print(gamedata)
        if(len(gamedata) != 2):
            continue
        if(gamedata[0] == name):
            found = True
            levelNumber = int(gamedata[1])
            print("read in level Number as ",levelNumber)
            break
    if(found == False):
        messagebox.showinfo("Confused","You don't have a save\nPlease start a new game")
        return
    speed = levelNumber + 3
    levelNumber += 1
    global playerPos
    playerPos = [width-50, height-50, width-10, height-10]

    canvas.bind(leftKey,left)
    canvas.bind(rightKey,right)
    canvas.bind(upKey,up)
    canvas.bind(downKey,down)
    canvas.focus_set()

    level()

def next():
    global gameOver,win,overSummon
    gameOver = win = overSummon = False
    global speed, levelNumber
    speed = levelNumber + 3
    levelNumber += 1
    global playerPos
    playerPos = [width-50, height-50, width-10, height-10]
    canvas.bind(leftKey,left)
    canvas.bind(rightKey,right)
    canvas.bind(upKey,up)
    canvas.bind(downKey,down)
    canvas.focus_set()
    level()

def getname():
    global name,nameEntry
    name=nameEntry.get()
    print(name)

def getupKey():
    global upEntry,upKey
    upKey=upEntry.get()

def getdownKey():
    global downEntry,downKey
    downKey=downEntry.get()

def getrightKey():
    global rightEntry,rightKey
    rightKey=rightEntry.get()

def getleftKey():
    global leftEntry,leftKey
    leftKey=leftEntry.get()

def backfromset():
    global settings,canvas
    settings.destroy()
    canvas.bind(leftKey,left)
    canvas.bind(rightKey,right)
    canvas.bind(upKey,up)
    canvas.bind(downKey,down)
    canvas.focus_set()

def setKey():
    global upKey,downKey,leftKey,rightKey,settings
    settings = Canvas(canvas,width=400,height=200,bg=SETTING_BG)
    settings.place(x=width/2,y=50,anchor="n")
    settings.create_text(200,5,text="Settings",fill=PAUSE_TITLE,anchor="n")
    settings.focus_set()

    global upEntry
    upEntry = Entry(settings)
    settings.create_window(200, 50, width=60, height=20, window=upEntry,anchor="n")
    getupButton = Button(text="upOk",command=getupKey)
    settings.create_window(200, 70, width=60, height=20,window=getupButton,anchor="n")
    global downEntry
    downEntry = Entry(settings)
    settings.create_window(200, 100, width=60, height=20, window= downEntry, anchor="n")
    getdownButton = Button(text="downOk",command=getdownKey)
    settings.create_window(200, 120, width=60, height=20,window=getdownButton,anchor="n")
    global rightEntry
    rightEntry = Entry(settings)
    settings.create_window(300, 100, width=60, height=20, window=rightEntry, anchor="n")
    getrightButton = Button(text="rightOk",command=getrightKey)
    settings.create_window(300, 120, width=60, height=20, window=getrightButton,anchor="n")
    global leftEntry
    leftEntry = Entry(settings)
    settings.create_window(100, 100, width=60, height=20, window=leftEntry,anchor="n")
    getleftButton = Button(text="leftOk",command=getleftKey)
    settings.create_window(100, 120, width=60, height=20, window=getleftButton,anchor="n")

    Button(
    settings,
    text="Back",
    command=backfromset
    ).place(x=200,y=170,anchor="n")

def menu():
    # draw the menu
    global canvas
    canvas.delete("all")
    titleImage = PhotoImage(file="title.png")
    global window
    window.titleImage = titleImage
    canvas.create_image(width/2,height/2,image=window.titleImage)
    canvas.pack()

    global name
    global nameEntry
    nameEntry = Entry (window)
    canvas.create_window(width/2, 10, width=100, height=20, window=nameEntry, anchor="n")

    nameButton = Button(text="nameOk",command=getname)
    canvas.create_window(width/2, 40, width=70, height=20, window=nameButton, anchor= "n")

    # Start Button
    global startButton
    startButton = Button(
    canvas,
    text="Start",
    command=start)
    startButton.place(x=0,y=2)

    # Save Button
    global saveButton
    saveButton = Button(
    canvas,
    text="Save",
    command=save)
    saveButton.place(x=80,y=2)

    # Load Button
    global loadButton
    loadButton = Button(
    canvas,
    text="Load",
    command=load)
    loadButton.place(x=160,y=2)

    global setButton
    setButton = Button(
    canvas,
    text="Settings",
    command=setKey
    )
    setButton.place(x=240,y=2)
menu()

window.mainloop()
