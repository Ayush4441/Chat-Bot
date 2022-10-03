from threading import *
import os
from time import sleep

def Load():
    star = ["*","*","*","*","*","*","*","*","*","*","*"]
    mess = ("i","n","i","t","i","a","l","i","z","e","d")

    sleep(0.1)
    os.system('cls')
    c = 0
    for c in range(len(mess)):
        star[c] = mess[c]
        print("Module ", end = '') 
        t = 0
        for t in range(len(star)):
            print(star[t], end = "")
            sleep(0.1)
            t += 1

        sleep(0.2)
        os.system('cls')
        c += 1

Load()
    
    
LoadScreen = Thread(Load())
#LoadScreen.start()

import nltk
from nltk.stem import WordNetLemmatizer

import pickle
import numpy as np

from keras.models import load_model

import json
import random

lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

#LoadScreen.join()

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
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
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

#Creating Terminal Application

delay = 100
UserLog = [""]
BotLog = [""]

Commands = ("Esc", "Help")

def Command(text):
    if text == Commands[1]:
        Help()

def Help():
    print(Commands)

def Intro():
    print("Bot: Hello a Chat Bot")
    print("Bot: How may I help you? \n")
    

def Send(text):
    UserLog.insert(text)
    Write()

def Prosses():
    pass

def Replay():
    pass

def Read():
    IOU = input()
    if IOU != "":
        Send()

def Write():
    system("cls")
    for i in UserLog:
        print(i)



Intro()
Read()