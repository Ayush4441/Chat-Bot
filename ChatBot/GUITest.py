# Importing tkinter module
import tkinter
from tkinter import *
from tkinter.ttk import *
from time import sleep

#Screen Settings
ScreenX = 800
ScreenY = 600
ScreenSize = str(ScreenX) + "x" + str(ScreenY)

#Text Format
Font = ("Arial",12,'bold')
bd = 0
bg = "White"

i = 0
UserText = ""
BotText = ""

StartUp = Tk()
StartUp.geometry("800x400")

StartUp.eval('tk::PlaceWindow . center')
StartUp.overrideredirect(True)

progress = Progressbar(StartUp, orient = HORIZONTAL, length = 100, mode = 'determinate')
progress.pack(side = BOTTOM, fill = BOTH, pady = 10)

SUImage = PhotoImage(file = "jojo-bizarre-adventure.png")
label = Label(StartUp,image = SUImage)
label.pack()

progress["value"] = 59

StartUp.after(2500, StartUp.destroy)
StartUp.mainloop()

def SetScreenSize(Window, Size):
    if Size == 2:
        Window.attributes('-fullscreen', True) #Make it Fullscreen
    elif Size == 1:
         Window.state('zoomed') #Make it maximized
    elif Size == 0:
        Window.minsize(ScreenY, ScreenX) #Make it minimized
    elif Size == -1:
        Window.resizable(width = True, height = True) #Make it Resizable
    elif Size == -2:
        Window.resizable(width = False, height = False) #Make it Non-Resizable

def WriteUI(widget, Text, user, ShiftCursor):
    if Text != '':
        global i
        widget.config(state = NORMAL)
        if i == 0:
            if user == 0:
                widget.insert(END,"You: ")
            elif user == 1:
                widget.insert(END,"Bot: ")
        if i < len(Text):
            if i == len(Text) - 1 and ShiftCursor == True:
                widget.insert(END, Text[i] + "\n")
            else:
                widget.insert(END, Text[i])
            widget.pack()
            #print(UserText[i], end = "")
            i += 1
            if user == 0:
                UI.after(250, UserInput)
            elif user == 0:
                UI.after(250, WriteUI)
        else:
            widget.config(state = DISABLED)
            Log.yview(END)
            #if ShiftCursor == True:
                #print("")
            i = 0
            return

def Send():
    global UserText
    UserText = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    UserInput()

UI = Tk()
UI.title("GUI Test")
frame = Frame(UI)
frame.pack(fill = BOTH, expand = True)

UI.geometry(ScreenSize)
SetScreenSize(UI, -2)
    

UserInput = lambda : WriteUI(Log, UserText, 0, True)
BotInput  = lambda : WriteUI(Log, BotText,  1, True)

Log = Text(frame)
scrollbar = Scrollbar(frame, command = Log.yview)

#Bind scrollbar to Chat window
scrollbar.config(command = Log.yview)
scrollbar.pack(side = RIGHT, fill = Y)

#Creating Chat Log
Log.pack(side = TOP, fill = BOTH, expand = True, padx = 10, pady = 10)
Log.config(state = DISABLED, yscrollcommand = scrollbar.set)

#Create the box to enter message
EntryBox = Text(frame)
EntryBox.pack(side = LEFT, expand = True, fill = X, padx = 10, pady = 10)

#Create Button to send message
SendButton = Button(frame, text = "Send", command = Send).pack(side = RIGHT, expand = True, fill = BOTH, padx = 10, pady = 10)

UI.mainloop()
