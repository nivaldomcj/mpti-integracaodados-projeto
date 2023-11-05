#adiciona e startar o serviço do minio
sudo systemctl enable minio.service
sudo systemctl start minio.service

# criar o namespace "datalake" no cluster kubernetes do minikube
kubectl create namespace datalake

# no arquivo minio.yaml, altere o "resources.requests.memory"
# para um valor de memória adequado para sua máquina

# aplicar a configuração do argo para subir o minio
kubectl apply -f ./datalake/minio.yaml

# acompanhe via Argo a instalação do Minio ser finalizada
# use o comando abaixo para fazer o port forwarding da aplicação
kubectl port-forward svc/minio 9000:9000 -n datalake & kubectl port-forward svc/minio-console 9001:9001 -n datalake &