# use o comando abaixo para fazer o port forwarding da aplicação
kubectl port-forward svc/airflow-web 8001:8080 -n orchestrator

# URL de interface do Airflow: http://localhost:8001/
# usuário: admin | senha: admin
