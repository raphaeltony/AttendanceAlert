from __future__ import print_function
import os.path
import time
import re
import telegram_send
from playsound import playsound
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']


def checkAttendance(sent):
    res = re.findall(r'\w+', sent)
    for i in res:
        if i.lower() == "attendance":
            return True
    return False


def getDocumentID(creds):
    driveService = build('drive', 'v3', credentials=creds)

    results = driveService.files().list(
        q="mimeType = 'application/vnd.google-apps.folder'", fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            if item['name'] == "Meet Transcript":
                folderID = item['id']
            #print(u'{0} ({1})'.format(item['name'], item['id']))

    results = driveService.files().list(
        q="parents in '{}'".format(folderID), pageSize=1, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        # for item in items:
        #     print(u'{0} ({1})'.format(item['name'], item['id']))
        DOCUMENT_ID = items[0]['id']
        return DOCUMENT_ID


def main():
    """Shows basic usage of the Docs API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Retrieve the documents contents from the Docs service.
    docService = build('docs', 'v1', credentials=creds)
    currentIndex = 1
    notFound = True
    while notFound:
        document = docService.documents().get(documentId=getDocumentID(creds)).execute()

        for i in range(currentIndex, len(document['body']['content'])):
            print("i =  :", i)
            try:
                if checkAttendance(document['body']['content'][i]['paragraph']
                                   ['elements'][1]['textRun']['content']):
                    notFound = False
                    break
                else:
                    currentIndex = i
                    if document['body']['content'][i+3]['paragraph']['elements'][0]['textRun']['content'] == "____________________________________________________________________________\n":
                        break

            except IndexError:
                continue
            except KeyError:
                continue

        time.sleep(2)

    print("Alert!")
    telegram_send.send(messages=["attendance"])
    # playsound('run.mp3')


if __name__ == '__main__':
    main()
