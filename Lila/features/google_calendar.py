from __future__ import print_function
from datetime import datetime, timedelta
import pytz
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from Lila import config, interface


MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authenticate_google():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    :return:
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

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

    return build('calendar', 'v3', credentials=creds)


def get_events(text):
    """
    Gets events from google calendar in the specified time interval
    :param text:
        text: (string) the text to parse to get the dates
    :return:
        None
    """
    # dallin customize this so it ignores my college classes

    service = authenticate_google()
    day = get_date(text)

    if day is None or not day:
        return None

    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary',
                                          timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        interface.speak('No upcoming events found.')
    else:
        length = len(events)
        if length == 1:
            interface.speak(f"You have one event on {day}.")
        else:
            interface.speak(f"You have {length} events on {day}.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

            # hours
            start_time = str(start.split("T")[1].split("-")[0])
            # if morning or afternoon
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            interface.speak(event["summary"] + " at " + start_time)


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
                    except:
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

        return today + datetime.timedelta(dif)

    if day != -1:
        return datetime.date(month=month, day=day, year=year)


def add_event(title, date, start,
              end=None, color="Blueberry", notification=10, description="", recurring=None):
    """
    Add an event to the user's calendar
    :param
        title: (string) title of the event
        start: (string) start time of the event
        end: (string) end time of the event
        date: (string) date of the event
        color: (string) color of the event
        notification: (int) notification time of the event
        description: (string) description of the event
        recurring: (string) when to recur the event
    :return:
    """
    service = authenticate_google()

    # error handling
    if end is None:
        # if end time is not provided, set it to 1 hour after start time
        start_time = datetime.strptime(start, '%H:%M')
        end_time = start_time + timedelta(hours=1)
        end = end_time.strftime('%H:%M')

    if color not in ["Tomato", "Flamingo", "Tangerine", "Banana", "Sage", "Basil",
                     "Peacock", "Blueberry", "Lavender", "Grape", "Graphite"]:
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
            'dateTime': '{}T{}'.format(date, start),
            'timeZone': config.timezone
        },
        'end': {
            'dateTime': '{}T{}'.format(date, end),
            'timeZone': config.timezone
        },
        'colorId': color,
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
    except HttpError as error:
        print('An error occurred: %s' % error)
        event = None
        return False

    return True

