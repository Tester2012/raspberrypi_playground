import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from os import environ

def send_message(body):
    message = MIMEText(body)

    message['Subject'] += datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message['To'] = environ['TO_EMAIL']

    smtp_server = smtplib.SMTP('localhost')
    smtp_server.send_message(message)
    smtp_server.quit()