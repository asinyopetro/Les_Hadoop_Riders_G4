# Projet 1 — Déploiement et Exploitation d’un Cluster Hadoop avec Docker

| | |
|:--|:--|
| **Cours** | Bases de données massives avancées (**IFM30522**) |
| **Unité** | UA1 — Projet 1 |
| **Groupe** | **G4 — Les_Hadoop_Riders** |
| **Image Docker** | `leshadoopriders/hadoop-tp-g4:1.0` |
| **Docker Hub** | https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4 |
| **Code source** | https://github.com/asinyopetro/Les_Hadoop_Riders_G4 |
| **Version Hadoop** | 3.3.6 |

### Membres du groupe

| Étudiant | Étudiant |
|----------|----------|
| Komla Petro Asinyo | Kassoum Dene |
| Joel Kazoni Tugirimana | Forbes Magène |
| Frank A Simo Ngounou | Wren Surprenant-Nicolson |

> **Objectif du livrable :** déployer un cluster Hadoop multi-nœuds avec Docker, manipuler HDFS, exécuter un job YARN, publier l’image sur Docker Hub, et documenter les résultats avec captures d’écran et commandes exactes.

---

## Introduction

Ce rapport présente le travail du **groupe G4 — Les_Hadoop_Riders** pour le Projet 1 de l’UA1. Nous avons choisi de déployer et d’exploiter un **cluster Hadoop** (stockage **HDFS** et orchestration **YARN**) entièrement conteneurisé avec **Docker** et **Docker Compose**.

Le document suit la structure de l’énoncé :

1. **Partie 1** — contexte théorique (cas d’usage Big Data, HDFS, YARN) ;
2. **Partie 2** — mise en pratique (déploiement Docker, manipulations HDFS, job YARN) ;
3. **Partie 3** — administration, monitoring et retour d’expérience.

Nous nous sommes appuyés sur une image unique `leshadoopriders/hadoop-tp-g4:1.0`, publiée sur Docker Hub, et sur un dépôt GitHub contenant le code source, les configurations et les scripts de démonstration.

---

## Lexique (sigles utiles)

| Sigle / terme | Signification |
|---------------|---------------|
| **HDFS** | *Hadoop Distributed File System* — système de fichiers distribué |
| **YARN** | *Yet Another Resource Negotiator* — gestionnaire de ressources |
| **3V** | Volume, Vélocité, Variété (caractéristiques du Big Data) |
| **NameNode** | Nœud maître HDFS (namespace / métadonnées) |
| **DataNode** | Nœud de stockage des blocs HDFS |
| **RM / NM** | ResourceManager / NodeManager (YARN) |
| **MapReduce** | Modèle de calcul (phase Map puis Reduce) |
| **Docker Hub** | Registre public d’images Docker |
| **UI** | Interface web (NameNode :9870, YARN :8088) |

---

## Partie 1 — Contexte théorique et architecture (5 pts)

### 1. Cas d’usage Big Data (1.5 pt)

Nous avons choisi le secteur de l’**e-commerce** (commerce électronique).

Exemple concret : une chaîne de magasins qui conserve les tickets de caisse, les logs du site web et les mouvements de stock. Chaque jour le volume grossit, les données arrivent souvent, et les formats changent (CSV, JSON, textes, images produits). Une base relationnelle seule peut devenir insuffisante lorsque les historiques sont très longs et que les formats sont hétérogènes.

Les **3V** du Big Data dans ce contexte :

| V | Signification | Application e-commerce |
|---|---------------|------------------------|
| **Volume** | Quantité de données | Millions d’événements, historique sur plusieurs années |
| **Vélocité** | Vitesse d’arrivée | Commandes et paiements en continu ; réaction rapide (fraude, rupture) |
| **Variété** | Diversité des formats | Tables, logs, JSON, images produits |

Dans ce scénario, **HDFS** permet de stocker ces données de façon distribuée sur plusieurs machines. **YARN** permet ensuite de lancer des traitements (MapReduce, etc.) directement sur le cluster, près des données.

---

### 2. HDFS vs système de fichiers classique (1.5 pt)

| Critère | FS classique (NTFS, ext4…) | **HDFS** |
|---------|----------------------------|----------|
| Emplacement | Une seule machine | Plusieurs machines (cluster) |
| Organisation | Fichier entier sur un disque | Fichier découpé en **blocs** |
| Métadonnées | Gérées par l’OS local | Gérées par le **NameNode** |
| Tolérance aux pannes | Faible (disque unique) | Forte grâce à la **réplication** |
| Contenu des fichiers | Sur le même disque que les métadonnées | Sur les **DataNodes** |

Sur un système local, un fichier vit sur **une** machine. Avec **HDFS**, le fichier est coupé en blocs (souvent 128 Mo), répartis et répliqués sur plusieurs DataNodes. Le NameNode conserve le namespace (noms, dossiers, emplacement des blocs) mais ne stocke pas le contenu des fichiers.

