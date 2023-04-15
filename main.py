import ctypes
import webbrowser

from Lila import NavaniAssistant
import os
import random
import datetime
import requests
import sys
import pyjokes
import time
import pyautogui as gui
import pywhatkit
import wolframalpha
from PIL import Image
import logging
# from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtCore import QTimer, QTime, QDate, Qt
# from PyQt5.QtGui import QMovie
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUiType
# from Lila.features.gui import Ui_MainWindow
from Lila import config
import utils

nav = NavaniAssistant()

# ================================ MEMORY ==============================================================================

GREETINGS = ["hey lila", "hello lila", "wake up lila", "you there lila", "time to work lila",
             "ok lila", "are you there", "wake up daddy's home", "lila are you up", "hello", "hi lila"]
GREETINGS_RES = ["always there for you sir", "i am ready sir", "for you sir, I'm always ready", "at your service sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir", "oh hello sir"]

EMAIL_DIC = {
    'myself': 'dallinpstewart@gmail.com',
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]

app_id = config.wolframalpha_id


# ======================================================================================================================


def speak(text):
    if config.INTERACTION == "silent":
        print("Reply:", text)
    else:
        nav.tts(text)


def output(text, level, msg=None):
    if config.INTERACTION == "silent":
        print("Reply:", text)
    else:
        nav.tts(text)
        print(text)

    if msg is None:
        msg = text
    if level == "info":
        logging.info(msg + text)
    else:
        logging.error(msg + text)


