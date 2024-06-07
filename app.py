import streamlit as st
import speech_recognition as sr
import os
from gtts import gTTS
import playsound
from time import ctime
import re
import webbrowser
import smtplib

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write('Bujji: I am listening...')
        audio = r.listen(source, phrase_time_limit=5)
    data = ""
    try:
        data = r.recognize_google(audio, language='en-US')
        st.write("You said: " + data)
    except sr.UnknownValueError:
        st.write("Bujji: I cannot hear you")
    except sr.RequestError as e:
        st.write("Request failed")
    return data

def respond(string):
    st.write(string)
    tts = gTTS(text=string, lang='en')
    tts.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")

def voice_assistant(data):
    if "how are you" in data:
        respond("I am doing fine here")
    elif "time" in data:
        respond(ctime())
    elif "open google" in data.casefold():
        reg_ex = re.search('open google(.*)', data)
        url = 'https://www.google.com/'
        if reg_ex:
            sub = reg_ex.group(1)
            url = url + 'r/'
        webbrowser.open(url)
        respond('Done')
    elif "send mail" in data:
        respond("Whom should I send email to?")
        to = listen()
        edict = {"hello": "tirumalasettignanamanjula29@gmail.com"}
        toaddr = edict.get(to, None)
        if toaddr:
            respond("What is the subject?")
            Subject = listen()
            respond("What should I tell the person?")
            message = listen()
            content = f'Subject: {Subject}\n\n{message}'
            # Initialize gmail smtp
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            # Login
            mail.login('kanakamanand333@gmail.com', 'awoqybikcmbvdgax')
            mail.sendmail('kanakamanand333@gmail.com', toaddr, content)
            mail.close()
            respond('Email sent')
        else:
            respond("I don't have the email address for that contact.")
    else:
        respond("I didn't understand that command.")

st.title("Voice Assistant")
st.write("Click the button and speak a command")

# Check if the microphone is accessible
mic_access = st.checkbox("Use Microphone")

if mic_access:
    if st.button('Speak'):
        data = listen()
        if data:
            voice_assistant(data)
else:
    command = st.text_input("Or type your command here:")
    if command:
        voice_assistant(command)


