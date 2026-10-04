# Projet 1 — Déploiement et Exploitation d’un Cluster Hadoop avec Docker

| | |
|:--|:--|
| **Cours** | Bases de données massives avancées (**IFM30522**) |
| **Unité** | UA1 — Projet 1 |
| **Groupe** | **G4 — Les_Hadoop_Riders** |
| **Date de remise** | 4 octobre 2026 |
| **Présentation** | 8 octobre 2026 |
| **Image Docker** | `leshadoopriders/hadoop-tp-g4:1.0` |
| **Docker Hub** | https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4 |
| **Code source** | https://github.com/asinyopetro/Les_Hadoop_Riders_G4 |

### Membres du groupe

| Étudiant | Étudiant |
|----------|----------|
| Komla Petro Asinyo | Kassoum Dene |
| Joel Kazoni Tugirimana | Forbes Magène |
| Frank A Simo Ngounou | Wren Surprenant-Nicolson |

> **Objectif du livrable :** déployer un cluster Hadoop multi-nœuds avec Docker, manipuler HDFS, exécuter un job YARN, publier l’image sur Docker Hub, et documenter les résultats avec captures d’écran (terminal et interfaces web).

---

## Introduction

Ce rapport présente le travail du groupe **Les_Hadoop_Riders (G4)** dans le cadre du Projet 1 de l’UA1. Nous avons choisi de déployer et d’exploiter un **cluster Hadoop** (HDFS + YARN) entièrement **conteneurisé avec Docker**.

La démarche suivie est la suivante :

1. Comprendre le besoin Big Data (cas e-commerce et 3V) et les rôles de HDFS / YARN.  
2. Construire une image Docker basée sur **Hadoop 3.3.6** et lancer **1 master + 5 workers**.  
3. Vérifier le cluster (5 DataNodes Live), publier l’image sur Docker Hub.  
4. Manipuler HDFS (droits, blocs, lecture, fusion, corbeille, réplication).  
5. Exécuter un job MapReduce (calcul de π) et analyser les interfaces de monitoring.  
6. Documenter les problèmes rencontrés et les solutions.

Le présent document suit la structure de l’énoncé (Parties 1, 2 et 3), avec les commandes exactes et les preuves (captures).

---

## Partie 1 — Contexte théorique et architecture (5 pts)

### 1. Cas d’usage Big Data (1.5 pt)

Nous avons choisi le secteur de l’**e-commerce** (commerce électronique : vente de produits ou services via Internet).

**Scénario :** une chaîne de magasins avec un site web doit conserver et analyser :

- les **transactions** (tickets de caisse, montants, magasins) ;  
- les **logs** de navigation et d’erreurs du site ;  
- les **mouvements de stock** ;  
- éventuellement des **images produits**.

Chaque jour le volume grossit, les données arrivent souvent, et les formats changent. Une base relationnelle seule peut devenir insuffisante pour tout stocker et traiter à grande échelle.

#### Les 3V du Big Data

Les **3V** sont les trois caractéristiques classiques utilisées pour décrire le Big Data :

| V | Signification | Application e-commerce |
|---|---------------|------------------------|
| **Volume** | Quantité de données | Millions d’événements, historique sur plusieurs années |
| **Vélocité** | Vitesse d’arrivée / de traitement | Commandes et paiements en continu ; réaction rapide (fraude, rupture de stock) |
| **Variété** | Diversité des formats | Tables CSV, JSON, logs texte, images produits |

Dans ce contexte :

- **HDFS** (*Hadoop Distributed File System*) sert à **stocker** les données de façon distribuée sur plusieurs machines.  
- **YARN** (*Yet Another Resource Negotiator*) sert à **lancer des traitements** (MapReduce, etc.) sur le cluster en allouant CPU et mémoire.

### 2. HDFS vs système de fichiers classique (1.5 pt)

Un **système de fichiers classique** (ex. NTFS sous Windows, ext4 sous Linux) stocke un fichier sur **une** machine. Les métadonnées et le contenu sont gérés par l’**OS** local. Si le disque tombe en panne, les données peuvent être perdues (sauf sauvegarde externe).

**HDFS**, au contraire, est conçu pour un **cluster** :

| Critère | FS classique (NTFS, ext4…) | **HDFS** |
|---------|----------------------------|----------|
| Emplacement | Une seule machine | Plusieurs machines (cluster) |
| Organisation | Fichier entier sur un disque | Fichier découpé en **blocs** (souvent 128 Mo) |
| Métadonnées | Gérées par l’OS local | Gérées par le **NameNode** |
| Contenu | Sur le même disque | Sur les **DataNodes** |
| Tolérance aux pannes | Faible (disque unique) | Forte grâce à la **réplication** (ex. facteur 3) |

