import datetime


def date():
    """
    Return the current date
    :return: (string) current date, False if failure
    """
    try:
        return datetime.datetime.now().strftime("%b %d %Y")
    except Exception as ex:
        print("Error in date function")
        print(ex)
        return False


def time():
    """
    Return the current time
    :return: (string) current time, False if failure
    """
    try:
        clock = datetime.datetime.now().strftime("%H:%M")
        parsed = clock.split(':')
        hour = int(parsed[0])
        if hour > 12:
            hour -= 12
            parsed[0] = str(hour)
            parsed.append("p.m.")
        elif hour == 12:
            parsed.append("p.m.")
        else:
            parsed.append("a.m.")
        if parsed[1][0] == "0":
            if parsed[1][1] == "0":
                parsed[1] = "o clock"
            else:
                parsed[1] = "o " + parsed[1][1]
        print(clock)
        clock = " ".join(parsed)
        return clock
    except Exception as ex:
        print("Error in time function")
        print(ex)
        return False