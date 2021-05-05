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
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = ''


# This function takes the text in a paragraph of the document and splits it up in a way such that
# it ignores punctuations (done by the 're' command) and stores all the words in a list(res).
# Then it checks if the word 'attendance' exists in the list
def checkAttendance(sent):
    res = re.findall(r'\w+', sent)
    for i in res:
        if i.lower() == "attendance":
            return True
    return False


def main():
    print("Enter the document ID : ")
    DOCUMENT_ID = input()

    """Shows basic usage of the Docs API. This code is a snippet from the Docs API website:
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

    service = build('docs', 'v1', credentials=creds)

    currentIndex = 1
    notFound = True
    while notFound:
        # Retrieve the documents contents from the Docs service. Here document is a dictionary
        # that has a lot of nested dictionaries and lists
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        # Going through every paragraph in the document
        for i in range(currentIndex, len(document['body']['content'])):
            print("i =  :", i)
            try:
                if checkAttendance(document['body']['content'][i]['paragraph']
                                   ['elements'][1]['textRun']['content']):
                    notFound = False
                    break
                else:
                    # This is so that the next time the document is retrieved, it doesn't have to
                    # go through all the paragraphs again. It just begins searching for the word
                    # at the latest paragraph.
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

    print("Alert!")
    telegram_send.send(messages=["attendance"])
    # playsound('run.mp3')


if __name__ == '__main__':
    main()
