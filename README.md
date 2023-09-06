# Email Keyword Filter and SMS Notifier

This project is a Python script that filters incoming emails for specific keywords and sends SMS notifications when a matching email is found. It can be a handy automation tool for staying informed about important emails while on the go.


## Features

- Connects to your email account using IMAP to retrieve incoming emails.

- Filters emails based on predefined keywords in the subject, body, or other headers.

- Sends SMS notifications when a matching email is detected.


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your local machine.

- IMAP access enabled for your email account.

- Installed package: `imaplib`. You can install them using `pip`:

```bash
pip install imaplib twilio
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.