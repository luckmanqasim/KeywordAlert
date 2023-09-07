from filter_email import EmailFilter
import imaplib
from dotenv import load_dotenv
import os

if __name__ == "__main__":

    email_filter = EmailFilter()
    
    try:
        email_filter.connect()
        email_ids = email_filter.matching_email_ids()
        email_filter.fetch_emails(email_ids)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        email_filter.disconnect()