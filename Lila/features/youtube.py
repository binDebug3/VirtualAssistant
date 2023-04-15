import time
import random
import re

from urllib import parse, request
import webbrowser
import pyautogui as gui
import pywhatkit


def search_video():
    domain = input("Enter the video name:")
    video = parse.urlencode({'search_query': domain})
    print("Video:", video)

    result = request.urlopen("http://www.youtube.com/results?" + video)
    search_results = re.findall(r'href=\"\/watch\?v=(.{4})', result.read().decode())
    print(search_results)

    url = "http://www.youtube.com/watch?v="+str(search_results)
    webbrowser.open_new(url)

def play_video(video):
    pywhatkit.playonyt(video)

def play_background():
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