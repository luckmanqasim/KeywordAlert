# Email Keyword Filter and SMS Notifier

This project is a Python script that filters incoming emails for specific keywords and sends SMS notifications when a matching email is found. It can be a handy automation tool for staying informed about important emails while on the go.


## Features

- **Email Filtering:** Automatically filter emails in your inbox based on keywords of interest.

- **SMS Alert:** Receive SMS alerts for important emails, keeping you informed on the go.

- **Customizable:** Configure the keywords to filter and destination folders for your emails.


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.

- Gmail or another email service that supports IMAP access.

- A Twilio account for or an email server for sending SMS alerts.

- Environment variables set up with your email and Twilio credentials (see [Configuration](#configuration)).


## Setup

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/email-filter-sms-alert.git
```

2. Navigate to the project directory:

```bash
cd email-filter-sms-alert
```

3. Create a virtual environment (recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

- Windows:

```bash
venv\Scripts\activate
```

- Linux/macOS:

```bash
source venv/bin/activate
```

5. Install the project dependencies:

```bash
pip install -r requirements.txt
```


##Usage

To use this project:

1. Ensure you have set up your environment variables for email and Twilio credentials.

2. Run the project by executing the main.py script:

```bash
python main.py
```

3. The script will filter your emails based on specified keywords, send SMS alerts for important emails, and store the filtered emails in the destination folder.

4. You will receive SMS notifications for important emails on your registered phone number.


## License

This project is licensed under the MIT License - see the LICENSE file for details.