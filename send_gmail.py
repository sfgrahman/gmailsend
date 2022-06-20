from __future__ import print_function

import os.path

import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = 'https://www.googleapis.com/auth/gmail.send'


def gmail_send():
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('cren.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	try:
		# create gmail api client
		service = build('gmail', 'v1', credentials=creds)
		message = EmailMessage()
		message.set_content('This is automated draft mail')
		message['To'] = 'sfgrahman35@gmail.com'
		message['From'] = 'gduser2@workspacesamples.dev'
		message['Subject'] = 'Automated draft'
		# encoded message
		encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
		create_message = {
			'raw': encoded_message
			}
		draft = service.users().drafts().create(userId="me",body=create_message).execute()
		print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
	except HttpError as error:
		print(F'An error occurred: {error}')
		draft = None

	return draft

if __name__ == '__main__':
	gmail_send()