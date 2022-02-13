#!/usr/bin/env bash
gtask ansible:playbook:k3s-nuke || true

gtask ansible:playbook:k3s-install

kubectl --kubeconfig=./provision/kubeconfig create namespace flux-system --dry-run=client -o yaml | kubectl --kubeconfig=./provision/kubeconfig apply -f -

cat ~/.config/sops/age/keys.txt |
    kubectl --kubeconfig=./provision/kubeconfig \
    -n flux-system create secret generic sops-age \
    --from-file=age.agekey=/dev/stdin

kubectl --kubeconfig=./provision/kubeconfig apply --kustomize=./cluster/base/flux-system

kubectl --kubeconfig=./provision/kubeconfig apply --kustomize=./cluster/base/flux-system
