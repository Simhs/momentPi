from __future__ import print_function
import httplib2
import os
import pprint
from apiclient import discovery
import apiclient.http
import datetime
from oauth2client import *
from oauth2client.file import Storage
import argparse


class Gdrive:
	def __init__(self):
		SCOPES = 'https://www.googleapis.com/auth/drive'
		CLIENT_SECRET_FILE = '/home/dollar/Desktop/Dclient_secret.json'
		APPLICATION_NAME = 'Drive API Python Quickstart'

		#self.FILENAME = 'test.mp4'

		# Metadata about the file.
		self.MIMETYPE = 'video/mp4'
		self.TITLE = str(datetime.datetime.now())
		self.DESCRIPTION = 'A shiny new text document about hello world.'
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

	def get_credentials(self):
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
			Credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = self.APPLICATION_NAME
			if self.flags:
				credentials = tools.run_flow(flow, store, self.flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
				print('Storing credentials to ' + credential_path)
		return credentials

	def drive(self, FILENAME):
		"""Shows basic usage of the Google Drive API.

		Creates a Google Drive API service object and outputs the names and IDs
		for up to 10 files.
		"""
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		drive_service = apiclient.discovery.build('drive', 'v2', http=http)
		media_body = apiclient.http.MediaFileUpload(FILENAME,mimetype=self.MIMETYPE,resumable=True)
		body = {'title': self.TITLE,'description': self.DESCRIPTION,}

		"""send file"""
		new_file = drive_service.files().insert(body=body, media_body=media_body).execute()

		"""google drive file list"""
		results = drive_service.files().list(maxResults=10).execute()
		items = results.get('items', [])
		print('Files:')
		for item in items:
			print('{0}'.format(item['title']))

if __name__ == '__main__':
	gsend = Gdrive()
	gsend.drive("/home/dollar/Downloads/testlapse100.mp4")
