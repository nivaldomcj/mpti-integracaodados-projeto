from trino.dbapi import connect, Cursor
from trino.auth import BasicAuthentication

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.engine import URL
from sqlalchemy.engine import Connection, Engine

TRINO_HOST = 'trino.ifpbapps.online'
TRINO_PORT = 443
TRINO_USER = 'trino'
TRINO_PASS = 'REDACTED_TRINO_PASS'

YUGABYTE_HOST = 'yugabyte.ifpbapps.online'
YUGABYTE_PORT = 5433
YUGABYTE_DB = 'yugabyte'
YUGABYTE_USER = 'yugabyte'
YUGABYTE_PASS = 'REDACTED_YUGABYTE_PASS'

# Mude aqui qual é o bucket do minio onde estão os arquivos
BUCKET_NAME = 'indimap'
SCHEMA_NAME = 'data'


def send_table_to_yugabyte(trino_cursor: Cursor, 
                           yugabyte_connection: Connection, 
                           table_name: str):
    # TODO: ler os registros do trino
    trino_cursor.execute(
        f'SELECT * FROM "{BUCKET_NAME}"."{SCHEMA_NAME}"."{table_name}"')
    rows = trino_cursor.fetchall()


    # for row in rows:
    #     row_dict = dict(zip([desc[0] for desc in trino_cursor.description], row))
    #     country_id = row_dict['country_id']
    #     print(country_id)

    print([desc[0] for desc in trino_cursor.description])
    # TODO: conectar ao yugabyte e jogar esses registros no yugabyte
    # result = yugabyte_connection.execute(text('SELECT * FROM ?'))
    pass


def create_focos_table(cursor: Cursor, table_name: str):
    # Lembre-se: CSV não tem tipos de dados, por isso aqui tudo é varchar
    cursor.execute(
        f'create table "{BUCKET_NAME}"."{SCHEMA_NAME}".{table_name} ('
        f"    country_id varchar,"
        f"    latitude varchar,"
        f"    longitude varchar,"
        f"    brightness varchar,"
        f"    scan varchar,"
        f"    track varchar,"
        f"    acq_date varchar,"
        f"    acq_time varchar,"
        f"    satellite varchar,"
        f"    instrument varchar,"
        f"    confidence varchar,"
        f"    version varchar,"
        f"    bright_t31 varchar,"
        f"    frp varchar,"
        f"    daynight varchar"
        f") with ("
        f"    format = 'csv',"
        f"    skip_header_line_count = 1,"
        f"    external_location = 's3a://{BUCKET_NAME}/'"
        f")"
    )


def connect_to_yugabyte():
    yugabyte_url = URL.create(
        drivername='postgresql',
        host=YUGABYTE_HOST,
        port=YUGABYTE_PORT,
        username=YUGABYTE_USER,
        password=YUGABYTE_PASS,
        database=YUGABYTE_DB,
    )
    yugabyte_engine = create_engine(yugabyte_url)
    yugabyte_connection = yugabyte_engine.connect()
    if yugabyte_engine and yugabyte_connection:
        print(f'Conectado com sucesso ao YugabyteDB via ({YUGABYTE_HOST})')
    return yugabyte_engine, yugabyte_connection


def connect_to_trino():
    trino_connection = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        auth=BasicAuthentication(TRINO_USER, TRINO_PASS),
        http_scheme='https',
    )
    trino_cursor = trino_connection.cursor()
    if trino_connection and trino_cursor:
        print(f'Conectado com sucesso ao Trino via ({TRINO_HOST})')
    return trino_connection, trino_cursor


def main():
    trino_connection, trino_cursor = connect_to_trino()
    yugabyte_engine, yugabyte_connection = connect_to_yugabyte()

    """
    Defina aqui os scripts para criação da namespace para o Trino acessar o Minio
    Se você tem um arquivo "example.csv" e quer acessar ele com SQL pelo Trino,
    primeiro é necessário criar uma namespace (table) com os dados das colunas.
    Então, o nome será, por ex: `CREATE TABLE indimap.data.example`.
    
    Lembre que aqui estamos considerando que o SCHEMA já foi criado anteriormente!
    
    Isso só precisa ser feito na primeira vez que for acessar esse arquivo,
    para que o Trino adicione os metadados lá no bucket. Depois defina como "False".
    
    Você precisará fazer isso para cada um dos arquivos que deseja acessar.
    """
    # create_focos_table(trino_cursor, 'focos_s_npp')
    # create_focos_table(trino_cursor, 'focos_noaa_20')
    # create_focos_table(trino_cursor, 'focos_modis')
    # trino_cursor.execute('drop table indimap.data.focos_noaa_20')
    # trino_cursor.execute('drop table indimap.data.focos_s_npp')

    for table_name in ['focos_s_npp', 'focos_noaa_20', 'focos_modis']:
        send_table_to_yugabyte(trino_cursor, yugabyte_connection, table_name)


    print("Finished! :D")

if __name__ == '__main__':
    main()