> **En pratique :** le FS local est centralisé ; HDFS est distribué et plus tolérant aux pannes grâce à la réplication. Si un DataNode tombe, d’autres copies du bloc restent disponibles.

---

### 3. Rôle de YARN — ResourceManager et NodeManager (2 pts)

**YARN** (*Yet Another Resource Negotiator*) gère les ressources CPU/mémoire du cluster lorsqu’une application est soumise.

| Composant | Où ? | Rôle |
|-----------|------|------|
| **ResourceManager (RM)** | Master | Reçoit la demande, connaît les ressources, alloue des conteneurs, démarre l’ApplicationMaster |
| **NodeManager (NM)** | Chaque worker | Démarre et surveille les conteneurs **sur sa machine**, remonte l’état au RM |
| **ApplicationMaster** | Conteneur alloué | « Chef » du job : suit l’exécution Map/Reduce |

Enchaînement typique : le client soumet un job → le ResourceManager alloue des ressources → l’ApplicationMaster coordonne le job → les NodeManagers exécutent les tâches dans des conteneurs.

> **À retenir :** le ResourceManager **orchestre** ; le NodeManager **exécute** localement.

---

## Partie 2 — Déploiement et manipulation pratique (15 pts)

### A. Mise en place de l’environnement Docker (4 pts)

#### 1. Déploiement NameNode + 5 DataNodes (1.5 pt)

Nous avons déployé **six conteneurs** sur le réseau Docker `hadoop-net`, à partir d’une image unique dont le rôle (master ou worker) est choisi via la variable d’environnement `HADOOP_ROLE`.

| Conteneur | Rôles |
|-----------|--------|
| `hadoop-master` | NameNode, ResourceManager, SecondaryNameNode |
| `hadoop-worker1` … `hadoop-worker5` | DataNode + NodeManager |

**Ports exposés :**

| Port | Service |
|------|---------|
| **9870** | Interface web HDFS (NameNode UI) |
| **8088** | Interface web YARN |
| **9000** | HDFS RPC |

```bash
docker compose up --build -d
docker ps
```

La commande `up --build -d` construit l’image si nécessaire, crée le réseau et démarre les six services en arrière-plan. `docker ps` permet de vérifier que les conteneurs sont bien *Up*.

![Capture terminal — docker ps / dfsadmin](captures/screenshot-terminal-01.png)

#### 2. Vérification des DataNodes (1.5 pt)

```bash
docker exec -it hadoop-master hdfs dfsadmin -report
```

Cette commande interroge le NameNode et affiche l’état du cluster DFS (capacité, DataNodes vivants, etc.).

> **Résultat observé :** Live datanodes **(5)** — le cluster est opérationnel.  
> Interface NameNode : http://localhost:9870

![UI NameNode](captures/screenshot-namenode.png)

![Liste des DataNodes](captures/screenshot-datanodes.png)

#### 3. Publication de l’image (1 pt)

```bash
docker login
docker push leshadoopriders/hadoop-tp-g4:1.0
```

> **URL publique :** https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4  
> **Note :** Docker Hub impose les minuscules dans le nom de dépôt, d’où `g4` plutôt que `G4`.

---

### B. Manipulation avancée sur HDFS (6 pts)

Pour coller au cas d’usage e-commerce, nous avons préparé un fichier local `data/transactions.csv` (colonnes ID, Date, Montant, Magasin — 10 lignes) et un second fichier `transactions_part2.csv` pour tester la fusion.

#### 4. Répertoires et droits (2 pts)

```bash
hdfs dfs -mkdir -p /data/ventes/2026
hdfs dfs -chmod 755 /data/ventes/2026
hdfs dfs -put -f /data/transactions.csv /data/ventes/2026/
hdfs dfs -chmod 644 /data/ventes/2026/transactions.csv
```

Nous créons l’arborescence `/data/ventes/2026`, appliquons des droits sur le dossier (`755`), uploadons le CSV, puis fixons les droits du fichier (`644`).

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

Le fait d’avoir **un seul bloc** est normal : la taille du fichier est très inférieure à la taille de bloc HDFS (128 Mo). La réplication 3 signifie que ce bloc existe en trois copies sur le cluster.

![Capture terminal — HDFS](captures/screenshot-terminal-02.png)

#### 6. Lecture et concaténation (1 pt)

```bash
hdfs dfs -cat /data/ventes/2026/transactions.csv | head -n 5
hdfs dfs -put -f /data/transactions_part2.csv /data/ventes/2026/
hdfs dfs -getmerge /data/ventes/2026 /tmp/transactions_merged.csv
hdfs dfs -put -f /tmp/transactions_merged.csv /data/ventes/2026/transactions_merged.csv
```

Les 5 premières lignes sont lues directement depuis HDFS. Les deux fichiers du dossier ont ensuite été fusionnés via `getmerge`, puis le résultat a été remis dans HDFS.

#### 7. Suppression / corbeille (1 pt)

```bash
hdfs dfs -rm /data/ventes/2026/transactions_part2.csv
hdfs dfs -D fs.trash.interval=10080 -rm /data/ventes/2026/to_delete.csv
hdfs dfs -ls -R /user/hadoop/.Trash
# suppression définitive :
# hdfs dfs -rm -skipTrash /chemin/fichier
```

