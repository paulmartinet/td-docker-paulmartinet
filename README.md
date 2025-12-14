# Rapport – TD Conception d’une application conteneurisée générique

## Quelque liens utile :

## pour voir le front : http://localhost:8080

## Pour voir les routes de l'API :

## Status : http://localhost:8080/api/status

## Items : http://localhost:8080/api/items

## Metrics : http://localhost:8080/api/metrics

## Pour accéder à Grafana : http://localhost:3000 (user:admin, mdp:admin)
## Pour accéder à Prometheus : http://localhost:9090


## 1. Introduction

J'ai réalisé ce projet dans le cadre du TD « Conception d’une application conteneurisée générique ». L’objectif est de concevoir, construire et déployer une application complète composée de plusieurs services conteneurisés, en respectant les bonnes pratiques Docker, de sécurité et d’automatisation.

L’application finale est composée de :

* une API développée en Python
* une base de données PostgreSQL
* une interface web statique
* des outils de supervision (Prometheus et Grafana)

L’ensemble est orchestré à l’aide de Docker Compose.

---

## 2. Architecture de l’application

### 2.1 Description des services

**Base de données (PostgreSQL)**
La base de données stocke les données exposées par l’API. Le schéma est initialisé automatiquement au démarrage du conteneur via un script SQL. Les données sont persistées grâce à un volume Docker.

**API (FastAPI – Python)**
L’API expose les routes suivantes :

* `/status` : permet de vérifier la disponibilité de l’API
* `/items` : retourne la liste des éléments stockés en base de données
* `/metrics` : expose des métriques pour Prometheus

La connexion à la base de données est entièrement externalisée via des variables d’environnement.

**Front-end (HTML / JavaScript + Nginx)**
Le front-end est une interface web statique qui interroge l’API via des requêtes HTTP et affiche les données à l’utilisateur. Le site est servi par Nginx, configuré comme serveur statique et reverse-proxy vers l’API.

**Supervision (Prometheus & Grafana)**
Prometheus collecte les métriques exposées par l’API. Grafana permet de visualiser ces métriques à travers des tableaux de bord.

### 2.2 Schéma d’interaction

Navigateur → Front (Nginx) → API (FastAPI) → Base de données (PostgreSQL)

---

## 3. Choix techniques

* **Langage API** : Python avec FastAPI (léger, performant, adapté aux API REST)
* **Base de données** : PostgreSQL (robuste et surtout vous nous l'avez conseillez dans le TD)
* **Conteneurisation** : Docker
* **Orchestration** : Docker Compose
* **Supervision** : Prometheus et Grafana

Ces choix reposent sur des technologies libres, largement utilisées dans le monde professionnel.

---

## 4. Construction des images Docker

### 4.1 Dockerfile multi-étapes

Les Dockerfiles de l’API utilisent des builds multi-étapes :

* une première étape pour installer les dépendances
* une seconde étape minimaliste pour exécuter l’application

Cette approche permet de réduire significativement la taille des images finales.

### 4.2 Images légères

Les images sont basées sur des versions `slim` ou `alpine` afin de limiter la surface d’attaque et la taille des conteneurs.

### 4.3 Fichiers .dockerignore

Chaque service dispose d’un fichier `.dockerignore` afin d’exclure les fichiers inutiles lors du build (cache Python, fichiers temporaires, etc.).

---

## 5. Gestion des variables d’environnement

Toutes les informations sensibles (identifiants de base de données, ports, hôtes) sont externalisées dans un fichier `.env` et injectées dans les conteneurs via Docker Compose.

Cette approche permet :

* une meilleure sécurité
* une configuration plus flexible
* une séparation claire entre code et configuration

---

## 6. Orchestration avec Docker Compose

Le fichier `docker-compose.yml` définit les services suivants :

* db
* api
* front
* prometheus
* grafana

Il configure également :

* les réseaux entre services
* les volumes persistants
* les variables d’environnement
* les dépendances entre conteneurs

### 6.1 Healthchecks

Des healthchecks sont définis pour les services critiques (base de données et API) afin de s’assurer qu’ils sont opérationnels avant le démarrage des services dépendants.

---

## 7. Sécurité

Plusieurs bonnes pratiques de sécurité ont été appliquées :

* exécution des conteneurs avec un utilisateur non-root
* images minimales
* absence de secrets en dur dans le code

Les images peuvent être analysées à l’aide de `docker scan` afin d’identifier d’éventuelles vulnérabilités.

---

## 8. Supervision et logs

### 8.1 Logs

Les applications écrivent leurs logs sur la sortie standard. Ceux-ci sont accessibles via la commande :

```
docker compose logs
```

### 8.2 Métriques

L’API expose un endpoint `/metrics` collecté par Prometheus. Grafana permet ensuite de visualiser :

* la disponibilité de l’API
* le nombre de requêtes

---

## 9. Automatisation

Un script `deploy.sh` permet d’automatiser :

* la vérification de la configuration Docker Compose
* la construction des images
* le scan de sécurité
* le déploiement de l’ensemble de la stack

Cette automatisation facilite le déploiement et réduit les erreurs humaines.

---

## 10. Commandes clés

* Construction et lancement :

```
docker compose up --build -d
```

* Arrêt de la stack :

```
docker compose down
```

* Consultation des logs :

```
docker compose logs
```

---

## 11. Difficultés rencontrées

Les principales difficultés rencontrées concernent :

* la partie affichage des métrics dans Grafana
* la persistance du volume grafana
* la partie Python car je ne suis pas dev (je me suis aider d'une IA)

---

## 12. Améliorations possibles

Plusieurs améliorations pourraient être envisagées :

* mise en place d’une réel intégration continu (CI/CD)
* sécurisation avancée (secrets Docker, HTTPS, authentification)
* mise en place d'un nom de domaine pour remplacer localhost

---

## 13. Conclusion

Ce projet permet de mettre en pratique les différents concepts qu'on a vu en cours sur Docker. L’ensemble des objectifs pédagogiques du TD est respecté grace a l'ajout de Prometheus et Grafana (qu'on a pas pu voir en cours a cause du manque de temps), et l’architecture mise en place est cohérente, sécurisée et évolutive.
