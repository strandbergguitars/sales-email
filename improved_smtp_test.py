import smtplib
from dotenv import load_dotenv
import os
import sys
import traceback

def test_smtp_connection():
    try:
        print("Starting SMTP connection test")
        
        print("Loading .env file")
        load_dotenv()
        
        print("Reading SMTP settings from .env")
        smtp_server = os.getenv('SendEmailSMTP')
        smtp_port = os.getenv('SendEmailPort')
        username = os.getenv('SendEmailUSR')
        password = os.getenv('SendEmailPWD')

        print(f"SMTP settings loaded:")
        print(f"Server: {smtp_server}")
        print(f"Port: {smtp_port}")
        print(f"Username: {username}")
        print(f"Password: {'*' * len(password) if password else 'Not set'}")

        if not all([smtp_server, smtp_port, username, password]):
            raise ValueError("One or more SMTP settings are missing in the .env file")

        smtp_port = int(smtp_port)

        print(f"Attempting to connect to {smtp_server}:{smtp_port}")
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            print("Connected to SMTP server")
            server.login(username, password)
            print("Login successful")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Script started")
    result = test_smtp_connection()
    print(f"SMTP connection test {'passed' if result else 'failed'}")
    print("Script finished")