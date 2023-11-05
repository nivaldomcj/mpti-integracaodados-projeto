# criar o namespace "orchestrator" no cluster kubernetes do minikube
kubectl create ns orchestrator

# no arquivo airflow.yaml, altere o 'dags.gitSync.repo'
# para o local (git) onde estarão armazenadas as DAGs do Airflow.
# isso é para que o Airflow aplique as atualizações enviadas ao git.

# como utilizaremos o git para fazer o gerenciamento das nossas DAGs,
# precisamos adicionar a chave privada SSH ao chaveiro do kubernetes,
# assim o container do Airflow terá acesso ao repositório das DAGs
# 
# certifique-se de substituir os caminhos onde estão em <> por caminhos *absolutos*
# ex: /home/nivaldo/.ssh/seuarquivo.pub
# -> id_rsa: geralmente é o arquivo `.ssh/id.rsa` ou `.ssh/id_ed25519`
# -> known_hosts: é o arquivo .ssh/known_hosts
# -> id_rsa.pub: geralmente é o arquivo `.ssh/id_ed25519.pub` ou `.ssh/id_rsa.pub`
#kubectl create secret generic git-ssh-key-secret --from-file=id_rsa=<arquivo_rsa> --from-file=known_hosts=<arquivo_known> --from-file=id_rsa.pub=<arquivo_pub> -n orchestrator
kubectl create secret generic git-ssh-key-secret --from-file=id_rsa=~/.ssh/id_ed25519 --from-file=known_hosts=.ssh/known_hosts --from-file=id_rsa.pub=~/.ssh/id_ed25519.pub -n orchestrator

# aplicar a configuração do Argo para subir o Airflow
kubectl apply -f ./orchestration/airflow.yaml

# acompanhe via Argo a instalação do Airflow ser finalizada
# use o comando abaixo para fazer o port forwarding da aplicação
kubectl port-forward svc/airflow-web 8001:8080 -n orchestrator
