from datetime import datetime, timedelta
import os
import platform
import pandas as pd
import re
from unidecode import unidecode
from gtts import gTTS

import os
import requests
import traceback
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def formatar_datahora(data_hora):
    data_hora_str = pd.Timestamp(data_hora).strftime('%Y-%m-%d %H:%M:%S%z')
    dt = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S%z")
    novo_formato = dt.strftime("%Y/%m/%d %H:%M:%S")
    return novo_formato

def formatar_datahora2(data_hora):
    data_hora_str = pd.Timestamp(data_hora).strftime('%Y-%m-%d %H:%M:%S')
    dt = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
    novo_formato = dt.strftime("%Y/%m/%d %H:%M:%S")
    return novo_formato

def getDataHoraNasa(data_hora_str):
    data_str, minutos_segundos_str = data_hora_str.split(',')
    data_formatada = datetime.strptime(data_str, "%Y-%m-%d")
    minutos_segundos = int(minutos_segundos_str)
    tempo_formatado = timedelta(minutes=minutos_segundos // 60, seconds=minutos_segundos % 60)
    data_hora_formatada = data_formatada + tempo_formatado
    return data_hora_formatada


def getPlataforma(nome_arquivo):
    if platform.system() == "Linux":
        return '/var/aplicacaoes/indimap/indimap_py/logs/'+nome_arquivo
    elif platform.system() == "Windows":
        return 'logs/'+nome_arquivo
    else:
        return nome_arquivo


def getPlataformaDownload():
    if platform.system() == "Linux":
        return '/var/aplicacaoes/indimap/indimap_py/downloads/'
    elif platform.system() == "Windows":
        return os.path.abspath('../../airflow/dags')+ '\downloads\\'
    else:
        return '/downloads/'


def getPath(nome_arquivo):
    if platform.system() == "Linux":
        return '/var/aplicacaoes/indimap/indimap_py/'+nome_arquivo
    elif platform.system() == "Windows":
        return 'D:\dev\mestrado\indimap\indimap_py\\'+nome_arquivo
    else:
        return nome_arquivo
    
