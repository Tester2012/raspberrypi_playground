import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from os import environ

def send_message(body):
    message = MIMEText(body)

    message['Subject'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message['To'] = environ['TO_EMAIL']
    message['From'] = environ['FROM_EMAIL']

    smtp_server = smtplib.SMTP(environ['MAIL_HUB'])
    smtp_server.starttls()
    smtp_server.login(message['From'], environ['FROM_PASSWORD'])
    smtp_server.send_message(message)
    smtp_server.quit()

send_message("This is a test")
