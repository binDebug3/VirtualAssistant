import subprocess
import datetime
import os
from Lila import config

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    file_path = os.path.join(config.note_path, file_name)
    with open(file_path, "w") as f:
        f.write(text)

    notepad = "notepad.exe"
    subprocess.Popen([notepad, file_path])