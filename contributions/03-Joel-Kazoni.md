# Joel Kazoni Tugirimana (joelkazoni) — Partie présentation

## Sujet (2–3 min)
Déploiement Docker : **hadoop-master + worker1…5**, UI NameNode.

## Points à dire
1. `docker compose up --build -d` lance 6 conteneurs sur le réseau `hadoop-net`.
2. Ports : **9870** (HDFS), **8088** (YARN), **9000** (RPC).
3. Vérif : `docker ps` + `hdfs dfsadmin -report` → **5 Live DataNodes**.
4. UI : http://localhost:9870 → onglet Datanodes.
5. Image Hub : `leshadoopriders/hadoop-tp-g4:1.0`.

## Démo live (si possible)
```powershell
cd Les_Hadoop_Riders_G4
docker compose up -d
docker ps
```
Ouvrir http://localhost:9870

## À faire avant le 7 oct
- [ ] Accepter invite GitHub
- [ ] Commit + push
- [ ] Tester que le cluster démarre chez toi

## Validation
- [ ] Validé par Joel — date : ________
