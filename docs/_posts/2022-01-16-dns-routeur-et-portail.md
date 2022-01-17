---
title: Routeur, DNS et portail
---

Installation sur le cluster des applis qui me faciliteront la vie pour les suivantes

## Routeur

k3s embarque de base [traefik](https://doc.traefik.io/traefik/) qui définit 2 endpoints

 * **web** sur le port 80 que je vais reserver aux applis internes
 * **websecure** sur le port 443 pour les applis externes. Ce port sera accessible depuis internet via cloudflare mais ce n'est pas le sujet aujourd'hui.

Plus tard, je pense que j'installerai moi meme traefik pour plus comprendre, maîtriser et apprendre son fonctionnement. Dans un premier temps je vais en profiter sans frais.

Pour limiter l'accès a un service sur tel ou tel port, on peut difficilement faire plus simple que ça:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
# ...
```

## DNS

Maintenant que traefik répond sur le port 80 et dispatch les requêtes en fonction du domaine demandé, je dois permettre aux machines de mon réseau de résoudre bidule.sillykube vers l'ip de mon serveur.

Pour commencer je configure mon router (mes google wifi dans mon cas) pour utiliser l'ip de mon server comme dns primaire et 4.4.4.4 comme dns secondaire (dns google).

Ensuite, j'install [adguard](https://adguard.com/) sur mon cluster.

 > AdGuard is the best way to get rid of intrusive ads and online tracking, and to protect your computer from malware. Make your web surfing faster, safer and more comfortable with AdGuard!

Alors c'est super, je dis pas mais surtout adguard va me permettre de precisier moi meme mes regles dns! [k8s-at-home] fournit un chart donc c'est tres simple. Le but est d'exposer sur le port 53 le service dns (ce qui posera surement problème quand j'aurai plusieurs noeuds mais pour l'instant tout va bien)

```yaml
    - name: "adguard Chart"
      kubernetes.core.helm:
        name: "adguard"
        chart_ref: "k8s-at-home/adguard-home"
        release_namespace: "adguard"
        create_namespace: true
        state: present
        values:
          ingress:
            main:
              enabled: true
              annotations:
                traefik.ingress.kubernetes.io/router.entrypoints: web
              hosts:
                - host: "adguard.sillykube"
                  paths:
                    - path: "/"
                      pathType: Prefix
          service:
            dns-tcp:
              type: LoadBalancer
              ports:
                dns-tcp:
                  nodePort: 53
            dns-udp:
              type: LoadBalancer
              ports:
                dns-udp:
                  nodePort: 53
          # Les valeurs pas comme sur https://github.com/k8s-at-home/charts/blob/master/charts/stable/adguard-home/values.yaml
          # Seul le tableau dns.rewrites est modifié
          config: |
            dns:
              rewrites:
                - domain: '*.sillykube'
                  answer: 192.168.86.20
```

## Portail

Pour finir, je vais utiliser [homer] pour un portail pour lier les applis. Une fois encore, [k8s-at-home] fournit tout

```yaml
    - name: Public portal
      kubernetes.core.helm:
        name: homer
        chart_ref: k8s-at-home/homer
        release_namespace: homer-public
        create_namespace: true
        values:
          ingress:
            main:
              enabled: true
              annotations:
                traefik.ingress.kubernetes.io/router.entrypoints: websecure
              hosts:
                - host: "paulin.homes"
                  paths:
                    - path: "/"
                      pathType: Prefix
          configmap:
            config:
              enabled: true
              data:
                config.yml: |
                  title: Sillyhome
                  subtitle: Private
                  services:
                  - items:
                      - name: adguard
                        url: "https://adguard.sillykube"
                        target: "_blank"
```


[k8s-at-home]: https://k8s-at-home.com/
[homer]: https://github.com/bastienwirtz/homer
