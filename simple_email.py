import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_simple_email():
    load_dotenv()
    smtp_server = os.getenv('SendEmailSMTP')
    smtp_port = int(os.getenv('SendEmailPort'))
    username = os.getenv('SendEmailUSR')
    password = os.getenv('SendEmailPWD')

    # Ange din e-postadress här
    recipient = "mats@duvner.com"

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = "Test E-post"

    body = "Detta är ett testmeddelande från Python-skriptet."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.send_message(msg)
            print("E-postmeddelande skickat framgångsrikt!")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

if __name__ == "__main__":
    send_simple_email()