# Attendance Alert

A Python Script that alerts the user whenever the teacher says the word "attendance" during online class. The alert is sent to their phone via a Telegram Bot.

> NOTE : This is only supported for **Google Meet**.

## How the script works

This script depends on a Chrome extension called "Meet Transcript". During your Google Meet, this extension converts your conversation into text and stores it as a Google Doc file in your Google account. The Python script then accesses the Doc file and checks if the word "attendance" exists in the file. If it does, it alerts the user via a Telegram bot.

## Pre-requisites

- Google Chrome
- Install the "Meet Transcript" Chrome extension from the Chrome webstore. Get it [here](https://chrome.google.com/webstore/detail/meet-transcript/jkdogkallbmmdhpdjdpmoejkehfeefnb?hl=en)

- Python

- A Google Cloud Platform project with the **Drive API** and **Docs API** enabled, along with its authorization credentials for a desktop application. Checkout the following section [(Setting Up Google Cloud Console)](#setting-up-google-cloud-console) to learn how to implement this.

- Setup your telegram bot and link it to python. Refer [here](https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580) (If you can't access this link, try opening it in incognito mode)

- Open up the terminal and run this command :

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

```

## Setting Up Google Cloud Console

For the script to access the Google Doc that contains the meeting dialogues, a Google Cloud Platform project must be set up with the **_Drive API_** and **_Docs API_** enabled. Then the user credentials must be downloaded and placed in the same folder as the script.

- Follow the steps mentioned in this [link](https://medium.com/@chingjunetao/simple-way-to-access-to-google-service-api-a22f4251bb52) (If you can't access the above link, try opening it in incognito mode).
- In Step 2 of the link mentioned above, make sure you add the Google Docs API also.
- At Step 3, click the _Credentials_ menu at the sidebar on the left and then click _Create Credentials_. Choose _OAuth client ID_. Application Type is _Desktop App_.
- While setting up the OAuth consent screen, choose _User Type_ as _External_ and hit _Create_. At the _App Information_ screen, give any name and fill **only** the required email fields. The scopes menu can be left blank. **Make sure you add your Google Account under Test users**

> After downloading the file, rename it to 'credentials' and place it on the same folder as the script

## Running the Script

- Only run the script if you have succesfully completed the pre-requisites
- The Captions must be turned on during the Google Meet for the extension to record the conversation.
  > During the meeting, observe the "Meet Transcript" logo at the bottombar. Only run the program when the logo changes from "Ready" to "Transcript"
- When the script runs for the first time, it will launch the browser and ask you to verify your Google Account. Complete the authentication process.
