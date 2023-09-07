import email
import imaplib
from dotenv import load_dotenv
import os
import html


class EmailFilter:

    def __init__(self):

        # access evironmental variables
        load_dotenv()

        self.email_address = os.getenv('INBOX_ADDRESS')
        self.password = os.getenv('INBOX_PASSWORD')
        self.imap_server = os.getenv('INBOX_IMAP_SERVER')
        self.keywords = os.getenv('KEYWORDS')
        self.mail = None

    
    # connect to the IMAP server
    def connect(self):

        try:
            # connect to the IMAP server usign email and password
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)

        except Exception as e:
            print(f'Error connecting so the server: {str(e)}')


    # disconnect the IMAP server
    def disconnect(self):
        if self.mail:
            self.mail.logout()


    # search inbox and return filtered email ids
    def matching_email_ids(self):

        # check if we are connected to the imap server
        if not self.mail:
            raise Exception('Not connected to the IMAP server.')
        
        # switch to the inbox to look for new mails
        self.mail.select('inbox')
        
        # store the email ids of the emails in the search criteria
        matching_email_ids = []

        # go through all the search keywords
        for keyword in self.keywords:

            search_criteria = f'(BODY "{keyword}")'
            status, email_ids = self.mail.search(None, search_criteria)

            # save the email ids in the matching_email_ids list
            matching_email_ids.extend(email_ids[0].split())

        # removes the duplicates from the list
        matching_email_ids = list(set(matching_email_ids))
        
        return matching_email_ids
    

    # fetch emails using the email_ids
    def fetch_emails(self, email_ids):
        
        for email_id in email_ids:
            status, email_data = self.mail.fetch(email_id, '(BODY[TEXT])')
            print("----------------")
            email_message = email_data[0][1].decode('utf-8')
            print(email_message)