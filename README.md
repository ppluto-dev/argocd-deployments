# ArgoCD Setup

```bash
# Setup linux
apt update && apt upgrade -y

## https://github.com/rancher/k3os/issues/702#issuecomment-850246749
apt install apparmor apparmor-utils -y

# Install k3s
# https://k3s.io/
curl -sfL https://get.k3s.io | sh - 

# Disable Traefik
# https://github.com/k3s-io/k3s/issues/1160#issuecomment-1133559423
kubectl -n kube-system delete helmchart traefik traefik-crd
touch /var/lib/rancher/k3s/server/manifests/traefik.yaml.skip
systemctl restart k3s

# Install Kubernetes Gateway CRD
# https://gateway-api.sigs.k8s.io/guides/#install-standard-channel
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v0.6.0/standard-install.yaml

# Install ArgoCD
# https://argo-cd.readthedocs.io/en/stable/getting_started/
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Provide Gitlab container registry secret credentials.
# https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line
kubectl create secret docker-registry regcred \
  --docker-server=<your-registry-server> \
  --docker-username=<your-name> \
  --docker-password=<your-pword> \
  --docker-email=<your-email> \
  --namespace <namespace>

# Print ArgoCD password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
# Port-forward ArgoCD UI
echo https://$(curl ifconfig.me -s):8081
kubectl port-forward svc/argocd-server -n argocd 8081:443 --address='0.0.0.0'
```

## Creating ssh keys
```bash
# https://levelup.gitconnected.com/connect-argocd-to-your-private-github-repository-493b1483c01e
podman run --rm -it debian:testing

apt update && apt-get install -y openssh-client
ssh-keygen -t ed25519 -C "Argo CD"
cat ~/.ssh/*
```
