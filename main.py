from filter_email import EmailFilter
import imaplib
from dotenv import load_dotenv
import os
from message_client import Message

if __name__ == "__main__":

    # access evironmental variables
    load_dotenv()

    email_address = os.getenv('INBOX_ADDRESS')
    password = os.getenv('INBOX_PASSWORD')
    imap_server = os.getenv('INBOX_IMAP_SERVER')
    #keywords = os.getenv('KEYWORDS')
    keywords = ['job']
    

    email_filter = EmailFilter(email_address, password, imap_server, keywords, destination_folder='Test')
    
    try:
        email_filter.connect()
        print('connected')
        email_ids = email_filter.matching_email_ids()
        print(email_ids)
        email_filter.create_destination_folder()
        print('labels')
        email_filter.move_emails(email_ids)
        email_filter.fetch_emails(email_ids)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        email_filter.disconnect()