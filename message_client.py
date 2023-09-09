import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Message:

    def __init__(self, smtp_server, port, sender_email, sender_password):
        """
        Initialize the email sender.

        Args:
            smtp_server (str): SMTP server address.
            port (int): SMTP server port.
            sender_email (str): Sender's email address.
            sender_password (str): Sender's email password.
        """

        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password


    # send and email with the name, price and url of the new ads
    def send_email(self, receiver_email, new_data):
        """
        Send an email.

        Args:
            receiver_email (str): Recipient's email address.
            subject (str): Email subject.
            body (str): Email body.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """

        try:
            # initialze the email client and login
            smtp_obj = smtplib.SMTP_SSL(self.smtp_server, self.port)
            smtp_obj.ehlo()
            smtp_obj.login(self.sender_email, self.sender_password)

            subject = self._create_email_subject(new_data)
            body = self._create_email_body(new_data)
            print(subject, body)

            # create the email object
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
                
            # send the email
            smtp_obj.sendmail(self.sender_email, receiver_email, msg.as_string())
            smtp_obj.quit()

            # returns True if the email is successfully sent
            return True

        except smtplib.SMTPAuthenticationError as auth_error:
            # handle authentication errors
            print(f'SMTP Authentication Error: {auth_error}')
            return False
        
        except smtplib.SMTPException as smtp_error:
            # handle other SMTP errors
            print(f'SMTP Error: {smtp_error}')
            return False
        
        except Exception as e:
            # handle other exceptions
            print(f'Error sending email: {e}')
            return False


    # create a subject for the email depending if there are any new ads or not
    def _create_email_subject(self, new_data):
        """
        Create the email subject based on the number of new ads.

        Args:
            new_data (list): List of new ads.

        Returns:
            str: Email subject.
        """

        if len(new_data) == 0:
            subject = 'Sorry you have no new emails related your query.'
        else:
            subject = f'You have {str(len(new_data))} new emails related to your query!'

        return subject
    

    # Creates a body containing the info for new ads by parsing the list of new data in human readable form
    def _create_email_body(self, new_data):
        """
        Create the email body with information about new ads.

        Args:
            new_data (list): List of new ads.

        Returns:
            str: Email body.
        """

        # formats the list of new ads into human readable form
        if len(new_data) == 0:
            body = 'Sadly there are no new emails regarding your query since last time.'
        else:
            body = ''
            for item in new_data:
                    body += f'Subject: {item["Subject"]}\nFrom: {item["From"]}\n\n'

        return body
