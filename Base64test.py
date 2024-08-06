import os
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import logging

# Konfigurera loggning
logging.basicConfig(filename='base64_test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class ConfigLoader:
    def __init__(self, env_path):
        self.env_path = env_path

    def load_config(self):
        load_dotenv(self.env_path)
        config = {
            'sender_email': os.getenv('SendEmailUSR'),
            'password': os.getenv('SendEmailPWD'),
            'smtp_server': os.getenv('SendEmailSMTP'),
            'smtp_port': int(os.getenv('SendEmailPort')),
        }
        logging.info(f"Config loaded: {config}")
        return config

def convert_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        logging.info(f"Image converted to BASE64. Length: {len(base64_string)}")
        return base64_string
    except Exception as e:
        logging.error(f"Error converting image to base64: {e}")
        return ""

def create_test_html(base64_image):
    html_content = f"""
    <html>
    <body>
        <h1>BASE64 Image Test</h1>
        <img src="data:image/png;base64,{base64_image}" alt="Test Image">
    </body>
    </html>
    """
    logging.info(f"HTML content created. Length: {len(html_content)}")
    return html_content

def send_test_email(config, recipient, subject, html_content):
    try:
        logging.info(f"Attempting to connect to SMTP server: {config['smtp_server']}:{config['smtp_port']}")
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
            logging.info("Connected to SMTP server. Attempting login.")
            server.login(config['sender_email'], config['password'])
            logging.info("Login successful. Creating email message.")
            
            msg = MIMEMultipart()
            msg['From'] = config['sender_email']
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(html_content, 'html'))
            
            logging.info(f"Sending email to: {recipient}")
            server.sendmail(config['sender_email'], recipient, msg.as_string())
            logging.info("Test e-mail sent successfully.")
    except Exception as e:
        logging.error(f'Error sending test e-mail: {e}')
        raise  # Re-raise the exception to see it in the console

if __name__ == "__main__":
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_directory, '.env')
        logging.info(f"Loading config from: {dotenv_path}")
        
        config_loader = ConfigLoader(dotenv_path)
        config = config_loader.load_config()
        
        test_image_path = "sales_data_plot_WUSmRV.png"
        logging.info(f"Converting image: {test_image_path}")
        base64_image = convert_image_to_base64(test_image_path)
        
        if base64_image:
            html_content = create_test_html(base64_image)
            recipient = "mats@duvner.com"  # Ändra till din testmottagaradress
            subject = "BASE64 Image Test"
            
            logging.info("Attempting to send test email")
            send_test_email(config, recipient, subject, html_content)
        else:
            logging.error("Failed to convert image to BASE64.")
    except Exception as e:
        logging.error(f"Unexpected error in main execution: {e}")
        print(f"An error occurred. Check the log file for details: {e}")