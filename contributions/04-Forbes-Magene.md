# Forbes Magène (formagene-sys) — Partie présentation

## Sujet (2–3 min)
Manipulations **HDFS** (création, droits, blocs, lecture, merge, corbeille).

## Points à dire
1. Arborescence : `/data/ventes/2026` + `transactions.csv`.
2. Droits : `hdfs dfs -chmod 755` / `644`.
3. `fsck` / `stat` : taille, réplication (=3 au départ), 1 bloc (fichier petit).
4. `hdfs dfs -cat ... | head -n 5` sans tout retélécharger.
5. `getmerge` pour fusionner part1 + part2.
6. Corbeille `.Trash` avec `fs.trash.interval` ; sinon `-skipTrash`.

## Démo live
```bash
docker exec -it hadoop-master bash
hdfs dfs -ls /data/ventes/2026
hdfs dfs -cat /data/ventes/2026/transactions.csv | head -n 5
```

## À faire avant le 7 oct
- [ ] Accepter invite : https://github.com/asinyopetro/Les_Hadoop_Riders_G4/invitations
- [ ] Commit + push
- [ ] Relancer les commandes une fois

## Validation
- [ ] Validé par Forbes — date : ________
