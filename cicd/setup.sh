sudo systemctl enable docker.service
sudo systemctl start docker.service

# cria o namespace no cluster kubernetes do minikube
kubectl create namespace cicd

# atualiza os repositórios do Helm
# e adiciona o repositório de charts do Argo ao Helm local
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# instala o Argo a partir do chart local do Helm
helm upgrade --install argocd argo/argo-cd --namespace cicd --wait

# realiza o port-forward para ter acesso à interface pelo browser
# este comando de port-forward fica em "idle" no terminal
kubectl port-forward svc/argocd-server 8080:80 -n cicd

# o Argo utiliza um acesso de usuário/senha na interface gráfica
# precisamos obter a senha (o usuário é 'admin')
# para isto, basta executar esse comando em um novo terminal
password="$(kubectl -n cicd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)"
echo $password

# adiciona a permissão ao Argo para gerenciar os recursos do cluster
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=system:serviceaccount:cicd:argocd-application-controller -n cicd

# para executar o comando abaixo (argocd) é necessário ter o CLI do ArgoCD na sua máquina
# https://argo-cd.readthedocs.io/en/stable/cli_installation/
pacman -S argocd

# adiciona o cluster do minikube como cluster gerenciado pelo Argo
# esses comandos devem ser executados no mesmo terminal que foi executado o comando de obter o password
# se aparecer uma mensagem "WARNING: server certificate had error", basta prosseguir
argocd login localhost:8080 --username admin --password $password
CLUSTER="minikube"
argocd cluster add $CLUSTER --in-cluster

# adiciona o repositório do projeto como gerenciado pelo argo
# isso é para que o Argo aplique as atualizações enviadas ao git.
# o argumento --ssh-private-key-path é o caminho no qual está a sua chave SSH privada para uso do github!
# o padrão é ela estar na pasta ~/.ssh, por isso, altere para o caminho da sua chave, ou o Argo terá problemas com o git.
REPOSITORY="git@github.com:nivaldomcj/mpti-integracaodados-projeto.git"
argocd repo add $REPOSITORY --ssh-private-key-path ~/.ssh/id_ed25519

# se tudo deu certo, use a url http://localhost:8080 para acessar o Argo
# use o usuário "admin" e a senha da variável $password

