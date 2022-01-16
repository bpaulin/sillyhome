---
title: Installation de k3s
---

Maintenant que le système est pret, setup de k3s

<!-- more -->

## Installation de k3s

j'ai choisi k3s et archlinux justement parce que les packages de l'un sont dans les repos de l'autre, ca va etre rapide.

Il suffit d'installer, et de démarrer, et c'est tout

```yaml
- name: Install common packages
  kewlfft.aur.aur:
    name:
      # k3s
      - k3s-bin
      # kubernetes client (k3s fournit le sien mais je veux rester pure kube)
      - kubectl
      # interface terminal tres user friendly pour surveiller son cluster
      - k9s
      # module python pour que ansible puisse jouer avec kubernetes aussi
      - python-openshift
      # gestionnaire de packages applicatifs kubernetes
      - helm
    use: yay
    state: present
  become: true
  become_user: aur_builder

- name: Start k3s
  service:
    name: k3s
    state: started
    enabled: true
  become: true
```

## Acces a k3s

k3s fournit un fichier de config utilisable, mais uniquement par l'user root. Pour permettre a l'user que ansible utilise sur le serveur, je le copie au bon endroit avec les bons droits:

```yaml
- name: create kube directory
  file:
    path: "/home/{{ ansible_user }}/.kube"
    state: directory
    mode: '700'

- name: copy kubeconfig
  copy:
    src: /etc/rancher/k3s/k3s.yaml
    remote_src: true
    dest: "/home/{{ ansible_user }}/.kube/config"
    owner: "{{ ansible_user }}"
    group: "{{ ansible_user }}"
    mode: '600'
  become: true
```

Cet user aura aussi besoin d'un plugin helm pour qu'ansible m'assure l'idempotence de mes deploiements:

```yaml
- name: Install Helm diff plugin
  kubernetes.core.helm_plugin:
    plugin_path: https://github.com/databus23/helm-diff
    state: present
```

Et enfin, pour pouvoir acceder au cluster kubernetes directement depuis mon poste (uniquement depuis le reseau local) je télécharge localement le fichier de config que j'utiliserai avec ```export KUBECONFIG=kubeconfig```

```yaml
- name: check if kubeconfig exists locally
  stat:
    path: "../kubeconfig"
  delegate_to: localhost
  register: st

- name: fetch kubeconfig
  fetch:
    src: "/home/{{ ansible_user }}/.kube/config"
    dest: "../kubeconfig"
    flat: true
  when: not st.stat.exists

- name: set ip in kubeconfig
  replace:
    path: "../kubeconfig"
    regexp: '127\.0\.0\.1'
    replace: "{{ ansible_host }}"
  delegate_to: localhost
```

Le cluster est pret, plus qu'a deployer des machins dessus!
