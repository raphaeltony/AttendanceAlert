from __future__ import print_function
import os.path
import sys
import time
import re
import telegram_send
#from playsound import playsound
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']


# This function takes the text in a paragraph of the document and splits it up in a way such that
# it ignores punctuations (done by the 're' command) and stores all the words in a list(res).
# Then it checks if the word 'attendance' exists in the list
def checkAttendance(sent):
    res = re.findall(r'\w+', sent)
    for i in res:
        if i.lower() == "attendance":
            return True
    return False

# This function uses the Drive API to fetch the folders in your Google Drive. Once it gets the
# id of the folder called "Meet Transcript", it then returns the id of the very first file (the
# latest doc which contains the dialogues of the current Google Meeting) in that folder.


def getDocumentID(creds):
    driveService = build('drive', 'v3', credentials=creds)

    results = driveService.files().list(
        q="mimeType = 'application/vnd.google-apps.folder' and name = 'Meet Transcript'", fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        sys.exit("The folder called 'Meet Transcript' does not exist. Please run the program after the 'Meet Transcript' Chrome Extension is running during the Google Meeting")
    else:
        folderID = items[0]['id']

    results = driveService.files().list(
        q="parents in '{}'".format(folderID), pageSize=1, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        sys.exit("No doc files found. Please run the program after the 'Meet Transcript' Chrome Extension is running during the Google Meeting")
    else:
        return items[0]['id']


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

    # Getting the document ID of the latest Google Meet conversation
    DOCUMENT_ID = getDocumentID(creds)
    print("Script is up and running ! DO NOT CLOSE THIS APPLICATION")

    # Retrieve the documents contents using the Docs API. Here document is a dictionary
    # that has a lot of nested dictionaries and lists within it.
    docService = build('docs', 'v1', credentials=creds)
    currentIndex = 1
    notFound = True
    while notFound:
        document = docService.documents().get(documentId=DOCUMENT_ID).execute()

        # Going through every paragraph in the document
        for i in range(currentIndex, len(document['body']['content'])):
            #print("i =  :", i)
            try:
                if checkAttendance(document['body']['content'][i]['paragraph']
                                   ['elements'][1]['textRun']['content']):
                    notFound = False
                    break
                else:
                    # This is so that the next time the document is retrieved, it doesn't have to
                    # go through all the paragraphs again. It just begins searching for the word
                    # at the paragraph it left off.
                    currentIndex = i

                    # In case, there are chat messages during the Gmeet, the document gets
                    # modified by the chrome extension. In that case, we have to manually stop
                    # the search whenever we find this page seperator. The reason its i+3 is
                    # because after the text of the latest paragraph, there are two '\n'
                    # characters, only after which the seperator occurs in the document
                    if document['body']['content'][i+3]['paragraph']['elements'][0]['textRun']['content'] == "____________________________________________________________________________\n":
                        break

            except IndexError:
                continue
            except KeyError:
                continue

        time.sleep(2)  # Checking every 2 seconds

    print("Alert! : Attendance Call")
    telegram_send.send(messages=["ATTENDANCE"])
    # playsound('run.mp3')


if __name__ == '__main__':
    main()
