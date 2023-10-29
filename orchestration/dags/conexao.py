import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from urllib.parse import quote_plus
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_pass = os.getenv('DB_PASS')



def geConnection(): 
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host,port=db_port)
    return conn

def geConnectionSqlAlchemyGetEngine():
    db_pass_encoded = quote_plus(db_pass)
    url_conexao = f'postgresql://{db_user}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(url_conexao)
    return engine

