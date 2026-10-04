# Les_Hadoop_Riders (G4)

Projet UA1 — Cluster Hadoop (HDFS + YARN) avec Docker.

- Image : `leshadoopriders/hadoop-tp-g4:1.0`
- Docker Hub : https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4

## Démarrage

```powershell
docker compose up --build -d
docker ps
docker exec -it hadoop-master hdfs dfsadmin -report
```

- NameNode : http://localhost:9870  
- YARN : http://localhost:8088  

```powershell
docker exec -it hadoop-master bash
```

## Scripts

```bash
# depuis le master
bash /opt/hadoop/tmp/demo-hdfs.sh
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000
```

Copier les scripts :

```powershell
docker cp scripts/demo-hdfs.sh hadoop-master:/opt/hadoop/tmp/
docker cp scripts/demo-yarn-pi.sh hadoop-master:/opt/hadoop/tmp/
```

## Arrêt

```powershell
docker compose down
docker compose down -v
```

Base pédagogique : https://github.com/Ous-data/hadoop-cluster-docker
