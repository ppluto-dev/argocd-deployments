# argocd-test

Kubernetes setup
```
# k3s.io
curl -sfL https://get.k3s.io | sh - 

# https://helm.sh/docs/intro/install/


# https://github.com/k3s-io/k3s/issues/1160#issuecomment-1133559423

```


```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
kubectl port-forward svc/argocd-server -n argocd 8081:443 --address='0.0.0.0'

```

```bash
# https://levelup.gitconnected.com/connect-argocd-to-your-private-github-repository-493b1483c01e
podman run --rm -it debian:testing

apt update && apt-get install -y openssh-client
ssh-keygen -t ed25519 -C "Argo CD"
cat ~/.ssh/*

```
