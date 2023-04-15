import speech_recognition as sr
import pyttsx3
from Demos.mmapfile_demo import system_info

from Lila import config
from Lila.features import date_time, launch_app, open_website, weather, send_email, google_calendar, google_search, \
    note, location, wikipedia_search, system, todo_list

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[config.voice_index].id)

class NavaniAssistant:
    def __init__(self):
        # I don't love the way this code is structured
        # it kind of seems like this developer wrote this class just for the sake of having OOP
        # really main should just call the features directly
        # idk if it's worth the effort to refactor this though
        pass

    # LISTEN
    def mic_input(self):
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
                command = self.mic_input()
            return command
        except Exception as ex:
            print(ex)
            return False

    # SPEAK
    def tts(self, text):
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

    # TELL DATE
    def tell_date(self):
        return date_time.date()

    # TELL TIME
    def tell_time(self):
        return date_time.time()

    # LAUNCH APP
    def launch_app(self, path):
        """
        Run a windows application
        :param path: path to the application
        :return: (boolean) True if successful, False if failure
        """
        return launch_app.launch_app(path)

    # RUN PROGRAM
    def run_program(self, path, name):
        """
        Run a python projects
        :param path: path to the project
        :return: (boolean) True if successful, False if failure
        """
        return launch_app.run_program(path, name)

    # PUSH CODE
    def push_code(self, name, message):
        return launch_app.push_code(name, message)

    # OPEN WEBSITE
    def open_website(self, url):
        """
        Open a website
        :param url: (string) url of the website
        :return: (boolean) True if successful, False if failure
        """
        return open_website.website_opener(url)

    # TELL WEATHER
    def weather(self, city):
        """
        Return the weather
        :param city: (string) name of the city
        :return: (string) weather info
        """
        try:
            return weather.fetch_weather(city)
        except Exception as ex:
            print("Error in weather function")
            print(ex)
            return False

    # WIKIPEDIA
    def tell_me(self, topic):
        """
        Tells about anything on wikipedia
        :param topic: (string) topic to be searched on wikipedia
        :return: (string) First 500 characters of the wikipedia page, boolean False otherwise
        """
        return wikipedia_search.tell_me_about(topic)

    # SEND EMAIL
    def send_email(self, sender, password, receiver, message):
        return send_email.mail(sender, password, receiver, message)

    # USE GOOGLE CALENDAR
    def calendar(self, text):
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text)

        if date:
            return google_calendar.get_events(date, service)
        pass

    # SEARCH GOOGLE
    def search_google(self, text):
        return google_search.google_search(text)

    # TAKE NOTE
    def take_note(self, text):
        return note.note(text)

    # TELL SYSTEM INFO
    def system_info(self):
        return system.system_stats()

    # GET BATTERY LEVEL
    def battery_level(self):
        return system.battery_level()

    def switch_window(self):
        return system.switch_window()

    # TELL LOCATION
    def find_location(self, loc):
        return location.location(loc)

    # TELL POSITION
    def my_location(self):
        return location.my_location()

    # GET TO DO LIST
    def get_todo(self, day):
        return todo_list.get_todo(day)

    """
    - run other programs
        - AVA
        - Casper
        - ACME labs, and specific test cases in ACME labs
    
    - use more APIs
        - text analysis
        - scrapeninja or scrapestack
        - SEO API
        - XKCD API
        - IBM watson text to speech
        
    - favorite automation
        - use chatGPT
        - process gmails for me
        
    - make a chatbot feature
    - try out the GUI
    """