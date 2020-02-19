import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import urllib.request

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRETS_FILE = 'client_secret_668378957760-c17u8nc01o5h9tf7gp52sjjqfdjhpsnn.apps.googleusercontent.com.json'
def get_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

service = get_service()

results = service.mediaItems().list(pageSize=100).execute()
item_counter = len(results['mediaItems'])
next = results['nextPageToken']

counter = 1
while True:
    print('ループ回数: ' + str(counter))
    results = service.mediaItems().list(pageSize=100, pageToken=next).execute()
    items = len(results['mediaItems'])
    item_counter = item_counter + items
    try:
        next = results['nextPageToken']
        counter = counter + 1
    except KeyError:
        break

print('Google Photo のファイル合計数' + str(item_counter))
