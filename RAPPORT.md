# UA1 – Projet 1 : Cluster Hadoop avec Docker

**Groupe G4 – Les_Hadoop_Riders**

| | |
|---|---|
| Image Docker Hub | `leshadoopriders/hadoop-tp-g4:1.0` |
| Lien | https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4 |
| Remise | 4 octobre 2026 |
| Présentation | 8 octobre 2026 |

**Équipe :** Komla Petro Asinyo, Kassoum Dene, Joel Kazoni Tugirimana, Forbes Magène, Frank A Simo Ngounou, Wren Surprenant-Nicolson

On s’est basés sur le dépôt du cours (hadoop-cluster-docker), puis on a adapté la config pour avoir un vrai cluster avec 1 master et 5 workers, comme demandé dans l’énoncé.

---

## Partie 1 – Théorie

### 1. Cas d’usage Big Data (e-commerce)

On a choisi l’e-commerce, parce que ça colle bien avec notre fichier `transactions.csv` (ventes par magasin).

Imaginons une chaîne de magasins qui reçoit des milliers de transactions par jour (caisse + site web). Le problème, c’est pas juste « stocker un Excel » :

- **Volume** : l’historique sur plusieurs années devient énorme (transactions, logs de navigation, stocks).
- **Vélocité** : les données arrivent en continu. Si on attend le lendemain pour analyser, on rate des alertes (fraude, rupture de stock).
- **Variété** : on a du CSV, du JSON, des logs texte, parfois des images produits. Ce n’est pas un seul format propre.

Dans ce contexte, HDFS sert à stocker tout ça sur plusieurs machines, et YARN à lancer des traitements dessus sans tout faire sur un seul PC.

### 2. HDFS vs système de fichiers classique

Sur Windows/Linux classique (NTFS, ext4), un fichier est sur **un** disque / **une** machine. Si le disque lâche et qu’on n’a pas de backup, c’est fini.

Sur HDFS, le fichier est découpé en **blocs**. Ces blocs sont copiés sur plusieurs DataNodes (réplication). Le NameNode garde la « carte » : quel bloc est où. Du coup :

- on peut lire en parallèle ;
- si un worker tombe, les autres ont encore une copie.

C’est ça la grosse différence : local = centralisé ; HDFS = distribué + répliqué.

### 3. ResourceManager vs NodeManager

Quand on lance un job (ex. calcul de pi) :

- Le **ResourceManager** (sur le master) regarde les ressources du cluster et décide où placer les tâches.
- Le **NodeManager** (sur chaque worker) exécute vraiment les conteneurs sur sa machine et dit au RM si ça va ou pas.

En gros : le RM organise, les NM font le travail.

---

## Partie 2 – Pratique

### A. Docker : master + 5 workers

On a construit une image et lancé 6 conteneurs avec Docker Compose.

```bash
docker compose up --build -d
docker ps
```

Conteneurs : `hadoop-master`, `hadoop-worker1` … `hadoop-worker5`  
Réseau : `hadoop-net`  
Ports ouverts sur la machine : 9870 (HDFS UI), 8088 (YARN), 9000 (HDFS).

Capture terminal (docker ps + rapport DataNodes) :

![Terminal Docker / dfsadmin](captures/screenshot-terminal-01.png)

Pour vérifier les DataNodes :

```bash
docker exec -it hadoop-master hdfs dfsadmin -report
```

On obtient bien **Live datanodes (5)**.  
UI : http://localhost:9870

![NameNode](captures/screenshot-namenode.png)

![DataNodes](captures/screenshot-datanodes.png)

#### Publication Docker Hub

Compte créé : **leshadoopriders**

```bash
docker login
docker push leshadoopriders/hadoop-tp-g4:1.0
```

Lien public : https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4  

Petit détail : Docker refuse les majuscules dans le nom d’image, donc on a mis `g4` et pas `G4`.

---

### B. Manipulations HDFS

Création du dossier, droits, et upload du CSV (fichier préparé dans `data/transactions.csv`) :

```bash
hdfs dfs -mkdir -p /data/ventes/2026
hdfs dfs -chmod 755 /data/ventes/2026
hdfs dfs -put -f /data/transactions.csv /data/ventes/2026/
hdfs dfs -chmod 644 /data/ventes/2026/transactions.csv
hdfs dfs -ls -d /data/ventes/2026
hdfs dfs -ls /data/ventes/2026/transactions.csv
hdfs fsck /data/ventes/2026/transactions.csv -files -blocks -locations
hdfs dfs -stat "%n | taille=%b | replication=%r | block_size=%o" /data/ventes/2026/transactions.csv
```

Après `chmod`, on voit bien `drwxr-xr-x` sur le dossier et `-rw-r--r--` sur le fichier (preuve : `captures/12-droits-chmod.txt`).

Capture terminal HDFS (`ls`, `head`, `fsck`) :

