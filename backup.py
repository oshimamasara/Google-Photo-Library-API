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

results = service.mediaItems().list(pageSize=100).execute() # pageSize最大100
item_counter = len(results['mediaItems']) #item_counter max 99
next = results['nextPageToken']

# 最初のページ
# ファイル数 99/page
counter = 1

def save_data():
    global counter
    items_per_page = 0
    while items_per_page < item_counter:
        file_name = results['mediaItems'][items_per_page]['filename']
        item_url = results['mediaItems'][items_per_page]['baseUrl']
        data_type = results['mediaItems'][items_per_page]['mimeType']
        folder_name = file_name[2:8]

        def data_save():
            # image or video
            if 'image' in data_type:
                try:
                    urllib.request.urlretrieve(item_url + '=d', folder_name + '/' + file_name)
                except:
                    print('save error...')
                    print(file_name)

            elif 'video' in data_type:
                try:
                    urllib.request.urlretrieve(item_url + '=dv', folder_name + '/' + file_name)
                except:
                    print('save error...')
                    print(file_name)
            else:
                print('あれ、このデータは何だ...error,,,')
                print(file_name)

        if os.path.isdir(folder_name):
            data_save()
        else:
            os.mkdir(folder_name)
            data_save()

        print(str(counter))

        items_per_page += 1
        counter += 1

save_data()

while True:
    results = service.mediaItems().list(pageSize=100, pageToken=next).execute()
    item_counter = len(results['mediaItems'])
    save_data()

    try:
        next = results['nextPageToken']
        counter = counter + 1
    except KeyError:
        break


print('バックアップしたファイル数：' + str(counter))