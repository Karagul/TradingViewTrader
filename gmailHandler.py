import base64
import time
from email.mime.text import MIMEText

from aptdaemon import errors
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import extractedEmail
from extractedEmail import email

from apiclient import errors

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'


class gmailHandler:
    label = 'inbox'
    fromFilter = None
    gmailAPI = None
    refreshTime = 5
    real_money = False
    readEmailCommand = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
    lastReceivedEmails = None

    def __init__(self, locationOfCredentials):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(locationOfCredentials, SCOPES)
            creds = tools.run_flow(flow, store)
        self.gmailAPI = build('gmail', 'v1', http=creds.authorize(Http()))

    # responds with the message
    def listen(self, timeoutSeconds):
        count = 0
        while count < timeoutSeconds or timeoutSeconds < 0:

            if not self.real_money:
                response = self.gmailAPI.users().messages().list(userId='me',
                                                             q=' is:unread from:kalgofund@gmail.com').execute()
            else:
                response = self.gmailAPI.users().messages().list(userId='me',
                                                                 q=' is:unread from:noreply@tradingview.com').execute()

            if 'messages' in response:
                return self.readEmails(response)
            else:
                time.sleep(self.refreshTime)
                if count % 240 == 0:
                    print("\n")
                print(".", end="", flush=True)
                count = count + 1

    def readEmails(self, emails):
        messageIds = emails['messages']
        processedEmails = []

        self.lastReceivedEmails = messageIds

        for messageId in messageIds:
            message = self.gmailAPI.users().messages().get(userId='me', id=messageId['id']).execute()
            if self.authEmail(message):
                processedEmails.append(email(message))
            else:
                self.setEmailsToRead()

        return processedEmails




    def setEmailsToRead(self):
        for messageId in self.lastReceivedEmails:
            self.gmailAPI.users().messages().modify(userId='me', id=messageId['id'],
                                                    body=self.readEmailCommand).execute()

    def authEmail(self, email):
        return extractedEmail.getParamFromHeader(email['payload']['headers'], 'Subject').find(
            extractedEmail.email.boundaryString) != -1


    def sendEmail(self, message):
        try:
            message = (self.gmailAPI.users().messages().send(userId='me', body=message).execute())
            print
            'Message Id: %s' % message['id']
            return message
        except errors.HttpError as error:
            print
            'An error occurred: %s' % error
        return


    def createMessage(sender, subject, message_text):
        message = MIMEText(message_text)
        message['To'] = 'kalgofund@gmail.com'
        message['From'] = 'kalgofund@gmail.com'
        message['Subject'] = subject

        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_string = b64_bytes.decode()
        return {'raw': b64_string}
