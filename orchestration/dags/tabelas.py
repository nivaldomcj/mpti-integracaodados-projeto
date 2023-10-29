from geoalchemy2 import Geometry
from sqlalchemy import TIMESTAMP, BigInteger, Boolean, DateTime, Float, String, Text, create_engine, Column, Integer, VARCHAR, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base


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
    id_inpe = Column(VARCHAR(60), unique=True)
    datahora = Column(DateTime, nullable=True)
    terra_id = Column(Integer)



class TerrasIndigenas(Base):
    __tablename__ = 'terras_indigenas'
    __table_args__ = {'schema': 'public'}
    gid = Column(Integer, primary_key=True, autoincrement=True)
    __gid = Column(Float)
    terrai_cod = Column(Float)
    terrai_nom = Column(String(100))
    etnia_nome = Column(String(150))
    municipio_ = Column(String(200))
    uf_sigla = Column(String(10))
    superficie = Column(Numeric)
    fase_ti = Column(String(20))
    modalidade = Column(String(80))
    reestudo_t = Column(String(20))
    cr = Column(String(60))
    faixa_fron = Column(String(5))
    undadm_cod = Column(String(20))
    undadm_nom = Column(String(80))
    undadm_sig = Column(String(20))
    dominio_un = Column(String(1))
    data_atual = Column(String(20))
    epsg = Column(Float)
    geom = Column(Geometry('MULTIPOLYGON', srid=4674))
    ultimo_id_foco = Column(Integer, default=0)
    ultima_data_deter = Column(String(20))
    ultima_data_deter_cerrado = Column(String(20))
    ultimo_alerta_id_mapbiomas = Column(Integer, default=0)


class Alertas_MapBiomas(Base):
    __tablename__ = 'alertas_mapbiomas'
    __table_args__ = {'schema': 'public'}
    codealerta = Column(Integer, primary_key=True)
    fonte = Column(String(50))
    bioma = Column(String(20))
    estado = Column(String(30))
    municipio = Column(String(60))
    areaha = Column(Numeric)
    anodetec = Column(Numeric)
    datadetec = Column(String(15))
    dtimgant = Column(Date)
    dtimgdep = Column(Date)
    vpressao = Column(String(20))
    geom = Column(Geometry('MULTIPOLYGON', srid=4674), nullable=True)

class Alertas_deter(Base):
    __tablename__ = 'alertas_deter'
    __table_args__ = {'schema': 'public'}
    gid = Column(Integer, primary_key=True, autoincrement=True)
    classname = Column(String(30), nullable=True)
    quadrant = Column(String(5), nullable=True)
    path_row = Column(String(10), nullable=True)
    view_date = Column(Date, nullable=True)
    sensor = Column(String(10), nullable=True)
    satellite = Column(String(13), nullable=True)
    areauckm = Column(Numeric, nullable=True)
    uc = Column(String(80), nullable=True)
    areamunkm = Column(Numeric, nullable=True)
    municipali = Column(String(50), nullable=True)
    geocodibge = Column(String(7), nullable=True)
    uf = Column(String(2), nullable=True)
    geom = Column(Geometry('MULTIPOLYGON', srid=4674), nullable=True)

class Alertas_deter_cerrado(Base):
    __tablename__ = 'alertas_deter_cerrado'
    __table_args__ = {'schema': 'public'}
    gid = Column(Integer, primary_key=True, autoincrement=True)
    classname = Column(String(30), nullable=True)
    quadrant = Column(String(5), nullable=True)
    path_row = Column(String(10), nullable=True)
    view_date = Column(Date, nullable=True)
    sensor = Column(String(10), nullable=True)
    satellite = Column(String(13), nullable=True)
    areauckm = Column(Numeric, nullable=True)
    uc = Column(String(80), nullable=True)
    areamunkm = Column(Numeric, nullable=True)
    municipali = Column(String(50), nullable=True)
    geocodibge = Column(String(7), nullable=True)
    uf = Column(String(2), nullable=True)
    geom = Column(Geometry('MULTIPOLYGON', srid=4674), nullable=True)

