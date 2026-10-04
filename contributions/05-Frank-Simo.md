# Frank A Simo Ngounou (Frank-Bleriot) — Partie présentation

## Sujet (2–3 min)
Job **YARN / MapReduce** : calcul de π + UI 8088.

## Points à dire
1. Commande:
   `yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000`
2. Principe : Monte Carlo, 4 maps, YARN alloue les conteneurs.
3. Résultat : application **SUCCEEDED**, π ≈ 3.14.
4. UI : http://localhost:8088 → Apps FINISHED.
5. ID exemple : `application_1791039798429_0001`.

## Démo live
```bash
docker exec -it hadoop-master bash
yarn application -list -appStates ALL
```
Puis ouvrir http://localhost:8088

## À faire avant le 7 oct
- [ ] Déjà dans le repo (OK)
- [ ] Commit + push
- [ ] Relancer le job pi une fois si besoin

## Validation
- [ ] Validé par Frank — date : 2026-10-03
