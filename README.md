# argocd-test

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
kubectl port-forward svc/argocd-server -n argocd 8081:443 --address='0.0.0.0'

```

```bash
podman run --rm -it debian:testing

apt update && apt-get install -y openssh-client
ssh-keygen -t ed25519 -C "Argo CD"
cat ~/.ssh/*
