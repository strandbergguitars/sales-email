import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import logging
from smtplib import SMTP_SSL
import csv

# Konfigurera loggning
logging.basicConfig(filename='email_log.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class ConfigLoader:
    """Laddar konfigurationer från en .env-fil."""
    
    def __init__(self, env_path):
        self.env_path = env_path

    def load_config(self):
        """Laddar konfigurationer från .env-filen och returnerar en ordbok."""
        load_dotenv(self.env_path)
        config = {
            'sender_email': os.getenv('SendEmailUSR'),
            'password': os.getenv('SendEmailPWD'),
            'smtp_server': os.getenv('SendEmailSMTP'),
            'smtp_port': os.getenv('SendEmailPort')
        }
        
        # Diagnostik - Skriv ut alla laddade värden
        logging.info("Laddade konfigurationsvärden: %s", config)
        print("Laddade konfigurationsvärden:", config)

        # Kontrollera om någon variabel saknas
        missing_keys = [key for key, value in config.items() if not value]
        if missing_keys:
            logging.error("Följande miljövariabler saknas eller är ogiltiga: %s", missing_keys)
            raise ValueError(f"Följande miljövariabler saknas eller är ogiltiga: {missing_keys}")
        
        # Konvertera smtp_port till int
        config['smtp_port'] = int(config['smtp_port'])
        
        return config


class EmailBuilder:
    """Bygger e-postmeddelanden."""
    
    def __init__(self, sender_email, receiver_email, subject, message):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject
        self.message = message

    def build_email(self):
        """Bygger och returnerar ett e-postmeddelande som ett MIMEMultipart-objekt."""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message, 'plain'))
        return msg


class EmailSender:
    """Skickar e-postmeddelanden via en SMTP-server."""
    
    def __init__(self, smtp_server, smtp_port, sender_email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password

    def send_email(self, email_msg):
        """Skickar ett e-postmeddelande och hanterar anslutning till SMTP-servern."""
        try:
            logging.info("Försöker att ansluta till SMTP-servern: %s på port %d med SSL.", self.smtp_server, self.smtp_port)
            print(f"Försöker att ansluta till SMTP-servern: {self.smtp_server} på port {self.smtp_port} med SSL.")
            with SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.password)
                logging.info("Inloggning till SMTP-servern lyckades.")
                server.sendmail(self.sender_email, email_msg['To'], email_msg.as_string())
                logging.info("E-postmeddelandet har skickats till %s.", email_msg['To'])
            logging.info("SMTP-anslutningen avslutades.")
            print("E-postmeddelandet har skickats!")
        except smtplib.SMTPAuthenticationError:
            logging.error("Inloggning till SMTP-servern misslyckades. Kontrollera användarnamn och lösenord.")
            print("Inloggning till SMTP-servern misslyckades. Kontrollera användarnamn och lösenord.")
        except smtplib.SMTPConnectError:
            logging.error("Anslutning till SMTP-servern misslyckades. Kontrollera serveradressen och porten.")
            print("Anslutning till SMTP-servern misslyckades. Kontrollera serveradressen och porten.")
        except Exception as e:
            logging.error("Ett oväntat fel inträffade: %s", e)
            print(f"Ett oväntat fel inträffade: {e}")


def load_recipients(csv_path):
    """Laddar mottagare från en CSV-fil och returnerar en lista med e-postadresser."""
    recipients = []
    try:
        with open(csv_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                recipients.append(row['email'])
        logging.info("Laddade mottagare: %s", recipients)
    except Exception as e:
        logging.error("Kunde inte läsa CSV-filen: %s", e)
        raise e
    return recipients


if __name__ == "__main__":
    # Hämta den aktuella arbetskatalogen och ladda konfigurationer
    current_directory = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_directory, '.env')
    csv_path = os.path.join(current_directory, 'recipients.csv')

    if not os.path.exists(dotenv_path):
        logging.error(".env-filen hittades inte i katalogen: %s", current_directory)
        raise FileNotFoundError(f".env-filen hittades inte i katalogen: {current_directory}")

    config_loader = ConfigLoader(dotenv_path)
    config = config_loader.load_config()

    # Ladda mottagare från CSV-filen
    recipients = load_recipients(csv_path)

    # Bygg och skicka e-postmeddelandet till varje mottagare
    subject = "Ditt ämne här"
    message = "Ditt meddelande här"
    email_sender = EmailSender(config['smtp_server'], config['smtp_port'], config['sender_email'], config['password'])

    for recipient in recipients:
        email_builder = EmailBuilder(config['sender_email'], recipient, subject, message)
        email_msg = email_builder.build_email()
        email_sender.send_email(email_msg)