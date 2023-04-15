import subprocess
import datetime
import os
from Lila import config
import pyautogui as gui
import time
from PIL import Image

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    file_path = os.path.join(config.note_path, file_name)
    with open(file_path, "w") as f:
        f.write(text)

    notepad = "notepad.exe"
    subprocess.Popen([notepad, file_path])


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


