from __future__ import print_function

import base64
import os.path
from datetime import datetime, timedelta
from Lila import config

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_labels():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
