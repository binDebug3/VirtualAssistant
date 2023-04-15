from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
import pyttsx3
import time

from Lila import config


def speak(text):
    # dallin make speak a global function so I don't have to keep re instantiating
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[config.voice_index].id)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 175)


def google_search(prompt):
    reg_ex = re.search('google (.*)', prompt)
    print("prompt: ", prompt)
    search_for = prompt.split("google ", 1)[1]
    url = 'https://www.google.com/'

    if reg_ex:
        sub = reg_ex.group(1)
        url = url + 'r/' + sub

    speak('Okay!')
    speak("Searching for " + search_for)

    driver = webdriver.Chrome(executable_path=config.chrome_path)
    driver.get('http://www.google.com', )
    time.sleep(0.1)
    search = driver.find_element(By.NAME, 'q')
    search.send_keys(search_for)
    search.send_keys(Keys.RETURN)

    input("Close the browser to continue")
    driver.quit()

    # dallin add a way to speak search results