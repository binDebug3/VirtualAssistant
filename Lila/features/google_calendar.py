from __future__ import print_function
from datetime import datetime, timedelta, date
import pytz
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from Lila import config, interface


MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    :return:
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.

    if os.path.exists(config.cal_token):
        with open(config.cal_token, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.cal_credentials, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(config.cal_token, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds, cache_discovery=False)


def get_events(text):
    """
    Gets events from Google calendar in the specified time interval
    :param text:
        text: (string) the text to parse to get the dates
    :return:
        None
    """
    # dallin customize this so it ignores my college classes

    service = authenticate_google()
    day = get_date(text)

    if day is None or not day:
        return False

    # Call the Calendar API
    target_date = datetime.combine(day, datetime.min.time())
    end_date = datetime.combine(day, datetime.max.time())
    utc = pytz.UTC
    target_date = target_date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary',
                                          timeMin=target_date.isoformat(),
                                          timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        interface.output('No upcoming events found.', "info")
    else:
        length = len(events)
        if length == 1:
            interface.output(f"You have one event on {day}.", "info")
        else:
            interface.output(f"You have {length} events on {str(day).split()[0]}.", "info")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])

            # hours
            start_time = str(start.split("T")[1].split("-")[0])
            # if morning or afternoon
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            interface.output(event["summary"] + " at " + start_time, "info")

    return True


def get_date(text):
    """
    Gets the date from the text
    :param text:
           text: (string) the text to parse to get the dates
    :return:
        date: (datetime) the date that was parsed
    """
    today = datetime.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except ValueError:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + timedelta(dif)

    if day != -1:
        return date(month=month, day=day, year=year)


def add_event(title, target_date, start,
              end=None, color="Blueberry", notification=10, description="", recurring=None):
    """
    Add an event to the user's calendar
    :param title: (string) title of the event
    :param start: (string) start time of the event
    :param end: (string) end time of the event
    :param date: (string) date of the event
    :param color: (string) color of the event
    :param notification: (int) notification time of the event
    :param description: (string) description of the event
    :param recurring: (string) when to recur the event
    :return: True if event was added successfully, False otherwise
    """
    colors = ["Tomato", "Flamingo", "Tangerine", "Banana", "Sage", "Basil",
                     "Peacock", "Blueberry", "Lavender", "Grape", "Graphite"]
    service = authenticate_google()
    start += ":00"
    target_date = "2023-" + target_date

    # error handling
    if end is None:
        # if end time is not provided, set it to 1 hour after start time
        start_time = datetime.strptime(start, '%H:%M:%S')
        end_time = start_time + timedelta(hours=1)
        end = end_time.strftime('%H:%M:%S')
    else:
        end += ":00"

    if color not in colors:
        color = "Blueberry"

    if type(notification) is not int:
        notification = 10

    # recurring = "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"

    # Create event object
    event = {
        'summary': title,
        'location': '',
        'description': description,
        'start': {
            'dateTime': '{}T{}-06:00'.format(target_date, start),
            'timeZone': config.timezone
        },
        'end': {
            'dateTime': '{}T{}-06:00'.format(target_date, end),
            'timeZone': config.timezone
        },
        'colorId': colors.index(color),
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': notification},
            ],
        },
    }

    # Add recurrence if specified
    if recurring:
        event['recurrence'] = [
            'RRULE:{}'.format(recurring),
        ]

    # Add event to calendar
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return True
    except HttpError as error:
        print('An error occurred: %s' % error)
        return False
