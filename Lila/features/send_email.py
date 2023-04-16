from __future__ import print_function

import base64
import os.path
from datetime import datetime, timedelta
from email.mime.text import MIMEText

from Lila import config

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(config.mail_token):
        creds = Credentials.from_authorized_user_file(config.mail_token, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.mail_credentials, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(config.mail_token, 'w') as token:
            token.write(creds.to_json())

    return creds


def check_unread():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = get_credentials()

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Define the search parameters for the email query
        today = datetime.today() + timedelta(days=1)
        one_day_ago = today - timedelta(days=3)
        query = "is:unread after:{} before:{}".format(one_day_ago.strftime('%Y/%m/%d'), today.strftime('%Y/%m/%d'))

        # Execute the email query
        result = service.users().messages().list(userId='me', q=query).execute()

        return process_query(result, service)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def process_query(result, service, detailed=False):
    # Process the results
    emails = []
    if 'messages' in result:
        messages = result['messages']

        for i, msg in enumerate(messages):
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload['headers']

            for d in headers:
                if d['name'] == 'From':
                    sender = d['value']
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'Date':
                    received_time = datetime.strptime(d['value'][:-6], '%a, %d %b %Y %H:%M:%S').strftime(
                        '%Y/%m/%d %I:%M %p')

            if 'parts' in payload:
                parts = payload['parts']
                data = parts[0]['body']['data']

            else:
                data = payload['body']['data']

            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)
            if detailed:
                emails.append(f"{i+1}: From: {sender}\nSubject: {subject}"
                              f"\nReceived: {received_time}\nBody: {decoded_data}")
            emails.append(f"{i+1}: From: {sender}\nSubject: {subject}")

        intro = f"You have {len(messages)} unread messages in the last day \n"
        return intro + "\n\n".join(emails)
    else:
        return 'No unread messages found in the last day'


def send_email(subject, message_text, recipient):
    """
    Send an email from the user's account.
    :param
        subject: (string) The subject of the email message.
        message_text: (string) The text of the email message.
        recipient: (string) The email address of the recipient.
    :return:
    """
    creds = get_credentials()

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Create the email message
        message = MIMEText(message_text)
        message['to'] = recipient
        message['subject'] = subject

        # Send the email message
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (service.users().messages().send(userId='me', body=create_message).execute())

        return send_message['id']

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None



def delete_email(identifier, mark_as_read=False):
    """
    Delete an email from the user's account.
    :param
        identifier: (string) The id of the email message.
            Could be the subject, the sender, or the message id.
        mark_as_read: (boolean) If true, mark the email as read, delete otherwise.
    :return:
    """
    creds = get_credentials()

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Find the email message
        query = ' '.join(['"' + identifier + '"', 'in:all'])
        result = service.users().messages().list(userId='me', q=query).execute()

        if not result['messages']:
            print('No message matches the search criteria.')
            return None

        # Delete or mark as read the email message
        if mark_as_read:
            msg_labels = {'removeLabelIds': ['UNREAD']}
            print('The email message will be marked as read.')
        else:
            msg_labels = {'addLabelIds': ['TRASH']}
            print('The email message will be deleted.')

        # Modify the email message
        for msg in result['messages']:
            msg_id = msg['id']
            service.users().messages().modify(userId='me', id=msg_id, body=msg_labels).execute()

        return True

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def scan_inbox():
    """
    Scan the users inbox and automatically identify urgent emails,
    and mark as read or delete unimportant emails
    """
    raise NotImplementedError("This feature is not yet implemented")


def create_event():
    """
    Create an event in the user's calendar based on details in an email.
    """
    creds = get_credentials()

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Define the search parameters for the email query
        today = datetime.today() + timedelta(days=1)
        one_day_ago = today - timedelta(days=7)
        query = "after:{} before:{} subject:{}".format(one_day_ago.strftime('%Y/%m/%d'), today.strftime('%Y/%m/%d'), "Event Details")

        # Execute the email query
        result = service.users().messages().list(userId='me', q=query).execute()

        if not result['messages']:
            print('No message matches the search criteria.')
            return None

        # Extract the event details from the email message
        event_details = get_event_details(result['messages'][0]['id'], service)

        # Call the Calendar API
        calendar_service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': event_details['title'],
            'location': event_details['location'],
            'description': event_details['description'],
            'start': {
                'dateTime': event_details['start_time'],
                'timeZone': event_details['time_zone'],
            },
            'end': {
                'dateTime': event_details['end_time'],
                'timeZone': event_details['time_zone'],
            },
            'reminders': {
                'useDefault': True,
            },
        }

        # Create the event in the user's calendar
        calendar_service.events().insert(calendarId='primary', body=event).execute()

        print('Event created: %s' % (event.get('htmlLink')))
        return True

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def get_event_details(msg_id, service):
    """
    Extract the event details from an email message.
    :param
        msg_id: (string) The id of the email message.
        service: (Gmail service object) The Gmail service object.
    :return:
        event_details: (dictionary) A dictionary of the event details.
    """
    # Get the email message
    message = service.users().messages().get(userId='me', id=msg_id).execute()

    # Extract the event details from the message body
    message_body = message['payload']['parts'][0]['body']['data']
    message_body_decoded = base64.urlsafe_b64decode(message_body).decode('utf-8')
    event_details = {}
    for line in message_body_decoded.splitlines():
        if line.startswith('Title: '):
            event_details['title'] = line[7:]
        elif line.startswith('Location: '):
            event_details['location'] = line[10:]
        elif line.startswith('Start Time: '):
            start_time_str = line[12:]
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
            event_details['start_time'] = start_time
        elif line.startswith('End Time: '):
            end_time_str = line[10:]
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
            event_details['end_time'] = end_time

    return event_details