import email
from email.header import decode_header
import imaplib
from dotenv import load_dotenv
import os
import html


class EmailFilter:

    def __init__(self, email_address, password, imap_server, keywords, destination_folder):

        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.keywords = keywords
        self.destination_folder = destination_folder
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
            self.mail.close()
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

            search_criteria = f'(UNSEEN BODY "{keyword}")'

            status, email_ids = self.mail.search(None, search_criteria)

            if status == 'OK':
                # save the email ids in the matching_email_ids list
                matching_email_ids.extend(email_ids[0].split())

        # removes the duplicates from the list
        matching_email_ids = list(set(matching_email_ids))
        
        return matching_email_ids
    

    # fetch emails using the email_ids
    def fetch_emails(self, email_ids):
        """
        Fetch and process (get the subject and sender) email messages based on a list of email IDs.

        Args:
            email_ids (list): A list of email IDs to fetch and process.

        Returns:
            list: A list of dictionaries, where each dictionary contains the subject and sender information
                of the fetched emails.

        Raises:
            Exception: If an error occurs during the fetching and processing of emails, an exception is raised,
                    and the error message is printed.
        """

        new_emails = []
        
        for email_id in email_ids:

            try:
                # fetch the email by ID
                status, email_data = self.mail.fetch(email_id, '(RFC822)')

                # parse the email content
                msg = email.message_from_bytes(email_data[0][1])

                # decode the subject
                subject, encoding = decode_header(msg['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or 'utf-8')

                # append the subject and sender of the emails to new_emails list
                new_email = {'Subject': subject, 'From': msg['From']}
                new_emails.append(new_email)

            except Exception as e:
                print(f'An error occurred {e}')

        return new_emails


    # create a new label/folder if it doesnt exist, default is 'starred'
    def _create_destination_folder(self):

        # get the list of all the labels
        response, mailbox_list = self.mail.list()

        # check for the destinaion folder in the list of all folders
        folder_exists = any(self.destination_folder in mailbox.decode('utf-8') for mailbox in mailbox_list)

        # if it does not exist create a new one
        if not folder_exists:

            try:
                self.mail.create(self.destination_folder)
                
            except Exception as e:
                print(f'Error creating the folder: {e}')


    # move the selected emails to a different folder
    def move_emails(self, email_ids):
        """
        Move specified emails to a destination folder and mark them as seen.

        Args:
            email_ids (list): A list of email IDs to move.

        Raises:
        Exception: If the destination folder is not provided or is empty, an exception is raised with
                   an error message.
        """

        if not self.destination_folder:
            raise Exception('Please enter a destination folder name to move your emails to')
        
        # create a destiation folder is it doesnt already exist
        self._create_destination_folder()

        for email_id in email_ids:

            try:
                # copy the emails to the new folder
                self.mail.copy(email_id, self.destination_folder.encode('utf-8'))
                
                # mark the emails as seen
                self.mail.store(email_id, '+FLAGS', '(\Seen)')

            except Exception as e:
                print(f'An error occured {e}')