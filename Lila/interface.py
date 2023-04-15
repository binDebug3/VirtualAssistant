import speech_recognition as sr
import pyttsx3

import logging
import datetime
import random

from Lila import config
from Lila.features import date_time, gui


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[config.voice_index].id)

# LISTEN
def mic_input():
    """
    Takes input from the microphone and returns it as a string
    :return: (string) input from the microphone, (boolean) False if failure
    """
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.energy_threshold = 4000
            audio = r.listen(source, timeout=30, phrase_time_limit=20)

        try:
            print("Recognizing...")
            command = r.recognize_google(audio, language='en-in').lower()
            print(f"User said: {command}\n")
        except:
            print("Say that again please...")
            command = mic_input()
        return command
    except Exception as ex:
        print(ex)
        return False

# SPEAK
def tts(text):
    """
    Text to speech function
    :param text: (string) text to be spoken
    :return: (boolean) True if successful, False if failure
    """
    try:
        engine.say(text)
        engine.runAndWait()
        engine.setProperty('rate', 175)
        return True
    except Exception as ex:
        print("Error in tts function")
        print(ex)
        return False


# choose output style
def speak(text):
    if config.INTERACTION == "silent" or config.INTERACTION == "terminal":
        print("Reply:", text)
    else:
        tts(text)

# choose output style
def output(text, level, msg=""):
    if config.INTERACTION == "silent" or config.INTERACTION == "terminal":
        print("Reply:", text)
    else:
        tts(text)
        print(text)

    if msg != "":
        msg = ". Note+ " + msg

    if level == "info":
        logging.info("Action: " + text + msg)
    else:
        logging.error("Action: " + text + msg)


def startup():
    if not config.skip:
        speak("Initializing Lila")
        speak("Importing preferences and calibrating virtual environment")
        speak("I've prepared a safety briefing for you to entirely ignore")
        speak("I have indeed been uploaded sir")
        speak("We're online and ready")

    wish()

# starting interaction 
def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

    speak(f"It is {date_time.time()}")
    speak("How can I help you today?")
    logging.info("Startup complete")

def greetings():
    speak(random.choice(config.GREETINGS_RES))


# choose to proceed
def check_command(command):
    if not command:
        return False

    if config.INTERACTION in ["silent", "earbud", "terminal"]:
        proceed = True
    else:
        proceed = any([x in command for x in config.speech_impediment])
        
    return proceed

# get command
def get_command():
    if config.INTERACTION in ["silent", "earbud"]:
        command = gui.input_window("Command").lower()
    elif config.INTERACTION == "press":
        gui.input_window("Press enter to speak: ")
        print("One moment please...")
        command = mic_input()
    elif config.INTERACTION == "terminal":
        command = input("Command: ").lower()
    else:
        command = mic_input()
    logging.info("User said: " + command)

    return command, command.split(' ', 2)[-1]

