#UI Stuff
import tkinter
from tkinter import *
from tkinter.ttk import *
import threading

model = 0
words = 0
intents = 0
rand = 0
np = 0
lemmatizer = 0
classes = 0
nlp = 0

#Start up Screen
#Bacaly a Loading Up Screen
StartUp = Tk()
StartUp.geometry("800x400")

StartUp.eval('tk::PlaceWindow . center')
StartUp.overrideredirect(True)

progress = Progressbar(StartUp, orient = HORIZONTAL, length = 100, mode = 'determinate')
progress.pack(side = BOTTOM, fill = BOTH, pady = 10)

#Just a Place Holder Image (Cause i don't have suitable Image right now)
SUImage = PhotoImage(file = "jojo-bizarre-adventure.png")
#Properbly a Suitable Image
#SUImage = PhotoImage(file = "PyChatBot.png")
label = Label(StartUp, image = SUImage)
label.pack()

#Importing Packages
def Import():
    print("Loading Started")
    global model, words, intents, rand, np, nlp, classes, lemmatizer
    #Chat Bot Stuff
    progress["value"] = 0
    import nltk as nlp
    progress["value"] = 10
    from nltk.stem import WordNetLemmatizer
    progress["value"] = 20
    lemmatizer = WordNetLemmatizer()
    progress["value"] = 25
    import pickle
    progress["value"] = 30
    words = pickle.load(open('words.pkl','rb'))
    progress["value"] = 35
    classes = pickle.load(open('classes.pkl','rb'))
    progress["value"] = 40
    import numpy as np
    progress["value"] = 60
    import keras
    progress["value"] = 65
    from keras.models import load_model
    progress["value"] = 70
    model = load_model('chatbot_model.h5')
    progress["value"] = 80
    import json
    progress["value"] = 85
    intents = json.loads(open('intents.json').read())
    progress["value"] = 90
    import random as rand
    progress["value"] = 100

def Check():
    while True:
        if progress["value"] == 100:
            StartUp.destroy()
            break

IM = threading.Thread(target = Import)
CK = threading.Thread(target = Check)
IM.start()
CK.start()
StartUp.mainloop()

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nlp.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = rand.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

#Creating Main Application

#Screen Settings
ScreenX = 800
ScreenY = 600
ScreenSize = str(ScreenX) + "x" + str(ScreenY)

UserText = ""
BotText = ""

Delay = 250
toExit = False

index = 0

def Intro():
    global BotText
    BotText = "Hello"
    BotInput()

def Process(message):
    global BotText
    if message.casefold() == "exit":
        Exit()
    BotText = chatbot_response(message)
    if BotText != "":
        BotInput()

def Exit():
    toExit = True
    sys.exit()

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
        global index
        widget.config(state = NORMAL)
        if index < len(Text):
            if index == 0:
                if user == 0:
                    widget.insert(END,"You: ")
                elif user == 1:
                    widget.insert(END,"Bot: ")
            if index == len(Text) - 1 and ShiftCursor == True:
                widget.insert(END, Text[index] + "\n")
                print(Text)
            else:
                widget.insert(END, Text[index])
            widget.pack()
            index += 1
            if user == 0:
                UI.after(Delay, UserInput)
            elif user == 1:
                UI.after(Delay, BotInput)
        else:
            widget.config(state = DISABLED)
            Log.yview(END)
            index = 0
            return
    else:
        print("No Text")

def Send():
    global UserText
    UserText = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if UserText != "":
        UserInput()
        Process(UserText)

UI = Tk()
UI.title("GUI Test")
frame = Frame(UI)
frame.pack(fill = BOTH, expand = True)

UI.geometry(ScreenSize)
SetScreenSize(UI, -2)
    
Log = Text(frame)
scrollbar = Scrollbar(frame, command = Log.yview)

UserInput = lambda : WriteUI(Log, UserText, 0, True)
BotInput  = lambda : WriteUI(Log, BotText,  1, True)

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

Intro()
UI.mainloop()
