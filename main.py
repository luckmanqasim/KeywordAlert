from filter_email import EmailFilter
from dotenv import load_dotenv
import os
from message_client import Message
from typing import List


def move_and_return_emails(keywords: List[str], destination_folder: str) -> List[dict]:
    '''
    Moves emails matching specified keywords to a destination folder and retrieves them.

    Args:
        keywords (List[str]): A list of keywords to filter emails.
        destination_folder (str): The destination folder where matching emails will be moved.

    Returns:
        List[dict]: A list of dictionaries representing the retrieved emails.

    Raises:
        Exception: If an error occurs during email filtering and retrieval.
    '''

    email_address = os.getenv('INBOX_ADDRESS')
    password = os.getenv('INBOX_PASSWORD')
    imap_server = os.getenv('INBOX_IMAP_SERVER')
    keywords = keywords
    destination_folder = destination_folder

    if not destination_folder:
        raise Exception('Please enter a destination folder name to move your emails to.')
    
    try:
        email_filter = EmailFilter(email_address, password, imap_server, keywords, destination_folder)

        email_filter.connect()
        email_ids = email_filter.matching_email_ids()
        email_filter.move_emails(email_ids)
        new_data = email_filter.fetch_emails(email_ids)

        return new_data
    
    except Exception as e:
        print(f'An error occurred while sending the email: {e}')

    finally:
        email_filter.disconnect()


def send_new_emails(receiver_email: str, new_data: List[dict]):
    '''
    Send a list of retrieved emails to a specified recipient via email.

    Args:
        receiver_email (str): The email address of the recipient.
        new_data (List[dict]): A list of dictionaries representing the retrieved emails.

    Raises:
        Exception: If an error occurs during the email sending process.
    '''

    sender_email = os.getenv('SENDER_ADDRESS')
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    receiver_email = os.getenv('RECEIVER')

    try:

        msg_client = Message(smtp_server, smtp_port, sender_email, sender_password)
        msg_client.send_email(receiver_email, new_data)

    except Exception as e:
        print(f'An error occurred while sending the email: {e}')


def main():
    '''
    Entry point of the script to filter and send emails.

    This function serves as the entry point for the script. It performs the following tasks:
    
    1. Loads environment variables using `dotenv`.
    2. Filters and retrieves emails matching specified keywords.
    3. Sends the retrieved emails to a specified recipient via email.

    The script relies on environment variables to configure email and messaging services.
    '''

    # access evironmental variables
    load_dotenv()

    new_data = move_and_return_emails(keywords=['test'], destination_folder='test')
    send_new_emails(receiver_email='test@example.com', new_data=new_data)


if __name__ == "__main__":
    main()