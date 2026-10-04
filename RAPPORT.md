# Projet 1 — Déploiement et Exploitation d’un Cluster Hadoop avec Docker

| | |
|:--|:--|
| **Cours** | Bases de données massives avancées (**IFM30522**) |
| **Unité** | UA1 — Projet 1 |
| **Groupe** | **G4 — Les_Hadoop_Riders** |
| **Image Docker** | `leshadoopriders/hadoop-tp-g4:1.0` |
| **Docker Hub** | https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4 |
| **Code source** | https://github.com/asinyopetro/Les_Hadoop_Riders_G4 |

### Membres du groupe

| Étudiant | Étudiant |
|----------|----------|
| Komla Petro Asinyo | Kassoum Dene |
| Joel Kazoni Tugirimana | Forbes Magène |
| Frank A Simo Ngounou | Wren Surprenant-Nicolson |

> **Objectif du livrable :** déployer un cluster Hadoop multi-nœuds avec Docker, manipuler HDFS, exécuter un job YARN, publier l’image sur Docker Hub, et documenter les résultats avec captures.

---

## Partie 1 — Contexte théorique et architecture (5 pts)

### 1. Cas d’usage Big Data (1.5 pt)

Nous avons choisi le secteur de l’**e-commerce** (commerce électronique).

Exemple concret : une chaîne de magasins qui conserve les tickets de caisse, les logs du site web et les mouvements de stock. Chaque jour le volume grossit, les données arrivent souvent, et les formats changent (CSV, JSON, textes, images produits).

Les **3V** du Big Data dans ce contexte :

| V | Signification | Application e-commerce |
|---|---------------|------------------------|
| **Volume** | Quantité de données | Millions d’événements, historique sur plusieurs années |
| **Vélocité** | Vitesse d’arrivée | Commandes et paiements en continu ; réaction rapide (fraude, rupture) |
| **Variété** | Diversité des formats | Tables, logs, JSON, images produits |

**HDFS** permet de stocker ces données de façon distribuée. **YARN** permet de lancer des traitements (MapReduce, etc.) sur le cluster.

---

### 2. HDFS vs système de fichiers classique (1.5 pt)

| Critère | FS classique (NTFS, ext4…) | **HDFS** |
|---------|----------------------------|----------|
| Emplacement | Une seule machine | Plusieurs machines (cluster) |
| Organisation | Fichier entier sur un disque | Fichier découpé en **blocs** |
| Métadonnées | Gérées par l’OS local | Gérées par le **NameNode** |
| Tolérance aux pannes | Faible (disque unique) | Forte grâce à la **réplication** |
| Contenu des fichiers | Sur le même disque que les métadonnées | Sur les **DataNodes** |

Sur un système local, un fichier vit sur **une** machine. Avec **HDFS**, le fichier est coupé en blocs, répartis et répliqués sur plusieurs DataNodes. Le NameNode conserve le namespace (noms, dossiers, emplacement des blocs).

> **En pratique :** le FS local est centralisé ; HDFS est distribué et plus tolérant aux pannes grâce à la réplication.

---

### 3. Rôle de YARN — ResourceManager et NodeManager (2 pts)

**YARN** (*Yet Another Resource Negotiator*) gère les ressources CPU/mémoire du cluster lorsqu’une application est soumise.

| Composant | Où ? | Rôle |
|-----------|------|------|
| **ResourceManager (RM)** | Master | Reçoit la demande, connaît les ressources, alloue des conteneurs, démarre l’ApplicationMaster |
| **NodeManager (NM)** | Chaque worker | Démarre et surveille les conteneurs **sur sa machine**, remonte l’état au RM |
| **ApplicationMaster** | Conteneur alloué | « Chef » du job : suit l’exécution Map/Reduce |

> **À retenir :** le ResourceManager **orchestre** ; le NodeManager **exécute** localement.

---

## Partie 2 — Déploiement et manipulation pratique (15 pts)

### A. Mise en place de l’environnement Docker (4 pts)

#### 1. Déploiement NameNode + 5 DataNodes (1.5 pt)

