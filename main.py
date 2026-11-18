
import site
from pydoc import text

import speech_recognition as sr
import os
import pyttsx3
from pyttsx3 import engine
from pywin.Demos.ocx import webbrowser
import webbrowser
import openai
from config import apikey
import random
from frontend import *


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n ************************ \n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # todo: Wrap this inside the try catch block
   #print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    #with open(f"Openai/prompt- {random.randint()}", "w") as f:
    with open(f"Openai/{prompt[0:30]}.txt", "w") as f:
        f.write(text)


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Sorry, Error Occured."



if __name__ == '__main__':
    print('PyCharm')
    say("Welcome, how can I help you?... ")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["facebook", "https://www.facebook.com"], ["instagram", "https://www.instagram.com"], ["spotify", "https://www.open.spotify.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} ....")
                webbrowser.open(site[1])

            if "the time" in query:
                hour = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"The time is {hour}.")

            if "using ai".lower() in query.lower():
                ai(prompt=query)