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
    keywords = ['job']

    sender_email = os.getenv('SENDER_ADDRESS')
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    

    email_filter = EmailFilter(email_address, password, imap_server, keywords, destination_folder='Test')
    msg_client = Message(smtp_server, smtp_port, sender_email, sender_password)
    
    try:
        email_filter.connect()
        print('connected')
        email_ids = email_filter.matching_email_ids()
        print(email_ids)
        email_filter.create_destination_folder()
        print('labels')
        email_filter.move_emails(email_ids)
        new_datas = email_filter.fetch_emails(email_ids)
        msg_client.send_email(receiver_email='7097666866@msg.koodomobile.com', new_data=new_datas)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        email_filter.disconnect()