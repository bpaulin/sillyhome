#!/usr/bin/env bash

MESSAGE=${1:-last}

git checkout dev
git rebase main
git reset --soft main
git checkout main -- cluster/base/flux-system/gotk-sync.yaml
git add cluster/base/flux-system/gotk-sync.yaml
git commit -m "$MESSAGE"
git push -u origin -f dev
git checkout main
git merge --ff-only dev
git push -u origin main
kubectl --kubeconfig=./provision/kubeconfig apply -f cluster/base/flux-system/gotk-sync.yaml
