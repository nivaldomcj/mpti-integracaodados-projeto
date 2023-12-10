from minio import Minio
from urllib.request import urlopen

MINIO_ENDPOINT = 'minio.ifpbapps.online'
ACCESS_KEY = 'REDACTED_ACCESS_KEY'
SECRET_KEY = 'REDACTED_SECRET_KEY'

# Mude aqui qual é o bucket que deve ser enviado os arquivos
BUCKET_NAME = 'indimap-test'

# Arquivos que vamos enviar para o bucket vindos da web
# Chave => Nome do arquivo | Valor => URL do arquivo
files_to_upload = {
    'example.csv': \
        'https://gist.githubusercontent.com/nivaldomcj/66e6404464de10fb3ce19ba361908e5b/raw/465d38bd1b9b55a83b77831649500b667cc7ffb6/example.csv'
}

# Foi preciso criar um ACCESS_KEY e SECRET_KEY no Minio Console,
# ver: https://minio-console.ifpbapps.online/access-keys
minio_client = Minio(
    endpoint=MINIO_ENDPOINT, access_key=ACCESS_KEY, secret_key=SECRET_KEY,
)

if minio_client:
    print(f'Conectado com sucesso ao {MINIO_ENDPOINT}')

if not minio_client.bucket_exists(BUCKET_NAME):
    print(f'Bucket {BUCKET_NAME} não existe. Tentando criar...')
    minio_client.make_bucket(BUCKET_NAME)

for filename in files_to_upload:
    minio_client.remove_object(BUCKET_NAME, filename)
    print(f'Tentando remover o arquivo {BUCKET_NAME}/{filename}')

    # ver: https://min.io/docs/minio/linux/developers/python/API.html
    file_content = urlopen(url=files_to_upload[filename])
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

