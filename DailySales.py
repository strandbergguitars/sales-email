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
import traceback
from typing import List, Dict
from datetime import datetime, timedelta
from typing import List, Dict
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict
import pandas as pd  # Kontrollera att pandas importeras korrekt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import time




# Konfigurera loggning
# Generera dagens datum i formatet ÅÅÅÅ-MM-DD
today_date = datetime.now().strftime('%Y-%m-%d')

# Skapa filnamnet med dagens datum
log_filename = f'DailySales_log_{today_date}.log'

# Konfigurera loggning med det genererade filnamnet
logging.basicConfig(filename=log_filename, level=logging.DEBUG,
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
        
        # Kontrollera om någon variabel saknas
        missing_keys = [key for key, value in config.items() if not value]
        if missing_keys:
            logging.error("Följande miljövariabler saknas eller är ogiltiga: %s", missing_keys)
            raise ValueError(f"Följande miljövariabler saknas eller är ogiltiga: {missing_keys}")
        
        # Konvertera smtp_port till int
        config['smtp_port'] = int(config['smtp_port'])
        
        return config
    
def read_recipients(csv_file):
    """Läser mottagare från en CSV-fil och returnerar en lista med e-postadresser."""
    df = pd.read_csv(csv_file)
    return df['email'].tolist()

def wait_for_images_to_be_created(image_paths, wait_time=5):
    """Wait and verify that images are created."""
    print(f"Waiting for {wait_time} seconds to ensure all images are created...")
    time.sleep(wait_time)  # Vänta för att säkerställa att bilderna är skapade

    for path in image_paths:
        if not os.path.exists(path):
            print(f"Image file {path} was not found.")
        else:
            print(f"Image file {path} exists.")

def send_emails(config, recipients, subject, html_content):
    """Bygger och skickar e-postmeddelanden till alla mottagare."""
    try:
        # Anslut till SMTP-servern med SSL
        logging.info(f"Ansluter till SMTP-servern {config['smtp_server']} på port {config['smtp_port']}")
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
            server.login(config['sender_email'], config['password'])
            
            for recipient in recipients:
                msg = MIMEMultipart()
                msg['From'] = config['sender_email']
                msg['To'] = recipient
                msg['Subject'] = subject
                
                # Lägg till HTML-delen av meddelandet
                msg.attach(MIMEText(html_content, 'html'))
                
                # Skicka e-postmeddelandet
                logging.info(f"Skickar e-post till {recipient}")
                server.sendmail(config['sender_email'], recipient, msg.as_string())
        
        logging.info("E-postmeddelanden skickades framgångsrikt.")
    except smtplib.SMTPException as e:
        logging.error(f'SMTP-fel: {e}')
    except Exception as e:
        logging.error(f'Allmänt fel vid e-postsändning: {e}')

class DatabaseFetcher:
    """Hämtar data från en databas."""
    
    def __init__(self, db_server, db_name, db_user, db_password):
        self.db_server = db_server
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def execute_sql(self, sql_file_path, fetch_results=False):
        """Kör SQL-kommandon från en fil."""
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
            logging.info(f'Läste SQL-frågan från fil: {sql_file_path}')

            # Ställ SQL-frågan
            logging.info('Ställer SQL-frågan')
            cursor.execute(sql_query)

            if fetch_results:
                rows = cursor.fetchall()
                logging.info('SQL-frågan kördes framgångsrikt')

                # Bearbeta resultatet
                results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
                logging.info(f'Hämtade resultat: {results}')

                return results
            else:
                conn.commit()  # Bekräfta ändringar om det är en DDL- eller DML-kommando
                logging.info('Ingen resultatuppsättning för detta kommando')

        except pyodbc.Error as e:
            logging.error(f'PyODBC Error: {e}')
            logging.error(traceback.format_exc())
            raise
        except Exception as e:
            logging.error(f'Allmänt fel: {e}')
            logging.error(traceback.format_exc())
            raise
        finally:
            # Stäng anslutningen
            if 'conn' in locals() and conn is not None:
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

import base64

def convert_image_to_base64(image_path):
    """Convert an image file to a base64-encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return ""

class HTMLTableGenerator:
    def __init__(self, data):
        self.data = data

    def generate_html_table(self):
        # Base64-strängar för bilderna
        images_base64 = {
            "sales_data_plot_WUSmRV.png": convert_image_to_base64("sales_data_plot_WUSmRV.png"),
            "sales_data_plot_WEUmRV.png": convert_image_to_base64("sales_data_plot_WEUmRV.png"),
            "sales_data_plot_USRW.png": convert_image_to_base64("sales_data_plot_USRW.png"),
            "sales_data_plot_EURV.png": convert_image_to_base64("sales_data_plot_EURV.png"),
            "sales_data_plot_USB2B.png": convert_image_to_base64("sales_data_plot_USB2B.png"),
            "sales_data_plot_EUB2B.png": convert_image_to_base64("sales_data_plot_EUB2B.png")
        }

        html = '''
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                @media only screen and (max-width: 600px) {
                    table {
                        width: 100%;
                        display: block;
                        overflow-x: auto;
                    }
                    thead {
                        display: none;
                    }
                    tr {
                        display: block;
                        margin-bottom: 10px;
                    }
                    td {
                        display: block;
                        text-align: right;
                        position: relative;
                        padding-left: 50%;
                    }
                    td::before {
                        content: attr(data-label);
                        position: absolute;
                        left: 0;
                        width: 45%;
                        padding-left: 10px;
                        white-space: nowrap;
                        font-weight: bold;
                    }
                }
            </style>
        </head>
        <body>
            <h2>Sales Data</h2>
            <table>
                <thead>
                    <tr>
                        <th>Sales channel</th>
                        <th>Quantity</th>
                    </tr>
                </thead>
                <tbody>
        '''

        for entry in self.data:
            category = entry['Category']
            quantity = entry.get('quantity', 0)  # Assuming 'quantity' is the correct key
            html += f'''
            <tr>
                <td>{category}</td>
                <td>{quantity}</td>
            </tr>
            '''

        html += '''
                </tbody>
            </table>
            <h2>Sales Data Charts</h2>
            <table>
                <tbody>
                    <tr>
                        <td><strong>Sales data US web last 30 days</strong></td>
                        <td><img src="data:image/png;base64,{0}" alt="Sales data US web last 30 days" style="width: 100%; max-width: 600px;"></td>
                    </tr>
                    <tr>
                        <td><strong>Sales data EU web last 30 days</strong></td>
                        <td><img src="data:image/png;base64,{1}" alt="Sales data EU web last 30 days" style="width: 100%; max-width: 600px;"></td>
                    </tr>
                    <tr>
                        <td><strong>Sales data US Reverb last 30 days</strong></td>
                        <td><img src="data:image/png;base64,{2}" alt="Sales data US Reverb last 30 days" style="width: 100%; max-width: 600px;"></td>
                    </tr>
                    <tr>
                        <td><strong>Sales data EU Reverb last 30 days</strong></td>
                        <td><img src="data:image/png;base64,{3}" alt="Sales data EU Reverb last 30 days" style="width: 100%; max-width: 600px;"></td>
                    </tr>
                    <tr>
                        <td><strong>Sales data US B2B last 30 days</strong></td>
                        <td><img src="data:image/png;base64,{4}" alt="Sales data US B2B last 30 days" style="width: 100%; max-width: 600px;"></td>
                    </tr>
                    <tr>
                        <td><strong>Sales data EU B2B last 30 days</strong></td>
                        <td><img src="data:image/png;base64,{5}" alt="Sales data EU B2B last 30 days" style="width: 100%; max-width: 600px;"></td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
        '''.format(
            images_base64.get("sales_data_plot_WUSmRV.png", ""),
            images_base64.get("sales_data_plot_WEUmRV.png", ""),
            images_base64.get("sales_data_plot_USRW.png", ""),
            images_base64.get("sales_data_plot_EURV.png", ""),
            images_base64.get("sales_data_plot_USB2B.png", ""),
            images_base64.get("sales_data_plot_EUB2B.png", "")
        )
        
        return html


def convert_none_to_zero(data_list):
    for data in data_list:
        for key, value in data.items():
            if value is None:
                data[key] = 0
    return data_list


def save_data_to_file(data, filename='data.txt'):
    """
    Sparar data till en textfil.

    Args:
        data (list of dict): Data som ska sparas i filen.
        filename (str): Namn på filen där datan ska sparas. Standard är 'data.txt'.
    """
    try:
        with open(filename, 'w') as file:
            # Konvertera varje ordbok till en sträng och skriv till filen
            for record in data:
                file.write(str(record) + '\n')
        print(f"Data har sparats till {filename}.")
    except Exception as e:
        print(f"Det gick inte att spara data till filen: {e}")



def get_yesterday_values(data: List[Dict[str, any]]) -> List[Dict[str, any]]:
    # Beräkna gårdagens datum
    today = datetime.strptime('2024-08-04', '%Y-%m-%d')
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Filtrera och omstrukturera data
    filtered_data = []
    for entry in data:
        category = entry['Category']
        if yesterday in entry:
            filtered_data.append({ 'Category': category, yesterday: entry[yesterday] })
    
    return filtered_data


class DataVisualizer:
    def __init__(self, data: List[Dict[str, any]]):
        self.data = data
        self.dates = self.get_dates()
    
    def get_dates(self) -> List[str]:
        """Return a sorted list of all dates present in the data."""
        dates = set()
        for entry in self.data:
            dates.update(date for date in entry.keys() if date != 'Category')
        return sorted(dates)

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class DataAnalyzer:
    def __init__(self, data: List[Dict[str, any]]):
        self.data = data

    def get_dates(self) -> List[str]:
        """Return a sorted list of all dates present in the data."""
        dates = set()
        for entry in self.data:
            dates.update(date for date in entry.keys() if date != 'Category')
        return sorted(dates)
    
    def filter_dates_to_mondays(self, dates):
        dates = pd.to_datetime(dates)
        mondays = dates[dates.to_series().dt.dayofweek == 0]
        return mondays

    def plot_data(self):
        # Definiera bildnamnen som variabler
        category_to_filename = {
            "Web US orders, RV excluded.": "WUSmRV",
            "US Reverb orders": "USRW",
            "Web EU orders, RV excluded.": "WEUmRV",
            "EU Reverb orders": "EURV",
            "US B2B orders": "USB2B",
            "EU B2B orders": "EUB2B"
        }
        
        # Filtrera och ordna datan baserat på de önskade kategorierna
        desired_categories = list(category_to_filename.keys())
        filtered_data = [entry for entry in self.data if entry['Category'] in desired_categories]
        ordered_data = sorted(filtered_data, key=lambda x: desired_categories.index(x['Category']))

        for category_data in ordered_data:
            category = category_data['Category']
            dates = [datetime.strptime(date, '%Y-%m-%d') for date in list(category_data.keys())[1:]]
            values = [category_data[date.strftime('%Y-%m-%d')] for date in dates]
            
            mondays = self.filter_dates_to_mondays([date.strftime('%Y-%m-%d') for date in dates])
            monday_dates_str = mondays.strftime('%Y-%m-%d')
            monday_dates = [datetime.strptime(date, '%Y-%m-%d') for date in monday_dates_str]
            monday_values = [category_data.get(date.strftime('%Y-%m-%d'), 0) for date in monday_dates]
            
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(dates, values, marker='o', label='All data')
            ax.plot(monday_dates, monday_values, 'ro', label='Mondays')
            
            ax.set_title(category)
            ax.set_xlabel('Date')
            ax.set_ylabel('Value')
            ax.grid(True)
            ax.set_xticks(dates)
            ax.set_xticklabels([date.strftime('%Y-%m-%d') for date in dates], rotation=45, ha='right')
            ax.set_xticks(monday_dates)
            ax.set_xticklabels([date.strftime('%Y-%m-%d') for date in monday_dates], rotation=45, ha='right')

            filename_key = category_to_filename.get(category)
            if filename_key:
                filename = f'sales_data_plot_{filename_key}.png'
                plt.tight_layout()
                plt.savefig(filename)
                plt.close()
            else:
                print(f"No filename defined for category: {category}")

        print("All plots saved successfully.")

if __name__ == "__main__":
    # Hämta den aktuella arbetskatalogen och ladda konfigurationer
    current_directory = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_directory, '.env')
    csv_path = os.path.join(current_directory, 'recipients.csv')
    sql_file_create_temp_table = os.path.join(current_directory, 'SQL_create_temp_table.sql')
    sql_file_get_data = os.path.join(current_directory, 'SQL_getSalesDataArray.sql')
    sql_file_remove_temp_table = os.path.join(current_directory, 'SQL_delete_temp_table.sql')

    if not os.path.exists(dotenv_path):
        logging.error(".env-filen hittades inte i katalogen: %s", current_directory)
        raise FileNotFoundError(f".env-filen hittades inte i katalogen: {current_directory}")

    # Ladda konfigurationer
    config_loader = ConfigLoader(dotenv_path)
    config = config_loader.load_config()

    # Hämta data från databasen
    db_fetcher = DatabaseFetcher(config['db_server'], config['db_name'], config['db_user'], config['db_password'])
    try:
        logging.info("Startar skapa temp tabell")
        db_fetcher.execute_sql(sql_file_create_temp_table)

        logging.info("Startar Sök i temp tabell")
        data = db_fetcher.execute_sql(sql_file_get_data, fetch_results=True)
        logging.info(f'Hämtade data: {data}')

    except Exception as e:
        logging.error(f'Något gick fel: {e}')

    # Ändra all NULL till 0
    converted_data = convert_none_to_zero(data)

    # Ta endast fram datat som gäller för igår
    yesterdays_sales = get_yesterday_values(converted_data)
    print(yesterdays_sales)

    # Skapa grafer per kategori
    analyzer = DataAnalyzer(converted_data)
    analyzer.plot_data()

    # Vänta och verifiera att bilderna skapades
    image_paths = [
        "sales_data_plot_WUSmRV.png",
        "sales_data_plot_WEUmRV.png",
        "sales_data_plot_USRW.png",
        "sales_data_plot_EURV.png",
        "sales_data_plot_USB2B.png",
        "sales_data_plot_EUB2B.png"
    ]
    wait_for_images_to_be_created(image_paths)

    # Konvertera bilder till base64
    base64_images = {path: convert_image_to_base64(path) for path in image_paths}

    for path, base64_str in base64_images.items():
        if base64_str:
            print(f"Base64 string for {path} successfully generated.")
        else:
            print(f"Base64 string for {path} is empty.")

    # Generera HTML-tabell
    generator = HTMLTableGenerator(yesterdays_sales)
    html_content = generator.generate_html_table()

    # Läs mottagare från CSV
    recipients = read_recipients(csv_path)

    # Bygg e-postmeddelandet
    yesterday = datetime.now() - timedelta(1)
    formatted_date = yesterday.strftime('%Y-%m-%d')
    subject = f"Sales data from {formatted_date}"
    message_html = f"<p>This is the sales data from {formatted_date}</p>{html_content}"
    
    # Skicka e-postmeddelanden
    send_emails(config, recipients, subject, message_html)
    logging.info(f'Subject: {subject}')
    logging.info(f'Mail message_html: {message_html}')