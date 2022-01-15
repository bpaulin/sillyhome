---
title: Choix matériels et logiciels
---

 * Mini PC core i5 / 16 Gio / 512Gio
 * [Archlinux]
 * [k3s]
 * [Ansible]

# Le matériel

Plusieurs choix possibles, dans l'ordre chronologique de leur arrivée chez moi:

## Le cluster de raspberry

De loin le plus interessant a installer, le plus fun à annoncer et le plus geek.

Pour autant, je ne reprendrais pas cette solution:

 * C'est finalement assez cher, en multipliant les raspberrys et en ajoutant les alims et la connectique réseau
 * La plateforme arm fait que pas mal de softs ne sont pas disponibles, que certaines images docker doivent etre construites localement etc.
 * Le **W**ife **A**cceptance **F**actor est clairement négatif. Même pour moi, j'ai passé l'age de la décoration a base de cable apparent. Le sapin de noël de diodes ne me tente plus.

## Le mini pc entrée de gamme

Ce [mini pc](https://www.amazon.fr/gp/product/B07K6H6XVN) à 150€ sert actuellement ma domotique. Je voulais à l'epoque remplacer mes raspbery par un mini pc le moins cher possible.

Il remplit sa fonction principale mais il ne répond pas au besoin futurs:

 * Le disque est petit. si je veux faire autre chose que de la domotique, je dois brancher un hdd externe et le waf baisse.
 * La puissance est trop faible pour faire tourner ce que j'ai en tete. je pourrais up la ram, mais le cpu reste le point faible
 * Il est tout petit... donc il chauffe beaucoup meme en domotique seule. un encodage de video en live le rend brulant en quelques minutes

## Le mini pc moyen de gamme

Mince quel dommage je dois donc acheter un nouveau jouet technologique. Plus de cpu, plus de ram, plus de disque le tout a un prix correct: [mon nouveau jouet](https://www.amazon.fr/gp/product/B0919ZGR1R)

![Specification](https://m.media-amazon.com/images/I/71Ss7FKzLYL._AC_SY450_.jpg)

# L'OS

**Debian** m'aurait apporté une grande stabilité (pas cruciale pour un jouet) au prix de package datés.

**NixOs** m'aurait apporté des packages récents et enfin l'occasion de jouer avec. Ceci dit je vais avoir assez de trucs a apprendre sur ce projet pour ne pas me mettre nix sur le chemin

Ca sera **[archlinux]**:

 * C'est une distrib en rolling release, je n'aurais jamais à préparer une migration potentiellement douloureuse.
 * Le choix de packages natifs est immense et ils sont toujours très récents
 * C'est ma distrib de travail, je connais assez bien

# Le cluster kubernetes

J'ai choisi [k3s] parce qu'il me parait etre un bon compromis pour la facilité d'installation, les services fournis de base, la compatibilité avec le *vrai* kubernetes et la légèreté. Sincerement ce choix est basé sur pas grand chose mais en théorie, peu importe

# L'outil de déploiement

Ca sera [ansible] parce que je bosse avec tout les jours, et que je veux un seul outil pour gérer le système, le cluster  et les déploiements kubernetes .

[k3s]: https://k3s.io/
[archlinux]: https://archlinux.org/
[ansible]: https://www.ansible.com/
