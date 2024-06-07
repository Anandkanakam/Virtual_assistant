import speech_recognition as sr
import os
from gtts import gTTS
import playsound
from time import ctime
import re
from bs4 import BeautifulSoup
import requests
import webbrowser
import smtplib
def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('I am listening')
        audio=r.listen(source,phrase_time_limit=5)
    data=""
    try:
        data=r.recognize_google(audio,language='en-US')
        print("You said : "+data)
    except sr.UnknownValueError:
        print("I cannot hear you")
    except sr.RequestError as e:
        print("Request failed")
    return data
def respond(string):
    print(string)
    tts=gTTS(text=string,lang='en')
    tts.save("nani.mp3")
    playsound.playsound("nani.mp3")
    os.remove("nani.mp3")

def voice_assistant(data):
    if "how are you" in data:
        listening=True
        respond("I am doing fine here")
    if "time" in data:
        listening=True
        respond(ctime())
    if "open google" in data.casefold():
        listening=True
        reg_ex=re.search('open google(.*)',data)
        url='https://www.google.com/'
        if reg_ex:
            sub=reg_ex.group(1)
            url=url+'r/'
        webbrowser.open(url)
        respond('Done')
    if "send mail" in data:
        listening=True
        respond("whom should i send email to?")
        to=listen()
        edict={"hello" : "tirumalasettignanamanjula29@gmail.com"}
        toaddr=edict[to]
        respond("what is the subject")
        Subject=listen()
        respond("what should i tell the person")
        message=listen()
        content='Subject: {}\n\n{}'.format(Subject,message)
        #initialize gmail smtp
        mail=smtplib.SMTP('smtp.gmail.com',587)
        #identify the server
        mail.ehlo()
        mail.starttls()
        #login
        mail.login('kanakamanand333@gmail.com','awoqybikcmbvdgax')
        mail.sendmail('kanakamanand333@gmail.com',toaddr,content)
        mail.close()
        respond('Email sent')
respond("Hello Anand, what can i do for you?")
listening=True
while listening==True:
    data=listen()
    listening=voice_assistant(data)





