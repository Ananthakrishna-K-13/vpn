### Setup
1. Install wireguard
2. Run these commadns to clear existing things
```bash
sudo wg-quick down wg0 2>/dev/null
sudo rm -f /etc/wireguard/wg0.conf

minikube delete --all

sudo ip route flush table main
```

-----

### Step 2

```bash

minikube start --driver=docker --ports=30000:30000/udp --ports=30001:30001/tcp


eval $(minikube docker-env)

docker build -t vpn-manager:local ./vpn_manager

kubectl apply -f k8s.yaml

kubectl get pods
```
Make sure all the pods are running before moveing to next steps

-----

### Step 3


```bash

CLIENT_PRIV=$(wg genkey)
CLIENT_PUB=$(echo "$CLIENT_PRIV" | wg pubkey)
MY_IP="10.13.13.99"


SERVER_PUB=$(kubectl exec deployment/vpn-gateway -- wg show wg0 public-key)
MINI_IP=$(minikube ip)

cat <<EOF > manual_vpn.conf
[Interface]
PrivateKey = $CLIENT_PRIV
Address = $MY_IP/32
MTU = 1280

[Peer]
PublicKey = $SERVER_PUB
Endpoint = $MINI_IP:30000
AllowedIPs = 10.0.0.0/8, 10.13.13.0/24
PersistentKeepalive = 25
EOF

kubectl exec deployment/vpn-gateway -- wg set wg0 peer $CLIENT_PUB allowed-ips $MY_IP/32

kubectl exec deployment/vpn-gateway -- ip addr add 10.13.13.1/24 dev wg0 2>/dev/null

kubectl exec deployment/vpn-gateway -- iptables -t nat -I POSTROUTING 1 -s 10.13.13.0/24 -j MASQUERADE

kubectl exec deployment/vpn-gateway -- /bin/sh -c "sysctl -w net.ipv4.conf.all.rp_filter=0; sysctl -w net.ipv4.conf.default.rp_filter=0"


sudo cp manual_vpn.conf /etc/wireguard/wg0.conf
sudo wg-quick up wg0
```

-----

### **Phase 4: Verification**

Note: if connecting to vpn casues wifi to stop working, then fix some wifi powersaving options.

1.  **Check the Tunnel:**

    ```bash
    sudo wg show
    ```

    Look for: **latest handshake: X seconds ago** . If found ,then good, else some error.

2.  **Access the Hidden Webpage:**

    ```bash
    kubectl get svc hidden-target-service
    ```

    This command gives address of private webserver (cluster-ip), which can be pinged (curled/ browsed) only why vpn is switched on.

    Browse that address on browser and you will see `Welcome to nginx!` page

    You can check switichng vpn off and browing the same webserver, and then switch on and browse the same webserver

```
    # Switches the vpn on
    sudo wg-quick up wg0

    # Switches the vpn off
    sudo wg-quick down wg0
```

