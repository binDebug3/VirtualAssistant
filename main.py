from Lila import config, interface
from Lila.features import date_time, launch_app, open_website, weather, send_email, google_calendar, google_search, \
    note, location, wikipedia_search, system, todo_list, youtube, news, gui, process_files

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
        # Set up the log ging configuration
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
                    interface.output(date, "info")

                # TELL THE TIME
                elif "time" in command:
                    local_time = date_time.time()
                    interface.output(local_time, "info")

                # OPEN APPLICATION
                elif "launch" in command or "open" in command:
                    app = "Not found"
                    try:
                        path = launch_app.get_path(interest, "app")

                        if path is None:
                            interface.output("Sorry sir, I don't know that application: " + app,
                                             "error")
                        else:
                            interface.speak(f"Launching {app} for you sir")
                            success = launch_app.launch_app(path)

                            if success:
                                interface.output("Action: Opened " + app + " for the user", "info")
                            else:
                                raise Exception("Failed to open application")

                    except Exception as ex:
                        interface.output("Sorry sir, I ran into an error with that application: " + app,
                                         "error")
                        print(ex)

                # RUN ANOTHER PROGRAM
                elif "run" in command:
                    project = "Not found"
                    try:
                        path = launch_app.get_path(project, "program")

                        if path is None:
                            interface.output("Sorry sir, I don't know that program: " + project,
                                             "error")
                        else:
                            interface.speak(f"Launching {project} for you sir")
                            success = launch_app.run_program(path[0], path[1])

                            if success:
                                interface.output("Action: Opened " + project + " for the user", "info")
                            else:
                                raise Exception("Failed to open application")

                    except Exception as ex:
                        interface.output("Sorry sir, I ran into an error with that program: " + project,
                                         "error")
                        print(ex)

                # PUSH CODE
                elif "push" in command:

                    try:
                        if interest.isdigit():
                            directory = "volume " + interest
                        else:
                            directory = interest

                        # ask for a commit message
                        if config.INTERACTION in ["terminal"]:
                            commit_message = input("Commit message: ")
                        elif config.INTERACTION in ["silent", "earbud"]:
                            commit_message = gui.input_window("Commit message: ")
                        else:
                            interface.speak("What is the commit message?")
                            commit_message = interface.mic_input()

                        interface.speak(f"Pushing code for you sir")
                        success = launch_app.push_code(directory, commit_message)

                        if success:
                            interface.output(f"Code for {directory} pushed successfully", "info")
                        else:
                            raise Exception("Failed to push code")

                    except Exception as ex:
                        interface.output("Sorry sir, I ran into an error with pushing code", "error")
                        print(ex)

                # SAY GREETING
                elif command in config.GREETINGS:
                    interface.greetings()
                    logging.info("Action: Greeted the user")

                # OPEN WEBSITE
                elif "go to" in command:
                    open_result = open_website.website_opener(interest)

                    if open_result is None:
                        interface.output("Sorry sir, I couldn't open that website: " + interest, "error")
                    else:
                        interface.output("Opening " + interest, "info")

                # TELL THE WEATHER
                elif "weather" in command:
                    weather_result = weather.fetch_weather(city=interest)
                    interface.output(weather_result, "info")

                # SEARCH WIKIPEDIA
                elif "tell me about" in command:
                    error_string = "Sorry sir, I couldn't find anything on that topic"

                    if interest:
                        wiki_result = wikipedia_search.tell_me_about(interest)

                        if wiki_result:
                            interface.output(wiki_result, "info")
                        else:
                            interface.output(error_string, "error")
                    else:
                        interface.output(error_string, "error")

                # SEARCH GOOGLE
                elif "google" in command:
                    try:
                        google_search.google_search(command)
                        logging.info("Action: Searched google for " + interest)

                    except Exception as ex:
                        interface.output("Sorry sir, I couldn't find anything on that topic", "error")
                        print(ex)

                # SEARCH YOUTUBE
                elif "youtube" in command:
                    interface.output(f"Okay sir, playing {interest} on youtube", "info")
                    youtube.play_video(interest)

                # PLAY MUSIC
                elif "piano" in command:
                    youtube.play_background()

                elif "news" in command:
                    stories = news.parse_news(news.get_headlines())
                    interface.output(stories, "info")

                elif "check email" in command:
                    labels = send_email.check_unread()
                    interface.output(labels, "info")

                # SEND EMAIL
                elif "send email" in command:

                    try:
                        interface.speak("Who should I send the email to?")
                        recipient, _ = interface.get_command("To whom?")
                        # rec_email = config.EMAIL_DIC[recipient]
                        rec_email = recipient

                        if rec_email is not None:
                            interface.speak("What is the title?")
                            subject, _ = interface.get_command("Title?")
                            interface.speak("What should I say?")
                            message, _ = interface.get_command("Body?")
                            msg = "Subject: {}\n\n{}".format(subject, message)

                            success, _ = send_email.send_email(subject, msg, rec_email)

                            if success:
                                interface.output("Email sent successfully", "info")
                            else:
                                raise Exception("Email not sent")

                        else:
                            interface.output("Sorry sir, I couldn't find that email address", "error")

                    except Exception:
                        interface.output("Sorry sir, I couldn't send that email", "error")

                # DO MATH
                elif "calculate" in command:
                    answer = wikipedia_search.compute_math(command)
                    interface.output(answer, "info")

                # USE GOOGLE CALENDAR
                elif "check calendar" in command:
                    success = google_calendar.get_events(command)
                    if success:
                        interface.output("Action: Checked the calendar", "info")
                    else:
                        interface.output("Sorry sir, I couldn't access the calendar", "error")

                # ADD CALENDAR EVENT
                elif "add event" in command:
                    interface.speak("What is the event called?")
                    event_name, _ = interface.get_command()
                    interface.speak("What day is the event?")
                    event_date, _ = interface.get_command()
                    interface.speak("What time does the event start?")
                    event_start, _ = interface.get_command()

                    interface.speak("Would you like to customize the details further?")
                    customize, _ = interface.get_command()

                    if "yes" in customize:
                        interface.speak("What time does the event end?")
                        event_end, _ = interface.get_command()
                        interface.speak("What color is the event?")
                        color, _ = interface.get_command()
                        interface.speak("How early should the notification be?")
                        notification, _ = interface.get_command().split(" ")[0]
                        interface.speak("What should I write in the description?")
                        description, _ = interface.get_command()

                        success = google_calendar.add_event(event_name, event_date, event_start,
                                                            event_end, color, notification, description)
                    else:
                        success = google_calendar.add_event(event_name, event_date, event_start)

                    if success:
                        interface.output("Event added successfully", "info")
                    else:
                        interface.output("Sorry sir, I couldn't add that event", "error")

                # CLOSE NOTES
                elif "close notes" in command:
                    interface.output("Okay sir, closing notes", "info")
                    note.close_notes()

                # TAKE NOTES
                elif "note" in command or "write" in command:
                    interface.speak("What should I write down?")
                    if config.INTERACTION in ["silent", "earbud", "terminal"]:
                        scribble = input("Write here: ")
                    else:
                        scribble = interface.mic_input()

                    note.note(scribble)
                    interface.output("I've made a note of that sir", "info")

                # GET TO DO LIST
                elif "to-do" in command or "to do" in command or "todo" in command:
                    interface.speak("Here is your to-do list")
                    interface.output(todo_list.get_todo(interest.split()[-1]), "info")

                # TELL JOKES
                elif "joke" in command:
                    joke = news.tell_joke()
                    interface.output(joke, "info")

                # GET XKCD
                elif "xkcd" in command:
                    news.get_xkcd()
                    interface.output("Here's the most recent x k c d comic", "info")

                # SHOW SYSTEM INFO
                elif "system info" in command:
                    info = system.system_stats()
                    interface.output(info, "info")

                # USE MAPS
                elif "where is" in command:
                    try:
                        result = location.parse_input(command)
                        interface.output(result, "info")

                    except Exception as ex:
                        interface.output("Sorry sir, I couldn't find that location", "error")
                        print(ex)

                # GET IP ADDRESS
                elif "ip address" in command:
                    ip = system.get_ip()
                    interface.output(f"Your IP address is {ip}", "info")

                # CHANGE TABS
                elif "switch window" in command:
                    interface.output("Okay sir, switching windows", "info")
                    system.switch_window()

                # LOCK COMPUTER
                elif "lock computer" in command:
                    interface.output("Okay sir, locking computer", "info")
                    system.lock_computer()

                # TAKE SCREENSHOTS
                elif "screenshot" in command:
                    interface.speak("What should I call this screenshot sir?")
                    if config.INTERACTION in ["silent", "earbud", "terminal"]:
                        title = input("Title: ")
                    else:
                        title = interface.mic_input()

                    interface.speak("Okay sir, taking screenshot")
                    note.take_screenshot(title)

                    interface.output("Screenshot saved successfully", "info")

                # OPEN IMAGE
                elif "image" in command:

                    try:
                        note.show_image(interest)
                        interface.output("Okay sir, showing screenshot", "info")

                    except IOError as ex:
                        interface.output("Sorry sir, I couldn't find that screenshot", "error")
                        print(ex)

                # ANSWER QUESTIONS
                elif "what is" in command or "who is" in command:
                    answer = wikipedia_search.compute_math(command)
                    interface.output(answer, "info")

                # START OF DAY
                elif "start my day" in command:
                    interface.speak("Okay sir, let's get our day started.")

                    # describe the weather
                    interface.output(weather.fetch_weather(city="Provo"), "info")

                    # recite today's to do list
                    interface.speak("Here is your to-do list")
                    interface.speak(todo_list.get_todo("today"))
                    logging.info("Action: Got the to-do list")

                    # check battery
                    if system.battery_level() < 50:
                        interface.output("Your battery is low. Please plug in your computer.", "warning",
                                         msg="Action: ")

                # MERGE PDFS
                elif "merge pdf" in command:
                    default = interface.get_command("Default?")
                    if default != "no":
                        success, name = process_files.merge_pdfs()
                    else:
                        interface.speak("Please enter the p d fs you would like to merge")
                        file_path1 = input("File path one:")
                        file_path2 = input("File path two:")

                        success, name = process_files.merge_pdfs(file_path1, file_path2)

                    if success:
                        interface.output(f"Successfully created {name}", "info")
                    else:
                        interface.output("Sorry sir, I couldn't merge those files", "error")

                # CONVERT JUPITER NOTEBOOKS
                elif "jupiter" in command:
                    interface.speak("Please enter the jupiter notebook you would like to convert")
                    file_path = input("File path:")

                    success, name = process_files.convert_notebook(file_path)

                    if success:
                        interface.output(f"Successfully created {name}", "info")
                    else:
                        interface.output("Sorry sir, I couldn't convert that file", "error")

                # EXTRACT TEXT
                elif "extract text" in command:
                    interface.speak("Please enter the file you would like to extract text from")
                    file_path = input("File path:")

                    success, name = process_files.extract_text(file_path)

                    if success:
                        interface.output(f"Successfully created {name}", "info")
                    else:
                        interface.output("Sorry sir, I couldn't extract text from that file", "error")


                # DESCRIBE CAPABILITIES
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

                # DESCRIBE UPCOMING FEATURES
                elif "development" in command:
                    interface.speak("Right now, the features still in development are: "
                                    "running other programs like Ava and Casper, "
                                    "interactive chats, "
                                    "and of course, incorporating chat gpt"
                                    )

                # REPORT KEYWORDS
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
                    interface.output("Okay sir, switching to silent mode", "info")

                elif "voice mode" in command:
                    config.INTERACTION = "voice"
                    interface.output("Okay sir, switching to voice mode", "info")

                elif "earbud mode" in command:
                    config.INTERACTION = "earbud"
                    interface.output("Okay sir, switching to earbud mode", "info")

                elif "press mode" in command:
                    config.INTERACTION = "press"
                    interface.output("Okay sir, switching to press to speak mode", "info")

                elif "terminal mode" in command:
                    config.INTERACTION = "terminal"
                    interface.output("Okay sir, switching to terminal only mode", "info")

                elif "power down" in command:
                    interface.output("Okay sir, powering down", "info")
                    system.power_down()

                else:
                    logging.error("Action: Command not recognized - " + command)
            if config.INTERACTION not in ["silent", "earbud", "terminal"]:
                logging.error("Action: No keyword found in command - " + command)


startExecution = MainThread()
startExecution.run()

# nlp
# TODO work on nlp part
# TODO make more nlp data
# TODO process gmails for me
# TODO make a chatbot feature

# testing and debugging
# TODO get run other programs working
# TODO test pypdf2 functionality
# TODO implement todoist functionality

"""
- use more APIs
    - AI APIs
"""
