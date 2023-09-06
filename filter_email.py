import email
import imaplib
from dotenv import load_dotenv
import os


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
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)
            self.mail.select('inbox')

        except Exception as e:
            print(f'Error connecting so the server: {str(e)}')


    # disconnect the IMAP server
    def disconnect(self):
        if self.mail:
            self.mail.logout()


    # search inbox and return filtered email ids
    def matching_email_ids(self):

        if not self.mail:
            raise Exception('Not connected to the IMAP server.')
        
        matching_email_ids = []

        for keyword in self.keywords:
            search_criteria = f'(BODY "{keyword}")'
            status, email_ids = self.mail.search(None, search_criteria)
            matching_email_ids.extend(email_ids[0].split())

        # removes the duplicates from the list
        matching_email_ids = list(set(matching_email_ids))
        
        return matching_email_ids
    

