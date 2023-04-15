from todoist_api_python.api import TodoistAPI
from Lila import config
import datetime


api = TodoistAPI(config.todoist_api)

def get_todo(day):
    present = {}
    abnormal = {}
    future = {}
    if day != "today":
        target_date = datetime.date.today() + datetime.timedelta(days=1)
        target_date = target_date.strftime("%Y-%m-%d")
    else:
        target_date = datetime.date.today()
        target_date = target_date.strftime("%Y-%m-%d")

    try:
        tasks = api.get_tasks()
    except Exception as error:
        print(error)
        return "Sorry, I can't get your tasks right now."

    for task in tasks:
        if task.due is not None:
            todo = {task.content: [task.due.date, task.labels, task.due.is_recurring]}
            if task.due.date == target_date:
                if not task.due.is_recurring:
                    abnormal.update(todo)
                else:
                    present.update(todo)
            else:
                future.update(todo)

    return formet_list(abnormal, present, day)


def formet_list(abnormal, present, day):
    output = ""

    # recite abnormal tasks
    count_ab = len(abnormal)
    if count_ab == 0:
        output += f"All of your tasks are normal {day}. "
    elif count_ab == 1:
        output += f"You have {len(abnormal)} scheduled task. " + \
                    f"You need to {list(abnormal.keys())[0]}."
    else:
        output += f"You have {len(abnormal)} scheduled tasks today. You need to: "
        for task in abnormal.keys():
            output += f"{task}."

    # analyze recurring tasks
    count_math = 0
    for key in present.keys():
        if "HW" in key:
            count_math += 1
    for key in list(present.keys()):
        if "HW" in key:
            del present[key]
    if count_math == 4:
        present.update({"Complete and submit all of the ACME homework": [None, None, True]})

    # recite recurring tasks
    count_rec = len(present)
    if count_rec == 0:
        output += "Congratulation! You have no recurring tasks today."
    elif count_rec == 1:
        output += f"You have {count_rec} recurring task. " + \
                    f"You need to {list(present.keys())[0]}."
    else:
        output += f"You have {count_rec} recurring tasks. You need to: "
        for i, task in enumerate(present.keys()):
            output += f"{task}, "
            if i == count_rec - 2:
                output += "and "

    return output