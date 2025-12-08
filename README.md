
# VPN

```
docker build -t app-image:latest ./app
docker build -t vpn-image:latest ./vpn

eval $(minikube docker-env)

kubectl apply -f k8s/main.yaml

kubectl port-forward service/nginx 9000:80
kubectl port-forward service/prometheus 9090:9090
```

go to

```
localhost:9000 -> application
localhost:9090 -> prometheus dashboard

```

and test

traffic goes 

```
local -> nginx rev proxy -> vpn -> app
```
