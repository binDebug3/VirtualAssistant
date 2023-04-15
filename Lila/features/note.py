from Lila import config

import os
import time
import datetime
import subprocess
import pyautogui as gui
from PIL import Image


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    file_path = os.path.join(config.note_path, file_name)
    with open(file_path, "w") as f:
        f.write(text)

    notepad = "notepad.exe"
    subprocess.Popen([notepad, file_path])

def close_notes():
    os.system("TASKKILL /F /IM notepad.exe")


def take_screenshot(title):
    image_path = os.path.join(config.image_path, title)

    screenshot = gui.screenshot()
    screenshot.save(f"{image_path}.png")


def show_image(interest):
    image_path = os.path.join(config.image_path,
                              interest + ".png")
    img = Image.open(image_path)
    img.show()
    time.sleep(2)


