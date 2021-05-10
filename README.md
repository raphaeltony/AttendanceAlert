# Attendance Alert

A Python Script that alerts the user whenever the teacher says the word "attendance" during online class. The alert is sent to their phone via a Telegram Bot.

> NOTE : This is only supported for **Google Meet**.

## How the script works

This script depends on a Chrome extension called "Meet Transcript". During your Google Meet, this extension converts your conversation into text and stores it as a Google Doc file in your Google account. The Python script then accesses the Doc file and checks if the word "attendance" exists in the file. If it does, it alerts the user via a Telegram bot.

## Pre-requisites

- Google Chrome
- Install the "Meet Transcript" Chrome extension from the Chrome webstore. Get it [here](https://chrome.google.com/webstore/detail/meet-transcript/jkdogkallbmmdhpdjdpmoejkehfeefnb?hl=en)

- Python

- A Google Cloud Platform project with the Drive API and Docs API enabled. To create a project and enable an API, refer to [Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)

1.  Authorization credentials for a desktop application. To create credentials for a desktop application, refer to [Create credentials](https://medium.com/@chingjunetao/simple-way-to-access-to-google-service-api-a22f4251bb52) (If you can't access the above link, try opening it in incognito mode).
2.  Rename the file to 'credentials' and place it on the same folder as the script
3.  In the OAuth consent screen menu, make sure you add your Google account to 'Trusted Users'

- Setup your telegram bot and link it to python. Refer [here](https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580) (If you can't access this link, try opening it in incognito mode)

- Open up the terminal and run this command :

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

```

## Running the Script

- Only run the script if you have succesfully completed the pre-requisites
  > The Captions must be turned on during the Google Meet for the extension to record the conversation.
- During the meeting, observe the "Meet Transcript" logo at the bottombar.
  > Only run the program when the logo changes from "Ready" to "Transcript"
- When the script runs for the first time, it will launch the browser and ask you to verify your Google Account. Complete the authentication process.