Nous avons déployé **six conteneurs** sur le réseau Docker `hadoop-net` :

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

![Capture terminal — docker ps / dfsadmin](captures/screenshot-terminal-01.png)

#### 2. Vérification des DataNodes (1.5 pt)

```bash
docker exec -it hadoop-master hdfs dfsadmin -report
```

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
> **Note :** Docker Hub impose les minuscules, d’où `g4` plutôt que `G4`.

---

### B. Manipulation avancée sur HDFS (6 pts)

#### 4. Répertoires et droits (2 pts)

Fichier local préparé : `data/transactions.csv` (colonnes ID, Date, Montant, Magasin — 10 lignes).

```bash
hdfs dfs -mkdir -p /data/ventes/2026
hdfs dfs -chmod 755 /data/ventes/2026
hdfs dfs -put -f /data/transactions.csv /data/ventes/2026/
hdfs dfs -chmod 644 /data/ventes/2026/transactions.csv
```

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

![Capture terminal — HDFS](captures/screenshot-terminal-02.png)

#### 6. Lecture et concaténation (1 pt)

```bash
hdfs dfs -cat /data/ventes/2026/transactions.csv | head -n 5
hdfs dfs -put -f /data/transactions_part2.csv /data/ventes/2026/
hdfs dfs -getmerge /data/ventes/2026 /tmp/transactions_merged.csv
hdfs dfs -put -f /tmp/transactions_merged.csv /data/ventes/2026/transactions_merged.csv
```

Les 5 premières lignes sont lues directement depuis HDFS. Les deux fichiers ont été fusionnés via `getmerge`.

#### 7. Suppression / corbeille (1 pt)

```bash
hdfs dfs -rm /data/ventes/2026/transactions_part2.csv
hdfs dfs -D fs.trash.interval=10080 -rm /data/ventes/2026/to_delete.csv
hdfs dfs -ls -R /user/hadoop/.Trash
# suppression définitive :
# hdfs dfs -rm -skipTrash /chemin/fichier
```

> Sans `fs.trash.interval`, la suppression peut être définitive. Avec un intervalle > 0, le fichier passe dans `.Trash`. L’option `-skipTrash` force la suppression définitive.

---

### C. Exécution d’un job YARN (5 pts)

Exemple choisi : **calcul de π** par méthode de Monte Carlo (exemple officiel MapReduce).

```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000
```

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

**NameNode — http://localhost:9870**  
Le cluster affiche **5 DataNodes** actifs. L’espace DFS utilisé reste faible (environnement de laboratoire). Aucun *missing block* observé pendant nos tests.

**YARN — http://localhost:8088**  
L’application pi apparaît en état **FINISHED / SUCCEEDED**. Les métriques montrent l’allocation mémoire et le temps d’exécution (environ 198589 MB-seconds et 216 vcore-seconds sur un des runs).

### 2. Facteur de réplication (3 pts)

```bash
hdfs dfs -setrep -w 2 /data/ventes/2026/transactions.csv
```

> Après la commande, la réplication du fichier passe à **2**. Le NameNode met à jour la cible. Comme on diminuait de 3 à 2, une copie de bloc superflu est retirée. L’option `-w` attend la fin de l’opération.

### 3. Retour d’expérience / troubleshooting (3 pts)

| # | Problème | Cause | Solution |
|---|----------|-------|----------|
| 1 | `pull access denied` | Compose téléchargeait une image pas encore sur Hub | `pull_policy: never` + build local |
| 2 | `repository name must be lowercase` | Majuscules dans le tag (`G4`) | Tag final `leshadoopriders/hadoop-tp-g4:1.0` |
| 3 | Build bloqué longtemps | Téléchargement trop lent depuis archive.apache.org | Base `apache/hadoop:3.3.6` + notre config / `entrypoint.sh` |

---

## Annexes

### Structure du code source

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

### Liens du projet

| Ressource | URL |
|-----------|-----|
| Docker Hub | https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4 |
| GitHub | https://github.com/asinyopetro/Les_Hadoop_Riders_G4 |
| UI NameNode (local) | http://localhost:9870 |
| UI YARN (local) | http://localhost:8088 |