Le **NameNode** conserve le *namespace* (noms de fichiers, dossiers, emplacement des blocs). Les **DataNodes** stockent les blocs réels. Plusieurs copies d’un même bloc peuvent exister sur des nœuds différents : si un DataNode tombe, les données restent disponibles ailleurs.

> **En pratique :** le FS local est centralisé ; HDFS est distribué et plus tolérant aux pannes grâce à la réplication.

### 3. Rôle de YARN — ResourceManager et NodeManager (2 pts)

**YARN** gère les **ressources** du cluster (CPU, mémoire) lorsqu’une application est soumise. Le flux typique est le suivant :

1. Un **client** soumet un job (ex. `yarn jar … pi`).  
2. Le **ResourceManager (RM)**, sur le master, reçoit la demande, connaît l’état des ressources, alloue des **conteneurs** et démarre l’**ApplicationMaster**.  
3. Les **NodeManagers (NM)**, sur chaque worker, démarrent et surveillent les conteneurs **localement**, puis remontent l’état au RM.  
4. L’**ApplicationMaster** pilote le job (demande de conteneurs pour les tâches Map/Reduce, suivi de l’avancement).

| Composant | Où ? | Rôle |
|-----------|------|------|
| **ResourceManager (RM)** | Master | Orchestre et alloue les ressources |
| **NodeManager (NM)** | Chaque worker | Exécute et surveille les conteneurs sur sa machine |
| **ApplicationMaster (AM)** | Conteneur alloué | « Chef » du job en cours |

> **À retenir :** le ResourceManager **orchestre** ; le NodeManager **exécute** localement.

---

## Partie 2 — Déploiement et manipulation pratique (15 pts)

### A. Mise en place de l’environnement Docker (4 pts)

#### Choix techniques

| Élément | Choix du groupe |
|---------|-----------------|
| Version Hadoop | **3.3.6** |
| Image de base | `apache/hadoop:3.3.6` |
| Image du groupe | `leshadoopriders/hadoop-tp-g4:1.0` |
| Orchestration | Docker Compose (`docker-compose.yml`) |
| Architecture | 1 master + **5** workers |
| Réseau | `hadoop-net` (bridge) |

Chaque conteneur démarre via `entrypoint.sh` selon la variable `HADOOP_ROLE` (`master` ou `worker`). Les fichiers de configuration (`core-site.xml`, `hdfs-site.xml`, `yarn-site.xml`, `mapred-site.xml`, `workers`) sont copiés dans l’image.

#### 1. Déploiement NameNode + 5 DataNodes (1.5 pt)

Nous avons déployé **six conteneurs** :

| Conteneur | Rôles |
|-----------|--------|
| `hadoop-master` | NameNode, ResourceManager, SecondaryNameNode |
| `hadoop-worker1` … `hadoop-worker5` | DataNode + NodeManager |

**Ports exposés sur la machine hôte :**

| Port | Service |
|------|---------|
| **9870** | Interface web HDFS (NameNode UI) |
| **8088** | Interface web YARN |
| **9000** | HDFS RPC |

**Commandes de démarrage :**

```bash
docker compose up --build -d
docker ps
```

![Figure 1 — Terminal : docker ps / dfsadmin](captures/screenshot-terminal-01.png)

#### 2. Vérification des DataNodes (1.5 pt)

```bash
docker exec -it hadoop-master hdfs dfsadmin -report
```

> **Résultat observé :** Live datanodes **(5)** — le cluster est opérationnel.  
> Interface NameNode : http://localhost:9870

Cette commande confirme que les cinq DataNodes se sont bien enregistrés auprès du NameNode. Sans cela, le stockage HDFS ne serait pas réellement distribué.

![Figure 2 — UI NameNode (vue d’ensemble)](captures/screenshot-namenode.png)

![Figure 3 — Liste des DataNodes (5 Live)](captures/screenshot-datanodes.png)

#### 3. Publication de l’image (1 pt)

```bash
docker login
docker push leshadoopriders/hadoop-tp-g4:1.0
```

> **URL publique :** https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4  
> **Note :** Docker Hub impose les **minuscules** dans le nom du dépôt, d’où `g4` plutôt que `G4`.

