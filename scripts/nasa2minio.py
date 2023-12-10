from minio import Minio
from urllib.request import urlopen

MINIO_ENDPOINT = 'minio.ifpbapps.online'
ACCESS_KEY = 'REDACTED_ACCESS_KEY'
SECRET_KEY = 'REDACTED_SECRET_KEY'
BUCKET_NAME = 'indimap'

files_to_upload = [{
    'focos_modis.csv': 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/REDACTED_FIRMS_KEY/MODIS_NRT/BRA/3'},{
    'focos_noaa_20.csv': 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/REDACTED_FIRMS_KEY/VIIRS_NOAA20_NRT/BRA/3'},{
    'focos_s_npp.csv': 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/REDACTED_FIRMS_KEY/VIIRS_SNPP_NRT/BRA/3'}
]


minio_client = Minio(
    endpoint=MINIO_ENDPOINT, access_key=ACCESS_KEY, secret_key=SECRET_KEY,
)

if minio_client:
    print(f'Conectado com sucesso ao {MINIO_ENDPOINT}')

if not minio_client.bucket_exists(BUCKET_NAME):
    print(f'Bucket {BUCKET_NAME} não existe. Tentando criar...')
    minio_client.make_bucket(BUCKET_NAME)

for file_info in files_to_upload:
    for filename, url in file_info.items():
        minio_client.remove_object(BUCKET_NAME, filename)
        print(f'Tentando remover o arquivo {BUCKET_NAME}/{filename}')

        file_content = urlopen(url=url)
        upload_result = minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=filename,
            data=file_content,
            length=-1,
            part_size=10*1024*1024,
        )
        print('Criado o objeto {0} (etag={1}, version_id={2})'.format(
            upload_result.object_name, upload_result.etag, upload_result.version_id
        ))

