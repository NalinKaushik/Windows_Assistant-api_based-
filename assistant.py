import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import pyttsx3
import pywhatkit as kt

# Initialize chat history
chatStr = ""

# Text-to-Speech
def say(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # [0] for male, [1] for female
    engine.say(audio)
    engine.runAndWait()

# Chat with GPT
def chat(query):
    global chatStr
    chatStr += f"Nalin: {query}\nJarvis: "
    try:
        openai.api_key = apikey
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response.choices[0].text.strip()
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        say("There was an error connecting to OpenAI.")
        print("OpenAI Error:", e)

# One-time AI prompt handler
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n\n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response.choices[0].text.strip()
        text += reply

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        # Safe filename using first 5 words
        filename = "_".join(prompt.split()[:5]) + ".txt"
        with open(f"Openai/{filename}", "w") as f:
            f.write(text)

        say("The result has been saved.")
    except Exception as e:
        say("Failed to generate AI response.")
        print("AI Error:", e)

# Voice recognition
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Recognition Error:", e)
            say("Sorry, I didn't catch that.")
            return None

# Main Program
if __name__ == '__main__':
    say("Good morning, Sir.")
    print("Welcome to Jarvis A.I")

    try:
        while True:
            query = takeCommand()
            if not query:
                continue
            query = query.lower()

            # Handle website opening
            if "open" in query and "on browser" in query:
                site_name = query.replace("open", "").replace("on browser", "").strip()
                say(f"Opening {site_name} on your browser.")
                try:
                    kt.search(site_name)
                except:
                    say("Sorry, I couldn't connect to the internet.")

            # Play on YouTube
            elif "play" in query and "on youtube" in query:
                song = query.replace("play", "").replace("on youtube", "").strip()
                say(f"Playing {song} on YouTube.")
                try:
                    kt.playonyt(song)
                except:
                    say("Unable to play due to a network issue.")

            # Tell the time
            elif "the time" in query:
                now = datetime.datetime.now()
                hour = now.strftime("%H")
                minute = now.strftime("%M")
                say(f"Sir, the time is {hour} hours and {minute} minutes.")

            # Run one-time AI prompt
            elif "using artificial intelligence" in query:
                ai(prompt=query)

            # Exit
            elif "jarvis exit" in query or "exit" in query:
                say("Goodbye, sir.")
                break

            # Reset chat history
            elif "reset chat" in query:
                chatStr = ""
                say("Chat history has been reset.")

            # Otherwise, use GPT chat
            else:
                print("Chatting...")
                chat(query)

    except KeyboardInterrupt:
        say("Shutting down. Goodbye!")