> Sans `fs.trash.interval`, la suppression peut être définitive. Avec un intervalle > 0, le fichier passe dans `.Trash`. L’option `-skipTrash` force la suppression définitive, utile pour nettoyer l’espace DFS.

---

### C. Exécution d’un job YARN (5 pts)

Exemple choisi : **calcul de π** par méthode de Monte Carlo, via l’exemple officiel MapReduce fourni avec Hadoop. Cet exemple est pédagogique : il démarre rapidement et permet de vérifier que YARN alloue bien des ressources et que les NodeManagers exécutent les tâches.

```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000
```

Les paramètres `4` et `1000` correspondent à **4** tâches map et **1000** échantillons par map.

| Champ | Résultat |
|-------|----------|
| Application | `application_1791039798429_0001` |
| Nom | QuasiMonteCarlo |
| État final | **SUCCEEDED** |
| Estimation | π ≈ **3.14** |
| Paramètres | 4 maps, 1000 samples |

![Capture terminal — YARN](captures/screenshot-terminal-03.png)

![UI YARN — applications](captures/screenshot-yarn.png)

![Détail application SUCCEEDED](captures/screenshot-yarn-app.png)

---

## Partie 3 — Administration, monitoring et analyse (10 pts)

### 1. Interfaces web (4 pts)

Les interfaces web permettent de contrôler l’état du cluster sans rester uniquement en ligne de commande.

**NameNode — http://localhost:9870**  
Le cluster affiche **5 DataNodes** actifs. L’espace DFS utilisé reste faible (environnement de laboratoire). Aucun *missing block* (bloc manquant) observé pendant nos tests. L’onglet DataNodes confirme que chaque worker est bien enregistré.

**YARN — http://localhost:8088**  
L’application pi apparaît en état **FINISHED / SUCCEEDED**. Les métriques montrent l’allocation mémoire et le temps d’exécution (environ 198589 MB-seconds et 216 vcore-seconds sur un des runs). On peut aussi ouvrir le détail de l’application pour voir les tentatives Map/Reduce.

### 2. Facteur de réplication (3 pts)

```bash
hdfs dfs -setrep -w 2 /data/ventes/2026/transactions.csv
```

> Après la commande, la réplication du fichier passe à **2**. Le NameNode met à jour la cible. Comme on diminuait de 3 à 2, une copie de bloc superflu est retirée sur les DataNodes. L’option `-w` (*wait*) attend la fin de l’opération avant de rendre la main.

Changer la réplication est utile pour équilibrer **fiabilité** (plus de copies) et **coût en espace disque** (moins de copies).

### 3. Retour d’expérience / troubleshooting (3 pts)

| # | Problème | Cause | Solution |
|---|----------|-------|----------|
| 1 | `pull access denied` | Compose téléchargeait une image pas encore sur Hub | `pull_policy: never` + build local |
| 2 | `repository name must be lowercase` | Majuscules dans le tag (`G4`) | Tag final `leshadoopriders/hadoop-tp-g4:1.0` |
| 3 | Build bloqué longtemps | Téléchargement trop lent depuis archive.apache.org | Base `apache/hadoop:3.3.6` + notre config / `entrypoint.sh` |

Ces incidents nous ont permis de mieux comprendre le cycle de vie d’une image Docker (build local → test → push Hub) et les contraintes de nommage de Docker Hub.

---

## Conclusion

Le groupe **Les_Hadoop_Riders** a déployé un cluster Hadoop **1 master + 5 workers** avec Docker, manipulé HDFS (droits, fsck, lecture, fusion, corbeille, setrep), exécuté un job MapReduce π terminé en **SUCCEEDED**, et publié l’image `leshadoopriders/hadoop-tp-g4:1.0` sur Docker Hub.

Ce travail montre qu’un environnement Big Data pédagogique peut être reproduit de façon reproductible grâce à la conteneurisation, tout en couvrant les notions centrales du cours : **3V**, **HDFS**, **YARN**, monitoring et administration de base.

---

## Annexes

### A. Structure du code source

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

### B. Liste des captures

| Fichier | Contenu |
|---------|---------|
| `screenshot-terminal-01.png` | `docker ps` / dfsadmin |
| `screenshot-terminal-02.png` | Manipulations HDFS |
| `screenshot-terminal-03.png` | Sortie job π |
| `screenshot-namenode.png` | UI NameNode |
| `screenshot-datanodes.png` | Liste des 5 DataNodes |
| `screenshot-yarn.png` | UI YARN — applications |
| `screenshot-yarn-app.png` | Détail application SUCCEEDED |

### C. Liens du projet

| Ressource | URL |
|-----------|-----|
| Docker Hub | https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4 |
| GitHub | https://github.com/asinyopetro/Les_Hadoop_Riders_G4 |
| UI NameNode (local) | http://localhost:9870 |
| UI YARN (local) | http://localhost:8088 |
