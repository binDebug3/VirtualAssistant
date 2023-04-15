from Lila import config, interface
from Lila.features import date_time, launch_app, open_website, weather, send_email, google_calendar, google_search, \
    note, location, wikipedia_search, system, todo_list, youtube, news

import logging


# from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtCore import QTimer, QTime, QDate, Qt
# from PyQt5.QtGui import QMovie
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUiType
# from Lila.features.gui import Ui_MainWindow


class MainThread:
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        # Set up the logging configuration
        logging.basicConfig(filename=config.log, level=logging.INFO,
                            format='%(asctime)s & %(levelname)s & %(message)s')

        interface.startup()

        while True:

            command, interest = interface.get_command()
            proceed = interface.check_command(command)

            if proceed:

                # TELL THE DATE
                if "date" in command or "day is" in command:
                    date = date_time.date()
                    interface.output(date, "info", msg="Action: ")

                # TELL THE TIME
                elif "time" in command:
                    local_time = date_time.time()
                    interface.output(local_time, "info", msg="Action: ")

                # OPEN APPLICATION
                elif "launch" in command or "open" in command:
                    app = "Not found"
                    try:
                        path = launch_app.get_path(interest, "app")

                        if path is None:
                            interface.output("Sorry sir, I don't know that application: " + app,
                                             "error", msg="Action: ")
                        else:
                            interface.speak(f"Launching {app} for you sir")
                            success = launch_app.launch_app(path)

                            if success:
                                logging.info("Action: Opened " + app + " for the user")
                            else:
                                raise Exception("Failed to open application")

                    except Exception as ex:
                        interface.output("Sorry sir, I ran into an error with that application: " + app,
                                         "error", msg="Action: ")
                        print(ex)


                elif "run" in command:
                    project = "Not found"
                    try:
                        path = launch_app.get_path(project, "program")

                        if path is None:
                            interface.output("Sorry sir, I don't know that program: " + project,
                                             "error", msg="Action: ")
                        else:
                            interface.speak(f"Launching {project} for you sir")
                            success = launch_app.run_program(path[0], path[1])

                            if success:
                                logging.info("Action: Opened " + project + " for the user")
                            else:
                                raise Exception("Failed to open application")

                    except Exception as ex:
                        interface.output("Sorry sir, I ran into an error with that program: " + project,
                                         "error", msg="Action: ")
                        print(ex)

                # PUSH CODE
                elif "push" in command:

                    try:
                        if interest.isdigit():
                            directory = "volume " + interest
                        else:
                            directory = interest

                        # ask for a commit message
                        if config.INTERACTION in ["silent", "earbud"]:
                            commit_message = input("Commit message: ")
                        else:
                            interface.speak("What is the commit message?")
                            commit_message = interface.mic_input()

                        interface.speak(f"Pushing code for you sir")
                        success = launch_app.push_code(directory, commit_message)

                        if success:
                            interface.output(f"Code for {directory} pushed successfully", "info", msg="Action: ")
                        else:
                            raise Exception("Failed to push code")

                    except Exception as ex:
                        interface.output("Sorry sir, I ran into an error with pushing code", "error", msg="Action: ")
                        print(ex)

                # SAY GREETING
                elif command in config.GREETINGS:
                    interface.greetings()
                    logging.info("Action: Greeted the user")

                # OPEN WEBSITE
                elif "go to" in command:
                    open_result = open_website.website_opener(interest)

                    if open_result is None:
                        interface.output("Sorry sir, I couldn't open that website: " + interest,
                                         "error", msg="Action: ")
                    else:
                        interface.output("Opening " + interest, "info", msg="Action: ")

                # TELL THE WEATHER
                elif "weather" in command:
                    city = interest
                    weather_result = weather.fetch_weather(city=city)
                    interface.output(weather_result, "info", msg="Action: ")

                # SEARCH WIKIPEDIA
                elif "tell me about" in command:
                    topic = interest
                    error_string = "Sorry sir, I couldn't find anything on that topic"

                    if topic:
                        wiki_result = wikipedia_search.tell_me_about(topic)

                        if wiki_result:
                            interface.output(wiki_result, "info", msg="Action: ")
                        else:
                            interface.output(error_string, "error", msg="Action: ")
                    else:
                        interface.output(error_string, "error", msg="Action: ")

                # SEARCH GOOGLE
                elif "google" in command:
                    try:
                        google_search.google_search(command)
                        logging.info("Action: Searched google for " + interest)

                    except Exception as ex:
                        interface.output("Sorry sir, I couldn't find anything on that topic", "error", msg="Action: ")
                        print(ex)

                # SEARCH YOUTUBE
                elif "youtube" in command:
                    interface.output(f"Okay sir, playing {interest} on youtube", "info", msg="Action: ")
                    youtube.play_video(interest)

                elif "piano" in command:
                    youtube.play_background()


                # SEND EMAIL
                elif "send an email" in command:

                    try:
                        interface.speak("Who should I send the email to?")
                        recipient = interface.mic_input()
                        rec_email = config.EMAIL_DIC[recipient]

                        if rec_email:
                            interface.speak("What is the title?")
                            subject = interface.mic_input()
                            interface.speak("What should I say?")
                            message = interface.mic_input()
                            msg = "Subject: {}\n\n{}".format(subject, message)

                            success = send_email.mail(config.email, config.email_password, rec_email, msg)

                            if success:
                                interface.output("Email sent successfully", "info", msg="Action: ")
                            else:
                                raise Exception("Email not sent")

                        else:
                            interface.output("Sorry sir, I couldn't find that email address", "error", msg="Action: ")

                    except Exception:
                        interface.output("Sorry sir, I couldn't send that email", "error", msg="Action: ")

                # DO MATH
                elif "calculate" in command:
                    answer = wikipedia_search.compute_math(command)
                    interface.output(answer, "info", msg="Action: ")

                # USE GOOGLE CALENDAR
                elif "calendar" in command:
                    google_calendar.get_events(command)
                    logging.info("Action: Used the calendar")

                elif "close notes" in command:
                    interface.output("Okay sir, closing notes", "info", msg="Action: ")
                    system.close_notes()

                # TAKE NOTES
                elif "note" in command or "write" in command:
                    interface.speak("What should I write down?")
                    if config.INTERACTION in ["silent", "earbud"]:
                        scribble = input("Write here: ")
                    else:
                        scribble = interface.mic_input()

                    note.note(scribble)
                    interface.output("I've made a note of that sir", "info", msg="Action: ")

                # GET TO DO LIST
                elif "to-do" in command or "to do" in command:
                    interface.speak("Here is your to-do list")
                    quehaceres = todo_list.get_todo(interest.split()[-1])
                    interface.output(quehaceres, "info", msg="Action: ")

                # TELL JOKES
                elif "joke" in command:
                    joke = news.tell_joke()
                    interface.output(joke, "info", msg="Action: ")

                # SHOW SYSTEM INFO
                elif "system info" in command:
                    info = system.system_stats()
                    interface.output(info, "info", msg="Action: ")

                # USE MAPS
                elif "where is" in command:
                    try:
                        result = location.parse_input(command)
                        interface.output(result, "info", msg="Action: ")

                    except Exception as ex:
                        interface.output("Sorry sir, I couldn't find that location", "error", msg="Action: ")
                        print(ex)

                # GET IP ADDRESS
                elif "ip address" in command:
                    ip = system.get_ip()
                    interface.output(f"Your IP address is {ip}", "info", msg="Action: ")

                # CHANGE TABS
                elif "switch window" in command:
                    interface.speak("Okay sir, switching windows")
                    system.switch_window()
                    logging.info("Action: Switched window")

                # LOCK COMPUTER
                elif "lock computer" in command:
                    interface.speak("Okay sir, locking computer")
                    system.lock_computer()
                    logging.info("Action: Locked computer")

                # TAKE SCREENSHOTS
                elif "screenshot" in command:
                    interface.speak("What should I call this screenshot sir?")
                    if config.INTERACTION in ["silent", "earbud"]:
                        title = input("Title: ")
                    else:
                        title = interface.mic_input()

                    interface.speak("Okay sir, taking screenshot")
                    note.take_screenshot(title)

                    interface.output("Screenshot saved successfully", "info", msg="Action: ")

                elif "image" in command:

                    try:
                        note.show_image(interest)
                        interface.output("Okay sir, showing screenshot", "info", msg="Action: ")

                    except IOError as ex:
                        interface.output("Sorry sir, I couldn't find that screenshot", "error", msg="Action: ")
                        print(ex)

                # ANSWER QUESTIONS
                elif "what is" in command or "who is" in command:
                    answer = wikipedia_search.compute_math(command)
                    interface.speak(answer)
                    logging.info("Action: Answered " + command)

                # START OF DAY
                elif "start my day" in command:
                    interface.speak("Okay sir, let's get our day started.")

                    # describe the weather
                    interface.output(weather.fetch_weather(city="Provo"), "info", msg="Action: ")

                    # recite today's to do list
                    interface.speak("Here is your to-do list")
                    interface.speak(todo_list.get_todo("today"))
                    logging.info("Action: Got the to-do list")

                    # check battery
                    if system.battery_level() < 50:
                        interface.output("Your battery is low. Please plug in your computer.", "warning",
                                         msg="Action: ")




                elif "what can you do" in command:
                    interface.speak("Right now, I can: "
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
                                    "pushing and pulling code, "
                                    "search google, and "
                                    "open apps like slack and v s code, "
                                    )
                    logging.info("Action: Told the user what the Lila can do")

                elif "development" in command:
                    interface.speak("Right now, the features still in development are: "
                                    "sending emails, "
                                    "using google calendar, "
                                    "running other programs like Ava and Casper, "
                                    "interactive chats, "
                                    "and of course, incorporating chat gpt"
                                    )

                elif "keyword" in command:
                    interface.speak("Here is what I listen for in your commands: "
                                    "Lila will tell me to listen for a command, "
                                    "time, "
                                    "date, "
                                    "launch or open, "
                                    "run, "
                                    "push, "
                                    "go to, "
                                    "weather, "
                                    "tell me about, "
                                    "google, "
                                    "youtube, "
                                    "piano, "
                                    "send an email, "
                                    "calculate, what is, or who is, "
                                    "note, "
                                    "close notes, "
                                    "joke, "
                                    "system info, "
                                    "where is for maps, "
                                    "ip address, "
                                    "switch window, "
                                    "lock computer, "
                                    "screenshot, "
                                    "image, "
                                    "start my day, "
                                    "what can you do, "
                                    "development, "
                                    "silent mode, "
                                    "voice mode, "
                                    "power down, and "
                                    "keyword, "
                                    )

                # SWITCH INPUT MODE
                elif "silent mode" in command:
                    interface.speak("Okay")
                    config.INTERACTION = "silent"
                    interface.output("Okay sir, switching to silent mode", "info", msg="Action: ")

                elif "voice mode" in command:
                    config.INTERACTION = "voice"
                    interface.output("Okay sir, switching to voice mode", "info", msg="Action: ")

                elif "earbud mode" in command:
                    config.INTERACTION = "earbud"
                    interface.output("Okay sir, switching to earbud mode", "info", msg="Action: ")

                elif "press mode" in command:
                    config.INTERACTION = "press"
                    interface.output("Okay sir, switching to press to interface.speak mode", "info", msg="Action: ")

                elif "power down" in command:
                    interface.output("Okay sir, powering down", "info", msg="Action: ")
                    system.power_down()

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
# TODO get google calendar working
# TODO get email working

# other
# TODO add a input box for silent and earbud mode
