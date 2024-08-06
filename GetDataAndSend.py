import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import logging
from smtplib import SMTP_SSL
import csv
import pyodbc
from datetime import datetime, timedelta

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
            'smtp_port': os.getenv('SendEmailPort'),
            'db_server': os.getenv('DB_SERVER'),
            'db_name': os.getenv('DB_NAME'),
            'db_user': os.getenv('DB_USER'),
            'db_password': os.getenv('DB_PASSWORD'),
        }
        
        # Diagnostik - Skriv ut alla laddade värden
        logging.info("Laddade konfigurationsvärden: %s", config)

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
    
    def __init__(self, sender_email, receiver_email, subject, message, message_html):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject
        self.message = message
        self.message_html = message_html

    def build_email(self):
        """Bygger och returnerar ett e-postmeddelande som ett MIMEMultipart-objekt."""
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = self.subject

        part1 = MIMEText(self.message, 'plain')
        part2 = MIMEText(self.message_html, 'html')

        msg.attach(part1)
        msg.attach(part2)
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


class DatabaseFetcher:
    """Hämtar data från en databas."""
    
    def __init__(self, db_server, db_name, db_user, db_password):
        self.db_server = db_server
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def fetch_data(self, sql_file_path):
        """Hämtar data från databasen genom att köra en SQL-fråga från en fil."""
        try:
            # Skapa anslutningssträngen
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.db_server};DATABASE={self.db_name};UID={self.db_user};PWD={self.db_password}"
            
            # Anslut till databasen
            logging.info('Försöker ansluta till databasen')
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            logging.info('Anslutning till databasen lyckades')

            # Läs SQL-frågan från filen
            with open(sql_file_path, 'r') as file:
                sql_query = file.read()
            logging.info(f'Läste SQL-frågan.')
            
            # Ställ SQL-frågan
            logging.info('Ställer SQL-frågan')
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            logging.info('SQL-frågan kördes framgångsrikt')

            # Bearbeta resultatet
            results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            logging.info(f'Hämtade resultat: {results}')

            return results
        except Exception as e:
            logging.error(f'Fel vid körning av SQL-frågan: {e}')
            raise
        finally:
            # Stäng anslutningen
            conn.close()
            logging.info('Databasanslutningen stängdes')


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


def convert_to_html_table(data):
    """Konverterar en lista med ordböcker till en HTML-tabell."""
    if not data:
        return "<p>Inga data tillgängliga.</p>"
    
    headers = data[0].keys()
    html = "<table border='1' style='border-collapse: collapse;'>"
    html += "<tr>" + "".join(f"<th style='padding: 8px; border: 1px solid black;'>{header}</th>" for header in headers) + "</tr>"
    
    for row in data:
        html += "<tr>" + "".join(f"<td style='padding: 8px; border: 1px solid black;'>{value}</td>" for value in row.values()) + "</tr>"
    
    html += "</table>"
    return html


if __name__ == "__main__":
    # Hämta den aktuella arbetskatalogen och ladda konfigurationer
    current_directory = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_directory, '.env')
    csv_path = os.path.join(current_directory, 'recipients.csv')
    sql_file_path = os.path.join(current_directory, 'getinstruments.sql')

    if not os.path.exists(dotenv_path):
        logging.error(".env-filen hittades inte i katalogen: %s", current_directory)
        raise FileNotFoundError(f".env-filen hittades inte i katalogen: {current_directory}")

    config_loader = ConfigLoader(dotenv_path)
    config = config_loader.load_config()

    # Ladda mottagare från CSV-filen
    recipients = load_recipients(csv_path)

    # Hämta data från databasen
    db_fetcher = DatabaseFetcher(config['db_server'], config['db_name'], config['db_user'], config['db_password'])
    data = db_fetcher.fetch_data(sql_file_path)

    # Konvertera data till en HTML-tabell
    data_html = convert_to_html_table(data)

    # Lägg till gårdagens datum i ämnesraden
    yesterday = datetime.now() - timedelta(1)
    formatted_date = yesterday.strftime('%Y-%m-%d')

    # Bygg och skicka e-postmeddelandet till varje mottagare
    subject = f"Sales data from {formatted_date}"
    message = "Ditt meddelande här"  # Plain text version
    message_html = f"<p>This is the sales data from {formatted_date}</p>{data_html}"  # HTML version

    email_sender = EmailSender(config['smtp_server'], config['smtp_port'], config['sender_email'], config['password'])

    for recipient in recipients:
        email_builder = EmailBuilder(config['sender_email'], recipient, subject, message, message_html)
        email_msg = email_builder.build_email()
    email_sender.send_email(email_msg)