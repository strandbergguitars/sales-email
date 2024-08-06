import os
from dotenv import load_dotenv
import pyodbc
import logging

# Konfigurera loggning
logging.basicConfig(filename='sql.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Startar scriptet och laddar miljövariabler')

# Ladda in miljövariabler från .env-filen
load_dotenv()

DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

logging.info(f'Använder DB_SERVER: {DB_SERVER}, DB_NAME: {DB_NAME}, DB_USER: {DB_USER}')

try:
    # Skapa anslutningssträngen
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"

    # Anslut till databasen
    logging.info('Försöker ansluta till databasen')
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    logging.info('Anslutning till databasen lyckades')
except Exception as e:
    logging.error(f'Kunde inte ansluta till databasen: {e}')
    raise

try:
    # Läs SQL-frågan från filen sql.sql
    with open('getinstruments.sql', 'r') as file:
        sql_query = file.read()
    logging.info(f'Läste SQL-frågan: {sql_query}')

    # Ställ SQL-frågan
    logging.info('Ställer SQL-frågan')
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    logging.info('SQL-frågan kördes framgångsrikt')

    # Bearbeta resultatet
    results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    logging.info(f'Hämtade resultat: {results}')

    # Visa resultatet
    print("SQL-fråga resultat:")
    for result in results:
        print(result)
        logging.info(f'Resultat rad: {result}')
except Exception as e:
    logging.error(f'Fel vid körning av SQL-frågan: {e}')
finally:
    # Stäng anslutningen
    conn.close()
    logging.info('Databasanslutningen stängdes')