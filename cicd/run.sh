# para executar o forwarding (manter aberto em um terminal)
kubectl port-forward svc/argocd-server 8080:80 -n cicd

# URL de interface do Argo: http://localhost:8080