![Terminal HDFS](captures/screenshot-terminal-02.png)

Ce qu’on a vu chez nous :
- taille ≈ 377 octets
- réplication de départ = 3
- 1 seul bloc (normal, le fichier est petit ; la taille de bloc par défaut est 128 Mo)
- fsck : HEALTHY

Lecture des 5 premières lignes **depuis HDFS** (sans re-télécharger le fichier à la main) :

```bash
hdfs dfs -cat /data/ventes/2026/transactions.csv | head -n 5
```

Ensuite on a ajouté `transactions_part2.csv`, puis fusionné avec `getmerge` :

```bash
hdfs dfs -put -f /data/transactions_part2.csv /data/ventes/2026/
hdfs dfs -getmerge /data/ventes/2026 /tmp/transactions_merged.csv
hdfs dfs -put -f /tmp/transactions_merged.csv /data/ventes/2026/transactions_merged.csv
```

Pour la suppression / corbeille :

```bash
hdfs dfs -rm /data/ventes/2026/transactions_part2.csv
# pour forcer la corbeille :
hdfs dfs -D fs.trash.interval=10080 -rm /data/ventes/2026/to_delete.csv
hdfs dfs -ls -R /user/hadoop/.Trash
# suppression définitive :
# hdfs dfs -rm -skipTrash ...
```

Au début, la corbeille n’était pas activée (intervalle à 0), donc le fichier disparaissait direct. En mettant `fs.trash.interval`, on a bien vu le fichier arriver dans `.Trash`.

Preuves terminal : `captures/01-demo-hdfs.txt`, `captures/10-trash.txt`.

---

### C. Job YARN – calcul de pi

On a choisi l’exemple pi (Monte Carlo), comme dans l’énoncé :

```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000
```

Résultat :
- Application : `application_1791039798429_0001`
- Nom : QuasiMonteCarlo
- État final : **SUCCEEDED**
- Estimation de π ≈ **3.14**
- 4 maps, puis reduce à 100%

Capture terminal YARN (`yarn application -list` / status) :

![Terminal YARN](captures/screenshot-terminal-03.png)

![YARN](captures/screenshot-yarn.png)

![Job SUCCEEDED](captures/screenshot-yarn-app.png)

Après le job, on a eu un warning parce que le JobHistory Server (port 10020) n’était pas lancé. Le job était quand même réussi dans l’UI YARN (8088), donc on a gardé ça comme point de troubleshooting.

---

## Partie 3 – Monitoring et analyse

### Interfaces web

**NameNode (9870)**  
On voit l’espace disque (chez nous ça affiche une grosse capacité à cause de Docker/WSL) et surtout les **5 DataNodes live**. Pas de missing blocks sur nos tests.

**YARN (8088)**  
On retrouve l’appli pi en FINISHED / SUCCEEDED, avec le temps et la mémoire consommée (environ 198589 MB-seconds et 216 vcore-seconds).

### Changement du facteur de réplication

```bash
hdfs dfs -setrep -w 2 /data/ventes/2026/transactions.csv
```

Après la commande : replication = 2.  
Hadoop met à jour la cible côté NameNode. Comme on descendait de 3 à 2, il a juste enlevé une copie en trop sur les DataNodes. L’option `-w` attend que ce soit fini avant de rendre la main.

### Problèmes qu’on a eus (et comment on a réglé)

1. **Compose essayait de pull l’image sur Docker Hub alors qu’elle n’existait pas encore**  
   Erreur du style `pull access denied`.  
   Fix : `pull_policy: never` + build local d’abord.

2. **Nom d’image avec majuscules (`G4`)**  
   Docker refuse.  
   Fix : `leshadoopriders/hadoop-tp-g4:1.0`.

3. **Build trop long** (téléchargement Hadoop depuis archive.apache.org très lent)  
   On est partis sur l’image `apache/hadoop:3.3.6` et on a mis nos configs + entrypoint par-dessus pour avoir master/workers.

---

## Annexes

### Commandes utiles

```bash
docker compose up --build -d
docker exec -it hadoop-master bash
hdfs dfsadmin -report
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000
docker push leshadoopriders/hadoop-tp-g4:1.0
```

### Contenu du dossier rendu

- `Dockerfile`, `docker-compose.yml`, `entrypoint.sh`
- `config/` (core-site, hdfs-site, yarn-site, mapred-site, workers)
- `data/` (CSV)
- `scripts/` (démos)
- `captures/` (preuves)
- ce rapport

### Qui présente quoi (8 octobre)

À répartir dans le groupe (exemple) :
1. Cas e-commerce / 3V  
2. Architecture Docker + preuve des 5 DataNodes  
3. Commandes HDFS  
4. Job pi + UI YARN  
5. setrep + monitoring  
6. Troubleshooting + lien Docker Hub  

Présence obligatoire le 8 octobre.
