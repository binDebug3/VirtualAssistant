from Lila import config

import sys
import os
import subprocess


def get_path(interest, select_dict):
    for key in config.dict_app.keys():
        if key in interest:
            app = key
            break
    if select_dict == "app":
        return config.dict_app[app]
    elif select_dict == "program":
        return config.dict_app[app]


def launch_app(path):
    try:
        # subprocess.run([path])
        subprocess.Popen(path)
        return True
    except Exception as ex:
        print(ex)
        return False


def run_program(path, name):
    try:
        # Replace the file path below with the path to your requirements file
        req_path = path + "/requirements.txt"
        program_path = path + "/" + name

        # Read the contents of the file and create a list of each line as an element
        with open(req_path, "r") as file:
            packages = [line.strip() for line in file]

        # get required imports
        for package in packages:
            sys.path.append(os.path.join(os.environ["USERPROFILE"], "anaconda3", "lib", "site-packages", package))
        # sys.path.append(os.path.join(os.environ["USERPROFILE"], "anaconda3", "lib", "site-packages"))
        print("Packages:")
        for path in sys.path:
            print(path)

        print("\nExecutable")
        print(sys.executable)

        # print("\nTesting")
        # print(os.path.join(os.environ["USERPROFILE"], "anaconda3", "lib", "site-packages", package[0]))

        subprocess.run(["python", program_path])
        return True

    except Exception as ex:
        print(ex)
        return False


def push_code(name, message=None, master=True):
    try:
        push_path = os.path.abspath(config.dir_dict[name])
    except KeyError as ex:
        print(ex)
        return False

    if not os.path.exists(push_path):
        return False

    if master:
        master = "master"
    else:
        master = "main"

    command = f"cd {push_path} && git pull origin {master} && git add ."

    if message is None:
        # add commit pull push with a default commit message
        command += " && git commit -m 'pushing'"
    else:
        # add commit pull push with the passed-in commit message
        command += f" && git commit -m '{message}'"

    command += f" && git push origin {master}"

    subprocess.run(command, shell=True)

    return True
