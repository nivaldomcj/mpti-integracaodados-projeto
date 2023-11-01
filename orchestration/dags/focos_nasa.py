# -*- coding: utf-8 -*-
import csv
import geopandas as gpd
import conexao
import requests
import tabelas
from shapely.geometry import Point
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import sessionmaker
import uteis
from geoalchemy2.shape import from_shape
from shapely.wkt import loads
import time
from sqlalchemy.sql import text

start_time = time.time()
engine = conexao.geConnectionSqlAlchemyGetEngine()

def get_dados_inicias():
    sql = 'select gid, terrai_cod, terrai_nom, geom from public.terras_indigenas'
    conn = engine.connect()
    df_postgis = gpd.GeoDataFrame.from_postgis(text(sql), conn)
    return df_postgis

def create_url_list():
    BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/country/csv/REDACTED_FIRMS_KEY"
    COUNTRY = "BRA"
    DAYS = "3"
    lista_urls = [
        {"instrumento": "MODIS", "url": f"{BASE_URL}/MODIS_NRT/{COUNTRY}/{DAYS}"},
        {"instrumento": "VIIRS", "satelite": "NOAA-20", "url": f"{BASE_URL}/VIIRS_NOAA20_NRT/{COUNTRY}/{DAYS}"},
        {"instrumento": "VIIRS", "satelite": "S-NPP", "url": f"{BASE_URL}/VIIRS_SNPP_NRT/{COUNTRY}/{DAYS}"}
    ]
    return lista_urls

def execute_function_postgres():
    global Session
    try:
        Session = sessionmaker(bind=engine)
        session_fun = Session()
        sql_fun = "SELECT public.indimap_atualiza_cidades_focos();"
        session_fun.execute(text(sql_fun))
        session_fun.commit()
        print("Função executada com sucesso!")

    except Exception as e:
        print(f"1Erro ao executar a função indimap_atualiza_cidades_focos: {e}")

def csv_to_json(csv_data, item):
    csv_reader = csv.DictReader(csv_data.splitlines())
    lista_pontos = []
    for row in csv_reader:
        if "satelite" in item:
            sat = item["instrumento"] + " - " + item["satelite"]
        else:
            sat = item["instrumento"] + " - " + row["satellite"]
            
        obj = {"id_inpe": row['latitude'] + '-' + row['longitude'] + '-' + row["acq_date"] + '-' + row["acq_time"],
               "satelite": sat,
               "frp": row["frp"],
               "data_hora_gmt": uteis.getDataHoraNasa(f"{row['acq_date']},{row['acq_time']}"),
               # "data_hora_gmt": datetime.strptime(f"{row['acq_date']} {row['acq_time'][:2]}:{row['acq_time'][2:]}", "%Y-%m-%d %H:%M"),
               "geom": Point(float(row['longitude']), float(row['latitude']))
               }
        lista_pontos.append(obj)
    return  lista_pontos

df_postgis_terras_indigenas = get_dados_inicias()
lista_de_urls = create_url_list()


def salva_focos_ti(df_focos_terras):
    global Session
    lista_registros = []
    for index, row in df_focos_terras.iterrows():
        geom = from_shape(loads('POINT({} {})'.format(Point(row["geom"]).x, Point(row["geom"]).y)), srid=4674)
        objInsert = {"id_inpe": row['id_inpe'],
                     "satelite": row['satelite'],
                     "datahora": row['data_hora_gmt'],
                     "frp": row["frp"],
                     "datahora_texto": uteis.formatar_datahora2(row['data_hora_gmt']),
                     "terra_id": row['gid'],
                     "geom": geom
                     }
        lista_registros.append(objInsert)
    if (len(lista_registros) > 0):
        Session = sessionmaker(bind=engine)
        session = Session()
        insert_stmt = insert(tabelas.Focos).values(lista_registros)
        on_conflict_stmt = insert_stmt.on_conflict_do_nothing()
        session.execute(on_conflict_stmt)
        session.commit()
        print("REGISTROS INSERIDOS:", len(lista_registros))


def filtra_apenas_focos_ti(lista_pontos, df_postgis_terras_indigenas):
    global df_focos_terras
    df_api = gpd.GeoDataFrame(lista_pontos, geometry='geom')
    df_api.crs = 'EPSG:4674'
    df_focos_terras = df_api.sjoin(df_postgis_terras_indigenas)
    df_focos_terras.crs = 'EPSG:4674'
    return df_focos_terras

for item in lista_de_urls:
    response = requests.get(item["url"])
    data_list = []
    csv_data = response.text
    lista_pontos = csv_to_json(csv_data, item)

    if len(lista_pontos) > 0:
        df_focos_terras=filtra_apenas_focos_ti(lista_pontos, df_postgis_terras_indigenas)
        salva_focos_ti(df_focos_terras)
    else:
        print("NENHUM REGISTRO NOVO")

time.sleep(20)
execute_function_postgres()

end_time = time.time()
total_time = end_time - start_time
print('Tempo de execução em segundo: {} '.format(str(total_time)))
print('PROCESSAMENTO FINALIZADO!')