# Pipeline de Dados: Meio-ambiente e Dados Geoespaciais

## Sobre o projeto

(A fazer: Descrever o projeto)

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
- [Configurar o Argo](cicd/setup.sh)
- [Configurar o MinIO](datalake/setup.sh)
- [Configurar o Airflow](orchestration/setup.sh)
- (A fazer: Colocar as instruções de outras partes da config. do projeto)
- 

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

## URL de cada serviço
- [Argo](https://localhost:8080/)
- [MinIO](http://127.0.0.1:9000)
- [Airflow](http://127.0.0.1:8001)


## Autores

- Laerty Santos da Silva
- Jose Mario Fraga Miranda
- Nivaldo Mariano de Carvalho Junior
