---
title: Installation du système
---

En partant d'un archlinux vierge avec juste openssh installé, setup d'un projet ansible et installation de k3s

<!-- more -->

## Accès et inventaire

Il y a dans le repo un vagrantfile et l'inventaire ansible correspondant. Dans un premier temps le mini pc n'est utilisé par personne, donc le mini pc fait office d'env de dev et ca provoque le premier problème: comment y acceder?

Je veux acceder à mon server dans 3 situations differentes:
 * depuis mon propre reseau
 * depuis l'exterieur (en 4g par exemple)
 * depuis le reseau de mon travail (a travers un proxy)

Pour ça, je vais masquer ces complications à ansible en confiant tout a une config ssh par cas. Ma clé ssh est dans l'emplacement par defaut (```~/.ssh/id_rsa```) et l'inventaire 'live' du projet ansible n'a qu'un host:

```ini
sillykube
```

### Depuis mon réseau

Le cas le plus simple le serveur repond sur le port classique avec cette configuration ssh:

```ssh
Host sillykube
    Hostname 192.168.86.20
    User XXXXXXXX
```

### Depuis l'exterieur

J'ai configuré mon routeur pour que le port 2222 (par exemple) renvoie vers le port 22 de mon serveur

```ssh
Host sillykube
    Hostname 111.111.111.111 # mon ip externe
    User XXXXXXXX
    Port 2222
```

### Depuis le travail

Pour sortir du reseau, je dois passer par un proxy authentifié. Pour ça j'ai besoin de corkscrew (```sudo pacman -S corkscrew```) et d'un fichier contenant mon mot de passe.

**/home/bruno_paulin/.ssh/auth**:

```
MON_LOGIN:MON_PASSWORD
```

Le fichier de configuration ssh se complexifie un peu pour passer par corkscrew:

```ssh
Host sillykube
    Hostname 111.111.111.111 # mon ip externe
    User XXXXXXXX
    Port 2222
    ProxyCommand corkscrew <PROXY_IP> <PROXY_PORT> %p /home/bruno_paulin/.ssh/auth
```

Au final, j'ai ces 3 fichiers ignorés a la racine du repo et je suis a un lien symbolique de pouvoir acceder a mon serveur quelque soit la situation.

## Playbook système

Comme sur mon poste je vais utiliser yay pour installer les [packages natifs](https://archlinux.org/packages/) et les [packages aur](https://aur.archlinux.org/packages/) de la meme maniere.

Pour ca, une collection ansible existe: [ansible-aur](https://github.com/kewlfft/ansible-aur) que j'installe avec ```ansible-galaxy collection install kewlfft.aur```

Yay ne pouvant pas se lancer en root mais ayant besoin du mot de passe root plus tard dans le process, il faut créer un user pouvant acceder a pacman sans avoir a taper un mot de passe:

```yaml
- name: Create the `aur_builder` user
    become: true
    ansible.builtin.user:
    name: aur_builder
    create_home: true
    group: wheel

- name: Allow the `aur_builder` user to run `sudo pacman` without a password
    become: true
    ansible.builtin.lineinfile:
    path: /etc/sudoers.d/11-install-aur_builder
    line: 'aur_builder ALL=(ALL) NOPASSWD: /usr/bin/pacman'
    mode: '600'
    create: true
    validate: 'visudo -cf %s'
```

On peut maintenant installer les packages de build (qui seront de toute facon utiles a un moment ou a un autre pour contruire les packages aur) et utiliser makepkg (natif) pour installer yay

```yaml
- name: install build packages
    become: true
    ansible.builtin.pacman:
    name:
        - base-devel
    update_cache: true
    state: present

- name: Install yay using makepkg if it isn't installed already
    kewlfft.aur.aur:
    name: yay
    use: makepkg
    state: present
    become: true
    become_user: aur_builder
```

Et pour finir l'installation du systeme, j'installe quelques packages basiques toujours utiles


```yaml
- name: Install common packages
  kewlfft.aur.aur:
  name:
    - htop
    - ncdu
    - p7zip
    - speedtest-cli
    - vim
    - jq
    - curl
  use: yay
  state: present
  become: true
  become_user: aur_builder
```