# this should be in features.py
def compute_math(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except Exception as ex:
        print(ex)
        output("Sorry sir I couldn't solve that problem. Please try again.", "error")
        return None


def startup():
    if not config.skip:
        speak("Initializing Lila")
        speak("Importing preferences and calibrating virtual environment")
        speak("I've prepared a safety briefing for you to entirely ignore")
        speak("I have indeed been uploaded sir")
        speak("We're online and ready")

    wish()


def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

    speak(f"It is {nav.tell_time()}")
    speak("How can I help you today?")
    logging.info("Startup complete")


class MainThread:
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        # Set up the logging configuration
        logging.basicConfig(filename=config.log, level=logging.INFO,
                            format='%(asctime)s & %(levelname)s & %(message)s')

        self.TaskExecution()

    def TaskExecution(self):
        startup()

        while True:
            if config.INTERACTION in ["silent", "earbud"]:
                command = input("Command: ").lower()
            elif config.INTERACTION == "press":
                input("Press enter to speak: ")
                print("One moment please...")
                command = nav.mic_input()
            else:
                command = nav.mic_input()
            logging.info("User said: " + command)

            if not command:
                continue
            interest = command.split(' ', 2)[-1]
            post_interest = command.split(' ', 2)[-1]

            speech_impediment = ["lila", "milo", "leila", "layla",
                                 "tyler", "liner", "myla", "leather", "lima", "wireless",
                                 "weather", "leather", "mama"]
            if config.INTERACTION in ["silent", "earbud"]:
                proceed = True
            else:
                proceed = any([x in command for x in speech_impediment])
            if proceed:

                # TELL THE DATE
                if "date" in command or "day is" in command:
                    date = nav.tell_date()
                    output(date, "info", msg="Action: ")

                # TELL THE TIME
                elif "time" in command:
                    local_time = nav.tell_time()
                    output(local_time, "info", msg="Action: ")

                # OPEN APPLICATION
                elif "launch" in command or "open" in command:
                    app = "Not found"
                    try:
                        for key in config.dict_app.keys():
                            if key in post_interest:
                                app = key
                                break
                        path = config.dict_app[app]

                        if path is None:
                            output("Sorry sir, I don't know that application: " + app, "error", msg="Action: ")
                        else:
                            speak(f"Launching {app} for you sir")
                            success = nav.launch_app(path)
                            if success:
                                logging.info("Action: Opened " + app + " for the user")
                            else:
                                raise Exception("Failed to open application")

                    except Exception as ex:
                        output("Sorry sir, I ran into an error with that application: " + app, "error", msg="Action: ")
                        print(ex)


                elif "run" in command:
                    dict_program = config.dict_program
                    try:
                        project = "Not found"
                        print(post_interest)
                        for key in dict_program.keys():
                            if key in post_interest:
                                project = key
                                break
                        path = dict_program[project]

                        if path is None:
                            output("Sorry sir, I don't know that program: " + project, "error", msg="Action: ")
                        else:
                            speak(f"Launching {project} for you sir")
                            success = nav.run_program(path[0], path[1])
                            if success:
                                logging.info("Action: Opened " + project + " for the user")
                            else:
                                raise Exception("Failed to open application")

                    except Exception as ex:
                        output("Sorry sir, I ran into an error with that program: " + project, "error", msg="Action: ")
                        print(ex)

                # PUSH CODE
                elif "push" in command:
                    # valid = ["1", "2", "casper", "dashboard", "blog"]

                    try:
                        # if valid not in command:
                        #     raise Exception("Invalid project")

                        if post_interest.isdigit():
                            directory = "volume " + post_interest

                        # ask for a commit message
                        if config.INTERACTION in ["silent", "earbud"]:
                            commit_message = input("Commit message: ")
                        else:
                            speak("What is the commit message?")
                            commit_message = nav.mic_input()

                        speak(f"Pushing code for you sir")
                        success = nav.push_code(directory, commit_message)

                        if success:
                            output(f"Code for {directory} pushed successfully", "info", msg="Action: ")
                        else:
                            raise Exception("Failed to push code")

                    except Exception as ex:
                        output("Sorry sir, I ran into an error with pushing code", "error", msg="Action: ")
                        print(ex)

                # SAY GREETING
                elif command in GREETINGS:
                    speak(random.choice(GREETINGS_RES))
                    logging.info("Action: Greeted the user")

                # OPEN WEBSITE
                elif "go to" in command:
                    domain = interest
                    open_result = nav.open_website(domain)
                    if open_result is None:
                        output("Sorry sir, I couldn't open that website: " + domain, "error", msg="Action: ")
                    else:
                        output("Opening " + domain, "info", msg="Action: ")

                # TELL THE WEATHER
                elif "weather" in command:
                    city = interest
                    weather_result = nav.weather(city=city)
                    output(weather_result, "info", msg="Action: ")

                # SEARCH WIKIPEDIA
                elif "tell me about" in command:
                    topic = interest
                    if topic:
                        wiki_result = nav.tell_me(topic)
                        if wiki_result:
                            output(wiki_result, "info", msg="Action: ")
                        else:
                            output("Sorry sir, I couldn't find anything on that topic", "error", msg="Action: ")
                    else:
                        output("Sorry sir, I couldn't find anything on that topic", "error", msg="Action: ")

                # SEARCH GOOGLE
                elif "google" in command:
                    try:
                        nav.search_google(command)
                        logging.info("Action: Searched google for " + interest)
                    except Exception as ex:
                        output("Sorry sir, I couldn't find anything on that topic", "error", msg="Action: ")
                        print(ex)

                # SEARCH YOUTUBE
                elif "youtube" in command:
                    video = post_interest
                    output(f"Okay sir, playing {video} on youtube", "info", msg="Action: ")
                    pywhatkit.playonyt(video)

                elif "piano" in command:
                    # randomly choose one of two urls
                    playlist = random.choice(["https://www.youtube.com/watch?v=ddO7faOdu1k",
                                              "https://www.youtube.com/watch?v=TXmWlUj5b3A"])
                    webbrowser.open(playlist)

                    # Wait for the page to load
                    time.sleep(12)

                    # Minimize the window using gui
                    gui.keyDown('altleft')
                    gui.keyDown('space')
                    gui.keyDown('n')
                    gui.keyUp('altleft')
                    gui.keyUp('space')
                    gui.keyUp('n')


                # SEND EMAIL
                elif "send an email" in command:
                    sender_email = config.email
                    sender_password = config.email_password

                    try:
                        speak("Who should I send the email to?")
                        recipient = nav.mic_input()
                        rec_email = EMAIL_DIC[recipient]

                        if rec_email:
                            speak("What is the title?")
                            subject = nav.mic_input()
                            speak("What should I say?")
                            message = nav.mic_input()
                            msg = "Subject: {}\n\n{}".format(subject, message)

                            success = nav.send_email(sender_email, sender_password, rec_email, msg)
                            if success:
                                speak("Email sent successfully")
                                time.sleep(1)
                                logging.info("Action: Sent an email to " + recipient)
                            else:
                                raise Exception("Email not sent")

                        else:
                            speak("Sorry sir, I couldn't find that email address")
                            logging.error("Action: Tried to send an email to a recipient that doesn't exist")

                    except Exception as ex:
                        print("Error sending email")
                        print(ex)
                        speak("Sorry sir, I couldn't send that email")
                        logging.error("Action: Tried to send an email to a recipient that doesn't exist")

                # DO MATH
                elif "calculate" in command:
                    question = command
                    answer = compute_math(question)
                    speak(answer)
                    logging.info("Action: Calculated " + question)

                # USE GOOGLE CALENDAR
                elif "calendar" in command:
                    nav.calendar(command)
                    logging.info("Action: Used the calendar")

                elif "close notes" in command:
                    speak("Okay sir, closing notes")
                    os.system("TASKKILL /F /IM notepad.exe")
                    logging.info("Action: Closed notes")

                # TAKE NOTES
                elif "note" in command or "write" in command:
                    speak("What should I write down?")
                    if config.INTERACTION in ["silent", "earbud"]:
                        note = input("Write here: ")
                    else:
                        note = nav.mic_input()
                    nav.take_note(note)
                    speak("I've made a note of that sir")
                    logging.info("Action: Took a note")

                # GET TO DO LIST
                elif "to-do" in command or "to do" in command:
                    speak("Here is your to-do list")
                    quehaceres = nav.get_todo(post_interest.split()[-1])
                    output(quehaceres, "info", msg="Action: ")

                # TELL JOKES
                elif "joke" in command:
                    joke = pyjokes.get_joke()
                    print(joke)
                    speak(joke)
                    logging.info("Action: Told a joke")

                # SHOW SYSTEM INFO
                elif "system info" in command:
                    info = nav.system_info()
                    print(info)
                    speak(info)
                    logging.info("Action: Told the system info")

                # USE MAPS
                elif "where is" in command:
                    place = command.split("where is", 1)[1]
                    current, target, distance = nav.find_location(place)
                    city = target.get("city", " ")
                    state = target.get("state", " ")
                    country = target.get("country", " ")
                    time.sleep(1)

                    try:
                        if city:
                            result = f"{place} is in {city}, {state}, {country}. " \
                                     f"It is {distance} miles away from {current}"
                        else:
                            result = f"{place} is in {state}, {country}. It is {distance} miles away from {current}"
                        output(result, "info", msg="Action: ")

                    except Exception as ex:
                        output("Sorry sir, I couldn't find that location", "error", msg="Action: ")
                        print(ex)

                # GET IP ADDRESS
                elif "ip address" in command:
                    ip = requests.get("https://api.ipify.org").text
                    output(f"Your IP address is {ip}", "info", msg="Action: ")

                # CHANGE TABS
                elif "switch window" in command:
                    speak("Okay sir, switching windows")
                    nav.switch_window()
                    logging.info("Action: Switched window")

                # LOCK COMPUTER
                elif "lock computer" in command:
                    speak("Okay sir, locking computer")
                    ctypes.windll.user32.LockWorkStation()
                    logging.info("Action: Locked computer")

                # TAKE SCREENSHOTS
                elif "screenshot" in command:
                    speak("What should I call this screenshot sir?")
                    if config.INTERACTION in ["silent", "earbud"]:
                        title = input("Title: ")
                    else:
                        title = nav.mic_input()
                    image_path = os.path.join(config.image_path, title)

                    speak("Okay sir, taking screenshot")
                    screenshot = gui.screenshot()
                    screenshot.save(f"{image_path}.png")

                    output("Screenshot saved successfully", "info", msg="Action: ")

                elif "image" in command:
                    image_path = os.path.join(config.image_path,
                                              post_interest + ".png")
                    try:
                        img = Image.open(image_path)
                        speak("Okay sir, showing screenshot")
                        img.show()
                        time.sleep(2)
                        logging.info("Action: Showed a screenshot")

                    except IOError as ex:
                        output("Sorry sir, I couldn't find that screenshot", "error", msg="Action: ")
                        print(ex)

                # ANSWER QUESTIONS
                elif "what is" in command or "who is" in command:
                    question = command
                    answer = compute_math(question)
                    speak(answer)
                    logging.info("Action: Answered " + question)

                # START OF DAY
                elif "start my day" in command:
                    speak("Okay sir, let's get our day started.")

                    # describe the weather
                    weather_result = nav.weather(city="Provo")
                    output(weather_result, "info", msg="Action: ")

                    # recite today's to do list
                    speak("Here is your to-do list")
                    quehaceres = nav.get_todo("today")
                    speak(quehaceres)
                    logging.info("Action: Got the to-do list")

                    # check battery
                    battery = nav.battery_level()
                    if battery < 50:
                        output("Your battery is low. Please plug in your computer.", "warning", msg="Action: ")




                elif "what can you do" in command:
                    speak("Right now, I can: "
                          "tell the date, "
                          "tell the time, "
                          "tell you the weather, "
                          "describe system info, "
                          "tell the user's IP address, "
                          "switch windows, "
                          "take notes, "
                          "take screenshots, "
                          "tell jokes, "
                          "tell you your to-do list, "
                          "search wikipedia, "
                          "open youtube videos, "
                          "play background music, "
                          "search google, and "
                          "open apps like slack and v s code, "
                          )
                    logging.info("Action: Told the user what the Lila can do")

                elif "development" in command:
                    speak("Right now, the features still in development are: "
                          "sending emails, "
                          "using google calendar, "
                          "pushing and pulling code, "
                          "running other programs like Ava and Casper, "
                          "interactive chats, "
                          "and of course, incorporating chat gpt"
                          )

                elif "keyword" in command:
                    speak("Here is what I listen for in your commands: "
                          "Lila will tell me to listen for a command, "
                          "time, "
                          "date, "
                          "launch or open for running apps, "
                          "run for running other programs, "
                          "push, "
                          "go to for opening websites, "
                          "weather, "
                          "tell me about for wikipedia, "
                          "google for searching google, "
                          "youtube, "
                          "piano for playing background music, "
                          "send an email, "
                          "calculate, what is, or who is for wolfram alpha, "
                          "note and close notes for note taking, "
                          "joke, "
                          "system info, "
                          "where is for maps, "
                          "ip address, "
                          "switch window, "
                          "lock computer, "
                          "screenshot, "
                          "image for opening an image, "
                          "start my day, "
                          "what can you do to learn about my functionality, "
                          "development to learn about my future features, "
                          "silent mode, "
                          "voice mode, "
                          "power down, and "
                          "keyword to learn about my keywords, "
                          )

                # SWITCH INPUT MODE
                elif "silent mode" in command:
                    speak("Okay")
                    config.INTERACTION = "silent"
                    speak("Okay sir, switching to silent mode")
                    logging.info("Action: Switched to silent mode")

                elif "voice mode" in command:
                    config.INTERACTION = "voice"
                    speak("Okay sir, switching to voice mode")
                    logging.info("Action: Switched to voice mode")

                elif "earbud mode" in command:
                    config.INTERACTION = "earbud"
                    speak("Okay sir, switching to earbud mode")
                    logging.info("Action: Switched to earbud mode")

                elif "press mode" in command:
                    config.INTERACTION = "press"
                    speak("Okay sir, switching to press to speak mode")
                    logging.info("Action: Switched to press to speak mode")

                elif "power down" in command:
                    speak("Okay sir, powering down")
                    logging.info("Action: Powered down")
                    utils.save_interactions()
                    sys.exit()

                else:
                    logging.error("Action: Command not recognized - " + command)
            if config.INTERACTION not in ["silent", "earbud"]:
                logging.error("Action: No keyword found in command - " + command)


startExecution = MainThread()
startExecution.run()


# nlp
# TODO work on nlp part
# TODO make more nlp data

# debugging
# TODO get other programs working

# APIs
# TODO learn about wolfram alpha
# TODO get google calendar working
# TODO get email working

# other
# TODO remove navani class to restructure code
# TODO add a input box for silent and earbud mode