Toute personne disposant de Docker peut ensuite récupérer l’image et relancer le cluster à partir de notre dépôt GitHub / Compose.

---

### B. Manipulation avancée sur HDFS (6 pts)

Nous simulons des données de ventes e-commerce. Le fichier local `data/transactions.csv` contient 10 lignes (colonnes : ID, Date, Montant, Magasin).

#### 4. Répertoires et droits (2 pts)

```bash
hdfs dfs -mkdir -p /data/ventes/2026
hdfs dfs -chmod 755 /data/ventes/2026
hdfs dfs -put -f /data/transactions.csv /data/ventes/2026/
hdfs dfs -chmod 644 /data/ventes/2026/transactions.csv
```

- `mkdir -p` crée l’arborescence.  
- `chmod 755` sur le dossier autorise lecture/exécution pour les autres, écriture pour le propriétaire.  
- `put` envoie le CSV vers HDFS.  
- `chmod 644` sur le fichier le rend lisible sans le rendre exécutable.

#### 5. Transfert et vérification des blocs (2 pts)

```bash
hdfs fsck /data/ventes/2026/transactions.csv -files -blocks -locations
hdfs dfs -stat "%n | taille=%b | replication=%r | block_size=%o" /data/ventes/2026/transactions.csv
```

| Indicateur | Valeur observée |
|------------|-----------------|
| Taille | 377 octets |
| Réplication initiale | 3 |
| Nombre de blocs | 1 (fichier petit ; bloc par défaut 128 Mo) |
| État FSCK | **HEALTHY** |

Un fichier très petit occupe quand même **un bloc** HDFS : c’est normal. La réplication à 3 signifie que ce bloc existe en trois copies sur le cluster.

![Figure 4 — Terminal : commandes HDFS (fsck, stat, etc.)](captures/screenshot-terminal-02.png)

#### 6. Lecture et concaténation (1 pt)

```bash
hdfs dfs -cat /data/ventes/2026/transactions.csv | head -n 5
hdfs dfs -put -f /data/transactions_part2.csv /data/ventes/2026/
hdfs dfs -getmerge /data/ventes/2026 /tmp/transactions_merged.csv
hdfs dfs -put -f /tmp/transactions_merged.csv /data/ventes/2026/transactions_merged.csv
```

Les 5 premières lignes sont lues directement depuis HDFS (`cat` + `head`). Ensuite, un second fichier est ajouté et les fichiers du dossier sont fusionnés avec `getmerge`, puis le résultat est réinjecté dans HDFS.

#### 7. Suppression / corbeille (1 pt)

```bash
hdfs dfs -rm /data/ventes/2026/transactions_part2.csv
hdfs dfs -D fs.trash.interval=10080 -rm /data/ventes/2026/to_delete.csv
hdfs dfs -ls -R /user/hadoop/.Trash
# suppression définitive :
# hdfs dfs -rm -skipTrash /chemin/fichier
```

> Sans `fs.trash.interval`, la suppression peut être **définitive**. Avec un intervalle > 0, le fichier passe dans `.Trash` (corbeille HDFS). L’option `-skipTrash` force la suppression définitive, sans passer par la corbeille.

---

### C. Exécution d’un job YARN (5 pts)

Pour valider YARN, nous avons lancé l’exemple officiel MapReduce de calcul de **π** (méthode de **Monte Carlo** : estimation à partir de points aléatoires).

```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000
```

Les paramètres `4` et `1000` correspondent à **4 tâches map** et **1000 échantillons** par map.

| Champ | Résultat |
|-------|----------|
| Application | `application_1791039798429_0001` |
| Nom | QuasiMonteCarlo |
| État final | **SUCCEEDED** |
| Estimation | π ≈ **3.14** |
| Paramètres | 4 maps, 1000 samples |

Ce résultat montre que le ResourceManager a alloué des ressources et que les NodeManagers ont bien exécuté les tâches jusqu’à la fin.

![Figure 5 — Terminal : sortie du job π](captures/screenshot-terminal-03.png)

![Figure 6 — UI YARN : liste des applications](captures/screenshot-yarn.png)

![Figure 7 — Détail application FINISHED / SUCCEEDED](captures/screenshot-yarn-app.png)

---

## Partie 3 — Administration, monitoring et analyse (10 pts)

### 1. Interfaces web (4 pts)

Les interfaces web permettent de contrôler le cluster sans rester uniquement en ligne de commande.

