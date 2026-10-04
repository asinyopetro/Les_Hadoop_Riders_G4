# Les_Hadoop_Riders (G4) – Hadoop + Docker

Projet UA1 – cluster HDFS/YARN avec 1 master et 5 workers.

Image Hub : `leshadoopriders/hadoop-tp-g4:1.0`  
https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4

## Lancer le cluster

```powershell
cd "C:\Users\asiny\Desktop\Les_Hadoop_Riders_G4"
docker compose up --build -d
```

Attendre 1–2 min, puis :

```powershell
docker ps
docker exec -it hadoop-master hdfs dfsadmin -report
```

- NameNode : http://localhost:9870  
- YARN : http://localhost:8088  

## Entrer dans le master

```powershell
docker exec -it hadoop-master bash
```

## HDFS (résumé)

```bash
hdfs dfs -mkdir -p /data/ventes/2026
hdfs dfs -put -f /data/transactions.csv /data/ventes/2026/
hdfs fsck /data/ventes/2026/transactions.csv -files -blocks -locations
hdfs dfs -cat /data/ventes/2026/transactions.csv | head -n 5
hdfs dfs -setrep -w 2 /data/ventes/2026/transactions.csv
```

Ou : `bash /opt/hadoop/tmp/demo-hdfs.sh` (après copie du script).

## Job pi

```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000
```

## Arrêter

```powershell
docker compose down
# reset HDFS :
docker compose down -v
```

Squelette de départ : https://github.com/Ous-data/hadoop-cluster-docker  
(adapté en multi-nœuds pour le TP)
