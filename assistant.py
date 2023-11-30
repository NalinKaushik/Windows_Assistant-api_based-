import speech_recognition as sr
import os
import webbrowser
import openai
from openai import OpenAI
from config import apikey
import datetime
import random
import numpy as np
import pyttsx3
import pywhatkit as kt

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    # openai.api_key = apikey
    chatStr += f"Nalin: {query}\n Jarvis: "
    client = OpenAI(api_key = apikey)
    response = client.completions.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response.choices[0].text)
    chatStr += f"{response.choices[0].text}\n"
    return response.choices[0].text


def say(audio):
	
	engine = pyttsx3.init()
	# getter method(gets the current value
	# of engine property)
	voices = engine.getProperty('voices')
	
	# setter method .[0]=male voice and 
	# [1]=female voice in set Property.
	engine.setProperty('voice', voices[0].id)
	
	# Method for the speaking of the assistant
	engine.say(audio) 
	
	# Blocks while processing all the currently
	# queued commands
	engine.runAndWait()




def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    client = OpenAI(api_key = apikey)
    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response.choices[0].text
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

# def say(text):
#     os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Good morning sir!")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        web = query.replace("open","")
        web = query.replace("on browser","")
        website = "open"+web+"on browser"
        if website.lower() in  query.lower():
            try:
                kt.search(web)
            except:
                say("Due to some network error i am not able to perform that task")
        # todo: Add a feature to play a specific song
        # if "open music" in query:
        #     musicPath = "C:\Users\Asus\Videos\Dynamite.mp3"
        #     os.system(f"open {musicPath}")

        if "the time" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")

       

        # elif "open pass".lower() in query.lower():
        #     os.system(f"open /Applications/Passky.app")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis exit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""
        if "on youtube".lower() in query.lower() :
            try:
                song = query.replace("on youtube","")
                song = song.replace("play","")
                say("playing"+song+"on youtube ")
                kt.playonyt(song)
            except:
                say("Due to some network error i am not able to perform that task")
        else:
            print("Chatting...")
            chat(query)





        # say(query)