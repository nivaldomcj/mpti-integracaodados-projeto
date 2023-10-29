# use o comando abaixo para fazer o port forwarding da aplicação
# porta 9001 => acessar o console do minio via navegador
# porta 9000 => acessar o minio via api/código
kubectl port-forward svc/minio 9000:9000 -n datalake & kubectl port-forward svc/minio-console 9001:9001 -n datalake

# URL de interface do Minio: http://localhost:9001
# usuário: root | senha: minio123