**NameNode — http://localhost:9870**  
On observe **5 DataNodes** actifs. L’espace DFS utilisé reste faible (environnement de laboratoire, petits fichiers CSV). Aucun *missing block* (bloc manquant) n’a été observé pendant nos tests.

**YARN — http://localhost:8088**  
L’application pi apparaît en état **FINISHED / SUCCEEDED**. Les métriques affichent l’allocation mémoire et le temps d’exécution (environ **198589 MB-seconds** et **216 vcore-seconds** sur un des runs).

Ces UI sont complémentaires aux commandes `dfsadmin -report` et `yarn application -list`.

### 2. Facteur de réplication (3 pts)

```bash
hdfs dfs -setrep -w 2 /data/ventes/2026/transactions.csv
```

> Après la commande, la réplication du fichier passe de **3 à 2**. Le NameNode met à jour la **cible** de réplication. Une copie de bloc devenue superflu est retirée sur les DataNodes. L’option `-w` (*wait*) attend que l’opération soit terminée avant de rendre la main.

Baisser la réplication économise de l’espace disque, mais réduit la redondance. L’augmenter fait l’inverse : plus de tolérance aux pannes, plus d’espace consommé.

### 3. Retour d’expérience / troubleshooting (3 pts)

| # | Problème | Symptôme | Cause | Solution |
|---|----------|----------|-------|----------|
| 1 | Pull avant publication | `pull access denied` | Compose téléchargeait une image pas encore sur Hub | `pull_policy: never` + build local, puis `docker push` |
| 2 | Majuscules dans le tag | `repository name must be lowercase` | Docker Hub refuse `G4` | Tag final `leshadoopriders/hadoop-tp-g4:1.0` |
| 3 | Build trop long | Téléchargement bloqué | archive.apache.org très lent | Image de base `apache/hadoop:3.3.6` + notre config / `entrypoint.sh` |

Ces incidents ont permis de mieux comprendre le cycle de vie d’une image Docker (build → run local → push Hub → pull éventuel) et les contraintes de nommage des registres.

---

## Conclusion

Le groupe **Les_Hadoop_Riders** a livré un cluster Hadoop opérationnel en Docker :

- **Architecture** conforme : 1 master + 5 workers (DataNodes / NodeManagers).  
- **HDFS** manipulé : arborescence, droits, fsck, lecture, getmerge, Trash, setrep.  
- **YARN** validé : job MapReduce π en état **SUCCEEDED** (π ≈ 3.14).  
- **Image publiée** : `leshadoopriders/hadoop-tp-g4:1.0` sur Docker Hub.  
- **Preuves** : captures terminal + UI NameNode / YARN dans ce rapport et dans le dépôt.

Ce travail montre que nous savons déployer, exploiter et administrer un environnement Hadoop conteneurisé, en reliant la théorie (3V, HDFS, YARN) à une mise en pratique documentée.

---

## Annexes

### A. Glossaire des sigles

| Sigle / terme | Signification |
|---------------|---------------|
| **HDFS** | *Hadoop Distributed File System* — système de fichiers distribué |
| **YARN** | *Yet Another Resource Negotiator* — gestionnaire de ressources |
| **RM / NM** | ResourceManager / NodeManager |
| **3V** | Volume, Vélocité, Variété |
| **MapReduce** | Modèle de calcul (phase Map puis Reduce) |
| **DFS** | *Distributed File System* |
| **UI** | Interface utilisateur (web) |
| **RPC** | *Remote Procedure Call* (port 9000 HDFS) |
| **CSV** | *Comma-Separated Values* |
| **Trash** | Corbeille HDFS |
| **setrep** | Commande de changement du facteur de réplication |
| **fsck** | Vérification de l’intégrité HDFS |
| **Docker Hub** | Registre public d’images Docker |

### B. Structure du code source

```text
Les_Hadoop_Riders_G4/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── config/
│   ├── core-site.xml
│   ├── hdfs-site.xml
│   ├── yarn-site.xml
│   ├── mapred-site.xml
│   └── workers
├── data/
│   ├── transactions.csv
│   └── transactions_part2.csv
├── scripts/
│   ├── demo-hdfs.sh
│   └── demo-yarn-pi.sh
├── captures/
└── README.md
```

### C. Liens du projet

| Ressource | URL |
|-----------|-----|
| Docker Hub | https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4 |
| GitHub | https://github.com/asinyopetro/Les_Hadoop_Riders_G4 |
| UI NameNode (local) | http://localhost:9870 |
| UI YARN (local) | http://localhost:8088 |
