from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import os
import boto3

minio_access_key = "REDACTED_MINIO_ACCESS_KEY"
minio_secret_key = "REDACTED_MINIO_SECRET_KEY"
minio_endpoint = "https://endereço_do_seu_minio"
minio_bucket_name = "seu_bucket_no_minio"
minio_object_name = "dashboard_alerts-shapefile.zip"


default_args = {
    "owner": "seu_nome",
    "start_date": datetime(2023, 1, 1),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "schedule_interval": timedelta(weeks=1),
}

def download_and_upload_to_minio():
    # URL do arquivo ZIP a ser baixado
    file_url = "https://storage.googleapis.com/alerta-public/dashboard/downloads/dashboard_alerts-shapefile.zip"

    # Caminho para onde o arquivo será baixado temporariamente
    temp_file_path = "/tmp/dashboard_alerts-shapefile.zip"

    # Fazer o download do arquivo ZIP
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(temp_file_path, "wb") as file:
            file.write(response.content)

        # Inicializar o cliente do Minio
        minio_client = boto3.client(
            "s3",
            aws_access_key_id=minio_access_key,
            aws_secret_access_key=minio_secret_key,
            endpoint_url=minio_endpoint,
            region_name="us-east-1"  # Altere para a região correta
        )

        # Enviar o arquivo para o Minio
        try:
            minio_client.upload_file(temp_file_path, minio_bucket_name, minio_object_name)
        except Exception as e:
            raise Exception("Erro ao enviar o arquivo para o Minio: " + str(e))
        finally:
            # Remover o arquivo temporário
            os.remove(temp_file_path)

# Crie a DAG
dag = DAG(
    "download_and_upload_to_minio",
    default_args=default_args,
    description="DAG para baixar um arquivo ZIP e enviá-lo para o Minio",
    schedule_interval=timedelta(weeks=1),
)

# Crie uma tarefa na DAG que executa a função de download_and_upload_to_minio
task = PythonOperator(
    task_id="download_and_upload_task",
    python_callable=download_and_upload_to_minio,
    provide_context=True,
    dag=dag,
)

if __name__ == "__main__":
    dag.cli()
