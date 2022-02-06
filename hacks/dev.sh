#!/usr/bin/env bash

git checkout dev
git rebase main
sed -i 's/branch: main/branch: dev/' cluster/base/flux-system/gotk-sync.yaml
git add cluster/base/flux-system/gotk-sync.yaml
git commit -m "switch branch"
git push -u origin dev
kubectl --kubeconfig=./provision/kubeconfig apply -f cluster/base/flux-system/gotk-sync.yaml
