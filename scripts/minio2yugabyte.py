from datetime import datetime, timedelta
from shapely.wkt import loads

import pandas as pd
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from geopandas import GeoDataFrame
from sqlalchemy.orm import declarative_base, sessionmaker
from trino.dbapi import connect, Cursor
from trino.auth import BasicAuthentication
import geopandas as gpd
from sqlalchemy.sql import text
from sqlalchemy import create_engine, Column, Integer, VARCHAR, Numeric, DateTime
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.sql import text
from sqlalchemy.engine import URL
from sqlalchemy.engine import Connection, Engine
from shapely.geometry import Point

TRINO_HOST = 'trino.ifpbapps.online'
TRINO_PORT = 443
TRINO_USER = 'trino'
TRINO_PASS = 'REDACTED_TRINO_PASS'


YUGABYTE_HOST = 'yugabyte.ifpbapps.online'
YUGABYTE_PORT = 5433
YUGABYTE_DB = 'indimap'
YUGABYTE_USER = 'yugabyte'
YUGABYTE_PASS = 'REDACTED_YUGABYTE_PASS'

BUCKET_NAME = 'indimap'
SCHEMA_NAME = 'data'

Base = declarative_base()
class Focos(Base):
    __tablename__ = 'focos'
    __table_args__ = {'schema': 'public'}
    gid = Column(Integer, primary_key=True)
    datahora_texto = Column(VARCHAR(25))
    satelite = Column(VARCHAR(25))
    estado = Column(VARCHAR(30))
    municipio = Column(VARCHAR(80))
    bioma = Column(VARCHAR(25))
    frp = Column(Numeric)
    geom = Column(Geometry(geometry_type='POINT', srid=4674))
    id_inpe = Column(VARCHAR(60))
    datahora = Column(DateTime, nullable=True)
    terra_id = Column(Integer)

def getDataHoraNasa(data_hora_str):
    data_str, minutos_segundos_str = data_hora_str.split(',')
    data_formatada = datetime.strptime(data_str, "%Y-%m-%d")
    minutos_segundos = int(minutos_segundos_str)
    tempo_formatado = timedelta(minutes=minutos_segundos // 60, seconds=minutos_segundos % 60)
    data_hora_formatada = data_formatada + tempo_formatado
    return str(data_hora_formatada)
def get_dados_inicias():
    sql = 'select gid, terrai_cod, terrai_nom, geom from terras_indigenas;'
    df_postgis = gpd.GeoDataFrame.from_postgis(text(sql), yugabyte_connection)
    return df_postgis

def formatar_datahora2(data_hora):
    data_hora_str = pd.Timestamp(data_hora).strftime('%Y-%m-%d %H:%M:%S')
    dt = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
    novo_formato = dt.strftime("%Y/%m/%d %H:%M:%S")
    return novo_formato

def get_pre_list(rows:list, trino_cursor:Cursor):
    lista_pontos = []
    for row in rows:
        row_dict = dict(zip([desc[0] for desc in trino_cursor.description], row))
        sat = '-'
        if row_dict['instrument'] == 'MODIS':
            sat = row_dict['instrument'] + ' - ' + row_dict['satellite']
        if row_dict['instrument'] == 'VIIRS':
            if row_dict['satellite'] == '1':
                sat = 'VIIRS - NOAA-20'
            else:
                sat = 'VIIRS - S-NPP'
        obj = {"id_inpe": row_dict['latitude'] + '-' + row_dict['longitude'] + '-' + row_dict["acq_date"] + '-' + row_dict["acq_time"],
               "satelite": sat,
               "frp": row_dict["frp"],
               "data_hora_gmt": getDataHoraNasa(f"{row_dict['acq_date']},{row_dict['acq_time']}"),
               "geom": Point(float(row_dict['longitude']), float(row_dict['latitude']))
               }
        lista_pontos.append(obj)

    return lista_pontos


def data_to_db(df: GeoDataFrame):

    lista_registros = []
    for index, row in df.iterrows():
        geom = from_shape(loads('POINT({} {})'.format(Point(row["geom"]).x, Point(row["geom"]).y)), srid=4674)
        objInsert = {"id_inpe": row['id_inpe'],
                     "satelite": row['satelite'],
                     "datahora": row['data_hora_gmt'],
                     "frp": row["frp"],
                     "datahora_texto": formatar_datahora2(row['data_hora_gmt']),
                     "terra_id": row['gid'],
                     "geom": geom
                     }
        lista_registros.append(objInsert)
    if (len(lista_registros) > 0):
        Session = sessionmaker(bind=yugabyte_connection)
        session = Session()
        insert_stmt = insert(Focos).values(lista_registros)
        on_conflict_stmt = insert_stmt.on_conflict_do_nothing()
        session.execute(on_conflict_stmt)
        session.commit()

    return True

def send_table_to_yugabyte(trino_cursor: Cursor, 
                           yugabyte_connection: Connection, 
                           table_name: str):
    # TODO: ler os registros do trino
    trino_cursor.execute(
        f'SELECT * FROM "{BUCKET_NAME}"."{SCHEMA_NAME}"."{table_name}"')
    rows = trino_cursor.fetchall()

    lista_focos = get_pre_list(rows, trino_cursor)
    df_api = gpd.GeoDataFrame(lista_focos, geometry='geom')
    df_api.crs = 'EPSG:4674'
    df_focos_terras = df_api.sjoin(df_ti)
    df_focos_terras.crs = 'EPSG:4674'
    r3 = data_to_db(df_focos_terras)
    print(r3)



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

def finish_processo():
    Session = sessionmaker(bind=yugabyte_connection)
    session = Session()
    try:
        sql_statement = text("select public.indimap_atualiza_cidades_focos();")
        session.execute(sql_statement)
        session.commit()
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        session.close()


def main():
    trino_connection, trino_cursor = connect_to_trino()
    global yugabyte_engine, yugabyte_connection
    yugabyte_engine, yugabyte_connection = connect_to_yugabyte()

    global df_ti
    df_ti = get_dados_inicias()
    df_ti.crs = 'EPSG:4674'
    for table_name in ['focos_s_npp', 'focos_noaa_20', 'focos_modis']:
        send_table_to_yugabyte(trino_cursor, yugabyte_connection, table_name)

    finish_processo()
    print("Finished! :D")

if __name__ == '__main__':
    main()
