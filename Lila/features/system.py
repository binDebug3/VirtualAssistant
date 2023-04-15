import math
import time
import sys
import ctypes
import psutil
import requests
import pyautogui as gui

import utils


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    output = "%s %s" % (s, size_name[i])
    print(output)
    return output


def system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery().percent
    memory_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)

    return f"Currently {cpu_stats} percent of CPU, {memory_use} of RAM out of total {total_memory} is being used. " + \
        f"Battery level is at {battery_percent} percent"

def battery_level():
    return psutil.sensors_battery().percent


def switch_window():
    gui.keyDown("alt")
    gui.press("tab")
    time.sleep(0.01)
    gui.keyUp("alt")


def get_ip():
    return requests.get("https://api.ipify.org").text

def lock_computer():
    ctypes.windll.user32.LockWorkStation()

def power_down():
    utils.save_interactions()
    sys.exit()