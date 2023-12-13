# Pipeline de Dados: Meio-ambiente e Dados Geoespaciais

## Sobre o projeto

Este projeto coleta focos de calor detectados por satélite no Brasil e guarda apenas os focos que caem dentro de terras indígenas.

Os dados vêm da API FIRMS da NASA. A pipeline lê os instrumentos MODIS e VIIRS (satélites NOAA-20 e S-NPP), sempre com os últimos 3 dias. Cada foco passa por uma junção espacial (GeoPandas, EPSG:4674) com a tabela `terras_indigenas`. Os focos que sobram são gravados na tabela `public.focos`. No fim de cada carga, a pipeline executa a função SQL `indimap_atualiza_cidades_focos()`.

## Requisitos do projeto

- [Linux](https://distrochooser.de/), MacOS ou [Windows com WSL](https://learn.microsoft.com/pt-br/windows/wsl/install)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Helm](https://helm.sh/docs/intro/install/)
- [k9s (opcional)](https://k9scli.io/)
- [Interface CLI do Argo (argocd)](https://argo-cd.readthedocs.io/en/stable/cli_installation/)

## Configurando o projeto

- Instalar o git e as ferramentas necessárias
- Fazer o clone deste repositório na sua máquina
- [Iniciar o Minikube](start_minikube.sh) (4 CPUs e 8 GB de memória)
- [Configurar o Argo](cicd/setup.sh)
- [Configurar o MinIO](datalake/setup.sh)
- [Configurar o Airflow](orchestration/setup.sh)

Cada `setup.sh` traz comentários com os ajustes necessários. Um exemplo é o repositório das DAGs em `orchestration/airflow.yaml`. O `run.sh` de cada pasta refaz o `port-forward` e lista o usuário padrão do serviço.

Para rodar os scripts da pasta `scripts/`, instale as dependências com `pip install -r scripts/requirements.txt`. O `minio2yugabyte.py` exige a versão 1.4.49 do SQLAlchemy.

## Descrição da pipeline

Essa é uma descrição simplificada da pipeline:

```
⚙️ CI/CD
    📦 Argo
⚙️ Data Lake
    📦 Minio
⚙️ Orchestration
    📦 Airflow
```

Existem dois caminhos para a mesma carga de dados.

1. **DAG do Airflow** (`orchestration/dags/focos_nasa_dag.py`). Roda a cada hora, baixa os três CSVs da NASA, filtra os focos em terras indígenas e grava em `public.focos`. Em caso de falha, tenta de novo uma vez após 10 minutos. Só uma execução fica ativa por vez.
2. **Scripts** (`scripts/`). O `nasa2minio.py` baixa os CSVs para o bucket `indimap` do MinIO. O `minio2yugabyte.py` lê esses arquivos pelo Trino (tabelas `focos_modis`, `focos_noaa_20` e `focos_s_npp`), filtra os focos e grava no YugabyteDB.

## URL de cada serviço

- [Argo](https://localhost:8080/)
- MinIO: [console](http://localhost:9001) e API em `http://localhost:9000`
- [Airflow](http://localhost:8001)

O Trino e o YugabyteDB são serviços externos. Eles não sobem no Minikube.

## Estado atual

O projeto está incompleto.

- O `minio2yugabyte.py` é o último passo escrito e ainda não virou uma DAG.
- As credenciais do Trino, do YugabyteDB e do MinIO, e a chave da API da NASA, estão escritas no código. Elas devem ir para variáveis de ambiente.

## Autores

- Laerty Santos da Silva
- Jose Mario Fraga Miranda
- Nivaldo Mariano de Carvalho Junior
